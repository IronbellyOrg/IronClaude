---
title: "OntRAG R0+R1 Roadmap Patch Tasklist"
type: remediation-tasklist
target_files:
  - .dev/releases/current/feature-Ont-RAG/r0-r1/roadmap.md
  - .dev/releases/current/feature-Ont-RAG/r0-r1/test-strategy.md
findings_addressed: [F1, F2, F3, F5]
analysis_sources:
  - f1-test-count-analysis.md
  - f2-table-parseability-analysis.md
  - f3-missing-traces-analysis.md
  - f5-validation-coverage-analysis.md
status: pending
created: 2026-03-21
---

# OntRAG R0+R1 Roadmap Patch Tasklist

## Context

The roadmap pipeline completed successfully through the merge step but the validation gate (`superclaude roadmap validate`) found **4 blocking issues** preventing tasklist generation. This tasklist provides granular, ordered steps to remediate all 4 findings so the pipeline can proceed.

**Validation report**: `.dev/releases/current/feature-Ont-RAG/r0-r1/validate/validation-report.md`

---

## Phase 1: F3 — Missing Requirement Traces (3 line edits in roadmap.md)

### Problem
Tasks T0.2, T0.3, and T6.4 in `roadmap.md` cite no formal FR/NFR requirement IDs. T0.2 cites only "Open Question 1 (F6)", T0.3 cites only "Open Question 8", and T6.4 has "—" in the Requirements column. The validation gate requires all tasks to trace to formal requirement IDs or be explicitly marked as exempt.

### Root Cause
`extraction.md` structurally separates Open Questions from FR/NFR requirements without a "Parent Requirement" cross-reference column. Both roadmap generators (Opus, Haiku) faithfully cited OQ IDs but did not back-trace to parent FR-R1.2. T6.4 is genuinely non-requirement release administration work with no FR/NFR to trace to.

### Expected Result After Fix
All 3 tasks have explicit requirement traces or intentional exemption annotations. The `integration_contracts_covered` and traceability checks pass.

### Steps

- [x] **1.1** Open `roadmap.md` line 39. In the T0.2 row, change the Requirements cell from `Open Question 1 (F6)` to `FR-R1.2, OQ-1 (F6)`. Rationale: OQ-1 verifies the AsyncPostgresSaver API surface, which IS the FR-R1.2 implementation mechanism. Both generators implicitly understood this — the fix makes it explicit.

- [x] **1.2** Open `roadmap.md` line 40. In the T0.3 row, change the Requirements cell from `Open Question 8` to `FR-R1.2, OQ-8`. Rationale: OQ-8 decides the async initialization pattern for AsyncPostgresSaver, a prerequisite for FR-R1.2 implementation.

- [x] **1.3** Open `roadmap.md` line 226. In the T6.4 row, change the Requirements cell from `—` to `N/A — release administration`. Rationale: release tagging, CHANGELOG updates, and R2 limitation documentation are process activities with no formal FR/NFR. The explicit annotation distinguishes "intentionally exempt" from "accidentally missing".

---

## Phase 2: F2 — Table-to-List Conversion (7 tables in roadmap.md)

### Problem
All 7 phase sections in `roadmap.md` encode tasks as Markdown table rows (`| Task | Requirements | Description | Parallel? |`). The downstream `sc:tasklist` splitter expects headings + numbered/checklist items. Tables are not parseable by the splitter, so tasklist generation will fail.

### Root Cause
The Opus architect agent defaulted to Markdown tables for multi-dimensional task data. The Haiku analyzer produced numbered lists (the correct format), but the merge step selected Opus as the base variant. The merge evaluation criteria (C1-C10 in `base-selection.md`) did not include downstream splitter compatibility, so the table format was preserved unchecked.

### Expected Result After Fix
All phase task sections use numbered list items parseable by `sc:tasklist`. All data from table cells (task ID, requirements, description, parallelism) is preserved as inline annotations.

### Conversion Format
Each table row becomes a numbered list item:
```
Before: | T0.1 | FR-R0.1/AC1 | Clean virtualenv spike... | No — first task |
After:  1. **T0.1** [FR-R0.1/AC1] — Clean virtualenv spike... *(Seq: first task)*
```
Rules:
- `Task` cell → bold prefix `**T0.1**`
- `Requirements` cell → bracketed `[FR-R0.1/AC1]`
- `Description` cell → main text after em dash ` — `
- `Parallel?` cell → italic suffix `*(Seq: ...)* ` or `*(Par: with T2.1)*` or `*(Par: all T2.x)*`
- Tasks with `N/A — release administration` → `[admin]`

