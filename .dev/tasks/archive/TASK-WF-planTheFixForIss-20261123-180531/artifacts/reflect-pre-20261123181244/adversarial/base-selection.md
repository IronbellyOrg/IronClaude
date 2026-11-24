# Base Selection Report

## Quantitative Scoring (50% weight)

Computed by the orchestrator from the variant text. SR and SC come from a line-count script run on the three variant files (substantive lines = non-heading, non-blank, non-separator lines; concrete = lines with a digit, `.py`, `.md` or `/sc:`; vague = lines matching the scoring-protocol vague list): v1 19 substantive, 10 concrete, 0 vague, 5 H2; v2 28, 20, 0, 6 H2; v3 21, 12, 1, 4 H2. RC uses topic matching against the eight source clauses INF-001..INF-008 (REPORT.md inferred-requirements table), because the source has no formal requirement IDs that all cards use. IC and DC are orchestrator judgments recorded with their basis.

| Metric | Weight | Variant 1 (analyzer) | Variant 2 (qa) | Variant 3 (refactorer) |
|--------|--------|----------------------|----------------|------------------------|
| requirement_coverage | 0.30 | 0.875 (7/8; INF-007 repaired-output evidence not addressed) | 1.000 (8/8, explicit INF table) | 1.000 (8/8 spec units listed, v3:20) |
| internal_consistency | 0.25 | 0.947 (1 contradiction: row 1 graded Medium yet called harmless, over 19 substantive lines) | 1.000 (0) | 1.000 (0) |
| specificity_ratio | 0.15 | 1.000 (10/10) | 1.000 (20/20) | 0.923 (12/13) |
| dependency_completeness | 0.15 | 1.000 (no unresolved internal refs) | 1.000 (plan link at v2:17 is an external-document ref, excluded by rule; it is wrong by one level) | 1.000 |
| section_coverage | 0.15 | 0.833 (5/6) | 1.000 (6/6) | 0.667 (4/6) |
| **quant_score** | | **0.924** | **1.000** | **0.938** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV evidence is a card line (v1:N, v2:N, v3:N), a calibration line (rN:N), or a debate-transcript point. MET = 1, NOT MET = 0.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | NOT MET | misses wizard refs under "matching documentation" (X-001); INF-007 not addressed | NOT MET | claims INF004 covered (v2:23) though wizard refs stale (X-001) | MET | eight units audited, docs gap found (v3:14, v3:20) |
| Addresses edge cases/failures | MET | caller template equal to default, empty suppression (v1:13, v1:22) | MET | partial/insufficient success, spaces/comma paths (v2:25) | MET | scaffold flow, quoting (v3:16-17) |
| Includes dependencies/prerequisites | MET | preflight/inline_job dependency (v1:13) | MET | helpers and public group (v2:34) | MET | task dependency chain (v3:25) |
| Defines success/completion criteria | NOT MET | no verifier (r1:11 actionability) | MET | requirement-to-plan acceptance map (v2:18-27) | MET | concrete rows/count change (v3:14) |
| Specifies out-of-scope items | MET | resume outside plan; broader list out of scope (v1:14-15) | MET | verdict scope statement (v2:39) | MET | historical exclusions (v3:27) |
| **Subtotal** | **3/5** | | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors | NOT MET | resume consequence false (r1:16; X-002) | NOT MET | zero deviations / INF004 covered wrong (X-001); relative link wrong (r2:7) | NOT MET | prescribed count "four to six" is an acceptance number the debate showed is eight (Round 2) |
| Feasible approaches | MET | v1:21-23 | MET | v2:29-36 | MET | v3:23-25 |
| Terminology consistent | NOT MET | off-taxonomy "Note" (r1:9) | NOT MET | category vocabulary differs from rubric (r2:9) | NOT MET | dual severity/grade labels (r3:9) |
| No internal contradictions | NOT MET | "Medium" yet "harmless" (v1:13) | MET | none found | MET | none found |
| Claims supported by evidence | NOT MET | resume claim rests on grep only (v1:15, r1:7) | MET | all citations match (r2:16) | MET | cited locations match (r3:7) |
| **Subtotal** | **1/5** | | **3/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Logical section ordering | MET | verdict, table, summary, limits | MET | verdict, coverage, feasibility | MET | verdict, table, summary, checks |
| Consistent hierarchy depth | MET | H1/H2 only | MET | H1/H2 only | MET | H1/H2 only |
| Separation of concerns | MET | findings, reasons, limits separate | MET | coverage vs feasibility separate | NOT MET | corrective actions embedded in finding row (v3:14), no recommendation section (S-007) |
| Navigation aids / cross-references | MET | calibration refs | MET | plan-line cross-refs | MET | plan-line refs |
| Follows artifact conventions | MET | reflect card shape | MET | reflect card shape | MET | reflect card shape |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | NOT MET | "Medium ... harmless" (v1:13) | MET | | MET | |
| Concrete rather than abstract | MET | file:line rows | MET | file:line rows | MET | file:line rows |
| Clear section purpose | MET | | MET | | MET | |
| Terms defined on first use | NOT MET | INF/Drift shorthand undefined | NOT MET | INF shorthand undefined | NOT MET | "Authorized expansion1" etc. undefined |
| Actionable next steps | MET | wizard-guide disposition (v1:14) | MET | keep evidence requirements (v2:42) | MET | blocker fix list (v3:14) |
| **Subtotal** | **3/5** | | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| ≥3 risks with probability and impact | NOT MET | no probability | NOT MET | no risk register (r2:10) | NOT MET | no probability |
| Mitigation per risk | MET | suggestion per row | NOT MET | no risks stated | MET | suggestion per row |
| Failure modes/recovery | MET | empty suppression (v1:22) | MET | insufficient-success handling (v2:25) | MET | scaffold placeholder failure (v3:16) |
| External dependencies | MET | adversarial.md consumer (v1:21) | MET | command + skill (v2:33) | MET | consumer interface (v3:17) |
| Monitoring/validation mechanism | NOT MET | no verifier (r1:11) | MET | red/green evidence (v2:24) | MET | scaffold test, count check (v3:14, v3:16) |
| **Subtotal** | **3/5** | | **3/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Collection boundaries | MET | existing-file count guard (v1:21) | MET | partial/insufficient success (v2:25) | MET | count/path/empty-suggestion guards (v3:20) |
| State across components | MET | inline_job after preflight (v1:13) | MET | spec_dict vs preflight (v2:35) | MET | scaffold -> spec -> run (v3:16) |
| Guard condition gaps | MET | default-detection rule missing (v1:13) | NOT MET | said no gap (v2:35) | MET | v3:16 |
| Count divergence | NOT MET | none | MET | 2-10 count (v2:33) | MET | occurrence count (v3:14) |
| Interaction effects | MET | sibling prefix golden (v1:23) | NOT MET | none | MET | wizard tables vs run output, sibling protection (v3:14, v3:26) |
| **Subtotal** | **4/5** | | **3/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|
| Completeness | 3/5 | 4/5 | 5/5 |
| Correctness | 1/5 | 3/5 | 3/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 3/5 | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 3/5 | 4/5 |
| Invariant & Edge Case | 4/5 | 3/5 | 5/5 |
| **qual_score** | **19/30 = 0.633** | **22/30 = 0.733** | **25/30 = 0.833** |

