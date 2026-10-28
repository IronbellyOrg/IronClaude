# QA Report: Phase 6 Anti-Omission Verification, Structural

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks
**Date:** 2026-10-24
**Task step:** Step 6.40, Independent structural omission verification (`TASK-RESEARCH-review-loops-20261023-032537.md:533-535`)
**Phase:** Phase 6 anti-omission gate, fix-cycle verification (report-only, `fix_authorization: false`)
**Anti-omission fix cycle verified:** 1 (the Step 6.39 recovery)
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. All paths below are relative to R. "Report:N" means line N of the live report.
**Report under verification:** `RESEARCH-REPORT-review-loops.md`. It is 1,316 lines with sha256 `37753a81e7a797b770edb807e15d9bcf5d0609943c5b8f8911c8a14dcc761797`. I measured both values with `sha256sum` and `wc -l`, and they match the fix log's after-hash.
**Governing templates read:** `/config/.claude/skills/tech-research/SKILL.md:1196-1239` (anti-omission prompt and output format) and `/config/.claude/skills/task/SKILL.md:466-506` (standard QA report format).
**Restrictions honoured:** I ran no Git command, opened no session `.jsonl`, and edited no file.

---

## Overall Verdict

Verdict: FAIL

The recovery is real and correctly bounded:
- All 34 recoveries are present and placed where the fix log says.
- The diff against the pre-patch copy touches only the 30 hunks that hold the patches.
- The ranking, order and tallies are byte-identical.
- O-04 and O-05 are kept out of the Option Support rows.
- O-08 and O-14 are validly deduplicated.

