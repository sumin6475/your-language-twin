# Codex handoff — matcher centering + LLM-as-judge tiebreaker (2026-07-20)

**Owner:** Codex (backend). **Do not touch `web/`.**
**Why:** Applying the reviewed scores did NOT spread the vectors (nearest-neighbor cosine median still 0.997). The collapse is structural, not a data problem. Two changes fix it: (1) a standard embedding re-centering in the matcher, and (2) a cheap LLM tiebreaker for the creators whose style profiles are genuinely identical. **Do not fake scores or edit `make_style_probes`.**

---

## Change 1 — Center the matching space (the big fix)

Every vector shares a large common component that pins all pairwise cosine near 0.95–0.997. Subtracting the corpus centroid removes that shared component so real style differences dominate. This is standard "mean-centering / all-but-the-mean" post-processing — it does not fabricate anything.

**Verified offline on the current 140 vectors (numpy, no model):**

| transform | nearest-neighbor cosine (median) | all-pairs cosine (median) |
|---|:--:|:--:|
| raw (now) | 0.997 | 0.953 |
| **centroid removed** | **0.950** | **−0.04** |
| centroid + top-1 PC removed | 0.925 | −0.03 |

**Implement:**
1. In `build_corpus`: after building `vectors`, compute `centroid = vectors.mean(axis=0)`. Store `centroid` (float32, 768-d) inside `corpus.npz` alongside `ids`/`vectors`. (Optional dial: also store `pc1`, the top principal component of the centered matrix.)
2. In `corpus.load_vectors`: also return `centroid`.
3. In `corpus.top_k` (and wherever the query is scored): transform BOTH sides before cosine — `v' = normalize(v - centroid)` for every corpus vector, and `q' = normalize(q - centroid)` for the learner query. Rank by `q' · v'`. (If you added `pc1`, also subtract its projection from both.) The learner query must use the SAME centroid — it is a fixed transform of the space, not per-request fitting.
4. `quality_report`: compute `nearest_pairs` and the dispersion metrics in the **centered** space (that is the space the matcher actually ranks in), so the report reflects reality.

**Acceptance gate:** post-centering, all-pairs cosine median ≈ 0 and nearest-neighbor median < 0.96. If not, stop and report.

---

## Change 2 — Deterministic gate → cheap LLM tiebreaker (HAIT pattern)

Some creators have **identical 9-axis profiles** (archetype twins, e.g. `andrew-huberman` = `practical-engineering` = `coldfusion`; `ramit-sethi` = `matthew-hussey`). Their vectors are exactly equal (cosine 1.0), so centering cannot separate them. When a learner lands on such a cluster, a cheap LLM judge breaks the tie using pre-generated qualitative descriptors. Vectors stay the source of truth; the LLM only runs on ties.

### 2a. Pre-generate rich descriptors ONCE (offline build step)
- Add a field `style_descriptor_long` to every creator row (all 140): **2–3 original sentences describing HOW they talk** — sentence structure, pacing, questioning, directness, warmth, how they move from idea to idea. **No creator quotes, no catchphrases, no topic/plot, no names of their videos.** This is our authored style description (same legal rule as the existing short descriptors).
- Generate them with a new offline script `backend/build_descriptors.py` using the **cheap model** (see 2c), writing back into `creators.seed.json`. Run once now; committed as data. Tier it honestly: candidates stay `verification: "candidate"`, the 10 verified rows keep `human_verified` (you may hand-refine those 10).

### 2b. Runtime gate + tiebreaker (in the matcher stage)
- `top_k` returns the top **N = 6** by centered cosine (not just 3).
- **Deterministic gate:** flag a tie if `score[0] - score[2] < TIE_EPS` (default `0.03`) **OR** if two or more of the top-3 share an identical `style_profile`.
- **No tie →** return the top-3 as-is (LLM never runs; stays cheap).
- **Tie →** call the tiebreaker LLM with: the learner's `transcript_en` (style sample) + the `style_descriptor_long` of the N tied candidates. It returns a ranked top-3 (`{ranked_ids:[id,id,id]}`), which then flows into the existing Evidence Writer (B) and Confidence Judge (C) unchanged.
- **Fallback:** on tiebreaker error/timeout, return the raw centered top-3 (mirror the existing `judge_skipped` graceful path). Record a `tiebreak_used` / `tiebreak_skipped` flag in the step trace.

### 2c. Model + cost
- Use a **cheap, fast** model for the tiebreaker only — inject it as a separate callable (e.g. `tiebreak_llm`) with its own model string; default to your cheapest configured tier (e.g. a `-mini` sibling of gpt-5.6). Keep it OUT of the three core GPT-5.6 calls — those stay separate and unchanged.
- Budget: tiebreaker fires only on ties, one call, small `max_tokens` (~300), low temperature. Must fit inside the existing 45s deadline; wrap it in a short `asyncio.wait_for`.

### 2d. Prompt (tiebreaker system — plain, no jargon leakage)
> You compare how people talk. Given a learner's English sample and short descriptions of several creators who scored nearly equal on a style match, pick and rank the 3 whose WAY OF TALKING best fits the learner — sentence structure, pacing, how much they question, how direct or warm they are. Use only the descriptions provided. Return JSON `{ranked_ids:[...3], reasons:[...3]}`, each reason one plain sentence. Do not mention vectors, embeddings, or scores.

---

## Tests + housekeeping
- Unit-test the centering transform (query + corpus use the same centroid) and the deterministic gate (tie vs no-tie) with a fake `tiebreak_llm`.
- Keep the two-tier honesty labels and the "9-axis rubric, humor not measured" note.
- Re-run the full suite; all green. Bump `dataset_version`.

## Do NOT
- No `web/` edits. No score/probe fudging. Do not merge the tiebreaker into the three core GPT-5.6 calls — it is a separate, gated, cheap step.
