## Verdict
still-relevant

Keep [issue 731, the reusable BMAD/IronClaude release pipeline](https://github.com/IronbellyOrg/IronClaude/issues/731), open. It is a trial-first backlog item, not a completed pipeline or a rejected direction. Planning exists, but no completed first-release trial or final owner-reviewed reusable specification was verified. The issue explicitly says not to formulate or build the final pipeline before that trial.

Evidence checked on 2026-11-24:
- Current checkout commit: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. The actual executor still recognizes only its existing source/resume/ledger/review options at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/SKILL.md:55-59`. Grep across that entire directory found no unattended, plan-review, plan-only or E-PLAN-NOT-REVIEWED. Issue 733, the proposed unattended executor, remains OPEN; no matching PR was returned by the targeted search.
- The draft branch exists locally. Its pinned commit `fb97f77c1ddd7ef385df5d5730f6f7c17948f9e8` contains the decision record and consensus. Exact copies retained under this report directory preserve branch evidence without switching worktrees. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/731/source-pipeline-record.md:19-24` records issue creation, the panel gate, the unattended work items and a still-trial branching proposal, not a finished reusable pipeline.
- The issue body is stale about the open plan-approval decision: the later record at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/731/source-pipeline-record.md:20` says no human plan approval, only a panel verdict with no blockers. Issue 733's live body confirms this. Its later live comment assigns the separate review-worker gap to issue 734; the branch record confirms that at line 23.
- Existing source is reusable, not a substitute for the missing integration. Its halt and acceptance rules remain real safeguards; this review does not authorize bypassing them. The architecture pass is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/731/analyze/analyze-report.md`.

UNVERIFIED: whether newer remote branch contents exist, whether the first release has progressed outside the inspected issue/source/branch record, and whether the BMAD trial behaviors work. No fetch, build, test or live pipeline execution was allowed. These limits prevent a closure recommendation, not a claim that nothing has ever happened elsewhere.

## Complexity and size
complexity complex; size L. This is a release-spanning integration and trial involving planning handoff, independent review, story execution, progress write-back and branch ownership, not just one document; reuse existing components and size only the pipeline, not all dashboard features.

## Priority
P2. Reuse and reliable release coordination matter, but the final reusable pipeline is explicitly deferred until trial evidence exists; no production outage, data-loss incident or requirement to block all attended development was verified.

## Concrete next steps
Planning is partly done, so the following remain even though the verdict is still-relevant rather than active implementation:
1. The coordinator should reconcile the draft with the already-recorded decisions: no human plan approval; a verified blocker-free plan review gates execution; review and implementation are separate workers once the prerequisites land. Do not ask the owner the answered plan-approval question again.
2. Finish issue 733 before representing story execution as unattended. Issue 734 enables the fully worker-run review stage; until then, issue 733's live comment permits the plan review in a non-worker session. This is not a waiver of plan review or of user-only acceptance after a halt.
3. Use the draft for the first dashboard release trial under issue 727, subject to that issue's scheduling and architecture-first direction. Record every decision and finished phase in the existing append-only pipeline record; correct old entries by appending, not rewriting them. Resolve the still-trial branch naming/topology decisions before using them as settled instructions.
4. After the trial, derive the reusable written specification and only the agents, skills, templates or commands demonstrated necessary, then obtain the owner's review in chat. A second release trial is preferable, not mandatory according to issue 731. The consensus explicitly rejects a new handoff command, spec-review agent, second issue filer and release-planner agent; do not add them speculatively.

These are recommendations only. No source, original decision record, issue, PR or branch was modified.

## Dependencies
- Needs #727 (dashboard two-way roadmap) as the first real release and evidence source before finalizing the reusable pipeline. This is a process dependency, not a claim that every dashboard release through 2.0 must finish first.
- Needs #733 (unattended implementation) for worker-run execution; that capability is absent in the inspected source.
- Needs #734 (unattended stoprule plan review) for an entirely worker-run plan-review stage. It does not block an interim non-worker review or building #733, per #733's live comment.
- No further hard issue dependency or reverse blocking edge was verified. In particular, #731's final reusable spec is not a prerequisite for beginning the authorized draft trial.

## Related issues
- [#727](https://github.com/IronbellyOrg/IronClaude/issues/727): OPEN, dashboard roadmap and first trial context; no implementation before the owner's go, architecture/storage evaluation first.
- [#733](https://github.com/IronbellyOrg/IronClaude/issues/733): OPEN, unattended executor and plan-review gate. Its live comment resolves the review-runner choice into #734, despite stale introductory wording saying that choice remains open.
- [#734](https://github.com/IronbellyOrg/IronClaude/issues/734): OPEN, separate unattended plan-review worker and unchanged review integrity boundaries.
- [#726](https://github.com/IronbellyOrg/IronClaude/issues/726): OPEN, dashboard intervention voting. Its live comment allows two-way direction but waits for #727's storage/architecture evaluation; related product work, not a direct #731 blocker.

Issue 731 and its comment were read in full. Issues 727 and 726 were read with comments; issue 733's relevant requirements and all comments, and issue 734's feature/acceptance/dependency text and comments were inspected. No GitHub writes were made.

## Related PRs
No PR is directly linked or mentioned by issue 731 or its sole comment. The live all-state PR query for draft head `ironbelly/orch-ledger-20261122` returned none; the targeted `733 in:title,body` query also returned none.

Searches for `731` and `"release pipeline" in:title,body` returned PR #539 (merged sweep/coordinator work, commit `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7`) and PR #33 (merged older roadmap-parser work, commit `cd4c9e00e633d4c1480996fbc0db0da89ebb28c2`). Both PRs were viewed; neither implements this BMAD release pipeline, so neither supports closing #731. Search completeness and any unmentioned implementation PR remain UNVERIFIED.

Evidence provenance: the three `source-*.md` files here are unchanged `git show` copies from local branch commit `fb97f77c1ddd7ef385df5d5730f6f7c17948f9e8`, under original branch directory `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/`. They are evidence, not current owner grants. No network branch refresh was performed. The live issue snapshot is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/731/issue-731.json`.
