# Base Selection

## Quantitative Scoring (50% weight)

Formula: quant = RC x 0.30 + IC x 0.25 + SR x 0.15 + DC x 0.15 + SC x 0.15. Every count below comes from the variant files (`variant-N-original.md`, per-file line numbers).

### RC: Requirement Coverage, by topic match against 12 review topics drawn from the plan

The 12 review topics, with the plan lines they come from:

| # | Topic | Plan lines |
|---|---|---|
| 1 | Force propagation | 45, 50 |
| 2 | Nonforce skip with no Orca calls | 50 |
| 3 | No external --force | 23, 50 |
| 4 | Edited guides not rewritten | 23, 50 |
| 5 | Meaningful output relay and visible safe skip | 24, 45, 51 |
| 6 | Nonfatal absent, failure or timeout | 51 |
| 7 | Backward-compatible force argument | 45 |
| 8 | Distinguish Task 1 CLI sessions from shells | 35 |
| 9 | Worker and internal-agent boundaries | 36 |
| 10 | Separate mocked evidence from live evidence | 52 |
| 11 | Sync | 47, 52 |
| 12 | Named regression list | 52 |

Topics each variant covers:

| Variant | Topics hit | RC |
|---|---|---|
| V1 | 1, 2, 3 (card line 26); 4 and 5 (line 16); 8 (line 22); 11 and 12 (lines 9-12) | 8/12 = 0.667 |
| V2 | 1-7 (card line 12); 8 and 9 (line 13); 10 (line 14) | 10/12 = 0.833 |
| V3 | 1, 2, 7 (lines 23-24); 5 (line 21); 6 (line 24); 11 (line 25); 12 (lines 9-16) | 7/12 = 0.583 |

V2 topic 12: after the pass re-evaluation recorded below, "run planned guidance checks" (line 17) is not counted, because it names neither the routing-block test nor the wider regression set.

### IC: Internal Consistency

IC = 1 - contradictions/claims.

| Variant | Contradiction found | IC |
|---|---|---|
| V1 | R1-1's claim conflicts with its own note "not an omission" (lines 9 vs 12) | 1 - 1/12 = 0.917 |
| V2 | The covered count 21/21 (line 9) conflicts with "full matrix completeness not independently checked" (line 22) | 1 - 1/9 = 0.889 |
| V3 | None | 1 - 0/10 = 1.000 |

### SR: Specificity

SR = concrete/(concrete+vague).

| Variant | Concrete | Vague | SR |
|---|---|---|---|
| V1 | 8 | 2 (self-audit lines 25 and 27) | 8/10 = 0.800 |
| V2 | 7 | 4: the unsupported 21/21, self-audit lines 11 and 13, verifier line 17 | 7/11 = 0.636 |
| V3 | 9 | 1: self-audit line 24 claims behavior is preserved without anchors | 9/10 = 0.900 |

### DC: Dependency Completeness

DC = emitted references that resolve / total emitted references.

| Variant | Resolved | DC |
|---|---|---|
| V1 | 3/4. The three plan_refs resolve within the 53-line plan; `install_user_setup.py:113-119` does not resolve to the helper (it is inside `install_rules`). | 0.750 |
| V2 | 2/2. `reviewer-briefs/reviewer-2.md:49-82` and `:137` resolve, since the brief has 157 lines. | 1.000 |
| V3 | 6/6. Resolved: `install_user_setup.py:230-263`; plan 45-51; `tests/core/test_codegraph_guide.py:137-174`; `tests/cli/test_bash_inspection_policy.py:32`; `tests/cli/test_issue_body_templates.py:18`; `tests/core/test_how_we_work_routing_table.py`. Each of the last three exists and reads a core `CLAUDE.md`. A resolving location is not a verified defect. | 1.000 |

### SC: Section Coverage

SC = top-level keys / max.

| Variant | Top-level keys | SC |
|---|---|---|
| V1 | 12 | 12/16 = 0.750 |
| V2 | 16 | 16/16 = 1.000 |
| V3 | 12 | 12/16 = 0.750 |

