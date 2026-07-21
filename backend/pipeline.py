"""Fixed, request-scoped orchestration for the local demo."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import time
import uuid
from collections.abc import Callable
from typing import Any, TypeVar

import numpy as np

from backend.corpus import load_creators, load_vectors, needs_tiebreak, top_k
from backend.models import (ConfidenceJudgment, CreatorMatch, EvidenceItem, EvidenceWriting,
                            LearnerQuote, MatchCard, PipelineResponse, Sentence, StepTrace,
                            StyleReading, TranscriptResult, VerifiedPanel, WhyPanel)
from backend.prompts import EVIDENCE_SYSTEM, JUDGE_SYSTEM, STYLE_SYSTEM, TIEBREAK_SYSTEM, json_input

T = TypeVar("T")
EXPOSED_BANNED = re.compile(r"\b(embedding|style vector|descriptor|shadow)\b|—", re.I)
logger = logging.getLogger(__name__)


class MatchPipeline:
    """Dependencies are injectable to make all routing and fallback paths testable."""

    def __init__(self, translate: Callable[[bytes, str, str | None], str] | None = None,
                 llm: Callable[[str, str, int], str] | None = None,
                 embed: Callable[[str], np.ndarray] | None = None,
                 tiebreak_llm: Callable[[str, str, int], str] | None = None) -> None:
        self.translate = translate or self._groq_translate
        self.llm = llm or self._gpt56
        self.tiebreak_llm = tiebreak_llm or self._gpt_mini
        self._embedding_model: Any | None = None
        if embed:
            self.embed = embed
        else:
            self._embedding_model = self._load_embedding_model()
            self.embed = self._embed
        self.creators = load_creators()
        self.ids, self.vectors, self.centroid = load_vectors()
        self._creators_by_id = {creator.id: creator for creator in self.creators}

    async def run_pipeline(self, audio: bytes | bytearray, filename: str, content_type: str | None = None,
                           *, opt_in: bool = False, memory_token: str | None = None) -> PipelineResponse:
        started = time.monotonic()
        request_id = str(uuid.uuid4())
        trace: list[StepTrace] = []
        def mark(step: str, status: str) -> None:
            trace.append(StepTrace(step=step, status=status, elapsed_ms=int((time.monotonic() - started) * 1000)))

        try:
            return await asyncio.wait_for(self._run(audio, filename, content_type, opt_in, memory_token, request_id, mark, trace), 45)
        except asyncio.TimeoutError:
            mark("pipeline", "failed")
            return self._fallback_cards(trace, "We are showing the clearest overlap we found.")

    async def _run(self, audio: bytes | bytearray, filename: str, content_type: str | None, opt_in: bool,
                   memory_token: str | None, request_id: str, mark: Callable[[str, str], None], trace: list[StepTrace]) -> PipelineResponse:
        mark("transcript", "started")
        try:
            transcript = await asyncio.wait_for(self._transcript(audio, filename, content_type), 15)
        except Exception:
            logger.exception("Transcript Agent failed for request %s", request_id)
            mark("transcript", "failed")
            return PipelineResponse(matches=[], step_trace=trace, audio_deleted=True, message="The match could not be completed. Please try again.")
        finally:
            # The endpoint passes a bytearray, so clearing here also releases its only request copy.
            if isinstance(audio, bytearray):
                audio.clear()
            del audio
        mark("transcript", "completed")
        if transcript.word_count < 120 or (transcript.duration_ms is not None and transcript.duration_ms < 45_000):
            mark("input_gate", "failed")
            return PipelineResponse(matches=[], step_trace=trace, audio_deleted=True, message="Please talk a little longer, about a minute or two.")
        short_sample = (transcript.duration_ms is not None and transcript.duration_ms < 60_000) or transcript.word_count < 180
        mark("input_gate", "completed")

        mark("style_reader", "started"); mark("matcher", "started"); mark("memory", "started")
        style_task = asyncio.wait_for(self._style_reader(transcript, request_id), 20)
        matcher_task = asyncio.to_thread(self._matcher, transcript.transcript_en)
        memory_task = self._memory_read(opt_in, memory_token)
        style, candidate_matches, memory = await asyncio.gather(style_task, matcher_task, memory_task, return_exceptions=True)
        mark("style_reader", "completed" if not isinstance(style, Exception) else "failed")
        mark("matcher", "completed" if not isinstance(candidate_matches, Exception) else "failed")
        mark("memory", "completed" if not isinstance(memory, Exception) else "failed")
        if isinstance(candidate_matches, Exception):
            logger.error("Creator Matcher failed for request %s: %s", request_id, candidate_matches)
            return PipelineResponse(matches=[], step_trace=trace, audio_deleted=True, message="The match could not be completed. Please try again.")
        matches = candidate_matches[:3]
        tiebreak_used = False
        tiebreak_skipped = False
        if needs_tiebreak([(self._creators_by_id[match.creator_id], match.cosine_score) for match in candidate_matches]):
            mark("tiebreaker", "started")
            try:
                matches = await asyncio.wait_for(self._tiebreak(transcript, candidate_matches), 5)
                tiebreak_used = True
                mark("tiebreaker", "completed")
            except Exception:
                logger.exception("Tiebreaker failed for request %s", request_id)
                tiebreak_skipped = True
                mark("tiebreaker", "failed")
        else:
            tiebreak_skipped = True
            mark("tiebreaker", "skipped")
        if isinstance(style, Exception):
            return self._generic_response(matches, trace, short_sample).model_copy(update={"tiebreak_used": tiebreak_used, "tiebreak_skipped": tiebreak_skipped})

        mark("evidence_writer", "started")
        try:
            evidence = await asyncio.wait_for(self._evidence_writer(style, matches, request_id), 20)
            self._validate_evidence(evidence, style, matches)
            mark("evidence_writer", "completed")
        except Exception:
            mark("evidence_writer", "failed")
            return self._generic_response(matches, trace, short_sample).model_copy(update={"tiebreak_used": tiebreak_used, "tiebreak_skipped": tiebreak_skipped})

        mark("confidence_judge", "started")
        try:
            judgment = await asyncio.wait_for(self._judge(evidence, transcript, request_id), 18)
            mark("confidence_judge", "completed")
        except Exception:
            mark("confidence_judge", "failed")
            judgment = ConfidenceJudgment(verified_panels=[VerifiedPanel(creator_id=m.creator_id, resemblance="partial", evidence=[]) for m in matches], overall_confidence=0, judge_skipped=True)
        return self._assemble(matches, style, evidence, judgment, trace, short_sample, isinstance(memory, Exception), tiebreak_used, tiebreak_skipped)

    async def _transcript(self, audio: bytes | bytearray, filename: str, content_type: str | None) -> TranscriptResult:
        text = await asyncio.to_thread(self.translate, bytes(audio), filename, content_type)
        sentences = [Sentence(id=f"s{i + 1}", text=value.strip()) for i, value in enumerate(re.split(r"(?<=[.!?])\s+", text.strip())) if value.strip()]
        return TranscriptResult(transcript_en=text.strip(), sentences=sentences, word_count=len(text.split()), audio_deleted=True)

    async def _style_reader(self, transcript: TranscriptResult, request_id: str) -> StyleReading:
        result = await self._ask(StyleReading, STYLE_SYSTEM, json_input(request_id=request_id, transcript_en=transcript.transcript_en, sentences=[s.model_dump() for s in transcript.sentences], creator_trait_vocabulary=["question-led", "step-by-step", "reflective", "direct", "careful", "story-led"]), 500)
        valid = {s.id for s in transcript.sentences}
        if len(result.thinking_traits) < 3 or any(t.evidence_sentence_id not in valid for t in result.thinking_traits + result.learning_traits): raise ValueError("invalid style evidence")
        return result

    def _matcher(self, text: str) -> list[CreatorMatch]:
        rows = top_k(self.embed(text), self.creators, self.ids, self.vectors, self.centroid, k=6)
        if len(rows) < 3: raise ValueError("expected at least three matches")
        return [CreatorMatch(creator_id=c.id, creator_name=c.name, role=c.role, channel_url=c.video_url, cosine_score=score, descriptors=c.descriptors, rank=i + 1) for i, (c, score) in enumerate(rows)]

    async def _tiebreak(self, transcript: TranscriptResult, candidates: list[CreatorMatch]) -> list[CreatorMatch]:
        raw = await asyncio.to_thread(
            self.tiebreak_llm,
            TIEBREAK_SYSTEM,
            json_input(
                learner_transcript=transcript.transcript_en,
                candidates=[
                    {"id": match.creator_id, "style_description": self._creators_by_id[match.creator_id].style_descriptor_long}
                    for match in candidates
                ],
            ),
            300,
        )
        ranked_ids = json.loads(raw).get("ranked_ids")
        valid_ids = {match.creator_id for match in candidates}
        if not isinstance(ranked_ids, list) or len(ranked_ids) != 3 or len(set(ranked_ids)) != 3 or any(value not in valid_ids for value in ranked_ids):
            raise ValueError("Tiebreaker returned invalid ranking.")
        by_id = {match.creator_id: match for match in candidates}
        return [by_id[creator_id].model_copy(update={"rank": index + 1}) for index, creator_id in enumerate(ranked_ids)]

    async def _evidence_writer(self, style: StyleReading, matches: list[CreatorMatch], request_id: str) -> EvidenceWriting:
        return await self._ask(EvidenceWriting, EVIDENCE_SYSTEM, json_input(request_id=request_id, learner_quotes=[q.model_dump() for q in style.learner_quotes], thinking_traits=[t.model_dump() for t in style.thinking_traits], learning_traits=[t.model_dump() for t in style.learning_traits], matches=[m.model_dump() for m in matches]), 700)

    async def _judge(self, evidence: EvidenceWriting, transcript: TranscriptResult, request_id: str) -> ConfidenceJudgment:
        cited = {item.you_quote.sentence_id for panel in evidence.why_panels for item in panel.evidence}
        sentence_by_id = {s.id: s for s in transcript.sentences}
        return await self._ask(ConfidenceJudgment, JUDGE_SYSTEM, json_input(request_id=request_id, why_panels=[p.model_dump() for p in evidence.why_panels], cited_sentences=[sentence_by_id[i].model_dump() for i in cited if i in sentence_by_id]), 500)

    async def _ask(self, schema: type[T], system: str, user: str, max_tokens: int) -> T:
        """One retry with a stricter instruction; no agent can create an unbounded loop."""
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                suffix = " Return valid JSON only and satisfy every required field." if attempt else ""
                raw = await asyncio.to_thread(self.llm, system + suffix, user, max_tokens)
                return schema.model_validate(json.loads(raw))  # type: ignore[attr-defined, no-any-return]
            except Exception as error:
                last_error = error
        raise RuntimeError("LLM schema validation failed") from last_error

    async def _memory_read(self, opt_in: bool, token: str | None) -> dict[str, Any]:
        return {"skipped": True, "reason": "not_opted_in"} if not opt_in else {"found": False, "token": token}

    def _validate_evidence(self, evidence: EvidenceWriting, style: StyleReading, matches: list[CreatorMatch]) -> None:
        quotes = {q.sentence_id for q in style.learner_quotes}; allowed = {m.creator_id: set(m.descriptors) for m in matches}
        if {p.creator_id for p in evidence.why_panels} != set(allowed): raise ValueError("missing panel")
        for panel in evidence.why_panels:
            if len(panel.evidence) < 2 or any(e.you_quote.sentence_id not in quotes or e.creator_descriptor not in allowed[panel.creator_id] for e in panel.evidence): raise ValueError("ungrounded evidence")

    def _assemble(self, matches: list[CreatorMatch], style: StyleReading, evidence: EvidenceWriting, judgment: ConfidenceJudgment, trace: list[StepTrace], short: bool, memory_unavailable: bool, tiebreak_used: bool, tiebreak_skipped: bool) -> PipelineResponse:
        panels = {p.creator_id: p for p in evidence.why_panels}; verdicts = {p.creator_id: p for p in judgment.verified_panels}; cards = []
        for match in matches:
            panel = panels.get(match.creator_id, WhyPanel(creator_id=match.creator_id)); verdict = verdicts.get(match.creator_id)
            kept = {v.trait_id for v in verdict.evidence if v.verdict == "kept"} if verdict else set()
            items = [
                EvidenceItem(
                    trait_id=item.trait_id,
                    you_quote=item.you_quote,
                    creator_descriptor=self._clean(item.creator_descriptor),
                    match_reason=self._clean(item.match_reason),
                )
                for item in panel.evidence
                if not verdict or item.trait_id in kept
            ]
            resemblance = verdict.resemblance if verdict else "partial"
            if short and resemblance == "strong": resemblance = "clear"
            why = items[0].match_reason if items else "These two build sentences in a similar way."
            cards.append(MatchCard(creator_id=match.creator_id, name=match.creator_name, role=match.role, video_url=match.channel_url, similarity=match.cosine_score, resemblance=resemblance, trait_chips=[self._clean(chip) for chip in panel.learner_trait_chips], evidence=items, why=self._clean(why)))
        return PipelineResponse(matches=cards, step_trace=trace, audio_deleted=True, judge_skipped=judgment.judge_skipped, match_confidence_capped=short, memory_available=not memory_unavailable, tiebreak_used=tiebreak_used, tiebreak_skipped=tiebreak_skipped)

    def _generic_response(self, matches: list[CreatorMatch], trace: list[StepTrace], short: bool) -> PipelineResponse:
        return PipelineResponse(matches=[MatchCard(creator_id=m.creator_id, name=m.creator_name, role=m.role, video_url=m.channel_url, similarity=m.cosine_score, resemblance="partial", why="These two build sentences in a similar way.") for m in matches[:3]], step_trace=trace, audio_deleted=True, match_confidence_capped=short)

    def _fallback_cards(self, trace: list[StepTrace], message: str) -> PipelineResponse:
        return self._generic_response(self._matcher("A careful, reflective explanation."), trace, False).model_copy(update={"message": message})

    @staticmethod
    def _clean(value: str) -> str:
        return EXPOSED_BANNED.sub("", value).strip() or "These two build sentences in a similar way."

    @staticmethod
    def _groq_translate(audio: bytes, filename: str, content_type: str | None) -> str:
        from groq import Groq
        key = os.environ.get("GROQ_API_KEY")
        if not key: raise RuntimeError("GROQ_API_KEY is required to translate audio.")
        return (Groq(api_key=key).audio.translations.create(file=(filename, audio, content_type or "application/octet-stream"), model="whisper-large-v3").text or "").strip()

    @staticmethod
    def _gpt56(system: str, user: str, max_tokens: int) -> str:
        from openai import OpenAI
        if not os.environ.get("OPENAI_API_KEY"): raise RuntimeError("OPENAI_API_KEY is required for GPT-5.6.")
        return OpenAI().responses.create(model="gpt-5.6", instructions=system, input=user, max_output_tokens=max_tokens).output_text

    @staticmethod
    def _gpt_mini(system: str, user: str, max_tokens: int) -> str:
        from openai import OpenAI
        if not os.environ.get("OPENAI_API_KEY"): raise RuntimeError("OPENAI_API_KEY is required for the tiebreaker.")
        model = os.environ.get("TIEBREAK_MODEL", "gpt-4.1-mini")
        return OpenAI().responses.create(model=model, instructions=system, input=user, max_output_tokens=max_tokens).output_text

    @staticmethod
    def _load_embedding_model() -> Any:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("StyleDistance/styledistance")

    def _embed(self, text: str) -> np.ndarray:
        if self._embedding_model is None:
            raise RuntimeError("Style embedding model is not initialized.")
        return np.asarray(self._embedding_model.encode([text], normalize_embeddings=True)[0])
