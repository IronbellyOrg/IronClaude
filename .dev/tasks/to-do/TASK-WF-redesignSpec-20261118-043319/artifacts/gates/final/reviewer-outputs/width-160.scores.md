# Final gate, width 160: reviewer scorecard (iteration 1, text and ANSI tier)

Source: the fresh reviewer's JSON for width 160. failing_high_medium: none.

| Row | Result | Evidence |
|---|---|---|
| RB-01 | PASS | desk.truecolor.ansi: title cyan bold, age and question text amber bold, subjects base bold, header2 and footer muted, borders slate |
| RB-02 | PASS | desk.nocolor.txt:9 heavy DECISION DESK, rounded LINKED SESSION; questions strip :4, attention :9, RETAIN :19; ledger panes :5 and :9 |
| RB-03 | PASS | desk.nocolor.txt:9-20 two columns 76 and 80; questions order strip, list, RETAIN |
| RB-04 | PASS | questions.nocolor.txt:5-7 three-row figure; :6 full count line; 5 rows |
| RB-05 | PASS | literals whole in desk.nocolor.txt:16-24 |
| RB-06 | PASS | no ESC byte in any nocolor file |
| RB-07 | PASS | no non-ASCII in ascii files; borders + - \| |
| RB-08 | PASS | max width 160; h12 12 rows; h8 9 rows (accepted diagnostic overflow); footer last |
| RB-09 | PASS | desk.16.ansi distinct codes 32, 37, 90, 93, 96, 97 |
| RB-10 | PASS | running and ACTIVE green, idle and wait base |
| RB-11 | PASS | unknown, reasons note and unavailable text muted |
| RB-12 | PASS | ledger.nocolor.txt:11 heading above rows, no rule row |
| RB-13 | PASS | key list whole at 160 |
| RB-14 | PASS | desk.nocolor.txt:10-11 age then text; values aligned at column 10 |
| RB-15 | PASS | READ ONLY right-aligned on line 1 of every screen |
| RB-16 | PASS | questions.truecolor.ansi:11-15 bold rows; caveat lines muted, not bold |
| RB-17 | PASS | questions.nocolor.txt:19-23 RETAIN CONTEXT, three lines once each |
| RB-18 | PASS | ledger.nocolor.txt:2-9 panes hold real fields only |
| RB-19 | N/A | replaced by RB-27 |
| RB-20 | PASS | desk.nocolor.txt:31 rule above footer :32 |
| RB-21 | PASS | ledger.nocolor.txt:7 counts whole |
| RB-22 | FAIL (Low, deferred) | blank run 44 > 18 at 160; ledger.nocolor.txt:12 |
| RB-23 | PASS | desk.truecolor.ansi:15 selected row amber bold with marker |
| RB-24 | PASS | run id once (:22), count words once (:6); list row clipped |
| RB-25 | PASS | questions.nocolor.txt:17 reasons note; no per-row suffix |
| RB-26 | PASS | ledger.nocolor.txt:12 ACTIVE; :13 raw blocked/active/none |
| RB-27 | PASS | no 32+ hex run; desk-planask.nocolor.txt:14 `(plan hash )?` |
| RB-28 | PASS | no flags column, rule row or +N more; legend :10; footer shown 34/54 |
| RB-29 | PASS | desk.nocolor.txt:14-15 rows lead list; plain labels in one column; no msg_ id |
