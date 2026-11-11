import json, re, collections
P17 = "/home/user/IronClaude/.dev/research/346-review-loop-experiments/p17"
F = {json.loads(l)["gid"]: json.loads(l) for l in open(f"{P17}/findings.jsonl")}
pairs = json.load(open("pairs.json")); A = json.load(open("answers.json"))
REF = re.compile(r"\b(AC-\d+\.\d+|WC-\d+|SA-\d+|FR-\d+|P\d|D\d|\d+\.\d+)\b")
def refs(f): return set(REF.findall(f["heading"] + " " + f["body"]))
def pr(pred, truth):
    tp = sum(p and t for p, t in zip(pred, truth)); fp = sum(p and not t for p, t in zip(pred, truth)); fn = sum((not p) and t for p, t in zip(pred, truth))
    return tp, fp, fn, round(tp / max(1, tp + fp), 2), round(tp / max(1, tp + fn), 2)
truth_same = [p["same"] for p in pairs]; truth_ovl = [p["same"] or p["overlap"] for p in pairs]
rows = []
def jev(p, o): return A.get(f"{p['id']}|{o}", {})
st = collections.Counter(jev(p, o).get("status") for p in pairs for o in ("ab", "ba"))
ch = collections.Counter(jev(p, o).get("choice") for p in pairs for o in ("ab", "ba"))
agree = sum(jev(p, "ab").get("choice") == jev(p, "ba").get("choice") for p in pairs)
print("status", st, "choices", ch, f"order agreement {agree}/{len(pairs)}")
def jp(p): return min(jev(p, o).get("probs", {}).get("same_defect", 0) for o in ("ab", "ba"))
preds = {
 "jev both orders same": [all(jev(p, o).get("choice") == "same_defect" for o in ("ab", "ba")) for p in pairs],
 "jev either order same": [any(jev(p, o).get("choice") == "same_defect" for o in ("ab", "ba")) for p in pairs],
 "code: shared SPEC line": [p["shared_lines"] >= 1 for p in pairs],
 "code: line jaccard>=0.3": [p["jacc"] >= 0.3 for p in pairs],
 "code: shared ref (merge-like)": [bool(refs(F[p["a"]]) & refs(F[p["b"]])) for p in pairs],
}
for th in (0.5, 0.7, 0.9):
    preds[f"jev min P(same)>={th}"] = [jp(p) >= th for p in pairs]
print(f"positives: same {sum(truth_same)}, same-or-overlap {sum(truth_ovl)}, pairs {len(pairs)}")
print("rule | vs same: tp fp fn prec rec | vs same-or-overlap: tp fp fn prec rec | n flagged")
for k, v in preds.items():
    print(k, "|", pr(v, truth_same), "|", pr(v, truth_ovl), "|", sum(v))
# separation
import statistics as S
for lab, sel in (("same", lambda p: p["same"]), ("overlap", lambda p: p["overlap"] and not p["same"]), ("diff", lambda p: not p["overlap"])):
    xs = [jp(p) for p in pairs if sel(p)]
    print(lab, len(xs), "median min P(same)", round(S.median(xs), 3), "mean", round(S.mean(xs), 3))
# AUC
pos = [jp(p) for p in pairs if p["same"]]; neg = [jp(p) for p in pairs if not p["overlap"]]
auc = sum((x > y) + 0.5 * (x == y) for x in pos for y in neg) / (len(pos) * len(neg))
print("AUC same vs diff (min P same)", round(auc, 3))
# hard negatives: diff pairs sharing a line
hn = [p for p in pairs if not p["overlap"] and p["shared_lines"] >= 1]
print("hard negatives (different defects, shared line):", len(hn), "jev says same (both orders):", sum(all(jev(p, o).get("choice") == "same_defect" for o in ("ab", "ba")) for p in hn))
print("\n--- extra")
pj = [p["jacc"] for p in pairs]
pos = [p["jacc"] for p in pairs if p["same"]]; neg = [p["jacc"] for p in pairs if not p["overlap"]]
print("AUC jaccard same vs diff", round(sum((x > y) + 0.5 * (x == y) for x in pos for y in neg) / (len(pos) * len(neg)), 3))
for th in (0.9, 0.7):
    for jt in (0.1, 0.2, 0.3):
        v = [jp(p) >= th and p["jacc"] >= jt for p in pairs]
        print(f"jev>={th} AND jacc>={jt}", pr(v, truth_same), pr(v, truth_ovl))
    v = [jp(p) >= th or p["jacc"] >= 0.3 for p in pairs]; print(f"jev>={th} OR jacc>=0.3", pr(v, truth_same), pr(v, truth_ovl))
print("\nfalse positives at jev>=0.9 (vs same):")
for p in pairs:
    if jp(p) >= 0.9 and not p["same"]:
        a, b = F[p["a"]], F[p["b"]]
        print(p["id"], p["arm"], "overlap" if p["overlap"] else "DIFF", p["da"], p["db"], "jacc", p["jacc"])
        print("  A:", a["heading"][:160]); print("  B:", b["heading"][:160])
print("\nmisses (same, jev<0.5):")
for p in pairs:
    if p["same"] and jp(p) < 0.5:
        print(p["id"], p["da"], round(jp(p), 2), "jacc", p["jacc"], "|", F[p["a"]]["heading"][:110], "||", F[p["b"]]["heading"][:110])
