# Proposal A: slot C-03 (merge-verdict-policy-and-quorum)

Status: In Progress
Position: A (deterministic any-blocking union as the default, pluggable policy, quorum over recorded completion states, DEGRADED-style outcome for a partial panel, no calibrator in the default)
Conflict IDs: C-S4, VM-5, FX-9, FX-10
Written against: repo `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`, branch `ironbelly/shadow-runs`
Tags: [CODE-VERIFIED] = I read the cited line in this session; [CODE-CONTRADICTED] = the code says otherwise; [UNVERIFIED] = taken from a research file or document and not re-derived here (the source is named).

## 1. The position in one paragraph

The shared core computes the round outcome as a pure, deterministic function of three recorded things: the ledger rows (is any row blocking and open or regressed), the per-reviewer completion states (how many reviewers of those requested actually completed), and the policy named by the module. The default policy is the any-blocking union: a finding that any complete reviewer types as blocking enters the ledger and fails the round, whatever the other reviewers say, and single-reviewer findings are kept and marked unconfirmed, never discarded. Quorum is a rule about coverage, not about agreement: a round whose complete reviewers fall below the profile's minimum yields a DEGRADED-style outcome and never PASS, so "a review that did not happen never certifies PASS" (INV-I) holds at every panel size and not only at zero valid blocks. No calibrator, debate or grader sits in the default path; calibrated confidence stays an optional input that is displayed and never gates. The merge policy is pluggable, so reflect's legacy calibrate-validate-debate chain (and any later k-of-n or calibrated policy) is a named policy of its module, not a fork of the core.

## 2. Design consequence for the shared core and the named modules

### 2.1 Core

- One pure function in the core (illustrative name `derive_panel_outcome`), a sibling of `ledger._brief_ids`/`_decision`, taking `(rows, completion_records, policy)` and returning one of PASS, REVISE, ESCALATE, DEGRADED with a reason slug. It is derived on every read and never stored (this part is decided, synth-06 VM-3: the stored verdict is stale after `revise`, `ledger.py:363-372` [CODE-VERIFIED]).
- Completion records: one per requested reviewer, state from the existing vocabulary `COMPLETION_STATES = ("complete", "truncated", "invalid", "failed", "timed_out")` (`findings_v2.py:40` [CODE-VERIFIED]; research/03 section 1.2 had this as [UNVERIFIED], now verified). The manifest already counts `reviewers_requested`, `reviewers_resolved` and `reviewers_complete` from the latest collected-stage attempt per reviewer (`manifest.py:20-22`, `_recount` at `:269-274` [CODE-VERIFIED]). `ledger.merge_round` never reads the manifest: it takes only `reviewers` dicts (`ledger.py:107-149` [CODE-VERIFIED]; research/03 section 1.2 adds the negative grep for `manifest|reviewers_complete` over `ledger.py`). The round entry gains `requested`, `resolved` and a per-reviewer `completion`; `ledger.load` checks only the schema string (`ledger.py:47-48` [CODE-VERIFIED]), so additive keys do not break `review-ledger/1` readers.
- Quorum is data, not code: a profile field `min_complete` plus a `shortfall` mode of `degrade` (below `min_complete` gives DEGRADED) or `visible` (record the shortfall, leave the verdict alone). The code gives no quorum value (research/03 gap 6 [UNVERIFIED here]), so this proposal takes the one rule the repo already enforces as the floor: at least 2 complete reviewers when 2 or more were requested (`tier_reached = 2 if reviewer_count >= 2`, `merge_method = "single-reviewer-fallback"` below that, `ensemble.py:772-773` [CODE-VERIFIED]; the single-reviewer fallback already DEGRADES, `contract.py:294-296` [CODE-VERIFIED]). Whether the right floor is 2-of-3, majority or all is not decided by any evidence and is a measured parameter (section 5).
- Policy registry: `union` (default), `legacy-adversarial` (wraps the reflect chain, section 2.2), and room for `agree-k` or `calibrated` as added policies. Adding one changes no core signature.
- Reviewer-typed `blocking` is the per-finding input; which rule makes a finding blocking stays a per-lens module property (decided part of C-S3: MINOR is never blocking, `findings.py:100-101`, `findings_v2.py:161-162` as cited in synth-06 [UNVERIFIED here beyond `findings.py:100-101` via research/03]). This proposal does not decide who types `blocking` (that is slot C-02).
- Single-reviewer findings are not dropped. `cluster_v2` already computes `blocking_any`, `blocking_all`, `disputed` and `cluster_agreement` per cluster (`cluster.py:345-377`, `:403-412` [CODE-VERIFIED]); under this position they are display fields (unconfirmed versus confirmed), not verdict inputs.

