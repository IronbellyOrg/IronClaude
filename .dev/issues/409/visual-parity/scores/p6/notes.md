# Phase 7 (spec Phase 6): ledger table measurement and frame decision

Written in plan Task 25 (2026-11-18). Spec step 6.1 asked to measure the `flags` column; Part C removed it in Task 15, so the measurement is of the table as it now exists.

## Measured (render.py `_marker`, `_status_text`, `_alive_text`, `dispatch_id`; fixtures with `Session(show_historical=True)`, `fixture_view`)

| Fixture | Rows | Marker cell | Longest status | Longest alive | Longest dispatchId | FROZEN rows |
|---|---|---|---|---|---|---|
| base | 80 | 2 | 35 | 7 | 5 | 1 |
| empty | 0 | n/a | n/a | n/a | n/a | n/a |
| source-loss | 5 | 2 | 28 | 7 | 5 | 0 |
| injection | 3 | 2 | 28 | 7 | 7 | 0 |
| missing-fields | 5 | 2 | 28 | 9 | 7 | 0 |
| long-identifiers | 4 | 2 | 28 | 7 | 146 | 0 |

The 35-cell status is the FROZEN case (`FROZEN` and a space before a raw status). The marker cell is always the 2 cells of the column; nothing in it is cut.

## Does a border-only frame fit the 160-column table?

Yes. A border-only frame (no padding, no margin) has inner width `width - 2` = 158.

- Fixed cells at 160: marker 2, run 12, workerState 12, nextAction.kind 16, alive 14, evidence age 12 = 68, and 7 separators = 75.
- Longest status 35 leaves 158 - 75 - 35 = 48 cells for dispatchId, which is exactly the existing 48-cell cap. At 160 cells the id column was already capped at 48, so no column changes width at 160.
- At 116 (inner 114) the id column is 33 against 35 before, and at 80 (inner 78) it keeps at least the 20-cell minimum; only the long-identifiers fixture (146 characters) is clipped, as it was.
- Test: `test_the_columns_fit_the_cells_they_are_given_and_keep_their_set` checks every width at `width` and `width - 2`.

## Decision

Frame the ledger table at all three widths with a border-only frame (inner width `width - 2`, no padding, no margin). The 160-column unframed-under-a-titled-rule fallback of spec step 6.1 is not needed.

## Change made

`_columns(policy, avail, status_needed, alive_needed, id_needed)` uses `avail` in every width sum; `_row_segments(..., avail)` and `_header_lines(columns, policy, avail)` clip to `avail`. `_compose` passes the screen width for now; Task 26 passes the pane inner width. The three column sets are unchanged (AD-3, AD-6).

## Task 26: framed head and the small-height threshold

The questions-off ledger now has three full-width panes: the attention pane (heavy amber, `COORDINATOR QUESTIONS`, the gap notice and the historical-hidden note), the observation pane (round slate, `OBSERVATION WINDOW`: `header2`, the counts laid out to the inner width of 156, 112 or 76, and `changes_line`) and the ledger pane (round slate, border only, titled with `view.ledger_title`: the legend, the column heading and the rows). The title bar, the filter input, the notes, the one-off message, the footer rule and the footer stay outside the frames.

Rule: the framed ledger is drawn only while at least three ledger rows fit (fewer when fewer rows exist); otherwise the plain head of Phase 3 is kept. The forced single ledger row of the plain path stays the last resort.

Measured first height that is framed (six fixtures, `base`, `empty`, `source-loss`, `injection`, `missing-fields`, `long-identifiers`):

| Width | Lowest first framed height | Highest first framed height |
|---|---|---|
| 160 | 15 (empty) | 17 (base, source-loss, missing-fields) |
| 116 | 16 (empty) | 18 (base, source-loss) |
| 80 | 17 (empty) | 20 (source-loss) |

So 12 and 8 rows are always plain (the `lines_*x12` golden keys keep their plain form), and 24, 40 and 44 are always framed. No height from 12 up exceeds the budget in any fixture.
