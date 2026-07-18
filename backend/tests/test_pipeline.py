from __future__ import annotations

import json
import importlib
from pathlib import Path

import numpy as np
from fastapi.testclient import TestClient

from backend.models import Creator
from backend.pipeline import MatchPipeline


def test_pipeline_returns_three_matches_without_persisting_audio(monkeypatch, tmp_path: Path) -> None:
    creators = [
        Creator("a", "A", "analytical", "https://example.com/a", "qualified"),
        Creator("b", "B", "direct", "https://example.com/b", "imperative"),
        Creator("c", "C", "reflective", "https://example.com/c", "questions"),
    ]
    corpus_file = tmp_path / "corpus.npz"
    np.savez(corpus_file, ids=np.array(["a", "b", "c"]), vectors=np.eye(3, dtype=np.float32))
    creators_file = tmp_path / "creators.json"
    creators_file.write_text("[]", encoding="utf-8")

    monkeypatch.setattr("backend.pipeline.load_creators", lambda: creators)
    monkeypatch.setattr(
        "backend.pipeline.load_vectors", lambda: (["a", "b", "c"], np.eye(3, dtype=np.float32))
    )
    calls = []

    def fake_transcribe(audio: bytes, filename: str, content_type: str | None) -> str:
        calls.append((audio, filename, content_type))
        return "한국어 원문"

    def fake_llm(system: str, user: str) -> str:
        if "sociolinguist" in system:
            return json.dumps({"mood": "analytical", "hedging": "moderate"})
        if "translate" in system:
            return json.dumps({"translation": "I think we should look at the evidence carefully."})
        return "You both use careful, qualified reasoning before reaching a conclusion."

    pipeline = MatchPipeline(
        transcribe=fake_transcribe,
        llm=fake_llm,
        embed=lambda _: np.array([1, 0, 0], dtype=np.float32),
    )

    matches = pipeline.match(b"private audio", "sample.m4a", "audio/mp4")

    assert calls == [(b"private audio", "sample.m4a", "audio/mp4")]
    assert [match.creator.name for match in matches] == ["A", "B", "C"]
    assert all(match.why for match in matches)


def test_match_endpoint_returns_creator_cards(monkeypatch) -> None:
    app_module = importlib.import_module("backend.app")

    class FakePipeline:
        def match(self, audio: bytes, filename: str, content_type: str | None):
            assert audio == b"native audio"
            assert filename == "sample.m4a"
            assert content_type == "audio/mp4"
            return [
                type(
                    "Result",
                    (),
                    {
                        "creator": Creator("a", "Creator A", "explainer", "https://example.com", "clear"),
                        "similarity": 0.91,
                        "why": "You both explain ideas in careful steps.",
                    },
                )()
            ]

    monkeypatch.setattr(app_module, "pipeline", FakePipeline())
    response = TestClient(app_module.app).post(
        "/match", files={"audio": ("sample.m4a", b"native audio", "audio/mp4")}
    )

    assert response.status_code == 200
    assert response.json()["matches"][0]["name"] == "Creator A"
