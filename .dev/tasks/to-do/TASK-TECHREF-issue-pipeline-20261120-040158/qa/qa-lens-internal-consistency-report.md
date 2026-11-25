# QA Report - Lens: Internal Consistency (Gate 3)

**QA phase:** lens-internal-consistency
**Lens:** internal consistency
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md (2369 lines)
**Date:** 2026-11-20
**Report status:** see last line

---

Result summary: see the line-anchored verdict at the end of this report (4 BLOCKING, 13 MINOR).

Stance applied: assume at least 23 errors in the internal-consistency lens; findings below are only those evidenced by line numbers of the document (2369 lines, read in full in chunks 1-300, 301-600, 601-860, 861-1120, 1120-1369, 1369-1617, 1617-1845, 1846-2045, 2043-2370). Source files under the snapshot were not needed except two read-only existence/grep probes (Glob of tests/hooks/test_require_orca_worktree_agent*.py; Grep of LEASE in cycle.py). Nothing was written under the snapshot.

## Fact table (cross-checked facts, every location where stated)

| # | Fact | Locations and values | Consistent |
|---|------|----------------------|------------|
| 1 | Watcher package size | L207 "8 modules, 4,795 lines" + empty `__init__.py`; L417-424 per-file lines 1406/960/865/404/370/348/312/130 (sum 4795, recomputed); L680-687 same eight values | yes |
| 2 | Watcher module count wording | L207 "8 modules" (+ empty `__init__`); L371 "nine modules"; L689 "nine modules"; L1707, L2156 "exactly nine modules" (test pin); L2019 "eight modules and an empty `__init__.py`" | yes in substance (9 files); wording differs, see M-1 |
| 3 | gh call cap 35 = 32 + 3 reserved; 37 per cycle; 2 idle | L208; L467, L481-482; L631; L799; L904; L1656; L1780; L2076 | yes |
| 4 | Read-only gh calls G1-G7 (7); five `"gh"` literals at github.py 177/183/204/231/255 | L208, L589, L783, L1405, L2021, L2111 | yes |
| 5 | DAY_CAP = 6 per rolling 24 h | L749, L903, L1660, L1569 (24 h window, record.py:443) | yes |
| 6 | MAX_CANDIDATES = 10; MAX_LAUNCHES_PER_CYCLE = 1 dead; 14 constants at cycle.py:34-47 | L480, L731, L879, L939, L1658-1659 (lines 34/35/36 .. 47 reconcile with L1656-1672) | yes |
| 7 | SKEW_WARN_S = 60 (cycle.py:44,774) vs SKEW_TOLERANCE_S = 300 (predicates.py:17,295) | L476, L520, L828, L954, L1471, L1669-1670, L1882 | yes |
| 8 | Deadlines: DEADLINE_TOTAL_S 240, GH_FLOOR_S 5, GH_TIMEOUT_S 20, launch timeout 120, cut-off 120 | L771-773, L801, L904, L1662-1668, L2145 | yes |
| 9 | Lease 60 min, MAX_ATTEMPTS 3, backoff 10 min | L517, L823-826, L1569, L1623, L1674; lease cited to cycle.py:33-47 at L879 but defined in record.py (L1569, L1674) | yes (citation drift, M-5) |
| 10 | Exit codes 0,1,2,3,4,5,6,7,75 and precedence 2,6,7,5,3,4 | L208, L737, L853-865, L1455, L1580-1592, L1724 | yes |
| 11 | 59 reason words; groups 27/17/9/1/4/1 | L208, L685, L917-931 (4+7+5+2+2+5+1+1+17+9+1+4+1 = 59, recomputed), L1600-1604, L1703, L1760, L2107, L2152 | yes |
| 12 | dispatch.json: 7 top-level keys, 17 entry fields, 6 states | L209, L819, L1373, L1714, L2104-2105 (17 field names counted = 17) | yes |
| 13 | Transitions T-1..T-13; T-8/T-9 sweep, T-10/11/12 claimed, T-13 reset | L209, L521-522, L821-829, L2106, L2147 | yes |
| 14 | Launch argv 12 elements (retry argv 14) | L208, L600, L811, L910, L1422-1423, L1567, L2149, L2151, L2076 | yes |
| 15 | Five watcher verbs; exit-1 only from `once` crash and `status` unhealthy | L208, L843, L847-851, L858, L1455-1459, L1594 | yes |
| 16 | 18 `LL-*` block words (16 classes + LL-NOBIND + LL-BROKEN); 10 classes block at every level | L213, L646-647, L1253, L1612, L1704, L1847, L2126-2127 (counted 18 and 10) | yes |
| 17 | Guard levels W, WA, F, FS; 16 matrix cells | L201, L1218-1227, L2095-2099 | yes |
| 18 | Guard registrations: guard twice, identity once, timeout 5 | L395, L326, L1278-1280, L1491-1492, L2172; L2029 says "registered once each" | NO, see F-4 |
| 19 | hooks.json 192 lines; plugin copy 154 | L213, L437, L1178, L1482, L1496 | yes |
| 20 | Script sizes 808 / 582 / 208; install_hooks 614; install_ccsession 161; ccsession-orca 263 | L213, L434-439, L1163-1165, L1176-1180 | yes |
| 21 | WORKER-CONTRACT 339 lines; WC-2..WC-16 = 15 rules; no WC-1, no WC-17; test file 3,220 lines / 59 tests | L215, L440, L1328-1346, L1358-1360, L1922, L2025, L2192, L2233, L2340 (rule rows counted = 15) | yes |
| 22 | Removed package: 10 files / 1,597 lines / 10 verbs; 116 tests in 10 files + 1 | L216, L2218-2231 (sum 1597 recomputed), L2239-2250 (10 verbs), L2319-2334 (sum 116 and 2,391 lines recomputed), L2076 | yes |
| 23 | Removal commit 01e7a9e23, PR #682, 2026-11-19 18:02 -0600 = 2026-11-20 00:02 UTC | L185, L332, L366, L2214, L2091 | yes |
| 24 | 19 `_assumed_shape` fixtures | L210, L672-673, L805, L1780, L1867, L2034, L2114, L2164 | yes |
| 25 | Watcher tests: 20 files, 19,801 lines, 867 tests | L210; Appendix A.1 rows summed: lines 19,801 and tests 867 (recomputed) | yes |
| 26 | Guard tests: 17 files, 24,388 lines, 921 plain (920 strict) | L214; L1301-1311 (14+3 files); A.2/A.3/A.4 rows summed 24,388 lines and 920 tests (recomputed); A.2 L2170 gives 162 strict / 163 plain | yes |
| 27 | Claim files: issue.md 117, SKILL.md 197, orca_worktree.py 1,906, origin_repo 195, clickup_claim 270, 15 templates, 3 workers x 35 lines | L211, L385, L391, L425-433, L1013-1020, L1121 | yes |
| 28 | Observations: 12 skipped live cases (OB-H1 items 1-9 + OB-H2 + OB-H3 + OB-CTX = 12) | L338, L644, L1297, L1309, L1981, L1952, L2123, L2178 | yes |
| 29 | 44 sample payloads for the guard run | L220, L1299, L1988, L2040 | yes |
| 30 | Status of IR-7: BUILT-OFF via `IR7_REFUSE = False` (OW:822, 1757-1758) | L336, L581, L643, L1001, L1296, L1950, L2089, L2122; qualifier "(enabled:false)" vs "not enabled:false" differs, see M-4 | yes (word), qualifier differs |
| 31 | Status of `orca_worktree.py pending` caller: NOT BUILT; verb BUILT-ON | L334, L343, L572, L1003, L1480, L1949, L2352 | yes |
| 32 | Typed approval regex accepts `/sc:implement` and `/task`, not `/sc:task` | L555, L1086, L1243, L1615, L1887, L1915, L1954, L2028 | yes |
| 33 | Appendix A row count 48 = 21 + 11 + 9 + 7; 44 named + 4 added | L2140-2207 (rows counted per sub-table), L2208 closing line | yes |
| 34 | PR 686 / rewrite-design out-of-scope sentence count | grep "686\|rewrite": one hit, L218 (other "686" hits are line numbers such as 685-686) | yes (exactly one) |
| 35 | Table of Contents vs headers | L138-179 against grep of all `#` headers: every ToC entry (1-16, 2.1-2.4, 3.1, 4.1-4.6, 5.1.1-5.1.9, 5.2-5.4, 8.1-8.5, 9.1-9.4, 10.1-10.4, 11.1-11.2, 12.1-12.3, 13.1-13.2, 14.1-14.3, 15.1-15.6, A.1-A.4, B.1-B.9, Document History) has a matching header and the anchors match | yes |
| 36 | Cross-reference IDs D-xx, KW-x, X-xx, U-x | all D-01..D-31, KW-1..KW-8, X-1..X-28 cited elsewhere resolve in 14.1.2 / 14.2.1 (D-08, D-18, D-20, D-22, D-23, D-25, KW-1, KW-6, KW-7, X-28 checked) | yes |
| 37 | Cross-reference IDs Q-xx | Q-02..Q-11, Q-14, Q-18..Q-24 resolve in 14.1.1 / 14.2.1 / 14.3 / 14.3.1; Q-12, Q-13, Q-17 (L1258, L1362) do not appear in Section 14 | NO, see F-1 |
| 38 | Section 5.1.1 pointer "marked in 5.1.9" | L718 vs L950 (5.1.8 Contradictions) and L968 (5.1.9 Extension points) | NO, see F-2 |
| 39 | "Full per-word raise sites are in Section 9 / Appendix" | L919 vs Section 9 (L1509-1572) and Appendices A/B (L2136-2357): no per-word raise-site content in either | NO, see F-3 |
| 40 | [CONTRADICTION: ...] markers | none present (grep "CONTRADICTION" = 0 hits; the document uses [CODE-CONTRADICTED] doc-vs-code tags, all of which have matching rows in 14.1.2 / 14.2.1) | yes |

