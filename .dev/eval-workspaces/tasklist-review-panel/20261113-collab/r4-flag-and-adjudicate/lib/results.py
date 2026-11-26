"""The results row (design 5.2). The first code that reads ground truth for scoring.

usage: results.py <rowdir> --out results/<row>.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

LIB = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LIB)
from collab import overlap12  # noqa: E402

R4 = os.path.dirname(LIB)
REPO = os.environ.get("R4_REPO") or os.path.abspath(os.path.join(R4, "..", "..", "..", "..", ".."))
EVAL = os.environ.get("R4_EVAL", os.path.join(REPO, ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"))
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
SHORT = {DS: "DS", AL: "AL", DE: "DE"}
REACH = {DS: {"GT1", "GT2", "GT5", "GT6", "GT9", "GT10"}, AL: {"GT1", "GT3", "GT4"}, DE: {"GT1"}}
REJ_REASONS = ("too_early", "over_cap", "after_finish", "bad_args", "bad_move", "bad_category", "bad_severity",
               "bad_anchor_length", "anchor_not_in_candidate", "invalid")


def _load(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def _jsonl(p):
    out = []
    try:
        with open(p, encoding="utf-8") as fh:
            for ln in fh:
                try:
                    out.append(json.loads(ln))
                except json.JSONDecodeError:
                    pass
    except OSError:
        pass
    return out


def credited(pd: str, slot: dict, score: dict | None, gt_items: list) -> bool | None:
    """A converted line is credited when its ledger row's anchor overlaps the plan_quote of a covered GT item."""
    led = _load(os.path.join(pd, "ledger.json"))
    if not led or not score:
        return None
    covered = set(score.get("gt_covered_any") or [])
    quotes = [it["plan_quote"] for it in gt_items if it["id"] in covered]
    for row in led.get("rows", []):
        members = {(m.get("reviewer_id"), m.get("fid")) for m in row.get("members", [])}
        if any((slot["recipient"], fid) in members for fid in slot["converted_fids"]):
            if any(overlap12(row.get("anchor"), q) or overlap12(row.get("anchor2"), q) for q in quotes):
                return True
    return False


