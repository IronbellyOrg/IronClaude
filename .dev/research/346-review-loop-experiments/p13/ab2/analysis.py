"""PN2 analysis: token convention (D2), decision rule (D1, D6), strata (D3) and the adaptive extension (D4).

Pure functions plus a thin report writer. All thresholds come from decision.toml. Tokens are counted with each
message id once (C9.1) and are read only from finished transcripts; nothing here is called while a run is in progress
to decide whether it continues (D6).
"""
import glob, json, os, pathlib, re, tomllib, collections
import c93

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S/"scratchpad"; P11 = SP/"p11"; P12 = SP/"p12"; AB = pathlib.Path(os.environ.get("PN2_AB") or SP/"p13/ab2"); RUNS = AB/"runs"
TASKS_GLOB = os.environ.get("PN2_TASKS_GLOB") or "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
ORIG_BYTES = 57763
LOOP_STEPS = ("R1", "V1", "R2", "V2", "R3")

def config(path=None):
    return tomllib.load(open(path or AB/"decision.toml", "rb"))

def convert_limit(L, cfg):
    """D6: a limit L on R_B (loop + one audit) as a limit on R_LOOP, rounded to two decimals."""
    b = cfg["baseline"]
    return round((L * b["b_base"] - b["audit_base"]) / b["a_base"], 2)

# ---------- tokens (C9.1) ----------
def transcript_usage(lines):
    """Sum of output tokens with each message id counted once (max over its lines); done flag; models seen."""
    per = {}; done = False; models = collections.Counter(); anon = 0
    for line in lines:
        try: d = json.loads(line)
        except Exception: continue
        msg = d.get("message") or {}
        if msg.get("role") != "assistant": continue
        u = msg.get("usage") or {}
        mid = msg.get("id")
        if mid is None: anon += 1; mid = f"__anon{anon}"
        per[mid] = max(per.get(mid, 0), u.get("output_tokens") or 0)
        if msg.get("model"): models[msg["model"]] += 1
        if isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "SubagentHandback" and "DONE" in json.dumps(c.get("input")): done = True
    return sum(per.values()), done, models

def find_transcripts(prompt_path, glob_pat=TASKS_GLOB):
    out = []
    for f in glob.glob(glob_pat):
        try:
            with open(f, errors="ignore") as fh:
                head = "".join(next(fh, "") for _ in range(6))
        except Exception: continue
        if str(prompt_path) in head or _fp_match(prompt_path, head): out.append(pathlib.Path(f))
    return out

def _fp_match(prompt_path, head):
    """Fallback (coordinator launches by pasting the prompt text, so the prompt FILE path is not in the transcript):
    match on the prompt's SANDBOX dir plus its whole BRIEF body (JSON-escaped in the transcript)."""
    try:
        t = pathlib.Path(prompt_path).read_text(errors="ignore")
        m = re.search(r"SANDBOX: work ONLY inside (\S+?)\.", t)
        b = t.split("BRIEF (verbatim, from the coordinator):\n", 1)[1].split("\n\nFINAL REPLY", 1)[0]
    except Exception:
        return False
    esc = json.dumps(b)[1:-1]
    return bool(m) and (m.group(1) + ". Do not read") in head and esc in head

def step_tokens(prompt_path, expected_model_substr, glob_pat=TASKS_GLOB):
    """(tokens, done, warn). Several matching transcripts: keep the expected model with the most tokens, warn."""
    cands = []
    for f in find_transcripts(prompt_path, glob_pat):
        toks, done, models = transcript_usage(f.read_text(errors="ignore").splitlines())
        ok = any(expected_model_substr in m for m in models) if models else False
        cands.append((ok, toks, done, f))
    if not cands: return None
    warn = len(cands) > 1
    cands.sort(key=lambda c: (c[0], c[1]), reverse=True)
    ok, toks, done, f = cands[0]
    return {"tokens": toks, "done": done, "warn": warn, "transcript": str(f), "model_ok": ok}

MODEL_SUBSTR = {"sonnet": "sonnet", "haiku": "haiku"}

