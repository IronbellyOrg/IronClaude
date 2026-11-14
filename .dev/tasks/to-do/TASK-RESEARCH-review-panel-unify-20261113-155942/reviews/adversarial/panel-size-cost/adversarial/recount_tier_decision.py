"""Read-only recount of the non-shadow pre-run tier_decision.yaml files for debate C14.

Run: uv run python <this file> [--dump]
Reads .dev/reflect/pre-*/artifacts/tier_decision.yaml (skips directory names containing 'shadow').
Writes nothing. Prints the raw per-run rows and the tally by escalation path.
"""
import glob
import os
import re
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 8)))
files = sorted(glob.glob(os.path.join(ROOT, ".dev/reflect/pre-*/artifacts/tier_decision.yaml")))
rows = []
for f in files:
    d = os.path.basename(os.path.dirname(os.path.dirname(f)))
    if "shadow" in d:
        continue
    with open(f) as fh:
        txt = fh.read()
    try:
        y = yaml.safe_load(txt) or {}
    except Exception as e:  # keep going, report
        y = {"_parse_error": str(e)}
    rows.append((d, y, txt))

print("ROOT", ROOT)
print("non-shadow files:", len(rows))
keys = {}
for _, y, _ in rows:
    for k in y:
        keys[k] = keys.get(k, 0) + 1
print("KEYS", sorted(keys.items(), key=lambda kv: -kv[1]))

def g(y, *names):
    for n in names:
        if n in y:
            return y[n]
    return None

print("\nRAW ROWS: dir | tier | rule | flag | S_dom | S_dev | S_scope | C/conf | reason(<=110)")
for d, y, txt in rows:
    conf = g(y, "C", "confidence", "calibrated_confidence", "coverage_pct", "coverage_pct_union")
    reason = str(g(y, "escalation_reason", "reason") or "")[:110].replace("\n", " ")
    print(
        f"{d[:62]:62} | {g(y,'selected_tier')} | {g(y,'fired_rule_number')} | "
        f"{g(y,'coverage_degraded')} | {g(y,'S_domains')} | {g(y,'S_dev_density')} | {g(y,'S_scope')} | {conf} | {reason}"
    )

# tally
tot = len(rows)
t2 = [r for r in rows if r[1].get("selected_tier") == 2]
flag = [r for r in rows if r[1].get("coverage_degraded") not in (None, "null", "", False)]
flag_t2 = [r for r in flag if r[1].get("selected_tier") == 2]
print(f"\nTOTAL {tot}; tier2 {len(t2)}; flag set {len(flag)}; flag&tier2 {len(flag_t2)}")
by_rule = {}
for d, y, _ in flag_t2:
    pass
for d, y, _ in flag_t2:
    k = y.get("fired_rule_number")
    by_rule[k] = by_rule.get(k, 0) + 1
print("flag&tier2 by fired_rule_number:", by_rule)