### 2.2 Named modules

- Spec-review module (the `/sc:spec-panel` loop, `superclaude review merge` and `ledger`): policy `union`, `shortfall: degrade`. The merge keeps its `LedgerError` refusal at zero valid blocks (`ledger.py:150-157` [CODE-VERIFIED]) and adds the partial case; the one-valid-of-three PASS (D-2) becomes DEGRADED.
- Reflect module: policy `legacy-adversarial` stays authoritative, `shortfall: visible`. This is forced by verified code, not by preference: the 2-of-3 shortfall is deliberately PASS-eligible (FR-RH2.9; `ensemble.py:755-770`), pinned by `test_i3_partial_two_of_three_distinct_pass_eligible` (`tests/cli/reflect/test_ensemble_stub_integration.py:199-221`) and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` (`tests/cli/reflect/test_verdict_mapping.py:572-591`) [CODE-VERIFIED]. The code comment records verdict-degrade-on-shortfall as a deferred `needs_human_decision` (`ensemble.py:762-764`) [CODE-VERIFIED for the comment; the named decision file `fx7-degrade-on-reviewer-shortfall-DECISION.md` is not tracked in git outside `.dev/tasks/` (checked with `git ls-files`), [UNVERIFIED] whether it exists]. `derive_verdict` is not touched. The union verdict runs in shadow beside the legacy chain until a measurement exists (INV-L). Note for the debate: the slot summary says "a DEGRADED-style outcome (never PASS) for a partial panel"; for the reflect profile that sentence is [CODE-CONTRADICTED] by the pins above, so it holds only for modules that opt into `shortfall: degrade`.
- Tasklist and workflow (via reflect UC-1): unchanged; they read reflect's exit codes 0/10/11/2.
- Future PR-review module: policy `union`, findings only. The PR flow has no reviewer verdict today (research/13 P12 and the Output Contract at `pr-submit` SKILL.md l.52-61: `findings_count`, `dropped_count`, `pr_review_url`, no verdict field [UNVERIFIED here]), so the panel verdict is ignored and the union supplies the complete finding set.
- Future rf-qa replacement: policy `union` plus the regression and monotonicity halts as additive guards (research/13 R7 [UNVERIFIED here]).

### 2.3 Exit codes

`ledger verdict` maps decision to exit 0 PASS, 10 REVISE, 11 ESCALATE (`ledger_cmd.py:13` [CODE-VERIFIED]); reflect maps 0 PASS, 10 HALTED, 11 DEGRADED, 2 BLOCKED (`models.py:38-49` [CODE-VERIFIED]). The same numbers mean different things in the two products. This position adds DEGRADED to the ledger as a new, additive exit code that does not reuse 10 or 11, so the pinned 0/10/11 mapping (INV-D; `tests/review/test_review_cli.py:245, 349, 369` assert exit 10, 0 and 11 [CODE-VERIFIED]) is unchanged. Any non-zero code is non-PASS for a script, so an old caller fails closed on the new code.

## 3. Evidence

### 3.1 What the code does today (the defects the position fixes)

1. One valid block of N passes. `merge_round` refuses only when `not any(block_ok.values())` (`ledger.py:150-157`); otherwise `verdict = "FAIL" if brief else "PASS"` (`:273-275`) [CODE-VERIFIED]. Reproduced in research/03 section 1.2: four dispatched, one valid empty block, three broken gives PASS, exit 0, and the round record has only the keys `brief_ids, decision, doc_sha256, n, reviewers, verdict`, no quorum or completion key [CODE-VERIFIED by execution in that report; I re-read the code and did not re-run the script]. Pinned as intended by `tests/review/test_review_ledger.py:376-385`, `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` [CODE-VERIFIED by research/03; the name is quoted from it].
2. The union half is already the shipped rule and is sound where it fires. A row is in the brief when `blocking` and status `open` or `regressed` (`ledger.py:99-104`); the verdict is FAIL when the brief is non-empty (`:273-275`); `confidence` is computed (`:86-90`) and never read by `_decision` or `_brief_ids` (`:93-104`) [CODE-VERIFIED]. One reviewer's blocking flag fails the round however many others are silent (research/03 reproduction D-2 D [UNVERIFIED here, reproduced there]).
3. The partial-panel concept is half built. The manifest counts complete reviewers (`manifest.py:269-274`); `cluster_v2` already separates `complete_reviewers` from `invalid_reviewers`, returns `valid_blocks` (`cluster.py:386, 414-418`) and sets `cluster_agreement` to None below 2 complete reviewers (`:405-406`) [CODE-VERIFIED]. Nothing converts the count into an outcome.
4. Reflect already has the outcome this position wants as a state, DEGRADED, with 14 triggers (`contract.py:263-358`), including single-reviewer fallback (`:294-296`) [CODE-VERIFIED]. It reads orchestrator-typed contract fields, not ledger rows, and engine A fills several of them by default: `merge_method` by reviewer count (`ensemble.py:773`), zero deviation counts (`:779-785`) [CODE-VERIFIED]. So a PASS on that path rests on defaults, which is why this proposal does not feed ledger rows into `derive_verdict`.

### 3.2 What is known about the alternatives' machinery (stated, not weakened)

- Reflect's chain does calibrate, validate and debate, and that capability is not lost: it stays as the `legacy-adversarial` policy. What is unmeasured is whether it improves the verdict. E1 scored no run for quality (research/07 N-1: "No quality measurement" [UNVERIFIED here]); the calibrator was dispatched without a class in 6 of 15 combo runs and silently took the sonnet alias (research/07 E1-F5 [UNVERIFIED here, recounted from raw logs in that report]); contract diversity telemetry cannot see the served model (E1-F7 [UNVERIFIED here]). So a calibrated confidence as shipped is not a validated filter.
- E2 scored only any-blocking merges, with a judge whose "blocking" overstates (65 judge-blocking versus 38 real blocking over 71 valid rows, research/08 G4 [UNVERIFIED here, RECOMPUTED in that report]); wrong blockers per row 1.83 to 3.50 per family (research/08 line 60 via synth-06 C-S4 [UNVERIFIED here]). This is the cost side of the union and it is stated as a cost in section 7.
- The merge lost blocking findings before any policy ran: 92 findings (49 blocking) dropped in 80 reviewer runs flipped 3 verdicts FAIL to PASS (research/08 G5, `audit-D/summary.md` [UNVERIFIED here, RECOMPUTED in that report]). A union over what survives parsing is only as good as the repair policy of slot C-06; the completion state `truncated` or `invalid` is where that loss becomes visible to quorum (section 2.1).

### 3.3 External evidence (context only; transfer to code review is [UNVERIFIED] for every item)

- Aggregating independent reviews raised recall substantially on SWR-Bench; overlap between reviewers is low (arXiv 2509.01494; research/web-01 D1) [UNVERIFIED: preprint; the aggregation there uses an LLM call].
- Majority voting over independent answers accounts for most of the gain credited to multi-agent debate (NeurIPS 2025, arXiv 2508.17536; web-01 C1) [UNVERIFIED: single-answer NLP tasks, not finding sets].
- Nine judges from seven model families carried about two independent votes, so "k of n agree" is weaker evidence than it looks (arXiv 2605.29800; web-01 B3) [UNVERIFIED: NLI tasks, not code review].
- Opposed practice exists: a 2-of-3 filter that discards single-reviewer findings builds a golden set (entelligence.ai code-review benchmark; web-01 D3) [UNVERIFIED: vendor blog]; strict unanimity cut false accepts on SQL correctness (arXiv 2602.18492; web-01 F1) [UNVERIFIED]. No peer-reviewed study compares quorum rules on findings with ground truth (web-01 discrepancies). None of this decides the question; it shows the union is a defensible default and that discarding single-reviewer findings is a different design.

## 4. Invariants

### 4.1 Preserved

- Contract 1.8.0 byte-identical (INV-A): no change to `contract.py`, `models.py`, the 110 stable plus 27 telemetry names or the `merge_method` pair. The new outcome lives in the review package, not in the reflect contract.
- 36-test verdict matrix (INV-B): `derive_verdict` and `tests/cli/reflect/test_verdict_mapping.py` (36 `def test_` lines, counted by grep [CODE-VERIFIED]) are untouched; the reflect module keeps `shortfall: visible`, so `test_i3` and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` stay green by construction.
- Fail-closed (INV-I): strengthened from the zero-valid boundary to every panel size. No assignment of reviewers below `min_complete` yields PASS in a `degrade` profile.
- Shadow changes no verdict (INV-L): the union runs beside the legacy chain in reflect; legacy and the Wave 4 debate stay authoritative.
- `review-ledger/1` and the `ledger` command group (INV-D): additive round keys only (`ledger.load` checks the schema string alone, `ledger.py:47-48`); exit 0/10/11 unchanged, DEGRADED is a new code.
- findings-v1 grammar and `review merge` (INV-C): untouched; the change is in the merge result, not the parser.
- Repo rule S1-S5 (INV-J): `blocking` stays binary, MINOR never blocking, cap 2 fix cycles (3 reviews); no cap text changes. [UNVERIFIED] that no static test pins the one-valid-passes behaviour in primitive prose; research/12 section 2.1 lists only the cap and S1-S5 pins.
- Installed-path rule (INV-F) and `make sync-dev` / `verify-sync` (INV-K): the change is package code plus brief text; no primitive gains a `src/superclaude/...` path.

