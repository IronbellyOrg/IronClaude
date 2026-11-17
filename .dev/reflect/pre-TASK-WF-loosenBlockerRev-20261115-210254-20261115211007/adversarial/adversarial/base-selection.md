# Base Selection

## Quantitative Scoring (50% weight)

Two independent evaluators (sonnet class, a different class from both advocates, which ran as opus and haiku) scored the two cards in opposite orders. Full per-metric arithmetic and the 30-criterion CEV tables are in `debate/scoring-pass1.md` (order V1, V2) and `debate/scoring-pass2.md` (order V2, V1).

| Metric (weight) | Pass 1 V1 | Pass 1 V2 | Pass 2 V1 | Pass 2 V2 |
|---|---|---|---|---|
| Quantitative total | 0.765 | 0.877 | 0.766 | 0.908 |

Mean quantitative: V1 0.7655, V2 0.8925. V2 leads on requirement coverage (7 of 9 content points against 4).

## Qualitative Scoring (50% weight): additive binary rubric

| | Pass 1 V1 | Pass 1 V2 | Pass 2 V1 | Pass 2 V2 |
|---|---|---|---|---|
| Criteria MET of 30 | 25 | 24 | 24 | 24 |
| Correctness criteria MET of 5 | 4 | 4 | 4 | 4 |

Mean qualitative: V1 24.5/30 = 0.8167, V2 24/30 = 0.8000.

### Edge Case Floor Check

Invariant and edge-case dimension: pass 1 V1 5/5, V2 4/5; pass 2 V2 5/5, V1 4/5. Both variants clear the 1/5 floor and are eligible as base.

## Position-Bias Mitigation

The two passes used opposite evaluation orders. They agree on the winner and on every correctness subtotal. The combined scores differ by 0.016 (V1) and 0.015 (V2) between passes, which is below the re-evaluation trigger. No criterion-level disagreement needed a third pass (verdicts changed: 0).

## Combined Scoring

| Variant | Pass 1 | Pass 2 | Mean combined |
|---|---|---|---|
| Variant 1 (reviewer-1 card, analyzer, haiku class) | 0.799 | 0.783 | 0.791 |
| Variant 2 (reviewer-2 card, qa, opus class) | 0.839 | 0.854 | 0.8465 |

Margin: 0.0555 (5.6 percent of the scale), above the 5 percent tiebreaker band, so no tiebreaker applied.

## Selected Base: Variant 2 (reviewer-2 card, qa persona, opus class)

**Selection rationale.** Variant 2 covers 7 of the 9 content diff points and won the two highest-severity points (C-005, C-006) plus C-008. Both scoring passes put it first.

**Strengths to preserve from the base.** The three owner-gate findings with line evidence (F1, F2), the self-trip and mirror finding (F3), the pointer-only T3 finding (F4), and the longer Checked section.

**Strengths to incorporate from the non-base variant.**
- V1 F2 (C-003): the analysis template gets a digest and a `v2` row that the 11-row registry does not have.
- V1 F3 (C-004): the fresh-findings evaluation has no task.
- V1's cleaner single-cause statement of the Task 40 mirror finding (C-001), kept apart from the self-trip.

**Base weaknesses the debate corrected.**
- V2 F1 overstated "Tasks 11 to 46 run straight through": the executor does read Constraints (SKILL.md:105, refs/qa.md:52), but QA can anchor only a breach visible in a diff, and nothing in `/sc:implement` can pause for an owner go.
- V2 F3 bundled two defects, and the self-trip half depends on the executor's wording (minor).
- V2 F6 (coverage matrix) is accurate in substance but is a review-run artifact, not a plan defect (minor).
- V2's "Do not STOP. Do not split." quote (SKILL.md:72) is the N>=20 notice, not a phase-gate rule; F1 stands on SKILL.md:46, :56 and :87.

**Judge rulings on the open grades** (judge class: sonnet, disjoint from the debaters).
- C-004: blocking in widened form (the held-out split of Task 5 is also never evaluated; merged-requirements.md:934 names the held-out evaluation as plan work).
- C-007: minor (wording-dependent; Task 13's acceptance line at PLAN:170 needs only a path list).
- C-009: minor.
