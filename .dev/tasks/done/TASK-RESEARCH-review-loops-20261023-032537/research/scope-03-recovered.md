# Research: Review-loop session scope, indexes 13-18

**Investigation type:** Pattern Investigator
**Scope:** session-manifest.txt indexes 13-18 only
**Status:** Complete (scope discovery only)
**Date:** 2026-10-23

---

## Method and evidence boundaries
Scope discovery only, frozen manifest indexes 13-18. Parsed each original JSONL record with UV-run Python, retaining original physical line numbers and timestamps in focused excerpts. Scanned actual user command-name envelopes and assistant Skill calls, then focused review dispatches, tool outputs, and assistant reports; injected skill bodies/policies/examples were not counted as events. Full top-level scans covered 750, 384, 2095, 129, 4355, and 1451 records respectively; selected excerpts rather than giant serialized lines were read. Nested reviewer finals and five on-disk package artifacts were checked directly. No production files changed, no agents spawned, no commands proposed for execution. Runtime graph coverage is unavailable for session/log files, so findings are transcript/artifact-backed, not graph-backed.

The first attempted manifest location (task package root) was missing; listing located the manifest under `research/`. Initial broad extraction produced polluted/oversized output, so a narrower parser separated actual invocations from policy text. Exact review severity labels below reproduce historical reviewers and are not a new severity classification.

**Key Takeaways**
- This is an inventory and source map, not deep root-cause analysis.
- Archived ledger evidence sometimes omits a review failure that the nested reviewer transcript preserves.

## Session inventory
| Manifest index | Session ID | Initial screening result |
|---|---|---|
| 13 | c444c002-20df-4745-8f95-2254c4d3086f | Positive workflow invocation at original JSONL line 15, 2026-10-22T15:10:48.373Z. Issue #358 shell token plan. User accepts five plan changes; implementation occurs in session 15. No implement invocation in this session. |
| 14 | 10cacee5-9821-461e-89b4-903837da3b8b | Positive workflow Skill call at line 51, 2026-10-22T20:43:55.671Z. Issue #358 follow-up plan. One citation validator, then user requests Task 4 fix. No implement invocation found. |
| 15 | 0690ee9f-c2f6-40ef-96be-1a0913a37866 | Positive operational implement at line 15 and line 818; two separate issue #358 plan executions, including failed final reviews and re-reviews. Highest-priority candidate in this partition. |
| 16 | 97c47129-146b-4227-a0db-9830352b81aa | Negative workflow/implement invocation screen. Retry-ladder follow-up fix, merge and cleanup, not an operational execution. |
| 17 | 0f6383e1-533a-428c-aee4-18e6ddfb4aef | Positive actual implement invocation at line 15, 2026-10-22T12:03:04.399Z. Implements retry-ladder feature itself. Operational Task 8 re-review and final-review failure must be separated from later PR #277 feature-development review. |
| 18 | 5290b7ae-b9be-47ad-951d-ac7c63411061 | Negative workflow/implement invocation screen. Analyze/rewrite-script work, PR #278 monitor and troubleshoot. Review activity exists but outside target command execution. |

**Key Takeaways**
- Four sessions have actual workflow or implement calls; two have no such operational invocation.
- Same issue #358 package spans sessions 13 and 15 and must not become duplicate incidents.

## Session findings
### Sessions 13 and 14: actual workflow plans, corrections without another semantic review

All times below are original JSONL timestamps, not filesystem times. Original JSONL lines are cited; excerpts are decoded message text, not giant serialized lines.

**Session 13 source:** `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/c444c002-20df-4745-8f95-2254c4d3086f.jsonl`.
- L15, 2026-10-22T15:10:48.373Z: actual `/sc:workflow` command, issue #358 five-key overwrite, `--depth quick`.
- L364, 15:24:24.207Z: "The merged verdict fails the plan on three acceptance checks"; overwrite checks covered one key, man-page check accepted any one name, README troubleshooting row missing.
- L389, 15:25:42.633Z: plan package `TASK-WF-issue358InTempla-20261022-151058`, review report `.dev/reflect/pre-issue358-20261022151210/REPORT.md`, "The plan covers everything you asked for, but the review failed it."
- L392, 15:30:37.609Z: user "apply 5 changes". L406-L420: actual plan Edit calls.
- L435, 15:31:25.623Z: "I didn't re-run the review on the revised plan." Only format check reran. Implementation is session 15, same package, not a separate repeated-failure incident.

