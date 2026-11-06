"""Five offline observation compositions; records are proposed synthetic schema."""


def _rows(m):
    return m.get("sessions", [])


def _owners(f, rows):
    return [(o, [s for s in rows if s.get("owner") == o.get("id")])
            for o in f.get("orchestrators", [])]


def _state(s):
    if s.get("result") == "failed": return "F", "bad"
    if s.get("policy") == "frozen": return "P", "frozen"
    return {"running": ("R", "accent"), "settled": ("S", "good")}.get(s.get("lifecycle"), ("?", "muted"))


def _request(c, f, x, y, w, h=7):
    c.panel(x, y, w, h, "HUMAN QUESTION", "warn", True)
    qs = f.get("requests", [])
    if not qs:
        c.text(x+2, y+2, "No requests observed in this fixture", "muted", width=w-4)
        c.text(x+2, y+3, "Absence is not complete message coverage", "muted", width=w-4)
        return
    q = qs[0]
    c.text(x+2, y+1, q.get("question", "Question unavailable"), "warn", True, w-4)
    c.text(x+2, y+2, "Owner: "+str(q.get("owner", "unknown")), width=w-4)
    c.text(x+2, y+3, f"Scope: {len(q.get('affected', []))} sessions | observed {q.get('age_min', '?')}m ago", width=w-4)
    c.text(x+2, y+4, "Affected: "+", ".join(q.get("affected", [])), "muted", width=w-4)
    if h > 6:
        coverage = f.get("sources", {}).get("messages", {}).get("coverage", "unavailable")
        c.text(x+2, y+5, f"Messages {coverage} | {max(0, len(qs)-1)} other questions", "muted", width=w-4)


