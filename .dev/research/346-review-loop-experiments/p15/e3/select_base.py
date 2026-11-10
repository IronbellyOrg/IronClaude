#!/usr/bin/env python3
"""select_base.py  After pool labels: pick the 30 real base findings balanced by independent truth (15 blocking / 15 not, as far as the
pool allows) with random.Random(3), at most 2 per group, and write the 60 base cases (30 real + 30 synthetic) to offline/cases/base/.
Selection uses the independent labels (truth.jsonl) and code-determined outcomes only, never Jev.  Code-owned EXCEPTION findings
(CRITICAL label) are not selected among the real cases (the 4 synthetic exceptions test that path); undecidable labels are excluded."""
import json
import random
import sys

import e3lib
import packets as pk
from p15common import datasets

BASE = e3lib.CASES / "base"


def pick(real_cases, truth, rng, n_total=30, cap=2):
    """-> (selected ids in order, info).  real_cases: dicts; truth: {case_id: 'yes'|'no'|...}."""
    spec = e3lib.s1_text()
    elig = {"yes": [], "no": []}
    excluded = {"exception": 0, "undecidable_or_unlabeled": 0, "not_ok": 0}
    for c in sorted(real_cases, key=lambda c: c["case_id"]):
        t = truth.get(c["case_id"])
        if t not in ("yes", "no"):
            excluded["undecidable_or_unlabeled"] += 1
            continue
        p = pk.build_packet(spec, c["packet"]["finding_section"], finding_id=c["packet"].get("finding_id"))
        if p.code_outcome == "EXCEPTION":
            excluded["exception"] += 1
            continue
        if p.code_outcome != "OK":
            excluded["not_ok"] += 1
            continue
        elig[t].append(c)
    for k in elig:
        rng.shuffle(elig[k])
    per = {"yes": n_total // 2, "no": n_total - n_total // 2}
    gcount, chosen = {}, {"yes": [], "no": []}
    for k in ("yes", "no"):                      # first pass: up to the balanced quota per class
        for c in elig[k]:
            if len(chosen[k]) >= per[k]:
                break
            if gcount.get(c["group"], 0) < cap:
                chosen[k].append(c)
                gcount[c["group"]] = gcount.get(c["group"], 0) + 1
    short = {k: per[k] - len(chosen[k]) for k in chosen}
    for k, other in (("yes", "no"), ("no", "yes")):          # a shortfall in one class is filled from the other
        need = short[k]
        for c in elig[other]:
            if need <= 0:
                break
            if c in chosen[other] or gcount.get(c["group"], 0) >= cap:
                continue
            chosen[other].append(c)
            gcount[c["group"]] = gcount.get(c["group"], 0) + 1
            need -= 1
    sel = chosen["yes"] + chosen["no"]
    info = {"seed": e3lib.decision()["offline"]["select_seed"], "n_selected": len(sel), "yes": len(chosen["yes"]), "no": len(chosen["no"]),
            "shortfall_vs_balanced": short, "groups": len({c["group"] for c in sel}), "group_cap": cap,
            "excluded": excluded, "eligible": {k: len(v) for k, v in elig.items()}}
    return [c["case_id"] for c in sel], info


def main(argv=None):
    dec = e3lib.decision()
    o = dec["offline"]
    truth = {r["case_id"]: r["blocking"] for r in e3lib.read_jsonl(e3lib.LABELS / "truth.jsonl")}
    if not truth:
        print("ERROR offline/labels/truth.jsonl is missing: run the labeling steps and ingest_labels.py first")
        return 2
    real = [json.loads(p.read_text()) for p in sorted(e3lib.POOL.glob("real*.json"))]
    synth = [json.loads(p.read_text()) for p in sorted((e3lib.OFF / "synth").glob("*.json"))]
    ids, info = pick(real, truth, random.Random(o["select_seed"]), o["n_real_base"], o["group_cap"])
    by = {c["case_id"]: c for c in real}
    BASE.mkdir(parents=True, exist_ok=True)
    for old in BASE.glob("*.json"):
        old.unlink()
    for cid in ids:
        c = dict(by[cid]); c["split"] = "base"
        datasets.write_case(BASE / f"{cid}.json", c)
    for c in synth:
        c = dict(c); c["split"] = "base"
        datasets.write_case(BASE / f"{c['case_id']}.json", c)
    info["synthetic"] = len(synth)
    e3lib.write_json(e3lib.OFF / "selection.json", {**info, "real_ids": ids})
    print(f"SELECT real {info['n_selected']} (blocking {info['yes']}, not {info['no']}; shortfall {info['shortfall_vs_balanced']}; {info['groups']} groups) + synthetic {len(synth)} = {info['n_selected'] + len(synth)} base cases; excluded {info['excluded']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
