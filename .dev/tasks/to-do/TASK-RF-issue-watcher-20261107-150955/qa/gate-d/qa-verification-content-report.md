# QA Report: Gate D content verification (fix cycle 1)

**Date:** 2026-11-08
**Phase:** fix-cycle (content), `fix_authorization: false`
**Inputs read:** `qa/gate-d/qa-consolidated-findings.md`, `qa/gate-d/qa-fix-report.md`, `tests/issue_watch/test_no_shell.py`, `tests/issue_watch/test_module_boundaries.py`, `tests/issue_watch/test_no_text.py` (lines 255-560), `tests/issue_watch/conftest.py` (`load_fixture`), `tests/issue_watch/fixtures/_assumed_shape/orca_launch_success.json`, `src/superclaude/cli/issue_watch/launch.py:38-48`, design lines 636, 662, 788, 840, 847.

## Overall Verdict: PASS

## Per-finding results

| id | Result | Evidence |
|----|--------|----------|
| D-1 (guards blind to a sub-package) | FIXED | `test_no_shell.py:95-97` `_package_files` uses `rglob("*.py")`; `:100-105` `_module_name` gives `sub.runner` for a nested file, so a nested file never gets the runner exemption; `test_module_boundaries.py:187-207` `package_sources` (rglob, dotted names) and `stray_directories`; `:219-224` keeps the set-equality assertion and adds `stray_directories() == []`. The tautology is replaced by `all(PACKAGE_DIR in p.parents ...)` (`test_no_shell.py:147`). Replayed on /tmp copies: (M1) `sub/__init__.py` + `sub/x.py` with `import subprocess` and `shell=True` fails 3 tests (`test_no_shell_forms_in_issue_watch_package`, `test_runner_is_the_only_subprocess_importer`, `test_package_has_exactly_the_designed_modules`; 3 failed, 112 passed). (M1b) `sub/y.py` with `import os` + `os.system("x")` plus a nested `sub/runner.py` with `import subprocess` fails the same 3 tests. |
| D-2 (`import os.path` then `os.system` missed) | FIXED | `test_no_shell.py:55-67`: any `import os.x` without `as` binds `os`; `import os as o` binds `o`; `import os.path as p` binds nothing (correct, `p` is `os.path`). Replayed: (M2) `import os.path` + `os.system("x")` appended to `runner.py` fails `test_no_shell_forms_in_issue_watch_package`; (M2b) `import sys, os.path` + `os.popen("x")` appended to `cycle.py` fails the same test. Six new FLAGGED cases (`:214-219`) and three look-alike cases (`:243-245`). |
| D-3 (inline Orca launch reply) | FIXED | `test_no_text.py:495-514`: reply is `{**load_fixture("orca_launch_success.json")["payload"], "title": SENT, "body": SENT}` and the scenario sets `expect_state="launched"`; `:541-544` asserts `tmp_state.load().entries[7].state == sc.expect_state` for the real run. No inline `receipt` or `operation_id` text remains in `test_no_text.py` (grep empty). Design 636, 840 and 847 (shape is UNVERIFIED, lives in an `_assumed_shape` fixture) are met. Replayed on copies of the fixture: (M3) `operation_id` key renamed, (M3b) no operation id, (M3c) id moved to `result.operation_id`: each fails `test_canary_never_leaves_a_hostile_cycle[launch_ok_with_text_fields-real]` with `- launched / + unknown`. |

## Checks asked for

- **Fix is a real fix, not a silenced test:** yes for all three. Each mutant that the findings described now fails at least one test, and the real package still passes (baseline copy: 115 passed for the two scan files; 168 passed for `test_no_text.py`; real tree: 2628 passed).
- **No assertion weakened or deleted:** the visible assertions in the three files only gained cases. The two-file count went from 103 (consolidated findings) to 115, which equals the 12 new cases the fix report lists (9 scanner cases + 2 tree tests + 1 listing test). The full-suite count went from 2616 to 2628. No `skip`, `xfail` or loosened comparison was added. The tautology was replaced by a stronger check (`PACKAGE_DIR in p.parents`), not removed.
- **No false positives on the real package:** `scan_tree()`, `subprocess_importers()` (still exactly `{runner}`), `package_sources()` against `RULES`, and `stray_directories()` (`__pycache__` excluded) all pass on the real package; the look-alike cases (`import os.path` + `os.path.join`/`os.getpid`, `import os.path as p`, `from os import path`) return no findings.
- **Design ranges:** the scan matches design T6 (lines 662, 788) and the module list rule of 5.3; the Orca shape handling matches lines 636, 840, 847.
- **Repo untouched by my replays:** all mutants ran on /tmp copies, which are removed; `git status` shows only the expected untracked package, tests and the `main.py` registration.

## New blocking findings

None.

## Notes (minor, not blocking)

- The fix report states the known limit `from os import path` followed by `os.system(...)` is not flagged. That code would raise `NameError`, so it is not a real bypass; it stays in the minor D-21 family.
- The Python 3.10 run of `test_no_text.py` was not done by the fix agent (its change is data plus one `str | None` annotation under `from __future__ import annotations`). I did not run 3.10 either; this is the structural verifier's scope.

## Self-Audit

**(a) Reliance list:** Relied on the fix report only for the pytest/ruff totals and the 3.10 run, which I did not repeat except the full pytest run (2628 passed).

**(b) Independent semantic checks:**
- Scanner behaviour on a sub-package: replayed M1 and M1b on /tmp copies (3 failures each, named above).
- `import os.path` bypass: replayed M2 and M2b (1 failure each).
- Orca reply shape: replayed M3, M3b, M3c on copies of `_assumed_shape/orca_launch_success.json` (each fails with `unknown` instead of `launched`).
- False positives: baseline runs on copies (115 and 168 passed) and the full real-tree run (2628 passed).
- Assertion preservation: read the final text of all three changed test files and compared test counts before and after (103 to 115, 2616 to 2628).

**Confidence:** Verified: 3/3 blocking ids and 3 extra checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Grep: 3 | Glob: 0 | Bash: 7

## QA Complete
