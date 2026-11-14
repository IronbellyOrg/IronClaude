"""Values file, n, k and finish time (sections 6.5 and 14)."""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import math
import os
from pathlib import Path

from . import paths

EPS = 1e-9


def _floor(x: float) -> int:
    return math.floor(x + EPS)


def slack_s() -> float:
    """Owner decision 2026-11-14: the time cap is 1.35 x B + SLACK_S. Env PANEL_SLACK_S, default 0."""
    raw = os.environ.get("PANEL_SLACK_S", "").strip()
    if not raw:
        return 0.0
    try:
        s = float(raw)
    except ValueError:
        raise SystemExit(f"E_SLACK: PANEL_SLACK_S={raw!r} is not a number") from None
    if not math.isfinite(s) or s < 0:
        raise SystemExit(f"E_SLACK: PANEL_SLACK_S={raw!r} must be a finite number >= 0")
    return s


def slack_tag(s: float | None = None) -> str:
    """Folder suffix of the slack values files: 30 -> 'slack30'."""
    s = slack_s() if s is None else s
    return f"slack{s:g}"


def compute_n(T0, B_f, t_launch, box_cap, cap, start_cost, turn_p90) -> int:
    """6.5: n per launch attempt; all arithmetic on times relative to T0.

    The phase-2 box is the 30% share of the 35% cap, so SLACK_S widens it (and its
    fixed cap) by the same amount as the deadline in lib/package.sh.
    """
    s = slack_s()
    box = 1.30 * B_f + s - (t_launch - T0)
    if box_cap is not None:
        box = min(box_cap + s, box)
    return max(0, min(cap, _floor((box - start_cost) / (2 * turn_p90))))


def compute_k(B, turn_p90, T_report_p90, hooks=2.0) -> int:
    return max(
        0,
        min(
            2,
            _floor(
                (0.35 * B + slack_s() - hooks - turn_p90 - T_report_p90)
                / (2 * turn_p90)
            ),
        ),
    )


def finish_offset(B, turn_p90, T_report_p90) -> float:
    return 1.35 * B + slack_s() - turn_p90 - T_report_p90


def finish_at(T0, B, turn_p90, T_report_p90) -> float:
    return T0 + finish_offset(B, turn_p90, T_report_p90)


# ---- owner-authorised time-cap exception (2026-11-14, OVERRIDE.md). Default off: nothing above changes.
TCE_HANG_MULT = 3.0  # hang guard = max(1.5 x B_f, 3.0 x B_A1)
TCE_FALLBACK_START = 16.0  # a fresh fallback start costs 16 s (DESIGN 6.5)


def tce_forced() -> int:
    """Env TIME_CAP_EXCEPTION: unset or 0 = off; 1..3 = forced n per receiver (bounded by its cap)."""
    raw = os.environ.get("TIME_CAP_EXCEPTION", "").strip()
    if raw in ("", "0"):
        return 0
    if raw not in ("1", "2", "3"):
        raise SystemExit(
            f"E_TCE: TIME_CAP_EXCEPTION={raw!r}; allowed: unset, 0 (off), 1, 2 or 3"
        )
    return int(raw)


def tce_plan(forced: int, panel: str, pkg: str, v: dict, b_a1: float, src: str) -> dict:
    """Exception numbers for one package. v = the loaded values; b_a1 = frozen baseline B_A1 of the package."""
    pc = paths.cfg("panels.json")[panel]
    crit = (
        pc["readers"][0]["model"]
        if pc["critical_role"] == "readers"
        else pc["searcher"]["model"]
    )
    p = v["packages"][pkg]
    tmax = max(v["turn_p90"].values())
    hang = max(1.5 * p["B_f"], TCE_HANG_MULT * b_a1)
    p2 = max(
        1.30 * p["B_f"] + float(v.get("slack_s", 0)),
        hang + TCE_FALLBACK_START + 2 * forced * tmax,
    )
    fin = max(
        p["panel_finish_offset_s"], hang - v["turn_p90"][crit] - p["T_report_p90"]
    )
    return {
        "on": True,
        "forced_n": forced,
        "B_A1": b_a1,
        "B_A1_source": src,
        "hang_offset_s": hang,
        "p2_deadline_offset_s": p2,
        "finish_offset_s": fin,
        "finish_offset_cap_s": p["panel_finish_offset_s"],
        "k_measured": p["k"],
    }


