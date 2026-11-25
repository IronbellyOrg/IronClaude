# Base Selection (Step 3)

Method note: both position papers are argument documents, not plans, so the "source requirements" of the quantitative layer are the brief's required items per question (claim, mechanism, 5 to 10 cited facts, cost, risk, what it gets right) for each of OD-7, OD-8, OD-9. The orchestrator scored both layers itself, evaluating in input order (OURS, CLAY) and then in reverse order (CLAY, OURS). One evaluator ran both passes, so the dual pass reduces order effects but is not an independent second judge. This limit is recorded; the margin below is large enough that it does not change the base.

## Quantitative Scoring (50% weight)
| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | 18 of 18 brief items present in each (6 items x 3 ODs) |
| Internal consistency (IC) | 0.25 | 0.95 | 0.97 | V1: 2 contradictions (X-001 WC:137 scope, X-002 "not possible") in about 40 scorable claims; V2: 1 (X-003 narrow guard versus own risks) in about 32 |
| Specificity ratio (SR) | 0.15 | 0.93 | 0.90 | Concrete (file:line, numbers, named rows) against vague wording; V2 uses "narrowly" and "later costs a migration" without a figure |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | Internal references resolve; external verdict names (D07, D15) excluded |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 5 H2 sections each |
| **quant_score** | | **0.977** | **0.978** | .30 + .2375 + .1395 + .15 + .15 and .30 + .2425 + .135 + .15 + .15 |

## Qualitative Scoring (50% weight) - Additive Binary Rubric (30 criteria)
CEV format kept short: each cell is MET or NOT MET with the evidence or the reason. MET without evidence defaults to NOT MET.

### Completeness
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Covers all explicit requirements | MET (all three ODs, each with answer, mechanism, facts) | MET (same) |
| 2 | Edge cases and failure scenarios | MET (stale lease; nudge undoes interrupt) | MET (risk lists per OD) |
| 3 | Dependencies and prerequisites | MET (contract exception, U40, U8, marker rename D08) | MET (C25 to C29, suppression rule) |
| 4 | Success or completion criteria | MET (enable after U8 capture; trigger "second host or user polls") | NOT MET (no completion condition for the "yes" builds) |
| 5 | Explicit out of scope | MET ("closed unless the owner asks"; no report line until asked) | NOT MET |
Subtotal V1 5, V2 3.

### Correctness
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | No factual errors | NOT MET (WC:137 scope overstated; checked at `WORKER-CONTRACT.md:131-138`) | MET (cited lines re-checked: D:113, D:137, D:749, D:873, `claim.md:43`) |
| 2 | Technical approach feasible with stated constraints | MET (reserve forms are buildable) | NOT MET (N7 landing unconfirmed, U40 D:1298; nudge undoes it, WC:164) |
| 3 | Terminology consistent | MET | MET |
| 4 | No internal contradictions | MET (X-002 is a wording overreach, not a contradiction of its own facts) | NOT MET (X-003: "narrow guard" against its own concessions) |
| 5 | Claims supported by evidence | MET | MET (migration cost marked as not measured by the advocate; paper labels "honest limit") |
Subtotal V1 4, V2 3.

### Structure
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Logical ordering | MET | MET |
| 2 | Consistent depth | MET | MET |
| 3 | Separation of concerns | MET (one block per OD) | MET |
| 4 | Navigation aids | MET (headed blocks, D:nnn cross-references) | MET |
| 5 | Follows artifact conventions (brief: claim, mechanism, facts, cost, risk, gets right) | MET | MET |
Subtotal V1 5, V2 5.

### Clarity
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Unambiguous language | MET | MET |
| 2 | Concrete rather than abstract | MET | MET |
| 3 | Each section has a clear purpose | MET | MET |
| 4 | Terms defined on first use | MET (Terms paragraph: PR 686, D:nnn, U40, U8, D15) | NOT MET ("D15's N6 change" and "answer_ref" used without definition) |
| 5 | Actionable next steps | MET (reopen conditions per OD) | NOT MET (summary names benefits, no next step) |
Subtotal V1 5, V2 3.

### Risk Coverage
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | At least 3 risks with probability and impact | MET ("Risk of No" per OD with low, not observed, none to safety) | NOT MET (risks named, no probability or impact) |
| 2 | Mitigation for each risk | MET (triggers, build conditions, off switch) | NOT MET (stale lease has no mitigation) |
| 3 | Failure modes and recovery | MET (wedged issue; undone interrupt) | NOT MET (modes named, no recovery) |
| 4 | External dependencies and their failure | MET (Orca receipt U40; GitHub search replies U8) | MET (same) |
| 5 | Monitoring or validation mechanism | MET (U8 live capture, U40 check) | NOT MET |
Subtotal V1 5, V2 1.

