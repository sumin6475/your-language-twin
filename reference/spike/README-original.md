# Phase 0 — Science Spike (throwaway)

**This is not product code.** It answers one make-or-break question before we build anything:

> Can we find an English creator whose **linguistic/rhetorical style** genuinely resembles a
> learner speaking their **native language** — well enough to be worth shadowing?

## What we've learned so far (2026-07-18)

Running the pieces below, on a corpus of **51 real speakers** (43 US presidents [formal] + 8
conversational creators [spoken]) embedded with style models, we found:

- **Path A — embed Korean directly (`mstyledistance`) → k-NN: WEAK.** The multilingual style
  model can't discriminate style *within* Korean (formal vs. analytic Korean scored 0.997
  cosine), and Korean-vs-English similarity is dominated by the language gap, not style.
  Centering didn't reliably fix it. → **Not the path.**
- **Path B — translate Korean → English, then embed (`styledistance`) → k-NN: WORKS.** English
  style probes land on the right style-matched creators.
- **The catch:** plain Whisper translation *flattens* the speaker's idiolect (hedges, fillers,
  rhythm) — which is exactly what the style model matches on. So **how** we translate matters a
  lot. A text-level test confirmed it: the *same* Korean utterance translated plainly matched a
  "high-energy" creator (wrong), but translated with **style preservation** matched a "hedged
  casual explainer" (right), 0.95 vs 0.88. → **Path B with style-preserving translation is the
  design.**

So the direction is decided (**Path B**), and the open question is now narrower: *how much does
style-preserving translation actually improve matching on real voices?* → run the **bracket
test** below with your own audio.

## The pieces

- **`build_corpus.py`** — builds the English-creator corpus (real speakers from
  `chrissoria/presidential-speeches` + 8 hand-authored conversational-creator style profiles for
  genre diversity), embeds each with `mstyledistance` (Path A) and `styledistance` (Path B),
  saves `data/corpus.npz`. *(The 8 conversational creators are STYLE-representative excerpts, not
  verbatim transcripts — fine for the spike; replace with real self-transcribed creator speech
  for the product. See `.agents/reference/translation-style-preservation.md`.)*
- **`translate.py`** — style-preserving KO→EN translation (the Path B improvement), adapted from
  Sumin's `shadowing-plus` repo. Two small LLM calls: Stage A extracts the speaker's rhetorical
  fingerprint, Stage B translates while preserving hedges/fillers/rhythm. Needs `OPENAI_API_KEY`.
- **`match.py <audio>`** — runs all three paths (A / B-plain / B-styled) on one sample, side by
  side, for hand judgment.
- **`bracket.py`** — the **objective** test: for bilingual testers (Korean audio + their OWN
  genuine English), measures how close each variant lands them to their own real English style.
  This tells you whether better translation is even worth building. Reads `samples/manifest.json`.

## Setup

```bash
cd spike
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export GROQ_API_KEY=...      # ASR (free): https://console.groq.com/keys
export OPENAI_API_KEY=...    # style-preserving translation: https://platform.openai.com/api-keys
# (OPENAI_API_KEY optional — Path B-styled and the bracket's STYLED column skip gracefully without it.)
```

## Run

```bash
# 1) Build + embed the corpus (once, ~1 min). No keys needed.
python build_corpus.py

# 2) Drop native-language audio into spike/samples/ (wav/mp3/m4a/mp4), then:
python match.py samples/my_korean_selftalk.m4a     # 3-way comparison, judge by hand

# 3) THE OBJECTIVE GATE — needs bilingual samples. Create samples/manifest.json:
#    [{ "name": "me",
#       "korean_audio": "samples/me_ko.m4a",
#       "english_text": "samples/me_en.txt" }]   # your OWN genuine English (transcript or writing)
python bracket.py
```

## How to read the bracket test / the gate

`bracket.py` reports, per tester, the **rank** of their own English among the creator gallery
for four variants:

| Variant | What | Expect |
|---|---|---|
| FLOOR | Korean embedded directly | worst (confirms Path A is wrong) |
| PLAIN | Whisper translate → embed | the current baseline |
| STYLED | style-preserving translate → embed | the improvement |
| CEILING | the person's own English, embedded | best possible |

- **If PLAIN ≈ CEILING** → plain translation is already near the ceiling; improving translation is
  NOT the bottleneck. Ship Path B with plain translation, defer the styled translator.
- **If STYLED closes a real fraction of the PLAIN→CEILING gap** → the style-preserving translator
  earns its place. Build it into Phase 1.
- Also do a **blinded 2AFC** for the subjective truth: show a bilingual friend the Korean clip +
  the top-1 creator from PLAIN vs from STYLED (blind to which is which), ask "which sounds like the
  same kind of speaker?" Count wins over ~10-20 judgments.

**PASS (build the app):** for a majority of 5-10 samples, at least one path returns a top-3 creator
a bilingual human accepts as "structures thoughts like this speaker," and the bracket shows Path B
comfortably beating the floor. Record whether STYLED beats PLAIN — that decides whether Phase 1
includes the style-preserving translator.

## Notes / caveats

- **ASR erases some idiolect before translation even runs.** Whisper cleans up fillers/disfluency.
  That's a floor no translation prompt can recover — part of why we measure the ceiling.
- **Corpus representation mismatch (Phase 1 item):** the corpus English side is built from clean
  text; a translator that preserves disfluency may push the query into empty space. The honest fix
  is rebuilding both sides of the k-NN through the same style-preserving translator. Noted, not a
  spike blocker.
- **Legal:** we only *analyze* transcripts and later link out to creators' real videos. Do not
  commit raw audio (`.gitignore` blocks it); user audio is never retained in the product.
- **Everything here is disposable.** `data/`, `cache/`, `*.npz`, `install.log`, `*_build.log`, and
  `samples/*` (except `.gitkeep`) are gitignored.
- **Full design rationale:** `.agents/reference/translation-style-preservation.md`.
