# Anti-Omission Report 4 (Gate 5, agent 4)

## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md` (5,098 lines)
**Input files checked:** `research/24-value-ledger-evidence-consumers.md` (671 lines, 589 rows) and `synthesis/synth-08-value-inventory.md` (6,127 lines, 5,950 rows). Ledgers 19 to 23 were reassigned to agents 1, 2 and 3 by `qa/gate5-partition.md`. Total findings enumerated: 933 (589 + 344). Enumeration file: `qa/qa-anti-omission-enumeration-4.md`.
**Date:** 2026-11-14
Status: Complete

Grading: `qa/grading-override.md` read first and applied (blocking only for a wrong or unsupported decision, destination, conflict outcome or recommendation number; a missing required deliverable or section; or a security, data-loss or safety-boundary risk).

## Method

1. Created the enumeration file first, then enumerated ledger 24 row by row (589 entries) and synth-08 by prose item, by destination group, by ledger-by-destination row group and by every defect-register row (344 entries).
2. Recounts, all read-only: `grep -c '^| VL-24-'` on ledger 24 = 589; `grep -c '^| VL-'` on synth-08 = 5,779; `grep -c '^| DR-'` on synth-08 = 171; sum 5,950 (the report's 8.1.0 total). File size 2,024,775 bytes and 6,127 lines (the report's 8.1.2 and Appendix A figures).
3. Row-substance test for ledger 24 (not an ID test): an awk join of every ledger-24 row against its synth-08 row compared Statement, Kind and Destination. Result: 589 of 589 found, 0 Statement differences, 0 Kind differences, 5 destination changes (VL-24-153, 159, 167, 172 to `DROP: duplicate of` a re-verified DR row; VL-24-181 CORE to MODULE-reflect), each with its reason written in the row. The 8.1.3 table P3-012 and the P3-014 count "ledger 24: 1 moved" agree with those five changes.
4. Section 8.1 of the report was compared with synth-08 by line-by-line `diff`: 8.1.0 and 8.1.1 (report 4246 to 4273 against file 10 to 37) are identical; 8.1.3 and 8.1.4 (report 4316 to 4405 against file 6035 to 6127) are identical except the labelled report note inserted into limit 1; the verification paragraph (file line 6126) is carried at report line 4407. The 8.1.2 group table (heading lines 45, 997, 1279, 1623, 1696, 1745, 1802, 3171, 3642, 4062; ranges; row counts 948, 278, 340, 69, 45, 53, 1,365, 467, 416, 1,969) matches the file.
5. Recomputed the 8.1.0 table with awk by heading range: every one of the 7 source rows by 10 destinations equals the printed table; 0 rows sit under a heading different from their Destination column. DROP reasons recounted: duplicate 1,753, obsolete 126, out of scope or evidence-free 86, CODE-CONTRADICTED 4 (= 1,969); 27 non-DROP rows carry `CODE-CONTRADICTED`; 118 ledger rows and 43 register rows are `DROP[duplicate]` against the other side of a pair (161); the three cross-ledger duplicates (VL-21-131 of VL-22-017, VL-23-576 of VL-24-519, VL-22-583 of VL-20-299) are present.
6. Post-Gate-3 table in 8.1.2 (eight rows plus two context rows): every cited Appendix A line is right (VL-24-214 at 820, VL-24-218 at 822, VL-24-268 at 852, VL-24-269 at 853, VL-24-295 at 867, VL-24-525 at 921, VL-24-259 at 845, VL-24-278 at 860, VL-23-035 at 526, DR-113 at 982), each sits in the CORE group, and the keyword scan figure of 48 rows reproduces. The Section 7 anchors it cites exist (C-02 row, axis 10 "Port contracts, not scripts", F-4).
7. Earlier-gate removals: the Gate 3 and Gate 4 fix logs and consolidated findings were searched for synth-08, 8.1, Appendix A and ledger 24. The Gate 3 fix log only adds text to 8.1.2 and 8.1.4 (no removal). The Gate 4 entries touching ledger 24 rows (P6F-008 on VL-24-073, P6F-013 on VL-24-161) are minor figure corrections in the source rows and removed nothing from the report. No finding was classified JUSTIFIED-REMOVED because none was needed.

