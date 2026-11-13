import json, os, re, hashlib, sys, glob, collections
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PK = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
flags = []
cnt = collections.Counter()
drop_by_model = collections.defaultdict(lambda: [0, 0, 0])  # raw, kept, reviewers
extra = collections.Counter()
extra_list = collections.defaultdict(list)

def F(check, row, pkg, rid, sev, reason):
    flags.append((check, row, pkg, rid, sev, reason))
    cnt[(check, sev)] += 1

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_block(p):
    t = open(p, errors="replace").read()
    m = re.findall(r"```findings-v1\s*\n(.*?)```", t, re.S)
    if not m:
        return None, 0
    out, bad = [], 0
    for ln in m[-1].splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            bad += 1
    return out, bad

rows = sorted(d for d in os.listdir(f"{E}/combos") if os.path.isdir(f"{E}/combos/{d}"))
skip = re.compile(r"contaminated|superseded|quarantine|^i1-|^i2-")
rows = [r for r in rows if not skip.search(r)]
merges = 0
sigs = collections.defaultdict(list)
for row in rows:
    for pkg in PK:
        d = f"{E}/combos/{row}/{pkg}"
        mp = f"{d}/merged-1.md"
        if not os.path.exists(mp):
            continue
        merges += 1
        md = open(mp).read()
        mt = os.path.getmtime(mp)
        rdir = f"{E}/{pkg}/reviews/combos/{row}"
        try:
            res = json.load(open(f"{d}/resolution.json"))
            led = json.load(open(f"{d}/ledger.json"))
        except Exception as e:
            F("0-load", row, pkg, "-", "EXCLUDE", f"cannot load resolution/ledger: {e}")
            continue
        panel = [r["reviewer_id"] for r in res["reviewers"]]
        listed = re.findall(r"^- (\S+): report (\S+), block ok (true|false)\s*$", md, re.M)
        lids = [x[0] for x in listed]
        # 1 panel equality
        if sorted(lids) != sorted(panel):
            F("1-panel", row, pkg, ",".join(sorted(set(lids) ^ set(panel))), "EXCLUDE", f"merged lists {lids} vs resolution {panel}")
        present = sorted(f[:-3] for f in os.listdir(rdir) if re.fullmatch(r"[a-z0-9]+-\d+\.md", f)) if os.path.isdir(rdir) else []
        if sorted(present) != sorted(panel):
            F("1-panel", row, pkg, ",".join(sorted(set(present) ^ set(panel))), "WARN", f"reports present {present} vs panel {panel}")
        ledrev = {r["reviewer_id"]: r for r in led["rounds"][-1]["reviewers"]}
        # extra files like catfix / stale in dir
        for f in os.listdir(rdir) if os.path.isdir(rdir) else []:
            if re.search(r"catfix|stale|quarant|old|bak", f):
                extra["stray-files-in-reports-dir"] += 1
                extra_list["stray"].append(f"{row}/{pkg[8:20]}/{f}")
        raw = {}
        for rid, rp, bok in listed:
            exp = f"{rdir}/{rid}.md"
            if rp != exp:
                F("1-path", row, pkg, rid, "EXCLUDE", f"report path {rp} != current {exp}")
            if not os.path.exists(rp):
                F("1-path", row, pkg, rid, "EXCLUDE", "listed report missing")
                continue
            if os.path.exists(exp) and os.path.getmtime(exp) > mt + 1:
                F("5-stale", row, pkg, rid, "EXCLUDE", f"report newer than merged-1.md by {int(os.path.getmtime(exp)-mt)}s")
            cs = sha(rp)
            lr = ledrev.get(rid)
            if lr and lr.get("report_sha256") != cs:
                F("5-stale", row, pkg, rid, "EXCLUDE", "report sha256 differs from ledger report_sha256 (report changed after merge)")
            if lr is None:
                F("1-panel", row, pkg, rid, "EXCLUDE", "reviewer not in ledger rounds")
            blk, bad = parse_block(rp)
            raw[rid] = blk
            if bad:
                F("3-parse", row, pkg, rid, "WARN", f"{bad} unparsable findings lines")
            mem = [(m, r) for r in led["rows"] for m in r["members"] if m["reviewer_id"] == rid]
            n_raw = len(blk) if blk is not None else 0
            n_led = len(mem)
            drop_by_model[res_model := next((x["model"] for x in res["reviewers"] if x["reviewer_id"] == rid), "?")][0] += n_raw
            drop_by_model[res_model][1] += n_led
            drop_by_model[res_model][2] += 1
            if bok == "false":
                F("2-blockok", row, pkg, rid, "EXCLUDE", f"block ok false; raw findings={n_raw}, ledger members={n_led}" + ("" if blk is not None else " (no findings-v1 block)"))
            if blk is None and bok == "true":
                F("2-blockok", row, pkg, rid, "WARN", "block ok true but no findings block parsed by audit")
            if n_led < n_raw:
                sev = "EXCLUDE" if (n_raw - n_led) > 0.5 * n_raw else "WARN"
                F("3-conserve", row, pkg, rid, sev, f"raw {n_raw} vs ledger members {n_led} (dropped {n_raw-n_led})")
            elif n_led > n_raw:
                F("3-conserve", row, pkg, rid, "WARN", f"ledger members {n_led} > raw {n_raw}")
            # id-level
            if blk is not None:
                rawids = {f["id"] for f in blk}
                ledids = {m["fid"] for m, _ in mem}
                if rawids != ledids and bok == "true":
                    F("3-conserve", row, pkg, rid, "WARN", f"fid mismatch raw-only={sorted(rawids-ledids)} ledger-only={sorted(ledids-rawids)}")
                # 4 blocking
                rb = {f["id"]: bool(f.get("blocking")) for f in blk}
                nb_raw = sum(rb.values())
                nb_led = sum(1 for m, _ in mem if m["blocking"])
                if nb_raw != nb_led and bok == "true":
                    F("4-blocking", row, pkg, rid, "WARN", f"raw blocking {nb_raw} vs ledger blocking members {nb_led}")
                for m, _ in mem:
                    if m["fid"] in rb and rb[m["fid"]] != m["blocking"]:
                        F("4-blocking", row, pkg, rid, "WARN", f"{m['fid']} blocking flag changed raw={rb[m['fid']]} ledger={m['blocking']}")
                # model/meta
                mp_ = f"{rdir}/{rid}.meta.json"
                if os.path.exists(mp_):
                    meta = json.load(open(mp_))
                    rm = next(x for x in res["reviewers"] if x["reviewer_id"] == rid)
                    if meta.get("expected_model") != rm["model"]:
                        F("6-model", row, pkg, rid, "EXCLUDE", f"resolution model {rm['model']} != meta expected {meta.get('expected_model')}")
                    if meta.get("observed_model") != meta.get("expected_model"):
                        F("6-model", row, pkg, rid, "WARN", f"observed {meta.get('observed_model')} != expected {meta.get('expected_model')}")
                    for k in ("tier", "alias"):
                        if not rm.get(k):
                            F("6-model", row, pkg, rid, "WARN", f"resolution missing {k}")
                else:
                    F("6-model", row, pkg, rid, "WARN", "meta.json missing")
        # 4 row-level
        anyb = False
        for r in led["rows"]:
            rb = any(m["blocking"] for m in r["members"])
            if rb != r["blocking"]:
                F("4-blocking", row, pkg, "-", "WARN", f"{r['lid']} row blocking={r['blocking']} but any-member={rb}")
            anyb |= r["blocking"]
            # table
            mm = re.search(rf"^\| {r['lid']} \| (\S+) \| (yes|no) \|", md, re.M)
            if not mm or (mm.group(2) == "yes") != r["blocking"]:
                F("4-blocking", row, pkg, "-", "WARN", f"{r['lid']} md table blocking mismatch with ledger.json")
        v = re.search(r"verdict: (\w+)", md)
        sv = None
        try:
            sv = json.loads(open(f"{d}/merge-stdout.txt").read().split("\n", 1)[1]).get("verdict")
        except Exception:
            try:
                sv = json.loads(open(f"{d}/merge-stdout.txt").read()).get("verdict")
            except Exception:
                pass
        want = "FAIL" if anyb else "PASS"
        mv = v.group(1) if v else None
        if mv != want:
            F("4-blocking", row, pkg, "-", "WARN", f"verdict md={mv} stdout={sv} but expected {want} from blocking rows")
        # 5 doc sha / round
        cand = f"{E}/{pkg}/candidate.md"
        cs = sha(cand)
        for rn in led["rounds"]:
            if rn["doc_sha256"] != cs:
                F("5-doc", row, pkg, "-", "EXCLUDE", f"ledger doc sha {rn['doc_sha256'][:10]} != candidate {cs[:10]}")
        if len(led["rounds"]) != 1 or led["rounds"][0]["n"] != 1:
            F("5-round", row, pkg, "-", "WARN", f"ledger rounds {[r['n'] for r in led['rounds']]}")
        if os.path.isdir(f"{d}/stale-r1"):
            extra["stale-r1-dirs"] += 1
        if os.path.exists(f"{d}/stale-r1"):
            F("5-stale", row, pkg, "-", "WARN", "stale-r1 present (re-merge happened); verified current merged-1 sha vs reports above")
        # row-name reuse: merged older than resolution or reports of other pkg ?
        # EXTRA A: clustering with mixed anchors/categories; raw lookup
        for r in led["rows"]:
            cats, ancs, kinds = set(), set(), set()
            for m in r["members"]:
                blk = raw.get(m["reviewer_id"])
                if not blk:
                    continue
                f = next((x for x in blk if x["id"] == m["fid"]), None)
                if f:
                    cats.add(f.get("category")); ancs.add(f.get("anchor"))
            if len(r["members"]) >= 2 and len(ancs) >= 3 and len(ancs) > len({m["reviewer_id"] for m in r["members"]}) and False:
                pass
            # members from one reviewer that have different anchors AND mixed blocking -> blocking pulled by unrelated finding
            byrev = collections.defaultdict(list)
            for m in r["members"]:
                byrev[m["reviewer_id"]].append(m)
            for rid, ms in byrev.items():
                if len(ms) >= 2:
                    extra["row-with-multiple-same-reviewer-members"] += 1
                    extra_list["samerev"].append(f"{row}/{pkg[8:20]}/{r['lid']}/{rid}")
            if len(cats) >= 2:
                extra["row-mixed-categories"] += 1
                extra_list["mixcat"].append(f"{row}/{pkg[8:20]}/{r['lid']}:{sorted(c or '' for c in cats)}")
            bl = [m["blocking"] for m in r["members"]]
            if len(set(bl)) == 2:
                extra["row-mixed-blocking-members"] += 1
            # blocking row whose blocking members are all from one reviewer and row contains non-blocking from others (cluster hides)
            if r["blocking"] and not r["span"]:
                extra["blocking-row-no-span"] += 1
            if not r.get("span") or r.get("span") == [0, 0]:
                extra["row-without-span(anchor-unresolved?)"] += 1
                extra_list["nospan"].append(f"{row}/{pkg[8:20]}/{r['lid']}")
        # anchor warnings
        try:
            so = json.loads(open(f"{d}/merge-stdout.txt").read().split("\n", 1)[1])
            if so.get("warnings"):
                extra["merge-warnings"] += 1
                extra_list["warn"].append(f"{row}/{pkg[8:20]}:{so['warnings']}")
        except Exception:
            extra["merge-stdout-unparsed"] += 1
        # signature for cross-row reuse
        sigs[(pkg, sha(f"{d}/ledger.json"))].append(row)
        # merged older than resolution?
        rt = os.path.getmtime(f"{d}/resolution.json")
        if abs(rt - mt) > 600:
            extra["merged-vs-resolution-mtime-gap>10min"] += 1
            extra_list["mtimegap"].append(f"{row}/{pkg[8:20]}")
        # block order: reviewers in merged vs ledger equal
        if [x[0] for x in listed] != [r["reviewer_id"] for r in led["rounds"][-1]["reviewers"]]:
            extra["reviewer-order-differs-md-vs-ledger"] += 1
# identical ledgers across rows
for k, v in sigs.items():
    if len(v) > 1:
        extra["identical-ledger-sha-across-rows"] += 1
        extra_list["dupledger"].append(f"{k[0][8:20]}:{v}")

with open("/tmp/audit-D/flags.tsv", "w") as fh:
    fh.write("check\trow\tpackage\treviewer\tseverity\treason\n")
    for f in flags:
        fh.write("\t".join(f) + "\n")
print("merges", merges, "rows", len(rows))
for k, v in sorted(cnt.items()):
    print(k, v)
print("dropped stats per model (raw, kept, reviewers):")
for k, v in sorted(drop_by_model.items()):
    print(" ", k, v, "dropped", v[0]-v[1])
print(dict(extra))
for k, v in extra_list.items():
    print(k, len(v), v[:6])
json.dump({k: v for k, v in extra_list.items()}, open("/tmp/audit-D/extra.json", "w"), indent=1)
