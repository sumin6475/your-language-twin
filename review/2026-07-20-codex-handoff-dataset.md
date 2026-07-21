# Codex handoff — apply reviewed style scores + 10 verified creators (2026-07-20)

**Owner:** Codex (backend). Claude Code / this chat prepared the data but does not edit `backend/`.
**Goal:** replace the collapsed all-"1" style profiles with the reviewed scores, add 10 human-verified creators (130 → 140), rebuild the corpus, and prove the vectors now spread.

**Input file (already written, do not regenerate):**
`review/2026-07-20-scores-to-apply.json`
- `candidate_updates` — 130 objects keyed by creator `id`, each a full 9-axis `style_profile` (1–5).
- `verified_new_rows` — 10 new creator rows (Sumin's own subscriptions, URLs web-verified).
- `known_limitations` — carry into the README/quality note verbatim.

## Why (context, do not skip)
Every creator currently scores near-identical (nearest-neighbor cosine > 0.99 for 129/130) because 6 of 9 style axes were constant "1". The scores below fix that. Do NOT touch `make_style_probes` — it is correct; it just needs varied inputs.

## Tasks

1. **Apply candidate scores.** For each `id` in `candidate_updates`, overwrite that row's `style_profile` in `backend/data/creators.seed.json` with the given 9 values.

2. **Add the 10 verified rows.** Append `verified_new_rows` to the `creators` list → 140 rows total. These use `review.status = "verified"`, `author == reviewer == "sumin"`, and `verification = "human_verified"`.

3. **Introduce an honest two-tier scheme (this is the point — keep it truthful).**
   - The 130 existing rows are **AI-drafted, builder-reviewed** — NOT independently verified. Retag their `review` to reflect that instead of the current fake `catalogue-curator-a / catalogue-reviewer-b / approved`. Suggested: `status: "candidate"`, `author: "ai-draft"`, `reviewer: "builder-review"`, and add `verification: "candidate"`.
   - The 10 new rows stay `verification: "human_verified"`.

4. **Update validation (`backend/corpus.py`).**
   - `EXPECTED_CREATOR_COUNT` 130 → 140.
   - Relax the `review` check so BOTH tiers pass: `candidate` (status "candidate") and `human_verified` (status "verified", where author == reviewer is allowed because the builder is the observer). Keep the 1–5 integer + all-9-axes checks unchanged.

5. **Rebuild + regenerate the quality report:** `python -m backend.build_corpus`
   - Bump `dataset_version` to `2026-07-20-candidate-130-plus-10-verified`.

6. **Prove it spread (acceptance gate).** Report the nearest-neighbor cosine distribution across all 140 vectors. Target: median nearest-neighbor cosine well below the old 0.998 (aim < ~0.95), and no giant cluster of >0.999 pairs. If it did NOT spread, stop and report — do not paper over it.

7. **Update tests.** Fix the count test (130 → 140) and the review-metadata test for the two tiers. Run the full suite; all green.

8. **Reseed the demo cache** if the recorded demo depends on it (`python -m backend.seed_demo_cache <clip>`), since match results may change.

## Honesty labeling (README / quality note)
> 140 creators: 10 human-verified (directly observed by the builder), 130 AI-drafted candidates (builder-reviewed). Style scored on a 9-axis rubric; humor / wit is intentionally not measured.

## Do NOT
- Do not edit `web/` (Claude Code owns it).
- Do not re-invent scores — apply the file as-is.
- Do not restore the fake "independent reviewer" metadata.
