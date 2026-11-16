# Base Selection

## Quantitative Scoring (50% weight)

Two independent evaluators (sonnet class, a different class from both advocates, which ran as opus and haiku) scored the two cards in opposite orders. The 30-criterion CEV tables and the metric arithmetic are in `debate/scoring-pass1.md` (order V1, V2) and `debate/scoring-pass2.md` (order V2, V1).

| | Pass 1 V1 | Pass 1 V2 | Pass 2 V1 | Pass 2 V2 |
|---|---|---|---|---|
| Quantitative total | 0.822 | 0.817 | 0.822 | 0.879 |

Mean quantitative: V1 0.822, V2 0.848.

## Qualitative Scoring (50% weight): additive binary rubric

| | Pass 1 V1 | Pass 1 V2 | Pass 2 V1 | Pass 2 V2 |
|---|---|---|---|---|
| Criteria MET of 30 | 20 | 20 | 21 | 24 |
| Correctness criteria MET of 5 | 4 | 3 | 5 | 4 |

Mean qualitative: V1 20.5/30 = 0.683, V2 22/30 = 0.733.

### Edge Case Floor Check

Invariant and edge-case dimension: V1 3/5 in both passes; V2 5/5 in both passes. Both clear the 1/5 floor and are eligible.

## Position-Bias Mitigation

The two passes disagree on the winner: pass 1 puts V1 ahead by 0.002 (a tie), pass 2 puts V2 ahead by 0.078. They also differ on several criterion-level verdicts (for example V2's Risk coverage is 2/5 in pass 1 and 4/5 in pass 2, and V2's Clarity is 2/5 in pass 1 and 3/5 in pass 2). The disagreement is the position-bias signal the dual pass is meant to expose. Per the protocol the tiebreaker below decides, since the mean combined scores are within 5 percent.

## Combined Scoring

| Variant | Pass 1 | Pass 2 | Mean combined |
|---|---|---|---|
| Variant 1 (reviewer-1 card, analyzer, haiku class) | 0.744 | 0.761 | 0.7525 |
| Variant 2 (reviewer-2 card, qa, opus class) | 0.742 | 0.839 | 0.7905 |

Margin: 0.038 (3.8 percent of the scale), below the 5 percent line, so the tiebreaker applies.

### Tiebreaker

- Level 1, debate performance (points won in Step 2): V1 3 (X-001, C-001, A-002), V2 3 (C-002, C-003, C-005), 3 ties. Tied, so go to level 2.
- Level 2, correctness criteria count (sum over both passes): V1 4 + 5 = 9, V2 3 + 4 = 7. V1 leads. **Level 2 decides.**

## Selected Base: Variant 1 (reviewer-1 card, analyzer persona, haiku class)

**Selection rationale.** Variant 1 won the tiebreaker on correctness criteria (9 against 7). It also carries the one finding that decides the merged verdict (X-001, C-001: the Task 3 rerun overwrites hand-added evidence), and no claim of it was refuted in the debate.

**This choice moves little.** The merged card keeps every finding of both variants and the probe, so the base only fixes the card's layout and the provenance tags. The scoring passes disagree on the winner, and this document says so rather than hiding it.

**Strengths to preserve from the base.** The data-loss finding F1 with its four line citations, the list-style citations, and the plain verdict line.

**Strengths to incorporate from the non-base variant.**
- V2 F1 (always-staged constraint omitted; minor).
- V2 F2 (Task 2 frame not recorded; Medium after debate).
- V2 F3 (sizing fallback near certain, a minor note; Tasks 5 and 6 share the Task 2 sample, Medium).
- V2's Checked section: the Task 9 spec anchors, the RT1, RT2 and M12 locations, the staging decisions, the Task 4 anchors and the no-edit-outside-artifacts check.

**Base weaknesses the debate corrected.**
- V1 covered 1 of 9 tasks and missed C-002, C-003 and C-005.
- V1's "deletes Task 9's evidence pointer" overstated: the path survives, the cited content (results.md:58-74) goes.

**Judge rulings on the grades.**
- C-001: blocking (data loss, an unmet constraint and a vacuous comparison; the fix needs a decision the plan does not make).
- C-002: minor. C-003: Medium. C-004: minor note. C-005: Medium.
- Probe INV-006 (the SubagentStart hook injects the old rule into Task 4's blind graders): blocking. The plan's headline measurement is silently confounded, which is a silent wrong result under the severity rule, and the fix needs a plan decision (state the confound as a limit, or constrain the graders and record how).
- Probe INV-002, INV-005, INV-007 and the Task 10 gap: Medium. INV-009, INV-010, INV-012: minor.