The gate still fails because seven defects remain: one IMPORTANT and six MINOR. Three recoveries misstate or weaken their primary source (O-05, O-25 and O-30). One O-05 count instruction from the consolidation was not carried out (Question 6 still says "both"). One O-30 addition puts undebated evidence into a ranking row without a label. The new 2.5 row uses location keys the report never defines. The consolidation addendum accepted Partition 3 rerun counts that do not reconcile with the rerun's own table.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | All required inputs read | PASS | Read Step 6.40 (task :533-535) and both templates. Read in full: `qa/qa-anti-omission-consolidated-findings.md` 1-305 (including the Partition 3 rerun addendum at 229-304), `qa/qa-anti-omission-fix-log.md` 1-247 (including the Parent Application Record at 237-246), `phase-outputs/discovery/anti-omission-input-map.md` 1-223, `qa/qa-anti-omission-report-3-rerun.md` 1-260, and the full report 1-1316. |
| 2 | Report and component identity | PASS | Report sha256 `37753a81…` with 1,316 lines. synth-01 to synth-06 hash to `5268a163…`, `5da15419…`, `b0a561a5…`, `9487ceac…`, `994f3502…` and `d94f089e…`, each equal to its fix-log after-hash (fix log :125-130). The cards hash unchanged and their mtime is 03:48. |
| 3 | Patch scope: nothing changed outside the 78 patches | PASS | `/tmp/ao639/report.md` hashes to the input identity `a10cef08…`. `diff` against the live report shows exactly 30 hunks, all at patched lines (106-107, 110, 165, 167-170, 178-179, 181-182, 193-194, 230a, 256a, 261, 275-276, 344-345, 405, 407, 527, 550, 577, 609, 614, 757, 785, 872, 893, 901, 950, 1043, 1289-1290 in old numbering). Each rewritten patch keeps its original wording, so no content was removed. |
| 4 | Each of the 34 recoveries verified by meaning against its primary source | FAIL | 31 of 34 convey their source accurately. O-05, O-25 and O-30 do not (AO-V1, AO-V3, AO-V5). Sources read are listed under "Primary sources re-read" below. |
| 5 | O-08 and O-14 dedup rationale | PASS | O-08 is the syntax-error-then-corrected metadata command (`phase-outputs/discovery/input-inventory.md:83`). O-14 is the wrong manifest location and polluted extraction, "no unresolved source-access blocker remains" (`research/scope-03-recovered.md:13,176`). Both are research-producer recovery errors under the exclusion at Report:282 ("Historical producer recovery errors and administrative gate narratives are not new empirical loop incidents"). Both source files stay listed in the evidence trail (Report:1171, 1048), which satisfies `BUILD-REQUEST.md:35` ("retain every intermediate"). |
| 6 | Every enumeration row has a disposition | PASS | Mechanical counts. P1: 224 rows = 154 R + 49 D + 21 O. P2: 295 rows = 225 R + 56 C + 14 O. P4: 406 rows = 383 REP + 20 DEDUP + 3 OMIT. P3 rerun: 153 rows covering 290 items, every row with a status (140 R, 9 D, 3 R/D, 1 O). All 38 proposed omissions and the rerun's O1 map to O-01 to O-36. |
| 7 | Enumeration counts reconcile | FAIL | P1, P2 and P4 reconcile. The P3 rerun does not (AO-V7). |
| 8 | No source family unowned | PASS | The map gives 53 inputs: 14 to P1, 8 to P2, 5 to P3 and 26 to P4, with none unassigned and none assigned twice (map:180-186). The P3 rerun covers deck D1, D3, D5-D11 and D13-D15, all of web-01, and synth-01 to synth-03 by line diff. The consolidator directly covered D2, D4, D12 and D16 (addendum :247-251, :277). |
| 9 | Condition: O-04 and O-05 not in Section 6 Option Support rows | PASS | `annotated` appears only at Report:259, 348, 408, 904, 953 and 1292. `185406` and "skipped on purpose" appear only at Report:170. The Option C Support row (Report:580) names only the two debated Orca contradictions (source lines 142, 285, 382, 402). |
| 10 | Condition: O-25, O-28 and O-29 labelled as undebated | PASS | Report:553: "A further case-report finding the debate never weighed". Report:168: "Two low findings are case-report findings the debate never weighed". Variant greps for `same result`, `immutab`, `angle`, `D-007` and `D-010` return 0 in all five variants. |
| 11 | Undebated evidence stays out of ranking rows (consolidation :218, :291) | FAIL | The O-30 addition at Report:580 carries case-report detail that no card or debate record contains, with no label (AO-V4). |
| 12 | Cycle-0 PASS set still holds | PASS | Checked by diff (check 3). Everything outside the 30 hunks is byte-identical, and the hunks only add text or widen counts. Option Opposition rows are untouched, and the Section 7 lead through 7.2 is identical (old 661-712 against new 664-715). |
| 13 | Count assertions consistent after the O-05 three-tension change | FAIL | Question 6 Suggested Resolution still says "Preserve both source statements" (AO-V2). |
| 14 | Prior report-gate and fidelity checks affected by O-01, O-02 and O-03, rechecked on the new text | PASS | Decoded `research/historical-review-rules.json` records.before and records.after with `jq`. Before :65 "executor MUST NOT write the Ruling line". Before :79 "Missing, stale or unverifiable evidence is `issues`". After :61-68 (terminal-halt `E-HALT-QA`, `E-RESUME-NEEDED`, broadened `E-NO-RULING`, executor-recorded Ruling with unchanged verdict). After :82 (current files and `./artifacts/` logs, "a moved line number alone is never `issues`", accepted-gap check, FINAL reads revert briefs and `<retries>/T<id>/`). After :86 (A3-A5, re-run and operator reviews always subagents; before :83 "One mode for the rest of the run"). After :90 (retry and troubleshoot folders barred, citation means `cannot-verify`). Every clause in Report:231, 580, 612 and 896 matches. The second FINAL is the earlier load and the third is the later one (`research/scope-rules.md:70-71`; `research/scope-03-recovered.md:145-146`). The questions-answered-elsewhere check still holds: Q3 and Q4 stay open ("sharpen, and do not resolve", Report:231). |
| 15 | O-05 and O-23 rechecked | FAIL for O-05, PASS for O-23 | O-23 matches `research/01-session-ac2cd1fd.md:208,299` and `research/evidence-deck.md:431`, and "defensible" appears 0 times in all five variants. O-05 fails (AO-V1, AO-V2, AO-V6). |
| 16 | No new contradiction with the Git disclosure, the ranking-criterion disclosure or the P6-04 shared-install disclosure | PASS | No recovery adds a Git read. O-17 cites file-size checks at screening (`research/scope-03-recovered.md:158,162`). No recovery uses likelihood language. The new 2.3 text agrees with the 20:26:30 and 20:32:19 loads bracketing the 20:29:54Z install (Report:229, 583). O-16 states that no link to the rubric change is established (Report:181). |
| 17 | Ranks, the non-consensus order and tallies unchanged | PASS | Section 7 lead through 7.2 is byte-identical (check 12). `V1 > V3 > V2 > V5 > V4` appears 5 times in the report and 3 times in synth-04. 7.1 and 7.2 show 5 of 5, 3 of 5, 3 of 5, 2 of 5, 2 of 5 and 2 of 5 as before. |
| 18 | TOC, section numbering and stated counts | PASS | 66 heading lines, the same as before, with no heading added. R39 says "34 omissions", which matches the consolidation's 34 RECOVER. The R12 placement list matches Report:259, 348, 408, 904 and 953. Line count 1,313 + 3 = 1,316, consistent with R01 adding 2 lines and R08 adding 1. Patch total 40 + 38 = 78. |
| 19 | New text is resolvable within the report | FAIL | Undefined keys `Source:158`, `Source:469` and `Session:912` (AO-V6). |
| 20 | No placeholders; known defects J1 and L1-L3 not counted | PASS | `grep` for `TBD`, `TODO`, `FIXME`, `RF_PLACEHOLDER` and `{{` finds 0. The stale header and 10.9 status (Report:5, 1241) are J1 and are not counted here. |

