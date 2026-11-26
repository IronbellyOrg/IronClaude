# Variant 2 (refactorer): Run ledger as one file, one command, no hook

## Position
Smallest change that meets every Success Criterion except the hook one, where I choose the allowed "dropped with the reason written down" outcome. Four deletions against the brief:
1. No new command group: one `click` command, `superclaude run-ledger` (not `run-ledger build`), registered with one `main.add_command(...)` line in `src/superclaude/cli/main.py` (same place as `sweep_group`, line ~587).
2. One module file: `src/superclaude/cli/run_ledger.py` (builder, atomic write and click command together, about 150 lines). No package, no new `probes`-style layer.
3. No new sweep flag. `superclaude sweep run` falls back to the ledger when no `--run` is given.
4. No hook, so no lock, no merge logic and no second writer (see Hook).

## Q1 Code location and run
- File: `src/superclaude/cli/run_ledger.py`; test: `tests/run_ledger/test_run_ledger.py`.
- A standalone script would not be on PATH after `pipx install` or `superclaude install`; a CLI command is, so the schedule runs `superclaude run-ledger`. It calls `orca` through `subprocess.run([...], capture_output=True, timeout=30)` with a fixed argv list, no shell.
- Flags: `--ledger PATH` (default below), `--dry-run` (print the would-be ledger, write nothing), `--json` (print the summary line as JSON). Exit codes: 0 written; 1 Orca failure or implausible result (old ledger untouched); 2 usage.
- The builder uses only these Orca calls: `orca orchestration run-list --json`, `orca worktree list --json`, `orca orchestration task-list --run <id> --json`, `orca orchestration worker-list --run <id> --json --limit 100 [--cursor <c>]`. It does NOT touch sweep's `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py`, so `tests/sweep/test_probes_allowlist.py` stays green.

## Q3 Ledger file
- Fixed per-user path: `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`, overridable by `--ledger` or env `SUPERCLAUDE_RUN_LEDGER`. Reason: Orca Runs are global to the Orca server, not to a worktree; `.dev/coordinator/` inside one worktree is invisible to a schedule or sweep started from another, and is deleted when that worktree is removed. It must not be under the repo (nothing to stage, nothing to gitignore).
- Schema (version 1):
```json
{"version":1,"generated_at":"2026-11-26T18:00:00Z","orca":{"runs_listed":63,"worktrees_listed":12},
 "runs":[{"id":"run_915328e33d9a","created_at":"...","objective":"first 120 chars",
   "reasons":["live_worktree","unfinished_task","new"],
   "live_worktree_ids":["<repoId>::<path>"],"unfinished_task_count":0}]}
```
`generated_at` is captured BEFORE the first Orca call so the `new` rule cannot miss a Run created mid-build.

## Q5 Exact inclusion rules (verified against this host unless marked)
Candidates: every Run from `run-list` with `legacy == 0` and `id != "run_legacy_local"`. (`run_legacy_local` is the only `legacy:1` Run on this host: verified.) A Run is IN if any one reason holds:
- `live_worktree`: any worker row has `resource.worktreeId` (string equals) an `id` in `worktree list --json` `result.worktrees[].id`. Verified: worker `resource.worktreeId` is `de550e99-...::/home/coder/workspaces/worktrees/IronClaude/launch-gate-flip`, the same `<repoId>::<absolute path>` form as the list `id`. So match the whole string; do not split or compare bare paths. A worker row with no `resource` or null `worktreeId` counts as no match.
- `unfinished_task`: any task whose `status` is NOT in the terminal set `{completed, failed, cancelled}`. Observed statuses across all 63 Runs: completed 644, failed 60, blocked 18, ready 12 (counted by me now). Denylist not allowlist, so a status I did not see (`pending`, `dispatched`, `in_progress`, UNVERIFIED names) keeps the Run in rather than silently dropping live work. `failed` is terminal: counting it would pull in old Runs forever (60 failed tasks). Cost to record in the risks: a Run whose only open task is stale `blocked` stays in until someone settles that task.
- `new`: `created_at >= previous_ledger.generated_at`. If there is no previous ledger or it is unreadable, this rule is skipped (otherwise all 63 would be "new").
Pagination: loop `worker-list` while `result.page.hasMore` is true, passing `--cursor result.page.nextCursor` (key names verified), `--limit 100`. A repeated cursor or more than 50 pages for one Run is a FAIL. `task-list` returned all tasks in one response in my check (`result.tasks[]`, `count`); no pagination seen. UNVERIFIED for Runs above 100 tasks.
Short-circuit (saves calls): fetch tasks first; fetch workers only for Runs not already in by task or `new`.