**IMPORTANT**: After completing Phase 1 (F3 fixes), the Requirements cells for T0.2, T0.3, and T6.4 will already have the corrected values. Use the corrected values in the list conversion.

### Steps

- [x] **2.1** Open `roadmap.md` lines 36-42 (Phase 0). Delete the table header row, separator row, and all 5 data rows. Replace with numbered list items using the conversion format above. The 5 items are T0.1 through T0.5. Preserve the text before the table (exit gate, stop condition) and after (Milestone M0) unchanged.

- [x] **2.2** Open `roadmap.md` Phase 1 table (currently around lines 57-64 — line numbers may have shifted from 2.1). Delete the table (header + separator + 6 data rows for T1.1-T1.6). Replace with 6 numbered list items. Preserve surrounding text unchanged.

- [x] **2.3** Open `roadmap.md` Phase 2 table (currently around lines 78-85). Delete the table (header + separator + 6 data rows for T2.1-T2.6). Replace with 6 numbered list items. Preserve surrounding text unchanged.

- [x] **2.4** Open `roadmap.md` Phase 3 table (currently around lines 111-116). Delete the table (header + separator + 4 data rows for T3.1-T3.4). Replace with 4 numbered list items. Preserve surrounding text unchanged.

- [x] **2.5** Open `roadmap.md` Phase 4 table (currently around lines 146-152). Delete the table (header + separator + 5 data rows for T4.1-T4.5). Replace with 5 numbered list items. Preserve surrounding text unchanged.

- [x] **2.6** Open `roadmap.md` Phase 5 table (currently around lines 180-187). Delete the table (header + separator + 6 data rows for T5.1-T5.6). Replace with 6 numbered list items. Preserve surrounding text unchanged.

- [x] **2.7** Open `roadmap.md` Phase 6 table (currently around lines 221-226). Delete the table (header + separator + 4 data rows for T6.1-T6.4). Replace with 4 numbered list items. Note: T6.4's requirements should be `[admin]` per the conversion format, reflecting the F3 fix from step 1.3. Preserve surrounding text unchanged.

---

## Phase 3: F1 — Test Count Reconciliation (roadmap.md + test-strategy.md)

### Problem
The roadmap (Section 5) and test-strategy Section 9 both state "11 new tests". But test-strategy Section 3 enumerates 20 new pytest-relevant tests (14 unit + 5 integration + 1 load) plus 6 infrastructure checks (26 total). SC-12 says "11/11 new R1 tests pass" — ambiguous against 20 actual pytest functions. The discrepancy creates unclear completion criteria.

### Root Cause
The test-strategy generator used two different input sources without reconciliation. Section 3 was derived by walking every acceptance criterion in the spec, decomposing compound tests into individual pytest functions. Section 9 inherited the tech spec's 11-test count (functional groups) via the roadmap. The smoking gun is test-strategy lines 457-458: "11 new" immediately followed by category counts summing to 26.

### Expected Result After Fix
Both documents acknowledge two abstraction levels: 11 functional test groups (tech spec level) and ~20 pytest functions (implementation level). SC-12 is unambiguous. A reconciliation mapping exists so implementers know exactly how the 11 groups decompose.

### Steps

- [x] **3.1** Open `test-strategy.md` line 457. Change from:
  `**Total test count:** 30 (19 existing + 11 new)`
  To:
  `**Total test count:** 30 (19 existing + 11 functional test groups comprising ~20 pytest functions)`

- [x] **3.2** Open `test-strategy.md` line 458. Change from:
  `**Test categories:** Unit (14), Integration (5), Infrastructure (6), Load (1), Regression (19 existing)`
  To:
  `**Pytest functions by type:** Unit (~14), Integration (~5), Load (1). Infrastructure verification checks: 6 (non-pytest). Functional test groups: 11.`

- [x] **3.3** Open `test-strategy.md` line 405 (Gate E table, SC-12 row). Change from:
  `| SC-12: New R1 tests | 11/11 pass | Fix before release |`
  To:
  `| SC-12: New R1 tests | 11/11 functional groups pass (~20 pytest functions) | Fix before release |`

