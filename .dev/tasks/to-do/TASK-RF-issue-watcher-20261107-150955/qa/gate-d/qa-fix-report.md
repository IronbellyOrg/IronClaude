# Gate D fix report (cycle 1)

**Date:** 2026-11-08
**Fix agent:** one `rf-qa` agent, `fix_authorization: true`
**Findings fixed:** D-1, D-2, D-3 (all blocking). Minor findings D-4 to D-37 left as notes, not touched.
**Files changed (tests only):** `tests/issue_watch/test_no_shell.py`, `tests/issue_watch/test_module_boundaries.py`, `tests/issue_watch/test_no_text.py`. No source, design, spec, research, task file, pyproject, Makefile, workflow or `.claude/` file was edited. No assertion was weakened or deleted.

## Per-finding changes

### D-1 (guards blind to a sub-package)

- `tests/issue_watch/test_no_shell.py`
  - `_package_files(root=PACKAGE_DIR)` now uses `root.rglob("*.py")`.
  - New `_module_name(path, root)`: top-level `runner.py` is `runner`; `sub/runner.py` is `sub.runner`, so a nested file never gets the runner's subprocess exemption.
  - New `scan_tree(root)` and `subprocess_importers(root)`. The two real tests (`test_no_shell_forms_in_issue_watch_package`, `test_runner_is_the_only_subprocess_importer`) call them.
  - The tautology `all(p.parent == PACKAGE_DIR for p in files)` is replaced by `all(PACKAGE_DIR in p.parents for p in files)`, which now covers nested files.
  - New tests `test_tree_scan_reaches_a_sub_package_module` and `test_tree_scan_is_clean_for_a_clean_tree`, run on a synthetic tree under `tmp_path` (nested `shell=True`, nested `import subprocess`, nested `os.system`, a nested file named `runner.py`).
- `tests/issue_watch/test_module_boundaries.py`
  - New `package_sources(root)` (rglob, dotted name for nested files; `_sources()` now delegates to it) and `stray_directories(root)` (any directory except `__pycache__`).
  - `test_package_has_exactly_the_designed_modules` keeps its set-equality assertion and gains `assert stray_directories() == []`.
  - New `test_package_listing_reaches_a_sub_package` on a synthetic tree.

### D-2 (`import os.path` hides `os.system`)

- `tests/issue_watch/test_no_shell.py`, `scan_source`, the `ast.Import` branch:
  - `import os` and `import os.path` (no alias) both register the name `os`.
  - `import os as o` registers `o`.
  - `import os.path as p` registers nothing, because `p` is `os.path`, not `os`.
- New FLAGGED self-tests: `import os.path` + `os.system`; `import os.path` + `os.popen`; `import sys, os.path` + `os.system`; `import os.path as p` + `import os` + `os.system`; `from os import path` + `import os.path` + `os.system`; `import os.path` + `import os as o` + `o.system`.
- New look-alike (clean) self-tests: `import os.path` + `os.path.join` + `os.getpid`; `import os.path as p` + `p.join`; `from os import path` + `path.join`.
- Known limit, not fixed (minor D-21 family): `from os import path` alone followed by `os.system(...)` is not flagged, because `os` is unbound there and the call would raise `NameError`; `path.os.system(...)` is not followed.

### D-3 (inline Orca launch reply, scenario did not pin the launch)

- `tests/issue_watch/test_no_text.py`
  - Scenario `launch_ok_with_text_fields` builds its reply as `{**load_fixture("orca_launch_success.json")["payload"], "title": SENT, "body": SENT}`. The reply shape now comes from the existing `_assumed_shape` fixture (design 636, 840, 847) and no longer has a second inline copy.
  - `Scenario` gains `expect_state: str | None = None`; the scenario sets `expect_state="launched"`. The parametrized test `test_canary_never_leaves_a_hostile_cycle` asserts `tmp_state.load().entries[7].state == sc.expect_state` for the real (non-dry) run.
- Fixture count: no new fixture was added (the existing `orca_launch_success.json` plus the two text fields is enough), so the pin in `test_github.py` stays at 19. `test_every_assumed_shape_fixture_is_read_by_a_test__df32` still holds because `"orca_launch_success.json"` is read by name. `test_github.py` was not edited.

## Mutants re-run on /tmp copies (repo never mutated; copies removed afterwards)

| Mutant | Result |
|--------|--------|
| M1: `issue_watch/sub/__init__.py` + `sub/x.py` with `import subprocess` and `shell=True` | KILLED: `test_no_shell_forms_in_issue_watch_package`, `test_runner_is_the_only_subprocess_importer`, `test_package_has_exactly_the_designed_modules` fail (3 failed, 112 passed) |
| M2: `import os.path` + `os.system("x")` appended to `runner.py` | KILLED: `test_no_shell_forms_in_issue_watch_package` fails with `runner.py:133: call to os.system` |
| M2b: old scanner logic (`alias.name == "os"` only) restored in the copy of the test file | The new self-tests fail (4 failed): `import os.path`+`os.system`, `import os.path`+`os.popen`, `import sys, os.path`, `from os import path`+`import os.path` |
| M3: `operation_id` key renamed in the copy of `orca_launch_success.json` (launch becomes `unknown`) | KILLED: `test_canary_never_leaves_a_hostile_cycle[launch_ok_with_text_fields-real]` fails (`- launched` / `+ unknown`) |

## Final results

- `uv run pytest tests/issue_watch/ -q`: 2628 passed (before the fix 2616; 12 new cases). Zero skips, zero failures.
- xdist: `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/ -q`: 2628 passed.
- `make lint`: all checks passed (architecture policy: 5 pre-existing warnings, PASS; `ruff check .` passed).
- Pinned `uvx --offline ruff@0.15.20 check` on the three changed files: all checks passed.
- Pinned `uvx --offline ruff@0.15.20 format --check` on the three changed files: 3 files already formatted (one `ruff format` was applied to `test_no_shell.py` first).
- Python 3.10.20 (uv interpreter, run through `uv run --offline --python 3.10 --no-project python` with the repo venv's pure-Python packages plus `exceptiongroup` and `tomli` from the uv cache on `PYTHONPATH`): `test_no_shell.py` and `test_module_boundaries.py` copied to a /tmp tree with a symlink to `src`: 115 passed. `test_no_text.py` was not run on 3.10 (it needs the full package dependencies); its change is a data-only edit and one dataclass field annotation, which `from __future__ import annotations` keeps lazy.
- No temp directories left in `/tmp` (`gate-d-*` count 0).