### Quantitative Summary

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC | 0.30 | 0.667 | 0.833 | 0.583 |
| IC | 0.25 | 0.917 | 0.889 | 1.000 |
| SR | 0.15 | 0.800 | 0.636 | 0.900 |
| DC | 0.15 | 0.750 | 1.000 | 1.000 |
| SC | 0.15 | 0.750 | 1.000 | 0.750 |
| **Quant** | | **0.7742** | **0.8677** | **0.8225** |

## Qualitative Scoring (50% weight): additive binary rubric, CEV protocol

Every verdict is CLAIM / EVIDENCE / VERDICT. There is no partial credit. Evidence is per-file card lines, plan lines, or code lines.

### Completeness (5)

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 1 | Addresses the Task 1 launch requirement (plan 30, 35) | MET: R1-3, line 20 | MET: line 13 | NOT MET: no Task 1 terminal-surface content |
| 2 | Addresses Task 2 force/skip gating (plan 45, 50) | MET: line 26 | MET: line 12 | MET: line 23 |
| 3 | Addresses output relay (plan 45, 51) | MET: R1-2, line 14 | MET: "child output", line 12 | MET: R3-2, line 18 |
| 4 | Addresses the regression scope of plan 52 | MET: R1-1 routing checks, line 11 | NOT MET (re-evaluated): line 17 names only planned guidance checks | MET: R3-1, lines 9-15 |
| 5 | Separates mocked evidence from live evidence (plan 52) | NOT MET: absent | MET: line 14 | NOT MET: absent |
| | Subtotal | 4 | 4 | 3 |

### Correctness (5)

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 1 | Verdict PASS consistent with the debate-agreed ground truth | MET | MET | MET |
| 2 | Every emitted citation resolves to the cited content | NOT MET: 113-119, line 17 | MET: brief lines resolve | MET: 230-263, plan 45-51 |
| 3 | No overstated claim | NOT MET: "not precisely defined", line 14, against plan 24/45/51 | NOT MET: 21/21, line 9 | MET |
| 4 | No existing defect is misclassified as a regression or drift | MET: line 27 | MET: no classification | MET: no classification |
| 5 | No internal contradiction | NOT MET: lines 9 vs 12 | NOT MET: lines 9 vs 22 | MET |
| | Subtotal | 2 | 3 | 5 |

### Structure (5)

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 1 | Findings carry IDs | MET | NOT MET: no findings | MET |
| 2 | Every finding has a plan_ref | MET: lines 10, 15, 21 | NOT MET | NOT MET: R3-1 has none |
| 3 | Verifiers are present | MET | MET: line 15 | MET |
| 4 | A valid evidence anchor field is present | NOT MET: only the wrong `original_source_ref` | MET: line 18 | MET: lines 10, 19 |
| 5 | Limitations are present | MET | MET | MET |
| | Subtotal | 4 | 3 | 4 |

### Clarity (5)

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 1 | Claims are single testable sentences | MET | NOT MET: no claims | MET |
| 2 | Verifiers name a concrete fixture | MET: line 16 | NOT MET: generic "output", line 16 | MET: line 21 |
| 3 | Reading scope is stated | MET: line 24 | MET: line 22 | MET: line 27 |
| 4 | Severity is unambiguous (minor vs blocking) | MET | MET | MET |
| 5 | No brief-local or unresolvable reference emitted as evidence | NOT MET: line 17 | NOT MET: brief-only evidence | MET: 81-82 appears only in limitations, marked do-not-cite (line 30) |
| | Subtotal | 4 | 2 | 5 |

### Risk Coverage (5)

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 1 | Names the hidden-skip-as-success risk | MET: R1-2 | NOT MET: marks output covered | MET: R3-2 |
| 2 | Names the external --force risk | MET: line 26 | MET: line 12 | NOT MET |
| 3 | Names the shared-core-file regression risk | MET: R1-1 | NOT MET | MET: R3-1 |
| 4 | Names the New Terminal misroute risk | MET: R1-3, line 30 | NOT MET: marks it covered | NOT MET |
| 5 | Names the nonfatal-failure risk | NOT MET | MET: line 12 | MET: line 24 |
| | Subtotal | 4 | 2 | 3 |

