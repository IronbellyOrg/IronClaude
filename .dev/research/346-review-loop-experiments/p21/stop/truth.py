"""Test 2 ground truth: ledger score of the spec after V1 (s106-s129) vs the final spec (s82-s105), same blind Sonnet instrument."""
import json, collections, statistics as S
SC = "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p17/score"
key = json.load(open(f"{SC}/key.json"))
L = json.load(open("/home/user/IronClaude/.dev/research/346-review-loop-experiments/p17/ledger.json"))
sev = {d["id"]: d["severity"] for d in L["defects"]}
W = {"blocking": 3, "medium": 2, "minor": 1}
RES = {"PRESENT", "PARTIAL", "WORSE", "MOOT_BAD"}
def score(sid):
    o = json.load(open(f"{SC}/out/{sid}.json"))
    st = {d["id"]: d["status"] for d in o["defects"]}
    assert len(st) == 44
    return {"fixed": sum(s in ("FIXED", "DELETED_OK") for s in st.values()),
            "resid_blk": sum(s in RES and sev[i] == "blocking" for i, s in st.items()),
            "weighted": sum(W[sev[i]] for i, s in st.items() if s in RES),
            "intro": sum(x["status"] == "PRESENT" for x in o["introduced"]), "st": st}
byrun = collections.defaultdict(dict)
for sid, k in key.items():
    n = int(sid[1:])
    if 82 <= n <= 105: byrun[k["run"]]["final"] = sid; byrun[k["run"]]["arm"] = k["arm"]
    if 106 <= n <= 129: byrun[k["run"]]["v2"] = sid
rows = []
for run, d in sorted(byrun.items()):
    a, b = score(d["v2"]), score(d["final"])
    newly = sum(a["st"][i] not in ("FIXED", "DELETED_OK") and b["st"][i] in ("FIXED", "DELETED_OK") for i in a["st"])
    lost = sum(a["st"][i] in ("FIXED", "DELETED_OK") and b["st"][i] not in ("FIXED", "DELETED_OK") for i in a["st"])
    rows.append({"run": run, "arm": d["arm"], "v2": a["fixed"], "final": b["fixed"], "d_fixed": b["fixed"] - a["fixed"], "newly": newly, "lost": lost,
                 "d_weighted": b["weighted"] - a["weighted"], "d_blk": b["resid_blk"] - a["resid_blk"], "d_intro": b["intro"] - a["intro"]})
for r in rows: print(r)
print("median d_fixed", S.median(r["d_fixed"] for r in rows), "mean", round(S.mean(r["d_fixed"] for r in rows), 2),
      "| d_weighted mean", round(S.mean(r["d_weighted"] for r in rows), 2), "| runs with d_fixed<=0:", sum(r["d_fixed"] <= 0 for r in rows),
      "| runs with d_weighted>=0 (no improvement):", sum(r["d_weighted"] >= 0 for r in rows))
json.dump(rows, open("truth.json", "w"), indent=1)
