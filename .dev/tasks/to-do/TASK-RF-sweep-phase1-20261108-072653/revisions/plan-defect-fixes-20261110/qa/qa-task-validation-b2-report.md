# QA Report - Task Integrity, B2 Self-Containment Lens (R2 plan-defect fixes)

**Topic:** TASK-RF-sweep-phase1-20261108-072653, revision R2 (F-01 to F-10)
**Date:** 2026-11-10
**Phase:** task-integrity (lens: b2-self-containment)
**Fix cycle:** N/A (fix_authorization false)

**Task file:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (sha256 7b1881237f7aafe7954af9b5e60e0f1bc7912dd43098157b009903fa9910ea77, 3020 lines)
**Baseline:** `revisions/plan-defect-fixes-20261110/baseline/task-before-rev2.md` (sha256 f52e43a5...6855, matches the delta manifest)
**Fix authorization:** false. Only this report was written. Helper scripts lived in `/tmp` and a private `/tmp/ironclaude-batch.*` directory (removed by trap).

(Report is written incrementally; verdict at the end.)

## Part A - Mechanical pass over the whole file (prompt step a)

Method: `uv run python -I /tmp/b2_a10_mech2.py <file>` on the edited file and on the baseline. A field is a line starting `  - **<Name>**:`; continuation lines are any non-blank lines that follow it before the next field or blank line.

| Measure | Edited file | Baseline |
|---|---|---|
| Item headers | 355 (137 ticked) | 355 (137 ticked) |
| Items with Context / Action / Output / Verification / Completion gate each exactly once, in that order | 355 / 355 / 355 / 355 / 355 | 355 each |
| Nested checkboxes inside item bodies | 0 | 0 |
| Fields that span more than one physical line | 2 (7.16 Context = 10 lines, 7.17 Action = 5 lines) | same 2 |
| Blockquote prompt block between Action and Output | 14.48 (9 lines) | same |

Result: all 355 items carry the five B2 components in order. The statement "each a single physical line" is not true for two items, but both are byte-identical to the baseline, are not in the 64 changed labels, and were not touched by this revision (see note N-1). The 72 changed lines are each still one physical line, and the line count is unchanged at 3020 (3021 in the preservation JSON counts the final empty split element).

Preservation facts re-checked independently of `preservation-check.json`: `uv run python -I /tmp/b2_a10_ticked.py` compared all 355 item blocks. 137 ticked blocks changed: none. Ticked/unticked state flips: none. Unticked blocks changed: 64. Spot check of 1.1, 5.2, 6.3, 7.8, 7.9: identical to baseline.

## Part B - Every changed line (prompt step b)

Method: `diff` of baseline vs edited gives 72 changed lines; `/tmp/b2_a10_diff.py` produced a word-level diff of each (read in full, 1084 lines, in chunks of at most 150). The 72 lines break down as follows.