**Primary sources re-read for check 4.** These were the live source lines, not their summaries:
- `research/scope-rules.md:26-89`
- `research/historical-review-rules.json`, both decoded `content` fields
- `research/evidence-deck.md:425-560` and `:700-713`
- `synthesis/hypothesis-03.md:54-62` and `synthesis/hypothesis-01.md:138-144`
- `reviews/adversarial/merged-root-cause-analysis.md:70-79`
- `research/01-session-ac2cd1fd.md:185-302`
- `research/03-session-6f744b87.md:98-144`
- `research/04-session-43582de1.md:250-259`, `:344-358` and `:516-561`
- `research/05-session-e002bed2.md:52-176`, `:236-297` and `:408-449`
- `research/06-session-0690ee9f.md:68-79` and `:292-303`
- `research/scope-03-recovered.md:1-184`
- `research/scope-01-recovered.md:54-65`
- `research/scope-02.md:14-45`
- `research/research-notes.md:26-33`
- `phase-outputs/discovery/input-inventory.md:40-85`
- `research/screening-handoffs-source.txt:60-199` and `:366-383`
- variant greps across `reviews/adversarial/adversarial/variant-1..5-original.md` and `debate-transcript.md`

**Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 40 | Grep: 0 (searches ran through Bash grep) | Glob: 0 | Bash: 16 (read-only: sha256sum, wc, jq decode, grep, sed, cut, diff against `/tmp/ao639` copies). No web research.

## Summary

- Checks passed: 13 of 20. Checks failed: 7 (checks 4, 7, 11, 13, 15, 19 for O-05, and the count part of check 7 through AO-V7).
- Issues: 7 in total. CRITICAL 0, IMPORTANT 1 (AO-V1), MINOR 6 (AO-V2 to AO-V7).
- O-IDs verified: 36. Recovered and correct: 31. Recovered but defective: 3 (O-05, O-25, O-30). Dedup confirmed: 2 (O-08, O-14).
- Regressions against the cycle-0 PASS set: 0.
- Issues fixed in place: 0 (report-only).
- The same defects are mirrored in the synthesis components: synth-01:164, synth-04:82, synth-04:109 and synth-06:18.

