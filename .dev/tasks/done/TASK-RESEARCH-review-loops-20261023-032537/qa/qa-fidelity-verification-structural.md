# QA Report: Phase 6 Source-Fidelity Verification, Structural

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks (`R/RESEARCH-REPORT-review-loops.md`)
**Date:** 2026-10-24
**Task step:** 6.30 (independent structural fidelity verification)
**Phase:** fidelity verification, fix cycle 1 of 2
**Lens:** structural source fidelity: each original finding rechecked, frozen PASS identities checked for regression, corrected detail, chronology, counts and classes checked across all four partitions
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Mode:** report-only (`fix_authorization: false`). I edited no file and ran no Git command. I did not open the parent session log `dfade920-…jsonl`. I read the other JSONL logs only by record number.
**Report under review:** `R/RESEARCH-REPORT-review-loops.md`, 1,313 lines. I re-measured its sha256 as `a94475caee954ae9942c4b4e8d609e4fc4bfb898fa134026045c78657f18ccf2`, which matches.
**Changed files:** all six re-measured, and each matches the after-hash in the fix log (`qa/qa-fidelity-fix-log.md:74-79`):
- report `a94475ca…`
- `synth-01` `8d9c4db1…`
- `synth-02` `bcc1bdb3…`
- `synth-04` `f0e20bd9…`
- `gaps-and-questions.md` `9a688abf…`
- `research/04-session-43582de1.md` `b89b16d7…`

**Templates read first:**
- `/config/.claude/skills/tech-research/SKILL.md:1153-1194` (fidelity prompt and report format)
- `/config/.claude/skills/task/SKILL.md:466-506` (standard QA report format)
- task file Step 6.30 (`R/TASK-RESEARCH-review-loops-20261023-032537.md:495`)

**Known defect J1 (not counted):** the stale status lines. Because the fix inserted three report lines, they are now at Report:5, :1238 and :1290 (formerly :5, :1235 and :1287). The user accepted this defect, and it is not a finding here.

---

## Overall Verdict

Verdict: FAIL

- **Original findings:** nine of the ten (F-01 to F-03 and F-05 to F-10) are corrected, and primary evidence confirms each correction. F-04 is still open: its corrected 7.7 pointer still credits Section 4 with content Section 4 does not contain.
- **New defects introduced or exposed by this cycle:** four.
  - **N-01 (IMPORTANT):** a third set of Phase 2 Git reads is undisclosed. The corrected Report:904 now claims a complete list of two.
  - **N-03 (IMPORTANT):** the insertion-only edits to case 04 shifted its line numbers by +3 or +5. This broke report citations that were correct at cycle 0, and it made the new F-07 citations wrong from the moment they were applied.
  - **N-04 (MINOR):** the same shift problem in `gaps-and-questions.md`.
  - **N-05 (MINOR):** the new contradiction row says no source itemizes the final partial pair, but the final merged verdict names one member of it.
