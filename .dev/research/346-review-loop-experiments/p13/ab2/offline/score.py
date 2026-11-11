#!/usr/bin/env python3
"""O4: offline scores. usage: score.py [--out offline-results.md]. Scores both tuning passes and states G1 / live set / ADOPT-TOOL on pass 2 (the shipped lint)."""
import json, os, re, sys, pathlib, collections
import c93
AB = pathlib.Path(os.environ["AB"]); SP = pathlib.Path(os.environ["SP"]); OFF = AB/"offline"
corpus = json.load(open(OFF/"corpus.json")); by_sha = {r["sha256"]: r for r in corpus}
truth = json.load(open(OFF/"truth.json"))
THEME_RX = dict(c93.THEMES)
CHECKS = ["REF", "COUNT", "KV", "PHASE", "PATH"]
POS = {  # positive controls: (doc label, description, 1-based lines that locate the defect)
 "seeded": [("S1 retry 8 vs FR-3 5", [13, 39]), ("S2 delete log rows vs FR-7 30-day retention", [18, 41]), ("S3 signing secret logged vs FR-4/accept-5", [16, 47])],
 "cand_deletion": [("FR-5 removed, delivery_id still used", [16, 29])],
 "cand_regression": [("8 retries vs FR-3 (5)", [13, 39])],
}

def load(passdir):
    out = {}
    for r in corpus: out[r["sha256"]] = json.load(open(OFF/passdir/f"{r['sha256']}.json"))
    return out

def adjud(fn):
    rows = [json.loads(l) for l in open(OFF/fn)]
    return rows

def theme_hits(doc_findings, lint, theme):
    """True when the lint has a finding within 3 lines of a line cited by a blocking finding of `theme`, or a quote matching the theme regex."""
    cl = set()
    for rp in doc_findings:
        for f in rp.get("findings", []):
            if f["theme"] == theme: cl.update(f["cited"])
    hit = False
    for x in lint["findings"]:
        a, b = x["lines"]
        near = any(a - 3 <= n <= b + 3 for n in cl)
        rx = bool(re.search(THEME_RX[theme], x["quote"], re.I))
        yield x, near, rx

def hit_rates(lints, check, kind, near_only=False):
    """HIT(c,T) on final docs (document level) or on the orig doc (report level)."""
    res = {}
    for T in ("T1", "T2", "T3"):
        n = h = 0
        if kind == "final":
            for sha, rec in truth["docs"].items():
                if rec["group"] != "final": continue
                reps = [r for r in rec["reports"] if r.get("exists")]
                if not any(f["theme"] == T for r in reps for f in r.get("findings", [])): continue
                n += 1
                ok = False
                for x, near, rx in theme_hits(reps, lints[sha] if check is None else {"findings": [y for y in lints[sha]["findings"] if y["check"] == check]}, T):
                    ok |= near or (rx and not near_only)
                h += ok
        else:
            osha = truth["orig_sha"]
            for r in truth["docs"][osha]["reports"]:
                if not r.get("exists") or not any(f["theme"] == T for f in r.get("findings", [])): continue
                n += 1
                ok = False
                for x, near, rx in theme_hits([r], {"findings": [y for y in lints[osha]["findings"] if y["check"] == check]}, T):
                    ok |= near or (rx and not near_only)
                h += ok
        res[T] = (h, n)
    return res

def catalog_recall(lints, check):
    cat = truth["docs"][truth["orig_sha"]].get("catalog")
    if not cat: return None
    osha = truth["orig_sha"]
    cl = [c for c in cat["clusters"] if c.get("confirmed") and c.get("orig_span")]
    fl = [x for x in lints[osha]["findings"] if check is None or x["check"] == check]
    caught = []
    for c in cl:
        a, b = c["orig_span"]
        if any((x["lines"][0] - 3 <= b and a <= x["lines"][1] + 3) or (x["other_lines"] and x["other_lines"][0] - 3 <= b and a <= x["other_lines"][1] + 3) for x in fl):
            caught.append(c["cid"])
    return {"caught": caught, "n": len(cl)}

