# Base Selection

Source requirement set for RC: the 9 inferred rows INF-001..INF-009 (`../artifacts/inferred-requirements.json`). Sections for SC = finding count (plus the recorded coverage line for variant 2).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (sonnet:analyzer) | Variant 2 (glm-5.3:qa) | Variant 3 (opus:refactorer) |
|---|---|---|---|---|
| RC requirement coverage (INF rows touched) | 0.30 | 4/9 = 0.44 (INF-001, 005, 006, 007) | 4/9 = 0.44 (INF-001, 005, 007, 009) | 5/9 = 0.56 (INF-001, 003, 005, 007, 008) |
| IC internal consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| SR specificity ratio | 0.15 | 1.00 (4/4 cite file:line) | 1.00 (4/4) | 0.89 (8/9; F9 has no target line) |
| DC dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| SC section coverage | 0.15 | 4/9 = 0.44 | 5/9 = 0.56 | 9/9 = 1.00 |
| **quant_score** | | **0.748** | **0.766** | **0.852** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV summary per dimension (MET counts; evidence = card finding ids, debate transcript rounds).

| Dimension | V1 | V2 | V3 | Evidence notes |
|---|---|---|---|---|
| Completeness | 2/5 | 3/5 | 4/5 | V3 covers edge cases (F2, F3), dependencies (F6 ordering), success criteria (F1 red log); V2 coverage line (criterion 1); V1 dependencies (F1 Makefile) |
| Correctness | 3/5 | 5/5 | 4/5 | V1 R1-F4 factually wrong (calibrator, Round 1 concession) → criterion 1 NOT MET; V1 severity overclaim → criterion 5 NOT MET; V3 F1 severity overclaim (conceded) → criterion 5 NOT MET |
| Structure | 4/5 | 4/5 | 4/5 | All: id/headline/location/class/severity/fix; none has navigation aids |
| Clarity | 4/5 | 4/5 | 4/5 | All concrete; V1 F3 and V3 F9 have no actionable step (criterion 5) |
| Risk Coverage | 3/5 | 3/5 | 4/5 | V3 names failure modes of the test itself (F1, F2) and the blocked-basename path (F4) |
| Invariant & Edge Case | 1/5 | 1/5 | 3/5 | V3: collection boundary (F2 empty scan), guard gap (F1), interaction (F4); V1: guard (F1 constraint vs delete); V2: boundary (F4 `<REPORT.md`) |
| **qual_score** | **17/30 = 0.567** | **20/30 = 0.667** | **23/30 = 0.767** | |

### Edge Case Floor Check
All three variants score ≥ 1/5: all eligible.

## Position-Bias Mitigation

Pass 1 (order 1, 2, 3) and Pass 2 (order 3, 2, 1) agreed on every dimension except V2 Correctness (Pass 2 gave 4/5 for the incomplete "CI-safe" severity rationale); re-evaluation kept 5/5 because the card's claim is literally true and V2 conceded the omission only in debate. Disagreements: 1; verdicts changed: 0.

## Combined Scoring

| Variant | 0.5 × quant | 0.5 × qual | Combined |
|---|---|---|---|
| Variant 1 | 0.374 | 0.284 | 0.658 |
| Variant 2 | 0.383 | 0.334 | 0.717 |
| Variant 3 | 0.426 | 0.384 | 0.810 |

Margin V3 over V2: 0.093 (> 0.05): no tiebreaker. Debate points won: V3 7 (S-001, C-002, C-003, X-002, X-003 plus U-001, U-002 adopted), V1 2 (C-001, X-001 class/remedy), V2 3 (S-002, C-004, X-001 severity with V3).

## Selected Base: Variant 3 (opus:refactorer)

- Selection rationale: highest combined score; owns the unique test-design findings the source's regression-test requirement depends on.
- Strengths to preserve: R3-F1 (shared `old_summary_refs` helper), R3-F2 (non-empty scan), R3-F4 (`<scope>`), R3-F5, R3-F7, R3-F3 (low), R3-F6 (informational).
- Strengths to incorporate: V1 R1-F1 class (grounding_gap) and remedy (amend Constraints line 20, delete the gitignored mirror, verify-sync exit 0) replacing R3-F8; V1 R1-F3 (SKILL.md:66 correctly unchanged); V2 R2-F3 (design-doc grep for lines 168/249); V2 coverage line; V2 CI fact (`.github/workflows/test.yml:118-124`); invariant probe INV-001, INV-002, INV-007; A-001 handoff note.
