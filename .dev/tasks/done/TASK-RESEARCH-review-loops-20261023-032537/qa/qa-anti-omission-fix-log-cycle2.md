# QA Report: Phase 6 Anti-Omission Corrections, Cycle 2

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks
**Date:** 2026-10-24
**Phase:** Phase 6 anti-omission gate, Step 6.42
**Anti-omission fix cycle:** 2 of 2
**Fix authorization:** true. The parent applies every write. This worker edited no package file. It returns exact patches.
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. Paths below are relative to R. "Report:N" means line N of `RESEARCH-REPORT-review-loops.md`.
**Report under repair:** 1,316 lines, sha256 `37753a81e7a797b770edb807e15d9bcf5d0609943c5b8f8911c8a14dcc761797`. Measured before and after the work, unchanged on disk.
**Governing template:** `/config/.claude/skills/task/SKILL.md:466-506` (Standard QA Report Output Format).
**Restrictions honoured:**
- No Git command was run and no session `.jsonl` was opened.
- Bash was used only for reading, grep, awk counting, sha256sum, wc, and the private copies in `/tmp/ao642c2/`, where `jq` applied and checked the patch array.

---

## Overall Verdict

Verdict: FAIL

- **Input set fails.** Groups M1 to M7 are still present in the live report, in `synthesis/synth-01`, `synth-04` and `synth-06`, and in the consolidation.
- **Patches written.** This cycle wrote 14 literal patches that resolve all seven groups. All 14 were applied and checked on `/tmp` copies.
- **Patches are pending parent application.** Nothing on disk has changed yet.
- **Rankings unchanged.** No rank, ranked cause, tally or the order V1 > V3 > V2 > V5 > V4 changes.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Required inputs read | PASS | Read in full: `phase-outputs/plans/anti-omission-gate-decision.md` 1-52; `qa/qa-anti-omission-verification-structural.md` 1-123; `qa/qa-anti-omission-verification-content.md` 1-99; `qa/qa-anti-omission-fix-log.md` 1-247; template `/config/.claude/skills/task/SKILL.md:466-506`; the full report 1-1316; `qa/qa-anti-omission-consolidated-findings.md` 140-304; `qa/qa-anti-omission-report-3-rerun.md` 1-259. |
| 2 | Live identity of the five targets | PASS | Measured sha256: report `37753a81…`, synth-01 `5268a163…`, synth-04 `9487ceac…`, synth-06 `d94f089e…`, consolidation `2f677a40…`. The synth values equal the cycle-1 after-hashes (`qa/qa-anti-omission-fix-log.md:125,128,130`). Re-measured after the work: unchanged. |
| 3 | Each correction written from live source lines | PASS | M1: `research/01-session-ac2cd1fd.md:255` (column header "Historical classification") and `:259`; `research/evidence-deck.md:452`. M6: the case key table at `research/01-session-ac2cd1fd.md:30-31` (Session = Orca planning JSONL, Source = Orca `source.md`), plus the report's own usage "Orca `source.md` lines 142…" (Report:580) and "planning log 499" (Report:533). M5: `01-session-ac2cd1fd.md:222`; `evidence-deck.md:446`. M2 and M4: `research/05-session-e002bed2.md:58,132,135,145-146,156,240,242-248`; `synthesis/hypothesis-03.md:59`; `reviews/adversarial/adversarial/variant-3-original.md:28`. M7: the rerun table at `qa/qa-anti-omission-report-3-rerun.md:26-233`. |
| 4 | Patch array applies mechanically, each "before" unique in array order | PASS | `jq` applied the array file by file. Before each step it checked `split(before)|length-1 == 1`. Result: 14 of 14 steps returned count 1, `fail=0`. |
| 5 | Scope: nothing changed outside the targeted lines | PASS | `diff` of the `/tmp` input copies against the output copies:<br>• Report: lines 259, 553, 580, 953 and 1293 only.<br>• synth-01: line 164 only.<br>• synth-04: lines 82 and 109 only.<br>• synth-06: line 18 only.<br>• Consolidation: append only, new lines 305-326 after the unchanged final line 304. |
| 6 | Mirrors match the report | PASS | sha256-equal pairs after patching:<br>• Report:259 = synth-01:164<br>• Report:553 = synth-04:82<br>• Report:953 = synth-06:18<br>• The patched Option C span ("Broader monitor hardening … 242-248`).") is the same in Report:580 and synth-04:109. |
| 7 | Table structure and table of contents | PASS | Per-line pipe counts are identical before and after in all four Markdown targets. Lines starting with `#`: 66 before and 66 after. Report line count stays 1,316. |
| 8 | Ranks, ranked causes, non-consensus order and tallies unchanged | PASS | Section 7 lead through 7.2 (lines 664-715) is byte-identical. String counts, before/after: report "V1 > V3 > V2 > V5 > V4" 5/5, "5 of 5" 4/4, "3 of 5" 6/6, "2 of 5" 5/5; synth-04 3/3, 3/3, 4/4, 4/4. |
| 9 | Line between debated and undebated evidence in ranking rows | PASS | **Option C Support** keeps unlabelled only clauses found in the debated card (`synthesis/hypothesis-03.md:59` = `variant-3-original.md:28`): uncapped fields, case-insensitive matching, and the any-severity rule. The rest is now prefixed "Case-report detail the debate never weighed:", the same label pattern as Report:553 and :168.<br>**Option B** O-25 keeps its existing label, and the limit is restored. |
| 10 | Grep for sentences the changes contradict | PASS | 0 hits remain in the report or synth copies for `Source:158`, `Session:912`, "targeted reviewer classed", "Preserve both source statements" and "cosmetic output (the unused".<br>Searches for "both/two Orca", "both contradictory" and "both/two tensions" return only Report:1292, which already carries its Step 6.39 update note naming the third tension.<br>The new Q6 wording ("all three tensions") agrees with Report:904 ("all three Orca source tensions") and :408 ("all three contradictory statements"). |
| 11 | Forbidden files and accepted defects untouched | PASS | No case file, research source, card, `reviews/adversarial/**`, log, plan, gate decision or task file is in the array. No patch touches Report:5, :8, :324, :848, :1235, :1238 or :1287 (J1, L1, L2, L3). |
| 12 | Input-set anti-omission status | FAIL | M1 to M7 remain in the live files until the parent applies the patches. |

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 18 (one oversized-read error retried in chunks) | Grep: 0 (searches ran through Bash grep) | Glob: 0 | Bash: 13 (read-only, plus `/tmp/ao642c2/` copies and the `jq` application there) | Write: 1, to `/tmp/ao642c2/patches.json` only. No web research.

