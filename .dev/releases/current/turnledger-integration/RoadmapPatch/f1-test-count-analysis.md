---
finding_id: F1
status: analyzed
root_cause: "test-strategy Section 3 independently enumerated tests from the spec (counting 14 unit + 5 integration + 1 load = 20 categories) while Section 9 and the roadmap both inherited the tech spec's original 11-test count that groups by functional concern rather than test type"
recommended_fix: "Reconcile test-strategy Section 3 to match the 11-test functional grouping used by roadmap Section 5, release spec Section 8, and tech spec lines 306-327 — the 14-unit count in Section 3 double-counts tests that the spec bundles as single functional verifications"
---

# F1: Test Count Discrepancy Analysis

## 1. Evidence Summary

### 1.1 The 11-test count (tech spec origin)

The tech spec (`implementation-artifacts/tech-spec-ontrag-r0-r1-prerequisites-memory.md`, lines 306-327) enumerates exactly 11 new R1 tests, numbered 1-11:

- Tests 1-5: Reducer and checkpointer unit tests (lines 309-315)
- Tests 6-7: Integration/acceptance tests (lines 318-319)
- Tests 8-10: Cross-session context tests (lines 322-324)
- Test 11: Load test (lines 326-327)

The tech spec line 301 says: "Expanded to 12 tests" but the actual enumeration lists 11 (numbered 1-11). The "12" appears to be an off-by-one in the prose that was corrected in the actual list.

### 1.2 The 11-test count in the roadmap

The merged roadmap (`roadmap.md`, lines 348-362) contains a "Test Plan Summary" table that totals 11 new tests:

| Category | Count |
|----------|-------|
| Reducer unit tests | 2 |
| thread_id unit test | 1 |
| Checkpoint integration (AT-1) | 1 |
| Conversation isolation | 1 |
| Cross-session context unit | 2 |
| Cross-session context integration | 1 |
| Conversation status API | 2 |
| Load test | 1 |
| **Total new** | **11** |

This table originated from the Opus architect variant (`roadmap-opus-architect.md`, lines 253-267), which has the identical table. The Opus variant was selected as the base for the merge (`base-selection.md`, line 149).

### 1.3 The 11-test count in the release spec

The release spec (`release-spec-ontrag-r0-r1.md`, lines 524-543) enumerates tests numbered 1-11 (with gaps: 1,2,3,4,5,6,7,8,9,10,11). The numbering matches the tech spec exactly. Section 10 (line 559) states: "R1 Complete (11 new tests pass)".

### 1.4 The 11-test count in test-strategy Section 9

Test-strategy Section 9 (`test-strategy.md`, line 457) states: "Total test count: 30 (19 existing + 11 new)"

SC-12 in test-strategy Section 7 (`test-strategy.md`, line 405) states: "SC-12: New R1 tests | 11/11 pass"

### 1.5 The 20-category count in test-strategy Section 3

Test-strategy Section 3 (`test-strategy.md`, lines 164-208) breaks tests into categories:

- **Section 3.1 Unit Tests**: 14 tests enumerated (lines 164-181)
- **Section 3.2 Integration Tests**: 5 tests enumerated (lines 183-191)
- **Section 3.3 Infrastructure Verification Tests**: 6 checks (lines 193-202)
- **Section 3.4 Load Tests**: 1 test (lines 204-208)
- **Section 3.5 Regression Tests**: 19 existing (lines 212-217)

New test total from Section 3: 14 + 5 + 6 + 1 = 26 new items (or 20 if excluding infrastructure checks: 14 + 5 + 1 = 20).

### 1.6 The discrepancy

The 14 unit tests in Section 3.1 include items NOT present in the tech spec's 11-test list:

