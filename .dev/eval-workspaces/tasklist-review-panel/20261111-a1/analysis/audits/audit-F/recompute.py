import json, glob, os, re, hashlib, itertools, math, statistics as st, collections
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
PK = [DS, AL, DE]
SH = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "gpt-6-luna": "luna", "gpt-6.1-terra": "terra", "gpt-6.1-sol": "sol",
      "grok-4.7": "grok", "muse-wonder-1.0": "wonder", "muse-ember-1.0": "ember", "glm-5.3": "glm"}
BLK_GT = {}
for p in PK:
    g = json.load(open(f"{E}/{p}/ground-truth.json"))
    BLK_GT[p] = {i["id"] for i in g["items"] if i.get("blocking_in_implement")}
def valid(r):
    if any(x in r for x in ("contaminated", "superseded", "quarantine")): return False
    return (r.endswith("-src") or r.startswith("b4-") or r.endswith("-ember") or (r[:1] in "egh" and r[1:2].isdigit())
            or r in ("sol-alone-src", "terra-alone-src"))
rows = set(os.listdir(f"{E}/arms/scoring/combos"))
for p in PK:
    rows |= set(os.listdir(f"{E}/{p}/reviews/combos"))
rows = sorted(r for r in rows if valid(r))
flags = []  # (check,row,pkg,reviewer,sev,reason)
def flag(c, r, p, rv, s, why): flags.append((c, r, (p or "na").replace("TASK-WF-", ""), rv or "na", s, why))
R = {}
hashes = collections.defaultdict(list)
for row in rows:
    d = dict(row=row, pk={}, models={})
    complete = True
    for p in PK:
        sc = [f for f in glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json")]
        if len(sc) == 0:
            flag("3-completeness", row, p, None, "EXCLUDE", "no score.json for this package"); complete = False; continue
        if len(sc) > 1: flag("3-completeness", row, p, None, "WARN", f"{len(sc)} score.json files (re-judged?): {[os.path.basename(os.path.dirname(x)) for x in sc]}")
        s = json.load(open(sc[0]))
        if s.get("combo") != row or s.get("package") != p: flag("1-score", row, p, None, "EXCLUDE", f"score.json combo/package field mismatch: {s.get('combo')} {s.get('package')}")
        any_, blk = s["gt_covered_any"], s["gt_covered_blocking"]
        if len(set(any_)) != len(any_) or len(set(blk)) != len(blk): flag("6-pitfall-double-count", row, p, None, "WARN", f"duplicate GT id in score lists {any_} {blk}")
        if not set(any_) <= {i for i in [f"GT{k}" for k in range(1, 11)]}: flag("1-score", row, p, None, "WARN", f"unknown GT ids {any_}")
        if not set(blk) <= set(any_): flag("1-score", row, p, None, "WARN", f"gt_covered_blocking not subset of gt_covered_any: {blk} vs {any_}")
        exp_wb = s["ledger_rows_blocking"] - s["blocking_rows_gt_matched"]
        if exp_wb != s["wrong_blockers"]: flag("1-score", row, p, None, "WARN", f"wrong_blockers {s['wrong_blockers']} != ledger_rows_blocking-blocking_rows_gt_matched {exp_wb}")
        blk_true = [g for g in blk if g in BLK_GT[p]]
        any_true = [g for g in any_ if g in BLK_GT[p]]
        # reviewers
        metas = [f for f in glob.glob(f"{E}/{p}/reviews/combos/{row}/*.meta.json") if "attempt" not in f]
        costs = [f for f in glob.glob(f"{E}/{p}/reviews/combos/{row}/*.cost.json") if "attempt" not in f]
        mids = sorted(os.path.basename(f).split(".")[0] for f in metas); cids = sorted(os.path.basename(f).split(".")[0] for f in costs)
        if mids != cids: flag("3-completeness", row, p, None, "EXCLUDE", f"meta reviewers {mids} != cost reviewers {cids}")
        cj = {os.path.basename(f).split(".")[0]: json.load(open(f)) for f in costs}
        tok = sum(c["total_output_tokens_all"] for c in cj.values()); ws = sum(c["total_wall_s"] for c in cj.values()); mx = max(c["total_wall_s"] for c in cj.values()) if cj else 0
        ms = []
        for f in metas:
            m = json.load(open(f)); rid = os.path.basename(f).split(".")[0]; ms.append(SH.get(m["expected_model"], m["expected_model"]))
            if m["observed_model"] == "grok-4.7-build" and m["expected_model"] == "grok-4.7": pass  # grok gateway id, seen in all grok runs
            elif not m.get("model_ok") or m["observed_model"] != m["expected_model"]: flag("3-completeness", row, p, rid, "EXCLUDE", f"model_ok={m.get('model_ok')} observed={m['observed_model']} expected={m['expected_model']}")
            if not m.get("findings_block"): flag("3-completeness", row, p, rid, "WARN", "no findings block")
            if m.get("attempt", 1) > 1 or cj.get(rid, {}).get("attempts", 1) > 1:
                if cj[rid]["total_output_tokens_all"] != m.get("output_tokens_all"): flag("6-pitfall-retry-cost", row, p, rid, "WARN", f"cost counts {cj[rid]['attempts']} attempts: total_tokens_all {cj[rid]['total_output_tokens_all']} vs final-attempt meta {m.get('output_tokens_all')}")
            mdf = f.replace(".meta.json", ".md")
            if os.path.exists(mdf): hashes[hashlib.md5(open(mdf, "rb").read()).hexdigest()].append((row, p, rid))
        d["models"][p] = tuple(sorted(ms))
        d["pk"][p] = dict(any=len(any_), blk=len(blk), wb=s["wrong_blockers"], tok=tok, ws=ws, mx=mx, blk_true=len(blk_true), any_true=len(any_true), anyids=any_, blkids=blk, n=len(cj))
    if len({v for v in d["models"].values()}) > 1: flag("2-family", row, None, None, "EXCLUDE", f"model multiset differs across packages: {d['models']}")
    d["complete"] = complete and len(d["pk"]) == 3
    d["ms"] = next(iter(d["models"].values()), ())
    R[row] = d
for h, L in hashes.items():
    if len({x[0] for x in L}) > 1 and len(L) > 1: flag("6-pitfall-dup-output", ",".join(sorted({x[0] for x in L})), L[0][1], L[0][2], "WARN", f"identical reviewer output md5 in {len(L)} places: {L[:4]}")
def agg(r):
    if not r["complete"]: return None
    pk = r["pk"]; a = sum(pk[p]["any"] for p in (DS, AL)); b = sum(pk[p]["blk"] for p in (DS, AL)); w = sum(pk[p]["wb"] for p in (DS, AL))
    return dict(any=a, blk=b, wb=w, cany=pk[DE]["any"], cblk=pk[DE]["blk"], cwb=pk[DE]["wb"], tok=sum(pk[p]["tok"] for p in PK), rs=sum(pk[p]["ws"] for p in PK), el=sum(pk[p]["mx"] for p in PK),
                blk_true=sum(pk[p]["blk_true"] for p in (DS, AL)), any_true=sum(pk[p]["any_true"] for p in (DS, AL)))
M = {k: agg(v) for k, v in R.items()}
with open("/tmp/audit-F/recomputed.tsv", "w") as f:
    f.write("row\tmodels\tcomplete\tDR_found\tDR_blocking\tDR_wrong_blockers\tctl_found\tctl_blocking\tctl_wrong_blockers\ttokens\treviewer_s_sum\telapsed_s\tDR_blk_GTs_caught_any_row(true8)\tDR_blk_GTs_caught_by_blocking_row\n")
    for k, v in R.items():
        m = M[k]
        if m is None: f.write(f"{k}\t{'+'.join(v['ms'])}\tNO\t\t\t\t\t\t\t\t\t\t\t\n"); continue
        f.write(f"{k}\t{'+'.join(v['ms'])}\tYES\t{m['any']}\t{m['blk']}\t{m['wb']}\t{m['cany']}\t{m['cblk']}\t{m['cwb']}\t{m['tok']}\t{m['rs']}\t{m['el']}\t{m['any_true']}\t{m['blk_true']}\n")
json.dump({k: dict(R[k], models={p: list(x) for p, x in R[k]["models"].items()}, m=M[k]) for k in R}, open("/tmp/audit-F/rows.json", "w"), default=list)
# ---- report comparison
rep = open(f"{E}/COMBO-REPORT.md").read().split("\n")
def cells(line): return [c.strip().replace("**", "") for c in line.strip().strip("|").split("|")]
def ints(s): return [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", s)]
def cmp(section, lo, hi, kind):
    for i in range(lo - 1, hi):
        c = cells(rep[i]); row = c[0]
        if row not in R or M.get(row) is None:
            if row in R: flag("1-mismatch", row, None, None, "WARN", f"{section}: row in report but not complete in eval")
            continue
        m = M[row]
        if kind == "b45":   # Row|Models|any|blk|wb|ctl any/blk, |wbctl|tok|wall
            v = dict(any=ints(c[2])[0], blk=ints(c[3])[0], wb=ints(c[4])[0], cany=ints(c[5])[0], cblk=ints(c[5])[2], cwb=ints(c[6])[0], tok=ints(c[7])[0], wall=ints(c[8])[0])
        else:               # b6: Row|vs|any|blk|wb|ctl "2/2, 2 blk, 0 wb"|tok|wall
            ci = ints(c[5]); v = dict(any=ints(c[2])[0], blk=ints(c[3])[0], wb=ints(c[4])[0], cany=ci[0], cblk=ci[2], cwb=(ci[3] if len(ci) > 3 else M[row]["cwb"]), tok=ints(c[6])[0], wall=ints(c[7])[0])
        if kind == "b6": pass
        for key in ("any", "blk", "wb", "cany", "cblk", "cwb", "tok"):
            if v[key] != m[key]: flag("1-mismatch", row, None, None, "WARN", f"{section} line {i+1} col {key}: report {v[key]} vs recomputed {m[key]}")
        if v["wall"] not in (m["rs"], m["el"]): flag("1-mismatch", row, None, None, "WARN", f"{section} line {i+1} wall: report {v['wall']} vs reviewer-s {m['rs']} / elapsed {m['el']}")
        elif v["wall"] != m["rs"]: flag("1-mismatch", row, None, None, "WARN", f"{section} line {i+1} wall {v['wall']} equals elapsed, not reviewer-s sum {m['rs']}")
cmp("batch4/5", 114, 129, "b45"); cmp("batch6", 155, 160, "b6"); cmp("batch7", 181, 185, "b45")
def tomulti(cell):
    out = []
    for t in cell.split(","):
        t = t.strip(); n = 2 if t.endswith(" x2") else 1; t = t.replace(" x2", "")
        out += [t] * n
    return out
for lo, hi in ((114, 129), (181, 185)):
    for i in range(lo - 1, hi):
        c = cells(rep[i]); row = c[0]
        if row not in R: continue
        want = tomulti(c[1]); got = list(R[row]["ms"])
        if "muse" in want:
            want = [("wonder" if "wonder" in got and "ember" not in got else "ember") if w == "muse" else w for w in want]
        if sorted(want) != sorted(got): flag("2-family", row, None, None, "WARN", f"report line {i+1} Models '{c[1]}' vs meta models {got}")
# attempts>1 in valid rows
for row in R:
    for p in PK:
        for f in glob.glob(f"{E}/{p}/reviews/combos/{row}/*.cost.json"):
            if "attempt" in f: continue
            c = json.load(open(f))
            if c["attempts"] > 1: flag("6-pitfall-retry-cost", row, p, os.path.basename(f).split(".")[0], "WARN", f"cost.json attempts={c['attempts']} tokens_all={c['total_output_tokens_all']} wall={c['total_wall_s']} (retries counted in tokens/wall)")
# ---- families
def fam_rows(n, k=4): return [f"{n}-r{i}" for i in range(1, k + 1)]
FAM = [("ember + luna", ("ember", "luna"), fam_rows("g9-ember-luna")),
 ("ember + 2x luna", ("ember", "luna", "luna"), fam_rows("g1-ember-luna2") + ["b4-muse-ember-luna2", "e2-ember-luna2-rep"]),
 ("2x ember + luna", ("ember", "ember", "luna"), fam_rows("g5-ember2-luna") + ["e3-ember2-luna"]),
 ("2x luna + 2x ember", ("ember", "ember", "luna", "luna"), fam_rows("g6-luna2-ember2")),
 ("ember + terra", ("ember", "terra"), fam_rows("g8-ember-terra")),
 ("sonnet + ember", ("ember", "sonnet"), fam_rows("g2-sonnet-ember")),
 ("sonnet + luna + ember", ("ember", "luna", "sonnet"), fam_rows("g3-sonnet-luna-ember") + ["n5-sonnet-ember"]),
 ("haiku + ember + terra", ("ember", "haiku", "terra"), fam_rows("g4-haiku-ember-terra") + ["terra-muse-haiku-ember"]),
 ("haiku + 2x luna", ("haiku", "luna", "luna"), fam_rows("g7-haiku-luna2") + ["r1-haiku-luna2-src"]),
 ("ref grok+ember+luna", ("ember", "grok", "luna"), ["e1-grok-ember-luna"]),
 ("ref haiku+ember+luna", ("ember", "haiku", "luna"), ["e5-haiku-ember-luna"]),
 ("ref haiku+2x ember", ("ember", "ember", "haiku"), ["e6-haiku-ember2"]),
 ("h1 haiku+2luna+2ember", ("ember", "ember", "haiku", "luna", "luna"), fam_rows("h1-haiku-luna2-ember2")),
 ("h2 sonnet+2luna+2ember", ("ember", "ember", "luna", "luna", "sonnet"), fam_rows("h2-sonnet-luna2-ember2"))]
for lab, ms, rs in FAM:
    for r in rs:
        if r not in R: flag("2-family", r, None, None, "EXCLUDE", f"family '{lab}': row dir not found"); continue
        if R[r]["ms"] != ms: flag("2-family", r, None, None, "EXCLUDE", f"family '{lab}' expects {ms} but meta models are {R[r]['ms']}")
        if M[r] is None: flag("3-completeness", r, None, None, "EXCLUDE", f"family '{lab}': row incomplete")
def fs(rs, k): return [M[r][k] for r in rs if M.get(r)]
FS = {}
for lab, ms, rs in FAM:
    FS[lab] = {k: fs(rs, k) for k in ("any", "blk", "wb", "cany", "cwb", "tok", "rs", "el")}
json.dump(FS, open("/tmp/audit-F/fam.json", "w"))
# printed family means for compare
def sd(x): return st.stdev(x) if len(x) > 1 else float("nan")
out = ["family\tn\tDR_mean\tmin-max\tsd\tblk_mean\tblk_minmax\tblk_sd\twb_mean\tctl_mean\tctl_sd\ttok_mean\trs_mean\tel_mean\tDRtrue-blk-GT mean"]
for lab, ms, rs in FAM:
    x = FS[lab]; n = len(x["any"])
    if not n: continue
    bt = [M[r]["blk_true"] for r in rs if M.get(r)]
    out.append(f"{lab}\t{n}\t{st.mean(x['any']):.2f}\t{min(x['any'])}-{max(x['any'])}\t{sd(x['any']):.2f}\t{st.mean(x['blk']):.2f}\t{min(x['blk'])}-{max(x['blk'])}\t{sd(x['blk']):.2f}\t{st.mean(x['wb']):.2f}\t{st.mean(x['cany']):.2f}\t{sd(x['cany']):.2f}\t{st.mean(x['tok']):,.0f}\t{st.mean(x['rs']):,.0f}\t{st.mean(x['el']):,.0f}\t{st.mean(bt):.2f}")
open("/tmp/audit-F/fam.tsv", "w").write("\n".join(out) + "\n")
# ---- stats: Welch + permutation
def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    def cf(a, b, x):
        tiny = 1e-30; qab = a + b; qap = a + 1; qam = a - 1; c = 1.0; d = 1 - qab * x / qap
        d = tiny if abs(d) < tiny else d; d = 1 / d; h = d
        for m in range(1, 300):
            m2 = 2 * m; aa = m * (b - m) * x / ((qam + m2) * (a + m2)); d = 1 + aa * d; d = tiny if abs(d) < tiny else d
            c = 1 + aa / c; c = tiny if abs(c) < tiny else c; d = 1 / d; h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2)); d = 1 + aa * d; d = tiny if abs(d) < tiny else d
            c = 1 + aa / c; c = tiny if abs(c) < tiny else c; d = 1 / d; de = d * c; h *= de
            if abs(de - 1) < 1e-12: break
        return h
    if x < (a + 1) / (a + b + 2): return math.exp(lbeta) * cf(a, b, x) / a
    return 1 - math.exp(lbeta) * cf(b, a, 1 - x) / b
