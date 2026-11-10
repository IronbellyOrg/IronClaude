## Internal-Consistency QA Report

**Report reviewed:** .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md
**Lens:** Internal-Consistency (IDs and labels vs prose, counts across sections, cross-references, contradictions). No other dimension checked.
**Date:** 2026-11-08
**Fix authorization:** false (report only; the report was not modified)

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | §2.5(c) (line 379, marker at line 384), §2.6 item 3 (line 466) vs §4.1 G-26 (line 662), §4.5 (line 735), §3.4 W1-16, §8 Phase 2.2, §8.8 G-26 row, §9.3 R9 (line 1331) | An unresolved `[CONTRADICTION: ...]` assembler marker remains in the delivered report. §2.5(c) and §2.6 item 3 say `git rev-parse --path-format=absolute --git-path hooks/pre-push` was "not exercised" and is [UNVERIFIED]. G-26 says "Answered by web-01 D3", §4.5 says "G-26 resolved", Phase 2.2 says "Resolves G-26", §8.8 marks it Resolved and R9 cites web-01 D3a-e. The report therefore states both "unverified" and "resolved" for the same fact. | Resolve in favour of web-01 D3 (the only source that tested it): reword §2.5(c) to "not exercised in file 04; verified locally in web-01 D3", update the §2.6 item-3 row to match, and delete the marker at line 384 and the "see the [CONTRADICTION]" pointers at lines 466, 662 and 1331. |
| 2 | IMPORTANT | §8.6 Phase 6.7 and marker at line 1140 vs §9 rows 7, 8 and 29 (row 7 at line 1279) | A second unresolved `[CONTRADICTION]` marker. Phase 6.7 names `tests/hooks/test_launch_level_guard_with_identity.py` as the L1 test file and says no other L1 test file was listed. Rows 7, 8 and 29 put the same L1 regression tests in `tests/hooks/test_launch_level_guard.py`. Both files exist (Glob: `tests/hooks/test_launch_level_guard.py`, `test_launch_level_guard_with_identity.py`, `test_launch_level_guard_registration.py`), so the claim "no other L1 test file was listed" is also false in the report's own text. | Choose one target file (or name both with which tests go where) and use it in Phase 6.7 and rows 7, 8 and 29; drop the "no other L1 test file" sentence and the marker at line 1140. |
| 3 | MINOR | §2, §3.3, §8 Phases 1.1, 1.3, 2.1, 2.4, 2.5, 2.6; §4.1 G-33 | Section cross-references into research file 01 disagree. File 01's headings are §3 proc/boot/identify/members, §5 validation fields, §6 publish() and ownership/self-test, §8 dependencies and integration points. The report cites publish() as 01 §6 (lines 233, 430, 548-549, 915, 961) but 01 §3 in Phase 2.1 (line 1088); the ownership and self-test checks as 01 §6 in L-7/SC-18 but 01 §3 in Phases 2.4-2.6 (lines 1091-1093); the three-copy layout and installed entry point as 01 §8 (line 235) but 01 §5 in Phases 1.1 and 1.3 (lines 1074, 1076). Lines 231 and 669 cite 01 §5 for PID namespaces, which is in §3/§7 territory, not the §5 validation-fields section. | Normalise: publish(), ownership and self-test → 01 §6; copies and installed path → 01 §8; PID-namespace caveat → the 01 section that states it. |
| 4 | MINOR | §4.1 G-27 (line 663) vs §8.8 G-27 row (line 1185) and §9 row 24 | G-27 is "Open [UNVERIFIED]" in §4.1 but "Partly resolved" in §8.8 and row 24. | Align the §4.1 status note to "Partly resolved" with the same evidence pointer. |
| 5 | MINOR | §7 (line 1018) vs §4.1 G-6 (line 642); §3.3 line 539, §9 row 1, SC-23 | §7 quotes G-6 as "design choice open: brainstorm decision", but the G-6 row reads only "Design choice open". The decision owner for the same item varies between "owner" and "brainstorm" across §3.3, §7, row 1 and SC-23. | Quote G-6 exactly and name one decision owner everywhere. |
| 6 | MINOR | §6 diagram (line 884) vs §3 W2-5 (line 787) | The same git `path.c` citation is "lines 402-403" in the §6 diagram and "lines 402-405" in W2-5. | Use one range in both places. |
| 7 | MINOR | §5.4 web-01 R6 row | The row includes "a config.worktree hooksPath" test and maps it to SC-6, SC-8, SC-9 and SC-17, but none of those success criteria covers a `config.worktree` hooksPath case. | Add a criterion for it or remap the row to the Phase 6 test item that covers it. |
| 8 | MINOR | §10.1 file 04 row (line 1343) and §9.4 (line 1362) vs §2.5 / §2.6 (lines 407, 435) | §10.1 and §9.4 describe file 04 as "E1-E31, F1-F3", while §2.5/§2.6 cite "F1-F4" and file 04 does contain F4 (`### F4. D19-29`). §9.4 also says "15 of 17 rows are CONFIRMED" for Step 2.5, which does not match the 8-row Step 2.5 table in §2.5. | Change to F1-F4 in both places; restate the count against the table it describes or name the source table. |
| 9 | MINOR | §4.1 G-43 vs §9 row 33 | The two lists of D19 items needing "no code" differ: G-43 includes 21, 23, 27, 29 and 35, row 33 omits them; 41 appears in the settled list but not in G-43's no-code list. | Use one list in both places. |
| 10 | MINOR | §4.1, §8.9 | The same defect carries different severities across gap families: G-12 Important vs L1-3/L1-4 Critical; G-13 Important vs L1-5 Critical; G-14 Important vs BP-4/L1-1 Critical; G-16 Important vs BP-7/L1-6 Critical. §8.9 shows Critical rows "Covered by" Important G rows. The severity rule is disclosed, so this is a readability inconsistency, not a false claim. | Add one sentence in §8.9 stating which family's severity governs, or align the G-row severities. |
| 11 | MINOR | §2.5(a), T-1, SC-1; L-6, W2-9, Phase 2.1 vs Phase 6.4 | E2 is cited in T-1 and SC-1 but is absent from the §2.5(a) experiment table. The same errno is spelled ENOTSUP in L-6, W2-9 and Phase 2.1 but EOPNOTSUPP in Phase 6.4. | Add E2 to the §2.5(a) table; use one errno name. |

### Checks that passed

- Header "4 codebase + 2 web" agrees with §10.1 and §10.2.
- The 24 QA files listed in §10.4 match the `qa/` directory.
- All 43 G-rows (G-1 to G-43) appear in both §4.1 and §8.8.
- The nine synth-01 items match the nine table rows.
- Every ToC entry resolves to a section heading.
- Section 9 row references (1, 2, 3, 12, 14, 15, 16, 23, 24, 26, 28) resolve to rows on the cited topic.
- Option A/B/C labels and their meanings agree between §6 and §7.
- The "Phase 4.4" and "Phase 6.11" cross-references exist.

### Summary

- Total findings: 11
- Critical: 0
- Important: 2
- Minor: 9

Verdict: FAIL (2 important findings: the two unresolved `[CONTRADICTION]` markers; the 9 minor findings are notes)
