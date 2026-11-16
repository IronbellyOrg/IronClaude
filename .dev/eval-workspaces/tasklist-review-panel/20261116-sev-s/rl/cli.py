"""The Recipe Ledger command line (DESIGN 2.2, 2.3, 8): `lens`, `check` and `reask`.

Run it as a script: `uv run --frozen --project REPO python RL/rl/cli.py <subcommand> ...`.

    reask R3: the ember's one repair call (rl/reask.py, DESIGN 7.6).
          reask --run RUN --rid RID --cwd SANDBOX_REPO --now-s SECONDS [--b SECONDS]
              decides with reask_allowed (the lens file of RID gives the model, `reask` and `b`; `--now-s` is the panel
              clock), makes the call only when allowed, and always writes RUN/reviews/RID.reask.json (allowed, asked,
              accepted, reason, seconds, ...). An accepted repair is written to RID.reask.md and RID.md (the original
              to RID.preask.md); run `check ... --via-reask RID` next. Fail soft: any failure, or RL_FORCE_EXC=reask,
              leaves RID.md as it was, records `error:<class>` and exits 0 (stdout is the record as one JSON line).
              Exit 2 only for a usage error.

    check R3: the ledger row check of one run folder (rl/rowcheck.py).
          check --run RUN --candidate FILE [--source FILE] [--via-reask RID ...]
              reads RUN/lens/<rid>.json and RUN/reviews/<rid>.{md,attempt1.json,meta.json}; writes
              RUN/check/<rid>.ledger.json, RUN/check/<rid>.checked.md and RUN/check/check.json. The raw reports are
              not edited. Exit 0 done; 1 the check raised (message on stderr, nothing written: the launcher sets
              check_skipped; RL_FORCE_EXC=check raises on purpose); 2 a usage error.

    lens  R1: render the lens of each reviewer of one panel and its brief.
          lens --validate                 print the three panels of the lens table and exit 0 (E_LENS_INVALID, exit 1)
          lens --panel P --doc D --candidate-sb FILE --out RUN [--source FILE] [--b SECONDS] [--c-luna SECONDS]
               [--fallback REASON]
              writes RUN/lens/<rid>.json, RUN/briefs/<rid>.txt, RUN/briefs/<rid>.sha256 and merges the lens fields
              into RUN/run.json (DESIGN 2.2).

Exit codes of `lens`: 0 done; 1 the render raised (RUN/lens/error.json holds the exception class and `reason`, `error` or
`lens_invalid`; the message on stderr starts with E_LENS_INVALID for a bad table; the launcher falls back to Z0, DESIGN 8
rows 1 and 2); 2 a usage error or an unreadable input; 3 `no_budget` (the files are written, the run is refused, row 4).
`--fallback REASON` writes Z0 briefs and no lens, for the launcher to call after exit 1.

    plan, briefs, prepare-merge, record: the steps bin/run-panel.sh needs around the three above.
          plan --arm A --panel P --doc D [--b S]      prints {"b", "hang_s"} (b defaults to values.json for the document)
          briefs --arm A --panel P --doc D --candidate-sb F [--source F] --out RUN
              arms Z0-raw, Z0 and K: writes RUN/briefs/<rid>.{txt,sha256} and the brief fields of RUN/run.json
          prepare-merge --run RUN [--checked]         H2 on each reviewer that finished (the checked report when --checked),
              writes RUN/normalised/, RUN/resolution.json and prints {"used", "absent"} as one JSON line
          record --run RUN --arm A --t0 S --render-s S --check-s S [--r3-end S] [--check-skipped] [--check-ran] ...
              writes RUN/timing.json and the closing fields of RUN/run.json
          `check` also copies RUN/reviews/<rid>.reask.json into the `reask` key of check.json.

Adding a subcommand: add one entry to COMMANDS, (help, function that adds its arguments, function that runs and returns
the exit code). Nothing in `lens` changes.

Importing: the folder of this file is taken off sys.path first and RL is put on it, so `rl` and `scaffold` import when
the file is run by path.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_RL = os.path.dirname(_HERE)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]
if _RL not in sys.path:
    sys.path.insert(0, _RL)

import argparse  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

from rl import lens as lens_mod  # noqa: E402
from rl import reask, render, rowcheck  # noqa: E402
from scaffold import briefs as briefs_mod  # noqa: E402
from scaffold import clock, normalise  # noqa: E402

PACKAGES_JSON = Path(_RL) / "config" / "packages.json"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _validate(args) -> int:
    try:
        table = lens_mod.load(args.lenses)
    except ValueError as e:  # LensInvalid, or recipes.json that does not validate
        print(e, file=sys.stderr)
        return 1
    for name, panel in table["panels"].items():
        print(f"{name}: {panel['label']}")
        for role, r in panel["roles"].items():
            print(
                f"  {role} {r['rid']} {r['model']} lens={','.join(r['lens'])} table_cap={r['table_cap']}"
            )
    return 0


def _check_source(args) -> str | None:
    """The source path to use; refuses a `--source` that disagrees with packages.json (a silent C2 drop, DR-7)."""
    pk = json.loads(Path(args.packages).read_text(encoding="utf-8"))["packages"]
    if args.doc in pk and bool(pk[args.doc]["source"]) != bool(args.source):
        raise ValueError(
            f"{args.doc}: packages.json source is {pk[args.doc]['source']!r} but --source is {args.source!r}"
        )
    return args.source or None


def _lens(args) -> int:
    if args.validate:
        return _validate(args)
    missing = [
        f"--{o.replace('_', '-')}"
        for o in ("panel", "doc", "candidate_sb", "out")
        if not getattr(args, o)
    ]
    if missing:
        print(f"lens needs {', '.join(missing)}", file=sys.stderr)
        return 2
    out = Path(args.out)
    try:
        source = _check_source(args)
        doc = {
            "cand_sb": str(Path(args.candidate_sb)),
            "sha": render.file_sha256(args.candidate_sb),
        }
        values = lens_mod.values()
        if (
            args.c_luna is not None
        ):  # the timing spike's measured cost per luna row (REQ-32)
            values = {**values, "c": {**values["c"], "gpt-6-luna": args.c_luna}}
        b = args.b if args.b is not None else min(values["b"][args.panel].values())
    except (OSError, ValueError, KeyError) as e:
        print(f"lens failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    try:
        if os.environ.get("RL_FORCE_EXC") == "lens":
            raise RuntimeError("RL_FORCE_EXC=lens")
        if args.fallback:
            return _fallback(args, out, doc, source, values, b)
        table = lens_mod.load(args.lenses)
        roles = lens_mod.render(args.panel, bool(source), b, values["c"], table=table)
        briefs = {r["rid"]: render.brief(r, doc, source) for r in roles.values()}
        for role, r in roles.items():
            info = dict(
                r,
                panel=args.panel,
                role=role,
                doc=args.doc,
                has_source=bool(source),
                b=b,
                c=values["c"][r["model"]],
            )
            _write(out / "lens" / f"{r['rid']}.json", render.dumps(info))
        fields = render.run_fields(
            roles,
            has_source=bool(source),
            b=b,
            c_by_model=values["c"],
            lenses_path=args.lenses,
            briefs=briefs,
        )
    except Exception as e:  # DESIGN 8 rows 1 and 2: the launcher falls back to Z0
        reason = "lens_invalid" if isinstance(e, lens_mod.LensInvalid) else "error"
        err = {"error": type(e).__name__, "reason": reason, "message": str(e)}
        _write(out / "lens" / "error.json", render.dumps(err))
        print(
            str(e)
            if reason == "lens_invalid"
            else f"lens failed: {type(e).__name__}: {e}",
            file=sys.stderr,
        )
        return 1
    _write_briefs(out, briefs)
    _merge_run_json(out, args, fields)
    return 3 if fields["no_budget"] else 0


def _write_briefs(out: Path, briefs: dict) -> None:
    for rid, b in briefs.items():
        _write(out / "briefs" / f"{rid}.txt", b["text"])
        _write(out / "briefs" / f"{rid}.sha256", b["sha256"] + "\n")


def _merge_run_json(out: Path, args, fields: dict) -> None:
    path = out / "run.json"
    run = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    run.update(fields, panel=args.panel, doc=args.doc)
    _write(path, render.dumps(run))


def _fallback(args, out: Path, doc: dict, source, values, b) -> int:
    """Z0 briefs for the reviewers of the panel; the table is read without validation (it may be the reason)."""
    table = json.loads(Path(args.lenses).read_text(encoding="utf-8"))
    roles = {
        role: {"rid": r["rid"], "model": r["model"]}
        for role, r in table["panels"][args.panel]["roles"].items()
    }
    briefs = {
        r["rid"]: render.brief(r, doc, source, fallback=True) for r in roles.values()
    }
    fields = render.run_fields(
        roles,
        has_source=bool(source),
        b=b,
        c_by_model=values["c"],
        lenses_path=args.lenses,
        fallback=True,
        fallback_reason=args.fallback,
        briefs=briefs,
    )
    _write_briefs(out, briefs)
    _merge_run_json(out, args, fields)
    return 0


def _lens_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--validate", action="store_true", help="validate the lens table")
    p.add_argument("--panel", help="primary, haiku or sonnet")
    p.add_argument(
        "--doc", help="the document id (a key of packages.json when it has one)"
    )
    p.add_argument(
        "--candidate-sb", help="absolute path of the candidate in the sandbox"
    )
    p.add_argument(
        "--source",
        help="absolute path of the source document; leave out when there is none",
    )
    p.add_argument("--out", help="the run folder")
    p.add_argument(
        "--b",
        type=float,
        help="seconds; default is the smallest b of the panel in values.json",
    )
    p.add_argument(
        "--c-luna",
        type=float,
        help="seconds per luna ledger row instead of the planning value (the timing spike's c)",
    )
    p.add_argument(
        "--fallback", metavar="REASON", help="write Z0 briefs, record this reason"
    )
    p.add_argument("--lenses", default=str(lens_mod.LENSES_JSON))
    p.add_argument("--packages", default=str(PACKAGES_JSON))


def _check_args(p: argparse.ArgumentParser) -> None:
    # dest is not `run`: set_defaults(run=...) of build_parser would overwrite it
    p.add_argument("--run", dest="run_dir", help="the run folder")
    p.add_argument(
        "--candidate", help="absolute path of the candidate the reviewers read"
    )
    p.add_argument("--source", help="absolute path of the source; leave out if none")
    p.add_argument(
        "--via-reask",
        action="append",
        default=[],
        metavar="RID",
        help="a reviewer whose report was repaired by the re-ask (its rows are not promoted)",
    )


def _check(args) -> int:
    missing = [
        f"--{o}"
        for o, v in (("run", args.run_dir), ("candidate", args.candidate))
        if not v
    ]
    if missing:
        print(f"check needs {', '.join(missing)}", file=sys.stderr)
        return 2
    try:
        result = rowcheck.check_run(
            args.run_dir, args.candidate, args.source, args.via_reask
        )
        _fill_reask(Path(args.run_dir), result)
    except Exception as e:  # DESIGN 8 row 10: the launcher sets check_skipped
        print(f"check failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    return 0


def _fill_reask(run: Path, result: dict) -> None:
    """The `reask` key of check.json (DESIGN 7.4) from the records of the re-ask step."""
    recs = {}
    for f in sorted((run / "reviews").glob("*.reask.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        recs[r["rid"]] = {
            k: r.get(k) for k in ("allowed", "reason", "accepted", "seconds")
        }
    if recs:
        result["reask"] = recs
        _write(run / "check" / "check.json", render.dumps(result))


def _reask_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run", dest="run_dir", help="the run folder")
    p.add_argument("--rid", help="the reviewer id (the ember's)")
    p.add_argument("--cwd", help="the sandbox repo the reviewer ran in")
    p.add_argument(
        "--now-s",
        type=float,
        help="the panel clock (seconds since t0) when the report was read",
    )
    p.add_argument(
        "--b", type=float, help="seconds; default is the `b` of lens/<rid>.json"
    )


def _reask(args) -> int:
    missing = [
        flag
        for flag, v in (
            ("--run", args.run_dir),
            ("--rid", args.rid),
            ("--cwd", args.cwd),
            ("--now-s", args.now_s),
        )
        if v in (None, "")
    ]
    if missing:
        print(f"reask needs {', '.join(missing)}", file=sys.stderr)
        return 2
    try:
        if os.environ.get("RL_FORCE_EXC") == "reask":
            raise RuntimeError("RL_FORCE_EXC=reask")
        rec = reask.do_reask(args.run_dir, args.rid, args.cwd, args.now_s, args.b)
    except (
        Exception
    ) as e:  # DESIGN 8 rows 8 and 20: fail soft, the original report stays
        print(f"reask failed: {type(e).__name__}: {e}", file=sys.stderr)
        rec = {
            "rid": args.rid,
            "asked": True,
            "allowed": True,
            "accepted": False,
            "seconds": 0.0,
            "reason": f"error:{type(e).__name__}",
        }
        try:
            path = Path(args.run_dir) / "reviews" / f"{args.rid}.reask.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render.dumps(rec), encoding="utf-8")
        except OSError as w:
            print(f"reask record not written: {w}", file=sys.stderr)
    print(json.dumps(rec, sort_keys=True))
    return 0


def _roles(args) -> dict:
    """{role: {rid, model}} of the panel, read without validation (the table may be the reason for a fallback)."""
    table = json.loads(Path(args.lenses).read_text(encoding="utf-8"))
    return {
        role: {"rid": r["rid"], "model": r["model"]}
        for role, r in table["panels"][args.panel]["roles"].items()
    }


def _plan_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--arm", help="Z0-raw, Z0, K or RL")
    p.add_argument("--panel", help="primary, haiku or sonnet")
    p.add_argument("--doc", help="the document id")
    p.add_argument(
        "--b", type=float, help="seconds; default is the value of values.json"
    )


def _plan(args) -> int:
    """The b of the run and the hang guard of its arm (DESIGN 9.4)."""
    pb = lens_mod.values()["b"].get(args.panel)
    if pb is None or not args.arm or not args.doc:
        print("plan needs a known --panel, --arm and --doc", file=sys.stderr)
        return 2
    b = args.b if args.b is not None else pb.get(args.doc, min(pb.values()))
    try:
        hang = clock.hang_s(b, args.arm, args.panel)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    print(json.dumps({"b": b, "hang_s": hang}))
    return 0


def _briefs_args(p: argparse.ArgumentParser) -> None:
    _plan_args(p)
    p.add_argument(
        "--candidate-sb", help="absolute path of the candidate in the sandbox"
    )
    p.add_argument("--source", help="absolute path of the source; leave out if none")
    p.add_argument("--out", help="the run folder")
    p.add_argument("--lenses", default=str(lens_mod.LENSES_JSON))


def _briefs(args) -> int:
    """Arms Z0-raw, Z0 and K: the same brief for every reviewer of the panel (no lens, DESIGN 2.1)."""
    if args.arm not in ("Z0-raw", "Z0", "K") or not (
        args.panel and args.doc and args.candidate_sb and args.out
    ):
        print(
            "briefs needs --arm Z0-raw|Z0|K, --panel, --doc, --candidate-sb and --out",
            file=sys.stderr,
        )
        return 2
    try:
        roles = _roles(args)
        source = args.source or None
        doc = {
            "cand_sb": str(Path(args.candidate_sb)),
            "sha": render.file_sha256(args.candidate_sb),
        }
        brief = briefs_mod.render(args.arm, doc, None, source)
        z0 = briefs_mod.render("Z0", doc, None, source)
        fields = {
            "fallback": False,
            "fallback_reason": None,
            "no_source": not source,
            "c2_not_applicable": not source,
            "no_budget": False,
            "lenses_sha256": render.file_sha256(args.lenses),
            "recipes_sha256": render.file_sha256(render.recipes_mod.RECIPES_JSON),
            "z0_sha256": z0["sha256"],
            "reviewers": {
                r["rid"]: {"model": r["model"], "brief_sha256": brief["sha256"]}
                for r in roles.values()
            },
        }
    except (OSError, ValueError, KeyError) as e:
        print(f"briefs failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    _write_briefs(Path(args.out), {r["rid"]: brief for r in roles.values()})
    _merge_run_json(Path(args.out), args, fields)
    return 0


def _merge_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run", dest="run_dir", help="the run folder")
    p.add_argument(
        "--checked",
        action="store_true",
        help="take check/<rid>.checked.md where it exists (arm RL with a check that ran)",
    )


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def _prepare_merge(args) -> int:
    """H2 on each reviewer that finished (status ok) and the resolution file of the merge (DESIGN 9.6).

    A killed, invalid or errored reviewer, or one whose findings block is still unusable after H2, is absent."""
    run = Path(args.run_dir)
    info = _read_json(run / "run.json")
    used, absent, models = [], {}, []
    for rid, spec in info["reviewers"].items():
        meta = _read_json(run / "reviews" / f"{rid}.meta.json")
        if meta is None or meta.get("status") != "ok":
            absent[rid] = (meta or {}).get("status", "not_run")
            continue
        src = run / "check" / f"{rid}.checked.md"
        if not (args.checked and src.is_file()):
            src = run / "reviews" / f"{rid}.md"
        if not normalise.normalise_file(src, run / "normalised", rid)["ok"]:
            absent[rid] = "h2_not_ok"
            continue
        used.append(rid)
        models.append({"reviewer_id": rid, "model": spec["model"]})
    _write(run / "resolution.json", render.dumps({"reviewers": models}))
    out = {"used": used, "absent": absent}
    _write(run / "merged" / "merge-input.json", render.dumps(out))
    print(json.dumps(out, sort_keys=True))
    return 0


def _record_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run", dest="run_dir", help="the run folder")
    p.add_argument("--arm")
    for name in ("t0", "render-s", "check-s", "r3-end", "merge-exit"):
        p.add_argument(f"--{name}", type=float)
    for name in ("check-skipped", "check-ran", "sandbox-dirty"):
        p.add_argument(f"--{name}", action="store_true")


def _record(args) -> int:
    """timing.json (clock.timing_record) and the closing fields of run.json."""
    run = Path(args.run_dir)
    info = _read_json(run / "run.json")
    start, end, reasks, per = {}, {}, [], {}
    for rid in info["reviewers"]:
        s, e = (run / "stamps" / f"{rid}.{k}" for k in ("start", "end"))
        if s.is_file() and e.is_file():
            start[rid], end[rid] = float(s.read_text()), float(e.read_text())
        ask = _read_json(run / "reviews" / f"{rid}.reask.json") or {}
        meta = _read_json(run / "reviews" / f"{rid}.meta.json") or {}
        if ask.get("asked"):
            reasks.append(rid)
        per[rid] = {
            "status": meta.get("status", "not_run"),
            "killed": bool(meta.get("killed")),
            "model_ok": meta.get("model_ok"),
            "wall_s": meta.get("wall_s"),
            "reask_s": ask.get("seconds", 0) if ask.get("asked") else 0,
        }
    rl = args.arm == "RL"
    if end:
        timing = clock.timing_record(
            args.arm,
            args.t0,
            start,
            end,
            render_s=args.render_s if rl else 0,
            check_s=args.check_s if rl else 0,
            reask_s=round(sum(v["reask_s"] for v in per.values()), 3),
            r3_end=args.r3_end if rl else None,
        )
    else:  # no reviewer ran: there is no clock to report
        timing = {"t0": args.t0, "panel_elapsed_s": None, "slowest_reviewer_s": None}
    for k in ("arm", "panel", "doc", "b", "hang_s", "concurrent_panels_at_start"):
        timing[k] = info[k]
    _write(run / "timing.json", render.dumps(timing))
    merged = _read_json(run / "merged" / "merge-input.json") or {}
    err = run / "merged" / "merge.err"
    for rid, v in per.items():
        v["merged"] = rid in merged.get("used", [])
        v["absent_reason"] = merged.get("absent", {}).get(rid)
        info["reviewers"][rid].update(v)
    info.update(
        reask=reasks,
        retries=0,
        check_skipped=args.check_skipped,
        check_ran=args.check_ran,
        sandbox_dirty=args.sandbox_dirty,
        merge_refused=bool(args.merge_exit),
        merge_error=err.read_text(encoding="utf-8")[-500:]
        if args.merge_exit and err.is_file()
        else None,
        time_cap_exception=False,
        verifier=0,
    )
    _write(run / "run.json", render.dumps(info))
    return 0


# name -> (help, function that adds the arguments, function that runs and returns the exit code)
COMMANDS = {
    "lens": ("render the lens and the brief of each reviewer (R1)", _lens_args, _lens),
    "check": ("check the ledgers of one run folder (R3)", _check_args, _check),
    "reask": ("the ember's one repair call (R3, DR-8)", _reask_args, _reask),
    "plan": ("the b and the hang guard of a run", _plan_args, _plan),
    "briefs": ("the briefs of arms Z0-raw, Z0 and K", _briefs_args, _briefs),
    "prepare-merge": (
        "H2 and the resolution file (the merge input)",
        _merge_args,
        _prepare_merge,
    ),
    "record": (
        "timing.json and the closing fields of run.json",
        _record_args,
        _record,
    ),
}


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="rl", description="The Recipe Ledger tools.")
    sub = ap.add_subparsers(
        dest="cmd", required=True, metavar="{" + ",".join(COMMANDS) + "}"
    )
    for name, (help_, add_args, run) in COMMANDS.items():
        p = sub.add_parser(name, help=help_)
        add_args(p)
        p.set_defaults(run=run)
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
