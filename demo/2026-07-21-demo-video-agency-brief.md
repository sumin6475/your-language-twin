# Demo Video — Agency Production Brief

*Product: **Language Role Model** (working repo: `your-ideal-role-model`). Prepared 2026-07-21. This brief is the build spec for an external motion / editing team. It is derived from the internal final-cut storyboard and is self-contained — an editor should be able to build the full film from this document plus the four supplied assets.*

> **How to read this brief.** English lines inside quotation marks under **VO** are **verbatim** — record and place them exactly, do not paraphrase. Everything else is direction. Timecodes are targets; the hard rule is **total runtime under 3:00** (see §2).

---

## 1. What we are making (the one idea)

This is **not** "another AI English app" video. It proves **one idea**: the hard part of a new language is not vocabulary or grammar — it is **thought transfer**, expressing the thoughts you already have in another language. The product reads *how a person organizes their thinking* in their own language, and finds the real English creator who already thinks that way.

The film should feel like **proving one idea**, not touring an app. Three principles govern every cut:

1. **Say the word "English" as late as possible.** The subject is thought transfer, not English. (First spoken "English" is Beat 3.)
2. **Observation, not theory.** First person. Never "we propose a theory."
3. **Show, don't explain.** 70%+ of the runtime is the real app running as one clean, continuous journey. The open and the close are the same idea, flipped.

