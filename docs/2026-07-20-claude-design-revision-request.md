# Claude Design — Revision Request (Landing + new About/Vision page + App polish)

*2026-07-20. Paste this into Claude Design. It has the existing design system, `Landing.dc.html`,
and `WebAppFlow.dc.html` already. Goal: three coherent surfaces — a clean honest Landing, a new
About/Vision page that carries the depth and the ideal-app mockups, and light polish on the App
(demo). Reuse the existing components, tokens, and the aurora/animation style already in
`WebAppFlow.dc.html`. Do not invent a new design system.*

---

## Why this change (context)

Today `WebAppFlow.dc.html` (the app: Upload / Processing / Results / Empty) is up to date and strong.
But `Landing.dc.html` is an old version and still contradicts the product. And a marketing landing
cannot hold the full vision without over-claiming. So we split into three surfaces:

- **Landing** = sell it, honestly. Only what the demo actually does.
- **About / Vision (NEW page)** = the depth the landing cannot hold: the reasoning system, the agent
  pipeline, and the ideal-app **mockups** (memory, loop, network, Language Twin), all clearly
  labeled as vision.
- **App** = the working demo (already good), plus small technical-credibility touches.

## Global rules (apply to all three surfaces)

1. **Reuse the existing design system.** Same components (Button, Card, Badge, Avatar,
   ConsentCheckbox, MatchCard), tokens, and the aurora background + rise/pop animations from
   `WebAppFlow.dc.html`.
2. **One status vocabulary, used everywhere:**
   - `Live` badge (blue tint) = works in the demo today.
   - `Coming soon` badge (muted, dashed border) + dimmed/ghosted card = vision, not built.
3. **Copy rules (non-negotiable):** no jargon in user-facing copy, **no em dashes** (use commas,
   periods, or "then"), no metaphor. Resemblance is a **word** (strong / clear / partial), never a
   percentage. Sample length is **a minute or two**, never "20 seconds". Never say "how you think"
   (use "the way you talk"). Never mention Shadowing Plus.
4. **Unify the sample creators across every surface:** **Jay Shetty, Ali Abdaal, Cleo Abram** (match
   the App). Do not use Marques Brownlee or mixed sets.
5. **Do NOT add fabricated numbers** (see the Reject list at the bottom). Confidence is shown as a
   verified count of real evidence, never an invented percentage.

---

## Surface 1 — Landing page (fix to match the App, add the differentiation line + About link)

Keep the current structure (hero, how it works, sample results, closing CTA) but fix every stale
piece and add two things (the differentiation subline, and a link to the new About page).

**Header:** wordmark `Language Role Model`. Nav links: `How it works`, `About` (new, routes to
Surface 2), and primary button `Try it, no account` (not "Try it free").

**Hero — replace copy with exactly:**
- Badge: `Share a clip in your own language`
- H1: `Learn English from someone who already talks the way you do.`
- Differentiation subline (add this, it is the strongest line): `Most apps help you sound like a native speaker. We find the native speaker who already sounds like you.`
- Why-native line (add, under the subline): `The way you build a sentence, ask a question, or tell a story is the same in any language, and that is what we listen for.`
- Buttons: primary `Try it, no account`; secondary `See how it works`

**How it works (3 steps) — fix the false facts:**
- Section heading: `Three steps, about a minute or two`
- Step 01 `Speak your mind`: `Record a minute or two in your own language. No script, no account, no sign up.`
- Step 02 — retitle `We listen to how you talk`: `We look at how you build a sentence: how you open, add to it, and land your point.` (remove "how you think" / "structure a thought")
- Step 03 `Meet your matches`: keep, it is fine.

**What you get back (sample teaser) — remove the percentages:**
- Keep the 3 sample MatchCards but the three creators become **Jay Shetty, Ali Abdaal, Cleo Abram**,
  and each shows a **resemblance word** (`strong resemblance` / `clear resemblance` /
  `partial resemblance`), never `match-percent`. Keep one short "why" line each.
