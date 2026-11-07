# Base Selection Report

Step 3 of sc:adversarial, Mode A, `--depth standard`. The orchestrator scores; it ran no debate in this step.
Variants: V1 = `variant-1-original.md` (sonnet:analyzer), V2 = `variant-2-original.md` (haiku:qa), V3 = `variant-3-original.md` (opus:refactorer). All three are read-only.
Source requirements (19): F-1..F-17 (source.md Part 3), the Part 4 texts, and the Part 5 constraints, in `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md`.
Inputs: `diff-analysis.md`, `debate-transcript.md` (22/22 points resolved, CONVERGED), `invariant-probe.md`, and `../artifacts/calibration.yaml` (V1 has 9 wrong line numbers re-mapped; V3 has 1, plan:90 to plan:95; V2 has none).
Formulas: quant = 0.30·RC + 0.25·IC + 0.15·SR + 0.15·DC + 0.15·SC; qual = MET/30; final = 0.50·quant + 0.50·qual.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|--------|--------|---------------|---------|-----------------|
| Requirement Coverage (RC) | 0.30 | 0.632 | 1.000 | 0.842 |
| Internal Consistency (IC) | 0.25 | 0.889 | 1.000 | 0.938 |
| Specificity Ratio (SR) | 0.15 | 0.939 | 0.960 | 0.941 |
| Dependency Completeness (DC) | 0.15 | 0.741 | 1.000 | 0.980 |
| Section Coverage (SC) | 0.15 | 0.750 | 1.000 | 0.500 |
| **quant_score** | | **0.776** | **0.994** | **0.850** |

Computation per variant:

- **RC** (requirements addressed / 19).
  - V1: 12/19 = 0.632. Not addressed: F-6, F-10, F-11, F-13, F-14, F-15 and F-16.
  - V2: 19/19 = 1.000. The `per_correction` rows F-1..F-17 (variant-2:151-167) and the Part 4 and Part 5 rows (:169-185) cover them all.
  - V3: 16/19 = 0.842. Not addressed: F-11, F-14 and F-15. Its checked_clean (variant-3:140) covers F-2, F-13, F-16 and F-17.
- **IC** (1 - contradictions / claims).
  - V1: 1 - 2/18 = 0.889. First contradiction: the `line_numbers` convention (variant-1:9, "brief-file line minus 88") is not followed by its own citations plan:114, :115, :46 and :136. Second: R1-F4's premise ("if one of them were already dirty") rests on [INFERRED] evidence (:82) that its own unverified list (:152) says was not observed.
  - V2: 1 - 0/30 = 1.000. R2-01 ("preserve the pin set") and R2-02 ("the extra pin fails F-7") are consistent, because an equality check is not a pin.
  - V3: 1 - 1/16 = 0.938. R3-2 says the check "adds no new pins" and is "a byte check of text the brief already fixes" (variant-3:46-47). Its mechanism, however, saves the reference text from the executor's own copy (:41-44), so the check is self-referential. V3 conceded this in Round 1. R3-1 and R3-8 are factual errors and are scored under Correctness.
- **SR** (concrete lines / (concrete + vague) lines, comment lines excluded).
  - V1: 93/99 = 0.939. Vague lines: :82, :94, :105, :107, :110, :152.
  - V2: 97/101 = 0.960. Vague lines: :27, :98, :106, :192. All four are [INFERRED] labels or quotations of one.
  - V3: 111/118 = 0.941. Vague lines: :17, :19, :20, :38, :83, :107, :123.
- **DC** (file:line references that resolve to the stated content / all file:line references).
  - V1: 43/58 = 0.741. Fifteen tokens fail, carrying the 9 distinct wrong numbers re-mapped in calibration.yaml: plan:114/115 to 26/27, spec:375/379 to 296/300, lc10:396/401 to 8/13, test_codegraph_adoption.py:532-540 to 75-82, plan:46 to 44 and plan:136 to 137.
  - V2: 140/140 = 1.000. That total is 35 file:line tokens, 88 bracketed plan/source line numbers and 17 `source_verifier_line` values. Calibration re-mapped none of them.
  - V3: 50/51 = 0.980. One fails: plan:90 should be plan:95.
