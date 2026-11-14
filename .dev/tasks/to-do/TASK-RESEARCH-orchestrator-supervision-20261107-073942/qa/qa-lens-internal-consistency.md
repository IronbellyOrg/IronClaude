## Internal-Consistency QA Report

**Report:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Phase:** report-lens-internal-consistency
**Date:** 2026-11-07
**Fix authorization:** false (report only)
**Status:** COMPLETE (verdict FAIL; see Summary)

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | 4.2 G-B row (:492); 9.1 row 2 (:1442) | Waiting-kind contradiction (checklist d). :492 says "Waiting on a person" **(a)** comes from `blocked_question`, a non-null `agentWait` **and the frozen-plan test** (`WORKER-CONTRACT.md:133-136`). Everywhere else the frozen plan is kind **(b)** "frozen or blocked by policy": :64, :115, :369, :391 (its own report section, "no question text, ever"), :922 ("(b) frozen plan / policy / foreign ready Task"). An implementer following 4.2 would file frozen plans under (a) and print them in the wrong report section. | At :492, move the frozen-plan test out of (a): "(a) comes from WC-3 `blocked_question` and a non-null `agentWait`; (b) frozen plan (`WORKER-CONTRACT.md:133-136`) is unaffected by G-B." At :1442, label the fallbacks (a) and (b) the same way. |
| 2 | IMPORTANT | 4.3 K1 row (:508) vs 4.5 (:543), 8.1 (:1257 vs :1282), 9.6 (:1584) | GQ-18 (K1) has two statuses. 4.3 lists it as an open non-critical gap whose second-worker check goes "-> Open Questions". 4.5, 8.1 :1282 and 9.6 list it as **resolved**, and the 75/25 tally counts it as resolved. 9.1 has no GQ-18 row, so the "-> Open Questions" pointer in 4.3 resolves nowhere (checklist c and d). | Choose one status. If resolved (as the 75/25 tally says), change :508 to "Resolved for lc16; a second-worker check is a plan step (1.4)" and drop "-> Open Questions". If open, add a 9.1 row and change the tally to 76/24 in 4.5, 9.6, 10 and the header. |
| 3 | IMPORTANT | 3.1 (:329) and 8 step 1.15 (:1198) vs 9.1 row 21 (:1461); [CONTRADICTION] marker :1507 | The `allowed-tools` patterns the plan pins have two forms. :329 and step 1.15 use the space form `Bash(superclaude sweep *)` / `Bash(uv run superclaude sweep *)`. 9.1 row 21 (GQ-26) says "Pin both `Bash(superclaude sweep:*)` and `Bash(uv run superclaude sweep:*)`" (colon form). The marker at :1507 records this correctly and was left in place, but the conflict is unresolved on a value that step 1.15 writes into a file. | Owner or QA chooses one form (scope-03:208-209 and the cited precedent `sc-reflect-protocol/SKILL.md:63-64` should decide), then align :329, step 1.15 and row 21. The marker stays until that choice is recorded. |
| 4 | MINOR | 4.6 CC row (:563) vs 4.5 (:532), 9.1 row 58 (:1499) | The "41 tests" CC row says it is "settled by GQ-84 (M1)". GQ-84 is about fenced exclusion with an unreadable transcript, not a test count, and 9.1 row 58 lists GQ-84 as **open**. The cross-reference points to an unrelated item that is still open. | Cite the GQ or B-item that actually settled the "41 tests" count, or write "count only, not settled". |
| 5 | MINOR | 1 (:9), 4.9 (:641) vs 2/3 (:36) | The research question's class list: :9 and :641 name six (waiting, working, stalled, could not determine, finished, idle). :36 names Section C's seven with fenced and says idle applies to person-started sessions only. These are reconciled only by OQ-13 / 9.4 row 98a. | Add "(six in the question; seven in Section C, see OQ-13 / row 98a)" at :9 and :641. |
| 6 | MINOR | 2.x (:237), 4.x (:433), 6 (:935), 8 step 6 (:1075), (:1214); [CONTRADICTION] marker :1078 | HOW-WE-WORK "Other commands" is cited as `:314-337` in some places and `:318-337` in others. The marker at :1078 flags it and was left in place. It is a citation range only. | Re-read the file and use one range everywhere. |
| 7 | MINOR | 3.1 data sources (:344) vs :156, :444, :909, :1059, :1177, :1188, X-1 (:1373) | The git read forms: :344 allows status, log, branch and rev-parse (four). The other lines allow `stash list` as well ("five read forms"). | Add `stash list` to :344. |
| 8 | MINOR | :456, :555, :1005 vs 2.3 (:157, :162), :1133 | The `~/workspace` hardcoded path is cited at crash-recovery `SKILL.md:25-27`. 2.3 puts the path at `:4` and `:53`, and `:25-27` is the 72 h `--since` default. :1133 cites `:4`, `:25-27` and `:53` together. | Cite `:4`, `:53` for the path, and `:25-27` only for the window. |
| 9 | MINOR | 5.9 (:729, :814) vs 4.6 C1/C2; 9.4 rows 88-89 | ID collision. 5.9 uses its own C1 and C2 for external contradictions; 4.6 and 9.4 use C1 (F1-F12 numbering) and C2 (test file length). A reader following "C1" cannot tell which is meant. | Rename the 5.9 pair (for example E-1 and E-2). |
| 10 | MINOR | 6 A4 rejection table (:1002-1016), :748, :853 vs 4.1 severity rules (:484) | ID collision. The A4 table uses R-1 to R-4; 4.1 defines severity rules R-1 to R-3; 5.10 uses R1-R9. "R4" at :748 and :853 reads like a fourth severity rule. | Rename the A4 reasons (for example AR-1 to AR-4). |
| 11 | MINOR | 4.3 K1-K4 vs 6 K-1 to K-6; :1103 | Near-collision. Gaps K1-K4 and option constraints K-1 to K-6 differ only by a hyphen. :1103 cites "K4", meaning the gap; X-3 (:1061) cites "K-4/K-5", meaning the constraints. | Rename one family (for example OC-1 to OC-6 for the constraints). |
| 12 | MINOR | 4.2 G6 row (:498) vs R-2 list (:484) | G6 says "Retiring G6 needs the owner's decision cited (R-2)", but the gap list under R-2 at :484 does not include G6. | Add G6 to the R-2 list, or cite the rule that does cover it. |
| 13 | MINOR | 2.5 table count (:307) | The row claims "3 [CODE-CONTRADICTED]", but the 2.5 table has only 2 CC tags (sort, partial; omission). The third (scope-04:33 "generated files not read") is not a layout fact in that table. | Write "2 in this table; 1 more at scope-04:33 (row 75)". |
| 14 | MINOR | scope-04 tally (:265) | The tally says "0 UNVERIFIED", but the same paragraph and table keep the Approval mapping [UNVERIFIED] (GQ-34; 9.1 row 29). | Change it to "1 UNVERIFIED (Approval mapping, GQ-34)", or say what the zero counts. |
| 15 | MINOR | :444 | The coordinator-only constraint (never as a worker) is attributed to "(G3)". G3 is the periodic sweep (9.1 row 5); the never-as-worker list is GQ-12 / WC-13 (9.1 row 10). | Cite GQ-12 (or the never-as-worker list) instead of G3. |
| 16 | MINOR | 2.3 (:162) | "otherwise the row is could not determine (Section C rule 2)". In the precedence used everywhere else (2.2, 3.1, 6, step 1.3), could not determine is rule 7; rule 2 is stalled (proved). | Change it to "rule 7". |
| 17 | MINOR | 8 Phase 1 goal (:1156) | "Success criteria SC-1 to SC-16 in synth-02 3.2" points to a source file, not to this report. In the report they are Section 3.2. | Cite "Section 3.2". |
| 18 | MINOR | 4.10 (:629) vs 9.5 (:1573) | :629 maps AMBIGUITIES 1-11 to 13 GQ IDs (GQ-09 to 11, 24, 29, 34, 35, 60 to 63, 66, 67). 9.5 AMB 7 also maps to **GQ-12**, which makes 14. | Add GQ-12 at :629. |
| 19 | MINOR | 7 X-4 (:1062) vs 8.4 X-4 (:1376) | X-4 has two resolutions. Section 7 calls it "Open" and says "the guide's reading is the safer one for stop decisions". 8.4 says "Follow the help reading: null = no wait observed". The operational rule matches (null is never stall proof; absent = could not determine), so it is wording, but the status and the preferred reading conflict. | Use one status and one wording for X-4 in both tables. |
| 20 | MINOR | 8.5 (:1390) vs 9.7 (:1599), 10 (:1615) | 8.5 says synth-02 reflects "C1-C13". Elsewhere the family is C1-C15 (C14 resolved, 9.6; C15 nested workers, 9.1 row 35). | Write "C1-C15". |
| 21 | MINOR | 9.2 heading (:1511) vs rows 65, 71, 74, 78 | The heading says the claims have "no GQ row", but row 65 = GQ-14, row 71 = GQ-21 (9.1 row 16 cites the same `scope-02:165`), row 74 = GQ-28 and row 78 = GQ-53. | Retitle it "claims tagged in research files (some duplicate a GQ row)", or move the duplicates into their GQ rows. |
| 22 | MINOR | 10 synthesis list (:1639-1640) | Reproduced text calls synth-05 "planned; not yet written" and synth-06 "(this file)". The assembler note at :1642 corrects synth-05 only; "(this file)" is false inside the assembled report. | Drop both parentheticals; the assembler note already gives the line counts and mapping. |
| 23 | MINOR | 8.3 (:1354) vs 5.9 D2 (:804), 9.4 row 95 (:1557) | The Nagios KB `kb/article.php?id=72` is cited in 8.3 as support for "tool errors are UNKNOWN". 5.9 D2 quotes the same article: timeouts "should generally NOT be reported as UNKNOWN". The plan rule (timeout = could not determine) is unchanged. | Drop the KB URL from the 8.3 row, or say it is cited as a counter-example. |
| 24 | MINOR | 8.3 (:1359) vs 5.9 D6 (:808); 9.4, 9.7 (:1600) | 8.3 uses agents-fleet coordinator-resilience as support for WC-14 G1/G2. 5.9 D6 rejects that source as "unfetched source, context only". D6 also has no Section 9 row: 9.4 covers D1-D4 and the Grafana row (D5), and 9.7 lists web-01 "D1-D4" only. | Mark the 8.3 row "context only (D6)" and add a 9.4 row for D6, or extend 9.7 to D1-D6. |
| 25 | MINOR | OQ numbering: 4.9 (:616), 7.1 (:1111), 8.2 (:1328-1342), 8.5 (:1391) | The same OQ number means different questions. 4.9 OQ-7 is six versus seven classes; 8.2 OQ-7 is the `allowed-tools` combination; 8.2 OQ-13 is six versus seven. 8.5 says synth-04's "OQ-1 to OQ-10" are reflected in "8.2", which numbers synth-05's questions. The note at :1326 says the 8.2 numbers are local, which explains the numbers but does not make the cross-references resolve. | Prefix the local IDs (for example 4.9-OQ-7, P-OQ-7), or cite only the Section 9 row numbers. |