## Findings

### BLOCKING

| ID | Severity | Location(s) | Issue | Evidence | Required fix |
|----|----------|-------------|-------|----------|--------------|
| F-1 | BLOCKING | L1258, L1362 (Section 5.3 orca-ide paragraph; Section 5.4 "Open items") | Cross-references that say "see Section 14" / "all listed in Section 14" cite question IDs that do not exist in Section 14. Q-17 (orca-ide) at L1258 and L1362; Q-12 (OB-H gate passed?), Q-13 (who runs `pending`), Q-17 and C-36 to C-38, C-64 at L1362. Section 14 holds Q-02 to Q-11, Q-14, Q-18 to Q-24 only (grep of `Q-[0-9]+` shows Q-12, Q-13 and Q-17 occur only at L1258 and L1362; no `C-` ID occurs outside L1362). The questions themselves exist under other IDs (U-4, U-6, D-18, D-21, D-25), so the reader cannot resolve the cited ID inside the document. L1362 states the items are "all listed in Section 14 and in the gap log", which is false for these IDs. | grep `\bQ-[0-9]+` over the document: lines 1243, 1258, 1284, 1362, 1852, 1869-1871, 1947, 1954, 1971, 1987-1988; Section 14 spans L1856-2000. | Either add the Q-12, Q-13, Q-17 labels (and the C-36..C-38, C-64 pointers) to the matching rows U-4, U-6, D-25 / 14.3.1, or rewrite L1258 and L1362 to cite the existing IDs (U-4, U-6, D-25, D-18) instead of Q-ids. |
| F-2 | BLOCKING | L718 (Section 5.1.1) vs L950 and L968 | Wrong cross-reference: "all [CODE-VERIFIED] against DES 6.2 except where marked in 5.1.9". Subsection 5.1.9 is "Extension points" (L968) and contains no marks or exceptions; the contradictions and exceptions are in 5.1.8 (L950). ToC L152 confirms 5.1.8 = contradictions, 5.1.9 = extension points. | Headers at L950 ("5.1.8 Contradictions found and open questions") and L968 ("5.1.9 Extension points"). | Change "5.1.9" to "5.1.8" at L718. |
| F-3 | BLOCKING | L919 (Section 5.1.6) | Dangling reference: "Full per-word raise sites are in Section 9 / Appendix." Section 9 is Configuration & Environment (L1509-1572) and Appendix A/B (L2136-2357) are test-pin and removed-code appendices; none holds a per-word table of raise sites. The only "raise site" text elsewhere is 13.1.1 L1752 (one example) and the Evidence column of 10.1 (partial lines). | grep `raise sites?|per-word` returns only L919 and L1752. | Point to the real location (Section 10.1 Evidence column plus 10.2) or delete the sentence, or add the per-word raise-site table. |
| F-4 | BLOCKING | L2029 (15.2 spot check 11) vs L395, L326, L1278-1280, L1491-1492, L2172 | A counted fact stated two ways. 15.2 row 11 says "The guard and identity hooks are registered once each". Everywhere else the guard is registered TWICE (UserPromptSubmit HJ:63-71 and PreToolUse HJ:115-124) and the identity hook once: L395 "launch-level guard twice, job identity once", L326, the registration table L1278-1280, the 8.4 table, and A.2 L2172 ("guard registered once per event"). The row's own expected-result column lists three entries (guard twice, identity once), so the row contradicts itself. | L2029 versus L395 and L1278-1280. | Reword L2029 to "the guard hook is registered twice (once per event) and the identity hook once". |

