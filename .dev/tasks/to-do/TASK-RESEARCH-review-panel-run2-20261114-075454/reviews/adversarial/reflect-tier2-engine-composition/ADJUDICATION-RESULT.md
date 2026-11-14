# Adjudication result: slot C-04 (reflect-tier2-engine-composition)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the advocates, the diff analyst, the fault-finder, the scorers, the plan drafter and reviewer and the merge-executor were separate agents. Depth standard: Round 1 (parallel), Round 2 (sequential), Round 2.5 (invariant probe), no Round 3.

## Winner

**Variant 1 (Proposal A) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant 1 (Proposal A; `variant-1-original.md`)". The merged resolution is `merged-output.md`: the hybrid both advocates reached in Round 2, called H-C04 by the Variant 1 advocate and H-C04B by the Variant 2 advocate, "code-owned write side behind a gated shell; no engine moves now". Neither proposal won as written. Both advocates conceded the points that the code settled against their own text, and after Round 2 they named the same label on 42 of 45 debate points (Variant 1 5, Variant 2 12, Hybrid 12, Not material 7, Neither 1 over the 37 agreed S/C/X points; 3 S/C/X points stayed unresolved; the five shared assumptions A-001..A-005 were all agreed).

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: Variant 1 0.9938, Variant 2 0.9889 (requirement coverage 1.0000 and 1.0000, 11 of 11 IDs; internal consistency 0.9753 and 0.9683; specificity 1.0000 and 1.0000; dependency completeness 1.0000 and 0.9787; section coverage 1.0000 each). The base-selection text: "The quantitative layer is saturated and separates them by 0.005."
- Qualitative layer (30 criteria, two position-bias passes, 8 of 60 criterion-variant pairs re-evaluated): Variant 1 26/30 = 0.8667, Variant 2 22/30 = 0.7333. By dimension: Completeness 5/5 and 5/5; Correctness 2/5 and 1/5; Structure 5/5 and 5/5; Clarity 4/5 and 4/5; Risk Coverage 5/5 and 3/5; Invariant & Edge Case Coverage 5/5 and 4/5.
- Combined: Variant 1 0.9302, Variant 2 0.8611. "Margin: 6.91% (above the 5% threshold)". "Tiebreaker applied: No". The edge-case floor (at least 1/5) was met by both.
- The debate's stated reason (`base-selection.md`): "The qualitative layer decides it: 26/30 against 22/30." The scorers charged each document with the defects the debate verified against code and that its own advocate conceded. For Variant 1: the unrouted grounded lane (`runner.py:538-545`, X-001), the CV-5 pin collision (`test_ensemble_stub_integration.py:141-168`), an allowlist that would drop `adversarial_subrun_status` (`contract.py:306`), the INV-K edit-fence row, and the headless lint-layout conflict (X-008). For Variant 2: the CV-5 wording that reverses the decided row and contradicts its own section 1(i) (X-003, X-009), the uncorrected CV-8 lines, the double use of GQ-067 (X-006), the overstated "reuse, not new logic" (V-29), and a kernel placement of the serializer whose frozen lists live in `cli/reflect/panel_lint.py`.
- "The selection is a choice of base text, not of position" (`base-selection.md`): Variant 1's 14-row invariant table, its reopen conditions for C-01, C-02 and C-03, its per-step failure-to-code table and its offline replay oracle are the structures the hybrid is built on, and Variant 2's contributions (staging evidence, seam probe, trigger, disclosure, edit-fence accounting) were incorporated as additions.
- Both layers favoured Variant 1. The debate's scoring matrix does not favour Variant 1 by points won (Variant 2 12, Variant 1 5, Hybrid 12); the tiebreaker was not applied, so that count did not enter the selection.
- Convergence: 42 of 45 points agreed (93.33%; Round 1 was 36 of 45 = 80.00%) against an 80% threshold. Status CONVERGED (no HIGH-severity UNADDRESSED invariant; see below). Unresolved labels: C-007 (Variant 1 advocate: Hybrid; Variant 2 advocate: Variant 2), C-009 (Variant 2; Hybrid), C-018 (Hybrid; Variant 2).

