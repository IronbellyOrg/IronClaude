import json
leg=[l.rstrip("\n").split("\t") for l in open("/tmp/issue-legend.tsv")][1:]
labs=[(a,b,c) for a,b,c,*_ in leg]
pk={"designSpec":"TASK-WF-designSpec-20261107-075614","alias":"TASK-WF-makeTheAliasOnly-20261105-051649","control":"TASK-WF-design-20261108-041415"}
out=[];dump=[]
for s in json.load(open("/tmp/allsets-chunks/chunk-10.json")):
    found={l:0 for l,_,_ in labs};bc=dict(found);pr={};issues=[]
    for r in s["runs"]:
        f=[];b=[]
        for l,p,g in labs:
            d=json.load(open(r["scores"][pk[p]]))
            if g in d.get("gt_covered_any",[]): found[l]+=1;f.append(l)
            if g in d.get("gt_covered_blocking",[]): bc[l]+=1;b.append(l)
        pr[r["run"]]={"found":f,"blocking_credit":b}
    out.append({"sid":s["sid"],"set":s["set"],"era":s["era"],"n_runs":s["n_runs"],"found":found,"blocking_credit":bc,"per_run":pr,"check":""})
    for r in s["runs"]:
        for p,path in r["scores"].items():
            d=json.load(open(path));dump.append((s["sid"],r["run"],p[:18],d.get("gt_covered_any"),d.get("gt_covered_blocking"),str(d.get("notes"))[:700]))
json.dump(out,open("/tmp/allsets-out/chunk-10.json","w"),indent=1)
for x in dump: print(x,"\n")
