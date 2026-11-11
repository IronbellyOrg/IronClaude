e5713941b11dd572ae6240353e5a34f39861bfd0
Review one task for spec compliance.

Task brief: 
## Task 11: Build the exports and JSON snapshot schema `export.py`

Depends on: Task 8

Create `src/superclaude/cli/observe/export.py`, `src/superclaude/cli/observe/snapshot.schema.json`, `tests/observe/test_export.py` and `tests/observe/test_snapshot_schema.py`, following `ARCHITECTURE-SPINE.md` AD-11, AD-12, AD-20 and CD-3, CD-6, `snapshot-export-schema.md` (every field, type and rule), SNAPSRC and tests T27 and T48 in `acceptance-tests.md`. `record_text(view) -> str` is the text record for `e` and `--once`: no ESC byte, full identifiers, no truncation, one line per row, header naming the active filter and historical toggle; it reads only `view.all_rows` and session-independent blocks. `snapshot_json(view) -> str` emits the version 1 snapshot with `json.dumps(indent=2, sort_keys=True)`: envelope `schemaVersion` (1), `producer.name` and `producer.version`, `cycle`, `generatedAt` (UTC ISO 8601), `source.namespace`, `source.status` (`OK`, `STALE`, `ERROR` or `UNKNOWN`, with FAILED mapped to `ERROR` and NOT_POLLED and NOT_AVAILABLE to `UNKNOWN`), `source.observedAt`, `source.error` (the short code only, present only on `ERROR`), `page.hasMore`, `page.total`, `page.limit`, `scope`, `counts` (passed through, never summed), the optional `collection.*` fields and `rows`; each row has the fields in the Row table of `snapshot-export-schema.md` as nested objects (for example `stage.worker` is the key `worker` inside `stage`), the optional `orderUnknown`, `notReobserved` and `absentFields`, rows in timestamp order newest first with ties by `dispatchId` then namespace, every collected row including historical ones whatever the filter, a missing value as the string `UNKNOWN` (only `export.py` maps the sentinel), and never `stage.detail`, `stage.activity`, terminal handles, worktree or endpoint ids, ownership or release state, warnings, `page.nextCursor`, message bodies, prompts, file contents or credentials. `snapshot.schema.json` is a JSON Schema (Draft 7, checked with `Draft7Validator.check_schema` at import) with `additionalProperties: false` on the producer side; consumers reject an unknown major `schemaVersion` and ignore unknown fields. A helper writes a file by writing a temporary file in the same directory, setting mode 0600 and calling `os.replace`, and `state_dir()` returns `$XDG_STATE_HOME/superclaude/observe` or `~/.local/state/superclaude/observe`. Neither export function goes through a Rich `Console`, and `export.py` does not import `render.py`, `parse.py` or `adapter.py`.