- **Regression:** frozen identity P3-C11 was PASS at cycle 0 and now FAILs, because its case-04 anchors moved (details under N-03).
- **Ranking:** the ranks, the order V1 > V3 > V2 > V5 > V4 and all pair tallies are unchanged.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Report and changed-file identity | PASS | `sha256sum` of all six files matches the fix-log after-hashes. The report has 1,313 lines. |
| 2 | F-01 plan-version replay row | PASS | Orca log `ac2cd1fd…jsonl`, recomputed from the records: Write 141 = `648c5578`; Write 141 plus Edit 163 (one occurrence, `replace_all` false) = `ebc03d45`, which equals the first `input-snapshot.yaml:6`; Write 544 = `d3a12ef9`, which equals the second `input-snapshot.yaml:6`; Write 841 = `cbfb606a`. Record 151 is the freshness-hook block of Edit 150. Record 163 is the narrowed retry of the same wording change. Report:846. |
| 3 | F-02 criterion disclosure | PASS | The quotes match `BUILD-REQUEST.md:12` ("ranked most to least likely") and `:34`, and `diff-analysis.md:64,69`. The user acceptance is in task log entry `[2026-10-24T06:32Z]` (task file :683). Report:88, :90, :716. |
| 4 | F-03 who skipped the Phase 5 review | PASS | Task file :645 ("Parent judgment … NOT run") and `synthesis-gate-decision.md:65` match Report:10 and :1236. |
| 5 | F-04 coverage pointers and the authorized no-review v4 edit | FAIL (residual) | Records 858 (user: "have one fresh reviewer check only N-01 and N-12 against plan v3"), 885 ("without another review … per-task reviewer will hold each task to it") and 889 (user: "make the small edit") support Report:165 and :271. Report:768 also credits Section 4 with the authorization content, and Report:379 does not contain it. |
| 6 | F-05 case-03 Coder Git disclosure | PASS for its defined scope | `research/03-session-6f744b87.md:121-131,212-250` and `report-gate-decision.md:115` support Report:8, :324, :614 and :904. The clause "(not the Coder trees named in Option D)" is gone. |
| 7 | Undisclosed Git reads, swept across all six case files | FAIL (N-01) | `research/06-session-0690ee9f.md:94,283,292-293` records a separate Phase 2 inspection of Coder Git objects that the report does not disclose. The other case files show no further Git object reads (grep sweep). |
| 8 | F-06 reviewer identity | PASS | Documentation records 204, 222 and 234 carry the same agent id `a728a634771049499`. Record 234 contains "relying on your account". Report:167. |
| 9 | F-07 the CI 16/2 count survived debate | PASS for the defect | Records: 821 (03:24:28.367Z; "16 are fixed and 2 are only partly fixed", "ready with notes"); 1052 (03:46:28.426Z, Write of `REPORT.md` with "fixes 16 of the 18 … other 2 in part"); 1084 (03:48:11.615Z, the same count told to the user). Debate files: `round2-v1.md:5` (R1-3 concession), `:16` and `:33`; `merged-verdict.yaml:8`; `consensus-summary.md:3`. Report:168, :254, :274, :349, :382. |
| 10 | F-08 monitor skill-load time | PASS | Monitor records 14 (19:29:17.282Z, user command), 40 (19:29:22.409Z, Skill call), 42 (19:29:22.708Z) and 58 (19:29:28.357Z). Report:580. |
| 11 | F-09 historical `ledger.md` bytes | PASS | Record 873 is a Read at 20:34:06.131Z. Record 874's `toolUseResult.file` has `filePath` = installed `ledger.md`, `startLine` 1, `numLines` 243, `totalLines` 243, and content sha256 `bd66451d…`. Compared with the current installed copy, the only difference is line 3. Report:580. |
| 12 | F-10 provenance class (scope-rules, scope-02, 04, 05) | PASS | Rule-map record 79 (03:31:40.642Z) is a 13,299-character status-table return with no `0b533765` and no "Recovered historical" section. `scope-rules.md:1,11,47,64`; `qa-phase-2-fix-log.md:487-514`. `scope-02/04/05.md:8,11` and the capture bounds `screening-handoffs-source.txt:9-195,214-382,386-443`. Report:1240, :1245, :1246. |
| 13 | Case-04 edits are insertion-only and attributed | PASS | `sed '119,121d;298,299d' research/04… \| sha256sum` = `661d0604…`, the fix-log before-hash. Both blocks are dated and attributed to Step 6.29 / F-07. |
| 14 | Gap-register edit is insertion-only and attributed | PASS | `sed '36,37d' gaps-and-questions.md \| sha256sum` = `0c4904e5…`, the before-hash. The marker is attributed. |
| 15 | Citation integrity after the insertions | FAIL (N-03, N-04) | Current lines of case 04: 133, 146, 148, 170, 210, 243, 247, 297, 366, 410, 475-476, 598. Gap register: 56, 58, 61. Mapping in Issues Found. |
| 16 | New marker's "unrecoverable" claims against the final merged verdict | FAIL (N-05) | Second-review `merged-verdict.yaml:154` (M-06): "(the M-05 fix is partial)". |
| 17 | Ranks, order and tallies unchanged | PASS | Report: "V1 > V3 > V2 > V5 > V4" ×5, "3 of 5" ×6, "2 of 5" ×5, "5 of 5" ×4. synth-04: ×3, ×4, ×4, ×3. 7.1 and 7.2 unchanged, and they match `debate-transcript.md:477-484`. |
| 18 | Frozen cycle-0 PASS identities (regression) | FAIL (P3-C11) | See the PASS/FAIL Set History. |
| 19 | Placeholders | PASS | Grep for `TODO`, `TBD`, `FIXME`, `{{`, `RF_PLACEHOLDER` and `XXX` over the report, synth-01/02/04 and the gap register: no hits. |
| 20 | Table integrity of changed rows | PASS | Pipe counts on 29 changed rows and their headers agree (for example 254:4/251:4, 716:4/713:4, 846:6/842:6). |
| 21 | J1 untouched | PASS | Report:5, :1238 and :1290 are unchanged in substance. No patch targeted them. |
| 22 | Synthesis mirrors carry the same text | PASS | The hash match proves exact application. Grep confirms the patched strings in synth-01 (7 lines), synth-02 (2) and synth-04 (lines 248 and 300). The same residual defects repeat there (noted per issue). |