| Group | Lines | What I checked | Result |
|---|---|---|---|
| Uniform Context sentence reword (F-06) | 58 Context lines (all labels in the manifest except 7.10, 8.19, 10.5) | `/tmp/b2_a10_ctx.py` applies the one substitution to each baseline line and compares with the edited line | 58 of 58 equal the substitution; 0 mismatches. The literal `not an implemented exception` remains only in 7.10 (line 1209). New sentence is self-contained and repeats no literal. |
| OQ lens wording (F-01b) | 12 lens Contexts 7.21-7.28, 7.31, 7.32, 7.35, 7.36 | same script | 12 of 12 now read "the eight prerequisite decision records `...OQ-[1-8]-*-decision.md` (OQ-1 to OQ-8) plus any OQ-17 or OQ-18 decision record in that folder that item 7.17 wrote". Path spelled exactly. |
| 7.10 Action + Output | 1210, 1211 | read the full new lines | Restated clauses match addendum lines 15-21 in substance (one quote drift, see N-3). Heading string, result-file path and "written first, before the style edit" are in the item. Branch pointer is restated in the item itself; "(see the note appended at the end of this task)" is extra support only. |
| 7.20 Action | 1293 | full line read; commands run on synthetic file sets (Part C) | All new commands carry an expected value. Two path/reference defects, see B2-1. |
| 7.22 / 7.25 Action | 1307, 1328 | full lines read | "plus one row for each resolved OQ-17 or OQ-18 decision file that exists" and "(an absent optional file needs no row)": measurable, self-contained. |
| 7.30 / 7.34 Action | 1363, 1391 | full lines read; every new path tested for existence (`/tmp/b2_a10_paths.py`) | sha256 record-before / re-run-after is embedded with four full paths that exist (addendum, R1 BUILD-REQUEST, R2 BUILD-REQUEST, OQ-6 record) and a named log file that matches the item Output. One pointer defect, see B2-2. |
| 8.19 Action, 10.5 Context | 1551, 1812 | full lines read | "the recorded GQ-63 decision governs only the sweep skill's chat reply, not the report file layout" / "layout follows the OQ-4 (GQ-35) record". Self-contained. |
| 11.4 Action, Verification | 1980, 1982 | full lines read, compared with baseline | Presence-not-absence rule embedded; repair routes named (11.1/11.3 in place; style defect HALT with a named blocker). 11.14 does follow 11.4, so "11.14 cannot run before this item is complete" is true. |
| 13.1 Action, Verification | 2265, 2267 | `/tmp/b2_a10_q131.py` compares the quoted bullet with DESIGN line 716 | Quote equals DESIGN row R2 byte for byte (EQUAL: True). Verification uses `grep -nF`, expects one line, line 404 after the never-workers bullet and before the Orca-creates bullet. Simulated insertion into a copy of HOW-WE-WORK.md gave `404:` and 0 for the other greps (Part C). |
| 14.19 Action | 2572 | full line read | "OQ-1 to OQ-8, plus any recorded OQ-17 or OQ-18 decision" embedded in the lens prompt. |

Format hygiene on all 72 lines (`/tmp/b2_a10_balance.py`): backtick parity, parenthesis balance, quote parity, double spaces, trailing space, space-before-punctuation: no new anomaly in any line. Forbidden-token scan of all new text ("see above", "as above", "previous item", TBD, TODO, FIXME, UNVERIFIED, CODE-CONTRADICTED): no hit. Pointer-to-item scan of all new text: hits only the two defects below plus explanatory mentions of item 7.17 (which carry the full paths).

Paths introduced by the edit (`/tmp/b2_a10_paths.py`): `OQ-[1-8]-*-decision.md` (glob), `OQ-17-cursor-template-decision.md`, `OQ-18-run-current-json-decision.md` (both spelled as in item 7.17 line 1270), `step-7.10-style-exception.md` (created by 7.10 itself), `pragmatic.md`, `design-addendum.md`, R2 `BUILD-REQUEST.md`, `OQ-6-GQ-63-done-next-decision.md` (the last four exist). The OQ-17/OQ-18 and step-7.10 files are absent today, which is correct: later items create them.

## Part C - Fix by fix, F-01 to F-10 (prompt step c)

Authoritative text: `merged-verdict.yaml` findings F-01 to F-10 (read lines 69-450). TL = the task file. Verifiers were run in one private batch script (`/tmp/ironclaude-batch.*`, 27 read-only commands, BATCH_OK) plus a synthetic-file simulation (4 file sets, a copy of HOW-WE-WORK.md, a sample result file), none of which wrote into the repository.

