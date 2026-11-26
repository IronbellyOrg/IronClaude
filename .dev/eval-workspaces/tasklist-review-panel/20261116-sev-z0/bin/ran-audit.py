"""The 20 rows of the `ran` audit (TESTING REQ-28, row M), each with the tool calls of its reviewer's transcript.

    ran-audit.py [RUN_DIR ...] [--rows N] [--seed S]

RUN_DIR is a run folder (it has `reviews/`) or a folder of run folders; the default is RL/runs/spike-compliance. The rows are
those of analysis/ran_check.py with their `ran_status`; N of them (default 20) are drawn with a seeded sample, so the same
runs give the same rows. For each row it prints what the reviewer wrote in `ran`, the status the heuristic gave, the
transcript path and the transcript's tool calls (the command or input, and the start of the result). A person reads them and
writes results/ran-audit.md: agreement on at least 18 of 20 rows, else DESIGN 7.7 is revised. Called by
bin/open-manual-checks.sh ran-audit. It reads run folders and starts nothing.
"""

import argparse
import os
import random
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_RL = os.path.dirname(_HERE)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]
if _RL not in sys.path:
    sys.path.insert(0, _RL)

from analysis import ran_check  # noqa: E402

CLIP = 300


def clip(text, n=CLIP):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n] + " ..."


def collect(paths):
    """[(run folder, row)] of every run folder named."""
    out = []
    for run in ran_check.run_dirs_of(paths):
        out += [(run, r) for r in ran_check.check_run(run)]
    return out


def show(i, n, run, row):
    path = Path(run) / "reviews" / f"{row['reviewer']}.attempt1.json"
    print(
        f"=== row {i} of {n}: run {row['run']}, reviewer {row['reviewer']}, item {row['item']} (class {row['class']}) ==="
    )
    print(f"ran: {clip(row['ran'])}")
    print(f"ran_status: {row['status']}")
    print(f"transcript: {path}")
    calls = (
        ran_check.calls_of(path.read_text(encoding="utf-8")) if path.is_file() else []
    )
    if not calls:
        print("tool calls: none")
    for k, c in enumerate(calls, 1):
        print(f"  {k}. {c['name']}: {clip(c['text'])}")
        print(f"     -> {clip(c['result'], 200)}")
    print()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("runs", nargs="*")
    ap.add_argument("--rows", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261115)
    a = ap.parse_args(argv)
    runs = a.runs or [str(Path(_RL) / "runs" / "spike-compliance")]
    missing = [r for r in runs if not Path(r).is_dir()]
    if missing:
        print(f"ran-audit: no such folder: {missing[0]}", file=sys.stderr)
        return 2
    rows = collect(runs)
    if not rows:
        print("ran-audit: no ledger rows found in the run folders", file=sys.stderr)
        return 1
    pick = random.Random(a.seed).sample(rows, min(a.rows, len(rows)))
    pick.sort(key=lambda t: (t[1]["run"], t[1]["reviewer"], t[1]["item"]))
    for i, (run, row) in enumerate(pick, 1):
        show(i, len(pick), run, row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
