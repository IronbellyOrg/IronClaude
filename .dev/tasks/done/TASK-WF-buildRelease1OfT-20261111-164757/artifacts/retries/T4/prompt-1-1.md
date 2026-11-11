68d2012121c0ecb598842d1a6d5c19417f18d51e
Review one task for spec compliance.

Task brief: 
## Task 4: Build the parser and merge `parse.py`

Depends on: Task 2

Create `src/superclaude/cli/observe/parse.py` and `tests/observe/test_parse.py`, following `ARCHITECTURE-SPINE.md` AD-7 and AD-19 and the "Parsing" and "Identity, duplicates, order" sections of `adapter-contract.md`. Define the `UNKNOWN` sentinel (one object, not `None`, `0`, `False` or `""`), frozen dataclasses `Row` (which also has a `fixture_frozen` boolean, default False, set only by the fixture loader in Task 5 and never by `parse_page`), `Snapshot` and `Coverage`, `parse_page(obj, namespace, cycle, source_rank_base)` and the pure `merge(previous, pages, stopped_by_cap, stopped_by_error, clock)`. Strict envelope: `result` must be an object, `result.workers` a list, `result.page.hasMore` a bool (the string `"false"` fails, JSON null counts as absent), otherwise a shape error and the previous `Snapshot` stays. Optional: `result.scope`, `result.page.total` (a non-negative integer, else `UNKNOWN`), `result.counts` (passed through, never summed) and `result.warnings` (sanitized). Rows are read field by field with absent-tolerant access over the keys listed in `adapter-contract.md` section 3 and `rendering-rules.md` inspector list: `dispatchId`, `taskId`, `runId`, `workerState`, `dispatchStatus`, `terminalState`, `resource.{id, ownershipState, releaseState, worktreeId, ownerDispatchId, originDispatchId, recoveryAttemptCount}`, `projection.{outcome, role, provider.id, host.id, host.kind, workspace.id, workspace.kind, stage.worker, stage.dispatch, stage.activity, stage.detail, nextAction.kind, liveness.verdict, liveness.source, liveness.observedAt, evidence.durable, evidence.liveStatus, evidence.lastObservedAt}`; a missing key or JSON null becomes `UNKNOWN`; every string passes `sanitize` (block mode only for `stage.detail` and `stage.activity`); unexpected keys are counted per row. A non-object row is counted as malformed and skipped. Row identity is `(namespace, dispatchId)`; a row whose `dispatchId` is absent, JSON null, empty or whitespace-only (the `UNKNOWN` sentinel) gets the per-cycle identity `(namespace, UNKNOWN, cycle, source_rank)`, carries the flag `identity unknown`, is never deduplicated or matched across cycles, is not counted as a duplicate and is counted separately (`adapter-contract.md` section "Identity, duplicates, order"); the next cycle that is not PARTIAL replaces the previous cycle's such rows, while a PARTIAL cycle keeps them (`ARCHITECTURE-SPINE.md` AD-7). `merge` keeps a row set across pages and cycles: duplicates within a cycle are dropped and counted; the newer `liveness.observedAt` (compared only with the same field from the other copy, likewise `evidence.lastObservedAt`) wins; an absent or unparsable timestamp, or no common timestamp field, makes the newer cycle win and sets the `order unknown` flag; a backward timestamp sets `conflict (time went back)`; equal timestamps let the newer cycle win; a previous row with a real identity that is not returned this cycle stays with `reobserved=False` and its last-seen cycle; `Coverage` records the per-page totals, any empty-page index, `has_more_at_stop`, the duplicate count and whether `total` changed during the read.

Acceptance criteria:
- [T4.AC1] `uv run pytest tests/observe/test_parse.py -v` passes.
- [T4.AC2] T32 (parse half): removing `result`, `result.workers` or `result.page.hasMore`, or giving `workers` a non-list or `hasMore` the string `"false"` or null, yields a shape error and keeps the previous snapshot; removing `result.scope` or `page.total` yields `UNKNOWN` for that field only; removing an inner `projection.*` key yields `UNKNOWN` in that row, not an error.
- [T4.AC3] T22 and T39: an older `observedAt` never overwrites a newer one; a row with both timestamps missing is flagged `order unknown`; a backward timestamp is flagged `conflict (time went back)`; the duplicate count is exact; the same `dispatchId` under two different namespaces stays two rows.
- [T4.AC4] A test shows a row with no `dispatchId` keeps a per-cycle identity, is never merged with another such row and is not counted as a duplicate; the same holds for an empty and a whitespace-only `dispatchId`, each such row carries `identity unknown`, and two of them in one cycle stay two rows.
- [T4.AC5] A test shows a JSON null and an absent key both give `UNKNOWN`, and that `UNKNOWN`, `None`, `0`, `False` and `""` are five distinct values.
- [T4.AC6] A test shows a row seen in cycle 1 and absent in cycle 2 stays with `reobserved=False`.
- [T4.AC7] A test shows anonymous rows from cycle 1 are replaced by cycle 2's anonymous rows when cycle 2 is not PARTIAL and are kept when it is PARTIAL, and that rows with a real identity are unaffected either way.
- [T4.AC8] A test shows extra unknown keys are counted and their names and values do not appear in the parsed row text.

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

