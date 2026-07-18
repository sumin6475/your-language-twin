"""File-backed creator corpus and in-memory cosine matching for the local demo."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from backend.models import Creator


DATA_DIR = Path(__file__).parent / "data"
CREATORS_PATH = DATA_DIR / "creators.json"
VECTORS_PATH = DATA_DIR / "corpus.npz"


def load_creators(path: Path = CREATORS_PATH) -> list[Creator]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [
        Creator(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            video_url=row["video_url"],
            source_note=row["source_note"],
        )
        for row in rows
    ]


def load_vectors(path: Path = VECTORS_PATH) -> tuple[list[str], np.ndarray]:
    if not path.exists():
        raise RuntimeError(
            "Corpus vectors are missing. Run `python -m backend.build_corpus` once."
        )
    data = np.load(path, allow_pickle=False)
    return data["ids"].astype(str).tolist(), data["vectors"].astype(np.float32)


def top_k(
    query: np.ndarray, creators: list[Creator], ids: list[str], vectors: np.ndarray, k: int = 3
) -> list[tuple[Creator, float]]:
    if vectors.ndim != 2 or len(ids) != len(creators):
        raise ValueError("Corpus vectors and creators are inconsistent.")
    index = {creator.id: creator for creator in creators}
    norm = np.linalg.norm(query)
    if not norm:
        raise ValueError("Query embedding is empty.")
    scores = vectors @ (query / norm)
    order = np.argsort(-scores)[: min(k, len(scores))]
    return [(index[ids[i]], float(scores[i])) for i in order]
