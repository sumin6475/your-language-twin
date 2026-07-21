"""Prompts for the three intentionally separate GPT-5.6 calls."""

from __future__ import annotations

import json

STYLE_SYSTEM = """Read only the English learner transcript and fill the supplied response schema. Describe how the learner organizes ideas, hedges, questions, persuades, or learns; do not discuss voice, accent, identity, or topic. Cite only supplied sentence IDs, include at least three thinking traits, and quote only actual learner sentences."""
EVIDENCE_SYSTEM = """Fill the supplied response schema for every creator. Make two or three grounded evidence items per creator. Use only supplied learner quotes and creator descriptors. Never invent a creator quote or fact. Each match_reason must be concise, plain English, and explain a communication pattern rather than a topic."""
JUDGE_SYSTEM = """Fill the supplied response schema. Independently verify each evidence item using only the cited learner sentences. Mark unsupported or generic items dropped, give every panel strong, clear, or partial resemblance, and do not generate new reasons."""
TIEBREAK_SYSTEM = """You compare how people talk. Given a learner's English sample and short descriptions of several creators who scored nearly equal on a style match, pick and rank the 3 whose WAY OF TALKING best fits the learner: sentence structure, pacing, questioning, directness, and warmth. Use only the descriptions provided. Return JSON {ranked_ids:[...3], reasons:[...3]}. Each reason must be one plain sentence. Do not mention vectors, embeddings, or scores."""


def json_input(**payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False)
