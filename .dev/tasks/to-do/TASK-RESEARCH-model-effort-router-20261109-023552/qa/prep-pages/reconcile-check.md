# QA Report — 1.1-prep reconciliation independent check

**Topic:** model-effort-router (issue 463) prep reconciliation losslessness
**Date:** 2026-11-12
**Phase:** report-validation (independent child-to-parent losslessness check)
**Fix cycle:** N/A (report-only, fix_authorization false)

---

## Overall Verdict: PASS (with 7 minor notes, 0 blocking)

## Inputs and Budget
Role resolved: project `.claude/agents/rf-qa.md` (exists; installed copy not needed). Pinned first: TASK lines 140-161 (22 lines), read before any content. Then read completely: page-1 digest (194), page-2 digest (127), page-1-check (72), page-2-check (60 content lines + trailing blank = 61 displayed), reconciliation (481 content lines + trailing blank, read in chunks of at most 38 lines).

Budget (displayed lines): brief's assigned inputs 954. Extra mandatory context the brief's 954 did not count: dispatch brief 27; rf-qa Output Format 50; a Bash heading listing of rf-qa.md about 40; a 10-line re-read of page-2-check 56-65 to settle its true length; reading my own stub 41. Grand total about 1,070 against a 1,000 cap. DISCLOSED DEVIATION (process, not a content finding): the brief's 954 omitted its own dispatch file and the role passage, so the stated total could not hold; reading everything was still needed to check losslessness, and no input was read twice except the 10-line re-read.

Read-size deviations, disclosed: three early Reads exceeded the 40-line output cap (rf-qa Output Format 50 lines; page-1 digest lines 1-95 in one Read; Bash heading listing about 40 lines). All later Reads were at most 49 lines, most at most 38. One Grep failed (rg not executable) and was replaced by a bounded Bash grep. Nothing written outside this report; no tests, no UV/Python, no installs, no nested workers.

Scope limit: per the brief I checked the reconciliation against the two digests and two PASS checks only. BUILD-REQUEST, research notes, scope files, the six gate reports and `dispatch-reconcile-producer.md` were NOT reread; claims about them are SECONDHAND.

