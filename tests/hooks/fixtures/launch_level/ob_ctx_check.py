"""OB-CTX coverage checker: counts per row R1-R10 and violations of P1-P6, P8.

Rows and predicates are those of .dev/launch-level-observations/obs-ctx-plan.md
(sections 4 and 7). Input is probe lines: JSONL, or TSV where column 4 is the
JSON payload and column 5 is the store stat or "absent".

P1 session_id present but not a valid id; P4 session_id absent (identity loss).
P2 event or tool shape; P3 agent fields and foreign session ids.
P5 selector verdicts; P6 human shell beside a governed child; P8 row completeness.
P7 (resume, fork) is not a separate predicate: run P1-P4 on the resumed run with
the original --session, and on the fork with its own.
"""

import argparse
import json
import re
import sys
from collections import Counter

ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")
EVENTS = ("UserPromptSubmit", "PreToolUse", "PostToolUse")
STATUS = ("governed", "ordinary", "unknown")
PUSH = re.compile(
    r"^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file"
    r"|update_ref|create_ref|create_branch)"
)
ROWS = {
    "R1": "UserPromptSubmit",
    "R2": "Bash foreground",
    "R3": "Bash background",
    "R4": "Monitor",
    "R5": "Agent",
    "R6": "Skill/Edit/Write",
    "R7": "SendMessage",
    "R8": "NotebookEdit/Cron*/Schedule*",
    "R9": "Task/Workflow/RemoteTrigger/MCP push-class",
    "R10": "Read/Grep/Glob",
    "other": "any other tool",
}
# (row, actor) pairs that P8 needs a PreToolUse (R1: UserPromptSubmit) line for
REQUIRED = [("R1", "main")] + [
    (r, a)
    for r, actors in (
        ("R2", ("main", "sub")),
        ("R3", ("main",)),
        ("R4", ("main",)),
        ("R5", ("main", "sub")),
        ("R6", ("main", "sub")),
        ("R7", ("main", "sub")),
    )
    for a in actors
]
MAX_ORDINARY = (
    2  # LIM-1 (Monitor) and LIM-2 (setsid child) are expected to read ordinary
)


def valid_id(value):
    return isinstance(value, str) and ID.fullmatch(value) is not None


def row_of(event):
    if event.get("hook_event_name") == "UserPromptSubmit":
        return "R1"
    tool, inputs = event.get("tool_name"), event.get("tool_input")
    if tool == "Bash":
        bg = isinstance(inputs, dict) and inputs.get("run_in_background") is True
        return "R3" if bg else "R2"
    for row, match in (
        ("R4", tool == "Monitor"),
        ("R5", tool == "Agent"),
        ("R6", tool in ("Skill", "Edit", "Write")),
        ("R7", tool == "SendMessage"),
        (
            "R8",
            isinstance(tool, str)
            and re.fullmatch(r"NotebookEdit|Cron\w*|Schedule\w*", tool),
        ),
        (
            "R9",
            isinstance(tool, str)
            and (tool in ("Task", "Workflow", "RemoteTrigger") or PUSH.match(tool)),
        ),
        ("R10", tool in ("Read", "Grep", "Glob")),
    ):
        if match:
            return row
    return "other"


def verdicts(value):
    """Every selector verdict dict found in a value, a JSON-lines string or a list."""
    if isinstance(value, dict):
        if value.get("status") in STATUS:
            return [value]
        return [v for item in value.values() for v in verdicts(item)]
    if isinstance(value, list):
        return [v for item in value for v in verdicts(item)]
    found = []
    if isinstance(value, str):
        for line in value.splitlines():
            try:
                parsed = json.loads(line)
            except ValueError:
                continue
            if isinstance(parsed, (dict, list)):
                found += verdicts(parsed)
    return found


def jsonl_records(text):
    return [
        (n, line, None) for n, line in enumerate(text.splitlines(), 1) if line.strip()
    ]


def tsv_records(text):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        cols = line.split("\t")
        if line.strip() and len(cols) > 3:
            out.append((n, cols[3], cols[4] if len(cols) > 4 else None))
    return out


def check_event(n, event, governed, add):
    sid = event.get("session_id")
    if "session_id" not in event:
        add("P4", n, "no session_id (identity loss)")
    elif not valid_id(sid):
        add("P1", n, f"session_id is not a valid id: {sid!r}")
    elif sid not in governed:
        add("P3", n, f"session_id {sid!r} is not a governed session of this run")
    kind = event.get("hook_event_name")
    if kind not in EVENTS:
        add("P2", n, f"unexpected hook_event_name {kind!r}")
    elif kind == "UserPromptSubmit":
        if not isinstance(event.get("prompt"), str):
            add("P2", n, "UserPromptSubmit without a string prompt")
    else:
        if not isinstance(event.get("tool_name"), str):
            add("P2", n, "tool_name is not a string")
        if not isinstance(event.get("tool_input"), dict):
            add("P2", n, "tool_input is not an object")
        if not valid_id(event.get("tool_use_id")):
            add("P2", n, f"tool_use_id is not a valid id: {event.get('tool_use_id')!r}")
    for field in ("agent_id", "agent_type"):
        if field in event and not isinstance(event[field], str):
            add("P3", n, f"{field} is not a string: {event[field]!r}")


