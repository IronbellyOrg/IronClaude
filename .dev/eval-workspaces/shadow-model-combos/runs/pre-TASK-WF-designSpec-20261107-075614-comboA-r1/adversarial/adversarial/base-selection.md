judge_model_class: opus (claude-gw-tier3 orchestrator session)

# Base selection (Step 3)

Variants: V1 = reviewer-1 (sonnet:analyzer, 8 findings), V2 = reviewer-2 (haiku:qa, 4 findings), V3 = reviewer-3 (opus:refactorer, 12 findings).

## Quantitative pass

Weights: RC 0.30, IC 0.25, SR 0.15, DC 0.15, SC 0.15.

- **RC (requirement coverage)**: the share of the 15 INF rows in `artifacts/coverage-matrix.yaml` that at least one finding touches, through its FR refs or its spec citation.
  - V1 covers INF-001, 002, 005, 006, 007, 012, 013 and 014 (8 of 15).
  - V2 covers INF-003, 007, 008, 009, 013 and 014 (6 of 15).
  - V3 covers INF-001, 002, 003, 007, 008, 009, 011, 012, 013, 014 and 015 (11 of 15).
  - No card touches INF-004 or INF-010.
- **IC (internal consistency)**: 1 - contradictions/claims, where a contradiction is a claim refuted (counted 1) or overstated (counted 0.5) against the frozen inputs.
  - V1: 0 of 8.
  - V2: 0 of 4.
  - V3: F3 is refuted as a defect (1), F11 is overstated (0.5) and F4's "no task owns" is partly rebutted by plan:108 (0.5), so 2 of 12.
- **SR (specificity)**: 0.5 × min(1, mean citations per finding / 3) + 0.5 × (share of findings carrying a quoted citation).
  - V1: 19 citations / 8 = 2.38; 7 of 8 quoted.
  - V2: 10 / 4 = 2.5; 0 of 4 quoted.
  - V3: 40 / 12 = 3.33; 11 of 12 quoted.
- **DC (dependency resolution)**: the share of citations that resolve to the claimed content on re-read. All citations of all three cards resolved.
- **SC (section coverage)**: the share of the 14 plan sections (Constraints plus Tasks 1 to 13) cited.
  - V1: Tasks 2, 3, 4, 8, 9, 10 and 11 (7).
  - V2: Tasks 1, 5, 8, 10 and 11 (5).
  - V3: Tasks 1, 3, 5, 7, 8, 9, 10, 11, 12 and 13 (10).

| Metric | V1 | V2 | V3 |
|---|---|---|---|
| RC | 0.533 | 0.400 | 0.733 |
| IC | 1.000 | 1.000 | 0.833 |
| SR | 0.833 | 0.417 | 0.958 |
| DC | 1.000 | 1.000 | 1.000 |
| SC | 0.500 | 0.357 | 0.714 |
| **Quant (weighted)** | **0.760** | **0.636** | **0.829** |

## Qualitative pass (30 criteria, Claim-Evidence-Verdict)

Each cell is met (1) or not met (0). The pattern is Claim: the criterion; Evidence: the finding ids or plan/spec lines; Verdict: 1 or 0.

### Completeness

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| Q1 | Covers the Task 11 gating gap | 1 | 1 | 0 | R1-F1, R2-F2; V3 has none |
| Q2 | Covers the dependency-declaration rule (INF-011) | 0 | 0 | 1 | R3-F2 is verified against plan:134-193 |
| Q3 | Covers a fold-table row defect | 1 | 0 | 1 | R1-F3 (spec:206), R3-F11 (spec:201); R2-F4 is a corrupt-line case, not a row |
| Q4 | Covers the ref's input-section scope (section 4.2) | 0 | 1 | 0 | R2-F1 against plan:124 |
| Q5 | Covers an O1 to O4 open item | 1 | 1 | 1 | R1-F8 (O1), R2-F3 (O4), R3-F4 (O2) and R3-F5 (O4) |
| Q6 | Touches at least half the INF rows | 1 | 0 | 1 | RC above |