| Section 3.1 test | Tech spec equivalent | In 11-count? |
|-------------------|---------------------|--------------|
| AgentState reducer accumulation | Test 1 | YES |
| SwarmState reducer accumulation | Test 1 (bundled) | NO — split out |
| `thread_id` uses `conversation_id` | Test 2 | YES |
| Conversation isolation (2 IDs) | Test 3 | YES |
| `max_size=10` verification | Test 4 | YES |
| `store_context(embedding=NULL)` | Test 8 (part) | NO — split out |
| `get_recent_context()` ordering | Test 8 (part) | NO — split out |
| NULL vector column accepts NULL | Test 10 | YES |
| Status transition: active->completed | Test (not in 11) | NO — new |
| Status transition: active->archived | Test (not in 11) | NO — new |
| Invalid transition rejected (400) | Test (not in 11) | NO — new |
| Response schema validation | Test (not in 11) | NO — new |
| Fallback warning log | Test (not in 11) | NO — new |
| Config defaults (UE_MANAGER_URL, DSN) | Test (not in 11) | NO — new |

The 5 integration tests in Section 3.2 include:
- NORTH STAR (AT-1) — Test 6 in spec
- Cross-session PG restart — Test 9 in spec
- `generate_summary()` on transition — NOT in 11-count
- Import verification in clean virtualenv — NOT in 11-count
- Migration 003 executes cleanly — NOT in 11-count

The 6 infrastructure checks in Section 3.3 are all NEW — none appear in the tech spec's 11-test list. These are grep/SQL verification checks, not pytest tests.

### 1.7 Test-strategy Section 9 line 458

Line 458 states: "Test categories: Unit (14), Integration (5), Infrastructure (6), Load (1), Regression (19 existing)"

This line CONTRADICTS the "11 new" total on line 457. If 14 + 5 + 6 + 1 = 26 new items, but the stated total is 11, these cannot both be correct. The line 458 category breakdown matches Section 3's detail. The line 457 total matches the tech spec's 11-count.

---

## 2. Root Cause Analysis — Three Proposed Root Causes

### RC-1: Independent derivation from different granularity levels

The test-strategy generator independently enumerated tests from the release spec's acceptance criteria (Section 3-5), decomposing compound spec tests into individual test functions. Meanwhile, the roadmap inherited the tech spec's 11-count verbatim via the Opus variant. The two artifacts never cross-referenced each other because the pipeline generates them as separate steps from the same spec input.

### RC-2: The test-strategy conflated verification checks with pytest tests

The test-strategy Section 3 counted infrastructure verification checks (grep commands, SQL queries, file inspections) as "tests" alongside actual pytest tests. The tech spec's 11-count only includes items that become pytest test functions. The test-strategy generator expanded the definition of "test" to include all verification activities, inflating the count. Section 9 then copy-pasted the 11-count from the spec without reconciling it against its own Section 3.

### RC-3: The test-strategy Section 9 summary was generated from the spec/roadmap while Section 3 was generated from acceptance criteria enumeration

The test-strategy generator used two different input sources for two different sections. Section 9 (summary) was synthesized from the roadmap's test plan summary table (which says 11), while Section 3 (detail) was synthesized by walking every acceptance criterion in the extraction and creating a test for each. The generator did not perform a reconciliation pass between its own sections.

---

## 3. Adversarial Debate on Root Causes

### RC-1 Debate: Independent derivation from different granularity levels

**Prosecution (supporting RC-1):**

The tech spec (lines 306-327) bundles related verifications into single numbered tests. For example, tech spec Test 8 is "Store and retrieve context entries by recency" — a single test. But test-strategy Section 3.1 splits this into three separate unit tests: `store_context(embedding=NULL)` (line 173), `get_recent_context()` ordering (line 174), and NULL vector column accepts NULL (line 175). Similarly, the tech spec has no separate tests for status transitions, but test-strategy Section 3.1 enumerates four status-related unit tests (lines 176-179). The tech spec bundled FR-R1.5's four sub-requirements (FR-R1.5a through FR-R1.5d) as untested or tested by implication; the test-strategy created explicit tests for each.

The roadmap's test plan summary table (`roadmap.md`, lines 348-362) was copied from the Opus architect variant (`roadmap-opus-architect.md`, lines 253-267). The Opus variant was generated from the same spec but adopted the tech spec's 11-count grouping. The diff-analysis (`diff-analysis.md`, line 76) confirms: "Opus: Explicit test plan table: 19 existing + 11 new = 30 total."

