# QA Report — Anti-omission Verification (Content Quality)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** report-qualitative (fix-cycle verification of anti-omission fixes)
**Fix cycle:** 1
**Fix authorization:** false (report only)
**Status:** Complete
**Overall Verdict: FAIL** (2 blocking findings, see Issues Found)

Inputs: RESEARCH-REPORT-issue-watcher.md, qa/qa-anti-omission-consolidated-findings.md, qa/qa-anti-omission-fix-log.md

---

## Check log (appended incrementally)

Report path reviewed: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` (line numbers below are from this review's reads, 2026-11-07).
Sources re-read: `research/03-governance-and-security-surface.md` line 84 (O-05 source), `research/01-claim-flow-and-session-launch.md` lines 150-159 (O-04 source).

### C1. O-05 fidelity (Section 2.2 row, report line 277; Section 7.9 item 5, line 1428)
- Source R03 line 84: the help-output list is `--agent --worktree --prompt --model --effort --surface`; "one free-text argument; no flag for a permission mode or an allowed-tool list. [OBSERVED]".
- Report row 277 states the same, tags the fact [OBSERVED] and the per-host mechanism [UNVERIFIED]. The Invocation row 271 adds `--focus`, `--retry-launch`, `--json`; none concerns permissions, so the row is consistent. PASS on fidelity and evidence level.
- Minor wording note: "cannot be set from the launch call" is a reasonable inference from the flag list, and is hedged by the [UNVERIFIED] tag on the per-host source.

### C2. O-04 fidelity and scope of the estimate (lines 499, 962, 1319, 1429, 1806, 2047)
- Source R01 line 155 gives the estimate ("seconds to minutes", "possible but not frequent") in the paragraph headed "Race: two workspaces with DIFFERENT logins". The same-login race is the separate paragraph at line 159, with a different window (Wave 1 until the Wave 6 comment) and no estimate.
- All six report places label the figure an estimate from reading the code and not measured. No place presents it as a measurement. PASS on the estimate-versus-measurement point.
- FAIL on scope: see issue B1 below (the estimate is attached to the same-login case in three places).

### C3. Cross-section consistency of the recovered O-04 text
- 2.4 (499), 6 revisit table cond. 4 (1319), 7.9 item 6 (1429), second revisit copy (1806): same figure, same qualifiers, consistent with each other and with "was not measured" elsewhere. No contradiction with Sections 4, 6, 7, 8 found (G7 row 690 and 5.12 row 880 keep "not measured" without the estimate; omission only, no contradiction).
- 5.15 row 4 (962) and Appendix A.2 Q3 (2047) differ in scope from Section 6 cond. 4 (see B1).

### C4. Does the fix log place the edits where it says? (verification of the fix log itself)
- Fix log says O-04 was added to the "Section 9 gap table, Q3 row". Line 2047 is in Appendix A.2 ("Carried to Open Questions", synthesis-02 carry-forward list), whose numbers the report itself calls local (report line 139: "Qn is always a row of the Section 9.2 open-question table; the Appendix A numbers are local").
- The real Section 9.2 rows on these subjects were not edited: Q13 (line 1867: "the real race window between claim Wave 1 and Wave 3, which was not measured", the exact row the consolidated finding named) and Q6 (line 1860: permission mode of the launched session, the row the consolidated finding named for O-05).
- Fix log states "The Section 9 'Q6' row is about where the poller runs, not permission mode". That is true only of Appendix A.2 Q6 (line 2050); Section 9.2 Q6 (line 1860) is the permission-mode row. The log misread the numbering and the O-05 recovery therefore never reached Section 9.2 Q6.
- The consolidated findings allowed "Section 2.2 or the Q6 row", and "Q13 row and/or the at-most-once discussion and revisit condition 4", so the original dispositions are met. The problem is chain reflection (C5), not the disposition.

### C5. Chain reflection: do the recovered facts reach the gap and plan chain where they warrant action?
- Plan step 1.10 (line 1545) tells the design doc to "copy the open rows of Section 9 of this report" and step 1.6 (line 1541) cites Q6 for the permission-mode risk. Section 9.2 Q6 (line 1860) says only that applying `agentDefaultArgs` "was not traced" and suggests "trace the CLI route"; it does not say that the launch call has no permission-mode or allowed-tools flag. G14 (line 697) likewise.
- Phase 3 preamble contract table (lines 1574-1586), from which step 1.8 builds the design-doc contract, has no row for permission mode or allowed tools, while the Section 2.2 table it duplicates now has one (line 277). The two copies of the same contract now differ.
- Section 9.2 Q13 (line 1867) keeps "was not measured" with no estimate while 2.4, 6, 7.9 and 5.15 carry it.

### C6. Addendum conformance and content rules (checks a, b, c of the prompt)
- Option A decided by the owner: 1.1 D1 (line 135), 7.1 (line 1336, "decided by the owner (ADDENDUM 2)"), headings 6.1 "Decided by the owner" (1058), 6.2 and 6.3 "Documented alternative" (1117, 1169). Intact.
- B and C scored with revisit conditions: Requirement Scoring (1257), Options Comparison (1293), nine-condition revisit table (1310-1328), 7.2 row "What the score does and does not say" (1351). Intact.
- Coder#477: 1.2 (lines 143-149) with repo boundary and "Option A makes #477 unnecessary unless B or C is revisited"; 7.7 (1414) same; 9.1 D5 (1846); G18 (701); table note line 1326. Intact.
- Integer-only prompt rule: 1.1 D3 (137), 7.3 Prompt row (1362), G12 (695), 9.1 D3 (1844). Intact. Claim-only D2: 1.1 (136), 7.3 (1355). Intact.
- Scannability: the 8 edits are one new table row and 7 added clauses inside existing cells or one paragraph; no new full source code, no new section, no prose-over-table change. PASS. Minor note: the added clauses lengthen already long table cells (lines 1319, 1429).
- No `[CONTRADICTION` marker anywhere in the report (fix log claim; consistent with my reads).

## Issues Found

| # | Severity | Blocking | Location | Issue | Required Fix |
|---|---|---|---|---|---|
| B1 | IMPORTANT | yes | Report lines 962 (5.15 row 4), 2047 (Appendix A.2 Q3), and by pairing 1319 and 1806 (Section 6 and Section 8 cond. 4) | The R01 section 9 estimate (window "seconds to minutes", collision "possible but not frequent") was made for the two-different-logins race (R01 line 155). R01 treats the same-login race separately (line 159): its window runs from Wave 1 to the Wave 6 comment, so it is longer, and R01 gives no estimate for it. The report attaches the estimate to "The same login in several workspaces" (962) and to "Same-login several-workspace polling" (2047), and to a condition that names the same login first (1319, 1806). A reader will take the "not frequent" estimate as covering the same-login case, which understates that case. Also, 962 (same login only) and 1319 (same login or two logins) differ in scope for the "same nine items". | State the scope in each place: "R01 section 9 estimates the two-login race window at seconds to minutes and a collision as possible but not frequent (from reading the code, not measured); R01 gives no estimate for the same-login case, whose window runs from Wave 1 to the Wave 6 comment". Apply to 962, 1319, 1806, 2047 (and keep 499, 1429 as they are, since they speak of the Wave 1 to Wave 3 window of the cross-login race). |
| B2 | IMPORTANT | yes | Report line 1860 (9.2 Q6), 697 (G14), 1574-1586 (Phase 3 contract table); fix log lines 26 and 39 | The recovered O-05 fact (no permission-mode or allowed-tools flag on `orca agent launch`) sits only in Section 2.2 and Section 7.9 item 5. Section 9.2 Q6, which plan steps 1.6 and 1.10 copy into the design doc, and the Phase 3 contract table (a duplicate of the 2.2 table that step 1.8 uses) do not carry it, so the design doc and the mock contract will omit it. The fix log's account of where it edited is wrong: it treats the Appendix A.2 local numbers (Q3, Q4) as the "Section 9" rows and says Section 9 Q6 is about the poller host, which is false for Section 9.2 Q6. | Add one clause to 9.2 Q6 (and to G14 or its Notes): "the launch call has no permission-mode or allowed-tools flag, so the posture must come from the host (ccsession, Orca settings); [OBSERVED]", and add the matching row to the Phase 3 contract table. Correct the fix log's numbering note. |

Minor notes (not blocking, not rechecked):
- N1. Section 9.2 Q13 (line 1867) and Section 4 G7 (line 690) say "not measured" without the R01 estimate; add the clause for symmetry with 7.9 item 6.
- N2. The 2.4/7.9 clauses present the collision estimate without the premise that multi-assignee behaviour is itself unobserved (Q14 carries it). Consider "if multi-assignee holds (UNVERIFIED)".
- N3. Appendix A.2 Q3 mixes the same-login subject with the cross-login window (covered by B1).
- N4. About 25 minor omissions remain unrecovered by design (per the consolidated file); not rechecked.

## Items Reviewed (report-qualitative checklist, adapted to a recovery-fix review)
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement and decisions intact | PASS | C6: 1.1 D1-D3, 1.2 |
| 2 | Current state describes what the sources say | FAIL | C2/B1: R01 line 155 vs 159 against report 962, 2047 |
| 3 | Options still distinct and scored | PASS | C6: lines 1257-1328 |
| 4 | Recommendation follows from analysis (A decided, B/C scored) | PASS | C6: 7.1, 7.2 |
| 5 | Plan actionable and consistent with recovered facts | FAIL | C5/B2: Phase 3 table 1574-1586, step 1.10 |
| 6 | Gaps honest (estimate vs measurement, verified vs not) | PASS | C2: six places all say estimate, not measured; [OBSERVED]/[UNVERIFIED] split kept in row 277 |
| 7 | External research relevant | PASS | No external research touched by the fix; none needed (Tavily not used) |
| 8 | Scale claims substantiated | PASS | Estimate labelled as derived from code (C2) |
| 9 | Risk assessment complete | FAIL | B1 understates same-login risk; B2 permission posture not in Q6 |
| 10 | Evidence trail complete | FAIL | C4: fix log misstates where edits went |
| 11 | No circular reasoning | PASS | Recovered text cites R01/R03 sources, re-read at lines 155 and 84 |
| 12 | Conclusion proportionate | PASS | "possible but not frequent" kept as an estimate; no upgrade to measured |

## Summary
- Checks passed: 8 / 12
- Checks failed: 4 (all trace to B1, B2)
- Critical issues: 0
- Blocking issues: 2 (B1, B2; both IMPORTANT)
- Issues fixed in-place: 0 (report only)

## Self-Audit
**(a) Reliance list:** No Inherited Structural Verdict was supplied; no structural PASS was relied on. The fix log's own claims (8 grep hits, 0 `[CONTRADICTION`, row positions) were treated as claims and re-checked, not relied on.

**(b) Independent semantic checks:**
- O-04 fidelity: Read R01 lines 150-159 and compared with report lines 499, 962, 1319, 1429, 1806, 2047 (found the scope mismatch B1).
- O-05 fidelity: Read R03 lines 78-90 and compared with report lines 271-278 and 1428.
- Fix-log location claims: Read report 1834-1890 and Grep for `Q6|Q13`; found the log's "Section 9" edits are in Appendix A.2 and its Q6 reading is wrong (C4).
- Plan-chain reflection: Read report 1538-1546 and 1567-1586 (C5).
- Addendum conformance: Read report 100-151, 1308-1442 (C6).
- Factual claims independently verified: about 30. Files read: the report (many ranges), fix log, consolidated findings, R01, R03. Ran no tests (document review).
- 0 issues was not the result: 2 blocking and 4 minor notes.

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (verification coverage; the verdict is FAIL on content findings, not on coverage).
**Tool engagement:** Read: 14 | Grep: 8 | Glob: 0 | Bash: 0 (Edit/Write: report only). Tavily: not used (no external lookup needed).

## Recommendations
1. Fix B1: scope the R01 estimate to the two-login race in 962, 1319, 1806 and 2047; say that R01 gives no estimate for the same-login case.
2. Fix B2: add the "no permission-mode or allowed-tools flag" clause to 9.2 Q6 and G14, add the matching row to the Phase 3 contract table, and correct the fix log numbering note.
3. Optional (N1): add the estimate clause to 9.2 Q13 and G7.
4. This is the first review of fix cycle 1; after these fixes one more verification cycle remains within the 2-fix-cycle limit.

## QA Complete

Status: Complete

VERDICT: FAIL

