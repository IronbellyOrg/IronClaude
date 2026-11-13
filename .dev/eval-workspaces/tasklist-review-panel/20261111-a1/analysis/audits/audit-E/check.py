import json, os, re, sys, glob, hashlib
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
S = E + "/arms/scoring/combos"
flags = []
def flag(check, row, pkg, sev, reason):
    flags.append((check, row, pkg, "na", sev, reason))
gts = {}
cand_sha = {}
for p in os.listdir(E):
    g = f"{E}/{p}/ground-truth.json"
    if os.path.exists(g):
        gts[p] = {i["id"]: i for i in json.load(open(g))["items"]}
        cand_sha[p] = hashlib.sha256(open(f"{E}/{p}/candidate.md", "rb").read()).hexdigest()
LEAK = re.compile(r"\b(grok|luna\d?|ember\d?|muse|wonder)\b|\bt[1-4][ab]?-\d\b|reviews/combos|\.catfix|/combos/", re.I)
def ledger(path):
    rows = []
    try:
        txt = open(path).read()
    except Exception:
        return None
    m = re.search(r"## Ledger\n(.*?)(\n## |\Z)", txt, re.S)
    if not m: return []
    for ln in m.group(1).splitlines():
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if re.fullmatch(r"L\d+", c[0] if c else ""):
            rows.append(tuple(c[:6]))
    return rows
def notes_gt(notes):
    cov, unc = set(), set()
    for s in re.split(r"(?<=[.;])\s+", notes):
        ids = set(re.findall(r"GT\d+", s))
        # expand ranges like GT1-GT3 ignored
        neg = re.search(r"uncovered|not covered|no GT|match(es)? no|matches none|unmatched|not matched|miss|none of|no ground|no GT item|not in GT|doesn't match|does not match|no match", s, re.I)
        (unc if neg else cov).update(ids)
    return cov, unc
