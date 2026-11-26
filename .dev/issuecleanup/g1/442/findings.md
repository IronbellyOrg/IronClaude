# Issue 442: live launch-level guard observations

Template: findings section structure in ../362/report-template.md, populated for the coordinator's required fields.

## Verdict and evidence
**Verdict: in-progress.** Keep [issue 442](https://github.com/IronbellyOrg/IronClaude/issues/442) open: live observations have landed, but observation coverage and test/result reconciliation are incomplete. Its body and 2026-11-17 comment are outdated, not grounds for closure.

- PR [677](https://github.com/IronbellyOrg/IronClaude/pull/677), merged as `ccf3c461800523921a36bd096f2a35a6f40861a9`, archived the first run; PR [685](https://github.com/IronbellyOrg/IronClaude/pull/685), `cba6ef2145b0aabedda0f66653dadba7671c93fe`, added its runbook, scripts and results. The old claim that none ran is false now.
- Saved results include passes, pending cases and a failure: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/observation-results.md:19-65`, `:204-267`, `:529-550`, `:754-763`.
- All 12 tests still skip unconditionally: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_launch_level_observations.py:79-110`. Issue 442's completion condition is not met.
- PR [709](https://github.com/IronbellyOrg/IronClaude/pull/709), `5e48b98e4ef9fad6f88cc8a29ddb72ae998785ce`, replaced screen-reading with a launch-result file. Closed issue [691](https://github.com/IronbellyOrg/IronClaude/issues/691) records a newer successful live check, backed by `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/691/ob-h2-rerun-logs/gov-log.txt:7-34`. Do not repeat the original OB-H2 failure as the latest evidence.

## Real current state
The following are recorded outcomes, not new live runs. All result-line citations in this table refer to `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/observation-results.md`.

| Observation | Current recorded state |
|---|---|
| OB-H1 item 1, nested-agent identity | PASS, lines 19-42 |
| Item 2, Skill input shape | Pending: only one call captured, lines 44-65 |
| Item 3, Agent/isolation input | PASS, lines 68-94 |
| Item 4, typed implement prompt ordering | PASS, lines 96-149 |
| Item 5, self-started turn wrapping | PASS, lines 151-202 |
| Item 6, TaskCreate matcher | Pending: tool absent from captured log, lines 204-235 |
| Item 7, SendMessage/MCP names | PASS across two runs, updated 2026-11-20, lines 237-260 |
| Item 8, bare Claude child process | FAIL, lines 263-316; parked separately in open issue 678, explicitly not a ship-gate item |
| Item 9, basic tool names | PASS, lines 318-347 |
| OB-H2, launch binding/preflight | Original FAIL was a printed-text check, not absence of refusals (lines 467-476). The newer 2026-11-21 issue-691 run records successful refusals, launch, layer and inode checks in its saved log. Formal acceptance of the full OB-H2 observation remains UNVERIFIED pending reconciliation into the results/test inventory |
| OB-H3, level restrictions | Partial: worktree/full cases recorded; merge refusal PASS in run 2; protected push still pending because the agent declined before the hook saw the call, lines 529-550 |
| OB-CTX, process identity | PASS within the recorded scope, lines 754-763; this does not eliminate every documented process-context limit |

**Built:** the L1 command-text guard is registered at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:63-69` and `:115-122`. It binds launch markers and releases worktree implementation on typed `/sc:implement` or `/task` prompts at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:318-378`. Current source is narrower than PR 583's body, which also named `/sc:task`; use current source for future observation wording.

**Also built:** the L2 Git pre-push layer, delivered by PR 469 (`5f8a1ea2d506fa6a6b8fa5eb335a20140032c64d`), contrary to the old issue pick-up note.

**Still off:** missing-L2 refusal activation at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:855-859`, and governed automatic watcher launches at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/launch.py:48-53`. The latter is coupled to pending observations by `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_launch_level_observations.py:82-105`.

This review changes reports only, not source, tests, hooks, GitHub records, the git index or commits.

## Concrete next steps
1. Reconcile the existing results before rerunning everything: carry the issue-691 live rerun evidence into the OB-H2 record, with explicit acceptance or the exact remaining checks. Preserve the earlier failures as history, not the current headline.
2. With the owner's explicit go, finish the protected-push part of session E against a proven local disposable bare remote, not the real fork. Have the test session independently confirm its push destination before attempting it. A model refusal is not evidence that the hook blocks the call.
3. Capture a second Skill call for OB-H1 item 2. For item 6, either capture TaskCreate or record a checked tool-availability reason for its remaining skip. Do not turn missing evidence into PASS.
4. Keep item 8's failure and its parked disposition linked to issue 678. A fix or a fresh live rerun of that case requires its own authorization; it is not a reason to pretend the remaining test passed.
5. In a separate reviewed change, replace completed items' unconditional skips with recorded evidence/regression checks, retain checked reasons for any remaining skips, and reconcile the watcher gate's four required observations (items 1 and 5, OB-H2 and OB-H3). Changing either activation switch needs its own reviewed owner-approved change, not this report.
6. Have the coordinator update issue 442's obsolete no-observations/no-L2 wording after the owner's go. No GitHub update was made here.

## Complexity and size
**Complexity: medium. Size: M.** The hook and observation scripts already exist, but remaining completion needs a person-supervised multi-session rerun, reconciliation of historical results and current code, and a reviewed test-inventory update. This estimate excludes implementing the separately parked issue 678.

## Priority
**P1.** Missing acceptance evidence keeps governed automatic watcher levels off and prevents the separately approved missing-L2-refusal activation; it blocks confidence in authorization boundaries, not just test polish. Not P0: the automatic gate remains closed and there is no verified current production incident in this review.

## Dependencies
- Needs the result-file workflow from issue [691](https://github.com/IronbellyOrg/IronClaude/issues/691): resolved (CLOSED), PRs 693 and 709 merged; its live-check comment and saved log remove the former screen-parsing obstacle.
- Requires the owner's go and a disposable environment for the remaining live observations; this unattended report does not grant a launch, install, push or session change.
- Blocks governed watcher-level activation (direct switch/test coupling cited above) and the missing-L2-refusal turn-on described in issue [441](https://github.com/IronbellyOrg/IronClaude/issues/441). Issue 441 is CLOSED; that does not mean its activation switch is on.
- Parent issue [394](https://github.com/IronbellyOrg/IronClaude/issues/394) is CLOSED; building the guard did not satisfy this separate live-observation task.
- Issue [678](https://github.com/IronbellyOrg/IronClaude/issues/678) tracks item 8's parked failure, not a required ship-gate fix. It remains part of the result/skip accounting. No other formal dependency edge was verified.

## Related issues
- [394](https://github.com/IronbellyOrg/IronClaude/issues/394), CLOSED: parent launch-level hook feature.
- [441](https://github.com/IronbellyOrg/IronClaude/issues/441), CLOSED: L2 pre-push layer and deferred refusal activation.
- [678](https://github.com/IronbellyOrg/IronClaude/issues/678), OPEN: bare Claude child-session failure discovered by item 8, parked by the owner.
- [691](https://github.com/IronbellyOrg/IronClaude/issues/691), CLOSED: durable launch-result file and successful live reader check.
- Disposable test issues 645 and 679 are named by PRs 654 and 680; issue 712 is named in the issue-691 rerun. Their own issue states were not queried (UNVERIFIED); they are observation fixtures, not product dependencies.

## Related PRs
| PR | Verified status and contribution |
|---|---|
| [432](https://github.com/IronbellyOrg/IronClaude/pull/432) | MERGED, `3b344dd4e0481a9063d4ac22abb24a9e589614a6`: original L1 guard and pending-observation tests |
| [469](https://github.com/IronbellyOrg/IronClaude/pull/469) | MERGED, `5f8a1ea2d506fa6a6b8fa5eb335a20140032c64d`: tested L2 pre-push layer; activation still gated |
| [583](https://github.com/IronbellyOrg/IronClaude/pull/583) | MERGED, `d32465f21b103e52d9e620bafb528c2ac7c46fbc`: removed bare approved release, so original observation wording changed |
| [677](https://github.com/IronbellyOrg/IronClaude/pull/677) | MERGED, `ccf3c461800523921a36bd096f2a35a6f40861a9`: live-run archive |
| [685](https://github.com/IronbellyOrg/IronClaude/pull/685) | MERGED, `cba6ef2145b0aabedda0f66653dadba7671c93fe`: runbook, scripts and observation outcomes |
| [693](https://github.com/IronbellyOrg/IronClaude/pull/693) | MERGED, `dd7bdf2f7fa99ec3a0dc56c4ba8c1fbdaea67873`: producer of durable launch-result JSON |
| [709](https://github.com/IronbellyOrg/IronClaude/pull/709) | MERGED, `5e48b98e4ef9fad6f88cc8a29ddb72ae998785ce`: observation scripts consume the JSON |
| [654](https://github.com/IronbellyOrg/IronClaude/pull/654), [680](https://github.com/IronbellyOrg/IronClaude/pull/680) | CLOSED, neither merged: disposable targets for the live runs, not fixes completing the observation issue |

PR search for 442 returned seven matches with limit 30; PR 258 was an unrelated numeric match and was excluded. PR 583 was found through the issue comment; PR 693 through issue 691. No open completion PR was returned by that query; completeness beyond that search is UNVERIFIED.

## Verification limits and negative evidence
- Reviewed on 2026-11-23 in this assigned feature worktree. Issue 442, its sole returned comment and the related PRs above were read using only allowed `gh issue view` and `gh pr view/list` calls on IronbellyOrg/IronClaude. No fetch, push, issue/PR mutation, install or live launch was performed.
- **Full event timeline: UNVERIFIED.** The allowed issue view/list interface returned issue text, comments and visible status/dependency metadata, not the complete event timeline. No forbidden API query was used to fill that gap. Related PR merge status/timestamps were independently retrieved with PR view.
- **Live safety and gate acceptance: UNVERIFIED beyond the saved evidence.** This is a static review, not a new observation. The newer issue-691 log demonstrates the reader/binding checks, not an automatically accepted complete OB-H2 record. The protected-push gap remains open. Existing observation passes are explicitly attributed to their saved run, not claimed as new results.
- The codegraph index was fresh, but the shell target was absent from its parsed file inventory. The analysis used direct source reads/searches and records `graph:empty`, not invented caller/impact data.
- No test suite ran in this quick static command. The 12 unconditional skips were verified directly in the test source. No source/test fixes were requested or attempted.
- Raw archived screens and every hook event were not exhaustively reread. Saved result blocks, the newer rerun log and associated issue/PR records were checked; no claim that hook execution order is now proven is made.
- Three initial report edits were blocked by the freshness hook before modification (four attempted Edit calls in total). Recovery used tracked Read calls on the new stubs and then surgical Edit calls, without a bypass.
- The task's required architecture analysis is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/442/analyze/analyze-report.md`; worker handoff and contract are supporting local records, not additional product deliverables.
