model: opus (top rung; tier unknown) family: claude rung: top  entry: escalation 1, adviser A
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T12.AC1 | It was not missed. The review marks it met (review-2.md:6). `list` and `prune` with no `--apply` record no removal command, and only removable rows reach the removal step (attempt-2.diff:417-427, attempt-2.diff:792-817, attempt-2.diff:879-916). | Rebuild it exactly as in attempt-2.diff. No new behaviour. |
| T12.AC2 | It was not missed. The review marks it met (review-2.md:7). Each repo gets its own lock file, taken with a non-blocking `flock` and never deleted (attempt-2.diff:268-303), and a second run says "nothing more to do" (attempt-2.diff:368-369, attempt-2.diff:933-953). | Rebuild it exactly as in attempt-2.diff. |
| T12.AC3 | The review says this AC is unmet (review-2.md:8). The finding is review-2.md:10: in the second check after the terminals close, `remove_worktree` returns status `kept` when it cannot read a fact. That covers git status giving None, the process scan failing, and an unknown relation to the pull request. `_apply_removal` passes that status straight through (attempt-2.diff:333-337). `_summarize` counts a row as failed only when its decision is `failed` or its decision from the eight rules is marked unread (attempt-2.diff:343-348). So `prune --apply` exits 0 with failed 0. `retire` turns `kept` into 64 (attempt-2.diff:516-518). An existing Task 11 test fixes the wrong status in place: tests/worktree_cleanup/test_removal.py:319 asserts `kept` for a failed process scan. | Keep every fix the review accepted (review-2.md:2-5). Then, inside `remove_worktree`, make an unreadable fact in the second check return `RemovalResult("failed", ...)`. A real change still returns `kept`. Update test_removal.py:319 and add tests at the verb level. |
| T12.AC4 | It was not missed. The review marks it met (review-2.md:9). Both prune files go under `--out` (attempt-2.diff:431-445). The JSON holds `rows` and `commands` (attempt-2.diff:94-107). An `--out` inside a worktree is refused (attempt-2.diff:398-401). | Rebuild it exactly as in attempt-2.diff. |

differs-by: the second check inside `remove_worktree` sorts what it finds into two groups. A fact it could not read gives status `failed` (exit 69). A fact it read and found changed gives `kept`. The earlier attempt marked unreadable facts only in the verdict of the eight rules and passed every second-check stop through as `kept`.

Steps:
1. Rebuild the whole attempt from attempt-2.diff as the base. The simplest way is to apply it with `git apply`; check first with `git apply --check`. The diff covers:
   - `import time`
   - `RuleInputs.orca_known`, `UNREAD_PREFIXES`, `Decision.unread`, the `orca_known` check in `_rule8`, and the unread flag in `decide`
   - the "n/a" cells in `table_row` and `render_json` with `commands` and `summary`
   - the archive help text that says patch-and-bundle is not built
   - the whole "the four verbs" section: `Entry`, `Found`, `_current_repo`, `find_worktrees`, `assess`, `_assess_all`, `resolve_selector`, `RepoLocks`, `_command_log`, `_apply_removal`, `_summarize`, `_summary_text`, `_inside_any`, `_run_verb`, `_one_worktree`, and the new `main`
   - the test changes in test_rules.py, test_runner.py and the new test_verbs.py

   This keeps the four accepted fixes: the unreadable Orca list, lookup failures as 69, the `--out` checks for every verb, and the OSError handling.
2. In `scripts/worktree_cleanup.py`, function `remove_worktree`, change only step 3 ("check again"). Run the checks in this order:
   1. Right after `again = gather_facts(...)`: if `again.present` is False, return `RemovalResult("failed", "re-check failed: the folder could not be read after the terminals were closed", tuple(steps), verified=verified)`. If `again.state is None`, return `failed` with reason "re-check failed: git status could not be read after the terminals were closed". If `again.head is None`, return `failed` with reason "re-check failed: HEAD could not be read after the terminals were closed".
   2. Saved files: if a file still exists but `_safe_sha` gives None, return `failed` with reason "re-check failed: a saved file could not be read". A saved file that is missing, or whose digest differs, is still a change.
   3. Next, keep the existing `changed` comparison (state, head, digests) returning `kept` with "changed since the terminals were closed". Drop the `again.state is None` term from it, because sub-step 1 now handles that.
   4. After `commits_after_pr`: if `after.relation == "unknown"`, return `failed` with reason `f"re-check failed: {after.reason}"`. Any relation other than `same` or `ancestor` still returns `kept` with "changed since the terminals were closed".
   5. If `scan.ok` is False, return `failed` and keep the current reason text, "in use: the process scan failed (...)".
   6. A process found inside still returns `kept`.
   7. Also, at the top of the function: if `first.decision != "removable"` and `first.unread` is True, return `RemovalResult("failed", first.reason)`; otherwise keep `kept`.

   Change nothing else in steps 1 to 7.
3. Leave `_apply_removal`, `_summarize` and `_one_worktree` as rebuilt. A `failed` status already becomes a failed row, is counted in "failed", and makes `prune` and `retire` exit 69 (attempt-2.diff:446, attempt-2.diff:518).
4. In tests/worktree_cleanup/test_removal.py, change line 319 to expect `done.status == "failed"`. Add unit tests in the same style, all on throwaway repos with fake replies:
   - Make `git status` fail only on its second call for the worktree path (match on `"status" in argv` and the cwd), expect `failed`, and assert no `xargs` was recorded.
   - Do the same with `git rev-parse HEAD` failing on its second call.
   - Monkeypatch `wc.scan_processes` to return `ProcScan(False, failure="x")` on its second call only, and expect `failed`.
   - Keep the existing tests that expect `kept` for a real change and for a process still inside.
5. In tests/worktree_cleanup/test_verbs.py, add one test for each of the three unreadable second-check cases. Use a worktree added with `world.add("plain", dev=False)`, so no save runs and the second check follows right after the first assessment. Fail only the second read for that worktree. Assert:
   - `world.run("prune", "--apply") == 69`
   - the output holds "failed 1"
   - the JSON row's decision is "failed"
   - the folder still exists
   - no `git worktree remove` or `xargs` command was recorded

   Then rebuild the world and assert `world.run("retire", "plain", "--apply") == 69`. Also add one control test: a real change made during the terminal close (as in the existing test_removal.py busy-terminal test) still gives "kept" and `prune --apply` exit 0.
6. Run `uv run pytest tests/worktree_cleanup -q` and `uv run ruff check scripts/worktree_cleanup.py tests/worktree_cleanup`. Only the tests run the script, on throwaway repos with fake `gh`, `git` and `orca`. Never run it with `--apply` against real worktrees. Never add `--force`, `git branch -D`, `rm`, `git worktree prune` or a remote branch delete. Write plain English with no em or en dashes, and no literal credentials.

Files involved:
- /home/coder/workspaces/worktrees/IronClaude/issue-687/scripts/worktree_cleanup.py
- /home/coder/workspaces/worktrees/IronClaude/issue-687/tests/worktree_cleanup/test_removal.py
- /home/coder/workspaces/worktrees/IronClaude/issue-687/tests/worktree_cleanup/test_verbs.py
- /home/coder/workspaces/worktrees/IronClaude/issue-687/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/retries/T12/attempt-2.diff
