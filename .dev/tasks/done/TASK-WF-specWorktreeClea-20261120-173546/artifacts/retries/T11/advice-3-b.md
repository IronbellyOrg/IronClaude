model: opus (top rung; tier unknown) family: claude rung: top  family-fallback: no verified spawn path for a GPT T1 model  entry: escalation 1, adviser B
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T11.AC1 | Not missed. The review accepted it (review-2.md:3). The order is set in attempt-2.diff:101-206 and tested at attempt-2.diff:440-445 and attempt-2.diff:465-474. | Keep the pipeline steps as they are. Only the Orca read back changes, and it changes what happens after the last read, not the order. The orca list stays the last recorded command, and the non-Orca test at attempt-2.diff:447-448 still expects that one Orca call. |
| T11.AC2 | Not missed. Accepted at review-2.md:4. The clear is at attempt-2.diff:167-181 and the refusal test at attempt-2.diff:772-782. | No change. New tests add no clear command. |
| T11.AC3 | Not missed. Accepted at review-2.md:5. The scan of forbidden commands is at attempt-2.diff:490-516. | No change. New tests must use only the commands already allowed: `git worktree list --porcelain` and `orca worktree list --json`. |
| T11.AC4 | Not missed. Accepted at review-2.md:6. The guard is at attempt-2.diff:90-94 and the test at attempt-2.diff:522-543. | No change. |
| T11.AC5 | The read back runs `orca worktree list` for a worktree that Orca did not list before, then ignores the reply (review-2.md:7-8, attempt-2.diff:245-251). It ignores a failed exit too: attempt-2.diff:247-248 returns None when `orca` is None. The same fault hides in `orca_lists` (attempt-2.diff:264-280). It searches every key at every depth, so an Orca error reply (`"ok": false`) or a reply with no worktrees list counts as "not listed". The unit test even fixes `{}` as False (attempt-2.diff:755-756). An empty id would also match any row with an empty `id` (attempt-2.diff:274-275). Every read-back test uses the Orca fixture (attempt-2.diff:658-681, 735-743), so the `git worktree remove` path was never tested. | Make the Orca read back the same whether or not Orca listed the worktree before. A failed exit, an Orca error, an unreadable reply or a reply with no worktrees list is a failed row. A row matching the worktree's path, or its non-empty id, is the failed row "removed in git but still listed in Orca". |

differs-by: The Orca read back no longer depends on whether Orca listed the worktree before. Every reply goes through the script's existing strict Orca reply reader (`_orca_rows(text, "worktrees")`) instead of a free search of the JSON, so any failed, error or shapeless reply becomes a failed read back instead of "not listed".

Steps:
1. In `/home/coder/workspaces/worktrees/IronClaude/issue-687/scripts/worktree_cleanup.py`, rewrite `orca_lists(text, path, worktree_id="")`:
   - Call the existing helper `_orca_rows(text, "worktrees")`. If it returns a string (not JSON, `"ok": false`, or no worktrees list), return None.
   - Otherwise, for each row, return True when the row's `path` is a non-empty string whose `os.path.normpath` equals the wanted path's normpath.
   - Also return True when `worktree_id` is non-empty and the row's `worktreeId` is a non-empty string equal to it.
   - Stop searching nested keys and the bare `id` key. Return False otherwise.
   - Update the docstring to say an error or shapeless reply is "unreadable" (None).
2. In `_read_back`, remove both `orca is None` branches (the conditional return at the old lines 246-249 and the early `return None` at 250-251):
   - A non-zero exit of `orca worktree list --json` always returns "read back failed: orca worktree list failed".
   - Then call `still = orca_lists(seen.stdout, wt.path, orca.worktree_id if orca is not None else "")`.
   - None returns "read back failed: the orca worktree list could not be read". True returns "removed in git but still listed in Orca".
3. Close the same gap on the git side of `_read_back`. git always lists the main checkout, so if `parse_worktree_porcelain` returns an empty list on an exit of 0, return "read back failed: the git worktree list could not be read". Do not treat an empty parse as "gone".
4. Leave steps 1 to 6 of `remove_worktree`, the runner allowlist and every accepted test as they are.
5. In `/home/coder/workspaces/worktrees/IronClaude/issue-687/tests/worktree_cleanup/test_removal.py`, add a test on the plain `setup` fixture, where Orca did not list the worktree:
   - Set the reply for `("worktree", "list")` to `{"ok": true, "result": {"worktrees": [{"worktreeId": "x", "path": "<the worktree path>"}]}}`.
   - Assert `(status, reason) == ("failed", "removed in git but still listed in Orca")` and that the folder is gone.
   - Assert that the removal was the git command `worktree remove` and that no `orca worktree rm` was recorded.
6. Add a parametrized test on the same `setup` fixture for the other failed replies:
   - exit 1 gives "read back failed: orca worktree list failed"
   - `<html>` gives "read back failed: the orca worktree list could not be read"
   - `{"ok": false, "error": "x"}` gives the same "could not be read" reason
   - `{}` gives the same "could not be read" reason
7. Update `test_orca_lists_compares_paths_and_ids_for_equality`:
   - `{}` now gives None, not False.
   - Add `{"ok": false}` gives None.
   - `[]` and `{"result": {"worktrees": []}}` still give False.
   - A row with `"worktreeId": ""` and another path, checked with an empty wanted id, gives False.
   - Keep the sibling and trailing slash cases.
8. Run `uv run pytest tests/worktree_cleanup -q` and `make lint` and confirm both pass. The tests use only throwaway repositories under `tmp_path` and fake `orca` replies. Never run the script with `--apply`, never point it at a real worktree, and use no `--force`, `git branch -D`, `rm`, `git worktree prune` or remote branch delete.
