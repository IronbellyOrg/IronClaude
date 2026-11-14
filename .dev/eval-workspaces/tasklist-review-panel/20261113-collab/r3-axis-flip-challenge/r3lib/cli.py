"""argparse dispatcher for the Python subcommands (section 2.3)."""

from __future__ import annotations

import argparse
import glob
import json
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from r3lib import digest, findings_io, metrics, paths, values  # noqa: E402

PIN_SOURCES = {
    "judge-one.sh": paths.EVAL / "tools/tmp-scripts/judge-one.sh",
    "findings.py": paths.REPO / "src/superclaude/cli/review/findings.py",
    "ledger.py": paths.REPO / "src/superclaude/cli/review/ledger.py",
    "merge_cmd.py": paths.REPO / "src/superclaude/cli/review/merge_cmd.py",
}


def _pin_hashes(config_dir: Path) -> dict:
    h = {k: values.sha256_file(p) for k, p in PIN_SOURCES.items()}
    for p in sorted(config_dir.iterdir()):
        if p.is_file() and p.name != "pins.json":
            h["config/" + p.name] = values.sha256_file(p)
    return h


def cmd_pin(a) -> int:
    cdir = Path(a.config_dir) if a.config_dir else paths.CONFIG
    pf = cdir / "pins.json"
    now = _pin_hashes(cdir)
    if a.check:
        old = paths.load_json(pf)["sha256"]
        bad = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
        if bad:
            print("E_PIN_MISMATCH " + " ".join(bad))
            return 1
        print("pins ok")
        return 0
    head = subprocess.run(
        ["git", "-C", str(paths.REPO), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    paths.write_json(pf, {"repo_commit": head, "sha256": now})
    print(f"pinned {len(now)} files")
    return 0


def cmd_normalize(a) -> int:
    text = Path(a.inp).read_text(encoding="utf-8")
    out, info = findings_io.normalise_text(text)
    Path(a.out).write_text(out, encoding="utf-8")
    paths.write_json(a.json, info)
    return info["exit"]


def cmd_digest(a) -> int:
    rc, out = digest.build(a.pkgdir, a.rid, a.t_launch, a.start_cost)
    print(json.dumps(out))
    return rc


def cmd_combine(a) -> int:
    pd = Path(a.pkgdir)
    rv = pd / "reviews"
    p1 = (rv / f"{a.rid}.p1.md").read_text(encoding="utf-8")
    p2m = metrics._j(rv / f"{a.rid}.p2.meta.json", {}) or {}
    lines, log = (
        [],
        {
            "p2_lines_valid": 0,
            "p2_lines_dropped": 0,
            "p2_lines_salvaged": 0,
            "answered": [],
        },
    )
    stream = p2m.get("final_stream")
    if stream and p2m.get("model_ok", False):
        reask = p2m.get("p2reask_stream")
        lines, log = findings_io.extract_p2_lines(
            pd / stream, (pd / reask) if reask else None
        )
    elif stream:
        log["p2_model_mismatch"] = True
    try:
        text, clog = findings_io.combine(p1, lines)
        norm1, _ = findings_io.combine(p1, [])
    except findings_io.CombineError as exc:
        print(str(exc), file=sys.stderr)
        paths.write_json(rv / f"{a.rid}.combine.json", {"error": str(exc)})
        return 7
    (rv / f"{a.rid}.md").write_text(text, encoding="utf-8")
    (rv / f"{a.rid}.p1norm.md").write_text(norm1, encoding="utf-8")
    n_launched = int(p2m.get("n_launched", 0) or 0)
    answered = [c for c in log.get("answered", []) if 1 <= c <= n_launched]
    out = {
        "p1_lines": clog["p1_lines"],
        "p2_lines_valid": clog["p2_lines_combined"],
        "p2_lines_dropped": log["p2_lines_dropped"],
        "p2_drop_msgs": log.get("p2_drop_msgs", []),
        "p2_lines_salvaged": log["p2_lines_salvaged"],
        "p2_dupe_dropped": clog["p2_dupe_dropped"],
        "p2_self_reference": clog["p2_self_reference"],
        "p2x_renames": clog["p2x_renames"],
        "challenges_answered": len(answered),
        "n_launched": n_launched,
        "p2_model_mismatch": bool(log.get("p2_model_mismatch", False)),
    }
    paths.write_json(rv / f"{a.rid}.combine.json", out)
    return 0


def cmd_p2check(a) -> int:
    """Phase-2 lines that fail the parser after normalisation (7.4 re-ask trigger)."""
    _, log = findings_io.extract_p2_lines(a.stream)
    msgs = log["p2_drop_msgs"]
    print(
        "\n".join(f"line {d['id']}: {d['msg']}" for d in msgs[:10])
        + (f"\n... and {len(msgs) - 10} more" if len(msgs) > 10 else "")
    )
    return 3 if msgs else 0


def cmd_reask_errors(a) -> int:
    info = paths.load_json(a.json)
    errs = info.get("errors", [])
    lines = [f"line {e['line']}: {e['msg']}" for e in errs[:10]]
    if len(errs) > 10:
        lines.append(f"... and {len(errs) - 10} more")
    print("\n".join(lines))
    return 0


def cmd_errcount(a) -> int:
    print(findings_io.error_count(Path(a.inp).read_text(encoding="utf-8")))
    return 0


def cmd_capture(a) -> int:
    print(json.dumps(metrics.capture_sessions(a.pkgdir)))
    return 0


def cmd_judge_ok(a) -> int:
    return 0 if metrics.judge_ok(Path(a.dir)) else 1


def cmd_metrics(a) -> int:
    metrics.collab_json(a.pkgdir)
    return 0


def cmd_audit(a) -> int:
    out = metrics.audit(a.pkgdir)
    return 8 if out["violations"] else 0


def cmd_anon(a) -> int:
    text, rep = metrics.anonymise(Path(a.inp).read_text(encoding="utf-8"))
    if rep["residue"]:
        print("E_ANON_RESIDUE " + " ".join(rep["residue"]), file=sys.stderr)
        return 6
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(text, encoding="utf-8")
    return 0


def cmd_result(a) -> int:
    row = metrics.result_row(a.rundir)
    print(
        json.dumps(
            {
                k: row[k]
                for k in (
                    "run_id",
                    "found14",
                    "real_blocking8",
                    "control_found2",
                    "judge_ok",
                    "invalid_pkgs",
                    "contaminated",
                )
            }
        )
    )
    return 0


def cmd_values_freeze(a) -> int:
    rr = paths.runs_root()
    v = values.freeze(a.panel, [rr / r for r in a.runs])
    print(json.dumps(v["turn_p90"]))
    return 0


def cmd_values_show(a) -> int:
    v, sha = values.load(
        a.panel, smoke=a.smoke, spike4=a.spike4, prefer_frozen=bool(a.tce)
    )
    out = {"values": v, "sha256": sha}
    if a.tce:  # time-cap exception: per-package widened timers (OVERRIDE.md)
        out["tce"] = values.tce_all(a.tce, a.panel, v)
    print(json.dumps(out))
    return 0


def cmd_summarize(a) -> int:
    f = Path(a.results) if a.results else paths.results_root() / "results.jsonl"
    rows = (
        [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
        if f.exists()
        else []
    )
    vf = paths.values_file(a.panel)
    b_f = (
        {k: v["B_f"] for k, v in paths.load_json(vf)["packages"].items()}
        if vf.exists()
        else None
    )
    s = metrics.summarize(rows, a.panel, b_f)
    print(json.dumps(s, indent=1))
    print(metrics.summary_table(s))
    return 0


def _rows(pattern: str) -> list[tuple[str, list[dict], str]]:
    out = []
    for p in sorted(glob.glob(pattern)):
        pkg = next((x for x in Path(p).parts if x.startswith("TASK-WF-")), None)
        if not pkg:
            continue
        out.append(
            (p, findings_io.valid_findings(Path(p).read_text(encoding="utf-8")), pkg)
        )
    return out


def cmd_calibrate_surface(a) -> int:
    routing = paths.cfg("routing.json")
    rx = routing["surface_regex"]
    import re

    by_model: dict[str, list] = {}
    samples = []
    for p, fs, pkg in _rows(a.rows):
        meta = metrics._j(Path(p[:-3] + ".meta.json"), {}) or {}
        model = meta.get("expected_model") or Path(p).stem
        for f in fs:
            hit = bool(re.search(rx, f.get("claim", "")))
            by_model.setdefault(model, []).append(hit)
            samples.append((hit, model, f.get("claim", "")))
    rng = random.Random(1)
    hits = [s for s in samples if s[0]]
    miss = [s for s in samples if not s[0]]
    out = {
        "share": {
            m: {"n": len(v), "match_share": sum(v) / len(v)}
            for m, v in by_model.items()
        },
        "overall": (sum(s[0] for s in samples) / len(samples)) if samples else None,
        "matches": [s[2] for s in rng.sample(hits, min(20, len(hits)))],
        "non_matches": [s[2] for s in rng.sample(miss, min(20, len(miss)))],
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


def cmd_dry_digest(a) -> int:
    routing = paths.cfg("routing.json")
    pc = paths.cfg("panels.json")[a.panel]
    R = digest.roles(pc)
    pv = values.planning(a.panel)
    per_pkg: dict[str, dict] = {}
    for p, fs, pkg in _rows(a.rows):
        rid = Path(p).name.split(".")[0]
        run = Path(p).parent.name
        per_pkg.setdefault(f"{pkg}/{run}", {})[rid] = fs
    out = {}
    for key, revs in per_pkg.items():
        pkg = key.split("/")[0]
        cand = (paths.EVAL / pkg / "candidate.md").read_text(encoding="utf-8")
        B = pv["packages"][pkg]["B_f"]
        row = {}
        for rid, me in R.items():
            n = values.compute_n(
                0, B, B, pc["box_cap_s"], me["cap"], 6, pv["turn_p90"][me["model"]]
            )
            q = sum(
                len(digest.select(revs.get(s, []), cand, routing, me["style"]))
                for s in me["sources"]
            )
            if me["style"] == "reading":
                q = (q + 1) // 2
            row[rid] = {
                "qualifying": q,
                "n": n,
                "expected_real": min(n, q) * (1 - routing["gap_probability"]),
                "expected_gap": n * routing["gap_probability"],
            }
        out[key] = row
    print(json.dumps(out, indent=1))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="r3lib/cli.py")
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("pin")
    s.add_argument("--check", action="store_true")
    s.add_argument("--config-dir")
    s.set_defaults(f=cmd_pin)
    s = sp.add_parser("normalize")
    s.add_argument("--in", dest="inp", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--json", required=True)
    s.set_defaults(f=cmd_normalize)
    s = sp.add_parser("digest")
    s.add_argument("--pkgdir", required=True)
    s.add_argument("--rid", required=True)
    s.add_argument("--t-launch", type=float, required=True)
    s.add_argument("--start-cost", type=float, choices=[6, 16], required=True)
    s.set_defaults(f=cmd_digest)
    s = sp.add_parser("combine")
    s.add_argument("--pkgdir", required=True)
    s.add_argument("--rid", required=True)
    s.set_defaults(f=cmd_combine)
    s = sp.add_parser("p2check")
    s.add_argument("--stream", required=True)
    s.set_defaults(f=cmd_p2check)
    s = sp.add_parser("reask-errors")
    s.add_argument("--json", required=True)
    s.set_defaults(f=cmd_reask_errors)
    s = sp.add_parser("errcount")
    s.add_argument("--in", dest="inp", required=True)
    s.set_defaults(f=cmd_errcount)
    s = sp.add_parser("metrics")
    s.add_argument("--pkgdir", required=True)
    s.set_defaults(f=cmd_metrics)
    s = sp.add_parser("capture-sessions")
    s.add_argument("--pkgdir", required=True)
    s.set_defaults(f=cmd_capture)
    s = sp.add_parser("judge-ok")
    s.add_argument("--dir", required=True)
    s.set_defaults(f=cmd_judge_ok)
    s = sp.add_parser("audit")
    s.add_argument("--pkgdir", required=True)
    s.set_defaults(f=cmd_audit)
    s = sp.add_parser("anon")
    s.add_argument("--in", dest="inp", required=True)
    s.add_argument("--out", required=True)
    s.set_defaults(f=cmd_anon)
    s = sp.add_parser("result")
    s.add_argument("--rundir", required=True)
    s.set_defaults(f=cmd_result)
    s = sp.add_parser("values-freeze")
    s.add_argument("--panel", required=True)
    s.add_argument("--runs", nargs="+", required=True)
    s.set_defaults(f=cmd_values_freeze)
    s = sp.add_parser("values-show")
    s.add_argument("--panel", required=True)
    s.add_argument("--smoke", action="store_true")
    s.add_argument("--spike4", action="store_true")
    s.add_argument("--tce", type=int, default=0)
    s.set_defaults(f=cmd_values_show)
    s = sp.add_parser("summarize")
    s.add_argument("--panel", required=True)
    s.add_argument("--results")
    s.set_defaults(f=cmd_summarize)
    s = sp.add_parser("calibrate-surface")
    s.add_argument("--rows", required=True)
    s.set_defaults(f=cmd_calibrate_surface)
    s = sp.add_parser("dry-digest")
    s.add_argument("--rows", required=True)
    s.add_argument("--panel", required=True)
    s.set_defaults(f=cmd_dry_digest)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
