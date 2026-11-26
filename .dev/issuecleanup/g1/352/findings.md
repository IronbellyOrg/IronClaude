# Issue #352 review

Governing structure: the coordinator's TASK brief, fields in its numbered report requirement. Scope: read-only review, 2026-11-23.

## Verdict and evidence
**still-relevant**. Keep [issue #352, flaky ccsession shim tests under load](https://github.com/IronbellyOrg/IronClaude/issues/352), open. Adjacent fixes have landed, but no closing PR is recorded and the inspected startup path still uses the same polling shape. This is not a claim that a current flake was reproduced.

- Inspected checkout: HEAD `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/ccsession:1252-1265` discards child output and waits ten checks with 0.3-second sleeps before `shim failed to start`. Lines 1267-1276 separately wait for matching health. The sleeps total about three seconds per loop; probes and scheduling add time, so this is not an exact wall-clock timeout.
- [PR #453, gateway/shim port pairing fix](https://github.com/IronbellyOrg/IronClaude/pull/453), merged as `0423fe5f1feabe5bf826a2a131c1e24a2dadf188`, explicitly excludes the residual startup flake. Retained evidence at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/done/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t5-runs.md:18-29` records a later-port startup failure under 28-worker load; lines 31-48 retain subsequent passing reruns and leave its cause UNVERIFIED.
- [PR #486, issue metadata changes and fallback-port assertion correction](https://github.com/IronbellyOrg/IronClaude/pull/486), merged as `54e21668f6a4887241cb76acc4f770669c5f5a49`, documents residual startup failure as well as the separately corrected wrong-port assertion. The issue's November 12 comment reports failures after #453, and its November 17 comment explicitly reports no fix or new reproduction.
- No active implementation was established: issue assignees and closing-PR links are empty, and narrow PR searches found no dedicated later startup fix. That is negative lookup evidence, not proof that no unpublished work exists.

## Real current state
The launcher already protects other sessions by leaving old/incompatible shims running and choosing alternate ports. It then verifies health identity before using a new shim. Existing startup diagnostics still do not distinguish slow scheduling, a child import/crash, or a lost port race. A longer wait is a hypothesis, not a demonstrated fix.

The tests now avoid the known gateway-port window collision and accept the designed fallback-port family. The remaining load reliability criterion has no current acceptance evidence in this review. The directly started proxy fixture and real-launch tests have different waiting behavior, and real launches still inherit the parent environment. These are investigation targets, not established root causes.

The required analysis ran at the top level through the Skill tool on the narrow source package. Its detailed findings are in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/352/analyze/analyze-report.md`; its worker contract is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/352/analyze/return-contract.yaml`. No production source, tests, GitHub records, shared shims, index, or commits were changed.

## Concrete next steps
1. In a separate diagnostic task, repeat the whole tier-test file under controlled load as the issue requests. Retain the launcher and child logs, process exit state, selected gateway/base/fallback ports, health responses, and relevant inherited settings. Keep unrelated live shims untouched.
2. Split failures by their actual message and failing assertion. Capture whether a child exited, became ready late, or lost its port. Compare an explicitly isolated test environment with the inherited one before assigning an environment-leak cause.
3. Only after reproducing and identifying the failing mechanism, implement the smallest bounded readiness or harness-isolation fix. Reuse the existing health endpoint; preserve identity checks and the tests that prove busy sessions are not interrupted. Add a deterministic test for the demonstrated delayed-start, crash, or contention case rather than weakening assertions.
4. Meet the issue's example acceptance target: 20 consecutive whole-file runs under load without startup failures, plus CI remaining green. A single passing run does not close this issue.

## Complexity and size
**Complexity: medium. Size: M.** The eventual code change may be small, but reproducing a nondeterministic multi-process failure, distinguishing its causes, and proving repeated under-load reliability requires more than a simple timeout edit. This is an estimate of remaining work, not a measured schedule.

## Priority
**P2.** Intermittent failures make local full-suite and release-gate results less trustworthy and consume validation time across unrelated work. No current production outage or hard dependent issue block is established, so P0/P1 would overstate the verified impact.

## Dependencies
GitHub's `blockedBy` and `blocking` fields both returned zero items. No hard issue prerequisite or downstream issue dependency was verified. Issue #443's port-pairing correction is already merged through #453, so it is background, not an outstanding dependency. Reliable test/release validation benefits from #352, but a formal release block is UNVERIFIED.

## Related issues
- [#443, gateway ports accidentally inside shim windows](https://github.com/IronbellyOrg/IronClaude/issues/443): CLOSED, fixed by #453; a different failure message from startup timeout.
- [#341, shared shim killed with its launching terminal](https://github.com/IronbellyOrg/IronClaude/issues/341): CLOSED, fixed by #342; do not conflate lifetime survival with startup readiness.
- [#347, session lists crossing worktree boundaries](https://github.com/IronbellyOrg/IronClaude/issues/347): CLOSED, fixed by #350; related validation context, not a startup fix.
- [#392, retry/failover and retained proxy logs](https://github.com/IronbellyOrg/IronClaude/issues/392): closed work via #481; that PR cites #352 for a separate terminal-lifetime test failure, not proof of this issue's startup cause.
- [#438, issue metadata creation changes](https://github.com/IronbellyOrg/IronClaude/issues/438): completed through #486; its validation supplied later evidence and a fallback-port assertion correction.

The brief names #342 and #350 alongside issues, but both resolve to merged PRs; they are listed below as PRs.

## Related PRs
All PRs below target the authorized fork and were read through allowed `gh pr view` or `gh issue view` calls.

- [#453, test gateway/shim port isolation](https://github.com/IronbellyOrg/IronClaude/pull/453): MERGED 2026-11-08, merge `0423fe5f1feabe5bf826a2a131c1e24a2dadf188`. Partial adjacent correction, explicitly not #352 completion.
- [#486, issue metadata and port-family assertion](https://github.com/IronbellyOrg/IronClaude/pull/486): MERGED 2026-11-10, merge `54e21668f6a4887241cb76acc4f770669c5f5a49`. The issue comment names the assertion change as commit `d16568bd6`; the live PR metadata also references its full hash `d16568bd66d74f19c15585219629b14c9326f3c5`. The current assertion is verified on disk.
- [#481, retry/failover change](https://github.com/IronbellyOrg/IronClaude/pull/481): MERGED 2026-11-10, merge `12d6bb497f8733caa0083f2892529c6575e970a6`. Mentions #352 for a baseline terminal-survival failure, a different assertion from startup failure.
- [#353, release follow-through](https://github.com/IronbellyOrg/IronClaude/pull/353): MERGED 2026-11-03, merge `5e513796b8f2087ef79323dbf928aaa9924508a0`. Explicitly references #352 without fixing it.
- [#342, detach shared shim from terminal lifetime](https://github.com/IronbellyOrg/IronClaude/pull/342): MERGED; closes #341, not #352.
- [#350, worktree-specific session lists](https://github.com/IronbellyOrg/IronClaude/pull/350): MERGED; closes #347, not #352, and records the baseline terminal-survival test failure.

Searches for `352` and `shim startup` found historical and adjacent PRs, not a dedicated current fix. Other search hits (#396, #711, #570, #90, #416, #355, #227, #253) were not treated as evidence of resolution; their full scope is UNVERIFIED in this review.

## Verification limits
- Read the issue body, both live comments, dates, dependency fields and closing-PR references. **UNVERIFIED: complete event timeline and cross-reference event history.** Attempting `gh issue view 352 --repo IronbellyOrg/IronClaude --json timelineItems` failed with `Unknown JSON field: timelineItems`. The allowed issue view surface supplies comments and selected metadata but not the full timeline; the brief prohibits API/GraphQL or other GitHub access. No prohibited fallback was used.
- **UNVERIFIED: current failure rate and root cause.** No tests, CPU stress process, parallel full suite, live shim restart, or 20-run acceptance experiment was run. The required quick architecture command is static; historical failures are explicitly historical.
- **UNVERIFIED: live CI currently green.** PR narratives record earlier CI results, but no CI checks were queried or rerun here. The conclusion does not depend on a current CI-green claim.
- Historical release logs under `/tmp` and local #438 worktree reports were not assumed to exist or treated as newly verified raw logs. The retained #443 run report was read. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/392/baseline-terminal.log:14-22` was read and shows a terminal-survival assertion failure, not `shim failed to start`; it must not be used as proof of startup latency.
- Negative evidence: narrow current-source search found existing startup polling and no dedicated delayed-start/readiness regression name; whole-project absence is not asserted. Recent launcher/test commit history and narrow PR searches did not establish an active #352 fix.
- The development command mirror was absent, while the installed `/sc:analyze` command contained Unattended mode; the brief guard passed on that existing copy. One initial report Edit was blocked by the freshness hook and succeeded after the required Read; no bypass was used.
- Only this task's report directory was written. No staging or local commit was authorized. GitHub was read-only throughout.