The test-strategy was generated as a separate pipeline step (`generator: superclaude-roadmap-executor`, timestamp `2026-03-21T03:19:02`) AFTER the roadmap merge. It used the release spec as input (`spec_source: release-spec-ontrag-r0-r1.md`, test-strategy line 8) and independently walked every acceptance criterion to derive tests.

**Defense (against RC-1):**

If the test-strategy generator independently derived tests, why does Section 9 say "11 new"? An independent derivation would have produced its own total. The fact that Section 9 matches the tech spec's count suggests the generator DID reference the tech spec or roadmap for the summary, not just the acceptance criteria. This undermines the "independent derivation" narrative — it was partially independent (Section 3) and partially copied (Section 9).

**Rebuttal:**

The defense actually strengthens the prosecution. The generator used TWO sources: acceptance criteria for the detail (Section 3) and the roadmap/spec count for the summary (Section 9). The "independent derivation" refers specifically to Section 3's detail enumeration, not the entire document. The discrepancy exists precisely BECAUSE Section 3 was independently derived while Section 9 was not.

**Verdict: LIKELY.** The evidence strongly supports that Section 3 was derived by walking acceptance criteria independently, while Section 9 inherited the 11-count from the upstream spec chain. The discrepancy is a reconciliation failure between two sections of the same document that used different derivation methods.

---

### RC-2 Debate: Conflation of verification checks with pytest tests

**Prosecution (supporting RC-2):**

Test-strategy Section 3.3 lists 6 "Infrastructure Verification Tests" (lines 193-202) that are grep commands, SQL queries, and file inspections — NOT pytest tests. The tech spec's 11 tests are all pytest-executable. The Section 9 summary (line 458) includes these 6 infrastructure checks in its category breakdown ("Infrastructure (6)") but still states "11 new" on line 457. If we subtract the 6 infrastructure checks from the 26 total Section 3 items, we get 20. If we further note that some Section 3 unit tests are decompositions of spec tests, the original 11 maps to the pytest-only subset.

**Defense (against RC-2):**

Even removing the 6 infrastructure checks, Section 3 still has 14 unit + 5 integration + 1 load = 20 new pytest-relevant tests, not 11. The inflation from 11 to 20 is not explained by infrastructure checks alone. The 9-test gap between 11 and 20 comes from unit test decomposition and new integration tests (import verification, migration execution, generate_summary), not from infrastructure checks. RC-2 explains 6 of the 15-item gap (26 vs 11) but not the remaining 9.

**Rebuttal:**

The prosecution overstated the case. The infrastructure check conflation explains part of the inflation but not the core discrepancy. The defense is correct that the 14 unit tests vs the spec's ~7 unit tests is a decomposition issue, not a categorization issue.

**Verdict: PARTIALLY TRUE but NOT the primary root cause.** Infrastructure check conflation contributes to the total inflation but does not explain the 11 vs 20 gap in pytest-relevant tests. RC-2 is a secondary factor.

---

### RC-3 Debate: Dual-source generation without reconciliation

**Prosecution (supporting RC-3):**

The test-strategy's internal contradiction is the strongest evidence. Line 457 says "11 new" and line 458 says "Unit (14), Integration (5), Infrastructure (6), Load (1)." These two lines are adjacent and irreconcilable. This is the signature of a generator that produced Section 3 from one source (acceptance criteria walk) and Section 9 from another source (roadmap/tech-spec summary count) without a reconciliation pass.

The pipeline generates the test-strategy after the roadmap merge. The generator has access to both the release spec (which contains the 11-test enumeration in Section 8) and the extraction (which contains all acceptance criteria). Section 3 appears to be generated by iterating over every testable acceptance criterion and creating a test entry. Section 9 appears to be generated by summarizing the release spec's test plan section.

The smoking gun is line 458: the category counts (14+5+6+1=26) are CORRECT for Section 3's enumeration but WRONG for the "11 new" total on line 457. The generator wrote the categories from Section 3 data but the total from the spec.

**Defense (against RC-3):**

