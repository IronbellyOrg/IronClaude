# Diff Analysis: reviewer-card Comparison (UC-1 pre-execution review of the B-CTX observation plan)

## Metadata

- Generated: 2026-11-08T02:10:00Z
- Variants compared: 2 (variant-1 = reviewer 1, analyzer persona, haiku class; variant-2 = reviewer 2, qa persona, opus class)
- Total differences found: 22 (diff points in the convergence denominator: 15)
- Categories: structural (3), content (6), contradictions (2), unique (7), shared assumptions (4 promoted)
- Focus: correctness, coverage, deviation-classification
- Variant file lines: variant-1 35, variant-2 44. Note: variant files are single-line-per-table-row markdown; "line" counts are lower than content size.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|---|---|---|---|
| S-001 | Section order | Verdict, Findings (A-01..A-05), Coverage, Independent assessment of Tier 1, Grade, Gaps | Verdict, Findings (Q-1..Q-8), Judgement on Tier 1 (N-1..N-14), Coverage, Run budget, FAIL/PASS, Grade, Gaps | Low |
| S-002 | Finding labels | every finding carries Category "Drift" plus MEDIUM or LOW | severity only; five rows hedged ("Low-Medium", "Medium-Low", "Info/Low") | Medium |
| S-003 | Treatment of the Tier 1 defects N-1..N-14 | narrative bullets covering N-1, N-3, N-4 and M-12 only | one row per N-id with confirm, refute or extend and a basis | Medium |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity |
|---|---|---|---|---|
| C-001 | Survivor job versus timeout and teardown /proc sweep (plan:31) | A-01 MEDIUM: define timeout cleanup separately from final teardown, exempt registered survivors, add a self-check that times out a dependent run | Confirms N-3 (Medium) and adds Q-6: a setsid daemon that changes its working directory escapes the cwd sweep, so teardown should also stop recorded pids | Low |
| C-002 | Interactive pty /clear versus the per-run budget cap (plan:22, :55) | A-02 MEDIUM: grounded in the archived CLI help (claude-help.txt:131-132, "only works with --print"); choose between recording it unavailable or authorizing a separately bounded interactive run | Confirms N-4 but marks the budget part [INFERRED] (did not read the help); also notes --disable-slash-commands in live_probe.py | Low |
| C-003 | The /clear reused-process topology (plan:55, :59) | A-03 MEDIUM: the plan SIGKILLs the first Claude process and then starts a different pty process, so the controller that originated the governed job is not reused; specify controller identity before and after /clear or leave the case unavailable | Q-1 MEDIUM: the pty session's starting identity and the expected status of each call before and after /clear are unstated; Q-7: a fork gets a new session id and is expected ordinary, state it | Medium |
| C-004 | Evidence for the launch wrapper, the Git and hook process trees and auto mode (plan:44, :90, :114-117) | A-04 MEDIUM: add redacted tree snapshots (pid, ppid, start identity, role) and align the report's allowed classes; do not accept M-12 as resolved | Q-3 MEDIUM: no task produces wrapper or auto-mode evidence; either add one bounded observation or allow "not run (budget)"; Q-5: add one Git push started by a real governed Claude call inside an existing run | Medium |
| C-005 | Report row categories (plan:23, :114, :117) | A-04 (second half): distinguish "not attempted within this budget" from an actually missing interface | Q-2 MEDIUM: add a category "not observed (reason)" counted as an evidence gap, because timeouts, dead jobs and unfollowed prompts are not a missing interface | Low |
| C-006 | Whether the INF requirements are covered | INF-001, INF-002, INF-003, INF-008 Partial; the rest Covered | all ten Covered; INF-005 only as controlled evidence although observed evidence is reachable | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | Tier 1 defect N-1: does the plan force a thirteenth real Claude run? | Refuted: the plan says "one JSON line per run" and shares four shapes across three Claude starts (plan:22, :31), so thirteen starts are not forced; a unique run id would still help traceability | Confirmed Medium: one ledger line per shape with real_claude true gives 1+4+4+4 = 13 and the runner's "refuses a thirteenth" guard could refuse a legitimate shape (plan:31, :66, :119) | Medium |
| X-002 | Coverage verdicts INF-001, INF-002, INF-003, INF-008 | Partial (conflicting cleanup and budget rules, incomplete tree capture, /clear topology unresolved, report classes conflict with controlled evidence) | Covered (plan:15, :19, :22 and Tasks 2, 3, 4, 6, 8 address them; defects are separate findings) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | A-05: reparent shape samples the descendant "inside the same governed command before it exits" with no proof that reparenting happened (helper:292-295 installs a subreaper); require the intermediate parent to exit and the PPID change to be observed | Medium |
| U-002 | 2 | Q-4: release can be observed for real by deleting the governed session record after Task 3's decisive measurements (design:526, :557; helper:238-241); costs no extra Claude run and removes one of the causes of the fixed FAIL | High |
| U-003 | 2 | Q-5: a Git push started by a real governed Claude Bash call is never observed; add one inside an existing governed run | Medium |
| U-004 | 2 | Q-6: a setsid daemon that changes directory escapes the cwd sweep; teardown should also stop every pid recorded in ready files after a start-ticks check | Medium |
| U-005 | 2 | Q-8: no rule identifies "the Claude process" for the parent-hop count; have the runner write its Claude child's pid to a file and walk to it with a cap | Low |
| U-006 | 2 | Run-budget arithmetic check (1+4+4+3 = 12) and an explicit statement that PASS is blocked by several independent causes (N-14) | Low |
| U-007 | 1 | An explicit independent assessment of Tier 1: confirms boot comparison and ancestry facts, refuses to accept M-12 as resolved | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | A SIGKILL of the first Claude process leaves the supervisor and the surviving child alive, and the killed session can then be resumed or forked | both build the Task 3 findings (C-001, C-003) on a surviving child | the whole decisive case is conditional on it; both cards list it as unverified | STATED (not promoted) |
| A-002 | /clear and --fork-session give the new work a new session id that has no governed record, so the adapter treats it as ordinary | C-003 and the decisive-case discussion | if /clear keeps the session id, the decisive case needs a different expected status; the cards mark it [INFERRED] only in passing | UNSTATED (promoted) |
| A-003 | The executor can start real Claude runs from its own session: a nested launch is not refused and authentication is available in the throwaway HOME | both treat the twelve-run budget and the unavailable branches as workable | if refused, the whole real-Claude half is unavailable and the report is an empty FAIL | UNSTATED (promoted) |
| A-004 | The twelve-run cap and the 0.25 USD per-run cap are binding on the executor and the plan owner will not relax them for the interactive /clear run | C-002 (both accept the caps as fixed) | decides whether the right fix is "unavailable" or "authorize a bounded interactive run" | UNSTATED (promoted) |
| A-005 | Reading the plan and the cited code statically is enough to judge that the plan is executable; no dry run of the runner or the commands is needed | both reviewers read only, ran nothing | executability defects that only a dry run shows (onboarding dialogs, shim pids, tool timeouts) cannot be excluded | UNSTATED (promoted) |
| A-006 | An expected FAIL with two gap lists is an acceptable deliverable of the plan | both | if the owner wanted a possible PASS, the plan's whole design is wrong | STATED (not promoted) |

Only the UNSTATED rows A-002 to A-005 are promoted to diff points. A-001 and A-006 are stated and documented only.

## Summary

- Total structural differences: 3
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 7
- Total shared assumptions surfaced: 6 (UNSTATED 4 promoted, STATED 2, CONTRADICTED 0)
- Highest-severity items: none High; Medium: S-002, S-003, C-003, C-004, C-006, X-001, X-002
- Similarity check: differences are well above 10% of comparable items, so the debate is not skipped.
- Denominator for convergence: S 3 + C 6 + X 2 + A 4 = 15.
- Taxonomy levels: L1 surface S-001, S-002; L2 structural S-003, C-004, C-005, C-006, X-002; L3 state mechanics C-001, C-003, X-001 (guard on the thirteenth run), A-002, A-003, A-004, A-005, and C-002 (budget guard). All three levels are covered; no forced round is needed.