### Correctness

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| Q7 | No claim refuted on re-read | 1 | 1 | 0 | R3-F3: Task 13's full-suite run consumes Task 2's test changes |
| Q8 | No overstated claim | 1 | 1 | 0 | R3-F11 ("every named fold AC"), R3-F4 ("no task owns") |
| Q9 | Severities match consequence | 1 | 1 | 0 | R3-F4 MAJOR, downgraded because its failure is conditional and loud |
| Q10 | Blocking flags match the blocking rule | 0 | 1 | 1 | R1-F1 false, judged true (X-002); R2 F1 and F2 upheld; V3 flags none wrongly |
| Q11 | T1 hypotheses confirmed or refuted correctly | 1 | 1 | 1 | H1 and H4 (V1); H4 (V2); H1, H2 and H3 refuted (V3) |
| Q12 | All citations resolve | 1 | 1 | 1 | DC = 1.0 |

### Structure

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| Q13 | findings-v2 block is valid | 1 | 1 | 1 | all parse |
| Q14 | One defect per finding | 0 | 1 | 1 | R1-F6 bundles corrupt-line and the row 11 `notes` |
| Q15 | Every finding has a category and refs or citations | 1 | 1 | 1 | all |
| Q16 | Primary citations carry quotes | 1 | 0 | 1 | V2 has no quotes |
| Q17 | At least 75% of findings pair a plan and a spec citation | 1 | 1 | 1 | V1 7 of 8, V2 4 of 4, V3 10 of 12 |
| Q18 | Ids sequential, no gaps | 1 | 1 | 1 | all |

### Clarity

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| Q19 | Claims of 300 characters or fewer | 1 | 1 | 1 | all |
| Q20 | States the failure scenario | 1 | 1 | 1 | all |
| Q21 | Names exact tasks | 1 | 1 | 1 | all |
| Q22 | Plain wording | 1 | 1 | 1 | all |
| Q23 | Separates spec defects from plan defects | 1 | 0 | 1 | R1-F3 and R3-F1 note the spec tension; R2-F1 misses that spec:240 includes section 4.2 |
| Q24 | The fix is implied | 1 | 1 | 1 | all |

### Risk coverage

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| Q25 | Finds a ship-unverified (blocking-class) risk | 1 | 1 | 0 | R1-F1, R2-F1, R2-F2 |
| Q26 | Finds a live-protocol (runtime agent) gap | 1 | 1 | 1 | R1-F5, R2-F1, R3-F12 |
| Q27 | Finds an ordering or parallelism risk | 0 | 0 | 1 | R3-F2, R3-F10 |
| Q28 | Finds a pin or byte-identity risk | 0 | 1 | 1 | R2-F3, R3-F5 |
| Q29 | Finds an output-field fidelity risk | 1 | 0 | 0 | R1-F3, R1-F4 |
| Q30 | Finds a conditional open-item risk | 1 | 0 | 1 | R1-F8, R3-F4 |

| Dimension (6 each) | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 3 | 4 |
| Correctness | 5 | 6 | 3 |
| Structure | 5 | 5 | 6 |
| Clarity | 6 | 5 | 6 |
| Risk coverage | 4 | 3 | 4 |
| **Qual (of 30)** | **24 (0.800)** | **22 (0.733)** | **23 (0.767)** |

### Position-bias mitigation

- Forward pass order: V1, V2, V3. Reverse pass order: V3, V2, V1, re-scoring all 90 cells from the evidence column.
- Disagreements between the passes: 0.
- Cells re-examined as borderline in the reverse pass, all unchanged:
  - Q17 for V1 (7 of 8 paired, above the 75% threshold).
  - Q25 for V3 (R3-F11 is an unverified-artifact risk, but MINOR, so it is not blocking-class).
  - Q10 for V1 (depends on the X-002 ruling).

## Combined score and selection

| | V1 sonnet:analyzer | V2 haiku:qa | V3 opus:refactorer |
|---|---|---|---|
| Quant | 0.760 | 0.636 | 0.829 |
| Qual | 0.800 | 0.733 | 0.767 |
| **Combined (0.5 / 0.5)** | **0.780** | **0.685** | **0.798** |

- The V3 lead over V1 is 0.018, inside the 0.05 tie band, so a tiebreaker applies: structural fitness as base, meaning the share of merged findings the card's findings structure.
- Fitness: V3 sources 11 of 18 merged findings, V1 9 of 18, V2 4 of 18. The tiebreaker confirms V3.

**Selected base: V3 (opus:refactorer).**

Weaknesses of the base, corrected in the merge:
- R3-F3 rejected.
- R3-F4 downgraded to MINOR.
- R3-F11 narrowed.
- No blocking findings of its own; MF1 and MF2 are imported from V2 and V1.
