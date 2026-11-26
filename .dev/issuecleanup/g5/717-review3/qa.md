VERDICT: FAIL
# QA Source Fidelity - Independent watcher review 3

- **Topic:** Issue 717, watcher follow-up bundle.
- **Date:** 2026-11-24.
- **Phase:** source-fidelity.
- **Fix cycle:** 2 / 2, final review.
- **Template:** /home/coder/.claude/templates/modularization-template-review/qa-source-fidelity_template.md. The dispatch requires the additional first-line verdict and consequence-based blocking/minor grading.

## Sources Reviewed

| Source Doc | Assigned Section Range | Line Count |
|---|---|---|
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/findings.md | Entire report, seven headings, W1-W15 and estimates/dependencies | 54 substantive lines |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/analyze/analyze-report.md | Entire architecture analysis | 27 substantive lines |
| https://github.com/IronbellyOrg/IronClaude/issues/717 | Independently retrieved live body, comments, state and timestamp | API JSON, not line-numbered |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/qa.md | Existing acceptance requirements and open evidence blocker, not authority for implementation claims | 64 |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717-review2/qa.md | Prior open blocking finding only; no prior minor findings adopted | Read lines 1-80 |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/return-contract.yaml | Original task evidence requirements/status | 16 substantive lines |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/analyze/return-contract.yaml | Static analysis scope and declared outcome | 6 substantive lines |

Implementation excerpts, tests and runbook were read directly and are cited below. Revision notes were not used. The live issue read succeeded: OPEN, 15 unchecked items, no comments, updatedAt 2026-11-21T15:01:02Z. Its tool result immediately reported the shared 5,000/hour API limit exceeded. No further GitHub calls or prohibited API-limit probe were made; remaining live records are UNVERIFIED, not absent.

## Per-Source Fidelity

| Source | Semantic Coverage | Detail Preservation | Phantom-Coverage Check | Operational Completeness | Verdict |
|---|---|---|---|---|---|
| Findings | All 15 acceptance items covered | Conditional triggers, shared request shape and live gates preserved | Static claims supported; issue read independently verified | Mandatory live PR/current-work verification still missing and explicitly disclosed | FAIL |
| Architecture analysis | All six findings checked against source, including package scope and production entry | Synthetic setup distinguished from real-host acceptance | No additional unsupported current implementation claim found | Valid narrow static review; not a substitute for the larger blocked gate | FAIL for complete package; static content supported |

### Independent source checks

| Claim | Independently read evidence and result |
|---|---|
| W1: first-enabled-poll baseline missing | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:976-1037 performs per-candidate approval checks then launches; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/first_run.py:207-254 initializes/reuses state and compares store bytes, not all prior assignments. Source-wide would_baseline search returned no matches. Supported as a gap, not proof that every older assignment launches. Coordinator hand-over remains UNVERIFIED. |
| W2: quiet-hour request lifecycle missing | Source-wide search for plan_requests, plan_stuck, quiet_since and would_baseline returned no matches; watcher search for held_incomplete returned no matches. Store fields at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/record.py:91-129 and closed reasons at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/audit.py:35-104 support the narrow absence statement. No exhaustive alternative-spelling absence is claimed. |
| W3: poll interval absent from watcher configuration/status | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:59-72,1464-1473 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/defaults.py:32-41 omit the interval. Host scheduler UNVERIFIED. |
| W4: throttle wait not exponential | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/github.py:511-524 uses Retry-After/reset or the fixed ceiling, without a consecutive-throttle input. Supported; ordinary issue retry backoff does not satisfy this acceptance test. |
| W5: fixture versus live acceptance | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/first_run.py:227-254 performs same-process lock contention and reload, not workspace restart. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/issue_watch/test_concurrency.py:146-187 starts two processes and asserts exit 75, one launch total and audit reasons. The runbook at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:235-257 requires real-host tests. Fixture existence verified, its execution and completed host acceptance UNVERIFIED. |
| W6: full shadow-cycle review | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:223-231 explicitly calls for every 24-hour cycle and named reasons. Procedure exists, but no completed shadow record was supplied or verified. |
| W7: read-only token migration | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:670 retains the off-CLI-login trigger. Actual migration/scopes UNVERIFIED; no credential inspection. |
| W8: health is age, not consecutive failures | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:1416-1418,1464-1473 ignores audit and uses cycle age; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cli.py:182-197 exits on that health field. Supported. |
| W9: conditional reads | CLI-tree search found no ETag or If-None-Match. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:672 retains the budget-pressure trigger. Actual need UNVERIFIED. |
| W10: effective permissions not inferred from argv | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/launch.py:136-157 validates the claim prompt and adds no permission override. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:627-628 requires observing the mode and prohibits adding a second approver before the follow-up. Correctly leaves effective mode UNVERIFIED. |
| W11: retry builder/display, not executed recovery | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/launch.py:160-173 builds operation-id retry argv; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:1446-1462 returns it for display. CLI search found only that caller plus definition. Live lost-reply deduplication and owner's retry choice UNVERIFIED. |
| W12: service reducer versus dated review | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:1497-1544 calculates four numbers; CLI search found only its definition, no invocation. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:677 retains seven live days. No enable date or dated review supplied. |
| W13: store entry bound | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/record.py:693-696 prunes consumed timestamps, not finished entries; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:678 retains the greater-than-1-MiB trigger. Actual size UNVERIFIED. |
| W14: network deny-list is not persistence proof | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:49-52,293-295 lists seven network types and applies the check only when mount information exists. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:679 explicitly defers the local-filesystem allow-list. Supported. |
| W15: partial runbook versus captured live rewrite | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/issue-watcher-setup.md:685-699 retains live/shadow/lock/restart gates; :701-713 documents automatic setup. Neither proves a post-S17 rewrite with a named merged PR or the issue-442 runbook's completion. |
| Architecture finding 1: automatic setup enables after synthetic tests | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/first_run.py:149-157 enables on passing checks, and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/dispatch.py:425-436 then checks enabled. Supported as a mismatch with issue 717's stronger gates, not proof of current host enablement or violation of the earlier implementation's requirements. |