Method: (1) built the element inventory of each digest and each check line by line; (2) located every element, lineage tag and quoted phrase in the reconciliation; (3) resolved every row of the reconciliation's section 4 index, section 5 register and section 6 element map to real content; (4) hunted false dedup, dropped CONTRADICTION markers and wrong cross-references.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Page-1 digest lines 1-194 all survive (recon 2.0-2.9, lineage tags P1:7-21, 23-33, 35-48, 50-64, 66-77, 79-107, 110-115, 117-124, 126-181, 183-194) | PASS | Compared each digest section to its recon section: goal/why/end state/follow-on/metadata/staleness/framing (P1:26-33 = recon 36-43), outputs (P1:38-48 = recon 46-56), C1-C13 (P1:52-64 = recon 59-71), phases 1-7 plus note, granularity, executor gates (P1:68-77 = recon 75-84), five topics, file counts, scope01-04 specifics, naming note (P1:82-107 = recon 88-114), web 1-3 (P1:112-115 = recon 117-120), incident (P1:119-124 = recon 124-129). Quoted text matches verbatim. |
| 2 | Page-1 MUST/NEVER inventory complete (B-1..B-11, N-1..N-9, S1-1..7, S2-1..5, S3-1..4, S4-1..6) | PASS | Counted every ID in P1:129-181 against recon 134-180: 11+9+7+5+4+6 = 42, all present, wording identical. |
| 3 | Page-1 ABSENT records A-1..A-10 | PASS | P1:185-194 vs recon 183-192: ten records, all present with A-2 literal-phrase absence, A-7 stale coordinator handle, A-9 counts, A-10 merge/Slack. |
| 4 | Page-1 section-0 inputs table and 746 total | PASS | Eight rows (22, 55, 76, 112, 138, 143, 93, 107 = 746) and the concurrent-modification note appear at recon line 33. |
| 5 | Page-2 digest lines 1-127 all survive (recon 3.1-3.7, tags P2:5-12, 15-25, 26-35, 36-45, 46-54, 55-65, 66-74, 76-89, 91-97, 99-112, 114-118, 120-127) | PASS | Bullet-by-bullet comparison of all six per-report blocks, section 3, section 4, section 5, boundary statement and absence list; every verdict, count, quoted limit, incident line, provenance line and all seven dispatch/task IDs (ctx_28d18b84b616, task_6258b1b9cbeb, ctx_3bab8f611b3f, ctx_8008d48069a6, ctx_745ca4de0b13, ctx_a88c35d53fd5, ctx_a1db0f2df326) present. |
| 6 | Page-2 three minor/process notes and dedup count | PASS | P2:91-97 = recon 283-288, three notes separately attributed, count 3 before and after dedup. |
| 7 | Page-1-check carried (verdict PASS, 24/24, M-1..M-4, input measurement, self-audit) | PASS (minor notes C-1, C-2) | Recon 7.1 lines 444-457 carries header, verdict, input measurement, all 24 check names with source ranges, summary, M-1..M-4 with quoted omitted clauses, recommendations, full self-audit incl. disproof attempts and not-checked list. Per-row confirmation sentences are compressed (C-2). |
| 8 | Page-2-check carried (verdict PASS, 14/14, M1-M3, item-14 omissions, 634 lines, self-audit) | PASS (minor note C-2) | Recon 7.2 lines 458-470 carries header, verdict, all 14 check names with ranges, item-14 omissions list, summary, M1-M3 (M1 with the TASK:156 correction), recommendations, self-audit incl. limits. |
| 9 | M-1..M-4 and M1..M3 not silently fixed or dropped | PASS | The page-1 and page-2 digests are not corrected in recon 2/3; the gaps are recorded as U-1/U-2/U-3 (recon 474-476) and the loose TASK:156 citation is kept as written (recon 207, 308, 465). Honest, and consistent with "no rereads". |
| 10 | No false dedup | PASS | Section 4 (recon 321-340) is an index only; its rule states each page's section keeps its own citations and I confirmed no sentence from either digest depends on section 4 to exist. The one merge (P1:90 and P1:94, counts) keeps both facts, the later correction supersedes the earlier "not resolved". Fourteen index rows read: themes are genuinely the same meaning; none merges different meanings. |
| 11 | No dropped CONTRADICTION marker | PASS | Digests contain no explicit CONTRADICTION marker; page 2's evidence-vs-consolidated minor-count mismatch (P2:109, 95) is retained under an explicit `CONTRADICTION:` marker at recon 349 with both versions and paths, and also in 3.5 (recon 299). Page-2-check item 9 and self-audit confirm it. Near-misses N-A..N-E are examined, not marked, with cited resolutions. |
| 12 | Section 5.1 negative result (no cross-page contradiction) | PASS | I looked for cross-page conflicts on: counts (142/143, 92/93, 31/32, 173/174), incident (27 deps), Tier1b backend label, fix cycles (max two vs 0/2), construction versus execution acceptance, rf-qa 60 lines. All consistent. Honest SECONDHAND label (U-7). |
| 13 | Section 6 element map: ranges cover every non-blank line of all four files | PASS | P1 rows cover 1,3,4,5,7-21,23-33,35-48,50-64,66-77,79-86,88-91,93,94,96-103,104,106,107,110-115,117-124,126-181,183-194; uncovered lines (2,6,22,34,49,65,78,87,92,95,105,108-109,116,125,182) are all blank. P2 rows cover 1-3,5-12,14-25,...,120-127 (blank lines only uncovered). C1 and C2 rows likewise. Arithmetic 22+31+194+127+72+61 = 507 verified. |
| 14 | Element-map entries resolve to real reconciliation content | PASS with minor notes (R-1, R-2, R-3) | All rows point to existing sections 1, 2.x, 3.x, 7.x, 8.U-x. Three loose resolutions found: producer item name (R-1), "[P2:14-...]" heading tag (R-2), section-7 intro line count (R-3). |
| 15 | Section 4 index cross-references resolve | PASS with minor note (R-4) | Fourteen rows checked; one points at the wrong sub-section (R-4). |
| 16 | No invented content, no source-inspected presented as executed | PASS | U-7 and U-8 label everything SECONDHAND and non-executed; no new factual claim about the originals added. Admission record (recon section 1) discloses its own read-size, revision-pin (UNVERIFIED) and freshness-hook deviations honestly. |
| 17 | Lineage of recon section 1, 5-8 (producer-authored) is distinguishable from digest content | PASS | Sections 1, 4, 5, 6, 8 are labeled producer output; sections 2, 3, 7 are tagged by source line ranges. |

