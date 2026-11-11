import math,random,statistics as S,collections
exec(open('analyze.py').read().split("# 1 yield")[0])
def build(runs_sub):
    freq={d:{'S':0,'H':0} for d in DEF}; n={'S':0,'H':0}
    for rv in runs_sub:
        for r,s in rv.items():
            n[typ(r)]+=1
            for d in s: freq[d][typ(r)]+=1
    return {d:{T:(freq[d][T]+0.5)/(n[T]+1) for T in 'SH'} for d in DEF}
def pkfor(names):
    byk=collections.defaultdict(lambda:[0,0])
    for run in names:
        rv=runs[run]
        for d in DEF:
            k=min(sum(1 for s in rv.values() if d in s),3)
            byk[k][0]+=1; byk[k][1]+= d in fixed[run]
    return {k:(v[1]+0.5)/(v[0]+1) for k,v in byk.items()}
def expf(q,pk,nS,nH,cap=None):
    tot=0
    for d in DEF:
        ps=[q[d]['S']]*nS+[q[d]['H']]*nH; dist=[1.0]
        for p in ps:
            nd=[0]*(len(dist)+1)
            for i,x in enumerate(dist): nd[i]+=x*(1-p); nd[i+1]+=x*p
            dist=nd
        tot+=sum(x*pk[min(i,3)] for i,x in enumerate(dist))
    return tot
allrunsets=list(runs.values()); names=list(runs)
q=build(allrunsets)
cfgs=[(1,3),(2,3),(3,3),(1,4),(1,6),(2,6),(3,6)]
for var,nm in [('panel',[r for r in fixed if r.startswith('d5-')]),('full',[r for r in fixed if r.startswith('d5f-')])]:
    pk=pkfor(nm); base=expf(q,pk,1,3)
    print(var,'pk',{k:round(v,2) for k,v in sorted(pk.items())},'model base %.1f observed %.1f'%(base,S.mean(len(fixed[r]) for r in nm)))
    random.seed(3); res={c:[] for c in cfgs}
    for _ in range(400):
        qs=build([runs[random.choice(names)] for _ in names]); nms=[random.choice(nm) for _ in nm]
        pkb=pkfor(nms); b=expf(qs,pkb,1,3)
        for c in cfgs: res[c].append(expf(qs,pkb,*c)-b)
    for c in cfgs:
        v=sorted(res[c]); print('  %dS+%dH  delta fixed %+.1f  90%% CI [%+.1f, %+.1f]'%(c[0],c[1],S.mean(v),v[int(.05*len(v))],v[int(.95*len(v))]))