def welch(a, b):
    ma, mb = st.mean(a), st.mean(b); va, vb = st.variance(a) / len(a), st.variance(b) / len(b)
    if va + vb == 0: return float("nan"), float("nan")
    t = (ma - mb) / math.sqrt(va + vb); df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    p = betai(df / 2, 0.5, df / (df + t * t)); return t, p
def perm(a, b):
    allv = a + b; n = len(a); obs = abs(st.mean(a) - st.mean(b)); cnt = tot = 0
    for idx in itertools.combinations(range(len(allv)), n):
        s = set(idx); x = [allv[i] for i in idx]; y = [allv[i] for i in range(len(allv)) if i not in s]
        tot += 1; cnt += abs(st.mean(x) - st.mean(y)) >= obs - 1e-12
    return cnt / tot
CMP = [("ember+2x luna vs ember+luna", "ember + 2x luna", "ember + luna"), ("2x ember+luna vs ember+luna", "2x ember + luna", "ember + luna"), ("2x luna+2x ember vs ember+luna", "2x luna + 2x ember", "ember + luna"),
       ("2x luna+2x ember vs ember+2x luna", "2x luna + 2x ember", "ember + 2x luna"), ("2x luna+2x ember vs 2x ember+luna", "2x luna + 2x ember", "2x ember + luna"),
       ("h1 vs g6 (adding haiku)", "h1 haiku+2luna+2ember", "2x luna + 2x ember"), ("h2 vs g6 (adding sonnet)", "h2 sonnet+2luna+2ember", "2x luna + 2x ember"),
       ("h2 vs sonnet+luna+ember", "h2 sonnet+2luna+2ember", "sonnet + luna + ember"), ("h2 vs sonnet+ember", "h2 sonnet+2luna+2ember", "sonnet + ember"),
       ("h1 vs haiku+2x luna", "h1 haiku+2luna+2ember", "haiku + 2x luna"), ("ember+terra vs ember+luna", "ember + terra", "ember + luna"), ("sonnet+ember vs ember+luna", "sonnet + ember", "ember + luna")]
