# QA Report: Gate 3 fix verification (content, cycle 1)

Status: Complete (final line of this file; verdict PASS, F_1 = 0)

**Topic:** review-panel-unification-run2 research report, Gate 3 fix cycle 1
**Date:** 2026-11-15
**Phase:** fix-cycle (report-qualitative, content verification)
**Fix cycle:** 1
**Grading:** `qa/grading-override.md` applied
**Mode:** fix_authorization false; only this file is written
**Inputs read:** grading-override.md, qa-consolidated-findings-phase6.md, qa-fix-log.md, the report (5,098 lines, confirmed by `wc -l`)
**Inherited Structural Verdict:** none in the spawn prompt, so this review ran standalone (no rf-qa PASS relied on).
**Scope of blocking set:** the consolidated file has two blocking rows (P6-001, P6-002; Grep for `| Y |` rows returns exactly those two). Everything else is minor under the override and was not rechecked.

## 1. Finding ID | FIXED or STILL-OPEN | reason

| Finding ID | FIXED or STILL-OPEN | reason |
|---|---|---|
| P6-001 (Sections 3 and 4 targets against the adjudicated Section 7: no statement of which governs) | FIXED | Three precedence statements now exist: report line 120 (Baseline and Conventions), line 1125 (head of Section 3, "Section 7 governs") and line 3584 (7.0.1 "Precedence"), plus the Section 4 preamble (line 1232) naming G-01, G-02, G-03, G-04, G-14, G-17, G-20, G-99, G-136. The delta table (lines 1127-1144, 16 rows, 5 pipes on every line) covers every item the finding asked for: T-1, T-2, T-3, the Finding contract, Dispatch, Merge and Ledger rows of 3.2, SC-01, SC-02, SC-05, SC-11, and the target cells of G-01, G-02, G-14, G-20, G-99, G-136 (plus T-4/DO4, 3.5, G-03, G-04, G-17, Run record, SC-29, 4.2). I checked every right-hand cell against the Section 7 text it cites and each matches in substance: T-2 against 7.0 axis 8 and A-8 ("OVERTURNS", "no engine moves now", write-side helpers, Q-09); T-3 and the 7.1 introduction (thin contract list includes brief hooks and evaluation hooks); Finding contract against 7.0 axis 2, A-15, A-16, 7.1 element 1, I-3 (the `calibrated_confidence` reason is stated in I-3 itself) and the register family row "DR-113 avoided by engine separation"; Merge against element 2; G-14 against axis 4 and A-3, A-9 (no expiry, `refound_deferred`, `min(2, requested)`); Dispatch against axis 5, A-6, A-7, element 6 (soft distinctness default, "a repeat is recorded" reading of SC-11; the G-136 target cell does contain the alternative "a recorded, visible degrade"); G-99 against C-01, element 6 ("per-slot `lens` key (withdrawn in C-11)"), A-14; SC-29 against A-11; 4.2 against 7.1 Reflect row, C-04, C-08, X-14. All five conflicts (i) to (v) named in the finding plus the 4.2 conflict now have a row. The table adds no number, decision or tag (Grep for `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]` in the added passages: none) and no plan words (sprint, milestone, estimate, weeks: 0). It states its own limit ("not a second review of every row"). Still report-only. |
| P6-002 (value-inventory destinations send the blind grader and E3i scripts to CORE against 7.0 axes 4 and 10, A-4) | FIXED | New note and table at report lines 4300-4314 (end of 8.1.2), plus a prefix on 8.1.4 limit 1 (line 4399) and the Baseline sentence (line 120). All ten Appendix A lines cited in the table are correct: I printed lines 820, 822, 852, 853, 867, 921, 845, 860, 526, 982 of `synthesis/synth-08-value-inventory.md` and each has the quoted ID, kind (artifact, artifact, strategy, script, finding, strategy, script, script, defect, defect) and destination CORE; VL-24-525's Reason says "Slice proposes an optional MODULE stage; classified CORE here because the verdict contract needs it", as quoted. The adjudicated readings match Section 7: no grader and no category predicate in the core (axis 4, A-4 "the grader stays an optional module"), "port contracts, not scripts" with grader and ledger sweep as "optional modules or evaluation instruments" (axis 10), F-4, elements 4 and 5. The report states that Section 7 governs, that Appendix A rows and the 8.1.0 counts and 8.1.2 line ranges are unchanged (confirmed: the file is still 6,127 lines and 2,024,775 bytes, the same figures the report prints), that axis 10 does not choose between module and instrument, and that the DROP reading for the two script rows is a reading, not a decision. The 48-row scan claim reproduces exactly (`sed -n 45,996p | grep -ciE <the seven terms>` = 48). The claims about VL-24-524 and VL-24-526 ("ideas, not the script") and VL-24-213 and VL-24-215 (contract as Reason) are true against the file. The 8.1.2 table has 6 pipes on all 11 lines. The report no longer leaves 8.1 contradicting 7.0 without a stated precedence, which was the defect. |

