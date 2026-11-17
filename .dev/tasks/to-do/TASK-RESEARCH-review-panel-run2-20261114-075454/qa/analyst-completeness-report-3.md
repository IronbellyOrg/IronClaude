# Research Completeness Verification (Gate 1, Partition C, completeness lens)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Files reviewed:** research/17-*.md through research/24-*.md (8 files: 17-defect-register, 18-repo-constraints-and-branching, 19-value-ledger-handoffs, 20-value-ledger-e2-study, 21-value-ledger-brainstorms, 22-value-ledger-collab-designs, 23-value-ledger-e1-e3-code, 24-value-ledger-evidence-consumers)
**Lens:** completeness (coverage, completeness of structure, cross-references; gate focus a-e)
**Depth tier:** Deep
**Date:** 2026-11-14
**Status: Complete** (verdict PASS, 0 blocking, 6 minor; see Summary at the end)

---

## Methodology and mechanical recounts (read-only)

- Read research-notes.md (all 269 lines) and qa/phase2-output-inventory.md first; read file 17 completely (560 lines); ledgers read in chunks (see per-file sections).
- Mechanical ledger recount (read-only awk, one private /tmp script, removed afterwards, escaped pipes `\|` inside cells handled): every row of every ledger splits into exactly 6 columns (ID, Source, Statement, Kind, Destination, Reason), no empty cell, no duplicate id, ids sequential with no gap, and the Destination cell is one single value from the closed set {CORE, MODULE-reflect, MODULE-tasklist, MODULE-spec, MODULE-pr-review, MODULE-rfqa, EVAL, HARNESS, KNOWLEDGE, DROP}. Counts: 19 = 886 rows, 20 = 868, 21 = 1,685, 22 = 955, 23 = 796, 24 = 589 (`grep -c '^| VL-NN-'` agrees with the awk count in all six).
- Per-destination recount (used below to check each ledger Summary):

| Ledger | Rows | CORE | DROP | EVAL | HARNESS | KNOWLEDGE | MOD-pr-review | MOD-reflect | MOD-rfqa | MOD-spec | MOD-tasklist |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 19 | 886 | 179 | 443 | 104 | 38 | 58 | 7 | 23 | 5 | 16 | 13 |
| 20 | 868 | 93 | 298 | 285 | 143 | 15 | 3 | 3 | 2 | 3 | 23 |
| 21 | 1685 | 85 | 584 | 489 | 58 | 247 | 4 | 1 | 1 | 2 | 214 |
| 22 | 955 | 77 | 237 | 288 | 173 | 47 | 4 | 4 | 1 | 0 | 124 |
| 23 | 796 | 276 | 150 | 75 | 20 | 28 | 4 | 225 | 2 | 10 | 6 |
| 24 | 589 | 169 | 83 | 116 | 45 | 26 | 23 | 14 | 42 | 39 | 32 |

- Further mechanical checks run on all six ledgers: (1) every `VL-NN-mmm` id mentioned anywhere in files 17-24 resolves to an existing row (0 dangling, 0 cross-ledger references); (2) per-slice destination splits recounted by the Source prefix and compared with each Summary (19, 21, 22, 23, 24 print per-slice tables, all equal to my recount; ledger 20 states 614 + 1 + 253 rows and my recount is 03 = 614, 04 = 253, other = 1); (3) DROP rows: all 1,795 carry a non-empty reason, and the "duplicate of a named VL id" counts claimed in the Summaries of 19 (411), 21 (508 + 71 obsolete), 23 (145 + 5) and 24 (57) equal my recount; (4) every slice "Gaps and Questions" line range was mapped to the ledger rows whose Source cites it (gate focus b, see Coverage Audit); (5) 228 distinct-per-file `src/tests/scripts/docs/plugins` path citations in files 17-24 (31 + 48 + 16 + 63 + 12 + 9 + 14 + 35) were tested against `git ls-files` and the working tree: no fabricated path (the 65 that did not resolve are E2-tip tools/tmp-scripts names cut to a `scripts/` prefix by the extraction, installed-skill scripts under `~/.claude`, or E2 test files, all legitimately outside HEAD); (6) forbidden-string search of files 17-24 for the two independence paths, `155942`, `RUN2-QUEUED`, `panel-unify`, `RESEARCH-REPORT-review-panel-unification` (see gate c).
- Spot checks of code claims against HEAD (read-only `sed`/`grep`/`git`, 70+ items): file 17 rows DR-001, 002, 003, 007, 014, 021, 042, 047, 049, 061, 064, 109, 120, 124, 133-136, 140, 143, 144, 153, 155, 156 and the stale-doc list; file 18 Makefile lines 113-118, 148-151, 171-176, 292-295, 479-481, 549, `test.yml` 22, 47, 125-136, `.gitignore` 13, 79, 83-85, 127-135, `.pre-commit-config.yaml` 119-141, CLAUDE.md lines 16-37, 67, 100, 303-315, `git ls-files .claude`, branch-prefix counts (40/2/2/1/1/1 = 47), 19 worktrees, 0 `integration` refs, 36 verdict-matrix tests, 38 reflect test files, 125 plugin files, 148 `src/superclaude` lines; ledger addenda in 19-24 (findings.py, findings_v2.py, ledger.py, panel.py, telemetry.py, cluster.py, `reflect_shadow_exit.py`, `fsm.py`/`loop_guard.py`, line counts of 10 consumer files and 15 reflect modules/scripts, `git diff --shortstat ec259f1b7 HEAD`, `rev-list` = 11, E2 tip `git ls-tree` 96 dirs / 55 tmp-scripts / 0 `/lib/` paths, E2 `src tests` diff empty). Every one of these checks agreed with the research file. Where a claim could not be checked read-only I say so in the findings.