# ---------- baseline from the Stage 2 data ----------
def baseline_tokens(glob_pat=TASKS_GLOB):
    """Per a3 run: loop tokens (R1,V1,R2,V2,R3) and AUD tokens from the p11 transcripts. None when a transcript is missing."""
    out = {}
    for i in range(1, 7):
        run = f"a3-r{i}"; rec = {"steps": {}}
        for step in LOOP_STEPS + ("AUD",):
            p = P11/"runs"/run/f"PROMPT-{step}.md"
            if not p.exists(): continue
            t = step_tokens(p, "sonnet", glob_pat)
            if t is None: continue
            rec["steps"][step] = t["tokens"]
        if not rec["steps"]: continue
        rec["loop"] = sum(v for k, v in rec["steps"].items() if k in LOOP_STEPS)
        rec["aud"] = rec["steps"].get("AUD")
        out[run] = rec
    return out

def baseline_audits():
    """The 12 baseline audits (6 first + 6 second): blocking ids and themes by C9.3."""
    rows = []
    for i in range(1, 7):
        run = f"a3-r{i}"
        for tag, p in (("AUD", P11/"runs"/run/"aud/ws"/D/"review/audit.md"), ("AUD2", P12/"baseline-audit2"/run/"ws"/D/"review/audit.md")):
            if p.exists(): rows.append(audit_record(p, f"{run}/{tag}"))
    return rows

def audit_record(path, source):
    t = pathlib.Path(path).read_text(errors="ignore")
    vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", t, re.I)
    verdict = vs[-1].upper() if vs else "NONE"
    ids = c93.parse_ids(c93.ids_from(path)) if verdict == "FAIL" else []
    themes = []
    for fid in ids:
        sec = c93.find_section(t, fid)
        themes.append(c93.tag(sec[0], sec[1]) if sec else "other")
    return {"source": source, "verdict": verdict, "blocking": len(ids), "ids": ids, "themes": themes}

def theme_share(audits, themes):
    """Share of audits that report at least one blocking finding tagged with a theme in `themes`."""
    if not audits: return None
    return sum(1 for a in audits if any(t in themes for t in a["themes"])) / len(audits)

# ---------- one run ----------
def run_record(run, glob_pat=TASKS_GLOB):
    d = RUNS/run
    st = json.load(open(d/"state.json"))
    log = st["log"]; stratum = st.get("stratum", "sonnet")
    loop_verdicts = [(s, log[s].get("verdict")) for s in ("R1", "R2", "R3") if s in log]
    reviews = len(loop_verdicts)
    final = loop_verdicts[-1][1] if loop_verdicts else None
    auds = [audit_record(d/sub/"ws"/D/"review/audit.md", f"{run}/{tag}") for sub, tag in (("aud", "AUD"), ("aud2", "AUD2"))
            if (d/sub/"ws"/D/"review/audit.md").exists() and tag in log and log[tag].get("output_exists")]
    completed = len(auds) == 2
    spec_bytes = None
    for s in ("R3", "V2", "R2", "V1", "R1"):       # the spec after the last loop step that finished
        if s in log and "spec_after" in log[s]: spec_bytes = log[s]["spec_after"]["bytes"]; break
    growth = None if spec_bytes is None else 100.0*(spec_bytes - ORIG_BYTES)/ORIG_BYTES
    toks = {}
    for step in LOOP_STEPS + ("AUD", "AUD2"):
        p = d/f"PROMPT-{step}.md"
        if step in log or p.exists():
            model = "sonnet" if step in ("AUD", "AUD2") else ("haiku" if stratum == "haiku" else "sonnet")
            t = step_tokens(p, MODEL_SUBSTR[model], glob_pat) if p.exists() else None
            if t: toks[step] = t["tokens"]
    loop = sum(v for k, v in toks.items() if k in LOOP_STEPS)
    audv = [toks[k] for k in ("AUD", "AUD2") if k in toks]
    return {"run": run, "stratum": stratum, "completed": completed, "final_verdict": final, "reviews": reviews, "pass": final == "PASS",
            "growth_pct": growth, "loop_tokens": loop, "r1_tokens": toks.get("R1"), "aud_tokens": audv,
            "one_audit_tokens": (sum(audv)/len(audv)) if audv else None, "audits": auds,
            "lint": {k: v for k, v in log.items() if k.startswith("LINT")}, "tokens_by_step": toks}

# ---------- decision ----------
def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs)/len(xs) if xs else None

