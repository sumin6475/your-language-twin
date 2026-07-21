from __future__ import annotations

import json

import numpy as np

from backend.build_corpus import build, quality_report
from backend.corpus import EXPECTED_CREATOR_COUNT, centered_vectors, load_catalogue, load_vectors, make_style_probes, needs_tiebreak, top_k, validate_catalogue
from backend.models import Creator


class FakeEmbeddingModel:
    def encode(self, texts, normalize_embeddings):
        assert normalize_embeddings is True
        return np.asarray(
            [[len(text) % 7 + 1, index + 1, len(text.split())] for index, text in enumerate(texts)],
            dtype=np.float32,
        )


def test_candidate_catalogue_has_140_two_tier_creators_and_four_neutral_probes() -> None:
    catalogue = load_catalogue()
    assert len(catalogue["creators"]) == EXPECTED_CREATOR_COUNT
    assert validate_catalogue(catalogue) == []
    assert "politician" in catalogue["eligibility"]["excluded_target_types"]
    assert all(row["political_office_holder"] is False for row in catalogue["creators"])
    assert all(len(make_style_probes(row)) == 4 for row in catalogue["creators"])
    assert sum(row["verification"] == "candidate" for row in catalogue["creators"]) == 130
    assert sum(row["verification"] == "human_verified" for row in catalogue["creators"]) == 10
    assert all(
        row["review"]["author"] == "ai-draft" and row["review"]["reviewer"] == "builder-review"
        for row in catalogue["creators"] if row["verification"] == "candidate"
    )
    assert all(
        row["review"]["author"] == row["review"]["reviewer"] == "sumin"
        for row in catalogue["creators"] if row["verification"] == "human_verified"
    )


def test_build_mean_pools_probes_and_reports_distribution() -> None:
    catalogue = load_catalogue()
    ids, vectors, dispersions = build(FakeEmbeddingModel(), catalogue)
    assert len(ids) == EXPECTED_CREATOR_COUNT
    assert vectors.shape == (EXPECTED_CREATOR_COUNT, 3)
    assert dispersions.shape == (EXPECTED_CREATOR_COUNT,)
    report = quality_report(catalogue, ids, vectors, dispersions)
    assert report["creator_count"] == EXPECTED_CREATOR_COUNT
    assert report["verification_tiers"] == {"candidate": 130, "human_verified": 10}
    assert len(report["nearest_pairs"]) == 10
    assert report["exact_duplicate_vectors"] >= 0
    assert report["requires_blinded_human_evaluation"] is True
    assert "nearest_neighbor_median" in report["centered_cosine_distribution"]
    assert set(report["style_axis_distribution"]) == set(catalogue["creators"][0]["style_profile"])


def test_catalogue_rejects_invalid_review_tier_or_duplicate_rows() -> None:
    catalogue = load_catalogue()
    broken = json.loads(json.dumps(catalogue))
    broken["creators"][1]["id"] = broken["creators"][0]["id"]
    broken["creators"][0]["review"]["status"] = "pending"
    errors = validate_catalogue(broken)
    assert any("Duplicate creator ids" in error for error in errors)
    assert any("candidate or human-verified" in error for error in errors)


def test_top_k_returns_distinct_creators() -> None:
    creators = [
        Creator("a", "A", "role", "https://example.com/a", "Clear sequencing; evidence-aware context."),
        Creator("b", "B", "role", "https://example.com/b", "Practical next steps; direct encouragement."),
        Creator("c", "C", "role", "https://example.com/c", "Open questions; attentive follow-up."),
    ]
    rows = top_k(np.asarray([1, 0, 0], dtype=np.float32), creators, ["a", "b", "c"], np.eye(3, dtype=np.float32), np.zeros(3, dtype=np.float32))
    assert [creator.id for creator, _ in rows] == ["a", "b", "c"]


def test_centering_uses_the_same_fixed_centroid_for_query_and_corpus() -> None:
    vectors = np.asarray([[3, 1], [1, 3], [1, 1]], dtype=np.float32)
    centroid = vectors.mean(axis=0)
    transformed = centered_vectors(vectors, centroid)
    query = centered_vectors(np.asarray([[3, 1]], dtype=np.float32), centroid)[0]
    assert np.isclose(np.linalg.norm(query), 1)
    assert int(np.argmax(transformed @ query)) == 0


def test_tie_gate_catches_near_scores_and_identical_profiles() -> None:
    creators = [Creator(str(index), str(index), "role", "https://example.com", "note", (index,)) for index in range(3)]
    assert needs_tiebreak(list(zip(creators, [0.82, 0.81, 0.80])))
    distinct = [Creator(str(index), str(index), "role", "https://example.com", "note", (index,)) for index in range(3)]
    assert not needs_tiebreak(list(zip(distinct, [0.90, 0.82, 0.80])))
    twins = [Creator("a", "A", "role", "https://example.com", "note", (1,)), Creator("b", "B", "role", "https://example.com", "note", (1,)), Creator("c", "C", "role", "https://example.com", "note", (3,))]
    assert needs_tiebreak(list(zip(twins, [0.90, 0.84, 0.80])))


def test_built_artifact_matches_the_140_creator_catalogue() -> None:
    ids, vectors, centroid = load_vectors()
    assert len(ids) == EXPECTED_CREATOR_COUNT
    assert vectors.shape[0] == EXPECTED_CREATOR_COUNT
    assert len(set(ids)) == EXPECTED_CREATOR_COUNT
    assert centroid.shape == (vectors.shape[1],)
