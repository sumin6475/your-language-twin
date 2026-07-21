# UI Spec — Your Ideal Role Model

A screen + flow brief for generating the UI (mockups or `.tsx`). It describes **what each screen
contains, how it behaves, and the exact copy** — it does NOT define colors, fonts, or spacing
values.

## How to use this

- **Apply the existing design system**, do not invent one: `docs/design/DESIGN.md` (rules) +
  `docs/design/tokens.json` (values) + `docs/design/tailwind.config.js` (Tailwind mapping). All
  color / type / spacing / radius / shadow decisions come from there.
- **Use the real copy in this doc.** No placeholders like `[Creator name]` or `92%` (DESIGN.md 4.4).
- **No em dashes in any user-facing copy** (DESIGN.md 4.2). Commas, periods, or "then".
- Headlines are real sentences, not slogans. Check every screen against DESIGN.md section 7.
- Layout is **mobile-first, single column, centered**, comfortable max content width.

## Product in one line

A learner uploads a short clip of themselves speaking their native language and meets three real
English creators whose way of speaking feels familiar, each with a one-sentence reason and a link
to that creator's videos.

## Flow overview

```
Landing / Upload  --submit-->  Processing (in-place)  -->  Results
      |                              |                        |
   (no file / no consent)        (backend error)         (no stored result)
      v                              v                        v
  inline validation            inline error message      empty state -> back to upload
```

Two long-lived local servers back this: a Next.js frontend and a local FastAPI `/match` endpoint.
The frontend calls `/match` once, synchronously, and shows a loading state while it waits
(processing takes roughly 15 to 40 seconds).

---

## Screen 1 — Landing / Upload  (route `/`)

### Purpose
First impression + the single action: give us a voice note. Communicate the value and the privacy
promise so uploading feels safe.

### Layout (top to bottom)
1. Small wordmark/eyebrow: `YOUR IDEAL ROLE MODEL`
2. Headline (real sentence): **Find the English creator who structures thoughts like you.**
3. Subhead: *Share a short clip in your native language, then meet three English creators whose way
   of explaining, questioning, or persuading feels familiar.*
4. Upload card (a raised surface):
   - Card label: **Choose a voice note**
   - Helper: *A natural clip of about two minutes works best. Upload-only for this demo.*
   - File input (button reads "Choose File"); accepts `audio/*` plus `.m4a .mp3 .wav .mp4 .webm .ogg`
   - When a file is chosen, show `Selected: <filename>` in a muted line
   - Consent checkbox (required): *I consent to processing this audio to generate a one-time style
     match. My audio is deleted after processing.*
   - Age line (muted): *You confirm that you are 18 or older.*
   - Primary button: **Find my creators**

### States
- **Default:** button disabled until a file is selected AND consent is checked.
- **File selected:** show the filename line; enable button (if consent also checked).
- **Invalid submit:** if pressed without file or consent, show inline message: *Choose an audio file
  and confirm consent before continuing.*
- **Loading:** button becomes disabled and reads **Finding your matches...**; add a reassuring
  muted line below: *This can take about 30 seconds.* Keep the form visible, do not blank the page.
- **Error (backend/network):** show the returned message inline (muted), keep the form so they can
  retry. Example fallbacks: *The match could not be completed.* / *The creator corpus did not
  return exactly three matches.*

### Interactions
- Selecting a file clears any prior error.
- Submit builds a multipart form (`audio`) and POSTs to the backend `/match`.
- On success: store the response in `sessionStorage`, then navigate to `/results`.
- On failure: stay on this screen, show the error, re-enable the button.

### Acceptance
- Button cannot be pressed without file + consent.
- Loading and error states are visible and clear.
- Privacy promise and 18+ line are present before any processing.

---

## Screen 2 — Processing (in-place loading moment)

This is not a separate route; it is the loading state of Screen 1 after submit. It matters
(DESIGN.md section 6), so make it feel intentional:
- The button shows **Finding your matches...** and is disabled.
- A calm one-line reassurance: *This can take about 30 seconds.*
- Optional: a subtle indeterminate indicator (spinner or progress shimmer) using design-system
  surfaces, no hard/black elements.
- Do not show fake progress percentages.

---

## Screen 3 — Results  (route `/results`)

### Purpose
Deliver the payoff: three creators who feel familiar, each with a reason, and a way to go watch
them. Read as warm recognition, not a scored test.

### Layout (top to bottom)
1. Eyebrow: `YOUR THREE MATCHES`
2. Headline (real sentence): **Someone already speaks English in a way that may feel familiar.**
3. Honest framing line (muted): *These are learning-fit recommendations, not a verdict on your
   voice or identity.*
4. **Three MatchCards**, ranked best-first, generous vertical spacing between them.
5. Privacy line (muted, with a check glyph): *✓ Audio deleted. Nothing you said was stored.*
6. **Creator teaser** section (raised surface):
   - Eyebrow: `FOR CREATORS, COMING SOON`
   - Body: *Are you a creator? Learners who think like you are looking for someone to shadow. Soon
     you'll be able to add your voice, with your consent, and get discovered. Coming soon.*
7. Footer (muted, divider above):
   - *Not affiliated with or endorsed by any creator.*
   - A **Takedown request** link (opens `mailto:` a configurable contact address)

