# Orca automation for the worktree cleanup

Definition only. Nothing in this file has been created in Orca, switched on or triggered. A person sets the automation up in Orca once, and the owner of each workspace switches it on.

The exact file format Orca expects for an automation is not confirmed here. The fields below are what a person enters when creating the automation.

Name: worktree-cleanup-daily
Trigger (UTC): 0 8 * * *
Status: written, not switched on

## Why the name and the trigger are what they are

- The name must not start with `coordinator-`. Orca run history under that prefix is copied into the daily work report, and this job must stay out of it.
- Orca triggers are UTC, so the cron string is in UTC: 08:00 every day of the week. That is 2:00 AM Central in winter and 3:00 AM Central in daylight saving time. Whether the `--timezone America/Chicago` option can hold 2:00 AM all year, for a cron string and not only for a preset such as `daily --time 02:00`, is UNVERIFIED (source section 11, item 8). If it cannot, keep `0 8 * * *`.
- The command below has no `--apply`. The script's default is a dry run, so this job only prints and writes the table of what it would remove (`prune-<UTC stamp>.md` and `.json` under the output folder) and removes nothing.

## Command to run (precheck shape)

This is the shape the workspace's existing scheduled jobs use (not re-verified here): load the workspace environment, start the script detached, and exit non-zero so Orca starts no agent session and leaves no terminal. A run that exits this way shows as `skipped_precheck`; that this happens in this Orca build is UNVERIFIED (source section 11, item 6). `<checkout>` is a checkout of this repository and `<out dir>` is a folder outside every worktree.

```
bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv; [ -f ~/.env ] && . ~/.env; set +a; cd <checkout> && setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune --out <out dir> >> <out dir>/run.log 2>&1 < /dev/null &'; exit 1
```

`uv run --no-project` is used on purpose: a plain `uv run` inside a checkout can rewrite `uv.lock`, which an unattended job must not do. The script itself reads credentials only from environment variables; the command above only loads the workspace's own environment first. If the variables are already in the environment of the process Orca starts, drop the two `. ~/...` loads.

## Rollout ladder

1. The owner of each workspace switches the automation on. Nobody switches it on for another workspace, and a dispatched worker does none of this.
2. The first week it reports only: the command stays exactly as written above, with no `--apply`. Each day the owner reads the table in `<out dir>`.
3. When the tables show only worktrees the owner would remove by hand, the owner edits the automation and adds `--apply` to the command. This edit is the owner's decision and is never made by a worker.

## Environment variables (names only; no value belongs in any file)

- `GH_TOKEN`: a token that can read pull requests and issues in IronbellyOrg and, for the evidence push, write to `IronbellyOrg/run-evidence`.

Optional, not secret: `RUN_EVIDENCE_REPO` (default `IronbellyOrg/run-evidence`), `RUN_EVIDENCE_DIR` (the local clone of the evidence repo) and `WORKTREE_CLEANUP_IDLE_DAYS` (default 7).

## Human steps, in order

- Run `uv run --no-project python scripts/worktree_cleanup.py list` once by hand in the workspace and read the table.
- Run `prune` once by hand without `--apply` and read the two files it writes under the output folder.
- Create the automation in Orca from the fields at the top of this file and leave it switched off.
- The workspace owner switches the automation on, then follows the rollout ladder above.

## When a run fails

A failed run exits non-zero and removes nothing it could not finish: a worktree whose save or check failed is kept, and the table shows the reason. Because the name stays out of the daily work report, nothing else reports the failure. `<out dir>/run.log` holds the error text (it never holds a token), and the newest `prune-<UTC stamp>.md` shows when the job last ran.
