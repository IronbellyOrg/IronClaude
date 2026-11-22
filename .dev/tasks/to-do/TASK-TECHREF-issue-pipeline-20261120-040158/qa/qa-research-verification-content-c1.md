# QA Report - Research Gap-Fill Verification (Qualitative), Cycle 1

**Topic:** IronClaude issue-to-work pipeline technical reference
**Date:** 2026-11-20
**Phase:** research-gate fix-cycle verification (qualitative)
**Fix cycle:** 1
**Fix authorization:** false (report only)
**Status:** Complete

---

(findings follow below; verdict at the end)

## Working notes (incremental)

- B-1 verified: snapshot `src/superclaude/cli/issue_watch/cycle.py` lines 34-47 are 14 assignments (Read 30-51). Grep over `src` for the 14 names shows production reads for 13 (HEALTH_AGE_S :1327 and STALE_AGE_S :1259 only in status code) and none for MAX_LAUNCHES_PER_CYCLE; case-insensitive Grep for `max_launches_per_cycle` outside `.dev`/`docs` finds only cycle.py:35. Erratum in research/01 lines 658-689 states exactly this, with a 14-row evidence table.
- B-2 verified: `wc -l` of the three agent files = 35 each; `model:` on line 6, `tools:` line 5, `effort: low` line 7 of t3 only; job items 21-24 (t1, t2) and 22-24 (t3), `## Rules` at 26, "Writing only" at 30, "Return value" at 35 (Read t1 18-35, t3 18-35, Grep t2). The 20 other line counts the erratum re-states are plausible (spot-checked test_clickup_claim 569, test_model_alias_policy 249, clickup_claim.py 270 by `wc -l`).
- B-3 verified: `wc -l` and `grep -c 'def test_'` on all 17 files (and on 9 further table-C files) match the erratum tables (research/05 lines 502-579), including the 163 vs 162 difference (string literal at test_launch_level_guard.py:4615, Grep) and the path correction (hooks/ not skills/ for test_require_orca_worktree_agent_governed.py; the skills/ path does not exist, `ls`). Sums re-added by hand: 21115 + 3273 = 24388 lines; 785 + 136 = 921 tests; 10 + 3 + 1 + 2 = 16 files in search (1).
- F-2 verified: both test files read in full (test_model_alias_policy.py all 250 lines; test_clickup_claim.py lines 1-48, 140-329, 440-569); 29 and 11 `def test_`; parametrize case counts 2+5+2+2+6 = 17 (41 collected); ISSUE_WORKER_PINS at :29-33; `model:` lines in the three agents match the pins; design doc sc-issue-command.md still says `claude-gw-tier3` at lines 58, 107, 129, 391, 423, 449 (Grep); model-aliases.md lines 12, 16, 18 read and match the staleness claims; clickup_claim.py:160-259 read and the code-side line map (166, 169, 203-206, 210-220, 230-242, 245-259) is right.
- F-1 verified: predicates.py:17 (`SKEW_TOLERANCE_S = 300`), :279-296 (`marker_in_window`, use at :295), cycle.py:44, 770-775, 848-865 (`_hit` calls `marker_in_window` at :858), issue-watcher.md:494, 509, 510, 656, 826, 827, issue-watcher-setup.md:384, 422, 651 all read and match the erratum. Erratum's withdrawal list (research/03 lines 226, 256, 295, 322, 447, 470, 495) matches the live grep of the file; it covers more places than the four the consolidated finding named.

## Verdict: PASS

All five previously BLOCKING findings are FILLED; no new BLOCKING finding was found. Number of BLOCKING findings: 0. Number of MINOR notes: 5 (M-1 to M-5, below).

## Previously BLOCKING findings

