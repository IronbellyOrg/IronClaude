"""Second design set: human supervision across orchestrators, offline and read-only."""
from canvas import selected_summary
from fixtures import metrics

DIGITS={"0":["███","█ █","█ █","█ █","███"],"1":[" █ ","██ "," █ "," █ ","███"],"2":["███","  █","███","█  ","███"],"3":["███","  █","███","  █","███"],"4":["█ █","█ █","███","  █","  █"],"5":["███","█  ","███","  █","███"],"6":["███","█  ","███","█ █","███"],"7":["███","  █","  █","  █","  █"],"8":["███","█ █","███","█ █","███"],"9":["███","█ █","███","  █","███"]}
def big(c,x,y,n,color="accent"):
    for k,ch in enumerate(str(n)):
        for j,line in enumerate(DIGITS[ch]):c.text(x+k*4,y+j,line,color)
def frame(c,f,m,name):c.header(name,f,m);c.footer()
def qlines(f):
    return [f"{q['id']} {q['age_min']:>2}m  {q['question']}" for q in f['requests']]
def scope(c,f,y=6):selected_summary(c,f,y)
def listbox(c,x,y,w,h,title,lines,color="line",heavy=False):
    c.panel(x,y,w,h,title,color,heavy)
    shown=min(len(lines),h-4)
    for i,line in enumerate(lines[:shown]):c.text(x+2,y+2+i,line,width=w-4)
    c.text(x+2,y+h-2,f"{shown}/{len(lines)} lines shown", "muted",width=w-4)
def owners(f,m):
    return [(o,[s for s in m['sessions'] if s['owner']==o['id']]) for o in f['orchestrators']]
def evidence_rows(m):
    return [f"{s['id']} {s['owner']}  {s['result'] or 'no report':10}  {s['admission']}" for s in m['sessions'] if s['result']]
def narrow(c,f,m,name,lines):
    frame(c,f,m,name);scope(c,f)
    listbox(c,1,11,c.w-2,c.h-15,"SELECTED SIGNALS",lines,"accent")

def leverage(c,f,m):
    name="Leverage Board";qs=f['requests']
    if c.w<116:return narrow(c,f,m,name,qlines(f)+[f"Distinct affected sessions: {m['affected']}","Overlap is counted once, not once per request.","Decision owners are humans; requesters are separate."])
    frame(c,f,m,name)
    c.panel(1,5,c.w-2,11,"YOUR NEXT ANSWER", "warn",True)
    big(c,5,8,m['affected'],"warn");c.text(20,8,"UNIQUE SESSIONS AFFECTED", "ink",True)
    c.text(20,10,"Across observed questions; not additive by question", "muted",width=c.w-25)
    c.text(20,12,"Answering may unblock work; it does not approve results.",width=c.w-25)
    left=c.w*2//3
    for i,q in enumerate(qs[:3]):
        y=18+i*7;c.panel(1,y,left-3,6,q['id']+" / "+q['owner'],"warn")
        c.text(4,y+2,q['question'],bold=True,width=left-8)
        c.text(4,y+3,f"{q['age_min']}m | {len(q['affected'])} sessions | {q['requester']} -> human",width=left-8)
    listbox(c,left,18,c.w-left-1,21,"BOUNDARIES",["Declared effects only","No estimated completion ETA","No automatic approvals","Messages: "+f['sources']['messages']['coverage'],"Evidence in inspector","Full stable IDs available","Orca remains authority"],"accent")

def attention(c,f,m):
    name="Attention Ledger"
    if c.w<116:return narrow(c,f,m,name,qlines(f)+["Questions stay until explicit resolution.","No reply observed is not delivery failure."])
    frame(c,f,m,name);right=c.w-43
    c.panel(1,5,right-3,c.h-9,"OPEN HUMAN QUESTIONS", "warn",True)
    for i,q in enumerate(f['requests']):
        y=8+i*8;c.text(4,y,f"{q['age_min']:02} MIN", "warn",True);c.text(15,y,q['question'],bold=True,width=right-21)
        c.text(15,y+2,q['requester']+" requests / "+q['owner'],width=right-21)
        c.text(15,y+3,"Affected: "+", ".join(q['affected']),"muted",width=right-21)
        c.line(4,y+5,right-10)
    c.panel(right,5,42,13,"SEEN IS NOT RESOLVED","accent")
    big(c,right+4,8,len(f['requests']),"warn");c.text(right+13,9,"observed questions",width=26)
    listbox(c,right,20,42,18,"RETAIN CONTEXT",["original question","original age","acting owner","requesting orchestrator","affected stable IDs","source coverage","explicit closure evidence"],"line")

