# Hypothesis: the draft `bounded()` fallback holds up on edge cases; the `timeout` branch can call `timeout 0` (no limit) at the deadline

**Agent**: quality-engineer (lens; worker troubleshoot-analyst)
**Tier**: 2
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: off-by-one-second race in the unchanged `timeout` branch; the draft fallback itself is sound
**Claim class**: `code_path`
**Evidence class**: `runtime_repro` (A2 hang reproduced, probe-evidence.out:7; `timeout 0` behaviour measured by the parent on receipt, audit.log)
**Verdict direction**: `AFFIRM` (A2's draft fix, with one amendment)
**Consistency with docs**: aligned (script header :26 "whole run is bounded to 60 seconds"; design :841 per doc-context.md)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:75-105 @ bash, with and without `timeout` on PATH
producer-citation-check: skipped — menu absent or empty (producers.md header-only)

## Claim
Draft paths verified correct by source read: `wait "$pid"` returns the job's status; safe under `set -u` (rc unset only on the fail path); a job that exits before the first `kill -0` is reaped by bash and the loop ends; callers send stdout/stderr into $TMP files (:202, :210-211) and the job's fds 3/4 are closed, so a leftover grandchild cannot hold the caller's pipes; `fail` exits the main shell so the EXIT trap removes $TMP; a missing `sleep` spins but still stops at the deadline. The real gap is outside the draft: `check_deadline` passes at SECONDS = DEADLINE-1 and, if the clock ticks before the subtraction, `remaining` is 0 and `timeout 0 cmd` runs with no bound (GNU coreutils: duration 0 disables the limit).

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:69 | check_deadline uses a strict `<` |
| E2 | source_citation | (draft, before amendment) collect-conflict-evidence.sh:77-80 | check, subtraction and `timeout "$remaining"` are separate steps |
| E3 | source_citation | collect-conflict-evidence.sh:86-101 (draft) | background job, poll, TERM, sleep 1, KILL, wait, fail |
| E4 | source_citation | collect-conflict-evidence.sh:202, :210-211 | the only callers, both redirected into $TMP |
| E5 | command_output | audit.log (parent measurement on receipt) | `timeout 0 sleep 2` exited 0 after 2 s on GNU coreutils 9.7: a 0 duration disables the limit |
| E6 | behaviour-definition | behaviour-definition: row 1, row 3 | foreground run unbounded; kill -0 / kill (verified by P-1) |

## Proposed Fix
Keep the draft. In `bounded()` replace `check_deadline` + `remaining=` with `remaining=$((DEADLINE - SECONDS)); [ "$remaining" -gt 0 ] || fail timeout "the evidence run exceeded ${LIMIT_SECONDS} seconds"`; keep the after-command check_deadline. No banned words.

## Confidence
Self-reported 0.80 (calibrator re-grades).

## Risks
- PID reuse within the 1 s grace (needs a PID wrap): accepted.
- A process in uninterruptible I/O ignores KILL and `wait` blocks (same for GNU timeout; earlier rev-parse calls would hang first).
- `timeout` runs without `-k`; a command with TERM ignored is not stopped on that branch (the fallback's KILL covers its own branch).
- macOS bash 3.2 `wait <pid>` on an already-reaped job unverified.

## If I'm wrong, it's probably because...
The installed `timeout` treats 0 as expire-now (BusyBox), so the race would fail closed; or bash does not reap the job during `sleep`.

## Falsification standard
`timeout 0 sleep 2; echo $?` prints 0 after ~2 s (measured: yes); with DEADLINE=$SECONDS before a bounded call the amended script gives EVIDENCE_FAIL timeout without running the command; the three draft tests and test_evidence_script_static_rules pass.

## Alternatives considered
- `timeout -k 1` and treat 137 as timeout: rejected (misreports other kills).
- Drop `wait` after KILL: rejected (job not confirmed dead before the trap).
- `read -t` delay instead of sleep: rejected (only CPU cost).
