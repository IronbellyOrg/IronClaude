PASS 1 (input order: Variant 1 then Variant 2)

Variant 1 = Proposal A (union default). Variant 2 = Proposal B (adjudicated default). Requirement source: conflict row C-03 (position text, INV-I/B/L/A, research files 03, 06, 07, 08, 12, 17). Debate evidence is cited as `debate:<round/advocate>`.

## Completeness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| C1 | Variant 1 | 0 | Position, INV-I/B/L/A and r03, r07, r08, r12 are covered, but no research file 06 or 17 is cited anywhere (searched sections 1-7; only 03, 07, 08, 12, 13, web-01 appear). |
| C1 | Variant 2 | 1 | Position (s1), INV-A/B/I/L (s4) and all six files are cited: "r03", "r06 sections 2, 4.1, 7", "r07 E1-F5", "r08 sections 1, 4, 7", "r12 sections 2, 8", "r17 DR-062, DR-137". |
| C2 | Variant 1 | 1 | s5 item 1: quorum matrix "for requested N in 1..5 and every assignment of the five completion states", seeded from the 4-requested, 1-valid, 3-broken case. |
| C2 | Variant 2 | 1 | s2.1 item 4: "If the adjudication stage is down, the policy falls back to union ... DEGRADED-style state, never PASS"; s5 failure conditions (a) to (d) including a wrongly rejected real blocker. |
| C3 | Variant 1 | 1 | s3.2: "A union over what survives parsing is only as good as the repair policy of slot C-06"; s2.1 states the new `requested`/`resolved` round keys the merge needs. |
| C3 | Variant 2 | 1 | s2.1 item 5 names `model_observed` as "a decided requirement, C-08"; s5 item 2 depends on "the Tier Q rule of slot X-14" and an unrun seeded-defect design. |
| C4 | Variant 1 | 1 | s5 item 5 gives falsifiers: union wrong-blocker rate driving escalate-at-cap above 2-of-3 "with no recall advantage"; quorum floor falsifier; D-2 case "must change from PASS to DEGRADED". |
| C4 | Variant 2 | 1 | s5: "B is shown right if the adjudicated policy lowers wrong blockers per run with no loss of real-blocking recall"; wrong if (a) to (d). |
| C5 | Variant 1 | 1 | s2.1: "This proposal does not decide who types `blocking` (that is slot C-02)"; s4.2 INV-A: the reflect `shortfall: degrade` switch "is outside this proposal". |
| C5 | Variant 2 | 1 | s2.3: "Per-row clearing is slot C-02 and is assumed independent"; s6: PR wire format "stays slot C-10"; "neither policy supports describing the panel as a full replacement". |

## Correctness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| K1 | Variant 1 | 0 | debate:R1/advocate-A K5 concedes "PASS on that path rests on defaults" (s3.1 item 4) is overstated; debate:R1/advocate-B W1 shows "a wrong blocker costs at most one fix cycle" (s7) is wrong because a rejected row stays open until the cap. |
| K1 | Variant 2 | 0 | E11 is tagged [CODE-VERIFIED] as "computed from served model ids", but debate:R1/advocate-A W3 and debate:R1/advocate-B C3 both show `openai_compat.py:468` stamps the configured model id. |
| K2 | Variant 1 | 1 | s2.1 builds a pure `derive_panel_outcome` from fields that exist (`COMPLETION_STATES`, manifest `_recount`, additive round keys); quorum as profile data is implementable without a model call. |
| K2 | Variant 2 | 0 | s2.1 item 5 makes "at least 2 distinct model ids" a default verdict precondition, but served ids are not on the verdict path (debate:R1/advocate-A W3); `pending` rows have no brief or exit slot (debate:R1/advocate-A W1). |
| K3 | Variant 1 | 1 | Consistent use of `union`, `legacy-adversarial`, `shortfall: degrade|visible`, DEGRADED; s2.3 explicitly separates the two products' meanings of exit codes 10 and 11. |
| K3 | Variant 2 | 0 | Row-state words drift: s2.1 item 3 uses "`pending` and `uncalibrated` blockers", s3.3 and s6 use "unconfirmed", s1 uses "contested"; "independent completions" is used for both completion count and served-model count. |
| K4 | Variant 1 | 0 | s1 and s4.1 claim INV-I holds "at every panel size", while s2.2 sets reflect to `shortfall: visible` where a 2-of-3 shortfall is PASS-eligible (diff X-005; debate:R1/advocate-B weakness 4). |
| K4 | Variant 2 | 0 | s4 Preserved says "No verdict changes until a stage that promotes the engine", but s4 Endangered and s2.2 make `adjudicated` the default for spec-loop first reviews, "not shadow work" (diff X-006). |
| K5 | Variant 1 | 1 | s3.1 gives file:line evidence per defect (`ledger.py:150-157`, `:273-275`) and s7 gives a rationale (asymmetric cost, S3 cap); unverified items are tagged [UNVERIFIED]. |
| K5 | Variant 2 | 1 | s3.1 and s3.2 are claim/source/tag tables E1-E17; the unsupported adjudication-beats-union claim is stated outright: "no measurement yet shows adjudication beating the union". |

