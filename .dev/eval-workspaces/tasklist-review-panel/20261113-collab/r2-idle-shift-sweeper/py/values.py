"""Timing arithmetic (R-41, R-42, D-2), the Spike 4 reducer and manifest pinning.

compute: print one values JSON.   reduce: values inputs from A1 run dirs.   pin: write config/manifest.json.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import re
import statistics
import subprocess
import sys
from pathlib import Path

HOOKS_S = 2.0
EPS = 1e-9  # floor() guard: 12.8/12.8 computed in floats must give 1, not 0


def finish_at(B: float, turn_crit: float, report_crit: float) -> float:
    """panel_finish_at_s = 1.35 B_f - turn_p90_crit - T_report_p90_crit (offset from T0)."""
    return 1.35 * B - turn_crit - report_crit


def k(finish_s: float, e_recv: float, turn_recv: float, hooks: float = HOOKS_S) -> int:
    """D-2: k = max(0, min(2, floor((finish - E_recv - hooks) / (2 turn_recv))))."""
    return max(0, min(2, math.floor((finish_s - e_recv - hooks) / (2 * turn_recv) + EPS)))


def k_r42(B: float, turn: float, report: float, hooks: float = HOOKS_S) -> int:
    """R-42 literal form: floor((0.35 B - hooks - turn - report) / (2 turn))."""
    return max(0, min(2, math.floor((0.35 * B - hooks - turn - report) / (2 * turn) + EPS)))


def sweeper_kill(finish_s: float, turn_recv: float) -> float:
    return finish_s - 2 * turn_recv


def hang(B: float) -> float:
    return 1.5 * B


def compute(panel, pkg, B, turn_crit, report_crit, e_recv, turn_recv, report_recv, source="planning", n_runs=0) -> dict:
    f = finish_at(B, turn_crit, report_crit)
    return {
        "panel": panel, "pkg": pkg, "B_f": B,
        "turn_p90_crit": turn_crit, "T_report_p90_crit": report_crit,
        "E_recv": e_recv, "turn_p90_recv": turn_recv, "T_report_p90_recv": report_recv,
        "hooks_s": HOOKS_S, "panel_finish_at_s": round(f, 3), "k": k(f, e_recv, turn_recv),
        "sweeper_kill_s": round(sweeper_kill(f, turn_recv), 3), "hang_s": round(hang(B), 3),
        "source": source, "n_runs": n_runs,
    }


# ------------------------------------------------------------------ Spike 4 reducer

def p90(xs: list[float]) -> float | None:
    if not xs:
        return None
    xs = sorted(xs)
    return xs[min(len(xs) - 1, math.ceil(0.9 * len(xs)) - 1)]


def _ts(s: str) -> float:
    return _dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def turn_durations(transcript: Path) -> list[float]:
    """Gaps between consecutive assistant entries' timestamps in a persisted session transcript."""
    ts = []
    for line in transcript.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "assistant" and e.get("timestamp") and not e.get("isSidechain"):
            ts.append(_ts(e["timestamp"]))
    ts.sort()
    return [b - a for a, b in zip(ts, ts[1:]) if b > a]


