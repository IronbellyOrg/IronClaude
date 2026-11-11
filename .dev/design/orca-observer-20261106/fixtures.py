"""Synthetic observation records. No Orca adapter, environment reads or network I/O."""
import copy
import json
from pathlib import Path

STAMP = "2026-11-06T08:00:00Z"
NAMES = ["Atlas", "Beacon", "Cinder", "Delta", "Ember", "Forge", "Grove", "Harbor", "Iris", "Juniper"]
MISSIONS = ["Billing migration", "API compatibility", "Release readiness", "Identity refresh", "Search upgrade", "Build reliability", "Docs delivery", "Telemetry cleanup", "Sandbox validation", "Packaging"]


def fixture(owners=8, count=80, variant="base"):
    assert owners in (5, 8, 10) and count in (50, 80, 100)
    f = {"synthetic": True, "as_of": STAMP, "variant": variant,
         "sources": {"workers": {"id": "demo:workers", "observed_at": "2026-11-06T07:59:56Z", "age_s": 4, "coverage": "complete fixture"},
                     "messages": {"id": "demo:messages", "observed_at": "2026-11-06T07:59:48Z", "age_s": 12, "coverage": "partial"},
                     "checks": {"id": "demo:checks", "observed_at": "2026-11-06T07:46:00Z", "age_s": 840, "coverage": "stale"},
                     "cost": {"id": "demo:usage", "observed_at": "2026-11-06T07:59:00Z", "age_s": 60, "coverage": "partial"},
                     "resources": {"id": "demo:resources", "observed_at": "2026-11-06T07:59:45Z", "age_s": 15, "coverage": "partial"}},
         "orchestrators": [{"id": f"O{i+1:02}", "name": NAMES[i], "mission": MISSIONS[i]} for i in range(owners)],
         "sessions": [], "worktrees": [], "requests": [], "edges": [], "events": [],
         "scope": {"host": "demo-local", "expected_hosts": None, "collection": "offline fixture"}}
    for i in range(count):
        owner = min(owners-1, i*owners//count)
        if variant == "uneven":
            owner = 0 if i < count//3 else 1+(i-count//3)%(owners-1)
        sid, wid = f"S{i+1:03}", f"W{i+1:03}"
        lifecycle = "running" if i%10 < 6 else ("settled" if i%10 < 9 else "unknown")
        result = ["succeeded", "partial", "failed"][i%10-6] if 6 <= i%10 <= 8 else None
        head = f"demo-{i+1:03}-b"
        s = {"id": sid, "owner": f"O{owner+1:02}", "worktree": wid,
             "lifecycle": lifecycle, "phase": ["work", "review", "queue", "dependency", "work", "review"][i%6],
             "health": "failed result" if result == "failed" else "unknown" if lifecycle == "unknown" else "no issue observed",
             "approval": "none observed", "freshness": "stale" if i%17 == 0 else "fresh", "age_s": 900 if i%17 == 0 else 4,
             "result": result, "admission": "admitted" if result == "succeeded" and i%20 == 6 else "not admitted",
             "evidence": "complete packet" if result else "partial packet", "policy": "frozen" if i == 14 else "not frozen",
             "revision": head, "check_revision": f"demo-{i+1:03}-a" if i%7 == 0 else head,
             "tests": None if i%11 == 0 else "failed" if result == "failed" else "passed",
             "review": None if i%9 == 0 else "recorded", "report": f"demo:evidence/{sid}/report.txt" if result else None,
             "cost_usd": None if i%4 == 0 else round(0.15+(i%13)*0.11,2), "cost_window": "07:00-08:00 UTC",
             "cpu_pct": None if i%5 == 0 else 10+i%65, "rss_mib": None if i%5 == 0 else 180+(i%12)*35,
             "retry_count": 3 if i == 22 else 0, "retry_source": "demo:authoritative-attempt-log" if i == 22 else None,
             "historical": False, "label": f"{MISSIONS[owner]} / task {i+1:03}",
             "timeline": (["queue"]*(i%4)+["work"]*(5+i%5)+["review"]*(2+i%3)+["gap"]*(1 if i%3==0 else 0)+["dependency"]*(3+i%4)+["work"]*20)[:20]}
        f["sessions"].append(s)
        f["worktrees"].append({"id":wid,"branch":f"demo/{NAMES[owner].lower()}-{i+1:03}","base":"demo-main@a00",
                                "head":head,"dirty":i%6 == 0,"paths":["billing/schema.py"] if i in (0,10,20) else [f"src/part_{i+1}.py"],
                                "conflict":"not established", "policy":s["policy"]})
    # Explicitly construct coherent relationships for each ownership scenario.
    owned={o['id']:[s['id'] for s in f['sessions'] if s['owner']==o['id']] for o in f['orchestrators']}
    for j,(label,age,scope) in enumerate([
        ("Choose schema compatibility policy",45,[owned[f'O{i:02}'][0] for i in (1,2,3,4)]),
        ("Confirm deployment window",20,[owned['O01'][1],owned['O02'][1]]),
        ("Name the release reviewer",10,[owned['O01'][2],owned['O02'][2]])]):
        f["requests"].append({"id":f"Q{j+1:02}","question":label,"owner":"Human operator", "requester":f"O{j+1:02}",
                              "age_min":age,"affected":scope,"evidence":f"demo:messages/Q{j+1:02}","state":"unanswered observed"})
        for sid in scope:
            f["sessions"][int(sid[1:])-1]["approval"]="human decision observed"
    f["edges"]=[{"id":"E01","from":"O01","to":"O02","reason":"schema contract","sessions":owned['O02'][:2],"evidence":"demo:dependency/E01"},
                 {"id":"E02","from":"O02","to":"O03","reason":"compatibility proof","sessions":owned['O03'][:3],"evidence":"demo:dependency/E02"},
                 {"id":"E03","from":"O03","to":"O04","reason":"release handoff","sessions":owned['O04'][:1],"evidence":"demo:dependency/E03"}]
    f["events"]=[{"id":"D01","seq":1,"kind":"new","text":"Newly observed: schema decision spans owner boundaries","ref":"Q01"},
                 {"id":"D02","seq":2,"kind":"worsened","text":"Checks refer to older revision","ref":"S008"},
                 {"id":"D03","seq":3,"kind":"resolved","text":"Prior docs question explicitly closed","ref":"demo:resolved/Q00"},
                 {"id":"D04","seq":4,"kind":"unchanged","text":"Policy freeze still requires human handling","ref":"S015"}]
    f["previous"]={"as_of":"2026-11-06T07:45:00Z", "source":"demo:previous-successful-snapshot"}
    if variant == "shared-unmapped":
        f["sessions"][1]["worktree"]="W001"
        f["sessions"][2]["worktree"]=None
    if variant == "historical":
        h=copy.deepcopy(f["sessions"][0]); h.update(id="H001",historical=True,lifecycle="settled",admission="not admitted",result="partial")
        f["sessions"].append(h)
    if variant == "long-identifiers":
        f["sessions"][0]["label"]="Very long mission / 漢字 / é / "+"compatibility-"*12
        f["worktrees"][0]["branch"]="demo/"+"long-branch-"*15
    if variant == "source-loss":
        f["sources"]["messages"].update(coverage="unavailable",age_s=3600,observed_at="2026-11-06T07:00:00Z")
        f["sources"]["workers"].update(coverage="stale",age_s=1800,observed_at="2026-11-06T07:30:00Z")
    if variant == "missing-fields":
        for s in f["sessions"][:12]:
            s.update(cost_usd=None, cpu_pct=None, rss_mib=None, tests=None, review=None)
    if variant == "duplicate-out-of-order":
        f["events"]=[f["events"][3],f["events"][0],f["events"][0],f["events"][2],f["events"][1]]
    if variant == "empty":
        f.update(sessions=[],worktrees=[],requests=[],edges=[],events=[])
    if variant == "injection":
        f["sessions"][0]["label"]="safe\x1b]52;c;ZXZpbA==\x07\x1b[2J\rspoof‮end"
    return f


def normalize_events(events):
    records={}
    for e in events:
        old=records.get(e["id"])
        if old is None or e["seq"]>old["seq"]: records[e["id"]]=e
    return sorted(records.values(), key=lambda e:(e["seq"],e["id"]))


def metrics(f, owner=None):
    global_rows=[s for s in f["sessions"] if not s["historical"]]
    rows=[s for s in global_rows if owner is None or s["owner"]==owner]
    measured=[s for s in rows if s["cost_usd"] is not None]
    affected={sid for q in f["requests"] for sid in q["affected"]}
    return {"sessions":rows,"total":len(rows),"global_total":len(global_rows),"historical":sum(s["historical"] for s in f["sessions"]),
            "worktrees":len({s["worktree"] for s in rows if s["worktree"]}),"inventory_worktrees":len(f["worktrees"]),
            "unmapped":sum(s["worktree"] is None for s in rows),
            "running":sum(s["lifecycle"]=="running" for s in rows),"settled":sum(s["lifecycle"]=="settled" for s in rows),
            "unknown":sum(s["lifecycle"]=="unknown" for s in rows),"stale":sum(s["freshness"]=="stale" for s in rows),
            "failed":sum(s["result"]=="failed" for s in rows),"frozen":sum(s["policy"]=="frozen" for s in rows),
            "admitted":sum(s["admission"]=="admitted" for s in rows),
            "cost":round(sum(s["cost_usd"] for s in measured),2),"cost_measured":len(measured),
            "affected":len(affected & {s["id"] for s in rows}),"events":normalize_events(f["events"])}


def write_fixtures(root):
    root=Path(root); (root/"scenarios").mkdir(exist_ok=True)
    (root/"fixture.json").write_text(json.dumps(fixture(),indent=2)+"\n")
    variants=["uneven","shared-unmapped","historical","long-identifiers","source-loss","missing-fields","duplicate-out-of-order","empty","injection"]
    for variant in variants:
        (root/"scenarios"/(variant+".json")).write_text(json.dumps(fixture(variant=variant),indent=2)+"\n")
    for o in (5,8,10):
        for n in (50,80,100):
            (root/"scenarios"/f"scale-{o}-{n}.json").write_text(json.dumps(fixture(o,n),indent=2)+"\n")
