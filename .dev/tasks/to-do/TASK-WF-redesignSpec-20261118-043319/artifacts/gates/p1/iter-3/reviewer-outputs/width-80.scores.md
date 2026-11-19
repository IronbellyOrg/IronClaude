```json
{
  "width": 80,
  "iteration": 3,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "All fg triples are in the palette (decoded ledger/questions/desk/desk-planask truecolor.ansi); questions.truecolor.ansi:1 cyan+bold title; :12-16 age amber+bold, subject base+bold; desk-planask.truecolor.ansi:16-19 question text amber+bold; :2,:22,:24 muted; (e) treated as not applicable. Caveat: questions.truecolor.ansi:4 'cost un>' is a base-coloured cut fragment (the cut itself is RB-21, scheduled P2)."},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 pass; verified questions.txt:10 'seen, not resolved: 5 | closed by evidence: unavailable (no source)' whole and desk-planask.txt:25 'nextAction.kind: wait' verbatim. Caveat: counts strip cut at ledger.txt:5 'runs seen>' and questions.txt:4 'cost un>' (RB-21, scheduled P2)."},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass; 0 ESC bytes in all four *.nocolor.txt, and each truecolor.ansi with SGR removed equals its .nocolor.txt and .txt byte for byte (ledger, questions, desk, desk-planask)."},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass; 0 non-ASCII bytes in all four *.ascii.txt and *.ascii.ansi (the '▸' marker in desk.txt:13 is replaced); no frames exist at this phase."},
    "RB-08": {"result": "FAIL", "evidence": "checks.json RB-08 ledger@80 'footer keys are not among the last lines'; ledger.txt:41 keys line is cut 'm mark  e exp>' (no 'e export all  q quit') and ledger.txt:42 'shown 31/54 | collected 80 / reported 80' is the last line. Width, blink and mouse checks are clean on all screens."},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass; desk-planask.16.ansi and questions.16.ansi map cyan=96, amber=93, base=97, muted=37, slate=90, green=32 to distinct codes (red and violet are not shown in these fixtures)."},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass; theme.py:95-106 STATE_ROLE holds the five required keys and FROZEN_ROLE='state_frozen'; desk.truecolor.ansi:23 'liveness:[green] alive (terminal)' carries the state role, while 'workerState: idle' and 'dispatchStatus: active' (desk-planask :21-22) are base; all words are in the plain pass."},
    "RB-11": {"result": "PASS", "evidence": "questions.truecolor.ansi:3-4,10 'unknown' and 'unavailable (no source)' muted; :12 'reason unknown' muted; desk.truecolor.ansi:25 'unknown (absent in source)' muted; the nocolor files are plain."},
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi:13 selected row '▸ 59m  Ship the change now?' is wholly amber+bold, against :12 unselected subject base+bold; desk-planask.16.ansi:13 keeps 1;93 on the selected row."},
    "RB-02": {"result": "N/A", "evidence": "N/A (scheduled P3)"},
    "RB-03": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
    "RB-04": {"result": "N/A", "evidence": "N/A (scheduled P4)"},
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
    "RB-24": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-25": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-26": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-27": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-28": {"result": "N/A", "evidence": "N/A (scheduled P2)"},
    "RB-29": {"result": "N/A", "evidence": "N/A (scheduled P2)"}
  },
  "failing_high_medium": ["RB-08"]
}
```
