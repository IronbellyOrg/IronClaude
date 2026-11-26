import json, statistics as st
R = json.load(open("/tmp/audit-F/rows.json")); FAM = json.load(open("/tmp/audit-F/fam.json"))
M = {k: v["m"] for k, v in R.items() if v["m"]}
for mdl in ("sonnet","haiku","grok","luna","terra","ember","wonder"):
    w=[k for k in M if mdl in R[k]["ms"]]; wo=[k for k in M if mdl not in R[k]["ms"]]
    f=lambda L,key: st.mean(M[k][key] for k in L)
    print(mdl, "blk judge %.2f vs %.2f | blk_true %.2f vs %.2f"%(f(w,"blk"),f(wo,"blk"),f(w,"blk_true"),f(wo,"blk_true")))
for lab,x in FAM.items(): print(lab, "ctl_wb mean %.2f"%st.mean(x["cwb"]) if x["cwb"] else "")
top=sorted(M,key=lambda k:(-M[k]["any"],-M[k]["blk"]))[:6]
print([(k,M[k]["any"],M[k]["blk"],M[k]["blk_true"]) for k in top])
print("r2-sonnet-src", M["r2-sonnet-src"]); print("c3", M["c3-luna-grok-src"]); print("n2-sonnet-src", M["n2-sonnet-src"])
