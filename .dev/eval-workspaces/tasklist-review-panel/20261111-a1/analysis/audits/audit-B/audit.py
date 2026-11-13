import os, re, json, hashlib, sys, collections
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PKGS = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
SEV = {"CRITICAL", "MAJOR", "MINOR"}
CAT = {"contradiction", "unpassable-check", "data-loss", "safety", "missing-requirement", "other"}
MODELS = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "grok-4.7": "grok", "gpt-6-luna": "luna",
          "gpt-6.1-terra": "terra", "gpt-6.1-sol": "sol", "muse-ember-1.0": "ember", "muse-wonder-1.0": "wonder",
          "muse-wonder-full-1.0": "wonder"}
EXCL_DIR = re.compile(r"contaminated|superseded|quarantine|^i[12]-", re.I)
ws = lambda s: re.sub(r"\s+", " ", s).strip()
cand = {}; cand_ws = {}; sha = {}
for p in PKGS:
    b = open(f"{E}/{p}/candidate.md", "rb").read()
    cand[p] = b.decode("utf8", "replace"); cand_ws[p] = ws(cand[p]); sha[p] = hashlib.sha256(b).hexdigest()
flags = []  # (check,row,pkg,rid,sev,reason)
runs = []
def flag(c, r, sev, reason):
    flags.append((c, r["row"], r["pkg"], r["rid"], sev, reason))
for p in PKGS:
    base = f"{E}/{p}/reviews/combos"
    for row in sorted(os.listdir(base)):
        d = f"{base}/{row}"
        if not os.path.isdir(d) or EXCL_DIR.search(row): continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".md") or ".attempt" in f: continue
            if ".catfix" in f: continue
            rid = f[:-3]
            txt = open(f"{d}/{f}", "rb").read().decode("utf8", "replace")
            meta = {}
            try: meta = json.load(open(f"{d}/{rid}.meta.json"))
            except Exception: pass
            runs.append(dict(row=row, pkg=p, rid=rid, txt=txt, meta=meta, size=len(txt.encode()), dir=d))
print("runs", len(runs), file=sys.stderr)
# parse
blk_re = re.compile(r"```findings-v1[^\n]*\n(.*?)```", re.S)
for r in runs:
    t = r["txt"]; p = r["pkg"]
    m = blk_re.findall(t)
    r["nblocks"] = len(m)
    r["findings"] = None; r["badlines"] = []
    if m:
        fs = []
        for ln in m[-1].split("\n"):
            if not ln.strip(): continue
            try:
                o = json.loads(ln)
                if not isinstance(o, dict): raise ValueError("not object")
                fs.append(o)
            except Exception as e:
                r["badlines"].append(ln[:60])
        r["findings"] = fs
        r["grep_blocking"] = len(re.findall(r'"blocking" *: *true', m[-1]))
    vm = re.findall(r"^\s*\**verdict:?\**\s*:?\s*\**(PASS|FAIL)\b", t, re.M | re.I)
    r["verdict"] = vm[-1].upper() if vm else None
    r["lastline"] = [l for l in t.split("\n") if l.strip()][-1] if t.strip() else ""
