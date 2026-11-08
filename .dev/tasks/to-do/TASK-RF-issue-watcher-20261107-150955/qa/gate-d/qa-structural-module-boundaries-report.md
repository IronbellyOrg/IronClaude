# QA Report - Gate D, lens module-boundaries-and-python-310

**Topic:** issue-watch Phase 8 (conftest part 5 plus seven cross-cutting test files)
**Date:** 2026-11-08
**Phase:** task-integrity / structural (report only, `fix_authorization: false`)
**Fix cycle:** N/A (first review of Gate D)
**Change set read:** `phase-outputs/reports/gate-d-change-set.md`; files re-counted with `wc -l` (1155, 443, 961, 373, 275, 191, 961, 375 lines, all equal to the change set).

---

## Overall Verdict: FAIL (2 blocking findings, 9 minor notes)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Re-derive the import table from `docs/designs/issue-watcher.md:233-242` and compare with `RULES` in `test_module_boundaries.py:51-76` | PASS (with minor note N-1) | Read design rows runner/predicates/audit none; github runner+predicates; record predicates + `superclaude.cli.swarm.atomic`; launch runner + `install_user_setup` (`_ORCA_CLIS` only); cycle runner, github, predicates, record, launch, audit; cli cycle, record, audit, launch, runner + click. `RULES` encodes the same edges; `names_only` pins `_ORCA_CLIS`. Two relaxations are written in the module docstring (lines 15-21): `atomic` allowed in any function (design C18 says "inside save") and any name from `predicates` for `record` (design says "types only"). |
| 2 | Function-level imports are walked | PASS | `_Collector` (lines 89-124) uses `generic_visit`, so nested defs/classes count. Mutations on a /tmp copy of the package: function-level `from .runner import Runner` in `predicates.py` (M2), function-level `import requests` in `cycle.py` (M7), function-level `from . import cycle` in `record.py` (M19) each failed `test_module_imports_obey_the_design_table[...]`. |
| 3 | Relative imports are resolved | PASS | `from . import cycle` (M1), `from .. import swarm` (M15, resolved to `superclaude.cli` and refused), plain `import superclaude.cli.issue_watch.github` in `cli.py` (M8b) and `...cli` in `cycle.py` (M17b) all failed. `test_walker_resolves_relative_and_absolute_to_the_same_name` (line 338) passes. |
| 4 | Mutation guards would fail if the detector were broken | PASS | 16 real-package mutations on a /tmp copy: runner->cycle, predicates->runner (function level), audit->click, github->launch, record module-level `atomic` (fails twice), launch plain/other-name `install_user_setup`, cycle third-party `requests`, cli->github, cycle->cli, predicates `try: import yaml`, record function-level cycle, plus `subprocess` in cycle and `shell=True` in runner for `test_no_shell.py`, plus a new sibling module. Every one turned a green run (baseline 103 passed) red with the right message. The synthetic FLAGGED (35) and CLEAN (18) lists exercise the same two functions (`collect_imports`, `violations`) the real scan uses. |
| 5 | The AST tests enforce the no-shell rule | FAIL | Hole in `scan_source` (G-1: `import os.path` then `os.system`) and hole in file enumeration (G-2: subpackages are never scanned). The forms the test claims to cover (`shell=` not False, `import os` / alias / `from os import`, `subprocess` outside runner) do fail when mutated (M13, M14). |
| 6 | Python 3.10 grep from the lens | PASS | `grep -rnE 'tomllib|datetime\.UTC|from datetime import .*\bUTC\b|import UTC|StrEnum|import Self|typing\.Self|ExceptionGroup|except\*|asyncio\.timeout|fromisoformat' src/superclaude/cli/issue_watch/ tests/issue_watch/` printed one hit: `src/superclaude/cli/issue_watch/predicates.py:30`, a docstring sentence "DF-35: no ``fromisoformat``". Justified: it states the rule, there is no call. A wider grep (add_note, Path.walk, batched, typing.override/NotRequired/LiteralString, TaskGroup, slots/kw_only, process_cpu_count, onexc, UTC) found only docstring words and `str.removesuffix` (3.9). |
| 7 | Python 3.10 by execution, not only by reading | PASS | (a) Python 3.10.20 `compile()` of all 30 `.py` files under `src/.../issue_watch` and `tests/issue_watch`: 0 syntax errors. (b) Full `tests/issue_watch` on Python 3.10.20 in a /tmp copy: `2616 passed in 20.95s`, including the three subprocess e2e tests and the spawn test. Method note: `uv run --offline` could not build a 3.10 project environment (tomli not in the cache), so I used a /tmp venv of the uv 3.10 interpreter with a `.pth` to the pure-Python dependencies of the repo's 3.11 venv, `exceptiongroup` and `tomli` from the uv cache, and two import shims (`rpds`, `jsonschema`, needed only by an unrelated `eval` module). The repo was not touched. |
| 8 | Multiprocessing test uses `spawn` and bounded joins | PASS (minor note N-5) | `test_concurrency.py:148` `multiprocessing.get_context("spawn")`; waits are `_wait_for(..., WAIT_S=30)` polls (lines 54-62, 108, 155); `two.join(timeout=JOIN_S)` and `one.join(timeout=JOIN_S)` (161-162) with `JOIN_S=60`; the `finally` terminates any live process and joins with `timeout=10` (165-169). No other file under `tests/issue_watch` uses fork, Process, Pool or Thread (Grep). |
| 9 | LF endings | PASS | `grep -rlP '\r'` over `tests/issue_watch` and `src/.../issue_watch` (excluding `__pycache__`): no file. No BOM either. |
| 10 | Exactly one trailing newline on every non-empty file | PASS | Loop over all 40 files under `tests/issue_watch` (21 py, 19 json) and the package files: only `src/.../issue_watch/__init__.py` and `tests/issue_watch/__init__.py` are reported, both empty (exempt). No file lacks the final newline and none ends with a blank line. |
| 11 | No trailing spaces in .py and .json | PASS | `grep -rnE '[ <tab>]+$'` over both trees: no match. |
| 12 | No executable file under `tests/issue_watch/` | PASS | `find tests/issue_watch src/superclaude/cli/issue_watch -type f -perm /111 -not -path '*/__pycache__/*'` printed nothing. |
| 13 | No test or fixture writes outside `tmp_path` | PASS | Read `stub_path` (`conftest.py:1108-1155`): `stubbin`, `linkbin`, `home`, `stub-calls.jsonl`, `scenario.json`, `xdg` are all under `tmp_path`; the subprocess env holds only `PATH`, `HOME`, `XDG_STATE_HOME`, `IW_STUB_*`. Every write/mkdir/open hit in `test_cli_e2e`, `test_security_invariants`, `test_crash_injection`, `test_no_text` traced to `tmp_path` or `run.state_dir`; all ten `run_world(...)` call sites start from `tmp_path`; `test_no_text` sets `HOME`/`XDG_STATE_HOME` under `tmp_path` with `monkeypatch`. `__file__` use is read-only (`FIXTURE_DIR`, `PACKAGE_DIR`). |
| 14 | No pytest marker in `tests/issue_watch/` | PASS for the eight Phase 8 files; carried minor note N-2 for earlier files | Phase 8 files use `@pytest.mark.parametrize` only (`test_no_shell.py:137,161`, `test_module_boundaries.py:205,328,333`). Builtin `skipif(os.geteuid() == 0)` markers and one `pytest.skip` exist in earlier-phase files (N-2). No custom marker exists, so `--strict-markers` is satisfied. |
| 15 | The tests enumerate the whole package | FAIL | Findings G-1 and G-2. |
| 16 | Change-set claims in this lens (line counts, executable list, orphan bytecode) | PASS | Line counts equal `wc -l`; executable list empty; the four orphan `.pyc` names (`test_smoke_x`, `test_zz_scratch_world`, `test_tmp_orig`, `test_dbg_tmp`) exist in `tests/issue_watch/__pycache__/`, which is ignored (`.gitignore:2`). |

