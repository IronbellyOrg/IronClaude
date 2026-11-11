"""PN3 harness: C1-C3 panel resolution implemented from the shared contract (not product code)."""
import hashlib
import json
import pathlib
import random
import re
from datetime import date

HERE = pathlib.Path(__file__).parent
PANEL = json.load(open(HERE / "data/review-panel.default.json"))
TIERS = json.load(open(HERE / "data/review-tiers.default.json"))


class NoModelAvailable(Exception):
    pass


def _h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_panel(obj, tiers=None):
    e = []
    if obj.get("schema") != "review-panel/1":
        e.append("schema")
    if not re.match(r"^[a-z0-9][a-z0-9-]{0,31}$", str(obj.get("template_id", ""))):
        e.append("template_id")
    if not re.match(r"^\d+\.\d+\.\d+$", str(obj.get("version", ""))):
        e.append("version")
    if not isinstance(obj.get("distinct_across_slots"), bool):
        e.append("distinct_across_slots")
    at = obj.get("apply_to")
    if not isinstance(at, list) or not at or not set(at) <= {"first", "re-review"}:
        e.append("apply_to")
    slots = obj.get("slots")
    if not isinstance(slots, list) or not slots:
        return e + ["slots"]
    ids, total, fixed = set(), 0, 0
    for s in slots:
        if not re.match(r"^[a-z0-9]{1,8}$", str(s.get("slot_id", ""))) or s["slot_id"] in ids:
            e.append("slot_id")
        ids.add(s.get("slot_id"))
        if not re.match(r"^tier[0-9]{1,2}[a-z]?$", str(s.get("tier", ""))) or (tiers and s["tier"] not in tiers["aliases"]):
            e.append("tier")
        if not isinstance(s.get("count"), int) or not 1 <= s["count"] <= 4:
            e.append("count")
        else:
            total += s["count"]
        if s.get("strategy") not in ("fixed", "random", "round_robin"):
            e.append("strategy")
        fixed += s.get("strategy") == "fixed"
        if set(s) - {"slot_id", "tier", "count", "strategy", "seed"}:
            e.append("unknown slot key")
    if not 1 <= total <= 8:
        e.append("total reviewers")
    if fixed != 1:
        e.append("exactly one fixed slot")
    if set(obj) - {"schema", "template_id", "version", "distinct_across_slots", "apply_to", "slots", "description"}:
        e.append("unknown key")
    return e


def resolve_slot(models, strategy, seed, available, stand_ins, exclude=()):
    cands = [m for m in models if available == "all" or m in available]
    stand = False
    src = models
    if not cands:
        cands = [m for m in stand_ins if available == "all" or m in available]
        stand, src = True, stand_ins
        if not cands:
            raise NoModelAvailable("no model")
    if strategy == "fixed":
        model = cands[0]
    elif strategy == "random":
        pool = [m for m in cands if m not in exclude] or cands
        model = random.Random(seed).choice(pool)
    else:
        model = cands[seed % len(cands)]
    i = cands.index(model)
    return {"model": model, "fallback_depth": src.index(model), "stand_in": stand, "fallbacks": cands[i + 1:] + cands[:i]}


def resolve(panel, tiers, env, run_id, review_kind="first", seed=None, sequence=None):
    e = tiers["environments"][env]
    use_all = review_kind in panel["apply_to"]
    slots = sorted(panel["slots"], key=lambda s: s["strategy"] != "fixed") if True else panel["slots"]
    # fixed slot first, the others in file order (sorted is stable)
    out, chosen = [], []
    for s in slots:
        if not use_all and s["strategy"] != "fixed":
            continue
        for i in range(1, (s["count"] if use_all else 1) + 1):
            if s["strategy"] == "random":
                base = s.get("seed", seed if seed is not None else int(hashlib.sha256(run_id.encode()).hexdigest()[:8], 16))
                sd = f"{base}|{s['slot_id']}|{i}"
            elif s["strategy"] == "round_robin":
                sd = (sequence if sequence is not None else date.today().toordinal()) + i - 1
            else:
                sd = None
            al = tiers["aliases"][s["tier"]]
            r = resolve_slot(al["models"], s["strategy"], sd, e["available"], e["stand_ins"].get(s["tier"], []),
                             exclude=tuple(chosen) if panel["distinct_across_slots"] else ())
            chosen.append(r["model"])
            out.append({"reviewer_id": f"{s['slot_id']}-{i}", "slot_id": s["slot_id"], "tier": s["tier"], "alias": al["alias"],
                        "strategy": s["strategy"], "seed": sd, "model": r["model"],
                        "model_name": tiers.get("names", {}).get(r["model"]), "fallback_depth": r["fallback_depth"],
                        "stand_in": r["stand_in"], "fallbacks": r["fallbacks"], "launch": e["launch"].get(r["model"])})
    return {"schema": "review-panel-resolution/1", "template_id": panel["template_id"], "template_version": panel["version"],
            "template_sha256": _h(panel), "tiers_version": tiers["version"], "tiers_sha256": _h(tiers), "environment": env,
            "run_id": run_id, "review_kind": review_kind, "reviewers": out}