**Session 14 source:** `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/10cacee5-9821-461e-89b4-903837da3b8b.jsonl`.
- L51, 2026-10-22T20:43:55.671Z: actual `Skill sc:workflow-protocol`, follow-ups from `TASK-WF-issue358FollowUp-20261022-193837/artifacts/t17-followups.md`.
- L275, 20:50:38.271Z: `Skill sc:reflect-protocol --mode pre`, new package `TASK-WF-reviewAndPlanThe-20261022-204721`.
- L344, 20:52:56.695Z: "advisory review ran only as an abbreviated first pass and found five minor issues"; Task 4 acceptance bullet cannot be checked and contradicts its Surface 1 string change.
- L346, 20:55:36.671Z: user requests Task 4 fix and decision preset. L360-L366 actual plan edits.
- L371, 20:56:05.203Z: old review report left unchanged; no new semantic review or implement call observed.

**Key Takeaways**
- Both are genuine workflow invocations, but neither demonstrates review, fix, second failed review by itself.
- The issue #358 initial plan in session 13 is the input to the first implement run in session 15.

### Session 15: issue #358 operational implementation, two final-review incidents

**Source:** `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl`.

**First package, final-review evidence failure (incident `review-loop:issue358InTempla:final:20261022`).**
- L15, 2026-10-22T15:32:02.303Z: actual `/sc:implement .dev/tasks/to-do/TASK-WF-issue358InTempla-20261022-151058/TASK-WF-issue358InTempla-20261022-151058.md`; L36 actual protocol Skill call.
- L375, 15:43:26.516Z: fresh final reviewer after four task reviewers.
- L390, 15:44:52.068Z: `FINAL: issues evidence=./progress.md:8`; state digest unchanged during review.
- L393, 15:44:57.271Z: "Task 3 ledger line ... cites README.md:161 as proof that markdownlint reports no new findings. Line 161 is a table separator row ... and there is no markdownlint log"; append-only/closed task rule prompts user authorization.
- L396, 15:51:38.336Z: user reopens Task 3 evidence only.
- L411, 15:51:55.456Z: actual lint comparison output, before 28, after 28, zero findings on changed lines. L415: corrected Task 3 progress line appended.
- L419, 15:52:16.384Z: second fresh final reviewer.
- L435, 15:54:23.570Z: `FINAL: pass`, archive helper `status=archived`, exit 0; L438 confirms done package.
- Historical artifact root: `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/`; key paths `progress.md`, `artifacts/t3-markdownlint.log`.

**Follow-up plan regeneration, not another implementation failure.**
- L592, 18:53:50.673Z: actual workflow Skill invocation for docs follow-up, first package `TASK-WF-issue358FollowUp-20261022-185406`.
- L762, 19:35:39.535Z: "review found real gaps ... isn't safe to run"; missing stale strings, closing sweep, impossible comment-only check, rotation wording, and startup-card issue. "The review's own report file wasn't written"; verdict at `.dev/reflect/pre-issue358followup-20261022190016/adversarial/merged-verdict.yaml`.
- L764, 19:38:01.081Z: user "regenerate".
- L817, 19:40:25.443Z: second plan format passed; "Its own review was skipped on purpose". L818, 19:40:25.935Z actual implement Skill call for `TASK-WF-issue358FollowUp-20261022-193837`.