## Issues Found

### Blocking findings

| id | Severity | File:line | Evidence | Expected vs actual |
|----|----------|-----------|----------|--------------------|
| G-1 | BLOCKING (security control T6 can be bypassed; docstring claim is false) | `tests/issue_watch/test_no_shell.py:55-59` | `scan_source` adds a name to `os_names` only when `alias.name == "os"`. `import os.path` also binds the name `os`, but its `alias.name` is `"os.path"`, so the name is never recorded and the later call is not seen. Direct call on the real function: `scan_source('import os.path\nos.system("x")\n', 'cycle')` returned `[]`, while `import os` + the same call returned `['2: call to os.system']`. Mutation on a /tmp copy: appending `import os.path` / `os.system("x")` to `runner.py` left `test_no_shell.py` + `test_module_boundaries.py` at `103 passed`. The module docstring (lines 6-7) and design T6 (`issue-watcher.md:662,788`) promise that any `os.system` call is found "through `import os`, an alias, or `from os import system`". No FLAGGED case uses `import os.path`, so the self-tests do not catch it. | Expected: every statement that binds the name `os` (`import os`, `import os.path`) registers it, and a FLAGGED case `("import os.path\nos.system('x')\n", "cycle")` exists. Actual: `import os.path` is not registered, so the call is not flagged. Fix: in the `ast.Import` branch add `os` for an alias with no `asname` whose root is `os`, and add `alias.asname` only when `alias.name == "os"`; then add the FLAGGED case. |
| G-2 | BLOCKING (an "exactly the designed modules" / "only the package" test is blind to a subpackage; same blindness hides forbidden imports and shell calls) | `tests/issue_watch/test_module_boundaries.py:187-190` and `:198-202`; `tests/issue_watch/test_no_shell.py:89-90` and `:98-103` | Both files enumerate the package with the non-recursive `PACKAGE_DIR.glob("*.py")`, while the same two files elsewhere use `rglob` (`test_module_boundaries.py:234,241`). Mutation on a /tmp copy: adding `issue_watch/sub/__init__.py` and `issue_watch/sub/x.py` containing `import os`, `from superclaude.cli.main import main` and `os.system("x")` left the run at `103 passed`: `test_package_has_exactly_the_designed_modules` still passes, no AST test opens `sub/x.py`. (A `sub/select.py` was caught only because the select and Protocol tests use `rglob`.) `test_scan_covers_the_package_and_only_the_package` ends in `all(p.parent == PACKAGE_DIR for p in files)`, which is true for any `glob("*.py")` result, so it asserts nothing. NFR-014 fixes the module list; the design says the test "walks each module's AST and fails on any other `superclaude.*` import" (`issue-watcher.md:231`). | Expected: a file or directory outside the nine designed modules fails `test_package_has_exactly_the_designed_modules`, and the import and no-shell scans cover every `.py` below `PACKAGE_DIR`. Actual: new subpackages are invisible to both. Fix: enumerate with `rglob("*.py")` keyed by the relative path (module name = stem only at the top level), fail on any path that is not `<module>.py` for a module in `RULES`, and drop or replace the tautological assertion at `test_no_shell.py:103`. |

