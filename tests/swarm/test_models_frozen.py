"""F-P1-3 model-frozen probe (Option C — selective freeze).

Authored by TASK-RF-20260607-212210 as the ONLY authorized test addition for
the MultiModelSwarm remediation.

Proves the principled rule resolved for HALT decision F-P1-3:

  * Contract / source-of-truth records are FROZEN:
        ResultContract (DM-012), Manifest (DM-016), DoneSentinel (DM-017)
  * Accumulator / state records remain MUTABLE by design:
        WorkerResult (DM-013), SwarmState (DM-014), EventRecord (DM-015),
        WorkerSpec (DM-002)

The mutable records are mutated in-flight by the dispatcher / TUI / state
modules (e.g. ``dispatch.py`` stamps ``WorkerResult.attempts`` /
``.elapsed_ms``), so freezing them would break the pipeline. The contract
records are emitted once and never mutated post-construction, so freezing them
enforces the source-of-truth invariant without breaking any caller.

Style mirrored from ``tests/swarm/test_config.py`` (SwarmConfig frozen probe).
"""

from __future__ import annotations

import dataclasses

import pytest

from superclaude.cli.swarm.models import (
    DoneSentinel,
    EventRecord,
    Manifest,
    ResultContract,
    SwarmState,
    WorkerResult,
    WorkerSpec,
)

# ---------------------------------------------------------------------------
# Contract / source-of-truth records — MUST be frozen (F-P1-3 Option C)
# ---------------------------------------------------------------------------


def test_result_contract_is_frozen() -> None:
    inst = ResultContract()
    assert inst.__dataclass_params__.frozen is True
    with pytest.raises(dataclasses.FrozenInstanceError):
        inst.status = "failed"  # type: ignore[misc]


def test_manifest_is_frozen() -> None:
    inst = Manifest()
    assert inst.__dataclass_params__.frozen is True
    with pytest.raises(dataclasses.FrozenInstanceError):
        inst.job_id = "x"  # type: ignore[misc]


def test_done_sentinel_is_frozen() -> None:
    inst = DoneSentinel()
    assert inst.__dataclass_params__.frozen is True
    with pytest.raises(dataclasses.FrozenInstanceError):
        inst.contract_path = "/x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Accumulator / state records — MUST stay mutable (mutation must SUCCEED)
# ---------------------------------------------------------------------------


def test_worker_result_is_mutable() -> None:
    inst = WorkerResult()
    assert inst.__dataclass_params__.frozen is False
    inst.index = 7  # mutated in-flight by dispatch.py — must NOT raise
    assert inst.index == 7


def test_swarm_state_is_mutable() -> None:
    inst = SwarmState()
    assert inst.__dataclass_params__.frozen is False
    inst.state = "dispatching"  # coarse wave-state transitions mutate in place
    assert inst.state == "dispatching"


def test_event_record_is_mutable() -> None:
    inst = EventRecord()
    assert inst.__dataclass_params__.frozen is False
    inst.event_type = "terminal"  # appended-record fields may be stamped
    assert inst.event_type == "terminal"


def test_worker_spec_is_mutable() -> None:
    inst = WorkerSpec()
    assert inst.__dataclass_params__.frozen is False
    inst.count = 8  # lens-expansion mutates the spec at preflight
    assert inst.count == 8
