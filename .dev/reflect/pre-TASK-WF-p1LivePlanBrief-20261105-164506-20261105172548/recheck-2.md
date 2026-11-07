# Recheck 2 of plan revision 3 (adversarial)

Plan: `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md` (589 lines of text, file ends at line 589/590). Fix list: `post-fix-rechecks.md` in this folder, "Fix cycle 2", rows 14-21. Brief: `source.md` in the plan folder. Previous review: `recheck-1.md`.

## 1. Rows 14-21

| Row | Present | Plan lines | Result |
|---|---|---|---|
| 14 B1 `run-use` re-attach | yes | 19, 28, 60, 66 | Task 1 (60): if `live-run.json` exists, reuse its `result.run.id`; if its `result.run.coordinator_handle` differs from `$ORCA_TERMINAL_HANDLE`, run `orca orchestration run-use --id <run_id> --json`, receipt `./artifacts/run-use.json`. Line 28 applies the same rule to a resumed live task, receipt `./artifacts/run-use-<NN>.json`. AC (66) accepts a matching handle or `run-use.json`. The two file names are distinct on purpose (Task 1 versus live task NN) and every use agrees (grep: `run-use.json` x2, `run-use-<NN>.json` x1, all in lines 28/60/66). `run-use --id <id> --json` is valid per `orca orchestration run-use --help` (`--id`, `--json`). See m3. |
| 15 M1 baseline keep clause | yes | 60 | The first sentence now reads "save ... only for a file that does not exist yet (on a retry or resume ... both files already exist and are kept)", for both `status-baseline.txt` and `worktree-list-before.json`. The old trailing clause is gone. Consistent with ACs 67 and 589. |
| 16 M2 help list | yes | 60, 65 | The list at 60 now contains `worktree current` and `orchestration run-use`; both exist in the installed Orca (`--help` exit 0). AC 65 ("every Orca verb this plan calls") now holds for all verbs used in the plan text (run-create, run-use, task-create, worker-start, check, worker-show, worker-read, worker-release, worker-list, worker-stop, task-update, worktree create/rm/list/current, status, repo list). |
| 17 M3 parent-check AC | yes | 556, 572 | AC 572 requires `lc22-parent-check.txt` to show the new worktree's parent and the feature worktree id, equal, else FAIL and nothing dispatched. File name matches line 556. See m5. |
| 18 M4 watcher pipeline | yes | 453, 467 | `ps -eo args \| grep -e '--watch' \| grep -v -w -e grep -e shell-snapshots -e ps \| sort` run live here: empty output, with PIPESTATUS `0 0 1 0` under `pipefail`. The old substring bug is gone (`-w`). See m2 about the "exits 1" sentence. |
| 19 M5 lc08 listing files | yes | 229, 242 | `lc08-pgrep-before.txt` and `lc08-pgrep-after.txt` named in the extra (229) and in the AC (242); the pipeline it points to is in Task 19 (453). Names agree. |
| 20 M6 `find` sorted | yes | 543 | Both `find ... \| sort` runs (`ac13-find-before.txt`, `ac13-find.txt`) and the `diff` to `ac13-find-diff.txt`; AC 546 names all three. Same worktree path in both runs, so the diff is meaningful. |
| 21 M9 check verdicts | yes | 27 | "Only `lc<NN>-result.md`, `ac-1.3.md` and `p1-phase-report.md` carry check verdicts (the per-condition results in `lc<NN>-step5.md` are condition results, not check verdicts)." Consistent with 44. See m4. |

## 2. Other checks run (read-only)

