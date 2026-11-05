# Research: Checks Prove Less Than the Requirement

**Investigation type:** Evidence-backed causal hypothesis
**Scope:** Six selected historical sessions; candidate one, not a final rank
**Status:** Complete, hypothesis for debate; not ranked or independently approved
**Date:** 2026-10-23
**Governing template:** tech-research/SKILL.md, Codebase Research Agent Prompt

## Hypothesis
Repeated discovery is partly caused by checks that establish format, labels or presence while leaving the required behavior unproved. A later reviewer then exercises another already-existing failure path. Large units and deferred lasting tests amplify this gap; they are not independently proven universal causes.

## Exact Mechanism
1. A behavioral requirement is represented by a weaker check: parsing, a keyword, a count, a marker, or the presence of a validation step.
2. Implementation and early review accept that narrower evidence without establishing execution order, semantic inputs, cross-component use, or exceptional paths.
3. The fix closes the demonstrated example but does not make the whole behavioral requirement executable at the current task boundary.
4. A later review finds another preexisting counterexample. This explains new discoveries without assuming the prior fix caused them.

## Supporting Incidents and Primary Evidence
**Counting:** Multiple examples within one incident are not independent session observations.

Paths below are primary-source locations recorded and checked in the linked case reports; historical raw anchors mean physical JSONL records, not current product-file lines.

| Incident | Observed mechanism | Research and primary anchors |
|---|---|---|
| Oracle semantics | Family counts, labels and one-field differences pass while known/unknown author and default-path security meanings are wrong. Initial67/78 tests pass despite four valid defects. | [Oracle case](../research/02-session-a9b88895.md), sections4-5; `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl:291`; preserved reviews under its task package `artifacts/t12-review-1.md:20-22` and `t12-review-2.md:20-40`, absolute package path in the case evidence register. |
| Orca monitor task | One640-line workflow combines three jobs and many behaviors; current acceptance checks are structural while lasting behavior tests are deferred to Task14. Later checks find originally present range, summary and size defects. | [Monitor case](../research/05-session-e002bed2.md), sections2-5; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl:585`, `:804`, `:906`, `:1021`; plan `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/TASK-WF-designSpec-20261022-132541.md:209-232`. |
| Orca plan coverage | Coverage credits an up-to-date state that original tasks do not name; validation exists after the fetch that uses its input. Presence is mistaken for correct wiring or timing. | [Planning case](../research/01-session-ac2cd1fd.md), section4; first review `artifacts/coverage-matrix.yaml:1749-1757` under `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/`; second merged findings in sibling `pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml:39-47`. |
| CI search and advisory checks | PR creation arguments are asserted, but the search stub ignores search filters; stronger phrase blacklists still accept contradictory advisory wording. | [CI planning case](../research/04-session-43582de1.md), sections6 and final-outcome supplement; `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md:117-129`; original plan and final probe comparisons are preserved in that case. |

## Counterevidence
- The oracle's three permitted repairs worked; its second failure repeats the one deliberately frozen input defect. Weak checks explain initial escape, not the authorization barrier that prolonged that specific finding ([oracle case](../research/02-session-a9b88895.md), sections4-6).
- Smaller monitor Tasks10/11 converged after one repair using the same general arrangement. Task size/deferred testing is an amplifier here, not proof that independent review cannot converge ([monitor case](../research/05-session-e002bed2.md), section6).
- New plan defects and the stdout-trap regression have actual repair introductions. They cannot all be explained as earlier undetected behavior.

## Scope, Overlap and Competing Explanations
This candidate explains why previously wrong behavior survives apparently successful verification. Candidate two explains a different event: the repair introduces an interaction or fails to cover sibling paths. Candidate three explains changing judgments, not the missing original behavior itself.
Frozen fixtures, unavailable render tools and defective evidence pointers are competing immediate blockers. They may coexist with weak verification, but do not become instances of this hypothesis merely because a review fails again.

## Discriminating Test
Use preserved historical versions, not mutable current files, and keep original acceptance criteria and review policy fixed.
- For each later finding, construct its minimal counterexample on the version that first passed the existing checks.
- Run the described check against the counterexample and ask whether it still passes; separately verify whether the relevant behavior test was deferred or absent.
- If the original checks reject these wrong behaviors and were actually used, this mechanism weakens. If examples pass weak checks but fail a criterion-derived behavioral check, it strengthens.
This is a proposed bounded test, not a run performed for this card; it must not relax valid criteria or replace independent final review.

## Provisional Evidence Strength and Limits
Strong case-specific support across oracle, monitor and both planning examples: concrete bad states satisfy weaker predicates or remain outside scheduled tests. The monitor size and deferred-test contribution is observational, not a controlled size experiment.
The sample is clustered and selected by recent file modification. No causal rate, probability, model comparison or claim that every new finding was missed initially is established.

## Key Takeaways
- A passing check can be genuine yet too weak for the requirement; validation presence is not validation timing, and fixture labels are not fixture meaning.
- Discovery of another old counterexample is not evidence that the preceding repair introduced it.

## Gaps and Questions
Why particular reviewers missed some counterexamples remains unknown. The contribution of task size versus the number of behavioral paths is not isolated. Historical tests were inspected, not rerun here.

## Stale Documentation Found
Historical coverage rows over-credit some behavior, and source test inventories omit requirements described elsewhere. These are specific historical findings in the case reports, not proof current production documentation is stale.

## Summary
The evidence supports a recurring gap between what checks prove and what the task requires. That gap permits progressive discovery of old defects, particularly when lasting behavioral tests are deferred. Its relative likelihood against the other four candidates remains for the actual debate.
