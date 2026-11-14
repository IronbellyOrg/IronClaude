# ruff: noqa: N803, N806  (B and G are the design's own symbols)
"""Timing values (R-41, R-42, R-43, R-45) and the Spike 4 aggregation. DESIGN.md section 2.6.

Usage (from REPO, uv run python tools/values.py ...):
  spike4 <panel> <row> <row> <row> [...] [--root R1]   write values/<panel>/<pkg>.json (+ .sha256) for the 3 packages
  show <panel> <pkg> [--root R1]                        print the values file, or the planning fallback
  deadlines <panel> <pkg> <collab 0|1> <T0_MS> [--root R1] [--cap-exception 1]
      print {"values","FINISH_MS","GUARD_MS","HANG_MS","k","T_report","finish_offset_s","guard_offset_s",
             "hang_offset_s","B"}; exit 2 when collab 1 has no values file (k cannot be computed).
      --cap-exception 1 (collab 1 only; launch.sh passes it for TIME_CAP_EXCEPTION=1): cap_exception() below, and the output
      gains "time_cap_exception": true and "cap_exception": {...}. Without the flag the output is exactly as before.
All times are seconds from T0. p90 is the nearest-rank 90th percentile.
PANEL_SLACK_S (env, seconds, default 0): the owner's extra time on top of the +35% cap (cap = 1.35 B + SLACK_S). It enters k,
the finish offset and the guard offset (and so the A-2 reader k); the 1.5 B hang guard is not derived from the cap and is unchanged.
With a non-zero value the values files live in values-slack<S>/<panel>/ (never in values/) and carry "slack_s".
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import statistics
import sys

R1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKGS = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
G_EL2 = 47.0


def slack_s() -> float:
    """PANEL_SLACK_S, read at call time; 0 when unset."""
    v = float(os.environ.get("PANEL_SLACK_S", "0") or "0")
    if v < 0:
        raise SystemExit("PANEL_SLACK_S must be >= 0")
    return v


def values_dir() -> str:
    s = slack_s()
    return "values" if s == 0 else f"values-slack{s:g}"


def _floor(x: float) -> int:
    return math.floor(round(x, 9))  # 0.35 * 238 - ... must not land on 0.9999999


def k_for(B: float, turn: float, trep: float) -> int:
    """R-42: k = max(0, min(2, floor((0.35 B + SLACK_S - 2 - turn - T_report) / (2 turn))))."""
    return max(0, min(2, _floor((0.35 * B + slack_s() - 2 - turn - trep) / (2 * turn))))


def finish_offset(B: float, turn: float, trep: float) -> float:
    """PANEL_FINISH_AT - T0 = 1.35 B + SLACK_S - turn_p90[crit] - T_report_p90[crit]."""
    return 1.35 * B + slack_s() - turn - trep


def guard_g(panel: str, turn_crit: float) -> float:
    """G = 47 s on el2; Adaptation A-3: 47 x turn_p90[crit] / 6.4 on sl2 and hl2."""
    return G_EL2 if panel == "el2" else G_EL2 * turn_crit / 6.4


def guard_offset(B: float, finish_off: float, G: float) -> float:
    return min(1.35 * B + slack_s() - G, finish_off)


def reader_k_a2(finish_off: float, e_reader: float, turn_reader: float) -> int:
    """Adaptation A-2 (sl2, hl2 only): the off-path luna role gets its own k from its p90 end time."""
    return max(0, min(2, _floor((finish_off - e_reader - 2) / (2 * turn_reader))))


CAP_EXC_HANG_X = 3.0  # time-cap exception (OVERRIDE.md): hang guard = max(existing, 3.0 x B_f)


def cap_exception(v: dict, forced: int) -> tuple[dict, dict]:
    """Owner-authorised exception to the +35% rule (OVERRIDE.md, 2026-11-14). Returns (values to use, record).

    Off (forced == 0), or no role with a measured k of 0: `v` comes back unchanged (the same object). On: every role whose measured k
    is 0 gets k = forced; roles with a measured k >= 1 keep it. The hang guard becomes max(hang, 3.0 x B_f), and the finish offset
    and the injection guard move with it: finish' = finish + (hang' - hang), guard' = finish' (the original guard headroom G was
    derived from the waived cap; the finish signal stays the last point for an injection). The values file is never rewritten.
    """
    k0 = dict(v["k"])
    roles = sorted(r for r, n in k0.items() if n == 0) if forced else []
    if not roles:
        return v, {"forced_k": forced, "k_measured": k0, "forced_roles": []}
    hang = max(v["hang_offset_s"], CAP_EXC_HANG_X * v["B_f"])
    fin = v["finish_offset_s"] + (hang - v["hang_offset_s"])
    out = dict(v, k={r: (forced if n == 0 else n) for r, n in k0.items()}, hang_offset_s=hang, finish_offset_s=fin, guard_offset_s=fin)
    return out, {"forced_k": forced, "k_measured": k0, "forced_roles": roles, "hang_offset_s_orig": v["hang_offset_s"],
                 "finish_offset_s_orig": v["finish_offset_s"], "guard_offset_s_orig": v["guard_offset_s"]}


def compute(panel: str, cfg: dict, B: float, turn: dict, trep: dict, e: dict) -> dict:
    crit = cfg["critical_role"]
    fin = finish_offset(B, turn[crit], trep[crit])
    k = {crit: k_for(B, turn[crit], trep[crit])}
    other = "searcher" if crit == "reader" else "reader"
    if panel == "el2":
        k[other] = k[crit]  # R-42 verbatim on el2
    else:
        k[other] = reader_k_a2(fin, e["reader"], turn["reader"])
    return {"critical_role": crit, "finish_offset_s": fin, "guard_offset_s": guard_offset(B, fin, guard_g(panel, turn[crit])),
            "hang_offset_s": 1.5 * B, "k": k, "slack_s": slack_s()}


def planning(panel: str, cfg: dict) -> dict:
    crit = cfg["critical_role"]
    turn = {r: cfg["roles"][r]["planning_turn"] for r in ("searcher", "reader")}
    trep = dict(turn)
    trep[crit] = cfg["planning_T_report"]
    e = {"reader": cfg["planning_reader_end"], "searcher": None}
    v = compute(panel, cfg, cfg["planning_B"], turn, trep, e)
    v.update({"panel": panel, "B_f": cfg["planning_B"], "turn_p90": turn, "T_report_p90": trep, "E_p90": e, "values": "planning"})
    return v


def p90(xs: list[float]) -> float:
    s = sorted(xs)
    return s[max(0, math.ceil(0.9 * len(s)) - 1)]


def _sec(ts: str) -> float:
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()


def turns_of(entries: list) -> tuple[list[float], float | None]:
    """(inner turn durations, final response duration) of one --output-format json transcript.

    Top-level entries only. A response is the group of assistant entries sharing message.id; its duration is its last
    timestamp minus the latest tool-result timestamp before it. The first response (no earlier tool result) is left
    out; the final response feeds only T_report.
    """
    groups: list[tuple[float | None, float]] = []
    last_tr: float | None = None
    cur_id = None
    for en in entries:
        if not isinstance(en, dict) or en.get("parent_tool_use_id") or not en.get("timestamp"):
            continue
        ts = _sec(en["timestamp"])
        msg = en.get("message") or {}
        if en.get("type") == "assistant":
            mid = msg.get("id")
            if groups and mid == cur_id:
                groups[-1] = (groups[-1][0], max(groups[-1][1], ts))
            else:
                groups.append((last_tr, ts))
                cur_id = mid
        elif en.get("type") == "user" and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in msg.get("content") or []):
            last_tr = ts if last_tr is None else max(last_tr, ts)
            cur_id = None
    durs = [(end - start) if start is not None else None for start, end in groups]
    if not durs:
        return [], None
    final = durs[-1]
    inner = [d for d in durs[:-1] if d is not None]
    return inner, final


def _root(argv: list[str]) -> tuple[list[str], str]:
    if "--root" in argv:
        i = argv.index("--root")
        return argv[:i] + argv[i + 2 :], argv[i + 1]
    return argv, R1


def spike4(panel: str, rows: list[str], root: str) -> int:
    if len(rows) < 3:
        print(f"REFUSE spike4 needs at least 3 collab-0 rows, got {len(rows)}", file=sys.stderr)
        return 2
    cfg = json.load(open(f"{root}/config/panels.json"))[panel]
    roles = {cfg["roles"]["searcher"]["rid"]: "searcher", **{r: "reader" for r in cfg["roles"]["reader"]["rids"]}}
    outs = [f"{root}/{values_dir()}/{panel}/{p}.json" for p in PKGS]
    if any(os.path.exists(o) for o in outs):
        print(f"REFUSE {values_dir()} file exists; values are written once", file=sys.stderr)
        return 2
    for p, out in zip(PKGS, outs):
        elapsed, turns, rep, ends = [], {"searcher": [], "reader": []}, {"searcher": [], "reader": []}, {"searcher": [], "reader": []}
        for row in rows:
            d = f"{root}/runs/{row}/{p}"
            t0 = json.load(open(f"{d}/run.json"))["T0_MS"]
            end_all = []
            for rid, role in roles.items():
                meta = json.load(open(f"{d}/reviews/{rid}.meta.json"))
                end_all.append(meta["end_ms"])
                ends[role].append((meta["end_ms"] - t0) / 1000)
                att = f"{d}/reviews/{rid}.attempt{meta['attempts']}.json"
                try:
                    entries = json.load(open(att))
                except (OSError, ValueError):
                    continue
                inner, final = turns_of(entries if isinstance(entries, list) else [])
                turns[role] += inner
                if final is not None:
                    rep[role].append(final)
            elapsed.append((max(end_all) - t0) / 1000)
        B = statistics.median(elapsed)
        tp = {r: p90(turns[r]) for r in turns}
        trp = {r: p90(rep[r]) for r in rep}
        ep = {r: p90(ends[r]) for r in ends}
        v = compute(panel, cfg, B, tp, trp, ep)
        v.update({"panel": panel, "pkg": p, "B_f": B, "turn_p90": tp, "T_report_p90": trp, "E_p90": ep,
                  "source_runs": rows, "computed_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
        os.makedirs(os.path.dirname(out), exist_ok=True)
        body = json.dumps(v, indent=1) + "\n"
        with open(out, "x") as f:
            f.write(body)
        with open(out + ".sha256", "x") as f:
            f.write(f"{hashlib.sha256(body.encode()).hexdigest()}  {os.path.basename(out)}\n")
        print(out)
    return 0


def load(panel: str, pkg: str, root: str) -> dict | None:
    """The values file when it exists and matches its .sha256, else None."""
    out = f"{root}/{values_dir()}/{panel}/{pkg}.json"
    if not os.path.exists(out):
        return None
    body = open(out, "rb").read()
    want = open(out + ".sha256").read().split()[0] if os.path.exists(out + ".sha256") else ""
    if hashlib.sha256(body).hexdigest() != want:
        raise SystemExit(f"values file {out} does not match its .sha256")
    v = json.loads(body)
    if v.get("slack_s", 0) != slack_s():
        raise SystemExit(f"values file {out} was computed with slack_s={v.get('slack_s', 0)}, PANEL_SLACK_S is {slack_s():g}")
    v["values"] = want
    return v


def deadlines(panel: str, pkg: str, collab: int, t0: int, root: str, cap_exc: int = 0) -> int:
    cfg = json.load(open(f"{root}/config/panels.json"))[panel]
    if cap_exc and collab != 1:
        print("REFUSE the time-cap exception applies only to collab 1 rows", file=sys.stderr)
        return 2
    v = load(panel, pkg, root)
    if v is None:
        if collab == 1 or slack_s() != 0:  # with slack there is no planning fallback, even for collab 0
            print(f"REFUSE PANEL_COLLAB={collab} PANEL_SLACK_S={slack_s():g} needs {values_dir()}/{panel}/{pkg}.json (Spike 4)", file=sys.stderr)
            return 2
        v = planning(panel, cfg)
        v["hang_offset_s"] = 2.0 * cfg["planning_B"]  # Spike 4 rows: wider guard so slow rows are not truncated
    info = None
    if cap_exc:
        v, info = cap_exception(v, cap_exc)
    out = {"values": v["values"], "B": v["B_f"], "k": v["k"], "T_report": v["T_report_p90"],
           "finish_offset_s": v["finish_offset_s"], "guard_offset_s": v["guard_offset_s"], "hang_offset_s": v["hang_offset_s"], "slack_s": slack_s(),
           "FINISH_MS": t0 + round(1000 * v["finish_offset_s"]), "GUARD_MS": t0 + round(1000 * v["guard_offset_s"]),
           "HANG_MS": t0 + round(1000 * v["hang_offset_s"])}
    if info is not None:  # only with the override on: an override-off output keeps exactly its old keys
        out["time_cap_exception"] = True
        out["cap_exception"] = info
    print(json.dumps(out))
    return 0


def main(argv: list[str]) -> int:
    argv, root = _root(argv)
    if argv[:1] == ["spike4"] and len(argv) >= 2:
        return spike4(argv[1], argv[2:], root)
    if argv[:1] == ["show"] and len(argv) == 3:
        v = load(argv[1], argv[2], root) or planning(argv[1], json.load(open(f"{root}/config/panels.json"))[argv[1]])
        print(json.dumps(v, indent=1))
        return 0
    if argv[:1] == ["deadlines"] and len(argv) in (5, 7) and (len(argv) == 5 or argv[5] == "--cap-exception"):
        return deadlines(argv[1], argv[2], int(argv[3]), int(argv[4]), root, int(argv[6]) if len(argv) == 7 else 0)
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
