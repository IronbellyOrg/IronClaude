# Proposal B: slot C-03 (merge-verdict-policy-and-quorum)

Status: Complete

Date: 2026-11-14
Slot: C-03, slug `merge-verdict-policy-and-quorum`, conflict IDs C-S4, VM-5, FX-9, FX-10
Position: B (a calibrated or debated verdict for multi-reviewer panels)
Tags: every claim taken from a document or research file carries [CODE-VERIFIED] (re-read against the code or tests in this session), [CODE-CONTRADICTED] or [UNVERIFIED] (reported by the cited research file and not re-run here). Citation shorthand: `rNN` is `research/NN-*.md`, `web-01` is `research/web-01-multi-model-review-evidence.md`, `s05` is `synthesis/synth-05-options.md`, `UC` is `phase-outputs/discovery/undecidable-conflicts.md`. Code paths are relative to the repository root.

## 1. The position

The shared core does not take the union of reviewer-typed `blocking` flags as the verdict of a panel of two or more reviewers. A blocking row can fail a round only after it has passed an adjudication stage that the core owns and records per row: a code-checked evidence gate (citations resolve in the snapshot), a support signal (blind-calibrated cluster support, used to order and flag, never as proof), and, for rows still contested, the evidence-validator re-read and the adversarial merge that the reflect legacy path already runs. A contested blocker that nobody has adjudicated is never dropped and never passes: it stays open, is counted in the headline, and the round cannot be PASS. The any-blocking union stays in the core as a named policy: the floor that applies when the adjudication stage is unavailable, and the policy for single-reviewer modules. The quorum for a panel verdict counts independent completions (complete state, distinct observed model ids, not single vendor), not dispatched reviewers, because the evidence shows that requested ids and served models diverge. B accepts that no measurement yet shows adjudication beating the union (UC row C-03); it claims the core should be built so that the policy is the thing measured, with `adjudicated` as the default for panels, and the union as the baseline arm.

## 2. Design consequence for the shared core and the named modules

### 2.1 Shared core

