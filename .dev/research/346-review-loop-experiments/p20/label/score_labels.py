import json,collections,math
key=json.load(open('sample_key.json'))
lab={}
for b in (1,2,3):
    for x in json.load(open(f'labels_b{b}.json'))['labels']: lab[x['label_id']]=x
assert set(lab)==set(key), (len(lab),len(key))
def wilson(k,n,z=1.645):
    if n==0: return (float('nan'),)*2
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); r=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return ((c-r)/d,(c+r)/d)
tab=collections.defaultdict(collections.Counter)
for lid,k in key.items(): tab[k['jev']][lab[lid]['label']]+=1
for j in ('cannot_pass','can_pass','cannot_discriminate'):
    print(j,dict(tab[j]),'n=',sum(tab[j].values()))
# Jev cannot_pass precision: opus says there IS a flaw (cannot_pass or cannot_discriminate)
cp=tab['cannot_pass']; n=sum(cp.values()); k=cp['cannot_pass']+cp['cannot_discriminate']
print('Jev cannot_pass: Opus agrees flawed %d/%d = %.0f%% (90%% CI %.0f-%.0f%%); exact cannot_pass %d/%d'%(k,n,100*k/n,*[100*v for v in wilson(k,n)],cp['cannot_pass'],n))
# Jev can_pass: Opus says can_pass?
ok=tab['can_pass']; n=sum(ok.values()); print('Jev can_pass: Opus can_pass %d/%d'%(ok['can_pass'],n))
cd=tab['cannot_discriminate']; n=sum(cd.values()); print('Jev cannot_discriminate: Opus flawed(cannot_pass/cannot_discriminate) %d/%d'%(cd['cannot_pass']+cd['cannot_discriminate'],n))
# population estimate: weights = stratum sizes in the 242 unique usable packets
N={'cannot_pass':220,'can_pass':16,'cannot_discriminate':6}
flawed_rate={j:(sum(c[l] for l in ('cannot_pass','cannot_discriminate'))/sum(c.values())) for j,c in tab.items()}
est_flawed=sum(N[j]*flawed_rate[j] for j in N)
print('est. truly flawed packets among 242 usable:',round(est_flawed),'=> overall flawed %.0f%%'%(100*est_flawed/242))
tp=N['cannot_pass']*flawed_rate['cannot_pass']+N['cannot_discriminate']*flawed_rate['cannot_discriminate']
flagged=N['cannot_pass']+N['cannot_discriminate']
print('Jev flagged (cannot_pass+cannot_discriminate)=%d, est. precision %.0f%%; est. recall (flagged-true / all-true) %.0f%%'%(flagged,100*tp/flagged,100*tp/est_flawed))
# confidence relation: Opus confidence
import statistics
print('Opus mean confidence',round(statistics.mean(x['confidence'] for x in lab.values()),2))
# list the disagreements
for lid,k in sorted(key.items()):
    flaw=lab[lid]['label'] in ('cannot_pass','cannot_discriminate'); jflaw=k['jev'] in ('cannot_pass','cannot_discriminate')
    if flaw!=jflaw: print('DISAGREE',lid,k['row'],'jev',k['jev'],'opus',lab[lid]['label'],'|',lab[lid]['reason'][:170])
