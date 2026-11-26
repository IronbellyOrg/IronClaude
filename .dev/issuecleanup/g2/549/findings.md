# Issue 549 review
## Verdict and evidence
**Verdict: in-progress.** Keep [issue #549, Review-Panel Merged Efforts](https://github.com/IronbellyOrg/IronClaude/issues/549) open. Research and comparison artifacts exist in this checkout and the shared helper package exists, but the comparison explicitly is not a sequencing plan and no verified record establishes the owner's worktree close condition.

Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/MERGED-review-panel-unification.md:24-34 records partial convergence, six jointly open points, eight split points and seven historically blocking invariants; lines 74-76 carry unresolved items and explicitly disclaim a roadmap, branch plan or schedule. These are historical report claims, not freshly re-graded blockers.

Research commits verified locally: run 1 `50d4d2b9d1f2288afa497830b3049f2fe48f5c75`, run 2 `ad8f5756044f8bbaab12651b46e7b9835d025faf`. Both report/comparison package paths entered this checkout through merged PR #581, commit `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d` (local path history plus GitHub merge metadata). This supersedes the issue's older statement that this material is only on a private branch or uncommitted folder.

The owner's recorded close condition is the new unification worktree existing and both older worktrees finished and deleted (issue body and 2026-11-14 comment). That transition is **UNVERIFIED**, not presumed complete from a helper library, a merged research PR or the absence of old local checkout names.
## Real current state
**Code state in this worktree (HEAD a7ae3dd30fcf88aaab655c37e94e58e121c2d863).**

- The shared helper package contains 20 top-level Python files. Nine command modules are registered for panel selection, merge, ledger, telemetry, clustering, citation verification, manifest, safety and fixcheck. The registration list also names lint and estimate, but those modules are absent and therefore skipped: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/__init__.py:19-38. The package's `/cli/review/panel.py` name matches the issue's proposed core directory.
- Caller adoption is staged, not complete. The reflect protocol defaults to legacy, shadow runs only measurement and the panel engine is not yet selectable: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-reflect-protocol/SKILL.md:311-328.
- The reflect contract gate moved on from the issue's wording. Recorded 1.8.0 remains supported, and the current frozen contract is 1.9.0: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/panel_lint.py:187-190.
- Newer shared review work has landed since the issue was written: PR #581 (issue 552 stages 0 and 1), PR #582 (consequence-based severity rule and `review fixcheck`), PR #623 (wonsol provisional default, selected via /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/data/review-default.json:1).
- Dependency issues verified open or closed: #520 open, #550 open, #552 open, #531 open, #487 open, #489 open; #346 closed; #488 closed.
- Issue accuracy notes: the "Components Affected" list names files that now exist; its session-tier reference labelled a pull request is actually issue #488, closed; no pull request links to this programme directly; PR #519 is merged.
## Concrete next steps
1. Refresh the sequencing plan against the partial comparison, the seven unresolved invariants, the current 1.9.0 contract and consequence-based grading.
2. Inventory tasklist experiments and fold in the later tasklist commits under [issue #550](https://github.com/IronbellyOrg/IronClaude/issues/550) before any source checkout is retired.
3. Define no-regression gates separately for historical 1.8.0 fixtures and the current 1.9.0 contract; do not rerun the historical 36-case matrix without its recorded fixture set.
4. Verify whether the old research and tasklist checkouts have finished and whether the new unification checkout has been created; record that evidence before closure. This review does not authorize creating or deleting any checkout.
## Complexity and size
**Complexity: complex. Size: XL.** It spans a shared library, several callers, contract migration, experiment evidence and an ordered checkout transition, not a single code change.
## Priority
**Priority: P2.** It blocks coherent sequencing of shared-review adoption and the durable destination and incorporation/re-test route for proven experiment designs, not the experiment inventory itself; it is not a production outage or a security incident.
## Dependencies
- Needs the sequencing and contract decisions recorded in the research comparison and the current reflect protocol.
- [Issue #550](https://github.com/IronbellyOrg/IronClaude/issues/550) depends on this plan for the durable destination and incorporation/re-test route for proven designs. Its experiment inventory can proceed independently and must be complete before the tasklist worktree is deleted (issue body and comments dated 2026-11-17 and 2026-11-24).
- Also depends on the owner decisions named by the comparison's six jointly open points and seven unresolved invariants.
## Related issues
- [#520](https://github.com/IronbellyOrg/IronClaude/issues/520): open feature definition; its body still says PR #519 is unmerged, which is stale.
- [#550](https://github.com/IronbellyOrg/IronClaude/issues/550): open sub-issue; no pull request closes it.
- [#552](https://github.com/IronbellyOrg/IronClaude/issues/552): open severity programme that changed review grading after this issue was written.
- [#531](https://github.com/IronbellyOrg/IronClaude/issues/531), [#487](https://github.com/IronbellyOrg/IronClaude/issues/487), [#489](https://github.com/IronbellyOrg/IronClaude/issues/489): open related work.
- [#488](https://github.com/IronbellyOrg/IronClaude/issues/488): closed tier reorganisation; the issue text incorrectly called it a pull request.
- [#346](https://github.com/IronbellyOrg/IronClaude/issues/346): closed origin issue.
- [#546](https://github.com/IronbellyOrg/IronClaude/issues/546): open but unrelated to this review programme; it is a model-launch policy issue. The tasklist commit's reference to it was not verified as relevant.
## Related PRs
- [#519](https://github.com/IronbellyOrg/IronClaude/pull/519): merged, commit `d2d8a2d166c945f556d921b31530a3673f00df89`.
- [#581](https://github.com/IronbellyOrg/IronClaude/pull/581): merged, commit `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d`; also carried the research packages into this checkout.
- [#582](https://github.com/IronbellyOrg/IronClaude/pull/582): merged, commit `64e8eacf2b3ff40be07ae9c9959071684c3765a0`.
- [#623](https://github.com/IronbellyOrg/IronClaude/pull/623): merged, commit `7f93c0d9f7b72938976127d59a2bf523c06d5e03`.
- No pull request was found by direct search for #549 or by head branch `ironbelly/eval-tasklist-review-panel`. The branch `ironbelly/shadow-runs` is the head of merged PR #581, not a separate open research pull request.
## Verification limits and negative evidence
- Full GitHub timeline events, live Orca checkout ownership and remote branch deletion state are UNVERIFIED. Allowed reads were issue view/list and pull request list/view, plus a local worktree list.
- Local checkouts found: main IronClaude, Coordinator, Issuecleanup, claim-handoff-planb, issue-597, issue-751 and open-decisions. None is named shadow-runs, eval-tasklist-review-panel or a new unification checkout. Absence from this local list does not prove a remote or Orca-managed checkout is finished or deleted.
- The historical 36-case verdict matrix was not rerun. No tests or live review commands were run. The comparison's seven invariant claims were not independently re-adjudicated.
