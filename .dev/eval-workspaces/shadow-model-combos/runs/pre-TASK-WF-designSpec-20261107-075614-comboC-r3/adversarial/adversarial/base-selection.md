# Base Selection

Method note (honest limits): the quantitative layer uses proxies suited to reviewer cards, not roadmaps. RC = share of the 9 consensus findings (M1..M9, see refactor-plan.md) the card contains; IC = 1 - contested claims / claims (a claim a Round 2 advocate conceded or refuted counts as contested); SR = concrete over concrete plus vague statements; DC = resolved internal references / references (the T2 calibrator's off-by-one line notes count as unresolved for V2); SC = H2 headings / max H2 headings. Both position-bias passes were run by the orchestrator itself (input order, then reverse), not by an independent agent; they produced no verdict differences. The orchestrator is a sonnet-class model, the same class as reviewer 1 (judge_class_collision: true).

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC | 0.30 | 0.333 (M1, M2, M8) | 0.556 (M3, M4, M5, M6, M9) | 0.556 (M1, M2, M3, M4, M7) |
| IC | 0.25 | 1.00 | 0.95 (plan:33 over-read) | 0.95 (F2 overreach) |
| SR | 0.15 | 0.95 | 0.93 | 0.95 |
| DC | 0.15 | 1.00 | 0.90 | 1.00 |
| SC | 0.15 | 1.00 (4 H2) | 0.25 (1 H2) | 0.75 (3 H2) |
| quant_score | | 0.7925 | 0.7162 | 0.8092 |

## Qualitative Scoring (50% weight): additive binary rubric (30 criteria, CEV; MET only with cited evidence)

| Dimension | V1 | V2 | V3 | Evidence (MET counts) |
|---|---|---|---|---|
| Completeness (5) | 2 | 4 | 4 | V1 states it covered Tasks 1-4 and 9 only; V2 and V3 span all tasks; V3 misses cycle-id and retry |
| Correctness (5) | 3 | 3 | 4 | V1 F2 downgraded after plan:140 check; V2 F1 over-reads plan:33; V3 F2 overreach conceded; all claims re-read OK |
| Structure (5) | 4 | 3 | 4 | V2 has one H2; V1 and V3 have summary, findings, verified-rows |
| Clarity (5) | 3 | 3 | 4 | V3 gives sources and failing test; V1 remedy vague |
| Risk coverage (5) | 3 | 3 | 3 | no card covers exit-path held reports (INV-012) |
| Invariant and edge-case coverage (5) | 2 | 3 | 3 | floor 1 of 5: all variants eligible |
| qual_score (total/30) | 17/30 = 0.567 | 19/30 = 0.633 | 22/30 = 0.733 | |

## Position-Bias Mitigation

Pass 1 (V1, V2, V3) and Pass 2 (V3, V2, V1) gave identical verdicts on all 90 criterion-variant pairs; disagreements_found 0; verdicts_changed 0.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Final |
|---|---|---|---|
| V1 | 0.3963 | 0.2833 | 0.6796 |
| V2 | 0.3581 | 0.3167 | 0.6748 |
| V3 | 0.4046 | 0.3667 | 0.7713 |

Margin V3 over V1: 9.2 points; no tiebreaker applied.

## Edge Case Floor Check

All three variants score at least 2 of 5 on the invariant dimension: eligible.

## Selected Base: Variant 3 (reviewer-3, refactorer, opus class)

- Rationale: highest combined score (0.7713), widest repo-grounded coverage (Tasks 1-13), named input sources for resume row 4, and the strongest pin evidence (whole-line classification keys).
- Strengths to preserve: F1 sources and failing test; F3 whole-line pin (widened to every existing Wave bullet); F4 same-file ordering; the "sound rows" list.
- Strengths to incorporate: V1 F2 (wording ambiguity, MINOR), V1 F3 (guard_status halt reason), V1's vacuous-head-check mechanism and its category labels; V2 F1 (cycle-id equality test, MINOR), V2 F2 (FR-16 retry bound, MAJOR), V2 F3 (crash boundaries), V2's concrete git-verb failure consequence; probe findings INV-012 (exit-path held reports) and INV-009.