- [x] **3.4** Open `test-strategy.md` after line 458 (end of Section 9). Insert a new reconciliation mapping subsection:
  ```
  ### Test Group to Pytest Function Mapping

  | Spec Test # | Functional Group | Pytest Functions | Count |
  |-------------|-----------------|------------------|-------|
  | 1 | Reducer accumulation (AgentState) | AgentState reducer test, SwarmState reducer test | 2 |
  | 2 | thread_id uses conversation_id | thread_id mapping test | 1 |
  | 3 | Conversation isolation | Isolation test (2 conversation_ids) | 1 |
  | 4 | AsyncPostgresSaver max_size | max_size=10 verification | 1 |
  | 5 | Content fidelity | NULL vector column accepts NULL | 1 |
  | 6 | North Star (AT-1) | Restart persistence integration test | 1 |
  | 7 | Cross-session PG restart | Context survives restart integration test | 1 |
  | 8 | Store and retrieve context | store_context(embedding=NULL), get_recent_context() ordering | 2 |
  | 9 | Cross-session integration | Cross-session context integration test | 1 |
  | 10 | Status transitions | active→completed, active→archived, invalid rejection (400) | 3 |
  | 11 | Load test | 50 concurrent conversations | 1 |
  | — | Additional coverage | Config defaults, fallback warning log, response schema, generate_summary integration, import verification, migration 003 | ~6 |
  | | **Total** | | **~20** |

  The 11 functional test groups are the tech spec's enumeration (tests 1-11). The ~20 pytest functions reflect Section 3's decomposition into individual test functions. Both counts are correct at their respective abstraction level.
  ```

- [x] **3.5** Open `roadmap.md` Test Plan Summary section (around line 361 — the `**Total new** | **11**` row). After the table, add a footnote:
  `*11 functional test groups; see test-strategy Section 3 for pytest-level decomposition (~20 functions).*`

- [x] **3.6** Open `roadmap.md` Phase 6 task T6.1 (converted to list item in Phase 2). If the description says "19 existing + 11 new = 30 tests", append: `(11 functional groups comprising ~20 pytest functions)`.

---

## Phase 4: F5 — Validation Coverage Gaps (test-strategy.md)

### Problem
Tasks T2.5 (dead code import trace) and T6.4 (tag release / CHANGELOG / limitations) appear in the roadmap but have zero matching validation steps in the test strategy — not in any validation milestone, test category, or acceptance checklist.

### Root Cause
The test-strategy generator's validation taxonomy is built around machine-verifiable outputs (CLI commands, grep checks, SQL queries, pytest execution). T2.5 produces a prose analysis document and T6.4 produces administrative artifacts (git tag, CHANGELOG). Neither fits the generator's testability heuristic. The gap pre-dates the merge — the old Opus test strategy also lacked coverage for these tasks.

### Expected Result After Fix
VM-2 includes a document-existence check for T2.5. VM-6 includes artifact-existence checks for T6.4 (git tag, CHANGELOG, limitations). M6 acceptance checklist includes 3 new items. All roadmap tasks now have validation coverage.

### Steps

- [x] **4.1** Open `test-strategy.md` VM-2 section (around line 62, after the `T-2.6` item). Insert a new bullet:
  `- **T-2.5**: Dead code import trace document committed to `.dev/` — file exists with non-empty content`

- [x] **4.2** Open `test-strategy.md` VM-6 section (around line 150, after the `T-6.3` item). Insert 3 new bullets:
  ```
  - **T-6.4a**: Git tag matching release version exists (`git tag -l "v0.1-r0r1"`)
  - **T-6.4b**: `CHANGELOG.md` contains R0+R1 release section (`grep "R0+R1" CHANGELOG.md`)
  - **T-6.4c**: Known limitations for R2 documented (nullable vector column, no HNSW index, inert ConversationSummaryBufferMemory)
  ```

- [x] **4.3** Open `test-strategy.md` M6 acceptance section (around line 355, after the release anchors item). Insert 3 new checklist items:
  ```
  - [ ] CHANGELOG.md updated with R0+R1 section
  - [ ] Git tag created matching release version
  - [ ] Known R2 limitations documented
  ```

---

## Phase 5: Verification

### Steps

- [x] **5.1** Re-read `roadmap.md` end-to-end. Verify: (a) no remaining Markdown tables in phase task sections, (b) all tasks have requirement traces or `[admin]` annotation, (c) test plan summary footnote is present, (d) T6.1 description includes the group/function clarification.

- [x] **5.2** Re-read `test-strategy.md` lines 457-458 and the new reconciliation table. Verify: (a) line 457 says "11 functional test groups comprising ~20 pytest functions", (b) line 458 category breakdown is updated, (c) reconciliation table sums to ~20, (d) SC-12 (line 405) is updated.

- [x] **5.3** Re-read `test-strategy.md` VM-2 and VM-6 sections. Verify: (a) T-2.5 exists in VM-2, (b) T-6.4a/b/c exist in VM-6, (c) M6 acceptance has 3 new checklist items.

- [ ] **5.4** Run `superclaude roadmap validate` on the output directory to confirm all 4 blocking issues are resolved and `tasklist_ready: true`.
