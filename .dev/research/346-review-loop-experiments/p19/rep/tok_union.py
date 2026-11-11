import json,glob,collections,os,random
def mean(v): return sum(v)/len(v)
armof=lambda run:'pn1o' if run.startswith('o2') else 'pn1d2'
res={}
for st in sorted(glob.glob('pn1*/runs/*/state.json')):
    s=json.load(open(st)); run=s['run']; lane=collections.Counter()
    for step,v in s['log'].items():
        t=v.get('tokens') or {}
        if not t or step.startswith('AUD'): continue
        k='H' if 'haiku' in (t.get('model') or '') else 'S'
        lane[k]+=t.get('out',0)+t.get('in',0)+t.get('cache_write',0)
    res[run]=lane
for arm in ('pn1o','pn1d2'):
    rs=[v for k,v in res.items() if armof(k)==arm]
    print(arm,'primary(S) %.0fk  parallel(H) %.0fk  total %.0fk'%(mean([r['S'] for r in rs])/1e3,mean([r['H'] for r in rs])/1e3,mean([r['S']+r['H'] for r in rs])/1e3))
# defect-level union
os.chdir('/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p17/score')
key=json.load(open('key.json'))
fx=collections.defaultdict(lambda:collections.defaultdict(set))
for n in range(94,106):
    d=json.load(open(f'out/s{n}.json')); arm=key[f's{n}']['arm']
    for x in d['defects']:
        if x['status'] in ('FIXED','DELETED_OK'): fx[arm][x['id']].add(f's{n}')
for arm in ('pn1o','pn1d2'):
    u=fx[arm]; freq=collections.Counter(len(v) for v in u.values())
    print(arm,'union fixed',len(u),'fixed in all6',freq[6],'in exactly1',freq[1],'dist',dict(sorted(freq.items())))
both=set(fx['pn1o'])|set(fx['pn1d2'])
print('union both arms',len(both),'only o',len(set(fx['pn1o'])-set(fx['pn1d2'])),'only d2',len(set(fx['pn1d2'])-set(fx['pn1o'])))
# per-defect fix rate difference
rates=[(i,len(fx['pn1d2'].get(i,()))/6,len(fx['pn1o'].get(i,()))/6) for i in sorted(both)]
ups=[(i,d,o) for i,d,o in rates if d-o>=0.5]; dn=[(i,d,o) for i,d,o in rates if o-d>=0.5]
print('defects fixed >=50pts more often by d2:',ups); print('by o:',dn)
# first-3 vs other-9 perm
slots=json.load(open('../../p19/rep/slots.json')); order={b['run']:b['i'] for b in slots['built']}
import sys; sys.path.insert(0,'.'); sys.argv=['x','out']; import aggregate as A
fixed={r['run']:r['fixed'] for s,r in A.rows.items() if int(s[1:])>=94}
a=[fixed[r] for r in fixed if order[r]<3]; b=[fixed[r] for r in fixed if order[r]>=3]
rnd=random.Random(1); allv=a+b; obs=mean(a)-mean(b); c=0
for _ in range(50000):
    rnd.shuffle(allv)
    if abs(mean(allv[:3])-mean(allv[3:]))>=abs(obs)-1e-12:c+=1
print('first3(k=3) vs other9 fixed diff %+.2f p=%.3f'%(obs,c/50000))