| Id | `recommendation.fix` present in the edited lines? | Verifier (expected value) | Actual output | Status |
|---|---|---|---|---|
| F-01 HIGH | Yes. (a) `OQ-[1-8]-*-decision.md` glob + per-file OQ-17/OQ-18 check with skip-if-absent on 7.20, 7.30, 7.34 (15 lines carry the glob). (b) 12 lens Contexts + 14.19 reworded. (c) second grep has an expected value for OQ-17/OQ-18 on 7.20, 7.30, 7.34. 7.22 "seven plus one per resolved optional decision", 7.25 same rule. 7.30/7.34 fixers may correct `owner-decisions.md` (that sentence was already in the item). | "Run the new count and per-file checks against three file sets: eight alone, eight plus one, eight plus both; all PASS; an unresolved required record FAILs" | Simulation: set A (8) count 8, both optional files SKIP; set B (8+OQ-17) count 8, OQ-17 = 1, OQ-18 SKIP; set C (8+both) count 8, both = 1; set D (OQ-3 PENDING) count 7 = FAIL. `does NOT authorize adoption` per-file counts: OQ-1 0, OQ-2..7 1, OQ-8 0, OQ-17/18 1. Static: `grep -c 'the eight decision records' TL` = 0; `grep -c 'plus any OQ-17 or OQ-18 decision record in that folder' TL` = 12; `grep -c 'OQ-\[1-8\]-\*-decision.md' TL` = 15. | PASS |
| F-02 HIGH | Yes (13.1 lines 2265, 2267): DESIGN:716 wording, `grep -nF`, placement check kept, ticked 5.2 untouched. | `grep -nF 'The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes' HOW-WE-WORK.md` prints line 404; `grep -n 'The coordinator sweeps on every wake'` on TL prints only line 776 | TL: only `776` (was also 2265 and 2267). HOW-WE-WORK.md today: no hit and 0 for `sweeps on every wake`, which is expected until item 13.1 runs. Simulated insertion after line 403 of a copy: `404:- **The coordinator runs `/sc:sweep`...`, `sweeps on every wake` 0, WC-14 on the line 0, `src/superclaude` on the line 0, neighbours are the never-workers and Orca-creates bullets. | PASS (later-true part expected) |
| F-03 MED | Yes (7.10 Action 1210): all clauses embedded; "proposed" not copied; no new 11.4 assertion; 11.4 states presence-not-absence. | `grep -n` for `same message`, `Formatting never`, `chat-presentation` hit 1210 | `same message`: 1210 and 1973; `Formatting never`: 1210; `chat-presentation`: 1210 | PASS (see N-3) |
| F-04 MED | Yes. 7.10 Action/Output: dated verbatim quote + supplied report paths, section written first, before the style edit, "a quote written by this executor is a record, not independent evidence". 7.20: command + expected value. | result file has the section; `grep -n` of the header hits; 7.20 has command and expected value | `Execution authorization (verbatim)` appears on 1210, 1211, 1293. Command `grep -c '^## Execution authorization (verbatim)' <file>` (expect 1) gave 1 on a sample file. | PASS for the F-04 text; the extra "must match the owner's words recorded in the revision BUILD-REQUEST.md files" rule is defective, see B2-1 |
| F-05 LOW | Yes (11.4 Verification 1982). Both routes, no "fresh authorization" rule. | `grep -n 're-run this item'` hits 1982 | hits 291, 458, 632, 848, 1008, 1295, **1982**, 2476 | PASS |
| F-06 LOW | Yes (58 Context lines). | `grep -c 'not an implemented exception'` on TL prints 1 | 1 (line 1209, item 7.10); `grep -c 'Pre-7.10 source anchor'` = 58 | PASS |
| F-07 LOW | Yes (7.30, 7.34): four sums before the spawn, hash only the OQ-6 record, re-run after, PASS only if all four unchanged. | `grep -c sha256sum` on TL rises from 4 to 6 | 6 (lines 1363, 1391, 2614, 2642, 2705, 2733) | PASS |
| F-08 LOW | Yes (7.20, 7.30, 7.34). | after 7.10 the command prints 6 (0 before) | Style file today: 0, expected until 7.10 runs. TL lines carrying the command: 1210, 1293, 1363, 1391. | PASS (later-true part expected) |
| F-09 LOW | Yes (7.10 Action opening sentence). | `grep -n 'Phase 7 preamble Branches'` hits 1210 | 1210 only | PASS |
| F-10 LOW | Yes (8.19 Action, 10.5 Context). | GQ-63 scoped to the chat reply, GQ-35 to the layout | `governs only the sweep skill` on 1551 and 1812; old strings `GQ-35 and GQ-63` and `OQ-4 (GQ-35) and OQ-6 (GQ-63) records` now 0 | PASS |

