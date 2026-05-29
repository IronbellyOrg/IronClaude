"""Manifest loader entry points for the cliEval suite pipeline.

Roadmap FR-SCH1 / Deliverable D-0004 (Task T01.04).

This module exposes :func:`validate_manifest`, the single entry point used by
both ``eval doctor`` (T01.13) and ``eval run`` (M2 commands) to turn a
``suites/*.yaml`` manifest into a list of :class:`~superclaude.cli.eval.models.EvalSpec`
records *before any filesystem write occurs*.

Validation pipeline (per design-spec §5 / FR-SCH1):

1. Read the manifest from disk as raw bytes and decode YAML.
2. Validate the decoded mapping against ``suite.schema.json`` (DM-011,
   T01.02) using ``jsonschema``'s Draft 2020-12 validator.
3. On any violation raise :class:`SchemaError` with a stable field-path
   message; the CLI catches it and exits with :data:`SCHEMA_ERROR_EXIT_CODE`
   (= 2 per the harness exit-code table in design-spec §4).
4. On success, project every ``evals[]`` entry through
   ``EvalSpec.from_dict()`` and return the resulting list.

What this module is **not** responsible for:

* FR-SCH2 eval-id regex enforcement — lives in :func:`validate_eval_id`
  (T01.05) and is applied by the SuiteLoader orchestrator (T01.07) both
  pre- and post-parameterize-expansion.
* Capability resolution and parameterize expansion — also COMP-002 (T01.07).
* Any filesystem write (artifact dirs, scratch HOMEs, log files).
  Callers MUST treat ``validate_manifest`` as a pure read so that schema
  rejections cannot leak partial state onto disk (NFR-SEC1 invariant).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, runtime_checkable

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from . import exit_codes as _exit_codes
from .artifact_layout import EVAL_ID_PATTERN as EVAL_ID_REGEX
from .models import EvalSpec
from .suites import SCHEMA_PATH

__all__ = [
    "CapabilityResolver",
    "EVAL_ID_REGEX",
    "INVALID_EVAL_ID_EXIT_CODE",
    "InvalidEvalId",
    "ParsedSuite",
    "PermissiveCapabilityResolver",
    "SCHEMA_ERROR_EXIT_CODE",
    "SUITE_LOADER_ERROR_EXIT_CODE",
    "SchemaError",
    "SuiteLoader",
    "SuiteLoaderError",
    "UNRESOLVED_CAPABILITY_EXIT_CODE",
    "UnresolvedCapability",
    "validate_eval_id",
    "validate_manifest",
]


SCHEMA_ERROR_EXIT_CODE: int = _exit_codes.USAGE_ERROR
"""Process exit code emitted when :class:`SchemaError` reaches the CLI boundary.
Design-spec §4 ``2``. Canonical value: ``exit_codes.USAGE_ERROR`` (CC2 / OQ-2).
"""


INVALID_EVAL_ID_EXIT_CODE: int = _exit_codes.USAGE_ERROR
"""Process exit code emitted when :class:`InvalidEvalId` reaches the CLI boundary.
FR-SCH2 / NFR-SEC1 ``2``. Canonical value: ``exit_codes.USAGE_ERROR`` (CC2 / OQ-2).
"""


"""Compiled FR-SCH2 eval-id regex (single source of truth for the runtime guard).

Per CC1 / OQ-1, the canonical declaration lives in
``artifact_layout.EVAL_ID_PATTERN``; :data:`EVAL_ID_REGEX` is an import alias
preserved for backward-compat with ``tests/cli/eval/test_eval_id_regex.py``
and any external callers that imported from ``loader``.

Matches the literal regex declared in design-spec §5 and mirrored by the
``evalIdString`` ``pattern`` inside ``suite.schema.json`` (T01.02). The
pattern accepts canonical eval ids (``E1``, ``E15``, ``D15``) and
parameterize-expanded ids (``E2.1``, ``E2.10``) while rejecting:

