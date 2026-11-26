"""Seven small run folders for the `ran` cross-check (REQ-28), built from F-REPORT-RL and F-TRANSCRIPT-RL. Invented.

    build(root) -> [run folder, ...]   root/<run>/reviews/<rid>.md and <rid>.attempt1.json; nothing else is needed.

run        reviewer  report (rows)                              transcript
ran-1      t2b-1     good_ember: C4.1 C4.2 C5.1 C6.1 C8.1       search_done: one Bash grep, result SEARCH_HIT
ran-2      t2b-1     none_found: C4.1 C5.1 C6.1 C8.1            none_found_with_search: one Bash git grep
ran-3      t4-1      none_found_with_rows: C4.1 C4.2 C5.1 C6.1 C8.1   none_found_without_search: no call
ran-4      t3-1      good_luna1: C1.1 C2.1 C3.1                 luna_array_results: codegraph_node and Bash ls
ran-5      t2b-1     C5.1 (grep, retention window), C8.1        a Grep call on "retention window"
ran-6      t2b-1     C4.1 (grep -c), C6.1 (grep -rn)            a Read call only
ran-7      t3-1      C2.1 (grep of the source)                  codegraph_node whose result is an array holding the quote

The expected `ran_status` of each row is worked out by hand in tests/test_ran_check.py.
"""

import json
from pathlib import Path

from fixtures.reports import make_rl_reports as rep
from fixtures.transcripts import make_transcripts as tr

# (run, reviewer, report case or None, transcript case or None)
FROM_CASES = (
    ("ran-1", "t2b-1", "good_ember", "search_done"),
    ("ran-2", "t2b-1", "none_found", "none_found_with_search"),
    ("ran-3", "t4-1", "none_found_with_rows", "none_found_without_search"),
    ("ran-4", "t3-1", "good_luna1", "luna_array_results"),
)


def _custom():
    """{run: (reviewer, report, transcript)} of runs 5 to 7."""
    q = rep.Q
    run5 = rep.standard(
        [
            rep.row("C5.1", ran="grep for retention window in the guide"),
            rep.row("C8.1", ran="NONE FOUND: no test mentions the hold flag"),
        ]
    )
    run6 = rep.standard(
        [
            rep.row("C4.1", ran="grep -c pattern plan.md: 0"),
            rep.row("C6.1", ran="grep -rn of both scopes, 3 hits"),
        ]
    )
    run7 = rep.standard(
        [
            rep.row(
                "C2.1",
                "PROBLEM",
                q["legal"],
                q["source_legal"],
                rep.PROBLEM,
                "grep of the source: 1 hit",
            )
        ]
    )
    return {
        "ran-5": (
            "t2b-1",
            run5,
            tr.run(
                tr.EMBER,
                [
                    (
                        "tool",
                        "Grep",
                        {"pattern": "retention window", "path": "docs"},
                        "docs/guide.md:3:Retention window",
                    )
                ],
            ),
        ),
        "ran-6": (
            "t2b-1",
            run6,
            tr.run(
                tr.EMBER,
                [("tool", "Read", {"file_path": "/tmp/x/plan.md"}, "the plan text")],
            ),
        ),
        "ran-7": (
            "t3-1",
            run7,
            tr.run(
                tr.LUNA,
                [
                    (
                        "tool",
                        "mcp__codegraph__codegraph_node",
                        {"file": "docs/source.md"},
                        [
                            {
                                "type": "text",
                                "text": f"docs/source.md:4: {q['source_legal']}",
                            }
                        ],
                    )
                ],
            ),
        ),
    }


def build(root):
    root = Path(root)
    runs = {
        run: (rid, rep.build(case).report, tr.build(tcase))
        for run, rid, case, tcase in FROM_CASES
    } | _custom()
    out = []
    for run, (rid, report, events) in sorted(runs.items()):
        d = root / run / "reviews"
        d.mkdir(parents=True)
        (d / f"{rid}.md").write_text(report, encoding="utf-8")
        (d / f"{rid}.attempt1.json").write_text(json.dumps(events), encoding="utf-8")
        out.append(root / run)
    return out
