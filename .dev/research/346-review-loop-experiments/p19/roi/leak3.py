exec(open('leak1.py').read().split("L=[json.loads")[0])
led={d['id']:d for d in json.load(open(f'{SP}/p17/ledger.json'))['defects']}
def hunks(diff):
    ranges=[]
    for l in diff:
        m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',l)
        if m: ranges.append((int(m.group(1)),int(m.group(1))+int(m.group(2) or 1)))
    return ranges
def touched(lines,rng,pad=5):
    return any(a-pad<=ln<=b+pad for ln in lines for a,b in rng)
stat=collections.defaultdict(lambda:collections.Counter())
quote_ok=collections.Counter(); quote_tot=collections.Counter()
for f in glob.glob(f'{SP}/p17/score/out/s*.json'):
    d=json.load(open(f)); sid=d['sid']; k=key[sid]; arm=k['arm']
    diff=open(f'{SP}/p17/score/in/{sid}.diff').read().splitlines(); rng=hunks(diff)
    rev=open(f'{SP}/p17/score/in/{sid}.md').read()
    revn=re.sub(r'\s+',' ',rev)
    for x in d['defects']:
        st='FIXED' if x['status'] in('FIXED','DELETED_OK') else ('PARTIAL' if x['status']=='PARTIAL' else 'PRESENT+')
        lines=led[x['id']]['spec_lines']
        t=touched(lines,rng)
        stat[arm][(st,t)]+=1
        if st=='FIXED':
            qs=[q for q in re.findall(r'`([^`]{20,200})`|"([^"]{20,200})"',x['evidence']) for q in q if q]
            for q in qs:
                quote_tot[arm]+=1
                if re.sub(r'\s+',' ',q).strip() in revn: quote_ok[arm]+=1
print('FIXED claims whose defect lines are within +-5 of a diff hunk (else the fix would be elsewhere or unsupported)')
for arm in ['base-fresh','ab4','pn1','ab5-panel','ab5-full']:
    c=stat[arm]; nf=c[('FIXED',True)]+c[('FIXED',False)]; npr=c[('PRESENT+',True)]+c[('PRESENT+',False)]
    print('%-10s FIXED %3d, near a hunk %.0f%% | PRESENT/WORSE %3d, near a hunk %.0f%% | quotes in FIXED evidence found verbatim in revised spec: %d/%d'%(arm,nf,100*c[('FIXED',True)]/max(nf,1),npr,100*c[('PRESENT+',True)]/max(npr,1),quote_ok[arm],quote_tot[arm]))
