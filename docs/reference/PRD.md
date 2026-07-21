# Your Ideal Role Model (Language Role Model) — PRD v2

*2026-07-20. Upgraded from the original `docs/PRD.md` (DRAFT) to reflect the hackathon pivot and all
plan-stage decisions. Companion docs: `2026-07-20-strategy-ai-role-model-engine.md` (strategy),
`2026-07-20-agent-architecture-spec.md` (build-ready architecture), `2026-07-20-session-context-primer.md`
(background), and `docs/branding/*` (positioning, copy, design). This PRD is the product source of
truth; the architecture spec is the engineering source of truth.*

---

## 0. What changed from v1 (read first)

v1 framed this as a recommendation app: record audio, get 3 creators. v2 reframes it as **an AI
reasoning system that decides who you should copy to learn fastest**, and positions the product as a
**Personal Language Twin** whose first feature is that match. The recommendation is one step of a
loop, not the whole product. Concretely, v2 adds: a multi-agent reasoning pipeline with a separate
verification pass (Confidence Judge), evidence chains grounded in the learner's own words, locked
plain-language positioning, an honest "poor fit" caveat, and a staged vision (memory, twin, loop,
network) shown but not built.

## 1. Problem statement

Adults learning English are told to shadow (copy) native speakers, but **copy who?** They are handed
generic celebrities or whoever is popular, people whose way of building thoughts may be nothing like
their own, so copying feels fake and slow. There is no way to find an English speaker whose *way of
talking* already resembles how the learner personally expresses thoughts, which is the fastest path:
practice, in the target language, the structures *you* already use, spoken by someone who talks a
similar way.

## 2. The reframe (the heart of v2)

- **Not a recommendation engine. A reasoning system.** The value is not "here are 3 creators," it is
  "an AI read how you build your thoughts, verified every claim against your own words, and only then
  matched you." The reasoning being *visible and checkable* is the product.
- **Personal Language Twin.** Each session builds a picture of how you talk. The match is feature one;
  memory, a practice loop, and a two-sided creator network follow.
- **Direction is fixed:** native-language-in → English-creator-out. Never flipped.

## 3. Key hypotheses

- **Product:** analyzing a learner's speaking style from their native speech and matching it to a
  similar English creator gives a role model that is markedly easier and more motivating to copy.
  Success signal: **≥60% of a small bilingual test panel rate their top-3 match as "this person
  builds thoughts like me."**
- **Credibility (new in v2):** a match feels true only when the "why" is concrete and checkable. The
  Confidence Judge (a second AI pass that verifies each reason against the transcript and drops what
  it cannot find) is what turns a subjective match from a horoscope into evidence.
- **Technical (validated, Phase 0):** cross-language style matching works via translate-then-embed
  (Path B); embedding native text directly (Path A) is dead; a style-preserving translator is
  abandoned (it polishes away the idiolect we need). Ship plain Whisper translation.

## 4. Users

- **Primary:** an adult learning English at an intermediate level (the plateau: can converse, stuck
  with the same words and grammar), who already believes in copying real speakers and wants a
  *specific real person* to model. Can produce 1 to 2 minutes of themselves talking naturally in
  their native language.
- **Job to be done:** "When I try to learn English by copying a native speaker, I want a real English
  creator whose way of building and delivering thoughts resembles mine, so I can model someone who
  already talks a similar way and pick up the language faster."
- **Non-users:** complete beginners; people wanting accent or pronunciation scoring (accent apps
  serve them); people wanting a "which celebrity do I sound like" novelty; anyone expecting voice
  cloning.

## 5. Solution

A frictionless web app: the learner records or uploads ~1 to 2 minutes of themselves speaking their
**native** language (no account). The system:
1. **Transcribes and translates** to English (Groq `whisper-large-v3`, plain translate), then deletes
   the raw audio immediately.
2. **Reads how they talk** (thinking pattern + learning style), grounded in specific sentences.
3. **Matches** the top-3 English creators from a hand-seeded corpus by style similarity.
4. **Writes evidence chains** per creator: **You said → Creator does → Match**.
5. **Verifies** every reason against the transcript (Confidence Judge), drops anything unverifiable,
   and sets a resemblance word (strong / clear / partial), never a percentage.
6. Returns the **top-3 cards + evidence chains + resemblance word + a reasoning trace**, and links out
   to the creators' real videos to start copying.

