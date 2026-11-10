import json,glob,collections,random,sys
sys.argv=['x','out']
import aggregate as A
key=A.key; sev=A.sev; RES=A.RES
sup=json.load(open('defect_support.json'))
def subset(minfam): return {i for i,v in sup.items() if len(v['arms'])>=minfam}
def rows_for(ids):
    out=collections.defaultdict(list)
    for f in glob.glob('out/s*.json'):
        d=json.load(open(f)); a=key[d['sid']]['arm']
        st={x['id']:x['status'] for x in d['defects'] if x['id'] in ids}
        out[a].append(dict(blk=sum(1 for i,s in st.items() if sev[i]=='blocking' and s in RES),
                           w=sum(A.W[sev[i]] for i,s in st.items() if s in RES),
                           fixed=sum(1 for s in st.values() if s in('FIXED','DELETED_OK'))))
    return out
def perm(a,b,n=20000,seed=1):
    rnd=random.Random(seed); obs=sum(a)/len(a)-sum(b)/len(b); pool=a+b; c=0
    for _ in range(n):
        rnd.shuffle(pool); x=pool[:len(a)]; y=pool[len(a):]
        if abs(sum(x)/len(x)-sum(y)/len(y))>=abs(obs)-1e-12: c+=1
    return obs,c/n
for minfam in (1,2,3):
    ids=subset(minfam); nb=sum(1 for i in ids if sev[i]=='blocking')
    R=rows_for(ids)
    print(f'\n=== core ledger: defects supported by >= {minfam} arm families: {len(ids)} defects ({nb} blocking)')
    print('%-10s %2s %9s %9s %7s %s'%('arm','n','resid_blk','resid_w','fixed','diff_w vs ref (p)'))
    for a in ['base-fresh','stage2','ab1','ab2','ab3','ab4','pn1','pn2','haiku-base','ab1h','ab2h','ab3h','ab4h']:
        v=R[a]; m=lambda k:sum(x[k] for x in v)/len(v)
        ref='haiku-base' if a.endswith('h') else 'base-fresh'
        if a in('base-fresh','haiku-base'): ps=''
        else:
            o,p=perm([x['w'] for x in v],[x['w'] for x in R[ref]]); ps='%+.1f (p=%.3f)'%(o,p)
        print('%-10s %2d %9.1f %9.1f %7.1f %s'%(a,len(v),m('blk'),m('w'),m('fixed'),ps))
