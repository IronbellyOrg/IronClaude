"""Parsing and merging of ``worker-list`` pages (AD-7, AD-19).

``parse_page`` is strict on the envelope and lenient inside rows. ``merge`` is the one
pure function that owns the row set across pages and cycles. Only verified worker-list
keys are read; any other key is counted and dropped (its name and value are never kept).
"""

from __future__ import annotations

import copy
import json
import math
import re
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from importlib import resources
from typing import Any

from superclaude.cli.observe.sanitize import sanitize

# -- the UNKNOWN sentinel -------------------------------------------------------


class _Unknown:
    """The single "the source did not give this" value (never None, 0, False or "")."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "UNKNOWN"

    def __copy__(self) -> _Unknown:
        return self

    def __deepcopy__(self, memo: object) -> _Unknown:
        return self

    def __reduce__(self) -> str:
        return "UNKNOWN"


UNKNOWN: Any = _Unknown()

IDENTITY_UNKNOWN = "identity unknown"
ORDER_UNKNOWN = "order unknown"
CONFLICT_BACKWARD = "conflict (time went back)"
_ORDER_FLAGS = (ORDER_UNKNOWN, CONFLICT_BACKWARD)


class ShapeError(ValueError):
    """The envelope is not a worker-list reply (cycle is ``FAILED (shape)``)."""


# -- the verified worker-list keys ------------------------------------------------

# attribute name -> key path inside one worker row
_FIELDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("dispatch_id", ("dispatchId",)),
    ("task_id", ("taskId",)),
    ("run_id", ("runId",)),
    ("worker_state", ("workerState",)),
    ("dispatch_status", ("dispatchStatus",)),
    ("terminal_state", ("terminalState",)),
    ("resource_id", ("resource", "id")),
    ("ownership_state", ("resource", "ownershipState")),
    ("release_state", ("resource", "releaseState")),
    ("worktree_id", ("resource", "worktreeId")),
    ("owner_dispatch_id", ("resource", "ownerDispatchId")),
    ("origin_dispatch_id", ("resource", "originDispatchId")),
    ("recovery_attempt_count", ("resource", "recoveryAttemptCount")),
    ("outcome", ("projection", "outcome")),
    ("role", ("projection", "role")),
    ("provider_id", ("projection", "provider", "id")),
    ("host_id", ("projection", "host", "id")),
    ("host_kind", ("projection", "host", "kind")),
    ("workspace_id", ("projection", "workspace", "id")),
    ("workspace_kind", ("projection", "workspace", "kind")),
    ("stage_worker", ("projection", "stage", "worker")),
    ("stage_dispatch", ("projection", "stage", "dispatch")),
    ("stage_activity", ("projection", "stage", "activity")),
    ("stage_detail", ("projection", "stage", "detail")),
    ("next_action_kind", ("projection", "nextAction", "kind")),
    ("liveness_verdict", ("projection", "liveness", "verdict")),
    ("liveness_source", ("projection", "liveness", "source")),
    ("liveness_observed_at", ("projection", "liveness", "observedAt")),
    ("evidence_durable", ("projection", "evidence", "durable")),
    ("evidence_live_status", ("projection", "evidence", "liveStatus")),
    ("evidence_last_observed_at", ("projection", "evidence", "lastObservedAt")),
)
_BLOCK_FIELDS = frozenset(
    {"stage_detail", "stage_activity"}
)  # the only block-mode text


def _known_tree() -> dict[str, Any]:
    tree: dict[str, Any] = {}
    for _, path in _FIELDS:
        node = tree
        for key in path[:-1]:
            node = node.setdefault(key, {})
        node[path[-1]] = None  # leaf
    return tree


_KNOWN = _known_tree()


@dataclass(frozen=True)
class Row:
    """One worker, every value a source value or ``UNKNOWN`` (strings already sanitized)."""

    namespace: str
    identity: tuple
    cycle: int  # the cycle whose data this copy holds
    last_seen_cycle: int  # the latest cycle that returned this row
    source_rank: int  # position in the cycle's newest-first pages
    dispatch_id: Any = UNKNOWN
    task_id: Any = UNKNOWN
    run_id: Any = UNKNOWN
    worker_state: Any = UNKNOWN
    dispatch_status: Any = UNKNOWN
    terminal_state: Any = UNKNOWN
    resource_id: Any = UNKNOWN
    ownership_state: Any = UNKNOWN
    release_state: Any = UNKNOWN
    worktree_id: Any = UNKNOWN
    owner_dispatch_id: Any = UNKNOWN
    origin_dispatch_id: Any = UNKNOWN
    recovery_attempt_count: Any = UNKNOWN
    outcome: Any = UNKNOWN
    role: Any = UNKNOWN
    provider_id: Any = UNKNOWN
    host_id: Any = UNKNOWN
    host_kind: Any = UNKNOWN
    workspace_id: Any = UNKNOWN
    workspace_kind: Any = UNKNOWN
    stage_worker: Any = UNKNOWN
    stage_dispatch: Any = UNKNOWN
    stage_activity: Any = UNKNOWN
    stage_detail: Any = UNKNOWN
    next_action_kind: Any = UNKNOWN
    liveness_verdict: Any = UNKNOWN
    liveness_source: Any = UNKNOWN
    liveness_observed_at: Any = UNKNOWN
    evidence_durable: Any = UNKNOWN
    evidence_live_status: Any = UNKNOWN
    evidence_last_observed_at: Any = UNKNOWN
    absent_fields: tuple[
        str, ...
    ] = ()  # attributes that are UNKNOWN because the source omitted them
    flags: tuple[
        str, ...
    ] = ()  # "identity unknown", "order unknown", "conflict (time went back)"
    unrecognised_keys: int = 0
    reobserved: bool = True
    fixture_frozen: bool = False  # set only by the fixture loader, never by parse_page

    @property
    def identity_unknown(self) -> bool:
        return IDENTITY_UNKNOWN in self.flags


@dataclass(frozen=True)
class ParsedPage:
    rows: tuple[Row, ...]
    raw_count: int  # entries in result.workers, malformed ones included
    cycle: int
    namespace: str
    has_more: bool
    total: Any = UNKNOWN  # int or UNKNOWN
    limit: Any = UNKNOWN  # int or UNKNOWN
    scope: Any = UNKNOWN  # sanitized object or UNKNOWN
    counts: Any = UNKNOWN  # sanitized object, passed through, never summed
    warnings: tuple[str, ...] = ()
    malformed_rows: int = 0
    unrecognised_keys: int = 0


@dataclass(frozen=True)
class Coverage:
    page_totals: tuple = ()  # result.page.total of each page read (int or UNKNOWN)
    pages_read: int = 0
    empty_page: int | None = (
        None  # 1-based index of a page with no workers while its total is above 0
    )
    has_more_at_stop: bool = False
    duplicates: int = 0
    total_changed: bool = False  # page.total differed between pages
    stopped_by_cap: bool = False
    stopped_by_error: str | None = None
    collected: int = 0  # distinct rows read this cycle
    identity_unknown_rows: int = 0
    malformed_rows: int = 0
    unrecognised_keys: int = 0

    @property
    def reported_total(self) -> Any:
        """``page.total`` of the last page read (``UNKNOWN`` when it was absent)."""
        return self.page_totals[-1] if self.page_totals else UNKNOWN

    @property
    def partial(self) -> bool:
        return (
            self.stopped_by_cap
            or self.stopped_by_error is not None
            or self.empty_page is not None
            or self.has_more_at_stop
        )

    @property
    def mismatch(self) -> bool:
        total = self.reported_total
        return not self.partial and isinstance(total, int) and self.collected != total

    @property
    def state(self) -> str:
        if self.partial:
            return "PARTIAL"
        return "MISMATCH" if self.mismatch else "COMPLETE"


@dataclass(frozen=True)
class Snapshot:
    rows: tuple[Row, ...]  # this cycle's rows in source order, then rows not reobserved
    cycle: int
    namespace: str
    has_more: Any = UNKNOWN
    total: Any = UNKNOWN
    limit: Any = UNKNOWN
    scope: Any = UNKNOWN
    counts: Any = UNKNOWN
    warnings: tuple[str, ...] = ()


# -- timestamps ---------------------------------------------------------------------


def parse_timestamp(value: Any) -> float | None:
    """Epoch seconds from an ISO 8601 string or an epoch number; None when unparsable."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        number = float(value)
        if not math.isfinite(number):
            return None
        return (
            number / 1000.0 if number > 1e11 else number
        )  # PROPOSED: huge numbers are milliseconds
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(
                text[:-1] + "+00:00" if text.endswith(("Z", "z")) else text
            )
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.timestamp()
    return None


