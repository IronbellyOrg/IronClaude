"""outcomes and analyze for PN1 (reads the run states written by harness/advance)."""
import collections, itertools, json, pathlib, sqlite3, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import analysis as A, c93, harness as h

THEME_UNIVERSE = ("T1", "T2", "T3")


def theme_of(f):
    return c93.tag(f.get("claim", ""), f.get("anchor", "") + " " + (f.get("anchor2") or ""))


def original_spec():
    return (h.S1 / "inputs/repo-overlay" / h.SPEC).read_text()


def round1_findings(run):
    """{rid: [finding dicts]} (blocking only) from the ingested round-1 reports."""
    st = h.load(run)
    fm = h.findings_mod()
    out = {}
    for rid in h.reviewers_of(st, 1):
        key = f"R1.{rid}"
        if key not in st["done"]:
            continue
        p = h.ws(run) / h.D / f"review/round1-{rid}.md"
        out[rid] = [f for f in fm.parse_block(p.read_text(errors='ignore'))["findings"] if f["blocking"]]
    return out


def truth_theme(fs_by_rid):
    hits = {rid: {theme_of(f) for f in fs} & set(THEME_UNIVERSE) for rid, fs in fs_by_rid.items()}
    return hits, set(THEME_UNIVERSE)


def truth_catalog(fs_by_rid, catalog):
    fm = h.findings_mod()
    spec = original_spec()
    clusters = [c for c in catalog["clusters"] if c.get("confirmed") and c.get("orig_span")]
    hits = {rid: set() for rid in fs_by_rid}
    new = []          # [(key, (s,e))]
    new_hits = collections.defaultdict(set)
    for rid, fs in fs_by_rid.items():
        for f in fs:
            sp = fm.locate(spec, f["anchor"])
            span = sp[0] if sp else None
            th = theme_of(f)
            refs = set(fm.refs_norm(f))
            match = None
            if span:
                for c in clusters:
                    s, e = c["orig_span"]
                    if span[0] <= e + 3 and s <= span[1] + 3:
                        ctext = " ".join([c.get("label", ""), c.get("anchor", "")] + [m.get("quote", "") for m in c["members"]])
                        crefs = set(fm.refs_norm({"anchor": ctext, "claim": "", "refs": []}))
                        if c.get("theme") == th or (refs & crefs):
                            match = c["cid"]
                            break
            if match:
                hits[rid].add(match)
                continue
            key = None
            for k, ks in new:
                if span and ks and span[0] <= ks[1] + 3 and ks[0] <= span[1] + 3:
                    key = k
                    break
            if key is None:
                key = f"N{len(new) + 1}"
                new.append((key, span))
            new_hits[key].add(rid)
            hits[rid].add(key)
    confirmed_new = {k for k, rids in new_hits.items() if len(rids) >= 2}
    universe = {c["cid"] for c in clusters} | confirmed_new
    for rid in hits:
        hits[rid] = {k for k in hits[rid] if k in universe}
    return hits, universe


def truth_adjudicated(run, fs_by_rid):
    """Row level (one row per ledger row, as adjudicated): hits, universe, rejected counts, or None when ADJ is missing."""
    st = h.load(run)
    if "ADJ" not in st["done"]:
        return None
    mp = json.loads((h.run_dir(run) / "adj-map.json").read_text())
    txt = h.out_path(run, "ADJ").read_text(errors="ignore")
    verdict = {}
    import re
    for ln in txt.splitlines():
        ln = ln.strip()
        if ln.startswith("{") and '"x"' in ln:
            try:
                d = json.loads(ln)
                verdict[mp.get(d["x"])] = d["verdict"]
            except Exception:
                pass
    led = json.loads((h.ws(run) / h.D / "review/ledger.json").read_text())
    members = {}
    for row in led["rows"]:
        for m in row["members"]:
            if m["round"] == 1 and m["blocking"]:
                members.setdefault(m["reviewer_id"], set()).add(row["lid"])
    universe = {l for l, v in verdict.items() if v == "confirmed"}
    hits = {rid: {l for l in members.get(rid, set()) if l in universe} for rid in fs_by_rid}
    rej = {rid: sum(1 for l in members.get(rid, set()) if verdict.get(l) == "rejected") for rid in fs_by_rid}
    return hits, universe, rej


