# Adjudication result: slot C-07 (dispatch-and-launch-mechanism)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the diff analyst, advocates, fault-finder, scorers, plan reviewer and merge-executor were separate agents.

## Winner

**Variant 2 (Proposal B) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant 2 (Proposal B; default model, default persona)". The merged resolution is `merged-dispatch-and-launch-mechanism.md`: Proposal B's dispatch contract (the core launches nothing; a reviewer is launched with its `launch` word as the Agent `model` argument) with its packaged `gateway.launch` class-word fill withdrawn and replaced by a binding stated as data in an explicit environment, and with Proposal A's falsifiable probes and gated `claude-p` launcher design added. Neither proposal won as written: after Round 2 both advocates named a gated hybrid ("H-gated" for Proposal A's advocate, "V2-bound" for Proposal B's advocate) that agrees on what ships now and differs on what is committed for later.

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: Variant 1 0.8773, Variant 2 0.9800 (requirement coverage 0.8000 against 0.9333, internal consistency 0.8824 against 1.0000, specificity 1.0 each, dependency completeness 1.0 each, section coverage 0.7778 against 1.0000).
- Qualitative layer (30 criteria, two position-bias passes, 8 of 60 pairs re-evaluated): Variant 1 22/30 = 0.7333, Variant 2 26/30 = 0.8667. Dimensions: Completeness 4/5 against 5/5, Correctness 1/5 against 3/5, Structure 4/5 against 5/5, Clarity 3/5 against 4/5, Risk Coverage 5/5 against 4/5, Invariant & Edge Case 5/5 each.
- Combined: Variant 1 0.8053, Variant 2 0.9233. "Margin: 11.80% (above the 5% threshold)". "Tiebreaker applied: No". The debate tally, reported for reference, is Variant 2 9 points against Variant 1 2 (Hybrid 5, Neither 5, unresolved 5).
- The debate's stated reason: Variant 1 lost Correctness on two intra-variant contradictions (X-008 identity evidence from a flag set the read-only adapter cannot use; X-009 ceiling widened without reading `read_only`), an `adapters` key the tier validator rejects (`panel.py:371-373`) and conceded overstatements. Variant 2 lost Correctness on the packaged `gateway.launch` fill (withdrawn by its own advocate in Round 2), a misstatement of Variant 1 on the test pin (X-002) and a missed existing static test (X-007). Variant 1 led only on Risk Coverage.
- Convergence: 21 of 26 diff points agreed (80.77%) against an 80% threshold; Round 1 agreement was 16 of 26 (61.54%). Status BLOCKED_BY_INVARIANTS (see unaddressed invariants below).

## Conditions under which the winner holds (all stated in `merged-dispatch-and-launch-mechanism.md`)

