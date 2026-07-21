# Build Prompt — Landing Page (Your Ideal Role Model)

Self-contained brief to build the landing / upload page (route `/`) for the Next.js app in this
repo. It contains the design tokens (literal), the structure and copy, and the animation. Paste and
build. Every value is literal so nothing is left to guess.

## Build rules

- **Stack:** Next.js (App Router) + Tailwind + `framer-motion` (pin the version). TypeScript `.tsx`.
- **Use ONLY the tokens in this doc.** Do not invent colors, fonts, sizes, spacing, radius, or
  shadows. (Full source of truth also lives in `docs/design/DESIGN.md` + `tokens.json`; this doc
  embeds the values you need.)
- **Copy:** use the exact strings below, no placeholders. **No em dashes anywhere in copy** (use
  commas or periods). Headlines are real sentences, not slogans.
- **Motion:** `framer-motion`, using the motion tokens below. Respect `prefers-reduced-motion`: when
  set, skip transforms/opacity animation and render the final state.
- Layout: mobile-first, single centered column, comfortable max width, generous vertical spacing
  (section gaps at least 48px).
- Scope: this page only. It ends by navigating to `/results` after a successful match.

---

## DESIGN TOKENS (literal — the look)

### Fonts
- **Display** (headlines, names, eyebrows, buttons, section labels): **Clash Display**, weights
  500 and 600. Headlines are 500 to 600, **never thin**. Load in `<head>`:
  `https://api.fontshare.com/v2/css?f[]=clash-display@500,600&display=swap`
- **Body** (body text, UI, the "why" paragraph): **Inter**, 400/500/600/700. Load in `<head>`:
  `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap`

### Colors
```
bg.base      #FFFFFF   page background
bg.subtle    #FAFAFB   section fill / card fill on white
text.primary #18181B   headlines, body
text.secondary #52525B supporting body, the subhead, the "why"
text.tertiary  #71717A roles, meta, muted lines (lightest grey allowed for readable text)
blue.deep    #1E40AF   primary button, key highlight (accent, use sparingly)
blue.bright  #3B82F6   hover, gradient partner
blue.tint    #EFF3FF   small chips (e.g. tier chip background)
border       #ECECF0   card borders, dividers
```
Blue is an accent only: primary button, the avatar gradient (`blue.deep` to `blue.bright`), and one
key highlight per screen. Never blue for borders, body text, or decoration. No gradients as
backgrounds. Do not invent new colors.

### Type scale
```
h1    34px / line-height 1.1  / letter-spacing -0.015em
h2    24px / 1.15
h3    18px / 1.3
body  15px / 1.6
small 13px / 1.5
label 12px / 1.4 / letter-spacing 0.1em   (eyebrow/label floor, never smaller)
```
Weights: display headlines 500 to 600; body 400; labels and buttons 500. Uppercase only on small
labels/eyebrows, only at weight 500.

### Spacing / radius / shadow
```
space  4 · 8 · 12 · 16 · 24 · 32 · 48   (section gap floor 48)
radius sm 8 · md 12 (buttons) · lg 16 (cards) · xl 24 (page container)
shadow card   0 4px 14px rgba(0,0,0,0.04)    (resting cards)
       raised 0 12px 32px rgba(0,0,0,0.10)   (lifted / hero card)
```
Soft shadows only. No hard/black shadows, no heavy borders.

### Anti-AI-cliche guardrails (audit every screen)
- Eyebrow/label at least 12px, weight 500+, not faint.
- No thin or light all-caps display type.
- Grey no lighter than `text.tertiary` for anything readable.
- Consistent spacing scale (4/8/12/16/24/32/48).
- Real-sentence headlines; real data, never placeholders.
- No em dashes in copy.

---

## MOTION TOKENS (literal — the movement)

```
EASE         = [0.44, 0, 0.56, 1]   // primary ease-in-out (measured from the reference)
EASE_FAST    = [0.20, 0, 0.00, 1]   // taps
DUR          = 0.5                   // section reveal
DUR_HOVER    = 0.4                   // hover / state
DUR_TAP      = 0.1                   // press
RISE         = 24                    // px translateY for text/card reveals
RISE_BIG     = 40                    // px for a product-preview rise
STAGGER      = 0.12                  // between siblings (steps)
STAGGER_WORD = 0.03                  // subhead word-by-word
```
The Hero and Upload card animate on **mount** (load sequence). Everything below animates on **scroll
into view**: `whileInView`, `viewport {once:true, margin:"-10% 0px"}`.

---

## SECTION ORDER
1. Wordmark
2. Hero (headline + subhead + trust line)
3. Upload card (primary action, visible without scrolling)
4. How it works (3 steps)
5. Privacy line
6. Footer

---

## 1. Wordmark
Small, muted (`text.secondary`), top of page. Text: `Your Ideal Role Model`.
Motion: first item in the hero load sequence.

## 2. Hero
- **Headline (display, `text.primary`, size h1):**
  `Turns out someone already speaks English the way you think.`
