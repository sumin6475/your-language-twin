# Demo Video — Final Cut (storyboard + script)

*Written 2026-07-21. This is the definitive cut. English lines are verbatim — say them exactly. Korean text is direction only.*

---

## Primer — read this first (full context)

**Situation.** This is the demo video for the **OpenAI Build Week** hackathon submission. Deadline: **today, 2026-07-21, 5:00pm PDT.** Requirements: under 3 minutes, public YouTube, shows the product actually working, and the voiceover explains how **Codex** and **GPT-5.6** were used.

**What the product is (one sentence).**
> Not an app that teaches you English — a system that reads *how you organize your thoughts* in your own language and finds the real English creator who already thinks the way you do, so you learn by expressing the thoughts you already have.

**The reframe that runs the whole video.** This is not "another AI English app." It is a **new mental model for language learning**: the hard part isn't vocabulary or grammar, it's **thought transfer** — expressing the thoughts you already have, in another language. The video should feel like **proving one idea**, not touring an app.

**Judging criteria (design the video to prove all four):**
- **Technical implementation** — GPT-5.6 and Codex used meaningfully in the core experience.
- **UX / product** — a real, working product with a clean, complete journey.
- **Idea** — an original, memorable concept.
- **Potential impact** — a clear problem solved, and a **scalable vision** (the creator/learning network).

**The three principles to hold:**
1. Say the word **"English" as late as possible.** The subject is thought transfer.
2. **Observation, not theory.** First person, no "we propose a theory."
3. **Show, don't explain.** 70%+ is the real app running as one clean journey. Open and close are the same idea, flipped.

**Framing guardrail for GPT-5.6 vs Codex.** In the video: **GPT-5.6 = the product's core reasoning engine** (what the user interacts with); **Codex = the engineering teammate that built and iterated the system.** Do not enumerate other development-time tooling — that is a separate story and not what judges score.

---

## The storyboard (~2:56)

### 1. Hook (0:00–0:12) — black screen, text only, one line at a time
> Everyone tells you to learn from native speakers.
> *(0.8s)* We think that's wrong.
> *(0.5s)* Learn from the native speaker who already thinks like you.

### 2. Cognitive-compression visual (0:12–0:22) — black screen, animated, no voice
Center-aligned, stacked vertically. For each pair: the **pre-arrow word appears first**, then a beat later the **arrow + post word** appears.
> `Example`  →  `→ Lesson`
> `Question`  →  `→ Answer`
> `Story`  →  `→ Reflection`

After all three are stacked, subtitle fades in:
> *"Language changes. This doesn't."*

### 3. Cut to app + philosophy (0:22–0:36) — VO over the upload screen
> You don't think in English. You already know how you think. The hard part is expressing those same thoughts in another language.

*(Optional reinforcement, if time allows — the personal observation:)*
> I wasn't struggling because I lacked English. I was struggling because I couldn't express the thoughts I naturally have every day.

### 4. Demo — the spine (0:36–1:20) — real app recording, minimal words
Screen: upload → Processing (agent flow animation) → Result → Evidence *(use the footage you already recorded).*
> We don't analyze your vocabulary. → We analyze how you build ideas. → Then we verify every claim. → Only then → we look for the best role model.

### 5. Signature scene (1:20–1:38) — newly made, abstract (no specific person)
- First, your **silent speaking video**, full frame.
- It animates into a **left/right split**: left = your silent video (mouth moving), right = an **abstract representation of a YouTube creator speaking** (YouTube logo / silhouette — not a real person's video).
- Slight dim, then the line appears, split by sentence:
> They don't use the same **words**.  *(highlight "words", then fade)*
> They use the same **way of thinking**.  *(highlight "thinking")*

### 6. Why GPT-5.6 (1:38–2:00) — centered on a GPT-5.6 icon
> GPT-5.6 doesn't analyze your English. It reasons about how you organize ideas.

Then, small: *builds your communication profile → verifies every observation → finds creators*

### 7. Codex (2:00–2:15) — real artifacts (PR · test · architecture · prompt · agent) shown fast
> Codex helped us build and iterate on the system.

*(Fuller line lives in the README: "We used Codex as an engineering teammate to iterate on the reasoning pipeline, refactor the backend, and rapidly incorporate design feedback.")*

### 8. Future / network vision (2:15–2:42) — camera zooms out to the Landing "Future," animated
> Instead of searching through millions of videos, you discover the one person who already explains the world the way your mind understands it.
> *(0.5s)* And it runs both ways. Even a small creator can come here — to be discovered by the exact people who already think the way they explain the world.

Framing caption: *"Recognition, not recommendation."*
*(Visual: a Learner ↔ Role Model ↔ Practice ↔ Network loop coming alive.)*

### 9. Close (2:42–2:56) — end card + logo
> Today, we help you find someone who already thinks like you.
> *(0.5s)* Tomorrow, we might understand how you learn well enough to help you become someone else's role model.

---

## Notes & alternates
- **The two-sided network is intentional:** beat 8 is the **creator-discovery** side (small creators come to be found by minds that match how they explain things); beat 9 is the **learner-growth** side. Together they make it a system, not a recommender.
- **Alternate close (8C)** if you want to nail the creator side at the very end instead:
  > Today, you find someone who thinks like you. *(0.5s)* Tomorrow, the creators who think like you find you too.
- **Simpler 6+7 pair** (if timing is tight, swap beats 6–7 for this and let the README carry the detail):
  > Codex helped us build and iterate on the system. GPT-5.6 powers the reasoning engine that users interact with.
- **Timing is tight at ~2:56.** If over 3:00, trim the middle of beat 8 (keep the two lines above, drop extra loop narration) or shorten beat 4.

## Production reminders
- Face optional, music optional. Clean screen recording + natural VO is enough.
- Record VO separately, lay it over the captured app run.
- Record the app demo off the **sample file** (cache hit, no keys, identical every time).
- Screen-capture the real Codex artifacts now for beat 7 while they are open.
