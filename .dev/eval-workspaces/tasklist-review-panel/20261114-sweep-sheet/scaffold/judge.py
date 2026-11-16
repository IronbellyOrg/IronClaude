"""Judge-batch helpers (REQ-43, DESIGN 11.3, 14.3): the seeded second-judge sample and the audit of judge outputs.

Standard library only. bin/judge-batch.sh runs it as a script:
    judge.py sample SEED ID...    prints the ids of the second-judge sample, one per line
    judge.py audit DIR...         prints the audit as JSON; exit 1 when any folder is bad
A judge folder holds merged-anon.md (the report the judge saw), judge.json, judge.err, judge.started and score.json.
"""

import json
import random
import re
import sys
from pathlib import Path

FRACTION = 0.15
# The text of an Opus API error: the `result` of a failed call, or a line of its stderr.
API_ERROR = re.compile(r"^\s*API Error\b", re.M)


def sample(ids, seed, fraction=FRACTION):
    """round(fraction * n) of the n distinct ids, drawn with a generator seeded by `seed`; sorted."""
    ids = sorted(set(ids))
    return sorted(random.Random(seed).sample(ids, round(fraction * len(ids))))


def ledger_counts(text):
    """(rows, blocking rows) of the `## Ledger` table of a merged report (columns: lid, status, blocking, ...)."""
    rows = blocking = 0
    inside = False
    for line in text.splitlines():
        if line.strip() == "## Ledger":
            inside = True
        elif inside and line.startswith("## "):
            break
        elif inside and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells[0] == "lid" or not cells[0].strip("-: "):
                continue  # the header and the separator row
            rows += 1
            blocking += len(cells) > 2 and cells[2] == "yes"
    return rows, blocking


def _is_api_error(node):
    """True when a parsed judge.json carries `is_error: true` or a string that starts with `API Error`."""
    if isinstance(node, dict):
        return node.get("is_error") is True or any(
            _is_api_error(v) for v in node.values()
        )
    if isinstance(node, list):
        return any(_is_api_error(v) for v in node)
    return isinstance(node, str) and API_ERROR.search(node) is not None


def _load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, ValueError):
        return None, False


def audit_one(folder):
    """The problems of one judge folder (an empty list means clean)."""
    d = Path(folder)
    bad = []
    jj = d / "judge.json"
    if not jj.is_file():
        bad.append("judge_missing")
    else:
        data, ok = _load(jj)
        if not ok:
            bad.append("judge_unparseable")
        elif _is_api_error(data):
            bad.append("api_error")
    err = d / "judge.err"
    if "api_error" not in bad and err.is_file():
        if API_ERROR.search(err.read_text(encoding="utf-8", errors="replace")):
            bad.append("api_error")
    sc = d / "score.json"
    if not sc.is_file():
        bad.append("no_score")
        return bad
    score, ok = _load(sc)
    if not ok or not isinstance(score, dict):
        bad.append("score_unparseable")
    else:
        report = d / "merged-anon.md"
        if not report.is_file():
            bad.append("no_merged_report")
        else:
            rows = ledger_counts(report.read_text(encoding="utf-8"))
            if (
                score.get("ledger_rows_total"),
                score.get("ledger_rows_blocking"),
            ) != rows:
                bad.append("rows_mismatch")
    # A score file older than the start of this judge run is left over from an earlier run (the defect CR line 147 describes).
    started = d / "judge.started"
    if started.is_file() and sc.stat().st_mtime < started.stat().st_mtime:
        bad.append("score_stale")
    return bad


def audit(folders):
    items = []
    for f in folders:
        problems = audit_one(f)
        if problems:
            items.append({"dir": str(f), "problems": problems})
    return {"checked": len(folders), "bad": len(items), "items": items}


def main(argv):
    if len(argv) >= 3 and argv[1] == "sample":
        for i in sample(argv[3:], int(argv[2])):
            print(i)
        return 0
    if len(argv) >= 2 and argv[1] == "audit":
        result = audit(argv[2:])
        print(json.dumps(result, indent=1))
        return 1 if result["bad"] else 0
    print("usage: judge.py sample SEED ID... | judge.py audit DIR...", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
