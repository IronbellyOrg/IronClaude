model: opus (top rung; tier unknown) family: claude rung: top  family-fallback: no verified spawn path for a GPT T1 model  entry: escalation 1, adviser B
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T12.AC1 | Not missed. The review accepted it (review-2.md:6): under `prune --apply` only rows marked removable reach the removal (attempt-2.diff:417-427), and a dry `retire` stops before any removal (attempt-2.diff:511-513). | Rebuild this exactly as before. The only new thing is that the outcome of each row is also written to the run ledger (steps 4 and 5). |
| T12.AC2 | Not missed (review-2.md:7). The per-repo lock never deletes its file (attempt-2.diff:268-303). A lock held by another run keeps the row (attempt-2.diff:324-327) and the lock test proves it (attempt-2.diff:933-938). One weakness of the same kind sits nearby: the summary takes its kept groups only from the decision made before the removal (attempt-2.diff:353), so a row kept during the removal step ("another run holds the lock", "changed since the terminals were closed") never shows up as a kept group. Also, "nothing more to do" is printed even when rows failed (attempt-2.diff:368). | Keep the lock code as it is. Build the kept groups and the "nothing more to do" line from the ledger. Rows kept during the removal step form an "at removal" group. "nothing more to do" is printed only when removed, removable and failed are all 0. |
| T12.AC3 | `remove_worktree` returns `kept` when the re-check after the terminals close cannot read a fact (review-2.md:10). `_apply_removal` passes that status on unchanged (attempt-2.diff:335-337). The summary counts a row as failed only when its decision cell says "failed" or the earlier `Decision.unread` flag is set (attempt-2.diff:344-348), and that flag is False on every removable row. So `prune` exits 0 (attempt-2.diff:446) and `retire` turns `kept` into 64 (attempt-2.diff:516-518). An existing test pins the wrong status for a failed process scan (tests/worktree_cleanup/test_removal.py:319). The same problem also hides in four other places. (1) When `orca repo list` fails, the run falls back to the current repo and only prints a note (attempt-2.diff:173-174), which the exit code never reads. (2) `archive` and `retire` look at `found.failures` only when the selector matches nothing (attempt-2.diff:462-466). (3) argparse usage errors leave `parse_args` with exit 2, not 64 (attempt-2.diff:125, attempt-2.diff:529). (4) Unreadable rows are counted as failed and also listed in kept groups (attempt-2.diff:347, attempt-2.diff:353). | `remove_worktree` returns `failed` for every unreadable fact: in its own first `decide` and in the re-check. One run ledger decides the failed count and the exit code. The `orca repo list` fallback counts as a lookup failure. `archive` and `retire` exit 69 when any lookup in the run failed. argparse usage errors map to 64. Keep the four accepted fixes. |
| T12.AC4 | Not missed (review-2.md:9). `--out` is refused inside a worktree (attempt-2.diff:398-401). The folder is created before any removal (attempt-2.diff:407-412). Both files are written, and an OSError there gives 69 (attempt-2.diff:431-445). The JSON holds `rows`, `commands` and `summary` (attempt-2.diff:94-107, attempt-2.diff:306-310). | Rebuild it exactly as before. The JSON `summary` takes its counts from the ledger. |

differs-by: every row and run outcome goes into one run ledger (each row removed, kept, removable or failed, set by the step that ended it, plus run-level lookup failures), and the summary counts, kept groups and exit code are all computed from that ledger; `remove_worktree` itself returns `failed` for every unreadable re-check fact, instead of the summary reading only the pre-removal `Decision.unread` flag and passing `remove_worktree`'s `kept` through.

Steps:
1. Re-apply attempt-2.diff as the base: the script hunks (attempt-2.diff:5-549), the test_rules.py hunk (attempt-2.diff:556-597), the test_runner.py hunk (attempt-2.diff:606-624) and the new test_verbs.py (attempt-2.diff:633-1219). The four accepted fixes must survive without change:
   - the unreadable Orca list: `orca_known` and the rule 8 reason (attempt-2.diff:17-18, 47-49, 146, 186);
   - the unread lookup reasons: `UNREAD_PREFIXES` and `Decision.unread` (attempt-2.diff:21-40, 53-64), and a selector in a repo whose listing failed gives 69 (attempt-2.diff:465-466);
   - the output folder checks (attempt-2.diff:398-412);
   - the OSError handling (attempt-2.diff:284-291, 333-334, 440-445, 498-500).
