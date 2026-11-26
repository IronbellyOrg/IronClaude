"""Results row (DESIGN 5.4). Definitions follow EVAL/analysis/final-table.py: defect-rich = designSpec + alias,
control = design; real blocking = judge-blocking AND blocking_in_implement in the ground truth.

results_row.py --row <row> --opaque <id> --out results/<row>.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import R2  # noqa: E402

CONTROL = "TASK-WF-design-20261108-041415"
OUT = Path(os.environ.get("R2_OUT") or R2)
EVAL = Path(os.environ.get("R2_EVAL") or R2.parents[1] / "20261111-a1")


def jload(p: Path, default=None):
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return default


def rtext(p: Path) -> str | None:
    return p.read_text().strip() if p.exists() else None


def api_error(d: Path) -> bool:
    j = jload(d / "judge.json")
    texts = []
    if isinstance(j, list):
        texts += [str(e.get("result", "")) for e in j if isinstance(e, dict) and e.get("type") == "result"]
    elif isinstance(j, dict):
        texts.append(str(j.get("result", "")))
    if (d / "score.json").exists():
        texts.append((d / "score.json").read_text())
    return any("API Error" in t for t in texts)


def build(row: str, opaque: str) -> dict:
    rd = OUT / "runs" / row
    panel = rtext(rd / "panel")
    panels = json.loads((R2 / "config/panels.json").read_text())
    pkgs = [p for p in panels["packages"] if (rd / p).is_dir()]
    invalid = []
    exception = (rd / "time_cap_exception").exists()  # written by launch-panel.sh when TIME_CAP_EXCEPTION=1
    per, coll, elapsed, overhead, vsha = {}, [], {}, {}, {}
    tok = {"reviewers": 0, "sweeper": 0, "reask": 0}
    for pkg in pkgs:
        pd = rd / pkg
        c = jload(pd / "collab.json", {}) or {}
        coll.append((pkg, c))
        valid = (pd / "DONE").exists() and not (pd / "INVALID").exists()
        if (pd / "INVALID").exists():
            invalid += [f"{pkg}: {x}" for x in (pd / "INVALID").read_text().splitlines()]
        audit_ok = bool((jload(pd / "audit.json", {}) or {}).get("ok", False))
        if not audit_ok:
            invalid.append(f"{pkg}: audit not ok")
        label = (jload(OUT / "scoring" / opaque / pkg / "label-key.json", {}) or {}).get("label")
        sd = OUT / "scoring" / opaque / pkg / (label or "_none")
        score = jload(sd / "score.json")
        apierr = api_error(sd) if label else False
        if score is None:
            invalid.append(f"{pkg}: unscored")
        if apierr:
            invalid.append(f"{pkg}: judge API Error (score excluded)")
            score = None
        if not (pd / "merged-1.md").exists():
            invalid.append(f"{pkg}: not merged")
        for f in sorted((pd / "reviews").glob("*.cost.json")):
            cj = jload(f, {}) or {}
            tok["reviewers"] += int(cj.get("total_output_tokens_all", 0)) - int(cj.get("reask_output_tokens", 0))
            tok["reask"] += int(cj.get("reask_output_tokens", 0))
        tok["sweeper"] += int((jload(pd / "sweeper/sw-1.meta.json", {}) or {}).get("output_tokens") or 0)
        elapsed[pkg] = c.get("elapsed_s")
        overhead[pkg] = c.get("overhead_pct")
        vsha[pkg] = c.get("values_sha256")
        sw = c.get("sweeper") or {}
        per[pkg] = {
            "gt_covered_any": score.get("gt_covered_any") if score else None,
            "gt_covered_blocking": score.get("gt_covered_blocking") if score else None,
            "wrong_blockers": score.get("wrong_blockers") if score else None,
            "ledger_rows": c.get("ledger_rows"), "label": label, "score_ok": score is not None,
            "judge_api_error": apierr, "valid": valid, "audit_ok": audit_ok,
            "slo_breach": bool(c.get("slo_breach")), "elapsed_s": c.get("elapsed_s"), "k": c.get("k"),
            "facts_posted": sw.get("facts_posted", 0), "facts_harvested": sw.get("facts_harvested", 0),
            "facts_delivered": {r: v["msgs_received"] for r, v in (c.get("reviewers") or {}).items() if v["role"] == "receiver"},
            "snapshot_missing": sum(bool(v.get("snapshot_missing")) for v in (c.get("reviewers") or {}).values()),
            "receivers": sum(v["role"] == "receiver" for v in (c.get("reviewers") or {}).values()),
            # owner-authorised time-cap exception columns (OVERRIDE.md); B_A1 is the Spike 4 baseline of this package
            "time_cap_exception": bool(c.get("time_cap_exception")),
            "time_cap_exception_applied": bool(c.get("time_cap_exception_applied")),
            "B_A1": c.get("B_A1"), "elapsed_over_baseline": c.get("elapsed_over_baseline"),
            "k_measured": c.get("k_measured"),
            "messages_delivered": c.get("messages_delivered"),
        }
        if exception and not c.get("time_cap_exception"):
            invalid.append(f"{pkg}: time_cap_exception row but the package values carry no exception stamp")

    def gt_items(pkg):
        g = jload(EVAL / pkg / "ground-truth.json", {"items": []})
        return {it["id"]: it for it in g["items"]}

    rich = [p for p in pkgs if p != CONTROL]
    rich_scored = rich and all(per[p]["score_ok"] for p in rich)
    found = real = jb = wrong = None
    if rich_scored:
        found = sum(len(per[p]["gt_covered_any"]) for p in rich)
        jb = sum(len(per[p]["gt_covered_blocking"]) for p in rich)
        wrong = sum(per[p]["wrong_blockers"] for p in rich)
        real = sum(1 for p in rich for g in per[p]["gt_covered_blocking"]
                   if gt_items(p).get(g, {}).get("blocking_in_implement") is True)
    ctl = per.get(CONTROL)
    cf = len(ctl["gt_covered_any"]) if ctl and ctl["score_ok"] else None
    cw = ctl["wrong_blockers"] if ctl and ctl["score_ok"] else None

    def s(key, sub="reviewers"):
        return sum(int(v.get(key) or 0) for _, c in coll for v in (c.get(sub) or {}).values())

    collab = {
        "k": {p: c.get("k") for p, c in coll},
        "facts_posted": sum((c.get("sweeper") or {}).get("facts_posted", 0) for _, c in coll),
        "facts_harvested": sum((c.get("sweeper") or {}).get("facts_harvested", 0) for _, c in coll),
        "facts_rejected": sum((c.get("sweeper") or {}).get("facts_rejected", 0) for _, c in coll),
        "over_cap": sum((c.get("sweeper") or {}).get("over_cap", 0) for _, c in coll),
        "witness_facts": sum((c.get("sweeper") or {}).get("witness_facts", 0) for _, c in coll),
        "facts_delivered": {r: sum(per[p]["facts_delivered"].get(r, 0) for p in pkgs) for r in ("t4-1", "t3-1")},
        "late": s("late"), "not_delivered_cap": s("not_delivered_cap"),
        "isolated_for": {p: c.get("isolated_for", []) for p, c in coll},
        "snapshot_missing": sum(per[p]["snapshot_missing"] for p in pkgs),
        "finish_signal_fired": sum(1 for _, c in coll for v in (c.get("reviewers") or {}).values() if v.get("finish_signal_t")),
        "finish_would_fire": sum(1 for _, c in coll for v in (c.get("reviewers") or {}).values() if v.get("finish_would_fire")),
        "hook_error": s("hook_error"),
        "hook_ms_p95": max([v["hook_ms_p95"] for _, c in coll for v in (c.get("reviewers") or {}).values()
                            if v.get("hook_ms_p95") is not None], default=None),
        "peer_lines": s("peer_lines"), "peer_lines_first_hand": s("peer_lines_first_hand"),
        "reruns": s("reruns"), "rerun_mismatches": s("rerun_mismatches"),
        "cmd_unrun": sum((c.get("sweeper") or {}).get("cmd_unrun", 0) for _, c in coll),
        "echo_rate": {p: c.get("echo_rate") for p, c in coll},
        "own_line_jaccard": {p: c.get("own_line_jaccard") for p, c in coll},
        "sweeper_start_t_s": {p: (round(((c.get("sweeper") or {}).get("start_t") - int((rd / p / "t0").read_text())) / 1000, 3)
                                  if (c.get("sweeper") or {}).get("start_t") else None) for p, c in coll},
        "hang_kill": sum(1 for _, c in coll for v in (c.get("reviewers") or {}).values() if v.get("hang_kill")),
        "slo_breach": sum(bool(c.get("slo_breach")) for _, c in coll),
        "retry_isolated": sum(1 for _, c in coll for v in (c.get("reviewers") or {}).values() if v.get("retry_isolated")),
        "reask_count": sum(1 for p in pkgs for m in (rd / p / "reviews").glob("*.reask.jsonl")),
        "dropped_lines": s("dropped_lines"),
    }
    models = {}
    for r in panels.get(panel, {}).get("reviewers", []):
        models[r["rid"]] = r["model"]
    collab_flag = rtext(rd / "panel_collab")
    finished = jload(rd / "finished_at.json", {}) or {}
    return {
        "schema": "r2-results/1", "row": row, "arm": "F4" if collab_flag == "1" else "A1", "panel": panel,
        "panel_collab": int(collab_flag) if collab_flag else None, "models": models,
        "sweeper_model": rtext(rd / "sweeper_model"), "planning": (rd / "planning").exists(),
        "time_cap_exception": exception,
        "values_sha256": vsha, "opaque": opaque, "started_at": rtext(rd / "started_at"),
        "finished_at": finished.get("t") or rtext(rd / "finished_at"),
        "found_14": found, "real_blocking_8": real, "judge_blocking": jb, "wrong_blockers": wrong,
        "control_found_2": cf, "control_wrong_blockers": cw,
        "output_tokens": {"total": sum(tok.values()), **tok},
        "elapsed_s": elapsed, "overhead_pct": overhead, "per_package": per, "collab": collab,
        "invalid": invalid,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--row", required=True)
    ap.add_argument("--opaque", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", a.row):
        print("bad row", file=sys.stderr)
        return 2
    row = build(a.row, a.opaque)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(row, indent=1) + "\n")
    print(json.dumps({"invalid": row["invalid"], "found_14": row["found_14"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
