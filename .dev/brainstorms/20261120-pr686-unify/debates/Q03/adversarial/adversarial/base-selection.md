# Base Selection Report (Q03)

Variant 1 = OURS (read-only variant now). Variant 2 = CLAY (keep dormant behind the grant). Qualitative scoring was done by two independent evaluator agents (pass 1 order V1 then V2; pass 2 order V2 then V1). The orchestrator re-evaluated every disagreement and its verdict is final.

## Quantitative Scoring (50% weight)

The source "requirements" are R1 to R6 (recommend one of three options; cite D09; cite PR 686 code with file and line; address NG-2; state costs and risks; compare the other two options). Specificity counts were estimated by hand, not by a script (UNVERIFIED precision; they move the score by under 0.01).

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 0.833 (R1 to R5 met; R6 not: strip is not compared apart from the read-only variant) | 0.833 (R1 to R5 met; R6 not: the read-only variant is never compared) |
| internal_consistency | 0.25 | 0.950 (1 intra contradiction in about 20 claims: dry-run listed as kept, X-003) | 1.000 (no intra contradiction; the M1 conflict is with the repo, not inside the paper) |
| specificity_ratio | 0.15 | 0.940 (about 45 concrete, about 3 vague) | 0.920 (about 36 concrete, about 3 vague) |
| dependency_completeness | 0.15 | 1.000 | 1.000 |
| section_coverage | 0.15 | 1.000 (6 H2 sections) | 1.000 (6 H2 sections) |
| **quant_score** | | **0.9285** | **0.9380** |

## Qualitative Scoring (50% weight) - Additive Binary Rubric (30 criteria)

Final verdicts after re-evaluation. E = short evidence.

### Completeness
| Criterion | V1 | E (V1) | V2 | E (V2) |
|---|---|---|---|---|
| C1 all requirements R1 to R6 | NOT MET | strip not compared apart from the read-only variant | NOT MET | read-only variant never compared |
| C2 edge cases, failures | MET | Fact 5: `hold_write_failed` every cycle; row 3 stuck | MET | Costs: warning every cycle; Claim: stuck leftover label |
| C3 dependencies | MET | "own small PR, together with the NG-2 amendment" | MET | "one grant line plus the NG-2 amendment" |
| C4 success criteria | NOT MET | end state "writes nothing", no named test | MET | fact 1 no-write test; fact 3 dry-run gate |
| C5 out of scope | MET | label write "NOT" shipped, deferred | NOT MET | no out-of-scope list |
| **Subtotal** | **3/5** | | **3/5** | |

### Correctness
| Criterion | V1 | E (V1) | V2 | E (V2) |
|---|---|---|---|---|
| C1 no factual errors | NOT MET | says `HOLD_LABEL` is in `record.py`; the constant is not (only the text `hold:plan` in a docstring, `record.py:11`) | NOT MET | "Today no repo names it" conflicts with M1 (`orchestrator.md:291`, `conftest.py:286`) |
| C2 feasible | MET | skip, clear, keep-entry needs no write (M3) | MET | gate already exists (`_hold_write_ok`) |
| C3 terminology | MET | "read-only variant", `plan_check`, `held_incomplete` consistent | MET | "dormant", "grant", "rows" consistent |
| C4 no internal contradiction | MET | "No label read" is loose wording for no `hold:plan` read, not a contradiction (scored under Clarity) | MET | claim, costs, risks agree |
| C5 claims supported | MET | file:line cites; counts labelled rough | NOT MET | "one-line change makes the no-grant state silent" and "no repo names it" unsupported |
| **Subtotal** | **4/5** | | **3/5** | |

### Structure
| Criterion | V1 | V2 |
|---|---|---|
| C1 to C5 (order, depth, separation, navigation, artifact conventions) | MET x5 (same skeleton, paths preamble, file:line cross references) | MET x5 |
| **Subtotal** | **5/5** | **5/5** |

### Clarity
| Criterion | V1 | E (V1) | V2 | E (V2) |
|---|---|---|---|---|
| C1 unambiguous | NOT MET | "backlog label present: skip" next to "No label read" | MET | "it runs only when the repo list names the grant" |
| C2 concrete | MET | names `LabelWriter`, `github.py:983-1069`, `cycle.py:1064-1119` | MET | file:line and a named test |
| C3 section purpose | MET | short headed sections | MET | short headed sections |
| C4 terms defined | MET | NG-2 glossed in the Claim | NOT MET | NG-2, Ruling 33, R11 undefined |
| C5 actionable | MET | "rework must create the entry without the write" | MET | "Fix the two rough edges" |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage
| Criterion | V1 | V2 |
|---|---|---|
| C1 at least 3 risks with probability and impact | NOT MET (two risks, no probability) | NOT MET |
| C2 mitigation for each | MET (entry created without the write; a second PR) | NOT MET (second risk has none) |
| C3 failure modes and recovery | MET (quiet hour never starts; second PR) | NOT MET (a fix, no recovery path) |
| C4 external dependencies | NOT MET | NOT MET |
| C5 monitoring or validation | NOT MET (dry-run listed as kept, not tied to a risk) | MET (NG-2 test fails any extra write; dry-run shadow gate) |
| **Subtotal** | **2/5** | **1/5** |

