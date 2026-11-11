import sys, json, glob, hashlib, pathlib, random, collections, tempfile
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p19/ab6")
import a2_observability as A
AB6 = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p19/ab6")
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
specs = json.load(open(AB6/"specs-shadow.json"))
uniq = {}   # key -> dict
for sp in specs:
    sid = sp["sid"]
    rep = json.load(open(AB6/"out"/"a2"/f"{sid}.json"))
    ans = {a["id"]: a for a in rep["answers"] if a.get("usable")}
    text = pathlib.Path(sp["spec"]).read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as td:
        _r, _an, items, _l = A.build_items(text, pathlib.Path(td)/"x", sid)
        ctl = {c["id"]: c for c in A.control_items(items)}
    for iid, a in ans.items():
        if iid not in ctl: continue
        c = ctl[iid]
        key = hashlib.sha256(json.dumps([iid.split(":")[-1], c["state"]], sort_keys=True).encode()).hexdigest()[:16]
        u = uniq.setdefault(key, {"key": key, "row": iid.split(":")[-1], "state": c["state"], "jev": a["choice"], "jev_conf": a["confidence"], "specs": []})
        u["specs"].append(sid)
        assert u["jev"] == a["choice"], (key, u["jev"], a["choice"])
json.dump(list(uniq.values()), open(OUT/"all_unique.json", "w"), indent=1)
print("unique usable packets", len(uniq), collections.Counter(u["jev"] for u in uniq.values()))
