# Diff Analysis: reviewer deviation cards 1-3 (sc-reflect post, Wave 4)

## Metadata

- Mode: A (--compare), depth standard, focus: correctness, coverage, deviation-classification
- Variants: variant-1-original.md (reviewer-1, sonnet/analyzer, calibrated 0.78), variant-2-original.md (reviewer-2, haiku/qa, calibrated 0.82), variant-3-original.md (reviewer-3, opus/refactorer, calibrated 0.83)
- Audited set: TASKDIR = `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/` (REPORT = RESEARCH-REPORT-orchestrator-mode.md, GAPS = gaps-and-questions.md, TASK = the task file)
- Orchestrator ground checks (read-only batch, 13 blocks, BATCH_OK failures=0): TASK:545-560, TASK:574-582, REPORT:1-16, :227-230, :1535-1549, :1598-1606, :1734-1762, GAPS:1-28, :118-130, synth-06/synth-02/phase7-summary grep, qa-fidelity-verification-cycle1:1-12 and :70-82, web-01:205-232
- Binding constraint from the owner (debate context): the NB-4 research-gate exception, the Phase 6 anti-omission pass-with-exceptions (GQ-101, GQ-102, GQ-103; owner decision TASK:556) and the 4 entries under TASK "### Deviations" must be Authorized expansion or Necessary deviation, never Drift.

## Ground facts confirmed by the orchestrator

| Fact | Evidence |
|---|---|
| Owner decision line is TASK:556, not :552 | TASK:556 "Owner decision (coordinator msg_5970c0dfc669, 2026-11-08T00:38Z) ... Recorded in the report (exception paragraph after the NB-4 note near :15, Gaps Log bullet near :1754)"; TASK:552 is the NB-2 finding text |
| Gaps summary moved to :128; :125 is the GQ-102 row | GAPS:125 = GQ-102 row; GAPS:128 "**Row count:** 103 rows. Open: 78. Resolved: 25 ... Open blocking QA finding: none at the research and synthesis gates; ... Phase 6 anti-omission gate: GQ-101 (NB-2) and GQ-102 (NB-4c) are open blocking findings" |
| REPORT:229 quotes the old count and unqualified "none" | REPORT:229 "The summary counts at `gaps-and-questions.md:125` read \"Open: 75. Resolved: 25\" after the NB-4 fix, and state \"Open blocking QA finding: none\"." |
| REPORT:15 records the Phase 6 exception and that Section 8 steps 1.2, 1.3, 1.8, 1.9 are not yet corrected | REPORT:15 |
| REPORT:1537 completeness claim | "Every open GQ row is cited. Rows that share one resolution are grouped." 9.1 ends at row 64 = GQ-100 (REPORT:1605) |
| Settled rows inside 9.1 | REPORT:1547 row 7 GQ-09 "Settled by the sources"; REPORT:1598 row 57 GQ-67 "settled, not an open question" |
| Future-tense past gates | REPORT:1601 row 60 "Correct the wording in the final report"; REPORT:1602 row 61 GQ-97 "Re-cite at the Phase 5 synthesis gate"; REPORT:1754 "is re-checked at the Phase 5 synthesis gate"; GAPS:26 "re-check at Phase 5 synthesis gate"; GQ-97 open at GAPS:120 |
| REPORT:1754 counts updated, citation stale | "GQ-01 to GQ-103; 78 open, 25 resolved (`:125`)" |
| REPORT:1758 is a labelled snapshot | "Count as of report assembly (end of the Phase 5 synthesis gate): 43 files in `qa/` ... The Phase 6 report-lens files ... were written after assembly and are not counted." |
| web-01 source count | REPORT:1738 "14 sources"; web-01 Sources table rows 1-15 |
| Synthesis stale values, no snapshot label | synth-06:6 "GQ-01 to GQ-100" (range only, no :125); synth-06:13 "75 open rows, 25 resolved (`gaps-and-questions.md:125`)"; synth-06:228; synth-02:7, :230 ("now reads Open 75"), :315 "Every row GQ-01 to GQ-100" |
| phase7-summary:34 | repeats "(`:125`)" and the :1537 claim; notes settled rows 7, 57, 106, 109 |
| Fidelity counter labels | qa-fidelity-verification-cycle1:8 "|F_0'| = 4 for this pass"; :77 "|F_0| = 4"; :79 "|F_1| = 0" (deliberate pass-local re-base) |
| Report date | REPORT:3 "**Date:** 2026-11-07"; no Updated field; REPORT:15 records a 2026-11-08 decision |
| Gaps header | GAPS:4 Date 2026-11-07; GAPS:7 "carried below as an OPEN gap" (NB-4); GAPS:9-14 files-read list predates Phase 6 |

