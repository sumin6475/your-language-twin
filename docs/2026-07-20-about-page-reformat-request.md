# About Page — Reformat Request (lift the persuasion to WebAppFlow level)

*2026-07-20. Paste into Claude Code / Claude Design. It has the existing design system, the aurora
background, the rise/pop animations from `WebAppFlow.dc.html`, and the current `About.dc.html`. Goal:
keep all the substance, but rebuild the About page so it reads like a story with peaks, not a flat
spec sheet. The quality bar is the Processing screen in `WebAppFlow.dc.html` (staged reveal, one
clear hero moment). Do not change the product claims or invent features.*

---

## The problem with the current About (what to fix)

The content is all correct, but the delivery is flat:
1. Every section has the same rhythm and the same visual weight, so nothing grabs. There is no peak.
2. The 5 agent steps are 5 near-identical cards with no connectors, so they read as a feature list,
   not a reasoning chain.
3. The strongest line (the "We are not matching by topic or vocabulary" quote) is buried at the end
   of a section instead of being a hero moment.
4. The vision mockups are dimmed to ~0.62 opacity, which makes them feel unfinished and undesirable
   instead of something you want.
5. There is no human entry point and no motion. It informs, it does not pull.

## Global rules (keep these)

- **Reuse the existing design system**: tokens, components, the aurora background, and the
  `lrm-rise` / `lrm-pop` / scan animations already defined in `WebAppFlow.dc.html`.
- **Status vocabulary stays**: `Live` (blue) for what the demo does, `Coming soon` (dashed) for
  vision.
- **Copy rules**: plain English, no jargon in body copy, **no em dashes** (commas, periods, "then"),
  resemblance stays a word, never mention Shadowing Plus, no fabricated numeric scores.
- **Keep all substance**: the idea, the 5 agents, the pull-quote, the real-vs-next split, and the
  four vision mockups (Personal Language Memory, Language Twin, the loop, the creator network). This
  is a reformat for impact, not a content cut.
- **Add motion**: sections rise in on scroll (reuse `lrm-rise`), the pipeline reveals step by step,
  the Confidence Judge pops. Match the Processing screen's feel.

## New narrative arc (reorder into a story with peaks)

Rebuild the page as six beats, each with a distinct layout so the eye gets variety:

**Beat 1 — Human hook (NEW, the emotional entry).**
Before any abstraction, one vivid, relatable beat. A large centered line, then the idea headline.
- Small line (muted): `You have been told to copy a native speaker.`
- Hero headline (largest type on the page): `But copying a stranger who talks nothing like you feels like wearing a costume.`
- Then the turn, one line: `So we start from how you already talk.`
This is the biggest type moment on the page. Give it real air (large top padding, generous line
height). No card, just type on the aurora.

**Beat 2 — The shift (make the differentiation a designed moment, not a paragraph).**
Turn the "Most apps / We" contrast into a visual two-side comparison, not body text:
- Left (muted, the old way): `Most apps help you sound like a native speaker.`
- Right (blue, our way): `We find the native speaker who already sounds like you.`
Lay them side by side with a divider or an arrow between, so the reframe reads in one glance. Under
it, the plain why-native line: `The way you build a sentence, ask a question, or tell a story is the same in any language, and that is what we listen for.`

**Beat 3 — How the reasoning works (make it a FLOW, with motion, Judge as hero).**
- Keep the 5 agents, but connect them as a real pipeline: vertical connectors or arrows between the
  cards so it reads as a chain, not a list. Number them, and let them **rise in one by one on scroll**
  (staged `lrm-rise`, like the Processing screen).
- The **Confidence Judge is the visual hero**: bigger card, blue border, the shield icon, and a short
  "the step that keeps us honest" sublabel (reuse the Processing screen's Confidence card styling
  exactly, for continuity).
- Keep each agent's plain description and the small `Agent N` mono tag.

**Beat 4 — The payoff line (promote the pull-quote to a hero moment).**
Pull the "We are not matching by topic or vocabulary" quote out into **its own full-width statement
section**, large display type, centered, generous padding, maybe a thin blue rule above and below.
This is the intellectual peak of the page. It should feel like the mission, not a footnote.
Exact text (keep verbatim, no em dashes): `We are not matching people by topic or vocabulary. We build a reasoning based language profile, verify every behavioral claim against your own transcript, and only then search for creators whose communication patterns truly align.`

**Beat 5 — The vision, as a desirable showcase (mockups at full fidelity).**
This is where the ambition lives. Two changes from today:
- **Stop dimming the mockups to 0.62.** Render them at near-full fidelity so they look like real,
  polished product, each with a clear `Coming soon` badge. The badge does the "not built" work, not
  the greying-out. We want the judge to think "I want that," not "that looks unfinished."
- Give the two richest mockups room to be showcases:
  - **Personal Language Memory**: the Day 1 vs Day 14 comparison, full fidelity, with the off-by-default
    opt-in toggle. Add a one-line frame above it: `Your matches are step one. The profile keeps growing.`
  - **Your Language Twin**: the profile card with the qualitative bars (keep the "seen in your clips"
    labels, no numbers). Make it feel like a dashboard you would open daily.
  - The **loop** and the **creator network** stay as the connected chip diagrams, but give them a touch
    more size and a one-line "why it matters" under each (the network one already has it, keep it).
- Section intro headline: `Where a Personal Language Twin takes this.` + `Everything below is the vision, mocked up, not built yet.`

**Beat 6 — Close.**
A confident CTA `Try the demo` (routes to the app), plus the legal line and `Request removal`. Keep
it simple.

## Pacing and layout variety (so it does not feel like one long column)

- Vary widths: Beat 1 and Beat 4 are wide and centered (statement moments); Beat 3 is a tighter left
  column (the technical block); Beat 5 is a wide showcase. Do not keep everything at the same
  max-width and center alignment.
- Add generous vertical space between beats (section gaps larger than today), and a subtle divider or
  a change in background tint between the "how it works" block and the "vision" block, so the reader
  feels they crossed from "real" into "what is next".
- Reuse the aurora background, but consider letting Beat 1 and Beat 4 sit directly on it (no card) for
  contrast against the carded technical sections.

## What NOT to do

- Do not cut any of the substance (5 agents, pull-quote, real-vs-next, 4 mockups all stay).
- Do not add numeric scores ("9/10", "164 behaviors", "%") anywhere.
- Do not add em dashes, jargon in body copy, or any mention of Shadowing Plus.
- Do not invent new product features or claims; this is a reformat of what exists.
- Do not introduce new colors or fonts; reuse the tokens only.

## Output

Rebuild `About.dc.html` (or the Next.js About page) as the six beats above, reusing the existing
components, tokens, aurora, and animations. Keep the `Live` / `Coming soon` badges. Deliver one
polished, scannable page that reads like a story and matches the Processing screen's level of polish.