Verifiers that can only be true after later items run (recorded as expected, not as failures): the style-file count of 6 (0 until 7.10), the HOW-WE-WORK.md grep for the new bullet (nothing until 13.1), `OQ-[1-8]` RESOLVED count of 8 (currently 6 OQ files exist, all RESOLVED, until 7.11-7.15), the `## Execution authorization (verbatim)` count of 1 (file absent until 7.10), and the OQ-17/OQ-18 branch (only if item 7.17 fires it).

## Part D - Regression check against the baseline (prompt step d)

Method: `/tmp/b2_a10_regress.py` extracted every backtick span, every `(expect ...)` clause, every quoted string and every sentence of the 72 baseline lines and listed those missing from the edited line. After filtering the uniform Context substitution, each remaining item was read in the full edited line.

| Changed line | Baseline element reported missing | Verdict |
|---|---|---|
| 7.20 (1293) | `grep -l 'status: RESOLVED' ...OQ-*-decision.md \| wc -l` (expect 8) | Kept, glob narrowed to `OQ-[1-8]-*` on purpose (F-01); expected value 8 kept. |
| 7.20 (1293) | `(expect at least 1 for each of the OQ-2 to OQ-7 files ... and 0 for the OQ-1 file ... and for the OQ-8 Run-id file)` | Kept and extended with "at least 1 for each OQ-17 or OQ-18 file that exists". |
| 7.20 (1293) | word "independently" before "evidenced" | Removed on purpose (F-04: an executor-written quote is not independent evidence). |
| 7.22 (1307) | sentence "Check `owner-decisions.md` has seven decision rows and the APPROVED table. Each missing part is BLOCKING." | Still present; the new "plus one row for each resolved OQ-17 or OQ-18 decision file that exists" sits inside it. |
| 7.25 (1328) | "owner-decisions.md matches each file" | Extended to "each of its seven decision files plus each resolved OQ-17 or OQ-18 decision file that exists". |
| 7.30 / 7.34 (1363, 1391) | `grep -l ... (expect 8)` and the `does NOT authorize adoption` expectations | Both kept (glob narrowed, OQ-17/18 added). |
| 8.19 (1551), 10.5 (1812) | "layout follows the recorded GQ-35 and GQ-63 decisions" | Replaced on purpose (F-10). |
| 11.4 Verification (1982) | "fixed in its owning source item or authorized serialized fixer" | Route narrowed on purpose (F-05); see N-4. No command or expected value lost. |
| 13.1 (2265, 2267) | old quoted bullet and old two greps | Replaced on purpose (F-02); the placement check, the `WC-14` and `src/superclaude` checks are kept. |
| 14.19 (2572) | "owner decisions OQ-1 to OQ-8 reflected where they apply" | Extended, not removed. |

No command, expected value, completion gate, output path or HALT/stop clause was dropped by accident. All 72 changes are inside the 85 allowed labels.

## Part E - Tick-marked items (prompt step e)

None changed. `/tmp/b2_a10_ticked.py`: 137 ticked blocks compared with the baseline, 0 differ; header check state flips 0; five spot checks (1.1, 5.2, 6.3, 7.8, 7.9) identical. Agrees with `preservation-check.json` (`completed_items` 137, `pass` true, three frozen hashes `ok`).

## Findings (graded)

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| B2-1 | MAJOR | TL:1293 (item 7.20 Action; Context at TL:1292) | New F-04 check says "the quote must match the owner's words recorded in the revision `BUILD-REQUEST.md` files; ... a mismatch or an empty section is a FAIL". The item names no path for those files. Its Context names only the R1 file `.../chat-output-exception-20261109-133150/BUILD-REQUEST.md`; the R2 path `.../plan-defect-fixes-20261110/BUILD-REQUEST.md` appears only in items 7.30 and 7.34 (`grep -n 'plan-defect-fixes'` on TL: 1363, 1391). The R1 file records only the planning authorization ("authorizes plan revision/checking only", line 15; "user decides execution separately", line 55). The owner's execution-direction words ("Already approved plan is confirmed proceed with implementation", "then execute") are recorded only in the R2 file, line 9. A literal run of 7.20 therefore has no named file in which to find the words it must match, yet FAILs on mismatch. This breaks B2 check 4 (specific paths) and can fail a correct run. | Name the R2 BUILD-REQUEST path (section "Authorization (direct, by the owner)") in 7.20, and say what the quote is compared with when the separate authorization is a later dated owner message supplied with the reports (for example "the BUILD-REQUEST words or the dated owner message supplied with the reports"). |
| B2-2 | MAJOR | TL:1363 (7.30 Action), TL:1391 (7.34 Action) | New text says "for each of the OQ-17 and OQ-18 decision files named in item 7.20 that exists `grep -c 'status: RESOLVED' <file>`". The two file paths are not restated in either item; the executor must open item 7.20 to learn them. This is exactly "points to another item for something the item needs" (B2 check 2). The baseline restated every other path of this re-run list in full; only the new part leans on 7.20. | Write the two full paths (`.../phase-outputs/plans/OQ-17-cursor-template-decision.md` and `.../OQ-18-run-current-json-decision.md`) into 7.30 and 7.34, as 7.20 does. |

