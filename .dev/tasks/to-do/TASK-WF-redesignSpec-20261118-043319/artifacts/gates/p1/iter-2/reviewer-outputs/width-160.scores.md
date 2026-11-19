```json
{
  "width": 160,
  "iteration": 2,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "All fg triples are in the 8-colour palette on all four screens. questions.truecolor.ansi:1 header cyan+bold. Ages (:11-15) are amber+bold with base+bold subjects. desk:12 is the selected row, exempt. Desk question text lines (desk-planask:15-16) are amber+bold. Freshness (:2), keys hint and footer (:23) are muted. Ledger plain cells are base. (e) not applicable."},
    "RB-02": {"result": "N/A", "evidence": "N/A (scheduled P3)"},
    "RB-03": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-04": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 status pass (all). Literals such as 'DECISION DESK' (desk.txt:13), 'reason unknown' (questions.txt:11) and 'nextAction.kind: wait' (desk.txt:21) are whole."},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass. I read the files: no ESC byte in any .nocolor.txt, and each .truecolor, .256 and .16 file with SGR stripped equals the .txt (ledger, questions, desk, desk-planask)."},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass. All four .ascii.txt and .ascii.ansi files are pure ASCII (every char code below 128)."},
    "RB-08": {"result": "PASS", "evidence": "At 160, max line width is 160 cells and the footer keys are the last line (ledger.txt:48, desk.txt:33). No SGR 5/6 and no mouse sequences. The only RB-08 fail in checks.json is ledger@80, not this width."},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass. theme.py:80-88 'standard' table: base bright_white, muted white, slate bright_black, amber bright_yellow, cyan bright_cyan, green green, red red, violet magenta, all distinct. The .16.ansi SGR codes 97, 37, 90, 93, 96 and 32 are all different."},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass. Spot check: 'running' and 'alive' are green (ledger.truecolor.ansi:12, desk:22, desk:30). idle, blocked, active and none are base. All words are printed in the plain pass."},
    "RB-11": {"result": "FAIL", "evidence": "questions.truecolor.ansi:9 and desk.truecolor.ansi:9 'seen, not resolved: 5 | closed by evidence: unavailable (no source)' is one base-colour span, so the absent value 'unavailable (no source)' is not muted. Other absent values are muted (:3, :4, desk:24)."},
    "RB-12": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-13": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-14": {"result": "N/A", "evidence": "N/A (scheduled P5)"},
    "RB-15": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-16": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-17": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-18": {"result": "N/A", "evidence": "N/A (scheduled P6)"},
    "RB-19": {"result": "N/A", "evidence": "N/A (scheduled P3)"},
    "RB-20": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-21": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-22": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi:12 the selected row '▸ 59m  Ship the change now?' is wholly bold amber. The unselected row at :11 is amber age, base-bold subject and muted reason, so the selected row has its own role style plus the glyph."},
    "RB-24": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-25": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-26": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-27": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-28": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-29": {"result": "N/A", "evidence": "N/A (scheduled P2)"}
  },
  "failing_high_medium": ["RB-11"]
}
```
