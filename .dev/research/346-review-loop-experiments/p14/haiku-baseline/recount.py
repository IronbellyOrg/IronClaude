"""Prompt-path recount (these loop workers got a short 'Read <PROMPT path>' first message). Each message id once; model recorded; duplicates reported."""
import glob, json, re, collections
G = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
rx = re.compile(r"p14/haiku-baseline/runs/(a3-r\d)/PROMPT-(\w+)\.md")
import pathlib
RUNS = pathlib.Path(__file__).resolve().parent/"runs"
FP = {}
for p in RUNS.glob("a*-r*/PROMPT-*.md"):
    try:
        t = p.read_text(errors="ignore"); sb = re.search(r"SANDBOX: work ONLY inside (\S+?)\.", t).group(1)
        b = t.split("BRIEF (verbatim, from the coordinator):\n", 1)[1].split("\n\nFINAL REPLY", 1)[0]
        FP[(sb + ". Do not read", json.dumps(b)[1:-1])] = (p.parent.name, p.stem.replace("PROMPT-", ""))
    except Exception: pass
c = collections.defaultdict(list)
for f in glob.glob(G):
    try:
        with open(f, errors="ignore") as fh: head = "".join(next(fh, "") for _ in range(6))
    except Exception: continue
    m = rx.search(head[:1500]); key = m.groups() if m else None
    if key is None:
        for (sb, esc), k in FP.items():
            if sb in head and esc in head: key = k; break
    if key is None: continue
    best = {}; models = collections.Counter(); done = False
    for l in open(f, errors="ignore"):
        try: d = json.loads(l)
        except Exception: continue
        msg = d.get("message") or {}
        if msg.get("role") != "assistant": continue
        u = msg.get("usage") or {}; mid = msg.get("id") or f"anon{len(best)}"
        best[mid] = max(best.get(mid, 0), u.get("output_tokens") or 0)
        if msg.get("model"): models[msg["model"]] += 1
        if isinstance(msg.get("content"), list):
            for x in msg["content"]:
                if isinstance(x, dict) and x.get("type") == "tool_use" and x.get("name") == "SubagentHandback" and "DONE" in json.dumps(x.get("input")): done = True
    c[key].append({"tok": sum(best.values()), "model": (models.most_common(1) or [("?",)])[0][0], "done": done, "f": f[-26:]})
out = {}
for (r, s), v in sorted(c.items()):
    v.sort(key=lambda x: (x["done"], x["tok"]), reverse=True)
    out.setdefault(r, {"steps": {}, "models": {}, "dups": []})
    out[r]["steps"][s] = v[0]["tok"]; out[r]["models"][s] = v[0]["model"]
    if len(v) > 1: out[r]["dups"].append((s, [x["tok"] for x in v]))
for r, o in out.items():
    o["loop"] = sum(t for s, t in o["steps"].items() if s in ("R1", "V1", "R2", "V2", "R3")); o["aud"] = [t for s, t in o["steps"].items() if s.startswith("AUD")]
    print(r, o["loop"], o["steps"], set(o["models"].values()), "dups", o["dups"])
print("mean loop", round(sum(o["loop"] for o in out.values())/len(out)))
json.dump(out, open("tokens_generic.json", "w"), indent=1)
