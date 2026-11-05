# Tier 1 observation
- Source read (orchestrator): collect-conflict-evidence.sh:78-85. With `timeout` on PATH the command runs as `timeout "$remaining" "$@"`; without it the else branch runs `"$@"` directly, and `check_deadline` (:68-70) runs only after the command returns (:86). A hung git read is not bounded; the script only reports `timeout` once the command finally returns.
- Source read: collect-conflict-evidence.sh:147-151 fails `out_not_empty` when `--out` exists and is not empty.
- Source read: refs/conflict-intent.md:19 passes `--out <output-dir>/sync/<cycle_id>/<n>/`; refs/conflict-mechanical.md:71 reuses the open `cycle_id` on a resume restart and :247 (row 5) restarts "under the same cycle_id". The first attempt's evidence directory therefore already exists and is not empty when the restarted cycle collects again.

## Probe (run 2026-11-04T22:13:20Z, same-shell, scratch repo under /tmp, unfixed script; command: bash probe-evidence.sh <collect-conflict-evidence.sh>; full output in probe-evidence.out)
    == C1: first attempt collects into sync/sync-1/1/
    {"dir":"/tmp/ev-probe.Z4o9dm/out/sync/sync-1/1/","files":["s
    exit=0
    == C1: resume restart (same cycle_id) collects into the same directory
    EVIDENCE_FAIL out_not_empty
    exit=2
    == A2: PATH without timeout; git replaced by a wrapper that hangs on 'show'
    timeout on PATH: none; exit=2; elapsed=65s (the first 'git show' sleeps 65s; a bounded run would stop at 60s)

## Behaviour definitions
- (a) observed: a restart that reuses the cycle's evidence directory fails `EVIDENCE_FAIL out_not_empty` (probe-evidence.out:4-5); per the refs, any EVIDENCE_FAIL escalates the cycle to Tier 3, so a recoverable restart halts.
- (b) observed: without `timeout` on PATH a read that hangs for 65 s is waited out in full (elapsed=65s, probe-evidence.out:7); the 60-second budget is enforced only after the command returns.
- (c) observed (first probe run, wrapper matched only `$1`): with no hang the same PATH completes normally, so the restricted PATH itself is not the failure (run record in audit.log).