## Pair check (ledger 24 against the defect register)

The defect register rows that cite slice 11 or 12 are 20 (DR-140, 148, 153, 154, 156 to 171 except 155). Every one has exactly one kept row and one single destination in synth-08:

| Pair | Ledger-24 row [dest] | DR row [dest] | Kept row |
|---|---|---|---|
| X-1 | VL-24-153 [DROP, was HARNESS] | DR-156 [MODULE-reflect, REPRODUCED] | DR-156 |
| X-3 | VL-24-155 [CORE] | DR-157 [DROP, UNVERIFIED] | VL-24-155 |
| X-4 | VL-24-156 [CORE] | DR-158 [DROP] | VL-24-156 |
| X-5 | VL-24-157 [CORE] | DR-159 [DROP] | VL-24-157 |
| X-7 | VL-24-159 [DROP, was HARNESS] | DR-160 [MODULE-reflect, TRACED] | DR-160 |
| X-8 | VL-24-160 [CORE] | DR-161 [DROP] | VL-24-160 |
| X-9 | VL-24-161 [CORE] | DR-162 [DROP] | VL-24-161 |
| X-10 | VL-24-162 [HARNESS] | DR-163 [DROP] | VL-24-162 |
| X-11 | VL-24-163 [HARNESS] | DR-164 [DROP] | VL-24-163 |
| X-12 | VL-24-164 [CORE] | DR-165 [DROP] | VL-24-164 |
| X-13 | VL-24-165 [CORE] | DR-166 [DROP] | VL-24-165 |
| X-14 | VL-24-166 [DROP] | DR-167 [DROP, mutation] | both DROP, one destination |
| X-15 | VL-24-167 [DROP, was MODULE-reflect] | DR-154 [HARNESS, REPRODUCED] | DR-154 |
| X-16 | VL-24-168 [DROP, CODE-CONTRADICTED] | DR-153 [DROP, obsolete] | both DROP, one destination |
| X-17 | VL-24-169 [CORE] | DR-168 [DROP] | VL-24-169 |
| X-18 | VL-24-170 [MODULE-reflect] | DR-148 [DROP] | VL-24-170 |
| X-19 | VL-24-171 [HARNESS] | DR-169 [DROP] | VL-24-171 |
| X-20 | VL-24-172 [DROP, was HARNESS] | DR-140 [MODULE-reflect, REPRODUCED] | DR-140 |
| X-21 | VL-24-173 [HARNESS] | DR-170 [DROP] | VL-24-173 |
| X-22 | VL-24-174 [DROP, already DROP] | DR-171 [CORE, UNVERIFIED] | DR-171 (the ledger row was already DROP, so the rule "a ledger row already DROP stays DROP" applies and the register row keeps its owner) |

No defect appears twice with two different non-DROP destinations. X-2 (VL-24-154) and X-6 (VL-24-158) have no register row. The 8.1.3 P3-012 table rows for DR-140, 148, 154, 156, 157, 158, 160, 161, 163, 164, 166, 169 and 170 give the same kept rows and destinations as the file.

Reconciliation line check: the 8.1.0 reconciliation line (report 4261) states the pair count as 161 rows marked `DROP: duplicate of` (118 ledger rows, 43 register rows), covering 162 of the 171 register rows; 8.1.1 (report 4269) adds 208 register/ledger pairs. So the number of such pairs is stated (161 marked rows, 208 pairs). The file does not state a per-ledger figure; for ledger 24 the count is 20 pairs (table above).

### Omissions Found

| # | Source finding | Source file | Status (OMITTED / COVERED-BY-DEDUP / JUSTIFIED-REMOVED) | If deduped, by which report item; if JUSTIFIED-REMOVED, the fix-log entry and the code evidence | Severity |
|---|---|---|---|---|---|
| none | No distinct finding of ledger 24 or synth-08 is missing from Section 8.1 / Appendix A | both | n/a | n/a | n/a |

