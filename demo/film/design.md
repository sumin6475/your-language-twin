# Language Role Model — Demo Film Design System

Derived from the product's real tokens (`web/app/globals.css`) and the agency brief.
Two visual worlds, one blue thread. Every A↔B transition hands off on a blue element.

## Colors

| Token | Hex | Use |
| --- | --- | --- |
| world-a-black | `#0A0A0B` | World A background (never pure #000) |
| white | `#FFFFFF` | World A primary type; World B cards |
| dim-label | `#A1A1AA` | World A de-emphasized / previous lines |
| blue-deep | `#1E40AF` | Primary accent, buttons, verified |
| blue-bright | `#3B82F6` | Highlights, underlines, arrows, live pulse |
| blue-tint | `#EFF3FF` | Pills, badges fill |
| ink | `#18181B` | World B primary text |
| ink-secondary | `#52525B` | World B body text |
| ink-tertiary | `#71717A` | World B captions |
| bg-subtle | `#FAFAFB` | World B stage / subtle fills |
| border | `#ECECF0` | Card borders |

Avatar/brand gradient: `linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%)`.
No other hues anywhere. Blue is the only color shared by both worlds.

## Typography

- Display: **Clash Display** 600 (500 for medium UI), tracking −0.02em. Files: `fonts/ClashDisplay-500.woff2`, `fonts/ClashDisplay-600.woff2`.
- Body/UI: **Inter** (variable, `fonts/InterVariable.woff2`).
- Mono (agent tags): ui-monospace / Menlo.

## Motion

- World A (ideas): ease-out entrances 350–460ms, key words get a slight spring (`back.out(1.2)`, overshoot ≤6%, one settle).
- World B (product): weighted `power2.inOut` / `power3.out`, 500–700ms, no overshoot. Panels move like glass.
- Entrance vocabulary: rise+fade (y 10→0), pop-scale (.6→1), mask-wipe underlines. First animation never at t=0 (offset 0.1–0.3s).

## World B stage

Light aurora: white `#FAFAFB` base, the app's own repeating-gradient aurora bloom masked to the top-right, blurred, slowly drifting. Screens are floating glass panels: border-radius 18px+, shadow `0 12px 32px rgba(0,0,0,.10)`, slight tilt, slow push-ins, rack focus.

## What NOT to do

- No colors outside the palette (no greens, purples, warm hues).
- No word "English" on screen before Beat 3.
- No real creator faces/footage — creators appear only as in-app cards or the gradient avatar tile.
- No technology names on screen except GPT-5.6 and Codex.
- World A stays near-black `#0A0A0B`; World B stays light — never swap.
