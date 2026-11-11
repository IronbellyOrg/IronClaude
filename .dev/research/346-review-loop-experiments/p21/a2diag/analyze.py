import json, re, collections
LBL = "/home/user/IronClaude/.dev/research/346-review-loop-experiments/p20/label"
P, L = [], {}
for b in (1, 2, 3):
    P += json.load(open(f"{LBL}/packets_b{b}.json"))
    for x in json.load(open(f"{LBL}/labels_b{b}.json"))["labels"]: L[x["label_id"]] = x
A = json.load(open("answers.json"))
truth = {p["label_id"]: L[p["label_id"]]["label"] in ("cannot_pass", "cannot_discriminate") for p in P}
ids = [p["label_id"] for p in P]
def auc(s):
    pos = [s[i] for i in ids if truth[i]]; neg = [s[i] for i in ids if not truth[i]]
    return round(sum((x > y) + 0.5 * (x == y) for x in pos for y in neg) / (len(pos) * len(neg)), 3)
def topk(s, k=12):
    top = sorted(ids, key=lambda i: -s[i])[:k]; return sum(truth[i] for i in top)
def flawp(a): pr = a.get("probs") or {}; return pr.get("cannot_pass", 0) + pr.get("cannot_discriminate", 0)
S = {}
S["original choice, packet"] = {i: flawp(A[f"{i}|packet|orig"]) for i in ids}
S["original choice, options reversed"] = {i: flawp(A[f"{i}|packet|rev"]) for i in ids}
S["noul: empty result passes"] = {i: A[f"{i}|atomic|empty"]["noul"] for i in ids}
S["noul: needs unproduced output"] = {i: A[f"{i}|atomic|unprod"]["noul"] for i in ids}
S["noul: contradicts a cited row (max)"] = {i: max([A[k]["noul"] for k in A if k.startswith(f"{i}|atomic|contra")] or [0]) for i in ids}
S["atomic combined (max of the three)"] = {i: max(S[n][i] for n in ("noul: empty result passes", "noul: needs unproduced output", "noul: contradicts a cited row (max)")) for i in ids}
S["original choice, full spec"] = {i: flawp(A[f"{i}|spec|orig"]) for i in ids}
S["noul: spec rule conflicts, full spec"] = {i: A[f"{i}|spec|conflict"]["noul"] for i in ids}
S["noul: empty passes, full spec"] = {i: A[f"{i}|spec|empty"]["noul"] for i in ids}
print(f"46 packets, {sum(truth.values())} flawed per Opus labels; top-12 by chance ~{12*sum(truth.values())/46:.1f}")
for n, s in S.items():
    print(f"{n:42s} AUC {auc(s):.3f}  flawed in top-12: {topk(s)}  mean score {sum(s.values())/46:.2f}")
ch = lambda k: collections.Counter(A[f"{i}|{k}"].get("choice") for i in ids)
print("choices packet/orig", ch("packet|orig")); print("choices packet/rev", ch("packet|rev")); print("choices spec/orig", ch("spec|orig"))
print("order agreement orig vs reversed:", sum(A[f"{i}|packet|orig"]["choice"] == A[f"{i}|packet|rev"]["choice"] for i in ids), "/ 46")
ID = re.compile(r"\b(WC-\d+|SA-\d+|AC-C?\d+(?:\.\d+)?|D\d|P\d|7\.2#?\d*|\d\.\d)\b")
outside = {p["label_id"] for p in P if set(ID.findall(L[p["label_id"]]["reason"])) - set(ID.findall(json.dumps(p["check"]) + json.dumps(p["cited"]) + json.dumps(p["code_stage"])))}
print("flawed labels whose reason needs ids outside the packet:", sum(truth[i] for i in outside), "of", sum(truth.values()), "| can_pass labels doing so:", sum(not truth[i] for i in outside))