It is possible that the generator intentionally kept the 11-count as "new pytest tests" and the 26 categories as "all verification activities including infrastructure checks and decomposed sub-tests." Under this interpretation, the 11 represents functional test groups while 14+5+6+1 represents individual verification items. The "discrepancy" might be intentional taxonomy rather than a bug.

**Rebuttal:**

If this were intentional, the document would explain the distinction. There is no explanatory text between lines 457 and 458. The reader encounters "11 new" immediately followed by "Unit (14)" — there is no framing like "11 functional test groups decomposed into 26 individual verifications." The SC-12 gate criterion says "11/11 new R1 tests pass" (line 405), which is used as a release gate. If the actual pytest test count is 20, then "11/11 pass" is an undercount that could cause a release with 9 untested items. This is not a taxonomy choice; it is a defect.

**Verdict: LIKELY and MOST EXPLANATORY.** RC-3 explains both the mechanism (dual-source generation) and the symptom (adjacent contradictory numbers). The lack of a reconciliation pass is the direct cause.

---

## 4. Most Likely Root Cause Declaration

**RC-3 (dual-source generation without reconciliation) is the MOST LIKELY root cause**, with RC-1 (independent derivation at different granularity) as the underlying mechanism.

The test-strategy generator produced Section 3 by walking every testable acceptance criterion in the release spec/extraction, decomposing compound tests into individual test functions, and adding infrastructure verification checks. It produced Section 9 by copying the tech spec's 11-test total that flows through the release spec (line 559: "R1 Complete (11 new tests pass)") and the roadmap (lines 348-362). No reconciliation pass was performed between Sections 3 and 9.

The 11-count originates from the tech spec (lines 306-327), which numbers tests 1-11 as functional groups. This count was adopted by the release spec (Section 8), the Opus roadmap variant (test plan summary), the merged roadmap (Section 5), and test-strategy Section 9 — all inheriting from the same upstream source. The 20-count (excluding infrastructure checks) was independently derived by the test-strategy's Section 3 generator, which decomposed compound spec tests into individual pytest-granularity tests and added coverage for acceptance criteria that the tech spec's 11-test list did not explicitly cover (status transitions, config defaults, fallback logging, import verification, migration execution, generate_summary integration).

---

## 5. Solution Brainstorm — Three Proposals

### S-1: Adopt the 11-count as canonical; demote Section 3 extras to "verification activities"

Reconcile test-strategy by keeping the 11-count as the number of new pytest test functions. Reclassify the additional items in Section 3 into two categories: (a) sub-assertions within existing tests (e.g., the 3 status transition tests become assertions within a single `test_status_transitions` test), and (b) non-pytest verification activities (infrastructure grep checks, import verification, migration execution). Update Section 9 line 458 to match: "Pytest tests: 11 new. Infrastructure checks: 6. Total verification items: 17." Update SC-12 to "11/11 new R1 pytest tests pass."

This preserves alignment with the tech spec, release spec, and roadmap. The Section 3 detail becomes an expanded view showing what each of the 11 tests covers internally.

### S-2: Adopt the 20-count as canonical; update roadmap and SC-12 to match

Accept that the test-strategy's Section 3 detail is the more accurate representation of what will actually be implemented as separate pytest test functions. Update: (a) roadmap Section 5 test plan summary table to show 20 new tests, (b) SC-12 to "20/20 new R1 tests pass", (c) test-strategy Section 9 to "39 total (19 existing + 20 new)", (d) release spec Section 10 milestone statement. Keep the 6 infrastructure checks separate as non-pytest verification.

This accepts that the tech spec's 11-count was a functional grouping that underestimated the actual pytest function count, and corrects all downstream documents to match the more granular reality.

### S-3: Define two explicit tiers — "11 functional test groups" and "20 pytest functions" — and document the mapping

Create a reconciliation table in test-strategy that maps each of the 11 tech-spec tests to their decomposed pytest functions. Update SC-12 to reference both: "11/11 functional test groups pass (20 pytest functions)." Add a footnote to roadmap Section 5 test plan summary: "11 functional groups decompose into 20 individual pytest functions; see test-strategy Section 3 for full enumeration." This preserves backward compatibility with all documents while resolving the ambiguity.

