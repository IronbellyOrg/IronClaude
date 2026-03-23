# Patch Checklist

Generated: 2026-03-20
Total edits: 5 across 2 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] Add OQ-009 to T01.01 deliverables, steps, and acceptance criteria (from finding M1)
  - [ ] Add "(FR-MOD1.6)" annotation to T01.02 step 3 (from finding L1)
  - [ ] Change T01.09 acceptance criterion from "never raises exceptions" to "without blocking the pipeline" (from finding L3)
- phase-3-tasklist.md
  - [ ] Add `wiring_gate_mode` no-interaction acceptance criterion to T03.03 (from finding M5)
  - [ ] Add cli-portify regression criterion to End of Phase 3 checkpoint (from finding L5)

## Cross-file consistency sweep

- [ ] Verify T01.01 "five OQs" count is consistent in mid-phase checkpoint text (line 270)

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### T01.01 -- OQ-009 addition (M1)

**A. Deliverables section**
Current issue: Deliverable 1 lists OQ-003, OQ-004, OQ-005, OQ-010 only
Change: Add OQ-009 (global vs contract-specific matching deferral per roadmap line 63)
Diff intent: After "OQ-005 (defense-in-depth...)" add ", OQ-009 (global pattern matching in Phase 1; contract-specific matching deferred)"

**B. Steps section**
Current issue: Steps 3-6 cover four OQs only
Change: Add step for OQ-009 resolution documentation
Diff intent: Add step between current step 5 and step 6: "**[EXECUTION]** Document OQ-009 resolution: Phase 1 uses global pattern matching; contract-specific matching deferred to future iteration"

**C. Acceptance criteria**
Current issue: Line 44 says "all four OQs"
Change: Change to "all five OQs (OQ-003, OQ-004, OQ-005, OQ-009, OQ-010)"
Diff intent: Replace "all four OQs" with "all five OQs" and add OQ-009 to the enumeration

**D. Mid-phase checkpoint**
Current issue: Line 270 says "all four OQ resolutions"
Change: Change to "all five OQ resolutions"

#### T01.02 -- FR-MOD1.6 annotation (L1)

**A. Step 3**
Current issue: Step 3 defines dataclasses without FR tag
Change: Append "(FR-MOD1.6)" to step text
Diff intent: Add "(FR-MOD1.6)" at end of step 3

#### T01.09 -- Pipeline blocking language (L3)

**A. Acceptance criterion**
Current issue: "function returns result object and never raises exceptions"
Change: "function returns result object without blocking the pipeline (FR-MOD4.3)"
Diff intent: Replace "never raises exceptions" with "without blocking the pipeline (FR-MOD4.3)"

### 2) phase-3-tasklist.md

#### T03.03 -- wiring_gate_mode criterion (M5)

**A. Acceptance criteria**
Current issue: Four criteria listed; no mention of wiring_gate_mode
Change: Add fifth criterion
Diff intent: After line 154 (`uv run pytest...`), add: "- `wiring_gate_mode` behavior is unaffected by anti-instinct gate configuration (no interaction verified by test)"

#### End of Phase 3 checkpoint -- cli-portify regression (L5)

**A. Exit criteria**
Current issue: Three exit criteria; no cli-portify regression
Change: Add fourth exit criterion
Diff intent: After line 176, add: "- cli-portify regression case passes end-to-end (Checkpoint B requirement)"