def tce_all(forced: int, panel: str, v: dict) -> dict:
    """tce_plan for every package of v. B_A1 comes from the frozen values file of the panel when it exists
    (smoke runs load planning values otherwise), else from v itself."""
    f = paths.values_file(panel)
    frozen = paths.load_json(f)["packages"] if f.exists() else {}
    out = {}
    for pkg, p in v["packages"].items():
        b, src = (
            (frozen[pkg]["B_f"], "frozen")
            if pkg in frozen
            else (p["B_f"], v.get("status", "planning"))
        )
        out[pkg] = tce_plan(forced, panel, pkg, v, b, src)
    return out


def tce_floor_n(
    n: int, tce: dict | None, t_rel: float, start_cost: float, turn_p90: float, cap: int
) -> int:
    """Raise a measured n of 0 to the forced n while the widened phase-2 deadline still has room for it."""
    if not tce or n > 0:
        return n
    f = min(cap, int(tce["forced_n"]))
    room = tce["p2_deadline_offset_s"] - t_rel - start_cost
    return f if f > 0 and room >= 2 * f * turn_p90 else n


def p90(xs):
    xs = sorted(xs)
    if not xs:
        return None
    return xs[max(0, math.ceil(0.9 * len(xs)) - 1)]


def _ts(s: str) -> float:
    return _dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def turn_durations(session_jsonl) -> list[float]:
    """Each assistant entry's timestamp minus the timestamp of the entry just before it."""
    out, prev = [], None
    for line in Path(session_jsonl).read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = e.get("timestamp")
        if not isinstance(t, str):
            continue
        ts = _ts(t)
        if e.get("type") == "assistant" and prev is not None:
            out.append(ts - prev)
        prev = ts
    return out


def sha256_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def planning(panel: str) -> dict:
    pk = paths.cfg("packages.json")
    pn = paths.cfg("panels.json")[panel]
    turns = dict(pk["planning_turn_p90"])
    crit = (
        pn["readers"][0]["model"]
        if pn["critical_role"] == "readers"
        else pn["searcher"]["model"]
    )
    pkgs = {}
    for pid, p in pk["packages"].items():
        B = float(p["planning_B"][panel])
        t = turns[crit]
        pkgs[pid] = {
            "B_f": B,
            "T_report_p90": t,
            "k": compute_k(B, t, t),
            "panel_finish_offset_s": finish_offset(B, t, t),
        }
    return {
        "schema": "r3-values/1",
        "panel": panel,
        "status": "planning",
        "source_runs": [],
        "frozen_at": None,
        "slack_s": slack_s(),
        "turn_p90": turns,
        "packages": pkgs,
        "slowdown_s": None,
    }


def load(
    panel: str, smoke: bool = False, spike4: bool = False, prefer_frozen: bool = False
) -> tuple[dict, str | None]:
    """Return (values, sha256 or None). Frozen file required unless smoke or spike4.

    prefer_frozen (only the time-cap exception sets it): a smoke run uses the frozen file when one exists,
    so the forced n is exercised on the measured numbers; otherwise smoke uses planning values (A10).
    """
    if smoke and not prefer_frozen:
        return planning(panel), None  # A10: smoke runs use planning values
    f = paths.values_file(panel)
    if f.exists():
        v = paths.load_json(f)
        sha = sha256_file(f)
        shaf = Path(str(f) + ".sha256")
        if (
            v.get("status") == "frozen"
            and shaf.exists()
            and shaf.read_text().split()[0] == sha
        ):
            if float(v.get("slack_s", 0)) != slack_s():
                raise SystemExit(
                    f"E_VALUES: {f} was frozen with slack_s={v.get('slack_s', 0)} "
                    f"but PANEL_SLACK_S={slack_s():g}"
                )
            return v, sha
        if not (smoke or spike4):
            raise SystemExit(
                f"E_VALUES: {f} is not frozen or its sha256 does not match"
            )
    elif not (smoke or spike4):
        raise SystemExit(
            f"E_VALUES: {f} missing (only R3_SMOKE=1 or R3_SPIKE4=1 may run without it)"
            + (
                f"; PANEL_SLACK_S={slack_s():g} needs the slack values "
                f"(r3_py values-freeze --panel {panel} --runs <spike-4 run ids>)"
                if slack_s()
                else ""
            )
        )
    return planning(panel), None


