# QA Report — Gate B security-invariants lens

**Topic:** issue-watch Phases 4 and 5 (record.py, launch.py and tests)
**Date:** 2026-11-07
**Phase:** task-qualitative (lens: security-invariants)
**Fix cycle:** N/A
**Fix authorization:** false (report only)

**Scope read:** `src/superclaude/cli/issue_watch/{record,launch,runner,github}.py`, `tests/issue_watch/{conftest,test_record,test_launch,test_origin_parity,test_find_orca_parity,test_marker_contract}.py`, the two `_assumed_shape` fixtures, `src/superclaude/cli/swarm/atomic.py`, `docs/designs/issue-watcher.md` sections 7, 8.4, 9. Four edge cases were also run through `uv run python -I` against temp directories (no repo file written).

## Overall Verdict: FAIL

Four blocking findings (B1 to B4), all reproduced by running the code. Thirteen minor notes follow. The 12-element argv, prompt gate, no-shell, file/dir modes, lock checks, launches monotonicity and origin check all hold (see the table below).

## Invariant-by-invariant result

| Invariant asked for | Result | Evidence |
|---|---|---|
| Only `build_claim_prompt(int)` text reaches `--prompt`; `type(v) is int`, 1..999999999, bool rejected | HOLDS | launch.py:89-91 `type(n) is not int or not 1 <= n <= MAX_ISSUE_NUMBER`; launch.py:100 `PROMPT_PATTERN.fullmatch` in `launch_argv`; `[1-9][0-9]{0,8}` ASCII digits only; test_launch.py:45-57,116-145 (bool, str, float, 10**9, newline, fullwidth digit, trailing space) |
| Nothing else data-derived in argv except Orca path and worktree | HOLDS with caveat | launch.py:102-115 constants only; caveat is B4 (the Orca path is not required to be absolute) |
| Launch argv exactly 12 elements, no permission-widening flag | HOLDS | launch.py:102-115 counted 12; test_launch.py:74-108 equality, 12-length, flag list pinned |
| Runner is the only spawner; launch.py builds no shell string | HOLDS | Grep for `subprocess/Popen/os.system/shlex/shell=` in the package: only runner.py:10,91-100 (`shell=False`, argv list, stdin DEVNULL); launch.py has no hit except `"/".join` of owner/repo |
| Store file 0600, dir 0700 | HOLDS | record.py:770-771, 775-776, 785; save at 368-376 over `mkstemp` (0600 from creation, atomic.py:22-26); probe printed dir 0o700, store 0o600, lock 0o600; test_record.py:578, 1709-1725 |
| Lock: O_NOFOLLOW, regular file, owner, inode, link count; bad lock never lets a cycle run | HOLDS | record.py:391-416 matches design 7.6 table step for step; tests 652-749 (symlink, dangling, dir, foreign uid, replace, unlink) |
| Pending written before any launch; launches never lowered once 1 except reset of abandoned/unknown | HOLDS in code, not pinned by a test | every transition in record.py:505-713 uses `replace(entry, ...)` and never sets `launches` except `mark_pending` (0 to 1, from None or failed, record.py:546-563); `reset_entry` removes the entry (record.py:699-713). No test asserts `launches` is non-decreasing over the allowed-pair table (M6) |
| Unreadable, truncated, higher-version or missing store never repaired or reset | HOLDS for dispatch.json | `FileStore.load` never writes (record.py:345-366, test_record.py:470); `migrate` rejects version > 1 (record.py:264); `init_state` refuses an existing file (record.py:766-768). `dry-run.json` is reset by design (design line 449) |
| Operation id validated with the regex before it can be stored or printed | FAILS at the record layer | B1, B2 |
| Origin compared case-insensitively with ironbellyorg/ironclaude, fails closed on every error | HOLDS | launch.py:220-229; tests 389-444, test_origin_parity.py:119-176 |
| No module writes to GitHub | HOLDS | github.py:175-260: `gh api user`, `gh issue list`, REST calls with `--method GET`, GraphQL queries only (EDITS_QUERY, PROJECT_ITEMS_QUERY, no `mutation`); Grep for mutation/POST/PATCH/issue edit/comment found only the DF-28 comment and read argv |

## Blocking findings

## Issues Found

