"""6.4-style smoke checks (DESIGN 6.5 AC-2, AC-2b, AC-4, AC-5, AC-6, AC-9, AC-10) for ONE collaboration row run with
TIME_CAP_EXCEPTION=1, plus the override's own checks OV-1..OV-3. The AC numbers keep their DESIGN meaning; AC-4 is the EL2 form.

uv run --no-project python -I spikes/s3_exception_check.py --stamp <file> --row <row> --out <check.json>
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
from collab_metrics import check_schema  # noqa: E402

REPO = R2.parents[4]
EVAL = R2.parents[1] / "20261111-a1"
OUT = Path(os.environ.get("R2_OUT") or R2)
PKG = "TASK-WF-design-20261108-041415"
ROW_KEYS = ["schema", "row", "arm", "panel", "panel_collab", "models", "sweeper_model", "planning", "values_sha256", "opaque",
            "started_at", "finished_at", "found_14", "real_blocking_8", "judge_blocking", "wrong_blockers", "control_found_2",
            "control_wrong_blockers", "output_tokens", "elapsed_s", "overhead_pct", "per_package", "collab", "invalid",
            "time_cap_exception"]


def jl(p):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, json.JSONDecodeError):
        return None


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stamp", required=True)
    ap.add_argument("--row", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    acs: dict[str, dict] = {}

    def ac(name, ok, **detail):
        acs[name] = {"pass": bool(ok), **detail}

    r = a.row
    pd = OUT / "runs" / r / PKG
    rcf = R2 / "spikes/out/s3-exception" / f"{r}.rc"
    rc = int(rcf.read_text()) if rcf.exists() else None
    c = jl(pd / "collab.json") or {}
    v = jl(pd / "values.json") or {}
    row = jl(OUT / f"results/{r}.json") or {}

    newer = subprocess.run(["find", str(REPO / "src"), str(EVAL), "-type", "f", "-newer", a.stamp], capture_output=True, text=True).stdout.split()
    ac("AC-2", not newer, newer_files=newer[:20])
    dropped, reask_bad = [], []
    for m in sorted((pd / "reviews").glob("*.meta.json")):
        if ".attempt" in m.name:
            continue
        mm = jl(m) or {}
        if mm.get("dropped_lines", 0) != 0:
            dropped.append(f"{m.name}={mm.get('dropped_lines')}")
        if mm.get("reask") and mm.get("reask_model_ok") is not True:
            reask_bad.append(m.name)
    ac("AC-2b", not dropped and not reask_bad, dropped=dropped, reask_problems=reask_bad)

    ok_schema, err = True, None
    try:
        check_schema(c)
    except Exception as e:  # noqa: BLE001
        ok_schema, err = False, str(e)
    sw = c.get("sweeper") or {}
    recv = {k: x for k, x in (c.get("reviewers") or {}).items() if x.get("role") == "receiver"}
    seal_ok = []
    for rid, x in recv.items():
        if x["msgs_received"] >= 1:
            snap, hf = pd / f"board/snap/{rid}.jsonl", pd / f"board/snap/{rid}.sha256"
            seal_ok.append(bool(x["seal_t"] and x["first_delivery_t"] and x["seal_t"] <= x["first_delivery_t"] and snap.exists()
                                and hf.exists() and sha(snap) == hf.read_text().strip() == x.get("seal_sha256")))
    ac("AC-4", rc == 0 and ok_schema and sw.get("facts_posted", 0) + sw.get("facts_harvested", 0) >= 1
       and any(x["msgs_received"] >= 1 for x in recv.values()) and all(seal_ok)
       and all(x["msgs_received"] <= c.get("k", 0) for x in recv.values()) and all(x["stop_blocks"] == 0 for x in c["reviewers"].values()),
       exit=rc, schema_error=err, facts_posted=sw.get("facts_posted"), facts_harvested=sw.get("facts_harvested"),
       delivered={k: x["msgs_received"] for k, x in recv.items()}, k=c.get("k"), seal_before_delivery=seal_ok)
    merged = (pd / "merged-1.md").read_text() if (pd / "merged-1.md").exists() else ""
    nrev = len(re.findall(r"^- t[0-9a-z]+-\d+: report ", merged, re.M))
    opaque = (OUT / f"runs/{r}/opaque").read_text().strip() if (OUT / f"runs/{r}/opaque").exists() else "?"
    scores = list((OUT / "scoring" / opaque / PKG).glob("*/score.json"))
    anon = list((OUT / "scoring" / opaque / PKG).glob("*/merged-anon.md"))
    new_arms = subprocess.run(["find", str(EVAL / "arms"), "-newer", a.stamp], capture_output=True, text=True).stdout.split()
    ac("AC-5", nrev == 3 and anon and scores and not new_arms and all(k in row for k in ROW_KEYS),
       reviewers_in_merge=nrev, anon=[str(x.relative_to(OUT)) for x in anon], scores=[str(x.relative_to(OUT)) for x in scores],
       new_under_eval_arms=new_arms[:10], missing_row_keys=[k for k in ROW_KEYS if k not in row])
    au = jl(pd / "audit.json") or {}
    ac("AC-6", au.get("ok") is True and au.get("gt_checked") is True, violations=au.get("violations"))
    bad = []
    for m in (pd / "reviews").glob("*.attempt*.meta.json"):
        mm = jl(m) or {}
        o, e = (mm.get("observed_model") or "").lower(), (mm.get("expected_model") or "").lower()
        if o not in (e, e + "-build"):
            bad.append(f"{m.name}: {o} != {e}")
    sm = jl(pd / "sweeper/sw-1.meta.json") or {}
    if sm.get("observed_model") is not None and sm["observed_model"].lower() != sm["model"].lower():
        bad.append(f"sweeper: {sm['observed_model']}")
    fb = [str(x) for x in pd.rglob("*fallback*")]
    ac("AC-9", not bad and not fb and sm.get("model_ok") is True and row.get("sweeper_model") == "muse-ember-1.0",
       mismatches=bad, fallback_files=fb, sweeper_model_ok=sm.get("model_ok"))
    ac("AC-10", bool(c) and (c["elapsed_s"] <= v.get("hang_s", 0) or c.get("slo_breach")),
       elapsed_s=c.get("elapsed_s"), hang_s=v.get("hang_s"), slo_breach=c.get("slo_breach"))
    # the override's own checks
    pp = (row.get("per_package") or {}).get(PKG) or {}
    ac("OV-1", row.get("time_cap_exception") is True and c.get("time_cap_exception") is True and c.get("time_cap_exception_applied") is True
       and v.get("k") == 1 and (v.get("time_cap_exception") or {}).get("k_measured") == 0 and c.get("k") == 1,
       row_stamp=row.get("time_cap_exception"), values_k=v.get("k"), values_stamp=v.get("time_cap_exception"))
    ac("OV-2", all(pp.get(k) is not None for k in ("B_A1", "elapsed_s", "elapsed_over_baseline", "k", "k_measured", "messages_delivered"))
       and pp.get("time_cap_exception") is True and pp["elapsed_over_baseline"] == c.get("elapsed_over_baseline"),
       columns={k: pp.get(k) for k in ("B_A1", "elapsed_s", "elapsed_over_baseline", "k", "k_measured", "messages_delivered")})
    ac("OV-3", sm.get("skipped_k0") is False and sm.get("skipped_late") is False and sm.get("start_ms") is not None,
       sweeper_started=sm.get("start_ms") is not None, skipped_k0=sm.get("skipped_k0"), skipped_late=sm.get("skipped_late"))
    res = {"row": r, "acs": acs, "all_pass": all(x["pass"] for x in acs.values())}
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: x["pass"] for k, x in acs.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
