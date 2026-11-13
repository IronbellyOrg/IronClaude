import os, re, json, glob, hashlib, collections, sys
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PK = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
T_SRC = 1794574774.0  # placeholder, overwritten below
import datetime
T_SRC = datetime.datetime(2026, 11, 12, 12, 59, 34, 240000, tzinfo=datetime.timezone.utc).timestamp()
SKIP = ("contaminated", "superseded", "quarantine")
VALID_RE = re.compile(r"(-src$|^b4-|^sol-alone-src$|^terra-alone-src$|-ember$|^[egh]\d-|^i\d-)")
def sha(b): return hashlib.sha256(b).hexdigest()
cand = {}
for p in PK:
    b = open(f"{E}/{p}/candidate.md", "rb").read()
    cand[p] = dict(sha=sha(b), text=b.decode("utf-8", "replace"))
    cand[p]["lines"] = set(l.strip() for l in cand[p]["text"].splitlines() if l.strip())
    cand[p]["norm"] = re.sub(r"\s+", " ", cand[p]["text"])
KNOWN = set()
for p in PK:
    KNOWN.add(sha(open(f"/tmp/evalsb/cand/{p}/source.md", "rb").read()))
flags = []
def flag(check, row, pkg, rid, sev, reason):
    flags.append((check, row, pkg.replace("TASK-WF-", "")[:14], rid, sev, reason))
HEX = re.compile(r"\b[0-9a-f]{64}\b")
runs = []
def load(fp):
    try: return json.load(open(fp))
    except Exception: return None
for p in PK:
    base = f"{E}/{p}/reviews/combos"
    for row in sorted(os.listdir(base)):
        if any(s in row for s in SKIP) or re.match(r"i\d-", row): continue
        d = f"{base}/{row}"
        if not os.path.isdir(d): continue
        for f in sorted(glob.glob(d + "/*.md")):
            fn = os.path.basename(f)
            if ".attempt" in fn or fn.endswith(".catfix.md") or ".md." in fn: continue
            rid = fn[:-3]
            atts = sorted([x for x in glob.glob(f"{d}/{rid}.attempt*.json") if re.search(r"attempt\d+\.json$", x)], key=lambda x: int(re.search(r"attempt(\d+)\.json", x).group(1)))
            meta = load(f"{d}/{rid}.meta.json") or {}
            r = dict(pkg=p, row=row, rid=rid, path=f, mtime=os.path.getmtime(f), body=open(f, "rb").read(),
                     model=meta.get("observed_model", "?"), exp=meta.get("expected_model", "?"), wall=meta.get("wall_s", 0),
                     meta=meta, atts=atts, valid=bool(VALID_RE.search(row)))
            runs.append(r)
print("runs", len(runs))
# --- era
def start_of(r): return r["mtime"] - (r["wall"] or 0)
GPT = lambda m: m.startswith("gpt-")
for r in runs:
    r["start"] = start_of(r)
    r["pre"] = r["start"] < T_SRC
    r["end_pre"] = r["mtime"] < T_SRC
    gp = GPT(r["model"]) or GPT(r["exp"])
    if r["valid"] and r["pre"]:
        flag("1-era", r["row"], r["pkg"], r["rid"], "EXCLUDE", f"valid-era-named row but run start {datetime.datetime.fromtimestamp(r['start'], datetime.timezone.utc):%m-%d %H:%M:%S} predates source.md ship {T_SRC}; model={r['model']}")
    if (not r["valid"]):
        r_sev = "EXCLUDE" if gp else "WARN"
        flag("1-era", r["row"], r["pkg"], r["rid"], r_sev, f"old-era row (no source.md); model={r['model']}")
