# Adjudication result: slot X-14 (eval-acceptance-and-harness-owner; synth-06 name C-14)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the diff analyst, both advocates (Round 1 and Round 2), the fault-finder, the two scorers, the re-evaluator, the plan reviewer and the merge-executor were separate agents. Conflict row: X-14 in `phase-outputs/discovery/undecidable-conflicts.md` (conflict rows CO-15, CO-16, CO-17; context rows FX-17, FX-18; invariants at stake INV-F HIGH, INV-H MEDIUM, INV-K MEDIUM).

## Winner

**Variant A (Proposal A) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`adversarial/base-selection.md`): "Selected Base: Variant A (Proposal A; `variant-1-original.md`)". The merged result is `merged-output.md`: Proposal A's three acceptance tiers, metric of record and tested `scripts/` plus `tests/` set, with Proposal A's kernel `superclaude review verify-run` command and its two ledger-entry additions removed (Advocate A withdrew both in Round 2), and with Proposal B's procedure items added (the two reflect-gate repairs and the gate-bite test, the offline metric-discrimination test, tasklist-review coverage, the status wording, the concessions). In the merged text the verifier is a script in the tested set, the kernel is read and never written, and a kernel command is "deferred, not rejected".

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: A 0.9980, B 0.9787 (requirement coverage 1.0000 each; internal consistency A 0.9921, B 0.9815; specificity 1.0000 each; dependency completeness 1.0000 each; section coverage A 1.0000, B 0.8889). The scorer noted that requirement coverage, specificity and dependency completeness saturate for both variants, so the quantitative layer separates them only through internal consistency and section coverage.
- Qualitative layer (30 criteria, two position-bias passes, 4 of 60 criterion-variant pairs disagreed and were re-evaluated): A 25/30 = 0.8333, B 25/30 = 0.8333. Dimensions: Correctness A 3/5, B 2/5; Risk Coverage A 3/5, B 4/5; Completeness 5/5 each; Structure 5/5 each; Clarity 4/5 each; Invariant & Edge Case Coverage 5/5 each (the edge-case floor is met by both). The re-evaluation sided with pass 1 on all four pairs: final verdicts changed from pass 1: 0.
- Combined: A 0.9157, B 0.9060. "Margin: 0.0097 (0.97%) (below the 5% threshold)". "Tiebreaker applied: Yes". Level 1 (debate performance): A won 11 points, B 9, 20 were agreed ties and 4 are unresolved (A leads 55% to 45% of decided points, or 25.0% to 20.5% of all 44). Level 2 (correctness criteria met): A 3, B 2. "Both readings select Variant A, so the selection does not depend on which denominator is used."
- The debate's stated reasons for the base: A won the points that decide a base for this slot (the metric of record, tested placement, the tiers, the integrity checks); B won the points on the kernel command and its inputs, the repaired reflect gate, module coverage and the fuller severity reading; the convergence is a hybrid whose backbone is A's, so taking A as the base and applying B's contributions is the smaller edit.
- Honest limits stated in the base selection: the qualitative totals tie and the margin is 0.97%, so the base is selected by the tiebreaker and not by a wide gap; both variants contain statements the debate found false (Correctness K1 NOT MET for both). A's: "a silent swap passes `model_ok`" (the swap is logged), the per-reviewer counts that `parse_block` "already returns" (it returns none), "no served-model field" (declared in `telemetry.py:49`, no writer). B's: "89 test files, so fixable in place" (28 of 89 belong to designs whose code is absent from git at the study tip), "the same three easy catches inside it" (GT7 is not blocking in implement), "the manifest cannot hold `model_observed`".
- Convergence: 40 of 44 diff points agreed (90.9%; Round 1 was 28 of 44, 63.6%; counting only the 24 points where at least one advocate named a winner, 20 of 24 = 83.3%) against an 80% threshold. Status BLOCKED_BY_INVARIANTS (see the unaddressed invariants below). Scoring Matrix tally: A wins 11, B wins 9, 20 agreed ties, 4 unresolved (C-005, C-007, C-008, X-004).

## Conditions under which the winner holds (all stated in `merged-output.md`)

