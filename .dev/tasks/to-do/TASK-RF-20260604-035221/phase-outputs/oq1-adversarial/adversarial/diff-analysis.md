# Diff Analysis: OQ-1 Integrity Signal B — Opt-1 (minimal) vs Opt-2 (deeper)

## Metadata
- Generated: 2026-06-04
- Variants compared: 2 (Opt-1 minimal widening; Opt-2 deeper recovered-aware gate)
- Depth: quick (Round 1 only)
- Decision: how the sprint auto-resume `BoundaryIntegrityGate` Signal B should treat a `PASS_RECOVERED` last_completed task.

## Shared mechanics (ground truth, both options accept)
- `validated_last = signal_a_pass and signal_b_pass and artifacts_ok`; if False → `lc.suspect = True` → gate `passed=False` → auto-resume STOPs / requires operator confirmation.
- Signal A (already fixed): `lc.persisted_status is not None and lc.persisted_status.is_success` → True for PASS_RECOVERED.
- Signal B: `derived = _classify_transcript(transcript); signal_b_pass = derived is TaskStatus.PASS`.
- `_classify_transcript` (shared, imported from `rerun_tasks`) is `-> TaskStatus`, NEVER emits PASS_RECOVERED, and a genuinely-recovered task's transcript (non-zero exit + error result-event) classifies as FAIL_TERMINAL / FAIL_RECOVERABLE.
- Therefore: **even after the Signal A fix, Signal B independently returns False for a recovered last_completed → the gate STOPs the exact crash-tail scenario auto-resume targets.**

## Content Differences

| # | Topic | Opt-1 (minimal) | Opt-2 (deeper) | Severity |
|---|---|---|---|---|
| C-001 | Does the gate validate a recovered seam? | NO — `signal_b_pass` widening is behavior-neutral for pass_recovered; gate still STOPs (operator must override) | YES — gate validates recovered seams end-to-end | High |
| C-002 | Code change | ~1 line (`derived is not None and derived.is_success`) | integrity.py: exempt PASS_RECOVERED last_completed from transcript re-derivation (Opt-2a) OR teach `_classify_transcript` (Opt-2b) | High |
| C-003 | Blast radius | Behavior-neutral, integrity.py only | Opt-2a: localized to integrity.py; Opt-2b: touches SHARED `_classify_transcript` (also feeds `discover_failed_tasks_from_transcripts` rerun failed-task discovery) → large | High |
| C-004 | Test burden | None (planner+Signal-A tests already cover load-bearing behavior) | New test: recovered last_completed → `validated_last is True` (the assertion the original task's F1 GUARD deliberately deferred) | Medium |
| C-005 | Double-check integrity for recovered tasks | Preserved structurally but USELESS (always stops) | Opt-2a: 2 signals (persisted ∧ artifacts); drops the transcript axis ONLY for recovered (which cannot work anyway) | Medium |
| C-006 | Failure mode | Fails CLOSED (safe; asks operator) | Validates (passes) recovered seams automatically | Medium |

## Contradictions
- X-001: "The gate is an INDEPENDENT deterministic double-check" (design intent) vs "A recovered task's transcript is structurally a failure transcript" → Signal B's transcript-rederivation axis is fundamentally incompatible with PASS_RECOVERED. Both options must reconcile this; Opt-1 by disabling the gate for recovered tasks, Opt-2a by replacing the transcript axis with artifact-existence for recovered tasks.

## Shared Assumptions (UNSTATED, promoted)
- A-001 [SHARED-ASSUMPTION]: Both assume a recovered crash-tail is a COMMON auto-resume scenario (PASS_RECOVERED = "hit turn/budget overrun but completed"). If recovered tails are RARE, Opt-1's degraded UX matters little; if COMMON, Opt-1 permanently cripples the gate for the headline case. **Status: load-bearing for the recommendation.**
- A-002 [SHARED-ASSUMPTION]: Both assume Opt-2b (touching shared `_classify_transcript`) is OUT — only Opt-2a (localized integrity exemption) is a safe deeper fix. CONTRADICTED if someone reads "Opt-2" as the shared-function change.

## Summary
- Highest-severity items: C-001, C-002, C-003 (High). The crux is A-001 (frequency of recovered tails) and the X-001 design tension (transcript-rederivation cannot work for recovered tasks).
