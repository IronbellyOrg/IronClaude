import json,os
leg={}
for i,l in enumerate(open('/tmp/issue-legend.tsv')):
    if i==0: continue
    p=l.rstrip('\n').split('\t'); leg[p[0]]=(p[1],p[2])
pk={'designSpec':'TASK-WF-designSpec-20261107-075614','alias':'TASK-WF-makeTheAliasOnly-20261105-051649','control':'TASK-WF-design-20261108-041415'}
labels=list(leg)
out=[]; notes_dump=[]
for s in json.load(open('/tmp/allsets-chunks/chunk-03.json')):
    found={l:0 for l in labels}; bc={l:0 for l in labels}; per={}; missing=[]; flags=[]
    for r in s['runs']:
        pf=[];pb=[]
        for l in labels:
            pkg,gt=leg[l]; path=r['scores'].get(pk[pkg])
            if not path or not os.path.exists(path): missing.append((r['run'],pkg)); continue
            d=json.load(open(path))
            if gt in d['gt_covered_any']: found[l]+=1; pf.append(l)
            if gt in d['gt_covered_blocking']: bc[l]+=1; pb.append(l)
            if gt in d['gt_covered_blocking'] and gt not in d['gt_covered_any']: flags.append(f"{r['run']} {l} blocking not in any")
        per[r['run']]={'found':pf,'blocking_credit':pb}
        for pkg,path in r['scores'].items():
            if os.path.exists(path):
                d=json.load(open(path)); notes_dump.append((s['sid'],r['run'],pkg[8:20],d['gt_covered_any'],d['gt_covered_blocking'],d['notes']))
    out.append({'sid':s['sid'],'set':s['set'],'era':s['era'],'n_runs':s['n_runs'],'found':found,'blocking_credit':bc,'per_run':per,'_missing':missing,'_flags':flags})
json.dump(out,open('/tmp/allsets-out/chunk-03.json','w'),indent=1)
pass
for o in out: print(o['sid'],o['_missing'],o['_flags'])
CHK={'S03':"1 run; read all 3 notes; arrays agree (designSpec GT3,GT7 any / GT7 blocking; alias and control none; blocking rows all wrong blockers). No unreadable-report remarks.",
'S13':"4 runs; read all 12 notes; arrays agree with notes. Note: r1 designSpec lists GT8 in any (non-blocking L3) and r4 notes L6 as a borderline wrong blocker on GT8 (not credited, consistent with arrays). No unreadable-report remarks.",
'S23':"1 run; read all 3 notes; arrays agree (designSpec GT3,GT7 non-blocking; control GT2 non-blocking). No unreadable-report remarks.",
'S33':"1 run; read all 3 notes; arrays agree (designSpec GT3 blocking, GT7 non-blocking; control GT2 blocking). No unreadable-report remarks.",
'S43':"1 run; read all 3 notes; arrays agree (designSpec GT3,GT5,GT7 non-blocking; alias GT2 blocking; control GT2 blocking). No unreadable-report remarks.",
'S53':"1 run; read all 3 notes; arrays agree (designSpec GT3 blocking, GT7 non-blocking; control GT2 blocking). No unreadable-report remarks."}
for o in out:
    assert not o['_missing'] and not o['_flags']
    del o['_missing'],o['_flags']; o['check']=CHK[o['sid']]
json.dump(out,open('/tmp/allsets-out/chunk-03.json','w'),indent=1)
for o in out: print(o['sid'],{k:v for k,v in o['found'].items() if v},{k:v for k,v in o['blocking_credit'].items() if v})
