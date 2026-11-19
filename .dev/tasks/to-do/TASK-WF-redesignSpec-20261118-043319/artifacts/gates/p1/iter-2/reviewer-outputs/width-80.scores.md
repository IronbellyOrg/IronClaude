```json
{
  "width": 80,
  "iteration": 2,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "truecolor census of all four screens is only the eight palette triples; cyan bold title (desk.truecolor.ansi:1); amber bold ages and desk question text (desk-planask.truecolor.ansi:15-19); base bold subjects (questions.truecolor.ansi:12-16); selected row all amber bold (desk.truecolor.ansi:13); header2, keys and footer muted (desk.truecolor.ansi:2,33-35); slate pane title (desk.truecolor.ansi:29); ledger cells base (ledger.truecolor.ansi:9-39); (e) not applicable"},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 all pass; gap notice ledger.txt:6 'Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"'; the 'runs seen>' cut at ledger.txt:5 is the strip cut that RB-21 scores at P2, and the counts tokens before it are whole"},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass; grep -c ESC on the four nocolor.txt files returns 0 each"},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 pass; the four ascii.txt files have zero non-ASCII bytes and zero ESC bytes"},
    "RB-08": {"result": "FAIL", "evidence": "checks.json RB-08 ledger@80: 'footer keys are not among the last lines'; ledger.txt:41 keys line is cut 'm mark  e exp>' (q quit lost) and the last line 42 is 'shown 31/54 | collected 80 / reported 80'"},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass; desk.16.ansi gives distinct codes: base 97, muted 37, slate 90, amber 93, cyan 96, green 32 (red and violet are not drawn in these screens)"},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass; desk.truecolor.ansi:23 'liveness: alive (terminal)' green, :18 workerState 'idle' and :19-20 dispatchStatus/terminalState 'active' base, :22 nextAction.kind 'wait' base; all words printed in desk.txt"},
    "RB-11": {"result": "FAIL", "evidence": "questions.truecolor.ansi:10 and desk.truecolor.ansi:10 'seen, not resolved: 5 | closed by evidence: unavailable (no source)' is one base-colour span, so the absent value is not muted (muted elsewhere, e.g. line 4 and desk line 25)"},
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi:13 '▸ 59m  Ship the change now?' is bold amber (selected role) while the unselected row on line 12 is amber age plus base-bold subject; the questions screen has no selected row"}
  },
  "failing_high_medium": ["RB-08", "RB-11"]
}
```

Every other row (RB-02, RB-03, RB-04 and RB-12 to RB-22 and RB-24 to RB-29) is `N/A (scheduled P<n>)` and was not scored.
