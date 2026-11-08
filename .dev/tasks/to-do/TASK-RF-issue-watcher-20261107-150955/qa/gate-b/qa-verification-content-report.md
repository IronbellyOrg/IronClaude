# QA Report - Gate B content verification (Step 5.G11)

**Topic:** issue-watch implementation, Gate B (Phases 4 and 5), fix cycle 1
**Date:** 2026-11-08
**Phase:** fix-cycle (rf-qa-qualitative, `fix_authorization: false`)
**Fix cycle:** 1
**Inputs read:** `qa/gate-b/qa-consolidated-findings.md`, `qa/gate-b/qa-fix-report.md`, the changed sources (`record.py`, `launch.py`, `predicates.py`) and tests (`test_record.py`, `test_launch.py`, `test_predicates.py`, `test_find_orca_parity.py`), the design (`docs/designs/issue-watcher.md` 5.3, 7.6, 8.4, 9.2), `install_user_setup._find_orca`.

---

## Overall Verdict: PASS

All 13 blocking findings are fixed in the code or the tests, each against the design rows it cites. No assertion was weakened or deleted (all 1372 pre-fix test ids are still present and pass). No new blocking content issue was found.

## Per-finding verification (B-1 to B-13)

| id | Result | Evidence |
|----|--------|----------|
| B-1 | FIXED | `launch.py:144-153` and `test_find_orca_parity.py:1-19` now say the original raises on null, int, bool, a non-empty str or dict, and a list with a non-dict before any `orca-cli` dict. I read `install_user_setup.py:198-221`: `topics` is iterated outside the `try` at line 219, so an empty str or dict yields zero iterations and a list with the `orca-cli` dict first short-circuits `any`. The new wording is true and agrees with `_SAME_RESULT` (lines 52-53) and `_ORIGINAL_RAISES` in the same file. DF-36 text in the design still has the old wording; the fix agent was not allowed to edit it (note below). |
| B-2 | FIXED | `test_launch.py:558-590`: `_id_reply` and `_no_id_reply` copy `orca_launch_success.json["payload"]` and set or delete the id at `OPERATION_ID_PATHS[0]`. Grep for `receipt`, `"outcome"`, `operation_id":`, `"error":` over `tests/issue_watch/*.py` finds no inline Orca reply body (the only hits are record-store dicts at `test_record.py:91,293,906,1206`). The success assertion (`:608-613`) and the unknown test (`:695-706`) read the fixtures through the paths. Fixture files are the 16 under `fixtures/_assumed_shape/`, unchanged. |
| B-3 | FIXED | `record.py:391-397`: `FileNotFoundError` gives `lock_missing`; every other `OSError` gives `lock_invalid`. Design 7.6 line 515-516 names ELOOP and EISDIR as `lock_invalid` and exit 6 covers `lock_missing`/`lock_invalid` (design line 162, 345), so the mapping stays in the closed set. I probed it: `chmod 0` on the lock gives `LockError lock_invalid`; a state_dir that is a file gives `LockError lock_invalid`. Test `test_record.py:739-750` does the real `chmod 0`, restores the mode in `finally`, and checks the lock is free afterwards. It skips as uid 0 (root ignores mode bits), the same limit as B-32. |
| B-4 | FIXED | `test_record.py:2142-2225`: parametrized over approver id, event id and account id (0, -1, True, False, "11", None, 1.5), naive/None/str/int `approved_at`, non-absolute or non-str `launch_cwd`, empty or non-str `launch_login`, for `mark_pending`; the id and time cases again for `mark_claimed`; one case on a `failed` entry. Each goes through `refused()` (`:2157-2162`), which requires `ValueError` and a document equal to its deep copy, and most also assert no entry was created. The guards are at `record.py:494-500`, `:547-553`. A deleted guard fails the matching case. |
| B-5 | FIXED | `test_record.py:2228-2239`: `mark_launched` with `""`, `"a;b"`, `"$(id)"`, `"op\n1"`, 129 chars, None, 5, `b"op"`, a list and True raises `ValueError`, input unchanged, state still `pending`; ids of 1 and 128 characters are kept. Guard at `record.py:585-586`. |
| B-6 | FIXED | `test_record.py:2283-2301`: `fail` and `mark_pending` with n in 0, -1, True, "7", None, 7.0, 10**9 raise `ValueError` and create no entry (`_new_entry` guard `record.py:467-468`); `init_state` with a naive `now` raises and creates no directory (`record.py:771`, the `_to_raw` pre-check). |
| B-7 | FIXED | `test_record.py:2313-2369`: `set_considered` is pinned for stamp, keep-old-time-when-unexamined, drop-undiscovered, no stamp for examined-but-undiscovered, iterators, empty discovered, input and other fields untouched; `set_next_permitted` (set, clear, input untouched); `set_last_completed` (exactly `now`). Design line 356 ("every examined candidate ... pruned to the discovery set") matches `record.py:738-745`, so the tests pin the specified behaviour and not an accident. |
| B-8 | FIXED | `test_record.py:394-405`: `TIME_PLACES` now holds `last_completed_cycle_at`, `approved_at` and `pending_at`, each run against all 11 `BAD_TIMES`. Wrong-type cases for `last_completed_cycle_at` are at `:265-266`; the loaded `last_completed_cycle_at`, `approved_at` and `pending_at` are asserted at `:185-191`. |
| B-9 | FIXED | `test_record.py:2021-2043`: the writer is patched to leave 0666 (same `wide()` as the `FileStore.save` twin at `:620-633`), so only `save_dry_run`'s own `os.chmod` (`record.py:864`) can give 0600; the test no longer passes with the chmod deleted. `:2046-2062` observes the directory fsync as the last fsync (`record.py:865`). |
| B-10 | FIXED | `predicates.py:57-67` holds `OPERATION_ID_PATTERN` and `valid_operation_id` (uses `fullmatch`; probed: `"op\n"` is rejected, non-ASCII is rejected). `record.py:183` (`_entry`, on load), `:585` (`mark_launched`), `:607` (`mark_unknown`) enforce it. `launch.py` keeps its own copy because design 5.3 line 240 lets `launch` import only `runner`; `test_launch.py:194-200` pins pattern and flags equal (probed: both True). Tests: on-disk unsafe ids give `store_invalid` (`test_record.py:336-352`), safe ids at both bounds load (`:355-358`), unit tests in `test_predicates.py:674-702`. Design 9.2 line 689 (only a regex-passing id is stored; an id that fails it is stored as null) is consistent: the launch layer already maps a bad id to `unknown` with None. |
| B-11 | FIXED | `record.py:607-608`: `mark_unknown` raises `ValueError` unless the id is None or a valid str. `test_record.py:2256-2260` round-trips `validate(_to_raw(after)) == after` for every allowed (state, trigger) pair, `:2263-2266` does it for `sweep`, and `:2269-2280` saves and reloads a valid id after the hostile ones are refused. One behaviour change: `mark_unknown(..., "")` used to store None and now raises; `LaunchOutcome` never carries `""` (its `__post_init__` accepts None or a pattern match), so no caller is affected. |
| B-12 | FIXED | `record.py:132` bounds keys to `[1-9][0-9]{0,8}` (9 digits equals `MAX_ISSUE_NUMBER` 999,999,999). `load` (`:361-366`) and `load_dry_run` (`:845-848`) catch `RecursionError`, and `load` also wraps `migrate` and `validate`. I probed a 5000-digit key, a 200,000-deep `[`, and non-UTF-8 bytes: each gives `StoreError store_invalid`. Tests at `test_record.py:316-333` and `:2065-2084` cover both keys (`entries`, `considered`) and both nesting shapes for both loaders. See the minor note on the key bound. |
| B-13 | FIXED | `launch.py:184`: a `which()` result that is not absolute is skipped before any probe, and the path probed is the path returned. I probed `which -> "./orca-ide"`: result None, zero runner calls. Tests `test_launch.py:320-343` cover `./orca-ide`, `orca-ide`, `bin/orca-ide`, `../orca` (None, no call), a relative first candidate with an absolute second (probed and returned), and probed path equals returned path. |

