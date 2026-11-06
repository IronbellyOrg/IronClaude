# Base Selection

Scoring was done by the orchestrator in one session, not by a script. The quantitative figures are manual counts and are marked as estimates; the protocol asks for deterministic scores, so treat differences under about 0.03 as noise. That is why the tiebreaker below decides the result.

## Quantitative Scoring (50% weight)

Source requirements for RC: the 4 success criteria and 4 open questions of `seed-brief.md` (it has no formal requirement IDs, so section-level topic matching applies).

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | Both cover 8 of 8 topics: V1 via FR-003, naming table, FR-004, FR-002, decisions table; V2 via FR-003, pattern, FR-010, FR-001/FR-007, FR-008, FR-009 and risk 1 |
| Internal consistency (IC) | 0.25 | 0.97 | 0.94 | V1: 1 conflict (FR-004 absolute wording against the WC-3 case) in about 30 claims. V2: 2 conflicts (FR-005 and risk 2 against FR-012; FR-011 against the contract's two-token tdd example) in about 32 claims |
| Specificity ratio (SR) | 0.15 | 0.92 | 0.90 | Both are mostly concrete (names, numbers, paths); each has a few "may" or "UNVERIFIED" statements |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | Every internal reference (FR-n, R-n, risk n) resolves in both |
| Section coverage (SC) | 0.15 | 0.75 | 1.00 | V1 has 6 H2 sections, V2 has 8 |
| **quant_score** | | **0.943** | **0.970** | RC x0.30 + IC x0.25 + SR x0.15 + DC x0.15 + SC x0.15 |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Each verdict cites evidence; no evidence means NOT MET.

### Completeness (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|---|---|---|---|
| 1 | Covers all explicit requirements | MET | MET | See RC above |
| 2 | Edge cases and failure scenarios | MET | MET | V1 R1, R2, FR-006; V2 FR-012, FR-013, risks 1 to 6 |
| 3 | Dependencies and prerequisites | MET | MET | Both end each requirement with "Depends on" |
| 4 | Success or completion criteria | NOT MET | NOT MET | Neither gives acceptance checks for the naming rule; searched both for "acceptance", "verify", "done" |
| 5 | What is out of scope | MET | MET | V1 R3 ("protects only `return-contract.yaml`"); V2 risk 6 |

Subtotal: V1 4, V2 4.

### Correctness (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|---|---|---|---|
| 1 | No factual errors | MET | NOT MET | V2 FR-011 says the path appears once on the `Command:` line; WORKER-CONTRACT.md line 159 shows it twice (`--output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`). V1 FR-004 is over-broad but true for retries |
| 2 | Approaches feasible with stated constraints | MET | MET | Both fit WC-4, WC-6, WC-11 |
| 3 | Terminology consistent | MET | MET | Attempt, subject, command used the same way throughout |
| 4 | No internal contradictions | MET | NOT MET | V2 FR-005 and risk 2 (recover the counter by listing directories) against FR-012 (a guard refusal consumes an attempt but leaves no directory); both advocates agreed (A-003) |
| 5 | Claims supported within the document | MET | MET | Both cite contract rules for each requirement |

Subtotal: V1 5, V2 3.

### Structure (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|---|---|---|---|
| 1 | Logical section order | MET | MET | Pattern before requirements before examples |
| 2 | Consistent hierarchy depth | MET | MET | H2 sections only, tables inside |
| 3 | Separation of concerns | MET | MET | V2 splits Retries, Nested, Child worktrees; V1 keeps them as requirements |
| 4 | Navigation aids | MET | MET | Numbered requirements and "Depends on" cross-references |
| 5 | Follows the artifact type's conventions | MET | MET | Numbered FR list with examples and risks |

Subtotal: V1 5, V2 5.

### Clarity (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|---|---|---|---|
| 1 | Unambiguous language | MET | MET | Both use "must" style rules |
| 2 | Concrete rather than abstract | MET | MET | Worked-example tables in both |
| 3 | Each section has one purpose | MET | MET | Section titles match content |
| 4 | Terms defined on first use | NOT MET | NOT MET | Neither defines WC-3, WC-4 or WC-6 by name where first cited |
| 5 | Actionable next steps | MET | MET | V1 run-notes line (FR-009); V2 recommendation in risk 1 |

Subtotal: V1 4, V2 4.

### Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | NOT MET | NOT MET | Both list 5 to 6 risks without probability or impact |
| 2 | Mitigation for each risk | NOT MET | NOT MET | V1 R3 to R5 and V2 risks 5 and 6 have none |
| 3 | Failure modes and recovery | MET | MET | V1 R1; V2 risk 2 (recovery method is flawed, see Correctness 4) |
| 4 | External dependencies and failure scenarios | MET | MET | V1 R2, R4; V2 risk 6 and the Orca listing question |
| 5 | Validation mechanism | MET | MET | Pre-dispatch free-path check in V1 FR-006 and V2 FR-005 |

Subtotal: V1 3, V2 3.

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|---|---|---|---|
| 1 | Collection boundaries (one, many siblings) | MET | MET | V1 example of three parallel workers; V2 FR-004 |
| 2 | State across component boundaries | MET | MET | V1 R1, R2; V2 risk 2 |
| 3 | Guard condition gaps | MET | MET | V1 FR-006, FR-007; V2 FR-005 to FR-007 |
| 4 | Count divergence (attempt numbering, limits) | NOT MET | MET | V2 FR-012 ties attempts to the 2-fix, 3-attempt limit and risk 3 flags trailing digits; V1 does not |
| 5 | Interaction effects | MET | MET | V1 R3, FR-008; V2 FR-013, FR-014 |

Subtotal: V1 4, V2 5.

### Qualitative Summary

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 4 | 4 |
| Correctness | 5 | 3 |
| Structure | 5 | 5 |
| Clarity | 4 | 4 |
| Risk Coverage | 3 | 3 |
| Invariant & Edge Case | 4 | 5 |
| **Total** | **25 / 30 = 0.833** | **24 / 30 = 0.800** |

### Edge Case Floor Check

Threshold 1 of 5 on Invariant & Edge Case Coverage: V1 has 4, V2 has 5. Both eligible.

## Position-Bias Mitigation

The protocol asks for two independent passes (input order, then reverse order). That was not run: at depth quick one orchestrator scored both variants once, in input order, with no independent second pass. Residual risk: order bias toward Variant 1. Effect on the result: the combined scores differ by 0.003, so the choice is made by the tiebreaker, which uses the debate record and not these scores alone.

## Combined Scoring

| Variant | quant x0.50 | qual x0.50 | Combined |
|---|---|---|---|
| Variant 1 (opus:scribe) | 0.472 | 0.417 | 0.888 |
| Variant 2 (sonnet:analyzer) | 0.485 | 0.400 | 0.885 |

Margin: 0.003 (0.3 points), inside the 5% tiebreaker band.

Tiebreaker applied: yes.

- Level 1, debate performance (agreed points won, from the scoring matrix in `debate-transcript.md`): Variant 2 won 5 (S-003, C-003, C-004, C-008, X-002); Variant 1 won 3 (S-002, C-007, A-003); 2 were MERGE and 6 unresolved. The gap, 2 of 16 points (12.5%), is above 5%, so Level 1 decides.
- Levels 2 and 3 were not needed. For the record, Level 2 (correctness criteria met) would have favoured Variant 1, 5 against 3; the two levels point in opposite directions, so the choice of base is a close call and the refactoring plan carries V1's correctness fixes into the merge.

## Selected Base: Variant 2 (sonnet:analyzer)

### Selection Rationale

Variant 2 won more debate points (5 against 3), is the contract's own worked example generalized, has the broader set of state rules (WC-3 re-run, guard refusals, sibling subjects, undecided merge-back) and the fuller section coverage. It loses on three verified defects: it ignores folders other tools already own under `.dev/` (X-001, A-002), FR-011 is wrong for the contract's two-token example, and its counter recovery by listing directories undercounts (A-003).

### Strengths to Preserve from Base

- Pattern `.dev/<command>/<subject>-<n>/` (as the starting shape), root-cause framing, FR-001 to FR-010, FR-012 to FR-016, the Retries, Nested commands and Child worktrees sections, the examples table and the open risks.

### Strengths to Incorporate from Non-Base Variants

- V1 run-notes audit line per name (FR-009, U-002).
- V1 decisions table for the seed brief's open questions (S-002, U-003).
- V1 correct recovery rule: the counter comes from written run notes, because a guard-refused attempt leaves no directory (A-003, V1 R1).
- V1 attempt-only change for the circuit-breaker comparison, replacing V2 FR-011 (C-005).
- V1 `-1` suffix from the first run as a requirement (C-007).
- V1 root-isolation point as an open decision, with V2's reserved-name rule as the base answer (C-001, X-001, A-002 are unresolved, so both options are recorded, not decided).
