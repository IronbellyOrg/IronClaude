# Base Selection Report

## Quantitative Scoring (50% weight)

Observed read-only UV computation is preserved in `./quantitative-scores.json`. Formula: 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC.

| Metric | Weight | V1 | V2 | V3 |
|---|---:|---:|---:|---:|
| Requirement phrase overlap (RC) | 0.30 | 1/12 = 0.083333 | 1/12 = 0.083333 | 2/12 = 0.166667 |
| Explicit internal verdict consistency (IC) | 0.25 | 1.0 | 1.0 | 1.0 |
| Concrete/vague indicator ratio (SR) | 0.15 | 7/(7+0) = 1.0 | 4/(4+0) = 1.0 | 12/(12+0) = 1.0 |
| Local finding-id reference completion (DC) | 0.15 | 3/3 = 1.0 | 0 unresolved, 1.0 convention | 4/4 = 1.0 |
| H2 section coverage (SC) | 0.15 | 4/4 = 1.0 | 4/4 = 1.0 | 4/4 = 1.0 |
| Quant score | | 0.725 | 0.725 | 0.750 |

Deterministic text heuristics are intentionally disclosed: RC searches normalized exact 3-word source-quote fragments (whole phrase when shorter), IC detects explicit opposing verdict tokens within the verdict section, SR uses fixed concrete/vague regex over non-heading substantive lines, DC resolves local F identifiers, SC counts H2 sections. These metrics measure card presentation/overlap, not semantic source coverage or correctness. No lack of detected contradiction is claimed to prove full logical consistency. Semantic conclusions depend on real-source debate and the independent evidence gate.

## Qualitative Scoring (50% weight)

### Completeness

Neutral coordinator's 30-criterion CEV (claim/evidence/verdict) review follows. M = MET, N = NOT MET. Scores concern the original cards, not product correctness. Each row states the criterion followed by each card's evidence and verdict.

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| All explicit requirements | N: advocate conceded omitted stand-alone rule (debate:13) | N: advocate conceded governing omission (debate:44) | M: Scope covers assigned slice plus template/qa boundary |
| Edge/failure cases | M: F1 wrapped negative guard | M: Scope excludes collection errors, preserves parser guard | M: F3 capture hyphen splits |
| Dependencies/prerequisites | M: Scope red/green order | M: Scope test suites exist | M: Scope five files/coverage dependency checked |
| Success criteria | M: Verdict zero blockers stated | M: Verdict no contradictory acceptance state | M: Verdict correction subject to re-review |
| Out of scope | M: Scope non-exhaustive, F3 excluded placeholder | M: Verdict no implementation approval | M: Verdict authorizes no edit |

Subtotals: V1 4/5; V2 4/5; V3 5/5.

### Correctness

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| No factual errors/invented claims | M: test-pin claim corroborated in debate:30; omission counted in completeness only | M: intact captures corroborated debate:17; omission counted once | M: F1 governing and candidate citations verified in debate |
| Feasible approach | M: F1 remove-whitespace remedy | N: Scope says Task 4 final states coherent; debate refuted isolated comparison feasibility | M: F1 inline input remedy feasible, not proven exhaustive |
| Terminology consistent | M: Label/Grade fields | M: label/blocking vocabulary | M: Label/Grade/Category fields |
| No internal contradictions | M: PASS aligns with Medium only | M: zero findings aligns with PASS | M: F1/F2 grade distinction upheld Round 2 |
| Evidence-supported claims | M: F1 width/guard mechanism | M: Scope historical rows and candidate final review | M: F1 contract and F3 capture citations |

Subtotals: V1 5/5; V2 4/5; V3 5/5. Internal consistency scoring does not establish completeness.

### Structure

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Logical order | M: Scope/Findings/Verdict/Calibration | M: same four sections | M: same four sections |
| Hierarchy | M: H2/H3 findings | M: flat H2 | M: H2/H3 findings |
| Separation | M: one finding per H3 | M: separate scope paragraphs and Findings | M: one finding per H3 with Category |
| Navigation | M: calibration path and F ids | M: calibration path | M: calibration and coverage receipt refs |
| Card conventions | M: Location/Claim/Consequence/Grade | M: checked scope supports valid zero-finding form | M: Location/Evidence/Rule/Action/Remedy |

Subtotals: all 5/5.

