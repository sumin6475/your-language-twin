# AGENTS.md — Your Ideal Role Model

Context file for Codex. Keep it lean — only what's true everywhere in the repo. Heavy detail
lives in `docs/`. Read the linked docs before working in their area.

## What this is

**Your Ideal Role Model** — a web app for adults learning English. A learner uploads ~2–3 min
of themselves speaking **their native language**; the pipeline analyzes their
*linguistic/rhetorical style* (sentence structure, hedges, persuasion patterns — **not** vocal
timbre) and returns the most-similar real **English creator** to shadow, with a GPT-5.6 "why you
two are alike" sentence and links out to that creator's real videos.

**Non-negotiable direction: native-language-in → English-creator-out.** Never flip it.
Full spec: [`docs/reference/PRD.md`](docs/reference/PRD.md).

## Current status (2026-07-18) — Phase 0 DONE, Phase 1 in progress

Building in Codex, in this folder. Prior Claude-Code spike is **not carried in** — only its
*findings* + reference code, under `reference/spike/` (read-only; do not build on it).

**Read [`docs/reference/phase0-findings.md`](docs/reference/phase0-findings.md) before touching the pipeline.**
The decisions are settled:

- **GO.** Path B validated (dominates the floor). Path A (embed native text directly) is DEAD.
- **The pipeline is PLAIN, not styled:**
  `native audio → Groq Whisper PLAIN translate (audio→English) → styledistance embed → cosine k-NN`.
- **The STYLED (LLM style-preserving) translator is ABANDONED — do not build it.** It refines/
  splits sentences and erases the idiolect the style model needs. `reference/spike/translate.py`
  is shelved, reference only.
- **GPT-5.6 is used in ONE place: the "why you match" sentence.** (Translation is Groq, no LLM.)

## Build order

1. **Phase 1 — thin vertical slice (in progress in `backend/`):** upload native audio → PLAIN
   translate → embed → k-NN over a small hand-seeded creator corpus → results (top-3 + GPT-5.6
   "why" + video links). One synchronous local backend, in-memory corpus, no DB, no accounts.
2. Minimal web UI (upload page + results) calling the backend.
3. Demo video + README + capture the Codex `/feedback` session ID. (Build Week — see bottom.)

Do the core build inside Codex and preserve the session (needed for submission).

## Tech stack

| Layer | Choice | Note |
|-------|--------|------|
| Backend | One synchronous Python service (FastAPI), local | Runs the whole pipeline per request. No worker/queue/DB for the demo. |
| Frontend | Minimal Next.js (or simple page) → calls backend `/match` | Never runs ML itself. |
| ASR + translation | Groq **`whisper-large-v3`** (audio→English **translate** task) | **PLAIN.** `whisper-large-v3-turbo` is transcribe-only and CANNOT translate — do not use it for the translate step. |
| Style embedding | `StyleDistance/styledistance` (English), CPU | Path B. The multilingual `mstyledistance` (Path A) is dead — ignore. |
| Matching | numpy cosine k-NN over a precomputed `corpus.npz` | 6–12 creators; in-memory, no pgvector. |
| LLM ("why you match") | **OpenAI GPT-5.6** | The only LLM call. One sentence from learner style + our creator descriptors (never creator words). |

Budget ceiling ~$10/mo; ~$0 marginal at demo volume. Justify any new paid dependency.

## Architecture

```
native audio (≤3 min)
  → [backend: Groq Whisper PLAIN translate → styledistance embed
             → cosine k-NN over precomputed corpus → GPT-5.6 "why" sentence]
  → results: top-3 creator cards + why + link-out to real videos
```

Corpus is precomputed offline (hand-seeded creators → embed once → `corpus.npz`). The frontend
never touches ML. Raw user audio lives only transiently in the request and is dropped right after
translation.

## Data strategy & legal rules (from PRD `## Data Strategy` — adopt verbatim)

- **Match targets are English creators, hand-seeded, never a learner.** A learner vector is NEVER
  added to the creator corpus and NEVER returned as another user's match target. (Red line.)
- **A corpus row MAY hold:** style_vector, creator_name, source_url (for link-out), our own
  human-authored style_descriptors, factual metadata. **MUST NOT hold:** full transcripts / long
  verbatim passages / multiple excerpts that reconstruct content / downloaded audio or caption
  dumps / stored creator photos/logos.
- The GPT-5.6 "why" is built from **our descriptors**, not the creator's words.
- Onboarding: native-language audio, 3 topics → pick 1, "talk like you'd tell a friend" framing,
  ~2 min (floor 90s, cap 3 min), no account.

## Critical gotchas

- **Ship PLAIN translation. Do NOT build the styled translator** — it was tried and abandoned.
- **`whisper-large-v3-turbo` cannot translate** — use non-turbo `whisper-large-v3` for translate.
- **Path A is dead** — don't embed native-language text directly.
- **Never retain raw user audio** — dropped right after translation; `.gitignore` blocks audio.
- **ML never runs on the frontend.**
- **`reference/spike/` is throwaway** — read for findings, don't import into product code.
- **Legal red lines:** no voice cloning; no scraping / bulk caption pulls; analyze + link out
  only — never rehost transcripts or store creator likeness.

## Conventions

- Python `snake_case`; JS/TS follow create-next-app defaults.
- Trunk-based on `main`; conventional commits (`feat:`, `fix:`, `docs:`, `chore:`…).
- Secrets in env only (`GROQ_API_KEY`, `OPENAI_API_KEY`), never committed.
- **Docs layout:** static/canonical docs (PRD, architecture spec, design-system, brand) live in
  `docs/reference/`; one-off docs (requests, plans, reviews, session primers) sit flat in `docs/`
  root. Keep this split when adding docs.

## Build Week note

Submitting to **OpenAI Build Week** (Education track; deadline 2026-07-21 17:00 PT). Requires:
built with Codex + GPT-5.6, a <3-min demo video covering how both were used, a public/shared repo
with README, and the Codex `/feedback` session ID from where core functionality was built.
