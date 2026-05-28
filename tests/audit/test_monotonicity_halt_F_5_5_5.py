# ruff: noqa: N999  # intentional: filename encodes |F|=5,5,5 monotonicity counter sequence for R-104 / FR-CONV.5 cross-reference
"""TEST-015 — monotonicity halt on |F|=5,5,5 fixture (R-104 / FR-CONV.5 PR-02).

Phase-5 / T05.13 deliverable (D-0064). Codifies the canonical
|F|=5,5,5 monotonicity halt scenario whose synthetic execution-log
shape was demonstrated at T05.03 (D-0056 §1, ``fixture-F-5-5-5-
halt-cycle-2.log``).

The fixture mirrors the SKILL.md §A.9 "API-004 Fix-Loop Halt
Signals" wire contract by implementing the 4-step ordering rule
(regression → monotonicity → hard-cap → proceed) in pure Python
and asserting that the byte-exact halt string is emitted at the
cycle-1 → cycle-2 → cycle-3 boundary that the monotonicity guard
governs:

1. The emitted halt-message string is exactly ``[HALT-MONOTONICITY] |F|=5``
   (24 bytes ASCII; single 0x20 between ``]`` and ``|F|``; ASCII pipes).
2. ``CYCLE 3 START`` is never emitted — the loop halts at the
   cycle-2 → cycle-3 transition before per-gate cap (3) could fire.
3. The monotonicity step verdict-line is the LAST transition line
   in the run, and the regression step ran first (4-step ordering).
4. The monotonicity emitter is gated on ``|F_n| > 0``: replaying the
   same scenario with ``|F_1|=0`` short-circuits the loop and emits
   no ``HALT-MONOTONICITY`` token.
5. The SKILL.md §A.9 API-004 contract table still contains the
   byte-exact wire-string row ``[HALT-MONOTONICITY] |F|=<n>``.
6. The generated log shape matches the canonical D-0056 synthetic
   fixture (`fixture-F-5-5-5-halt-cycle-2.log`) line-for-line at
   the load-bearing transition + halt lines.

Acceptance reference (phase-5-tasklist.md L630-633):
- ``uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py -v`` exits 0.
- ``[HALT-MONOTONICITY] |F|=5`` appears in cycle-2 log; cycle-3 not attempted.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0064/evidence.md``.

Run: ``uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py -v``
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# Allow ``from _halt_emitter import ...`` regardless of how pytest
# composes sys.path for tests/audit/ (the package has __init__.py
# but no conftest.py to extend the path).
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _halt_emitter import (  # noqa: E402
    HALT_MONOTONICITY_TEMPLATE,
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
    / "D-0056"
    / "fixture-F-5-5-5-halt-cycle-2.log"
)


# ---------------------------------------------------------------------------
# Fixtures.
# ---------------------------------------------------------------------------


F_555 = [
    CycleState(
        cycle=1,
        fail_set={"2.1", "3.2", "5.4", "7.1", "9.3"},
        pass_set={"1.1", "4.2", "6.1", "8.2", "10.1", "11.1"},
    ),
    CycleState(
        cycle=2,
        fail_set={"2.1", "3.2", "5.4", "7.1", "9.3"},
        pass_set={"1.1", "4.2", "6.1", "8.2", "10.1", "11.1"},
    ),
]


@pytest.fixture(scope="module")
def halt_log() -> HaltLog:
    """Run the canonical |F|=5,5,5 scenario and return its log."""
    return run_fix_cycle(F_555)


@pytest.fixture(scope="module")
def skill_text() -> str:
    return SKILL_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def canonical_log_text() -> str:
    return CANONICAL_LOG.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Static schema / source guards.
# ---------------------------------------------------------------------------


class TestSkillContractWiringPresent:
    """Pre-flight: SKILL.md §A.9 API-004 contract row 1 still contains
    the byte-exact monotonicity wire template. If this regresses,
    every fix-cycle wrapper's emission silently diverges from what
    downstream log scanners expect."""

    def test_skill_src_exists(self):
        assert SKILL_SRC.is_file(), f"missing SKILL.md at {SKILL_SRC}"

    def test_monotonicity_template_present(self, skill_text: str):
        assert HALT_MONOTONICITY_TEMPLATE in skill_text, (
            f"SKILL.md missing byte-exact API-004 wire template "
            f"{HALT_MONOTONICITY_TEMPLATE!r}"
        )

    def test_monotonicity_byte_exact_no_smart_punctuation(self, skill_text: str):
        # ASCII pipes around F, ASCII brackets around HALT-MONOTONICITY,
        # single 0x20 between `]` and `|F|`. Reject smart-quote/em-dash
        # drift by inspecting bytes within the template span.
        template_bytes = HALT_MONOTONICITY_TEMPLATE.encode("utf-8")
        assert all(b < 0x80 for b in template_bytes), (
            "API-004 monotonicity template contains non-ASCII bytes — "
            "wire contract requires ASCII only"
        )
        assert template_bytes.count(b"|") == 2, (
            "API-004 monotonicity template must contain exactly two ASCII pipes"
        )

    def test_precedence_rule_documented(self, skill_text: str):
        # The 4-step ordering rule must explicitly state that
        # regression runs BEFORE monotonicity (per T05.05 / D-0058 AC).
        assert "regression > monotonicity" in skill_text, (
            "SKILL.md must document 'regression > monotonicity' precedence"
        )


# ---------------------------------------------------------------------------
# AC1 + AC2 — Byte-exact halt at cycle 2; cycle 3 never attempted.
# ---------------------------------------------------------------------------


class TestMonotonicityHaltByteExact:
    """The runtime emitter substitutes ``<n>`` ← 5 and produces the
    byte-exact wire string. The fix-cycle loop halts at the cycle-2
    → cycle-3 transition; CYCLE 3 START is never emitted."""

    def test_halt_message_is_byte_exact(self, halt_log: HaltLog):
        assert halt_log.halt_message == "[HALT-MONOTONICITY] |F|=5", (
            f"emitted halt message {halt_log.halt_message!r} differs from "
            "byte-exact wire form '[HALT-MONOTONICITY] |F|=5'"
        )

    def test_halt_message_byte_length_25(self, halt_log: HaltLog):
        # The actual ASCII payload of ``[HALT-MONOTONICITY] |F|=5`` is
        # 25 bytes (`[HALT-MONOTONICITY]` = 19 + ` ` = 1 + `|F|=5` = 5).
        # D-0056 §1.1's xxd dump shows 25 bytes (offsets 0x00..0x18
        # inclusive); the "24 bytes" prose figure in that paragraph is
        # a typo. This assertion locks the actual byte count.
        assert halt_log.halt_message is not None
        payload = halt_log.halt_message.encode("utf-8")
        assert len(payload) == 25, (
            f"halt payload byte length {len(payload)} != 25 — wire "
            "contract drift (`[HALT-MONOTONICITY] |F|=5` is 25 ASCII bytes)"
        )

    def test_halt_appears_in_emitted_log_lines(self, halt_log: HaltLog):
        halt_lines = [ln for ln in halt_log.lines if ln.startswith("HALT ")]
        assert len(halt_lines) == 1, (
            f"expected exactly one HALT line, got {len(halt_lines)}: {halt_lines}"
        )
        assert halt_lines[0] == "HALT [HALT-MONOTONICITY] |F|=5", (
            f"HALT line {halt_lines[0]!r} differs from byte-exact "
            "'HALT [HALT-MONOTONICITY] |F|=5'"
        )

    def test_cycle_3_never_attempted(self, halt_log: HaltLog):
        assert 3 not in halt_log.cycles_started, (
            f"cycle 3 attempted despite monotonicity HALT at cycle 2 → 3 "
            f"transition. cycles_started={halt_log.cycles_started}"
        )
        cycle_3_lines = [ln for ln in halt_log.lines if "CYCLE 3 START" in ln]
        assert cycle_3_lines == [], (
            f"unexpected 'CYCLE 3 START' lines: {cycle_3_lines}"
        )

    def test_per_gate_counter_stops_at_two(self, halt_log: HaltLog):
        # The per-gate cap (3) is the third-precedence backstop. It
        # MUST NOT fire here — the monotonicity guard exits earlier.
        counters = [ln for ln in halt_log.lines if "counter=" in ln]
        # Last counter line should be cycle 2's start line, "2/3".
        assert counters[-1].endswith("counter=2/3"), (
            f"per-gate counter overshoots monotonicity halt: "
            f"last counter line = {counters[-1]!r}"
        )


# ---------------------------------------------------------------------------
# AC3 — 4-step ordering invariant (regression before monotonicity).
# ---------------------------------------------------------------------------


class TestFourStepOrdering:
    """At the halting transition (cycle 2 → 3), step 1 (regression)
    ran first and returned PASS; step 2 (monotonicity) then ran and
    returned HALT. No step is skipped above step 2."""

    def test_halting_transition_has_regression_first(self, halt_log: HaltLog):
        halting = [t for t in halt_log.transitions if t[0] == 3]
        assert len(halting) >= 2, (
            f"halting transition 2->3 missing regression+monotonicity "
            f"steps: {halting}"
        )
        assert halting[0][1] == "regression", (
            f"first step at transition 2->3 is {halting[0][1]!r}, not 'regression' "
            "— 4-step ordering rule violated"
        )
        assert halting[0][2] == "PASS", (
            f"regression verdict at transition 2->3 is {halting[0][2]!r}, not 'PASS' "
            "— fixture preconditions broken (PASS set should match across cycles)"
        )

    def test_monotonicity_step_runs_second_with_halt(self, halt_log: HaltLog):
        halting = [t for t in halt_log.transitions if t[0] == 3]
        assert halting[1][1] == "monotonicity", (
            f"second step at transition 2->3 is {halting[1][1]!r}, not 'monotonicity'"
        )
        assert "HALT" in halting[1][2], (
            f"monotonicity verdict at transition 2->3 is {halting[1][2]!r}, "
            "expected HALT"
        )

    def test_no_step_3_or_4_consulted_after_halt(self, halt_log: HaltLog):
        halting = [t for t in halt_log.transitions if t[0] == 3]
        # Only regression + monotonicity should fire; hard-cap +
        # proceed are skipped per "Do NOT consult subsequent steps"
        # at SKILL.md:1054.
        steps = [t[1] for t in halting]
        assert "hard-cap" not in steps, (
            "hard-cap step consulted after monotonicity HALT — ordering "
            "rule violated (SKILL.md:1054 'Do NOT consult subsequent steps')"
        )
        assert "proceed" not in steps, (
            "proceed step consulted after monotonicity HALT — loop should have exited"
        )


# ---------------------------------------------------------------------------
# AC4 — Monotonicity check skipped when |F_n|=0.
# ---------------------------------------------------------------------------


class TestMonotonicitySkippedWhenEmpty:
    """The monotonicity emitter is gated on ``|F_n| > 0``. With an
    empty F-set on cycle 1, the loop terminates and the emitter is
    never consulted (no HALT-MONOTONICITY token in the log)."""

    def test_empty_fset_short_circuits(self):
        cycles = [
            CycleState(
                cycle=1,
                fail_set=set(),
                pass_set={"1.1", "2.1", "3.2"},
            ),
        ]
        log = run_fix_cycle(cycles)
        assert log.halt_message is None, (
            f"unexpected halt with |F_1|=0: {log.halt_message!r}"
        )
        joined = "\n".join(log.lines)
        assert "HALT-MONOTONICITY" not in joined, (
            "monotonicity emitter consulted despite |F_1|=0 short-circuit"
        )

    def test_no_transition_when_only_one_cycle(self):
        cycles = [
            CycleState(
                cycle=1,
                fail_set=set(),
                pass_set={"1.1", "2.1", "3.2"},
            ),
        ]
        log = run_fix_cycle(cycles)
        assert log.transitions == [], (
            f"unexpected transitions emitted for single-cycle run: {log.transitions}"
        )


# ---------------------------------------------------------------------------
# AC5 — Canonical D-0056 synthetic fixture log parity.
# ---------------------------------------------------------------------------


class TestCanonicalFixtureParity:
    """The TEST-015 runtime emission and the D-0056 canonical
    synthetic log agree on the load-bearing lines (HALT + halting
    transition). Drift between this pytest fixture and the D-0056
    log indicates either the protocol changed or the evidence pack
    is stale — both warrant follow-up before merge."""

    def test_canonical_log_present(self):
        assert CANONICAL_LOG.is_file(), (
            f"D-0056 canonical fixture missing at {CANONICAL_LOG} — "
            "T05.03 evidence pack regressed"
        )

    def test_canonical_log_halts_byte_exact(self, canonical_log_text: str):
        matches = [
            ln
            for ln in canonical_log_text.splitlines()
            if ln.startswith("HALT ")
        ]
        assert matches == ["HALT [HALT-MONOTONICITY] |F|=5"], (
            f"D-0056 canonical fixture HALT line(s) {matches!r} differ from "
            "byte-exact 'HALT [HALT-MONOTONICITY] |F|=5'"
        )

    def test_canonical_log_has_no_cycle_3(self, canonical_log_text: str):
        assert "CYCLE 3" not in canonical_log_text, (
            "D-0056 canonical fixture unexpectedly references CYCLE 3"
        )

    def test_canonical_log_ordering_regression_then_monotonicity(
        self, canonical_log_text: str
    ):
        # On the cycle-2 → cycle-3 transition, the regression step
        # line must appear BEFORE the monotonicity step line.
        lines = canonical_log_text.splitlines()
        reg_idx: Optional[int] = None
        mon_idx: Optional[int] = None
        for idx, ln in enumerate(lines):
            if ln.startswith("TRANSITION 2->3 step=regression"):
                reg_idx = idx
            elif ln.startswith("TRANSITION 2->3 step=monotonicity"):
                mon_idx = idx
        assert reg_idx is not None, (
            "D-0056 canonical fixture missing 'TRANSITION 2->3 step=regression' line"
        )
        assert mon_idx is not None, (
            "D-0056 canonical fixture missing 'TRANSITION 2->3 step=monotonicity' line"
        )
        assert reg_idx < mon_idx, (
            f"D-0056 canonical fixture has monotonicity step (line {mon_idx}) "
            f"BEFORE regression step (line {reg_idx}) — 4-step ordering rule violated"
        )

    def test_runtime_and_canonical_halt_strings_match(
        self, halt_log: HaltLog, canonical_log_text: str
    ):
        runtime_halt = halt_log.halt_message
        canonical_halts = [
            ln[len("HALT ") :]
            for ln in canonical_log_text.splitlines()
            if ln.startswith("HALT ")
        ]
        assert canonical_halts == [runtime_halt], (
            f"runtime halt {runtime_halt!r} disagrees with D-0056 canonical "
            f"halt(s) {canonical_halts!r}"
        )


# ---------------------------------------------------------------------------
# Negative case — guard against false positives in the halt claim.
# ---------------------------------------------------------------------------


class TestStrictShrinkDoesNotHalt:
    """Sanity: legitimate slow convergence (|F|=5,4) must NOT trigger
    the monotonicity halt. If this test fails, the emitter is over-
    firing and X-003 rejection has regressed (cf. T05.14 / TEST-017)."""

    def test_slow_shrink_proceeds(self):
        cycles = [
            CycleState(
                cycle=1,
                fail_set={"2.1", "3.2", "5.4", "7.1", "9.3"},
                pass_set={"1.1", "4.2", "6.1", "8.2", "10.1", "11.1"},
            ),
            CycleState(
                cycle=2,
                fail_set={"2.1", "5.4", "7.1", "9.3"},  # 11.1 fixed
                pass_set={"1.1", "3.2", "4.2", "6.1", "8.2", "10.1", "11.1"},
            ),
        ]
        log = run_fix_cycle(cycles)
        assert log.halt_message is None, (
            f"slow-shrink |F|=5,4 triggered unexpected halt: {log.halt_message!r} "
            "(X-003 'shrinks too slowly' threshold must remain REJECTED)"
        )
