# Landing Page Brief — Your Ideal Role Model

A self-contained brief to build the **landing / upload page only** (route `/`). Hand this file
plus the design system to generate the page.

## How to use this

- **Apply the existing design system, do not invent one:** `docs/design/DESIGN.md` (rules) +
  `docs/design/tokens.json` (values) + `docs/design/tailwind.config.js`. All color, type, spacing,
  radius, and shadow come from there. This brief never sets those values.
- **Use the exact copy below.** No placeholders (DESIGN.md 4.4).
- **No em dashes in any copy** (DESIGN.md 4.2). Commas or periods only.
- Headlines are real sentences, not slogans. Run DESIGN.md section 7 before finishing.
- **Layout:** mobile-first, single centered column, comfortable max width, generous vertical
  spacing between sections (per the design system spacing scale).

## Scope

This page only. The results page and its cards are out of scope here (built separately). This page
ends by sending the user to `/results` after a successful match.

## Section order (top to bottom)

1. Wordmark
2. Hero (headline + subhead + trust line)
3. Upload card (the primary action, visible without scrolling)
4. How it works (3 steps)
5. Privacy line
6. Footer

The upload card sits high, right after the hero, so the action is immediate. How it works and the
privacy line sit below for anyone who hesitates before uploading a voice clip.

---

## 1. Wordmark

Small, muted, top of page.

```
Your Ideal Role Model
```

## 2. Hero

- **Headline (real sentence, display type):**
  `Turns out someone already speaks English the way you think.`
- **Subhead:**
  `Talk for two minutes in your own language. We find three real English creators who speak the way you already think, so shadowing feels natural, not forced.`
- **Trust line (small, muted, reduces friction):**
  `No account. No sign up. Just a voice note.`

## 3. Upload card (= the CTA)

A raised surface holding the whole action.

- **Card label:** `Start with a voice note`
- **Helper:** `A natural clip, about two minutes, works best. Talk the way you would to a friend.`
- **File input:** button reads "Choose File"; accepts `audio/*` plus `.m4a .mp3 .wav .mp4 .webm .ogg`
- **Selected file line (muted, only after a file is chosen):** `Selected: <filename>`
- **Consent checkbox (required):**
  `I consent to processing this audio to generate a one-time style match. My audio is deleted after processing.`
- **Age line (muted):** `You confirm that you are 18 or older.`
- **Primary button:** `Find my creators`

### States
- **Default:** button disabled until a file is selected AND consent is checked.
- **File selected:** show the `Selected:` line; enable the button (if consent is also checked).
- **Invalid submit:** if pressed without file or consent, show inline (muted):
  `Choose an audio file and confirm consent before continuing.`
- **Loading:** button disabled, text becomes `Finding your matches...`; show a calm muted line
  below it: `This takes about 30 seconds.` Keep the form on screen, do not blank the page.
- **Error (backend or network):** show inline (muted): `Something went wrong. Please try that once more.`
  (If the backend returns a specific message, show that instead.) Re-enable the button so they can retry.

### Behavior / flow
- Selecting a file clears any prior error.
- On submit, build a multipart form with field name `audio` and POST it to the backend match
  endpoint: `${NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000"}/match`.
- On success (HTTP 200 with exactly 3 matches): store the JSON response in `sessionStorage`, then
  navigate to `/results`.
- On failure: stay here, show the error, re-enable the button. Never persist anything locally on
  failure.

## 4. How it works (3 steps)

Three short steps, evenly spaced. Each has a bold step title and one short line.

1. **Speak your language.**
   `Record or upload about two minutes of yourself talking naturally, in your native language.`
2. **We read your style, not your words.**
   `Our model looks at how you build sentences, pause, and make a point, not what you talked about.`
3. **Meet your matches.**
   `Get three real English creators who speak in a familiar way, with a link to start shadowing today.`

## 5. Privacy line

A single reassuring line (muted), reinforcing the promise made at the upload card.

```
Your audio is deleted the moment we are done. We keep only a set of numbers about your style, never your voice and never your words.
```

## 6. Footer

Muted, divider above.

- `Not affiliated with or endorsed by any creator.`
- `For creators, coming soon.`
- A `Takedown request` link (opens `mailto:` a configurable contact address).

---

## Components to build

- **Wordmark** (text only)
- **Hero** (headline + subhead + trust line)
- **UploadCard** (file input, selected-file line, consent checkbox, age line, submit button, loading
  state, error message)
- **HowItWorks** (3 steps)
- **PrivacyLine**
- **Footer** (disclaimer + creators note + takedown link)

## Acceptance

- The submit button cannot fire without a file AND consent.
- Loading and error states are visible and clear; the form stays on screen during both.
- Consent and the 18+ line appear before any processing can start.
- On success the user lands on `/results`; on failure they stay and can retry.
- Real copy exactly as above, no placeholders, no em dashes.
- Every color, font, spacing, radius, and shadow comes from the design system, nothing hardcoded.
- Passes the DESIGN.md section 7 AI-cliche checklist (eyebrow >= 12px weight 500+, no thin or
  all-caps display type, grey no lighter than the meta floor, generous spacing, blue as accent only).