res = ["comparison\tmetric\tn1\tn2\tdelta\tse_rule(|d|>=2se)\tWelch_t\tWelch_p\tperm_p"]
for lab, A, B in CMP:
    for k, kn in (("any", "DR found"), ("blk", "DR blocking"), ("cany", "ctl found"), ("wb", "DR wrong blockers")):
        a, b = FS[A][k], FS[B][k]
        d = st.mean(a) - st.mean(b); se = math.sqrt(sd(a) ** 2 / len(a) + sd(b) ** 2 / len(b))
        t, p = welch(a, b)
        res.append(f"{lab}\t{kn}\t{len(a)}\t{len(b)}\t{d:+.2f}\t{'beyond' if abs(d) >= 2 * se else 'within'}\t{t:.2f}\t{p:.3f}\t{perm(a, b):.3f}")
open("/tmp/audit-F/stats.tsv", "w").write("\n".join(res) + "\n")
# ---- presence stats / ceiling (check untried claims)
comp = [r for r in R if M[r]]
cnt = collections.Counter(M[r]["any"] for r in comp)
pres = ["valid-era complete rows: %d, distinct multisets %d; DR any distribution %s" % (len(comp), len({R[r]["ms"] for r in comp}), sorted(cnt.items()))]
for m in ("sonnet", "haiku", "grok", "luna", "terra", "sol", "ember", "wonder"):
    w = [r for r in comp if m in R[r]["ms"]]; wo = [r for r in comp if m not in R[r]["ms"]]
    f = lambda L, k: st.mean(M[r][k] for r in L) if L else float("nan")
    pres.append(f"{m}: with n={len(w)} any={f(w,'any'):.2f} blk={f(w,'blk'):.2f} wb={f(w,'wb'):.2f} | without n={len(wo)} any={f(wo,'any'):.2f} blk={f(wo,'blk'):.2f} wb={f(wo,'wb'):.2f}")
