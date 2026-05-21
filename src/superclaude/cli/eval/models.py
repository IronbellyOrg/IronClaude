"""Data models for parsed cliEval manifests.

Roadmap DM-002 / Deliverable D-0003 (Task T01.03),
DM-009 / Deliverable D-0013 (Task T01.15),
DM-005 / Deliverable D-0014 (Task T01.16),
DM-001 / Deliverable D-0045 (Task T03.01),
DM-003 / Deliverable D-0046 (Task T03.02),
DM-010 / Deliverable D-0047 (Task T03.03), and
DM-004 / Deliverable D-0052 (Task T03.09).

``EvalSpec`` carries the 9 fields declared by the ``evalEntry`` shape in
``suite.schema.json`` (T01.02): ``id``, ``title``, ``category``, ``requires``,
``timeout_sec``, ``isolation``, ``inputs``, ``expects``, ``parameterize``.

``ExpectResult`` carries the 6 fields declared by DM-009: ``name``,
``passed``, ``message``, ``details``, ``duration_sec``, ``failure``. Every
``ExpectCallable`` (COMP-010 / T01.14 stubs in M1, primitives land in M4)
returns one of these so the Reporter (COMP-008 / T03.13) can render per-
Expect outcomes without re-parsing assertion messages.

``ExpectFailure`` carries the 8 fields declared by DM-005: ``eval_id``,
``expect_id``, ``expect_name``, ``expected``, ``actual``, ``message``,
``artifact_ref``, ``traceback``. The Reporter (COMP-008 / T03.13) renders
exactly one ``ExpectFailure`` per failing Expect inside ``EvalOutcome``
(T03.01).

Field names match the schema verbatim so round-tripping a manifest entry
through ``EvalSpec.from_dict()`` is deterministic. Sequence fields are stored
as tuples so equality is preserved and instances cannot be mutated through
their container (the dataclass itself is also frozen).

Parameterize expansion and FR-SCH2 id re-validation happen one layer up in
COMP-002 (T01.07); this module is intentionally schema-shape-only.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Literal, Mapping, Optional, get_args

if TYPE_CHECKING:  # pragma: no cover - import guard for type-checkers only.
    from .isolation import HomeIsolation


EvalStatus = Literal[
    "PASS",
    "FAIL",
    "ERRORED",
    "TIMEOUT",
    "INTERRUPTED",
    "SKIPPED",
    "XFAIL",
    "XPASS",
]
# Resolved tuple for runtime membership checks. Kept in module scope so the
# Reporter (COMP-008 / T03.13) and orchestrator can validate status values
# against the same authoritative set without re-deriving from the Literal.
EVAL_STATUSES: tuple[str, ...] = get_args(EvalStatus)


@dataclass(frozen=True)
class EvalSpec:
    """Parsed manifest entry (one row of ``evals[]``).

    Field shape mirrors ``evalEntry`` in ``suites/suite.schema.json``:

    * ``id`` / ``title`` are required by the schema.
    * ``category`` defaults to an empty string for unclassified evals.
    * ``requires`` is the tuple of capability names a runner must check.
    * ``timeout_sec`` is ``None`` when the manifest does not override the
      suite-wide default in ``EvalConfig.defaults``.
    * ``isolation`` carries the raw ``isolationBlock`` mapping; ``None``
      when omitted.
    * ``inputs`` / ``expects`` / ``parameterize`` are tuples of raw row
      mappings. Their interior shape is validated by ``suite.schema.json``;
      richer typed models land later (ExpectCallable in M4).
    """

    id: str
    title: str
    category: str = ""
    requires: tuple[str, ...] = ()
    timeout_sec: int | None = None
    isolation: Mapping[str, Any] | None = None
    inputs: tuple[Mapping[str, Any], ...] = ()
    expects: tuple[Mapping[str, Any], ...] = ()
    parameterize: tuple[Mapping[str, Any], ...] = ()
    no_pty: str | None = None
    # ``no_pty`` is the DOC-OQ3 / R-077 exclusion-set tag (schema enum
    # ``"skip"``); ``None`` when the manifest omitted the field. The
    # runner consults this tag when ``--no-pty`` is set on
    # ``superclaude eval run`` to short-circuit PTY-required evals with
    # status SKIPPED + skip_reason=``"--no-pty"`` before any HOME setup.

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EvalSpec":
        """Build an ``EvalSpec`` from a schema-valid manifest entry.

        The mapping keys mirror ``suite.schema.json`` field names. Sequence
        values (``requires``, ``inputs``, ``expects``, ``parameterize``) are
        normalised to tuples; nested mappings inside ``inputs`` / ``expects``
        / ``parameterize`` rows are passed through as-is (the schema already
        constrained their shape).

        Missing optional keys fall back to the dataclass defaults; ``id`` and
        ``title`` are required by the schema upstream so absence here is a
        contract bug rather than user error.
        """

        if "id" not in data or "title" not in data:
            raise ValueError(
                "EvalSpec.from_dict requires schema-validated input with 'id' and 'title'"
            )

        requires_raw = data.get("requires", ())
        inputs_raw = data.get("inputs", ())
        expects_raw = data.get("expects", ())
        parameterize_raw = data.get("parameterize", ())

        return cls(
            id=data["id"],
            title=data["title"],
            category=data.get("category", ""),
            requires=tuple(requires_raw),
            timeout_sec=data.get("timeout_sec"),
            isolation=data.get("isolation"),
            inputs=tuple(inputs_raw),
            expects=tuple(expects_raw),
            parameterize=tuple(parameterize_raw),
            no_pty=data.get("no_pty"),
        )


@dataclass(frozen=True)
class ExpectResult:
    """Assertion outcome returned by every ``ExpectCallable`` (DM-009).

    Six-field contract:

    * ``name``         — assertion name, matching the DSL method that emitted
      the result (e.g. ``"exit_code"``, ``"file.contains_event"``). Used by
      the Reporter (COMP-008 / T03.13) as a stable per-Expect key.
    * ``passed``       — ``True`` when the assertion was satisfied. The
      reporter rolls these up into the per-eval pass/fail bit.
    * ``message``      — human-readable one-liner suitable for the terminal
      summary; empty string when no message is required.
    * ``details``      — additional structured information (typically the
      diff fragments or matched event payload) carried through to the JSON
      report. Stored as an immutable ``Mapping`` so the frozen dataclass
      keeps its equality / hashability contract; an empty mapping is the
      default for passing results.
    * ``duration_sec`` — wall-clock seconds the assertion took to evaluate.
      Stored as ``float`` to capture sub-millisecond resolution.
    * ``failure``      — optional ``ExpectFailure`` (DM-005 / T01.16) carrying
      the diff-level detail for a failing assertion. ``None`` for passing
      results; DM-009 does not couple the failure presence to ``passed``, so
      callers must populate ``failure`` explicitly when they want the
      reporter to render a rich per-Expect failure block.

    Equality is structural across all six fields (``@dataclass``-generated
    ``__eq__``). The dataclass is frozen so once an ``ExpectCallable``
    returns a result it cannot be mutated by downstream consumers.
    """

    name: str
    passed: bool
    message: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)
    duration_sec: float = 0.0
    failure: Optional["ExpectFailure"] = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable mapping per DM-009.

        Uses ``dataclasses.asdict`` so nested dataclasses (notably
        ``ExpectFailure`` once T01.16 lands) are recursively unwrapped into
        plain dicts. ``details`` is shallow-copied to break the shared
        reference with the dataclass instance — callers that mutate the
        returned mapping must not affect the immutable source.
        """

        payload = dataclasses.asdict(self)
        # ``asdict`` already returns a fresh mapping, but ``details`` may
        # contain nested mutable containers (lists of event payloads, etc.).
        # We rely on ``asdict``'s recursive copy for that — no extra work
        # needed here. Keep this method as the one stable serialisation
        # surface so the Reporter can call it without touching internals.
        return payload