## Conditions under which the winner holds (all stated in `merged-output.md`)

1. No capability moves now. Production Tier 2 stays engine A's ensemble (`runner.py:540` routes `standard` and `deep` there). The grounded lane through the wrapper is DEFERRED, not built; it needs a routing switch before `runner.py:540`, an extended seam probe (M3-ext: marker set, `reviewer_profile=True`, agent calls complete, files written, a `review` command not suppressed), one reviewer-count rule (kernel cap 3 against the runner's clamp to 1 or [2,4]) and executor exclusion with slot C-09.
2. The write-side helpers make a skipped step detectable, not prevented. Fail-closed holds only where a Python parent exists (the headless lane). Skip detection by stage advance works only if the kernel verifies output hashes against files (`manifest.py:285-291` checks the hash format only).
3. Helper output is a comparison artifact until promoted (INV-L). Promotion is a separate decision after the offline replay (M-A) and `scripts/reflect_verdict_replay.py` show no verdict differences; how INV-L reads (helpers write only under `panel/`, or hygiene writers are allowed) is recorded as an owner question.
4. CV-5 is "acknowledged non-conforming, change deferred", with release conditions: the stub lane writes a disk merged output or the I1 witness is rewritten under an explicit decision that headless PASS is not credit-free, or engine A's reviewer path is retired.
5. The decided document and script fixes (D1: CV-1, CV-2, CV-3, CV-6, CV-8, CV-9) are done now, with the SKILL.md edit allow-list (`test_shadow_skill_contract.py:65`) widened in the same change and `:838-839` kept as residue inside frozen 9.1.
6. The headless lane, its lens and its layout are unchanged, and the production T5 PASS is disclosed as a convergence-and-diversity result with no deviation audit. The headless finalizer and the lens change return only on a measured condition.
7. The single-engine decision is named, not scheduled: one decision with a fork (Option 3, retire engine A's reviewer path; or D3, the grounded lane through the wrapper with the swarm lane kept), triggered by the owner's answer to the wrapper-switch question. An M-B failure with mechanical presence is an owner escalation, not a retirement trigger.
8. The hybrid is an analysis, not an observation: no run has used a code-written contract, card or `merged-verdict.yaml`, and no quality measurement exists at HEAD. Run counts (13 pilot, 15 combo, 28 runs, 8 of 13, 6 of 13) were not re-derived by the diff analyst (V-13, V-34).
9. Items from the Variant 2 advocate's Round 2 (R-1..R-7, E-1..E-8) were not answered by the Variant 1 advocate; where they enter the merged file they are marked as such.
10. The adjudicated slots stay valid on the readings the debate fixed: "no change to `cli/reflect`" is read as the weak reading (additive files, no edit to engine A's behaviour); C-02 reopens if the `--fix` loop gains cross-round finding identity; the C-03 dependencies (reflect keeps `shortfall: visible`, requested-based diversity, support flags only in the v2 kernel) hold.
11. Three S/C/X labels and six sub-disputes inside the hybrid are OPEN and carried two-sided in `merged-output.md` section 9.2: (1) the labels C-007, C-009, C-018 including the disclosure sentence and the trigger prongs (M4 repaired; "T5 gate must report deviations"; a Stage 5 deadline); (2) helper placement (code in `cli/reflect/` registered onto `review_group` at `cli/main.py`, against `cli/review/<name>_cmd.py` with a lazy import of the `panel_lint.py` constants; root registration is the stated fallback); (3) the serializer's accepted key set (lint set plus `adversarial_subrun_status`, against exactly the lint set with that key as a named exemption in the coverage pin); (4) which stages a helper advances (each helper-owned stage, against `resolved`, `calibrated`, `debated` only); (5) the shape of INV-L (one comparison artifact, against three points with siblings first); (6) the default direction before the owner answers (Option 3 only on a "switch" answer, against Option 3 as the named default on "switch and no headless").

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 20 findings, 3 ADDRESSED (INV-004 LOW, INV-018 MEDIUM, INV-020 LOW), 17 UNADDRESSED. None is HIGH, so convergence was not blocked and the return contract's `unaddressed_invariants` is empty. Standard depth has no Round 3; the 17 stay open in `merged-output.md` section 9.3.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-001 | MEDIUM | state_variables | A helper writes a comparison sibling, not the legacy file, in shadow; the consensus never says where it reads the mode (`manifest.py:123-127, :496-500`). |
| INV-002 | MEDIUM | state_variables | `calibrated` as a helper-owned stage: `SKILL.md:345` has the orchestrator fix `panel/cards/` after `calibrated`; a rerun raises `Conflict` and a hand fix leaves a stale hash. |
| INV-003 | MEDIUM | state_variables | Arm A and M-B cannot each be read off the exit script as a clean 20-run set: `collect` counts every published shadow run with no arm or date filter. |
| INV-005 | MEDIUM | guard_conditions | Name-only validation over the stable and telemetry lists: `degraded_components` is read by `derive_verdict` only at top level, and the lint allows both placements. |
| INV-006 | MEDIUM | guard_conditions | "Helper refuses", "helper advances its own stage" and shadow's "continue as legacy" are not shown compatible (`advance_stage` raises `OutOfOrder`). |
| INV-007 | MEDIUM | guard_conditions | M-A's "every recorded run yields a lint-clean contract" does not hold for runs with a leaked key under a serializer that refuses; the 3 unparseable alias contracts are not exercised. |
| INV-008 | MEDIUM | count_divergence | "Exactly one verdict-read key lies outside the frozen lists": A counts 19 keys, B 18; both miss alias reads in `_make_result`; "137 names" is 136 distinct. |
| INV-009 | MEDIUM | count_divergence | D1's CV-8 and CV-1 line lists may be incomplete (`executor-disjoint` at further lines; `0.75` on 10 `SKILL.md` lines plus 2 in `refs/grader-extensions.md`). |
| INV-011 | MEDIUM | collection_boundaries | M-B cannot require zero parity failures over 20 runs: a 2-of-3 shortfall run is normal for the exit but fails parity on a card-count mismatch. |
| INV-012 | MEDIUM | collection_boundaries | D1's fix at `reflect_shadow_exit.py:313` does not close all of CV-9; the meaning of "no baseline" for the EV-1 comparison is unstated. |
| INV-013 | MEDIUM | collection_boundaries | The presence rule and a refusing finalizer do not cover every run shape (no-merge fallback run must still advance `debated`; `reviewers_resolved: 0`). |
| INV-014 | MEDIUM | interaction_effects | The exit rule and `reflect_verdict_replay.py` read fixed paths and pair by directory name, so code-built siblings are not readable without change beyond line 313. |
| INV-015 | MEDIUM | interaction_effects | The card writer's target differs between the two advocates' texts; CV-9 also names the card-name regex mismatch (`panel_lint.py:188` against `reflect_shadow_exit.py:59`). |
| INV-017 | MEDIUM | sufficiency_challenge | "Helpers that advance their own stage make skipping detectable": the orchestrator can advance with its own or empty payload; hash-versus-file check is optional. |
| INV-019 | MEDIUM | sufficiency_challenge | "Comparison siblings let promotion be decided without risk": the absence path is never exercised in shadow, promotion is an engine flip with a new invocation, and `read_committed` passes in shadow. |
| INV-010 | LOW | count_divergence | The reviewer-count value 1 and the I2 witness (`test_ensemble_stub_integration.py:174-196`) have no named replacement. |
| INV-016 | LOW | interaction_effects | Widening the fence is not only bookkeeping: `SKILL.md:703` and `:1480-1481` are legacy-path instructions outside `### 4.3a`; the 3/39 baseline predates the new prose. |

Return contract `unaddressed_invariants` (HIGH only): none.

## Return contract

Status `partial`; convergence score 0.9333 (42 of 45); base variant `Variant 1 (Proposal A, variant-1-original.md; default model, default persona)`; unresolved conflicts 3 (C-007, C-009, C-018); fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/reflect-tier2-engine-composition/`

- Merged file: `.../reflect-tier2-engine-composition/merged-output.md`
- Artifacts folder `.../reflect-tier2-engine-composition/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score.md`, `quant-score-output.json`)
  - `refactor-plan.md`
  - `merge-log.md`
  - `return-contract.yaml`