## Issues Found

| ID | Severity | Location path:line | Issue | Primary evidence | Required fix |
|---|---|---|---|---|---|
| AO-V1 | IMPORTANT | `RESEARCH-REPORT-review-loops.md:259`; mirror `synthesis/synth-01-problem-current-state.md:164` | **O-05 misattributes a classification.** The new 2.5 row says "The targeted reviewer classed the resulting finding as preexisting and inherited from the source, not a v3 regression." In the primary source that classification belongs to the case analysis, not the targeted reviewer. The report's subject is the difference between what reviewers claimed and what was established, so assigning an analyst's judgment to a historical reviewer is a fidelity defect. | `research/01-session-ac2cd1fd.md:255,259`: the table columns are "Targeted observation \| Historical classification \| Actual v4 response". The reviewer's observation is "Annotated tags are followed through an upstream-controlled URL without checking it first". The "Historical classification" cell, "Pre-existing, inherited from Source:158 ... not a v3 regression", is the analyst's. `research/evidence-deck.md:452` gives the same classification as the deck's own. No package source states that the reviewer made this classification. | Replace the sentence in both files with: "The case analysis classes the resulting finding as preexisting and inherited from the source, not a v3 regression (`research/01-session-ac2cd1fd.md:259`; `research/evidence-deck.md:452`)." |
| AO-V2 | MINOR | `RESEARCH-REPORT-review-loops.md:953` (Question 6, Suggested Resolution); mirror `synthesis/synth-06-questions-evidence.md:18` | **O-05 count instruction only partly applied.** The Impact cell now lists three Orca tensions, but the Suggested Resolution still says "Preserve both source statements and their historical frames". The consolidation told the fixer to change "both" at old Report:950 (this row) to name all three tensions. The only "both" in that pre-patch row is this one. The fixer's grep (fix log :37) missed it. | Consolidation O-05 recovery text: "At Report:901 and Report:950, change 'both' to name all three tensions" (`qa/qa-anti-omission-consolidated-findings.md:150`). Pre-patch `/tmp/ao639/report.md:950` shows this resolution text, and `diff` shows that only the Impact cell changed. | Change the phrase to "Preserve the statements on both sides of all three tensions and their historical frames" in the report and in synth-06. |
| AO-V3 | MINOR | `RESEARCH-REPORT-review-loops.md:580` (Option C Support, R32); mirror `synthesis/synth-04-options-recommendation.md:109` | **O-30 misclassifies a finding.** The recovered text lists "cosmetic output (the unused `vhex()` helper, punctuation and grammar)". The primary source classes the unused `vhex()` helper as a preexisting extra, which is a spec-compliance "Extra", not cosmetic output. It is not output at all. The row's own citation of `05-session-e002bed2.md:132` contradicts the label. | `research/05-session-e002bed2.md:132`: "Unused `vhex()` helper. \| **Preexisting extra.**" Cosmetics are separate rows at :135 and :146. `research/evidence-deck.md:534` ("Preexisting extra/output defect") is separate from :549 ("Cosmetics"). | Reword to "cosmetic output (punctuation and grammar) and an unused `vhex()` helper, a preexisting extra" in both files. |
| AO-V4 | MINOR | `RESEARCH-REPORT-review-loops.md:580` (Option C Support, R32); mirror `synthesis/synth-04-options-recommendation.md:109` | **Undebated evidence added to a ranking row without a label.** The O-30 addition goes beyond the debated card. The card carries the any-severity prompt rule and case-insensitive matching. The addition also says prompts told reviewers "to judge every Task 12 requirement bullet directly, so findings mixed requirement violations with exactness problems in commands the requirements suggested (the `git diff --name-only` rename overlap) and cosmetic output". That case-report detail sits in V3's Support row with no "never weighed by the debate" label. This breaks the consolidation's rule that undebated evidence stays out of ranking rows, and the labelling the fixer itself applied to O-23, O-25, O-28 and O-29. | `synthesis/hypothesis-03.md:59` and `reviews/adversarial/merged-root-cause-analysis.md:77` mention only uncapped fields, case-insensitive matching and the any-severity rule. A `grep` for `cosmetic`, `rename`, `exactness` and `requirement bullet` returns 0 hits in `variant-3-original.md`, `debate-transcript.md` and `merged-root-cause-analysis.md`, and `vhex` returns 0 in all five variants. Consolidation :218 and :291 state the rule. | Keep the debated clauses (any-severity, case-insensitive) in Option C Support. Label the mixed-findings clause "case-report detail the debate never weighed", or move it so it appears only in the 2.6 monitor row (Report:278), which already carries it. Make the same change in synth-04. |
| AO-V5 | MINOR | `RESEARCH-REPORT-review-loops.md:553` (Option B Support, R27); mirror `synthesis/synth-04-options-recommendation.md:82` | **O-25 dropped the source's own limit.** The recovery adds N-17 to V2's Support row as "an introduced acceptance-executability gap" but omits the source's opposing qualifier. Step 6.39 required recoveries to preserve opposing evidence. | `research/01-session-ac2cd1fd.md:222`: "Introduced acceptance-executability gap ...; a known local-failure comparison also existed in v2 constraints". `research/evidence-deck.md:446` (limit column): "Earlier local failure comparison also existed; no execution claimed." | Append "; a known local-failure comparison already existed in the v2 constraints, and no execution is claimed" to the clause in both files. |
| AO-V6 | MINOR | `RESEARCH-REPORT-review-loops.md:259`; mirror `synthesis/synth-01-problem-current-state.md:164` | **Location keys the report never defines.** The new 2.5 row cites `Source:158`, `Source:469` and `Session:912`. These keys are the case file's own notation. The report never defines them, and they appear nowhere else in it. Elsewhere the report writes Orca `source.md` lines (Report:580) and "raw" or "record" for session records (Report:159). | `grep -o "Source:[0-9]*\|Session:[0-9]*"` matches only Report:259. The header path convention (Report:12) defines package-relative paths and `ADV/` only. | Write "Orca `source.md` line 158 / line 469" and "planning-session record 912" (`research/01-session-ac2cd1fd.md:259`) in both files. |
| AO-V7 | MINOR | `qa/qa-anti-omission-consolidated-findings.md:243`; `qa/qa-anti-omission-report-3-rerun.md:248-251` | **The accepted P3 rerun counts do not reconcile.** The addendum accepts the rerun as the item-level pass because "its counts reconcile: 256 represented + 33 covered-by-dedup + 1 omitted = 290". Only the 290 total reconciles. The rerun's own table gives 210 R, 76 D, 3 R/D and 1 O. The three dedup range rows alone (E46-E75, E97-E114, E117-E138) hold 70 items, more than the stated 33. This is the same class of count failure recorded against the original P3 report under PF-01. | Counted from the rerun table (:26-233). R: A17 + B7 + C20 + D34 (E45, E76-E91, E92-E96, E116, E140-E150) + E14 + F15 + G13 + H18 + I11 + J34 + K24 + L3 = 210. D: 30 + 18 + 22 + E139 + E151 + E170 + E177 + E178 + E207 = 76. R/D: E115, E168, E176 = 3. O: E209 = 1. Sum 290. | Append a dated, attributed correction under the addendum (do not rewrite the history above it) stating the recounted split (210 R, 76 D, 3 R/D, 1 O) and noting that the rerun's stated split is wrong. The O-ID set does not change, because every D range was re-adjudicated in the mapping table (addendum :262-277). |

