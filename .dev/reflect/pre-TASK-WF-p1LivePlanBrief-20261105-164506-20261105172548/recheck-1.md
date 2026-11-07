# Recheck 1 of plan revision 2 (adversarial)

Plan: `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md` (589 lines, working copy at HEAD `0b44374513780b69f59d9018c06cbf0b4af420ad`). Fix list: `post-fix-rechecks.md` in this folder (13 rows).

## 1. The 13 revision-2 fixes

| Row | Present | Plan lines | Result |
|---|---|---|---|
| 1 install comparison limited to `*.md` except `README.md` | yes | 60 | Correct. `src/superclaude/cli/install_commands.py:11` (`_EXCLUDE_FILES = {"README.md"}`) and `:40` (`glob("*.md")`) match the wording. The live run passes (section 2). |
| 2 clean-tree check scoped to `src plugins tests` | yes | 60 | Correct. Prints nothing live. The reason in parentheses matches the Worktree step at line 37. |
| 3 Task 23 find baseline and diff | yes | 543, 546 | Correct, and the AC names all three files. 325 tracked `return-contract.yaml` files today (`git ls-files`), so a baseline is needed. See M6. |
| 4 `>>>` `<<<` markers | yes | 52-53, 554, 558, 563 | Consistent. The gate (554) reads the text between the markers and tests for `NOT YET GIVEN`. The substitution (558) uses the same text without the markers. Lines 14, 30 and 51 agree. See M7. |
| 5 Task 25 AC wording | yes | 586 | "grant file" is gone from the ACs. The only remaining use is at line 14, which describes the snapshot and is correct. |
| 6 WC-9 cited for staging | yes | 407 | Correct. The static report line 29 says D-P1-5 covers only the skipped `--handoff implement`. Spec WC-9 says a worker "never runs `git add` (including `git add .dev/tasks`)". |
| 7 watcher listing | yes | 229, 453, 467 | Live run printed nothing (section 3). See M4 and M5. |
| 8 report-path compare with `realpath -m` | yes | 41 | Consistent with spec 7.2 step 3 ("its report path is the WC-4 contract path"). |
| 9 Task 1 retry reuses `live-run.json` | yes | 60 | Introduces B1 and M1. |
| 10 AC-1.8 parent check | yes | 556 | Can be checked: `orca worktree list --json` rows carry `parentWorktreeId`, and `orca worktree current --json` prints `result.worktree.id` = `de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1`. See M2 and M3. |
| 11 Task order bullet | yes | 54 | Consistent with the shared `check --run` inbox and the process listing. |
| 12 Task 25 states both commits | yes | 582 | Present. |
| 13 revision note | yes | 19 | Both cited `post-fix-rechecks.md` files exist. |

## 2. Task 1 checks run as written (read-only, from the repo root)

| Check | Result |
|---|---|
| `cmp` of 46 `src/superclaude/commands/*.md` (minus README.md) against `~/.claude/commands/sc/` | all exit 0 |
| skill paths from `git diff --name-only "$(git merge-base master HEAD)" HEAD -- src/superclaude/skills` (merge-base `4eb75698`) | 15 compared, all exit 0, none deleted |
| `cmp ~/.claude/WORKER-CONTRACT.md src/superclaude/core/WORKER-CONTRACT.md` | exit 0 |
| `git status --porcelain -- src plugins tests` | empty |
| `git merge-base --is-ancestor 7127c247... HEAD` | exit 0 |
| `git rev-parse HEAD` and `refs/heads/ironbelly/OrcaCLICommandRefactor-P1` | both `0b44374513780b69f59d9018c06cbf0b4af420ad`. Branch name is correct. |
| `git remote get-url origin` | `https://github.com/IronbellyOrg/IronClaude` |
| `ORCA_TERMINAL_HANDLE` | set (`term_558daf54-...`) |
| AC-C6 grep | `"nestedWorkerMaxDepth":1` only |
| `orca --version` | `1.4.245-aidev02.dfe1eb410300` |
| `orca status --json` | `runtime.state: ready` |
| `orca repo list --json` | lists `de550e99-fa3c-42e2-abfe-1d092771c759` |
| `--help` of all 15 listed verbs | all exit 0. Every flag and selector the procedure uses is present. `worktree create` shows `--parent-worktree <selector>` (with `active/current`, `path:` and `worktree:` selectors) and `--no-parent`. `task-create` shows `--task-title` and `--run`. |
| `claude --help` | shows `--max-budget-usd` and `--permission-mode` |

No Task 1 check fails on the current tree.

## 3. lc18 watcher listing

