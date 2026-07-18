"""
Phase 0 spike — style-preserving Korean→English translation for Path B.

WHY THIS EXISTS
The spike found Path B (translate → embed with an English style model) works, but its
weakness was that Whisper's built-in translation FLATTENS the speaker's idiolect — and
idiolect (sentence rhythm, hedging, filler density, persuasion moves) is exactly the signal
the style embedder matches on. This module replaces the flat translation with a
STYLE-PRESERVING one, adapted (mechanism, not code) from Sumin's shadowing-plus repo. See
.agents/reference/translation-style-preservation.md for the full design and its rationale.

KEY INVERSION vs shadowing-plus: they translate EN→KO for a human to READ, so they smooth
disfluency into fluent Korean. We translate KO→EN for a STYLE MODEL to MATCH, so we do the
opposite — we preserve disfluency, hedges, and rhythm even when the English is less polished.

Single-prompt version (the verification analysis recommended NOT porting the full
profile+batch machinery at alpha scale). Two small LLM calls:
  Stage A: extract the speaker's rhetorical fingerprint (JSON) from the Korean transcript.
  Stage B: translate KO→EN with that fingerprint injected + idiolect-preserving principles.

Provider: OpenAI-compatible. Defaults to gpt-4o-mini (cheap, ~$0.002/match). Set
OPENAI_API_KEY. (Swap to Claude/Vercel AI Gateway in the product; kept simple here.)

Throwaway spike code.
"""

from __future__ import annotations

import json
import os

import _env  # noqa: F401  — loads spike/.env into os.environ on import

TRANSLATE_MODEL = os.environ.get("TRANSLATE_MODEL", "gpt-4o-mini")

# ── Stage A: speaker rhetorical fingerprint ──────────────────────────────────
_FINGERPRINT_SYS = """You are a sociolinguist analyzing HOW a person speaks, not what they say. \
You receive a raw Korean speech transcript of one person talking spontaneously (self-talk / \
monologue). Extract that speaker's RHETORICAL FINGERPRINT — the stable, content-independent \
habits of their speaking style — as JSON.

This fingerprint is used to translate their speech into English while PRESERVING these habits, \
so downstream software can match them to an English speaker with a similar style. You are \
DESCRIBING what is already there — never prescribing, correcting, or improving it. A rambling, \
hedged, repetitive, or grammatically rough speaker MUST be described as rambling, hedged, \
repetitive, and rough. Grammatical roughness is itself a style signal, not a defect to flag \
for fixing. Fidelity to their real style is the only goal.

CRITICAL CALIBRATION — filler_density and disfluency describe the ENGLISH that would sound like \
this same person, NOT the raw rate of Korean discourse particles. Korean speech uses particles \
like 그니까/약간/뭔가/막/좀 as ordinary grammatical connective tissue; most of them are NOT the \
English equivalent of "like/you know/I mean". A speaker who says 약간 every clause is usually a \
NORMAL Korean speaker, not an English filler-machine. Judge filler_density by asking: "if this \
person spoke English with the same underlying disposition, how filler-heavy would they sound to \
an English ear?" — and default toward LOWER unless the Korean shows genuine hesitation, \
self-repair, or hedging beyond routine particle use.

Return ONLY this JSON object (no commentary):
{
  "filler_density": "low | medium | high — calibrated to how filler-heavy this person would sound IN ENGLISH, not to the Korean particle rate. Most speakers are low or medium. 'high' only if they genuinely hesitate/repair/stall constantly.",
  "disfluency_type": "clean | filler-heavy | grammatically-rough | self-interrupting — the DOMINANT texture of their disfluency (pick the closest; may name a second if clearly mixed)",
  "hedging": "how much and how they soften claims + the actual hedge patterns they lean on (tentative vs confident). Distinguish real hedging from routine particles.",
  "fillers": "their characteristic discourse fillers, if any, and roughly how often — described for ENGLISH output, consistent with filler_density",
  "sentence_rhythm": "long run-on clause-stacked | short clipped | mixed — describe how clauses connect",
  "mood": "imperative/hyping | reflective/wondering | analytical/qualifying | narrating | persuading",
  "directness": "blunt asserts-and-moves-on | circling/tangential/self-interrupting | hedged/tentative",
  "persuasion_move": "signature move if any: numbered lists | rhetorical-Q-then-A | contrast X-but-Y | anecdote-then-lesson | repetition | none",
  "self_reference_stance": "confident I-statements | tentative I-think/maybe | impersonal/general",
  "register_note": "the ENGLISH register that would sound like the SAME person: casual vs formal — mirror THEM, never default"
}"""

