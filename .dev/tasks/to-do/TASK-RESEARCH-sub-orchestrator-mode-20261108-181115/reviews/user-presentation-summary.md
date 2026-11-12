# Sub-Orchestrator Mode: Research Summary for the User

**Date:** 2026-11-09
**Status:** Complete
**Template:** Task Step 7.2 presentation summary (plain English; every number copied from the report and the gate verdict files).

**No gate ended in a halt.** Every gate passed. One report check carries a caveat: the report keeps four contradiction markers, two of which (the PR #449 phrase against the worker rule, and the D5 mailbox clause) are source conflicts the evidence cannot settle. The report says so openly and carries them as open questions Q01 and Q06. Because of this the task is closed "with caveats", not "clean".

## Where the report is
`.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md` (10 sections; final SHA-256 `832dd841b8c6a0171189c83424408cb5ece2329c79044be483bf8cbd4adeb6c6`).

## The answer
Do not add a subordinate-coordinator mode (`--sub`) now. The report recommends option O6: **defer it, with 25 testable approval conditions that would have to be met before anyone reconsiders.** This is not a permanent no. The best future technical candidate is O3, a supervised middle worker using Orca's native helpers, but the report ranks it only provisionally. The 25 conditions (DG-01 to DG-25) cover things like an approved autonomous brief, a measured case where work could not be planned before dispatch, recursive admission limits, and verified recovery. None of the 25 is passed today.

## Value, implications, unlocks, rethinks
- **Value:** the only unique benefit found is conditional: a split discovered during execution could be tracked as child work without a round trip through the top orchestrator. No measured saving exists. Direct parallel workers, flat fan-in and in-session helpers already cover most needs.
- **Implications:** a middle session owes progress upward and service downward, must leave its children with a known owner if it stops, and its message or success never counts as a human decision or as proof for each child.
- **Unlocks (only if conditions are met):** local helper selection, independently checkable child work, less reconstruction by the top orchestrator, and persistent delegated ownership through a separately approved role.
- **Rethinks:** rule WC-13 (the worker-session fan-out ban) stays as is; any future exception must name the eligible session, helper route, counts and retained bans. Decision D5 (depth one, person-opened coordinators, the ban) stays current policy. The PR #449 phrase "a coordinator under another orchestrator" is an open defect (gap A01, Important): it reads as if a middle role exists, while the worker rule still forbids it.

## Key findings
| Finding | Detail |
|---|---|
| The PR #449 phrase conflicts with the worker rule | The contradiction is kept visible in the report (gap A01, question Q01). The report does not pick a side. |
| Historical research showed native ancestry and creator-directed reporting work | Credited as a historical snapshot only. The replacement build and exact-target routing are not certified. |
| No qualifying measured saving was found | Marked unverified. The search was bounded, not a claim that none exists. |
| Hook and guard limits | The launch guard matches the literal `orca` command, and some probes are unlisted. These are ceilings and a compatibility defect, not permission to bypass. |
| Flat supervision (issue #339) and knowledge sharing (issue #423) do not need another tier | Neither inherently requires a supervisory generation. |
| Size of the work | 34 adoption gaps, 38 stale or interpretation families, 54 compiled gap groups, 46 external findings, 35 issue requirements. |

## Research files
8 codebase research files, 4 web research files, 0 fix-addendum files. Also 6 synthesis files plus the evidence correction record, 4 scope files, and the research notes.

## Quality checks (cycles and verdicts)
| Gate | Result |
|---|---|
| Research gate (Phase 3) | PASS, cycle 1 (10 reports, 39 checks, 0 blockers) |
| Synthesis gate (Phase 5) | PASS, cycle 1 (10 reports, 57 checks, 0 blockers) |
| Report lens gate (Phase 6) | PASS, cycle 1 (13 lenses; 2 blockers fixed, then 0) |
| Source fidelity gate | PASS, cycle 1 (1 blocker fixed, then 0) |
| Anti-omission gate | PASS, cycle 1 (73 omissions recovered, then 0) |
| Final validation gate | PASS, cycle 2 (4 blockers, then 1, then 0) |

Earlier boundary checks for Phases 2 to 5 each took one fix cycle. Minor notes from all reviewers were recorded and not fixed.

## Open questions
71 in total (Q01 to Q71). 21 need a live Orca run, which this report neither did nor authorized: Q09, Q10, Q17 to Q20, Q22, Q25 to Q31, Q36, Q38, Q39, Q41 to Q43 and Q71. Of the other 50, 24 are policy decisions and 26 need more evidence. Section 9.2 of the report has a triage table with each question's type.

## What was not done
No implementation plan was written and nothing was implemented. No live Orca run, settings change, commit or push happened. The historical archive residual (867 lines, 274 paths) stays excluded and unverified by agreement.

## Recommended next step
The contract owner decides gap A01: either narrow the PR #449 phrase now as a separate wording change, or leave it and keep the conflict recorded. The report leans toward narrowing, labelled as inference. This is the only live defect, and the decision costs no experiment. Details: Section 7.6, "Recommended next action".
