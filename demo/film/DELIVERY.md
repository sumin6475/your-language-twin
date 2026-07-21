# Language Role Model — Demo Film Delivery

Built with HyperFrames (HTML compositions, deterministic render) from
`demo/2026-07-21-demo-video-agency-brief.md`.

## Deliverables

- `renders/…​.mp4` — raw render (1920×1080, 30 fps, H.264 + AAC)
- `language-role-model-demo-master.mp4` — delivery master, −14 LUFS / ≤−1 dBTP
- `language-role-model-demo.srt` — VO captions (verbatim, accessibility)

## Spec checklist (§11 of the brief)

- [x] 1920×1080, 30 fps, H.264 MP4
- [x] Runtime 2:56.0 (< 3:00)
- [x] All VO lines verbatim per §8 (Kokoro TTS `af_heart`, unhurried)
- [x] `.srt` caption file included
- [x] Two visual worlds; every A↔B hand-off happens on a blue element
  (B1→B2 black cut · B2 collapse→blue bloom→aurora · evidence pill→B5 ·
  waveform merge→blue pulse→GPT-5.6 mark · B8 loop→blue node→B9)
- [x] Clash Display 600 (display) + Inter (body); exact product palette
- [x] First on-screen/spoken "English" is Beat 3
- [x] Only GPT-5.6 (reasoning engine) and Codex (engineering teammate) named
- [x] Beat 5 creator side = app gradient avatar + waveform (no real person)
- [x] Real matches appear only as in-app UI (Cinema Therapy MatchCard rebuild,
  real recording of results)

## Structure

| Beat | Time | Source |
| --- | --- | --- |
| 1 Hook | 0:00–0:11.6 | `compositions/b1.html` |
| 2 Cognitive compression | 0:12–0:22.4 | `compositions/b2.html` |
| 3+4 App spine | 0:21.6–1:20 | `compositions/spine.html` + root footage (`footage/seg_*`) |
| 5 Signature split | 1:19.4–1:38.4 | `compositions/b5.html` + `footage/sumin_1080.mp4` |
| 6 GPT-5.6 | 1:37.8–2:00.4 | `compositions/b6.html` |
| 7 Codex | 1:59.6–2:15.4 | `compositions/b7.html` (real repo artifacts) |
| 8 Network vision | 2:14.6–2:42 | `compositions/b8.html` + `footage/seg_vision.mp4` |
| 9 Close | 2:41.2–2:56 | `compositions/b9.html` |

## Audio

- Score: `audio/score.wav` — composed programmatically (`scripts/make_score.py`),
  restrained pads + felt-piano motif, automated to the 9-beat arc.
- VO: `audio/vo/*.wav` — regenerate with `npx hyperframes tts` if lines change.
- SFX: `audio/sfx/*` — soft ticks per agent check, warmer confirm on
  "Evidence verified", whooshes on the Codex montage, sub-hits at open/close.
- Remaster loudness: `scripts/master_audio.sh <in.mp4> <out.mp4>`.

## Re-render

```bash
cd demo/film
npm run check    # lint + layout + contrast
npm run render   # → renders/<timestamp>.mp4
scripts/master_audio.sh renders/<file>.mp4 language-role-model-demo-master.mp4
```