---

## Verdict: PASS (0 blocking findings, 6 minor notes, gaps listed below)

## Coverage Audit

| Scope item (from research-notes.md SUGGESTED_PHASES rows 17-24 and the assigned slices) | Covered by | Status |
|---|---|---|
| 17: every defect of slices 01, 02, 03, 04, 09, 10, 11 (D1-D13, P1-P7, T1-T2, B-1..B-7, H1-H12, run-1 D1-D16, R2CM D1-D23, R2CP 1-19, slice 03 P1-P10 / H1-H19, slice 04 7.1-7.26, slice 09 D-1..D-31, slice 10 D-01..D-25 / C-01..C-19 / H-01..H-12, slice 11 X-1..X-22) | 171 rows DR-001..DR-171 plus the crosswalk table at lines 427-468; I rechecked the mapping of slice 09 D-1..D-31 against slice 09 lines 247-279 and slice 10 / 11 id lists | COVERED (slice 04 section S3 script defects 3.2, 3.3, 3.6, 3.9, 3.10, 3.13 are not rows; see M4) |
| 17 open item (a): reproduce read-only | 64 REPRODUCED, 44-46 TRACED, 58-59 UNVERIFIED rows; my recount of the Repro column of the 168 rows that split cleanly: 64 / 44 / 58 / 2 mixed, the remaining 3 rows (escaped pipes) bring it to the stated 64 / 46 / 59 / 2 | COVERED |
| 17 open item (b): tests that pin a defect as intended behaviour | table at lines 484-496, plus 12 additional pins; the 8 named ids (D-1, D-2, D-3, D-5, D-6, D-11, D-25, D-26) all answered, 2 honestly marked "from slice 09 only [UNVERIFIED]" | COVERED |
| 17 open item (c): one numbering scheme | DR-nnn with crosswalk over 4 schemes (A hand-off, B R2CM, C R2CP, D run-1) plus slice-local schemes; the assignment said "three"; the file found four and says so | COVERED |
| 17 open item (d): count in vs out | table at lines 410-421 (263 in, 253 mapped, 10 claim checks, 0 silently missing); sums recomputed: 41 + 23 + 19 + 16 + 29 + 26 + 31 + 56 + 22 = 263; owner buckets 75 + 29 + 2 + 2 + 14 + 36 + 2 + 11 = 171 | COVERED (closure claim slightly overstated, see M4) |
| 17 open item (e): the two [CODE-CONTRADICTED] claims (159 functions; fenced-yaml memory lesson) | lines 517-520 and DR-074, DR-153; I re-ran the code reading of `cluster_cmd.py:27-34` and memory line 64: both as described | COVERED |
| 18: ref rule (`feat/review-panel` vs `feat/review-panel/<name>`) tested in a scratch repo | section 3 with verbatim command output in both creation orders; git 2.47.3 confirmed; real-repo state (0 `feat/review-panel*` refs) re-checked | COVERED |
| 18: sync-dev / verify-sync, installed-path rule, plugin mirror, contract pins, test layout, fork-only PR flow, Orca rule, `.claude/` staging ban, "what fails on a naive layout" | sections 1, 2, 4-9 (18 numbered failure modes F1-F18) | COVERED |
| 19: slices 01 and 02 (hand-offs, notes) | 886 rows; every gap and question line of slice 01 (539-548, 554-560) and slice 02 (610-621, 624-631) has a row | COVERED |
| 20: slices 03 and 04 | 868 rows; every gap and question line of slice 03 (555-565, 568-576) and slice 04 (335-342, 345-352) has a row | COVERED |
| 21: slices 05 and 06 | 1,685 rows; every gap and question line of slice 05 (695-697, 700-706, 709-718) has a row; slice 06 lines 662-663, 665, 669-675, 678-687 have rows, lines 664 and 666 are carried by VL-21-1667 / VL-21-1668 (sources cite 663 / 665) | COVERED |
| 22: slices 07 and 08 | 955 rows; every gap and question line of slice 07 (425-437) and slice 08 (733-742, 745-756) has a row | COVERED |
| 23: slices 09 and 10 | 796 rows; every gap and question line of slice 09 (462-472) and slice 10 (586-594, 597-604) has a row | COVERED |
| 24: slices 11 and 12 | 589 rows; slice 12 lines 485-494 and 497-505 have rows (Q5 at 501 is carried by VL-24-543 as the Summary says); slice 11 gaps G-1..G-9 and questions Q-1..Q-7 are not each a row with their own source line (only G-6, G-8, G-9 are), but each is named inside a row that carries its substance (G-1 in VL-24-015/016/018, G-2 in VL-24-162/180, G-3 in VL-24-155/165, G-4 in VL-24-138..142, G-5 in VL-24-109, G-7 in VL-24-034, Q-1 in VL-24-188, Q-2 in VL-24-148, Q-3 in VL-24-189, Q-5 in VL-24-158/196, Q-6 in VL-24-162, Q-7 in VL-24-183) | COVERED by meaning |
| Slice body coverage of the six ledgers (all non-header lines of the 12 slices against ledger Source cites, ranges wider than 14 lines treated as bulk) | single-line cites cover 380 of 415, 420 of 464, 418 of 446, 240 of 269, 498 of 548, 427 of 511, 231 of 309, 419 of 556, 277 of 349, 417 of 455, 168 of 295, 326 of 360 non-header lines; the large uncovered runs are all items the ledgers say they fold into a grouped row (slice 07 C1/C4/C5 tables in VL-22-312/329/337, slice 08 S9.1/S10 in VL-22-883/905, slice 09 constants table in VL-22-210..212 of ledger 23, slice 09 K table in VL-23-287..294, slice 06 file-tree and comparison tables in VL-21-912 and neighbours, slice 11 value table V-28..V-42 each cited by a row) | COVERED |

