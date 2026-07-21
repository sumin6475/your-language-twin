"""Build a validated, versioned creator style corpus and quality report."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np

from backend.corpus import CREATORS_PATH, DATA_DIR, VECTORS_PATH, centered_vectors, load_catalogue, make_style_probes, validate_catalogue

REPORT_PATH = DATA_DIR / "corpus.quality.json"


def quality_report(catalogue: dict, ids: list[str], vectors: np.ndarray, dispersions: np.ndarray) -> dict:
    creators = catalogue["creators"]
    centered = centered_vectors(vectors, vectors.mean(axis=0))
    similarities = centered @ centered.T
    np.fill_diagonal(similarities, -1)
    pairs = []
    for flat_index in np.argsort(similarities.ravel())[::-1]:
        left, right = np.unravel_index(flat_index, similarities.shape)
        if left >= right:
            continue
        pairs.append({"left_id": ids[left], "right_id": ids[right], "cosine_similarity": round(float(similarities[left, right]), 6)})
        if len(pairs) == 10:
            break
    axes = {axis: Counter(row["style_profile"][axis] for row in creators) for axis in creators[0]["style_profile"]}
    exact_duplicates = len(ids) - len(np.unique(vectors, axis=0))
    tier_counts = Counter(row["verification"] for row in creators)
    nearest = similarities.max(axis=1)
    pair_scores = similarities[np.triu_indices_from(similarities, k=1)]
    return {
        "dataset_version": catalogue["dataset_version"],
        "creator_count": len(creators),
        "verification_tiers": dict(sorted(tier_counts.items())),
        "known_limitations": catalogue.get("known_limitations", []),
        "genre_distribution": dict(sorted(Counter(row["genre"] for row in creators).items())),
        "style_axis_distribution": {axis: {str(value): count for value, count in sorted(counts.items())} for axis, counts in axes.items()},
        "probe_dispersion": {"mean": round(float(dispersions.mean()), 6), "max": round(float(dispersions.max()), 6)},
        "nearest_pairs": pairs,
        "matching_space": "corpus-centroid-centered cosine",
        "centered_cosine_distribution": {
            "nearest_neighbor_median": round(float(np.median(nearest)), 6),
            "nearest_neighbor_p90": round(float(np.quantile(nearest, 0.9)), 6),
            "all_pairs_median": round(float(np.median(pair_scores)), 6),
            "pairs_above_0_999": int(np.sum(pair_scores > 0.999)),
        },
        "exact_duplicate_vectors": exact_duplicates,
        "requires_blinded_human_evaluation": True,
        "review_gate": "candidate rows are AI-drafted and builder-reviewed; verified rows are directly observed by the builder",
    }


def build(model: object, catalogue: dict) -> tuple[list[str], np.ndarray, np.ndarray]:
    errors = validate_catalogue(catalogue)
    if errors:
        raise ValueError("\n".join(errors))
    ids: list[str] = []
    vectors: list[np.ndarray] = []
    dispersions: list[float] = []
    for row in catalogue["creators"]:
        probe_vectors = np.asarray(model.encode(make_style_probes(row), normalize_embeddings=True), dtype=np.float32)
        vector = probe_vectors.mean(axis=0)
        vector /= np.linalg.norm(vector)
        ids.append(row["id"])
        vectors.append(vector)
        dispersions.append(float(np.mean(1 - (probe_vectors @ vector))))
    return ids, np.asarray(vectors, dtype=np.float32), np.asarray(dispersions, dtype=np.float32)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()
    from sentence_transformers import SentenceTransformer

    catalogue = load_catalogue(CREATORS_PATH)
    ids, vectors, dispersions = build(SentenceTransformer("StyleDistance/styledistance"), catalogue)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    centroid = vectors.mean(axis=0).astype(np.float32)
    np.savez_compressed(VECTORS_PATH, ids=np.asarray(ids), vectors=vectors, centroid=centroid, probe_dispersion=dispersions, dataset_version=np.asarray(catalogue["dataset_version"]))
    args.report.write_text(json.dumps(quality_report(catalogue, ids, vectors, dispersions), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(ids)} creator vectors to {VECTORS_PATH} and quality report to {args.report}")


if __name__ == "__main__":
    main()
