# Diff Analysis: Position Paper Comparison (slot C-03, merge-verdict-policy-and-quorum)

## Metadata
- Generated: 2026-11-14 (orchestrator, Step 1)
- Variants compared: 2 (Variant 1 = Proposal A, `variant-1-original.md`; Variant 2 = Proposal B, `variant-2-original.md`)
- Mode: A (--compare), depth standard, focus: correctness, risk, test-coverage
- Total differences found: 26 diff points (denominator for convergence = S + C + X + A)
- Categories: structural (3), content (12), contradictions (6), unique (11), shared assumptions (5)
- Taxonomy tags: L1 surface, L2 structural, L3 state-mechanics (auto-tagged per protocol; highest matching level wins)
- Source of requirements for scoring: conflict row C-03 in `phase-outputs/discovery/undecidable-conflicts.md` (Position A and Position B text, "Invariants at stake", "Research files to cite")

## Structural Differences

| # | Area | Variant A (Proposal A) | Variant B (Proposal B) | Severity | Level |
|---|------|------------------------|------------------------|----------|-------|
| S-001 | Section skeleton | 7 H2 sections: position, design consequence, evidence, invariants, test/measurement, PR/rf-qa effect, objection | Same 7 H2 sections in the same order | Low | L1 |
| S-002 | Evidence presentation | Numbered prose items (3.1, 3.2, 3.3); tags inline | Tables E1..E17 with Claim / Source / Tag columns; invariants as tables | Low | L1 |
| S-003 | Section 2 sub-structure | 2.1 Core, 2.2 Named modules (bullets), 2.3 Exit codes | 2.1 Shared core (numbered list), 2.2 Module table, 2.3 "What B takes from common ground" | Medium | L2 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Level |
|---|-------|--------------------|--------------------|----------|-------|
| C-001 | Default merge policy for a panel of 2 or more reviewers | `union`: a finding any complete reviewer types as blocking fails the round; confidence is display only | `adjudicated` (default when `reviewers_resolved >= 2`): a blocking row fails a round only after evidence gate, support signal and, for contested rows, validator re-read and adversarial merge; `union` is the baseline arm and the fallback | High | L2 |
| C-002 | Where the calibrate/validate/debate chain lives | Not in the default path; it is the module-owned `legacy-adversarial` policy (reflect only); calibrated confidence is an optional displayed input | A core-owned adjudication stage reusing the reflect legacy chain, callable from the core, recorded per row | High | L2 |
| C-003 | Definition of quorum | Count of `complete` reviewers among requested, against profile field `min_complete`; floor = 2 when 2 or more requested (mirrors `ensemble.py:772-773`); value 2-of-3 / majority / all declared unmeasured | Count of independent completions: `complete` state AND at least 2 distinct served model ids AND not single vendor unless flagged (mirrors `fallback.py:75-82`, `contract.py:282-288`) | High | L3 |
| C-004 | Outcome for a partial panel (complete below requested) | `shortfall` profile mode: `degrade` gives DEGRADED, never PASS; `visible` records the shortfall and leaves the verdict (reflect profile, because of pins FR-RH2.9) | DEGRADED-style outcome accepted as common ground (r03 I-2); PASS needs quorum met, zero confirmed and zero pending blockers; adjudication stage down gives `union` plus DEGRADED | High | L3 |
| C-005 | Treatment of a blocking row nobody has adjudicated | Any blocking `open`/`regressed` row is in the brief and fails the round (existing ledger rule, unchanged) | `pending`/`uncalibrated` blockers stay open, are counted in the headline and block PASS; only `confirmed` blockers drive FAIL/REVISE and the Reviser brief; `rejected` allowed only on deterministic evidence failure or a quoted validator re-read | High | L3 |
| C-006 | Ledger/exit-code expression of the new outcome | Adds DEGRADED as a new additive ledger exit code that does not reuse 10 or 11; pure function `derive_panel_outcome(rows, completion_records, policy)` returns PASS/REVISE/ESCALATE/DEGRADED | Ledger exit contract 0/10/11 unchanged; DEGRADED-style state named but no exit code or function signature given; `policy(rows, panel_state, adjudication)` | Medium | L3 |
| C-007 | Reflect module integration | `legacy-adversarial` policy stays authoritative with `shortfall: visible`; union runs in shadow; `derive_verdict` untouched | Reflect keeps calibrator, validator and adversarial merge as the adjudication stage; `derive_verdict` stays the shell; four consumer-read contract fields populated by the core stage | Medium | L2 |
| C-008 | Spec-review loop behaviour | `union` + `shortfall: degrade`: one-valid-of-three PASS (D-2) becomes DEGRADED; zero-valid refusal kept | First reviews of 3 to 4 reviewers use `adjudicated`; single-reviewer re-review uses `union`; B itself flags this as a shipped-behaviour change (INV-L MEDIUM) | Medium | L2 |
| C-009 | PR-review effect | Verdict ignored (PR flow has none); union supplies the complete finding set; DEGRADED visible so module can re-dispatch | Adjudication decides which findings enter `verify`/`push`; evidence-gate rejections never reach a fix round | Medium | L2 |
| C-010 | rf-qa replacement effect | Declared single-reviewer re-review meets quorum; intended 3-reviewer re-review completing with 1 does not; regression/monotonicity halts additive | Exposes `support`, `disputed` and adjudication record as inputs for confidence gate and monotonicity check | Medium | L2 |
| C-011 | Test and measurement plan | Quorum matrix over N in 1..5 and all 5 completion states; monotonic fail-closed property test; replay of E2 under 3 policies; falsifiers for default and for the quorum floor | Offline replay of union vs contested-row rules; run adding the adjudication stage on same stored outputs; adjudicator `model_observed` check; failure conditions (a) to (d) | Medium | L2 |
| C-012 | Calibration channel and adjudicator independence | Not a default input; per-finding `confidence` rendered and never read | Separate `calibration_map` keyed by finding id; adjudicator observed model id recorded and must differ from reviewers' served models | Medium | L2 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Which policy is the default for a multi-reviewer panel | A section 1: "The default policy is the any-blocking union ... No calibrator, debate or grader sits in the default path" | B section 1: "`adjudicated` as the default for panels, and the union as the baseline arm" | High |
| X-002 | Whether "DEGRADED (never PASS) for a partial panel" is a settled common-ground point | A section 2.2: for the reflect profile the slot sentence is "[CODE-CONTRADICTED]" by pins `test_i3_partial_two_of_three_distinct_pass_eligible` and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` (FR-RH2.9, `ensemble.py:755-770`); holds only for modules opting into `shortfall: degrade` | B section 2.3: "Quorum over recorded completion states and a DEGRADED-style outcome for a partial panel (r03 I-2) ... decided by reproduced evidence ... assumed here" | High |
| X-003 | Whether a served-model-id quorum already exists in code | B E11: `QuorumState(...)` is "a Tier-2 gate computed from served model ids [that] already exists" (`fallback.py:75-82`, `contract.py:281-288`) | B E16 and UC row C-04 text: `calibrator_diversity: full` was reported while every agent served one model; engine A's diversity is over REQUESTED ids (`openai_compat.py:467-470`); B section 2.1 item 5 says served ids need `model_observed` which is a decided requirement [UNVERIFIED] | High |
| X-004 | Does the legacy reflect verdict rest on adjudication evidence or on defaulted fields | A section 3.1 item 4: engine A fills `merge_method` by reviewer count (`ensemble.py:773`) and zero deviation counts (`:779-785`), so a PASS "rests on defaults" | B E7, E8: production reflect verdict DEGRADES on 5 listed triggers and is derived from the adversarial child's convergence score, not a union | High |
| X-005 | Intra-A: fail-closed "at every panel size" versus reflect `shortfall: visible` | A section 1 and 4.1: "No assignment of reviewers below `min_complete` yields PASS in a `degrade` profile" and "INV-I holds at every panel size" | A section 2.2: reflect profile `shortfall: visible` lets a 2-of-3 shortfall be PASS-eligible | Medium |
| X-006 | Intra-B: shadow-only (INV-L) versus default change in the spec loop | B section 4 Preserved: "No verdict changes until a stage that promotes the engine" | B section 4 Endangered and 2.2: `adjudicated` default for first reviews of the spec loop "changes a verdict that ships today ... not shadow work" | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Pure outcome function `derive_panel_outcome(rows, completion_records, policy)` with policy registry and quorum as data (`min_complete`, `shortfall` degrade/visible) | High |
| U-002 | A | New additive DEGRADED ledger exit code that avoids reusing 10/11 (avoids ESCALATE/DEGRADED conflation across the two products) | High |
| U-003 | A | Test design: quorum matrix over N=1..5 and all 5 completion states; monotonic fail-closed property test | High |
| U-004 | A | Verified reflect pins (FR-RH2.9, `ensemble.py:755-770`, two named tests) that bound where DEGRADED-on-shortfall can apply; `shortfall: visible` profile | High |
| U-005 | A | Asymmetric-cost argument tied to repo rule S3 (cap of 2 fix cycles; never pass open blocking findings) | Medium |
| U-006 | B | Per-row adjudication record (`evidence_gate`, `support`, `adjudication` enum, adjudicator observed model id), ids/enums/numbers only (INV-H) | High |
| U-007 | B | Served-model quorum: distinct model ids and single-vendor check as quorum components | Medium |
| U-008 | B | `pending` row state that blocks PASS without being dropped; restriction of `rejected` to deterministic or quoted-re-read failures; fail-open risk of a buggy adjudicator named as HIGH | High |
| U-009 | B | Stated falsifiers (a) to (d) incl. adjudicator served by a reviewer's model; `model_observed` check inside the run | Medium |
| U-010 | B | Four consumer-read contract names (`confidence_calibrated`, `evidence_validator_ran`, `reviewer_cards`, `calibrator_diversity`) become core-populated, not prose-only (E10) | Medium |
| U-011 | B | Limit on claims: union of 4 automated reviewers passed 41.5% of tests built from human reviews; panel not a full replacement | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | A reviewer in state `complete` has substantively examined the document, so counting `complete` states measures coverage | Both quorums count `complete` completions (A `min_complete`; B "independent completions") | UNSTATED | High: a parsed-but-shallow reviewer satisfies quorum and a one-valid-block PASS is the reproduced defect D-2 | Promoted |
| A-002 | Additive round keys (A) and additive optional row keys (B) in `review-ledger/1` break no reader | Both claim additive-only change; only A cites `ledger.load` (`ledger.py:47-48`) | UNSTATED (B) / STATED (A, schema string only) | Medium: E2 tools, variant ledgers and scripts are not enumerated | Promoted |
| A-003 | DEGRADED (A) and `pending` rows (B) have a defined transition in the fix loop (cycle cap, re-dispatch, ESCALATE at cap, exit status) | Both add a non-PASS, non-FAIL state | UNSTATED | High: a state that blocks PASS but does not enter the Reviser brief can stall or silently consume cycles | Promoted |
| A-004 | The 2-of-3 PASS-eligible shortfall in reflect (FR-RH2.9) is intended behaviour, not a defect | A states and proves with pins; B silent and treats DEGRADED-on-partial as decided | CONTRADICTED (by B section 2.3) / STATED (A) | High | Promoted |
| A-005 | Served model id (`model_observed`) is obtainable for every reviewer and the adjudicator in every transport | B depends on it for quorum and independence; A only for diversity telemetry | UNSTATED | Medium: B marks it [UNVERIFIED]; headless/stub lanes may lack it | Promoted |

STATED and shared, not promoted: derive-the-verdict-on-read (both); `defer` cannot rewrite a verdict (B I-4; A section 2.1); single-reviewer findings are kept as unconfirmed (both); who types `blocking` is slot C-02 (both); measurement is the arbiter and E2 is a derivation set (both).

## Summary
- Total structural differences: 3
- Total content differences: 12
- Total contradictions: 6
- Total unique contributions: 11
- Total shared assumptions surfaced: 5 (UNSTATED: 4 counting A-002 mixed, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: C-001, C-002, C-003, C-004, C-005, X-001, X-002, X-003, X-004, A-001, A-003, A-004
- Similarity check: differences far exceed 10% of comparable items; variants are not substantially identical. Debate proceeds.
- Agreement points (convergence seeds): derive-on-read; single-reviewer findings kept as unconfirmed; INV-A/B/C/D contract preservation; pins rewritten with the fix; evidence gate stays code-backed; policy must be measurable; union stays in the design as a named policy.