- Installed Orca verbs and flags used by the new text: `run-use --id --json`, `check --run --wait --types --timeout-ms --ack`, `worker-list --run --terminal-state reclaimable`, `worker-read --dispatch --source --cursor`, `task-update --id --status --result --run`, `worktree rm --worktree path: --force`: all present in `--help`.
- `orca worktree current --json` prints `result.worktree.id` = `de550e99-...::/home/coder/.../OrcaCLICommandRefactor-P1` and `orca worktree list --json` rows carry `parentWorktreeId` (null today).
- Files cited by the plan exist: the 165021 `post-fix-rechecks.md`, `ac-c6-depth-setting.txt`, `p1-static-report.md`, both P0 scripts, `p0-phase-report.md`, `APPROVED.md`, `tests/skills/test_worker_contract.py`, `decisions/D1/option-a.md` and `option-b.md`, `install_core_files` in `install_core.py`.
- `git status --porcelain -- src plugins tests` is empty; the tree shows only the plan edit and two untracked `.dev/reflect/` folders (both in the baseline-type allowance of AC 67).
- All 22 check ids, the 16 commands and their flags match `source.md` lines 45-79; the only intended departures (owner instruction markers instead of a grant file, `ps` listing instead of `pgrep`, `--parent-worktree active` child instead of `new-child`) are stated in the plan.

## 3. Findings

| # | blocking/minor | plan:line | evidence | fix |
|---|---|---|---|---|
| m1 | minor | 19 | Revision note says revision 3 is "the re-attach ... plus eight wording and listing fixes". Rows 15-21 are seven fixes (M1-M6, M9). | Say "seven". |
| m2 | minor | 453 | "The pipeline exits 1 when the listing is empty" is true only under `pipefail`. Run without `pipefail` here: `rc=0` (the last stage, `sort`, exits 0). Under `pipefail`: `PIPESTATUS=0 0 1 0`, rc 1. The pass rule (second listing has no extra line) is unaffected, so no check can fail on this. | Reword to "the exit status is not used; an empty listing is the passing case and the file is saved even then". |
| m3 | minor | 28, 60 | The re-attach test compares `$ORCA_TERMINAL_HANDLE` with `result.run.coordinator_handle` in `live-run.json`, which is the run-create receipt and keeps the creation-time handle after a `run-use`. In a new terminal every later live task will therefore see a "difference" and run `run-use` again (once per task, receipts `run-use-<NN>.json`). Harmless if `run-use` is idempotent for the bound terminal; the plan does not say what to record if it errors. `orca orchestration run-current` (installed) shows the bound Run and would give the live value. | Optional: compare against `orca orchestration run-current --json` (add it to the line-60 help list), or state that a repeated `run-use` is expected and an error from it is recorded and the task continues to `worker-start`. |
| m4 | minor | 44, 489 (and the other step-5 ACs) | Line 44 still says step 5 writes "one verdict ... for each of five conditions"; line 27 now calls them condition results. Wording only. | Optional: "result" in place of "verdict" in line 44 and the ACs. |
| m5 | minor | 556, 572 | The parent check compares the new worktree's `parentWorktreeId` with the id printed by `worktree current`. No child worktree exists today, so the id format of `parentWorktreeId` (full `<repo>::<path>` form versus the instance id) cannot be confirmed here. A format difference would make an equal parent look unequal and fail the check before dispatch. | Optional: say "compare after normalising: the id, the `identity.instanceId` or the path of the parent must match the feature worktree". |

No finding is blocking.

## 4. Self-Audit (zero blocking findings)

Checked: each of rows 14-21 at its plan lines; every use of `run-use.json`, `run-use-<NN>.json`, `lc08-pgrep-before.txt`, `lc08-pgrep-after.txt`, `lc18-pgrep-*.txt`, `lc22-parent-check.txt`, `ac13-find*.txt` for name drift (none); the install-precondition gate and Task 1 retry path for a second Orca run (reused); the AC at 66 against the `run-use` receipt alternative; the help-list claim at 65 against every verb the plan calls; the watcher pipeline run live (empty output, exit status behaviour both ways); Orca flag presence for every verb in the live-check procedure; cited-file existence; clean-tree check at the current tree; check ids and command lines against `source.md`; Task 25 dependencies (Tasks 2-24) and staging rule.

RECHECK: blocking findings: 0
