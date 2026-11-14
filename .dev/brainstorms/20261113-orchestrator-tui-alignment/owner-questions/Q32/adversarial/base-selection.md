# Base Selection Report (Q32)

Scoring was done by the orchestrating session (this group worker acting as the skill's debate orchestrator). Source "requirements" for coverage are the eight points `Q32/question.md` asks an answer to handle: (R1) yes or no; (R2) the sentence if yes; (R3) WC-9's three conditions; (R4) one grant per Task (`WORKER-CONTRACT.md:244`); (R5) who commits otherwise (spec 6.4 rule 14); (R6) review before push; (R7) the uncommitted gap; (R8) hooks and no `--no-verify`.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (proposal-A) | Variant 2 (proposal-B) | Variant 3 (proposal-C) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.88 (misses R8) | 1.00 (R2 not applicable to a "no") | 1.00 |
| internal_consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.85 | 0.90 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.94** | **0.98** | **0.99** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

### Completeness

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Covers explicit requirements | MET (owner's words per Task) | MET | MET (gives the sentence) |
| Edge cases and failures | MET ("If no or no reply") | MET (worktree cleaned, stray checkout) | MET (commit refused by a strict guard) |
| Dependencies | MET (WC-9 conditions, child worktree) | MET (rule 14, `:245` steps) | MET |
| Success criteria | MET (grant row ends at `worker_done`) | MET (ledger row; no commit rows) | MET |
| Out of scope stated | NOT MET | MET ("covers this program only") | NOT MET |
| **Subtotal** | **4/5** | **5/5** | **4/5** |

### Correctness

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| No factual errors | MET | MET (one line-number slip, `:42` for text at `:44`: minor, claim true) | MET |
| Feasible with stated constraints | MET | MET | NOT MET (rests on two UNVERIFIED contract readings; cannot cite evidence it works) |
| Terminology consistent | MET | MET | MET |
| No internal contradictions | MET | MET | MET |
| Claims supported | MET | MET | MET |
| **Subtotal** | **5/5** | **5/5** | **4/5** |

### Structure
All three: same five sections, consistent depth, cross-references to contract and spec lines. 5/5 each.

### Clarity

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Unambiguous | NOT MET ("worth a commit" has no criterion) | MET | MET |
| Concrete | MET | MET | MET |
| Clear section purpose | MET | MET | MET |
| Terms defined | MET | MET (PR session glossed) | MET |
| Actionable next steps | MET | MET | MET |
| **Subtotal** | **4/5** | **5/5** | **5/5** |

### Risk Coverage

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | NOT MET | NOT MET |
| Mitigation for each risk | NOT MET | NOT MET (gap unmitigated) | NOT MET |
| Failure modes and recovery | MET (fallback to rule 14) | NOT MET | MET (refused commit reported) |
| External dependency failures | MET (child worktree UNVERIFIED) | MET (hook failures on PR session) | MET |
| Monitoring or detection | NOT MET | NOT MET | MET (commit id in `worker_done`) |
| **Subtotal** | **2/5** | **1/5** | **3/5** |

### Invariant and Edge Case Coverage

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Collection boundaries | MET (zero approved Tasks falls back) | NOT MET | NOT MET |
| State across components | MET | MET (gap between worker and PR session) | MET |
| Guard condition gaps | MET (strict WC-9) | NOT MET (no guard on the gap) | MET (only after `succeeded`) |
| Count divergence | MET (up to nine questions) | NOT MET | MET (nine Tasks, one answer) |
| Interaction effects | MET (two commit paths) | MET (load on the PR route, INV-001) | MET (PR fix commits on top) |
| **Subtotal** | **5/5** | **2/5** | **4/5** |

Edge-case floor (at least 1/5): all eligible.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 5/5 | 4/5 |
| Correctness | 5/5 | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 5/5 | 5/5 |
| Risk Coverage | 2/5 | 1/5 | 3/5 |
| Invariant and Edge Case | 5/5 | 2/5 | 4/5 |
| **qual_score** | **25/30 = 0.83** | **23/30 = 0.77** | **25/30 = 0.83** |

## Position-Bias Mitigation

Pass 1 (order 1, 2, 3) and pass 2 (order 3, 2, 1) were both run by the same orchestrating context, so they are not independent.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Correctness: feasible | 3 | MET | NOT MET | DISAGREE | NOT MET (no evidence the filled-in sentence passes WC-9) |
| Correctness: no factual errors | 2 | NOT MET | MET | DISAGREE | MET (line slip is a citation-format matter on a true claim) |

Disagreements re-evaluated: 2. Final verdicts changed: 2.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won (sole) |
|---|---|---|---|---|
| 1 (proposal-A) | 0.470 | 0.417 | **0.89** | 1 (C-003) |
| 2 (proposal-B) | 0.490 | 0.383 | **0.87** | 6 (C-001, C-002, C-005, C-007, X-001, X-002) |
| 3 (proposal-C) | 0.495 | 0.417 | **0.91** | 4 (S-002, C-004, C-006, A-002) |

**Margin**: all three lie within 3.9 points of the top (0.91, 0.89, 0.87), inside the 5 percent tiebreak band.
**Tiebreaker applied**: Yes, level 1 (debate points won). Interpretation recorded: the protocol text says "top two variants within 5%"; here all three are within 5% of the top, so the tiebreak was applied across all three. Under the strict top-two reading (Variants 3 and 1), Variant 3 would be selected (4 points against 1). The rubric scores document quality (Variant 2's short, honest text earns fewer risk and edge-case points), while the debate scores the answer; all three advocates, including those for Variants 1 and 3, chose Variant 2.

## Selected Base: Variant 2 (proposal-B)

### Selection Rationale
Wins the tiebreak with 6 sole debate points, including all three high-severity content points it contests (C-001, C-002) and both contradictions; unanimous overall vote of the advocates (65, 70, 60 percent).

### Strengths to Preserve from Base
1. One commit path and one review point; no owner wording to collect.
2. Uses only rules already written (`WORKER-CONTRACT.md:44`, `:245`; spec 6.4 rule 14).
3. Equals the default, so silence changes nothing.

### Strengths to Incorporate from Non-Base Variants
1. From the Variant 2 advocate's concession and A-002: a guard that the coordinator does not remove or clean a worker's worktree until its PR session has committed (not currently a general rule in the spec).
2. From Variant 1 (C-003): the door stays open; if the owner later wants a checkpoint for one specific Task, that Task can get its own owner sentence and grant, which meets WC-9 strictly.
3. From Variant 3 (S-002): if the owner prefers "yes", the stronger sentence form names all nine work items so each brief quotes it unchanged (fit with "for that Task" still UNVERIFIED).
4. Correct the citation `:42` to `:44` for "Outside that grant a worker never runs `git add` ...".
