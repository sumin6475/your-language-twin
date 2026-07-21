"""Request-scoped contracts used by the matching pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class Creator:
    id: str
    name: str
    role: str
    video_url: str
    source_note: str
    style_profile: tuple[int, ...] = ()
    style_descriptor_long: str = ""

    @property
    def descriptors(self) -> list[str]:
        """Human-authored facts only; creator transcripts never leave the seed file."""
        return [part.strip() for part in self.source_note.split(";") if part.strip()]


class Sentence(BaseModel):
    id: str
    text: str
    start_ms: int = 0
    end_ms: int = 0


class TranscriptResult(BaseModel):
    transcript_en: str
    sentences: list[Sentence]
    word_count: int
    duration_ms: int | None = None
    audio_deleted: bool = True


class Trait(BaseModel):
    trait_id: str
    label: str
    evidence_sentence_id: str
    confidence: float = Field(ge=0, le=1)


class LearnerQuote(BaseModel):
    sentence_id: str
    text: str


class StyleReading(BaseModel):
    thinking_traits: list[Trait]
    learning_traits: list[Trait] = []
    learner_quotes: list[LearnerQuote]
    style_summary: str


class CreatorMatch(BaseModel):
    creator_id: str
    creator_name: str
    role: str
    channel_url: str
    cosine_score: float
    descriptors: list[str]
    rank: int


class EvidenceItem(BaseModel):
    trait_id: str
    you_quote: LearnerQuote
    creator_descriptor: str
    match_reason: str


class WhyPanel(BaseModel):
    creator_id: str
    resemblance: Literal["strong", "clear", "partial"] = "partial"
    learner_trait_chips: list[str] = []
    evidence: list[EvidenceItem] = []


class EvidenceWriting(BaseModel):
    why_panels: list[WhyPanel]


class Verdict(BaseModel):
    trait_id: str
    verdict: Literal["kept", "dropped"]
    verifiable: bool
    grounded: bool
    note: str = ""


class VerifiedPanel(BaseModel):
    creator_id: str
    resemblance: Literal["strong", "clear", "partial"]
    evidence: list[Verdict]
    judge_summary: str = ""


class ConfidenceJudgment(BaseModel):
    verified_panels: list[VerifiedPanel]
    overall_confidence: float = Field(ge=0, le=1)
    judge_skipped: bool = False


class StepTrace(BaseModel):
    step: str
    status: Literal["started", "completed", "failed", "skipped"]
    elapsed_ms: int


class MatchCard(BaseModel):
    creator_id: str
    name: str
    role: str
    video_url: str
    similarity: float
    resemblance: Literal["strong", "clear", "partial"]
    trait_chips: list[str] = []
    evidence: list[EvidenceItem] = []
    why: str


class PipelineResponse(BaseModel):
    matches: list[MatchCard]
    step_trace: list[StepTrace]
    audio_deleted: bool
    judge_skipped: bool = False
    match_confidence_capped: bool = False
    memory_available: bool = True
    tiebreak_used: bool = False
    tiebreak_skipped: bool = False
    message: str | None = None
