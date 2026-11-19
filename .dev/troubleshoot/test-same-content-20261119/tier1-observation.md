# Tier 1 observation (run-bound: local pytest, same-shell, 2026-11-19)

## Captured failing-run output (command: `uv run pytest tests/cli/test_install_keep.py -q -k same_content`)

```
tests/cli/test_install_keep.py:43: in test_same_content_is_true_only_for_identical_readable_files
    assert not same_content(a, b)
E   AssertionError: assert not True
E    +  where True = same_content(PosixPath('/tmp/pytest-of-coder/pytest-58/test_same_content_is_true_only0/a'), PosixPath('/tmp/pytest-of-coder/pytest-58/test_same_content_is_true_only0/b'))
1 failed, 13 deselected
```

Repeat runs of the same command: 1 passed, then 1 failed x5 (six runs in total, one pass).

## Captured probe output (same shell)

```
first True
sig equal after rewrite: True (32768, 1, 1795050557.418777) (32768, 1, 1795050557.418777)
second True
after clear_cache False
```

Source printed from the standard library (`filecmp.cmp`): the `_cache.get((f1, f2, s1, s2))` lookup comes before `_do_cmp`; `_sig` = (file type, size, mtime).

## Rerun in the full make test (before the owner synced the mirror)
This test also failed in the first `make test` run and in the rerun after the sync (1 failed, 28414 passed).

## Behaviour definitions

See behaviour-definitions.md row 1 (stdlib filecmp.cmp and _sig source, verbatim).

## Parent probe 2 (same shell, 2026-11-19; script /tmp/probe_same_content.py; writes only under temp dirs; command `uv run python /tmp/probe_same_content.py`)

```
runs=200 same_mtime_tick=188 wrong_true_answers=188 (wrong answers iff mtime unchanged: verified per run)
forced same signature: same_content -> True (expected False)
after clear_cache -> False
proposed fix, forced same signature -> False (expected False)
```

Meaning: with the real test sequence (write x, compare, write y, compare) the two writes landed in the same mtime tick in 188 of 200 runs, and in every one of those 188 runs `same_content` wrongly returned True; in the 12 runs where the mtime changed it returned False. The proposed fix (clear the cache first), applied to a local copy of the function only, returned False in the forced same-signature case. No repo file was changed.

Also read: `src/superclaude/cli/install_core.py:121-125` has its own private `_same_content` that calls `filecmp.cmp(a, b, shallow=False)` the same way, so it has the same latent flaw.

## Parent probe 3 (inside the real failing pytest process; 2026-11-19; command `PYTHONPATH=/tmp uv run pytest tests/cli/test_install_keep.py -q -k same_content -p probe_plugin`, six runs; the throwaway plugin /tmp/probe_plugin.py wraps `filecmp.cmp` to log `b`'s mtime, size and whether the cache already held the key; no repo file changed)

```
run 1: PROBE b mtime_ns=1795051668232527094 size=1 cache_hit=False result=True
       PROBE b mtime_ns=1795051668232527094 size=1 cache_hit=True  result=True   -> 1 failed
run 2: same pattern (mtime_ns 1795051669275551262 on both calls, second call cache_hit=True, result True) -> 1 failed
run 3: same pattern (1795051670338575893) -> 1 failed
run 4: same pattern (1795051671408600686) -> 1 failed
run 5: same pattern (1795051672469625271) -> 1 failed
run 6: same pattern (1795051673511649415) -> 1 failed
```

Meaning: in all six runs of the real test, `b`'s mtime_ns was identical on the first and second call, the second call was answered from the cache (`cache_hit=True`), and the test failed. This is the measurement the Falsification standard asked for. Note: the plugin runs only one tick-sensitive pytest process per run, so this sample (6 of 6 fail) is more adverse than the earlier plain runs (5 of 6 fail).
## git history of the two files (parent, 2026-11-19, command output)
$ git log --format="%h %cI %s" -- src/superclaude/cli/install_keep.py tests/cli/test_install_keep.py
5fa680778 2026-11-09T22:21:16-05:00 fix(install): name kept files that differ and save them before a forced overwrite (refs #346) (#480)
$ git diff --stat master...HEAD -- src/superclaude/cli/install_keep.py tests/cli/test_install_keep.py src/superclaude/cli/install_core.py (branch vs master)
 src/superclaude/cli/install_core.py |  21 +++++
 src/superclaude/cli/install_keep.py |  46 +++++++++
 tests/cli/test_install_keep.py      | 180 ++++++++++++++++++++++++++++++++++++
 3 files changed, 247 insertions(+)
$ git status --short -- src/superclaude/cli/install_keep.py tests/cli/test_install_keep.py src/superclaude/cli/install_core.py (worktree)
(empty output above means no change)

$ git log --oneline origin/master..HEAD -- src/superclaude/cli/install_keep.py tests/cli/test_install_keep.py src/superclaude/cli/install_core.py   (changes on this branch, not on origin/master, to the three files; local master is behind and made them look new)
(empty = this branch changed none of them)
$ git branch --contains 5fa680778 --list ironbelly/issue-606
* ironbelly/issue-606
