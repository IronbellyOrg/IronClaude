# Research: issue 326, Git and project workflow integration

- **Topic type:** Issue status review
- **Scope:** Git command, implementation task boundaries, worktree and PR cleanup ownership
- **Status:** Review written; verification limits recorded
- **Date:** 2026-11-23
- **Template:** /home/coder/.claude/templates/modularization-template-review/codebase-research_template.md; task-required fields extend Findings.

## Findings

### Verdict and evidence
**Verdict: still-relevant.** The issue is partly addressed by other work, but its remaining Git refactor and per-task commit feature are not delivered. This is not a recommendation to revive its rejected central relay, and no active implementation of the residual scope was verified.

[CODE-VERIFIED] The current Git entry still contains the generic five-step flow and only smart-commit/interactive options (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/git.md:19-45). Local history identifies its last change as 89df2c1105c01caff199288f949d5783f6594e70 (2026-05-22, formatting), before the issue was opened on 2026-10-29. The current worker contract explicitly says per-task commits inside implement wait for issue 326 (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:42).

Review baseline: checkout HEAD a7ae3dd30fcf88aaab655c37e94e58e121c2d863, 2026-11-23. Live issue: https://github.com/IronbellyOrg/IronClaude/issues/326, OPEN; its project item says In review. That project label does not establish that the residual work is implemented. The last issue comment is dated 2026-11-17; a newer merged cleanup PR materially changes that comment's claim that all branch cleanup remains.

### Real current state
| Area | Real state and evidence |
|---|---|
| Modular Git refactor | [CODE-VERIFIED] Not delivered in the checked-out command: it is still a standalone 91-line instruction file, not activation of a Git protocol skill (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/git.md:19-45). Glob over source skills found no Git protocol package. |
| Per-task commit feature | [CODE-VERIFIED] Still deferred explicitly to this issue (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:42). Implement's task gate writes the completion record and advances without a commit step (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/SKILL.md:149-150). This is distinct from private-index snapshots and a separately authorized end-of-worker-task commit. |
| Worker Git ownership and parallel experiments | [CODE-VERIFIED] Already specified: no outward worker actions, narrowly granted local commits only, and separate worktrees for parallel experiments or colliding writers (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:40-47). Do not rebuild these rules here. |
| Post-merge cleanup | [CODE-VERIFIED] Partly delivered after the last issue update: PR 711 added a person-triggered worktree cleanup command, including guards on merged PRs, closed issues and saved work (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/worktrees.md:15-21). It attempts safe local branch deletion and keeps branches Git refuses to delete, including squash-merge cases (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/scripts/worktree_cleanup.py:2617-2647). Remote branch deletion and universal automatic deletion are not delivered by this path. |
| Submodule operations | [CODE-VERIFIED] No submodule lifecycle procedure is specified in the full Git command (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/git.md:19-91). Searches found defensive submodule handling in retry, sweep and PR conflicts, not an operational management workflow. Do not describe the product as completely submodule-unaware. |
| Central relay | [CODE-VERIFIED] Not an approved implementation target for workers: Git remains on the never-as-worker list (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:23). The issue owner's 2026-11-02 approval comment explicitly rejects the relay. |

No implementation, cleanup operation, staging, commit or GitHub write was performed in this review.

### Concrete next steps
1. Coordinator asks the owner to confirm the narrowed remaining scope, then updates the issue body after authorization: modular Git refactor, explicitly authorized between-task commits, submodule operations, and only cleanup gaps not covered by PR 711. Keep the universal worker relay excluded. This review itself makes no issue edit.
2. Replace stale launch prompts: plugin search uses `/sc:recommend --plugin`, not `--pipeline`; implement has no documented `--depth` option. These surfaces were checked in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/recommend.md:23-42 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/SKILL.md:57-59.
3. Plan the approved residual scope through the existing workflow-to-implement route, keeping planning separate from execution (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/HOW-WE-WORK.md:17-23). Define submodule operations concretely before estimating them as an implementation task; do not introduce a second PR submission path.
4. For per-task commits, test that authorization is explicit, commits occur only after completion and before the next task starts, no commits happen inside parallel batches, hooks can refuse safely, and only intended files plus task evidence are staged. Preserve recovery's unchanged-HEAD requirement during a task (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:35-44).
5. Reuse the existing safe worktree/local-branch cleanup rather than rebuilding it. Decide separately whether standalone or remote branch deletion is actually wanted, and retain explicit authorization for destructive/outward actions. Add tests around any new scope, not another general orchestrator.