### Invariant and Edge Case Coverage
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Collection boundaries (empty, single, maximum) | NOT MET (no mention of the 0 to 50 entry limit, D:184) | NOT MET |
| 2 | State variable interactions across components | MET (host-local state file against cross-host claim; nudge ladder against interrupt) | MET (same facts) |
| 3 | Guard condition gaps | MET (grant-bound write, `E-NO-GRANT`; escalation refused sends nothing) | MET (escalation-first guard) |
| 4 | Count divergence | NOT MET | NOT MET |
| 5 | Interaction effects | MET (interrupt with nudge; lease with grant) | MET |
Subtotal V1 3, V2 3.

### Qualitative Summary
| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 5 | 3 |
| Correctness | 4 | 3 |
| Structure | 5 | 5 |
| Clarity | 5 | 3 |
| Risk Coverage | 5 | 1 |
| Invariant and Edge Case | 3 | 3 |
| **Total / 30** | **27** | **18** |
| **qual_score** | **0.900** | **0.600** |

### Edge Case Floor Check
Both variants score 3 of 5 (at or above 1 of 5): both eligible as base.

## Position-Bias Mitigation
Pass 1 (V1 then V2) and pass 2 (V2 then V1) produced the same verdict on 29 of 30 criteria for both variants. The one disagreement was Correctness 5 for V2 (migration-cost claim): pass 1 MET, pass 2 NOT MET because the advocate marked the cost "UNVERIFIED". Re-evaluation with both evidence lines: MET, because the paper itself carries the "not measured" label in its risk text and the criterion asks whether claims have support within the document. Disagreements found: 1. Verdicts changed: 0 of the final verdicts from pass 1.

## Combined Scoring
| Variant | 0.50 x quant | 0.50 x qual | Final |
|---|---|---|---|
| 1 (OURS) | 0.4885 | 0.4500 | **0.9385** |
| 2 (CLAY) | 0.4890 | 0.3000 | **0.7890** |

Margin: 15.0 points (15.9 percent of the leader). Tiebreaker: not applied (margin above 5 percent).

Caution recorded: the quantitative layer is a tie (0.977 against 0.978). The whole margin comes from the qualitative layer, mostly Risk Coverage (5 against 1) and Clarity. That rubric rewards a paper that states probabilities, mitigations and next steps; it does not measure which answer is right. The answer is decided by the debate result (15 of 17 points converged on the owner's line, with CLAY's advocate agreeing on all three final answers), and the two agree.

## Selected Base: Variant 1 (OURS, the owner's line)
**Selection rationale.** Highest combined score (0.9385 against 0.7890), and it is the line the debate converged on: both advocates give No (reserve) for OD-7, OD-8 and OD-9, on the same three reasons per question: OD-7 no incident, no landing receipt (U40, D:1298) and a nudge that undoes it (WC:164); OD-8 trigger absent (D:113, D07) and a stale-lease defect; OD-9 unverified search replies (U8, D:137) and most streams duplicate `involves` (`collect.py:200-209`). The owner's weighting rule (OURS wins unless CLAY shows a clear, evidenced benefit; a tie goes to OURS) gives the same result.

**Strengths to preserve from the base.**
- Reserved-design form with an explicit trigger and explicit build conditions per question.
- Per-OD "Cost of No / Risk of No".
- The facts U-001 (`collect.py:200-210`), U-002 (ruling 25 is among Clay's rulings 23 to 35, D:1170, D:1197).

**Strengths to incorporate from the non-base variant.**
1. X-001 correction: line 137 of `WORKER-CONTRACT.md` is scoped to answer typing (`:131-138`); the correct OD-7 fact is "no contract text authorizes N7" (D:749, D:764 add the exception themselves).
2. U-006 escalation-first ordering rule stays as a rule of `escalate`, without the interrupt option (hybrid on OD-7).
3. U-004 build conditions for a later N7: contract exception written like S6's, the C25 to C29 changes (D:925-928), a nudge-suppression rule, a check whether `--interrupt` has its own receipt (U40 covers text sends).
4. U-005 reserve the persisted state step names (`plan_rechecked`, `lease_posted`, `claim_started`, `claim_done`, D:547) and the renamed marker so a later build needs no migration.
5. X-002 wording change: "trigger not present" instead of "not possible"; record that K13 (D:1235) rates the double-claim risk medium/medium and names the lease as its mitigation.
6. C-007 hybrid: if the info streams are ever enabled, enable `could_assign` alone.
7. A-001 qualification: U40 and U8 are cheap read-only checks; run them before the owner decides on a later build.
8. Honest limit on the `marker_in_window` defence (`predicates.py:279-293`): it counts an own-login marker after the claim exists, so it does not close the window before the marker is posted.
9. Orchestrator addition (inference, not from a source): a stale-lease rule that uses time would give up the "no clock agreement between hosts" property that D:113 names as a reason for the lowest-comment-id lease; the rule is a design task, not a one-line fix.

## Resolution of unresolved points
- X-002: resolved as HYBRID wording (see 5 above).
- A-002: stays with OURS: the OD-8 gap is real (`claim.md:43`, D:113) but only the trigger is unobserved; the tie rule applies to the trigger.
