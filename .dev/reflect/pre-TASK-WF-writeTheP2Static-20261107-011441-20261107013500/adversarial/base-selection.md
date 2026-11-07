# Base Selection

Variants: V1 = `variant-1-original.md` (sonnet, analyzer), V2 = `variant-2-original.md` (haiku, qa), V3 = `variant-3-original.md` (opus, refactorer).
The variants are reviewer findings documents, not plans, so several metric definitions are adapted below. Each adaptation is stated with its method so the computation can be repeated.

## Quantitative Layer (50%)

### Methods

- **RC (0.30)**: plan-task coverage. The P2 plan has 21 tasks. RC = distinct plan tasks touched by at least one finding (including `verified_ok` checks) / 21. Chosen over the 28-row coverage matrix because `coverage-matrix.yaml` reports `coverage_pct_union 1.0` for the union and does not attribute rows per variant.
  - V1 tasks {5, 10, 13, 14, 15, 16, 17, 18} = 8/21
  - V2 tasks {2, 3, 4, 8, 13, 14, 20, 21} = 8/21
  - V3 tasks {1, 2, 3, 4, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21} = 17/21
- **IC (0.25)**: 1 - 0.5 x (findings the calibrator rated "partly" / total findings), using `../artifacts/calibration.yaml` tier 2. A "partly" rating means the finding contains a claim contradicted by the record.
  - V1: 4 partly (F6, F7, F8, F9) of 10 -> 0.800
  - V2: 0 of 5 -> 1.000
  - V3: 5 partly (F2, F6, F7, F12, F13) of 14 -> 0.821
- **SR (0.15)**: findings with line-level citations and no `[INFERRED]` marker / total findings.
  - V1: 9/10 = 0.900 (F9 cites a table, not a line-level defect)
  - V2: 4/5 = 0.800 (F2 is `[INFERRED]`)
  - V3: 12/14 = 0.857 (F12, F13 are `[INFERRED]`)
- **DC (0.15)**: proxy = calibrator `recommendation_actionability` (whether each fix resolves to a defined plan target). V1 0.75, V2 0.80, V3 0.85.
- **SC (0.15)**: H2 sections / max. V3 has 4 (findings, verified_ok, self_confidence, self_audit); V1 3; V2 3.

### Quantitative Table

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC | 0.30 | 0.381 | 0.381 | 0.810 |
| IC | 0.25 | 0.800 | 1.000 | 0.821 |
| SR | 0.15 | 0.900 | 0.800 | 0.857 |
| DC | 0.15 | 0.750 | 0.800 | 0.850 |
| SC | 0.15 | 0.750 | 0.750 | 1.000 |
| **quant_score** | | **0.674** | **0.717** | **0.854** |

## Qualitative Layer (50%)

Binary rubric, 30 criteria, Claim-Evidence-Verdict. Each row's claim is "criterion is met in Variant X"; the evidence cell cites the variant (finding id) or the debate record; MET = 1, NOT MET = 0.

### Completeness

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Covers all explicit requirements | NOT MET | NOT MET | MET | V1 and V2 touch 8/21 tasks each; V3 touches 17/21 and is the only variant with a nested-call sweep (R3-F1, F4, F5) |
| 2 | Edge cases and failure scenarios | MET | MET | MET | V1 R1-F3 conditional CLI gate; V2 R2-F2 reversal negatives; V3 R3-F1 unflagged nested task |
| 3 | Dependencies and prerequisites | NOT MET | NOT MET | MET | Only V3 checks task dependencies (`verified_ok`: 12->11, 13->5, 16->15, 17->15, 18->4); V1, V2: no evidence found in findings or self_audit |
| 4 | Success/completion criteria | MET | MET | MET | Every finding in all three carries a suggested fix; V1 R1-F7 grep AC, V2 R2-F2 assertions, V3 R3-F11 test |
| 5 | Out of scope stated | MET | NOT MET | NOT MET | V1 self_audit names what it did not check; V2 has no self_audit; V3 self_audit lists method, not exclusions |
| | **Subtotal** | 3 | 2 | 4 | |

