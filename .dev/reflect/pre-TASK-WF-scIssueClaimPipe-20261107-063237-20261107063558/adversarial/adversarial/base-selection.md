# Base Selection: reviewer-card variants

Variants: V1 = reviewer 1 (sonnet, analyzer), V2 = reviewer 2 (haiku, qa), V3 = reviewer 3 (opus, refactorer). Rubric adaptation for review cards: `rubric.md` in this folder.

## Quantitative Scoring (50% weight)

Computed by script (`/tmp/reflect-quant-scIssueClaimPipe.py`, output `quant-scores.json`); deterministic.

| Metric | Weight | V1 | V2 | V3 | How computed |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.6875 | 0.2500 | 0.6250 | consensus content points found: 11, 4, 10 of 16 (C-001..C-015 plus N-001) |
| Internal consistency (IC) | 0.25 | 0.7778 | 0.8000 | 0.8462 | 1 - findings later shown wrong or overstated / findings (2/9, 1/5, 2/13) |
| Specificity ratio (SR) | 0.15 | 1.0000 | 1.0000 | 1.0000 | concrete tokens / (concrete + vague words); no vague word in any card |
| Dependency completeness (DC) | 0.15 | 1.0000 | 1.0000 | 1.0000 | plan:N and source.md:N references inside the file length (40, 11, 24 refs) |
| Section coverage (SC) | 0.15 | 1.0000 | 0.8333 | 0.9167 | top-level keys 12, 10, 11 over max 12 |
| **quant_score** | | **0.8507** | **0.7000** | **0.8366** | |

Caveat: SR and DC saturate at 1.0 for all three, so they do not separate the cards. DC counts a reference as resolved when its line number is inside the file; it does not check that the line says what the card claims (the calibrators did that).

## Qualitative Scoring (50% weight): additive binary rubric, dual pass

Pass 1 order V1, V2, V3 (sonnet); pass 2 order V3, V2, V1 (opus). Per-dimension counts, final = after disagreement resolution below.

| Dimension (5 each) | V1 P1 | V1 P2 | V1 final | V2 P1 | V2 P2 | V2 final | V3 P1 | V3 P2 | V3 final |
|---|---|---|---|---|---|---|---|---|---|
| Completeness | 5 | 4 | 4 | 3 | 3 | 3 | 4 | 4 | 4 |
| Correctness | 5 | 5 | 5 | 3 | 4 | 3 | 4 | 5 | 4 |
| Structure | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Clarity | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 4 | 4 |
| Risk Coverage | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 4 |
| Invariant and Edge Case | 3 | 4 | 4 | 2 | 4 | 3 | 5 | 5 | 5 |
| **Total of 30** | 26 | 26 | **26** | 20 | 23 | **21** | 25 | 27 | **26** |

### Position-bias disagreement log (11 criterion-variant pairs)

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason (orchestrator re-evaluation, evidence from both passes) |
|---|---|---|---|---|---|
| Completeness.4 (what a corrected plan would pass) | V1 | MET | NOT MET | NOT MET | The cited text states fixes, not a completion condition; same standard pass 2 applied to V2 and V3 |
| Inv.1 (collection boundaries) | V1 | NOT MET | MET | MET | Finding 3 turns on the empty tracked-file set ("no file under the worktree .dev/issues/<N>/ is tracked") |
| Corr.1 (no factual errors) | V2 | NOT MET | MET | NOT MET | The card's own calibration records an overstated finding 3 that was not corrected in the card |
| Clarity.4 (terms defined) | V2 | NOT MET | MET | NOT MET | LA-7 and ARG-1 are defined inline, but INF-035 and "T1 F-4" are used undefined |
| Risk.3 (failure modes and recovery) | V2 | MET | NOT MET | MET | Finding 1 names the failure (retry after an uncertain launch) and the recovery (check Orca before retrying) |
| Inv.2 (state across components) | V2 | NOT MET | MET | MET | A hand-started agent sits outside the hook's state: a cross-component state fact |
| Inv.5 (interaction effects) | V2 | NOT MET | MET | NOT MET | The cited text lists gaps; it does not describe parts of the plan combining |
| Comp.4 | V3 | MET | NOT MET | NOT MET | Same ruling as V1 |
| Comp.5 (what is not checked) | V3 | NOT MET | MET | MET | A specific not-run statement exists with evidence (the -k note); weaker than V1 and V2's card-wide statements |
| Corr.1 | V3 | NOT MET | MET | NOT MET | Own calibration records an overstated finding 5 and a stretched Regression label, uncorrected in the card |
| Clarity.1 (unambiguous) | V3 | NOT MET | MET | MET | "may run before Task 4" states a possibility, not a hedge |