Checks that passed (no finding):
- G1-G7 map to GQ-04 to GQ-10 the same way in 4.2, 8.1 and 9.1.
- Open and resolved count: 9.1 cites 75 distinct open GQ IDs (counted: GQ-01, 02, 04-06, 08-12, 14-17, 19, 21-41, 43, 44, 46-54, 56-67, 84-95, 97-100), and 9.6 cites 25 resolved (GQ-03, 07, 13, 18, 20, 42, 45, 55, 96, 68-83). That is 100, which matches the header, 4.5, X-6, 8.5 and 10 (`:125`, 75/25). Finding 2 is about the 4.3 status label, not the tally.
- 9.7 gaps-to-row mapping: the scope-01 to 06 entry counts (7, 9, 6, 8, 10, 19) match the GQ IDs listed.
- AMB numbers in the 9.1 rows (GQ-09 AMB 8, GQ-10 AMB 3, GQ-11 AMB 4, GQ-35 AMB 9, GQ-60 to 63 AMB 1, 2, 5, 6, GQ-66 AMB 10, GQ-67 AMB 11) match 9.5. "AMBIGUITY 9" at :1274 matches.
- 8.4 X-1 to X-6 mean the same as Section 7 X-1 to X-6 (except the X-4 wording, finding 19).
- Step 1.17 "OQ-11" (:1205) resolves: 8.2 OQ-11 includes WC-14 versus WC-1 (GQ-11) and G6.
- Evidence Trail counts: 10 lists 8 codebase files (research-notes, scope-01 to 04, 05, 06, 07) and 2 web files, which matches the header's "8 codebase + 2 web research".
- Class precedence diagrams (2.2 :356, 3.1 :369, 6 :922, step 1.3) agree apart from finding 1. Six versus seven is consistently routed to OQ-13 / row 98a.
- NB-4 record: 9.6 (:1583), 10 (:1646, :1651) and X-6 agree (coordinator-approved exception at the Phase 3 gate, resolved by the fix pass, re-checked at Phase 5).
- Both [CONTRADICTION] markers (:1078, :1507) are still in place and were judged in findings 6 and 3. Neither was removed.
- Lines :390-395 starting with `## ` are inside the mock-output code fence and were not treated as headers.

### Summary

- Findings: 25 in total. CRITICAL 0, IMPORTANT 3 (blocking), MINOR 22 (notes).
- Blocking findings: 1 (frozen plan as kind (a) versus (b)), 2 (GQ-18 open versus resolved), 3 (`allowed-tools` colon versus space form, the unresolved [CONTRADICTION] at :1507).
- Checklist: (a) IDs and labels match: FAIL (findings 1, 9-11, 15, 16, 25). (b) Counts agree: PASS for gaps and files; minor count notes 13, 14, 18, 20. (c) Cross-references resolve: FAIL (findings 2, 4, 17, 21, 25). (d) No contradictions: FAIL (findings 1, 2, 3, 19, 23, 24).
- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 17 | Grep: 7 | Glob: 0 | Bash: 0 (plus 1 Write and 4 Edit to this file only). The report was read in full (lines 1-1651, chunks of 150 lines or fewer). Line numbers in findings 4-17 come from those reads; the report was not changed during the review.
- No state-changing command was run. No file except this output was edited.

**Verdict: FAIL** (3 blocking IMPORTANT findings; 22 MINOR findings recorded as notes)

**Status:** COMPLETE
