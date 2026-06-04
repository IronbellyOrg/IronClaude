# QA Report — Task Integrity (Phase 5, Test Coverage)

**Topic:** v4.3.0 sprint rerun-tasks — Phase 5 test suite (4 NEW + 5 EDITED files)
**Date:** 2026-06-02
**Phase:** task-integrity
**Fix cycle:** N/A (first pass)
**Fix authorization:** true (adversarial stance)

---

## Scope and Method

Verified the 9 in-scope test files in the git worktree
`/config/workspace/IronClaude/.claude/worktrees/SprintReRun/tests/sprint/`.
Every criterion was checked by READING the actual test source and, where the
criterion concerns behavior, RUNNING `uv run pytest` from the worktree root.
Zero-trust: the aggregation report and pytest summary were NOT taken at face
value — the 54-pre-existing-failure claim and the green/red regression
question were independently re-derived (git stash of the 5.9 edit + run at
HEAD).

Pre-existing-failure exclusion was re-proven, not assumed (see Criterion 9).

---

## Criterion 1 — Mirror structure (research §2)

**Contract:** the 4 NEW files mirror `test_checkpoints.py` conventions (module
docstring, section-banner comments, `tmp_path`, module-level `_` helpers, no
shared conftest, one `TestXxx` class per concept).

**Finding (READ all 4 files):**
- Module docstring: present in all 4 (`test_recovery.py:1`, `test_rerun_tasks.py:1-21`,
  `test_rerun_tasks_e2e.py:1`, `test_rerun_tasks_failure_modes.py:1-19`).
- Section-banner comments (`# ----`): present in all 4 (e.g. `test_recovery.py:23,85,135,153,252,281`).
- `tmp_path` used throughout (built-in); no `tests/sprint/conftest.py` introduced.
- Module-level `_`-prefixed helpers, not fixtures: `_seed_release`, `_bundle_with_sidecar`
  (recovery); `_task_block`, `_write_phase_tasklist`, `_seed_orchestration` (rerun_tasks);
  `_write_index_and_phase`, `_seed_failed_phase`, `_popen_factory_all_pass` (e2e);
  `_write_sprint`, `_phase_result_payload`, `_invoke`, `_passing_executor` (failure-modes).
- One `TestXxx` class per concept: confirmed via collect-only.

**Result: PASS** [VERIFIED — Read ×4]

## Criterion 2 — `from __future__ import annotations` (research §1.1)

**Contract:** present in all 4 NEW files.

**Finding (Grep):**
```
test_recovery.py:3 / test_rerun_tasks.py:23 / test_rerun_tasks_e2e.py:3 / test_rerun_tasks_failure_modes.py:21
```
All four present.

**Result: PASS** [VERIFIED — Grep]

## Criterion 3 — AC1–AC8 coverage + AC3-merge invariant (Resolution 3)

**Contract:** each AC maps to ≥1 collected, real test; AC3 (merged into AC2
round-trip per Resolution 3) must genuinely assert the verify-checkpoints /
round-trip invariant, not merely AC2's rename/flip/event.

**Finding (collect-only + Read):**
- `--collect-only` of the two AC files = 10 tests collected (2 e2e + 8 failure-mode).
- AC1: `TestRerunTasksDryRun::test_dry_run_prints_plan_does_not_execute` — asserts
  `mock_popen.assert_not_called()` + `[dry-run]` plan printed (e2e:160-186).
- AC2: round-trip test asserts originals renamed to `*.failed-<ts>` (Invariant 1),
  `SUPERCLAUDE-RERUN`/`rerun_history:` flipped on source (Invariant 2), exactly one
  `phase_rerun_complete` event (Invariant 3) (e2e:263-289).
- AC3 (merged): the SAME test additionally asserts **Invariant 4** — `verify-checkpoints
  --recover` was auto-invoked (`mock_verify.called`; argv contains `verify-checkpoints`
  AND `--recover`, e2e:291-298) — AND the **round-trip artifact-equivalence** form:
  merged `phase-7-result.json` retains both target task_ids and appends `recovery_history`
  (e2e:300-311). These are distinct invariants from AC2; AC3 is genuinely asserted.
- AC4–AC8: mapped to the 8 failure-mode tests; each asserts a byte-exact production
  abort string or restore invariant (locking PID, SHA mismatch + `--force-merge`,
  retry-cap "rerun 3 times", legacy transcript fallback spy, abort-restore bytes).