`ps -eo args | grep -e '--watch' | grep -v -e grep -e 'bash -c' -e shell-snapshots -e ps` printed nothing, so nothing spurious. Without the filter the raw listing showed only this session's own `/bin/bash -c source .../shell-snapshots/...` wrapper and `grep -e --watch`, and the filter removes both. The pipeline exits 1 when it prints nothing (`PIPESTATUS` = `0 0 1`). The Claude processes on this machine carry no prompt text in their argv (`--settings {...} --model ... --name ...`), so a worker's own process line should not match `--watch`.

## 4. Findings

| # | blocking/minor | plan:line | evidence | fix |
|---|---|---|---|---|
| B1 | blocking (applies when Task 1 is retried or resumed in a new terminal) | 60, 66, 28 | The row-9 rule reuses `live-run.json` but never rebinds the Run. A resumed coordinator runs in a new Orca terminal. Orca's own help gives `orchestration run-use --id <run_id>` as "Resume coordinating a Run", and the memory note `orca-coordinator-rebind-after-resume.md` (2026-11-04, issue #302) records that `worker-start` fails `consumer_fenced` until `run-use` is run. The plan never mentions `run-use` (grep finds no hit). On such a resume, the AC at line 66 ("`result.run.coordinator_handle` equal to the `ORCA_TERMINAL_HANDLE` recorded in `preflight.md`") cannot pass, because `preflight.md` is rewritten with the new handle while `live-run.json` keeps the old one. Every later `worker-start` would also fail, and line 29 would record each failure as step 1 FAIL. | On reuse, if `coordinator_handle` differs from `$ORCA_TERMINAL_HANDLE`, run `orca orchestration run-use --id <run_id> --json` and save the receipt to `./artifacts/run-use.json`. Apply the same rule at the start of any resumed live task (line 28). Add `orchestration run-use` to the help list. Change the AC at line 66 to accept either a matching handle or a `run-use` receipt that binds the current handle. |
| M1 | minor | 60 | The first sentence says "Before any other write, save `git status --porcelain` to `./artifacts/status-baseline.txt` and `orca worktree list --json` to `worktree-list-before.json`". The retry clause later in the same paragraph says "keep an existing `./artifacts/status-baseline.txt`". An executor that works in order overwrites the baseline before it reads the keep clause. No check fails, because the overwrite only loosens the line-67 and line-588 comparisons. | Move the retry clause to the start of Task 1 and cover both baseline files. |
| M2 | minor | 60, 65, 556 | Task 24 calls `orca worktree current --json` (line 556), but the Task 1 help list (line 60) omits `worktree current`. The AC at line 65 calls that list "every Orca verb this plan calls", which is then false. B1's `run-use` is also missing from the list. | Add `worktree current` (and `orchestration run-use`) to the line-60 list. |
| M3 | minor | 556, 571-574 | The row-10 parent check writes `lc22-parent-check.txt`, but no Task 24 AC names it. | Add an AC: when the check ran, `lc22-parent-check.txt` shows the new worktree's `parentWorktreeId` and the feature worktree id, and they are equal (or the result records FAIL and no dispatch). |
| M4 | minor | 453 | `grep -v -e ps` drops every line that contains the substring "ps" (`https`, `apps`, `steps`, `snapshots`). `-e 'bash -c'` also drops a worker-started watcher whose only process is a `bash -c` wrapper. Both cause false negatives. An empty listing, which is the passing case, exits 1. | Use `grep -v -w ps` (or `-e '^ps '`). State that exit 1 with empty output is the expected result. |
| M5 | minor | 229, 242-245 | lc08's extra refers to "the process listing taken by the lc18 rule below" but names no before or after file for lc08, and its ACs list none. | Name `lc08-pgrep-before.txt` and `lc08-pgrep-after.txt`, taken before dispatch and after the worker settles, and add them to the ACs. |
| M6 | minor | 543 | `find` output is in directory order, so new entries could reorder the output and make the diff non-empty without any new contract file. | Pipe both `find` runs through `sort` before saving. |
| M7 | minor | 53 | `  >>>NOT YET GIVEN<<<` is indented under a list item, so Markdown renders it as nested blockquotes and hides the `>>>` marker in a rendered view. The raw text, which is what the executor reads, is correct. | Optional: put the marker line in backticks, or state that the raw text is authoritative. |
| M8 | minor | 60 | The skill diff uses local `master`, which is stale (merge-base `4eb75698` against `origin/master`'s `8b4858f7`). The compared set is therefore wider (it includes skill files from the origin/master merge). All 15 exit 0 today. | Optional: use `origin/master`, or keep it and state that the wider set is deliberate. |
| M9 | minor (predates revision 2) | 27, 44 | Line 27 says "Only `lc<NN>-result.md`, `ac-1.3.md` and `p1-phase-report.md` carry verdicts", but line 44 has `lc<NN>-step5.md` record "one verdict" per condition. | Change line 27 to "carry check verdicts", or call the step-5 entries "condition results". |

RECHECK: blocking findings: 1