2. In `remove_worktree` in scripts/worktree_cleanup.py (Task 11 code, which the attempt did not touch), split "could not read" from "changed" and return `RemovalResult("failed", ...)` for the first:
   - a. The first `decide` call: when the result is not removable, return `failed` if `first.unread`, otherwise `kept`.
   - b. At the re-check, return failed when `again.present` is False, when `again.state` is None, or when `again.head` is None while `facts.head` was not. Use a reason that starts "the re-check after the terminals were closed could not read" and names the fact.
   - c. Next, call `commits_after_pr`. Return failed when `after.relation == "unknown"`, or when it is "ahead" with `commits_after` None.
   - d. A saved file that still exists (`os.path.lexists`) but whose hash comes back None is failed. A saved file that is missing, or whose hash differs, counts as a change.
   - e. Only after a, b, c and d, keep the existing `kept` "changed since the terminals were closed" check, including the "ahead" relation.
   - f. A process scan that is not ok returns `failed` with the existing text "in use: the process scan failed (...)".
   - g. A process still inside stays `kept`.
3. In tests/worktree_cleanup/test_removal.py, change line 319 to expect `failed`. Add tests, each asserting `failed`, no `xargs` and no removal command, with the folder still there:
   - `git status` fails only after the terminal close reply has run (use the fake runner's git reply);
   - the HEAD comparison cannot be read after the close;
   - a saved file is unreadable at the re-check.
   The existing change tests at test_removal.py:282-305 must still pass with `kept`.
4. In `_run_verb`, build one ledger entry per row:
   - status `failed` when `decision.unread`, `removable` when removable, otherwise `kept`, with group `rule N`;
   - for rows passed through `_apply_removal`, its status, with group `at removal`.
   Rewrite `_summarize` to count removed, kept and failed from the ledger only. Kept still includes removable rows in a dry run, so the line at attempt-2.diff:1069 still holds. Take `first_reasons` only from entries with status `kept`. Print "nothing more to do" only when removed, removable and failed are all 0. Use the same numbers in the JSON `summary`.
5. Add a run-level `run_failures` list:
   - Start it from `found.failures`.
   - In `find_worktrees`, when `orca repo list` fails and the run falls back to the current repo, also append that lookup failure. Still print the note and still list the current repo.
   - Compute the exit code once: 69 when `run_failures` or any ledger entry is failed; otherwise 64 for a usage error or a non-removable `retire`; otherwise 0.
   - `--out` inside a worktree still returns 64 at once, before any work, as at attempt-2.diff:398-401.
   - For `archive` and `retire`, when the selector matches but `found.failures` is not empty, do the work as now and then return 69.
   - `archive` always prints its row. When the save is verified but the decision was unread at rule 6, 7 or 8, it still returns 69 after printing `VERIFIED`.
6. In `main`, wrap `parse_args` in a try. On `SystemExit`, return 0 when the code is 0 or None (this keeps `--help`) and `EXIT_USAGE` otherwise. Check that the `__main__` block passes `main()` to `sys.exit`.
7. Leave `_remove_branch` alone: source.md:96 says a branch that is kept is not an error.
8. Add tests in tests/worktree_cleanup/test_verbs.py, using only the throwaway World fixture:
   - `prune --apply` and `retire --apply` both exit 69 with "failed 1" when the re-check cannot read `git status`, and nothing is removed;
   - the same when the process scan fails at the re-check: the close reply breaks a fake proc root, as in `make_fake_proc` with `{43: "file"}`;
   - a real change made during the close is still kept: exit 0 for `prune`, 64 for `retire`, and the reason appears under an "at removal" group;
   - only `orca repo list` fails while `orca worktree ps` answers: exit 69, with the note and the fallback table;
   - an unreadable row is not listed in a kept group, and "nothing more to do" does not appear when failed is above 0;
   - `main(["retire"])`, `main(["bogus"])` and `main(["list", "--nope"])` all return 64, and `--help` still exits 0.
9. Run `uv run ruff check scripts/worktree_cleanup.py tests/worktree_cleanup` and `uv run pytest tests/worktree_cleanup -q`. The current base is 436 passed (extras-2.log:2). Fix any older test whose fixture lets `orca repo list` fail but expects 0. Never run the script with `--apply` against real worktrees, and add no `--force`, `-D`, `rm`, `git worktree prune` or remote branch delete anywhere.

Relevant files:
- /home/coder/workspaces/worktrees/IronClaude/issue-687/scripts/worktree_cleanup.py
- /home/coder/workspaces/worktrees/IronClaude/issue-687/tests/worktree_cleanup/test_removal.py
- /home/coder/workspaces/worktrees/IronClaude/issue-687/tests/worktree_cleanup/test_verbs.py
- /home/coder/workspaces/worktrees/IronClaude/issue-687/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/retries/T12/review-2.md
- /home/coder/workspaces/worktrees/IronClaude/issue-687/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/retries/T12/attempt-2.diff

| DONE | NEXT |
|---|---|
| Found the cause of F1.5 and four more spots with the same flaw, and wrote a rebuild plan that keeps the four accepted fixes | The executor rebuilds from steps 1 to 9 and reruns lint and the worktree_cleanup tests |
