#!/usr/bin/env python3
"""Stage B: predict the fixes of ANY panel composition from single-model profile reports.

Input  : a directory of match files, one per first-round report, each
           {"model": "<model id>", "rep": 1, "findings": [{"defect": "D07", "also": null|"D12", ...}, ...]}
         (the matcher output of prompts/02-stage-a-matcher.md), or the legacy ROI match files
         {"run": ..., "reviewers": {"t1b-1": [...], ...}} with --legacy-map "t1b=claude-sonnet-5-5,*=claude-haiku-5-5".
Model  : p[m][d] = P(a report of model m raises ledger defect d), estimated as (raises + 0.5) / (reports + 1).
         A panel's reviewers are independent draws; k_d = number of reviewers raising defect d (Poisson-binomial).
         E[fixed] = sum_d sum_k P(k_d = k) * conv[min(k, 3)], conv = P(fixed | raised by k) = 0.03, 0.35, 0.50, 0.58
         (measured on the ab5 runs, p19/roi/ROI-OF-EXTRA-REVIEWS.md); override with --conv.
         Random slots average over their model pool uniformly.
Output : expected fixed per panel, expected distinct defects raised, expected blocking raised, cost in tokens when
         --tokens-file is given, and the ranking.  It is a screening model: confirm the top panels end to end (Stage C).

Usage:
  simulate.py --reports DIR --ledger LEDGER.json --panels combos.json [--tiers TIERS.json] [--enumerate K]
              [--anchor MODEL] [--tokens-file tokens.json] [--top N] [--conv 0.03,0.35,0.5,0.58]
"""
from __future__ import annotations

import argparse
import glob
import itertools
import json
import sys
from collections import defaultdict


def load_reports(path: str, legacy_map: str | None):
    by_model: dict[str, list[set[str]]] = defaultdict(list)
    lm = {}
    if legacy_map:
        for part in legacy_map.split(","):
            k, v = part.split("=")
            lm[k.strip()] = v.strip()
    for f in sorted(glob.glob(f"{path}/*.json")):
        d = json.load(open(f))
        if "findings" in d:
            groups = [(d["model"], d["findings"])]
        else:
            groups = []
            for rid, fs in d["reviewers"].items():
                slot = rid.split("-")[0]
                model = lm.get(slot, lm.get("*"))
                if model is None:
                    raise SystemExit(f"{f}: no --legacy-map entry for slot {slot}")
                groups.append((model, fs))
        for model, fs in groups:
            s = set()
            for x in fs:
                for k in ("defect", "also"):
                    v = x.get(k)
                    if v and isinstance(v, str) and v[:1] == "D" and v[1:].isdigit():
                        s.add(v)
            by_model[model].append(s)
    return by_model


def capture_rates(by_model, defects):
    p = {}
    for m, reps in by_model.items():
        n = len(reps)
        p[m] = {d: (sum(1 for r in reps if d in r) + 0.5) / (n + 1) for d in defects}
    return p


def slot_p(slot, p, tiers):
    """Per-defect raise probability for one reviewer drawn from the slot (uniform over its model pool)."""
    pool = slot.get("models") or tiers["aliases"][slot["tier"]]["models"]
    pool = [m for m in pool if m in p]
    if not pool:
        raise SystemExit(f"no profiled model for slot {slot}: pool {slot.get('models') or slot['tier']}")
    return {d: sum(p[m][d] for m in pool) / len(pool) for d in next(iter(p.values()))}, pool


def expected_for(reviewers, defects, sev, conv):
    """reviewers: list of dict d->prob.  Returns (E fixed, E distinct raised, E blocking raised)."""
    ef = er = eb = 0.0
    for d in defects:
        dist = [1.0]
        for r in reviewers:
            q = r[d]
            new = [0.0] * (len(dist) + 1)
            for k, pk in enumerate(dist):
                new[k] += pk * (1 - q)
                new[k + 1] += pk * q
            dist = new
        ef += sum(pk * conv[min(k, len(conv) - 1)] for k, pk in enumerate(dist))
        raised = 1 - dist[0]
        er += raised
        if sev[d] == "blocking":
            eb += raised
    return ef, er, eb


def panel_reviewers(panel, p, tiers):
    revs, models = [], []
    for slot in panel["slots"]:
        sp, pool = slot_p(slot, p, tiers)
        for _ in range(slot["count"]):
            revs.append(sp)
            models.append(pool)
    return revs, models


def panel_cost(panel, models_pools, tokens):
    if not tokens:
        return None
    tot = 0.0
    for pool in models_pools:
        tot += sum(tokens.get(m, 0) for m in pool) / len(pool)
    return tot


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reports", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--panels", help="combos.json (reads its 'panels')")
    ap.add_argument("--tiers", help="tier file (default: the packaged review-tiers.default.json is NOT read; pass the one used live)")
    ap.add_argument("--enumerate", type=int, metavar="K", help="also enumerate every multiset of K reviewers from the profiled models")
    ap.add_argument("--anchor", default="claude-sonnet-5-5", help="the fixed first reviewer in enumerated panels")
    ap.add_argument("--tokens-file", help='JSON {"model": mean output tokens per report}')
    ap.add_argument("--legacy-map")
    ap.add_argument("--conv", default="0.03,0.35,0.50,0.58")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args(argv)

    led = json.load(open(a.ledger))
    defects_list = led["defects"]
    sev = {d["id"]: d["severity"] for d in defects_list}
    defects = sorted(sev)
    conv = [float(x) for x in a.conv.split(",")]
    by_model = load_reports(a.reports, a.legacy_map)
    p = capture_rates(by_model, defects)
    tokens = json.load(open(a.tokens_file)) if a.tokens_file else None
    tiers = json.load(open(a.tiers)) if a.tiers else {"aliases": {}}
    rows = []
    if a.panels:
        combos = json.load(open(a.panels))
        for panel in combos["panels"]:
            revs, pools = panel_reviewers(panel, p, tiers)
            ef, er, eb = expected_for(revs, defects, sev, conv)
            rows.append((panel["id"], len(revs), ef, er, eb, panel_cost(panel, pools, tokens)))
    if a.enumerate:
        models = sorted(p)
        rest = a.enumerate - 1
        anchor = {d: p[a.anchor][d] for d in defects}
        for combo in itertools.combinations_with_replacement(models, rest):
            revs = [anchor] + [p[m] for m in combo]
            ef, er, eb = expected_for(revs, defects, sev, conv)
            cost = None if not tokens else tokens.get(a.anchor, 0) + sum(tokens.get(m, 0) for m in combo)
            rows.append(("A:" + a.anchor + " + " + " + ".join(combo), a.enumerate, ef, er, eb, cost))
    rows.sort(key=lambda r: -r[2])
    print(f"models profiled: " + ", ".join(f"{m} (n={len(v)})" for m, v in sorted(by_model.items())))
    print(f"{'panel':<70} {'n':>2} {'E[fixed]':>9} {'E[raised]':>10} {'E[blk]':>7} {'tokens':>9}")
    for r in rows[: a.top] if a.enumerate and not a.panels else rows:
        print(f"{r[0][:70]:<70} {r[1]:>2} {r[2]:>9.1f} {r[3]:>10.1f} {r[4]:>7.1f} {'' if r[5] is None else int(r[5]):>9}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
