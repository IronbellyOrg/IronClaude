import json,sys,random,collections,glob,os
os.chdir('/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p17/score')
sys.argv=['x','out']
sys.path.insert(0,'.')
import aggregate as A
rows=A.rows
slots=json.load(open('../../p19/rep/slots.json'))
built={b['run']:(b['i'],b['t']) for b in slots['built']}
new={s:r for s,r in rows.items() if int(s[1:])>=94}
for s,r in sorted(new.items(), key=lambda x:(x[1]['arm'],x[1]['run'])):
    r['i'],r['t']=built[r['run']]
    print(s,r['arm'],r['run'],'slot',r['i'],r['t'][11:16],'fixed',r['fixed'],'resid_w',r['resid_w'],'blk',r['resid_blk'],'intro',r['intro'],'new',r['other_new'])
def mean(v): return sum(v)/len(v)
def sd(v):
    m=mean(v); return (sum((x-m)**2 for x in v)/(len(v)-1))**.5
def perm(a,b,n=50000,seed=1):
    rnd=random.Random(seed); obs=mean(a)-mean(b); pool=a+b; c=0
    for _ in range(n):
        rnd.shuffle(pool); x=pool[:len(a)]; y=pool[len(a):]
        if abs(mean(x)-mean(y))>=abs(obs)-1e-12: c+=1
    return obs,c/n
by=collections.defaultdict(list)
for r in rows.values(): by[r['arm']].append(r)
print()
for a in ['pn1','pn1d','pn1m','pn1o','pn1d2']:
    v=by.get(a,[])
    if v: print('%-6s n=%d fixed %.1f±%.1f  resid_w %.1f±%.1f  resid_blk %.1f intro %.1f'%(a,len(v),mean([x['fixed'] for x in v]),sd([x['fixed'] for x in v]) if len(v)>1 else 0,mean([x['resid_w'] for x in v]),sd([x['resid_w'] for x in v]) if len(v)>1 else 0,mean([x['resid_blk'] for x in v]),mean([x['intro'] for x in v])))
print()
def cmp(a,b,k):
    x=[r[k] for r in by[a]]; y=[r[k] for r in by[b]]
    o,p=perm(x,y); print(f'{a} vs {b} {k}: diff {o:+.2f} p={p:.3f}')
for k in ('fixed','resid_w'):
    cmp('pn1d2','pn1o',k)
    cmp('pn1o','pn1',k); cmp('pn1d2','pn1d',k); cmp('pn1d2','pn1',k); cmp('pn1o','pn1d',k)
# pooled same-protocol: pn1+pn1o vs pn1d+pn1d2
for k in ('fixed','resid_w'):
    x=[r[k] for a in ('pn1d','pn1d2') for r in by[a]]; y=[r[k] for a in ('pn1','pn1o') for r in by[a]]
    o,p=perm(x,y); print(f'pooled 1S+6H (pn1d+pn1d2, n={len(x)}) vs 1S+3H (pn1+pn1o, n={len(y)}) {k}: diff {o:+.2f} p={p:.3f}')
# run-order effect within replicate
import itertools
def rank(v):
    s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v)
    for k,i in enumerate(s): r[i]=k
    return r
def spearman(x,y):
    rx,ry=rank(x),rank(y); mx,my=mean(rx),mean(ry)
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry)); den=(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**.5
    return num/den
R=sorted(new.values(),key=lambda r:r['i'])
print('\nstart-order effect (slot index vs fixed): all12 rho=%.2f'%spearman([r['i'] for r in R],[r['fixed'] for r in R]))
for a in ('pn1o','pn1d2'):
    S=[r for r in R if r['arm']==a]
    print(a,'rho(slot,fixed)=%.2f'%spearman([r['i'] for r in S],[r['fixed'] for r in S]),[ (r['i'],r['fixed']) for r in S])
early=[r for r in R if r['i']<3]; late=[r for r in R if r['i']>=3]
print('first3 (k=3) fixed',[r['fixed'] for r in early],'mean %.1f ; other9 mean %.1f'%(mean([r['fixed'] for r in early]),mean([r['fixed'] for r in late])))
