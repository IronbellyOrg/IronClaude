ROUND 1, TWO-COLUMN ADVOCATE (read from the six PNGs and the spec files; row counts are my reading of the images, about 21 px per row)

Facts checked in the files
- rendering-rules.md line 43 says "One stacked block at every width of 80 columns or more" and keeps the two-column layout as "design reference". Line 57 says the Decision Desk is "one stacked block under the question list".
- FINDINGS.md M-03 and M-04 are both High, both reviewers agree, and both need the owner (O-1) because they reverse those two lines. The 160 mockups put the questions left and the count tile plus context right; the desk has evidence on the right.
- REDESIGN-SPEC.md says frames add 2 rows each and Live(screen=True) crops silently from the bottom (footer keys vanish). RB-03 requires two columns at 160 and 116, stacked at 80.

CASE 1: questions screen, 160 columns
- Stacked: one frame of about 11 rows. The caveat fits on one line, the 3 questions sit in rows 5 to 7, under 4 lines of grey prose.
- Two columns: left frame of 8 rows, right column of about 16 rows (count tile 5 glyph rows plus text, then RETAIN CONTEXT).
- Where the eye goes: in stacked, the first thing is "one Run only" and the caveat, not a question. In two columns the left frame opens with the question rows after one wrapped caveat, and the big orange "3" tile is the only thing on the right that pulls the eye. The caveat and retention text are demoted into a dim box.
- Stacked genuinely wins on height: about 11 rows against about 16, and the right column has 6 wrapped lines of low-value text.
- Verdict: MIXED, 55 percent. Two columns win on question primacy (M-03), stacked wins on rows.

CASE 2: questions screen, 116 columns
- Stacked: about 11 rows. The 64-hex hash line fits on one row at 116, the caveat wraps to two rows.
- Two columns: left pane is 70 wide, so the question wraps to 3 rows and "reason unknown" falls onto an orphan row; the pane is about 13 rows and the right column about 16.
- This is the weakest case for two columns. Wrapping the question text is the exact thing a reader is trying to read, and the right column costs 5 extra rows for a tile and a dim box.
- Verdict: STACKED, 70 percent. I concede it.

CASE 3: Decision Desk, 160 columns
- Stacked: three frames, about 22 rows (desk 5, linked session 12, questions 6, plus gaps). Three frames means 6 border rows, and the question list is pushed to the bottom, which is the part most likely to be cropped.
- Two columns: left holds desk (6 rows) over questions (8 rows) for about 14 rows; linked session sits right at about 12 rows. Total about 14 rows against 22, so about 8 rows saved (36 percent).
- Wrapping cost is small: the desk question wraps to 3 rows instead of 3 (hash on its own row either way), the linked-session note wraps to 2 rows. The 64-hex hash still shows in full.
- Eye: the question and the other questions are together on the left, the evidence on the right. This is exactly the original decision-desk mockup (question and other questions left, evidence right) and it removes the 12-row key/value block that sits between the question and the list in stacked.
- Height argument is on my side: fewer rows means the footer keys survive on a shorter terminal.
- Verdict: TWO COLUMNS, 80 percent.

CASE 4: Decision Desk, 116 columns
- Stacked: same 22 rows as at 160, because nothing wraps.
- Two columns: desk full width (5 rows) over two side-by-side panes (linked session 12 rows, questions 12 rows). About 17 rows against 22, saves about 5. This matches the 116 mockup (question full width over two side-by-side panes).
- Honest cost: the right questions pane is about 44 wide. The hash is cut to "012345678..." with an ellipsis, "reason unknown" wraps, and the question takes 4 rows. A reader loses the full hash, which the Q7 hash fixture exists to protect. That is a real defect unless the pane wraps the hash instead of cutting it.
- Verdict: TWO COLUMNS, 60 percent, conditional on wrapping the hash instead of cutting it. If the cut stays, call it MIXED.

Summary of where each side wins
- Stacked wins: questions at 116 (clear), questions at 160 (height), simpler code (no side-by-side width math, no per-pane heights, which is P3 versus P4 and P5 in the plan).
- Two columns win: desk at 160 (clear), desk at 116 (with the hash fix), question primacy on the questions screen at 160.
- Suggested split if the owner wants one rule: two columns for the desk at both widths, two columns for questions at 160 only, stacked everywhere else.
