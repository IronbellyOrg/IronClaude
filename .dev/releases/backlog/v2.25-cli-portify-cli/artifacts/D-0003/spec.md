# D-0003 — Open Question Resolution List

**Produced by**: T01.03
**Sprint**: v2.25-cli-portify-cli
**Date**: 2026-03-16

---

## Summary

All 14 Open Questions classified. All 5 blocking OQs resolved. Zero blocking unknowns remain.

---

## Blocking OQs — All Resolved

### OQ-001 — TurnLedger Semantics
**Status**: RESOLVED
**Resolution**: "One turn" is defined as one complete Claude subprocess invocation: from prompt delivery to output completion. The `TurnLedger` records per-step turn counts as (step_id → int) for the full portify run. Retry attempts each count as a separate turn.

### OQ-003 — phase_contracts Schema
**Status**: RESOLVED
**Resolution**: `phase_contracts` is defined as a mapping of `phase_type → list[str]`, where keys are phase type identifiers (e.g., `"synthesize_spec"`, `"analyze_workflow"`) and values are lists of required artifact paths that must exist after the phase completes. Example:
```python
{
  "synthesize_spec": ["release-spec.md"],
  "analyze_workflow": ["workflow-analysis.md", "step-inventory.md"]
}
```

### OQ-004 — api_snapshot_hash Algorithm
**Status**: RESOLVED
**Resolution**: `api_snapshot_hash` is computed as SHA-256 of the sorted, serialized interface contract fields. Serialization: sort field names alphabetically, concatenate as `key=value\n` pairs, encode as UTF-8, then SHA-256. The hash is stored as a hex digest string. Provides a stable fingerprint for detecting interface drift between phases.

### OQ-009 — failure_type Enum Values
**Status**: RESOLVED
**Resolution**: The `FailureType` enum contains exactly 5 values for Phase 1 scope:
```python
class FailureType(Enum):
    NAME_COLLISION = "NAME_COLLISION"
    OUTPUT_NOT_WRITABLE = "OUTPUT_NOT_WRITABLE"
    AMBIGUOUS_PATH = "AMBIGUOUS_PATH"
    INVALID_PATH = "INVALID_PATH"
    DERIVATION_FAILED = "DERIVATION_FAILED"
```
Note: `CONTENT_TOO_LARGE` is NOT part of the Phase 1 5-error spec. It is added in Phase 7 (T07.04) as a Phase 6 amendment for the release-spec synthesis embed guard.

### OQ-011 — --debug Flag Behavior
**Status**: RESOLVED
**Resolution**: `--debug` enables verbose subprocess output capture. When set: (1) raw stdout and stderr from the Claude subprocess are written to the execution log entry for each step, (2) subprocess command is logged at DEBUG level before spawn, (3) gate evaluation details are logged. Does not affect subprocess behavior — only controls log verbosity and log completeness.

---

## Pre-Closed OQs

### OQ-008 — --file Subprocess Behavior
**Status**: CLOSED (pre-session)
**Source**: oq-resolutions.md
**Resolution**: `claude --file <path>` does not reliably deliver content. Use inline `-p` embedding exclusively. Raise `PortifyValidationError` for content exceeding `_EMBED_SIZE_LIMIT` (120 * 1024 bytes).

### OQ-013 — PASS_NO_SIGNAL Retry Behavior
**Status**: CLOSED (pre-session)
**Source**: oq-resolutions.md
**Resolution**: `PASS_NO_SIGNAL` (result file present, no EXIT_RECOMMENDATION marker) → triggers retry. `PASS_NO_REPORT` (no result file) → does NOT trigger retry; treated as pass.

---

## Non-Blocking OQs (to be resolved in assigned phases)

| OQ | Description | Assigned Phase | Default Behavior |
|----|-------------|----------------|-----------------|
| OQ-002 | Kill signal: SIGTERM→SIGKILL grace period | Phase 2 | SIGTERM → 5s → SIGKILL (assessed T01.04) |
| OQ-005 | Prompt template versioning | Phase 5 | No versioning in Phase 1; single template per phase type |
| OQ-006 | TUI refresh rate | Phase 8 | 0.5s refresh interval (matches cleanup_audit TUI) |
| OQ-007 | Agent discovery warning | Phase 2 | `warnings.warn()` for missing agent files (assessed T01.07) |
| OQ-010 | Log rotation policy | Phase 8 | No rotation in Phase 1; single log file per run |
| OQ-012 | Dry-run output format | Phase 2 | Print step list to stdout; no subprocess invocation |
| OQ-014 | Workdir cleanup policy | Phase 9 | Retained after run; no auto-cleanup (assessed T01.07) |

---

## Classification Summary

| Status | Count |
|--------|-------|
| RESOLVED (blocking) | 5 |
| CLOSED (pre-session) | 2 |
| NON-BLOCKING (deferred) | 7 |
| **Total** | **14** |

**Gate**: Zero blocking unknowns remain. Phase 2 implementation may proceed.
