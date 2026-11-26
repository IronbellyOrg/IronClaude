"""F-JUDGE (TESTING section 2, REQ-43): synthetic run folders and judge folders. Every name, path and text is invented;
there is no ground truth here, the score files hold only counts and invented notes.

    write_runs(root)    -> {run id: folder}   root/<run id>/{run.json, resolution.json, merged/merged-1.md}
                           (the merged report has the shape of the real merge output: it prints each reviewer's report
                           path with the run id, and carries arm marker text that the anonymiser must remove)
    write_scoring(root) -> {case: folder}     root/<case>/{merged-anon.md, judge.json, judge.err, score.json}
        ok            judge answered, score has the right row counts
        err_score     judge.json is an API error and a score file is still there (the defect REQ-43 audits)
        rows_total    score says 4 rows, the report has 3
        rows_blocking score says 2 blocking rows, the report has 1
        no_score      judge answered, no score file
        stale         score older than the report it scores
        bad_json      judge.json is not JSON
        err_stderr    judge.json looks fine, judge.err holds an API error
    ROWS, BLOCKING are the row counts of the merged reports.
"""

import json
import os
from pathlib import Path

ROWS, BLOCKING = 3, 1
IDS = ("a1-1", "b2-1", "c3-1")
T0 = 1_700_000_000  # the report's mtime; judge output follows 5 s later

RAW = """review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-synth/cand/doc-x/candidate.md sha256 {sha}
reviewers:
- a1-1: report /home/someone/eval/runs/{run}/normalised/a1-1.md, block ok true
- b2-1: report /home/someone/eval/runs/{run}/normalised/b2-1.md, block ok true
- c3-1: report /home/someone/eval/runs/{run}/normalised/c3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | a1-1 |
| L2 | open | no | overlap | MINOR | - | b2-1, c3-1 |
| L3 | open | no | single | MINOR | - | c3-1 |

## Blocking findings

- L1 (MAJOR, open, single): The table row says 5 where the text says 4. class: C4 probe=true src=sandbox
  Raised by a1-1 under ledger-v1 in arm RL (see runs/{run}/reviews/a1-1.md).

## Other findings

- L2 (MINOR, open, overlap): The wording leaves one reading open.
- L3 (MINOR, open, single): A step names no owner.

## Reviser brief

Blocking finding ids: L1.

verdict: FAIL
"""

ANON = """review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 {sha}
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | no | overlap | MINOR | - | R2, R3 |
| L3 | open | no | single | MINOR | - | R3 |

## Blocking findings

- L1 (MAJOR, open, single): The table row says 5 where the text says 4.

## Other findings

- L2 (MINOR, open, overlap): The wording leaves one reading open.
- L3 (MINOR, open, single): A step names no owner.
"""

OK_MSG = "score.json written, gt_covered_any 2, wrong_blockers 0"


def write_runs(
    root,
    runs=(("synth-rl-1", "doc-x"), ("synth-z0-1", "doc-x"), ("synth-k-1", "doc-y")),
):
    out = {}
    for run, doc in runs:
        d = Path(root) / run
        (d / "merged").mkdir(parents=True)
        (d / "merged" / "merged-1.md").write_text(
            RAW.format(run=run, sha="ab" * 32), encoding="utf-8"
        )
        meta = {
            "arm": "RL",
            "doc": doc,
            "reviewers": {rid: {"model": "synthetic"} for rid in IDS},
        }
        (d / "run.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
        res = {"reviewers": [{"reviewer_id": rid, "model": "synthetic"} for rid in IDS]}
        (d / "resolution.json").write_text(
            json.dumps(res, indent=1) + "\n", encoding="utf-8"
        )
        out[run] = d
    return out


def _score(label, rows=ROWS, blocking=BLOCKING):
    return {
        "label": label,
        "combo": label,
        "package": "doc-x",
        "gt_total": 3,
        "gt_covered_any": ["GT1", "GT2"],
        "gt_covered_blocking": ["GT1"],
        "ledger_rows_total": rows,
        "ledger_rows_blocking": blocking,
        "blocking_rows_gt_matched": 1,
        "wrong_blockers": 0,
        "notes": "invented",
    }


def _result(text, error=False):
    return [
        {
            "type": "result",
            "subtype": "error_during_execution" if error else "success",
            "is_error": error,
            "result": text,
        }
    ]


def write_scoring(root):
    cases = {
        "ok": dict(),
        "err_score": dict(judge=_result("API Error: 529 overloaded_error", True)),
        "rows_total": dict(score=_score("rows_total", rows=4)),
        "rows_blocking": dict(score=_score("rows_blocking", blocking=2)),
        "no_score": dict(score=None),
        "stale": dict(score_age=-100),
        "bad_json": dict(judge="this is not json"),
        "err_stderr": dict(err="API Error: 500 internal server error\n"),
    }
    out = {}
    for name, c in cases.items():
        d = Path(root) / name
        d.mkdir(parents=True)
        merged = d / "merged-anon.md"
        merged.write_text(ANON.format(sha="cd" * 32), encoding="utf-8")
        judge = c.get("judge", _result(OK_MSG))
        (d / "judge.json").write_text(
            judge if isinstance(judge, str) else json.dumps(judge), encoding="utf-8"
        )
        (d / "judge.err").write_text(c.get("err", ""), encoding="utf-8")
        files = [merged, d / "judge.json", d / "judge.err"]
        os.utime(merged, (T0, T0))
        score = c.get("score", _score(name))
        if score is not None:
            (d / "score.json").write_text(json.dumps(score), encoding="utf-8")
            files.append(d / "score.json")
        for f in files[1:]:
            t = T0 + c.get("score_age", 5) if f.name == "score.json" else T0 + 5
            os.utime(f, (t, t))
        out[name] = d
    return out
