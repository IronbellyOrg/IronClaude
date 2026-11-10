"""O3: offline falsification of the capture-recapture stop rule on the 12 (+3) first reviews of the original spec.
Run with: uv run --project $CLONE python falsify.py   (imports the product estimator)."""
import collections
import difflib
import itertools
import json
import math
import random
import statistics
import subprocess
import sys
import tempfile
import common as c
from superclaude.cli.review import estimate as E

CAT = json.load(open(c.CAT / "catalog.json"))
MECH = json.load(open(c.AB / "offline/mech_clusters.json"))
PRIMARY = c.RUN_NAMES
ALL15 = c.ARM1 + c.RUN_NAMES


def matrix(cat_clusters, occasions, srcstep="R1"):
    """defect -> frozenset of occasions (runs) whose <run>/R1 reported it."""
    rows = {}
    for cl in cat_clusters:
        s = {m["source"].split("/")[0] for m in cl["members"] if m["source"].endswith("/" + srcstep)}
        rows[cl["cid"]] = frozenset(s & set(occasions))
    return rows


def est_subset(rows, subset):
    sub = set(subset)
    return E.estimate_matrix([r & sub for r in rows.values()], len(subset))


def capture_json(rows, occasions, path):
    obj = {"schema": "review-capture/1", "source": "defect-catalog/1", "round": 1, "doc_sha256": c.SPEC_SHA,
           "occasions": list(occasions),
           "defects": [{"key": k, "blocking": True, "captured_by": sorted(v)} for k, v in rows.items()]}
    json.dump(obj, open(path, "w"))
    return obj


def subsets(k, rng_seed=None):
    allc = list(itertools.combinations(PRIMARY, k))
    if len(allc) <= 500:
        return allc
    return random.Random(k).sample(allc, 500)


def f1(rows, s_ref, label):
    out = {}
    for k in (2, 3, 4, 6):
        ss = subsets(k)
        obs, ch, jk, jk2, cp = [], [], [], [], []
        cov = collections.Counter()
        for sub in ss:
            r = est_subset(rows, sub)
            obs.append(abs(r["S_obs"] - s_ref))
            ch.append(abs(r["chao2"]["N"] - s_ref))
            jk.append(abs(r["jackknife1"]["N"] - s_ref))
            jk2.append(abs(r["jackknife2"]["N"] - s_ref))
            cov["chao2"] += r["chao2"]["ci95"][0] <= s_ref <= r["chao2"]["ci95"][1]
            cov["jack1"] += r["jackknife1"]["ci95"][0] <= s_ref <= r["jackknife1"]["ci95"][1]
            if r["chapman"]:
                cp.append(abs(r["chapman"]["N"] - s_ref))
                cov["chapman"] += r["chapman"]["ci95"][0] <= s_ref <= r["chapman"]["ci95"][1]
        n = len(ss)
        out[k] = dict(n=n, MAE_obs=statistics.mean(obs), MAE_chao2=statistics.mean(ch), COVER_chao2=cov["chao2"] / n,
                      MAE_jack1=statistics.mean(jk), COVER_jack1=cov["jack1"] / n, MAE_jack2=statistics.mean(jk2),
                      MAE_chapman=statistics.mean(cp) if cp else None,
                      COVER_chapman=cov["chapman"] / n if cp else None,
                      mean_S_obs=statistics.mean(E.estimate_matrix([r & set(s) for r in rows.values()], k)["S_obs"] for s in ss))
    return out


def verdict(t):
    m = t[4]
    def bad(mae, cov):
        return mae >= m["MAE_obs"] or cov < 0.5
    if bad(m["MAE_chao2"], m["COVER_chao2"]) and bad(m["MAE_jack1"], m["COVER_jack1"]):
        return "FALSIFIED"
    for mae, cov in ((m["MAE_chao2"], m["COVER_chao2"]), (m["MAE_jack1"], m["COVER_jack1"])):
        if mae <= 0.7 * m["MAE_obs"] and cov >= 0.7:
            return "SUPPORTED"
    return "WEAK"


