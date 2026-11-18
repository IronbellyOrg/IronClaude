# Merge Execution Log

## Metadata

- Base: Variant 2 (run 2 report, `RESEARCH-REPORT-review-panel-unification-run2.md`, 5,098 lines; copy `adversarial/variant-2-original.md`)
- Other variant: Variant 1 (run 1 report, 4,476 lines; copy `adversarial/variant-1-original.md`)
- Plan: `adversarial/refactor-plan.md` (changes M-00 to M-30; auto-approved after three plan reviews, see "Plan departures and open points")
- Executors: E1 (base corrections: M-01, M-12, M-13, M-24), E2 (run 1 block extraction: M-03 to M-07, M-09, M-11, M-14, M-16 to M-22, M-25, M-27 heading demotion), E3 (new text: M-00, M-02, M-08, M-10, M-15, M-21 part 9.12, M-22 part 10.B, M-28, M-29 D and E), E4 (assembly, table of contents, Appendix F, edits left to E4, validation: M-23, M-26, M-27 Appendix F, M-30)
- Output: `.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/MERGED-review-panel-unification.md` (10,109 lines, 2,629,571 bytes)
- Scripts: `partials/merge-scripts/e1_base_corrections.py`, `e2_v1_extract.py`, `e3_appendix_c.py`, `e3_appendix_d.py`, `e4_assemble.py`, `e4_validate.py`
- Machine records: `partials/merge-stage/e1-edits.json` (E1 before/after), `partials/merge-stage/e4-edits.json` (E4 before/after, 22 entries), `partials/merge-stage/e4-blocks.json` (block list with output line ranges), `partials/merge-stage/E4-validation-report.md` (full validation output)
- Changes applied: 31 of 31 (none skipped, none failed; departures listed below)
- Merge execution status: success (all 16 validation checks PASS)
- Document status carried by the merged file: `partial` (compare convergence 94.0% strict, gate BLOCKED_BY_INVARIANTS: 7 HIGH UNADDRESSED invariants, carried as open items in 9.12)
- Timestamp: 2026-11-15T02:16:58Z
- Read-only guarantees: the two variant copies, the original reports and every stage file were read, never written (`base-corrected.md`, the 15 run 1 blocks and the 9 new-text blocks were copied into memory by `e4_assemble.py`; every E4 text change is an asserted single-occurrence replacement recorded in `e4-edits.json`). No git write command was run. Nothing under `.claude/` was read or written.

## Changes Applied

Line ranges are lines of the merged file (Appendix F.1 has the full list). "V2:n" is a line of run 2's report before the merge (the corrected base keeps run 2's line numbers); "V1:n" is a line of run 1's report.

