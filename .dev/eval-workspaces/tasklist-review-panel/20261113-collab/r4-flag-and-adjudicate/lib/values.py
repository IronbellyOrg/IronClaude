"""Timing formulas (REQ 2.0 timing rules, design 2.7) and the Spike 4 values builder.

The k formula lives only here. All formulas compute in integer milliseconds.
PANEL_SLACK_S (default 0) adds a slack in seconds to the 35% cap (cap = 1.35 B + SLACK_S); with it > 0 every CLI writes
under $R4_OUT/values-slack<S>/ instead of values/ and stamps slack_s in the file.

CLIs (each writes its file under $R4_OUT/values/ and a matching .sha256):
  values.py planning --panel <P>
  values.py build    --panel <P> --runs <A1 row dirs...>
  values.py srun     --panel <P>
  values.py slowdown --panel <P> --a1 <row dirs...> --srun <row dirs...>
  values.py tce      --values <file> --pkg <id>      (time-cap exception entry; prints JSON, writes no file)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import statistics
import sys
from datetime import datetime

R4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS_S = 2.0


def _ms(x: float) -> int:
    return int(round(x * 1000))


def slack_s() -> float:
    """Owner decision 2026-11-14: the time cap is 1.35 B + SLACK_S. PANEL_SLACK_S (seconds, default 0 = the old 1.35 B cap)."""
    try:
        return max(0.0, float(os.environ.get("PANEL_SLACK_S", "0") or 0))
    except ValueError:
        raise SystemExit("PANEL_SLACK_S must be a number of seconds")


def k_of(B: float, turn: float, rep: float, hooks: float = HOOKS_S, slack: float | None = None) -> int:
    """k = max(0, min(2, floor((0.35 B + SLACK_S - hooks - turn - rep) / (2 turn)))), in integer ms."""
    b, t, r, h = _ms(B), _ms(turn), _ms(rep), _ms(hooks)
    sl = _ms(slack_s() if slack is None else slack)
    if t <= 0:
        return 0
    return max(0, min(2, (b * 35 // 100 + sl - h - t - r) // (2 * t)))


def finish_offset(B: float, turn: float, rep: float, slack: float | None = None) -> float:
    """PANEL_FINISH_AT - T0 = 1.35 B + SLACK_S - turn_p90 - T_report_p90 (seconds)."""
    sl = _ms(slack_s() if slack is None else slack)
    return (_ms(B) * 135 // 100 + sl - _ms(turn) - _ms(rep)) / 1000


def hang_s(B: float) -> float:
    """Hang guard offset 1.5 B (seconds)."""
    return (_ms(B) * 150 // 100) / 1000


TCE_HANG_X = 3  # time-cap exception: hang guard is at least 3.0 x B_A1 (OVERRIDE.md)


def tce_entry(v: dict) -> dict:
    """Owner-authorised time-cap exception (OVERRIDE.md, 2026-11-14) for one package's values entry.

    Used only when TIME_CAP_EXCEPTION=1. k is forced to 1 where the measured k is 0 (else unchanged); the hang guard
    becomes max(hang_s, 3.0 B_A1); the finish offset keeps its original distance to the hang guard
    (hang_s - finish_offset_s = 0.15 B + turn_p90 + T_report_p90), so it moves by the same amount as the hang guard.
    The off path never calls this, so no value computed without the override changes.
    """
    hang, fin = _ms(v["hang_s"]), _ms(v["finish_offset_s"])
    new_hang = max(hang, _ms(v["B_A1"]) * TCE_HANG_X)
    k = int(v["k"])
    return {"k": max(1, k), "k_measured": k, "k_forced": k < 1,
            "finish_offset_s": (new_hang - (hang - fin)) / 1000, "hang_s": new_hang / 1000}


def slowdown_limit(B: float, turn: float, k: int, hooks: float = HOOKS_S, slack: float | None = None) -> float | None:
    """Section 3 limit s <= (0.35 B + SLACK_S - W) / B with W = hooks + 2k turns + one turn of slip; None when k = 0."""
    if k < 1:
        return None
    w = _ms(hooks) + (2 * k + 1) * _ms(turn)
    sl = _ms(slack_s() if slack is None else slack)
    return (_ms(B) * 35 // 100 + sl - w) / _ms(B)


def p90(xs: list[float]) -> float | None:
    """Nearest rank: the value at position ceil(0.9 n) of the sorted list."""
    if not xs:
        return None
    s = sorted(xs)
    return s[math.ceil(0.9 * len(s)) - 1]


def _ts(s: str) -> float:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def turns(transcript: str) -> list[float]:
    """Durations (s) of the main-thread assistant turns of one transcript, in order.

    Consecutive entries with the same message.id form one turn; its duration runs from the
    timestamp of the last entry before the group to the timestamp of the group's last entry.
    """
    entries = []
    try:
        with open(transcript, encoding="utf-8") as fh:
            for line in fh:
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(e, dict) and e.get("timestamp") and not e.get("isSidechain"):
                    entries.append(e)
    except OSError:
        return []
    out: list[float] = []
    i = 0
    while i < len(entries):
        e = entries[i]
        mid = (e.get("message") or {}).get("id") if e.get("type") == "assistant" else None
        if mid is None:
            i += 1
            continue
        j = i
        while (
            j + 1 < len(entries)
            and entries[j + 1].get("type") == "assistant"
            and (entries[j + 1].get("message") or {}).get("id") == mid
        ):
            j += 1
        if i > 0:
            out.append(_ts(entries[j]["timestamp"]) - _ts(entries[i - 1]["timestamp"]))
        i = j + 1
    return out


def elapsed_s(pkgdir: str) -> float | None:
    """(max reviewer t_end_ms - T0) / 1000 for one package-run (retries and re-asks included)."""
    try:
        with open(os.path.join(pkgdir, "panel.json")) as fh:
            panel = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None
    ends = []
    for r in panel.get("reviewers", []):
        try:
            with open(os.path.join(pkgdir, "reviews", r["rid"] + ".meta.json")) as fh:
                ends.append(json.load(fh)["t_end_ms"])
        except (OSError, KeyError, json.JSONDecodeError):
            pass
    return (max(ends) - panel["t0_ms"]) / 1000 if ends else None


def cp_rids(panel: dict, panel_def: dict) -> list[str]:
    if panel_def["cp_role"] == "flagger":
        return [panel_def["flagger"]["rid"]]
    return [a["rid"] for a in panel_def["adjudicators"]]


def cp_wall_s(pkgdir: str, rids: list[str]) -> float | None:
    """Wall of the critical-path role in one package-run: (max t_end_ms of those reviewers - T0) / 1000."""
    try:
        with open(os.path.join(pkgdir, "panel.json")) as fh:
            t0 = json.load(fh)["t0_ms"]
    except (OSError, KeyError, json.JSONDecodeError):
        return None
    ends = []
    for rid in rids:
        try:
            with open(os.path.join(pkgdir, "reviews", rid + ".meta.json")) as fh:
                ends.append(json.load(fh)["t_end_ms"])
        except (OSError, KeyError, json.JSONDecodeError):
            pass
    return (max(ends) - t0) / 1000 if ends else None


# ---------------------------------------------------------------- files


def _load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def packages() -> list[dict]:
    return _load(os.path.join(R4, "frozen", "packages.json"))


def panel_def(p: str) -> dict:
    return _load(os.path.join(R4, "frozen", "panels.json"))["panels"][p]


def out_dir() -> str:
    """values/ normally; values-slack30/ (named by the slack in seconds) when PANEL_SLACK_S > 0, so the old files are never touched."""
    sl = slack_s()
    d = os.path.join(os.environ.get("R4_OUT", R4), "values" if sl <= 0 else f"values-slack{sl:g}")
    os.makedirs(d, exist_ok=True)
    return d


def write_pinned(path: str, obj) -> str:
    if slack_s() > 0 and isinstance(obj, dict):
        obj = {**obj, "slack_s": int(slack_s()) if slack_s() == int(slack_s()) else slack_s()}  # the launcher refuses a values file whose slack differs from PANEL_SLACK_S
    data =(json.dumps(obj, indent=1, sort_keys=True) + "\n").encode()
    with open(path, "wb") as fh:
        fh.write(data)
    h = hashlib.sha256(data).hexdigest()
    with open(path + ".sha256", "w") as fh:
        fh.write(f"{h}  {os.path.basename(path)}\n")
    return h


def _entry(B, turn, rep, cp_role, **extra) -> dict:
    k = k_of(B, turn, rep)
    d = {
        "B_A1": B,
        "turn_p90": turn,
        "T_report_p90": rep,
        "finish_offset_s": finish_offset(B, turn, rep),
        "hang_s": hang_s(B),
        "k": k,
        "deliver": True,
        "cp_role": cp_role,
    }
    d.update(extra)
    return d


def cmd_planning(a) -> str:
    pd = panel_def(a.panel)
    pl = pd["planning"]
    obj = {
        "panel": a.panel,
        "kind": "planning",
        "packages": {
            p["id"]: _entry(pl["B"], pl["turn"], pl["rep"], pd["cp_role"], planning=True, n_runs=0, source_rows=[])
            for p in packages()
        },
    }
    path = os.path.join(out_dir(), f"planning-{a.panel}.json")
    write_pinned(path, obj)
    return path


def cmd_build(a) -> str:
    pd = panel_def(a.panel)
    rids = cp_rids({}, pd)
    pk = {}
    for p in packages():
        els, tns, reps, rows = [], [], [], []
        for row in a.runs:
            pkgdir = os.path.join(row, p["id"])
            el = elapsed_s(pkgdir)
            if el is None:
                continue
            rows.append(os.path.basename(os.path.normpath(row)))
            els.append(el)
            for rid in rids:
                t = turns(os.path.join(pkgdir, "reviews", rid + ".transcript.jsonl"))
                if t:
                    tns.extend(t)
                    reps.append(t[-1])
        if not els or not tns:
            raise SystemExit(f"no usable A1 rows for {p['id']}")
        B = statistics.median(els)
        pk[p["id"]] = _entry(round(B, 3), round(p90(tns), 3), round(p90(reps), 3), pd["cp_role"], n_runs=len(els), source_rows=rows)
    path = os.path.join(out_dir(), f"{a.panel}.json")
    write_pinned(path, {"panel": a.panel, "kind": "measured", "packages": pk})
    return path


def cmd_srun(a) -> str:
    src = _load(os.path.join(out_dir(), f"{a.panel}.json"))
    src["kind"] = "srun"
    for v in src["packages"].values():
        v["deliver"] = False
    path = os.path.join(out_dir(), f"{a.panel}-srun.json")
    write_pinned(path, src)
    return path


def cmd_slowdown(a) -> str:
    pd = panel_def(a.panel)
    rids = cp_rids({}, pd)
    vals = _load(os.path.join(out_dir(), f"{a.panel}.json"))["packages"]
    pk = {}
    for p in packages():
        v = vals[p["id"]]
        base = [w for w in (cp_wall_s(os.path.join(r, p["id"]), rids) for r in a.a1) if w is not None]
        sr = [w for w in (cp_wall_s(os.path.join(r, p["id"]), rids) for r in a.srun) if w is not None]
        s = statistics.median(sr) / statistics.median(base) - 1 if base and sr else None
        lim = slowdown_limit(v["B_A1"], v["turn_p90"], v["k"])
        pk[p["id"]] = {
            "s": None if s is None else round(s, 4),
            "k": v["k"],
            "limit": None if lim is None else round(lim, 4),
            "budget_fail": bool(s is not None and lim is not None and s > lim),
            "n_a1": len(base),
            "n_srun": len(sr),
        }
    path = os.path.join(out_dir(), f"{a.panel}-slowdown.json")
    write_pinned(path, {"panel": a.panel, "packages": pk})
    return path


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "tce":  # values.py tce --values <file> --pkg <id>: prints the exception entry, writes nothing
        tp = argparse.ArgumentParser(prog="values.py tce")
        tp.add_argument("--values", required=True)
        tp.add_argument("--pkg", required=True)
        t = tp.parse_args(argv[2:])
        print(json.dumps(tce_entry(_load(t.values)["packages"][t.pkg]), sort_keys=True))
        return 0
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("planning", "build", "srun", "slowdown"):
        sp = sub.add_parser(name)
        sp.add_argument("--panel", required=True, choices=("EL2", "SL2", "HL2"))
        if name == "build":
            sp.add_argument("--runs", nargs="+", required=True)
        if name == "slowdown":
            sp.add_argument("--a1", nargs="+", required=True)
            sp.add_argument("--srun", nargs="+", required=True)
    a = ap.parse_args(argv[1:])
    path = {"planning": cmd_planning, "build": cmd_build, "srun": cmd_srun, "slowdown": cmd_slowdown}[a.cmd](a)
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
