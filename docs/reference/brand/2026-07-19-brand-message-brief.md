# Brand & Message Brief — Your Ideal Role Model

*2026-07-19. Codex-ready. This revises the copy in `docs/design/ui-spec.md` (Copy sheet). Where
this brief and the old copy sheet disagree, this brief wins. All user-facing copy here is
em-dash-free and uses plain, everyday words a normal learner understands on first read.*

---

## 1. The one rule for all copy

Marketing and product copy use **general, intuitive words**. If a normal learner would need to
look a word up, it does not ship. Banned in user-facing copy:

| Don't say | Say instead |
|-----------|-------------|
| shadow / shadowing | copy, repeat after, practice with |
| structures thoughts / rhetorical style | the way you talk, how you say things |
| thinks like you | talks the way you do |
| hedging / directness | softens what they say ("kind of", "I guess") / gets straight to the point |
| style match / style vector | speaking-style match |

Internal specs (like the "why" panel spec) may keep precise terms. The **screen** may not.

## 2. Positioning

**The promise (say the smaller, true thing, let the demo over-deliver):**
we match on *how you talk*, not *how you think*. "How you think" over-claims and reads like a
personality quiz. "How you talk" is true, checkable, and still compelling.

- **Headline:** Learn English from someone who already talks the way you do.
- **Subhead (does the competitor work in one breath):** Most apps help you sound like a native
  speaker. We find the native speaker who already sounds like you.

**Category we attack:** accent-scoring apps (ELSA, BoldVoice) and celebrity-soundalike novelty.
We are neither. We do not grade your accent and we are not a "which star do you sound like" toy.

**Dropped:** "Stop shadowing strangers." It fights a problem the user does not feel yet, the match
result is still a person they have not met, and "shadowing" is jargon. Do not use it.

## 3. Kill the one confusion first

The single most confusing thing about this product, and the very first thing the user does, is:

> "I am learning English. Why are you asking me to record my **native** language?"

If screen 1 does not answer this instantly, the demo dies before the magic. Answer it in one plain
line, right under the subhead:

> **Speak in your own language. The way you build a sentence, ask a question, or tell a story is
> the same in any language, and that is what we listen for.**

This turns the weird step into the clever step. It is the highest-leverage line on the landing page.

## 4. Demo narrative spine (use this order in the video and on the page)

1. **Problem (everyone gets the same bad advice):** learners are told "watch native speakers and
   copy them." But copy *who*? A random famous person who talks nothing like you feels fake and
   slow to imitate.
2. **Insight (the clever inversion):** the way you build sentences shows up in *any* language you
   speak. So we listen to you in your own language, before you say a word of English, and find the
   English speaker who talks the same way.
3. **Payoff:** three real English speakers who already sound like you, a plain reason for each, and
   a link to go practice with their real videos today.
4. **Potential (why this is bigger than a demo):** this is step one. Next comes practice-and-compare
   with your match, and a second side where English speakers opt in to be found. A small tool now,
   a two-sided learning network later.

## 5. Revised copy set (replace the ui-spec Copy sheet with these)

### Landing / Upload (route `/`)
- Eyebrow: `YOUR IDEAL ROLE MODEL`
- H1: `Learn English from someone who already talks the way you do.`
- Subhead: `Most apps help you sound like a native speaker. We find the native speaker who already sounds like you.`
- Why-native line (new, high-leverage): `Speak in your own language. The way you build a sentence, ask a question, or tell a story is the same in any language, and that is what we listen for.`
- Upload label: `Record or upload a short clip of yourself talking.`
- Upload helper: `About two minutes of natural talking works best. Speak in your own language, the way you would with a friend.`
- Consent: `I agree to have this clip processed once to find my matches. My audio is deleted right after.`
- Age line: `You confirm that you are 18 or older.`
- Button (idle): `Find my matches`
- Button (loading): `Finding your matches...`
- Loading reassurance: `This takes about 30 seconds.`
- Validation error: `Add a clip and check the box before continuing.`

### Processing (in-place on screen 1)
- Keep it calm and honest. Show, in sequence, what is actually happening, in plain words:
  `Listening to how you talk...` then `Finding English speakers who talk the same way...`
- Privacy reassurance surfaces here too: `Your audio is being deleted now. We only keep the match.`
- No fake percentages.

### Results (route `/results`)
- Eyebrow: `YOUR THREE MATCHES`
- H1: `These three English speakers talk the way you do.`
- Framing line (muted, honest): `Think of them as people you will find easy to copy, not a score on your voice.`
- Privacy line: `Audio deleted. Nothing you said was stored.`
- Journey teaser (new, the "step 1" signal) eyebrow: `WHAT COMES NEXT`
- Journey teaser body: `This is step one. Soon you will be able to practice a line with your match and hear how close you got. Coming soon.`
- Creator teaser eyebrow: `FOR ENGLISH SPEAKERS, COMING SOON`
- Creator teaser body: `Do you make videos in English? Learners who talk like you are looking for someone to copy. Soon you will be able to opt in and get found. Coming soon.`
- Footer disclaimer: `Not affiliated with or endorsed by any creator.`
- Takedown link: `Request removal`
- Empty H1: `Your matches will show up here.`
- Empty body: `Add a clip first, then we will introduce you to three English speakers.`
- Empty button: `Add a clip`

## 6. The three "this is a real system" signals (weight them 80/10/10)

1. **Evidence signal (spend most of your polish here):** the match reason must show 2 to 3 concrete,
   checkable things you and the creator both do, not vague praise. Full detail in
   `2026-07-19-why-panel-spec.md`. This one screen is worth more than the other two combined, because
   it is what makes "it knows how I talk" believable instead of gimmicky.
2. **Journey signal:** the `WHAT COMES NEXT` teaser frames today's result as step one of a bigger loop.
3. **Network signal:** the `FOR ENGLISH SPEAKERS, COMING SOON` teaser hints at a two-sided network.

## 7. What changed vs the current build (so Codex knows this is a revision)

- Headline, subhead, and results headline rewritten (plain words, no "structures thoughts").
- Added the **why-native line** on landing (the confusion-killer). New string.
- Added the **`WHAT COMES NEXT`** journey teaser on results. New section.
- Renamed the creator teaser to **`FOR ENGLISH SPEAKERS`** and removed the word "shadow".
- "Find my creators" to "Find my matches"; "Visit their channel" stays.
- No backend changes required for any of section 5. Section 6.1 needs the small `/match` change in
  the why-panel spec.
