"""Synthetic merged reports, run folders and judge folders for test_anon.py and test_judge.py. Everything is invented here;
no ground-truth file and no real score file is read or written (the GT and score files below are made up in tmp_path)."""

import json
import os
import time
from pathlib import Path

from helpers import REPO

RIDS = ("t2b-1", "t3-1", "t4-1")
SHA = "ab" * 32
# The judge worker of the earlier study (JJ): its BRIEF is lines 12 to 23. Read as a script text; it is not run.
JJ = (
    REPO
    / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/judge-one.sh"
)


def jj_brief():
    """Lines 12 to 23 of JJ, the BRIEF text, joined with newlines."""
    return "\n".join(JJ.read_text(encoding="utf-8").splitlines()[11:23])


def brief_of(script):
    """The BRIEF assignment of a script: from the line that starts `BRIEF="` through the line that ends `say why."`."""
    lines = Path(script).read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith('BRIEF="'))
    end = next(i for i in range(start, len(lines)) if lines[i].endswith('say why."'))
    return "\n".join(lines[start : end + 1])


# (lid, status, blocking): 4 ledger rows, 1 of them blocking
ROWS = (
    ("L1", "open", "yes"),
    ("L2", "open", "no"),
    ("L3", "open", "no"),
    ("L4", "open", "no"),
)


def merged_report(run, sb, doc="p1", rids=RIDS, rows=ROWS):
    """A merged report in the shape of ledger.render_merged_report, with invented findings."""
    out = [
        "review: 1 of 3",
        f"# Merged review 1 (coordinator script; panel of {len(rids)} reviewers)",
        f"candidate: {sb}/cand/{doc}/candidate.md sha256 {SHA}",
        "reviewers:",
    ]
    out += [f"- {r}: report {run}/normalised/{r}.md, block ok true" for r in rids]
    out += [
        "",
        "## Ledger",
        "",
        "| lid | status | blocking | confidence | severity | refs | reviewers |",
        "|---|---|---|---|---|---|---|",
    ]
    out += [
        f"| {lid} | {st} | {bl} | medium | MAJOR | - | {rids[0]}, {rids[1]} |"
        for lid, st, bl in rows
    ]
    out += ["", "## Blocking findings", ""]
    for lid, _, bl in rows:
        if bl == "yes":
            out += [
                f"### {lid}",
                "",
                f"#### {lid}.{rids[0]} (F1)",
                "",
                "- claim: The step names a file that the report cannot reach.",
                '- anchor: "the stated text of the first acceptance criterion"',
                "",
            ]
    out += ["## Other findings", ""]
    out += [
        f"- {lid} (MINOR, open, low): The wording leaves one reading open."
        for lid, _, bl in rows
        if bl != "yes"
    ]
    out += ["", "verdict: FAIL", ""]
    return "\n".join(out)


def make_run(runs, name, sb, doc="p1", **kw):
    """RUNS/<name>/{run.json, merged/merged-1.md}; returns the run folder."""
    run = Path(runs) / name
    (run / "merged").mkdir(parents=True)
    (run / "run.json").write_text(json.dumps({"doc": doc, "arm": "SS"}))
    (run / "merged" / "merged-1.md").write_text(merged_report(run, sb, doc, **kw))
    return run


def make_inputs(root, docs=("p1",)):
    """Candidates under root/sb/cand and invented ground-truth files under root/gt; returns (cand_root, gt_dir)."""
    cand, gt = Path(root) / "sb" / "cand", Path(root) / "gt"
    gt.mkdir(parents=True, exist_ok=True)
    for d in docs:
        (cand / d).mkdir(parents=True, exist_ok=True)
        (cand / d / "candidate.md").write_text("# An invented plan\n\nTask 1: do it.\n")
        items = [{"id": "GT1", "class": "C4", "blocking_in_implement": True}]
        (gt / f"{d}.json").write_text(json.dumps({"items": items}))
    return cand, gt


def judge_json(kind="ok"):
    """The JSON array a `claude -p --output-format json` call prints (the shape of tests/fakes/claude)."""
    err = kind == "api_error"
    text = "API Error: 529 overloaded_error" if err else "score.json written, 2, 0"
    return json.dumps(
        [
            {"type": "system", "subtype": "init", "session_id": "s"},
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": text}]},
            },
            {"type": "result", "is_error": err, "result": text, "session_id": "s"},
        ]
    )


def make_judge_dir(
    root, name, *, judge="ok", score=None, rows=ROWS, err="", started_age=None
):
    """A judge folder: merged-anon.md, judge.json (kind `judge`, or None for none, or a string for raw text),
    judge.err, an optional score.json (a dict) and a judge.started marker `started_age` seconds before the score."""
    d = Path(root) / name
    d.mkdir(parents=True)
    (d / "merged-anon.md").write_text(merged_report("<RUN>", "<SB>", rows=rows))
    if judge in ("ok", "api_error"):
        (d / "judge.json").write_text(judge_json(judge))
    elif judge is not None:
        (d / "judge.json").write_text(judge)
    (d / "judge.err").write_text(err)
    if score is not None:
        (d / "score.json").write_text(json.dumps(score))
    if started_age is not None:
        now = time.time()
        (d / "judge.started").write_text("")
        os.utime(d / "judge.started", (now, now))
        if score is not None:
            os.utime(d / "score.json", (now - started_age, now - started_age))
    return d


def score_for(rows=ROWS, **kw):
    """A score.json whose row counts match `rows` (a judge that read the report right)."""
    s = {
        "label": "x",
        "combo": "blind",
        "package": "p1",
        "gt_total": 1,
        "gt_covered_any": ["GT1"],
        "gt_covered_blocking": [],
        "ledger_rows_total": len(rows),
        "ledger_rows_blocking": sum(r[2] == "yes" for r in rows),
        "blocking_rows_gt_matched": 0,
        "wrong_blockers": 1,
        "notes": "invented",
    }
    s.update(kw)
    return s
