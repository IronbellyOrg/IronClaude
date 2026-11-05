# Base Selection Report

- Generated: 2026-11-04T18:48:52Z
- Inputs: `variant-{1,2,3}-original.md`, `debate-transcript.md`, `diff-analysis.md`, `../artifacts/calibration-t2.yaml`
- Variants: A = reviewer 1 (analyzer, sonnet); B = reviewer 2 (qa, glm-5.3 on the haiku alias); C = reviewer 3 (refactorer, opus)
- Artifact type: YAML reviewer cards. No variant has H2 headings, so the section metric falls back to top-level card keys (see SC below).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (analyzer, sonnet) | Variant B (qa, glm-5.3) | Variant C (refactorer, opus) |
|--------|--------|-------------------|-------------------|-----|
| requirement_coverage | 0.30 | 0.727 (16/22: CF-01..CF-16) | 0.455 (10/22: CF-01..04, 08, 11..15) | 0.591 (13/22: CF-01..06, 15..21) |
| internal_consistency | 0.25 | 0.909 (1 contradiction / 11 claims: X-005, A-1/A-2 Medium vs A-3/A-4 Low for one defect type) | 0.875 (1 / 8: Q-2..Q-4 Medium vs Q-8 Low for one defect type) | 1.000 (0 / 11) |
| specificity_ratio | 0.15 | 1.000 (21 concrete / 21; 0 vague; 2 of 23 statements carry no indicator and are excluded) | 1.000 (17 / 17; 0 vague) | 1.000 (23 / 23; 0 vague) |
| dependency_completeness | 0.15 | 1.000 (6 / 6 internal finding references resolve, e.g. A-10 "per A-5") | 1.000 (0 internal references; vacuously complete) | 1.000 (1 / 1: "4a/4b" in the summary resolves to F-1) |
| section_coverage | 0.15 | 1.000 (7 / 7 top-level keys) | 1.000 (7 / 7) | 1.000 (7 / 7) |
| **quant_score** | | **0.895** | **0.805** | **0.877** |

