| Status | Result |
|---|---|
| DONE | Independently reviewed the disputed source paths and task authority. Variant 2’s late-launch finding stands, with severity reduced to MEDIUM. |
| NEXT | Correct the deadline path without removing durable-before-launch protection, then verify the slow-save case and the prohibited test skips. |

## Position summary

**Verdict: FAIL.** Variant 2 identifies a real violation of the acceptance requirement that no launch starts after 120 seconds, but HIGH severity is unsupported by the available evidence. Its no-skip finding also stands; its blanket authorization of predicate-helper imports does not.

The classifications below apply the supplied precedence: **Regression > Drift > Necessary deviation > Authorized expansion**. A useful implementation choice does not override an explicit, unamended requirement.

## Steelman of Variant 1

Variant 1 correctly separates at-most-once protection from recovery quality and identifies valuable concerns involving clock rollback, lost launch receipts, event-history ties, and truncated stderr. Its strongest structural observation is that validating operation ids is necessary, although that does not establish that importing a fourth predicate helper was the only permitted solution.

Its confirmation that persistence precedes launch is correct. That ordering proves one safety property, not compliance with the separate launch deadline.

## Steelman of Variant 3

Variant 3 gives the strongest explanation of why some duplication follows the required module boundaries. In particular, consolidating helpers across isolated modules would itself require changing those boundaries.

It also identifies concrete operator-facing gaps: inconsistent kill-switch status and silent omission of some schema-valid unknown entries from the retry list. Its distinction between documented proposals and authorized changes is useful, although it overlooks explicit task instructions for runner timing and reset/status exit codes.

## Strengths claimed

1. **The late-launch counterexample is direct control flow, not speculation about Orca.** The last check permits launch at 119 seconds; persistence can finish at 121 seconds; the next statement invokes the launcher with its full timeout. The deadline helper permits launch only through 120 seconds, while the acceptance criterion expressly forbids later starts. See [cycle.py:410][deadline-helper], [cycle.py:1048][launch-path], and [issue-watcher.md:892][acceptance].

2. **The no-skip finding rests on an explicit instruction and an actual prohibited construct.** The task prohibits skip expressions unconditionally, while the test suite contains a root-dependent `skipif`. A successful non-root run does not remove that contradiction. See [task:188][task-tests] and [test_cli.py:1070][skip].

3. **Variant 2 correctly distinguishes authorized verification scope from a full-suite pass.** The decision register expressly replaces the local full-suite gate with named affected subsets and leaves the full suite to CI. That is authorization for the narrower local gate, not evidence that every repository test passed. See [06-gap-fill-decisions.md:28][local-gate].

### Deadline correction that preserves durable-before-spawn ordering

Keep the pending-state save **before** every launcher invocation. Preserve the immediately preceding document, recheck the deadline after that save, and invoke the launcher only if the cutoff still permits it.

If persistence crosses the cutoff before any spawn, durably restore the pre-pending document under the existing lock. This must remove the new reservation or restore the previous failed entry, avoid consuming the daily allowance, and retain the existing unstamped `budget_exhausted` outcome. If restoration fails, stop without launching and report persistence failure; do not claim that rollback succeeded.

A bare post-save check is insufficient: it leaves a pending reservation that the next sweep abandons as an orphan. Moving the save after the spawn would instead break the at-most-once protection. See [record.py:538][pending] and [record.py:627][sweep].

Add an injected-clock case where pending persistence crosses 120 seconds. It must assert no launcher invocation, restored prior state, no new consumed reservation, and the required budget-exhausted decision. This is a proposed correction, not an implemented or executed test.

## Weaknesses identified in the others

1. **Variant 1’s deadline conclusion checks the wrong property.** Save-before-spawn ordering and no-late-launch behavior must both hold. Its “checked once” account of the kill switch is also incorrect: the source contains a second check immediately before the origin/deadline portion of the launch step. See [cycle.py:1033][launch-path].

2. **Neither alternative classification of runner timing survives the task text.** The task expressly orders `time.monotonic()` around the child and says that duration is never used for a decision. This is Authorized expansion, not Drift or merely Necessary deviation. See [task:193][task-tests].

3. **Variant 3 overstates the reset/status production deviations.** The task expressly requires configuration-invalid status exit 2 and platform/configuration reset exit 2. The remaining problem is incomplete documentation, not unauthorized command behavior. See [task:498][task-cli] and [task:501][task-cli].