### Clarity

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Unambiguous | M: zero vague lines, F1 names concrete risk | M: zero vague lines | M: zero vague lines, directives explicit |
| Concrete | M: F1 exact split spelling | M: Scope exact file citations | M: F1 commands and paths |
| Section purpose | M: headed sections | M: headed sections | M: headed sections |
| Terms defined first use | N: JobSpec/CliRunner/C undefined | N: CliRunner/AC/C undefined | N: INF/AC/C undefined |
| Next step | M: F1 whitespace follow-up | N: no next action, only no approval | M: F1 narrow remedy |

Subtotals: V1 4/5; V2 3/5; V3 4/5.

### Risk Coverage

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Three risks with probability/impact | N: only one risk | N: no risks | N: consequences but no probabilities |
| Mitigation each | M: F1 remedy, F2/F3 rejected | N: no risk mitigation | M: F1-F3 remedies, F4 guidance |
| Failure/recovery | M: Verdict honest failure reporting | M: Scope no invented passes or missing-proof closure | M: F1 affected action, Verdict independent re-review |
| External dependency failure | M: Verdict coverage-tool availability | N: none named | N: Scope checks dependency but gives no failure case |
| Validation | M: F1 real public-output backstop | M: Scope persisted final review | M: Verdict re-review |

Subtotals: V1 4/5; V2 2/5; V3 3/5.

### Invariant and Edge Case Coverage

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| Collection boundaries | M: F1 width 100, INV-004 line boundary classification | N: declined wrapping | M: F3 capture line-boundary splits |
| Cross-component state | N: no cross-boundary state | M: Scope intermediate/final states analysed, wrong conclusion counted under correctness | M: F1 isolated input versus sibling-task baselines |
| Guard gaps | M: F1 weak negative guard | N: no gap identified | M: F3 weak negative guard |
| Count divergence | N: none | M: Scope literal 6/12 versus substantive coverage | N: six assigned is not divergence |
| Interaction effects | M: F1 negative/positive assertions and public backstop | N: none | M: F3 current red still fails positive checks |

Subtotals: V1 3/5; V2 2/5; V3 4/5. All meet the 1/5 eligibility floor. Total qualitative scores: V1 25/30; V2 20/30; V3 26/30.

## Position-Bias Mitigation

Neutral coordinator evaluated forward V1,V2,V3 and reverse V3,V2,V1. Eight disagreements were re-evaluated against both evidence sets:

| Criterion/card | Forward | Reverse | Final, reason |
|---|---|---|---|
| Completeness 1/V3 | M | N | M, assigned slice and governing boundary fully covered |
| Correctness 1/V1 | M | N | M, omission counted under completeness; no false citation shown |
| Correctness 1/V2 | M | N | M, same counting rule |
| Correctness 2/V2 | M | N | N, debate refuted Task 4 isolated comparison feasibility |
| Risk 4/V3 | M | N | N, dependency failure case absent |
| Invariant 1/V1 | N | M | M, independent INV-004 line-boundary classification |
| Invariant 1/V3 | N | M | M, same classification |
| Invariant 2/V2 | N | M | M, state was analysed, wrong result counted in correctness |

Eight disagreements resolved, four results changed from forward pass. These are evidence-backed binary card scores, not fresh product observations.

## Combined Scoring

| Card | Quant x 0.5 | Qual x 0.5 | Combined |
|---|---:|---:|---:|
| V1 | 0.3625 | 0.416667 | 0.779167 |
| V2 | 0.3625 | 0.333333 | 0.695833 |
| V3 | 0.375 | 0.433333 | 0.808333 |

Top margin 0.029166, below 0.05. Debate tiebreaker: V3 won S-001 (2/3, V1 neutral), S-003, S-004, C-001, C-003, X-001 and X-003; V2 won C-004. Shared points: C-002/X-002 (V1/V3), S-002/C-005 (all). Thus V3 wins at tiebreak level 1; correctness/input-order levels not needed. Scoring is coordinator-owned; main only persists arithmetic and receipts.

## Selected Base

Selected V3, `variant-3-original.md` (requested opus/refactorer): strongest combined score and seven outright debate wins. Retain its one baseline-comparability blocker, two Medium findings and receipt-wording Note. Integrate V1 mechanism/exclusion and V2 full-source/history details per refactor-plan.md. All taxonomy levels covered, convergence 11/12 and no HIGH unaddressed invariant after explicit six-category clarification. Four Medium probe warnings limit remedy sufficiency but do not block merge or authorize a fix pass. The merged card is not independently recalibrated; 0.81 remains original V3 calibration only. Final REPORT citation validation still required.