def freeze(panel: str, run_dirs: list) -> dict:
    """14.2. Refuses fewer than 3 runs, an invalid package, or an existing frozen file."""
    f = paths.values_file(panel)
    if f.exists():
        raise SystemExit(
            f"refused: {f} exists; a person must move it aside first (R-30)"
        )
    if len(run_dirs) < 3:
        raise SystemExit(f"refused: need at least 3 Spike-4 runs, got {len(run_dirs)}")
    pn = paths.cfg("panels.json")[panel]
    model_of = {pn["searcher"]["rid"]: pn["searcher"]["model"]}
    model_of.update({r["rid"]: r["model"] for r in pn["readers"]})
    crit_rids = (
        [r["rid"] for r in pn["readers"]]
        if pn["critical_role"] == "readers"
        else [pn["searcher"]["rid"]]
    )
    crit_model = model_of[crit_rids[0]]
    elapsed: dict[str, list] = {}
    turns: dict[str, list] = {}
    last_turn: dict[str, list] = {}
    for rd in map(Path, run_dirs):
        run = paths.load_json(rd / "run.json")
        if run.get("panel") != panel:
            raise SystemExit(f"refused: {rd} is panel {run.get('panel')}")
        for pkgdir in sorted(
            p for p in rd.iterdir() if p.is_dir() and p.name.startswith("TASK-WF-")
        ):
            pj = paths.load_json(pkgdir / "pkg.json")
            if not pj.get("valid", False):
                raise SystemExit(
                    f"refused: {pkgdir} is invalid ({pj.get('invalid_reason')})"
                )
            cj = paths.load_json(pkgdir / "collab.json")
            elapsed.setdefault(pkgdir.name, []).append(cj["panel"]["elapsed_s"])
            for rid, model in model_of.items():
                s = pkgdir / "reviews" / f"{rid}.p1.session.jsonl"
                if not s.exists():
                    continue
                d = turn_durations(s)
                turns.setdefault(model, []).extend(d)
                if rid in crit_rids and d:
                    last_turn.setdefault(pkgdir.name, []).append(d[-1])
    tp = {m: p90(v) for m, v in turns.items() if v}
    if crit_model not in tp:
        raise SystemExit("refused: no transcript turns for the critical model")
    pkgs = {}
    for pid, xs in elapsed.items():
        xs = sorted(xs)
        mid = len(xs) // 2
        B = xs[mid] if len(xs) % 2 else (xs[mid - 1] + xs[mid]) / 2
        tr = p90(last_turn.get(pid, [])) or tp[crit_model]
        pkgs[pid] = {
            "B_f": B,
            "T_report_p90": tr,
            "k": compute_k(B, tp[crit_model], tr),
            "panel_finish_offset_s": finish_offset(B, tp[crit_model], tr),
        }
    v = {
        "schema": "r3-values/1",
        "panel": panel,
        "status": "frozen",
        "source_runs": [Path(r).name for r in run_dirs],
        "frozen_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "slack_s": slack_s(),
        "turn_p90": tp,
        "packages": pkgs,
        "slowdown_s": None,
    }
    paths.write_json(f, v)
    Path(str(f) + ".sha256").write_text(sha256_file(f) + "\n")
    return v
