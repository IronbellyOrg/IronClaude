"""Exports: the plain-text record and the versioned JSON snapshot, both from one ``View`` (AD-11, AD-12).

Both read only ``view.all_rows`` and the session-independent blocks, so an export is lossless
whatever the filter, the historical toggle or the selection. Neither goes through the screen
renderer or any console. This is the only module that turns the ``UNKNOWN`` sentinel into the
snapshot string ``"UNKNOWN"``.
"""

from __future__ import annotations

import json
import os
import tempfile
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

from superclaude.cli.observe.sanitize import sanitize
from superclaude.cli.observe.view import ORDER_UNKNOWN_FLAG, UNKNOWN, RowView, View

SCHEMA_VERSION = 1
SCHEMA_PACKAGE = "superclaude.cli.observe"
SCHEMA_FILE = "snapshot.schema.json"
SNAPSHOT_NAME = "snapshot.json"
UNKNOWN_TEXT = "UNKNOWN"  # the snapshot spelling of a missing value

SCHEMA: dict = json.loads(
    resources.files(SCHEMA_PACKAGE).joinpath(SCHEMA_FILE).read_text(encoding="utf-8")
)
Draft7Validator.check_schema(
    SCHEMA
)  # a broken schema fails at import, not in the field

# snapshot key (dotted for nesting) -> attribute of the typed row
_TEXT_FIELDS = (
    ("dispatchId", "dispatch_id"),
    ("taskId", "task_id"),
    ("runId", "run_id"),
    ("workerState", "worker_state"),
    ("dispatchStatus", "dispatch_status"),
    ("terminalState", "terminal_state"),
    ("role", "role"),
    ("provider", "provider_id"),
    ("hostKind", "host_kind"),
    ("hostId", "host_id"),
    ("stage.worker", "stage_worker"),
    ("stage.dispatch", "stage_dispatch"),
    ("outcome", "outcome"),
    ("liveness.verdict", "liveness_verdict"),
    ("liveness.source", "liveness_source"),
    ("liveness.observedAt", "liveness_observed_at"),
    ("evidence.liveStatus", "evidence_live_status"),
    ("evidence.lastObservedAt", "evidence_last_observed_at"),
    ("nextAction", "next_action_kind"),
)
_ANY_FIELDS = (("evidence.durable", "evidence_durable"),)  # a JSON value as given
_KEY_OF_ATTR = {attr: key for key, attr in (*_TEXT_FIELDS, *_ANY_FIELDS)}


# -- plain-text record ---------------------------------------------------------------------------


def _row_line(row: RowView) -> str:
    fields = [
        ("dispatchId", row.dispatch_id),
        ("run", row.run),
        ("workerState", row.worker_state),
        ("dispatchStatus", row.dispatch_status),
        ("terminalState", row.terminal_state),
        ("outcome", row.outcome),
        ("nextAction", row.next_action),
        ("liveness", row.liveness),
        ("evidenceAge", row.evidence_age),
    ]
    if row.flags:
        fields.append(("flags", ", ".join(row.flags)))
    line = " | ".join(f"{name}={value}" for name, value in fields)
    return sanitize(line, "line")  # one line per row, whatever the identifier held


def record_text(view: View) -> str:
    """The ``e`` and ``--once`` record: full identifiers, no truncation, one line per row."""
    filter_name = view.filter_text or "none"
    historical = "shown" if view.show_historical else "hidden"
    lines = [
        view.header1,
        view.header2,
        "  ".join(token.text for token in view.counts_tokens),
        f"screen filter: {filter_name}  historical rows on screen: {historical}  (this record lists every collected row)",
        view.gap_notice,
        view.ledger_title,
    ]
    lines.extend(view.ledger_empty)
    lines.extend(_row_line(row) for row in view.all_rows)
    return "\n".join(sanitize(line, "line") for line in lines) + "\n"


# -- JSON snapshot -----------------------------------------------------------------------------------


