"""
Phase 0 spike — match one native-language audio sample against the creator corpus.

Runs THREE candidate pipelines side by side so you can judge which to build on:

  Path A  (direct):        audio --Whisper(Korean)--> KO text
                           --mstyledistance--> vec --kNN--> corpus.mstyle
                           (spike finding: WEAK — mstyledistance can't discriminate
                            style within Korean; kept here only for the record.)

  Path B1 (plain xlate):   audio --Whisper(translate=EN)--> flat EN
                           --styledistance--> vec --kNN--> corpus.enstyle
                           (works, but Whisper flattens idiolect.)

  Path B2 (styled xlate):  audio --Whisper(Korean)--> KO text
                           --LLM style-preserving KO→EN (translate.py)--> EN
                           --styledistance--> vec --kNN--> corpus.enstyle
                           (the improvement: preserves hedges/rhythm/fillers the
                            style model matches on. See translate.py + the reference doc.)

Prints top-5 for each, side by side. YOU judge which matches feel right.

Requires: GROQ_API_KEY (ASR) and, for Path B2, OPENAI_API_KEY (translation).
Path B2 is skipped gracefully if OPENAI_API_KEY is absent. Throwaway spike code.
"""

from __future__ import annotations

import os
import sys

import numpy as np

import _env  # noqa: F401  — loads spike/.env into os.environ on import

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CORPUS = os.path.join(DATA_DIR, "corpus.npz")

MSTYLE_MODEL = "StyleDistance/mstyledistance"
ENSTYLE_MODEL = "StyleDistance/styledistance"
# Groq Whisper models: turbo is transcription-only (cheaper/faster); the audio→English
# `translate` endpoint is supported ONLY by the non-turbo large-v3. So we pick per call.
WHISPER_TRANSCRIBE_MODEL = "whisper-large-v3-turbo"  # transcribe (original language)
WHISPER_TRANSLATE_MODEL = "whisper-large-v3"  # translate to English (turbo can't)
TOP_K = 5


def _die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def transcribe(path: str, translate: bool) -> str:
    """Groq Whisper. translate=False -> original language; translate=True -> English."""
    try:
        from groq import Groq
    except Exception as e:
        _die(f"groq lib not installed ({e}). pip install -r requirements.txt")
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        _die("GROQ_API_KEY not set. Get a free key at https://console.groq.com/keys")
    client = Groq(api_key=key)
    with open(path, "rb") as f:
        if translate:
            resp = client.audio.translations.create(
                file=(os.path.basename(path), f.read()),
                model=WHISPER_TRANSLATE_MODEL,
            )
        else:
            resp = client.audio.transcriptions.create(
                file=(os.path.basename(path), f.read()),
                model=WHISPER_TRANSCRIBE_MODEL,
            )
    return (resp.text or "").strip()


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n else v


def knn(query_vec: np.ndarray, corpus_mat: np.ndarray, names, k: int):
    sims = corpus_mat @ _unit(query_vec)  # cosine (corpus rows are unit vectors)
    order = np.argsort(-sims)[:k]
    return [(names[i], float(sims[i])) for i in order]


def _fmt_col(results, width: int = 36) -> list[str]:
    return [f"{sc:5.3f} {nm[: width - 7]:<{width - 6}}" for nm, sc in results]


def main(audio_path: str) -> None:
    if not os.path.exists(CORPUS):
        _die("data/corpus.npz missing. Run: python build_corpus.py")
    if not os.path.exists(audio_path):
        _die(f"audio not found: {audio_path}")

    data = np.load(CORPUS, allow_pickle=True)
    names = list(data["names"])
    mstyle_mat = data["mstyle"]
    enstyle_mat = data["enstyle"]

    from sentence_transformers import SentenceTransformer

    cache = os.path.join(DATA_DIR, "cache")

    print(f"\n=== Sample: {os.path.basename(audio_path)} ===\n")

    # ---- Path A: direct (native language -> multilingual style space) ----
    print("Path A (direct): transcribing in Korean ...")
    korean_text = transcribe(audio_path, translate=False)
    print(f"  KO transcript ({len(korean_text)} chars): {korean_text[:160]}...\n")
    mstyle = SentenceTransformer(MSTYLE_MODEL, cache_folder=cache)
    qa = mstyle.encode([korean_text], normalize_embeddings=True)[0]
    a_results = knn(qa, mstyle_mat, names, TOP_K)

    enstyle = SentenceTransformer(ENSTYLE_MODEL, cache_folder=cache)

    # ---- Path B1: plain Whisper translation ----
    print("Path B1 (plain xlate): Whisper translate -> English ...")
    plain_en = transcribe(audio_path, translate=True)
    print(f"  EN ({len(plain_en)} chars): {plain_en[:160]}...\n")
    qb1 = enstyle.encode([plain_en], normalize_embeddings=True)[0]
    b1_results = knn(qb1, enstyle_mat, names, TOP_K)

    # ---- Path B2: style-preserving LLM translation (skipped if no OPENAI_API_KEY) ----
    b2_results = None
    if os.environ.get("OPENAI_API_KEY"):
        print("Path B2 (styled xlate): LLM style-preserving KO->EN ...")
        from translate import fingerprint, translate_styled

        fp = fingerprint(korean_text)
        print(f"  fingerprint: {fp}")
        styled_en = translate_styled(korean_text, fp=fp)
        print(f"  EN ({len(styled_en)} chars): {styled_en[:160]}...\n")
        if styled_en:
            qb2 = enstyle.encode([styled_en], normalize_embeddings=True)[0]
            b2_results = knn(qb2, enstyle_mat, names, TOP_K)
    else:
        print("Path B2 (styled xlate): SKIPPED (set OPENAI_API_KEY to enable).\n")

    # ---- side-by-side ----
    print("=" * 116)
    header = f"{'PATH A — KO direct (mstyle)':<38}{'PATH B1 — plain xlate (enstyle)':<38}{'PATH B2 — styled xlate (enstyle)':<38}"
    print(header)
    print("-" * 116)
    col_a = _fmt_col(a_results)
    col_b1 = _fmt_col(b1_results)
    col_b2 = (
        _fmt_col(b2_results)
        if b2_results
        else ["  (skipped — no OPENAI_API_KEY)"] + [""] * (TOP_K - 1)
    )
    for i in range(TOP_K):
        print(f"{col_a[i]:<38}{col_b1[i]:<38}{col_b2[i]:<38}")
    print("=" * 116)
    print(
        "\nJUDGE BY HAND: play a clip of your top match(es). Does that creator actually"
    )
    print(
        "structure thoughts like the person in this sample? Compare B1 (plain) vs B2 (styled) —"
    )
    print(
        "does style-preserving translation change/improve the match? Repeat for 5-10 samples."
    )
    print(
        "For an objective read, run: python bracket.py  (needs bilingual samples — see README)."
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python match.py <path-to-native-language-audio>")
        sys.exit(2)
    main(sys.argv[1])