## Summary

- Checks passed: 11 of 12. Checks failed: 1 (check 12, the status of the input set).
- Groups processed: 7 = 7 RESOLVED + 0 UNRESOLVED. By severity: IMPORTANT 2 (M1, M2) + MINOR 5 (M3, M4, M5, M6, M7) = 7.
- Patches: 14 in total.
  - Report: 7, of which 6 are M-group fixes and 1 is a change-record note (C2-R07).
  - synth-01: 3. synth-04: 2. synth-06: 1. Consolidation erratum: 1.
  - Sum: 7 + 3 + 2 + 1 + 1 = 14.
- Critical issues: 0. Issues fixed in place: 0, because direct writes are prohibited and the patches are pending.
- Rank impact: none for every group.

## Issues Found

| ID | Sev. | Old issue | Evidence path:line | Resolution (patches) | Status | Rank impact |
|---|---|---|---|---|---|---|
| M1 (AO-V1, F-01) | IMPORTANT | Report:259 and synth-01:164 said "The targeted reviewer classed the resulting finding as preexisting and inherited…". In the source, that classification is the case analyst's. | `research/01-session-ac2cd1fd.md:255` (column "Historical classification"), `:259` (the reviewer's observation is in column 1; the classification is in column 2); `research/evidence-deck.md:452` | Replaced with: the reviewer's actual observation from :259 column 1, then "the case analysis, not that reviewer, classes the resulting finding as preexisting and inherited from the source, not a v3 regression", with citations `:255,259` and deck `:452` (C2-R02, C2-S1-02) | RESOLVED | None. Section 2.5 is not a ranking row. |
| M2 (AO-V4, F-02) | IMPORTANT | Report:580 and synth-04:109 (Option C Support, ranked V3) carried undebated case detail with no label: judge every bullet, rename-overlap exactness, cosmetics, `vhex()`. | Debated card `synthesis/hypothesis-03.md:59` = `reviews/adversarial/adversarial/variant-3-original.md:28` (uncapped fields, case-insensitive matching, any-severity only); `research/05-session-e002bed2.md:58,145-146,242-248` | The debated clauses stay unlabelled, each with its own citation (`:156`; `hypothesis-03.md:59`, `:240`). The undebated clause is now prefixed "Case-report detail the debate never weighed:" (C2-R05, C2-S4-05). Labelling was chosen over removal so that no recovered O-30 content is lost. | RESOLVED | None. No undebated evidence remains unlabelled in a ranking row. |
| M3 (AO-V2) | MINOR | Question 6 Suggested Resolution (Report:953, synth-06:18) still said "Preserve both source statements" after a third tension was added. | `qa/qa-anti-omission-consolidated-findings.md:150` (the instruction to name all three); Report:953 Impact cell lists three | Now reads "Preserve the statements on both sides of all three tensions and their historical frames" (C2-R06, C2-S6-06) | RESOLVED | None |
| M4 (AO-V3, F-03) | MINOR | Report:580 and synth-04:109 called the unused `vhex()` helper "cosmetic output". | `research/05-session-e002bed2.md:132` ("**Preexisting extra.**"); cosmetics are separate rows at `:135`, `:146`; `research/evidence-deck.md:534` vs `:549` | Now reads "cosmetic output (punctuation and grammar) and an unused `vhex()` helper that the case classes as a preexisting extra" (in C2-R05, C2-S4-05) | RESOLVED | None |
| M5 (AO-V5, F-04) | MINOR | The O-25 clause in Option B Support (Report:553, synth-04:82) stated the introduced N-17 gap without the source's limit. | `research/01-session-ac2cd1fd.md:222` ("a known local-failure comparison also existed in v2 constraints"); `research/evidence-deck.md:446` ("Earlier local failure comparison also existed; no execution claimed.") | Added ", although a known local-failure comparison already existed in the v2 constraints and no execution is claimed" before the citation (C2-R04, C2-S4-04) | RESOLVED | None. The label "the debate never weighed" is kept. |
| M6 (AO-V6) | MINOR | Report:259 and synth-01:164 used the location keys `Source:158`, `Source:469` and `Session:912`, which the report never defines. | `research/01-session-ac2cd1fd.md:30-31` (key table: Session = Orca planning JSONL, Source = Orca `source.md`), `:259`; report usage at Report:533 ("planning log 499") and :580 ("Orca `source.md` lines …") | Now reads "Orca `source.md` line 158", "Orca `source.md` line 469" and "Orca planning log record 912" (C2-R01, C2-R03, C2-S1-01, C2-S1-03) | RESOLVED | None |
| M7 (AO-V7) | MINOR | The consolidation addendum accepted the rerun because its "counts reconcile: 256 + 33 + 1 = 290". Only the 290 total reconciles. | `qa/qa-anti-omission-consolidated-findings.md:243`; `qa/qa-anti-omission-report-3-rerun.md:248-251` (stated split) against its table `:26-233`. A mechanical awk count with every range expanded gives R 210, D 76, R/D 3 (E115, E168, E176) and O 1 (E209), total 290. | Appended the section "## Erratum: Partition 3 Rerun Counts (2026-10-24, anti-omission cycle 2)". It is attributed, and it records the recount table and three related labelling slips: rerun :254; addendum :275 for E168/E176; addendum :276 for E139. It states that the O-ID set is unchanged. No earlier text is rewritten (C2-Q-07). | RESOLVED | None. The O-ID set, the RECOVER list and the ranking are unchanged. |