# CHECK 1-5
claimhash = collections.defaultdict(list)
for r in runs:
    t = r["txt"]; p = r["pkg"]; fs = r["findings"]
    # 1
    low = t.lower()
    pre = low[:500]
    pre = re.sub(r"\b(not|n't|no|never)\W{0,3}(be\W{0,3})?incomplete\b", "", pre)
    zero_valid = (fs is not None and len(fs) == 0 and r["verdict"] in ("PASS", "FAIL") and re.search(r"coverage|covered", low))
    if r["size"] < 600:
        if zero_valid and r["verdict"] == "PASS": flag("1-short", r, "WARN", f"report {r['size']} bytes but a valid zero-finding PASS with coverage statement")
        else: flag("1-short", r, "EXCLUDE", f"report {r['size']} bytes")
    inc_verdict = re.search(r"^\W*verdict:?\W*incomplete", t, re.M | re.I)
    if inc_verdict or re.search(r"\bincomplete\b", pre) or re.search(r"^\W*(#+\s*)?review incomplete", low, re.M):
        flag("1-incomplete", r, "EXCLUDE", "positive 'incomplete' refusal" + (" (verdict: INCOMPLETE)" if inc_verdict else "") + "; " + ("empty findings block" if fs == [] else "findings=%s" % (len(fs) if fs is not None else None)))
    else:
        body_pre = re.split(r"```findings-v1", t)[0].lower()
        mm = re.search(r"(?<!no )(?<!not )(?<!nor )(source\.md|source document|requirements document|input file|merged-requirements\.md)[^.\n]{0,80}(is missing|are missing|unreadable|not found|could not be read|cannot be read|does not exist|missing or unreadable)", body_pre)
        if mm:
            neg = re.search(r"(no input (was )?missing|nothing (was )?missing|no input is missing|not incomplete)", body_pre)
            if not neg:
                hit = mm.start() < 600
                flag("1-missing-input", r, "EXCLUDE" if (hit or r["size"] < 2500) else "WARN", "mentions missing/unreadable input: ..." + ws(body_pre[max(0, mm.start()-20):mm.end()+20])[:120])
    if "API Error" in t[:600] or ("api error" in low and r["size"] < 2000): flag("1-apierror", r, "EXCLUDE", "'API Error' text")
    if "unrecognized_model" in low and not ("unrecognized_model" in cand[p].lower()):
        flag("1-unrecognized_model", r, "EXCLUDE" if (r["size"] < 2000 or fs is None) else "WARN", "'unrecognized_model' text (not in candidate)")
    # 2
    first = [l for l in t.split("\n") if l.strip()][:1]
    if not first or first[0].strip() != "review: 1 of 3":
        flag("2-firstline", r, "WARN", "first line: " + (first[0][:60] if first else "<none>"))
    if len(re.findall(r"^review: \d of 3", t, re.M)) > 1: flag("2-multi-review-marker", r, "WARN", "multiple 'review: N of 3' markers")
    if fs is None:
        flag("2-noblock", r, "EXCLUDE", "no findings-v1 block")
    else:
        if r["nblocks"] > 1: flag("2-multiblock", r, "WARN", f"{r['nblocks']} findings-v1 blocks")
        if r["badlines"]: flag("2-badjson", r, "EXCLUDE" if len(r["badlines"]) >= max(1, len(fs)) else "WARN", f"{len(r['badlines'])} unparseable lines vs {len(fs)} parsed")
        bad = []
        for o in fs:
            miss = [k for k in ("id", "severity", "blocking", "category", "anchor", "claim") if k not in o]
            if miss: bad.append(f"{o.get('id')}:missing {miss}")
            elif o["severity"] not in SEV: bad.append(f"{o['id']}:sev {o['severity']}")
            elif o["category"] not in CAT: bad.append(f"{o['id']}:cat {o['category']}")
            elif not isinstance(o["blocking"], bool): bad.append(f"{o['id']}:blocking type")
            if "refs" not in o and not miss: pass
        if bad: flag("2-schema", r, "WARN", "; ".join(bad[:4]) + (f" (+{len(bad)-4})" if len(bad) > 4 else ""))
        ids = [str(o.get("id")) for o in fs]
        if len(ids) != len(set(ids)): flag("X-dup-ids", r, "WARN", "duplicate finding ids")
        incons = [str(o.get("id")) for o in fs if isinstance(o.get("blocking"), bool) and ((o.get("severity") == "MINOR" and o["blocking"]) or (o.get("severity") == "CRITICAL" and not o["blocking"]))]
        if incons: flag("X-sev-blocking-mismatch", r, "WARN", "severity vs blocking inconsistent: " + ",".join(incons[:5]))
        nb = sum(1 for o in fs if o.get("blocking") is True)
        r["nb"] = nb
        if r["verdict"] is None: flag("2-noverdict", r, "WARN", "no verdict line")
        elif (nb > 0) != (r["verdict"] == "FAIL"): flag("2-verdict-inconsistent", r, "WARN", f"blocking={nb} verdict={r['verdict']}")
        if r["verdict"] is not None and not re.match(r"^\W*verdict:?\W*(PASS|FAIL)\W*$", r["lastline"], re.I):
            flag("X-verdict-not-last", r, "WARN", "last line: " + r["lastline"][:60])
        # 5
        if nb != r["grep_blocking"]: flag("5-blocking-parse", r, "WARN", f"jq/parsed={nb} grep={r['grep_blocking']}")
        # 3
        n = len(fs); inv = 0; invws = 0; lenbad = 0; foreign = 0
        for o in fs:
            a = o.get("anchor") if isinstance(o.get("anchor"), str) else ""
            if not (12 <= len(a) <= 200): lenbad += 1
            ok = a in cand[p]
            okws = ws(a) in cand_ws[p]
            if not ok: inv += 1
            if not okws: invws += 1
            if not okws and a:
                others = [q for q in PKGS if q != p and ws(a) in cand_ws[q]]
                if others: foreign += 1
        r["n"] = n; r["inv"] = inv; r["invws"] = invws
        r["valid_rate"] = (n - invws) / n if n else None
        r["exact_rate"] = (n - inv) / n if n else None
        if lenbad: flag("3-anchor-length", r, "WARN", f"{lenbad}/{n} anchors outside 12-200 chars")
        if n:
            f_ = invws / n
            if f_ >= 0.9: flag("3-anchors", r, "EXCLUDE", f"{invws}/{n} anchors not in candidate (ws-normalised); exact-invalid {inv}")
            elif f_ >= 0.5: flag("3-anchors", r, "WARN", f"{invws}/{n} anchors not in candidate (ws-normalised); exact-invalid {inv}")
            elif inv / n >= 0.5: flag("3-anchors-exact", r, "WARN", f"{inv}/{n} anchors fail exact match (pass after whitespace normalisation)")
            if foreign and foreign / n >= 0.5: flag("4-foreign-anchors", r, "EXCLUDE", f"{foreign}/{n} anchors occur in another package's candidate, not its own")
            elif foreign: flag("4-foreign-anchors", r, "WARN", f"{foreign}/{n} anchors occur only in another package's candidate")
            anc = [ws(o.get("anchor", "")) for o in fs]
            if n >= 3 and len(set(anc)) == 1: flag("X-same-anchor", r, "WARN", "all findings share one anchor")
            short = [o.get("id") for o in fs if len(str(o.get("claim", ""))) < 25]
            if short: flag("X-short-claim", r, "WARN", f"claims <25 chars: {short[:4]}")
        else:
            r["valid_rate"] = None
    # 4 sha
    shas = set(re.findall(r"\b[0-9a-f]{64}\b", t))
    if shas and sha[p] not in shas: flag("4-sha-mismatch", r, "WARN", "quotes sha " + list(shas)[0][:12] + " != true " + sha[p][:12])
    for q in PKGS:
        if q != p and q in t: flag("4-other-pkg-mention", r, "WARN", "mentions other package id " + q)
    for q in PKGS:
        if q != p and sha[q] in t: flag("4-sha-other-pkg", r, "EXCLUDE", "quotes sha of another package " + q)
    # meta
    mt = r["meta"]
    if not mt: flag("X-nometa", r, "WARN", "no meta.json")
    else:
        if mt.get("model_ok") is False: flag("X-model-not-ok", r, "WARN", f"expected {mt.get('expected_model')} observed {mt.get('observed_model')!r}")
        if mt.get("findings_block") is False and fs: flag("X-meta-block-mismatch", r, "WARN", "meta findings_block=false but report has block")
        if mt.get("output_tokens_all", 1) == 0: flag("X-zero-tokens", r, "WARN", "meta output_tokens_all=0")
    if os.path.exists(f"{r['dir']}/{r['rid']}.fallback.log"): flag("X-fallback-used", r, "WARN", "fallback ladder used: " + open(f"{r['dir']}/{r['rid']}.fallback.log").read().strip().replace("\n", " | ")[:150])
    # restates candidate
    lines = [ws(l) for l in t.split("\n") if len(ws(l)) > 40 and "findings-v1" not in l and not l.strip().startswith("{")]
    if len(lines) >= 5:
        frac = sum(1 for l in lines if l in cand_ws[p]) / len(lines)
        r["restate"] = frac
        if frac >= 0.4: flag("X-restates-candidate", r, "WARN", f"{frac:.0%} of long report lines occur verbatim in candidate")
    # truncated
    if r["verdict"] is None or (fs is not None and not t.rstrip().endswith(("PASS", "FAIL", "PASS.", "FAIL.", "**PASS**", "**FAIL**"))):
        if not re.search(r"verdict", r["lastline"], re.I): flag("X-truncated", r, "WARN", "report does not end with verdict: " + r["lastline"][-60:])
    # hash
    body = ws(t).lower()
    r["bodyhash"] = hashlib.sha256(body.encode()).hexdigest()
    if fs:
        r["claimsig"] = frozenset(ws(str(o.get("claim", ""))).lower() for o in fs)
        r["anchorsig"] = frozenset(ws(str(o.get("anchor", ""))).lower() for o in fs)
