# Preflight (Task 1)

Run in the feature worktree `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs` on 2026-11-04 (UTC, 05:59 to 06:01).

| # | Check | Command | Output | Result |
|---|---|---|---|---|
| 1 | Orca terminal handle set | `echo "$ORCA_TERMINAL_HANDLE"` | `term_cddf23a9-82f5-45ee-a9b8-1fdd61d80197` | PASS (non-empty) |
| 2 | HEAD commit | `git rev-parse HEAD` | `8db29f1165508187b7a14a48f2f66793e269d596` | PASS |
| 3 | Branch | `git branch --show-current` | `ironbelly/OrcaCLICommandRefactor-Specs` | PASS |
| 4 | Branch ref commit | `git rev-parse refs/heads/ironbelly/OrcaCLICommandRefactor-Specs` | `8db29f1165508187b7a14a48f2f66793e269d596` | PASS (same commit as check 2) |
| 5 | Installed worker contract equals source | `cmp ~/.claude/WORKER-CONTRACT.md src/superclaude/core/WORKER-CONTRACT.md` | no output, `cmp_exit=0` | PASS |
| 6 | AC-C6 depth setting | `grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json` | `"nestedWorkerMaxDepth":1` (one line, `grep_exit=0`) | PASS |
| 7 | Orca runtime ready | `orca status --json` | `"runtime": {"state": "ready", "reachable": true, "connectionState": "connected", ...}` (app version `1.4.237-aidev02.0e4491a95e92`) | PASS |
| 8 | Repo listed | `orca repo list --json` | contains id `de550e99-fa3c-42e2-abfe-1d092771c759`, path `/home/coder/workspaces/IronClaude` (1 match) | PASS |

Other Task 1 steps (files in this folder):

- `status-baseline.txt`: `git status --porcelain` saved before any other write (14 lines).
- `orca-help.txt`: `--help` of the 13 verbs the plan uses, each with `[exit=0]`.
- `symptom-check.txt`: pytest run, exit 1, `3 failed in 0.39s`. Cause shown in the file: `Failed to spawn: ruff`.
- `live-run.json`: run id `run_0f9350decd8c`, `coordinator_handle` `term_cddf23a9-82f5-45ee-a9b8-1fdd61d80197` (equals check 1).
- `status-end-t1.txt`: `git status --porcelain` after the task; the sorted path list is identical to the baseline's.
