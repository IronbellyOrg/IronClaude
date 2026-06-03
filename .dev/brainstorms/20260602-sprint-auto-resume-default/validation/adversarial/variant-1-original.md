# Position A — DD-1 as written: Derive-only, no new state file

## Claim
The resume cursor (which phase was interrupted) can be reconstructed entirely
from the existing `execution-log.jsonl` balanced-event ledger, with NO new
pre-phase breadcrumb file.

## Mechanism
- `phase_start` is written before/at phase execution (`executor.py:1267` per-task path,
  `executor.py:1335` single-process path) via `logging_.write_phase_start` (`logging_.py:59-69`).
- It is closed by either `phase_complete` (`logging_.py:89-107`) or `phase_interrupt`
  (`logging_.py:71-87`, emitted at `executor.py:1488`).
- A `phase_start` with no closing event = hard crash; the interrupted phase number is
  STILL KNOWN from the dangling `phase_start.phase` field.
- This downgrades the R2 crash blind spot from "unknown phase" to "known phase,
  unknown intra-phase progress" — which the BoundaryIntegrityGate already handles.

## Arguments for
1. Zero new write-path surface. NG1 (don't change phase execution) is honored — the
   only write-path change in the whole feature is the DD-4 `tasklist_sha256` field.
2. The ledger already exists and is already written on every phase. No new failure mode
   from a breadcrumb file that itself could be torn/stale.
3. A breadcrumb written "before phase_start" would be redundant with phase_start, which
   is itself written before the per-task subprocess work (`executor.py:1267` → 1270).
4. The planner reads tolerantly (skip malformed lines, design §3), so a torn final line
   degrades gracefully to "phase known from the last good line."

## Cost if wrong
If a hard crash can leave NO usable phase_start (process dies before flush, or torn
line is the only phase_start), the planner falls back to "first phase without
result.json" — still safe, just coarser. The gate catches intra-phase ambiguity.