## Actions Taken

- **Copies made.** Copied the five targets to `/tmp/ao642c2/in/` and confirmed that each copy's hash equals the live file.
- **Patches written and applied on copies.** Wrote 14 patches in `/tmp/ao642c2/patches.json` and applied them in order to `/tmp/ao642c2/out/` with a per-step uniqueness check (14 of 14, count 1). Hashed the results, then re-measured the live files and confirmed they are unchanged.
- **Change-record note added (C2-R07).** This is outside M1 to M7. It adds one sentence to the 10.10 "Assembly changes to component text" row recording this cycle's corrections and naming this fix log. Without it, the 10.10 record stops at Step 6.39. The cycle-1 content verifier checked that 10.10 records each correction pass (`qa/qa-anti-omission-verification-content.md:41`). The sentence exists only in the report, because 10.10 has no component mirror.
- **Deliberate choices:**
  - For M2, the undebated clause was labelled rather than removed. The O-30 recovery content stays, and the case-insensitive and any-severity clauses each carry their own citation.
  - For M1, the reviewer's real observation from the source (`:259` column 1) was kept next to the corrected attribution, so the row still says what the reviewer did.
- **Observation, not fixed.** The consolidation's own O-05 recovery text (`qa/qa-anti-omission-consolidated-findings.md:150`) is where the misattribution "The targeted reviewer classed…" came from. The rule forbids rewriting earlier consolidation text, and the M7 erratum is limited to counts, so that line is left as historical. The report and synth-01, the deliverable surfaces, are corrected.

