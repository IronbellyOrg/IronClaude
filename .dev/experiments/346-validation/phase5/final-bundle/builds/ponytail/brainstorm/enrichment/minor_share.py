import difflib, re, sys
def run(v_old, v_new, minor, blocking):
    a=open(v_old,encoding='utf-8').read().splitlines(); b=open(v_new,encoding='utf-8').read().splitlines()
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    tot=0; res={'minor-only':0,'blocking-involved':0,'untagged':0}
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        old="\n".join(a[i1:i2]); new="\n".join(b[j1:j2])
        # bytes added = changed chars via char-level diff
        cs=difflib.SequenceMatcher(None,old,new,autojunk=False)
        added=sum((d2-d1) for o,c1,c2,d1,d2 in cs.get_opcodes() if o in('insert','replace'))
        ids=set(re.findall(r'\b([A-Z]{1,2}[0-9]{1,2})\b',new))
        hit_b=ids&blocking; hit_m=ids&minor
        k='blocking-involved' if hit_b else ('minor-only' if hit_m else 'untagged')
        res[k]+=added; tot+=added
    print(v_new.split('/')[-6], {k:(v, round(v/tot,2) if tot else 0) for k,v in res.items()}, 'total_added', tot)
R='/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/'
run(R+'spec-v2-after-round1.md',R+'spec-v3-after-round2.md',{'N7','N8','N9','N10','N11','C9','C12','C13','C14'},{'N1','N2','N3','N4','N5','N6'})
run(R+'spec-v1-draft.md',R+'spec-v2-after-round1.md',{f'F{i}' for i in range(14,23)},{f'F{i}' for i in range(1,14)})