1. The scores rate the two documents as written. The gated hybrid was not scored.
2. What both advocates agreed ships now: the dispatch rule (S1), no packaged tier, resolver, validator or ceiling change (S2), one transcript reader (S3), the deferred dynamic read-only test on the Agent path (S4), and bindings as data in a workspace or explicit tier file (S5). S6 (shape tests) and S7 (a PreToolUse guard, named, not built) are Advocate B's additions and were not adopted or rejected by Advocate A. With the packaged `gateway.launch` still `{}`, the `--env gateway` refusal remains for any caller that does not pass an explicit tier file and environment (INV-018).
3. The `claude-p` launcher is gated, not built: it needs G1 (identity and reach under the restricted flag set), G2 (read-only plus tool surface) and G3 (no regression) first, and G2 before any widening of `_REFLECT_LAUNCH` by one value. No `--restricted` run on a gateway id exists. If G2 fails, Advocate A states the end state is Variant 2's.
4. Read-only by construction is a static pin for the agent-file path only; the dynamic no-mutation test is deferred, so INV-G is statically pinned for both positions.
5. A class-word binding is correct only for the session binding it states; a mismatch is found after the fact (INV-001), not before dispatch. The dispatch rule S1 is a prompt rule with no enforcer; the collapse replay runs after the votes.
6. Claude Code behaviours the repo does not pin (the Agent enum, `resolvedModel`, `message.model` truthfulness after shim failover, `SubagentStop` transcripts) are assumed stable (A-001, A-002 both QUALIFY); no cost or quality comparison of the paths exists.
7. Two things the debate left split between the advocates, recorded side by side in the merged file: after G1-G3 pass, Advocate A ships launcher, `gateway.launch` fill with `claude-p` and ceiling widening together in the shared review layer, while Advocate B builds only on a named consumer need (a panel with more than three distinct served models) in the consuming engine and never fills the packaged `gateway` environment. Five diff points are unresolved: X-001, X-006, A-003, A-004, A-006.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 19 findings, 3 ADDRESSED (INV-008 LOW, INV-013 MEDIUM, INV-019 MEDIUM), 16 UNADDRESSED. Convergence was blocked by the one HIGH item; standard depth has no Round 3, so it was not resolved.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-017 | HIGH | sufficiency_challenge | The ship-now set does not by itself close the A-r3 collapse (all reviewers and calibrators served one model): in shadow the dispatch is legacy, calibrator Agent calls carry a null word in six of 15 runs and no S item covers them, an omitted `model` falls back to `model: sonnet`, and the only mechanical guard (S7) is unbuilt with an unverified payload. |
| INV-001 | MEDIUM | state_variables | A class-word binding written as data is not compared with the session's binding before dispatch; the combo runs disagreed with the pin in 11 of 15 runs. |
| INV-003 | MEDIUM | state_variables | S5 is stated in two forms (`find_path` override vs `--tiers`); the `find_path` form silently replaces the packaged tiers for every shadow resolve. |
| INV-005 | MEDIUM | guard_conditions | S1 does not govern calibrator calls; a replay over every Agent row would flag six runs and falsify the "flags A-r3 and no other" prediction. |
| INV-006 | MEDIUM | guard_conditions | S4 passes if the model declines in prose; no effective-tool-list source on the Agent path; `permissionMode: plan` may block instead of the allowlist. |
| INV-007 | MEDIUM | guard_conditions | G2 has no "reads its inputs and returns a valid findings block" criterion; `--restricted` confines file tools to the working directories. |
| INV-009 | MEDIUM | count_divergence | Three reviewers on three class words leaves no class for a disjoint blind calibrator; `calibrator_diversity` "full" occurs only in the collapsed run. |
| INV-010 | MEDIUM | count_divergence | S6's "same panel for any run id" is false for the `x2` templates; exclusion paths (`--hard-exclude-class`) are untested and the floor is N=2. |
| INV-011 | MEDIUM | count_divergence | The transcript reader's key (reviewer id vs attempt id) is not stated; attempts are not reviewers. |
| INV-014 | MEDIUM | interaction_effects | Executor-class exclusion expands through model-id classes, not class words; with `haiku` bound to a non-Claude model the executor's own served model can review its own work. |
| INV-015 | MEDIUM | interaction_effects | S1 and the shadow fence: applied to shadow dispatch it stops shadow being shadow; applied only under the `panel` engine it has no consumer until Stage 3. |
| INV-016 | MEDIUM | interaction_effects | Once `claude-p` is a permitted `launch` value, the reflect check tests the value, not the model; a `claude-p` reviewer's tool surface lives in launcher argv with no static test. |
| INV-018 | MEDIUM | sufficiency_challenge | The ship-now set does not change behaviour in a gateway workspace: `--env gateway` still refuses, and no S item makes any caller pass an explicit tier file and environment. |
| INV-002 | LOW | state_variables | A static fixture copy of the tier file tests its own aliases, not the packaged ones. |
| INV-004 | LOW | guard_conditions | S1's "`launch: null` is a dispatch error" contradicts D4's legacy-rotation rule and can fire only for generic templates. |
| INV-012 | LOW | collection_boundaries | `resolve` prints a launch word for the primary pick only; a fallback model may have no word. |

Return contract `unaddressed_invariants` (HIGH only): INV-017.

## Return contract

Status `partial`; convergence score 0.81 (21 of 26 = 0.8077); base variant `variant-2 (Proposal B; default model, default persona)`; unresolved conflicts 5 (X-001, X-006, A-003, A-004, A-006); fallback mode false; failure stage null; invocation method `task-agent`. Merge: 12 of 12 planned changes applied, post-merge validation PASS.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/dispatch-and-launch-mechanism/`

- Merged file: `.../dispatch-and-launch-mechanism/merged-dispatch-and-launch-mechanism.md`
- Artifacts folder `.../dispatch-and-launch-mechanism/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`)
  - `refactor-plan.md`
  - `merge-log.md`
  - `return-contract.yaml`