def score_pass(name, lintdir, adjfile):
    lints = load(lintdir); adj = adjud(adjfile)
    R = {"pass": name, "checks": {}}
    for c in CHECKS:
        rows = [r for r in adj if r["check"] == c]
        t = sum(1 for r in rows if r["verdict"] == "true"); n = len(rows)
        tw = sum(r["n_docs"] for r in rows if r["verdict"] == "true"); nw = sum(r["n_docs"] for r in rows)
        td = sum(1 for r in rows if r["verdict"] == "true" and r["defect"] == "yes")
        # flag counts per group
        cnt = collections.Counter(); 
        for sha, d in lints.items():
            for x in d["findings"]:
                if x["check"] == c: cnt[by_sha[sha]["group"]] += 1
        # audit relevance of true flags
        rel = 0
        for r in rows:
            if r["verdict"] != "true": continue
            d = lints[r["doc_sha"]]; x = next(y for y in d["findings"] if y["lint_id"] == r["lint_id"])
            cl = set()
            for rep in truth["docs"][r["doc_sha"]]["reports"]:
                for f in rep.get("findings", []): cl.update(f["cited"])
            if any(x["lines"][0] - 3 <= n_ <= x["lines"][1] + 3 for n_ in cl): rel += 1
        clean = sum(len([x for x in lints[s]["findings"] if x["check"] == c]) for s, r_ in by_sha.items() if r_["group"] == "clean")
        pos = {}
        for lab, items in POS.items():
            sha = next(s for s, r_ in by_sha.items() if any(l == f"pos:{lab}" for l in r_["labels"]))
            fl = [x for x in lints[sha]["findings"] if x["check"] == c]
            pos[lab] = [(desc, any(x["lines"][0] - 3 <= ln <= x["lines"][1] + 3 or (x["other_lines"] and x["other_lines"][0] - 3 <= ln <= x["other_lines"][1] + 3) for x in fl for ln in lines)) for desc, lines in items]
        orig_rows = [r for r in rows if r["doc_sha"] == truth["orig_sha"]]
        R["checks"][c] = {"MP": (t / n) if n else None, "true": t, "adjudicated": n, "distinct": None, "MP_weighted": (tw / nw) if nw else None,
                          "MP_defect": (td / n) if n else None, "audit_relevant_true": rel,
                          "MP_orig_only": (sum(1 for r in orig_rows if r["verdict"] == "true"), len(orig_rows)),
                          "flags": dict(cnt), "CLEAN": clean, "pos": pos,
                          "HIT_final": hit_rates(lints, c, "final"), "HIT_orig": hit_rates(lints, c, "orig"),
                          "HITn_final": hit_rates(lints, c, "final", True), "HITn_orig": hit_rates(lints, c, "orig", True),
                          "catalog": catalog_recall(lints, c)}
    # RFC census of orig
    osha = truth["orig_sha"]; R["census_orig"] = lints[osha]["census"].get("rfc2119_total")
    R["findings_total"] = sum(len(d["findings"]) for d in lints.values())
    return R

def g1(R):
    live = [c for c, v in R["checks"].items() if v["MP"] is not None and v["MP"] >= 0.8 and v["CLEAN"] == 0]
    g1 = {}
    for c in live:
        for T in ("T1", "T2", "T3"):
            for basis in ("HIT_final", "HIT_orig"):
                h, n = R["checks"][c][basis][T]
                if n and h / n >= 0.5: g1[(c, T, basis)] = (h, n)
    adopt = [c for c, v in R["checks"].items() if v["MP"] is not None and v["MP"] >= 0.9 and v["CLEAN"] == 0 and any(ok for items in v["pos"].values() for _, ok in items)]
    return live, g1, adopt