stats = []
rowsinfo = []
for rowdir in sorted(glob.glob(S + "/*/*")):
    pkg = os.path.basename(rowdir); row = os.path.basename(os.path.dirname(rowdir))
    if not os.path.isdir(rowdir): continue
    if re.search(r"contaminated|superseded|quarantine|^i1-|^i2-", row): continue
    labdirs = [d for d in os.listdir(rowdir) if os.path.isdir(f"{rowdir}/{d}")]
    if len(labdirs) != 1:
        flag("1.labeldirs", row, pkg, "EXCLUDE", f"{len(labdirs)} label dirs: {labdirs}");
    try: key = json.load(open(rowdir + "/label-key.json"))
    except Exception as e:
        flag("1.labelkey", row, pkg, "EXCLUDE", f"label-key unreadable {e}"); continue
    for lab in labdirs:
        D = f"{rowdir}/{lab}"
        sp = D + "/score.json"
        if not os.path.exists(sp):
            flag("1.noscore", row, pkg, "WARN", f"no score.json in {lab}"); continue
        if key.get("label") != lab: flag("1.labelmatch", row, pkg, "EXCLUDE", f"label-key {key.get('label')} != dir {lab}")
        if key.get("combo") != row: flag("1.labelkeycombo", row, pkg, "EXCLUDE", f"label-key combo {key.get('combo')}")
        try: sc = json.load(open(sp))
        except Exception as e:
            flag("1.scorejson", row, pkg, "EXCLUDE", f"score.json invalid: {e}"); continue
        # judge.json
        jj = None
        try:
            jj = json.load(open(D + "/judge.json"))
        except Exception as e:
            flag("1.judgejson", row, pkg, "EXCLUDE", f"judge.json unparseable: {e}")
        reads = []
        if jj is not None:
            res = [x for x in jj if isinstance(x, dict) and x.get("type") == "result"] if isinstance(jj, list) else [jj]
            if not res: flag("1.judgeresult", row, pkg, "EXCLUDE", "no result object in judge.json")
            else:
                r = res[-1]
                rs = str(r.get("result", ""))
                if "API Error" in rs or r.get("is_error"): flag("1.apierror", row, pkg, "EXCLUDE", f"is_error={r.get('is_error')} result={rs[:120]!r}")
                if r.get("subtype") != "success": flag("1.subtype", row, pkg, "EXCLUDE", f"subtype {r.get('subtype')}")
            if isinstance(jj, list):
                for x in jj:
                    if x.get("type") == "assistant":
                        for b in x.get("message", {}).get("content", []):
                            if isinstance(b, dict) and b.get("type") == "tool_use":
                                inp = b.get("input", {})
                                reads.append((b.get("name"), inp.get("file_path") or inp.get("command") or ""))
                # did the judge itself write score.json?
                if not any(n == "Write" and str(a).endswith("score.json") for n, a in reads) and not any(n == "Bash" and "score.json" in str(a) for n, a in reads):
                    flag("1.judgewrote", row, pkg, "EXCLUDE", "no tool call writing score.json in judge.json (possible fabricated)")
                for n, a in reads:
                    if n == "Read" and not (a.startswith(D) or a.startswith(f"{E}/{pkg}/") ):
                        flag("1.judgeread", row, pkg, "WARN", f"judge Read outside brief: {a}")
        err = os.path.getsize(D + "/judge.err") if os.path.exists(D + "/judge.err") else -1
        if err != 0: flag("1.judgeerr", row, pkg, "WARN", f"judge.err size {err}")
        if sc.get("combo") != row: flag("1.combo", row, pkg, "EXCLUDE", f"score combo {sc.get('combo')}")
        if sc.get("package") != pkg: flag("1.package", row, pkg, "EXCLUDE", f"score package {sc.get('package')}")
        if sc.get("label") != lab: flag("1.scorelabel", row, pkg, "EXCLUDE", f"score label {sc.get('label')}")
        # 2 schema
        gt = gts[pkg]
        need = ["label","combo","package","gt_total","gt_covered_any","gt_covered_blocking","ledger_rows_total","ledger_rows_blocking","blocking_rows_gt_matched","wrong_blockers","notes"]
        miss = [k for k in need if k not in sc]
        if miss: flag("2.schema", row, pkg, "EXCLUDE", f"missing keys {miss}"); continue
        ca, cb = set(sc["gt_covered_any"]), set(sc["gt_covered_blocking"])
        if sc["gt_total"] != len(gt): flag("2.gttotal", row, pkg, "EXCLUDE", f"gt_total {sc['gt_total']} != {len(gt)}")
        if not ca <= set(gt): flag("2.gtids", row, pkg, "EXCLUDE", f"covered ids not in GT: {ca-set(gt)}")
        if not cb <= ca: flag("2.subset", row, pkg, "EXCLUDE", f"blocking not subset of any: {cb-ca}")
        if len(sc["gt_covered_any"]) != len(ca): flag("2.dups", row, pkg, "WARN", "duplicate ids in gt_covered_any")
        mf = D + "/merged-anon.md"; m1 = f"{E}/combos/{row}/{pkg}/merged-1.md"
        qsrc = False
        if not os.path.exists(m1):
            q = f"{E}/quarantine-pre-src-luna/_combos/{row}/{pkg}/merged-1.md"
            if os.path.exists(q): m1 = q; qsrc = True
        if qsrc: flag("4.quarantined_source", row, pkg, "EXCLUDE", "merged-1.md only exists under quarantine-pre-src-luna (row superseded by -src variant)")
        la = ledger(mf); l1 = ledger(m1)
        if la is None: flag("2.noanon", row, pkg, "EXCLUDE", "merged-anon.md missing")
        if l1 is None: flag("2.nomerged", row, pkg, "EXCLUDE", "merged-1.md missing")
        if la is not None:
            tot = len(la); blk = sum(1 for r in la if r[2].lower() == "yes")
            if sc["ledger_rows_total"] != tot: flag("2.rowstotal", row, pkg, "EXCLUDE", f"ledger_rows_total {sc['ledger_rows_total']} != anon table {tot}")
            if sc["ledger_rows_blocking"] != blk: flag("2.rowsblock", row, pkg, "EXCLUDE", f"ledger_rows_blocking {sc['ledger_rows_blocking']} != anon table {blk}")
            if l1 is not None:
                a = [r[:5] for r in la]; b = [r[:5] for r in l1]
                if a != b: flag("3.anonledger", row, pkg, "EXCLUDE", "anon ledger rows differ from merged-1 ledger (lid..severity)")
        if sc["wrong_blockers"] > sc["ledger_rows_blocking"]: flag("2.wrong>blk", row, pkg, "EXCLUDE", "wrong_blockers > ledger_rows_blocking")
        if sc["blocking_rows_gt_matched"] + sc["wrong_blockers"] != sc["ledger_rows_blocking"]:
            flag("2.sum", row, pkg, "WARN", f"matched {sc['blocking_rows_gt_matched']} + wrong {sc['wrong_blockers']} != blocking rows {sc['ledger_rows_blocking']}")
        if sc["blocking_rows_gt_matched"] < len(cb) and sc["blocking_rows_gt_matched"] < 1 and cb:
            flag("2.matched<cb", row, pkg, "WARN", "covered_blocking nonempty but matched rows 0")
        if cb and sc["ledger_rows_blocking"] == 0: flag("2.cbnoblock", row, pkg, "EXCLUDE", "gt_covered_blocking nonempty but 0 blocking rows")
        if sc["blocking_rows_gt_matched"] > 0 and not cb: flag("2.matchednocb", row, pkg, "WARN", "matched rows >0 but gt_covered_blocking empty")
        if len(cb) > sc["blocking_rows_gt_matched"] and sc["blocking_rows_gt_matched"] >= 0 and len(cb) > sc["ledger_rows_blocking"] * 3:
            pass
        cov, unc = notes_gt(sc["notes"])
        allm = cov | unc
        bad_cov = cov - ca - unc
        if bad_cov: flag("2.notes", row, pkg, "WARN", f"notes mention {sorted(bad_cov)} as covered but not in gt_covered_any")
        miss_n = ca - allm
        if ca and miss_n and len(ca) >= 1 and not allm & ca: flag("2.notes2", row, pkg, "WARN", f"covered {sorted(miss_n)} not named in notes")
        if unc & ca and not (cov & ca >= unc & ca): flag("2.notes3", row, pkg, "WARN", f"notes list {sorted(unc & ca)} as uncovered but arrays say covered")
        # 3 leaks
        if la is not None:
            lines = open(mf).read().splitlines()
            hits = [(i + 1, l.strip()[:110]) for i, l in enumerate(lines) if LEAK.search(re.sub(r"claude-gw-tier\w*|claude-gw\w*", "", l))]
            hdr = [h for h in hits]
            if hits: flag("3.leak", row, pkg, "WARN", f"{len(hits)} lines match leak regex; first: L{hits[0][0]} {hits[0][1]!r}")
            txt = "\n".join(lines)
            if E in txt or "eval-tasklist-review-panel" in txt or "/combos/" in txt: flag("3.pathleak", row, pkg, "WARN", "eval path fragment in anon file")
            m = re.search(r"sha256 ([0-9a-f]{64})", txt)
            if m and m.group(1) != cand_sha[pkg]: flag("3.candsha", row, pkg, "EXCLUDE", f"candidate sha {m.group(1)[:12]} != package candidate {cand_sha[pkg][:12]}")
            if not m: flag("3.nosha", row, pkg, "WARN", "no candidate sha in anon file")
        if l1 is not None:
            t1 = open(m1).read()
            mm = re.search(r"candidate: (\S+)", t1)
            if mm and f"{pkg}/" not in mm.group(1): flag("3.mergedpkg", row, pkg, "EXCLUDE", f"merged-1 candidate path {mm.group(1)}")
        # mtimes
        ts, tm, ta = os.path.getmtime(sp), (os.path.getmtime(m1) if os.path.exists(m1) else 0), (os.path.getmtime(mf) if os.path.exists(mf) else 0)
        if ts < tm: flag("4.stale_vs_merged1", row, pkg, "EXCLUDE", f"score.json older than merged-1.md by {tm-ts:.0f}s")
        if ts < ta: flag("4.stale_vs_anon", row, pkg, "EXCLUDE", f"score.json older than merged-anon.md by {ta-ts:.0f}s")
        if ta < tm: flag("4.anon_vs_merged1", row, pkg, "EXCLUDE", f"merged-anon.md older than merged-1.md by {tm-ta:.0f}s")
        rowsinfo.append(dict(row=row, pkg=pkg, lab=lab, any=len(ca), cb=len(cb), blk=sc["ledger_rows_blocking"], tot=sc["ledger_rows_total"], wrong=sc["wrong_blockers"], ms=ts, mm=tm, ma=ta))
json.dump(rowsinfo, open("/tmp/audit-E/rows.json", "w"))
with open("/tmp/audit-E/flags.tsv", "w") as f:
    f.write("check\trow\tpackage\treviewer(na)\tseverity(EXCLUDE|WARN)\treason\n")
    for x in flags: f.write("\t".join(x) + "\n")
from collections import Counter
print(len(rowsinfo), "scores checked;", len(flags), "flags")
print(Counter((x[0], x[4]) for x in flags))
