# Tier-1 reflect card (Wave 1C): TASK-RESEARCH-orchestrator-supervision-20261107-073942

Paths are relative to the task folder. `TASK` = `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md`; `REPORT` = `RESEARCH-REPORT-orchestrator-mode.md`; `GAPS` = `gaps-and-questions.md`.

## Summary

**Verdict: PASS-WITH-DRIFT.** Authorized expansion 2, Necessary deviation 3, Drift 6, Regression 0.

Every deliverable the seven objectives ask for is on disk. Every Task Summary number checks out against the files: report 1762 lines and 10 sections; 10 research files; 7 synthesis files; 88 QA files; 117 Section 9 rows; 103 gap rows, 78 open and 25 resolved. Every `|F|` sequence in Phase Gate Findings matches the QA verdict files it cites, and every final-verdict file it names exists. The two gate exceptions and the four Deviations entries are owner-approved or forced and documented, so none of them is Drift. The Drift is all one root cause. When GQ-101 to GQ-103 were added to `GAPS` on 2026-11-08, the gap-count summary moved from `GAPS:125` to `GAPS:128`, but only one of the report's count statements was updated (`REPORT:1754`, and it still cites `:125`). The report still cites the old line, quotes "Open: 75" in five places, and still says "Open blocking QA finding: none" in Section 2. Section 9 says it lists every open gap row, yet it has no row for GQ-101 to GQ-103. None of this reverses a gate outcome, because `REPORT:15` states the exceptions correctly. But a reader of Section 2, 4, 7, 8 or 9 alone would see stale counts and no Phase 6 open blockers.

## Root-cause / deviations

### D-1: Gap-count citation `GAPS:125` and the "Open: 75" quote went stale after GQ-101 to GQ-103 were added

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:229`, `:597`, `:1127` (2 times), `:1474` (2 times), `:1496`, `:1754`
- **Mapped tasklist item:** Objective 6 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:65`), and the owner decision that added GQ-101 to GQ-103 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`)
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:229`: "The summary counts at `gaps-and-questions.md:125` read "Open: 75. Resolved: 25"". The actual text is now at `gaps-and-questions.md:128`: "**Row count:** 103 rows. Open: 78. Resolved: 25". `gaps-and-questions.md:125` is now the GQ-102 row.
- **Classification:** Drift
- **Rationale:** The owner-approved edit added three rows above the summary line and fixed only `REPORT:1754`'s numbers (78/25), not its line citation. Five other report sites still quote 75 open and cite `:125`. Undocumented and inaccurate. Nothing that passed before now fails, so it is not a Regression.
- **Severity:** important (6 sites in the report contradict the gaps log and `REPORT:1754`)
- **Default remediation:** In `REPORT`, change every `gaps-and-questions.md:125` / `` `:125` `` count citation to `:128`. Change "Open: 75" / "Open 75" to 78 at `:229`, `:597`, `:1127`, `:1474` and `:1496`, or mark each as the Phase 5 snapshot ("75 open before GQ-101 to GQ-103").

