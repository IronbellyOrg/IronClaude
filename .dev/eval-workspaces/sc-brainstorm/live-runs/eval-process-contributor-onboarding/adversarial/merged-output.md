---
phase: merged-output
schema_version: "1.0"
domain: process
strategy: agile
depth: standard
convergence_score: 0.82
status: PASS
created: 2026-05-27T00:00:00Z
---

# Merged Output — Contributor Onboarding Improvements (Agile)

Unified specification derived from 3 adversarial variants (scribe/pm/architect). Tooling-first foundation; layered docs + lightweight process. One-sprint shippable.

## Sprint 1 — Mandatory Deliverables (12 items)

### Tooling

1. `make onboard` — idempotent one-shot bootstrap (UV check, `make dev`, smoke tests, next-step output).
2. `pytest -m smoke` marker — <30s subset for env validation.
3. Pre-commit hook `--explain` mode for `verify-sync`, `markdownlint`, `freshness-pre-edit`.
4. `superclaude doctor --contributor` profile checking UV, editable install, sync diff, hooks, fork remote.

### Documentation

5. `QUICKSTART.md` (top-level, ~150 lines) linking to `make onboard` as step 1.
6. `docs/contributor-guide/glossary.md` covering skill/command/agent/hook/sync-dev/MDTM/persona/MCP.
7. CONTRIBUTING.md gains "If a hook blocked you" appendix referencing `--explain` output.

### Process

8. PR template gains "this is my first PR" checkbox.
9. GitHub Action auto-comments on flagged first-PRs with 3-link doc bundle + shepherd availability.
10. `MAINTAINERS.md` lists shepherd-available maintainers (informal, no rotation).

### Coherence Gates

11. All cross-references wired: `make onboard` → QUICKSTART, hook `--explain` → CONTRIBUTING appendix, PR auto-comment → QUICKSTART.
12. `make docs-check` (lightweight) verifies QUICKSTART command sequence still resolves.

## Sprint 2 — Deferred / Stretch (4 items, conditional)

- Worked-example skill PR walkthrough doc.
- `.devcontainer/devcontainer.json` for Codespaces.
- 2-week cohort discussion threads (gated on ≥4 first-PRs per fortnight).
- Sprint retro on contributor experience.

## Dropped

- Formal maintainer-of-the-week rotation (insufficient pool signal).
- Three-doc reading rule (replaced by simpler 3-link auto-comment).

## Success Metrics

- Median time-to-first-PR drops ≥30% within 8 weeks of Sprint 1 completion.
- Setup-related issues drop ≥50%.
- First-PR maintainer response time ≤48h median.
- Contributor return rate (2nd PR within 90 days) +25%.

## Constraints Preserved

- Pre-commit gates unchanged (verify-sync, markdownlint, ruff).
- UV-only Python operations.
- Source-of-truth discipline (`src/superclaude/` → `make sync-dev` → `.claude/`).
- Branch discipline (feature/* off integration).
- `.claude/` gitignore rule.

## Unresolved Conflicts

None blocking.

## Provenance

Base variant: V3 (Architect/Tooling). Layered: 3 V1 elements (docs), 3 V2 elements (process). Convergence 0.82.
