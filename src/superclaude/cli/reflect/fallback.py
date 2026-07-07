"""Tier-2 fallback ladder helpers for reflect.

Pure helpers appear first; ``run_fallback_ladder`` is the only impure controller.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from superclaude.cli.swarm.commands import ModelPoolTooSmallError
from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.models import (
    CallerMetadata,
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
    WorkerSpec,
)
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.cli.swarm.transports import Transport
from superclaude.cli.swarm.transports.openai_compat import TransportEnvError

from ._diversity import (
    _vendor_from_model_id,
    compute_model_class_diversity,
    compute_vendor_diversity,
)

if TYPE_CHECKING:
    from superclaude.cli.reflect.models import ReflectConfig

FallbackTransportFactory = Callable[[str], Transport]
FALLBACK_ELIGIBLE_STATUSES = frozenset({"timeout", "proxy_error", "parse_error"})
# Passthrough recipe: preserves the full reviewer body verbatim, identical to the
# primary Tier-2 seam (ensemble.REFLECT_REVIEW_RECIPE). Named locally so fallback.py
# never imports from reflect.ensemble (the cycle Phase 1 exists to break).
_REFLECT_REVIEW_RECIPE = "passthrough"
# Do not dispatch a fallback attempt with less than this many seconds left on the
# run deadline (§7.4 "a small floor"): starting an attempt with near-zero budget
# would only ever time out.
_FALLBACK_WALL_CLOCK_FLOOR_SEC = 1.0
TERMINAL_REASONS = (
    "not_needed_primary_quorum_met",
    "certified_t2_with_fallback",
    "fallback_config_missing",
    "fallback_pool_exhausted",
    "fallback_wall_clock_exhausted",
    "fallback_attempts_failed",
    "diversity_unrepairable",
    "no_fallback_eligible_primary_failure",
)
TIER2_CERTIFICATION_BASES = (
    "primary_only_quorum",
    "primary_plus_fallback_quorum",
    "not_certified",
)


@dataclass(frozen=True)
class FallbackDecision:
    """Output of the pure planner: whether to dispatch, which slot, why."""

    action: Literal["dispatch", "certified", "degraded"]
    slot: str | None
    reason: str


@dataclass(frozen=True)
class QuorumState:
    """Pure snapshot of the current contributing set vs the Tier-2 gate."""

    reviewer_count: int
    model_class_diversity: str
    vendor_diversity: str | None
    satisfies_tier2: bool


@dataclass(frozen=True)
class LadderOutcome:
    """Fallback ladder result handed back to the reflect ensemble.

    ``contributing_workers`` is the SMALLEST success subset that satisfies the
    Tier-2 gate — it feeds only the certification-basis telemetry, NOT the
    downstream worker accounting. ``all_workers`` is the FULL augmented worker
    set (every normalized primary — successes AND failures — plus every
    dispatched fallback attempt). The ensemble hands ``all_workers`` to
    ``reduce_wave3`` / ``build_reflect_contract`` so a healthy run where >2
    reviewers succeed is NOT mis-counted (feeding the trimmed subset would make
    ``determine_status`` see ``M < N`` and mark the swarm subrun ``partial``
    even though every primary succeeded).
    """

    contributing_workers: list[WorkerResult]
    attempt_ledger: list[dict]
    metadata: dict[str, Any]
    all_workers: list[WorkerResult] = field(default_factory=list)


def is_fallback_eligible(worker: WorkerResult) -> bool:
    """Return True when ``worker`` failed in a fallback-eligible way."""
    return worker.status in FALLBACK_ELIGIBLE_STATUSES


def build_fallback_metadata(
    *,
    ladder: tuple[str, ...],
    engaged: bool,
    attempt_ledger: list[dict],
    contributing_ids: list[str],
    primary_failures: list[str],
    terminal_reason: str,
    certification_basis: str,
    original_primary_pool_fully_succeeded: bool,
) -> dict[str, Any]:
    """Build the additive ``t2_fallback`` contract metadata block."""
    if terminal_reason not in TERMINAL_REASONS:
        raise ValueError(f"unknown fallback terminal_reason: {terminal_reason}")
    if certification_basis not in TIER2_CERTIFICATION_BASES:
        raise ValueError(
            f"unknown fallback tier2_certification_basis: {certification_basis}"
        )

    return {
        "enabled": True,
        "policy_version": "reflect-t2-fallback-ladder-v1",
        "strategy": "post_primary_quorum_top_up",
        "ladder": list(ladder),
        "engaged": engaged,
        "certified_with_fallback": certification_basis
        == "primary_plus_fallback_quorum",
        "fallback_attempt_count": sum(
            1 for attempt in attempt_ledger if attempt.get("role") == "fallback"
        ),
        "exhausted": terminal_reason
        in {"fallback_pool_exhausted", "fallback_attempts_failed"},
        "terminal_reason": terminal_reason,
        "original_primary_pool_fully_succeeded": original_primary_pool_fully_succeeded,
        "reviewer_attempts": attempt_ledger,
        "contributing_reviewer_attempt_ids": contributing_ids,
        "primary_failures_preserved": primary_failures,
        "tier2_certification_basis": certification_basis,
    }


def classify_outcomes(
    workers: list[WorkerResult],
) -> tuple[list[WorkerResult], list[WorkerResult]]:
    """Split workers into successes and fallback-eligible failures."""
    successes = [worker for worker in workers if worker.status == "success"]
    eligible_failures = [worker for worker in workers if is_fallback_eligible(worker)]
    return successes, eligible_failures


def evaluate_quorum(
    workers: list[WorkerResult], *, allow_single_vendor: bool
) -> QuorumState:
    """Evaluate the current workers against the unchanged Tier-2 gate."""
    successes = [worker for worker in workers if worker.status == "success"]
    reviewer_count = len(successes)
    model_class_diversity = compute_model_class_diversity(successes)
    vendor_diversity = compute_vendor_diversity(successes)
    satisfies_tier2 = (
        reviewer_count >= 2
        and model_class_diversity == "full"
        and (vendor_diversity == "multi" or allow_single_vendor)
    )
    return QuorumState(
        reviewer_count=reviewer_count,
        model_class_diversity=model_class_diversity,
        vendor_diversity=vendor_diversity,
        satisfies_tier2=satisfies_tier2,
    )


def plan_next_attempt(
    quorum: QuorumState,
    eligible_failures: list[WorkerResult],
    attempts_made: list[str],
    ladder: tuple[str, ...],
    *,
    fallback_available: dict[str, bool],
    wall_clock_ok: bool,
) -> FallbackDecision:
    """Plan the next fallback transition without performing I/O."""
    if quorum.satisfies_tier2:
        reason = (
            "certified_t2_with_fallback"
            if attempts_made
            else "not_needed_primary_quorum_met"
        )
        return FallbackDecision(action="certified", slot=None, reason=reason)

    if not wall_clock_ok:
        return FallbackDecision(
            action="degraded", slot=None, reason="fallback_wall_clock_exhausted"
        )

    if not eligible_failures:
        if quorum.reviewer_count >= 2 and (
            quorum.model_class_diversity != "full" or quorum.vendor_diversity != "multi"
        ):
            return FallbackDecision(
                action="degraded", slot=None, reason="diversity_unrepairable"
            )
        return FallbackDecision(
            action="degraded", slot=None, reason="no_fallback_eligible_primary_failure"
        )

    next_slot = next((slot for slot in ladder if slot not in attempts_made), None)
    if next_slot is None:
        return FallbackDecision(
            action="degraded", slot=None, reason="fallback_pool_exhausted"
        )
    if not fallback_available.get(next_slot, False):
        return FallbackDecision(
            action="degraded", slot=next_slot, reason="fallback_config_missing"
        )

    return FallbackDecision(action="dispatch", slot=next_slot, reason="dispatch")


def select_contributing_set(
    primaries: list[WorkerResult],
    fallback_successes: list[WorkerResult],
    *,
    allow_single_vendor: bool,
) -> list[WorkerResult]:
    """Select the smallest success set that satisfies the Tier-2 gate."""
    ordered_successes = [
        (worker, "primary") for worker in primaries if worker.status == "success"
    ] + [
        (worker, "fallback")
        for worker in fallback_successes
        if worker.status == "success"
    ]
    if not ordered_successes:
        return []

    for size in range(2, len(ordered_successes) + 1):
        candidates: list[tuple[int, tuple[int, ...], list[WorkerResult]]] = []
        for indices in combinations(range(len(ordered_successes)), size):
            workers = [ordered_successes[index][0] for index in indices]
            if evaluate_quorum(
                workers, allow_single_vendor=allow_single_vendor
            ).satisfies_tier2:
                primary_count = sum(
                    1 for index in indices if ordered_successes[index][1] == "primary"
                )
                candidates.append((-primary_count, indices, workers))
        if candidates:
            return sorted(candidates, key=lambda item: (item[0], item[1]))[0][2]

    return [worker for worker, _role in ordered_successes]


def make_fallback_slot_factory(
    pool: tuple[str, ...],
    ladder: tuple[str, ...],
    build_transport: Callable[[str], Transport],
) -> FallbackTransportFactory:
    """Bind fallback slot names to pool models by ladder position."""
    slot_to_model: dict[str, str] = {}
    for index, slot in enumerate(ladder):
        if index >= len(pool):
            break
        slot_to_model[slot] = pool[index]

    def _factory(slot_name: str) -> Transport:
        model_id = slot_to_model.get(slot_name)
        if model_id is None:
            requested = (
                ladder.index(slot_name) + 1 if slot_name in ladder else len(ladder)
            )
            raise ModelPoolTooSmallError(len(pool), requested)
        return build_transport(model_id)

    return _factory


# ---------------------------------------------------------------------------
# Impure controller (the ONE side-effecting function)
# ---------------------------------------------------------------------------


def _primary_attempt_id(worker: WorkerResult) -> str:
    return f"primary:{worker.index:02d}"


def _fallback_attempt_id(slot_name: str) -> str:
    return f"fallback:{slot_name}"


def _wall_clock_ok(
    deadline_monotonic: float | None, now: float
) -> tuple[bool, float | None]:
    """Return ``(ok, remaining)`` for the shared run deadline (F4).

    ``deadline_monotonic is None`` means the wall-clock bound is inert (no
    configured timeout) — always ok, no remaining clamp.
    """
    if deadline_monotonic is None:
        return True, None
    remaining = deadline_monotonic - now
    return remaining > _FALLBACK_WALL_CLOCK_FLOOR_SEC, remaining


def _build_fallback_preflight(transport: str) -> PreflightResult:
    """Minimal 1-worker swarm preflight for a single fallback attempt.

    Mirrors ``ensemble.build_preflight_result`` but hard-codes
    ``workers_requested=1`` (one slot per attempt) and is built from swarm-model
    primitives only, so ``fallback.py`` never imports ``reflect.ensemble``.
    """
    manifest = Manifest(
        job_id="reflect-ensemble-fallback",
        preflight=PreflightSummary(
            target_checksum="",
            workers_requested=1,
            transport_kind=transport,
        ),
        caller_metadata=CallerMetadata(suspect=True, tier="T2"),
    )
    return PreflightResult(
        manifest=manifest,
        state=SwarmState(state="preflight_ok", job_id=manifest.job_id),
        caller_metadata=manifest.caller_metadata,
    )


def _ledger_entry(
    worker: WorkerResult,
    *,
    role: str,
    attempt_id: str,
    contributing_ids: set[int],
    fallback_for: list[str] | None = None,
    fallback_reason: str | None = None,
) -> dict[str, Any]:
    """Build one §5 attempt-ledger entry from a real ``WorkerResult``.

    Deliberately OMITS ``model_slot`` / ``retry_count`` / ``normalization`` (design
    §6 F-coverage) to avoid widening ``WorkerResult``. ``failure_class`` is
    free-form telemetry — the worker's status when non-success, else ``None``.
    """
    return {
        "attempt_id": attempt_id,
        "role": role,
        "model_id": worker.model_id,
        "vendor": _vendor_from_model_id(worker.model_id) if worker.model_id else None,
        "status": worker.status,
        "failure_class": None if worker.status == "success" else worker.status,
        "fallback_for": fallback_for,
        "fallback_reason": fallback_reason,
        "contributes_to_quorum": id(worker) in contributing_ids,
    }


def _dispatch_one_fallback(
    slot_name: str,
    *,
    transport_for_fallback_slot: FallbackTransportFactory,
    prompt: str,
    config: ReflectConfig,
    swarm_output_dir: Path,
    stamp: Callable,
    dispatch: Callable,
    normalize: Callable,
    timeout_sec: int,
) -> WorkerResult:
    """Dispatch a single fallback reviewer for ``slot_name`` (F2 order).

    Resolves the slot-NAME transport EAGERLY (so a ``TransportEnvError`` /
    ``ModelPoolTooSmallError`` surfaces here for the caller to catch into
    ``fallback_config_missing``), then dispatch -> STAMP -> normalize, mirroring
    the primary seam order so the fallback worker carries a stable ``final_path``.
    """
    transport = transport_for_fallback_slot(slot_name)  # eager (may raise)

    def _slot_adapter(_slot_index: int) -> Transport:
        return transport

    preflight = _build_fallback_preflight(config.transport)
    worker_spec = WorkerSpec(count=1, models=[], timeout_sec=timeout_sec)
    raw = dispatch(
        preflight,
        transport_for_slot=_slot_adapter,
        prompt=prompt,
        worker_spec=worker_spec,
    )
    attempt_dir = Path(swarm_output_dir) / f"fallback-{slot_name}"
    stamped = stamp(raw, attempt_dir)
    normalized = normalize(
        stamped,
        _REFLECT_REVIEW_RECIPE,
        recipe_args={
            "target": str(config.tasklist_path),
            "target_checksum": "",
            "caller_label": "reflect-ensemble-fallback",
        },
    )
    return normalized[0]


def run_fallback_ladder(
    *,
    primaries: list[WorkerResult],
    config: ReflectConfig,
    transport_for_fallback_slot: FallbackTransportFactory,
    prompt: str,
    swarm_output_dir: Path,
    stamp: Callable,
    dispatch: Callable = dispatch_wave1,
    normalize: Callable = normalize_wave2,
    deadline_monotonic: float | None = None,
    env: Mapping[str, str] | None = None,
) -> LadderOutcome:
    """Bounded T1 quorum top-up after primary normalize (the ONE impure helper).

    Loops ``evaluate_quorum -> plan_next_attempt -> (dispatch ONE slot -> stamp ->
    normalize)`` until the Tier-2 quorum is met, the ladder/attempt budget is
    spent, or the run deadline is exhausted. Every attempt is a 1-worker dispatch
    against the slot-NAME factory, so at most one attempt per ladder slot occurs.
    ``dispatch`` / ``normalize`` / ``stamp`` are injected so unit and stub tests
    never touch a transport. Returns a :class:`LadderOutcome` carrying: the
    ``contributing_workers`` (smallest certifying subset, used only for the
    certification-basis telemetry), ``all_workers`` (the FULL augmented set — every
    normalized primary plus every dispatched fallback attempt — which the ensemble
    hands to ``reduce_wave3`` / ``build_reflect_contract`` for worker accounting and
    reviewer_count/diversity), the full attempt ledger, and the §6 metadata.
    """
    ladder = tuple(config.tier2_fallback_ladder)
    max_attempts = int(config.tier2_fallback_max_attempts)
    allow_single_vendor = bool(config.allow_single_vendor)

    primary_successes, eligible_failures = classify_outcomes(primaries)
    primary_failure_ids = [_primary_attempt_id(w) for w in eligible_failures]
    original_primary_pool_fully_succeeded = len(eligible_failures) == 0

    attempts_made: list[str] = []
    fallback_records: list[tuple[str, WorkerResult]] = []
    config_missing_slots: list[str] = []
    terminal_reason: str | None = None

    while len(attempts_made) < max_attempts:
        current = primary_successes + [w for _s, w in fallback_records]
        quorum = evaluate_quorum(current, allow_single_vendor=allow_single_vendor)
        wall_ok, remaining = _wall_clock_ok(deadline_monotonic, time.monotonic())
        # Ladder slots are optimistically available; a real factory failure is
        # discovered eagerly at dispatch and folded into fallback_config_missing.
        fallback_available = {slot: True for slot in ladder}
        decision = plan_next_attempt(
            quorum,
            eligible_failures,
            attempts_made,
            ladder,
            fallback_available=fallback_available,
            wall_clock_ok=wall_ok,
        )
        if decision.action != "dispatch":
            terminal_reason = decision.reason
            break

        slot_name = decision.slot or ""
        attempts_made.append(slot_name)
        attempt_timeout = int(config.timeout_seconds)
        if remaining is not None:
            attempt_timeout = max(1, int(min(config.timeout_seconds, remaining)))
        try:
            fb_worker = _dispatch_one_fallback(
                slot_name,
                transport_for_fallback_slot=transport_for_fallback_slot,
                prompt=prompt,
                config=config,
                swarm_output_dir=swarm_output_dir,
                stamp=stamp,
                dispatch=dispatch,
                normalize=normalize,
                timeout_sec=attempt_timeout,
            )
        except (TransportEnvError, ModelPoolTooSmallError):
            config_missing_slots.append(slot_name)
            terminal_reason = "fallback_config_missing"
            break
        fallback_records.append((slot_name, fb_worker))

    fallback_successes = [w for _s, w in fallback_records if w.status == "success"]

    if terminal_reason is None:
        final_quorum = evaluate_quorum(
            primary_successes + fallback_successes,
            allow_single_vendor=allow_single_vendor,
        )
        if final_quorum.satisfies_tier2:
            terminal_reason = (
                "certified_t2_with_fallback"
                if attempts_made
                else "not_needed_primary_quorum_met"
            )
        elif all(slot in attempts_made for slot in ladder):
            # Every ladder slot NAME was attempted and quorum is still unmet
            # (design §8 counter-case): the ladder is fully exhausted.
            terminal_reason = "fallback_pool_exhausted"
        else:
            # max_attempts truncated the ladder before every slot was consumed.
            terminal_reason = "fallback_attempts_failed"

    contributing = select_contributing_set(
        primary_successes, fallback_successes, allow_single_vendor=allow_single_vendor
    )
    contributing_ids = {id(w) for w in contributing}
    fallback_success_ids = {id(w) for w in fallback_successes}
    contributing_quorum = evaluate_quorum(
        contributing, allow_single_vendor=allow_single_vendor
    )
    if not contributing_quorum.satisfies_tier2:
        certification_basis = "not_certified"
    elif any(id(w) in fallback_success_ids for w in contributing):
        certification_basis = "primary_plus_fallback_quorum"
    else:
        certification_basis = "primary_only_quorum"

    attempt_ledger: list[dict] = [
        _ledger_entry(
            worker,
            role="primary",
            attempt_id=_primary_attempt_id(worker),
            contributing_ids=contributing_ids,
        )
        for worker in primaries
    ]
    for slot_name, worker in fallback_records:
        attempt_ledger.append(
            _ledger_entry(
                worker,
                role="fallback",
                attempt_id=_fallback_attempt_id(slot_name),
                contributing_ids=contributing_ids,
                fallback_for=primary_failure_ids or None,
                fallback_reason="primary_terminal_failure",
            )
        )
    for slot_name in config_missing_slots:
        attempt_ledger.append(
            {
                "attempt_id": _fallback_attempt_id(slot_name),
                "role": "fallback",
                "model_id": None,
                "vendor": None,
                "status": "proxy_error",
                "failure_class": "fallback_config_missing",
                "fallback_for": primary_failure_ids or None,
                "fallback_reason": "primary_terminal_failure",
                "contributes_to_quorum": False,
            }
        )

    contributing_ledger_ids = [
        entry["attempt_id"]
        for entry in attempt_ledger
        if entry["contributes_to_quorum"]
    ]

    metadata = build_fallback_metadata(
        ladder=ladder,
        engaged=bool(attempts_made),
        attempt_ledger=attempt_ledger,
        contributing_ids=contributing_ledger_ids,
        primary_failures=primary_failure_ids,
        terminal_reason=terminal_reason,
        certification_basis=certification_basis,
        original_primary_pool_fully_succeeded=original_primary_pool_fully_succeeded,
    )

    # The FULL augmented worker set: every normalized primary (successes AND
    # failures) plus every dispatched fallback attempt. Handed to reduce_wave3 /
    # build_reflect_contract so worker accounting (status, workers_failed,
    # output_files, reviewer_count, diversity) is computed over what ACTUALLY ran
    # — never the trimmed certifying subset (which would spuriously mark a healthy
    # >2-success run ``partial``).
    all_workers = list(primaries) + [worker for _slot, worker in fallback_records]

    return LadderOutcome(
        contributing_workers=contributing,
        attempt_ledger=attempt_ledger,
        metadata=metadata,
        all_workers=all_workers,
    )
