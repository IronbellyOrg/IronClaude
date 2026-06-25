# D1 fix verification (design (b) — telemetry-honesty)

**Date:** 2026-06-24

## Falsifier discipline — fail-before → pass-after

- **Fail-before** (`../test-results/d1-failbefore.txt`): `test_snapshot_success_reports_children_only_not_full_snapshot` FAILED on the pre-fix tree — `assert 'snapshot' == 'snapshot-children-only'` (the runner emitted the overclaiming `"snapshot"`). 1 failed, 1 passed.
- **Pass-after** (`../test-results/d1-passafter.txt`): full suite **145 passed, 1 xpassed**. The new test now PASSES. Falsifier discipline satisfied (FAIL → PASS).

## Suite delta vs baseline

- Baseline (`baseline-summary.md`): 143 passed, 1 xpassed.
- Post-fix: 145 passed, 1 xpassed. Delta = **+2** = the two new tests in `test_reviewer_swarm_target_grounding.py` (`test_snapshot_success_reports_children_only_not_full_snapshot` + `test_disabled_path_unchanged_when_isolation_off`). No previously-passing test regressed.

## Authorized change to a pre-existing test (NOT a regression)

`tests/cli/reflect/test_reviewer_isolation_gate.py::test_clean_committable_grounds_reviewers_in_snapshot` line 84 was intentionally updated from `assert result.reviewer_isolation == "snapshot"` to `== "snapshot-children-only"` per the design-(b) decision record. This is the sanctioned correctness update to a pre-existing telemetry assertion (the value the runner now emits), explicitly authorized in Step 3.2 — distinct from any unexpected failure. It still passes.

## Flaky-test note (transient, not a regression)

During the post-ruff re-run, `test_fix_loop.py::test_non_convergence_exit10_five_launches` failed ONCE then passed 3/3 in isolation and in the subsequent full-suite run (145 passed). A cosmetic ruff reformat (collapsing the `ensemble.py` `reviewer_isolation` ternary to one line) cannot change runtime behavior; the one-off failure was test-ordering nondeterminism in an unrelated test (single retry flipped the result → classified flaky/Grounding-Gap, NOT a Regression, per the §6.1.1 exit-code taxonomy). Final deterministic state: green.

## Edit sites applied (design (b))

- `src/superclaude/cli/reflect/models.py` — `ReflectResult.reviewer_isolation` enum doc comment: added `snapshot-children-only`.
- `src/superclaude/cli/reflect/ensemble.py:315-316` — contract-telemetry branch emits `"snapshot-children-only"` when `reviewer_grounding_root` is set.
- `src/superclaude/cli/reflect/runner.py:682` — operator-visible `result.reviewer_isolation = "snapshot-children-only"` on the snapshot-success path.
- `tests/cli/reflect/test_reviewer_isolation_gate.py:84` — assertion updated to the honest value.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` Step 0.5e item 4 + telemetry line — rewritten to honestly state the children-only scope; `make sync-dev` + `make verify-sync` clean.
- NEW `tests/cli/reflect/test_reviewer_swarm_target_grounding.py` — the falsifier + a default-OFF regression guard.

## Ruff

`d1-ruff.txt`: all 5 changed files formatted clean (ensemble.py reformatted once, then clean).

## Default-OFF preserved

`test_disabled_path_unchanged_when_isolation_off` confirms the flag-off (#153) path never snapshots and still reports `reviewer_isolation == "disabled"` — no behavioral change when `reviewer_grounding_root` is unset.