| ID | Research location | FILLED / NOT-FILLED | Justification |
|---|---|---|---|
| B-1 | research/01-watcher-decision-engine.md, "Gap-fill c1 B-1" (lines 658-689), replaces Key Takeaways line 34 | FILLED | States 14 constants at cycle.py:34-47, 13 read (HEALTH_AGE_S :1327 and STALE_AGE_S :1259 read only by the status report), MAX_LAUNCHES_PER_CYCLE dead (cycle.py:35 only). Backed by a 14-row per-constant table with production read lines and test pins, a count check, a dead-constant search and the declaring design lines (issue-watcher.md:380, 819). Independent re-run: Read of cycle.py:30-51 shows 14 assignments; Grep of all 14 names over `src/**/*.py` gives the same read lines; case-insensitive Grep for the dead name finds one hit. Not a surface patch: it also reclassifies the dead constant as DC-1 with the enforcing mechanism (`launching` + `halt`). |
| B-2 | research/04-claim-flow-and-orca-worktree.md, "Gap-fill c1 B-2" (lines 498-541), replaces the three `36` cells at lines 69-71 | FILLED | Corrects all three to 35 and shows line 35 is the `**Return value.**` rule, which agrees with the existing `t*:35` citations. `wc -l` of the three files = 35. It also re-ran `wc -l` on 20 other counts stated in the file; I re-checked the agent frontmatter (`model:` line 6, `tools:` line 5, `effort: low` line 7 of t3), the job-item ranges, the Rules and Return-value lines, and three of the other counts: all correct. |
| B-3 | research/05-guard-stack-and-ccsession.md, "Gap-fill c1 B-3" (lines 502-579), replaces Key Takeaways bullet at line 355 | FILLED | States 14 test files in the section 11.1 table plus 3 claim-side pin files, with path, `wc -l`, `grep -c` and strict count for all 17. I re-ran the counts for all 17 files: every number matches, including 163 vs 162 for the main guard file (the extra hit is the string literal at test_launch_level_guard.py:4615). It corrects a wrong path in the finding text (hooks/, not skills/; the skills/ path does not exist). It adds a searched list of further pinning files (table C, 9 files re-counted and 4 of them spot-checked at the cited test lines) and states the negative-search limit. Sums are right (21115 + 3273 lines; 785 + 136 tests). |
| F-1 | research/03-watcher-operator-surface-and-setup.md, "Gap-fill c1 F-1" (lines 497-543), supersedes the DES:827 verdict | FILLED | Re-tags the row `skew tolerance | 300 s | equals the cadence` (issue-watcher.md:827) as [CODE-VERIFIED] with an ambiguous label. Traces both numbers to code: `SKEW_TOLERANCE_S = 300` (predicates.py:17, used only at :295 inside `marker_in_window`, called only by `_hit`, cycle.py:858) and `SKEW_WARN_S = 60` (cycle.py:44, used only at :774). Cites the design (issue-watcher.md:494, 509, 510) and setup doc (:384, :651) rows and I confirmed each. Lists every earlier location to withdraw (lines 226, 256, 295, 322, 447, 470, 495), which is more than the four named in the finding, and corrects the BUILD-REQUEST.md:32 warning as half right. Its instruction 4 also flags the loose tag in research/01 :610. Matches file 01 row 22 (:594). |
| F-2 | research/04-claim-flow-and-orca-worktree.md, "Gap-fill c1 F-2" (lines 545-597) | FILLED | Adds the two missing test-pin rows with path, lines, test count and behaviour pinned: test_clickup_claim.py (569 lines, 29 tests, 41 collected cases) and test_model_alias_policy.py (249 lines, 11 tests, 13 cases). Counts and case arithmetic re-checked. Both files were read; the line numbers I spot-checked (:145-146, :160-168, :277, :298, :311-318, :343, :372, :389, :405, :442, :459-482, :492, :500-508, :514-545, :548, :561; :29-33, :38-44, :83-101, :104-119, :191-196, :246-249) are right. It ties the rows to the C2 write at clickup_claim.py:232-237 and to the stale `claude-gw-tier3` design text (Grep: sc-issue-command.md lines 58, 107, 129, 391, 423, 449), finds a drift in docs/reference/model-aliases.md (moved test line numbers at lines 12 and 18, and the omitted fourth allow-list path `cli/review/data/`), and lists what the two files do not pin (checked against the code at clickup_claim.py:125-132, 178-179, 196-199, 241-242). Not a surface patch. |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over / new | previously-rated-PASS |
|---|---|---|---|---|---|
| (none) | - | No new BLOCKING finding. No contradiction between research files was introduced by the five gap-fills; the corrections agree with research/01 rows 22 and :594/:610, with research/05 section 11.1 and with the test-pin table in research/04. | See Checks performed. | n/a | n/a |

## Minor notes (not blocking, not rechecked in later rounds)

- M-1. The gap-fills are append-only errata, as the task prompts required ("do not alter existing text"). The superseded wording therefore still stands at research/01:34, research/03:226, 256, 295, 322, 447, 470, 495, research/04:69-71 and research/05:355. The errata name these places, so the assembler must take the erratum values: 14/13/1 constants, 35 lines, 14 + 3 test files, DES:827 as [CODE-VERIFIED] (ambiguous label). Synthesis prompts should say so.
- M-2. research/04 line 3 still says "eight test files"; with F-2 the pin table covers ten. Take ten from the addendum.
- M-3. research/01:610 (Gaps item 7) keeps the tag word `[CODE-CONTRADICTED, refined]` and research/01:634 keeps `[STALE DOC]` for DES:827; the body text in both is right (ambiguous label, not wrong in number). The F-1 erratum (instruction 4) tells the assembler to use [CODE-VERIFIED] with the ambiguity noted. The final document should not list DES:827 as stale.
- M-4. The F-1 erratum tags DES:827 [CODE-VERIFIED] although the design row never names the constant; the match rests on the constant name (`SKEW_TOLERANCE_S`), the value 300 and the design's "equals the cadence" remark. The erratum says the label is ambiguous, so the wording is honest; the final document can say "matches `predicates.SKEW_TOLERANCE_S`; label ambiguous".
- M-5. The 41 and 13 collected-case figures in F-2 come from reading the `parametrize` lists, not from a pytest run (the file says so). The final document should call them "collected cases by reading", not a run result.