### 4.2 Endangered

- INV-D (HIGH if mishandled): the tests that encode the defects as intended behaviour must be rewritten with the fix, not deleted: `test_review_ledger.py:376-385` (one valid block is enough) directly; the D-1 family at `test_review_ledger.py:193-217` and `test_review_cli.py:274-292` belong to slot C-02 (research/03 section 2: 6 of 8 pins read assert defect behaviour [UNVERIFIED here, read in that report]).
- INV-B (MEDIUM): the exit numbers 10 and 11 carry different meanings in the ledger and in reflect; if a later step maps ledger DEGRADED onto 11 for tidiness, a script reading both products conflates ESCALATE and DEGRADED. Section 2.3 avoids it; the exposure is a later change, not this design.
- INV-A (MEDIUM): if the reflect profile were later switched to `shortfall: degrade`, that reverses FR-RH2.9 non-additively (`ensemble.py:762-764`); that switch is outside this proposal and would need its own decision.
- INV-L (HIGH if the union ever replaced the debate in reflect before measurement): this proposal keeps the debate authoritative, so the invariant holds only while that boundary is kept.

## 5. The test or measurement that would show it right or wrong

Code tests (decidable now):
1. Quorum matrix: for requested N in 1..5 and every assignment of the five completion states, assert the outcome is DEGRADED when `complete < min_complete` in a `degrade` profile, never PASS; PASS only when quorum is met and no blocking row is open. Seeded from research/03 reproduction D-2 A (4 requested, 1 valid, 3 broken), which must change from PASS to DEGRADED.
2. A property test: adding a failed or timed-out reviewer to a round never turns a non-PASS outcome into PASS (monotonic fail-closed).
3. Regression guards: `uv run pytest tests/cli/reflect/test_verdict_mapping.py` stays at 36 passing; `scripts/reflect_verdict_replay.py` stays at 0 differences over its 42 replayed runs (research/07 section 1 [UNVERIFIED here]; it is a self-replay by construction, so it shows non-interference only).

