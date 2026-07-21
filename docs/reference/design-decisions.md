# Design Decisions and Engineering Judgment

*Your Ideal Role Model — written 2026-07-20*

This document records the non-obvious design calls behind the matching engine and why each was made. It is not a feature list. It is the reasoning: what was chosen, what was deliberately left out, and what the evidence said. Two ideas run through all of it: **focus** (build the smallest thing that proves the claim) and **honesty** (never let the system, or its labels, claim more than it earned).

The product itself is simple to state: a learner records a few minutes in their native language, and the system returns real English creators who talk in a similar way, with checkable evidence. Everything below is about making that trustworthy.

---

## 1. Architecture: a deterministic supervisor around narrow agents

**Decision.** One synchronous FastAPI request runs a fixed sequence: transcript (Groq Whisper, no LLM) → deterministic input gate → three *separate* GPT-5.6 calls (Style Reader, Evidence Writer, Confidence Judge) with a non-LLM vector matcher running in parallel. A hard 45-second deadline wraps the whole thing, and every stage has a graceful fallback.

**Why.** The parts that must be reliable (gating, matching, orchestration) are deterministic code, not model calls. The parts that need judgment (reading style, writing evidence, checking that evidence) are isolated model calls with one job each. Splitting the LLM work into three prompts instead of one keeps each call auditable and lets a failure in one stage degrade to a simpler answer instead of breaking the response.

**Tradeoff.** More moving parts and more prompts to maintain than a single "do everything" call. Accepted, because separation is what makes the output checkable and the failure modes bounded.

*This mirrors the deterministic-supervisor pattern from HAIT: the code decides when and whether a model runs; the model only does the qualitative step.*

---

## 2. Focus: decide what NOT to build

**Decision.** Ship a thin vertical slice. Plain audio-to-English translation, not a style-preserving translator. One embedding path (Path B), not two. A precomputed in-memory corpus, no database or vector store. A demo cache for a reliable live demo. Originally a single LLM call.

**Why.** Each cut removed a failure surface without weakening the core claim. The style-preserving translator was actually tried and then abandoned: it polished and re-split sentences, which erased the idiolect the style model depends on. Embedding native-language text directly (Path A) was tested and killed because it did not match. Focus here was not laziness; it was subtraction backed by a test.

**Tradeoff.** The demo-scale corpus and in-memory matching will not survive real traffic. That is fine for what this is: a proof, not a production service.

---

## 3. Scale the dataset only after checking quality

**Decision.** Grow the creator corpus from 26 to 130, but treat the larger set as *candidate* data until its quality is proven, not as a finished asset.

**Why.** The expansion passed every structural check: 130 rows, schema valid, politicians excluded, URLs well-formed, ten tests green. But structural validity is not quality. A closer look showed the substance was hollow: six of nine style axes were the constant value "1" for every creator, and the three that varied were assigned in mechanically even buckets. The scores that actually drive matching were placeholders.

**Evidence.** With those profiles, the vectors did not discriminate. Nearest-neighbor cosine was above 0.99 for 129 of 130 creators (median 0.998). In plain terms, every creator looked like every other creator, so any match was effectively random.

**Lesson.** "The tests pass" and "the data is good" are different claims. Automated validation guards shape, not truth.

---

## 4. Put the human in the loop where it actually pays off

**Decision.** Do not hand-score 130 creators. Instead, run two honest tiers: 130 AI-drafted, builder-reviewed *candidate* rows, plus 10 *human-verified* rows drawn from creators the builder personally follows and can observe directly. Total 140, of which 10 are genuinely verified.

**Why.** Hand-scoring 130 creators the night before a deadline is not realistic, and pretending to is worse than not doing it. The useful move was to spend real human attention where it changes the outcome: a small set the builder actually watches, scored on a shared nine-axis rubric, with URLs verified by search. Honesty is carried by the *label*, not by faking effort.

**A line held.** The original data auto-stamped every row as "approved" by named reviewers who never existed. That metadata was replaced: candidates are marked `ai-draft` / `builder-review`, and only the ten observed rows carry `human_verified`. The system does not claim an independent review it never had. A known limit is stated plainly too: the rubric has nine axes and does not measure humor.

---

## 5. Normalization: diagnose the real cause, then fix it without faking

**Decision.** When applying real, varied scores still did not spread the vectors, do not touch the scores or the probe generator. Re-center the matching space instead: subtract the corpus centroid from both the creator vectors and the learner query before cosine.

**Why.** The collapse was structural, not a data problem. Every vector shared a large common component that pinned all pairwise similarities near the top of the scale. Removing that shared component (standard mean-centering) lets the real differences dominate. This is a normalization, not a fabrication, so it keeps the "no fudging the numbers" rule intact.

**Evidence (measured offline on the 140 vectors).**

| transform | nearest-neighbor cosine (median) | all-pairs cosine (median) |
|---|:--:|:--:|
| raw | 0.997 | 0.953 |
| centroid removed | 0.950 | −0.04 |
| centroid + top principal component removed | 0.925 | −0.03 |

All-pairs similarity moved from 0.95 to about 0, which means the vectors finally point in genuinely different directions.

**Status.** Verified offline; handed to the backend to implement in the matcher and re-check against an acceptance gate.

---

## 6. LLM-as-a-judge, gated so it stays cheap

**Decision.** Some creators share an identical nine-axis profile (archetype twins), so their vectors are exactly equal and centering cannot separate them. For those ties only, a deterministic gate triggers a cheap, fast LLM that re-ranks the tied candidates using pre-generated qualitative style descriptions. Vectors stay the source of truth; the model runs on the exception, not the rule.

**Why.** This spends model cost precisely where the cheap method runs out of resolution, and nowhere else. The gate is deterministic (a similarity-gap threshold, or an exact-profile match), so the expensive path is predictable. The descriptions are generated once, offline, and describe *how* a creator talks without quoting them, which respects the same legal line as the rest of the corpus. The tiebreaker is kept separate from the three core reasoning calls and falls back to the plain vector result on any error.

**Tradeoff.** One more component and one more prompt. Justified because it removes arbitrary ties without making every request pay for an LLM.

*Same principle as sections 1 and 4: the deterministic layer decides when the model is worth it; the model only does the judgment a rule cannot.*

**Status.** Designed and specified; handed to the backend to build.

---

## What this set of decisions demonstrates

| Decision | Judgment shown |
|---|---|
| Deterministic supervisor around narrow agents | System design, failure isolation |
| Subtracting features backed by tests | Scoping, knowing what not to build |
| Candidate vs verified dataset tiers | Data quality skepticism, honest labeling |
| Human review placed on the 10 that matter | Effort allocation under a deadline |
| Centering the embedding space | Root-cause diagnosis, principled fix |
| Gated LLM tiebreaker | Cost-aware use of models where rules fall short |

The consistent thread: prefer the cheapest reliable method, measure whether it actually works, and when it does not, fix the real cause rather than dress up the number.