def _ledger(c, rows, x, y, w, h, title="SESSION REGISTER"):
    c.panel(x, y, w, h, title)
    c.text(x+2, y+1, "SESSION / LIFECYCLE / PHASE; RESULT / ADMISSION BELOW", "muted", width=w-4)
    shown = rows[:max(0, (h-5)//2)]
    for i, s in enumerate(shown):
        _, color = _state(s)
        c.text(x+2, y+3+i*2, f"{s.get('id', '?'):7} {s.get('lifecycle', 'unknown'):8} / {s.get('phase', 'unknown')}", color, width=w-4)
        c.text(x+2, y+4+i*2, f"{s.get('result') or 'not observed'} / {s.get('admission', 'unknown')} | {s.get('freshness', 'unknown')} | {s.get('policy', 'unknown')}", "muted", width=w-4)
    c.text(x+2, y+h-2, f"{len(shown)}/{len(rows)} shown | result is not admission", "muted", width=w-4)


def _sources(c, f, x, y, w, h):
    c.panel(x, y, w, h, "OBSERVATION WINDOW")
    for i, (name, source) in enumerate(list(f.get("sources", {}).items())[:max(0, (h-4)//3)]):
        yy = y+2+i*3
        c.text(x+2, yy, name.upper(), "accent", True, w-4)
        c.text(x+2, yy+1, f"{source.get('coverage', 'unavailable')} | age {source.get('age_s', '?')}s", "muted", width=w-4)
    c.text(x+2, y+h-2, "Stale does not mean failed", "muted", width=w-4)


def signal_bridge(c, f, m):
    c.header("Signal Bridge", f, m)
    rows = _rows(m)
    if c.w >= 160:
        left, right = 46, 34
        _request(c, f, 1, 5, left, 8)
        _sources(c, f, 1, 15, left, c.h-19)
        _ledger(c, rows, left+3, 5, c.w-left-right-6, c.h-9)
        x, w = c.w-right-1, right
        c.panel(x, 5, w, c.h-9, "SIGNALS", "accent", True)
        for i, (key, label, color) in enumerate([("running", "RUNNING", "accent"), ("settled", "SETTLED", "good"), ("unknown", "UNKNOWN", "muted"), ("stale", "STALE", "warn"), ("frozen", "POLICY FROZEN", "frozen")]):
            y = 8+i*6
            c.text(x+3, y, str(m.get(key, 0)).rjust(3)+"  "+label, color, True, w-6)
            c.bar(x+3, y+2, m.get(key, 0), m.get("total", 0), w-6, color)
    elif c.w >= 144:
        _request(c, f, 1, 5, 53, 8)
        _sources(c, f, 1, 15, 53, c.h-19)
        _ledger(c, rows, 56, 5, c.w-57, c.h-9)
    elif c.w >= 116:
        _request(c, f, 1, 5, c.w-2)
        _ledger(c, rows, 1, 13, c.w-38, c.h-17)
        _sources(c, f, c.w-35, 13, 34, c.h-17)
    else:
        _request(c, f, 1, 5, c.w-2)
        c.text(3, 13, f"RUN {m.get('running', 0)}  SETTLED {m.get('settled', 0)}  UNKNOWN {m.get('unknown', 0)}  STALE {m.get('stale', 0)}", "accent", width=c.w-6)
        _ledger(c, rows, 1, 15, c.w-2, c.h-19, "SELECTED FLEET SLICE")
    c.footer()


def _quilt_strip(c, o, rows, x, y, w, compact=False):
    label_width = 28 if compact else w
    c.text(x, y, f"{o.get('name', '?').upper():10} {len(rows):3} sessions", "accent", True, label_width)
    c.text(x, y+1, o.get("mission", "Mission unavailable"), "muted", width=label_width)
    start = x+30 if compact else x
    cell_width = max(7, max((len(str(s.get('id', '?')))+3 for s in rows), default=7))
    columns = max(1, (w-(start-x))//cell_width)
    capacity = columns*2
    shown = rows[:capacity]
    yy = y if compact else y+2
    for j, s in enumerate(shown):
        mark, color = _state(s)
        c.text(start+(j%columns)*cell_width, yy+j//columns, f"{s.get('id', '?')} {mark}", color, width=cell_width-1)
    if len(rows) > capacity:
        c.text(x, y+1 if compact else y+4, f"+{len(rows)-capacity} sessions omitted", "muted", width=label_width)
    return len(shown)


def fleet_quilt(c, f, m):
    c.header("Fleet Quilt", f, m)
    _request(c, f, 1, 5, c.w-2)
    owners = _owners(f, _rows(m))
    c.text(3, 13, "ONE CELL = ONE SESSION   R running  S settled  F failed result  P frozen  ? unknown", "muted", width=c.w-6)
    visible = 0
    if c.w >= 160:
        split = (len(owners)+1)//2; left = 88
        stride = max(5, (c.h-22)//max(1, split))
        for group, x, w in [(owners[:split], 3, left-5), (owners[split:], left+3, c.w-left-6)]:
            for i, (o, rows) in enumerate(group[:5]):
                visible += _quilt_strip(c, o, rows, x, 16+i*stride, w)
    elif c.w >= 144:
        for i, (o, rows) in enumerate(owners[:10]):
            visible += _quilt_strip(c, o, rows, 3, 15+i*3, c.w-6, True)
    elif c.w >= 116:
        for i, (o, rows) in enumerate(owners[:10]):
            visible += _quilt_strip(c, o, rows, 3, 15+i*2, c.w-6, True)
    else:
        if owners:
            o, rows = owners[0]
            visible = _quilt_strip(c, o, rows, 3, 16, c.w-6)
            c.line(3, 21, c.w-6)
            for i, (other, items) in enumerate(owners[1:7]):
                c.text(3, 23+i*2, f"{other.get('name', '?'):12} {len(items):3} sessions (cells omitted)", width=c.w-6)
    total = len(_rows(m))
    c.text(3, c.h-4, f"{visible}/{total} session IDs shown; {total-visible} omitted | membership, not progress", "muted", width=c.w-6)
    c.footer()


def time_loom(c, f, m):
    c.header("Time Loom", f, m)
    wide = c.w >= 144
    left = 49 if c.w >= 160 else 44 if wide else 0
    if wide:
        _request(c, f, 1, 5, left-2, 8)
        _sources(c, f, 1, 15, left-2, c.h-19)
        x, y, unit = left+2, 7, 3 if c.w >= 160 else 2
    else:
        _request(c, f, 1, 5, c.w-2)
        x, y, unit = 3, 14, 2 if c.w >= 116 else 1
    c.text(x, y, "60 MINUTES / 20 EQUAL 3-MINUTE BUCKETS", "accent", True, c.w-x-2)
    start = x+15
    c.text(start, y+2, "-60m"+" "*(20*unit-9)+" now", "muted", width=c.w-start-2)
    rows = _rows(m); limit = max(0, (c.h-y-11)//2)
    marks = {"work": ("W", "accent"), "review": ("V", "accent"), "queue": ("Q", "accent"), "dependency": ("D", "accent"), "gap": ("·", "muted")}
    for i, s in enumerate(rows[:limit]):
        yy = y+4+i*2
        c.text(x, yy, f"{s.get('id', '?')} {s.get('owner', '?')}", width=13)
        timeline = s.get("timeline") or []
        for j in range(20):
            mark, color = marks.get(timeline[j] if j < len(timeline) else "gap", ("?", "muted"))
            span = "·"*unit if mark == "·" else mark+{"W": "━", "V": "═", "Q": "┄", "D": "─"}.get(mark, "?")*(unit-1)
            c.text(start+j*unit, yy, span, color)
    c.text(x, c.h-7, f"{min(limit, len(rows))}/{len(rows)} lanes shown; gaps are unobserved", "muted", width=c.w-x-2)
    c.text(x, c.h-6, "W━ work  V═ review  Q┄ queue  D─ dependency", "muted", width=c.w-x-2)
    c.text(x, c.h-5, "· gap | no completion estimate", "muted", width=c.w-x-2)
    c.footer()


def worktree_atlas(c, f, m):
    c.header("Worktree Atlas", f, m)
    _request(c, f, 1, 5, c.w-2)
    rows = _rows(m); trees = {t.get('id'): t for t in f.get('worktrees', [])}
    by_tree = {}
    for s in rows: by_tree.setdefault(s.get('worktree'), []).append(s)
    split = c.w >= 116
    w = c.w*3//5 if split else c.w-2
    bottom = c.h-5 if split else 29
    c.panel(1,13,w,bottom-12,"RECORDED BASE / BRANCH ATTACHMENTS","accent",True)
    c.text(4,15,"demo-main@a00  [declared base]","accent",True,width=w-7)
    # Prefer selected-path peers, then remaining branches; show explicit omission counts.
    selected=trees.get(rows[0].get('worktree'),{}) if rows else {}
    paths=set(selected.get('paths',[]))
    ordered=sorted(by_tree.items(),key=lambda item:(not bool(paths & set(trees.get(item[0],{}).get('paths',[]))),str(item[0])))
    cap=max(0,(bottom-19)//3);shown=ordered[:cap]
    for i,(wid,ss) in enumerate(shown):
        t=trees.get(wid,{});y=17+i*3
        c.text(4,y,'├━━ '+str(wid or 'UNMAPPED')+'  '+t.get('branch','no base attachment'),"accent",width=w-7)
        c.text(4,y+1,'│   '+str(t.get('head','unknown head'))+' / '+', '.join(s['id'] for s in ss),width=w-7)
        c.text(4,y+2,'│   '+('dirty' if t.get('dirty') else 'clean')+' / '+t.get('policy','unknown'),"muted",width=w-7)
    c.text(3,bottom-1,f"{len(shown)}/{len(by_tree)} mappings | {m['unmapped']} unmapped sessions","muted",width=w-4)
    x,y,pw,ph=(w+3,13,c.w-w-4,c.h-17) if split else (1,30,c.w-2,8)
    c.panel(x,y,pw,ph,"SELECTED PATH / PEER WORKTREES","warn")
    peers=[t for t in trees.values() if paths & set(t.get('paths',[]))]
    detail=[selected.get('id','No mapped tree'),*sorted(paths),'',*[t['id']+'  '+t['branch'] for t in peers],
            '',f'{len(peers)} worktrees share selected paths','Conflict: NOT ESTABLISHED','Dirty is not dangerous.',
            f"Inventory {len(trees)} / mapped {m['worktrees']}",f"Historical {m['historical']} excluded from active"]
    c.lines(x+2,y+2,detail[:max(0,ph-4)],pw-4)
    c.footer()


def decision_desk(c, f, m):
    c.header("Decision Desk", f, m)
    qs = f.get("requests", []); q = qs[0] if qs else {}
    affected = set(q.get("affected", [])); rows = [s for s in _rows(m) if s.get("id") in affected]
    wide = c.w >= 144
    w = 76 if c.w >= 160 else 64 if wide else c.w-2
    _request(c, f, 1, 5, w, 8)
    if wide:
        _ledger(c, rows, w+3, 5, c.w-w-4, c.h-9, "AFFECTED SESSION EVIDENCE")
        y = 15
    elif c.w >= 116:
        _ledger(c, rows, 1, 15, 66, c.h-19, "AFFECTED SESSIONS")
        x, y, w = 69, 15, c.w-70
    else:
        _ledger(c, rows, 1, 15, c.w-2, 12, "AFFECTED SESSIONS")
        y = 29
    x = 1 if wide or c.w < 116 else x
    h = c.h-y-4
    c.panel(x, y, w, h, "OTHER OBSERVED QUESTIONS")
    capacity = max(0, (h-4)//4)
    for i, other in enumerate(qs[1:1+capacity]):
        yy = y+2+i*4
        c.text(x+2, yy, other.get("question", "Question unavailable"), "warn", True, w-4)
        c.text(x+2, yy+1, "Owner: "+str(other.get("owner", "unknown")), width=w-4)
        c.text(x+2, yy+2, f"{len(other.get('affected', []))} affected | {other.get('age_min', '?')}m observed", "muted", width=w-4)
    c.text(x+2, y+h-2, f"{min(capacity, max(0, len(qs)-1))}/{max(0, len(qs)-1)} other questions shown", "muted", width=w-4)
    c.footer()


DESIGNS = {
    "signal-bridge": {"name": "Signal Bridge", "question": "What needs attention while the fleet is running?", "omits": "Detailed time history and workspace paths.", "tradeoff": "Strong overview; narrow width becomes a selected session register.", "data": "Current synthetic sessions, human questions and source ages.", "missing": "Missing source evidence remains unknown, never healthy by default.", "render": signal_bridge},
    "fleet-quilt": {"name": "Fleet Quilt", "question": "How is observed work distributed across owners?", "omits": "Per-session evidence packets and workspace paths.", "tradeoff": "Membership cells make uneven ownership visible; narrow mode selects one strip.", "data": "One literal cell per visible session, grouped by declared owner.", "missing": "Unknown lifecycle has its own marker; hidden records are counted.", "render": fleet_quilt},
    "time-loom": {"name": "Time Loom", "question": "Where did observed time go?", "omits": "Cost, resource use and admission evidence.", "tradeoff": "Comparable lanes require a fixed window and fewer visible sessions.", "data": "Twenty observed three-minute buckets, never inferred completion.", "missing": "Missing buckets are gaps, not inactivity or failure.", "render": time_loom},
    "worktree-atlas": {"name": "Worktree Atlas", "question": "Which sessions occupy which workspaces?", "omits": "Cross-owner dependencies and full session timelines.", "tradeoff": "Workspace-first directory prioritizes shared and unmapped membership.", "data": "Explicit session-worktree joins, paths, revisions and policy fields.", "missing": "Unmapped sessions remain visible; absent dirty state is unknown.", "render": worktree_atlas},
    "decision-desk": {"name": "Decision Desk", "question": "Which human question is waiting, and who is affected?", "omits": "Unaffected session inventory and resource telemetry.", "tradeoff": "Decision-first reading sacrifices fleet density.", "data": "Observed requests with explicit owner, age, evidence scope and affected sessions.", "missing": "No requests does not imply complete message coverage.", "render": decision_desk},
}