## PASS/FAIL Set History

| Set | Cycle 0 (consolidation, Step 6.38 plus addendum) | This verification (after the Step 6.39 recovery) |
|---|---|---|
| Omissions to recover | FAIL: 34 (IMPORTANT O-01, O-02, O-04, O-05; MINOR O-03, O-06, O-07, O-09 to O-13, O-15 to O-36) | PASS: 31 (O-01, O-02, O-03, O-04, O-06, O-07, O-09, O-10, O-11, O-12, O-13, O-15, O-16, O-17, O-18, O-19, O-20, O-21, O-22, O-23, O-24, O-26, O-27, O-28, O-29, O-31, O-32, O-33, O-34, O-35, O-36). FAIL: 3 (O-05: AO-V1, AO-V2, AO-V6; O-25: AO-V5; O-30: AO-V3, AO-V4) |
| Dedup | O-08, O-14 adjudicated DEDUP | Still DEDUP, rationale confirmed (check 5) |
| Process findings | PF-01 (IMPORTANT), PF-02 (MINOR) | PF-01 is resolved for coverage by the rerun plus the addendum, but its count-reconciliation part recurs in the accepted rerun (AO-V7). PF-02 stays on record against the historical P3 report, which is not rewritten. |
| Cycle-0 PASS set | P1 154 R + 51 dedup; P2 225 R + 56 dedup (including out-of-scope rows 252 and 287 under `BUILD-REQUEST.md:14,35`); P4 383 REP + 20 DEDUP (including L08, R06, R08, R11, Q07, A69, A95, A96 and the debate outcomes V1 5/5, V3 above V2 3/5, V4 above V5 3/5 with V5 above V4 displayed at 2/5). P3 none, later replaced by the rerun items the addendum agreed with. | All hold. No PASS item regressed (diff check 3; Section 7 identical). |
| Failure count | 36 (34 omissions + PF-01 + PF-02) | 7 (AO-V1 to AO-V7). This is a strict decrease, so neither the monotonicity guard nor the regression guard is triggered. |