def project_slug(cwd: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", cwd)


def reduce_runs(run_dirs: list[Path], panels: dict, projects: Path) -> dict:
    """Values inputs for one (panel, package) from n A1 package dirs (runs/<row>/<pkg>)."""
    elapsed, e_recv = [], []
    turns: dict[str, list[float]] = {}
    last: dict[str, list[float]] = {}
    panel = None
    for d in run_dirs:
        collab = json.loads((d / "collab.json").read_text())
        panel = collab["panel"]
        elapsed.append(collab["elapsed_s"])
        t0 = int((d / "t0").read_text())
        ends = []
        sb = (d / "sandbox").read_text().strip() if (d / "sandbox").exists() else None
        for r in panels[panel]["reviewers"]:
            meta = json.loads((d / "reviews" / f"{r['rid']}.meta.json").read_text())
            if r["model"] == "gpt-6-luna":
                ends.append((meta["end_ms"] - t0) / 1000)
            sid = meta.get("session_id")
            if sid and sb:
                tr = projects / project_slug(sb) / f"{sid}.jsonl"
                if tr.exists():
                    ds = turn_durations(tr)
                    turns.setdefault(r["model"], []).extend(ds)
                    if ds:
                        last.setdefault(r["model"], []).append(ds[-1])
        if ends:
            e_recv.append(max(ends))
    crit = panels[panel]["critical_role"]
    return {
        "panel": panel, "n_runs": len(run_dirs), "B_f": statistics.median(elapsed),
        "E_recv": statistics.median(e_recv) if e_recv else None,
        "turn_p90_crit": p90(turns.get(crit, [])), "T_report_p90_crit": p90(last.get(crit, [])),
        "turn_p90_recv": p90(turns.get("gpt-6-luna", [])), "T_report_p90_recv": p90(last.get("gpt-6-luna", [])),
    }


# ------------------------------------------------------------------ manifest

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pin(r2: Path, repo: Path, eval_dir: Path, out: Path) -> dict:
    panels = json.loads((r2 / "config/panels.json").read_text())
    base = {}
    for pkg in panels["packages"]:
        c = subprocess.run(["git", "-C", str(repo), "log", "--reverse", "--format=%H", "--",
                            f".dev/tasks/to-do/{pkg}", f".dev/tasks/done/{pkg}"],
                           capture_output=True, text=True, check=True).stdout.split()[0]
        base[pkg] = subprocess.run(["git", "-C", str(repo), "rev-parse", f"{c}^1"],
                                   capture_output=True, text=True, check=True).stdout.strip()
    shas = {
        "judge-one.sh": sha256(eval_dir / "tools/tmp-scripts/judge-one.sh"),
        "catalogue.json": sha256(r2 / "config/catalogue.json"),
        "brief_a1": sha256(r2 / "config/brief-a1.tmpl"),
        "sweeper_brief": sha256(r2 / "config/sweeper-brief.tmpl"),
    }
    for f in sorted((r2 / "config/values").glob("*/*.json")):
        shas[f"values/{f.parent.name}/{f.name}"] = sha256(f)
    m = {"base_sha": base,
         "base_rule": "first parent of the squash commit that first added the package folder",
         "sha256": shas,
         "committed_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    out.write_text(json.dumps(m, indent=1) + "\n")
    return m


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compute")
    for a in ("panel", "pkg"):
        c.add_argument(f"--{a}", required=True)
    for a in ("B", "turn-crit", "report-crit", "e-recv", "turn-recv", "report-recv"):
        c.add_argument(f"--{a}", type=float, required=True)
    c.add_argument("--source", default="planning")
    c.add_argument("--n-runs", type=int, default=0)
    r = sub.add_parser("reduce")
    r.add_argument("--runs", nargs="+", required=True)
    r.add_argument("--panels", required=True)
    r.add_argument("--projects", default=str(Path.home() / ".claude/projects"))
    r.add_argument("--pkg")
    r.add_argument("--out")
    p = sub.add_parser("pin")
    p.add_argument("--r2", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--eval", required=True)
    p.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "compute":
        print(json.dumps(compute(a.panel, a.pkg, a.B, a.turn_crit, a.report_crit, a.e_recv,
                                 a.turn_recv, a.report_recv, a.source, a.n_runs)))
    elif a.cmd == "reduce":
        inp = reduce_runs([Path(x) for x in a.runs], json.loads(Path(a.panels).read_text()), Path(a.projects))
        missing = [x for x in ("B_f", "E_recv", "turn_p90_crit", "T_report_p90_crit", "turn_p90_recv", "T_report_p90_recv") if inp[x] is None]
        if missing:
            print(json.dumps({"error": "missing inputs", "missing": missing, "inputs": inp}))
            return 1
        v = compute(inp["panel"], a.pkg or "", inp["B_f"], inp["turn_p90_crit"], inp["T_report_p90_crit"],
                    inp["E_recv"], inp["turn_p90_recv"], inp["T_report_p90_recv"], "spike4", inp["n_runs"])
        s = json.dumps(v)
        if a.out:
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_text(s + "\n")
        print(s)
    else:
        print(json.dumps(pin(Path(a.r2), Path(a.repo), Path(a.eval), Path(a.out))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
