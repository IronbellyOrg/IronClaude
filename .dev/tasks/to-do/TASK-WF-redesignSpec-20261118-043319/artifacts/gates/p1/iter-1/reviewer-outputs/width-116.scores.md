```json
{
  "width": 116,
  "iteration": 1,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "checks.json RB-01 pass; my decode of all four truecolor files finds only palette triples. questions.truecolor.ansi:1 header cyan bold, :12 age amber bold with subject base bold, :2 freshness muted, :22 keys hint and :23 footer muted. desk.truecolor.ansi:16 question text amber bold. The selected row (desk :13) is exempt. Clause (e) treated as not applicable."},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 pass; I confirmed 'DECISION DESK' (desk.txt:14), 'reason unknown' (questions.txt:12) and the retention line (questions.txt:17), all whole and uncut."},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass; grep for ESC bytes across *.nocolor.txt returns 0."},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass; a non-ASCII byte count across *.ascii.txt returns 0."},
    "RB-08": {"result": "PASS", "evidence": "checks.json has no failing case at 116 (its only RB-08 failure is ledger@80); manifest widest_cell is at most 116 and lines at most 42; no SGR 5/6 found in *.truecolor.ansi."},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass; the 16-colour SGR set in desk.16.ansi shows distinct indexes: 97, 1;90, 1;93, 1;96, 32 and 37."},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass; desk.truecolor.ansi:23 'liveness: alive (terminal)' is green and ledger rows show 'alive' green. Non-table values such as 'workerState: idle' (:18) and 'dispatchStatus: active' (:19) are base."},
    "RB-11": {"result": "FAIL", "evidence": "questions.truecolor.ansi:3 and desk.truecolor.ansi:3 print 'source counts: unknown' in base colour, not muted. (Line 4 'cost unavailable' is also base.) The other absent values are muted: 'unavailable (no source)' (:3), 'unknown (absent in source)' (desk :25) and 'reason unknown' (:12)."},
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi:13 and desk-planask.truecolor.ansi:13: the selected row '▸ 59m ...' is entirely bold amber, which is a role style beyond the glyph; the unselected row :12 is base bold."}
  },
  "failing_high_medium": ["RB-11"]
}
```

Every other row is `N/A (scheduled P<n>)`: RB-02, RB-03, RB-04, RB-12 to RB-22 and RB-24 to RB-29.
