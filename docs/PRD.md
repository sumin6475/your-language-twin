# Your Ideal Role Model

## Problem Statement

Adults learning English are told to "shadow" native speakers, but they're handed generic
celebrities or whoever is popular — people whose way of thinking and structuring speech may
be nothing like their own, which makes shadowing feel unnatural and slow. There is no way
for a learner to find an English speaker whose *rhetorical style* already matches how they
personally express thoughts, so they miss the fastest path linguistics offers: study the
phrases and structures *you* already use, in the target language, spoken by someone who
thinks like you.

## Key Hypothesis

We believe that analyzing a learner's **linguistic/rhetorical style** from their native
speech and matching it to a similar English creator will give them a role model who is
markedly easier and more motivating to shadow.
We'll know we're right when **≥60% of a small bilingual test panel rate their top-3 match
as "yes, this person structures thoughts like me."**

Upstream of that product hypothesis sits a **technical hypothesis that must be validated
first** (Phase 0): that cross-language style matching works at all — that a learner speaking
Korean/Spanish can be meaningfully matched to an English creator by style. This is unproven
and is the single biggest risk in the project.

## Users

**Primary user**: An adult foreigner actively learning English (intermediate level), who
already knows about shadowing/immersion and wants a *specific real person* to model — not
another app that just scores their pronunciation. They can produce 2–3 minutes of themselves
speaking their native language (self-talk video, a phone/meeting recording).

**Job to Be Done**: When I'm trying to learn English by shadowing a native speaker, I want to
find a real English creator whose way of structuring and delivering thoughts matches mine, so
I can model someone who already "thinks like me" and pick up the language faster.

**Non-users**: Complete beginners with no English; people wanting pronunciation/accent scoring
(ELSA, BoldVoice already serve them); people wanting acoustic "which celebrity do I *sound*
like" novelty (a crowded, different space); anyone expecting voice cloning.

## Solution

A frictionless web app: the learner records or uploads ~2–3 min of themselves speaking their
**native language**; the system transcribes it (Groq Whisper), embeds its *style* (not its
content or timbre) with a multilingual style model, and finds the nearest English creators in
a precomputed corpus by cosine similarity. It returns the **top-3 matches**, an LLM-generated
**"why you two are alike"** rhetorical profile (the explainability that makes a subjective
match feel true — "you both open with rhetorical questions and use 'kind of / you know'"), and
**links out to the creators' real videos** to start shadowing. This approach is chosen because
the core novelty is linguistic-style matching, and the reusable ML for it now exists off the
shelf (`mStyleDistance`), letting us compose rather than build from scratch on a tiny budget.

### MVP Scope
| Priority | Capability | Rationale |
|----------|------------|-----------|
| **Must** | Phase 0 science spike: validate cross-language matching (direct vs translate-then-match) before product code | The whole concept rides on this; it's cheap to test and expensive to assume |
| **Must** | Upload/record native-language audio (cap ~3 min), no account | Frictionless = fastest to a validation alpha + honors "don't retain raw audio" |
| **Must** | Async pipeline: Groq Whisper → style embedding → pgvector k-NN over ~100 English creators | The core matching engine |
| **Must** | Results page: top-3 matches + LLM rhetorical "why" + links to real videos | The deliverable value; the "why" is what makes a subjective match credible |
| **Must** | Consent + raw-audio-deleted-after-processing | Legal/privacy posture; also a trust signal |
| **Should** | Thumbs up/down on each match ("feels right?") | Captures the primary success metric directly |
| **Should** | Precomputed corpus of ~100 English creators (celebrities/podcasters first) | Easier to source with licensed transcripts; better name recognition for the reveal |
| **Won't** | User accounts / saved history / login | Deferred: adds build + security surface an alpha doesn't need; revisit for pedagogy phase |
| **Won't** | Shadowing pedagogy loop (clips, record-and-compare, pronunciation scoring) | Phase 2 — only valuable once matching is proven |
| **Won't** | YouTube scraping at scale / marketing with creator names & likenesses | ToS + publicity-rights risk; use licensed datasets + link-out only |
| **Won't** | Voice cloning of any kind | Legal/ethical red line |

## Success Metrics
| Metric | Target | How measured |
|--------|--------|--------------|
| **Match feels right** (primary) | ≥60% of testers rate top-3 as "structures thoughts like me" | Thumbs up/down on results page + bilingual panel judgment |
| Phase 0 gate (pre-product) | A majority of 5–10 samples yield a top-3 match a bilingual human accepts | Manual judgment in the spike (see `spike/README.md`) |
| Marginal cost per match | ≈$0 (within free/owned tiers) | Groq free tier + Railway $5 + Vercel Pro; watch Groq req/day |

