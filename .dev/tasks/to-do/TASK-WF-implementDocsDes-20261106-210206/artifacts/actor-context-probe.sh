#!/usr/bin/env bash
# Log-only Linux feasibility probe. No argv, environment values or enforcement writes.
set -euo pipefail
exec uv run --no-project python -I - "$@" <<'PY'
import json
import os
from pathlib import Path
import subprocess
import sys

LIMIT = 64  # Diagnostic bound only; not a proven production ancestry limit.

def process(pid):
    text = Path(f"/proc/{pid}/stat").read_text()
    # comm can contain spaces and ')'; all following stat fields are numeric.
    fields = text[text.rfind(") ") + 2:].split()
    return {"pid": pid, "ppid": int(fields[1]), "start_ticks": int(fields[19]),
            "comm": Path(f"/proc/{pid}/comm").read_text().strip()}

def ancestry(pid):
    rows = []
    seen = set()
    for _ in range(LIMIT):
        if pid <= 0:
            return {"rows": rows, "stop": "root"}
        if pid in seen:
            return {"rows": rows, "stop": "cycle"}
        seen.add(pid)
        try:
            row = process(pid)
        except (OSError, ValueError, IndexError) as exc:
            return {"rows": rows, "stop": type(exc).__name__}
        rows.append(row)
        pid = row["ppid"]
    return {"rows": rows, "stop": "bound-exhausted"}

def selected(pid, identity):
    return any((row["pid"], row["start_ticks"]) == identity
               for row in ancestry(pid)["rows"])

children = []
try:
    current = process(os.getpid())
    identity = (current["pid"], current["start_ticks"])
    # Both children read stdin until their controller closes it; no fixed sleep.
    code = "import sys; sys.stdin.buffer.read()"
    for _ in range(2):
        children.append(subprocess.Popen([sys.executable, "-I", "-c", code],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL))
    results = [selected(child.pid, identity) for child in children]
    assert results == [True, True]
    assert not selected(children[0].pid, (identity[0], identity[1] + 1))
    assert not selected(children[0].pid, (0, identity[1]))
    payload = {
        "schema": "actor-context-probe/1",
        "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
        "diagnostic_bound": LIMIT,
        "current_ancestry": ancestry(os.getpid()),
        "controlled_children": [ancestry(child.pid) for child in children],
        "controlled_result": {
            "both_children_match_one_ancestor": results,
            "different_start_identity_rejected": True,
            "nonmatching_pid_rejected": True,
            "session_reset_observed": False,
            "meaning": "Kernel ancestry alone does not encode two logical session memberships. This is a controlled topology check, not a real Claude reset observation."
        },
        "runtime_cases_not_observed": [
            "real Claude /clear with old governed child and new ordinary session",
            "real resume/fork across Claude processes",
            "main/subagent/nested Bash and Monitor hook event identities",
            "same-worktree human terminal versus actual claim-launched agent",
            "detached/reparented actual agent job",
            "actual process ID reuse or reboot",
            "release of real bound session while old background child remains alive"
        ],
        "gate": "BLOCKED",
        "self_checks": 3,
        "production_changes": False
    }
    print(json.dumps(payload, indent=2))
finally:
    for child in children:
        if child.stdin:
            child.stdin.close()
        try:
            child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(timeout=3)
PY
