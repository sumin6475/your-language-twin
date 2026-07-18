# Phase 0 Findings — what the science spike already settled

*Distilled 2026-07-18 from the throwaway spike (`reference/spike/`). This is the leverage:
the make-or-break matching question is directionally answered, so Codex does **not** need to
re-run the science — it builds on this conclusion.*

## The one question Phase 0 exists to answer

> Can we find an English creator whose **linguistic/rhetorical style** genuinely resembles a
> learner speaking their **native language** — well enough to be worth shadowing?

## Conclusion (directional): YES, via Path B

| Path | What it does | Verdict |
|------|--------------|---------|
| **A — direct** | Embed the Korean transcript with a multilingual style model (`mstyledistance`) → k-NN | **DEAD.** The model can't discriminate style *within* Korean (formal vs. analytic Korean scored ~0.997 cosine); Korean-vs-English similarity is dominated by the language gap, not style. Centering didn't fix it. Do not build on this. |
| **B — translate then embed** | Translate Korean → English, embed with the English style model (`styledistance`) → k-NN | **WORKS.** English style probes land on the right style-matched creators. This is the architecture. |

## The catch that shapes Phase 1

Plain Whisper translation **flattens the speaker's idiolect** — hedges, fillers, rhythm — which
is exactly the signal `styledistance` matches on. A text-level test confirmed it: the *same*
Korean utterance translated plainly matched a "high-energy" creator (wrong), but translated with
**style preservation** matched a "hedged casual explainer" (right), 0.95 vs 0.88.

→ **The design is Path B with a style-preserving KO→EN translator** (two small LLM calls:
extract a rhetorical fingerprint, then translate while preserving hedges/fillers/rhythm). Full
design + the inverted-principles prompt: [`translation-design.md`](./translation-design.md).
Working prompt logic already exists in [`../reference/spike/translate.py`](../reference/spike/translate.py).

## What is NOT yet done (the honest gap)

- The **objective bracket test on real bilingual audio has not been run.** The direction above
  came from text-level tests + a small hand-authored corpus (the spike's built `corpus.npz` held
  only ~6 creators, despite an aspirational "51 speakers" note in the old spike README). Treat
  Path B as *chosen*, not *empirically gated on real voices* yet.
- Needs, to close it: `GROQ_API_KEY` (ASR) + `OPENAI_API_KEY` (styled translation) + 5–10
  native-language samples, ideally with each speaker's own genuine English as the "ceiling."
- **Decision the bracket test still owes us:** does style-preserving translation beat plain
  translation *enough to build the translator into Phase 1*, or is plain translation already near
  the ceiling? (If PLAIN ≈ CEILING, ship plain and defer the styled translator.)

## Known floors / caveats to carry forward

- **ASR erases some idiolect before translation even runs** — Whisper cleans up fillers. That's a
  floor no prompt can recover; part of why we measure the ceiling.
- **Corpus representation mismatch (Phase 1 item):** the corpus English side was clean text; a
  translator that preserves disfluency may push the query into empty space. The honest fix is
  rebuilding *both* sides of the k-NN through the same style-preserving translator.
- **"Style similarity" is subjective, no ground truth** — present matches as "creators you'll
  learn well from," keep the human thumbs-up signal, use the LLM "why you match" for credibility.