## Failure and implausible-empty rule (keep old ledger, exit 1)
Keep the old file and print the reason to stderr when any of these hold:
1. any Orca call exits non-zero, times out (30 s each) or returns JSON without `"ok": true`;
2. `worktree list` returns 0 worktrees (the main checkout always exists, so 0 means a broken read);
3. `run-list` returns 0 Runs while a previous ledger exists;
4. the new ledger has 0 runs while the previous ledger had at least 1 AND at least 1 non-legacy Run exists. A real "all settled" state is rare; an operator forces it with `--accept-empty`.
No partial writes: build the whole dict in memory first; any exception before the write leaves disk untouched.

## Q4 Write method and concurrency
One writer only (the schedule), so no lock is needed for correctness. Write `run-ledger.json.tmp.<pid>` in the same directory, `fsync`, then `os.replace` to the final name; readers see the old or the new file, never half. A second overlapping rebuild just overwrites with an equally fresh file. Skipping `flock` is deliberate; add one only if the hook is ever adopted.

## Q2 How sweep consumes it
- Change `src/superclaude/cli/sweep/commands.py`: after the explicit `--run` list and the terminal-bound Run lookup both come up empty, read the ledger file (plain `json.load`, zero Orca calls) and use its ids; each id still passes `probes.RUN_ID_RE`. Explicit `--run` always wins and the ledger is then not read. Only if the ledger is missing or invalid does it exit 2 with the old message plus `run "superclaude run-ledger" first`.
- No `--ledger` flag on sweep (add one only if a test needs it; the env var `SUPERCLAUDE_RUN_LEDGER` already covers tests). The sweep skill still runs only `superclaude sweep run`, so its `Bash(superclaude sweep run:*)` permission is unchanged. No change to the allowlist.
- Staleness: if `generated_at` is older than 3 hours, sweep prints one header line "ledger is N h old" in the report; it does not fail (a stale list is better than none, and the report says so).

