# Landing Page — Reformat Request (match the About page's fidelity + fix outdated copy)

*2026-07-20. Paste into Claude Design (the studio project that produced the About page). Goal: bring
the Landing up to the About page's polish (aurora background, scroll-reveal animations, richer
layout, evidence preview) AND fix the outdated copy still on it. After this, Claude Code builds the
real Next.js files. Reuse the same design system, tokens, aurora, and animations the About page uses.*

---

## Why this change

The current Landing is behind the About page in two ways: (1) the copy is outdated (old headline,
"20 seconds", percentage scores, "how you think"), and (2) the visual fidelity is flat (no aurora,
no scroll-reveal, no evidence preview). Make it match the About page's level and correctness.

## Global rules (same as About)

- Reuse the existing design system, tokens, the **aurora background**, and the `lrm-rise` / `lrm-pop`
  animations. No new colors or fonts.
- Status vocabulary: `Live` (blue) vs `Coming soon` (dashed).
- Copy rules: plain English, no jargon, **no em dashes**, resemblance is a **word** (never a %),
  keep **"similar"** (never "same"), never mention Shadowing Plus.
- Sample creators consistent with the app: **Jay Shetty, Ali Abdaal, Cleo Abram**.

## Fix these outdated pieces (content)

| Location | Current (wrong) | Change to |
|----------|-----------------|-----------|
| Header button | `Try it free` | `Try it, no account` |
| H1 | `Find the English creator who structures thoughts like you.` | `Learn English from someone who already talks the way you do.` |
| Hero subhead | `Record 20 seconds in your own language...` | the differentiation line + why-native line (below) |
| How-it-works heading | `Three steps, about a minute` | `Three steps, about a minute or two` |
| Step 01 | `Record 20 seconds in your native language...` | `Record a minute or two in your own language. No script, no account, no sign up.` |
| Step 02 title / body | `We map how you think` / `how you structure a thought` | `We listen to how you talk` / `We look at how you build a sentence: how you open, add to it, and land your point.` |
| Sample cards | `match-percent 94 / 91 / 88` | resemblance words `strong resemblance` / `clear resemblance` / `partial resemblance` |
| Sample creators | Cleo, Ali, Marques Brownlee | Jay Shetty, Ali Abdaal, Cleo Abram |
| Footer H2 | `Someone already speaks English the way you think.` | `Someone already speaks English the way you do.` |
| Footer subline | `...about a minute and no account.` | `...a minute or two and no account.` |

## Lift the fidelity to About level (structure + motion)

Rebuild the Landing as these beats, on the aurora background, with `lrm-rise` scroll-reveal on each
section (staggered like the About page):

**1. Header.** Wordmark `Language Role Model` + nav: `How it works` (to `#how-it-works`), `About`
(to the About page), and primary button `Try it, no account`. Sticky with a soft backdrop blur, same
as the About header.

**2. Hero (aurora, big type, rise-in).**
- Badge: `Share a clip in your own language`
- H1 (largest type): `Learn English from someone who already talks the way you do.`
- Differentiation subhead (the strongest line, give it weight): `Most apps help you sound like a native speaker. We find the native speaker who already sounds like you.`
- Why-native line (muted, under it): `The way you build a sentence, ask a question, or tell a story is similar in any language, and that is what we listen for.`
- Two buttons: primary `Try it, no account` (routes to the app), secondary `See how it works`
  (scrolls to how-it-works).
- Hero elements rise in with `lrm-rise`.

**3. How it works (3 steps, staggered reveal).**
- Heading: `Three steps, about a minute or two`
- Three numbered cards (`lrm-card`), each rising in with a small stagger. Use the corrected step
  copy from the table above. Consider a subtle connector or number treatment so it reads as a
  sequence, not three loose boxes.

**4. What you get back (evidence preview, replaces the percentage cards).**
- Eyebrow `What you get back` + heading `Not just names. The reason each one fits.`
- Three creator cards (Jay Shetty, Ali Abdaal, Cleo Abram), each with: name, role, a **resemblance
  word** badge (strong / clear / partial), a one-line why, and **one mini evidence row** previewing
  the chain: `You said "..." then <creator> does ...`. This mirrors the real results and previews the
  credibility. No percentages.

**5. The bigger idea strip (link to About).**
- A compact band (soft tint): eyebrow `The bigger idea`, line `This is step one of a loop that keeps building a profile of how you talk.`, and a text link `See the whole idea` routing to the About page.

**6. Closing CTA (blue footer).**
- H2: `Someone already speaks English the way you do.`
- Subline: `Go find them. It takes a minute or two and no account.`
- Button `Record my clip` (routes to the app).
- Keep the bottom row: `Language Role Model` + `Your clip is analyzed, never shared.`

## Consistency with About (so the two pages feel like one product)

- Same aurora, same `lrm-rise` / `lrm-pop` motion, same card and badge styling, same type scale and
  generous spacing.
- Same header and nav so moving between Landing and About feels seamless.

## Do not

- No em dashes, no jargon, no percentage scores, no "how you think", no Shadowing Plus mention.
- Do not invent new claims or features; this is the marketing surface for what the demo does.
- Do not introduce a new color system or fonts; reuse the tokens only.

## Output

Deliver the updated Landing in the same `.dc.html` design-system format as the About page, matching
its fidelity and motion, with all the outdated copy fixed. Claude Code will then build the real
Next.js files from it (preserving the existing app routes and the real /match data binding).