| # | Severity | Axis | Location | Issue | Required Fix |
|---|---|---|---|---|---|
| B1 | CRITICAL (blocking) | AX-3 | record.py:582-595 (`mark_launched`), 598-610 (`mark_unknown`), 180-181 (`_entry`) | The operation-id regex lives only in launch.py (`OPERATION_ID_PATTERN`, enforced by `LaunchOutcome.__post_init__`). The record layer checks only "non-empty str" on write and "str or null" on load. Reproduced: `mark_launched(doc, 8, "x; rm -rf ~\n\x1b[31m", now)` saves, and `FileStore.load()` returns that exact string. Design 9.2 says the id is printed by `status` inside a shell command the operator copies, and that only a regex-passing id may reach the store. Today the only guard is the caller using `LaunchOutcome`; a hand-edited or tampered `dispatch.json` carries any string to `status`. | Put the regex where record.py may import it (`predicates`, record imports only stdlib and predicates by design) and use it from both modules. `mark_launched` raises `ValueError` on a non-match; `mark_unknown` stores None or a match; `_entry` rejects a non-null id that does not match with `store_invalid`. Add tests for each of the three entry points with `"a;b"`, `"$(id)"`, `"op\n1"`, 129 characters. |
| B2 | CRITICAL (blocking) | AX-2 | record.py:598-610 | `mark_unknown` has no type check: `operation_id=operation_id or None` stores any truthy object. Reproduced: `mark_unknown(doc, 7, 5, now)` then `save` succeeds, and the next `load` raises `StoreError("store_invalid")`. Because an invalid store is never repaired or reset automatically, one bad call makes the watcher refuse every later cycle until the owner intervenes. The writer produces a file its own validator rejects (validate at 180-181 requires str or null). | In `mark_unknown` raise `ValueError` unless the id is None or a valid str (same check as B1). Add a test that a non-str id raises and that `validate(_to_raw(result))` round-trips for every transition output. |
| B3 | IMPORTANT (blocking) | AX-2 | record.py:132 and 159-165 (`_DECIMAL_KEY`, `_issue_key`), 360-362 (`load`), 839-841 (`load_dry_run`) | `validate`'s docstring (lines 211-222) promises `StoreError("store_invalid")` on any deviation, and design NFR-011 maps a bad store to exit 6. Two inputs break that. (1) A key of 4301 or more decimal digits passes `[1-9][0-9]*` and then `int(key)` raises a raw `ValueError` (reproduced: `ValueError`). (2) Deeply nested JSON makes `json.loads` raise `RecursionError`, which `except ValueError` does not catch (reproduced: `RecursionError` from `FileStore.load`; `load_dry_run` catches only `(ValueError, StoreError)` and has the same hole). launch.py already handles `RecursionError` (launch.py:138), so the two modules disagree on the same input class. The result is an unclassified traceback instead of exit 6, so no closed audit reason is written. | Bound the key regex to `[1-9][0-9]{0,8}`; catch `RecursionError` next to `ValueError` in both loaders and raise `StoreError("store_invalid")` (dry-run: return the reset shadow). Add the two inputs to the invalid-store tests. |
| B4 | IMPORTANT (blocking) | AX-5 | launch.py:160-181 (`find_orca`), 336-348 (`OrcaLauncher.launch`) | `find_orca` returns whatever `which()` gives and never requires an absolute path. Reproduced: `which` returning `./orca-ide` is accepted. The probe runs with `cwd=None`, but the launch runs with `cwd=str(worktree)`; `subprocess.run` resolves a relative executable against that `cwd`, so the binary that was probed is not the binary that is launched, and a file named `orca-ide` inside the worktree (repository content) would be executed with the Orca arguments. Needs a relative entry in PATH, so it is a hardening gap, but the stated invariant is "only the resolved Orca path", and nothing proves it is a single fixed binary. All parity tests use `/bin/...` paths (test_find_orca_parity.py:126-133), so none exercises this. | In `find_orca` skip any candidate for which `os.path.isabs(path)` is false (or resolve it with `os.path.realpath` before the probe and return that). Add a test where `which` returns `./orca-ide` and the result is None with no probe. |

## Minor notes (do not affect the verdict)

