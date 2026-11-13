import json, os, re, collections, hashlib
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PK = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
CATS = {"contradiction", "unpassable-check", "data-loss", "safety", "missing-requirement", "other"}
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$")
flat = lambda s: " ".join(s.split())

def check(obj, seen):
    fid = obj.get("id")
    if not isinstance(fid, str) or not ID.match(fid): return "bad-id"
    if fid in seen: return "dup-id"
    if obj.get("severity") not in ("CRITICAL", "MAJOR", "MINOR"): return "bad-severity"
    if not isinstance(obj.get("blocking"), bool): return "blocking-not-bool"
    if obj["blocking"] and obj["severity"] == "MINOR": return "MINOR-blocking"
    if obj.get("category") not in CATS: return "category:" + str(obj.get("category"))
    a = obj.get("anchor")
    if not isinstance(a, str): return "anchor-not-str"
    if len(flat(a)) < 12: return "anchor<12"
    if len(flat(a)) > 200: return "anchor>200"
    a2 = obj.get("anchor2")
    if a2 is not None:
        if not isinstance(a2, str): return "anchor2-not-str"
        if len(flat(a2)) < 12: return "anchor2<12"
        if len(flat(a2)) > 200: return "anchor2>200"
    r = obj.get("refs", [])
    if not isinstance(r, list) or len(r) > 8 or not all(isinstance(x, str) for x in r): return "refs-bad"
    c = obj.get("claim")
    if not isinstance(c, str): return "claim-not-str"
    if len(flat(c)) > 300: return "claim>300"
    return None

def raw_lines(p):
    t = open(p, errors="replace").read()
    m = re.search(r"^#{1,6}\s+Findings block\s*$", t, re.M | re.I)
    if not m: return None
    t = t[m.start():]
    b = re.findall(r"```findings-v1\s*\n(.*?)```", t, re.S)
    return b[-1].splitlines() if b else None

# --- clustering helpers (copy of findings.py logic)
REF = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")
SEC = re.compile(r"^\d+(?:\.\d+)*$")
HEAD = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
def locate(text, quote):
    q = flat(quote)
    if not q: return []
    chars = []; line_of = []; line = 0; prev = True
    for ch in text:
        if ch.isspace():
            if not prev:
                chars.append(" "); line_of.append(line); prev = True
        else:
            chars.append(ch); line_of.append(line); prev = False
        if ch == "\n": line += 1
    norm = "".join(chars); out = []; pos = norm.find(q)
    while pos != -1:
        out.append((line_of[pos], line_of[pos + len(q) - 1] + 1)); pos = norm.find(q, pos + 1)
    return out
def refs_norm(f):
    pcs = [f.get("anchor") or "", f.get("anchor2") or "", f.get("claim") or ""]
    refs = [r for r in (f.get("refs") or []) if isinstance(r, str)]
    pcs += refs
    s = set()
    for p in pcs:
        for m in REF.finditer(p): s.add(m.group(0).upper())
    for r in refs:
        if SEC.match(r.strip()): s.add(r.strip())
    return sorted(t for t in s if not t.startswith("SHA-"))
def section_of(text, line):
    lines = text.splitlines()
    for i in range(min(line, len(lines) - 1), -1, -1):
        m = HEAD.match(lines[i])
        if m:
            n = re.match(r"^(\d+(?:\.\d+)*)", m.group(1))
            return n.group(1) if n else re.sub(r"[^a-z0-9]+", "-", m.group(1).lower())
    return "top"
def ann(f, text):
    o = dict(f); sp = locate(text, f["anchor"]); o["span"] = sp[0] if sp else None
    o["span2"] = None
    if f.get("anchor2"):
        s2 = locate(text, f["anchor2"]); o["span2"] = s2[0] if s2 else None
    o["refs_norm"] = refs_norm(f)
    o["section"] = section_of(text, o["span"][0]) if o["span"] else "none"
    o["fp"] = hashlib.sha256(("v1|" + o["section"] + "|" + ",".join(o["refs_norm"])).encode()).hexdigest()[:16]
    return o
def spans(x): return [s for s in (x.get("span"), x.get("span2")) if s]
def same(a, b):
    if a.get("fp") and a["fp"] == b.get("fp") and a.get("refs_norm"): return True
    ra, rb = set(a["refs_norm"]), set(b["refs_norm"])
    if ra & rb or (not ra and not rb):
        for s1 in spans(a):
            for s2 in spans(b):
                if s1[0] <= s2[1] + 3 and s2[0] <= s1[1] + 3: return True
    return False

