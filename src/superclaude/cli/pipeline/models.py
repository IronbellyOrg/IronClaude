"""Pipeline data models -- shared dataclasses consumed by sprint and roadmap.

This module has zero imports from superclaude.cli.sprint or
superclaude.cli.roadmap (NFR-007). All types here are generic pipeline
primitives that both consumers extend.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Literal, Optional, Protocol


class CosmeticRemediator(Protocol):
    """Pluggable cosmetic-failure remediator (see cli/roadmap/cosmetic_remediator.py).

    Consumers of the generic pipeline executor may inject one via
    ``PipelineConfig.cosmetic_remediator``. The executor calls it after a gate
    fails to ask "can this be auto-fixed?" When the callable rewrites the file
    on disk such that the gate now passes, it returns ``(True, transforms)``
    and the executor records the step as PASS with ``remediated=True``.
    Returning ``(False, [])`` lets the executor proceed to FAIL/retry as
    before. Implementations MUST be idempotent (calling twice on the same
    rewritten artifact is a no-op).
    """

    def __call__(
        self,
        output_file: Path,
        gate_name: str,
        failure_reason: str,
        *,
        step_id: str,
    ) -> tuple[bool, list[str]]: ...


class StepStatus(Enum):
    """Lifecycle status of a single pipeline step."""

    PENDING = "PENDING"
    PASS = "PASS"
    FAIL = "FAIL"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    SKIPPED = "SKIPPED"

    @property
    def is_terminal(self) -> bool:
        return self in (
            StepStatus.PASS,
            StepStatus.FAIL,
            StepStatus.TIMEOUT,
            StepStatus.CANCELLED,
            StepStatus.SKIPPED,
        )

    @property
    def is_success(self) -> bool:
        return self == StepStatus.PASS

    @property
    def is_failure(self) -> bool:
        return self in (StepStatus.FAIL, StepStatus.TIMEOUT)


class GateMode(Enum):
    """Gating behavior for pipeline steps.

    BLOCKING: Step must pass before the next step can begin (default).
    TRAILING: Step runs but does not block subsequent steps; failures
              are evaluated after a grace period.
    """

    BLOCKING = "BLOCKING"
    TRAILING = "TRAILING"


@dataclass
class SemanticCheck:
    """Pure Python check applied to file content. No LLM invocation."""

    name: str
    check_fn: Callable[[str], bool | str]
    failure_message: str


@dataclass
class CodeAssertion:
    """Code-graph predicate applied at gate evaluation time (R1.3 / §MVR §2).

    Unlike ``SemanticCheck`` (which inspects the rendered string content of an
    output file), a ``CodeAssertion`` inspects the live code graph -- it may
    parse Python source via ``ast``, import callables, or walk module-level
    constants. The widened
    ``(PipelineEnvelope, Path) -> Finding | None`` signature is the
    BUILD-REQUEST §MVR §2 verbatim contract.

    ``PipelineEnvelope`` and ``Finding`` are referenced as string forward
    refs to preserve NFR-007 (``pipeline.*`` MUST NOT import from
    ``roadmap.*`` or ``sprint.*``). At runtime ``check_fn`` receives a
    ``PipelineEnvelope`` (defined in ``cli/roadmap/envelope.py``) and a
    repository-root ``Path``; it returns ``None`` on PASS or a typed
    ``Finding`` (defined in ``cli/roadmap/findings.py``) on FAIL with
    ``severity``/``description``/``location`` populated for downstream
    gate reporters.

    Return convention:
      None     -> PASS (the assertion held)
      Finding  -> FAIL (assertion violated)

    ``ci_only`` (R1.6 CI-vs-runtime split) classifies whether the predicate is
    safe to evaluate in the live gate path. A ``ci_only=True`` assertion
    inspects the *source tree* (e.g. an ``ast`` walk of ``src/superclaude/cli``)
    and therefore cannot run on a pipx-installed package, which ships no
    ``src/`` tree -- it is enforced exclusively by its dedicated CI test and is
    skipped by ``gate_passed`` even when the envelope is plumbed. The default
    ``ci_only=False`` marks a runtime-safe assertion (it inspects only the
    ``PipelineEnvelope`` state) that fires in the live path whenever a caller
    plumbs the envelope.
    """

    name: str
    check_fn: Callable[..., object]
    failure_message: str
    ci_only: bool = False


@dataclass
class GateCriteria:
    """Defines what constitutes a passing output for a pipeline step.

    ``required_frontmatter_fields`` accepts two entry shapes:
      * ``str`` — that exact top-level key must be present in the frontmatter.
      * ``tuple[str, ...]`` — an OR-group: at least one of the listed aliases
        must be present. Used when the template contract allows mutually
        exclusive aliases for the same slot (e.g. ``("spec_source",
        "spec_sources")`` for single-spec vs multi-spec roadmap artifacts).

    ``code_assertions`` is the R1.3 / §MVR §2 slot for code-graph predicates
    (AST walks, import-and-call). It is dispatched by
    ``cli/pipeline/gates.py:gate_passed`` AFTER all semantic_checks pass.
    Default ``None`` preserves backward compatibility with every existing
    ``GateCriteria(...)`` call site that pre-dates R1.3.
    """

    required_frontmatter_fields: list[str | tuple[str, ...]]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
    code_assertions: list[CodeAssertion] | None = None


@dataclass
class Step:
    """A single pipeline step."""

    id: str
    prompt: str
    output_file: Path
    gate: Optional[GateCriteria]
    timeout_seconds: int
    inputs: list[Path] = field(default_factory=list)
    retry_limit: int = 1
    model: str = ""
    gate_mode: GateMode = GateMode.BLOCKING
    tool_write_mode: bool = False
    template_path: Optional[Path] = None


@dataclass
class StepResult:
    """Outcome of executing a single pipeline step.

    ``remediated`` and ``remediations`` are populated when the cosmetic-failure
    auto-remediation lane (see ``cli/roadmap/cosmetic_remediator.py``) rewrote
    a gate-failing output into a gate-passing one. The step's ``status`` stays
    ``PASS`` so existing pattern-matching keeps working; downstream consumers
    that care about remediation (audit log, halt formatter, certify prompt)
    read these fields explicitly.
    """

    step: Optional[Step] = None
    status: StepStatus = StepStatus.PENDING
    attempt: int = 1
    gate_failure_reason: str | None = None
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    remediated: bool = False
    remediations: list[str] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()


class DeliverableKind(Enum):
    """Classification of deliverable type for decomposition and analysis."""

    IMPLEMENT = "implement"
    VERIFY = "verify"
    INVARIANT_CHECK = "invariant_check"
    FMEA_TEST = "fmea_test"
    GUARD_TEST = "guard_test"
    CONTRACT_TEST = "contract_test"

    @classmethod
    def from_str(cls, value: str) -> DeliverableKind:
        """Parse a string into a DeliverableKind, raising ValueError on unknown."""
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join(k.value for k in cls)
            raise ValueError(
                f"Unknown deliverable kind: {value!r}. Valid kinds: {valid}"
            )


@dataclass
class Deliverable:
    """A single deliverable within a pipeline step or roadmap task.

    Attributes:
        id: Unique identifier (e.g. 'D-0001', 'D-0001.a').
        description: Human-readable description of what this deliverable produces.
        kind: Classification for decomposition passes. Defaults to 'implement'
              for backward compatibility with pre-extension deliverables.
        metadata: Attachment point for analytical passes (M2-M4). Defaults to
                  empty dict. Round-trip serializable.
    """

    id: str
    description: str
    kind: DeliverableKind = DeliverableKind.IMPLEMENT
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to a dict for JSON round-trip."""
        return {
            "id": self.id,
            "description": self.description,
            "kind": self.kind.value,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Deliverable:
        """Deserialize from a dict. Pre-extension dicts without 'kind' default to 'implement'."""
        kind_str = data.get("kind", "implement")
        return cls(
            id=data["id"],
            description=data["description"],
            kind=DeliverableKind.from_str(kind_str),
            metadata=data.get("metadata", {}),
        )


@dataclass
class PipelineConfig:
    """Configuration shared by both sprint and roadmap pipelines.

    ``allow_cosmetic_remediation`` enables the cosmetic-failure auto-remediation
    lane in the generic executor: when a gate fails and the failure can be
    classified as purely cosmetic (heading shape, dash variant, whitespace,
    etc. -- see ``cli/roadmap/cosmetic_remediator.py``), the output is
    deterministically rewritten and re-checked before the step is marked FAIL.
    Defaults True for user-friendly behavior; set False (or pass
    ``--strict-no-remediation`` on the CLI) to preserve strict halt-on-any-
    failure for high-stakes runs.
    """

    work_dir: Path = field(default_factory=lambda: Path("."))
    dry_run: bool = False
    max_turns: int = 100
    model: str = ""
    permission_flag: str = "--dangerously-skip-permissions"
    debug: bool = False
    grace_period: int = 0
    allow_cosmetic_remediation: bool = True
    cosmetic_remediator: Optional[CosmeticRemediator] = None