## 2. New blocking issue | location | reason

| New blocking issue | location | reason |
|---|---|---|
| None | not applicable | I looked for a new blocking defect in each added passage under the three override tests. (1) Decision, recommendation, inventory destination, conflict outcome or number: every right-hand cell of the delta table and the 8.1.2 table restates a Section 7 outcome that I found in the cited Section 7 text, no new number or decision appears, and the two tables defer to Section 7 where they differ. (2) Required section or deliverable: Sections 1 to 10 and Appendices A and B are all present (headings at lines 124, 139, 1112, 1229, 1538, 2138, 3567, 4234, 4689, 4847, 5072, 5076); no heading was added or renamed. (3) Security, data-loss or safety: none touched, the fix only adds report text. Candidate defects I considered and graded minor are in section 3 below. |

## 3. New minor notes (all minor under grading override; never rechecked)

1. (minor under grading override) Not every Section 3 success criterion that Section 7 overtakes is named in the delta table. SC-27 ("the `/task` phase gate run through the core") conflicts with 7.1 rf-qa row and C-11 ("no panel engine in any rf-qa gate" in the first change). SC-09 (`identity_source: observed` on every run) sits against the C-08 gate on measurement M1 and CT-4. SC-18 (executor-class exclusion on the reflect Tier-2 path) and SC-23 (merged-verdict written at the legacy layout) sit against C-04 (grounded lane and promotion deferred). The general rule in the precedence paragraph covers them and the table states it is not exhaustive, so the original defect (no governing statement) is closed. Downstream use: Sections 6 to 9 do not read these cells.
2. (minor under grading override) The first sentence of 3.5 ("the target above holds under every option of the decisions below; they change its detail, not its shape") was not edited and no longer fits T-2 (withdrawn) and the narrowed T-1 and T-3. The 3.5 row of the delta table says all of the listed decisions were adjudicated, which corrects it.
3. (minor under grading override) The body sentence of 4.2 ("None is downgraded to future phase") is unchanged; the delta table row narrows it. Same mechanism as note 2.
4. (minor under grading override) 8.1.1 and 8.1.4 limit 3a still place the exchange layer (seal, hook, resume, board, transport) in CORE "as an optional capability", while 7.0 axis 6 says "no hook transport in the core" and "nothing of it is built now". Limit 3a already says this is a placement, not a quality claim, and the Baseline sentence makes Section 7 govern any inventory destination that differs, so I did not grade it blocking. The new 8.1.2 table does not list these rows (the keyword scan covered grader and variant scripts only).
5. (minor under grading override) The `DROP` destination offered for `review_ledger.py` and `diffgate.py` in the 8.1.2 table is worded "the closest of the ten destinations"; the report marks it as a reading. DROP in this inventory also means duplicate or obsolete, which the "contract ported, script not carried" label only partly fits.
6. (minor under grading override) The report says in the 8.1.2 note that eight rows contradict Section 7 and in the scope paragraph that 48 rows match the keyword scan; the original finding's "30 CORE rows" is not reproduced and not used (the fix log says so). No inconsistency, only a figure that differs from the Gate 3 report.

## 4. Item Status table, report Sections 1 to 10

Basis: the fix log says only Sections 3, 4, 7, 8 and the Baseline block were edited. I re-read the edited passages in full and checked that the cross-references they use resolve (CT-1 to CT-6 at lines 3610-3615, 7.3 at 3960, 9.10 at 4782, choices A-3 to A-20 at 3654-3671, element and invariant tables at 3740-3764). I did not re-read Sections 1, 2, 5, 6, 9 and 10 in full; for those the status is "unchanged by the fix, present, no new defect seen", and their earlier minor findings stay on the follow-up list.