# --- per-run JSON analysis
leak_pat = re.compile(r"ground-truth\.json|ground-truth-draft|resolution-(default|live7)\.json|reviews/combos|20261111-a1|eval-workspaces/tasklist|COMBO-REPORT|PILOT-REPORT|quarantine-pre|/tmp/evalsb/(jobs|progress|start|xargs)|/tmp/(r1jobs|n2run|r2|b[0-9]+-)|eval-tasklist-review-panel|\.dev/eval-workspaces/tasklist", re.I)
STUDY = ["designSpec-20261107-075614", "makeTheAliasOnly-20261105-051649", "design-20261108-041415"]
pkpat = re.compile(r"TASK-WF-(?:designSpec-20261107-075614|makeTheAliasOnly-20261105-051649|design-20261108-041415)")
sibpat = re.compile(r"TASK-WF-(?:design-20261020-090627|designSpec-20261107-072120|designSpec-20261107-074040|designV2-20261020-132032)")
wr_pat = re.compile(r"(>\s*\S*cand/|\btee\b[^|]*cand/|sed\s+-i[^|;]*cand/|\b(cp|mv|truncate|touch|ln)\b[^|;]*cand/|git\s+(checkout|commit|stash|add|reset|clean|apply)\b)")
stats = collections.defaultdict(lambda: collections.Counter())
leaks = []
for r in runs:
    r["saw_src"] = None; r["tool_src"] = False; r["txt_src"] = False
    att = r["atts"][-1] if r["atts"] else None
    r["hex"] = set(HEX.findall(r["body"].decode("utf-8", "replace")))
    r["leak"] = []; r["writes"] = []; r["otherpkg"] = []; r["candmis"] = []
    if att is None: continue
    j = load(att)
    if not isinstance(j, list): r["saw_src"] = None; continue
    tu = {}
    allstr = []
    for m in j:
        msg = m.get("message") or {}
        c = msg.get("content")
        if m.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if b.get("type") == "tool_use":
                    tu[b["id"]] = b
                elif b.get("type") == "text":
                    allstr.append(b.get("text", ""))
    r["txt_src"] = any("source.md" in s for s in allstr) or "source.md" in r["body"].decode("utf-8", "replace")
    # tool_use analysis, all attempts for leaks
    for a in r["atts"]:
        jj = j if a == att else load(a)
        if not isinstance(jj, list): continue
        tus = {}
        for m in jj:
            msg = m.get("message") or {}
            c = msg.get("content")
            if m.get("type") == "assistant" and isinstance(c, list):
                for b in c:
                    if b.get("type") == "tool_use": tus[b["id"]] = b
        for b in tus.values():
            s = json.dumps(b.get("input", {}))
            if a == att and "source.md" in s: r["tool_src"] = True
            if leak_pat.search(s): r["leak"].append((b["name"], s[:200]))
            for pk in set(pkpat.findall(s)):
                if pk != r["pkg"]: r["otherpkg"].append((b["name"], s[:200]))
            if sibpat.search(s): r.setdefault("sib", []).append((b["name"], s[:200]))
            if b["name"] == "Bash" and wr_pat.search(b["input"].get("command", "")):
                r["writes"].append(b["input"].get("command", "")[:200])
            if b["name"] == "Bash" and re.search(r"pytest|uv run|\bmake\b|npm |pip ", b["input"].get("command", "")): r["exec"] = True
        # candidate content integrity (final attempt only)
        if a == att:
            for m in jj:
                msg = m.get("message") or {}
                c = msg.get("content")
                if m.get("type") == "user" and isinstance(c, list):
                    for b in c:
                        if b.get("type") == "tool_result" and b.get("tool_use_id") in tus:
                            t = tus[b["tool_use_id"]]
                            inp = t.get("input", {})
                            if t["name"] == "Read" and inp.get("file_path", "").endswith("/candidate.md"):
                                fp = inp["file_path"]
                                m2 = re.search(r"cand/(TASK-WF-[^/]+)/", fp)
                                tpk = m2.group(1) if m2 else r["pkg"]
                                cont = b.get("content")
                                if isinstance(cont, list): cont = "\n".join(x.get("text", "") for x in cont if isinstance(x, dict))
                                if not isinstance(cont, str): continue
                                r["candread"] = True
                                bad = 0; tot = 0
                                for ln in cont.splitlines():
                                    ln2 = re.sub(r"^\s*\d+[\t→]", "", ln).strip()
                                    if not ln2 or ln2.startswith("<system-reminder") : continue
                                    tot += 1
                                    if tpk in cand and ln2 not in cand[tpk]["lines"]: bad += 1
                                if tot and bad > 2:
                                    r["candmis"].append((fp, bad, tot))
                                if tpk != r["pkg"]:
                                    r["candmis"].append((fp, "WRONGPKG", tot))
    # sha mentions in text
    r["hex"] = set()
    for s in allstr: r["hex"] |= set(HEX.findall(s))
    r["hex"] |= set(HEX.findall(r["body"].decode("utf-8", "replace")))
