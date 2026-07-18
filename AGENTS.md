# AGENTS.md — Your Ideal Role Model

Context file for Codex. Keep it lean — only what's true everywhere in the repo. Heavy detail
lives in `docs/`. Read the linked docs before working in their area.

## What this is

**Your Ideal Role Model** — a web app for adults learning English. A learner uploads ~2–3 min
of themselves speaking **their native language**; the pipeline analyzes their
*linguistic/rhetorical style* (sentence structure, hedges, persuasion patterns — **not** vocal
timbre) and returns the most-similar real **English creator** to shadow, with an LLM "why you
two are alike" profile and links out to that creator's real videos.

**Non-negotiable direction: native-language-in → English-creator-out.** This is the core novelty;
do not flip it. Full spec: [`docs/PRD.md`](docs/PRD.md).

## Current status (2026-07-18)

Greenfield rebuild in Codex. The prior Claude-Code spike is **not carried in** — only its
*findings* and reference code are, under `reference/spike/` (read-only; do not build on it).

**The make-or-break matching science is already directionally settled** — read
[`docs/phase0-findings.md`](docs/phase0-findings.md) before touching the pipeline. Summary:

- **Path A (embed native-language text directly) is DEAD.** Don't build it.
- **Path B (translate → embed with `styledistance` → k-NN) WORKS.** This is the architecture.
- The design includes a **style-preserving KO→EN translator** (preserves hedges/rhythm the style
  model matches on). Prompt logic exists in `reference/spike/translate.py`; design in
  [`docs/translation-design.md`](docs/translation-design.md).
- **Not yet done:** the objective bracket test on real bilingual audio. Closing it is the first
  engineering task (needs API keys + samples).

## Build order

1. **Close Phase 0** — run the bracket test on real audio; decide styled-vs-plain translator. Do
   this in a Codex session and keep the `/feedback` session ID (needed for the Build Week submission).
2. **Phase 1 — thin vertical slice:** upload native audio → transcribe → translate → embed → k-NN
   over a precomputed creator corpus → results page (top-3 + LLM "why" + video links). No accounts.
3. Later (post-MVP): shadowing pedagogy loop; corpus at scale; personalization. Deferred.

## Tech stack

| Layer | Choice | Note |
|-------|--------|------|
| Frontend / API | Next.js (App Router) on Vercel | Orchestrates + polls only. **Never runs ML here** (no GPU, short timeouts). |
| ASR | Groq `whisper-large-v3-turbo` (transcribe) / `whisper-large-v3` (translate) | Free tier. `translate` endpoint needs non-turbo. |
| Style embedding | `StyleDistance/styledistance` (English), CPU | Path B. The multilingual `mstyledistance` is Path A — dead, ignore. |
| Worker | Python worker (Railway) | Async: Whisper → translate → embed → k-NN → LLM profile. |
| Vector store + jobs | pgvector on Railway Postgres | Embeddings + creator metadata + job rows. Brute-force cosine is fine at MVP scale. |
| LLM ("why you match" + styled translation) | **OpenAI GPT-5.6** | Build Week requires GPT-5.6 in the build. (Spike used gpt-4o-mini for translation — upgrade to GPT-5.6.) |

Budget ceiling ~$10/mo; effectively ~$0 marginal at MVP volume. Justify any new paid dependency.

## Commands

```bash
# Reference spike (read-only — how Phase 0 was validated; do NOT extend it)
cd reference/spike && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY=...      # free: https://console.groq.com/keys
export OPENAI_API_KEY=...    # styled translation
python build_corpus.py
python match.py <native-language-audio>   # 3-way comparison
python bracket.py                          # objective gate (needs samples/manifest.json)

# Phase 1 web app + worker: scaffold here; add real dev/build/test commands to this file.
```

## Architecture (Phase 1 target)

```
native audio (≤3 min)
  → [Vercel: upload, write job row]
  → [Railway worker: Groq Whisper → style-preserving translate → styledistance embed
                     → cosine k-NN over precomputed corpus → GPT-5.6 "why" profile]
  → [Vercel: poll/SSE → results page]
  → link out to creators' real videos
```

Corpus is precomputed offline (collect licensed creator text → embed once → store in pgvector).
The frontend never touches ML.

## Critical gotchas

- **Never run Whisper/embeddings on Vercel** — ML lives only in the Railway worker.
- **Never retain raw user audio** — delete after transcription (privacy promise; `.gitignore`
  must block audio commits).
- **Path A is dead** — do not spend time embedding native-language text directly.
- **`reference/spike/` is throwaway** — read it for findings, don't import from it into product code.
- **Legal red lines:** no voice cloning; no scraping YouTube at scale; analyze + link out only —
  never rehost transcripts or market with a creator's name/likeness.

## Conventions

- Python: `snake_case`. JS/TS: follow create-next-app defaults.
- Trunk-based on `main`; conventional commits (`feat:`, `fix:`, `docs:`, `chore:`…).
- Secrets in env only, never committed (`GROQ_API_KEY`, `OPENAI_API_KEY`, Railway `DATABASE_URL`).

## Build Week note

This project is being submitted to **OpenAI Build Week** (Education track; deadline 2026-07-21
17:00 PT). Submission requires: built with Codex + GPT-5.6, a <3-min demo video covering how both
were used, a public/shared repo with README, and the Codex `/feedback` session ID from where core
functionality was built. Do the core build inside Codex and preserve that session.