## Structure

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| S1 | Variant 1 | 1 | Seven sections in the template order: position, design, evidence, invariants, test, PR/rf-qa effect, objection. |
| S1 | Variant 2 | 1 | Same seven sections in the same order (s1 to s7). |
| S2 | Variant 1 | 1 | Numbered subsections 2.1-2.3, 3.1-3.3, 4.1-4.2 at one depth; no orphaned subsections. |
| S2 | Variant 2 | 1 | Subsections 2.1-2.3, 3.1-3.3, and "### Preserved"/"### Endangered" under s4, all one level deep; none orphaned. |
| S3 | Variant 1 | 0 | s2.2 mixes design with evidence and a debate aside ("Note for the debate ... [CODE-CONTRADICTED] by the pins above"); s2.3 holds test-pin evidence inside the design section. |
| S3 | Variant 2 | 1 | s2 is design only (core list, module table, common-ground scope in 2.3); s3 separates code evidence (3.1), measured runs (3.2) and external evidence (3.3). |
| S4 | Variant 1 | 1 | Tag legend in the header ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]) plus in-text cross-references ("section 5 item 4", "section 2.2"). |
| S4 | Variant 2 | 1 | Tag legend and citation shorthand line (`rNN`, `web-01`, `s05`, `UC`) plus evidence ids E1-E17 referenced later ("see 3, E2", "(E16)"). |
| S5 | Variant 1 | 1 | Follows the position-paper template with Status lines and all required parts, including strongest objection and answer. |
| S5 | Variant 2 | 1 | Follows the same template with Status lines and all required parts. |

## Clarity

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| L1 | Variant 1 | 1 | Decisive wording: "The default policy is the any-blocking union"; "No assignment of reviewers below `min_complete` yields PASS in a `degrade` profile"; open parameters are named as such. |
| L1 | Variant 2 | 0 | s1 says a blocker "can fail a round only after" adjudication, while s2.1 item 3 says pending blockers "block PASS" without naming the resulting verdict; "contested" is never defined where first used (s1). |
| L2 | Variant 1 | 1 | Names `derive_panel_outcome(rows, completion_records, policy)`, `min_complete`, `shortfall`, a new additive exit code and an N=1..5 test matrix. |
| L2 | Variant 2 | 1 | Names `policy(rows, panel_state, adjudication)`, row fields `evidence_gate`, `support`, `adjudication`, and the default trigger "`reviewers_resolved >= 2`". |
| L3 | Variant 1 | 1 | Each section has a single stated purpose (position, core and module consequence, evidence, invariants, test, effects, objection). |
| L3 | Variant 2 | 1 | Same; each section and subsection headed by its purpose, e.g. "2.3 What B takes from common ground and does not argue". |
| L4 | Variant 1 | 0 | INV-B, INV-L, INV-A, INV-D, "D-2", "S3", "FR-RH2.9", "slot C-06" are used without definition; only INV-I gets an inline gloss in s1. |
| L4 | Variant 2 | 0 | INV-A through INV-L, "UC", "D-13", "I-2", "TPR/FPR/Youden's J" and "Tier Q rule" are used without definition (only `rNN`/`web-01`/`s05` shorthand is defined in the header). |
| L5 | Variant 1 | 1 | s5 lists five numbered tests and two falsifiers; s7 names the residual decision: single-reviewer blocking stopping a loop, and the quorum floor. |
| L5 | Variant 2 | 1 | s5 lists four numbered steps with a pre-committed decision rule and explicit right/wrong conditions; s7 ends with what the evidence does not support. |

