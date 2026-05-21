"""R3-mit retry-once policy module (T05.23 / D-0101).

Lands the additive retry-once branch reserved by NFR-REL2 (T03.08 /
D-0051): evals carrying the :data:`MCP_FLAKY_TAG` capability tag are
eligible for exactly one in-process retry when the first attempt
produces a non-PASS outcome. Non-tagged evals continue under the
NFR-REL2 default (zero retries — see ``docs/eval/retry.md``).

The policy is intentionally orthogonal to ``EvalRunner.retry_count``
which remains pinned at ``0``: the latter guards the orchestrator
N'-vs-K invariant (FR-RPT1 / T03.11) against an accidental caller
sweep, while ``RetryOncePolicy`` is opt-in per-eval and keyed off the
manifest tag the operator wrote.

The retry path records a ``mcp_server_flaky`` artifact on the final
outcome regardless of whether the retry recovered (PASS) or the
failure persisted (FAIL/ERRORED/TIMEOUT). The artifact is the
single forensic signal the Reporter (COMP-008 / T03.13) surfaces so
post-mortem tooling can identify retries without re-parsing the
per-eval JSONL log.

See ``artifacts/D-0101/spec.md`` for the per-task deliverable record.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import ClassVar, FrozenSet

from .models import EvalOutcome, EvalSpec

__all__ = [
    "MCP_FLAKY_TAG",
    "MCP_SERVER_FLAKY_ARTIFACT",
    "RetryOncePolicy",
    "is_mcp_flaky_tagged",
    "is_flaky_outcome",
]


# Canonical tag string the manifest carries on an MCP-flaky eval. Kept
# in module scope (and mirrored on ``EvalRunner.MCP_FLAKY_TAG``) so a
# future taxonomy change has a single source-of-truth pin.
MCP_FLAKY_TAG: str = "MCP-flaky"

# Canonical artifact key dropped onto ``EvalOutcome.artifacts`` after a
# retry-eligible failure has been observed. ``"true"`` is the only
# documented value; the Reporter renders the presence of the key, not
# its content.
MCP_SERVER_FLAKY_ARTIFACT: str = "mcp_server_flaky"

# Outcomes the retry policy treats as a candidate failure. ``SKIPPED``
# and ``INTERRUPTED`` are excluded because they signal "did not run"
# (capability gate / SIGINT) rather than "ran and failed under MCP
# flake". ``XFAIL`` / ``XPASS`` are excluded because they encode an
# expected-failure contract the policy does not re-interpret.
_FLAKY_STATUSES: FrozenSet[str] = frozenset({"FAIL", "ERRORED", "TIMEOUT"})


def is_mcp_flaky_tagged(spec: EvalSpec) -> bool:
    """Return ``True`` when ``spec`` carries the MCP-flaky tag.

    The tag lives in ``EvalSpec.requires`` for two reasons:

    1. The schema already accepts arbitrary strings there (one item
       per capability gate) so no schema migration is required.
    2. Manifest authors already think of ``requires:`` as "things this
       eval depends on" — flakiness is a property of the dependency
       set, not the eval body.

    A spec is considered MCP-flaky-tagged iff the canonical tag
    string :data:`MCP_FLAKY_TAG` appears in ``spec.requires``. Other
    capability strings present alongside are ignored — the tag is the
    sole signal.
    """

    return MCP_FLAKY_TAG in tuple(spec.requires)


def is_flaky_outcome(outcome: EvalOutcome) -> bool:
    """Return ``True`` when ``outcome.status`` is a retry candidate.

    Encodes the policy's failure taxonomy verbatim: only FAIL,
    ERRORED, and TIMEOUT are eligible for a retry attempt. PASS /
    SKIPPED / INTERRUPTED / XFAIL / XPASS are returned as-is by the
    caller (no retry).
    """

    return outcome.status in _FLAKY_STATUSES


@dataclass(frozen=True)
class RetryOncePolicy:
    """R3-mit retry-once policy (T05.23 / D-0101).

    The policy is a small immutable record the runner consults after
    each attempt. Two questions:

    * :meth:`is_eligible` — does the spec opt into the policy at all?
      (Answer: ``MCP_FLAKY_TAG`` is in ``spec.requires``.)
    * :meth:`should_retry` — did the *first* attempt's outcome warrant
      a retry? (Answer: eligible AND outcome is FAIL/ERRORED/TIMEOUT.)

    The runner is expected to track attempt count externally because
    the policy is stateless by design — a stateful policy would have
    to be reset between evals which is exactly the kind of bug
    NFR-REL2 was written to prevent. Callers MUST consult
    :meth:`should_retry` only on the first attempt's outcome; passing
    a retry attempt's outcome back through it would (correctly)
    return ``True`` again and loop forever.

    :meth:`annotate` returns a new ``EvalOutcome`` with the
    ``mcp_server_flaky`` artifact added. The original outcome is
    immutable (``EvalOutcome`` is a frozen dataclass) so callers must
    rebind to the return value.
    """

    MAX_ATTEMPTS: ClassVar[int] = 2
    """Total lifecycle attempts the runner is permitted under this
    policy: the original attempt plus exactly one retry."""

    flaky_tag: str = MCP_FLAKY_TAG
    artifact_name: str = MCP_SERVER_FLAKY_ARTIFACT

    def is_eligible(self, spec: EvalSpec) -> bool:
        """Return ``True`` when ``spec`` opts into the policy."""

        return self.flaky_tag in tuple(spec.requires)

    def should_retry(self, spec: EvalSpec, outcome: EvalOutcome) -> bool:
        """Return ``True`` when ``outcome`` warrants exactly one retry.

        Combines :meth:`is_eligible` with :func:`is_flaky_outcome` so
        callers have a single decision boundary. The runner pattern is:

            outcome = run_lifecycle(spec)
            if policy.should_retry(spec, outcome):
                outcome = policy.annotate(run_lifecycle(spec))
            return outcome
        """

        return self.is_eligible(spec) and is_flaky_outcome(outcome)

    def annotate(self, outcome: EvalOutcome) -> EvalOutcome:
        """Return ``outcome`` with the flaky-server artifact attached.

        The artifact key is added to ``outcome.artifacts`` (or left
        untouched if a key with the same name already exists, so the
        annotation is idempotent under re-application). The artifact's
        value is the literal string ``"true"`` — the Reporter
        surfaces the *presence* of the key, not its content.

        The returned outcome preserves every other field verbatim,
        including ``status``. The caller is responsible for deciding
        whether a recovered retry (PASS) should also carry the
        artifact; the policy answers "yes — the flake was real and
        retry covered it, surface that fact in the artifact map".
        """

        if self.artifact_name in outcome.artifacts:
            return outcome

        new_artifacts = dict(outcome.artifacts)
        new_artifacts[self.artifact_name] = "true"
        return replace(outcome, artifacts=new_artifacts)