## Actions Taken

None. This verification was report-only, and I edited no file.

## Recommendations

- Run one serialized fixer for anti-omission fix cycle 2 to apply the six report and component wording fixes (AO-V1 to AO-V6), mirroring each into synth-01, synth-04 and synth-06 at the lines listed. Add the dated count correction for AO-V7 to the consolidation as an attributed addendum. Then run fresh Steps 6.40 and 6.41 verifiers on the result.
- AO-V1, AO-V2 and AO-V6 change Section 2.5 and Question 6. AO-V3 and AO-V4 change Option C Support, a ranking row. Recheck the affected report-gate and fidelity checks on the corrected text. None of these fixes should change the order V1 > V3 > V2 > V5 > V4 or the tallies.
- For the user (not a finding, because J1 is user-accepted): the 10.10 note (Report:1293) now records that the anti-omission recovery ran, while the header (Report:5) and 10.9 (Report:1241) still say the anti-omission gate "has not run". That makes the known J1 staleness more visible.

## QA Complete

| Status | Result |
|---|---|
| DONE | Verified report identity (`37753a81…`, 1,316 lines) and all six component after-hashes. Diffed against the pre-patch `a10cef08…` copy: only the 30 patched hunks changed, and Section 7 through 7.2 is byte-identical. |
| DONE | Checked all 36 O-IDs against their live primary sources, including both decoded rubric texts. 31 recoveries are correct, 2 dedups are confirmed, and 3 recoveries (O-05, O-25, O-30) are defective. |
| DONE | Confirmed that every enumeration row in P1, P2, P4 and the P3 rerun has a disposition and that no source family is unowned. Confirmed the O-04/O-05 placement condition and the O-25/O-28/O-29 labelling condition. Found that the accepted rerun's R/D split does not reconcile. |
| NEXT | Anti-omission fix cycle 2: correct AO-V1 to AO-V7 in the report, synth-01, synth-04, synth-06 and the consolidation addendum, then run fresh Step 6.40 and 6.41 verification. |