**One-sentence product definition (for the team's understanding — not on screen):**
> Not an app that teaches you English — a system that reads how you organize your thoughts in your own language and finds the real English creator who already thinks the way you do, so you learn by expressing the thoughts you already have.

---

## 2. Deliverable specification

| Field | Spec |
| :--- | :--- |
| **Runtime** | Target ~2:56. **Hard cap: under 3:00.** If over, trim per §9 (Trim order). |
| **Master resolution** | 1920×1080, 16:9, progressive. (Optional 2560×1440 master; 1080p is the required delivery.) |
| **Frame rate** | 30 fps (match the app screen-capture source; do not conform to 24 unless the whole film is regraded). |
| **Format** | H.264 MP4, ~16–24 Mbps, AAC audio −14 LUFS integrated (YouTube loudness). |
| **Captions** | Burned-in on-screen text as designed **plus** a separate `.srt` of the VO for accessibility. |
| **Destination** | Public YouTube (hackathon submission). |
| **Aspect variants** | 16:9 only for submission. (No vertical cut required.) |

---

## 3. The two visual worlds

The film alternates between two clearly separated looks. Keeping them distinct is what makes the app feel *real* and the ideas feel *authored*.

### World A — "Designed" (kinetic typography)
Used for: Beat 1 (Hook), Beat 2 (Cognitive compression), Beat 6 (Why GPT-5.6), Beat 7 title, Beat 9 (Close).

- **Background:** near-black `#0A0A0B` (not pure #000 — avoids banding on YouTube compression).
- **Type:** white `#FFFFFF` primary; dim label grey `#A1A1AA`.
- **One accent only:** the product blue — `#1E40AF` (deep) and `#3B82F6` (bright) for highlights, underlines, and the "hand-drawn" accent marks (see Apple decode, §5). No other colour enters World A.
- **Font:** **Clash Display**, weight 600, tight tracking (−0.02em) for all display lines. This is the app's real display face — using it here pre-loads the brand before the product appears.
- **Mood:** editorial, high-contrast, confident, a lot of negative space. One thought per screen.

### World B — "App demo" (light, atmospheric, floating panels)
Used for: Beat 3, Beat 4 (the spine), Beat 5 (signature), Beat 8 (network vision).

- **Background:** the app's own **aurora** — a soft animated blue gradient bloom (top-right radial) over white `#FFFFFF` / `#FAFAFB`. It already exists in the product (`.lrm-page::before`, `lrm-aurora` keyframe). Keep it; do **not** recolour to dark.
- **Screens as floating glass panels:** the real UI is presented as slightly tilted panels floating in shallow 3D with soft drop shadows (`0 12px 32px rgba(0,0,0,.10)`), gentle **parallax** and **rack-focus / depth-of-field**, and slow **push-ins** — the Lovio treatment (§5), applied to a *light* stage rather than a dark one.
- **Type:** **Clash Display** headings, **Inter** body — as built in the product.
- **Palette (product tokens, use exactly):**

| Token | Hex | Use |
| :--- | :--- | :--- |
| blue-deep | `#1E40AF` | primary accent, buttons, "Match", verified |
| blue-bright | `#3B82F6` | gradient partner, live pulse |
| blue-tint | `#EFF3FF` | badges, "Evidence verified" pill fill |
| ink | `#18181B` | primary text |
| ink-tertiary | `#71717A` | secondary/caption text |
| surface / bg | `#FFFFFF` / `#FAFAFB` | cards / stage |
| border | `#ECECF0` | card borders |
| avatar gradient | `135° #1E40AF → #3B82F6` | avatars, brand mark |

**The bridge between worlds:** blue is the only colour shared by both worlds. Every transition from A→B or B→A should hand off *on a blue element* (a highlighted word dissolving into a blue button, a blue pill becoming a blue underline). That single colour thread is what makes the two looks read as one film.

---

## 4. Motion & pacing principles (global)

Derived from the references in §5. These apply everywhere.

- **Rhythm follows the voice.** Cut on the VO's natural clause breaks. Text appears **as it is spoken**, not before. Silence beats (the plan's `(0.8s)`, `(0.5s)`) are real holds — do not fill them.
- **Two easing personalities.**
  - *Ideas (World A):* **ease-out** entrances, ~350–460ms, with a **slight spring/overshoot** on the key word — this is the "쫀득한" springy snap from Freshbooks. Springy, not bouncy-cartoon: overshoot ≤ 6%, one settle.
  - *Product (World B):* **smooth, weighted** ease-in-out, ~500–700ms, no overshoot. The product moves like glass — calm and expensive.
- **Entrance vocabulary:** rise+fade (`translateY 10px → 0`, opacity 0→1), pop-scale (`scale .6 → 1`) for status ticks, mask-wipe for underlines. These exist in the app as `lrm-rise`, `lrm-pop` — reuse the same curves so live-driven UI and added motion match.
- **Transitions:** hard **cut on the beat** for idea-to-idea (World A). **Match-cut** or **cross-dissolve through a blue element** for A↔B. Inside the app journey, prefer **camera moves** (push-in, pan, rack focus) over cuts, so the demo reads as one continuous session.
- **Never overwhelm.** Only one new idea on screen at a time. When a new line arrives, the previous line either fades or is de-emphasized to grey. This is the Apple "cut-and-connect" discipline (§5) — the antidote to text overload.

---

## 5. Reference decode — why each clip works, in editing terms

Each supplied reference is decoded into the specific technique to borrow and where to apply it. Files are in `demo/reference/`.

### 5.1 Apple — *Every product carbon neutral by 2030* — **#1 mood reference (World A)**
**What it does:** full-frame colour-block cards (off-white / brand-green / black) where **each card holds one short sentence fragment**, and cards **hard-cut on the beat**. A hand-drawn marker accent (a script word, an underline, a circular arrow) is layered over clean Helvetica; the logo is dropped **inline** to replace a word.
**Why it creates the mood:** the "overwhelming amount of text, but never overwhelming" effect comes from **fragmentation + one-thought-per-card + colour-flip cuts**. Your eye only ever reads 2–5 words, the colour flip re-sets attention each beat, and the hand-drawn mark adds a human, authored warmth against the clean type.
**Borrow:** the fragment-per-card cadence, the single hand-drawn accent per key word, inline-logo/word substitution. **Apply to:** Beats 1, 2, 6, 9. **Adapt:** replace Apple's green with our **blue `#3B82F6`**; our background stays near-black (World A) rather than flipping to colour blocks (we chose the calmer "black + blue" direction, not full colour-flip).

### 5.2 Lovio (Zelios) — *Best AI Product Video for SaaS* — **#1 demo reference (World B)**
**What it does:** app UI shown as **floating glass panels** in a shallow, cinematic 3D space — soft god-rays and bokeh, **depth-of-field** so one panel is sharp while others blur, slow **push-ins** and **parallax**, thin elegant display type with huge negative space ("an idea", "in any", "What will you create").
**Why it creates the mood:** presenting screens as **objects in space** (not flat recordings) plus **rack focus** makes software feel **premium and physical**. The DoF directs the eye to exactly one panel at a time, so a dense dashboard never overwhelms.
**Borrow:** screens-as-floating-panels, rack focus between panels, slow push-in, generous negative space, big thin title cards between product moments. **Apply to:** Beats 3, 4, 8. **Adapt:** we keep our **light aurora** stage instead of Lovio's dark one — same motion language, our colour world.

### 5.3 Freshbooks — *Tax Time* — **rhythm & "쫀득" springiness**
**What it does:** cream stage; navy/blue/yellow dots act as **motion characters** that scatter, cluster, and morph into shapes; text **swaps in place** (word replaces word) with a **springy overshoot**; punchy, quick beats.
**Why it creates the mood:** the springy easing + in-place word-swaps give a satisfying, "chewy" tactility; the dots carry energy through the gaps so momentum never drops.
**Borrow:** the **spring/overshoot easing curve** for key-word entrances (World A), and the **word-swap-in-place** technique. **Apply to:** Beat 2 (the `word → arrow → word` reveals) and any key-word emphasis. **Do NOT borrow** the multicolour palette or literal dot-characters — that belongs to Freshbooks, not us.

### 5.4 Freighty (Vidico) — *B2B Insurance Explainer* — **abstraction calibration**
**What it does:** turns sentences into **flat 2-colour vector scenes** — one clean metaphor per idea ("Increased Margin" = bar + 30% arrow; "Order Received" = phone with a check). Moderate abstraction: simplified, icon-driven, never photoreal.
**Why it creates the mood:** a **single legible metaphor per line** keeps abstract claims concrete without clutter.
**Borrow:** the *level* of abstraction as our ceiling — **if** any concept needs a visual beyond type, it should be this simple and this flat. **Apply to:** reference only. We chose **type-first** (no illustration) for World A, so treat Freighty as the guardrail for "how far to abstract," not a call to add illustration.

### 5.5 Seeklab & Membrain — **#2 demo references (supporting World B)**
- **Seeklab:** alternating light-blue / navy sections, big **thin** display type, floating **product-screenshot cards**, and an **orbit diagram** (app icons circling a search bar). *Borrow:* the orbit-diagram device for showing "many → one," and stacked floating result cards. *Apply to:* Beat 8 (network loop), Beat 4 (results stack).
- **Membrain:** dark premium stage, **gradient stat-rings** (81%, 67%), **avatar clusters** orbiting a stat, dashboards in **isometric tilt**. *Borrow:* avatar-cluster orbit and tilted-panel presentation. *Apply to:* Beat 8 (learner ↔ creator network) — recoloured to our light world.

### 5.6 CleanShot (`CleanShot 2026-07-21 at 14.01.50.mp4`) — **split-screen transition technique**
Not a mood reference — it is a **how-to** for the **split-screen transition** used in Beat 5: a full frame that splits into left/right halves with a clean vertical wipe, warm/cool colour separation on each side. **Apply to:** Beat 5 (your video | the creator side). Use its wipe timing and centre-line treatment.

---

## 6. Supplied assets & live-drivable UI

### 6.1 Footage in `demo/`
| Asset | Detail | Use |
| :--- | :--- | :--- |
| `app-real-record.mp4` | 2414×1440, ~99s, real screen capture of the full journey (landing → file picker → processing → results → evidence → coming-soon) | **Primary source for Beat 4.** This is the spine. Re-frame/crop to 1080p; drive camera moves on it. |
| `sumin-talking.mp4` | 3840×2160 HEVC, ~18s, the founder speaking to camera (silent-usable) | **Beat 5 left panel** (your silent speaking video). Also usable as an optional small inset in Beat 3. |
| `2026-07-21-demo-video-final-cut.md` | the internal storyboard/script | source of truth for VO — already reflected in §8. |

### 6.2 The app is its own design system — drive it live where possible
The real front-end (Next.js) can be run and captured at native resolution for crisper panels than upscaling the recording. Editors may request fresh captures of these **real components** (all already built, styled in the tokens of §3):

- **Landing hero** — `Learn English from someone who already talks the way you do.` (Clash Display 52px) with the animated aurora and rise-in reveals. *(Beats 3.)*
- **`ProcessingVisualizer`** — the agent chain, in order: **Transcript Agent → Thinking Style Agent → Role Model Matching Agent → Evidence Agent**, each a card with a spinner→check status, then the raised **Confidence Judge** card ("the step that keeps us honest") with a shield mark and a live pulse. Ends on **"Building your Language Twin…"**. *(Beat 4 — the heart of the technical story.)*
- **`MatchCard`** — the evidence card: avatar + name + resemblance badge, then the **"Why these two line up"** block laid out as **`You said` → (arrow) → `[creator] does` → `Match`** with an **"Evidence verified"** pill. The three real matches captured are **Cinema Therapy, Jay Shetty, Leila Hormozi**. *(Beat 4 climax, Beat 6 support.)*
- **`ComingSoonVision`** — three dashed "vision" cards (**Personal Language Memory** with a Day 1 → Day 14 growth table; **A practice loop**; **A new way for real creators to be found**) plus the animated trail-border **"For creators"** card. *(Beat 8.)*
- **Avatar (gradient monogram tile)** — the product's stand-in for a person; **this is the creator representation for Beat 5** (see §8, Beat 5).

> Capture note for the team: record the app off the **sample file** (deterministic — `kor_3min_demo.m4a`, cache-hit, no keys, identical every run) so re-captures match the existing footage frame-for-frame.

---

## 7. Storyboard at a glance

| # | Beat | TC | World | Core move |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Hook | 0:00–0:12 | A · black+blue | Three lines, one at a time. The reframe. |
| 2 | Cognitive compression | 0:12–0:22 | A · black+blue | `word → word` pairs; "Language changes. This doesn't." |
| 3 | Cut to app + philosophy | 0:22–0:36 | B · app | First app screen; the thought-transfer VO. |
| 4 | The demo spine | 0:36–1:20 | B · app | Upload → Processing (agents) → Result → Evidence. |
| 5 | Signature scene | 1:20–1:38 | B · app | Split screen: you \| the creator (app avatar + waveform). |
| 6 | Why GPT-5.6 | 1:38–2:00 | A→B | Reasoning engine, not an English grader. |
| 7 | Codex | 2:00–2:15 | A + artifacts | The engineering teammate that built it. |
| 8 | Network / future | 2:15–2:42 | B · app | Zoom out to the two-sided loop. |
| 9 | Close | 2:42–2:56 | A · black+blue | Today / Tomorrow. End card + logo. |

---

## 8. Shot-by-shot spec

> Legend — **VO** = record verbatim · **TXT** = on-screen text · **COMP** = composition · **MOVE** = animation/motion · **SRC** = source asset or live component · **OUT** = transition out · **SFX** = sound.

### Beat 1 — Hook · 0:00–0:12 · World A (black + blue)

- **VO:** "Everyone tells you to learn from native speakers." *(0.8s hold)* "We think that's wrong." *(0.5s hold)* "Learn from the native speaker who already thinks like you."
- **TXT (each line appears as spoken, one at a time, centre screen):**
  1. `Everyone tells you to learn from native speakers.`
  2. `We think that's wrong.`
  3. `Learn from the native speaker who already **thinks like you**.`
- **COMP:** near-black `#0A0A0B`. Clash Display 600, white, ~44–52px, one line centred, wide margins. Line 3 breaks so **"thinks like you"** sits on its own line.
- **MOVE:** each line **rise+fade in** (ease-out ~420ms). When the next line comes, the previous line **dims to grey `#A1A1AA`** and shifts up slightly (it stays visible, stacking) — so by line 3 the viewer sees the argument build. On "wrong," a quick **blue underline wipe** under *wrong*. On line 3, **"thinks like you"** is **blue `#3B82F6`** with a hand-drawn-style underline that draws on (Apple accent, recoloured).
- **SRC:** designed from scratch.
- **OUT:** hold 0.5s on the full stack, then **hard cut to black** on the last consonant.
- **SFX:** near silence; a single soft low sub-hit on line 1, a subtle rising tone into Beat 2. VO dry, intimate, close-mic.
- *Note:* no logo, no product yet. The word "English" does **not** appear.

### Beat 2 — Cognitive compression · 0:12–0:22 · World A · **no voice**

- **VO:** none. Music/rhythm carries it.
- **TXT (centre, stacked vertically; for each pair the left word appears first, then a beat later the arrow + right word):**
  - `Example` → `Lesson`
  - `Question` → `Answer`
  - `Story` → `Reflection`
  - then, after all three are stacked, subtitle fades in: `"Language changes. This doesn't."`
- **COMP:** black. Left words white; arrows and right words in **blue `#3B82F6`**. Three rows, generous leading, centred. Subtitle smaller, italic-weight Clash, dim white.
- **MOVE:** this is the **Freshbooks springy beat**. Left word snaps in with a **spring/overshoot** (≤6%); a beat later the **arrow draws left-to-right** and the right word **pops** in (`scale .6→1`). Stagger the three rows ~500ms apart, on the music's pulse. When the subtitle arrives, the three pairs **de-saturate/dim** so the line "Language changes. This doesn't." owns the frame.
- **SRC:** designed from scratch.
- **OUT:** the whole stack **collapses toward centre and the blue lingers**, cross-dissolving into the blue of the app's aurora → **into Beat 3** (blue is the A→B bridge).
- **SFX:** light rhythmic ticks synced to each snap; the springy motion should feel "chewy," satisfying.

### Beat 3 — Cut to app + philosophy · 0:22–0:36 · World B (light app)

- **VO:** "You don't think in English. You already know how you think. The hard part is expressing those same thoughts in another language."
  - *(Optional reinforcement if timing allows — founder, first person):* "I wasn't struggling because I lacked English. I was struggling because I couldn't express the thoughts I naturally have every day."
- **TXT:** minimal. Optionally a lower-third of the current VO clause in Inter; otherwise let the screen speak.
- **COMP:** first reveal of the product. The **landing / upload screen** as a floating glass panel on the light **aurora** stage, tilted ~4°, soft shadow. The app's real hero (`Learn English from someone who already talks the way you do.`) and the **"Choose a voice note"** card are visible. *(This is where the word "English" is first allowed on screen — we have earned it.)*
- **MOVE:** **slow push-in** (Lovio) from a wide, slightly-blurred stage toward the upload card as the VO says "expressing those same thoughts." **Rack focus:** aurora soft → card sharp. If using the optional founder line, a small **`sumin-talking.mp4` inset** (rounded, bottom-corner) fades in for that sentence only, then out.
- **SRC:** live-capture of landing/upload, or re-frame from `app-real-record.mp4` (0:00–0:10 region). Optional inset: `sumin-talking.mp4`.
- **OUT:** match-cut forward as the cursor selects the voice note → into the demo spine.
- **SFX:** room tone lifts; a soft UI "focus" chime as the card sharpens. VO warm, first-person.

### Beat 4 — The demo spine · 0:36–1:20 · World B · **the 70%, one continuous session**

This is the technical proof. It must read as **one unbroken run** of the real product. Minimal words; the UI does the talking. VO lands as short captions over the corresponding UI moment.

- **VO (spread across the run, each clause over its matching screen):** "We don't analyze your vocabulary." → "We analyze how you build ideas." → "Then we verify every claim." → "Only then" → "we look for the best role model."
- **Sub-beats:**
  1. **Upload (0:36–0:44).** Cursor picks the voice note in the "Choose a voice note" card; the **"Find my matches"** button goes active and is pressed. *MOVE:* push-in on the button; the press triggers a soft blue ripple. *VO:* "We don't analyze your vocabulary."
  2. **Processing / the agents (0:44–1:04) — the heart.** The **`ProcessingVisualizer`** runs: title **"Finding the creators who talk the way you do."** then the four agent cards resolve **in order**, each spinner → **blue check**:
     `Transcript Agent` → `Thinking Style Agent` → `Role Model Matching Agent` → `Evidence Agent`, then the raised **Confidence Judge** card ("the step that keeps us honest") with its shield mark and live pulse, ending on **"Building your Language Twin…"**. *MOVE:* let the real staggered `lrm-rise` play; add a gentle **parallax drift** and **rack focus** down the list so the eye follows each check. Optionally **speed-ramp** the middle (fast) and settle to real-time on the Confidence Judge — that card is the "we verify every claim" money moment. *VO:* "We analyze how you build ideas." over the first agents; "Then we verify every claim." lands exactly on the **Confidence Judge** card.
  3. **Result (1:04–1:12).** Screen: **"These three English speakers talk the way you do."** with the three **`MatchCard`**s stacking in — **Cinema Therapy, Jay Shetty, Leila Hormozi**. *MOVE:* cards rise/stagger in as floating panels (Seeklab stacked-cards feel). *VO:* "Only then" (hold) …
  4. **Evidence (1:12–1:20).** Push into **one** `MatchCard`'s **"Why these two line up"** block: the **`You said` → `[creator] does` → `Match`** row, with the **"Evidence verified"** pill. *MOVE:* rack focus onto the `You said` quote, then a small lateral move to the `Match` pill as it stamps in (pop). *VO:* "…we look for the best role model."
- **SRC:** primarily `app-real-record.mp4`; recommend fresh native-res capture of `ProcessingVisualizer` and one `MatchCard` for crispness.
- **OUT:** from the verified evidence pill, dissolve on blue → Beat 5.
- **SFX:** quiet, competent UI sounds — soft tick per agent check, a slightly warmer confirm on "Evidence verified." No music swell yet; let it build.
- **Guardrail:** show the journey as **one clean path**. Do not cut away to enumerate other tooling. The only technology named on screen here is the app's own agent names.

### Beat 5 — Signature scene · 1:20–1:38 · World B · newly made, abstract (no real person)

- **VO:** "They don't use the same **words**." *(highlight "words", then fade)* "They use the same **way of thinking**." *(highlight "thinking")*
- **COMP & MOVE:**
  1. Open on **your silent speaking video** full-frame (`sumin-talking.mp4`), lightly graded to the app's cool palette.
  2. It **splits into a left/right frame** via the **CleanShot split-screen wipe** (§5.6): **left = your silent video** (mouth moving); **right = the creator side, represented abstractly with the app's own gradient Avatar tile** (the `135° #1E40AF→#3B82F6` monogram) **plus an animated audio waveform** "speaking" in sync. *No real person, no YouTube logo* — the product's avatar **is** the creator stand-in (keeps it on-brand and trademark-safe).
  3. Slight global **dim**, then the two lines appear centred on the split line, one at a time.
- **TXT:** line 1 `They don't use the same words.` — **"words"** highlights in blue then **fades out**. Line 2 `They use the same way of thinking.` — **"way of thinking"** highlights in blue and **stays**.
- **MOVE detail:** as line 1's "words" fades, the two waveforms briefly look **different** (mismatched shapes); as line 2 lands, the **two waveforms fall into the same rhythm/shape** — the visual punchline that the *thinking* matches even though the words don't.
- **SRC:** `sumin-talking.mp4` (left) + app Avatar + generated waveform (right).
- **OUT:** waveforms merge into a single blue pulse → carries into Beat 6's GPT-5.6 mark.
- **SFX:** two voices faintly out of phase on line 1, resolving into one rhythm on line 2. First subtle music warmth enters here.

### Beat 6 — Why GPT-5.6 · 1:38–2:00 · World A → B

- **VO:** "GPT-5.6 doesn't analyze your English. It reasons about how you organize ideas."
- **TXT:**
  - Centre: a clean **GPT-5.6 mark/wordmark** on near-black. Key contrast beat — **"doesn't analyze your English"** (the word *English* briefly struck-through or dimmed) vs **"reasons about how you organize ideas"** (blue emphasis on *reasons* / *organize ideas*).
  - Then, small, a one-line flow fades in beneath: `builds your communication profile → verifies every observation → finds creators`.
- **COMP:** starts World A (black + blue, the GPT-5.6 icon centred), then the small flow line can dissolve to a **light** mini-panel to bridge back toward the product.
- **MOVE:** icon **pops** in; the contrast line uses a **word-swap emphasis** (strike *English* → reveal *organize ideas* in blue). The 3-step flow draws left-to-right with small connective arrows (echo the app's real `→` flow pills).
- **SRC:** designed; GPT-5.6 official mark. The 3-step line mirrors the app's `ProcessingVisualizer` logic (profile → verify → find).
- **OUT:** cross-dissolve on blue.
- **SFX:** a single clean synth tone on the icon; VO measured, confident.
- **Framing guardrail:** GPT-5.6 = **the product's core reasoning engine** (what the user interacts with). Keep it to reasoning about *ideas*, not grading English.

### Beat 7 — Codex · 2:00–2:15 · World A + real artifacts

- **VO:** "Codex helped us build and iterate on the system."
- **TXT:** small header `Codex` (World A style). Optional single caption: `our engineering teammate`.
- **COMP:** a fast, confident montage of **real Codex artifacts** shown as floating panels: **a pull request · a passing test run · an architecture diagram · a prompt file · an agent definition.** 3–5 artifacts, ~2–3s each, slight overlap.
- **MOVE:** artifacts **whip / slide** in fast with motion blur (this is the one deliberately *quick* montage — energy spike), each snapping to a brief hold. Keep camera moving. Real code is legible for a beat, then blurs as the next arrives (Lovio DoF).
- **SRC:** screen-capture the real artifacts (PR, CI test, `ARCHITECTURE`, a prompt, an agent) — grab these now while open.
- **OUT:** the last artifact recedes into the aurora → Beat 8.
- **SFX:** brisk mechanical/typing ticks; slight tempo lift.
- **Framing guardrail:** Codex = **the engineering teammate that built and iterated the system.** Do **not** enumerate other dev-time tools — only Codex is named here.

### Beat 8 — Network / future vision · 2:15–2:42 · World B (light, animated)

- **VO:** "Instead of searching through millions of videos, you discover the one person who already explains the world the way your mind understands it." *(0.5s)* "And it runs both ways. Even a small creator can come here — to be discovered by the exact people who already think the way they explain the world."
- **TXT:** framing caption, held: `Recognition, not recommendation.`
- **COMP:** camera **zooms out** from a single match to the **`ComingSoonVision`** landscape — the two-sided loop. Use the real vision cards as anchors (**Personal Language Memory** Day 1→Day 14 growth; **the practice loop**; **"A new way for real creators to be found"**), then abstract into a living **Learner ↔ Role Model ↔ Practice ↔ Network** diagram.
- **MOVE:** start on one learner–creator pair, **pull back** (Lovio push-out) to reveal many nodes; **avatar-cluster orbit** (Membrain) of gradient avatars around the loop; connective lines draw between learners and creators. "It runs both ways" = animate arrows **both directions** (learner→creator discovery *and* creator→learner). Keep it calm and expansive, not busy — one loop breathing.
- **SRC:** `ComingSoonVision` component + `app-real-record.mp4` tail (the coming-soon section) + added diagram animation. Gradient avatars from the app.
- **OUT:** the loop contracts to a single glowing blue node → Beat 9.
- **SFX:** music opens up to its fullest, warm and hopeful. VO visionary but grounded.
- *Trim note:* if runtime is tight, keep both VO sentences but drop extra loop narration/animation flourishes (see §9).

### Beat 9 — Close · 2:42–2:56 · World A (black + blue)

- **VO:** "Today, we help you find someone who already thinks like you." *(0.5s)* "Tomorrow, we might understand how you learn well enough to help you become someone else's role model."
- **TXT:** two lines, **Today / Tomorrow** parallel structure, one at a time. `Today,` line white; `Tomorrow,` line resolves with **"someone else's role model"** in blue.
- **COMP:** back to near-black. The film's open ("learn from someone who thinks like you") and close ("help *you* become someone else's role model") are **the same idea, flipped** — mirror the Beat 1 typographic layout so the ending visually rhymes with the opening.
- **MOVE:** calm rise+fade, no spring here — the close is settled, not punchy. After the last line, everything fades but the **blue** persists, resolving into the **product logo / wordmark** (the gradient brand mark + `Language Role Model`).
- **SRC:** designed; app brand mark.
- **OUT:** end card holds ~2s: logo, and (small) the public URL if desired. Fade to black.
- **SFX:** music resolves and lands; last VO line sits in near-silence. Final soft sub-hit as the logo settles.

---

## 9. Runtime & trim order

Target ~2:56; **must land under 3:00.** If the assembly runs over, trim in this order (protect the two book-ends and the technical proof):

1. Drop the **optional founder reinforcement line** in Beat 3.
2. Trim the **middle of Beat 8** — keep both VO sentences and the caption; cut extra loop-animation flourishes.
3. Shorten **Beat 4** processing by speed-ramping the middle agents faster (keep the Confidence Judge in real time).
4. Tighten holds in Beat 7 (artifacts to ~2s each).

**Do not** cut: Beat 1 three-line hook, the Confidence Judge moment (Beat 4), Beat 5 signature, or the Today/Tomorrow close.

**Alternates available (director's choice, from the source script):**
- *Close 9C (creator-side ending):* "Today, you find someone who thinks like you. *(0.5s)* Tomorrow, the creators who think like you find you too."
- *Simpler 6+7 pair (if very tight):* "Codex helped us build and iterate on the system. GPT-5.6 powers the reasoning engine that users interact with."

---

## 10. Music & sound direction

- **Arc:** near-silence and intimacy at the open (Beats 1–3) → quiet competence under the demo (Beat 4) → first warmth at the signature (Beat 5) → opening up through 6–7 → **fullest, hopeful** at the network vision (Beat 8) → resolve and land on the close (Beat 9). One continuous build, not stitched cues.
- **Palette:** minimal, modern, cinematic — soft synth pads, a simple felt-piano or plucked motif, sub-hits on key type beats. No corporate "explainer" stock music, no heavy beat drops. Reference the restraint of the Apple and Lovio clips.
- **VO:** dry, close, first-person, unhurried. Record separately and lay over the captured app run (do not rely on app audio). Respect every scripted `(0.8s)` / `(0.5s)` hold as real silence.
- **SFX:** subtle, expensive UI sounds only (soft ticks on agent checks, a warmer confirm on "Evidence verified"). The Beat 2 springy motion and Beat 7 artifact montage are the two places sound can add "chew" and energy.
- **Loudness:** −14 LUFS integrated, true-peak ≤ −1 dBTP.

---

## 11. Delivery checklist

- [ ] 1920×1080, 30 fps, H.264 MP4, ~16–24 Mbps, AAC.
- [ ] Runtime **under 3:00** (target 2:56).
- [ ] All VO lines match §8 **verbatim**.
- [ ] `.srt` caption file of the VO included.
- [ ] Two visual worlds kept distinct; every A↔B transition hands off on a **blue** element.
- [ ] Fonts: Clash Display (display) + Inter (body) throughout; product palette (§3) exact.
- [ ] Word "English" first appears no earlier than Beat 3.
- [ ] Only **GPT-5.6** and **Codex** named as technologies (see §12); GPT-5.6 = reasoning engine, Codex = engineering teammate.
- [ ] Beat 5 uses the **app avatar + waveform**, not a real person or YouTube logo.
- [ ] Master + a YouTube-uploaded public link.

---

## 12. What to keep OUT (scope guardrails)

To protect the "prove one idea" focus, the following must **not** appear on screen:

- **README / repo prose.** The source script's *Notes & alternates*, *Production reminders*, and README passages (e.g. the fuller Codex sentence) are **director context only** — never on-screen text. Only the verbatim VO of §8 is spoken.
- **App copy that isn't in the plan.** The product contains extra sections (About page's "What this is, and what it is not," accent-scorer comparisons, the takedown/contact email, legal/privacy lines). These are **not** in the video. The only app text that appears is what is naturally visible on the hero, processing, results, evidence, and coming-soon screens as framed in §8.
- **Other development tooling.** Do not enumerate any build-time tools beyond **Codex**. That is a separate story and dilutes the judged narrative.
- **A real, named creator's face/video on the "creator" side.** Beat 5's creator is represented abstractly (app avatar + waveform). The three real matches (Cinema Therapy, Jay Shetty, Leila Hormozi) appear **only** as their in-app `MatchCard`s during the demo — no external channel footage.
- **The word "English" in Beats 1–2.** The subject is thought transfer; earn the word at Beat 3.

---

## Appendix A — Real components & exact on-screen copy (for capture)

| Beat | Component / screen | Exact copy to show |
| :--- | :--- | :--- |
| 3 | Landing hero + upload card | `Learn English from someone who already talks the way you do.` · `Choose a voice note` · `Find my matches` |
| 4 | `ProcessingVisualizer` title | `Finding the creators who talk the way you do.` |
| 4 | Agent cards (in order) | `Transcript Agent` · `Thinking Style Agent` · `Role Model Matching Agent` · `Evidence Agent` |
| 4 | Confidence Judge card | `Confidence check` · `the step that keeps us honest` · `Building your Language Twin…` |
| 4 | Results title + matches | `These three English speakers talk the way you do.` · Cinema Therapy · Jay Shetty · Leila Hormozi |
| 4 | `MatchCard` evidence block | `Why these two line up` · `You said` → `[creator] does` → `Match` · `Evidence verified` |
| 8 | `ComingSoonVision` cards | `Personal Language Memory` (Day 1 → Day 14) · `A practice loop, built around your match.` · `A new way for real creators to be found.` · `For creators` |
| 9 | Brand mark | gradient monogram + `Language Role Model` |

## Appendix B — Palette quick-reference (hex)

`#0A0A0B` world-A black · `#FFFFFF` white · `#A1A1AA` dim label · `#1E40AF` blue-deep · `#3B82F6` blue-bright · `#EFF3FF` blue-tint · `#18181B` ink · `#71717A` ink-tertiary · `#FAFAFB` app stage · `#ECECF0` border · avatar gradient `135° #1E40AF→#3B82F6`.

## Appendix C — Fonts
- **Display:** Clash Display, weight 600, tracking −0.02em.
- **Body / UI / captions:** Inter.
- (Both are the product's real typefaces — using them in World A pre-brands the film before the product appears.)