1. The acceptance status wording: a use case is "accepted" only with Tier S, a pre-registered Tier Q and Tier G; with Tier S and Tier Q only it is "not worse on what is pinned, lead only". Building and shadow runs are not held up. Both advocates accepted this wording; it is an owner definition with no code falsifier. Tier G is unbuilt, not unbuildable (a candidate package pool exists, `PILOT-REPORT.md:83`); who writes and who pays for it is open.
2. E1 and E2 are one evidence family and the 16-item ground truth is a derivation set, so every Tier Q number is a lead until Tier G exists.
3. The kernel `verify-run` command is deferred, not rejected. The flip condition both advocates named: a kernel command is the better design if a skill or command must run an identity or completeness check inside a run, or if slot C-08 lands a served-model record by default together with a consumer of the `flag` path. The present half is verified (no caller was found); the future half is not.
4. The metric of record is reported per item, with unmatched blocking rows (not "wrong blockers") until a blind adjudication of those rows on a sample exists. The any-severity count and the control wrong-blocker ceiling are secondary columns and gate nothing at pilot n (the pilot margin was one item of ten). The rule states a minimum detectable effect and the comparison count, and "no evidence" is a valid output; the pilot's blocking recall was 0 of 8 in every arm and 81 of the 89 blocking-in-implement catches sit on two items, so at pilot n the metric's value is its guard rails.
5. Timing: the rule, analysis script and values file are committed after slot C-02 lands and before the first run commit; the offline discrimination test (M-7) runs first on the 71 stored rows and is re-run after C-02 lands. Recording the rule commit's sha in the run record is an addition made by Advocate A in Round 2 and is contested (diff point C-007 is unresolved).
6. The identity check reports `unrecorded` until a writer of `model.observed` exists (nothing writes it at HEAD). Slot C-08's adjudicated design places an identity gate in `scripts/reflect_shadow_exit.py`, partial and BLOCKED_BY_INVARIANTS; an `unrecorded` identity check is not a pass, so "accepted" is unreachable while it stays `unrecorded`, and the debate did not decide what then happens.
7. One kernel touch stays open: conservation needs the raw text of a rejected line, which sits behind the private `_blocks_after` (`findings.py:38`); a script imports a private name or the kernel exposes one small public helper (a C-01 and C-06 interaction).
8. The dispatch-time expected-cells manifest (written before `panel.resolve` drops skipped slots) is owed to the dispatch slot and is not in any adjudicated merged output.
9. The import of the E2 harness into the main line needs a named owner and a `.gitignore` exception (the study tip is not an ancestor of HEAD; `lib/` is hidden by `.gitignore:13`); generic harness code lives in `scripts/` with `tests/`, run data, ground truth and values files stay under `.dev/`, and one sentence is added to `.dev/README.md` line 5.
10. The two reflect-gate repairs (`scripts/reflect_shadow_exit.py:313` and `:59`) and the gate-bite test M-6 are in scope; whether the repaired gate can reach PASS on real data is open (probe INV-017).
11. Slot C-06 and slot C-08 have been adjudicated since the proposals were written and are cited by the advocates and the fault-finder (outside the three slots named in the brief; not a forbidden path). The statement in the base text that it relates to "the three adjudicated slots" is kept with one added sentence saying so.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 29 findings, 4 ADDRESSED (probe INV-009, 010, 014, 024), 25 UNADDRESSED (12 HIGH, 13 MEDIUM, 0 LOW). Convergence was blocked by the 12 HIGH items; standard depth has no Round 3, so none was resolved. Ids are the probe's (`probe INV-nnn`), not the ids of the same number in adjudicated slots.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-001 | HIGH | state_variables | A rule committed after C-02 lands can still be measuring a kernel that C-03 and C-06 later change; an offline run on the 71 stored rows may not predict the live metric. |
| INV-002 | HIGH | state_variables | Git commit order is not execution order, nothing stamps the rule commit sha into the run record, and a squash merge can rewrite order. |
| INV-003 | HIGH | state_variables | Re-parse conservation can give false flags when parser or policy version drifts; the ledger entry stores no version and C-06 puts the cut behind `repair=False`. |
| INV-005 | HIGH | state_variables | No expected-cells manifest exists in any adjudicated output or E2 run; a post-hoc manifest of the surviving cells would pass completeness. |
| INV-006 | HIGH | guard_conditions | A verifier record that is all `unrecorded`, or a truncated `flags.tsv`, satisfies a "record exists" refusal; flags-only output makes a crashed verifier read as clean. |
| INV-007 | HIGH | guard_conditions | The judge writes its own three counts and `gt_covered_blocking` has no (GT id, row id) map, so the wrapper equation is only arithmetic self-consistency. |
| INV-013 | HIGH | count_divergence | The unit of analysis is not named: the 71 rows hold 32 multisets with repeats on 3 packages and 81 of 89 catches sit on two items, so a row-level test is anti-conservative; the fault-finder's own arithmetic puts the smallest one-sided p of an exact test over 3 packages at 1/8 (unverified). |
| INV-019 | HIGH | interaction_effects | The adjudicated C-06 hybrid already adds `repaired` and `dropped` keys to each reviewer entry; the verifier must read them and give an acknowledged drop a defined flag state. |
| INV-021 | HIGH | interaction_effects | The verifier reports `unrecorded` where C-08's identity gate maps a skipped `ingest` to `requested-pinned`; two readers of one file have different absent-input semantics. |
| INV-025 | HIGH | sufficiency_challenge | The metric of record and the conservation law are defined on `review-ledger/1` rows; no acceptance metric exists for the reflect Tier 2 panel, UC-1, UC-2, PR review or rf-qa. |
| INV-026 | HIGH | sufficiency_challenge | The answer-key and tool-use defect class has no component in the hybrid; if C-08's M1 fails, identity stays `unrecorded`, Tier S can never be `pass`, and "accepted" is unreachable for every use case. |
| INV-027 | HIGH | sufficiency_challenge | Inline enumeration: an identity swap, a dispatch-skipped cell, a judge row mismatch with consistent counts and a post-hoc rule each pass every gate; only parser drift fails a gate, and falsely (INV-003). |
| INV-004 | MEDIUM | state_variables | Ledgers written before and after C-02 are read differently (stored `verdict`/`decision`/`brief_ids` versus derived on read). |
| INV-008 | MEDIUM | guard_conditions | The single severity policy file decides the audit-clean population, yet the pre-registered set does not name it. |
| INV-011 | MEDIUM | count_divergence | "71" is not one population and the denominators 8 and 14 ignore the control's 2 items. |
| INV-012 | MEDIUM | count_divergence | Part of the 89 against 38 gap may be rejected blocking lines (C-06), not severity typing, so M-7 cannot attribute a move to C-02. |
| INV-015 | MEDIUM | collection_boundaries | The expected cell has no attempt component; an empty manifest passes completeness vacuously; cells absent from the manifest get no flag. |
| INV-016 | MEDIUM | collection_boundaries | The headline and "control found" are undefined for a package with zero blocking-in-implement items (the control: 0 of 0). |
| INV-017 | MEDIUM | collection_boundaries | M-6 may not show the gate bites: on real data the repaired gate can only move FAIL to INSUFFICIENT-RUNS (15 tracked runs against 20 required) and the empty-baseline verdict is unspecified. |
| INV-018 | MEDIUM | collection_boundaries | One run per cell and one judge pass per (package, label) leave the noise floor unknown; the double-scored sample is not yet in a pinned list. |
| INV-020 | MEDIUM | interaction_effects | "Ledger row typed blocking" is not one stable field after C-02's CRITICAL floor; the rule must name the field and the merge-policy version. |
| INV-022 | MEDIUM | interaction_effects | `.gitignore:13` (`lib/`, also `build/`, `dist/`, `parts/`, `var/`) can hide harness modules that pass locally and are missing in CI; no `git check-ignore` check is planned. |
| INV-023 | MEDIUM | interaction_effects | Path-less CI `pytest -n auto --maxfail=3` collecting harness tests over untracked study data fails or skips on a clean clone; tests need small committed fixtures. |
| INV-028 | MEDIUM | sufficiency_challenge | The 16-item ground truth has unrecorded authorship and one implement run per plan; a flipped label moves the per-item headline; Tier G has no owner. |
| INV-029 | MEDIUM | sufficiency_challenge | A post-run verifier finds a bad run after the judge cost is paid; the identity-overwrite fix sits in a launcher that is untracked at HEAD. |