### Change M-00: Provenance header, title, status and Merge Notes
- **Status**: Applied (E3 wrote it; E4 placed it and corrected the debate numbers)
- **Source**: new, `partials/merge-stage/new-blocks/M00-merge-notes.md`
- **Target**: lines 1-3 (provenance header: the skill's three lines first), 5-7 (M-00 Source comment and title), 18-76 (`## Merge Notes`)
- **Before**: base title "Technical Research Report: Unified Central Review Panel (run 2)"; E3's notes carried the older numbers (218 resolved, 93.2% / 95.7%, 10 split, 7 artefacts, tally 26 / 130 / 62, tiebreaker 130 vs 26) and a paragraph saying the matrix mis-records C-053, C-056, C-065 and S-039
- **After**: title "Technical Research Report: Unified Central Review Panel (merged from run 1 and run 2)"; authoritative numbers from the regenerated `partials/scoring-matrix.md` and `partials/matrix.json`: 234 points, 220 resolved (94.0% strict; 96.6% with the both-open points; 82.5% after Round 1), 6 both-open (X-040, X-056, X-058, C-060, X-041, X-057), 8 still split: 3 label disputes on the core shape (C-005, C-076, X-051; run 1 advocate BOTH/MERGE, run 2 advocate V2) and 5 Medium/Low rows (C-053, C-065, S-044, C-014, C-025) with each advocate's position and its source line (`partials/r1-advocate-V1.md:247, 249, 254, 259, 262`; `partials/r1-advocate-V2.md:94, 96, 101, 109, 279`); tally Variant 1 33, Variant 2 123, Both 64; tiebreaker 123 vs 33 with 64 Both; E3's caveat paragraph removed; the stale first line of `partials/consensus-summary.md` ("224 of 234 = 0.957", "10 points still disputed") is named with the regenerated figures (220; 226 = 0.966 in `partials/convergence-r2.md`; 8 split)
- **Provenance tag**: `<!-- Source: new text — merged per Change #M-00 -->` (title) and `<!-- Source: new text — merged per Change #M-00 (Merge Notes) -->`
- **Validation**: checks 1, 3, 15 PASS (no stale number in new text: `218 of 234`, `93.2%`, `95.7%`, `10 split`, `7 artefacts`, `130 of 234`, `62 needed`, `run 1's 26`, `0.93162` all absent)

### Change M-01: Status wording of the base title block
- **Status**: Applied (E1: V2:5; E4: title line V2:1 replaced by the M-00 title)
- **Source**: base V2:1-9. **Target**: lines 9-16
- **Before/After**: V2:5 "24 codebase + 4 web research (+ 12 scope slices)" -> plan wording naming both runs' research files; metadata lines V2:3-6 kept
- **Provenance tag**: `Base (original, modified) — M-01: research-files line covers both runs`
- **Validation**: PASS (check 3)

### Change M-02: Baseline and Conventions addendum
- **Status**: Applied (E3 text; E4 placed it before the `---` that closes Baseline, so it stays inside the section)
- **Source**: new, `M02-baseline-addendum.md`. **Target**: lines 253-265
- **Content**: E2 pins (`6c09843` vs `4a22d74`, 4 commits), `e2f2ac268` 7 commits later, code identical at `792cf8c52`, `50d4d2b9d`, `ad8f57560`, `origin/master` `d4d1662a8` 3 commits past merge-base `d2d8a2d16`, pins on `origin/master`, citation-form rule
- **Provenance tag**: `Source: new text — merged per Change #M-02`
- **Validation**: PASS; the duplicate at V2:108 was reduced to a pointer (edit (b), see M-24 item 9)

### Change M-03: `### 2.10 Run 1 current-state material`
- **Status**: Applied (E2). **Source**: V1:108-129, 131-238, 279-435 (287 lines carried). **Target**: lines 1258-1552
- **Before/After**: ids prefixed `R1-`; legend line added under V1:108-129; M-25 corrections at V1:133, 201, 204, 305 (caption note at V1:319), 381, 410
- **Provenance tag**: `Variant 1, Section 2 (lines 108-129, 131-238, 279-435) — merged per Change #M-03; ids prefixed R1-`
- **Validation**: PASS (checks 3, 4, 14)

### Change M-04: `### 3.6 Run 1 target-state material`
- **Status**: Applied (E2). **Source**: V1:483-492, 494-577. **Target**: lines 1673-1774
- **Lead**: base delta table governs; run 1's superset core is the recorded one-engine alternative; both advocates' positions on C-005, C-076, X-051
- **Validation**: PASS

### Change M-05: `### 4.7 Run 1 gap rows`
- **Status**: Applied (E2). **Source**: V1:580-733. **Target**: lines 2087-2244
- **Lead**: counts 145 vs 148 rows with units, severity differences (Appendix C X-011 to X-019), run 2's rule governs; M-25 unit notes at V1:616, 624, 716
- **Validation**: PASS

### Change M-06: `### 4.8 Run 1 contradictions and track coverage`
- **Status**: Applied (E2). **Source**: V1:735-780. **Target**: lines 2246-2296
- **Note**: the lead points at 8.4 for the R1-M1..R1-M4 steps (the plan text said "see M-20"; E2 log item 3)
- **Validation**: PASS

### Change M-07: `### 5.6 Run 1 external findings`
- **Status**: Applied (E2). **Source**: V1:784-1153. **Target**: lines 2899-3270
- **Validation**: PASS (High U-064, U-065, U-066, U-068 found)

### Change M-08: `#### 6.13.0 Disposition of run 1 conflicts`
- **Status**: Applied (E3 table; E4 inserted it at E2's marker as the first block inside 6.13 and corrected three rows)
- **Source**: new, `M08-disposition-table.md`. **Target**: inside 6.13 (lines 4702 onward)
- **Before/After (E4)**: R1-C-06 "the matrix records Variant 2 (cluster CL-04), but both advocates give Variant 1" -> "C-056 Variant 1: both advocates give Variant 1"; R1-C-15 "the matrix records Variant 2 (cluster CL-02)" -> "unresolved split in the matrix (run 2 advocate: Variant 2, its CL-02 cluster verdict)"; R1-C-16 "the matrix records Variant 2 (cluster CL-04)" -> "unresolved split in the matrix". Every other verdict cited in the 20 rows was re-checked against `partials/matrix.json` (C-051, X-002, X-038, C-052, C-059, C-054, C-034, C-057, C-083, X-010, C-082, X-050, X-009, X-045, C-058, C-066, C-063, C-085, C-061, C-090, X-042, C-055, C-079, X-046, C-073, C-093, C-084, X-043, X-054, C-062, C-067, C-064, X-044, C-070, C-092) and agrees
- **E3 corrections to the plan's guidance** (from `E3-log.md`): R1-C-03 (C-059 Both added), R1-C-06, R1-C-08 (C-082, X-050 cited), R1-C-12/13/14/18 (R25-INV-005, -030, -006 added), R1-C-15, R1-C-16, R1-C-20
- **Provenance tag**: `Source: new text — merged per Change #M-08`
- **Validation**: PASS (checks 3, 12)

### Change M-09: `### 6.13 Run 1 conflict blocks`
- **Status**: Applied (E2). **Source**: V1:1155-2807 (1,653 lines). **Target**: lines 4702-6389
- **Head note**: run 1's labels are its own; X-052; ordering words are run 1's recommendation. M-25 read-only correction at V1:2332 and a correction paragraph after V1:2381
- **Validation**: PASS (U-086, U-087, U-088 found)

### Change M-10: `### 7.0.2 Status of the 15 adjudicated outcomes`
- **Status**: Applied (E3 text; E4 inserted it after the 7.0.1 block, before the base heading `### Rationale: the 11 decision axes`)
- **Source**: new, `M10-status-table.md`. **Target**: lines 6456-6478
- **Content**: 15 rows; C-01 Open; C-04, C-09, C-11, X-14 Changed (OPEN); others Unchanged with notes. E3 corrected the plan's C-04 cell (steps R1-M3-03..R1-M3-07, not an ENS range) and added caveats on C-05, X-15 and C-03
- **Validation**: PASS

### Change M-11: `### 7.4 Run 1 recommendation and architecture (recorded alternative)`
- **Status**: Applied (E2). **Source**: V1:2809-3098. **Target**: lines 7086-7378
- **Validation**: PASS (U-102 exposure list found: `R1-X14`, `R1 7.2`)

### Change M-12: Section 8 retitle and lead
- **Status**: Applied (E1). **Source/Target**: V2:4234 (heading), V2:4236 (lead)
- **Before/After**: "## 8. Value Inventory and Inputs for a Later Plan" -> "## 8. Value Inventory, Migration and Value-Capture Content, and Inputs for a Later Plan"; lead keeps "no roadmap, no branch plan, no PR plan, no risk register, no estimate and no schedule" for what the document adds
- **Note**: the heading carries a trailing provenance comment; the ToC script strips HTML comments from heading text before building entries and slugs
- **Validation**: PASS (checks 1, 16)

### Change M-13: Keep V2 8.1 and 8.2; pin the inventory pointer
- **Status**: Applied (E1). **Target**: V2:4280
- **After**: the 5,950 rows live in the synth-08 file committed at `ad8f57560`; pointer `ad8f57560:<path>` (R25-INV-023); Q-35 note
- **Validation**: PASS (U-110 token `synth-08-value-inventory` found)

### Change M-14: `### 8.3 Run 1 value inventory (698 rows)`
- **Status**: Applied (E2; E4 added two X-025 notes found by the validation re-scan)
- **Source**: V1:3105-3821. **Target**: lines 7837-8591
- **Before/After (E4)**: rows R1-V-043 and R1-V-098 kept "3 of 3 slots" (the same fact M-25 corrected at V1:204 only); E4 appended "[corrected per Appendix C X-025: 3 of 4 Qwen runs timed out; a 4th finished]" and the tag `Variant 1 (modified) — E4, M-30 re-scan: X-025 note` (rule 8: the verified value wins, the other is shown)
- **Validation**: PASS (check 14 X-025)

### Change M-15: Translation table for run 1 destinations
- **Status**: Applied (E3 table; E4 inserted it at E2's marker in 8.3, immediately before the inventory rows)
- **Content**: one row per run 1 destination with row counts; one no-counterpart row (Calibration); marked `[derived from the two cited tables; not a finding of either report]`
- **Validation**: PASS

### Change M-16: `### 8.4 Run 1 migration content`
- **Status**: Applied (E2). **Source**: V1:3822-3908, 3910-4030. **Target**: lines 8593-8800
- **Before/After**: V1:3829, 3860, 3879, 3897 (`**Dependencies:**`) deleted; V1:3830, 3861, 3880, 3898 moved to 8.6; status column added from the fault-finder enumeration: 13 CONFLICTS, 14 PARTLY COMPATIBLE, 21 COMPATIBLE (E2 counts 13/14/21)
- **Validation**: PASS (check 5: four lines absent; check 6: 48 step ids, one status each, counts CONFLICTS 13, PARTLY COMPATIBLE 14, COMPATIBLE 21)

### Change M-17: `### 8.5 Run 1 no-regression gates`
- **Status**: Applied (E2 block; E4 the base half)
- **Source**: V1:4031-4056. **Target**: lines 8802-8831; base C18 row (V2:4447, merged line 7595)
- **Before/After (E4, edit (a))**: run 2's C18 rewrite list gains "Merge addition: the rewrite list also takes `tests/review/test_review_ledger.py:299-304` and `:468-472`, which run 1's gate R1-G2 pins as "must NOT change" only under run 1's verdict design, which is not adopted (8.5; R25-INV-026)."
- **Provenance tag**: `<!-- Source: Base (original, modified) — M-17: run 1 R1-G2 pins, R25-INV-026 -->`
- **Validation**: PASS (check 10: `no-regression` in 8.2(b) and 8.5)

### Change M-18: `### 8.6 Run 1 persisted-format compatibility and rollback rules`
- **Status**: Applied (E2). **Source**: V1:3830, 3861, 3880, 3898. **Target**: lines 8833-8849
- **Content**: the four lines plus the R25-INV-003 correction and both versions (V2 A-9 `review-ledger/1`; run 1 `min_writer` plus `/2`)
- **Validation**: PASS

### Change M-19: `### 8.7 Run 1 branch-structure constraint and facts`
- **Status**: Applied (E2). **Source**: V1:4057-4061. **Target**: lines 8851-8861
- **Before/After**: heading replaced; "3 commits ahead" -> "5 commits past merge-base `d2d8a2d16` (`origin/master` `d4d1662a8` is 3 commits past the merge-base)"; layout table V1:4063-4069 dropped; constraint stated for both reports and for the owner's prefix `feat_review-panel/<name>`
- **Validation**: PASS (check 9: phrase in base C4 and in 8.7, owner prefix in 8.7)

### Change M-20: `### 8.8 Run 1 risk inputs and integration checklist`
- **Status**: Applied (E2; E4 edit (c))
- **Source**: V1:4071-4101, 4103-4122. **Target**: lines 8863-8917
- **Before/After**: V1:4115 (PR-process item) dropped; V1:4120 clause "and mark the steps that wait on each" dropped; V1:4116 "the chosen branch layout of 8.4" -> "the branch names (see 8.7 constraint)"; E4 fixed the verb: "Confirm the branch names (see 8.7 constraint) does not create both" -> "... do not create both"; tag kept as `Variant 1 (modified)` and now says "(plan text; verb agreement 'do not create' fixed by E4)"
- **Validation**: PASS

### Change M-21: `### 9.11 Run 1 open questions` and `### 9.12 Open items raised by the compare debate`
- **Status**: Applied (E2: 9.11, V1:4125-4387, lines 9079-9346; E3: 9.12, lines 9348-9375)
- **Content**: 9.12 Part A: R25-INV-003, -006, -018, -024 with -029, -027, -028; Part B: claim cut, exit code 12, distinctness default, post-gate engine, quorum denominator, per-slot keys, line-number base
- **Validation**: PASS (check 14: all Appendix C OPEN rows appear in 9.12 or as the X-051 label split)

### Change M-22: `### 10.A Run 1 evidence trail` and `### 10.B Compare artifacts`
- **Status**: Applied (E2: 10.A, V1:4389-4476, lines 9602-9691; E3: 10.B, lines 9693-9730; E4 changed one pointer in 10.B)
- **Before/After (E4)**: "(see Merge Notes (a) on the inheritance artefacts in `r2-state.json`)" -> "(see Merge Notes (a) on cluster-label inheritance and the advocates' exception lists)"
- **Validation**: PASS

### Change M-23: Carry V1 unique content not placed above
- **Status**: Applied (check by script, E4)
- **Result**: all 62 High U rows of `diff-analysis.md` (V1 20, V2 42) have their mapped token in the merged file; U-099 needs only the git constraint (layout table dropped on purpose)
- **Validation**: PASS (check 11)

### Change M-24: In-place corrections to base text
- **Status**: Applied (E1: 80 edits on 78 lines; E4 replaced the item 9 note, edit (b))
- **Per item** (from `E1-corrections-log.md`; before/after texts in `e1-edits.json`):
  - item 1 KeyError path: edited V2:940, 1177 (note), 1236, 1334, 1437, 2177, 3329, 3411, 3487, 3637, 3666, 3882, 4508, 4677, plus extra sites 2226, 3636; kept 545 and 4312 (plan)
  - item 2 withdrawn arXiv 2606.19544: V2:1647, 1648 (two edits, incl. the EMNLP 2025 tier correction of 2510.27106), 1655, 2044, 2072, 2078, 2829; 1650 and 2049 not edited (rest on 2510.27106)
  - item 3 calibrator: V2:891, 1033, 3474; V2:3323 edited narrower than the plan (the `[UNVERIFIED]` tag kept because it also covers the vocabulary claim; the calibrator part is marked CODE-VERIFIED)
  - item 4 `tests/pr_submit` 47 test files: V2:710, 1202, 1335, 2973, 3357, 3496, 3735, 3804, 4479, 4593, plus V2:3797 (extra site the plan said not to edit; its "50 files" is wrong under every unit checked; the 47 kept)
  - item 5 read-only mechanism: V2:1728, 1792, 2054, 3517, 3640, 3658, 4085 (the base never claimed `--allowedTools` restricts tools; the missing MCP / `--strict-mcp-config` part was added)
  - item 6 engine-A keys: V2:179, 892, 1255, 1430, 2703, plus extra 2507, 4503
  - item 7 rf-* census: V2:683, 1341, 2953, 3736, 3820, 3892, 4602, plus extra 3387
  - item 8: V2:1331 "(6)" -> 5 lines, 7 occurrences
  - item 9: E1 inserted the note at V2:108; E4 replaced it by "[Compare-merge baseline note: `origin/master`, HEAD `ad8f57560` and the later E2 commit `e2f2ac268` are stated once, in the merge addendum at the end of this section.]" and retagged it `Base (original, modified) — M-24 item 9: pointer to the merge addendum (E4 replaced E1's inline note, which repeated the M-02 addendum)`; Appendix E row M-24.9 updated to say so
  - item 10: V2:215, plus extra 1282, 2370
  - item 11: V2:216, 874
  - item 12: V2:154, 845
  - item 13: V2:874, 1027, 1368, 3743
  - item 14: V2:3516, 3638, worded "narrows the fail-open path but does not close it" (the word "closes" is not used)
- **Provenance tag**: `Base (original, modified) — <item>` at the end of each changed line
- **Validation**: PASS (check 14: no `195 of 1,398`, no `reflect's 5 [UNVERIFIED]`, `(6)` corrected, no uncorrected `50 ... files`, every base 2606.19544 line marked, only the two kept KeyError lines untagged)

### Change M-25: In-place corrections inside carried run 1 blocks
- **Status**: Applied (E2; E4 extended the X-025 note to two inventory rows, see M-14)
- **Edits** (from `E2-extraction-log.md` section 10): V1:133, 201, 204, 305 (fence) with caption note at V1:319, 381, 410, 616, 624, 716, 2332, 2381 (correction paragraph), 2443, 2976, 3567, 3790, 4038 (M-17), 4061 (M-19), 4092, 4116 and 4120 (M-20), 4348
- **Not corrected (logged by E2)**: V1:3843 (R1-M1-10) and V1:3855 (R1-M1-22) name `--allowedTools` inside 8.4 Details cells, which M-16 forbids editing; V1:4170 (R1-Q-35) names it as an open question
- **Validation**: PASS (every carried `43 call sites` has the unit note; `same_defect` branch present; X-025 and X-026 clean outside quotes)

### Change M-26: Table of Contents rebuild
- **Status**: Applied (E4, `e4_assemble.py`)
- **After**: 146 entries (18 H2 other than the ToC itself, 98 H3, 30 H4 under 6.13 and 7.4), same list style as the base; HTML comments stripped from heading text; slugs built like GitHub (lowercase, spaces to hyphens, punctuation removed, `-n` suffix for repeated headings). The slug function was checked against run 2's own ToC: it reproduces all 88 entries of V2:12-99. `---` kept after the ToC.
- **Validation**: PASS (check 16: every entry matches exactly one heading; every H2 and H3 has an entry)

### Change M-27: Heading-level and anchor repair; Appendix F
- **Status**: Applied (E2: 167 run 1 headings demoted with the `R1 ` prefix where they start with a run 1 number; E4: Appendix F)
- **After**: no V1 H2 carried; Appendix F.1 lists the 39 merged parts with their output line ranges and sources; F.2 maps run 1 section numbers to merged headings (17 section-level rows plus one row per carried `R1 n.m` heading)
- **Validation**: PASS (checks 1, 2: one H1, no level gaps; H2 set exactly Merge Notes, ToC, Baseline, 1-10, Appendix A-F)

### Change M-28: Appendix C, contradiction register
- **Status**: Applied (E3, `e3_appendix_c.py`). **Target**: lines 9764-9838
- **Validation**: PASS (63 rows X-001..X-063; every "debate:" verdict equals the regenerated `partials/matrix.json`; every "Where handled" section number resolves to a heading)

### Change M-29: Appendices D, E (and F, see M-27)
- **Status**: Applied (E3, `e3_appendix_d.py` and hand-written E; E4 edits)
- **Before/After (E4)**: the generator marker `<!-- APPENDIX-E -->` replaced by `---` and the Source comment of Appendix E; R25-INV-016 carrier "(218 resolved; ...)" -> "(220 resolved; the 6 both-open points counted apart, 226 with them)"; M-24.9 "Applied by" cell updated (edit (b)); new `### E.3 Promoted shared assumptions not named elsewhere` with 14 rows (A-008, A-012, A-018, A-019, A-024, A-027, A-037, A-038, A-041, A-052, A-055, A-056, A-057, A-059), verdicts read from `partials/matrix.json`
- **Validation**: PASS (check 8: all 18 promoted assumptions addressed)

### Change M-30: Final validation and merge log
- **Status**: Applied (E4, `e4_validate.py`; this file)
- **Validation**: 16 checks PASS, 0 FAIL (one failure in the first run, the X-025 re-scan, was fixed in M-14; two first-run failures were false positives of the check itself and the check was narrowed: a quoted wrong value in Appendix C or inside an HTML provenance comment is not a stale statement, and `DOC-50` / `:50-62` are not counts)

## Plan departures and open points

- **Plan review escalation.** The plan review hit the limit of two fix cycles and three reviews; the last blocking finding R3-B1 (closed-item rename coverage, 103 tokens) was fixed WITHOUT a fourth review. The validation of the closed-item prefixes was therefore mandatory: check 4 PASS (no `Closed item R1-C-`, no `GQ:R1-C-`, no `GQ R1-C-`; 107 `R1-CLS-nn` tokens in the merged file).
- **E1, V2:3797 edited** although the plan named it as a locator hit not to edit: its "(50 files, 47 `test_*.py`)" is wrong under every unit checked (49 tracked `.py`, 47 `test_*.py`, 91 tracked files); annotated, 47 kept.
- **E1, V2:3323 kept `[UNVERIFIED]`** with a note: the tag covers both the vocabulary claim and the calibrator claim; only the calibrator part is marked CODE-VERIFIED.
- **E1, item 5 reality**: the base never says `--allowedTools` restricts tools (it says the opposite at V2:1725, 1728, 2054); its error is incompleteness (MCP servers stay loaded), so only the "add" part of item 5 was applied.
- **E1, item 14 wording**: "this narrows the fail-open path but does not close it" instead of the plan's "narrows, not closes", to honour the plan's own ban on the word "closes".
- **E1, extra sites** beyond the plan's lists: item 1 (2226, 3636), item 6 (2507, 4503), item 7 (3387), item 10 (1282, 2370).
- **E2, EXTRA_PINS at V1:3736**: four more closed-item tokens (C-01, C-02, C-04, C-12 in row R1-V-614) renamed `R1-CLS-nn` beyond the plan's 103 (107 in total); without it they would have become conflict ids next to `R1-CLS-25`.
- **E2, R1-M4-01 and R1-M4-03 cells**: R25-INV-027 names no run 2 outcome id for these CONFLICTS rows; the cells say so ("conflicts with run 2's adopted design (R25-INV-027 names no outcome id: the step edits `fsm.py`" / "`severity_router.py`") instead of inventing an id.
- **E2, other choices**: M-06 lead points at 8.4 (plan said "see M-20"); residual mentions of the dropped layouts at V1:4061 and V1:4086 kept as carried text; no lead added to 10.A (plan prescribes none); `--allowedTools` in two 8.4 Details cells not corrected (M-16 forbids editing Details cells); the main id pass made 7,686 replacements, 37 range rewrites and 103 (+4) closed-item renames; spot check of 20 replacements in `E2-extraction-log.md` section 7.
- **E3, cell corrections**: M-08 rows R1-C-03, -06, -08, -12, -13, -14, -15, -16, -18, -20 differ from the plan's starting guidance after row-by-row verification; M-10 cells C-04 (step range R1-M3-03..R1-M3-07 instead of an ENS range), C-05, X-15, C-03 corrected or extended; M-02 corrects the plan's M-24 item 9 attribution (C14 and C26 cite only `test_worker_contract.py`; `pragmatic.md` is the X-15 basis); R25-INV-022 has no carrier ("Appendix D only").
- **E3 caveat on the matrix removed (E4)**: E3 reported that the matrix recorded C-053, C-056, C-065 and S-039 by cluster inheritance. The matrix was regenerated after E3 wrote its files and now applies the advocates' exception lists (C-056 and S-039 Variant 1; C-053 and C-065 unresolved splits); the caveat paragraph was removed and the three affected M-08 cells were corrected.
- **E3 duplication resolved (E4, edit (b))**: E1's item 9 note at V2:108 repeated the M-02 addendum; the note is now a one-line pointer.
- **E4, M-17 C18 addition (edit (a))**: done in the base (E2 log item 4 had flagged it as the base executor's task).
- **E4, M-20 grammar (edit (c))**: "does not create" -> "do not create".
- **E4, X-025 notes on R1-V-043 and R1-V-098**: an extension of M-25 found by the validation re-scan (rule 8 applied as a note; run 1's text kept).
- **E4, E.3 added to Appendix E**: 14 promoted assumptions were not named by id anywhere in the Merge Notes, Appendices C-E or 9.12; one line each was added (validation instruction).
- **E4, placement choices**: the M-00 Source comment follows the three provenance lines; an extra Source comment precedes `## Merge Notes` and one precedes each base segment (`Base (original), V2:a-b`); M-02 sits before the `---` that closes Baseline; `---` separators precede the ToC and Appendices C, D, E and F.
- **Open, not resolved by the merge** (carried in the document): the 7 HIGH UNADDRESSED invariants (9.12 Part A), the 6 both-open points and 8 split points (Merge Notes (a)), the owner decisions of 9.12 Part B. The first line of `partials/consensus-summary.md` still states 224 / 0.957 / 10 disputed; the Merge Notes name the regenerated figures. The collected-test counts (651, 353, 2258) were not re-collected by any executor (fault-finder row 5).

## Post-Merge Validation

Full output: `partials/merge-stage/E4-validation-report.md`.

### Structural integrity
- H2 sections: 19, exactly Merge Notes, Table of Contents, Baseline and Conventions, 1 to 10 in order, Appendix A to F: PASS
- Heading levels: one H1; no level gaps (headings by level: H1 1, H2 19, H3 98, H4 194, H5 115): PASS
- Every block carries a Source comment; the three provenance lines are lines 1-3: PASS
- Table of Contents: 146 entries, each matching exactly one heading; every H2/H3 listed; `---` after it: PASS
- Closed-item prefixes (R3-B1): PASS. Deleted `**Dependencies:**` lines absent: PASS. 48 step ids with a status (13 / 14 / 21): PASS
- Leftover insertion markers, double prefixes (`R1-R1-`, `R1-R25-`), duplicate `origin/master` note: none

### Internal references
- 72 `Section n.m` / `Appendix X` references in new text, 0 unresolved; 24 merged-numbering pointers (2.10, 3.6, 4.7, 4.8, 5.6, 6.13, 6.13.0, 7.0.2, 7.4, 8.3-8.8, 9.11, 9.12, 10.A, 10.B, E.1-E.3, F.1, F.2) all resolve: PASS
- Appendix C "Where handled" section numbers all resolve: PASS

### Contradiction re-scan against Appendix C
- X-021 (`195 of 1,398` gone), X-025 (carried "3 of 3 slots" carries the correction), X-026, X-030/X-048, X-017, X-031, `tests/pr_submit` count, X-036 (every base 2606.19544 line marked; run 1's 5.6 line states its own exclusion), X-020/X-049/X-053 (only V2:545 and V2:4312 untagged, as planned), X-022/X-029/X-061 (unit note on every carried "43 call sites"): PASS
- Appendix C verdicts equal the regenerated matrix for all 63 rows; the 6 open rows (X-040, X-041, X-051, X-056, X-057, X-058) are carried as open items (9.12) or as the label split: PASS
- 18 promoted shared assumptions: A-002, A-006, A-036, A-058 in Appendix D; all 18 in Appendix E.3 or D: PASS

### Other checks
- Git-ref constraint: phrase present in base C4 and in 8.7 (twice); `feat_review-panel/<name>` in 8.7: PASS
- `no-regression`: run 2's 8.2(b) and run 1's 8.5 both contain it: PASS
- High U rows: 62 of 62 have their token (V1 20, V2 42), plus ENS-4, MS-24, R1-D1, R1-C-14, R1-V-001, R1-M1-01, G-133, Appendix A pointer, C29, G27, AE-15: PASS
- Roadmap / schedule / PR-plan words in the 394 new-text lines: 6 hits, all justified (5 are the Merge Notes (h) scope sentence "adds no roadmap, no branch plan, no pull-request plan and no schedule"; 1 is 8.7's lead naming the dropped layout table as a branch plan; the 9.12 cell quoting run 2's "named, not scheduled" is a negation): PASS
- Stale debate numbers in new text: none: PASS

### Counts
- 10,109 lines; 2,629,571 bytes; 8,128 `R1-` prefixed tokens; 107 `R1-CLS-nn`; 172 `R25-INV-nnn`
- Lines per H2 section (start line, lines): Merge Notes 20, 62; ToC 82, 153; Baseline 235, 36; 1. 271, 15; 2. 286, 1,270; 3. 1556, 222; 4. 1778, 522; 5. 2300, 974; 6. 3274, 3,119; 7. 6393, 989; 8. 7382, 1,539; 9. 8921, 458; 10. 9379, 357; Appendix A 9736, 4; B 9740, 28; C 9768, 76; D 9844, 45; E 9889, 82; F 9971, 139

## Summary

- Changes applied: 31 of 31 (M-00 to M-30), by four executors; E4 made 22 recorded edits (`e4-edits.json`): the three edits left to it ((a) C18 pins, (b) V2:108 pointer, (c) M-20 grammar), 12 debate-number corrections (d) across M00, M08, M29 and M22b, the Appendix E marker, and 4 X-025 note edits found by validation; plus Appendix E.3 (14 rows)
- Validation: PASS on all 16 checks
- Structural issues: none
- Document status: `partial` (7 HIGH UNADDRESSED invariants carried as open items; 6 both-open and 8 split debate points stated with both positions)
- Merge time: single session, 2026-11-15
