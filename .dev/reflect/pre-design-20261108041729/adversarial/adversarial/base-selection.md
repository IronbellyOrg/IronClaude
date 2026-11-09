# Base Selection

Adaptation note: the rubric of the adversarial skill is written for design documents. The variants here are three review cards, so each metric is computed from the card's findings against the debate's settled outcome. Computations are listed so they can be re-run.

## Quantitative Scoring (50% weight)

Settled valid findings (the "source requirements"), from the debate: C-001, C-002, C-003, C-004, C-005, C-006, C-007, C-008, C-009 (9).

| Metric | Weight | V1 | V2 | V3 | Computation |
|---|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.667 | 0.333 | 0.778 | valid findings raised / 9. V1: C-001..C-006 (6). V2: C-002, C-005, C-009 (3). V3: C-001, C-002, C-003, C-004, C-006, C-007, C-008 (7) |
| IC internal consistency | 0.25 | 0.714 | 0.500 | 0.714 | 1 - (findings the debate found overstated or partly wrong / findings). V1: R1-F4, R1-F6 of 7. V2: R2-F1, R2-F2 severity of 4. V3: R3-F4, R3-F7 of 7 |
| SR specificity | 0.15 | 0.857 | 1.000 | 1.000 | findings with a file:line citation / findings. V1's R1-F7 cites a data file without lines |
| DC dependency completeness | 0.15 | 1.000 | 1.000 | 1.000 | every cited path resolved in the advocates' re-reads |
| SC section coverage | 0.15 | 1.000 | 0.571 | 1.000 | findings / max findings (7) |
| **quant_score** | | **0.807** | **0.611** | **0.862** | RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15 |

## Qualitative Scoring (50% weight) — additive binary rubric

Criteria met out of 5 per dimension, with the deciding evidence (a criterion without evidence counts as not met):

| Dimension | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness | 4 | 3 | 4 | V1/V3 cover test fallout, files, docs; V2 omits C-001, C-003, C-004 |
| Correctness | 4 | 3 | 4 | Each has two overstated or partly wrong points; V2's two are the blocking labels |
| Structure | 4 | 4 | 5 | V3 has uniform finding/evidence/recommendation fields and a clean split of kinds |
| Clarity | 5 | 5 | 5 | All name file, change and verifier |
| Risk coverage | 4 | 3 | 4 | V1/V3 name the CI break; V2 names test weakness only |
| Invariant & edge-case coverage | 3 | 2 | 3 | V1/V3 cover the `orgs/` regex edge, silent drift of keys; V2 covers format/pair edges |
| **Total / 30** | 24 | 20 | 25 | |
| **qual_score** | **0.800** | **0.667** | **0.833** | total / 30 |

Edge-case floor (needs at least 1 of 5): V1 3, V2 2, V3 3. All eligible.

## Position-Bias Mitigation
Degraded and recorded as such: the orchestrator scored once in input order (V1, V2, V3). A second independent reverse-order pass was not run. The two top scores differ by under 5%, so the tiebreaker below was applied, and it does not depend on the rubric scores.

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | Combined |
|---|---|---|---|
| V3 (opus, refactorer) | 0.431 | 0.417 | **0.847** |
| V1 (sonnet, analyzer) | 0.404 | 0.400 | **0.804** |
| V2 (haiku, qa) | 0.306 | 0.333 | **0.639** |

V3 leads V1 by 0.043 (under the 0.05 tiebreaker threshold).

Tiebreaker level 1 (diff points won in Round 1 as sole winner): V3 4 (S-001, C-003, C-007, C-008); V1 3 (C-005, C-010, X-001). V3 wins at level 1.

## Selected Base: Variant 3 (opus:refactorer)
- Rationale: highest combined score (0.847), widest coverage of the settled findings (7 of 9), the only card to find C-007, and its blocking finding (C-001) was confirmed by all three advocates and both independent calibrations.
- Strengths to preserve: R3-F1 (blocking), R3-F2, R3-F3, R3-F5, the checks_done list.
- Strengths to incorporate from non-base variants:
  - V1: the checker function range `:2005-2012` and the rule that no POST line may be classified read-only (`:3150-3156`) for the C-001 fix; C-005 (mode label as well as comment); the prose-guard self-check test design for the `orgs/` scanner; the named Task 3 revert gap; `complexity-field.json` Task 1/2 naming.
  - V2: C-002 (exact formats and Q7/Q8 pair assertions, at Medium); C-009 (Will / Will Not test reads only SKILL).