### MINOR (notes; do not affect the verdict)

| ID | Severity | Location(s) | Issue | Evidence | Suggested fix |
|----|----------|-------------|-------|----------|---------------|
| M-1 | MINOR | L207 vs L371, L689, L1707, L2156 | "8 modules" (Section 1) versus "nine modules" (tree comment, test-pin text). Both are true once the empty `__init__.py` is counted (Section 1 says "plus an empty `__init__.py`"; L2019 says "eight modules and an empty `__init__.py`"), but the two numbers sit unreconciled. | as cited | Say "eight modules plus an empty `__init__.py` (nine files; the test pins nine)" once at L371. |
| M-2 | MINOR | L513 vs L1004, L1951 | Default `--pipeline` pick: Section 4.2 says "(BUILT-ON as text only)", Section 5.2 and D-20 say "NOT BUILT as code (prose rule only)". Same fact (text exists, no code computes it) with two status words; "BUILT-ON" is defined at L319 as code that exists. | as cited | Use "NOT BUILT as code (prose rule only)" in 4.2. |
| M-3 | MINOR | L330 (row 7) vs L199, L1948, L2272-2289 | The "Issue pipeline duties" contract text is "NOT BUILT" in ledger row 7 but "REMOVED" in the Section 1 piece table row 5, D-17 and Appendix B.5; 15.6 maps row 7 to D-16 and D-17 together. Defensible (row 7 = current text, row 8 = removal) but unlabelled. | as cited | Add "(removal: row 8, D-17)" to row 7. |
| M-4 | MINOR | L336 vs L1950, L2089 | IR-7 status word qualifier: ledger row 12, 4.4 and 4.6 print "BUILT-OFF (enabled:false)"; D-19 prints "BUILT-OFF (`IR7_REFUSE = False`; not `enabled:false`)"; the glossary L2089 says the `(enabled:false)` word covers IR-7. L319 reconciles it for row 12 only. | as cited | Use one form everywhere. |
| M-5 | MINOR | L879 vs L1569, L1674 | L879 cites `cycle.py:33-47` for "the timeouts, DAY_CAP, 10 candidates and 60 min lease"; the lease (`LEASE`), `MAX_ATTEMPTS`, `BACKOFF` and `DAY_CAP_WINDOW` are in `record.py:434-443` (L1569, L1674; confirmed: cycle.py only reads `record.LEASE`). Also `cycle.py:33-47` here and in 9.4 versus `34-47` at L939. | grep LEASE in cycle.py shows only `record.LEASE` uses | Cite `cycle.py:34-47` and `record.py:434-443`. |
| M-6 | MINOR | L554, L1117, L1917 | The same discrepancy (`refs/claim.md:125` says the L2 hook is "the worktree's pre-push hook") is tagged [CODE-CONTRADICTED] in 4.3 but [STALE DOC] in 5.2 and X-23. | as cited | Use one tag. |
| M-7 | MINOR | L522, L1216, L1375, L1378, L1556 (O- labels); L1362 (C- labels) | Open-item labels `O-2`, `O-3`, `O-4`, `O-15` (Sections 4.2, 5.3, 6, 9.3) are never defined in the document and do not match the `Q-` labels for the same items in 14.3.1 (dangling-symlink status = O-3 in Section 6 but Q-08 in U-10; orphan tmp = O-4 vs Q-06; stuck entries = O-2 vs Q-02). | as cited | State once that `O-`, `Q-`, `C-` ids belong to the gap log (L2059) or map them. |
| M-8 | MINOR | L212 vs L2201, L1133-1142 | "Claim tests: 10 test files (the 8 named for the claim path plus ...)" counts `tests/cli/test_issue_body_templates.py`; A.4 says that file is "not a claim test" and the 5.2 pin table lists 9 claim-test files. The sentence is not false (the 8 are "named", not "verified as claim tests") but the count of 10 cannot be rebuilt from the document. | as cited | List the ten files or say 9 + 1. |
| M-9 | MINOR | L1167, L1290 (guard "G1") vs L467, L593-594, L787-788 (watcher G1, G2) | Identifier collision: "G1" and "G2" name the watcher's login and discovery `gh` calls (4.1, 4.5, 5.1.2) and also the guard design's "G1" (coordinator-started worker has no marker) and "G2 rule 1/2" (5.3, 2.3). Context disambiguates. | as cited | Prefix with "guard" or "watcher" on first use per section. |
| M-10 | MINOR | L319 | The intro lists "rows 1b, 7b and 9 to 18 as additional rows" but the ledger also has row 12b (L337). | as cited | Add 12b. |
| M-11 | MINOR | L483 vs L734, L737 | Step 12 `_commit` is cited as lines 1116-1144 in 4.1 and 1116-1126 in 5.1.1 (the health stamp at 1138-1139 sits in the wider range). Not a contradiction. | as cited | none needed. |
| M-12 | MINOR | L1780 | "the per-issue budget is 32 plus 3 reserved (37 per cycle)": 32+3 = 35; the 37 adds G1 and G2 (stated correctly at L208, L799). | as cited | Reword to "35 per-issue plus the two shared calls = 37". |
| M-13 | MINOR | L1962 | D-31 class value "RETIRED" is not one of the class values used in the other rows (DEFECT CANDIDATE, NOT BUILT, BUILT-OFF, REMOVED). | as cited | Use REMOVED. |

