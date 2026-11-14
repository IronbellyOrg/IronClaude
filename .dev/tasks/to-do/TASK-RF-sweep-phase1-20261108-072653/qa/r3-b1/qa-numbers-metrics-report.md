# QA Report: R3-B1 numbers lens (doc-qualitative, DESIGN `docs/designs/orchestrator-mode.md`)

**Topic:** R3-B1 design fix (window rule reads fields the model lacks), items 2.1 to 2.6
**Date:** 2026-11-08
**Phase:** doc-qualitative, numbers lens (recount every countable claim)
**Fix cycle:** 1 (first review of this gate)
**fix_authorization:** false (only this report was written)
**Inherited Structural Verdict:** none in the spawn prompt, so standalone behaviour applies.
**Axis lens status:** not a task-qualitative phase; no Axis column.

Inputs read (all in chunks of at most 150 lines): DESIGN lines 1-1023 (whole file, 1023 lines per `wc -l`); research/04 lines 75-140 and 216-232; research/09 lines 139-225 (Gap 4 and Gap 5); `r3-b1-mechanical.md` lines 1-126; task item 2.7 text (task file lines 287-289); SPEC lines 103-104 and the GAPS row-count line; `tests/skills/test_worker_contract.py` and `src/superclaude/core/WORKER-CONTRACT.md` for the section 8 counts and anchors.

## Counts the task named, recounted

| Claim in DESIGN | Where | What the text lists | Recount | Match |
|---|---|---|---|---|
| 6 fixtures, `test_probes_allowlist.py` row | 740 (and 766 "the six reader and parser fixtures") | `..._sets_first_and_last_record_ts`, `..._first_record_ts_is_minimum`, `..._first_record_ts_over_256k`, `..._dispatch_times_sqlite_form`, `..._dispatch_times_iso_z_form`, `..._dispatch_times_missing_or_bad` | 6 | yes |
| 4 fixtures, `test_classify.py` row | 741 | `test_path_b_window_open_row_joins`, `..._inclusive_bounds`, `..._terminal_row_without_end_has_no_window`, `..._row_without_start_has_no_window` | 4 | yes |
| `Total: 9 deviations.` | 819 | rows D1 to D9 in the table at 807-817 (`grep -c '^| D[0-9]* |'` = 9) | 9 | yes |
| `Total: 23 open items.` | 995 | rows 1 to 23 at 971-993 (awk range count = 23) | 23 | yes |
| 256 KiB transcript tail | 317, 398, 457, 511, 544 (`256 * 1024`), 740 (3 mentions), 989, 1015 | every hit says 256 KiB; the hit at 739 is `SHA-256`, not the tail | consistent | yes |
| em-dash count 0 | whole file | `grep -c '—'` = 0; `grep -c '–'` (en-dash) = 0 | 0 | yes |
| Mechanical section-by-field matrix | r3-b1-mechanical.md 105-113 | re-run with `sed -n 'a,bp' | grep -c` per range and per name (49 cells) | all 49 cells equal the report | yes |
| Design length | mechanical line 3 "(1023 lines)" | `wc -l` = 1023 | 1023 | yes |

## Checks

