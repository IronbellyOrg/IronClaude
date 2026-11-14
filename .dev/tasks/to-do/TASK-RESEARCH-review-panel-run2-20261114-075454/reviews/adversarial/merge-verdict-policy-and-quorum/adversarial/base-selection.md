# Base Selection Report

Variant A = Variant 1 = Proposal A (`variant-1-original.md`). Variant B = Variant 2 = Proposal B (`variant-2-original.md`). Both are position papers; the "requirements" are those of conflict row C-03 (no formal requirement IDs exist, so the protocol's edge case applies: topic matching).

## Quantitative Scoring (50% weight)

Computed by the script `quant-score.py` in this folder (output: `quant-score-output.json`); deterministic, no model judgement. Run twice, identical output.

| Metric | Weight | Variant A (Proposal A) | Variant B (Proposal B) |
|--------|--------|-------------------|-------------------|
| requirement_coverage | 0.30 | 0.9091 (20 of 22 topics matched; missing: research 06 cited, research 17 cited) | 1.0000 (22 of 22 topics matched) |
| internal_consistency | 0.25 | 0.9811 (1 intra-variant contradiction, X-005, over 53 tagged claims) | 0.9487 (2 intra-variant contradictions, X-003 E11 vs E16 and X-006, over 39 tagged claims) |
| specificity_ratio | 0.15 | 1.0000 (434 concrete indicators, 0 vague) | 1.0000 (371 concrete indicators, 0 vague) |
| dependency_completeness | 0.15 | 1.0000 (14 of 14 internal section references resolve) | 0.9831 (58 of 59 internal section and E-number references resolve) |
| section_coverage | 0.15 | 1.0000 (7 H2 of max 7) | 1.0000 (7 H2 of max 7) |
| **quant_score** | | **0.9680** | **0.9846** |

Method notes (stated so the numbers can be challenged): RC uses 22 keyword patterns derived from row C-03 (union, pluggable policy, completion-state quorum, DEGRADED outcome, calibrator stance, evidence gate/adversarial merge, k-of-n clusters, INV-I/B/L/A, research files 03/06/07/08/12/17, PR effect, rf-qa effect, test/measurement, strongest objection, exit codes). IC counts only contradictions inside one variant (diff-analysis X-003 internal part, X-005, X-006) against tagged claims (`[CODE-VERIFIED]`, `[UNVERIFIED]`, `[CODE-CONTRADICTED]`, `[VERIFIED]`). SR and DC saturate near 1.0 for both, so they do not discriminate. The quantitative layer favours Variant B by 0.0166.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent scorer agents evaluated all 30 criteria for both variants with the CEV protocol: pass 1 in input order (A then B, `score-pass1.md`), pass 2 in reverse order (B then A, `score-pass2.md`). Evidence cells below are pass 1's CEV evidence (pass 2 reached the same verdict with equivalent evidence on every agreed row); the two disagreeing rows show the tie-resolving evaluation. `debate:` evidence refers to `debate-transcript.md`. The rubric scores each variant as written in its original file.

### Completeness (5 criteria)

| Criterion | Variant A (Proposal A) | Evidence | Variant B (Proposal B) | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 Covers all explicit requirements | NOT MET | Position, INV-I/B/L/A and r03, r07, r08, r12 are covered, but no research file 06 or 17 is cited anywhere (searched sections 1-7; only 03, 07, 08, 12, 13, web-01 appear). | MET | Position (s1), INV-A/B/I/L (s4) and all six files are cited: "r03", "r06 sections 2, 4.1, 7", "r07 E1-F5", "r08 sections 1, 4, 7", "r12 sections 2, 8", "r17 DR-062, DR-137". |
| C2 Addresses edge cases and failure scenarios | MET | s5 item 1: quorum matrix "for requested N in 1..5 and every assignment of the five completion states", seeded from the 4-requested, 1-valid, 3-broken case. | MET | s2.1 item 4: "If the adjudication stage is down, the policy falls back to union ... DEGRADED-style state, never PASS"; s5 failure conditions (a) to (d) including a wrongly rejected real blocker. |
| C3 Includes dependencies and prerequisites | MET | s3.2: "A union over what survives parsing is only as good as the repair policy of slot C-06"; s2.1 states the new `requested`/`resolved` round keys the merge needs. | MET | s2.1 item 5 names `model_observed` as "a decided requirement, C-08"; s5 item 2 depends on "the Tier Q rule of slot X-14" and an unrun seeded-defect design. |
| C4 Defines success/completion criteria | MET | s5 item 5 gives falsifiers: union wrong-blocker rate driving escalate-at-cap above 2-of-3 "with no recall advantage"; quorum floor falsifier; D-2 case "must change from PASS to DEGRADED". | MET | s5: "B is shown right if the adjudicated policy lowers wrong blockers per run with no loss of real-blocking recall"; wrong if (a) to (d). |
| C5 Specifies out-of-scope items | MET | s2.1: "This proposal does not decide who types `blocking` (that is slot C-02)"; s4.2 INV-A: the reflect `shortfall: degrade` switch "is outside this proposal". | MET | s2.3: "Per-row clearing is slot C-02 and is assumed independent"; s6: PR wire format "stays slot C-10"; "neither policy supports describing the panel as a full replacement". |
| **Subtotal** | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A (Proposal A) | Evidence | Variant B (Proposal B) | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 No factual errors or hallucinated claims | NOT MET | debate:R1/advocate-A K5 concedes "PASS on that path rests on defaults" (s3.1 item 4) is overstated; debate:R1/advocate-B W1 shows "a wrong blocker costs at most one fix cycle" (s7) is wrong because a rejected row stays open until the cap. | NOT MET | E11 is tagged [CODE-VERIFIED] as "computed from served model ids", but debate:R1/advocate-A W3 and debate:R1/advocate-B C3 both show `openai_compat.py:468` stamps the configured model id. |
| K2 Technical approaches feasible with stated constraints | MET | s2.1 builds a pure `derive_panel_outcome` from fields that exist (`COMPLETION_STATES`, manifest `_recount`, additive round keys); quorum as profile data is implementable without a model call. | NOT MET | s2.1 item 5 makes "at least 2 distinct model ids" a default verdict precondition, but served ids are not on the verdict path (debate:R1/advocate-A W3); `pending` rows have no brief or exit slot (debate:R1/advocate-A W1). |
| K3 Terminology used consistently and accurately | MET | Consistent use of `union`, `legacy-adversarial`, `shortfall: degrade|visible`, DEGRADED; s2.3 explicitly separates the two products' meanings of exit codes 10 and 11. | NOT MET | Row-state words drift: s2.1 item 3 uses "`pending` and `uncalibrated` blockers", s3.3 and s6 use "unconfirmed", s1 uses "contested"; "independent completions" is used for both completion count and served-model count. |
| K4 No internal contradictions | NOT MET | s1 and s4.1 claim INV-I holds "at every panel size", while s2.2 sets reflect to `shortfall: visible` where a 2-of-3 shortfall is PASS-eligible (diff X-005; debate:R1/advocate-B weakness 4). | NOT MET | s4 Preserved says "No verdict changes until a stage that promotes the engine", but s4 Endangered and s2.2 make `adjudicated` the default for spec-loop first reviews, "not shadow work" (diff X-006). |
| K5 Claims supported by evidence or rationale | MET | s3.1 gives file:line evidence per defect (`ledger.py:150-157`, `:273-275`) and s7 gives a rationale (asymmetric cost, S3 cap); unverified items are tagged [UNVERIFIED]. | MET | s3.1 and s3.2 are claim/source/tag tables E1-E17; the unsupported adjudication-beats-union claim is stated outright: "no measurement yet shows adjudication beating the union". |
| **Subtotal** | **3/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant A (Proposal A) | Evidence | Variant B (Proposal B) | Evidence |
|-----------|-----------|----------|-----------|----------|
| S1 Logical section ordering | MET | Seven sections in the template order: position, design, evidence, invariants, test, PR/rf-qa effect, objection. | MET | Same seven sections in the same order (s1 to s7). |
| S2 Consistent hierarchy depth, no orphans | MET | Numbered subsections 2.1-2.3, 3.1-3.3, 4.1-4.2 at one depth; no orphaned subsections. | MET | Subsections 2.1-2.3, 3.1-3.3, and "### Preserved"/"### Endangered" under s4, all one level deep; none orphaned. |
| S3 Clear separation of concerns | MET | Re-evaluation (tie-resolver): section-level separation is explicit; the pass-1 blemishes (test-pin evidence and one debate aside inside s2.2/s2.3) are placement issues that Variant 2 shares in kind. See score-reeval.md. | MET | s2 is design only (core list, module table, common-ground scope in 2.3); s3 separates code evidence (3.1), measured runs (3.2) and external evidence (3.3). |
| S4 Navigation aids present | MET | Tag legend in the header ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]) plus in-text cross-references ("section 5 item 4", "section 2.2"). | MET | Tag legend and citation shorthand line (`rNN`, `web-01`, `s05`, `UC`) plus evidence ids E1-E17 referenced later ("see 3, E2", "(E16)"). |
| S5 Follows artifact-type conventions | MET | Follows the position-paper template with Status lines and all required parts, including strongest objection and answer. | MET | Follows the same template with Status lines and all required parts. |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A (Proposal A) | Evidence | Variant B (Proposal B) | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 Unambiguous language | MET | Decisive wording: "The default policy is the any-blocking union"; "No assignment of reviewers below `min_complete` yields PASS in a `degrade` profile"; open parameters are named as such. | NOT MET | s1 says a blocker "can fail a round only after" adjudication, while s2.1 item 3 says pending blockers "block PASS" without naming the resulting verdict; "contested" is never defined where first used (s1). |
| L2 Concrete rather than abstract | MET | Names `derive_panel_outcome(rows, completion_records, policy)`, `min_complete`, `shortfall`, a new additive exit code and an N=1..5 test matrix. | MET | Names `policy(rows, panel_state, adjudication)`, row fields `evidence_gate`, `support`, `adjudication`, and the default trigger "`reviewers_resolved >= 2`". |
| L3 Clear section purpose | MET | Each section has a single stated purpose (position, core and module consequence, evidence, invariants, test, effects, objection). | MET | Same; each section and subsection headed by its purpose, e.g. "2.3 What B takes from common ground and does not argue". |
| L4 Acronyms and terms defined on first use | NOT MET | INV-B, INV-L, INV-A, INV-D, "D-2", "S3", "FR-RH2.9", "slot C-06" are used without definition; only INV-I gets an inline gloss in s1. | NOT MET | INV-A through INV-L, "UC", "D-13", "I-2", "TPR/FPR/Youden's J" and "Tier Q rule" are used without definition (only `rNN`/`web-01`/`s05` shorthand is defined in the header). |
| L5 Actionable next steps / decision points | MET | s5 lists five numbered tests and two falsifiers; s7 names the residual decision: single-reviewer blocking stopping a loop, and the quorum floor. | MET | s5 lists four numbered steps with a pre-committed decision rule and explicit right/wrong conditions; s7 ends with what the evidence does not support. |
| **Subtotal** | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A (Proposal A) | Evidence | Variant B (Proposal B) | Evidence |
|-----------|-----------|----------|-----------|----------|
| Q1 At least 3 risks with probability and impact | NOT MET | s4.2 gives four risks with impact only ("INV-D (HIGH if mishandled)", "INV-B (MEDIUM)"); no probability or likelihood is assessed for any. | NOT MET | s4 Endangered table gives severity (HIGH/MEDIUM/LOW) and exposure for five invariants; no likelihood assessed. |
| Q2 Mitigation for each risk | MET | Each s4.2 risk has a mitigation: rewrite pins "with the fix, not deleted"; "Section 2.3 avoids it"; the reflect switch "outside this proposal"; debate kept authoritative. | NOT MET | The INV-L row ("a behaviour change for an existing consumer, not shadow work") states exposure but no mitigation; the other rows have a "B must do" action. |
| Q3 Failure modes and recovery | MET | s6: "A partial panel in a PR round is visible as DEGRADED and the module can re-dispatch"; zero-valid refusal kept; s5 item 2 monotonic fail-closed property. | MET | s2.1 item 4: adjudication stage down means fallback to `union` and DEGRADED, never PASS; s4 requires every rejection to be recorded and counted. |
| Q4 External dependencies and failure scenarios | MET | s3.2: union quality depends on "the repair policy of slot C-06"; truncated or invalid completion states "where that loss becomes visible to quorum"; calibrator lost its class in 6 of 15 runs. | MET | s5 condition (c): "the adjudicator was served by a reviewer's model ... as the calibrator was in 6 of 15"; dependency on `model_observed` (C-08) and on the validator agent. |
| Q5 Monitoring or validation mechanism | MET | s5 items 3-5: `test_verdict_mapping.py` stays at 36, replay at 0 differences, and "wrong blockers per row" as the one number that shows failure. | MET | s5 item 4: "the adjudicator's `model_observed` must differ from the reviewers' served models in every run"; rejections reported per run; replay regression gate. |
| **Subtotal** | **4/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A (Proposal A) | Evidence | Variant B (Proposal B) | Evidence |
|-----------|-----------|----------|-----------|----------|
| I1 Collection boundary conditions | MET | s5 item 1: N in 1..5 across all five completion states; s6: single-reviewer re-review (`requested = 1`, `complete = 1`) meets quorum; zero-valid refusal at `ledger.py:150-157`. | MET | s2.1 item 1: `adjudicated` only when "`reviewers_resolved >= 2`", single-reviewer re-review uses `union`; s4: "zero valid blocks still refuses"; s5 (d): contested set "so large" it becomes the verdict. |
| I2 State-variable interactions across boundaries | MET | s2.1: `ledger.merge_round` "never reads the manifest" while the manifest counts `reviewers_complete`; s2.3: exit 10/11 mean different things in ledger and reflect. | MET | Re-evaluation (tie-resolver): cites cross-boundary flows with named carriers (manifest to quorum in s2.1 item 5; core adjudication state to reflect `degraded_components`/`adversarial_unavailable` in s4 Preserved); the `pending` vs `_brief_ids`/`defer` gap is a completeness limit of the same class as A's DEGRADED gap. See score-reeval.md. |
| I3 Guard-condition gaps | MET | s3.1 item 1: the only guard is `not any(block_ok.values())`; "Nothing converts the count into an outcome" (item 3); `ledger.load` checks only the schema string. | MET | E3: "The only refusal is at zero valid blocks; one valid block of N is enough"; E4 reproduces the unguarded case; s4 restricts `rejected` to deterministic failure as a guard. |
| I4 Count-divergence scenarios | MET | s2.1: `requested`, `resolved`, `complete` counts and the `tier_reached = 2 if reviewer_count >= 2` boundary; the floor choice "2-of-3, majority or all" is called out as unmeasured. | MET | s1: quorum "counts independent completions ... not dispatched reviewers, because ... requested ids and served models diverge"; E15: 13 of 216 clusters had two or more reviewers. |
| I5 Interaction effects when components combine | MET | s2.2: reflect `shortfall: visible` interacting with pins `test_i3...` and `test_fx7...`; s6: rf-qa regression and monotonicity halts "additive to the outcome function". | MET | s2.2: first reviews use `adjudicated` while single-reviewer re-review uses `union`; s2.1 item 4: adjudication-down fallback to `union` combines with the DEGRADED state. |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 3/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 3/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **22/30 = 0.7333** |
### Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Floor (>= 1/5) | Eligible as base |
|---------|-------------------------------|----------------|------------------|
| A | 5/5 | met | Yes |
| B | 5/5 | met | Yes |

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| S3 Clear separation of concerns | A | NOT MET | MET | DISAGREE | MET (re-evaluated, `score-reeval.md`) |
| I2 State-variable interactions across boundaries | B | MET | NOT MET | DISAGREE | MET (re-evaluated, `score-reeval.md`) |
Disagreements re-evaluated: 2 of 60 criterion-variant pairs (58 agreed). Final verdicts changed relative to pass 1 or pass 2: 2 (S3 for A: pass 1 NOT MET to MET; I2 for B: pass 2 NOT MET to MET; each re-evaluation sided with one of the two passes). Net effect: neither scorer pass alone would have produced the final totals (pass 1: A 24, B 22; pass 2: A 25, B 21; final: A 25, B 22).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (Proposal A) | 0.4840 | 0.4167 | **0.9007** | 9 points won (S-003, C-002, C-004, C-005, C-006, C-008, X-002, X-003, X-006) = 43% of 21 scored S/C/X points |
| B (Proposal B) | 0.4923 | 0.3667 | **0.8590** | 3 points won (S-002, C-012, X-005) = 14% of 21 |

