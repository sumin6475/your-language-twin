"""Local HTTP API. Audio is held only in request memory and dropped after ASR."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.demo_cache import DemoResultCache
from backend.models import PipelineResponse
from backend.pipeline import MatchPipeline


# Local convenience only. Deployment-provided variables (including Vercel's) win.
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)

MAX_AUDIO_BYTES = 40 * 1024 * 1024
app = FastAPI(title="Your Ideal Role Model - local demo")
app.add_middleware(CORSMiddleware, allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+", allow_methods=["*"], allow_headers=["*"])
pipeline = MatchPipeline()
demo_cache = DemoResultCache.from_file()

@app.get("/health")
def health() -> dict[str, str]: return {"status": "ok"}

@app.post("/match", response_model=PipelineResponse)
async def match(audio: UploadFile = File(...), opt_in: bool = False, memory_token: str | None = None) -> PipelineResponse:
    raw_audio = bytearray(await audio.read(MAX_AUDIO_BYTES + 1))
    try:
        if not raw_audio: raise HTTPException(400, "Upload a non-empty audio file.")
        if len(raw_audio) > MAX_AUDIO_BYTES: raise HTTPException(413, "Audio must be 40 MB or smaller for this demo.")
        cached = demo_cache.get(raw_audio)
        if cached:
            return cached
        return await pipeline.run_pipeline(raw_audio, audio.filename or "recording", audio.content_type, opt_in=opt_in, memory_token=memory_token)
    finally:
        raw_audio.clear()
        del raw_audio
        await audio.close()
