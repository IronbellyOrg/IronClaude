# Merged Reflection: v3.05 Tasklist Validation

**Date**: 2026-03-20
**Sources**: Agent A reflection, Agent B reflection
**Tasklist**: `tasklist.md` (24 tasks, 6 waves)
**Merged Plan**: `adversarial/merged-output.md` (20 edits, 9 interaction effects, 11 migration notes)

---

## Agreement Summary

Both agents agree on the following findings with high confidence:

1. **100% edit coverage**: All 20 numbered edits from the merged plan's summary table have corresponding tasks in the tasklist. No edits are missing.
2. **No circular dependencies**: The dependency graph is a clean DAG.
3. **Line references are accurate**: All line number references checked against the spec are correct (with one minor imprecision noted by Agent B on W4-01).
4. **Wave ordering is correct and safe**: The 6-wave structure follows a logical progression from metadata through core changes to peripheral content and final verification.
5. **W5-04 is a justified orphan**: Both agents trace it to the merged plan's completeness assessment section. It is not a true orphan.
6. **Verify tasks are legitimate structural additions**: W1-V, W2-V, W3-V, W4-V, W6-V are tasklist infrastructure, not merged-plan-sourced edits.
7. **5 of 9 interaction effects missing from Cross-Cutting Notes**: Both agents independently identified the same 5 missing IEs (IE-4, IE-5, IE-6, IE-8, IE-9).
8. **High-risk edits are properly sequenced**: W2-02 (budget model), W2-03 (budget isolation), and W3-05 (pipeline wiring) are all in early waves with verification.
9. **Overall confidence: HIGH**: The tasklist is faithful to the merged plan and ready for execution with minor improvements.

---

## Disagreements & Resolutions

### D1: Missing Dependency Severity -- W3-03 -> W3-01/W3-02

| Position | Agent A | Agent B |
|----------|---------|---------|
| **Finding** | W3-03 should depend on W3-01 and W3-02 | Same finding |
| **Severity** | LOW -- criteria can be written before subsections exist; W3-V catches it | MEDIUM -- executor confusion if W3-03 runs first; dependency should be explicit |

**Resolution: Agent B wins (MEDIUM).**
Reasoning: While Agent A is correct that all Wave 3 tasks are in the same wave, the merged plan's acceptance criteria for W3-03 explicitly reference `reimburse_for_progress()` and `reimbursement_rate` by name. If an executor processes W3-03 before W3-01, the references dangle. The W3-V verify task mitigates but does not eliminate the risk. Making the dependency explicit costs nothing and prevents confusion.

### D2: Missing Dependency -- W5-01 -> W3-03

| Position | Agent A | Agent B |
|----------|---------|---------|
| **Finding** | W5-01 could reasonably depend on W3-03 | W5-01 should also depend on W3-03 |
| **Severity** | LOW -- diagram content derived from budget model, not criteria | LOW -- existing dependencies sufficient in practice |

**Resolution: Agreed (LOW).** Both agents rate this as low severity. The existing dependencies (W3-01, W3-02, W3-05) are sufficient since the diagram annotations derive from FR-7 content, not from the acceptance criteria list.

### D3: Gaps Count -- NFR-2 and Appendix C

| Position | Agent A | Agent B |
|----------|---------|---------|
| **Classification** | "Minor gaps from completeness assessment" (2 items noted but not called primary gaps) | Formal GAP-1 (NFR-2) and GAP-2 (Appendix C) |
| **Severity** | Low | Low |

**Resolution: Agent B's classification is more precise.** Both agents identify the same two items. Agent B correctly notes the internal contradiction in the merged plan: the completeness assessment flags these, but the "Sections Unchanged" table lists them as intentionally untouched. These are real gaps but intentionally deferred by the merged plan itself. Classification: confirmed gaps, low severity, non-blocking.

### D4: Vague Acceptance Criteria

| Position | Agent A | Agent B |
|----------|---------|---------|
| **Finding** | 0 vague criteria -- "all specific and verifiable" | 3 vague criteria (AC-1: W2-01 rationale, AC-2: W3-04 cross-refs, AC-3: W5-01 "all" debit/credit points) |

**Resolution: Agent B wins (3 low-impact criteria).** Agent A's assessment is overly generous. Agent B correctly identifies that:
- W2-01's "description paragraph present explaining injection rationale" lacks enumerated points (the merged plan specifies 3 specific points).
- W5-01's "all debit/credit points" should reference the specific count (7) from the description.
- W3-04's cross-reference criterion exists in AC but not description, creating a mild gap.
All three are low-impact since the task descriptions contain the needed detail, but the acceptance criteria themselves are technically underspecified.

### D5: Section Reference Accuracy -- W4-01 and W4-03

| Position | Agent A | Agent B |
|----------|---------|---------|
| **W4-01** | "after line 781" -- CORRECT | "after line 781" -- APPROXIMATELY CORRECT but imprecise (FR-9 starts ~779) |
| **W4-03** | "Section 4.2 (Module Disposition)" -- CORRECT | "Section 4.2" label is misleading -- no such section in spec; it's YAML frontmatter |

**Resolution: Agent B wins on W4-03.** The spec does not have a "Section 4.2" heading. The merged plan uses this as an organizational label, and the tasklist inherits it. The task description body correctly identifies lines 25-28 in YAML frontmatter, so the impact is low, but Agent B's observation is factually correct. W4-01 is a draw -- both are functionally correct.

### D6: Wave Collapse Opportunity

| Position | Agent A | Agent B |
|----------|---------|---------|
| **Recommendation** | Collapse Wave 5 into Wave 4 (save 1 wave cycle, 6->5 waves) | Wave 4+5 could merge but saves minimal time and adds complexity |
| **Assessment** | Recommended | Not recommended |

