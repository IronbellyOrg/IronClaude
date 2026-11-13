import json, os, re, glob, hashlib, collections, statistics
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
S = E + "/arms/scoring/combos"
out = []
def flag(c, row, pkg, sev, r): out.append((c, row, pkg, "na", sev, r))
hashes = collections.defaultdict(list)
models = collections.Counter(); turns = []
by = []
for sp in sorted(glob.glob(S + "/*/*/*/score.json")):
    D = os.path.dirname(sp); pkg = D.split("/")[-2]; row = D.split("/")[-3]
    if re.search(r"^i1-|^i2-", row): continue
    sc = json.load(open(sp))
    mf = D + "/merged-anon.md"
    if os.path.exists(mf):
        h = hashlib.md5(open(mf, "rb").read()).hexdigest(); hashes[h].append((row, pkg))
    try: jj = json.load(open(D + "/judge.json"))
    except Exception: continue
    init = [x for x in jj if x.get("type") == "system" and x.get("subtype") == "init"]
    m = init[0].get("model") if init else None
    models[m] += 1
    if m != "claude-opus-5-5": flag("5.judgemodel", row, pkg, "WARN", f"judge model {m}")
    res = [x for x in jj if x.get("type") == "result"][-1]
    turns.append(res.get("num_turns", 0))
    reads = []
    for x in jj:
        if x.get("type") == "assistant":
            for b in x["message"].get("content", []):
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    inp = b["input"]; reads.append((b["name"], json.dumps(inp)))
    blob = "\n".join(a for n, a in reads)
    needs = {"GT": f"{pkg}/ground-truth.json", "cand": f"{pkg}/candidate.md", "anon": "merged-anon.md"}
    for k, v in needs.items():
        if v not in blob: flag("5.judgeinputs", row, pkg, "WARN", f"judge tool calls never mention {v}")
    others = [p for p in os.listdir(E) if p.startswith("TASK-WF") and p != pkg]
    for p in others:
        if p in blob: flag("5.crosspkg", row, pkg, "EXCLUDE", f"judge tool calls mention other package {p}")
    # judge reads of the correct label dir (not a sibling row's)
    for m2 in set(re.findall(r"arms/scoring/combos/([^/\"]+)/", blob)):
        if m2 != row: flag("5.crossrow", row, pkg, "EXCLUDE", f"judge tool calls mention row {m2}")
    # score written after judge finished?
    dt = os.path.getmtime(sp) - os.path.getmtime(D + "/judge.json")
    if dt > 2: flag("5.scoreafterjudge", row, pkg, "WARN", f"score.json modified {dt:.0f}s after judge.json (manual edit?)")
    fin = res.get("result", "")
    # final reply count claims vs score
    mm = re.search(r"covers? (\d+) ground", fin) or re.search(r"gt_covered_any[^0-9]*(\d+)", fin)
    if mm and int(mm.group(1)) != len(sc["gt_covered_any"]): flag("5.replymismatch", row, pkg, "WARN", f"final reply says {mm.group(1)} covered, score.json has {len(sc['gt_covered_any'])}")
    gt = json.load(open(f"{E}/{pkg}/ground-truth.json"))
    by.append(dict(row=row, pkg=pkg, n=len(sc["gt_covered_any"]), nb=len(sc["gt_covered_blocking"]), blk=sc["ledger_rows_blocking"], wr=sc["wrong_blockers"], gt=len(gt["items"]), mt=os.path.getmtime(sp)))
for h, v in hashes.items():
    if len(v) > 1:
        # same anon content across different packages is a serious fault; same row-package pair is not possible
        pk = set(p for r, p in v)
        sev = "EXCLUDE" if len(pk) > 1 else "WARN"
        for r, p in v: flag("5.dupanon", r, p, sev, f"identical merged-anon.md as {[x for x in v if x != (r,p)][:3]}")
json.dump(by, open("/tmp/audit-E/by.json", "w"))
print("models", models); print("turns min/med/max", min(turns), statistics.median(turns), max(turns))
with open("/tmp/audit-E/flags.tsv", "a") as f:
    for x in out: f.write("\t".join(x) + "\n")
print(len(out), collections.Counter((x[0], x[4]) for x in out))
# strictness drift: by batch prefix and package
pre = lambda r: re.match(r"[a-z]+\d*|terra|sol", r).group(0)
agg = collections.defaultdict(list)
for b in by: agg[(b["pkg"][8:20], pre(b["row"]))].append(b)
for k in sorted(agg):
    v = agg[k]
    print(k, "n=%d" % len(v), "cov/gt=%.2f" % (sum(x["n"] for x in v) / sum(x["gt"] for x in v)), "wrong/blk=%s" % (("%.2f" % (sum(x["wr"] for x in v) / max(1, sum(x["blk"] for x in v))))), "blk/row=%.1f" % (sum(x["blk"] for x in v) / len(v)))