Open items from the invariant probe, and the evidence-staleness note. (a) No decisive point turns on a fact from commit `c44c98a77`: the fault-finder read nothing from it and the advocates' uses were corroboration only; the diff analysis and merge log agree. Nothing needs to be recorded as an open item for that commit. (b) Facts the debate could not verify: the exact-test floor in INV-013 is the fault-finder's own arithmetic; the overlap of audit D's 45 `3-dropped-blocking` flags with the 71 presence rows was not computed; the judge token figure in INV-029 and the untracked status of `run-reviewer.sh` rest on other agents' statements; C-06's `repair=False` default is read from the adjudication, not from code (C-06 is not implemented at HEAD); the C-02 and C-08 behaviours are adjudicated designs, not shipped code; the control ground-truth labels were taken from the diff analysis, not re-run with `jq` by the fault-finder (the advocates verified them at the study tip).

## Unresolved by label

Diff points C-005, C-007, C-008 and X-004: the two Round 2 calls differ (A against TIE) while the substance converged on the status wording. The merged text keeps Proposal A's three-valued identity state (C-005) and Proposal A's pre-registration condition with the sha recording marked contested (C-007), and carries the agreed wording of condition 1 for C-008 and X-004.

## Artifacts

- Merged result: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/eval-acceptance-and-harness-owner/merged-output.md`
- Adversarial directory: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/eval-acceptance-and-harness-owner/adversarial/` containing:
  - `variant-1-original.md`, `variant-2-original.md` (the two proposals as copied in)
  - `diff-analysis.md` (Step 1: 9 structural, 16 content, 6 contradictions, 15 unique contributions, 13 shared assumptions)
  - `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`
  - `invariant-probe.md` (Round 2.5)
  - `debate-transcript.md` (Step 2, with the Scoring Matrix and Convergence Assessment)
  - `quant-score.py`, `quant-score-output.json`, `score-pass1.md`, `score-pass2.md`, `score-reeval.md`
  - `base-selection.md` (Step 3)
  - `refactor-plan.md` and `plan-review.md` (Step 4)
  - `merge-log.md` (Step 5: 13 of 13 changes applied, post-merge validation PASS)
  - `return-contract.yaml` (status partial, convergence 0.91, 12 HIGH unaddressed invariants)
