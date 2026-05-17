# Patch Checklist

Generated: 2026-05-17
Total edits: 18 across 7 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] T01.02: add "bundle-specific tasklist checks forbidden" AC bullet (from finding H1)
  - [ ] T01.06: add "TB-Add-1..3 stubs present on all 3 surfaces" Verification bullet (from finding M1)
  - [ ] T01.13: enumerate DM-002 fields (rf_qa_table_verbatim, prompt_directive, reinjection_rule) and DM-005 10-field producer/consumer AC (from finding M2)
  - [ ] T01.14: add API-002 placement + API-003 all-fail-routing AC details (from finding M3)
  - [ ] T01.18: add standalone TB-Add-2 ADVISORY non-blocking AC bullet (from finding M4)
- phase-2-tasklist.md
  - [ ] T02.03: add "Generated MDTM contains `## Execution Context` block" AC bullet (from finding M5)
- phase-3-tasklist.md
  - [ ] T03.03: replace `rf-qa.md` with `qa-task-integrity.md` in AC #2 diff target (from finding M6)
  - [ ] T03.04: add Notes cross-link to T03.14 runtime verification (from finding L1)
  - [ ] T03.17: add release-spec §4.6 enforcement grep AC (from finding L2)
- phase-4-tasklist.md
  - [ ] T04.13: tighten line-range AC to [958, 964] or document tolerance (from finding L3)
  - [ ] T04.15: add 4-bullet governance enumeration AC (logical-flag, revert path, K-004 gate, M7 reference) (from finding H3)
  - [ ] T04.16: replace "T04.01-T04.17" with "T04.01-T04.15" in Exit Criteria + Acceptance; correct "All 16 regular tasks" to "All 13 regular tasks T04.01-T04.05, T04.07-T04.11, T04.13-T04.15" (from finding H2)
- phase-5-tasklist.md
  - [ ] T05.03: add prior-regression-check gate AC bullet (from finding M7)
  - [ ] T05.05: strengthen ordering-precedence AC with ordered regex + sub-agent confirmation (from finding M8)
- phase-6-tasklist.md
  - [ ] T06.01: add SKILL.md grep AC (or explicit deferral note) (from finding H4)
  - [ ] T06.05: add exhaust_point vocabulary-membership AC bullet (from finding L4)
- phase-7-tasklist.md
  - [ ] T07.04: promote Q-DM-1 binding to enforced AC bullet (from finding H5)
  - [ ] T07.19: split MET-002 unresolved-token + DAG-cycle into two AC bullets (from finding L5)

## Cross-file consistency sweep

- [ ] Verify all checkpoint Exit Criteria task-range phrasing uses the regular-task list (not the literal end-task-number range) where ranges are non-contiguous.
- [ ] Verify all FF_* governance entries record the 4-tuple (logical-flag, revert path, cleanup gate, M7-consolidation reference) — apply pattern from H3 to FF_TB_ADD (T01.17), FF_EXECUTION_CONTEXT_HEADER (T02.11), FF_INHERITED_STRUCTURAL_VERDICT (T03.16), FF_RETRY_MONOTONICITY_GUARDS (T05.16), FF_SYNTHETIC_DNSP_EMISSION (T06.17) if not already complete.

---

## Precise diff plan

Suggested execution order (highest-impact first): H1 → H2 → H3 → H4 → H5 → M1..M8 → L1..L5 → cross-file sweep.

### 1) phase-1-tasklist.md

#### Section/heading to change
- T01.02 Acceptance Criteria
- T01.06 Verification
- T01.13 Acceptance Criteria
- T01.14 Acceptance Criteria
- T01.18 Acceptance Criteria

#### Planned edits

**A. T01.02 — Add bundle-specific-checks forbidden bullet (H1)**
Current issue: AC lacks the R-007 prohibition.
Change: Append AC bullet.
Diff intent: Insert `- Diff confirms no bundle-specific tasklist-only checks introduced (R-007 invariant).` as the 5th AC bullet.

**B. T01.06 — Add three-surface verification (M1)**
Current issue: Mid-checkpoint omits three-surface mirror diff re-check.
Change: Add Verification bullet.
Diff intent: Insert `- TB-Add-1..3 stubs present on all 3 surfaces (rf-qa.md + SKILL.md A.10 + SKILL.md 15-item).` as the 4th Verification bullet.

**C. T01.13 — Enumerate DM-002 + DM-005 fields (M2)**
Current issue: AC enumerates DM-003 + DM-004 only.
Change: Add AC bullet covering DM-002 and DM-005 fields.
Diff intent: Insert `- DM-002 schema enumerates rf_qa_table_verbatim, prompt_directive (fixed-string), reinjection_rule (INV-002 cycle-N fresh). DM-005 enumerates 10 producer/consumer fields including schema_version 1.0.0 and INV-019 Self-Audit obligation.`