def outcomes():
    cat = json.loads(h.CATALOG.read_text()) if h.CATALOG.exists() else None
    basis = "catalog-v1" if cat else "theme-v1"
    n = 0
    store = {}
    for run in h.all_runs():
        st = h.load(run)
        if st["phase"] != "complete":
            continue
        fs = round1_findings(run)
        if not fs:
            continue
        tok = {rid: (st["log"][f"R1.{rid}"]["tokens"] or {}).get("out") for rid in fs}
        bn = {rid: len(v) for rid, v in fs.items()}
        sets = {}
        hits, uni = truth_catalog(fs, cat) if cat else truth_theme(fs)
        sets[basis] = (hits, uni, None)
        t = truth_adjudicated(run, fs)
        if t:
            sets["adjudicated-v1"] = t
        store[run] = {}
        for b, tup in sets.items():
            hits, uni = tup[0], tup[1]
            rej = tup[2] if len(tup) > 2 else None
            rows = A.outcome_rows(hits, bn, uni, rej, tok)
            store[run][b] = {"hits": {k: sorted(v) for k, v in hits.items()}, "universe": sorted(uni), "rows": rows}
            for rid, row in rows.items():
                rec = {"schema_version": "review-telemetry/1", "kind": "outcome", "record_id": __import__("uuid").uuid4().hex, "ts_utc": h.now(),
                       "run_id": run, "reviewer_record_id": st["telemetry_ids"].get(f"R1.{rid}"), "truth_basis": b, **row, "supersedes": None,
                       "stratum": st["stratum"]}
                if not rec["reviewer_record_id"]:
                    continue
                f = h.run_dir(run) / f"outcome-{b}-{rid}.json"
                f.write_text(json.dumps(rec))
                h.cli("telemetry", "append", "--dir", h.TELEMETRY_DIR, "--record", f)
                n += 1
    (h.AB / "outcomes.json").write_text(json.dumps(store, indent=1))
    h.cli("telemetry", "load", "--dir", h.TELEMETRY_DIR, "--db", h.AB / "telemetry.sqlite")
    print(f"wrote {n} outcome records (truth {basis} + adjudicated-v1 where ADJ exists); loaded into {h.AB / 'telemetry.sqlite'}")


def fmt(x, nd=2):
    return "n/a" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def baseline_r1_tokens():
    out = []
    for a in (2, 3):
        for r in range(1, 7):
            p = h.P11 / "runs" / f"a{a}-r{r}" / "PROMPT-R1.md"
            s = A.step_tokens(p, h.TASKS_GLOB, "sonnet", warn=lambda *_: None) if p.exists() else None
            if s:
                out.append(s["out"])
    return out


