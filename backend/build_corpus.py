"""Precompute `styledistance` vectors for the local creator catalogue.

The source text is intentionally not served by the app. Before a public release it must be
replaced with licensed, creator-authored speech text; this small catalogue is demo-only.
"""

from __future__ import annotations

import json

import numpy as np

from backend.corpus import CREATORS_PATH, DATA_DIR, VECTORS_PATH


def main() -> None:
    from sentence_transformers import SentenceTransformer

    rows = json.loads(CREATORS_PATH.read_text(encoding="utf-8"))
    texts = [row["style_seed"] for row in rows]
    model = SentenceTransformer("StyleDistance/styledistance")
    vectors = model.encode(texts, normalize_embeddings=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        VECTORS_PATH,
        ids=np.asarray([row["id"] for row in rows]),
        vectors=np.asarray(vectors, dtype=np.float32),
    )
    print(f"Wrote {len(rows)} creator vectors to {VECTORS_PATH}")


if __name__ == "__main__":
    main()