- **SC** (expected card sections present / 4). The four sections are findings, checked_clean, per-requirement coverage and a limits statement.
  - V1: 3/4 = 0.75. It has findings, checked_clean and `unverified` (:151-153); it has no coverage section.
  - V2: 4/4 = 1.00. It has findings, `per_correction` plus `additional_part_checks`, checked_clean, and a limits row (:192).
  - V3: 2/4 = 0.50. It has findings and checked_clean. Its limits appear only inside the R3-1 and R3-5 claims, and it has no coverage section.
- **quant**:
  - V1 = 0.1895 + 0.2222 + 0.1409 + 0.1112 + 0.1125 = **0.776**
  - V2 = 0.3000 + 0.2500 + 0.1440 + 0.1500 + 0.1500 = **0.994**
  - V3 = 0.2526 + 0.2344 + 0.1412 + 0.1470 + 0.0750 = **0.850**

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Each cell gives the claim, the evidence (a citation into the card, written vN:line) and the verdict, with MET or NOT MET in bold. A MET verdict needs a specific citation. The verdicts shown are final, after the two-pass check in Position-Bias Mitigation.

### Completeness

| Criterion | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|-----------|---------------|---------|-----------------|
| 1. Covers all explicit requirements | 12 of 19; F-6, F-10, F-11, F-13 to F-16 are unaddressed (see RC). **NOT MET** | Has a row for each of F-1 to F-17, plus rows for Part 4 and Part 5 (v2:151-185). **MET** | 16 of 19; F-11, F-14 and F-15 are unaddressed. **NOT MET** |
| 2. Edge cases and failure scenarios | A missed refusal gives a false FAIL (R1-F3, v1:59-62); covers the failed, timed-out and Unknown-skill cases (v1:145). **MET** | The verifier deletes an unpinned clause, which then passes (R2-01, v2:27-30); verifier-scope edge case (R2-04, v2:75-78). **MET** | A wrong path makes `grep -c` print 0, which passes for nothing (R3-4, v3:64-65). **MET** |
| 3. Dependencies and prerequisites | Start-state cleanliness (R1-F4, v1:77-80); the managed-workspace `./artifacts/` base and sync-dev outputs (v1:147-148). **MET** | Part 5 row: existing changes, the six-file boundary and UV/test settings (v2:178-185). **MET** | Task 1 runs before Tasks 2-6 by sequential default (v3:139); start-state guard (R3-6, v3:94-98). **MET** |
| 4. Success/completion criteria | A `verifier` for each finding (for example v1:34, :86, :119). **MET** | A `verifier` for each finding (v2:26-30, :45-48, :136-140). **MET** | A `verifier` for each finding, including R3-1's void condition (v3:27-29). **MET** |
| 5. Explicit out of scope | "Owner decision only" (v1:47); "Do not edit the spec beyond the two planned lines" (v1:117-118). **MET** | "Research remains out of scope" (v2:183); "Keep the approved replacement sentence unchanged" (v2:86). **MET** | "Keep the F-13 sentence verbatim" (v3:111); R3-8 is an owner decision (v3:126). **MET** |
| **Subtotal** | **4/5** | **5/5** | **4/5** |

### Correctness

| Criterion | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|-----------|---------------|---------|-----------------|
| 1. No factual errors | 9 distinct wrong line numbers (calibration.yaml; orchestrator note v1:2-4); R1-F4 is void per E-1; R1-F7 was folded. **NOT MET** | No citation re-mapped by calibration; its 14 pass / 3 fail table was upheld in debate (S-001, C-002 to C-005). **MET** | R3-1's premise is void per E-1; R3-8 was dropped because spec:300 makes risk 4 true (C-012); plan:90 was re-mapped. **NOT MET** |
| 2. Approaches feasible | The four-fragment `grep -cF` check (v1:28-32) and the lint rewording (v1:98-99) are both runnable. **MET** | Exact-equality ACs (v2:22-25) and verbatim copying of risks (v2:105-106) are feasible; Round 2 adopted source-derived extraction. **MET** | The `grep -cF -f` byte check (v3:41-47) runs; its self-reference is a consistency defect, not an infeasibility. **MET** |
| 3. Terminology consistent | "plan:N" is defined as brief line minus 88 (v1:9) but used with brief-file numbers (v1:114-116 cites plan:114). **NOT MET** | "pin", "verifier" and "literal" are used the same way throughout (v2:35-37, :146-149). **MET** | "pin" against "byte check" is kept distinct (v3:46-47); `write(s) no nested directory` is kept separate (v3:66). **MET** |
| 4. No internal contradictions | IC 0.889: two contradictions (see IC). **NOT MET** | IC 1.000 (see IC). **MET** | IC 0.938: R3-2's self-reference (see IC). **NOT MET** |
| 5. Claims supported by evidence | Every finding has evidence (for example v1:65-67 cites analyze.md:97-98). **MET** | Every finding has evidence lines (v2:14-20, :39-40, :58-62). **MET** | Every finding has evidence (v3:21, :39, :57, :69, :84, :124). **MET** |
| **Subtotal** | **2/5** | **5/5** | **3/5** |

