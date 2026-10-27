# Patch Checklist
Generated: 2026-03-20
Total edits: 11 across 4 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] T01.01: Add conservative default `provider_dir_names` to acceptance criteria (from finding M1)
  - [ ] T01.02: Expand parse degradation acceptance to include structured observability event details and `analysis_complete` propagation (from finding M2)

- phase-2-tasklist.md
  - [ ] T02.02: Soften field name references to trace to T02.01 decision record (from finding M3)
  - [ ] T02.03: Replace `wiring_gate_mode` with `resolve_gate_mode()`-compatible config inputs (from finding H1)
  - [ ] T02.04: Add helper functions to deliverables and cross-reference null-ledger split to T02.07 (from finding M4)
  - [ ] T02.08: Replace `can_run_wiring_gate()` test with tracking test; fix "reimbursement consumed" terminology (from findings H2, M5)

- phase-3-tasklist.md
  - [ ] T03.01: Remove invented "floor-to-zero surfaced in KPI" from acceptance (from finding L1)
  - [ ] T03.02: Add "SC-008 validated" to acceptance criteria (from finding M6)

- phase-5-tasklist.md
  - [ ] T05.01: Expand baseline evaluation acceptance to explicitly list all 4 items (from finding M7)
  - [ ] T05.02: Strengthen FPR criterion to "manageable through `wiring_whitelist.yaml`" (from finding H3)

## Cross-file consistency sweep
- [ ] Verify all acceptance criteria changes remain consistent with Deliverable Registry in tasklist-index.md
- [ ] Verify no checkpoint exit criteria are invalidated by acceptance changes

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### T01.01 Acceptance Criteria

**A. Add provider_dir_names defaults (M1)**
Current issue: Acceptance doesn't mention conservative defaults for `provider_dir_names`
Change: Add 5th acceptance bullet (expanding to mention specific defaults)
Diff intent: After the 4th acceptance bullet about `whitelist_entries_applied`, add: "- `WiringConfig` provides conservative default `provider_dir_names`: `steps/`, `handlers/`, `validators/`, `checks/` (R6 mitigation)"

#### T01.02 Acceptance Criteria

**B. Expand parse degradation details (M2)**
Current issue: Bullet 4 says "Parse errors are caught per-file with structured warning emission; `files_skipped` count is accurate (NFR-002)" but omits `analysis_complete` propagation
Change: Expand bullet 4 to include full observability chain
Diff intent: Replace "Parse errors are caught per-file with structured warning emission; `files_skipped` count is accurate (NFR-002)" with "Parse errors emit structured warning with file path, parse reason, and files-skipped count (NFR-002); `analysis_complete` reflects whether all files parsed successfully; `files_skipped: N` propagated to report frontmatter"

### 2) phase-2-tasklist.md

#### T02.02 Steps

**C. Soften field names (M3)**
Current issue: Step 3 hard-codes field names not in roadmap
Change: Add qualifier that names are per T02.01 resolution
Diff intent: Change "Add 3 new fields to TurnLedger dataclass: `wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted`, all defaulting to 0" to "Add 3 new fields to TurnLedger dataclass (names per T02.01 decision record, e.g. `wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted`), all defaulting to 0"

#### T02.03 Steps and Acceptance

**D. Replace wiring_gate_mode (H1)**
Current issue: Step 3 adds `wiring_gate_mode` which contradicts `resolve_gate_mode()` architecture
Change: Replace `wiring_gate_mode` with config inputs for `resolve_gate_mode()`
Diff intent: In Step 3, change "Add 3 SprintConfig fields: `wiring_gate_mode`, `wiring_analysis_turns`, `remediation_cost`" to "Add 3 SprintConfig fields: `wiring_gate_scope`, `wiring_analysis_turns`, `remediation_cost` (inputs to `resolve_gate_mode()` per Goal-5d)"

#### T02.04 Deliverables and Notes

**E. Add helper functions and null-ledger cross-reference (M4)**
Current issue: Missing FR: T07b-f (helper functions) and null-ledger traceability
Change: Add helper functions to deliverables; add note about null-ledger split
Diff intent: After the existing deliverable, add note text: "Helper functions required by the hook are included (FR: T07b-f). Null-ledger compatibility is split to T02.07 per FR: T07b-e."

#### T02.08 Steps and Acceptance

**F. Fix test scope and terminology (H2, M5)**
Current issue: Third test is `can_run_wiring_gate()` instead of tracking; "Reimbursement consumed" is not roadmap terminology
Change: Replace test and fix terminology
Diff intent:
- Step 4: Change "Write test: `can_run_wiring_gate()` returns False when budget exhausted, True otherwise" to "Write test: sequential `debit_wiring()`/`credit_wiring()` cycle correctly tracks cumulative budget consumption"
- Acceptance bullet 2: Change "Reimbursement consumed tracking validated (SC-013)" to "`debit_wiring`/`credit_wiring` tracking validated (SC-013)"
- Acceptance bullet 1: Change "3 TurnLedger tests exist validating debit/credit/budget-check semantics" to "3 TurnLedger tests exist validating `debit_wiring`/`credit_wiring` tracking semantics"

### 3) phase-3-tasklist.md

#### T03.01 Acceptance

**G. Remove invented requirement (L1)**
Current issue: "Floor-to-zero credit behavior surfaced in KPI output for operator visibility (R7)" is not a Phase 3 acceptance criterion
Change: Remove this bullet
Diff intent: Remove acceptance bullet "Floor-to-zero credit behavior surfaced in KPI output for operator visibility (R7)" from T03.01

#### T03.02 Acceptance

**H. Add SC-008 (M6)**
Current issue: Missing explicit SC-008 validation requirement
Change: Add SC-008 to acceptance
Diff intent: Add acceptance bullet: "SC-008 validated: deviation count reconciliation produces deterministic gate failure on mismatch"

### 4) phase-5-tasklist.md

#### T05.01 Acceptance

**I. Expand baseline criteria (M7)**
Current issue: Compressed evaluation items
Change: Expand to match roadmap's 4 explicit items
Diff intent: Replace "Findings volume, whitelist usage, and zero-findings anomalies documented" with "Findings volume per analysis run evaluated; whitelist usage and coverage assessed; zero-findings anomalies (SC-011 warnings) documented; p95 runtime under real workloads measured"

#### T05.02 Acceptance

**J. Strengthen FPR criterion (H3)**
Current issue: "FPR burden documented" is weaker than roadmap's promotion criterion
Change: Require manageability through whitelist
Diff intent: Replace "FPR burden documented: whitelist adequacy assessed against real finding data" with "False-positive rate shown to be manageable through `wiring_whitelist.yaml` with evidence from real finding data (promotion criterion per Goal-5b)"

## Suggested execution order (highest-impact first)
1. phase-2-tasklist.md (4 edits including 2 High-severity)
2. phase-5-tasklist.md (2 edits including 1 High-severity)
3. phase-1-tasklist.md (2 Medium edits)
4. phase-3-tasklist.md (2 Low/Medium edits)
