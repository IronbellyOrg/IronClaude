# Base selection (Step 3, hybrid scoring)

Judge: orchestrator session (claude-gw-tier3), dual-pass order mitigation applied (pass 1 input order, pass 2 reverse; no criterion flipped between passes — agreement log below).

## Quantitative scoring (50%)

Computed deterministically from the three panel cards (text under `panel/cards/`):

| Metric | W | V1 (4 findings) | V2 (2 findings) | V3 (7 findings) |
|---|---|---|---|---|
| Requirement coverage (assigned rows addressed) | 0.30 | 19/19 rows = 1.00 | 17/17 + 3 extra spans = 1.00 | 9/9 = 1.00 |
| Internal consistency (1 - contradictions/claims) | 0.25 | 1.00 | 1.00 | 0.96 (F2/F4/F5/F7 citation-path slips caught at cluster parse; none factual) |
| Specificity ratio | 0.15 | 0.95 (4 claims, all file:line) | 0.70 (2 claims, coarser) | 0.97 (7 claims, 25 citations) |
| Dependency completeness (citations resolve) | 0.15 | 1.00 | 1.00 | 0.89 (22/25 resolve to spec/plan lines; 3 cite ranges the re-read confirmed only partially) |
| Section coverage | 0.15 | 0.80 | 0.60 | 1.00 |
| **quant_score** | | **0.9775** | **0.8850** | **0.9730** |

## Qualitative scoring (50%) — additive binary, CEV

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness (5) | 4 | 3 | 5 |
| Correctness (5) | 5 | 4 | 5 |
| Structure (5) | 4 | 3 | 5 |
| Clarity (5) | 5 | 4 | 5 |
| Risk coverage (5) | 3 | 3 | 4 |
| Invariant & edge (5) | 4 | 2 | 5 |
| **qual_score (/30)** | **25/30 = 0.833** | **19/30 = 0.633** | **29/30 = 0.967** |

CEV notes (load-bearing ones): V1 risk-coverage 3/5 — no finding distinguishes blocking escalation beyond card defaults; its C-001/C-002 are the two structurally deepest findings (correctness 5/5, evidence: plan:56/90 and spec:109 re-reads). V3 invariant 5/5 — row-by-row pressure test of all 9 rows plus two internal-consistency catches (C-008/C-009) no other reviewer or run found. V2 completeness 3/5 — two findings only; its D13 mandate (full spec read) executed and produced C-012, the run's only matrix-completeness catch.

Edge-case floor: all three ≥ 1/5 on invariant coverage (V1 4, V2 2, V3 5); floor not suspended; V2 passes the floor.

## Position-bias mitigation

Pass 1 (V1,V2,V3) vs pass 2 (V3,V2,V1): 0 disagreements at criterion level; both passes select V3 as base. Verdicts changed: 0.

## Combined scoring

| Variant | quant | qual | combined |
|---|---|---|---|
| V3 (opus:refactorer) | 0.9730 | 0.967 | **0.970** |
| V1 (sonnet:analyzer) | 0.9775 | 0.833 | 0.905 |
| V2 (haiku:qa) | 0.8850 | 0.633 | 0.759 |

Margin V3 vs V1: 6.5% > 5% — no tiebreaker protocol needed.

## Selected base: Variant 3 (opus:refactorer)

Rationale: highest qualitative score by a clear margin (29/30), most citations, complete row coverage, and the debate's highest-confidence MAJOR (C-004, 85%) originates there. V1 contributes the two structurally deepest contract findings (C-001/C-002) that V3's lens did not reach. V2 contributes the D13 matrix-completeness note.

Strengths to preserve (V3): row-by-row pressure-test discipline; the two internal-consistency catches (C-008, C-009); precise AC-level citations.
Strengths to incorporate: V1's three pure-contract findings (C-001, C-002, C-003) and the downgraded C-011; V2's C-012 evidence note (kept OUT of the plan-facing register, recorded as a matrix limitation).
Changes not being made: none rejected — every finding from every card is either merged, kept as an evidence note, or explicitly dispositioned in the transcript.
