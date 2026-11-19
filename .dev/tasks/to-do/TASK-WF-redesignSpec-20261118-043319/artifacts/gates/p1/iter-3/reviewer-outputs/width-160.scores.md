```json
{
  "width": 160,
  "iteration": 3,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "checks.json RB-01 pass. I decoded the truecolor files: every foreground triple is one of the eight palette colours. desk.truecolor.ansi:1 is cyan bold. Ages are amber bold (questions:11 '1h', desk-planask:14-16 question text). Subject text is base bold (questions:11 'synthetic question 0'). Lines 2, 18 and 23 (header2, column heading, keys hint) are muted. Check (e) not applicable."},
    "RB-02": {"result": "N/A", "evidence": "N/A (scheduled P3)"},
    "RB-03": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-04": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 pass. I confirmed in questions.txt:8 the gap notice 'bounded best effort; coverage unknown; at most 100 rows per read...', in :11 'reason unknown', and in desk.txt:13 'DECISION DESK'. No mid-token cuts at 160 on these lines."},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass. I counted 0 ESC bytes in all four *.nocolor.txt files. The SGR-stripped truecolor, 256 and 16 files each match <screen>.txt and <screen>.nocolor.txt (diff, for ledger, questions, desk, desk-planask)."},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass. grep for non-ASCII bytes returned 0 hits in ledger, questions, desk and desk-planask .ascii.txt and .ascii.ansi. The ledger rule row is '--' in ledger.ascii.txt. No border exists yet."},
    "RB-08": {"result": "PASS", "evidence": "checks.json lists no 160 case for RB-08. Its only failure is ledger@80 ('footer keys are not among the last lines'), which is outside this width. My own check at 160: widest line is 160 cells in all four screens (ledger 48 rows, questions 23, desk 33, desk-planask 34, all at most 48). The footer 'Up/Down j/k move ...' is the last line in each (ledger.txt:48). No SGR 5/6 and no mouse sequences."},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass. theme.py:80-89 maps the standard depth to bright_white, white, bright_black, bright_yellow, bright_cyan, green, red and magenta, eight distinct indexes. The ledger.16.ansi and desk.16.ansi files use six distinct codes (97, 37, 90, 93, 96, 32), with no two roles sharing one."},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass. theme.py:95-106 holds a non-empty STATE_ROLE and FROZEN_ROLE. In ledger.truecolor.ansi rows (e.g. w-005) 'running' and 'alive' are green (139,215,175). 'idle', 'blocked', 'active', 'none', 'wait' and 'review' are base. Every state word is printed in the plain pass."},
    "RB-11": {"result": "PASS", "evidence": "'unavailable (no source)' and 'unavailable' are muted at ledger.truecolor.ansi:3-4 and questions:3-4. 'unknown' is muted at questions:3. '  reason unknown' is muted at questions:11-15. 'unknown (absent in source)' is muted at desk:24. The nocolor files carry the same words as plain text."},
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
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi:12 and desk-planask:12 have the selected row '▸ 59m  Ship the change now?' in bold amber (250,178,25). Unselected rows get a base-bold subject (desk:11), so the glyph is backed by a role style. The questions screen shows no selected row and no ▸."}
  },
  "failing_high_medium": []
}
```