## Risk Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| Q1 | Variant 1 | 0 | s4.2 gives four risks with impact only ("INV-D (HIGH if mishandled)", "INV-B (MEDIUM)"); no probability or likelihood is assessed for any. |
| Q1 | Variant 2 | 0 | s4 Endangered table gives severity (HIGH/MEDIUM/LOW) and exposure for five invariants; no likelihood assessed. |
| Q2 | Variant 1 | 1 | Each s4.2 risk has a mitigation: rewrite pins "with the fix, not deleted"; "Section 2.3 avoids it"; the reflect switch "outside this proposal"; debate kept authoritative. |
| Q2 | Variant 2 | 0 | The INV-L row ("a behaviour change for an existing consumer, not shadow work") states exposure but no mitigation; the other rows have a "B must do" action. |
| Q3 | Variant 1 | 1 | s6: "A partial panel in a PR round is visible as DEGRADED and the module can re-dispatch"; zero-valid refusal kept; s5 item 2 monotonic fail-closed property. |
| Q3 | Variant 2 | 1 | s2.1 item 4: adjudication stage down means fallback to `union` and DEGRADED, never PASS; s4 requires every rejection to be recorded and counted. |
| Q4 | Variant 1 | 1 | s3.2: union quality depends on "the repair policy of slot C-06"; truncated or invalid completion states "where that loss becomes visible to quorum"; calibrator lost its class in 6 of 15 runs. |
| Q4 | Variant 2 | 1 | s5 condition (c): "the adjudicator was served by a reviewer's model ... as the calibrator was in 6 of 15"; dependency on `model_observed` (C-08) and on the validator agent. |
| Q5 | Variant 1 | 1 | s5 items 3-5: `test_verdict_mapping.py` stays at 36, replay at 0 differences, and "wrong blockers per row" as the one number that shows failure. |
| Q5 | Variant 2 | 1 | s5 item 4: "the adjudicator's `model_observed` must differ from the reviewers' served models in every run"; rejections reported per run; replay regression gate. |

## Invariant & Edge Case Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| I1 | Variant 1 | 1 | s5 item 1: N in 1..5 across all five completion states; s6: single-reviewer re-review (`requested = 1`, `complete = 1`) meets quorum; zero-valid refusal at `ledger.py:150-157`. |
| I1 | Variant 2 | 1 | s2.1 item 1: `adjudicated` only when "`reviewers_resolved >= 2`", single-reviewer re-review uses `union`; s4: "zero valid blocks still refuses"; s5 (d): contested set "so large" it becomes the verdict. |
| I2 | Variant 1 | 1 | s2.1: `ledger.merge_round` "never reads the manifest" while the manifest counts `reviewers_complete`; s2.3: exit 10/11 mean different things in ledger and reflect. |
| I2 | Variant 2 | 1 | s4 Preserved: adjudication failures reach `derive_verdict` "through fields it already reads (`degraded_components` ..., `adversarial_unavailable`)"; s2.1 item 5 joins manifest completion with served model ids. |
| I3 | Variant 1 | 1 | s3.1 item 1: the only guard is `not any(block_ok.values())`; "Nothing converts the count into an outcome" (item 3); `ledger.load` checks only the schema string. |
| I3 | Variant 2 | 1 | E3: "The only refusal is at zero valid blocks; one valid block of N is enough"; E4 reproduces the unguarded case; s4 restricts `rejected` to deterministic failure as a guard. |
| I4 | Variant 1 | 1 | s2.1: `requested`, `resolved`, `complete` counts and the `tier_reached = 2 if reviewer_count >= 2` boundary; the floor choice "2-of-3, majority or all" is called out as unmeasured. |
| I4 | Variant 2 | 1 | s1: quorum "counts independent completions ... not dispatched reviewers, because ... requested ids and served models diverge"; E15: 13 of 216 clusters had two or more reviewers. |
| I5 | Variant 1 | 1 | s2.2: reflect `shortfall: visible` interacting with pins `test_i3...` and `test_fx7...`; s6: rf-qa regression and monotonicity halts "additive to the outcome function". |
| I5 | Variant 2 | 1 | s2.2: first reviews use `adjudicated` while single-reviewer re-review uses `union`; s2.1 item 4: adjudication-down fallback to `union` combines with the DEGRADED state. |

## Subtotals

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness | 4/5 | 5/5 |
| Correctness | 3/5 | 1/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 3/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| Total | 24/30 | 22/30 |
