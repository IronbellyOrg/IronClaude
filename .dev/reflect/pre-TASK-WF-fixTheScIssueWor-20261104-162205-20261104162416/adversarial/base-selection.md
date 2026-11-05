# Base Selection Report

- Generated: 2026-11-04T17:03:27Z
- Artifact type: Tier-2 reviewer cards (YAML: reviewer, persona, model_class, verdict, self_reported_confidence, findings, self_audit)
- Source requirements, used for RC: source.md:1 has no formal IDs, so topic-level matching was used against 7 requirement topics:
  - R1: rule in each agent's Rules section
  - R2: the files are input files for the orchestrator's next tool calls
  - R3: the consumers (`gh --body-file`, `/sc:recommend`)
  - R4: the harness note does not apply
  - R5: returning content as text is a failure (`E-WORKER-NO-OUTPUT`)
  - R6: a regression test in tests/skills/test_issue_worker_agents.py
  - R7: the Files scope

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (sonnet:analyzer) | Variant 2 (haiku:qa) | Variant 3 (opus:refactorer) |
|--------|--------|-------------------|-------------------|-------------------|
| requirement_coverage | 0.30 | 1.000 (7/7: R1-R5 via F2, R6 via F4, R7 via F1 and F3) | 0.857 (6/7: R4 harness exemption not referenced) | 0.857 (6/7: R5 `E-WORKER-NO-OUTPUT` not referenced) |
| internal_consistency | 0.25 | 1.000 (0 contradictions in 13 claims) | 1.000 (0 in 11) | 1.000 (0 in 13) |
| specificity_ratio | 0.15 | 0.846 (11/13; "could" in F4 and F6) | 0.909 (10/11; "ideally" in R2-3) | 0.923 (12/13; the "or drop it" option in F3) |
| dependency_completeness | 0.15 | 1.000 (all cited lines resolve: test:160-169, create.md:32) | 1.000 (reviewer-briefs/reviewer-2.md:34-37, SKILL.md:64 resolve) | 1.000 (SKILL.md:94, claim.md:24,54,58, create.md:20,32 resolve) |
| section_coverage | 0.15 | 1.000 (7/7 top-level keys) | 1.000 (7/7) | 1.000 (7/7) |
| **quant_score** | | **0.977** | **0.944** | **0.945** |

All citations were re-checked by the orchestrator with sed/grep on 2026-11-04.

## Qualitative Scoring (50% weight) — Additive Binary Rubric (30 criteria, CEV)

The evidence below is the final result after the two-pass position-bias check (see the next section).

### Completeness

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | F1-F4 touch R1-R7 | MET | self_audit: "Six requirement-bearing spans in source.md:1 all located in Tasks 1-3" | NOT MET | No finding covers the missing E-WORKER-NO-OUTPUT in Rules (M-03); the advocate conceded silence |
| Addresses edge cases/failures | MET | F6 verify-sync failure; F4 | MET | R2-5 trailing-period boundary | MET | F4: analysis/ only on out_of_date |
| Includes dependencies/prerequisites | MET | self_audit: scans, no plugins mirror | MET | anchors with lines, 500-line cap | MET | spawn sections of refs/claim.md and refs/create.md read |
| Defines success/completion criteria | MET | verdict plus a recommendation per finding | MET | same | MET | same |
| Specifies out-of-scope items | MET | F3 flags-user.md; F6 "do not fix it here" | MET | R2-4 "no tasklist change" | MET | F4 "record that refs stay unchanged on purpose" |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Correctness

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims | NOT MET | F4 "a no-op removal could pass vacuously" is mechanically false; conceded in Round 2 | MET | Every claim verified, including the anchors | MET (after re-evaluation) | F3's facts are true (flags-t1 feeds --compare, SKILL.md:94); only its drift judgement was conceded |
| Feasible approaches | MET | recommendations are text edits | MET | same | MET | same |
| Consistent terminology | MET | taxonomy used consistently | MET | same | MET | same |
| No internal contradictions | MET | IC 1.0 | MET | IC 1.0 | MET | IC 1.0 |
| Claims supported by evidence | MET | file_line on every finding | MET | same | MET | same |
| **Subtotal** | **4/5** | | **5/5** | | **5/5** | |

### Structure

| Criterion | V1 | V2 | V3 | Evidence (all) |
|---|---|---|---|---|
| Logical ordering | MET | MET | MET | header, then findings, then self_audit |
| Consistent hierarchy | MET | MET | MET | uniform finding schema |
| Separation of concerns | MET | MET | MET | claim / class / severity / recommendation fields |
| Navigation aids | MET | MET | MET | finding IDs and file_line cross-references |
| Follows artifact conventions | MET | MET | MET | reviewer-card schema |
| **Subtotal** | **5/5** | **5/5** | **5/5** | |

### Clarity

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET (after re-evaluation) | "could" only describes a risk's possibility; every recommendation is definite | NOT MET | R2-3 "ideally the tool calls" leaves the instruction open | MET | definite recommendations |
| Concrete | MET | named files and lines | MET | same | MET | same |
| Each item summarizable | MET | one-line claims | MET | same | MET | same |
| Terms defined | MET | uses the plan's terms | NOT MET | R2-4 "INF-001..003" undefined in the card | MET | uses the plan's terms |
| Actionable next steps | MET | per-finding recommendation | MET | same | MET | same |
| **Subtotal** | **5/5** | | **3/5** | | **5/5** | |