## Open Questions
- [ ] **Phase 0 result**: does cross-language matching hold? Which path wins — direct
  (`mstyledistance`) or translate-then-match? Determines the Phase 1 pipeline. **Blocks product code.**
- [ ] Which specific creators seed the ~100-creator corpus, and from which licensed datasets? (TBD - needs sourcing pass)
- [ ] Minimum viable sample length for a stable style signal (2 min? 3 min?) — tune in Phase 0.
- [ ] How to present matches so they read as "creators you'll learn well from," not false precision.

## Implementation Phases
| # | Phase | Delivers | Status | Depends |
|---|-------|----------|--------|---------|
| 0 | Science spike (done: built; must be RUN) | Go/no-go on cross-language matching; chosen pipeline path | pending | - |
| 1 | Thin vertical slice | Upload → transcribe → match → top-3 + "why" + video links, no account | pending | 0 |
| 2 | Pedagogy (shadowing loop) | Clips, transcript, record-and-compare; surface learner's own high-frequency chunks | pending | 1 |
| 3 | Scale corpus & personalization | More creators (licensed sourcing, legal hardening), match-quality eval, accounts | pending | 1 |

---

## Technology Stack
*(feeds `/create-rules`)*

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend / API | Next.js (App Router) on **Vercel Pro** (owned) | Orchestrates + polls only; never runs ML (no GPU, short timeouts) |
| ASR | Groq **`whisper-large-v3-turbo`** | ~$0.0006/min, free tier ~2000 req/day, <5s per file; no self-hosted GPU |
| Style embedding | **`StyleDistance/mstyledistance`** (multilingual, content-independent) on CPU | The pivotal enabler for native-in → English-out; runs in seconds on the Railway box |
| Fallback embedding | **`StyleDistance/styledistance`** (English) for translate-then-match | Used if direct cross-language matching is weak |
| Worker | Python worker on **Railway $5** | Runs Whisper call + embed + k-NN + LLM profile async |
| Vector store + jobs | **pgvector on Railway Postgres** | Embeddings + creator metadata + job rows in one DB; brute-force cosine fine at this scale |
| LLM "why" profile | Claude via **Vercel AI Gateway** (`anthropic/claude-*`) | Structured rhetorical profile for explainability + optional re-rank |

**Budget:** ~$10/mo ceiling; effectively $0 marginal at MVP volume (owned Vercel Pro + Groq free tier + Railway $5).

## Core Architecture & Patterns

`native-language audio (≤3 min) → [Vercel: upload, write job row] → [Railway worker: Groq
Whisper → style embed → cosine k-NN over precomputed corpus → LLM rhetorical profile] →
[Vercel: poll/SSE → results page] → link out to creators' real videos.`

Corpus is precomputed offline (transcribe/collect licensed creator content → embed once →
store in pgvector). Frontend never touches the ML.

## Security & Configuration

- **No accounts** in MVP → minimal PII surface.
- **Raw audio is never retained**: deleted immediately after transcription; only the derived
  transcript/embedding (and only as long as needed to return a result) persist. Stated consent
  at upload.
- Learner audio is personal data (GDPR): consent + deletion honored by design.
- Secrets (`GROQ_API_KEY`, DB URL, AI Gateway key) in env only; `.env` blocked by the security
  hook and `.gitignore`.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **Cross-language style matching may not hold** (research-grade, unproven) | Phase 0 spike gates all product code; translate-then-match fallback preserves native input |
| **ASR erases idiolect** (Whisper cleans up fillers/disfluencies — the signal we want) | Accept matching on structural/rhetorical > lexical features; use longer (2–3 min) samples |
| **Spoken ≠ written** (style models trained on written text; transcribed speech is a domain shift) | The spike is exactly how we detect if this is fatal |
| **"Style similarity" is subjective; no ground truth** | Present as "creators you'll vibe with / learn well from"; human-in-the-loop thumbs rating; LLM "why" for credibility |
| **Legal: YouTube ToS, publicity/voice rights, scraping IP bans** | Licensed datasets + self-transcription only; analyze + link out (never rehost/large verbatim); no voice cloning; no name/likeness marketing until reviewed |

## Future Considerations (post-MVP, deferred)

- Native-input for many languages (MVP proves the mechanism on a few).
- Shadowing pedagogy: surface the learner's own high-frequency chunks (Lexical Approach) and
  their English equivalents in the matched creator's speech; optional ELSA-style pronunciation scoring.
- Accounts, saved matches, progress tracking, personalization.
- Corpus at scale: paid transcript APIs, proxy/legal hardening, match-quality judgment sets.

---
*Status: DRAFT - needs validation (Phase 0 spike is the first validation step)*