### D-2: Section 2 still says "Open blocking QA finding: none", which the gates left open

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:229`
- **Mapped tasklist item:** Check (7), report states nothing the gates left open as settled. Owner decision at `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`.
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:229`: "and state "Open blocking QA finding: none"". `gaps-and-questions.md:128`: "Open blocking QA finding: none at the research and synthesis gates; ... GQ-101 (NB-2) and GQ-102 (NB-4c) are open blocking findings".
- **Classification:** Drift
- **Rationale:** The quote drops the qualifier "at the research and synthesis gates". That makes the report say there are no open blocking findings. That contradicts `REPORT:15` and the anti-omission HALT (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:550-556`). The same unqualified wording comes from `synthesis/synth-01-problem-current-state.md:201` and `synthesis/synth-02-target-gaps.md:7`.
- **Severity:** important
- **Default remediation:** Rewrite the `REPORT:229` sentence to quote `GAPS:128` in full, or add "(research and synthesis gates; Phase 6 left GQ-101 and GQ-102 open, see :15)".

### D-3: Section 9 says it cites every open gap row, but GQ-101 to GQ-103 are missing; coverage tables stop at GQ-100

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:1537`, `:684`, `:1496`
- **Mapped tasklist item:** Objective 6 (10-section report, `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:65`); owner decision `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:1537`: "Every open GQ row is cited." A grep for `GQ-10[123]` in `REPORT` hits only `:15` and `:1754`. `REPORT:684`: "Every row GQ-01 to GQ-100".
- **Classification:** Drift
- **Rationale:** The owner decision named only `:15` and `:1754` as the places to record the exception. It did not change Section 9's claim that it covers every open row. GQ-101 to GQ-103 are open Important plan blockers (`gaps-and-questions.md:124-126`), and the 117-row Section 9 has no row for them. /sc:design reads Section 9 as its open-questions input [INFERRED], so it would miss them there.
- **Severity:** important
- **Default remediation:** Add three 9.1 rows (GQ-101, GQ-102, GQ-103) pointing to `GAPS:124-126` and `REPORT:15`, and widen `:684` and `:1496` to "GQ-01 to GQ-103". If rows are added, update the Task Summary count of 117 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:374`) and `synthesis/phase7-summary.md:34`.

### D-4: Synthesis files carry the same stale `:125` / "Open 75" statements

- **Location:** `synthesis/synth-01-problem-current-state.md:201`, `synthesis/synth-02-target-gaps.md:7`, `:230`, `synthesis/synth-04-options-recommendation.md:220`, `synthesis/synth-05-implementation-plan.md:261`, `:283`, `synthesis/synth-06-questions-evidence.md:6`, `:13`, `:228`
- **Mapped tasklist item:** Objective 5 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:64`)
- **Evidence:** `synthesis/synth-02-target-gaps.md:7`: "its summary line `:125` reads Open 75 / Resolved 25 with no open blocking QA finding."
- **Classification:** Drift
- **Rationale:** These statements were correct when the synthesis gate passed them (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:527`). They are now wrong about the live gaps file, with no history note. Lower impact than D-1 because the report replaces the synthesis files as the deliverable.
- **Severity:** minor
- **Default remediation:** Add a one-line "snapshot as of the Phase 5 gate; see `GAPS:128`" note at the top of each synthesis file, or leave them as is and fix only `REPORT` (D-1).

### D-5: "Is re-checked at the Phase 5 synthesis gate" is still written as future, though the re-check already passed

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:1754`, `gaps-and-questions.md:128`
- **Mapped tasklist item:** Research-gate exception follow-through (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:521`, `:524`)
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:1754`: "GQ-03 (NB-4) was resolved by the NB-4 fix pass and is re-checked at the Phase 5 synthesis gate." `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:524`: "NB-4 re-check PASS 10 of 10."
- **Classification:** Drift
- **Rationale:** The wording is left over from before the gate ran. It does not change any outcome.
- **Severity:** minor
- **Default remediation:** Change it to "was re-checked at the Phase 5 synthesis gate (PASS, 10 of 10)".

### D-6: Counter labels in the fidelity cycle-2 verification are off by one from the task log

- **Location:** `qa/qa-fidelity-verification-cycle1.md:77`, `:79`
- **Mapped tasklist item:** Fidelity gate cycle control (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:540-542`)
- **Evidence:** `qa/qa-fidelity-verification-cycle1.md:77`: "Previously open blocking: |F_0| = 4 (C1-01 to C1-04)"; `:79`: "**|F_1| = 0**". The task log says `|F_1| = 4` and `|F_2| = 0` (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:540`, `:542`).
- **Classification:** Drift
- **Rationale:** The numbers agree (4 then 0) but the index labels do not. Every other gate's cycle-1 verifier uses the task log's indexing (for example `qa/qa-synthesis-verification-cycle1.md:68`). Cosmetic, with no effect on the verdict.
- **Severity:** minor
- **Default remediation:** None needed for the outcome. Optionally relabel to `|F_1| = 4`, `|F_2| = 0`.

### D-7: Research-gate pass-by-exception for NB-4

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:519-521`, `:578`; `qa/qa-nb4-fix-log.md`; `RESEARCH-REPORT-orchestrator-mode.md:13`; `gaps-and-questions.md:7`
- **Mapped tasklist item:** Objective 3 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:62`); item 182 precondition
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:521`: "Research gate closed as PASS-BY-EXCEPTION at cycle 2 with 1 open blocking finding (NB-4); the exception is recorded in the final report."
- **Classification:** Authorized expansion
- **Rationale:** The coordinator approved it (msg_c2aed3001b18). `REPORT:13` states it accurately. The `|F|` sequence 28 -> 3 -> 1 matches `qa/qa-consolidated-findings-phase3.md:116`, `qa/qa-consolidated-findings-phase3-cycle1.md:15` and `qa/qa-research-verification-qualitative-cycle1.md:82`.
- **Severity:** minor
- **Default remediation:** None.

### D-8: Anti-omission gate passed with exceptions (NB-2, NB-4c as GQ-101 and GQ-102; ponytail-review findings as GQ-103)

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:549-556`; `gaps-and-questions.md:124-126`; `RESEARCH-REPORT-orchestrator-mode.md:15`, `:1754`; `qa/ponytail-review-phase1-plan.md`
- **Mapped tasklist item:** Objective 6 anti-omission gate (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:65`)
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`: "The anti-omission gate is passed with exceptions, not clean: it halted on the 2-cycle limit with 2 open blocking findings."
- **Classification:** Authorized expansion
- **Rationale:** The owner decided it (msg_5970c0dfc669). `REPORT:15` matches the log: "18 -> 1 -> 2", `[HALT-MONOTONICITY] |F|=2`, 2026-11-08, carried to /sc:design. The /ponytail-review file is an owner-requested addition outside the checklist. The related stale citations are D-1 to D-3.
- **Severity:** minor
- **Default remediation:** None beyond D-1 to D-3.

### D-9: Pointer prompts instead of retyped prompts for subagents

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:577`
- **Mapped tasklist item:** Every agent-spawn item
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:577`: "each subagent is given a pointer prompt ... instead of a retyped copy".
- **Classification:** Necessary deviation
- **Rationale:** Forced by the coordinator's context limits after the autocompact thrash, and documented. The agent reads the same instruction bytes from disk.
- **Severity:** minor
- **Default remediation:** None.

### D-10: WebSearch/WebFetch fallback for Tavily, and the rf-analyst re-run in Phase 4

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:579`; `research/web-01-agent-supervisor-session-health.md`; `research/web-02-static-status-report-conventions.md`; `RESEARCH-REPORT-orchestrator-mode.md:1734`, `:1739`
- **Mapped tasklist item:** Objective 4 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:63`)
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:579`: "Tavily MCP tools are not available in this session, so both Phase 4 web items use the WebSearch/WebFetch fallback".
- **Classification:** Necessary deviation
- **Rationale:** An environment limit, documented in the log, in both output files and in report Section 10.
- **Severity:** minor
- **Default remediation:** None.

### D-11: NB-4 fix ran as its own pass between Phase 4 and Phase 5

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:580`; `qa/qa-nb4-fix-log.md`
- **Mapped tasklist item:** Coordinator decision at `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:521`
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:580`: "Phase 4 here is external research and synthesis is Phase 5. So the fix ran as one serialized rf-qa fix pass after Phase 4 and before Phase 5".
- **Classification:** Necessary deviation
- **Rationale:** It resolves a contradiction between the coordinator's wording and the phase numbering, and it is documented. The synthesis gate re-checked NB-4 and passed it 10 of 10 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:524`).
- **Severity:** minor
- **Default remediation:** None.