- Optionally show one mini evidence row ("You said ... then Creator does ...") to preview the
  evidence chain.

**New strip near the bottom — link to About:** a compact band: heading `There is a bigger idea here`,
one line `This is step one of a loop that keeps building a profile of how you talk.`, and a text link
`See the whole idea` routing to Surface 2 (About).

**Closing CTA (blue footer) — fix copy:**
- H2: `Someone already speaks English the way you do.` (was "the way you think")
- Subline: `Go find them. It takes a minute or two and no account.`
- Button `Record my clip` routes into the App.
- Keep the privacy line `Your clip is analyzed, never shared.`

---

## Surface 2 — About / Vision page (NEW)

A single scrollable page that carries what the landing cannot: the philosophy, the reasoning system
(agents exposed), and the **ideal-app mockups**. This is the one place we go technical and show
ambition. Everything future is clearly badged `Coming soon` / `Vision`.

**Header:** same as landing, with `About` marked active. A `Back to home` link.

**Section A — The idea (short).**
- Eyebrow: `THE IDEA`
- Heading: `You learn a language fastest by starting from how you already talk.`
- One paragraph: `Most learners are told to copy a native speaker, but copy who? A stranger who talks nothing like you feels fake and slow. So we listen to how you build your thoughts in your own language, before you say a word of English, and find the English speaker who talks the same way.`

