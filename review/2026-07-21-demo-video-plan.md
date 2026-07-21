# Demo Video Plan — Your Ideal Role Model (v2, judge-aligned)

*Written 2026-07-21. Under 3 min, public YouTube. Format: your voice VO + clean screen recording (face optional, music optional). Feel: short product pitch + real app demo, NOT a tutorial and NOT slideware.*

**Judge guidance this version follows:**
- **70–80% of the video is the real app working.** Title/slide cards ≤ ~25 seconds total.
- Show **one complete, error-free user journey**, end to end — not a feature tour.
- Voice must explain **how Codex and GPT-5.6 were used.**
- GPT-5.6 = the **core AI**, producing structured outputs the UI uses — not a chatbot.
- Codex = show **real sessions/diffs** and **one hard technical decision** solved with it, not "it wrote code."
- Prove the four judging axes: technical implementation, complete product experience, real impact, original idea.

## Ground truth (from the seeded demo cache — all real, safe to show)
- 3 matches: **Cinema Therapy**, **Jay Shetty**, **Leila Hormozi** — resemblance word **"clear"** for each (never a percentage).
- Evidence chain to feature on card 1: **You said** *"So I brainstormed it and collected ideas every day"* → **Creator does** *"clear step-by-step structure"* → **Match**.
- **Tiebreaker actually fired** on this clip; **Confidence Judge ran**; full step trace completes; **audio deleted: true**.
- Our app renders the evidence chain natively, so the "make the reasoning visible" moment is the real UI — you barely need overlays.

---

## Beat sheet (~2:45, app-dominant)

| # | Time | Screen | VO (short, easy English) | Note |
|---|------|--------|--------------------------|------|
| 1. Problem | 0:00–0:12 | One title card *or* the app idle | "I'm learning English. Copying a perfect native voice never sounded like me. So I asked: who already speaks English the way I do?" | Only slide allowed. Keep ≤ 12s |
| 2. Solution | 0:12–0:24 | App home screen | "Your Ideal Role Model records how you talk in your own language, and finds real English creators who talk the same way." | App is on screen from here on |
| 3. **Real app demo — the spine** | 0:24–1:45 (81s) | Full run, no hidden cuts: upload → processing → results | "Here's the whole thing, start to finish. This is two minutes of me talking in Korean about a project idea. I upload it. It translates my speech, reads *how* I talk, and matches me. Here are my three creators. And each match shows the proof: this is what I said, this is what the creator does, this is why they match. It's a word, not a fake percentage — *clear*. And my raw audio is already deleted." | This is 70%+ of the video. Let the real UI carry it. Optional: one light highlight on card 1's chain |
| 4. GPT-5.6 = the core reasoning | 1:45–2:12 (27s) | **Stay on the results screen**; small structure line appears | "This isn't a chatbot. GPT-5.6 runs the reasoning in three separate steps — one reads my style, one writes the evidence, one checks it — and the app renders those structured outputs. When two creators nearly tie, a cheaper model breaks the tie, which is exactly what happened here." | On-screen line: **You said → your style → creator match → checked evidence**. App stays visible |
| 5. Codex = how it was built | 2:12–2:38 (26s) | **Real Codex sessions + a diff** on screen | "I built the whole backend in Codex. The hardest moment: my matches first collapsed — every creator looked the same. With Codex I diagnosed it and chose to re-center the data and add that gated tiebreaker, instead of faking the numbers. Codex took it from a broken prototype to a complete, runnable system." | Show 2–3 real Codex threads / the diff / the 0.997 → 0.95 result. This is real "working evidence" too |
| 6. Impact + close | 2:38–2:52 | Back to results / end card | "Every learner gets a role model who already talks like them — with proof they can check. That's Your Ideal Role Model." | End card: name + one line |

Pure slides in this cut: only beat 1 (≤12s) plus the end card. Everything else is the real app or real Codex on screen.

---

## Why this wins on the four axes
- **Technical implementation:** the multi-step GPT-5.6 reasoning + the gated tiebreaker + the honest centering fix, shown on real screens (beats 4–5).
- **Complete product experience:** one unbroken upload → result journey (beat 3).
- **Real impact:** a clear learner problem and outcome (beats 1, 6).
- **Original idea:** the reversed premise, stated once and shown, not explained to death (beats 1–3).

## Production notes (today)
1. **Record the run off the sample file** (cache hit, no keys, identical every time) — one clean take of upload → processing → results is your spine footage.
2. **Record VO separately** from the VO column, lay it over the capture.
3. **Screen-record 2–3 real Codex threads and one diff** now (e.g. the agent-architecture session, the corpus session, a diff view) for beat 5. This is required evidence, so capture it while you have it open.
4. **Keep overlays minimal** — one structure line in beat 4, maybe one highlight in beat 3. The app already shows the reasoning; do not bury it.
5. **Land around 2:45**, safely under 3:00.

## Shot checklist (capture once, clean)
- [ ] Beat 1 title card (or app idle)
- [ ] App home
- [ ] Upload screen with `samples/kor_3min.m4a` selected
- [ ] Processing screen (agent steps animating)
- [ ] Results: all three cards
- [ ] Results close-up: card 1 evidence chain + the word "clear" + "audio deleted"
- [ ] Results: the two near-tied cards / step trace (tiebreaker beat)
- [ ] **Codex: 2–3 real threads + one diff** (for beat 5)
- [ ] End card