def _unknown(value: Any) -> Any:
    return UNKNOWN_TEXT if value is UNKNOWN else value


def _text(value: Any) -> Any:
    if value is UNKNOWN:
        return UNKNOWN_TEXT
    return value if isinstance(value, str) else json.dumps(value)


def _set(target: dict, dotted: str, value: Any) -> None:
    *parents, leaf = dotted.split(".")
    for key in parents:
        target = target.setdefault(key, {})
    target[leaf] = value


def _row_dict(view_row: RowView) -> dict:
    raw = view_row.raw
    out: dict = {}
    for key, attr in _TEXT_FIELDS:
        _set(out, key, _text(getattr(raw, attr)))
    for key, attr in _ANY_FIELDS:
        _set(out, key, _unknown(getattr(raw, attr)))
    if ORDER_UNKNOWN_FLAG in raw.flags:
        out["orderUnknown"] = True
    if not raw.reobserved:
        out["notReobserved"] = True
    absent = sorted(_KEY_OF_ATTR[a] for a in raw.absent_fields if a in _KEY_OF_ATTR)
    if absent:
        out["absentFields"] = absent
    return out


def snapshot_dict(view: View) -> dict:
    meta = view.meta
    source: dict = {
        "namespace": meta.namespace or UNKNOWN_TEXT,
        "status": meta.source_status,
        "observedAt": _unknown(meta.source_observed_at),
    }
    if meta.source_error is not None:
        source["error"] = meta.source_error
    snapshot: dict = {
        "schemaVersion": SCHEMA_VERSION,
        "producer": {"name": meta.producer_name, "version": meta.producer_version},
        "cycle": meta.cycle,
        "generatedAt": meta.generated_at,
        "source": source,
        "page": {
            "hasMore": _unknown(meta.has_more),
            "total": _unknown(meta.total),
            "limit": _unknown(meta.limit),
        },
        "scope": _unknown(meta.scope),
        "counts": _unknown(meta.counts),
        "rows": [_row_dict(row) for row in view.all_rows],
    }
    if meta.collection_state is not None:
        snapshot["collection"] = {
            "state": meta.collection_state,
            "collected": meta.collection_collected,
            "changedDuringRead": meta.collection_changed_during_read,
            "duplicatesIgnored": meta.collection_duplicates_ignored,
        }
    return snapshot


def snapshot_json(view: View) -> str:
    """Snapshot v1: ``json.dumps(indent=2, sort_keys=True)``, every collected row, filter-independent."""
    # ``default`` maps a sentinel nested inside ``scope`` or ``counts`` (parse caps depth at 6).
    return json.dumps(
        snapshot_dict(view), indent=2, sort_keys=True, default=_unknown_in_json
    )


def _unknown_in_json(value: Any) -> Any:
    if value is UNKNOWN:
        return UNKNOWN_TEXT
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


# -- files ---------------------------------------------------------------------------------------------


def state_dir(env: dict | None = None, home: str | None = None) -> Path:
    """``$XDG_STATE_HOME/superclaude/observe`` (when absolute), else ``~/.local/state/superclaude/observe``."""
    env = os.environ if env is None else env
    base = env.get("XDG_STATE_HOME", "")
    if base and os.path.isabs(base):
        root = Path(base)
    else:
        root = Path(home if home is not None else Path.home()) / ".local" / "state"
    return root / "superclaude" / "observe"


def record_path(directory: Path, view: View) -> Path:
    """A timestamped record name built from the view's generation time."""
    stamp = view.meta.generated_at.replace(":", "-")
    return directory / f"observe-{stamp}.txt"


def snapshot_path(directory: Path) -> Path:
    return directory / SNAPSHOT_NAME


def write_atomic(path: Path, text: str) -> Path:
    """Write ``text`` to ``path`` mode 0600 via a temporary file in the same directory and ``os.replace``."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".observe-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    except BaseException:
        try:
            os.unlink(temp)
        except FileNotFoundError:
            pass
        raise
    return path
