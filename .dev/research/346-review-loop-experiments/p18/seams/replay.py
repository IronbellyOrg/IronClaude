#!/usr/bin/env python3
"""Offline replay of the ab6 seams A1 / A2 / A3 over the 13 specs of specs-13.json (original + 6 ab4 finals + 6 PN1 finals).

  python3 replay.py --seam all                       # DRY RUN (default): builds every packet, checks privacy/size, prints the reservation; no call, no key
  python3 replay.py --seam a1 --mock                 # deterministic fake transport (plumbing check; the answers are NOT evidence)
  python3 replay.py --seam all --mock --mock-mode mixed
  bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $SP/p18/seams && python3 replay.py --seam all --live'     # coordinator only

--live (contract J2/J4/J5): needs JEV_API_KEY in the environment of that single command; the pre-flight builds every request with live=False,
reserves estimate x 1.2 BEFORE the first paid call (a reservation that does not fit writes BLOCKED-BUDGET-<seam>.json and makes no call, exit 5),
journals every attempt under journal/jev-<seam>.jsonl, caches validated answers under cache/ (a re-run costs nothing), and treats every
non-ok / insufficient answer as a fallback (no hint).  Exit codes: 0 ok, 2 usage, 3 key missing/rejected, 5 blocked budget.
This script never reads the key file and never prints the environment.

Outputs (per seam, per spec): out/<seam>/<sid>.json (schema ab6-replay/1: packets, answers, hints, fallbacks, counts), out/<seam>/summary.json,
out/<seam>/control/ (identical packets for a same-packet Sonnet judge, with --control-export).  The mode ('mock'/'live') is written into every file.
"""
import argparse
import json
import math
import os
import pathlib
import sys

import seamlib as S
import a1_support as A1
import a2_observability as A2
import a3_novelty as A3

OUT = S.SEAMS / "out"
EXIT_KEY, EXIT_BUDGET = 3, 5


def select_specs(arg):
    specs = S.load_specs13()
    if not arg:
        return specs
    want = set(arg.split(","))
    got = [e for e in specs if e["sid"] in want]
    missing = want - {e["sid"] for e in got}
    if missing:
        raise SystemExit(f"unknown spec id(s): {sorted(missing)}")
    return got


def counts_delta(after, before):
    keys = ("calls", "ok", "fallback", "input_tokens")
    return {k: after[k] - before[k] for k in keys}


def packet_rows(items):
    out = []
    for it in items:
        b = S.packet_bytes(it)
        out.append({"id": it["id"], "bytes": b, "est_tokens": int(math.ceil(b / S.C.SIZE_BYTES_PER_TOKEN)), "sha256": S.sha(it["state"]), "score": it.get("score")})
    return out


def fallbacks_of(outs):
    return [{"id": o["id"], "reason": o["fallback"]} for o in outs if not o.get("usable")]


def enforce_packet_limit(items, dec):
    """A packet over the byte limit is refused locally (no truncation, no call); it is recorded as a fallback by the caller."""
    lim = dec["caps"]["packet_bytes_max"]
    ok, refused = [], []
    for it in items:
        (ok if S.packet_bytes(it) <= lim else refused).append(it)
    return ok, refused


# ----------------------------------------------------------------------------- per-seam builders: spec entry -> (meta, items, finish(outs))
def build_a1(entry, dec, accepted_dir):
    text = S.spec_text(entry)
    acc = None
    if accepted_dir and (pathlib.Path(accepted_dir) / f"{entry['sid']}.json").exists():
        acc = json.loads((pathlib.Path(accepted_dir) / f"{entry['sid']}.json").read_text())
    ex, bp, items = A1.build_items(text, entry["sid"], acc, dec["caps"]["a1_pairs"])
    meta = {"extract": {"obligations": len(ex["obligations"]), "criteria": len(ex["criteria"])},
            "prefilter": {k: bp[k] for k in ("raw", "eligible", "dropped_covered")}, "accepted_findings": 0 if not acc else len(acc),
            "pairs": [{"id": p["id"], "score": p["score"], "signals": p["signals"], "o_line": p["o"]["line"], "c_line": p["c"]["line"]} for p in bp["pairs"]]}

    def finish(outs):
        return {"hints": A1.make_hints(bp, outs, dec["caps"]["a1_hints"]), "keyword_flags": A1.keyword_flags(bp)}
    return meta, items, finish


def build_a2(entry, dec, seam_dir):
    text = S.spec_text(entry)
    rows, analysis, items, lint_all = A2.build_items(text, seam_dir / "scratch" / entry["sid"], entry["sid"])
    meta = {"rows": len(rows), "to_jev": sum(1 for a in analysis if a["to_jev"]), "code_flagged": sum(1 for a in analysis if a["code_flags"]),
            "analysis": analysis, "lint_all": [{"id": f["lint_id"], "lines": f["lines"], "check": f["check"]} for f in lint_all]}

    def finish(outs):
        return {"lines": A2.make_lines(analysis, outs, dec["caps"]["a2_lines"])}
    return meta, items, finish


