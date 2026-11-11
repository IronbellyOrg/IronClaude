"""Prompt-text token recount for any harness dir: python3 tokens_generic.py <dir>. Read-only; prints per run loop/aud tokens."""
import glob, json, pathlib, sys, collections, importlib.util
d = pathlib.Path(sys.argv[1]).resolve(); sys.path.insert(0, str(d))
spec = importlib.util.spec_from_file_location("h", d/"harness.py"); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
norm = lambda s: " ".join(s.split())
runsdir = pathlib.Path(h.RUNS) if hasattr(h, "RUNS") else d/"runs"
prompts = {}
for p in runsdir.rglob("PROMPT*.md"):
    if "misparsed" in p.name or "failed" in p.name: continue
    rel = p.relative_to(runsdir).parts
    prompts[norm(p.read_text(errors="ignore"))] = (rel[0], p.stem.replace("PROMPT-", "").replace("PROMPT", "?"))
tglob = getattr(h, "TASKS_GLOB", "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output")
spec1 = importlib.util.spec_from_file_location("h1", "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/harness.py"); h1 = importlib.util.module_from_spec(spec1); sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1"); spec1.loader.exec_module(h1); ti = h1.transcript_info
idx = collections.defaultdict(list); un = 0; seen = 0
tag = str(runsdir).split("scratchpad/")[1]
for f in glob.glob(tglob):
    info = ti(f)
    if not info or not info.get("first"): continue
    k = norm(info["first"])
    if tag not in k: continue
    seen += 1
    m = prompts.get(k)
    if m: idx[m].append(info)
    else: un += 1
print(d.name, "seen", seen, "matched", sum(len(v) for v in idx.values()), "unmatched", un)
loops = {"sonnet": [], "haiku": []}; auds = []
for (run, step) in sorted(idx): pass
runs = sorted({r for r, _ in idx})
out = {}
for run in runs:
    row = {}
    for (r, s), c in idx.items():
        if r != run: continue
        c.sort(key=lambda x: (x["done"], x["tokens"]), reverse=True); row[s] = (c[0]["tokens"], c[0]["model"], len(c))
    loop = sum(v[0] for s, v in row.items() if not s.startswith("AUD"))
    au = [row[s][0] for s in ("AUD", "AUD2") if s in row]
    models = {v[1] for s, v in row.items() if not s.startswith("AUD")}
    out[run] = {"loop": loop, "aud": au, "models": sorted(models), "steps": {s: v[0] for s, v in row.items()}, "step_models": {s: v[1] for s, v in row.items()}}
    print(run, "loop", loop, "aud", au, sorted(models), "dups", [s for s, v in row.items() if v[2] > 1])
json.dump(out, open(d/"tokens_models.json", "w"), indent=1)