### Correctness

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | No factual errors | NOT MET | MET | NOT MET | V1 R1-F6 misreads D-P2-13 (conceded R1); V2 all findings confirmed by calibrator; V3 R3-F13 dirty-folder example is wrong (plan:372, conceded R2) and R3-F3 pin claim (conceded R1) |
| 2 | Approaches feasible | MET | MET | MET | All fixes are plan/test edits within P2 scope |
| 3 | Terminology accurate | NOT MET | MET | MET | V1 uses "none" and "authorized" outside the four-class taxonomy on F7, F8, F9 (conceded R1); V2 and V3 use one class consistently (classification accuracy is scored at C-008) |
| 4 | No internal contradictions | MET | MET | NOT MET | V3 `verified_ok` says "dependency chains correct" while R3-F1 asks for a missing edge (conceded R2, round2-advocate-3 s1) |
| 5 | Claims supported by evidence | MET | MET | MET | All three cite plan, spec or skill lines; V2 R2-F2 `[INFERRED]` carries a stated rationale |
| | **Subtotal** | 3 | 5 | 3 | |

### Structure

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Logical ordering | MET | MET | MET | Findings ordered by id, then confidence/audit |
| 2 | Consistent hierarchy | MET | MET | MET | Flat finding lists, no orphaned subsections |
| 3 | Separation of concerns | MET | MET | MET | Findings separate from self-assessment in all three |
| 4 | Navigation aids | MET | NOT MET | MET | V1 and V3 cross-reference findings to each other and to a self_audit; V2 has no self_audit and no cross-references between findings |
| 5 | Artifact-type conventions | NOT MET | NOT MET | MET | Reviewer output carries findings, verified_ok, self_confidence, self_audit; only V3 has all four (SC metric) |
| | **Subtotal** | 4 | 3 | 5 | |

### Clarity

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Unambiguous language | MET | MET | MET | Findings state a defect and a target; no "as appropriate" phrasing found |
| 2 | Concrete | MET | MET | MET | Each finding names a plan task or line |
| 3 | Section purpose clear | MET | MET | MET | Section titles state purpose |
| 4 | Terms and references self-locating | NOT MET | MET | NOT MET | S-003 won by V2 (95): repo-relative file:line paths; V1 and V3 use short forms that need outside context |
| 5 | Actionable next steps | MET | MET | MET | Suggested fix per finding |
| | **Subtotal** | 4 | 5 | 4 | |

### Risk Coverage

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | At least 3 risks with severity | MET | MET | MET | P1-P3 severity on every finding; V2 has 5, V1 10, V3 14 |
| 2 | Mitigation per risk | MET | MET | MET | Suggested fix per finding |
| 3 | Failure modes and recovery | NOT MET | NOT MET | MET | V3 R3-F1 traces what an unflagged nested `sc:task` does at run time; V1, V2: no run-time failure trace found |
| 4 | External dependency failure | MET | MET | MET | V1 R1-F3 (task-builder CLI mode); V2 R2-F1 (cli-eval); V3 R3-F4, F5 (nested skills) |
| 5 | Validation mechanism | MET | MET | MET | V1 R1-F7 grep AC; V2 R2-F2 relationship negatives; V3 R3-F11 parametrized test |
| | **Subtotal** | 4 | 4 | 5 | |

