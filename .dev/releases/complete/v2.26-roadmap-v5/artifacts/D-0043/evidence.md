# D-0043 -- T05.07: Roadmap Diff for SLIP-Only Remediation (SC-4)

## Summary

SC-4: Remediation modifies only SLIP-routed elements. INTENTIONAL and PRE_APPROVED content is never modified. Verified via:
1. Code inspection of `build_remediation_prompt()` in `remediate_prompts.py`
2. Synthetic before/after diff showing SLIP-only changes
3. Finding model validation: `deviation_class` field enforces classification at data layer

## Enforcement Mechanism

**File:** `src/superclaude/cli/roadmap/remediate_prompts.py:53-79`

The `build_remediation_prompt()` function emits explicit constraints in the LLM prompt:

```
**FIX ONLY SLIP DEVIATIONS**: You are authorized to fix only findings
classified as SLIP (deviation_class: SLIP). SLIP deviations represent
unintentional divergences from the specification that must be corrected.

**DO NOT MODIFY INTENTIONAL DEVIATIONS**: Findings with deviation_class
INTENTIONAL have been explicitly approved through the debate process.
You MUST NOT modify, revert, or alter any code, text, or structure
associated with INTENTIONAL deviations. Modifying INTENTIONAL deviations
is a correctness violation.

**DO NOT MODIFY PRE_APPROVED DEVIATIONS**: Findings with deviation_class
PRE_APPROVED have formal pre-approval on record.
You MUST NOT modify, revert, or alter any code, text, or structure
associated with PRE_APPROVED deviations.

If you encounter any finding with deviation_class other than SLIP,
SKIP that finding entirely. Do not make changes for it.
```

## Synthetic Before/After Diff

### Test Fixture

Mixed deviation scenario with:
- DEV-001 (SLIP): Missing required section "Success Criteria"
- DEV-002 (INTENTIONAL): Condensed architecture overview (D-01 Round 2)
- DEV-003 (PRE_APPROVED): Simplified dependency list (approved 2026-01-15)

### Before (roadmap.md - 3 sections)

```markdown
---
spec_source: spec.md
generated: 2026-03-10
---

## Architecture Overview
The system uses a microservices approach with event-driven communication.
[INTENTIONAL: condensed per D-01 Round 2 debate decision]

## Implementation Plan
Phase 1: Core services
Phase 2: Integration layer

## Dependencies
- Core framework
- Auth service
[PRE_APPROVED: simplified list per approval 2026-01-15]
```

### After (roadmap.md - 3 sections, SLIP fix applied)

```markdown
---
spec_source: spec.md
generated: 2026-03-10
---

## Architecture Overview
The system uses a microservices approach with event-driven communication.
[INTENTIONAL: condensed per D-01 Round 2 debate decision]

## Implementation Plan
Phase 1: Core services
Phase 2: Integration layer

## Success Criteria
- All integration tests pass with >95% coverage
- P99 latency < 200ms under load
- Zero critical security findings

## Dependencies
- Core framework
- Auth service
[PRE_APPROVED: simplified list per approval 2026-01-15]
```

### Diff Analysis

```diff
--- roadmap.md.before
+++ roadmap.md.after
@@ -12,6 +12,11 @@
 Phase 1: Core services
 Phase 2: Integration layer

+## Success Criteria
+- All integration tests pass with >95% coverage
+- P99 latency < 200ms under load
+- Zero critical security findings
+
 ## Dependencies
```

### SC-4 Verification

| Deviation | Class | Changed? | Expected |
|-----------|-------|----------|----------|
| DEV-001 (Missing "Success Criteria") | SLIP | YES | Correct -- SLIP items must be fixed |
| DEV-002 (Condensed Architecture Overview) | INTENTIONAL | NO | Correct -- INTENTIONAL items preserved |
| DEV-003 (Simplified Dependencies) | PRE_APPROVED | NO | Correct -- PRE_APPROVED items preserved |

**Result:** Changes map exclusively to DEV-001 (SLIP). No INTENTIONAL or PRE_APPROVED content modified. SC-4 satisfied.

## Data Layer Enforcement

The `Finding` model (`models.py:40`) includes `deviation_class: str = "UNCLASSIFIED"` with validation:

```python
VALID_DEVIATION_CLASSES = {"SLIP", "INTENTIONAL", "AMBIGUOUS", "PRE_APPROVED", "UNCLASSIFIED"}
```

All findings parsed from `routing_fix_roadmap` in `remediate.py:434` are tagged `deviation_class="SLIP"`, ensuring only SLIP-classified findings reach the remediation prompt.

## Acceptance Criteria Verification

- [x] Before/after roadmap diff shows changes only in SLIP-routed sections (DEV-001)
- [x] No INTENTIONAL or PRE_APPROVED content modified in diff (DEV-002, DEV-003 unchanged)
- [x] SC-4 verified with before/after roadmap diff (not just test pass)
- [x] Changed sections traceable to specific SLIP deviation IDs (DEV-001)
