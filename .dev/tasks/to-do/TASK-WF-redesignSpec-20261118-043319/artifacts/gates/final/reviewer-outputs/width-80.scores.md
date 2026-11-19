# Final gate, width 80: reviewer scorecard (iteration 1, text and ANSI tier)

Source: the fresh reviewer's JSON for width 80. failing_high_medium: none. Count words are the owner-ruled short forms (scores/p4/ruling.md).

| Row | Result | Evidence |
|---|---|---|
| RB-01 | PASS | questions.truecolor.ansi title cyan bold, ages amber bold, subjects base bold, borders slate |
| RB-02 | PASS | ledger.txt:2 heavy, :6 and :11 rounded; questions.txt:4 and desk.txt:4 heavy; desk.txt:8,16 rounded |
| RB-03 | PASS | desk.txt three stacked 78-wide panes; questions.txt list pane only |
| RB-04 | PASS | questions.txt:11 `seen !done: 5 \| proof-done: unavailable (no source)`; no strip frame |
| RB-05 | PASS | disclosure, retention, source UNVERIFIED, DECISION DESK intact |
| RB-06 | PASS | desk.nocolor.txt zero ESC, same text |
| RB-07 | PASS | desk.ascii.txt:4 `+- DECISION DESK ---+` |
| RB-08 | PASS | h44 to h12 within height; h8 9 to 11 rows (accepted overflow) |
| RB-09 | PASS | desk.16.ansi 96, 93, 97, 37, 90 distinct |
| RB-10 | PASS | ACTIVE and dot green; blocked/active/none base |
| RB-11 | PASS | worktree unknown and unavailable text muted |
| RB-12 | PASS | ledger.txt:13 heading above rows |
| RB-13 | PASS | desk.txt:34-35 keys wrap between pairs |
| RB-14 | PASS | desk.txt:5-6 text leads; values at one column |
| RB-15 | PASS | READ ONLY right on line 1 |
| RB-16 | PASS | questions.truecolor.ansi:5-9 bold rows; :10-17 muted |
| RB-17 | PASS | no RETAIN frame at 80; retention once in list pane |
| RB-18 | PASS | ledger.txt:2-10 real-field panes only |
| RB-19 | N/A | replaced by RB-27 |
| RB-20 | PASS | desk.txt:33 rule, :34 keys intact |
| RB-21 | PASS | ledger.txt:9 source counts whole |
| RB-22 | FAIL (Low, deferred) | blank run 23 > 18 at 80; ledger.txt:14 |
| RB-23 | PASS | desk.txt:18 selected row amber bold with marker |
| RB-24 | PASS | text once (desk.txt:6), run id once (:16) |
| RB-25 | PASS | questions.txt:12 reasons note; no suffix |
| RB-26 | PASS | ledger.txt:14 ACTIVE; :15 raw combination |
| RB-27 | PASS | desk-planask.txt:6-8 no 32+ hex run |
| RB-28 | PASS | no flags column, rule row or +N more; legend :12; shown 26/54 |
| RB-29 | PASS | desk.txt:17-18 rows lead; plain labels at :9-14 |