def format_utc_iso(epoch: float) -> str:
    """Epoch seconds as UTC ISO 8601, whole seconds, e.g. ``2026-11-08T12:00:03Z``."""
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_local(epoch: float, tz: Any, pattern: str) -> str:
    """Epoch seconds as local time in ``tz`` (a tzinfo from the injected clock)."""
    return datetime.fromtimestamp(epoch, tz).strftime(pattern)


# -- parsing --------------------------------------------------------------------------


def _clean_json(value: Any, depth: int = 0) -> Any:
    """A JSON value with every string sanitized; deep nesting collapses to UNKNOWN."""
    if depth > 6:
        return UNKNOWN
    if isinstance(value, str):
        return sanitize(value, "line")
    if isinstance(value, dict):
        return {
            sanitize(str(k), "line"): _clean_json(v, depth + 1)
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_clean_json(v, depth + 1) for v in value]
    return value


def _lookup(obj: Any, path: tuple[str, ...]) -> Any:
    for key in path:
        if not isinstance(obj, dict):
            return UNKNOWN
        obj = obj.get(key)
    return UNKNOWN if obj is None else obj


def _value(raw: Any, attr: str) -> Any:
    """One row value: UNKNOWN stays UNKNOWN, text is sanitized, containers become text."""
    if raw is UNKNOWN:
        return UNKNOWN
    mode = "block" if attr in _BLOCK_FIELDS else "line"
    if isinstance(raw, str):
        return sanitize(raw, mode)
    if isinstance(raw, (dict, list)):
        return sanitize(
            json.dumps(raw, sort_keys=True, ensure_ascii=False, default=str), mode
        )
    return raw


