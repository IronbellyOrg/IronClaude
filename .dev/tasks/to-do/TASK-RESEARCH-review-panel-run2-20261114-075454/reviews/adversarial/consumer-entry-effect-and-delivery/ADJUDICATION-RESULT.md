# Adjudication result: slot C-05 (consumer-entry-effect-and-delivery)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the advocates, the fault-finder, the two scorers, the re-evaluator and the merge-executor were separate agents. Conflict rows: C-S7, CO-25, CO-35.

## Winner

**Variant A (Proposal A) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant A (Proposal A; `variant-1-original.md`)". The merged resolution is `merged-output.md`. Neither proposal won as written: both advocates, after two rounds, named the same winner on all 24 diff points (Variant A 4, Variant B 3, Hybrid 13, Neither 4).

The merged resolution, as the debate produced it:
- **Entry (C-001, Variant A wins, 90%).** Workflow Wave 4 and tasklist Stage 10.5 keep the single call `/sc:reflect --mode pre ...`. No B-replace and no direct panel call in this release. B-add was withdrawn by Variant B's advocate as a recommendation for this release.
- **Effect (C-002, Hybrid, 90%).** Advisory at Wave 4. Stage 10.5 is "advisory-blocking" by its own label, not plain advisory (the bundle ships whatever the verdict; a `needs_human_decision` item halts; an unattended run ends `blocked`). Blocking stays at T5 and Stages 6-10. Any blocking use of the panel at generation time is a later, separate Stage 7 reviewer-feed change gated on a replay.
- **Delivery (C-003, Variant A wins, 93%).** No panel-only plugin copy; plugin delivery is decided as one set (reflect, panel, reviewer agent, CLI availability).
- Structure and measurement taken from Variant B: the three separable parts (S-002), per-row invariant verdicts (S-003), a parity test per added plugin file (A-006), and a two-arm replay with loop and cost columns.

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: A 0.9789, B 0.9808 (requirement coverage A 1.0000, B 1.0000; internal consistency A 0.9655, B 0.9231; specificity 1.0000 each; dependency completeness A 0.9167, B 1.0000; section coverage 1.0000 each).
- Qualitative layer (30 criteria, two position-bias passes, 3 of 60 pairs re-evaluated, the re-evaluator sided with Pass 2 on all three): A 23/30 = 0.7667, B 24/30 = 0.8000. Dimensions: Completeness A 5/5, B 5/5; Correctness A 2/5, B 2/5; Structure 5/5 each; Clarity A 3/5, B 4/5; Risk Coverage A 4/5, B 3/5; Invariant & Edge Case A 4/5, B 5/5.
- Combined: A 0.8728, B 0.8904. "Margin: 0.0176 (1.76%), below the 5% threshold. Variant B leads on the combined score." "Tiebreaker applied: Yes." Level 1 (debate performance): Variant A won 4 points outright against 3 for Variant B; the debate notes that 4 versus 3 is 4.2 percentage points of the 24 points, within 5%, so Level 2 (correctness criteria MET: A 2, B 2) and Level 3 (input order: A first) were also checked. "Every path through the tiebreaker ... selects Variant A."
- The debate's stated reason: the combined score does not select a base on its own; both variants have identical Correctness (2/5) because each carries debate-verified errors and contradictions (A: "the fence test must be changed" withdrawn, "zero edits" versus rule D1, "four readers" undercount; B: the contract 1.1 to 1.2 bump, E6 and E7 overstated, the blocking effect placed at fenced Stage 10.5). Variant B's advocate withdrew B-add, the version bump, E6 and E7, and agreed with Variant A's final verdict on all 24 points.
- Both layers are reported: the quantitative layer and the qualitative layer each favoured B by a small margin; the tiebreaker selected A.
- Convergence: 24 of 24 diff points agreed (100%) against an 80% threshold. Status BLOCKED_BY_INVARIANTS (see unaddressed invariants below). The orchestrator's own note in the transcript: B's advocate conceded most points, and that speed is itself a sycophancy signal, so the probe checked whether the conceded claims are true in code; it found several overstated or wrong.

## Conditions under which the winner holds (all stated in `merged-output.md`, Sections 1, 3a, 6, 9a and 11)

