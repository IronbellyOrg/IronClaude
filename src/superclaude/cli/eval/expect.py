"""FR-EXP1 ``Expect.*`` assertion primitives (COMP-010).

Roadmap COMP-010 / FR-EXP1 / Deliverable D-0064 (Task T04.01).

Seven primitives — :meth:`Expect.file`, :meth:`Expect.jsonl`,
:meth:`Expect.settings_json`, :meth:`Expect.exit_code`,
:meth:`Expect.stderr`, :meth:`Expect.stdout`, :meth:`Expect.duration` —
each return an :data:`ExpectCallable` (DM-009) that accepts an
:class:`EvalContext` (DM-010) and emits an :class:`ExpectResult`.

Both forms are supported:

* **Programmatic** — call the static method directly with named
  arguments (``Expect.exit_code(equals=0)``). The returned callable
  closes over the configured arguments and executes at runtime.
* **Declarative** — manifest authors write a YAML mapping like
  ``{exit_code: {equals: 0}}`` and :meth:`Expect.from_mapping` resolves
  the key against the primitive registry. Mapping form keys are the
  exact primitive names; mapping values are forwarded verbatim as
  keyword arguments.

Failure ExpectResults carry an :class:`ExpectFailure` (DM-005) with the
``expected`` / ``actual`` payload so the Reporter (COMP-008 / T03.13)
can render a diff without re-parsing the assertion message.

Per-primitive edge-case coverage lands in T04.02..T04.08; this module is
the FR-EXP1 package skeleton + initial implementations the per-primitive
subtasks then harden.
"""

from __future__ import annotations

import difflib
import json
import re
import time
import traceback
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Optional

from .models import EvalContext, ExpectFailure, ExpectResult
from .pty_stream import ANSI_ESCAPE_RE

__all__ = [
    "Expect",
    "ExpectCallable",
    "PRIMITIVE_NAMES",
]


# Re-export the runner's ExpectCallable alias so callers can import
# directly from :mod:`expect` without pulling in the runner module.
ExpectCallable = Callable[[EvalContext], ExpectResult]


PRIMITIVE_NAMES: tuple[str, ...] = (
    "file",
    "jsonl",
    "settings_json",
    "exit_code",
    "stderr",
    "stdout",
    "duration",
)


# Sentinel used by ``Expect.settings_json`` to distinguish "equals not
# provided" from "equals=None" (legitimate JSON null comparison). Module-
# level so the default-arg expression on ``Expect.settings_json`` can
# reference it at class-definition time.
_SENTINEL: Any = object()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_path(ctx: EvalContext, path: str | Path) -> Path:
    """Resolve a primitive's ``path`` argument against the per-eval HOME.

    Absolute paths are returned untouched. Relative paths are resolved
    against ``ctx.home_path`` so manifest authors can write paths like
    ``"logs/hook.jsonl"`` without worrying about the per-eval scratch
    root layout.
    """

    p = Path(path)
    if p.is_absolute():
        return p
    return ctx.home_path / p


def _strip_ansi(text: str) -> str:
    """Return ``text`` with ANSI escape sequences removed.

    ``PtyStream`` (T02.17) already strips ANSI from captured stdout /
    stderr, but the primitives re-strip defensively so manifest authors
    who feed raw transcript fixtures to :meth:`Expect.stdout` /
    :meth:`Expect.stderr` still get clean predicate matches.
    """

    return ANSI_ESCAPE_RE.sub("", text)


def _make_failure(
    ctx: EvalContext,
    *,
    name: str,
    expected: Any,
    actual: Any,
    message: str,
    artifact_ref: Optional[str] = None,
    exc: Optional[BaseException] = None,
) -> ExpectFailure:
    """Build an :class:`ExpectFailure` record from primitive-local state."""

    tb = "".join(traceback.format_exception(exc)) if exc is not None else None
    return ExpectFailure(
        eval_id=ctx.eval_spec.id,
        expect_id=name,
        expect_name=name,
        expected=expected,
        actual=actual,
        message=message,
        artifact_ref=artifact_ref,
        traceback=tb,
    )