## Edge Case Floor Check

V1 4/5, V2 3/5, V3 5/5: all at or above the 1/5 floor, all eligible.

## Position-Bias Mitigation

Pass 1 in input order (V1, V2, V3); Pass 2 in reverse order (V3, V2, V1). Both passes were run by the orchestrator in the same context, so this is not an independent re-evaluation.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Correctness: no factual errors | V3 | MET (citations all match, r3:7) | NOT MET (fix count four to six is a wrong acceptance number) | DISAGREE | NOT MET: re-evaluated with both passes' evidence; the count is a number the plan fix would rest on and Round 2 showed eight, so the stricter verdict holds |

Disagreements re-evaluated: 1
Final verdicts changed from Pass 1: 1

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---|---|---|---|---|
| V1 (analyzer) | 0.462 | 0.317 | **0.779** | 3 points won (S-006, S-007, C-002) |
| V2 (qa) | 0.500 | 0.367 | **0.867** | 2 points won (S-004, C-009) |
| V3 (refactorer) | 0.469 | 0.417 | **0.886** | 15 points won |

**Margin**: V3 minus V2 = 0.019 (1.9%, below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance): V3 won 15 diff points, V2 won 2.

## Selected Base: Variant 3 (reviewer-3 card, persona refactorer, requested model opus)

### Selection Rationale
V3 is the only card whose verdict survives the debate: all three advocates conceded that plan:81 and plan:84 are false given the wizard reference tables (X-001, 100% confidence), and the fault-finder found nothing that makes the FAIL verdict or the Blocking finding wrong (invariant-probe.md). V3 also carries the scaffold (C-003) and quoting (C-004) Mediums, and its resume reading (X-002) is correct. Its calibrated confidence is the highest (0.87). It wins the tiebreaker by debate performance after a 1.9% margin over V2, whose structural advantages are incorporated below.

### Strengths to Preserve from Base
1. FAIL verdict with one Blocking (Decision) finding on plan:81/plan:84 (v3:8, v3:14).
2. Medium findings on default-vs-caller provenance and quoting (v3:16-17).
3. Correct resume reading and two-file boundary check (v3:23).
4. Historical-exclusion confirmation (v3:27).

### Strengths to Incorporate from Non-Base Variants
1. From V2: the INF-001..INF-008 to plan-line coverage table (v2:18-27), corrected for INF-004.
2. From V2: feasibility notes, especially the public `swarm_group` gap (v2:34) and the reduce.py:672-697 oracle (v2:32).
3. From V1: the wizard-guide.md:216 finding read correctly (v1:14, C-002) and the explicit limits disclosure style (v1:27-28).
4. From V1: consumer/suspect coupling evidence (v1:21) and the verified bare-review golden prefix (v1:23, U-007).
5. From the debate and probe: corrected blocker fix (eight mentions, required search, plan:20/:75/:84 wording, INV-007), refined C-003 rule with explicit refactor-find condition (INV-001, INV-003), quoting proven against the consumer and confined to the refactor-find branch (INV-004, INV-005), and Low notes INV-008..INV-010.
6. Refutation of V1's resume claim recorded as a dropped finding.
