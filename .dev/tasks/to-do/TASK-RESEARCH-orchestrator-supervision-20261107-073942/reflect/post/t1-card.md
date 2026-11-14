# T1 reflect card: UC-2 post-execution, TASK-RESEARCH-orchestrator-supervision-20261107-073942

Author: root-cause-analyst (Tier 1); persisted verbatim by the orchestrator because the agent's Write was blocked by the freshness hook.
Scope: research/ (10), synthesis/ (7), qa/ (88), gaps-and-questions.md, RESEARCH-REPORT-orchestrator-mode.md (1762 lines), baseline-git-status.txt; driving doc TASK-RESEARCH-orchestrator-supervision-20261107-073942.md (TASK). Read-only audit; no git run. Line refs: TASK = task file, REP = report, GAPS = gaps-and-questions.md, P7 = synthesis/phase7-summary.md.

## Verdict

**PASS-WITH-DRIFT**, self-confidence 0.80.

All seven objectives (TASK:60-66) are met with recorded exceptions. The 10-section report exists (REP TOC :19-32; Section 10 at :1715; TASK:368). The read-only constraint holds (baseline-git-status.txt is 3 untracked entries, the same as the session start). The hard rules are honoured (WC-10, C8 UNVERIFIED tagging, A4 rejected). There is no Regression. The drift is confined to stale or wrong line-anchored citations into the gaps log and to a stale count in the Task Summary. None of it changes a recommendation or a gap's status.

## Coverage

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| C-01 | Obj 1: verify scope-01..04 citations | covered | TASK:60; research/scope-01..04; TASK:369 |
| C-02 | Obj 2: G-A row schema, G-B open questions | covered | TASK:61; research/05, 06, 07-gate-gap-fill.md; TASK:564 |
| C-03 | Obj 3: research gate, 2-cycle cap, gaps file | covered by coordinator exception | TASK:371-372, :580; REP:13 |
| C-04 | Obj 4: two external-pattern files | covered (WebSearch fallback) | TASK:63, :581; TASK:369 |
| C-05 | Obj 5: six synthesis files + gate | covered | TASK:64, :370-371 (15 -> 3 -> 0 PASS) |
| C-06 | Obj 6: 10-section report; lens, fidelity, anti-omission | covered; anti-omission passed with owner exception | TASK:65, :371, :558; REP:15 |
| C-07 | Obj 7: close-out, summary, I17 | 7.1-7.4 covered; 7.5 (this gate) and 7.6 pending by design | TASK:66, :454-455, :457; P7:1-55 |
| C-08 | Nothing outside the task folder changed | covered | baseline-git-status.txt (3 entries); TASK:454 |
| C-09 | GQ-101..110 recorded; report deliberately not edited | covered | GAPS:124-133, :135; TASK:456 |
| C-10 | Report citations into the gaps log resolve | **drift** | D-1, D-2, D-4 below |

## Deviations

| ID | Category | Finding | Evidence |
|---|---|---|---|
| D-1 | Drift (Medium) | The report says in the present tense that `gaps-and-questions.md:125` "reads Open: 75. Resolved: 25". GAPS:125 is now the GQ-102 row, and the summary at GAPS:135 reads "110 rows. Open: 85. Resolved: 25". The four claims also contradict the report's own Gaps Log, "78 open" (REP:1754). The owner ruling covers only the Gaps Log count, stale by 7 rows (TASK:456); it does not cover these four claims, which were already stale when the :558 edit changed :1754. | REP:229, REP:597, REP:1127, REP:1474; GAPS:125, :135; TASK:456, :582 |
| D-2 | Drift (Low) | The Gaps Log bullet added in the anti-omission exception edit cites the 78/25 summary as `(:125)`. Once GQ-101..103 were inserted above it, the summary was no longer at :125, so the anchor was wrong when it was written. | REP:1754; TASK:558; GAPS:124-126 |
| D-3 | Drift (Low) | The Task Summary still says "the gaps log counts 103 rows, 78 open, 25 resolved". The later Execution Log row and the gaps log say 110/85/25. The Task Summary was not updated when TASK:456 recorded the change. P7:34 inherits the 78/25 (`:125`) figure. | TASK:374 vs TASK:456, GAPS:135; P7:34 |
| D-4 | Drift (Low) | Section 9 row 36 is about GQ-41 but cites `gaps-and-questions.md:82`. GAPS:82 is GQ-59 (the runtime-version probe); GQ-41 is GAPS:64. Either an unlabelled cross-reference or a mis-cite; the anchor is not GQ-41. | REP:1577; GAPS:64, GAPS:82 |
| D-5 | Necessary deviation | The research gate halted at the 2-fix-cycle cap with NB-4 open; the coordinator approved proceeding; NB-4 was fixed and re-checked at the synthesis gate. | TASK:371-372, :580; REP:13 |
| D-6 | Necessary deviation | Tavily was unavailable, so the work used WebSearch/WebFetch; deep-research has no Write tool, so it was re-run as rf-analyst and the executor saved web-02 with a provenance note. | TASK:581 |
| D-7 | Necessary deviation | The NB-4 fix ran as its own serialized pass after Phase 4 and before Phase 5, because "during Phase 4 synthesis" did not match this task's phase numbering. | TASK:582 |
| D-8 | Necessary deviation | The anti-omission gate halted with `[HALT-MONOTONICITY] |F|=2`; the owner carried NB-2 and NB-4c as GQ-101 and GQ-102 to /sc:design; the report says it passed with exceptions. | TASK:371-372, :558; REP:15; GAPS:124-125 |
| D-9 | Necessary deviation | The report's Gaps Log count (78 open, GQ-01..103) is stale against the gaps log (85 open, GQ-01..110) because the owner ruled out report edits outside a gate; disclosed in both files. | TASK:456; GAPS:135; REP:1754 |
| D-10 | Authorized expansion | Owner-requested /ponytail-review of the Phase 1 plan (qa/ponytail-review-phase1-plan.md); its 10 findings carried as GQ-103 (3 blocking) and GQ-104..110 (7 minor). | TASK:451, :456; GAPS:126-133 |
| D-11 | Authorized expansion | After the gate, the owner decision edited the report: the exception paragraph at REP:15 and the Gaps Log bullet at REP:1754. | TASK:558; REP:15, :1754 |
| D-12 | Authorized expansion | A gate fix agent created research/07-gate-gap-fill.md, not listed as a research file in the plan; it is counted in the 8 codebase files. | TASK:369; REP:5; P7:27 |

