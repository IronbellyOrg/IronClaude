# QA Input Manifest — Step PG.1

**Timestamp:** 2026-06-04 05:28
**Task:** TASK-RF-20260604045025 — Fix CI hermeticity (Bug A canonical fixtures + Bug B brainstorm test)
**Purpose:** Review-ready bundle giving rf-qa everything needed to verify the task against real repo state without re-running discovery.

## Output file inventory (11 files)

| Path | Purpose |
|------|---------|
| phase-outputs/discovery/branch-setup.md | Records active branch `fix/ci-canonical-brainstorm-hermetic`, branched off `origin/master` SHA `80fd352`, stash `stash@{0}`, fixture persistence post-checkout |
| phase-outputs/test-results/gitignore-negation-check.md | `git check-ignore` proof: negation on `.gitignore:82` (after `*.log` line 79), all 6 targets un-ignored, 6 non-targets recorded as known-untracked-not-to-commit |
| phase-outputs/plans/bugA-commit.md | Bug A commit record: SHA `b9d533ff`, 7 files (6 fixtures + `.gitignore`), `.claude/` guard empty, no `-f` |
| phase-outputs/plans/bugB-test-rewrite.md | Bug B rewrite record: methods replaced/added, production + fallback test + `patch` import left untouched |
| phase-outputs/test-results/audit-canonical.txt | Raw pytest output for Bug A audit selection |
| phase-outputs/test-results/audit-canonical-summary.md | Bug A audit summary: 27 passed |
| phase-outputs/test-results/brainstorm-skill.txt | Raw pytest output for Bug B `-k skill` selection |
| phase-outputs/test-results/brainstorm-skill-summary.md | Bug B summary: 3 passed |
| phase-outputs/test-results/lint-format.txt | Raw ruff check + format-check output |
| phase-outputs/test-results/lint-format-summary.md | Lint/format summary: both clean |
| phase-outputs/plans/phase3-verdict.md | Phase 3 consolidated verdict: PASS |

## Key results for rf-qa verification

### Bug A — `.gitignore` negation + 6-fixture commit
- **Commit SHA:** `b9d533ff230d79afb689dde231fb73f45f32217d`
- **Committed file list (7):** 6 fixtures (D-0056/fixture-F-5-5-5-halt-cycle-2.log, D-0057/fixture-pass1-fail2-shrinking.log, D-0057/fixture-pass1-fail2-non-shrinking.log, D-0059/fixture-cross-cycle-dedup-shrinking.log, D-0059/fixture-cross-cycle-dedup-non-shrink.log, D-0060/fixture-slow-shrink-F-5-4.log) + `.gitignore`
- **Negation:** `!.dev/releases/**/artifacts/**/fixture-*.log` at `.gitignore:82`, appended AFTER `*.log` (line 79)
- **`.claude/` guard:** EMPTY; `git add -f` NOT used

### Bug B — hermetic test rewrite
- `tests/cli_portify/test_brainstorm_gaps.py`: `test_skill_not_available_returns_false` rewritten to HOME-redirect via `monkeypatch.setenv("HOME", str(tmp_path))` (no longer patches `check_brainstorm_skill_available`); new `test_skill_available_returns_true` added
- `test_fallback_activates_with_warning` UNCHANGED; `from unittest.mock import patch` import RETAINED
- `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py` UNMODIFIED

### Phase 3 test summaries
- **Bug A audit (`-k Canonical`):** PASS — 27 passed
- **Bug B brainstorm (`-k skill`):** PASS — 3 passed
- **ruff check:** PASS (All checks passed)
- **ruff format --check src/ tests/:** PASS (784 files already formatted)

### Phase 3 consolidated verdict
- **PASS** — no further fixes needed (per `phase3-verdict.md`).
