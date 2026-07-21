# Landing Motion Spec — extracted from the Dreelio Framer reference

Motion parameters measured live from `https://amiable-notes-134437.framer.app/` (Dreelio), to
apply to **our** landing. **Borrow the motion and a couple of composition ideas only. Keep our own
design system** (Signature Blue, Clash Display + Inter, our tokens) and our copy. Do NOT copy
Dreelio's look (sky/clouds, Open Runde font, its 10-section SaaS structure).

Target: **framer-motion** in Next.js (the closest engine to Framer's own). Values below are literal.

## Motion vocabulary (measured)

- **Primary easing:** `cubic-bezier(0.44, 0, 0.56, 1)` — smooth symmetric ease-in-out. Used on ~all
  hovers/state changes at **0.4s**. In framer-motion: `ease: [0.44, 0, 0.56, 1]`.
- **Fast micro easing:** `cubic-bezier(0.2, 0, 0, 1)` at **0.1s** — taps / quick state flips.
- **Appear pattern:** key blocks fade in with a small upward translate (opacity 0 to 1 + translateY).
  Framer "appear" system was active on the hero cluster and section headers.
- **Transform-heavy:** 100+ elements use `will-change: transform` — hover lifts on cards/buttons and
  a rise on the product mockup are core to the feel.
- **Signature hero touch:** the subhead reveals **word by word** (each word brightens from faded to
  full as it scrolls into view). This is the one distinctive motion worth copying.

## Reusable motion tokens (define once, reuse)

```
EASE       = [0.44, 0, 0.56, 1]     // primary
EASE_FAST  = [0.20, 0, 0.00, 1]     // taps
DUR        = 0.5                     // section reveal
DUR_HOVER  = 0.4                     // hover/state
DUR_TAP    = 0.1                     // press
RISE       = 24                      // px translateY for reveals (cards/text)
RISE_BIG   = 40                      // px for the product mockup
STAGGER    = 0.12                    // between siblings (steps, cards)
STAGGER_WORD = 0.03                  // subhead word-by-word
```

## Per-section motion (mapped to OUR landing sections)

Our landing order: Wordmark, Hero (headline + subhead + trust line), Upload card, How it works (3),
Privacy line, Footer.

1. **Hero — load sequence (plays on mount, not scroll).** Stagger the hero children top to bottom:
   wordmark, headline, subhead, trust line, then the upload card. Each: `initial {opacity:0, y:RISE}`
   to `animate {opacity:1, y:0}`, `transition {duration:DUR, ease:EASE}`, with `delayChildren: 0.05`
   and `staggerChildren: 0.10` on the wrapper.
2. **Subhead word reveal (signature).** Split the subhead into words; each word `initial {opacity:0.35}`
   to `{opacity:1}`, `staggerChildren: STAGGER_WORD`, `ease: EASE`. Trigger with the hero on load
   (and/or `whileInView`).
3. **Upload card — entrance + presence.** Rises with the hero (`y:RISE`). On hover of the primary
   button: `whileHover {y:-2}` and `whileTap {scale:0.98}` with `DUR_HOVER` / `DUR_TAP`, `EASE`.
4. **How it works (3 steps) — scroll reveal + stagger.** Wrapper `whileInView`, `viewport {once:true,
   margin:"-10% 0px"}`, `staggerChildren: STAGGER`. Each step `initial {opacity:0, y:RISE}` to
   `{opacity:1, y:0}`, `transition {duration:DUR, ease:EASE}`.
5. **Privacy line + Footer — gentle scroll fade.** `whileInView {opacity:1, y:0}` from
   `{opacity:0, y:12}`, `DUR`, `EASE`, `once:true`. Smaller travel, they are quiet.

## Composition ideas worth borrowing (optional, keep our look)

- **Product mockup directly under the hero CTA.** Dreelio shows its dashboard right below the hero.
  For us: show a small **results preview** (one blurred/sample MatchCard or a simple app frame)
  under the upload card, rising on scroll: `initial {opacity:0, y:RISE_BIG, scale:0.98}` to
  `{opacity:1, y:0, scale:1}`, `duration:0.6`, `EASE`. Signals "this is a real product."
- **Pill-shaped sticky nav / wordmark** (Dreelio's nav is a rounded pill). Optional, matches our
  soft-radius system.

## Rules

- **Motion only from this doc; look from the design system.** Colors, fonts, spacing, radius come
  from `DESIGN.md` + `tokens.json`. Never adopt Dreelio's palette or font.
- **Respect `prefers-reduced-motion`:** when set, disable transforms/opacity animation and render
  final state (accessibility).
- **Do not over-animate.** Only the motions listed here. No parallax on everything, no autoplay
  loops, no motion on body text beyond the subhead reveal.
- Every animation states duration + easing + offset (per the reference-to-spec quality floor).

## Dependency

- `framer-motion` (pin the version at build time). Import `motion`, `useReducedMotion`, and (for the
  word reveal) optionally `useScroll` / `useInView`.
