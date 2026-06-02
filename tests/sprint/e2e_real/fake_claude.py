#!/usr/bin/env python3
"""Deterministic ``claude`` shim for the real-subprocess e2e harness.

This standalone script is copied onto ``$PATH`` as an executable named
``claude`` and spawned *for real* by the sprint executor's
``ClaudeProcess.start()`` — there is NO ``subprocess.Popen`` / ``shutil.which``
mock anywhere in the harness. It therefore has to honour the exact runtime
contract the executor relies on for the per-TASK execution path:

Contract (reverse-engineered from ``executor.execute_phase_tasks`` /
``_run_task_subprocess`` / ``_is_transient_failure``):

* The prompt is delivered on **stdin** in the shape::

      Execute task T01.02: <title>
      From phase file: <phase tasklist path>
      Description: ...

  so the shim reads stdin and extracts the ``T<PP>.<TT>`` id.

* The shim's **stdout** is redirected by the parent into the canonical task
  output file (``config.task_output_file`` =
  ``phase-N-task-T<id>-output.txt``). The executor does NOT require the shim
  to write any result file in per-task mode — task PASS/FAIL is decided purely
  from the shim's **exit code** plus, for non-zero exits, the last JSON line of
  that captured stdout:

      exit 0                                   -> TaskStatus.PASS
      exit 124                                 -> TaskStatus.INCOMPLETE
      non-zero AND last-json-line has
        ``is_error: true`` + ``output_tokens == 0``  -> FAIL_RECOVERABLE
      non-zero otherwise                       -> FAIL_TERMINAL

* A CONTROL file (path from ``$FAKE_CLAUDE_CONTROL``) is shared JSON state:
  ``fail_tasks`` lists the task ids that should fail *transiently* on this run,
  and ``runs`` records, per task id, how many times the shim has executed it
  (so the same task can fail on run #1 and pass on the rerun, and so the test
  can prove that only the rerun target was re-executed).

The shim is stdlib-only so it runs under whatever interpreter ``/usr/bin/env
python3`` resolves to inside the spawned subprocess.
"""

from __future__ import annotations

import json
import os
import re
import sys

_TASK_ID_RE = re.compile(r"\bT\d{2}\.\d{2}\b")


def _read_prompt() -> str:
    """Read the full prompt the executor wrote to our stdin."""
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
    """Write a realistic stream-json PASS transcript to stdout.

    The terminal ``{"type":"result", ...}`` line carries ``is_error: false``
    and a non-zero ``output_tokens`` so the legacy transcript classifier
    (used by the rerun discovery fallback) would also read it as PASS. The
    per-task executor path only looks at the exit code, but emitting a
    faithful transcript keeps the artifact honest.
    """
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
    """Write a transcript whose terminal result line marks a transient failure.

    ``_is_transient_failure`` reads the LAST non-blank JSON line of the task
    output file and returns True iff ``is_error`` is truthy AND
    ``output_tokens == 0``. That maps the non-zero exit to
    ``TaskStatus.FAIL_RECOVERABLE``.
    """
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


def main() -> int:
    prompt = _read_prompt()
    match = _TASK_ID_RE.search(prompt)
    task_id = match.group(0) if match else "UNKNOWN"

    control_path = os.environ.get("FAKE_CLAUDE_CONTROL", "")
    control = _load_control(control_path) if control_path else {}

    # Record that this task id was executed in this invocation, and which
    # "generation" of the control file it ran under. The test asserts on the
    # per-task run counter to prove only the rerun target was re-executed.
    runs = control.setdefault("runs", {})
    runs[task_id] = int(runs.get(task_id, 0)) + 1
    control.setdefault("run_log", []).append(task_id)
    if control_path:
        _save_control(control_path, control)

    fail_tasks = set(control.get("fail_tasks", []))
    if task_id in fail_tasks:
        _emit_transient_fail_transcript(task_id)
        # Non-zero, non-124 exit -> executor consults _is_transient_failure,
        # which sees is_error:true + output_tokens:0 -> FAIL_RECOVERABLE.
        return 1

    _emit_pass_transcript(task_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
