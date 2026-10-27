# Patch Checklist
Generated: 2026-03-20
Total edits: 7 across 4 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] T01.06: Add ParseWarning population test to acceptance criteria (from H1)

- phase-3-tasklist.md
  - [ ] T03.01: Expand D-0018 RunMetadata to list all 7 fields (from M2)
  - [ ] T03.03: Expand prior findings summary to include field names ID/severity/status/run_number (from M3)

- phase-4-tasklist.md
  - [ ] T04.03: Add token budget cap and YAML parse failure acceptance criteria (from H2)

- phase-5-tasklist.md
  - [ ] T05.03: Add SPEC_FIDELITY_GATE exclusion acceptance criterion (from M4)

- phase-6-tasklist.md
  - [ ] T06.01: Add cross-file coherence check step and snapshot/restore retention (from M5, M6)
  - [ ] T06.08: Fix OQ numbering to OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6 (from M7)

## Cross-file consistency sweep
- [ ] Verify all patched tasks still have exactly 4 acceptance criteria bullets
- [ ] Verify no deliverable ID changes from patches

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### Section: T01.06 Acceptance Criteria
**A. Add ParseWarning test criterion (H1)**
Current issue: Acceptance criteria missing ParseWarning population test
Change: Add 4th criterion about ParseWarning
Diff intent: After "Section splitting round-trip test passes", add: "- `ParseWarning` entries produced and correctly populated for malformed YAML, irregular tables, and missing language tags"

### 2) phase-3-tasklist.md

#### Section: T03.01 Deliverables (D-0018)
**B. Expand RunMetadata field list (M2)**
Current issue: D-0018 says "structural_high_count, semantic_high_count, total_high_count" only
Change: Prepend missing fields
Diff intent: Replace "Run metadata with `structural_high_count`, `semantic_high_count`, `total_high_count`" with "Run metadata (`RunMetadata`) with `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`, `structural_high_count`, `semantic_high_count`, `total_high_count`"

#### Section: T03.03 Deliverables
**C. Add prior findings field names (M3)**
Current issue: Says "prior findings summary (max 50, oldest-first truncation)" without field names
Change: Add field names
Diff intent: Replace "prior findings summary (max 50, oldest-first truncation)" with "prior findings summary (ID, severity, status, run_number per finding; max 50, oldest-first truncation)"

### 3) phase-4-tasklist.md

#### Section: T04.03 Acceptance Criteria
**D. Add token budget and YAML parse failure (H2)**
Current issue: Missing token budget cap and YAML failure behavior
Change: Add two acceptance criteria items (replace existing generic ones or append)
Diff intent: After "Conservative tiebreak: margin within +/-0.15 always produces CONFIRM_HIGH", add: "- Token budget per finding ~3,800 (hard cap: 5,000)" and "- YAML parse failure for either side defaults all rubric scores to 0"

### 4) phase-5-tasklist.md

#### Section: T05.03 Acceptance Criteria
**E. Add SPEC_FIDELITY_GATE exclusion (M4)**
Current issue: Doesn't mention SPEC_FIDELITY_GATE exclusion in convergence mode
Change: Add to acceptance criteria
Diff intent: After "Convergence result mapped to `StepResult` for pipeline compatibility", add: "- In convergence mode, `SPEC_FIDELITY_GATE` is NOT invoked; `DeviationRegistry` is sole pass/fail authority"

### 5) phase-6-tasklist.md

#### Section: T06.01 Steps and Acceptance Criteria
**F. Add cross-file coherence and snapshot retention (M5, M6)**
Current issue: Missing cross-file coherence check and snapshot/restore retention
Change: Add step for coherence check; add acceptance criterion for snapshot retention
Diff intent: After step 5 "Implement per-file rollback", add step: "Implement post-execution cross-file coherence check: evaluate rollback of successful files when related files fail". Add acceptance criterion: "Existing snapshot/restore mechanism (create_snapshots/restore_from_snapshots/cleanup_snapshots) retained"

#### Section: T06.08 Deliverables
**G. Fix OQ numbering (M7)**
Current issue: Says "OQ-1 through OQ-5" but roadmap lists OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6
Change: Replace OQ range with explicit list
Diff intent: Replace "OQ-1 through OQ-5" with "OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6" and expand deliverable text accordingly