The reasoning is surfaced to the user: a Processing screen shows the pipeline running, and the results
show the reasoning trace and the Judge's verdict. That visible reasoning is the differentiator.

## 6. MVP scope

| Priority | Capability | Note |
|----------|-----------|------|
| **Must** | Prompted record/upload of native-language audio, no account | ~1 to 2 min, plain elicitation, "talk like you would with a friend" |
| **Must** | Reasoning pipeline: transcript → style read → match → evidence → **Confidence Judge** | 3 GPT-5.6 calls (A style, B evidence, C judge) + non-GPT ASR and cosine; see architecture spec |
| **Must** | Results: exactly 3 matches, evidence chains (quote → descriptor → match), **resemblance word**, links out | resemblance is a word, never a % |
| **Must** | Reasoning visualization (Processing + a "how we got here" trace) | the visible-reasoning hero |
| **Must** | Consent + raw audio deleted right after translation; nothing derived persists by default | privacy spine |
| **Should** | Demo cache (seeded recording returns instantly) for reliable demo | p90 can exceed the 45s deadline; demo runs on cache |
| **Should** | 3 surfaces: Landing (sell), About (depth + vision mockups), App (demo) | see branding docs |
| **Won't (built)** | Accounts, login, saved history | shown as vision only |
| **Won't (built)** | Personal Language Memory, Language Twin, practice loop, creator network | **shown as labeled vision mockups**, not built |
| **Won't** | Automated YouTube scraping, stored transcripts, marketing with creator names/likeness | legal red line |
| **Won't** | Voice cloning | legal/ethical red line |

## 7. Reasoning system (summary; full detail in the architecture spec)

- **Single synchronous FastAPI `/match`**, deterministic supervisor (`run_pipeline`), in-process
  `asyncio` only. No queue, lock, or worker.
- **6 roles → 3 real GPT-5.6 calls:** Call A = Style Reader (thinking + learning style), Call B =
  Evidence Writer, Call C = **Confidence Judge (separate pass, never merged)**. Non-GPT: Transcript
  Agent (Groq) and Creator Matcher (styledistance + numpy cosine). A future opt-in Memory Worker is
  the only component that touches persistence.
- **Guardrails:** global 45s deadline, per-step timeouts, max 1 retry each; input gate **≥45s AND
  ≥120 words** (short samples give unstable matches); a deterministic copy guard strips jargon and em
  dashes from user-facing fields; graceful degradation always renders 3 cards.

## 8. Success metrics

| Metric | Target | How |
|--------|--------|-----|
| Match feels right (primary) | ≥60% rate top-3 as "builds thoughts like me" | thumbs + bilingual panel |
| Reasoning is checkable (new) | Judge drops unverifiable reasons; shown reasons are grounded in the transcript | inspect evidence vs transcript |
| Marginal cost per match | ≈$0 at demo volume | Groq free tier + owned hosting |

## 9. Positioning and messaging (locked; full copy in branding docs)

- **Headline:** Learn English from someone who already talks the way you do.
- **Differentiation:** Most apps help you sound like a native speaker. We find the native speaker who
  already sounds like you.
- **Why native language:** The way you build a sentence, ask a question, or tell a story is **similar**
  in any language, and that is what we listen for. *(Use "similar", never "same" — cultures express
  differently.)*
