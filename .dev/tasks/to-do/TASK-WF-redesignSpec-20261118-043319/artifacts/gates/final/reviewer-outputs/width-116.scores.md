# Final gate, width 116: reviewer scorecard (iteration 1, text and ANSI tier)

Source: the fresh reviewer's JSON for width 116. failing_high_medium: none.

| Row | Result | Evidence |
|---|---|---|
| RB-01 | PASS | desk.truecolor.ansi:1 title cyan bold; ages amber bold over base bold subjects; borders slate |
| RB-02 | PASS | questions.txt:9 and desk.txt:9 heavy amber; slate RETAIN, LINKED SESSION, OBSERVATION WINDOW; cyan strip :4 |
| RB-03 | PASS | desk.txt:13 two columns 66 and 46 under full-width desk :9; questions order strip, list, RETAIN |
| RB-04 | PASS | strip cyan, figure :5-7, count line :6 whole, N=5 |
| RB-05 | PASS | DECISION DESK, reasons note, disclosure and retention intact |
| RB-06 | PASS | zero ESC in nocolor; SGR-stripped ANSI equals nocolor |
| RB-07 | PASS | no non-ASCII in ascii files |
| RB-08 | PASS | h44 to h12 within height; h8 9 rows (accepted overflow) |
| RB-09 | PASS | desk.16.ansi indexes 90, 37, 97, 96, 93, 32 distinct |
| RB-10 | PASS | alive and ACTIVE green; idle and wait base |
| RB-11 | PASS | desk.truecolor.ansi:19 unknown muted; unavailable text muted |
| RB-12 | PASS | ledger.txt:12 heading with rows; no rule row (RB-28) |
| RB-13 | PASS | desk.txt:34 key list whole |
| RB-14 | PASS | desk.txt:10-11 age then text, amber bold; values aligned |
| RB-15 | PASS | READ ONLY right-aligned, amber bold |
| RB-16 | PASS | questions.truecolor.ansi:12-16 bold rows; other lines muted |
| RB-17 | PASS | questions.txt:20-24 RETAIN CONTEXT once each |
| RB-18 | PASS | ledger.txt:2,5,10 panes, real fields only |
| RB-19 | N/A | replaced by RB-27 |
| RB-20 | PASS | desk.txt:33 rule, :34 keys intact |
| RB-21 | PASS | questions.txt:3 counts whole |
| RB-22 | FAIL (Low, deferred) | blank run 44 > 18 at 116 |
| RB-23 | PASS | desk.txt:15 marker and amber bold line |
| RB-24 | PASS | run id once (:21), count words once (:6) |
| RB-25 | PASS | questions.txt:18 reasons note; no suffix on rows |
| RB-26 | PASS | desk.txt:18 and ledger.txt:13 ACTIVE; :14 raw combination |
| RB-27 | PASS | no 32+ hex run; leftover `(plan hash )?` |
| RB-28 | PASS | ledger.txt:12 heading then rows; legend :11; shown 27/54 |
| RB-29 | PASS | desk.txt:14-19 plain labels, one value column; disclosure leads the stand-alone questions list as RB-16(c) allows |