Position-bias metrics: disagreements found 11 of 90 criterion-variant pairs (12%). The re-evaluation kept the stricter verdict in 6 (Comp.4 for V1 and V3, Corr.1 for V2 and V3, Clarity.4 for V2, Inv.5 for V2) and the more lenient verdict in 5 (Inv.1 for V1, Risk.3 and Inv.2 for V2, Comp.5 and Clarity.1 for V3). Pass 2 (opus, reverse order) scored higher than pass 1 (sonnet, forward order) for V2 (+3) and V3 (+2) and equal for V1; the two passes use different models, so the gap cannot be attributed to order alone.

### Edge Case Floor Check

Invariant and Edge Case final scores: V1 4, V2 3, V3 5; all at or above 1 of 5: all eligible.

## Combined Scoring

| Variant | quant x 0.50 | qual (final/30) x 0.50 | Combined |
|---|---|---|---|
| V1 | 0.4254 | 0.8667 -> 0.4333 | **0.8587** |
| V3 | 0.4183 | 0.8667 -> 0.4333 | **0.8516** |
| V2 | 0.3500 | 0.7000 -> 0.3500 | **0.7000** |

Margin V1 over V3: 0.0071 (0.8%), under the 5% tiebreak band.

### Tiebreaker

- Level 1, debate performance (points won in the scoring matrix, sole winner): V1 wins C-002, C-003, C-004, C-005, C-012, C-014, C-015 = 7; V3 wins C-007, C-009, C-011, C-013 = 4; shared or merge: S-001, S-002, C-001, C-006, C-008, X-001..X-004. V1 leads on Level 1.
- Tiebreaker applied: Yes, level 1. Margin 0.8%.

## Selected Base: Variant 1 (sonnet, analyzer)

**Selection rationale.** V1 has the highest combined score and the most sole-won debate points. It is the only card that found the write-verb audit in tests/skills/test_worker_contract.py (the most consequential defect, confirmed by two advocates and by the orchestrator's re-Read), the single-warning problem and the ST-4 collision as full findings. Its citations were corrected in place after calibration (plan:130, source.md:357).

**Strengths to preserve from V1.** All nine findings with evidence lists; the write-verb audit finding; the warning-precedence finding; the ST-4 finding; the orchestrator verification note on finding 2; the advisory correctness channel.

**Strengths to incorporate from non-base variants.**
- From V3: the missing dependency edge Task 7 and 9 on Task 3 (C-009); the `--repo` trap in tests/commands/test_issue_command.py:99-103 (U-004); the fork-safety gap for the launch prompt (C-013); the SKILL.md claim steps 6 and 7 as a separate MEDIUM (C-007); the reviewability notes (C-011).
- From V2: the MEDIUM grade for the dropped Task 6 safeguards (C-008); the Orca-is-a-dependency constraint (C-010); the restraint of not using Regression for a transient plan state.
- From the invariant probe: INV-002, INV-003, INV-004, INV-006, INV-008, INV-009 (MEDIUM, new), INV-005, INV-010, INV-013 (LOW).
- From Round 2: reclassify V1's two Regression findings as Drift (HIGH for the write-verb audit, MEDIUM for the inventory test); the new create-timeout item N-001.
- Missing from all cards (Completeness.4, Risk.2): a fix and a fix location for every finding. The merge adds both (plan only, or design first).
