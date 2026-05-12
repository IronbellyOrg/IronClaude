# Patch Checklist
Generated: 2026-04-05
Total edits: 5 across 4 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] M1: Reword T01.02 acceptance criterion 3 to treat line numbers as expected, not guaranteed (from finding M1)
  - [ ] M2: Add Section 9.7 to T01.03 title, steps, deliverables, and acceptance criteria (from finding M2)
- phase-3-tasklist.md
  - [ ] M3: Add incomplete-prompt template retention as 5th acceptance criterion in T03.03 (from finding M3)
  - [ ] L1: Update T03.04 Why field to cite both NFR-TDD-CMD.3 and FR-TDD-CMD.2f (from finding L1)
- phase-4-tasklist.md
  - [ ] M4: Add `refs/operational-guidance.md` as 5th acceptance criterion in T04.04 (from finding M4)

## Cross-file consistency sweep
- [ ] Verify traceability matrix in tasklist-index.md still accurate after patches (no structural changes, only content enrichment)

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### T01.02 Acceptance Criteria
**A. Reword line-number assumption (M1)**
Current issue: Criterion treats line numbers 48-63 and 82-88 as facts
Change: Reword to indicate these are expected locations to verify
Diff intent: Replace "Both migration blocks (lines 48-63 and 82-88) located and content boundaries confirmed" with "Migration blocks located; if at expected lines 48-63 and 82-88, content boundaries confirmed; if at different lines, actual locations recorded and deviation flagged"

#### T01.03 Section 9.7 addition
**B. Add Section 9.7 throughout T01.03 (M2)**
Current issue: Task only covers Sections 9.3 and 5.10
Change: Add "9.7" alongside 9.3 and 5.10 in title, Why, steps, deliverables, acceptance criteria
Diff intent:
- Title: "Read Developer Guide Sections 9.3 and 5.10" -> "Read Developer Guide Sections 9.3, 9.7, and 5.10"
- Why: add "Section 9.7" reference
- Steps: add step to read Section 9.7
- Deliverables: add Section 9.7
- Acceptance criteria: add Section 9.7

### 2) phase-3-tasklist.md

#### T03.03 Acceptance Criteria
**C. Add incomplete-prompt template retention check (M3)**
Current issue: 4 acceptance criteria, missing incomplete-prompt template
Change: Add 5th criterion after existing 4th
Diff intent: Add "- Incomplete-prompt template (originally lines 65-76) retained and unmodified" after the 4th acceptance criterion

#### T03.04 Why field
**D. Add FR-TDD-CMD.2f citation (L1)**
Current issue: Only cites NFR-TDD-CMD.3
Change: Add FR-TDD-CMD.2f
Diff intent: Replace "NFR-TDD-CMD.3 mandates" with "NFR-TDD-CMD.3 and FR-TDD-CMD.2f mandate"

### 3) phase-4-tasklist.md

#### T04.04 Acceptance Criteria
**E. Add 5th refs file (M4)**
Current issue: Only 4 of 5 refs files listed
Change: Add `refs/operational-guidance.md` as 5th criterion
Diff intent: Add "- `git diff` on `refs/operational-guidance.md` returns empty" after existing 4th criterion
