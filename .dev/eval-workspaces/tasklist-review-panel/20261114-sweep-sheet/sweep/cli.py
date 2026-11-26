"""The sweep command line (DESIGN 2.2, 2.3): `prepass`, `lint`, `brief`, `normalise`, `check` and `clock`.

Run it as a script: `uv run --frozen --project REPO python SW/sweep/cli.py <subcommand> ...`.

    prepass    sweep/prepass.py: --candidate, --source (optional), --repo, --seed, --out, --panel
    lint       scaffold/lint.py: every argument after `lint` is lint's own (--all, --gt-glob, --forbid, files)
    brief      scaffold/briefs.py render: one reviewer's brief, written to --out with `<stem>.sha256` beside it
    normalise  scaffold/normalise.py normalise_file: H2 on one report, written to --out-dir/<rid>.md and h2.json
    check      S5 (scaffold/ledgerv1.py): the raw reviews/<rid>.md of every reviewer of the run in; check/<rid>.checked.md,
               check/<rid>.ledger.json and check/check.json out. The raw reports are only read.
    clock      `plan` prints b, the kill limit, the hang guard and no_budget as JSON; `timing` writes timing.json from the
               event times of bin/run-panel.sh (scaffold/clock.py does the arithmetic; Task 27, DESIGN 11.4, 11.5);
               `spike` prints whether config/values.json holds the spike record and whether its fallback applies, and with
               --panels-out writes the panel file of a schedule run (bin/run-schedule.sh, Task 32, REQ-32)

`prepass --available RID,RID` re-runs the assignment with the reviewers that can still be launched (DESIGN 7.3, Task 27).

Exit codes: 0 success; 1 the pre-pass raised (prepass.error.json is written, DESIGN 10 row 1) or `check` raised
(DESIGN 10 row 11: nothing is written, the caller sets check_skipped); 2 a usage error or an unreadable input of `brief`
and `normalise`; `lint` keeps its own codes (0 clean, 1 leak, 2 usage).

Gaps in the design resolved here (the design names the delegation, not the arguments):
  C1  `brief` takes the arm, the absolute path of the candidate in the sandbox (the sha256 is computed from that file),
      the source path, the sheet file `sheets/<rid>.md` of arm SS and `--fallback`; it prints the brief's metadata as
      JSON (never the text) so a launcher can read `no_trigger` and `fallback`.
  C2  `normalise` prints the report's info as JSON and exits 0 even when lines stay unrepaired: they are recorded in
      h2.json (DESIGN 11.2: not silently dropped, not an error).
  C3  Importing: the folder of this file is taken off sys.path before anything else is imported, because
      sweep/select.py would otherwise shadow the standard `select` module that `subprocess` imports.
  C4  `check` (DESIGN 9.4 names the outputs, not the arguments). One call checks the whole run: `--run RUN`, with
      `--candidate` and `--source` (as the sandbox holds them). It reads RUN/prepass/items.json and
      RUN/prepass/assignment.json (`reviewers`: the items of each reviewer id), RUN/reviews/<rid>.md and, for the
      `transcript` corpus, RUN/reviews/<rid>.attempt1.json when it exists. A reviewer with no report file is listed in
      check.json `no_report` and skipped. Everything is computed before anything is written, so an exception leaves
      no `check/` files behind; it propagates as exit 1 with the message on stderr (no `check/error.log` is written
      here; the caller keeps stderr). The scope is the environment variable CHECK_SCOPE (DD-3), default `linked`.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SW = os.path.dirname(_HERE)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]  # C3
sys.path.insert(0, _SW)

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

from scaffold import briefs, clock, ledgerv1, lint, normalise  # noqa: E402
from sweep import assign, prepass  # noqa: E402

DELEGATED = {"lint": lint.main}


def _prepass(args) -> int:
    try:
        prepass.run(
            args.candidate,
            args.source,
            args.repo,
            seed=args.seed,
            out=args.out,
            panel=args.panel,
            available=args.available.split(",") if args.available else None,
        )
    except (
        Exception
    ) as e:  # the error file is already written; the caller falls back to Z0
        print(f"prepass failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    return 0


def _brief(args) -> int:
    cand = Path(args.candidate_sb)
    sheet = None
    try:
        sha = hashlib.sha256(cand.read_bytes()).hexdigest()
        if args.sheet:
            sheet = {
                "path": str(Path(args.sheet).resolve()),
                "text": Path(args.sheet).read_text(encoding="utf-8"),
            }
        out = briefs.render(
            args.arm,
            {"cand_sb": str(cand), "sha": sha},
            sheet,
            args.source,
            fallback=args.fallback,
        )
    except (OSError, ValueError) as e:
        print(f"brief failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out["text"], encoding="utf-8")
    dest.with_suffix(".sha256").write_text(out["sha256"] + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "text"}, sort_keys=True))
    return 0


def _normalise(args) -> int:
    try:
        info = normalise.normalise_file(Path(args.report), Path(args.out_dir), args.rid)
    except OSError as e:
        print(f"normalise failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    print(json.dumps(info, sort_keys=True))
    return 0


def run_check(
    run: Path,
    candidate: Path,
    source: Path | None = None,
    out_dir: Path | None = None,
) -> dict:
    """S5 for one run folder (C4): writes check/<rid>.checked.md, check/<rid>.ledger.json and check/check.json.

    Returns check.json. Raises on any error; nothing is written before every reviewer has been checked.
    """
    out_dir = Path(out_dir) if out_dir else run / "check"
    items = json.loads((run / "prepass" / "items.json").read_text(encoding="utf-8"))[
        "items"
    ]
    reviewers = json.loads(
        (run / "prepass" / "assignment.json").read_text(encoding="utf-8")
    )["reviewers"]
    cand = candidate.read_text(encoding="utf-8")
    src = source.read_text(encoding="utf-8") if source else None
    results, texts, no_report = {}, {}, []
    for rid, assigned in reviewers.items():
        report_path = run / "reviews" / f"{rid}.md"
        if not report_path.is_file():
            no_report.append(rid)
            continue
        transcript_path = run / "reviews" / f"{rid}.attempt1.json"
        results[rid] = ledgerv1.check_report(
            report_path.read_text(encoding="utf-8"),
            assigned=assigned,
            candidate=cand,
            source=src,
            items=items,
            transcript=ledgerv1.read_transcript(transcript_path)
            if transcript_path.is_file()
            else (),
        )
        texts[rid] = results[rid].pop("text")
    summary = ledgerv1.summarise(
        results, {i["item_id"]: i["class"] for i in items if i.get("class")}, no_report
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    for rid, res in results.items():
        (out_dir / f"{rid}.checked.md").write_text(texts[rid], encoding="utf-8")
        (out_dir / f"{rid}.ledger.json").write_text(
            json.dumps({"rid": rid, **res}, indent=1, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    (out_dir / "check.json").write_text(
        json.dumps(summary, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def _check(args) -> int:
    try:
        summary = run_check(
            Path(args.run_dir),
            Path(args.candidate),
            Path(args.source) if args.source else None,
            Path(args.out_dir) if args.out_dir else None,
        )
    except Exception as e:  # the caller sets check_skipped (DESIGN 10 row 11)
        print(f"check failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 0


def _clock_plan(args) -> int:
    """The numbers bin/run-panel.sh needs before it starts: b, expected overhead, kill limit, hang guard, no_budget."""
    try:
        values = (
            clock.load_values(Path(args.values)) if args.values else clock.load_values()
        )
        b = values["b"][args.panel][args.doc]
        overhead = clock.expected_overhead(args.arm, args.panel, values)
        out = {
            "b": b,
            "expected_overhead_s": overhead,
            "kill_s": clock.kill_s(b, values),
            "hang_s": clock.hang_s(b, overhead, values),
            "no_budget": clock.no_budget(b, values),
            "sweep_version": prepass.SWEEP_VERSION,
            "values": values,
        }
    except (OSError, KeyError, ValueError) as e:
        print(f"clock plan failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    print(json.dumps(out, sort_keys=True))
    return 0


def _clock_timing(args) -> int:
    """timing.json (DESIGN 11.4) from the event times the launcher wrote: lines `<event><TAB><epoch seconds>`.

    Events: t0, prepass_start, prepass_end, render_start, render_end, s5_start, s5_end, rev_start:<rid>,
    rev_end:<rid>. They are replayed in time order (ties keep file order) through PanelClock, so the arithmetic is the
    one test_clock.py tests. `stage_t` (the raw start and end of each stage) is added for the launcher tests.
    """
    try:
        events = []
        for line in Path(args.events).read_text(encoding="utf-8").splitlines():
            name, _, t = line.partition("\t")
            events.append((float(t), len(events), name))
        now = [0.0]
        c = clock.PanelClock(args.arm, lambda: now[0])
        for t, _, name in sorted(events):
            now[0] = t
            if name == "t0":
                c.start()
            elif name.startswith("rev_start:"):
                c.reviewer_start(name.split(":", 1)[1])
            elif name.startswith("rev_end:"):
                c.reviewer_end(name.split(":", 1)[1])
            elif name.endswith("_start"):
                c.stage_start(name[: -len("_start")])
            elif name.endswith("_end"):
                c.stage_end(name[: -len("_end")])
            else:
                raise ValueError(f"unknown clock event {name!r}")
        out = {**c.timing(), "stage_t": c.stage_t}
    except (OSError, ValueError, clock.ClockError) as e:
        print(f"clock timing failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


def _clock_spike(args) -> int:
    """Print the spike plan as JSON (`ok`, `fallback`, ...); --panels-out writes the panel file a schedule run uses."""
    try:
        values = (
            clock.load_values(Path(args.values)) if args.values else clock.load_values()
        )
        plan = clock.spike_plan(values)
        if args.panels_out:
            src = (
                Path(args.panels)
                if args.panels
                else Path(_SW) / "config" / "panels.json"
            )
            panels = json.loads(src.read_text(encoding="utf-8"))
            if plan["fallback"]:
                panels = clock.fallback_panels(panels)
            dest = Path(args.panels_out)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(
                json.dumps(panels, indent=1, sort_keys=True) + "\n", encoding="utf-8"
            )
    except (OSError, KeyError, ValueError) as e:
        print(f"clock spike failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    print(json.dumps(plan, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="sweep", description="The sweep sheet tools.")
    sub = ap.add_subparsers(
        dest="cmd", required=True, metavar="{prepass,lint,brief,normalise,check,clock}"
    )

    p = sub.add_parser(
        "prepass", help="extract, select, assign and render the sheets (S1 to S3)"
    )
    p.add_argument("--candidate", required=True, help="the candidate plan")
    p.add_argument("--source", help="the source document, when there is one")
    p.add_argument(
        "--repo", required=True, help="the repository snapshot (a git checkout)"
    )
    p.add_argument("--seed", required=True, type=int)
    p.add_argument(
        "--out", required=True, help="the run folder; prepass/ is made inside it"
    )
    p.add_argument("--panel", default="primary", choices=sorted(assign.load_panels()))
    p.add_argument(
        "--available",
        help="comma-separated reviewer ids that can still be launched (DESIGN 7.3); default all of the panel",
    )
    p.set_defaults(run=_prepass)

    sub.add_parser(
        "lint", help="AO-1 leak lint (arguments as scaffold/lint.py)", add_help=False
    )

    b = sub.add_parser("brief", help="render one reviewer's brief")
    b.add_argument("--arm", required=True, choices=briefs.ARMS)
    b.add_argument(
        "--candidate-sb",
        required=True,
        help="absolute path of the candidate in the sandbox",
    )
    b.add_argument(
        "--source", help="absolute path of the source document; none leaves CB-1 out"
    )
    b.add_argument(
        "--sheet",
        help="sheets/<rid>.md (arm SS); none or an empty file is an empty sheet",
    )
    b.add_argument(
        "--fallback",
        action="store_true",
        help="the pre-pass failed: arm SS gets the Z0 parts",
    )
    b.add_argument(
        "--out",
        required=True,
        help="the brief file; <stem>.sha256 is written beside it",
    )
    b.set_defaults(run=_brief)

    n = sub.add_parser(
        "normalise", help="H2: cut anchors and claims to the merge limits"
    )
    n.add_argument("--report", required=True, help="the reviewer report to normalise")
    n.add_argument("--out-dir", required=True, help="writes <rid>.md and h2.json here")
    n.add_argument("--rid", required=True)
    n.set_defaults(run=_normalise)

    c = sub.add_parser(
        "check",
        help="S5: parse the ledgers, demote, promote; writes check/ (raw reports are only read)",
    )
    c.add_argument(
        "--run",
        dest="run_dir",
        required=True,
        help="the run folder: prepass/items.json, prepass/assignment.json and reviews/<rid>.md are read",
    )
    c.add_argument(
        "--candidate", required=True, help="the candidate plan (the sandbox copy)"
    )
    c.add_argument("--source", help="the source document, when there is one")
    c.add_argument("--out-dir", help="default RUN/check")
    c.set_defaults(run=_check)

    k = sub.add_parser(
        "clock",
        help="the numbers and the timing.json of bin/run-panel.sh (DESIGN 11.4, 11.5)",
    )
    ks = k.add_subparsers(
        dest="clock_cmd", required=True, metavar="{plan,timing,spike}"
    )
    ksp = ks.add_parser(
        "spike",
        help="the spike record and its fallback (REQ-32); with --panels-out writes the panel file of the run",
    )
    ksp.add_argument("--values", help="a values file (default config/values.json)")
    ksp.add_argument(
        "--panels", help="the panel file to copy (default config/panels.json)"
    )
    ksp.add_argument(
        "--panels-out",
        help="write the panel file here: the fallback caps when the fallback applies",
    )
    ksp.set_defaults(run=_clock_spike)
    kp = ks.add_parser(
        "plan", help="print b, kill_s, hang_s, no_budget and the values as JSON"
    )
    kp.add_argument("--arm", required=True, choices=briefs.ARMS)
    kp.add_argument("--panel", required=True)
    kp.add_argument("--doc", required=True)
    kp.add_argument("--values", help="a values file (default config/values.json)")
    kp.set_defaults(run=_clock_plan)
    kt = ks.add_parser(
        "timing", help="write timing.json from the launcher's event times"
    )
    kt.add_argument("--arm", required=True, choices=briefs.ARMS)
    kt.add_argument("--events", required=True)
    kt.add_argument("--out", required=True)
    kt.set_defaults(run=_clock_timing)
    return ap


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv and argv[0] in DELEGATED:
        return DELEGATED[argv[0]](argv[1:])
    args = build_parser().parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