def summarize(records, cfg, baseline_theme):
    """Sonnet-stratum numbers for the rule table. `records` are completed or not; only completed ones count."""
    done = [r for r in records if r["completed"]]
    b = cfg["baseline"]
    all_aud = [a for r in done for a in r["audits"]]
    blk = mean([a["blocking"] for a in all_aud])
    first = mean([r["audits"][0]["blocking"] for r in done]); second = mean([r["audits"][1]["blocking"] for r in done])
    loop = mean([r["loop_tokens"] for r in done if r["loop_tokens"]])
    oneaud = mean([r["one_audit_tokens"] for r in done if r["one_audit_tokens"]])
    out = {"n_planned": len(records), "n_completed": len(done), "BLK_T": blk, "AUD_mean": first, "AUD2_mean": second,
           "PASS_T": (sum(1 for r in done if r["pass"])/len(done)) if done else None,
           "GROWTH_T": mean([r["growth_pct"] for r in done]), "loop_tokens": loop, "one_audit_tokens": oneaud,
           "R_LOOP": (loop/b["a_base"]) if loop else None,
           "R_B": ((loop + oneaud)/b["b_base"]) if loop and oneaud else None,
           "THEME_T": theme_share(all_aud, cfg["theme"]["themes"]), "THEME_B": baseline_theme,
           "R1_tokens": mean([r["r1_tokens"] for r in done if r["r1_tokens"]])}
    return out

def decide(m, cfg):
    """Rule table of PLAN-2 section 2 with decision.toml constants. Returns (verdict, reasons, band) ; band tells D4 whether
    the INCONCLUSIVE comes from the noise band (extension allowed) or from a validity problem (not extendable)."""
    dr, ad, va, b = cfg["drop"], cfg["adopt"], cfg["validity"], cfg["baseline"]
    if m["n_completed"] < va["min_completed"]:
        return "INCONCLUSIVE", [f"only {m['n_completed']} completed runs (< {va['min_completed']})"], False
    if m["AUD_mean"] is not None and abs(m["AUD_mean"] - m["AUD2_mean"]) > va["aud_gap_max"]:
        return "INCONCLUSIVE", [f"AUD and AUD2 arm means differ by {abs(m['AUD_mean']-m['AUD2_mean']):.2f} > {va['aud_gap_max']}"], False
    drops = []
    if m["BLK_T"] >= dr["blk_t_at_least"]: drops.append(f"BLK_T {m['BLK_T']:.2f} >= {dr['blk_t_at_least']}")
    if m["R_LOOP"] is not None and m["R_LOOP"] > dr["r_loop_above"]: drops.append(f"R_LOOP {m['R_LOOP']:.2f} > {dr['r_loop_above']} (post-hoc cost clause)")
    if m["PASS_T"] < dr["pass_t_below"]: drops.append(f"PASS_T {m['PASS_T']:.2f} < {dr['pass_t_below']:.2f}")
    if m["GROWTH_T"] > dr["growth_above_pct"]: drops.append(f"GROWTH_T {m['GROWTH_T']:.2f}% > {dr['growth_above_pct']}%")
    if drops: return "DROP", drops, True
    ok = []
    adopt = (m["BLK_T"] <= b["b_blk"] - ad["blk_t_drop"]
             and m["THEME_T"] is not None and m["THEME_B"] is not None and m["THEME_T"] <= ad["theme_ratio_at_most"] * m["THEME_B"]
             and m["R_LOOP"] is not None and m["R_LOOP"] <= ad["r_loop_at_most"])
    if adopt: return "ADOPT", [f"BLK_T {m['BLK_T']:.2f} <= {b['b_blk']-ad['blk_t_drop']:.2f}", f"THEME_T {m['THEME_T']:.2f} <= {ad['theme_ratio_at_most']}*{m['THEME_B']:.2f}", f"R_LOOP {m['R_LOOP']:.2f} <= {ad['r_loop_at_most']}"], True
    return "INCONCLUSIVE", ["no DROP condition and not all ADOPT conditions (noise band)"], True

