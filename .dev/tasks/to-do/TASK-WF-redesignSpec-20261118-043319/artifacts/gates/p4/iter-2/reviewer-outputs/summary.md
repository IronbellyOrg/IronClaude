# Phase 5 gate (plan Phase 5, spec Phase 4), iteration 2: reviewer scorecards

Three fresh reviewers, one per width, text and ANSI tier (the PNG route is unavailable). NO_COLOR and ASCII passes present and read (ASCII: `+ - |` borders, `#` block figure, no `?` on a border). Script rows come from `../checks.json`: every row passes except RB-22 (Low, deferred).

Owner ruling used (2026-11-18, in chat; see `.dev/issues/409/visual-parity/scores/p4/ruling.md`): at 80 columns the questions list count line reads `seen !done: N | proof-done: unavailable (no source)`; RB-04 (c) and (d) are read with those short forms at 80 columns.

| Row | 160 | 116 | 80 | Evidence |
|---|---|---|---|---|
| RB-01 colour roles | PASS | PASS | PASS | eight palette triples; title bold cyan; ages bold amber; subjects bold base |
| RB-02 titled frames | PASS | PASS | PASS | strip cyan, list heavy amber, RETAIN and secondary slate; desk heavy amber |
| RB-03 questions order | PASS | PASS | PASS | strip, list, RETAIN at 160 and 116 (questions.txt:4, 9, 20); list only at 80 |
| RB-04 count strip | PASS | PASS | PASS | 3-row block figure in a cyan frame; full count line at 160 and 116; short-form line at 80, no strip |
| RB-05 to RB-11, RB-13, RB-15, RB-20, RB-21 | PASS | PASS | PASS | script rows copied; literals whole; NO_COLOR 0 ESC; ASCII pure |
| RB-12 heading | PASS | PASS | PASS | heading present, no rule row under it (RB-28), as logged in scores/p2/notes.md |
| RB-16 hierarchy | PASS | PASS | PASS | rows bold, caveat lines muted and not bold; first line after the disclosure is a row |
| RB-17 RETAIN census | PASS | PASS | PASS | run, caveat and retention each once; RETAIN frame at 160 and 116 only |
| RB-22 blank band | FAIL | FAIL | FAIL | Low, deferred (44 at 116, 25 at 80, N = 18) |
| RB-24 to RB-29 | PASS | PASS | PASS | census, reasons, badge, no hash, ledger diet, labels |

failing_high_medium: [] at every width.

Iteration 1: the 80 column reviewer failed RB-04 (the short count line lacked `(no source)`); 160 and 116 passed. The owner ruled on the wording (short forms at 80 only); iteration 2 passes.

Extra check asked for by Task 21 (stacked layout and invented content): strip, list and RETAIN CONTEXT stack in the order of the stacked option at 160 and 116 (rows RB-02 and RB-03 above); a search for `owner`, `requester` and `mapped` over every iteration 2 render (`*.txt`, `*.nocolor.txt`, `*.ascii.txt`) found nothing, and the reviewers saw no owner, requester, mapped-tree or signal-bar content.