(8 further points resolved as Hybrid: C-001, C-003, C-007, C-009, C-010, C-011, X-001, X-004; 1 as Neither: S-001.)

**Margin**: 4.17% (below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance). Variant A won 9 points against 3 for Variant B, a decisive difference, so levels 2 and 3 were not needed (for the record: correctness criteria MET were A 3, B 1).

## Selected Base: Variant A (Proposal A; `variant-1-original.md`)

### Selection Rationale

- The combined scores are inside the 5% tiebreaker band (A 0.9007, B 0.8590, margin 4.17%). The raw scores favour A, and the tiebreaker (debate performance: A 9 points won, B 3, 8 Hybrid, 1 Neither) confirms A.
- The two layers pull in opposite directions and both are reported: the quantitative layer favours B (0.9846 versus 0.9680, driven by requirement coverage 1.0 versus 0.909 because A cites no research 06 or 17); the qualitative layer favours A (25/30 versus 22/30) on Correctness (3/5 versus 1/5), Clarity (4/5 versus 3/5) and Risk Coverage (4/5 versus 3/5). B's Correctness losses are three code-checked defects the debate established: E11 "computed from served model ids" is wrong for the shipped transport (`openai_compat.py:467-468`), the `pending` row state has no brief entry, verdict or exit code in the ledger (`ledger.py:99-104, 273-275, 356-360`), and B's INV-L statements contradict each other. A's Correctness losses are an overstated claim ("at most one fix cycle", conceded) and the "every panel size" headline against its own reflect profile.
- Both advocates, after two rounds and with code evidence, named the same winner on all 21 S/C/X points (A 9, B 3, Hybrid 8, Neither 1). The Hybrid points mean the merged result takes elements of both; the base is the variant the merge changes least.
- Both variants meet the edge-case floor (5/5 each).

