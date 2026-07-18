"""Synchronous native-language-audio to English-creator matching pipeline."""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from typing import Any

import numpy as np

from backend.corpus import load_creators, load_vectors, top_k
from backend.models import Match
from backend.prompts import (
    FINGERPRINT_SYSTEM,
    TRANSLATION_SYSTEM,
    WHY_SYSTEM,
    fingerprint_input,
    translation_input,
    why_input,
)


def _json(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise RuntimeError("GPT-5.6 returned invalid JSON.") from error
    if not isinstance(value, dict):
        raise RuntimeError("GPT-5.6 returned an unexpected JSON shape.")
    return value


class MatchPipeline:
    def __init__(
        self,
        transcribe: Callable[[bytes, str, str | None], str] | None = None,
        llm: Callable[[str, str], str] | None = None,
        embed: Callable[[str], np.ndarray] | None = None,
    ) -> None:
        self.transcribe = transcribe or self._groq_transcribe
        self.llm = llm or self._gpt56
        self.embed = embed or self._embed

    def match(self, audio: bytes, filename: str, content_type: str | None = None) -> list[Match]:
        """Process raw bytes in memory only; the caller must never persist user audio."""
        try:
            native_text = self.transcribe(audio, filename, content_type)
        finally:
            # Raw user audio has no disk copy and is released even if ASR fails.
            del audio

        fingerprint = _json(self.llm(FINGERPRINT_SYSTEM, fingerprint_input(native_text)))
        translation = _json(
            self.llm(TRANSLATION_SYSTEM, translation_input(native_text, fingerprint))
        ).get("translation")
        if not isinstance(translation, str) or not translation.strip():
            raise RuntimeError("GPT-5.6 did not produce a usable English translation.")

        creators = load_creators()
        ids, vectors = load_vectors()
        candidates = top_k(self.embed(translation), creators, ids, vectors)
        matches = []
        for creator, similarity in candidates:
            why = self.llm(
                WHY_SYSTEM,
                why_input(
                    fingerprint,
                    {"name": creator.name, "role": creator.role, "source_note": creator.source_note},
                ),
            ).strip()
            matches.append(Match(creator=creator, similarity=similarity, why=why))
        return matches

    @staticmethod
    def _groq_transcribe(audio: bytes, filename: str, content_type: str | None) -> str:
        try:
            from groq import Groq
        except ImportError as error:
            raise RuntimeError("Install backend requirements before running the API.") from error
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            raise RuntimeError("GROQ_API_KEY is required to transcribe audio.")
        client = Groq(api_key=key)
        response = client.audio.transcriptions.create(
            file=(filename, audio, content_type or "application/octet-stream"),
            model="whisper-large-v3-turbo",
        )
        return (response.text or "").strip()

    @staticmethod
    def _gpt56(system: str, user: str) -> str:
        from openai import OpenAI

        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required for GPT-5.6.")
        response = OpenAI().responses.create(
            model="gpt-5.6",
            instructions=system,
            input=user,
        )
        return response.output_text

    @staticmethod
    def _embed(english_text: str) -> np.ndarray:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as error:
            raise RuntimeError("Install backend requirements before running the API.") from error
        model = SentenceTransformer("StyleDistance/styledistance")
        return np.asarray(model.encode([english_text], normalize_embeddings=True)[0])
