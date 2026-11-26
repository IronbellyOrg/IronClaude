## Verdict
**in-progress**. Keep issue [#572](https://github.com/IronbellyOrg/IronClaude/issues/572) open: the live issue has a substantive 2026-11-18 usage study and provisional recommendations for its eight `rf-*` agents, but not the required current, reasoned disposition of every agent. This is progress in research, not proof that an implementation worker or removal PR is active.

The 2026-11-17 comment's BLOCKED assessment is stale. Part A shipped in #640 (`3f3b34a26280fd3fd64649f5d010f874b1905b65`); the Part B map now exists at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/cleanup/bundle/dependency-map.md:158-168` and explicitly leaves all eight rf agents to #572. The bundle removal merged as #656 (`a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6`) and reached master through corrected release #664 (`64dfc0e8622281a56d6c4e6826c63d50c6959da8`), not the reverted squash #658. Issue #647 is CLOSED.

Real current state: the canonical inventory has **49 agent definitions**, not the historical 48 (50 `.md` files minus README, cross-checked with Glob and tracked-file inventory). The added agent is the restricted workflow reviser from #705 (`1a6c8723fe9e6caa85bfffcdb97b2dc434978bf9`), defined at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/workflow-reviser.md:1-24`. No agent was removed by 6.1.0: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/releases/v6.1.0.md:135-152`; the current retirement table is empty at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_retired_data.py:30-31`.

The remaining work is concrete: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/rf-task-executor.md:6-7,150-168` still names a task skill and `.gfdoc` execution script, while `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/rf-team-lead.md:38-48` still coordinates that task-file pipeline. The nine old canonical skill entry points are absent. Yet `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/SKILL.md:614-627` still uses both rf QA agents. Therefore neither wholesale removal nor treating the old task/doc consumers as present is justified.

UNVERIFIED: the usage study's raw evidence (not found in this checkout), its transcript totals and external project rules; a complete approved 49-row disposition record; runtime behavior; formal GitHub blocking relationships. No tests or install runs were performed under the brief's no-UV/no-outside-writes restriction.

## Complexity and size
**complexity: complex; size: L.** The remaining issue covers 49 agent roles, surviving command/skill references including `refs/`, agent-to-agent links, templates, installer/test inventories, and possible breaking removals; this is much larger than deleting the two low-use candidates mentioned in the usage study.

## Priority
**P2.** Stale task-flow instructions remain and the cleanup evaluation is unfinished, but both cleanup releases already shipped, retained review callers still exist, and no incident or release-blocking dependency was verified; there is no evidence for P0/P1 urgency.

## Concrete next steps
1. Refresh the issue's starting inventory to 49, replace the old wait-for-#571/Part-B note with the merged #640/#656/#664 evidence, and separate completed usage research from still-pending disposition decisions. The coordinator owns any issue edit.
2. Build the current per-agent user map across canonical commands, skills and their `refs/`, agents, hooks, core/rules, templates, tests and installer entries; check development/plugin mirrors separately without staging ignored copies. Record one reasoned keep/refactor/simplify/remove outcome for every current definition, including the newer workflow reviser. The historical eight-agent recommendations are input, not the entire acceptance record.
3. For rf agents, distinguish the removed task/doc callers from retained QA callers and external project use. Review the proposed removal candidates `rf-task-executor` and `rf-team-lead` first, without assuming removal is approved; include cross-agent links and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/unit/test_cli_install.py:53-66`. Re-check the study's external-user evidence before relying on it. Resolve or explicitly account for the retained stale instructions and the leftovers assigned by `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/releases/v6.1.0.md:149-152`.
4. Coordinate the retry adviser's disposition with #393 and leave the eval agents held pending the eval-harness decision described in #572. Preserve existing QA roles and the restricted workflow reviser's tool boundary if consolidating roles.
5. Only after the owner approves concrete changes, plan and implement each removal with reference/test updates, release notes and an upgrade-retirement check. Do not infer that the historical 6.0.0 target or 6.1.0 retention decision authorizes a new removal. No such change is made by this review.

## Dependencies
- **#571 and #647:** historical ordering prerequisites, now satisfied for beginning evaluation. The #571 parent issue remains OPEN administratively, but Part A release #640 and Part B #656/#664 are merged; #647 is CLOSED. Do not wait for #571's closure alone.
- **#393:** OPEN retry-adviser model-selection defect. A role-specific coordination constraint before deciding `implement-retry-adviser`, not a verified blocker on evaluating every other agent. Its latest review explicitly distinguishes overlap from whole-issue blocking.
- **Eval-harness decision:** #572 holds the three eval agents; a distinct numbered decision issue was not verified. Keep this limited gate rather than inventing a blocking issue number.
- **Blocks:** no numbered dependent issue was verified. Formal GitHub blocked-by/blocking metadata is UNVERIFIED because only the brief's issue/PR view/list calls were used.

## Related issues
- [#571](https://github.com/IronbellyOrg/IronClaude/issues/571), OPEN: original cleanup/release plan, with completed releases recorded in comments.
- [#647](https://github.com/IronbellyOrg/IronClaude/issues/647), CLOSED: task/documentation bundle removal and explicit retention of the rf agents pending #572.
- [#573](https://github.com/IronbellyOrg/IronClaude/issues/573), CLOSED: historical documentation-skill findings and dependency cautions, not current proof that removed skills still ship.
- [#393](https://github.com/IronbellyOrg/IronClaude/issues/393), OPEN: retry-adviser selection defect relevant to one agent's evaluation.
- [#536](https://github.com/IronbellyOrg/IronClaude/issues/536), CLOSED: PM startup-promise exception named by #572; not an outstanding blocker here.

## Related PRs
- [#582](https://github.com/IronbellyOrg/IronClaude/pull/582), MERGED, `64e8eacf2b3ff40be07ae9c9959071684c3765a0`: consequence-based review rule and rf analyst/QA rewrites. Relevant retained investment, not an agent disposition decision.
- [#511](https://github.com/IronbellyOrg/IronClaude/pull/511), MERGED, `7764bb6235524694684b426eb1e91c3e32dd0c3f`: codegraph guidance for ten generic specialists; not removal.
- [#509](https://github.com/IronbellyOrg/IronClaude/pull/509), MERGED, `35073356ec1a7f28f8e6c9619eb30eb6b7cc0c84`: issue-worker tier/fallback update. [#516](https://github.com/IronbellyOrg/IronClaude/pull/516), MERGED, `b0977b4f2b7ad2ca19d0048b0774da6fbbac8580`: low effort for the lookup worker. [#518](https://github.com/IronbellyOrg/IronClaude/pull/518), MERGED, `167184c6ba449ab49b7f2af1dc9f4c9080006bd3`: subsequent worker pin and retry-rung changes. These explain why the original agent snapshot must be refreshed.
- [#640](https://github.com/IronbellyOrg/IronClaude/pull/640), MERGED, `3f3b34a26280fd3fd64649f5d010f874b1905b65`: Part A release, no agent evaluation included.
- [#652](https://github.com/IronbellyOrg/IronClaude/pull/652), CLOSED UNMERGED: withdrawn compliance-task command removal, not evidence those commands were removed. [#656](https://github.com/IronbellyOrg/IronClaude/pull/656), MERGED, `a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6`: actual MDTM skill removal; explicitly keeps all eight rf agents.
- [#657](https://github.com/IronbellyOrg/IronClaude/pull/657), MERGED, `5772d21ad01c725665897597e141af081f6e491f`: release paperwork, agent retention and known leftovers for #572.
- Release history: [#658](https://github.com/IronbellyOrg/IronClaude/pull/658) merged as squash `3e6ced3f369c641ff84f21f9421390b3b66388f8`, reverted by merged [#662](https://github.com/IronbellyOrg/IronClaude/pull/662), `0eb96d5c30e6a831c61f101c785a8e1ce54940eb`; corrected merged [#664](https://github.com/IronbellyOrg/IronClaude/pull/664), `64dfc0e8622281a56d6c4e6826c63d50c6959da8`, is the release completion evidence.
- [#705](https://github.com/IronbellyOrg/IronClaude/pull/705), MERGED, `1a6c8723fe9e6caa85bfffcdb97b2dc434978bf9`: adds the restricted workflow reviser, explaining the 49th current agent.
- No dedicated active #572 completion PR was identified by all-state PR search `572` and open search `agent`. This is bounded search evidence, not proof that no differently titled work exists. PR bodies and metadata were read; exhaustive nested review threads and GitHub timeline events are UNVERIFIED.
