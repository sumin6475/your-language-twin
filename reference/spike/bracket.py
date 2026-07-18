"""
Phase 0 spike — the BRACKET TEST (run this to decide if better translation is worth it).

The adversarial verification analysis said: before comparing "fancy vs plain" translation,
measure how far PLAIN translation already sits from the CEILING. If plain is already near
the ceiling, improving translation chases tiny headroom and should be deferred.

The trick for label-free ground truth: style similarity is subjective, but "this is the SAME
person" is objective. If a bilingual tester gives us BOTH their Korean speech AND their own
genuine English speech/writing, then their real English is the target their Korean SHOULD
translate to, stylistically. We measure, for each variant, how close the variant lands the
person to THEIR OWN English — via self-retrieval rank in a gallery of (English creators + this
person's own English).

Four variants per person, bracketing the achievable range:
  FLOOR    = embed Korean directly (mstyledistance)          [known-bad]
  PLAIN    = Whisper translate -> embed (styledistance)      [current]
  STYLED   = LLM style-preserving translate -> embed         [the improvement]
  CEILING  = embed the person's OWN genuine English          [best possible]

Metric: rank (1 = best) of the person's own English among the gallery, for each variant.
Read it as: does STYLED move the rank meaningfully between PLAIN and CEILING? If PLAIN≈CEILING,
translation work is not the bottleneck.

INPUT: spike/samples/manifest.json — a list of testers, e.g.
[
  {
    "name": "tester1",
    "korean_audio": "samples/tester1_ko.m4a",
    "english_text": "samples/tester1_en.txt"   // their OWN genuine English (spoken transcript or writing)
  }
]
(english_text may also be an audio path ending in .m4a/.mp3/.wav/.mp4 — it'll be transcribed.)

Requires GROQ_API_KEY (+ OPENAI_API_KEY for the STYLED variant). Throwaway spike code.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

import _env  # noqa: F401  — loads spike/.env into os.environ on import

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CORPUS = os.path.join(DATA_DIR, "corpus.npz")
MANIFEST = os.path.join(os.path.dirname(__file__), "samples", "manifest.json")
AUDIO_EXTS = (".m4a", ".mp3", ".wav", ".mp4", ".webm", ".ogg")


def _die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n else v


def _rank_of_self(query_vec, gallery_mat, self_idx: int) -> int:
    """1-based rank of the person's own English among the gallery (1 = closest)."""
    sims = gallery_mat @ _unit(query_vec)
    order = np.argsort(-sims)
    return int(np.where(order == self_idx)[0][0]) + 1


def _topk_names(query_vec, corpus_mat, names, k: int) -> list[str]:
    """Names of the top-k creators for a query vec (corpus rows are unit vectors)."""
    sims = corpus_mat @ _unit(query_vec)
    return [names[i] for i in np.argsort(-sims)[:k]]


def _overlap(a: list[str], b: list[str]) -> int:
    """Size of the set intersection of two top-k name lists."""
    return len(set(a) & set(b))


def _spearman(a: np.ndarray, b: np.ndarray) -> float:
    """Spearman rho of two similarity vectors (rank-correlation of the full ordering).
    numpy-only (no scipy): Pearson correlation of the ranks."""

    def _rank(x):
        return np.argsort(np.argsort(x)).astype(
            float
        )  # 0..n-1; ties arbitrary (fine at n~50)

    ra, rb = _rank(a), _rank(b)
    ra -= ra.mean()
    rb -= rb.mean()
    denom = np.sqrt((ra @ ra) * (rb @ rb))
    return float((ra @ rb) / denom) if denom else 0.0


def _load_english(path_or_text: str) -> str:
    """Load the person's genuine English: a .txt file, an audio file, or inline text.
    Under the LOCKED philosophy this MUST be the tester's NATURAL, unrehearsed English
    (disfluency intact) — NOT a polished/presentation register. Prefer TEXT: supplying it
    as .txt embeds it directly and avoids the Whisper ASR fingerprint that biases PLAIN.
    The manifest documents which recording was used; this loader is register-agnostic."""
    from match import transcribe

    p = (
        os.path.join(os.path.dirname(__file__), path_or_text)
        if not os.path.isabs(path_or_text)
        else path_or_text
    )
    if os.path.exists(p):
        if p.lower().endswith(AUDIO_EXTS):
            return transcribe(p, translate=False)  # already-English audio
        with open(p, encoding="utf-8") as f:
            return f.read().strip()
    return path_or_text  # treat as inline text


def _split_english(text: str, frac: float = 0.5):
    """Optional held-out split: first `frac` = CEILING gallery anchor, rest = probe.
    Guards against self-retrieval being trivially rank-1 because the SAME text is both
    query and gallery row, and kills content leakage. Sentence-granular; returns
    (anchor, probe). If too short to split, returns (text, text)."""
    import re

    sents = re.split(r"(?<=[.!?…])\s+", text.strip())
    if len(sents) < 4:
        return text, text
    cut = max(1, int(len(sents) * frac))
    return " ".join(sents[:cut]).strip(), " ".join(sents[cut:]).strip()


