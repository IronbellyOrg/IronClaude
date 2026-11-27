"""Event log: one JSON line per event, append-only, plus the commands that record the owner's input, the price and the go.

Command line (each takes ``--root``, the experiment folder by default):
  events.py owner-input --evidence PATH --note TEXT
  events.py price --usd-per-mtok VALUE --source TEXT
  events.py go --words TEXT
The other events (freeze, rule_freeze, gate1, gate2, tests_passed, first_request, run_end, scoring, verdict) are written by the
module that does the work, through ``append_event``.  This module never rewrites or deletes a line.
"""
import argparse
import datetime
import json
import os
import pathlib
import sys

_EXP = pathlib.Path(__file__).resolve().parents[1]
_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
for _p in (str(_EXP), str(_JEV)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from harness import loader  # noqa: E402

EVENTS = ("owner_input_received", "freeze", "rule_freeze", "gate1", "gate2", "tests_passed", "price_confirmed", "lead_go",
          "first_request", "run_end", "scoring", "verdict")
_CORE = ("ts", "event", "evidence", "evidence_sha256")


def _evidence_path(paths, evidence):
    p = pathlib.Path(evidence)
    try:
        return str(p.resolve().relative_to(paths.root.resolve()))
    except ValueError:
        return str(p)


def append_event(paths, event, evidence=None, **fields):
    """Append one event line (sorted keys, UTC timestamp, the evidence path and the evidence file's SHA-256) and return it.

    An event with no evidence of its own is tied to the rule file in force when it was written, so the line still carries a path
    and a hash.  An evidence path that is not a file is refused.  Only a log with no rule file yet leaves both null.
    """
    if event not in EVENTS:
        raise ValueError(f"unknown event {event!r}")
    clash = [k for k in fields if k in _CORE]
    if clash:
        raise ValueError(f"event field names reserved: {clash}")
    if evidence is None and paths.rule.is_file():
        evidence = paths.rule
    ev_path, ev_sha = None, None
    if evidence is not None:
        if not pathlib.Path(evidence).is_file():
            raise ValueError(f"evidence file does not exist: {evidence}")
        ev_path = _evidence_path(paths, evidence)
        ev_sha = loader.sha256_file(evidence)
    rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "event": event,
           "evidence": ev_path, "evidence_sha256": ev_sha, **fields}
    paths.events.parent.mkdir(parents=True, exist_ok=True)
    with open(paths.events, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return rec


def read_events(paths):
    """Every event in the log, oldest first; an empty list when there is no log."""
    if not paths.events.is_file():
        return []
    return [json.loads(line) for line in paths.events.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest(paths, name):
    """The newest event with this name, or ``None``."""
    found = [e for e in read_events(paths) if e["event"] == name]
    return found[-1] if found else None


def main(argv=None):
    ap = argparse.ArgumentParser(prog="events.py", description="record owner input, the confirmed price and the lead's go")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("owner-input", help="record that the owner gave input, with the file that holds it")
    a.add_argument("--evidence", required=True)
    a.add_argument("--note", required=True)
    b = sub.add_parser("price", help="record the re-confirmed price per million input tokens")
    b.add_argument("--usd-per-mtok", type=float, required=True)
    b.add_argument("--source", required=True)
    c = sub.add_parser("go", help="record the lead's go, naming the rule file's current hash")
    c.add_argument("--words", required=True)
    for p in (a, b, c):
        p.add_argument("--root", default=None)
    args = ap.parse_args(argv)
    paths = loader.Paths(args.root)
    if args.cmd == "owner-input":
        ev = pathlib.Path(args.evidence)
        if not ev.is_file() and (paths.root / ev).is_file():
            ev = paths.root / ev
        if not ev.is_file():
            ap.error(f"--evidence {args.evidence} is not a file")
        rec = append_event(paths, "owner_input_received", evidence=ev, note=args.note)
    elif args.cmd == "price":
        if not args.usd_per_mtok > 0:
            ap.error("--usd-per-mtok must be above zero")
        rec = append_event(paths, "price_confirmed", usd_per_mtok=args.usd_per_mtok, source=args.source)
    else:
        if not paths.rule.is_file():
            ap.error("no rule file to name in the go")
        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), route=loader.GATEWAY_URL,
                           words=args.words)
    print(json.dumps(rec, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