| # | Axis | Location | Note |
|---|---|---|---|
| M1 | AX-2 | launch.py:270-281, 304-327 | `_first_hit` tries `receipt.operation_id` then `error.operation_id`, and `outcome_of` uses it for the exit-0 success branch. Reproduced: exit 0 with `{"error": {"operation_id": "op-1"}}` and exit 0 with `{"outcome": {"kind": "failed"}, "receipt": {"operation_id": "op-1"}}` both give `launched/ok`. It fails safe (launches stays 1, no relaunch) and matches design row 633, but the success fixture names `outcome.kind` and the code never reads it. Re-check once FU-1 records a real reply; no test covers the error-path id at exit 0. |
| M2 | AX-5 | launch.py:35, 118-131 | The mandated regex allows a leading `-`. Reproduced: `retry_argv(..., "--agent")` gives `... --retry-launch --agent --json`. Only Orca's own reply can supply the id, so risk is low. Consider requiring an alphanumeric first character (a design change, owner decision). |
| M3 | AX-3 | launch.py:211-229 | `check_origin` reads the fetch URL only (`git remote get-url origin`, which also applies `insteadOf`). A `pushurl` pointing elsewhere is not examined. Given the repository rule about never pushing to the upstream, record this as a residual in the design. |
| M4 | AX-3 | record.py:345-366, 378-421 | `load` does not check that `dispatch.json` is a regular file owned by the user (the lock gets that check), and `read_bytes` on a FIFO would block with no timeout; the mode of `state_dir` is only set in `init_state`, never re-checked. Needs write access to the state directory, where the attacker could do more, so minor. |
| M5 | AX-2 | record.py:396-399 | `lock()` re-raises a raw `OSError` for EACCES and ENOTDIR instead of a closed `LockError` reason. No cycle runs, but no audit reason is written. |
| M6 | AX-3 | tests/issue_watch/test_record.py:1303-1310 | The allowed-pair test checks only `check_reasons`. No test asserts `new.launches >= old.launches` for every allowed pair, which is the invariant behind the at-most-once argument (design line 533). Also untested: the B1 to B4 inputs. |
| M7 | AX-1 | launch.py:29 vs predicates.py:20 | `MAX_ISSUE_NUMBER` is defined twice (and a third time in audit.py:197). test_audit.py:479 pins audit against predicates; nothing pins launch.py or `PROMPT_PATTERN` (`{0,8}`) to the same bound. |
| M8 | AX-2 | record.py:174-208 | `validate` accepts states the transitions never create: `pending`, `launched` or `unknown` with `launches` 0, and a negative `approver_id` (writers require positive, record.py:492-499). Matches the design's listed checks, so only a hardening note. |
| M9 | AX-3 | record.py:360 | `json.loads` keeps the last of duplicate keys, so a doubled `"launches"` or `"entries"` is not detected. |
| M10 | AX-3 | record.py:770-771 | `os.chmod(state_dir, 0o700)` follows a symlink and there is no `lstat` check on `state_dir`. |
| M11 | AX-2 | launch.py:244-252 | `LaunchOutcome` accepts inconsistent pairs (`kind="spawn_error"` with detail `"ok"`, `kind="launched"` with detail `"timeout"`). |
| M12 | AX-3 | record.py:374-376 | If `_fsync_dir` raises after `os.replace`, the new file is already durable but the caller sees a failed save. Safe for the pending write (no launch follows), but the cycle must treat it as "may have been written". |
| M13 | AX-4 | tests/issue_watch/test_marker_contract.py:22-39 | Reads `~/.claude` when present, so the result depends on the developer's installed copy. Not a security issue. |

## Actions Taken

None (fix_authorization false). No file other than this report was written; the probes used `tempfile.mkdtemp()` under the system temp directory.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | The ruff/pytest results in gate-b-change-set.md were not re-run (pytest and ruff write caches; report-only rule). The probes I ran against record.py and launch.py behave as the tests assume except for B1 to B4 inputs, which no test covers. |
| 2 | Project convention compliance | none | PASS | launch.py imports only stdlib, `runner`, `_ORCA_CLIS` (design 5.3); record.py module level imports stdlib and predicates only, `swarm.atomic` lazily (record.py:370, 846); no `src/superclaude/` path hardcoded in a primitive. |
| 3 | Intra-phase execution order | none | PASS | Fixtures (5.2) exist before test_launch uses them; conftest imports `launch_argv`/`LaunchOutcome` that exist. |
| 4 | Signature verification | AX-2 | FAIL | B2: `mark_unknown(operation_id: str \| None)` accepts non-str; B1: `mark_launched` accepts any non-empty str. |
| 5 | Module context / cross-symbol input shape | AX-2 | FAIL | B3: `launch._json_object` catches `RecursionError`, `record.load`/`load_dry_run` do not; `_issue_key` vs `validate` docstring. Operation-id shape differs between launch.py (regex) and record.py (any str), B1. |
| 6 | Downstream consumer analysis | none | PASS | See Confidence: consumers `cycle.py`, the CLI `status` verb and the runner wiring do not exist yet, so only the producer side was checked (counted UNVERIFIABLE below). Within the change set, `FakeLauncher`/`CrashingStore` track the real signatures. |
| 7 | Test validity | AX-4 | FAIL | M6: the allowed-pair test never asserts `launches` monotonicity; other tests are real (symlink, replaced lock, foreign uid, fixtures from files). |
| 8 | Test coverage of primary use case | none | PASS | Launch argv, outcome table, origin parity and lock/save/init cycle each have end-to-end style tests; gaps are listed in M6 and B4. |
| 9 | Error path coverage | AX-3 | FAIL | B3 (raw ValueError / RecursionError), M5 (raw OSError from lock). |
| 10 | Runtime failure path trace | none | PASS | Traced input to `LaunchOutcome` to `mark_*` to `save` to `load`; the break points are B1 to B3 and are reported there; cycle-level handling is UNVERIFIABLE (no cycle.py yet). |
| 11 | Completion scope honesty | AX-3 | FAIL | design 9.1 T8 lists `test_record.py` for 0600/0700 and exit 6 on damage; the exit-6 claim is not true for the B3 inputs. |
| 12 | Ambient dependency completeness | none | PASS | `_ORCA_CLIS` imported and pinned by test_find_orca_parity.py:221; `OPERATION_ID_PATHS`, `LAUNCH_DETAILS` exported and used by tests. |
| 13 | Kwarg sequencing | none | PASS | `cwd=` kwarg exists in the `Runner` protocol, `SubprocessRunner.run`, `FakeRunner.run` (runner.py:41-45, 70-72; conftest.py:84-86). |
| 14 | Function existence claims | none | PASS | Grepped every symbol named in the change set and design lines 618-636 (`launch_argv`, `retry_argv`, `outcome_of`, `find_orca`, `check_origin`, `write_prepared_bytes` at atomic.py:14). |
| 15 | Cross-reference accuracy | none | PASS | Design 7.6 lock table, 8.4 outcome table and 9.2 boundary table read and compared with the code; code comments citing `origin_repo.py:65-69, 86-99` not re-read (minor). |