## Coverage / acceptance

| Objective | Status | Grounding |
|---|---|---|
| 1. Verify scope-01..04 | PASS | `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`; verification results logged at `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:385-389` |
| 2. Close G-A and G-B | PASS | `research/05-orca-row-schema.md` (206 lines), `research/06-orca-open-questions.md` (190 lines), plus the gate fix file `research/07-gate-gap-fill.md` |
| 3. Research gate (10 agents, at most 2 fix cycles, gaps file) | PASS by Authorized exception (D-7) | 10 gate reports in `qa/` (analyst completeness/cross-validation, research evidence/gaps/qualitative, 2 each); 2 fix logs; `gaps-and-questions.md` (362 lines, 103 rows) |
| 4. External patterns | PASS (Necessary deviation D-10) | `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md` |
| 5. Six synthesis files and synthesis gate | PASS (gate PASS at cycle 2; stale snapshot text D-4) | `synthesis/synth-01..06`; `qa/qa-synthesis-verification-cycle1.md:83` PASS, `qa/qa-synthesis-verification-qualitative-cycle1.md:83` PASS |
| 6. Report with 10 sections; 11 lens, 4+1 fidelity and 4 anti-omission agents | PASS-WITH-DRIFT (D-1 to D-3; anti-omission by Authorized exception D-8) | `## 1` to `## 10` at `RESEARCH-REPORT-orchestrator-mode.md:36,44,345,532,690,923,1096,1189,1531,1715`; 11 `qa/qa-lens-*.md`; 5 `qa/qa-source-fidelity-report-*.md`; 4 `qa/qa-anti-omission-report-*.md`; `qa/qa-fix-verification-cycle1.md:101` PASS; `qa/qa-fidelity-verification-cycle1.md:89` PASS; `qa/qa-anti-omission-verification-qualitative-cycle1.md:94` FAIL (exception) |
| 7. Close-out | Partial by design (7.5 is this gate; 7.6 waits on it) | `synthesis/phase7-summary.md`; `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:366-376`, `:492-505` |
| Read-only constraint | PASS (accepted from the orchestrator; I ran no git command) | `baseline-git-status.txt:1-3` (3 untracked entries); `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:505`. Caveat [INFERRED]: porcelain lists untracked directories, not the files in them, so a change inside `.dev/issues/339/` or `.dev/brainstorms/...` would not show as a new entry. |