Computation notes:
- RC: the source (a reflect review task) has no FR-/NFR- IDs, so the protocol's topic-matching edge case applies. The topic set is the 22 canonical findings in `diff-analysis.md`. CF-22 is matched by no card.
- IC: scorable claims are the findings. The only intra-card contradiction found is the X-005 severity split. C's F-10 claim is partly false (X-004), but that is a factual error scored under Correctness, not a self-contradiction.
- SR: statements are each finding's `claim` and `recommendation` plus the `summary` (A 23, B 17, C 23). The vague list is applied literally: "appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practice" and "industry standard". Hedges with "optionally" (A 1, C 2) are not on that list; they count against Clarity CL1 instead.
- DC: evidence citations into the plan, the spec and the repo are external references and are excluded. B's wrong citation (S:1392 for S:1408) is scored under CR1.
- quant = 0.30·RC + 0.25·IC + 0.15·SR + 0.15·DC + 0.15·SC. A = 0.2182 + 0.2273 + 0.45 = 0.8955. B = 0.1364 + 0.2188 + 0.45 = 0.8051. C = 0.1773 + 0.2500 + 0.45 = 0.8773.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent evaluator agents ran the rubric. Pass 1 went in order A, B, C and Pass 2 in reverse order C, B, A. Both saw only the three variants plus the fact-check sources (`diff-analysis.md`, `calibration-t2.yaml`), not the debate. The verdicts below are final: agreed verdicts, or the re-evaluated verdict where the passes disagreed (marked †).

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | Summary: coverage, graph (A-1..A-5), ACs (A-6..A-8), class on every finding | MET | Summary: "Every section 12 test is assigned to a task"; edges, ACs, classes | MET | F-1..F-11 cover order, edges, AC observability (F-8); class on every finding |
| Addresses edge cases/failures | MET | A-1: "Tasks 11, 12 and 13 would also edit that one file concurrently" | MET | Q-5: "fails without an identity, breaking F9, F10, X1, X3" | MET | F-4: "graph-ordered or parallel execution hits a missing file or conflicting appends" |
| Includes dependencies/prerequisites | MET | A-2: Task 15 needs `parse_resolution_record` from Task 4 | MET | Q-2..Q-4, Q-8 give the missing Depends-on lines | MET | F-2..F-5 name the missing edges |
| Defines success/completion criteria | MET | A-6: AC on `git diff --cached --name-only`; A-1 "Verify every editor..." | MET | Q-1: "verify both pass in ./artifacts/t20-checks.log" | MET | "Verify:" clause on every recommendation |
| Specifies out-of-scope items | MET | A-11: "No invented functional requirement... No change." | MET | Summary: "no regression-class contradiction" | MET | F-11: "No change required"; F-10: "Keep Task 5's edge" |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| No factual errors | MET | Calibrator: A-1..A-4, A-6..A-8 true; grounding 0.92; no citation defect (C-011) | NOT MET | Q-1 cites `source.md:1392`; the make-test step is `:1408` (calibration-t2) | NOT MET | F-10 calls Task 5/8 → Task 4 "stricter than spec"; both are spec-required (X-004) |
| Feasible approaches | MET | A-2: one-line Depends-on edit | MET | Q-5: fixed `GIT_AUTHOR_*` / `GIT_COMMITTER_*` variables | MET | F-1 4a/4b split with concrete dependencies; F-4 chain |
| Terminology consistent/accurate | NOT MET | A-10 labels task size "drift" (A withdrew it; CF-07 became advisory); A-8d "drift" became a spec defect | MET | `authorized` for the documented override (Q-1), `drift` elsewhere; no label disputed by the calibrator | NOT MET | F-9 labelled `necessary`; calibrator: "drift, not necessary" |
| No internal contradictions | NOT MET | X-005: A-1/A-2 Medium vs A-3/A-4 Low for one defect type, no rule | NOT MET | Q-2..Q-4 Medium vs Q-8 Low for one defect type, no rule | MET | All five missing-edge findings Medium |
| Claims supported by evidence | MET | Every finding cites file:line (A-6: P:191, P:27, S:1429) | MET | Q-1 cites `commands.py:99` and the test file `:18` | MET | F-8 cites `poll-ci-checks.sh:30` (confirmed, U-005) |
| **Subtotal** | **3/5** | | **3/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Logical ordering | MET | Graph (A-1..A-5), then ACs, then authorized, then sizing | MET † | Severity-descending: Medium Q-1..Q-5, then Low Q-6..Q-8 | MET | Medium F-1..F-6, then Low F-7..F-11 |
| Consistent hierarchy | MET | Uniform finding fields; no orphans | MET | Uniform fields | MET | Uniform fields |
| Separation of concerns | NOT MET | A-8 bundles four defects (a)-(d); A-6 and A-10 bundle two each | NOT MET | Q-5 and Q-6 bundle two defects each | NOT MET | F-1 and F-5 bundle two defects each |
| Navigation aids | MET | A-10 "resume per A-5"; summary cites "A-1 to A-5" | MET | IDs Q-1..Q-8 plus file:line references | MET | IDs F-1..F-11, repo-relative paths, Verify clauses |
| Artifact-type conventions | MET | All card fields present | MET | All card fields present | MET | All card fields present |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | NOT MET | A-1: "optionally chain 11 -> 12 -> 13" | MET | No "optionally"/"might"/"should consider" hedges | NOT MET | F-10 "optionally drop..."; F-11 "optionally tighten..." |
| Concrete actions | MET | A-6: `git add -- src tests CHANGELOG.md` | MET | Q-6: "use loop-guard.md:86-103" | MET | F-9 gives exact insertion anchors |
| One-sentence summarizable | NOT MET | A-8 carries four unrelated defects | MET | Q-6: "Task 2 drops the 6.5 clause and miscites the range" | MET | F-7: "Tasks 11 and 12 run only test_conflict_scripts.py" |
| Terms defined on first use | NOT MET | "VG-2", "AC", "QA" undefined | NOT MET | "TL", "INF rows", "unmapped-union" undefined | NOT MET | "TL", "E5", "E12", "X1", "C1-C4" undefined |
| Actionable next steps | MET | Every finding has a recommendation; A-11 "No change." | MET | Every recommendation names the insertion | MET | Exact edit plus Verify step |
| **Subtotal** | **2/5** | | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| ≥3 risks with probability and impact | MET | A-6 "cannot be observed", A-7 "no command that can fail", A-8 "fails"; each with a severity | MET † | Q-1 test left "outside every task's verification run", Q-5 "fails", Q-7 "vacuously true"; each with a severity | MET † | F-6 test left out, F-7 scan not run, F-4 states its triggering condition ("graph-ordered or parallel execution"); each with a severity |
| Mitigation per risk | MET | Recommendation on every finding | MET | Recommendation on every finding | MET | Recommendation on every finding |
| Failure modes and recovery | MET | A-8b commit fails; recovery: fixed identity | MET | Q-5 F9/F10/X1/X3 break; recovery: fixed identity | MET | F-4 missing file / conflicting appends; recovery: chain |
| External dependencies | MET | A-8 git under `GIT_CONFIG_GLOBAL=/dev/null`; A-6 `git ls-files` behaviour | MET | Q-5 git identity; merge-tree capability | MET | F-8 script exit behaviour; F-4 executor ordering |
| Monitoring/validation mechanism | MET | A-7: grep checks saved under `./artifacts/` | MET | Q-4: header-match grep | MET | F-6: "Verify: t9-tests.log and t20-checks.log" |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Collection boundaries | NOT MET † | A-6 implies only that an unstaged file has no index entry; it does not name an empty-collection case | MET † | Q-7: the "no staged `.claude/` path" check over an empty staged set is "vacuously true" | NOT MET | No empty/single/max case |
| State interactions across components | MET | A-5: hand-built state vs `RunLog.rebuild_state()` | MET | Q-5: `GIT_CONFIG_GLOBAL` environment state reaches `git commit` identity | MET | F-1: state dicts "can drift from what rebuild_state actually returns" |
| Guard condition gaps | MET | A-8a: missing capability skip | MET | Q-5: missing merge-tree capability skip | MET | F-8: missing `--pr` guard lets C4 pass for the wrong reason |
| Count divergence | MET | A-8d: `:86-99` vs `:103` | MET | Q-6: `:86-99` vs `:103` | MET | F-11: "at most 15 lines" vs spec "net +15" |
| Interaction effects | MET | A-1: concurrent edits to one test file | MET | Q-1: reflect CLI coupled to the package `__init__` | MET | F-4: sibling appends to one test file |
| **Subtotal** | **4/5** | | **5/5** | | **4/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 3/5 | 3/5 | 3/5 |
| Structure | 4/5 | 4/5 | 4/5 |
| Clarity | 2/5 | 4/5 | 3/5 |
| Risk Coverage | 5/5 | 5/5 | 5/5 |
| Invariant & Edge Case | 4/5 | 5/5 | 4/5 |
| **qual_score** | **23/30 = 0.767** | **26/30 = 0.867** | **24/30 = 0.800** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case | Floor (≥1/5) | Eligible as base |
|---|---|---|---|
| A | 4/5 | Met | Yes |
| B | 5/5 | Met | Yes |
| C | 4/5 | Met | Yes |