Accepted tier decision (not a finding): the line-budget overshoot of the document.

## Checks performed

Counts: 40 facts in the table above; 36 consistent, 4 inconsistent (rows 18, 37, 38, 39 = F-4, F-1, F-2, F-3). 4 BLOCKING findings, 13 MINOR notes.

Lens checklist coverage:
1. Identifiers, names and values in more than one place (40 facts, including every constant named in the lens: DAY_CAP, MAX_CANDIDATES, SKEW_WARN_S, deadlines, 35-call budget with 3 reserved, exit codes, 59 reason words, 6 states, 17 fields, 5 verbs, 12-element argv, line counts and test counts). Sums recomputed from per-file rows: watcher lines 4,795; watcher tests 19,801 lines / 867 tests; guard tests 24,388 lines / 920 strict; removed package 1,597 lines; removed tests 116 tests / 2,391 lines; contract rule rows 15; REASON_TABLE groups 59; LL words 18. All reconcile except the items in F-4.
2. Status words across Section 1, 2.3, 5, 14.2.1 and Appendix B: consistent in meaning for every piece; qualifier differences recorded as M-2, M-3, M-4, M-13.
3. Trigger table (4.4) against 2.3 and 5: consistent, including every "no trigger found in snapshot" row (scheduler, dispatcher / COORD-, `pending` caller, coordinator hand-off, SLO reducer).
4. Writes-to-GitHub table (4.5) against 5.2, 8.1 and Appendix B.4: every command (C1-C5, X1-X3, G1-G7, reads, removed-package reads) is identical in the compared places.
5. Cross-references: D-xx, KW-x, X-xx, "see Section 14", Appendix A/B and 15.2 section pointers resolve, except F-1 (Q-12, Q-13, Q-17), F-2 (5.1.9) and F-3 (Section 9 / Appendix).
6. Table of Contents against all headers: matches (fact 35).
7. Appendix A row count: 48 = 21 + 11 + 9 + 7 and 44 + 4 added; matches the closing line and Section 1's watcher-file count.
8. [CONTRADICTION: ...] markers: none exist; the 14.1.2 rows and the [CODE-CONTRADICTED] tags in Sections 4, 5, 8, 10 map one-to-one to 14.1.2 / 14.2.1 rows (5.1.8 rows 1-9 = KW-1, X-1, X-2, X-3, X-4, X-6, X-5, X-8, X-9).
9. PR 686 / rewrite-design sentence: exactly one (L218).

Tool engagement: Read: 12 (document in 9 chunks, task prompt lines, report re-read) | Grep: 8 (686/rewrite, CONTRADICTION, headers, Q-ids, O/C/raise-site ids, section pointers, LEASE in snapshot cycle.py, registration wording) | Glob: 2 (test_require_orca_worktree_agent*.py in snapshot; one earlier hook-block retry) | Bash: 0. No web research. No write outside this report.
Confidence: Verified 40 / 40 facts and 9 / 9 lens items | Unverifiable: 0 | Unchecked: 0. The document claims about source code behaviour were not re-verified (out of lens scope); only document-internal agreement was tested.

## Verdict: FAIL

Four BLOCKING findings (F-1 to F-4), all one-line fixes: two dangling or wrong cross-references (F-2, F-3), one set of question IDs cited as "in Section 14" that are not there (F-1), one counted fact stated two ways (F-4). Thirteen MINOR notes (M-1 to M-13) do not affect the verdict.

Status: Complete
