from __future__ import annotations

import asyncio
import json

import numpy as np

from backend.demo_cache import DemoResultCache
from backend.models import Creator, CreatorMatch, PipelineResponse, Sentence, StyleReading, TranscriptResult
from backend.pipeline import MatchPipeline


def test_pipeline_runs_fixed_graph_and_keeps_only_grounded_evidence(monkeypatch) -> None:
    creators = [
        Creator("a", "Creator A", "analytical", "https://example.com/a", "Careful qualifiers; question-led framing", (1,)),
        Creator("b", "Creator B", "direct", "https://example.com/b", "Short declarative sentences; direct conclusions", (2,)),
        Creator("c", "Creator C", "reflective", "https://example.com/c", "Reflective asides; open questions", (3,)),
    ]
    monkeypatch.setattr("backend.pipeline.load_creators", lambda: creators)
    monkeypatch.setattr("backend.pipeline.load_vectors", lambda: (["a", "b", "c"], np.eye(3, dtype=np.float32), np.zeros(3, dtype=np.float32)))
    calls: list[str] = []
    text = " ".join(["I think we should look at this carefully before deciding."] * 30)

    def llm(system: str, user: str, _: int) -> str:
        calls.append(system.split()[0])
        if "Read only" in system:
            return json.dumps({"thinking_traits": [{"trait_id": "careful", "label": "Careful", "evidence_sentence_id": "s1", "confidence": .9}] * 3, "learning_traits": [], "learner_quotes": [{"sentence_id": "s1", "text": "I think we should look at this carefully before deciding."}], "style_summary": "Careful."})
        if "Fill the supplied response schema for every creator" in system:
            payload = json.loads(user)
            return json.dumps({"why_panels": [{"creator_id": m["creator_id"], "resemblance": "partial", "learner_trait_chips": ["Careful"], "evidence": [{"trait_id": "careful", "you_quote": {"sentence_id": "s1", "text": "I think we should look at this carefully before deciding."}, "creator_descriptor": m["descriptors"][0], "match_reason": "You both consider the evidence before reaching a conclusion."}, {"trait_id": "careful", "you_quote": {"sentence_id": "s1", "text": "I think we should look at this carefully before deciding."}, "creator_descriptor": m["descriptors"][0], "match_reason": "You both leave room to think before deciding."}]} for m in payload["matches"]]})
        payload = json.loads(user)
        return json.dumps({"verified_panels": [{"creator_id": panel["creator_id"], "resemblance": "clear", "evidence": [{"trait_id": item["trait_id"], "verdict": "kept", "verifiable": True, "grounded": True} for item in panel["evidence"]]} for panel in payload["why_panels"]], "overall_confidence": .8, "judge_skipped": False})

    pipeline = MatchPipeline(translate=lambda *_: text, llm=llm, embed=lambda _: np.array([1, 0, 0], dtype=np.float32))
    response = asyncio.run(pipeline.run_pipeline(b"private audio", "sample.m4a"))

    assert len(response.matches) == 3
    assert response.audio_deleted is True
    assert [item.step for item in response.step_trace if item.status == "started"] == ["transcript", "style_reader", "matcher", "memory", "evidence_writer", "confidence_judge"]
    assert len(calls) == 3
    assert response.matches[0].evidence
    assert response.analysis_complete is True
    assert response.degraded_reason is None
    assert response.tiebreak_skipped is True


def test_short_transcript_stops_before_gpt(monkeypatch) -> None:
    monkeypatch.setattr("backend.pipeline.load_creators", lambda: [])
    monkeypatch.setattr("backend.pipeline.load_vectors", lambda: ([], np.empty((0, 3)), np.zeros(3, dtype=np.float32)))
    pipeline = MatchPipeline(translate=lambda *_: "too short", llm=lambda *_: (_ for _ in ()).throw(AssertionError()), embed=lambda _: np.ones(3))
    response = asyncio.run(pipeline.run_pipeline(b"private audio", "sample.m4a"))
    assert response.matches == []
    assert response.message == "Please talk a little longer, about a minute or two."
    assert response.analysis_complete is False
    assert response.degraded_reason == "input"


def test_demo_cache_returns_only_an_allowlisted_audio_result() -> None:
    pipeline_response = {"matches": [], "step_trace": [], "audio_deleted": True}
    known = b"project-owned demo recording"
    cache = DemoResultCache({DemoResultCache.digest(known): PipelineResponse.model_validate(pipeline_response)})
    assert cache.get(known) is not None
    assert cache.get(b"a learner recording") is None


