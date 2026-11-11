"""Analysis for PN3: gate, adaptive extension (D4), RESULTS.md. Decision constants come from decision_rules.json (D1-D4)."""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decision as DEC  # noqa: E402

PREDICTION = """Pre-registered prediction for the live arm (see the validity note on timing): the stop rule will often demand another whole-document panel round,
and with the cap of 3 reviews many runs will ESCALATE. Original plan figure: R_TOK about 3.3 on a loop-plus-audit basis, which D6 converts
to R_LOOP = (3.3 x 169,468 - 69,044) / 100,424 = 4.88 (the DROP limit; the ADOPT limit 2.5 converts to 3.53). Loop-only forecast (a forecast for scheduling, not a limit):
about 200,000 output tokens per panel round x 2 plus about 90,000 for revises and re-reviews is about 490,000 per run, so R_LOOP is about 4.9, on the DROP edge."""


def offline():
    p = HERE / "offline/falsification.json"
    return json.load(open(p)) if p.exists() else None


def shadow():
    p = HERE / "shadow.json"
    return json.load(open(p)) if p.exists() else {"ran": False}


def gate_result():
    """Gate for the live arm: F1 SUPPORTED, and F3 CALIBRATED if PN1 data exists."""
    f = offline(); sh = shadow()
    f1 = f["verdict"] if f else "missing"
    f3 = sh.get("verdict") if sh.get("ran") else "not run"
    ok = f1 == "SUPPORTED" and (f3 in ("CALIBRATED", "not run"))
    return {"pass": ok, "F1": f1, "F3": f3, "note": "F3 not run (no PN1 data): gate rests on F1 alone" if f3 == "not run" else ""}


def gate():
    g = gate_result(); json.dump(g, open(HERE / "gate.json", "w"), indent=1)
    print("GATE", "PASS" if g["pass"] else "FAIL", g); return g


def live_runs():
    import harness as H
    out = {"sonnet": [], "haiku": []}
    if not H.RUNS.exists(): return out
    toks = H.step_tokens()
    for d in sorted(p for p in H.RUNS.iterdir() if (p / "state.json").exists()):
        r = H.run_result(d.name, {k: v for k, v in toks.items() if k[0] == d.name})
        out[r["stratum"]].append(r)
    return out


def sonnet_state(sonnet):
    primary = [r for r in sonnet if int(r["run"].split("-r")[1]) <= DEC.RULES["sonnet"]["n"]]
    ext = [r for r in sonnet if int(r["run"].split("-r")[1]) > DEC.RULES["sonnet"]["n"]]
    s6 = DEC.summarize(primary); d6, why6 = DEC.decide_sonnet(s6)
    marker = HERE / "extension.json"
    extended = marker.exists()
    if d6 == "INCONCLUSIVE" and extended and ext:
        s9 = DEC.summarize(primary + ext); d9, why9 = DEC.decide_sonnet(s9)
        return {"n6": (s6, d6, why6), "final": (s9, d9, why9), "extended": True, "need_extension": False}
    return {"n6": (s6, d6, why6), "final": (s6, d6, why6), "extended": extended,
            "need_extension": DEC.extension_needed(d6, len(primary), extended) and len(primary) > 0}


def extend():
    import harness as H
    live = live_runs()
    if not live["sonnet"]:
        print("no Sonnet runs yet"); return
    st = sonnet_state(live["sonnet"])
    if not st["need_extension"]:
        print("extension not needed (or already used):", st["n6"][1], "extended" if st["extended"] else ""); return
    (HERE / "extension.json").write_text(json.dumps({"reason": st["n6"], "extra": DEC.RULES["extension"]["extra_sonnet_replicates"]}, default=str))
    H.build(DEC.RULES["extension"]["extra_sonnet_replicates"], "sonnet", start=DEC.RULES["sonnet"]["n"] + 1)
    print("D4 extension started once: 3 more Sonnet replicates added; recompute with n=9 and then decide; no second extension.")


