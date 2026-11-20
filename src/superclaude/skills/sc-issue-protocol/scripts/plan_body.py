#!/usr/bin/env python3
"""Build the new issue body of `/sc:issue --plan` from drafted section texts.

Standard library only. The model drafts the section texts and nothing else;
this script reads the current body and the drafted texts from files and writes
the new body to a file, so the one body edit of plan mode is deterministic
(the rules are the plan check, Wave 5 and "Re-plan" of `refs/plan.md`). It
never calls `gh`, never uses the network and touches only the files named in
its arguments.

Usage:
    plan_body.py check  (--body-json F | --body-file F) [--remaining R]
    plan_body.py check  --remaining R
    plan_body.py splice (--body-json F | --body-file F) --sections-file S
                        --out O [--remaining R --before-out B]
    plan_body.py verify (--base-json F | --base-file F)
                        (--readback-json F | --readback-file F) [--remaining R]

A ``--*-json`` file is the output of ``gh issue view ... --json body`` (any
other fields are ignored); a ``--*-file`` file is the body as plain text. Both
are read as bytes and decoded as UTF-8, so CRLF line endings survive.

``check`` applies the plan check to a body (a heading that occurs twice is a
refusal) and prints the section states, the sections that need text
(``need``), ``already_planned`` and ``body_sha`` (the first 16 hex digits of
the SHA-256 of the body, for comparing two reads). With ``--remaining`` it
first checks the remaining file, then requires the three sections to pass,
and also prints ``round``, ``sha`` (8 hex digits of the SHA-256 of the file),
``criteria`` and ``marker``; with ``--remaining`` alone it checks the file.

``splice`` writes the new body to ``--out`` (never to the body argument): an
absent heading is appended at the end, an empty or "Not known yet" section is
filled in place, the plan marker is added once under the first heading filled
or appended, every other byte is kept and added lines take the CRLF of a CRLF
body. Blocks of sections that pass are dropped. With ``--remaining`` it
replaces ``## Fix approach`` and ``## Test plan`` in place, keeps the hidden
markers of the skill inside them, drops an old re-plan marker, adds the new
marker under ``## Fix approach`` and saves the old text of both sections to
``--before-out``. It writes nothing when the body is already planned.

``verify`` runs the four read-back checks of Wave 5: every byte outside the
sections filled or appended is unchanged, each heading occurs once, the plan
check passes and the marker occurs once (CRLF and LF count as the same).

Output: one JSON line on stdout. Exit codes (the reason goes to stderr as one
line):
    0  success (also ``already_planned``)
    1  a refused input; the line starts with the STOP code:
       E-PLAN-REPEATED-HEADING, E-REMAINING-FILE, E-REMAINING-NEEDS-PLAN,
       E-WORKER-NO-OUTPUT, E-PLAN-WRITE-FAILED
    2  a call that cannot run (bad arguments, an unreadable body file);
       nothing was written
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

PLAN_TOKENS = ("priority", "fix_approach", "test_plan")
REPLAN_TOKENS = ("fix_approach", "test_plan")
PLAN_HEADING = {
    "priority": "## Priority",
    "fix_approach": "## Fix approach",
    "test_plan": "## Test plan",
}
PLAN_MARKER = "<!-- sc:issue:plan -->"
CREATE_MARKER_PREFIX = "<!-- sc:issue:create"
MAX_CRITERIA = 20
MAX_LINE = 300

_HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
_BLOCK_OPEN = re.compile(r"^<!-- plan-section: (priority|fix_approach|test_plan) -->$")
_KEPT_MARKER = re.compile(r"^<!-- sc:issue:(?!replan).*-->\s*$")


class PlanStop(Exception):
    """A refused input: `code` is the STOP code of refs/plan.md."""

    def __init__(self, code: str, reason: str = "") -> None:
        super().__init__(f"{code}: {reason}" if reason else code)
        self.code = code
        self.reason = reason


class UsageError(Exception):
    """A call that cannot run (exit 2)."""


# --- the plan check ---------------------------------------------------------------------


def _bare(line: str) -> str:
    return line.rstrip("\r\n")


def plan_section_span(body: str, token: str):
    """Return (heading count, first line, line after the last) of one section.

    A section runs from the line after its heading to the next line that starts
    with `## ` or with the hidden create marker, or to the end of the body.
    """
    lines = body.splitlines(keepends=True)
    heading = [i for i, ln in enumerate(lines) if _bare(ln) == PLAN_HEADING[token]]
    if len(heading) != 1:
        return len(heading), None, None
    start = heading[0] + 1
    end = next(
        (
            i
            for i in range(start, len(lines))
            if _bare(lines[i]).startswith(("## ", CREATE_MARKER_PREFIX))
        ),
        len(lines),
    )
    return 1, start, end


def plan_section_state(body: str, token: str) -> str:
    count, start, end = plan_section_span(body, token)
    if count == 0:
        return "absent"
    if count > 1:
        return "repeated"
    lines = body.splitlines(keepends=True)
    text = _HTML_COMMENT.sub("", "".join(lines[start:end])).strip()
    if not text:
        return "empty"
    if text.lower() == "not known yet":
        return "placeholder"
    return "ok"


def plan_check(body: str) -> dict[str, str]:
    return {token: plan_section_state(body, token) for token in PLAN_TOKENS}


def section_text(body: str, token: str) -> str:
    _, start, end = plan_section_span(body, token)
    return "".join(body.splitlines(keepends=True)[start:end])


def _refuse_repeated(states: dict[str, str]) -> None:
    repeated = [PLAN_HEADING[t] for t in PLAN_TOKENS if states[t] == "repeated"]
    if repeated:
        raise PlanStop("E-PLAN-REPEATED-HEADING", ", ".join(repeated) + " occurs twice")


def body_sha(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


# --- the drafted blocks -----------------------------------------------------------------


def parse_plan_sections(text: str) -> dict[str, str]:
    """Read `plan-sections.md`: one block per `<!-- plan-section: <token> -->`."""
    blocks: dict[str, list[str]] = {}
    token = None
    for line in text.splitlines():
        opened = _BLOCK_OPEN.match(line.strip())
        if opened:
            token = opened.group(1)
            blocks[token] = []
        elif token:
            blocks[token].append(line)
    return {t: "\n".join(lines).strip() for t, lines in blocks.items()}


def plan_block_problems(
    states: dict[str, str], blocks: dict[str, str], needed
) -> list[str]:
    """What is wrong with the blocks of the sections that need text."""
    problems = []
    for token in needed:
        text = blocks.get(token, "")
        if not text:
            problems.append(f"{token}: no block")
            continue
        if "not known yet" in text.lower():
            problems.append(f"{token}: says Not known yet")
        first, *rest = text.splitlines()
        if states[token] == "absent":
            if first != PLAN_HEADING[token]:
                problems.append(f"{token}: an absent section needs its heading line")
        else:
            rest = [first, *rest]
        if any(ln.startswith(("## ", "<!-- sc:issue:")) for ln in rest):
            problems.append(f"{token}: a drafted line starts a heading or a marker")
    return problems


# --- building the body ------------------------------------------------------------------


def _nl(body: str) -> str:
    return "\r\n" if "\r\n" in body else "\n"


def _text_lines(text: str, nl: str) -> list[str]:
    return [_bare(ln) + nl for ln in text.strip().splitlines()]


def build_plan_body(body: str, blocks: dict[str, str]) -> str | None:
    """Plain plan mode: append absent headings, fill empty sections in place."""
    states = plan_check(body)
    _refuse_repeated(states)
    needed = [t for t in PLAN_TOKENS if states[t] != "ok"]
    if not needed:
        return None
    problems = plan_block_problems(states, blocks, needed)
    if problems:
        raise PlanStop("E-WORKER-NO-OUTPUT", "; ".join(problems))
    nl = _nl(body)
    lines = body.splitlines(keepends=True)
    marker = [] if PLAN_MARKER in body else [PLAN_MARKER + nl]
    first = needed[0]
    in_place = [t for t in needed if states[t] != "absent"]
    for token in sorted(
        in_place, key=lambda t: plan_section_span(body, t)[1], reverse=True
    ):
        _, start, end = plan_section_span(body, token)
        region = [
            nl,
            *(marker if token == first else []),
            *_text_lines(blocks[token], nl),
        ]
        if end < len(lines):
            region.append(nl)
        lines[start:end] = region
    out = "".join(lines)
    for token in (t for t in needed if states[t] == "absent"):
        block = _text_lines(blocks[token], nl)  # its first line is the heading
        if token == first:
            block[1:1] = marker
        if out and not out.endswith("\n"):
            out += nl
        out += nl + "".join(block)
    return out


def replan_marker(round_number: int, sha: str) -> str:
    return f"<!-- sc:issue:replan round={round_number} sha={sha} -->"


def build_replan_body(body, blocks, round_number, sha):
    """`--remaining`: replace Fix approach and Test plan in place."""
    states = plan_check(body)
    _refuse_repeated(states)
    if any(state != "ok" for state in states.values()):
        raise PlanStop(
            "E-REMAINING-NEEDS-PLAN", "the three sections do not pass the plan check"
        )
    if replan_marker(round_number, sha) in body:
        return None
    problems = plan_block_problems(
        {t: "empty" for t in REPLAN_TOKENS}, blocks, REPLAN_TOKENS
    )
    if problems:
        raise PlanStop("E-WORKER-NO-OUTPUT", "; ".join(problems))
    nl = _nl(body)
    lines = body.splitlines(keepends=True)
    for token in sorted(
        REPLAN_TOKENS, key=lambda t: plan_section_span(body, t)[1], reverse=True
    ):
        _, start, end = plan_section_span(body, token)
        kept = [
            _bare(ln) + nl for ln in lines[start:end] if _KEPT_MARKER.match(_bare(ln))
        ]
        new_marker = (
            [replan_marker(round_number, sha) + nl] if token == "fix_approach" else []
        )
        region = [nl, *kept, *new_marker, *_text_lines(blocks[token], nl)]
        if end < len(lines):
            region.append(nl)
        lines[start:end] = region
    return "".join(lines)


# --- the read-back checks ---------------------------------------------------------------


def _outside(body: str, tokens):
    """The body without the text of the given sections (LF only); None when a
    heading of one of them does not occur exactly once."""
    spans = [plan_section_span(body, t) for t in tokens]
    if any(count != 1 for count, _, _ in spans):
        return None
    lines = body.splitlines(keepends=True)
    for _, start, end in sorted(spans, key=lambda s: s[1], reverse=True):
        del lines[start:end]
    return "".join(lines).replace("\r\n", "\n")


def outside_unchanged(old: str, new: str, filled, appended=()) -> bool:
    """Every byte outside the sections filled (or appended) is as it was."""
    before, after = _outside(old, filled), _outside(new, filled)
    if before is None or after is None:
        return False
    return after.startswith(before) if appended else after == before


def verify_readback(base: str, back: str, replan=None) -> list[str]:
    """The failed checks of Wave 5 step 5 (an empty list means all four pass)."""
    states = plan_check(base)
    _refuse_repeated(states)
    if replan is None:
        filled = [t for t in PLAN_TOKENS if states[t] in ("empty", "placeholder")]
        appended = [t for t in PLAN_TOKENS if states[t] == "absent"]
        marker_ok = back.count(PLAN_MARKER) == 1
    else:
        filled, appended = list(REPLAN_TOKENS), []
        marker_ok = back.count(replan_marker(replan[0], replan[2])) == 1
    failed = []
    if not outside_unchanged(base, back, filled, appended):
        failed.append("bytes outside the changed sections are not unchanged")
    if any(plan_section_span(back, t)[0] != 1 for t in PLAN_TOKENS):
        failed.append("a plan heading does not occur exactly once")
    if not all(state == "ok" for state in plan_check(back).values()):
        failed.append("the plan check does not pass")
    if not marker_ok:
        failed.append("the marker does not occur exactly once")
    return failed


# --- the remaining file -----------------------------------------------------------------


def parse_remaining_file(path):
    """The rules of the file of `--remaining`; any breach is E-REMAINING-FILE.

    Returns (round, criteria, sha) where sha is 8 hex digits of its SHA-256."""
    try:
        raw = Path(path).read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as err:
        raise PlanStop("E-REMAINING-FILE", f"cannot read {path}") from err
    lines = text.splitlines()
    head = re.fullmatch(r"round: ([0-9]+)", lines[0]) if lines else None
    if not head or int(head.group(1)) < 2:
        raise PlanStop(
            "E-REMAINING-FILE", "the first line must be `round: <n>`, n >= 2"
        )
    items = [ln for ln in lines[1:] if ln.strip()]
    if not 1 <= len(items) <= MAX_CRITERIA:
        raise PlanStop(
            "E-REMAINING-FILE", f"1 to {MAX_CRITERIA} criterion lines needed"
        )
    if any(not ln.startswith("- ") or len(ln) > MAX_LINE for ln in items):
        raise PlanStop(
            "E-REMAINING-FILE", f"each line is `- <criterion>` of at most {MAX_LINE}"
        )
    return (
        int(head.group(1)),
        [ln[2:] for ln in items],
        hashlib.sha256(raw).hexdigest()[:8],
    )


# --- commands ---------------------------------------------------------------------------


def _read_bytes(path) -> str:
    try:
        return Path(path).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as err:
        raise UsageError(f"cannot read {path}: {err}") from err


def read_body(json_path, file_path) -> str:
    if file_path is not None:
        return _read_bytes(file_path)
    try:
        body = json.loads(_read_bytes(json_path))["body"]
    except (ValueError, KeyError, TypeError) as err:
        raise UsageError(
            f"{json_path} is not `gh issue view --json body` output"
        ) from err
    if body is None:
        return ""
    if not isinstance(body, str):
        raise UsageError(f"{json_path}: `body` is not text")
    return body


def _write_bytes(path, text: str) -> None:
    try:
        Path(path).write_bytes(text.encode("utf-8"))
    except OSError as err:
        raise UsageError(f"cannot write {path}: {err}") from err


def cmd_check(args) -> dict:
    replan = parse_remaining_file(args.remaining) if args.remaining else None
    result: dict = {"cmd": "check"}
    if replan is not None:
        round_number, criteria, sha = replan
        result |= {
            "round": round_number,
            "sha": sha,
            "criteria": len(criteria),
            "marker": replan_marker(round_number, sha),
        }
    if args.body_json is None and args.body_file is None:
        if replan is None:
            raise UsageError(
                "check needs a body (--body-json or --body-file) or --remaining"
            )
        return result
    body = read_body(args.body_json, args.body_file)
    states = plan_check(body)
    _refuse_repeated(states)
    if replan is None:
        need = [t for t in PLAN_TOKENS if states[t] != "ok"]
        planned = not need
    else:
        if any(state != "ok" for state in states.values()):
            raise PlanStop(
                "E-REMAINING-NEEDS-PLAN",
                "the three sections do not pass the plan check; run plain --plan first",
            )
        need = list(REPLAN_TOKENS)
        planned = replan_marker(replan[0], replan[2]) in body
    return result | {
        "states": states,
        "need": need,
        "already_planned": planned,
        "body_sha": body_sha(body),
    }


def cmd_splice(args) -> dict:
    replan = parse_remaining_file(args.remaining) if args.remaining else None
    if replan is not None and not args.before_out:
        raise UsageError("--remaining needs --before-out")
    if replan is None and args.before_out:
        raise UsageError("--before-out belongs to --remaining")
    body = read_body(args.body_json, args.body_file)
    try:
        blocks = parse_plan_sections(_read_bytes(args.sections_file))
    except UsageError as err:
        raise PlanStop("E-WORKER-NO-OUTPUT", f"no sections file: {err}") from err
    if replan is None:
        new_body = build_plan_body(body, blocks)
        tokens = [t for t in PLAN_TOKENS if plan_section_state(body, t) != "ok"]
    else:
        new_body = build_replan_body(body, blocks, replan[0], replan[2])
        tokens = list(REPLAN_TOKENS)
    result = {
        "cmd": "splice",
        "mode": "plan" if replan is None else "replan",
        "result": "already_planned" if new_body is None else "written",
        "base_sha": body_sha(body),
        "out": str(args.out),
        "sections_added": [],
        "sections_replaced": [],
        "dropped": [],
    }
    if new_body is None:
        return result
    result["dropped"] = [t for t in blocks if t not in tokens]
    result["sections_added" if replan is None else "sections_replaced"] = tokens
    if replan is not None:
        nl = _nl(body)
        old = "".join(PLAN_HEADING[t] + nl + section_text(body, t) for t in tokens)
        _write_bytes(args.before_out, old)
        result["before_out"] = str(args.before_out)
    _write_bytes(args.out, new_body)
    return result


def cmd_verify(args) -> dict:
    replan = parse_remaining_file(args.remaining) if args.remaining else None
    base = read_body(args.base_json, args.base_file)
    back = read_body(args.readback_json, args.readback_file)
    failed = verify_readback(base, back, replan)
    if failed:
        raise PlanStop(
            "E-PLAN-WRITE-FAILED", "read-back check failed: " + "; ".join(failed)
        )
    return {"cmd": "verify", "result": "ok", "body_sha": body_sha(back)}


def _body_args(parser, prefix: str, required: bool) -> None:
    group = parser.add_mutually_exclusive_group(required=required)
    group.add_argument(f"--{prefix}-json", dest=f"{prefix}_json", metavar="FILE")
    group.add_argument(f"--{prefix}-file", dest=f"{prefix}_file", metavar="FILE")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="apply the plan check to a body")
    _body_args(check, "body", False)
    check.add_argument("--remaining", metavar="FILE")
    splice = sub.add_parser("splice", help="write the new body")
    _body_args(splice, "body", True)
    splice.add_argument("--sections-file", required=True, metavar="FILE")
    splice.add_argument("--out", required=True, metavar="FILE")
    splice.add_argument("--remaining", metavar="FILE")
    splice.add_argument("--before-out", metavar="FILE")
    verify = sub.add_parser("verify", help="check the body read back after the edit")
    _body_args(verify, "base", True)
    _body_args(verify, "readback", True)
    verify.add_argument("--remaining", metavar="FILE")
    return parser


COMMANDS = {"check": cmd_check, "splice": cmd_splice, "verify": cmd_verify}


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = COMMANDS[args.command](args)
    except PlanStop as stop:
        print(str(stop).replace("\n", " "), file=sys.stderr)
        return 1
    except UsageError as err:
        print(f"plan_body.py: {err}".replace("\n", " "), file=sys.stderr)
        return 2
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
