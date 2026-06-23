"""Capability dataclasses for the cliEval harness.

* ``Capability``        — DM-007 / D-0008 (Task T01.09): descriptor for a
  single precondition the harness checks before running evals.
* ``CapabilityStatus``  — DM-008 helper: per-capability outcome carried in
  ``CapabilityReport.report``.
* ``CapabilityReport``  — DM-008 / D-0009 (Task T01.10): aggregate report
  produced by COMP-009 ``CapabilityGates.check_all`` and consumed by
  ``eval doctor`` (T01.13) and the run pre-flight.

``Capability`` 5-field contract (DM-007):

* ``name``         — capability identifier (e.g. ``binary.claude``).
* ``check``        — zero-arg callable returning ``True`` when the
  capability is satisfied. The callable is evaluated by
  ``CapabilityGates.check_all`` (not at descriptor construction time).
* ``failure_mode`` — one of ``"hard"``, ``"skip"``, ``"xfail"``. ``hard``
  aborts the run; ``skip`` marks gated evals as ``SKIPPED``; ``xfail``
  marks them as expected-fail (see design-spec §11 "Three tiers of gates").
* ``skip_flag``    — optional CLI flag (e.g. ``--no-mcp``) that forces
  soft-skip behaviour even when the check would otherwise pass.
* ``description``  — human-readable label for the doctor output.

``CapabilityReport`` 6-field contract (DM-008):

* ``report``         — tuple of ``CapabilityStatus`` entries, one per
  capability that was evaluated.
* ``blocked_evals``  — eval ids gated off by a failing or skip-flagged
  capability.
* ``skip_flags``     — CLI flags currently active (e.g. ``("--no-mcp",)``).
* ``hard_failures``  — names of capabilities classified ``hard`` that
  failed; doctor must exit 2 when this is non-empty.
* ``soft_skips``     — names of capabilities classified ``skip`` that
  failed or were skip-flagged.
* ``soft_xfails``    — names of capabilities classified ``xfail`` that
  failed (gated evals run as expected-fail).

Gate evaluation, MCP reachability checks, and CLI wiring all live in
``CapabilityGates`` below (COMP-009 / T01.11) and the ``eval doctor``
subcommand (T01.13).
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Literal, Optional

FailureMode = Literal["hard", "skip", "xfail"]
_VALID_FAILURE_MODES: frozenset[str] = frozenset({"hard", "skip", "xfail"})


@dataclass(frozen=True)
class Capability:
    """Descriptor for a single capability check.

    Equality is structural across all 5 fields (``@dataclass``-generated
    ``__eq__``). Instances are hashable only when ``check`` is hashable —
    ``shutil.which`` lambdas typically are, but callers should not rely on
    Capability being a dict key.

    Construction with an invalid ``failure_mode`` raises ``ValueError``
    via ``__post_init__`` so a typo in a manifest or in the static
    ``CAPABILITIES`` list fails loudly at import time rather than at gate
    evaluation time.
    """

    name: str
    check: Callable[[], bool]
    failure_mode: FailureMode
    skip_flag: Optional[str] = None
    description: str = ""

    def __post_init__(self) -> None:
        if self.failure_mode not in _VALID_FAILURE_MODES:
            raise ValueError(
                f"Capability.failure_mode must be one of "
                f"{sorted(_VALID_FAILURE_MODES)!r}; got {self.failure_mode!r}"
            )


@dataclass(frozen=True)
class CapabilityStatus:
    """Per-capability outcome carried in ``CapabilityReport.report``.

    Mirrors the doctor green-checklist row: name, pass/fail bit, failure
    mode (so consumers know how the harness will react), human-readable
    description, and an optional ``detail`` (e.g. resolved binary path or
    the error message that explains the failure). ``skipped_by_flag`` is
    ``True`` when the capability would have passed but was forced down by
    the descriptor's ``skip_flag`` (e.g. ``--no-mcp``).
    """

    name: str
    passed: bool
    failure_mode: FailureMode
    description: str = ""
    detail: str = ""
    skipped_by_flag: bool = False

    def __post_init__(self) -> None:
        if self.failure_mode not in _VALID_FAILURE_MODES:
            raise ValueError(
                f"CapabilityStatus.failure_mode must be one of "
                f"{sorted(_VALID_FAILURE_MODES)!r}; got {self.failure_mode!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "failure_mode": self.failure_mode,
            "description": self.description,
            "detail": self.detail,
            "skipped_by_flag": self.skipped_by_flag,
        }


@dataclass(frozen=True)
class CapabilityReport:
    """Aggregate capability-gate result (DM-008).

    Tuples are used instead of lists so the dataclass remains hashable and
    a populated ``CapabilityReport`` cannot be mutated after construction.
    The six tuple fields map 1:1 to the field list named in DM-008; the
    ``report`` field carries structured ``CapabilityStatus`` entries while
    the other five carry plain identifiers (capability names or eval ids /
    CLI flags) so they can be diffed and serialised cheaply.
    """

    report: tuple[CapabilityStatus, ...] = field(default_factory=tuple)
    blocked_evals: tuple[str, ...] = field(default_factory=tuple)
    skip_flags: tuple[str, ...] = field(default_factory=tuple)
    hard_failures: tuple[str, ...] = field(default_factory=tuple)
    soft_skips: tuple[str, ...] = field(default_factory=tuple)
    soft_xfails: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, Any]:
        """Return a JSON-serialisable mapping per DM-008.

        Keys are emitted in the same order as the dataclass fields so the
        ``eval doctor --json`` payload is stable across invocations. List
        ordering inside each field is preserved as supplied by the caller
        — downstream doctor snapshot tests (T01.13) may sort independently
        if byte-level determinism is required.
        """
        return {
            "report": [status.to_dict() for status in self.report],
            "blocked_evals": list(self.blocked_evals),
            "skip_flags": list(self.skip_flags),
            "hard_failures": list(self.hard_failures),
            "soft_skips": list(self.soft_skips),
            "soft_xfails": list(self.soft_xfails),
        }


# ---------------------------------------------------------------------------
# COMP-009 CapabilityGates (T01.11 / D-0010)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _CapabilitySpec:
    """Static descriptor of one capability the harness checks.

    Internal to this module — keeps the binary lookup target and the
    classification metadata together so :class:`CapabilityGates` can
    build ``Capability`` instances and ``CapabilityStatus`` rows from a
    single source of truth without repeating the binary name.
    """

    name: str
    target: str
    kind: Literal["binary", "mcp_server"]
    failure_mode: FailureMode
    skip_flag: Optional[str]
    description: str


# Roster ordering matches design-spec §11 (HARD binaries first, then
# SOFT-SKIP MCP servers). ``CapabilityGates`` emits ``report[]`` rows in
# this order, which is what gives ``eval doctor`` (T01.13) its stable
# green-checklist layout.
_DEFAULT_CAPABILITY_SPECS: tuple[_CapabilitySpec, ...] = (
    _CapabilitySpec(
        "binary.claude",
        "claude",
        "binary",
        "hard",
        None,
        "Claude CLI on PATH",
    ),
    _CapabilitySpec(
        "binary.make",
        "make",
        "binary",
        "hard",
        None,
        "GNU make on PATH",
    ),
    _CapabilitySpec(
        "binary.jq",
        "jq",
        "binary",
        "hard",
        None,
        "jq JSON processor on PATH",
    ),
    _CapabilitySpec(
        "binary.git",
        "git",
        "binary",
        "hard",
        None,
        "git VCS on PATH",
    ),
    _CapabilitySpec(
        "mcp_server.auggie",
        "auggie",
        "mcp_server",
        "skip",
        "--no-mcp",
        "Auggie MCP server reachable",
    ),
    _CapabilitySpec(
        "mcp_server.auggie-mcp",
        "auggie-mcp",
        "mcp_server",
        "skip",
        "--no-mcp",
        "auggie-mcp MCP server reachable",
    ),
    _CapabilitySpec(
        "mcp_server.airis-mcp-gateway",
        "airis-mcp-gateway",
        "mcp_server",
        "skip",
        "--no-mcp",
        "AIRIS MCP gateway reachable",
    ),
    _CapabilitySpec(
        "mcp_server.tavily",
        "tavily",
        "mcp_server",
        "skip",
        "--no-mcp",
        "Tavily MCP server reachable",
    ),
)


# Type alias for the (passed, detail) tuple returned by per-target probes.
ProbeResult = tuple[bool, str]


class CapabilityGates:
    """COMP-009: evaluate every capability and emit a ``CapabilityReport``.

    The gate is constructed once per ``eval doctor`` / ``eval run``
    invocation. Pass the active CLI ``skip_flags`` (e.g. ``{"--no-mcp"}``)
    so SOFT-SKIP capabilities whose descriptor names a matching flag are
    forced to skipped status even when their underlying probe would pass.

    The class is purposely small: ``check_all`` drives the static
    :data:`_DEFAULT_CAPABILITY_SPECS` roster through :meth:`which_or_skip`
    or :meth:`mcp_server_reachable` and assembles the report. Tests
    inject a custom spec tuple via the ``capabilities`` keyword to mock
    PATH state without monkeypatching ``shutil``.

    OQ-5 (roadmap Open Questions): the precise ``mcp_server_reachable``
    contract (PATH presence vs handshake vs SSE probe) must be resolved
    before COMP-009 close at M2. The M1 implementation here uses PATH
    presence as the reachability signal — see :meth:`mcp_server_reachable`
    for the deferral note and the override hook.
    """

    def __init__(
        self,
        skip_flags: Optional[Iterable[str]] = None,
        capabilities: Optional[Iterable[_CapabilitySpec]] = None,
        mcp_probe: Optional[Callable[[str], ProbeResult]] = None,
    ) -> None:
        self._skip_flags: frozenset[str] = frozenset(skip_flags or ())
        self._specs: tuple[_CapabilitySpec, ...] = tuple(
            capabilities if capabilities is not None else _DEFAULT_CAPABILITY_SPECS
        )
        # Test hook so ``mcp_server_reachable`` can be redirected without
        # monkeypatching the module. Production callers leave this ``None``
        # and the default PATH-presence probe (OQ-5 M1 stub) is used.
        self._mcp_probe = mcp_probe

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------

    @property
    def skip_flags(self) -> tuple[str, ...]:
        """Active CLI skip flags, sorted for deterministic report output."""
        return tuple(sorted(self._skip_flags))

    def capabilities(self) -> tuple[Capability, ...]:
        """Materialise the static spec table as ``Capability`` instances.

        Each ``Capability.check`` is a closure that defers to
        :meth:`which_or_skip` / :meth:`mcp_server_reachable` so the
        descriptors stay in sync with the gate's own probing — there is no
        second copy of the lookup logic in the closures.
        """

        return tuple(self._make_capability(spec) for spec in self._specs)

    def which_or_skip(self, name: str) -> ProbeResult:
        """Probe whether binary ``name`` is on ``PATH``.

        Returns ``(True, "<resolved-path>")`` when ``shutil.which`` finds
        the binary, ``(False, "not found on PATH")`` otherwise. The
        ``detail`` half is carried verbatim onto the
        :class:`CapabilityStatus` row so ``eval doctor`` can print the
        resolved path on success or the failure reason on miss.
        """

        path = shutil.which(name)
        if path is None:
            return False, "not found on PATH"
        return True, path

    def mcp_server_reachable(self, name: str) -> ProbeResult:
        """Probe whether MCP server ``name`` is reachable.

        OQ-5 deferral: the canonical reachability semantics (PATH
        presence vs full stdio handshake vs SSE health probe) are open
        and must resolve before COMP-009 closes at M2. Until then, this
        implementation treats "binary on PATH" as the reachability
        signal because every MCP server in the default roster
        (``auggie``, ``auggie-mcp``, ``airis-mcp-gateway``) ships as an
        executable.

        Tests inject a custom probe via the ``mcp_probe`` constructor
        argument; the M2 follow-up will land a real handshake probe
        under the same signature.
        """

        if self._mcp_probe is not None:
            return self._mcp_probe(name)
        path = shutil.which(name)
        if path is None:
            return False, "MCP server binary not on PATH"
        return True, path

    def check_all(self) -> CapabilityReport:
        """Run every spec through its probe and assemble the report.

        Returns:
            A :class:`CapabilityReport` whose ``report`` tuple has one
            :class:`CapabilityStatus` row per spec in declaration order.
            ``hard_failures`` / ``soft_skips`` / ``soft_xfails`` carry
            the capability names that failed (or were skip-flagged) per
            their declared ``failure_mode``. ``blocked_evals`` is empty
            here — the SuiteLoader (T01.07) is the layer that knows
            which evals depend on which capability and populates that
            list at run time.

            Calling :meth:`check_all` twice on the same gate instance
            produces equal reports (idempotence is required by the
            T01.11 acceptance criteria; verified by
            ``test_check_all_is_idempotent``).
        """

        rows: list[CapabilityStatus] = []
        hard_failures: list[str] = []
        soft_skips: list[str] = []
        soft_xfails: list[str] = []

        for spec in self._specs:
            passed, detail = self._probe(spec)
            skipped_by_flag = False
            if spec.skip_flag is not None and spec.skip_flag in self._skip_flags:
                # SOFT-SKIP override: the user asked us to ignore this
                # capability tier regardless of probe result. The probe
                # detail is preserved so doctor output can still show
                # why the capability would have passed/failed without
                # the flag.
                skipped_by_flag = True
                passed = False

            rows.append(
                CapabilityStatus(
                    name=spec.name,
                    passed=passed,
                    failure_mode=spec.failure_mode,
                    description=spec.description,
                    detail=detail,
                    skipped_by_flag=skipped_by_flag,
                )
            )

            if not passed:
                if spec.failure_mode == "hard":
                    hard_failures.append(spec.name)
                elif spec.failure_mode == "skip":
                    soft_skips.append(spec.name)
                else:  # "xfail"
                    soft_xfails.append(spec.name)

        return CapabilityReport(
            report=tuple(rows),
            blocked_evals=(),
            skip_flags=self.skip_flags,
            hard_failures=tuple(hard_failures),
            soft_skips=tuple(soft_skips),
            soft_xfails=tuple(soft_xfails),
        )

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _probe(self, spec: _CapabilitySpec) -> ProbeResult:
        if spec.kind == "binary":
            return self.which_or_skip(spec.target)
        if spec.kind == "mcp_server":
            return self.mcp_server_reachable(spec.target)
        # Defensive — the Literal annotation prevents this at type-check
        # time, but the runtime guard keeps a typo in a custom spec
        # tuple from silently producing an always-passing row.
        raise ValueError(f"unknown capability kind: {spec.kind!r}")

    def _make_capability(self, spec: _CapabilitySpec) -> Capability:
        if spec.kind == "binary":

            def _check(target: str = spec.target) -> bool:
                return self.which_or_skip(target)[0]
        else:

            def _check(target: str = spec.target) -> bool:
                return self.mcp_server_reachable(target)[0]

        return Capability(
            name=spec.name,
            check=_check,
            failure_mode=spec.failure_mode,
            skip_flag=spec.skip_flag,
            description=spec.description,
        )
