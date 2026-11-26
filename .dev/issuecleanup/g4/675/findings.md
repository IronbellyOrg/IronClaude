## Verdict
**not-planned**. Issue #675 remains OPEN on GitHub, but its requested work is to account for review findings in the plan for the now-retired #655 design, not to repair a verified defect in the adopted watcher. This is a closure recommendation, not a GitHub change and not a claim that the findings are fixed.

- Live issue #675 has F1-F54 in its body and a later comment adding F55-F68, so the title's 54 understates the scope: **68 findings** are recorded. Its acceptance criteria require a disposition for each finding and reconsideration of the external-file claims marked unclear. https://github.com/IronbellyOrg/IronClaude/issues/675
- Parent #655 is CLOSED. Its [2026-11-21 owner-decision record](https://github.com/IronbellyOrg/IronClaude/issues/655#issuecomment-7089357630) selects merged watcher PR #707, says nothing from the archived orchestrator design is adopted as is, and directs uncovered features to #716, #717 and #718. Its [2026-11-23 closure note](https://github.com/IronbellyOrg/IronClaude/issues/655#issuecomment-7089440080) explicitly closes it as not planned.
- PR #700 merged the rollback of design PR #681 and associated PRs #682/#684, retaining closeout PR #683. Rollback commit: `471f10511c8e2e8176c0e2088720ece03beca317`. The target design document `docs/designs/orchestrator.md` is not present in this checkout. PR #686, the poll implementation that says it fixed selected #675 findings, and PR #690, the plan/re-plan implementation, are both CLOSED with no merge. Their claimed fixes are not delivery evidence.
- Current source at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` reflects the other architecture: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/dispatch.py:348-375,428-475` enumerates repos and runs bounded per-repo children; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:1007-1037` still uses approval/Project checks and a launch-level gate. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/issue.md:30-31,53` supports claim/create, not the retired plan/re-plan mode. The retained `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-closeout-protocol/SKILL.md:18-24` separately describes closeout, which does not establish delivery of the retired orchestrator's wave 8.
- The required quick architecture command ran on the live watcher package; its report is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/675/analyze/analyze-report.md`. Package-scoped searches found no `hold:plan`, `plan_requests`, `merge_safety_files`, `handback` or `reach_daily_max` references. This is bounded negative evidence, not proof those concepts are absent everywhere.

**UNVERIFIED:** the archived additions draft itself, any unmerged branch implementation beyond the PR descriptions, a one-to-one disposition of all F1-F68 into the replacement issues, and live deployment. Do not close this as completed or assert that #716-#718 already preserve every review finding; they track selected features, not a verified replacement for this entire finding ledger.

## Complexity and size
**complexity: complex; size: L** for the original requested work: 68 findings cross plan creation, watcher state, permissions, closeout, merge checks, audit and recovery tests; this estimates the old implementation/planning scope, not the small administrative act of marking the retired work not planned. Exact hours are UNVERIFIED.

## Priority
**P3** for this retired-design follow-up: no active adopted work was verified to depend on completing its old plan, and parent #655 is closed not planned; this does not downgrade an individual safety concern if it is independently reproduced in current code.

## Concrete next steps
1. The coordinator should propose marking #675 not planned, with the parent decision, rollback and replacement-feature links as the reason; only act after the owner's go. Do not describe it as fixed, and preserve its body and comment as the historical finding list.
2. No implementation is requested under this retired plan. If an accepted feature from #716, #717 or #718 encounters one of these concerns, verify it against that feature's actual source and criteria, then give it an explicit disposition there. Do not assume the 68 findings have all been transferred.
3. Do not revive the former design's GitHub writes, interrupts, merge permissions or automatic hand-back from this issue. Runtime validation was not performed, and this report authorizes no such actions.

## Dependencies
- **Needs, historically:** #655, the owner-approved orchestrator specification into whose plan the findings were to go. That issue is now CLOSED not planned, so this prerequisite is retired.
- **Related historical interface dependency:** #668, closeout, is CLOSED and its implementation landed in PR #683; it does not make the rest of #655 current.
- **Blocks:** no current issue was verified as requiring #675 to finish. A complete reverse-dependency inventory is UNVERIFIED; #716-#718 are candidate consumers of relevant lessons, not verified strict dependencies on this ledger.

## Related issues
All issue links below refer only to `https://github.com/IronbellyOrg/IronClaude/issues/<number>`.

- #655: issue-polling orchestrator design, CLOSED not planned; decisive parent scope decision.
- #668: settle a merged PR, its issue and worker, CLOSED; retained closeout implementation.
- #665: 21 Medium review findings for the #655 plan, OPEN; parallel historical review ledger, not a proven duplicate of every #675 finding.
- #674: 70 open closeout-design review findings for #668, OPEN; distinct closeout follow-up, not a basis to mark those concerns fixed.
- #716: coordinator features absent from the selected plan, OPEN; selected-feature successor.
- #717: watcher features absent from the selected plan, OPEN; includes future plan-request work, but not a verified disposition of F1-F68.
- #718: dashboard/report-view features absent from the selected plan, OPEN; selected-feature successor.

Statuses were read live on 2026-11-24. No issue was edited, linked, commented on, labelled or closed.

## Related PRs
- [#700, rollback of the old orchestrator design and build](https://github.com/IronbellyOrg/IronClaude/pull/700): MERGED 2026-11-20, commit `471f10511c8e2e8176c0e2088720ece03beca317`; its body identifies reverted #681 (design), #682 (approval-gate retirement) and #684 (report-skill move). Those three details were verified through the rollback PR, not separate reviews of each historical diff.
- [#707, adopted zero-setup watcher](https://github.com/IronbellyOrg/IronClaude/pull/707): MERGED 2026-11-20, commit `2ea524514154bde03258a7d7d8a0265c371609af`; the parent owner decision names it as the selected design. This is not a claim of deployment or unrestricted launch readiness.
- [#683, retained closeout skill](https://github.com/IronbellyOrg/IronClaude/pull/683): MERGED 2026-11-20, commit `8b2ce556c691ed53490c1c7f3ab7f56275491c02`; source confirms the skill remains.
- [#686, alternative poll waking the repo orchestrator](https://github.com/IronbellyOrg/IronClaude/pull/686): CLOSED, unmerged. It claims fixes to #675 F1/F4/F5/F17/F20/F21/F45 and a choice for F23, but these are unmerged work, not current fixes.
- [#690, plan/re-plan mode](https://github.com/IronbellyOrg/IronClaude/pull/690): CLOSED, unmerged. It describes new plan/re-plan behavior and review fixes; the current issue-command interface still lacks that mode.

A repository-scoped PR search for `675` also returned #628 and #630, both ccsession performance PRs with no demonstrated relationship to these findings; they were excluded as search noise. No PR that completes the F1-F68 disposition requirement was verified. Historical per-finding implementation and test results on closed branches remain UNVERIFIED.