Minor notes (never fail the gate, not rechecked in later rounds):

| # | Severity | Location | Note |
|---|---|---|---|
| N-1 | MINOR | TL:1251-1260 (7.16 Context, 10 physical lines), TL:1268-1272 (7.17 Action, 5 lines), TL:2777-2785 (14.48 blockquote prompt), TL:1632 ("exactly as above" in 9.1), TL:1362 and 8 sibling fix items ("the gate inputs listed in Context" inside Context) | Pre-existing, byte-identical to the baseline, outside the 64 changed labels. The "single physical line" premise of the prompt does not hold for 7.16 and 7.17. Not caused by R2. |
| N-2 | MINOR | `delta-manifest.md` row F-03 | "Lines changed" lists 1210 only, but line 1980 (11.4 Action) also changed and is described in the same row. `preservation-check.json` lists 1980. Documentation gap only. |
| N-3 | MINOR | TL:1210 (7.10 Action) | The item puts `"Formatting never authorizes advice the sweep skill prohibits"` in quotation marks as the rule's wording; addendum line 19 and the R2 BUILD-REQUEST read "advice prohibited by the sweep skill". Same meaning, different quoted words; a verbatim copy would differ from the addendum. Use the addendum wording. |
| N-4 | MINOR | TL:1982 (11.4 Verification) | The old route "authorized serialized fixer" was dropped. It is consistent with F-05 and with 11.14 running after 11.4, but a defect inside the new test module itself has no named route (the item still says to log and stop incomplete). |
| N-5 | MINOR | TL:1295 (7.20 Verification, unchanged) | On FAIL it says "return to the owning item and re-run this item". For the new authorization-section check the owning item is ticked 7.10, the retry hazard that F-05 describes for 11.4. Operational question for the qualitative lens, not graded here. |

## Checks