Resolution 3 (research 06 §Resolution 3, line 70) explicitly authorizes the AC2+AC3
merge ("Merge AC2+AC3 into one round-trip equivalence test"). Compliant.

**Result: PASS** [VERIFIED — Bash collect-only + Read]

## Criterion 4 — Test count (mandated 49 in PG5 band 34–50; 55 total with 6 extras)

**Contract:** judge whether the 6 documented extras are legitimate or padding;
flag any non-asserting "test".

**Finding (git-diff tally + Read):** total NEW `def test_` across all 9 files = **55**
(recovery 12, rerun_tasks 13, e2e 2, failure-modes 8, cli_contract +5, models +4,
executor +5, checkpoints +3, backward_compat +3). Mandated 49 is in the 34–50 band.
The 6 extras:
- 4 import-surface smoke in `test_recovery.py::TestRecoverySurfaceSmoke` — each makes
  a real assertion (`ManualNominator.nominate == [...]`, lock round-trip exists/removed,
  `retry_count_for_task == 1`). Not padding; they exercise the mandated import surface
  so ruff F401 does not fire.
- 1 R-F4 regression (`test_rerun_tasks.py::TestRerunNameMatchRegression`) — real regex
  assertions (see Criterion 10).
- 1 extra transient trigger (`test_executor.py::...connection_refused...`) — asserts
  `FAIL_RECOVERABLE` on the ConnectionRefused marker.

No `assert True`, no empty test bodies (fake-green scan, Criterion 10). All 6 extras assert.

**Result: PASS** [VERIFIED — git diff + Read]

## Criterion 5 — Integration markers (research §1.6)

**Contract:** every test in `test_rerun_tasks_e2e.py` and `test_rerun_tasks_failure_modes.py`
is `@pytest.mark.integration`.

**Finding (Grep):** the marker is applied at CLASS level on all 6 test classes across the
two files (e2e: lines 156, 210; failure-modes: 249, 286, 363, 423, 477). A class-level
mark applies to every method, so all 10 tests inherit `integration`. No un-marked class.

**Result: PASS** [VERIFIED — Grep]

## Criterion 6 — Subprocess mocking, no real spawn (research §4)

**Contract:** e2e/failure-mode tests use stacked `patch()` and never spawn a real
process; Popen / `execute_sprint` / `subprocess.run` are patched.

**Finding (Grep + Read):**
- e2e dry-run: patches `superclaude.cli.pipeline.process.subprocess.Popen` and asserts
  `assert_not_called()` (e2e:164-182).
- e2e round-trip: stacked patches on `executor.shutil.which`, `process.subprocess.Popen`
  (Popen factory), `process.os.setpgrp`, `notify._notify`, and
  `rerun_tasks.subprocess.run` (e2e:228-242). No real spawn.
- failure-modes: every test patches `executor.execute_sprint` (side_effect stub) and
  `rerun_tasks.subprocess.run` (lines 313/316, 345/349, 405/409, 453/457, 497/500, 524/529);
  abort-path tests reach the abort before any executor call. AC4 pre-creates the lock so
  the abort fires before nomination. No real process spawns in any of the 10 tests.

**Result: PASS** [VERIFIED — Grep + Read]

## Criterion 7 — CliRunner (research §1.1)

**Contract:** CLI/contract tests use `CliRunner`.

**Finding (Read):** `CliRunner` imported and used in `test_rerun_tasks_e2e.py:12,162,221`,
`test_rerun_tasks_failure_modes.py:29,213` (via `_invoke`), and
`test_cli_contract.py::TestRerunTasksContract` (`setup_method` instantiates `self.runner`,
lines 96-97; all 5 methods invoke `sprint_group`).

**Result: PASS** [VERIFIED — Read]

## Criterion 8 — No duplicate test names within a class

**Contract:** no shadowed/colliding test names.

**Finding (Bash uniq -d on each NEW file):** zero duplicates in any of the 4 NEW files.
Edited-file new classes were collected without collision (`--collect-only` showed unique
nodeids; full runs green).

**Result: PASS** [VERIFIED — Bash]

## Criterion 9 — Zero regressions (independently re-derived)

**Contract:** no Phase 5 edit turned a previously-GREEN test red. The 54 pre-existing
failures + 2 collection errors must be excluded from the Phase 5 regression judgment.
Specifically check the `test_e2e_success.py` `stdin=None` edit (5.9 author).

**Finding (Bash — git stash + run-at-HEAD; the strongest available proof):**