### Structure

| Criterion | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|-----------|---------------|---------|-----------------|
| 1. Logical ordering | Convention (v1:9), then findings (:11), checked_clean (:137) and unverified (:151). **MET** | Findings (v2:5), per_correction (:144), part checks (:169), checked_clean (:187). **MET** | Header (v3:4-7), then findings (:8) and checked_clean (:132). **MET** |
| 2. Consistent hierarchy | Every finding has the same five keys (v1:12-34). **MET** | Findings, rows and checks each have a uniform schema (v2:151-167). **MET** | Every finding has the same five keys (v3:9-29). **MET** |
| 3. Separation of concerns | Defects (findings), confirmed checks (checked_clean) and limits (unverified) are kept apart. **MET** | Findings are kept apart from verifier results (`per_correction`, v2:144-167) and Part checks (:169-185). **MET** | Findings are kept apart from checked_clean (v3:132-140). **MET** |
| 4. Navigation aids | IDs are cross-referenced ("card finding F-1 / R-1", v1:33) and the citation convention is stated (v1:9). **MET** | Rows link back to findings (`finding: R2-02`, v2:157, :162, :164, :177). **MET** | The header names the plan and brief paths (v3:6-7); IDs R3-1..R3-8 are cross-cited (v3:89). **MET** |
| 5. Artifact-type conventions | The card has findings, checked_clean, unverified and confidence (v1:135-153). **MET** | The card has findings, per-correction verifiers, checked_clean, a limits row and confidence (v2:142-192). **MET** | No limits section; the "could not run git" limit sits inside R3-1's claim (v3:19-20). **NOT MET** |
| **Subtotal** | **5/5** | **5/5** | **4/5** |

### Clarity

| Criterion | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|-----------|---------------|---------|-----------------|
| 1. Unambiguous language | Hedged predictions: "could be skipped" (v1:94), "may sit" (:105), "will usually have" (:107), "could be failed" (:110). **NOT MET** | Its only hedged lines are explicit `[INFERRED]` labels or quotations of one (v2:27, :98, :106, :192). **MET** | Hedged predictions: "could paraphrase" (v3:38), "could flag" (:107), "could read step 4 as passed" (:123). **NOT MET** |
| 2. Concrete | Exact fragments to pin (v1:29-31). **MET** | R2-06 lists the 17 verifier line numbers (v2:130-132). **MET** | Exact AC text (v3:58, :71, :100). **MET** |
| 3. Purpose per section | Each finding opens with a one-sentence claim (for example v1:15). **MET** | Each finding has a one-sentence claim, and `interpretation` states the table's purpose (v2:146-149). **MET** | Each finding opens with a one-sentence claim (for example v3:12). **MET** |
| 4. Terms defined | "UC-1" (v1:8), "lc10" and "P2 live-plan author" (v1:105) are used undefined. **NOT MET** | "INV-022 and INV-023" (v2:97) and F-n IDs are used undefined. **NOT MET** | "INV-001 reasoning" (v3:18) and "F-2" (v3:17) are used undefined. **NOT MET** |
| 5. Actionable next steps | Every finding has `exact_change`, and owner decisions are flagged (v1:46-48, :115-118). **MET** | Every finding has `exact_change`; R2-03 asks for a clarification (v2:63-66). **MET** | Every finding has `exact_change`; R3-8 offers two owner options (v3:125-129). **MET** |
| **Subtotal** | **3/5** | **4/5** | **3/5** |

### Risk Coverage