def main() -> None:
    if not os.path.exists(CORPUS):
        _die("data/corpus.npz missing. Run: python build_corpus.py")
    if not os.path.exists(MANIFEST):
        _die(
            f"{MANIFEST} missing. Create it — see the docstring at the top of bracket.py."
        )

    with open(MANIFEST, encoding="utf-8") as f:
        testers = json.load(f)
    if not testers:
        _die("manifest.json is empty.")

    from sentence_transformers import SentenceTransformer

    from match import transcribe  # reuse

    cache = os.path.join(DATA_DIR, "cache")
    data = np.load(CORPUS, allow_pickle=True)
    creator_names = list(data["names"])
    creator_en = data["enstyle"]  # English style vectors of the creators
    creator_ko = data["mstyle"]  # multilingual vectors (for the FLOOR gallery)

    mstyle = SentenceTransformer("StyleDistance/mstyledistance", cache_folder=cache)
    enstyle = SentenceTransformer("StyleDistance/styledistance", cache_folder=cache)
    have_openai = bool(os.environ.get("OPENAI_API_KEY"))

    rows = []
    for t in testers:
        name = t.get("name", "?")
        ko_audio = t["korean_audio"]
        ko_audio = (
            ko_audio
            if os.path.isabs(ko_audio)
            else os.path.join(os.path.dirname(__file__), ko_audio)
        )
        if not os.path.exists(ko_audio):
            print(f"  [{name}] skip: korean_audio not found ({ko_audio})")
            continue

        print(f"\n[{name}] transcribing Korean ...")
        ko_text = transcribe(ko_audio, translate=False)
        # NATURAL English is the target (fact A/B). english_natural wins if provided.
        own_en_text = _load_english(t.get("english_natural") or t["english_text"])
        if not own_en_text:
            print(f"  [{name}] skip: no english_text")
            continue

        # Optional held-out split so the gallery anchor != the CEILING query text.
        if t.get("holdout"):
            anchor_text, probe_text = _split_english(own_en_text)
        else:
            anchor_text = probe_text = own_en_text

        # EN gallery = creators + this person's OWN english ANCHOR (appended last row).
        anchor_en_vec = enstyle.encode([anchor_text], normalize_embeddings=True)[0]
        en_gallery = np.vstack([creator_en, _unit(anchor_en_vec)])
        self_idx = len(creator_names)  # own english is the appended last row

        # FLOOR: KO direct in the multilingual gallery (creators + own-english via mstyle).
        anchor_en_m = mstyle.encode([anchor_text], normalize_embeddings=True)[0]
        m_gallery = np.vstack([creator_ko, _unit(anchor_en_m)])
        ko_vec_m = mstyle.encode([ko_text], normalize_embeddings=True)[0]
        floor_rank = _rank_of_self(ko_vec_m, m_gallery, self_idx)

        # PLAIN: Whisper translate -> enstyle
        plain_en = transcribe(ko_audio, translate=True)
        plain_vec = enstyle.encode([plain_en], normalize_embeddings=True)[0]
        plain_rank = _rank_of_self(plain_vec, en_gallery, self_idx)

        # STYLED: LLM style-preserving translate -> enstyle
        styled_rank = styled_vec = styled_top = None
        if have_openai:
            from translate import translate_styled

            styled_en = translate_styled(ko_text)
            if styled_en:
                styled_vec = enstyle.encode([styled_en], normalize_embeddings=True)[0]
                styled_rank = _rank_of_self(styled_vec, en_gallery, self_idx)

        # CEILING: the person's PROBE english embedded directly. With holdout this is a
        # DIFFERENT slice than the gallery anchor (rank is meaningful); without holdout it
        # is the same text (rank ~1 by construction — a sanity check only).
        ceiling_vec = enstyle.encode([probe_text], normalize_embeddings=True)[0]
        ceiling_rank = _rank_of_self(ceiling_vec, en_gallery, self_idx)

        # --- Creator-ordering agreement vs the CEILING (the REAL signal; robust to ASR bias) ---
        c_top3 = _topk_names(ceiling_vec, creator_en, creator_names, 3)
        c_top5 = _topk_names(ceiling_vec, creator_en, creator_names, 5)
        c_sims = creator_en @ _unit(ceiling_vec)

        p_top3 = _topk_names(plain_vec, creator_en, creator_names, 3)
        p_top5 = _topk_names(plain_vec, creator_en, creator_names, 5)
        p_sims = creator_en @ _unit(plain_vec)
        cos_plain = float(_unit(plain_vec) @ _unit(ceiling_vec))
        rho_plain = _spearman(p_sims, c_sims)
        ov3_plain, ov5_plain = _overlap(p_top3, c_top3), _overlap(p_top5, c_top5)
        hit1_plain = p_top3[0] == c_top3[0]

        if styled_vec is not None:
            s_top3 = _topk_names(styled_vec, creator_en, creator_names, 3)
            s_top5 = _topk_names(styled_vec, creator_en, creator_names, 5)
            s_sims = creator_en @ _unit(styled_vec)
            cos_styled = float(_unit(styled_vec) @ _unit(ceiling_vec))
            rho_styled = _spearman(s_sims, c_sims)
            ov3_styled, ov5_styled = _overlap(s_top3, c_top3), _overlap(s_top5, c_top5)
            styled_top = s_top3[0]
            hit1_styled = s_top3[0] == c_top3[0]
        else:
            cos_styled = rho_styled = ov3_styled = ov5_styled = hit1_styled = None

        rows.append(
            {
                "name": name,
                "floor": floor_rank,
                "plain": plain_rank,
                "styled": styled_rank,
                "ceiling": ceiling_rank,
                "ceiling_top1": c_top3[0],
                "plain_top1": p_top3[0],
                "styled_top1": styled_top,
                "cos_plain": cos_plain,
                "cos_styled": cos_styled,
                "ov3_plain": ov3_plain,
                "ov5_plain": ov5_plain,
                "ov3_styled": ov3_styled,
                "ov5_styled": ov5_styled,
                "rho_plain": rho_plain,
                "rho_styled": rho_styled,
                "hit1_plain": hit1_plain,
                "hit1_styled": hit1_styled,
                "holdout": bool(t.get("holdout")),
            }
        )

    if not rows:
        _die("no testers produced results — check manifest paths and API keys.")

    n_creators = len(creator_names)
    print("\n" + "=" * 78)
    print(
        f"BRACKET TEST — {n_creators} creators + self. Headline = agreement with NATURAL-English CEILING."
    )
    print("-" * 78)
    print(
        f"{'tester':<11}{'FLOOR':>6}{'PLAIN':>6}{'STYLED':>7}{'CEIL':>5}   "
        f"{'ceiling_top1':<20} {'plain_top1':<20} {'styled_top1'}"
    )
    for r in rows:
        styled = r["styled"] if r["styled"] is not None else "—"
        stop = (r["styled_top1"] or "—")[:20]
        hb = " [holdout]" if r["holdout"] else ""
        print(
            f"{r['name'][:10]:<11}{r['floor']:>6}{r['plain']:>6}{str(styled):>7}{r['ceiling']:>5}   "
            f"{r['ceiling_top1'][:20]:<20} {r['plain_top1'][:20]:<20} {stop}{hb}"
        )
    print("-" * 78)
    print("AGREEMENT WITH CEILING (the DECISION metrics — trust these over rank):")
    print(
        f"{'tester':<11}{'hit@1 pl/st':>12}{'ov3 pl/st':>10}{'ov5 pl/st':>10}"
        f"{'rho pl/st':>12}{'cos pl/st':>14}"
    )
    for r in rows:

        def _ps(p, s, fmt="{}"):
            sp = fmt.format(s) if s is not None else "—"
            return f"{fmt.format(p)}/{sp}"

        hit = _ps(
            "Y" if r["hit1_plain"] else "n",
            ("Y" if r["hit1_styled"] else "n")
            if r["hit1_styled"] is not None
            else None,
        )
        ov3 = f"{r['ov3_plain']}/{r['ov3_styled'] if r['ov3_styled'] is not None else '—'}"
        ov5 = f"{r['ov5_plain']}/{r['ov5_styled'] if r['ov5_styled'] is not None else '—'}"
        rho = _ps(r["rho_plain"], r["rho_styled"], "{:.2f}")
        cos = _ps(r["cos_plain"], r["cos_styled"], "{:.3f}")
        print(f"{r['name'][:10]:<11}{hit:>12}{ov3:>10}{ov5:>10}{rho:>12}{cos:>14}")
    print("=" * 78)
    print("READ IT:")
    print(
        "  • hit@1 = does the variant's #1 creator equal the CEILING's #1 creator? (pl / st)"
    )
    print(
        "  • ov3/ov5 = how many of the CEILING's top-3 / top-5 creators the variant also"
    )
    print(
        "            surfaces — the product-relevant number (same creators the real English would?)."
    )
    print(
        "  • rho = Spearman of the FULL 51-creator ordering vs the ceiling. cos = cosine to ceiling."
    )
    print(
        "  • *_top1 columns: if plain_top1 != styled_top1, the styled path CHANGES what the user"
    )
    print(
        "            sees. Decisive product question: does styled_top1 match ceiling_top1 and plain not?"
    )
    print(
        "  • CONFOUND: PLAIN and a Whisper-transcribed CEILING share ASR surface, so PLAIN's rank+cos"
    )
    print(
        "            are biased UP for reasons unrelated to style. DECIDE on hit@1/ov3/ov5/rho, not rank/cos."
    )
    print(
        "  • Set holdout=true so the CEILING probe != the gallery anchor (else CEILING rank is trivially ~1)."
    )
    print(
        "  • n=1 gates NOTHING about STYLED. The gate is the blinded 2AFC across >=5 varied testers (README)."
    )


if __name__ == "__main__":
    main()
