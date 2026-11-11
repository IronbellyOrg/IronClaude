"""Test 1: Jev 'same defect?' on 932 same-run finding pairs, both orders; compare to code rules and the ledger labels."""
import json, re, sys, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21")
import jrun
P17 = "/home/user/IronClaude/.dev/research/346-review-loop-experiments/p17"
F = {json.loads(l)["gid"]: json.loads(l) for l in open(f"{P17}/findings.jsonl")}
pairs = json.load(open("pairs.json"))
QDEF = {"type": "choice",
        "instructions": ("Two reviewers each reported a finding about the same specification document. Decide whether the two findings "
                         "describe the same underlying defect, meaning one correction to the specification would resolve both. "
                         "Citing the same section, rule or acceptance check is not enough: two different problems in the same place are different defects."),
        "criteria": {"same_defect": "Both findings describe the same underlying defect; one correction resolves both.",
                     "different_defects": "The findings describe different defects, even if they overlap in location or topic.",
                     "unclear": "The supplied text does not let you decide."}}
def fstate(f):
    return {"heading": f["heading"].lstrip("# ").strip(), "body": f["body"].strip()}
items = []
for p in pairs:
    a, b = F[p["a"]], F[p["b"]]
    for order, (x, y) in (("ab", (a, b)), ("ba", (b, a))):
        items.append({"id": f"{p['id']}|{order}", "state": {"finding_1": fstate(x), "finding_2": fstate(y)}, "qname": "same_defect", "qdef": QDEF})
if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else len(items)
    ans, st = jrun.run(items[:n], out_dir="out", experiment="p21-dedup", ceiling_usd=0.50, workers=8)
    print(st, collections.Counter((v["status"], v.get("choice")) for v in ans.values()))