## Evidence Quality

| Research file | Evidenced claims | Unsupported claims | Quality Rating |
|---|---|---|---|
| 17-defect-register.md | all 171 rows carry file:line or git path:line plus a Repro status; 64 reproduced and 44-46 traced against code, 58-59 rows explicitly `UNVERIFIED` with the reason; I re-verified 25 rows against HEAD or the E2 tip and all agreed | 0 untagged. Three rows (DR-066, DR-069, DR-078) rest on a slice line and say so ("TRACED via slice") | Strong |
| 18-repo-constraints-and-branching.md | every rule row has a stating file:line and an enforcing file:line, tagged CODE-VERIFIED / OBSERVED / UNVERIFIED; 40+ lines re-verified, all agreed | 0 | Strong |
| 19-value-ledger-handoffs.md | 886 rows, each with `slice:line` Source; 182 rows tagged `[V]`/CODE-VERIFIED, 93 `[UNVERIFIED]`, 10 `[CODE-CONTRADICTED]`; verification addendum with 17 checks I re-ran in part | 0 rows without a source; untagged rows are the slice's own claims by the stated tag convention (lines 899-901) | Strong |
| 20-value-ledger-e2-study.md | 868 rows with slice:line; 58 `[UNVERIFIED]`, 5 `[CODE-CONTRADICTED]`; 12-row code verification table (lines 885-896) | 0 without a source (1 row cites "git ls-tree" instead of a slice line and says so) | Adequate-Strong (very few bracket tags; the table at lines 881-896 and gap list 919-927 carry the unverified status in bulk) |
| 21-value-ledger-brainstorms.md | 1,685 rows with slice:line; 63 `[UNVERIFIED]`, 18-19 `[CODE-VERIFIED]`, 3 `[CODE-CONTRADICTED]` bracketed; verification table lines 1700-1719 | the Summary tag counts are wrong (M1) | Adequate-Strong |
| 22-value-ledger-collab-designs.md | 955 rows with slice:line; 68 `[UNVERIFIED]`, 14 `[CODE-VERIFIED]`, 4 `[CODE-CONTRADICTED]`; verification table lines 1006-1019 | 0 | Strong |
| 23-value-ledger-e1-e3-code.md | 796 rows; 64 `[UNVERIFIED]`, 50 `[CODE-VERIFIED]`, 12 `[CODE-CONTRADICTED]`; batch of 11 re-derived quantities, all equal to my recount | 0 | Strong |
| 24-value-ledger-evidence-consumers.md | 589 rows; 38 `[UNVERIFIED]`, 21 `[CODE-VERIFIED]`, 2 `[CODE-CONTRADICTED]`; verification notes lines 604-615 (I re-ran a subset of ten of those checks) | 0 | Strong |

## Documentation Staleness

The assigned files are code-first research; the doc-sourced claims they carry are the ones in AMBIGUITIES_FOR_USER. Status of each in my partition:

