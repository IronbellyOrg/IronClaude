"""Five observe-only terminal compositions over the proposed synthetic schema."""


def _decision(c, f, y=5):
    q = next(iter(f.get("requests", [])), None)
    c.panel(1, y, c.w-2, 6, "HUMAN QUESTION", "warn")
    if q:
        c.text(3, y+1, q.get("question", "Question unavailable"), "warn", True, c.w-6)
        c.text(3, y+2, f"Owner: {q.get('owner', 'unknown')} | affected: {len(q.get('affected', []))} sessions | observed {q.get('age_min', '?')}m ago", width=c.w-6)
        c.text(3, y+3, "Scope: " + ", ".join(q.get("affected", [])), width=c.w-6)
        c.text(3, y+4, f"{q.get('evidence', 'Evidence unavailable')} | {max(0, len(f['requests'])-1)} other requests", "muted", width=c.w-6)
    else:
        c.text(3, y+2, "No question observed; message coverage is not assurance.", "muted", width=c.w-6)


def _list(c, x, y, w, h, title, rows, color="line"):
    c.panel(x, y, w, h, title, color)
    limit = max(0, h-3)
    for n, row in enumerate(rows[:limit]):
        text, tone = row if isinstance(row, tuple) else (row, "ink")
        c.text(x+2, y+1+n, text, tone, width=w-4)
    c.text(x+2, y+h-2, f"{min(len(rows), limit)}/{len(rows)} text lines shown" if rows else "No records observed", "muted", width=w-4)


def _pin(s):
    return bool(s.get("revision")) and s.get("revision") == s.get("check_revision")


def proof_gate(c, f, m):
    c.header("Proof Gate", f, m)
    _decision(c, f)
    rows = m["sessions"]
    ranked = sorted(rows, key=lambda s: (_pin(s), s.get("tests") == "passed", s.get("id", "")))
    pinned = sum(_pin(s) for s in rows)
    c.text(3, 12, f"{pinned}/{len(rows)} revision-matched checks | {m['admitted']} admitted separately", "accent", True, c.w-6)
    selected = next(iter(ranked), {})
    facts = [("CURRENT " + str(selected.get("revision", "unknown")), "accent"),
             "CHECKED " + str(selected.get("check_revision", "unknown")),
             ("REVISION MATCH" if _pin(selected) else "REVISION MISMATCH / UNKNOWN", "warn"),
             "Tests: " + str(selected.get("tests") or "unknown"),
             "Review: " + str(selected.get("review") or "unknown"),
             "Report: " + str(selected.get("report") or "missing"),
             "Worker result: " + str(selected.get("result") or "not observed"),
             "Admission: " + str(selected.get("admission") or "unknown"),
             "Freshness: " + str(selected.get("freshness") or "unknown"),
             ("Worker success is not admission.", "muted"),
             ("Matched revision is not a fresh source.", "muted")]
    ledger = []
    for s in ranked:
        checked = (s.get("tests") or "unknown") if _pin(s) else "UNPINNED"
        ledger.append((f"{s['id']}  {s.get('owner', '?')}  {checked:<10}  review:{s.get('review') or '?'}  {s.get('admission', '?')}", "ink" if _pin(s) else "warn"))
    if c.w >= 150:
        _list(c, 1, 14, 97, c.h-18, "REVISION EVIDENCE LEDGER", ledger)
        _list(c, 100, 14, c.w-101, 16, "SELECTED / " + selected.get("id", "none"), facts, "accent")
        _list(c, 100, 31, c.w-101, c.h-35, "INTERPRETATION", ["Admission is recorded, not inferred.", "Unpinned tests prove no current head.", "Missing review is unknown, not failed.", "Historical records excluded here."])
    elif c.w >= 130:
        _list(c, 1, 14, 79, c.h-18, "EVIDENCE LEDGER", ledger)
        _list(c, 82, 14, c.w-83, c.h-18, "SELECTED / " + selected.get("id", "none"), facts, "accent")
    elif c.w >= 100:
        _list(c, 1, 14, c.w-2, 9, "CURRENT-HEAD CHECKS", ledger)
        _list(c, 1, 24, c.w-2, c.h-28, "SELECTED / " + selected.get("id", "none"), facts, "accent")
    else:
        _list(c, 1, 14, c.w-2, 16, "SELECTED / " + selected.get("id", "none"), facts, "accent")
        _list(c, 1, 31, c.w-2, c.h-35, "OTHER EVIDENCE RECORDS", ledger[1:])
    c.footer()