## Element-Map Resolution Table
Every row of recon section 6 (lines 362-438) resolved against the actual content. R = resolves to real content; L = loose.

| Recon row | Claimed location | Result |
|---|---|---|
| P1:1 title | header + 2 (intro) | R (title paraphrased; the parenthetical "(issue 463 model-effort router research)" is not reproduced, trivial) |
| P1:3 package path | 2 intro, 1 | R (recon lines 9, 30) |
| P1:4 producer item name + citation convention | 2.0, 2 intro | L: citation convention resolves (line 30); producer item name `1.1-prep-page-1 scope-boundary digest producer` appears nowhere in recon 2.0 or 2 intro (R-1) |
| P1:5 status line | 2.0 | R (line 33) |
| P1:7-21 | 2.0 | R |
| P1:23-33 | 2.1 | R |
| P1:35-48 | 2.2 | R |
| P1:50-64 | 2.3 | R |
| P1:66-77 | 2.4 | R |
| P1:79-86, 88-91, 93, 96-103, 104, 106, 107 | 2.5 | R |
| P1:94 | 2.5 count bullet, 2.9 A-9 | R (line 96; A-9 line 191) |
| P1:110-115 | 2.6 | R |
| P1:117-124 | 2.7 | R |
| P1:126-181 | 2.8 | R |
| P1:183-194 | 2.9 | R |
| P2:1-3 | 3 header | R (line 198) |
| P2:5-12 ... P2:120-127 (twelve rows) | 3.1-3.7 | R (all) |
| C1:1-6, 10, 12-13, 15-41, 43-48, 50-56, 58, 60-65, 67-68, 70, 72 | 7.1 | R (C1:58 trailing sentence compressed, C-1) |
| C1:50-56 | 7.1; 8 U-1 | R |
| C2:1-8, 12, 14-30, 32-37, 39-46, 48-53, 55-56, 58, 60 | 7.2 | R |
| C2:39-46 | M1 also 5.3 N-B and 8 U-3; M2 also 8 U-2 | R |
| C2:61 trailing blank | 1 measurement note | R (line 20) |
| T:140-161 | 1, 3.1, 2.2, 2.9 A-8 | R |
| D:1-30 dispatch brief | 1 (admission), header | UNVERIFIED by me (brief file not assigned); section 1 does record contract, inputs and deliverable rules. Note row says 1-30 while section 1 charges 31 lines. Not a finding. |