**Resolution: Agent B wins (keep 6 waves).** The savings from collapsing one wave boundary are marginal for a spec amendment where correctness matters more than speed. The current 6-wave structure provides clearer execution boundaries and simpler verification. The optimization is noted but not recommended.

---

## Merged Findings

### Confirmed Gaps (deduplicated)

| # | Gap | Source | Severity | Blocking? |
|---|-----|--------|----------|-----------|
| G1 | NFR-2 measurement language should reference `ledger.can_launch()` | Both agents (A: minor gap, B: GAP-1) | LOW | No |
| G2 | Appendix C missing v1.2.0 amendment traceability row | Both agents (A: minor gap, B: GAP-2) | LOW | No |
| G3 | IE-4, IE-5, IE-6, IE-8, IE-9 missing from Cross-Cutting Notes | Both agents | LOW-MEDIUM | No |

**Note on G1/G2**: The merged plan's own "Sections Unchanged" table marks NFR-2 and Appendix C as intentionally untouched. The completeness assessment contradicts this. These gaps exist within the merged plan's internal logic, not the tasklist's coverage of it.

### Confirmed Dependency Issues

| # | Issue | Source | Severity | Recommendation |
|---|-------|--------|----------|----------------|
| DEP-1 | W3-03 missing dependency on W3-01 and W3-02 | Both agents | MEDIUM | Add explicit deps |
| DEP-2 | W5-01 could depend on W3-03 | Both agents | LOW | No change needed |

### Acceptance Criteria Issues

| # | Issue | Task | Severity | Recommendation |
|---|-------|------|----------|----------------|
| AC-1 | "Injection rationale" paragraph lacks enumerated points | W2-01 | LOW | Add: "(a) caller owns budget, (b) prior consumption in steps 1-7, (c) step 9 reservation" |
| AC-2 | Cross-reference criterion in AC but not description | W3-04 | LOW | No change needed (AC is authoritative) |
| AC-3 | "All debit/credit points" should specify count (7) | W5-01 | LOW | Change to "all 7 debit/credit points enumerated in description" |

### Wave Optimization Opportunities

| # | Opportunity | Savings | Recommendation |
|---|------------|---------|----------------|
| OPT-1 | Collapse Wave 5 into Wave 4 | 1 wave cycle | NOT RECOMMENDED -- clarity over speed for spec amendments |
| OPT-2 | Overlap Wave 1 and Wave 2 | Partial parallelism | NOT RECOMMENDED -- Wave 1 scope boundaries inform Wave 2 review |
| OPT-3 | Move W4-01 into late Wave 3 sub-batch | Minor parallelism | NOT RECOMMENDED -- negligible benefit, adds complexity |

### Interaction Effects Coverage

| IE | In Cross-Cutting Notes? | Implicitly Covered? | Action |
|----|------------------------|---------------------|--------|
| IE-1: FR-7 <-> FR-7.1 budget ownership | YES | -- | None |
| IE-2: Cost constants <-> FR-10 logging | YES | -- | None |
| IE-3: FR-7 <-> Appendix A diagrams | YES | -- | None |
| IE-4: Baseline <-> FR-7 AC traceability | NO | Yes, by W1-05 method list | Add to notes (low priority) |
| IE-5: reimbursement_rate multiple consumers | NO | Partially, W3-01 risk field | **Add to notes (medium priority)** |
| IE-6: TurnLedger location (sprint vs pipeline) | NO | Yes, by W3-04 + W5-03 | Add to notes (low priority) |
| IE-7: Budget domain confusion | YES | -- | None |
| IE-8: attempt_remediation parallel path | NO | No task modifies this area | Add to notes (low priority) |
| IE-9: ConvergenceBudget rejection | NO | Partially, by contradiction #3 | Add to notes (low priority) |

---

## Final Verdict

| Metric | Value |
|--------|-------|
| **Overall confidence** | **HIGH** |
| **Total confirmed gaps** | 3 (G1, G2, G3) |
| **Total confirmed issues** | 12 (3 gaps + 2 dep issues + 3 AC issues + 3 wave notes + 1 ref inaccuracy) |
| **Blocking issues** | **0** |

### Recommended Actions Before Execution (ordered by priority)

1. **Add missing dependency W3-03 -> W3-01, W3-02** (DEP-1, MEDIUM). Explicit dependency prevents executor confusion when referencing `reimburse_for_progress()` and cost constants in acceptance criteria.

2. **Add IE-5 (reimbursement_rate multiple consumers) to Cross-Cutting Notes** (G3 partial, MEDIUM). This is the highest-priority missing interaction effect because v3.05 and v3.1 both consume `reimbursement_rate`, creating a cross-version coordination concern.

3. **Tighten 3 acceptance criteria** (AC-1, AC-2, AC-3, LOW). Enumerate injection rationale points in W2-01; specify count of 7 debit/credit points in W5-01.

4. **Add remaining missing IEs (IE-4, IE-6, IE-8, IE-9) to Cross-Cutting Notes** (G3 remainder, LOW). Reduces executor surprise for edge cases.

5. **Optionally add NFR-2 and Appendix C tasks** (G1, G2, LOW). Only if the merged plan's internal contradiction is resolved in favor of the completeness assessment. Otherwise, accept as intentionally deferred.

### Execution Readiness

The tasklist is **ready for execution** as-is. The recommended actions above are improvements, not prerequisites. The most impactful action (DEP-1) is a one-line dependency addition. The tasklist achieves 100% edit coverage with correct wave ordering, verified line references, and specific acceptance criteria throughout.
