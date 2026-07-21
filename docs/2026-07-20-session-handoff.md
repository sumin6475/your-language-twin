# Session Handoff — 2026-07-20 (pick up here)

*Read this first to continue exactly where the last session stopped. This is the "current state +
next steps" note. For deep background read `2026-07-20-session-context-primer.md`; for the product
spec read `reference/PRD.md`; for the engineering spec read `reference/2026-07-20-agent-architecture-spec.md`.*

---

## 30-second status

**Your Ideal Role Model (Language Role Model)** — an AI that reads how you talk in your native
language and matches you to real English creators (vloggers) who talk a similar way, with checkable
evidence. Hackathon: OpenAI Build Week, Education track, **due 2026-07-21 17:00 PT** (tomorrow).

- **Backend: essentially done.** FastAPI `/match`, the 3-GPT-call reasoning pipeline, demo cache
  added, embedding singleton fixed. Tests pass. **Not yet run end-to-end locally with real keys.**
- **Frontend: mid-rebuild.** Codex built a working-but-flat Next.js version. Decision: **rebuild the
  frontend at Claude Design fidelity via Claude Code**, preserving the real data binding. Claude
  Design surfaces are being upgraded via the request docs (see Next steps).
- Docs were reorganized and the PRD replaced with v2 (see Doc map).

## Tool split (keep this)

- **Codex** = backend only (the pipeline). Source of truth for the API.
- **Claude Code** = frontend (builds real Next.js in `web/` from Claude Design).
- **Claude Design** (studio project) = the visual source of truth (`.dc.html` surfaces).
- **This chat** = strategy, branding, copy, review, doc-keeping.
- Do not let Codex and Claude Code edit `web/` at the same time.

## Doc map (after reorg)

- **`docs/reference/`** (static / canonical): `PRD.md` (v2), `2026-07-20-agent-architecture-spec.md`
  (engineering source of truth), `phase0-findings.md`, `design-system/` (DESIGN.md, tokens.json,
  tailwind.config.js, ui-spec.md, landing-motion-spec.md), `brand/` (brand-message-brief,
  why-panel-spec).
- **`docs/` root** (one-off): the strategy, the context primer, plan-stage prompts, and all the
  request docs (see below). `AGENTS.md` links point at `docs/reference/…`.

## Locked decisions and rules (non-negotiable)

- **Positioning:** "Learn English from someone who already talks the way you do." Differentiation:
  "Most apps help you sound like a native speaker. We find the native speaker who already sounds like
  you." Why-native uses **"similar in any language"** (never "same").
- **Reasoning system:** deterministic FastAPI supervisor, 3 real GPT-5.6 calls (A Style Reader, B
  Evidence Writer, C Confidence Judge kept separate), + non-GPT transcript & matcher, opt-in Memory
  Worker (future). 45s deadline, input gate ≥45s AND ≥120 words, demo cache for reliable demo.
- **Results:** exactly 3 cards, evidence chains (You said → Creator does → Match), **resemblance as a
  word** (strong/clear/partial), never a percentage.
- **Creator network = discovery channel for real vloggers** (a small vlogger gets found by learners
  who talk like them). NOT "learners become role models" (that old cycle is wrong and was corrected).
- **Copy rules:** plain English, no jargon in user-facing copy, **no em dashes**, never "how you
  think" (use "the way you talk"), never mention Shadowing Plus.
- **Privacy:** raw audio deleted right after translation; nothing derived persists by default; memory
  is opt-in + seeded for the demo.

## Done

- PRD upgraded to v2; docs reorganized (reference/ vs root); AGENTS.md links fixed.
- Backend pipeline + demo cache + embedding singleton.
- Strategy, architecture spec (P1/P2/P3 consolidated), branding docs, all request docs written.
- Creator-network concept corrected across strategy, PRD, and request docs.
- Codex built a first Next.js frontend (real data binding, routes, error path, 5.2s processing gate)
  — functional but low visual fidelity, so being rebuilt from Claude Design.

## Next steps (in order)

1. **Run the 3 Claude Design requests** to get corrected, high-fidelity `.dc.html`:
   - `2026-07-20-landing-page-reformat-request.md` (lift Landing to About fidelity + fix outdated copy)
   - `2026-07-20-about-page-reformat-request.md` + `2026-07-20-about-page-upgrade-request.md` (if the
     latest About does not already have the Good-to-know section + the corrected vlogger-discovery
     network)
   - `2026-07-20-webappflow-fix-request.md` (2 surgical fixes: same→similar, creator card → discovery)
2. **Claude Code builds all screens into `web/`** from the Claude Design HTML, at that fidelity,
   **preserving the existing routes and the real `/match` data binding**. Make it cover **every**
   screen: `/` Landing, `/about` About, `/app` (Upload → Processing → Results), `/app/results`
   (real data), the **Empty** state, and `/results` → `/app/results` redirect. Reuse the working
   globals.css tokens + tailwind config (do not re-architect the CSS pipeline).
3. **Local end-to-end test** (backend + frontend + `GROQ_API_KEY` + `OPENAI_API_KEY`): record the
   actual ~1–2 min demo clip, run it through Upload → Processing (viz) → Results, check the evidence
   chains / resemblance words / "audio deleted", and eyeball match quality. Then **seed that clip
   into the demo cache** (`python -m backend.seed_demo_cache <file>`) so the demo is instant, and run
   it once with the backend off to confirm the error path is graceful.
4. **Demo video (<3 min) + README + capture the Codex `/feedback` session ID** → submit.

## Open items / watch-outs

- **End-to-end has never run with real keys.** This is the biggest remaining verification.
- `web/app/layout.tsx` metadata title/description still uses old copy ("structures thoughts like
  you") — update to the new headline.
- The **creator ecosystem** should be the node diagram (learners ↔ vloggers, "gets discovered"), not
  a text paragraph — Claude Design has the diagram; make sure it survives into the Next.js build.
- Confirm the About page being edited is the **latest** (has the human-hook hero, Good-to-know
  caveats, and the corrected discovery network).
- Earlier CSS-not-loading issue was a runtime/cache thing (clean `.next` restart fixes it), not a
  config bug — the Tailwind/tokens setup is correct.

## Key links

- Hackathon: OpenAI Build Week, Education track, deadline 2026-07-21 17:00 PT.
- Methodology: Sumin's "Science of Inputs and Outputs" (full text in the context primer, Appendix A).
- Adjacent product (context only, never merged / never publicly connected): Shadowing Plus.