## Q7 and the hook: drop it
Reasons, written down for the Success Criterion:
- With a 30-minute rebuild the `new` rule already admits a Run created after the last build at the next build; the hook only shortens that gap from at most 30 min to 0, and sweep itself runs every 30-60 min. The sweep after the next build sees the Run either way.
- It adds the only second writer (lock, merge with rebuild, a race where the rebuild's `new` rule and the hook append disagree), a PostToolUse parser of Bash output, a settings.json edit the owner must approve, and an install path through `src/superclaude/cli/install_hooks.py`.
- What `run-create` prints to a PostToolUse hook is UNVERIFIED: I may not run `run-create`, and the hook input shape (`tool_response` for Bash) is not confirmed on this host. The brief's own test would need a throwaway Run.
- Fallback if the owner insists on instant pickup: have the coordinator run `superclaude run-ledger` itself right after it calls `run-create` (about 25 s, one command, no hook). That needs no new file.
Criterion changed: "Hook tested ... or dropped with the reason written down" is met by the second branch; the test for the first branch is not built.

## Q6 Scheduling (nothing installed)
Recommend the system crontab for the coder user, shipped as a comment-only example `docs/user-guide/run-ledger-cron.md` (or a 3-line snippet inside the command's `--help`), not installed:
`17,47 * * * * /home/coder/.local/bin/superclaude run-ledger >> ~/.local/state/superclaude/run-ledger.log 2>&1`
Why: it survives session and Orca restarts, needs no model, and exits non-zero with a logged reason. Session-only cron dies with the session (the exact problem); an Orca automation adds a dependency on a feature this builder does not need (UNVERIFIED whether it runs non-model commands). The `PATH` entry must be the pipx path above (UNVERIFIED on the owner's host: `command -v superclaude` first). Offset minutes avoid the top-of-hour Orca load. The owner gives a go before `crontab -e`.

## Rebuild cost estimate (to verify in the real run)
Calls: 1 run-list, 1 worktree list, 62 task-list, plus worker-list pages only for undecided Runs (about 8 pages in the brief's measurement). At 0.18 s each that is about 15 to 25 s, against 48.6 s for sweeping every Run. The real-Orca run must report the measured time and the sweep time over the resulting ledger (expected: 3 Runs plus any with open tasks, about 3 to 10 s).

## Named tests (`tests/run_ledger/test_run_ledger.py`; fake `orca` via a `monkeypatch` of the runner, no real Orca)
- `test_live_worktree_run_in`: worker `worktreeId` equal to a listed id gives reason `live_worktree`.
- `test_deleted_worktrees_only_run_out`: all worker ids absent from the list, all tasks completed, old `created_at` gives OUT.
- `test_unfinished_task_run_in`: parametrized over `ready`, `blocked`, `in_progress`, `some_unknown_status` gives IN; `completed`, `failed`, `cancelled` give OUT.
- `test_new_run_in`: `created_at` after the previous ledger `generated_at`, no workers or tasks gives IN with reason `new`; no previous ledger skips the rule.
- `test_legacy_run_out`: `run_legacy_local` and any `legacy:1` Run are OUT even with a live worktree.
- `test_orca_failure_keeps_old_ledger`: non-zero exit, timeout and `ok:false` leave the file bytes unchanged and exit 1.
- `test_implausibly_empty_keeps_old_ledger`: rules 2 to 4 above; `--accept-empty` overrides rule 4 only.
- `test_worker_list_pagination`: three pages via `hasMore` and `nextCursor`; a repeated cursor FAILs.
- `test_atomic_write`: a failure raised inside `os.replace` leaves the old file and no `.tmp` residue.
- `test_sweep_reads_ledger_when_no_run`: `sweep run` with no `--run` uses ledger ids; explicit `--run` ignores the ledger; a missing ledger gives exit 2 and the hint; a malformed id in the ledger is rejected by `RUN_ID_RE`.

## Delivery steps
1. Edit under `src/superclaude/` only (`cli/run_ledger.py`, `cli/main.py`, `cli/sweep/commands.py`), then `make sync-dev`; do not stage `.claude/`. 2. `uv run pytest tests/run_ledger tests/sweep -v`. 3. One real run: `uv run superclaude run-ledger --dry-run`, then a real write to a temp `--ledger`, then `SUPERCLAUDE_RUN_LEDGER=<temp> uv run superclaude sweep run`; report both timings. 4. Nothing installed, no commit until the owner says so; stage `.dev/tasks` if a task package is created.

## Risks
- Unknown task status names for unfinished work: mitigated by the denylist; a wrongly-open Run only costs sweep time.
- A Run with live work but a worktree Orca no longer lists, and no open task, drops out: accepted by the brief's own rule.
- A Run created and finished between two builds never enters: harmless (nothing to sweep).
- `generated_at` clock use: single host, same clock; an NTP step back could re-admit a few Runs as `new` (harmless).
- Ledger stale if cron dies: surfaced by the 3-hour header line, not silent.
- Dropping the hook trades up to 30 min of lag for one fewer writer; the coordinator-runs-the-command fallback covers urgent cases.
