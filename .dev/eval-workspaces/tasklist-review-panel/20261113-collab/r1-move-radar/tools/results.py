"""results.py: the results row of one launch (DESIGN.md section 5.4, schema r1-results/1).

Usage (from REPO): uv run python tools/results.py <row> [--root R1] [--a1 A1DIR]
Reads runs/<row>/<pkg>/{status,run.json,collab.json,audit.json,label-key.json,reviews/*.cost.json,reviews/*.meta.json},
the judge's scoring/<opaque>/<pkg>/<L>/score.json and A1DIR/<pkg>/ground-truth.json (id and blocking_in_implement only).
Writes results/<row>.json and appends one line to results/results.jsonl; refuses (exit 2) a row id already there.
Definitions as A1DIR/analysis/final-table.py:31-37: any = |gt_covered_any|, jb = |gt_covered_blocking|,
rb = judge-blocking items whose blocking_in_implement is true, wb = wrong_blockers.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

REPO = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel"
R1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A1DIR = f"{REPO}/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
PKGS = [DS, AL, DE]


def load(p, default=None):
    try:
        return json.load(open(p))
    except (OSError, ValueError):
        return default


def package(root: str, a1: str, row: str, pkg: str) -> tuple[dict, dict | None]:
    d = f"{root}/runs/{row}/{pkg}"
    if not os.path.isdir(d):
        return {"status": "not_run"}, None
    status = open(f"{d}/status").read().strip() if os.path.exists(f"{d}/status") else "invalid"
    c = load(f"{d}/collab.json", {}) or {}
    run = load(f"{d}/run.json", {}) or {}
    key = load(f"{d}/label-key.json")
    score = load(f"{root}/scoring/{key['opaque']}/{pkg}/{key['label']}/score.json") if key else None
    if status == "ok" and score is None:
        status = "judge_failed"
    costs = [load(f, {}) for f in glob.glob(f"{d}/reviews/*.cost.json")]
    metas = [load(f, {}) for f in glob.glob(f"{d}/reviews/*.meta.json") if ".attempt" not in f]
    out = {"status": status, "label": key["label"] if key else None,
           "ledger_rows": c.get("ledger_rows"), "output_tokens": sum(x.get("total_output_tokens_all", 0) for x in costs),
           "elapsed_s": c.get("elapsed_s"), "B_f": c.get("baseline_elapsed_s"), "overhead_pct": c.get("overhead_pct"),
           "slo_breach": c.get("slo_breach"), "k": run.get("k"), "values": run.get("values"),
           "dropped_lines": sum(m.get("dropped_lines") or 0 for m in metas),
           "reask": sum(1 for m in metas if m.get("reask_s") is not None),
           "retry_isolated": sum(1 for m in metas if m.get("retry_isolated")),
           "hang_kill": sum(1 for m in metas if m.get("hang_kill")),
           "gt_covered_any": None, "real_blocking": None, "judge_blocking": None, "wrong_blockers": None}
    if status == "ok":
        gt = {i["id"]: i["blocking_in_implement"] for i in load(f"{a1}/{pkg}/ground-truth.json")["items"]}
        out.update({"gt_covered_any": score["gt_covered_any"], "judge_blocking": score["gt_covered_blocking"],
                    "real_blocking": [g for g in score["gt_covered_blocking"] if gt.get(g)], "wrong_blockers": score["wrong_blockers"]})
    return out, c


def build(row: str, root: str, a1: str) -> dict:
    m = re.fullmatch(r"(el2|sl2|hl2)-c([01])-r(\d+)", row)
    if not m:
        raise SystemExit(f"bad row id {row}")
    panel, collab, rep = m.group(1), int(m.group(2)), int(m.group(3))
    cfg = json.load(open(f"{root}/config/panels.json"))[panel]["roles"]
    models = {cfg["searcher"]["rid"]: cfg["searcher"]["model"], **{r: cfg["reader"]["model"] for r in cfg["reader"]["rids"]}}
    rowrun = load(f"{root}/runs/{row}/run.json", {}) or {}
    pk, cj = {}, {}
    for p in PKGS:
        pk[p], cj[p] = package(root, a1, row, p)
    ok = {p: pk[p]["status"] == "ok" for p in PKGS}

    def total(ps, f):
        return sum(f(pk[p]) for p in ps) if all(ok[p] for p in ps) else None

    cnt = {"injections": 0, "injections_by_move": {}, "src_checks": 0, "search_injections": 0, "static_injections": 0,
           "observable_moves_executed": 0, "skips_no_gap": 0, "skips_guard": 0, "finish_signals": 0, "finish_would_fire": 0,
           "hook_calls": 0, "hook_errors": 0, "hook_ms_p95": None, "snapshot_missing": 0, "late": 0, "receivers": 0,
           "leak_violations": 0, "moves_covered_panel": {}, "own_line_jaccard": {}}
    for p in PKGS:
        c = cj[p]
        if not c:
            continue
        a = load(f"{root}/runs/{row}/{p}/audit.json", {}) or {}
        cnt["leak_violations"] += a.get("leak_violations", 0)
        for s in c.get("slots", []):
            cnt["injections"] += 1
            cnt[{"src": "src_checks", "search": "search_injections", "static": "static_injections"}[s["slot_type"]]] += 1
            if s["move"]:
                cnt["injections_by_move"][s["move"]] = cnt["injections_by_move"].get(s["move"], 0) + 1
            cnt["observable_moves_executed"] += 1 if s.get("move_executed") is True else 0
        for r, rv in c.get("reviewers", {}).items():
            met = []
            mp = f"{root}/runs/{row}/{p}/board/metrics/{r}.jsonl"
            for ln in open(mp).read().splitlines() if os.path.exists(mp) else []:
                try:
                    v = json.loads(ln)
                except ValueError:
                    continue
                if isinstance(v, dict):
                    met.append(v)
            cnt["skips_no_gap"] += sum(1 for e in met if e.get("ev") == "skip" and e.get("reason") == "no_gap")
            cnt["skips_guard"] += sum(1 for e in met if e.get("ev") == "skip" and e.get("reason") == "guard")
            cnt["finish_signals"] += 1 if rv.get("finish_signal_t") else 0
            cnt["finish_would_fire"] += 1 if rv.get("finish_would_fire") else 0
            cnt["hook_calls"] += rv.get("hook_calls") or 0
            cnt["hook_errors"] += rv.get("hook_error") or 0
            cnt["snapshot_missing"] += rv.get("snapshot_missing") or 0
            cnt["late"] += rv.get("late") or 0
            cnt["receivers"] += 1 if (rv.get("k") or 0) > 0 else 0
            if rv.get("hook_ms_p95") is not None:  # the one counter not summed: the worst package p95
                cnt["hook_ms_p95"] = max(cnt["hook_ms_p95"] or 0, rv["hook_ms_p95"])
        for s, n in (c.get("moves_covered") or {}).items():
            cnt["moves_covered_panel"][s] = cnt["moves_covered_panel"].get(s, 0) + n
        cnt["own_line_jaccard"][p] = c.get("own_line_jaccard")
    return {
        "schema": "r1-results/1", "design": "r1-move-radar", "row": row, "panel": panel, "models": models,
        "collab": collab, "rep": rep, "started_utc": rowrun.get("started_utc"), "values": {p: pk[p].get("values") for p in PKGS},
        "status": "complete" if all(ok.values()) else "incomplete",
        "found_14": total([DS, AL], lambda x: len(x["gt_covered_any"])),
        "real_blocking_8": total([DS, AL], lambda x: len(x["real_blocking"])),
        "judge_blocking": total([DS, AL], lambda x: len(x["judge_blocking"])),
        "wrong_blockers": total([DS, AL], lambda x: x["wrong_blockers"]),
        "control_found_2": total([DE], lambda x: len(x["gt_covered_any"])),
        "control_wrong_blockers": total([DE], lambda x: x["wrong_blockers"]),
        "output_tokens": total(PKGS, lambda x: x["output_tokens"]),
        "elapsed_s": {p: pk[p].get("elapsed_s") for p in PKGS},
        "packages": pk, "collab_counters": cnt,
    }


def main(argv: list[str]) -> int:
    root, a1, rest, it = R1, A1DIR, [], iter(argv)
    for x in it:
        if x == "--root":
            root = next(it)
        elif x == "--a1":
            a1 = next(it)
        else:
            rest.append(x)
    if len(rest) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    row = rest[0]
    os.makedirs(f"{root}/results", exist_ok=True)
    jl = f"{root}/results/results.jsonl"
    seen = {json.loads(x)["row"] for x in open(jl).read().splitlines() if x.strip()} if os.path.exists(jl) else set()
    if row in seen:
        print(f"REFUSE row {row} is already in results.jsonl", file=sys.stderr)
        return 2
    res = build(row, root, a1)
    json.dump(res, open(f"{root}/results/{row}.json", "w"), indent=1)
    with open(jl, "a") as f:
        f.write(json.dumps(res) + "\n")
    print(f"{root}/results/{row}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