| Criterion | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|-----------|---------------|---------|-----------------|
| 1. At least 3 risks, each with probability and impact | False FAIL on a timed-out run, and the lc10-class FAIL (R1-F1, v1:20-22). Missed-refusal false FAIL (R1-F3, v1:61). Condition-2 failure that "usually" applies (R1-F6, v1:107-110). Each is rated P2 or P3. **MET** | Findings report where the literal verifier fails (v2:35-37, :53-57). None gives the likelihood or runtime impact of a false PASS or false FAIL. **NOT MET** | AC infeasible (R3-1, v3:17). Check passes "for nothing" (R3-4, v3:65). Lint halt "for a reason outside this plan" (R3-5, v3:81). Each is rated P2 or P3 and carries an [INFERRED] likelihood qualifier. **MET** |
| 2. Mitigation per risk | `exact_change` for every finding (v1:27-33, :68-71). **MET** | `exact_change` for every finding (v2:21-25, :105-106). **MET** | `exact_change` for every finding (v3:22-26, :85-89). **MET** |
| 3. Failure modes and recovery | Mode: refusal missed. Recovery: record `not verifiable` (v1:69-71). **MET** | checked_clean asserts the qualifications are retained (v2:189) and does not probe how they fail. No recovery path is given. **NOT MET** | Mode: `git show` fails and grep prints 0 (v3:64-65). Recovery: the void condition (v3:28-29). **MET** |
| 4. External dependencies | Session-file encoding (v1:153). Chat-only refusal (analyze.md:97, v1:59). Whole-repo ruff (Makefile:48-50, v1:91-93). **MET** | Names session-file encoding as not verified (v2:192) but gives no failure scenario for it. **NOT MET** | Whole-repo ruff over the out-of-scope dirty files (v3:79-81). `git add .dev/tasks` (managed-workspace.md:36, v3:13-14). **MET** |
| 5. Monitoring or validation | A `verifier` per finding (v1:34, :72). **MET** | `verifier` per finding, plus the per_correction table (v2:150-167). **MET** | A `verifier` per finding (v3:48, :90). **MET** |
| **Subtotal** | **5/5** | **2/5** | **5/5** |

### Invariant & Edge Case Coverage

| Criterion | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|-----------|---------------|---------|-----------------|
| 1. Boundary conditions for collections | Tier 1 anchor is the first match, ahead of the research tiers at 42/63 (v1:139). The `**Under**` lead-in appears once inside Wave 2A (v1:138). **MET** | Notes only that "the two routing tiers are pinned separately" (v2:190). Does not analyse the first-match, empty or duplicate cases. **NOT MET** | The bold lead-in appears once in Wave 2A. The Tier 1 end anchor is distinct from the research Tier 2 (v3:137). **MET** |
| 2. State across component boundaries | Spec step 5 condition 2 against a nested Skill call inside a `Task` subagent (R1-F6, v1:105-111). **MET** | Gives no analysis of state that crosses components. **NOT MET** | `/sc:implement`'s `git add .dev/tasks` against Task 7's status snapshot (R3-1, v3:12-18). **MET** |
| 3. Guard condition gaps | No start-state guard (R1-F4). `--report-dir` is matched literally (v1:62-64). **MET** | Unpinned clauses of the approved text are unguarded (R2-01, v2:27-30). **MET** | Task 5 lacks the `git cat-file -e` guard (R3-4, v3:63-65). **MET** |
| 4. Count divergence | `_removals` +2 (v1:140). The `grep -c 2` is only a smoke check (v1:143). **MET** | Requires the saved count plus two, never 18 or 19 (F-8 row, v2:158). **MET** | `text.replace` removes every occurrence, so +2 holds (v3:135). **MET** |
| 5. Interaction effects | Whole-repo lint combined with out-of-scope dirty files (R1-F5, v1:91-95). **MET** | The F-12 quantifier conflicts with F-3's independent pin (R2-03, v2:53-57). **MET** | Lint combined with dirty files (R3-5). The planned text against other brainstorm tests (v3:138). **MET** |
| **Subtotal** | **5/5** | **3/5** | **5/5** |

### Qualitative Summary

| Dimension | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|-----------|---------------|---------|-----------------|
| Completeness | 4/5 | 5/5 | 4/5 |
| Correctness | 2/5 | 5/5 | 3/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 3/5 | 4/5 | 3/5 |
| Risk Coverage | 5/5 | 2/5 | 5/5 |
| Invariant & Edge Case | 5/5 | 3/5 | 5/5 |
| **Total** | **24/30** | **24/30** | **24/30** |
| **qual_score** | **0.800** | **0.800** | **0.800** |

