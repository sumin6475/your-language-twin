# DESIGN.md — Your Ideal Role Model

> The rules an AI (or a new designer) needs to build this app consistently.
> Values live in `tokens.json`. This file says **when to use what, and what never to do.**
> Load this into your agent's context every session.

---

## 1. What this app feels like

The app tells a user: *"here are real English speakers who think like you."*
The core emotion is **warm recognition** — "someone gets me" — delivered by a **thoughtful indie maker**, not a lab, not a soft ed-tech brand.

Everything below serves that feeling. When a choice is ambiguous, pick the one that feels **more human and more crafted**, not more "clean and modern-generic."

---

## 2. Color rules

**Blue is a guest, not the wallpaper.** It is white + grey by default, blue only at the emotional peaks.

- Use `blue.deep` (#1E40AF) ONLY for: primary buttons, the match/reveal screen background, and the single key highlight per screen.
- Use `blue.tint` (#EFF3FF) for small chips like the match-% badge.
- Everything else is `bg.base` / `bg.subtle` + `ink.*` text.
- **Do NOT** use blue for borders, body text, or decoration.
- **Do NOT** invent new colors. If you need one, it's a bug — ask.
- **Do NOT** use gradients as backgrounds. The only allowed gradient is the small avatar block (`blue.deep → blue.bright`).

**Text color:**
- Body/headlines → `ink.DEFAULT` (#18181B)
- Supporting text, the "why" paragraph → `ink.secondary` (#52525B)
- Roles, timestamps, meta → `ink.tertiary` (#71717A). This is the **lightest grey allowed for real text.** Never go lighter for anything a user needs to read.

---

## 3. Typography rules

- Headlines, names, eyebrows, buttons, section labels → **Clash Display** (`font-display`).
- Body, UI, the "why" paragraph → **Inter** (`font-body`).
- Headline weight 500–600. **Never thin/light weight headlines** (AI cliché).
- Uppercase is allowed only on small labels/eyebrows, and only at weight 500. **No light-weight all-caps.**
- Eyebrow/label floor is **12px**. Never smaller. An eyebrow you have to squint at reads as AI decoration.

---

## 4. The "human-feel" rules (this is what kills the AI smell)

These came from studying what makes a real, crafted site feel human. Follow them literally.

1. **Headlines are real sentences, not slogans.**
   - ❌ "Meet the voice that thinks like you"
   - ✅ "Turns out someone already speaks English the way you think."
   - Write the way a thoughtful person actually talks. Specific beats punchy.

2. **No em dashes (—).** They are the #1 AI writing tell. Use commas, periods, or "then".
   - ❌ "We studied how you think — then found your matches."
   - ✅ "We studied how you think, then found your matches."

3. **Keep body text short.** One tight sentence beats two padded ones. Cut every word that isn't earning its place.

4. **Use concrete, real-looking data everywhere.** Never ship `[Creator name]` / `92% match` placeholders in mockups. Use real names, real "why" sentences. Placeholder data makes a design look dead.

5. **Spacing is generous.** Section gaps ≥ 48px. Don't crowd. Whitespace is what makes it feel intentional, not templated.

---

## 5. Shape & depth rules

- Cards: `radius.lg` (16px) + `shadow.card`. Lifted/hero cards use `shadow.raised`.
- Buttons: `radius.md` (12px).
- Soft shadows only. No hard/black shadows, no heavy borders.
- Everything should feel *placed on a surface*, with quiet depth (the Ghost feeling).

---

## 6. Component inventory (MVP)

Build only these for now:

- **Button** — primary (blue.deep fill) / secondary (outline, ink border)
- **Card** — generic surface
- **MatchCard** — THE core component: avatar + name + role + match% chip + "why you're alike" text
- **Upload / Record zone** — the entry point (no account)
- **Consent checkbox** — required before processing
- **Thumbs up/down** — feedback on each match
- **Loading state** — the async pipeline runs in the background; this screen matters
- **EmptyState** — before upload / no result

---

## 7. AI-cliché guardrails (audit every screen against this)

- [ ] Tiny eyebrow / subtitle labels → keep ≥12px, weight 500+, opacity ≥0.85
- [ ] Light-weight, all-caps fonts → never
- [ ] Light grey as body text → `ink.tertiary` is the floor, meta only
- [ ] Inconsistent vertical rhythm → stick to the spacing scale (4/8/12/16/24/32/48)
- [ ] Purple gradients / generic hero → we use blue, and real-sentence headlines
- [ ] Em dashes in copy → never (see §4.2)
- [ ] Placeholder data in mockups → never (see §4.4)

**The loop:** every new AI-smell you catch → add a line here → it never comes back.

---

## 8. How to reference this when prompting

Paste or point your agent at this file, then:

> "Build [screen] using the tokens in `tokens.json` and the rules in `DESIGN.md`.
> Use only defined tokens, never invent colors. Follow the human-feel rules in §4
> and check your output against the guardrails in §7 before finishing."