## Summary

- Checks passed: 10 / 15
- Checks failed: 5
- Critical issues: 2 (B1, B2); important blocking: 2 (B3, B4); minor notes: 13
- Issues fixed in-place: 0 (report only)
- Axis lens status: AX-1 applied through the design and fixture comparison (GOAL verbatim not supplied in the spawn prompt, so drift was judged against the prompt's invariant list and design sections 7, 8.4, 9 instead of BUILD_REQUEST.GOAL); no AX-1 blocking finding.

## Self-Audit

**(a) Reliance list: items taken from other reports and not re-checked:**
- No `## Inherited Structural Verdict` was in the spawn prompt, so I ran standalone (no rf-qa PASS items relied on).
- gate-b-change-set.md pass counts (1094 and 1372 tests, ruff and lint exit 0) were read as context only and not re-run; I make no claim about them.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Operation id at the store boundary: read record.py:180-181, 582-610, then ran `mark_launched` with shell text and ESC and `mark_unknown` with `5` in a temp store (output: id accepted and reloaded; `store_invalid` after reload).
- Loader contract: ran `FileStore.load` with a 5000-digit key and a 200000-bracket file (output: `ValueError`, `RecursionError`).
- Orca path: ran `find_orca` with `which` returning `./orca-ide` (returned it) and read runner.py:90-100 for the cwd rule.
- Spawn surface: Grep over the package for subprocess, Popen, os.system, shlex, `shell=` (only runner.py).
- Modes: printed `stat` of dir, store and lock after `init_state` and `save` (0700, 0600, 0600); read atomic.py:22-26 (mkstemp).
- Write surface: read github.py:175-260 and grepped for mutation, POST, PATCH, issue edit/comment.
- Outcome mapping: ran `outcome_of` on an exit-0 error-only reply and an `outcome.kind: failed` reply (both `launched`, noted as M1).

## Confidence

- **Confidence:** Verified: 13/15 | Unverifiable: 2 | Unchecked: 0 | Confidence: 100.0% (13 / (15 - 2))
- **Tool engagement:** Read: 19 | Grep: 14 | Glob: 4 | Bash: 2 (37 calls, above the 15 items)
- UNVERIFIABLE: item 6 and item 10 (consumer side only): `cycle.py`, the CLI verbs and the runner wiring that will call `mark_*`, `retry_argv` and `status` are not in the repository yet (Glob of the package found no cycle.py), so what `status` prints and how a cycle handles an exception from `lock()` or `load()` could not be checked.
- UNCHECKED: none.

## Recommendations

1. Fix B1 and B2 together: one shared operation-id check used by launch.py and record.py (store write, store load, retry print).
2. Fix B3: bounded key regex and `RecursionError` handling in both loaders, with tests.
3. Fix B4: reject a relative Orca path in `find_orca`, with a test.
4. Then take M6 (launches monotonicity test), M5 and M1 as cheap follow-ups; the rest are residual notes for the design owner.

## QA Complete
