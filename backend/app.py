"""Local synchronous HTTP API. It never writes user audio to disk."""

from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.pipeline import MatchPipeline


MAX_AUDIO_BYTES = 40 * 1024 * 1024
app = FastAPI(title="Your Ideal Role Model — local demo")
pipeline = MatchPipeline()


class CreatorResult(BaseModel):
    name: str
    role: str
    video_url: str
    similarity: float
    why: str


class MatchResponse(BaseModel):
    matches: list[CreatorResult]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/match", response_model=MatchResponse)
async def match(audio: UploadFile = File(...)) -> MatchResponse:
    raw_audio = await audio.read(MAX_AUDIO_BYTES + 1)
    try:
        if not raw_audio:
            raise HTTPException(status_code=400, detail="Upload a non-empty audio file.")
        if len(raw_audio) > MAX_AUDIO_BYTES:
            raise HTTPException(
                status_code=413, detail="Audio must be 40 MB or smaller for this demo."
            )
        found = pipeline.match(raw_audio, audio.filename or "recording", audio.content_type)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    finally:
        # The endpoint holds the upload in memory only and drops it immediately after ASR.
        del raw_audio
        await audio.close()
    return MatchResponse(
        matches=[
            CreatorResult(
                name=item.creator.name,
                role=item.creator.role,
                video_url=item.creator.video_url,
                similarity=item.similarity,
                why=item.why,
            )
            for item in found
        ]
    )
