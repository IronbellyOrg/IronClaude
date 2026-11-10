#!/usr/bin/env python3
"""review_ledger.py: the script-kept finding ledger for document review loops.

The script is the only writer of the ledger. Models write small JSON inputs (or a
report holding one fenced ``ledger-input`` block) and their own reports; the
script validates and ingests them atomically. The actor is implied by the
subcommand: there is no role flag, no event log and no version-control call
(snapshots are plain copies, because a reviewed document may be untracked).

Ledger folder: ``<doc dir>/<doc stem>.review-ledger/`` (or ``--ledger <dir>``),
holding ``ledger.json``, ``snapshots/``, ``diffs/``, ``inputs/`` and ``.lock``.

Output: one JSON object on stdout. Exit codes: 0 committed (whatever the
decision), 1 usage, 2 row-level input refused, 3 state refused, 4 lock or
sequence conflict. ``verdict`` alone exits 0 PASS, 10 CONTINUE, 11 ESCALATE,
12 PENDING (the loop is terminal and the sweep has not run).

``--dry-run`` (on the input-taking subcommands) validates the input against the
current ledger and prints the would-be result; it takes no lock and writes no
file anywhere.
"""

import argparse
import difflib
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

SCHEMA = 1
CAP_REVIEWS = 3  # tied by a test to "at most 2 fix cycles (3 reviews)"
HUNKS_LARGE_SHARE = 0.4  # changed lines above this share of the document: HUNKS_LARGE

GRADES_SPEC_PANEL = ("CRITICAL", "MAJOR", "MINOR")


def _blocking_spec_panel(row: dict) -> bool:
    grade = row["grade"]
    rule = (row.get("rule") or "").strip().upper()
    wrong = (row.get("wrong_outcome") or "").strip()
    return (
        grade == "CRITICAL"
        or rule in {"FR-8", "FR-9"}
        or (grade == "MAJOR" and bool(wrong))
    )


# One row per profile: grade vocabulary, blocking predicate, cap.
PROFILES = {
    "spec-panel": {
        "grades": GRADES_SPEC_PANEL,
        "blocking": _blocking_spec_panel,
        "cap_reviews": CAP_REVIEWS,
    },
}

PHASES = ("find", "revise", "verify", "terminal", "swept")
EXIT_OK, EXIT_USAGE, EXIT_INPUT, EXIT_STATE, EXIT_CONFLICT = 0, 1, 2, 3, 4
VERDICT_EXIT = {"PASS": 0, "CONTINUE": 10, "ESCALATE": 11, "PENDING": 12}
ROW_INPUT_KEYS = {"grade", "rule", "wrong_outcome", "anchor", "finding", "label"}
ANSWER_ACTIONS = ("fixed", "not-fixed", "disputed")
LIVE_STATUSES = {"open", "fixed", "reopened"}

# --dry-run: atomic_write records the path instead of writing.
_DRY = {"on": False, "would_write": []}


class Refusal(Exception):
    def __init__(self, code: str, detail, exit_code: int, next_action: str = ""):
        super().__init__(code)
        self.code, self.detail, self.exit_code, self.next_action = (
            code,
            detail,
            exit_code,
            next_action,
        )


def refuse(code: str, detail, exit_code: int, next_action: str = "") -> None:
    raise Refusal(code, detail, exit_code, next_action)


# ---------------------------------------------------------------- utilities


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def canonical(obj) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def body_digest(state: dict) -> str:
    return sha256_bytes(
        canonical({k: v for k, v in state.items() if k != "body_sha256"})
    )


def atomic_write(path: Path, data: bytes) -> None:
    if _DRY["on"]:
        _DRY["would_write"].append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def flat(text: str) -> str:
    return " ".join(text.split())


def locate(text: str, quote: str) -> list[tuple[int, int]]:
    """Every occurrence of ``quote`` in ``text`` as a half-open 0-based line range.

    Matching is whitespace-normalized, so a quote copied across a line wrap is
    still found.
    """
    q = flat(quote)
    if not q:
        return []
    chars: list[str] = []
    line_of: list[int] = []
    line = 0
    prev_space = True
    for ch in text:
        if ch.isspace():
            if not prev_space:
                chars.append(" ")
                line_of.append(line)
                prev_space = True
        else:
            chars.append(ch)
            line_of.append(line)
            prev_space = False
        if ch == "\n":
            line += 1
    norm = "".join(chars)
    out = []
    start = norm.find(q)
    while start != -1:
        end = start + len(q) - 1
        out.append((line_of[start], line_of[end] + 1))
        start = norm.find(q, start + 1)
    return out


# ---------------------------------------------------------------- diff, units, spans

LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")


def overlaps(a, b) -> bool:
    """Half-open line ranges; a zero-width range at p overlaps [s, e) when s <= p <= e."""
    a1, a2 = a
    b1, b2 = b
    if a1 == a2:
        return b1 <= a1 <= b2
    if b1 == b2:
        return a1 <= b1 <= a2
    return a1 < b2 and b1 < a2


def units(lines: list[str]) -> list[tuple[int, int]]:
    """Admission units: maximal runs of non-blank lines, except that each table
    row (a line starting ``|``) and each list item (with its continuation lines)
    is its own unit."""
    out: list[tuple[int, int]] = []
    cur = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            if cur:
                out.append(tuple(cur))
                cur = None
            continue
        if s.startswith("|"):
            if cur:
                out.append(tuple(cur))
                cur = None
            out.append((i, i + 1))
            continue
        if LIST_ITEM.match(line):
            if cur:
                out.append(tuple(cur))
            cur = [i, i + 1]
            continue
        if cur:
            cur[1] = i + 1
        else:
            cur = [i, i + 1]
    if cur:
        out.append(tuple(cur))
    return out


def widen(span, unit_list) -> tuple[int, int]:
    """Widen a span to the admission units it overlaps."""
    s, e = span
    hit = [u for u in unit_list if overlaps((s, e), u)]
    if not hit:
        return (s, e)
    return (min(s, min(u[0] for u in hit)), max(e, max(u[1] for u in hit)))


def diff_lines(old: list[str], new: list[str]):
    """Whitespace-insensitive line diff (autojunk off). Returns (hunks, opcodes)."""
    sm = difflib.SequenceMatcher(
        None, [flat(x) for x in old], [flat(x) for x in new], autojunk=False
    )
    opcodes = sm.get_opcodes()
    old_units, new_units = units(old), units(new)
    hunks = []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            continue
        old_t, new_t = "\n".join(old[i1:i2]), "\n".join(new[j1:j2])
        uo = [u for u in old_units if overlaps((i1, i2), u)]
        un = [u for u in new_units if overlaps((j1, j2), u)]
        o_par = flat("\n".join("\n".join(old[a:b]) for a, b in uo))
        n_par = flat("\n".join("\n".join(new[a:b]) for a, b in un))
        hunks.append(
            {
                "n": len(hunks) + 1,
                "old": [i1, i2],
                "new": [j1, j2],
                "old_text": old_t,
                "new_text": new_t,
                "old_bytes": len(old_t.encode("utf-8")),
                "new_bytes": len(new_t.encode("utf-8")),
                "bytes": max(len(old_t.encode("utf-8")), len(new_t.encode("utf-8"))),
                "key": f"{i1}:{i2}:{sha256_text(new_t)[:16]}",
                "rewrap": bool(uo) and bool(un) and o_par == n_par,
            }
        )
    return hunks, opcodes


def map_pos(i: int, opcodes) -> int:
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal" and i1 <= i < i2:
            return j1 + (i - i1)
        if i < i1:
            return j1
    return opcodes[-1][4] if opcodes else i


def map_span(span, opcodes, hunks, new_text: str, anchor: str):
    """Relocate a row's span from the old snapshot into the new text.

    Returns (span or None, method); method is unchanged, exact, rewritten-in-hunk,
    missing or ambiguous.
    """
    s, e = span
    touching = [h for h in hunks if overlaps(h["old"], (s, e))]
    if not touching:
        if s == e:
            p = map_pos(s, opcodes)
            return (p, p), "unchanged"
        return (map_pos(s, opcodes), map_pos(e - 1, opcodes) + 1), "unchanged"
    occ = locate(new_text, anchor)
    region = (min(h["new"][0] for h in touching), max(h["new"][1] for h in touching))
    if len(occ) == 1:
        return occ[0], "exact"
    if len(occ) > 1:
        inside = [o for o in occ if overlaps(o, region)]
        if len(inside) == 1:
            return inside[0], "exact"
        return None, "ambiguous"
    covered = all(
        any(h["old"][0] <= i < h["old"][1] for h in touching) for i in range(s, e)
    )
    if covered:
        return region, "rewritten-in-hunk"
    return None, "missing"


def revert_hunks(lines: list[str], hunks: list[dict], old: list[str]):
    """Restore each hunk's old text, preimage-checked. Returns (lines, reverted, failed)."""
    out = list(lines)
    reverted, failed = [], []
    for h in sorted(hunks, key=lambda x: x["new"][0], reverse=True):
        j1, j2 = h["new"]
        if "\n".join(out[j1:j2]) != h["new_text"]:
            failed.append(h["n"])
            continue
        out[j1:j2] = old[h["old"][0] : h["old"][1]]
        reverted.append(h["n"])
    return out, sorted(reverted), sorted(failed)


def join_lines(lines: list[str], trailing_newline: bool) -> str:
    text = "\n".join(lines)
    return text + "\n" if trailing_newline and lines else text


# ---------------------------------------------------------------- ledger I/O


class Ledger:
    def __init__(self, root: Path):
        self.root = root
        self.state_path = root / "ledger.json"

    def exists(self) -> bool:
        return self.state_path.is_file()

    def load(self) -> dict:
        if not self.exists():
            refuse(
                "E-NO-LEDGER",
                f"no ledger at {self.root}",
                EXIT_STATE,
                "pass --ledger or --doc for an existing ledger, or run init",
            )
        raw = self.state_path.read_bytes()
        try:
            state = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            refuse(
                "E-TAMPERED",
                "ledger.json is not valid JSON",
                EXIT_STATE,
                "restore ledger.json; never hand-edit it",
            )
        if not isinstance(state, dict) or state.get("body_sha256") != body_digest(
            state
        ):
            refuse(
                "E-TAMPERED",
                "ledger.json body_sha256 does not match its content",
                EXIT_STATE,
                "restore ledger.json; never hand-edit it",
            )
        return state

    def save(self, state: dict) -> None:
        state["body_sha256"] = body_digest(state)
        atomic_write(
            self.state_path,
            json.dumps(state, indent=2, ensure_ascii=False).encode("utf-8") + b"\n",
        )

    def lock(self):
        self.root.mkdir(parents=True, exist_ok=True)
        fh = open(self.root / ".lock", "a+")
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            fh.close()
            refuse(
                "E-LOCKED",
                f"another writer holds {self.root / '.lock'}",
                EXIT_CONFLICT,
                "wait for the other writer, read status, then retry",
            )
        return fh

    def doc_path(self, state: dict) -> Path:
        return (self.root / state["doc"]).resolve()

    def snapshot_path(self, name: str) -> Path:
        return self.root / "snapshots" / f"{name}.md"