### Invariant & Edge Case Coverage

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Collection boundaries | NOT MET | MET | MET | V2 R2-F3 and V3 R3-F11 cover all 15 commands vs the pinned subset; V1: no evidence found |
| 2 | State across component boundaries | MET | NOT MET | MET | V1 R1-F3 (gate inside a nested call); V3 R3-F1 (tasklist -> task); V2: no cross-component finding |
| 3 | Guard condition gaps | MET | MET | MET | V1 R1-F2, V2 R2-F1, V3 R3-F2: missing cli-eval safety guard |
| 4 | Count divergence | NOT MET | MET | NOT MET | V2 R2-F3: matrix overstates the pinned count (real count 2, calibration.yaml); V1, V3: no evidence found |
| 5 | Interaction effects | NOT MET | NOT MET | MET | V3 R3-F8: task.md:44 flag-line edit collides with the ADDITIVE check |
| | **Subtotal** | 2 | 3 | 4 | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 2 | 4 |
| Correctness | 3 | 5 | 3 |
| Structure | 4 | 3 | 5 |
| Clarity | 4 | 5 | 4 |
| Risk Coverage | 4 | 4 | 5 |
| Invariant & Edge Case | 2 | 3 | 4 |
| **Total** | **20/30** | **22/30** | **25/30** |
| **qual_score** | **0.667** | **0.733** | **0.833** |

Edge case floor (at least 1/5): V1 2, V2 3, V3 4. All eligible.

## Position-Bias Mitigation

Pass 1 order V1, V2, V3; Pass 2 order V3, V2, V1. Both passes were run by this orchestrator in one context, which limits their independence.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Clarity-4 | V2 | MET | NOT MET | No | MET (repo-relative paths confirmed by S-003 at 95) |
| Correctness-4 | V3 | MET | NOT MET | No | NOT MET (`verified_ok` "correct" vs R3-F1 missing edge, conceded) |
| Risk-5 | V1 | NOT MET | MET | No | MET (R1-F7 grep AC is a validation mechanism) |
| All other 87 verdicts | all | agree | agree | Yes | as Pass 1 |

- Disagreements re-evaluated: 3
- Final verdicts changed from Pass 1: 2 (V3 Correctness-4, V1 Risk-5)

## Combined Scoring

| Variant | Quant x 0.50 | Qual x 0.50 | Final | Debate Tiebreaker |
|---|---|---|---|---|
| V1 | 0.337 | 0.333 | **0.671** | 0 direct wins |
| V2 | 0.358 | 0.367 | **0.725** | 3 direct wins |
| V3 | 0.427 | 0.417 | **0.844** | 2 direct wins, leads 4 of 11 merges |

- Margin (V3 - V2): 0.119
- Tiebreaker applied: No (margin above 0.05)

## Selected Base: Variant 3 (opus, refactorer)

### Selection Rationale

V3 leads on the two heaviest drivers: coverage (17/21 plan tasks against 8/21) and structure (the only variant with all four reviewer sections). Its nested-call sweep is the only method in the record that keeps finding defects: R3-F1 in Round 1 and the troubleshoot `--diagnosability-handoff` finding in Round 2. All three advocates chose V3 as base in Round 2. Its weaknesses are correctness-level (an overstated harm, one wrong example, an over-broad `verified_ok`), and every one was conceded and is fixable in place. V2 wins on correctness and evidence form, which the merge imports.

### Strengths to Preserve from Base

- The nested-call sweep and its findings R3-F1 (P1), R3-F4, R3-F5.
- R3-F11: one parametrized WC-4 test over all 15 commands.
- R3-F8 (task.md:44 vs ADDITIVE), R3-F10 (format baseline), R3-F14, R3-F9 (as an observation).
- `verified_ok` checks, bounded to "listed edges exist".
- The four-section reviewer structure.

### Strengths to Incorporate from Non-Base Variants

- V2: repo-relative file:line evidence form (S-003); cli-eval P1 and the missing safety-block (R2-F1, X-001); relationship-level negatives (R2-F2, C-004); full "left out (WC-4)" scope (R2-F3, C-003); Task 21 path list at P3 (R2-F4, C-005); matrix-gap note (R2-F5).
- V1: task-builder CLI-mode gate, corrected (R1-F3, U-004); spec-panel socratic (R1-F4, U-005); `refs/return-contract.md` on C-002 (R1-F1); per-gate phrase inventory (R1-F10); narrowed R1-F6 and R1-F7; R1-F8 wording beside R3-F8.
