exec(open('leak1.py').read().split("L=[json.loads")[0])
import subprocess
rows=[]
for f in glob.glob(f'{SP}/p17/score/out/s*.json'):
    d=json.load(open(f)); sid=d['sid']; k=key[sid]
    fx=sum(1 for x in d['defects'] if x['status'] in('FIXED','DELETED_OK'))
    df=open(f'{SP}/p17/score/in/{sid}.diff').read().splitlines()
    ch=sum(1 for l in df if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++','---')))
    rows.append((k['arm'],k['run'],sid,fx,ch))
print('pooled specs',len(rows),'rho(fixed, changed lines)=%.2f'%spear([r[3] for r in rows],[r[4] for r in rows]))
by=collections.defaultdict(list)
for r in rows: by[r[0]].append(r)
for a in ['base-fresh','ab4','pn1','ab5-panel','ab5-full']:
    v=by[a]; print('%-10s rho %.2f  mean changed lines %.0f  mean fixed %.1f  fixed per 100 changed lines %.1f'%(a,spear([x[3] for x in v],[x[4] for x in v]),S.mean(x[4] for x in v),S.mean(x[3] for x in v),100*S.mean(x[3] for x in v)/S.mean(x[4] for x in v)))
for a in ['ab5-panel','ab5-full']:
    print(a,[(x[1],x[3],x[4]) for x in sorted(by[a],key=lambda x:x[1])])