# Field order below mirrors DM-005 so ``to_dict()`` output is stable across
# Reporter snapshots and review diffs.
_EXPECT_FAILURE_FIELDS: tuple[str, ...] = (
    "eval_id",
    "expect_id",
    "expect_name",
    "expected",
    "actual",
    "message",
    "artifact_ref",
    "traceback",
)


@dataclass(frozen=True)
class ExpectFailure:
    """Per-Expect failure detail record (DM-005).

    The Reporter (COMP-008 / T03.13) attaches exactly one ``ExpectFailure``
    to each failing assertion inside ``EvalOutcome`` (T03.01). The 8-field
    contract intentionally mirrors the diff payload a human reviewer needs:

    * ``eval_id``     — id of the eval that produced the failure (already
      regex-guarded by FR-SCH2 / T01.05 upstream, so the reporter can use it
      verbatim in artifact filenames).
    * ``expect_id``   — stable per-Expect identifier such as
      ``"exit_code[0]"`` or ``"file.contains_event[2]"``; the reporter uses
      this to deduplicate failures across re-runs.
    * ``expect_name`` — DSL method name that emitted the failure (matches
      ``ExpectResult.name`` so the two records line up in the JSON report).
    * ``expected``    — assertion's expected value as supplied by the
      manifest. ``Any`` because primitives accept arbitrary JSON-shaped
      payloads (int exit codes, regex strings, structured event payloads).
    * ``actual``      — observed value the Expect saw on the run. Same
      typing rationale as ``expected``.
    * ``message``     — human-readable one-liner summarising the diff;
      defaults to ``""`` so a caller can omit it when the diff between
      ``expected`` / ``actual`` is self-explanatory.
    * ``artifact_ref`` — optional path-or-URI to a side-car artifact
      (rendered diff file, dumped JSONL, captured stderr). ``None`` when no
      artifact was written. The Reporter resolves the ref against the run's
      scratch root before emitting the JSON report.
    * ``traceback``   — optional Python traceback string captured when the
      Expect itself raised. ``None`` for assertion failures that produced a
      clean diff rather than an exception.

    The dataclass is frozen so a Reporter consumer cannot mutate failure
    records mid-render. Equality is structural across all 8 fields, which
    keeps deduplication straightforward.
    """

    eval_id: str
    expect_id: str
    expect_name: str
    expected: Any
    actual: Any
    message: str = ""
    artifact_ref: Optional[str] = None
    traceback: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable mapping per DM-005.

        Builds an explicit ordered dict from ``_EXPECT_FAILURE_FIELDS`` so
        the output ordering is stable regardless of Python version or
        dataclass internals. ``expected`` / ``actual`` are passed through
        as-is — callers populate them with JSON-shaped payloads, so the
        reporter can ``json.dumps`` the result directly.
        """

        return {name: getattr(self, name) for name in _EXPECT_FAILURE_FIELDS}


# Field order mirrors DM-001 verbatim so ``to_dict()`` output is stable
# across Reporter snapshots, JSON summaries, and review diffs.
_EVAL_OUTCOME_FIELDS: tuple[str, ...] = (
    "eval_id",
    "title",
    "status",
    "duration_sec",
    "expects",
    "skip_reason",
    "skip_flag_triggered",
    "artifacts",
    "error_class",
)


@dataclass(frozen=True)
class EvalOutcome:
    """Per-expanded-eval outcome record emitted by ``EvalRunner`` (DM-001).

    Nine-field contract consumed by the Reporter (COMP-008 / T03.13) and
    exit-code logic. The dataclass is frozen so once a runner emits an
    outcome it cannot be mutated by downstream consumers.

    * ``eval_id``             — id of the expanded eval. Already regex-guarded
      by FR-SCH2 (T01.05) so the Reporter can use it verbatim in artifact
      filenames and summary keys.
    * ``title``               — human-readable eval title (from ``EvalSpec``);
      copied onto the outcome so the Reporter does not need to re-resolve the
      manifest at render time.
    * ``status``              — one of the 8 ``EvalStatus`` literals: ``PASS``,
      ``FAIL``, ``ERRORED``, ``TIMEOUT``, ``INTERRUPTED``, ``SKIPPED``,
      ``XFAIL``, ``XPASS``. Validated in ``__post_init__``: any other value
      raises ``ValueError``.
    * ``duration_sec``        — wall-clock seconds the eval ran (lifecycle
      start to teardown). ``float`` for sub-millisecond resolution.
    * ``expects``             — tuple of ``ExpectResult`` records, one per
      assertion the eval evaluated. Stored as a tuple so the frozen dataclass
      preserves equality and hashability; an empty tuple is the default for
      ``SKIPPED`` outcomes (no assertions executed).
    * ``skip_reason``         — free-form reason string when ``status`` is
      ``SKIPPED`` (e.g. ``"capability 'mcp.tavily' unresolved"``). ``None``
      otherwise. DM-001 does not couple ``status == SKIPPED`` to a non-None
      reason — empty-skip rows are documented elsewhere (loader paths) and
      the model accepts both shapes.
    * ``skip_flag_triggered`` — name of the flag/capability that triggered
      the skip (e.g. ``"mcp.tavily"``, ``"--include-skipped"``). ``None``
      when the skip was not flag-driven.
    * ``artifacts``           — mapping of artifact-name to absolute (or
      run-relative) path produced by the eval. Stored as an immutable
      ``Mapping`` so the frozen dataclass keeps its hashability contract;
      an empty mapping is the default.
    * ``error_class``         — fully-qualified Python exception class name
      when ``status`` is ``ERRORED`` (e.g. ``"builtins.RuntimeError"``).
      ``None`` for non-error outcomes. The Reporter uses this to group
      identical harness failures across runs.

    Field declaration order matches DM-001 verbatim so ``to_dict()`` and
    ``dataclasses.asdict`` produce stable, reviewable JSON.
    """

    eval_id: str
    title: str
    status: EvalStatus
    duration_sec: float
    expects: tuple[ExpectResult, ...] = ()
    skip_reason: Optional[str] = None
    skip_flag_triggered: Optional[str] = None
    artifacts: Mapping[str, str] = field(default_factory=dict)
    error_class: Optional[str] = None

    def __post_init__(self) -> None:
        # Validate status membership against the authoritative literal set.
        # The acceptance criteria require "Invalid status raises ValueError;
        # valid statuses are exactly the 8 listed in DM-001" — a runtime
        # check is the cheapest enforcement that survives mypy being absent
        # at runtime and callers that build outcomes from dynamic strings
        # (e.g. JSON replay, partial summary on SIGINT).
        if self.status not in EVAL_STATUSES:
            raise ValueError(
                f"EvalOutcome.status must be one of {EVAL_STATUSES!r}; "
                f"got {self.status!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-serialisable mapping per DM-001.

        Builds an explicit ordered dict from ``_EVAL_OUTCOME_FIELDS`` so the
        output ordering is stable regardless of Python version or dataclass
        internals. Nested ``ExpectResult`` values are unwrapped via their
        own ``to_dict()`` so the Reporter can ``json.dumps`` the result
        directly without bespoke recursion. ``artifacts`` is shallow-copied
        into a plain ``dict`` so callers that mutate the returned mapping do
        not affect the immutable source.
        """

        payload: dict[str, Any] = {}
        for name in _EVAL_OUTCOME_FIELDS:
            value = getattr(self, name)
            if name == "expects":
                payload[name] = [item.to_dict() for item in value]
            elif name == "artifacts":
                payload[name] = dict(value)
            else:
                payload[name] = value
        return payload


