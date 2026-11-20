# Base Selection Report

Variants: V1 = `reviewer-cards/reviewer-1-card.md` (analyzer, sonnet), V2 = `reviewer-2-card.md` (qa, haiku), V3 = `reviewer-3-card.md` (refactorer, opus). Scoring per `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md`. Where the protocol's metrics assume a design document, they are applied to a review card as stated in each row. The "source requirements" for RC are the 14 content points C-001 to C-014 of `diff-analysis.md`, and a point counts only if the card raised it with a finding that the orchestrator verified (`round2-rebuttals.md`).

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|--------|--------|---------------|---------|-----------------|
| requirement_coverage | 0.30 | 0.357 (5/14: C-004, C-007, C-008, C-009, C-013) | 0.286 (4/14: C-003, C-004, C-005, C-014) | 0.643 (9/14: C-001, C-002, C-004, C-006, C-007, C-009, C-010, C-011, C-012) |
| internal_consistency | 0.25 | 0.958 (1 of ~24 claims contradicted: Q-1 FIXED against its own M-5) | 0.889 (2 of ~18: Blocking label vs MEDIUM column; "order is sound") | 0.967 (1 of ~30: M-3 overstates what the guard sees) |
| specificity_ratio | 0.15 | 0.882 (15 file:line anchors vs 2 hedges) | 0.909 (10 vs 1) | 0.983 (57 vs 1) |
| dependency_completeness | 0.15 | 1.000 (every finding id referenced resolves) | 1.000 | 1.000 |
| section_coverage | 0.15 | 1.000 (4 H2, the maximum) | 0.750 (3 of 4) | 0.750 (3 of 4) |
| **quant_score** | | **0.779** | **0.707** | **0.845** |

Arithmetic: V1 = 0.1071 + 0.2395 + 0.1323 + 0.15 + 0.15 = 0.779; V2 = 0.0858 + 0.2223 + 0.1364 + 0.15 + 0.1125 = 0.707; V3 = 0.1929 + 0.2418 + 0.1475 + 0.15 + 0.1125 = 0.845. Counts came from `grep` on the cards (anchors, hedge words, H2 headings) and from the diff analysis; contradiction counts are my reading and are the soft part of this layer.

## Qualitative Scoring (50% weight): additive binary rubric

CEV rule applied: a MET needs a cited place in the card; otherwise NOT MET. Evidence cites the card's own item ids.

### Completeness

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | Q-1..Q-10, six decisions, R1..R33 coverage | MET | same plus "33 of 33" | MET | same plus per-task Q map |
| Addresses edge cases/failures | MET | M-1 zero or several items, M-4 budget | MET | QA-2 missing-hash case, QA-4 zero/several Projects | MET | B-1 fail-open path, B-2 empty Pipeline |
| Includes dependencies/prerequisites | MET | M-1 helper order | MET | "every dependency names an earlier task" | MET | M-1 same-file pairs |
| Defines success/completion criteria | MET | a Fix per finding | MET | a Fix per QA item | MET | a Fix per finding |
| Specifies out-of-scope items | MET | "Not checked" list | MET | "Not checked" list | MET | "Not checked" list |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors | NOT MET | Q-1 FIXED; case run shows bare `p.complete.run()` unmatched | NOT MET | "ordering sound" false (plan:30 omits Task 10) | NOT MET | M-3 overstates guard visibility of script `gh api` calls |
| Feasible with stated constraints | MET | fixes fit the plan's files | MET | fixes fit | MET | fixes fit |
| Terminology consistent | MET | Q-/M-/N- used one way | MET | | MET | |
| No internal contradictions | NOT MET | Q-1 FIXED vs M-5 "acceptance checks do not pin which" | NOT MET | Blocking label vs MEDIUM column | MET | none found |
| Claims supported by evidence | MET | line cites re-verified | MET | `approval_record.py:313-359`, guard 444 verified | MET | B-1, B-2 verified |
| **Subtotal** | **3/5** | | **3/5** | | **4/5** | |