Acceptance criteria:
- [T11.AC1] `uv run pytest tests/observe/test_export.py tests/observe/test_snapshot_schema.py -v` passes.
- [T11.AC2] The schema test validates the snapshot of every fixture variant (including `missing-fields`, `injection` and `source-loss`) against `snapshot.schema.json`, rejects a copy with `schemaVersion` 2, rejects an added unknown field on the producer schema, asserts every missing value is the string `UNKNOWN` and that `absentFields` separates a missing key from a source value that is the text `UNKNOWN`.
- [T11.AC3] The schema test asserts no snapshot contains the words or keys for message bodies, prompts, file contents, credentials, `stage.detail`, `stage.activity`, terminal handles or worktree ids, by scanning the serialized output and the fixture inputs.
- [T11.AC4] T27: `record_text` contains no ESC byte, full identifiers and no truncation marker for the `long-identifiers` variant.
- [T11.AC5] T29 (export half): for the `injection` variant, `record_text` and `snapshot_json` contain no ESC byte, no C1 character and no `Cf` character.
- [T11.AC6] T48: an ID that the screen renderer truncates with `>` appears in full in `record_text`, and two different sessions (filter and toggle settings) over the same `CycleResult` give byte-identical `snapshot_json`.
- [T11.AC7] A test shows a `\n` inside an identifier still yields exactly one line per row in `record_text`.
- [T11.AC8] A test shows the atomic writer leaves either the old or the new file (never a partial one) when interrupted between the temporary write and the replace, creates the file with mode 0600, and that `state_dir()` honours `XDG_STATE_HOME`.
- [T11.AC9] A test shows a FAILED cycle exports `source.status` `ERROR` with the short code and the last good rows.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: e5713941b11dd572ae6240353e5a34f39861bfd0
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/export.py b/src/superclaude/cli/observe/export.py
new file mode 100644
index 000000000..d18e70542
--- /dev/null
+++ b/src/superclaude/cli/observe/export.py
@@ -0,0 +1,217 @@
+"""Exports: the plain-text record and the versioned JSON snapshot, both from one ``View`` (AD-11, AD-12).
+
+Both read only ``view.all_rows`` and the session-independent blocks, so an export is lossless
+whatever the filter, the historical toggle or the selection. Neither goes through the screen
+renderer or any console. This is the only module that turns the ``UNKNOWN`` sentinel into the
+snapshot string ``"UNKNOWN"``.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import tempfile
+from importlib import resources
+from pathlib import Path
+from typing import Any
+
+from jsonschema import Draft7Validator
+
+from superclaude.cli.observe.sanitize import sanitize
+from superclaude.cli.observe.view import ORDER_UNKNOWN_FLAG, UNKNOWN, RowView, View
+
+SCHEMA_VERSION = 1
+SCHEMA_PACKAGE = "superclaude.cli.observe"
+SCHEMA_FILE = "snapshot.schema.json"
+SNAPSHOT_NAME = "snapshot.json"
+UNKNOWN_TEXT = "UNKNOWN"  # the snapshot spelling of a missing value
+
+SCHEMA: dict = json.loads(
+    resources.files(SCHEMA_PACKAGE).joinpath(SCHEMA_FILE).read_text(encoding="utf-8")
+)
+Draft7Validator.check_schema(
+    SCHEMA
+)  # a broken schema fails at import, not in the field
+
+# snapshot key (dotted for nesting) -> attribute of the typed row
+_TEXT_FIELDS = (
+    ("dispatchId", "dispatch_id"),
+    ("taskId", "task_id"),
+    ("runId", "run_id"),
+    ("workerState", "worker_state"),
+    ("dispatchStatus", "dispatch_status"),
+    ("terminalState", "terminal_state"),
+    ("role", "role"),
+    ("provider", "provider_id"),
+    ("hostKind", "host_kind"),
+    ("hostId", "host_id"),
+    ("stage.worker", "stage_worker"),
+    ("stage.dispatch", "stage_dispatch"),
+    ("outcome", "outcome"),
+    ("liveness.verdict", "liveness_verdict"),
+    ("liveness.source", "liveness_source"),
+    ("liveness.observedAt", "liveness_observed_at"),
+    ("evidence.liveStatus", "evidence_live_status"),
+    ("evidence.lastObservedAt", "evidence_last_observed_at"),
+    ("nextAction", "next_action_kind"),
+)
+_ANY_FIELDS = (("evidence.durable", "evidence_durable"),)  # a JSON value as given
+_KEY_OF_ATTR = {attr: key for key, attr in (*_TEXT_FIELDS, *_ANY_FIELDS)}
+
+
+# -- plain-text record ---------------------------------------------------------------------------
+
+
+def _row_line(row: RowView) -> str:
+    fields = [
+        ("dispatchId", row.dispatch_id),
+        ("run", row.run),
+        ("workerState", row.worker_state),
+        ("dispatchStatus", row.dispatch_status),
+        ("terminalState", row.terminal_state),
+        ("outcome", row.outcome),
+        ("nextAction", row.next_action),
+        ("liveness", row.liveness),
+        ("evidenceAge", row.evidence_age),
+    ]
+    if row.flags:
+        fields.append(("flags", ", ".join(row.flags)))
+    line = " | ".join(f"{name}={value}" for name, value in fields)
+    return sanitize(line, "line")  # one line per row, whatever the identifier held
+
+
+def record_text(view: View) -> str:
+    """The ``e`` and ``--once`` record: full identifiers, no truncation, one line per row."""
+    filter_name = view.filter_text or "none"
+    historical = "shown" if view.show_historical else "hidden"
+    lines = [
+        view.header1,
+        view.header2,
+        "  ".join(token.text for token in view.counts_tokens),
+        f"screen filter: {filter_name}  historical rows on screen: {historical}  (this record lists every collected row)",
+        view.gap_notice,
+        view.ledger_title,
+    ]
+    lines.extend(view.ledger_empty)
+    lines.extend(_row_line(row) for row in view.all_rows)
+    return "\n".join(sanitize(line, "line") for line in lines) + "\n"
+
+
+# -- JSON snapshot -----------------------------------------------------------------------------------
+
+
+def _unknown(value: Any) -> Any:
+    return UNKNOWN_TEXT if value is UNKNOWN else value
+
+
+def _text(value: Any) -> Any:
+    if value is UNKNOWN:
+        return UNKNOWN_TEXT
+    return value if isinstance(value, str) else json.dumps(value)
+
+
+def _set(target: dict, dotted: str, value: Any) -> None:
+    *parents, leaf = dotted.split(".")
+    for key in parents:
+        target = target.setdefault(key, {})
+    target[leaf] = value
+
+
+def _row_dict(view_row: RowView) -> dict:
+    raw = view_row.raw
+    out: dict = {}
+    for key, attr in _TEXT_FIELDS:
+        _set(out, key, _text(getattr(raw, attr)))
+    for key, attr in _ANY_FIELDS:
+        _set(out, key, _unknown(getattr(raw, attr)))
+    if ORDER_UNKNOWN_FLAG in raw.flags:
+        out["orderUnknown"] = True
+    if not raw.reobserved:
+        out["notReobserved"] = True
+    absent = sorted(_KEY_OF_ATTR[a] for a in raw.absent_fields if a in _KEY_OF_ATTR)
+    if absent:
+        out["absentFields"] = absent
+    return out
+
+
+def snapshot_dict(view: View) -> dict:
+    meta = view.meta
+    source: dict = {
+        "namespace": meta.namespace or UNKNOWN_TEXT,
+        "status": meta.source_status,
+        "observedAt": _unknown(meta.source_observed_at),
+    }
+    if meta.source_error is not None:
+        source["error"] = meta.source_error
+    snapshot: dict = {
+        "schemaVersion": SCHEMA_VERSION,
+        "producer": {"name": meta.producer_name, "version": meta.producer_version},
+        "cycle": meta.cycle,
+        "generatedAt": meta.generated_at,
+        "source": source,
+        "page": {
+            "hasMore": _unknown(meta.has_more),
+            "total": _unknown(meta.total),
+            "limit": _unknown(meta.limit),
+        },
+        "scope": _unknown(meta.scope),
+        "counts": _unknown(meta.counts),
+        "rows": [_row_dict(row) for row in view.all_rows],
+    }
+    if meta.collection_state is not None:
+        snapshot["collection"] = {
+            "state": meta.collection_state,
+            "collected": meta.collection_collected,
+            "changedDuringRead": meta.collection_changed_during_read,
+            "duplicatesIgnored": meta.collection_duplicates_ignored,
+        }
+    return snapshot
+
+
+def snapshot_json(view: View) -> str:
+    """Snapshot v1: ``json.dumps(indent=2, sort_keys=True)``, every collected row, filter-independent."""
+    return json.dumps(snapshot_dict(view), indent=2, sort_keys=True)
+
+
+# -- files ---------------------------------------------------------------------------------------------
+
+
+def state_dir(env: dict | None = None, home: str | None = None) -> Path:
+    """``$XDG_STATE_HOME/superclaude/observe`` (when absolute), else ``~/.local/state/superclaude/observe``."""
+    env = os.environ if env is None else env
+    base = env.get("XDG_STATE_HOME", "")
+    if base and os.path.isabs(base):
+        root = Path(base)
+    else:
+        root = Path(home if home is not None else Path.home()) / ".local" / "state"
+    return root / "superclaude" / "observe"
+
+
+def record_path(directory: Path, view: View) -> Path:
+    """A timestamped record name built from the view's generation time."""
+    stamp = view.meta.generated_at.replace(":", "-")
+    return directory / f"observe-{stamp}.txt"
+
+
+def snapshot_path(directory: Path) -> Path:
+    return directory / SNAPSHOT_NAME
+
+
+def write_atomic(path: Path, text: str) -> Path:
+    """Write ``text`` to ``path`` mode 0600 via a temporary file in the same directory and ``os.replace``."""
+    path = Path(path)
+    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
+    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".observe-", suffix=".tmp")
+    try:
+        with os.fdopen(fd, "w", encoding="utf-8") as handle:
+            handle.write(text)
+            handle.flush()
+            os.fsync(handle.fileno())
+        os.replace(temp, path)
+    except BaseException:
+        try:
+            os.unlink(temp)
+        except FileNotFoundError:
+            pass
+        raise
+    return path
diff --git a/src/superclaude/cli/observe/snapshot.schema.json b/src/superclaude/cli/observe/snapshot.schema.json
new file mode 100644
index 000000000..ccf9b501b
--- /dev/null
+++ b/src/superclaude/cli/observe/snapshot.schema.json
@@ -0,0 +1,128 @@
+{
+  "$schema": "http://json-schema.org/draft-07/schema#",
+  "title": "superclaude observe snapshot, schema version 1 (PROPOSED, not an Orca contract)",
+  "description": "Additive-only: a new optional field may be added by a reviewed edit; removing, renaming or retyping a field needs schemaVersion 2. A value the source did not give is the string UNKNOWN. Consumers reject an unknown major schemaVersion and ignore unknown fields.",
+  "type": "object",
+  "additionalProperties": false,
+  "required": ["schemaVersion", "producer", "cycle", "generatedAt", "source", "page", "scope", "counts", "rows"],
+  "properties": {
+    "schemaVersion": {"const": 1},
+    "producer": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["name", "version"],
+      "properties": {
+        "name": {"type": "string"},
+        "version": {"type": "string"}
+      }
+    },
+    "cycle": {"type": "integer", "minimum": 0},
+    "generatedAt": {"$ref": "#/definitions/utcTime"},
+    "source": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["namespace", "status", "observedAt"],
+      "properties": {
+        "namespace": {"type": "string"},
+        "status": {"enum": ["OK", "STALE", "ERROR", "UNKNOWN"]},
+        "observedAt": {"anyOf": [{"$ref": "#/definitions/utcTime"}, {"const": "UNKNOWN"}]},
+        "error": {"type": "string"}
+      },
+      "if": {"properties": {"status": {"const": "ERROR"}}},
+      "then": {"required": ["error"]},
+      "else": {"not": {"required": ["error"]}}
+    },
+    "page": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["hasMore", "total", "limit"],
+      "properties": {
+        "hasMore": {"type": ["boolean", "string"], "enum": [true, false, "UNKNOWN"]},
+        "total": {"anyOf": [{"type": "integer", "minimum": 0}, {"const": "UNKNOWN"}]},
+        "limit": {"anyOf": [{"type": "integer", "minimum": 0}, {"const": "UNKNOWN"}]}
+      }
+    },
+    "scope": {"anyOf": [{"type": "object"}, {"const": "UNKNOWN"}]},
+    "counts": {
+      "anyOf": [
+        {
+          "type": "object",
+          "additionalProperties": {"type": ["integer", "number", "string", "boolean", "null"]}
+        },
+        {"const": "UNKNOWN"}
+      ]
+    },
+    "collection": {
+      "type": "object",
+      "additionalProperties": false,
+      "properties": {
+        "state": {"enum": ["COMPLETE", "PARTIAL", "MISMATCH"]},
+        "collected": {"type": "integer", "minimum": 0},
+        "changedDuringRead": {"type": "boolean"},
+        "duplicatesIgnored": {"type": "integer", "minimum": 0}
+      }
+    },
+    "rows": {"type": "array", "items": {"$ref": "#/definitions/row"}}
+  },
+  "definitions": {
+    "utcTime": {
+      "type": "string",
+      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
+    },
+    "text": {"type": "string"},
+    "row": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": [
+        "dispatchId", "taskId", "runId", "workerState", "dispatchStatus", "terminalState",
+        "role", "provider", "hostKind", "hostId", "stage", "outcome", "liveness", "evidence", "nextAction"
+      ],
+      "properties": {
+        "dispatchId": {"$ref": "#/definitions/text"},
+        "taskId": {"$ref": "#/definitions/text"},
+        "runId": {"$ref": "#/definitions/text"},
+        "workerState": {"$ref": "#/definitions/text"},
+        "dispatchStatus": {"$ref": "#/definitions/text"},
+        "terminalState": {"$ref": "#/definitions/text"},
+        "role": {"$ref": "#/definitions/text"},
+        "provider": {"$ref": "#/definitions/text"},
+        "hostKind": {"$ref": "#/definitions/text"},
+        "hostId": {"$ref": "#/definitions/text"},
+        "stage": {
+          "type": "object",
+          "additionalProperties": false,
+          "required": ["worker", "dispatch"],
+          "properties": {
+            "worker": {"$ref": "#/definitions/text"},
+            "dispatch": {"$ref": "#/definitions/text"}
+          }
+        },
+        "outcome": {"$ref": "#/definitions/text"},
+        "liveness": {
+          "type": "object",
+          "additionalProperties": false,
+          "required": ["verdict", "source", "observedAt"],
+          "properties": {
+            "verdict": {"$ref": "#/definitions/text"},
+            "source": {"$ref": "#/definitions/text"},
+            "observedAt": {"$ref": "#/definitions/text"}
+          }
+        },
+        "evidence": {
+          "type": "object",
+          "additionalProperties": false,
+          "required": ["durable", "liveStatus", "lastObservedAt"],
+          "properties": {
+            "durable": {},
+            "liveStatus": {"$ref": "#/definitions/text"},
+            "lastObservedAt": {"$ref": "#/definitions/text"}
+          }
+        },
+        "nextAction": {"$ref": "#/definitions/text"},
+        "orderUnknown": {"type": "boolean"},
+        "notReobserved": {"type": "boolean"},
+        "absentFields": {"type": "array", "items": {"type": "string"}, "uniqueItems": true}
+      }
+    }
+  }
+}
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index ce6324572..7d2b092b5 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -15,6 +15,9 @@ from typing import Any
 
 from superclaude import __version__
 from superclaude.cli.observe.parse import (  # noqa: F401  (UNKNOWN is re-exported)
+    ORDER_UNKNOWN as ORDER_UNKNOWN_FLAG,
+)
+from superclaude.cli.observe.parse import (
     UNKNOWN,
     Coverage,
     Row,
diff --git a/tests/observe/test_export.py b/tests/observe/test_export.py
new file mode 100644
index 000000000..15e922aae
--- /dev/null
+++ b/tests/observe/test_export.py
@@ -0,0 +1,243 @@
+"""Text record, atomic writer and state directory tests (AD-11; T27, T29 export half, T48)."""
+
+from __future__ import annotations
+
+import json
+import os
+import re
+import stat
+import unicodedata
+from pathlib import Path
+
+import pytest
+
+import superclaude.cli.observe.export as export_module
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.export import (
+    record_path,
+    record_text,
+    snapshot_json,
+    snapshot_path,
+    state_dir,
+    write_atomic,
+)
+from superclaude.cli.observe.render import screen_lines
+from superclaude.cli.observe.terminal import resolve_policy
+from superclaude.cli.observe.view import Session, build_view
+from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+
+
+def fixture_view(variant, clock, session=None, cycles=1):
+    collector = Collector(FixtureSource(variant), clock)
+    for _ in range(cycles):
+        result = collector.run_once()
+    return build_view(result, session or Session(), clock)
+
+
+def bad_chars(text):
+    return [
+        ch
+        for ch in text
+        if ch == "\x1b"
+        or (ch != "\n" and unicodedata.category(ch) in ("Cc", "Cf", "Cs"))
+    ]
+
+
+# -- T27 -----------------------------------------------------------------------------------------------------
+
+
+def test_record_has_full_identifiers_no_escape_and_no_truncation_marker(fake_clock):
+    view = fixture_view("long-identifiers", fake_clock, Session(show_historical=True))
+    text = record_text(view)
+    assert "\x1b" not in text and ">" not in text
+    for row in view.all_rows:
+        assert f"dispatchId={row.dispatch_id} |" in text
+        assert len(row.dispatch_id) >= 60
+    lines = [line for line in text.splitlines() if line.startswith("dispatchId=")]
+    assert len(lines) == 4 == len(view.all_rows)
+
+
+def test_record_first_line_is_the_header_and_names_the_synthetic_fixture(fake_clock):
+    text = record_text(fixture_view("base", fake_clock))
+    first, second = text.splitlines()[:2]
+    assert "SYNTHETIC FIXTURE base, not Orca data" in first and first.startswith(
+        "ORCA OBSERVER"
+    )
+    assert second.startswith("worker-list OK")
+    assert text.endswith("\n") and "Human questions: source UNVERIFIED" in text
+
+
+def test_record_header_names_the_filter_and_toggle_but_lists_every_row(fake_clock):
+    plain = record_text(fixture_view("base", fake_clock))
+    session = Session(filter_text="run-a", show_historical=True)
+    narrowed = record_text(fixture_view("base", fake_clock, session))
+    assert "screen filter: none  historical rows on screen: hidden" in plain
+    assert "screen filter: run-a  historical rows on screen: shown" in narrowed
+
+    def rows(text):
+        return [line for line in text.splitlines() if line.startswith("dispatchId=")]
+
+    assert rows(plain) == rows(narrowed) and len(rows(plain)) == 80
+
+
+def test_a_newline_inside_an_identifier_still_gives_one_line_per_row(
+    fake_clock, argv_log
+):
+    rows = make_rows(3, 1)
+    rows[1]["dispatchId"] = "w-002\nsecond line\r\nthird"
+    runner = FakeRunner(argv_log, [(0, json.dumps(make_envelope(rows, total=3)))])
+    result = Collector(
+        LiveSource(runner, FakeDiscover(argv_log)), fake_clock
+    ).run_once()
+    text = record_text(build_view(result, Session(), fake_clock))
+    assert (
+        len([line for line in text.splitlines() if line.startswith("dispatchId=")]) == 3
+    )
+    assert "dispatchId=w-002 second line third" in text
+
+
+def test_empty_and_not_polled_records_say_so_without_inventing_rows(fake_clock):
+    empty = record_text(fixture_view("empty", fake_clock))
+    assert "no observed items in this source window; not proof none exist" in empty
+    assert not any(line.startswith("dispatchId=") for line in empty.splitlines())
+    never = record_text(
+        build_view(
+            Collector(FixtureSource("base"), fake_clock).latest(), Session(), fake_clock
+        )
+    )
+    assert "no successful worker-list read yet" in never and "as of never" in never
+
+
+# -- T29 export half -----------------------------------------------------------------------------------------
+
+
+def test_injection_variant_exports_contain_no_escape_c1_or_format_characters(
+    fake_clock,
+):
+    for session in (Session(), Session(show_historical=True, filter_text="w-inj")):
+        view = fixture_view("injection", fake_clock, session)
+        assert bad_chars(record_text(view)) == []
+        assert bad_chars(snapshot_json(view)) == []
+    assert "[bold]x[/bold]" in record_text(
+        fixture_view("injection", fake_clock, Session(show_historical=True))
+    )
+
+
+# -- T48 --------------------------------------------------------------------------------------------------------
+
+
+def test_an_id_truncated_on_screen_appears_in_full_in_the_record(fake_clock):
+    view = fixture_view("long-identifiers", fake_clock, Session(show_historical=True))
+    policy = resolve_policy({}, "utf-8", {}, 80, 40)
+    screen = "\n".join(screen_lines(view, policy))
+    record = record_text(view)
+    truncated = [row for row in view.all_rows if row.dispatch_id not in screen]
+    assert truncated and all(">" in screen for _ in truncated)
+    for row in truncated:
+        assert row.dispatch_id in record
+
+
+def test_two_sessions_over_one_cycle_result_give_byte_identical_snapshots(fake_clock):
+    collector = Collector(FixtureSource("base"), fake_clock)
+    result = collector.run_once()
+    sessions = [
+        Session(),
+        Session(filter_text="run-b", show_historical=True),
+        Session(show_historical=False, focus="inspector"),
+    ]
+    outputs = {snapshot_json(build_view(result, s, fake_clock)) for s in sessions}
+    assert len(outputs) == 1
+    assert len(json.loads(outputs.pop())["rows"]) == 80  # historical rows are in it too
+
+
+# -- files ------------------------------------------------------------------------------------------------------
+
+
+def test_atomic_writer_creates_a_0600_file_and_replaces_atomically(tmp_path):
+    target = tmp_path / "state" / "out.json"
+    write_atomic(target, "first")
+    assert (
+        target.read_text() == "first" and stat.S_IMODE(target.stat().st_mode) == 0o600
+    )
+    target.chmod(0o644)
+    write_atomic(target, "second")
+    assert (
+        target.read_text() == "second" and stat.S_IMODE(target.stat().st_mode) == 0o600
+    )
+    assert [p.name for p in target.parent.iterdir()] == [
+        "out.json"
+    ]  # no temporary file left
+
+
+def test_an_interrupted_write_leaves_the_old_file_whole_and_no_temporary_file(
+    tmp_path, monkeypatch
+):
+    target = tmp_path / "snapshot.json"
+    write_atomic(target, "old content")
+
+    def boom(src, dst):
+        raise OSError("interrupted between the temporary write and the replace")
+
+    monkeypatch.setattr(os, "replace", boom)
+    with pytest.raises(OSError):
+        write_atomic(target, "new content that must never be seen half written")
+    assert target.read_text() == "old content"
+    assert [p.name for p in tmp_path.iterdir()] == ["snapshot.json"]
+    fresh = tmp_path / "never-written.json"
+    with pytest.raises(OSError):
+        write_atomic(fresh, "x")
+    assert not fresh.exists()
+
+
+def test_state_dir_honours_xdg_state_home_and_falls_back_to_the_home_folder(tmp_path):
+    assert (
+        state_dir({"XDG_STATE_HOME": str(tmp_path)})
+        == tmp_path / "superclaude" / "observe"
+    )
+    assert (
+        state_dir({}, home=str(tmp_path))
+        == tmp_path / ".local" / "state" / "superclaude" / "observe"
+    )
+    assert "relative" not in str(
+        state_dir({"XDG_STATE_HOME": "relative/path"}, home=str(tmp_path))
+    )
+    assert state_dir({"XDG_STATE_HOME": ""}, home=str(tmp_path)).parts[-3:] == (
+        "state",
+        "superclaude",
+        "observe",
+    )
+
+
+def test_record_and_snapshot_names(fake_clock, tmp_path):
+    view = fixture_view("base", fake_clock)
+    assert record_path(tmp_path, view) == tmp_path / "observe-2026-11-08T12-00-00Z.txt"
+    assert snapshot_path(tmp_path) == tmp_path / "snapshot.json"
+
+
+def test_a_failed_cycle_exports_error_with_the_short_code_and_the_last_good_rows(
+    fake_clock,
+):
+    collector = Collector(FixtureSource("source-loss"), fake_clock)
+    for _ in range(3):
+        failed = collector.run_once()
+    data = json.loads(snapshot_json(build_view(failed, Session(), fake_clock)))
+    assert data["source"]["status"] == "ERROR" and data["source"]["error"] == "timeout"
+    assert (
+        len(data["rows"]) == 5
+        and data["source"]["observedAt"] == "2026-11-08T12:00:00Z"
+    )
+    assert "worker-list FAILED (timeout)" in record_text(
+        build_view(failed, Session(), fake_clock)
+    )
+
+
+# -- hygiene ------------------------------------------------------------------------------------------------------
+
+
+def test_export_does_not_import_render_parse_or_adapter_or_use_a_console():
+    text = Path(export_module.__file__).read_text(encoding="utf-8")
+    assert not re.search(
+        r"observe\.(render|parse|adapter|collector)\b|Console\b|from rich|import rich",
+        text,
+    )
diff --git a/tests/observe/test_snapshot_schema.py b/tests/observe/test_snapshot_schema.py
new file mode 100644
index 000000000..ae4d8be24
--- /dev/null
+++ b/tests/observe/test_snapshot_schema.py
@@ -0,0 +1,410 @@
+"""Snapshot v1 schema test (CAP-10, recorded owner decision 2; no ID assigned in acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import copy
+import json
+import re
+from importlib import resources
+
+import pytest
+from jsonschema import Draft7Validator
+
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.export import SCHEMA, snapshot_json
+from superclaude.cli.observe.parse import VARIANTS, load_fixture
+from superclaude.cli.observe.view import Session, build_view
+from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+
+VALIDATOR = Draft7Validator(SCHEMA)
+
+
+def every_snapshot(variant, clock):
+    """The snapshot after each replayed cycle of a fixture variant."""
+    collector = Collector(FixtureSource(variant), clock)
+    for _ in range(len(load_fixture(variant).cycles)):
+        yield json.loads(
+            snapshot_json(build_view(collector.run_once(), Session(), clock))
+        )
+
+
+def live_snapshot(rows, clock, **kw):
+    runner = FakeRunner([], [(0, json.dumps(make_envelope(rows, total=len(rows))))])
+    result = Collector(LiveSource(runner, FakeDiscover([])), clock).run_once()
+    return json.loads(snapshot_json(build_view(result, Session(), clock)))
+
+
+def walk(value, path=()):
+    """Every (path, key) and (path, scalar) in a JSON document."""
+    if isinstance(value, dict):
+        for key, inner in value.items():
+            yield path, key
+            yield from walk(inner, (*path, key))
+    elif isinstance(value, list):
+        for inner in value:
+            yield from walk(inner, path)
+    else:
+        yield path, value
+
+
+# -- the schema file ---------------------------------------------------------------------------------------------
+
+
+def test_the_schema_ships_in_the_package_is_draft_7_and_closed_on_the_producer_side():
+    text = (
+        resources.files("superclaude.cli.observe")
+        .joinpath("snapshot.schema.json")
+        .read_text(encoding="utf-8")
+    )
+    assert json.loads(text) == SCHEMA
+    Draft7Validator.check_schema(SCHEMA)
+    assert SCHEMA["$schema"].endswith("draft-07/schema#")
+    closed = [
+        SCHEMA,
+        SCHEMA["properties"]["producer"],
+        SCHEMA["properties"]["source"],
+        SCHEMA["properties"]["page"],
+        SCHEMA["properties"]["collection"],
+        SCHEMA["definitions"]["row"],
+        SCHEMA["definitions"]["row"]["properties"]["stage"],
+        SCHEMA["definitions"]["row"]["properties"]["liveness"],
+        SCHEMA["definitions"]["row"]["properties"]["evidence"],
+    ]
+    assert all(node["additionalProperties"] is False for node in closed)
+
+
+# -- every variant validates -----------------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("variant", VARIANTS)
+def test_every_fixture_variant_snapshot_validates_after_every_cycle(
+    fake_clock, variant
+):
+    count = 0
+    for snapshot in every_snapshot(variant, fake_clock):
+        assert list(VALIDATOR.iter_errors(snapshot)) == []
+        assert (
+            snapshot["schemaVersion"] == 1
+            and snapshot["producer"]["name"] == "superclaude-observe"
+        )
+        count += 1
+    assert count == len(load_fixture(variant).cycles)
+
+
+def test_not_polled_and_not_available_snapshots_validate_with_unknown_status(
+    fake_clock,
+):
+    never = Collector(FixtureSource("base"), fake_clock).latest()
+    data = json.loads(snapshot_json(build_view(never, Session(), fake_clock)))
+    assert list(VALIDATOR.iter_errors(data)) == []
+    assert data["source"] == {
+        "namespace": "UNKNOWN",
+        "status": "UNKNOWN",
+        "observedAt": "UNKNOWN",
+    }
+    assert data["page"] == {
+        "hasMore": "UNKNOWN",
+        "total": "UNKNOWN",
+        "limit": "UNKNOWN",
+    }
+    assert (data["scope"], data["counts"], data["rows"]) == (
+        "UNKNOWN",
+        "UNKNOWN",
+        [],
+    ) and "collection" not in data
+    unavailable = Collector(
+        LiveSource(FakeRunner([]), FakeDiscover([], None)), fake_clock
+    ).run_once()
+    data = json.loads(snapshot_json(build_view(unavailable, Session(), fake_clock)))
+    assert (
+        list(VALIDATOR.iter_errors(data)) == []
+        and data["source"]["status"] == "UNKNOWN"
+    )
+
+
+def test_status_error_stale_and_ok_map_from_the_source_state(fake_clock):
+    collector = Collector(FixtureSource("source-loss"), fake_clock)
+    results = [collector.run_once() for _ in range(3)]
+    ok = json.loads(snapshot_json(build_view(results[0], Session(), fake_clock)))
+    assert ok["source"]["status"] == "OK" and "error" not in ok["source"]
+    fake_clock.advance(50)
+    stale = json.loads(snapshot_json(build_view(results[1], Session(), fake_clock)))
+    assert stale["source"]["status"] == "STALE" and "error" not in stale["source"]
+    failed = json.loads(snapshot_json(build_view(results[2], Session(), fake_clock)))
+    assert (
+        failed["source"]["status"] == "ERROR" and failed["source"]["error"] == "timeout"
+    )
+    for data in (ok, stale, failed):
+        assert list(VALIDATOR.iter_errors(data)) == []
+
+
+# -- the schema rejects what it must --------------------------------------------------------------------------------------
+
+
+def test_schema_version_two_and_unknown_fields_are_rejected(fake_clock):
+    data = next(every_snapshot("base", fake_clock))
+    assert list(VALIDATOR.iter_errors(data)) == []
+    wrong = copy.deepcopy(data)
+    wrong["schemaVersion"] = 2
+    assert list(VALIDATOR.iter_errors(wrong))
+    for where in (
+        lambda d: d.update(extra=1),
+        lambda d: d["producer"].update(extra=1),
+        lambda d: d["source"].update(extra=1),
+        lambda d: d["page"].update(extra=1),
+        lambda d: d["collection"].update(extra=1),
+        lambda d: d["rows"][0].update(extra=1),
+        lambda d: d["rows"][0]["stage"].update(detail="x"),
+        lambda d: d["rows"][0]["liveness"].update(extra=1),
+        lambda d: d["rows"][0]["evidence"].update(extra=1),
+    ):
+        mutated = copy.deepcopy(data)
+        where(mutated)
+        assert list(VALIDATOR.iter_errors(mutated)), where
+
+
+def test_schema_rejects_wrong_types_missing_required_keys_and_misplaced_error(
+    fake_clock,
+):
+    data = next(every_snapshot("base", fake_clock))
+    mutations = [
+        lambda d: d.pop("rows"),
+        lambda d: d.update(cycle="1"),
+        lambda d: d.update(generatedAt="yesterday"),
+        lambda d: d["source"].update(status="BROKEN"),
+        lambda d: d["source"].update(error="timeout"),  # error only with status ERROR
+        lambda d: d["rows"][0].pop("nextAction"),
+        lambda d: d["rows"][0].update(dispatchId=None),
+        lambda d: d["rows"][0].update(absentFields=["a", "a"]),
+        lambda d: d["page"].update(total=-1),
+        lambda d: d["page"].update(hasMore="false"),
+        lambda d: d["collection"].update(state="DONE"),
+        lambda d: d.update(scope=None),
+    ]
+    for mutate in mutations:
+        mutated = copy.deepcopy(data)
+        mutate(mutated)
+        assert list(VALIDATOR.iter_errors(mutated)), mutate
+    failed = copy.deepcopy(data)
+    failed["source"]["status"] = "ERROR"
+    assert list(VALIDATOR.iter_errors(failed))  # ERROR needs the short code
+
+
+# -- UNKNOWN versus a source value that is the text UNKNOWN -------------------------------------------------------------------
+
+
+def test_missing_values_are_the_string_unknown_and_absent_fields_separate_them_from_source_text(
+    fake_clock,
+):
+    rows = make_rows(2, 1)
+    rows[0]["taskId"] = "UNKNOWN"  # a source value that is itself the text
+    del rows[1]["taskId"]
+    rows[1]["projection"]["nextAction"] = None
+    del rows[1]["projection"]["liveness"]["observedAt"]
+    data = live_snapshot(rows, fake_clock)
+    assert list(VALIDATOR.iter_errors(data)) == []
+    by_id = {row["dispatchId"]: row for row in data["rows"]}
+    typed, absent = by_id["w-001"], by_id["w-002"]
+    assert typed["taskId"] == "UNKNOWN" and "taskId" not in typed.get(
+        "absentFields", []
+    )
+    assert absent["taskId"] == "UNKNOWN" and "taskId" in absent["absentFields"]
+    assert absent["nextAction"] == "UNKNOWN" and "nextAction" in absent["absentFields"]
+    assert (
+        absent["liveness"]["observedAt"] == "UNKNOWN"
+        and "liveness.observedAt" in absent["absentFields"]
+    )
+    assert absent["absentFields"] == sorted(absent["absentFields"])
+    # no stand-in for a missing value: JSON null, 0, false and "" never appear for it
+    for scalar in (
+        absent["taskId"],
+        absent["nextAction"],
+        absent["liveness"]["observedAt"],
+    ):
+        assert (
+            scalar == "UNKNOWN"
+            and scalar is not None
+            and scalar != ""
+            and scalar is not False
+        )
+
+
+def test_the_missing_fields_variant_has_unknown_everywhere_the_source_was_silent(
+    fake_clock,
+):
+    data = next(every_snapshot("missing-fields", fake_clock))
+    assert (
+        data["page"]["total"] == "UNKNOWN"
+        and data["scope"] == "UNKNOWN"
+        and data["counts"] == "UNKNOWN"
+    )
+    for row in data["rows"]:
+        for _, scalar in walk(row):
+            assert scalar is not None
+    first = next(r for r in data["rows"] if r["dispatchId"] == "w-001")
+    assert first["liveness"] == {
+        "verdict": "UNKNOWN",
+        "source": "UNKNOWN",
+        "observedAt": "UNKNOWN",
+    }
+    assert {
+        "liveness.verdict",
+        "liveness.source",
+        "liveness.observedAt",
+        "nextAction",
+    } <= set(first["absentFields"])
+    anonymous = next(r for r in data["rows"] if r["dispatchId"] == "UNKNOWN")
+    assert "dispatchId" in anonymous["absentFields"]
+
+
+# -- nothing sensitive leaves the observer ---------------------------------------------------------------------------------------
+
+FORBIDDEN_KEYS = {
+    "detail",
+    "activity",
+    "terminalHandle",
+    "agentTerminalHandle",
+    "worktreeId",
+    "endpointId",
+    "ownershipState",
+    "releaseState",
+    "warnings",
+    "nextCursor",
+    "body",
+    "prompt",
+    "content",
+    "credentials",
+    "token",
+    "password",
+    "secret",
+    "message",
+    "messages",
+}
+FORBIDDEN_WORDS = (
+    "prompt",
+    "credential",
+    "password",
+    "secret",
+    "token",
+    "worktree",
+    "terminal handle",
+    "stage.detail",
+    "stage.activity",
+)
+
+
+@pytest.mark.parametrize("variant", VARIANTS)
+def test_snapshots_carry_no_forbidden_keys_words_or_fixture_input_values(
+    fake_clock, variant
+):
+    fixture = load_fixture(variant)
+    withheld: set[str] = set()
+    for cycle in fixture.cycles:
+        for worker in (cycle.envelope or {}).get("result", {}).get("workers", []):
+            if not isinstance(worker, dict):
+                continue
+            stage = worker.get("projection", {}).get("stage", {})
+            resource = worker.get("resource", {})
+            withheld |= {
+                v
+                for v in (
+                    stage.get("detail"),
+                    stage.get("activity"),
+                    resource.get("worktreeId"),
+                    worker.get("agentTerminalHandle"),
+                    resource.get("terminalHandle"),
+                )
+                if isinstance(v, str) and len(v) > 3
+            }
+    for snapshot in every_snapshot(variant, fake_clock):
+        text = json.dumps(snapshot)
+        key_names = {key for _, key in _only_keys(snapshot)}
+        assert key_names.isdisjoint(FORBIDDEN_KEYS), key_names & FORBIDDEN_KEYS
+        lowered = text.lower()
+        assert not any(word in lowered for word in FORBIDDEN_WORDS)
+        for value in withheld:
+            assert value not in text, value
+
+
+def _only_keys(value, path=()):
+    if isinstance(value, dict):
+        for key, inner in value.items():
+            yield path, key
+            yield from _only_keys(inner, (*path, key))
+    elif isinstance(value, list):
+        for inner in value:
+            yield from _only_keys(inner, path)
+
+
+# -- ordering and optional groups ----------------------------------------------------------------------------------------------------
+
+
+def test_rows_are_newest_first_with_untimed_rows_last_and_ties_by_dispatch_id(
+    fake_clock,
+):
+    rows = make_rows(5, 1)
+    stamp = "2026-11-08T11:00:00Z"
+    for row in rows:
+        row["projection"]["liveness"]["observedAt"] = stamp
+    rows[0]["projection"]["liveness"]["observedAt"] = "2026-11-08T11:30:00Z"  # newest
+    rows[1]["dispatchId"] = (
+        "w-000"  # ties with w-003..w-005 on the timestamp, sorts first by id
+    )
+    del rows[2]["projection"]["liveness"]["observedAt"]
+    del rows[2]["projection"]["evidence"][
+        "lastObservedAt"
+    ]  # untimed: after every timed row
+    data = live_snapshot(rows, fake_clock)
+    assert [r["dispatchId"] for r in data["rows"]] == [
+        "w-001",
+        "w-000",
+        "w-004",
+        "w-005",
+        "w-003",
+    ]
+
+
+def test_historical_rows_are_in_the_snapshot_and_collection_fields_are_filled(
+    fake_clock,
+):
+    data = next(every_snapshot("historical", fake_clock))
+    assert len(data["rows"]) == 9
+    assert {r["terminalState"] for r in data["rows"]} >= {
+        "released",
+        "retained",
+        "orphaned",
+        "UNKNOWN",
+    }
+    assert data["collection"] == {
+        "state": "COMPLETE",
+        "collected": 9,
+        "changedDuringRead": False,
+        "duplicatesIgnored": 0,
+    }
+    dup = list(every_snapshot("duplicate-out-of-order", fake_clock))
+    assert dup[0]["collection"]["duplicatesIgnored"] == 1
+    assert [r["dispatchId"] for r in dup[1]["rows"] if r.get("orderUnknown")] == [
+        "w-003"
+    ]
+
+
+def test_not_reobserved_rows_carry_the_flag_and_output_is_indented_and_sorted(
+    fake_clock,
+):
+    rows = make_rows(3, 1)
+    runner = FakeRunner(
+        [],
+        [
+            (0, json.dumps(make_envelope(rows, total=3))),
+            (0, json.dumps(make_envelope(rows[:2], total=2))),
+        ],
+    )
+    collector = Collector(LiveSource(runner, FakeDiscover([])), fake_clock)
+    collector.run_once()
+    text = snapshot_json(build_view(collector.run_once(), Session(), fake_clock))
+    data = json.loads(text)
+    flagged = [r["dispatchId"] for r in data["rows"] if r.get("notReobserved")]
+    assert flagged == ["w-003"]
+    assert text == json.dumps(data, indent=2, sort_keys=True)
+    assert re.match(r'^\{\n  "collection"', text)

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