# ── Stage B: idiolect-preserving translation ─────────────────────────────────
_TRANSLATE_SYS_TMPL = """You translate spontaneous Korean speech into English. Your goal is UNUSUAL: \
you are NOT producing clean, publishable English. You are producing English that a style-analysis \
model will read to recognize THIS speaker's personal way of talking. Carry the speaker's rhetorical \
fingerprint into English, even when that means the English is less polished than a professional \
translator would write. Translate MEANING faithfully, but preserve STYLE aggressively. When "the \
natural English way to say it" and "the way THIS speaker would say it" conflict, choose the speaker.

Your job is REPRODUCTION, symmetric in both directions: reproduce exactly what is in the speech, \
NEVER adding what is not there and NEVER removing what is. Adding fillers, hedges, or disfluency the \
speaker did not exhibit is exactly as wrong as smoothing away the ones they did. Both distort the \
fingerprint. Do NOT "make it sound more natural / more casual / more spoken" — that is adding.

This speaker's fingerprint:
{fingerprint}

HARD CEILING — filler and disfluency budget (this overrides every stylistic instinct below):
Your English output's filler/disfluency level is capped by the fingerprint's filler_density and \
disfluency_type. Treat filler_density as a CEILING, not a target:
  • low  → at most an occasional filler; long stretches should have NONE. Do NOT sprinkle "like / \
you know / I mean / I guess" across clauses. If in doubt, leave it out.
  • medium → fillers appear sometimes, at natural boundaries — not in the majority of clauses.
  • high → frequent fillers are appropriate.
A Korean particle (그니까/약간/뭔가/막/좀 …) is NOT an instruction to emit an English filler. Most of \
the time it maps to nothing, or to sentence rhythm. NEVER translate particles one-to-one into \
"like/you know/I mean". Whether an English filler appears is governed ONLY by the ceiling above. \
If your draft has a filler in most sentences and filler_density is low or medium, you have \
over-injected — delete them until you are back under the ceiling.

PRINCIPLES (all in service of preserving idiolect for style-matching):
1. PRESERVE SENTENCE RHYTHM. Match their sentence length and clause shape. If they stack clauses into \
long run-ons (근데/그래서/그리고), render one long English sentence joined by "but/so/and" — do NOT break \
into tidy short sentences. If they speak in clipped fragments, keep fragments. Restructure only as much \
as grammar forces.
2. HEDGES: reproduce the ones that are there, at their real strength; add none. Translate a genuine \
hedge as a hedge (a tentative claim stays tentative, a confident one stays confident). Under-hedging a \
real hedger and over-hedging a blunt speaker are both errors. Routine particles are not hedges.
3. GRAMMATICAL ROUGHNESS IS SIGNAL — PRESERVE IT, DO NOT CORRECT IT. If the speaker's phrasing is \
awkward, if articles/tenses/prepositions come out non-standard when carried into English, if a \
sentence trails or doesn't fully resolve, LEAVE IT. Rough, ESL-flavored, or imperfect English that \
mirrors how this person actually structures thought is CORRECT output. Do not tidy it into fluent \
native English — that erases the fingerprint. (This is not license to ADD errors; only to keep the \
ones the speaker's own phrasing produces.)
4. PRESERVE SELF-CORRECTIONS / FALSE STARTS only where the speaker actually made them ("no wait— I \
mean," "the thing is—"). Mirror them; NEVER manufacture disfluency that isn't there. A clean speaker \
gets clean output.
5. PRESERVE THE PERSUASION MOVE AND MOOD, not just content. Rhetorical question then answer → keep it \
as a question then answer. Threefold repetition → repeat three times. Keep imperatives imperative, \
wondering tentative.
6. REGISTER MIRRORS THE SPEAKER, held consistent throughout. Never default to formal/polished/"professional" \
English unless the speaker themselves is formal.
Keep named entities verbatim (romanized). Mark quoted/inner speech with English quotation conventions.

INPUT is a JSON array: [{{"n": 0, "ko": "..."}}, ...].
Return JSON: {{"0": "<english>", "1": "<english>", ...}} — one entry per input "n", same count, keyed by "n"."""


def _client():
    try:
        from openai import OpenAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            f"openai lib not installed ({e}). pip install -r requirements.txt"
        ) from e
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Get a key at https://platform.openai.com/api-keys "
            "(or set TRANSLATE_MODEL + a compatible base_url)."
        )
    return OpenAI(api_key=key)


def fingerprint(korean_text: str) -> dict:
    """Stage A — extract the speaker's rhetorical fingerprint as a dict."""
    client = _client()
    resp = client.chat.completions.create(
        model=TRANSLATE_MODEL,
        messages=[
            {"role": "system", "content": _FINGERPRINT_SYS},
            {"role": "user", "content": korean_text},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    try:
        return json.loads(resp.choices[0].message.content or "{}")
    except json.JSONDecodeError:
        return {}


def _chunk_sentences(text: str, max_chars: int = 1500) -> list[str]:
    """Rough sentence chunking so a long sample stays inside one or few calls."""
    import re

    sents = re.split(r"(?<=[.!?。…])\s+", text.strip())
    chunks: list[str] = []
    cur = ""
    for s in sents:
        if len(cur) + len(s) + 1 > max_chars and cur:
            chunks.append(cur.strip())
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur.strip():
        chunks.append(cur.strip())
    return chunks or [text.strip()]


def translate_styled(korean_text: str, fp: dict | None = None) -> str:
    """
    Stage A + Stage B — style-preserving KO→EN.

    Returns the concatenated English translation (embedded as one string downstream,
    matching how match.py embeds the whole translation). If `fp` is provided, Stage A
    is skipped (useful for A/B where the fingerprint is reused).
    """
    if fp is None:
        fp = fingerprint(korean_text)
    client = _client()
    sys_prompt = _TRANSLATE_SYS_TMPL.format(
        fingerprint=json.dumps(fp, ensure_ascii=False, indent=2)
        if fp
        else "(none extracted)"
    )
    chunks = _chunk_sentences(korean_text)
    payload = [{"n": i, "ko": c} for i, c in enumerate(chunks)]
    resp = client.chat.completions.create(
        model=TRANSLATE_MODEL,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,  # low: reproduce, don't invent. The ceiling + roughness rules do the anti-flattening work, not sampling noise.
    )
    try:
        out = json.loads(resp.choices[0].message.content or "{}")
    except json.JSONDecodeError:
        return ""
    # Reassemble in n-order; tolerate the model keying by int or str.
    parts = []
    for i in range(len(chunks)):
        parts.append(out.get(str(i)) or out.get(i) or "")
    return " ".join(p for p in parts if p).strip()