Start sha: 68d2012121c0ecb598842d1a6d5c19417f18d51e
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/parse.py b/src/superclaude/cli/observe/parse.py
new file mode 100644
index 000000000..9381a458d
--- /dev/null
+++ b/src/superclaude/cli/observe/parse.py
@@ -0,0 +1,535 @@
+"""Parsing and merging of ``worker-list`` pages (AD-7, AD-19).
+
+``parse_page`` is strict on the envelope and lenient inside rows. ``merge`` is the one
+pure function that owns the row set across pages and cycles. Only verified worker-list
+keys are read; any other key is counted and dropped (its name and value are never kept).
+"""
+
+from __future__ import annotations
+
+import json
+import math
+from collections.abc import Sequence
+from dataclasses import dataclass, replace
+from datetime import datetime, timezone
+from typing import Any
+
+from superclaude.cli.observe.sanitize import sanitize
+
+# -- the UNKNOWN sentinel -------------------------------------------------------
+
+
+class _Unknown:
+    """The single "the source did not give this" value (never None, 0, False or "")."""
+
+    __slots__ = ()
+
+    def __repr__(self) -> str:
+        return "UNKNOWN"
+
+    def __copy__(self) -> _Unknown:
+        return self
+
+    def __deepcopy__(self, memo: object) -> _Unknown:
+        return self
+
+    def __reduce__(self) -> str:
+        return "UNKNOWN"
+
+
+UNKNOWN: Any = _Unknown()
+
+IDENTITY_UNKNOWN = "identity unknown"
+ORDER_UNKNOWN = "order unknown"
+CONFLICT_BACKWARD = "conflict (time went back)"
+_ORDER_FLAGS = (ORDER_UNKNOWN, CONFLICT_BACKWARD)
+
+
+class ShapeError(ValueError):
+    """The envelope is not a worker-list reply (cycle is ``FAILED (shape)``)."""
+
+
+# -- the verified worker-list keys ------------------------------------------------
+
+# attribute name -> key path inside one worker row
+_FIELDS: tuple[tuple[str, tuple[str, ...]], ...] = (
+    ("dispatch_id", ("dispatchId",)),
+    ("task_id", ("taskId",)),
+    ("run_id", ("runId",)),
+    ("worker_state", ("workerState",)),
+    ("dispatch_status", ("dispatchStatus",)),
+    ("terminal_state", ("terminalState",)),
+    ("resource_id", ("resource", "id")),
+    ("ownership_state", ("resource", "ownershipState")),
+    ("release_state", ("resource", "releaseState")),
+    ("worktree_id", ("resource", "worktreeId")),
+    ("owner_dispatch_id", ("resource", "ownerDispatchId")),
+    ("origin_dispatch_id", ("resource", "originDispatchId")),
+    ("recovery_attempt_count", ("resource", "recoveryAttemptCount")),
+    ("outcome", ("projection", "outcome")),
+    ("role", ("projection", "role")),
+    ("provider_id", ("projection", "provider", "id")),
+    ("host_id", ("projection", "host", "id")),
+    ("host_kind", ("projection", "host", "kind")),
+    ("workspace_id", ("projection", "workspace", "id")),
+    ("workspace_kind", ("projection", "workspace", "kind")),
+    ("stage_worker", ("projection", "stage", "worker")),
+    ("stage_dispatch", ("projection", "stage", "dispatch")),
+    ("stage_activity", ("projection", "stage", "activity")),
+    ("stage_detail", ("projection", "stage", "detail")),
+    ("next_action_kind", ("projection", "nextAction", "kind")),
+    ("liveness_verdict", ("projection", "liveness", "verdict")),
+    ("liveness_source", ("projection", "liveness", "source")),
+    ("liveness_observed_at", ("projection", "liveness", "observedAt")),
+    ("evidence_durable", ("projection", "evidence", "durable")),
+    ("evidence_live_status", ("projection", "evidence", "liveStatus")),
+    ("evidence_last_observed_at", ("projection", "evidence", "lastObservedAt")),
+)
+_BLOCK_FIELDS = frozenset(
+    {"stage_detail", "stage_activity"}
+)  # the only block-mode text
+
+
+def _known_tree() -> dict[str, Any]:
+    tree: dict[str, Any] = {}
+    for _, path in _FIELDS:
+        node = tree
+        for key in path[:-1]:
+            node = node.setdefault(key, {})
+        node[path[-1]] = None  # leaf
+    return tree
+
+
+_KNOWN = _known_tree()
+
+
+@dataclass(frozen=True)
+class Row:
+    """One worker, every value a source value or ``UNKNOWN`` (strings already sanitized)."""
+
+    namespace: str
+    identity: tuple
+    cycle: int  # the cycle whose data this copy holds
+    last_seen_cycle: int  # the latest cycle that returned this row
+    source_rank: int  # position in the cycle's newest-first pages
+    dispatch_id: Any = UNKNOWN
+    task_id: Any = UNKNOWN
+    run_id: Any = UNKNOWN
+    worker_state: Any = UNKNOWN
+    dispatch_status: Any = UNKNOWN
+    terminal_state: Any = UNKNOWN
+    resource_id: Any = UNKNOWN
+    ownership_state: Any = UNKNOWN
+    release_state: Any = UNKNOWN
+    worktree_id: Any = UNKNOWN
+    owner_dispatch_id: Any = UNKNOWN
+    origin_dispatch_id: Any = UNKNOWN
+    recovery_attempt_count: Any = UNKNOWN
+    outcome: Any = UNKNOWN
+    role: Any = UNKNOWN
+    provider_id: Any = UNKNOWN
+    host_id: Any = UNKNOWN
+    host_kind: Any = UNKNOWN
+    workspace_id: Any = UNKNOWN
+    workspace_kind: Any = UNKNOWN
+    stage_worker: Any = UNKNOWN
+    stage_dispatch: Any = UNKNOWN
+    stage_activity: Any = UNKNOWN
+    stage_detail: Any = UNKNOWN
+    next_action_kind: Any = UNKNOWN
+    liveness_verdict: Any = UNKNOWN
+    liveness_source: Any = UNKNOWN
+    liveness_observed_at: Any = UNKNOWN
+    evidence_durable: Any = UNKNOWN
+    evidence_live_status: Any = UNKNOWN
+    evidence_last_observed_at: Any = UNKNOWN
+    absent_fields: tuple[
+        str, ...
+    ] = ()  # attributes that are UNKNOWN because the source omitted them
+    flags: tuple[
+        str, ...
+    ] = ()  # "identity unknown", "order unknown", "conflict (time went back)"
+    unrecognised_keys: int = 0
+    reobserved: bool = True
+    fixture_frozen: bool = False  # set only by the fixture loader, never by parse_page
+
+    @property
+    def identity_unknown(self) -> bool:
+        return IDENTITY_UNKNOWN in self.flags
+
+
+@dataclass(frozen=True)
+class ParsedPage:
+    rows: tuple[Row, ...]
+    raw_count: int  # entries in result.workers, malformed ones included
+    cycle: int
+    namespace: str
+    has_more: bool
+    total: Any = UNKNOWN  # int or UNKNOWN
+    limit: Any = UNKNOWN  # int or UNKNOWN
+    scope: Any = UNKNOWN  # sanitized object or UNKNOWN
+    counts: Any = UNKNOWN  # sanitized object, passed through, never summed
+    warnings: tuple[str, ...] = ()
+    malformed_rows: int = 0
+    unrecognised_keys: int = 0
+
+
+@dataclass(frozen=True)
+class Coverage:
+    page_totals: tuple = ()  # result.page.total of each page read (int or UNKNOWN)
+    pages_read: int = 0
+    empty_page: int | None = (
+        None  # 1-based index of a page with no workers while its total is above 0
+    )
+    has_more_at_stop: bool = False
+    duplicates: int = 0
+    total_changed: bool = False  # page.total differed between pages
+    stopped_by_cap: bool = False
+    stopped_by_error: str | None = None
+    collected: int = 0  # distinct rows read this cycle
+    identity_unknown_rows: int = 0
+    malformed_rows: int = 0
+    unrecognised_keys: int = 0
+
+    @property
+    def reported_total(self) -> Any:
+        """``page.total`` of the last page read (``UNKNOWN`` when it was absent)."""
+        return self.page_totals[-1] if self.page_totals else UNKNOWN
+
+    @property
+    def partial(self) -> bool:
+        return (
+            self.stopped_by_cap
+            or self.stopped_by_error is not None
+            or self.empty_page is not None
+            or self.has_more_at_stop
+        )
+
+    @property
+    def mismatch(self) -> bool:
+        total = self.reported_total
+        return not self.partial and isinstance(total, int) and self.collected != total
+
+    @property
+    def state(self) -> str:
+        if self.partial:
+            return "PARTIAL"
+        return "MISMATCH" if self.mismatch else "COMPLETE"
+
+
+@dataclass(frozen=True)
+class Snapshot:
+    rows: tuple[Row, ...]  # this cycle's rows in source order, then rows not reobserved
+    cycle: int
+    namespace: str
+    has_more: Any = UNKNOWN
+    total: Any = UNKNOWN
+    limit: Any = UNKNOWN
+    scope: Any = UNKNOWN
+    counts: Any = UNKNOWN
+    warnings: tuple[str, ...] = ()
+
+
+# -- timestamps ---------------------------------------------------------------------
+
+
+def parse_timestamp(value: Any) -> float | None:
+    """Epoch seconds from an ISO 8601 string or an epoch number; None when unparsable."""
+    if isinstance(value, bool):
+        return None
+    if isinstance(value, (int, float)):
+        number = float(value)
+        if not math.isfinite(number):
+            return None
+        return (
+            number / 1000.0 if number > 1e11 else number
+        )  # PROPOSED: huge numbers are milliseconds
+    if isinstance(value, str):
+        text = value.strip()
+        if not text:
+            return None
+        try:
+            parsed = datetime.fromisoformat(
+                text[:-1] + "+00:00" if text.endswith(("Z", "z")) else text
+            )
+        except ValueError:
+            return None
+        if parsed.tzinfo is None:
+            parsed = parsed.replace(tzinfo=timezone.utc)
+        return parsed.timestamp()
+    return None
+
+
+# -- parsing --------------------------------------------------------------------------
+
+
+def _clean_json(value: Any, depth: int = 0) -> Any:
+    """A JSON value with every string sanitized; deep nesting collapses to UNKNOWN."""
+    if depth > 6:
+        return UNKNOWN
+    if isinstance(value, str):
+        return sanitize(value, "line")
+    if isinstance(value, dict):
+        return {
+            sanitize(str(k), "line"): _clean_json(v, depth + 1)
+            for k, v in value.items()
+        }
+    if isinstance(value, list):
+        return [_clean_json(v, depth + 1) for v in value]
+    return value
+
+
+def _lookup(obj: Any, path: tuple[str, ...]) -> Any:
+    for key in path:
+        if not isinstance(obj, dict):
+            return UNKNOWN
+        obj = obj.get(key)
+    return UNKNOWN if obj is None else obj
+
+
+def _value(raw: Any, attr: str) -> Any:
+    """One row value: UNKNOWN stays UNKNOWN, text is sanitized, containers become text."""
+    if raw is UNKNOWN:
+        return UNKNOWN
+    mode = "block" if attr in _BLOCK_FIELDS else "line"
+    if isinstance(raw, str):
+        return sanitize(raw, mode)
+    if isinstance(raw, (dict, list)):
+        return sanitize(
+            json.dumps(raw, sort_keys=True, ensure_ascii=False, default=str), mode
+        )
+    return raw
+
+
+def _count_unexpected(obj: dict, known: dict) -> int:
+    count = 0
+    for key, value in obj.items():
+        if key not in known:
+            count += 1
+        elif isinstance(known[key], dict) and isinstance(value, dict):
+            count += _count_unexpected(value, known[key])
+    return count
+
+
+def _parse_row(raw: dict, namespace: str, cycle: int, rank: int) -> Row:
+    values: dict[str, Any] = {}
+    absent: list[str] = []
+    for attr, path in _FIELDS:
+        found = _lookup(raw, path)
+        values[attr] = _value(found, attr)
+        if found is UNKNOWN:
+            absent.append(attr)
+    dispatch_id = values["dispatch_id"]
+    anonymous = (
+        dispatch_id is UNKNOWN
+        or not isinstance(dispatch_id, str)
+        or not dispatch_id.strip()
+    )
+    if anonymous:
+        values["dispatch_id"] = UNKNOWN
+        identity: tuple = (namespace, UNKNOWN, cycle, rank)
+        flags: tuple[str, ...] = (IDENTITY_UNKNOWN,)
+    else:
+        identity = (namespace, dispatch_id)
+        flags = ()
+    return Row(
+        namespace=namespace,
+        identity=identity,
+        cycle=cycle,
+        last_seen_cycle=cycle,
+        source_rank=rank,
+        absent_fields=tuple(absent),
+        flags=flags,
+        unrecognised_keys=_count_unexpected(raw, _KNOWN),
+        **values,
+    )
+
+
+def _non_negative_int(value: Any) -> Any:
+    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
+        return value
+    return UNKNOWN
+
+
+def parse_page(
+    obj: Any, namespace: str, cycle: int, source_rank_base: int = 0
+) -> ParsedPage:
+    """Parse one decoded ``worker-list`` reply; raise ``ShapeError`` on a broken envelope."""
+    result = obj.get("result") if isinstance(obj, dict) else None
+    if not isinstance(result, dict):
+        raise ShapeError("result is not an object")
+    workers = result.get("workers")
+    if not isinstance(workers, list):
+        raise ShapeError("result.workers is not a list")
+    page = result.get("page")
+    if not isinstance(page, dict):
+        raise ShapeError("result.page is not an object")
+    has_more = page.get("hasMore")
+    if not isinstance(has_more, bool):
+        raise ShapeError("result.page.hasMore is not a boolean")
+
+    rows: list[Row] = []
+    malformed = 0
+    for index, raw in enumerate(workers):
+        if not isinstance(raw, dict):
+            malformed += 1
+            continue
+        rows.append(_parse_row(raw, namespace, cycle, source_rank_base + index))
+
+    scope = result.get("scope")
+    counts = result.get("counts")
+    warnings = result.get("warnings")
+    return ParsedPage(
+        rows=tuple(rows),
+        raw_count=len(workers),
+        cycle=cycle,
+        namespace=namespace,
+        has_more=has_more,
+        total=_non_negative_int(page.get("total")),
+        limit=_non_negative_int(page.get("limit")),
+        scope=_clean_json(scope) if isinstance(scope, dict) else UNKNOWN,
+        counts=_clean_json(counts) if isinstance(counts, dict) else UNKNOWN,
+        warnings=tuple(sanitize(w, "line") for w in warnings if isinstance(w, str))[:50]
+        if isinstance(warnings, list)
+        else (),
+        malformed_rows=malformed,
+        unrecognised_keys=sum(row.unrecognised_keys for row in rows),
+    )
+
+
+# -- merging --------------------------------------------------------------------------
+
+
+def _with_order_flag(row: Row, flag: str | None) -> Row:
+    flags = tuple(f for f in row.flags if f not in _ORDER_FLAGS)
+    if flag:
+        flags += (flag,)
+    return replace(row, flags=flags)
+
+
+def _common_timestamps(old: Row, new: Row) -> tuple[float, float] | None:
+    """Like fields only: liveness.observedAt with liveness.observedAt, else evidence with evidence."""
+    for attr in ("liveness_observed_at", "evidence_last_observed_at"):
+        a, b = parse_timestamp(getattr(old, attr)), parse_timestamp(getattr(new, attr))
+        if a is not None and b is not None:
+            return a, b
+    return None
+
+
+def _pick_within_cycle(first: Row, second: Row) -> Row:
+    """Two copies of one identity in one cycle: the newer timestamp wins; no common one keeps the first."""
+    stamps = _common_timestamps(first, second)
+    if stamps is None:
+        return _with_order_flag(first, ORDER_UNKNOWN)
+    return second if stamps[1] > stamps[0] else first
+
+
+def _pick_across_cycles(previous: Row, new: Row, cycle: int) -> Row:
+    """The same identity in an earlier cycle and this one."""
+    stamps = _common_timestamps(previous, new)
+    if stamps is None:
+        return _with_order_flag(new, ORDER_UNKNOWN)  # the newer cycle wins
+    if stamps[1] >= stamps[0]:
+        return new  # newer, or equal: the newer cycle wins
+    # An older timestamp never overwrites a newer one.
+    kept = replace(
+        previous,
+        last_seen_cycle=cycle,
+        source_rank=new.source_rank,
+        reobserved=True,
+    )
+    return _with_order_flag(kept, CONFLICT_BACKWARD)
+
+
+def merge(
+    previous: Snapshot | None,
+    pages: Sequence[ParsedPage],
+    stopped_by_cap: bool,
+    stopped_by_error: str | None,
+    clock: object = None,
+) -> tuple[Snapshot, Coverage]:
+    """Merge the pages of one cycle into the row set kept since earlier cycles.
+
+    Pure: ``clock`` is accepted for the AD-19 signature and unused, because ordering comes
+    from the rows' own timestamps and the cycle numbers.
+    """
+    if not pages:
+        raise ValueError("merge needs at least one page")
+    cycle = pages[0].cycle
+    this_cycle: list[Row] = []
+    index_of: dict[tuple, int] = {}
+    duplicates = 0
+    for page in pages:
+        for row in page.rows:
+            if row.identity_unknown:
+                this_cycle.append(row)  # no identity: never deduplicated, never matched
+            elif row.identity in index_of:
+                duplicates += 1
+                slot = index_of[row.identity]
+                this_cycle[slot] = _pick_within_cycle(this_cycle[slot], row)
+            else:
+                index_of[row.identity] = len(this_cycle)
+                this_cycle.append(row)
+
+    last = pages[-1]
+    totals = tuple(page.total for page in pages)
+    known_totals = {t for t in totals if isinstance(t, int)}
+    empty_page = next(
+        (
+            n
+            for n, page in enumerate(pages, start=1)
+            if not page.rows
+            and page.raw_count == 0
+            and isinstance(page.total, int)
+            and page.total > 0
+        ),
+        None,
+    )
+    coverage = Coverage(
+        page_totals=totals,
+        pages_read=len(pages),
+        empty_page=empty_page,
+        has_more_at_stop=last.has_more,
+        duplicates=duplicates,
+        total_changed=len(known_totals) > 1,
+        stopped_by_cap=stopped_by_cap,
+        stopped_by_error=stopped_by_error,
+        collected=len(this_cycle),
+        identity_unknown_rows=sum(1 for row in this_cycle if row.identity_unknown),
+        malformed_rows=sum(page.malformed_rows for page in pages),
+        unrecognised_keys=sum(page.unrecognised_keys for page in pages),
+    )
+
+    previous_rows = previous.rows if previous is not None else ()
+    previous_by_id = {
+        row.identity: row for row in previous_rows if not row.identity_unknown
+    }
+    merged: list[Row] = []
+    for row in this_cycle:
+        before = None if row.identity_unknown else previous_by_id.get(row.identity)
+        merged.append(
+            row if before is None else _pick_across_cycles(before, row, cycle)
+        )
+    returned = {row.identity for row in merged}
+    for row in previous_rows:
+        if row.identity in returned:
+            continue
+        if row.identity_unknown and not coverage.partial:
+            continue  # a complete cycle replaces the previous cycle's anonymous rows
+        merged.append(replace(row, reobserved=False))
+
+    warnings: list[str] = []
+    for page in pages:
+        warnings.extend(w for w in page.warnings if w not in warnings)
+    snapshot = Snapshot(
+        rows=tuple(merged),
+        cycle=cycle,
+        namespace=last.namespace,
+        has_more=last.has_more,
+        total=last.total,
+        limit=last.limit,
+        scope=last.scope,
+        counts=last.counts,
+        warnings=tuple(warnings[:50]),
+    )
+    return snapshot, coverage
diff --git a/tests/observe/test_parse.py b/tests/observe/test_parse.py
new file mode 100644
index 000000000..7f470fe7f
--- /dev/null
+++ b/tests/observe/test_parse.py
@@ -0,0 +1,444 @@
+"""Parser and merge tests (AD-7, AD-19; T22, T32 parse half, T39 in acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import copy
+
+import pytest
+
+from superclaude.cli.observe.parse import (
+    CONFLICT_BACKWARD,
+    IDENTITY_UNKNOWN,
+    ORDER_UNKNOWN,
+    UNKNOWN,
+    ShapeError,
+    merge,
+    parse_page,
+    parse_timestamp,
+)
+
+T0 = "2026-11-08T12:00:00Z"
+T1 = "2026-11-08T12:00:10Z"
+T2 = "2026-11-08T12:00:20Z"
+
+
+def worker(dispatch="w-001", observed=None, evidence=None, kind="none", **extra):
+    liveness = {"verdict": "alive", "source": "terminal"}
+    if observed:
+        liveness["observedAt"] = observed
+    row = {
+        "dispatchId": dispatch,
+        "taskId": "t-001",
+        "runId": "run-a",
+        "workerState": "running",
+        "dispatchStatus": "active",
+        "terminalState": "active",
+        "resource": {"id": "r-1", "worktreeId": "wt-1"},
+        "projection": {
+            "outcome": "none",
+            "role": "worker",
+            "provider": {"id": "claude"},
+            "host": {"id": "local", "kind": "local"},
+            "stage": {"worker": "coding", "dispatch": "running"},
+            "nextAction": {"kind": kind},
+            "liveness": liveness,
+            "evidence": {"durable": False, "liveStatus": "live"},
+        },
+    }
+    if evidence:
+        row["projection"]["evidence"]["lastObservedAt"] = evidence
+    row.update(extra)
+    return row
+
+
+def envelope(workers, has_more=False, total=UNKNOWN, **result):
+    page = {"hasMore": has_more, "limit": 100}
+    if total is not UNKNOWN:
+        page["total"] = total
+    body = {
+        "workers": workers,
+        "page": page,
+        "scope": {"source": "all"},
+        "counts": {"active": 1},
+    }
+    body.update(result)
+    return {"result": body}
+
+
+def page(workers, cycle=1, namespace="orca-a", base=0, **kw):
+    return parse_page(envelope(workers, **kw), namespace, cycle, base)
+
+
+def run_cycle(
+    previous,
+    workers,
+    cycle,
+    namespace="orca-a",
+    cap=False,
+    error=None,
+    has_more=False,
+    total=UNKNOWN,
+):
+    parsed = page(
+        workers, cycle=cycle, namespace=namespace, has_more=has_more, total=total
+    )
+    return merge(previous, [parsed], cap, error, None)
+
+
+def by_id(snapshot, dispatch):
+    return next(r for r in snapshot.rows if r.dispatch_id == dispatch)
+
+
+# -- T32: envelope is strict, rows are lenient ---------------------------------------
+
+BROKEN = {
+    "empty object": {},
+    "not an object": [],
+    "result null": {"result": None},
+    "result missing": {"other": 1},
+    "result not object": {"result": []},
+    "workers missing": {"result": {"page": {"hasMore": False}}},
+    "workers not a list": {"result": {"workers": {}, "page": {"hasMore": False}}},
+    "workers string": {"result": {"workers": "x", "page": {"hasMore": False}}},
+    "workers null": {"result": {"workers": None, "page": {"hasMore": False}}},
+    "page missing": {"result": {"workers": []}},
+    "hasMore missing": {"result": {"workers": [], "page": {}}},
+    "hasMore string false": {"result": {"workers": [], "page": {"hasMore": "false"}}},
+    "hasMore null": {"result": {"workers": [], "page": {"hasMore": None}}},
+    "hasMore int": {"result": {"workers": [], "page": {"hasMore": 0}}},
+}
+
+
+@pytest.mark.parametrize("name", sorted(BROKEN))
+def test_broken_envelope_is_a_shape_error_and_leaves_the_previous_snapshot(name):
+    previous, _ = run_cycle(None, [worker()], cycle=1)
+    frozen = copy.deepcopy(previous)
+    with pytest.raises(ShapeError):
+        merge(previous, [parse_page(BROKEN[name], "orca-a", 2)], False, None, None)
+    assert previous == frozen
+
+
+def test_missing_scope_and_total_are_unknown_for_that_field_only():
+    body = envelope([worker()])
+    del body["result"]["scope"]
+    parsed = parse_page(body, "orca-a", 1)
+    assert parsed.scope is UNKNOWN and parsed.total is UNKNOWN
+    assert parsed.counts == {"active": 1}
+    assert len(parsed.rows) == 1 and parsed.has_more is False
+
+
+@pytest.mark.parametrize("bad_total", [-1, "5", True, 1.5, None])
+def test_total_that_is_not_a_non_negative_integer_is_unknown(bad_total):
+    body = envelope([worker()])
+    body["result"]["page"]["total"] = bad_total
+    assert parse_page(body, "orca-a", 1).total is UNKNOWN
+    body["result"]["page"]["total"] = 0
+    assert parse_page(body, "orca-a", 1).total == 0
+
+
+def test_missing_inner_projection_key_is_unknown_in_that_row_not_an_error():
+    w = worker()
+    del w["projection"]["liveness"]["verdict"]
+    del w["projection"]["nextAction"]
+    row = page([w]).rows[0]
+    assert row.liveness_verdict is UNKNOWN and row.next_action_kind is UNKNOWN
+    assert row.liveness_source == "terminal"
+    assert {"liveness_verdict", "next_action_kind"} <= set(row.absent_fields)
+    w2 = worker()
+    del w2["projection"]
+    assert page([w2]).rows[0].outcome is UNKNOWN
+
+
+def test_json_null_and_absent_both_give_unknown_and_five_values_are_distinct():
+    w = worker(taskId=None)
+    del w["runId"]
+    row = page([w]).rows[0]
+    assert row.task_id is UNKNOWN and row.run_id is UNKNOWN
+    for other in (None, 0, False, ""):
+        assert UNKNOWN is not other and UNKNOWN != other
+    assert repr(UNKNOWN) == "UNKNOWN"
+    assert copy.deepcopy(UNKNOWN) is UNKNOWN and copy.copy(UNKNOWN) is UNKNOWN
+    # a source value that is the text "unknown" is a string, not the sentinel
+    assert page([worker(taskId="UNKNOWN")]).rows[0].task_id == "UNKNOWN"
+
+
+def test_non_object_rows_are_counted_and_skipped_and_text_is_sanitized():
+    parsed = page(
+        [worker("w-1"), "text", 5, None, worker("w-2\nsecond-line", stage=None)]
+    )
+    assert [r.dispatch_id for r in parsed.rows] == ["w-1", "w-2 second-line"]
+    assert parsed.malformed_rows == 3 and parsed.raw_count == 5
+    w = worker()
+    w["projection"]["stage"]["detail"] = "line1\nline2\x1b[31m"
+    w["projection"]["stage"]["activity"] = "act\nivity"
+    w["projection"]["role"] = "wo\nrker"
+    row = page([w]).rows[0]
+    assert row.stage_detail == "line1\nline2" and row.stage_activity == "act\nivity"
+    assert row.role == "wo rker"
+
+
+def test_unexpected_keys_are_counted_and_never_kept():
+    w = worker(agentTerminalHandle="term_secret_handle", surprise={"x": 1})
+    w["resource"]["terminalHandle"] = "term_other_secret"
+    w["projection"]["mystery"] = "mystery-value"
+    w["projection"]["nextAction"]["extra"] = "nested-extra-value"
+    row = page([w]).rows[0]
+    assert row.unrecognised_keys == 5
+    text = repr(row)
+    for leaked in (
+        "term_secret_handle",
+        "term_other_secret",
+        "mystery",
+        "nested-extra-value",
+        "surprise",
+    ):
+        assert leaked not in text
+    assert page([worker()]).rows[0].unrecognised_keys == 0
+
+
+def test_fixture_frozen_is_never_set_by_parse_page():
+    assert page([worker(fixtureOnly={"frozen": True})]).rows[0].fixture_frozen is False
+
+
+# -- identity ---------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("missing", ["absent", "null", "empty", "blank"])
+def test_row_without_dispatch_id_keeps_a_per_cycle_identity_and_never_merges(missing):
+    def anonymous():
+        w = worker()
+        if missing == "absent":
+            del w["dispatchId"]
+        else:
+            w["dispatchId"] = {"null": None, "empty": "", "blank": "  \t "}[missing]
+        return w
+
+    snapshot, coverage = run_cycle(
+        None, [anonymous(), anonymous(), worker("w-1")], cycle=1
+    )
+    anon = [r for r in snapshot.rows if r.dispatch_id is UNKNOWN]
+    assert len(anon) == 2 and len({r.identity for r in anon}) == 2
+    assert all(IDENTITY_UNKNOWN in r.flags and r.identity_unknown for r in anon)
+    assert coverage.duplicates == 0 and coverage.identity_unknown_rows == 2
+    assert anon[0].identity[1] is UNKNOWN and anon[0].identity[2] == 1
+
+
+def test_anonymous_rows_are_replaced_by_a_complete_cycle_and_kept_by_a_partial_one():
+    def anonymous():
+        w = worker()
+        del w["dispatchId"]
+        return w
+
+    first, _ = run_cycle(None, [anonymous(), worker("w-1")], cycle=1)
+    complete, _ = run_cycle(first, [anonymous(), worker("w-1")], cycle=2)
+    anon = [r for r in complete.rows if r.identity_unknown]
+    assert len(anon) == 1 and anon[0].cycle == 2 and anon[0].reobserved
+
+    partial, cov = run_cycle(
+        first, [anonymous(), worker("w-1")], cycle=2, cap=True, has_more=True
+    )
+    assert cov.partial
+    anon = sorted(
+        (r for r in partial.rows if r.identity_unknown), key=lambda r: r.cycle
+    )
+    assert [(r.cycle, r.reobserved) for r in anon] == [(1, False), (2, True)]
+    # rows with a real identity are unaffected either way
+    for snap in (complete, partial):
+        assert len([r for r in snap.rows if r.dispatch_id == "w-1"]) == 1
+
+
+def test_same_dispatch_id_under_two_namespaces_stays_two_rows():
+    pages = [
+        page([worker("w-1")], namespace="orca-a"),
+        page([worker("w-1")], namespace="orca-b", base=1),
+    ]
+    snapshot, coverage = merge(None, pages, False, None, None)
+    assert len(snapshot.rows) == 2 and coverage.duplicates == 0
+    assert {r.identity for r in snapshot.rows} == {("orca-a", "w-1"), ("orca-b", "w-1")}
+
+
+# -- duplicates, order, time (T22) -----------------------------------------------------
+
+
+def test_duplicates_within_a_cycle_are_dropped_and_counted_exactly():
+    pages = [
+        page([worker("w-1", observed=T1), worker("w-1", observed=T1), worker("w-2")]),
+        page([worker("w-1", observed=T1), worker("w-3")], base=3),
+    ]
+    snapshot, coverage = merge(None, pages, False, None, None)
+    assert [r.dispatch_id for r in snapshot.rows] == ["w-1", "w-2", "w-3"]
+    assert coverage.duplicates == 2 and coverage.collected == 3
+
+
+def test_within_a_cycle_the_newer_timestamp_wins_and_no_common_timestamp_flags_order_unknown():
+    snapshot, _ = run_cycle(
+        None,
+        [
+            worker("w-1", observed=T0, kind="old"),
+            worker("w-1", observed=T2, kind="new"),
+        ],
+        1,
+    )
+    assert snapshot.rows[0].next_action_kind == "new" and snapshot.rows[0].flags == ()
+    snapshot, _ = run_cycle(
+        None,
+        [
+            worker("w-1", observed=T2, kind="first"),
+            worker("w-1", observed=T0, kind="late"),
+        ],
+        1,
+    )
+    assert snapshot.rows[0].next_action_kind == "first"
+    snapshot, _ = run_cycle(None, [worker("w-1", kind="a"), worker("w-1", kind="b")], 1)
+    assert (
+        snapshot.rows[0].flags == (ORDER_UNKNOWN,)
+        and snapshot.rows[0].next_action_kind == "a"
+    )
+
+
+def test_an_older_observed_at_never_overwrites_a_newer_one():
+    first, _ = run_cycle(None, [worker("w-1", observed=T2, kind="newer-data")], cycle=1)
+    second, _ = run_cycle(
+        first, [worker("w-1", observed=T0, kind="older-data")], cycle=2
+    )
+    row = by_id(second, "w-1")
+    assert row.next_action_kind == "newer-data" and row.liveness_observed_at == T2
+    assert (
+        row.flags == (CONFLICT_BACKWARD,)
+        and row.reobserved
+        and row.last_seen_cycle == 2
+    )
+
+
+def test_newer_and_equal_timestamps_let_the_newer_cycle_win():
+    first, _ = run_cycle(None, [worker("w-1", observed=T1, kind="c1")], cycle=1)
+    newer, _ = run_cycle(first, [worker("w-1", observed=T2, kind="c2")], cycle=2)
+    assert (
+        by_id(newer, "w-1").next_action_kind == "c2" and by_id(newer, "w-1").flags == ()
+    )
+    equal, _ = run_cycle(first, [worker("w-1", observed=T1, kind="c2")], cycle=2)
+    assert (
+        by_id(equal, "w-1").next_action_kind == "c2" and by_id(equal, "w-1").flags == ()
+    )
+
+
+def test_missing_both_timestamps_or_no_common_field_or_unparsable_flags_order_unknown():
+    first, _ = run_cycle(None, [worker("w-1", kind="c1")], cycle=1)
+    second, _ = run_cycle(first, [worker("w-1", kind="c2")], cycle=2)
+    row = by_id(second, "w-1")
+    assert row.flags == (ORDER_UNKNOWN,) and row.next_action_kind == "c2"
+    # no common field: liveness in one cycle, evidence in the other
+    a, _ = run_cycle(None, [worker("w-1", observed=T1)], cycle=1)
+    b, _ = run_cycle(a, [worker("w-1", evidence=T2, kind="c2")], cycle=2)
+    assert by_id(b, "w-1").flags == (ORDER_UNKNOWN,)
+    # unparsable counts as absent
+    c, _ = run_cycle(a, [worker("w-1", observed="not a time", kind="c3")], cycle=2)
+    assert (
+        by_id(c, "w-1").flags == (ORDER_UNKNOWN,)
+        and by_id(c, "w-1").next_action_kind == "c3"
+    )
+
+
+def test_evidence_timestamps_are_compared_with_evidence_timestamps():
+    a, _ = run_cycle(None, [worker("w-1", evidence=T2, kind="newer")], cycle=1)
+    b, _ = run_cycle(a, [worker("w-1", evidence=T0, kind="older")], cycle=2)
+    assert by_id(b, "w-1").next_action_kind == "newer" and by_id(b, "w-1").flags == (
+        CONFLICT_BACKWARD,
+    )
+
+
+def test_a_flag_clears_on_the_next_clean_cycle():
+    a, _ = run_cycle(None, [worker("w-1", kind="c1")], cycle=1)
+    b, _ = run_cycle(a, [worker("w-1", kind="c2")], cycle=2)
+    c, _ = run_cycle(
+        b, [worker("w-1", observed=T1, kind="c3")], cycle=3
+    )  # b has no liveness stamp: unknown again
+    d, _ = run_cycle(c, [worker("w-1", observed=T2, kind="c4")], cycle=4)
+    assert by_id(d, "w-1").flags == ()
+
+
+# -- the row set across cycles ---------------------------------------------------------
+
+
+def test_a_row_missing_from_the_next_cycle_stays_with_reobserved_false():
+    first, _ = run_cycle(None, [worker("w-1"), worker("w-2")], cycle=1)
+    second, _ = run_cycle(first, [worker("w-2")], cycle=2)
+    assert [(r.dispatch_id, r.reobserved, r.last_seen_cycle) for r in second.rows] == [
+        ("w-2", True, 2),
+        ("w-1", False, 1),
+    ]
+    third, _ = run_cycle(second, [worker("w-2")], cycle=3)
+    assert (
+        by_id(third, "w-1").reobserved is False
+        and by_id(third, "w-1").last_seen_cycle == 1
+    )
+
+
+def test_coverage_records_totals_empty_pages_has_more_and_changes():
+    p1 = page([worker("w-1")], total=250, has_more=True)
+    p2 = page([worker("w-2")], total=251, has_more=True, base=1)
+    snapshot, cov = merge(None, [p1, p2], True, None, None)
+    assert (
+        cov.page_totals == (250, 251)
+        and cov.total_changed
+        and cov.reported_total == 251
+    )
+    assert (
+        cov.has_more_at_stop
+        and cov.stopped_by_cap
+        and cov.partial
+        and cov.state == "PARTIAL"
+    )
+    assert snapshot.total == 251 and snapshot.has_more is True
+
+    empty = page([], total=5, base=1)
+    _, cov = merge(
+        None, [page([worker("w-1")], total=5, has_more=True), empty], False, None, None
+    )
+    assert cov.empty_page == 2 and cov.partial
+
+    _, cov = merge(None, [page([worker("w-1")], total=3)], False, None, None)
+    assert cov.state == "MISMATCH" and cov.mismatch and not cov.partial
+    _, cov = merge(None, [page([worker("w-1")], total=1)], False, None, None)
+    assert cov.state == "COMPLETE"
+    _, cov = merge(None, [page([worker("w-1")], total=1)], False, "timeout", None)
+    assert cov.partial and cov.stopped_by_error == "timeout"
+    _, cov = merge(None, [page([worker("w-1")])], False, None, None)
+    assert cov.reported_total is UNKNOWN and cov.state == "COMPLETE"
+
+
+def test_merge_needs_at_least_one_page():
+    with pytest.raises(ValueError):
+        merge(None, [], False, None, None)
+
+
+def test_envelope_fields_are_sanitized_and_counted():
+    body = envelope(
+        [worker()],
+        warnings=["warn\x1b[31m one", 5, "two\nlines"],
+        scope={"source": "bo\x07und"},
+    )
+    parsed = parse_page(body, "orca-a", 1)
+    assert parsed.warnings == ("warn one", "two lines")
+    assert parsed.scope == {"source": "bound"}
+    assert parsed.limit == 100
+
+
+@pytest.mark.parametrize(
+    ("value", "expected"),
+    [
+        (T0, 1794139200.0),
+        ("2026-11-08T12:00:00+00:00", 1794139200.0),
+        ("2026-11-08T12:00:00", 1794139200.0),
+        (1794139200, 1794139200.0),
+        (1794139200000, 1794139200.0),
+        ("garbage", None),
+        ("", None),
+        (True, None),
+        (None, None),
+        (float("nan"), None),
+        (UNKNOWN, None),
+    ],
+)
+def test_parse_timestamp(value, expected):
+    assert parse_timestamp(value) == expected

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