def _count_unexpected(obj: dict, known: dict) -> int:
    count = 0
    for key, value in obj.items():
        if key not in known:
            count += 1
        elif isinstance(known[key], dict) and isinstance(value, dict):
            count += _count_unexpected(value, known[key])
    return count


def _parse_row(raw: dict, namespace: str, cycle: int, rank: int) -> Row:
    values: dict[str, Any] = {}
    absent: list[str] = []
    for attr, path in _FIELDS:
        found = _lookup(raw, path)
        values[attr] = _value(found, attr)
        if found is UNKNOWN:
            absent.append(attr)
    dispatch_id = values["dispatch_id"]
    anonymous = (
        dispatch_id is UNKNOWN
        or not isinstance(dispatch_id, str)
        or not dispatch_id.strip()
    )
    if anonymous:
        values["dispatch_id"] = UNKNOWN
        identity: tuple = (namespace, UNKNOWN, cycle, rank)
        flags: tuple[str, ...] = (IDENTITY_UNKNOWN,)
    else:
        identity = (namespace, dispatch_id)
        flags = ()
    return Row(
        namespace=namespace,
        identity=identity,
        cycle=cycle,
        last_seen_cycle=cycle,
        source_rank=rank,
        absent_fields=tuple(absent),
        flags=flags,
        unrecognised_keys=_count_unexpected(raw, _KNOWN),
        **values,
    )


def _non_negative_int(value: Any) -> Any:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return UNKNOWN


def parse_page(
    obj: Any, namespace: str, cycle: int, source_rank_base: int = 0
) -> ParsedPage:
    """Parse one decoded ``worker-list`` reply; raise ``ShapeError`` on a broken envelope."""
    result = obj.get("result") if isinstance(obj, dict) else None
    if not isinstance(result, dict):
        raise ShapeError("result is not an object")
    workers = result.get("workers")
    if not isinstance(workers, list):
        raise ShapeError("result.workers is not a list")
    page = result.get("page")
    if not isinstance(page, dict):
        raise ShapeError("result.page is not an object")
    has_more = page.get("hasMore")
    if not isinstance(has_more, bool):
        raise ShapeError("result.page.hasMore is not a boolean")

    rows: list[Row] = []
    malformed = 0
    for index, raw in enumerate(workers):
        if not isinstance(raw, dict):
            malformed += 1
            continue
        rows.append(_parse_row(raw, namespace, cycle, source_rank_base + index))

    scope = result.get("scope")
    counts = result.get("counts")
    warnings = result.get("warnings")
    return ParsedPage(
        rows=tuple(rows),
        raw_count=len(workers),
        cycle=cycle,
        namespace=namespace,
        has_more=has_more,
        total=_non_negative_int(page.get("total")),
        limit=_non_negative_int(page.get("limit")),
        scope=_clean_json(scope) if isinstance(scope, dict) else UNKNOWN,
        counts=_clean_json(counts) if isinstance(counts, dict) else UNKNOWN,
        warnings=tuple(sanitize(w, "line") for w in warnings if isinstance(w, str))[:50]
        if isinstance(warnings, list)
        else (),
        malformed_rows=malformed,
        unrecognised_keys=sum(row.unrecognised_keys for row in rows),
    )


