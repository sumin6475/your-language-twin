# Phase 0 Findings — SETTLED (GO)

*Updated 2026-07-18 after the full spike run in Claude Code. Phase 0 is DONE. This is the
leverage: the matching question is answered, the pipeline is decided, and the data strategy is
locked. Codex builds on this — it does not re-run the science.*

## The question Phase 0 answered

> Can we match a learner speaking their **native language** to an English creator whose
> **rhetorical style** resembles theirs — well enough to shadow?

**Answer: YES → GO.** Path B validated (it dominates the FLOOR). Phase 1 (the app) is unblocked.

## The decided pipeline: Path B, PLAIN translation

```
native audio → Groq Whisper PLAIN translate (audio → English) → styledistance embed → cosine k-NN
```

| Option | Verdict |
|--------|---------|
| **Path A — embed native text directly** (`mstyledistance`) | **DEAD.** Can't discriminate style within one language; the language gap dominates. |
| **Path B — translate → embed** (`styledistance`) | **THE PIPELINE.** Validated, beats the floor. |
| **STYLED translator** (LLM style-preserving KO→EN) | **ABANDONED — do not build.** See below. |

## Why STYLED was abandoned (important — the code almost went here)

The intuition was that plain Whisper translation flattens idiolect, so an LLM "style-preserving"
translator would help. **It backfired.** The style translator *structurally refines the speaker*
— its sentence-splitting and cleanup erase the very idiolect the style model matches on
(confirmed by geometry measurement, not vibes). Worse, users never input polished English anyway;
the product's goal is their **present, messy speaking voice**. So:

- **Ship PLAIN Whisper translation.** Use Groq's audio→English **translate** task directly.
- `translate.py` (the styled translator) is **shelved** in `reference/spike/` — reference only.
- **Groq gotcha:** `whisper-large-v3-turbo` is transcribe-only and CANNOT translate. The PLAIN
  translate task needs non-turbo **`whisper-large-v3`**.

## GPT-5.6 usage after this decision

Because translation is now PLAIN (Groq, no LLM), **GPT-5.6 is used in ONE place: the "why you
match" explanation** — one warm, specific sentence from the learner's style + our creator
descriptors (never the creator's words). That still satisfies the Build Week "used GPT-5.6"
requirement. (The fingerprint + styled-translation GPT calls are gone.)

## Data strategy (locked — full detail in PRD `## Data Strategy`)

- **Match targets = English creators, always hand-seeded, never a learner.** A learner vector is
  never added to the creator corpus and never returned as another user's match. (Red line.)
- **Corpus row MAY hold:** style_vector, creator_name, source_url (link-out), our own
  human-authored style_descriptors, factual metadata. **MUST NOT hold:** transcripts / long
  verbatim passages / downloaded audio-caption dumps / stored brand assets.
- **Onboarding standardizes intake:** native-language audio, 3 universal topics → pick 1,
  "talk like you'd tell a friend" framing (counters the polished-reading failure mode), ~2 min
  (floor 90s, cap 3 min), no account.
- **Growth flywheel:** aggregate learner vectors (opt-in) only reveal *coverage gaps* → tell
  hand-curation what creators to seed next. Learner-side stores only.
- **Retention:** raw audio destroyed within the job unconditionally; transcript + translation
  transient.

## Optional (NOT a blocker)

Spike hygiene only: rebalance the test corpus (presidents 43 → ~5) + fix a hold-out bug + one
confirmation run (~2.5h). Skip for the sprint unless time is free — it does not gate Phase 1.