### Minor notes (carried forward, never rechecked)

| id | File:line | Note |
|----|-----------|------|
| N-1 | `docs/designs/issue-watcher.md:239` vs `test_module_boundaries.py:15-21,57-61` | Design row for `record` says `predicates` "types only" and `atomic` "inside save". `record.py:23-29` imports `ApprovalResult` (a type) and four functions (`format_utc`, `parse_utc`, `valid_issue_number`, `valid_operation_id`); `atomic` is imported in two functions (`record.py:372,853`). The test encodes the code, discloses it in its docstring, and the direction of every edge matches the design. The design row should be amended (outside this change set) or `names_only` added; no name-level rule for `record` is enforced today. |
| N-2 | `test_cli.py:889,992`, `test_record.py:739`, `test_cycle.py:735` (`skipif(os.geteuid() == 0)`), `test_cycle.py:4635` (`pytest.skip`, non-Linux) | Builtin skip markers exist outside the Phase 8 files, so the lens wording "no pytest marker anywhere" is met only for custom markers (`--strict-markers` is satisfied) and for the Phase 8 files. Already recorded by Gate C as C-51 and M-1. Uid here is 1000, so the recorded 2616 passed / 0 skipped is true here; as uid 0 these tests skip and the xdist "zero skips" condition fails. |
| N-3 | `test_module_boundaries.py:134-158` | Dynamic imports (`importlib.import_module(...)`, `__import__(...)`) are not seen. Mutations that appended either to `cycle.py` / `runner.py` left the run at `103 passed`. The design asks only for AST import statements; note only. |
| N-4 | `test_no_shell.py:44-86` | Other shell-capable or process-replacing entry points pass the scan: `asyncio.create_subprocess_shell("x")` returned `[]`; `from os import *` + `system("x")` returned `[]`; an alias assignment `_r = os.system; _r("x")` left the run green; `os.exec*`, `os.spawn*` and `pty.spawn` are not listed. T6 names only `shell=True`, `os.system` and `subprocess` outside the runner, so these are beyond the stated contract. |
| N-5 | `test_concurrency.py:165-169` | After `terminate()` the cleanup joins for 10 s and never escalates to `kill()`; a worker that ignores SIGTERM would be left running. The first two joins are bounded and the test fails with a message, so no hang results. |
| N-6 | `test_module_boundaries.py:239-243` | `protocol_class_names` only matches a base literally named `Protocol` (or `typing.Protocol`); `from typing import Protocol as P` would not count. |
| N-7 | `tests/issue_watch/__pycache__/` | Bytecode of four deleted scratch tests (`test_smoke_x`, `test_zz_scratch_world`, `test_tmp_orig`, `test_dbg_tmp`, cpython-311) shows scratch files were written into the tests directory during Phase 8 and removed. Ignored by git, never collected by pytest; harmless. |
| N-8 | `tests/issue_watch/test_cli_e2e.py:101-123` | The e2e subprocess runs `sys.executable -m superclaude.cli.main` with a scrubbed env, so it needs `superclaude` importable from the interpreter's own site (editable install). With a `PYTHONPATH`-only setup the three e2e tests fail (seen once in my first 3.10 attempt: `No module named 'superclaude'`). Normal `uv run` and CI installs satisfy this; note only. |
| N-9 | `test_module_boundaries.py:188-190` | `_sources()` rebuilds a dict of all package sources on each of the 12+ parametrized calls; harmless cost (suite runs in under 1 s). Listed for completeness. |

## Actions Taken

None (report only). Experiments ran on `/tmp/qa310-modbound` (a copy of `src`, `tests/conftest.py`, `tests/__init__.py`, `tests/issue_watch`, `pyproject.toml`) and were removed at the end. No repository file other than this report was modified.

## Recommendations

- Fix G-1 and G-2 in `test_no_shell.py` and `test_module_boundaries.py` and add the matching FLAGGED/negative cases (`import os.path` + `os.system`; a sub-directory module). Then run `uv run pytest tests/issue_watch/test_no_shell.py tests/issue_watch/test_module_boundaries.py -v`.
- No Python 3.10 defect found; the full suite passes on 3.10.20.

## Summary

- Checks passed: 14 / 16
- Checks failed: 2 (items 5 and 15, one root cause each: G-1 and G-2)
- Critical issues: 2 (blocking: G-1, G-2); minor notes: 9 (N-1 to N-9)
- Issues fixed in-place: 0 (not authorized)

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (item 7 used shims for two unrelated import-only modules; stated in the item)
**Tool engagement:** Read: 14 | Grep: 10 | Glob: 0 | Bash: 17 (3.10 compile, 3.10 full run, two mutation scripts of 18 and 5 runs, hygiene batch, direct scanner probe)

## QA Complete
