# Landing Page Review — `Landing.dc.html`

*2026-07-19. Codex-ready. Review of the uploaded landing design against the brand brief, the
why-panel spec, and the product facts in `docs/PRD.md` + `docs/design/ui-spec.md`. Use alongside
the other three branding docs in this folder. Plain-word rule applies: no jargon in any user-facing
copy, no em dashes.*

---

## One-line verdict

Strong structure and a smart evidence preview, but it (a) states two things that are not true of
the product (20-second clip, 94% score), (b) revives the "how you think" over-claim we removed, and
(c) is missing the "why native language?" answer and the competitor difference. Fix a to c and it
is demo-ready.

## What is good (keep it)

- **Structure:** hero, "how it works", sample results, closing CTA. A real marketing page, a big
  step up from the bare upload screen.
- **Evidence preview is the best decision on the page.** The "What you get back" section shows sample
  MatchCards *with the reason*, so the credibility engine is previewed on the landing. The sample
  reason lines are genuinely strong and concrete (for example, "You both open with the question
  everyone is quietly asking, then answer it one honest step at a time"). This matches the why-panel
  spec exactly.
- **Real names and roles** (Cleo Abram, Ali Abdaal, Marques Brownlee), no placeholders.
- **Trust signals** present: "no account", "Your clip is analyzed, never shared".
- Blue used as accent only (footer). No em dashes. On-brand with the design system.

## Must fix (these conflict with product facts, not just copy)

1. **"20 seconds" is wrong.** Short clips give unstable matches; the product needs about two minutes
   (soft floor 90 seconds), per the PRD. Change every "20 seconds" and "about a minute" to
   **"a minute or two"**. This is an accuracy issue, not a wording preference.
   - Hero subhead, step 01 card, footer subline.
2. **"94% / 91% / 88%" match scores.** The build rule is a resemblance *word*, not a number, because
   style similarity is a fit signal, not a precise measurement. A percent reads like a soulmate
   accuracy score, the exact "horoscope" risk to avoid. Use **strong resemblance / clear resemblance
   / partial resemblance** on the sample cards.
   - *Decision needed:* if you deliberately want a playful number, it must be framed (for example
     "your style: 94%"), never a bare percent. Pick one and apply it everywhere.

## Should fix (from the brand brief)

3. **"how you think / structures thoughts / the way you think" is back.** It is in the H1, step 02,
   and the footer. This is the over-claim and jargon we removed. Change all to **"the way you talk"**.
   - H1 → `Learn English from someone who already talks the way you do.`
   - Step 02 title → `We listen to how you talk`; body → `We listen to how you build a sentence: how you open, add to it, and land your point.`
   - Footer H2 → `Someone already speaks English the way you do.`
4. **The "why native language?" question is not answered.** The page says "in your native language"
   but never says *why that helps you learn English*, which is the single most confusing thing. Add
   the brief's why-native line near the hero or as step 02 support:
   `The way you build a sentence, ask a question, or tell a story is the same in any language, and that is what we listen for.`
5. **No competitor difference line.** Nothing says why this is not an accent app. Add the contrast
   subhead under the H1: `Most apps help you sound like a native speaker. We find the native speaker who already sounds like you.`

## Nice to have (the "shows development potential" goal)

6. **Add one "what comes next" line** so the page hints at a bigger system, not just today's tool.
   For example a short closing note: `This is step one. Practice-and-compare with your match is coming.`
   Optionally a one-line two-sided hint: `Make videos in English? Soon learners who talk like you can find you.`
7. **Hero has no visual.** It is competent but generic. One simple graphic of the core idea (your
   own-language clip on the left, the matched English speaker on the right, a link between them)
   would make it memorable instead of standard-SaaS.
8. **Vary the three sample creators.** All three are calm tech/productivity explainers, which reads
   as "it always matches tech YouTubers". Swap one for a different style (a storyteller, a blunt
   straight-talker) to show range.

## Copy replacements (drop-in)

| Location | Current | Change to |
|----------|---------|-----------|
| H1 | Find the English creator who structures thoughts like you. | Learn English from someone who already talks the way you do. |
| Hero subhead | Record 20 seconds in your own language... | Record a minute or two in your own language. Then meet three English speakers who already talk the way you do. |
| New line under hero | (none) | Most apps help you sound like a native speaker. We find the native speaker who already sounds like you. |
| Step 01 body | Record 20 seconds in your native language... | Record a minute or two in your own language. No script, no account. |
| Step 02 title / body | We map how you think / how you structure a thought | We listen to how you talk / how you build a sentence: how you open, add to it, and land your point. |
| Sample cards | match-percent 94 / 91 / 88 | strong resemblance / clear resemblance / partial resemblance |
| Footer H2 | Someone already speaks English the way you think. | Someone already speaks English the way you do. |
| Footer subline | ...about a minute and no account. | ...about a minute or two and no account. |

## Priority order for tomorrow

1 and 2 (product-truth) → 3, 4, 5 (positioning) → 6, 7, 8 if time allows.
