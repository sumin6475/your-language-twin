"""Allowlisted, read-only cached responses for known demo recordings only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from backend.models import PipelineResponse


DEMO_CACHE_PATH = Path(__file__).parent / "data" / "demo_results.json"


class DemoResultCache:
    """Matches complete audio bytes against a fixed SHA-256 allowlist.

    This is deliberately not a general result cache: unknown recordings return ``None`` and
    are processed normally. The stored payloads are only for project-owned demo recordings.
    """

    def __init__(self, entries: dict[str, PipelineResponse] | None = None) -> None:
        self._entries = entries or {}

    @classmethod
    def from_file(cls, path: Path = DEMO_CACHE_PATH) -> "DemoResultCache":
        if not path.exists():
            return cls()
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            {
                item["audio_sha256"]: PipelineResponse.model_validate(item["response"])
                for item in payload.get("entries", [])
            }
        )

    @staticmethod
    def digest(audio: bytes | bytearray) -> str:
        return hashlib.sha256(audio).hexdigest()

    def get(self, audio: bytes | bytearray) -> PipelineResponse | None:
        response = self._entries.get(self.digest(audio))
        return response.model_copy(deep=True) if response else None
