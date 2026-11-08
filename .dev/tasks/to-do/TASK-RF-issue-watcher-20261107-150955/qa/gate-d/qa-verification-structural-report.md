# QA Report - Gate D structural verification of the fix (cycle 1)

**Topic:** issue-watch implementation, Gate D (Phase 8), fix verification
**Date:** 2026-11-08
**Phase:** fix-cycle (structural verifier, report-only, `fix_authorization: false`)
**Fix cycle:** 1

## Overall Verdict: PASS

All three blocking findings (D-1, D-2, D-3) are fixed in the repository files and no new blocking structural issue was found. Minor findings D-4 to D-37 are notes and were not rechecked.

## Blocking findings

| id | Status | Evidence |
|----|--------|----------|
| D-1 (guards blind to a sub-package) | FIXED | `tests/issue_watch/test_no_shell.py:95-97` `_package_files` uses `root.rglob("*.py")`; `:100-105` `_module_name` gives `sub.runner` for a nested `runner.py` (no subprocess exemption); `:108-133` `scan_tree` and `subprocess_importers` feed the two real tests (`:150-156`); the tautology is now `PACKAGE_DIR in p.parents` (`:147`). `tests/issue_watch/test_module_boundaries.py:187-211` `package_sources` (rglob, dotted names) and `stray_directories`; `:219-224` `test_package_has_exactly_the_designed_modules` keeps the set-equality check and adds `stray_directories() == []`. New self-tests on synthetic trees: `test_no_shell.py:166-192`, `test_module_boundaries.py:227-236`. Independent mutation on a /tmp copy of src and tests (baseline 115 passed): adding `issue_watch/sub/__init__.py` plus `sub/x.py` with `import subprocess` and `shell=True` failed `test_no_shell_forms_in_issue_watch_package`, `test_runner_is_the_only_subprocess_importer` and `test_package_has_exactly_the_designed_modules` (3 failed, 112 passed). |
| D-2 (`import os.path` hides `os.system`) | FIXED | `test_no_shell.py:55-65` registers `os` for any un-aliased `import os...` and the alias only for `import os as o`; `import os.path as p` registers nothing (correct, `p` is `os.path`). FLAGGED self-tests added at `:214-219` (`import os.path` plus `os.system` and `os.popen`, `import sys, os.path`, mixed alias forms); look-alike (clean) cases at `:243-245`. Independent mutation: appending `import os.path` / `os.system("x")` to `runner.py`, and `import os.path` / `os.popen("x")` to `cycle.py`, each failed `test_no_shell_forms_in_issue_watch_package` (1 failed, 114 passed). |
| D-3 (inline Orca launch reply, scenario did not pin the launch) | FIXED | `tests/issue_watch/test_no_text.py:495-514` builds the reply as `{**load_fixture("orca_launch_success.json")["payload"], "title": SENT, "body": SENT}` with `expect_state="launched"`; `Scenario.expect_state` at `:268`; the parametrized test asserts `tmp_state.load().entries[7].state == sc.expect_state` for the real run (`:541-544`). Independent mutation: renaming `operation_id` in a /tmp copy of `orca_launch_success.json` failed `test_canary_never_leaves_a_hostile_cycle[launch_ok_with_text_fields-real]` (1 failed, 167 passed). |

## New blocking findings

None.

## Gate checks (run by me, not taken from the fix report)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `uv run pytest tests/issue_watch/ -v -rs` | PASS | 2628 passed, EXIT=0, no SKIPPED line, no "skipped" in the summary. |
| 2 | `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/ -rs` | PASS | 2628 passed, EXIT=0, zero skips. |
| 3 | `make lint` | PASS | architecture policy PASS (5 pre-existing warnings, 0 errors); `uv run ruff check .` all checks passed. |
| 4 | Pinned `uvx --offline ruff@0.15.20 check` and `format --check` on the three changed files | PASS | "All checks passed!" and "3 files already formatted". |
| 5 | Same pinned ruff on `tests/issue_watch` and `src/superclaude/cli/issue_watch` | PASS | "All checks passed!" and "30 files already formatted". |
| 6 | Real Python 3.10.20, changed test files (`test_no_shell.py`, `test_module_boundaries.py`, `test_no_text.py`) | PASS | 283 passed. Method: /tmp copy of `src`, `tests/conftest.py`, `tests/issue_watch`, `pyproject.toml`; `uv run --offline --python 3.10` interpreter (`python -V` printed 3.10.20, pytest header "Python 3.10.20"); repo venv pure-Python packages plus `exceptiongroup` and `tomli` from the uv cache on `PYTHONPATH`; stubs for `jsonschema` and `rpds` (needed only by the unrelated `eval` and `swarm` modules). |
| 7 | Real Python 3.10.20, the whole `tests/issue_watch` | PASS | 2628 passed. A first run with `PYTHONPATH` only gave 3 failures, all in `test_cli_e2e.py` (`No module named 'superclaude'` in the scrubbed-env child process); this is the known environment note D-24 (the e2e child needs `superclaude` on the interpreter's own site), not a defect. Rerun in a 3.10 venv with a `.pth` to the same paths: 2628 passed. |
| 8 | Python 3.10 incompatibilities in the new code | PASS | Nothing new beyond `from __future__ import annotations` plus `str | None` annotations (lazy) and `ast.unparse` (3.9+); the 3.10 runs above exercise them. |
| 9 | Imports against design lines 233-242 | PASS | `test_module_boundaries.py` (115 cases with `test_no_shell.py`) passes on the unchanged source tree; the fix touched no `src/` file. |
| 10 | File hygiene on the three changed files | PASS | No CR characters (`grep -lP '\r'` printed nothing); ruff format covers trailing spaces and the final newline. |
| 11 | git status shows no change outside `tests/issue_watch/` (and fixtures) | PASS | `git status --short` identical before and after my runs. Files newer than `qa-consolidated-findings.md`: only the three test files, `qa-fix-report.md`, the task file (ledger) and the gitignored `.codegraph/` database. `src/` and `main.py` have no change after the findings file; no `.claude/`, `pyproject.toml`, `Makefile` or workflow change. |
| 12 | No assertion weakened or deleted | PASS | The two real tests keep their assertions (`not offenders`, `subprocess_importers() == {RUNNER_MODULE}`, set equality of modules); additions only. Test count rose from 2616 to 2628 (12 new cases). |

## Notes (minor, not blocking)

- `test_no_shell.py:55-65`: `from os import path` followed by `path.os.system(...)` is not followed, and an unbound `os.system(...)` is not flagged; both are the D-21 family already recorded as minor by the fix report.
- `from superclaude...` e2e tests need the package importable from the interpreter's own site (D-24, unchanged).

## Summary

- Blocking findings verified FIXED: 3 / 3
- New blocking findings: 0
- Temporary directories under `/tmp` created by this verification were removed (checked: none remain). No repository file other than this report was modified.

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 4 | Glob: 1 | Bash: 14

## QA Complete