4. **Both broader cards require qualifications on external-process claims.** The code explicitly marks Orca reply paths UNVERIFIED. Captured-pipe inheritance and leading-dash argument handling are risks to investigate, not demonstrated failures of the actual Orca executable. See [launch.py:39][orca-shapes] and [runner.py:91][runner].

## Concessions

- **Reduce late-launch severity from HIGH to MEDIUM, retaining blocking status.** The acceptance violation is established, but neither its frequency nor a HIGH-impact consequence was demonstrated. Approval checks and durable at-most-once protection remain intact.
- **Correct Variant 2’s import finding.** Three predicate functions are expressly permitted; `valid_operation_id` is a fourth function. Blanket authorization of every predicate name is broader than the task permits. See [task:332][task-record] and [record.py:23][record-imports].
- **Correct the no-skip category under the supplied precedence.** Variant 2 called it Drift. Because the implementation directly contradicts an explicit verification requirement, my final classification is Regression, MEDIUM.
- **Do not present reviewed assertions or recorded gate results as fresh test execution.** No tests or shell commands were run in this review, and no files were changed.

## Shared-assumption responses

| Assumption | Response |
|---|---|
| A-001, decision-register authority | **Qualified acceptance.** Explicit task instructions and registered owner decisions authorize their stated departures. Mere disclosure of an executor choice does not authorize it. |
| A-002, proposal comments as authority | **Reject.** A proposal comment alone proves neither authorization nor necessity. |
| A-003, task as an amending layer | **Accept.** Apply explicit amendments narrowly, then assess remaining contradictions against the unchanged requirements. |
| A-004, reliable card citations | **Reject.** The supplied cards contain stale lines, a wrong source path, and a line-offset error. Conclusions require independent source reads. |
| A-005, source-only findings | **Qualified acceptance.** This review ran no tests or shell commands. Recorded historical results and source-derived counterexamples remain distinct evidence. |
| A-006, complete audited change span | **Qualified acceptance.** I accept the supplied target span as scope, but did not independently reproduce the Git comparison. |
| A-007, verified Orca reply shapes | **Reject.** The implementation itself labels those paths UNVERIFIED. |
| A-008, unstated precedence among requirements | **Reject.** Resolve specific conflicts through explicit amendments. The status-exit task instruction resolves that particular inconsistency; it is not blanket precedence for every conflict. |
| A-009, complete combined coverage | **Reject.** Different reviewer slices and their union do not establish exhaustive coverage. Silence is not agreement. |
| A-010, calibration scores | **Accept as metadata only.** Scores do not decide whether a cited counterexample is correct. |

## POINT TABLE

“Backed variant” identifies the closest supported substantive account, not endorsement of every original label. Confidence concerns the recommendation shown, not the probability of an unobserved production failure.

