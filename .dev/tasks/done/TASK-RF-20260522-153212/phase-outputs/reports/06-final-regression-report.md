# cliEval Remediation — Final Regression Report

Task: TASK-RF-20260522-153212
Date: 2026-05-22T18:47:05Z

## Phase 1 — Baselines

01-eval-doctor-help-baseline.txt
01-eval-run-help-baseline.txt
01-grep-gates-pre.txt
01-line-number-reconfirm.txt
01-pytest-baseline.txt
01-ruff-baseline.txt
01-verify-sync-baseline.txt

## Phase 2-5 — Test Results (per-phase)

02-pytest-red-baseline.txt
02-ruff.txt
02-verify-sync.txt
03-h2-pytest.txt
03-h3-pytest.txt
03-h4-pytest.txt
03-m2-pytest.txt
03-m3-pytest.txt
03-pytest.txt
03-ruff.txt
03-verify-sync.txt
04-pytest.txt
04-ruff.txt
04-verify-sync.txt
05-cc1-pytest.txt
05-cc2-pytest.txt
05-m5-pytest.txt
05-m6-doctor-help.txt
05-m6-run-help.txt
05-pytest.txt
05-ruff.txt
05-t8-pytest.txt
05-t9-pytest.txt
05-verify-sync.txt
06-eval-run-help-diff.txt
06-eval-run-help-post.txt
06-grep-gates-final.txt
06-pyproject-diff.txt
06-pytest-final.txt
06-ruff-final.txt
06-verify-sync-final.txt

## QA Gate Reports

PG-1-input-summary.md
PG-1-rf-qa-report.md
PG-2-input-summary.md
PG-2-rf-qa-report.md

## Plans + Verdicts

01-oq-decisions.md
PG-1-final-verdict.md
PG-2-final-verdict.md
PG-2-verdict.md

## Final Gate Results (Step 6.1/6.2/6.3)

=== GATE 1 (H1): grep -rn 'run_dir=resolved_output' src/superclaude/cli/eval/ ===
0
(0 hits — PASS)

=== GATE 2 (H5): home_root.mkdir vs runtime_allowed ordering in commands.py ===
1765:    # ``home_root.mkdir`` below so the path is in the allowlist at the
1768:    runtime_allowed = tuple(base_config.allowed_scratch_roots) + (
1773:    runtime_config = EvalConfig(
1776:        allowed_scratch_roots=runtime_allowed,
1783:    home_root.mkdir(parents=True, exist_ok=True)

=== GATE 3 (CC1 per OQ-1): re.compile of eval-id patterns ===
Total re.compile() calls in eval module: 9
src/superclaude/cli/eval/artifact_layout.py:101:_EVAL_ID_PATH_SAFETY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
src/superclaude/cli/eval/artifact_layout.py:108:EVAL_ID_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$")

=== GATE 4 (CC2): no literal sys.exit(N) or Exit(N) ===
0
(0 hits — PASS)

=== GATE 5 (CC2 per OQ-2): no *_EXIT_CODE = <literal-int> outside exit_codes.py ===
0
(0 hits outside exit_codes.py — PASS)

## AC Matrix Summary

| **T7** | session_id orchestrator ownership | Step 5.7 | (test addition only) | test_run_one_spec_uses_orchestrator_allocate_session_id in test_orchestrator.py | phase-outputs/test-results/05-m5-pytest.txt | RESOLVED |
| **T8** | EVAL_ID_PATTERN single-source-of-truth | Step 5.2 | (test addition only) | test_eval_id_pattern_single_source in test_eval_id_regex.py | phase-outputs/test-results/05-t8-pytest.txt | RESOLVED |
| **T9** | no magic exit codes outside exit_codes.py | Step 5.4 | (test addition only — plus docstring fix in commands.py:23) | test_no_magic_exit_code_literals_in_eval_module in test_exit_codes.py | phase-outputs/test-results/05-t9-pytest.txt | RESOLVED |

## Summary

- **Total findings tracked:** 23 rows (5 High + 6 Medium + 3 CC + 9 Tests = 23; CC3 rolls into M2 per spec §5 but still gets a row pointing at M2's evidence).
- **Status breakdown:**
  - **RESOLVED:** 22 (5 High + 5 Medium [M2-M6] + 2 CC [CC1+CC2] + 1 CC3-via-M2 + 9 Tests)
  - **DEFERRED-SPEC §4:** 1 (M1 — see Follow-Up Items + OQ-3 decision)
- **Resolution rate:** 22/23 (95.6%) RESOLVED; 1/23 (4.3%) deferred-with-rationale; 0 SKIPPED, 0 WONTFIX.
- **Test additions:** 9 new test functions (T1-T9) + 1 collateral positive test (T5b) = 10 new tests.
- **New source files:** 1 (`src/superclaude/cli/eval/exit_codes.py`).
- **Source files modified:** 9 (commands.py, coverage.py, config.py, isolation.py, reporter.py, run_report.py, artifact_layout.py, loader.py, orchestrator.py, models.py, **init**.py — count includes models.py + **init**.py M3 re-exports).

## Phase Gate Verdicts

- **PG-1** (Phase 2 test scaffolding QA): PASS at cycle 1 — see `phase-outputs/plans/PG-1-final-verdict.md`.
- **PG-2** (Phase 4 layout + ordering QA): PASS at cycle 1 — see `phase-outputs/plans/PG-2-final-verdict.md`.
- **PG-FINAL** (composite task-integrity): pending — Step PG-FINAL.2 spawns rf-qa with `fix_authorization: true`.

## Static Grep Gates (VALIDATION_REQUIREMENTS §5)

| Gate | Description | Expected | Actual | Status |
|---|---|---|---|---|
| GATE 1 | H1 — `run_dir=resolved_output` | 0 hits | 0 hits | PASS |
| GATE 2 | H5 — `runtime_allowed` precedes `home_root.mkdir` in commands.py | runtime_allowed line < home_root.mkdir line | L1768 < L1783 | PASS |
| GATE 3 | CC1 — `re.compile` of eval-id patterns | 2 in artifact_layout.py, 0 in loader.py | 2 in artifact_layout.py, 0 in loader.py | PASS |
| GATE 4 | CC2 — `sys.exit(N)` / `Exit(N)` literals | 0 hits | 0 hits | PASS |
| GATE 5 | CC2 per OQ-2 — `*_EXIT_CODE = <literal-int>` outside exit_codes.py | 0 hits outside exit_codes.py | 0 hits | PASS |

## VALIDATION_REQUIREMENTS Compliance

- §3 (5 static grep gates): ALL PASS.
- §4 (eval run --help diff vs baseline): EMPTY (DIFF_EXIT_CODE=0).
- §4 (eval doctor --help diff vs baseline): EXPECTED DIFF (M6 adds `file_okay=False`).
- §5 (full pytest exit 0): 1372 passed / 4 skipped / 0 failed.
- §5 (ruff F401/F821 exit 0): clean.
- §5 (make verify-sync exit 0): clean.
- §6 (no new pyproject.toml dependencies): pyproject.toml unchanged (EXIT_CODE=0 from git diff).