def haiku_check(test_records, base_path):
    """D3: relative reduction of mean audit blockers vs the shared Haiku baseline; harness-failure rate not inflated."""
    cfg = config()
    done = [r for r in test_records if r["completed"]]
    n = len(test_records)
    res = {"n_planned": n, "n_completed": len(done)}
    if not test_records:
        return dict(res, status="pending", reason="no Haiku runs yet")
    t_blk = mean([a["blocking"] for r in done for a in r["audits"]])
    t_fail = (n - len(done))/n
    p = pathlib.Path(base_path)
    if not p.exists(): return dict(res, status="pending", reason="Haiku baseline results.json not present", mean_blocking=t_blk, failure_rate=t_fail)
    try:
        base = json.load(open(p)); runs = base.get("runs", base)
        vals = []; fails = 0; total = 0
        for r in (runs.values() if isinstance(runs, dict) else runs):
            if not isinstance(r, dict): continue
            total += 1
            counts = r.get("audit_blocking") or r.get("aud_blocking") or r.get("blocking_counts") or r.get("blocking")
            if isinstance(counts, (int, float)): counts = [counts]
            if counts: vals.extend(counts)
            else: fails += 1
        b_blk = sum(vals)/len(vals) if vals else None
        b_fail = fails/total if total else None
    except Exception as e:
        return dict(res, status="pending", reason=f"Haiku baseline unreadable: {e}", mean_blocking=t_blk, failure_rate=t_fail)
    if not b_blk:
        return dict(res, status="pending", reason="Haiku baseline has no usable blocker counts", mean_blocking=t_blk, failure_rate=t_fail)
    rel = 1 - t_blk/b_blk if t_blk is not None else None
    ok = rel is not None and rel > 0 and t_fail <= (b_fail or 0) + cfg["strata"]["haiku_failure_margin"]
    return dict(res, status="ok" if ok else "against", mean_blocking=t_blk, baseline_blocking=b_blk, relative_reduction=rel, failure_rate=t_fail, baseline_failure_rate=b_fail)

def final_verdict(sonnet_verdict, haiku):
    """D3: ADOPT needs the Haiku stratum to agree; a missing stratum makes it 'ADOPT (Haiku robustness pending)'."""
    if sonnet_verdict != "ADOPT": return sonnet_verdict
    if haiku["status"] == "pending": return "ADOPT (Haiku robustness pending)"
    if haiku["status"] == "ok": return "ADOPT"
    return "INCONCLUSIVE (Sonnet ADOPT, Haiku stratum points the other way)"

def analyze(write=True):
    cfg = config()
    recs = {"sonnet": [], "haiku": []}
    for d in sorted(RUNS.iterdir()) if RUNS.exists() else []:
        if (d/"state.json").exists():
            r = run_record(d.name); recs[r["stratum"]].append(r)
    base_audits = baseline_audits()
    theme_b = theme_share(base_audits, cfg["theme"]["themes"])
    b_blk = mean([a["blocking"] for a in base_audits]) if base_audits else None
    m = summarize(recs["sonnet"], cfg, theme_b)
    verdict, reasons, band = decide(m, cfg) if m["n_completed"] else ("NOT RUN", ["no completed Sonnet runs"], False)
    ext_used = (AB/"extension.json").exists()
    action = None
    if verdict == "INCONCLUSIVE" and band and not ext_used and m["n_completed"] == cfg["strata"]["sonnet_n"]:
        action = "EXTEND: run `harness.py extend` once (D4), then re-run analyze at n=9"
    hk = haiku_check(recs["haiku"], SP/cfg["strata"]["haiku_baseline"])
    fv = final_verdict(verdict, hk) if verdict != "NOT RUN" else verdict
    result = {"decision": fv, "sonnet_verdict": verdict, "reasons": reasons, "summary": m, "baseline": {"B_BLK_recomputed": b_blk, "THEME_B": theme_b, "audits": len(base_audits)},
              "haiku": hk, "next_action": action, "extension_used": ext_used, "runs": recs}
    if write: (AB/"results.json").write_text(json.dumps(result, indent=1, default=str)); write_report(result, cfg)
    return result

def f2(x, nd=2): return "n/a" if x is None else f"{x:.{nd}f}"

