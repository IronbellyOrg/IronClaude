# Research: Local Repairs Miss Connected Effects

**Investigation type:** Evidence-backed causal hypothesis
**Scope:** Six selected historical sessions; candidate two, not a final rank
**Status:** Complete, hypothesis for debate; not ranked or independently approved
**Date:** 2026-10-23
**Governing template:** tech-research/SKILL.md, Codebase Research Agent Prompt

## Hypothesis
Some repairs are checked against the reported symptom without tracing the connected execution paths, dependency order, data sources and unchanged constraints. The repair can therefore introduce a new defect or leave a sibling failure intact. This is demonstrated in selected changes, not inferred from every later failure.

## Exact Mechanism
1. A finding proposes a local remedy, such as adding a test, earlier validation, an error trap or a simpler dependency edge.
2. The amendment crosses a boundary: a test needs a later artifact, two stages have different contracts, or diagnostic output shares a captured data stream.
3. The remedy is accepted without proving the affected neighbors and original invariants still hold.
4. Subsequent review exposes the new interaction, or another untouched path in the same requirement family.

## Supporting Incidents and Primary Evidence
**Counting:** Several repair interactions from one plan are not independent session observations.

Historical plan defects are distinct from runtime regressions. The linked reports reconstruct successful writes and edits, excluding blocked attempts.

| Repair and connected effect | Before/after conclusion | Research and primary anchors |
|---|---|---|
| Add inventory regression test | Original plan did not demand the new comparison at that point. Revised Task13 requires it before Task14 registers the workflow, making intermediate acceptance unsatisfiable. | [Orca planning case](../research/01-session-ac2cd1fd.md), section3.3 and full16-repair supplement; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl:544-545` writes historicalv2, `:841` writesv3; second merged findings `pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml:120-128` in the Coder worktree's `.dev/reflect/`. |
| Reuse four-asset predicate earlier | Detection originally distinguishes release existence from pin-writer eligibility. A recommended stronger early predicate changes which job rejects the release. | [Orca planning case](../research/01-session-ac2cd1fd.md), section3.1; same planning log `:544`; `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml:75-83`; original source `:316` versus `:245`, full path in case evidence register. |
| Capture old digest before mutation | The timing fix chooses deployed-package provenance where the companion field contract specifies the recipe. A locally plausible source crosses a contract boundary without declaring the substitution. | [Orca planning case](../research/01-session-ac2cd1fd.md), section3.2; same log `:544`; second merged findings `:57-65`; companion requirements `:302`, full path in case evidence register. |
| Inherit pin-job error trap | First repair enables inherited traps and writes errors to stdout. A failed command substitution captures the annotation as data and may emit it again outside. This is a proven implementation regression. | [Monitor case](../research/05-session-e002bed2.md), section5.2; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl:759-762` successful introduction, `:1240` reproduced failure; workflow `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.github/workflows/orca-upstream-monitor.yml:413,422-428` at analyst observation. |
| Repoint overly serial dependencies | The original safe chain includes earlier edits. Revised graph loses required ancestors. The intended executor's sequential order prevents proven runtime reordering, but does not repair graph conformance. | [CI planning case](../research/04-session-43582de1.md), section7 and eight-entry addendum; original/regenerated plans under `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/`; regenerated `TASK-WF-specR1-20261023-031725.md:138,153,172`, source `:82`; exact package paths in the case. |

## Counterevidence
- The corrected first-round ledger records fourteen original planning amendments accepted and two partial. Several non-recurring fixes worked; this hypothesis must not turn twenty numbered later items into twenty repair regressions ([planning case](../research/01-session-ac2cd1fd.md), complete original-repair supplement).
- Most later monitor defects already exist in its first workflow. Removing an argument-size failure exposes later preexisting output limits rather than creating them ([monitor case](../research/05-session-e002bed2.md), section5.3).
- Oracle repairs resolve three defects, and credential FINAL repairs change evidence only. Their recurring failures need other explanations, not this mechanism.

## Scope, Overlap and Competing Explanations
Two outcomes must remain separate: demonstrably introduced connected defects, and incomplete coverage of an existing failure family. Evidence for the latter alone does not prove a regression.
Weak behavioral checks can allow the connected problem to escape, so candidate one can precede this mechanism. Changing criteria can create an apparent conflict without damaged behavior, so candidate three must be tested separately. This candidate is an impact-analysis mechanism, not an explanation of reviewer cognition.

## Discriminating Test
For each alleged repair regression, replay only confirmed successful edits against the preserved immediate pre-fix state.
- Hold the original criterion and policy fixed; identify the affected producer, consumer, sibling path or dependency edge.
- Require a counterexample absent before the edit and present afterward, with an explicit data-flow or ordering explanation.
- Check the proposed remedy against unchanged constraints and neighboring paths before another broad review.
If the failure already occurs before the edit, reclassify it as retained or previously missed. A finding newly phrased after a fix is not enough.
This is a proposed historical replay, not production execution or proof that smaller diffs alone prevent regressions.

## Provisional Evidence Strength and Limits
Strong direct introduction evidence for selected plan interactions and one shell data-flow regression. The CI graph defect has a runtime safeguard, so its impact is plan conformance rather than observed execution disorder.
This does not explain the majority of later monitor findings or unchanged environmental/frozen-input blockers. No claim about every repair, context limits or general model ability follows.

## Key Takeaways
- Several fixes genuinely introduce connected defects; the evidence includes original state, successful amendment and next counterexample.
- Path-specific repairs also leave sibling failures intact, but those retained defects must not be counted as new damage.

## Gaps and Questions
No controlled experiment isolates impact review from task complexity or reviewer selection. Some proposed later repairs were not applied. The monitor regression was later accepted with known defects, not shown repaired; the separately timed continuation preserves that distinction.

## Stale Documentation Found
Some reviewed proposals violate existing source distinctions or create contradictory dependency/testing instructions. This card describes historical amended plans and code payloads, not a claim all corresponding current files remain defective.

## Summary
Missing connected-impact analysis explains a specific subset of fix-to-new-failure transitions. It is directly supported for plan ordering/source-boundary mistakes and one stdout error-trap regression. It does not justify attributing every later finding to the immediately preceding fix.
