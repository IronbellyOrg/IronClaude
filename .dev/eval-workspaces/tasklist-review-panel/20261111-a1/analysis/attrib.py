"""Per-model GT attribution from judge notes + merge ledgers (source.md-era rows only).
Approximate: parses judge prose 'Lk ... matches GTn' clauses. Wrong blockers credited to members marked blocking."""
import json, re, glob, os, sys, itertools, collections
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PK = {"TASK-WF-designSpec-20261107-075614": "DS", "TASK-WF-makeTheAliasOnly-20261105-051649": "AL", "TASK-WF-design-20261108-041415": "DE"}
ok = lambda r: r.endswith("-src") or r.startswith("b4-") or r.endswith("-ember") or (r[:1] == "e" and r[1:2].isdigit())
SHORT = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "gpt-6-luna": "luna", "gpt-6.1-terra": "terra",
         "gpt-6.1-sol": "sol", "grok-4.7": "grok", "muse-wonder-1.0": "wonder", "muse-ember-1.0": "ember"}
out = []  # (row, pkg, rid, model, set(GT any), set(GT blk-credited), wrong_blockers)
for row in sorted(os.listdir(f"{E}/combos")):
    if not ok(row) or "contaminated" in row or "superseded" in row: continue
    for pkg, p in PK.items():
        led = f"{E}/combos/{row}/{pkg}/ledger.json"
        sc = [s for s in glob.glob(f"{E}/arms/scoring/combos/{row}/{pkg}/*/score.json")]
        if not os.path.exists(led) or not sc: continue
        score = json.load(open(sc[0]))
        L = json.load(open(led)); rows = L["rows"] if isinstance(L, dict) and "rows" in L else L
        members = {r["lid"]: r["members"] for r in rows}
        lblk = {r["lid"]: r["blocking"] for r in rows}
        models = {}
        for m in glob.glob(f"{E}/{pkg}/reviews/combos/{row}/t*.meta.json"):
            if "attempt" in m: continue
            j = json.load(open(m)); models[j["reviewer_id"]] = SHORT.get(j["expected_model"], j["expected_model"])
        gany = collections.defaultdict(set); gblk = collections.defaultdict(set); wb = collections.Counter()
        matched = set()
        for cl in re.split(r"[;.](?:\s|$)", score.get("notes", "")):
            if re.search(r"no GT|not covered|matches none|no ground", cl, re.I): continue
            mm = re.search(r"\b(match|cover)", cl, re.I)
            if not mm: continue
            # L ids named before the verb (parentheticals stripped: they quote candidate text like 'L3');
            # GT ids after the verb, up to the first colon/paren (the judge's explanation follows)
            head = re.sub(r"\([^)]*\)|'[^']*'", "", cl[:mm.start()])
            ls = re.findall(r"\bL(\d+)\b", head); gs = re.findall(r"\bGT(\d+)\b", re.split(r"[:(]", cl[mm.start():])[0])
            if not ls or not gs: continue
            for l in ls:
                lid = f"L{l}"; matched.add(lid)
                for mem in members.get(lid, []):
                    for g in gs:
                        gany[mem["reviewer_id"]].add(g)
                        if lblk.get(lid) and f"GT{g}" in score["gt_covered_blocking"]: gblk[mem["reviewer_id"]].add(g)
        # fallback for judged GT hits the clause parser missed: any sentence naming that GT plus L ids
        credited = set().union(*gany.values()) if gany else set()
        for gt in score["gt_covered_any"]:
            g = gt.replace("GT", "")
            if g in credited: continue
            for sent in re.split(r"(?<=[.;])\s", score.get("notes", "")):
                if not re.search(rf"\bGT{g}\b", sent) or re.search(r"not (covered|raised)|no finding|matches no", sent, re.I): continue
                for l in re.findall(r"\bL(\d+)\b", re.sub(r"'[^']*'", "", sent)):
                    lid = f"L{l}"
                    if lid not in members: continue
                    matched.add(lid)
                    for mem in members[lid]:
                        gany[mem["reviewer_id"]].add(g)
                        if lblk.get(lid) and gt in score["gt_covered_blocking"]: gblk[mem["reviewer_id"]].add(g)
        for lid, b in lblk.items():
            if b and lid not in matched:
                for mem in members.get(lid, []):
                    if mem.get("blocking"): wb[mem["reviewer_id"]] += 1
        for rid, mod in models.items():
            out.append((row, p, rid, mod, gany[rid], gblk[rid], wb[rid]))
json.dump([[a, b, c, d, sorted(e), sorted(f), g] for a, b, c, d, e, f, g in out], open("/tmp/attrib.json", "w"))
# per-model aggregate (defect-rich only)
agg = collections.defaultdict(lambda: [0, 0, 0, 0, set()])
for row, p, rid, mod, ga, gb, w in out:
    if p == "DE": continue
    a = agg[mod]; a[0] += 1; a[1] += len(ga); a[2] += len(gb); a[3] += w; a[4] |= {f"{p}:GT{g}" for g in ga}
print("DEFECT-RICH per reviewer run: model runs GTany/run GTblk/run wrongblk/run distinct-GTs-ever")
for m, (n, ga, gb, w, s) in sorted(agg.items()):
    print(f"{m:7s} {n:3d} {ga/n:5.2f} {gb/n:5.2f} {w/n:5.2f} {sorted(s)}")
# pairwise complementarity: union of distinct GTs ever caught (defect-rich)
print("\nPAIR union of distinct GTs ever caught / overlap")
for x, y in itertools.combinations(sorted(agg), 2):
    sx, sy = agg[x][4], agg[y][4]
    print(f"{x}+{y}: union={len(sx|sy)} overlap={len(sx&sy)}")
print("\nROWS containing luna AND terra (per reviewer, defect-rich):")
for row, p, rid, mod, ga, gb, w in out:
    if p != "DE" and row in ("b4-terra-luna-muse", "terra-luna-muse-ember"):
        print(row, p, rid, mod, "any", sorted(ga), "blk", sorted(gb), "wb", w)