The old-approval rejection at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/predicates.py:266-269 is not W1's permanent seen baseline: a later reapproval can pass that date floor. The findings do not falsely say this older safeguard is absent.

Glob independently returned 15 Python files in the watcher package. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cli.py:129 invokes the cycle; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:1318 delegates to _Cycle. The earlier analysis's historical graph timestamp and 5-of-17 sample are UNVERIFIED historical telemetry, not new evidence. This review's own MCP status reported zero changed files; timestamp read afterwards: 2026-11-24T15:04:52Z. No absence conclusion depends on graph sampling.

Local read-only git show confirmed each cited association: 2ea524514 (#707), 4c93b6c73 (#447), ce6608258 (#448), 91375feb1 (#485), d4d1662a8 (#548), 6af80d6c0 (#591), 471f10511 (#700), 0a4664457 (#701), 01e7a9e23 (#682). The #700 subject explicitly names the rollback of #681/#682/#684 and retained closeout. This verifies local history, not independent live PR states, discussions or a complete rollback-diff audit.

### Verdict, complexity, size, priority, dependencies and next steps

The provisional still-relevant verdict is supported by concrete source gaps, not merely unchecked issue boxes. Complex / XL is defensible for the complete 15-item bundle: durable watcher state, a coordinator interface, scheduling/status changes, permission/retry checks, real-host tests and timed operational review. It is not a measured engineering estimate or a claim that each item is large. P2 is defensible as provisional planned reliability/rollout work; reviewed evidence shows no active outage, which does not establish that none exists.

The live issue confirms the shared W2/coordinator-consumer interface, W14 before W5, W5/W6 before enable, W1 hand-over after coordinator availability, W4/W9 after captured replies, conditional W7/W13 triggers, W12 after seven live days and W15 after the live test. The revised next steps retain these constraints, request stage-completion evidence before implementation, reuse the existing watcher, and prohibit treating printed retry commands or absent permission flags as live proof. They authorize no live operation. Related issues' own current states and current plan completion remain UNVERIFIED, so none of these estimates or destinations is accepted as final project triage.

## Overall Verdict: FAIL

The review task is complete, but the underlying findings package still fails its required live-evidence gate. Static claims and the independently read issue support useful provisional triage; they do not close B1. The revised reports correctly keep this limitation visible. This failure does not demand building the feature or executing real-host acceptance during a read-only review.

## Issues Found

### B1: Blocking, Missing and Decision: required live PR/current-work verification remains incomplete

- **Evidence:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/findings.md:33,49-54 leaves every live PR record/discussion, discussion-discovered link and newer implementation PR UNVERIFIED; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/analyze/analyze-report.md:27 explicitly retains that blocker. The original QA and task contract identify this as required acceptance, not optional operational testing. This fresh review retrieved the issue/comments successfully but immediately received the shared API-limit warning, so no additional GitHub reads were attempted.
- **Affected action and consequence:** accepting the full triage as current, then using its verdict, size, priority, dependencies or implementation destination to plan work. A superseding PR discussion or newer implementation could change those decisions; local source and commit subjects cannot exclude that outcome. Disclosure is accurate but does not complete the required review.
- **Resolved part:** the current issue, 15 unchecked items, OPEN state, timestamp and empty comment list are independently verified. Do not continue treating the issue read itself as missing.
- **Remaining evidence:** live PR records/discussions starting with #707, #447, #448, #485, #548, #591, #700, #701, #686, #697, #682, #681 and #684; relevant newly discovered links/newer implementation work; related issue states. This is a starting inventory, not a complete live inventory.
- **Disposition:** FAIL at review 3, after two correction cycles. Escalate the unresolved missing-evidence gate to the coordinator/user; do not start a fourth review or pass the package. Any later recovery needs the coordinator's authorized disposition and actual permitted GitHub access, not a reset probe, alternate-service bypass or GitHub write.

No additional blocking source-content defect was found. No Medium follow-up candidate or form-only correction is required by the evidence checked.

### Notes and limits

- Direct Read of /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md failed because the file is absent here. Exact current-plan completion is UNVERIFIED; the issue's quoted stage requirements are verified as issue text only. Absence is not evidence that a stage failed.
- Related issue bodies/comments/current states, live PR discussions, newly discovered links and newer implementation remain UNVERIFIED under the API blocker. The review did not infer PR state from commit subjects.
- Host enablement/scheduler, persistent mounts, completed lock/restart/shadow results, effective launched permissions, retry deduplication, owner retry choice, first-enable date, seven-day review, store size and token scopes remain UNVERIFIED. No supplied result proves them; helpers, test fixtures and procedures are not acceptance records.
- No tests, builds, uv/pip, package operations, watcher cycles, credential reads, restarts, scheduler edits, source/findings changes, git staging/commits, GitHub writes or external publication. Only this task's report directory is written.
- Tool recovery: the first Edit of the new QA stub was blocked by the freshness hook because it required a tracked Read; the file was Read and that exact Edit retried successfully. No bypass tool was used. Coordinator checks returned no messages, so no answer acknowledgments were needed.

## QA Complete

Review 3 complete: every W1-W15 implementation claim, six architecture findings, seven findings headings, provisional verdict/estimates/priority, dependencies, ordering and bounded next steps checked. One previously open blocking missing-evidence finding remains; no new substantive source defect was confirmed. Required final disposition is escalation, not a fourth review.

VERDICT: FAIL