# Field order mirrors DM-003 verbatim so ``to_dict()`` output is stable across
# Reporter snapshots, JSON summaries, and review diffs.
_EVAL_RESULT_FIELDS: tuple[str, ...] = (
    "eval_id",
    "outcome",
    "start",
    "end",
    "duration_sec",
    "stdout",
    "stderr",
    "artifacts",
    "error",
)


@dataclass(frozen=True)
class EvalResult:
    """Reporter-facing per-eval result record (DM-003).

    Nine-field contract consumed by COMP-008 Reporter (T03.13) as its primary
    per-eval input. Where ``EvalOutcome`` (DM-001 / T03.01) is the *runner
    emission* (status + assertions), ``EvalResult`` is the *reporter input*
    that carries the captured stdout/stderr, the start/end timestamps, and the
    harness-level error (if any). The pair travels together: runner builds an
    ``EvalOutcome`` and wraps it in an ``EvalResult`` for the Reporter.

    * ``eval_id``      — id of the expanded eval. Already regex-guarded by
      FR-SCH2 (T01.05) upstream so the Reporter can use it verbatim in
      artifact filenames and summary keys.
    * ``outcome``      — the ``EvalOutcome`` emitted by the runner (DM-001).
      Stored by-reference; the dataclass is frozen so the wrapped outcome
      cannot be swapped after construction.
    * ``start``        — ISO 8601 wall-clock timestamp marking the runner
      lifecycle start. Stored as ``str`` so the field round-trips through JSON
      without bespoke datetime serialization. The Reporter does not parse
      these strings — it forwards them verbatim into ``summary.json``.
    * ``end``          — ISO 8601 wall-clock timestamp marking lifecycle end
      (teardown complete). Same string-typing rationale as ``start``.
    * ``duration_sec`` — wall-clock seconds derived from ``end - start`` in
      ``__post_init__``. Any value supplied by the caller is overwritten so
      the field is *always* consistent with the timestamps. ``float`` for
      sub-millisecond resolution. When either timestamp is empty (e.g. an
      INTERRUPTED outcome captured before ``end`` was written) the supplied
      value is kept verbatim so partial summaries remain constructible.
    * ``stdout``       — captured stdout from the eval's PTY transcript.
      ``str`` for direct JSON emission; binary noise is already stripped by
      ``PtyStream`` (T02.17) upstream.
    * ``stderr``       — captured stderr from the eval. Same typing rationale
      as ``stdout``.
    * ``artifacts``    — mapping of artifact-name to absolute (or run-
      relative) path produced by the eval. Stored as an immutable ``Mapping``
      so the frozen dataclass keeps its hashability contract; an empty
      mapping is the default. ``to_dict()`` returns a shallow copy so callers
      that mutate the returned mapping do not affect the immutable source.
    * ``error``        — optional ``BaseException`` instance captured when the
      *harness* (not an assertion) raised. ``None`` for clean runs. The
      Reporter renders this as ``{"type": "<fqcn>", "message": "<str>"}`` in
      ``to_dict()``; the live exception instance is kept on the dataclass so
      diagnostic tools can inspect the traceback if it is still attached.

    Field declaration order matches DM-003 verbatim so ``to_dict()`` produces
    stable, reviewable JSON.
    """

    eval_id: str
    outcome: EvalOutcome
    start: str
    end: str
    duration_sec: float = 0.0
    stdout: str = ""
    stderr: str = ""
    artifacts: Mapping[str, str] = field(default_factory=dict)
    error: Optional[BaseException] = None

    def __post_init__(self) -> None:
        # DM-003 acceptance: ``duration_sec`` is computed from ``end - start``
        # consistently. We overwrite any caller-supplied value so the field
        # cannot drift from the timestamps it derives from. Empty strings are
        # tolerated (partial summaries on SIGINT may carry a start with no
        # end) — in that case we keep the caller's value untouched so the
        # Reporter can still emit a row.
        if self.start and self.end:
            computed = (
                datetime.fromisoformat(self.end) - datetime.fromisoformat(self.start)
            ).total_seconds()
            # Frozen dataclasses block ``self.duration_sec = ...``; the
            # documented escape hatch is ``object.__setattr__``.
            object.__setattr__(self, "duration_sec", computed)

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-serialisable mapping per DM-003.

        Builds an explicit ordered dict from ``_EVAL_RESULT_FIELDS`` so the
        output ordering is stable regardless of Python version or dataclass
        internals. ``outcome`` is unwrapped via ``EvalOutcome.to_dict()`` so
        the Reporter never has to recurse manually. ``artifacts`` is shallow-
        copied into a plain ``dict``. ``error`` is converted to a
        ``{"type": "<fqcn>", "message": "<str>"}`` mapping (or ``None``) so
        the payload remains JSON-serializable — bare ``BaseException``
        instances cannot pass through ``json.dumps``.
        """

        payload: dict[str, Any] = {}
        for name in _EVAL_RESULT_FIELDS:
            value = getattr(self, name)
            if name == "outcome":
                payload[name] = value.to_dict()
            elif name == "artifacts":
                payload[name] = dict(value)
            elif name == "error":
                payload[name] = _render_error(value)
            else:
                payload[name] = value
        return payload


def _render_error(error: Optional[BaseException]) -> Optional[dict[str, str]]:
    """Render an exception as a JSON-safe mapping.

    Returns ``None`` when no error was captured. Otherwise emits a two-key
    mapping with the fully-qualified class name and the ``str()`` rendering
    of the exception. We deliberately do *not* serialise the traceback here
    — the per-eval JSONL log (T03.05) is the authoritative traceback source;
    DM-003's ``error`` is the Reporter-facing summary handle.
    """

    if error is None:
        return None
    cls = type(error)
    qualified = f"{cls.__module__}.{cls.__qualname__}"
    return {"type": qualified, "message": str(error)}


# Field order mirrors DM-010 verbatim so attribute traversal, factory
# construction, and any future ``to_dict()`` consumer iterate in the same
# canonical order the roadmap row enumerates.
_EVAL_CONTEXT_FIELDS: tuple[str, ...] = (
    "eval_spec",
    "home",
    "home_path",
    "artifacts_dir",
    "run_dir",
    "env",
    "stdout_path",
    "stderr_path",
    "transcript_path",
    "jsonl_paths",
    "exit_code",
    "stdout",
    "stderr",
    "duration_sec",
    "artifacts",
)


@dataclass(frozen=True)
class EvalContext:
    """Runtime context passed to every ``ExpectCallable`` (DM-010).

    Fifteen-field immutable view fed to each assertion primitive
    (FR-EXP1 / T04.01) after the runner (FR-LC1 / T03.04) has finished
    spawning the Claude subprocess and captured its outputs. Every
    primitive ``Expect.file`` / ``Expect.jsonl`` / ``Expect.exit_code``
    receives this exact record so manifest authors get a stable shape
    regardless of which runner internal path produced the eval.

    Field declaration order matches DM-010 verbatim (see
    ``_EVAL_CONTEXT_FIELDS``) so structural traversal, JSON dumping by
    downstream tools, and review diffs stay deterministic.

    * ``eval_spec``       — parsed manifest row (DM-002 / T01.03). Stored
      by-reference; ``EvalSpec`` is itself frozen so the runner cannot
      mutate the spec after the context is built. ExpectCallables read
      ``eval_spec.id`` / ``eval_spec.expects`` / ``eval_spec.timeout_sec``
      directly off the context without having to re-thread the spec.
    * ``home``            — the per-eval ``HomeIsolation`` record
      (DM-006 / T02.04). Carries ``eval_id``, ``home_root``,
      ``session_id``, ``time_offset_sec`` and the COMP-006 method
      surface; ExpectCallables that need to call ``home.env()`` /
      ``home.state_path(...)`` (e.g. ``Expect.settings_json`` reading
      ``~/.claude/settings.json``) can do so without re-deriving the
      object.
    * ``home_path``       — the per-eval ``HOME`` directory created by
      :meth:`HomeIsolation.setup`. Stored as a separate ``Path`` so
      ExpectCallables that only need the path avoid the
      ``home.home_path`` property indirection (and the ``RuntimeError``
      it raises when setup has not run — by the time the context is
      built the setup has already completed). The factory keeps
      ``home.home_path == home_path`` invariant.
    * ``artifacts_dir``   — directory the runner writes per-eval
      artifacts under (PTY transcripts, hook outputs, captured
      side-cars). Resolved beneath ``home_path``; primitives that emit
      diff side-cars (``Expect.file`` / ``Expect.jsonl`` failures) drop
      them here.
    * ``run_dir``         — the run-scoped scratch directory the
      orchestrator created (FR-G2 / T03.16). One ``run_dir`` per
      ``superclaude eval run`` invocation; per-eval ``HOME``s and
      artifact directories live beneath it.
    * ``env``              — frozen mapping of environment variables that
      were exported to the Claude subprocess (the union of
      ``HomeIsolation.env()`` plus ``IsolationLayers.env_vars`` plus any
      caller overrides). Stored as a ``MappingProxyType`` so callers
      cannot mutate the record post-build; the factory wraps the supplied
      mapping in ``MappingProxyType`` to enforce this.
    * ``stdout_path``      — filesystem path of the captured stdout
      transcript (the PTY-stripped variant the ``PtyStream`` / T02.17
      wrote). ExpectCallables that need raw bytes (``Expect.stdout``)
      open this path.
    * ``stderr_path``      — same for stderr.
    * ``transcript_path``  — path to the raw PTY transcript (pre-strip,
      ANSI escapes preserved). Used by tooling that needs the byte-for-
      byte capture; ExpectCallables generally use ``stdout_path`` /
      ``stderr_path`` instead.
    * ``jsonl_paths``      — frozen mapping of named JSONL log file
      paths (e.g. ``{"hook_log": ..., "telemetry": ...}``). Per-eval
      runtime logs land here; ``Expect.jsonl(name="hook_log", ...)``
      resolves the path through this mapping. Stored as a
      ``MappingProxyType`` for the same immutability reason as ``env``.
    * ``exit_code``        — captured exit code of the Claude subprocess
      (``int``). The runner records the value the PTY driver observed
      after ``wait()``; ``Expect.exit_code`` reads it.
    * ``stdout``           — full captured stdout as a ``str``. Mirrors
      what ``stdout_path`` points at so ExpectCallables can read it
      in-memory without re-opening the file. Empty when no output was
      captured.
    * ``stderr``           — full captured stderr; same rationale as
      ``stdout``.
    * ``duration_sec``     — wall-clock seconds the eval body ran
      (subprocess spawn to exit). ``float`` for sub-millisecond
      resolution. ``Expect.duration`` reads this verbatim.
    * ``artifacts``        — frozen mapping of artifact-name to absolute
      (or run-relative) path produced by the eval. Mirrors
      ``EvalOutcome.artifacts`` (DM-001) — the post-run inventory the
      runner builds before emitting the outcome. Stored as a
      ``MappingProxyType`` so the context cannot be tampered with by
      ExpectCallables that share the record across primitives.

    The dataclass is ``frozen=True`` so any attempted ``ctx.foo = bar``
    raises :class:`dataclasses.FrozenInstanceError` — the contract every
    ExpectCallable can rely on. Mapping fields are additionally wrapped
    in :class:`types.MappingProxyType` to prevent the more subtle attack
    of mutating ``ctx.env["HOME"]`` (frozen-dataclass blocks
    ``__setattr__``, not method calls on field values).

    Use :meth:`from_runner_state` to construct an ``EvalContext`` from
    the runner's internal state; direct ``EvalContext(...)`` construction
    is permitted (tests build minimal contexts for ExpectCallable unit
    tests) but the factory is the single place runner-internal mappings
    are wrapped in ``MappingProxyType`` and the ``home.home_path ==
    home_path`` invariant is enforced.
    """

    eval_spec: "EvalSpec"
    home: "HomeIsolation"
    home_path: Path
    artifacts_dir: Path
    run_dir: Path
    env: Mapping[str, str]
    stdout_path: Path
    stderr_path: Path
    transcript_path: Path
    jsonl_paths: Mapping[str, Path]
    exit_code: int
    stdout: str
    stderr: str
    duration_sec: float
    artifacts: Mapping[str, str]

    def __post_init__(self) -> None:
        # Wrap mapping fields in MappingProxyType so callers that share
        # the context across ExpectCallables cannot mutate the underlying
        # mapping. Frozen-dataclass only blocks attribute assignment; the
        # mapping objects themselves stay mutable unless we proxy them.
        # ``object.__setattr__`` is the documented escape hatch.
        for name in ("env", "jsonl_paths", "artifacts"):
            value = getattr(self, name)
            if not isinstance(value, MappingProxyType):
                object.__setattr__(self, name, MappingProxyType(dict(value)))

    @classmethod
    def from_runner_state(
        cls,
        *,
        eval_spec: "EvalSpec",
        home: "HomeIsolation",
        run_dir: Path,
        artifacts_dir: Path,
        stdout_path: Path,
        stderr_path: Path,
        transcript_path: Path,
        jsonl_paths: Mapping[str, Path],
        env: Mapping[str, str],
        exit_code: int,
        stdout: str,
        stderr: str,
        duration_sec: float,
        artifacts: Mapping[str, str],
    ) -> "EvalContext":
        """Build an ``EvalContext`` from EvalRunner internal state.

        Centralises three concerns the runner would otherwise have to
        repeat for every emitted context:

        1. Resolves ``home_path`` off the ``HomeIsolation`` instance so
           the runner does not duplicate ``home.home_path`` at the call
           site. The property accessor raises
           :class:`RuntimeError` if :meth:`HomeIsolation.setup` has not
           run — which is exactly the failure we want surfaced at
           context construction (rather than later when an
           ExpectCallable reads ``ctx.home_path``).
        2. Wraps the three mapping arguments (``env``, ``jsonl_paths``,
           ``artifacts``) in :class:`types.MappingProxyType` so the
           context's mapping fields are read-only views of the runner's
           internal state. ``__post_init__`` would also wrap them, but
           doing it here keeps the wrap close to the call site for
           readability.
        3. Produces a deterministic instance: every ``EvalContext``
           built from the same arguments compares equal (the
           ``@dataclass``-generated ``__eq__`` covers the 15 fields; the
           mapping proxies compare equal when their underlying dicts do).

        Keyword-only arguments are required so future field additions
        (e.g. when DM-010 grows a 16th field) do not silently re-order
        positional callers.
        """

        return cls(
            eval_spec=eval_spec,
            home=home,
            home_path=home.home_path,
            artifacts_dir=artifacts_dir,
            run_dir=run_dir,
            env=MappingProxyType(dict(env)),
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            transcript_path=transcript_path,
            jsonl_paths=MappingProxyType(dict(jsonl_paths)),
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            duration_sec=duration_sec,
            artifacts=MappingProxyType(dict(artifacts)),
        )


# Field order mirrors the DM-012 ``counts`` sub-object verbatim so the
# Reporter's JSON output and any schema validator iterates in the same
# canonical order across runs.
_RUN_COUNTS_FIELDS: tuple[str, ...] = (
    "manifest_n",
    "expanded_n_prime",
    "kept_k",
    "skipped_s",
    "kept_plus_skipped_equals_n_prime",
)


@dataclass(frozen=True)
class RunCounts:
    """Counts sub-structure for ``RunSummary`` (DM-004 / DM-012).

    Five-field accounting record that captures the manifest expansion and
    skip pipeline so the Reporter (COMP-008 / T03.13) can enforce the
    ``len(evals[]) == counts.expanded_n_prime`` invariant FR-RPT1
    declares.

    * ``manifest_n``                       — number of rows in the source
      manifest before parameterize expansion.
    * ``expanded_n_prime``                 — number of expanded eval rows
      after parameterize expansion. Used as the ground-truth row count by
      the FR-RPT1 invariant guard.
    * ``kept_k``                           — number of expanded rows that
      ran end-to-end (status in ``{PASS,FAIL,ERRORED,TIMEOUT,XFAIL,XPASS}``).
    * ``skipped_s``                        — number of expanded rows that
      were skipped (status ``SKIPPED`` or ``INTERRUPTED``).
    * ``kept_plus_skipped_equals_n_prime`` — boolean assertion documented
      in DM-012 that the equation ``kept_k + skipped_s == expanded_n_prime``
      holds. ``RunSummary.__post_init__`` raises ``ValueError`` when the
      flag and the actual math disagree, so a misreporting orchestrator
      fails loudly instead of emitting an internally inconsistent summary.
    """

    manifest_n: int
    expanded_n_prime: int
    kept_k: int
    skipped_s: int
    kept_plus_skipped_equals_n_prime: bool

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable mapping per DM-012 counts sub-object.

        Builds an explicit ordered dict from ``_RUN_COUNTS_FIELDS`` so the
        output ordering is stable regardless of Python version or dataclass
        internals.
        """

        return {name: getattr(self, name) for name in _RUN_COUNTS_FIELDS}


