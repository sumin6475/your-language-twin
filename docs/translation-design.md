# Reference: Style-Preserving KO→EN Translation for Path B

> Analysis of how to adapt the translation mechanism from Sumin's own `shadowing-plus`
> repo (github.com/sumin6475/shadowing-plus) into this project's Path B pipeline
> (Korean speech → style-preserving English → style embedding → match to similar English
> creator). Produced 2026-07-18 by a 4-agent workflow (port design / stylometry / adversarial
> verification / synthesis). This is a REFERENCE doc — decisions here feed Phase 1, not the
> spike. No code was copied from shadowing-plus; only the mechanism and adaptation design.

## Background: what shadowing-plus does (the source mechanism)

`web/src/lib/pipeline/stage_4_translate.ts` (431 lines). Direction: **English audio →
Korean subtitles** (opposite of ours). Two-stage GPT-4o-mini design:
- **Stage A `profileVideo()`**: one call extracts a VideoProfile (context, genre, register,
  named entities, domain-term glosses). Explicitly instructs "do NOT default to polite —
  match the genre/audience."
- **Stage B `buildSystemPrompt()` + `translateBatch()`**: profile injected into a cached
  static system prompt teaching 8 translation principles (natural word order, register
  consistency, idiomatic discourse markers, smooth self-corrections, voice-within-voice,
  cultural refs, disambiguation, audience interjections). Batches of 20, 6 concurrent,
  6-sentence context window, output keyed by source number to survive drop/reorder.

Our direction is REVERSED and our consumer is a style-embedding model, not a human reader —
so several of its "make it fluent" principles must be INVERTED (see synthesis).

---

## SYNTHESIS (the decision)


## The synthesis in one paragraph

The three analyses agree more than they disagree, and I resolved the one real tension between them (Analysis 1 wants to build the full port; Analysis 3 says don't) in favor of Analysis 3's skepticism — because Analysis 2 supplies the mechanism proving why the port's benefit is *unproven*, not just unmeasured. My recommendation as tech lead: **No-Go on porting the machinery; Go on one prompt plus one measurement.**

## The five sections

1. **What we can reuse** — the two-stage idea and the prompt craft, honestly *not* the code (reversed direction + machine-consumer goal means the reference's "render fluent" instinct is the exact thing we invert). Keep: two-stage shape, JSON-keyed output, "don't default to fluent." Drop: smooth-the-disfluency, segment sampling, subtitle register.

2. **The adapted design** — concrete Stage A (speaker fingerprint) and Stage B (5 inverted principles) prompts, written out in full, replacing exactly `match.py:96`. Flags the sequence trap (transcribe KO, don't use Whisper's EN translation) and the clean-corpus-vs-disfluent-output mismatch for Phase 1.

3. **Does it help** — the load-bearing mechanism: `styledistance` keys hardest on exactly the features (rhythm, hedging, filler density) that plain translation destroys, so the prompt is directionally right but might do nothing if the model re-cleans. Plus the honorific ceiling (partly untranslatable, but symmetrically so). Measurement: self-retrieval MRR + blinded 2AFC + the floor/current/ceiling bracket run *first*.

4. **Minimum to build** — single prompt now, three-step gated decision path, full port only if it earns it. Cost reassurance (~$0.002–0.01/match, budget is never the constraint — measurement is).

5. **Risks** — three ways a "style-preserving" translator makes matching *worse*, with the single most-likely failure called out: **silent regression to generic register**, which fakes a good result (fluency up, discrimination down). That failure is the reason the measurement is built before the translator is trusted.

## One thing worth surfacing beyond the three analyses

`spike/README.md` already warns that **Whisper's ASR strips fillers and disfluencies before translation even runs**. That's a floor no downstream LLM prompt can recover — it strengthens the case for measuring the ceiling first, since part of the idiolect is already gone at the transcription stage, not the translation stage. I noted this in the doc's grounding footer.

The design flaw in the corpus (clean style-representative text vs. a translator now preserving disfluency) is real and I flagged it as a Phase-1 item, not a spike blocker — the honest fix is rebuilding both sides of the k-NN through the same translator.

---

## Analysis 1 — Port design (concrete prompts)

I now have full grounding: the exact `transcribe(path, translate=True)` call site in `match.py` (line 96) that I'm replacing, how the corpus English side is embedded (`styledistance`, mean-pooled chunks, in `build_corpus.py`), and the known weakness (Whisper's built-in translation flattens idiolect). This is a design task with all context gathered — I'll return the concrete design as my final response.

---

# Design: Style-Preserving KO→EN Translator for Path B

## 0. Core reframe (what changes vs the reference mechanism)

| Axis | shadowing-plus (reference) | Ours |
|---|---|---|
| Direction | EN source → KO output | **KO source → EN output** |
| Consumer of output | a **human reading subtitles** | a **style-embedding model (`styledistance`)** |
| Optimize for | comprehension, natural fluent target | **preservation of the speaker's own idiolect in English** |
| Source material | produced multi-speaker video | **one learner's spontaneous native-language monologue** |
| Profile subject | the *video* (genre/register/entities) | the *speaker* (rhetorical fingerprint) |

The single most important inversion: **their principles push toward fluent, normalized target text; ours must resist normalization.** The reference translator's Principle 4 ("drop stutter marks, render smoothly") is actively harmful to us — that stutter *is* the signal `styledistance` matches on. We keep the two-stage architecture and the batching/caching infra, but rewrite the objective.

This directly fixes the spike's stated Path B weakness (`match.py:96`, `transcribe(..., translate=True)` uses Whisper's built-in translation which "flattens tone/idiolect"). We replace that one call with a profile-then-translate LLM step.

---

## 1. What we keep from the two-stage design, and how the profile changes

**Keep:**
- **The two-stage split itself** (Stage A: one cheap profiling call → JSON; Stage B: profile injected into a cached static system prompt → translate). This is the right shape: extract a per-speaker style contract once, then translate every chunk against it consistently. Consistency across chunks matters *more* for us than for them, because our corpus creators are embedded as **one mean-pooled vector** (`build_corpus.py:161-164`) — if the translator's style drifts across our chunks, the learner's mean vector smears and k-NN degrades.
- `json_object` mode, temperature discipline, per-call usage logging, prompt caching on the static system message, output keyed by chunk index to survive reorder/drop.

**Drop / neutralize:**
- Sampling "first-30 + last-30 segments." A 3-min monologue is ~450–600 words — small enough to profile on the **entire** transcript. No sampling.
- Genre/register-**for-subtitles**. We don't care what politeness level a Korean reader expects; we care what the speaker's rhetoric *is*.
- Principle 8 (audience interjections) — no audience in a monologue. Drop.