def fmt(R):
    L = [f"### Pass {R['pass']}\n", "| Check | MP (true/adjudicated) | MP weighted by docs | MP defect-only | flags final/orig/other/hist/ref | CLEAN | positive controls caught | HIT final T1/T2/T3 | HIT orig (R1 reports) T1/T2/T3 | HIT near-only final / orig | MP orig-only | catalog clusters caught on orig |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c, v in R["checks"].items():
        mp = "n/a" if v["MP"] is None else f"{v['MP']:.2f} ({v['true']}/{v['adjudicated']})"
        mw = "n/a" if v["MP_weighted"] is None else f"{v['MP_weighted']:.2f}"
        md = "n/a" if v["MP_defect"] is None else f"{v['MP_defect']:.2f}"
        fl = v["flags"]; f5 = "/".join(str(fl.get(g, 0)) for g in ("final", "orig", "other", "hist", "ref"))
        pc = "; ".join(f"{lab}:" + ",".join("Y" if ok else "n" for _, ok in items) for lab, items in v["pos"].items())
        hf = " / ".join(f"{h}/{n}" for h, n in (v["HIT_final"][T] for T in ("T1", "T2", "T3")))
        ho = " / ".join(f"{h}/{n}" for h, n in (v["HIT_orig"][T] for T in ("T1", "T2", "T3")))
        o = v["MP_orig_only"]
        hnf = " / ".join(f"{h}/{n}" for h, n in (v["HITn_final"][T] for T in ("T1", "T2", "T3")))
        hno = " / ".join(f"{h}/{n}" for h, n in (v["HITn_orig"][T] for T in ("T1", "T2", "T3")))
        cg = v["catalog"]; cgs = "n/a" if cg is None else f"{len(cg['caught'])}/{cg['n']} {cg['caught']}"
        L.append(f"| {c} | {mp} | {mw} | {md} | {f5} | {v['CLEAN']} | {pc} | {hf} | {ho} | {hnf} ; {hno} | {o[0]}/{o[1]} | {cgs} |")
    live, g, adopt = g1(R)
    L.append(f"\nLive check set (MP>=0.8 and CLEAN=0): {live or 'none'}.")
    L.append("G1 (a live-set check with HIT>=0.5 on T1/T2/T3, literal definition incl. quote-regex matches): " + ("PASS " + str({f'{k[0]}/{k[1]}/{k[2]}': v for k, v in g.items()}) if g else "FAIL"))
    gn = {}
    for c in live:
        for T in ("T1", "T2", "T3"):
            for basis in ("HITn_final", "HITn_orig"):
                h, n = R["checks"][c][basis][T]
                if n and h / n >= 0.5: gn[f"{c}/{T}/{basis}"] = (h, n)
    L.append("G1 restricted to line-proximity hits only (no quote-regex matches): " + ("PASS " + str(gn) if gn else "FAIL"))
    L.append(f"ADOPT-TOOL (MP>=0.9, CLEAN=0, one positive control caught): {adopt or 'none'}.")
    L.append(f"RFC census of the original (information only): {R['census_orig']}. Total findings over the corpus: {R['findings_total']}.\n")
    return "\n".join(L)

if __name__ == "__main__":
    P1 = score_pass("1 (literal, as written in the plan)", "lint-pass1", "adjudication-pass1.jsonl")
    P2 = score_pass("2 (after one tuning pass; the shipped lint)", "lint-pass2", "adjudication-pass2.jsonl")
    json.dump({"pass1": P1, "pass2": P2}, open(OFF/"scores.json", "w"), indent=1, default=str)
    cat = "present" if (SP/"p13/catalog/catalog.json").exists() else "absent: theme-v1 truth only (no catalog-level recall)"
    sizes = {c: (v["adjudicated"]) for c, v in P2["checks"].items()}
    txt = ["# PN2 offline results (Phase O)\n", f"Truth basis: theme-v1 (C9.3 tags). Catalog: {cat}.",
           "MP sample sizes: pass 1 REF 30 of 430 distinct, PATH 30 of 196, KV 26/26, COUNT 7/7, PHASE 4/4; pass 2 REF 30 of 245, PATH 18/18, PHASE 35/35, KV 3/3 (random.Random(0) samples where a check had more than 60 distinct flags). Distinct = identical quote+message across documents counted once.\n",
           fmt(P1), fmt(P2),
           "Supplementary stratum (adjudicated in full, not sampled): the 52 distinct REF flags on the Orca-spec family (finals, history, reference snapshots; 0 on the original) are all true-mechanical, "
           "and all are revision-log rows or reviewer finding ids (F-nn, N-nn, B-n, REQ-n, ARCH-n) cited in the spec body: 52/52, none is a defect an audit blocked on. "
           "The pass-2 REF sample (30 of 245 distinct) was drawn over all groups and is dominated by the `other` design documents (193 of 270 flags), whose ids are defined in sibling documents.\n",
           "G1 note: the literal G1 passes only through REF hits on revision-log rows of final documents (3/6 T1, 6/9 T2 documents); REF has 0 flags on the original and 0/12 R1 reports hit. "
           "PHASE and PATH reach T3 and T2 on the original (PHASE: AC-0.4 -> 7.2 -> WC-4, catalog D19; PATH: adversarial/workflow report paths vs the WC-4 template, catalog D1/D2/D10) but fail MP (0.03 and 0.11) because the revised finals handle the same dependency in their own text.\n"]
    (AB/"offline-results.md").write_text("\n".join(txt)); (OFF/"offline-results.md").write_text("\n".join(txt))
    print("\n".join(txt))