### Complexity, size and priority
- **Complexity: complex. Size: L.** Assessment of the narrowed remaining feature, not this review: it crosses a command, the implementation/recovery protocol, submodule behavior and cleanup authorization, with regression tests needed at task boundaries. Submodule scope remains undefined, so L is provisional rather than a time promise.
- **Priority: P2.** Useful workflow reliability and collaboration work, and it explicitly gates the per-task commit extension, but current manual Git, PR submission, worker ownership and safe worktree cleanup already exist; no verified production outage or urgent safety fix requires P0/P1.

### Dependencies and related issues
Live `gh issue view 326 --json blockedBy,blocking,parent,subIssues,closedByPullRequestsReferences` returned zero blocking dependencies, zero blocked issues, no parent, no subissues and no closing PR references. These are formal GitHub links, not proof that no work is conceptually related.

| Issue | Verified state | Relationship |
|---|---|---|
| [289](https://github.com/IronbellyOrg/IronClaude/issues/289), worktree and branch protocol | OPEN | Related cleanup/ownership decisions; not a verified hard prerequisite for refactoring Git. Its old body still describes retired paths, so use current source rules, not that historical text. |
| [339](https://github.com/IronbellyOrg/IronClaude/issues/339), orchestrator for worktree sessions | OPEN | Related coordinator and communication responsibilities; not a dependency to replace with a Git relay. |
| [394](https://github.com/IronbellyOrg/IronClaude/issues/394), launch-level enforcement hook | CLOSED | Related authorization boundary. Do not keep this as an open prerequisite based on its old issue body. |
| [687](https://github.com/IronbellyOrg/IronClaude/issues/687), cleanup of merged worktrees | CLOSED on 2026-11-23 | Partial replacement of the cleanup request, delivered by PR 711; retain remaining Git work rather than duplicating cleanup. |

**Needs:** owner agreement on the residual scope and compatibility with the current worker contract; no specific open issue was verified as a hard blocker. **Blocks:** the per-task commit extension named explicitly by the worker contract, but no distinct blocked issue number is recorded. The old issue comments' P2/P4 sequencing refers to worker-contract rollout phases, not priority P2 and not numbered GitHub dependency links.

### Related PRs and history
All PRs below were read with `gh pr view --repo IronbellyOrg/IronClaude`, except PR search rows used only to discover candidates. All listed PRs are MERGED; none completes the residual Git refactor.

| PR | Delivered relationship | Verified merge commit |
|---|---|---|
| [711](https://github.com/IronbellyOrg/IronClaude/pull/711) | Most important new evidence: safe worktree cleanup plus attempted local branch deletion; merged 2026-11-22, after the last status comment | 6b17a7449f9400a9acc4140d6ce48dec93a9de8e |
| [411](https://github.com/IronbellyOrg/IronClaude/pull/411) | Unattended worker contract and command conversions, constraining Git ownership | cb8f2f81ab7d99c51bcfe81fec8e200b52cf2c86 |
| [356](https://github.com/IronbellyOrg/IronClaude/pull/356) | Orca default worktree locations and self-cleaning evaluation checkouts | 119622e3a78284f83377f920e3858f864ac7e6c6 |
| [344](https://github.com/IronbellyOrg/IronClaude/pull/344) | Issue-body templates and rule, part of communication workflow already supplied elsewhere | c118b5a59d365b894c5f2caa2270ec9986812934 |
| [285](https://github.com/IronbellyOrg/IronClaude/pull/285) | Route PR submission through the existing monitor command | 8d89f307ba0e2449b348fd0467cb8fe8409816dd |
| [287](https://github.com/IronbellyOrg/IronClaude/pull/287) | Origin-first PR target and existing-PR attachment | 7c344d1b81bd07792621664ef347a3eb16a385f1 |
| [288](https://github.com/IronbellyOrg/IronClaude/pull/288) | Always stage task evidence, which new commit handling must preserve | 4eb36b6864083c623a7c27893b3b4e7a738b6c4b |
| [319](https://github.com/IronbellyOrg/IronClaude/pull/319) | Historical command-evaluation research only, not implementation | 2cb683f5c1f0dfbd3c5f169a8b64a432931f718e |
| [329](https://github.com/IronbellyOrg/IronClaude/pull/329) | Codegraph migration phases 1-2, historical orchestration context | 2f10a0e1e43bee841a4143235a92fc16171c9707 |
| [336](https://github.com/IronbellyOrg/IronClaude/pull/336) | Codegraph adoption in primitives, not Git refactoring | 75d0d1e2c23d3abfa60a075ec0c85b4f9b1e047a |

History read: issue opened 2026-10-29; owner expanded requirements that day; 2026-11-02 comments first related the worker-contract proposal and then recorded approval with narrowed residual scope and rejected relay; 2026-11-17 review said the refactor had not started; PR 711 merged 2026-11-22. Source command history remains unchanged since the 2026-05-22 formatting commit.

Bounded search: PR search for 326 returned unrelated historical PR 203; search for the exact Git command in title/body returned only merged recommendation-routing PR 295. Neither is treated as a completion PR. No direct Git refactor PR was verified; search is not an exhaustive proof of absence. Historical issue links pin planning to ce6424924c8879e7835352fce025bb5412728ab3 and approved decisions to 969c770942a8b5d52424e478932b95f370f3b428; those pins are issue-record evidence, not newly verified commit objects in this review.

## Gaps

- **UNVERIFIED: full event timeline.** Read the issue body, all four comments, creation/update timestamps, current state, project state, formal dependencies and closing-PR references. The permitted `gh issue view/list` surface exposes no timeline-event field (`gh issue view --help` lists its JSON fields). Assignment/label history, cross-reference events and edits beyond comment metadata could not be enumerated without an API/browser route outside the brief's GitHub allowlist. No such route was used.
- **UNVERIFIED: work on an unmentioned branch or unindexed external plan.** Local history, source searches and two PR searches did not verify an active residual implementation. This is why the verdict is still-relevant rather than in-progress despite the project's In review label.
- **UNVERIFIED: runtime safety/availability of cleanup or Git operations.** This review did not run cleanup, git mutations or a live implementation session. PR 711 reports an unreadable-process guard that can keep worktrees, and an automation definition that was not switched on; these are PR claims, not runtime checks performed here.
- **UNVERIFIED: complete submodule feature scope.** The owner asks for awareness/functionality without specifying exact operations. Defensive handling does exist, including manual submodule restoration in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:208, but that does not fulfill a general management workflow.
- **Verification limits and recovered attempts:** the project analyze command copy did not exist, so the guard inspected the installed copy and accepted its unattended section. Codegraph was fresh but explicitly cannot index this Markdown target; direct Read/Grep supplied the evidence. No installed tech-research skill folder or issue-specific report template was found in the searched locations; the registered Codebase Research template was Read and used with the task's requested fields. An initial report Edit was blocked by the freshness hook, then retried only after the required Read. No source files changed; no tests or builds were run for this static report.

## Key Takeaways

Keep issue 326 open, but narrow and refresh it before planning implementation. Preserve the Git refactor, opt-in per-task commit extension and defined submodule operations; mark safe worktree/local-branch cleanup as partly delivered by issue 687 / PR 711, and do not revive the rejected universal relay. The report's recommendation is P2, complex, L (provisional scope), with no formally linked issue blocker.

Required quick architecture command ran through the Skill tool on the narrow Git command source. Analysis: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/326/analyze/analyze-report.md. Worker contract and chain handoff are adjacent under its analyze directory. The coordinator owns any later issue edit or follow-up work.
