"""Results row from score.json + ground truth + cost + collab (DESIGN 5.5; final-table.py metrics, MR:22, MR:955).
Ground truth is read here only for blocking_in_implement flags, after judging; nothing reaches a reviewer."""
import json
import sys

from r5 import PKGS, append_jsonl, eval_dir, out, read_json, read_jsonl, write_json

DS, AL, CT = PKGS
LABELS = {DS: {f"GT{i}": f"B{i}" for i in range(1, 6)} | {f"GT{i}": f"I{i - 5}" for i in range(6, 11)},
          AL: {"GT1": "B6", "GT2": "B7", "GT3": "B8", "GT4": "I6"},
          CT: {"GT1": "I7", "GT2": "I8"}}
TARGET = {"B1", "B2", "B5", "B6", "B8", "I1", "I4", "I5", "I6", "I7"}
COLLAB_KEYS = ("k", "late", "dup_card", "hook_calls", "hook_error", "hook_ms_p95", "finish_signal_t", "finish_would_fire",
               "hang_kill", "retry_isolated", "reask_s", "dropped_lines", "k0_isolated", "deflection_overlap",
               "union_anchored_tasks", "own_line_jaccard", "ledger_rows", "slo")


def label(pkg: str, gt: str) -> str:
    return LABELS.get(pkg, {}).get(gt, f"{pkg[:12]}:{gt}")


def metrics(scores: dict, gt_blocking: dict) -> dict:
    def s(p, key):
        return scores.get(p, {}).get(key) or []
    m = {"found_14": sum(len(s(p, "gt_covered_any")) for p in (DS, AL)),
         "real_blocking_8": sum(1 for p in (DS, AL) for g in s(p, "gt_covered_blocking") if gt_blocking.get(p, {}).get(g)),
         "judge_blocking": sum(len(s(p, "gt_covered_blocking")) for p in (DS, AL)),
         "wrong_blockers": sum(scores.get(p, {}).get("wrong_blockers", 0) for p in (DS, AL) if p in scores),
         "control_found_2": len(s(CT, "gt_covered_any")) if CT in scores else None,
         "control_wrong_blockers": scores[CT].get("wrong_blockers") if CT in scores else None}
    any_ = sorted({label(p, g) for p in scores for g in s(p, "gt_covered_any")})
    blk = sorted({label(p, g) for p in scores for g in s(p, "gt_covered_blocking")})
    hard = [x for x in any_ if x in TARGET]
    m["issues"] = {"credited_any": any_, "credited_blocking": blk, "target_reach": bool(hard), "hard_credits": len(hard)}
    return m


def collab_summary(c: dict, run_dir) -> dict:
    revs = c.get("reviewers") or {}
    cards = c.get("cards") or []
    timing = [read_json(run_dir / "reviews" / f"{r}.timing.json") or {} for r in revs]
    def total(k):
        vals = [r.get(k) for r in revs.values() if r.get(k) is not None]
        return sum(int(v) for v in vals) if vals else None
    s = {k: c.get(k) for k in COLLAB_KEYS if k in c}
    s.update(cards_posted=sum(1 for x in cards if x.get("id")), cards_delivered=sum(1 for x in cards if x["status"] == "delivered"),
             requests_delivered=c.get("requests_delivered"), requests_acted=c.get("requests_acted"),
             superseded=sum(1 for x in cards if x["status"] == "superseded"), dup_card=sum(1 for x in cards if x["status"] == "dup_card"),
             late=total("late") or 0, snapshot_missing=total("snapshot_missing") or 0, hook_calls=total("hook_calls") or 0,
             hook_error=total("hook_error") or 0, hang_kill=sum(1 for r in revs.values() if r.get("hang_kill")),
             retry_isolated=sum(1 for r in revs.values() if r.get("retry_isolated")),
             reask_s=sum(t.get("reask_s") or 0 for t in timing), dropped_lines=sum(t.get("dropped_lines") or 0 for t in timing),
             hook_ms_p95=max((r["hook_ms_p95"] for r in revs.values() if r.get("hook_ms_p95") is not None), default=None),
             finish_signal_t=next((r["finish_signal_t"] for r in revs.values() if r.get("finish_signal_t")), None))
    return s


