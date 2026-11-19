```json
{
  "width": 160,
  "iteration": 1,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "checks.json RB-01 pass. I read all four .truecolor.ansi files: only palette triples appear and no blink. Title is bold cyan (desk.truecolor.ansi:1). List ages are bold amber with bold base subjects (questions.truecolor.ansi:11 `1;250;178;25m1h` + `1;225;233;238m  synthetic question 0`). The selected row is the bold amber `selected` role, which is exempt. Desk question text and age lines are bold amber (desk-planask lines 14-16). Freshness line, keys hint and footer are muted (ledger.truecolor.ansi:2 and last line). Ledger cells are base. (e) is not applicable."},
    "RB-05": {"result": "PASS", "evidence": "checks.json RB-05 status pass for all cases. Literals are visible whole in desk.nocolor.txt: `closed by evidence: unavailable (no source)`, `reason unknown`, `DECISION DESK`, `retention reset at 12:00; ...`, `nextAction.kind: wait`."},
    "RB-06": {"result": "PASS", "evidence": "checks.json RB-06 pass. I read desk.nocolor.txt and it is plain text with the same content as desk.txt and hierarchy carried by text and glyphs (`▸ 59m  Ship the change now?`)."},
    "RB-07": {"result": "PASS", "evidence": "checks.json RB-07 status pass for all cases; no 160-wide failure is recorded."},
    "RB-08": {"result": "PASS", "evidence": "checks.json RB-08 has one failing case, ledger@80 (`footer keys are not among the last lines`). No case is recorded for width 160; desk.txt:last line is the keys/footer line (`Up/Down j/k move workers ... shown 3/3 | collected 3 / reported 3`) and no SGR 5/6 appears in the census."},
    "RB-09": {"result": "PASS", "evidence": "checks.json RB-09 pass. The 16-colour SGR codes are distinct per role: base 97, muted 37, slate 90, amber 93, cyan 96, green 32 (desk-planask.16.ansi:1-3, 5, 12, 29-31). Red and violet do not appear in these screens, so their mapping rests on the script's theme-table check."},
    "RB-10": {"result": "PASS", "evidence": "checks.json RB-10 pass. Spot check: `running` and `alive` are green (desk.truecolor.ansi ledger rows `139;215;175mrunning`), while `idle`, `active`, `none` and `wait` are base and printed in the plain pass (desk.txt:`workerState: idle`)."},
    "RB-11": {"result": "FAIL", "evidence": "Absent values are shown in base colour, not muted. Counter-example: `source counts: unknown` is `38;2;225;233;238m` on line 3 of desk.truecolor.ansi and questions.truecolor.ansi. `cost unavailable` is base on line 4 (desk.truecolor.ansi:4; ledger.truecolor.ansi:4). The other absent values are muted (`reason unknown`, `unavailable (no source)`, `unknown (absent in source)`)."},
    "RB-23": {"result": "PASS", "evidence": "The selected question has the bold amber `selected` role on the whole line plus the marker. desk-planask.16.ansi:12 is `1;93m▸ 59m  Approve the plan...`; desk.truecolor.ansi:12 is `1;38;2;250;178;25m▸ 59m  Ship the change now?  reason unknown`. Other rows are bold base."},
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
  "failing_high_medium": ["RB-11"]
}
```
