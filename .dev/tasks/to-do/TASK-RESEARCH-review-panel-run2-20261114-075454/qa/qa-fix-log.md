# Gate 3 fix log (cycle 1, single fix agent)

Input: `qa/qa-consolidated-findings-phase6.md` (F_0 = 2: P6-001, P6-002). Target: `RESEARCH-REPORT-review-panel-unification-run2.md`.
Minor findings P6-003 to P6-110 were not touched (never fixed in the gate, never rechecked). Only the report and this log were edited. The two fixes are additions: the report grew from 5,057 to 5,098 lines (+41). No heading changed, so the Table of Contents is unchanged; no id, count or table elsewhere was renumbered. The Gate 3 reports and `qa/report-size-and-partition.md` were not edited, and their line numbers refer to the report as it stood when they were written (the report now says this in "Baseline and Conventions").

Status: Complete

## P6-001 (blocking): Sections 3 and 4 targets not reconciled with the adjudicated Section 7

Chosen fix: a precedence paragraph plus a delta table at the head of Section 3, pointers in Section 4 and 7.0.1, and one row for 4.2 (no target cell was rewritten, so every research-derived target stays visible and the table says which Section 7 outcome replaces it). Every right-hand cell of the table is taken from the Section 7 text it names (7.0 axes 1, 2, 4, 5, 8, 9, 11; choices A-3, A-4, A-6, A-7, A-8, A-9, A-11, A-13, A-14, A-15, A-16; 7.0.1; 7.1 elements 1, 2, 4, 5, 6, 8 and invariants I-3, I-4, I-8; the 7.1 register). No new fact, number or decision was added.

| Place in the report | Before (one line) | After (one line) |
|---|---|---|
| Section 3 head, after "This section states the target, not a plan..." | no statement of which section governs | "**Precedence between Sections 3 and 4 and Section 7 (read this first).** ... Section 7 governs" followed by a 4-column delta table (Section 3 or 4 item, pre-adjudication wording, adjudicated outcome that governs, Status) |
| Delta table rows | none | T-1 (narrowed), T-2 (withdrawn, 7.0 axis 8 / C-04), T-3 (narrowed), T-4 and 3.5 DO4 (replaced, A-13 / C-05), 3.5 other open decisions (replaced), 3.2 Finding contract with G-01, G-02, SC-01, SC-02 (replaced, C-01), 3.2 Merge cluster verify (narrowed), G-04 (replaced), G-03 and G-17 with 3.2 Ledger and verdict (narrowed, C-02), G-14 with SC-05 (narrowed, no expiry), 3.2 Dispatch and identity with G-136 and SC-11 (narrowed, A-6, A-7), G-20 with 3.2 Reflect-specific (replaced, C-04), G-99 (replaced, C-01, C-11), 3.2 Run record memory (narrowed), SC-29 (narrowed, A-11), 4.2 Rule C8 check (narrowed) |
| Section 4 preamble, "Columns: ..." line | "Gap ids are G-nn." | "... The Target State cells state the pre-adjudication target: ... Section 7 governs, and the delta table at the head of Section 3 names the cells concerned (G-01, G-02, G-03, G-04, G-14, G-17, G-20, G-99, G-136)." |
| Section 7.0.1, before "How the 15 outcomes combine into one design" | no precedence sentence | "Precedence. Section 3 (...) and the Target State cells of Section 4 were written before the adjudication fold. Where they differ from 7.0, 7.0.1 or 7.1, this section governs; ..." |
| Baseline and Conventions, after "Source key" | none | "**Precedence and later additions.** ..." (also covers P6-002 and the line-count notice) |

Conflicts named by the finding and where each is now resolved: (i) T-2 versus 7.0 axis 8: row T-2; (ii) Finding contract, SC-01, SC-02 versus 7.0 row 2, 7.1 element 1, I-3: finding-contract row; (iii) G-14, SC-05, 3.2 Ledger versus "no expiry in the core": G-14 row; (iv) G-136, 3.2 Dispatch, SC-11 versus 7.1 element 6 and A-6: dispatch row; (v) 3.2 Merge versus 7.1 element 2: merge row; 4.2 versus `panel` rejected until Stage 3: 4.2 row. SC-11 is stated as holding "as a repeat is recorded", not "prevented by default", which is the A-6 outcome.

Limit stated in the report: the table lists items found by comparing the 7.0, 7.0.1 and 7.1 text with Sections 3 and 4; it is not a second review of every row.

## P6-002 (blocking): value-inventory destinations contradict the adjudicated architecture

Chosen fix: the table-in-the-report option (the finding's first fix), not a re-route in `synth-08-value-inventory.md`. Reason: rule 4 limits edits to the report and this log, and a re-route would change the 8.1.0 counts and the 8.1.2 line ranges across a 6,127-line file. The Appendix A rows, the 8.1.0 counts and the 8.1.2 line ranges are unchanged. The adjudicated reading of each row comes from 7.0 axis 4, choice A-4 and the C-02 result (`reviews/adversarial/ledger-clearing-and-verdict-authority/ADJUDICATION-RESULT.md`: "no category predicate and no grader in the core"), 7.0 axis 10 ("port contracts, not scripts"; the grader and the ledger sweep are "optional modules or evaluation instruments"), 7.0.1 fact F-4, 7.1 elements 4 and 5 and the 7.1 register. Where 7.0 does not choose (grader as optional module or EVAL instrument; script rows as DROP) the report says it is a reading and not a decision.

| Place in the report | Before (one line) | After (one line) |
|---|---|---|
| 8.1.2, after the reconciliation line and before "#### 8.1.3" | none | Paragraph "**Rows whose ledger destination differs from the adjudicated architecture (report note added after Gate 3 review 1; not carried text).**" saying Section 7 governs and Appendix A is unchanged |
| 8.1.2 table (5 columns) | none | Rows VL-24-214, VL-24-218, VL-24-268, VL-24-269, VL-24-295, VL-24-525, VL-24-259, VL-24-278 (each with its Appendix A line, kind, ledger destination CORE, adjudicated reading, Section 7 source) plus VL-23-035 and DR-113 as context rows |
| 8.1.2, "Scope of the exceptions" paragraph | none | keyword scan of the CORE group (Appendix A lines 45 to 996) for the variant scripts and the grader: 48 rows, including the eight; the other 40 are read under the same rule (VL-24-524 and VL-24-526 already say "ideas, not the script"); all other rows keep their ledger destination and were not re-judged |
| 8.1.4 limit 1 (carried text) | "1. Re-validation against the split was targeted, ..." | same text, prefixed with a bracketed report note that the destinations predate the adjudication fold and pointing to the 8.1.2 table |

Counts checked while writing: the 48 in the scope paragraph is my own scan (awk over Appendix A lines 45 to 996, case-insensitive for `review_ledger.py`, `stoprule`, `diffgate`, `finding-grader`, `fix_audit`, "blind grader", "blind-grader", "fix-audit"); the finding's "30 CORE rows" figure is not used because it could not be reproduced from the sources in scope. Table column counts of both inserted tables were checked (4 and 5 columns on every line).

## Findings not fixed

None of the blocking findings is left unfixed. P6-003 to P6-110 are minor and were left alone by instruction. Open points that remain by design and are stated in the report: Section 7 axis 10 does not choose between "optional module" and "evaluation instrument" for the grader and the ledger sweep; the DROP reading for the two script rows is marked as a reading. The pre-existing `[UNVERIFIED]` items and Section 9 were not changed, so nothing was added to Section 9.