---

## 6. Adversarial Debate on Solutions

### S-1 Debate: Adopt the 11-count, demote extras

**Advocate:**

S-1 is the simplest fix. It requires changes only to test-strategy (one file), preserving the roadmap, release spec, and tech spec unchanged. The 11-count has been validated through 4 documents and the adversarial roadmap pipeline. The Section 3 extras are either decompositions of existing tests (sub-assertions, not separate tests) or verification activities that don't belong in a pytest count. Infrastructure grep checks were never intended to be pytest tests. This solution correctly distinguishes between "tests" (pytest functions) and "verification activities" (manual or scripted checks).

SC-12 remains clean: "11/11 new R1 tests pass." A developer implementing Task 20 in the tech spec knows exactly what to write: 11 test functions in `test_checkpointer.py` and `test_memory_persistence.py`.

**Critic:**

S-1 forces the implementer to bundle logically distinct tests into compound test functions to hit the 11 number. For example, `test_status_transitions` would contain assertions for active->completed, active->archived, AND invalid transition rejection — three distinct behaviors in one test. This violates pytest best practice (one assertion concept per test) and makes failure diagnosis harder. If the test fails, you don't know which transition broke.

Additionally, "config defaults" and "fallback warning log" tests in Section 3 address real acceptance criteria (FR-R0.3/AC4, FR-R1.3b) that have no corresponding test in the tech spec's 11-count. Demoting these to "verification activities" means they might not get implemented as automated tests at all, leaving acceptance criteria uncovered.

**Rebuttal:**

The bundling concern is valid for status transitions but overstated for other tests. Tests 1 and 5 in the tech spec (reducer accumulation and content fidelity) are already separate, not bundled. The config defaults and fallback warning tests are legitimate additions that the tech spec missed — but they can be added as tests 12 and 13, making the count "13 new tests" rather than forcing everything into 11. S-1 can be modified to "adopt the tech spec grouping as the baseline, add the genuinely new tests that Section 3 identified, and arrive at a reconciled count."

**Verdict: ACCEPTABLE with modification.** S-1's principle is sound (use the tech spec as canonical), but the rigid 11-count should be updated to include the genuinely new tests Section 3 identified. Pure 11-count enforcement would leave gaps.

---

### S-2 Debate: Adopt the 20-count, update all documents

**Advocate:**

S-2 is the most accurate. When the implementer writes Task 20, they will create individual pytest functions — not compound tests. Pytest best practice is one test per behavior. The 20-count from Section 3 is closer to what will actually exist in the test files. Updating the roadmap and SC-12 to match reality prevents confusion during implementation and release verification.

The tech spec's 11-count was written before the test-strategy decomposition and before the adversarial roadmap pipeline added coverage for acceptance criteria like status transitions and config defaults. The 20-count reflects the pipeline's improvement over the original spec.

**Critic:**

S-2 requires changes to 4 documents (roadmap, release spec, test-strategy, extraction success criteria). The roadmap was generated through an adversarial process with two variants, debate, scoring, and merge. Changing its test plan summary table post-merge undermines the pipeline's validation. If we change 19+11=30 to 19+20=39 in the roadmap, we also need to update every milestone that references "30 tests" (M4 line 339 "23 total", M5 line 349 "30/30", M6 line 352 "30/30").

Furthermore, the 20-count itself may not be stable. Section 3 includes "Config defaults (UE_MANAGER_URL, DSN)" as one test — but is that 1 pytest function or 2? The decomposition is still somewhat arbitrary. Adopting 20 as canonical just shifts the reconciliation problem.

**Rebuttal:**

The cascade concern is real but manageable — it's a finite set of line edits. The instability concern is valid: the "correct" pytest count won't be known until the tests are actually written. However, the 20-count is a better estimate than 11. The pipeline generated 20 as its best analysis of what's needed. S-2 simply propagates that analysis to all documents.

