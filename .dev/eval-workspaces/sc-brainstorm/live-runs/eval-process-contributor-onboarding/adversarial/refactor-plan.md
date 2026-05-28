---
phase: refactor-plan
base_variant: 3
layered_variants: [1, 2]
created: 2026-05-27T00:00:00Z
---

# Refactor Plan — Tooling-First Base + Docs + Process Layers

## Goal

Take Variant 3 (Architect / Tooling) as the foundation; layer high-leverage elements from Variant 1 (Scribe / Docs) and Variant 2 (PM / Process) without inflating sprint scope beyond what one 2-week sprint can ship.

## Sprint 1 (this sprint) — Mandatory

### Tooling (from Variant 3)

- `make onboard` — one-shot bootstrap target
- Smoke-test marker (`pytest -m smoke`, <30s wall time)
- Pre-commit hook `--explain` mode (verify-sync, markdownlint, freshness-pre-edit)
- `superclaude doctor --contributor` profile

### Docs (from Variant 1)

- `QUICKSTART.md` (top-level, ~150 lines, points at `make onboard`)
- `docs/contributor-guide/glossary.md`
- CONTRIBUTING.md gets a new "If a hook blocks you" appendix referencing the new `--explain` output

### Process (from Variant 2)

- PR template gets a "first PR" checkbox
- GitHub Action auto-comments on first-PR checkbox: 3 doc links + shepherd availability note
- `MAINTAINERS.md` lists current shepherd-available maintainers (no formal rotation in sprint 1)

## Sprint 2 (deferred, conditional) — Stretch

### From Variant 1

- Worked-example skill PR walkthrough (`docs/contributor-guide/worked-example-skill-pr.md`)

### From Variant 2

- 2-week cohort discussion thread (only if newcomer volume justifies — measure during Sprint 1)
- Sprint-retro post on contributor experience

### From Variant 3

- `.devcontainer/devcontainer.json` (Codespaces support)

## Dropped (out of scope this brainstorm)

- Maintainer-of-the-week formal rotation — PM proposal acknowledged but deferred until maintainer pool surveys confirm volunteer count.
- Three-doc reading rule — replaced by simpler 3-link auto-comment from PM variant.
- Issue-template per-label customization — kept simple in sprint 1; revisit if signal demands.

## Cross-Layer Coherence Checks

- `make onboard` script must reference `QUICKSTART.md` in its success output.
- `QUICKSTART.md` must direct contributors to `make onboard` as step 1.
- Hook `--explain` output must link to the failure-mode appendix in CONTRIBUTING.md.
- PR-template auto-comment must reference `make onboard` (not the legacy manual sequence).
- `superclaude doctor --contributor` failure messages must match QUICKSTART step numbers.

## Open Questions Carried Forward

- Hard threshold for "cohort cadence kicks in" — define a newcomer-PR count (e.g., 4+ first-PRs in a 2-week window) before enabling cohort threads.
- Whether `--explain` output should be machine-parseable (JSON) for future tooling — defer until a consumer exists.
