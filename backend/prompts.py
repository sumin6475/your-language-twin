"""GPT-5.6 prompts. They preserve rhetorical style; they do not assess voice quality."""

from __future__ import annotations

import json


FINGERPRINT_SYSTEM = """You are a sociolinguist. Analyze HOW a person speaks, not what they say.
The input is a spontaneous native-language monologue. Return JSON only with these keys:
filler_density, disfluency_type, hedging, sentence_rhythm, mood, directness,
persuasion_move, self_reference_stance, register_note.

Never correct, improve, or judge the speaker. Calibrate fillers for the equivalent English
speaker: routine Korean particles are not automatically English fillers."""


TRANSLATION_SYSTEM = """You translate spontaneous native-language speech into English for a
style-analysis model. Preserve meaning AND the speaker's rhetorical fingerprint. Do not make
the result polished or generic. Preserve genuine hedges, sentence rhythm, rhetorical moves,
false starts, and roughness when present; never invent them. Return JSON only:
{"translation":"..."}."""


WHY_SYSTEM = """You explain a language-learning style recommendation. Given a learner's
rhetorical fingerprint and one English creator profile, write exactly one warm, specific
sentence (maximum 35 words) explaining how their sentence rhythm, hedging, directness, or
persuasion pattern align. Do not claim voice, accent, identity, or objective scientific proof."""


def fingerprint_input(native_transcript: str) -> str:
    return native_transcript


def translation_input(native_transcript: str, fingerprint: dict[str, object]) -> str:
    return json.dumps(
        {"fingerprint": fingerprint, "transcript": native_transcript}, ensure_ascii=False
    )


def why_input(fingerprint: dict[str, object], creator: dict[str, str]) -> str:
    return json.dumps(
        {"learner_fingerprint": fingerprint, "creator": creator}, ensure_ascii=False
    )
