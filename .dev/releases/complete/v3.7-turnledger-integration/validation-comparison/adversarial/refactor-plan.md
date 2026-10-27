# Refactoring Plan

## Overview
- **Base variant**: Variant A (Claude Report) — score 0.819
- **Incorporated from**: Variant B (GPT Report) — score 0.753
- **Total planned changes**: 8
- **Risk level**: Medium (modifies metrics and adds findings, but preserves structure)

---

## Planned Changes

### Change #1: Add GAP-H007 — FR-7.1 Schema Conflict (HIGH)
- **Source**: Variant B, GAP-H005
- **Target**: Gap Registry, after GAP-H006
- **Integration approach**: Insert new HIGH gap entry
- **Rationale**: Verified genuine conflict — roadmap L47 lists 9-field schema, spec FR-7.1 shows 10 fields including `duration_ms`. Debate Round 1 evidence: 92% confidence.
- **Risk**: Low (additive)

### Change #2: Add GAP-H008 — FR-7.3 Flush Semantics Conflict (HIGH)
- **Source**: Variant B, GAP-H006
- **Target**: Gap Registry, after Change #1
- **Integration approach**: Insert new HIGH gap entry
- **Rationale**: Verified genuine conflict — roadmap L48 says "auto-flushes on session end", spec FR-7.3 says "auto-flushes after each test". Directly impacts FR-3.3 interrupted sprint testing. Debate Round 1: 92% confidence.
- **Risk**: Low (additive)

### Change #3: Add GAP-M006 — FR-5.2 Positive-Case Test Gap (MEDIUM)
- **Source**: Variant B, GAP-M002
- **Target**: Gap Registry, after existing MEDIUM findings
- **Integration approach**: Insert new MEDIUM gap entry
- **Rationale**: Spec FR-5.2 (L403-414) explicitly requires both positive and negative synthetic tests. Roadmap task 3B.3 only describes negative case. Debate Round 1: 85% confidence.
- **Risk**: Low (additive)

### Change #4: Add GAP-M007 — Boundary/Count Inconsistency (MEDIUM)
- **Source**: Variant B, GAP-H007 (downgraded from HIGH to MEDIUM — presentational issue, not implementation-blocking)
- **Target**: Gap Registry, after Change #3
- **Integration approach**: Insert new MEDIUM gap
- **Rationale**: Roadmap L271 says "13 requirements" — ambiguous and potentially misleading. Actual atomic FR count is 47; total with SCs and constraints is ~65.
- **Risk**: Low (additive)

### Change #5: Correct D1 Domain Score
- **Source**: Ground-truth verification + Variant B's domain scoring
- **Target**: Coverage by Domain table, D1 row
- **Integration approach**: Modify D1 from "25 | 25 | 0 | 0 | 100%" to "25 | 22 | 0 | 3 | 88.0%"
- **Rationale**: FR-1.19, FR-1.20, FR-1.21 are confirmed MISSING. The adversarial pass already identified them, but the D1 domain table was not updated. This fixes the internal inconsistency. Debate evidence: X-002, X-005 (80-85% confidence).
- **Risk**: Medium (modifies existing data, cascades to aggregate metrics)

### Change #6: Correct Requirement Universe and Metrics
- **Source**: Ground-truth count (~65 requirements)
- **Target**: Frontmatter, Executive Summary, Aggregate Metrics
- **Integration approach**: Revise total_requirements from 84 to 65; recalculate covered/partial/missing; recalculate coverage scores
- **Rationale**: Ground truth from spec enumeration: 47 FRs + 12 SCs + 6 constraints = 65. Original 84 over-counts by treating sub-assertions as separate requirements. Debate evidence: X-001 (72% confidence).
- **Risk**: High (cascading metric changes throughout document)

### Change #7: Correct Integration Wiring — `_run_checkers()`
- **Source**: Variant B integration audit
- **Target**: Integration Wiring Audit section
- **Integration approach**: Change `_run_checkers()` from implicit FULLY_WIRED to PARTIALLY_WIRED with note about FR-5.2 positive-case gap
- **Rationale**: Variant B correctly identifies the checker test surface is partial. Debate evidence: X-004 (70% confidence).
- **Risk**: Low (single cell change)

### Change #8: Add FR-6.1/6.2 Specificity Notes
- **Source**: Variant B, GAP-M003/M004
- **Target**: Gap Registry, as LOW-severity notes appended to existing GAP-L entries
- **Integration approach**: Add LOW-severity note about task description vagueness
- **Rationale**: Partially valid concern — cross-references exist but "extend existing/add any missing" language is vague. Debate evidence: U-005 (68% confidence).
- **Risk**: Low (additive note)

---

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Rejection |
|------------|-------------------|------------------------|
| 4-domain decomposition | Variant B uses 4 merged domains | Variant A's 7-domain model provides more targeted analysis per functional area (S-001, 82% confidence) |
| Sequential gap IDs without [ADV] prefix | Variant B doesn't separate adversarial finds | [ADV] tagging provides discovery provenance transparency (S-002, 75% confidence) |
| No REJECTED section | Variant B has 0 rejections | REJECTED section demonstrates adjudication rigor (S-006, 90% confidence) |
| 62 requirement count | Variant B's original count | Neither 84 nor 62 is correct; using ground-truth ~65 instead |
| Narrative CC table | Variant B uses prose-style cross-cutting | Structured PASS/FAIL/WARNING table is more scannable (S-004, 65% confidence) |

---

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1-4 | Low | Additive gaps — no existing content modified | Remove entries |
| #5 | Medium | Cascades to domain summary; may confuse readers familiar with original | Revert D1 row |
| #6 | High | Changes frontmatter, summary, and metrics throughout | Revert to original counts |
| #7 | Low | Single cell in integration table | Revert cell |
| #8 | Low | Additive note | Remove note |

---

## Review Status

- **Approval**: Auto-approved (non-interactive mode)
- **Timestamp**: 2026-03-23T00:00:00Z
