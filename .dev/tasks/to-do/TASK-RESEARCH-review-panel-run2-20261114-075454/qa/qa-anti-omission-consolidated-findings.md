# QA Anti-Omission Consolidated Findings (Gate 5, review 1, item 6.58)

**Status:** Complete
**Result:** F_0 = 0; verdict PASS (the one recount finding P6A-RC-1 was CLOSED-BY-RERUN)
**Section order in this file:** Reading check, (2), (1), (5), (6)(ii), (3), (4), (6); each is headed with its item 6.58 number.
**Date:** 2026-11-14
**Grading:** `qa/grading-override.md` applies (blocking only on conditions 1, 2 or 3; every other omission is MINOR with `(minor under grading override)`).
**Partition used:** the FINAL partition in `qa/gate5-partition.md`.
**Inputs read completely:** `qa/qa-anti-omission-report-1.md` to `-4.md` (all four are `Status: Complete`, each verdict PASS with 0 blocking omissions under the override), `qa/grading-override.md`, `qa/gate5-partition.md`, the four enumeration files (structure, every `COUNT` line, section ranges), the Gate 3 and Gate 4 fix logs. The report `RESEARCH-REPORT-review-panel-unification-run2.md` and the input files were read only for the recount and the sampling below; nothing was modified.
**Independence:** the run-1 task folder and the queued-run note were not read, listed, grepped or cited; no repo-wide search was made.

## Reading check

