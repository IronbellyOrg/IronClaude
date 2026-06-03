# Refactor Plan — DD-1 (base = derive-only, corrected)

## Overview
Keep the derive-only decision (no new heavyweight breadcrumb file). Correct the rationale's
two factual errors and harden the §3 algorithm against torn ledger lines by making the
COMPLETED classification key off the atomically-written `result.json`, not solely the
`phase_complete` ledger event. Net change: documentation + one algorithm clause. No new file.

## Planned Changes
1. **Correct X-001** (DD-1 cell): "written **before** a phase executes" → reflect that on the
   single-process path the subprocess is spawned (executor.py:1331) before `write_phase_start`
   (executor.py:1335). Reframe as "written at phase entry."
2. **Correct X-002 / INV-001** (DD-1 cell + §12 R2): "phase number always survives" is false —
   the JSONL append (logging_.py:265-267) has no fsync/atomic-rename; a hard crash can torn or
   drop the last line. Replace with the accurate durability story: the phase is recoverable
   because `result.json` is written atomically (tmp+rename) and the planner keys off its presence.
3. **Harden §3 COMPLETED test (INV-004 + the torn-`phase_complete` bug):** a completed phase
   whose `phase_complete` line is torn currently falls through to PENDING (line 110 requires the
   event) and is needlessly re-run — dangerous for non-idempotent phases. Make COMPLETED key off
   `result.json` (PASS-family) with the ledger event as corroboration, not a precondition.
4. **Document concurrency caveat (INV-003):** note that `_resolve_release_dir` is deterministic
   (config.py:242) so concurrent `sprint run <same index>` share one ledger with no lock;
   derive-only's pairing loop must tolerate interleaved events (or FR-5 ambiguity must catch it).

## Changes NOT Being Made
- **Do NOT adopt the breadcrumb file (Variant B).** Rejected because INV-004 shows result.json
  already provides the atomic durability anchor; a breadcrumb is redundant write-path surface
  (violates NG1 / the "one write-path change" property) for a case result.json already covers.