### Structure

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Logical ordering | MET | summary, Q-list, coverage, findings | MET | findings then recheck then coverage | MET | summary, Q-list, findings |
| Consistent hierarchy | MET | | MET | | MET | |
| Separation of concerns | MET | | MET | | MET | |
| Navigation aids | MET | ids M-1..N-2 | MET | ids QA-1..4 | MET | ids B/M/N with task and action |
| Follows artifact conventions (the brief's grading scheme) | MET | Medium and Note used | NOT MET | Blocking in prose, MEDIUM in column | MET | Blocking (Safety/Decision), Medium, Note with affected action |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Clarity

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | NOT MET | "probably need an ISSUE entry", M-4 "[INFERRED] ... or note" | NOT MET | severity label ambiguous | MET | one hedge only |
| Concrete | MET | | MET | | MET | |
| Each section has a clear purpose | MET | | MET | | MET | |
| Terms defined on first use | MET | | MET | | MET | |
| Actionable next steps | MET | Fix lines | MET | Fix lines | MET | Fix lines |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Risk Coverage

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | severity only | NOT MET | severity only | MET | B-1 "live even with the gate closed" plus affected action |
| Mitigation for each risk | MET | | MET | | MET | |
| Failure modes and recovery | MET | M-4 `budget_exhausted` | NOT MET | none | MET | B-2 refusal outcome, M-3 known limit |
| External dependencies | MET | M-4 call cap, N-2 docs | NOT MET | "live GitHub not checked" only | MET | M-3 pr-submit, B-1 |
| Monitoring or validation mechanism | MET | tests named per finding | MET | tests named | MET | tests named |
| **Subtotal** | **4/5** | | **2/5** | | **5/5** | |

### Invariant and Edge Case Coverage

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Boundary conditions for collections | MET | M-1 zero or several items | MET | QA-4 zero and several Projects | MET | B-2 empty Pipeline |
| State interactions across components | MET | M-2 store vs retry | MET | QA-2 claim event vs plan approval | MET | B-1 repo across `stage-status` and the cycle |
| Guard condition gaps | MET | M-5 over-matches | MET | QA-3 | MET | M-4, N-4 |
| Count divergence | MET | N-1 `GRID_CLASSES` and import-time assert | NOT MET | only "33 of 33" | MET | N-2 one-second resolution |
| Interaction effects | MET | M-4 gate and call budget | MET | QA-4 Task 19 with Task 24 | MET | B-3 Task 6 with Task 11 |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

Edge case floor (at least 1/5 on this dimension): V1 5/5, V2 4/5, V3 5/5. All eligible.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 3/5 | 3/5 | 4/5 |
| Structure | 5/5 | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 5/5 |
| Risk Coverage | 4/5 | 2/5 | 5/5 |
| Invariant and Edge Case | 5/5 | 4/5 | 5/5 |
| **qual_score** | **26/30 = 0.867** | **22/30 = 0.733** | **29/30 = 0.967** |

## Position-Bias Mitigation

Pass 1 evaluated V1, V2, V3; Pass 2 evaluated V3, V2, V1. Criteria where the two passes first differed, and the re-evaluation against both passes' evidence:

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness: no factual errors | V3 | MET | NOT MET | DISAGREE | NOT MET (M-3 overstated; the card's own plan:24 reading says the guard is text-only) |
| Correctness: no internal contradictions | V1 | MET | NOT MET | DISAGREE | NOT MET (Q-1 FIXED against M-5) |
| Clarity: unambiguous language | V1 | MET | NOT MET | DISAGREE | NOT MET ("probably", "[INFERRED]... or note") |
| Risk: at least 3 risks with probability | V3 | NOT MET | MET | DISAGREE | MET (B-1 gives likelihood and the affected action) |
| Risk: external dependencies | V1 | NOT MET | MET | DISAGREE | MET (M-4 35-call cap) |

Disagreements re-evaluated: 5. Final verdicts changed relative to Pass 1: 3. The pass 1 and pass 2 sheets were not saved as separate files; the table lists only the differing rows.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (analyzer, sonnet) | 0.390 | 0.433 | **0.823** | not needed |
| V2 (qa, haiku) | 0.354 | 0.367 | **0.720** | not needed |
| V3 (refactorer, opus) | 0.423 | 0.483 | **0.906** | not needed (V3 also won 11.5 of 20 scored points in `debate-transcript.md`) |

**Margin**: 0.083 between V3 and V1 (above the 0.05 threshold). **Tiebreaker applied**: No.

## Selected Base: Variant 3 (reviewer-3 card, refactorer, opus)

### Selection Rationale
V3 leads on both layers: it raised 9 of the 14 content points against 5 and 4, it is the only card with the owner's category per finding (Safety, Decision) and the affected action, and it carries the two verified safety and behaviour findings (C-001, C-002) that the others missed. Its weak spots are bounded: M-3 overstates what the guard sees (C-011), M-5 and N-1 are wording, and it missed C-003, C-005, C-008 and C-014.

### Strengths to Preserve from Base
1. B-1 (cross-repo approval read), B-2 (empty Pipeline), B-3 (brief levels) with evidence, fix and affected action.
2. The B/M/N grading with category per finding and the Q-1..Q-10 recheck with PARTIAL calls on Q-6 and Q-10.
3. M-1 (same-file pairs), M-2 (retry has no stored Status), M-4 (over-match contradiction), N-3 to N-5.

### Strengths to Incorporate from Non-Base Variants
1. From V2: QA-2 (claim-time check cannot pass in `test_approval_record.py`, re-pointed at `stage_predicates`), QA-1 (R6/R9 lifecycle, graded Medium), QA-3 (bare `p.complete.run()` unmatched, now run), QA-4 (Task 19 vs Task 24 Project count and missing R14 cases).
2. From V1: M-1 (Task 5 needs the live-item helper first, zero or several items), M-3 (Task 9 cites a runtime value), M-5 (over-matches on `git`, `sed`, `ruff`), N-1 (three test pins) and N-2 (two docs lines with version 1).
3. Orchestrator additions: the case-test table for C-004 and the stage_predicates location for C-003 (`round2-rebuttals.md`).
