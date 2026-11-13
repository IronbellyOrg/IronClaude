import json,re,os,sys
E="/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
import csv
rows=[l.rstrip("\n").split("\t") for l in open("/tmp/audit-B/flags.tsv")][1:]
ws=lambda s:re.sub(r"\s+"," ",s).strip()
n=0
for c,row,pkg,rid,sev,reason in rows:
    if c!="3-anchors" or sev!="EXCLUDE": continue
    t=open(f"{E}/{pkg}/reviews/combos/{row}/{rid}.md").read(); cand=ws(open(f"{E}/{pkg}/candidate.md").read())
    m=re.findall(r"```findings-v1[^\n]*\n(.*?)```",t,re.S)[-1]
    for ln in m.split("\n"):
        if ln.strip():
            o=json.loads(ln); a=ws(o["anchor"]); 
            # longest prefix found
            k=len(a)
            while k>5 and a[:k] not in cand: k-=1
            print(row,rid,"len",len(a),"prefix-match",k,"|",a[:90])