## Checks performed

1. B-1: Read cycle.py:30-51; Grep of 14 constant names over `src/**/*.py` (production read lines); case-insensitive Grep for `max_launches_per_cycle` outside `.dev` and `docs`; Read of research/01 lines 20-100 and 640-690; Grep for "13 constants" across the task folder (only the superseded line and the erratum quote).
2. B-2: `wc -l` of the three agent files and of two test files plus clickup_claim.py; Grep of `model:`, `effort:`, `tools:` in the three agents; Read of issue-worker-t1.md 18-35 and issue-worker-t3.md 18-35; Grep of t2 headings; Grep for other "36 lines" claims across the task folder (only research/04:69-71 and the erratum).
3. B-3: a loop of `wc -l`, `grep -c 'def test_'` and the strict count over 26 test files (the 17 and the 9 in table C); `ls` of the wrong skills/ path; Grep of test_launch_level_guard.py for the string literal at :4615; Read of research/05 lines 318-360 (section 11.1) and 495-580; hand re-addition of the totals.
4. F-1: Read predicates.py:10-21 and 276-313; cycle.py:762-777 and 846-867; Grep of issue-watcher.md for 300 / 60 s and of issue-watcher-setup.md for skew; Read of issue-watcher.md:820-829; Grep of research/03 for every "827" and "skew" location, compared against the erratum's withdrawal list; Grep of research/01 and research/02 for the same terms.
5. F-2: Read of test_model_alias_policy.py (all) and test_clickup_claim.py (lines 1-48, 140-329, 440-569); Read of clickup_claim.py:160-259 and Grep of its error and page-cap lines; Grep of `def test_`; Grep of `parametrize`; Read of docs/reference/model-aliases.md lines 1-30; Grep of sc-issue-command.md for `claude-gw-tier3` and for the `## 12.` heading; Read of test_issue_worker_agents.py:14-29; spot-check of table-C test names and lines (test_freshness_subagent_start_policy.py:91-115, test_update_command.py :123/:173/:194/:223, test_cli_doctor.py :143, test_doctor_version.py :197/:212, test_launch.py :75/:102, test_issue_protocol.py :486).
6. Regression check (contradictions between research files introduced by the gap-fills): compared the five errata against each other and against research/01 rows 22 and 15, research/03 line 77 (the 14 constants and `SKEW_WARN_S = 60`), research/05 table C4 versus research/04 F-2 (test_model_alias_policy.py is "not a pin of the guard area" in 05 and "a pin of the issue-worker tier in 04": different scopes, no contradiction) and the task file's gap-fill items 3.5.1 to 3.5.5 (task lines 902-918), which require append-only errata. No contradiction found.
7. Consolidated MINOR findings (evidence M-3/M-4/M-5, depth M-1..M-6, analyst F-01..F-12) were not re-opened and not elevated, per the grading rule.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:** none. The spawn prompt carried no `## Inherited Structural Verdict` section; I applied standalone behaviour. I did not rely on the structural-c1 report that sits in the same folder.

**(b) Independent semantic checks (at least one required, INV-019):**
- Constant counts -> verified by Read of cycle.py:30-51 and a Grep of all 14 names over `src`, not from the erratum's own table.
- Test-file counts -> verified by my own `wc -l` / `grep -c` loop over 26 files, including the 163/162 string-literal case (Grep at test_launch_level_guard.py:4615).
- Skew values -> verified by reading predicates.py:17, 279-296, cycle.py:44, 770-775, 848-865 and the doc rows at issue-watcher.md:494, 509-510, 827 and issue-watcher-setup.md:384, 651.
- F-2 test-pin behaviour claims -> verified by reading both test files and clickup_claim.py:160-259, including the "not pinned" list.

Why the 0 new findings can be trusted: every number the errata introduce (about 60 distinct figures) was recomputed from the snapshot, the erratum's own arithmetic was re-added, one wrong path in the finding text was found by the gap-fill agent and confirmed by me, and I looked for residual false statements and cross-file contradictions (M-1 to M-3 record what remains by design).

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist = 5 previously BLOCKING items + 4 regression checks: cross-file contradiction, residual stale text, new-claim spot checks, minor-not-elevated).
**Tool engagement:** Read: 33 | Grep: 29 | Glob: 2 | Bash: 2 (read-only `wc`, `grep -c`, `ls` on the snapshot; nothing written under it). Web research: none (Tavily not needed; no external lookup).

## QA Complete

Status: Complete
