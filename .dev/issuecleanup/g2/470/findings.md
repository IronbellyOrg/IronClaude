# Issue 470 review

Reviewed 2026-11-24 against checkout a7ae3dd30. Task: task_d67d983d50e9; Dispatch: ctx_acef7c41172a.
Template: ./report-template.md, findings skeleton.

## Verdict and evidence
**Verdict: close (superseded by intentional removal, not fixed).** The research-only workflow whose redesign #470 requested was removed by merged PRs [#650](https://github.com/IronbellyOrg/IronClaude/pull/650) (commit `430eaa87f25c84f6cb319fe66f929e50b96125f0`, removed tech-research) and [#656](https://github.com/IronbellyOrg/IronClaude/pull/656) (commit `a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6`, removed task/task-builder and their named regression test). Release PR [#658](https://github.com/IronbellyOrg/IronClaude/pull/658), merged 2026-11-18 as `3e6ced3f369c641ff84f21f9421390b3b66388f8`, brought those removals to master; all three commits are ancestors of this checkout.

This follows #470's own 2026-11-17 comment: if task and task-builder go, close as superseded. It does not claim every defect was corrected. The schema mismatch survives in retained agents/templates and must be explicitly carried into #572's agent evaluation in any owner-approved closeout. Evidence: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/rf-qa.md:316` requires `created`, `template`, `tracks`, while `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1-40` uses `created_date` at line 12 and does not supply those keys. This is a verified text-contract conflict, not a newly run agent failure.

## Real current state
- GitHub still reports #470 OPEN, with one comment (2026-11-17), no assignee, no labels and no closing-PR reference. Its last reported update predates the 6.1.0 removal.
- Three canonical skills are absent: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/tech-research/SKILL.md`, `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/task-builder/SKILL.md`, `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/task/SKILL.md`. Git history identifies the intentional removals, and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_retired_data.py:83-101` lists all three in retired-install data.
- The issue's test path `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_task_builder_merge.py` is absent. PR #656 expressly removed it with the skills. No resume-state tests were run or claimed fixed.
- The standalone task builder agent remains and still mandates the old complex template: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/rf-task-builder.md:61-84`. All eight rf-* agent files remain. PR #656 and release PR #658 explicitly preserved them and deferred their future to #572. Removing the skills therefore did NOT fix or eliminate every standalone agent/template defect.
- The QA agent's task-integrity trigger still names the removed tech-research stage: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/rf-qa.md:307-316`. Its contradictory header check persists. Current reflect/spec-panel references to rf-qa mean the agent is not globally unused; actual invocation of its task-header check through those routes is UNVERIFIED.
- Inventory bootstrap circularity, unsafe task-builder resume, universal input-allocation machinery and duplicate task-executor QA are superseded on the removed skill route. The old issue-463 generated package and historical FAIL verdicts were not changed or re-executed. Completion-delivery reliability remains a separate open concern under #465/#468, not a demonstrated in-repository implementation fix here.

## Concrete next steps
No implementation is in progress for #470 that this review verified. Recommended coordinator-only next step, after the owner's go: close #470 as superseded by #650/#656/#658, explicitly retaining the unresolved header/schema conflict and standalone task-builder/template relationship under #572. Do not call the old bug fixed, restore removed skills, alter issue-463 history, grant research-entry exceptions or restart its exhausted repair loop. This worker made no GitHub changes.

## Complexity and size
**Complexity: simple. Size: XS** for the recommended administrative closeout and preservation of the residual finding, because the relevant skills and test were already removed and no product-code change is proposed. This is not an estimate for implementing the original multi-skill redesign; any retained-agent repair is separately scoped through #572.

## Priority
**Priority: P3.** The reported research entry path no longer ships and its originating research request #463 is closed, so #470 no longer blocks a supported skill route. Preserve the real remaining agent/schema defect in #572 rather than treating removal as its repair; production impact of that defect through surviving agent callers is UNVERIFIED.

## Dependencies
GitHub's issue fields report no blocked-by, blocking, parent or sub-issue relations for #470. No verified hard implementation dependency remains for its closeout. Logical relation: #571 Part B / #647 supplied the removal decision (now landed through #650/#656/#658); #572 owns the retained-agent disposition and should receive the residual schema finding before closeout. #465 and #468 are related lifecycle concerns, not established prerequisites.