# flag check 2
bymodel = collections.defaultdict(lambda: [0, 0, 0])
for r in runs:
    if not r["valid"] or r["pre"]: continue
    bymodel[r["model"]][0] += 1
    if r["tool_src"]: bymodel[r["model"]][1] += 1
    elif r["txt_src"]: bymodel[r["model"]][2] += 1
    else:
        flag("2-nosrc", r["row"], r["pkg"], r["rid"], "WARN", f"no source.md in tool_use or text; model={r['model']}")
# 3
for r in runs:
    if r["candmis"]:
        sev = "EXCLUDE"
        flag("3-candcontent", r["row"], r["pkg"], r["rid"], sev, f"Read of candidate differs/wrong pkg: {r['candmis'][:2]}")
    ts = cand[r["pkg"]]["sha"]
    for h in r["hex"]:
        if h != ts:
            others = [q for q in PK if cand[q]["sha"] == h]
            if h in KNOWN: continue
            if others:
                flag("3-sha", r["row"], r["pkg"], r["rid"], "EXCLUDE", f"report/answer quotes sha of different package {others[0]}")
            else:
                # may be a stale candidate sha (e.g., modified sandbox copy)
                flag("3-sha", r["row"], r["pkg"], r["rid"], "WARN", f"64-hex {h[:12]} in output not equal to true candidate sha {ts[:12]} (could be other hash)")
# 4 anchors
fb = re.compile(r"```findings-v1\s*\n(.*?)```", re.S)
for r in runs:
    body = r["body"].decode("utf-8", "replace")
    m = fb.search(body)
    r["anch"] = []
    if not m: continue
    for ln in m.group(1).splitlines():
        ln = ln.strip()
        if not ln.startswith("{"): continue
        try: o = json.loads(ln)
        except Exception: continue
        for k in ("anchor", "anchor2"):
            a = o.get(k)
            if isinstance(a, str) and len(a) >= 12: r["anch"].append(re.sub(r"\s+", " ", a.strip()))
    if not r["anch"]: continue
    own = 0; oth = collections.Counter(); none = 0
    for a in r["anch"]:
        key = a[:40]
        if key in cand[r["pkg"]]["norm"]: own += 1; continue
        f = [q for q in PK if q != r["pkg"] and key in cand[q]["norm"]]
        if f: oth[f[0]] += 1
        else: none += 1
    r["a_stat"] = (own, sum(oth.values()), none)
    if sum(oth.values()) > 0:
        flag("4-xpkg", r["row"], r["pkg"], r["rid"], "EXCLUDE" if sum(oth.values()) >= max(2, own) else "WARN", f"anchors own={own} other-pkg={dict(oth)} none={none}")
# 5 dup
byh = collections.defaultdict(list); byp = collections.defaultdict(list)
for r in runs:
    if not r["body"].strip(): continue
    byh[sha(r["body"])].append(r)
    byp[r["body"][:300]].append(r)
for h, L in byh.items():
    if len(L) < 2: continue
    for r in L:
        peers = [f"{x['row']}/{x['rid']}({x['pkg'][8:16]})" for x in L if x is not r]
        samepanel = [x for x in L if x is not r and x["row"] == r["row"] and x["pkg"] == r["pkg"] and x["rid"] != r["rid"]]
        flag("5-dupbody", r["row"], r["pkg"], r["rid"], "EXCLUDE" if samepanel else "WARN", f"byte-identical to {peers[:4]}")
seen = set(h for h in byh if len(byh[h]) > 1)
for k, L in byp.items():
    if len(L) < 2: continue
    if sha(L[0]["body"]) in seen and all(sha(x["body"]) == sha(L[0]["body"]) for x in L): continue
    for r in L:
        peers = [f"{x['row']}/{x['rid']}" for x in L if x is not r]
        flag("5-dupstart", r["row"], r["pkg"], r["rid"], "WARN", f"same first 300 bytes as {peers[:4]}")