- **Copy rules:** plain English, no jargon in user-facing copy (no "embedding / style vector /
  idiolect", avoid "shadow" in marketing → use "copy"), **no em dashes**, resemblance as a word,
  never say "how you think" (use "the way you talk"), never mention the adjacent shadowing product in
  public copy.

## 10. Honest caveats (when this is a poor fit)

State plainly, as clarity not apology: the product reads your **natural, present speaking voice**.
- Talk loosely and unscripted, in your own language.
- A rehearsed script read aloud, or written English typed in, is a **poor fit** — a polished
  performance hides how you really talk, which is the one thing we listen for.
- The result is a learning-fit suggestion, not a score on your voice or your English.

## 11. Roadmap (vision, shown but not built at MVP)

1. **Personal Language Memory** — with opt-in, save a profile of how you talk (never audio) and show
   what changed between recordings.
2. **Language Twin** — a living profile that gets richer each session, sharpening matches and practice.
3. **Practice loop** — understand you → find match → practice with them → see what grew → fresh match.
4. **Creator discovery network** — the role models are real English vloggers, a pool that keeps
   growing. When a learner matches a vlogger, that vlogger gets found by exactly the person who wants
   to learn from them, so a small creator gains a new way to be discovered through the way they talk.
   More learners means better matches and more creators found; a bigger pool means a better match for
   every learner. (Learners are never turned into match targets, per the data-strategy red line.)

## 12. Data strategy and legal (carried from v1, still binding)

- **Match targets are English creators, always hand-seeded, never a learner.** A learner's vector is
  never added to the creator corpus and never returned as another user's match. (Red line.)
- **A corpus row MAY hold:** style vector, creator name, source URL (link-out), our own
  human-authored style descriptors, factual metadata. **MUST NOT hold:** full/long verbatim
  transcripts, downloaded audio/caption dumps, or stored creator photos/logos.
- The evidence "why" is built from **our descriptors + the learner's own words**, never the creator's
  words.
- **Retention:** raw audio destroyed within the job, unconditionally. Transcript and translation are
  transient. By default nothing derived persists. Only with explicit, default-off, opt-in may a
  derived style vector be kept (pseudonymous, opaque-token deletable) for learner-side eval / "learners
  like you" — never added to the creator corpus, never shown to another user.
- **DO:** hand-pick a small curated set; store the style vector + name + canonical link + our own
  descriptors; present as the learner's result with a "not affiliated" line and a takedown link.
  **DON'T:** run scrapers/downloaders at any volume; store transcripts or long verbatim; use a
  creator's name/face/branding in ads/SEO; imply endorsement; add a user to the creator corpus.

## 13. Tech stack

| Layer | Choice | Note |
|-------|--------|------|
| Backend | Single synchronous FastAPI `/match`, local | runs the whole pipeline per request; no DB/queue for the demo |
| ASR + translation | Groq `whisper-large-v3` (translate task) | plain translate; `-turbo` cannot translate |
| Style embedding | `StyleDistance/styledistance` (English), CPU | on the plain-translated text (Path B); load once at startup (singleton) |
| Matching | numpy cosine over precomputed `corpus.npz` (26 hand-seeded creators) | vectors precomputed offline, loaded at startup |
| LLM (A/B/C) | OpenAI **GPT-5.6** | Style Reader, Evidence Writer, Confidence Judge; token caps A 500 / B 700 / C 500 |
| Frontend | Next.js (App Router) + the existing design system | never runs ML; renders reasoning trace + evidence |
| Future (not MVP) | opt-in Style Memory store, opaque-token keyed | the only persistent, opt-in component |

Budget ceiling ~$10/mo; ~$0 marginal at demo volume.

## 14. Security and privacy

- No accounts in MVP → minimal PII. 18+ affirmation.
- Raw audio never retained (deleted right after translation). Transcript and translation transient.
  By default nothing derived persists; only an opt-in derived vector may be kept (pseudonymous,
  deletable via opaque token).
- Secrets (`GROQ_API_KEY`, `OPENAI_API_KEY`) in env only, never committed.

## 15. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Match feels like a horoscope (subjective, no ground truth) | evidence chains + **Confidence Judge** verifying against the transcript; resemblance as a word; honest framing |
| Latency (3 sequential GPT calls, ~36s typical, p90 ~56s) | token caps, shrink Judge input to cited sentences, startup singletons, progressive reveal, **demo cache** |
| Bad input (scripted or written English) | honest caveat + input gate (≥45s AND ≥120 words) + short-sample resemblance cap |
| Legal (ToS, publicity, scraping) | hand-curation only, never scraping; analyze + link out; store vector + descriptors, no verbatim; takedown link; no voice cloning |
| ASR erases idiolect / spoken vs written domain shift | accept structural/rhetorical over lexical features; longer natural samples |

## 16. Build Week submission

Built with **Codex + GPT-5.6** (Education track, deadline 2026-07-21 17:00 PT). Requires a <3-min
demo video (covering how Codex and GPT-5.6 were used), a public/shared repo with README, and the
Codex `/feedback` session ID from where the core was built. README one-liner: *Codex built a
deterministic FastAPI orchestrator running GPT-5.6 as a 3-call reasoning pipeline (read style, write
evidence, then a separate Confidence Judge verifies every claim against the learner's own words), so
the match is reasoned and checkable, not a vibe.*

---
*Status: v2, aligned to the hackathon build. Phase 0 validated; Phase 1 (this MVP) in build.*
