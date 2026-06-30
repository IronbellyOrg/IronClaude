# Integrity Signal B — `needs_human_decision` Decision Marker (Step 3.7)

**Status:** ⏸️ PENDING USER DECISION
**Timestamp:** 2026-06-04 05:06

## Problem statement (one line)

Integrity `signal_b_pass` re-derives the last_completed task's status from its transcript via
`_classify_transcript`, which **never emits `PASS_RECOVERED`** — so a genuinely-recovered
`last_completed` is re-derived as `FAIL_*` and Signal B independently fails the recovered seam even
after the Signal A widening. A bare `is_success` widening of Signal B is behavior-neutral for
`pass_recovered` (the value can't appear from `_classify_transcript`) but does NOT make the integrity
gate actually validate a recovered seam. This is a DESIGN DECISION, not a one-line swap.

## Options (verbatim from OQ-1)

### Opt-1 (minimal)
Widen only the identity comparison to `is_success` for consistency/future-proofing, and ACCEPT that
the integrity gate still will not validate a recovered seam via Signal B. The load-bearing RED→GREEN
signal is the planner-level pair of assertions: (a) the recovered task is NOT in `rerun_task_ids`, and
(b) it IS selected as `last_completed`. This is a planner-level fix only.

Concretely (if selected): widen `integrity.py` `signal_b_pass = derived is TaskStatus.PASS` →
`derived is not None and derived.is_success` (consistency/future-proofing only — behavior-neutral for
`pass_recovered`).

### Opt-2 (deeper)
Additionally teach Signal B / `_classify_transcript` to recognize a recovered tail (e.g., treat a
`PASS_RECOVERED` persisted status as authoritative, or exempt a recovered `last_completed` from
transcript re-derivation). Broader change with its own tests.

## Blocking statement

**PENDING USER DECISION — Step 3.8 is BLOCKED until a human selects Opt-1 or Opt-2.**

Until a human records a selection (e.g. by adding a `signal-b-decision-RESOLVED.md` in this same
`plans/` directory naming Opt-1 or Opt-2), Step 3.8 makes **NO code change** to `signal_b_pass`. No
default is auto-applied.

## Load-bearing-signal note

The load-bearing regression signal — the planner assertions (a) recovered task NOT in
`rerun_task_ids` and (b) recovered task IS `last_completed` (plus the drift `recorded_completed` and
integrity Signal-A guards in Phase 4) — does **NOT** depend on this decision. The PR is mergeable and
semantically-correct for the planner/drift/Signal-A axes regardless of how OQ-1 is resolved; the
Signal-B design question concerns only whether the integrity gate can additionally *validate* (not
merely not-STOP) a recovered seam.
