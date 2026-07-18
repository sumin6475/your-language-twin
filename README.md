# Your Ideal Role Model

Web app for adults learning English: upload ~2–3 min of yourself speaking your **native
language**, get matched to a real **English creator** whose rhetorical style resembles yours —
to shadow. Direction is native-in → English-out.

**Start here:** [`AGENTS.md`](AGENTS.md) (Codex context) → [`docs/phase0-findings.md`](docs/phase0-findings.md)
(what's already settled) → [`docs/PRD.md`](docs/PRD.md) (full spec).

## Layout

```
AGENTS.md      # Codex context — read first
docs/
  PRD.md                 # product spec, scope, metrics, risks
  phase0-findings.md     # the matching science, already directionally settled
  translation-design.md  # style-preserving KO→EN translator design
reference/
  spike/       # READ-ONLY prior spike code — findings only, do not build on it
```

Fresh rebuild in Codex (2026-07-18). The prior Claude-Code project's build-system pack, venv,
model cache, and audio were intentionally left behind — only the leverage was carried over.
