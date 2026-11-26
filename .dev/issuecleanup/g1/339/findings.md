# Cross-Validation Report: issue 339

- **Date:** 2026-11-23
- **Template:** installed analyst-cross-validation_report_template.md, extended with the dispatch's required issue-review fields.
- **Claims verified:** 8 assessed: 1 VERIFIED, 6 CONTRADICTED, 1 UNVERIFIED.

## Verdict and evidence
**verdict: in-progress.** Keep issue [339](https://github.com/IronbellyOrg/IronClaude/issues/339) open as a partly delivered umbrella, not a new build from scratch. Reviewed checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` on 2026-11-23.

PR [539](https://github.com/IronbellyOrg/IronClaude/pull/539), merged as `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7`, delivered the read-only sweep and coordinator-loop rule. PR [579](https://github.com/IronbellyOrg/IronClaude/pull/579), merged as `b46ecc1bd47ad817f8cd6181fde0b968dd3f24a0`, restored working-state classification. Actual code still stops at observation: `src/superclaude/cli/sweep/commands.py:269-278` collects and publishes; `src/superclaude/cli/sweep/classify.py:455-504` never authorizes removal. `/sc:closeout` expressly excludes branch/worktree deletion and worker release (`src/superclaude/commands/closeout.md:68-77`), so it does not satisfy the requested `/sc:close`.

## Real current state
- **Implemented:** Orca's coordinator/worker reporting contract, unattended command execution and report files; read-only sweep with a six-hour default; coordinator must keep re-arming its wait and sweep at most every five minutes until its work is settled and inspected (`src/superclaude/core/WORKER-CONTRACT.md:288-290`). This last item is a written duty, not an automatic scheduler supplied by sweep.
- **Implemented beside this issue:** the observer terminal dashboard (PR 503 and later changes), and post-merge closeout (PR 683). Closeout settles issue/report/task records, not branches, worktrees or terminals. PR 700 rolled back the competing issue-655 orchestrator design/build while deliberately keeping closeout. Do not count a previously merged but reverted design as delivered functionality.
- **Partly implemented:** safe cleanup rules exist for the coordinator (`src/superclaude/core/WORKER-CONTRACT.md:233-247`), but the sweep refuses unsafe removal or reports uncertainty, never permission to delete. The source has no `close.md` or dedicated coordinator/orchestrator primitive. No automatic recovery action occurs in the sweep's entry-point flow.
- **Still missing or separate:** the requested checked close/delete operation, blanket permanent orchestrator registration for every future session, periodic replacement chat report, signed narrow delegation and management-server relay. Search of source for macaroon, Biscuit, signed grant, management server, request_close and sc:orchestrator returned no matches. This is absence in this checkout, not proof about external Orca internals.
- **Outdated issue statements:** the 2026-11-07 accuracy table says no sweep, no shipped endless-loop duty and PR 422 open; sweep and the duty now exist and PR 422 is merged. The 2026-11-17 comment is closer but predates closeout, the rollback and coordinator-definition changes. Issue 444 is now CLOSED, not OPEN/deferred as that old comment implies; its closure reason/evaluation completion is UNVERIFIED.
- **Current behavior differs from the original proposal by design:** person-started sessions are observed, never messaged by the sweep; cleanup and retries stay subject to admission/authorization. The repo requires preserving task packages rather than treating every plan/artifact as disposable. The narrow successful-sweep chat-summary exception exists, but it is not a general periodic all-session report (`src/superclaude/output-styles/pragmatic.md:22-26`).

## Validation Results
| # | Claim | Source | Code Path Checked | Verdict | Notes |
|---|-------|--------|-------------------|---------|-------|
| 1 | Sweep is not built. | Accuracy comment, 2026-11-07 | `src/superclaude/cli/sweep/commands.py:214-288` | CONTRADICTED | PR 539 delivered it; default window at line 27 is 6h. |
| 2 | No shipped rule requires indefinite coordinator watching. | Accuracy comment, 2026-11-07 | `src/superclaude/core/WORKER-CONTRACT.md:288-290` | CONTRADICTED | The rule exists, but says Phase 1 adds a duty, not a scheduler. |
| 3 | Working-state classification is broken/inert. | Phase-1 limitations; older docs | `src/superclaude/cli/sweep/classify.py:251-269` | CONTRADICTED | PR 579 restored it. `docs/user-guide/orchestrator-mode.md:69` still carries the stale limit. |
| 4 | Sweep supports the whole recovery/close request. | Original feature request | `src/superclaude/cli/sweep/commands.py:269-278`; `classify.py:455-504` | CONTRADICTED | Observation/reporting only; safe-to-close is not authorization. |
| 5 | Closeout supplies the requested deletion process. | Name-based possibility, not an issue claim | `src/superclaude/commands/closeout.md:68-77` | CONTRADICTED | It excludes branch/worktree deletion and worker release. |
| 6 | All large/restarted Runs are adequately classified. | Original scale goal | `src/superclaude/cli/sweep/probes.py:89,124-167`; `classify.py:272-291` | CONTRADICTED | 50 detailed reads, 100-row list bound and parsed-contract requirement remain; 534/590 own the coverage problem. |
| 7 | Cleanup refuses unmerged/unread/unfinished work. | Later contract evolution | `src/superclaude/core/WORKER-CONTRACT.md:237-247` | VERIFIED | This is coordinator policy; it is not a new close command or a completed automated cleanup gate. |
| 8 | Signed trust layer and management relay are delivered. | Proposed later work in comments | Source-wide keyword search and primitive discovery | UNVERIFIED | No matching implementation found in this checkout; external Orca product behavior and cryptographic designs were not audited. |

## Concrete next steps
1. Coordinator/owner narrows the umbrella's remaining acceptance criteria against the existing watcher/coordinator program; do not rebuild the reverted issue-655 approach. The local unification spec cited by issue 716 is absent in this checkout, so its exact coverage must be read in its owning checkout before implementation planning.
2. Complete issue 590's coverage/classification work under parent 534, with a before/after recorded run. The source still has the 50-read budget; an old owner comment selected paging, while the later 590 pickup comment asks for measurement before choosing. Reconcile those recorded instructions in the implementation plan, not by inventing approval here.
3. Define and build safe close as a separate bounded operation: fresh worktree/branch state, task/report preservation, upstream/push and merge checks, no open PR or unread result, explicit ownership and user approval, then Orca-managed removal. Existing closeout must not be repurposed as if it already did this.
4. Define recovery only on positive stall evidence, never silence or a connection error alone; decide whether permanent coordinator registration, periodic chat reporting and management-server relay are still required or superseded by the current coordinator/dashboard work.
5. Keep trustless nesting and proactive cross-workspace knowledge separate, with the existing worker fan-out boundary intact until an approved design changes it. The review does not grant any of these actions.

## Complexity, size and priority
- **Complexity: complex.** Remaining work crosses session identity, restart evidence, authorization, preserving unmerged work and destructive cleanup; it is not just a missing slash-command wrapper.
- **Size: L.** Estimate applies to the remaining v1 supervision/close/recovery work after removing the delivered sweep and separately tracked v2 features; several coordinated components and live safety checks remain. It is a review estimate, not a measured schedule.
- **Priority: P1.** Incomplete supervision at the stated 10-20-session target causes unattended blockers and risks unsafe cleanup, and issue 423 explicitly waits for v1 completion; no production outage or data loss was established, so not P0.

## Dependencies
GitHub's structured `blockedBy` and `blocking` lists for 339 are both empty. The following are evidence-based functional relationships, not newly created GitHub dependency links:

- **Needs 534 and its narrower 590 follow-up** for useful sweep status across large/restarted Runs before relying on that status for supervision decisions.
- **Blocks 423:** that open issue explicitly says proactive orchestrator v2 is a separate release after v1 issue 339 is complete.
- **Coordinates with 716** (open next-release coordinator backlog) to avoid overlapping scope. It is not proven to be a strict dependency or a replacement for 339.
- **444** is the closed sub-orchestrator evaluation tracker, not an open blocker; the reason it closed is UNVERIFIED. **446** is an open lock-retry improvement, related but not demonstrated as a prerequisite for the report/close design.

## Related issues
- [534](https://github.com/IronbellyOrg/IronClaude/issues/534), OPEN: sweep follow-ups and accepted limits; [590](https://github.com/IronbellyOrg/IronClaude/issues/590), OPEN: detailed-read cap and unread-contract classification.
- [409](https://github.com/IronbellyOrg/IronClaude/issues/409), OPEN: human-facing dashboard; [706](https://github.com/IronbellyOrg/IronClaude/issues/706), OPEN: dashboard follow-ups, not a replacement for supervision actions.
- [423](https://github.com/IronbellyOrg/IronClaude/issues/423), OPEN: proactive v2; [444](https://github.com/IronbellyOrg/IronClaude/issues/444), CLOSED: sub-orchestrator evaluation.
- [446](https://github.com/IronbellyOrg/IronClaude/issues/446), OPEN: bounded index-lock retry; [431](https://github.com/IronbellyOrg/IronClaude/issues/431), CLOSED: weak liveness signals; [668](https://github.com/IronbellyOrg/IronClaude/issues/668), CLOSED: delivered closeout.
- [655](https://github.com/IronbellyOrg/IronClaude/issues/655), CLOSED: competing orchestrator design whose build was rolled back; [716](https://github.com/IronbellyOrg/IronClaude/issues/716), OPEN: remaining coordinator features from that design. These relationships are context, not authority to implement or close anything.

## Related PRs
All numbers below are PRs on IronbellyOrg/IronClaude; each was checked with read-only `gh pr view` or `gh pr list`.

- **539, MERGED**, `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7`: read-only sweep, slash command, worker-loop duty and narrow chat exception.
- **579, MERGED**, `b46ecc1bd47ad817f8cd6181fde0b968dd3f24a0`: restore working-state classification using real Orca field names.
- **587, 588, 589, MERGED:** alignment decision records and corrections, documentation only, not an implementation of the remaining action phase.
- **683, MERGED**, `8b2ce556c691ed53490c1c7f3ab7f56275491c02`: closeout; **700, MERGED**, `471f10511c8e2e8176c0e2088720ece03beca317`: roll back 681/682/684 while retaining closeout and restoring plan approval. These materially change what can be counted as delivered since the issue's last review.
- **503, MERGED**, `9e2608b03857c78ab89fc9439c85256d3bd5d989`: observer release 1. **514, 592, 673, 708, MERGED:** later observer/question/UI/docs changes, states and titles checked, implementation not audited here.
- **754, MERGED**, `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`: remaining live descriptions no longer require a person-opened coordinator; do not copy the older issue comment's definition unchanged.
- Historical foundation, all **MERGED**, individual descriptions and merge states read: **368** (worker contract/P0), **411** (unattended P1), **413** (artifact/report refinements), **383** (setup safety), **380** (issue-slug safety), **417** (P1 records), **403** (permission-mode opt-in), **415** (CLI launches), **355** (tab reopen), **386** (avoid name-prompt stalls), **350** (per-worktree session list), **414** (same-user governed-job identity, not signed trust), **356** (Orca worktree placement). **422 is now MERGED**, `2327fbd37819d4013ffc57511dc4ef5011c3bf27`; the issue's old 'open blocker' entry is stale.

No PR closes 339 through its structured `closedByPullRequestsReferences` field. Search for PRs mentioning 339 also returned 230 due to a test-count match; it is unrelated and not counted as orchestration delivery.

## Verification limits and negative evidence
- Issue body, all six returned comments, current state, structured dependencies and closing-PR field were read. The dated history reconstructed here comes from those comments and PR merge metadata. **Full GitHub event timeline: UNVERIFIED**, because the allowed `gh issue view/list` surface exposes comments and selected fields, not timeline events; the brief forbids `gh api` and other GitHub access. No forbidden fallback was used. Missing events may contain additional cross-references or reasons for closure; no claim of complete event history is made.
- `gh issue view` initially rejected combining `--comments` and `--json`; recovered with the `comments` JSON field. No issue data was changed.
- Negative searches: source-wide terms macaroon/Biscuit/signed grant/management server/request_close/sc:orchestrator yielded no matches; primitive discovery found only closeout, not close or coordinator. The local spec path cited by 716 was absent; **its latest detailed decisions are UNVERIFIED**. Issue 716's long body was returned in a saved tool result, and only its opening context was used, not an invented synthesis of the unread remainder.
- The narrow static analysis completed through the Skill tool; evidence is `analyze/analyze-report.md`, with contract and handoff beside it. No tests, live sweep, destructive cleanup or cross-session security experiment ran. Historical PR test claims were not re-executed.
- The current guide has stale wording (working class and person-opened coordinator). Source and current contract take precedence. No cleanup or correction was applied as part of a report-only task.
- No GitHub write, git staging, commit, push, HEAD move or source edit occurred. All task writes are within `.dev/issuecleanup/g1/339/`. This report recommends an issue disposition; the coordinator alone decides any outward action after owner approval.