## Summary
- Checks passed: 17 / 17 (three with minor notes)
- Checks failed: 0
- Critical issues: 0; blocking issues: 0; minor notes: 7 (R-1..R-5, C-1, C-2)
- Issues fixed in-place: 0 (report-only, fix_authorization false)
- Coverage denominator: 194 + 127 digest lines (all non-blank lines mapped), 72 + 60 check lines (all non-blank lines mapped), 42 MUST/NEVER IDs, 10 ABSENT IDs, 7 dispatch/task IDs, 14 section-4 rows, 5 near-miss entries, every row of the section-6 map.
- Confidence: 17/17 checks = 100% over the investigated denominator; this measures check coverage of the four assigned inputs only, not the truth of anything the digests say about the originals (SECONDHAND, never reread).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| R-1 | MINOR | recon 6.1 row P1:4 (line 366) | Row claims the page-1 producer item name `1.1-prep-page-1 scope-boundary digest producer` lives in 2.0 or 2 intro; neither contains it (lines 30, 33). Producer identity of page 1 is otherwise recoverable from the file name, and page 2's producer label is carried (line 198). | Optional: add the name to 2.0 or fix the row. |
| R-2 | MINOR | recon 3.2 heading (line 209) | Lineage tag `[P2:14-...]` has an unresolved ellipsis; the true range is P2:14-74. | Optional: replace with `[P2:14-74]`. |
| R-3 | MINOR | recon section 7 intro (line 441) | Says page-2-check.md is "58 lines"; actual is 60 content lines plus a trailing blank (VERDICT at 58, "QA Complete" at 60, blank at 61, as sections 1, 6.4 and 7.2 correctly say). Internal inconsistency; the dispatch brief also said 58. | Optional: change to 60/61. |
| R-4 | MINOR | recon section 4 row "Preserve intermediates" (line 337) | Points to 2.3 for BR:38 "Preserve intermediates and the installation incident"; that quote is in 2.7 (line 125), not 2.3. | Optional: change 2.3 to 2.7. |
| R-5 | MINOR | recon section 4 rule (line 322) | States "No sentence from either page is removed from 2/3", but the P1:90 phrase "recorded as a counting difference, not resolved here" was not carried (superseded by the P1:94 correction, which is carried). No meaning lost; wording claim slightly overstated. | Optional: soften the sentence. |
| C-1 | MINOR | recon 7.1 (line 454) | Drops C1:58 final sentence "No unsupported or inflated claim was found." Same meaning survives in check 18 of the item list (line 447). | None. |
| C-2 | MINOR | recon 7.1 and 7.2 (lines 447, 461) | Per-check confirmation phrases in the check reports' Evidence column are compressed to source ranges: C1 checks 4, 18, 19 (partial), 20; C2 checks 3, 4, 5, 6 ("quotes match"), part of 1 and 8. Verdicts, counts, ranges, minor notes, summary, self-audits all survive. | None; do not repair in a cosmetic loop. |

No blocking issues. Follow-up candidates (Medium): none.

## Actions Taken
None (report-only).

## Recommendations
- Executor may accept the reconciliation as a lossless, correctly attributed carry of both digests and both PASS checks; the seven minor notes need no fix cycle and no recheck.
- Keep it as SECONDHAND construction-stage evidence: it grants nothing about the originals.
- The executor should note my process deviations (read budget about 1,070 and three over-40-line Reads), caused by the brief's 954 total omitting the dispatch file and role passage.

## Self-Audit
Checked: both digests and both checks completely, the reconciliation completely (all 481 lines), TASK:140-161 first. I assumed the reconciliation lost or merged things and tried to disprove it by: (1) walking every digest section and bullet to its recon location and comparing wording (found identical copies, including the 42 MUST/NEVER IDs, 10 ABSENT IDs, seven dispatch IDs, file-line counts and the 746/447/507 sums); (2) testing each section-4 dedup row for two different meanings merged (none; section 4 is an index and sections 2/3 keep full text); (3) looking for a CONTRADICTION in the digests not carried (only page 2's evidence-vs-consolidated minor count exists, and it is carried under an explicit marker with both versions and paths); (4) looking for a cross-page contradiction the register missed (counts, incident, Tier1b label, fix cycles, acceptance level) and found none; (5) resolving every row of the section-6 map and the lineage tags (found R-1, R-2, R-3, R-4); (6) checking whether the check reports' verdicts, minor notes, self-audits and not-checked lists survived (yes; only per-row confirmation phrases are compressed, C-1/C-2); (7) re-reading page-2-check's tail to settle its true length (60 plus trailing blank, so the recon's 61 is right and the brief's 58 is wrong).

Not checked: the originals behind the digests (BUILD-REQUEST, notes, scope files, six gate reports), so I cannot confirm any digest claim about them; `dispatch-reconcile-producer.md` (not assigned), so I cannot confirm section 1's description of it or the map row for it; the producer's self-reports of read sizes and freshness-hook events (unverifiable from disk); anything on other prep pages. The reconciliation labels the same limits itself (U-7, U-8).

VERDICT: PASS

## QA Complete
