# Refactoring Plan: Forensic Spec Quick Mode + Task-Unified Integration

## Overview
- **Base variant**: Variant A (forensic-refactor-handoff.md) — architectural framework
- **Incorporated variant**: Variant B (tfep-refactoring-context.md) — tactical specifications
- **Total planned changes**: 11 incorporations + 2 invariant resolutions
- **Overall risk**: Medium
- **Output type**: Tasklist (per --generate tasklist)

---

## Planned Changes

### Change #1: Incorporate per-phase behavior table
- **Source**: Variant B, Section 3.1
- **Target**: Merged output, Section "Quick Mode Phase Behavior"
- **Rationale**: Debate point C-002, 80% confidence for B. Phase table is directly actionable vs A's conceptual descriptions.
- **Integration approach**: Insert as new section, preserving A's three-tier model naming.
- **Risk**: Low (additive)

### Change #2: Incorporate binary escalation thresholds
- **Source**: Variant B, Section 4
- **Target**: Merged output, Section "Escalation Threshold Rules"
- **Rationale**: Debate point C-004, 75% confidence for B. Binary rules are LLM-enforceable.
- **Integration approach**: Merge B's binary entry-gate thresholds with A's qualitative within-TFEP escalation triggers.
- **Risk**: Low (additive, complementary)

### Change #3: Incorporate token budget estimates
- **Source**: Variant B, Section 3.1
- **Target**: Merged output, task descriptions
- **Rationale**: Debate point C-003, 85% confidence for B. A has no estimates.
- **Integration approach**: Append token estimates to relevant tasks.
- **Risk**: Low (additive)

### Change #4: Incorporate two-phase implementation strategy
- **Source**: Variant B, Section 8
- **Target**: Merged output, tasklist phasing structure
- **Rationale**: Debate point C-008, 82% confidence for B. Delivers immediate value.
- **Integration approach**: Structure tasklist into Phase 1 (immediate guard) and Phase 2 (full integration).
- **Risk**: Low (additive)

### Change #5: Incorporate YAML context interface
- **Source**: Variant B, Section 3.3
- **Target**: Merged output, Section "Caller Context Interface"
- **Rationale**: Debate point C-007, 78% confidence for B. Schema > bullet list.
- **Integration approach**: Include as specification within coupling contract tasks.
- **Risk**: Low (additive)

### Change #6: Incorporate section-by-section change mapping
- **Source**: Variant B, Section 6
- **Target**: Merged output, forensic spec refactoring tasks
- **Rationale**: Debate point C-009, 80% confidence for B. A has no mapping.
- **Integration approach**: Convert section mapping into discrete tasks.
- **Risk**: Low (additive)

### Change #7: Incorporate "test is wrong" valid outcome
- **Source**: Variant B, Section 9
- **Target**: Merged output, TFEP behavioral rules
- **Rationale**: Debate point C-010, 75% confidence for B. Prevents infinite remediation.
- **Integration approach**: Add as explicit rule in TFEP specification tasks.
- **Risk**: Low (additive)

### Change #8: Incorporate artifact directory tree
- **Source**: Variant B, Section 3.5
- **Target**: Merged output, artifact specification tasks
- **Rationale**: U-007, Medium value. Directly implementable directory structure.
- **Integration approach**: Include as specification within artifact tasks.
- **Risk**: Low (additive)

### Change #9: Incorporate user-approved decision log
- **Source**: Variant B, Section 9
- **Target**: Merged output, constraints section
- **Rationale**: 9 explicit user decisions provide authoritative constraints for planning agent.
- **Integration approach**: Include as constraints reference in tasklist preamble.
- **Risk**: Low (additive)

### Change #10: Resolve INV-001 — test baseline mechanism
- **Source**: Invariant probe
- **Target**: Merged output, new task for baseline snapshot
- **Rationale**: HIGH-severity unaddressed invariant. Neither variant specifies how to distinguish pre-existing from agent-written tests.
- **Integration approach**: Add task requiring test baseline snapshot before implementation begins.
- **Risk**: Medium (new requirement not in either variant)

### Change #11: Resolve INV-004 — artifact/tasklist compatibility
- **Source**: Invariant probe
- **Target**: Merged output, new task for format specification
- **Rationale**: HIGH-severity unaddressed invariant. Forensic output must be parseable by task-unified.
- **Integration approach**: Add task requiring explicit format specification for tasklist insertion.
- **Risk**: Medium (new requirement not in either variant)

---

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|--------------------------|
| C-001 (flag model) | B: Reuse `--depth` for pipeline control | A's 3-axis model is architecturally cleaner; B's P-002 evidence is about precedence within existing `--depth`, not about overloading it with new semantics. X-001 debate: A wins at 60%. |
| U-002 (--caller flag) | N/A (A-only contribution) | Preserved in base as-is |
| U-003 (profiles abstraction) | N/A (A-only contribution) | Preserved in base as-is |

---

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1-#9 | Low | Additive — enriches base without modifying architecture | Remove section |
| #10 (INV-001) | Medium | New requirement — may affect task-unified's pre-implementation flow | Remove task |
| #11 (INV-004) | Medium | New requirement — adds format specification work | Remove task |

---

## Review Status
- Approval: auto-approved
- Timestamp: 2026-03-19T00:00:00Z
