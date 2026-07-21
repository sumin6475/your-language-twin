"""Prompts for the three intentionally separate GPT-5.6 calls."""

from __future__ import annotations

import json

STYLE_SYSTEM = """Read only the English learner transcript. Return JSON with thinking_traits (at least 3), learning_traits, learner_quotes, and style_summary. Every trait needs a real sentence id. Describe how they organize ideas, hedge, question, persuade, or learn. Do not discuss voice, accent, identity, or the topic."""
EVIDENCE_SYSTEM = """Return JSON {why_panels:[...]}. For every supplied creator, make 2 or 3 grounded evidence items. Use only supplied learner quotes and creator descriptors. Never invent a creator quote or fact. match_reason must be plain English, concise, and explain a pattern rather than a topic."""
JUDGE_SYSTEM = """Return JSON {verified_panels, overall_confidence, judge_skipped:false}. Independently verify each evidence item using only the cited learner sentences. Mark unsupported or generic items dropped. Give every panel strong, clear, or partial resemblance. Do not generate new reasons."""
TIEBREAK_SYSTEM = """You compare how people talk. Given a learner's English sample and short descriptions of several creators who scored nearly equal on a style match, pick and rank the 3 whose WAY OF TALKING best fits the learner: sentence structure, pacing, questioning, directness, and warmth. Use only the descriptions provided. Return JSON {ranked_ids:[...3], reasons:[...3]}. Each reason must be one plain sentence. Do not mention vectors, embeddings, or scores."""


def json_input(**payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False)