| Check | What was recounted or verified | Result |
|---|---|---|
| C1 | 6 named fixtures in the `test_probes_allowlist.py` row (line 740), and the same "six" in the FR-010 traceability row (766) | PASS |
| C2 | 4 named fixtures in the `test_classify.py` row (line 741) | PASS |
| C3 | `Total: 9 deviations.` against the D1 to D9 rows (807-817), and against the "Not counted" bullets (3, none of them a D row) | PASS |
| C4 | `Total: 23 open items.` against rows 1 to 23 (971-993); item 23 was reworded, not added | PASS |
| C5 | 256 KiB tail limit identical in 7.1 (398), 7.2 (457, 511), 7.3 constant (544), section 6 diagram (317), section 11 (740), item 19 (989), cycle 2 row (1015) | PASS |
| C6 | em-dash count 0 (and en-dash 0) | PASS |
| C7 | mechanical matrix: all 49 cells recounted; per-section rule of task item 2.7 (7.2, 2.2, 18 hold all four model names; 7.1 holds `first_record_ts`; 11 holds all four; 15.1 and 17 hold the three source names) is met | PASS |
| C8 | mechanical report checks 1 to 7 each reproduce (`first_record_ts`/`dispatch_*` hits at 60, 398, 455, 457, 496, 740, 741, 1023; no `TODO`/`TBD`; one `Total:` hit each) | PASS |
| C9 | R3-B1 fixture values copied from research/04 2.3 (timestamps 07:00:01Z, 07:00:05Z, 07:00:09Z; 07:00:00Z and 08:00:00Z; `2026-11-08 07:00:00`; `.123Z`; 10:00, 10:05, 12:00; 10:00:00.700, 11:00:00.400, 11:00:01.000; 10:30) | PASS |
| C10 | Inclusive-window arithmetic: 10:00:00.700 cuts to 10:00:00 (in); 11:00:00.400 cuts to 11:00:00 (in); 11:00:01.000 cuts to 11:00:01 (out); "first two join, third does not" is correct | PASS |
| C11 | Counts of model fields: "all three are None" (455) = `dispatch_started`, `dispatch_ended`, `dispatch_status`; "the three fields" (496) the same three; 15.1 item 4 and item 23 name 3 source fields | PASS |
| C12 | Other DESIGN counts: 8 templates and 7 verbs (7.3 lines 523-532, 550, 181, 196, 875, 796); 9 rules (472-484); 12 `SECTIONS` functions (634); 7 new files under `tests/sweep/` (conftest plus 6 test files); 4 join-incomplete cases (499, 766); 4 SPEC assertions in `test_readonly`; 13 capture items; 3 `Pre` steps; 26 FR rows and 15 NFR rows in section 12; R1 to R8 (8 rows in 9); M1 to M10; SP-19 to SP-29; 50-call cap with 60 rows giving `bound_reached == 10` and 2 Runs of 40 giving 25 each; 512 KiB + 512 KiB = 1 MiB; SPEC 653 lines; GAPS 113 rows = 88 open + 25 resolved; 3 blocking findings R3-B1 to R3-B3 | PASS |
| C13 | SPEC-derived counts in the `test_classify.py` row: four FR-008 inputs, two FR-009 cases, five FR-010 exemptions (SPEC lines 102-104) | PASS |
| C14 | "giving 9 entries" for `NEVER_AS_WORKER` (section 8): the tuple at `test_worker_contract.py:382-391` has 8 entries today, plus `/sc:sweep` is 9. The contract line 23 names 7 commands today plus the conditional `pr-submit`; the new line names 8 plus the conditional `pr-submit` | PASS |
| C15 | Section 11 intro: "Seven new files under `tests/sweep/`, one new command test, and edits to four existing test files" | FAIL (F1) |
| C16 | R3-B1 edited text uses no DESIGN self-line numbers (the fixture says "per the unknown row schema rule", 7.2 says "the 'Unknown row schema' bullet below"), so the R3-B1 edits cannot go stale by a line shift | PASS |
| C17 | Line anchors to files outside DESIGN in section 8 (`test_worker_contract.py`, `WORKER-CONTRACT.md`) against the files on disk | FAIL (m1, MINOR) |
| C18 | Python 3.10 claim for the `Z` suffix (`datetime.fromisoformat` accepts `Z` only from 3.11) against the project floor `>=3.10` (project CLAUDE.md) | PASS |

## Findings

### F1 (MAJOR): "edits to four existing test files" lists only three edited files

- Evidence: `docs/designs/orchestrator-mode.md:728` says "Seven new files under `tests/sweep/` ..., one new command test, and edits to four existing test files." The existing files the section names are at lines 746-747: `tests/skills/test_worker_contract.py` (edit), `tests/core/test_how_we_work_routing_table.py` (edit), `tests/recommend/test_routing_refresh.py` (edit) and `tests/commands/test_routing_plugin_parity.py` ("unchanged, must pass"). Section 8 (line 677) and section 9 rows R4 and R5 (lines 699-700) confirm the same three edits. `tests/sweep/test_readonly.py` is one of the seven new files (created at step 1.4a), so it cannot be the fourth.
- Wrong: three existing test files are edited, not four. A task builder that plans one task per counted file will look for a fourth edit that does not exist, or will edit the parity test that the design says stays unchanged.
- Scope: not introduced by the R3-B1 edits (items 2.1 to 2.6 did not touch line 728); it is a count in DESIGN that does not match what the text lists, which the numbers lens asks to report.
- Smallest fix: at line 728 change "edits to four existing test files" to "edits to three existing test files (`tests/commands/test_routing_plugin_parity.py` must also still pass, unchanged)".

### m1 (MINOR): section 8 line anchors into other files no longer match the files on disk