| Report | File | Status line | Verdict quoted | Enumeration file | Every assigned file has a `COUNT` line |
|---|---|---|---|---|---|
| 1 | `qa/qa-anti-omission-report-1.md` (82 lines) | `Status: Complete` | PASS, 0 blocking | `qa-anti-omission-enumeration-1.md` (3,283 lines) | yes (26 of 26: 7 research/web, 3 synthesis, 15 debate results, ledger 19) |
| 2 | `qa/qa-anti-omission-report-2.md` (143 lines) | `Status: Complete` | PASS, 0 blocking | `qa-anti-omission-enumeration-2.md` (3,531 lines) | yes (13 of 13: 8 research/web, 3 synthesis, ledgers 21 and 20) |
| 3 | `qa/qa-anti-omission-report-3.md` (174 lines) | `Status: Complete` | PASS, 0 blocking | `qa-anti-omission-enumeration-3.md` (4,175 lines) | yes (13 of 13 plus the `NONROW-COUNT` line for the two ledgers' 55 non-row items) |
| 4 | `qa/qa-anti-omission-report-4.md` (97 lines) | `Status: Complete` | PASS, 0 blocking | `qa-anti-omission-enumeration-4.md` (963 lines) | yes (2 of 2: ledger 24, synth-08) |

No report is missing or `In Progress`; no enumeration file is missing; no `COUNT` line is missing.

## (2) Enumeration totals (quoted from the four reports) and per-file counts

### (2a) Totals per report

| Report | Agent / final partition | Findings enumerated | Represented | Covered-by-dedup | Justified-removed | Omitted (whole finding) | Detail-level / sub-detail rows (all minor) | Blocking omissions (agent) |
|---|---|---|---|---|---|---|---|---|
| 1 | research 01-05, web-01, web-02, synth-05/06/07, 15 debate results, ledger 19 | 3,183 | 3,183 | 0 | 0 | 0 | 10 | 0 |
| 2 | research 06-11, web-03, web-04, synth-04/09/10, ledgers 21 and 20 | 3,431 | 3,400 (main substance; 65 of them lack a sub-detail) | 15 (14 ledger rows + web-04 entry 23) | 0 | 16 | 65 (81 rows in all with the 16) | 0 |
| 3 | research 12-18, gaps-and-questions, synth-01/02/03, ledgers 22 and 23 | 4,067 | 3,724 | 88 (45 ledger rows + 43 register rows); plus 209 gap pointer rows covered by the ledger row they name | 0 | 46 (research 12: 4; 13: 7; 14: 13; 15: 3; 16: 1; 17: 2; 18: 2; non-row ledger items: 6; gap rows: 8) | 0 (plus 13 pair-check notes PC-1 to PC-13 that are not omissions) | 0 |
| 4 | ledger 24, synth-08 | 933 | 829 | 104 (61 ledger-24 rows + 43 register rows) | 0 | 0 | 5 notes (not omissions) | 0 |
| **All** | | **11,614** | 11,136 | 207 (+209 pointer rows) | 0 | 62 | 75 detail rows + 13 pair notes + 5 notes | 0 |

Arithmetic checks made: report 1: 3,183 = 249 (research/web) + 1,517 (synth) + 531 (15 debates) + 886 (ledger 19); report 2: 3,431 = 326 + 552 + 2,553; report 3: 4,067 = 461 + 200 + 555 + 1,045 + 1,806 (ledgers 22 and 23 with 55 non-row items); 3,724 + 88 + 209 + 46 = 4,067; report 4: 933 = 589 + 344, 829 + 104 = 933; 3,400 + 16 + 15 = 3,431.

### (2b) Per-file counts of every enumeration file (equal to each file's `COUNT` lines; every line was found by Grep)

Enumeration file 1 (`qa/qa-anti-omission-enumeration-1.md`, total 3,183):

| File | COUNT |
|---|---|
| research/01-overlap-capability-matrix.md | 44 |
| research/02-finding-contract.md | 48 |
| research/03-merge-ledger-verdict.md | 33 |
| research/04-dispatch-identity-tiers.md | 46 |
| research/05-input-delivery-brief.md | 31 |
| research/web-01-multi-model-review-evidence.md | 24 |
| research/web-02-claude-code-hooks-headless.md | 23 |
| synthesis/synth-06-conflict-log.md | 325 |
| synthesis/synth-05-options.md | 629 |
| synthesis/synth-07-recommendation-architecture.md | 563 |
| 15 debate results (collaboration-exchange-capability 32, consumer-entry-effect-and-delivery 33, core-shape-and-finding-contract 36, dispatch-and-launch-mechanism 30, eval-acceptance-and-harness-owner 44, ledger-clearing-and-verdict-authority 40, limits-repair-policy 41, merge-verdict-policy-and-quorum 28, panel-resolution-and-tier-source 36, pr-review-wire-format-and-slot 33, process-redesign-modules 37, reflect-tier2-engine-composition 37, rfqa-first-step-and-readonly-scope 31, run-record-and-served-model-capture 38, tasklist-medium-and-fidelity-vocab 35) | 531 |
| research/19-value-ledger-handoffs.md | 886 |

Enumeration file 2 (`qa/qa-anti-omission-enumeration-2.md`, total 3,431):

| File | COUNT |
|---|---|
| research/21-value-ledger-brainstorms.md | 1,685 |
| research/20-value-ledger-e2-study.md | 868 |
| research/06-reflect-two-engines.md | 69 |
| research/07-e1-evidence-grading.md | 38 |
| research/08-e2-evidence-grading.md | 46 |
| research/09-collaboration-designs.md | 42 |
| research/10-process-redesign.md | 43 |
| research/11-consumers-tasklist-workflow.md | 35 |
| research/web-03-git-branch-hierarchy-stacked-prs.md | 24 |
| research/web-04-finding-schemas-review-bots.md | 29 |
| synthesis/synth-04-external-findings.md | 145 |
| synthesis/synth-09-sequence-and-gates.md | 191 |
| synthesis/synth-10-questions-evidence.md | 216 |

Enumeration file 3 (`qa/qa-anti-omission-enumeration-3.md`, total 4,067):

| File | COUNT |
|---|---|
| research/22-value-ledger-collab-designs.md | 955 (+ non-row items, see below) |
| research/23-value-ledger-e1-e3-code.md | 796 (+ non-row items, see below) |
| non-row items of ledgers 22 and 23 (`NONROW-COUNT`) | 55 (28 + 27) |
| research/12-consumers-spec-review.md | 74 |
| research/13-future-pr-review-and-rfqa.md | 110 |
| research/14-e3-variants-and-experiments.md | 97 |
| research/15-telemetry-manifest-run-record.md | 60 |
| research/16-eval-governance.md | 61 |
| research/17-defect-register.md | 200 |
| research/18-repo-constraints-and-branching.md | 59 |
| gaps-and-questions.md | 555 |
| synthesis/synth-01-problem-current-state.md | 497 |
| synthesis/synth-02-overlap-matrix.md | 203 |
| synthesis/synth-03-target-gaps.md | 345 |

Enumeration file 4 (`qa/qa-anti-omission-enumeration-4.md`, total 933):

| File | COUNT |
|---|---|
| research/24-value-ledger-evidence-consumers.md | 589 |
| synthesis/synth-08-value-inventory.md | 344 (63 prose items, 10 destination groups, 41 P3-012 rows, 59 ledger-by-destination groups, 171 defect-register rows) |

### (2c) INDEPENDENT RECOUNT, first pass (item 6.58 (6)(i))

The three files per agent were chosen by me from the final partition, the three largest by `wc -l` of the assigned files (measured here: agent 1 synth-05 991, ledger 19 986, synth-07 673; agent 2 ledger 21 1,797, ledger 20 935, synth-04 606; agent 3 ledger 22 1,046, ledger 23 894, synth-01 749; agent 4 has only two assigned files, synth-08 6,127 and ledger 24 671, so both were recounted and no third file exists). The enumerated value `e` is the number of numbered entries I counted in that file's section of the enumeration file with a read-only `awk` over the section's line range (it equals the `COUNT` line in every case); `r` is my own recount of the source file.

Methods: ledgers, `grep -c '^| VL-NN-'` (and `grep -o ... | sort -u | wc -l` for distinct ids, equal in every case). synth-05, synth-07, synth-01: non-blank lines minus two lines per table (its header row and its separator row), so headings, prose lines and table data rows each count once. synth-04: `grep -c '^\*\*Finding:\*\*'` blocks plus table data rows (header and separator rows excluded; headings and prose paragraphs not counted, the most generous recount for the agent). synth-08: own content only (the ledger rows are recounted by the ledger lines): 171 `DR-` rows + 59 distinct (ledger, destination) groups (awk over the headings) + 20 headings + 59 data rows of the four non-ledger tables (8.1.0: 8, P3-011: 7, P3-014: 3, P3-012: 41) + 28 prose lines = 337.

```
AGENT 1 FILE synth-05-options.md ENUMERATED=629 RECOUNT=629
AGENT 1 FILE 19-value-ledger-handoffs.md ENUMERATED=886 RECOUNT=886
AGENT 1 FILE synth-07-recommendation-architecture.md ENUMERATED=563 RECOUNT=563
AGENT 2 FILE 21-value-ledger-brainstorms.md ENUMERATED=1685 RECOUNT=1685
AGENT 2 FILE 20-value-ledger-e2-study.md ENUMERATED=868 RECOUNT=868
AGENT 2 FILE synth-04-external-findings.md ENUMERATED=145 RECOUNT=182
AGENT 3 FILE 22-value-ledger-collab-designs.md ENUMERATED=955 RECOUNT=955
AGENT 3 FILE 23-value-ledger-e1-e3-code.md ENUMERATED=796 RECOUNT=796
AGENT 3 FILE synth-01-problem-current-state.md ENUMERATED=497 RECOUNT=493
AGENT 4 FILE synth-08-value-inventory.md ENUMERATED=344 RECOUNT=337
AGENT 4 FILE 24-value-ledger-evidence-consumers.md ENUMERATED=589 RECOUNT=589
```

Result: ten of eleven lines pass (`e` at least 0.9 times `r`). One fails: AGENT 2 FILE synth-04-external-findings.md ENUMERATED=145 RECOUNT=182, 145 is 0.797 of 182 (shortfall 20.3 percent, below the 0.9 line, which is 163.8). The agent enumerated one entry per `**Finding:**` block (68), the 15 takeaway rows and the 62 coverage-table rows, and did not enumerate the other 37 table data rows (182 minus 145) of the smaller tables inside the provenance block and sections 5.1.2, 5.1.7, 5.2.10, 5.3.6 and 5.4.5. The agent's own verbatim-line test (386 of 389 substantive lines of synth-04 found in the report) shows these rows are carried in the report text, so the shortfall is an enumeration-granularity gap and not a found omission; the rule of item 6.58 (6)(i) is mechanical, so it is recorded as a blocking finding and agent 2's partition is re-run (spawned: see (6)).

| ID | Severity | Blocking | Source finding | Source file(s) | Why it matters | Proposed handling | Originating reports |
|---|---|---|---|---|---|---|---|
| P6A-RC-1 | IMPORTANT (process) | Y at first pass; now N (CLOSED-BY-RERUN, see the rerun recount below) | Recount shortfall: agent 2 enumerated 145 distinct findings of `synthesis/synth-04-external-findings.md` against an independent recount of 182 (0.797) | `synthesis/synth-04-external-findings.md`; enumeration `qa/qa-anti-omission-enumeration-2.md` (lines 2939-3095) | The gate's proof of "nothing silently dropped" depends on an exhaustive enumeration; 37 table rows were not enumerated individually | CLOSED-BY-RERUN (rule: rerun report Complete and recount at least 0.9 of r for each chosen file of agent 2; met, see below) | recount by the consolidator; agent 2 report (`qa-anti-omission-report-2.md`) |

Rerun recount (same method, same three files, on `qa/qa-anti-omission-enumeration-2-rerun.md`; numbered entries counted with the same read-only `awk` over each section's line range, equal to the `COUNT` lines):

```
AGENT 2 FILE 21-value-ledger-brainstorms.md ENUMERATED=1685 RECOUNT=1685 (rerun)
AGENT 2 FILE 20-value-ledger-e2-study.md ENUMERATED=868 RECOUNT=868 (rerun)
AGENT 2 FILE synth-04-external-findings.md ENUMERATED=176 RECOUNT=182 (rerun; 0.967 of r, above the 0.9 line of 163.8)
```

Every one of the 13 assigned files has a `COUNT` line in the rerun enumeration (13 `COUNT` lines found), and the distinct `VL-21-` (1,685) and `VL-20-` (868) ids in the two ledger sections equal the ledgers' rows. The rerun report ends `Status: Complete` with a Summary and verdict PASS (0 blocking, 1 OMITTED minor row, 29 COVERED-BY-DEDUP, 0 JUSTIFIED-REMOVED); its header block still reads `**Status:** In Progress` (a stale line in the agent's own report that I may not edit; the final `Status: Complete` line, the Summary and the verdict are written, so I treat the report as Complete and note the stale header as a formatting defect, minor under the grading override).

## (1) Deduplicated table of every OMITTED finding

Reading rules. Blocking Y only where the originating agent graded the row blocking under `qa/grading-override.md` (no agent did; each of the four reports has 0 blocking omissions) or where my own checks found an invalid COVERED-BY-DEDUP claim or a JUSTIFIED-REMOVED entry without code evidence (none was found, see (6)(ii) and the dedup sampling). The only Blocking Y row is the recount finding `P6A-RC-1` (a process finding, graded by item 6.58 (6)(i), not by the override). The table carries every OMITTED row whose whole finding is absent from the report (agent 2: 16 rows, agent 3: 46 rows; agent 1 and agent 4 found none). The detail-level and sub-detail rows (agent 1: 10; agent 2: 65; agent 4: 5 notes; agent 3: 13 pair-check notes PC-1 to PC-13) are listed in section (5). No substance was found by two agents in two input files, so no row needed merging; the two agents' rows never overlap (checked by source file: agent 2 owns research 06-11 and web-03/04, agent 3 owns research 12-18, gaps and ledgers 22/23). The severity cell keeps the agent's label MINOR; every MINOR row carries `(minor under grading override)`. Proposed handling for every MINOR row: JUSTIFY as a detail that no decision rests on and put it on the owner's follow-up list; not fixed in the gate.

| ID | Severity | Blocking | Source finding | Source file(s) | Why it matters | Proposed handling | Originating reports |
|---|---|---|---|---|---|---|---|
| P6A-RC-1 | IMPORTANT (process, item 6.58 (6)(i)); now CLOSED-BY-RERUN | N (CLOSED-BY-RERUN, not counted in F_0 after the rerun) | Agent 2 enumerated 145 distinct findings of synth-04 against an independent recount of 182 (shortfall 20.3 percent) | `synthesis/synth-04-external-findings.md` | Enumeration is the proof of exhaustiveness; 37 table rows were not enumerated individually (carried verbatim in the report per agent 2's own line test) | CLOSED-BY-RERUN: agent 2's whole partition was re-run (`qa/qa-anti-omission-report-2-rerun.md`, `qa/qa-anti-omission-enumeration-2-rerun.md`); recount of the rerun enumeration: synth-04 176 of 182 (0.967), ledger 21 1,685 of 1,685, ledger 20 868 of 868, all 13 `COUNT` lines present; rerun verdict PASS, 0 blocking (details in (6)) | consolidator recount; report 2; rerun report |
| P6A-001 | MINOR (minor under grading override) | N | 06-5: HALTED reasons and the PASS / tier-mismatch rule | research/06-reflect-two-engines.md | detail only | follow-up list | report 2 |
| P6A-002 | MINOR (minor under grading override) | N | 06-13: verification_ran False / no-verification-stage is exempt even under --promote | research/06 | detail only | follow-up list | report 2 |
| P6A-003 | MINOR (minor under grading override) | N | 06-15: `reviewer-shortfall` token not in the halt set (2-of-3 stays PASS-eligible) | research/06 | detail only | follow-up list | report 2 |
| P6A-004 | MINOR (minor under grading override) | N | 06-20: probe variants (two same-vendor workers, one worker) | research/06 | detail only | follow-up list | report 2 |
| P6A-005 | MINOR (minor under grading override) | N | 06-47: engine B grounding chain (reuse-auditor use, reachability gate 5.6, required-capability pass 5.6a) absent from engine A | research/06 | detail only | follow-up list | report 2 |
| P6A-006 | MINOR (minor under grading override) | N | 06-64: additional deterministic logic in SKILL prose (Wave 7 gate, convergence routing, envelope validator, executor rotation, memory trim) as move-into-code candidates ("candidates only" in the source) | research/06 | detail only | follow-up list | report 2 |
| P6A-007 | MINOR (minor under grading override) | N | 07-20: E1-F19 troubleshoot report (three root causes, two prompt-only fixes) | research/07-e1-evidence-grading.md | detail only | follow-up list | report 2 |
| P6A-008 | MINOR (minor under grading override) | N | 07-22: stage 0a agreement 24/358 = 6.70 percent (rerun 6.33 percent) | research/07 | detail only; the conversion figures 67.28/63.38 are in the report | follow-up list | report 2 |
| P6A-009 | MINOR (minor under grading override) | N | 08-32: G9 surviving significant effects (second luna, ember+terra, 6 of 48 p<0.05) | research/08-e2-evidence-grading.md | exploratory; 48 tests are in the report | follow-up list | report 2 |
| P6A-010 | MINOR (minor under grading override) | N | 08-35: G12 single-run leaders are anecdotes | research/08 | detail only | follow-up list | report 2 |
| P6A-011 | MINOR (minor under grading override) | N | 09-24: radar signatures M1/M2/M4/M7 are Bash patterns (report 2 did not put the asterisk on this row; its cell says `none`, so it is one of the 16 wholly absent rows) | research/09-collaboration-designs.md | detail only | follow-up list | report 2 |
| P6A-012 | MINOR (minor under grading override) | N | 10-19: anti-overfitting rules AO-1 to AO-8 | research/10-process-redesign.md | detail only | follow-up list | report 2 |
| P6A-013 | MINOR (minor under grading override) | N | 10-33: C6 instances 8 of 12 are delivered docs | research/10 | detail only | follow-up list | report 2 |
| P6A-014 | MINOR (minor under grading override) | N | 11-3: wave 4 pre-check file, Will / Will Not lines | research/11-consumers-tasklist-workflow.md | detail only | follow-up list | report 2 |
| P6A-015 | MINOR (minor under grading override) | N | 11-9: stage 10.5 writes the index column and reflect_pre_summary | research/11 | detail only | follow-up list | report 2 |
| P6A-016 | MINOR (minor under grading override) | N | 11-13: outputs the panel must keep (index column, summary, directories); the key interface is kept at report line 667 | research/11 | detail only | follow-up list | report 2 |
| P6A-017 | MINOR (minor under grading override) | N | OM-1 (12.48): design.md unattended contract detail ("There is no gate", "Nested invocations. None." absent) | research/12-consumers-spec-review.md | detail only | follow-up list | report 3 |
| P6A-018 | MINOR (minor under grading override) | N | OM-2 (12.67): limitation that review-panel-live7.md numbers were not opened by R12 | research/12 | limitation note | follow-up list | report 3 |
| P6A-019 | MINOR (minor under grading override) | N | OM-3 (12.68): limitation: rf-qa.md lines 402 and 549 cap mentions and the 185-line spawn census were not re-read by R12 | research/12 | limitation note | follow-up list | report 3 |
| P6A-020 | MINOR (minor under grading override) | N | OM-4 (12.70): limitation that the tests were not run and test_f's rejection of a non-2 cap was read from source | research/12 | limitation note | follow-up list | report 3 |
| P6A-021 | MINOR (minor under grading override) | N | OM-5 (13.18): fsm.py defaults (DEFAULT_MONITOR 3, MIN_POLL_INTERVAL 30, timeouts 600/300, MAX_ROUNDS_ERROR string) absent; only the 2/5 round caps are carried | research/13-future-pr-review-and-rfqa.md | detail only | follow-up list | report 3 |
| P6A-022 | MINOR (minor under grading override) | N | OM-6 (13.19): gate_arm (ordinal>=1), gate_edit (>=2) and the evaluate_push_decision condition list absent | research/13 | detail only | follow-up list | report 3 |
| P6A-023 | MINOR (minor under grading override) | N | OM-7 (13.21): seed_troubleshoot, batch_by_file, plan_dispatch truncation absent | research/13 | detail only | follow-up list | report 3 |
| P6A-024 | MINOR (minor under grading override) | N | OM-8 (13.27): pr-submit SKILL Will Not Do list (no headless run, no upstream push, no force push, no .claude add) absent; the fork rule itself is carried elsewhere | research/13 | detail only | follow-up list | report 3 |
| P6A-025 | MINOR (minor under grading override) | N | OM-9 (13.34): auggie-review remediation chain (design, workflow, reflect pre, user-run implement, reflect post) absent | research/13 | detail only | follow-up list | report 3 |
| P6A-026 | MINOR (minor under grading override) | N | OM-10 (13.53): names of the 8 standard /task lenses absent (report says only "4 structural, 4 content") | research/13 | detail only | follow-up list | report 3 |
| P6A-027 | MINOR (minor under grading override) | N | OM-11 (13.101): gap: panel.py/ledger.py/cluster.py/verify_cmd.py/manifest.py bodies not read by R13 and findings_v2.py read to l.150 only absent | research/13 | limitation note | follow-up list | report 3 |
| P6A-028 | MINOR (minor under grading override) | N | OM-12 (14.07): two different definitions of "3 unresolved prior CRITICAL+MAJOR labels" (R25,R27,R28 vs R25,R34,R36) absent | research/14-e3-variants-and-experiments.md | detail only | follow-up list | report 3 |
| P6A-029 | MINOR (minor under grading override) | N | OM-13 (14.09): fixed-screen arithmetic (control mean 6, half 3, growth limit 44.457 from 0.7 x 63.51) absent | research/14 | detail only | follow-up list | report 3 |
| P6A-030 | MINOR (minor under grading override) | N | OM-14 (14.11): arm means 5.5 and 3.5 absent | research/14 | detail only | follow-up list | report 3 |
| P6A-031 | MINOR (minor under grading override) | N | OM-15 (14.13): comparator JSON copies under MEAS/diffgate/reviews/comparators not opened (limitation) | research/14 | limitation note | follow-up list | report 3 |
| P6A-032 | MINOR (minor under grading override) | N | OM-16 (14.14): control/treatment growth means 63.5% / 29.7% / 30.0% absent | research/14 | detail only | follow-up list | report 3 |
| P6A-033 | MINOR (minor under grading override) | N | OM-17 (14.24): diffgate per-review arrays 13/5/3 new findings and CM 7/2/2 absent | research/14 | detail only | follow-up list | report 3 |
| P6A-034 | MINOR (minor under grading override) | N | OM-18 (14.27): ponytail per-review arrays 16/15/0 and CM 9/7/0 absent | research/14 | detail only | follow-up list | report 3 |
| P6A-035 | MINOR (minor under grading override) | N | OM-19 (14.29): cost figures (ponytail audit 18 calls/18,713 tokens; loops 274 calls/239,628; diffgate 186 tools/207,181) absent | research/14 | detail only | follow-up list | report 3 |
| P6A-036 | MINOR (minor under grading override) | N | OM-20 (14.31): ponytail orphan reference R3-N1 absent | research/14 | detail only | follow-up list | report 3 |
| P6A-037 | MINOR (minor under grading override) | N | OM-21 (14.67): historical incident row 18/10/8 and 92,194 bytes not recomputable absent | research/14 | detail only | follow-up list | report 3 |
| P6A-038 | MINOR (minor under grading override) | N | OM-22 (14.69): FINAL-REPORT-QA independent PASS cannot be reproduced absent | research/14 | limitation note | follow-up list | report 3 |
| P6A-039 | MINOR (minor under grading override) | N | OM-23 (14.86): gap: comparator copies and raw control session transcripts not tried absent | research/14 | limitation note | follow-up list | report 3 |
| P6A-040 | MINOR (minor under grading override) | N | OM-24 (14.87): gap: Claude Code version not recorded (2.1.319 in ponytail metrics) absent | research/14 | limitation note | follow-up list | report 3 |
| P6A-041 | MINOR (minor under grading override) | N | OM-25 (15.28): E2 R-23 collab.json field list, R-24 +35% cap audit, R-30, R-46 absent | research/15-telemetry-manifest-run-record.md | detail only | follow-up list | report 3 |
| P6A-042 | MINOR (minor under grading override) | N | OM-26 (15.31): blind-label keys must stay out of the scoring directory absent | research/15 | detail only | follow-up list | report 3 |
| P6A-043 | MINOR (minor under grading override) | N | OM-27 (15.39): memory content is review output and belongs beside the run record by pointer, not inside it absent | research/15 | detail only | follow-up list | report 3 |
| P6A-044 | MINOR (minor under grading override) | N | OM-28 (16.52): E1 PLAN mtime 46 minutes after the E2 owner's "we are done testing" order absent | research/16-eval-governance.md | detail only | follow-up list | report 3 |
| P6A-045 | MINOR (minor under grading override) | N | OM-29 (17.08): corrections-to-earlier-rows table (DR-006, 007/061, 054, 058, 053, 080 pin cells; DR-090 merged into DR-017) absent | research/17-defect-register.md | detail only | follow-up list | report 3 |
| P6A-046 | MINOR (minor under grading override) | N | OM-30 (17.28): DR-053 note (test_review_cli.py:296-312 not read, not claimed as a pin) absent | research/17 | limitation note | follow-up list | report 3 |
| P6A-047 | MINOR (minor under grading override) | N | OM-31 (18.50): gap: docs searched for hooks/tests that enforce the rules (migration-skill.md, contributing-code.md, designs/spec-panel-review-loop.md) absent | research/18-repo-constraints-and-branching.md | limitation note | follow-up list | report 3 |
| P6A-048 | MINOR (minor under grading override) | N | OM-32 (18.58): doc claims that held (sync-discipline three gates, C1 pragmatic.md:224-229, C4/C5 pins) absent | research/18 | detail only | follow-up list | report 3 |
| P6A-049 | MINOR (minor under grading override) | N | OM-33 (L22.10): verification of R1/R2 hook sites (seal block, turns_of, R2 run-package.sh writes DONE even when INVALID) absent | research/22-value-ledger-collab-designs.md (non-row) | detail only | follow-up list | report 3 |
| P6A-050 | MINOR (minor under grading override) | N | OM-34 (L22.12): arithmetic re-derivations (0.30x116, C(12,4)=495, C(24,4)=10,626, Fisher p values) absent | research/22 (non-row) | detail only | follow-up list | report 3 |
| P6A-051 | MINOR (minor under grading override) | N | OM-35 (L22.27): Q8: can reflect Tier 2 reviewers be hooked at all or is resume the only collaboration path, absent as a question | research/22 (non-row) | open question not carried | follow-up list | report 3 |
| P6A-052 | MINOR (minor under grading override) | N | OM-36 (L23.13): re-validate 7: code-engine swarm dispatch MODULE-reflect, survival CORE, V-38 proposes DROP or MERGE absent | research/23-value-ledger-e1-e3-code.md (non-row) | detail only | follow-up list | report 3 |
| P6A-053 | MINOR (minor under grading override) | N | OM-37 (L23.18): G-3: _check_flat accepts an empty claim (no minimum length), no D-number absent | research/23 (non-row) | detail only | follow-up list | report 3 |
| P6A-054 | MINOR (minor under grading override) | N | OM-38 (L23.24): G-9: no executed baseline of tests/review; the 352-passed reflect result is a slice quotation absent | research/23 (non-row) | limitation note | follow-up list | report 3 |
| P6A-055 | MINOR (minor under grading override) | N | OM-39 (GQ-123): slice 05 cites merged-spec.md lines; merged-requirements.md has the same text at line + 6 absent | gaps-and-questions.md | detail only | follow-up list | report 3 |
| P6A-056 | MINOR (minor under grading override) | N | OM-40 (GQ-137): E2 requirements assume findings-v1 and the study launcher; HEAD also has findings-v2 for reflect, absent as a stated correction | gaps-and-questions.md | detail only | follow-up list | report 3 |
| P6A-057 | MINOR (minor under grading override) | N | OM-41 (GQ-262): counting rule for DROP duplicates (475 primary rows = 886 - 411 duplicate DROP) absent; the report states DROP totals and reasons | gaps-and-questions.md | detail only | follow-up list | report 3 |
| P6A-058 | MINOR (minor under grading override) | N | OM-42 (GQ-266): "2.75-3.25 more wrong blockers" is a three-comparator basis; BAD_CHECKS "A none, E none" not quoted absent | gaps-and-questions.md | detail only | follow-up list | report 3 |
| P6A-059 | MINOR (minor under grading override) | N | OM-43 (GQ-328): contract_setup subpackage has nine modules (evidence.py, questions.py, states.py also) absent; the report names the subpackage only | gaps-and-questions.md | detail only | follow-up list | report 3 |
| P6A-060 | MINOR (minor under grading override) | N | OM-44 (GQ-332): model swap visible only in fallback.log while final meta.json shows the fallback model absent | gaps-and-questions.md | detail only | follow-up list | report 3 |
| P6A-061 | MINOR (minor under grading override) | N | OM-45 (GQ-336): launch-level-guard requires a non-empty --repo operand absent | gaps-and-questions.md | detail only | follow-up list | report 3 |
| P6A-062 | MINOR (minor under grading override) | N | OM-46 (GQ-341): 8 packaged panel templates (2 spec, 6 reflect) plus the tier file correction absent | gaps-and-questions.md | detail only | follow-up list | report 3 |

Folded from the rerun of (6)(i) (one OMITTED row; the rerun's other rows are COVERED-BY-DEDUP and are not omissions, see (6)):

| ID | Severity | Blocking | Source finding | Source file(s) | Why it matters | Proposed handling | Originating reports |
|---|---|---|---|---|---|---|---|
| P6A-063 | MINOR (minor under grading override) | N | Pilot per-package by arm cells (any, judge-blocking, real blocking, ledger rows, wrong blockers for 3 packages x 3 arms) and the arm-key mapping of blind labels (designSpec A=Y B=X C=Z; alias A=Y B=Z C=X; design A=X B=Z C=Y) | research/08-e2-evidence-grading.md section 1 (rerun enumeration item 2) | the totals the cells sum to are in report 2.2 (any severity 2, 3, 4 of 16; real blocking 0 in every arm; wrong blockers 0, 1, 3), so no decision or number rests on the per-cell values; Appendix A carries only that the 9 cells match the pilot table (VL-20-041) and the arm-key role (VL-20-026, VL-20-640), which I confirmed | follow-up list | rerun of report 2 |

Cross-reading of the rerun against the first pass (no grade changed): the rerun found the substance of first-pass rows P6A-001 to P6A-003 (06-5, 06-13, 06-15: derive_verdict trigger slugs, HALTED reasons, `no-verification-stage` exemption, `reviewer-shortfall` token), P6A-007 (07-20), P6A-012 (10-19), P6A-014 to P6A-016 (11-3, 11-9, 11-13) in Appendix A rows (VL-23-463, 465, 467, 442, 727, VL-24-076, VL-21-1008, 1371, 1583, 1630, VL-24-349, 368, 370, 376). I read those rows in `synthesis/synth-08-value-inventory.md` and confirmed their headline substance: the BLOCKED and DEGRADED slug lists (VL-23-463, 465), the PASS / HALTED tier-mismatch rule (VL-23-467), the hard-coded contract values (VL-23-442), the 2-of-3 PASS-eligible decision (VL-23-727), the troubleshoot report's root causes (VL-24-076), AO-1 to AO-8 (VL-21-1008, 1371, 1583, 1630), the Stage 10.5 sign-off, `COMPLEXITY_SCORE` and `reflect_pre_summary` rows (VL-24-368, 370, 376) and the Wave 4 pre-check row (VL-24-349); the detail lines of those findings (for example the `Will / Will Not` lines of 11-3) were not individually confirmed. So those eight rows are recoverable by pointing to Appendix A; they stay on the follow-up list as minor.

## (5) Minor omissions as notes (all `(minor under grading override)`; never fixed, never rechecked)

Counts by report: report 1: 10 detail rows; report 2: 81 rows, of which 16 whole findings are in table (1) as P6A-001 to P6A-016 and 65 sub-detail rows are below; report 3: 46 rows (all in table (1) as P6A-017 to P6A-062) plus 13 pair-check notes PC-1 to PC-13 below; report 4: 5 notes below. Together with the table: 10 + 81 + 46 + 13 + 5 = 155 rows, every one with its originating report. The wording is each agent's, cut.

### Report 1 (10 detail rows; headline substance of each is in the report, per the agent)

1. `theory.py` HARD-set per-model figures (ember 0.25 to 0.22, luna 0.09, haiku 0.29 to 0.70, sonnet 0.46 to 0.74, grok 0.08 to 0.50, terra, wonder) and Spearman 0.64 (research/05; the conclusion is at report L1276).
2. Identifier-level details: `_embedded_calibration`, `--calibration` override order, `findings_block_compliance_rate`, `MAX_REF_TEXT = 200`, `F<index>` id replacement in `card_convert`, `_SECTION_REF`, `ROW_INPUT_KEYS`, `FROZEN_FIELDS`, `VERDICT_EXIT ... PENDING 12` (research/02 sections 4.3, 6, 7).
3. Per-file table of the 18 `T2bModel01` occurrences in 11 files (research/04 section 6; count, definition and reader are at L645, L883, L1011).
4. `19 RESULT.md` count under E2 `combos/`; line-shift entries of the stale-documentation lists (research/01, research/04).
5. `claude -p` background-work wait message, deleted-working-directory warning, extractor stripped-wildcard caveat (research/web-02).
6. C-06 replay populations behind conditions 2 and 4 (10 of 273 merges below the C-03 floor with bare `ok`, at least 7 of 264, 0 of 273 refusals with the cut, 36 of 39) (limits-repair-policy debate result).
7. X-13 quote-exactness figures: 31 of 313 quoted citations (9.9 percent), 18.8 percent for a two-quote row (process-redesign-modules debate result).
8. C-09 condition number "17 pins (16 byte-identity parameters plus the packaged-tier golden)" (panel-resolution-and-tier-source debate result).
9. Quantitative sub-scores of each debate and the debates' Return-contract and Artifacts lists (all 15 debate results).
10. Design-detail identifiers inside the debates' conditions (`first_pass_state`, `original_sha256`, `slot_order`, `reviewer_activity`, `CORE_PURE_FILES`, `finding_from_v2`, `fix_key`, `verification_status`, `LedgerError.reason`, `live_outcome_conflicts`, `duplicate_reviewer`, `no_valid_block`, `round_order`, `read_only`, `panel.py:371-373`, `manifest.py:371-372`) (five debate results).

### Report 2 (65 sub-detail rows; main substance of each entry is in the report; id = entry number in `qa-anti-omission-enumeration-2.md`)

- research/06 (15): 06-3 BLOCKED slugs other than contract-missing; 06-4 the 14 DEGRADED trigger slugs, halt set, exemptions, `promoting` effect; 06-11 engine A step-level data flow; 06-17 swarm docstring calls git-diff materialization a logged follow-up; 06-19 names of the 10 contract keys outside the frozen lists; 06-26 lint assertion map L0-L7 and rule B; 06-27 `_ev1` pass 2 "loud fallback", ev1_failures use_manifest; 06-36 task-builder emits the wrapper only with CLI_MODE; 06-42 config.py output default path, --output under .claude rejected, stub default ladder off; 06-48 deviation precedence Regression > Drift > Necessary > Authorized, grounding-gaps artifact; 06-49 rules D1-D5 of the shadow flag; 06-51 skill null-convergence handling, 0.60 floor; 06-56 invented keys zero_drop_flag, memory_status, notes, run_started, run_finished; 06-57 commit ids 9874d63fb and c2e3347d3; 06-58 exit docstring "trivially equal" parity.
- research/07 (5): 07-2 per-run token min 93,616 (A3) and max 367,381 (E3); 07-10 pilot cluster figures (71 clusters, 19 multi-reviewer, 45%); 07-15 689 findings with 0 per-finding calibration; 07-16 strata of the 50-pair check; 07-21 replay "49 skipped".
- research/08 (4): 08-13 three-way rows for sonnet+luna+ember and h2; 08-23 j1 sensitivity table S0-S4 rows; 08-36 audit span-null rows (46, 13 blocking); 08-41 per-audit grade table A-F.
- research/09 (15): 09-4 transport tally over 25 proposals and the rejection table for Orca mail, A2A, cross-session messaging (substance in Appendix A rows VL-21-054 to 057); 09-8 hook lock placement differences; 09-9 parallel-call race found by smoke runs; 09-11 parametrize marker counts; 09-12 r1 gate0 gate names; 09-13 r2 smoke elapsed pairs; 09-14 r3 baseline variance remark; 09-15 r4 "own gate says F7 should not run on 0/5 luna"; 09-16 r5 diagnostic chain sentence; 09-18 per-design requirement table; 09-28 three-implementation split of the exchange capability; 09-33 H4 "list per module"; 09-34 argv-diff test for the kill switch; 09-39 MR:396 and MR:909 kit statements; 09-42 MR line offset +6 note.
- research/10 (14): 10-2 verify-citations reads coverage only to pass to parse_block; 10-3 findings-v2 constants other than LENSES, CHANNELS, REFLECT_CATEGORIES; 10-7 two naming conventions; 10-10 wave 1B pass 2 INF-NNN quote pinning, 0.6 threshold; 10-18 class card block kinds; 10-21 recipe ledger row budgets and re-ask rules; 10-26 individual D1-D7 thresholds; 10-29 quote_other as a printed tool line; 10-31 per-item decidability rows for C1-C8, X1-X7, G0, D1-D7; 10-32 the doubtful C6/C5 instance and the #346 file list; 10-36 line-cite drift findings.py:15-22; 10-38 unit 9 table rows 15-19 individually; 10-40 0.914 x 0.914 = 0.835 product; 10-41 explicit M1-M10 to C1-C8 mapping.
- research/11 (9): 11-7 PatchChecklist, gate-results.txt names; 11-11 COMPLEXITY_SCORE terms, override, depth-map.yaml; 11-18 UC-1 partial cases; 11-19 D1-D5; 11-20 commands/reflect.md does not document the flag; 11-22 pool-exclusion detail; 11-23 25 fixtures, pass.yaml version; 11-24 per-trigger lines of the matrix; 11-32 troubleshoot refs and remediation-handoff readers.
- web-03 (2): web03-3 Hacker News source naming; web03-14 pr-submit force-push remark. web-04 (1): web04-22 SARIF kind / suppression tables partly visible.

### Report 3 pair-check notes (not omissions; the finding is carried and only a related row is a duplicate or a different kind; the agent's grading: no "one defect, two different destinations" case; all minor under override)

PC-1 `annotate` KeyError on a citation-only v2 finding (VL-23-035 and DR-113, both CORE; 8.1.2 lists the pair as "context only"); PC-2 `telemetry._ID_TOKEN` copy of `findings._REF_TOKEN` (VL-23-080, DR-007, both CORE); PC-3 code engine `contract_version "1.0"` (VL-23-437, DR-128, MODULE-reflect); PC-4 reviewers see only the tasklist body (VL-23-439, DR-131); PC-5 `merge_method` hard-coded by reviewer count (VL-23-442, VL-23-443, DR-129); PC-6 stale `cli/reflect/__init__.py` docstring (VL-23-458, DR-142); PC-7 runner comment on `--no-promote` default (VL-23-459, DR-144); PC-8 `reflection-rubric.md` old deviation classes (VL-23-496, 497, DR-136, 137); PC-9 HEAD-relative pins in `test_shadow_skill_contract.py` (VL-23-531, DR-141); PC-10 `--t2-engine` missing from command file and CLI (VL-23-577, 603, DR-145, 150); PC-11 dead API `channel_of`, `read_committed` (VL-23-067, 187, DR-120); PC-12 stage 2 shadow-exit result 8 of 13 against 3 of 39 (VL-23-505, 519 EVAL versus DR-138 MODULE-reflect; different kinds, named in 8.1.4 limit 3b in part); PC-13 untracked `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md` (VL-23-664, 788 KNOWLEDGE versus DR-154 HARNESS; different kinds, named in 8.1.4 limit 3b). Handling noted by the agent: mark the second row `DROP: duplicate of <ID>` in a later pass of synth-08.

### Report 3 detail-level partials (agent 3: not omissions, listed for completeness)

12.27 (V9 synthetic HIGH "fixed, non-overridable" wording), 13.07 (five PushDecision predicates), 13.11 (six-step order of `remap_severity`), 13.30 (auggie-only/claude-only/both source tag), 13.33 (never-approve rule of auggie-review), 13.35 (deep-mode cost figures), 14.78 (column-1 grammar as a fourth finding format), 15.45 (per-consumer derivation rows), L22.04 (MODULE-spec zero-row note).

### Report 4 minor notes (none is an omission)

1. The 8.1.0 reconciliation line calls 161 marked rows "pairs"; 8.1.1 gives 208 pairs; both stated, neither changes a destination; 153 register rows name a ledger id, so 162 and 208 are not reproducible from the register side alone.
2. "3,989 rows that are not DROP" (report line 4271) is 3,981 after the Gate 2 fix (5,950 minus 1,969); already logged as P6-090 in `qa/qa-consolidated-findings-phase6.md` (a duplicate of an earlier-gate minor finding).
3. Section 8.1 carries the 5,950 rows by reference (Appendix A is the same synth-08 file, 2,024,775 bytes) per the report's own carrying note; rows are identical to the ledgers; if a later reader wants the rows inline, that is an owner decision.
4. Forty CORE rows of ledgers 19 to 24 that mention the variant scripts or the grader (for example VL-24-292 to 298, VL-24-406, VL-24-489) are not in the eight-row exception table; the "Scope of the exceptions" paragraph says to read CORE in them as the contract, not the script or grader.
5. Register rows exist for 20 of the 22 X-n defects of ledger 24 (X-2 and X-6 have none); not a report omission.

### Consolidator notes

- Report 2 says "16 of the 81 are wholly absent" and "rows marked * are wholly absent"; the table carries 15 asterisks and 81 rows, and the sixteenth wholly absent row (09-24, cell `none`) has no asterisk. All 16 are in table (1). Counts and conclusion unaffected.

## (6)(ii) JUSTIFIED-REMOVED check and COVERED-BY-DEDUP sampling

### JUSTIFIED-REMOVED check

All four agents classified 0 findings JUSTIFIED-REMOVED (reports 1, 2, 3 and 4, Summary sections). The "at least 10" sampling rule applies only when there are more than 10 such entries, so there is nothing to sample; I opened the earlier-gate logs myself to confirm that no removal exists that an agent could have missed:

| Gate and file read | Content (read in full, 39 or 1 lines) | Removal of a claim as false or unsupported? |
|---|---|---|
| Gate 3 cycle 1, `qa/qa-fix-log.md` (39 lines) | Two fixes, P6-001 and P6-002, both additions (precedence paragraph and delta table in Section 3, pointers in Sections 4 and 7.0.1, a table and paragraph in 8.1.2, a prefixed note on 8.1.4 limit 1); line 4 states the report grew from 5,057 to 5,098 lines and no id, count or table was renumbered; line 35 records only that a "30 CORE rows" figure of the finding was not used because it could not be reproduced (a figure not written into the report, not a removal from it); minor findings P6-003 to P6-110 untouched | no |
| Gate 3 cycle 2, `qa/qa-fix-log-c2.md` (1 line) | `Skipped: Gate 3 passed at review 2` | no |
| Gate 4 cycle 1, `qa/qa-fidelity-fix-log-c1.md` (1 line) | `No fix required: zero blocking findings at review 1` | no |
| Gate 4 cycle 2, `qa/qa-fidelity-fix-log-c2.md` (1 line) | `Skipped: Gate 4 passed at review 2` | no |
| Gate 4 consolidated findings (agent 4's two cited entries), `qa/qa-fidelity-consolidated-findings.md` lines 152 and 157 | P6F-008 and P6F-013 are minor figure corrections ("12 of 13", "12 of 15") not applied, not removals | no |

Table of JUSTIFIED-REMOVED entries (Source finding, Gate and fix-log entry, code evidence): none. Zero entries, so no entry lacks code evidence and no omission row is created from this check. This agrees with the item's premise that the earlier-gate fix logs record no removal.

### COVERED-BY-DEDUP sampling (at least 10 required; 16 claims checked)

Method: for each sampled claim I read the claimed row and the kept row in `synthesis/synth-08-value-inventory.md` (Appendix A, the file Section 8.1.2 names) with a read-only `grep -m1` and `awk` over the destination and reason cells, and checked that the dedup row says `DROP[duplicate]: duplicate of <kept id>`, that the kept row exists, and that the kept row carries the same substance. The sample spans agents 2, 3 and 4 (agent 1 claimed none).

| # | Claimed COVERED-BY-DEDUP row (Appendix A line) | Kept row (Appendix A line, destination) | Result |
|---|---|---|---|
| 1 | VL-21-131 (L4879, DROP, was MODULE-tasklist: same seal rule) | VL-22-017 (L407, CORE) | valid: same seal rule, kept row is the evidence-snapshot design |
| 2 | VL-20-025 (L4568, DROP: same category-label defect fixed in the harness) | DR-028 (L5982, DROP obsolete "fixed in the harness") | valid with a note: kept row is itself DROP, which carries the same substance (fixed defect); the per-module category concern is carried by DR-080 CORE per the row |
| 3 | VL-20-407 (L4619, DROP: [CODE-CONTRADICTED] "no error") | DR-087 (L6002, DROP obsolete "wording correction; the real defect is DR-002") | valid with the same note; DR-002 (CORE) carries the real defect |
| 4 | VL-20-643 (L4756, DROP, was HARNESS) | DR-091 (L3162, EVAL, REPRODUCED) | valid |
| 5 | VL-20-767 (L4807, DROP, was EVAL) | DR-092 (L3163, EVAL, REPRODUCED for audit D only) | valid |
| 6 | VL-22-167 (L5475, DROP, was HARNESS: missing `lib/`) | DR-155 (L3641, HARNESS, REPRODUCED) | valid |
| 7 | VL-22-583 (L5576, DROP, was EVAL: judge skip rule) | VL-20-299 (L3298, HARNESS) | valid |
| 8 | VL-23-007 (L5707, DROP, was KNOWLEDGE: dangling registration) | DR-042 (L956, CORE, REPRODUCED by Glob) | valid |
| 9 | VL-23-576 (L5784, DROP, was MODULE-reflect: eight packaged panel templates) | VL-24-519 (L918, CORE) | valid (the row says the dormant-reflect-template detail stays with VL-23-180) |
| 10 | VL-23-697 (L5847, DROP, was KNOWLEDGE: stale memo) | DR-153 (L6021, DROP obsolete "stale lesson") | valid with a note: kept row is DROP and carries the stale-lesson substance (agent 3 disclosed this) |
| 11 | VL-23-468 (L5778, DROP, was MODULE-reflect: two thresholds for one score) | DR-133 (L994, CORE, TRACED) | valid |
| 12 | VL-24-153 (L5899, DROP, was HARNESS: exit-aggregate defect) | DR-156 (L1277, MODULE-reflect, REPRODUCED by reading) | valid |
| 13 | VL-24-159 (L5900, DROP, was HARNESS: replay script) | DR-160 (L1278, MODULE-reflect, TRACED) | valid |
| 14 | VL-24-299 (L5912, DROP: duplicate of VL-24-231, installed-only consequence) | VL-24-231 (L826, CORE) | valid |
| 15 | VL-24-459 (L5921, DROP: duplicate of VL-24-347, plugin mirror state) | VL-24-347 (L877, CORE) | valid |
| 16 | web-04 entry 23 "Key finding 1-7 restating 1.x to 5.x" (enumeration-2 line 2929) | entries 1-16 of the same enumeration (lines 2907-2922), each REPRESENTED at report lines 1919-2005 | valid: the restated entries are individually represented |

Result: 16 of 16 claims are valid; no invalid dedup claim, so no omission row is created. Rows 2, 3 and 10 point to a kept row that is itself `DROP[obsolete]`; the destination of both rows is DROP and the substance (a fixed, retracted or stale item) is recorded in the kept row's reason, so no destination, decision or number is wrong; all three were disclosed by the originating agents.

## (3) Item Status table (report Sections 1-10, after review 1)

No agent found a blocking omission in any section, my own sampling found no invalid COVERED-BY-DEDUP claim and no JUSTIFIED-REMOVED entry without code evidence, and the one recount finding (P6A-RC-1) is a process finding about an input file, not an omission in a report section, and is CLOSED-BY-RERUN. The minor omissions of table (1) and section (5) are on the follow-up list and do not change a section status.

| Report section | Status after review 1 | Blocking omissions |
|---|---|---|
| 1 Problem Statement | PASS | 0 |
| 2 Current State Analysis | PASS | 0 |
| 3 Target State | PASS | 0 |
| 4 Gap Analysis | PASS | 0 |
| 5 External Research Findings | PASS | 0 |
| 6 Options Analysis (with the 6.12 conflict log) | PASS | 0 |
| 7 Recommendation (with 7.0.1 and 7.3 invariants) | PASS | 0 |
| 8 Implementation Plan and Value Inventory (8.1, Appendix A) | PASS | 0 |
| 9 Open Questions | PASS | 0 |
| 10 Evidence Trail | PASS | 0 |

## (4) F_0

Written after the rerun of (6)(i): blocking omissions in table (1): 0; recount findings `P6A-RC-<n>` not CLOSED-BY-RERUN: 0 (`P6A-RC-1` is CLOSED-BY-RERUN and is not counted); invalid COVERED-BY-DEDUP claims found: 0; JUSTIFIED-REMOVED entries without code evidence: 0.

**F_0 = 0**

## (6) Verdict and the two checks

### (6)(i) Independent recount: summary

First pass: 11 recount lines, 10 pass, 1 fails (`AGENT 2 FILE synth-04-external-findings.md ENUMERATED=145 RECOUNT=182`, 0.797). The failing line became blocking finding `P6A-RC-1` (Blocking Y, counted in F_0 while open). Rerun: one Agent (subagent_type `rf-analyst`, name `ao3-rerun-2`) was spawned with the AGENT PROMPT text of item 6.55 (task-file line 577) copied word for word, with exactly the two path substitutions (`qa-anti-omission-report-2.md` became `qa-anti-omission-report-2-rerun.md` and `qa-anti-omission-enumeration-2.md` became `qa-anti-omission-enumeration-2-rerun.md`, in the ENUMERATION FILE clause and in the `Output path`), the final assigned-file list of `qa/gate5-partition.md` for agent 2 (research 06-11, web-03, web-04, synth-04, synth-09, synth-10 and the moved ledgers 21 and 20, with the ledger-row enumeration and `grep -c '^| VL-NN-'` recount rule that travels with a moved ledger), the grading-override paragraph (first read `qa/grading-override.md`; BLOCKING only under conditions 1 to 3; otherwise MINOR with `(minor under grading override)`), and the appended sentence "INDEPENDENCE OF THE RE-RUN: ..." at the end. The rerun produced `qa/qa-anti-omission-report-2-rerun.md` (80 lines, ends `Status: Complete`, verdict PASS, 3,463 findings enumerated, 1 minor OMITTED row folded into table (1) as P6A-063, 29 COVERED-BY-DEDUP, 0 JUSTIFIED-REMOVED, 0 blocking) and `qa/qa-anti-omission-enumeration-2-rerun.md` (13 `COUNT` lines). The recount of the rerun enumeration (same method, the same three files) is written in (2c) under `P6A-RC-1`: ledger 21 1,685 of 1,685, ledger 20 868 of 868, synth-04 176 of 182 (0.967, at least 0.9). The row is therefore `CLOSED-BY-RERUN` (Blocking N, listed with its rerun result, not counted in F_0 after the rerun).

Checks on the rerun's own dedup claims (made because its rows 2 to 7 reclassify first-pass OMITTED rows as COVERED-BY-DEDUP): I read the Appendix A rows it names (VL-23-463, 465, 467, 442, 727, VL-24-076, VL-21-1008, 1371, 1583, 1630, VL-24-349, 368, 370, 376, DR-080, DR-002, DR-086, VL-20-471) in `synthesis/synth-08-value-inventory.md`; all exist and carry the headline substance claimed (see the cross-reading paragraph under table (1)); no invalid dedup claim.

### (6)(ii) JUSTIFIED-REMOVED check and COVERED-BY-DEDUP sampling

Result (details in the section "(6)(ii)" above): the Gate 3 and Gate 4 fix logs record no removal (Gate 3 cycle 1 added text only; the other three logs are one line each, `Skipped` or `No fix required`), so the JUSTIFIED-REMOVED table has zero entries and no omission row arises from it; 16 COVERED-BY-DEDUP claims were sampled (agents 2, 3, 4; agent 1 claimed none) and all 16 are valid, plus the 8 rerun dedup claims named above, so no invalid dedup claim became an omission.

### Other checks required by the item

| Check | Result |
|---|---|
| All four reports read; none missing or `In Progress` | yes, all four are `Status: Complete` (see "Reading check") |
| Enumeration totals quoted from the reports | yes, section (2a); arithmetic re-checked (sums equal the stated totals) |
| Enumeration files exist with a `COUNT` line for every assigned file | yes: 26 + 13 + 13 (+ the `NONROW-COUNT`) + 2 `COUNT` lines found by Grep; rerun file 13 of 13 |
| Nothing invented | every figure above is quoted from a report or measured by a read-only command named in the section; the shortfall and its closure rest on counts I made |
| Reports, enumeration files, research report and inputs modified by me | no (I wrote only this file; the only Agent I spawned wrote only the two rerun files) |

### Verdict

F_0 = 0 (no blocking omission, no open recount finding, no invalid dedup claim, no JUSTIFIED-REMOVED entry without code evidence).

**Verdict: PASS (Gate 5, review 1: F_0 = 0).** 155 first-pass minor rows plus 1 rerun minor row (P6A-063) go to the owner's follow-up list, all `(minor under grading override)`.

Status: Complete