# ----------------------------------------------------------------------------- driver
def run_seam(seam, specs, args, dec):
    seam_dir = OUT / seam
    seam_dir.mkdir(parents=True, exist_ok=True)
    mode = "live" if args.live else "mock" if args.mock else "dry"
    built = []
    if seam == "a3":
        d = A3.load_pn1_cases()
        S.write_json(seam_dir / "cases.json", {"report": d["report"], "cases": [dict(c, analysis={k: v for k, v in c["analysis"].items() if k != "hunks"}) for c in d["cases"]]})
        (seam_dir / "label-packets").mkdir(exist_ok=True)
        for c in d["cases"]:
            (seam_dir / "label-packets" / f"{c['case_id']}.md").write_text(A3.label_packet(c))
        wanted = {e["sid"] for e in specs}
        by_sid = {}
        for c in d["cases"]:
            if c["sid"] in wanted:
                by_sid.setdefault(c["sid"], []).append(c)
        for e in specs:
            if e["sid"] not in by_sid:
                continue
            cs = by_sid[e["sid"]]
            items = A3.case_items(cs)
            meta = {"cases": [{"case_id": c["case_id"], "lid": c["lid"], "outcome_hidden_from_jev": True, "to_jev": c["analysis"]["to_jev"],
                               "touched_v1": c["analysis"]["touched_v1"], "named_not_touched": c["analysis"]["named_not_touched"],
                               "span_overlap": c["analysis"]["span_overlap"], "r2_on_v1_lines": c["analysis"]["r2_on_v1_lines"]} for c in cs]}

            def finish(outs, cs=cs):
                an = [c["analysis"] for c in cs]
                return {"lines": A3.make_lines(an, outs)}
            built.append((e, meta, items, finish))
    else:
        for e in specs:
            meta, items, finish = (build_a1(e, dec, args.accepted_dir) if seam == "a1" else build_a2(e, dec, seam_dir))
            built.append((e, meta, items, finish))

    # packet size limit (local refusal, no truncation)
    refused_big = {}
    for i, (e, meta, items, finish) in enumerate(built):
        ok, big = enforce_packet_limit(items, dec)
        refused_big[e["sid"]] = [b["id"] for b in big]
        built[i] = (e, meta, ok, finish)
    all_items = [it for (_, _, items, _) in built for it in items]
    ceil_usd = args.ceiling_usd if args.ceiling_usd is not None else None
    ceil_tok = args.ceiling_tokens if args.ceiling_tokens is not None else None

    if mode == "live" and not os.environ.get(S.C.KEY_ENV):
        print(f"ERROR {S.C.KEY_ENV} is not set (use bash -c 'set -a; . \"$SP/.jev.env\"; set +a; ...'); live replay refused, no fallback")
        return EXIT_KEY
    ctx = S.mock_env() if mode == "mock" else _null()
    with ctx:
        runner = S.Runner(seam=seam, mode="live" if mode == "live" else "mock", out_dir=seam_dir, mock_mode=args.mock_mode, mock_seed=args.seed,
                          dec=dec, ceiling_usd=ceil_usd, ceiling_tokens=ceil_tok)
        pre = runner.preflight(all_items)
        print(f"PREFLIGHT {seam}: {len(built)} specs, {pre['requests']} requests, privacy-refused {pre['privacy_refused']}, oversize-refused {pre['oversize_refused']}; "
              f"reservation {pre['reserve_tokens']} tokens (${pre['reserve_usd']:.6f}) of ${dec['jev']['offline_ceiling_usd']} / {dec['jev']['offline_ceiling_input_tokens']} tokens")
        S.write_json(seam_dir / "preflight.json", dict(pre, seam=seam, mode=mode, specs=[e["sid"] for e, *_ in built]))
        if mode == "dry":
            _write_dry(seam, built, seam_dir, pre, refused_big)
            print(f"DRY RUN OK ({seam}): no network object created, no key needed")
            return 0
        try:
            runner.reserve(pre["reserve_tokens"])
        except S.BudgetExhausted as ex:
            S.write_json(seam_dir / f"BLOCKED-BUDGET-{seam}.json", {"seam": seam, "estimate": pre, "error": str(ex)})
            print(f"BLOCKED-BUDGET {seam}: {ex}")
            return EXIT_BUDGET
        try:
            for e, meta, items, finish in built:
                before = dict(runner.stats)
                before["status"] = dict(runner.stats["status"])
                outs = [runner.ask(it) for it in items]
                fin = finish(outs)
                rec = {"schema": "ab6-replay/1", "seam": seam, "sid": e["sid"], "arm": e["arm"], "run": e["run"], "mode": mode, "qset": items[0]["qset"] if items else None,
                       "meta": meta, "packets": packet_rows(items), "oversize_refused": refused_big[e["sid"]], "answers": outs, "fallbacks": fallbacks_of(outs) +
                       [{"id": i, "reason": "refused:oversize_local"} for i in refused_big[e["sid"]]],
                       "counts": dict(counts_delta(runner.stats, before), usable=sum(1 for o in outs if o.get("usable"))), **fin}
                S.write_json(seam_dir / f"{e['sid']}.json", rec)
                print(f"  {seam} {e['sid']:5s} calls {rec['counts']['calls']:3d} ok {rec['counts']['ok']:3d} usable {rec['counts']['usable']:3d} "
                      f"fallback {rec['counts']['fallback']:3d} lines/hints {len(fin.get('hints', fin.get('lines', [])))}")
        except (S.KeyMissing, S.KeyRejected) as ex:
            runner.release()
            print(f"ERROR configuration: {ex}")
            return EXIT_KEY
        runner.release()
        if mode == "live":
            from jevlib.manifest import update as manifest_update
            manifest_update(S.SEAMS / "journal" / f"jev-{seam}.jsonl", S.SEAMS / f"manifest-{seam}.json")
        st = runner.finish()
        S.write_json(seam_dir / "summary.json", {"schema": "ab6-replay-summary/1", "seam": seam, "mode": mode, "specs": [e["sid"] for e, *_ in built], "stats": st, "preflight": pre})
        print(f"REPLAY DONE {seam} ({mode}): calls {st['calls']} ok {st['ok']} fallback {st['fallback']} input_tokens {st['input_tokens']} spent ${st['usd']:.6f}; "
              f"statuses {st['status']}")
        if mode == "live":
            print("Next: keyscan (contract J2), then score_gates.py")
    return 0