def build(rowdir: str) -> dict:
    run = _load(os.path.join(rowdir, "run.json"), {})
    audit = _load(os.path.join(rowdir, "audit.json"), {})
    order = [DS, AL, DE]
    pkgs, collab, elapsed, overhead = {}, {}, {}, {}
    tokens, valid = 0, True
    reach_ids = []
    for pkg in order:
        pd = os.path.join(rowdir, pkg)
        panel = _load(os.path.join(pd, "panel.json"))
        if not panel:
            valid = False
            continue
        status = (open(os.path.join(pd, "status")).read().strip() if os.path.exists(os.path.join(pd, "status")) else "not_run")
        score = _load(os.path.join(pd, "scoring", "score.json")) if status == "ok" else None
        if status == "ok" and not score:
            status = "judge_failed"
        if status != "ok":
            valid = False
        gt_items = _load(os.path.join(EVAL, pkg, "ground-truth.json"), {"items": []})["items"]
        gtb = {it["id"]: it["blocking_in_implement"] for it in gt_items}
        cj = _load(os.path.join(pd, "collab.json"), {})
        metas = {r["rid"]: _load(os.path.join(pd, "reviews", r["rid"] + ".meta.json"), {}) for r in panel["reviewers"]}
        if any(m.get("model_mismatch") for m in metas.values()):
            valid = False
        ptok = sum(m.get("output_tokens_all") or 0 for m in metas.values())
        tokens += ptok
        elapsed[SHORT[pkg]] = cj.get("elapsed_s")
        overhead[SHORT[pkg]] = cj.get("overhead_pct")
        lk = _load(os.path.join(pd, "scoring", "label-key.json"), {})
        cov = list(score.get("gt_covered_any") or []) if score else []
        if score:
            reach_ids += [f"{SHORT[pkg]}:{g}" for g in cov if g in REACH[pkg]]
        pkgs[pkg] = {
            "status": status, "label": lk.get("label"),
            "gt_covered_any": cov if score else None,
            "gt_covered_blocking": list(score.get("gt_covered_blocking") or []) if score else None,
            "real_blocking": [g for g in score.get("gt_covered_blocking") or [] if gtb.get(g)] if score else None,
            "wrong_blockers": score.get("wrong_blockers") if score else None,
            "ledger_rows_total": score.get("ledger_rows_total") if score else None,
            "ledger_rows_blocking": score.get("ledger_rows_blocking") if score else None,
            "output_tokens": ptok,
            "slo_breach": bool(cj.get("slo_breach")),
            "dropped_lines": sum(m.get("dropped_lines") or 0 for m in metas.values()),
            "reask_count": sum(1 for m in metas.values() if m.get("reask")),
        }
        slots = cj.get("slots") or []
        rej = [e for e in _jsonl(os.path.join(pd, "board", "metrics", panel["flagger"] + ".jsonl")) if e.get("ev") == "post_rejected"]
        conv = {}
        for form in ("challenge", "finding"):
            dl = [s for s in slots if s["card_form"] == form and s["status"] == "delivered"]
            cv = [s for s in dl if s["converted"]]
            cr = [credited(pd, s, score, gt_items) for s in cv]
            conv[form] = {"delivered": len(dl), "converted": len(cv), "credited": sum(1 for c in cr if c),
                          "uncredited": sum(1 for c in cr if c is False)}
        per = cj.get("reviewers") or {}
        tasks = [s["card_task"] for s in slots]
        collab[pkg] = {
            "k": cj.get("k"), "k0_isolated": cj.get("k0_isolated"), "deal_r": cj.get("deal_r"), "deal_c": cj.get("deal_c"),
            # time-cap exception columns (OVERRIDE.md); baseline_elapsed_s below is B_A1
            "time_cap_exception": bool(cj.get("time_cap_exception")), "k_measured": cj.get("k_measured"),
            "k_forced": bool(cj.get("k_forced")), "hang_s": cj.get("hang_s"), "finish_offset_s": cj.get("finish_offset_s"),
            "elapsed_s": cj.get("elapsed_s"), "elapsed_over_baseline": cj.get("elapsed_over_baseline"),
            "delivered_per_reviewer": cj.get("delivered_per_reviewer"),
            "cards_sent": cj.get("cards_sent", 0),
            "cards_rejected": {r: sum(1 for e in rej if e.get("reason") == r) for r in REJ_REASONS},
            "cards_delivered": cj.get("cards_delivered", 0),
            "late": sum(1 for s in slots if s["status"] == "late"),
            "no_snapshot": sum(1 for s in slots if s["status"] == "no_snapshot"),
            "receiving_lunas": len({s["recipient"] for s in slots}),
            "snapshot_missing": sum(1 for rid in {s["recipient"] for s in slots} if (per.get(rid) or {}).get("snapshot_missing")),
            "baseline_elapsed_s": cj.get("baseline_elapsed_s"),
            "conversions": conv,
            "passed_lines": sum(1 for s in slots if s["passed_line"]),
            "card_tasks": tasks,
            "early_tasks_only": (bool(tasks) and all(t is not None and int(t[1:]) < 8 for t in tasks)) if pkg == DS else None,
            "flag_finding_overlap": cj.get("flag_finding_overlap"),
            "adjudication_agreement": cj.get("adjudication_agreement"),
            "finish_signal_fired": any(v.get("finish_signal_t") for v in per.values()),
            "finish_would_fire": cj.get("finish_would_fire"),
            "hang_kill": any(v.get("hang_kill") for v in per.values()),
            "retry_isolated": any(v.get("retry_isolated") for v in per.values()),
            "hook_error": sum(v.get("hook_error") or 0 for v in per.values()),
            "hook_ms_p95": max((v.get("hook_ms_p95") or 0 for v in per.values()), default=None) if per else None,
            "own_line_jaccard": cj.get("own_line_jaccard"),
            "pairwise_task_jaccard": cj.get("pairwise_task_jaccard"),
            "ledger_rows": cj.get("ledger_rows"),
        }

    def tot(pk_list, key, f):
        if not valid:
            return None
        return sum(f(pkgs[p][key]) for p in pk_list)

    return {
        "schema": "r4-results/1",
        "row": run.get("row"), "panel": run.get("panel"), "arm": run.get("arm"), "panel_collab": run.get("panel_collab"),
        "time_cap_exception": bool(run.get("time_cap_exception")),
        "models": run.get("models"), "values_sha256": run.get("values_sha256"), "pins_ok": run.get("pins_ok"),
        "seed": run.get("seed"), "started": run.get("started"), "finished": run.get("finished"),
        "valid": valid,
        "found_14": tot([DS, AL], "gt_covered_any", len),
        "real_blocking_8": tot([DS, AL], "real_blocking", len),
        "judge_blocking": tot([DS, AL], "gt_covered_blocking", len),
        "wrong_blockers": tot([DS, AL], "wrong_blockers", int),
        "control_found_2": tot([DE], "gt_covered_any", len),
        "control_wrong_blockers": tot([DE], "wrong_blockers", int),
        "output_tokens": tokens,
        "elapsed_s": elapsed,
        "overhead_pct": overhead,
        "reach": bool(reach_ids) if valid else None,
        "reach_ids": reach_ids,
        "credited_method": "row anchor overlaps a covered plan_quote",
        "packages": pkgs,
        "collab": collab,
        "audit": {k: audit.get(k) for k in ("audit_ok", "violations", "sandbox_clean", "candidate_sha_ok", "board_lines_invalid",
                                              "harness_text_gt_overlap", "a1_brief_gt_overlap", "anchor_gt_overlap",
                                              "first_hand_suspect", "ignored_only", "tmp_other", "home_other")},
    }


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rowdir")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv[1:])
    out = build(os.path.abspath(a.rowdir))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
