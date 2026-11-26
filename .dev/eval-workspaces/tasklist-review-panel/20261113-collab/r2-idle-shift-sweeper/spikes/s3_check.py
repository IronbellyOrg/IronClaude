"""Smoke-test checks for DESIGN 6.5 AC-2, AC-2b and AC-4..AC-10 over the smoke rows written by s3-smoke.sh.

uv run --no-project python -I spikes/s3_check.py --stamp <file> --out <check.json> --panels EL2 SL2 HL2
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

R2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R2 / "py"))
from _lib import findings  # noqa: E402
from collab_metrics import check_schema  # noqa: E402

REPO = R2.parents[4]
EVAL = R2.parents[1] / "20261111-a1"
OUT = Path(os.environ.get("R2_OUT") or R2)
SBR = Path(os.environ.get("R2_SBR", "/tmp/evalsb-collab-r2"))
PKG = "TASK-WF-design-20261108-041415"
ROW_KEYS = ["schema", "row", "arm", "panel", "panel_collab", "models", "sweeper_model", "planning", "values_sha256", "opaque",
            "started_at", "finished_at", "found_14", "real_blocking_8", "judge_blocking", "wrong_blockers", "control_found_2",
            "control_wrong_blockers", "output_tokens", "elapsed_s", "overhead_pct", "per_package", "collab", "invalid"]


def jl(p):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, json.JSONDecodeError):
        return None


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rc(row):
    p = R2 / "spikes/out/s3" / f"{row}.rc"
    return int(p.read_text()) if p.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stamp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--panels", nargs="+", default=["EL2", "SL2", "HL2"])
    a = ap.parse_args()
    acs: dict[str, dict] = {}

    def ac(name, ok, **detail):
        acs[name] = {"pass": bool(ok), **detail}

    rows = [f"smoke-{p.lower()}-{c}" for p in a.panels for c in ("collab", "iso")]
    pds = {r: OUT / "runs" / r / PKG for r in rows}

    newer = subprocess.run(["find", str(REPO / "src"), str(EVAL), "-type", "f", "-newer", a.stamp], capture_output=True, text=True).stdout.split()
    hits = subprocess.run(["grep", "-rnE", r"src/superclaude|20261111-a1", str(R2 / "bin"), str(R2 / "py")], capture_output=True, text=True).stdout.splitlines()
    ac("AC-2", not newer, newer_files=newer[:20], read_path_references=[h.replace(str(R2) + "/", "") for h in hits])

    dropped, reask_bad = [], []
    for r, pd in pds.items():
        for m in sorted((pd / "reviews").glob("*.meta.json")) if pd.exists() else []:
            if ".attempt" in m.name:
                continue
            mm = jl(m) or {}
            if mm.get("dropped_lines", 0) != 0:
                dropped.append(f"{r}/{m.name}={mm.get('dropped_lines')}")
            if mm.get("reask") and mm.get("reask_model_ok") is not True:
                reask_bad.append(f"{r}/{m.name}")
        for rj in sorted((pd / "reviews").glob("*.reask.jsonl")) if pd.exists() else []:
            p = subprocess.run(["jq", "-s", "length", str(rj)], capture_output=True, text=True)
            if p.returncode != 0:
                reask_bad.append(f"{r}/{rj.name} unparseable")
    ac("AC-2b", not dropped and not reask_bad, dropped=dropped, reask_problems=reask_bad)

    if "EL2" in a.panels:
        r = "smoke-el2-collab"
        pd = pds[r]
        c = jl(pd / "collab.json") or {}
        ok_schema, err = True, None
        try:
            check_schema(c)
        except Exception as e:  # noqa: BLE001
            ok_schema, err = False, str(e)
        sw = c.get("sweeper") or {}
        recv = {k: v for k, v in (c.get("reviewers") or {}).items() if v.get("role") == "receiver"}
        seal_ok = []
        for rid, v in recv.items():
            if v["msgs_received"] >= 1:
                snap, hf = pd / f"board/snap/{rid}.jsonl", pd / f"board/snap/{rid}.sha256"
                seal_ok.append(bool(v["seal_t"] and v["first_delivery_t"] and v["seal_t"] <= v["first_delivery_t"] and snap.exists()
                                    and hf.exists() and sha(snap) == hf.read_text().strip() == v.get("seal_sha256")))
        ac("AC-4", rc(r) == 0 and ok_schema and sw.get("facts_posted", 0) + sw.get("facts_harvested", 0) >= 1
           and any(v["msgs_received"] >= 1 for v in recv.values()) and all(seal_ok)
           and all(v["msgs_received"] <= c.get("k", 0) for v in recv.values()) and all(v["stop_blocks"] == 0 for v in c["reviewers"].values()),
           exit=rc(r), schema_error=err, facts_posted=sw.get("facts_posted"), facts_harvested=sw.get("facts_harvested"),
           delivered={k: v["msgs_received"] for k, v in recv.items()}, k=c.get("k"), seal_before_delivery=seal_ok)
        merged = (pd / "merged-1.md").read_text() if (pd / "merged-1.md").exists() else ""
        nrev = len(re.findall(r"^- t[0-9a-z]+-\d+: report ", merged, re.M))
        row = jl(OUT / f"results/{r}.json") or {}
        opaque = (OUT / f"runs/{r}/opaque").read_text().strip() if (OUT / f"runs/{r}/opaque").exists() else "?"
        scores = list((OUT / "scoring" / opaque / PKG).glob("*/score.json"))
        anon = list((OUT / "scoring" / opaque / PKG).glob("*/merged-anon.md"))
        new_arms = subprocess.run(["find", str(EVAL / "arms"), "-newer", a.stamp], capture_output=True, text=True).stdout.split()
        ac("AC-5", nrev == 3 and anon and scores and not new_arms and all(k in row for k in ROW_KEYS),
           reviewers_in_merge=nrev, anon=[str(x.relative_to(OUT)) for x in anon], scores=[str(x.relative_to(OUT)) for x in scores],
           new_under_eval_arms=new_arms[:10], missing_row_keys=[k for k in ROW_KEYS if k not in row])
        au = jl(pd / "audit.json") or {}
        ac("AC-6", au.get("ok") is True and au.get("gt_checked") is True, violations=au.get("violations"))
        r = "smoke-el2-iso"
        pd = pds[r]
        c = jl(pd / "collab.json") or {}
        runid = (OUT / f"runs/{r}/runid").read_text().strip() if (OUT / f"runs/{r}/runid").exists() else "?"
        metas = [jl(m) or {} for m in (pd / "reviews").glob("*.attempt*.meta.json")]
        own = True
        for rid in (c.get("reviewers") or {}):
            res = findings().parse_block((pd / f"reviews/{rid}.final.md").read_text()) if (pd / f"reviews/{rid}.final.md").exists() else {"findings": []}
            own &= all(f.get("origin") == "own" for f in res["findings"])
        counters = sum(v["msgs_received"] + v["peer_lines"] + v["late"] + v["hook_calls"] for v in (c.get("reviewers") or {}).values())
        ac("AC-7", not (pd / "board").exists() and not (SBR / "board" / runid).exists() and metas and not any(m.get("settings") for m in metas)
           and not (pd / "sweeper/sw-1.json").exists() and own and counters == 0 and c.get("sweeper") is None
           and all("finish_would_fire" in v for v in (c.get("reviewers") or {}).values()),
           exit=rc(r), settings_used=[m.get("settings") for m in metas], all_own=own, counters=counters,
           note="test_launch_command_diff.py is part of the pytest run")
    others = [p for p in a.panels if p != "EL2"]
    if others:
        det = {}
        ok = True
        for p in others:
            for cs in ("collab", "iso"):
                r = f"smoke-{p.lower()}-{cs}"
                pd = pds[r]
                c = jl(pd / "collab.json") or {}
                row = jl(OUT / f"results/{r}.json") or {}
                mok = [v["model_ok"] for v in (c.get("reviewers") or {}).values()]
                if cs == "collab":
                    sw = c.get("sweeper") or {}
                    mok.append(sw.get("model_ok") is True or sw.get("skipped_late") or sw.get("skipped_k0"))
                good = rc(r) == 0 and mok and all(mok) and row.get("sweeper_model") == "muse-ember-1.0" and c.get("k") is not None
                det[r] = {"exit": rc(r), "model_ok": mok, "sweeper_model": row.get("sweeper_model"), "k": c.get("k")}
                ok &= bool(good)
        ac("AC-8", ok, rows=det)
    bad, fb = [], []
    for r, pd in pds.items():
        for m in (pd / "reviews").glob("*.attempt*.meta.json") if pd.exists() else []:
            mm = jl(m) or {}
            o, e = (mm.get("observed_model") or "").lower(), (mm.get("expected_model") or "").lower()
            if o not in (e, e + "-build"):
                bad.append(f"{r}/{m.name}: {o} != {e}")
        sm = jl(pd / "sweeper/sw-1.meta.json")
        if sm and sm.get("observed_model") is not None and sm["observed_model"].lower() != sm["model"].lower():
            bad.append(f"{r}/sweeper: {sm['observed_model']}")
        fb += [str(x) for x in pd.rglob("*fallback*")] if pd.exists() else []
    ac("AC-9", not bad and not fb, mismatches=bad, fallback_files=fb)
    over = []
    for r, pd in pds.items():
        c = jl(pd / "collab.json") or {}
        v = jl(pd / "values.json") or {}
        if c and v and c["elapsed_s"] > v["hang_s"] and not c.get("slo_breach"):
            over.append(r)
    ac("AC-10", not over, elapsed={r: (jl(pd / "collab.json") or {}).get("elapsed_s") for r, pd in pds.items()},
       slo_breach={r: (jl(pd / "collab.json") or {}).get("slo_breach") for r, pd in pds.items()}, over_without_breach=over)
    res = {"rows": rows, "acs": acs, "all_pass": all(x["pass"] for x in acs.values())}
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v["pass"] for k, v in acs.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