## Related issues
- [#463](https://github.com/IronbellyOrg/IronClaude/issues/463): originating research request, CLOSED on 2026-11-17. The incident history is reported by #470; it was not replayed.
- [#462](https://github.com/IronbellyOrg/IronClaude/issues/462): orchestrator model-default bug, CLOSED / NOT_PLANNED; mentioned by #470's status comment.
- [#465](https://github.com/IronbellyOrg/IronClaude/issues/465): verifier report delivery failure, OPEN.
- [#468](https://github.com/IronbellyOrg/IronClaude/issues/468): orchestration-check spam, OPEN.
- [#571](https://github.com/IronbellyOrg/IronClaude/issues/571): removal/release planning parent, OPEN; broad issue status does not negate the merged Part B removal PRs.
- [#572](https://github.com/IronbellyOrg/IronClaude/issues/572): evaluation of rf-* and other agents, OPEN; body and both comments read. The later 2026-11-18 comment contains usage research, so the earlier claim that no evaluation existed is stale. Usage counts in that comment were not independently reproduced.
- [#647](https://github.com/IronbellyOrg/IronClaude/issues/647): 6.1.0 task/documentation bundle removal, CLOSED / COMPLETED.

## Related PRs
- [#515](https://github.com/IronbellyOrg/IronClaude/pull/515): MERGED 2026-11-12, MCP grants affecting the then-existing task-builder/tech-research skills. Mentioned in #470's comment; metadata and changed paths read, not treated as a defect fix.
- [#582](https://github.com/IronbellyOrg/IronClaude/pull/582): MERGED 2026-11-17, consequence-based review and rf-qa rewrites, commit `64e8eacf2b3ff40be07ae9c9959071684c3765a0`. Mentioned in #470's comment; metadata and changed paths read. Current schema line still conflicts.
- [#650](https://github.com/IronbellyOrg/IronClaude/pull/650): MERGED 2026-11-18, removed tech-research and five documentation skills; body/comments and merge identity read.
- [#656](https://github.com/IronbellyOrg/IronClaude/pull/656): MERGED 2026-11-18, removed task/task-builder/roadmap and the task-builder test; explicitly kept templates and all eight rf-* agents. Body/comments and merge identity read.
- [#658](https://github.com/IronbellyOrg/IronClaude/pull/658): MERGED 2026-11-18, 6.1.0 release into master including those removals; body and merge identity read.
- `gh pr list --repo IronbellyOrg/IronClaude --state all --search '470'` returned no matching PR. #470's closing-PR field is empty. This does not prove no PR ever mentioned it in an event or inline review.

## Verification limits and negative evidence
- **UNVERIFIED: complete GitHub timeline.** The authorized `gh issue view/list` and `gh pr view/list` surface exposes issue dates, comments, dependency fields and closing PRs, but no full timeline/event field (`gh issue view --help` inspected). No `gh api`, browser or other GitHub access was used to bypass the brief's read-only allowlist. Creation (2026-11-09), comment/update (2026-11-17), subsequent removal PR merges (2026-11-18) and present OPEN status are verified; a complete cross-reference/event history is not.
- This is a static quick architecture review. No tests, builds, installs, paid experiments, runtime pipeline execution or delivery-recovery scenario were run. PR-reported test results are not this worker's observed test passes. Historical package metrics, admission failures and inventory deadlock remain incident evidence from #470, not a current replay.
- Negative evidence: direct lookup of the canonical tech-research skill failed because it is absent; Glob and fixed existence checks found no task/task-builder/tech-research skill and no named task-builder test. Git history and merged PR bodies establish intentional removal, not an unexplained missing file.
- Codegraph readiness was fresh at 2026-11-24T02:40:42Z. The grouped layout listing was truncated; Markdown is not indexed, so graph caller/impact tools cannot establish dependencies of these Markdown contracts. Native source searches and bounded Reads supplied the evidence instead. The common ancestor of all five original change surfaces is the requested analyze target `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude`; only the issue area was examined, not every package file.
- **Process deviation:** the initial supporting analyze report was written without the required template/stub-first sequence. This was not retroactively represented as compliant. This findings file was created from the task-local registered skeleton and filled section by section. The first investigation also read GitHub before the brief guard was fully evaluated; no source or GitHub mutation occurred. Those process defects should be visible to the coordinator alongside the usable evidence.
- Only files under this task's report directory were written. No source, historical task package, Git index, branch, issue or PR was changed. Owner approval and any issue closure/transfer remain coordinator responsibilities.
