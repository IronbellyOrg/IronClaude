```json
{
  "width": 80,
  "iteration": 1,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "checks.json RB-01 pass (all eight palette triples). questions.truecolor.ansi:1 title is 1;38;2;112;205;226 (cyan bold); :12-16 ages are 1;38;2;250;178;25 and subjects 1;38;2;225;233;238; desk.truecolor.ansi:15-16 and desk-planask.truecolor.ansi:15-19 are amber bold; header2, keys and footer are 165,182,194 (desk:2,33-35). Clause (e) not applicable."},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 status pass (all cases); desk.txt:14 'DECISION DESK' and desk.txt:28 retention line printed whole"},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass; grep for ESC in all four *.nocolor.txt files gives 0 matches"},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass; grep for non-ASCII bytes in all four *.ascii.txt files gives 0 matches"},
    "RB-08": {"result": "FAIL", "evidence": "checks.json RB-08 ledger@80: 'footer keys are not among the last lines'; ledger.txt:41 keys hint is cut ('... m mark  e exp>') and line 42 is the 'shown' line"},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass; questions.16.ansi uses 1;96 cyan, 97 base, 37 muted, 1;93 amber, 1;90 slate, desk.16.ansi:23 uses 32 green, all distinct"},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass; desk.truecolor.ansi:23 'liveness: alive (terminal)' is 139,215,175 (state_running); :18-22 idle, active, active, none, wait are base 225,233,238; STATE_ROLE in theme.py:95-103 is non-empty with FROZEN_ROLE defined"},
    "RB-11": {"result": "FAIL", "evidence": "questions.truecolor.ansi:3 'source counts: unknown' is base 225,233,238, not muted; desk.truecolor.ansi:13 and desk-planask.truecolor.ansi:13 print 'reason unknown' inside the amber bold selected-row run, not muted"},
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi:13 selected row is '▸ 59m  Ship the change now?  reason unknown' in 1;38;2;250;178;25 (bold amber) while unselected row :12 subject is base bold; desk-planask.truecolor.ansi:13 same"}
  },
  "failing_high_medium": ["RB-08", "RB-11"]
}
```