The three cards tie on the qualitative layer, each scoring 24 of 30. The pattern of strengths differs:

- V2 earns its points in Completeness and Correctness, the dimensions that check fidelity to the brief.
- V1 and V3 earn theirs in Risk Coverage and Invariant & Edge Case, the dimensions that check runtime behaviour.

### Edge-Case Floor Check

| Variant | Invariant & Edge Case score | Floor (at least 1/5) | Eligible as base |
|---------|-----------------------------|----------------------|------------------|
| V1 | 5/5 | Pass | Yes |
| V2 | 3/5 | Pass | Yes |
| V3 | 5/5 | Pass | Yes |

## Position-Bias Mitigation

The rubric was scored twice. Pass 1 took the variants in the order V1, V2, V3; pass 2 took them in the order V3, V2, V1. For each disagreement below, the criterion was re-scored with the specific card line(s) open. The final column is the verdict used in the tables above.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation basis |
|-----------|---------|--------|--------|-----------|-------|---------------------|
| Completeness 2 | V2 | NOT MET | MET | Disagree | MET | R2-01's verifier (v2:27-30) and R2-04 (v2:75-78) both describe a failure scenario. |
| Correctness 5 | V1 | MET | NOT MET | Disagree | MET | Every finding carries evidence. Wrong numbers are already penalised in Correctness 1 and DC, so they are not counted again here. |
| Correctness 2 | V3 | NOT MET | MET | Disagree | MET | The `-f` mechanism runs. Its self-reference is a consistency defect, scored in Correctness 4. |
| Structure 3 | V2 | MET | NOT MET | Disagree | MET | `per_correction` is a separate block from findings (v2:144). |
| Structure 4 | V3 | NOT MET | MET | Disagree | MET | The header names the plan and brief paths (v3:6-7), and the IDs are cross-cited. |
| Clarity 4 | V1 | MET | NOT MET | Disagree | NOT MET | "UC-1" (v1:8) and "lc10" are never defined. |
| Clarity 2 | V2 | NOT MET | MET | Disagree | MET | R2-06 lists exact line numbers (v2:130-132). |
| Risk 3 | V2 | MET | NOT MET | Disagree | NOT MET | v2:189 asserts that the qualifications are retained but gives no failure mode or recovery path. |

Disagreements re-evaluated: 8 of 90 paired criterion-variant comparisons (30 criteria × 3 variants), so the two passes agreed on 82 of 90 (91%).
Final verdicts changed from pass 1: 6 (V2 Completeness 2, V3 Correctness 2, V3 Structure 4, V1 Clarity 4, V2 Clarity 2, V2 Risk 3).

## Combined Scoring

| Variant | quant × 0.50 | qual × 0.50 | Final | Debate points won (tiebreaker 1) |
|---------|--------------|-------------|-------|----------------------------------|
| V1 (analyzer) | 0.776 × 0.50 = 0.388 | 0.800 × 0.50 = 0.400 | **0.788** | 5 (S-002, C-007, C-008, C-011, X-003) |
| V2 (qa) | 0.994 × 0.50 = 0.497 | 0.800 × 0.50 = 0.400 | **0.897** | 8 (S-001, C-002, C-003, C-004, C-005, C-006, C-012, X-001) |
| V3 (refactorer) | 0.850 × 0.50 = 0.425 | 0.800 × 0.50 = 0.400 | **0.825** | 5 (C-001, C-010, C-014, C-015, X-002) |

Four points have no winner and are not counted: C-009, C-013, C-016 and A-001.

**Margin**: V2 beats V3 by 0.897 - 0.825 = 0.072, which is above the 0.05 tiebreak threshold. V2 beats V1 by 0.109.
**Tiebreaker applied**: No. For the record, every tiebreaker level would also pick V2: it won 8 debate points against 5 and 5, and it met 5 of 5 correctness criteria against 2 and 3.

## Selected Base: Variant 2 (haiku:qa)

### Selection Rationale

The three cards tie on the qualitative layer at 24/30, so the quantitative layer decides. V2 scores 0.994 there, against 0.850 for V3 and 0.776 for V1. It is the only card that is complete and correct on all of the following:

