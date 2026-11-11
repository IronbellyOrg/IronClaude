"""Test 1 setup check: the same 932 pairs with a Noul (skill guidance) instead of the three-option Choice."""
import json, sys, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21")
import jrun
from run_dedup import F, pairs, fstate
NOUL = {"type": "noul",
        "instructions": "Do `finding_1` and `finding_2` report the same defect in the specification, so that one correction to the specification would resolve both?",
        "criteria": {"true": "Both findings point at the same wrong or missing rule; fixing it resolves both claims.",
                     "false": "The findings point at different problems that need separate corrections, even if they quote the same section or rule."}}
items = [{"id": p["id"], "state": {"finding_1": fstate(F[p["a"]]), "finding_2": fstate(F[p["b"]])}, "qname": "same_defect", "qdef": NOUL} for p in pairs]
ans, st = jrun.run(items, out_dir="out-noul", experiment="p21-dedup-noul", ceiling_usd=0.10, workers=8)
print(st)
A = json.load(open("out/answers.json"))
def auc(s, pos_ids, neg_ids):
    pos = [s[i] for i in pos_ids]; neg = [s[i] for i in neg_ids]
    return round(sum((x > y) + 0.5 * (x == y) for x in pos for y in neg) / (len(pos) * len(neg)), 3)
nou = {p["id"]: ans[p["id"]]["noul"] for p in pairs}
cho = {p["id"]: min(A[f"{p['id']}|{o}"]["probs"]["same_defect"] for o in ("ab", "ba")) for p in pairs}
pos = [p["id"] for p in pairs if p["same"]]; neg = [p["id"] for p in pairs if not p["overlap"]]
print("AUC same vs diff: noul", auc(nou, pos, neg), "| choice (both orders, min)", auc(cho, pos, neg))
for th in (0.5, 0.7, 0.9):
    fl = [p for p in pairs if nou[p["id"]] >= th]; tp = sum(p["same"] for p in fl)
    print(f"noul >= {th}: flagged {len(fl)}, precision {tp/max(1,len(fl)):.2f}, recall {tp/len(pos):.2f}")
