# Verification Protocol — Release Split Fidelity Audit

> Loaded by Part 4 of sc:release-split-protocol. Do NOT pre-load during earlier parts.

## Purpose

This reference defines the detailed verification checklist for auditing fidelity between an original release artifact and the split (or validated) outputs. The goal is an auditable, traceable proof that 100% of original scope is preserved.

## 6-Point Verification Checklist

### Check 1: Coverage Matrix

Build a complete coverage matrix mapping every discrete item from the original spec to its destination.

**Extraction rules**:
- Extract EVERY discrete requirement, feature, acceptance criterion, constraint, and non-functional requirement
- Include implicit requirements (e.g., "the system must..." buried in descriptions)
- Include edge cases and error handling requirements
- Number each item sequentially (REQ-001, REQ-002, ...)

**Matrix columns**:

| # | Original Requirement | Source Section | Destination | Release | Status | Justification |
|---|---------------------|---------------|-------------|---------|--------|---------------|
| REQ-001 | Description | Section ref | Where it appears in output | R1/R2/Single | Status code | Why |

**Status codes**:
- `PRESERVED` — Requirement appears in output with equivalent scope and meaning
- `TRANSFORMED` — Requirement appears but has been restructured, combined, or rephrased. Justification required explaining why the transformation preserves intent.
- `DEFERRED` — Requirement intentionally moved to a later release. Must be explicitly tracked with a dependency declaration.
- `REMOVED` — Requirement does not appear in any output. CRITICAL finding unless justified (e.g., requirement was already completed, or superseded by another requirement).

**Traceability check**: After building the matrix, scan ALL output items and verify each maps back to a source requirement. Flag any output item that does not trace to an original requirement as SCOPE-CREEP.

### Check 2: Losslessness Analysis

Scan for three categories of change:

**Missing items** (severity: CRITICAL):
- Requirements present in the original but absent from all outputs
- Acceptance criteria that were dropped
- Constraints that were not carried forward
- For each: explain impact and whether it's recoverable

**Weakened items** (severity: WARNING):
- Requirements where scope was reduced (e.g., "must support 10 formats" → "must support 3 formats")
- Acceptance criteria that were relaxed
- Constraints that were softened
- For each: explain the delta and whether it's intentional

**Added items** (severity: INFO or WARNING):
- Requirements in the output that don't trace to the original
- New acceptance criteria or constraints not in the original
- For each: classify as VALID-ADDITION (necessary for split coherence) or SCOPE-CREEP (invented scope)

### Check 3: Fidelity Assessment

Calculate overall fidelity score:

```
fidelity = (PRESERVED + TRANSFORMED_valid) / total_requirements

Where:
- PRESERVED = count of items with status PRESERVED
- TRANSFORMED_valid = count of items with status TRANSFORMED and valid justification
- total_requirements = total items extracted from original

Thresholds:
- 1.0 = Perfect fidelity (all items preserved or validly transformed)
- 0.95-0.99 = Acceptable with minor remediation
- 0.90-0.94 = Requires remediation before proceeding
- < 0.90 = Split should be revised or abandoned
```

If fidelity < 1.0, produce a remediation list with:
- Each gap item
- Which release it should be added to
- Priority (CRITICAL / HIGH / MEDIUM)
- Suggested wording

### Check 4: Boundary Integrity (Split Only)

For each item assigned to Release 1:
- Verify it belongs in Release 1 per the split rationale
- Verify it does not depend on Release 2 deliverables
- Flag any item that should be in Release 2

For each item assigned to Release 2:
- Verify it was intentionally deferred (not accidentally dropped)
- Verify its dependencies on Release 1 are explicitly declared
- Flag any item that should be in Release 1

**Boundary violation categories**:
- `MISPLACED-R1`: Item in Release 1 that belongs in Release 2
- `MISPLACED-R2`: Item in Release 2 that should be in Release 1
- `MISSING-DEPENDENCY`: Release 2 item depends on something not in Release 1
- `CIRCULAR-DEPENDENCY`: Items that create cross-release dependency cycles

### Check 5: Release 2 Planning Gate Verification (Split Only)

Verify that the Release 2 spec contains an explicit planning gate statement equivalent to:

> Release 2 roadmap/tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.

**Gate requirements**:
- The gate must be present in Release 2 spec (not just in the proposal)
- The gate must specify what "real-world validation" means for Release 1
- The gate must specify who reviews the results
- The gate must specify what happens if validation fails (rollback? revision?)

If the gate is missing or incomplete, flag as CRITICAL finding.

### Check 6: Real-World Validation Audit

Scan all validation, testing, and verification items across all outputs:

**Pass criteria**: Every validation item must describe real-world usage scenarios. Specifically:
- Uses actual functionality in production-like conditions
- Involves real data flows, real user interactions, or real system integration
- Produces observable results that can be verified by a human

**Fail criteria**: Flag any item that:
- Mentions "mock", "simulate", "fake", "stub", or "synthetic" as a testing approach
- Describes unit tests or integration tests as sufficient validation (these are necessary but not sufficient)
- Uses abstract language without specifying concrete scenarios (e.g., "validate the system works" without saying how)
- Relies on automated test suites alone without human verification of real-world behavior

For each flagged item, suggest a real-world validation replacement.

## Output Template

```markdown
# Fidelity Audit Report

## Verdict: [VERIFIED / VERIFIED WITH REQUIRED REMEDIATION / NOT VERIFIED]

## Summary
- Total requirements extracted: N
- Preserved: N (X%)
- Transformed (valid): N (X%)
- Deferred: N (X%)
- Missing: N (X%)  [CRITICAL if > 0]
- Weakened: N (X%) [WARNING]
- Added (valid): N
- Added (scope creep): N [WARNING if > 0]
- Fidelity score: X.XX

## Coverage Matrix
[Full matrix table]

## Findings by Severity

### CRITICAL
[Missing items, removed items without justification]

### WARNING
[Weakened items, scope creep, incomplete gates]

### INFO
[Valid additions, transformations, notes]

## Boundary Integrity [Split Only]
[Misplaced items, dependency issues]

## Planning Gate Status [Split Only]
[Gate present/absent, completeness assessment]

## Real-World Validation Status
[Flagged items, suggested replacements]

## Remediation Required
[Ordered list of items to fix before proceeding]

## Sign-Off
[Either:]
"All N requirements from [original spec] are represented across Release 1 and Release 2 with full fidelity."
[Or:]
"Fidelity gaps found — N items require remediation before proceeding."
```