1. It holds while the C-01 to C-03 outcomes stand (reflect keeps its own engine and `shortfall: visible`).
2. It reopens if the replay shows the direct path catches materially more blocking ground-truth items per cost, not explained by depth routing; if the owner chooses plugin parity; or if blocking ground-truth items sit in phases that never reach the panel. "Materially more" has no numeric threshold (INV-013), and the third condition has no working instrument today (INV-005).
3. The engine switch is released only after the replay, a contract-compat test against the 36-test verdict matrix and a headless smoke run. The panel-to-status map is not defined (INV-011), and whether consumers would see any benefit is open (INV-014).
4. Reach behind reflect is limited and unsized: workflow reaches a panel only on rubric escalation; tasklist only on forced-deep phases and rubric escalations. The depth-policy remedy is not a pure reach fix and is open (INV-003, INV-004, INV-006).
5. Advisory first; any blocking use waits for a replay. A zero-success blocking feed must escalate, not fail open (A-004).
6. Additive keys at `contract_version` "1.1" are safe at the three consumer-side readers; the 1.1 to 1.2 bump is wrong. A later direct module needs the `artifacts` rule and nested-kind test constants edited by hand, companion-eval allow-list and staging edits, a parity test per plugin file, and its own replay.
7. Nothing was run: no test, no headless call, no replay. The plugin CLI availability, `verify-sync` coverage of `plugins/` and `findings_v2.py:36` were not checked by the fault-finder.
8. No Round 3 ran (depth standard) and no second pass of the 24-point matrix ran after the probe; the probe changes the conditions under which the agreed text holds, not the winners of the 24 points.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 15 findings, 3 ADDRESSED, 12 UNADDRESSED. Convergence was blocked by the seven HIGH items; standard depth has no Round 3, so none was resolved.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-001 | HIGH | guard_conditions | "Advisory at Wave 4 and Stage 10.5": Stage 10.5 halts on `needs_human_decision` and ends `blocked` when unattended (`sc-tasklist-protocol/SKILL.md:1640-1646`); the effect of an engine switch on halt frequency is open. |
| INV-002 | HIGH | interaction_effects | Stage 10.5 always passes `--remediate`, a write path that can nest reflect, workflow and reflect (`sc-reflect-protocol/SKILL.md:369-371,383-385`); unpriced. |
| INV-003 | HIGH | interaction_effects | The depth-policy remedy changes the remediation route and forces Tier 2 under the legacy engine at Wave 4. |
| INV-005 | HIGH | collection_boundaries | The reach share has no working instrument: the only aggregator globs shadow-run panel manifests and cannot see unreached phases or tasklist consumer output directories. |
| INV-007 | HIGH | count_divergence | "Only `status`, `coverage_pct`, `tier_reached`" is too narrow; two of the three fields are fixed before the engine is read. |
| INV-013 | HIGH | sufficiency_challenge | The replay that decides every disputed point has no ground-truth scorer, no engine selector for arm R, a harness that denies Bash, Agent, Task and `mcp__*`, and no numeric threshold. |
| INV-014 | HIGH | sufficiency_challenge | The consensus does not show consumers receive the panel's benefit without a second entry and without pin changes: no visible benefit path, no panel-to-status map, reflect-owned pins change. |
| INV-004 | MEDIUM | guard_conditions | A call-site depth flag is not "pin-safe": both workflow trees need the edit; "defaults for every other flag" becomes false and is unpinned. |
| INV-006 | MEDIUM | collection_boundaries | The reach-share denominator is undefined (no-run populations, `--budget-remaining` downgrade, forced-deep boundary). |
| INV-008 | MEDIUM | count_divergence | A default flip reaches every UC-1 caller (task-builder PRE gate, auggie-review, troubleshoot), and more than four kinds of `reflect_status` reader exist. |
| INV-010 | MEDIUM | state_variables | "One reflect-side switch" is prose in three places with no staged selector; shadow-first doubles Tier-2 reviewer spend. |
| INV-011 | MEDIUM | guard_conditions | A contract-compat test against the 36-test matrix does not cover the panel lint rules or define a panel-to-status map. |

ADDRESSED with residuals recorded in `merged-output.md` Section 11.2: INV-009 (LOW), INV-012 (MEDIUM; the three diff-based fence tests are working-tree guards, the content pins at `test_shadow_skill_contract.py:146-238` are standing), INV-015 (LOW).

Return contract `unaddressed_invariants` (HIGH only): INV-001, INV-002, INV-003, INV-005, INV-007, INV-013, INV-014.

## Return contract

Status `partial`; convergence score 1.00 (24 of 24 diff points agreed; status BLOCKED_BY_INVARIANTS); base variant `variant-1 (Proposal A; default model, default persona)`; unresolved conflicts 0; fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/consumer-entry-effect-and-delivery/`

- Merged file: `.../consumer-entry-effect-and-delivery/merged-output.md`
- Artifacts folder `.../consumer-entry-effect-and-delivery/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`)
  - `refactor-plan.md`
  - `merge-log.md`
  - `return-contract.yaml`
