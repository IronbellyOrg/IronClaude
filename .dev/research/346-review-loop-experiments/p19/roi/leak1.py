exec(open('analyze.py').read().split("# 1 yield")[0])
import re,datetime,itertools,difflib
def spear(xs,ys):
    def rk(v):
        o=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v); i=0
        while i<len(o):
            j=i
            while j+1<len(o) and v[o[j+1]]==v[o[i]]: j+=1
            for t in range(i,j+1): r[o[t]]=(i+j)/2
            i=j+1
        return r
    a,b=rk(xs),rk(ys);n=len(a);ma,mb=sum(a)/n,sum(b)/n
    c=sum((x-ma)*(y-mb) for x,y in zip(a,b));s=(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5
    return c/s if s else 0
L=[json.loads(l) for l in open(f'{SP}/p18/ab5/launch-ledger.jsonl')]
start={}
for e in L:
    t=datetime.datetime.fromisoformat(e['t']).timestamp()
    start.setdefault(e['run'],t)
for var,pre in (('panel','d5-'),('full','d5f-')):
    rs=sorted([r for r in fixed if r.startswith(pre)],key=lambda r:int(r.split('-r')[1]))
    idx=[int(r.split('-r')[1]) for r in rs]; st=[start[r] for r in rs]
    det=[len(U[r]) if False else len(set().union(*runs[r].values())) for r in rs]
    fx=[len(fixed[r]) for r in rs]
    conv=[len(fixed[r])/max(1,len(set().union(*runs[r].values()))) for r in rs]
    sonn=[len([s for k,s in runs[r].items() if typ(k)=='S'][0]) for r in rs]
    print(var,'runs',rs)
    print('  start offset (min):',[round((t-min(start.values()))/60) for t in st])
    print('  detected union:',det,'rho(idx)=%.2f'%spear(idx,det))
    print('  sonnet distinct:',sonn,'rho(idx)=%.2f'%spear(idx,sonn))
    print('  fixed:',fx,'rho(idx)=%.2f'%spear(idx,fx))
    print('  fixed/detected:',[round(c,2) for c in conv],'rho(idx)=%.2f'%spear(idx,conv))
# final-spec similarity on added lines
orig=open(f'{SP}/p17/in/spec-original.md').read().splitlines()
def added(path):
    new=open(path).read().splitlines()
    sm=difflib.SequenceMatcher(None,orig,new,autojunk=False); out=set()
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag in('replace','insert'):
            for l in new[j1:j2]:
                l=re.sub(r'\s+',' ',l).strip()
                if len(l)>25: out.add(l)
    return out
sets={}
for sid,k in key.items():
    if k['arm'].startswith('ab5') or k['arm'] in('ab4','pn1'): sets[(k['arm'],k['run'],sid)]=added(f'{SP}/p17/score/in/{sid}.md')
def jac(a,b): return len(a&b)/len(a|b) if a|b else 0
within=collections.defaultdict(list);cross=[]
items=list(sets.items())
for (ka,sa),(kb,sb) in itertools.combinations(items,2):
    j=jac(sa,sb)
    if ka[0]==kb[0]: within[ka[0]].append(j)
    else: cross.append(j)
print('mean Jaccard of added lines: within arm',{a:round(S.mean(v),3) for a,v in within.items()},'across arms %.3f'%S.mean(cross))
# time proximity effect inside ab5 (12 runs)
pairs=[]
ab5=[(k[1],s) for k,s in items if k[0].startswith('ab5')]
for (ra,sa),(rb,sb) in itertools.combinations(ab5,2):
    if ra in start and rb in start: pairs.append((abs(start[ra]-start[rb])/60,jac(sa,sb),ra[:3]==rb[:3] or ra.startswith('d5f')==rb.startswith('d5f')))
print('rho(time gap, Jaccard) over ab5 pairs: %.2f (n=%d)'%(spear([p[0] for p in pairs],[p[1] for p in pairs]),len(pairs)))
same=[p for p in pairs if p[2]]; print('  same-variant pairs rho %.2f n=%d'%(spear([p[0] for p in same],[p[1] for p in same]),len(same)))