### Debate-informed check (verdicts not changed)

The passes were blind to the debate by design. Two debate outcomes bear on their evidence:
1. **A, Correctness 3.** Pass evidence cited the calibrator's "Refinement not Drift" ruling on A-5. Debate X-001 unanimously held A-5 to be drift, so that particular ground is overturned. The verdict still stands as NOT MET on other grounds: A withdrew the A-10b "drift" label, and A-8d was reclassified as a spec defect.
2. **B, Correctness 3 (MET in both passes).** Debate C-008 reclassified Q-6's line-range "drift" as a spec defect, and B conceded this in R2. The agreed verdict is kept, per the protocol. Sensitivity: scoring it NOT MET gives B 25/30 (qual 0.833, final 0.819). The selection is unchanged (see Combined Scoring).

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 (A, B, C) | Pass 2 (C, B, A) | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| IE1 collection boundaries | A | NOT MET | MET | DISAGREE | NOT MET: A-6 never names an empty-collection case; Pass 2 itself flagged its MET as "only implies" |
| ST1 logical ordering | B | NOT MET | MET | DISAGREE | MET: severity-descending order is the ordering both passes credited to C |
| RK1 ≥3 risks with probability/impact | B | MET | NOT MET | DISAGREE | MET: Q-1, Q-5, Q-7 each state a certain outcome with a severity, the same standard both passes applied to A |
| IE1 collection boundaries | B | NOT MET | MET | DISAGREE | MET: Q-7 states that a check over an empty staged set is vacuously true |
| RK1 ≥3 risks with probability/impact | C | MET | NOT MET | DISAGREE | MET: F-6, F-7 certain omissions, and F-4 states its triggering condition explicitly; same standard as A and B |