Counts: Regression 0, Drift 4 (D-1..D-4), Necessary deviation 5 (D-5..D-9), Authorized expansion 3 (D-10..D-12).

Not a deviation: the pointer-prompt technique (TASK:579); each agent reads the same bytes from disk. synthesis/phase7-summary.md was written for item 348 (TASK:370) and copies only from the report (P7:3).

## Root cause / deviation analysis

**D-1 and D-2 share one root cause.** The report cites the gaps log by line number; the gaps log is a growing table whose summary line sits below the rows.

1. At 20:24Z the NB-4 fix pass put the summary at GAPS:125 and set it to 75/25 (TASK:582). REP :229, :597, :1127, :1474 were true when written.
2. The anti-omission exception added GQ-101..103 above the summary (GAPS:124-126). The report edit then (TASK:558) updated the count at :1754 to 78 but kept the `:125` anchor and left the four "Open: 75" claims; from then on the report disagreed with itself.
3. GQ-104..110 were added under the owner ruling "no report edits outside a gate" (TASK:456), freezing every stale anchor; the ruling's disclosure names only the 78-open count.

Hypotheses tested:

- **H1: D-1 claims are covered by the ruling. Rejected.** TASK:456 and GAPS:135 disclose only that the Gaps Log count of 78 is stale "by these 7 rows". The 75/25 claims were stale before the ruling and conflict with REP:1754.
- **H2: D-1 changes a conclusion. Rejected.** X-6 (REP:1474) and the GQ-03 row (REP:597) are about GQ-03 being resolved; GQ-03 is still resolved (GAPS:135). Only count and anchor are stale, hence Medium, not Regression.

**D-3** is bookkeeping: the Execution Log recorded the new count (TASK:456) but the Task Summary was not touched (TASK:374). **D-4** is an isolated anchor slip.

## Acceptance / coverage notes

- WC-10 applied at REP:58, :407, :481, :500, :752, :903, :1246. C8 [UNVERIFIED] tags at REP:103, :113, :572, :797, :1633. A4 rejected as CODE-CONTRADICTED at REP:325, :874, :1055, :1079, :1555, :1591.
- 10 sections ## 1 to ## 10 run REP:36 to REP:1715 (TASK:500 I17 check). Evidence Trail line counts REP:1723-1748 match disk. "43 files in qa/" (REP:1758) is dated to assembly time.
- Gate cycle counts and the two HALTs with deciding message IDs recorded (TASK:371-372); 88 qa files (TASK:370).
- Correct gaps-log anchors confirmed: REP:340 (GAPS:22-70), :538 (:20), :601 and :1246 (:119), :802 (:84), :1455 (:27), :1599 (:107).
- Pending by design: item 7.5 is this gate (TASK:457, attempt 2); 7.6 waits for it; `reflect_post` (TASK:375) is filled by 7.5.

## Structural / tech-debt notes

- Cite the gaps log by GQ id or by its "**Row count:**" line (GAPS:135), not by `:125`; a summary below a growing table moves with every row.
- At the next gate that allows report edits (for example the /sc:design hand-off), rewrite REP:229, :597, :1127, :1474 and :1754 against GQ-ids or the Row-count anchor, bring the Gaps Log count to 110/85/25, and fix REP:1577 to cite GAPS:64 (GQ-41).
- When the Execution Log records a count change, update the Task Summary in the same step; TASK:374 and P7:34 should carry 110/85/25 or state an as-of date.
- Carry forward to /sc:design: GQ-101..110 (GAPS:124-133); GQ-103 (1) `--no-optional-locks` is the safety item to carry first (GAPS:126).
