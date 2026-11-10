"""Recount tokens matching each agent transcript to a PROMPT-<STEP>.md by prompt TEXT (the agents were launched with the prompt pasted verbatim,
so the harness NEW_PAT (path-in-first-message) never matches). Read-only: prints a table, writes tokens_by_prompt.json. Run with python3."""
import glob, json, pathlib, sys, collections
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h

def norm(s): return " ".join(s.split())

prompts = {}   # norm(text) -> (run, step)
for run in h.all_runs():
    for p in pathlib.Path(h.SP / "p12/ab1/runs" / run).glob("PROMPT-*.md"):
        if ".misparsed" in p.name or ".failed" in p.name: continue
        step = p.stem.replace("PROMPT-", "")
        prompts[norm(p.read_text())] = (run, step)

idx = collections.defaultdict(list); unmatched = 0; seen = 0
for f in sorted(glob.glob(h.TASKS_GLOB)):
    info = h.transcript_info(f)
    if not info or not info["first"]: continue
    key = norm(info["first"])
    if "p12/ab1/runs/" not in key: continue
    seen += 1
    k = prompts.get(key)
    if k: idx[k].append(info)
    else: unmatched += 1
print("transcripts mentioning p12/ab1:", seen, "matched keys:", len(idx), "unmatched:", unmatched)
res = {}
for run in h.all_runs():
    st = h.load(run)
    row = {}
    for step in h.STEPS:
        c = idx.get((run, step))
        if not c: continue
        best = h.pick(c, h.expected_model(st, step), f"{run} {step}")
        if best: row[step] = best["tokens"]
    loop = sum(v for s, v in row.items() if s in h.LOOP_STEPS)
    res[run] = {"steps": row, "loop": loop, "aud": row.get("AUD"), "aud2": row.get("AUD2"), "missing_loop_steps": [s for s in st["done"] if s in h.LOOP_STEPS and s not in row]}
    print(run, "loop", loop, "aud", row.get("AUD"), "aud2", row.get("AUD2"), "missing", res[run]["missing_loop_steps"])
json.dump(res, open(h.SP / "p12/ab1/tokens_by_prompt.json", "w"), indent=1)