| Id | Check | Result | Evidence |
|---|---|---|---|
| C1 | All 355 items have Context, Action, Output, Verification, Completion gate exactly once, in order | PASS | Part A, `/tmp/b2_a10_mech2.py`: counts 355 each |
| C2 | The 72 changed lines are each one physical line; line count stays 3020 | PASS | `diff` shows 72 `c` hunks of single lines; both files 3020 lines (`wc -l`) |
| C3 | Whole-file "single physical line" premise | PASS (N-1) | Only 7.16 Context and 7.17 Action span several lines, identical to baseline, not R2 |
| C4 | Headers, order, checkboxes untouched | PASS | 355 headers identical, 0 state flips |
| C5 | B2 check 1: five components in every one of the 64 changed items | PASS | Part A and Part B |
| C6 | B2 check 2: no changed item relies on another item for context it needs | FAIL | B2-2 (7.30, 7.34) |
| C7 | B2 check 3: agent-spawning items keep fully embedded prompts | PASS | 7.22, 7.25, 7.30, 7.34, 8.19, 14.19 still carry the verbatim preamble and lens prompt (full lines read) |
| C8 | B2 check 4: file paths specific and spelled exactly | FAIL | B2-1 (7.20); all other new paths exact (`/tmp/b2_a10_paths.py`) |
| C9 | B2 check 5: verification measurable, new commands carry an expected value | PASS | 7.20, 7.30, 7.34, 13.1 commands each have an expected value; run on synthetic sets |
| C10 | B2 check 6: no batch "process all X" item introduced | PASS | no new multi-target item; 7.20 batch of commands is pre-existing |
| C11 | B2 check 7: nothing rests on CODE-CONTRADICTED or UNVERIFIED findings | PASS | scan of all new text: no tag |
| C12 | F-01 text present and verified | PASS | Part C |
| C13 | F-02 text present and verified | PASS | quote equals DESIGN line 716; `grep -nF` simulated |
| C14 | F-03 text present and verified | PASS | `same message`, `Formatting never`, `chat-presentation` on 1210 (N-3 wording drift) |
| C15 | F-04 text present (command, expected value, record-not-evidence) | PASS | command gave 1 on a sample file; the match rule is graded under C8 |
| C16 | F-05 text present and verified | PASS | `re-run this item` hits 1982 |
| C17 | F-06 text present and verified | PASS | literal count 1; 58 lines reworded uniformly |
| C18 | F-07 text present and verified | PASS | `sha256sum` lines 4 to 6 |
| C19 | F-08 text present and verified | PASS | command and expected value 6 on 7.20, 7.30, 7.34 |
| C20 | F-09 text present and verified | PASS | `Phase 7 preamble Branches` hits 1210 |
| C21 | F-10 text present and verified | PASS | 1551 and 1812 |
| C22 | Regression: no command, expected value or gate lost | PASS | Part D |
| C23 | No tick-marked item changed | PASS | Part E, 137 blocks compared |
| C24 | Format hygiene and stale references to the old R2 sentence | PASS | balance script clean; no unticked item still cites the old sentence |
| C25 | New text quotes authoritative sources faithfully | PASS (N-3) | 13.1 quote EQUAL to DESIGN:716; 7.10 clauses match addendum 15-21 except one quoted phrase |

## Summary

- Checks passed: 23 / 25. Checks failed: 2 (C6, C8).
- Blocking findings (BLOCKING plus MAJOR): 2 (B2-1, B2-2). Minor notes: 5 (N-1 to N-5).
- Issues fixed in place: 0 (fix_authorization false).

## Self-Audit

What I did to look for faults, with the evidence behind each:
1. Whole-file structure by script on both files, with a continuation-line aware parser; found and explained 7.16, 7.17 and 14.48 as pre-existing (a first, stricter parser gave 64 false positives, which I discarded after reading them).
2. Read all 72 changed lines as word-level diffs (1084 lines, chunks of at most 150) and read the full new text of 7.10, 7.20, 7.22, 7.25, 7.30, 7.34, 8.19, 10.5, 11.4, 13.1, 14.19 and one 58-group Context line.
3. Proved the 58 Context rewords are one identical substitution and that 12 lens lines also carry the OQ wording (script, 58/58 and 12/12).
4. Ran every shell-runnable verifier from the findings, and ran the new 7.20/7.30/13.1 commands on synthetic inputs (four OQ file sets, a copy of HOW-WE-WORK.md with the bullet inserted, a sample result file). They behave as the items state, including the FAIL case.
5. Compared the 13.1 quoted bullet with DESIGN line 716 by script (equal), and the 7.10 clauses with addendum lines 13-23 (found one quote drift, N-3).
6. Followed each new reference to where it points: found that the R2 BUILD-REQUEST is named only in 7.30/7.34 (B2-1), and that 7.30/7.34 lean on 7.20 for two paths (B2-2).
7. Did not accept the preservation JSON as proof; recomputed ticked-block equality and line counts myself.

Limits: I did not judge whether the edited plan is operationally sound end to end (that is the qualitative lens), nor re-run the structure/phase-order lens. UNVERIFIABLE items: none. UNCHECKED items: none.

Confidence: Verified: 25/25 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 16 | Grep: 0 | Glob: 0 | Bash: 37 (includes `uv run python -I` scripts and two private-directory batch scripts; shell `grep`/`diff` stood in for the Grep tool). Read + Grep + Glob (16) is below the 25 checklist items, which the agent rules mark as suspect; the shortfall is covered by Bash-run scripts whose outputs are quoted above, but the reader should weigh it.
Web research: none (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).

## QA Complete

VERDICT: FAIL
Blocking count: 2

