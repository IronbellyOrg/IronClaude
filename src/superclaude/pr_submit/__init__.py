"""Deterministic core for the ``sc:pr-submit`` PR-review auto-remediation monitor.

This underscored, importable package holds the pure decision logic the skill's
markdown orchestrator and bash glue defer to: the finite state machine
(:mod:`~superclaude.pr_submit.fsm`), the severity router
(:mod:`~superclaude.pr_submit.severity_router`), the loop-guard fence-post
(:mod:`~superclaude.pr_submit.loop_guard`), the three-state detection classifier
(:mod:`~superclaude.pr_submit.classifier` / :mod:`~superclaude.pr_submit.detection`),
the write-ahead JSONL run-log (:mod:`~superclaude.pr_submit.run_log`), the
crash-window recovery (:mod:`~superclaude.pr_submit.recovery`), and the shared
data models (:mod:`~superclaude.pr_submit.models`).

NFR-6 core purity: the modules in this package contain ZERO ``gh``/``git`` tokens.
All ``gh``/``git`` I/O lives in the skill's bash scripts and the SKILL.md VAL
validator; the core consumes already-fetched, already-classified data.

Top-level re-exports (``run_skill``, ``remap_severity``, ``poll_augment_review``,
``classify``) are wired incrementally as the modules land (see Step 4.3 / Step 5.1).
"""

from .classifier import STATE_DECLINED, classify, is_decline
from .detection import DetectionContract, DetectionContractLocked, poll_augment_review
from .fsm import RunConfig, evaluate_push_decision, parse_args, run_skill, transition
from .models import (
    EventType,
    Finding,
    MonitorState,
    PushDecision,
    Severity,
    SkillResult,
)
from .severity_router import remap_severity, route

# NOTE: ``load_fixture`` lives in ``tests/pr_submit/conftest.py`` (Phase 10) per the
# repo's fixture-helper precedent (research/04 §D: ``FIXTURES_DIR`` + ``load_fixture``
# in the test layer), NOT in this package's public API.

__all__ = [
    # detection / classification
    "classify",
    "is_decline",
    "STATE_DECLINED",
    "poll_augment_review",
    "DetectionContract",
    "DetectionContractLocked",
    # FSM
    "run_skill",
    "transition",
    "parse_args",
    "evaluate_push_decision",
    "RunConfig",
    # severity routing
    "remap_severity",
    "route",
    # models
    "EventType",
    "Finding",
    "MonitorState",
    "PushDecision",
    "Severity",
    "SkillResult",
]
