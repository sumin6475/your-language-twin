# WebAppFlow — Content Fix Request (surgical, keep everything else)

*2026-07-20. Paste into Claude Design (the studio project). WebAppFlow is already in good shape
(fidelity, animations, evidence chains, resemblance words, step trace). This is a **surgical content
fix** of two outdated items. Do not restructure or restyle anything else.*

---

## Keep everything as-is except the two fixes below

Leave the Upload, Processing (agent steps + Confidence check), Results (three cards, evidence chains,
resemblance words, "How we got here" trace, privacy line), the "For creators" teaser, and the Empty
state exactly as they are. Only change these two things.

## Fix 1 — "same" to "similar" (Upload why-native line)

- Current: `The way you build a sentence, ask a question, or tell a story is the same in any language, and that is what we listen for.`
- Change to: `The way you build a sentence, ask a question, or tell a story is similar in any language, and that is what we listen for.`

(Reason: cultures express differently, so "same" over-claims. "similar" is used everywhere else.)

## Fix 2 — Creator network vision card: use the discovery framing, not "learners become role models"

In the Results "Where this goes next" section, the card currently titled **"As learners grow, they
become role models too."** shows the wrong concept (a learner graduating into a role model). Replace
it with the creator-discovery framing (the role models are real vloggers; the product is a discovery
channel for them).

- Heading: `A new way for real creators to be found.`
- Body: `The role models are real English vloggers, and that pool keeps growing. When a learner matches a creator, that creator gets found by exactly the person who wants to learn from them. For a small vlogger, that is a new way to be discovered, not through ads, but through the way they talk.`
- Replace the chip cycle `A learner -> Finds a match -> Practices and improves -> Opts in as a creator -> a new learner finds them` with a simple discovery flow: `Learners -> matched by how they talk -> Creators (vloggers) get found`. Remove any "opts in as a creator" or "becomes a role model" step.
- Keep the `Coming soon` badge and the dashed card style.

*(Note: the separate "For creators" teaser lower on the page is already correct, keep it. Fixing this
card removes the contradiction.)*

## Copy rules (unchanged)

Plain English, no jargon, no em dashes, resemblance stays a word, keep "similar" (never "same" for
the cross-language claim), never mention Shadowing Plus.

## Output

Return the updated WebAppFlow with only those two changes applied; everything else untouched. Claude
Code will then build the real Next.js from it, preserving the existing app routes and the real /match
data binding.
