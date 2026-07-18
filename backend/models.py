"""Small, framework-independent data shapes for the demo pipeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Creator:
    id: str
    name: str
    role: str
    video_url: str
    source_note: str


@dataclass(frozen=True)
class Match:
    creator: Creator
    similarity: float
    why: str

