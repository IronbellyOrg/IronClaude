# Gate 3 consolidated findings, cycle 2

Halt guards run before this cycle: (1) regression check: no item that passed in the first review fails now (N1 concerns RB-01, which was already a blocking finding, number 1, in the first review); (2) monotonicity: |F_2| = 1 < |F_1| = 10. No halt.

Sources: `qa-fix-verification.md` (structural, FAIL, 1 blocking) and `qa-fix-verification-qualitative.md` (qualitative, FAIL, 1 blocking). Both name the same defect (N1 in the structural report, N-1 in the qualitative one).

## Blocking findings (|F_2| = 1)

| # | Finding | Report location | Originating agent(s) | Proposed fix |
|---|---|---|---|---|
| N1 | The anchor added to RB-01(c) (Section 8.4, about line 1388) requires every question age and every question-text line "in the list and in the desk" to be amber. Step 1.4 (about line 1494) and RB-16(a) (about line 1403) build the list question text as `body_bold` (base colour, bold) and only the age as amber; research file 04 line 57 and the 160-column ledger mockup say question text is base bold in the list and amber only in the desk. A Phase 1 built exactly as planned would fail RB-01(c), a High row, so the phase could never close. | Section 8.4 RB-01(c); consistency with step 1.4, RB-16(a), Section 3.2 | rf-qa (N1), rf-qa-qualitative (N-1) | Change RB-01(c) to: question ages (list and desk) and desk question-text lines are amber; list question subject text is base colour and bold (consistent with step 1.4, RB-16(a) and 3.2); and state how the selected row is scored (its marker and line carry the `selected` role; say whether RB-16(a) accepts it). Re-read the mockup `.ansi` colour evidence in research file 04 before editing. |

## Minor findings (notes; fix only where the same text is being edited)

M1/N-3: `STATE_ROLE` is keyed by `(field, value)` tuples and `FROZEN` has no tuple form, but step 1.6(e), RB-10(d) and SC-6 describe "keys running, succeeded, failed, completed and FROZEN". M2: `test_commands.py` assertions are at :671 and :691. M3/N-2: step 0.8 baseline sentence overlaps and is wrong for RB-05 to RB-08. M4: RB-04(c) needs the whitespace-collapsed `panes_flat` for the wrapped counts line. N-4: RB-04(b) narrow-tile fallback "taller than any other text". N-5: Section 5 verification tags and the `:747-760` vs `:747-756` guard-test range. N-6: three small harness and rubric statements disagree.
