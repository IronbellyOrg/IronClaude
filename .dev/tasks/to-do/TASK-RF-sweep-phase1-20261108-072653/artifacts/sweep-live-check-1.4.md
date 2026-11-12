# Step 1.4 live check against the OQ-8 Run (item 9.3), 2026-11-12

Read-only. Run id `run_a4723d345399` (from `phase-outputs/plans/OQ-8-run-id-decision.md`, selected by the owner). `ORCA_CLI_COMMAND` was unset, so the binary is `orca-ide`. Step (0): `grep -n '"worker-list"' src/superclaude/cli/sweep/probes.py` shows `probes.py:49` holds `("orchestration", "worker-list", "--run", "<run>", "--json")`, equal to DESIGN 7.3.

## Step 1: the worker list

Command, exactly: `orca-ide orchestration worker-list --run run_a4723d345399 --json`
Its argv after the binary is `orchestration worker-list --run run_a4723d345399 --json`: the `ALLOWED_ORCA` entry with `<run>` filled, nothing added. Exit code 0, stderr empty. Saved to `artifacts/sweep-live-check-1.4-workers.json` (5 workers, `page.total` 5, `hasMore` false).

## Step 2: the sweep

Command: `uv run superclaude sweep run --run run_a4723d345399` (Bash timeout 120000 ms). Stdout saved to `artifacts/sweep-live-check-1.4.json`.
Exit code 0. Stderr empty (0 bytes). Wall time 5.1 s (collected interval 03:12:39Z to 03:12:44Z). Report: `.dev/sweeps/20261112-031239-sweep.md` (605 lines, last line `Report complete`; the folder is gitignored by item 8.6). The sweep issued 9 Orca reads (1 `worker-list`, 2 `task-list`, 5 `worker-show`, 1 `worktree ps`) and one `git status` per worktree (30 worktrees).

Runs of this check: three live runs happened. The first two (03:11:51Z and 03:12:09Z) each showed 993 `unscanned` source rows `package ledger ...: ledger not readable`, because a `to-do/` package folder without `progress.md` was reported as an unreadable ledger. DESIGN GQ-105 says such a package is `unfinished`, so `probes._ledger` now returns no FINAL line (not unreadable) for a missing ledger file (logged in `### Phase 9 Findings`). The third run (this record) has 0 unscanned sources. Only the third run's output is saved here; the two earlier reports stay in the gitignored `.dev/sweeps/`.

## Step 3: the five recorded workers

Recorded state (from the worker list): `workerState` succeeded, `dispatchStatus` completed, `terminalState` released, `projection.outcome` succeeded, `liveness.verdict` exited. Expected class under step 1.3: no contract was read for these Tasks and `worker_done_seen` is not observable, so rule 6 (finished) and rule 2 (stalled) decline and rule 9 (could not determine) applies; the transcript tails are longer than 256 KiB (`tail_complete` false), so the path-B join also yields could not determine.

| Worker (Dispatch id) | Recorded state | Expected class (step 1.3) | Reported class | Match |
|---|---|---|---|---|
| ctx_4e3237d227c3 | succeeded / completed / exited | could not determine (rule 9) | could not determine (rule `fallback`) | yes |
| ctx_6a0e3e3baaee | succeeded / completed / exited | could not determine (rule 9) | could not determine (rule `fallback`) | yes |
| ctx_7c86fffa9716 | succeeded / completed / exited | could not determine (rule 9) | could not determine (rule `fallback`) | yes |
| ctx_9a3728b21883 | succeeded / completed / exited | could not determine (rule 9) | could not determine (rule `fallback`) | yes |
| ctx_dad78c5c1332 | succeeded / completed / exited | could not determine (rule 9) | could not determine (rule `fallback`) | yes |

Notes carried on each worker row: `Orca: exited; fenced evidence not readable`, `session start not observable: transcript tail only`.

## Step 4: the five REPORT:1247 pass conditions

1. PASS: exit 0 (stderr empty).
2. PASS: the probe calls finished inside the 90 s budget: wall time 5.1 s, no source carries `time budget reached` or `show cap reached`, `summary.bound_reached` is 0.
3. PASS: every row carries a class: 180 of 180 rows (5 Orca rows and 175 transcript rows) have a class (`could not determine`).
4. PASS: each recorded worker got the class its recorded state maps to under step 1.3 (table above, 5 of 5 match).
5. PASS: no row is could not determine because of a probe error or timeout: every source row is read (0 `unscanned` sources); the reasons on the five worker rows are the fencing-evidence and transcript-tail notes above, and the 175 transcript rows are could not determine because no tab-map join places them in the scoped Run (`Orca pane session, not in scoped Runs`).

Result: five PASS lines. Observations for the owner, none a failure of this check: all 180 rows are could not determine (nothing is idle or working in this fixture-less live data, as the design expects with Phase 1 evidence); 2 packages in two worktrees (`TASK-FU-CI-IRONCLAUDE-PIPX-SEGFAULT-20260626`) are in both `to-do/` and `done/` (state `conflict`, listed under Retained problems); the JSON stdout is about 320 KB because it carries every transcript row.
