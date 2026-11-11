"""Aggregate ledger scores per arm. Usage: python3 aggregate.py [outdir]"""
import json,glob,sys,os,random,collections,itertools
outdir=sys.argv[1] if len(sys.argv)>1 else 'out'
key=json.load(open('key.json')); led=json.load(open('ledger-blind.json'))
sev={d['id']:d['severity'] for d in led['defects']}
W={'blocking':3,'medium':2,'minor':1}   # severity weights for the weighted score
RES={'PRESENT','PARTIAL','WORSE','MOOT_BAD'}   # residual statuses
rows={}
for f in sorted(glob.glob(outdir+'/s*.json')):
    d=json.load(open(f)); sid=d['sid']
    st={x['id']:x['status'] for x in d['defects']}
    r=dict(sid=sid,arm=key[sid]['arm'],run=key[sid]['run'])
    r['resid_blk']=sum(1 for i,s in st.items() if sev[i]=='blocking' and s in RES)
    r['resid_blk_strict']=sum(1 for i,s in st.items() if sev[i]=='blocking' and s in ('PRESENT','WORSE','MOOT_BAD'))
    r['resid_w']=sum(W[sev[i]] for i,s in st.items() if s in RES)
    r['resid_all']=sum(1 for s in st.values() if s in RES)
    r['fixed']=sum(1 for s in st.values() if s in ('FIXED','DELETED_OK'))
    r['worse']=sum(1 for s in st.values() if s in ('WORSE','MOOT_BAD'))
    r['intro']=sum(1 for x in d['introduced'] if x['status']=='PRESENT')
    r['other_new']=len(d.get('other_new_defects',[]))
    rows[sid]=r
if __name__=='__main__':
    arms=collections.defaultdict(list)
    for r in rows.values(): arms[r['arm']].append(r)
    def mean(v): return sum(v)/len(v) if v else float('nan')
    def sd(v):
        m=mean(v); return (sum((x-m)**2 for x in v)/(len(v)-1))**.5 if len(v)>1 else float('nan')
    print('n specs',len(rows))
    print('%-11s %2s %8s %8s %8s %8s %6s %6s %6s'%('arm','n','blk_res','blk_stri','weighted','allres','fixed','intro','new'))
    for a in ['stage2','base-fresh','ab1','ab2','ab3','ab4','pn1','pn2','haiku-base','ab1h','ab2h','ab3h','ab4h']:
        v=arms.get(a,[]); 
        if not v: continue
        print('%-11s %2d %5.1f±%.1f %8.1f %8.1f %8.1f %6.1f %6.1f %6.1f'%(a,len(v),mean([x['resid_blk'] for x in v]),sd([x['resid_blk'] for x in v]),mean([x['resid_blk_strict'] for x in v]),mean([x['resid_w'] for x in v]),mean([x['resid_all'] for x in v]),mean([x['fixed'] for x in v]),mean([x['intro'] for x in v]),mean([x['other_new'] for x in v])))
