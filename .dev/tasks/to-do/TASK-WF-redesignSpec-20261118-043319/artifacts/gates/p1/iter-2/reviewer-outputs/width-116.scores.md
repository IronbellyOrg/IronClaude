```json
{
  "width": 116,
  "iteration": 2,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "checks.json RB-01 pass. Every SGR foreground in the four 116 truecolor files is one of the eight palette triples. Line 1 is bold cyan 112,205,226. desk.truecolor.ansi line 13 has the age '59m' in the bold amber selected line, and line 12 has '1h' bold amber then 'Which branch should the worker rebase on?' bold base. Desk lines 14-16 are bold amber. Line 2 and the keys and footer lines are muted 165,182,194. Ledger cells are base. (e) treated as not applicable."},
    "RB-02": {"result": "N/A", "evidence": "N/A (scheduled P3)"},
    "RB-03": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-04": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 pass. Literals present whole: desk.txt:14 'DECISION DESK', :25 'nextAction.kind: wait', :26 'resource.worktreeId: unknown (absent in source)', :12 'reason unknown', :29 'retention reset at 12:00; questions observed before this start are not retained'."},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass. I counted 0 ESC bytes in each of the four .nocolor.txt files. Each .nocolor.txt equals its .truecolor.ansi with SGR stripped (diff clean)."},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass. I found 0 non-ASCII bytes in each .ascii.txt and .ascii.ansi. The selection marker becomes '@' (desk.ascii.txt:13). The only '?' characters are the question marks inside question text (desk.ascii.txt:16, desk-planask.ascii.txt:18); no border exists yet."},
    "RB-08": {"result": "PASS", "evidence": "At 116 the only failing case in checks.json RB-08 is ledger@80, so no 116 case fails. I measured the widest line at 116 cells (manifest widest_cell, desk-planask line 13; the 118 from awk counted bytes, since the marker is 3 bytes). Ledger is 42 rows, which does not exceed height 42. I found no SGR 5/6 and no mouse sequences."},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass. The 16-colour files use 97, 37, 90, 93, 96 and 32. theme.py 'standard' table: base bright_white, muted white, slate bright_black, amber bright_yellow, cyan bright_cyan, green green, red red, violet magenta. All eight are distinct."},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass. 'alive' is green 139,215,175 in ledger.truecolor.ansi rows and in desk.txt:25 'liveness: alive (terminal)'. Not in the table, so body base: 'workerState: idle', 'dispatchStatus: active', 'terminalState: active', 'outcome: none', 'nextAction.kind: wait'. The words are printed in every case. STATE_ROLE in theme.py holds the required keys, and the four state roles map to green, cyan, red and violet, which are distinct at the standard depth."},
    "RB-11": {"result": "PASS", "evidence": "'unavailable (no source)' (questions.truecolor.ansi lines 3-4), 'unknown' (line 3), 'reason unknown' (lines 12-16) and desk 'resource.worktreeId: unknown (absent in source)' are all muted 165,182,194. The text is the same in the NO_COLOR pass."},
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
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi line 13: the selected row '▸ 59m  Ship the change now?' is one bold amber 250,178,25 span, in addition to the '▸' glyph. The unselected row on line 12 is not."},
    "RB-24": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-25": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-26": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-27": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-28": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-29": {"result": "N/A", "evidence": "N/A (scheduled P2)"}
  },
  "failing_high_medium": []
}
```