## Exact Patches If Direct Writes Are Prohibited

**(a) Hashes, measured on the `/tmp` copies before and after applying the array below in order:**

| File | sha256 before | sha256 after |
|---|---|---|
| `RESEARCH-REPORT-review-loops.md` | `37753a81e7a797b770edb807e15d9bcf5d0609943c5b8f8911c8a14dcc761797` | `41145b5e9660967e6f6498efb90da18bbfcd51eb3a81a0850fbdcde29fca40a0` |
| `synthesis/synth-01-problem-current-state.md` | `5268a163f929eaf197f64cb3aee62dc0fa4302c9da8fe7d9f01e9704c284428c` | `06ec10475fbdb65c2cede45fa642fc62411a1f3a86f8b40cc15c610fdcbcff9c` |
| `synthesis/synth-04-options-recommendation.md` | `9487ceac2220f9018fa09a2054b89930fc159dac1cb30465d70a22090f3fcdd3` | `b7ea841f4ce97f0fc8dd826ca6722f0327d46ce239a7de3388dd4cb0c440da36` |
| `synthesis/synth-06-questions-evidence.md` | `d94f089e1e6ac7e3172b535136730e84a3a06f615aacdcb05d52161c2aa4e7f1` | `bdf94b0d6c32bfbdb168270cdcd1b9c82b246599a7ee4549aa043216ec23ceda` |
| `qa/qa-anti-omission-consolidated-findings.md` | `2f677a40682ddab6712eb770779b97be65c6f6fbaaa17548db4a92a463032fe1` | `df17bffe25e345ea19e83637106dce11f5f004f4641b47e61c3c8f1016ac8a5e` |

**(b) Patch array.**
- Apply in array order using literal, non-regex replacement.
- Each "before" occurs exactly once in its file at its step. This was verified with `jq` `split/join`: 14 of 14 steps returned count 1.
- After application, the report has 1,316 lines and the consolidation has 326.
- The same array is saved at `/tmp/ao642c2/patches.json`.

