"""The timing spike record (DESIGN 12.4, REQ-32): c, the seconds one ledger row costs luna.

    c = (median(RL run of luna 1) - median(Z0 run of luna 1) - 4) / mean rows written by luna 1 in the RL runs

The 4 is the reading time of DESIGN 10.1. The medians are of the reviewer's `wall_s` over the runs in which it finished
(`status` ok); the rows are `rows_per_reviewer` of each RL run's check/check.json. `write_record` stores the record as
`spike` in a values file, next to the planning values and never over them. bin/run-spike.sh timing calls this file as
a script:

    spike.py timing --values FILE --rid RID --doc D --panel P --rl-run DIR ... --z0-run DIR ...

This file only reads finished run folders: it starts no model.
"""

import argparse
import datetime
import json
import statistics
import sys
from pathlib import Path

READING_S = 4


class SpikeError(Exception):
    pass


def _json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def luna_seconds(dirs, rid) -> list[float]:
    """`wall_s` of the reviewer in each run folder where it finished."""
    out = []
    for d in dirs:
        meta = _json(Path(d) / "reviews" / f"{rid}.meta.json")
        if meta and meta.get("status") == "ok":
            out.append(float(meta["wall_s"]))
    return out


def rows_written(dirs, rid) -> list[int]:
    out = []
    for d in dirs:
        chk = _json(Path(d) / "check" / "check.json")
        if chk and rid in chk.get("rows_per_reviewer", {}):
            out.append(int(chk["rows_per_reviewer"][rid]))
    return out


def timing_record(rl_dirs, z0_dirs, rid, doc, panel, date=None) -> dict:
    rl_s, z0_s, rows = (
        luna_seconds(rl_dirs, rid),
        luna_seconds(z0_dirs, rid),
        rows_written(rl_dirs, rid),
    )
    if not rl_s or not z0_s or not rows or not sum(rows):
        raise SpikeError(
            f"no usable data: {len(rl_s)} RL and {len(z0_s)} Z0 runs where {rid} finished, "
            f"{len(rows)} RL runs with its rows"
        )
    m_rl, m_z0 = statistics.median(rl_s), statistics.median(z0_s)
    mean_rows = statistics.fmean(rows)
    c = (m_rl - m_z0 - READING_S) / mean_rows
    if c <= 0:
        raise SpikeError(
            f"c = {c:.3f} s is not positive (RL median {m_rl} s, Z0 median {m_z0} s): "
            "the spike measured noise, run it again"
        )
    return {
        "runs": len(rl_s),
        "baseline_runs": len(z0_s),
        "c_luna": round(c, 3),
        "median_rl_s": m_rl,
        "median_z0_s": m_z0,
        "mean_rows": mean_rows,
        "reading_s": READING_S,
        "rid": rid,
        "doc": doc,
        "panel": panel,
        "date": date or datetime.date.today().isoformat(),
    }


def write_record(values_path, record: dict) -> None:
    p = Path(values_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    data["spike"] = record
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    tmp.replace(p)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="spike.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("timing", help="compute c and write the spike record")
    t.add_argument("--values", required=True)
    t.add_argument("--rid", required=True, help="reviewer id of luna 1")
    t.add_argument("--doc", required=True)
    t.add_argument("--panel", required=True)
    t.add_argument("--rl-run", action="append", default=[])
    t.add_argument("--z0-run", action="append", default=[])
    args = ap.parse_args(argv)
    try:
        rec = timing_record(args.rl_run, args.z0_run, args.rid, args.doc, args.panel)
        write_record(args.values, rec)
    except (SpikeError, OSError, ValueError) as e:
        print(f"E_SPIKE_DATA: {e}", file=sys.stderr)
        return 1
    print(json.dumps(rec, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
