# QA Report: Anti-Omission Recoveries, Content Verification (report-qualitative)

**Topic:** Unified Review Panel research report, Gate 5 (anti-omission) recoveries
**Date:** 2026-11-14
**Phase:** report-qualitative (ROLE = content), cycle 1
**Fix cycle:** 1 (no fix authorization; report only)
**Report under review:** `RESEARCH-REPORT-review-panel-unification.md` (new 6.E, rows V-692 to V-698 in 8.1, in-place corrections S1 to S3, Section 10 pointer)

## Overall Verdict: PASS

No CRITICAL or IMPORTANT defect found. Six MINOR notes are listed below; none changes a decision, a residual risk or an open item in substance.

## What was checked and how

All 529 consolidated rows are RECOVER rows and the fix log shows 529 rows, all `Fixed`, none JUSTIFIED (grep of the fix log: 529 `| F5-` rows, 0 with another status, 0 "justified"). Check (b) of the embedded prompt (JUSTIFIED rows) therefore has nothing to test this cycle.

Rows compared against their source file and line (`reviews/adversarial/<slug>/` and `research/`):

| Table | Rows in 6.E | Rows compared to source | Method |
|---|---|---|---|
| 6.E.1 C-13 ledger model | 46 | 46 (C13-01 to C13-46) | the cited PM, IP, DT, DA, ML, RP, FF, VA, VB, R1A, R2A, R2B, BS, SP2 lines read and compared claim by claim; numbers, ids, line cites, status words |
| 6.E.2 C-14 panel size | 32 | 32 | PM, IP, DT, DA, ML, RP, VA, VB lines read; C14-04, 09, 11, 14, 18, 21, 24, 25, 28, 29, 30, 32 compared to their main source line |
| 6.E.3 C-05 who judges blocking | 43 | 15 in depth (C05-01, 02, 03, 05, 07, 11, 13, 15, 16, 24, 25, 26, 27, 36, 38; C05-25 is the S3 row) | PM, IP, DA, ML, RP, VA, VB lines read |
| 6.E.4 C-03 model tier | 34 | 16 in depth (C03-01, 02, 03, 06, 10, 16, 17, 19, 20, 21, 22, 24, 30, 31, 32, 34) | PM, IP, DT, DA, ML, RP lines read |
| 8.1 research recoveries | 7 | 7 (V-692 to V-698) | R09, R10, R11, R13 lines read |

Total rows individually compared: 46 + 32 + 15 + 16 + 7 = 116 of 162 (155 group rows plus 7 research rows); the requested floor was 60. Every kind of row was covered: decision (C13-10, 12, 13, 19, 27, 38, 42; C14-02, 14, 22, 23, 26, 27, 30, 31; C05-01, 02, 05, 13, 24, 25; C03-20, 21, 22, 24, 30), residual risk (C13-01, 05, 11, 15, 16, 17, 20, 41; C14-01, 06, 07, 08, 12, 21, 25, 29; C05-03, 11, 15, 36; C03-01, 10, 16, 34), open item (C13-21, 33 to 37, 44, 45; C14-15, 18, 19, 28; C05-07, 16, 38; C03-32), invariant closure (C13-03, 04, 06 to 09, 22 to 24, 26, 29, 30; C14-32), test pin (C13-14, 40; C14-17), script (C14-16; C03-17), coupled edit site (C13-25, 39; C14-03, 04), rule (C13-02, 18, 28, 31, 32, 43, 46; C14-10, 20; C05-26, 27; C03-19).

