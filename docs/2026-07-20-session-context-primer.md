# Session Context Primer — Your Ideal Role Model (hackathon upgrade)

*Read this first. This document exists so that a brand-new session, with a model that has never
seen this project, can pick up the full context in one read: what the project is, why the four
branding docs were written, what background material seeded the work, how Sumin opened the task,
and what she is actually asking for. Nothing here is invented; it is the assembled context of the
task as it stood on 2026-07-20, one day before the hackathon deadline.*

---

## 0. TL;DR (orient in 30 seconds)

**Your Ideal Role Model** (working product name on the landing: **Language Role Model**) is a web
app for adults learning English. You record about two minutes of yourself talking **in your own
native language**. The app looks at *how you talk* — how you build a sentence, open a point, soften
or sharpen a claim — and matches you to three real English YouTubers/creators who talk the same
way, so you can copy (shadow) someone who already sounds like you instead of a random famous person.

It is being built for the **OpenAI Build Week hackathon** (Education track), which is **due
2026-07-21 17:00 PT**. Sumin has **one day** to upgrade it from "works" to "can win." The core
already runs. The gap she wants closed: **stronger analysis, higher-quality recommendations, a
richer results page, and a clear story of future potential** (network effects + a promotion channel
for small creators), plus possibly a **designed team of AI agents** to raise the experience. She
wants to **go deep on planning first**, before building.

---

## 1. The project, precisely

- **What the user does:** records or uploads ~2 minutes of themselves speaking their **native**
  language (no account).
- **What the system does:** transcribes and translates the audio to English (Groq Whisper, plain
  translation), turns *how they talk* into a style measurement, finds the nearest English creators
  in a small hand-built library, and returns the **top 3** with a plain-language reason for each and
  a link to that creator's real videos.
- **Direction is fixed:** native-language-in → English-creator-out. Never flipped.
- **What it is NOT:** not an accent/pronunciation scorer (ELSA, BoldVoice do that), not a "which
  celebrity do you sound like" toy, not voice cloning. The novelty is matching on *how you talk*,
  pulled from your own language before you say a word of English.

### Current build state (what actually exists today)
- A single synchronous **FastAPI** backend, one `/match` endpoint:
  Groq `whisper-large-v3` plain translate → `StyleDistance/styledistance` embedding → numpy cosine
  top-3 → **GPT-5.6** writes the "why you two are alike" text. In-memory corpus, no database, raw
  audio dropped right after translation.
- A **26-creator** hand-seeded library (`backend/data/creators.seed.json`); each row is our own
  descriptors + a channel link, never the creator's real words.
- A minimal **Next.js** front end: upload page → results page with three cards. Tests pass.
- **Phase 0 (the science) is already settled:** matching across languages works via the
  translate-then-measure path ("Path B"); the direct-multilingual path ("Path A") is dead; a fancy
  "style-preserving" translator was tried and abandoned because it polishes away the very speaking
  style we need. Ship plain translation.

*(Full spec: `docs/PRD.md`. Codex build context: `AGENTS.md`. Findings: `docs/phase0-findings.md`.)*

## 2. The hackathon (the target)

- **OpenAI Build Week**, **Education track**. Deadline **2026-07-21 17:00 PT**.
- **Must be built with Codex + GPT-5.6.** Submission needs a **<3-min demo video** (covering how
  Codex and GPT-5.6 were used), a **public/shared repo with a README**, and the **Codex `/feedback`
  session ID** from where the core was built.
- **Judged on four things:** Technological Implementation, Design, Potential Impact, Quality of Idea.
- Every strategic choice in this task traces back to those four judging axes.

## 3. Where the idea came from (the intellectual root)

