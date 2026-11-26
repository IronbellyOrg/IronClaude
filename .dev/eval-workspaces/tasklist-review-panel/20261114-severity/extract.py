"""Build the blind batches for the contradiction-narrowing measurement (PLAN.md section 5).
Items = every blocking finding with category 'contradiction' in the 699 valid-era reviewer reports, plus control items made from
the ground-truth contradiction defects (written as findings, neutral ids). Output: batches/batch-NN.json (what the judge sees)
and key.json (id -> package, run, reviewer id, model, kind, ground-truth id), which the judge never sees."""
import glob, json, random, re, os

E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
O = os.path.dirname(os.path.abspath(__file__))
sets = json.load(open(f"{E}/analysis/allsets/allsets.json"))
rows = {r["run"] for s in sets if s["era"] == "source.md" for r in s["runs"]}
SH = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "gpt-6-luna": "luna", "gpt-6.1-terra": "terra", "gpt-6.1-sol": "sol",
      "grok-4.7": "grok", "muse-wonder-1.0": "wonder", "muse-ember-1.0": "ember"}
items, key = [], {}
for row in sorted(rows):
    for f in sorted(glob.glob(f"{E}/TASK-WF-*/reviews/combos/{row}/*.md")):
        if re.search(r"\.(attempt\d+|catfix)\.md$", f):
            continue
        pkg = f.split("/")[-5]; rid = os.path.basename(f)[:-3]
        m = re.search(r"```findings-v1\n(.*?)```", open(f, errors="ignore").read(), re.S)
        if not m:
            continue
        try:
            model = SH.get(json.load(open(f[:-3] + ".meta.json")).get("expected_model"), "?")
        except Exception:
            model = "?"
        for ln in m.group(1).splitlines():
            try:
                o = json.loads(ln)
            except Exception:
                continue
            if o.get("blocking") is True and o.get("category") == "contradiction":
                items.append({"pkg": pkg, "anchor": o.get("anchor", ""), "anchor2": o.get("anchor2"), "claim": o.get("claim", "")})
                key_id = len(items)
                key[f"X{key_id:04d}"] = {"pkg": pkg, "run": row, "rid": rid, "model": model, "kind": "reviewer", "severity": o.get("severity")}
# controls: ground-truth items of class contradiction (written as the reviewer-style claim + the plan quote as anchor)
for p in sorted(glob.glob(f"{E}/TASK-WF-*/ground-truth.json")):
    pkg = p.split("/")[-2]
    for it in json.load(open(p))["items"]:
        if it["class"] == "contradiction":
            items.append({"pkg": pkg, "anchor": (it.get("plan_quote") or "")[:200], "anchor2": None, "claim": it["description"][:300]})
            key[f"X{len(items):04d}"] = {"pkg": pkg, "run": None, "rid": None, "model": None, "kind": "control", "gt": it["id"],
                                         "blocking_in_implement": it["blocking_in_implement"]}
for i, it in enumerate(items, 1):
    it["id"] = f"X{i:04d}"
random.Random(20261114).shuffle(items)  # controls mixed in; judge sees no kind
os.makedirs(f"{O}/batches", exist_ok=True)
# batches of up to 25, one package per batch (the judge reads that package's candidate and source)
by = {}
for it in items:
    by.setdefault(it["pkg"], []).append(it)
n = 0
for pkg, its in sorted(by.items()):
    for i in range(0, len(its), 25):
        n += 1
        json.dump({"package": pkg, "candidate": f"{E}/{pkg}/candidate.md",
                   "source": f"/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/{pkg}/source.md",
                   "items": [{k: v for k, v in x.items() if k != "pkg"} for x in its[i:i + 25]]},
                  open(f"{O}/batches/batch-{n:02d}.json", "w"), indent=1)
json.dump(key, open(f"{O}/key.json", "w"), indent=1)
print("items", len(items), "reviewer", sum(1 for v in key.values() if v["kind"] == "reviewer"), "controls", sum(1 for v in key.values() if v["kind"] == "control"), "batches", n)
