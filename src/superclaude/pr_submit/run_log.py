"""Write-ahead JSONL run-log substrate for the ``sc:pr-submit`` core (spec §11).

The append-only ``monitor-run-<PR>.jsonl`` is AUTHORITATIVE; ``state.snapshot.json``
is a rebuildable cache. Every external action is preceded by a write-ahead record
fsynced BEFORE the side effect (the load-bearing crash-safety primitive — the push
triad in §12.1 is its instance). On snapshot/JSONL disagreement, rebuild FROM the
JSONL (NFR-6).

NFR-7 (credential redaction): no token/credential pattern ever reaches the JSONL —
:func:`_redact` scrubs values before they are written (T-N51).

Core purity: this module is pure file/fsync I/O — it contains no shell or
version-control command tokens.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from .models import EventType

# The 5 idempotency sets (§11.4).
IDEMPOTENCY_SETS = (
    "processed_review_ids",
    "processed_finding_ids",  # keyed on fix_key
    "replied_comment_ids",
    "resolved_thread_ids",
    "pushed_commit_shas",
)

_VALID_EVENT_VALUES = frozenset(e.value for e in EventType)

# NFR-7 credential/token patterns scrubbed before any value reaches the JSONL.
_REDACTION_PATTERNS = [
    re.compile(
        r"gh[pousr]_[A-Za-z0-9]{16,}"
    ),  # GitHub PATs / tokens (ghp_/gho_/ghu_/ghs_/ghr_)
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{8,}"),
    re.compile(
        r"(?i)(password|passwd|secret|api[_-]?key|token|access[_-]?key)"
        r"\s*[:=]\s*['\"]?[^'\"\s]{4,}"
    ),
    re.compile(r"sk-[A-Za-z0-9]{16,}"),  # generic secret-key prefix
]
_REDACTED = "[REDACTED]"


def fix_key(path: str, line: int | str, body: str) -> str:
    """``sha256(path + line + finding_body)`` — comment_id-INDEPENDENT (INV-009 / §11.4)."""
    return hashlib.sha256(f"{path}\n{line}\n{body}".encode("utf-8")).hexdigest()


def _redact(value):
    """Recursively scrub credential/token patterns from a value (NFR-7)."""
    if isinstance(value, str):
        scrubbed = value
        for pat in _REDACTION_PATTERNS:
            scrubbed = pat.sub(_REDACTED, scrubbed)
        return scrubbed
    if isinstance(value, dict):
        return {k: _redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact(v) for v in value]
    return value


class RunLog:
    """The authoritative append-only run-log + its materialized snapshot cache."""

    def __init__(self, pr_number: int, output_dir: str | Path):
        self.pr_number = pr_number
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.jsonl_path = self.output_dir / f"monitor-run-{pr_number}.jsonl"
        self.snapshot_path = self.output_dir / "state.snapshot.json"
        self._event_id = 0
        # If resuming an existing log, continue the event_id from the last line.
        if self.jsonl_path.exists():
            self._event_id = self._last_event_id()

    # --- writing ---------------------------------------------------------- #

    def _last_event_id(self) -> int:
        last = 0
        for line in self.jsonl_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                last = max(last, int(json.loads(line).get("event_id", 0)))
            except (ValueError, json.JSONDecodeError):
                continue
        return last

    def append(self, event: dict) -> dict:
        """Append a validated, redacted event with a monotonic ``event_id`` and fsync.

        Raises :class:`ValueError` if ``event_type`` is not one of the 33 closed
        enum values (the run-log writer validates against ``models.EventType``).
        """
        event_type = event.get("event_type")
        if event_type not in _VALID_EVENT_VALUES:
            raise ValueError(
                f"unknown event_type: {event_type!r} (not one of the 33 §11.3 events)"
            )
        self._event_id += 1
        record = {
            "schema_version": "1.0",
            "event_id": self._event_id,
            **_redact(event),
        }
        record.setdefault("timestamp", None)
        with self.jsonl_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return record

    def write_ahead(self, event: dict) -> dict:
        """Append + fsync BEFORE returning, so the caller performs the side effect after.

        Identical durability to :meth:`append`; named distinctly to mark the call
        sites where the fsync MUST precede the external action (§11.1).
        """
        return self.append(event)

    # --- reading / state -------------------------------------------------- #

    def read_events(self) -> list[dict]:
        """Return all events from the authoritative JSONL, in order."""
        if not self.jsonl_path.exists():
            return []
        events = []
        for line in self.jsonl_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                events.append(json.loads(line))
        return events

    def rebuild_state(self) -> dict:
        """Fold the authoritative JSONL into a state snapshot (the NFR-6 rebuild path).

        Reconstructs the FSM state, ``round_counter``, the 5 idempotency sets, and
        ``push_count``/``reply_count`` from the event stream. This is the source of
        truth on any snapshot/JSONL disagreement.
        """
        state = {
            "pr_number": self.pr_number,
            "state": None,
            "round_counter": 0,
            "push_count": 0,
            "reply_count": 0,
            "last_event_id": 0,
            **{s: [] for s in IDEMPOTENCY_SETS},
        }
        sets = {s: set() for s in IDEMPOTENCY_SETS}
        for ev in self.read_events():
            state["last_event_id"] = ev.get("event_id", state["last_event_id"])
            et = ev.get("event_type")
            if ev.get("state_after"):
                state["state"] = ev["state_after"]
            if et == EventType.ROUND_INCREMENTED.value:
                state["round_counter"] += 1
            elif et == EventType.PUSH_COMPLETED.value:
                state["push_count"] += 1
                if ev.get("target_sha"):
                    sets["pushed_commit_shas"].add(ev["target_sha"])
            elif et == EventType.REPLY_POSTED.value:
                state["reply_count"] += 1
                if ev.get("comment_id") is not None:
                    sets["replied_comment_ids"].add(ev["comment_id"])
            elif et == EventType.THREAD_RESOLVED.value and ev.get("thread_id"):
                sets["resolved_thread_ids"].add(ev["thread_id"])
            elif (
                et == EventType.FINDINGS_NORMALIZED.value
                and ev.get("review_id") is not None
            ):
                # A normalized finding set implies its review was processed (the
                # emission-level mapping: findings_normalized.review_id is keyed here).
                sets["processed_review_ids"].add(ev["review_id"])
            elif et == EventType.FIX_APPLIED.value and ev.get("fix_key"):
                sets["processed_finding_ids"].add(ev["fix_key"])
        for s in IDEMPOTENCY_SETS:
            state[s] = sorted(sets[s], key=str)
        return state

    def materialize_snapshot(self) -> dict:
        """Write the rebuilt state to ``state.snapshot.json`` (a rebuildable cache)."""
        state = self.rebuild_state()
        self.snapshot_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        return state

    # --- idempotency ------------------------------------------------------ #

    def record_idempotent(self, set_name: str, key) -> bool:
        """Record ``key`` in an idempotency set; append ``idempotency_skip`` if already present.

        Returns True if newly recorded (the action should proceed), False if the key
        was already present (the action is skipped and an ``idempotency_skip`` event
        is appended). Dedup of fixes is keyed on ``fix_key`` (comment_id-independent).
        """
        if set_name not in IDEMPOTENCY_SETS:
            raise ValueError(f"unknown idempotency set: {set_name!r}")
        state = self.rebuild_state()
        if str(key) in {str(k) for k in state.get(set_name, [])}:
            self.append(
                {
                    "event_type": EventType.IDEMPOTENCY_SKIP.value,
                    "set": set_name,
                    "key": str(key),
                }
            )
            return False
        return True

    # --- output-dir resolution ------------------------------------------- #

    @staticmethod
    def default_output_dir(pr_number: int, timestamp: str) -> Path:
        """Default ``<output-dir>`` = ``.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/`` (§11.2).

        ``timestamp`` is supplied by the caller (the SKILL) so this stays pure.
        """
        return Path(
            f"/config/workspace/IronClaude/.dev/pr-monitor/pr-{pr_number}-{timestamp}"
        )

    def round_dirs(self, round_n: int) -> tuple[Path, Path]:
        """Create + return the ``validation/round-<N>/`` and ``troubleshoot/round-<N>/`` subdirs."""
        val = self.output_dir / "validation" / f"round-{round_n}"
        ts = self.output_dir / "troubleshoot" / f"round-{round_n}"
        val.mkdir(parents=True, exist_ok=True)
        ts.mkdir(parents=True, exist_ok=True)
        return val, ts