### Strengths to Preserve from Base
1. Pure outcome function over rows, recorded completion states and a named policy; policy registry with `union` default and `legacy-adversarial` for reflect (A section 2.1, 2.2).
2. Reflect profile `shortfall: visible`, bounded by the verified pins `test_i3_partial_two_of_three_distinct_pass_eligible` and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` (FR-RH2.9, `ensemble.py:755-770`); `derive_verdict` and its 36 tests untouched.
3. The 10/11 exit-code collision analysis (`ledger_cmd.py:13` versus `models.py:34-48`) and the rule not to reuse those codes (A section 2.3).
4. Quorum matrix (N=1..5 x five completion states) and the monotonic fail-closed property test (A section 5).
5. The asymmetric-cost argument tied to the S3 cap, with the correction that a Reviser-rejected row stays open to the cap (debate:R2/A R1).

### Strengths to Incorporate from Non-Base Variants
1. From Variant B, section 5 failure conditions (a) to (d) and the served-by-a-reviewer's-model check, as falsifiers for any promoted adjudicated policy (debate:R2/A bullet 11, R2/B term 11).
2. From Variant B, the `adjudicated` policy as a named policy run offline on stored reviewer outputs, with `rejected` restricted to a deterministic evidence failure or a quoted re-read and every rejection recorded (B section 2.1 item 3, section 4 Endangered; debate:R2/B terms 6, 7).
3. From Variant B, independence (distinct served model ids, vendor) as recorded "requested, not served" data now and a quorum predicate only when the transport records `model_observed` (B section 2.1 item 5; debate:R2/B term 12).
4. From Variant B, the claim limit (a union of automated reviewers is not a full replacement for human or test-based review; B section 6) and B's `calibration_map` channel kept separate from the reviewer line (B section 2.1 item 6).
5. From the Round 2 debate (new, both advocates): quorum as a merge-time refusal (nothing recorded, exit 12, no new decision value), `requested` from the resolution with a `len(--report)` lower bound, no `pending` state, and the precondition that the union is the cheap-error side only if a Reviser-rejected row has a non-human exit (slot C-02).
6. From the Round 2.5 invariant probe: the 2 HIGH and 8 MEDIUM UNADDRESSED items (`invariant-probe.md`) are carried into the refactoring plan as explicit open risks; they are not resolved by the base choice.