**The profile changes from "VideoProfile" to "SpeakerFingerprint."** Instead of extracting genre + subtitle register + named entities + domain glosses, it extracts the axes that `styledistance` actually discriminates on — which we can read straight off our own corpus definitions (`build_corpus.py:51-92`): hedging density, sentence length/rhythm, imperative vs. reflective mood, filler habits, persuasion move, directness, tangentiality. The profile's job is to name these so Stage B can *reproduce them in English* rather than launder them away.

### Stage A prompt — `buildFingerprintPrompt()` (one call, whole transcript, temp 0.2, json_object)

**System:**
```
You are a sociolinguist analyzing HOW a person speaks, not what they say. You will
receive a raw Korean speech transcript of one person talking spontaneously (self-talk /
monologue). Extract that speaker's RHETORICAL FINGERPRINT — the stable, content-independent
habits of their speaking style — as JSON.

This fingerprint will be used to translate their speech into English while PRESERVING these
habits, so downstream software can match them to an English speaker with a similar style.
Do NOT judge, correct, or improve the speech. A rambling, hedged, or repetitive speaker
must be described as rambling, hedged, and repetitive. Fidelity to their real style is the
only goal.

Return ONLY this JSON object:
{
  "hedging": "<how much and how they soften claims: 'heavy — qualifies almost every claim
              with 뭔가/약간/그런 것 같아요' | 'moderate' | 'low — states things flatly'.
              Give the actual hedge words they lean on.>",
  "fillers": "<their characteristic discourse fillers and how often, e.g. '그니까/약간/뭔가
               every sentence' — name the ones to carry into English as their English
               equivalents, not to delete>",
  "sentence_rhythm": "<'long, run-on, clause-stacked with 근데/그래서' | 'short, clipped,
                       staccato' | 'mixed, builds then punchlines' — describe their actual
                       average length and how clauses connect>",
  "mood": "<dominant illocutionary posture: 'imperative/hyping' | 'reflective/wondering' |
           'analytical/qualifying' | 'narrating/storytelling' | 'persuading/rhetorical-
           questions' — pick what dominates>",
  "directness": "<'blunt, asserts and moves on' | 'circling, tangential, self-interrupting'
                 | 'hedged and tentative'>",
  "persuasion_move": "<their signature rhetorical move if any: 'numbered lists', 'rhetorical
                      questions then answers', 'contrast (X but actually Y)', 'personal
                      anecdote then lesson', 'repetition for emphasis', 'none obvious'>",
  "self_reference_stance": "<how they position themselves: 'confident I-statements' |
                            'tentative I-think/maybe' | 'impersonal/general'>",
  "named_entities": ["<proper nouns to keep verbatim in romanization, if any>"],
  "register_note": "<the ENGLISH register that would sound like the SAME person: casual/
                    conversational vs formal — chosen to mirror THEM, never defaulted>"
}
```
**User:** the full Korean transcript.

Note the explicit anti-improvement instruction — the mirror image of the reference's "do NOT default to polite." Ours is "do NOT default to fluent/clean."

---

## 2. The 8 principles, rewritten to preserve idiolect

Here is the actual Stage B system prompt text. The reference's principles that *normalize* are inverted; the ones that already serve fidelity are kept and re-pointed at English output. I'll give the full revised text for the 5 load-bearing ones (2, 3, 4, 5, 6 in their numbering are where the objective flips), plus the framing header.

### Stage B system prompt — `buildTranslatePrompt(fingerprint)` (static + cached, temp 0.4, json_object)

**Header (the objective statement — this is what does most of the work):**
```
You translate spontaneous Korean speech into English. Your goal is UNUSUAL: you are NOT
producing clean, publishable English. You are producing English that a style-analysis model
will read to recognize THIS speaker's personal way of talking. So your translation must
carry the speaker's rhetorical fingerprint across into English, even when that means the
English is less polished than a professional translator would write.

Translate MEANING faithfully, but preserve STYLE aggressively. When "the natural English
way to say it" and "the way THIS speaker would say it" conflict, choose the speaker.

This speaker's fingerprint:
  hedging: {{hedging}}
  fillers: {{fillers}}
  sentence rhythm: {{sentence_rhythm}}
  mood: {{mood}}
  directness: {{directness}}
  persuasion move: {{persuasion_move}}
  self-reference: {{self_reference_stance}}
  target English register: {{register_note}}
```

**Principle 1 — Preserve sentence rhythm and clause structure, don't tidy it.**
> Match the speaker's sentence length and clausal shape. If they stack clauses into long run-on sentences joined by 근데/그래서/그리고, render one long English sentence joined by "but / so / and" — do NOT break it into clean short sentences. If they speak in short clipped fragments, keep English fragments. Sentence rhythm is a primary style signal; standardizing it erases the speaker. This directly overrides the usual instinct to restructure into idiomatic English word order — restructure only as much as grammar forces, no more.