Measurement (not decidable from existing evidence; the position is wrong if this says so):
4. Replay the E2 merges and a seeded-defect set under three policies (`union`, 2-of-3 cluster support, calibrated) and report per policy: defects found, real blocking found, wrong blockers per row, control defects found, and the escalate-at-cap rate over 3 reviews. The E2 ground truth is 16 defects in 3 packages, 4 never caught, 3 carrying 89% of catches (research/08 ground-truth paragraph [UNVERIFIED here]); it is a derivation set, so a held-out package is required before any default is claimed. Pre-register the decision rule before the first run (web-01 recommends TPR and FPR per rule).
5. Falsifier for the default: if the union's wrong-blocker rate drives the escalate-at-cap rate materially above the 2-of-3 policy's on the held-out set, with no recall advantage, the default should change. Falsifier for the quorum floor: if `min_complete` = 2 of 3 leaves defect-miss rates indistinguishable from 3 of 3, the floor costs more than it protects.

## 6. Effect on future PR code review and rf-qa replacement

- PR review: the existing flow has no reviewer verdict (research/13 P12 [UNVERIFIED here]); only findings enter. The union's useful property there is that no single-reviewer blocking finding is lost. The PR module declares `union` and consumes findings through its adapter (slot C-10 decides the wire format; this proposal does not depend on it). A partial panel in a PR round is visible as DEGRADED and the module can re-dispatch, which fits the "one reviewer failed synthetic finding" idea (research/13 M8 [UNVERIFIED here]).
- rf-qa replacement: FX-9 says rf-qa fix loops need a quorum at re-review, and today a re-review resolves one reviewer because the packaged templates carry `apply_to: ["first"]` (`panel.py:189-196` validation and `:600` selection [CODE-VERIFIED for the code path; the count of 8 templates is research/03 section 1.1, [UNVERIFIED here]]). Under this position a declared single-reviewer re-review (`requested = 1`, `complete = 1`) meets quorum, while an intended 3-reviewer re-review that completes with 1 does not. Whether a re-review should run the full panel is slot C-02's question; this proposal only makes a shortfall visible instead of silent. The regression and monotonicity halts (`rf-qa.md` byte-exact strings, research/13 R7 [UNVERIFIED here]) are additive to the outcome function and do not conflict with it.
- Cost: the union needs no extra calls (no calibrator, no debate), so a PR round costs the reviewers only; the price is wrong-blocker triage, bounded by the 3-review cap.

