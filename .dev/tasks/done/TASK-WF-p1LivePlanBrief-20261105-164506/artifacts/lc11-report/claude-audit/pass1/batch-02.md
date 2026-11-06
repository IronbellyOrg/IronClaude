# tests/pr_submit Audit (Pass 1) - Batch 2 of 2

**Status**: Complete (scanner report; spot-check pending)
**Files audited**: 31 / 31 assigned
**Date**: 2026-11-05
**Agent**: audit-scanner
**Batch**: 2

All 31 files are KEEP. None is DELETE, REVIEW or wiring-flagged. The scanner did not run any tests.

**Shared evidence for every file below**
- **Collection**: `pyproject.toml:107-111` sets `testpaths = ["tests"]`, `python_files = ["test_*.py"]`, `python_classes = ["Test*"]` and `python_functions = ["test_*"]`. Every `tests/pr_submit/test_*.py` file is therefore collected by pytest (dynamic-use pattern 5, config-driven loading).
- **Collection proof**: `.dev/tasks/issue-302-handoff/pre-pr/full-pytest-rebased.log` lists each of the 31 files with passing results. It is a hidden-path referrer and is not audited. Below it is written `LOG:<line>`.
- **Wiring Indicator rule**: in `tests/pr_submit/*.py`, `grep -n "Callable|REGISTRY|DISPATCH|HANDLERS|ROUTER|BUILDERS"` returned 0 matches. `tests/pr_submit/` is not a `steps/`, `handlers/`, `validators/` or `checks/` directory. None of the three triggers fires.
- **`test_gate_helper_differentials.py`**: defines a module-level `HELPER_TEST_MAP` that its docstring calls "the enforced registry". The name does not match the `*_REGISTRY` suffix family, so it was not flagged; Pass 2 may want to know.
- **Dynamic loading in the directory**: none of the matches is a loader for these 31 files.
  - `importlib.util.spec_from_file_location` at `conftest.py:161-170` loads a helper module.
  - The `glob`, `rglob` and `iterdir` calls at `test_static_grep.py:151,776`, `test_conflict_e2e.py:869,1049,1112`, `test_conflict_sync_protocol.py:413`, `test_contract_setup_pr_submit_integration.py:224,227` and `test_conflict_scripts.py:548,1312` scan source or temporary directories, not this folder.

## Safe to Delete
- None.

## Need Decision
- None. There are no `[wiring]` entries.