def fmt(x, nd=2):
    return "-" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def table(runs):
    lines = ["| run | decision | reviews | panel rounds | growth % | A loop tokens | B loop+audit | blk AUD | blk AUD2 | stops (unseen_upper95) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in runs:
        a = r["loop_tokens"]; b = (a + r["audit_tokens"]) if a is not None and r["audit_tokens"] is not None else None
        stops = ", ".join(f"r{s['review']}:{'stop' if s['stop'] else 'go'}({s['unseen_upper95']})" for s in r["stops"]) or "-"
        blk = r["blk"] + [None] * (2 - len(r["blk"]))
        lines.append(f"| {r['run']} | {r['decision']} | {r['reviews']} | {r['panel_rounds']} | {fmt(r['growth_pct'])} | {fmt(a, 0)} | {fmt(b, 0)} | {fmt(blk[0], 0)} | {fmt(blk[1], 0)} | {stops} |")
    return "\n".join(lines)


def analyze():
    f = offline(); sh = shadow(); g = gate_result(); live = live_runs()
    out = ["# PN3 results: capture-recapture estimate as a stop rule", ""]
    off_verdict = f["verdict"] if f else "MISSING"
    if not live["sonnet"]:
        live_line = "NOT RUN (gate)" if not g["pass"] else "NOT RUN (gate passed, runs not launched yet)"
        sdec = None
    else:
        st = sonnet_state(live["sonnet"]); sdec = st["final"][1]
        hb = DEC.load_haiku_baseline(); hsum = DEC.summarize(live["haiku"]) if live["haiku"] else {"n_completed": 0}
        hstat, hdet = DEC.decide_haiku(hsum, hb) if live["haiku"] else ("pending", "no Haiku runs")
        live_line = DEC.final_line(sdec, hstat, st["extended"])
        if st["need_extension"]: live_line = "INCONCLUSIVE at n=6: D4 extension required (run `harness.py extend`)"
    out.append(f"DECISION: {off_verdict} ; live: {live_line}")
    out += ["", PREDICTION, ""]
    out.append(f"Gate for the live arm c3: **{'PASS' if g['pass'] else 'FAIL'}** (F1 {g['F1']}; F3 {g['F3']}). {g['note']}")
    out += ["", "## Offline results (O1-O3)", ""]
    if f:
        out += [(HERE / "offline/falsification.md").read_text(), "", f"Catalog: {(pathlib.Path(DEC.HERE) / '..' / 'catalog' / 'BUILD-NOTES.md').resolve()}", ""]
    out += ["## Shadow calibration (F3)", "", (HERE / "shadow.md").read_text() if (HERE / "shadow.md").exists() else "Not run.", ""]
    out += ["## Live arm c3", ""]
    if not live["sonnet"] and not live["haiku"]:
        out.append("Not run: " + ("the gate failed, so no workers were launched." if not g["pass"] else "no run directories exist yet."))
    else:
        c = DEC.RULES
        out += [f"Constants: decision_rules.json (A_BASE {c['A_BASE']:,}, one audit {c['AUD_BASE']:,}, B_BASE {c['B_BASE']:,}, B_BLK {c['B_BLK']}). Token pass/fail uses A (loop only, audits excluded); B (loop + one audit) is reported and never decides.", ""]
        if live["sonnet"]:
            st = sonnet_state(live["sonnet"])
            out += ["### Sonnet stratum (decides)", "", table(live["sonnet"]), ""]
            for name, key in (("n=6", "n6"), ("final", "final")):
                s, d, why = st[key]
                out += [f"- {name}: completed {s['n_completed']}/{s['n_total']}; BLK_T {fmt(s['BLK_T'])}; PASS_T {fmt(s['PASS_T'])}; GROWTH_T {fmt(s['GROWTH_T'])}%; "
                        f"R_LOOP {fmt(s['R_LOOP'])} (A_T {fmt(s['A_T'], 0)}); R_B {fmt(s['R_B'])} (reported only); AUD mean {fmt(s['AUD_mean'])}, AUD2 mean {fmt(s['AUD2_mean'])} -> **{d}** {'; '.join(why)}"]
            out.append(f"- D4 extension used: {st['extended']}")
        if live["haiku"]:
            hb = DEC.load_haiku_baseline(); hs = DEC.summarize(live["haiku"]); hstat, hdet = DEC.decide_haiku(hs, hb)
            out += ["", "### Haiku stratum (secondary, never pooled)", "", table(live["haiku"]), "", f"- Haiku result: {hstat}; {hdet}"]
        out += ["", "### Residual decomposition", "See per-run audit blocking ids above; map them to catalog clusters with catmap.audit_findings and the run ledger rows (captured by a panel round versus never captured)."]
    out += ["", "## Validity notes", "",
            "- The prediction above was written into this script after the offline phases had run (the plan asked for it before analysis); it concerns the live arm, which has not run.",
            "- Cost policy (D6): cost is judged only after runs complete; nothing in the harness stops, truncates or skips a run on token or dollar cost.",
            "- The 12 primary occasions are one model with one prompt, so detection is correlated and every estimator here is a lower bound.",
            "- Defects have very unequal detection probability (cluster capture counts in the profile), which is why Mh-type estimators (Chao2, Jackknife-1) are used.",
            "- The reference truth (the catalog) is itself built from the same kind of review: 21 audits and 15 first reviews, adjudicated by one reader; arm-1 reports are a different instrument and add 10 clusters the primary occasions never saw.",
            "- Dedupe overrides: the sensitivity run ignoring them is in the offline section.",
            "- Re-reviews are scoped to changed lines and are not capture occasions (C7).",
            "- Token method (C9.1): output tokens, each message id counted once (max over its lines); D2: the decision uses loop-only tokens.",
            "- Haiku stratum: panel composition unchanged (sonnet anchor plus haiku stand-ins); the non-panel loop workers (reviser, scoped re-reviewer) run on Haiku; audits always Sonnet; never pooled with Sonnet."]
    (HERE / "RESULTS.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[:6]))


if __name__ == "__main__":
    {"gate": gate, "extend": extend, "analyze": analyze}[sys.argv[1] if len(sys.argv) > 1 else "analyze"]()