**Section B — How the reasoning works (agents exposed).**
- Eyebrow: `HOW THE REASONING WORKS`
- Heading: `Not one guess. A short chain of steps, each doing one job.`
- A horizontal or vertical pipeline of 5 steps, each a small Card with a plain-language description
  **and a small monospace `Agent` tag** (this is where we make the agent system visible):
  1. `Transcript Agent` — `Writes down what you said and splits it into sentences.`
  2. `Thinking Style Agent` — `Reads how you open a point, connect ideas, and land it.`
  3. `Role Model Matching Agent` — `Finds the English speakers whose way of talking fits yours.`
  4. `Evidence Agent` — `Pulls the exact lines where you and a creator do the same thing.`
  5. `Confidence Judge` — highlighted as the hero (blue border, like the App's Confidence card):
     `Reads every reason back against your own words, and drops anything it cannot find there.`
- Pull-quote block under the pipeline (the positioning sentence, verbatim):
  `We are not matching people by topic or vocabulary. We build a reasoning based language profile, verify every behavioral claim against your own transcript, and only then search for creators whose communication patterns truly align.`
  (Note: em dashes removed from the original; keep it exactly as written here.)

**Section C — In the demo today vs where it is going.**
- A simple two-column split: `In the demo today` (Live badges: record, the agent pipeline, evidence
  chains, the Confidence Judge, three matches) vs `Where it is going` (Coming soon badges: the items
  mocked up in Section D).

**Section D — The ideal app (MOCKUPS, all badged `Coming soon` / `Vision`).**
This is the part Sumin most wants: real, richer mockups (not just one-liners), dimmed and dashed to
read clearly as vision.

1. **Personal Language Memory** (fuller than the App's teaser).
   - Heading: `Personal Language Memory` + `Coming soon` badge.
   - Line: `With your permission we save a profile of how you talk, never your audio, and show what grew between recordings.`
   - Mockup: a profile panel with a Day 1 vs Day 14 comparison (reuse the App's Day1/Day14 idea but
     larger), showing plain changes: `Sentence length: short then a little longer`,
     `Questions you ask: rarely then more often`, `Your own opinions: sometimes then clearly`.
     Show a small `opt-in` toggle in the mock (off by default) with the label
     `Save my talk profile (you can delete it anytime)`.
2. **Your Language Twin** (the concept made visible).
   - Heading: `Your Language Twin` + `Coming soon` badge.
   - Line: `Every session adds to a living picture of how you talk, so your matches and practice get sharper over time.`
   - Mockup: a single "twin" profile card — a name-less avatar, a few qualitative trait rows
     (`story driven`, `example first`, `question led`, `reflective`) shown as **simple filled bars
     or word labels, NOT numeric scores**, each with a tiny `seen in your clips` note. No "9/10",
     no "164 behaviors".
3. **The learning loop.**
   - Heading: `Finding your match is step one of a loop.` + `Coming soon` badge.
   - Mockup: a loop diagram `Understand you -> Find your match -> Practice with them -> See what grew -> a fresh match` (curved back to the start).
4. **The creator discovery network.** (The role models are real English vloggers, a growing pool.
   The two-sided story is discovery for creators, NOT learners becoming role models.)
   - Heading: `A new way for real creators to be found.` + `Coming soon` badge.
   - Mockup: a two-sided diagram `Learners -> matched by how they talk -> Creators (vloggers)`, with
     one small creator node getting discovered. No "learner becomes a creator" loop.
   - One line on why it matters: `Small creators get found by learners who already talk like them, and every new learner makes the matches better.`

**Section E — Close.** A `Try the demo` button routing to the App, and the legal line
`Not affiliated with or endorsed by any creator.` plus a `Request removal` mailto.

---

## Surface 3 — App (`WebAppFlow.dc.html`) — light additions only

Keep everything. Add four small technical-credibility touches (all factual, no invented numbers):

1. **Processing steps get agent tags.** Next to each existing plain step, add the small monospace
   `Agent` tag matching Section B: `Transcript Agent`, `Thinking Style Agent`,
   `Role Model Matching Agent`, `Evidence Agent`. The existing Confidence check card is the
   `Confidence Judge`. Keep the plain descriptions; the tag sits beside them.
2. **Processing final beat.** After the Confidence check completes, add one short beat before Results:
   `Building your Language Twin...` with a brief hold, then transition to Results.
3. **Results cards get a verified evidence chip** (factual, from the Judge): a small chip reading
   `Evidence verified, 3 of 3 confirmed` (use the real count per card). Do NOT add a percentage.
4. **Memory vision card** on Results is renamed/labeled **`Personal Language Memory`** (keep the
   `Coming soon` badge and the Day1/Day14 mock).

---

## Confirmed copy block (use verbatim, do not regenerate)

- Landing H1: `Learn English from someone who already talks the way you do.`
- Landing differentiation: `Most apps help you sound like a native speaker. We find the native speaker who already sounds like you.`
- Why-native: `The way you build a sentence, ask a question, or tell a story is the same in any language, and that is what we listen for.`
- App Upload helper: `About a minute or two of natural talking works best. Speak in your own language, the way you would with a friend.`
- Resemblance words: `strong resemblance` / `clear resemblance` / `partial resemblance`
- Verified chip: `Evidence verified, 3 of 3 confirmed`
- Twin beat: `Building your Language Twin...`
- Privacy: `Audio deleted. Nothing you said was stored.`
- Creator teaser: `Do you make videos in English? Learners who talk like you are looking for someone to copy. Soon you will be able to opt in and get found. Coming soon.`
- Legal: `Not affiliated with or endorsed by any creator.` / `Request removal`

## Reject list (do NOT add any of these)

- Any percentage match score (`94%`, `91% confidence`, etc.). Resemblance is a word.
- `9/10` style trait scores or `Generated from 164 language behaviors`. Fabricated precision reads as
  fake and breaks the honest-evidence story. Use qualitative traits tied to real clips instead.
- `20 seconds` (it is a minute or two).
- `how you think` / `structures thoughts` (it is "the way you talk").
- Em dashes anywhere in user-facing copy.
- Any mention of Shadowing Plus.
- A new color system or new fonts. Reuse the existing tokens only.

## Output

Extend the existing `.dc.html` system. Deliver: the fixed **Landing**, the new **About/Vision** page,
and the updated **App**. Label each screen. Apply the one status vocabulary consistently, and mark
each vision element `Coming soon`.