- **Subhead (`text.secondary`, size body):**
  `Talk for two minutes in your own language. We find three real English creators who speak the way you already think, so shadowing feels natural, not forced.`
- **Trust line (`text.tertiary`, size small):** `No account. No sign up. Just a voice note.`

**Motion — load sequence (on mount):** wrap the hero children and stagger top to bottom (wordmark,
headline, subhead, trust line, then the upload card). Each child `initial {opacity:0, y:RISE}` to
`animate {opacity:1, y:0}`, `transition {duration:DUR, ease:EASE}`. Wrapper `delayChildren:0.05`,
`staggerChildren:0.10`.

**Motion — subhead word reveal (signature):** split the subhead into words, each a `motion.span`,
`initial {opacity:0.35}` to `{opacity:1}`, `transition {ease:EASE}`, wrapper `staggerChildren:STAGGER_WORD`.
Plays as part of the hero load.

## 3. Upload card (= the CTA)
A `bg.subtle` surface, `radius.lg`, `shadow.raised`, generous padding.
- **Card label (display, h3):** `Start with a voice note`
- **Helper (`text.secondary`, small):** `A natural clip, about two minutes, works best. Talk the way you would to a friend.`
- **File input:** button reads "Choose File"; accept `audio/*` plus `.m4a .mp3 .wav .mp4 .webm .ogg`
- **Selected file line (`text.tertiary`, small, only after a file is chosen):** `Selected: <filename>`
- **Consent checkbox (required, accent `blue.deep`):** `I consent to processing this audio to generate a one-time style match. My audio is deleted after processing.`
- **Age line (`text.tertiary`, small):** `You confirm that you are 18 or older.`
- **Primary button (`blue.deep` fill, white text, `radius.md`):** `Find my creators`

**States**
- Default: button disabled until a file is selected AND consent is checked.
- File selected: show the `Selected:` line; enable the button (if consent also checked).
- Invalid submit: inline muted `Choose an audio file and confirm consent before continuing.`
- Loading: button disabled, text becomes `Finding your matches...`; muted line below `This takes about 30 seconds.` Keep the form on screen.
- Error: inline muted `Something went wrong. Please try that once more.` (or the backend message). Re-enable the button.

**Behavior / flow**
- Selecting a file clears any prior error.
- On submit, build a multipart form field `audio` and POST to
  `${NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000"}/match`.
- On success (200 with exactly 3 matches): store the JSON in `sessionStorage`, then navigate to `/results`.
- On failure: stay here, show the error, re-enable the button. Persist nothing on failure.

**Motion:** the card rises with the hero (`y:RISE`, last in the load sequence). Primary button
`whileHover {y:-2}` and `whileTap {scale:0.98}`, transitions `DUR_HOVER` / `DUR_TAP`, `EASE`.
(Optional: a small results-preview frame under the card that rises on scroll:
`initial {opacity:0, y:RISE_BIG, scale:0.98}` to `{opacity:1, y:0, scale:1}`, `duration:0.6, ease:EASE`.)

## 4. How it works (3 steps)
Three steps, evenly spaced. Bold step title (display, h3) + one body line each.
1. **Speak your language.** `Record or upload about two minutes of yourself talking naturally, in your native language.`
2. **We read your style, not your words.** `Our model looks at how you build sentences, pause, and make a point, not what you talked about.`
3. **Meet your matches.** `Get three real English creators who speak in a familiar way, with a link to start shadowing today.`

**Motion — scroll reveal + stagger:** wrapper `whileInView`, `viewport {once:true, margin:"-10% 0px"}`,
`staggerChildren:STAGGER`. Each step `initial {opacity:0, y:RISE}` to `{opacity:1, y:0}`,
`transition {duration:DUR, ease:EASE}`.

## 5. Privacy line
One reassuring line (`text.tertiary`, small):
`Your audio is deleted the moment we are done. We keep only a set of numbers about your style, never your voice and never your words.`
**Motion:** gentle scroll fade, `initial {opacity:0, y:12}` to `{opacity:1, y:0}`, `DUR`, `EASE`, `once:true`.

## 6. Footer
Muted (`text.tertiary`), divider (`border`) above.
- `Not affiliated with or endorsed by any creator.`
- `For creators, coming soon.`
- A `Takedown request` link (opens `mailto:` a configurable contact address).
**Motion:** same gentle scroll fade as the privacy line.

---

## Components to build
Wordmark, Hero (headline + subhead word-reveal + trust line), UploadCard (file input, selected line,
consent checkbox, age line, submit button, loading + error states), HowItWorks (3 steps), PrivacyLine,
Footer.

## Acceptance
- Submit cannot fire without a file AND consent; loading and error states visible; form stays on screen.
- Consent and the 18+ line appear before any processing.
- Success navigates to `/results`; failure stays and can retry.
- Exact copy, no placeholders, no em dashes.
- Only the tokens in this doc are used; nothing hardcoded outside them.
- `framer-motion` used with the motion tokens; every animation has duration + easing + offset;
  `prefers-reduced-motion` respected; nothing over-animated beyond what is specified.
- Passes the anti-AI-cliche guardrails above.