*(This is the deliberate inversion of the reference's Principle 1, "restructure freely; don't preserve source structure.")*

**Principle 2 — Keep hedges and fillers; translate them, never delete them.**
> Discourse fillers and hedges (그니까, 약간, 뭔가, 그런 것 같아요, 막) carry the speaker's style and MUST survive into English as their natural English equivalents — "like," "kind of," "I mean," "sort of," "I guess," "you know" — matched to the density in the fingerprint. A speaker who hedges every clause must hedge every clause in English. Do NOT clean these up. Do NOT collapse three hedges into one. Under-hedging a hedger is a translation error here, not an improvement.

*(Fuses the reference's Principle 3 with a hard anti-deletion rule and density-matching.)*

**Principle 3 — Preserve self-corrections and false starts as light disfluency.**
> When the speaker restarts, corrects themselves, or trails off ("아니 그게... 그니까 내 말은"), keep a light English trace of it ("no wait— I mean," "like, the thing is—"). Do not silently smooth it into a single clean statement. Render it readably, but leave the disfluency visible: it is exactly the idiolect signal we are matching on. (Do not invent disfluency that isn't there — mirror, don't manufacture.)

*(This is the **direct reversal** of the reference's Principle 4, which said "drop stutter marks, render the intended meaning smoothly." For a human subtitle reader, smoothing helps. For our style embedder, it destroys signal. This principle is the single most important behavioral difference from the reference mechanism.)*

**Principle 4 — Preserve the persuasion move and mood, not just the content.**
> If the fingerprint names a rhetorical move — rhetorical questions, numbered points, contrast framing ("X, but actually Y"), repetition for emphasis, anecdote-then-lesson — reproduce that MOVE in English, not just the propositional content. If they ask a rhetorical question then answer it, keep it as a question then an answer; do not flatten it into a declarative. If they repeat a word three times for emphasis, repeat it three times in English. The mood in the fingerprint ({{mood}}) sets the default illocutionary posture; keep imperatives imperative, wondering tentative.

*(Generalizes the reference's cultural/idiomatic Principle 6 up to the rhetorical level, which is our actual matching unit.)*

**Principle 5 — Register mirrors the speaker, consistently across every chunk.**
> Use the English register in the fingerprint ({{register_note}}) and hold it identical across all chunks — no drift toward formality in later chunks, no drift toward slang. Because all of this speaker's chunks are averaged into one style vector downstream, register drift between chunks blurs their fingerprint. Consistency across the whole monologue is as important as correctness within a chunk. Never default to formal, polished, or "professional" English unless the speaker themselves is formal.

*(Keeps the reference's Principle 2 "register consistency / no drift," but re-motivates it by the mean-pooling in our corpus and forbids the fluency default.)*

**Kept largely as-is (fidelity-serving), re-pointed at English output:**
- **Named entities** → keep verbatim in standard romanization (from the fingerprint list).
- **Disambiguation via context** → use surrounding chunks (reference-only context window) to pick the intended sense; prefer the reading that fits *this* speaker's topic over the dictionary default.
- **Voice-within-voice** → when the speaker quotes someone or shifts into inner speech, mark it with English quotation conventions.

**Output format instruction (kept from reference):**
```
Input is a JSON array of Korean chunks: [{"n": 0, "ko": "..."}, ...].
Return JSON: {"0": "<english>", "1": "<english>", ...}, one entry per input "n",
same count, keyed by "n" so nothing is dropped or reordered.
```

**Temperature note:** reference used 0.3 for translation. We nudge to **0.4** — we *want* the model to reproduce non-standard rhythm/disfluency, and slightly higher temperature reduces its regression-to-clean-English tendency. Still low enough to stay faithful to meaning. Worth a quick A/B during integration (0.3 vs 0.4) judged by whether the learner's English probe lands on the right corpus creator.

---

## 3. Where this runs in the pipeline

It replaces exactly one thing: the `transcribe(audio_path, translate=True)` call at **`match.py:96`** (and, in the product, the equivalent step in the Railway worker per `CLAUDE.md:74`). Everything downstream — `styledistance.encode(...)` and `knn(...)` — is unchanged.

**Product pipeline (Railway Python worker, never Vercel per `CLAUDE.md:106`):**

```
1. Groq Whisper TRANSCRIBE in Korean (translate=False)   ← already have this
   client.audio.transcriptions.create(...)  → korean_transcript
   [NOTE: we now use the KO transcription, NOT Whisper's EN translation.
    Whisper's built-in translate is what flattened idiolect in the spike.]

2. Chunk korean_transcript into ~20-sentence chunks (mirrors reference batch size).
   A 3-min monologue → typically 1–2 chunks. Keep chunk boundaries at sentence ends.

3. STAGE A — one LLM call (Claude via Vercel AI Gateway, or gpt-4o-mini):
   buildFingerprintPrompt() over the FULL transcript → SpeakerFingerprint JSON.
   Cache/log usage.

4. STAGE B — one (rarely 2) LLM call(s):
   buildTranslatePrompt(fingerprint) as cached static system prompt +
   the chunk array as user message → {"0": en, "1": en, ...}
   Concatenate in "n" order → english_text.
   (Reference used 6-concurrent batches for long videos; at 1–2 chunks we just do
    one call. The concurrency/CONTEXT_WINDOW machinery only matters if a sample runs long.)

5. styledistance.encode([english_text], normalize_embeddings=True) → query vector
   (unchanged; same model the corpus was built with in build_corpus.py:155,162)

6. cosine k-NN over corpus.enstyle (unchanged, knn() in match.py:64)

7. delete raw audio + korean_transcript per privacy rule (CLAUDE.md:107).
```

**Model choice:** default to Claude via Vercel AI Gateway (already owned, `CLAUDE.md:42`) — Claude Haiku-class is ample for this and cheap. gpt-4o-mini via OpenAI is a fine drop-in as the reference used it. Put the model behind the Gateway so you can swap without code changes. **Chunking note:** embed on the concatenated full English text (matching how `match.py:96-99` embeds the whole translation as one string), not per-chunk, so the learner's query vector is built the same way regardless of chunk count.

**One integration subtlety worth flagging:** our corpus English side (`build_corpus.py`) is built from *clean written* style-representative excerpts and *formal speech transcripts*. If our new translator preserves heavy disfluency but the corpus vectors were built from clean text, the disfluency could push the learner's vector into empty space rather than toward a matching creator. Two mitigations: (a) the `CONVERSATIONAL_CREATORS` seeds already include hedged/filler-heavy styles (the "Casual explainer," "Reflective storyteller" entries at `build_corpus.py:52,62`), which is the right direction; (b) longer-term, rebuild the corpus by running the **same** style-preserving translator over creators' real transcribed speech so both sides of the k-NN share one representation. Note this for Phase 1; not blocking for the spike.

---

## 4. Cost per match and monthly fit

**Per match, one ~3-min sample (~500–700 Korean words ≈ ~1,000–1,400 tokens):**

| Call | Input tokens | Output tokens |
|---|---|---|
| Stage A (fingerprint): system ~350 + transcript ~1,300 | ~1,650 in | ~250 out (JSON) |
| Stage B (translate): system ~700 (cached) + chunk array ~1,400 | ~2,100 in | ~1,600 out (English) |
| **Total** | **~3,750 in** | **~1,850 out** |

**With gpt-4o-mini** ($0.15 / 1M input, $0.60 / 1M output):
- Input: 3,750 × $0.15/1M ≈ **$0.00056**
- Output: 1,850 × $0.60/1M ≈ **$0.00111**
- **≈ $0.0017 per match** (~one sixth of a cent). Groq Whisper is free tier.

**With Claude Haiku-class via Gateway** (roughly $0.80 / $4 per 1M, order-of-magnitude): input ~$0.003 + output ~$0.0074 ≈ **~$0.01 per match**. Prompt caching on the Stage B static system prompt cuts the input side further across a session.

**Monthly fit at alpha volume:**
- At **~$0.002/match (gpt-4o-mini)**: the entire $10/mo budget = **~5,000 matches/mo**. Alpha is dozens to low-hundreds → effectively **$0**.
- At **~$0.01/match (Claude)**: $10/mo = **~1,000 matches/mo**. Still far above alpha volume.

**Verdict: fits comfortably, with 1–3 orders of magnitude of headroom** at either model choice. The LLM translation cost is negligible next to the already-owned fixed infra (Vercel Pro, Railway $5, Groq free tier per `CLAUDE.md:136`). Groq's free-tier *rate limits*, not dollars, are the only realistic ceiling at alpha, and they're generous for one 3-min transcription per match.

---

**Relevant files:**
- `/Users/jadekim/Documents/02 Building Projects/Your Ideal Rolmodel/spike/match.py` — replace the `translate=True` branch (line 96) with Stage A + Stage B; downstream `encode`/`knn` unchanged.
- `/Users/jadekim/Documents/02 Building Projects/Your Ideal Rolmodel/spike/build_corpus.py` — English corpus side (`styledistance`, mean-pooled, lines 155–164); note the clean-text-vs-disfluency representation mismatch for Phase 1.
- `/Users/jadekim/Documents/02 Building Projects/Your Ideal Rolmodel/CLAUDE.md` — pipeline placement (worker-only, lines 74/106), model default (Claude via Gateway, line 42), budget (line 136).

---

## Analysis 2 — Stylometry: what survives translation

This is a research/advisory question about translation and stylometry for a style-matching system. There's no codebase to inspect — the task is to deliver rigorous, concrete analysis. Let me answer directly.

Note: styledistance is a real published model (Patel et al., 2024) — a style-embedding model trained with contrastive learning on ~190k synthetic near-paraphrase pairs designed to isolate style from content. I'll ground my answer in what it actually keys on.

---

# What a Korean→English translation must preserve for style matching to work

## Framing: where in the pipeline style dies

Your pipeline is `KO speech → ASR → MT → English text → styledistance embedding → NN search`. Style attrition compounds at three stages, but the MT stage is where it's both largest and most controllable:

- **ASR** strips prosody, disfluency timing, and often auto-punctuates (imposing sentence boundaries the speaker didn't make — this alone destroys sentence-rhythm signal).
- **MT** is the dominant loss: it regresses every speaker toward the *translator's* mean register.
- **styledistance** only sees the English string, so anything MT normalized is unrecoverable downstream.

The key asymmetry to internalize: **styledistance measures style as realized in surface English form.** It cannot key on a Korean feature that MT didn't render into an English surface feature. So the question "what survives translation" and "what does styledistance key on" collapse into one practical question: *what English surface features can we force MT to carry, that styledistance is sensitive to?*

---

## 1. Which stylistic features survive translation, and which styledistance actually keys on

Split the feature space by **whether the feature is content-anchored (travels through MT for free) or realization-anchored (MT overwrites it by default).**

**Survive translation robustly (content-anchored — MT preserves because meaning forces it):**
- **Rhetorical questions** — survive well. They're propositional structure ("Isn't that crazy?"), and MT keeps the interrogative-as-assertion because dropping it would change meaning. styledistance is sensitive to interrogative rate and to the rhetorical-question construction.
- **Metaphor / figurative density** — survives moderately. A vivid Korean metaphor usually gets translated as *a* metaphor (content-preserving), though often a flattened one. The *presence* of figuration survives; the specific vehicle and its freshness degrade.
- **Directness vs. mitigation at the speech-act level** — partially survives. Whether someone gives commands vs. suggestions is partly propositional. But see honorifics below — the Korean grammatical machinery for this is exactly what's lost.
- **Topic/domain lexicon** — survives (it's content). This is why your video-level profile helps: it's operating on the surviving channel.
- **Discourse-relational structure** — whether the speaker argues by contrast, concession, enumeration, or narrative — survives moderately because connectives carry propositional meaning.

**Do NOT survive by default (realization-anchored — MT actively normalizes):**
- **Sentence length / clause-chaining rhythm** — largely destroyed, and this is the big one. Korean is left-branching and agglutinative; a single Korean sentence with stacked connective endings (-고, -는데, -니까, -어서) maps naturally to English either as one run-on or several short sentences, and **generic MT defaults to breaking them into medium-length, uniform sentences.** A speaker whose idiolect is "long, breathless, subordinate-clause-piling" and one who is "clipped and punchy" can converge to the same English cadence. styledistance is *highly* sensitive to sentence length distribution and clause structure — this is one of its strongest keys — so losing it is a direct hit to your matching signal.
- **Hedging / mitigation markers** — mostly destroyed. Korean hedges heavily via sentence-enders and particles (-것 같다 "seems like," -거든요, -잖아요, -는데요) and MT drops these as "not meaningful" or renders them as a flat declarative. A characteristically tentative speaker becomes assertive in translation. styledistance *does* key on hedging/epistemic-stance markers ("I think," "kind of," "sort of," "maybe"), so if MT deletes them the speaker's stance fingerprint is erased.
- **Fillers / discourse markers** — destroyed by default (ASR often removes them; MT "cleans" survivors). 그니까, 약간, 뭐랄까, 이제, 진짜 are dense idiolectal markers. Their English analogs (like, I mean, you know, basically, literally, kind of) are *strong* styledistance features — filler and discourse-marker profile is one of the most person-discriminating channels in casual speech. Default MT throws this entire channel away.
- **Formality / register** — this is the most treacherous. Korean formality is grammatically obligatory (speech levels, honorifics) and has **no clean English morphological analog**, so MT collapses the whole range into a single default English register — typically "neutral-fluent-written." styledistance *is* sensitive to formality (it was trained with formal/informal as a target style axis), but MT gives it a constant, so it becomes useless for discrimination. See §3.
- **Repetition / self-correction / emphasis-by-reduplication** — destroyed. MT de-duplicates and tidies. Emphatic repetition ("진짜 진짜") and restart patterns are idiolectal; styledistance would see them (repetition, punctuation bursts) but MT removes them.

**Compact verdict table:**

| Feature | Survives default MT? | styledistance keys on it? | Net for matching |
|---|---|---|---|
| Rhetorical questions | Yes | Yes | **Usable** |
| Metaphor presence | Mostly | Weakly-moderately | Partially usable |
| Speech-act directness | Partial | Yes | Fragile |
| Sentence length/rhythm | **No** | **Strongly** | **Lost unless forced** |
| Hedging/epistemic stance | **No** | **Yes** | **Lost unless forced** |
| Fillers/discourse markers | **No** | **Strongly** | **Lost unless forced** |
| Formality/register | Collapsed to constant | Yes | **Non-discriminating** |
| Repetition/emphasis | **No** | Moderately | Lost unless forced |

The brutal summary: **the features that survive MT for free are the ones styledistance is weakest on (content-ish, figurative), and the features styledistance is strongest on (length distribution, discourse markers, hedging, punctuation/register) are exactly the ones default MT destroys.** Your matching quality is therefore almost entirely a function of how much of the second group you can force MT to carry. This is the core mechanism, and it's why the reference system's "preserve discourse markers idiomatically + preserve voice-within-voice" principles are the right lever.

---

## 2. Prompt techniques to preserve the speaker's rhetorical fingerprint

The goal is to shift the LLM from **communicative translation** (its default: convey meaning in fluent target-register English) to **stylistic transliteration** (preserve the speaker's realization choices, accepting reduced fluency). Concrete, mechanism-tied techniques:

**(a) Give it a license to be disfluent.** The single most important instruction, because the model's RLHF prior fights you here:
> "This translation feeds a stylistic-analysis system, NOT a human reader. Fluency is NOT the goal — faithful reproduction of the speaker's rhetorical habits is. Preserve hedges, fillers, false starts, and repetition even when they make the English less polished. Do not clean up, tighten, or make the English more 'professional' than the Korean."

Without an explicit anti-fluency license, the model silently normalizes.

**(b) Constrain sentence segmentation explicitly** (protects the strongest styledistance key):
> "Preserve the speaker's sentence boundaries and clause-chaining. If the speaker runs three ideas into one long chained sentence, keep it as one long English sentence (use commas, dashes, 'and… and…'). If they speak in short fragments, keep fragments. Do NOT split long sentences into tidy short ones or merge short ones. Match roughly one output sentence per Korean sentence-final ending."

**(c) Map discourse markers idiomatically rather than deleting them** (this is the reference system's move — operationalize it):
> "Render Korean discourse markers and fillers as their natural English equivalents, preserving their frequency: 그니까→'I mean'/'so', 약간→'kind of'/'like', 뭐랄까→'how do I put it', 진짜→'literally'/'seriously', 이제→'now'/'so', 아 근데→'oh but'. Keep them at the SAME density the speaker uses them. Do not omit a filler because it seems unnecessary."

The frequency-matching instruction matters more than the specific mapping, because styledistance keys on marker *rate*.

**(d) Preserve epistemic stance / hedge strength as a scalar to hit:**
> "Match the speaker's certainty level. -것 같아요 → 'I think' / 'I feel like' / 'seems like' (keep the hedge — do NOT convert to a flat assertion). -잖아요 → 'you know' / 'right?' (appeals to shared knowledge). -거든요 → '...you see' / '...'cause'. If the speaker sounds tentative, the English must sound tentative."

**(e) Voice-within-voice tagging** (the reference system's principle — implement as explicit register-switch preservation):
> "If the speaker shifts register — quoting someone, mimicking, being sarcastic, dropping from polite to casual — mark that shift in the English (e.g., register drop, mock-formality, air-quotes tone). Do not flatten all speech to one register."

**(f) Feed the video-level profile as a register anchor**, so the model has a target other than its own default:
> "Speaker profile: [genre: casual vlog / register: informal-spoken / domain: skincare]. Translate as informal spoken English in this domain, NOT as written prose."

**(g) Few-shot with contrastive (style-erasing vs. style-preserving) pairs.** This is the highest-leverage technique because it *shows* the boundary rather than describing it. Example pairs (Korean gloss → two translations):

*KO:* "약간… 뭐랄까, 이게 진짜 좋은데 근데 좀 비싸긴 해요."
- ❌ Style-erasing (default MT): *"This is genuinely good, but it is somewhat expensive."*
- ✅ Style-preserving: *"It's kind of… how do I put it, it's like really good, but, I mean, it is a bit pricey though."*
- *Why:* preserves 약간→"kind of", 뭐랄까→"how do I put it", the trailing 근데/-긴 하다 concessive hedge→"though", and the mid-sentence self-interruption. The erasing version deletes four idiolectal markers and re-segments.

*KO:* "그래서 제가 이걸 딱 발랐잖아요? 근데 딱 바르자마자 아 이거다 싶었어요."
- ❌ *"When I applied this product, I immediately felt it was the right one."*
- ✅ *"So I put this on, right? And the second I put it on — oh, this is it, I just knew."*
- *Why:* preserves 잖아요→"right?" (shared-knowledge appeal), the 딱 punch/immediacy, the quoted inner monologue "oh, this is it," and the chained rhythm. The erasing version compresses to one neutral clause and deletes the interactive "right?".

Two or three such pairs in the domain of your creators do more than any amount of instruction prose, because they calibrate the fluency/fidelity tradeoff by demonstration.

**(h) Prohibit specific normalizations** the model does reflexively:
> "Do NOT: upgrade contractions to full forms, replace 'kind of/like' with precise adverbs, convert questions-as-emphasis into statements, merge repeated words, or add connectives the speaker didn't use."

**(i) Consider a two-pass or self-critique step within budget:** pass 1 translates; pass 2 is prompted "list every hedge, filler, and discourse marker in the Korean; confirm each appears in the English at matching frequency; restore any that were dropped." This catches the silent-deletion failure mode that single-pass prompting still leaks.

---

## 3. The fundamental ceiling: what is genuinely untranslatable

Yes, there is a hard ceiling, and honesty about it changes your architecture (see §4).

**The honorific/speech-level system is the core untranslatable idiolect.** Korean grammatically encodes, on nearly every verb, a *speech level* (하십시오체, 해요체, 해체/반말, etc.) and *subject/object honorification* (-시-, humble forms, honorific nouns/particles). A Korean speaker's idiolect includes *characteristic, non-obligatory choices* here: how they modulate 존댓말↔반말, whether they over- or under-honorify, their idiosyncratic sentence-ender palette (-네요 vs -더라고요 vs -거든요 vs -잖아요 as habitual tics). **English has no morphological analog.** You can gesture at register with lexis and contractions, but the *system* — a continuous, grammaticalized politeness/stance dimension that is one of the richest idiolectal channels in Korean — projects onto a nearly-constant point in English space.

**What you lose concretely:**
- **The sentence-ender fingerprint.** A speaker who habitually ends on -잖아요 (assertive/shared-knowledge) vs. one who ends on -것 같아요 (hedged) vs. -더라고요 (reportative/experiential) have distinct stances that English can only partially and lossily approximate. This is arguably the single densest idiolectal marker in Korean casual speech, and it's the least translatable.
- **Register-modulation as a personality signal** — some speakers code-switch 존댓말/반말 constantly for comedic or intimacy effect; that oscillation is invisible in English.
- **Particle-level emphasis and topic-marking habits** (은/는 vs 이/가 choices, 도/까지/조차 stacking) — subtle idiolect, no English surface.

**Does it matter for matching?** Partially, and here's the nuanced answer:
- It matters *less than you'd fear* for cross-lingual matching **because your English creators don't have these features either** — you're matching in English space, so a Korean-specific channel that has no English analog simply isn't part of the shared feature space. You can't match on a dimension your targets don't occupy. The honorific idiolect is lost, but it's lost symmetrically-ish: it was never going to discriminate among *English* creators.
- It matters *more than you'd hope* in that the honorific system is where a lot of the Korean speaker's stance/politeness/hedging *originates*, and when it collapses, the derived English features (hedge rate, formality) collapse too — so the loss leaks into channels that *do* exist in English. This is why §2(d) forcing hedge preservation is worth the effort: you're recovering the *English-expressible shadow* of an untranslatable Korean system.

So: the untranslatable core is real and unrecoverable, but the *matchable* loss is smaller than the *total* loss, because matching only needs the intersection of KO and EN feature spaces. Your job is to maximize the faithful projection onto that intersection (hedging, stance, rhythm, marker density), not to mourn the honorific morphology.

---

## 4. A better architecture than translate-then-embed

Translate-then-embed is fragile precisely because it funnels a rich multilingual signal through a single lossy bottleneck (MT) and then through a monolingual measure (styledistance) that can only see what survived. Within a normal LLM budget, here are better options, in order of recommendation.

**(A) Dual-channel: structured rhetorical profile + style embedding (strongly recommended).**
Have the LLM emit, alongside the translation, a **language-neutral structured rhetorical profile** computed *from the Korean source* (so it's measured before MT loss), on axes that are cross-lingually comparable and that you also compute for your English creators. Concretely, a fixed schema of scalar/categorical features:
- sentence-length distribution (mean, variance, % long-chained)
- hedging rate + dominant hedge type (epistemic / mitigating / none)
- discourse-marker density + top markers
- rhetorical-question rate
- directness (imperative/assertion vs. suggestion/question)
- figurative density
- register (formal↔casual, spoken↔written)
- stance (assertive / tentative / reportative)
- interactivity (addresses audience? rhetorical "right?" appeals?)
- narrative vs. expository vs. argumentative dominant mode

Compute the **same schema for every English creator** (run the same LLM extractor on their transcripts). Now match in this **explicit, language-neutral profile space**, either instead of or (better) *alongside* the styledistance embedding via a weighted combination / late fusion. 

Why this beats translate-then-embed on the mechanism:
- The profile is extracted **from the source language**, so features like hedge rate and sentence rhythm are measured *before* MT destroys them — you route around the bottleneck for exactly the features MT kills.
- It's **interpretable and debuggable** — you can see *why* two people matched, and audit which axes drive it, which a 768-dim opaque embedding can't give you.
- It's **honorific-aware by design** — you can have the extractor map the Korean speech-level/ender pattern *directly onto the stance/formality axes*, capturing the English-expressible shadow of the untranslatable system without routing it through MT at all.
- styledistance still contributes the fine-grained lexical/syntactic texture the coarse profile misses. Late-fusion gets both.

The main cost is **calibration**: an LLM scoring Korean and English on the same rubric may apply the rubric slightly differently per language (rater drift). Mitigate by (i) anchored rubrics with concrete examples per axis, (ii) forcing scalar outputs with defined endpoints, (iii) validating on a few bilingual creators or back-translation consistency checks.

**(B) Keep styledistance but embed a style-faithful translation, and validate the translator, not just the matcher.** If you stay single-channel, the leverage is entirely in §2. Add a **verification metric**: after translating, compute the profile of §4A on *both* the Korean source and the English output and check they agree (hedge rate preserved? length distribution preserved?). Reject/re-translate when the translation flattened the profile. This turns "did MT erase style" from an invisible failure into a measurable, gated one. Cheap and high-value even if you never build full dual-channel.

**(C) Multilingual style embedding to skip MT entirely (best if it exists for your data, but riskier).** If a multilingual style-embedding model covering Korean is available/trainable, embed the Korean directly and match against English creators in a shared multilingual style space — no MT bottleneck at all. The catch: styledistance itself is English-trained, and cross-lingual *style* alignment (as opposed to semantic alignment, which multilingual encoders do well) is not guaranteed — most multilingual encoders align on *content*, which is the opposite of what you want. So this is only better if the embedding is specifically style-contrastive *and* multilingual; otherwise it silently matches on topic. I'd treat this as a research bet, not the default.

**Recommendation:** Ship **(A) dual-channel with late fusion**, using the §2 prompt discipline for the translation half and the §4B verification gate to protect it. It routes around the MT bottleneck for the highest-value, most-MT-fragile features (rhythm, hedging, marker density, the honorific shadow), keeps styledistance for texture, and is interpretable enough to debug matches — all within an LLM-call budget you're already paying for the translation.

---

**One-line synthesis:** styledistance can only match on English surface features that survived MT; the features it keys on hardest (sentence rhythm, hedging, discourse-marker density, register) are exactly the ones generic MT destroys and the Korean honorific system can't fully export — so the fix is (1) prompt MT to preserve realization over fluency with contrastive few-shots and a frequency-matching mandate, and (2) extract a language-neutral rhetorical profile *from the Korean source* and match on it alongside the embedding, routing around the bottleneck for the features that die inside it.

---

## Analysis 3 — Adversarial verification & risk

This is a pure analysis/advisory task. The user (a skeptical ML evaluation lead persona) wants me to pressure-test a plan. No files to read, no code to write. Let me answer directly and adversarially.

Let me think carefully through each part before writing.

**The pipeline:** Korean speech → translate to English → embed with English style model → k-NN against English creators. Goal: match a Korean-speaking learner to a stylistically similar English creator to shadow.

**The proposed change:** upgrade the translation step from (presumably) a plain MT/LLM translation to a "style-preserving LLM translator" with a speaker profile + principled batch translation, ported from another project.

Let me reason through each question.

---

**Q1: How to measure MATCH QUALITY improvement (not translation quality)**

Key distinction: translation quality (BLEU, fluency, adequacy) is NOT the target. The target is whether the downstream match is better. The chain is translation → embedding → k-NN → match. So the measurement must be at the match/embedding level, not the translation level.

Ground truth problem: style similarity is subjective, no labels. But we have a few bilingual samples. The trick: a bilingual speaker who ALSO produces English natively is the ground truth generator. If a learner has both Korean content AND English content (that they wrote/spoke), then the "true" English style is their own English. So:

- **Anchor test / self-retrieval:** For each bilingual person, take their Korean speech, translate it (variant A = plain, variant B = fancy), embed, and measure distance to an embedding of THAT SAME PERSON's genuine English content. The translation that lands the person closer to their own real English embedding is preserving style better in a way that matters for matching. This is a concrete, label-free ground truth because self-identity is objective even if "style" is subjective.

- **Metric options:**
  - Rank of self among a pool: build a gallery of N English creators + the person's own English. Query = translated Korean. Metric = rank of the person's own English content in the k-NN list (should be near top if style preserved). Mean reciprocal rank (MRR) or recall@k across the handful of bilingual samples. This is the cleanest metric.
  - Or cosine distance to self-English vs. distance to a random creator (margin).

- **Control:** The plain/current translation is the control. Also add two crucial baselines: (a) embedding the person's genuine English directly (upper bound / ceiling — how good could matching be if translation were perfect), and (b) direct Korean embedding (the already-known-bad floor). This brackets the achievable gain. If fancy translation barely moves the needle between plain-translation and the English-ceiling, there's little headroom to buy.

- **Also test match STABILITY, not just self-retrieval:** does the top-1 matched creator change between plain and fancy? If the matches are identical, the fancy translation is not affecting the decision at all → no point. If they change, which is "better" — judged by blinded human preference (below).

- **Subjective ground truth via blinded human judgment:** since style similarity is ultimately subjective, run a small triangulation/2AFC. Show a bilingual friend the learner's Korean clip (they understand both) and two candidate English creators (top-1 from plain vs top-1 from fancy), ask "which of these two English creators sounds more like the same kind of speaker?" Blind to which pipeline produced which. Count wins. With a handful of samples this is n≈10-20 judgments — cheap, and it directly measures the actual product goal.

So the design: MRR/recall@k on self-retrieval (objective proxy) + blinded 2AFC on match preference (subjective truth) + English-direct ceiling and Korean-direct floor as brackets.

**Q2: Confounds that make fancy translation look better/worse than it is**

- **Profile content leakage → embedding bias:** if the speaker profile injects topic/content/named entities ("talks about startups, K-pop, lives in Seoul") into the translation, the English embedding may cluster on CONTENT not STYLE. If the English style model is not purely stylometric (most sentence embedders encode topic heavily), you'd match on shared topics, which could look like better matching but is measuring the wrong thing. Worse: if the SAME profile text or its phrasings appear across a person's samples, you get artificially high self-consistency that doesn't generalize to matching against strangers.
- **Regression to generic register:** LLM translators tend to "clean up" and standardize. If the learner has a scrappy, disfluent, idiosyncratic style, the LLM smooths it into fluent generic English → collapses everyone toward the mean → embeddings get closer together → self-retrieval margins shrink AND everyone matches the same "clean" English creators. This can make fancy look WORSE on discrimination while looking better on fluency.
- **Sample too short:** style embeddings are high-variance on short text. A handful of short clips means the between-person variance is swamped by within-person noise; you can't distinguish pipeline effect from sampling noise. Any measured "improvement" may be within noise.
- **Evaluation-on-training leakage:** if the profile is built from the same clip you then translate and match, the profile "knows" the answer. Must build profile on held-out samples of the person, evaluate on different samples.
- **Prompt/LLM version confound:** the fancy pipeline may just be a newer/bigger model, more tokens, or better instructions — the gain may come from "used GPT-4o vs GPT-3.5" not from the profile+principles mechanism. Hold the base model fixed across A/B.
- **Human judge not blind / knows Korean-English cultural cues:** bilingual judges may unconsciously prefer the translation that "sounds more Korean-inflected" as more authentic, biasing toward over-preservation regardless of match quality.
- **Cherry-picking / tiny-n multiple comparisons:** with 3-5 people and several metrics, something will look better by chance.

**Q3: Risk that style-preserving translation makes matching WORSE**

- **LLM's own stylistic tics injected uniformly:** the translator model has a signature (em-dashes, "it's not X, it's Y", tricolons, hedging). Applied to everyone, this adds a common-mode style vector to all translations → reduces between-speaker variance → k-NN discriminates worse. This is the exact opposite of what they want and is a very real risk. The plain translator has tics too, but a heavily-prompted "style" translator may impose MORE structure.
- **Over-preservation → out-of-distribution English:** forcing Korean syntax/discourse structure (topic-comment, sentence-final softening, honorific register, subject drop rendered awkwardly) into English produces English no native English creator actually writes. The translated vector lands in an empty region of the English-creator manifold → nearest neighbor is arbitrary/unstable → matches to whoever is closest to "weird," not closest in style. The plainer translation, by normalizing to fluent English, may actually land in-distribution and match more sensibly. So there's a real tension: fidelity to idiolect vs. living in the English embedding space the creators occupy.
- **The style model may not even encode the preserved features:** if the English style embedder was trained on native English register, the Korean-derived stylistic features it's asked to preserve may be projected out or map to noise. Effort spent preserving them is wasted or harmful.
- **Instability = worse UX:** even if average match quality is neutral, higher variance in matches (person gets a different shadow-target on re-run) is a product regression.

**Q4: MVP — full port vs single prompt, given $10/mo + alpha (you + few bilingual friends, no accounts)**

At this scale the full profile+principles+batch mechanism is over-engineered for what the spike can even measure. With n=3-5 people you cannot statistically distinguish a full mechanism from a single good prompt; the measurement error dwarfs the mechanism delta. The batch/principled machinery buys consistency at scale and cost efficiency at volume — neither matters at alpha. Porting it is real engineering + maintenance surface for a hypothesis you haven't validated is even directionally true.

Recommended MVP: a single well-crafted style-preserving prompt (one clear instruction to preserve rhetorical patterns, pacing, hedging, directness, sentence rhythm; explicitly forbid "improving" register; no separate profile artifact), run as the B arm against the current plain translation as A. Same base model both arms. Measure with the self-retrieval MRR + blinded 2AFC above. Total cost: a handful of LLM calls, well under budget.

Only port the full profile+principles mechanism if: (a) the single-prompt B arm beats A on both objective margin and blinded preference, AND (b) you observe the specific failure the profile is designed to fix (single-shot translation losing consistency across a long/multi-clip sample). If single-prompt already captures most of the English-direct ceiling, the full port has no headroom to justify it.

**Go/No-Go:**

- No-go on porting the full profile+principles mechanism now.
- Go on a tiny, tightly-controlled spike: single style-preserving prompt as B, current as A, same base model, with the English-direct ceiling and Korean-direct floor brackets, self-retrieval MRR + blinded 2AFC, on your handful of bilingual friends who each have both Korean and genuine English content.
- Gate: proceed to the full port only if B measurably closes a meaningful fraction of the plain→ceiling gap AND wins blinded preference AND doesn't reduce match stability.

Actually, let me reconsider one thing — is there even headroom? The original spike found Korean-direct fails and translate-then-embed works. The critical unknown is how far translate-then-embed already is from the English-direct ceiling. That's the single most decision-relevant measurement and it costs almost nothing. Let me foreground that: **the first thing to measure isn't fancy-vs-plain, it's plain-vs-ceiling.** If plain translation already gets you 90% of the way to the English-direct ceiling on the bracket test, the entire translation-improvement effort is chasing <10% headroom and should be deferred regardless. That's the sharpest adversarial point and should lead.

Let me write this up concisely and return it as my final message. No files. The task is advisory. I'll format it clearly since it's a substantive analysis but keep it tight.

# Pressure-test: style-preserving translation for style-matching

## Lead with the decision-relevant measurement you skipped

Before fancy-vs-plain, measure **plain-vs-ceiling**. Your original spike proved two points: Korean-direct fails, translate-then-embed works. It did *not* measure how far translate-then-embed already sits from the ceiling. Establish three brackets on the same samples:

- **Floor:** embed Korean directly (known-bad).
- **Current:** plain translation → embed.
- **Ceiling:** embed the person's *genuine English* content directly (see Q1 for why this is available).

If plain translation already recovers most of the floor→ceiling gap, the entire "improve the translator" effort is chasing single-digit headroom and should be deferred *regardless of how good the fancy translator is*. This one bracket test — a handful of embeddings, near-zero cost — likely settles the go/no-go on its own. Run it first.

## Q1 — Measuring MATCH quality, not translation quality

Don't score the translation (BLEU/fluency/adequacy all measure the wrong thing). Score the downstream retrieval.

**Ground truth despite subjectivity — use self-identity.** Style similarity is subjective, but *"this is the same person"* is objective. Recruit bilingual friends who have **both** Korean content and *genuine, self-produced* English content (not translated). The person's real English is the label-free target for what their Korean *should* translate to, stylistically.

**Objective metric — self-retrieval rank.** Build a gallery of N English creators plus the person's own English content. Query = their translated Korean. Metric = **rank of their own English in the k-NN list**, aggregated as **MRR / recall@k** across the handful of people. The translation that ranks a person nearer their own real English is preserving match-relevant style. Report the paired delta (fancy − plain) per person, not just the mean — with n≈3–5 the per-person sign is what you read.

**Subjective ground truth — blinded 2AFC.** Take top-1 match from plain and top-1 from fancy. Show a bilingual judge the learner's Korean clip plus the two candidate English creators, blinded to pipeline: *"which creator sounds like the same kind of speaker?"* Count wins over ~10–20 judgments. This measures the actual product goal directly.

**Also check match stability / whether it even moves the decision.** If top-1 is identical between plain and fancy across your samples, the fancy translator isn't changing the output → automatic no-go on the change, whatever the translation looks like.

**Control:** current plain translation, **same base model** as the fancy arm (see Q2).

## Q2 — Confounds that fake a result

- **Profile content-leak → topic matching in disguise.** Most "style" sentence embedders encode topic heavily. If the profile injects entities/topics ("Seoul, startups, K-pop") into the translation, you match on shared content and call it style. Worse: shared profile phrasings inflate *self-consistency* without helping match strangers. Test the embedder's topic-sensitivity separately, and keep the profile stylometric-only.
- **Regression to generic register.** LLM translators "clean up." A scrappy/disfluent idiolect gets smoothed to fluent generic English → everyone collapses toward the mean → self-retrieval margins shrink and everyone matches the same "clean" creators. This looks *better* on fluency, *worse* on discrimination.
- **Sample too short.** Style embeddings are high-variance on short text; within-person noise swamps between-person signal at small n. Any "improvement" may be inside the noise band. Use the longest samples you have; report per-person deltas so noise is visible.
- **Train-on-eval leak.** If the profile is built from the same clip you translate and match, it already "knows." Build profile on held-out clips, evaluate on different clips.
- **Base-model confound.** If the fancy pipeline also swaps in a bigger/newer model or 5× the tokens, the gain is the model, not the profile+principles mechanism. **Hold the base model and token budget fixed across arms** or you're testing the wrong variable.
- **Judge bias.** Bilingual judges may reward "sounds authentically Korean-inflected" as more faithful, biasing toward over-preservation independent of match quality. Blind, randomize order.
- **Tiny-n multiple comparisons.** 3–5 people × several metrics → something wins by chance. Pre-declare the primary metric (self-retrieval MRR) and treat the rest as secondary.

## Q3 — Real risk it makes matching WORSE

Yes, plausibly, via two distinct mechanisms:

1. **Common-mode LLM tics reduce between-speaker variance.** A heavily style-prompted translator stamps its own signature (tricolons, "not X but Y", hedging cadence) onto *everyone*. That adds a shared vector to all translations, shrinking the very between-speaker variance k-NN needs. A style-*preserving* prompt can inject *more* uniform structure than a plain one, degrading discrimination — the opposite of the goal.

2. **Over-preservation → out-of-distribution English.** Forcing Korean discourse structure (topic-comment, sentence-final softening, subject-drop, honorific register) into English yields English no native creator actually produces. That vector lands in an empty region of the English-creator manifold; its nearest neighbor is arbitrary and unstable — you match to "closest to weird," not "closest in style." The *plainer* translation, by normalizing into fluent English, may land in-distribution and match more sensibly. There is a genuine tension here: **idiolect fidelity vs. living in the embedding space your creators actually occupy.** The pipeline rewards the latter, and the fancy translator optimizes the former.

3. **The style model may not encode the preserved features at all.** If the English style embedder was trained on native register, Korean-derived features get projected out or mapped to noise — effort preserving them is wasted or harmful.

Instability alone is a product regression: a learner who gets a different shadow-target on re-run is a worse experience even if average quality is flat.

## Q4 — MVP: single prompt now, full port deferred

At $10/mo and n = you + a few friends, the full profile+principles+batch mechanism is over-engineered for what the spike can even resolve. Its value — cross-clip consistency and cost efficiency **at volume** — is exactly what you don't have at alpha. And with n≈3–5, measurement error dwarfs any mechanism-vs-prompt delta, so you *cannot* statistically justify the port even if you build it.

**Build now:** a single well-crafted style-preserving prompt as arm B — preserve rhetorical patterns, pacing, directness, hedging, sentence rhythm; explicitly forbid "improving" the register; no separate profile artifact. Same base model as arm A. Cost: a handful of calls, far under budget.

**Defer the full port** until you observe *both*: (a) single-prompt B closes a meaningful fraction of the plain→ceiling gap on self-retrieval **and** wins blinded 2AFC, **and** (b) you actually see the specific failure the profile mechanism fixes — consistency loss across long/multi-clip inputs. If single-prompt already sits near the ceiling, the full port has no headroom to buy.

## Recommendation: NO-GO on the port, GO on a scoped spike

- **No-go** on porting the full profile+principles+batch translator now — unvalidated hypothesis, engineering/maintenance surface, and unmeasurable at this n.
- **Go** on a tight spike, in this order:
  1. **Bracket test first** (floor / plain / ceiling). If plain ≈ ceiling, stop — defer all translation work.
  2. If headroom exists: **single style-preserving prompt (B) vs current (A), same base model**, scored by self-retrieval MRR (per-person paired deltas) + blinded 2AFC, plus a top-1 stability check.
- **Gate to the full port:** only if B measurably closes a real fraction of the plain→ceiling gap, wins blinded preference, and does **not** reduce match stability. Absent all three, the fancier translator is solving translation quality — which is not your metric.