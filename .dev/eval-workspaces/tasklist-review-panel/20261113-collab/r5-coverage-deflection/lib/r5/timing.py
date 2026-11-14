"""Timing rules (DESIGN 2.5; MR:284-308, R-41, R-42) and the Spike 4 values writer (R-30)."""
import argparse
import hashlib
import json
import math
import os
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

from r5 import cfg, out, read_json, read_jsonl

HOOKS_S = 2.0


def slack_s() -> int:
    """Extra whole seconds on top of the +35% cap (owner decision 2026-11-14): env PANEL_SLACK_S, default 0.

    The cap is 1.35 B + slack_s. The hang guard (1.5 B) is not derived from the cap and does not move.
    """
    v = os.environ.get("PANEL_SLACK_S", "") or "0"
    if not re.fullmatch(r"0|[1-9][0-9]*", v):
        raise ValueError(f"PANEL_SLACK_S must be a whole number of seconds (0, 30, ...), got {v!r}")
    return int(v)


def values_dirname() -> str:
    """Folder under config/ that holds the frozen values for the active slack (`values` when slack is 0)."""
    s = slack_s()
    return "values" if s == 0 else f"values-slack{s}"


def k(B: float, turn: float, report: float, hooks: float = HOOKS_S) -> int:
    return max(0, min(2, math.floor((0.35 * B + slack_s() - hooks - turn - report) / (2 * turn) + 1e-9)))


def finish_offset(B: float, turn: float, report: float) -> float:
    return 1.35 * B + slack_s() - turn - report


def hang_offset(B: float) -> float:
    return 1.5 * B


def slowdown_limit(B: float, k_: int, turn: float, hooks: float = HOOKS_S) -> float:
    return (0.35 * B + slack_s() - (hooks + 2 * k_ * turn)) / B


# Owner-authorised time-cap exception (2026-11-14, OVERRIDE.md). Off unless TIME_CAP_EXCEPTION=1.
EXC_HANG_FACTOR = 3.0  # hang guard = max(existing, 3.0 x B_A1)
EXC_CAP_FACTOR = 2.7   # cap used for the finish signal and over_cap: 0.9 x the hang guard (same ratio as 1.35 B to 1.5 B)
EXC_FORCED_K = 1


def time_cap_exception() -> int:
    """TIME_CAP_EXCEPTION: unset, empty or 0 = off (default); 1 = on. Anything else is refused."""
    v = os.environ.get("TIME_CAP_EXCEPTION", "") or "0"
    if v not in ("0", "1"):
        raise ValueError(f"TIME_CAP_EXCEPTION must be 0 or 1 (forced k of 1), got {v!r}")
    return int(v)


def exception_plan(vals: dict, on: bool) -> dict:
    """What one package runs with. `vals` is a frozen Spike 4 values file.

    Off: every number is the file's own (nothing recomputed), so an off row is byte-for-byte the old behaviour.
    On: k = 1 where the measured k is 0 (a measured k of 1 or 2 stays); hang guard = max(file value, 3.0 B_A1);
    finish offset = 2.7 B - turn - report (the finish signal moves out with the hang guard);
    the kit-slowdown limit is re-evaluated against the widened cap: (1.7 B - (2 + 2 k turn)) / B.
    """
    B, turn, report = vals["B_f_s"], vals["turn_p90_s"], vals["T_report_p90_s"]
    k_meas = vals["k"]
    plan = {"time_cap_exception": bool(on), "B_A1_s": B, "k_measured": k_meas}
    if not on:
        return {**plan, "k_run": k_meas, "k_forced": False, "hang_offset_s": vals["hang_offset_s"],
                "finish_offset_s": vals["finish_offset_s"], "time_cap_s": 1.35 * B + vals.get("slack_s", 0),
                "slowdown_limit": vals["slowdown_limit"], "budget_ok": vals["budget_ok"]}
    k_run = EXC_FORCED_K if k_meas == 0 else k_meas
    cap = EXC_CAP_FACTOR * B
    limit = (cap - B - (HOOKS_S + 2 * k_run * turn)) / B
    s = vals.get("slowdown_s")
    return {**plan, "k_run": k_run, "k_forced": k_meas == 0,
            "hang_offset_s": max(vals["hang_offset_s"], EXC_HANG_FACTOR * B), "finish_offset_s": cap - turn - report,
            "time_cap_s": cap, "slowdown_limit": limit, "budget_ok": s is not None and s <= limit}


def p90(values: list[float]) -> float:
    """Nearest-rank 90th percentile (with 4 runs this is the maximum)."""
    v = sorted(values)
    return v[max(0, math.ceil(0.9 * len(v)) - 1)]


def _ts(s: str) -> float:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def turns(session_jsonl) -> list[float]:
    """Main-session model turn durations in seconds; the last one is the report turn.

    A turn is a run of consecutive assistant entries; it starts at the timestamp of the entry before it.
    """
    entries = [
        e for e in read_jsonl(session_jsonl)
        if e.get("type") in ("user", "assistant") and not e.get("isSidechain") and e.get("timestamp")
    ]
    out_: list[float] = []
    prev_ts, group_end = None, None
    for e in entries:
        t = _ts(e["timestamp"])
        if e["type"] == "assistant":
            if group_end is None:
                group_start = prev_ts if prev_ts is not None else t
            group_end = t
        else:
            if group_end is not None:
                out_.append(max(0.0, group_end - group_start))
                group_end = None
            prev_ts = t
    if group_end is not None:
        out_.append(max(0.0, group_end - group_start))
    return out_


