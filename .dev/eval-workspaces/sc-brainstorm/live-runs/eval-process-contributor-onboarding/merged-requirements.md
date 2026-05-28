---
schema_version: "1.0"
spec_type: requirements
topic: "improving onboarding workflow for new contributors"
domain: process
strategy: agile
depth: standard
proposal_count: 3
convergence_score: 0.82
adversarial_status: PASS
handoff_target: none
created: 2026-05-27T00:00:00Z
source_seed_brief: ../seed-brief.md
source_adversarial_dir: ./adversarial/
---

# Merged Requirements — New Contributor Onboarding Improvements

## 1. Problem Statement

New open-source contributors face avoidable friction in their first 30-90 minutes with the SuperClaude repository: environment setup hiccups (UV vs pip confusion), opaque pre-commit hook failures (verify-sync, markdownlint, freshness-pre-edit), and a steep conceptual model around the skill / slash-command / source-of-truth architecture. This drives drop-off before a first PR, depresses contributor return rate, and indirectly burdens maintainers with repetitive setup questions. The goal is to reduce time-to-first-PR and lift contributor return rate via agile, one-sprint-shippable improvements layered on the existing CONTRIBUTING flow.

## 2. Objectives

- **O1.** Reduce median time-to-first-PR by ≥30% within 8 weeks of Sprint 1 completion.
- **O2.** Reduce setup-related GitHub issues (UV install, sync-dev confusion, hook failures) by ≥50%.
- **O3.** Achieve median first-PR maintainer response time ≤48h.
- **O4.** Increase contributor return rate (2nd PR within 90 days) by ≥25%.
- **O5.** Keep all existing quality gates (verify-sync, ruff, markdownlint, freshness checks) intact — no loosening.

## 3. Functional Requirements

### Sprint 1 — Mandatory

- **FR-1. `make onboard` target** — idempotent one-shot bootstrap: verify UV install (instruct install if missing), run `make dev`, run smoke-tests, print next-step links. Exits non-zero with remediation hints on failure.
- **FR-2. Smoke-test marker** — tag foundational tests with `@pytest.mark.smoke`; `uv run pytest -m smoke` completes <30s.
- **FR-3. Pre-commit `--explain` mode** — each gating hook (verify-sync, markdownlint, freshness-pre-edit) emits structured "BLOCKED / Why / Fix / Docs" output on failure.
- **FR-4. `superclaude doctor --contributor` profile** — checks UV active, editable install, `make sync-dev` produces no diff, hooks registered, remote is fork.
- **FR-5. `QUICKSTART.md`** — top-level, ≤150 lines, decision-tree-style first-PR path; `make onboard` is step 1.
- **FR-6. `docs/contributor-guide/glossary.md`** — defines skill, slash command, agent, hook, sync-dev, source-of-truth, MDTM, persona, MCP.
- **FR-7. CONTRIBUTING.md appendix** — "If a hook blocked you" failure-mode reference, cross-linked from `--explain` output.
- **FR-8. PR template "first PR" checkbox** — added to `.github/PULL_REQUEST_TEMPLATE.md`.
- **FR-9. First-PR auto-comment Action** — GitHub Action posts 3-link doc bundle + shepherd availability when checkbox is set.
- **FR-10. `MAINTAINERS.md` shepherd-available list** — informal list of maintainers committing to <48h first-response on first PRs.
- **FR-11. Cross-reference coherence** — `make onboard` mentions QUICKSTART, hook `--explain` links to CONTRIBUTING appendix, auto-comment references QUICKSTART, doctor messages mirror QUICKSTART step numbers.
- **FR-12. `make docs-check` target** — smoke-runs the QUICKSTART command sequence in CI to prevent doc drift.

### Sprint 2 — Deferred / Stretch

- **FR-13.** Worked-example skill PR walkthrough document.
- **FR-14.** `.devcontainer/devcontainer.json` for Codespaces / VS Code Dev Containers.
- **FR-15.** 2-week newcomer cohort GitHub Discussion threads — conditional on ≥4 first-PRs per fortnight signal.
- **FR-16.** Sprint retro on contributor experience (every 4 weeks).

## 4. Non-Functional Requirements