def ledger_root(args) -> Path:
    if getattr(args, "ledger", None):
        return Path(args.ledger)
    doc = getattr(args, "doc", None)
    if not doc:
        usage("pass --ledger <dir> or --doc <document>")
    d = Path(doc)
    return d.parent / f"{d.stem}.review-ledger"


def usage(msg: str) -> None:
    refuse("E-USAGE", msg, EXIT_USAGE, "see --help")


def read_input(path_str: str) -> tuple[object, bytes]:
    """Read ``--input``: a .json file, or a .md report with one ``ledger-input`` block."""
    path = Path(path_str)
    if not path.is_file():
        refuse(
            "E-SCHEMA",
            f"input file not found: {path}",
            EXIT_INPUT,
            "write the input file first",
        )
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        blocks = re.findall(
            r"^```ledger-input[ \t]*\n(.*?)^```[ \t]*$", text, re.M | re.S
        )
        if len(blocks) != 1:
            refuse(
                "E-SCHEMA",
                f"{path} holds {len(blocks)} ledger-input blocks; exactly one is required",
                EXIT_INPUT,
                "put exactly one ```ledger-input fenced block in the report",
            )
        text = blocks[0]
    elif path.suffix != ".json":
        refuse(
            "E-SCHEMA",
            f"input must be a .json file or a .md report: {path}",
            EXIT_INPUT,
            "",
        )
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        refuse(
            "E-SCHEMA", f"input is not valid JSON: {exc}", EXIT_INPUT, "fix the JSON"
        )
    return data, canonical(data)


# ---------------------------------------------------------------- state helpers


def new_state(doc_rel: str, profile: str) -> dict:
    return {
        "schema": SCHEMA,
        "profile": profile,
        "doc": doc_rel,
        "cap_reviews": PROFILES[profile]["cap_reviews"],
        "round": 1,
        "fix_cycles": 0,
        "phase": "find",
        "seq": 0,
        "snapshots": {},
        "decisions": [],
        "ops": [],
        "rows": [],
        "body_sha256": "",
    }


def review_header(state: dict) -> str:
    return f"review: {state['round']} of {state['cap_reviews']}"


def committed_ops(state: dict, cmd: str, rnd: int) -> list[dict]:
    return [o for o in state["ops"] if o["cmd"] == cmd and o["round"] == rnd]


def last_decision(state: dict, kind: str = "review") -> dict | None:
    found = [d for d in state["decisions"] if d["kind"] == kind]
    return found[-1] if found else None


def u_count(state: dict) -> int:
    return sum(
        1
        for r in state["rows"]
        if r["blocking"] and r["scope"] == "in" and r["status"] in LIVE_STATUSES
    )


def snapshots_intact(ledger: Ledger, state: dict) -> bool:
    for name, meta in state["snapshots"].items():
        p = ledger.snapshot_path(name)
        if not p.is_file() or sha256_bytes(p.read_bytes()) != meta["sha256"]:
            return False
    return True


def round_x_items(state: dict, k: int) -> list:
    """X items of review k: cannot-verify answers, unmappable anchors, failed revert preimages."""
    return [
        item
        for op in state["ops"]
        for item in op.get("x_items", [])
        if item["round"] == k
    ]


def counts(state: dict) -> dict:
    rows = state["rows"]
    out = {
        "rows": len(rows),
        "blocking": sum(1 for r in rows if r["blocking"]),
        "U": u_count(state),
        "X": len(round_x_items(state, state["round"])),
    }
    for s in ("open", "fixed", "verified", "reopened", "deferred"):
        out[s] = sum(1 for r in rows if r["status"] == s)
    return out


def loop_decision(state: dict) -> str | None:
    d = last_decision(state)
    return d["loop_decision"] if d else None


def delivery_outcome(state: dict) -> str | None:
    d = last_decision(state, "sweep")
    return d["delivery_outcome"] if d else None


def next_action(state: dict) -> str:
    phase = state["phase"]
    if phase == "find":
        if committed_ops(state, "find", 1):
            return "close --report <review report>"
        return "run the panel, then find --input <report or json>"
    if phase == "revise":
        return "reviser edits the document; then begin --doc <document> for the next review"
    if phase == "verify":
        if committed_ops(state, "verify", state["round"]):
            return "close --report <review report>"
        return f"answer every row of plan-r{state['round']}.md, then verify --input <report or json>"
    if phase == "terminal":
        return "run the sweep once: sweep --prepare, then sweep --input <report> --report <report>"
    return "done: read verdict"


def result(state: dict, **extra) -> dict:
    out = {
        "ok": True,
        "seq": state["seq"],
        "phase": state["phase"],
        "review": state["round"],
        "fix_cycles": state["fix_cycles"],
        "counts": counts(state),
        "loop_decision": loop_decision(state),
        "delivery_outcome": delivery_outcome(state),
        "next_action": next_action(state),
    }
    out.update(extra)
    return out