def check_human(text, governed, add):
    seen = {}
    for line in text.splitlines():
        for key, label in (
            ("human shell", "human"),
            ("governed job child", "child"),
            ("background job child", "child"),
        ):
            if line.startswith(key) and "{" in line:
                try:
                    seen[label] = json.JSONDecoder().raw_decode(
                        line[line.index("{") :]
                    )[0]
                except ValueError:
                    pass
    human, child = seen.get("human"), seen.get("child")
    if not isinstance(human, dict) or human.get("status") != "ordinary":
        add("P6", 0, f"human shell verdict is not ordinary: {human!r}")
    if (
        not isinstance(child, dict)
        or child.get("status") != "governed"
        or child.get("session_id") not in governed
    ):
        add(
            "P6",
            0,
            f"governed job child verdict is not governed with a run session id: {child!r}",
        )


def check(
    records,
    sessions=(),
    store_column=False,
    verdict_text=None,
    human_text=None,
    complete=False,
):
    """Return {counts, violations, scoped, verdicts, governed}; a void run is a VOID violation."""
    violations, counts, events = [], Counter(), []

    def add(pred, n, msg):
        violations.append((pred, n, msg))

    for n, text, store in records:
        if store_column and store in (None, "absent"):
            continue  # not a governed line
        try:
            event = json.loads(text)
        except ValueError:
            event = None
        if isinstance(event, dict):
            events.append((n, event))
        else:
            add("P2", n, "line is not a JSON object")
    main_ids = {
        e["session_id"]
        for _, e in events
        if "agent_id" not in e and valid_id(e.get("session_id"))
    }
    governed = set(sessions) or main_ids
    for n, event in events:
        check_event(n, event, governed, add)
        actor = "sub" if "agent_id" in event else "main"
        key = (
            "ups"
            if event.get("hook_event_name") == "UserPromptSubmit"
            else str(event.get("hook_event_name"))[:4].lower() + "_" + actor
        )
        counts[(row_of(event), key)] += 1
    found = None
    if verdict_text is not None:
        found = verdicts(verdict_text)
        if not found:
            add("P5", 0, "no selector verdicts found")
        for v in found:
            if v["status"] == "unknown":
                add("P5", 0, f"verdict unknown: {v}")
            elif v["status"] == "governed" and v.get("session_id") not in governed:
                add("P5", 0, f"governed verdict with a foreign session id: {v}")
        if sum(v["status"] == "ordinary" for v in found) > MAX_ORDINARY:
            add(
                "P5",
                0,
                f"more than {MAX_ORDINARY} ordinary verdicts (only LIM-1 and LIM-2 are expected)",
            )
    if human_text is not None:
        check_human(human_text, governed, add)
    if complete:
        for row, actor in REQUIRED:
            key = "ups" if row == "R1" else f"pret_{actor}"
            if not counts[(row, key)]:
                add(
                    "P8",
                    0,
                    f"no {'UserPromptSubmit' if row == 'R1' else 'PreToolUse'} line for {row} {ROWS[row]} by {actor}",
                )
    scoped = len(events)
    if not scoped:
        add("VOID", 0, "no governed lines in scope: the run is void, not a pass")
    return {
        "counts": counts,
        "violations": violations,
        "scoped": scoped,
        "verdicts": found,
        "governed": governed,
    }


def render(result):
    counts = result["counts"]
    cols = ("ups", "pret_main", "post_main", "pret_sub", "post_sub")
    out = ["row\twhat\t" + "\t".join(cols)]
    for row, what in ROWS.items():
        out.append(f"{row}\t{what}\t" + "\t".join(str(counts[(row, c)]) for c in cols))
    out.append(
        f"# governed lines in scope: {result['scoped']}; sessions: {', '.join(sorted(result['governed'])) or '-'}"
    )
    if result["verdicts"] is not None:
        out.append(
            "# verdicts: "
            + ", ".join(
                f"{s}={sum(v['status'] == s for v in result['verdicts'])}"
                for s in STATUS
            )
        )
    for pred, n, msg in result["violations"]:
        out.append(f"VIOLATION\t{pred}\tline {n}\t{msg}")
    out.append(f"OB-CTX-CHECK violations={len(result['violations'])}")
    return "\n".join(out)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--jsonl")
    source.add_argument("--tsv")
    parser.add_argument(
        "--governed-store-column",
        action="store_true",
        help="TSV: a line is governed when column 5 is not 'absent'",
    )
    parser.add_argument(
        "--session",
        action="append",
        default=[],
        help="governed session id (repeatable)",
    )
    parser.add_argument("--human-file")
    parser.add_argument("--stream", help="file holding the selector verdict lines (P5)")
    parser.add_argument(
        "--complete", action="store_true", help="also check P8 row completeness"
    )
    args = parser.parse_args(argv)
    records = (
        jsonl_records(read(args.jsonl)) if args.jsonl else tsv_records(read(args.tsv))
    )
    result = check(
        records,
        args.session,
        store_column=args.governed_store_column,
        verdict_text=read(args.stream) if args.stream else None,
        human_text=read(args.human_file) if args.human_file else None,
        complete=args.complete,
    )
    print(render(result))
    return 0 if not result["violations"] else 1


if __name__ == "__main__":
    sys.exit(main())
