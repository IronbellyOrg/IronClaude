# Round 1: advocate for STACKED

Row counts are read off the images (about 21 pixels per row), so they are approximate (plus or minus one).
Spec facts checked in the files: rendering-rules.md line 43 (one stacked block at every width of 80 or more) and
line 57 (one stacked Decision Desk); REDESIGN-SPEC.md 8.3 (frames cost 2 rows each; footer keys are dropped first
when rows run past the height); FINDINGS.md M-03 and M-04 (both need the owner's yes, O-1/D-1; if no, P3 stacked
frames stay and P4/P5 are skipped).

## 1. Questions screen at 160 columns
- Height: A is about 11 rows (one frame). B is about 17 rows, because the right column stacks two frames
  (tile, then RETAIN CONTEXT) and sets the height. The left pane in B is only 7 rows, so about 10 rows of the
  left side are empty. B costs about 6 more rows, and rows past the height are cut from the bottom, which is
  where the footer keys are.
- Where the eye goes: in A the bold cyan line "seen, not resolved: 3 | closed by evidence: unavailable" sits
  inside the amber pane, directly above the questions. In B that sentence moves to a small right tile that
  starts with a five-row block-glyph "3" (about 5 of its 8 rows are the glyph), and the first thing in the
  left pane is the disclosure sentence, not the count.
- B splits one disclosure across three places: the "bounded best effort" text on the left, the count on the
  right tile, and "no read marker in source" / "retention reset" in RETAIN CONTEXT. The spec says the caveat
  text is required in full and never squeezed. A keeps all of it in one read order.
- The 64-hex hash line is identical in A and B (the left pane in B is 114 wide), so B gains nothing there.
- Where two columns wins: it looks like the mockup (agent-focus-attention-ledger.png), and the questions
  pane gets a clean amber frame without the muted lines above the rows. That is parity, not readability.
- Verdict: STACKED, confidence 70%.

## 2. Questions screen at 116 columns
- Height: A is about 12 rows. B is about 17 rows. B's left pane (70 wide) wraps the disclosure to 2 lines and
  the Approve question to 4 lines (hash alone on line 3 or 4), and "reason unknown" falls onto its own line.
  In A at 116 the question line is still 2 lines (text, then hash plus "reason unknown" on one line).
- Reading: in B the right column is 42 wide, so the retention text wraps to 6 lines of ragged short lines
  ("questions stay listed", "observed before this start are not / retained"). In A each caveat is one clean line.
- B also repeats the count: the tile content "seen, not resolved: 3 | closed by evidence..." duplicates what A
  shows once. RETAIN CONTEXT adds no fact that A lacks; it only moves the lines.
- Where two columns wins: nothing real. The 42-wide right column is cramped at 116.
- Verdict: STACKED, confidence 75%.

## 3. Decision Desk at 160 columns
- Honest concession: this is where two columns wins on height. A is about 22 rows (desk 4, LINKED SESSION 13,
  COORDINATOR QUESTIONS 6, plus gaps). B is about 14 rows, because the 13-row LINKED SESSION pane sits beside
  the 4-row desk and 8-row question list. A uses about 8 more rows, and 3 frames cost 6 of them.
- B also matches the mockup (decision-desk.png: question left, evidence right).
- Against B: the desk question wraps to 4 lines in the 76-wide left pane (hash on the last line, whole), while
  in A it is 3 lines. The selected row in the list below repeats the same text in both layouts (it is the same
  question shown twice either way). B's left pane has a ragged "reason / unknown" break at the end of the
  hash line, which A does not have.
- In A the amber desk is first on the screen, then session evidence, then the list. The eye goes to the
  amber pane first in both.
- Verdict: MIXED leaning TWO COLUMNS, confidence 60%. If the terminal is at least about 48 rows tall, A is
  affordable; below that, B protects the footer.

## 4. Decision Desk at 116 columns
- Height: A about 23 rows, B about 18 rows. B wins by about 5 rows, but less than at 160.
- Cost in B: the question pane is only 42 wide, and the Approve line shows
  "0123456789abcdef0123456789abcdef012345678..." with a truncation mark. The 64-hex hash is no longer whole.
  The spec's Q7 check (RB-19) asks for the hash whole on one line and nothing lost. A keeps the whole hash.
- B also wraps "reason unknown" onto separate lines in the narrow pane (two rows each for the 59m lines),
  which eats back some of the height it saved (the 3-question list is 9 rows in B against 6 in A).
- Where two columns wins: shorter, and the desk is full width over two panes (the mockup 116 layout).
- Verdict: MIXED, confidence 55%. A hash that has to be read whole is a safety-of-meaning issue for an
  approval question; that is the one reason I lean STACKED here.

## 5. Cross-cutting facts for stacked
- 80 columns is stacked in both options (questions-80.png, desk-80.png), so stacked code must exist and be
  tested anyway. Two columns adds a second layout path at 160 and 116 (two widths, two screens), more golden
  files and more height cases (P4, P5), each adding frame rows that the 8.3 height rule must count.
- The failure mode the spec names (footer keys cropped without warning) hits two-column more on the questions
  screen (17 vs 11 rows) and stacked more on the desk (22 vs 14 rows). The cheapest hedge is stacked for
  questions and a height-based choice for the desk.
- Mockup parity: both mockups have large empty areas in their left panes (the 160 ledger pane is about
  half empty), so parity is a look, not a gain in information per row.

## One-line verdicts
- Questions 160: STACKED (70%).
- Questions 116: STACKED (75%).
- Decision Desk 160: MIXED leaning TWO COLUMNS (60%).
- Decision Desk 116: MIXED (55%).