| Section | Item status | Evidence |
|---|---|---|
| Baseline and Conventions | OK | New "Precedence and later additions" paragraph (line 120) is accurate: both tables exist where it says; line counts it mentions match (5,098 now). |
| 1 Problem Statement | OK (unchanged) | Heading at 124; no edit. Minor notes P6-003 and P6-004 stay open as notes. |
| 2 Current State Analysis | OK (unchanged) | Heading at 139; no edit by the fix. Minor notes stay as notes. |
| 3 Target State | OK, P6-001 FIXED | Precedence paragraph and delta table at 1125-1144; right-hand cells match Section 7; minor notes 1 to 3 above. |
| 4 Gap Analysis | OK, P6-001 FIXED | Preamble pointer at 1232 lists the nine cells; G-01, G-02, G-03, G-04, G-14, G-17, G-20, G-99, G-136 target cells still carry the pre-adjudication wording and are overridden by the pointer; 4.2 narrowed in the delta table. |
| 5 External Research Findings | OK (unchanged) | Heading at 1538; ends with `Status: Complete` (2135); no edit. |
| 6 Options Analysis | OK (unchanged) | Heading at 2138; ends with `Status: Complete` (3564); no edit. Its 6.12.9 conflict outcomes are the source the delta table relies on and I read the adjudicated rows in 7.0. |
| 7 Recommendation | OK, P6-001 FIXED | One precedence sentence at 3584 only; axes, choices A-3 to A-20, elements 1 to 9, invariants I-1 to I-9 and the register are unchanged and are what the new tables cite. Minor: F-1 "strict superset" (P6-018) stays a note. |
| 8 Value Inventory and Inputs for a Later Plan | OK, P6-002 FIXED | 8.1.2 note, 11-line table and scope paragraph at 4300-4314; 8.1.4 limit 1 prefix at 4399; 8.1.0 counts and the 8.1.2 line-range table unchanged and consistent with the 6,127-line Appendix A. Minor notes 4 to 6 above. |
| 9 Open Questions | OK (unchanged) | Heading at 4689; 9.10 at 4782 resolves; the fix added nothing to Section 9 (the fix log says so, and no new open point was created that Section 9 must carry). |
| 10 Evidence Trail | OK (unchanged) | Heading at 4847; no edit. |

## 5. Count and verdict

STILL-OPEN blocking: 0. NEW blocking: 0.

F_1 = 0

Verdict: PASS

The cycle-1 fix closed both blocking findings from Gate 3 review 1. The report stays report-only, adds no [CODE-CONTRADICTED] or [UNVERIFIED] claim as fact, and adds no tag, number or plan. No second fix cycle is needed. The follow-up list from this review is the six minor notes in section 3.

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was supplied, so nothing was skipped on the strength of an rf-qa PASS. Table shape (pipe counts) I checked myself with `awk`.

**(b) Independent semantic checks:**
- Delta table right-hand cells against Section 7: read report lines 3560-3764 (axes, choices A-3 to A-20, elements 1 to 9, invariants I-1 to I-9, register) and compared 16 rows, one by one.
- Pre-adjudication wording of the delta table against the real Section 3 and 4 cells: Read of lines 1150-1209, 1225-1237, and single-line Reads of the G-04, G-14, G-17, G-20, G-99, G-136 rows (1239, 1249, 1252, 1255, 1334, 1371) and 4.2 (1407-1409).
- Appendix A line citations and Reason quotes: `sed -n <n>p` on ten lines of `synth-08-value-inventory.md` and four more by ID (VL-24-213, 215, 524, 526).
- 48-row scan claim: re-ran the keyword count over lines 45-996 (result 48); also counted 60 CORE lines with exchange terms to judge note 4.
- Appendix A untouched: `wc -lc` gives 6,127 lines and 2,024,775 bytes, as printed in the report.
- Report-only and tags: grep of the added passages for plan words (0) and evidence tags (none).

**Confidence:** Verified: 12 / 12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The 12 items are: P6-001 precedence statements; P6-001 delta rows against Section 7; P6-001 pre-wording accuracy; P6-001 required items covered; P6-002 table rows against Appendix A; P6-002 readings against Section 7; P6-002 counts and untouched Appendix A; no new unsupported claim; no [CODE-CONTRADICTED] or [UNVERIFIED] used as fact; consistency with the rest of the report (cross-references resolve); report-only; required sections present. Sections 1, 2, 5, 6, 9, 10 were not read in full; the checks above do not depend on them.

**Tool engagement:** Read: about 22 (one report read failed on size and was repeated in smaller ranges) | Grep: 7 | Glob: 0 | Bash: 4 (all read-only: `sed`, `awk`, `grep`, `wc`, `git status`/`git diff --stat`). No web research was done, so no Tavily call was needed.

Status: Complete