The product is the applied form of a language-learning methodology **Sumin wrote herself** —
**"Language Learning Methodology: The Science of Inputs and Outputs"** by Sumin Kim
(https://colossal-spruce-b8b.notion.site/Language-Learning-Methodology-The-Science-of-Inputs-and-Outputs-1-2f9c0c9f8ce48025bf07fe34efb73b24).
The full text is reproduced in **Appendix A** of this primer — read it as the theory base. This
section summarizes its actual content (not an outside interpretation of it).

**The framework's core principle:** language learning runs on **input and output**, and the goal is
to *find your own sustainable way to keep doing both.* Learning a language is like learning to swim
— you improve by practicing, not by studying, and skills grow in **stages/plateaus** you only notice
in hindsight. Its structure:

- **Part 1 — Input (absorbing language).** Make input **comprehensible**: the **i+1 rule** — pick
  material about one step above you where you understand ~**80%** (Krashen). Combine **active input**
  (listen with no subtitles → look up and understand → relisten) with **passive input** (things you
  already understand 90%+, natural exposure). **Reading is the key to leveling up** (you need
  **10,000+ words** to understand 99% of real content); balance challenge against your energy, time,
  and enjoyment; and let your **goal** set how hard you push.
- **Part 2 — Output (expressing language).** Output = growing **"what you can say."** Keep asking
  **"how do I say this?"**, which is where **journaling and self-talk** come in. Input and output are
  linked: *you can't speak what you can't read or hear*; matching **text with audio** is what builds
  real listening. **Fluency is pure practice** — the brain learns to process fast and the mouth runs
  on muscle memory; **shadowing** (listen and speak at once) trains those neural pathways.
- **Part 3 — Practical methods.** Input: reading with **sentence mining**, a personal **vocabulary
  bank**, thematic clusters. Active/visual inputs: native→English writing, **shadowing** (its four
  effects: active attention to language, better pronunciation/accent, safe speaking practice,
  activated working memory), and expression-focused lessons. Output: **self-talk** (journal aloud,
  pick a topic and talk, vlog it, talk to a mirror) and **journaling**, with one rule — **don't stop
  to look things up; express first, look up later** — plus the **test effect** (things you try and
  fail are learned better).
- **Part 4 — Two tools.** **My Topics:** capture the specific things *you* actually want to say (your
  own personality and experiences), written in your native language first, then translated — a
  personal topic list for practice. **My Weaknesses:** track the exact skills you lack (subjunctive,
  contrast words, specific grammar), because the brain finds what you tell it to look for.
- **Part 5 — The intermediate plateau.** You can converse but stall with the same words and grammar.
  Causes: the **vocabulary wall** (Zipf's law — rare words that rarely appear), **bad-habit lock-in**,
  and the **comfort zone**. Breaking through: reconnect to your personal reason, practice with
  purpose on specific weaknesses, add harder input, leave the comfort zone, and use **spaced
  repetition**.
- **Appendix (in her doc) — Why listening fails.** Three causes: you can't get the **meaning**, your
  brain is too **slow**, or you can't recognize the **sounds**; fixed with focused vs relaxed
  listening, the **80% rule**, and **prediction training**.

**The through-line to the product (as Sumin built it):** the app operationalizes the **My Topics +
self-talk** step. The learner speaks their own recurring thoughts in their **native language**
(output-first, the thing the methodology says drives growth), and instead of leaving them to shadow
a random native speaker, the app finds a real English creator whose **speaking style matches
theirs** — a shadowing target they will copy naturally, because the sentences are already close to
their own. Shadowing's known payoffs are *why who you shadow matters*, and style-matching is what
makes the copying stick. This also maps the roadmap directly onto her framework: surfacing a
learner's **high-frequency phrases** (My Topics), tracking their **gaps** (My Weaknesses), and the
**practice loop** itself (Shadowing Plus, section 6).

## 4. Two repositories, and the "only look at Codex" rule

This project lives in two folders on purpose:

- **`your-ideal-role-model/`** (this repo) is the **Codex** build. It is the real, shipping code and
  the source of truth. **Only this repo matters for the build.**
- **`Your Ideal Rolmodel/`** (a separate folder) is the **Claude Code** design/experiment lab, where
  Sumin burns more tokens on design and trial-and-error. Its PRD and CLAUDE.md may be **out of date**
  (for example, its CLAUDE.md still calls the project "greenfield," which is no longer true).

**Decision (from Sumin, 2026-07-20):** for this work, **only look at the Codex repo.** If the Claude
Code side is outdated, that is its problem; leave it alone. Do not try to reconcile the two.

**Division of labor for the final push:** design is finished in **Claude Design** (a separate tool);
**branding/message is finished in the Cowork chat** (that produced the four docs in section 5);
**Codex does the functional build** (to save tokens) and assembles the designed HTML into screens;
**tomorrow (2026-07-21)** is demo video + README + submission.

## 5. Why the four branding docs exist (and how they were made)

Before this task, Sumin ran a session to sharpen the product for judging. The flow was:

1. She asked to grasp the whole context first (read the PRD, both repos), then refine.
2. She picked two directions to push: **sharpen the "why"** (make the match explanation credible)
   and **tighten the story** (make the problem → message land for judges).
3. She set a hard rule: **use general, intuitive words** — anyone should understand the marketing
   instantly, no jargon.
4. A strategy/growth sub-agent was run to **adversarially stress-test the positioning**.
5. That produced three docs; a fourth was added after she uploaded the landing-page design.

The four docs (all in `docs/branding/`, all written to be Codex-ready and jargon-free):

| File | What it is | Why it exists |
|------|-----------|---------------|
| `2026-07-19-brand-message-brief.md` | Positioning line, the "why native language?" answer, demo narrative spine, full landing→loading→results copy set | The single source of truth for what the product *says* |
| `2026-07-19-why-panel-spec.md` | Redesign of the match explanation: show 2–3 concrete shared traits as evidence (not one vague sentence) + learner trait chips + the GPT-5.6 prompt as structured JSON | Turns "match by how you talk" from gimmick into "wait, how does it know that?" — the credibility engine |
| `2026-07-19-positioning-adversarial-review.md` | The skeptic/judge review that shaped the above (killed "Stop shadowing strangers," downgraded "thinks like you" → "talks like you") | Keeps the reasoning on record so decisions are not re-litigated |
| `2026-07-19-landing-review.md` | Review of the uploaded `Landing.dc.html`: what is good, what conflicts with product facts (20s vs 2min, 94% score vs resemblance word), what copy to swap | Aligns the marketing landing with the product truth and the brief |

**Key decisions captured across those four (carry them forward):**
- Promise the smaller true thing: **"talks the way you do,"** not "thinks like you."
- Headline: **"Learn English from someone who already talks the way you do."**
- Difference line: **"Most apps help you sound like a native speaker. We find the native speaker who
  already sounds like you."**
- Answer the one confusion on screen 1: **why record your native language** (because how you build a
  sentence is the same in any language, and that is what we listen for).
- Results "why" = **concrete, checkable shared traits**, never a personality-quiz vibe.
- Resemblance shown as a **word** (strong / clear / partial), not a percentage, unless a score is
  deliberately framed as "your style: N%."
- **No em dashes** and **no jargon** in any user-facing copy.

## 6. The bigger vision (the "future potential" to sell, and how far to go)

Sumin is explicit that this hackathon entry is **not just a throwaway first step.** Three layers of
potential to weave into the strategy and the demo:

1. **Network synergy (gets better as users accumulate).** Every learner's result quietly reveals
   *coverage gaps* — "learners like this keep matching poorly, so hand-add more creators like X."
   More users → a smarter library → better matches. (Strict rule from the PRD: a learner is never
   added to the creator library and never shown as another user's match. The aggregate only tells
   the humans what kind of creator to add next.)
2. **A promotion channel for small creators (the two-sided angle).** The other side of the network:
   small English creators could opt in to be discovered by learners who already talk like them — a
   new, intent-matched audience they cannot get from normal recommendation feeds. This is the
   "For English speakers, coming soon" teaser, and it is a real go-to-market wedge, not filler.
3. **Adjacency to a real product she already runs — Shadowing Plus.** Sumin has already built and
   personally uses **Shadowing Plus** (https://github.com/sumin6475/shadowing-plus,
   live at shadowing-plus.vercel.app): a deployed English-shadowing web app + PWA — drop in a video,
   get word-level transcripts with translations, shadow sentence-by-sentence, and drill saved lines
   with spaced repetition (SM-2). It is being pushed toward production. **Strategically, Your Ideal
   Role Model is the front door** (it tells you *who* to shadow); **Shadowing Plus is the room behind
   it** (where you actually *do* the shadowing practice). That adjacency is what makes this entry a
   credible first step of a bigger system, not a toy.

   **Guardrails on that adjacency (from Sumin):** do **not** hard-wire the two together in the demo,
   do **not** paste any Shadowing Plus code into this project, and do **not** publicly announce the
   connection — its launch date and strategy are not set. Use the *idea* of the next step to show
   potential; keep the two codebases separate.

## 7. How Sumin opened this task (verbatim, then plain restatement)

She started the upgrade task with the four branding docs + the hackathon link + the Notion
methodology doc + the Shadowing Plus repo attached, and this prompt (original Korean, verbatim):

> 좋아, 지금 분석한 그 기준과 분석력을 그대로 가지고 내가 지금 진행하고 있는 프로젝트를 '우승
> 가능한 수준이 되도록 업그레이드' 하게 도와줘. 전략을 짜야하고 하루밖에 고칠 시간이 없어서 제대로
> 뾰족하게 가야해. 내가 노리는 해커톤 링크도 추가로 첨부할게. 그리고 지금 첨부한 4개 md파일은 PRD를
> 기준으로 정리한 여러 문서야. 지금은 단순히 음성을 받아서 분석하는것밖에 없어. 지금 내가 많이
> 아쉬운 것은 분석력을 높이고 추천 품질을 높이고 싶어. 그리고 분석 페이지에 보여주는 정보와 분석
> 측면이 다양하게 하는 것도 생각하고 있어. 앞으로의 발전 가능성 (사용자들이 쌓일 수록 시너지가 나는
> 것 + 작은 크리에이터들의 다른 홍보채널) 을 보여주는 전략도 잘 이용해야 할거 같아. 배경지식을 좀
> 더 주자면: 이 아이디어를 생각한 건 '내가 자주 말하는, 생각하는 것들을 먼저 말하기 시작하는 것이
> 빠르게 는다'는 아이디어를 가지고 발전시킨거야. 내가 언어론적인 부분에 깊게 파서 정리했던 Doc도
> 첨부했어. (shadowing-plus 레포) 그리고 발전가능성에 대해 이야기 하자면, 지금 내가 개인 용도로는
> 문제없이 쓰고 있는 쉐도잉 앱을 만들었고 지금 프로덕션 레벨로 발전시키고 있어. 런칭일이나 전략이
> 아직이라 대놓고 연결할 수는 없는데 이게 그 다음 스텝으로 진행되게끔도 할 수 있어. 그러니까, 내가
> 지금 해커톤에 내는 아이디어가 그냥 가벼운 1차 스텝 정도는 아닐거라는거야. 이걸 활용할 수 있으면
> 활용해도 좋아. (shadowing plus의 코드를 직접 넣겠다는건 당연히 아님) 니가 말한거처럼 에이전트를
> 넣는건 찬성이야. 이미 코딩 에이전트 들을 활용해본 경험이 있어. 그리고 이 기회에 핵심 에이전트 팀을
> 명확하게 디자인해서 사용자 경험을 늘리는 걸 해보는건 대찬성이야. 다만 그 전에 플랜 스테이지를 깊게
> 가져갈 생각이야.

**Plain restatement of the ask (for a model reading fresh):**
- Take the same rigor used to analyze the project and now **upgrade it to a level that can win.**
- **One day** only. Strategy has to be sharp and focused, not broad.
- The product today only "records audio and analyzes it." The gaps she most wants closed:
  1. **Higher analysis power** and **higher-quality recommendations.**
  2. A **richer, more varied results/analysis page** — more kinds of insight shown, not one sentence.
  3. A strategy that **shows future potential** — the network-synergy effect *and* the small-creator
     promotion channel.
- Background she wants known: the origin insight (say your own frequent thoughts first), the
  linguistics doc, and that **Shadowing Plus** (her real, in-production shadowing app) can be the
  natural next step — usable as a potential story, but not hard-connected and not code-merged.
- She **agrees with adding agents**, has used coding agents before, and is **enthusiastic about
  designing a clear core agent team** to raise the user experience.
- **But first: go deep on the plan stage.** Do not jump to building.

## 8. Constraints and non-negotiables (do not break these)

- **Plain, intuitive language in everything user-facing.** No jargon (no "rhetorical," "idiolect,"
  "embedding," "style vector," and avoid "shadow" in marketing — use "copy / practice with"). If a
  normal learner would need a dictionary, rewrite it. **No em dashes** in user-facing copy.
- **Product-truth in copy:** sample length is **a minute or two** (short clips break the match);
  resemblance is a **word**, not a bare percentage.
- **Pipeline facts:** plain translation (not a style-preserving translator); Groq non-turbo
  `whisper-large-v3` for the translate step; the English `styledistance` model on the translated
  text; GPT-5.6 only for the "why."
- **Legal red lines:** hand-curated creator library only — **no scraping, no caption/video
  downloaders, no stored transcripts or creator photos**; analyze and link out only; **never retain
  raw user audio**; **no voice cloning**; a learner is never added to the creator library or shown as
  another user's match; naming a creator is fine *inside* the product as a linked result, never in
  ads/marketing. Keep a "request removal" contact.
- **Build split:** design in Claude Design, branding in Cowork chat, function in Codex; **only the
  Codex repo is the source of truth.**

## 9. How Sumin likes to work (so a new session adapts fast)

- **Lead with the conclusion, then explain.** Be concise and direct; cut filler.
- Korean or English depending on the thread; she often works in Korean.
- **Plan first, deeply, before executing.** For multi-step work, outline the plan and get approval.
- She uses coding agents comfortably and wants a **deliberately designed agent team**, not ad-hoc.
- She wants outputs as **reusable artifacts** (docs, specs) that Codex or a future session can pick
  up directly, not one-off chat answers.

## 10. Status and open threads (as of 2026-07-20)

- **Done:** context grasped; positioning sharpened; four branding docs written; landing design
  reviewed.
- **Pending / next:** the **deep plan** for the winning upgrade — specifically (a) how to raise
  analysis power and recommendation quality, (b) what the richer results page shows, (c) the
  future-potential strategy (network + creator channel), and (d) the **core agent-team design** for
  the experience. Then hand a tight, Codex-ready build plan across.
- **Explicitly set aside:** reconciling the outdated Claude Code repo (ignore it); connecting
  Shadowing Plus directly (keep separate).

## 11. The input bundle (what seeds this task)

Attach or point a new session at these:
1. `docs/branding/2026-07-19-brand-message-brief.md`
2. `docs/branding/2026-07-19-why-panel-spec.md`
3. `docs/branding/2026-07-19-positioning-adversarial-review.md`
4. `docs/branding/2026-07-19-landing-review.md`
5. `docs/PRD.md` (full product spec) and `AGENTS.md` (Codex build context)
6. Hackathon: OpenAI Build Week, Education track (deadline 2026-07-21 17:00 PT)
7. Methodology: Sumin's "Science of Inputs and Outputs" doc — full text in **Appendix A** below
   (link in section 3)
8. Next-step product context: the Shadowing Plus repo (link in section 6) — context only, never merged
9. This primer.

---

## Appendix A — The methodology, in Sumin's words (source text)

*Sumin's own document, reproduced so a new session can read the source directly instead of a
summary. Lightly cleaned of copy-paste spacing artifacts; wording is unchanged. Author: Sumin Kim.*

### Introduction: The nature of language learning

Learning a language is like learning to swim. You can read books about swimming all day long, but
you won't actually be able to swim until you jump in the water and practice. Language learning works
the same way — you need to practice regularly. We call it "studying," but it's really more like an
exercise.

That's why language skills grow in stages. You won't notice yourself improving day by day. But when
you look back after a few months, you'll clearly see how much better you've become. Knowing this is
the first step to staying motivated in your language learning journey.

> **Key principle:** The main flow of language methodology is input and output. The goal is to find
> your own way to consistently input and output.

### Part 1. Input: The art of absorbing language

**1.1 The principles of Comprehensible Input.** The most important thing about input is to make sure
you can understand it. Listening to things you don't understand might help a little, but it wastes
your time. Choose materials you can actually understand to learn faster.

> **The i+1 rule:** Pick materials that are just a bit harder (+1) than what you know now (i). If you
> understand about 80% of it, that's perfect. This keeps you challenged without making you want to
> quit.

Language expert Stephen Krashen found that we learn best when we study things that are just slightly
above our current level. If it's too easy, we don't improve. If it's too hard, we quit.

**1.2 Active vs. passive input.** There are two types of input, and it's the combination of the two
that matters.

*Active Input:* This is when you stop, look up, understand, and listen again whenever you hear words
and sentences you don't recognize. An effective order: (1) listen without subtitles first; (2) look
up and understand with subtitles/text; (3) listen again and again. This process maximizes attention.
Research shows that whatever we focus on, we grow.

*Passive Input:* This is when you listen to new material that you understand 90% or more of, or
material that you've already actively learned. It's like listening to your favorite song, a natural
exposure.

> **The importance of exposure to English:** Deepen your learning with active input and increase your
> exposure time with passive input.

**1.3 Reading texts: The key to leveling up.** Reading real books and articles helps language
learners at every level, especially intermediate and advanced learners who want to reach the next
level. Even in your first language, people who read a lot have better vocabulary and express their
thoughts more clearly. The same happens in a new language.

How to read effectively: read regularly and enjoy what you read; choose books that are slightly
challenging (i+1); guess new words from the surrounding text; write down new words in full sentences
and review them regularly. It's fine to read hard books, but easier books help you stay consistent.
Reading anything is better than reading nothing. Reading is essential for reaching advanced levels
(C2) because books use more complex words than everyday conversation. Research shows you need to know
over 10,000 words to understand 99% of novels, articles, podcasts, and similar content.

**1.4 The attitude you should have.** *Proper load balancing:* it's better to study easy, familiar
material than nothing at all, but to improve you must keep challenging yourself at the right
difficulty. Push too hard and you'll quit right before progress. Balance the challenge against your
energy levels, how much time you have, and how much you enjoy it. *Savoring attitude:* when you see a
sentence you don't understand, read it carefully start to finish and try to figure out its meaning.

> If it's way too difficult (more than one level above you), skip it for now. Don't be hard on
> yourself if you can't understand everything. You'll see these sentence patterns and phrases again
> later, and you're always learning as you go.

*The importance of goals:* if your goal is to communicate, you can be satisfied with understanding in
context and move on. If your goal is to progress to an advanced level, take your time with i+2 level
sentences when you have more energy. Being strategic, learning, and accumulating is key.

### Part 2. Output: The art of expressing language

**2.1 The essence of output.** Output is basically about increasing "what you can say." So it's
important to constantly think about your thoughts, your surroundings, and how you would say this.
Collecting and reviewing these statements is also key. "How do I use what I've learned?" is the
question you need to keep asking. This is where journaling and self-talk come into play.

**2.2 Organic connection between inputs and outputs.**

> **Core truth:** You can't understand what you can't read, and you can't speak what you can't read
> or hear.

One reason for poor listening is a disconnect between "text" and "sound" — when you understand with
subtitles but not without them. That's why it's best to have both text and audio in your materials.
It's only when you start to match what you read with what you hear that you develop true listening
comprehension.

**2.3 Fluency is a matter of practice.** Being able to spit out words and form sentences quickly is
completely a matter of practice — the brain starting to process quickly. Research shows shadowing
requires you to actively pay attention because you're listening and speaking at the same time, which
is effective for training neural pathways. The brain has to create new pathways, and the mouth has to
work like muscle memory.

### Part 3. Practical Learning Methods: Maximizing Input and Output

**3.1 Input learning methods.** *Method 1 — Reading:* infer words in context and store new words in
sentences for cumulative review. Key vocabulary strategy: build a **personal vocabulary bank**
connected to your interests; memorize **thematic clusters** (islands of related words) instead of
random words; do **sentence mining** (memorize phrases or sentences, not just words — context has a
powerful effect on the brain). *Method 2 — Visual learning (three active inputs):* active input
(writing) — see the Korean and change it to English, building output muscles; active input
(shadowing) — mimic the speaker's words; and expressive lectures — study nuances explained in your
native language.

> **Four effects of shadowing:** (1) active attention to the language; (2) improves pronunciation and
> accent; (3) a safe opportunity to practice speaking; (4) activates the brain's working memory.

**3.2 Output learning methods.** *Method 1 — Self-talk:* speak out loud (powerful for introverts) —
journal as if you were talking, pick a topic and talk about it, film it vlog-style (no need to
upload), speak to a selfie or mirror. Questions like "How do I say it?" will naturally arise; save
and study them. *Method 2 — Journaling:* you can start even earlier than self-talk — review the
expressions you learned today and yesterday and actively use them.

> **An important principle:** During self-talk or journaling, don't stop to look for expressions.
> It's more effective to stay in the flow and express first, look up later.

*Leverage the test effect:* research shows concepts that are tested and failed are learned better
afterward. Journaling and self-talk create a virtuous cycle where you discover and improve on
concepts you couldn't produce in the first "huh?" moment.

### Part 4. Two Simple Tools: My Topics & My Weaknesses

**4.1 My Topics.** Goes beyond basic self-talk. While driving, walking, or commuting, you'll think of
specific things you want to say — small details that don't come up in regular practice. These moments
show your unique personality and experiences; learning to express them helps you talk about your life
naturally in the new language. How to use it: write your thoughts in your native language first, then
translate them; set aside regular time to practice; use it as a personal topic list for writing or
speaking practice.

**4.2 My Weaknesses.** Most helpful at intermediate/advanced level. Once you can chat easily about
everyday things, you may notice missing skills needed to persuade or explain complex ideas — the
subjunctive ("if I were you..."), contrast words (however, on the other hand), specific grammar
patterns. Write them down and review them regularly.

> **How your brain works:** Your brain is great at finding what you're actively looking for. Decide
> to look for red cars and you'll suddenly notice them everywhere. Writing down your weak areas helps
> you spot and learn them.

### Part 5. Why You Get Stuck (And How to Get Unstuck)

**5.1 Getting stuck is normal.** The intermediate plateau happens when you move past beginner level
and stop improving. You can have everyday conversations but can't get much better with vocabulary or
grammar — using the same words and grammar as months ago, not a beginner but not fluent. This is
completely normal and not your fault.

**5.2 Why you get stuck.** *The vocabulary wall (Zipf's Law):* the 100 most common words make up
~50% of everything you read or hear; the next 1,000 make up another 15–20%; you need more than 10,000
to understand 99%. Once at intermediate level you've learned the common words; what's next is rare,
infrequent, and harder to remember. *Bad habits:* reusing the same simple grammar and phrases locks
your brain into them (always "I want to go" instead of "I've been meaning to go for weeks"). *Comfort
zone:* sticking to familiar topics and rewatched shows instead of harder material.

**5.3 How to break through.** (1) Remember your reason and make it personal; (2) practice with
purpose on specific weaknesses; (3) add more challenging input; (4) leave your comfort zone and ask
people to correct you; (5) use spaced repetition.

> **Remember:** Input — keep learning from content slightly above your level, actively and passively.
> Output — practice talking to yourself and writing with a "how do I say this?" mindset. Connect —
> link what you read to what you hear. Organize — use My Topics and My Weaknesses. Mindset — plateaus
> are normal; trust that you improve in stages and keep going.

The goal of language learning is to communicate, not to be perfect. "Success comes from having a
strategy, learning consistently, and building up knowledge over time. Find a routine that works for
you and stick with it."

### Appendix (in her doc): Why You Can't Understand English Listening and What to Do

Getting better at listening doesn't happen quickly — you can only understand what you already know,
and just listening a lot isn't enough. Find the specific reason you struggle and work on it. Three
main reasons:

1. **You can't understand the meaning.** You hear the words but don't know what they mean — an
   understanding problem, not an ears problem. *Tell:* you still can't understand after reading the
   transcript. *Fix:* read carefully start to finish; study vocabulary, grammar, and patterns; then
   listen to the same material as audio after you've read it.
2. **Your brain is too slow.** You understand when reading the text but can't keep up with speech.
   *Tell:* you understand reading slowly but miss a lot at normal speed. *Fix:* read more (don't look
   up every word); listen to what you read, often; expect at least 5 days of practice to see results.
3. **You can't recognize the sounds.** You get the meaning and can think fast enough but can't catch
   the actual sounds. *Tell:* you understand with subtitles but not without, and trip on small words
   like "to," "the," "in." *Fix:* learn how English sounds work; practice speaking yourself; focus
   hard while listening; slow the audio.

*Train your brain to predict:* even good speakers hear a sentence's start but miss the end because
the brain hasn't learned to predict. To predict better you need lots of knowledge, quick thinking,
and lots of practice.

**Two ways to practice listening** (use both). *Focused (active):* pause when you don't understand;
listen many times over ~2 weeks at increasing intervals, attending to sounds and grammar; good for
all levels. *Relaxed (passive):* don't worry about details, listen for the main idea, let the brain
work naturally — and don't use text for this.

**The 80% rule — choosing the right level.** Easy (90%+): background review of known material. Just
right (80%, best for improvement): note what you don't understand, attend to small words and
connected sounds, practice saying things quietly. Hard (50%): you'll miss a lot but get the gist.
Very easy (100%): great for improving expression and quick thinking.

**Quick self-check.** (1) Can't understand even reading the text → study meaning. (2) Understand
reading slowly but not at normal speed → get faster. (3) Understand with subtitles but not without →
practice sounds. (4) Hear the start but miss the end → prediction practice. (5) Miss small words like
"to," "the," "in" → focused listening.

> "You understand what you know. And by listening, you learn more. Trust this cycle and keep going."

*Written by Sumin Kim, who creates templates to enhance self-improvement.*