## Checks on the fix as a whole

| Check | Result | Evidence |
|-------|--------|----------|
| A fix that only silences a test | none found | Each finding changed production code or added the missing case. B-1 and B-2 changed text and fixtures-derivation (the findings asked for exactly that). B-9 strengthened an existing test. |
| Assertion weakened or deleted | none | I took the 1372 PASSED node ids from `phase-outputs/test-results/p5-g1-raw.txt` and compared them with a verbose run of the current tree: 0 missing, 1577 present, all PASSED (205 added). The tests I read that were edited in place (`:185-191`, `:394-405`, `:2021-2043`, `test_launch.py` reply helpers) are stricter than before. |
| New wrong behaviour, false claim, missing deliverable, security or data-loss risk | none | Probes above; `mark_unknown("")` behaviour change checked against `LaunchOutcome`; new docstrings re-read against the code they describe. |
| Scope of the fix agent | clean | `git status` shows only the issue_watch source and test trees, the task file and the report folders; nothing under `.claude/`, no `pyproject.toml` or `Makefile` change. `/tmp/record.bak` and `/tmp/launch.bak` are byte-identical to the current files, so no mutation was left behind. |
| Test and lint state (spot check, not the structural verdict) | pass | `uv run pytest tests/issue_watch/ -q`: 1577 passed. `uvx --offline ruff@0.15.20 check` and `format --check` over `src/superclaude/cli/issue_watch` and `tests/issue_watch`: all passed, 18 files formatted. |