def table(t, ref_name):
    lines = [f"| k | subsets | mean S_obs | MAE_obs | Chao2 MAE | Chao2 COVER | Jack1 MAE | Jack1 COVER | Jack2 MAE | Chapman MAE | Chapman COVER |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in t.items():
        f = lambda x: "-" if x is None else f"{x:.2f}"
        lines.append(f"| {k} | {v['n']} | {v['mean_S_obs']:.2f} | {v['MAE_obs']:.2f} | {v['MAE_chao2']:.2f} | {v['COVER_chao2']:.2f} | {v['MAE_jack1']:.2f} | {v['COVER_jack1']:.2f} | {v['MAE_jack2']:.2f} | {f(v['MAE_chapman'])} | {f(v['COVER_chapman'])} |")
    return "\n".join(lines)


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for t in range(i, j + 1):
                r[order[t]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    sx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    sy = math.sqrt(sum((b - my) ** 2 for b in ry))
    if sx == 0 or sy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / (sx * sy)


# ---- C5 span mapping across the revision chain
def map_span(span, old, new):
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    touched = False
    mp = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mp[i1 + k] = j1 + k
        else:
            for k in range(i1, i2):
                mp[k] = j1
            if i1 == i2:
                touched |= span[0] <= i1 <= span[1]
            else:
                touched |= i1 < span[1] and span[0] < i2
    s, e = span
    ns = mp.get(s, mp.get(s - 1, 0))
    ne = mp.get(e - 1, ns) + 1
    return touched, (ns, max(ne, ns + 1))


def fixed_clusters(run):
    hist = c.RUNS / run / "ws" / c.D / "specs/history"
    vs = sorted(hist.glob("spec-v*.md")) if hist.exists() else []
    chain = [p.read_text().split("\n") for p in vs] + [c.final_spec(run).read_text().split("\n")]
    if not vs:
        return set()
    assert vs[0].read_bytes() == c.ORIG.read_bytes(), run
    fixed = set()
    for cl in CAT["clusters"]:
        if not any(m["source"] == f"{run}/R1" for m in cl["members"]):
            continue
        span = tuple(cl["orig_span"])
        for old, new in zip(chain, chain[1:]):
            t, span = map_span(span, old, new)
            if t:
                fixed.add(cl["cid"])
                break
    return fixed


def f2(rows):
    res = []
    for run in PRIMARY:
        others = [o for o in PRIMARY if o != run]
        r = est_subset(rows, others)
        fx = fixed_clusters(run)
        n_r1 = [cl["cid"] for cl in CAT["clusters"] if any(m["source"] == f"{run}/R1" for m in cl["members"])]
        hits = CAT["residual"][run]["audit_hits"]
        first = set(hits.get("AUD", []))
        allaud = first | set(hits.get("AUD2", []))
        res.append(dict(run=run, N_loo=r["jackknife1"]["N"], r1_clusters=len(n_r1), fixed=len(fx),
                        pred=r["jackknife1"]["N"] - len(fx), obs_all=len(allaud), obs_first=len(first)))
    return res


def main():
    out = []
    P = out.append
    rows12 = matrix(CAT["clusters"], PRIMARY)
    rows15 = matrix(CAT["clusters"], ALL15)
    s_ref = len(CAT["clusters"])
    s_conf = sum(cl["confirmed"] for cl in CAT["clusters"])
    cl_primary_only = [cl for cl in CAT["clusters"] if any(m["source"].split("/")[0] in PRIMARY for m in cl["members"] if m["source"].endswith("/R1"))]
    P(f"# Falsification (offline, O3)\n\nS_ref = {s_ref} clusters in the catalog (all 36 sources, not revision-introduced); S_conf = {s_conf}; "
      f"clusters captured by at least one of the 12 primary R1 occasions = {len(cl_primary_only)}.\n")
    # capture profile
    cnt = collections.Counter(len(v) for v in rows12.values())
    Q = {j: cnt.get(j, 0) for j in range(0, 13)}
    P("## Capture profile (12 primary occasions; blocking clusters)\n")
    P("Q_j = number of clusters captured by exactly j occasions: " + ", ".join(f"Q{j}={Q[j]}" for j in range(1, 13)) + f"; never captured by a primary occasion (Q0) = {Q[0]}.\n")
    P("Per-cluster capture counts: " + ", ".join(f"{k}:{len(v)}" for k, v in rows12.items()) + "\n")
    sets = {o: {k for k, v in rows12.items() if o in v} for o in PRIMARY}
    jac = []
    for a, b in itertools.combinations(PRIMARY, 2):
        u = sets[a] | sets[b]
        jac.append(len(sets[a] & sets[b]) / len(u) if u else 1.0)
    mean_jac = statistics.mean(jac)
    P(f"Occasion cluster sets: " + "; ".join(f"{o}={len(sets[o])}" for o in PRIMARY) + f". Mean pairwise Jaccard = {mean_jac:.3f} (min {min(jac):.2f}, max {max(jac):.2f}).\n")
    # F1
    t_ref = f1(rows12, s_ref, "S_ref")
    t_conf = f1(rows12, s_conf, "S_conf")
    P("## F1 held-out prediction, reference S_ref\n"); P(table(t_ref, "S_ref")); v_ref = verdict(t_ref)
    P(f"\n**F1 verdict at k=4 (S_ref): {v_ref}**\n")
    P("## F1 reference S_conf (secondary)\n"); P(table(t_conf, "S_conf")); v_conf = verdict(t_conf)
    P(f"\nF1 verdict at k=4 (S_conf): {v_conf}\n")
    # full-data
    F = {}
    for name, rows, occ in (("12 occasions", rows12, PRIMARY), ("15 occasions", rows15, ALL15)):
        r = E.estimate_matrix(list(rows.values()), len(occ))
        F[name] = r
    P("## Full-data estimates\n")
    P("| data | S_obs | Q1 | Q2 | Chao2 N [95%] | Jack1 N [95%] | Jack2 N | unseen_upper95 | stop (open=0) |\n|---|---|---|---|---|---|---|---|---|")
    for name, r in F.items():
        P(f"| {name} | {r['S_obs']} | {r['Q']['1']} | {r['Q']['2']} | {r['chao2']['N']} [{r['chao2']['ci95'][0]}, {r['chao2']['ci95'][1]}] | {r['jackknife1']['N']} [{r['jackknife1']['ci95'][0]}, {r['jackknife1']['ci95'][1]}] | {r['jackknife2']['N']} | {r['unseen_upper95']} | {r['stop']} |")
    P(f"\nS_ref = {s_ref}, S_conf = {s_conf}. S_ref is itself a lower bound (it is built from the same kind of review); an estimate above S_ref is not a failure by itself.\n")
    # extra, non-decisive: reference restricted to clusters reported by a source of a primary run (arm 1 excluded)
    s_ref12 = sum(1 for cl in CAT["clusters"] if any(m["source"].split("/")[0] in PRIMARY for m in cl["members"]))
    t_12 = f1(rows12, s_ref12, "S_ref12"); v_12 = verdict(t_12)
    P(f"## Extra (not pre-registered): reference = clusters reported by any source of the 12 primary runs (arm 1 excluded), S_ref12 = {s_ref12}\n")
    P(table(t_12, "S_ref12")); P(f"\nF1 verdict at k=4 (S_ref12): {v_12}\n")
    # F2
    rs = f2(rows12)
    rho_all = spearman([r["pred"] for r in rs], [r["obs_all"] for r in rs])
    rho_first = spearman([r["pred"] for r in rs], [r["obs_first"] for r in rs])
    P("## F2 per-run test (secondary)\n")
    P("| run | N_hat (LOO Jack1) | R1 clusters | fixed | predicted residual | observed (all audits) | observed (first audit) |\n|---|---|---|---|---|---|---|")
    for r in rs:
        P(f"| {r['run']} | {r['N_loo']:.2f} | {r['r1_clusters']} | {r['fixed']} | {r['pred']:.2f} | {r['obs_all']} | {r['obs_first']} |")
    fm = lambda x: "undefined" if x is None else f"{x:.3f}"
    P(f"\nSpearman rho (predicted vs observed, all audits) = {fm(rho_all)}; first audit only = {fm(rho_first)} (n=12, ties averaged). Read: rho <= 0 is consistent with falsification. Weak by construction: the leave-one-out N_hat is almost the same for every run, so the prediction varies only with the number fixed.\n")
    # sensitivity: mechanical clusters only
    anc = {(r["source"], r["fid"]): r for r in map(json.loads, open(c.AB / "offline/anchored.jsonl"))}
    mech_clusters = [dict(cid=mc["cid"], members=[dict(source=s, fid=f) for s, f in mc["members"]], confirmed=len({s for s, _ in mc["members"]}) >= 2) for mc in MECH]
    rows_m = matrix(mech_clusters, PRIMARY)
    s_ref_m = len(mech_clusters); s_conf_m = sum(m["confirmed"] for m in mech_clusters)
    t_m = f1(rows_m, s_ref_m, "mech"); v_m = verdict(t_m)
    t_mc = f1(rows_m, s_conf_m, "mech-conf"); v_mc = verdict(t_mc)
    P("## Sensitivity: adjudication overrides ignored (mechanical clusters only)\n")
    P(f"Mechanical clusters: S_ref = {s_ref_m}, S_conf = {s_conf_m}.\n"); P(table(t_m, "mech"))
    P(f"\nF1 verdict at k=4 (mechanical, S_ref): {v_m}; (mechanical, S_conf): {v_mc}. Verdict {'is unchanged' if v_m == v_ref else 'CHANGES'} versus the adjudicated catalog ({v_ref}).\n")
    # CLI cross-check
    P("## Product CLI cross-check\n")
    ok = 0; total = 0
    with tempfile.TemporaryDirectory() as td:
        jobs = [("12", rows12, PRIMARY), ("15", rows15, ALL15)]
        rng = random.Random(7)
        for _ in range(10):
            sub = rng.sample(PRIMARY, rng.choice([2, 3, 4, 6]))
            jobs.append(("sub", {k: v & set(sub) for k, v in rows12.items()}, sub))
        for i, (nm, rows, occ) in enumerate(jobs):
            p = f"{td}/c{i}.json"
            capture_json(rows, occ, p)
            res = subprocess.run(["superclaude", "review", "estimate", p, "--blocking-only"], capture_output=True, text=True)
            total += 1
            ok += json.loads(res.stdout) == json.loads(json.dumps(E.estimate_matrix(list(rows.values()), len(occ))))
    P(f"`superclaude review estimate` output equals the library result on {ok}/{total} matrices (12 and 15 occasions plus 10 random subsets).\n")
    P(f"\n## F1 VERDICT (pre-registered, section 2): **{v_ref}** (S_conf: {v_conf}; mechanical clusters: {v_m})\n")
    P("Pre-registered rule: FALSIFIED at k=4 if for both Chao2 and Jackknife-1 MAE_est(4) >= MAE_obs(4) or COVER(4) < 0.5; SUPPORTED if an estimator has MAE_est(4) <= 0.7 * MAE_obs(4) and COVER(4) >= 0.7; otherwise WEAK.\n")
    open(c.AB / "offline/falsification.md", "w").write("\n".join(out))
    json.dump(dict(f1_ref=t_ref, f1_conf=t_conf, f1_mech=t_m, verdict=v_ref, verdict_conf=v_conf, verdict_mech=v_m, verdict_ref12=v_12, s_ref12=s_ref12, f1_ref12=t_12,
                   full=F, f2=rs, rho_all=rho_all, rho_first=rho_first, Q=Q, mean_jaccard=mean_jac, s_ref=s_ref, s_conf=s_conf,
                   cli_ok=[ok, total]), open(c.AB / "offline/falsification.json", "w"), indent=1, default=str)
    print("\n".join(out))


if __name__ == "__main__":
    main()
