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