## 7. Strongest objection and the answer

Objection: "FX-10: a weak model must not decide alone. Under the union, one reviewer's mistaken blocking flag fails the round; E2 shows wrong blockers in every family and a judge that overstates blocking, and the legacy chain exists to filter exactly this. Without a calibrator or an agreement quorum the panel will cry wolf, burn fix cycles on false blockers and escalate to a human at the cap on noise."

Answer, without weakening the objection:
- The costs are asymmetric and the repo rule already prices them. A wrong blocker costs at most one fix cycle and, at the cap, a human decision (S3: at most 2 fix cycles, then escalate with the open blocking findings; never pass open blocking findings, `pragmatic.md:227` as cited in research/12 section 2.1 [UNVERIFIED here]). A missed real blocker is a PASS on a defective document, which INV-I forbids. The union puts the cost on the side the rules treat as cheaper.
- The calibrator is not a validated filter today: no run was scored (research/07 N-1), it lost its class in 6 of 15 runs (E1-F5), and per-finding `confidence` in the ledger is rendered and never read (`ledger.py:86-90`, `:93-104`). Replacing an unmeasured filter by an unmeasured filter would add calls and a failure mode without evidence that it helps.
- The usual remedy, a k-of-n agreement filter, rests on voters whose errors are correlated (web-01 B3) and discards exactly the single-reviewer findings that gave the recall gain in SWR-Bench (D1). It is also a policy this design hosts, so adopting it later is a data change, not a rewrite.
- Agreement and verification are kept apart. The evidence gate (a code-backed check that each cited line exists; synth-06 CO-22 keeps both gates) stays in the pipeline and drops unfounded citations before the union; that is verification by code, not another vote.
- The proposal does not claim the union is right. It claims the union is the least-unmeasured default and that its failure shows up as one number (wrong blockers per row, section 5 item 4) against which any other policy can be swapped in by name.

Residual disagreement this proposal does not remove: whether a single-reviewer blocking row should stop a loop when every other reviewer found nothing at all is a product judgment, and the quorum floor (2-of-3, majority, all) is a parameter nobody has measured.

Status: Complete