- Evidence: DESIGN 665 puts WC-14 "after the fan-in rule paragraph (line 156) and before `### Worked example: gate hit, answer, new Task` (line 158)", and 679 says "WC-13 is at line 155". On disk `WORKER-CONTRACT.md` has WC-13 at line 62 and the `### Worked example` heading at line 275. DESIGN 680-682 and 688 cite `test_worker_contract.py` lines 245-254 (`NEVER_AS_WORKER`), 624 (parametrized removal test), 545 (the rename target), 865 (the `"load"` assertion), 470 (the equality check) and 398 (`_check_never_as_worker`). On disk they are at 382, 1081, 912, 1322, 837 and 765. Line 25 (`RULE_PHRASES`) and `WORKER-CONTRACT.md` line 23 still match.
- Effect: the quoted heading and symbol names are right, so an implementer can still anchor by text. This is a moved line number on a true claim, so it does not fail the gate. It sits next to the line 1019 phrase "re-anchor to master `5dc29d23`", which therefore overstates what was re-anchored.
- Smallest fix: re-read the two files and update the numbers, or drop the numbers and keep the quoted anchors.

### m2 (MINOR): two path-B fixtures drop the pane and tab-map setup that research/04 gives

- Evidence: research/04:114 gives `test_path_b_window_open_row_joins` with "`session_join` pane P; tab-map entry P to session S" and 04:110 says "path B assumed". DESIGN 741 gives the same fixture without the `session_join` value or the tab-map entry, and `test_path_b_window_inclusive_bounds` (04:115) also drops it. The names and the heading "R3-B1 path-B window fixtures" carry the path, and section 7.2 defines path B, so a builder can infer the setup.
- Smallest fix: add "`session_join` pane P and a tab-map entry from P to session S" to the Given of those two fixtures.

### Notes (no action needed)

- n1: "nine boundary fixtures" (740, 776) is 3 limits times 3 values only because `CONTRACT_LIMIT = LEDGER_LIMIT` is one 1 MiB constant (line 542); a reader who counts contract and ledger as two limits gets 12. The count is right; the wording could say "three limits".
- n2: research/04:221 literally says to grep the four model names in 15.1 and 17; those sections hold only the Orca source names (as research/04 edits 7 and 8 prescribe). The per-section rule in task item 2.7 states this reading, and the mechanical report applies it. The DESIGN follows the edits, so this is a gate-wording gap, not a DESIGN defect.
- n3: Section 1 lines 7-11 still describe R3-B1 as open and say the rule reads "three time fields"; the model now holds four (`dispatch_status` was added). That is correct history until the R3-B1 gate closes; update it when it does. Section 18 now holds a "Fix cycle 3" although line 7 states a cap of 2 fix cycles; line 7 explains this with the coordinator approval, so the counts are consistent.
- n4: Not recounted in this review: line numbers into the SPEC, REPORT, `HOW-WE-WORK.md`, `.gitignore` and `main.py` (sections 7.6, 9, 10, 15.2). Only the anchors in m1 were checked against disk.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. The spawn prompt carried no `## Inherited Structural Verdict`; I re-counted from the DESIGN text itself. The mechanical report `r3-b1-mechanical.md` was treated as a claim to reproduce, not as evidence.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Matrix recount: re-ran 49 per-range, per-name line counts with `sed -n 'a,bp' | grep -c` and compared each cell with `r3-b1-mechanical.md` 105-113 (C7).
- Row counts from the tables themselves, not from the `Total:` lines: `grep -c '^| D[0-9]* |'` = 9 and an awk range count of open-item rows = 23 (C3, C4); FR rows 26 and NFR rows 15 (C12).
- Count of edited test files: grep of every `tests/...py` path in DESIGN, then reading lines 746-747, 699-700 and 677 (F1).
- External-file checks: `NEVER_AS_WORKER` tuple read at `test_worker_contract.py:380-391` (8 entries, C14); `WORKER-CONTRACT.md` and the test file grepped for the anchors behind m1; SPEC lines 102-104 read for the four, two and five counts (C13).
- Date arithmetic of the inclusive window checked by hand against the 7.2 rule (C10).

Confidence: Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 19 | Grep: 9 | Glob: 0 | Bash: 4 (Read + Grep + Glob = 28 is at least the 18 checks). No web research was performed, so no Tavily or fallback use to record.

## Verdict

R3-B1 numbers all hold: 6 fixtures, 4 fixtures, 9 deviations, 23 open items, the 256 KiB tail limit in every place, and em-dash count 0. One pre-existing count in section 11 (F1) does not match the files the section lists, and by the severity rule a false count claim is blocking.

Verdict: FAIL
Blocking count: 1