**Second package, repeated final evidence failures (incident `review-loop:issue358FollowUp193837:final:20261022`).**
- L1916, 20:16:10.434Z: final reviewer after 17 task reviews.
- L1932, 20:20:36.570Z: `FINAL: issues` citing operator doc, startup script and progress.
- L1935, 20:20:43.704Z: operator table lint total unchanged at 123, but literal "no finding on a changed line" criterion fails preexisting findings on changed rows. Also stale ledger citations for Tasks 7, 8, 17.
- L1938, 20:25:19.428Z: user "accept and fix".
- L1969, 20:25:54.487Z: corrected Task 7/8/17 evidence appended; owner acceptance file `artifacts/t6-owner-acceptance.md` recorded in L1987.
- L1979, 20:26:21.231Z: second fresh final review.
- L2012, 20:31:49.683Z: `T10: BLANK ./artifacts/t10-markdownlint.log:10-10`, `tokens checked; problems: 1`.
- L2028, 20:32:18.558Z: "The second final review found one more bad evidence line number ... Task 10's markdownlint citation pointed at a blank line"; corrected Task 10 and Task 7 evidence, and admits this exceeded literal authorization for Tasks 7, 8, 17. No delivery file changed.
- L2020, 20:32:13.997Z: third fresh final reviewer (dispatched before explanatory L2028).
- L2036, 20:37:22.846Z: `FINAL: pass`, archive `status=archived`, exit 0. L2052 confirms completion and still-open follow-ups.
- Historical artifact root: `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/`; key paths `progress.md`, `artifacts/t6-owner-acceptance.md`, `artifacts/t10-markdownlint.log`, `artifacts/t17-followups.md`.

**Key Takeaways**
- This session supplies one fail-fix-pass final-review incident and one fail-fix-fail-fix-pass final-review incident, on distinct packages.
- Plan regeneration and skipped second-plan reflection are separate workflow facts, not extra implementation retries.

### Session 17: operational run building retry ladder, distinct from later feature-development PR reviews

**Source:** `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/0f6383e1-533a-428c-aee4-18e6ddfb4aef.jsonl`.
- L15, 2026-10-22T12:03:04.399Z: actual `/sc:implement` for `TASK-WF-mergedEscalating-20261022-015540`; L36 actual protocol Skill.
- L818, 12:33:00.858Z: Task 8 reviewer. L832, 12:36:05.793Z: "Reviewer found one real deviation: my verify step skips fixed exclusions where the design says outside the domain of now".
- L836-L858: actual fix edits and regression test; L865, 12:36:36.284Z: 89 passed.
- L868, 12:36:55.368Z: fresh Task 8 re-review. L876 summarizes first verdict `misunderstood`, one allowed fix pass. Later L1295 confirms Task 8 eventually compliant. This is a normal task fail-fix-pass, not evidence of multiple failed retries (`review-loop:mergedEscalating:T8:20261022`).
- L1276, 12:54:17.142Z: first whole-package final reviewer. L1291, 13:02:00.408Z: `FINAL: issues`, unchanged state digest.
- L1295, 13:02:15.390Z: 10 stale ledger citations after later edits, wrong touched-file rule pointer, and real artifact-restore bug: original `report.dup-1` restored as `report`. Package stays to-do.
- L1301, 13:16:31.492Z: user authorizes brainstorms and fixes. L1310/L1312: two brainstorm agent calls.
- L1751, 14:24:19.862Z: second final reviewer. L1759: fixes include preserving collision path basenames and final review judging current end state rather than moved line numbers alone.
- L1770, 14:29:07.696Z: second final review passed. L1777, 14:29:11.199Z: archive helper `status=archived`, exit 0 (`review-loop:mergedEscalating:final:20261022`).
- L1801 onward starts user-directed commit/push/PR monitor. L1807 is `sc-pr-submit-protocol --monitor 3`. Later verification, troubleshoot, pushed-fix QA, and PR #277 threads are FEATURE-DEVELOPMENT reviews, not additional operational implement retries. Do not count them as this incident's failed attempts.
- Historical package root: `/config/workspace/IronClaude/.dev/worktrees/implement-retry-ladder/.dev/tasks/done/TASK-WF-mergedEscalating-20261022-015540/`; artifacts include `progress.md`, `artifacts/t8-test.log`, `artifacts/final-*.log`.

**Key Takeaways**
- A genuine implement run exists even though its subject is retry-ladder development.
- Its Task 8 and final archive gates are operational evidence. Its subsequent PR #277 review/remediation sequence is a different category.

### Sessions 16 and 18: exclusions, not silent missing positives

**Session 16 source:** `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/97c47129-146b-4227-a0db-9830352b81aa.jsonl` (129 original lines). No workflow/implement Skill or user-command invocation found. L56, 2026-10-22T20:32:03.711Z says PR #277 already merged. L83-L84 patch one adviser-effort sentence in source/plugin copies; L105 reports PR #279; L115 user requests cleanup. This is a follow-up correction and cleanup, not an operational review loop.