## Summary

- Checks: 22 run, 16 PASS, 6 FAIL (items 5, 7, 15 (covers N-03 and N-04), 16, 18).
- Original findings: 9 of 10 PASS. F-04 still FAILs (MINOR).
- New findings: 4 (N-01 IMPORTANT, N-03 IMPORTANT, N-04 MINOR, N-05 MINOR). No CRITICAL findings.
- Open after this cycle: |F_1| = 5 (F-04, N-01, N-03, N-04, N-05), against |F_0| = 10.
- Frozen identities: 70 enumerated, 69 hold, 1 regressed (P3-C11).
- Rank impact: none from any required correction. N-01 changes support for ranked cause V4 only if the user chooses to remove the case-06 Git evidence.
- **Confidence:** Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Limits: I read synth-01/02/04 through the hash match plus targeted greps, not line by line. I read case 04 in its changed regions plus a full line map, not every line.
- **Tool engagement:** Read: 23 | Grep: 0 (searches ran inside Bash) | Glob: 0 | Bash: 39. The Bash calls were read-only `sed`, `grep`, `wc`, `sha256sum` and `find`, plus `uv run --no-project python` readers that wrote no file. No web research.

## Issues Found

| ID | Severity | Location path:line | Issue | Primary evidence | Required fix |
|---|---|---|---|---|---|
| F-04 (residual) | MINOR | `R/RESEARCH-REPORT-review-loops.md:768`; mirror `R/synthesis/synth-04-options-recommendation.md:300` | The correction added: "The authorized narrowing and the authorized unreviewed v4 edit (raw 858, 885, 889) are in Section 2.2 (Orca row) and Section 4 (Key Takeaway Coverage, Orca planning row)". Section 2.2 does carry this (Report:165). Section 4's Orca row (Report:379) says only "narrowed review and unreviewed final amendment". It has no authorization, no no-review recommendation and no record ids. This is the same pointer overclaim F-04 targeted. | Orca records 858, 885 and 889 (texts in Items Reviewed #5); Report:379. | Point only to Section 2.2 for the authorization, or say that Section 4 records the narrowing and the unreviewed amendment without their authorization. Apply the same change to synth-04:300. |
| N-01 | IMPORTANT | Report:8 (Scope), :324 (Constraints), :904 ("None was performed here, except two disclosed sets of read-only Git reads"). Claims that depend on it: :170, :276, :346, :604 | **Undisclosed third set of Git reads.** The case-06 (credential) analyst also inspected Coder Git objects during Phase 2. It used tree `7ac64e6a91f624362b19daf46ea9544ad8a4edcd` to confirm that historical README line 161 was a table separator (case 06:94). It used tree `d9f262a48f82c55b18f883826428f2fd8d2d7be5` for the historical task-body check (case 06:277,283). Its controls state "performed read-only transcript parsing, hashing and Git object inspection" (case 06:292-293). The report relies on these reads for the README-separator citation (:604, :346, :170) and for the narrow task-body omission that qualifies the pass (:170, :276). The corrected :904 now claims a complete list, and that claim is false. No authorization is on record. The 06:32Z decision was asked on F-05, which named only the case-03 objects. No earlier fidelity review flagged this. The source map lists these trees as "Reached only through the case files". | `R/research/06-session-0690ee9f.md:94,277,283,292-293`; `R/phase-outputs/discovery/fidelity-source-map.md:288`; `R/qa/qa-fidelity-consolidated-findings.md:79-85`; task file :683 | At :8, :324 and :904, disclose the case-06 analyst's read-only inspection of the two Coder trees during Phase 2. Cite case 06:94,283,292-293, state that no authorization is on record, and correct "two disclosed sets". Get the user's ruling on whether the 06:32Z "Keep, disclosed" covers these reads, or a separate keep/remove decision. Removal would weaken V4's Option D support and the task-body qualification, and under Step 6.29 it would reopen the affected gates. |
| N-03 | IMPORTANT | Report:848, :951, :872, :873, :254, :349, :281, :151, :168; mirrors synth-01:56,73,159,186, synth-02:54, `gaps-and-questions.md:37` | **The insertion-only edits to case 04 broke line citations into it.** C-01 added 3 lines after old line 118, and C-02 added 2 lines after old line 294. So old lines 119-294 moved down by 3, and old lines 295 onward moved down by 5. Citations that were correct at cycle 0 now point to the wrong lines:<br>• :848 "research/04:470-471": now a blank line and a table header (the hashes are at 475-476).<br>• :951 ":593": now blank (the package is named at 598).<br>• :872 "line 167": now blank (heading at 170).<br>• :872 "line 405": now blank (heading at 410).<br>• :873 "line 207": now a bullet (heading at 210).<br>• :349 ":240,244": now blank lines (items at 243 and 247).<br>The new F-07 citations used pre-insertion numbers, so they were wrong as soon as they were applied:<br>• :254 ":130": now M-02 (M-05 is at 133).<br>• :254 ":143": now M-15 (M-18 is at 146).<br>• :254 ":145": now M-17 (the concession is at 148).<br>• :254 ":294": now a bullet (the sentence is at 297).<br>• :254 and :349 ":361": now blank ("The final report repeats" is at 366).<br>• gaps:37 carries the same stale numbers.<br>The ranges at :151, :168 and :281 drift by 3 to 5 lines. This causes the P3-C11 regression. | The removal-and-hash check (Items Reviewed #13) proves the shift. Current case-04 lines 133, 146, 148, 170, 210, 243, 247, 297, 366, 410, 475-476 and 598. | Preferred: move the C-01 marker and the C-02 erratum into one dated, attributed block appended at the end of `research/04-session-43582de1.md`. That keeps the edit insertion-only, restores every original line number (all the citations above, including the new F-07 ones, become correct again) and needs no report rewrite. Then re-point the markers' own "see …" references. Alternative: update every listed citation in the report, synth-01, synth-02 and gaps:37. Either way, re-verify P3-C11. |
| N-04 | MINOR | Report:530 and :749 (":56"), :256 (":35,59"), :345 (":57-59"); ranges at :258, :281, :297, :331, :352, :389, :414, :460, :836, :879, :910, :966; mirrors synth-01:161,163,186,202, synth-02:38,50,57,94, synth-03:28,80, synth-04:62,281, synth-06:34, `research/web-01-gap-applicability.md:36,38,40,49,81,85` | **The gap-register insertion broke line citations into it.** G-01 added 2 lines after line 35, so old lines 36-65 moved down by 2.<br>• ":56" (the dated three-equal/four-different comparison) now resolves to the table separator; the row is at :58.<br>• ":59" (the "Orca source contradictions resolved?" row) now resolves to the reviewer-miss row; the row is at :61.<br>• Ranges ending at old line 59 or 63 now leave out their last rows. | `sed '36,37d' gaps-and-questions.md \| sha256sum` = `0c4904e5…`. Pre-patch :56 is "Are installed and checkout protocol copies still identical?" and pre-patch :59 is "Were the historical Orca source contradictions resolved?". The current :56 is a table separator line. | Move the G-01 marker to a dated block at the end of `gaps-and-questions.md`. That restores every cited number, including web-01's, without editing research originals. Update Report:254's pointer "gaps-and-questions.md (Unresolved Contradictions)" to the new location. |
| N-05 | MINOR | Report:254; mirror synth-01:159 | The new 2.5 row says: "Do not choose which two findings the final count treats as partial: no surviving source itemizes them." The final debate-merged verdict of the second CI review records one of the two: its finding M-06 ends "Task 9 mentions `MISSING` only for deletions (the M-05 fix is partial)". Read in context (rename handling), this is cycle-0 M-05, which case 04 marks partial at current :133. Only the second partial is unrecoverable. | Second-review `adversarial/merged-verdict.yaml:146-154` (M-06), `:240-246` (M-11: boundary-guard is optional hardening, "M-10 of cycle 0"); `research/04-session-43582de1.md:133` | State that the final merged verdict records cycle-0 M-05 as partial (`merged-verdict.yaml:154`) and that no surviving source identifies the second partial, so the pair cannot be completed. Keep both statements and the marker. Apply the same wording to synth-01:159. |

## PASS/FAIL Set History

**Original findings (cycle 0 FAIL set, |F_0| = 10):**

| ID | Cycle 0 | Cycle 1 (this verification) | Basis |
|---|---|---|---|
| F-01 | FAIL | PASS | Hashes recomputed from records 141, 163, 544 and 841, matched to both `input-snapshot.yaml` files |
| F-02 | FAIL | PASS | `BUILD-REQUEST.md:12,34`; `diff-analysis.md:64,69`; task file :683 |
| F-03 | FAIL | PASS | Task file :645; `synthesis-gate-decision.md:65` |
| F-04 | FAIL | FAIL (residual at Report:768 and synth-04:300) | Records 858, 885, 889; Report:379 |
| F-05 | FAIL | PASS (case-03 scope); related new N-01 | `research/03…:121-131,212-250` |
| F-06 | FAIL | PASS | Same agent id at records 204, 222, 234 |
| F-07 | FAIL | PASS (count and marker); related new N-03 and N-05 | Records 821, 1052, 1084; `REPORT.md:21`; `round2-v1.md:5,16,33` |
| F-08 | FAIL | PASS | Records 14, 40, 42, 58 |
| F-09 | FAIL | PASS | Records 873, 874; line-3-only diff |
| F-10 | FAIL | PASS (scope-04/05 residual also resolved) | Record 79; `scope-*.md:8,11`; capture bounds |

**New at cycle 1:** N-01 (IMPORTANT), N-03 (IMPORTANT), N-04 (MINOR), N-05 (MINOR). |F_1| = 5.

**Frozen cycle-0 PASS identities:**
- **Count:** the consolidation's own list holds 70 identities: P1 14 (S1-S9, C1-C5), P2 12, P3 25, P4 7, cross-source 12. Its Summary line says "84" (`qa-fidelity-consolidated-findings.md:60`), which does not match the list. Step 6.32 should use the 70 listed identities.
- **Which identities could regress:** only an identity whose report text changed, or whose cited source changed. Among the report's cited sources, only `research/04` and `gaps-and-questions.md` changed (synth hashes are covered by P2-V12).
- **Rechecked against primary evidence:** P1-S1, P1-S3, P1-S7, P1-C5, P2-V8, P2-V10, P2-V12 (Report:1259 now records the Step 6.29 synth changes), P3-C4, P3-C5, P3-C11, P4-H6, XS-R2 and XS-R3 (gap-register :33 and :35 sit before the insertion), XS-R12 (the Report:258 range still covers the moved row :58) and XS-R13.
- **Result:** 69 hold.
- **Regression: P3-C11** (Q7 post-window ledger and plan hashes, `qa-source-fidelity-report-3.md:34`). The claim text is unchanged, but its source links broke. Report:848 "still match research/04-session-43582de1.md:470-471" now resolves to a blank line and a table header (the hashes moved to 475-476). Report:951 ":593" now resolves to a blank line (the package is named at 598). Both links held at cycle 0 (pre-patch lines 470-471 and 593, proven by the before-hash).
- **Monotonicity:** |F_1| = 5 is smaller than |F_0| = 10. The regression takes precedence. Step 6.32 must emit, with real values:
  `Regression detected on Item P3-C11 — previously PASS at cycle 0, now FAIL. Halt overrides monotonicity check.`

## Actions Taken

None. This was a report-only verification. No file was edited, no Git command was run and no memory file was written.

## Recommendations

1. **Step 6.32:** emit the regression halt for P3-C11 and stop for the user. Do not advance to anti-omission.
2. **If the user authorizes a second fix cycle:**
   - Move the two inserted blocks (case 04 C-01/C-02 and gap register G-01) to dated blocks at the end of their files. That clears N-03, N-04 and the P3-C11 regression without touching any other citation.
   - Fix the F-04 pointer.
   - Add the case-06 Git disclosure (N-01) and get the user's keep or remove ruling on it.
   - Correct the N-05 wording.
3. **Fixer contract going forward:** any insertion into a file the report cites by line number must either append at the end of the file or re-resolve every citation into that file.
4. **Infrastructure records (not report defects):** correct the consolidation's "84" to 70. The known `fidelity-source-map.md:299,303` errors remain. These are review records, so they are not counted above.

## QA Complete

**Verdict: FAIL.** Nine of the ten original fidelity defects are corrected and verified against primary records. F-04 has a residual. Four new defects exist (2 IMPORTANT, 2 MINOR), including a third undisclosed set of Phase 2 Git reads. Frozen identity P3-C11 regressed because the case-04 insertions shifted line numbers. The ranks, the order V1 > V3 > V2 > V5 > V4 and all tallies are unchanged.

| Status | Result |
|---|---|
| DONE | Rechecked F-01 to F-10 against primary records: hashes recomputed, records 821/1052/1084/858/885/889/874 and 79 read, agent ids matched. 9 PASS; F-04 residual FAIL. |
| DONE | Found 4 new defects: undisclosed case-06 Coder Git reads (N-01), shifted case-04 citations (N-03), shifted gap-register citations (N-04), overstated "no source itemizes" (N-05). |
| DONE | Checked 70 frozen PASS identities: 69 hold, P3-C11 regressed. Ranks and tallies unchanged. |
| NEXT | Step 6.32 emits the P3-C11 regression halt and asks the user how to proceed. |
| NEXT | If the user authorizes a second fix cycle: append-only relocation of the inserted blocks, the F-04 pointer fix, the N-01 disclosure with a user keep or remove ruling, and the N-05 wording. |