## Structural Differences

| ID | Difference | Severity |
|---|---|---|
| S-001 | Entry count and granularity: V1 12 entries (D-1 citation and D-2 qualifier split; D-12 new), V2 9 entries (citation, counts and range folded into R2-D1), V3 10 entries (citation R3-D1, counts plus qualifier R3-D2, range R3-D3, completeness R3-D4 split) | Medium |
| S-002 | V2 alone carries `coverage_assessment` (C-01..C-10) and `task_summary_number_checks`; V1 and V3 give coverage only in notes | Low |
| S-003 | V3 has no entries for T1 D-7, D-9, D-10, D-11 (research-gate exception and three of the four Deviations entries); its counts show 0 Authorized | High |
| S-004 | V3 carries `orchestrator_mapping_note`; V2 `orchestrator_note`; t1_ref values partly orchestrator-mapped in V2 and V3 | Low |

## Content Differences

| ID | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Stale `:125` citation (T1 D-1) | Drift important, 6 report sites + GAPS:128 | Drift important, sites :1496, :1754 only (plus TASK:270 criterion) | Drift important, 6 report sites | Low (class agreed, site coverage differs) |
| C-002 | Stale "Open 75" and unqualified "none" (T1 D-2) | Drift important (qualifier at :229) | folded into R2-D1 | Drift important, 5 sites, adds X-6 "Resolved, not a live conflict" at :1127/:1474 | Low |
| C-003 | Section 9 completeness claim :1537 (T1 D-3) | Drift important, adds :684, :1496 ranges | Drift important | Drift important, extends to 8.1/8.2 (:1335), 7.1 (:1156), :1605, phase7-summary:34 | Low |
| C-004 | "GQ-01 to GQ-100" ranges | inside R1-D3 (:684, :1496) | inside R2-D1 | separate R3-D3 minor, adds synth-06:6, :228, synth-02:315 | Low |
| C-005 | Synthesis 75/25 at :125 (T1 D-4) | Drift minor | not a deviation (historical) | Drift minor, adds :1750 source/output split | Medium (disputed point a) |
| C-006 | Past gates as future actions (T1 D-5) | Drift minor, :1754 | absent | Drift minor, :1601, :1602, :1754, GAPS:26 | Low |
| C-007 | Fidelity counter labels (T1 D-6) | Drift minor, optional relabel | explicitly not a deviation | absent | Medium (disputed point b) |
| C-008 | Research-gate PASS-BY-EXCEPTION (T1 D-7) | Authorized | Authorized | absent | Medium |
| C-009 | Phase 6 anti-omission exception (T1 D-8) and uncorrected Section 8 steps | Authorized (whole exception) | Authorized (whole exception) | Necessary (R3-D9, Section 8 steps only) | Medium (disputed point c) |
| C-010 | Deviations entries: pointer prompts, WebSearch fallback / rf-analyst rerun, NB-4 fix placement (T1 D-9..D-11) | Necessary x3 | Necessary x3 | absent | Medium |
| C-011 | REPORT:1758 "43 files in qa/" and TASK:580 history notes | absent | historical, not a deviation (note) | Necessary minor (R3-D10) | Medium (disputed point a) |

## Contradictions