# -- merging --------------------------------------------------------------------------


def _with_order_flag(row: Row, flag: str | None) -> Row:
    flags = tuple(f for f in row.flags if f not in _ORDER_FLAGS)
    if flag:
        flags += (flag,)
    return replace(row, flags=flags)


def _common_timestamps(old: Row, new: Row) -> tuple[float, float] | None:
    """Like fields only: liveness.observedAt with liveness.observedAt, else evidence with evidence."""
    for attr in ("liveness_observed_at", "evidence_last_observed_at"):
        a, b = parse_timestamp(getattr(old, attr)), parse_timestamp(getattr(new, attr))
        if a is not None and b is not None:
            return a, b
    return None


def _pick_within_cycle(first: Row, second: Row) -> Row:
    """Two copies of one identity in one cycle: the newer timestamp wins; no common one keeps the first."""
    stamps = _common_timestamps(first, second)
    if stamps is None:
        return _with_order_flag(first, ORDER_UNKNOWN)
    return second if stamps[1] > stamps[0] else first


def _pick_across_cycles(previous: Row, new: Row, cycle: int) -> Row:
    """The same identity in an earlier cycle and this one."""
    stamps = _common_timestamps(previous, new)
    if stamps is None:
        return _with_order_flag(new, ORDER_UNKNOWN)  # the newer cycle wins
    if stamps[1] >= stamps[0]:
        return new  # newer, or equal: the newer cycle wins
    # An older timestamp never overwrites a newer one.
    kept = replace(
        previous,
        last_seen_cycle=cycle,
        source_rank=new.source_rank,
        reobserved=True,
    )
    return _with_order_flag(kept, CONFLICT_BACKWARD)


def merge(
    previous: Snapshot | None,
    pages: Sequence[ParsedPage],
    stopped_by_cap: bool,
    stopped_by_error: str | None,
    clock: object = None,
) -> tuple[Snapshot, Coverage]:
    """Merge the pages of one cycle into the row set kept since earlier cycles.

    Pure: ``clock`` is accepted for the AD-19 signature and unused, because ordering comes
    from the rows' own timestamps and the cycle numbers.
    """
    if not pages:
        raise ValueError("merge needs at least one page")
    cycle = pages[0].cycle
    this_cycle: list[Row] = []
    index_of: dict[tuple, int] = {}
    duplicates = 0
    for page in pages:
        for row in page.rows:
            if row.identity_unknown:
                this_cycle.append(row)  # no identity: never deduplicated, never matched
            elif row.identity in index_of:
                duplicates += 1
                slot = index_of[row.identity]
                this_cycle[slot] = _pick_within_cycle(this_cycle[slot], row)
            else:
                index_of[row.identity] = len(this_cycle)
                this_cycle.append(row)

    last = pages[-1]
    totals = tuple(page.total for page in pages)
    known_totals = {t for t in totals if isinstance(t, int)}
    empty_page = next(
        (
            n
            for n, page in enumerate(pages, start=1)
            if not page.rows
            and page.raw_count == 0
            and isinstance(page.total, int)
            and page.total > 0
        ),
        None,
    )
    coverage = Coverage(
        page_totals=totals,
        pages_read=len(pages),
        empty_page=empty_page,
        has_more_at_stop=last.has_more,
        duplicates=duplicates,
        total_changed=len(known_totals) > 1,
        stopped_by_cap=stopped_by_cap,
        stopped_by_error=stopped_by_error,
        collected=len(this_cycle),
        identity_unknown_rows=sum(1 for row in this_cycle if row.identity_unknown),
        malformed_rows=sum(page.malformed_rows for page in pages),
        unrecognised_keys=sum(page.unrecognised_keys for page in pages),
    )

    previous_rows = previous.rows if previous is not None else ()
    previous_by_id = {
        row.identity: row for row in previous_rows if not row.identity_unknown
    }
    merged: list[Row] = []
    for row in this_cycle:
        before = None if row.identity_unknown else previous_by_id.get(row.identity)
        merged.append(
            row if before is None else _pick_across_cycles(before, row, cycle)
        )
    returned = {row.identity for row in merged}
    for row in previous_rows:
        if row.identity in returned:
            continue
        if row.identity_unknown and not coverage.partial:
            continue  # a complete cycle replaces the previous cycle's anonymous rows
        merged.append(replace(row, reobserved=False))

    warnings: list[str] = []
    for page in pages:
        warnings.extend(w for w in page.warnings if w not in warnings)
    snapshot = Snapshot(
        rows=tuple(merged),
        cycle=cycle,
        namespace=last.namespace,
        has_more=last.has_more,
        total=last.total,
        limit=last.limit,
        scope=last.scope,
        counts=last.counts,
        warnings=tuple(warnings[:50]),
    )
    return snapshot, coverage


