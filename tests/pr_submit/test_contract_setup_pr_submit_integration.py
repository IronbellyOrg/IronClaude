"""`/sc:pr-submit` missing-contract halt integration (research §"/sc:pr-submit
missing-contract halt integration").

These tests prove the fail-closed seam between the read-only contract-readiness
diagnosis (``diagnose`` / ``render_pr_submit_missing_contract_halt``) and the
armed monitor FSM (``run_skill``):

1. On a missing/unlocked contract, ``DetectionContract.for_arming()`` raises
   ``DetectionContractLocked`` BEFORE any monitor arm — the recorder seam proves
   the arm count is zero (T-210 fail-closed gate; same recorder pattern as
   ``test_monitor_arm.py`` / ``test_autonomy_gates.py``).
2. The missing-contract halt renderer emits the EXACT no-side-effect sentence.
3. ``--monitor 0`` remains the open-PR-only opt-out: never arms, never leaves
   ``S0_IDLE`` (AC-1, mirrors ``test_t110_monitor_never_armed_at_l0``).
4. Post-lock, ``DetectionContract.for_arming()`` returns the locked override
   (the existing arming path still works — mirrors
   ``test_local_override_arms_without_touching_shipped_source``).
5. Setup/readiness diagnosis PRINTS a next-command but never EXECUTES it: the
   renderer returns a plain string, and diagnose/render perform zero
   arm/push/reply/resolve/retrigger/retry/resume calls (recorder seams stay 0).

The local-override path is monkeypatched onto ``detection._LOCAL_OVERRIDE_PATH``
(the documented test seam); no real ``.dev/pr-monitor/`` is ever written. All
symbols imported here are REAL production symbols.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from superclaude.pr_submit import detection
from superclaude.pr_submit.contract_setup import ContractState
from superclaude.pr_submit.contract_setup.diagnosis import (
    diagnose,
    render_pr_submit_missing_contract_halt,
)
from superclaude.pr_submit.detection import (
    DetectionContract,
    DetectionContractLocked,
)
from superclaude.pr_submit.fsm import RunConfig, run_skill
from superclaude.pr_submit.models import MonitorState

# The exact no-side-effect sentence the halt renderer must contain (research
# Key Takeaway: [CODE-VERIFIED] canonical sentence).
NO_SIDE_EFFECTS_SENTENCE = (
    "No monitor was armed. No comments, pushes, retries, resolves, "
    "or retriggers were performed."
)


class _Recorder:
    """Records every call — the arm/push/reply/resolve/retrigger/retry/resume seam."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, *_a, **_k) -> None:
        self.calls += 1


def _write_locked_override(path):
    """Write a minimal locked local-override contract at ``path`` (locked:true)."""
    path.write_text(
        '# local\n\n```yaml\naugment_bot_login: "augmentcode[bot]"\nlocked: true\n```\n',
        encoding="utf-8",
    )


# --- 1. missing/unlocked contract → for_arming() HALTs before any arm ---------


def test_missing_contract_for_arming_halts_before_monitor_arm(tmp_path, monkeypatch):
    """A missing locked override makes ``for_arming()`` HALT — and no monitor arms.

    The arm seam is a recorder threaded through ``run_skill`` the SAME way as
    ``test_monitor_arm.py``. Because ``for_arming()`` raises BEFORE ``run_skill``
    is ever reached, the arm count is provably zero (fail-closed, T-210).
    """
    # Point the override at an absent path → for_arming() falls back to the shipped
    # source (locked:false) and HALTs.
    monkeypatch.setattr(
        detection, "_LOCAL_OVERRIDE_PATH", tmp_path / "absent.locked.md"
    )
    arm_recorder = _Recorder()

    armed = False
    with pytest.raises(DetectionContractLocked):
        contract = DetectionContract.for_arming()  # HALTs here — arm never reached.
        # Unreachable: only if a contract loaded would the FSM arm.
        run_skill(
            RunConfig(
                monitor_ordinal=1,
                arm_monitor=arm_recorder,
                review_state="polling",
                pr_number=42,
            )
        )
        armed = contract.locked

    assert armed is False
    # The arm gate is DOWNSTREAM of the raised lock gate → zero arms.
    assert arm_recorder.calls == 0