### MatchCard anatomy
A card surface (card radius + soft shadow). Left: a small square avatar block filled with the
allowed blue gradient, showing the creator's initials (e.g. `JS`). Right, in a column:
- Row: creator **name** (display type) on the left; a **tier chip** on the right.
- Under the name: **role** in muted meta text (e.g. *warm, reflective story-to-lesson host*).
- The **"why you're alike"** sentence in secondary body text.
- A secondary (outline) button/link: **Visit their channel** (opens the creator's `video_url` in a
  new tab, `rel="noreferrer"`).

### Tier chip (not a number)
The chip shows a resemblance **word**, derived from rank, never a raw score:
- rank 0 → **strong resemblance**
- rank 1 → **clear resemblance**
- rank 2 → **partial resemblance**
Use the blue tint chip style from the design system.
*(If we later choose the playful score variant, the chip would read e.g. "87% your style" and be
clearly framed as a style-resemblance score, not accuracy. Default is the word.)*

### States
- **Success:** three cards render from stored data.
- **Empty (no stored result, e.g. visited directly or refreshed a cleared tab):** show a calm empty
  state: headline *Your matches will appear here.*, body *Upload a clip first, then we can introduce
  you to three creators.*, and a primary button **Choose an audio file** back to `/`.

### Interactions
- "Visit their channel" opens a new tab.
- "Takedown request" opens the mail client to the contact address.

### Acceptance
- Exactly three cards.
- Chip shows a resemblance word, never the raw cosine number.
- Privacy line, creator teaser, and legal footer all present.
- Empty state handles direct navigation gracefully.

---

## Optional (post-demo) — Guided onboarding entry

Not required for the MVP demo (upload-only is enough). Spec it so we can design it later or if time
allows. It would sit before the upload, as a richer way to capture a good sample:
- **Topic picker:** offer **3 universal topics, user picks 1.** Each shows a one-line prompt plus a
  few optional "you could mention..." bullets (never full sentences to read aloud). Example topics:
  *A person who shaped you* / *A recent small decision* / *A movie or show you have opinions about.*
- **Framing line (high-leverage):** *Talk the way you'd tell a friend. Messy, tangents, thinking out
  loud is perfect. Don't script it.*
- **In-browser recorder:** record button, timer, soft floor around 90 seconds, gentle nudge if they
  stop under ~80s, one optional retake. Upload remains available as a fallback.
This replaces or augments the file input on Screen 1; everything downstream (processing, results) is
unchanged.

---

## Component inventory (build only these)

- **Button** — primary (filled) and secondary (outline).
- **Card** — generic raised surface.
- **UploadZone** — file input + selected-file line + helper text.
- **ConsentCheckbox** — required before submit.
- **MatchCard** — the core component (avatar, name, role, tier chip, why, channel link).
- **TierChip** — resemblance word on the tint surface.
- **LoadingState** — the in-place processing moment on Screen 1.
- **EmptyState** — results with no data.
- **TeaserSection** — "For creators, coming soon".
- **Footer** — legal line + takedown link.

## Copy sheet (all user-facing strings, em-dash-free)

- Eyebrow (landing): `YOUR IDEAL ROLE MODEL`
- H1 (landing): `Find the English creator who structures thoughts like you.`
- Sub (landing): `Share a short clip in your native language, then meet three English creators whose way of explaining, questioning, or persuading feels familiar.`
- Upload label: `Choose a voice note`
- Upload helper: `A natural clip of about two minutes works best. Upload-only for this demo.`
- Consent: `I consent to processing this audio to generate a one-time style match. My audio is deleted after processing.`
- Age: `You confirm that you are 18 or older.`
- Button (idle): `Find my creators`
- Button (loading): `Finding your matches...`
- Loading reassurance: `This can take about 30 seconds.`
- Validation error: `Choose an audio file and confirm consent before continuing.`
- Eyebrow (results): `YOUR THREE MATCHES`
- H1 (results): `Someone already speaks English in a way that may feel familiar.`
- Framing (results): `These are learning-fit recommendations, not a verdict on your voice or identity.`
- Tier chips: `strong resemblance` / `clear resemblance` / `partial resemblance`
- Privacy line: `Audio deleted. Nothing you said was stored.`
- Teaser eyebrow: `FOR CREATORS, COMING SOON`
- Teaser body: `Are you a creator? Learners who think like you are looking for someone to shadow. Soon you'll be able to add your voice, with your consent, and get discovered. Coming soon.`
- Channel button: `Visit their channel`
- Footer disclaimer: `Not affiliated with or endorsed by any creator.`
- Takedown link: `Takedown request`
- Empty H1: `Your matches will appear here.`
- Empty body: `Upload a clip first, then we can introduce you to three creators.`
- Empty button: `Choose an audio file`

## Data contract (what the UI binds to)

The backend `/match` returns:
```json
{ "matches": [
  { "name": "Jay Shetty", "role": "warm, reflective story-to-lesson host",
    "video_url": "https://www.youtube.com/@JayShetty",
    "similarity": 0.71, "why": "one warm sentence about HOW they speak" }
] }
```
- Always exactly 3 items, ranked best-first.
- The UI shows `name`, `role`, `why`, and links `video_url`. It derives the tier from the item's
  index (0/1/2). It never displays `similarity`.

## Guardrails (audit before finishing)

- Real names and real "why" sentences in every mockup, never placeholders.
- No em dashes anywhere in copy.
- Tier word on the chip, never the raw score.
- Generous spacing, soft shadows, blue as accent only, per the design system.
- Run the DESIGN.md section 7 AI-cliche checklist on every screen.