def analyze():
    r = h.rules()
    res = h.compute_results()
    son, hk = res["sonnet"], res["haiku"]
    lines = ["# PN1 RESULTS: panel + merge + ledger (design b1) versus the Stage 2 arm-3 baseline", ""]
    cls = son["class"]
    lines += [f"DECISION: {res['final']}", "",
              f"Rule applied (pre-registered, rules.json): {cls['decision']}" + (" (COST-HOLD)" if cls.get("cost_hold") else "") + "; " + "; ".join(cls["reasons"]),
              f"Haiku gate (D3, never pooled): {hk['gate']['status']} " + "; ".join(hk["gate"]["reasons"]), ""]
    ext = h.AB / "extension.json"
    lines.append(f"Replicates: Sonnet n={son['n_total']} completed of {len(son['runs'])} built" + ("; the single D4 extension (+3) was used" if ext.exists() else "; no D4 extension used")
                 + f". Haiku n={hk['n_total']} of {len(hk['runs'])}.")
    lines.append("")
    s = son["stats"]
    if s:
        tv = s["tokens"]
        b = r["baseline"]
        d = r["decision"]
        lines += ["## Decision table (Sonnet stratum)", "", "| Rule | Condition | Baseline | Test | Verdict |", "|---|---|---|---|---|",
                  f"| DROP-1 no gain | BLK_T > {d['drop1_blk_factor']} x B_BLK = {d['drop1_blk_factor'] * b['B_BLK']:.2f} | {b['B_BLK']} | {fmt(s['BLK_T'])} | {'HIT' if s['BLK_T'] > d['drop1_blk_factor'] * b['B_BLK'] else 'clear'} |",
                  f"| DROP-2 cost (D6: R_LOOP) | R_LOOP > {d['drop2_r_loop']} (3.3 on R_B rescaled) | 1.00 | {fmt(s['R_LOOP'])} | {'HIT' if (s['R_LOOP'] or 0) > d['drop2_r_loop'] else 'clear'} |",
                  f"| COST-HOLD | {d['cost_hold_r_loop']} < R_LOOP <= {d['drop2_r_loop']} (2.0 on R_B rescaled) | 1.00 | {fmt(s['R_LOOP'])} | {'HOLD' if cls.get('cost_hold') else 'clear'} |",
                  f"| DROP-3 harm | PASS_T < {d['drop3_pass_min']:.3f} or GROWTH_T > {d['drop3_growth_factor'] * b['B_GROWTH']:.4f} | 1.00 / {b['B_GROWTH']} | {fmt(s['PASS_T'])} / {fmt(s['GROWTH_T'], 4)} | {'HIT' if (s['PASS_T'] < d['drop3_pass_min'] or s['GROWTH_T'] > d['drop3_growth_factor'] * b['B_GROWTH']) else 'clear'} |",
                  f"| ADOPT | BLK_T <= {d['adopt_blk_factor'] * b['B_BLK']:.2f}, PASS_T >= {d['adopt_pass_min']:.3f}, GROWTH_T <= {d['adopt_growth_max']}, BLOCK_OK >= {d['adopt_block_ok_min']}, no cost hold | | BLOCK_OK {fmt(s['BLOCK_OK'])} | {'yes' if cls['decision'] == 'ADOPT' else 'no'} |",
                  f"| Audit agreement | |AUD - AUD2| <= {d['max_audit_gap']} | | {fmt(s['AUD1'])} vs {fmt(s['AUD2'])} (gap {fmt(s['audit_gap'])}) | {'ok' if s['audit_gap'] <= d['max_audit_gap'] else 'DISAGREE'} |", ""]
        lines += ["## Tokens (D2: A = loop only decides; B = loop + one audit is reported only; each message id counted once)", "",
                  "| | Test mean | Baseline | Ratio |", "|---|---|---|---|",
                  f"| A loop-only (incl. ADJ) | {fmt(tv['A'], 0)} | {r['tokens']['A_BASE']} | R_LOOP {fmt(tv['R_LOOP'])} |",
                  f"| one audit | {fmt(tv['AUD'], 0)} | {r['tokens']['AUD_BASE']} | |",
                  f"| B loop + one audit | {fmt(tv['B'], 0)} | {r['tokens']['B_BASE']} | R_B {fmt(tv['R_B'])} (reported, never decides) |", ""]
        mean_excl = A.mean(x["A_excl_adj"] for x in son["done"])
        lines += [f"Loop-only without the ADJ worker: {fmt(mean_excl, 0)} (R {fmt(mean_excl / r['tokens']['A_BASE'])}). The ADJ worker is a measurement device in this experiment; D2 counts adjudication in the loop, so the decision uses the figure with ADJ.", ""]
        res_by_run = sorted(x["residual"] for x in son["done"])
        q = lambda p: res_by_run[int(round(p * (len(res_by_run) - 1)))]
        lines += [f"Literal report criterion (not a decision rule): median residual {fmt(q(0.5))}, lower quartile {fmt(q(0.25))} (per-run residual = mean of its two audits).", ""]
    lines += ["## Per-run table (Sonnet)", "", "| run | reviews | decision | final bytes | growth | loop tokens A | AUD tokens | AUD ids (themes) | AUD2 ids (themes) | events |", "|---|---|---|---|---|---|---|---|---|---|"]
    for x in son["runs"]:
        if "reviews" not in x:
            lines.append(f"| {x['run']} | not completed ({x['phase']}) | | | | | | | | lost {x['lost']} |")
            continue
        t1, t2 = x["audit_tags"]
        lines.append(f"| {x['run']} | {x['reviews']} | {x['decision']} | {x['final_bytes']} | {x['growth'] * 100:.2f}% | {x['A']} | {x['AUD_tok']} | {t1 or 'PASS/none'} | {t2 or 'PASS/none'} | {x['events']} |")
    lines += ["", "## Haiku stratum (secondary, never pooled; AUD stays Sonnet)", ""]
    hb = hk["baseline"]
    lines.append(f"Haiku runs completed {hk['n_total']}/{len(hk['runs'])}; mean audit blockers test {fmt(hk['stats']['BLK_T']) if hk['stats'] else 'n/a'} vs Haiku baseline {fmt(hb['mean_blk']) if hb else 'n/a (results.json missing)'}; ratio {fmt(hk['gate']['ratio'])}; gate {hk['gate']['status']}.")
    if hk["stats"]:
        lines.append(f"Haiku loop-only R_LOOP {fmt(hk['stats']['R_LOOP'])} (against the Sonnet A_BASE; reported only), PASS_T {fmt(hk['stats']['PASS_T'])}, harness-failure rate {fmt(hk['lost_rate'])}.")
    lines += ["", "## Round-1 coverage: size, model and resampling (catalog-v1 if present else theme-v1)", ""]
    lines += coverage_section(son)
    lines += ["", "## Telemetry summary (model_scores view, per stratum)", ""]
    db = h.AB / "telemetry.sqlite"
    if db.exists():
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        rows = con.execute("select * from model_scores").fetchall()
        lines += ["| model | tier | stand_in | stratum | truth | n_runs | sum TP | sum FP | mean precision | mean recall | sum unique | tokens per TP |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for q_ in rows:
            lines.append("| " + " | ".join(fmt(q_[k]) for k in ("model_observed", "slot_tier", "slot_stand_in", "stratum", "truth_basis", "n_runs", "sum_confirmed_tp", "sum_false_pos", "mean_precision", "mean_recall_vs_confirmed", "sum_unique_tp", "cost_per_confirmed_tp")) + " |")
        lines.append("\nHaiku records are stand-ins: no conclusion is drawn about real Tier 2 / Tier 3 models.")
    else:
        lines.append("telemetry.sqlite not built yet (run `harness.py outcomes`).")
    lines += ["", "## Validity notes", ""]
    for x in son["runs"] + hk["runs"]:
        if x["lost"] or x["phase"] == "lost":
            lines.append(f"- {x['run']}: lost steps {x['lost']} (phase {x['phase']})")
    lines.append("- Cost never stopped a run (D6); token ratios are post-hoc. Reviewer telemetry records are written at merge time so that verdict_mismatch is known.")
    lines.append("- Clustering caveat (offline replay): single-linkage plus the low-specificity P0/P1 tokens can merge adjacent distinct defects into one row; per-defect recall uses member-level theme/catalog truth, ADJ rows are row-level.")
    (h.AB / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print("wrote", h.AB / "RESULTS.md")


def coverage_section(son):
    p = h.AB / "outcomes.json"
    if not p.exists():
        return ["Run `harness.py outcomes` first (needs completed runs)."]
    store = json.loads(p.read_text())
    sonnet_runs = {x["run"] for x in son["done"]}
    basis = "catalog-v1" if h.CATALOG.exists() else "theme-v1"
    out = []
    # (a) anchor check
    t1b = {run: set(v[basis]["hits"].get("t1b-1", [])) for run, v in store.items() if run in sonnet_runs and basis in v}
    base_tok = baseline_r1_tokens()
    tok_a = [x["tokens_by_step"].get("R1.t1b-1") for x in son["done"]]
    t1_missing = 0
    for x in son["done"]:
        fs = round1_findings(x["run"]).get("t1b-1", [])
        if "T1" not in {theme_of(f) for f in fs}:
            t1_missing += 1
    out += ["(a) Anchor check, t1b-1 (sonnet) round 1 versus the 12 baseline sonnet R1s:", "",
            f"- t1b-1 mean confirmed defects {fmt(A.mean(len(s) for s in t1b.values()))}; mean R1 output tokens {fmt(A.mean([t for t in tok_a if t]), 0)}; baseline mean R1 tokens {fmt(A.mean(base_tok), 0)} (n={len(base_tok)}).",
            f"- Drift check: T1 missing from {t1_missing} of {len(son['done'])} t1b-1 reports (baseline: present in every arm-3 R1 by C9.3 tags); more than 2 means possible drift since Stage 2" + (": DRIFT POSSIBLE." if t1_missing > 2 else ": no drift flagged."), ""]
    # (b) model vs resampling
    hh, sh, u2, u4 = [], [], [], []
    marg = collections.defaultdict(list)
    for run, v in store.items():
        if run not in sonnet_runs or basis not in v:
            continue
        hits = {k: set(x) for k, x in v[basis]["hits"].items()}
        uni = set(v[basis]["universe"])
        for a, b in itertools.combinations(["t2-1", "t3-1", "t3-2"], 2):
            if a in hits and b in hits:
                j = A.jaccard(hits[a], hits[b])
                if j is not None:
                    hh.append(j)
        for b in ["t2-1", "t3-1", "t3-2"]:
            if "t1b-1" in hits and b in hits:
                j = A.jaccard(hits["t1b-1"], hits[b])
                if j is not None:
                    sh.append(j)
        if "t1b-1" in hits and "t2-1" in hits:
            u2.append(A.union_recall([hits["t1b-1"], hits["t2-1"]], uni))
        u4.append(A.union_recall(list(hits.values()), uni))
        for rid, d in A.leave_one_out(hits, uni).items():
            marg[rid].append(d["marginal"])
    o4 = json.loads((h.AB / "offline/o4-union.json").read_text()) if (h.AB / "offline/o4-union.json").exists() else None
    o4k = None
    if o4:
        o4k = {k: (o4["catalog"]["k"][k]["recall_of_confirmed"] if basis == "catalog-v1" and "catalog" in o4 else o4["k"][k]["mean_themes"] / 3) for k in ("1", "2", "4")}
    out += ["(b) Different model versus resampling (Jaccard of confirmed-defect sets, lower = more complementary):", "",
            f"- haiku-haiku pairs mean {fmt(A.mean(hh))} (n={len(hh)}); sonnet-haiku pairs mean {fmt(A.mean(sh))} (n={len(sh)}).",
            f"- recall of t1b-1 + t2-1 (sonnet + haiku, k=2): {fmt(A.mean(u2))}; same-model counterfactual O4 k=2 (sonnet resampled): {fmt(o4k['2']) if o4k else 'n/a'}.", ""]
    out += ["(c) Marginal value (union of all four minus leave-one-out union):", "", "| reviewer | mean marginal recall |", "|---|---|"]
    for rid, vals in sorted(marg.items()):
        out.append(f"| {rid} | {fmt(A.mean(vals))} |")
    if o4k:
        out += ["", f"- union(4) mean {fmt(A.mean(u4))}; O4 same-model k=4 {fmt(o4k['4'])}, k=1 {fmt(o4k['1'])}: size effect = {fmt(o4k['4'] - o4k['1'])}; mix effect = union(4) - O4(k=4) = {fmt((A.mean(u4) or 0) - o4k['4'])}."]
    # residual decomposition
    out += ["", "Residual decomposition (audit blocking findings: never found by the run's R1 union vs found then survived):", ""]
    cnt = collections.Counter()
    for x in son["done"]:
        r1th = set()
        for rid, s in store.get(x["run"], {}).get("theme-v1", {}).get("hits", {}).items():
            r1th |= set(s)
        if not r1th:                       # catalog truth: use the C9.3 tags of the reviewers' blocking findings
            fs = round1_findings(x["run"])
            r1th = {theme_of(f) for v in fs.values() for f in v}
        for tags in x["audit_tags"]:
            for _id, th in (tags or []):
                cnt[A.residual_class(th, r1th)] += 1
    out.append(f"- test audits: {dict(cnt)}")
    base = collections.Counter()
    for r in range(1, 7):
        run = f"a3-r{r}"
        r1 = {t for _i, t in c93.blocking_tags(h.P11 / "runs" / run / "ws" / h.D / "review/round1.md")}
        for p in (h.P11 / "runs" / run / "aud/ws" / h.AUD_OUT, h.SP / "p12/baseline-audit2" / run / "ws" / h.AUD_OUT):
            if p.exists():
                for _i, th in c93.blocking_tags(p):
                    base[A.residual_class(th, r1)] += 1
    out.append(f"- baseline 12 audits: {dict(base)}")
    return out