### Risk Coverage

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | severity only, no probability | NOT MET | same | NOT MET | same |
| Mitigation per risk | MET | a recommendation per finding | MET | same | MET | same |
| Failure modes and recovery | MET | F6: report and do not fix | NOT MET | no failure-mode recovery stated | MET | F1: mis-copy failure mode plus a check |
| External dependency failure | MET | F6: make verify-sync | NOT MET | none | MET | F4: /sc:analyze picks the name |
| Monitoring/validation mechanism | MET | F4 pre-assertion | NOT MET | none proposed; red-run feasibility is an observation | MET | F6 position check |
| **Subtotal** | **4/5** | | **1/5** | | **4/5** | |

### Invariant & Edge Case Coverage

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Collection boundaries | NOT MET | none | NOT MET | none | MET | F4: analysis/ may be empty (out_of_date only) |
| State interactions across components | MET | F2: content split across early section and Rules | MET | R2-3 | MET | F3: consumers across orchestrator steps |
| Guard condition gaps | MET | F4: missing pre-assertion | NOT MET | none | MET | F6: missing position guard |
| Count divergence | MET | F4: "exactly once" | MET | SKILL.md 153 < 500; file-list union | NOT MET | none |
| Interaction effects | MET | F6: verify-sync with unrelated drift | MET | R2-1: spawn prompt vs Rules | MET | F2: wording vs harness note |
| **Subtotal** | **4/5** | | **3/5** | | **4/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 | Variant 3 |
|-----------|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 | 4/5 |
| Correctness | 4/5 | 5/5 | 5/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 3/5 | 5/5 |
| Risk Coverage | 4/5 | 1/5 | 4/5 |
| Invariant & Edge Case | 4/5 | 3/5 | 4/5 |
| **qual_score** | **27/30 = 0.900** | **22/30 = 0.733** | **27/30 = 0.900** |

Edge-case floor (at least 1/5 required): V1 4/5, V2 3/5, V3 4/5. All three are eligible.

## Position-Bias Mitigation

Pass 1 ran in input order (V1, V2, V3). Pass 2 ran in reverse order (V3, V2, V1).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Clarity: unambiguous language | V1 | NOT MET | MET | DISAGREE | MET. The hedges ("could fail", "could pass") state the possibility of a risk; none of the recommendations is ambiguous. The criterion targets vague instructions. |
| Correctness: no factual errors | V3 | NOT MET | MET | DISAGREE | MET. R3-F3's stated facts are verified true. The concession covered only whether the finding matters, which is a judgement and not a factual error. |
| Correctness: no factual errors | V1 | NOT MET | NOT MET | AGREE | NOT MET. The mechanics claimed in R1-F4 are false. |
| Risk: monitoring mechanism | V2 | NOT MET | NOT MET | AGREE | NOT MET |

- Disagreements re-evaluated: 2
- Final verdicts changed from pass 1: 2 (V1 Clarity-1 and V3 Correctness-1, both to MET)

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate points won (tiebreaker) |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (sonnet:analyzer) | 0.489 | 0.450 | **0.939** | 4 of 17 (23.5%) |
| V2 (haiku:qa) | 0.472 | 0.367 | **0.839** | 6 of 17 (35.3%) |
| V3 (opus:refactorer) | 0.473 | 0.450 | **0.923** | 6 of 17 (35.3%) |

- **Margin**: V1 leads V3 by 0.016 (1.6%), which is below the 5% threshold.
- **Tiebreaker applied**: Yes. Level 1 is debate performance: V3 won 6 points to V1's 4, a gap of 11.8 points, more than 5%. V3 is selected. No level-2 tiebreak was needed.

## Selected Base: Variant 3 (opus:refactorer)

### Selection Rationale
- The top two variants score within 5%, so the protocol's level-1 tiebreaker decides. Variant 3 won more debate points, and its positions became the consensus on the most diff points that bear on plan correctness: C-003, C-004, C-006, C-007, S-003 and A-003.
- Variant 3 holds the findings about defects in the plan's own text that every advocate kept: M-09, M-11 and M-12.
- Variant 3's one dropped finding (R3-F3, M-10) is cleanly removable.
- Variant 1's main correctness loss (R1-F4, the vacuity claim) was a false mechanical claim. Variant 1's advocate conceded it.

### Strengths to Preserve from Base
1. R3-F2: the "reports under analysis/" wording (M-09), strengthened by INV-008.
2. R3-F4: "names each exact path" cannot hold for analysis/ (M-11).
3. R3-F6: the missing check on the Rules bullet's position (M-12).
4. R3-F1: the delimiter ambiguity, with its mechanism (M-06).
5. R3-F5: the grounding_gap on the unstored coordinator message, scoped to the early section (M-01).

### Strengths to Incorporate from Non-Base Variants
1. From V2, R2-3 and from V1, R1-F2: the Rules bullet is a pointer without `E-WORKER-NO-OUTPUT` (M-03, drift).
2. From V2, R2-1: the SKILL.md line is outside the spec's Files list (M-02, drift; record sign-off or descope).
3. From V1, R1-F6: the risk of verify-sync failing on unrelated drift (M-07; evidence Makefile:188-200).
4. From V2, R2-5 and V1, R1-F5: the trailing-period and outer-delimiter details, added into M-06.
5. From the invariant probe and Round 2.6: M-13 (INV-001, blocking), M-14 (INV-002) and M-15 (INV-003).
