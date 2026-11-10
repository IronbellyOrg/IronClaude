#!/usr/bin/env python3
"""Phase S: shadow calibration of the capture-recapture estimate on PN1's live panel runs (zero workers, read-only on $SP/p13/ab1).
Usage: shadow.py [--ab1 DIR] [--out FILE] [--estimate-cmd uv|lib]"""
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "offline"))
import catmap  # noqa: E402
import common as c  # noqa: E402
import ledger_lite as L  # noqa: E402

SP = c.SP
AB1 = SP / "p13/ab1"
CLONE = SP / "p13/clones/pn3"
REVIEW = f"{c.D}/review"


def estimate(cap, open_blocking=0):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(cap, fh)
        name = fh.name
    r = subprocess.run(["uv", "run", "--project", str(CLONE), "superclaude", "review", "estimate", name, "--blocking-only",
                        "--open-blocking", str(open_blocking)], capture_output=True, text=True)
    pathlib.Path(name).unlink()
    if r.returncode:
        raise RuntimeError(r.stderr)
    return json.loads(r.stdout)


def completed_runs(ab1):
    out = []
    for d in sorted(pathlib.Path(ab1).glob("runs/b1-r*")):
        sf = d / "state.json"
        if not sf.exists():
            continue
        st = json.load(open(sf))
        if "AUD" in st.get("done", []) and "AUD2" in st.get("done", []) and (d / "ws" / REVIEW / "ledger.json").exists():
            out.append(d)
    return out


def analyse_run(d, est=estimate, cat=None):
    lg = json.load(open(d / "ws" / REVIEW / "ledger.json"))
    rows = lg["rows"]
    r1 = next(r for r in lg["rounds"] if r["n"] == 1)
    occ = [x["reviewer_id"] for x in r1["reviewers"]]
    cap = L.Ledger(data=lg).capture(1, str(d / "ws" / REVIEW / "ledger.json"))
    e = est(cap, 0)
    # round-1 rows -> catalog clusters
    r1rows = [r for r in rows if any(m["round"] == 1 for m in r["members"])]
    mapped = {}
    for r in r1rows:
        text = " ".join(filter(None, [r["anchor"], r.get("anchor2"), " ".join(r.get("refs", []))]))
        mapped[r["lid"]] = catmap.map_to_cluster([r["anchor"]] + ([r["anchor2"]] if r.get("anchor2") else []), text, cat)
    blocking_r1 = [r for r in r1rows if any(m["round"] == 1 and m["blocking"] for m in r["members"])]
    not_fixed = [r for r in blocking_r1 if r["status"] not in ("resolved", "resolved_check")]
    # observed residual: distinct non-revision-introduced clusters among both audits' blocking findings
    obs = set()
    n_new = 0
    for step in ("aud", "aud2"):
        p = d / step / "ws" / REVIEW / "audit.md"
        if not p.exists():
            continue
        for f in catmap.audit_findings(p):
            cid = catmap.map_to_cluster(f["quotes"], f["text"], cat)
            if cid:
                obs.add(cid)
            else:
                obs.add(f"N:{step}:{f['fid']}")
                n_new += 1
    pred = {"chao2": e["chao2"]["ci95"][1] - e["S_obs"], "jack1": e["jackknife1"]["ci95"][1] - e["S_obs"]}
    upper = e["unseen_upper95"] + len(not_fixed)
    # correlated blindness: occasions are sonnet (t1b) and haiku stand-ins
    sets = {o: {k["key"] for k in cap["defects"] if o in k["captured_by"] and k["blocking"]} for o in occ}
    models = {x["reviewer_id"]: x.get("model") for x in r1["reviewers"]}
    hk = [o for o in occ if "haiku" in str(models[o])]
    so = [o for o in occ if o not in hk]
    union = lambda ids: set().union(*[sets[o] for o in ids]) if ids else set()
    return {"run": d.name, "occasions": occ, "S_obs": e["S_obs"], "Q1": e["Q"]["1"], "Q2": e["Q"]["2"], "chao2": e["chao2"]["N"],
            "jack1": e["jackknife1"]["N"], "unseen_upper95": e["unseen_upper95"], "blocking_r1_rows": len(blocking_r1),
            "not_fixed": len(not_fixed), "predicted_upper_remaining": upper, "observed_residual": len(obs), "new_clusters_in_audits": n_new,
            "calibrated": len(obs) <= upper, "haiku_union": len(union(hk)), "sonnet_union": len(union(so)),
            "haiku_only": len(union(hk) - union(so)), "sonnet_only": len(union(so) - union(hk))}


def main(ab1=AB1, out=None, est=estimate):
    runs = completed_runs(ab1)
    out = pathlib.Path(out or (HERE / "shadow.md"))
    if len(runs) < 5:
        out.write_text(f"# Shadow calibration (F3)\n\nNot run: {len(runs)} completed PN1 runs found under {ab1} (need at least 5 with both audits ingested).\n")
        (HERE / "shadow.json").write_text(json.dumps({"ran": False, "completed": len(runs)}))
        print("shadow: not enough runs", len(runs))
        return None
    res = [analyse_run(d, est) for d in runs]
    ok = sum(r["calibrated"] for r in res)
    verdict = "CALIBRATED" if ok >= 5 else "NOT CALIBRATED"
    lines = ["# Shadow calibration of the stop rule on PN1's live panel (F3)", "",
             f"{len(res)} completed runs. CALIBRATED if observed residual <= predicted upper remaining in at least 5 runs: {ok}/{len(res)} -> **{verdict}**.", "",
             "| run | S_obs | Q1 | Q2 | Chao2 N | Jack1 N | unseen_upper95 | blocking rows not fixed | predicted upper remaining | observed residual | calibrated |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        lines.append(f"| {r['run']} | {r['S_obs']} | {r['Q1']} | {r['Q2']} | {r['chao2']} | {r['jack1']} | {r['unseen_upper95']} | {r['not_fixed']} | {r['predicted_upper_remaining']} | {r['observed_residual']} | {'yes' if r['calibrated'] else 'no'} |")
    lines += ["", "## Correlated blindness (haiku stand-ins versus the sonnet anchor, round 1, blocking clusters)", "",
              "| run | haiku union | sonnet union | haiku only | sonnet only |", "|---|---|---|---|---|"]
    for r in res:
        lines.append(f"| {r['run']} | {r['haiku_union']} | {r['sonnet_union']} | {r['haiku_only']} | {r['sonnet_only']} |")
    lines += ["", "Note: three of the four reviewers are the same model (haiku stand-ins), so underestimation of the remainder is expected."]
    out.write_text("\n".join(lines) + "\n")
    (HERE / "shadow.json").write_text(json.dumps({"ran": True, "verdict": verdict, "calibrated": ok, "n": len(res), "runs": res}, indent=1))
    print(verdict, ok, len(res))
    return verdict


if __name__ == "__main__":
    a = sys.argv[1:]
    main(ab1=a[a.index("--ab1") + 1] if "--ab1" in a else AB1, out=a[a.index("--out") + 1] if "--out" in a else None)
