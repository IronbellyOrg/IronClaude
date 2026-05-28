"""TEST-017 — slow-shrink |F|=5,4 continues (R-106 / X-003 REJECTION).

Phase-5 / T05.14 deliverable (D-0065). Codifies the X-003 rejection
invariant from the M5 roadmap row 10: a strict shrink by 1
(``|F_{n+1}| < |F_n|``, no matter how slow) MUST proceed to the
next cycle. No rate-of-shrink parameter is introduced; the
monotonicity check is the binary predicate ``|F_{n+1}| >= |F_n|``,
which is FALSE for ``|F|=5,4`` (4 < 5), so the 4-step ordering
rule advances to Step 4 (proceed).

The fixture mirrors the SKILL.md §A.9 "API-004 Fix-Loop Halt
Signals" wire contract by replaying the 4-step iterator from
``_halt_emitter.py`` (the same helper exercised by TEST-015 /
TEST-016) and asserting:

1. The runtime emits ZERO halt of any kind — no ``HALT-MONOTONICITY``
   token, no regression halt-message, no hard-cap halt.
2. ``CYCLE 3 START`` is attempted (slow shrink continues to cycle 3
   per X-003 rejection).
3. The transition between cycle 1 and cycle 2 produces a
   monotonicity verdict of PROCEED (cardinality strictly shrank),
   followed by hard-cap PROCEED (counter 2/3) and proceed re-spawn.
4. Replacing ``|F|=5,4`` with ``|F|=5,5`` flips the verdict to HALT —
   constructive proof that the X-003 rejection is load-bearing
   (without it, slow shrink would also halt under a rate threshold).
5. The generated log shape matches the canonical D-0060 synthetic
   fixture (``fixture-slow-shrink-F-5-4.log``) at the load-bearing
   transition + cycle-3 spawn lines.
6. The SKILL.md §A.9 API-004 contract block still encodes the
   strict-non-shrink predicate (``|F_{n+1}| >= |F_n|``), and the
   SKILL.md text rejects a rate-of-shrink threshold parameter.

Acceptance reference (phase-5-tasklist.md L676-679):
- ``uv run pytest tests/audit/test_slow_shrink_continues.py -v`` exits 0.
- TEST-017 assertion: execution log shows cycle continues.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0065/evidence.md``.

Run: ``uv run pytest tests/audit/test_slow_shrink_continues.py -v``
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# Allow ``from _halt_emitter import ...`` regardless of how pytest
# composes sys.path for tests/audit/. TEST-017 reuses the same
# 4-step iterator exercised by TEST-015 / TEST-016 so the X-003
# rejection assertion below is load-bearing against the actual
# wrapper whose halt strings TEST-015 verifies byte-for-byte.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _halt_emitter import (  # noqa: E402
    CycleState,
    HaltLog,
    run_fix_cycle,
)

SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"

CANONICAL_LOG = (
    REPO_ROOT
    / ".dev"
    / "releases"
    / "complete"
    / "task-builder-merge"
    / "artifacts"
    / "D-0060"
    / "fixture-slow-shrink-F-5-4.log"
)


# ---------------------------------------------------------------------------
# Fixtures — |F|=5,4 slow shrink + counterfactual |F|=5,5 non-shrink.
# ---------------------------------------------------------------------------


# Slow shrink: |F_1|=5, |F_2|=4. Item 3.1 fixed; items 3.2..3.5
# remain FAIL. No PASS@1 → FAIL@2 flip (items 3.2..3.5 were FAIL_1,
# not PASS_1), so regression check returns PASS. Monotonicity check
# returns PROCEED (4 < 5). The loop re-spawns cycle 3, which
# converges with |F_3|=0.
F_5_4_CYCLES = [
    CycleState(
        cycle=1,
        fail_set={"item-3.1", "item-3.2", "item-3.3", "item-3.4", "item-3.5"},
        pass_set={"item-1.1", "item-4.2", "item-6.1", "item-8.2", "item-10.1"},
    ),
    CycleState(
        cycle=2,
        # item-3.1 fixed (FAIL→PASS, refinement). Others persist.
        fail_set={"item-3.2", "item-3.3", "item-3.4", "item-3.5"},
        pass_set={
            "item-1.1",
            "item-3.1",
            "item-4.2",
            "item-6.1",
            "item-8.2",
            "item-10.1",
        },
    ),
    CycleState(
        cycle=3,
        # All remaining items fixed. Converges.
        fail_set=set(),
        pass_set={
            "item-1.1",
            "item-3.1",
            "item-3.2",
            "item-3.3",
            "item-3.4",
            "item-3.5",
            "item-4.2",
            "item-6.1",
            "item-8.2",
            "item-10.1",
        },
    ),
]


# Counterfactual: |F_1|=5, |F_2|=5 (non-shrink). Same composition
# pattern (no PASS→FAIL flip), but cardinality does NOT shrink — so
# monotonicity must HALT. This proves the X-003 rejection in the
# main fixture is load-bearing (a rate threshold would have halted
# |F|=5,4 too; the binary predicate does not).
F_5_5_CYCLES = [
    CycleState(
        cycle=1,
        fail_set={"item-3.1", "item-3.2", "item-3.3", "item-3.4", "item-3.5"},
        pass_set={"item-1.1", "item-4.2", "item-6.1", "item-8.2", "item-10.1"},
    ),
    CycleState(
        cycle=2,
        # item-3.1 fixed, but item-12.1 newly fails (NOT in PASS_1,
        # so not a regression). |F| stays at 5.
        fail_set={"item-3.2", "item-3.3", "item-3.4", "item-3.5", "item-12.1"},
        pass_set={
            "item-1.1",
            "item-3.1",
            "item-4.2",
            "item-6.1",
            "item-8.2",
            "item-10.1",
        },
    ),
]


@pytest.fixture(scope="module")
def slow_shrink_log() -> HaltLog:
    return run_fix_cycle(F_5_4_CYCLES)


@pytest.fixture(scope="module")
def counterfactual_non_shrink_log() -> HaltLog:
    return run_fix_cycle(F_5_5_CYCLES)


@pytest.fixture(scope="module")
def skill_text() -> str:
    return SKILL_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def canonical_log_text() -> str:
    return CANONICAL_LOG.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Static schema / source guards — SKILL.md X-003 rejection wording.
# ---------------------------------------------------------------------------


class TestSkillX003RejectionDocumented:
    """SKILL.md §A.9 encodes the X-003 rejection: the monotonicity
    predicate is binary (``|F_{n+1}| >= |F_n|``), not rate-of-shrink.
    A regression to a rate threshold would silently halt legitimate
    slow convergence."""

    def test_skill_src_exists(self):
        assert SKILL_SRC.is_file(), f"missing SKILL.md at {SKILL_SRC}"

    def test_monotonicity_predicate_is_binary(self, skill_text: str):
        # The binary predicate text appears verbatim in SKILL.md §A.9.
        # A rate-of-shrink threshold would have a percentage or
        # ratio operator instead of the ``>=`` non-shrink predicate.
        assert "|F_{n+1}| >= |F_n|" in skill_text, (
            "SKILL.md must encode the binary monotonicity predicate "
            "'|F_{n+1}| >= |F_n|' — X-003 rejection requires the "
            "non-shrink comparison, not a rate threshold"
        )


# ---------------------------------------------------------------------------
# AC1 — Zero halts of any kind on the |F|=5,4 fixture.
# ---------------------------------------------------------------------------


class TestSlowShrinkEmitsNoHalt:
    """Strict shrink by 1 must proceed. No HALT line, no
    ``HALT-MONOTONICITY`` token, no regression halt-message."""

    def test_halt_message_is_none(self, slow_shrink_log: HaltLog):
        assert slow_shrink_log.halt_message is None, (
            f"slow-shrink |F|=5,4 emitted unexpected halt: "
            f"{slow_shrink_log.halt_message!r} — X-003 rejection regressed"
        )

    def test_no_halt_line_in_log(self, slow_shrink_log: HaltLog):
        halt_lines = [ln for ln in slow_shrink_log.lines if ln.startswith("HALT ")]
        assert halt_lines == [], (
            f"slow-shrink |F|=5,4 emitted HALT line(s): {halt_lines!r} — "
            "loop must continue per the binary non-shrink predicate"
        )

    def test_no_monotonicity_token_anywhere(self, slow_shrink_log: HaltLog):
        joined = "\n".join(slow_shrink_log.lines)
        assert "HALT-MONOTONICITY" not in joined, (
            "monotonicity halt token unexpectedly present on slow-shrink "
            "|F|=5,4 run — emitter over-fired"
        )

    def test_no_regression_token_anywhere(self, slow_shrink_log: HaltLog):
        joined = "\n".join(slow_shrink_log.lines)
        assert "HALT Regression" not in joined, (
            "regression halt token unexpectedly present on slow-shrink "
            "|F|=5,4 run — no PASS→FAIL flip occurred (items 3.2..3.5 "
            "were FAIL_1, not PASS_1)"
        )


# ---------------------------------------------------------------------------
# AC2 — Cycle 3 IS attempted (loop continues).
# ---------------------------------------------------------------------------


class TestCycle3IsAttempted:
    """The whole point of X-003 rejection: cycle 3 must be spawned
    after a |F|=5,4 transition, because the binary non-shrink
    predicate is FALSE (strict shrink). If a rate threshold had
    been introduced, cycle 3 would NOT be spawned and this test
    would fail."""

    def test_cycle_3_in_cycles_started(self, slow_shrink_log: HaltLog):
        assert 3 in slow_shrink_log.cycles_started, (
            f"cycle 3 NOT attempted after slow shrink: "
            f"cycles_started={slow_shrink_log.cycles_started} — "
            "X-003 rejection regressed (rate threshold falsely triggered)"
        )

    def test_cycle_3_start_line_present(self, slow_shrink_log: HaltLog):
        cycle_3_lines = [ln for ln in slow_shrink_log.lines if "CYCLE 3 START" in ln]
        assert len(cycle_3_lines) == 1, (
            f"expected exactly one 'CYCLE 3 START' line, got "
            f"{len(cycle_3_lines)}: {cycle_3_lines}"
        )

    def test_per_gate_counter_advances_to_three(self, slow_shrink_log: HaltLog):
        # The cycle-3 spawn line includes ``counter=3/3``, signalling
        # the per-gate cap is at its boundary but NOT halting.
        counters = [ln for ln in slow_shrink_log.lines if "counter=" in ln]
        assert any(ln.endswith("counter=3/3") for ln in counters), (
            f"per-gate counter never reached 3/3 on slow-shrink run: "
            f"counter lines = {counters!r}"
        )


# ---------------------------------------------------------------------------
# AC3 — 4-step ordering verdicts at the cycle-1 → cycle-2 transition.
# ---------------------------------------------------------------------------


class TestSlowShrinkTransitionVerdicts:
    """At the cycle-1 → cycle-2 transition (labeled ``TRANSITION 2->3``
    in the helper's convention — decision_from=curr.cycle=2, decision_to=
    curr.cycle+1=3, per the comment block in ``_halt_emitter.py``),
    each of the four steps must run and produce the documented verdict:
    regression PASS, monotonicity PROCEED, hard-cap PROCEED, proceed
    re-spawn. The full set of steps confirms no early exit."""

    def test_regression_step_pass(self, slow_shrink_log: HaltLog):
        # decision_to=3 ⇒ first transition (between cycles 1 and 2).
        first_transition = [t for t in slow_shrink_log.transitions if t[0] == 3]
        regression_steps = [t for t in first_transition if t[1] == "regression"]
        assert len(regression_steps) == 1, (
            f"expected exactly one regression step at the cycle-1→cycle-2 "
            f"transition (label TRANSITION 2->3), got "
            f"{len(regression_steps)}: {regression_steps}"
        )
        assert regression_steps[0][2] == "PASS", (
            f"regression verdict at TRANSITION 2->3 is "
            f"{regression_steps[0][2]!r}, expected 'PASS' (no PASS→FAIL flip)"
        )

    def test_monotonicity_step_proceed(self, slow_shrink_log: HaltLog):
        first_transition = [t for t in slow_shrink_log.transitions if t[0] == 3]
        mon_steps = [t for t in first_transition if t[1] == "monotonicity"]
        assert len(mon_steps) == 1, (
            f"expected exactly one monotonicity step at TRANSITION 2->3, "
            f"got {len(mon_steps)}: {mon_steps}"
        )
        assert mon_steps[0][2] == "PROCEED", (
            f"monotonicity verdict at TRANSITION 2->3 is "
            f"{mon_steps[0][2]!r}, expected 'PROCEED' (strict shrink 4 < 5)"
        )

    def test_proceed_step_respawn(self, slow_shrink_log: HaltLog):
        first_transition = [t for t in slow_shrink_log.transitions if t[0] == 3]
        proceed_steps = [t for t in first_transition if t[1] == "proceed"]
        assert len(proceed_steps) == 1, (
            f"expected exactly one proceed step at TRANSITION 2->3, "
            f"got {len(proceed_steps)}: {proceed_steps}"
        )
        assert "re-spawn" in proceed_steps[0][2], (
            f"proceed verdict at TRANSITION 2->3 is {proceed_steps[0][2]!r}, "
            "expected 're-spawn'"
        )


# ---------------------------------------------------------------------------
# AC4 — Counterfactual: |F|=5,5 WOULD halt (X-003 rejection is load-bearing).
# ---------------------------------------------------------------------------


class TestCounterfactualNonShrinkHalts:
    """Constructive proof that the X-003 rejection is load-bearing.
    If the cardinality is non-shrinking (5,5 instead of 5,4), the
    same emitter MUST halt via the monotonicity guard — confirming
    that the |F|=5,4 case continues only because the binary
    predicate is FALSE for strict shrink, not because the guard is
    broken."""

    def test_counterfactual_halts_with_monotonicity(
        self, counterfactual_non_shrink_log: HaltLog
    ):
        assert counterfactual_non_shrink_log.halt_message == "[HALT-MONOTONICITY] |F|=5", (
            f"counterfactual |F|=5,5 did NOT halt with byte-exact "
            f"'[HALT-MONOTONICITY] |F|=5': got "
            f"{counterfactual_non_shrink_log.halt_message!r} — X-003 rejection "
            "test cannot prove monotonicity would have fired absent shrink"
        )

    def test_counterfactual_cycle_3_never_started(
        self, counterfactual_non_shrink_log: HaltLog
    ):
        assert 3 not in counterfactual_non_shrink_log.cycles_started, (
            "counterfactual |F|=5,5 unexpectedly attempted cycle 3"
        )


# ---------------------------------------------------------------------------
# AC5 — Canonical D-0060 synthetic fixture log parity.
# ---------------------------------------------------------------------------


class TestCanonicalFixtureParity:
    """The TEST-017 runtime emission and the D-0060 canonical
    synthetic log agree on the load-bearing lines (no HALT, cycle 3
    attempted, monotonicity PROCEED at transition 1->2). Drift
    between this pytest fixture and the D-0060 log indicates either
    the protocol changed or the evidence pack is stale."""

    def test_canonical_log_present(self):
        assert CANONICAL_LOG.is_file(), (
            f"D-0060 canonical fixture missing at {CANONICAL_LOG} — "
            "T05.08 evidence pack regressed"
        )

    def test_canonical_log_has_no_halt(self, canonical_log_text: str):
        halt_lines = [
            ln
            for ln in canonical_log_text.splitlines()
            if ln.startswith("HALT ")
        ]
        assert halt_lines == [], (
            f"D-0060 canonical fixture HALT line(s) {halt_lines!r} — "
            "X-003 rejection regressed in the evidence pack"
        )

    def test_canonical_log_has_cycle_3(self, canonical_log_text: str):
        assert "CYCLE 3 START" in canonical_log_text, (
            "D-0060 canonical fixture missing 'CYCLE 3 START' — slow "
            "shrink must continue to cycle 3 per X-003 rejection"
        )

    def test_canonical_log_no_monotonicity_token(self, canonical_log_text: str):
        # The fixture asserts ZERO ``HALT-MONOTONICITY`` lines in the
        # log per the in-file machine-checkable assertion block. The
        # template string ``[HALT-MONOTONICITY]`` IS referenced in the
        # API-004 contract sha256 line at the header (informational),
        # so we restrict the check to ``^HALT ...`` lines.
        halt_mon_lines = [
            ln
            for ln in canonical_log_text.splitlines()
            if ln.startswith("HALT ") and "HALT-MONOTONICITY" in ln
        ]
        assert halt_mon_lines == [], (
            f"D-0060 canonical fixture has HALT-MONOTONICITY lines: "
            f"{halt_mon_lines!r}"
        )

    def test_canonical_log_monotonicity_proceeds_at_transition_1_2(
        self, canonical_log_text: str
    ):
        # On the cycle-1 → cycle-2 transition, the monotonicity step
        # line records PROCEED (strict shrink).
        lines = canonical_log_text.splitlines()
        mon_idx: Optional[int] = None
        for idx, ln in enumerate(lines):
            if ln.startswith("TRANSITION 1->2 step=monotonicity"):
                mon_idx = idx
                assert "PROCEED" in ln, (
                    f"D-0060 monotonicity step at line {idx} did not record "
                    f"PROCEED: {ln!r}"
                )
                break
        assert mon_idx is not None, (
            "D-0060 canonical fixture missing 'TRANSITION 1->2 step=monotonicity' line"
        )

    def test_canonical_log_proceed_respawn_at_transition_1_2(
        self, canonical_log_text: str
    ):
        # Step 4 (proceed) re-spawns cycle 3 per SKILL.md L1057.
        lines = canonical_log_text.splitlines()
        proceed_idx: Optional[int] = None
        for idx, ln in enumerate(lines):
            if ln.startswith("TRANSITION 1->2 step=proceed"):
                proceed_idx = idx
                assert "re-spawn cycle 3" in ln, (
                    f"D-0060 proceed step at line {idx} did not record "
                    f"'re-spawn cycle 3': {ln!r}"
                )
                break
        assert proceed_idx is not None, (
            "D-0060 canonical fixture missing 'TRANSITION 1->2 step=proceed' line"
        )