class _null:
    def __enter__(self):
        return None

    def __exit__(self, *a):
        return False


def _write_dry(seam, built, seam_dir, pre, refused_big):
    for e, meta, items, finish in built:
        S.write_json(seam_dir / f"{e['sid']}.dry.json", {"schema": "ab6-replay/1", "seam": seam, "sid": e["sid"], "mode": "dry", "meta": {k: v for k, v in meta.items() if k != "analysis"},
                                                          "packets": packet_rows(items), "oversize_refused": refused_big[e["sid"]]})


def control_export(seam, specs, args, dec):
    """Identical packets for a same-packet Sonnet judge (no Jev): control/<sid>.packets.json, a prompt, and the path the answers go to."""
    cdir = OUT / seam / "control"
    cdir.mkdir(parents=True, exist_ok=True)
    for e in specs:
        if seam == "a1":
            _, _, items = A1.build_items(S.spec_text(e), e["sid"], None, dec["caps"]["a1_pairs"])
            packets = A1.control_items(items)
        elif seam == "a2":
            _, _, items, _ = A2.build_items(S.spec_text(e), OUT / "a2" / "scratch" / e["sid"], e["sid"])
            packets = A2.control_items(items)
        else:
            continue
        pk = cdir / f"{e['sid']}.packets.json"
        S.write_json(pk, packets)
        ans = cdir / f"{e['sid']}.answers.json"
        (cdir / f"PROMPT-{e['sid']}.md").write_text(
            f"# Task: answer {len(packets)} independent judgment packets (seam {seam}, spec {e['sid']})\n\n"
            f"Read `{pk}`. Each element has `id`, `state` (the facts), `question` and `options` (name -> meaning). For EVERY packet choose exactly one option name using ONLY the "
            f"text in that packet's state (do not open any other file, do not look for the source spec, do not use outside knowledge about which defects exist). "
            f"Write valid JSON `{{\"<packet id>\": \"<option name>\", ...}}` covering every id to `{ans}`. Reply `DONE {ans}` and nothing else.\n")
    print(f"control packets written under {cdir}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seam", choices=["a1", "a2", "a3", "all"], required=True)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--mock", action="store_true", help="deterministic fake transport (plumbing only)")
    g.add_argument("--live", action="store_true", help="real Jev calls (coordinator only; needs the key in the environment)")
    ap.add_argument("--mock-mode", default="ok", choices=["ok", "insufficient", "malformed", "timeout", "http500", "wrongmodel", "mixed"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--specs", help="comma-separated spec ids (default: all 13)")
    ap.add_argument("--accepted-dir", help="dir with <sid>.json lists of accepted findings (A1 drops covered pairs)")
    ap.add_argument("--ceiling-usd", type=float)
    ap.add_argument("--ceiling-tokens", type=int)
    ap.add_argument("--control-export", action="store_true")
    args = ap.parse_args(argv)
    dec = S.decision()
    specs = select_specs(args.specs)
    seams = ["a1", "a2", "a3"] if args.seam == "all" else [args.seam]
    rc = 0
    for sm in seams:
        if args.control_export:
            control_export(sm, specs, args, dec)
            continue
        rc = run_seam(sm, specs, args, dec) or rc
        if rc in (EXIT_KEY, EXIT_BUDGET):
            return rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