## Keep (verified legitimate)
- `tests/pr_submit/test_contract_setup_evidence.py` — contract-setup evidence loader tests. Referenced by: `pyproject.toml:108-109`; `LOG:368`.
- `tests/pr_submit/test_contract_setup_pr_submit_integration.py` — missing-contract halt and monitor FSM integration tests. Referenced by: `pyproject.toml:108-109`; `LOG:369`.
- `tests/pr_submit/test_contract_setup_questions.py` — setup-question table and lockability tests. Referenced by: `pyproject.toml:108-109`; `LOG:370`.
- `tests/pr_submit/test_contract_setup_validation.py` — `validate_candidate` tests. Referenced by: `pyproject.toml:108-109`; `LOG:371`; `.dev/analysis/qa-reflect-blindspot-pr209/CONSOLIDATED-root-cause.md:32`.
- `tests/pr_submit/test_contract_setup_writer.py` — safe-writer tests. Referenced by: `tests/cli/reflect/test_contract_status_cli.py:181`; `tests/pr_submit/test_contract_setup_pr_submit_integration.py:179`; `pyproject.toml:108-109`; `LOG:372`.
- `tests/pr_submit/test_cosmos_poll.py` — shell-adapter tests with a gh stub. Imported by `tests/pr_submit/test_cosmos_protocol.py:16` and `:19`; also `pyproject.toml:108-109`; `LOG:373`.
- `tests/pr_submit/test_cosmos_protocol.py` — runs the attended protocol gate against production helpers. Referenced by: `pyproject.toml:108-109`; `LOG:375`.
- `tests/pr_submit/test_cosmos_review.py` — PR266-shaped lifecycle regressions. Referenced by: `pyproject.toml:108-109`; `LOG:376`.
- `tests/pr_submit/test_crash_recovery.py` — crash-recovery tests (FM-1..FM-12). Referenced by: `tests/pr_submit/test_monitor_arm.py:7`; `tests/pr_submit/test_skill_parse.py:6`; `pyproject.toml:108-109`; `LOG:379`.
- `tests/pr_submit/test_detection_contract.py` — detection-contract tests. Referenced by: `tests/pr_submit/test_contract_setup_diagnosis.py:19`; `pyproject.toml:108-109`; `LOG:380`.
- `tests/pr_submit/test_edge_cases.py` — edge-case catalog tests (EC-1..EC-16). Referenced by: `pyproject.toml:108-109`; `LOG:382`.
- `tests/pr_submit/test_finding_verify.py` — verify-before-remediate tests. Referenced by: `pyproject.toml:108-109`; `LOG:383`.
- `tests/pr_submit/test_gate_helper_coverage.py` — one test that `conftest.py` parametrizes once per gate helper; uses the conftest fixtures `gate_helper` and `assert_gate_helper_coverage`. Referenced by: `pyproject.toml:108-109`; `LOG:384`.
- `tests/pr_submit/test_gate_helper_differentials.py` — mutation-must-fail differential tests, plus the `HELPER_TEST_MAP` that `conftest.py` imports. Referenced by: `tests/pr_submit/conftest.py:98`, `:157`, `:163`, `:165`, `:227`; `pyproject.toml:108-109`; `LOG:385`.
- `tests/pr_submit/test_idempotency.py` — idempotency tests (T-N01, T-N02). Referenced by: `tests/pr_submit/test_auggie_fallback.py:104`; `pyproject.toml:108-109`; `LOG:387`.
- `tests/pr_submit/test_loop_guard.py` — loop-guard fence-post tests (P0 surface). Referenced by: `.dev/review-severity-rule/inventory.md:174`, `:213`; `.dev/implement/calm-drifting-lightning-9ce59376/progress.md:9`; `pyproject.toml:108-109`; `LOG:388`.
- `tests/pr_submit/test_monitor_arm.py` — monitor-arming tests. Referenced by: `tests/pr_submit/test_contract_setup_pr_submit_integration.py:10`; `pyproject.toml:108-109`; `LOG:389`.
- `tests/pr_submit/test_pre_pr_checks.py` — pre-PR check tests, including the upstream-repo negative fixtures. Referenced by: `CLAUDE.md:56`; `pyproject.toml:108-109`; `LOG:390`.
- `tests/pr_submit/test_rate_limit.py` — rate-limit and backoff tests. Referenced by: `pyproject.toml:108-109`; `LOG:392`.
- `tests/pr_submit/test_reply_resolve.py` — reply, resolve and terminate tests. Referenced by: `pyproject.toml:108-109`; `LOG:393`.
- `tests/pr_submit/test_review_retrigger.py` — post-push re-trigger tests. Referenced by: `pyproject.toml:108-109`; `LOG:394`.
- `tests/pr_submit/test_run_log.py` — run-log tests. Referenced by: `tests/pr_submit/test_monitor_arm.py:7`; `pyproject.toml:108-109`; `LOG:395`.
- `tests/pr_submit/test_setup_questions_resolution.py` — AST regression test for the `SETUP_QUESTIONS` deriver fields. Referenced by: `pyproject.toml:108-109`; `LOG:396`.
- `tests/pr_submit/test_severity_router.py` — severity-router tests. Referenced by: `pyproject.toml:108-109`; `LOG:397`.
- `tests/pr_submit/test_silence.py` — silence and no-activity detection tests. Referenced by: `pyproject.toml:108-109`; `LOG:398`.
- `tests/pr_submit/test_skill_parse.py` — skill flag and argument parse tests. Referenced by: `pyproject.toml:108-109`; `LOG:399`.
- `tests/pr_submit/test_static_grep.py` — static-grep and core-purity tests. Referenced by: `tests/pr_submit/test_conflict_sync_protocol.py:21`; `.dev/implement/pr-submit-ci-wait-7e98c87b/progress.md:5`; `.dev/implement/auggie-review-remove-dee-a9e5dee8/progress.md:13`; `pyproject.toml:108-109`; `LOG:400`.
- `tests/pr_submit/test_timeout.py` — timeout and backoff tests. Referenced by: `pyproject.toml:108-109`; `LOG:401`.
- `tests/pr_submit/test_troubleshoot_seed.py` — troubleshoot-seeding tests. Referenced by: `pyproject.toml:108-109`; `LOG:402`.
- `tests/pr_submit/test_validated_not_verified.py` — validated-not-verified audit test; uses `load_fixture` on `behavioral-drift.json` at line 24. Referenced by: `pyproject.toml:108-109`; `LOG:403`.
- `tests/pr_submit/test_validation_gate.py` — validation-gate tests. Referenced by: `pyproject.toml:108-109`; `LOG:404`.

## Add to .gitignore
- None.

## Remaining / Not Audited
- None. `batch-02-files.txt` lists 31 paths and all 31 were audited.

## Summary
- **Total files audited**: 31 / 31 assigned
- **DELETE**: 0 | **REVIEW**: 0 | **KEEP**: 31 | **.gitignore**: 0
- **Coverage**: 31/31 = 100%
- Count check: audited 31 + remaining 0 = 31.

## Notes
- Orchestrator note: the scanner returned its report as text and the orchestrator wrote it here, because `audit-scanner` has only Read, Grep and Glob.
- The scanner's own date header said 2026-11-06; the session clock says 2026-11-05, which is used above.
