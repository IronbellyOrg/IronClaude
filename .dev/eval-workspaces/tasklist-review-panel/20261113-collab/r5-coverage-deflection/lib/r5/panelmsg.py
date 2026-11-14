"""panel-msg/1 validator for kind "coverage" (DESIGN 2.2; R-06, R-08)."""
import json
import re
import sys
from dataclasses import dataclass, field

KEYS = {"v", "id", "run", "from", "to", "t", "kind", "items"}
TASK_ID = re.compile(r"^T[1-9][0-9]?$")
TASK_HEADING = re.compile(r"^## Task (\d+):", re.M)


@dataclass
class Ctx:
    candidate_tasks: set
    receivers: set
    k: int
    run: str | None = None  # None: run is not checked (CLI without a run argument)
    seen_ids: set = field(default_factory=set)


def candidate_tasks(text: str) -> set:
    return {f"T{n}" for n in TASK_HEADING.findall(text)}


def validate(line: str, ctx: Ctx) -> tuple[bool, str]:
    line = line.rstrip("\n")
    if len(line.encode("utf-8")) > 600:
        return False, "over 600 bytes"
    try:
        obj = json.loads(line)
    except ValueError:
        return False, "invalid JSON"
    if not isinstance(obj, dict):
        return False, "not one JSON object"
    if set(obj) != KEYS:
        extra = sorted(set(obj) - KEYS)
        return False, f"keys must be exactly {sorted(KEYS)}" + (f"; forbidden {extra}" if extra else "")
    if obj["v"] != "panel-msg/1" or obj["kind"] != "coverage" or obj["from"] != "watcher":
        return False, "v, kind or from is wrong"
    if obj["to"] not in ctx.receivers:
        return False, "to is not a receiver"
    if ctx.run is not None and obj["run"] != ctx.run:
        return False, "run mismatch"
    if not isinstance(obj["t"], int) or isinstance(obj["t"], bool):
        return False, "t must be an integer"
    items = obj["items"]
    if not isinstance(items, list) or not items or len(items) > ctx.k:
        return False, "items must be a non-empty list of at most k"
    if len(set(map(str, items))) != len(items):
        return False, "duplicate items"
    for it in items:
        if not isinstance(it, str) or not TASK_ID.match(it) or it not in ctx.candidate_tasks:
            return False, f"item {it!r} is not a candidate Task id"
    if not isinstance(obj["id"], str) or obj["id"] in ctx.seen_ids:
        return False, "id missing or not unique"
    ctx.seen_ids.add(obj["id"])
    return True, "ok"


def main(argv: list[str]) -> int:
    cand, k, receivers = argv[0], int(argv[1]), set(argv[2].split(","))
    ctx = Ctx(candidate_tasks(open(cand).read()), receivers, k, argv[3] if len(argv) > 3 else None)
    bad = 0
    for line in sys.stdin:
        if not line.strip():
            continue
        ok, why = validate(line, ctx)
        print(json.dumps({"ok": ok, "reason": why}))
        bad += not ok
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