def render_rows(state: dict) -> list[str]:
    lines = [
        "| id | grade | rule | blocking | status | scope | anchor |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in state["rows"]:
        anchor = flat(r["anchor"]).replace("|", "\\|")
        lines.append(
            f"| {r['id']} | {r['grade']} | {r.get('rule') or ''} | {'yes' if r['blocking'] else 'no'} "
            f"| {r['status']} | {r['scope']} | {anchor} |"
        )
    return lines


def row_by_id(state: dict, rid: str) -> dict | None:
    return next((r for r in state["rows"] if r["id"] == rid), None)


def current_span(row: dict, snap: str):
    """The row's span in snapshot ``snap`` (None when it could not be mapped there)."""
    for m in reversed(row.get("mappings", [])):
        if m["snapshot"] == snap:
            return tuple(m["span"]) if m["span"] is not None else None
    if row.get("at_snapshot", "r1") == snap and row.get("at") is not None:
        return tuple(row["at"])
    return None


def last_snapshot(state: dict) -> str:
    return f"r{state['round']}"


def doc_lines(text: str) -> list[str]:
    return text.splitlines()


def provisional(ledger: Ledger, state: dict):
    """Hunks between the last snapshot and the live document (phase revise)."""
    old = ledger.snapshot_path(last_snapshot(state)).read_text(encoding="utf-8")
    live = ledger.doc_path(state).read_text(encoding="utf-8")
    hunks, opcodes = diff_lines(doc_lines(old), doc_lines(live))
    return old, live, hunks, opcodes


def stored_answers(state: dict) -> list[dict]:
    """Reviser claims stored by answer in the current revise phase."""
    return [
        c
        for op in committed_ops(state, "answer", state["round"])
        for c in op.get("claims", [])
    ]


# ---------------------------------------------------------------- mutation frame


def mutate(args, cmd: str, read_payload, apply):
    """Check integrity, read the input, lock, reload, replay identical requests, check seq, apply, save.

    With --dry-run: no lock, no replay, no write; the would-be result is printed.
    """
    ledger = Ledger(ledger_root(args))
    ledger.load()  # E-NO-LEDGER or E-TAMPERED before anything else is read or locked
    payload_bytes = read_payload()
    if getattr(args, "dry_run", False):
        state = ledger.load()
        _DRY["on"], _DRY["would_write"] = True, []
        try:
            state["seq"] += 1
            extra = apply(ledger, state) or {}
            state["ops"].append(
                {
                    "cmd": cmd,
                    "op": None,
                    "digest": "",
                    "round": state["round"],
                    "round_after": state["round"],
                    "phase_after": state["phase"],
                    **extra.pop("_op", {}),
                }
            )
            extra.pop("_after", None)
            return result(
                state, **extra, dry_run=True, would_write=list(_DRY["would_write"])
            )
        finally:
            _DRY["on"] = False
    if args.op is None or args.expect_seq is None:
        usage("--op and --expect-seq are required unless --dry-run is given")
    fh = ledger.lock()
    try:
        state = ledger.load()
        digest = sha256_bytes(cmd.encode() + b"\0" + payload_bytes)
        for op in state["ops"]:
            same_state = (op["phase_after"], op["round_after"]) == (
                state["phase"],
                state["round"],
            )
            # an op that changed the document replays only while the document is as it left it
            doc_unchanged = op.get("doc_after") in (
                None,
                live_binding(args)["doc_sha256"],
            )
            if op["digest"] == digest and same_state and doc_unchanged:
                on_replay = getattr(apply, "on_replay", None)
                if on_replay:
                    on_replay(ledger, state, op)
                return dict(op["result"], replayed=True)
            if op["op"] == args.op and op["digest"] != digest:
                refuse(
                    "E-OP-CONFLICT",
                    f"op id {args.op!r} was used for a different request",
                    EXIT_CONFLICT,
                    "use a new --op id",
                )
        if args.expect_seq != state["seq"]:
            refuse(
                "E-STALE-SEQ",
                f"--expect-seq {args.expect_seq} but the ledger is at seq {state['seq']}",
                EXIT_CONFLICT,
                "read status, then retry with the current seq",
            )
        phase_before, round_before = state["phase"], state["round"]
        state["seq"] += 1
        extra = apply(ledger, state) or {}
        op_data = extra.pop("_op", {})
        after = extra.pop("_after", None)
        entry = {
            "op": args.op,
            "cmd": cmd,
            "digest": digest,
            "seq": state["seq"],
            "phase_before": phase_before,
            "round": round_before,
            "phase_after": state["phase"],
            "round_after": state["round"],
            **op_data,
        }
        state["ops"].append(entry)  # before result(), so counts see this op's X items
        out = result(state, **extra)
        entry["result"] = out
        ledger.save(state)
        if after:
            after()
        return out
    finally:
        fh.close()


def require_phase(state: dict, *phases: str) -> None:
    if state["phase"] not in phases:
        code = "E-TERMINAL" if state["phase"] in ("terminal", "swept") else "E-PHASE"
        refuse(
            code,
            f"phase is {state['phase']}; this subcommand needs {' or '.join(phases)}",
            EXIT_STATE,
            next_action(state),
        )


def input_reader(path_str: str):
    """Return (read, got): read() parses --input after the ledger hash check."""
    got: dict = {}

    def read() -> bytes:
        got["data"], got["payload"] = read_input(path_str)
        return got["payload"]

    return read, got


# ---------------------------------------------------------------- subcommands


def cmd_init(args) -> dict:
    if args.profile not in PROFILES:
        usage(f"unknown profile {args.profile!r}; known: {', '.join(PROFILES)}")
    doc = Path(args.doc)
    if not doc.is_file():
        usage(f"document not found: {doc}")
    ledger = Ledger(ledger_root(args))
    archived = None
    if ledger.root.exists():
        if not args.archive_existing:
            refuse(
                "E-EXISTS",
                f"a ledger already exists at {ledger.root}",
                EXIT_STATE,
                "continue it with begin, or rerun init with --archive-existing to start over",
            )
        fh = Ledger(ledger.root).lock()
        try:
            stamp = 1
            while True:
                target = ledger.root.with_name(f"{ledger.root.name}.archived-{stamp}")
                if not target.exists():
                    break
                stamp += 1
            os.rename(ledger.root, target)
            archived = str(target.resolve())
        finally:
            fh.close()
    fh = ledger.lock()
    try:
        for sub in ("snapshots", "diffs", "inputs"):
            (ledger.root / sub).mkdir(parents=True, exist_ok=True)
        data = doc.read_bytes()
        atomic_write(ledger.snapshot_path("r1"), data)
        state = new_state(
            os.path.relpath(doc.resolve(), ledger.root.resolve()), args.profile
        )
        state["snapshots"]["r1"] = {"sha256": sha256_bytes(data), "bytes": len(data)}
        state["seq"] = 1
        out = result(
            state,
            review_header=review_header(state),
            ledger=str(ledger.root),
            archived=archived,
        )
        state["ops"].append(
            {
                "op": args.op or "init",
                "cmd": "init",
                "digest": "",
                "seq": 1,
                "phase_before": None,
                "round": 1,
                "phase_after": "find",
                "round_after": 1,
                "result": out,
            }
        )
        ledger.save(state)
        return out
    finally:
        fh.close()


def validate_rows(data, grades) -> list[dict]:
    if not isinstance(data, list):
        refuse(
            "E-SCHEMA",
            "find input must be a JSON array of rows",
            EXIT_INPUT,
            "fix the input shape",
        )
    problems = []
    for i, row in enumerate(data):
        if not isinstance(row, dict):
            problems.append(
                {"index": i, "code": "E-SCHEMA", "detail": "row is not an object"}
            )
            continue
        extra = set(row) - ROW_INPUT_KEYS
        if extra:
            problems.append(
                {
                    "index": i,
                    "code": "E-SCHEMA",
                    "detail": f"unknown keys {sorted(extra)}",
                }
            )
        if row.get("grade") not in grades:
            problems.append(
                {
                    "index": i,
                    "code": "E-SCHEMA",
                    "detail": f"grade must be one of {list(grades)}",
                }
            )
        for key in ("anchor", "finding"):
            if not isinstance(row.get(key), str) or not row.get(key).strip():
                problems.append(
                    {
                        "index": i,
                        "code": "E-SCHEMA",
                        "detail": f"{key} must be a non-empty string",
                    }
                )
        for key in ("rule", "wrong_outcome", "label"):
            if row.get(key) is not None and not isinstance(row.get(key), str):
                problems.append(
                    {
                        "index": i,
                        "code": "E-SCHEMA",
                        "detail": f"{key} must be a string or null",
                    }
                )
    if problems:
        refuse(
            "E-SCHEMA", problems, EXIT_INPUT, "fix the listed rows; nothing was written"
        )
    return data


def check_anchors(rows: list[dict], text: str) -> list[tuple[int, int]]:
    spans, problems = [], []
    for i, row in enumerate(rows):
        hits = locate(text, row["anchor"])
        if not hits:
            problems.append(
                {"index": i, "code": "E-ANCHOR", "detail": "anchor quote not found"}
            )
        elif len(hits) > 1:
            problems.append(
                {
                    "index": i,
                    "code": "E-ANCHOR-AMBIGUOUS",
                    "detail": f"anchor occurs {len(hits)} times, at lines {[h[0] + 1 for h in hits]}",
                }
            )
        else:
            spans.append(hits[0])
    if problems:
        code = (
            "E-ANCHOR"
            if any(p["code"] == "E-ANCHOR" for p in problems)
            else "E-ANCHOR-AMBIGUOUS"
        )
        refuse(
            code,
            problems,
            EXIT_INPUT,
            "quote each anchor exactly once from the reviewed text",
        )
    return spans


def make_row(
    state: dict, row: dict, span, rnd, origin: str, scope: str, caused_by, status: str
) -> dict:
    profile = PROFILES[state["profile"]]
    rid = f"R{len(state['rows']) + 1}"
    blocking = profile["blocking"](row) and scope == "in" and rnd != "sweep"
    return {
        "id": rid,
        "label": row.get("label"),
        "round_found": rnd,
        "grade": row["grade"],
        "rule": (row.get("rule") or None),
        "wrong_outcome": (row.get("wrong_outcome") or ""),
        "blocking": blocking,
        "anchor": row["anchor"],
        "at": list(span) if span else None,
        "at_snapshot": f"r{rnd}" if isinstance(rnd, int) else None,
        "origin": origin,
        "scope": scope,
        "caused_by": list(caused_by),
        "finding": row["finding"],
        "status": status if status else ("open" if blocking else "deferred"),
        "mappings": [],
        "claims": [],
        "history": [],
    }


def cmd_find(args) -> dict:
    read, got = input_reader(args.input)

    def apply(ledger: Ledger, state: dict):
        data, payload = got["data"], got["payload"]
        require_phase(state, "find")
        if committed_ops(state, "find", 1):
            refuse(
                "E-PHASE",
                "find already ran for review 1",
                EXIT_STATE,
                next_action(state),
            )
        rows = validate_rows(data, PROFILES[state["profile"]]["grades"])
        text = ledger.snapshot_path("r1").read_text(encoding="utf-8")
        spans = check_anchors(rows, text)
        for row, span in zip(rows, spans):
            new = make_row(state, row, span, 1, "find", "in", [], "")
            new["history"].append(
                {"seq": state["seq"], "via": "find", "to": new["status"]}
            )
            state["rows"].append(new)
        atomic_write(ledger.root / "inputs" / "r1-find.json", payload)
        return {}

    return mutate(args, "find", read, apply)


def check_claims(
    ledger: Ledger, state: dict, data
) -> tuple[list[dict], list[dict], list]:
    """Validate an answer input against the provisional hunks. Returns (claims, gaps, hunks)."""
    if (
        not isinstance(data, dict)
        or set(data) - {"claims", "gaps"}
        or not isinstance(data.get("claims", []), list)
    ):
        refuse(
            "E-SCHEMA",
            "answer input must be an object with a 'claims' list and an optional 'gaps' list",
            EXIT_INPUT,
            "fix the input shape",
        )
    gaps = data.get("gaps", [])
    if not isinstance(gaps, list) or any(
        not isinstance(g, dict) or not str(g.get("text", "")).strip() for g in gaps
    ):
        refuse(
            "E-SCHEMA",
            "each gap entry needs a non-empty 'text'",
            EXIT_INPUT,
            "fix the gaps list",
        )
    old, _live, hunks, _ops = provisional(ledger, state)
    old_lines = doc_lines(old)
    unit_list = units(old_lines)
    snap = last_snapshot(state)
    problems, claims = [], []
    for i, c in enumerate(data.get("claims", [])):
        if (
            not isinstance(c, dict)
            or c.get("action") not in ANSWER_ACTIONS
            or not isinstance(c.get("row"), str)
        ):
            problems.append(
                {
                    "index": i,
                    "code": "E-SCHEMA",
                    "detail": f"each claim needs 'row' and 'action' in {list(ANSWER_ACTIONS)}",
                }
            )
            continue
        row = row_by_id(state, c["row"])
        if (
            row is None
            or not row["blocking"]
            or row["scope"] != "in"
            or row["status"] not in {"open", "reopened"}
        ):
            problems.append(
                {
                    "index": i,
                    "code": "E-ILLEGAL",
                    "detail": f"{c['row']} is not a listed open blocking row (deferred and minor rows are "
                    "not answerable)",
                }
            )
            continue
        if c["action"] != "fixed":
            if not str(c.get("reason", "")).strip():
                problems.append(
                    {
                        "index": i,
                        "code": "E-SCHEMA",
                        "detail": f"{c['action']} needs a 'reason'",
                    }
                )
                continue
            claims.append(
                {
                    "row": row["id"],
                    "action": c["action"],
                    "keys": [],
                    "reason": c["reason"],
                }
            )
            continue
        nums = c.get("hunks")
        if (
            not isinstance(nums, list)
            or not nums
            or any(not isinstance(n, int) or not 1 <= n <= len(hunks) for n in nums)
        ):
            problems.append(
                {
                    "index": i,
                    "code": "E-SCHEMA",
                    "detail": f"'hunks' must list provisional hunk numbers 1..{len(hunks)} (see status)",
                }
            )
            continue
        span = current_span(row, snap)
        if span is None:
            problems.append(
                {
                    "index": i,
                    "code": "E-ILLEGAL",
                    "detail": f"{row['id']} has no mapped span",
                }
            )
            continue
        claimed = [hunks[n - 1] for n in nums]
        wide = widen(span, unit_list)
        if not any(overlaps(h["old"], span) for h in claimed):
            problems.append(
                {
                    "index": i,
                    "code": "E-FIXED-NO-EDIT",
                    "detail": f"no claimed hunk changes text inside {row['id']}'s span",
                }
            )
            continue
        too_wide = [
            h["n"]
            for h in claimed
            if not (wide[0] <= h["old"][0] and h["old"][1] <= wide[1])
        ]
        if too_wide:
            problems.append(
                {
                    "index": i,
                    "code": "E-CLAIM-WIDE",
                    "detail": f"hunks {too_wide} reach beyond {row['id']}'s paragraph",
                }
            )
            continue
        claims.append(
            {
                "row": row["id"],
                "action": "fixed",
                "keys": [h["key"] for h in claimed],
                "reason": c.get("reason", ""),
            }
        )
    if problems:
        order = ("E-SCHEMA", "E-ILLEGAL", "E-FIXED-NO-EDIT", "E-CLAIM-WIDE")
        code = next(o for o in order if any(p["code"] == o for p in problems))
        refuse(code, problems, EXIT_INPUT, "fix the listed claims; nothing was written")
    return claims, gaps, hunks


def live_binding(args) -> dict:
    """The live document's sha256 and the round: part of every request whose result
    depends on the document, so a call after a new edit is a new request, not a replay."""
    ledger = Ledger(ledger_root(args))
    state = ledger.load()
    doc = ledger.doc_path(state)
    return {
        "doc_sha256": sha256_bytes(doc.read_bytes()) if doc.is_file() else None,
        "round": state["round"],
    }


def cmd_answer(args) -> dict:
    read_only_input, got = input_reader(args.input)

    def read() -> bytes:
        return read_only_input() + b"\0" + canonical(live_binding(args))

    def apply(ledger: Ledger, state: dict):
        require_phase(state, "revise")
        claims, gaps, _hunks = check_claims(ledger, state, got["data"])
        for c in claims:
            if c["action"] == "disputed":
                row_by_id(state, c["row"])["history"].append(
                    {
                        "seq": state["seq"],
                        "via": "answer",
                        "dispute": c["reason"],
                        "round": state["round"],
                    }
                )
        atomic_write(
            ledger.root / "inputs" / f"c{state['round']}-answers-{state['seq']}.json",
            got["payload"],
        )
        doc_after = sha256_bytes(ledger.doc_path(state).read_bytes())
        return {
            "claims": claims,
            "gaps": gaps,
            "_op": {"claims": claims, "gaps": gaps, "doc_after": doc_after},
        }

    return mutate(args, "answer", read, apply)


def cmd_revert_unclaimed(args) -> dict:
    target = {}

    def read() -> bytes:
        return canonical({"hunk": args.hunk, **live_binding(args)})

    def apply(ledger: Ledger, state: dict):
        if state["phase"] != "revise":  # every other phase, terminal ones included
            refuse(
                "E-PHASE",
                f"phase is {state['phase']}; revert-unclaimed runs only in phase revise",
                EXIT_STATE,
                next_action(state),
            )
        old, live, hunks, _ops = provisional(ledger, state)
        claimed = {k for c in stored_answers(state) for k in c["keys"]}
        unclaimed = [h for h in hunks if not h["rewrap"] and h["key"] not in claimed]
        gone = []
        if args.hunk is not None:
            # --hunk is the key status printed, so the caller reverts the hunk it saw
            match = [h for h in hunks if h["key"] == args.hunk]
            if match and match[0] not in unclaimed:
                refuse(
                    "E-ILLEGAL",
                    f"hunk {args.hunk} is claimed or a rewrap",
                    EXIT_INPUT,
                    "",
                )
            if not match:
                gone = [
                    args.hunk
                ]  # the hunk the caller saw no longer exists: failed preimage
            unclaimed = match
        current = reread_doc(ledger.doc_path(state))
        if current != live:  # the document changed after the hunks were computed
            lines, reverted, failed = doc_lines(live), [], [h["n"] for h in unclaimed]
        else:
            lines, reverted, failed = revert_hunks(
                doc_lines(live), unclaimed, doc_lines(old)
            )
        failed = failed + gone
        restored = sum(h["new_bytes"] for h in unclaimed if h["n"] in reverted)
        if reverted:
            atomic_write(
                ledger.doc_path(state),
                join_lines(lines, live.endswith("\n")).encode("utf-8"),
            )
        x_items = [
            {"round": state["round"] + 1, "kind": "revert-preimage", "hunk": n}
            for n in failed
        ]
        target["n"] = len(reverted)
        after_text = join_lines(lines, live.endswith("\n")) if reverted else live
        return {
            "reverted": reverted,
            "failed": failed,
            "restored_bytes": restored,
            "_op": {"x_items": x_items, "doc_after": sha256_text(after_text)},
        }

    return mutate(args, "revert-unclaimed", read, apply)


def render_plan(
    state: dict,
    k: int,
    rows_info: dict,
    hunks: list,
    unclaimed: list,
    rewraps: list,
    gaps: list,
    dropped: list,
    hunks_large: bool,
    doc_rel: str,
    snap_sha: str,
) -> str:
    def rng(r):
        return (
            f"lines {r[0] + 1}-{r[1]}" if r[1] > r[0] else f"empty at line {r[0] + 1}"
        )

    def fence(text):
        return ["```text", text, "```"]

    lines = [
        f"# Ledger plan for review {k}",
        "",
        f"review: {k} of {state['cap_reviews']}",
        f"document: {doc_rel}; snapshot snapshots/r{k}.md sha256 {snap_sha}",
        "",
    ]
    if hunks_large:
        lines += [
            "HUNKS_LARGE: changed lines exceed 40% of the document; verify degrades toward a full review.",
            "",
        ]
    lines += ["## Rows to answer", ""]
    plan_rows = [
        r
        for r in state["rows"]
        if r["blocking"] and r["scope"] == "in" and r["status"] in LIVE_STATUSES
    ]
    if not plan_rows:
        lines += ["(none)", ""]
    for r in plan_rows:
        info = rows_info.get(r["id"], {})
        lines += [
            f"### {r['id']}: {r['grade']}, rule {r.get('rule') or '-'}, status {r['status']}",
            "",
            f"- finding: {flat(r['finding'])}",
            f"- wrong outcome: {flat(r['wrong_outcome']) or '-'}",
            f"- old anchor: {flat(r['anchor'])}",
        ]
        span = info.get("span")
        lines.append(
            f"- span in r{k}: {rng(span)}"
            if span is not None
            else f"- span in r{k}: unmappable ({info.get('method')})"
        )
        for n, via in info.get("hunks", []):
            h = hunks[n - 1]
            lines += (
                [
                    f"- hunk c{k - 1}#{n} (claimed by {via}), r{k - 1} {rng(h['old'])} -> r{k} {rng(h['new'])}",
                    "",
                    "old text:",
                ]
                + fence(h["old_text"])
                + ["new text:"]
                + fence(h["new_text"])
            )
        lines.append("")
    lines += ["## Unclaimed hunks", ""]
    if not unclaimed:
        lines += ["(none)", ""]
    for u in unclaimed:
        lines += [
            f"- {u['id']}: r{k - 1} {rng(u['old'])}, bytes {u['bytes']}, "
            f"{'reverted' if u['reverted'] else 'kept in the document'}",
            "",
            "old text:",
        ]
        lines += fence(u["old_text"]) + ["new text:"] + fence(u["new_text"]) + [""]
    if rewraps:
        lines += ["## Whitespace-only rewraps (not unclaimed, not claims)", ""]
        lines += [f"- c{k - 1}#{h['n']}: r{k} {rng(h['new'])}" for h in rewraps] + [""]
    if gaps:
        lines += (
            ["## Reviser gap entries", ""]
            + [f"- {flat(g['text'])}" for g in gaps]
            + [""]
        )
    if dropped:
        lines += ["## Reviser claims dropped (their hunk changed after answer)", ""]
        lines += [f"- {d['row']}: {d['key']}" for d in dropped] + [""]
    return "\n".join(lines)


def cmd_begin(args) -> dict:
    pending = {}

    def read() -> bytes:
        doc = Path(args.doc)
        if not doc.is_file():
            usage(f"document not found: {doc}")
        return canonical(
            {
                "doc": sha256_bytes(doc.read_bytes()),
                "revert": bool(args.revert_unclaimed),
            }
        )

    def apply(ledger: Ledger, state: dict):
        if (
            state["round"] >= state["cap_reviews"]
            or state["fix_cycles"] >= state["cap_reviews"] - 1
        ):
            refuse(
                "E-CAP",
                f"review {state['round']} was the last of {state['cap_reviews']}; no fourth review "
                "and no third fix cycle",
                EXIT_STATE,
                "escalate to the user with the open blocking findings",
            )
        require_phase(state, "revise")
        last = last_decision(state)
        last_report = ledger.root / last["report"]
        if not last_report.is_file() or not last_report.read_text(
            encoding="utf-8"
        ).endswith(last["tail"]):
            refuse(
                "E-REPORT-EDITED",
                f"{last_report} no longer ends with the tail close appended",
                EXIT_STATE,
                f"run close --report {last_report} to re-append the stored tail, then begin again",
            )
        doc = ledger.doc_path(state)
        if Path(args.doc).resolve() != doc:
            usage(f"--doc {args.doc} is not the ledger's document {doc}")
        k_old, k = state["round"], state["round"] + 1
        old_text = ledger.snapshot_path(f"r{k_old}").read_text(encoding="utf-8")
        live_text = doc.read_text(encoding="utf-8")
        old, live = doc_lines(old_text), doc_lines(live_text)
        d1, _ = diff_lines(old, live)
        unit_list = units(old)
        by_key = {h["key"]: h for h in d1}
        claimed_by: dict[int, list] = {}
        dropped = []
        answers = stored_answers(state)
        for c in answers:
            for key in c["keys"]:
                if key in by_key:
                    claimed_by.setdefault(by_key[key]["n"], []).append(
                        (c["row"], "answer")
                    )
                else:
                    dropped.append({"row": c["row"], "key": key})
        open_rows = [
            r
            for r in state["rows"]
            if r["blocking"]
            and r["scope"] == "in"
            and r["status"] in {"open", "reopened"}
        ]
        for h in d1:
            if h["rewrap"] or h["n"] in claimed_by:
                continue
            for r in open_rows:
                span = current_span(r, f"r{k_old}")
                if span is not None and overlaps(h["old"], widen(span, unit_list)):
                    claimed_by.setdefault(h["n"], []).append((r["id"], "auto"))
        unclaimed = [h for h in d1 if not h["rewrap"] and h["n"] not in claimed_by]
        x_items, reverted, failed = [], [], []
        final = live
        if args.revert_unclaimed and unclaimed:
            if (
                reread_doc(doc) != live_text
            ):  # preimage: the document changed while begin ran
                failed = [h["n"] for h in unclaimed]
            else:
                final, reverted, failed = revert_hunks(live, unclaimed, old)
            x_items += [
                {"round": k, "kind": "revert-preimage", "hunk": f"c{k_old}#{n}"}
                for n in failed
            ]
        final_text = (
            join_lines(final, live_text.endswith("\n")) if reverted else live_text
        )
        # committed hunks: old snapshot vs the text this review sees
        d2, opcodes = diff_lines(old, doc_lines(final_text))
        key_of_d1 = {h["n"]: h["key"] for h in d1}
        d2_by_key = {h["key"]: h for h in d2}

        def d2_for(n1):
            h = d2_by_key.get(key_of_d1[n1])
            if h is None:
                h = next(
                    (
                        x
                        for x in d2
                        if overlaps(
                            x["old"], next(y for y in d1 if y["n"] == n1)["old"]
                        )
                    ),
                    None,
                )
            return h

        hunk_claims: dict[int, list] = {}
        for n1, who in claimed_by.items():
            h = d2_for(n1)
            if h is not None:
                hunk_claims.setdefault(h["n"], []).extend(who)
        rows_info: dict[str, dict] = {}
        fixed_by: dict[str, list] = {}
        for n, who in hunk_claims.items():
            for rid, via in who:
                fixed_by.setdefault(rid, []).append((n, via))
        # relocate every row into the new snapshot
        for r in state["rows"]:
            span = current_span(r, f"r{k_old}")
            if span is None:
                continue
            new_span, method = map_span(span, opcodes, d2, final_text, r["anchor"])
            r["mappings"].append(
                {
                    "snapshot": f"r{k}",
                    "span": list(new_span) if new_span else None,
                    "method": method,
                }
            )
            rows_info[r["id"]] = {
                "span": new_span,
                "method": method,
                "hunks": fixed_by.get(r["id"], []),
            }
            needs_verify = (
                r["blocking"]
                and r["scope"] == "in"
                and r["status"] in LIVE_STATUSES | {"verified"}
            )
            if new_span is None and needs_verify:
                x_items.append(
                    {
                        "round": k,
                        "kind": "unmappable-anchor",
                        "row": r["id"],
                        "method": method,
                    }
                )
        for r in state["rows"]:
            if r["id"] in fixed_by and r["status"] in {"open", "reopened"}:
                r["claims"].append(
                    {
                        "cycle": k_old,
                        "via": sorted({v for _, v in fixed_by[r["id"]]}),
                        "hunks": [f"c{k_old}#{n}" for n, _ in fixed_by[r["id"]]],
                        "bytes": sum(d2[n - 1]["bytes"] for n, _ in fixed_by[r["id"]]),
                    }
                )
                r["history"].append(
                    {
                        "seq": state["seq"],
                        "via": "begin",
                        "from": r["status"],
                        "to": "fixed",
                        "claimed_by": sorted({v for _, v in fixed_by[r["id"]]}),
                    }
                )
                r["status"] = "fixed"
            elif r["status"] == "verified":
                span = current_span(r, f"r{k_old}")
                if span is not None and any(
                    overlaps(h["old"], span) for h in d2 if not h["rewrap"]
                ):
                    r["history"].append(
                        {
                            "seq": state["seq"],
                            "via": "begin",
                            "from": "verified",
                            "to": "fixed",
                            "reason": "a hunk of this round touches the verified span",
                        }
                    )
                    r["status"] = "fixed"
                    rows_info.setdefault(r["id"], {})["hunks"] = [
                        (h["n"], "touch")
                        for h in d2
                        if overlaps(h["old"], span) and not h["rewrap"]
                    ]
        changed = sum(
            max(h["old"][1] - h["old"][0], h["new"][1] - h["new"][0])
            for h in d2
            if not h["rewrap"]
        )
        hunks_large = changed > HUNKS_LARGE_SHARE * max(
            len(old), len(doc_lines(final_text)), 1
        )
        unclaimed_out = []
        for h in unclaimed:
            kept = d2_for(h["n"]) if h["n"] not in reverted else None
            unclaimed_out.append(
                {
                    "id": f"c{k_old}#{kept['n']}"
                    if kept
                    else f"c{k_old}-reverted-{h['n']}",
                    "old": h["old"],
                    "new": h["new"],
                    "bytes": h["bytes"],
                    "old_text": h["old_text"],
                    "new_text": h["new_text"],
                    "reverted": h["n"] in reverted,
                }
            )
        rewraps = [h for h in d2 if h["rewrap"]]
        gaps = [
            g
            for op in committed_ops(state, "answer", k_old)
            for g in op.get("gaps", [])
        ]
        for h in d2:
            h["claimed_by"] = [
                {"row": rid, "via": via} for rid, via in hunk_claims.get(h["n"], [])
            ]
            h["touches"] = [
                r["id"]
                for r in state["rows"]
                if current_span(r, f"r{k_old}") is not None
                and overlaps(h["old"], current_span(r, f"r{k_old}"))
            ]
        snap_bytes = final_text.encode("utf-8")
        state["snapshots"][f"r{k}"] = {
            "sha256": sha256_bytes(snap_bytes),
            "bytes": len(snap_bytes),
        }
        state["round"], state["fix_cycles"], state["phase"] = (
            k,
            state["fix_cycles"] + 1,
            "verify",
        )
        plan = render_plan(
            state,
            k,
            rows_info,
            d2,
            unclaimed_out,
            rewraps,
            gaps,
            dropped,
            hunks_large,
            state["doc"],
            sha256_bytes(snap_bytes),
        )
        diff_doc = {
            "from": f"r{k_old}",
            "to": f"r{k}",
            "hunks": d2,
            "unclaimed": unclaimed_out,
            "reverted": reverted,
            "failed_reverts": failed,
            "hunks_large": hunks_large,
        }
        if reverted:
            atomic_write(doc, snap_bytes)
        atomic_write(ledger.snapshot_path(f"r{k}"), snap_bytes)
        atomic_write(
            ledger.root / "diffs" / f"c{k_old}.json",
            json.dumps(diff_doc, indent=2).encode("utf-8"),
        )
        atomic_write(ledger.root / f"plan-r{k}.md", plan.encode("utf-8"))
        pending["k"] = k
        summary = {
            "review_header": review_header(state),
            "plan": str(ledger.root / f"plan-r{k}.md"),
            "hunks": len(d2),
            "auto_claimed": sorted(
                {n for n, w in hunk_claims.items() if any(v == "auto" for _, v in w)}
            ),
            "unclaimed": [
                {"id": u["id"], "bytes": u["bytes"], "reverted": u["reverted"]}
                for u in unclaimed_out
            ],
            "reverted_bytes": sum(u["bytes"] for u in unclaimed_out if u["reverted"]),
            "dropped_claims": dropped,
            "hunks_large": hunks_large,
        }
        return {
            **summary,
            "_op": {
                "x_items": x_items,
                "begin": {
                    "unclaimed": [
                        {k2: u[k2] for k2 in ("id", "bytes", "reverted")}
                        for u in unclaimed_out
                    ],
                    "reverted_bytes": summary["reverted_bytes"],
                },
            },
        }

    return mutate(args, "begin", read, apply)


VERIFY_RESULTS = ("resolved", "open", "regressed", "cannot-verify")
FROZEN_FIELDS = {
    "id",
    "label",
    "round_found",
    "grade",
    "rule",
    "wrong_outcome",
    "blocking",
    "anchor",
    "at",
    "origin",
    "scope",
    "caused_by",
    "finding",
}
ANSWER_KEYS = {"row", "result", "evidence", "touched_ok", "reason", "dispute_ruling"}
NEW_ROW_KEYS = ROW_INPUT_KEYS | {"side", "parent"}
VERIFY_ORDER = (
    "E-SCHEMA",
    "E-FROZEN",
    "E-ILLEGAL",
    "E-NOT-CHANGED",
    "E-ANCHOR",
    "E-ANCHOR-AMBIGUOUS",
    "E-INCOMPLETE",
)


def touched_value(v):
    return {"yes": True, "no": False, True: True, False: False}.get(v)


def unruled_dispute(row: dict, cycle: int) -> bool:
    """A reviser dispute raised in this fix cycle with no verifier ruling yet."""
    disputed = any(h.get("dispute") and h.get("round") == cycle for h in row["history"])
    ruled = any(
        h.get("dispute_ruling") and h.get("round") == cycle for h in row["history"]
    )
    return disputed and not ruled


def check_verify(ledger: Ledger, state: dict, data):
    """Validate a verify input. Returns (answers, new_rows, hunks, new_text, old_text)."""
    k = state["round"]
    if (
        not isinstance(data, dict)
        or set(data) - {"answers", "new_rows"}
        or not isinstance(data.get("answers", []), list)
        or not isinstance(data.get("new_rows", []), list)
    ):
        refuse(
            "E-SCHEMA",
            "verify input must be an object with an 'answers' list and an optional 'new_rows' list",
            EXIT_INPUT,
            "fix the input shape",
        )
    answers, new_rows = data.get("answers", []), data.get("new_rows", [])
    new_text = ledger.snapshot_path(f"r{k}").read_text(encoding="utf-8")
    old_text = ledger.snapshot_path(f"r{k - 1}").read_text(encoding="utf-8")
    hunks = json.loads(
        (ledger.root / "diffs" / f"c{k - 1}.json").read_text(encoding="utf-8")
    )["hunks"]
    plan_ids = [
        r["id"]
        for r in state["rows"]
        if r["blocking"] and r["scope"] == "in" and r["status"] in LIVE_STATUSES
    ]
    parents = {n.get("parent") for n in new_rows if isinstance(n, dict)}
    problems, seen = [], set()

    def bad(i, code, detail, where="answers"):
        problems.append({where: i, "code": code, "detail": detail})

    for i, a in enumerate(answers):
        if not isinstance(a, dict):
            bad(i, "E-SCHEMA", "answer is not an object")
            continue
        if set(a) & FROZEN_FIELDS:
            bad(
                i,
                "E-FROZEN",
                f"frozen fields cannot change: {sorted(set(a) & FROZEN_FIELDS)}",
            )
            continue
        if (
            set(a) - ANSWER_KEYS
            or a.get("result") not in VERIFY_RESULTS
            or touched_value(a.get("touched_ok")) is None
        ):
            bad(
                i,
                "E-SCHEMA",
                f"keys {sorted(ANSWER_KEYS)}; result in {list(VERIFY_RESULTS)}; touched_ok yes or no",
            )
            continue
        rid = a.get("row")
        row = row_by_id(state, rid) if isinstance(rid, str) else None
        if row is None:
            bad(i, "E-ILLEGAL", f"no row {rid!r}")
            continue
        if rid in seen:
            bad(i, "E-SCHEMA", f"{rid} is answered twice")
            continue
        seen.add(rid)
        if row["status"] == "deferred":
            bad(i, "E-ILLEGAL", f"{rid} is deferred and cannot change")
            continue
        if row["status"] == "verified":
            bad(
                i,
                "E-NOT-CHANGED",
                f"{rid} is verified and no hunk touched it: accepted text cannot be re-attacked",
            )
            continue
        if rid not in plan_ids:
            bad(i, "E-ILLEGAL", f"{rid} is not a row of plan-r{k}.md")
            continue
        result = a["result"]
        evidence = a.get("evidence")
        if result != "cannot-verify":
            if (
                not isinstance(evidence, str)
                or not evidence.strip()
                or not locate(new_text, evidence)
            ):
                bad(
                    i,
                    "E-ANCHOR",
                    f"{rid}: the evidence quote must occur in snapshots/r{k}.md",
                )
                continue
        if result == "resolved":
            if row["status"] != "fixed":
                bad(
                    i,
                    "E-NOT-CHANGED",
                    f"{rid} is {row['status']}: no hunk of this round changed it",
                )
                continue
            if current_span(row, f"r{k}") is None:
                bad(
                    i,
                    "E-ANCHOR",
                    f"{rid}'s anchor is unmappable in r{k}; answer cannot-verify",
                )
                continue
        if result == "regressed" and not any(
            h.get("to") == "verified" for h in row["history"]
        ):
            bad(i, "E-ILLEGAL", f"{rid} was never verified, so it cannot regress")
            continue
        if result == "open" and not (str(a.get("reason") or "").strip() or evidence):
            bad(i, "E-SCHEMA", f"{rid}: 'open' needs a reason or a quote")
            continue
        if touched_value(a["touched_ok"]) is False and rid not in parents:
            bad(
                i,
                "E-INCOMPLETE",
                f"{rid}: touched_ok no needs a child row in new_rows with parent {rid}",
            )
    for rid in plan_ids:
        if rid not in seen:
            bad(rid, "E-INCOMPLETE", f"plan row {rid} has no answer")
    spans = []
    for i, n in enumerate(new_rows):
        if not isinstance(n, dict):
            bad(i, "E-SCHEMA", "new row is not an object", "new_rows")
            continue
        if "id" in n:
            bad(i, "E-FROZEN", "a new row cannot carry an id", "new_rows")
            continue
        if (
            set(n) - NEW_ROW_KEYS
            or n.get("grade") not in PROFILES[state["profile"]]["grades"]
            or n.get("side", "new") not in ("new", "old")
            or not isinstance(n.get("anchor"), str)
            or not str(n.get("finding") or "").strip()
            or (n.get("parent") is not None and n.get("parent") not in plan_ids)
        ):
            bad(
                i,
                "E-SCHEMA",
                f"keys {sorted(NEW_ROW_KEYS)}; side new or old; parent a plan row",
                "new_rows",
            )
            continue
        hits = locate(
            new_text if n.get("side", "new") == "new" else old_text, n["anchor"]
        )
        if len(hits) != 1:
            bad(
                i,
                "E-ANCHOR" if not hits else "E-ANCHOR-AMBIGUOUS",
                f"anchor occurs {len(hits)} times on the {n.get('side', 'new')} side",
                "new_rows",
            )
            continue
        spans.append((n, hits[0]))
    if problems:
        code = next(o for o in VERIFY_ORDER if any(p["code"] == o for p in problems))
        refuse(
            code, problems, EXIT_INPUT, "fix the listed entries; nothing was written"
        )
    return answers, spans, hunks


def cmd_verify(args) -> dict:
    read, got = input_reader(args.input)

    def apply(ledger: Ledger, state: dict):
        require_phase(state, "verify")
        k = state["round"]
        if committed_ops(state, "verify", k):
            refuse(
                "E-PHASE",
                f"verify already ran for review {k}",
                EXIT_STATE,
                next_action(state),
            )
        answers, spans, hunks = check_verify(ledger, state, got["data"])
        at_cap = k >= state["cap_reviews"]
        x_items = []
        for a in answers:
            row = row_by_id(state, a["row"])
            result, before = a["result"], row["status"]
            entry = {
                "seq": state["seq"],
                "via": "verify",
                "round": k,
                "result": result,
                "touched_ok": touched_value(a["touched_ok"]),
                "evidence": a.get("evidence"),
            }
            if a.get("dispute_ruling"):
                entry["dispute_ruling"] = a["dispute_ruling"]
                entry["round"] = k - 1
            ever_verified = any(h.get("to") == "verified" for h in row["history"])
            if result == "resolved":
                if (
                    at_cap
                    and unruled_dispute(row, k - 1)
                    and not a.get("dispute_ruling")
                ):
                    after = "reopened" if ever_verified else "open"
                    entry["reason"] = "unruled dispute at the cap counts as open"
                else:
                    after = "verified"
            elif result == "open":
                after = (
                    ("reopened" if ever_verified else "open")
                    if before == "fixed"
                    else before
                )
                entry["reason"] = a.get("reason")
            elif result == "regressed":
                after = "reopened"
            else:  # cannot-verify
                after = before
                x_items.append({"round": k, "kind": "cannot-verify", "row": row["id"]})
            entry.update({"from": before, "to": after})
            row["history"].append(entry)
            row["status"] = after
        live_hunks = [h for h in hunks if not h["rewrap"]]
        new_ids = []
        for n, span in spans:
            side = n.get("side", "new")
            inside = [
                h
                for h in live_hunks
                if overlaps(h["new" if side == "new" else "old"], span)
            ]
            if inside:
                caused = sorted({c["row"] for h in inside for c in h["claimed_by"]})
                at = (
                    span
                    if side == "new"
                    else (inside[0]["new"][0], inside[0]["new"][0])
                )
                row = make_row(state, n, at, k, "changed", "in", caused, "")
            else:
                row = make_row(
                    state,
                    n,
                    span if side == "new" else None,
                    k,
                    "outside",
                    "outside",
                    [],
                    "deferred",
                )
            row["side"] = side
            row["parent"] = n.get("parent")
            row["history"].append(
                {"seq": state["seq"], "via": "verify", "to": row["status"], "round": k}
            )
            state["rows"].append(row)
            new_ids.append(row["id"])
        atomic_write(ledger.root / "inputs" / f"r{k}-verify.json", got["payload"])
        return {"new_rows": new_ids, "_op": {"x_items": x_items}}

    return mutate(args, "verify", read, apply)


def reread_doc(doc: Path) -> str:
    """Read the live document again right before a revert (preimage check)."""
    return doc.read_text(encoding="utf-8")


def decide(ledger: Ledger, state: dict) -> dict:
    k = state["round"]
    x_items = round_x_items(state, k)
    plan_answered = k == 1 or bool(committed_ops(state, "verify", k))
    i_ok = snapshots_intact(ledger, state) and plan_answered
    u = u_count(state)
    if not i_ok or x_items:
        decision = "ESCALATE"
    elif u == 0:
        decision = "PASS"
    elif k < state["cap_reviews"]:
        decision = "CONTINUE"
    else:
        decision = "ESCALATE"
    return {"loop_decision": decision, "U": u, "X": len(x_items), "I": i_ok}


def tail_text(state: dict, dec: dict) -> str:
    blocking_ids = [
        r["id"]
        for r in state["rows"]
        if r["blocking"] and r["scope"] == "in" and r["status"] in LIVE_STATUSES
    ]
    lines = [
        "",
        "<!-- review-ledger tail: written by review_ledger.py close; do not edit -->",
        "## Review ledger",
        "",
        review_header(state),
        "",
    ]
    lines += render_rows(state)
    lines.append("")
    if dec["loop_decision"] == "CONTINUE":
        lines += [
            "### Reviser brief",
            "",
            f"Blocking rows to fix: {', '.join(blocking_ids)}",
            "Revise only text a listed blocking row names; minor (deferred) rows are not answerable; "
            "add no rule, mechanism or section no blocking row calls for; each added paragraph or table "
            "cites its row id; report the byte size before and after.",
            "",
        ]
    lines.append(
        f"loop_decision: {dec['loop_decision']} (U={dec['U']}, X={dec['X']}, I={str(dec['I']).lower()})"
    )
    if dec["loop_decision"] == "CONTINUE":
        lines.append("verdict: FAIL")
    else:
        lines.append(f"loop: {dec['loop_decision']} (sweep pending)")
    return "\n".join(lines) + "\n"


def cmd_close(args) -> dict:
    report = Path(args.report)

    def read() -> bytes:
        if not report.is_file():
            refuse(
                "E-SCHEMA",
                f"report not found: {report}",
                EXIT_INPUT,
                "write the report first",
            )
        # the request is the report as the reviewer left it: a tail this report already
        # carries is not part of it, so a retry after a committed close is a replay
        ledger = Ledger(ledger_root(args))
        text = report.read_text(encoding="utf-8")
        for d in reversed(ledger.load()["decisions"]):
            same = (ledger.root / d.get("report", "")).resolve() == report.resolve()
            if same and text.endswith(d["tail"]):
                text = text[: -len(d["tail"])]
                break
        return canonical({"report": str(report), "content": sha256_text(text)})

    def apply(ledger: Ledger, state: dict):
        if state["phase"] == "revise":
            return reappend_tail(ledger, state)
        require_phase(state, "find", "verify")
        k = state["round"]
        if not committed_ops(
            state, "find" if state["phase"] == "find" else "verify", k
        ):
            refuse(
                "E-PHASE",
                f"close needs a committed {state['phase']} in review {k}",
                EXIT_STATE,
                next_action(state),
            )
        dec = decide(ledger, state)
        tail = tail_text(state, dec)
        state["decisions"].append(
            {
                "kind": "review",
                "round": k,
                **dec,
                "report": os.path.relpath(report.resolve(), ledger.root.resolve()),
                "tail": tail,
                "tail_sha256": sha256_bytes(tail.encode("utf-8")),
                "seq": state["seq"],
            }
        )
        state["phase"] = "revise" if dec["loop_decision"] == "CONTINUE" else "terminal"

        def after():
            text = report.read_text(encoding="utf-8")
            atomic_write(report, (text + tail).encode("utf-8"))

        return {
            "decision": dec,
            "last_line": tail.rstrip("\n").splitlines()[-1],
            "_after": after,
        }

    def reappend_tail(ledger: Ledger, state: dict):
        """Recovery for E-REPORT-EDITED: re-append the stored tail, no new decision."""
        last = last_decision(state)
        if report.resolve() != (
            ledger.root / last["report"]
        ).resolve() or report.read_text(encoding="utf-8").endswith(last["tail"]):
            refuse(
                "E-PHASE",
                "phase is revise and the last review report still ends with its tail",
                EXIT_STATE,
                next_action(state),
            )
        last.setdefault("reappended", []).append(state["seq"])

        def after():
            text = report.read_text(encoding="utf-8")
            atomic_write(report, (text + last["tail"]).encode("utf-8"))

        return {
            "reappended": True,
            "last_line": last["tail"].rstrip("\n").splitlines()[-1],
            "_after": after,
        }

    def on_replay(ledger: Ledger, state: dict, op: dict):
        """A replayed close re-appends a tail the report lost (a crash after the commit)."""
        mine = [
            d
            for d in state["decisions"]
            if d["kind"] == "review" and d["seq"] == op["seq"]
        ]
        if mine and report.is_file():
            text = report.read_text(encoding="utf-8")
            if not text.endswith(mine[0]["tail"]):
                atomic_write(report, (text + mine[0]["tail"]).encode("utf-8"))

    apply.on_replay = on_replay
    return mutate(args, "close", read, apply)


def cmd_status(args) -> dict:
    ledger = Ledger(ledger_root(args))
    state = ledger.load()
    extra = {}
    if state["phase"] == "revise":
        _old, _live, hunks, _ops = provisional(ledger, state)
        claimed = {k for c in stored_answers(state) for k in c["keys"]}
        extra["provisional_hunks"] = [
            {
                "n": h["n"],
                "old": h["old"],
                "new": h["new"],
                "bytes": h["bytes"],
                "rewrap": h["rewrap"],
                "key": h["key"],
                "claimed": h["key"] in claimed,
            }
            for h in hunks
        ]
    return result(
        state,
        review_header=review_header(state),
        rows=[
            {
                k: r[k]
                for k in (
                    "id",
                    "grade",
                    "rule",
                    "blocking",
                    "status",
                    "scope",
                    "origin",
                )
            }
            for r in state["rows"]
        ],
        snapshots_intact=snapshots_intact(ledger, state),
        x_items=round_x_items(state, state["round"]),
        metrics=metrics(ledger, state),
        **extra,
    )


# ---------------------------------------------------------------- sweep, defer, metrics

SWEEP_ROW_KEYS = ROW_INPUT_KEYS | {"challenges"}
CM = {"CRITICAL", "MAJOR"}


def sweep_copy(state: dict) -> dict | None:
    """The latest sweep --prepare record (path, sha256, post_terminal_edit)."""
    preps = [op["sweep_copy"] for op in state["ops"] if op.get("sweep_copy")]
    return preps[-1] if preps else None


def location_class(ledger: Ledger, state: dict, span) -> str:
    """Where a sweep row sits: in a claimed row's span, in a kept unclaimed hunk of the
    last fix cycle, or outside both (earlier cycles' hunks are not traced)."""
    k = state["round"]
    snap = f"r{k}"
    if span is None:
        return "outside_hunks"
    for r in state["rows"]:
        cur = current_span(r, snap)
        if r.get("claims") and cur is not None and overlaps(span, cur):
            return "in_claimed_span"
    diff_path = ledger.root / "diffs" / f"c{k - 1}.json"
    if k > 1 and diff_path.is_file():
        for h in json.loads(diff_path.read_text(encoding="utf-8"))["hunks"]:
            if not h["rewrap"] and not h["claimed_by"] and overlaps(h["new"], span):
                return "in_unclaimed_hunk"
    return "outside_hunks"


def tails_intact(ledger: Ledger, state: dict) -> bool:
    for d in state["decisions"]:
        if d["kind"] != "review":
            continue
        rep = ledger.root / d["report"]
        if not rep.is_file() or d["tail"] not in rep.read_text(encoding="utf-8"):
            return False
    return True


def cmd_sweep(args) -> dict:
    if args.prepare == bool(args.input):
        usage("sweep needs exactly one of --prepare or --input F --report R")
    if args.input and not args.report:
        usage("sweep --input needs --report R")
    if args.prepare:
        if args.dry_run:
            usage("--dry-run applies to sweep --input only")
        return sweep_prepare(args)
    read_only_input, got = input_reader(args.input)
    report = Path(args.report)

    def read() -> bytes:
        if not report.is_file():
            refuse(
                "E-SCHEMA",
                f"report not found: {report}",
                EXIT_INPUT,
                "write the report first",
            )
        return read_only_input() + b"\0" + canonical({"report": str(report.resolve())})

    def apply(ledger: Ledger, state: dict):
        if state["phase"] == "swept":
            refuse(
                "E-SWEEP-DONE",
                "the sweep already ran for this loop",
                EXIT_STATE,
                "read verdict",
            )
        if state["phase"] != "terminal":
            refuse(
                "E-PHASE",
                "the sweep runs only after a terminal close",
                EXIT_STATE,
                next_action(state),
            )
        copy = sweep_copy(state)
        if copy is None:
            refuse(
                "E-PHASE", "run sweep --prepare first", EXIT_STATE, "sweep --prepare"
            )
        data = got["data"]
        rows = (
            data.get("rows")
            if isinstance(data, dict) and set(data) <= {"rows"}
            else None
        )
        if not isinstance(rows, list):
            refuse(
                "E-SCHEMA",
                "sweep input must be an object with a 'rows' list",
                EXIT_INPUT,
                "fix the shape",
            )
        problems = []
        for i, row in enumerate(rows):
            if not isinstance(row, dict) or set(row) - SWEEP_ROW_KEYS:
                problems.append(
                    {
                        "index": i,
                        "code": "E-SCHEMA",
                        "detail": f"keys {sorted(SWEEP_ROW_KEYS)}",
                    }
                )
                continue
            ch = row.get("challenges")
            if (
                ch is not None
                and (row_by_id(state, ch) or {}).get("status") != "verified"
            ):
                problems.append(
                    {
                        "index": i,
                        "code": "E-SCHEMA",
                        "detail": f"challenges must name a verified row: {ch!r}",
                    }
                )
        if problems:
            refuse(
                "E-SCHEMA",
                problems,
                EXIT_INPUT,
                "fix the listed rows; nothing was written",
            )
        validate_rows(
            [{k: v for k, v in r.items() if k != "challenges"} for r in rows],
            PROFILES[state["profile"]]["grades"],
        )
        copy_text = (
            Path(copy["path"]).read_text(encoding="utf-8")
            if Path(copy["path"]).is_file()
            else None
        )
        if copy_text is None or sha256_text(copy_text) != copy["sha256"]:
            refuse(
                "E-PHASE",
                "the sweep copy is missing or changed; run sweep --prepare again",
                EXIT_STATE,
                "",
            )
        check_anchors(rows, copy_text)
        snap_text = ledger.snapshot_path(f"r{state['round']}").read_text(
            encoding="utf-8"
        )
        profile = PROFILES[state["profile"]]
        new_ids, s_count = [], 0
        for row in rows:
            hits = locate(
                snap_text, row["anchor"]
            )  # sweep anchors are quoted from the copy
            span = hits[0] if len(hits) == 1 else None
            new = make_row(state, row, span, "sweep", "sweep", "sweep", [], "deferred")
            new["at_snapshot"] = f"r{state['round']}"
            new["would_block"] = profile["blocking"](row)
            new["challenges"] = row.get("challenges")
            new["location"] = location_class(ledger, state, span)
            new["history"].append(
                {"seq": state["seq"], "via": "sweep", "to": "deferred"}
            )
            state["rows"].append(new)
            new_ids.append(new["id"])
            if new["would_block"] or new["challenges"]:
                s_count += 1
        intact = tails_intact(ledger, state)
        loop = loop_decision(state)
        outcome = (
            "ESCALATE" if loop == "ESCALATE" or s_count > 0 or not intact else "PASS"
        )
        sweep_rows = [r for r in state["rows"] if r["id"] in new_ids]
        lines = [
            "",
            "<!-- review-ledger tail: written by review_ledger.py sweep; do not edit -->",
            "## Review ledger sweep",
            "",
            "sweep",
            "",
            "| id | grade | rule | would block | challenges | location | anchor |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in sweep_rows:
            lines.append(
                f"| {r['id']} | {r['grade']} | {r.get('rule') or ''} | {'yes' if r['would_block'] else 'no'} "
                f"| {r['challenges'] or ''} | {r['location']} | {flat(r['anchor']).replace('|', chr(92) + '|')} |"
            )
        lines += [
            "",
            f"delivery_outcome: {outcome} (loop={loop}, S={s_count}, tails_intact={str(intact).lower()})",
            f"verdict: {'PASS' if outcome == 'PASS' else 'FAIL'}",
        ]
        tail = "\n".join(lines) + "\n"
        state["decisions"].append(
            {
                "kind": "sweep",
                "delivery_outcome": outcome,
                "S": s_count,
                "tails_intact": intact,
                "report": os.path.relpath(report.resolve(), ledger.root.resolve()),
                "tail": tail,
                "tail_sha256": sha256_text(tail),
                "seq": state["seq"],
                "copy_sha256": copy["sha256"],
            }
        )
        state["phase"] = "swept"
        atomic_write(ledger.root / "inputs" / "sweep.json", got["payload"])

        def after():
            text = report.read_text(encoding="utf-8")
            atomic_write(report, (text + tail).encode("utf-8"))

        return {
            "new_rows": new_ids,
            "S": s_count,
            "last_line": tail.rstrip("\n").splitlines()[-1],
            "_after": after,
        }

    return mutate(args, "sweep", read, apply)


def sweep_prepare(args) -> dict:
    def read() -> bytes:
        return canonical({"prepare": True, **live_binding(args)})

    def apply(ledger: Ledger, state: dict):
        if state["phase"] == "swept":
            refuse(
                "E-SWEEP-DONE",
                "the sweep already ran for this loop",
                EXIT_STATE,
                "read verdict",
            )
        if state["phase"] != "terminal":
            refuse(
                "E-PHASE",
                "the sweep runs only after a terminal close",
                EXIT_STATE,
                next_action(state),
            )
        doc = ledger.doc_path(state)
        data = doc.read_bytes()
        folder = Path(tempfile.mkdtemp(prefix="review-ledger-sweep-"))
        copy = folder / doc.name
        copy.write_bytes(data)
        last_sha = state["snapshots"][f"r{state['round']}"]["sha256"]
        record = {
            "path": str(copy),
            "sha256": sha256_bytes(data),
            "post_terminal_edit": sha256_bytes(data) != last_sha,
        }
        return {
            "copy": str(copy),
            "post_terminal_edit": record["post_terminal_edit"],
            "_op": {"sweep_copy": record},
        }

    return mutate(args, "sweep-prepare", read, apply)


def cmd_defer(args) -> dict:
    def read() -> bytes:
        return canonical({"id": args.id, "quote": args.quote})

    def apply(ledger: Ledger, state: dict):
        if state["phase"] not in ("terminal", "swept"):
            refuse(
                "E-PHASE",
                "defer records a user's words after the loop ended",
                EXIT_STATE,
                next_action(state),
            )
        row = row_by_id(state, args.id)
        if row is None:
            refuse("E-ILLEGAL", f"no row {args.id!r}", EXIT_INPUT, "")
        if not args.quote.strip():
            refuse("E-SCHEMA", "--quote must hold the user's words", EXIT_INPUT, "")
        row["history"].append(
            {
                "seq": state["seq"],
                "via": "defer",
                "quote": args.quote,
                "status": row["status"],
            }
        )
        return {"row": row["id"], "status": row["status"]}

    return mutate(args, "defer", read, apply)


def metrics(ledger: Ledger, state: dict) -> dict:
    rows = state["rows"]
    loop_rows = [
        r for r in rows if isinstance(r["round_found"], int) and r["scope"] == "in"
    ]
    u3 = sum(1 for r in loop_rows if r["grade"] in CM and r["status"] != "verified")
    sweep_rows = [r for r in rows if r["round_found"] == "sweep"]
    w = sum(1 for r in sweep_rows if r["grade"] in CM or r.get("challenges"))
    o = sum(1 for r in rows if r["scope"] == "outside" and r["grade"] in CM)
    floor = sum(
        1
        for r in rows
        if r["round_found"] == 1
        and r["grade"] in CM
        and r["history"]
        and r["history"][0].get("to") == "deferred"
    )
    per_cycle, minor_touched = [], {"answered": 0, "auto-claimed": 0}
    deferred_ids = {r["id"] for r in rows if r["status"] == "deferred"}
    for op in state["ops"]:
        if op.get("cmd") != "begin" or "begin" not in op:
            continue
        cycle = op["round"]
        unclaimed = op["begin"]["unclaimed"]
        per_cycle.append(
            {
                "cycle": cycle,
                "unclaimed_bytes": sum(
                    u["bytes"] for u in unclaimed if not u["reverted"]
                ),
                "reverted_bytes": op["begin"]["reverted_bytes"],
            }
        )
        diff_path = ledger.root / "diffs" / f"c{cycle}.json"
        if diff_path.is_file():
            for h in json.loads(diff_path.read_text(encoding="utf-8"))["hunks"]:
                vias = {c["via"] for c in h["claimed_by"]}
                touched = [rid for rid in h.get("touches", []) if rid in deferred_ids]
                if touched and "answer" in vias:
                    minor_touched["answered"] += len(touched)
                elif touched and "auto" in vias:
                    minor_touched["auto-claimed"] += len(touched)
    claim_bytes = {
        r["id"]: [{"cycle": c["cycle"], "bytes": c["bytes"]} for c in r["claims"]]
        for r in rows
        if r.get("claims")
    }
    doc = ledger.doc_path(state)
    last = state["snapshots"][f"r{state['round']}"]["sha256"]
    live = sha256_bytes(doc.read_bytes()) if doc.is_file() else None
    terminal = state["phase"] in ("terminal", "swept")
    return {
        "U3": u3,
        "W": w,
        "O": o,
        "deferred_floor": floor,
        "headline_raw": u3 + w + o,
        "per_cycle_bytes": per_cycle,
        "claim_bytes": claim_bytes,
        "minor_touched": minor_touched,
        "scope_outside": sum(1 for r in rows if r["scope"] == "outside"),
        "X": sum(len(op.get("x_items", [])) for op in state["ops"]),
        "post_terminal_edit": {
            "doc_sha256": live,
            "last_snapshot_sha256": last,
            "changed": terminal and live != last,
        },
    }


def verdict_of(state: dict) -> str:
    if state["phase"] in ("find", "revise", "verify"):
        return "CONTINUE"
    if state["phase"] == "terminal":
        return "PENDING"
    return delivery_outcome(state) or "PENDING"


def cmd_verdict(args) -> tuple[dict, int]:
    state = Ledger(ledger_root(args)).load()
    v = verdict_of(state)
    return {
        "verdict": v,
        "loop_decision": loop_decision(state),
        "delivery_outcome": delivery_outcome(state),
        "U": u_count(state),
        "review": state["round"],
        "phase": state["phase"],
    }, VERDICT_EXIT[v]


# ---------------------------------------------------------------- CLI


class Parser(argparse.ArgumentParser):
    def error(self, message):  # usage errors exit 1 with the JSON error shape
        emit({"error": "E-USAGE", "detail": message, "next_action": "see --help"})
        sys.exit(EXIT_USAGE)


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")


def build_parser() -> argparse.ArgumentParser:
    p = Parser(
        prog="review_ledger.py",
        description="Script-kept finding ledger for document review loops.",
    )
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=Parser)

    def where(sp, doc_required=False):
        sp.add_argument(
            "--ledger",
            help="ledger folder (default <doc dir>/<doc stem>.review-ledger/)",
        )
        sp.add_argument("--doc", required=doc_required, help="the reviewed document")

    def mutation(sp, dry=False):
        sp.add_argument(
            "--op", help="caller-chosen operation id (required unless --dry-run)"
        )
        sp.add_argument(
            "--expect-seq",
            type=int,
            help="the ledger seq the caller last read (required unless --dry-run)",
        )
        if dry:
            sp.add_argument(
                "--dry-run",
                action="store_true",
                help="validate and print the would-be result; take no lock and write no file",
            )

    sp = sub.add_parser("init", help="create the ledger and snapshot r1 (review 1)")
    where(sp, doc_required=True)
    sp.add_argument("--profile", required=True)
    sp.add_argument(
        "--archive-existing",
        action="store_true",
        help="rename an existing ledger folder first",
    )
    sp.add_argument("--op", help="optional operation id")

    sp = sub.add_parser("find", help="ingest review-1 rows (review 1)")
    where(sp)
    mutation(sp, dry=True)
    sp.add_argument(
        "--input",
        required=True,
        help=".json rows, or a .md report with one ledger-input block",
    )

    sp = sub.add_parser(
        "answer",
        help="reviser claims: provisional hunks per blocking row, gap entries (optional)",
    )
    where(sp)
    mutation(sp, dry=True)
    sp.add_argument(
        "--input",
        required=True,
        help=".json claims, or a .md file with one ledger-input block",
    )

    sp = sub.add_parser(
        "begin",
        help="start review 2 or 3: snapshot, diff, auto-claim, optional revert, plan file",
    )
    where(sp, doc_required=True)
    mutation(sp)
    sp.add_argument(
        "--revert-unclaimed",
        action="store_true",
        help="consent for this invocation only: restore hunks no blocking row claims",
    )

    sp = sub.add_parser(
        "revert-unclaimed",
        help="restore unclaimed provisional hunks in the document (phase revise)",
    )
    where(sp)
    mutation(sp)
    sp.add_argument(
        "--hunk",
        help="the key of one provisional hunk, as status lists it (default: every unclaimed hunk)",
    )

    sp = sub.add_parser(
        "verify",
        help="reviews 2 and 3: answer every plan row; new rows in or outside this round's hunks",
    )
    where(sp)
    mutation(sp, dry=True)
    sp.add_argument(
        "--input",
        required=True,
        help=".json answers, or a .md report with one ledger-input block",
    )

    sp = sub.add_parser(
        "close",
        help="compute the loop decision and append the report tail "
        "(in phase revise: re-append a lost tail)",
    )
    where(sp)
    mutation(sp)
    sp.add_argument("--report", required=True)

    sp = sub.add_parser(
        "sweep",
        help="once, after a terminal close: --prepare copies the document for a fresh "
        "context; --input F --report R ingests its rows and sets the delivery outcome",
    )
    where(sp)
    mutation(sp, dry=True)
    sp.add_argument(
        "--prepare",
        action="store_true",
        help="copy the live document to a new temporary folder",
    )
    sp.add_argument(
        "--input",
        help=".json {'rows': [...]}, or a .md report with one ledger-input block",
    )
    sp.add_argument(
        "--report", help="the sweep report; the sweep tail is appended to it"
    )

    sp = sub.add_parser(
        "defer", help="record a user's words on a row (no status change)"
    )
    where(sp)
    mutation(sp)
    sp.add_argument("--id", required=True, help="row id")
    sp.add_argument("--quote", required=True, help="the user's words")

    sp = sub.add_parser(
        "status", help="read-only counts (and provisional hunks in phase revise)"
    )
    where(sp)

    sp = sub.add_parser(
        "verdict",
        help="read-only verdict; exit 0 PASS, 10 CONTINUE, 11 ESCALATE, 12 PENDING",
    )
    where(sp)
    return p


COMMANDS = {
    "init": cmd_init,
    "find": cmd_find,
    "answer": cmd_answer,
    "begin": cmd_begin,
    "revert-unclaimed": cmd_revert_unclaimed,
    "verify": cmd_verify,
    "close": cmd_close,
    "sweep": cmd_sweep,
    "defer": cmd_defer,
    "status": cmd_status,
}


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "verdict":
            out, code = cmd_verdict(args)
            emit(out)
            return code
        emit(COMMANDS[args.cmd](args))
        return EXIT_OK
    except Refusal as r:
        emit({"error": r.code, "detail": r.detail, "next_action": r.next_action})
        return r.exit_code


if __name__ == "__main__":
    sys.exit(main())