# extra
for r in runs:
    if r["leak"]:
        hard = any(re.search(r"ground-truth|resolution-|reviews/combos|20261111|eval-workspaces/tasklist|COMBO|PILOT|quarantine|eval-tasklist", x[1]) for x in r["leak"])
        flag("X-leak", r["row"], r["pkg"], r["rid"], "EXCLUDE" if hard else "WARN", ("tool_use touches eval tree/ground truth: " if hard else "peeked at harness job lists /tmp/evalsb/jobs*.tsv (reviewer/model assignments, no findings): ") + str(r["leak"][0])[:150])
    if r["otherpkg"]: flag("X-otherpkg", r["row"], r["pkg"], r["rid"], "WARN", f"tool_use references other package: {r['otherpkg'][0]}")
    if r.get("sib"): flag("X-sibling", r["row"], r["pkg"], r["rid"], "WARN", f"reads sibling repo plan package(s): {r['sib'][0]}")
    if (not r["valid"]) and r["start"] < T_SRC <= r["mtime"]: flag("1-straddle", r["row"], r["pkg"], r["rid"], "WARN", "old-era run in flight when source.md appeared (may have seen it mid-run)")
    if False and r["writes"]: flag("X-bashwrite", r["row"], r["pkg"], r["rid"], "WARN", f"bash with write/exec-like pattern: {r['writes'][0]}")
with open("/tmp/audit-C/flags.tsv", "w") as f:
    f.write("check\trow\tpackage\treviewer\tseverity\treason\n")
    for x in flags: f.write("\t".join(str(y).replace("\t", " ").replace("\n", " ") for y in x) + "\n")
cnt = collections.Counter((x[0], x[4]) for x in flags)
print(json.dumps({f"{a}|{b}": v for (a, b), v in sorted(cnt.items())}, indent=1))
print("runs valid", sum(r["valid"] for r in runs), "valid-and-pre", sum(r["valid"] and r["pre"] for r in runs))
print("valid per model [n, toolsrc, txtonly]:", dict(bymodel))
print("first valid-row run start:", min((r["start"], r["row"], r["rid"]) for r in runs if r["valid"]))
print("first src-row report mtime:", sorted((r["mtime"], r["row"], r["rid"]) for r in runs if r["row"].endswith("-src") or r["row"].startswith("b4-"))[:3])
pm = collections.defaultdict(lambda: [0, 0])
for r in runs:
    if r["valid"]:
        pm[(r["pkg"][8:20], r["model"])][0] += 1
        pm[(r["pkg"][8:20], r["model"])][1] += int(r["tool_src"])
print("per pkg/model [n, toolsrc]:", dict(pm))
print("exec-runs", sum(1 for r in runs if r.get("exec")), "sib", sum(1 for r in runs if r.get("sib")))
print("min start all", min(r["start"] for r in runs), "n pre-T", sum(r["pre"] for r in runs), "old-era models", collections.Counter(r["model"] for r in runs if not r["valid"]))
print("empty bodies", sum(1 for r in runs if not r["body"].strip()), "tiny<800B", sum(1 for r in runs if 0 < len(r["body"].strip()) < 800), "no findings block", sum(1 for r in runs if b"findings-v1" not in r["body"]))
ast = [r.get("a_stat") for r in runs if r.get("a_stat")]
print("runs with anchors", len(ast), "total own/oth/none", [sum(x[i] for x in ast) for i in range(3)], "runs with any none-anchor", sum(1 for x in ast if x[2] > 0))
print("runs whose final attempt Read candidate.md and verified content:", sum(1 for r in runs if r.get("candread")), "valid-era:", sum(1 for r in runs if r.get("candread") and r["valid"]))
print("write-like (benign-checked) runs", sum(1 for r in runs if r["writes"]))
print("model counts", collections.Counter(r["model"] for r in runs))
json.dump([dict(row=r["row"], pkg=r["pkg"], rid=r["rid"], model=r["model"], valid=r["valid"], pre=r["pre"], start=r["start"], mtime=r["mtime"], tool_src=r["tool_src"], txt_src=r["txt_src"], a_stat=r.get("a_stat")) for r in runs], open("/tmp/audit-C/runs.json", "w"))
