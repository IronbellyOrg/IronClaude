# Refactoring Plan (base: variant 1)

## Overview
Base: variant 1. Incorporated: variant 3 (PC-04, PC-05, PC-09), variant 2 (PC-06, PC-08). Changes: 10. Risk: Low except PC-01 (Medium: it rewrites a repair). Review status: auto-approved (non-interactive).

## Planned Changes
- **PC-01 (Medium risk; INV-001, INV-002, C-001, X-001).** Replace R1-F1's repair. The cell cannot carry one value that satisfies both readers (STAGE2:57 tier; `ReviewerJudge` and the Task 12 matrix read IMPORTANT as blocking, SPEC:211, SPEC:592; `agents/rf-qa.md:111` lets a reviewer grade an IMPORTANT finding minor), and `MINOR=Note` sends rows to a Notes table with no tags or `why_not_blocking` (SPEC:371, STAGE2:42). The repair text must say: Task 3 fixes the three lens-scale labels in the `labels` cell with a `model` cell that says what the values mean to each reader; recommended values `CRITICAL=Blocking;IMPORTANT=Blocking;MINOR=Medium` for the shadow comparison (SPEC:211, SPEC:592), together with a stage 2 note that the importer takes blocking or non-blocking from the reviewer's own call (a filled `why not blocking`) and uses the cell only to split non-blocking rows into Medium and Note; or a second column. This is one owner decision (which of the two forms), flagged as such. Add an acceptance line to Task 3 asserting the chosen pairs. Grade stays blocking.
- **PC-02 (C-002).** Keep R1's note on Task 12 inputs and add variant 3's repair for the family key (a `reviewers` column or resolution from the reviewing agent in `source`); grade non-blocking (final 2 of 3 advocates).
- **PC-03 (C-003, INV-004).** Add the `unsettled` tag gap as non-blocking with the repair "Task 12 adds `unsettled` through the sole writer without clearing tags, or the stage 2 revision owns it", carried as a note with no owner today.
- **PC-04 (C-009).** Add variant 3's doctor/T2 literal finding, non-blocking, with its repair (build the marker from parts; an acceptance line that `grep -n "review-severity:digest" src/superclaude/cli/doctor.py` prints nothing, valid until stage 4).
- **PC-05 (C-010, C-011).** Add `STRICT_T2` effect and banned-phrase scan gap, non-blocking.
- **PC-06 (C-012).** Add variant 2's audit-artifact finding as a run note (not a plan defect) and the supplemental rows for source lines 51 to 53 in the inferred-requirements table.
- **PC-07 (C-005, INV-003).** Keep R1-F3 non-blocking; add the repair "Task 8: filing is refused unless an Offers row with an explicit filing answer and a matching `set_digest` exists; a resume returns the pending offer without asking".
- **PC-08 (C-007).** Keep R1-F5 and add: use a `recorded` or `offered` row; `pending` is an Offers state.
- **PC-09 (C-008).** Merge R1-F6 and variant 3's R3-F6 (stale stage 2 quotes at STAGE2:27 and STAGE2:57).
- **PC-10 (format).** Fix the id slip (R1-Fk), replace the hedged verdict with one verdict NEEDS-REVISION naming C-001 as the one blocking finding and noting the closest-call status, and add a "Checked and found clean" and a "Not checked" list (variant 3's pattern).

## Changes NOT Being Made
- Variant 2's blocking grade for C-002 and C-003: rejected; no requirement or exit test of this plan fails (advocate 2 conceded this in Round 2); both stay non-blocking notes.
- Variant 3's PASS verdict: withdrawn by its own advocate.
- Variant 1's `IMPORTANT=Medium` repair as stated: rejected (INV-001).
- Raising C-005 to blocking (INV-003): rejected; T8 can be met by building consent into the filing code; the repair is added instead.

## Risk Summary
PC-01 changes a repair; rollback: restore variant 1's text. Others are additive.

## Review Status
auto-approved