Not read line by line (46 rows, stated as unchecked, not as passed): 6.E.3 C05-04, 06, 08, 09, 10, 12, 14, 17 to 23, 28 to 35, 37, 39 to 43 (28 rows) and 6.E.4 C03-04, 05, 07, 08, 09, 11 to 15, 18, 23, 25 to 29, 33 (18 rows). The 31 rows of those two tables that were read showed no defect.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 6.E.1 (C-13) rows faithful to source: detail is what the debate says; no decision reworded; residual risks and open items still open; nothing added | PASS (3 MINOR notes) | All 46 rows compared. Examples: C13-01 against PM:364, RP:17,183, ML:182-183 (18 UNADDRESSED = 10 HIGH + 7 MEDIUM + 1 LOW, footer says 16, entries show 18: matches); C13-07 decision table against PM:66-74 and RP:277-286 (four rows identical); C13-10 against PM:57-59 and RR:72 (risk HIGH, `regrade_of` and `reattack_of`); C13-24 against PM:76 (the `[NOT APPLIED: ...]` marker is kept); C13-33 to C13-37 against DA:92-95, DA:43, DA:55, PM:595-601 (percentages 65, 55, 55 and the "NEITHER" outcomes match and stay open); C13-45 against ML:374,404 (provenance limit stays open). Notes M1, M2, M3 below. |
| 2 | 6.E.2 (C-14) rows faithful | PASS | All 32 rows compared. Examples: C14-01 against PM:55,188,240,507, IP:13 (shadow at requested 2 aborts at `manifest.py:314-315`, `:316` was blank, D2 is `:318`); C14-03 against PM:252-272 and ML:72 (13 EDIT rows, 16 sites, the "about nine edits in five files" discrepancy flagged and kept); C14-10 against IP:20, RP:190, ML:88,158-162 (withdrawn counts 13 of 23 / 0 of 6 and 14 of 26 / 2 of 9 appear only as withdrawn, corrected 20 of 23 and 5 of 6); C14-23 against DA:136,140 (decisive in 0 for certain, at most 1 of 39; 29 of 34 outside the flag's influence); C14-26 and C14-27 against DT:193,204,205,210 and DT:185,204 (22 degraded / 3 full / 1 untagged; nine two-card runs by cause 2/1/1/5); C14-30 against DT:263 (B won X-002); C14-31 against RP:133 (engine default stays 3). |
| 3 | 6.E.3 (C-05) rows faithful (15 compared, 28 not) | PASS | C05-01 against PM:28,183,501,551 and ML:59-62 (demotion rule agreed at HYBRID 78 percent; tri-state reply stays "Advocate B's proposal, not an agreed contract"); C05-05 against PM:203,673 ("D1 fixed" stays undefined, the two readings cancel); C05-13 against PM:210-219,547 (replay gate, low power, inconclusive keeps veto live); C05-24 against PM:396,465,528,674 (D1 pushes counted wrong blockers down; attribution unmeasured, OPEN 69-71 percent); C05-27 against VA:66,129,157, VB:143-144 (65 vs 38, 2.75-3.25, 0.17 / 1.83 / 0.83 figures); C05-36 against IP:126-131 (80 drops, luna 30, ember 33). |
| 4 | 6.E.4 (C-03) rows faithful (16 compared, 18 not) | PASS | C03-21 against PM:158,191, DT:32-33,87,204,406,573, DA:12,89, ML:177, RP:140-141 (A-004 REJECT as stated at 85 percent; `T4Model04=muse-ember-1.0` set live, absent from packaged data, serving unknown); C03-20 against PM:146,207, VA:75 (EV-10); C03-22 against PM:187,205,223 (A-002 QUALIFY 77 percent, parent equals SONNET binding, haiku and opus UNVERIFIED); C03-31 and C03-32 against DA:24,52,75,100 and ML:194 (S-007 and X-003 stay unresolved); C03-34 against DT:626-631 and IP:24-42 (14 findings, 4 ADDRESSED, 10 UNADDRESSED, 2 HIGH, 7 MEDIUM, 1 LOW). |
| 5 | Merged AO3 ids: merge is tight (one source location), no distinct item lost | PASS | Each merged row was read against the ids it carries. The multi-id rows (C13-14 with 9 ids, C13-27 with 6, C13-40 with 7, C05-25 with 10, C03-22 with 8) group items of one decision or one test list, all in one PM region plus the same item in DT, DA, ML or RP. Spot lookups in AO3: L1-022, L5-010, L4-162 (all "probe totals", all in C13-01); L1-183, L6-087, L6-138 (all INV-005 closure and clearing gate, all in C13-03); L3-096 (C13-18); L4-235 (C13-45). One id pairing is imprecise: see M1. |
| 6 | The 7 research-file recoveries against sources | PASS | V-692 against R09:210-212; V-693 against R10:60,72; V-694 against R10:121-126,133; V-695 against R11:151 and CR:426,428; V-696 against R13:50,75,112,116; V-697 against R13:212,264; V-698 against R13:269,276. Wording, numbers and line cites match. Destinations are the matching module rows of 8.1 (Spec review module, Severity scale and per-consumer mapping, rf-qa replacement module, Panel resolution, Reflect UC-2 module x3), placed after V-691. Only inference: V-696 "came in with PR #220" reads R13:75, which lists #213, #214, #220 and #329 for `ensemble.py`; the title "Tier-2 fallback ladder" is attached to #220 in that line, so the attribution is supported but not stated as a claim about the ladder alone (not a defect). "Not named as a caller-facing capability elsewhere": grep of the report for `tier2_fallback`, `t2_fallback` and `run_fallback_ladder` finds only V-696. |
| 7 | Priority correction S1 (`muse-ember-1.0`) | PASS | V-102 (report line 3224) and V-407 (line 3529) now say: set live as `T4Model04=muse-ember-1.0`, absent from packaged data, "absent from the environment" is false, whether it serves is unknown. Debate evidence: PM:158 (EV-14) and PM:191 (A-004 REJECT as stated, agreed 85 percent), DT:32,87,204,406,573, DA:89 (CONTRADICTED partially), ML:177, RP:140-141. Same words, same hedge on serving. |
| 8 | Priority correction S2 (E2's best panel expressible) | PASS | C-03 Option A cons (report line 1339) now says E2's best real-blocking panel `haiku + 2x luna` has the shape of combination E and is expressible by class binding (EV-10) and that `muse-ember-1.0` as a class value is untested (EV-9). PM:146 and PM:207 say the same, with the same tags (DOC-SOURCED for panel quality, OBSERVED-RUNTIME for reachability). See M4 for one remaining older sentence in Section 4. |
| 9 | Priority correction S3 (veto and panel size) | PASS | C-05 Option A cons (line 1469) now says E2 neither supports nor refutes a panel-size effect, the false-block rate is per candidate, control wrong blockers by panel size flat at 1.00, 1.27, 1.05, 1.33, 0.89, advocate-computed and not re-aggregated. Source: PM:466 and PM:672 (EC2, OPEN 73 percent), RP:104, DT:394 (the 1.27 row), ML:107. The figures match; the "advocate-computed" caveat is kept. |
| 10 | 6.E does not contradict Section 6 C-03, C-05, C-13, C-14 | PASS | Winners (A, B, B, B), `partial` status, convergence figures, HIGH-invariant counts (2, 11, 10, 3) and unresolved diff points in the Section 6 "Adversarial result" paragraphs match the 6.E rows (C13-01, C14-19, C05-38, C03-34, C03-31 and C03-32). C-13 recommended resolution (Option B through a staged hybrid with a gate) matches C13-38 (Stage 2 decision gate, "the plan does not assert which side wins"; option (i) "not adopted as the target"). C14-02 and the C-14 Step B (D-1 owner-gated, cap 3) match. C13-02 and C13-03 add "closed-in-port" design statuses; C13-02 states that the probe status stays UNADDRESSED and that no row is `closed` until its acceptance test passes, which agrees with the Section 6 and Section 7 statement that the HIGH invariants are unaddressed. |
| 11 | 6.E does not contradict Sections 7 and 8 | PASS (2 MINOR notes) | Section 7 open-risk table, Q-47 to Q-57 of 9.5, and the Section 8 binding facts agree with the 6.E counts and ids. The two soft differences (M5, M6) are wording differences that leave the Section 7 statement true. |
| 12 | Report-only scope; four debates still `partial`; winners unchanged; Section 7 core-verdict `[CONTRADICTION]` still raised | PASS | 6.E contains no roadmap, no `/sc:workflow`, no ordering commitment (grep of lines 2624-2807 finds only task-builder file names inside coupled-edit rows). The intro states "the four debates stay `partial` and no winner changes". `[CONTRADICTION` still appears in Section 7 (line 2961, bold flag in the Merge and verdict row), Section 8 (line 3095), V-433 and Q-54 (line 4379). 6.E.1 C13-12 and C13-31 carry OD-8 and the exit-12 PENDING question as open, not as decided. |
| 13 | Sample of at least 60 rows, every kind | PASS | 116 rows compared (see table above), 46 not read; kinds listed above. |

## Issues Found

All MINOR (notes; they do not fail the review and are not rechecked).

| # | Severity | Location | Issue | Suggested fix |
|---|----------|----------|-------|---------------|
| M1 | MINOR | 6.E.1 C13-03, "test: round 2 `unverified` FAIL, then round 3 ... reaches PASS (T-P5, T-P17)" | T-P17 is the INV-017 acceptance test (PM:393, PM:514; C13-30 carries it); the INV-005 test is T-P5 only (PM:381, PM:506). A reader could believe T-P17 covers the `unverified` path. C13-40 gives the correct pairing. | Delete ", T-P17" from C13-03. |
| M2 | MINOR | 6.E.1 C13-14, "result binding on whether the port stays the default" | The merged proposal asks the owner to "authorise the falsifier run ... and treat its result as binding on the gate" and lists it as OD-6, status Open (PM:581, PM:619). The row states the binding as if settled. Q-52 and C13-38 elsewhere keep the gate open. | Write "(owner decision OD-6, open)" after "binding". |
| M3 | MINOR | 6.E.1 C13-18, cites `VB:11,141,274` | The "256-line design document" figure is at VB:275 (`design doc 256 lines; command 475 lines`), not at the cited lines. | Add `275` to the source cell. |
| M4 | MINOR | Section 4 row MS-06 (report line 633) | Still says "E2's best panels (ember + 2x luna; `muse-ember-1.0` is in no alias or class) cannot be expressed". It is the origin of the sentence that S2 corrected in C-03. For `haiku + 2x luna` the debate shows it is expressible (EV-10); for ember it is untested (EV-9, EV-14), so "cannot" is an overstatement. AO3 listed only line 1338, so this was outside the recovery list. | Reword to "cannot be expressed from packaged data; class binding of a raw id works for `luna` and `haiku` (EV-9, 6.E.4) and is untested for `muse-ember-1.0`". |
| M5 | MINOR | Section 7 Merge and verdict row, `[CONTRADICTION]` text: "the C-13 merge ... no new exit code (OD-8)" against 6.E.1 C13-13 and C13-31 | The C-13 merge also uses exit 12 PENDING for sweep lenses (PM:110, "C19 Option A, decided"; PM:163,217). The Section 7 text is true for W and for an unattended non-PASS but a reader of 6.E may take it as a conflict. The flag stays open either way, and 6.E makes it stronger, not weaker. | Add "except exit 12 PENDING for lenses that require a sweep" to the parenthesis. |
| M6 | MINOR | Section 7 table row C-13 "What the architecture assumes meanwhile" and Q-52: "Stage 0 fixes only (cap by refusal, `--cap` conflict error, quorum of valid blocks, atomic refusal)" against 6.E.1 C13-38 | C13-38 lists a wider Stage 0 (also `revised` bookkeeping with four refusals, `defer` through the shared decision function and the shared exit-code table, `min_writer`). Summary versus detail; the difference is not noted. | Add "(full list in 6.E.1 C13-38)" to the Section 7 cell. |

No CRITICAL or IMPORTANT issue. No recovered row was found to reword a decision into a different conclusion, to close an open item, or to add a statement the debate files do not make. Where a row carries an `[UNVERIFIED]`, `[NOT APPLIED]`, `[PROPOSED]` or `[DOC-SOURCED]` tag in its source, the tag is kept (C13-24, C14-16, C14-15, C03-16).

## Actions Taken

None (report only; no file edited except this report).

## Self-Audit

**(a) Reliance list.** The spawn prompt carried no `## Inherited Structural Verdict` section, so no rf-qa PASS was relied on and no structural re-check was skipped. The structural role (tables, totals, Table of Contents, citations) belongs to the parallel rf-qa agent and was not repeated here beyond what the content checks needed (row counts per sub-table: 46, 32, 43, 34 = 155).

**(b) Independent semantic checks.**
- Debate-source comparison of 116 rows (listed above) by Read/sed of the cited `reviews/adversarial/<slug>/` lines, including every numeric claim in the C-14 recount rows (C14-10, 23, 26, 27) and in the E2 figures of C05-25 and C05-27.
- The three priority corrections S1, S2, S3 checked in the report text (lines 3224, 3529, 1339, 1469) against EV-14, A-004, EV-10, EC2.
- Cross-check of Section 6 adversarial results, Section 7 open-risk table, Section 8 binding facts and Q-47 to Q-57 against 6.E counts.
- Grep for the surviving older wording ("cannot be expressed", "absent from the environment", "adds blockers with each added reviewer"), which found the MS-06 residue (M4).
- Grep of the report for `[CONTRADICTION`, roadmap and `/sc:workflow` in 6.E.

## Confidence

Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% for the 13 check items. Row coverage is partial by design: 116 of 162 rows compared individually, 46 unchecked (named above); those 46 are not claimed as passed.

**Tool engagement:** Read: 9 | Grep: 8 | Glob: 0 | Bash: 45 (read-only sed, grep, ls, wc against debate and research sources; no mutation)

## Recommendations

- None blocking. The six MINOR notes are optional wording fixes; if the report is touched again, apply M1, M2 and M4 first (they are the only ones a reader could act on).

## QA Complete

