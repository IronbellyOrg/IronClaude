# Refactoring Plan — Apply Option B to Resolve OQ-1

## Overview

- **Base**: Option B (Helper Uppercases Input)
- **Incorporated from non-base**: NONE (B subsumes A's Test 1 wrapper change; C's contribution is rejected as scope-expansion)
- **Total changes planned**: 2 edits to TASK-RF-20260526-102600.md + 1 edit to merged-output.md
- **Risk**: Low (single-word production change; verified by 3 independent regex traces; unanimous adversarial concession)

## Planned Changes

### Change 1 — Update merged-output.md helper code

**Source**: Option B Part 1.
**Target**: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/merged-output.md`, the helper code block in Step 2.
**Approach**: Replace the helper's first body line.
**Rationale**: Make the upstream merged-output spec internally consistent so future readers don't hit the same OQ-1.

```python
# BEFORE (line in Step 2):
base_tokens = _extract_identifiers(text)

# AFTER:
base_tokens = _extract_identifiers(text.upper())
```

**Risk**: Low — documentation-side change only; the spec is being updated to match the chosen implementation.

### Change 2 — Update task file Step 2.5 (helper definition)

**Source**: Option B Part 1.
**Target**: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260526-102600/TASK-RF-20260526-102600.md`, Step 2.5 item (the helper definition).
**Approach**: Update the Action portion to specify `_extract_identifiers(text.upper())` rather than `_extract_identifiers(text)`.
**Rationale**: The task-builder copied verbatim from merged-output.md; updating it ensures the executor lands the correct code.

**Risk**: Low — task-file edit only.

### Change 3 — Update task file Step 2.1 (Test 1)

**Source**: Option B Part 2 (shared with Option A).
**Target**: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260526-102600/TASK-RF-20260526-102600.md`, Step 2.1 item (Test 1 pin test).
**Approach**: Update the Action to use `_canonicalize_identifiers("FR-S10-02") == frozenset({"FR-S10-02", "S10"})` instead of `set(_extract_identifiers("FR-S10-02")) == {"FR-S10-02", "S10"}`.
**Rationale**: Consistency with Tests 2-4 (all use `_canonicalize_identifiers`); also Test 1 wouldn't pass otherwise because `_extract_identifiers` is unmodified.

**Risk**: Low.

### Change 4 — Mark OQ-1 resolved in task file Open Questions

**Source**: Outcome of this adversarial debate.
**Target**: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260526-102600/TASK-RF-20260526-102600.md`, `## Open Questions` section.
**Approach**: Update OQ-1 with a `**RESOLVED 2026-05-26 via adversarial debate**` annotation pointing to this debate's artifacts directory.
**Rationale**: Audit trail.

**Risk**: None.

### Change 5 — Re-run rf-qa-qualitative to validate the resolution

**Source**: Standard task-builder A.10.5 protocol.
**Target**: spawn rf-qa-qualitative again with `fix_authorization: true`.
**Approach**: Verify the task-file changes resolve OQ-1 and the all-PASS verdict holds.
**Rationale**: Defense-in-depth — the same gate that caught the defect should confirm the fix.

**Risk**: Low (re-verification only).

## Changes NOT Being Made (and why)

- **Option C's modification of `_extract_identifiers`**: rejected. C alone doesn't fix Test 2; combining C with B's `.upper()` is strictly more scope than B alone; violates the V1/V2/V3 adversarial decision to preserve `_extract_identifiers` as a public contract.
- **Pure Option A (test-only, no helper change)**: rejected. Test 2 would still fail, blocking Phase 3.1's RED→GREEN verification gate and Phase 4.1's rf-qa final gate. Merged-output's Test Plan claim of "GREEN after Steps 2-4" requires Option B.
- **Drop or weaken Test 2**: not considered — would silently abandon the helper's docstring invariant 1 ("All tokens are uppercase") which is normative per the design intent.

## Risk Summary

| Change | Risk | Mitigation | Rollback |
|--------|------|-----------|----------|
| Change 1 (merged-output.md spec) | Low | Documentation-side; the canonical spec gets updated to match implementation | Revert single line |
| Change 2 (task Step 2.5) | Low | Surgical edit to the Action portion | Revert single edit |
| Change 3 (task Step 2.1) | Low | Surgical edit | Revert single edit |
| Change 4 (OQ-1 annotation) | None | Audit-trail only | n/a |
| Change 5 (re-run qa-qualitative) | Low | Re-verification step | Run again with adjustments if it surfaces new issues |

## Review Status

Auto-approved (non-interactive mode). User explicitly authorized the path via "Spawn a parallel agent to engage in an adversarial debate to validate the proposed solution. Ingest the results of the debate and either refactor accordingly or implement as is if validated." The debate validated Option B unanimously.