def handoffs(c,f,m):
    name="Handoff Switchboard"
    if c.w<116:return narrow(c,f,m,name,[f"{e['from']} -> {e['to']} / {e['reason']}" for e in f['edges']]+qlines(f))
    frame(c,f,m,name);scope(c,f,6)
    c.line(2,10,c.w-4,"accent",True)
    for i,e in enumerate(f['edges']):
        y=13+i*8;mid=c.w//2
        c.panel(2,y,25,5,e['from'],"accent",True);c.text(5,y+2,"DECLARED HANDOFF",width=20)
        c.text(27,y+2,"━"*(mid-28)+"◉","accent")
        c.text(mid+1,y+2,"━"*(c.w-mid-30)+"▶","accent")
        c.panel(c.w-28,y,26,5,e['to'],"accent",True);c.text(c.w-25,y+2,f"{len(e['sessions'])} affected",width=20)
        c.text(30,y,e['reason'],"warn",True,width=c.w-62)
        c.text(30,y+4,e['evidence'],"muted",width=c.w-62)
    c.text(3,c.h-5,"Cables show recorded dependencies, not communication volume or inferred topology.","muted",width=c.w-6)

def loops(c,f,m):
    name="Loop Detector";rows=[s for s in m['sessions'] if s['retry_count']]
    lines=[f"{s['id']} / {s['owner']} / {s['retry_count']} recorded retries" for s in rows]
    if c.w<116:return narrow(c,f,m,name,lines+["Source: authoritative fixture attempt log","Repeated output alone is not a retry."]+qlines(f))
    frame(c,f,m,name);scope(c,f)
    c.panel(2,11,c.w-4,15,"REPEATED ATTEMPT SIGNAL", "bad",True)
    if rows:
        s=rows[0];c.text(6,14,f"{s['id']}  /  {s['owner']}","bad",True)
        x=6
        for i in range(min(s['retry_count'],5)):
            c.panel(x,17,25,5,f"RETRY {i+1}","bad");c.text(x+3,19,"recorded by source",width=20)
            if i+1<min(s['retry_count'],5):c.text(x+25,19,"━━▶","warn")
            x+=30
        c.text(6,24,s['retry_source'],"muted",width=c.w-12)
    else:c.text(6,15,"No retry records in this fixture; not proof none occurred.",width=c.w-12)
    listbox(c,2,28,c.w//2-3,12,"INVESTIGATE",["Compare failure signatures","Inspect prior diagnosis","Check superseded attempt identity","Use existing evidence, not automatic retry"],"accent")
    listbox(c,c.w//2+1,28,c.w//2-3,12,"DO NOT INFER",["Quiet output != failure","Same text != repeated execution","Late heartbeat != dead worker","Observer cannot restart anything"],"line")

def collision(c,f,m):
    name="Collision Lens";groups={}
    for t in f['worktrees']:
        for p in t['paths']:groups.setdefault(p,[]).append(t)
    overlaps=[(p,ts) for p,ts in groups.items() if len(ts)>1]
    lines=[f"{p} / {len(ts)} worktrees / conflict NOT established" for p,ts in overlaps]
    if c.w<116:return narrow(c,f,m,name,lines+["Dirty is not dangerous; overlap is not conflict."]+qlines(f))
    frame(c,f,m,name);scope(c,f)
    c.panel(2,11,c.w-4,8,"SHARED PATH / NOT A PROVEN CONFLICT","warn",True)
    for i,(p,ts) in enumerate(overlaps[:3]):c.text(6,14+i,f"{p}     {len(ts)} distinct worktrees",bold=True,width=c.w-12)
    third=(c.w-8)//3
    trees=overlaps[0][1] if overlaps else []
    for i,t in enumerate(trees[:3]):
        x=2+i*(third+2);c.panel(x,21,third,15,t['id'],"accent")
        c.lines(x+2,24,["BRANCH",t['branch'],"HEAD  "+t['head'],"BASE  "+t['base'],"dirty: "+str(t['dirty']),"policy: "+t['policy'],"conflict: not established"],third-4)
    c.text(3,39,"Inspect actual diffs before making a conflict claim. No merge or worktree actions.","muted",width=c.w-6)

def outcomes(c,f,m):
    name="Outcome Ledger";rows=evidence_rows(m)
    if c.w<116:return narrow(c,f,m,name,rows[:12]+[f"{len(rows)} total report records; inspector has all."])
    frame(c,f,m,name);scope(c,f)
    c.panel(2,11,c.w-4,c.h-15,"SETTLEMENT  /  REPORT  /  ADMISSION", "accent",True)
    c.text(5,13,"SESSION   LIFECYCLE     REPORT        PACKET             ADMISSION", "muted")
    entries=[s for s in m['sessions'] if s['result']]
    for i,s in enumerate(entries[:c.h-20]):
        c.text(5,15+i,f"{s['id']:9} {s['lifecycle']:13} {s['result']:13} {s['evidence']:18} {s['admission']}", "bad" if s['result']=='failed' else "ink",width=c.w-10)
    c.text(5,c.h-6,f"{min(len(entries),c.h-20)}/{len(entries)} shown | failed reports retain evidence | complete packet != admission","muted",width=c.w-10)

def drift(c,f,m):
    name="Revision Drift";stale=[s for s in m['sessions'] if s['check_revision']!=s['revision']]
    if c.w<116:return narrow(c,f,m,name,[f"{s['id']} checked {s['check_revision']} -> now {s['revision']}" for s in stale]+["Passing old checks do not prove current readiness."])
    frame(c,f,m,name);scope(c,f)
    c.panel(2,11,c.w-4,11,"PROOF DOES NOT FOLLOW A MOVING HEAD", "warn",True)
    big(c,7,14,len(stale),"warn");c.text(25,15,"REVISION MISMATCHES",bold=True)
    c.text(25,18,"Test outcome and revision match are separate; stale source remains separate too.","muted",width=c.w-30)
    for i,s in enumerate(stale[:7]):
        y=24+i*2;c.text(5,y,s['id']+"  "+s['check_revision'],"muted")
        c.text(30,y,"──────────▶", "warn");c.text(46,y,s['revision'],bold=True)
        c.text(70,y,"tests: "+str(s['tests'] or 'unknown')+" / NOT current proof", "warn",width=c.w-75)
    c.text(5,c.h-5,f"{min(7,len(stale))}/{len(stale)} mismatches shown; select a record for full evidence.","muted",width=c.w-10)

def pulse(c,f,m):
    name="Mission Pulse";groups=owners(f,m)
    if c.w<116:return narrow(c,f,m,name,[f"{o['name']} / {len(ss)} sessions / {sum(s['admission']=='admitted' for s in ss)} admitted" for o,ss in groups]+qlines(f))
    frame(c,f,m,name);scope(c,f)
    c.text(3,11,"OWNER             MISSION                   RUNNING    SETTLED    ADMITTED    UNKNOWN","muted")
    for i,(o,ss) in enumerate(groups):
        y=14+i*2
        if y>=c.h-6:break
        running=sum(s['lifecycle']=='running' for s in ss);settled=sum(s['lifecycle']=='settled' for s in ss);admit=sum(s['admission']=='admitted' for s in ss);unknown=sum(s['lifecycle']=='unknown' for s in ss)
        c.text(3,y,o['name'],"accent",True,width=16);c.text(21,y,o['mission'],width=25)
        c.text(49,y,f"{running:3}        {settled:3}        {admit:3}         {unknown:3}")
        c.line(3,y+1,c.w-6)
    c.text(3,c.h-5,"Admitted is a recorded subset, not an extra lifecycle bucket. Activity is not outcome.","muted",width=c.w-6)

def balance(c,f,m):
    name="Owner Load";groups=owners(f,m)
    if c.w<116:return narrow(c,f,m,name,[f"{o['name']} owns {len(ss)} sessions" for o,ss in groups]+["Ownership count is not capacity or utilization."]+qlines(f))
    frame(c,f,m,name);scope(c,f)
    w=c.w*2//3;c.panel(2,11,w-4,c.h-15,"OWNERSHIP DISTRIBUTION", "accent")
    high=max([len(ss) for _,ss in groups]+[1])
    for i,(o,ss) in enumerate(groups):
        y=14+i*2
        if y>=c.h-6:break
        c.text(5,y,o['name'],width=12);c.bar(19,y,len(ss),high,w-32);c.text(w-11,y,str(len(ss)))
    listbox(c,w,11,c.w-w-2,14,"INTERPRETATION",["Sessions per orchestrator","Not a capacity score","Not a scheduling proposal","Use uneven scenario to compare","Historical sessions excluded"],"warn")
    listbox(c,w,27,c.w-w-2,13,"ATTENTION",qlines(f),"line")

def shift(c,f,m):
    name="Shift Brief"
    frame(c,f,m,name)
    c.panel(2,5,c.w-4,11,"HANDOVER / OBSERVED ATTENTION", "warn",True)
    big(c,6,8,len(f['requests']),"warn");c.text(22,8,"QUESTIONS NEED A HUMAN",bold=True,width=c.w-27)
    c.text(22,10,"Messages "+f['sources']['messages']['coverage']+"; this is not an all-clear.","muted",width=c.w-27)
    if f['requests']:c.text(22,12,f['requests'][0]['question'],width=c.w-27)
    y=18
    for q in f['requests']:
        c.text(5,y,f"{q['id']} / {q['age_min']}m / {q['owner']}","warn",True,width=c.w-10)
        c.text(5,y+1,q['question'],width=c.w-10)
        c.text(5,y+2,"Affects "+", ".join(q['affected'])+" | "+q['evidence'],"muted",width=c.w-10);y+=5
    c.text(5,c.h-6,f"{m['failed']} failed reports retained / {m['stale']} stale / {m['frozen']} policy frozen",width=c.w-10)
    c.text(5,c.h-5,"Inspection only. Existing tools and humans retain every operational decision.","muted",width=c.w-10)

DESIGNS={}
for slug,name,fn,q,omits in [
 ("leverage-board","Leverage Board",leverage,"Which answer has the widest declared effect?","Routine worker output"),
 ("attention-ledger","Attention Ledger",attention,"Which human questions remain unanswered?","Resource telemetry"),
 ("handoff-switchboard","Handoff Switchboard",handoffs,"Which owner handoff carries a dependency?","Undeclared communication paths"),
 ("loop-detector","Loop Detector",loops,"Where does the authoritative log report retries?","Inferred retry automation"),
 ("collision-lens","Collision Lens",collision,"Which paths are touched by isolated worktrees?","Unproven merge-conflict claims"),
 ("outcome-ledger","Outcome Ledger",outcomes,"Was the finished assignment actually admitted?","Token and activity leaderboards"),
 ("revision-drift","Revision Drift",drift,"Which passing checks belong to an old head?","Automatic reruns"),
 ("mission-pulse","Mission Pulse",pulse,"Which missions are producing admitted outcomes?","Misleading completion percentages"),
 ("owner-load","Owner Load",balance,"How uneven is observed ownership?","Dispatch and capacity assumptions"),
 ("shift-brief","Shift Brief",shift,"What must the next human know?","Raw transcripts")]:
    DESIGNS[slug]={"name":name,"render":fn,"question":q,"omits":omits,"tradeoff":"A focused supervision lens omits secondary fleet detail; inspect records for full context.","data":"Declared synthetic owner/session/worktree/report relationships and source coverage.","missing":"Unknown stays unknown; source-loss and partial coverage remain visible. Narrow view prioritizes selected facts."}