def _final_attempt_session(rev_dir: Path, rid: str):
    for n in (2, 1):
        p = rev_dir / f"{rid}.attempt{n}.session.jsonl"
        if p.exists():
            return p
    return None


def _wall(rev_dir: Path, rid: str):
    c = read_json(rev_dir / f"{rid}.cost.json")
    return c and c.get("total_wall_s")


def spike4(panel: str, rows: list[str], kit_rows: list[str], force: bool) -> int:
    panels = read_json(cfg() / "panels.json")
    P = panels[panel]
    receivers = [r["rid"] for r in P["reviewers"] if r["role"] == "receiver"]
    vdir = cfg() / values_dirname() / panel
    vdir.mkdir(parents=True, exist_ok=True)
    sums_p = vdir / "SHA256SUMS"
    sums = dict(reversed(line.split(None, 1)) for line in sums_p.read_text().splitlines() if line.strip()) if sums_p.exists() else {}
    pkgs = sorted({p.name for r in rows for p in (out() / "runs" / r).iterdir() if p.is_dir()})
    existing = [p for p in pkgs if (vdir / f"{p}.json").exists()]
    if existing and not force:
        print(f"refused: values exist for {existing} (written once; --force to replace)", file=sys.stderr)
        return 1
    for pkg in pkgs:
        target = vdir / f"{pkg}.json"
        elapsed, tt, reports, a1_wall, kit_wall, runs = [], [], [], [], [], []
        for r in rows:
            d = out() / "runs" / r / pkg
            c = read_json(d / "collab.json") or {}
            if c.get("elapsed_s") is None:
                continue
            elapsed.append(c["elapsed_s"])
            for rid in receivers:
                s = _final_attempt_session(d / "reviews", rid)
                ts = turns(s) if s else []
                if ts:
                    tt.extend(ts)
                    reports.append(ts[-1])
                w = _wall(d / "reviews", rid)
                if w:
                    a1_wall.append(w)
            runs.append(r)
        for r in kit_rows:
            d = out() / "runs" / r / pkg
            for rid in receivers:
                w = _wall(d / "reviews", rid)
                if w:
                    kit_wall.append(w)
        if not elapsed or not tt:
            print(f"refused: no usable runs for {pkg}", file=sys.stderr)
            return 1
        B = statistics.median(elapsed)
        turn, report = p90(tt), p90(reports)
        kk = k(B, turn, report)
        s = (statistics.median(kit_wall) / statistics.median(a1_wall) - 1) if kit_wall and a1_wall else None
        lim = slowdown_limit(B, kk, turn)
        vals = {
            "panel": panel, "pkg": pkg, "B_f_s": B, "turn_p90_s": turn, "T_report_p90_s": report, "hooks_s": 2,
            "slack_s": slack_s(), "k": kk, "finish_offset_s": finish_offset(B, turn, report), "hang_offset_s": hang_offset(B),
            "slowdown_s": s, "slowdown_limit": lim, "budget_ok": (s is not None and s <= lim),
            "runs": runs, "kit_runs": kit_rows, "n_turns": len(tt), "n_reports": len(reports),
            "p90_method": "nearest rank; with 4 runs p90 is close to the maximum",
            "measured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        text = json.dumps(vals, indent=1) + "\n"
        target.write_text(text)
        sums[f"{pkg}.json"] = hashlib.sha256(text.encode()).hexdigest()
        print(json.dumps({"pkg": pkg, "B_f_s": B, "turn_p90_s": turn, "T_report_p90_s": report, "k": kk, "budget_ok": vals["budget_ok"]}))
    sums_p.write_text("".join(f"{h}  {n}\n" for n, h in sorted(sums.items())))
    return 0


def main(argv: list[str]) -> int:
    if argv and argv[0] == "offsets":  # offsets <B> <turn> <report>: JSON for run-panel.sh planning mode
        B, turn, report = map(float, argv[1:4])
        print(json.dumps({"k": k(B, turn, report), "finish_offset_s": finish_offset(B, turn, report), "hang_offset_s": hang_offset(B)}))
        return 0
    if argv and argv[0] == "exception":  # exception <values.json>: the plan for that package under the active TIME_CAP_EXCEPTION
        print(json.dumps(exception_plan(json.loads(Path(argv[1]).read_text()), bool(time_cap_exception()))))
        return 0
    ap = argparse.ArgumentParser(prog="r5.timing")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s4 = sub.add_parser("spike4")
    s4.add_argument("--panel", required=True)
    s4.add_argument("--rows", required=True)
    s4.add_argument("--kit-rows", default="")
    s4.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    return spike4(a.panel, a.rows.split(","), [r for r in a.kit_rows.split(",") if r], a.force)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
