# P0 live plan: pre-run Orca flag check (2026-11-04)

Purpose: before the live P0 plan is edited and started, confirm every Orca verb, flag and selector it uses exists in the installed Orca, and how `--base-branch` resolves the unpushed local commit (reflect finding D-009 and D-014, `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/REPORT.md`). Read-only: only `--help` was run, plus `git remote`/`git rev-parse` and reads of Orca's installed code. No worktree, run or worker was created.

Raw help output: `.dev/orca-command-refactor/review/p0-live-orca-help.txt` (14 verbs, every `--help` exited 0).

## Flags the plan uses

| Plan use | Exists | Help line in p0-live-orca-help.txt |
|---|---|---|
| `worktree create --name --repo --base-branch <ref> --no-parent --json` | yes | 6, 26, 51 |
| `worktree rm --worktree path:<path> --force --json` | yes; `path:<path>` is a listed selector | 76, 85 |
| `worktree list --json` | yes | 100 |
| `orchestration run-create --objective <text> --json` | yes | 121 |
| `orchestration task-create --spec --task-title --run <run_id> --json` | yes | 142 |
| `orchestration worker-start --task --worktree path:<path> --agent --run <run_id> --json` | yes | 164 |
| `orchestration check --run <run_id> --wait --types --timeout-ms --ack <delivery_id> --json` | yes | 215 |
| `orchestration worker-show --dispatch --json` | yes (no `--run`) | 255 |
| `orchestration worker-read --dispatch --source transcript/terminal --cursor --json` | yes | 274 |
| `orchestration worker-release --dispatch --json` | yes | 297 |
| `orchestration worker-list --run <run_id> --terminal-state reclaimable --json` | yes | 320 |
| `orchestration worker-stop --dispatch --json` | yes | 345 |
| `orchestration task-update --id <task_id> --status failed --result cancelled` | yes; valid statuses pending, ready, dispatched, completed, failed, blocked; cancel = stop or abandon, then `--status failed --result cancelled` | 365 and its Notes |

Facts the plan must reflect:
- `worktree rm` "also attempts to delete the checked-out local branch, with or without --force. Orca retains branches it knows predated the worktree and any branch whose changes it cannot prove are already merged" (`worktree rm` Notes). So the plan records whether the branch remains; it never deletes it itself.
- `worker-start` rejects creation flags (`--name`, `--repo`, `--base-branch`, `--setup`) for an existing worktree (`worker-start` Notes), so the plan's route (create the worktree first, then `worker-start --worktree path:<path>`) passes no creation flags to `worker-start`.
- The `run-create` receipt field for the run id is `result.run.id`, and the coordinator handle is `result.run.coordinator_handle` (observed in the 2026-11-03 run-create receipt for run_9747672c2af1: `"run": {"id": "run_9747672c2af1", ..., "coordinator_handle": "term_cddf23a9-..."}`).

## How `--base-branch` resolves (Orca 1.4.237 installed code)

File: `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js` (minified; quoted by function).

- Worktree add: `ihe(...)` builds `git worktree add --no-track -b <new branch> <path> <effectiveBase>`, where `effectiveBase` comes from `tg(...)`.
- Candidate refs: `Pf(e,t)`: `if(e.startsWith('refs/'))return e;let n=e.includes('/')?['refs/remotes/${e}','refs/heads/${e}']:['refs/heads/${e}']` and returns the first candidate that `rev-parse --verify --quiet <ref>^{commit}` resolves.
- Local base refresh: `oh(...)` runs only when `ah(...)` returns a value, and `ah` returns nothing unless the base starts with `refs/remotes/` (or equals the configured remote-tracking base). A `refs/heads/...` base is never refreshed from the remote.

Local repo facts: `git remote` prints only `origin`; `refs/remotes/ironbelly/OrcaCLICommandRefactor-Specs` does not exist; `refs/heads/ironbelly/OrcaCLICommandRefactor-Specs` resolves to `8db29f1165508187b7a14a48f2f66793e269d596`.

Result: `--base-branch refs/heads/ironbelly/OrcaCLICommandRefactor-Specs` is used as given and resolves to the unpushed local commit `8db29f11`. The plan uses that exact form, and keeps its HEAD check in the new worktree as the run-time proof.