1. A verdict-policy interface in the core: `policy(rows, panel_state, adjudication) -> verdict`, with two named policies, `union` (today's rule, unchanged) and `adjudicated` (default when `reviewers_resolved >= 2`). The verdict is derived from rows on every read (decided fact D-13; both positions share it).
2. Per-row adjudication record on blocking rows: `evidence_gate` (pass, fail, skipped), `support` (the existing cluster value or None), `adjudication` (confirmed, rejected, pending), and the observed model id of the adjudicator. The record carries ids, enums and numbers only (INV-H). Rows are additive optional keys in `review-ledger/1`.
3. Row semantics: `confirmed` blockers drive FAIL/REVISE and the Reviser brief; `rejected` is allowed only for a deterministic evidence failure or a validator re-read that quotes the cited lines, and is itself recorded and counted; `pending` and `uncalibrated` blockers stay open, count in the headline (the owner counting rule already shipped in the variant ledger, r03 section 4.1 [UNVERIFIED]), and block PASS. Nothing is dropped.
4. Round outcome: PASS only with quorum met, zero confirmed blockers and zero pending ones. If the adjudication stage is down, the policy falls back to `union` and the outcome is the DEGRADED-style state, never PASS (the reflect map already degrades when the evidence validator is missing, `contract.py:31-33, 274-275` [CODE-VERIFIED]).
5. Quorum as a verdict precondition computed from recorded completion states (`manifest.py:52`, `reviewers_complete` at `manifest.py:20-21, 269-274` [CODE-VERIFIED]) and from served model ids (`model_observed` from the transcript is a decided requirement, C-08 decided parts [UNVERIFIED]); the default mirrors the Tier-2 gate that already exists: at least 2 complete reviewers, at least 2 distinct model ids, not single vendor unless the flag is set (`fallback.py:75-82`, `contract.py:282-288` [CODE-VERIFIED]).
6. The calibration channel stays separate from the reviewer line: a reviewer cannot self-calibrate (`findings_v2.py:96-97` rejects `calibrated_confidence` [CODE-VERIFIED]); the core receives a `calibration_map` keyed by finding id (`cluster.py:12-13` [CODE-VERIFIED]).

### 2.2 Named modules

| Module | Consequence under B |
|---|---|
| Spec review loop (CLI ledger, E2 tools) | `review merge` grammar, exit codes 0/10/11 and the `ledger` group unchanged. First reviews with 3 to 4 reviewers use `adjudicated`; a single-reviewer re-review (all 8 packaged templates carry `apply_to: ["first"]`, r03 section 1.1 [UNVERIFIED]) uses `union`. Pins that assert the fail-open behaviour are rewritten with the change (both positions share this). |
| Reflect (UC-1, UC-2, wrapper) | Keeps its calibrator, validator and adversarial merge as the adjudication stage; `derive_verdict` stays the shell (19 fields, 36 tests); `confidence_calibrated`, `evidence_validator_ran`, `reviewer_cards`, `calibrator_diversity` stay populated by the core stage and not by prose alone. |
| Tasklist and workflow | Unchanged entry through reflect; advisory at generation, blocking at the execution gate (C-05 is a separate slot). |
| PR review | Adjudication decides which findings enter `verify` and `push`; findings the evidence gate rejects (citation not in the diff, quote not found) never reach a fix round; `pr_submit.Finding`, `Severity` and the FSM untouched (INV-E). |
| rf-qa replacement | The panel gains the confidence output mode that C-11 position A already assumes; it comes from `support` and the adjudication record and not from a number nothing reads (see 3, E2). |
| `/sc:implement` QA | Single reviewer; `union` policy, exempt by rule S4 (r12 section 2 [UNVERIFIED]). |

### 2.3 What B takes from common ground and does not argue

Quorum over recorded completion states and a DEGRADED-style outcome for a partial panel (r03 I-2), derive-on-read (I-3), `defer` that cannot rewrite a verdict (I-4), refusal after ESCALATE (I-6), and rewriting the pins with the fix (I-7) are decided by reproduced evidence (synth-06 VM-5, D-11, D-13) and are assumed here. Per-row clearing is slot C-02 and is assumed independent of this proposal.

## 3. Evidence

### 3.1 What the code does today (the case against the raw union as a panel default)

| # | Claim | Source | Tag |
|---|---|---|---|
| E1 | The round verdict is FAIL if and only if some row is `blocking` and `open` or `regressed`; `blocking` is the value the reviewer typed. No other input reaches `_brief_ids` or `_decision`. | `src/superclaude/cli/review/ledger.py:93-104` | [CODE-VERIFIED] |
| E2 | `_confidence` computes `overlap` or `single` for each row from the reviewers who matched it in one round, and neither `_decision` nor `_brief_ids` reads it. FX-10's "rendered and never read" is therefore a fact: the support signal exists and is dropped. | `ledger.py:86-90, 93-104` | [CODE-VERIFIED] |
| E3 | The only refusal is at zero valid blocks; one valid block of N is enough, and the invalid reviewers produce a warning. Pinned as intended by `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported`. | `ledger.py:150-157`; `tests/review/test_review_ledger.py:376-385` | [CODE-VERIFIED] |
| E4 | Reproduced: 1 valid empty block of 4 dispatched reviewers gives PASS and exit 0; a reviewer-typed CRITICAL with `blocking: false` gives PASS; the reviewer's own `verdict:` line is ignored. | r03 section 1.2 (D-2) | [UNVERIFIED] (reproduced there by execution, not re-run here) |
| E5 | The v2 kernel already computes calibrated per-cluster `support`, a `disputed` flag (support below 0.5, or members disagree on blocking, or two deviation classes) and `cluster_agreement`, and the manifest already has the stages `calibrated`, `clustered`, `debated`, `validated`. `ledger.py` does not use any of them; within `cli/review` only `cluster.py` and `cluster_cmd.py` contain `disputed` or `cluster_agreement` (Grep of `src/superclaude`). The kernel is dormant (shadow mode), so the policy slot it was built for is empty. | `cluster.py:35-52`; `manifest.py:3-6, 39-49` | [CODE-VERIFIED] |
| E6 | `cluster.py` treats a cluster as blocking when `blocking_any` is true. The kernel's own default is also an any-blocking union at cluster level; what it adds is the `disputed` and `support` fields next to it. B uses those fields; it does not change the union at cluster level. | `cluster.py:46-49` | [CODE-VERIFIED] |
| E7 | The reflect verdict that ships in production is not a union. `derive_verdict` DEGRADES when the evidence validator is among the degraded components, when the adversarial merge is unavailable, on single-reviewer fallback, on a null convergence score, and when convergence is below 0.80; the 36-test matrix pins it. | `src/superclaude/cli/reflect/contract.py:31-33, 274-275, 291-300, 317-326`; `tests/cli/reflect/test_verdict_mapping.py` (36 `def test_`) | [CODE-VERIFIED] |
| E8 | The production Tier-2 path of `superclaude reflect run` is the swarm engine whose verdict is derived from the adversarial child's convergence score; the skill panel is reached through `/sc:reflect`. Both multi-reviewer reflect paths derive the verdict from a merge step, not from the union of reviewer flags. The only union consumer is the CLI ledger, which for re-reviews resolves one reviewer. | r06 sections 2, 4.1, 7 | [UNVERIFIED] (read there; `runner.py:538-545` not re-read here) |
| E9 | The reflect skill makes blind calibration and the evidence validator part of the verdict path: blind re-grade "so the merged verdict weights calibrated scores"; the validator is a "non-negotiable final gate" that re-Reads every cited line and drops unfounded items; consumers read the output (`sc-task` end-of-task hook marks a task done on `status: success AND confidence_calibrated >= 0.85`). | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:34, 631, 635, 999` | [CODE-VERIFIED] (the sentences exist at those lines; whether an orchestrator obeys them is measured only by shadow evidence) |
| E10 | The 1.8.0 stable field list carries `confidence_calibrated`, `evidence_validator_ran`, `reviewer_cards` and `calibrator_diversity`. A core whose default verdict path never produces them leaves four consumer-read names fed by prose only. | `src/superclaude/cli/reflect/panel_lint.py:40, 100, 102, 110` | [CODE-VERIFIED] |
| E11 | A Tier-2 gate computed from served model ids already exists: `QuorumState(reviewer_count, model_class_diversity, vendor_diversity, satisfies_tier2)`, and `derive_verdict` degrades on diversity that is not full and on single vendor. | `src/superclaude/cli/reflect/fallback.py:75-82`; `contract.py:281-288` | [CODE-VERIFIED] |

### 3.2 What the measured runs show (and do not show)

| # | Claim | Source | Tag |
|---|---|---|---|
| E12 | E2 families of 3 to 5 reviewers produced wrong blockers per run of 1.83 (sonnet + 2 luna, ember + 2 luna), 2.00 (sonnet + luna + ember) and 3.50 (the 5-reviewer h2 panel), against real blocking of 0.17 to 0.33, all under the any-blocking merge. The pilot arms gave 0, 1 and 3 wrong blockers and 0 of 8 real blocking in every arm. Caveat that cuts against B: a true novel defect scores as a wrong blocker, so these are upper bounds on false positives. | r08 sections 1, 4, 7 (G1); `PR:79` as cited there | [UNVERIFIED] |
| E13 | The E2 judge's blocking credit exceeded the implement-blocking ground truth: 65 judge-blocking catches against 38 real blocking over 71 valid rows. Reviewer rows flagged blocking are not reliably blocking in implementation. | r08 section 7 (G4) | [UNVERIFIED] |
| E14 | Real-blocking recall was at most 3 of 8 for any family and 0 of 8 in the pilot; no gate-accuracy measurement and no multi-round ledger exist. A union has not been shown to buy blocker recall either. | r08 section 7 points 3, 4 | [UNVERIFIED] |
| E15 | Overlap between reviewers is low: 13 of 216 clusters had two or more reviewers (7 unchained) in 15 combo runs, and 7 of those 15 runs resolved no citations at all because of a snapshot-path fault. | r07 E1-F9, E1-F10 | [UNVERIFIED] |
| E16 | Calibration can silently collapse: the calibrator was dispatched without a class in 6 of 15 combo runs, and the contract reported `calibrator_diversity: full` while every agent served one model (A3). Requested and served ids diverge (haiku slot served by `gpt-6.1-sol` in 5 runs). | r07 E1-F5, E1-F6, E1-F7 | [UNVERIFIED] |
| E17 | E1 scored no policy and E2 scored only any-blocking merges; the debate was never compared with the union (UC row C-03, s05 section 6.4 axis status). | UC:20; s05:322 | [UNVERIFIED] |

### 3.3 External evidence (context, transfer to PR review unverified)

All rows from `web-01`, read there through search excerpts; none is verified against code here. Tag: [UNVERIFIED] for all.

- Agreement is weak proof: nine judges from seven families carried about two independent votes, and the best single judge matched or beat the panel (B3). So B does not use k-of-n agreement or weighted votes as the validity test; it uses agreement to order the adjudication queue (web-01 recommendation 3).
- A mechanical citation-overlap check flagged about 8% of responses as hallucinated, with 97% of the sampled flags genuine; a passing check proves only that the cited code was in context (G1). B uses it as the evidence gate and as nothing more.
- Debate adds little over voting on benchmark questions (C1). B therefore keeps debate for contested blocking rows only, not for every finding.
- Union raised recall in SWR-Bench (D1) while a 2-of-3 filter that discards single-reviewer findings is used to build a golden set (D3). B follows web-01 recommendation 5: single-reviewer findings are kept as unconfirmed, never discarded.
- Weighted or dependence-aware aggregation needs labelled data (F3). B ships no weighting formula in the default; the gate rules are evidence-based, and support only orders and flags.

## 4. Invariants

### Preserved

| Invariant | How B keeps it |
|---|---|
| Contract 1.8.0 byte-identical (INV-A) | No field renamed or added to the stable lists. The four adjudication-fed names (E10) become populated by the core stage; `merge_method` stays `adversarial` or `single-reviewer-fallback`. |
| 36-test verdict matrix and `derive_verdict` (INV-B) | The function and its 19 inputs are untouched. Adjudication failures reach it through fields it already reads (`degraded_components` with `evidence-validator`, `adversarial_unavailable`, `adversarial_subrun_status`), which E7 shows are already degrade triggers. |
| Fail-closed (INV-I) | An unadjudicated blocker blocks PASS; an unavailable adjudication stage degrades; zero valid blocks still refuses; a rejected row needs a deterministic failure or a quoted re-read. |
| Shadow changes no verdict; legacy debate authoritative (INV-L) | The legacy calibrator, validator and debate are the adjudication stage; B reuses them and makes them callable from the core. No verdict changes until a stage that promotes the engine. |
| findings-v1 grammar, `review merge`, `ledger` group, exit codes (INV-C, INV-D) | Row keys are additive and optional; `merge` and `ledger verdict` keep their exit contract (0, 10, 11). |
| No document text in telemetry (INV-H) | The adjudication record holds ids, enums and numbers. |

### Endangered

| Invariant | Severity | Exposure and what B must do |
|---|---|---|
| Fail-closed (INV-I) | HIGH | A buggy adjudicator that rejects a true blocker is a new fail-open path, the exact class of defect B criticises in the union. B must restrict `rejected` to deterministic evidence failures or a quoted re-read, record every rejection, and report rejections per run. |
| Repo rule S1-S5, binary blocking (INV-J) | MEDIUM | `pending` and `unconfirmed` must stay a row status and never become a third severity token or a Medium-like tier (r12 sections 2, 8). |
| Reviewers blind and read-only (INV-G) | MEDIUM | The adjudicator and the debate step are further agents; they must be mechanically read-only. `evidence-validator` has Read, Grep and Glob only; the debate's merge executor is write-capable and must not run inside the adjudication stage. |
| Shadow changes no verdict (INV-L) | MEDIUM | Making `adjudicated` the default for a panel in a non-reflect module changes a verdict that ships today (the spec loop). That is a behaviour change for an existing consumer, not shadow work. |
| Telemetry without document text (INV-H) | LOW | Validator quotes must stay out of the adjudication record. |

## 5. The test or measurement that would show it right or wrong

The policy is the measured variable; reviewer outputs are stored once and every policy is applied to the same outputs, so the added spend is the adjudication stage only.

1. Offline replay on committed data, no model calls. Apply `union` (as shipped) and a rule set that marks a blocking row contested when it is single-reviewer, has no resolved anchor (r08 G13: 46 span-null rows, 13 blocking [UNVERIFIED]) or is flagged by the code gate. Score both against the E2 ground truth: real blocking recall out of 8, wrong blockers per run, control found, and a TPR/FPR/Youden's J per rule as in F1. The score tables reproduce from committed `score.json` and ledgers after patching five hard-coded paths (r08 section 4 [UNVERIFIED]). Limit: E2 holds no calibrator, validator or debate output, and raw transcripts are not committed, so this replay measures only how many blocking rows would be contested, not how they would be adjudicated.
2. A run that adds the adjudication stage. Use the E1 seeded-defect design that was never run (60 seeded defects; `pilot-design.md` as cited in r07 N-3 [UNVERIFIED]) or the E2 packages with held-out defects. Run `union` and `adjudicated` on the same stored reviewer outputs. Pre-commit the decision rule before the first run (the Tier Q rule of slot X-14).
3. A regression gate that needs no model: `uv run pytest tests/cli/reflect/test_verdict_mapping.py` stays green, and `scripts/reflect_verdict_replay.py` still replays the 42 recorded legacy contracts with no difference (r06 section 0 [UNVERIFIED]).
4. A served-model check inside the run: the adjudicator's `model_observed` must differ from the reviewers' served models in every run; a run where it does not is recorded as not independently adjudicated.

B is shown right if the adjudicated policy lowers wrong blockers per run with no loss of real-blocking recall, and if the contested rows per round are few enough for one batched validator call (E12 puts blocking rows at roughly 2 to 4 per defect-rich run [UNVERIFIED]).

B is shown wrong if (a) the stage confirms essentially every contested blocker, so it only adds cost; or (b) it rejects any real-blocking item, which is the fail-open case; or (c) the adjudicator was served by a reviewer's model in a material share of runs, as the calibrator was in 6 of 15 (E16); or (d) the contested set is so large that the validator becomes the verdict and its own error rate dominates.

## 6. Effect on future PR code review and rf-qa replacement

- PR review. The PR flow ignores the panel verdict; only findings enter (s05:320, citing r13 P12 [UNVERIFIED]). A verdict policy therefore matters to PR review through the finding set: under B, findings that fail the code gate or the validator re-read are rejected before `verify`, `troubleshoot` and `push`, and unconfirmed ones enter with a flag. The wire-format choice stays slot C-10. A `union` default would pass every reviewer-typed blocking row into the fix rounds of the push FSM, whose cap is set by pr-submit.
- rf-qa replacement. rf-qa has a confidence gate and lens floors that no test pins, and it needs regression and monotonicity halts (UC row C-11; s05:320 [UNVERIFIED]). A union default exposes no value for a confidence gate (E2: `confidence` is computed and never read). B exposes `support`, `disputed` and the adjudication record as the inputs for that gate and for the monotonicity check (a row that returns after being confirmed resolved). Halts stay additive in both positions.
- Limit on claims. A union of four automated reviewers passed 41.5% of tests built from human reviews (web-01 D4 [UNVERIFIED]); neither policy supports describing the panel as a full replacement for human or test-based review.

## 7. The strongest objection to B, and the answer

Objection. No measurement shows adjudication beating the union. The literature says debate is about as good as voting (C1), model votes are correlated (B3), the best single judge matches the panel, and weighted aggregation needs labels that do not exist (F3). The union is the only rule that assumes nothing about reviewer reliability, and external work found it raises recall (D1). The data shows low overlap (E15), so almost every blocker is single-reviewer and contested; the validator then becomes the de facto verdict-maker, at added cost and with its own fail-open surface. The calibration channel already failed silently in 6 of 15 runs (E16), the calibrator agent is shaped for troubleshoot with six dimensions while reflect expects a five-dimension mean, and the capability-ordering file it needs does not exist (r17 DR-062, DR-137 [UNVERIFIED]). Adding a calibrator to the default core imports those defects into every module.

Answer. First, B does not use agreement or weights as proof; the objection's two strongest sources (B3, F3) argue against a weighted vote, which B does not ship. The gates are evidence checks: a code check that the cited location resolves, and a validator that re-reads the cited lines. Both are verification that is not another model vote, the thing web-01 recommends (recommendation 3) and the thing the reflect skill already declares non-negotiable (E9). Second, nothing is discarded: contested rows stay open and counted, which is web-01's recommendation 5, so the recall that D1 reports is kept. Third, the stage runs on blocking rows only, which E12 puts at a handful per run, so the validator does not carry the whole review. Fourth, the union is kept as the named baseline arm and the fallback, so the claim is falsifiable by the test in section 5 and its failure conditions (a) to (d) are stated in advance. Fifth, the calibrator defects are defects of one legacy agent and of how its class was dispatched; the core's contract is a `calibration_map` per finding id (`cluster.py:12-13`) plus an observed-model check, which is the decided C-08 requirement, so the independence failure becomes visible in the record instead of silent. B does not claim the calibrator agent is correct as shipped; it claims the slot for it should exist in the core, because the production reflect verdict and four consumer-read contract fields already depend on it (E7, E9, E10).

What the evidence does not support for B, stated plainly: no run compares any policy against ground truth (E17); real-blocking recall is low under the union (E14) and has not been shown higher under adjudication; and every external result is on QA, NLI or SQL, not on finding-set review.

Status: Complete