## Summary
- Blocking ids verified: 13 / 13 FIXED
- New blocking findings: 0
- Checks passed: 15 / 15 (13 ids, no-weakening, no-new-blocking)
- Critical issues: 0

## Issues Found (all MINOR, notes only, not rechecked later)

| # | Severity | Location | Issue | Suggested follow-up |
|---|----------|----------|-------|---------------------|
| 1 | MINOR | `record.py:132`; `test_record.py:316-324` | The `{0,8}` key bound is not pinned by itself: restoring the old regex still passes, because the widened `except ValueError` in `load` catches the `int()` error. The fix report says so. A direct `validate()` call with a 4301-digit key has no test. | Add one `validate({... "entries": {"1"*4301: ...}})` case expecting `StoreError`. |
| 2 | MINOR | `record.py:23-29`; design 5.3 line 239 | The fix adds `valid_operation_id` to the `record` import from `predicates`, widening the already-recorded B-24 reading ("types only"). Import-boundary tests walk module names, so nothing breaks. | Resolve with B-24 (amend the design cell to "pure helpers and types"). |
| 3 | MINOR | `launch.py:174-178`; design 612; `test_find_orca_parity.py` | `find_orca` now deliberately differs from `_find_orca` (skips non-absolute paths). The parity module docstring and design 8.4 do not list this difference; parity tests use absolute fake paths so they are unaffected. | Add one sentence to the parity docstring and the design at the next design edit. |
| 4 | MINOR | `launch.py:95-116` | `launch_argv` and `OrcaLauncher.launch` do not themselves require an absolute `orca`; protection rests on `find_orca` being the only source. | Optional check in `OrcaLauncher.launch` in Phase 6. |
| 5 | MINOR | design DF-36 text and line 613 | Still carries the old "raises on a topics that is null, an int, a str, a dict" wording (outside the fix agent's scope). | Correct at the next design edit. |
| 6 | MINOR | `test_record.py:739` | The `chmod 0` lock test skips as root (same limit as B-32). | None. |

## Actions Taken
None (report-only). Only this report file was written. Temporary id lists I made under `/tmp` (`qa_pre_ids.txt`, `qa_post_ids.txt`) are outside the repository.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- The spawn prompt carried no `## Inherited Structural Verdict`, so I fell back to standalone behaviour. I did not rely on the structural verification report (Step 5.G10, run in parallel) and did not read it.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- B-1 claim truth: read `install_user_setup.py:198-221` and compared each shape in the new docstrings with Python iteration semantics, and with `_SAME_RESULT` and `_ORIGINAL_RAISES` in the parity test.
- B-3, B-10, B-12, B-13 behaviour: ran a Python probe against the real code (`chmod 0` lock, state_dir that is a file, 5000-digit key, 200,000-deep JSON, non-UTF-8 store, `which -> ./orca-ide`, `"op\n"`, pattern equality); every result matched the claim.
- No-weakening: diffed pre-fix and post-fix pytest node ids (1372 vs 1577, 0 missing).
- B-7 spec fidelity: read design lines 352-356 to confirm the new `set_considered` tests pin the specified stamp-and-prune behaviour.
- B-2: grepped all of `tests/issue_watch/*.py` for inline Orca reply shapes (none left) and read both `_assumed_shape` fixtures.
- Tavily/web: not used; no external lookup was needed.

## Confidence
Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 16 | Grep: 9 | Glob: 2 | Bash: 8 (above the 15 checklist items)

## QA Complete