# duplicate hashes
by = collections.defaultdict(list)
for r in runs: by[r["bodyhash"]].append(r)
for h, g in by.items():
    if len(g) > 1:
        for r in g: flag("X-identical-body", r, "WARN", "identical report body to " + ",".join(f"{x['row']}/{x['rid']}" for x in g if x is not r)[:200])
# same row same pkg identical / near identical findings between reviewers
byrow = collections.defaultdict(list)
for r in runs:
    if r.get("claimsig"): byrow[(r["pkg"], r["row"])].append(r)
for k, g in byrow.items():
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            a, b = g[i], g[j]
            if len(a["claimsig"]) >= 2 and len(b["claimsig"]) >= 2:
                jc = len(a["claimsig"] & b["claimsig"]) / len(a["claimsig"] | b["claimsig"])
                ja = len(a["anchorsig"] & b["anchorsig"]) / len(a["anchorsig"] | b["anchorsig"])
                if jc >= 0.8:
                    for x, y in ((a, b), (b, a)): flag("X-same-row-dup-claims", x, "WARN", f"claims Jaccard {jc:.2f} with {y['rid']} in same row")
                elif ja >= 1.0 and len(a["anchorsig"]) >= 3:
                    for x, y in ((a, b), (b, a)): flag("X-same-row-same-anchors", x, "WARN", f"identical anchor set with {y['rid']} in same row")