### Invariant and Edge Case (5)

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 1 | Exit-0 skip with all files present | MET: line 16 | NOT MET | MET: line 21 |
| 2 | Empty-output success case | MET: line 16 | NOT MET | NOT MET |
| 3 | Nonforce guard (early return only when force is false) | MET: line 26 | MET: "default skip", line 12 | MET: "force-gated early return", line 23 |
| 4 | Positional/backward compatibility | NOT MET | MET: line 12 | MET: line 24 |
| 5 | Absent, timeout or incomplete Orca | NOT MET | MET: line 16 | MET: line 24 |
| | Subtotal | 3 | 3 | 4 |

Edge-case floor (at least 1/5): V1 3, V2 3, V3 4. All variants are eligible.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 4 | 3 |
| Correctness | 2 | 3 | 5 |
| Structure | 4 | 3 | 4 |
| Clarity | 4 | 2 | 5 |
| Risk Coverage | 4 | 2 | 3 |
| Invariant and Edge Case | 3 | 3 | 4 |
| **Total** | **21/30** | **17/30** | **24/30** |
| **Qual** | **0.700** | **0.567** | **0.800** |

### Position-Bias Mitigation

- Pass 1 evaluated in forward order (V1, V2, V3). Pass 2 evaluated in reverse order (V3, V2, V1).
- 89 of 90 verdicts agreed. The one disagreement was V2 Completeness #4.
  - Pass 1 marked it MET on "run planned guidance checks".
  - Pass 2 had just read V3's R3-1 and marked it NOT MET.
- Re-evaluation against plan line 52: line 52 names the routing-block test and `tests/unit/test_cli_install.py`, and V2's line 17 names neither. Final verdict: NOT MET. The matching RC topic 12 was also set to not hit for V2, for consistency.

## Combined Scoring

| Variant | Quant (x0.5) | Qual (x0.5) | Final |
|---|---|---|---|
| V1 (sonnet/analyzer) | 0.3871 | 0.3500 | **0.7371** |
| V2 (haiku/qa) | 0.4339 | 0.2833 | **0.7172** |
| V3 (opus/refactorer) | 0.4113 | 0.4000 | **0.8113** |

Margin: V3 leads V1 by 0.0742 and V2 by 0.0941. Both gaps exceed 0.05, so no tiebreaker is needed.

## Selected Base: Variant 3 (reviewer-3-card, opus/refactorer)

### Selection Rationale

Variant 3 has the highest combined score. The result matches the debate, where Variant 3 won 7.0 of 11 points, Variant 1 won 4.0 and Variant 2 won 0.

Its advantages are in Correctness (5/5) and Clarity (5/5):
- the only correct code anchor (`install_user_setup.py:230-263`);
- the only plan_ref matching the 53-line plan with no pathology emitted;
- the sharpest verifier for the L3 state point (C-001, A-002): exit 0, three files present, a visible skip, and no refresh-success claim.

Variant 2 has the highest quantitative score because of breadth (RC, SC, DC). It loses on qualitative depth: it finds nothing, its count is unsupported, and its evidence comes from the brief only.

### Strengths to Preserve from Base

- R3-2, with its code anchor 230-263 and plan_ref 45-51, using "no keyword parser" wording that matches plan line 45.
- R3-1, kept only with its verified reader `tests/core/test_codegraph_guide.py:137-174`. Plan line 52 is attached as the anchor.
- The self-audit statements on bounded scope, positional callers, the sync delivery and no Orca mutation.

### Strengths to Incorporate from Non-Base Variants

- **From V1:**
  - Merge R1-2's empty-output success case into the R3-2 verifier (C-001).
  - Add R1-3 as a minor on Task 1 terminal-surface wording, combined with X-001. Anchors: plan lines 30 and 35, `source.md:1`, `orca-discovery.md:12-16`.
  - Keep R1-1 as an optional ordering note only.
- **From V2:**
  - The preservation checklist and the mocked-versus-live separation (U-003; plan lines 45 and 52), carried as self-audit context.
  - The 21/21 count is carried only as labelled reviewer judgment, next to lexical 13/21 = 0.6190.