def test_unlocked_local_override_for_arming_halts(tmp_path, monkeypatch):
    """An explicit ``locked:false`` local override still HALTs ``for_arming()`` (no arm)."""
    override = tmp_path / "detection-contract.locked.md"
    override.write_text(
        '# local\n\n```yaml\naugment_bot_login: "augmentcode[bot]"\nlocked: false\n```\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(detection, "_LOCAL_OVERRIDE_PATH", override)
    arm_recorder = _Recorder()

    with pytest.raises(DetectionContractLocked):
        DetectionContract.for_arming()

    assert arm_recorder.calls == 0


# --- 2. exact no-side-effect halt sentence ------------------------------------


def test_missing_contract_halt_prints_no_side_effects_sentence(tmp_path):
    """``render_pr_submit_missing_contract_halt(diagnose(...))`` contains the EXACT sentence."""
    diagnosis = diagnose(cwd=tmp_path)
    assert diagnosis.state is ContractState.MISSING

    rendered = render_pr_submit_missing_contract_halt(diagnosis)
    assert NO_SIDE_EFFECTS_SENTENCE in rendered
    # It is a fail-closed HALT that names the diagnosis state and checked paths.
    assert rendered.startswith("HALT:")
    assert f"Diagnosis state: {ContractState.MISSING.value}" in rendered


# --- 3. --monitor 0 open-PR-only semantics preserved --------------------------


def test_monitor_zero_never_arms_and_stays_idle():
    """``--monitor 0`` NEVER arms and the FSM never leaves ``S0_IDLE`` (AC-1, unaffected).

    Mirrors ``test_t110_monitor_never_armed_at_l0`` — the contract-setup work does
    not perturb the open-PR-only opt-out path.
    """
    arm_recorder = _Recorder()
    result = run_skill(
        RunConfig(monitor_ordinal=0, arm_monitor=arm_recorder, review_state="polling")
    )
    assert arm_recorder.calls == 0
    assert result.state == MonitorState.S0_IDLE


# --- 4. post-lock: for_arming() returns the locked override -------------------


def test_post_lock_for_arming_returns_locked_contract(tmp_path, monkeypatch):
    """With a valid locked override present, ``for_arming()`` returns a locked contract.

    Proves the existing arming path still works once a lock exists — the default
    ``load()`` still HALTs on the shipped source (T-210 unaffected), while the arm
    path prefers the override. Mirrors
    ``test_local_override_arms_without_touching_shipped_source``.
    """
    override = tmp_path / "detection-contract.locked.md"
    _write_locked_override(override)
    monkeypatch.setattr(detection, "_LOCAL_OVERRIDE_PATH", override)

    # Default load() ignores the override → shipped source (locked:false) → HALT.
    with pytest.raises(DetectionContractLocked):
        DetectionContract.load()

    # The arm path prefers the override → locked:true with the real bot login.
    armed = DetectionContract.for_arming()
    assert armed.locked is True
    assert armed.augment_bot_login == "augmentcode[bot]"

    # And now the armed FSM actually arms exactly once (the arming path works).
    arm_recorder = _Recorder()
    run_skill(
        RunConfig(monitor_ordinal=1, arm_monitor=arm_recorder, review_state="polling")
    )
    assert arm_recorder.calls == 1


# --- 5. setup/readiness prints a next-command but executes nothing ------------


def test_diagnose_and_render_perform_no_side_effects(tmp_path, monkeypatch):
    """Diagnose/render are presentation-only: a next-command is TEXT, never executed.

    ``diagnose``/``render_pr_submit_missing_contract_halt`` take NO seam arguments,
    so threading recorder callables through them is structurally impossible — a
    ``for rec in (...): assert rec.calls == 0`` loop over never-wired recorders is
    tautologically true and would pass even if the code path DID arm. This test
    instead binds the no-side-effect guarantee two real, non-tautological ways:

    1. **Static import-graph audit** (mirrors
       ``test_contract_setup_writer.py::test_writer_package_imports_no_fsm_seams``):
       the whole ``contract_setup`` package graph — including ``diagnosis`` — never
       imports the ``fsm``/``monitor``/reply-resolve/retrigger seams and exposes no
       ``arm_monitor`` entrypoint, so the diagnose/render path *cannot* reach a
       monitor/PR side-effect seam.
    2. **No-writes snapshot**: snapshot the tmp tree before and after a full
       ``diagnose(...)`` + ``render(...)``; assert not a single file was created
       (no lock, no report, no probe) — the printed ``next_command`` stays a string.
    """
    monkeypatch.setattr(
        detection, "_LOCAL_OVERRIDE_PATH", tmp_path / "absent.locked.md"
    )

    # (1) Static guarantee: import the full contract_setup graph and assert no
    # module references an FSM/monitor seam and the package exposes no arm entry.
    import superclaude.pr_submit.contract_setup as pkg
    import superclaude.pr_submit.contract_setup.candidate  # noqa: F401
    import superclaude.pr_submit.contract_setup.diagnosis  # noqa: F401
    import superclaude.pr_submit.contract_setup.evidence  # noqa: F401
    import superclaude.pr_submit.contract_setup.lockgate  # noqa: F401
    import superclaude.pr_submit.contract_setup.validation  # noqa: F401
    import superclaude.pr_submit.contract_setup.writer  # noqa: F401

    forbidden = ("fsm", "monitor", "reply_resolve", "review_retrigger")
    contract_setup_modules = [
        name
        for name in sys.modules
        if name.startswith("superclaude.pr_submit.contract_setup")
    ]
    assert contract_setup_modules  # sanity: the package graph is loaded
    # The diagnose/render surface under test is part of the audited graph.
    assert "superclaude.pr_submit.contract_setup.diagnosis" in contract_setup_modules
    for mod_name in contract_setup_modules:
        module = sys.modules[mod_name]
        source_file = getattr(module, "__file__", None)
        if not source_file:
            continue
        text = Path(source_file).read_text(encoding="utf-8")
        for seam in forbidden:
            assert f"pr_submit.{seam}" not in text and f"import {seam}" not in text, (
                f"{mod_name} references forbidden FSM seam '{seam}'"
            )
    assert not hasattr(pkg, "arm_monitor")

    # (2) Behavioral guarantee: a full diagnose + render writes ZERO files.
    before = {p for p in tmp_path.rglob("*")}
    diagnosis = diagnose(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)
    rendered = render_pr_submit_missing_contract_halt(diagnosis)
    after = {p for p in tmp_path.rglob("*")}
    assert after == before, f"diagnose/render created files: {sorted(after - before)}"

    # The rendered halt names a next safe step (a STRING) — it is not executed.
    assert isinstance(diagnosis.next_command, str)
    assert diagnosis.next_command  # non-empty
    assert diagnosis.next_command in rendered
    assert "Next safe step:" in rendered

    # The recommended next-command is the reflect contract-status readiness probe,
    # NOT an arming rerun (setup never executes /sc:pr-submit).
    assert "reflect contract-status" in diagnosis.next_command
    assert "--monitor" not in diagnosis.next_command