Disagreements re-evaluated: 5 of 90 criterion-variant pairs.
Final verdicts changed: 2 against Pass 1 (B ST1, B IE1) and 3 against Pass 2 (A IE1, B RK1, C RK1).
Pass totals before re-evaluation: Pass 1 A 23, B 24, C 24; Pass 2 C 23, B 25, A 24.
Re-evaluation note: the orchestrator did the re-evaluation using both passes' evidence. It applied one standard per criterion across all three cards. The orchestrator had debate context, so the re-evaluation step is not blind.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (analyzer, sonnet) | 0.448 | 0.383 | **0.831** | 8 of 27 points won (29.6%) |
| B (qa, glm-5.3) | 0.403 | 0.433 | **0.836** | 2 of 27 (7.4%) |
| C (refactorer, opus) | 0.439 | 0.400 | **0.839** | 11 of 27 (40.7%) |

Exact values: A 0.83106, B 0.83589, C 0.83864.

**Margin**: C over B = 0.0027 (0.27 points), which is below the 0.05 threshold. All three variants lie within 0.0076 of each other.
**Tiebreaker applied**: Yes, Level 1 (debate performance). C won 11 diff points and B won 2, a gap far outside 5%, so Level 2 and Level 3 were not needed. Against A (8 points, 29.6%), C also wins at Level 1.
**Sensitivity**: with the debate-informed B CR3 = NOT MET, the order is C 0.839, A 0.831, B 0.819. The top two are then C and A, and Level 1 still selects C (11 vs 8). The selection depends on the tiebreaker, not on the combined score, so these three cards are close to interchangeable on the rubric. C is chosen because its positions won the most debate points.

Context, not a scoring input: the calibrated confidences are A 0.82, B 0.78 and C 0.82. C's self-report matches its calibration exactly (C-012).

## Selected Base: Variant C (refactorer, opus)

### Selection Rationale
- The combined scores are a statistical tie (spread 0.0076), so the protocol's Level 1 tiebreaker decides.
- C's positions won 11 of 27 diff points, against A 8 and B 2. That includes both L3 points that carry the structural fixes: C-001, the chain on the shared test file, and C-004, the 4a/4b split. For C-004, C's own F-1 placement, "between Task 7 and Task 8", is the document position that R-INV made load-bearing (INV-005).
- C is the only card with no internal contradiction (IC 1.000; CR4 MET). It already applies one severity scale to every missing edge, which the debate adopted (X-005, S-002).
- C is weaker than A on acceptance-criteria coverage (CF-07..CF-14 are absent) and weaker than B on clarity and on the edge-case dimension. Those gaps are content additions, and they are planned in `refactor-plan.md`.

### Strengths to Preserve from Base
1. A "Verify:" clause on every recommendation (CO4), carried onto every merged finding.
2. Repo-relative evidence paths (S-005) and one severity scale for every missing edge (X-005).
3. F-4 chain 11 → 12 → 13 (CF-01), F-2 Task 19 → Task 13 (CF-17), F-7 force-push scan (CF-18), F-8 `--pr` guard (CF-19) and F-9 placement anchors (CF-20).
4. F-1's 4a/4b split and its placement of 4b between Task 7 and Task 8 (CF-05, CF-06), amended by R-INV.
5. Accurate self-calibration (0.82 = 0.82).

### Strengths to Incorporate from Non-Base Variants
1. From Variant A: A-6b staging step (CF-08); A-6a `test -x` (CF-09); A-7 grep checks (CF-10); A-8c/A-8d with the spec-defect reclassification (CF-13, CF-14); A-10b as advisory (CF-07); A-9's Low severity and the "VG-2 not run" log line (CF-15); A's Round 2 severity rule; A's 4b-on-Task-5 edge (R2).
2. From Variant B: Q-5 split into CF-11 and CF-12 with the named breakage of F9, F10, X1 and X3; Q-4 header-match grep (CF-03); Q-7 vacuity rationale (CF-08); Q-6 S:728 clause text (CF-13); B's Task 8 → 4b re-point (R2).
3. From the consensus and calibrators, no card: CF-22 (Task 10 → 4a); the A-002 method fix; R-INV in full; INV-007 (Task 3 → Task 1); and the INV-006 regrade with its executor qualifier.
