# "Why You Two Are Alike" Panel — Spec

*2026-07-19. Codex-ready. Replaces the single-sentence "why" with an evidence panel. This is the
highest-value screen in the demo: it is what turns "match by how you talk" from a gimmick into
"wait, how does it know that?"*

---

## 1. The problem with the current "why"

Today `why` is one sentence describing only the learner (`prompts.py` `WHY_SYSTEM`). It states a
verdict. A judge reads it as generic GPT flattery and assumes there is no real matching engine
underneath.

**The fix: show the receipts, not the verdict.** Name 2 to 3 concrete things the learner and the
creator *both* do, each one the user can actually hear in their own clip and in the creator's video.
Credibility comes entirely from these being specific and checkable, not warm and vague.

## 2. What the panel shows (per match card)

1. **Your speaking style (learner chips):** 3 short plain-word tags derived from the learner's own
   clip. Example: `asks before answering` · `softens with "kind of"` · `tells it as a story`.
   These are the same for all three cards (they describe the learner, shown once at the top of
   results OR repeated small on each card, design's call).
2. **Where you two line up (the evidence):** 2 to 3 short lines, each naming one thing *both* do.
   Plain words. Checkable. Example:
   - `You both open with a question, then answer it.`
   - `You both keep sentences short and add one idea at a time.`
   - `You both soften strong claims instead of stating them flat.`
3. **One warm human line (optional closer):** a single friendly sentence so it does not read like a
   checklist. Example: `Copying them should feel natural, not like putting on a costume.`

The card keeps: avatar, name, role, tier chip (resemblance word, never a number), `Visit their
channel`. The evidence lines replace the old single `why` sentence.

## 3. Plain-language rule (hard requirement)

Every trait line must pass all three:
- **Concrete:** names a specific move ("opens with a question"), not a mood ("thoughtful").
- **Checkable:** the user could hear it in both clips.
- **Plain:** a 12-year-old gets it. No "hedging", "rhetorical", "syntax", "discourse".

If a line is abstract or flattering-but-vague, it has slipped back into horoscope territory. Cut it.

## 4. Legal guardrails (unchanged, carry verbatim)

- The evidence is built from **our own creator descriptors** (`role`, `source_note`) plus the
  learner's translated text. **Never** quote or paraphrase the creator's actual words.
- Never claim to have watched the creator or to have proof. Frame as resemblance, not measurement.
- No accent, voice, identity, or "scientifically proven" claims.

## 5. GPT-5.6 prompt spec (replaces `prompts.py`)

The model receives the learner's English translation + the matched creator's descriptors, and
returns **structured JSON** (so the UI binds fields, not a blob).

### System prompt (draft)
```
You explain, in plain everyday words, why a language learner will find a specific English speaker
easy to copy. You are given (1) an English translation of the learner talking, and (2) short
human-written notes about how the English speaker talks. Never quote or guess the speaker's actual
words; use only the provided notes. Never mention accent, voice, identity, topic, or any proof or
science.

Return JSON with:
- "learner_traits": 3 tags, each 2 to 4 words, describing HOW the learner talks (sentence shape,
  how they open, how they connect ideas, how firm or soft they are). Plain words only.
- "shared_lines": 2 or 3 short sentences, each naming ONE concrete thing BOTH the learner and the
  speaker do, phrased "You both ...". Must be checkable by ear. No jargon.
- "closer": one warm sentence, at most 20 words, about copying them feeling natural.

Every line must be understandable by a 12-year-old. Banned words: rhetorical, hedging, syntax,
discourse, idiolect, cadence, register. No em dashes anywhere.
```

### Input (unchanged shape, still `why_input`)
```json
{ "learner_english_translation": "...", "creator": { "name": "...", "role": "...", "source_note": "..." } }
```

### Output the UI binds
```json
{
  "learner_traits": ["asks before answering", "softens with 'kind of'", "tells it as a story"],
  "shared_lines": [
    "You both open with a question, then answer it.",
    "You both keep sentences short and add one idea at a time."
  ],
  "closer": "Copying them should feel natural, not like putting on a costume."
}
```

### `/match` response change
Each match item's `why` (string) becomes `why` (object with the three fields above). The three
`learner_traits` are identical across the three matches (they describe the learner); `shared_lines`
and `closer` differ per creator. Small change: same call site, richer return.

## 6. Fallback (keep the graceful path)

If the GPT-5.6 call fails or returns malformed JSON, show a neutral one-liner instead of erroring
the whole match, e.g. `This speaker talks in a way that should feel familiar to you.` Never block
the three cards on the "why".

## 7. Why this wins the judging

- **Technological Implementation:** the panel makes the cross-language match *legible*. "You spoke
  Korean, here is what you both do in English." That is the hard, non-obvious part, shown not told.
- **Design:** one clean "aha" moment. Ideally the design pairs the learner chips and the shared
  lines so the eye sees the overlap.
- **Quality of Idea:** the evidence is the proof that the clever inversion actually works.
