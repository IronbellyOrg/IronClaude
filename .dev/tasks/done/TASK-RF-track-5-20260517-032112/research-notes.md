# Research Notes: PR5 — CONTRIBUTING.md "CI Hygiene" + Pull-Sync workflow fix

**Date:** 2026-05-17
**Scenario:** A (explicit)
**Depth Tier:** Standard
**Track Count:** 5 (this is track 5)
**Order:** PR1 → PR2 → PR3 → PR4 → PR5

---

## EXISTING_FILES

**CONTRIBUTING.md**: ABSENT. Confirmed via `test -f CONTRIBUTING.md` → "ABSENT". PR5 must CREATE the file, not modify.

**Pull-Sync workflow**: `.github/workflows/pull-sync-framework.yml` (116 lines). Suspected root cause of failures:
- Line 112: `git push origin main` — but this repo's default branch is `master`, not `main`. Recent runs all failed on commit `71b1b1f` (master tip).
- Workflow runs every 6h via cron + manual dispatch.
- Workflow purpose: sync upstream `SuperClaude-Org/SuperClaude_Framework` into this fork's `commands/`, `agents/`, `.claude-plugin/plugin.json`, root `plugin.json`.

Other suspect lines in pull-sync workflow:
- Line 28: reads `plugin-repo/docs/.framework-sync-commit` — `.framework-sync-commit` file existence/path needs verification.
- Lines 14-18: checkout into `plugin-repo/` directory.
- Lines 67-73: PROTECTED list includes `core/`, `modes/` — neither path exists in this repo (verify via `ls`).

**Repo branch reality**: `git branch --show-current` = `master`. No `main` branch. Default branch = master (per recent merge PRs).

## PATTERNS_AND_CONVENTIONS

- Project workflow file conventions: `.github/workflows/*.yml` with `name:` field, `on:` triggers, `jobs:` definitions.
- Other workflows (`test.yml`, `quick-check.yml`) correctly target `master` and `integration`.
- No CONTRIBUTING.md → no existing style to match; can use standard markdown.

## GAPS_AND_QUESTIONS

- **Pull-sync workflow scope of fix**: Two minimum changes:
  1. `git push origin main` → `git push origin master` (line 112)
  2. Verify `PROTECTED` paths exist (or remove non-existent ones)
- **CONTRIBUTING.md content**: User specified "CI Hygiene" section. Must include:
  - Rot-budget rule: no PR may introduce new lint/test failures; pre-existing failures may stay
  - "New failure" definition: failure absent from most recent master CI run
  - Pre-PR local checks: `uv run ruff check src/ tests/`, `uv run pytest tests/<changed-area>/ -v`, `make verify-sync`
  - Explicit "social convention, not CI-enforced gate" disclaimer
- **Should PR5 also document the closeout convention discovered in this session?** (e.g., `.dev/releases/current/ → complete/` archival pattern with CLOSEOUT.md). Out of brainstorm scope; document as Open Question.

## RECOMMENDED_OUTPUTS

- Branch: `fix/ci-rot-pr5-contributing-and-pullsync`
- Single task file: `TASK-RF-track-5-20260517-032112.md`
- PR title: `docs(ci): add CONTRIBUTING.md CI Hygiene + fix pull-sync push target`

## SUGGESTED_PHASES

1. Preparation: confirm PR1+PR2+PR3+PR4 merged + branch + dev-deps
2. Discovery: inspect pull-sync workflow latest failure log; confirm `git push origin main` is the failing step
3. Execute:
   - 3.1 Create CONTRIBUTING.md with "CI Hygiene" section
   - 3.2 Edit `.github/workflows/pull-sync-framework.yml` line 112 `main` → `master`
   - 3.3 Audit PROTECTED list for nonexistent paths (`core/`, `modes/`); remove if absent
4. Verify:
   - 4.1 `gh workflow run pull-sync-framework.yml --ref fix/ci-rot-pr5-contributing-and-pullsync` (dispatch test) — confirm green
   - 4.2 CONTRIBUTING.md renders correctly (e.g., GitHub preview or `markdown-lint`)
   - 4.3 AC4: PR CI test-summary succeeds (depends on PR1-4 having merged)
5. Commit + PR

## TEMPLATE_NOTES

- Template 02 (complex) — multi-file create+edit with discovery
- QA_GATE_REQUIREMENTS: PER_PHASE
- VALIDATION_REQUIREMENTS: pull-sync workflow dispatch succeeds, CONTRIBUTING.md present, ruff+pytest still green, AC4 + AC5 met
- TESTING_REQUIREMENTS: NONE (no new code tests; workflow dispatch IS the integration test)

## AMBIGUITIES_FOR_USER

- Whether the pull-sync workflow's PROTECTED list should be reduced (`core/`, `modes/` are not in this fork) is open — default action: remove non-existent entries to silence false-positive protection-violation noise. Document in Open Questions.

---
**Status:** Complete
