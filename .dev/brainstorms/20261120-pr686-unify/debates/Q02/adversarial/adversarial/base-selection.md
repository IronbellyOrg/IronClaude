# Base Selection (Q02)

## Quantitative Scoring (50% weight)
Computed by the orchestrator. Method notes: "requirements" are the five safe limits and the decision named in the topic question (no formal requirement IDs exist); the concrete and vague counts come from a grep of each file (`concrete` = numbers, backtick spans and quoted spans; `vague` = "appropriate", "as needed", "might", "various", "etc." and similar). The consistency and claim counts are hand estimates.

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.000 | 0.667 | V1 covers 6 of 6 (decision, merged-only, never `-D`, default branch, open PR, dry run). V2 covers 4 of 6: grep finds 0 mentions of a default-branch guard and 0 of an open-PR guard |
| Internal consistency (IC) | 0.25 | 1.000 | 0.929 | V1: 0 contradictions in about 13 claims. V2: 1 in about 14 (fact 8 says `-d` refuses an unmerged branch; its own Risk says `-d` can delete a pushed, unmerged branch) |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 | V1 85 concrete, 0 vague. V2 87 concrete, 0 vague |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | No dangling internal reference in either |
| Section coverage (SC) | 0.15 | 1.000 | 1.000 | 6 H2 sections each |
| **quant_score** | | **1.000** | **0.882** | 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC |

Caution: most of the quantitative gap is RC, and RC is measured against the topic question's own list of limits, which favours the paper that states them. Without RC the two are nearly equal.

## Qualitative Scoring (50% weight): Additive Binary Rubric
Two independent read-only graders scored all 30 criteria (pass 1 order V1 then V2; pass 2 order V2 then V1). Neither saw the debate files.

### Per-dimension results after resolving disagreements
| Dimension | V1 pass 1 | V1 pass 2 | V1 final | V2 pass 1 | V2 pass 2 | V2 final |
|---|---|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 4 | 4 | 4 | 4 |
| Correctness (5) | 5 | 5 | 5 | 5 | 5 | 5 |
| Structure (5) | 5 | 5 | 5 | 5 | 5 | 5 |
| Clarity (5) | 4 | 4 | 4 | 3 | 4 | 4 |
| Risk Coverage (5) | 4 | 2 | 2 | 3 | 3 | 3 |
| Invariant & Edge Case (5) | 4 | 4 | 4 | 3 | 3 | 3 |
| **Total (30)** | 26 | 24 | **24** | 23 | 24 | **24** |

Criteria both graders marked NOT MET for both variants: C4 for V1 only, L4 (terms such as D13, ADD5, PR undefined), R1 (no probabilities), E4 (equal versus ancestor not discussed). V2 also NOT MET on C1 (no default-branch or open-PR guard), R4 and E1.

## Position-Bias Mitigation
Disagreements found: 3 of 60 criterion-variant pairs. Each was re-evaluated with both passes' evidence side by side (the final verdict is the re-evaluation):

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| R2 mitigation for each risk | V1 | MET (guards plus reflog or remote copy) | NOT MET (over-strict risk has no mitigation) | NOT MET | The Risk section names an over-strict risk with no mitigation, only the label "cosmetic" |
| R4 external dependencies and their failure | V1 | MET ("fail-closed everywhere") | NOT MET (`gh` lookup failure not discussed) | NOT MET | "Fail-closed" is a generic phrase; no dependency failure is named |
| L5 actionable next step or decision point | V2 | NOT MET ("Nothing extra") | MET (decision: follow issue 687 as written) | MET | The Claim states the decision and the exact step |

Verdicts changed by re-evaluation: 3 (each overturned one pass).

## Edge Case Floor Check
V1 4/5 and V2 3/5 on Invariant & Edge Case Coverage. Both meet the 1/5 floor; both are eligible as base.

## Combined Scoring
| Variant | quant (50%) | qual (50%) | variant_score |
|---|---|---|---|
| Variant 1 (OURS) | 1.000 | 24/30 = 0.800 | **0.900** |
| Variant 2 (CLAY) | 0.882 | 24/30 = 0.800 | **0.841** |

Margin: 5.9 points (above the 5% tiebreaker trigger). Tiebreaker applied: No. For the record, debate performance also favours V1 on points won (C-002, C-006, X-001, and the gap in X-002) against V2 (C-005, and C-004 after resolution).

## Selected Base: Variant 1 (OURS)
Selection rationale: it scores higher on the topic question's own list of limits and on edge-case coverage, and the owner's weighting rule says OURS wins unless CLAY shows a clear, evidenced benefit (the tie on the qualitative layer goes to OURS). Variant 2 shows clear, separable benefits, so the result is a hybrid, not a pure OURS win.

C-004 resolution (the one unresolved point): use rule 3 of issue 687 as written (HEAD equals the merged PR's last head commit, or is an ancestor of it). A local ref at an ancestor of the PR head holds no commit that the PR head lacks, so the stricter exact-equality check protects nothing more, and Variant 1 itself withdrew the extra check.

Strengths to preserve from the base:
- Explicit refusal list for the default branch and long-lived branches, because `-d` has no such protection (measured; `integration` is real, with three merged PRs using it as head).
- "Any OPEN PR with this head keeps the branch" as one added line in rule 2.
- A per-row "branch: would delete / would keep (reason)" column in the dry run.
- The finding that `-d` means "pushed or merged", not "its PR landed", so the nine rules are the real gate.
- The script must not delete more than Orca would.

Strengths to incorporate from Variant 2:
- Keep issue 687's rule set and step order in place; the branch rules are an addendum to rules 1 to 3, not a parallel list (S-002).
- The acceptance test that records every command and fails on `--force`, `-D`, `rm`, `prune`, a push to anything but the evidence remote or a remote branch delete (U-003).
- Drop the redundant "no other worktree has it checked out" guard (git refuses it) and the speculative "open PR uses it as base" guard.
- Report-only first week before `--apply` in the daily automation (C-007).
- A-001: log the merged PR head SHA so a branch can be recreated from `refs/pull/N/head` when the remote branch is gone. A-003: require the PR's `headRepositoryOwner` to be ours and its head SHA to match.
