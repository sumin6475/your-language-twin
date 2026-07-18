"""
Phase 0 spike — build + embed a small English-creator corpus.

Produces data/corpus.npz containing, for each creator:
  - name
  - a style embedding from mstyledistance   (multilingual  -> used by Path A)
  - a style embedding from styledistance     (English-only  -> used by Path B)

We embed each creator once (mean-pooled over several of their transcript chunks).
At this scale, brute-force cosine k-NN in match.py is instant — no vector DB needed.

This is throwaway spike code. Not the product.
"""
from __future__ import annotations

import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUT = os.path.join(DATA_DIR, "corpus.npz")

MSTYLE_MODEL = "StyleDistance/mstyledistance"   # multilingual, content-independent
ENSTYLE_MODEL = "StyleDistance/styledistance"   # English style (for translate-then-match)

# Candidate ready-made, named-speaker transcript datasets on HF (licensed).
# We try these first; if unavailable/gated/moved we fall back to the bundled seed below.
CANDIDATE_DATASETS = [
    # (hf_id, split, text_column, speaker_column_or_None, fixed_name_if_single_speaker)
    # Verified accessible + speaker-separable on 2026-07-18. Gives ~43 real speakers, but
    # ALL formal (speeches) — so we always merge CONVERSATIONAL_CREATORS below for genre
    # diversity. (ryang2/youtube-podcast-transcripts dropped: it's a single channel.)
    ("chrissoria/presidential-speeches", "train", "text", "speaker", None),
]

MAX_ROWS_PER_DATASET = 1200   # scan enough rows to reach ~40 speakers
MAX_CHUNKS_PER_SPEAKER = 6    # cap so no one speaker dominates the corpus
MIN_CHUNK_CHARS = 400         # need enough text for a stable style signal

# Conversational-creator corpus, ALWAYS added alongside the dataset speakers.
# The HF datasets we can reach are formal (presidential speeches), so on their own the
# corpus is genre-skewed and can't match an everyday spoken sample. These entries add
# spoken/casual style diversity across the axes that matter (casual vs formal, energy,
# sentence length, rhetorical habits).
#
# HONEST CAVEAT: these are STYLE-REPRESENTATIVE excerpts written to capture each creator's
# well-known verbal habits — they are NOT verbatim transcripts (using verbatim video
# transcripts raises copyright/accuracy issues and we don't have them here). This is fine
# for a spike whose only job is "does style matching discriminate?" Before trusting any
# PASS/FAIL for the product, replace these with real self-transcribed excerpts (Whisper on
# licensed/public content), per spike/README.md.
CONVERSATIONAL_CREATORS: dict[str, list[str]] = {
    "Casual explainer YouTuber (hedged, 'basically', numbered)": [
        "Okay so basically what's happening here is, there's like three things going on, and I think it's worth just slowing down and taking them one at a time, right?",
        "And the thing is — and this is the part people kind of miss — it's not actually that complicated once you see it. It just looks scary from the outside.",
        "So yeah, if you take one thing away from this video, it's basically that. That's the whole idea, honestly.",
    ],
    "High-energy hype creator (short, imperative, repetitive)": [
        "Let's go. Right now. Today. Not tomorrow, today. You've got this. I need you to believe that.",
        "This is huge. This is massive. You are gonna look back on this moment and you're gonna be so glad you started.",
        "Stop overthinking it. Just start. Just do it. Momentum is everything. Go, go, go.",
    ],
    "Reflective storyteller vlogger (tangential, 'you know')": [
        "So, funny story, I was literally about to head home, you know, and then this whole unexpected thing just... happened, and I couldn't not film it.",
        "And I don't know, maybe it's just me, but there's something kind of beautiful about how the day completely fell apart, honestly.",
        "Anyway — long story short — I ended up staying way longer than I planned, and yeah, no regrets. None at all.",
    ],
    "Analytical podcaster (long sentences, qualified, 'sort of')": [
        "I think the interesting thing, and this is sort of an under-appreciated point, is that the incentives here are much more subtle than the headline suggests.",
        "If you actually look at the data, and you control for the obvious confounders, what you tend to find is a fairly modest but real effect.",
        "So I'd be careful about drawing a strong conclusion from that, because the sample is small and the mechanism isn't fully understood yet.",
    ],
    "Warm interviewer (open questions, reflective, affirming)": [
        "That's fascinating. I want to sit with that for a second, because I think there's something really important underneath what you just said.",
        "What was going through your mind in that exact moment? Like, when everything shifted — what did that actually feel like for you?",
        "It sounds like there's a real tension there, and I'd love for you to say more about how you hold both of those at once.",
    ],
    "Blunt persuader (rhetorical questions, contrast, 'here's the truth')": [
        "But is that really the argument? Because if it is, it falls apart the second you look at it honestly.",
        "Here's the truth nobody wants to say out loud: it was never about fairness. It was about incentives. It always has been.",
        "Ask yourself one question. Who actually benefits from this? Follow that answer, and everything else makes sense.",
    ],
    "Deadpan comedic commentator (dry, understated, aside-heavy)": [
        "So this happened. Which is fine. Everything's fine. This is exactly how I pictured my week going, obviously.",
        "And look, I'm not saying it's the worst idea anyone's ever had. I'm just saying I've seen better ideas written on the back of a napkin.",
        "Anyway, moving on, because dwelling on it would require feelings, and we don't do those here.",
    ],
    "Enthusiastic teacher (clear, encouraging, 'let's', step-by-step')": [
        "Alright, let's break this down together, step by step, and I promise by the end it's going to make complete sense.",
        "Great question — and honestly, this is exactly the kind of thing that trips a lot of people up, so let's take it slow.",
        "See? You already knew more than you thought. Now let's build on that and take it just one step further.",
    ],
}