def build(row: str) -> dict:
    rdir = out() / "runs" / row
    launch = read_json(rdir / "launch.json") or {}
    keys = [k for k in read_jsonl(out() / "results" / "scoring-keys.jsonl") if k.get("row") == row]
    scores, pkg_status = {}, {}
    gt_blocking = {}
    for p in PKGS:
        d = rdir / p
        if not d.is_dir():
            continue
        st = read_json(d / "pkg-status.json") or {}
        pkg_status[p] = st
        k = next((k for k in reversed(keys) if k["pkg"] == p), None)
        if k:
            sc = read_json(out() / "scoring" / k["token"] / p / k["label"] / "score.json")
            if sc:
                scores[p] = sc
        gt = read_json(eval_dir() / p / "ground-truth.json") or {"items": []}
        gt_blocking[p] = {i["id"]: i["blocking_in_implement"] for i in gt["items"]}
    run0 = next((read_json(rdir / p / "run.json") for p in pkg_status), {}) or {}
    res = {"row": row, "arm": run0.get("arm"), "panel": run0.get("panel"), "models": run0.get("models"),
           "switches": run0.get("switches"), "time_cap_exception": bool(run0.get("time_cap_exception")), "time_cap": {},
           "values_sha256": {}, **metrics(scores, gt_blocking),
           "output_tokens": {"total": 0, "per_pkg": {}, "per_reviewer": {}}, "elapsed_s": {}, "overhead_pct": {},
           "collab": {}, "alarms": {}, "audit": {}, "invalid": [], "pkg_status": pkg_status}
    for p in pkg_status:
        d = rdir / p
        info = read_json(d / "run.json") or {}
        res["values_sha256"][p] = info.get("values_sha256")
        per = {}
        for cf in sorted((d / "reviews").glob("*.cost.json")):
            per[cf.name[: -len(".cost.json")]] = (read_json(cf) or {}).get("total_output_tokens_all", 0)
        res["output_tokens"]["per_reviewer"][p] = per
        res["output_tokens"]["per_pkg"][p] = sum(per.values())
        c = read_json(d / "collab.json") or {}
        res["elapsed_s"][p] = c.get("elapsed_s")
        res["overhead_pct"][p] = c.get("overhead_pct")
        res["collab"][p] = collab_summary(c, d) if c else None
        if res["time_cap_exception"]:  # the columns the owner asked for; such a row is never pooled with rows that obeyed the cap
            res["time_cap"][p] = {key: c.get(key) for key in ("B_A1_s", "elapsed_s", "elapsed_over_baseline", "time_cap_s", "k_measured",
                                                              "k_forced", "messages_delivered")}
            res["time_cap"][p]["k_run"] = c.get("k")
        a = read_json(d / "alarms.json") or {}
        res["alarms"][p] = {k: a.get(k) for k in ("CONVERGENCE", "DEFLECTION", "SLO")}
        res["audit"][p] = (read_json(d / "audit.json") or {}).get("status", "missing")
        res["invalid"] += [f"{p}:{r}" for r in pkg_status[p].get("invalid", [])]
    res["output_tokens"]["total"] = sum(res["output_tokens"]["per_pkg"].values())
    bad = any(s.get("merge") != "ok" or s.get("anon") != "ok" or s.get("judge") != "ok" for s in pkg_status.values())
    if any(v != "pass" for v in res["audit"].values()):
        res["status"] = "quarantined"
    elif bad or res["invalid"] or len(scores) < len(launch.get("pkgs", pkg_status)):
        res["status"] = "partial"
    else:
        res["status"] = "complete"
    return res


def main(argv: list[str]) -> int:
    res = build(argv[0])
    write_json(out() / "results" / f"{argv[0]}.json", res)
    append_jsonl(out() / "results" / "results.jsonl", res)
    print(json.dumps({"row": res["row"], "status": res["status"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