| Claim | Source doc | Verification tag in my partition | Status |
|---|---|---|---|
| #518 credited with the `cli/review` changes | E2 hand-offs, `HANDOFF-run1-vs-run2.md:22` | DR-045 REPRODUCED, VL-19-027 `[CODE-CONTRADICTED]` | OK |
| run-1 D14 "no tasklist review step" | run-1 hand-off | VL-19-029 DROP `[CODE-CONTRADICTED]` with `SKILL.md:89`; DR note at line 470 | OK |
| "reflect has no panel/tier code" | run-2 Q4/Q9 | DR-066 (partly stale), file 18 section 9 (import direction), ledger 23 row on `SKILL.md:338-349` | OK |
| alias GT3 found once | run-1 | VL-19-091 / VL-19-428 correct it (alias GT1); VL-19-734 still prints the old wording untagged | FLAG (M2, minor) |
| "discarded with no error" | `COMBO-REPORT.md:292` | DR-087, VL-20-102 `[CODE-CONTRADICTED]` | OK |
| "four verdict flips" | `COMBO-REPORT.md:292` | DR-048, VL-20-739 (3, not 4); VL-19-209 prints "4 verdict flips (3 shown)" with a pointer to VL-19-090 | OK |
| "16 empty terra reviews" | `COMBO-REPORT.md:294` | DR-095 (14 terra + 2 luna), VL-20-718 / 771; VL-19-204 and VL-20-109 repeat the old figure untagged | FLAG (M2, minor) |
| harness `unpassable-ac` | E2 harness brief | DR-028 DROP (fixed in harness), VL-20-025 | OK |
| "T2bModel01 not referenced in src/ or tests/" | R2CP:56 | DR-075 `UNVERIFIED`; VL-19-494 `[CODE-CONTRADICTED]` at the base; at HEAD the contradiction holds (see M3) | OK with note |
| "159 functions" | run-2 notes | DR-074 re-summed to 179; VL-19-645 | OK |
| E2 seed "no missing-task / no severity levels" | seed brief | VL-21-1540 `[CODE-CONTRADICTED]` (and the verification table row at ledger 21 line 1707) | OK |
| `theory.py` HARD set as applied | E2 brainstorm | VL-21-712 `[CODE-VERIFIED]` at the tip | OK |
| memory lesson "fenced yaml calibration not parsed by cluster" | `docs/memory/reflect/...:64` | DR-153 `[CODE-CONTRADICTED]`, VL-23-676, VL-24-168; I re-read `cluster_cmd.py:27-34` | OK |
| [UNVERIFIED] list (92/80/49 unit; combos sizes; E2 commits after 4a22d7421; muse-ember; collaboration estimates; #346 numbers; installed variants; thresholds approval) | various | 92/80/49 unit carried open (VL-19-579, DR-046 label fix); combos size resolved to 96 dirs (DR-047, VL-19-088); E2 commits: `git diff ec259f1b7 <tip> -- src tests` empty (VL-19-454); muse-ember absent at HEAD (DR-016); estimates, #346 numbers, installed variants and thresholds carried as `[UNVERIFIED]` rows | OK |
| Doc errors found by file 18 (S1-S7) | CLAUDE.md, docs | all seven re-verified by me except S5 (PR #278 content not read; tagged UNVERIFIED by the file) | OK |

## Completeness

| Research file | Status | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 17-defect-register.md | Complete (line 4) | Y (line 557; per-slice Key Takeaways plus final register counts) | Y (line 522, 9 numbered gaps + 6 owner questions) | Y (per-slice blocks at lines 95, 168, 206, 243, 307, 362, 400) | Complete |
| 18-repo-constraints-and-branching.md | Complete | Y (line 228) | Y (line 206, 8 items) | Y (Key Takeaways bullets at the end of sections 1, 2, 3, 4, 5, 7, 8, 9) | Complete |
| 19-value-ledger-handoffs.md | Complete | Y (line 927; per-destination table with per-slice split, 886 total) | Y (line 960; G1-G10, Q1-Q6) | n/a for ledgers (Summary names the highest-value CORE rows) | Complete |
| 20-value-ledger-e2-study.md | Complete | Y (line 898; per-destination counts in text, per-slice 614 + 1 + 253) | Y (line 917) | n/a | Complete |
| 21-value-ledger-brainstorms.md | Complete | Y (line 1723; per-destination table with per-slice split) | Y (line 1773) | n/a | Complete |
| 22-value-ledger-collab-designs.md | Complete | Y (line 972; per-destination table with per-slice split) | Y (line 1021) | n/a | Complete |
| 23-value-ledger-e1-e3-code.md | Complete | Y (line 830; per-destination table; per-slice counts in text) | Y (line 869) | n/a | Complete |
| 24-value-ledger-evidence-consumers.md | Complete | Y (line 617; per-destination table with per-slice split) | Y (line 650) | n/a | Complete |

Ledger Summary totals versus my recount (all six equal, row by row and destination by destination): 19 = 886 (179 / 443 / 104 / 38 / 58 / 7 / 23 / 5 / 16 / 13), 20 = 868 (93 / 298 / 285 / 143 / 15 / 3 / 3 / 2 / 3 / 23), 21 = 1,685 (85 / 584 / 489 / 58 / 247 / 4 / 1 / 1 / 2 / 214), 22 = 955 (77 / 237 / 288 / 173 / 47 / 4 / 4 / 1 / 0 / 124), 23 = 796 (276 / 150 / 75 / 20 / 28 / 4 / 225 / 2 / 10 / 6), 24 = 589 (169 / 83 / 116 / 45 / 26 / 23 / 14 / 42 / 39 / 32), in the column order of the recount table at the top of this report.

---

## Gate focus (a) to (e)

| Gate focus | Result |
|---|---|
| (a) every kept claim has file:line / git path:line evidence or an explicit [UNVERIFIED] tag | Holds. File 17: every row has a location and a Repro status, 58-59 rows say `UNVERIFIED` and why. File 18: every claim tagged. Ledgers: every row has a slice:line Source; 1 row cites a git command instead; code facts re-derived by the ledger authors are tagged `[V]`/`[CODE-VERIFIED]`, slice-only facts are `[UNVERIFIED]` or covered by the bulk statement of the tag convention (ledger 19 lines 899-901; ledger 20 lines 919-927; ledger 21 lines 1720-1721). Weakness: ledgers 20 and 21 mark few rows individually as verified (16 and 26 rows mention a verified tag out of 868 and 1,685; 106 and 124 rows mention `unverified`), the rest relies on the bulk statements; see M1 for the wrong tag count in ledger 21. |
| (b) every open item of research-notes.md for the file and every slice gap/question resolved, logged or carried | Holds. File 17 open items (a)-(e) all answered. File 18 open items (a)-(d) answered (ref rule observed). Slice gap and question lines of all 12 slices are carried as ledger rows (see Coverage Audit); the one structural exception (slice 11 G-1..G-5, G-7, Q-1..Q-7 have no row with their own source line) is covered by meaning. |
| (c) no run-1 contamination | Holds. Search of files 17-24 for the two forbidden paths, `155942`, `RUN2-QUEUED`, `panel-unify`, `unify-2026`, `RESEARCH-REPORT-review-panel-unification` finds only independence statements: file 17 line 534 (names both paths in a rule sentence and the slice 03 slip; allowed), file 20 lines 616 and 927 (do not name the path), file 23 line 884, file 19 line 974, file 22 line 1033. No citation, quotation or tag from the run-1 folder. "Run-1" everywhere else means the E2 `HANDOFF-review-panel-unification.md` (4a22d7421), which is allowed. Note: file 17 line 534 spells out the complete forbidden folder name; allowed by the rule but a later "no occurrence" grep of the folder name will hit it (the Phase 2 inventory already records this hit). |
| (d) every value-ledger row has exactly one destination (CORE / MODULE-name / EVAL / HARNESS / KNOWLEDGE / DROP with reason) | Holds mechanically: 5,779 of 5,779 rows have one destination token from the closed set, 0 empty cells, 0 duplicate ids; all 1,795 DROP rows have a reason (1,759 use recognised duplicate / obsolete / retracted / out-of-scope / evidence-free wording; the other 36 give an explicit reason in other words, for example "count line", "by design, not a defect", "path-specific to the E2 worktree", "size inventory with no design consequence"). 44 duplicate-DROP rows name only other DROP rows as their target; following the chains, 22 of them end in a DROP row (the other 22 reach a live row), and I read those terminal rows (VL-19-029, 211, 212, 215, 307; VL-20-081, 209, 334-336, 342; VL-21-428, 430; VL-22-006, 105, 118, 155, 270, 883, 905; VL-24-217, 224, 291, 304, 470): each is dropped for a stated reason (contradicted claim, retracted figure, owner ended testing, obsolete variant, evidence-free prediction, out-of-scope cleanup, grouped restatement of live rows named in its statement). None loses design value that I could find. Two ledgers add the destinations MODULE-pr-review and MODULE-rfqa, which fit "MODULE-name". |
| (e) no claim builds on a [CODE-CONTRADICTED] / [UNVERIFIED] AMBIGUITIES row as fact | Holds for every design-relevant claim. Residual: three rows repeat a contradicted figure untagged (M2); all three have the correction in the same or a sibling ledger. File 17 and ledgers 19/20/23/24 treat the 12 contradicted claims as contradicted (see Documentation Staleness). |

## Cross-reference check

- File 17 <-> ledgers: the register states defect ids in slice-local schemes (`slice09 D-n`, `slice10 D-nn`, `slice11 X-n`, `01:line`) and the ledgers cite `slice:line`; both resolve to the same slice lines, so the synthesis can join them, but neither side carries the other's ids (0 `DR-` ids in the six ledgers, 0 `VL-` ids in file 17). Registered as part of M6.
- File 17 <-> file 18: DR-155 (`.gitignore:13` `lib/` and `:79` `*.log`) is a repository constraint that already destroyed E2 harness code; file 18 does not list it (M5).
- File 17 <-> ledger 22 <-> ledger 23: `.gitignore:13` is carried by 8 rows of ledger 22 and DR-155; the reflect-engine defects DR-128..DR-154 equal the ledger 23 defect rows (VL-23-606..630 and neighbours); the memory-lesson contradiction appears in DR-153, VL-23-676 and VL-24-168 with the same verdict; the `lint_cmd` / `estimate_cmd` ghost names appear in DR-042, VL-19-049, VL-23-007 / 329 and file 18 section 9 with the same file:line.
- Ledger 19 <-> ledger 20 <-> ledger 21: the 92 / 80 / 88 / 49 figures are carried as open in all three (VL-19-579, VL-20-735 / 737, VL-21-726), with the same verdict (92 = all dropped, 49 = blocking subset, unit of 80 open).
- Ledger 23 <-> ledger 24: ledger 24 re-checks `cluster_cmd.py:27-34`, `findings.py:14-24`, `ledger.py:17,19,22,37` that ledger 23 rows cite; consistent. Ledger 24 correctly flags slice 12's "15 modules / 5131 lines" against 16 files / 5,086 lines (also file 18 section 9 and ledger 23 row on the 16-module count).

## Contradictions Found

No contradiction between two research files that is not already surfaced by one of them. Surfaced and consistent:

- combos directory count: 96 directories (DR-047, VL-19-088, my `git ls-tree` = 96) against 95 (VL-20-625, kept open), 97 entries and "107" (E2 notes); the files agree on the 96 count except VL-20-625.
- `@live7` duplicate count 30 / 40 (DR-014, VL-19-122) against the E2 figure 26 / 40; recorded identically in 17 and 19 (G2).
- Test totals: "159" against 179 (DR-074, VL-19-645); claimed passing tests of the five collaboration packages (799) against static counts (VL-22 gaps line 1025); the `def test_` count of `tests/review` is 380 in ledger 23 (I recounted 380 in 19 modules).
- Same-ledger inconsistency: VL-19-734 (ledger 19 line 745) lists "alias GT3 in 1 row" among five defects "no valid row ever caught", while VL-19-091 (line 102) and VL-19-428 say the defect found once is alias GT1 (B6) and that run-1's "alias GT3 found once" is wrong; VL-20-438 carries the conflict as an open question. Registered as part of M2.
- Destination disagreements that the ledgers themselves list for the synthesis: ledger 23 "Destination decisions the synthesis must re-validate" items 1-9, ledger 21 gap 6, ledger 19 G8, ledger 22 gap 4, ledger 24 G-L7. Not contradictions, open design choices.

---

## Findings

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| M1 | MINOR | N | `21-value-ledger-brainstorms.md:1743` (Summary, last sentence of the DROP paragraph) | The sentence "Tags in the file: 25 rows mention [CODE-VERIFIED], 4 [CODE-CONTRADICTED], 89 [UNVERIFIED]" does not match the file. | My recount over the 1,685 rows: rows mentioning `[CODE-VERIFIED]` any form = 26 (19 occurrences with brackets), `[CODE-CONTRADICTED]` = 4, `unverified` any form = 124 rows (63 with the bracketed `[UNVERIFIED]` tag); whole-file mentions V = 40, C = 6, U = 127. Neither reading gives 89. | Replace the three figures with the recount (26 / 4 / 124 rows, or 18-19 / 3 / 63 for bracketed tags). Count metadata only; no row is affected. |
| M2 | MINOR | N | `19-value-ledger-handoffs.md:215` (VL-19-204), `:745` (VL-19-734); `20-value-ledger-e2-study.md:120` (VL-20-109) | Three rows repeat figures that research-notes AMBIGUITIES lists as [CODE-CONTRADICTED] without a tag: "16 empty terra reviews in valid rows" (VL-19-204, VL-20-109; slice 04 7.6 recomputes 14 terra + 2 luna) and "alias GT3 in 1 row" among never-caught defects (VL-19-734; the once-found defect is alias GT1 per VL-19-091). The corrections exist (VL-20-718 / 771; VL-19-091 / 428; VL-20-438) but are not linked from these rows. | `grep` for "16 empty terra" in ledgers 19-24 returns VL-19-204 and VL-20-109 as the only rows without a correction mark; VL-19-734 sentence is internally inconsistent ("never caught ... in 1 row"). Destinations (CORE, EVAL) do not depend on the wrong figure. | Append "[CODE-CONTRADICTED: 14 terra + 2 luna, VL-20-718]" to VL-19-204 and VL-20-109, and "[alias GT1, see VL-19-091]" to VL-19-734. |
| M3 | MINOR | N | `17-defect-register.md:155` (DR-075) | The row stays `UNVERIFIED` and carries a parenthetical saying `T2bModel01` was found at HEAD only under `skills/ccsession-tag/*` and `sc-implement-protocol/refs/retry.md`. A `git grep -c T2bModel01 -- src tests` at HEAD also lists `tests/unit/test_ccsession_tiers.py` (3), `tests/skills/test_model_alias_policy.py` (1), `tests/skills/test_workflow_archive.py` (1) and `src/superclaude/skills/ccsession-tag/ccsession-models.json:107`, `README.md`, `MODEL-TIERS.md`. The run-2 claim "not referenced anywhere in src/ or tests/" is therefore [CODE-CONTRADICTED] at HEAD, not merely at the base, and one grep would have settled it. | My `git grep -c` at HEAD (7 files, 10 hits). VL-19-494 already records the base-commit contradiction. | Change DR-075 to `[CODE-CONTRADICTED]` with the HEAD grep result and drop the incomplete parenthetical. The row is DROP (documentation error), so no ownership change. |
| M4 | MINOR | N | `17-defect-register.md:212` (slice 04 mapping paragraph) and the count table at `:410-421` | The closure claim "0 silently missing" counts only slice 04 items 7.1-7.26; the script-defect list S3 (3.1-3.15, slice 04 lines 46-62) is mapped for 3.1, 3.4, 3.5, 3.7, 3.8, 3.15 only. Items 3.3 (same bug in the clean view, covered by DR-091), 3.6 (`doubles.py` inherits the `attrib.py` flaw, covered by DR-038), 3.9 (three pre-final estimates), 3.10 (merge scripts hard-code reviewer-id to model/tier maps and call `/tmp/b4-job-one.sh`) and 3.13 (allsets chunk reconciliation not committed) have no register row. The assignment names "audit-script bugs" for this file. | Slice 04 lines 46-62 against the register; the omitted items are rowed in ledger 20 as VL-20-658, VL-20-659 (3.10), VL-20-662 (3.13), VL-20-331 / 342 / 553 (3.6) so no value is lost. | Add two HARNESS/EVAL rows (3.10, 3.13) or state in the count table that slice 04 S3 is carried by ledger 20. |
| M5 | MINOR | N | `18-repo-constraints-and-branching.md` sections 4 (rule table a1-a11) and 8 (failure table F1-F18) | The repository's `.gitignore:13` rule `lib/` and `:79` `*.log` are not listed as constraints or naive-layout traps. File 17 DR-155 and 8 rows of ledger 22 show that the `lib/` rule silently excluded the `lib/` folders of the E2 harnesses (0 `/lib/` paths in the tip tree, `git ls-tree` count = 0), so a plan that puts a shared core or harness code under any `lib/` folder would lose it without any hook or test failing. Research-notes feeds the sequence-and-gates synthesis (synth-09) from 18, 06, 16 and 13, not from 17 or 22. | `grep -n 'lib/\|gitignore:13\|gitignore:79' 18-*.md` finds no hit for the rule; `.gitignore:13` is `lib/`, `:79` is `*.log` (read). | Add one row to section 8 ("a directory named `lib/` or a `*.log` file is ignored by git, no gate fails", `.gitignore:13`, `:79`, cross-reference DR-155) and name 17 as an input of synth-09. |
| M6 | MINOR | N | `17-defect-register.md:513-515` (open item (a)) and `:559` (Summary) | The status label REPRODUCED is applied to 11 rows that are static reads (6 "REPRODUCED by reading": DR-046, 048, 088, 140, 144, 156; 5 "REPRODUCED by Grep"), while TRACED is defined as "read the code, did not execute". The Summary sentence "64 rows were reproduced by running read-only snippets or direct commands" therefore overstates by up to 11. Also no DR-to-VL crosswalk exists (see Cross-reference check). | Count of the Repro cells: `grep -c '| REPRODUCED by reading'` = 6, `'| REPRODUCED by Grep'` = 5. | Reword the Summary to "64 REPRODUCED (53 by execution or direct command, 11 by static read or Grep)" or relabel the 11 as TRACED. |

No finding is blocking: none of M1-M6 changes a design-relevant fact, a destination, a count that a later gate depends on for correctness, or a citation that a reader would act on wrongly.

---

## Compiled Gaps (all gaps of files 17-24, de-duplicated; none blocks synthesis)

### Critical Gaps (block synthesis)

- None. Every open item that synthesis needs to start (defect register, repository constraints, six value ledgers with one destination per row) exists and is internally consistent.

### Important Gaps (affect quality; each is logged by its own file and must reach synthesis section 9 or the evidence trail)

- Unverified evidence base of the E2 study: 58-59 register rows and the bulk of ledger 20 rest on E2 audit bodies B, C, E, F, `COMBO-REPORT.md` beyond a few lines, judge sessions and raw transcripts that are not in the commit (17 gap 1; 20 gaps 3-4; 19 G1). Any number from them must carry its tag in synthesis.
- Counts that the files could not settle: the unit behind "92 / 80 / 88 / 49", combos directories 95 vs 96, invalid score files 1 vs 2, gt2-hits 81 vs 83, 8,814 + 500 vs 9,312 files, Qwen slots 3 vs 4, quarantine 417 vs 428 files, audit A "70 rows" vs 71 / 88 / 89 (20 "still open"; 17 gap 2; 19 G2-G4).
- `@live7` duplicate count: 30 / 40 reproduced here against the E2 figure 26 / 40; the run-id set behind 26 is unknown (17 gap 2; 19 G2).
- Reflect shadow-exit numbers (13 of 20 runs, EV-1 8/13 against 3/39, 6 parity failures) were not re-run by file 17 or 23; DR-138, 139, 147 rest on slice 10's recorded output (17 gap 3; 23 G-9).
- The relation of the installed-only E3 scripts (`review_ledger.py`, `diffgate.py`, `stoprule.py`) to `cli/review/ledger.py`, the contents of `.dev/research/346-review-loop-experiments/` (6,523 tracked files) and all numbers of the #346 phase-5 FINAL-REPORT are unread or unverified (23 G-8; 24 G-L1, G-L6; research-notes AMBIGUITIES). Owned by files 03 and 14 in partition A / B, not by this partition.
- The E2 collaboration engines (`lib/` of R2 `bin/`, r3, r4, r5) cannot be inspected; the validator, renderer and engine rules exist only as design rows (22 gap 7; DR-155).
- The defect register covers slices 01-04 and 09-11 only; defects of slices 05-08 and 12 (collaboration harness defects D-R3-1, D-R5-1, C-11 sandbox flag, brainstorm arithmetic errors E1-E9, consumer conflicts I1-I17) are carried only in ledgers 21, 22 and 24 and have no register row or fix owner (17 gap 6).
- The collaboration planning values (reach probabilities, act rates, hook cost, resume start, +29% / +59% elapsed, 138 / 358 / 89 / 106 / 108 claimed tests) are slice-sourced and unverified in every ledger (21 gap 3; 22 gaps 1-2).
- Approval status of the pilot stop rule and thresholds T-1..T-10 is unknown (24 G-L5).
- Destination choices that the ledger authors flag for re-validation (19 G8, 21 gap 6, 22 gap 4, 23 "Destination decisions", 24 G-L7): the synthesis must settle them once, for example the review loop as CORE or MODULE-spec, the class registry and move catalogue as CORE or MODULE-tasklist, `cluster_agreement` as CORE or MODULE-reflect, `panel_lint` as EVAL or CORE.

### Minor Gaps (notes; do not block synthesis)

- M1-M6 above.
- Installed CLI version when the fenced-yaml memory lesson was written is unverified (17 gap, DR-153; 24 G-L3).
- Whether the Orca worktree hook and the pre-commit hooks are installed on a given machine; remote-side behaviour of the git ref rule; PR #278 content (18 gaps 1-3; S5).
- `make verify-sync`, `make lint-architecture`, pytest and ruff were not executed by file 18 (assignment forbade it); section 8 failures are derived by reading (18 gap 5). A later plan should run them.
- Slice-level arithmetic inconsistencies carried, not fixed (ledger 21 gap 2: SUM 0.92-2.73 vs 0.93-2.75 and 0.63-2.47 vs 0.64-2.48; 13 vs 15 failure rows; 13 vs 14 levers).
- File 17 line 534 spells out the full forbidden folder name inside an independence sentence (allowed; noted so that a later strict-string search is not surprised).

## Depth Assessment

**Expected depth:** Deep (data-flow traces, integration-point mapping, pattern analysis, exhaustive value capture).
**Actual depth achieved:** Deep. File 17 reproduces 64 behaviours with read-only code runs (four scratch scripts in `/tmp`, deleted afterwards) and maps 263 original ids from nine schemes onto 171 rows with owners, test pins and a crosswalk. File 18 observed the git ref rule in two scratch repositories (both creation orders, deleted afterwards) and derives 18 concrete naive-layout failures from the Makefile, workflows, pre-commit config, contract pins and test files, with 40+ line citations that I re-verified. The six ledgers enumerate the 12 slices item by item (5,779 rows, one destination each) and re-verify the code facts they relay.
**Missing depth elements:** None that block. The ledgers are secondary to the slices by design, so study numbers stay at slice-level confidence; the defect register does not cover slices 05-08 and 12 (see Important Gaps).

## Recommendations

- Before or during the serialized fix cycle, apply the six minor edits M1-M6 (all are one-line text corrections or one added row each; none needs new investigation). They are not required for the gate to pass.
- Carry the Important Gaps into synthesis section 9 (open questions) and the evidence trail with their tags; do not upgrade any [UNVERIFIED] row to fact.
- When synthesis builds section 8.2 (sequence and gates, inputs for a plan), take the `.gitignore:13` `lib/` and `:79` `*.log` rule from DR-155 together with file 18 section 8 (M5).

## Limits of this review (honest scope statement)

- Files 17 and 18 were read completely (560 and 230 lines). The six ledgers (886 + 868 + 1,685 + 955 + 796 + 589 rows, about 5,800 table lines) were NOT read line by line: I read the heads, the Summary, Verification and Gaps sections of all six in full, and sampled body rows in each (ledger 19 rows 1-49 and 880-886; ledger 20 rows 409-425 and 868; ledger 21 rows 1685 and the tag/summary section; ledger 22 rows 668, 883, 900, 905, 955; ledger 23 rows 137-150 and 285-294, 796; ledger 24 rows 14-33, 300-312, 587-589), plus every row that a targeted search surfaced (about 60 rows). The remaining rows were checked mechanically in full: column count, empty cells, id sequence, destination set, Summary recounts, per-slice splits, dangling references, DROP reasons and duplicate chains, forbidden strings, cited-path existence, gap-line coverage, and coverage of slice lines by Source cites. A defect that lives only in the wording of an unsampled row's Statement would not have been seen.
- I re-ran code checks only through read-only `sed`, `grep`, `git show`, `git ls-tree`, `git grep`, `git diff --shortstat`, `wc`, `ls`; no `pytest`, no `uv run`, no checkout, fetch, pull, stash, commit or push. Scratch files were written only inside private `/tmp/ironclaude-batch.*` directories that were removed in the same call (each call printed `CLEAN_OK`). I did not re-create the scratch git repository of file 18 section 3; I confirmed its result by reading the command log and the real-repository branch state (0 `feat/review-panel*` refs).
- No web research was used. No research file, scope slice, the task file or any other repository file was modified; the only file written is this report. Run-1 folder and `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` were never read, listed, grepped or cited; `.dev/tasks/` was excluded from repository-wide searches (all searches were pinned to `src`, `tests`, `scripts`, `docs`, `plugins`, `.github`, root files, or to this task's own `research/` folder).

---

## Summary

- Files reviewed: 8 (17, 18, 19, 20, 21, 22, 23, 24), 7,119 lines, 5,779 ledger rows, 171 register rows.
- Blocking findings: 0. Minor findings: 6 (M1-M6), all non-blocking text or count corrections.
- Gate focus: (a) holds, (b) holds, (c) holds, (d) holds mechanically for all 5,779 rows, (e) holds for every design-relevant claim (three untagged repeats of contradicted figures, M2).
- Mechanical results: all six ledger Summary totals and per-destination and per-slice splits equal my recount; ids sequential; 0 dangling cross-references; 1,795 DROP rows all with reasons; every slice gap and question line is carried by a ledger row or named inside one.
- Verdict: **PASS**. Synthesis may start from these eight files. The six minor edits are recommended, not required.

**Status: Complete**