### Invariant and Edge Case Coverage
| Criterion | V1 | V2 |
|---|---|---|
| C1 collection boundaries | NOT MET | NOT MET |
| C2 state interactions | MET (clock keyed on entries created with the write) | MET (entries created at row 4, read at `:1139-1149`) |
| C3 guard gaps | MET (one config line turns writes on; row 3 stuck) | MET (grant in config without code review) |
| C4 count divergence | NOT MET ("rows 3 to 5" here, "rows 3 to 6" elsewhere; counts not reconciled) | NOT MET |
| C5 interaction effects | MET (hold rows with the plan request) | MET (rows with the plan request; misses that no grant means no entry, M2) |
| **Subtotal** | **3/5** | **3/5** |

### Qualitative Summary

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 3/5 | 3/5 |
| Correctness | 4/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 2/5 | 1/5 |
| Invariant and Edge Case | 3/5 | 3/5 |
| **qual_score** | **21/30 = 0.700** | **19/30 = 0.633** |

### Edge Case Floor Check
Both variants score 3/5 on Invariant and Edge Case Coverage (floor 1/5). Both are eligible as base.

## Position-Bias Mitigation

Pass 1 totals: V1 21, V2 20. Pass 2 totals: V1 25, V2 18. Pass 2 (V2 evaluated first) was more favourable to V1 than pass 1, so the order did not favour whichever paper came first.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (re-evaluation) |
|---|---|---|---|---|---|
| D1.C1 | V1 | NOT MET | MET | DISAGREE | NOT MET (strip not compared apart from read-only) |
| D1.C4 | V1 | NOT MET | MET | DISAGREE | NOT MET (no checkable completion test named) |
| D2.C1 | V1 | NOT MET | MET | DISAGREE | NOT MET (the `record.py` attribution is wrong; form-level, but the criterion is binary) |
| D2.C4 | V1 | NOT MET | MET | DISAGREE | MET (loose wording, not a contradiction; charged under D4.C1) |
| D4.C1 | V1 | NOT MET | MET | DISAGREE | NOT MET ("No label read" beside the kept backlog label read) |
| D5.C5 | V1 | MET | NOT MET | DISAGREE | NOT MET (dry-run is not tied to a risk) |
| D2.C5 | V2 | MET | NOT MET | DISAGREE | NOT MET (two key claims unsupported) |
| D4.C1 | V2 | NOT MET | MET | DISAGREE | MET (the paper defines the six-row table and the grant in its Mechanism) |
| D5.C3 | V2 | MET | NOT MET | DISAGREE | NOT MET (a fix is named, no recovery path) |
| D6.C5 | V2 | MET | NOT MET | DISAGREE | MET (it does consider the rows with the plan request; the missed M2 case is charged under correctness) |

Disagreements re-evaluated: 10. Final verdicts that differ from the pass that was not followed: 10 (each side was followed 5 times).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (OURS) | 0.464 | 0.350 | **0.814** | 8 points won |
| V2 (CLAY) | 0.469 | 0.317 | **0.786** | 2 points won |

**Margin**: 2.8 percentage points (below the 5% threshold).
**Tiebreaker applied**: Yes, level 1 (debate performance): V1 won 8 scored points (C-001, C-003, C-004, C-006, C-008, C-010, X-001, X-002), V2 won 2 (C-009, C-011).

## Selected Base: Variant 1 (OURS, read-only variant now)

### Selection Rationale
Variant 1 leads on the combined score by 2.8 points, which is inside the tiebreak band, and wins the tiebreaker 8 to 2 on debate points. It also leads on correctness (4/5 against 3/5) and risk coverage (2/5 against 1/5). Variant 2 leads only the quantitative layer, by 0.010, because it has no internal contradiction. The result is the same under the owner's weighting rule: Variant 2 shows no clear, evidenced benefit that outweighs NG-2, and its own advocate conceded M1 and M2.

### Strengths to Preserve from Base
1. The check, the skip and the person-set backlog stop need no write (M3, M4).
2. Moderator fact M2: with no grant the dormant form leaves poll-found issues with no entry, so no quiet hour.
3. The standing grant list as the weak switch (M1; U-002).
4. The NG-2 test as a zero-write test.

### Strengths to Incorporate from Non-Base Variants
1. From V2, U-005: write down the narrow label-write form (add and remove only, no comment call, injected guard, grant gated) as the deferred design.
2. From V2, U-006 and C-007: keep a `would_hold` dry-run listing, and make a 24-hour dry-run shadow run plus a label-write-under-cron test the gate for any later switch-on.
3. From V2, C-009 and U-008: state the cost of restoring the code and of reworking `test_hold.py`, and name the hybrid fallback (delete only the write calls, keep the table and entry creation).
4. From V2, C-011: record the loss of a hand-placed `hold:plan` as a stated cost.
5. From V2, A-002: require the rework to be sized before it is asked of Clay.

### Defects of the base to fix in the merge
The `record.py` attribution; "No label read" wording; the dry-run overstatement (X-003); "rows 3 to 5" against "rows 3 to 6"; no named completion test; M1 and M2 not in the paper.
