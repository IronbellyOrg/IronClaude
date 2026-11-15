"""G0 for Recipe Ledger, the ledger-and-time half only (DESIGN 3.3, 12.3; the "ledger and time" row of MR 5.7).

g0.py --runs DIR [--prefix P] [--out FILE]
    DIR is a folder of run folders (the compliance spike). Two checks, both computed by analysis/analyze.py (this file
    defines no metric of its own):
      ledger_missing   rate before any re-ask over the reviewer runs of the RL runs that have a check, at most 10%
                       (`analyze.compliance`);
      luna cost        the measured seconds per ledger row (`analyze.time_table`) at or below the break-even row cost
                       of the 14-row cap at the measured b (the planned b when no Z0 run is there to measure it).
    Prints both, writes the JSON record to FILE, exits 0 when both pass and 1 otherwise. A cost that cannot be
    measured (no luna rows, no Z0 run to subtract) is not a pass. The selection half of G0 belongs to Redesign 1 and
    is not built here.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_RL = os.path.dirname(_HERE)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]
if _RL not in sys.path:
    sys.path.insert(0, _RL)

import argparse  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

from analysis import analyze as az  # noqa: E402


def g0(runs):
    """{ledger_missing, luna_cost_per_row, pass} for the loaded runs of `analyze.load_runs`."""
    lm = az.compliance([r["dir"] for r in runs])["ledger_missing"]
    t = az.time_table(runs)
    c = t["luna_cost_per_row"]["measured"]
    be = t["breakeven_row_cost_14"]
    limit = be["measured"] if be["measured"] is not None else be["planned"]
    cost = {
        "measured": c,
        "planned": t["luna_cost_per_row"]["planned"],
        "breakeven": limit,
        "pass": c is not None and c <= limit + az.EPS,
    }
    return {
        "ledger_missing": lm,
        "luna_cost_per_row": cost,
        "pass": lm["pass"] and cost["pass"],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", required=True)
    ap.add_argument("--prefix", default="")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    res = g0(az.load_runs(a.runs, a.prefix))
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(
            json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    lm, c = res["ledger_missing"], res["luna_cost_per_row"]
    print(
        f"ledger_missing: {lm['count']} of the reviewer runs, rate {lm['rate']}, limit {lm['limit']}: {'pass' if lm['pass'] else 'FAIL'}"
    )
    print(
        f"luna cost per row: measured {c['measured']}, break-even {c['breakeven']}: {'pass' if c['pass'] else 'FAIL'}"
    )
    print("G0 (ledger and time): " + ("pass" if res["pass"] else "FAIL"))
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
