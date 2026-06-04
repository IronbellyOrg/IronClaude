"""File-backed per-task handoff store (Stage 1, SYNTHESIS H4/M4).

Persists runner-constructed ``HandoffRecord`` objects to
``<results_dir>/handoff/phase-{N}-task-{task_id}.json`` using the canonical
atomic temp+replace idiom (``checkpoints.write_manifest``): write to a ``.tmp``
sibling then ``Path.replace`` it into place. The atomic write prevents
partial-write corruption of the JSON state if the process dies mid-write — a
reader never sees a half-written handoff file (important once resume treats the
handoff file, not the lock-free JSONL journal, as the authoritative completion
source).

``handoff_store: str = "file"`` (SprintConfig) selects this backend; "mail" is
reserved for the out-of-scope Stage 4 pilot.
"""

from __future__ import annotations

import json

from .models import GateOutcome, HandoffRecord, SprintConfig, TaskStatus


def is_validated_success(record: HandoffRecord) -> bool:
    """Resume skip predicate (H5 item 1): a *validated successful* record.

    Returns True ONLY when the task both PASSed and its gate succeeded — i.e.
    ``record.status == TaskStatus.PASS.value`` AND
    ``GateOutcome(record.gate_outcome).is_success``. Mere file existence is
    unsafe: ``FAIL_*``/``INCOMPLETE``/``SKIPPED`` tasks (and PASS-with-gate-fail)
    also leave records behind, and resume must NOT skip those. Per the H4 schema
    fix, ``gate_outcome`` is always the ``GateOutcome`` enum's ``.value`` string
    (never None, never a dict), so there is no None/absent-gate branch to decide.
    """
    if record.status != TaskStatus.PASS.value:
        return False
    try:
        return GateOutcome(record.gate_outcome).is_success
    except ValueError:
        # Defensive: an unrecognized gate_outcome string is not a validated success.
        return False


class FileHandoffStore:
    """Atomic file-backed store for per-task HandoffRecords."""

    def __init__(self, config: SprintConfig) -> None:
        self.config = config

    def write(self, record: HandoffRecord, *, phase, task) -> None:
        """Atomically persist ``record`` to ``config.handoff_file(phase, task)``.

        Uses the temp+replace idiom (mkdir parents → write ``.tmp`` →
        ``tmp.replace``) so a concurrent or crashing writer can never leave a
        partially-written JSON file in place.
        """
        path = self.config.handoff_file(phase, task)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(record.to_dict(), indent=2) + "\n")
        tmp.replace(path)

    def read(self, *, phase, task) -> HandoffRecord | None:
        """Return the stored ``HandoffRecord`` or typed ``None`` if absent.

        A missing handoff file returns ``None`` (does not raise) — resume and
        back-compat paths rely on this to degrade gracefully. A corrupt or
        unparseable handoff file also returns ``None`` (corrupt == absent), so a
        truncated/garbled record degrades to a re-run rather than aborting resume.
        """
        path = self.config.handoff_file(phase, task)
        if not path.exists():
            return None
        try:
            return HandoffRecord.from_dict(json.loads(path.read_text()))
        except (json.JSONDecodeError, ValueError):
            return None
