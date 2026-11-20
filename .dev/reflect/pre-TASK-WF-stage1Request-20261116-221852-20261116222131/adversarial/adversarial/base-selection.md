# Base Selection

## Quantitative Scoring (50% weight)

Computed by `quant.py` in this folder (deterministic; output `quant-scores.json`). Limits: RC is a keyword match of each card against the 12 content points of the diff analysis (a keyword hit can be a false positive: V2's C-001 hit comes from "entry checks" at source line 51, not the ledger package id); IC is 1.0 for all three because the contradiction scan found no contradiction inside a single card (X-001 and X-002 are between cards); SR and DC are 1.0 for all three.

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.5000 | 0.3333 | 0.5000 |
| Internal consistency (IC) | 0.25 | 1.0 | 1.0 | 1.0 |
| Specificity ratio (SR) | 0.15 | 1.0 | 1.0 | 1.0 |
| Dependency completeness (DC) | 0.15 | 1.0 | 1.0 | 1.0 |
| Section coverage (SC) | 0.15 | 1.0 | 0.3846 | 0.8462 |
| **quant_score** | | **0.8500** | **0.7077** | **0.8269** |

## Qualitative Scoring (50% weight): additive binary rubric

Rubric: `rubric.md`. Two independent evaluator passes (qual-pass-1 order V1, V2, V3; qual-pass-2 order V3, V2, V1), each criterion Claim-Evidence-Verdict.

Position-bias log (criterion-variant pairs where the passes disagreed, and the final verdict after re-evaluation against the cards):

| Criterion | Variant | Pass 1 | Pass 2 | Final | Re-evaluation evidence |
|---|---|---|---|---|---|
| C11 logical ordering | V1 | MET | NOT MET | NOT MET | V1's findings interleave gaps, confirmations and authorized items (F1 gap, F3 authorized, F4 drift, F6 same as F2, F10 verified); no blocking-first or grouped order |
| C29 count divergence | V1 | NOT MET | MET | NOT MET | V1 raises no count that fails to add up; F7 reads the parsed 0.0 as an artifact but not a count mismatch between lists |
| C30 interaction effects | V1 | NOT MET | MET | MET | V1 F2: Revision 4's cut of the owner summary interacts with the ledger text that still expects it (stage 3 gate has nothing to read) |
| C19 terms defined | V2 | MET | NOT MET | NOT MET | V2 uses "GR12 raise-only rule" and "coverage matrix" without defining them; pass 1's evidence ("terms clear on first use") cites no text |

Disagreements found: 4 of 90 criterion-variant pairs. Re-evaluation (done by the orchestrator against the cards, not by a third agent) resolved all 4 in favour of one of the two passes: C11, C29 and C19 end NOT MET, C30 ends MET. No final verdict differs from both passes.

### Final dimension subtotals (of 5 each)

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5 | 3 | 5 |
| Correctness | 5 | 5 | 5 |
| Structure | 2 | 5 | 4 |
| Clarity | 4 | 4 | 4 |
| Risk Coverage | 5 | 2 | 5 |
| Invariant & Edge Case Coverage | 3 | 1 | 4 |
| **qual_score (met/30)** | **24/30 = 0.8000** | **20/30 = 0.6667** | **27/30 = 0.9000** |

### Edge Case Floor Check
Floor: fewer than 1 of 5 makes a variant ineligible as base. V1 3, V2 1, V3 4: all three eligible.

## Combined Scoring

variant_score = 0.50 x quant + 0.50 x qual.

| Variant | Quant weighted | Qual weighted | Final |
|---|---|---|---|
| V1 | 0.4250 | 0.4000 | 0.8250 |
| V2 | 0.3539 | 0.3333 | 0.6872 |
| V3 | 0.4135 | 0.4500 | 0.8635 |

Margin V3 over V1: 0.0385 (3.85 points of 100), under the 5 percent tiebreaker band.

Tiebreaker level 1 (debate performance, points won in the Step 2 scoring matrix): V3 7 (S-001, C-006, C-007, C-008, C-009, C-010, A-003), V1 5 (C-001, C-004, C-011, X-001, A-004), V2 4 (S-002, C-005, X-002, A-002). V3 leads; no further level needed. Tiebreaker applied: yes (level 1).

## Selected Base: Variant 3 (opus:refactorer)

Selection rationale: highest combined score (0.8635) and the tiebreaker, with the strongest verified, executable findings (second twin pin, lint baseline, wording of partial and blocking, notes-file line kinds, grep scope).

Strengths to preserve: the quoted evidence per finding; the pin-by-pin check of the scans (F8); the twin-test finding (F2); the `make lint` baseline (F3).

Strengths to incorporate from other variants:
- V2 F1 (C-005, X-002): the Constraints bullet "code-assigned severity in `src/superclaude/cli/**/*.py`" contradicts Task 1's outcome function (plan:23 against plan:38). Blocking. The base verdict "ship" is replaced by "revise".
- V1 F1 (C-001, A-004): the ledger go names another package id; V1 F5 (C-004): the 35 percent target is missing from the Also-not-built bullet; V1 F9 (C-011): print-smoke.txt should hold the literal command output.
- V3's own C-003 (stored-tag grep) stays, with the unresolved note.

Weaknesses of the base: the "ship" verdict and its F8 claim missed C-005; it did not check the ledger (C-001); it undefines R1 to R4 (rubric C19).