**Verdict: ACCEPTABLE but high-cost.** S-2 is technically correct but requires touching 4+ documents and creates cascade risk. The benefit (accuracy) must be weighed against the cost (multi-document update, pipeline re-validation concerns).

---

### S-3 Debate: Define two tiers with explicit mapping

**Advocate:**

S-3 resolves the ambiguity without declaring either count "wrong." The 11-count represents functional test groups (the tech spec's intent). The 20-count represents pytest functions (the implementation reality). Both are valid at different abstraction levels. The reconciliation table makes the mapping explicit, so a developer can verify: "I wrote 20 test functions, they cover all 11 functional groups."

SC-12 becomes unambiguous: "11/11 functional test groups pass (20 pytest functions)." The roadmap's test plan summary stays at 11 groups with a footnote. No document is contradicted — both counts are correct in their context.

This solution also addresses the root cause: it creates the reconciliation artifact that the pipeline failed to generate. Future pipeline runs could include a reconciliation step that produces this mapping automatically.

**Critic:**

S-3 adds complexity. Every document that references test counts now needs a parenthetical clarification. "30 tests" becomes "30 tests (19 existing + 11 groups / 20 functions)" which is harder to parse. The dual-tier system creates a new source of confusion: when someone says "all tests pass," do they mean 30 or 39?

The reconciliation table itself requires maintenance. If the implementer adds a 21st test function, the table needs updating. If they consolidate two tests into one, the table needs updating. The mapping is a living artifact that adds overhead.

**Rebuttal:**

The complexity concern is overblown. The parenthetical appears in exactly 2 places: SC-12 and the roadmap test plan summary footnote. The reconciliation table is written once (now) and verified once (at implementation). It does not need continuous maintenance — it's a planning artifact, not a runtime dependency. The "30 vs 39" confusion is resolved by the footnote: "30 = 19 existing + 11 groups; each group may contain multiple pytest functions."

**Verdict: RECOMMENDED.** S-3 resolves the ambiguity without invalidating any existing document, provides the missing reconciliation artifact, and has minimal maintenance overhead. It correctly models the reality that test counts operate at two abstraction levels.

---

## 7. Recommended Solution Declaration

**S-3 (two-tier mapping with reconciliation table) is the RECOMMENDED solution.**

**Reasoning:**

1. **Minimal document disruption**: Roadmap, release spec, and tech spec need only a footnote addition, not a count change. Test-strategy Section 9 gets the reconciliation table and a clarified line 457/458.

2. **Root cause remediation**: The reconciliation table IS the artifact the pipeline should have produced. Adding it directly addresses the dual-source generation failure.

3. **Implementation clarity**: The mapping table tells the implementer exactly how to organize their test files: 11 functional groups, each decomposed into specific pytest functions, totaling ~20 functions.

4. **SC-12 becomes unambiguous**: "11/11 functional test groups pass (20 pytest functions)" — anyone reading this knows both the group count and the function count.

**Specific changes required:**

| File | Change |
|------|--------|
| `test-strategy.md` line 457 | Change to: "Total test count: 30 (19 existing + 11 functional test groups comprising ~20 pytest functions)" |
| `test-strategy.md` line 458 | Change to: "Pytest functions by type: Unit (~14), Integration (~5), Load (1). Infrastructure verification checks: 6. Functional test groups: 11." |
| `test-strategy.md` new section | Add reconciliation table mapping 11 spec tests to their Section 3 decompositions |
| `test-strategy.md` line 405 (SC-12) | Change to: "SC-12: New R1 tests \| 11/11 functional groups pass (~20 pytest functions)" |
| `roadmap.md` line 361 | Add footnote: "11 functional test groups; see test-strategy Section 3 for pytest-level decomposition (~20 functions)" |
| `roadmap.md` line 223 (T6.1) | Update to: "19 existing + 11 new test groups (~20 pytest functions). All pass." |

**Changes NOT required:**
- Release spec Section 8 — already enumerates 11 tests correctly at the functional level
- Tech spec Testing Strategy — upstream source, should not be modified post-spec-generation
- Extraction — derived artifact, will be consistent once test-strategy is fixed
