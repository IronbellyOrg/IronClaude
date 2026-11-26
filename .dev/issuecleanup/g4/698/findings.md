## Verdict
still-relevant.

Reviewed on 2026-11-24 at checkout `a7ae3dd30`. Live issue [#698](https://github.com/IronbellyOrg/IronClaude/issues/698) is OPEN and has no comments. Both reported behaviors remain in the checked-out code:

- Release creates the session's `.ok` file without reading an approval record: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_pipeline/release.py:38-66`. Its CLI delegates directly at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_pipeline/cli.py:201-215`. The guard still relies on matching command text, now at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:445-455`, explicitly noting constructed names are not matched. This is a same-user guardrail, not proof of an independent authority boundary. No bypass was attempted.
- Approval accepts a current assignee login OR an explicit approver account id: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_pipeline/stage_predicates.py:130-138`. Both label and comment channels use it (lines 180 and 208). `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_pipeline/cli.py:344-371` passes the current assignee snapshot and reports the host-login flag without refusing it. A comment posted after the plan, still unedited and otherwise valid, can become eligible after its author is assigned; no historical-assignment check is present in this evaluation path.

The historical story needs correction, not closure: PR #697 is CLOSED without merging; merged PR #700 restored the package (`471f10511c8e2e8176c0e2088720ece03beca317`). Merged PR #701 (`0a46644576a31f0f62b9629b0f095b213027cdf6`) explicitly excludes both approval/guard design questions. The later guard changes from commit `2ea524514` do not remove the two behaviors above. PR #686 is now CLOSED, not an open draft.

The issue's assertion that nothing runs because the watcher is disabled is historical, not verified deployment evidence today. Current source includes automatic first-run enabling; live config, deployment state, installed hook version, owner acceptance of the assignee branch and the referenced unification-spec rulings are UNVERIFIED. Existing same-login and release tests were inspected, not executed. The analyze report is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/698/analyze/analyze-report.md`.

## Complexity and size
complexity complex; size M. Two owner policy decisions cross the release helper, both approval channels, guard source/plugin copies, tests and the runbook; size assumes a scoped policy-and-regression change, not a new separate-account isolation service.

## Priority
P2. This is an unresolved approval-trust decision before relying on automated plan release, with no observed exploitation or verified live exposure; release permits implementation, not commits or pushes, and the shared-login limitation was already documented. Escalate urgency if live use is confirmed to depend on independent owner authorization.

## Concrete next steps
1. Have the coordinator obtain the owner's chat decision on both existing acceptance criteria: the release trust boundary and whether current-assignee approvals remain accepted. Check the referenced unification decision record first; do not invent approval or treat another agent's summary as the owner's ruling.
2. For release, implement and test the chosen behavior, or explicitly record acceptance of the same-user, honest-mistake guardrail. An approval-row check is useful defense in depth, but worker-writable rows cannot prove independent authorization. Do not claim extra text matching fully closes constructed or imported calls.
3. For approvers, either document and test retention of the assignee branch, or require the chosen explicit-account/historical-assignment policy. Cover both label and comment channels, an old comment whose author becomes an assignee later, edited comments, wrong plan hashes and same-host-login cases. Clarify whether historical assignment is required in addition to account-id allowlisting.
4. Keep a separate independent review for any guard edit and verify both distributed hook copies. Update the runbook to the actual selected rule; do not broaden this issue into the watcher redesign or the worktree lifecycle issue.
5. Replace historical issue/PR status claims with the verified state above. Current watcher deployment state and any previous owner acceptance still need verification by the coordinator before a safety claim or switch-on decision.

## Dependencies
No strict prerequisite issue number was established. The direct prerequisite is the owner's two recorded policy decisions, plus separate guard review if the hook changes. Issues #716 (coordinator roadmap) and #717 (watcher roadmap) are coordination touchpoints for approval and rollout; neither live issue establishes that all its work must wait for #698. Do not invent a global rollout blocker from this relationship. Issue #699 is a parallel worktree-lifecycle question, not a prerequisite to fixing approval eligibility.

## Related issues
- [#699](https://github.com/IronbellyOrg/IronClaude/issues/699), OPEN: claim worktree created without its agent; companion finding from the same review, a distinct decision.
- [#716](https://github.com/IronbellyOrg/IronClaude/issues/716), OPEN: next-release coordinator features; references #698 and distinguishes Orca terminal release from guard release.
- [#717](https://github.com/IronbellyOrg/IronClaude/issues/717), OPEN: next-release watcher features; references the same review and separate future token-scope work.
- #655: historical orchestrator work underlying removal PR #682 and rollback PR #700. Its current live issue state was not fetched and is UNVERIFIED. It is context, not evidence of completion.

## Related PRs
Live metadata and bodies were read for every PR named in #698, plus the restoration follow-ups discovered in #697:

- [#584](https://github.com/IronbellyOrg/IronClaude/pull/584), MERGED: original approval core, `b6d038a30c15ebeab5797c7b039500ee5dc6bb63`.
- [#591](https://github.com/IronbellyOrg/IronClaude/pull/591), MERGED: coordinator handoff and guard design, `6af80d6c04f74d7c1db196f467e09c1d937d5503`.
- [#682](https://github.com/IronbellyOrg/IronClaude/pull/682), MERGED then rolled back by #700: removed approval package, `01e7a9e23519fd54bc438bb1a1a0e03dcdae5baf`.
- [#697](https://github.com/IronbellyOrg/IronClaude/pull/697), CLOSED, unmerged: source of the findings; comments explicitly leave guard bypass and approver policy for #698. Its final comment identifies #700 as the actual restoration. Inline review-thread contents were not independently fetched because the allowed GitHub commands do not expose that full surface; the issue, PR comments and live source substantiate the findings.
- [#700](https://github.com/IronbellyOrg/IronClaude/pull/700), MERGED: actual restoration, `471f10511c8e2e8176c0e2088720ece03beca317`.
- [#701](https://github.com/IronbellyOrg/IronClaude/pull/701), MERGED: contract carry-over and issue-bound approval-line check only, `0a46644576a31f0f62b9629b0f095b213027cdf6`; explicitly leaves #698 and #699 open.
- [#686](https://github.com/IronbellyOrg/IronClaude/pull/686), CLOSED, unmerged: watcher redesign cited by the wider review, not a fix for #698.
- #707: local history attributes later watcher/guard work to `2ea524514`; its live PR body/state was not fetched in this run and is UNVERIFIED. The actual current release and approver implementations, rather than an assumed PR outcome, determine this verdict.

Searches: allowed read-only `gh pr list` search for 698 found #701 and unrelated older matches; source/history inspection found no change to the two remaining behaviors. A GitHub API-limit warning appeared during related-issue reads, so no further GitHub expansion was attempted. No tests, runtime bypass, approval forgery, installs, commits, staging or GitHub writes were performed.
