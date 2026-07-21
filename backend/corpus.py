"""Curated creator corpus, validation, and in-memory cosine matching.

The catalogue deliberately stores human-authored descriptors and structured style
observations, never creator transcripts, captions, or downloaded media.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import numpy as np

from backend.models import Creator


DATA_DIR = Path(__file__).parent / "data"
CREATORS_PATH = DATA_DIR / "creators.seed.json"
VECTORS_PATH = DATA_DIR / "corpus.npz"
EXPECTED_CREATOR_COUNT = 140
TIE_EPS = 0.03
REQUIRED_STYLE_AXES = (
    "directness",
    "rhythm",
    "questions",
    "hedging",
    "structure",
    "storytelling",
    "warmth",
    "persuasion",
    "spontaneity",
)
FORBIDDEN_PROBE_MARKERS = ("transcript", "caption", "verbatim", "youtube.com/watch")


def load_catalogue(path: Path = CREATORS_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("creators"), list):
        raise ValueError("Creator catalogue must contain a creators list.")
    return payload


def validate_catalogue(catalogue: dict[str, Any], *, expected_count: int | None = EXPECTED_CREATOR_COUNT) -> list[str]:
    """Return actionable validation errors without retaining source media or quotes."""
    errors: list[str] = []
    creators = catalogue.get("creators", [])
    eligibility = catalogue.get("eligibility")
    if not isinstance(eligibility, dict) or "politician" not in eligibility.get("excluded_target_types", []):
        errors.append("Catalogue must explicitly exclude politicians and office holders.")
    if expected_count is not None and len(creators) != expected_count:
        errors.append(f"Expected {expected_count} creators, found {len(creators)}.")
    ids = [row.get("id") for row in creators if isinstance(row, dict)]
    duplicate_ids = [key for key, count in Counter(ids).items() if key and count > 1]
    if duplicate_ids:
        errors.append(f"Duplicate creator ids: {', '.join(sorted(duplicate_ids))}.")
    for position, row in enumerate(creators, start=1):
        prefix = f"Creator {position}"
        if not isinstance(row, dict):
            errors.append(f"{prefix} is not an object.")
            continue
        for field in ("id", "name", "role", "video_url", "source_note", "genre", "target_type"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{prefix} is missing {field}.")
        parsed = urlparse(str(row.get("video_url", "")))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{prefix} has an invalid canonical URL.")
        if row.get("target_type") not in {"youtube_creator", "creator_host", "celebrity_creator"} or row.get("political_office_holder") is not False:
            errors.append(f"{prefix} is not an eligible creator target.")
        profile = row.get("style_profile")
        if not isinstance(profile, dict) or set(profile) != set(REQUIRED_STYLE_AXES):
            errors.append(f"{prefix} must define all fixed style axes.")
        elif any(not isinstance(profile[axis], int) or not 1 <= profile[axis] <= 5 for axis in REQUIRED_STYLE_AXES):
            errors.append(f"{prefix} style axes must be integers from 1 to 5.")
        long_descriptor = row.get("style_descriptor_long")
        if not isinstance(long_descriptor, str) or len(long_descriptor.split()) < 20 or long_descriptor.count(".") < 2:
            errors.append(f"{prefix} needs a two-sentence long style descriptor.")
        review = row.get("review")
        verification = row.get("verification")
        candidate = (
            verification == "candidate"
            and isinstance(review, dict)
            and review.get("status") == "candidate"
            and review.get("author") == "ai-draft"
            and review.get("reviewer") == "builder-review"
        )
        human_verified = (
            verification == "human_verified"
            and isinstance(review, dict)
            and review.get("status") == "verified"
            and review.get("author") == review.get("reviewer")
            and bool(review.get("author"))
        )
        if not candidate and not human_verified:
            errors.append(f"{prefix} has invalid candidate or human-verified review metadata.")
        probes = make_style_probes(row) if isinstance(profile, dict) else []
        if len(probes) != 4 or any(len(probe.split()) < 20 for probe in probes):
            errors.append(f"{prefix} must yield four substantial neutral style probes.")
        if any(marker in " ".join(probes).lower() for marker in FORBIDDEN_PROBE_MARKERS):
            errors.append(f"{prefix} probe contains a prohibited source marker.")
    return errors


def make_style_probes(row: dict[str, Any]) -> list[str]:
    """Create four original, neutral probes from a reviewed style rubric.

    These are not creator words and intentionally avoid names, catchphrases, events,
    and source material. Multiple prompts reduce topic leakage in the mean vector.
    """
    p = row["style_profile"]
    directness = ("I am only sketching a possibility.", "One option is worth considering.", "Here is the practical issue.", "Start with this decision.", "Do this now, then check the result.")[p["directness"] - 1]
    rhythm = ("The thought unfolds in a long, connected sentence, with room for one idea to modify the next.", "There is time to pause between related ideas and notice their gradual shape.", "The pace is steady, with a clear point in each sentence.", "Short beats keep the explanation moving. Notice it. Try it. Review it.", "Quick turns create momentum. Look. Choose. Act. Learn.")[p["rhythm"] - 1]
    question = ("The answer can stand on its own.", "A small question may help later.", "What part of this matters most?", "Why does that detail change the choice? What have we missed?", "What if the obvious answer is wrong? Why wait? What happens next?")[p["questions"] - 1]
    hedge = ("This is the conclusion.", "The evidence points in one direction.", "In many cases, that is probably enough.", "It may depend on context, and there are reasonable exceptions.", "I could be mistaken, so hold the conclusion lightly while testing it.")[p["hedging"] - 1]
    structure = ("The pieces can remain loosely connected while the point develops.", "We can group the ideas once the pattern becomes visible.", "There is a beginning, a comparison, and a conclusion.", "First name the goal. Next compare the options. Finally choose one action.", "Step one sets the frame. Step two tests it. Step three gives a repeatable rule.")[p["structure"] - 1]
    story = ("The pattern matters more than any single example.", "A small scene can make the point concrete.", "Imagine an ordinary moment when the plan changes.", "I remember a modest moment when one observation changed the whole plan.", "Here is what happened, what surprised me, and why that moment changed the next decision.")[p["storytelling"] - 1]
    warmth = ("The result follows from conditions we can inspect.", "It is fine to keep the standard practical.", "You can make progress without getting every part right.", "You are allowed to begin with the smallest workable version.", "Take a breath. You are not behind. Start where you are and keep going.")[p["warmth"] - 1]
    persuade = ("Consider the trade-offs before drawing a conclusion.", "The comparison is useful even without a final recommendation.", "The next action becomes clearer after a short test.", "Try it in ordinary life and keep the part that proves useful.", "Commit to a small experiment today, measure it honestly, and repeat what works.")[p["persuasion"] - 1]
    spontaneous = ("The reasoning is deliberate and prepared.", "The point is composed but conversational.", "There is room for an aside when it helps.", "Maybe that sounds strange at first, but stay with it for a second.", "Wait, there is another angle here, and it changes the whole picture.")[p["spontaneity"] - 1]
    return [
        f"{directness} {rhythm} {question} {hedge}",
        f"When learning a new skill, {structure} {warmth} {persuade}",
        f"{story} {spontaneous} {rhythm} {question}",
        f"A decision becomes easier when we describe what is happening without drama. {structure} {hedge} {warmth}",
    ]


def profile_descriptors(row: dict[str, Any]) -> str:
    """Turn reviewed rubric values into the only creator facts exposed to the LLM."""
    p = row["style_profile"]
    descriptors = [
        "direct conclusions" if p["directness"] >= 4 else "careful, qualified framing",
        "short energetic beats" if p["rhythm"] >= 4 else "measured sentence flow",
        "question-led exploration" if p["questions"] >= 4 else "statement-led explanation",
        "clear step-by-step structure" if p["structure"] >= 4 else "a looser reflective build",
        "story-to-insight transitions" if p["storytelling"] >= 4 else "pattern-first explanation",
        "warm reassurance" if p["warmth"] >= 4 else "calm analytical distance",
    ]
    return "; ".join(descriptors) + "."


def centered_vectors(vectors: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    """Apply the fixed corpus centering transform used by every matcher query."""
    centered = np.asarray(vectors, dtype=np.float32) - np.asarray(centroid, dtype=np.float32)
    norms = np.linalg.norm(centered, axis=-1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Centering produced an empty vector.")
    return centered / norms


def load_creators(path: Path = CREATORS_PATH) -> list[Creator]:
    catalogue = load_catalogue(path)
    errors = validate_catalogue(catalogue)
    if errors:
        raise ValueError("Invalid creator catalogue: " + " ".join(errors))
    return [
        Creator(
            id=row["id"], name=row["name"], role=row["role"], video_url=row["video_url"],
            source_note=profile_descriptors(row),
            style_profile=tuple(row["style_profile"][axis] for axis in REQUIRED_STYLE_AXES),
            style_descriptor_long=row["style_descriptor_long"],
        )
        for row in catalogue["creators"]
    ]


def load_vectors(path: Path = VECTORS_PATH) -> tuple[list[str], np.ndarray, np.ndarray]:
    if not path.exists():
        raise RuntimeError("Corpus vectors are missing. Run `python -m backend.build_corpus` once.")
    data = np.load(path, allow_pickle=False)
    if "centroid" not in data:
        raise RuntimeError("Corpus centroid is missing. Run `python -m backend.build_corpus` once.")
    return data["ids"].astype(str).tolist(), data["vectors"].astype(np.float32), data["centroid"].astype(np.float32)


def top_k(query: np.ndarray, creators: list[Creator], ids: list[str], vectors: np.ndarray, centroid: np.ndarray, k: int = 3) -> list[tuple[Creator, float]]:
    if vectors.ndim != 2 or len(ids) != len(creators) or len(set(ids)) != len(ids):
        raise ValueError("Corpus vectors and creators are inconsistent.")
    index = {creator.id: creator for creator in creators}
    corpus_vectors = centered_vectors(vectors, centroid)
    query_vector = centered_vectors(np.asarray(query, dtype=np.float32)[None, :], centroid)[0]
    scores = corpus_vectors @ query_vector
    order = np.argsort(-scores)[: min(k, len(scores))]
    return [(index[ids[i]], float(scores[i])) for i in order]


def needs_tiebreak(rows: list[tuple[Creator, float]], tie_eps: float = TIE_EPS) -> bool:
    """Use an LLM only when the centered score or rubric profile leaves a real tie."""
    if len(rows) < 3:
        return False
    score_tie = rows[0][1] - rows[2][1] < tie_eps
    profiles = [creator.style_profile for creator, _ in rows[:3]]
    profile_tie = len(profiles) != len(set(profiles))
    return score_tie or profile_tie