def _load_model(name: str):
    from sentence_transformers import SentenceTransformer
    print(f"  loading {name} (first run downloads + caches) ...")
    return SentenceTransformer(name, cache_folder=os.path.join(DATA_DIR, "cache"))


def _gather_from_datasets() -> dict[str, list[str]]:
    """Best-effort: pull a few chunks per named speaker from the candidate datasets."""
    corpus: dict[str, list[str]] = {}
    try:
        from datasets import load_dataset
    except Exception as e:  # pragma: no cover
        print(f"  (datasets lib unavailable: {e})")
        return corpus

    for hf_id, split, text_col, spk_col, fixed_name in CANDIDATE_DATASETS:
        try:
            print(f"  trying dataset {hf_id} ...")
            ds = load_dataset(hf_id, split=split, streaming=True)
            scanned = 0
            for row in ds:
                text = (row.get(text_col) or "").strip()
                if len(text) < MIN_CHUNK_CHARS:      # need enough text for a style signal
                    continue
                name = fixed_name or (row.get(spk_col) or "unknown").strip()
                if not name or name.lower() == "unknown":
                    continue
                corpus.setdefault(name, [])
                if len(corpus[name]) < MAX_CHUNKS_PER_SPEAKER:
                    corpus[name].append(text[:2000])
                scanned += 1
                if scanned >= MAX_ROWS_PER_DATASET:
                    break
            got = sum(len(v) for v in corpus.values())
            print(f"    scanned {scanned} rows -> {len(corpus)} speakers, {got} chunks total")
        except Exception as e:
            print(f"    skipped {hf_id}: {e}")
    # keep only speakers with at least 2 chunks (a single chunk is a weak style signal)
    return {k: v for k, v in corpus.items() if len(v) >= 2}


def build() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    print("Gathering transcripts ...")
    corpus = _gather_from_datasets()
    dataset_n = len(corpus)

    # ALWAYS merge the conversational creators — the dataset speakers are all formal, so
    # this is what gives the corpus genre diversity (casual/spoken vs formal/speech).
    for k, v in CONVERSATIONAL_CREATORS.items():
        corpus.setdefault(k, v)

    names = sorted(corpus.keys())
    print(f"Corpus: {len(names)} speakers "
          f"({dataset_n} from datasets [formal] + "
          f"{len(names) - dataset_n} conversational creators [spoken]).")

    print("Embedding with style models ...")
    mstyle = _load_model(MSTYLE_MODEL)
    enstyle = _load_model(ENSTYLE_MODEL)

    m_vecs, e_vecs = [], []
    for name in names:
        chunks = corpus[name]
        # one vector per creator = mean of their chunk embeddings (normalized)
        m = mstyle.encode(chunks, normalize_embeddings=True)
        e = enstyle.encode(chunks, normalize_embeddings=True)
        m_vecs.append(_unit(np.mean(m, axis=0)))
        e_vecs.append(_unit(np.mean(e, axis=0)))
        print(f"  ✓ {name}  ({len(chunks)} chunks)")

    np.savez(
        OUT,
        names=np.array(names, dtype=object),
        mstyle=np.vstack(m_vecs).astype(np.float32),
        enstyle=np.vstack(e_vecs).astype(np.float32),
    )
    print(f"\nSaved {len(names)} creators -> {OUT}")
    print("Next: python match.py samples/<your-native-language-audio>")


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n else v


if __name__ == "__main__":
    build()
