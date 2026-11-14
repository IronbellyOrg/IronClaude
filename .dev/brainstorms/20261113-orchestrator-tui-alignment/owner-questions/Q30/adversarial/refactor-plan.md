# Refactoring Plan: Merge into Base (Variant 3, proposal-C)

## Overview
- Base: Variant 3 (proposal-C)
- Incorporating strengths from: Variant 1 (proposal-A), Variant 2 (proposal-B)
- Planned changes: 3
- Risk level: Low

## Planned Changes

### Change 1: Read while the question is pending (from Variant 2 and Variant 3 advocates)
- **Target**: Base steps 1 and 3 (restructure order). **Rationale**: V3 concession 3; V2 concession 3; E-18 non-diagnostic precedent (ADJ `:144`). **Risk**: Low.

### Change 2: Loss detection by ground truth (from Variant 2, U-002, grounded by Variant 3)
- **Target**: Base step 3 (append). **Rationale**: A-002 (all QUALIFY); plain `check` consumes (ADJ `:97`). **Risk**: Low.

### Change 3: Holder-terminal preflight and written fallback (from Variant 1)
- **Target**: new step 1 and new fallback line. **Rationale**: A-001; OB-04 (4) (`merged-requirements.md:252`). **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale |
|---|---|---|
| C-002, X-003 | V2: use an existing real Run to save setup | conflicts with OB-04 (1) (X-002, 97%) and risks a real question (X-001, 95%) |
| V1 as the answer | hold indefinitely | kept only as the fallback |

## Review Status
- [x] Auto-approved (default). Approved by: auto. Timestamp: 2026-11-14T03:10Z
