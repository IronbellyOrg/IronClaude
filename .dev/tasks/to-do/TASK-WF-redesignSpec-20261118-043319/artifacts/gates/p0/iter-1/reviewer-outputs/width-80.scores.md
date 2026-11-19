```json
{
  "width": 80,
  "iteration": 1,
  "rows": {
    "RB-01": {"result": "FAIL", "evidence": "checks.json marks it na (no truecolour stream). Reviewer read of the colour pass: ledger.16.ansi, desk.16.ansi and questions.16.ansi contain no SGR escapes at all, so the header1 title is not cyan or bold and no role colours exist. The truecolour file is byte-identical to the 16-colour file."},
    "RB-02": {"result": "FAIL", "evidence": "desk.txt:10-30 and questions.txt:9-20 have no titled borders. 'DECISION DESK' (desk.txt:14) and 'COORDINATOR QUESTIONS' (questions.txt:5) are plain text lines. The mockup has heavy and rounded frames."},
    "RB-03": {"result": "FAIL", "evidence": "At 80 the desk should be three stacked 78-wide framed panes. desk.txt:10-38 is an unframed run of lines, and the question list is above 'DECISION DESK' with no pane structure. Mockup decision-desk.txt has three framed panes."},
    "RB-04": {"result": "PASS", "evidence": "checks.json RB-04 pass. questions.txt:11 reads 'seen, not resolved: 5 | closed by evidence: unavailable (no source)' whole on one line. No strip frame at 80."},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 pass. Literals are present, e.g. 'reason unknown' (desk.txt:18), 'retention reset at 12:00; questions observed before this start are not retained' (questions.txt:18), 'DECISION DESK' (desk.txt:14)."},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass. desk.nocolor.txt is byte-size equal to desk.txt (1532) with no ESC bytes; the .16.ansi files contain no escapes either."},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass. desk.ascii.txt shows the selection glyph as '>' instead of the Unicode marker (1530 bytes vs 1532)."},
    "RB-08": {"result": "FAIL", "evidence": "checks.json: 'ledger@80: footer keys are not among the last lines'. ledger.txt:40 holds the keys line cut as 'm mark rows  e exp>', and it is followed by the 'shown 31/54' line at ledger.txt:41."},
    "RB-09": {"result": "FAIL", "evidence": "checks.json marks it na (theme.py not built). Reviewer read of the colour pass: the 16-colour files contain zero SGR codes, so the eight roles do not map to eight distinct ANSI colours."},
    "RB-10": {"result": "FAIL", "evidence": "checks.json marks it na (theme.py not built). desk.16.ansi has no SGR, so 'workerState: idle', 'dispatchStatus: active' and 'liveness: alive (terminal)' carry no state role."},
    "RB-11": {"result": "FAIL", "evidence": "'unknown (absent in source)' (desk.txt:27) and 'unavailable (no source)' (desk.txt:4) carry no muted role in the .ansi, because there is no SGR in the file."},
    "RB-12": {"result": "FAIL", "evidence": "ledger.txt:9-39 shows rows ('none           w-001   10s') with no column heading or rule line above them. The mockup has a header row."},
    "RB-13": {"result": "FAIL", "evidence": "checks.json: 'key group not whole: m mark rows' (desk, questions) and 'e export', 'q quit' (ledger@80). desk.txt:34-35 splits 'm' from 'mark rows' across lines."},
    "RB-14": {"result": "FAIL", "evidence": "checks.json: 'field values start at 8 different offsets' for desk@80 and desk-planask@80. desk.txt:20-27 shows 'dispatchId: w-002' and 'nextAction.kind: wait' with unaligned values."},
    "RB-15": {"result": "FAIL", "evidence": "ledger.txt:1, desk.txt:1 and questions.txt:1 read 'ORCA OBSERVER  mode=live ...' with no right-aligned 'READ ONLY' badge. The mockup has 'SYNTHETIC · READ ONLY'."},
    "RB-16": {"result": "FAIL", "evidence": "checks.json marks it na (needs role spans). questions.txt:12-16 rows carry no bold or body_bold in the .ansi because there is no SGR at all, so row lines do not have strictly more bold characters than caveat lines (0 vs 0)."},
    "RB-17": {"result": "PASS", "evidence": "checks.json RB-17 pass. No RETAIN CONTEXT frame at 80, and 'retention reset at 12:00; ...' occurs once (questions.txt:18)."},
    "RB-18": {"result": "FAIL", "evidence": "ledger.txt:1-41 is plain unframed lines with no titled panes. 'worker-reported, not questions' (ledger.txt:8) is a bare line."},
    "RB-19": {"result": "PASS", "evidence": "checks.json RB-19 pass. desk-planask.txt:18 holds the 64-hex hash whole on one line, 66 cells with ')?'. The rubric says RB-27 replaces this row, and RB-27 fails."},
    "RB-20": {"result": "FAIL", "evidence": "checks.json: 'no rule line above the footer' for ledger, desk, questions and desk-planask @80. ledger.txt:40-41 has no rule before the keys."},
    "RB-21": {"result": "FAIL", "evidence": "checks.json: 'cut inside a token'. ledger.txt:5 ends 'runs seen>' and desk.txt:4 ends 'cost un>'."},
    "RB-22": {"result": "FAIL", "evidence": "checks.json: '80 cols: blank run 34 > N=18'. ledger.txt:10 has a long blank run between 'none' and 'w-001'."},
    "RB-23": {"result": "FAIL", "evidence": "desk.txt:17 shows the selected row only by a leading glyph. There is no SGR, so the selected row has no role style."},
    "RB-24": {"result": "FAIL", "evidence": "desk.txt:17 'Ship the change now?' and desk.txt:16 repeat the question text in the list and again at desk.txt:16-17. The run id is repeated at desk.txt:2 and desk.txt:6."},
    "RB-25": {"result": "FAIL", "evidence": "desk.txt:16-17 and questions.txt:12-16 end every question row with 'reason unknown'. The suffix is not suppressed and there is no 'reasons: none in source' in the title."},
    "RB-26": {"result": "FAIL", "evidence": "desk.txt:21-23 shows 'dispatchStatus: active', 'terminalState: active', 'outcome: none' as three raw rows. There is no single ACTIVE badge."},
    "RB-27": {"result": "FAIL", "evidence": "checks.json: 'desk-planask@80: hex run shown: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef)?'. This is a 64-hex run at desk-planask.txt:18."},
    "RB-28": {"result": "FAIL", "evidence": "ledger.txt:40 '31/54 shown  +23 more' sits above ledger.txt:42 'shown 31/54 | collected 80 / reported 80'. This is a '+N more' row above a 'shown n/N' footer, and there is no liveness dot legend."},
    "RB-29": {"result": "FAIL", "evidence": "desk.txt:20-27 uses raw field names ('dispatchId:', 'workerState:', 'nextAction.kind:', 'resource.worktreeId:') and the internal id 'msg_000000000001' (desk.txt:15). Labels are not plain words in an aligned column."}
  },
  "failing_high_medium": ["RB-01", "RB-02", "RB-03", "RB-08", "RB-09", "RB-10", "RB-11", "RB-12", "RB-13", "RB-14", "RB-15", "RB-16", "RB-18", "RB-24", "RB-25", "RB-26", "RB-27", "RB-28", "RB-29"]
}
```