# per-GT catch counts by package (alias GT vs ds GT)
gtc = collections.Counter()
for r in comp:
    for p in (DS, AL):
        for g in R[r]["pk"][p]["anyids"]: gtc[(p[8:14], g)] += 1
pres.append("GT catch counts by package: " + str(sorted(gtc.items())))
# blocking semantics
nb = sum(M[r]["blk"] for r in comp); nbt = sum(M[r]["blk_true"] for r in comp); nat = sum(M[r]["any_true"] for r in comp)
pres.append(f"sum over valid complete rows: judge gt_covered_blocking = {nb}; of which GT truly blocking_in_implement = {nbt}; true-blocking GTs caught by ANY ledger row = {nat}")
pres.append("rows where judge blocking count > true-blocking-GT count: " + str([(r, M[r]['blk'], M[r]['blk_true']) for r in comp if M[r]['blk'] != M[r]['blk_true']][:80]))
pres.append("max DR blk judge: %s ; max DR blk_true: %s" % (max(M[r]["blk"] for r in comp), max(M[r]["blk_true"] for r in comp)))
open("/tmp/audit-F/presence.txt", "w").write("\n".join(pres) + "\n")
with open("/tmp/audit-F/flags.tsv", "w") as f:
    f.write("check\trow\tpackage\treviewer(na)\tseverity(EXCLUDE|WARN)\treason\n")
    for x in flags: f.write("\t".join(x) + "\n")
print(len(rows), "rows", len(flags), "flags")