1. **Full sprint suite, current working tree (Phase 5 in place):**
   `54 failed, 959 passed, 20 warnings, 2 errors` — byte-identical to the documented baseline.
2. **Edited files in scope, full runs:**
   - `test_cli_contract.py` + `test_models.py` + `test_checkpoints.py` +
     `test_backward_compat_regression.py` = **215 passed, 0 failed.**
   - `test_executor.py` = **5 failed, 80 passed.** The 5 failures are in
     `TestExecuteSprintIntegrationCoverage` (×4) + `TestBackwardCompat` (×1), all
     `AttributeError: '_PassPopen' object has no attribute 'stdin'` — i.e. the pre-existing
     fake-Popen tech-debt, NOT the Phase 5 new classes (`TestPhaseResultJsonWrite`,
     `TestFailClassificationHeuristic` both green). 75→80 reconciliation holds.
3. **`test_e2e_success.py` `stdin=None` edit — re-derived independently:**
   - Working tree (with the edit): **6 failed**, failure mode `IndexError: list index
     out of range` (the test's own Popen factory `config.phases[call_count[0]-1]` is
     called more times than phases exist).
   - I `git stash`ed ONLY the `test_e2e_success.py` edit and re-ran at HEAD `f902d010`:
     **6 failed**, failure mode `AttributeError: '_FakePopenSuccess' object has no attribute
     'stdin'`.
   - **Conclusion:** all 6 tests in `test_e2e_success.py` were ALREADY red at HEAD before
     the edit. The `stdin=None` edit changed the failure *mode* (AttributeError → IndexError)
     but turned **zero green tests red**. Per the gate criterion ("no previously-GREEN test
     red"), this is **NOT a regression.**
   - **However** (see Issue #1): the edit's stated purpose ("fake-Popen `stdin=None` fix to
     enable the 5.9 reuse test") is NOT achieved — the file remains 6-of-6 red. The edit is
     INEFFECTIVE and its inline comment + the aggregation's "incidental fix" framing are
     misleading. `test_e2e_success.py` is NOT in this gate's fix-authorization path list, so
     it is flagged IMPORTANT, out-of-scope-for-fix, not a gate blocker.

**Result: PASS (no green→red regression).** [VERIFIED — Bash git stash + run-at-HEAD ×3]

## Criterion 10 — No fake-green

**Contract:** scan for weakened assertions (`assert True`, bare `pytest.xfail`,
trivially-true mock-call asserts, try/except swallowing failures). The R-F4 test must
genuinely assert the widened `PHASE_FILE_PATTERN`.

**Finding (Grep + Read of production regex):**
- Grep for `assert True | pytest.xfail | pytest.skip | except…: pass` across all 4 NEW
  files = **0 hits**. The one `except click.ClickException: pass` (`test_rerun_tasks.py:144`)
  is a legitimate "raises-OR-returns-empty" contract branch: the test first asserts the
  empty-branch outcome on disk (line 140), then tolerates the documented raise on a
  malformed ID. Not a swallowed failure.
- R-F4 (`test_rerun_tasks.py::TestRerunNameMatchRegression`): asserts
  `PHASE_FILE_PATTERN.search("phase-7r-tasklist.md") is not None`, that the captured group
  == `["7"]`, AND that the canonical `phase-7-tasklist.md` still matches. I READ
  `src/superclaude/cli/sprint/config.py:20-29` and confirmed the pattern genuinely carries
  the v4.3.0 alternation `phase-(\d+)r-tasklist\.md` (line 27). The assertion is real and
  the production widening exists.
- The round-trip's `mock_verify.called` assertion is NOT trivially true: the mock is
  installed for the auto-`verify-checkpoints --recover` boundary, and the test further
  inspects `call_args.args[0]` for both `verify-checkpoints` and `--recover` tokens.

**Result: PASS** [VERIFIED — Grep + Read]

---

## Production-Surface Cross-Check (zero-trust import resolution)

Grepped the production modules to confirm every imported symbol exists (so no test is a
green-on-a-stub illusion):
- `recovery.py`: `RecoveryStatus`, `RecoveryBundle`, `RecoveryBundleRef`, `ManualNominator`,
  `ReflectReportNominator`, `compute_tasklist_sha256`, `write_recovery_audit_log`,
  `acquire_recovery_lock`, `release_recovery_lock`, `retry_count_for_task`,
  `merge_recovery_bundle` — all present (lines 58–381).
- `rerun_tasks.py`: `extract_phase_subset`, `build_rerun_bundle_dir`, `build_sub_index`,
  `walk_dependencies`, `discover_failed_tasks_from_transcripts`, `flip_target_checkboxes`,
  `restore_checkboxes_on_abort`, `finalize_checkboxes_on_success`,
  `select_default_recoverable_tasks`, `run_rerun_tasks` — all present (lines 90–1193).
- `executor.py`: `_write_phase_result_json` (2053), `_is_transient_failure` (1782),
  `_run_task_subprocess` (1079) — all present.

No hallucinated imports. All NEW tests run against real production symbols.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Mirror structure (§2) | PASS | Read ×4: docstrings, banners, `_` helpers, no conftest |
| 2 | `from __future__` header | PASS | Grep: present in all 4 NEW files |
| 3 | AC1–AC8 + AC3-merge invariant | PASS | collect-only=10; AC3 asserts verify-checkpoints --recover + round-trip equivalence |
| 4 | Test count (49 mandated; 55 w/ 6 extras) | PASS | git-diff tally=55; all 6 extras assert real invariants |
| 5 | Integration markers | PASS | Grep: class-level mark on all 6 classes → all 10 tests |
| 6 | Subprocess mocking, no spawn | PASS | Grep+Read: Popen/execute_sprint/subprocess.run patched |
| 7 | CliRunner | PASS | Read: used in e2e, failure-modes (`_invoke`), cli_contract |
| 8 | No duplicate test names | PASS | Bash uniq -d: 0 dups |
| 9 | Zero regressions | PASS | git stash + run-at-HEAD: test_e2e_success 6-red at HEAD pre-edit; no green→red |
| 10 | No fake-green; R-F4 real | PASS | Grep 0 weakened asserts; Read config.py:27 confirms widened pattern |

## Summary

- Checks passed: **10 / 10**
- Checks failed: 0
- Critical issues: 0
- Issues found (non-blocking): 1 IMPORTANT (out-of-scope-for-fix)
- Issues fixed in-place: 0

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `tests/sprint/test_e2e_success.py:44-49` | The 5.9 `self.stdin = None` edit does NOT make the file green — all 6 tests still fail (`IndexError` in the test's own Popen factory). The inline comment ("makes the guarded write a no-op…") and the aggregation's "incidental fix to enable the 5.9 reuse test" framing are misleading: the file was already 6-of-6 red at HEAD (`AttributeError: stdin`) and remains 6-of-6 red after the edit. | Either (a) complete the fix — the factory's `config.phases[call_count[0]-1]` overruns because the executor now spawns more subprocesses than phases once the stdin write is a no-op; the factory must clamp the index or the fake must drive the poll/wait loop to a single spawn per phase — OR (b) revert the cosmetic edit and leave the file in the pre-existing-failure bucket with no misleading comment. **NOT actioned in this gate: `test_e2e_success.py` is outside this gate's fix-authorization path list. Routed to the pre-existing-suite-breakage cleanup task (carry-forward #2).** |

## Actions Taken

None. All 10 criteria passed. The single IMPORTANT finding concerns
`test_e2e_success.py`, which is explicitly outside this gate's fix-authorization
path list (PATH DISCIPLINE). No in-scope file required a fix:
- 35 NEW tests across the 4 NEW files: **35 passed.**
- New classes in the 5 EDITED files: **20 passed** (cli_contract 5, models 4,
  executor 5, checkpoints 3, backward_compat 3).
- `uv run ruff check` on all 9 in-scope files: **All checks passed.**

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 6 | Glob: 0 | Bash: 12
  (no web research performed; Tavily not engaged — all verification was local source-truth)
- Every checklist item carries tool evidence cited inline above. Tool-call count
  (29 Read/Grep/Bash) exceeds the 10-criterion minimum; no padding — each call
  targeted a specific criterion.
- Unchecked items: none. Unverifiable items: none.

## Recommendations

1. **Green light Phase 5** for the rerun-tasks task-integrity gate. The Phase 5
   test work is correct, asserts real invariants, introduces zero regressions, and
   covers AC1–AC8.
2. Carry forward the `test_e2e_success.py` ineffective-edit finding (Issue #1) to the
   pre-existing-suite-breakage cleanup task. It does not block this gate.
3. The SHA-guard self-trip (HIGH, carry-forward #1) is correctly routed to Step 6.7
   qualitative QA — out of scope for this structural test-integrity gate. The tests
   honestly document the `--force-merge` workaround inline rather than hiding it.

## QA Complete

VERDICT: PASS