**Task Summary number checks (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:368-376`):**

| Claim | On disk | Result |
|---|---|---|
| Report 1762 lines, 10 sections (:368) | `wc -l` 1762; ten `## N.` headings (:36 to :1715) | PASS |
| Research 10 files, 8 codebase + 2 web (:369) | 10 files in `research/`, 2 named `web-*` | PASS |
| Synthesis 6 + `phase7-summary.md` (:370) | 7 files in `synthesis/` | PASS |
| 88 files in `qa/` (:370) | 88 | PASS |
| Research gate 28 -> 3 -> 1 (:371) | `qa/qa-consolidated-findings-phase3.md:116`, `qa/qa-consolidated-findings-phase3-cycle1.md:15`, `qa/qa-research-verification-qualitative-cycle1.md:82` | PASS |
| Synthesis gate 15 -> 3 -> 0 (:371) | `qa/qa-consolidated-findings-phase5.md:40`, `qa/qa-consolidated-findings-phase5-cycle1.md:5`, `qa/qa-synthesis-verification-cycle1.md:68` | PASS |
| Lens QA 49 -> 5 -> 0 (:371) | `qa/qa-consolidated-findings-phase6.md:8`, `qa/qa-consolidated-findings-phase6-cycle1.md:5`, `qa/qa-fix-verification-cycle1.md:85` | PASS |
| Fidelity 21 -> 4 -> 0 (:371) | `qa/qa-fidelity-consolidated-findings.md:11`, `qa/qa-fidelity-consolidated-findings-cycle1.md:5`, `qa/qa-fidelity-verification-cycle1.md:79` (labels: D-6) | PASS |
| Anti-omission 18 -> 1 -> 2, HALT (:371) | `qa/qa-anti-omission-consolidated-findings.md:4`, `qa/qa-anti-omission-consolidated-findings-cycle1.md:5`, `qa/qa-anti-omission-verification-qualitative-cycle1.md:15` ("2 open blocking findings") | PASS |
| Fidelity cycle 0 is 5 reports (1 FAIL, 2 PASS, 3-5 FAIL) (:539) | `qa/qa-source-fidelity-report-1.md:67` FAIL, `-2.md:71` PASS, `-3.md:68` FAIL, `-4.md:67` FAIL, `-5.md:58` FAIL | PASS |
| Section 9 has 117 rows (1 to 109 plus 8 lettered), 4 settled (:374) | 109 numbered + 8 lettered (33a, 81a-d, 98a-c) between `REPORT:1531` and `:1715`; settled rows 7, 57, 106, 109 (`REPORT:1547`, `:1598`, `:1682`, `:1685`) | PASS |
| Gaps log 103 rows, 78 open, 25 resolved (:374) | 103 `| GQ-` rows; Status column: 78 `open*`, 25 `resolved` (GQ-03, 07, 13, 18, 20, 42, 45, 55, 68-83, 96), matching `gaps-and-questions.md:128` | PASS |
| Recommended option A1 at report :1098 (:373) | quoted at `synthesis/phase7-summary.md:21` | PASS |
| 4 Deviations entries (:376) | `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:577-580` | PASS |
| Every final-verdict file named in Phase Gate Findings exists | all 38 named files exist in `qa/` | PASS |
| Report Section 10 line counts (`REPORT:1723-1748`) | match `wc -l` for all 8 research, 2 web and 6 synthesis files | PASS |

**Exception statements vs the task log:** `REPORT:13` matches `TASK:521`/`:578`/`:580` (PASS). `REPORT:15` matches `TASK:547-556` (PASS). `REPORT:1754` matches on counts and GQ IDs but cites `:125` and uses the future tense (D-1, D-5).

## Structural / tech-debt

- **Citation hygiene:** Every `gaps-and-questions.md:NNN` citation in `REPORT` was checked. Row citations at or below line 123 still resolve, because the new rows went in after GQ-100: `:20` severity rule, `:22-70` GQ-01 to GQ-47, `:27` GQ-04, `:82` GQ-59, `:84` GQ-61, `:107` GQ-84, `:119` GQ-96. Only the `:125` count citation went stale (D-1). Pinning a moving summary line by number is fragile. A label citation ("the **Row count:** line") would survive later row additions.
- **Stale history notes, kept on purpose:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:580` ("row-count summary at `gaps-and-questions.md:125` (75 open, 25 resolved)") and `qa/qa-nb4-fix-log.md:39` are timestamped records and correct for their time. `RESEARCH-REPORT-orchestrator-mode.md:1758` ("43 files in `qa/`" as of assembly, against 88 now) says it is a snapshot, so it is acceptable, but a reader may take it as current.
- **Count drift:** "GQ-01 to GQ-100" stays at `REPORT:684`, `:1496` and `synthesis/synth-06-questions-evidence.md:6`, `:228` (D-3, D-4). The report header date is still 2026-11-07 (`REPORT:3`), though `:15` and `:1754` were edited on 2026-11-08 [INFERRED: no "updated" field exists].
- **Placeholders:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:466-488`: the Phase 1-6 Findings sections still read "(none yet)". The HALTs are logged in Phase Gate Findings instead, which item (e) at `:504` accepts.
- **Maintainability of the report:** At 1762 lines, the report repeats the gap-count statement in 7 places (`:229`, `:597`, `:1127`, `:1474`, `:1496`, `:1754`, plus `:684` coverage). That repetition is why one owner-approved edit left five stale copies. One authoritative count line, with the other places pointing to it, would stop a repeat of D-1.

## Self-confidence

0.88. I verified every count and citation directly on disk with grep, wc and Read. I could not run git, so the read-only check relies on the orchestrator's porcelain observation. I did not re-verify the content of the 88 QA files beyond their verdict and count lines.
