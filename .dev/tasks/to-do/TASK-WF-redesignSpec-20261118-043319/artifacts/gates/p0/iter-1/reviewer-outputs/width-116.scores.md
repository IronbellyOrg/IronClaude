```json
{
  "width": 116,
  "iteration": 1,
  "rows": {
    "RB-01": {"result": "FAIL", "evidence": "No colour exists: desk.16.ansi, ledger.16.ansi and questions.16.ansi have no ESC bytes and the 256 and truecolor files are copies; the title line 'ORCA OBSERVER ...' (line 1) is not cyan bold; checks.json marks it na only because no truecolor stream exists"},
    "RB-02": {"result": "FAIL", "evidence": "desk.txt:14 'DECISION DESK' is a bare line and no titled border exists on any screen (mockup has '┏━ HUMAN QUESTION ━' and '╭─ SESSION REGISTER ─')"},
    "RB-03": {"result": "FAIL", "evidence": "desk.txt:14-28 is one stacked column at 116 (mockup: two columns 66+46); questions.txt has no strip or RETAIN CONTEXT pane (lines 5-18 are flat text)"},
    "RB-04": {"result": "FAIL", "evidence": "checks.json RB-04 is 'pass' and (c) holds at questions.txt:10 'seen, not resolved: 5 | closed by evidence: unavailable (no source)', but no strip frame and no 3-row block figure are drawn at 116, so (a) and (b) fail"},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 pass; questions.txt:8-9 gap notice and questions.txt:12 'reason unknown' present, desk.txt:17 retention line whole"},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass; desk.nocolor.txt is identical in size (1639) to desk.txt and has no ESC"},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass; desk.ascii.txt is pure ASCII (the '▸' at desk.txt:13 becomes ASCII in the ascii pass)"},
    "RB-08": {"result": "PASS", "evidence": "checks.json has no RB-08 failure at 116 (only ledger@80 fails); manifest.json widest_cell 116 and 42 lines (ledger) are within bounds; desk.txt:32-36 footer keys and 'shown 3/3' are the last lines"},
    "RB-09": {"result": "FAIL", "evidence": "No role colours are emitted at all (no SGR in any 16-colour file); theme.py does not exist per checks.json, so eight distinct ANSI colours cannot be read"},
    "RB-10": {"result": "FAIL", "evidence": "desk.txt:20-23 'dispatchStatus: active', 'liveness: alive (terminal)' carry no state role (no SGR), and the STATE_ROLE table and its test do not exist"},
    "RB-11": {"result": "FAIL", "evidence": "desk.txt:27 'resource.worktreeId: unknown (absent in source)' and questions.txt:12 'reason unknown' carry no muted role; the 16-colour files have no SGR"},
    "RB-12": {"result": "FAIL", "evidence": "ledger.txt:8-39 shows 32 visible rows with no column heading or rule (line 7 is only 'worker-reported, not questions')"},
    "RB-13": {"result": "FAIL", "evidence": "checks.json RB-13 desk@116 and desk-planask@116: 'key group not whole: n/p question'; desk.txt:32-33 splits 'n/p' and 'question'"},
    "RB-14": {"result": "FAIL", "evidence": "checks.json RB-14 desk@116 and desk-planask@116: 'field values start at 8 different offsets'; desk.txt:17-27 labels like 'dispatchId: w-002' are not aligned; no amber bold question text"},
    "RB-15": {"result": "FAIL", "evidence": "desk.txt:1 and ledger.txt:1 have no right-aligned READ ONLY badge (mockup: 'SYNTHETIC · READ ONLY')"},
    "RB-16": {"result": "FAIL", "evidence": "questions.txt:12-16 question rows carry no bold or body_bold role (no SGR); checks.json RB-16 is na for lack of role spans"},
    "RB-17": {"result": "PASS", "evidence": "checks.json RB-17 pass; no RETAIN CONTEXT frame is drawn, and 'retention reset at 12:00; ...' occurs once (questions.txt:17); the check is vacuous at baseline and RB-03 records the missing pane"},
    "RB-18": {"result": "FAIL", "evidence": "ledger.txt:1-42 is flat text with no titled panes (mockup has 'SESSION REGISTER' and 'OBSERVATION WINDOW' frames)"},
    "RB-19": {"result": "PASS", "evidence": "checks.json RB-19 pass; desk-planask.txt:17-18 shows the hash whole on one line of 116 cells or fewer; superseded by RB-27, which fails"},
    "RB-20": {"result": "FAIL", "evidence": "checks.json RB-20 desk@116, desk-planask@116 and ledger, questions @116: 'no rule line above the footer'; desk@116 and desk-planask@116 also 'n/p question split' (desk.txt:32-33)"},
    "RB-21": {"result": "PASS", "evidence": "checks.json RB-21 failures are only at 80; ledger.txt:3 counts line 'source counts: active 54 / reclaimable 0 / retained 13 / released 13' is whole at 116"},
    "RB-22": {"result": "FAIL", "evidence": "checks.json RB-22 ledger: '116 cols: blank run 48 > N=18'; ledger.txt:8 'none               w-001' then a long blank run before 'alive'"},
    "RB-23": {"result": "FAIL", "evidence": "desk.txt:13 '▸ 59m  Ship the change now?' marks the selection by the glyph only; the 16-colour file has no role style"},
    "RB-24": {"result": "FAIL", "evidence": "desk.txt:13 and desk.txt:16 both print 'Ship the change now?'; desk.txt:12-13 and 15 print the age '59m' twice"},
    "RB-25": {"result": "FAIL", "evidence": "questions.txt:12-16 every row ends 'reason unknown' when no reason is given; no 'reasons: none in source' title"},
    "RB-26": {"result": "FAIL", "evidence": "desk.txt:20-22 'dispatchStatus: active', 'terminalState: active', 'outcome: none' are three separate raw rows with no ACTIVE badge"},
    "RB-27": {"result": "FAIL", "evidence": "checks.json RB-27 desk-planask@116: 'hex run shown'; desk-planask.txt:18 '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef)?'"},
    "RB-28": {"result": "FAIL", "evidence": "ledger.txt:40 '32/54 shown  +22 more' sits above ledger.txt:42 'shown 32/54 | ...'; liveness is the word 'alive' (ledger.txt:8), not a dot with a legend"},
    "RB-29": {"result": "FAIL", "evidence": "desk.txt:15 'msg_000000000001  age 59m' shows an internal msg_ id and desk.txt:17-27 uses raw field names ('dispatchId:', 'workerState:', 'nextAction.kind:') with unaligned values"}
  },
  "failing_high_medium": ["RB-01", "RB-02", "RB-03", "RB-04", "RB-09", "RB-10", "RB-11", "RB-12", "RB-13", "RB-14", "RB-15", "RB-16", "RB-18", "RB-24", "RB-25", "RB-26", "RB-27", "RB-28", "RB-29"]
}
```