- **NFR-1. Backward compatibility** — no breaking changes to existing CONTRIBUTING.md, Makefile, or pre-commit hooks. Additive only.
- **NFR-2. Async-first** — no requirement that contributors join synchronous calls or meetings.
- **NFR-3. Maintainer overhead** — additional maintainer time per first-PR ≤15 minutes (auto-comment automates the boilerplate).
- **NFR-4. Performance** — `make onboard` completes in ≤5 minutes on a clean machine with UV installed; `pytest -m smoke` ≤30s.
- **NFR-5. Maintainability** — hook `--explain` strings co-located with hook logic; reviewed together.
- **NFR-6. Accessibility** — all docs in plain Markdown, no embedded media that requires JS to render.
- **NFR-7. Sprint scope** — Sprint 1 deliverables (FR-1 through FR-12) ship in ≤2 weeks of focused effort.

## 5. Acceptance Criteria

- **AC-1.** `make onboard` succeeds on a freshly cloned repo with UV installed; emits a "ready to contribute" summary on success.
- **AC-2.** Each of the 3 hooks emits structured `--explain` output covering its top failure modes.
- **AC-3.** `QUICKSTART.md` is linked from `README.md` above CONTRIBUTING.md.
- **AC-4.** A PR with the first-PR checkbox triggers exactly one auto-comment from the new Action.
- **AC-5.** `MAINTAINERS.md` lists ≥3 shepherd-available maintainers before launch.
- **AC-6.** All FR-11 cross-references resolve to valid anchors (verified via a CI link-check).
- **AC-7.** `make docs-check` is wired into CI and passes on integration branch.
- **AC-8.** Existing pre-commit gates (verify-sync, ruff, markdownlint, freshness-pre-edit) remain unchanged in behavior — only output format is augmented.
- **AC-9.** A baseline measurement of current time-to-first-PR is captured before launch; a post-launch measurement is captured at 8 weeks.

## 6. Provenance

This specification was produced by `/sc:brainstorm` (case: process-contributor-onboarding) on 2026-05-27.

### Source variants

- **V1 (opus:scribe — documentation-first):** contributed FR-5 (QUICKSTART), FR-6 (glossary), FR-7 (CONTRIBUTING appendix), FR-13 (worked-example PR, deferred).
- **V2 (sonnet:pm — process / sprint cadence):** contributed FR-8 (PR template), FR-9 (auto-comment Action), FR-10 (shepherd list — formal rotation downgraded), FR-15/FR-16 (cohort + retro, deferred).
- **V3 (haiku:architect — tooling-first) [BASE]:** contributed FR-1 (`make onboard`), FR-2 (smoke marker), FR-3 (hook `--explain`), FR-4 (`doctor --contributor`), FR-14 (devcontainer, deferred). Selected as base via base-selection rubric (22/25).

### Convergence

- **Score:** 0.82 (target: 0.75) — PASS.
- **Resolved tensions:** (1) docs vs hooks → both, composed; (2) cohort cadence vs volume → defer to Sprint 2 with explicit threshold; (3) Codespaces vs local → local-first Sprint 1, devcontainer additive Sprint 2; (4) worked-example PR maintenance burden → defer with update-trigger documented.
- **Dropped:** formal maintainer-of-the-week rotation (insufficient pool signal); three-doc reading rule (replaced by 3-link auto-comment).

### Artifacts

- Seed brief: `../seed-brief.md`
- Variants: `./adversarial/variant-1-scribe.md`, `./adversarial/variant-2-pm.md`, `./adversarial/variant-3-architect.md`
- Debate transcript: `./adversarial/debate-transcript.md`
- Base selection: `./adversarial/base-selection.md`
- Refactor plan: `./adversarial/refactor-plan.md`
- Merge log: `./adversarial/merge-log.md`
- Merged output (adversarial): `./adversarial/merged-output.md`

### Defaults applied (non-interactive run)

- Audience: external OSS contributors with mixed Python/CLI experience.
- Success metrics: time-to-first-PR, drop-off rate at setup, contributor return rate.
- Scope cap: one 2-week sprint for mandatory items.
- Constraints preserved per `seed-brief.md` `must_preserve`.

### Out of scope (per seed brief)

- Paid contributor tracks; mandatory synchronous mentoring; full CONTRIBUTING.md rewrite; loosening of any quality gate; new contributor auth system; `src/superclaude/` package restructure; custom contributor portal app.