* Path-traversal patterns: ``../home``, ``/etc``, ``..``, ``./foo``.
* Embedded separators: ``foo/bar``, ``foo\\bar``, ``E1/x``.
* Empty strings and leading-digit ids (``1E``, ``9``).
* Template tokens that leaked past parameterize expansion
  (``{{prefix}}``, ``${var}``).

The pattern is compiled at module import (in ``artifact_layout``) so the
loader hot path (one :func:`validate_eval_id` call per eval, plus one per
parameterize-expanded id) avoids re-parsing on every check.
"""


class InvalidEvalId(Exception):
    """Raised when an eval id fails the FR-SCH2 regex.

    The guard is applied in two places by COMP-002 ``SuiteLoader`` (T01.07):

    1. At loader entry, against every static id in the manifest. (The
       schema layer rejects malformed static ids too, but the runtime
       guard is the authoritative check the security model relies on.)
    2. After parameterize expansion, against every generated id (``E2.1``,
       ``E2.2``, ...). This closes the path-traversal attack surface
       where a parameterize substitution could otherwise inject ``..`` or
       ``/`` into an id that then gets interpolated into
       ``home_root / eval_id / home`` by ``HomeIsolation``.

    The exception MUST raise before any filesystem write (NFR-SEC1
    invariant) and the CLI MUST map it to :data:`INVALID_EVAL_ID_EXIT_CODE`
    (= 2).

    Attributes:
        eval_id: The exact value that failed the regex. Stored as the
            original input (``repr``-rendered in :meth:`__str__`) so
            reporters can show the offending payload verbatim — including
            quotes around whitespace or empty values — without losing
            forensic detail.
    """

    def __init__(self, eval_id: Any) -> None:
        self.eval_id = eval_id
        super().__init__(
            f"eval id failed FR-SCH2 regex ({EVAL_ID_REGEX.pattern!r}): {eval_id!r}"
        )


def validate_eval_id(eval_id: str) -> None:
    """Enforce the FR-SCH2 eval-id regex.

    The function is a pure guard: it returns ``None`` on success and
    raises :class:`InvalidEvalId` otherwise. No filesystem access, no
    logging, no globals touched — so callers can apply it freely on
    the hot path without worrying about side effects.

    Args:
        eval_id: The eval identifier to check. Schema-valid manifests
            already constrain this to a string at the schema layer, but
            the runtime guard does its own type check so callers that
            bypass the schema (e.g., post-parameterize expansion code
            paths) cannot accidentally smuggle non-string scalars
            through.

    Raises:
        InvalidEvalId: Raised when ``eval_id`` is not a ``str`` or when
            it does not match :data:`EVAL_ID_REGEX`. The exception
            carries the offending value on :attr:`InvalidEvalId.eval_id`
            and MUST be mapped by the CLI boundary to
            :data:`INVALID_EVAL_ID_EXIT_CODE` (= 2).
    """

    # Type guard first so YAML scalars that decode to int/bool/None cannot
    # bypass the regex check via duck typing.
    if not isinstance(eval_id, str):
        raise InvalidEvalId(eval_id)

    if EVAL_ID_REGEX.fullmatch(eval_id) is None:
        raise InvalidEvalId(eval_id)


@dataclass(frozen=True)
class _Violation:
    """One jsonschema error projected into a stable, log-friendly shape."""

    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


class SchemaError(Exception):
    """Raised when a manifest fails ``suite.schema.json`` validation.

    The exception carries the manifest path, every collected
    :class:`jsonschema.exceptions.ValidationError` projected into a
    field-path / message pair, and a pre-rendered multi-line ``message``
    suitable for stderr. The CLI maps this to exit code
    :data:`SCHEMA_ERROR_EXIT_CODE` (= 2).

    Attributes:
        manifest_path: Filesystem path of the manifest that failed.
        violations: Tuple of ``(json_path, error_message)`` pairs, one per
            jsonschema error. Order is deterministic (sorted by JSON path)
            so reporter output is stable across runs.
    """

    def __init__(
        self,
        manifest_path: Path,
        violations: Iterable[_Violation],
    ) -> None:
        self.manifest_path = manifest_path
        self.violations: tuple[tuple[str, str], ...] = tuple(
            (v.path, v.message) for v in violations
        )
        lines = [f"Manifest schema validation failed: {manifest_path}"]
        lines.extend(f"  - {path}: {msg}" for path, msg in self.violations)
        super().__init__("\n".join(lines))


def _format_json_path(error: ValidationError) -> str:
    """Render a jsonschema error path as ``$.evals[0].id`` notation.

    ``$`` denotes the manifest root so the top-level key for a missing
    required field is also reportable (jsonschema leaves ``absolute_path``
    empty in that case and stores the field name in ``message``).
    """

    if not error.absolute_path:
        return "$"
    parts: list[str] = ["$"]
    for segment in error.absolute_path:
        if isinstance(segment, int):
            parts.append(f"[{segment}]")
        else:
            parts.append(f".{segment}")
    return "".join(parts)


def _load_schema() -> Mapping[str, Any]:
    return yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))


def _read_manifest(path: Path) -> Mapping[str, Any]:
    """Decode the YAML manifest at ``path``.

    The read is a pure ``open(...).read()`` — no scratch directories or
    artifact paths are touched. YAML decode errors surface as
    :class:`SchemaError` so CLI callers only have to handle a single
    typed error to honour FR-SCH1.
    """

    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        violation = _Violation(path="$", message=f"manifest file not found: {exc}")
        raise SchemaError(path, (violation,)) from exc
    except OSError as exc:
        violation = _Violation(path="$", message=f"manifest read failed: {exc}")
        raise SchemaError(path, (violation,)) from exc

    try:
        decoded = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        violation = _Violation(path="$", message=f"YAML decode failed: {exc}")
        raise SchemaError(path, (violation,)) from exc

    if not isinstance(decoded, Mapping):
        violation = _Violation(
            path="$",
            message=(
                "manifest must decode to a mapping at the top level; "
                f"got {type(decoded).__name__}"
            ),
        )
        raise SchemaError(path, (violation,))

    return decoded


def _validate_manifest_dict(path: Path) -> Mapping[str, Any]:
    """Read ``path``, decode YAML, and validate against ``suite.schema.json``.

    Returns the raw manifest mapping (suite envelope + ``evals[]``) so
    callers that need suite-level metadata (``name``, ``version``,
    ``required_binaries``, etc.) — notably :class:`SuiteLoader` — do not
    have to re-read or re-parse the file. This is the single ingress
    point for FR-SCH1: every schema rejection raised inside the loader
    flows through here.
    """

    manifest = _read_manifest(path)

    schema = _load_schema()
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(manifest),
        key=lambda e: (list(e.absolute_path), e.message),
    )
    if errors:
        violations = [
            _Violation(path=_format_json_path(err), message=err.message)
            for err in errors
        ]
        raise SchemaError(path, violations)

    return manifest


def validate_manifest(path: Path | str) -> list[EvalSpec]:
    """Validate ``path`` against ``suite.schema.json`` and return parsed evals.

    Args:
        path: Filesystem path to a ``suites/*.yaml`` manifest. ``str`` is
            accepted for ergonomics; the value is normalised to ``Path``.

    Returns:
        A list of :class:`EvalSpec` instances, one per ``evals[]`` entry
        in the manifest. Order matches the manifest order so downstream
        report ordering is deterministic.

    Raises:
        SchemaError: Raised when the manifest cannot be read, cannot be
            decoded as YAML, decodes to a non-mapping, or violates any
            constraint in ``suite.schema.json``. The exception carries
            one violation entry per jsonschema error, each annotated
            with a ``$.path.to.field`` JSON path. CLI callers MUST map
            this to :data:`SCHEMA_ERROR_EXIT_CODE` (= 2).
    """

    manifest_path = Path(path)
    manifest = _validate_manifest_dict(manifest_path)
    return [EvalSpec.from_dict(entry) for entry in manifest["evals"]]


# ---------------------------------------------------------------------------
# COMP-002 SuiteLoader (T01.07 / D-0006)
# ---------------------------------------------------------------------------


UNRESOLVED_CAPABILITY_EXIT_CODE: int = _exit_codes.USAGE_ERROR
"""Process exit code emitted when :class:`UnresolvedCapability` reaches the CLI.
Third member of the SuiteLoader error trio. Canonical value:
``exit_codes.USAGE_ERROR`` (CC2 / OQ-2).
"""


SUITE_LOADER_ERROR_EXIT_CODE: int = _exit_codes.USAGE_ERROR
"""Single canonical exit code for every :class:`SuiteLoaderError` subclass.

``SuiteLoader`` only ever exits with ``2`` because every loader-layer
failure is, from the operator's point of view, "the harness refused to
start running the suite". The per-class constants
(:data:`SCHEMA_ERROR_EXIT_CODE`, :data:`INVALID_EVAL_ID_EXIT_CODE`,
:data:`UNRESOLVED_CAPABILITY_EXIT_CODE`) are kept so callers can branch on
intent without coupling the failure classes; this constant is the
aggregate ``SuiteLoader``-boundary alias used by CLI tests.
"""


class UnresolvedCapability(Exception):
    """Raised when a required capability cannot be satisfied at load time.

    Surfaced by :class:`SuiteLoader` after :func:`validate_eval_id` has
    accepted every static id but before parameterize expansion runs. The
    exception names the capabilities that failed so reporters can render
    them verbatim; CLI callers MUST map this to
    :data:`UNRESOLVED_CAPABILITY_EXIT_CODE` (= 2).

    Attributes:
        eval_id: The eval whose ``requires`` clause could not be
            satisfied.
        missing: Tuple of capability names that the injected
            :class:`CapabilityResolver` rejected.
    """

    def __init__(self, eval_id: str, missing: Iterable[str]) -> None:
        self.eval_id = eval_id
        self.missing: tuple[str, ...] = tuple(missing)
        missing_list = ", ".join(self.missing) if self.missing else "<none>"
        super().__init__(
            f"eval {eval_id!r} requires unresolved capabilities: {missing_list}"
        )


# Convenience alias so callers can catch any loader-layer failure with a
# single ``except SuiteLoaderError`` clause. We intentionally do not make
# the three concrete classes inherit from a new base — the per-class
# subclassing already keeps them disjoint, and a base class would force
# downstream callers (and existing tests) to deal with a new ABC.
SuiteLoaderError = (SchemaError, InvalidEvalId, UnresolvedCapability)


@runtime_checkable
class CapabilityResolver(Protocol):
    """Pluggable contract the SuiteLoader uses to gate ``requires`` clauses.

    The Protocol intentionally has a single method so the M1 SuiteLoader
    can be wired before COMP-009 ``CapabilityGates`` (T01.11) lands. The
    real implementation arriving in T01.11 inspects PATH + MCP reachability
    + ``--no-mcp`` flags and either returns the set of unresolved
    capability names (which the loader turns into
    :class:`UnresolvedCapability`) or returns an empty iterable.

    Test code injects a stub that records its calls so the "id-check
    happens BEFORE capability resolution" acceptance criterion can be
    verified by call-order assertion rather than by side-effects.
    """

    def resolve(
        self,
        eval_id: str,
        required: tuple[str, ...],
    ) -> Iterable[str]:
        """Return the subset of ``required`` that could not be satisfied.

        Implementations MUST be pure with respect to the SuiteLoader
        invariants: no filesystem writes, no globals touched. Returning
        an empty iterable means every capability is satisfied; any
        non-empty iterable is bubbled up by the loader as
        :class:`UnresolvedCapability`.
        """
        ...


class PermissiveCapabilityResolver:
    """Default :class:`CapabilityResolver` that approves every requirement.

    Used by :class:`SuiteLoader` when the caller does not inject a real
    resolver — tests and ``eval doctor``'s dry runs both benefit from a
    no-op default. The real ``CapabilityGates`` implementation lands in
    T01.11 and is wired through ``commands.py`` (T01.13).
    """

    def resolve(
        self,
        eval_id: str,
        required: tuple[str, ...],
    ) -> Iterable[str]:
        return ()


@dataclass(frozen=True)
class ParsedSuite:
    """Schema-validated, capability-checked, parameterize-expanded suite.

    The :class:`SuiteLoader.load` return shape. Every field is a verbatim
    projection of the manifest envelope except ``evals``, which holds the
    *expanded* eval list (parameterize rows materialised into one
    ``EvalSpec`` per row, with ``.{index}``-suffixed ids).

    Sequence fields are tuples so the dataclass is hashable and downstream
    consumers cannot mutate them through the container.
    """

    name: str
    version: str
    description: str
    defaults: Mapping[str, Any]
    required_binaries: tuple[Mapping[str, Any], ...]
    optional_capabilities: tuple[Mapping[str, Any], ...]
    evals: tuple[EvalSpec, ...]
    source_path: Path


@dataclass
class SuiteLoader:
    """COMP-002 orchestrator: turn a manifest path into a :class:`ParsedSuite`.

    The gate ordering is fixed and documented in
    ``artifacts/D-0006/spec.md`` (T01.07):

    1. **Read + schema** (``_validate_manifest_dict``) — FR-SCH1.
    2. **Static id regex** (``validate_eval_id`` on every ``evals[].id``) —
       FR-SCH2 / NFR-SEC1. Runs BEFORE capability resolution so a
       traversal-pattern id cannot trigger ``shutil.which`` calls or
       network MCP-reachability probes.
    3. **Capability resolution** (the injected :class:`CapabilityResolver`)
       — COMP-009 contract surface.
    4. **Parameterize expansion** — generate ``E2.1, E2.2, ...`` from
       ``parameterize:`` rows, base-id suffixed by ``.{index}``.
    5. **Expanded-id regex re-check** (``validate_eval_id`` again) —
       the load-bearing FR-SCH2 application that closes the
       expansion-time path-traversal surface.

    Every typed error (``SchemaError``, ``InvalidEvalId``,
    ``UnresolvedCapability``) is allowed to propagate as-is so CLI
    callers map it to :data:`SUITE_LOADER_ERROR_EXIT_CODE` (= 2) and
    emit the error class name on stderr — operators see *which* gate
    fired without us collapsing the failure classes.

    The class is intentionally a plain dataclass with one composed
    field (the resolver) rather than a long ``__init__`` parameter list,
    so future T01.14 (ExpectDSL) wiring can be added as additional
    optional fields without breaking call sites.
    """

    capability_resolver: CapabilityResolver = field(
        default_factory=PermissiveCapabilityResolver
    )

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------

    def load(self, path: Path | str) -> ParsedSuite:
        """Run the five-stage gate chain and return a :class:`ParsedSuite`.

        Args:
            path: Filesystem path to a ``suites/*.yaml`` manifest. ``str``
                accepted for ergonomics; normalised to ``Path``.

        Returns:
            A :class:`ParsedSuite` whose ``evals`` tuple holds the
            post-parameterize-expansion eval list. Suite-level metadata
            is verbatim from the manifest envelope so callers do not
            need to re-read the file to access ``required_binaries``,
            ``defaults``, etc.

        Raises:
            SchemaError: Manifest read / YAML decode / jsonschema
                violation. Exit-mapped via
                :data:`SCHEMA_ERROR_EXIT_CODE`.
            InvalidEvalId: A static or post-expansion eval id failed
                :func:`validate_eval_id`. Exit-mapped via
                :data:`INVALID_EVAL_ID_EXIT_CODE`. Raised BEFORE any
                capability resolution call (verified by mocked test).
            UnresolvedCapability: The injected
                :class:`CapabilityResolver` rejected one or more
                ``requires`` entries. Exit-mapped via
                :data:`UNRESOLVED_CAPABILITY_EXIT_CODE`.
        """

        manifest_path = Path(path)

        # Stage 1+2: schema and read. Re-uses validate_manifest's
        # ingress so any FR-SCH1 rejection flows through one code path.
        manifest = _validate_manifest_dict(manifest_path)
        raw_evals = manifest["evals"]

        # Stage 3: FR-SCH2 static id guard. Apply to every manifest id
        # BEFORE we touch the capability resolver — see the spec.md
        # "ordering rationale" section for why this matters
        # (CapabilityGates can shell out via shutil.which / MCP probes).
        for entry in raw_evals:
            validate_eval_id(entry.get("id"))

        # Stage 4: capability resolution. Each eval's ``requires`` list
        # is funnelled through the injected resolver; the first eval
        # with unresolved capabilities short-circuits the load.
        for entry in raw_evals:
            self._check_capabilities(entry)

        # Stage 5: parameterize expansion + post-expansion id re-check.
        # Static ids without ``parameterize`` are passed through; ids
        # with ``parameterize`` produce one expanded EvalSpec per row.
        expanded: list[EvalSpec] = []
        for entry in raw_evals:
            expanded.extend(self._expand_entry(entry))

        return ParsedSuite(
            name=manifest["name"],
            version=manifest["version"],
            description=manifest["description"],
            defaults=manifest.get("defaults", {}),
            required_binaries=tuple(manifest.get("required_binaries", ())),
            optional_capabilities=tuple(manifest.get("optional_capabilities", ())),
            evals=tuple(expanded),
            source_path=manifest_path,
        )

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _check_capabilities(self, entry: Mapping[str, Any]) -> None:
        """Funnel one eval's ``requires`` clause through the resolver."""

        required = tuple(entry.get("requires", ()))
        missing = tuple(self.capability_resolver.resolve(entry["id"], required))
        if missing:
            raise UnresolvedCapability(eval_id=entry["id"], missing=missing)

    def _expand_entry(self, entry: Mapping[str, Any]) -> list[EvalSpec]:
        """Materialise ``parameterize`` rows into one ``EvalSpec`` per row.

        Expansion convention (design-spec §5):

        * Base id with no ``parameterize`` → one ``EvalSpec`` with the
          static id unchanged.
        * Base id with N ``parameterize`` rows → N ``EvalSpec`` rows
          whose ids are ``{base}.{1..N}``.

        Each expanded id is re-checked against :func:`validate_eval_id`
        before it returns — this is the load-bearing FR-SCH2 application
        that the security model relies on. The current 1-based index
        convention is safe by construction (digits-only suffix), but
        the guard is mandatory because future expansion strategies
        (e.g., named indices) could leak unsafe characters.

        Substitution of ``{{key}}`` tokens inside other fields is the
        runtime layer's responsibility, not the loader's: the schema
        already constrained per-row keys to ``^[A-Za-z_][A-Za-z0-9_]*$``,
        so any token a row carries is safe to interpolate later. The
        loader's job is to preserve the row data on the expanded
        ``EvalSpec`` (currently round-tripped via ``EvalSpec.from_dict``
        keeping ``parameterize`` populated) so the runner can apply
        substitutions per-id.
        """

        parameterize_rows = entry.get("parameterize", ())
        if not parameterize_rows:
            return [EvalSpec.from_dict(entry)]

        expanded: list[EvalSpec] = []
        base_id = entry["id"]
        for index, _row in enumerate(parameterize_rows, start=1):
            expanded_id = f"{base_id}.{index}"
            # FR-SCH2 re-check — see method docstring for rationale.
            validate_eval_id(expanded_id)
            expanded_entry = dict(entry)
            expanded_entry["id"] = expanded_id
            expanded.append(EvalSpec.from_dict(expanded_entry))
        return expanded
