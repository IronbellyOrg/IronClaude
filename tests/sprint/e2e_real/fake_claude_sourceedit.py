#!/usr/bin/env python3
"""Deterministic ``claude`` shim that also injects a mid-flight operator edit.

This is a self-contained sibling of ``fake_claude.py`` used ONLY by
``test_e2e_sha_guard_real_edit.py``. It honours the exact same executor
runtime contract (stdin prompt -> stdout stream-json transcript -> exit code
deciding PASS / FAIL_RECOVERABLE), so it can drive both the initial sprint run
and the rerun.

The one addition: when ``$FAKE_CLAUDE_EDIT_PATH`` is set to a real file path,
the shim *appends* a genuine content line to that file BEFORE emitting its
transcript. In the SHA-guard e2e this path points at the source
``phase-1-tasklist.md``. Because the shim is spawned by the rerun executor's
``execute_sprint(sub_config)`` (step 11), the edit lands in the window between
the rerun engine's step-4 source-SHA capture and its step-12 re-check — exactly
the mid-flight-edit scenario the guard must catch. The appended text is placed
at the END of the file (after the engine's ``<!-- SUPERCLAUDE-RERUN -->``
provenance block), so it is task-content the block-stripping hash WILL see.

To make the edit fire only on the rerun (and never on the initial sprint run),
the harness sets ``$FAKE_CLAUDE_EDIT_PATH`` just before the rerun invocation.

Stdlib-only so it runs under whatever ``/usr/bin/env python3`` resolves to in
the spawned subprocess.
"""

from __future__ import annotations

import json
import os
import re
import sys

_TASK_ID_RE = re.compile(r"\bT\d{2}\.\d{2}\b")

# A unique marker so the test can prove the edit actually landed in the source.
_EDIT_MARKER = "<!-- operator edit -->"
_EDIT_BODY = "Edited body line"


def _read_prompt() -> str:
    try:
        return sys.stdin.read()
    except Exception:  # noqa: BLE001 - stdin closed early; treat as empty
        return ""


def _load_control(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _save_control(path: str, data: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    os.replace(tmp, path)


def _emit_pass_transcript(task_id: str) -> None:
    lines = [
        {"type": "system", "subtype": "init", "task": task_id},
        {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": f"Executing {task_id}"}],
                "usage": {"input_tokens": 120, "output_tokens": 88},
            },
        },
        {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "output_tokens": 88,
            "task": task_id,
        },
    ]
    for obj in lines:
        sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def _emit_transient_fail_transcript(task_id: str) -> None:
    lines = [
        {"type": "system", "subtype": "init", "task": task_id},
        {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "api_retry: connection reset"}],
                "usage": {"input_tokens": 90, "output_tokens": 0},
            },
        },
        {
            "type": "result",
            "subtype": "error_during_execution",
            "is_error": True,
            "output_tokens": 0,
            "task": task_id,
        },
    ]
    for obj in lines:
        sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def _inject_operator_edit() -> None:
    """Append a real task-content line to the source tasklist, if configured.

    Mirrors a human opening ``phase-1-tasklist.md`` mid-rerun and saving an
    edit OUTSIDE the engine's provenance block.
    """
    edit_path = os.environ.get("FAKE_CLAUDE_EDIT_PATH", "")
    if not edit_path:
        return
    try:
        with open(edit_path, "a", encoding="utf-8") as fh:
            fh.write(f"\n{_EDIT_MARKER}\n{_EDIT_BODY}\n")
    except OSError:
        # An inability to edit must not change the PASS/FAIL contract; the test
        # asserts on the edit's effect separately.
        pass


def main() -> int:
    prompt = _read_prompt()
    match = _TASK_ID_RE.search(prompt)
    task_id = match.group(0) if match else "UNKNOWN"

    control_path = os.environ.get("FAKE_CLAUDE_CONTROL", "")
    control = _load_control(control_path) if control_path else {}

    runs = control.setdefault("runs", {})
    runs[task_id] = int(runs.get(task_id, 0)) + 1
    control.setdefault("run_log", []).append(task_id)
    if control_path:
        _save_control(control_path, control)

    # Inject the mid-flight operator edit (no-op unless FAKE_CLAUDE_EDIT_PATH set).
    _inject_operator_edit()

    fail_tasks = set(control.get("fail_tasks", []))
    if task_id in fail_tasks:
        _emit_transient_fail_transcript(task_id)
        return 1

    _emit_pass_transcript(task_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
