## Verdict
**still-relevant.** [Issue 761](https://github.com/IronbellyOrg/IronClaude/issues/761) is a research-and-owner-decision discussion, not authorization to fix 18 confirmed defects. The live issue was OPEN with no comments when read on 2026-11-24; its acceptance boxes were unchecked and no coverage document or decisions were attached there. A read-only all-state PR search for `761` returned no results; that search is not proof that no unlinked work exists. Completion elsewhere, unpublished branches and the assignee's private work are UNVERIFIED, so there is no basis to call the issue in-progress or close it.

The inspected checkout is `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, not a freshly fetched master. Real unresolved research questions remain: the watcher skips a claimed/pending issue before checking stage changes (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:976-982), whereas the coordinator instructions describe relaunch after moving Status back (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:297). The shared worker header applies plan approval to every stage (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt:8-30). These support keeping the discussion, not implementing the suggested replacement workflow.

Some original observations need updating rather than repetition: merged PRs #752 and #754 corrected current coordinator wording, and the contract explicitly permits a person or script to start it (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:71). Live PR discovery also found merged #759 (`f75cf81e3bf9ad61e22bb2e8b81052aba233fc5b`) for the failed-first-run retry bug #751; the local checkout still has the older first-run-only-on-generation path (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/dispatch.py:414-436). Do not present that local behavior as current master. The merged fix's detailed behavior and deployment are UNVERIFIED in this review.

The full 18-entry coverage document, owner decisions and authorized follow-ups are still the issue's deliverables, not deliverables claimed by this quick cleanup review.

## Complexity and size
**complexity complex; size L.** The bounded deliverable is research, but it needs 18 separately evidenced entries across three CLI areas, coordinator rules, claim templates, release decisions and an external Coder component, followed by owner decisions; it is not 18 implementation projects or a small wording fix.

## Priority
**P2.** This planned design review prevents duplicate work and unsupported changes to approvals and automation, but the issue reports potential gaps rather than a verified incident requiring emergency repair; no production outage or emergency dependency was established.

## Concrete next steps
1. Complete the issue's ordered 18-point coverage document at a named current-master revision, comparing that revision with the issue's `0dd726d18` baseline. Preserve the original groups and wording as questions. For each point record fully/partly/not-at-all coverage, implemented versus planned status, evidence links and the remaining question; document the search scope when nothing is found.
2. Incorporate known partial progress: coordinator wording in #752/#754 and the newly merged first-run retry PR #759 for #751. Reconcile each roadmap proposal with the existing R38 decision before calling it approved coverage. R38 is recorded at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64; this discussion does not override it.
3. Obtain owner decisions in chat for the still-open points and record them through the coordinator. Only then update an existing issue or create a follow-up for the chosen remaining work. Do not change approval gates, auto-restart workers, reset watcher claims, push, merge or close anything as a consequence of this review.

This cleanup review is not the complete coverage document and is not evidence that any of those owner decisions has been given.

## Dependencies
No hard prerequisite issue is established for starting this research. Issues #716/#717, #698/#722, #733 and #725 are coverage inputs, not verified blocking dependencies. The owner-decision step depends on the completed coverage document; chosen follow-ups depend on the owner's decisions. Which implementation issues it will block is UNVERIFIED until those choices are recorded. The Coder restart-check question needs external-source verification, not a guessed local-code answer.

## Related issues
Live issue-list state on 2026-11-24, with meaning limited to the discussion's stated related work:

- [#716](https://github.com/IronbellyOrg/IronClaude/issues/716), OPEN: coordinator future-feature list; its body refers to the earlier unification plan. Reconcile with R38 rather than assume adoption.
- [#717](https://github.com/IronbellyOrg/IronClaude/issues/717), OPEN: watcher future-feature list, explicitly says its items are not built. It is not implementation proof.
- [#339](https://github.com/IronbellyOrg/IronClaude/issues/339), OPEN: orchestration across sessions within a worktree.
- [#733](https://github.com/IronbellyOrg/IronClaude/issues/733), OPEN: unattended implementation mode.
- [#655](https://github.com/IronbellyOrg/IronClaude/issues/655), CLOSED: older issue-polling orchestrator design, not automatically adopted by this issue.
- [#698](https://github.com/IronbellyOrg/IronClaude/issues/698), OPEN: text-based release-worker/plan-approval checks and assignee shortcut.
- [#722](https://github.com/IronbellyOrg/IronClaude/issues/722), OPEN: distinguishing owner approval from AI helpers sharing the login.
- [#725](https://github.com/IronbellyOrg/IronClaude/issues/725), OPEN: peer coordinator read-only consultation before asking a person.
- [#751](https://github.com/IronbellyOrg/IronClaude/issues/751), CLOSED: failed-first-run watcher retry, now linked by PR search to merged #759. Do not duplicate it as unimplemented solely from this older checkout.
- [#409](https://github.com/IronbellyOrg/IronClaude/issues/409), OPEN: orchestration dashboard.

Bodies were read for #716/#717/#751 and the target issue. Other entries were checked for live title/state only; their detailed acceptance coverage is UNVERIFIED. The broad related-issue query returned these entries; it was not an exhaustive duplicate search.

## Related PRs
- [#707](https://github.com/IronbellyOrg/IronClaude/pull/707), MERGED, `2ea524514154bde03258a7d7d8a0265c371609af`: zero-setup watcher, stage-specific launch levels, Approved field and guard version 2. Read its body and comments. This implements the baseline, not the 18-point research and owner decisions.
- [#752](https://github.com/IronbellyOrg/IronClaude/pull/752), MERGED, `5bae2f9c35b544c8a76e0e323ff852b5f8b97d72`: current coordinator glossary wording correction; read its body and merge state.
- [#754](https://github.com/IronbellyOrg/IronClaude/pull/754), MERGED, `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`: remaining current coordinator descriptions corrected while dated history was retained; read its body and merge state.
- [#759](https://github.com/IronbellyOrg/IronClaude/pull/759), MERGED, `f75cf81e3bf9ad61e22bb2e8b81052aba233fc5b`: first-run retry for #751, discovered through an all-state PR search for `751`. Only list metadata verified; full body, diff, detailed behavior and deployed state are UNVERIFIED because related reads reached a shared API-rate-limit warning.

An all-state PR search for `761` returned no results. This does not exclude unlinked or unpushed work. Detailed review of other PRs indirectly named by related issue bodies is outside this cleanup triage.