**Session 18 source:** `/config/.claude/projects/-config-workspace-IronClaude/5290b7ae-b9be-47ad-951d-ac7c63411061.jsonl` (1451 original lines). No workflow/implement Skill or user-command invocation found. L15, 2026-10-22T15:49:26.403Z requests GlobalSrc-Home analyze/rewrite script; L35 is `Skill sc:analyze`. L171 reviews script, L262-L266 review resulting changes, L353/L360 invoke PR submission, L529 troubleshoot explicitly says "do NOT start sc:workflow or any task file". PR #278 review/remediation is real but not an implementation-command execution.

**Key Takeaways**
- Absence claims concern parsed actual invocations, not literal absence of command strings in injected instructions.
- These sessions should not inflate operational failure-loop counts.

## Candidate incident register

| Stable deduplication key | Classification | Confirmed outcome | Evidence strength |
|---|---|---|---|
| `review-loop:issue358InTempla:final:20261022` | Operational final-review fail, evidence-only fix, pass | Archived | Original session, two nested final reviewers, on-disk ledger |
| `review-loop:issue358FollowUp193837:final:20261022` | Operational final-review fail, fix, second fail, fix, third pass | Archived | Original session, three nested final reviewers, on-disk ledger, acceptance note and blank cited log line |
| `review-loop:mergedEscalating:T8:20261022` | Operational task misunderstanding, one fix, compliant re-review, while developing retry-ladder feature | Continued | Two nested reviewers and task completion ledger |
| `review-loop:mergedEscalating:final:20261022` | Operational final-review issues, user-authorized fixes, second pass, while developing retry-ladder feature | Archived | Two nested final reviewers and on-disk ledger |
| `workflow:issue358FollowUp185406:regenerated:20261022` | Failed pre-execution plan review, replaced by new plan whose review was skipped | Superseded, not executed | Session 15 L762-L818; missing standalone review report acknowledged |
| `workflow:issue358InTempla:correction:20261022` | Failed pre-execution plan review, user-authorized correction, no semantic re-review | Input to first implement incident | Session 13 L364-L435; same package as session 15 |
| `workflow:reviewAndPlanThe204721:correction:20261022` | Advisory review with five issues, user correction, no semantic re-review | Implement not observed here | Session 14 L344-L371 |

### Nested review source map

All following paths were checked present and their final assistant messages decoded directly. Each is supporting evidence for its parent session, not another top-level incident.

**First issue #358 package:** common nested directory `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/`.
- `agent-a59e9aa6df05118de.jsonl`, original L51, 2026-10-22T15:44:41.129Z: `FINAL: issues`; "One minor ledger-evidence problem (T3.AC5). The delivered code and docs meet every acceptance criterion and every Constraint."
- `agent-a6248e3c9fc51e940.jsonl`, L50, 15:54:17.688Z: `FINAL: pass`; "Every AC is met, and I found no stale ledger tokens."

**Second issue #358 package:** same nested directory.
- `agent-a9c0c61dd415c2c4d.jsonl`, L135, 20:20:21.142Z: `FINAL: issues`; "Every AC I checked is met except T6.AC4's lint clause, and the other issues are stale ledger tokens."
- `agent-acf0a51e6992c50ee.jsonl`, L116, 20:31:27.048Z: `FINAL: issues`; "One BLOCKING item: a stale ledger evidence token for T10. Every AC and Constraint in the files themselves holds."
- `agent-a4bfff371c63a6c39.jsonl`, L155, 20:37:13.395Z: `FINAL: pass`; records owner-accepted literal T6.AC4 gap and no blocking problems.

**Retry-ladder package:** common nested directory `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/0f6383e1-533a-428c-aee4-18e6ddfb4aef/subagents/`.
- `agent-a7e2f8f9f2f60f9ce.jsonl`, L63, 2026-10-22T12:35:55.368Z: `VERDICT: misunderstood`; T8 fixed-exclusion verification skip, confirmed with tampering `rm` shim.
- `agent-a4a9f17e0c9cd2e25.jsonl`, L57, 12:39:24.340Z: `VERDICT: compliant`; fixed skip removed, 89 tests passed in own run.
- `agent-a72c4592eac88daf4.jsonl`, L136, 13:01:40.292Z: `RESULT: issues`; stale ledger citations, dangling pointer, wrong-name move-back bug, and log citations to headers.
- `agent-a0cab87f5c9a76ec9.jsonl`, L134, 14:29:01.200Z: `RESULT: pass`.

