Sub-issue 2 of 3 of #609 (Command Jev Preflight). Step 2 of the recommended order.

## Feature Summary

Run a one-off comparison: about 30 past `/sc:troubleshoot` prompts, labelled by hand, scored against (a) the keyword table after sub-issue 1 and (b) Jev's `--type` answers. The result decides whether sub-issue 3 is built.

## Problem Statement

It is not known whether Jev beats the keyword table at choosing `--type`. Jev latency per call and accuracy on flag-choice questions are UNVERIFIED: no absolute latency figure was found in TypeSafe's docs and no live call was made. Without a measured number, building a preflight component is a guess.

## User Story

As the maintainer, I want a measured accuracy comparison on real prompts, so that I build the standalone preflight only if Jev clearly beats the table.

## Proposed Solution

1. Collect about 30 past `/sc:troubleshoot` prompts from this public repository's own history (public fixtures only), covering all six types plus a few ambiguous ones. Hand-label each with the correct `--type` (or "none fits"). Freeze the labels before running anything.
2. Keyword side: apply the table from sub-issue 1 as written; record the type it returns (or unset).
3. Jev side, following TypeSafe's guidance (https://docs.typesafe.ai/go/primitives.md and https://docs.typesafe.ai/patterns/companion-noul.md): one request per prompt with a Choice over the six types and a companion Noul "does any of these types fit?". Use model `jev-1.14.0`, not the alias. Treat a Noul between 0.3 and 0.7 as "not settled" and leave the type unset; record the probability of every answer; a failed call is an error, never a "no". Keep the question wording in one file.
4. Record per prompt: label, table answer, Jev answer, Jev probability, latency. Report accuracy of each side, the abstain rate, the cost, the median and slowest latency, and the prompts where they disagree.
5. Write the decision: "Jev clearly beats the table" or "does not", with the rule used. Suggested rule to confirm before running: Jev must be right on more prompts than the table by a margin larger than the disagreement noise on 30 prompts, with a median latency the owner accepts for a pre-step. The owner fixes the exact margin before the run.

Needs from the owner before any live call (TypeSafe guidance requires asking first): a yes to sending those prompts to TypeSafe, a budget (under $1 is enough: about $0.00004 per call at $0.042 per million input tokens), and use of `TYPESAFE_API_KEY`. The key is never printed or stored. Public fixtures only; the repository is public and the 2026-11-16 data-sharing hold lift covers it, but private repositories and the open question OD3 in #552 are not covered.

## Acceptance Criteria

- [ ] The labelled prompt set (about 30) is saved under `.dev/` with labels frozen before any run.
- [ ] The decision margin is written down before the live run.
- [ ] Both sides are scored and the per-prompt table, accuracy, abstain rate, cost and latency are recorded in this issue.
- [ ] The decision ("Jev clearly beats the table" or not) is written on this issue and on #609, and sub-issue 3 is updated accordingly.

## Out of Scope

- Evaluating `--depth` or `--scope` (only `--type` is compared).
- Building any preflight command or hook.
- Any gateway rewrite.
- Private-repository prompts.

## Components Affected (from `/sc:analyze`)

- None in the source tree: the output is a labelled prompt set and a result record under `.dev/`.
- Reads `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (the table under test).

## Related Issues/PRs

- #609 (parent: Command Jev Preflight)
- Sub-issue 1 (keyword table fix) must land first so the baseline is fair.
- Sub-issue 3 (standalone preflight) is blocked by this issue.
- #574 and #575: earlier Jev evaluations with the same limits (public fixtures, $50 budget, key never printed).

<!-- sc:issue:create template=issue-feature-simple -->
