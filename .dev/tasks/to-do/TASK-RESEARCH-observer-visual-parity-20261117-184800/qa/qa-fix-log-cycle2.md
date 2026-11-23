# QA fix log, Gate 3 (Phase 6 report validation), cycle 2

Report: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md
Source finding: qa/qa-consolidated-findings-phase6-cycle2.md (blocking N1; minor M1/N-3, M3/N-2, M4 fixed only where the same text is edited)

Fixes (one line each: finding, section, change):

- N1 (blocking), Section 8.4 RB-01(c): ages (list and desk) and desk question-text lines are amber and bold; list question subject text is base and bold (`body_bold`), never amber; the selected row is scored under the `selected` role (bold amber) and is exempt from the base-subject rule but not the amber-age rule. Evidence re-read: research 04 line 57 (amber bold in desks, base bold in the 160 ledger) and line 47.
- N1, Section 8.4 RB-16(a): "every question row line carries `body_bold`" replaced by: every row line is bold, subject text is `body_bold`, the selected row is accepted in the `selected` role and not counted against the clause (matches RB-01(c), step 1.4, RB-23).
- N1, Step 1.4: `selected` role stated as bold amber, the only amber list-row text besides the age (consistent with the open-items row that says "bold amber role").
- N1, Section 3.2 (amber rows at about lines 289 and 502): "question text" narrowed to "desk question text", with a note that list/160-ledger question rows are base, so no row contradicts RB-01(c).
- M1/N-3, Step 1.4, step 1.6(e), RB-10(d), SC-6: `STATE_ROLE` keys now named as `(field, value)` tuples; `FROZEN` is held as the separate constant `FROZEN_ROLE = "state_frozen"` (a flags cell with `FROZEN_MARKER`), and the tests assert the tuple keys plus `FROZEN_ROLE`.
- M3/N-2, Step 0.8: baseline sentence now says RB-01 to RB-04 and RB-09 to RB-18 FAIL, and RB-05 to RB-08 are expected to pass on the current plain text.
- M4, Section 8.4 RB-04(c): the check reads the whitespace-collapsed plain pass (`panes_flat`) because the counts line wraps inside the tile.

Self-check (adversarial): grepped RB-01, RB-16, `body_bold`, `amber`, `selected`, `FROZEN_ROLE` after editing. RB-01(c), RB-14(b) (desk text amber bold), RB-16(a), RB-23, step 1.4, 3.2 and the open-items row agree. Not fixed (out of scope here): M2, N-4, N-5, N-6.


## Coordinator fix after the Gate 3 review cap (user-approved, 2026-11-17)

N2 (the Decision Desk `qid  age` line had a muted age in step 5.3 while RB-01(c) requires every question age amber and bold) was resolved after the two fix cycles and three reviews were used. The owner chose, in chat, to make the desk age bold amber. Edits: report step 5.3 (the `_desk_question_pane` row), report step 1.4 (the role list now names the desk `qid  age` line `attention` bold), and the same step 5.3 text in synthesis/synth-05-implementation-plan.md. No fourth review was run; Gate 4 and Gate 5 re-read the edited report.
