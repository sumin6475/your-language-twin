# CLAUDE.md — Your Ideal Role Model

Guidance for Claude Code working in this repo. Product + backend detail lives in
[`AGENTS.md`](AGENTS.md) and [`docs/reference/`](docs/reference); read those for context.
This file exists mainly to keep two tools from colliding in one repo.

## Tool Ownership — Codex vs Claude Code (READ FIRST)

Codex and Claude Code both work in THIS folder. Codex builds the backend (hackathon rule);
Claude Code builds the frontend because its UI is better. Stay in your lane.

| Area | Owner | Rule for the other tool |
|------|-------|-------------------------|
| `web/` — Next.js UI, design, components | **Claude Code** | Codex must NOT edit `web/`. |
| `backend/` — `/match`, translate → embed → k-NN → GPT-5.6, tiebreaker | **Codex** | Claude Code treats `backend/` as **read-only reference**; never edits it. |
| `docs/`, PRD, specs | **Codex** (source of truth) | Claude Code reads, does not rewrite. |

**The only shared seam is the `/match` API contract** — the response shape the backend
returns (`backend/models.py`) and the frontend renders (`web/lib/matches.ts`). Keep them in
sync but edit only your own side. If the contract must change, flag it first; never edit both
sides in one pass.

**Handoff rules:** never let both tools edit `web/` at the same time; commit before switching
tools; one folder, one tool at a time.

## Frontend changes — port Claude Design into `web/` without regression

When updating `web/` from Claude Design (`.dc.html`) surfaces:

- **`.dc.html` is the LOOK only. The current `web/` is the BEHAVIOR** (routes, `/match` data
  binding, state). Port the visuals onto the existing behavior; do not replace it.
- **Do NOT touch:** the `/match` fetch in `web/app/app/page.tsx`, the types in
  `web/lib/matches.ts`, `RESULT_STORAGE_KEY`, and the `globals.css` design tokens +
  `tailwind.config.js` (reuse them; do not re-architect the CSS pipeline — the earlier
  "CSS not loading" issue was a stale `.next` cache, fixed by a clean restart).
- **Keep all routes:** `/`, `/about`, `/app` (Upload → Processing → Results), `/app/results`.
  Wire static placeholder data in the HTML to the existing props/state, never hardcode.
- **Work on a branch, one screen per commit.** After each screen: `npm run build` passes →
  clean `.next` + `dev` renders with CSS → real `/match` still works on `/app` (results +
  empty + error states) → `git diff` shows only intended changes → commit. If broken, revert
  that one commit.
- **Copy check:** the engine now has 140 creators (10 human-verified, 130 candidate),
  centered matching, and a gated tiebreaker. Do not let ported copy claim anything that
  contradicts this (creator counts, "how we got here" steps, resemblance-as-a-word not a %).

## Before starting
Commit a clean baseline first, so every design change is a reversible diff.