```json
[
{"id":"C2-R01","file":"RESEARCH-REPORT-review-loops.md","before":"`object.url` (Source:158), while its rule requires upstream values to be checked before use (Source:469).]","after":"`object.url` (Orca `source.md` line 158), while its rule requires upstream values to be checked before use (Orca `source.md` line 469).]"},
{"id":"C2-R02","file":"RESEARCH-REPORT-review-loops.md","before":"The targeted reviewer classed the resulting finding as preexisting and inherited from the source, not a v3 regression.","after":"The targeted reviewer observed that annotated tags are followed through an upstream-controlled URL without checking it first; the case analysis, not that reviewer, classes the resulting finding as preexisting and inherited from the source, not a v3 regression (`research/01-session-ac2cd1fd.md:255,259`; `research/evidence-deck.md:452`)."},
{"id":"C2-R03","file":"RESEARCH-REPORT-review-loops.md","before":"a fixed tag-object endpoint, Session:912)","after":"a fixed tag-object endpoint, Orca planning log record 912)"},
{"id":"C2-R04","file":"RESEARCH-REPORT-review-loops.md","before":"an introduced acceptance-executability gap (N-17; `research/01-session-ac2cd1fd.md:222`; `research/evidence-deck.md:446`).","after":"an introduced acceptance-executability gap, although a known local-failure comparison already existed in the v2 constraints and no execution is claimed (N-17; `research/01-session-ac2cd1fd.md:222`; `research/evidence-deck.md:446`)."},
{"id":"C2-R05","file":"RESEARCH-REPORT-review-loops.md","before":"and case-insensitive security-keyword matching that the written pattern did not clearly require. The per-review prompts made any defect of any severity noncompliant and told reviewers to judge every Task 12 requirement bullet directly, so findings mixed requirement violations with exactness problems in commands the requirements suggested (the `git diff --name-only` rename overlap) and cosmetic output (the unused `vhex()` helper, punctuation and grammar) (`research/05-session-e002bed2.md:58,132,145-146,156,240-250`; `synthesis/hypothesis-03.md:59`).","after":"and case-insensitive security-keyword matching that the written pattern did not clearly require (`research/05-session-e002bed2.md:156`). The per-review prompts made any defect of any severity noncompliant (`synthesis/hypothesis-03.md:59`; `research/05-session-e002bed2.md:240`). Case-report detail the debate never weighed: the review prompts also told reviewers to judge every Task 12 requirement bullet directly, and the findings mixed requirement violations with exactness problems in commands the requirements suggested (the `git diff --name-only` rename overlap), cosmetic output (punctuation and grammar) and an unused `vhex()` helper that the case classes as a preexisting extra (`research/05-session-e002bed2.md:58,132,135,145-146,242-248`)."},
{"id":"C2-R06","file":"RESEARCH-REPORT-review-loops.md","before":"Preserve both source statements and their historical frames.","after":"Preserve the statements on both sides of all three tensions and their historical frames."},
{"id":"C2-R07","file":"RESEARCH-REPORT-review-loops.md","before":"its 10.10 additions exist only in this report. |","after":"its 10.10 additions exist only in this report. Anti-omission fix cycle 2 (Task Step 6.42, `qa/qa-anti-omission-fix-log-cycle2.md`) then corrected recovered wording in the Section 2.5 annotated-tag row, Option B Support, Option C Support and Question 6, with the same text in `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-04-options-recommendation.md` and `synthesis/synth-06-questions-evidence.md`. |"},
{"id":"C2-S1-01","file":"synthesis/synth-01-problem-current-state.md","before":"`object.url` (Source:158), while its rule requires upstream values to be checked before use (Source:469).]","after":"`object.url` (Orca `source.md` line 158), while its rule requires upstream values to be checked before use (Orca `source.md` line 469).]"},
{"id":"C2-S1-02","file":"synthesis/synth-01-problem-current-state.md","before":"The targeted reviewer classed the resulting finding as preexisting and inherited from the source, not a v3 regression.","after":"The targeted reviewer observed that annotated tags are followed through an upstream-controlled URL without checking it first; the case analysis, not that reviewer, classes the resulting finding as preexisting and inherited from the source, not a v3 regression (`research/01-session-ac2cd1fd.md:255,259`; `research/evidence-deck.md:452`)."},
{"id":"C2-S1-03","file":"synthesis/synth-01-problem-current-state.md","before":"a fixed tag-object endpoint, Session:912)","after":"a fixed tag-object endpoint, Orca planning log record 912)"},
{"id":"C2-S4-04","file":"synthesis/synth-04-options-recommendation.md","before":"an introduced acceptance-executability gap (N-17; `research/01-session-ac2cd1fd.md:222`; `research/evidence-deck.md:446`).","after":"an introduced acceptance-executability gap, although a known local-failure comparison already existed in the v2 constraints and no execution is claimed (N-17; `research/01-session-ac2cd1fd.md:222`; `research/evidence-deck.md:446`)."},
{"id":"C2-S4-05","file":"synthesis/synth-04-options-recommendation.md","before":"and case-insensitive security-keyword matching that the written pattern did not clearly require. The per-review prompts made any defect of any severity noncompliant and told reviewers to judge every Task 12 requirement bullet directly, so findings mixed requirement violations with exactness problems in commands the requirements suggested (the `git diff --name-only` rename overlap) and cosmetic output (the unused `vhex()` helper, punctuation and grammar) (`research/05-session-e002bed2.md:58,132,145-146,156,240-250`; `synthesis/hypothesis-03.md:59`).","after":"and case-insensitive security-keyword matching that the written pattern did not clearly require (`research/05-session-e002bed2.md:156`). The per-review prompts made any defect of any severity noncompliant (`synthesis/hypothesis-03.md:59`; `research/05-session-e002bed2.md:240`). Case-report detail the debate never weighed: the review prompts also told reviewers to judge every Task 12 requirement bullet directly, and the findings mixed requirement violations with exactness problems in commands the requirements suggested (the `git diff --name-only` rename overlap), cosmetic output (punctuation and grammar) and an unused `vhex()` helper that the case classes as a preexisting extra (`research/05-session-e002bed2.md:58,132,135,145-146,242-248`)."},
{"id":"C2-S6-06","file":"synthesis/synth-06-questions-evidence.md","before":"Preserve both source statements and their historical frames.","after":"Preserve the statements on both sides of all three tensions and their historical frames."},
{"id":"C2-Q-07","file":"qa/qa-anti-omission-consolidated-findings.md","before":"_Parent persistence note (2026-10-24): addendum appended verbatim from the consolidator's final transcript text (record 233) at the parent's request; the original consolidation above is unchanged._","after":"_Parent persistence note (2026-10-24): addendum appended verbatim from the consolidator's final transcript text (record 233) at the parent's request; the original consolidation above is unchanged._\n\n## Erratum: Partition 3 Rerun Counts (2026-10-24, anti-omission cycle 2)\n\n**Attribution:** appended by the anti-omission fix cycle 2 worker (Task Step 6.42, group M7; `qa/qa-anti-omission-fix-log-cycle2.md`) from the structural verifier's finding AO-V7 (`qa/qa-anti-omission-verification-structural.md`, Issues Found). Everything above this heading is unchanged; this section corrects one statement and rewrites nothing.\n\n**Statement corrected:** the addendum's rerun validity verdict (line 243 above) says the rerun's \"counts reconcile: 256 represented + 33 covered-by-dedup + 1 omitted = 290\". Only the 290 total and the block sum 17+7+20+107+14+20+13+20+11+34+24+3 reconcile. The 256/33/1 split is the rerun's own summary (`qa/qa-anti-omission-report-3-rerun.md:248-251`), and it does not match the rerun's own enumeration table. This is the same class of count failure recorded against the original Partition 3 report under PF-01.\n\n**Recount from the rerun's own table** (`qa/qa-anti-omission-report-3-rerun.md:26-233`; every range row expanded to its item count, for example E46-E75 = 30; counted mechanically):\n\n| Status in the rerun table | Items | Rows |\n|---|---:|---|\n| R (represented) | 210 | Block A 17, B 7, C 20, D 34 (E45, E76-E91, E92-E96, E116, E140-E150), E 14, F 15, G 13, H 18, I 11, J 34, K 24, L 3 |\n| D (covered-by-dedup) | 76 | E46-E75 (30), E97-E114 (18), E117-E138 (22), E139, E151, E170, E177, E178, E207 |\n| R/D | 3 | E115, E168, E176 |\n| O (omitted) | 1 | E209 |\n| **Total** | **290** | 210 + 76 + 3 + 1 |\n\n**Related labelling slips, recorded and not rewritten:**\n- The rerun's own prose (`qa/qa-anti-omission-report-3-rerun.md:254`) names the dedup ranges \"E97-E116\" and \"E117-E139\", but its table marks E115 R/D and E116 R.\n- The addendum's mapping table groups E168 and E176 with the rerun's D rows (line 275 above), but the rerun marks them R/D. It groups E139 with the \"rerun R or R/D\" rows (line 276 above), but the rerun marks E139 D; its anchor, the five reviewer identities in the Section 2.2 monitor row, is present in the report.\n\n**Effect:** none on the O-ID set, the RECOVER list or the ranking. The mapping table above (lines 262-277) still adjudicates every D range and every single D row, and the recount changes no adjudication. The rerun file and the earlier text of this consolidation are not edited."}
]
```

