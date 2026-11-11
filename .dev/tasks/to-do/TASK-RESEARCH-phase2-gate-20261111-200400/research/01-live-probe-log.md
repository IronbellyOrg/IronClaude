# Research: live probe of `orca orchestration check --all --run <runId> --json`

**Investigation type:** Live test on throwaway Runs (Code Tracer / behaviour probe)
**Status:** Complete
**Date:** 2026-11-11 (first call 2026-11-11T20:00:47Z)
**Executable:** `orca-ide` (ORCA_CLI_COMMAND unset; Linux host; version 1.4.245-aidev02.9cfecdd30b2a). Used for every call.
**Probe Runs (mine, created by `run-create`):** `run_c1badaa6576b` ("phase 2 gate probe", Run A) and `run_14cfcbd8edf2` ("phase 2 gate probe B", Run B).
**Never touched:** `run_93bfa00cae2b` (coordinator's live inbox), no `run-use` for it, no read of any Run I did not create. One `inbox --limit 100` call was made and only per-Run row counts were kept (see L-12).

Raw (sanitized) outputs are in `research/evidence/`. Pane keys and pty ids were blanked.

## Log (command, result, evidence file)

| # | Command (all `orca-ide orchestration ...`) | Observed | Evidence |
|---|---|---|---|
| L-1 | `run-current --json` before anything | `"run": null` (terminal bound to nothing) | transcript |
| L-2 | `run-create --objective "phase 2 gate probe" --json` | ok; `run_c1badaa6576b`; `coordinator_handle` = my terminal; `consumer_generation` 1; terminal becomes bound to it | evidence/ (run-create output saved in /tmp, id recorded here) |
| L-3 | second `run-create` (Run B) | ok; `run_14cfcbd8edf2`; terminal now bound to B | evidence/ |
| L-4 | `send --to run:<A> --type question ...` from my worker terminal | FAILED `dispatch_run_mismatch`: my terminal is an active Dispatch of the coordinator's Run, so it cannot send into another Run. Same with `--run`. | transcript |
| L-5 | `send --to <my own terminal handle> --type question ...` while bound to B | ok; the stored row has `run_id` = B and `to_handle` = `run:run_14cfcbd8edf2` (a terminal handle is rewritten to the bound Run mailbox) | transcript |
| L-6 | `run-use --id A`, send question + status to own handle; `run-use --id B`, send status | 2 rows in A (question, status), 2 in B (question, status) | transcript |
| L-7 | `check --all --run A --json` while bound to B | FAILED `consumer_fenced`: "This caller is bound to Run B, not Run A. Nothing changed." | evidence/01, 02 |
| L-8 | `check --all --run B` and `check --all` (no flag) while bound to B | identical rows (2 messages, B only), `count` 2, `delivered_at` null | evidence/03, 04 |
| L-9 | Same reads with `ORCA_TERMINAL_HANDLE` and pane variables removed (`env -u ...`) | FAILED `no_active_terminal`, for `--run A`, `--run B` and no `--run` | evidence/17, 18, 19 |
| L-10 | after `run-use --id A`: `check --all --run A`, `check --all`, `check --all --run B` | A: 2 rows (A only); no-flag: same A rows; `--run B`: `consumer_fenced` | evidence/23 |
| L-11 | `run-show` on both Runs after the rebinding | `consumer_generation` rose (A: 1 -> 5, B: 1 -> 3); `coordinator_handle` of A was `null` while I was bound to B and returned to my handle when I bound A again | transcript |
| L-12 | `inbox --limit 100 --json` (counts only) | 100 rows, all Run B (my 104+ probe messages are the newest). Rows have `read`, `sequence`, `sender_pane_key`, `pointer_*` which `check --all` rows lack. Cross-Run reach of `inbox`: not shown | evidence/20 (3 rows), counts in transcript |
| L-13 | `check --all --types question` / `--peek --types status` / `--types bogus` | filters rows server-side (1 question row; 1 status row); unknown type rejected `invalid_argument` | evidence/24, 25 |

## Non-consumption sequence on Run B (my own Run; I am its coordinator)

| Step | Command | Result | Evidence |
|---|---|---|---|
| N1 | `check --all --run B` | 2 rows, `count` 2 | 03 |
| N2 | same again | identical to N1 apart from envelope id | 03 vs 04 |
| N3 | `check --peek --run B` | 2 rows, FIFO order (oldest first) | 05 |
| N4 | `check --all --run B` | 2 rows, newest first | 06 |
| N5 | consuming `check --run B` (the real owner) | **both messages delivered**, `deliveryId` `delivery_657cbe0e1ebb`, count 2 | 07 |
| N6 | `check --all` then `--peek` before ack | 2 rows both (a delivery is replayed until acked) | 08, 09 |
| N7 | `check --run B --ack delivery_657cbe0e1ebb` | `acknowledged` set, `count` 0, `deliveryId` null | 10 |
| N8 | `check --all` after ack | still 2 rows; `delivered_at` still null; no read flag | 11 |
| N9 | `check --peek` after ack | `count` 0 (messages now read) | 12 |

## Cap and timing (Run B, 104 messages)

| Check | Result | Evidence |
|---|---|---|
| 102 sends | 0 failures | 13 |
| `check --all` | exactly 100 rows, newest first (`cap probe 102` ... `cap probe 3`); the 4 oldest (cap probe 1, 2, "probe self q1", "probe B status") are missing; no truncation, total or hasMore field | 14 |
| `check --peek` | exactly 100 rows, oldest first, starting at `cap probe 1` (peek lists unread only; the two acked rows are excluded); `cap probe 102` and one other are missing | 15 |
| Latency | `--all` 0.197 / 0.199 / 0.200 s; `--peek` 0.189 / 0.197 / 0.195 s; one `send` 0.201 s | 16 |

## Other read-only facts (help text, not run)

- `worker-list --help` shows `--terminal-state <active|reclaimable|retained|release_pending|release_unknown|released>`. The spec calls a state filter UNVERIFIED (INV-007); help now shows one exists. Not run against live data.
- `reset (--all | --tasks | --messages)` has no Run argument in its usage line. Not run (could affect the live inbox).
- `send --type` valid values: status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat.
- `ask` (blocks, creates a question to the coordinator) was tried against my own Run and failed with `dispatch_run_mismatch`; so whether `ask` writes a `type: question` row is UNVERIFIED.

## Cleanup

No Run delete or archive verb exists in `orchestration --help`. The two probe Runs and their messages (about 107) stay. They are named in the report. My terminal is still bound to `run_c1badaa6576b`. `reset` was deliberately not run.
