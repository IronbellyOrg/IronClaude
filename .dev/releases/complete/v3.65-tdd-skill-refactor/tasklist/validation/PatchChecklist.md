# Patch Checklist
Generated: 2026-04-03
Total edits: 5 across 2 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] Add "Actor" column to T01.06 acceptance criteria (from finding M1)
  - [ ] Remove "extraction" from T01.07 Why field (from finding L1)
  - [ ] Add loading contract verification to End of Phase 1 checkpoint (from finding H1)
- phase-3-tasklist.md
  - [ ] Add FR-TDD-R.5c/d to T03.03 acceptance criteria (from finding M2)
  - [ ] Add FR-TDD-R.5c/d to End of Phase 3 checkpoint verification (from finding M2)

## Cross-file consistency sweep
- [ ] Verify no other checkpoints reference the loading contract without the fix from H1

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### A. T01.06 acceptance criteria — add Actor column (M1)
Current issue: Missing "Actor" column reference
Change: Update second acceptance criteria bullet
Diff intent:
  Before: "Every phase has explicit declared loads and forbidden loads columns"
  After: "Every phase has explicit Phase, Actor, Declared Loads, and Forbidden Loads columns matching the roadmap table schema"

#### B. T01.07 Why field — remove "extraction" (L1)
Current issue: Scope narrowed by "extraction" qualifier
Change: Remove "extraction" from Why field
Diff intent:
  Before: "The corrected fidelity index becomes the authoritative mapping for all subsequent extraction phases. Block ranges must be aligned to the spec baseline (1,364)."
  After: "The corrected fidelity index becomes the authoritative mapping for all subsequent phases. Block ranges must be aligned to the spec baseline (1,364)."

#### C. End of Phase 1 checkpoint — add loading contract bullet (H1)
Current issue: Missing loading contract verification
Change: Add fourth verification bullet
Diff intent:
  Before (3 verification bullets):
    "- Corrected fidelity index covers lines 1-1364..."
    "- Every block's checksum markers..."
    "- OQ-1 through OQ-5..."
  After (4 verification bullets — insert after OQ line):
    "- Corrected fidelity index covers lines 1-1364..."
    "- Every block's checksum markers..."
    "- OQ-1 through OQ-5..."
    "- Phase loading contract matrix documented and available for cross-checking"

### 2) phase-3-tasklist.md

#### D. T03.03 acceptance criteria — add FR-TDD-R.5c/d (M2)
Current issue: Missing explicit requirement ID references
Change: Add fifth acceptance criteria bullet
Diff intent:
  Before (4 acceptance criteria bullets ending with):
    "- Evidence records the full diff output with change classification"
  After (add new bullet):
    "- Evidence records the full diff output with change classification"
    "- FR-TDD-R.5c and FR-TDD-R.5d acceptance criteria met per roadmap verification gate"

#### E. End of Phase 3 checkpoint — add FR-TDD-R.5c/d (M2)
Current issue: Missing FR-TDD-R.5c/d in checkpoint verification
Change: Add fourth verification bullet
Diff intent:
  Before (3 verification bullets):
    "- All 6 path-reference updates applied and verified"
    "- Zero original section-name references remain..."
    "- Diff against source Block B12 shows exactly 6 allowlisted changes"
  After (add new bullet):
    "- All 6 path-reference updates applied and verified"
    "- Zero original section-name references remain..."
    "- Diff against source Block B12 shows exactly 6 allowlisted changes"
    "- FR-TDD-R.5c and FR-TDD-R.5d acceptance criteria met"
