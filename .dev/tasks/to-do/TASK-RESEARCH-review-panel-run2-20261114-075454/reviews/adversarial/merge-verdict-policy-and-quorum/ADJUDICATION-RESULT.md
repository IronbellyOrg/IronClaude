# Adjudication result: slot C-03 (merge-verdict-policy-and-quorum)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; advocates, fault-finder, scorers and merge-executor were separate agents.

## Winner

**Variant A (Proposal A) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant A (Proposal A; `variant-1-original.md`)". The merged resolution is `merged-output.md`: the union default and the pluggable policy of Proposal A, with quorum turned into a merge-time refusal, and with Proposal B's falsifiers, offline adjudicated policy, independence-as-data and claim limits added. Neither proposal won as written: both advocates, after two rounds, named the same winner on all 21 structural, content and contradiction points (Variant A 9, Variant B 3, Hybrid 8, Neither 1).

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: A 0.9680, B 0.9846 (requirement coverage A 0.9091, B 1.0000; internal consistency A 0.9811, B 0.9487; specificity A 1.0, B 1.0; dependency completeness A 1.0, B 0.9831; section coverage 1.0 each).
- Qualitative layer (30 criteria, two position-bias passes, 2 of 60 pairs re-evaluated): A 25/30 = 0.8333, B 22/30 = 0.7333. Dimensions: Correctness A 3/5, B 1/5; Clarity A 4/5, B 3/5; Risk Coverage A 4/5, B 3/5; Completeness A 4/5, B 5/5; Structure 5/5 each; Invariant & Edge Case 5/5 each.
- Combined: A 0.9007, B 0.8590. "Margin: 4.17% (below the 5% threshold)". "Tiebreaker applied: Yes, level 1 (debate performance). Variant A won 9 points against 3 for Variant B".
- The debate's stated reason: B's Correctness losses are three code-checked defects (the E11 "computed from served model ids" wording is wrong for the shipped transport; the `pending` row state has no brief entry, verdict or exit code in the ledger; B's INV-L statements contradict each other). A's losses are an overstated claim ("at most one fix cycle", conceded) and the "every panel size" headline against its own reflect profile.
- Both layers are reported: the quantitative layer favoured B, the qualitative layer favoured A.
- Convergence: 25 of 26 diff points agreed (96%) against an 80% threshold. Status BLOCKED_BY_INVARIANTS (see unaddressed invariants below).

## Conditions under which the winner holds (all stated in `merged-output.md`)

1. The default rests on fail-closed asymmetry and on the absence of any measurement, not on measured superiority. No policy was compared with ground truth; B's `adjudicated`-as-default is recorded as a hypothesis awaiting a pre-registered measurement.
2. The union is the cheap-error side only while a Reviser-rejected row has a non-human exit. Today a rejected row stays `open` and only `defer` clears it, so the false-blocker cost is "to the cap, then a human decision". This is a dependency on slot C-02, not a gate.
3. Fail-closed is claimed only in profiles that set `degrade` (spec review). Reflect keeps `shortfall: visible`, `derive_verdict`, its 36 tests and the two shortfall pins.
4. The quorum floor (`min(2, requested)`) is an unmeasured parameter. The refusal closes the one-valid-block-of-N defect (D-2) for `complete < floor` only, and for callers that supply reports for every dispatched reviewer; the variant where a reviewer wrote no file is closed only when the coordinator passes `--resolution`. The `requested` mechanism was proposed by B's Round 2 and not answered by A.
5. Independence (distinct served model ids, vendor) is recorded data "requested, not served" until the transport records `model_observed` (slot C-08).
6. The default does not satisfy FX-10 ("a weak model must not decide alone"); it prices it.
7. Support and disputed flags exist only in the v2 kernel; v1 ledger rows cannot feed an rf-qa confidence gate until findings-v2 reaches the ledger (slot C-01).
8. Four mechanism points inside the two Round 2 hybrids were chosen on B's code evidence without a reply from A (no rendered row flags; lower-bound enforcement instead of "quorum not measured"; adjudicated arm offline; `refusal` object with no `decision` key). Shared-assumption A-003 labels differ (A REJECT, B QUALIFY) though the substance converged.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 17 findings, 5 ADDRESSED, 12 UNADDRESSED. Convergence was blocked by the two HIGH items; standard depth has no Round 3, so none was resolved.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-006 | HIGH | guard_conditions | The consensus text says "any complete reviewer's blocking flag", but `merge_round` unions every parsable finding, including those of a reviewer whose block is invalid (`ledger.py:127-138`); no test pins this. |
| INV-007 | HIGH | count_divergence | `requested = max(len(resolution.reviewers), len(--report))` can collapse to 1 because `panel.resolve` drops skipped slots and writes `skipped_slots` only when an exclusion flag is used (`panel.py:636-656, 700-706`); then one valid empty block passes. |
| INV-001 | MEDIUM | state_variables | A refusal records nothing, so refusal rate, retries and reviews-to-cap are not measurable and refused rounds' reviewer spend is outside `cap_reviews`. |
| INV-002 | MEDIUM | state_variables | After exit 12, `ledger verdict` shows the previous round's stored decision; no rule tells the coordinator not to consult it. |
| INV-003 | MEDIUM | state_variables | Which layer owns the profile, `min_complete` and `requested` default is unspecified (`merge_round` has no such parameter; 24 test call sites). |
| INV-004 | MEDIUM | guard_conditions | `--resolution` is not checked for kind or run (a first-kind resolution with a single-reviewer re-review inflates `requested`; a stale one deflates it). |
| INV-005 | MEDIUM | guard_conditions | `complete` is not checked for distinct, current reviewers (unknown ids, identical report text, duplicate ids in the resolution, stale reports reused on retry). |
| INV-009 | MEDIUM | count_divergence | Between the floor and `requested` the shortfall is silent: the merged report prints "panel of N reviewers" from the reports passed. |
| INV-010 | MEDIUM | collection_boundaries | The N=1..5 x five-state test matrix can only distinguish three input states at the CLI; the zero-valid refusal pin asserts message text the new refusal object does not contain. |
| INV-016 | MEDIUM | sufficiency_challenge | The union is deterministic but runs over rows that may already hold a `same_defect` mistake (a new blocking defect matched to a `deferred` row never fails the round). |
| INV-012 | LOW | interaction_effects | `defer` is the only non-quorate route to a stored PASS and is reachable exactly when quorum keeps failing. |
| INV-013 | LOW | interaction_effects | `make verify-sync` does not cover the loop-prompt copies; installed prompt skew leaves callers without `--resolution` until reinstall. |

ADDRESSED with residuals recorded in `merged-output.md` section 4.3: INV-008 (LOW), INV-011, INV-014, INV-015, INV-017 (MEDIUM).

Return contract `unaddressed_invariants` (HIGH only): INV-006, INV-007.

## Return contract

Status `partial`; convergence score 0.96 (25 of 26 = 0.9615); base variant `variant-1 (Proposal A; default model, default persona)`; unresolved conflicts 1 (A-003); fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/merge-verdict-policy-and-quorum/`

- Merged file: `.../merge-verdict-policy-and-quorum/merged-output.md`
- Artifacts folder `.../merge-verdict-policy-and-quorum/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`)
  - `refactor-plan.md`
  - `merge-log.md`
  - `return-contract.yaml`