- It addresses all 19 source requirements (RC 1.000) through a per-correction verifier table, F-1..F-17 (v2:151-167), and the Part 4 and Part 5 rows (v2:169-185).
- Its citations all resolve: DC is 1.000, and calibration re-mapped none of them. V1 has 9 wrong line numbers and V3 has 1.
- It has no internal contradiction (IC 1.000), and it meets all five Correctness criteria.
- In the debate it won the most points (8 of 22). That includes S-001: all three advocates agreed that its verifier table is the coverage instrument that alone surfaced C-002 to C-005.

V2's weakness is Risk Coverage (2/5) and Invariant & Edge Case (3/5). It audits the plan against the brief and does not probe how the plan behaves at runtime. Those gaps are covered by V1's and V3's runtime findings, listed under "Strengths to Incorporate from Non-Base Variants".

### Strengths to Preserve from Base

- The F-1..F-17 per-correction verifier table, together with the Part 4 and Part 5 checks, as the coverage backbone (S-001; v2:144-185).
- R2-05: copy all five residual-risk texts verbatim from source.md:240-244, keeping risk 4's "the spec then blocks a PASS" wording, which spec:300 makes true (C-005, X-001, C-012).
- R2-02: keep plan:144's negative pin, and record it as a Necessary deviation from F-7's "exactly these pins" (C-002, with the action as settled in the debate).
- R2-03: record the brief's F-12 against F-3 quantifier contradiction as a P3 owner note, and keep the independent `only by a /sc:analyze call` pin (C-003).
- R2-04: fix the F-14 literal-absence conflict at plan:45 by rewriting the negative AC with the regex class `r[a]n`, which V1 proposed (C-004).
- R2-06: add rows to the review artifact's coverage matrix for the 17 Verifier lines. This is a P3 review-artifact repair, not a plan change (C-006).

### Strengths to Incorporate from Non-Base Variants

From V3 (opus:refactorer):
- **R3-2 corrected (C-001 and X-002, the merged P2).** Tasks 1, 2, 3 and 6 each get a whole-text AC. The reference text is extracted from `source.md` (lines 231, 232, 233, 223 and 219), not typed by the executor. The ACs:
  - `grep -cF --` prints 1 for each text.
  - For Task 2, `grep -cxF` prints 2.

  This is not a new pin, so it does not conflict with F-7. It is subject to three invariant fixes:
  - INV-001: one path base. State the cwd and use a package-path variable.
  - INV-002: a self-check on each extraction. It must be non-empty, and `grep -cxF` on the plan must print 1.
  - INV-003: no backtick in the Task 2 sed regex; use `.grep`.

  The LOW items INV-006 (`grep -c` counts lines) and INV-014 (do not hard-code `to-do/`) are kept as hardening notes.
- **R3-3:** Task 3 diff-shape AC (`git diff --stat` shows one insertion and one deletion) (C-014).
- **R3-4:** Task 5 gets the `git cat-file -e HEAD:src/superclaude/commands/brainstorm.md` guard. Either narrow the "which shows the pins fail" wording, or check both shared pins against HEAD (C-015).
- **R3-5, narrowed:** the Task 7 logs record `exit=<status>` after each command. The lint-baseline half is dropped per E-2 (C-010).

From V1 (sonnet:analyzer):
- **R1-F2:** owner note. "Required ... only when" states a necessary condition, not an "exactly when" condition. The owner's text stays unchanged (C-007).
- **R1-F3:** a residual-risk line. The refusal clause has no recorded marker (analyze.md:97 is chat-only), so a missed refusal is an inferred false-FAIL path. The checker records `not verifiable` for that call (C-008).
- **R1-F6:** owner note, placed at the top of the owner list. Spec 7.2 step 5 condition 2 should be read as applying to the command under test, not to a nested `/sc:analyze` Skill call inside a `Task` subagent (C-011).
- **X-003:** one residual-risk line that qualifies plan:133's "no known false FAIL" with the two conditional paths above. The live-check sentence itself does not change.
- **S-002:** an explicit `unverified` section stating what the review did not observe, including the session-file encoding.

Dropped by consensus, not to be merged:
- C-009 (R1-F4 and R3-6): void per E-1.
- C-013 (R3-1): void per E-1.
- C-016 (R3-7): source.md:169 and :171 mandate the F-13 sentence.
- R1-F5: moot per E-2.
- R1-F7 and R3-8: superseded by C-012.

Warning carried into Step 4: INV-001, INV-002 and INV-015 are MEDIUM UNADDRESSED. The merged P2 is not runnable as written until the path-anchoring fix and the extraction self-check above are applied.