def test_generic_and_timeout_fallbacks_never_return_more_than_three_cards(monkeypatch) -> None:
    matches = [
        CreatorMatch(
            creator_id=str(index), creator_name=f"Creator {index}", role="role",
            channel_url=f"https://example.com/{index}", cosine_score=1 - index / 10,
            descriptors=["clear structure"], rank=index + 1,
        )
        for index in range(6)
    ]
    pipeline = object.__new__(MatchPipeline)
    generic = pipeline._generic_response(matches, [], False, degraded_reason="style")
    assert len(generic.matches) == 3
    assert generic.analysis_complete is False
    assert generic.degraded_reason == "style"

    async def times_out(*_args):
        raise asyncio.TimeoutError

    monkeypatch.setattr(pipeline, "_run", times_out)
    monkeypatch.setattr(pipeline, "_matcher", lambda _text: matches)
    response = asyncio.run(pipeline.run_pipeline(b"audio", "sample.m4a"))
    assert len(response.matches) == 3
    assert response.message == "We are showing the clearest overlap we found."
    assert response.analysis_complete is False
    assert response.degraded_reason == "timeout"


def test_embedding_model_is_loaded_once_and_reused(monkeypatch) -> None:
    monkeypatch.setattr("backend.pipeline.load_creators", lambda: [])
    monkeypatch.setattr("backend.pipeline.load_vectors", lambda: ([], np.empty((0, 3)), np.zeros(3, dtype=np.float32)))
    loads = []

    class FakeModel:
        def encode(self, texts, normalize_embeddings):
            assert normalize_embeddings is True
            return np.array([[1, 2]], dtype=np.float32)

    monkeypatch.setattr(MatchPipeline, "_load_embedding_model", staticmethod(lambda: loads.append(True) or FakeModel()))
    pipeline = MatchPipeline(translate=lambda *_: "", llm=lambda *_: "")
    assert len(loads) == 1
    np.testing.assert_array_equal(pipeline._embed("first"), np.array([1, 2], dtype=np.float32))
    np.testing.assert_array_equal(pipeline._embed("second"), np.array([1, 2], dtype=np.float32))
    assert len(loads) == 1


def test_tiebreaker_reorders_only_the_six_centered_candidates(monkeypatch) -> None:
    creators = [Creator(str(index), f"Creator {index}", "role", f"https://example.com/{index}", "note", (index,), f"Creator {index} uses a measured pace. They move from questions to a clear conclusion.") for index in range(6)]
    monkeypatch.setattr("backend.pipeline.load_creators", lambda: creators)
    monkeypatch.setattr("backend.pipeline.load_vectors", lambda: ([str(index) for index in range(6)], np.eye(6, dtype=np.float32), np.zeros(6, dtype=np.float32)))
    calls = []
    def tiebreak(system, user, max_tokens):
        calls.append((system, user, max_tokens))
        return json.dumps({"ranked_ids": ["2", "1", "0"], "reasons": ["one", "two", "three"]})
    pipeline = MatchPipeline(translate=lambda *_: "", llm=lambda *_: "", embed=lambda _: np.ones(6), tiebreak_llm=tiebreak)
    candidates = pipeline._matcher("sample")
    ranked = asyncio.run(pipeline._tiebreak(TranscriptResult(transcript_en="A learner sample with enough words.", sentences=[Sentence(id="s1", text="A learner sample.")], word_count=120), candidates))
    assert [match.creator_id for match in ranked] == ["2", "1", "0"]
    assert calls[0][2] == 800


def test_live_llm_path_uses_pydantic_structured_output(monkeypatch) -> None:
    monkeypatch.setattr("backend.pipeline.load_creators", lambda: [])
    monkeypatch.setattr("backend.pipeline.load_vectors", lambda: ([], np.empty((0, 3)), np.zeros(3, dtype=np.float32)))
    pipeline = MatchPipeline(translate=lambda *_: "", embed=lambda _: np.ones(3))
    expected = StyleReading.model_validate({
        "thinking_traits": [{"trait_id": "careful", "label": "Careful", "evidence_sentence_id": "s1", "confidence": 0.9}] * 3,
        "learning_traits": [],
        "learner_quotes": [{"sentence_id": "s1", "text": "I think carefully."}],
        "style_summary": "Careful and clear.",
    })
    calls = []

    def parsed(schema, system, user, max_tokens):
        calls.append((schema, system, user, max_tokens))
        return expected

    monkeypatch.setattr(pipeline, "_gpt56_parsed", parsed)
    result = asyncio.run(pipeline._ask(StyleReading, "system", "user", 2500, request_id="test-request", stage="style_reader"))
    assert result == expected
    assert calls == [(StyleReading, "system", "user", 2500)]