rows = [r for r in sorted(os.listdir(f"{E}/combos")) if not re.search(r"contaminated|superseded|quarantine|^i1-|^i2-", r)]
cand = {p: open(f"{E}/{p}/candidate.md").read() for p in PK}
flags = []; nostdout = []
drop_reason = collections.Counter(); drop_model = collections.defaultdict(collections.Counter)
dropped_blocking_total = 0; verdict_flip = []
chain_rows = []; chain_total = 0; rows_total = 0
multi_blocking_same_rev_diff_section = []
mix_section = []
for row in rows:
    for pkg in PK:
        d = f"{E}/combos/{row}/{pkg}"
        if not os.path.exists(f"{d}/ledger.json"): continue
        led = json.load(open(f"{d}/ledger.json"))
        res = json.load(open(f"{d}/resolution.json"))
        mdl = {r["reviewer_id"]: r["model"] for r in res["reviewers"]}
        if not os.path.exists(f"{d}/merge-stdout.txt"): nostdout.append(f"{row}/{pkg[8:20]}")
        # verdict
        anyb_ledger = any(r["blocking"] for r in led["rows"])
        dropped_blk = []
        raws = {}
        for rv in led["rounds"][-1]["reviewers"]:
            rid = rv["reviewer_id"]; p = rv["report"]
            if not os.path.exists(p): continue
            lines = raw_lines(p)
            seen = set(); allf = []
            for ln in (lines or []):
                if not ln.strip(): continue
                try: o = json.loads(ln)
                except Exception: drop_reason["json"] += 1; continue
                if not isinstance(o, dict) or "prior" in o: continue
                e = check(o, seen)
                if e:
                    drop_reason[e] += 1; drop_model[mdl.get(rid, "?")][e.split(":")[0]] += 1
                    if o.get("blocking") is True: dropped_blk.append((rid, o.get("id"), e))
                    continue
                seen.add(o["id"]); allf.append(o)
            raws[rid] = allf
        if dropped_blk:
            dropped_blocking_total += len(dropped_blk)
            if not anyb_ledger:
                verdict_flip.append((row, pkg, dropped_blk))
            flags.append((row, pkg[8:20], dropped_blk, "ledger_blocking=" + str(anyb_ledger)))
        # clustering
        for r in led["rows"]:
            rows_total += 1
            mem = []
            for m in r["members"]:
                f = next((x for x in raws.get(m["reviewer_id"], []) if x["id"] == m["fid"]), None)
                if f: mem.append((m, ann(f, cand[pkg])))
            if len(mem) < 3: continue
            # connectivity: count pairs not directly same
            fs = [a for _, a in mem]
            nonpair = sum(1 for i in range(len(fs)) for j in range(i + 1, len(fs)) if not same(fs[i], fs[j]))
            tot = len(fs) * (len(fs) - 1) // 2
            secs = {a["section"] for a in fs}
            lo = min((s[0] for a in fs for s in spans(a)), default=None); hi = max((s[1] for a in fs for s in spans(a)), default=None)
            width = (hi - lo) if lo is not None else None
            if nonpair > 0:
                chain_total += 1
                chain_rows.append((row, pkg[8:20], r["lid"], len(fs), f"{nonpair}/{tot} pairs not directly same", sorted(secs), width, r["blocking"]))
print("no merge-stdout:", len(nostdout), sorted({x.split('/')[0] for x in nostdout})[:30])
print("dropped-reason tally:", dict(drop_reason))
print("dropped-blocking findings total:", dropped_blocking_total)
print("rows where all dropped blockings AND ledger had no blocking row (verdict PASS wrongly?):", len(verdict_flip))
for v in verdict_flip[:40]: print("  ", v)
print("rows with >=3 members:", "chained(not all pairs same):", chain_total, "of", rows_total)
wide = [c for c in chain_rows if c[6] is not None and c[6] > 60]
print("chained rows with span width >60 lines:", len(wide))
for c in sorted(chain_rows, key=lambda c: -(c[6] or 0))[:12]: print("  ", c)
json.dump({"drop_model": {k: dict(v) for k, v in drop_model.items()}, "verdict_flip": verdict_flip, "chain_rows": chain_rows}, open("/tmp/audit-D/audit2.json", "w"), indent=1, default=str)
print({k: dict(v) for k, v in drop_model.items()})
with open("/tmp/audit-D/flags.tsv", "a") as fh:
    flip = {(v[0], v[1]) for v in verdict_flip}
    for row, pk, db, lb in flags:
        for rid, fid, why in db:
            sev = "EXCLUDE" if (row, "TASK-WF-" + pk) in flip or any((row, p) in flip for p in PK if p[8:20] == pk) else "WARN"
            fh.write(f"3-dropped-blocking\t{row}\t{pk}\t{rid}\t{sev}\tblocking finding {fid} dropped by merge ({why}); " + ("ledger then has NO blocking row, so verdict PASS can be wrong" if sev == "EXCLUDE" else "ledger still FAIL via other rows") + "\n")
    for c in chain_rows:
        if c[3] >= 8 or len(c[5]) >= 4:
            fh.write(f"7-megacluster\t{c[0]}\t{c[1]}\t-\tWARN\trow {c[2]} merges {c[3]} findings across {len(c[5])} sections, {c[4]}, width {c[6]} lines, blocking={c[7]}\n")
    for x in nostdout:
        r, p = x.split("/")
        fh.write(f"8-nostdout\t{r}\t{p}\t-\tWARN\tmerge-stdout.txt missing; merge warnings/drop reasons UNVERIFIED (audit recomputed them)\n")
print("mega:", sum(1 for c in chain_rows if c[3] >= 8 or len(c[5]) >= 4))