# Field order mirrors the DM-012 ``totals`` sub-object verbatim.
_RUN_TOTALS_FIELDS: tuple[str, ...] = (
    "passed",
    "failed",
    "skipped",
    "errored",
    "interrupted",
    "timeout",
)


@dataclass(frozen=True)
class RunTotals:
    """Per-status tally sub-structure for ``RunSummary`` (DM-004 / DM-012).

    Six-field outcome tally that the Reporter surfaces in the headline of
    ``summary.md`` / ``summary.json``. Fields correspond to the
    ``EvalStatus`` literals that count toward a non-PASS outcome (XFAIL
    and XPASS roll into ``passed`` and ``failed`` respectively per the
    DM-012 schema).
    """

    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errored: int = 0
    interrupted: int = 0
    timeout: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable mapping per DM-012 totals sub-object."""

        return {name: getattr(self, name) for name in _RUN_TOTALS_FIELDS}


# Field order mirrors DM-004 verbatim so ``to_dict()`` output is stable
# across Reporter snapshots, JSON summaries, and review diffs.
_RUN_SUMMARY_FIELDS: tuple[str, ...] = (
    "run_id",
    "started_at",
    "finished_at",
    "duration_sec",
    "suite",
    "manifest_version",
    "parallel",
    "counts",
    "totals",
    "evals",
    "artifacts",
)


@dataclass(frozen=True)
class RunSummary:
    """Aggregate run summary record (DM-004).

    Eleven-field contract emitted by COMP-008 Reporter (T03.13) and the
    primary payload behind ``summary.md`` / ``summary.json`` (FR-RPT1 /
    T03.11). Carries the run-wide metadata, the per-status tally
    (``totals``), the row accounting (``counts``), and the per-eval rows
    (``evals``) the Reporter renders.

    * ``run_id``           — opaque identifier the orchestrator stamped on
      the run. Stable across artifacts and summary files so reviewers can
      join the per-eval JSONL logs against the aggregate summary.
    * ``started_at``       — ISO 8601 wall-clock timestamp marking the
      orchestrator start. Stored as ``str`` so the field round-trips
      through JSON without bespoke datetime serialisation.
    * ``finished_at``      — ISO 8601 wall-clock timestamp marking the
      orchestrator stop (after the last eval emitted its outcome). May be
      empty for partial summaries written on SIGINT before the
      orchestrator completed.
    * ``duration_sec``     — wall-clock seconds the orchestrator ran end
      to end. ``float`` for sub-millisecond resolution.
    * ``suite``            — manifest path / suite identifier the
      orchestrator loaded. The Reporter renders this verbatim in the
      summary header.
    * ``manifest_version`` — semantic version stamped on the manifest at
      author time. Helps the Reporter detect mismatched evals when a
      manifest is bumped between runs.
    * ``parallel``         — concurrency level the orchestrator scheduled
      at (post-clamp to ``[1,15]``). The Reporter surfaces this so
      reviewers can correlate the wall-clock budget against the scheduler
      knob.
    * ``counts``           — ``RunCounts`` instance (DM-012 counts sub-
      structure). ``__post_init__`` asserts the
      ``kept_k + skipped_s == expanded_n_prime`` equation matches the
      ``kept_plus_skipped_equals_n_prime`` flag; mismatched counts raise
      ``ValueError`` so a misreporting orchestrator fails loudly.
    * ``totals``           — ``RunTotals`` instance (DM-012 totals sub-
      structure). The 6 status tallies the Reporter renders in the
      summary headline.
    * ``evals``             — tuple of ``EvalOutcome`` records (DM-001 /
      T03.01), one per expanded spec. Stored as a tuple so the frozen
      dataclass preserves equality and hashability. FR-RPT1 (T03.11)
      enforces ``len(evals) == counts.expanded_n_prime`` *outside* this
      model so partial summaries (SIGINT) can still be constructed for
      writing.
    * ``artifacts``        — mapping of artifact-name to absolute (or
      run-relative) path produced by the orchestrator (e.g. the JSONL
      directory, the disk-budget breach side-car). Stored as an immutable
      ``Mapping`` so the frozen dataclass keeps its hashability contract;
      ``to_dict()`` returns a shallow copy so callers that mutate the
      returned mapping do not affect the immutable source.

    Field declaration order matches DM-004 verbatim (see
    ``_RUN_SUMMARY_FIELDS``) so ``to_dict()`` output is stable across
    Reporter snapshots and review diffs.
    """

    run_id: str
    started_at: str
    finished_at: str
    duration_sec: float
    suite: str
    manifest_version: str
    parallel: int
    counts: RunCounts
    totals: RunTotals
    evals: tuple[EvalOutcome, ...] = ()
    artifacts: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # DM-012 declares ``kept_plus_skipped_equals_n_prime`` as the
        # boolean assertion that the equation holds. We enforce that the
        # flag and the actual math agree at construction time so a
        # misreporting orchestrator cannot emit an internally inconsistent
        # summary: the FR-RPT1 invariant guard relies on
        # ``counts.expanded_n_prime`` being authoritative.
        actual = (
            self.counts.kept_k + self.counts.skipped_s == self.counts.expanded_n_prime
        )
        if self.counts.kept_plus_skipped_equals_n_prime != actual:
            raise ValueError(
                "RunSummary.counts.kept_plus_skipped_equals_n_prime claims "
                f"{self.counts.kept_plus_skipped_equals_n_prime!r} but "
                f"kept_k({self.counts.kept_k}) + skipped_s({self.counts.skipped_s}) "
                f"{'==' if actual else '!='} expanded_n_prime({self.counts.expanded_n_prime})"
            )

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-serialisable mapping per DM-004.

        Builds an explicit ordered dict from ``_RUN_SUMMARY_FIELDS`` so the
        output ordering is stable regardless of Python version or dataclass
        internals. Nested ``RunCounts`` / ``RunTotals`` / ``EvalOutcome``
        values are unwrapped via their own ``to_dict()`` so the Reporter
        never has to recurse manually. ``artifacts`` is shallow-copied
        into a plain ``dict`` so callers that mutate the returned mapping
        do not affect the immutable source.
        """

        payload: dict[str, Any] = {}
        for name in _RUN_SUMMARY_FIELDS:
            value = getattr(self, name)
            if name in ("counts", "totals"):
                payload[name] = value.to_dict()
            elif name == "evals":
                payload[name] = [item.to_dict() for item in value]
            elif name == "artifacts":
                payload[name] = dict(value)
            else:
                payload[name] = value
        return payload
