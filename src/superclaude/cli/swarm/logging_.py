"""T03.04 -- COMP-012 dual-format JSONL + Markdown event logger.

The :class:`Logger` emits :class:`EventRecord` (DM-015) events to two
side-by-side artifacts that share a single record stream so they cannot
drift:

* ``event-log.jsonl`` -- one JSON object per line, append-only,
  machine-parseable. This is the canonical surface; downstream
  consumers (``swarm status``, ``swarm logs --follow``, post-mortem
  tooling) parse this file.
* ``event-log.md``    -- one human-readable line per event for
  operators tailing the file. No JSON noise; rendered from the same
  :class:`EventRecord` so the two streams cannot disagree.

Append-only + lock-coordinated contract (NFR-002 / FR-026)
==========================================================

Concurrent transport workers (T03.02 ``dispatch_wave1``) call
:meth:`Logger.log_event` in parallel. Without serialization, the
underlying POSIX ``write(2)`` calls would interleave -- two writers
appending the same line at the same instant can land bytes in the
middle of each other's JSON object, leaving the file with one or more
lines that do not parse. Python's GIL does not save us here because
the GIL serializes bytecode, not the kernel-side ``write`` syscall on
the file descriptor.

The fix is a per-:class:`Logger` :class:`threading.Lock` (held for the
duration of one append) plus a *single* ``open(path, "a")`` per event
(``"a"`` mode opens with ``O_APPEND``, so even if the file is being
written by another process the kernel positions the write at end-of-
file atomically per ``write(2)`` call). The lock guarantees we never
emit a partial line; the ``O_APPEND`` guarantee handles the rare case
where two processes (e.g. inline executor + ``swarm attach``) write
the same file.

JSONL appends MUST be append-only (NFR-002); the logger never seeks,
never truncates, and never opens the JSONL file for writing in any
mode other than ``"a"``. Rotation / compaction is an operator concern,
not the logger's.

EventRecord round-trip contract (DM-015)
========================================

Every line emitted to ``event-log.jsonl`` is the JSON encoding of an
:class:`EventRecord` produced by :func:`to_json` (which sorts keys
for byte-stability). The corresponding ``from_json(EventRecord, line)``
call rebuilds the dataclass losslessly -- this is the
``T03.04`` acceptance "EventRecord serialization roundtrip" surface
verified in ``tests/swarm/test_logging.py``.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from superclaude.cli.swarm.models import EventRecord, to_json
from superclaude.cli.swarm.state import confine_path


__all__ = ["Logger"]


class Logger:
    """Dual-format JSONL + Markdown event logger (lock-coordinated).

    One :class:`Logger` instance owns one ``(jsonl_path, md_path)``
    pair and the :class:`threading.Lock` that serializes appends to
    both surfaces. Callers (typically ``dispatch_wave1``) construct a
    single Logger per job and share it across worker threads.

    The class is intentionally minimal: a constructor, an
    :meth:`log_event` entrypoint, and a private Markdown renderer.
    The per-event JSON encoding is delegated to
    :func:`superclaude.cli.swarm.models.to_json` so the wire format
    stays bound to DM-015 (one source of truth for the EventRecord
    serialization).
    """

    def __init__(
        self,
        jsonl_path: Union[str, Path],
        md_path: Union[str, Path],
        *,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        """Bind the logger to its two output paths.

        Args:
            jsonl_path: absolute or relative path to ``event-log.jsonl``.
                Parent directory MUST exist (preflight stamps the
                output directory at Wave 0); this constructor does
                not ``mkdir`` so a misconfigured path surfaces as an
                ``OSError`` at first append rather than silently
                creating a sibling directory outside the job's
                ``--output`` root.
            md_path: absolute or relative path to ``event-log.md``.
                Same parent-directory rules as ``jsonl_path``.
            output_dir: optional ``--output`` root. When supplied,
                both ``jsonl_path`` and ``md_path`` are run through
                :func:`~superclaude.cli.swarm.state.confine_path` at
                construction time and the resolved values stored, so
                NFR-013 / AC-014 confinement is enforced before the
                first ``log_event`` append (an early
                :class:`OutputConfinementError` surfaces the
                misconfiguration before any worker fans out). When
                ``None`` the legacy behaviour is preserved (the
                T03.04 acceptance shape uses no output root).
        """
        if output_dir is not None:
            jsonl_path = confine_path(jsonl_path, output_dir)
            md_path = confine_path(md_path, output_dir)
        self.jsonl_path = Path(jsonl_path)
        self.md_path = Path(md_path)
        self._lock = threading.Lock()

    def log_event(self, record: EventRecord) -> None:
        """Append one :class:`EventRecord` to both logs under the lock.

        Behaviour:
            1. Stamp ``record.timestamp`` with a UTC ISO-8601 string if
               the caller left it empty. (Tests pin specific
               timestamps; production callers leave the field blank.)
            2. Acquire the per-Logger :class:`threading.Lock`.
            3. Append one JSON line (via :func:`to_json`) to
               ``self.jsonl_path``.
            4. Append one Markdown line (rendered via
               :meth:`_render_markdown`) to ``self.md_path``.
            5. Release the lock.

        The two appends are inside the same critical section so a
        crash between the JSONL append and the Markdown append cannot
        leave the two streams out of sync. The JSONL file is the
        canonical surface; if the process dies between steps 3 and 4
        the JSONL line is durable and the Markdown file is missing
        one cosmetic line (recoverable by re-rendering from the
        JSONL).

        Returns:
            ``None``. Errors propagate -- a caller-visible ``OSError``
            on a missing parent directory or full disk is preferable
            to a silently dropped event.
        """
        if not record.timestamp:
            record.timestamp = datetime.now(timezone.utc).isoformat()

        jsonl_line = to_json(record) + "\n"
        md_line = self._render_markdown(record) + "\n"

        with self._lock:
            # ``"a"`` opens with O_APPEND so the kernel positions each
            # write(2) at end-of-file atomically; combined with the
            # lock, no two events ever interleave bytes.
            with open(self.jsonl_path, "a") as jsonl_fh:
                jsonl_fh.write(jsonl_line)
            with open(self.md_path, "a") as md_fh:
                md_fh.write(md_line)

    @staticmethod
    def _render_markdown(record: EventRecord) -> str:
        """Render one :class:`EventRecord` as a single human-readable line.

        Format (kept stable so operators can grep/tail without surprises):

            ``- [<timestamp>] <event_type> worker=<index|->: <payload_summary>``

        ``payload`` is rendered as a compact ``k=v`` list so the line
        stays on one row; the JSONL surface remains authoritative for
        full payload inspection.
        """
        worker = (
            str(record.worker_index)
            if record.worker_index is not None
            else "-"
        )
        if record.payload:
            payload_summary = " ".join(
                f"{key}={value}" for key, value in sorted(record.payload.items())
            )
        else:
            payload_summary = ""
        # Trailing-space trim keeps lines clean when payload is empty.
        return (
            f"- [{record.timestamp}] {record.event_type} worker={worker}: "
            f"{payload_summary}"
        ).rstrip()
