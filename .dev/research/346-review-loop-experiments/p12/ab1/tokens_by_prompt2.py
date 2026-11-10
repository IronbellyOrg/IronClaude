"""v2: match transcripts to (run, step) by pasted PROMPT text OR by a short 'Read <path>' launch (step from the PROMPT path / sandbox dir),
and keep only transcripts written after that step's recorded launch time (replays reuse identical prompt text). Each message id counted once."""
import glob, json, os, pathlib, re, sys, collections, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h
norm = lambda s: " ".join(s.split())
SUB = {"vf1": "VF1", "vf2": "VF2", "vf3": "VF3", "aud": "AUD", "aud2": "AUD2", "vf1-clean": "VF1", "r1a": "R1a", "r1b": "R1b", "r1c": "R1c"}
prompts = {}
for run in h.all_runs():
    for p in (h.SP / "p12/ab1/runs" / run).glob("PROMPT-*.md"):
        if any(x in p.name for x in (".misparsed", ".failed", ".superseded", ".orig")): continue
        prompts[norm(p.read_text())] = (run, p.stem.replace("PROMPT-", ""))
def key_of(first):
    k = prompts.get(norm(first))
    if k: return k
    m = re.match(r"\s*Read (\S+?/p12/ab1/runs/([\w-]+)/(?:([\w-]+)/)?PROMPT(?:-(\w+))?\.md)", first)
    if m:
        run, sub, step = m.group(2), m.group(3), m.group(4)
        if step: return (run, step)
        if sub in SUB: return (run, SUB[sub])
    return None
idx = collections.defaultdict(list)
for f in glob.glob(h.TASKS_GLOB):
    info = h.transcript_info(f)
    if not info or "p12/ab1/runs/" not in (info["first"] or ""): continue
    k = key_of(info["first"])
    if k:
        info["mtime"] = os.path.getmtime(f); idx[k].append(info)
res = {}
for run in h.all_runs():
    st = h.load(run); row = {}
    for step in h.STEPS:
        if step not in st["done"]: continue
        c = idx.get((run, step), [])
        lt = st["launched"].get(step)
        if lt:
            t0 = datetime.datetime.fromisoformat(lt).timestamp() - 5
            c = [x for x in c if x["mtime"] >= t0]
        best = h.pick(c, h.expected_model(st, step), f"{run} {step}") if c else None
        if best: row[step] = best["tokens"]
    loop = sum(v for s, v in row.items() if s in h.LOOP_STEPS)
    miss = [s for s in st["done"] if s not in row]
    res[run] = {"steps": row, "loop": loop, "missing": miss}
    print(run, "loop", loop, "aud", row.get("AUD"), row.get("AUD2"), "missing", miss)
    for s, v in row.items():
        if s in st["log"]: st["log"][s]["output_tokens"] = v
    h.save(run, st)
json.dump(res, open(h.SP / "p12/ab1/tokens_by_prompt2.json", "w"), indent=1)
