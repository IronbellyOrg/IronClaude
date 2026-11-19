```json
{
  "width": 160,
  "iteration": 1,
  "rows": {
    "RB-01": {"result": "FAIL", "evidence": "checks.json is N/A (no truecolor stream), but desk.16.ansi, ledger.16.ansi and questions.16.ansi contain no SGR sequences at all; title line 1 'ORCA OBSERVER' is not cyan or bold, ages are not amber, header2/footer are not muted"},
    "RB-02": {"result": "FAIL", "evidence": "questions.txt and desk.txt have no titled border; 'COORDINATOR QUESTIONS' (questions.txt:5) and 'DECISION DESK' (desk.txt:13) are plain lines, while attention-ledger.txt:7 has '┏━ OPEN HUMAN QUESTIONS ━┓' and '╭─ RETAIN CONTEXT'"},
    "RB-03": {"result": "FAIL", "evidence": "desk.txt is one column (list at line 11-12, DECISION DESK at 13, evidence at 16-25); the mockup has two columns at 160, and questions.txt has no strip, list pane or RETAIN CONTEXT pane"},
    "RB-04": {"result": "FAIL", "evidence": "checks.json passes (c) only; at 160 there is no cyan count-strip frame and no 3-row block figure; questions.txt:9 has only the plain 'seen, not resolved: 5 | closed by evidence: unavailable (no source)'"},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 all pass; e.g. questions.txt:16 'retention reset at 12:00...', desk.txt:13 'DECISION DESK', ledger.txt:5 'source UNVERIFIED'"},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 all pass; the .nocolor.txt files are byte-identical in size to the .txt files and the .ansi files carry no ESC colour codes"},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 all pass; ledger.ascii.txt is pure ASCII (no frames exist yet, so no '?' where a border should be)"},
    "RB-08": {"result": "PASS", "evidence": "checks.json RB-08 has a failure only for ledger@80; no 160 entry; ledger.txt is 48 lines with the keys line last (ledger.txt:48), widest cell 160 per manifest.json"},
    "RB-09": {"result": "FAIL", "evidence": "checks.json N/A (theme.py not built), but desk.16.ansi, ledger.16.ansi and questions.16.ansi contain no SGR codes, so the eight roles do not map to eight distinct ANSI colours"},
    "RB-10": {"result": "FAIL", "evidence": "checks.json N/A (theme.py not built); state words 'running', 'blocked', 'alive (terminal)' (ledger.txt:12-14) carry no role colour in ledger.16.ansi (no SGR present)"},
    "RB-11": {"result": "FAIL", "evidence": "'reason unknown' (questions.txt:11) and 'unknown (absent in source)' (desk.txt:24) carry no muted colour; no SGR in the .ansi files"},
    "RB-12": {"result": "PASS", "evidence": "ledger.txt:8-9 column heading and rule are present with rows visible (the rubric requirement is for 116 and 80; it holds at 160)"},
    "RB-13": {"result": "PASS", "evidence": "checks.json RB-13 has no entry for 160; desk.txt:33 keys line is whole, including 'n/p question'"},
    "RB-14": {"result": "FAIL", "evidence": "checks.json RB-14 desk@160 and desk-planask@160: 'field values start at 8 different offsets'; desk.txt:14-24 labels have no common value column, and question text does not lead (line 14 is 'msg_... age 59m')"},
    "RB-15": {"result": "FAIL", "evidence": "line 1 of all four screens ('ORCA OBSERVER  mode=live ...') has no right-aligned 'READ ONLY' badge; the mockup has 'SYNTHETIC · READ ONLY' at the right of its title line"},
    "RB-16": {"result": "FAIL", "evidence": "checks.json N/A (needs role spans), but questions.16.ansi has no bold or colour on question rows (lines 11-15), and the caveat lines 6-8 sit inside the list area rather than in a RETAIN CONTEXT pane"},
    "RB-17": {"result": "PASS", "evidence": "checks.json RB-17 all pass (script, string census); no RETAIN CONTEXT frame exists and 'retention reset' (questions.txt:16), 'bounded best effort' (:8) and 'one Run only' (:6) each occur once. The pass is vacuous, because the pane does not exist yet"},
    "RB-18": {"result": "FAIL", "evidence": "ledger.txt:1-7 are unframed plain lines; there are no titled panes for observation and attention content"},
    "RB-19": {"result": "PASS", "evidence": "checks.json RB-19 all pass; desk-planask.txt:16 shows the 64-hex hash whole on one line. RB-27 replaces this row and fails"},
    "RB-20": {"result": "FAIL", "evidence": "checks.json RB-20 fails at 160 for desk, desk-planask, ledger and questions: 'no rule line above the footer' (e.g. ledger.txt:47-48, '37/54 shown  +17 more' then keys)"},
    "RB-21": {"result": "PASS", "evidence": "checks.json RB-21 has failures only at 80; at 160 ledger.txt:48 key and count lines are whole"},
    "RB-22": {"result": "PASS", "evidence": "checks.json RB-22 fails only at 116 (48 > N=18) and 80 (34 > N=18); 160 is the reference measure N=18"},
    "RB-23": {"result": "FAIL", "evidence": "desk.txt:12 '▸ 59m  Ship the change now?' marks the selected row with a glyph only; desk.16.ansi has no role style (no SGR)"},
    "RB-24": {"result": "FAIL", "evidence": "desk.txt: 'Ship the change now?' occurs at line 12 and again at line 15; 'run_14cfcbd8edf2' occurs at lines 2 and 6; there is no script result in checks.json"},
    "RB-25": {"result": "FAIL", "evidence": "questions.txt:11-15 and desk.txt:11-12 each end with 'reason unknown', and no title line carries 'reasons: none in source'"},
    "RB-26": {"result": "FAIL", "evidence": "desk.txt:17-19 show three separate raw rows 'dispatchStatus: active / terminalState: active / outcome: none' instead of one ACTIVE badge"},
    "RB-27": {"result": "FAIL", "evidence": "checks.json desk-planask@160: hex run shown; desk-planask.txt:16 '(plan hash 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef)'"},
    "RB-28": {"result": "FAIL", "evidence": "ledger.txt:8 has a 'flags' column, :9 is a rule row, :47 '37/54 shown  +17 more' sits above footer 'shown 37/54', and liveness is the text 'alive (terminal)' rather than a dot with a legend"},
    "RB-29": {"result": "FAIL", "evidence": "desk.txt:14 'msg_000000000001  age 59m' shows an internal msg_ id, and desk.txt:16-24 use raw field names ('dispatchId:', 'workerState:', 'nextAction.kind:', 'resource.worktreeId:') in an unaligned layout"}
  },
  "failing_high_medium": ["RB-01", "RB-02", "RB-03", "RB-04", "RB-09", "RB-10", "RB-11", "RB-14", "RB-15", "RB-16", "RB-18", "RB-24", "RB-25", "RB-26", "RB-27", "RB-28", "RB-29"]
}
```