## Preservation Checks

| Check | Result |
|---|---|
| Live targets unchanged by this worker | The live sha256 of all five targets equals the "before" column, re-measured after the work. |
| No historical artifact edited | Not written: case files, research sources, cards, `reviews/adversarial/**`, logs, plans, gate decisions, the task file and the rerun report. The only writes were to `/tmp/ao642c2/`. |
| Consolidation history | Append only. Lines 1-304 are byte-identical; the erratum occupies new lines 305-326. |
| Ranking, ranked causes and tallies | Section 7 lead through 7.2 is byte-identical. The order string and every tally count are equal in the report and synth-04. |
| Debated and undebated evidence boundary | The ranking rows carry undebated content only under a "never weighed" label: Option B for O-23 and O-25, Option C for O-30's case detail. O-04 and O-05 remain outside the Option Support rows. |
| Accepted defects | J1, L1, L2 and L3 are untouched. |
| Table of contents and table structure | 66 heading lines before and after. Per-line pipe counts are unchanged in all four Markdown targets. |

## QA Complete

| Status | Result |
|---|---|
| DONE | Read the gate decision, both cycle-1 verifications, the cycle-1 fix log, the template, the full 1,316-line report, the consolidation and rerun, and the live source lines behind M1 to M7. |
| DONE | Wrote 14 literal patches: 7 to the report, 3 to synth-01, 2 to synth-04, 1 to synth-06 and the M7 erratum. They resolve M1 to M7 with 0 unresolved. All were applied on `/tmp` copies with unique "before" strings, and the after-hashes are listed above. |
| DONE | Confirmed that only the targeted lines change, the mirrors match the report, Section 7 is byte-identical, the tallies are unchanged and no contradicted sentence remains. Recounted the rerun split mechanically: 210 R, 76 D, 3 R/D, 1 O. |
| NEXT | Parent: apply the JSON array in order to the five files and confirm each after-hash. Then run fresh Step 6.40 and 6.41 verifiers against the corrected state. |
## Parent Application Record (2026-10-24)

| Item | Record |
|---|---|
| Persistence | The parent copied this report verbatim from the restricted worker's final transcript text (record 141 of `subagents/agent-ap6-ao-fixer-c2-*.jsonl`) into the prepared stub. The parent did not edit the worker text above this section. |
| Application | `/tmp/apply_p6.py qa/qa-anti-omission-fix-log-cycle2.md` applied all 14 JSON patches in array order; each `before` occurred exactly once; all five start and end hashes matched before any write. |
| Files written | `RESEARCH-REPORT-review-loops.md` (1,316 lines, sha256 41145b5e...), `synthesis/synth-01`, `synth-04`, `synth-06`, and an append-only erratum section in `qa/qa-anti-omission-consolidated-findings.md` (M7). |
| Not written | Case files, research sources, cards (hashes unchanged), `reviews/adversarial/**`, logs, plans, gate decisions, the task file. J1, L1, L2, L3 not fixed, by user decision. |
| Git | None run. |
| Verification | Pending: `qa/qa-anti-omission-verification-structural-cycle2.md` and `qa/qa-anti-omission-verification-content-cycle2.md`. |
