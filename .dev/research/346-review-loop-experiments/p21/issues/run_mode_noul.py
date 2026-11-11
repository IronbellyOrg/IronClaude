"""Test 3 setup check: the same descriptions with Nouls (one per mode) instead of a three-option Choice, plus the Choice with options reversed."""
import json, sys, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21")
import jrun
from run_mode import QDEF
cases = json.load(open("cases.json"))
BUG = {"type": "noul", "instructions": "Does `description` report that something which already exists does not work as documented or intended?",
       "criteria": {"true": "It reports existing behavior that is wrong: a wrong output, a crash, a broken or misleading help text, a failing check or a wrong value.",
                    "false": "It asks for something new or different: a new capability, a change of design, a refactor, a data or configuration change, or new docs or tests."}}
REV = {"type": "choice", "instructions": QDEF["instructions"], "criteria": dict(reversed(list(QDEF["criteria"].items())))}
items = []
for c in cases:
    for v, text in (("title", c["title"]), ("full", c["title"] + ". " + c["excerpt"])):
        items.append({"id": f"{c['number']}|{v}|noul", "state": {"description": text}, "qname": "is_bug_report", "qdef": BUG})
        items.append({"id": f"{c['number']}|{v}|rev", "state": {"description": text}, "qname": "issue_mode", "qdef": REV})
ans, st = jrun.run(items, out_dir="out-noul", experiment="p21-issue-mode-noul", ceiling_usd=0.05, workers=4)
print(st, collections.Counter(v["status"] for v in ans.values()))
orig = json.load(open("out/answers.json"))
for v in ("title", "full"):
    n = len(cases)
    nb = sum((ans[f"{c['number']}|{v}|noul"]["noul"] > 0.5) == (c["truth"] == "bug") for c in cases)
    gated = [c for c in cases if not 0.3 <= ans[f"{c['number']}|{v}|noul"]["noul"] <= 0.7]
    ng = sum((ans[f"{c['number']}|{v}|noul"]["noul"] > 0.5) == (c["truth"] == "bug") for c in gated)
    agree = sum(ans[f"{c['number']}|{v}|rev"].get("choice") == orig[f"{c['number']}|{v}"].get("choice") for c in cases)
    rv = [c for c in cases if ans[f"{c['number']}|{v}|rev"].get("choice") in ("bug", "feature")]
    rr = sum(ans[f"{c['number']}|{v}|rev"]["choice"] == c["truth"] for c in rv)
    print(f"{v}: noul@0.5 {nb}/{n} = {nb/n:.2f}; noul outside 0.3-0.7: {ng}/{len(gated)}; reversed choice decided {len(rv)}, correct {rr}; same choice as original order {agree}/{n}")
