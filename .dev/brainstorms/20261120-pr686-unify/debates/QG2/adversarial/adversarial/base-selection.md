# Base Selection Report

Scorer: the orchestrating session itself (single evaluator). Depth quick: the per-criterion tables are condensed to per-dimension notes, and the separate reverse-order second pass was not run (declared in the return contract as `fallback_mode: true`).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (OURS) | Variant B (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.00 (OD-3, OD-4, OD-5 all answered) | 1.00 (all three answered) |
| internal_consistency | 0.25 | 0.95 (states both cap texts honestly) | 0.90 (says "cap makes the notice safe" yet its own risk says default 0 means no cap) |
| specificity_ratio | 0.15 | 0.95 (re-count 25/30, 17/21, 8/9; line cites) | 0.90 (line cites; fewer counts) |
| dependency_completeness | 0.15 | 0.95 (D:nnn and INV refs resolve; one `D15` path given) | 0.95 |
| section_coverage | 0.15 | 1.00 (6 of 6) | 1.00 (6 of 6) |
| **quant_score** | | **0.9725** | **0.9525** |

## Qualitative Scoring (50% weight)

| Dimension | Variant A | Variant B | Note |
|-----------|-----------|-----------|------|
| Completeness | 4/5 | 4/5 | Both lack the owner's own position on naming (UNVERIFIED that none exists) |
| Correctness | 4/5 | 3/5 | B says the notice "needs no new design from the owner" while the sender, nine rows and cap are unbuilt or unruled |
| Structure | 5/5 | 5/5 | Identical template |
| Clarity | 4/5 | 4/5 | |
| Risk Coverage | 4/5 | 4/5 | |
| Invariant & Edge Case Coverage | 4/5 | 3/5 | A: masking limits, INV-013, INV-014; B: INV-013, bad cap value |
| **qual_score** | **25/30 = 0.833** | **23/30 = 0.767** | Edge case floor (>=1/5): both eligible |

## Position-Bias Mitigation
Not run as two separate passes at depth quick. Mitigation used instead: the two advocates received symmetric prompts and the same files. Disagreements re-evaluated: 0. Final verdicts changed: 0.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (OURS) | 0.486 | 0.417 | **0.903** | 7 of 12 points won or tied to A |
| B (CLAY) | 0.476 | 0.383 | **0.859** | 2 of 12 (C-002 per its advocate; C-005 on the fact) |

**Margin**: 4.4% (below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate points won): A wins; level 2 (correctness criteria MET: A 4, B 3) agrees.

## Selected Base: Variant A (OURS, position-OURS.md)

### Selection Rationale
A wins on the weighting rule and on the evidence: it keeps the safety channel independent of a wording rule (INV-013, D:692), it matches the 25-of-30 practice, and it names triggers for each deferral. B's correctness slips: "needs no new design from the owner" is contradicted by the unbuilt sender (UNVERIFIED in B itself).

### Strengths to Preserve from Base
1. Scope B and U54 before switching the rule on.
2. Fail open on delivery, written with a log.
3. Entry lines as the first channel; ledger-only owner rule.
4. Named triggers for deferred pieces.

### Strengths to Incorporate from Non-Base Variants
1. From Variant B, Section "Cited facts" 1, 2, 7: visible mask marker and fenced paths in the escalation template (C-003 hybrid).
2. From Variant B, "Mechanism" and fact 8 of D:847: offline scan of every template and fixture plus the fake `launch.effective` test, independent of scope (X-002 hybrid).
3. From Variant B, fact 6 and D:825: escalation shape rules (one per PR, warnings never reach the person, entry always written, cap never drops an entry) (U-004).
4. From Variant B, facts 6, 7: a reserved notice for AU4a, AU4c, AU5 only, with cap 5 written once the owner records it, and a tested sender (C-004 hybrid).
5. From the A-002 and A-003 answers: the rulings are Clay's, not shown to be the owner's; entry lines suffice for held items but not for post-merge hits.