### On-disk artifact cross-checks

These archived roots all still exist despite later worktree-cleanup narrative elsewhere.

1. `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/progress.md`: L8 original bad Task 3 evidence, L11 `FINAL: issues`, L12 corrected Task 3 evidence, L13 `FINAL: pass`, L14 archive start. Referenced `artifacts/t3-markdownlint.log` was checked present (1222 bytes).
2. `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/progress.md`: L22 original Task 10 citation `t10-markdownlint.log:10`; L37 first `FINAL: issues`; L38-L40 corrections; L41 corrected Task 10 citation `:9`; L42 second Task 7 correction; L43 `FINAL: pass`. IMPORTANT: no ledger line records the second final review's `issues`; that failure is independently present in nested reviewer L116 and top-level L2028.
3. Same package `artifacts/t10-markdownlint.log`: L9 `BEFORE total: 4`; L10 blank; L14 `AFTER total: 4`; L17 no new findings. This directly corroborates the second review's bad-token finding without relying on reviewer prose.
4. Same package `artifacts/t6-owner-acceptance.md`: L10-L13 records "accept and fix", accepting no-new-findings for the two already-flagged rows and reopening Tasks 7/8/17 only. Historical reviewer and parent later mention Task 10 correction beyond that specific list; authority interpretation is for later analysis, not decided here.
5. `/config/workspace/IronClaude/.dev/worktrees/implement-retry-ladder/.dev/tasks/done/TASK-WF-mergedEscalating-20261022-015540/progress.md`: L18 records final T8 compliant, L31 `FINAL: issues`, L32 `FINAL: pass`, L33 archive start. It does not persist Task 8's first misunderstanding as a separate verdict line. `artifacts/t8-test.log` checked present (11215 bytes).

**Key Takeaways**
- Highest-priority repeated-failure case is the second Coder final gate: the ledger alone hides its middle failure.
- Retry-ladder operational incidents and retry-ladder PR review chains have separate identities.

## Gaps and Questions

- No deep current-code root-cause analysis performed; this is scope discovery only. Historical reviewer findings are verified as events, not independently re-adjudicated as current code defects.
- Workflow report artifacts for sessions 13/14 and follow-up pre-review were linked from actual events but not fully read here. Session 15 explicitly reports that its first follow-up reflect REPORT.md was not written; merged-verdict YAML is the fallback source named by that session.
- Parent-level scans can miss an in-nested protocol invocation; this partition checked actual top-level commands and review-linked nested finals, not every arbitrary nested agent. Negatives mean no top-level operational invocation found.
- The second Coder final-review failure is absent from its progress ledger; use nested reviewer source rather than counting FINAL lines alone.
- Task 8's failed review is likewise absent from its archived progress ledger, which retains its compliant completion only.
- Source line references inside historical review text refer to historical working trees. They are not claims that current production source still has those defects or the same line numbers.
- Missing original manifest location and oversized initial extraction were recovered; no unresolved source-access blocker remains for the confirmed incidents.

## Stale Documentation Found

No present-day architecture documentation audit was in scope. Historical events explicitly report stale ledger citations, unchanged pre-fix review reports after plan correction, and a source-design naming paragraph intentionally left hash-pinned after a fix. These are historical evidence-staleness observations only; no claim of a current production documentation defect is made.

## Summary

Screened only frozen indexes 13-18 and found actual workflow/implement execution in four sessions, with two excluded sessions containing only analysis, follow-up fixes or PR review activity. Session 15 contains two distinct final-review incidents, including one confirmed fail-fix-fail-fix-pass sequence that its archived ledger incompletely records. Session 17 contains a real operational implement run developing the retry-ladder feature, with one Task 8 correction and one final-gate correction; subsequent PR #277 reviews are explicitly excluded from those operational attempts. Linked original timestamps, physical JSONL lines, nine nested reviewer logs and archived evidence artifacts make these candidates ready for deduplicated case selection, not yet deep case analysis.