| ID | Contradiction | Variants | Falsifiable test |
|---|---|---|---|
| X-001 | Synthesis snapshot counts are Drift (V1, V3) vs not a deviation (V2) | V1, V3 vs V2 | Does any synthesis file label its count as a snapshot, and is synthesis a frozen gate artifact under the task's rules? |
| X-002 | Fidelity |F_0|/|F_1| labels are Drift (V1) vs not a deviation (V2) | V1 vs V2 | Does the QA file declare a pass-local index (QA:8 `|F_0'|`), and do the numbers agree with TASK:540-542? |
| X-003 | Uncorrected Section 8 steps are part of an Authorized expansion (V1, V2) vs a Necessary deviation (V3) | V1, V2 vs V3 | Was leaving them a scope addition the owner authorized, or a constraint-forced departure from the plan's requirement? |
| X-004 | Labelled history note at REPORT:1758 is a Necessary deviation (V3) vs not a deviation (V2) | V3 vs V2 | Does a correctly labelled snapshot depart from any requirement at all? |
| X-005 | Owner decision line: V1 cites TASK:552, V2/T1 cite TASK:556 | V1 vs V2 | Orchestrator check: TASK:556 holds the decision text (V1 mis-cited) |
| X-006 | V1 says T1's synth-06:6 citation is unconfirmed; V3 cites synth-06:6 | V1 vs V3 | Orchestrator check: synth-06:6 carries the GQ-100 range but not :125 / 75 - both correct for different claims |

## Unique Contributions

| ID | Variant | Contribution | Verified by orchestrator | Value |
|---|---|---|---|---|
| U-001 | V1 | R1-D12 phase7-summary:34 repeats `:125` | yes | Medium |
| U-002 | V2 | R2-D3 settled rows 7, 57, 106, 109 inside the 9.1-9.5 open tables | rows 7 and 57 yes; phase7-summary:34 lists all four | Medium |
| U-003 | V2 | R2-D4 web-01 14 vs 15 sources at REPORT:1738 | yes | Low |
| U-004 | V3 | R3-D5 gaps header (GAPS:4, :7, :14) reads as current, NB-4 "OPEN" | yes | Medium |
| U-005 | V3 | R3-D6 extension: :1601, :1602, GAPS:26 future-tense gates | yes | Medium |
| U-006 | V3 | R3-D8 report header date with no Updated field | yes (REPORT:3) | Low |
| U-007 | V3 | R3-D3 adds synth-02:315 "Every row GQ-01 to GQ-100" | yes | Low |
| U-008 | V3 | R3-D4 extension to 8.1/8.2 (:1335) and 7.1 (:1156) | not checked by orchestrator | Medium |
| U-009 | V3 | R3-D2 X-6 at :1127/:1474 "Resolved, not a live conflict" now false | not checked by orchestrator | Medium |
| U-010 | V2 | coverage_assessment plus full Task Summary number check | n/a (method) | Medium |

## Shared Assumptions

| ID | Assumption | Classification | Taxonomy | Promoted |
|---|---|---|---|---|
| A-001 | No finding is a Regression: the task is docs-only and no item that passed a gate now fails, even though Phase 6 edits made previously true report claims (:229, :1537) false | STATED (V1 R1-D1 rationale, V3 notes); UNSTATED in V2 | L3 (invariant: what counts as "previously passing") | yes [SHARED-ASSUMPTION] |
| A-002 | The citation, count, range and completeness findings share one root cause: GQ-101..103 inserted above the summary without a citation sweep | STATED (V1 notes, V3 R3-D1); UNSTATED in V2 | L2 | yes |
| A-003 | The owner exception covers carrying GQ-101..103 and editing :15 and :1754 only; it does not cover leaving other sites stale or the false completeness claim | STATED (V1, V2, V3 rationales) | L3 (boundary of an authorization) | yes |
| A-004 | Synthesis files and phase7-summary are in audit scope as live documents, not frozen gate artifacts | UNSTATED in all three (V2 implicitly treats synthesis as history) | L3 (boundary) | yes |
| A-005 | The orchestrator's t1_ref and severity mappings (V2, V3) are faithful to what the reviewers meant | UNSTATED | L1 | yes |

## Summary

- Total diff points: S 4, C 11, X 6, U 10, A 5 (convergence denominator S+C+X+A = 26)
- Highest-severity items: S-003 (V3 omits the research-gate exception and three Deviations entries), X-001/X-003/X-004 (classification disputes a and c), A-001 (Regression boundary)
- All three variants agree on the verdict PASS-WITH-DRIFT and on zero Regressions.
- Similarity: well above 10% difference; full debate required.