def budget_engine(c, f, m):
    c.header("Budget Engine", f, m)
    _decision(c, f)
    rows = m["sessions"]
    owners = [(o, [s for s in rows if s.get("owner") == o["id"]]) for o in f["orchestrators"]]
    sums = [(o, ss, sum(s['cost_usd'] for s in ss if s.get('cost_usd') is not None)) for o, ss in owners]
    sums.sort(key=lambda item: -item[2])
    largest = max((v for _, _, v in sums), default=0)
    known = m["cost_measured"]
    subtotal = f"USD {m['cost']:.2f} known subtotal" if known else "USD unknown / no samples"
    c.text(3, 12, f"{subtotal} | {known}/{len(rows)} measured | NOT TOTAL SPEND", "warn", True, c.w-6)
    if c.w >= 150:
        x, y, w, h = 1, 14, 98, c.h-18
        sx, sy, sw, sh = 101, 14, c.w-102, c.h-18
    elif c.w >= 130:
        x, y, w, h = 1, 14, 85, c.h-18
        sx, sy, sw, sh = 88, 14, c.w-89, c.h-18
    elif c.w >= 100:
        x, y, w, h = 1, 14, c.w-2, 15
        sx, sy, sw, sh = 1, 30, c.w-2, c.h-34
    else:
        x, y, w, h = 1, 21, c.w-2, c.h-25
        sx, sy, sw, sh = 1, 14, c.w-2, 6
    c.panel(x, y, w, h, "OWNER SUBTOTALS / RELATIVE USD", "accent")
    cap = max(0, (h-4)//2)
    for i, (o, ss, value) in enumerate(sums[:cap]):
        yy = y+2+i*2
        measured = sum(s.get("cost_usd") is not None for s in ss)
        amount = f"USD {value:.2f}" if measured else "unknown / no samples"
        c.text(x+2, yy, f"{o['name']:<10} {amount}  {measured}/{len(ss)} measured", width=w-4)
        if measured:
            c.bar(x+2, yy+1, value, largest or 1, w-5)
        else:
            c.text(x+2, yy+1, "No measured subtotal", "muted", width=w-4)
    c.text(x+2, y+h-2, f"{min(cap, len(sums))}/{len(sums)} owners shown; bars compare known subtotals", "muted", width=w-4)
    coverage = f.get("sources", {}).get("cost", {})
    windows = sorted({s.get("cost_window") or "unknown" for s in rows})
    sample = next((s for s in rows if s.get('cpu_pct') is not None and s.get('rss_mib') is not None), next(iter(rows), {}))
    cpu = f"{sample['cpu_pct']}%" if sample.get('cpu_pct') is not None else 'unknown'
    rss = f"{sample['rss_mib']} MiB" if sample.get('rss_mib') is not None else 'unknown'
    resource_source = f.get('sources', {}).get('workers', {})
    notes = [(f"Unmeasured: {len(rows)-known} sessions", "warn"),
             f"Source: {coverage.get('coverage', 'unavailable')} / age {coverage.get('age_s', '?')}s",
             f"USD windows: {', '.join(windows) or 'none'}",
             f"{sample.get('id', 'No sample')} CPU {cpu} / RSS {rss}",
             f"Worker source age {resource_source.get('age_s', '?')}s; sample age {sample.get('age_s', '?')}s",
             "No budget limit supplied.", "No burn forecast available.",
             "No token-to-progress conversion.", "", "RESOURCE OBSERVATIONS",
             f"CPU known: {sum(s.get('cpu_pct') is not None for s in rows)}/{len(rows)}",
             f"RSS known: {sum(s.get('rss_mib') is not None for s in rows)}/{len(rows)}",
             "CPU values are per-session samples.", "Missing costs are not zero."]
    _list(c, sx, sy, sw, sh, "COVERAGE / NOT A BUDGET", notes, "warn")
    c.footer()


def relay_map(c, f, m):
    c.header("Relay Map", f, m)
    _decision(c, f)
    edges = f.get("edges", [])
    names = {o["id"]: o["name"] for o in f["orchestrators"]}
    c.text(3, 12, f"{len(edges)} declared links | arrows mean recorded dependency, not execution flow", "accent", True, c.w-6)
    if c.w >= 150:
        x, w, top, step, cap = 34, c.w-35, 14, 8, (c.h-19)//8
        roster = [f"{o['id']} {o['name']} / {sum(s.get('owner') == o['id'] for s in m['sessions'])}" for o in f['orchestrators']]
        _list(c, 1, 14, 31, c.h-18, "OWNERS / SESSIONS", roster)
    elif c.w >= 130:
        x, w, top, step, cap = 1, c.w-2, 14, 8, (c.h-19)//8
    elif c.w >= 100:
        x, w, top, step, cap = 1, c.w-2, 14, 7, (c.h-19)//7
    else:
        records = []
        for e in edges:
            records.extend([(f"{e.get('from', '?')} → {e.get('to', '?')} / {e.get('reason', 'unknown')}", "accent"),
                            f"Scope: {', '.join(e.get('sessions', []))}", "Evidence: " + str(e.get('evidence') or 'unavailable'), ""])
        _list(c, 1, 14, c.w-2, c.h-18, "DECLARED LINKS / DETAIL", records)
        c.footer()
        return
    for i, e in enumerate(edges[:cap]):
        yy = top+i*step
        box = 26 if c.w >= 130 else 23
        c.panel(x, yy, box, 5, e.get("from", "?"), "accent")
        c.text(x+2, yy+2, names.get(e.get("from"), "Unknown owner"), width=box-4)
        right = x+w-box
        c.panel(right, yy, box, 5, e.get("to", "?"), "accent")
        c.text(right+2, yy+2, names.get(e.get("to"), "Unknown owner"), width=box-4)
        start, length = x+box, w-2*box
        c.text(start+1, yy+1, e.get("reason", "unknown"), "ink", width=length-2)
        c.line(start, yy+2, length-1, "accent")
        c.text(right-1, yy+2, "→", "accent")
        c.text(start+1, yy+3, f"{len(e.get('sessions', []))} affected sessions", "muted", width=length-2)
        c.text(x+2, yy+5, "Evidence: " + str(e.get("evidence") or "unavailable"), "muted", width=w-4)
    c.text(x+2, c.h-5, f"{min(cap, len(edges))}/{len(edges)} links shown; absent links remain unknown", "muted", width=w-4)
    c.footer()


def delta_deck(c, f, m):
    import textwrap
    c.header('Delta Deck',f,m)
    _decision(c,f)
    c.text(3,12,f"UNRESOLVED CONTEXT: {len(f.get('requests',[]))} observed questions retained; silence never closes them.",'warn',True,c.w-6)
    c.text(3,13,'Previous success: '+str(f.get('previous',{}).get('as_of','unavailable')),'muted',width=c.w-6)
    groups=[(k,[e for e in m.get('events',[]) if e.get('kind')==k]) for k in ('new','worsened','resolved','unchanged')]
    for i,(kind,events) in enumerate(groups):
        if c.w>=144:
            w=(c.w-6)//4;x=1+i*(w+1);y=16;h=c.h-20
        elif c.w>=116:
            w=(c.w-5)//2;x=1+(i%2)*(w+2);y=16+(i//2)*11;h=10
        else:
            x=1;y=15+i*6;w=c.w-2;h=6
        tone='good' if kind=='resolved' else 'warn' if kind=='worsened' else 'accent'
        c.panel(x,y,w,h,kind.upper()+' / '+str(len(events))+' events',tone,True)
        lines=[]
        for e in events:
            lines += [e['id']+' / '+str(e['seq'])]+textwrap.wrap(e.get('text','unknown'),max(8,w-4))+['ref '+str(e.get('ref','unknown')),'']
        if not events:lines=['No events observed in this lane.']
        c.lines(x+2,y+2,lines[:max(0,h-3)],w-4)
        if c.w>=116:c.text(x+2,y+h-2,f"{len(events)} events / explicit source changes",'muted',width=w-4)
    c.footer()


def watchkeeper(c,f,m):
    c.header('Watchkeeper',f,m)
    from layouts.agent_focus import big
    c.panel(2,5,c.w-4,12,'HUMAN HANDOVER / NO ALL-CLEAR','warn',True)
    big(c,6,8,len(f.get('requests',[])),'warn')
    c.text(23,8,'OBSERVED QUESTIONS STILL OPEN','warn',True,c.w-28)
    c.text(23,10,f"{m['failed']} failed reports retained / {m['frozen']} policy frozen",width=c.w-28)
    c.text(23,12,'Message coverage '+f['sources']['messages']['coverage']+'; further questions may exist.','muted',width=c.w-28)
    q=next(iter(f.get('requests',[])),None)
    if q:
        c.text(3,19,q['question'],'warn',True,c.w-6)
        c.text(3,20,f"Owner {q['owner']} / {q['age_min']}m / {len(q['affected'])} affected sessions",width=c.w-6)
        c.text(3,21,q['evidence'],'muted',width=c.w-6)
    else:c.text(3,19,'No requests observed in fixture; coverage is not assurance.','muted',width=c.w-6)
    c.line(3,23,c.w-6)
    handover=[f"{m['admitted']} result admissions explicitly recorded.",f"{m['stale']} stale sessions; {m['unknown']} lifecycle unknown.",
              'Checks are stale: do not infer current readiness.','Policy-frozen work remains for explicit human handling.',
              'No automatic retry, approval or worker instruction.']
    source_rows=[f"{name}: {s.get('coverage','unknown')} / {s.get('age_s','?')}s" for name,s in f['sources'].items()]
    if c.w>=116:
        w=c.w*3//5
        _list(c,2,25,w-4,c.h-29,'FOR THE NEXT HUMAN',handover,'accent')
        _list(c,w,25,c.w-w-2,c.h-29,'SOURCE AGES / NOT HEALTH',source_rows,'line')
    else:
        c.lines(3,25,handover, c.w-6)
        c.line(3,31,c.w-6)
        c.lines(3,33,source_rows[:5],c.w-6,'muted')
    c.footer()


DESIGNS = {
    "proof-gate": dict(name="Proof Gate", question="Which evidence describes the current revision?", omits="Full task inventory and elapsed-time tracks.", tradeoff="Revision integrity over fleet density.", data="Session revision, check revision, report, review, tests, result and admission.", missing="Missing checks remain unknown; an unmatched check cannot certify the current head.", render=proof_gate),
    "budget-engine": dict(name="Budget Engine", question="How much measured spend is visible, and what is missing?", omits="No invented budget, forecast or token-progress estimate.", tradeoff="Partial-cost honesty over a single reassuring total.", data="Recorded session USD, measurement coverage, window and owner; sampled resource coverage.", missing="Unmeasured costs are excluded from the subtotal, never replaced by zero spend.", render=budget_engine),
    "relay-map": dict(name="Relay Map", question="Which recorded dependency crosses owner boundaries?", omits="Inferred relationships and generic all-to-all wiring.", tradeoff="Legible evidence-backed routes over exhaustive session visibility.", data="Only explicit fixture edges with source, target, affected sessions and evidence.", missing="Absent relationships remain unknown rather than disconnected by assertion.", render=relay_map),
    "delta-deck": dict(name="Delta Deck", question="What explicitly changed since the saved baseline?", omits="Static fleet inventory and inferred resolutions.", tradeoff="Change recognition over full current-state coverage.", data="Normalized event IDs and sequence, explicit kind, reference and previous snapshot.", missing="No baseline is labeled unavailable; silence cannot resolve an item.", render=delta_deck),
    "watchkeeper": dict(name="Watchkeeper", question="Which observations are missing or need attention?", omits="Work throughput rankings and inferred healthy verdicts.", tradeoff="Coverage uncertainty stays visible even when records look quiet.", data="Source freshness and coverage plus explicit session exceptions and retry provenance.", missing="Unknown, stale and failed remain distinct; missing messages never mean no requests.", render=watchkeeper),
}
