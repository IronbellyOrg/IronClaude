```json
{
  "width": 116,
  "iteration": 3,
  "rows": {
    "RB-01": {"result": "PASS", "evidence": "checks.json pass; I decoded all four truecolor files: every fg triple is one of the eight palette colours, no uncoloured visible text. ledger.truecolor.ansi:1 title is 1;38;2;112;205;226 (cyan bold); line 2 muted; footer and keys muted; questions.truecolor.ansi:12 age '1;..250;178;25 1h' amber bold with subject '1;..225;233;238' base bold; desk.truecolor.ansi:15-16 'msg_000000000001  age 59m' and 'Ship the change now?' amber bold; ledger 'none'/'w-001' cells base. (e) not applicable."},
    "RB-05": {"result": "PASS", "evidence": "checks.json pass; verified desk.txt:14 'DECISION DESK', desk.txt:25 'unknown (absent in source)', desk.txt:27 'retention reset at 12:00; questions observed before this start are not retained', desk.txt:22 'nextAction.kind: wait' and questions.txt:12 'reason unknown' present and uncut."},
    "RB-06": {"result": "PASS", "evidence": "checks.json pass; ledger, questions, desk and desk-planask .nocolor.txt contain zero ESC bytes and are byte-identical to the SGR-stripped truecolor text and to the plain .txt."},
    "RB-07": {"result": "PASS", "evidence": "checks.json pass; .ascii.txt and .ascii.ansi for all four screens are pure ASCII (all bytes < 128); the only '?' characters are question text, e.g. desk.ascii.txt 'Ship the change now?'."},
    "RB-08": {"result": "PASS", "evidence": "checks.json has no 116 entry for RB-08 (its only fail is ledger@80); I measured max line width 107/113/113/116 (ledger/questions/desk/desk-planask) <= 116 and 43/24/35/37 rows (<= 42 once the trailing empty split element is dropped); no SGR 5 or 6 and no mouse sequences; ledger.txt:40-42 keys line then 'shown 32/54 | collected 80 / reported 80' are last."},
    "RB-09": {"result": "PASS", "evidence": "checks.json pass; theme.py:80-89 maps the eight roles to bright_white, white, bright_black, bright_yellow, bright_cyan, green, red, magenta (all distinct); desk.16.ansi shows 1;97 base, 37 muted, 90 slate, 1;93 amber, 1;96 cyan, 32 green with no two roles sharing a code."},
    "RB-10": {"result": "PASS", "evidence": "checks.json pass; ledger.truecolor.ansi:11 and desk.truecolor.ansi:23 'alive' carry green 139;215;175 (state_running); desk.txt:18-22 'idle', 'active', 'none', 'wait' are base 225;233;238; test_theme.py:63-64 asserts the required keys and FROZEN_ROLE == 'state_frozen'; the four state roles are green, cyan, red and magenta, which are distinct."},
    "RB-11": {"result": "PASS", "evidence": "I scanned every span containing 'unknown', 'unavailable' or 'absent' in the four truecolor files and none is outside the muted role, e.g. ledger.truecolor.ansi:4 'unavailable (no source)' and 'unavailable' are 165;182;194, desk.truecolor.ansi:25 'unknown (absent in source)' is muted, questions.truecolor.ansi:12 '  reason unknown' is muted; the words stay in the nocolor text."},
    "RB-23": {"result": "PASS", "evidence": "desk.truecolor.ansi:13 selected row '1;38;2;250;178;25m▸ 59m  Ship the change now?' is bold amber (the selected role), while the unselected row 12 uses amber age plus base bold subject; desk-planask.truecolor.ansi:13 is the same."},
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
  "failing_high_medium": []
}
```