**D. T01.14 — Add API-002 + API-003 details (M3)**
Current issue: AC only enumerates API-001 + API-004.
Change: Add AC bullet.
Diff intent: Insert `- API-002 records placement-after-TARGET-FILES-before-INSTRUCTIONS and missing-verdict-halt-before-A.10.5. API-003 records all-fail routes to rf-team-lead.md:417 NO-DNSP.`

**E. T01.18 — Add TB-Add-2 ADVISORY standalone AC (M4)**
Current issue: TB-Add-2 advisory non-blocking referenced only via compressed Exit Conditions.
Change: Add AC bullet.
Diff intent: Insert `- TB-Add-2 confirmed emits literal [ADVISORY] prefix and does NOT block gate verdict on out-of-bounds fixture.`

### 2) phase-2-tasklist.md

#### Planned edits

**A. T02.03 — Add MUST-contain-block AC (M5)**
Current issue: BUILD_REQUEST contract update task does not enforce generated-MDTM block presence.
Change: Add AC bullet.
Diff intent: Insert `- Generated MDTM from updated BUILD_REQUEST contract contains "## Execution Context" block after frontmatter, before first phase (post-update contract-conformance check).`

### 3) phase-3-tasklist.md

#### Planned edits

**A. T03.03 — Replace rf-qa.md with qa-task-integrity.md in AC #2 (M6)**
Current issue: Diff target file name wrong.
Change: Literal substitution.
Diff intent: Replace `Diff of injected block vs \`rf-qa.md\` Items Reviewed table is byte-identical.` with `Diff of injected block vs \`qa-task-integrity.md\` Items Reviewed table is byte-identical.`

**B. T03.04 — Add Notes cross-link (L1)**
Current issue: Runtime verification dependency hidden.
Change: Update Notes line.
Diff intent: Replace `**Notes:** None.` with `**Notes:** Runtime sample verification deferred to T03.14 (TEST-009 self-audit fixture).`

**C. T03.17 — Add release-spec grep AC (L2)**
Current issue: No enforcement-check for sequencing rule.
Change: Add AC bullet.
Diff intent: Insert `- \`grep -n "PR-06 → PR-04" <release-spec>\` returns a match within §4.6, confirming sequencing rule is enforced (not merely documented in artifact note).`

### 4) phase-4-tasklist.md

#### Planned edits

**A. T04.13 — Tighten line-range AC (L3)**
Current issue: Tolerance widened to [955, 970].
Change: Restrict to [958, 964] or note tolerance.
Diff intent: Replace `with line N within [955, 970]` with `with line N within [958, 964] (small tolerance for whitespace shifts)`.

**B. T04.15 — Enumerate 4 governance bullets (H3)**
Current issue: FF_FIVE_ADVERSARIAL_AXES content under-specified.
Change: Add 4-bullet expansion.
Diff intent: Replace single AC bullet with 4: logical-flag designation; revert path = remove overlay; cleanup gate = K-004 axis-distribution audit; M7 consolidation reference.

**C. T04.16 — Fix task-range references (H2)**
Current issue: References non-existent T04.17.
Change: Replace task-range references.
Diff intent: Replace `T04.01-T04.17` with `T04.01-T04.15` in both Exit Criteria and Acceptance Criteria. Update "All 16 regular tasks" to "All 13 regular tasks T04.01-T04.05, T04.07-T04.11, T04.13-T04.15".

### 5) phase-5-tasklist.md

#### Planned edits

**A. T05.03 — Add prior-regression-check gate AC (M7)**
Diff intent: Insert `- Monotonicity emission verified gated on prior regression-check passing (test with regression flip on the same cycle confirms monotonicity NOT emitted).`

**B. T05.05 — Strengthen ordering AC (M8)**
Diff intent: Replace grep-count AC with ordered-text + sub-agent confirmation.

### 6) phase-6-tasklist.md

#### Planned edits

**A. T06.01 — Add SKILL.md grep AC (H4)**
Diff intent: Insert AC: `\`grep -c "synthetic-dnsp" src/superclaude/skills/task-builder/SKILL.md\` returns at least 1 (detailed merge-step verification deferred to T06.11).`

**B. T06.05 — Add vocabulary-membership AC (L4)**
Diff intent: Insert AC: `Emitter rejects synthesis with exhaust_point outside {retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}.`

### 7) phase-7-tasklist.md

#### Planned edits

**A. T07.04 — Promote Q-DM-1 binding to enforced AC (H5)**
Diff intent: Insert AC: `Fixture's schema reference matches the recorded Q-DM-1 resolution artifact (machine-checkable).`

**B. T07.19 — Split MET-002 into two AC bullets (L5)**
Diff intent: Replace single combined bullet with two: unresolved-token-detection on TB-Add-1 and DAG-cycle-detection on TB-Add-4, each at 100%.
