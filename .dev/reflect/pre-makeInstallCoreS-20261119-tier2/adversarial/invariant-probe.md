# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent agent (opus-class alias), read-only. Parent verification after receipt: INV-001 confirmed (CPython `filecmp.cmp` clears its cache when `len(_cache) > 100`, checked by printing `inspect.getsource(filecmp.cmp)`); INV-008 confirmed for the installers named (install_core.py:76 copies with `shutil.copy2` and no backup, while install_commands.py:68 and install_user_setup.py:95 call `backup_if_differs`; install_agents.py:56 and install_templates.py:76 also copy with no backup).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | When the fix is reverted, the new test reliably catches the old bug because the first call stores an "identical" answer the second call reuses | UNADDRESSED | MEDIUM | `filecmp.cmp` empties its whole cache once it holds more than 100 entries; the second call compares 8 files that sort before PRINCIPLES.md (install_core.py:15-29, :59). In a long test process with a full cache the purge could hide the old bug. The supplied failing run executed only this test (t2-checks.log:7, `-k same_size`) |
| INV-002 | guard_conditions | If the new test passes, the cache path it targets was exercised | UNADDRESSED | MEDIUM | test_how_we_work_install.py:125 ignores the first call's result; nothing checks PRINCIPLES.md was skipped as identical, and lines 128-129 do not check size and mtime match `before` after the rewrite |
| INV-003 | sufficiency_challenge | The fix makes a real user-facing bug go away | UNADDRESSED | MEDIUM | `filecmp` keys on both paths plus (type, size, mtime); the CLI calls `install_core_files` once per process (main.py:178) and `update` passes `force=True` (main.py:365), which copies without comparing (install_core.py:71-77). No shipped CLI path compares the same pair twice in one process; the bug is reachable only in-process (tests or a long-running caller). Changes priority, not correctness |
| INV-004 | sufficiency_challenge | The fix alone makes the new test pass; every gate between call and assertion lets it through | ADDRESSED | LOW | Traced: install_core.py:71 skip, :88 non-empty skipped, :97-99 `same_content` clears the cache (install_keep.py:22) then compares bytes (:24), :100-106 prints "NOT updated", test:133 `ok` True. Only `shallow=True` would break it; the code uses `False` |
| INV-005 | sufficiency_challenge | Disabling `filecmp.clear_cache` in a throwaway plugin restores the old behaviour and the rewrite recreates the same cache key | ADDRESSED | LOW | Old helper was the same without the clear (prompt-1-1.md:30-34); `same_content` looks up `filecmp.clear_cache` on the module each call; `os.utime(ns=...)` restores mtime exactly (test:129). Caveat: the plugin was not saved (see INV-010) |
| INV-006 | state_variables | The comments state the cache key correctly | UNADDRESSED | LOW | install_keep.py:20 and the test docstring (test:119) say "(size, mtime)"; the real key is (path 1, path 2, type, size, mtime), which is why answers do not leak between tests (and why INV-003 holds) |
| INV-007 | interaction_effects | The fix interacts safely with the other users of `same_content` | ADDRESSED | LOW | install_commands.py:61,68 and install_user_setup.py:90,95 already used it; the whole-process cache clear is a speed cost only; `backup_if_differs` compares the same pair again (install_keep.py:45) |
| INV-008 | interaction_effects | The core-file installer protects user-edited files like the other installers | UNADDRESSED | MEDIUM | install_keep.py:3-7 says `install --force` and `update` back up a differing file first; install_core.py:71-77 copies with `shutil.copy2` and no backup, and `update` always forces (main.py:365), so a user-edited `~/.claude/RULES.md` is overwritten with no copy. Outside this plan's scope; a lead on the function the plan touches |
| INV-009 | guard_conditions | An unreadable kept file is handled correctly | ADDRESSED | LOW | install_keep.py:25-26 turns the read error into False, so it is reported stale; already true before the change (variant-1-original.md:14); the notice says "differ" when the file could not be read (misleading, safe) |
| INV-010 | count_divergence | The supplied logs are consistent and record the stated setup | ADDRESSED | LOW | 351 to 352 passed is exactly one new test (t1-checks.log:6, t2-checks.log:16); 9 tests in the file match "9 passed". Not noted: the failing control run (t2-checks.log:7) is a bare `pytest`, possibly a different environment, the plugin was not saved, and the one skipped test is unidentified |
| INV-011 | collection_boundaries | The byte change works for any shipped PRINCIPLES.md | ADDRESSED | LOW | test:128 works for a one-byte file; an empty file raises IndexError (A-003 QUALIFY); a missing file raises FileNotFoundError at test:122 |
| INV-012 | collection_boundaries | Zero skipped files and exactly one stale file behave correctly | UNADDRESSED | LOW | install_core.py:88 no compare when nothing is skipped; lines 101-103 print the count correctly; no defect |
| INV-013 | guard_conditions | The IndexError failure is only a readability problem | ADDRESSED | LOW | test:134, :113; t2-checks.log:8-10; plan:36; one-line fix `assert "NOT updated" in message, message` should cover both tests |
| INV-014 | state_variables | The uncleared `filecmp.cmp` in orca_worktree.py cannot give a wrong answer | ADDRESSED | LOW | orca_worktree.py:480, 500, 1682; line 500 follows `copyfile`, which sets a new mtime; the advocate did not check whether a caller runs the two functions twice in one process, so "cannot" is not proven (lead only) |

## Summary

- **Total findings**: 14
- **ADDRESSED**: 8 (INV-004, 005, 007, 009, 010, 011, 013, 014)
- **UNADDRESSED**: 6 (INV-001, 002, 003, 006, 008, 012)
  - HIGH: 0
  - MEDIUM: 4 (INV-001, INV-002, INV-003, INV-008)
  - LOW: 2 (INV-006, INV-012)

Fault-finder judgment on the debate: the convergence on the verdict is for good reasons (the fix is correct and enough for the test, INV-004 and INV-005). The advocate reversals on C-001 and C-002 followed a newly checked fact (plan:36 prescribes the `split(...)[1]` expression); the C-003 reversal looks like mild deference on a low-stakes ranking. Both advocates argued inside the frame set by the diff analysis and so shared its blind spots (INV-001, INV-002, INV-003, INV-008).

Gate result: count(HIGH + UNADDRESSED) = 0, so convergence is NOT blocked. Four MEDIUM UNADDRESSED items are logged as warnings and carried into the merged output.
