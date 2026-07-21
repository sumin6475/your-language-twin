# Codex Build Plan — Phase 1 (lean, demo-first)

Working checklist for building in Codex. Complements [`../AGENTS.md`](../AGENTS.md) (always-true
context). Build one slice at a time: Codex proposes → writes → tests → Sumin reviews → commit → next.

## Reference-only note (read this first)

There is a heavy Build-System plan (`phase1-thin-vertical-slice.md`) in the *other* project folder.
It is **REFERENCE ONLY — for rules and copy, NOT architecture.**

- **DO NOT adopt its architecture:** no Postgres/pgvector, no docker-compose, no separate
  `worker/`, no Railway/Vercel deploy, no job queue/polling/SSE. Keep the current **single
  synchronous in-memory FastAPI backend + minimal frontend, run locally.**
- **DO NOT switch the LLM:** the "why" stays **GPT-5.6** (Build Week requires GPT-5.6). The heavy
  plan's "why via Claude/Vercel AI Gateway" does not apply here.
- The good parts to keep from it are already distilled into "Rules to honor" below.

## Current state (done)

- `backend/` single FastAPI `/match`: PLAIN translate (Groq `whisper-large-v3`) → `styledistance`
  embed → numpy cosine top-3 → GPT-5.6 "why". In-memory corpus, no DB. Raw audio dropped after
  translation. Tests green (pytest 3, ruff clean).

## Remaining slices (in order)

1. **Corpus swap + rebuild.** Replace `backend/data/creators.json` with the 26-creator
   `backend/data/creators.seed.json`; rerun the corpus build so `corpus.npz` regenerates (embed each
   `style_seed`, mean-pool if chunked). Run tests. *(Acceptance: 26 rows embedded; `/match` returns
   3 real creators with channel links.)*
2. **Minimal frontend.** Upload page → calls backend `/match` → results page with 3 cards. Honor the
   Rules below. No account, no recorder required (upload is enough for the demo).
3. **End-to-end run (HUMAN — needs keys).** One real Korean sample through the full local stack with
   `GROQ_API_KEY` + `OPENAI_API_KEY`. Sanity-check the top-3 + "why" read right.
4. **Ship prep.** README (one-command local run, env vars, architecture, privacy, corpus provenance,
   demo steps) + record the <3-min demo video + capture the Codex `/feedback` session ID for Devpost.

## Design system (use it — do not invent your own)

The frontend MUST follow `docs/design/`:

- `DESIGN.md` — the rules (when to use what, what never to do). Load it into context before building UI.
- `tokens.json` — the values (source of truth). Use only defined tokens; never invent colors or sizes.
- `tailwind.config.js` — use as the base Tailwind config when scaffolding the frontend. Load the
  Clash Display + Inter fonts in the HTML head (URLs are in that file's comment).

Obey: Signature Blue (blue is accent only; white/grey by default), Clash Display for display + Inter
for body, generous spacing (section gaps >= 48px), soft shadows, and the AI-cliche guardrails in
DESIGN.md section 7. **No em dashes in any user-facing copy** (DESIGN.md 4.2) — use commas, periods,
or "then". Real-sentence headlines, not slogans; real names/data, never placeholders.

## Rules to honor (distilled from PRD + the reference plan)

- **Exactly 3 matches.** If the corpus has < 3 rows, fail loudly ("corpus not seeded"), never return
  fewer.
- **Match chip carries a tier label, not a raw number (default).** DESIGN.md shows a match chip
  (blue.tint). Put a tier word in it ("strong resemblance" / "clear resemblance" / "partial
  resemblance"), never the raw cosine score — style similarity is a fit signal, not a precise
  measurement. (If Sumin prefers the playful horoscope vibe, a clearly-framed style score is an
  allowed alternative — confirm with her before using a number.)
- **Privacy copy on results:** "✓ Audio deleted. Nothing you said was stored." (True: no audio,
  transcript, translation, or vector is persisted.)
- **Legal footer:** "Not affiliated with or endorsed by any creator." + a takedown `mailto:` using a
  `CONTACT_EMAIL` const (Sumin confirms the address before demo).
- **Corpus rows:** only `id/name/role/video_url/source_note/style_seed`; `source_note`/`role` are OUR
  descriptors; `style_seed` is OUR authored style-representative text — never paste verbatim creator
  transcripts anywhere. `video_url` is the creator's own channel (link-out only).
- **Graceful "why" fallback:** if the GPT-5.6 call fails, show a neutral one-line fallback rather than
  erroring the whole match.
- **Landing page:** value prop ("find the English creator who structures thoughts like you") +
  the privacy promise + an 18+ affirmation line.
- **Creator teaser:** a static "For creators — coming soon" section (see PRD `## Data Strategy` →
  creator opt-in). Copy: *"Are you a creator? Learners who think like you are looking for someone to
  shadow. Soon you'll be able to add your voice, with your consent, and get discovered. Coming soon."*
  (No em dashes in UI copy — DESIGN.md 4.2.)
- **Should-if-time (optional, not required for demo):** topic-prompted onboarding — 3 universal
  topics, pick 1, "talk the way you'd tell a friend" framing, ~90s soft floor; in-browser recorder.
  Upload-only is an acceptable MVP; add this only if the frontend slice lands with time to spare.

## Do not (red lines)

No scraping / caption downloaders / YouTube tooling; no rehosting transcripts; no voice cloning; no
storing creator photos/logos; never run ML on the frontend; never persist raw user audio.