Rows classified COVERED-BY-DEDUP (not omissions), by kind:

| Group | Count | Where the substance sits |
|---|---|---|
| Ledger-24 rows marked `DROP[duplicate]` against another ledger-24 or ledger row (enumeration File 1, class `DEDUP of ...`) | 57 | the named kept row (for example VL-24-299 of VL-24-231, VL-24-459, 485 and 513 of VL-24-347) in Appendix A |
| Ledger-24 rows moved to `DROP: duplicate of DR-nnn` (VL-24-153, 159, 167, 172) | 4 | DR-156, DR-160, DR-154, DR-140 (kept rows, Appendix A and 8.1.3 P3-012) |
| Register rows marked `DROP: duplicate of VL-NN-nnn` (File 2 Part V) | 43 | the named ledger row; 14 of them are ledger-24 rows (VL-24-155 to 157, 160 to 165, 169, 171, 173, 170) |

No finding needed the JUSTIFIED-REMOVED class (0).

### Minor notes (none is an omission; none changes a destination, decision or recommendation number; all are `(minor under grading override)`)

1. (minor under grading override) The 8.1.0 reconciliation line calls 161 marked rows "pairs"; 8.1.1 gives 208 pairs. Both numbers are stated and neither changes a destination. The recount from the register rows' own Reason cells finds 153 register rows that name a ledger id (200 distinct mentions); the other links are written on the ledger side (for example DR-087, DR-045, DR-049 are named in the ledger rows' Reasons and in the 8.1.3 table), so the 162 and 208 figures are consistent with the file but are not reproducible from the register side alone.
2. (minor under grading override) "3,989 rows that are not DROP" (report 4271) is 3,981 after the Gate 2 fix (5,950 minus 1,969); already logged as P6-090 in `qa/qa-consolidated-findings-phase6.md`.
3. (minor under grading override) Section 8.1 carries the 5,950 rows by reference (Appendix A is the same synth-08 file, 2,024,775 bytes). This follows the orchestrator-approved carrying rule written in the report's own carrying note, and the rows are identical to the ledgers, so I treat every row as represented. If a later reader requires the rows inline, that is a decision for the owner, not an omission of source content.
4. (minor under grading override) Forty CORE rows of ledgers 19 to 24 that mention the variant scripts or the grader (for example VL-24-292 to 298, VL-24-406, VL-24-489) are not in the eight-row exception table. The report's "Scope of the exceptions" paragraph says to read CORE in them as the contract, not the script or grader, and that Section 7 governs, so no destination is made wrong.
5. (minor under grading override) Register rows exist for 20 of the 22 X-n defects of ledger 24 (the 20 pairs above); X-2 and X-6 have none (ledger rows only). Not a report omission; the ledger rows are in Appendix A.

### Per-File Counts

| File | distinct findings enumerated |
|---|---|
| research/24-value-ledger-evidence-consumers.md | 589 |
| synthesis/synth-08-value-inventory.md | 344 |

These equal the `COUNT` lines of `qa/qa-anti-omission-enumeration-4.md`. For synth-08 the 344 entries are: 63 prose items (preamble, 8.1.0 rows and reconciliation, 8.1.1 rules, authority rule, cross-ledger and provenance items, 8.1.3 and 8.1.4 items), 10 destination groups, 41 P3-012 table rows, 59 ledger-by-destination row groups (rows of ledgers 19 to 23 are enumerated row by row by agents 1 to 3) and 171 defect-register rows.

### Summary

| Measure | Count |
|---|---|
| Findings enumerated | 933 |
| REPRESENTED | 829 (528 ledger-24 rows including VL-24-181 moved with its reason; 301 synth-08 entries) |
| COVERED-BY-DEDUP | 104 (61 ledger-24 rows; 43 register rows) |
| JUSTIFIED-REMOVED | 0 |
| OMITTED | 0 |
| Blocking omissions under the grading override | 0 |

**Verdict: PASS** (zero blocking omissions; zero omissions of any kind; five minor notes above).
