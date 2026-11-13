"""Inventory EVERY scored panel run in the study (pilot arms + all combo rows), group into sets by (era, reviewer-model multiset),
and write /tmp/allsets.json (sets with their runs and score-file paths) for the per-set issue table."""
import json, glob, os, collections
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
PK = [DS, AL, DE]
SH = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "gpt-6-luna": "luna", "gpt-6.1-terra": "terra", "gpt-6.1-sol": "sol",
      "grok-4.7": "grok", "muse-wonder-1.0": "wonder", "muse-ember-1.0": "ember", "muse-spark-1.3": "spark", "glm-5.3": "glm", "Qwen3.8-max": "qwen"}
def valid(r):
    return r.endswith("-src") or r.startswith("b4-") or r.endswith("-ember") or (r[:1] in "eghj" and r[1:2].isdigit())
def models_of(resfile):
    try: return sorted(SH.get(x["model"], x["model"]) for x in json.load(open(resfile))["reviewers"])
    except Exception: return None
runs = []
# pilot arms
for arm in ("A", "B", "C"):
    sc = {}; ms = None
    for p in PK:
        key = json.load(open(f"{E}/arms/scoring/{p}/arm-key.json")); lab = key[arm]
        f = f"{E}/arms/scoring/{p}/{lab}/score.json"
        if os.path.exists(f): sc[p] = f
        ms = ms or models_of(f"{E}/arms/{arm}/{p}/resolution.json")
    runs.append(dict(run=f"pilot-arm-{arm}", era="pre-source.md", models=ms, scores=sc, note="pilot arm"))
# combo rows
for row in sorted(os.listdir(f"{E}/arms/scoring/combos")):
    if row.startswith(("i1-", "i2-")): continue
    sc = {}; ms = None; loc = "combos"
    for p in PK:
        fs = [f for f in glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json")]
        if fs: sc[p] = fs[0]
        for rf in (f"{E}/combos/{row}/{p}/resolution.json", f"{E}/quarantine-pre-src-luna/_combos/{row}/{p}/resolution.json"):
            if not ms and os.path.exists(rf):
                ms = models_of(rf); loc = "combos" if "/combos/" in rf and "quarantine" not in rf else "quarantine-pre-src-luna"
    notes = []
    if loc != "combos": notes.append("merged report only in quarantine-pre-src-luna")
    if row == "r2-sonnet": notes.append("stale scores (merge redone after judging, audit E)")
    if row == "b4-muse-ember-luna2": pass
    runs.append(dict(run=row, era="source.md" if valid(row) else "pre-source.md", models=ms, scores=sc, note="; ".join(notes)))
miss = [r["run"] for r in runs if not r["models"] or len(r["scores"]) < 3]
sets = collections.OrderedDict()
for r in runs:
    if not r["models"]: continue
    k = (r["era"], tuple(r["models"]))
    sets.setdefault(k, []).append(r)
out = []
for (era, ms), rs in sets.items():
    out.append(dict(set=" + ".join(f"{c}x {m}" if c > 1 else m for m, c in sorted(collections.Counter(ms).items())), models=list(ms), era=era, n_runs=len(rs), runs=rs))
out.sort(key=lambda s: (s["era"] != "source.md", s["set"]))
for i, s in enumerate(out, 1): s["sid"] = f"S{i:02d}"
json.dump(out, open("/tmp/allsets.json", "w"), indent=1)
print("runs:", len(runs), "sets:", len(out), "runs lacking models or a package score:", miss)
for s in out: print(s["sid"], s["era"], s["set"], s["n_runs"], [r["run"] for r in s["runs"]])
