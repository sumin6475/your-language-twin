"""Create an allowlisted cached result from a project-owned demo recording.

Run only with a prepared demo recording and valid API keys:
    python -m backend.seed_demo_cache path/to/demo-recording.m4a
The command never copies the audio. It writes only its SHA-256 and the derived response.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from backend.demo_cache import DEMO_CACHE_PATH, DemoResultCache
from backend.pipeline import MatchPipeline


async def seed(audio_path: Path) -> None:
    audio = bytearray(audio_path.read_bytes())
    digest = DemoResultCache.digest(audio)
    try:
        response = await MatchPipeline().run_pipeline(audio, audio_path.name)
    finally:
        audio.clear()
    if not response.matches:
        raise RuntimeError(response.message or "Demo recording did not produce matches.")

    existing = json.loads(DEMO_CACHE_PATH.read_text(encoding="utf-8")) if DEMO_CACHE_PATH.exists() else {"entries": []}
    entry = {"audio_sha256": digest, "response": response.model_dump(mode="json")}
    entries = [item for item in existing.get("entries", []) if item.get("audio_sha256") != digest]
    entries.append(entry)
    DEMO_CACHE_PATH.write_text(json.dumps({"entries": entries}, indent=2) + "\n", encoding="utf-8")
    print(f"Seeded demo cache for {audio_path.name}: {digest}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    args = parser.parse_args()
    asyncio.run(seed(args.audio))


if __name__ == "__main__":
    main()
