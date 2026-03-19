# Refactoring Plan: Merge Solution C Design Specs

## Overview
- **Base**: Variant A (Integration Plan) — score 0.918
- **Incorporated**: Variant B (idempotency, charset), Variant C (function body, edge cases)
- **Planned changes**: 6
- **Risk**: Low (all additive changes to an already-complete document)

---

## Planned Changes

### Change #1: Replace lstrip charset throughout
- **Source**: Variant B, Section 2.3
- **Target**: Base Section 1 (Fix 1 and Fix 2 code blocks)
- **Rationale**: Debate consensus (X-001, 90% confidence). Explicit `.lstrip("\n\r\t ")` is more principled than bare `.lstrip()`.
- **Integration approach**: Replace all instances of `.lstrip()` and `.lstrip("\n\r")` with `.lstrip("\n\r\t ")`
- **Risk**: Low

### Change #2: Add idempotency guards to Fix 2
- **Source**: Variant B, Section 3
- **Target**: Base Section 1, Fix 2 subsection
- **Rationale**: Debate consensus (C-004, 95% confidence). Retry scenarios can produce duplicate YAML keys.
- **Integration approach**: Replace the one-liner `_inject_provenance_fields` fix with B's field-existence-check implementation
- **Risk**: Low

### Change #3: Replace _sanitize_output code with full function body
- **Source**: Variant C, Section 2 (minimal fix version)
- **Target**: Base Section 1, Fix 1 subsection
- **Rationale**: Debate consensus (C-002, 85% confidence). Full function body is more implementable than diff fragments.
- **Integration approach**: Replace the "Proposed code" snippet with C's complete function, updating charset to `.lstrip("\n\r\t ")`
- **Risk**: Low

### Change #4: Add idempotency guard for _inject_pipeline_diagnostics
- **Source**: Variant B, Section 2.2 + Section 5.2
- **Target**: Base Section 5 (Implementation Checklist), Phase 1 audit item
- **Rationale**: Consistency with Change #2. Same retry risk exists for diagnostics injection.
- **Integration approach**: Add code and tests for diagnostics idempotency alongside provenance idempotency
- **Risk**: Low

### Change #5: Expand edge case table
- **Source**: Variant C, Section 3 + Variant B, Section 4
- **Target**: New section in merged document between Section 1 and Section 2
- **Rationale**: C-002, C-003. Consolidated edge case table aids implementer understanding.
- **Integration approach**: Merge B and C edge case tables, deduplicate, add byte count column
- **Risk**: Low

### Change #6: Add Variant B's provenance test code
- **Source**: Variant B, Section 5.1
- **Target**: Base Section 2.2 (TestInjectProvenanceFieldsLeadingWhitespace)
- **Rationale**: B's tests include idempotency tests (test_idempotent_double_call, test_partial_provenance_present) which A lacks
- **Integration approach**: Replace A's 4-test table with B's 8-test class (full pytest code)
- **Risk**: Low

---

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Rejecting |
|------------|-------------------|------------------------|
| S-002 | C's three-version code progression (initial → simplified → minimal) | Confusing; merged doc uses only the final minimal version |
| C-007 | B's reliance on write_text for atomicity | A's explicit tmp+os.replace pattern is safer and already in the codebase |
| U-005 | B's false positive analysis for substring matching | Acknowledged as acceptable risk; not worth complicating the implementation |

---

## Risk Summary

All 6 changes are LOW risk. They are additive to the base document's structure. No existing content is removed — only replaced with more detailed/correct versions.

## Review Status
- Approval: auto-approved
- Timestamp: 2026-03-18