| Point id | Recommended final classification | Backed variant | Confidence | One-line evidence with file:line |
|---|---|---|---:|---|
| X-001 | **Regression, MEDIUM** | V3 | 96% | Crash exit 1 contradicts the specified `once` exit set and exit-code acceptance criterion; [issue-watcher.md:114][commands], [issue-watcher.md:890][acceptance]. |
| X-002 | **Regression, LOW** | V3, severity only | 94% | A completion reason fills a real gap, but the added name still contradicts the unamended closed-table contract; [audit.py:62][reasons], [issue-watcher.md:718][audit-contract]. |
| X-003 | **Authorized expansion, LOW for three helpers; Regression, LOW for the fourth and overbroad boundary allowance** | V1, partial | 96% | The task names three functions, while the source imports four; [task:332][task-record], [record.py:23][record-imports]. |
| X-004 | **Not a defect** | V3, rationale | 95% | Independent bounds in isolated modules comply with the prescribed import boundaries; [issue-watcher.md:235][boundaries], [launch.py:30][orca-shapes]. |
| X-005 | **Authorized expansion, LOW** | none | 99% | The task explicitly requires runner `time.monotonic()` outside the cycle’s decision clock; [task:193][task-tests]. |
| X-006 | **Regression, MEDIUM; blocking** | V2 | 99% | An explicit unconditional no-skip instruction conflicts with a root-dependent `skipif`; [task:188][task-tests], [test_cli.py:1070][skip]. |
| X-007 | **Regression, MEDIUM; blocking** | V2 | 99% | Persistence separates the final deadline check from an unconditional launcher call; [cycle.py:1048][launch-path], [cycle.py:1061][launch-path]. |
| X-008 | **Advisory gap; actual parser failure UNVERIFIED** | V1, qualified | 94% | The accepted pattern permits a leading dash; validation and shell quoting do not establish Orca option-parser compatibility; [launch.py:36][orca-shapes], [launch.py:127][retry]. |
| X-009 | **Not a defect as alleged; residual timing window is advisory** | V3, partial | 99% | A second kill-switch check exists before the origin call; the “checked once” account is false; [cycle.py:1033][launch-path]. |
| X-010 | **Regression, LOW for the extra two names; correct the accounting** | V1 | 98% | The task requires 57 names, including five authorized additions; the implementation additionally defines completion and crash names; [task:199][task-tests], [audit.py:55][reasons]. |
| C-014 | **Regression, MEDIUM; blocking** | V2 | 99% | The acceptance criterion explicitly says no launch starts after 120 seconds; the save-to-launch interval is unchecked; [issue-watcher.md:892][acceptance], [cycle.py:1061][launch-path]. |
| C-013 | **Regression, MEDIUM; blocking** | V2 | 99% | Root-dependent skipping remains prohibited regardless of whether a recorded non-root run skipped nothing; [task:188][task-tests], [test_cli.py:1070][skip]. |
| C-016 | **Advisory design gap, not implementation drift** | V1 | 97% | Future consumed timestamps are excluded after clock rollback by the expressly required half-open window; [record.py:689][day-cap], [task:338][task-record]. |
| C-017 | **Regression, LOW: incorrect status/error reporting** | V3 | 98% | Presence uses `lexists`, timestamp reporting follows symlinks, and status catches only `StoreError`; [record.py:421][disabled], [cli.py:175][status-cli]. |
| C-018 | **Advisory recovery gap** | V1, qualified | 96% | An ordinary exception bypasses final commit; pending recovery preserves at-most-once behavior, but receipt information can be lost; [cycle.py:685][commit], [record.py:627][sweep]. |
| C-019 | **Advisory external-process risk, UNVERIFIED** | V1, qualified | 92% | Captured pipes and a timeout establish the mechanism, not that real Orca descendants retain those pipes; [runner.py:91][runner]. |
| C-024 | **Advisory integration uncertainty; no demonstrated implementation defect** | none | 96% | Exit-zero JSON with a valid id follows the specified mapping; candidate error-id semantics remain unverified; [issue-watcher.md:633][launch-design], [launch.py:39][orca-shapes]. |
| C-026 | **Regression, MEDIUM at the runner/launcher boundary** | V1 | 97% | Truncation can discard an unknown-outcome marker before classification, contradicting the “anywhere” rule; [runner.py:63][runner], [launch.py:322][outcome], [issue-watcher.md:634][launch-design]. |
| C-036 | **Regression, LOW: schema-valid status edge case** | V3 | 96% | Validation permits a missing working directory, while status silently excludes that unknown entry despite its operation id; normal pending creation supplies the directory; [record.py:184][validation], [cycle.py:1271][status]. |
| C-037 | **Advisory contract inconsistency; no demonstrated requirement for exit-pair validation** | V3, qualified | 94% | Fallback always emits kind `cycle`, while reset instructions both prohibit cycle lines and require this fallback; [audit.py:402][fallback], [task:501][task-cli]. |
| C-034 | **Drift, LOW, limited to documentation omissions** | V3, narrowed | 98% | Task-authorized exit 2 behavior is missing from the runbook’s status list; [task:498][task-cli], [issue-watcher-setup.md:432][runbook-status]. |
| C-022 | **Advisory specification gap** | V1 | 97% | Tie detection scans the complete event history, so later reapproval does not remove an old opposing tie; the task explicitly prescribes that behavior; [predicates.py:205][ties], [task:196][task-tests]. |

**Recommended action:** retain the FAIL verdict and correct the late-launch path first, including durable restoration when persistence crosses the cutoff. Then replace the prohibited skips and reverify the affected requirements.

Skipped: runtime reproduction, live GitHub/Orca checks, and an independent Git comparison. Actual Orca reply semantics and the production frequency of slow persistence remain unverified.

[deadline-helper]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:410
[launch-path]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1033
[acceptance]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:880
[task-tests]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:188
[skip]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cli.py:1070
[local-gate]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:28
[pending]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:538
[sweep]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:627
[task-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:498
[orca-shapes]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:30
[runner]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/runner.py:57
[task-record]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332
[record-imports]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:23
[commands]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:114
[reasons]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:55
[audit-contract]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:718
[boundaries]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:235
[retry]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:127
[day-cap]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:689
[disabled]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:421
[status-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cli.py:175
[commit]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:685
[launch-design]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:633
[outcome]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:322
[validation]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:184
[status]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1271
[fallback]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:402
[runbook-status]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher-setup.md:432
[ties]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/predicates.py:205
