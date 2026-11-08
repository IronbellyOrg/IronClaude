# QA Report - Gate B structural verification (Step 5.G10)

**Topic:** issue-watch implementation, Phases 4 and 5
**Date:** 2026-11-08
**Phase:** fix-cycle (structural verification of fix cycle 1)
**Fix cycle:** 1
**Agent:** rf-qa, `fix_authorization: false`. No file modified except this report. Mutation probes ran only on a private copy under `/tmp` that was removed afterwards.

---

## Overall Verdict: PASS

All 13 blocking ids (B-1 to B-13) are FIXED in the repository files. No new blocking structural issue was found. Minor ids B-14 to B-67 were not rechecked.

## Commands I ran myself

| Command | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` (three runs, one with `-rs`) | 1577 passed each time, no skips (uid 1000, so the `chmod 0` lock test runs) |
| `uvx --offline ruff@0.15.20 check` on the 7 changed files | All checks passed (ruff 0.15.20) |
| `uvx --offline ruff@0.15.20 format --check` on the 7 changed files | 7 files already formatted |
| the same two ruff commands on the whole `src/superclaude/cli/issue_watch` and `tests/issue_watch` | All checks passed; 18 files already formatted |
| `make lint` | architecture policy PASS (5 warnings), `ruff check .` All checks passed |
| `ast.parse(..., feature_version=(3, 10))` on every package and test file | 0 syntax errors |

## Per blocking finding

| id | Result | Evidence |
|---|---|---|
| B-1 | FIXED | `launch.py:144-153` (`_lists_orca_cli` docstring) and the `test_find_orca_parity.py:1-19` docstring now say "null, int, bool, non-empty str, non-empty dict, or a list with a non-dict element before any `orca-cli` dict" and that an empty str, an empty dict and `orca-cli`-first do not raise. I ran `install_user_setup._find_orca` on nine shapes: null, int, bool raise `TypeError`; non-empty str, non-empty dict, non-dict-first list raise `AttributeError`; empty str and empty dict return None; `orca-cli`-first returns the path. The docstrings match. The DF-36 text in the design still has the old wording (the fix agent declared this; the design is out of its scope; carried as a note, not blocking). |
| B-2 | FIXED | `test_launch.py:558-590`: `_success_payload`, `_id_holder`, `_id_reply` and `_no_id_reply` build the reply from `orca_launch_success.json` and `OPERATION_ID_PATHS[0]`. Grep for `"receipt"` and `"outcome"` in the file finds no inline reply body. `test_launch.py:608-613` reads the id through the path. The fixture count pin is unchanged. |
| B-3 | FIXED | `record.py:393-401`: `except FileNotFoundError` gives `lock_missing`, then `except OSError` gives `LockError("lock_invalid")`. New test `test_record.py:739-750` (`chmod 0`, restores the mode, checks the lock is free after). Mutation (narrow the `OSError` catch to `IsADirectoryError`) is killed. |
| B-4 | FIXED | `test_record.py:2165-2225`: parametrized refusals for `mark_pending` (approver id, event id, account id, naive or non-datetime `approved_at`, non-absolute `launch_cwd`, empty or non-str `launch_login`, failed entry) and `mark_claimed` (ids, `approved_at`). Each uses `refused()`, which asserts `ValueError` and an unchanged document. |
| B-5 | FIXED | `test_record.py:2228-2239`: `mark_launched` with `""`, `a;b`, `$(id)`, `op\n1`, 129 characters, None, 5, `b"op"`, a list and True; boundary ids kept. Mutation (guard replaced by `if False`) is killed. |
| B-6 | FIXED | `test_record.py:2283-2301`: `fail` and `mark_pending` with 0, -1, True, "7", None, 7.0, 10**9; `init_state` with a naive `now` raises and creates no directory. |
| B-7 | FIXED | `test_record.py:2313-2369`: five `set_considered` tests (stamp and prune, unexamined keeps old time, newly discovered, empty discovered, input and other fields unchanged), plus `set_next_permitted` set and clear and `set_last_completed` stamping exactly `now`. |
| B-8 | FIXED | `test_record.py:395-404` `TIME_PLACES` now holds `last_completed_cycle_at`, `approved_at` and `pending_at`, each run against all `BAD_TIMES` (`:408-411`). Wrong-type cases at `:265-266`. The load test asserts the loaded fields (`:185-191`). |
| B-9 | FIXED | `test_record.py:2021-2043` patches `atomic.write_prepared_bytes` to leave 0666, so only `save_dry_run`'s own `os.chmod` (`record.py:864`) gives 0600. `:2046-2062` observes that the last fsync is on the state directory (`record.py:865`). |
| B-10 | FIXED | `predicates.py:57-67` adds `OPERATION_ID_PATTERN` and `valid_operation_id` (a `str` that `fullmatch`es, so a trailing newline fails). `record.py:183` (`_entry`), `:585` (`mark_launched`) and `:607` (`mark_unknown`) enforce it. `test_launch.py:194-200` pins the `launch` copy equal to the `predicates` copy. Tests at `test_record.py:336-358` (on disk), `:2228-2253`, and `test_predicates.py:675-702`. Mutation (`_entry` check reduced to `isinstance(v, str)`) is killed. |
| B-11 | FIXED | `record.py:607-608`: `mark_unknown` raises `ValueError` unless the id is None or a valid str. Round-trip tests: `test_record.py:2256-2266` (`validate(_to_raw(after)) == after` for every allowed state and trigger pair except `backoff`, which returns a bool, and for `sweep`) and `:2269-2280` (a hostile id never reaches a saved file; a valid one saves and reloads). Mutation (guard removed) is killed. |
| B-12 | FIXED | `record.py:132` `[1-9][0-9]{0,8}`; `:361-366` `load` wraps parse, `migrate` and `validate` in one `try` that maps `ValueError` and `RecursionError` to `store_invalid` (`StoreError` derives from `Exception`, so a typed error is not swallowed); `:845-848` `load_dry_run` catches `RecursionError`. Tests at `test_record.py:316-333` and `:2065-2085` (10, 4301 and 20000 digit keys; 100000-deep arrays and objects). Mutation (drop the `RecursionError` catch in `load`) is killed. Mutation (old key regex) is NOT killed because the new `except ValueError` still maps the `int()` error; the fix agent disclosed this, behaviour is correct, so it is not a defect. |
| B-13 | FIXED | `launch.py:184`: `if not path or not os.path.isabs(path): continue` before the probe; the probed path is the one returned (`:186-187`). Tests at `test_launch.py:320-343` (`./orca-ide`, `orca-ide`, `bin/orca-ide`, `../orca` give None with no runner call; relative first candidate skipped, absolute second probed and returned; returned path equals probed path). Mutation (remove the `isabs` check) is killed. |

## Structural checks for new issues

| Check | Result | Evidence |
|---|---|---|
| Imports against design lines 233-242 | PASS | `launch.py:13-24` imports stdlib, `superclaude.cli.install_user_setup._ORCA_CLIS` and `.runner` only. `record.py:12-28` imports stdlib and `predicates`; the lazy imports at `:372`, `:389`, `:853` are `swarm.atomic` and `fcntl`. `predicates.py:7-12` imports stdlib only, still "none" for the package. The new `valid_operation_id` import by `record` is within the `record` -> `predicates` rule (design 5.3, same reading as open minor B-24). `launch` keeps its own pattern copy because it may import only `runner`, and a test pins the copies equal. |
| Python 3.10 compatibility | PASS | No 3.10 interpreter is installed offline (uv offline mode). `ast.parse` with `feature_version=(3, 10)` passes on all files; grep finds no `datetime.UTC`, `tomllib`, `StrEnum`, `Self`, `ExceptionGroup`, `except*`, `contextlib.chdir`, `batched`; every module except the empty `__init__.py` has `from __future__ import annotations`; ruff `target-version = "py310"` (`pyproject.toml:175`). Residual: not executed on a real 3.10 (unverifiable here). |
| File hygiene | PASS | No tracked file changed except the task file; `docs/designs/issue-watcher.md`, `pyproject.toml` and `Makefile` have mtimes before the fix (06:41 and 15:08 against 22:43-22:47). Files newer than the consolidated findings are only the 3 source files, 4 test files, the fix report and the task file. No `.bak`, `.orig`, `.rej` or backup files. No trailing whitespace. `__pycache__` is ignored by `.gitignore:2`. Non-`.py` files under the two directories are the 16 `_assumed_shape` fixtures only. No `.claude/` change. |
| Scope of fix | PASS | Only `launch.py`, `record.py`, `predicates.py` and four test files changed, all inside Phases 2 to 5. No assertion deleted or weakened that I could detect (the new and changed tests are strictly stronger; the earlier files are untracked, so no diff base exists, which limits this check). |
| Test count pins | PASS | The full suite passes, including the fixture-count pin and the "every fixture is read" check. |

## Items reviewed summary

- Blocking ids verified: 13 of 13 FIXED, 0 NOT FIXED.
- New blocking structural findings: 0.
- Confidence: Verified: 18/18 | Unverifiable: 1 (execution on a real Python 3.10 interpreter) | Unchecked: 0 | Confidence: 100.0% of the verifiable items.
- Tool engagement: Read: 14 | Grep: 6 | Glob: 0 | Bash: 7 (plus one failed Read on a directory, no effect). Web research: none.

## Mutation probes (private copy in /tmp, removed afterwards)

| Probe | Result |
|---|---|
| baseline `test_launch.py` on the copy | 168 passed |
| remove `isabs` in `find_orca` | killed |
| remove `RecursionError` in `load` | killed |
| `_entry` operation id check reduced to `isinstance` | killed |
| lock `OSError` mapping narrowed | killed |
| `mark_unknown` guard removed | killed |
| `mark_launched` guard removed | killed |
| old key regex `[1-9][0-9]*` | survives (disclosed; same typed result through the `ValueError` catch) |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR (note) | `docs/designs/issue-watcher.md` DF-36 text | Still carries the old "raises on ... a dict, or holds a non-dict" wording that the code docstrings now correct. Declared by the fix agent. | Update the design wording at the next design edit. |
| 2 | MINOR (note) | `record.py:132` | The 9-digit bound has no test of its own (the `ValueError` catch covers the same inputs). | None required. |
| 3 | MINOR (note) | `test_find_orca_parity.py:15` | One docstring line is long. Ruff passes. | None. |

## QA Complete