# cross-row exact claim-set duplicates (same package)
bysig = collections.defaultdict(list)
for r in runs:
    if r.get("claimsig") and len(r["claimsig"]) >= 2: bysig[(r["pkg"], r["claimsig"])].append(r)
for k, g in bysig.items():
    if len({(x["row"], x["rid"]) for x in g}) > 1:
        for r in g: flag("X-crossrun-identical-claims", r, "WARN", "identical claim set as " + ",".join(f"{x['row']}/{x['rid']}" for x in g if x is not r)[:160])
# write
sevrank = {"EXCLUDE": 0, "WARN": 1}
flags.sort(key=lambda f: (sevrank[f[4]], f[0], f[2], f[1], f[3]))
with open("/tmp/audit-B/flags.tsv", "w") as o:
    o.write("check\trow\tpackage\treviewer\tseverity\treason\n")
    for f in flags: o.write("\t".join(x.replace("\t", " ").replace("\n", " ") for x in f) + "\n")
# stats
st = collections.defaultdict(lambda: [0, 0, 0, 0, 0])  # runs, findings, valid, exactvalid, runs with fs
for r in runs:
    mname = MODELS.get(r["meta"].get("expected_model"), r["meta"].get("expected_model") or "unknown")
    s = st[mname]; s[0] += 1
    if r.get("findings") is not None:
        s[4] += 1; s[1] += r["n"]; s[2] += r["n"] - r["invws"]; s[3] += r["n"] - r["inv"]
cnt = collections.Counter((f[0], f[4]) for f in flags)
exrun = {(f[2], f[1], f[3]) for f in flags if f[4] == "EXCLUDE"}
warnrun = {(f[2], f[1], f[3]) for f in flags if f[4] == "WARN"} - exrun
json.dump({"runs": len(runs), "cnt": {f"{k[0]}|{k[1]}": v for k, v in cnt.items()}, "stats": st, "exclude_runs": sorted(exrun), "nwarn": len(warnrun),
           "pkgruns": collections.Counter(r["pkg"] for r in runs), "rows": len({(r["pkg"], r["row"]) for r in runs})}, open("/tmp/audit-B/stats.json", "w"), indent=1, default=lambda x: list(x))