# -- fixture loader (never used by the live parser path) ------------------------------

FIXTURE_PACKAGE = "superclaude.cli.observe.fixtures"
VARIANTS = (
    "base",
    "uneven",
    "shared-unmapped",
    "historical",
    "long-identifiers",
    "source-loss",
    "missing-fields",
    "duplicate-out-of-order",
    "empty",
    "injection",
)
_VARIANT_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True)
class FixtureCycle:
    """One replayed cycle: a worker-list envelope, or a failure code."""

    fail: str | None = None
    envelope: dict | None = None
    frozen: frozenset = (
        frozenset()
    )  # positions in result.workers carrying fixtureOnly.frozen


@dataclass(frozen=True)
class Fixture:
    variant: str
    cycles: tuple[FixtureCycle, ...]

    def cycle(self, index: int) -> FixtureCycle:
        """Cycle ``index`` (0-based); past the end the last cycle repeats."""
        return self.cycles[min(index, len(self.cycles) - 1)]

    def parse(
        self, index: int, namespace: str, cycle: int, source_rank_base: int = 0
    ) -> ParsedPage:
        """Parse a non-failing cycle with ``parse_page``, then mark frozen rows."""
        entry = self.cycle(index)
        if entry.envelope is None:
            raise ValueError(
                f"fixture cycle {index} is a failure ({entry.fail}), it has no page"
            )
        parsed = parse_page(entry.envelope, namespace, cycle, source_rank_base)
        return apply_frozen(parsed, entry.frozen, source_rank_base)


def apply_frozen(
    parsed: ParsedPage, frozen: frozenset, source_rank_base: int = 0
) -> ParsedPage:
    """Set ``fixture_frozen`` on the rows at the given raw positions (fixture mode only)."""
    if not frozen:
        return parsed
    rows = tuple(
        replace(row, fixture_frozen=True)
        if row.source_rank - source_rank_base in frozen
        else row
        for row in parsed.rows
    )
    return replace(parsed, rows=rows)


def load_fixture(variant: str) -> Fixture:
    """Load a fixture variant from the package data (``importlib.resources``)."""
    if not isinstance(variant, str) or not _VARIANT_NAME.match(variant):
        raise ValueError(f"invalid fixture variant name: {variant!r}")
    try:
        text = (
            resources.files(FIXTURE_PACKAGE)
            .joinpath(f"{variant}.json")
            .read_text(encoding="utf-8")
        )
    except (FileNotFoundError, OSError) as exc:
        raise ValueError(f"unknown fixture variant: {variant!r}") from exc
    data = json.loads(text)
    cycles: list[FixtureCycle] = []
    for raw in data["cycles"]:
        if "result" not in raw and "fail" in raw:
            cycles.append(FixtureCycle(fail=sanitize(str(raw["fail"]), "line")))
            continue
        envelope = copy.deepcopy(raw)
        frozen: set[int] = set()
        workers = (
            envelope.get("result", {}).get("workers")
            if isinstance(envelope.get("result"), dict)
            else None
        )
        if isinstance(workers, list):
            for position, worker in enumerate(workers):
                if isinstance(worker, dict) and "fixtureOnly" in worker:
                    marker = worker.pop(
                        "fixtureOnly"
                    )  # fixture-only: the live parser never sees it
                    if isinstance(marker, dict) and marker.get("frozen") is True:
                        frozen.add(position)
        cycles.append(FixtureCycle(envelope=envelope, frozen=frozenset(frozen)))
    return Fixture(variant=variant, cycles=tuple(cycles))
