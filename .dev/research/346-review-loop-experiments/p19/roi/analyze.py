import math,json,glob,random,itertools,collections,re,statistics as S
SP='/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad'
key=json.load(open(f'{SP}/p17/score/key.json'))
sev={d['id']:d['severity'] for d in json.load(open(f'{SP}/p17/ledger.json'))['defects']}
DEF=sorted(sev)
runs={}
for f in sorted(glob.glob('out/*.json')):
    d=json.load(open(f)); run=d['run']; rv={}
    for r,fs in d['reviewers'].items():
        s=set()
        for x in fs:
            for k in ('defect','also'):
                v=x.get(k)
                if v and re.fullmatch(r'D\d\d',v): s.add(v)
        rv[r]=s
    runs[run]=rv
def typ(r): return 'S' if r.startswith('t1b') else 'H'
# fixed sets for ab5 runs
fixed={}
for f in glob.glob(f'{SP}/p17/score/out/s*.json'):
    d=json.load(open(f)); k=key[d['sid']]
    if k['arm'].startswith('ab5'): fixed[k['run']]={x['id'] for x in d['defects'] if x['status'] in('FIXED','DELETED_OK')}
print('runs',len(runs),'reviewers',sum(len(v) for v in runs.values()))
# 1 yield per reviewer type
for T in 'SH':
    y=[len(s) for rv in runs.values() for r,s in rv.items() if typ(r)==T]
    yb=[len([d for d in s if sev[d]=='blocking']) for rv in runs.values() for r,s in rv.items() if typ(r)==T]
    print(T,'n',len(y),'mean distinct defects %.1f (blocking %.1f)'%(S.mean(y),S.mean(yb)),'range',min(y),max(y))
# union per run and curve of marginal gain by position (all orderings)
def marg(rv,order):
    seen=set();out=[]
    for r in order:
        new=rv[r]-seen; out.append(len(new)); seen|=rv[r]
    return out
pos=collections.defaultdict(list)
for run,rv in runs.items():
    ids=list(rv)
    for order in itertools.permutations(ids):
        m=marg(rv,order)
        for i,x in enumerate(m): pos[i].append(x)
print('mean new defects by reviewer position (all orderings):',[round(S.mean(pos[i]),1) for i in range(4)])
# Sonnet-first then Haiku marginal
sf=collections.defaultdict(list)
for run,rv in runs.items():
    ids=[r for r in rv if typ(r)=='S']; hs=[r for r in rv if typ(r)=='H']
    for h in itertools.permutations(hs):
        m=marg(rv,ids+list(h))
        for i,x in enumerate(m): sf[i].append(x)
print('Sonnet first then Haiku in random order: new defects per step',[round(S.mean(sf[i]),1) for i in range(len(sf))])
# union sizes
U={run:set().union(*rv.values()) for run,rv in runs.items()}
print('union per run mean %.1f'%S.mean(len(u) for u in U.values()),'| Sonnet alone %.1f'%S.mean(len(next(s for r,s in rv.items() if typ(r)=='S')) for rv in runs.values()))
# pooled discovery across runs (union of all reviewers of k runs)
allsets=list(U.values()); random.seed(1)
curve=[]
for k in range(1,len(allsets)+1):
    vals=[]
    for _ in range(300):
        pick=random.sample(allsets,k); vals.append(len(set().union(*pick)))
    curve.append(round(S.mean(vals),1))
print('pooled union of defects (of 44) after k runs (each run = 4 reviewers):',curve)
# per reviewer-slot discovery across all reviewers (72 reviewers) random order
revs=[s for rv in runs.values() for s in rv.values()]
c2=[]
for k in (1,2,4,8,12,16,24,36,54,len(revs)):
    c2.append((k,round(S.mean(len(set().union(*random.sample(revs,k))) for _ in range(300)),1)))
print('distinct defects after k random reviewer reports:',c2)
never=[d for d in DEF if not any(d in s for s in revs)]
print('defects never seen by any reviewer in R1:',len(never),never)
# detection frequency per defect, by type
freq={d:{'S':0,'H':0} for d in DEF}; n={'S':0,'H':0}
for rv in runs.values():
    for r,s in rv.items():
        n[typ(r)]+=1
        for d in s: freq[d][typ(r)]+=1
print('reviewer counts',n)
# conversion detected -> fixed (ab5 runs)
byk=collections.defaultdict(lambda:[0,0])
for run,rv in runs.items():
    if run not in fixed: continue
    for d in DEF:
        k=sum(1 for s in rv.values() if d in s)
        byk[min(k,3)][0]+=1; byk[min(k,3)][1]+= d in fixed[run]
print('P(fixed | #reviewers who raised it) over ab5 runs (k=0,1,2,3+):',{k:(v[0],round(v[1]/v[0],2)) for k,v in sorted(byk.items())})
bys=collections.defaultdict(lambda:[0,0])
for run,rv in runs.items():
    if run not in fixed: continue
    for d in DEF:
        if any(d in s for r,s in rv.items() if typ(r)=='S'): c='S raised'
        elif any(d in s for s in rv.values()): c='only H raised'
        else: c='none'
        bys[c][0]+=1; bys[c][1]+= d in fixed[run]
print('by who raised:',{k:(v[0],round(v[1]/v[0],2)) for k,v in bys.items()})
# expected-fix model: per-defect detection prob per reviewer type
q={d:{T:(freq[d][T]+0.5)/(n[T]+1) for T in 'SH'} for d in DEF}
pk={k:(v[1]+0.5)/(v[0]+1) for k,v in byk.items()}
def exp_fixed(nS,nH):
    tot=0
    for d in DEF:
        # distribution of detectors count (poisson-binomial)
        ps=[q[d]['S']]*nS+[q[d]['H']]*nH
        dist=[1.0]
        for p in ps:
            nd=[0]*(len(dist)+1)
            for i,x in enumerate(dist): nd[i]+=x*(1-p); nd[i+1]+=x*p
            dist=nd
        tot+=sum(x*pk[min(i,3)] for i,x in enumerate(dist))
    return tot
base=exp_fixed(1,3)
print('model expected fixed, panel 1S+3H: %.1f (observed ab5 runs mean %.1f)'%(base,S.mean(len(v) for v in fixed.values())))
for nS,nH in [(2,3),(3,3),(1,4),(1,6),(2,4),(2,6),(3,6),(1,8)]:
    e=exp_fixed(nS,nH); print(f'  {nS}S+{nH}H: expected fixed {e:.1f}  (+{e-base:.1f})   detected-union {sum(1-math.prod(1-p for p in [q[d]["S"]]*nS+[q[d]["H"]]*nH) for d in DEF):.1f}' if False else f'  {nS}S+{nH}H: expected fixed {e:.1f} (+{e-base:.1f})')
