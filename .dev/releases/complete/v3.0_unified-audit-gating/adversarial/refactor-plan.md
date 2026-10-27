# Refactoring Plan: Merge Into Variant B Base

**Date**: 2026-03-18
**Base variant**: Variant B (Wiring Verification Gate v2.0) -- score 0.860
**Donor variant**: Variant A (Unified Audit Gating v1.2.1) -- score 0.568
**Strategy**: Incorporate Variant A governance elements as a clearly separated appendix and adapt rollout content in-place.

---

## Merge Operations

### W-001: Add Lifecycle Governance Appendix

**Source**: Variant A Sections 4, 9
**Target**: New Appendix D in merged spec
**Operation**: Create a new appendix titled "Lifecycle Governance Framework" containing:

1. Legal/illegal transition table from Variant A Section 4.1-4.2, adapted to reference the wiring gate as one input to transition decisions
2. Override rules from Variant A Section 4.3, noting that overrides apply at the lifecycle level, not the gate level
3. Timeout/retry semantics from Variant A Section 4.4 (applicable to lifecycle transitions, not to the deterministic wiring gate which uses `retry_limit=0`)
4. Owner responsibilities from Variant A Section 9.2
5. Decision deadline requirements from Variant A Section 9.3

**Handling**: Mark this appendix as "governance layer -- implementation sequence follows wiring gate core" to prevent it from blocking wiring gate work.

### W-002: Adapt Rollout Section with Rollback Triggers

**Source**: Variant A Section 7.3
**Target**: Merged spec Section 7 (Rollout Plan)
**Operation**: Add rollback trigger conditions to each rollout phase, adapted for wiring gate context:

- Shadow: rollback if analysis produces zero findings on a known-positive codebase (sanity check)
- Soft: rollback if FPR exceeds calibrated threshold or determinism breach detected
- Full: rollback if validator bypass discovered or consecutive-pass window interrupted

Drop M-series metric references (M1-M12) as those are lifecycle-level KPIs not applicable to a single gate.

### W-003: Add Calibration Methodology to Rollout

**Source**: Variant A Section 8.2
**Target**: Merged spec Section 7, new subsection after Phase 1
**Operation**: Add calibration methodology adapted for wiring gate:

1. Collect FPR/TPR/p95 for at least two shadow windows
2. Compute baseline distributions per analysis type (unwired_callable, orphan_module, unwired_registry)
3. Propose thresholds and FPR noise floor (incorporating Variant B's existing FPR calibration formula)
4. Obtain sign-off for soft activation

### W-004: Add Decision Tracking Section

**Source**: Variant A Section 12.4, Section 9.3
**Target**: New Section 15 in merged spec
**Operation**: Add open decisions requiring user input, following Variant A's pattern (owner, deadline, effective phase). Wiring gate specific decisions:

1. `provider_dir_names` configuration -- which directories to scan
2. FPR threshold for soft activation
3. Whitelist governance (who can add entries, review cadence)
4. Shadow window duration (minimum sprints before soft consideration)

### W-005: Document GateResult Naming Resolution

**Source**: Contradiction X-001 from diff analysis
**Target**: Merged spec Section 14 (Decisions), new decision D8
**Operation**: Add a decision record documenting that:

1. The existing `GateResult` in `audit/evidence_gate.py` is unchanged
2. The existing `TrailingGateResult` in `pipeline/trailing_gate.py` is unchanged
3. The wiring gate uses `WiringReport` as its internal model and YAML frontmatter for gate evaluation
4. If a unified lifecycle `GateResult` is built later (from Variant A's design), it should use a distinct name like `TransitionGateResult` to avoid collision

### W-006: Drop Stale Variant A Content

**Source**: Variant A Sections 3.2, 6, 10.2, 11
**Target**: Not included in merged spec
**Operation**: The following Variant A content is excluded:

1. `--strictness` vs `--profile` alias resolution (Section 3.2) -- implementation detail
2. `GateResult` normative schema (Section 6.1) -- conflicts with existing code
3. `OverrideRecord` schema (Section 6.2) -- deferred to lifecycle spec
4. Event schemas (Section 6.3) -- deferred to lifecycle spec
5. `sc-audit-gate` skill file references (Section 10.2) -- nonexistent
6. Checklist closure matrix (Section 11) -- process state
7. Versioning policy (Section 6.4) -- premature for first implementation

### W-007: Add Governance Coordination Note

**Source**: Synthesis from debate
**Target**: Merged spec Section 15 (Coordination Notes), new subsection
**Operation**: Add a note documenting the relationship between the wiring gate and the lifecycle governance framework:

- The wiring gate is one input to lifecycle transition decisions
- The lifecycle state machine (from Variant A) governs whether transitions are permitted
- The wiring gate does not have its own override mechanism -- overrides are handled at the lifecycle level
- The `/sc:audit-gate` command (from Variant A) is a future integration point that would orchestrate multiple gates including the wiring gate

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Governance appendix creates scope creep | Mark as "governance layer" with explicit note that wiring gate implementation does not depend on it |
| Rollback triggers add implementation burden | Adapt to wiring-gate-specific conditions only; drop lifecycle-level triggers |
| Decision tracking section creates bureaucratic overhead | Limit to 4 wiring-gate-specific decisions; no lifecycle decisions |
| GateResult naming resolution is premature | Document as a decision record, not implementation requirement |

---

## Validation Checklist

After merge, verify:

1. All substrate references in the merged spec are from Variant B (verified line numbers)
2. No nonexistent file references remain from Variant A
3. The governance appendix is clearly separated from core implementation sections
4. Rollout section includes adapted rollback triggers
5. Decision tracking section includes only wiring-gate-specific decisions
6. Tasklist (Section 13) is unchanged from Variant B -- governance appendix does not create new implementation tasks
7. The merged spec can generate a tasklist without depending on governance infrastructure being complete
