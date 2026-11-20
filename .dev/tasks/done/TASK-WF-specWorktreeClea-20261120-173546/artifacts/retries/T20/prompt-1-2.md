0512af4cded2c73ae5ba5b25a0fd5e78358ed7cd
Review one task for spec compliance.

Task brief: ## Task 20: Capture the dry run of the real workspace and compare the counts

Depends on: Task 12, Task 13, Task 17, Task 18, Task 19

Run the finished script against this workspace as a dry run only: `uv run --no-project python scripts/worktree_cleanup.py list` and `uv run --no-project python scripts/worktree_cleanup.py prune --out ./artifacts/dry-run` (never `--apply`; the output folder is inside this package, not inside any worktree being judged; the script's own worktree is on the name list as "this is where the script runs"). Save the printed table and the `prune-<UTC timestamp>.md` and `.json` under `./artifacts/dry-run/` and write `./artifacts/dry-run-report.md` with: the command lines used, that `--apply` was never passed, the count of non-main worktrees of the IronClaude repo from `git worktree list --porcelain` against the number of IronClaude rows in the table, the count of rows with "in Orca" yes against the Orca list count read by the script (this session's launch guard may block typing an Orca command directly; if it does, record that and compare only through the script's own JSON), and the rows marked `removable` listed by folder and reason with a note on how they compare with the 13 of source section 2 as of the day (UNVERIFIED differences are expected and recorded as such, not forced to match). Confirm in the report that a worktree with a commit after its pull request's head, one whose issue is open and one with an ignored environment file (whichever the real data holds, else say none exists) are kept with the right reason, and that a worktree with only an open Orca terminal shows "its Orca terminals will be closed first" if one exists.

Acceptance criteria:
- `./artifacts/dry-run-report.md` exists and states that only `list` and `prune` without `--apply` were run, and the recorded command list in the `.json` output contains no removal, no terminal close, no archive and no push.
- The report gives the git count and the table count for the IronClaude repo, with any difference explained or marked UNVERIFIED.
- Every worktree of the real workspace is still present after the run (`git worktree list --porcelain` has the same entries before and after).
- No real worktree, file or Orca object was removed, moved, cleared, created or switched on to produce the report.
- The report records the results of the regression gate of source section 9 run on the finished change: the full test suite (`uv run pytest`), `make lint`, `make verify-sync`, and a scan of every new file for em and en dashes; any failure is stated, not hidden.

AC ids (in source order): T20.AC1, T20.AC2, T20.AC3, T20.AC4, T20.AC5
Global constraints: ## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.
- The pull request for this change is opened by the finishing step of the run, `/sc:pr-submit --monitor 3` (source section 15, step 7), after the last task; no task of this plan opens it.
- Corrections the implementer made to this plan before the first task started, from the advisory reflect review of the plan (the list is in `./artifacts/plan-corrections.md`): Task 1 (the item 1 fallback, the open pull request proof, item 7), Task 2 (a positive allowlist runner and its own first tests), Tasks 3 to 5 (their own tests, so no check waits for a later task), Task 7 (shared fixtures only), Tasks 11 and 12 (Orca read back, the command list in the JSON), Task 14 (the write-verb classification), Task 19 (15 rows), Task 20 (dependencies).
Start sha: 0512af4cded2c73ae5ba5b25a0fd5e78358ed7cd
Diff against the start snapshot: 
===== new file: .dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/dry-run-report.md =====
# Dry run of the finished script in the real workspace (Task 20)

Run on 2026-11-20 (UTC) from the issue-687 worktree of the IronClaude repo. Nothing in any worktree, in Orca or on GitHub was changed. The one write outside the output folder is the `git fetch` that the installed landed check runs on its own inside the real repos (it updates `FETCH_HEAD` and fetched objects there; see "Safety evidence").

## What was run

Only `list` and `prune`, both without `--apply`. `--apply` was never passed, to any verb, in any run.

```text
uv run --no-project python scripts/worktree_cleanup.py list
uv run --no-project python scripts/worktree_cleanup.py prune --out /tmp/worktree-cleanup-dry-run
```

One deviation from the plan, on purpose: the plan names an output folder inside this package. The package sits inside the issue-687 worktree, and the script (correctly) refuses an `--out` inside any worktree, so the output went to `/tmp/worktree-cleanup-dry-run` and the files were copied into `./artifacts/dry-run/` afterwards. A third, read only run (`whatif-driver.py`) called `list` with a fake empty process table, to show what rules 7 and 8 say about the worktrees that rule 6 held back (see "Findings").

Two real runs were made. The first (`./artifacts/dry-run/first-run-before-landed-fix/`) found a defect in the script, fixed afterwards; the second (`./artifacts/dry-run/`) ran on the fixed script. Both exited 69 (a lookup failed); the table still showed what happened.

## Findings of the run itself

1. **A real defect, fixed.** The first run kept every worktree whose pull request had merged with "landed check said UNKNOWN" (25 rows, exit 69). The installed landed check prints one line, the token and then key=value fields (`MERGED pr=301 by=... match=same url=...`), and the script accepted only a line that was exactly the token. My unit tests had used the bare token, so they passed. The script now reads the first word of the line, and the tests now use the real line shapes (`test_facts.py`). I ran the check by hand on pull requests 301, 700 and 410 to confirm the real output before changing anything. The second run shows no UNKNOWN row.
2. **Open question for the owner: every worktree that reaches rule 6 is kept, and the run exits 69.** The process scan found one process whose working folder it cannot read: pid 352, `chrome-sandbox` of `/opt/Orca/orca-ide --type=zygote` (Orca's own Electron sandbox helper). It runs as this user, has no capabilities and its `/proc/352/cwd` gives "permission denied". The specification (source section 11, item 4) says an unreadable entry of another user is noted and ignored, and any other error keeps everything, so the script keeps everything: 17 rows say "in use: the process scan failed (pid 352: permission denied for its own user), so everything is kept". While Orca runs, this process always exists, so with the rule as written no worktree can be removed in a workspace that runs Orca. This was not changed: loosening a safety rule is the owner's decision. The what-if run (empty process table, NOT a real answer) shows what would be removable: 5 rows, all in the Coder repo (`coder-agent-layout`, `coder-ccsession-access`, `coder-ccsession-orca`, `coder-orca-port`, `coder-tier-roles`).

## Counts

| Check | Git | Table | Result |
|---|---|---|---|
| IronClaude non-main worktrees | 37 (`git worktree list --porcelain`, 38 with the main checkout) | 37 non-main rows (38 rows) | equal |
| Coder | 14 | 14 | equal |
| IronFlow | 4 | 4 | equal |
| IronOrca | 2 | 2 | equal |
| Financials, GFxAI, IronOrchestrator, run-evidence | 0 each | main checkout only (run-evidence is not one of our listed repos) | equal |

Table rows in total: 64 (7 main checkouts and 57 linked worktrees). 13 rows are kept at rule 1: the 7 main checkouts, 5 detached HEADs and the folder the script runs in. The source section 2 count of 53 non-main worktrees was taken earlier on 2026-11-20; the git count now is 57 (37 + 14 + 4 + 2), so worktrees were added since. UNVERIFIED which ones.

"in Orca" yes: 36 rows (IronClaude 22, IronFlow 5, IronOrca 3, Coder 3, and one each for Financials, GFxAI and IronOrchestrator). That is the number of table rows matched to a row of the script's one `orca worktree ps` read; the script keeps no separate count of that reply, so this is not an independent second count. I did not type an Orca command by hand, because this session's launch guard blocks Orca commands typed in Bash, so the comparison is only through the script's own output. Source section 2 recorded 26 Orca-listed worktrees earlier the same day; the difference of 10 is UNVERIFIED (new worktrees, or the earlier figure counted differently).

## Rows marked removable

None in the real run (a consequence of finding 2). In the what-if run, 5 rows (listed in finding 2), each a merged pull request, nothing added after it, issues closed, idle 23 to 27 days, none listed in Orca. The 13 removable worktrees of source section 2 cannot be matched: that list is a day old, most of those worktrees now fall under rule 4 (issue 655 is open), rule 3 or rule 7, and the real run keeps everything at rule 6 anyway. The differences are UNVERIFIED and are not forced to match.

## The cases the plan asks to confirm (real data)

| Case | Real data | Row and reason |
|---|---|---|
| A commit after the pull request's head | one | `ic6-orchestrator`: "27 commits after the pull request" (rule 3) |
| An issue that is open | five | `rollback-655`, `issue-655-pr-c`, `issue-655-pr-d`, `issue-655-spec-pr` ("issue #655 is open") and `coder-orca-from-fork` of the Coder repo ("issue #373 is open") (rule 4) |
| Ignored local state | two | `ccsession-worktree-list` ("ignored local state: .serena/...") and `issue-668-build-p3` (".cache/uv/...") (rule 5). No worktree that reaches rule 5 holds an ignored `.env` file as such; rows kept at rules 1 to 4 are never checked for ignored files |
| Only an open Orca terminal, so "its Orca terminals will be closed first" | none exists | no removable row has an Orca terminal open (the 5 what-if rows are not listed in Orca), so the text did not appear |

## Safety evidence

- The recorded command list in the `.json` has 566 commands: `gh pr view`, `gh pr list`, `gh issue view`, `git status`, `git rev-parse`, `git remote get-url`, `git log`, `git worktree list`, `git merge-base`, `git rev-list`, `orca reference list`, `orca worktree ps`, `orca repo list` and the landed check. A search of it for a push, a terminal close, a worktree removal, `xargs`, `git clean`, a branch delete, `--force` and `rm` found none. No archive step ran (no clone, no evidence write).
- `git worktree list --porcelain` for this repo and for every repo directly under `~/workspaces` was identical before and after (`worktrees-before.txt`, `worktrees-after.txt`, `compare.txt`).
- Nothing in Orca was created, run, switched on, closed or removed. The only files the script wrote were the two `prune-<UTC stamp>` files under `/tmp/worktree-cleanup-dry-run`, outside every worktree (a dry run takes no lock, so no lock file exists there).
- The 25 `branch-landed.sh` entries in the command list are the landed check. That script runs a `git fetch` of the base branch and of `refs/pull/<N>/head` in the repo's main checkout (so it writes `FETCH_HEAD` and fetched objects inside the real Coder and IronClaude repos); that fetch is done by the script itself, so it is not a separate entry in the recorded list. It changes no worktree, branch or file of a worktree.

## The regression gate (source section 9), on the finished change

| Gate | Result |
|---|---|
| `uv run pytest` (whole suite) | 24072 passed, 69 skipped, 10 failed, in 27 minutes (`gate/pytest.txt`). The 10 failures are in two files this change does not touch, and neither mentions the worktree cleanup. Two (`tests/cli/eval/test_claude_process_adapter.py`) fail because `ruff` is not importable as a module in this `.venv` (`python -m ruff` finds none; run alone again: 2 failed, 11 passed, `gate/pytest-adapter-alone.txt`). Eight (`tests/unit/test_ccsession_tag.py`) depend on the machine: they failed in the full run and in a second run of the file alone (8 failed, 479 passed, `gate/pytest-ccsession-alone.txt`; the failure text is "Shim already running on 127.0.0.1:4555 (reusing)" followed by a connection error, which is a local service this session does not control), and they passed in an earlier run of the file alone (487 passed, output not saved) and when one of them was run by itself just now. They are not caused by this change, but I did not run the base commit to prove it. The full run took place before two small later edits (the command heading and two test names); the folders those edits touch were run again afterwards: 1924 passed (`gate/pytest-after-edits.txt`: `tests/commands`, the worker contract test, `tests/core`, `tests/recommend` and `tests/worktree_cleanup`). |
| `make lint` | First run failed in `lint-architecture` (Check 1): my command file had a `## Activation` heading, and that check then wants a skill folder. The heading is now `## What it runs` (a test pins it). Second run: exit 0, all checks passed (`gate/lint.txt`, `gate/lint2.txt`). |
| `make verify-sync` | "All components in sync." |
| Em and en dash scan of every new file and of the added lines of changed files | 0 in each |

## Not done, on purpose

- The script was never run with `--apply`, and no real worktree, file or Orca object was removed, moved, cleared or created.
- The change to the `IronbellyOrg/run-evidence` repo (`./artifacts/run-evidence-pointer.md`) is text only and not applied.


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/dry-run-report.md b/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/dry-run-report.md
index f70f86ec3..8ea0dcc0f 100644
--- a/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/dry-run-report.md
+++ b/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/dry-run-report.md
@@ -1,6 +1,6 @@
 # Dry run of the finished script in the real workspace (Task 20)
 
-Run on 2026-11-20 (UTC) from the issue-687 worktree of the IronClaude repo. Only reads were made.
+Run on 2026-11-20 (UTC) from the issue-687 worktree of the IronClaude repo. Nothing in any worktree, in Orca or on GitHub was changed. The one write outside the output folder is the `git fetch` that the installed landed check runs on its own inside the real repos (it updates `FETCH_HEAD` and fetched objects there; see "Safety evidence").
 
 ## What was run
 
@@ -32,7 +32,7 @@ Two real runs were made. The first (`./artifacts/dry-run/first-run-before-landed
 
 Table rows in total: 64 (7 main checkouts and 57 linked worktrees). 13 rows are kept at rule 1: the 7 main checkouts, 5 detached HEADs and the folder the script runs in. The source section 2 count of 53 non-main worktrees was taken earlier on 2026-11-20; the git count now is 57 (37 + 14 + 4 + 2), so worktrees were added since. UNVERIFIED which ones.
 
-"in Orca" yes: 36 rows (IronClaude 22, IronFlow 5, IronOrca 3, Coder 3, and one each for Financials, GFxAI and IronOrchestrator). That is the number of worktrees the script's one read of Orca's worktree list matched, so the table and the script's Orca list agree by construction. I did not type an Orca command by hand, because this session's launch guard blocks Orca commands typed in Bash, so the comparison is only through the script's own output. Source section 2 recorded 26 Orca-listed worktrees earlier the same day; the difference of 10 is UNVERIFIED (new worktrees, or the earlier figure counted differently).
+"in Orca" yes: 36 rows (IronClaude 22, IronFlow 5, IronOrca 3, Coder 3, and one each for Financials, GFxAI and IronOrchestrator). That is the number of table rows matched to a row of the script's one `orca worktree ps` read; the script keeps no separate count of that reply, so this is not an independent second count. I did not type an Orca command by hand, because this session's launch guard blocks Orca commands typed in Bash, so the comparison is only through the script's own output. Source section 2 recorded 26 Orca-listed worktrees earlier the same day; the difference of 10 is UNVERIFIED (new worktrees, or the earlier figure counted differently).
 
 ## Rows marked removable
 
@@ -43,22 +43,23 @@ None in the real run (a consequence of finding 2). In the what-if run, 5 rows (l
 | Case | Real data | Row and reason |
 |---|---|---|
 | A commit after the pull request's head | one | `ic6-orchestrator`: "27 commits after the pull request" (rule 3) |
-| An issue that is open | five | `rollback-655`, `issue-655-pr-c`, `issue-655-pr-d`, `issue-655-spec-pr` and one more: "issue #655 is open" (rule 4) |
-| Ignored local state | two | `ccsession-worktree-list` ("ignored local state: .serena/...") and `issue-668-build-p3` (".cache/uv/...") (rule 5). No worktree holds an ignored `.env` file as such |
+| An issue that is open | five | `rollback-655`, `issue-655-pr-c`, `issue-655-pr-d`, `issue-655-spec-pr` ("issue #655 is open") and `coder-orca-from-fork` of the Coder repo ("issue #373 is open") (rule 4) |
+| Ignored local state | two | `ccsession-worktree-list` ("ignored local state: .serena/...") and `issue-668-build-p3` (".cache/uv/...") (rule 5). No worktree that reaches rule 5 holds an ignored `.env` file as such; rows kept at rules 1 to 4 are never checked for ignored files |
 | Only an open Orca terminal, so "its Orca terminals will be closed first" | none exists | no removable row has an Orca terminal open (the 5 what-if rows are not listed in Orca), so the text did not appear |
 
 ## Safety evidence
 
 - The recorded command list in the `.json` has 566 commands: `gh pr view`, `gh pr list`, `gh issue view`, `git status`, `git rev-parse`, `git remote get-url`, `git log`, `git worktree list`, `git merge-base`, `git rev-list`, `orca reference list`, `orca worktree ps`, `orca repo list` and the landed check. A search of it for a push, a terminal close, a worktree removal, `xargs`, `git clean`, a branch delete, `--force` and `rm` found none. No archive step ran (no clone, no evidence write).
 - `git worktree list --porcelain` for this repo and for every repo directly under `~/workspaces` was identical before and after (`worktrees-before.txt`, `worktrees-after.txt`, `compare.txt`).
-- Nothing in Orca was created, run, switched on, closed or removed. The only files written were the two `prune-<UTC stamp>` files and the lock folder under `/tmp/worktree-cleanup-dry-run`, outside every worktree.
+- Nothing in Orca was created, run, switched on, closed or removed. The only files the script wrote were the two `prune-<UTC stamp>` files under `/tmp/worktree-cleanup-dry-run`, outside every worktree (a dry run takes no lock, so no lock file exists there).
+- The 25 `branch-landed.sh` entries in the command list are the landed check. That script runs a `git fetch` of the base branch and of `refs/pull/<N>/head` in the repo's main checkout (so it writes `FETCH_HEAD` and fetched objects inside the real Coder and IronClaude repos); that fetch is done by the script itself, so it is not a separate entry in the recorded list. It changes no worktree, branch or file of a worktree.
 
 ## The regression gate (source section 9), on the finished change
 
 | Gate | Result |
 |---|---|
-| `uv run pytest` (whole suite) | 24072 passed, 69 skipped, 10 failed, in 27 minutes. The 10 failures are in two files this change does not touch. Two (`tests/cli/eval/test_claude_process_adapter.py`) fail because `ruff` is not importable as a module in this `.venv` (`python -m ruff` finds none). Eight (`tests/unit/test_ccsession_tag.py`) pass when that file is run alone (487 passed), so they failed only under the load of the full run (terminal and Ctrl-C timing). The full run took place before two small later edits (the command heading below and two test names); the folders they touch were run again afterwards: 1924 passed, then `tests/worktree_cleanup` and `tests/commands` 946 passed. |
-| `make lint` | First run failed in `lint-architecture` (Check 1): my command file had a `## Activation` heading, and that check then wants a skill folder. The heading is now `## What it runs` (a test pins it). Second run: exit 0, all checks passed. |
+| `uv run pytest` (whole suite) | 24072 passed, 69 skipped, 10 failed, in 27 minutes (`gate/pytest.txt`). The 10 failures are in two files this change does not touch, and neither mentions the worktree cleanup. Two (`tests/cli/eval/test_claude_process_adapter.py`) fail because `ruff` is not importable as a module in this `.venv` (`python -m ruff` finds none; run alone again: 2 failed, 11 passed, `gate/pytest-adapter-alone.txt`). Eight (`tests/unit/test_ccsession_tag.py`) depend on the machine: they failed in the full run and in a second run of the file alone (8 failed, 479 passed, `gate/pytest-ccsession-alone.txt`; the failure text is "Shim already running on 127.0.0.1:4555 (reusing)" followed by a connection error, which is a local service this session does not control), and they passed in an earlier run of the file alone (487 passed, output not saved) and when one of them was run by itself just now. They are not caused by this change, but I did not run the base commit to prove it. The full run took place before two small later edits (the command heading and two test names); the folders those edits touch were run again afterwards: 1924 passed (`gate/pytest-after-edits.txt`: `tests/commands`, the worker contract test, `tests/core`, `tests/recommend` and `tests/worktree_cleanup`). |
+| `make lint` | First run failed in `lint-architecture` (Check 1): my command file had a `## Activation` heading, and that check then wants a skill folder. The heading is now `## What it runs` (a test pins it). Second run: exit 0, all checks passed (`gate/lint.txt`, `gate/lint2.txt`). |
 | `make verify-sync` | "All components in sync." |
 | Em and en dash scan of every new file and of the added lines of changed files | 0 in each |
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=scope at=artifacts/dry-run-report.md:36 anchor="Only reads were made" chk=n,y,n,n family=safety-evidence-wording fix=say that the landed check runs a git fetch inside the real repos first=A1 origin=new: the report said only reads were made, but the landed check writes FETCH_HEAD and fetched objects in the real repos.
F1.3 sev=blocking trigger=B1 ac=T20.AC5 at=artifacts/dry-run-report.md:93 anchor="the regression gate of source section 9 run on the finished change" chk=y,n,n,n family=gate-evidence fix=save the outputs of the reruns and cite them first=A1 origin=new: the reruns after the last edits (1924, 946, 487) had no saved evidence.

Saved-probe re-check hit locations (may be empty): 3:Run on 2026-11-20 (UTC) from the issue-687 worktree of the IronClaude repo. Nothing in any worktree, in Orca or on GitHub was changed. The one write outside the output folder is the `git fetch` that the installed landed check runs on its own inside the real repos (it updates `FETCH_HEAD` and fetched objects there; see "Safety evidence").
35:"in Orca" yes: 36 rows (IronClaude 22, IronFlow 5, IronOrca 3, Coder 3, and one each for Financials, GFxAI and IronOrchestrator). That is the number of table rows matched to a row of the script's one `orca worktree ps` read; the script keeps no separate count of that reply, so this is not an independent second count. I did not type an Orca command by hand, because this session's launch guard blocks Orca commands typed in Bash, so the comparison is only through the script's own output. Source section 2 recorded 26 Orca-listed worktrees earlier the same day; the difference of 10 is UNVERIFIED (new worktrees, or the earlier figure counted differently).
46:| An issue that is open | five | `rollback-655`, `issue-655-pr-c`, `issue-655-pr-d`, `issue-655-spec-pr` ("issue #655 is open") and `coder-orca-from-fork` of the Coder repo ("issue #373 is open") (rule 4) |
54:- Nothing in Orca was created, run, switched on, closed or removed. The only files the script wrote were the two `prune-<UTC stamp>` files under `/tmp/worktree-cleanup-dry-run`, outside every worktree (a dry run takes no lock, so no lock file exists there).
55:- The 25 `branch-landed.sh` entries in the command list are the landed check. That script runs a `git fetch` of the base branch and of `refs/pull/<N>/head` in the repo's main checkout (so it writes `FETCH_HEAD` and fetched objects inside the real Coder and IronClaude repos); that fetch is done by the script itself, so it is not a separate entry in the recorded list. It changes no worktree, branch or file of a worktree.
61:| `uv run pytest` (whole suite) | 24072 passed, 69 skipped, 10 failed, in 27 minutes (`gate/pytest.txt`). The 10 failures are in two files this change does not touch, and neither mentions the worktree cleanup. Two (`tests/cli/eval/test_claude_process_adapter.py`) fail because `ruff` is not importable as a module in this `.venv` (`python -m ruff` finds none; run alone again: 2 failed, 11 passed, `gate/pytest-adapter-alone.txt`). Eight (`tests/unit/test_ccsession_tag.py`) depend on the machine: they failed in the full run and in a second run of the file alone (8 failed, 479 passed, `gate/pytest-ccsession-alone.txt`; the failure text is "Shim already running on 127.0.0.1:4555 (reusing)" followed by a connection error, which is a local service this session does not control), and they passed in an earlier run of the file alone (487 passed, output not saved) and when one of them was run by itself just now. They are not caused by this change, but I did not run the base commit to prove it. The full run took place before two small later edits (the command heading and two test names); the folders those edits touch were run again afterwards: 1924 passed (`gate/pytest-after-edits.txt`: `tests/commands`, the worker contract test, `tests/core`, `tests/recommend` and `tests/worktree_cleanup`). |
62:| `make lint` | First run failed in `lint-architecture` (Check 1): my command file had a `## Activation` heading, and that check then wants a skill folder. The heading is now `## What it runs` (a test pins it). Second run: exit 0, all checks passed (`gate/lint.txt`, `gate/lint2.txt`). |


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