def write_report(res, cfg):
    m = res["summary"]; b = cfg["baseline"]
    off = AB/"offline-results.md"
    L = [f"# PN2 RESULTS", "", f"DECISION: {res['decision']}  (Sonnet stratum verdict: {res['sonnet_verdict']}; {'; '.join(res['reasons'])})", ""]
    if res["next_action"]: L += [f"NEXT: {res['next_action']}", ""]
    L += ["Token method (C9.1, D2): output tokens, each message id counted once. Pass/fail cost uses LOOP-ONLY tokens A (R1, V1, R2, V2, R3); loop + one audit (B) is reported and never decides. "
          "No cost rule stops a run (D6); the cost clauses below are post-hoc. Limits: DROP R_LOOP > "
          f"{cfg['drop']['r_loop_above']} (L=1.25 on R_B), ADOPT R_LOOP <= {cfg['adopt']['r_loop_at_most']} (L=1.15 on R_B).", ""]
    L += ["## Rule table (Sonnet stratum)", "", "| Quantity | Baseline | Test | Rule |", "|---|---|---|---|",
          f"| runs completed / planned | 6 | {m['n_completed']} / {m['n_planned']} | >= {cfg['validity']['min_completed']} |",
          f"| BLK (mean blocking ids per audit, AUD+AUD2) | {f2(res['baseline']['B_BLK_recomputed'])} (recomputed over {res['baseline']['audits']} audits; stated 1.50) | {f2(m['BLK_T'])} | DROP >= {cfg['drop']['blk_t_at_least']}; ADOPT <= {b['b_blk']-cfg['adopt']['blk_t_drop']:.2f} |",
          f"| PASS (loop ended PASS) | 1.00 | {f2(m['PASS_T'])} | DROP < {cfg['drop']['pass_t_below']:.2f} |",
          f"| GROWTH % | {b['growth_base_pct']} | {f2(m['GROWTH_T'])} | DROP > {cfg['drop']['growth_above_pct']} |",
          f"| R_LOOP (A / {b['a_base']}) | 1.00 | {f2(m['R_LOOP'])} | DROP > {cfg['drop']['r_loop_above']}; ADOPT <= {cfg['adopt']['r_loop_at_most']} |",
          f"| R_B (loop + one audit / {b['b_base']}), reported only | 1.00 | {f2(m['R_B'])} | none |",
          f"| THEME ({'+'.join(cfg['theme']['themes'])} share of audits) | {f2(m['THEME_B'])} | {f2(m['THEME_T'])} | ADOPT <= {cfg['adopt']['theme_ratio_at_most']} x baseline |",
          f"| AUD mean / AUD2 mean | | {f2(m['AUD_mean'])} / {f2(m['AUD2_mean'])} | gap <= {cfg['validity']['aud_gap_max']} |",
          f"| R1 output tokens | {b['r1_tokens_base']} | {f2(m['R1_tokens'], 0)} | reported |", ""]
    L += ["## Per run", "", "| run | stratum | reviews | final | growth % | loop tokens (A) | one audit | AUD blocking ids | lint findings R1/R2/R3 |", "|---|---|---|---|---|---|---|---|---|"]
    for s in ("sonnet", "haiku"):
        for r in res["runs"][s]:
            ls = "/".join(str(r["lint"].get(f"LINT{i}", {}).get("findings", "-")) for i in (1, 2, 3))
            ab = "; ".join(f"{a['source'].split('/')[-1]}:{','.join(a['ids']) or '0'}[{','.join(a['themes'])}]" for a in r["audits"])
            L.append(f"| {r['run']} | {r['stratum']} | {r['reviews']} | {r['final_verdict']} | {f2(r['growth_pct'])} | {r['loop_tokens']} | {f2(r['one_audit_tokens'],0)} | {ab} | {ls} |")
    h = res["haiku"]
    L += ["", "## Haiku stratum (D3, never pooled)", "", f"status {h['status']}; " + "; ".join(f"{k}={v}" for k, v in h.items() if k != "status"), ""]
    L += ["## Validity notes", "", "- Lint handling by reviewers (confirmed / dismissed / ignored): count `LINT-` ids in each review report (round1/2/3.md) against the lint-<n>.md of that round.",
          f"- Extension (D4) used: {res['extension_used']}.", ""]
    if off.exists(): L += ["## Offline measurement (Phase O)", "", off.read_text()]
    (AB/"RESULTS.md").write_text("\n".join(L))

if __name__ == "__main__":
    import sys
    r = analyze()
    print(r["decision"], "|", "; ".join(r["reasons"]))
