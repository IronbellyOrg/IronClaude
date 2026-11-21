pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a
## Task 11: Implement the removal pipeline: terminal close, second check, exact-path clear, removal, branch, read back
Acceptance criteria:
- The order of recorded commands (asserted by the tests of Task 13) is: archive commands, `orca terminal close`, the re-check reads, `xargs -0 git clean -f -x --`, the removal, `git branch -d`, the read-back reads.
- `git clean` is issued only after `VERIFIED` and only with paths from `saved-paths.txt`; a path not in the list is refused by the runner before any process starts.
- No recorded command contains `--force`, `-D`, `rm`, `worktree prune`, a remote delete or a push outside the evidence clone.
- A worktree with a tracked edit, or a commit after the pull request, produces no archive, no terminal close and no clear.
- When Orca still lists the worktree at the read back, the result is "removed in git but still listed in Orca": a failed row (exit 69), because no deregister command is proven.
AC ids (in source order): T11.AC1, T11.AC2, T11.AC3, T11.AC4, T11.AC5
Steps:
1. In `/home/coder/workspaces/worktrees/IronClaude/issue-687/scripts/worktree_cleanup.py`, change only `_read_back` and `orca_lists` in the removal pipeline section. Leave `remove_worktree`, `_remove_branch`, `_safe_sha`, the archive digests and the runner as they are.
2. In `_read_back`, after the git list check, run `orca worktree list --json` from the main checkout as now. If it exits non-zero, return "read back failed: orca worktree list failed" whether or not `orca` is None. Remove the `if orca is None: return None` early return. Call `orca_lists(seen.stdout, wt.path, orca.worktree_id if orca is not None else "")`. Return "read back failed: the orca worktree list could not be read" when it gives None, "removed in git but still listed in Orca" when it gives True, and None only when it gives False. Use these exact reason strings, because the existing tests and the AC use them.
3. In `orca_lists`, skip a value that is not a string or is empty, and compare against the id only when `worktree_id` is non-empty. Keep path matching by `os.path.normpath`. Also match `os.path.realpath(path)`, so a symlinked parent folder cannot hide a still-listed worktree. If the top-level JSON object has `"ok": false`, return None: it is an Orca error reply and cannot be read as "not listed". Keep `orca_lists("[]", ...)` and `orca_lists("{}", ...)` returning False, so the accepted unit test at attempt-2.diff:754-757 still passes.
4. In `/home/coder/workspaces/worktrees/IronClaude/issue-687/tests/worktree_cleanup/test_removal.py`, add tests that use the `setup` fixture (no Orca row, so the removal goes through `git worktree remove`):
   a. The Orca list reply is `{"ok": true, "result": {"worktrees": [{"path": "<worktree path>", "worktreeId": "x::<worktree path>"}]}}`. Assert the status and reason are failed and "removed in git but still listed in Orca", the folder is gone, a `worktree remove` verb was recorded, and no `orca worktree rm` was recorded.
   b. The reply is `<html>`. Assert failed with "read back failed: the orca worktree list could not be read".
   c. The list exits 1. Assert failed with "read back failed: orca worktree list failed".
   Override the reply through `setup.orca_replies[("worktree", "list")]`, as the existing Orca tests do.
5. Add unit checks to the `orca_lists` test. A row `{"id": "", "path": "/other"}` with an empty id is not a match (False). A row with no id field is not a match. `{"ok": false}` gives None.
6. Rename `test_an_orca_read_back_that_fails_is_a_failed_row_when_orca_listed_the_worktree` only if its name now misleads. Leave its assertions as they are.
7. Run `uv run pytest tests/worktree_cleanup -q` and `make lint`. Both must pass, and the order test at attempt-2.diff:431-458 must still show exactly one Orca call. Only throwaway repositories and the fake runner are used. Never run the script with `--apply`, and never add a force flag, `-D`, a deletion step, `git worktree prune` or a remote branch delete.
differs-by: the read back reads and judges the `orca worktree list` reply for every worktree, including one Orca had no row for before the removal, and a failed or unreadable reply is a failed row in both cases. Before, both cases counted as success when Orca had no row.