def _unified_diff(expected: str, actual: str, *, name: str) -> str:
    """Return a unified diff snippet between ``expected`` and ``actual``."""

    diff_lines = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=f"expected/{name}",
        tofile=f"actual/{name}",
        n=3,
    )
    return "".join(diff_lines)


def _named_callable(
    name: str, fn: Callable[[EvalContext], ExpectResult]
) -> ExpectCallable:
    """Tag ``fn`` with ``__name__`` so the runner's JSONL log records it."""

    fn.__name__ = name
    return fn


def _timed_result(
    name: str,
    builder: Callable[[], tuple[bool, str, Mapping[str, Any], Optional[ExpectFailure]]],
) -> ExpectResult:
    """Run ``builder`` and wrap the outcome in an ExpectResult with timing."""

    start = time.monotonic()
    passed, message, details, failure = builder()
    duration = time.monotonic() - start
    return ExpectResult(
        name=name,
        passed=passed,
        message=message,
        details=details,
        duration_sec=duration,
        failure=failure,
    )


# ---------------------------------------------------------------------------
# Public DSL surface
# ---------------------------------------------------------------------------


class Expect:
    """COMP-010 / FR-EXP1 assertion primitive namespace.

    The class itself is never instantiated; each primitive is a
    ``@staticmethod`` returning an :data:`ExpectCallable`. This mirrors
    the M1 stub interface (T01.14) so manifest authors who shaped their
    ``expects:`` blocks against the stubs find a drop-in replacement.
    """

    # ---- COMP-010.1 -------------------------------------------------------

    @staticmethod
    def file(
        *,
        path: str | Path,
        exists: Optional[bool] = None,
        contains: Optional[str] = None,
        regex: Optional[str] = None,
        equals: Optional[str] = None,
    ) -> ExpectCallable:
        """Assert a file's existence and / or content (COMP-010.1).

        ``path`` resolves against :attr:`EvalContext.home_path` when
        relative. At least one of ``exists`` / ``contains`` / ``regex`` /
        ``equals`` should be set; when all are ``None`` the primitive
        only asserts the file is readable.
        """

        compiled = re.compile(regex) if regex is not None else None

        def _run(ctx: EvalContext) -> ExpectResult:
            def _build() -> tuple[
                bool, str, Mapping[str, Any], Optional[ExpectFailure]
            ]:
                resolved = _resolve_path(ctx, path)
                file_exists = resolved.exists()

                if exists is not None and file_exists != bool(exists):
                    msg = f"file existence: expected {bool(exists)} got {file_exists}"
                    return (
                        False,
                        msg,
                        {"path": str(resolved), "exists": file_exists},
                        _make_failure(
                            ctx,
                            name="file",
                            expected={"exists": bool(exists)},
                            actual={"exists": file_exists},
                            message=msg,
                        ),
                    )

                if not file_exists:
                    # Nothing else to assert against a missing file.
                    return (
                        True,
                        "file absent (per exists=False)",
                        {"path": str(resolved)},
                        None,
                    )

                content = resolved.read_text(encoding="utf-8", errors="replace")

                if equals is not None and content != equals:
                    diff = _unified_diff(equals, content, name=str(resolved))
                    return (
                        False,
                        "file content does not equal expected",
                        {
                            "path": str(resolved),
                            "diff": diff,
                        },
                        _make_failure(
                            ctx,
                            name="file",
                            expected=equals,
                            actual=content,
                            message="file content does not equal expected",
                        ),
                    )

                if contains is not None and contains not in content:
                    return (
                        False,
                        f"file missing substring {contains!r}",
                        {
                            "path": str(resolved),
                        },
                        _make_failure(
                            ctx,
                            name="file",
                            expected={"contains": contains},
                            actual=content,
                            message=f"substring {contains!r} not found in {resolved}",
                        ),
                    )

                if compiled is not None and compiled.search(content) is None:
                    return (
                        False,
                        f"file does not match regex {regex!r}",
                        {
                            "path": str(resolved),
                        },
                        _make_failure(
                            ctx,
                            name="file",
                            expected={"regex": regex},
                            actual=content,
                            message=f"regex {regex!r} did not match {resolved}",
                        ),
                    )

                return True, "file assertions satisfied", {"path": str(resolved)}, None

            return _timed_result("file", _build)

        return _named_callable("file", _run)

    # ---- COMP-010.2 -------------------------------------------------------

    @staticmethod
    def jsonl(
        *,
        path: str | Path,
        line_count: Optional[int] = None,
        filter: Optional[Callable[[Mapping[str, Any]], bool]] = None,
        assert_each: Optional[Callable[[Mapping[str, Any]], bool]] = None,
        assert_any: Optional[Callable[[Mapping[str, Any]], bool]] = None,
    ) -> ExpectCallable:
        """Assert JSONL entries match a predicate (COMP-010.2).

        ``path`` first resolves against :attr:`EvalContext.jsonl_paths`
        (named lookup); falling back to filesystem resolution against
        :attr:`EvalContext.home_path` when no name matches.
        """

        def _run(ctx: EvalContext) -> ExpectResult:
            def _build() -> tuple[
                bool, str, Mapping[str, Any], Optional[ExpectFailure]
            ]:
                path_str = str(path)
                if path_str in ctx.jsonl_paths:
                    resolved = Path(ctx.jsonl_paths[path_str])
                else:
                    resolved = _resolve_path(ctx, path)

                if not resolved.exists():
                    msg = f"jsonl path {resolved} does not exist"
                    return (
                        False,
                        msg,
                        {"path": str(resolved)},
                        _make_failure(
                            ctx,
                            name="jsonl",
                            expected={"exists": True},
                            actual={"exists": False},
                            message=msg,
                        ),
                    )

                rows: list[Mapping[str, Any]] = []
                with resolved.open("r", encoding="utf-8") as fh:
                    for lineno, raw in enumerate(fh, start=1):
                        raw = raw.strip()
                        if not raw:
                            continue
                        try:
                            rows.append(json.loads(raw))
                        except json.JSONDecodeError as exc:
                            msg = f"line {lineno} not valid JSON: {exc}"
                            return (
                                False,
                                msg,
                                {"path": str(resolved)},
                                _make_failure(
                                    ctx,
                                    name="jsonl",
                                    expected="valid JSON per line",
                                    actual=raw,
                                    message=msg,
                                    exc=exc,
                                ),
                            )

                filtered = [r for r in rows if filter is None or filter(r)]

                if line_count is not None and len(filtered) != line_count:
                    msg = f"line_count expected {line_count} got {len(filtered)}"
                    return (
                        False,
                        msg,
                        {
                            "path": str(resolved),
                            "actual": len(filtered),
                        },
                        _make_failure(
                            ctx,
                            name="jsonl",
                            expected={"line_count": line_count},
                            actual={"line_count": len(filtered)},
                            message=msg,
                        ),
                    )

                if assert_each is not None:
                    for idx, row in enumerate(filtered):
                        if not assert_each(row):
                            msg = f"assert_each failed at index {idx}"
                            return (
                                False,
                                msg,
                                {
                                    "path": str(resolved),
                                    "row_index": idx,
                                },
                                _make_failure(
                                    ctx,
                                    name="jsonl",
                                    expected={"assert_each": "predicate true"},
                                    actual=dict(row),
                                    message=msg,
                                ),
                            )

                if assert_any is not None and not any(assert_any(r) for r in filtered):
                    msg = "assert_any predicate satisfied by no row"
                    return (
                        False,
                        msg,
                        {"path": str(resolved)},
                        _make_failure(
                            ctx,
                            name="jsonl",
                            expected={"assert_any": "any matching row"},
                            actual=[dict(r) for r in filtered],
                            message=msg,
                        ),
                    )

                return (
                    True,
                    "jsonl assertions satisfied",
                    {
                        "path": str(resolved),
                        "rows_inspected": len(filtered),
                    },
                    None,
                )

            return _timed_result("jsonl", _build)

        return _named_callable("jsonl", _run)

    # ---- COMP-010.3 -------------------------------------------------------

    @staticmethod
    def settings_json(
        *,
        path: str | Path,
        key_path: str,
        equals: Any = _SENTINEL,
        exists: Optional[bool] = None,
    ) -> ExpectCallable:
        """Assert ``settings.json`` shape (COMP-010.3).

        ``path`` resolves against :attr:`EvalContext.home_path` so a
        manifest can address the per-eval ``settings.json`` as
        ``"settings.json"`` regardless of whether the real ``~/.claude``
        exists on the host.

        ``key_path`` is a dot-separated traversal expression (e.g.
        ``"hooks.matchers"``). ``equals`` performs strict equality on
        the resolved value; ``exists`` asserts presence/absence of the
        key path.
        """

        def _run(ctx: EvalContext) -> ExpectResult:
            def _build() -> tuple[
                bool, str, Mapping[str, Any], Optional[ExpectFailure]
            ]:
                resolved = _resolve_path(ctx, path)
                if not resolved.exists():
                    msg = f"settings.json not found at {resolved}"
                    return (
                        False,
                        msg,
                        {"path": str(resolved)},
                        _make_failure(
                            ctx,
                            name="settings_json",
                            expected={"settings_json_present": True},
                            actual={"settings_json_present": False},
                            message=msg,
                        ),
                    )

                try:
                    payload = json.loads(resolved.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    return (
                        False,
                        f"settings.json invalid JSON: {exc}",
                        {
                            "path": str(resolved),
                        },
                        _make_failure(
                            ctx,
                            name="settings_json",
                            expected="valid JSON",
                            actual=resolved.read_text(
                                encoding="utf-8", errors="replace"
                            ),
                            message=str(exc),
                            exc=exc,
                        ),
                    )

                found = True
                value: Any = payload
                for segment in key_path.split("."):
                    if isinstance(value, Mapping) and segment in value:
                        value = value[segment]
                    else:
                        found = False
                        value = None
                        break

                if exists is not None and found != bool(exists):
                    msg = (
                        f"key_path {key_path!r} exists={found}, expected {bool(exists)}"
                    )
                    return (
                        False,
                        msg,
                        {
                            "path": str(resolved),
                            "key_path": key_path,
                            "found": found,
                        },
                        _make_failure(
                            ctx,
                            name="settings_json",
                            expected={"key_path": key_path, "exists": bool(exists)},
                            actual={"key_path": key_path, "exists": found},
                            message=msg,
                        ),
                    )

                if equals is not _SENTINEL:
                    if not found:
                        msg = f"key_path {key_path!r} missing; cannot compare"
                        return (
                            False,
                            msg,
                            {
                                "path": str(resolved),
                                "key_path": key_path,
                            },
                            _make_failure(
                                ctx,
                                name="settings_json",
                                expected=equals,
                                actual=None,
                                message=msg,
                            ),
                        )
                    if value != equals:
                        msg = f"key_path {key_path!r} value mismatch"
                        return (
                            False,
                            msg,
                            {
                                "path": str(resolved),
                                "key_path": key_path,
                                "actual": value,
                            },
                            _make_failure(
                                ctx,
                                name="settings_json",
                                expected=equals,
                                actual=value,
                                message=msg,
                            ),
                        )

                return (
                    True,
                    "settings.json assertions satisfied",
                    {
                        "path": str(resolved),
                        "key_path": key_path,
                        "found": found,
                    },
                    None,
                )

            return _timed_result("settings_json", _build)

        return _named_callable("settings_json", _run)

    # ---- COMP-010.4 -------------------------------------------------------

    @staticmethod
    def exit_code(
        equals: Any = _SENTINEL,
        in_set: Optional[Iterable[int]] = None,
        not_equals: Optional[int] = None,
    ) -> ExpectCallable:
        """Assert the subprocess exit code (COMP-010.4).

        Default behaviour asserts ``equals=0``. ``equals`` and ``in_set``
        are mutually exclusive — supplying both raises ``ValueError`` at
        primitive construction time. ``not_equals`` may be combined with
        either.
        """

        # Detect explicit ``equals=`` so the default value (0) does not
        # trip the mutual-exclusion guard when a manifest writes
        # ``{exit_code: {in_set: [0, 1]}}``.
        explicit_equals = equals is not _SENTINEL
        effective_equals: Optional[int] = equals if explicit_equals else 0

        if explicit_equals and in_set is not None:
            raise ValueError(
                "Expect.exit_code: 'equals' and 'in_set' are mutually exclusive"
            )

        normalized_set: Optional[frozenset[int]] = (
            frozenset(in_set) if in_set is not None else None
        )

        def _run(ctx: EvalContext) -> ExpectResult:
            def _build() -> tuple[
                bool, str, Mapping[str, Any], Optional[ExpectFailure]
            ]:
                code = ctx.exit_code

                if normalized_set is not None:
                    if code not in normalized_set:
                        msg = f"exit_code {code} not in {sorted(normalized_set)}"
                        return (
                            False,
                            msg,
                            {"actual": code},
                            _make_failure(
                                ctx,
                                name="exit_code",
                                expected={"in_set": sorted(normalized_set)},
                                actual=code,
                                message=msg,
                            ),
                        )
                elif effective_equals is not None and code != effective_equals:
                    msg = f"exit_code expected {effective_equals} got {code}"
                    return (
                        False,
                        msg,
                        {"actual": code},
                        _make_failure(
                            ctx,
                            name="exit_code",
                            expected=effective_equals,
                            actual=code,
                            message=msg,
                        ),
                    )

                if not_equals is not None and code == not_equals:
                    msg = f"exit_code expected != {not_equals}, got {code}"
                    return (
                        False,
                        msg,
                        {"actual": code},
                        _make_failure(
                            ctx,
                            name="exit_code",
                            expected={"not_equals": not_equals},
                            actual=code,
                            message=msg,
                        ),
                    )

                return True, f"exit_code={code}", {"actual": code}, None

            return _timed_result("exit_code", _build)

        return _named_callable("exit_code", _run)

    # ---- COMP-010.5 -------------------------------------------------------

    @staticmethod
    def stderr(
        contains: Optional[str] = None,
        regex: Optional[str] = None,
        not_contains: Optional[str] = None,
    ) -> ExpectCallable:
        """Assert ANSI-stripped stderr matches a pattern (COMP-010.5)."""

        return _stream_predicate(
            name="stderr",
            source=lambda ctx: ctx.stderr,
            contains=contains,
            regex=regex,
            not_contains=not_contains,
        )

    @staticmethod
    def stdout(
        contains: Optional[str] = None,
        regex: Optional[str] = None,
        not_contains: Optional[str] = None,
    ) -> ExpectCallable:
        """Assert ANSI-stripped stdout matches a pattern (COMP-010.5)."""

        return _stream_predicate(
            name="stdout",
            source=lambda ctx: ctx.stdout,
            contains=contains,
            regex=regex,
            not_contains=not_contains,
        )

    # ---- COMP-010.6 -------------------------------------------------------

    @staticmethod
    def duration(
        max_sec: Optional[float] = None,
        min_sec: Optional[float] = None,
    ) -> ExpectCallable:
        """Assert the eval duration within bounds (COMP-010.6).

        Behaviour matrix:

        * Both bounds unset → informational PASS; records the duration.
        * ``max_sec`` only → FAIL when ``duration > max_sec``.
        * ``min_sec`` only → FAIL when ``duration < min_sec``.
        * Both bounds set → FAIL when either bound is violated.
        """

        def _run(ctx: EvalContext) -> ExpectResult:
            def _build() -> tuple[
                bool, str, Mapping[str, Any], Optional[ExpectFailure]
            ]:
                observed = ctx.duration_sec
                details: dict[str, Any] = {"observed_sec": observed}

                if max_sec is not None and observed > max_sec:
                    msg = f"duration {observed:.3f}s exceeds max_sec {max_sec}"
                    return (
                        False,
                        msg,
                        details,
                        _make_failure(
                            ctx,
                            name="duration",
                            expected={"max_sec": max_sec},
                            actual=observed,
                            message=msg,
                        ),
                    )

                if min_sec is not None and observed < min_sec:
                    msg = f"duration {observed:.3f}s below min_sec {min_sec}"
                    return (
                        False,
                        msg,
                        details,
                        _make_failure(
                            ctx,
                            name="duration",
                            expected={"min_sec": min_sec},
                            actual=observed,
                            message=msg,
                        ),
                    )

                if max_sec is None and min_sec is None:
                    return (
                        True,
                        f"duration={observed:.3f}s (informational)",
                        details,
                        None,
                    )

                return True, f"duration={observed:.3f}s within bounds", details, None

            return _timed_result("duration", _build)

        return _named_callable("duration", _run)

    # ---- Declarative form -------------------------------------------------

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> ExpectCallable:
        """Resolve a YAML ``expects:`` row to an :data:`ExpectCallable`.

        The mapping must have exactly one key, matching one of
        :data:`PRIMITIVE_NAMES`. The associated value is forwarded as
        keyword arguments to the primitive::

            {"exit_code": {"equals": 0}}
            -> Expect.exit_code(equals=0)

        Empty value mappings invoke the primitive with no arguments
        (relevant for ``exit_code`` whose default is ``equals=0``).
        """

        if len(mapping) != 1:
            raise ValueError(
                "Expect.from_mapping requires exactly one primitive key; "
                f"got {sorted(mapping)!r}"
            )
        ((key, value),) = mapping.items()
        if key not in PRIMITIVE_NAMES:
            raise ValueError(
                f"Unknown Expect primitive {key!r}; valid names are {PRIMITIVE_NAMES!r}"
            )

        kwargs: Mapping[str, Any] = value if isinstance(value, Mapping) else {}
        primitive = getattr(cls, key)
        return primitive(**kwargs)


def _stream_predicate(
    *,
    name: str,
    source: Callable[[EvalContext], str],
    contains: Optional[str],
    regex: Optional[str],
    not_contains: Optional[str],
) -> ExpectCallable:
    """Shared predicate engine for :meth:`Expect.stdout` / :meth:`Expect.stderr`."""

    compiled = re.compile(regex) if regex is not None else None

    def _run(ctx: EvalContext) -> ExpectResult:
        def _build() -> tuple[bool, str, Mapping[str, Any], Optional[ExpectFailure]]:
            buf = _strip_ansi(source(ctx))

            if contains is not None and contains not in buf:
                msg = f"{name} missing substring {contains!r}"
                return (
                    False,
                    msg,
                    {"stream": name},
                    _make_failure(
                        ctx,
                        name=name,
                        expected={"contains": contains},
                        actual=buf,
                        message=msg,
                    ),
                )

            if compiled is not None and compiled.search(buf) is None:
                msg = f"{name} did not match regex {regex!r}"
                return (
                    False,
                    msg,
                    {"stream": name},
                    _make_failure(
                        ctx,
                        name=name,
                        expected={"regex": regex},
                        actual=buf,
                        message=msg,
                    ),
                )

            if not_contains is not None and not_contains in buf:
                msg = f"{name} unexpectedly contained {not_contains!r}"
                return (
                    False,
                    msg,
                    {"stream": name},
                    _make_failure(
                        ctx,
                        name=name,
                        expected={"not_contains": not_contains},
                        actual=buf,
                        message=msg,
                    ),
                )

            return True, f"{name} predicates satisfied", {"stream": name}, None

        return _timed_result(name, _build)

    return _named_callable(name, _run)
