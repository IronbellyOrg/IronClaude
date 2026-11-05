---
status: success
tier_reached: 2
confidence: 0.92
escalation_reason: low_confidence
caller: sc-pr-submit-protocol
---
# Troubleshoot report: Tier 2 evidence collector bounds and restart directory (PR #378 findings A2, C1)

## Summary
Two independent defects in the Tier 2 evidence path. A2: without `timeout` on PATH, `bounded()` runs the git read in the foreground and checks the 60-second budget only after it returns, so a hung read is waited out in full (65 s observed). C1: a resume restart keeps its cycle id and collects into the same `<output-dir>/sync/<cycle_id>/<n>/` again, which the collector rejects with `EVIDENCE_FAIL out_not_empty`, sending a recoverable restart to Tier 3.

## Documentation Context
The design promises "Whole run under 60 s (`timeout` per command when available)" and requires an empty `--out`, while resume rows 5 and 7 restart under the same cycle id; both defects are gaps the script and refs follow literally (doc-context.md). The fix keeps every documented token, the one-line stdout contract and the static-text rules.

## Diagnosability Context
Verdict partial, complexity trivial: A2 is silent until the hung command returns; C1 fails at once with a token. Hermetic regression tests make both observable (diagnosability-context.md; 2x2 rows D-1 to D-4).

## Diagnosis
A2: the no-`timeout` branch has no watchdog; the deadline is enforced only between commands. C1: the evidence directory is keyed by cycle id only, but an attempt needs a fresh, empty directory.

## Evidence
- src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:68-70 — check_deadline compares SECONDS only when called
- .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/probe-evidence.out:8 — `timeout on PATH: none; exit=2; elapsed=65s` (unfixed)
- .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/probe-evidence.out:5 — `EVIDENCE_FAIL out_not_empty` (restart into the same directory)
- src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:253 — row 5 restarts under the same `cycle_id`
- .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/probe-evidence.out:11 — post-fix `exit=2; elapsed=61s`

## Proposed Fix
(A2) `bounded()`: compute the remaining budget once and fail `timeout` when it is not positive (GNU `timeout 0` disables the limit); without `timeout`, run the command as a background job with fds 3 and 4 closed, poll it with `kill -0` and `sleep 0.2`, and at the deadline send TERM, wait 1 s, send KILL, reap it and fail `timeout`. (C1) A pure `conflict_attempt(events, cycle_id)` in conflicts.py counts the cycle's `sync_started` records; step 3 sets `cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/` and every attempt file (evidence, resolution.md, message, manifest) goes there; the validator reads only the attempt's directory; earlier attempts' files stay. Regression tests: test_without_timeout_a_hung_read_is_stopped_at_the_budget, test_without_timeout_a_normal_run_still_succeeds, test_restart_attempt_collects_into_a_fresh_attempt_directory, test_x3_resume_restart_collects_into_a_new_attempt_directory, conflict_attempt unit tests, the attempt-directory protocol pin.

## Risk + Rollback
An operator interrupt during the poll leaves the background read running (cleanup removes the temp directory, not the job); PID reuse within the 1 s grace; the hang test takes about 60 s. Rollback: revert the fix commit.

## Pipeline Hardening Closure
See hardening.md: applicable (CLI/subprocess, persisted resume state); verdict advisory (HC3, HC4 N/A with rationale).

## Next Steps
sc:pr-submit publishes the edits in the cycle's single fix commit after VAL, replies on threads A2 and C1 with the fix SHA and resolves them.
