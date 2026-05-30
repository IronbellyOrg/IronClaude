"""TEST-016 — regression precedence halt on PASS@1/FAIL@2 (R-105 / FR-CONV.5 PR-02).

Phase-5 / T05.13 deliverable (D-0064). Codifies the canonical
regression-halt scenario whose synthetic execution-log shape was
demonstrated at T05.04 (D-0057 §1-§3, ``fixture-pass1-fail2-
shrinking.log`` + ``fixture-pass1-fail2-non-shrinking.log``).

The fixture mirrors the SKILL.md §A.9 "API-004 Fix-Loop Halt
Signals" wire contract by implementing the 4-step ordering rule
(regression → monotonicity → hard-cap → proceed) in pure Python
and asserting that the regression emitter fires BEFORE the
monotonicity step is consulted, with the byte-exact halt-message
wire string:

> ``Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.``

1. The emitted regression halt-message substitutes ``X.Y`` ← the
   regressed item ID and ``N`` ← the prior-PASS cycle number; the
   em-dash byte sequence (U+2014, ``e2 80 94``) appears at the
   correct offset; the trailing period is preserved.
2. The regression emitter fires on BOTH the shrinking-cardinality
   case (``|F|=5,4`` with Item 3.2 regressing) and the non-shrinking
   case (``|F|=5,5`` with Item 3.2 regressing) — proving the
   detection is by per-item PASS→FAIL flip, NOT by ``|F|``
   comparison.
3. The monotonicity step is NEVER consulted on a regressed
   transition: no ``HALT-MONOTONICITY`` token in the halt log,
   even in the non-shrinking case where step 2 would otherwise
   have fired with ``|F|=5``.
4. ``CYCLE 3 START`` is never emitted — the regression guard exits
   at the cycle-2 → cycle-3 transition before per-gate cap (3)
   could fire.
5. The SKILL.md §A.9 API-004 contract table still contains the
   byte-exact wire-string row for the regression halt, complete
   with the U+2014 em-dash.
6. The generated log shape matches the canonical D-0057 synthetic
   fixtures line-for-line at the load-bearing transition + halt
   lines.

Acceptance reference (phase-5-tasklist.md L630-633):
- ``uv run pytest tests/audit/test_regression_halt_pass1_fail2.py -v`` exits 0.
- Regression message emitted BEFORE monotonicity check.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0064/evidence.md``.

Run: ``uv run pytest tests/audit/test_regression_halt_pass1_fail2.py -v``
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# Allow ``from _halt_emitter import ...`` regardless of how pytest
# composes sys.path for tests/audit/. TEST-015 and TEST-016 share
# the same 4-step iterator so the precedence-rule assertions here
# are load-bearing against the exact emitter whose monotonicity
# output TEST-015 verifies byte-for-byte.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _halt_emitter import (  # noqa: E402
    CycleState,
    HaltLog,
    run_fix_cycle,
)

SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"

CANONICAL_LOG_SHRINKING = (
    REPO_ROOT
    / ".dev"
    / "releases"
    / "complete"
    / "task-builder-merge"
    / "artifacts"
    / "D-0057"
    / "fixture-pass1-fail2-shrinking.log"
)

CANONICAL_LOG_NON_SHRINKING = (
    REPO_ROOT
    / ".dev"
    / "releases"
    / "complete"
    / "task-builder-merge"
    / "artifacts"
    / "D-0057"
    / "fixture-pass1-fail2-non-shrinking.log"
)

# Byte-exact wire template frozen by API-004-M5 (SKILL.md §A.9, row 2
# of the halt-message table). The em-dash is U+2014 (``e2 80 94``),
# NOT an ASCII hyphen-minus.
REGRESSION_HALT_TEMPLATE = (
    "Regression detected on Item X.Y — previously PASS at cycle N, "
    "now FAIL. Halt overrides monotonicity check."
)

# Em-dash byte sequence (UTF-8 encoding of U+2014).
EM_DASH_BYTES = b"\xe2\x80\x94"


# ---------------------------------------------------------------------------
# Fixtures — two PASS@1/FAIL@2 scenarios.
# ---------------------------------------------------------------------------


# Shrinking cardinality: |F_1|=5, |F_2|=4. If monotonicity were
# consulted, it would PROCEED (strict shrink). Regression must fire
# first per the 4-step ordering rule.
F_PASS1_FAIL2_SHRINKING = [
    CycleState(
        cycle=1,
        fail_set={"2.1", "5.4", "7.1", "9.3", "11.1"},
        pass_set={"1.1", "3.2", "4.2", "6.1", "8.2", "10.1"},
    ),
    CycleState(
        cycle=2,
        # 3.2 flipped PASS→FAIL (the regression). 11.1 was fixed
        # (legitimate refinement), so |F| shrinks 5→4.
        fail_set={"2.1", "3.2", "7.1", "9.3"},
        pass_set={"1.1", "4.2", "5.4", "6.1", "8.2", "10.1", "11.1"},
    ),
]

# Non-shrinking cardinality: |F_1|=5, |F_2|=5. If monotonicity were
# consulted, it would HALT (cardinality non-shrink AND |F_1|>0). The
# regression emitter must STILL exit first — this is the precedence
# proof.
F_PASS1_FAIL2_NON_SHRINKING = [
    CycleState(
        cycle=1,
        fail_set={"2.1", "5.4", "7.1", "9.3", "11.1"},
        pass_set={"1.1", "3.2", "4.2", "6.1", "8.2", "10.1"},
    ),
    CycleState(
        cycle=2,
        # 3.2 flipped PASS→FAIL (the regression). 11.1 was fixed,
        # but 5.4 stayed FAIL — net |F| identical: 5.
        fail_set={"2.1", "3.2", "5.4", "7.1", "9.3"},
        pass_set={"1.1", "4.2", "6.1", "8.2", "10.1", "11.1"},
    ),
]


@pytest.fixture(scope="module")
def shrinking_log() -> HaltLog:
    return run_fix_cycle(F_PASS1_FAIL2_SHRINKING)


@pytest.fixture(scope="module")
def non_shrinking_log() -> HaltLog:
    return run_fix_cycle(F_PASS1_FAIL2_NON_SHRINKING)


@pytest.fixture(scope="module")
def skill_text() -> str:
    return SKILL_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def canonical_shrinking_text() -> str:
    return CANONICAL_LOG_SHRINKING.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def canonical_non_shrinking_text() -> str:
    return CANONICAL_LOG_NON_SHRINKING.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Static schema / source guards.
# ---------------------------------------------------------------------------


class TestSkillContractWiringPresent:
    """SKILL.md §A.9 API-004 contract row 2 still contains the
    byte-exact regression wire template, including the em-dash."""

    def test_skill_src_exists(self):
        assert SKILL_SRC.is_file(), f"missing SKILL.md at {SKILL_SRC}"

    def test_regression_template_present(self, skill_text: str):
        assert REGRESSION_HALT_TEMPLATE in skill_text, (
            "SKILL.md missing byte-exact API-004 regression wire template"
        )

    def test_regression_template_uses_em_dash(self):
        # The template must encode the em-dash with the UTF-8 byte
        # sequence `e2 80 94`. A regression to ASCII `--` or hyphen
        # would silently break every downstream consumer.
        template_bytes = REGRESSION_HALT_TEMPLATE.encode("utf-8")
        assert EM_DASH_BYTES in template_bytes, (
            "API-004 regression template missing U+2014 em-dash byte sequence"
        )
        # Exactly one em-dash in the template per the SKILL.md L1040
        # invariant ("the em-dash ... is part of the wire string").
        assert template_bytes.count(EM_DASH_BYTES) == 1, (
            f"expected exactly one em-dash in template, got "
            f"{template_bytes.count(EM_DASH_BYTES)}"
        )

    def test_precedence_rule_documented(self, skill_text: str):
        assert "regression > monotonicity" in skill_text, (
            "SKILL.md must document 'regression > monotonicity' precedence"
        )

    def test_do_not_consult_subsequent_steps_documented(self, skill_text: str):
        # The "Do NOT consult subsequent steps" clause at SKILL.md:1054
        # is the load-bearing wire-level invariant that makes the
        # precedence rule actionable.
        assert "Do NOT consult subsequent steps" in skill_text, (
            "SKILL.md missing 'Do NOT consult subsequent steps' "
            "invariant — precedence rule is unenforceable without it"
        )


# ---------------------------------------------------------------------------
# AC1 — Byte-exact regression message on PASS@1/FAIL@2 fixture.
# ---------------------------------------------------------------------------


class TestRegressionMessageByteExact:
    """The emitter substitutes ``X.Y`` ← '3.2' and ``N`` ← 1 and
    produces the byte-exact wire string with the U+2014 em-dash."""

    EXPECTED_HALT = (
        "Regression detected on Item 3.2 — previously PASS at cycle 1, "
        "now FAIL. Halt overrides monotonicity check."
    )

    def test_shrinking_halt_message_byte_exact(self, shrinking_log: HaltLog):
        assert shrinking_log.halt_message == self.EXPECTED_HALT, (
            f"shrinking halt {shrinking_log.halt_message!r} differs from "
            f"byte-exact {self.EXPECTED_HALT!r}"
        )

    def test_non_shrinking_halt_message_byte_exact(self, non_shrinking_log: HaltLog):
        assert non_shrinking_log.halt_message == self.EXPECTED_HALT, (
            f"non-shrinking halt {non_shrinking_log.halt_message!r} differs from "
            f"byte-exact {self.EXPECTED_HALT!r}"
        )

    def test_halt_message_contains_em_dash(self, shrinking_log: HaltLog):
        assert shrinking_log.halt_message is not None
        payload = shrinking_log.halt_message.encode("utf-8")
        assert EM_DASH_BYTES in payload, (
            "emitted regression halt missing U+2014 em-dash byte sequence"
        )

    def test_halt_message_em_dash_at_expected_offset(self, shrinking_log: HaltLog):
        # Per D-0057 §1.1, the em-dash sits at offset 0x22 (34) of the
        # halt-payload (counting from the 'R' of 'Regression', NOT
        # from the optional 'HALT ' prefix). The fixed prefix
        # "Regression detected on Item 3.2 " is 32 bytes.
        assert shrinking_log.halt_message is not None
        payload = shrinking_log.halt_message.encode("utf-8")
        em_dash_idx = payload.find(EM_DASH_BYTES)
        assert em_dash_idx == 32, (
            f"em-dash offset {em_dash_idx} differs from D-0057 baseline 32 "
            "(byte position immediately after 'Regression detected on Item 3.2 ')"
        )

    def test_halt_message_ends_with_period(self, shrinking_log: HaltLog):
        assert shrinking_log.halt_message is not None
        assert shrinking_log.halt_message.endswith("."), (
            "emitted regression halt missing trailing period — wire-ABI "
            "drift from API-004 contract"
        )


# ---------------------------------------------------------------------------
# AC2 — Regression check runs FIRST (ordering invariant).
# ---------------------------------------------------------------------------


class TestRegressionPrecedence:
    """Both fixtures: at the cycle-2 → cycle-3 transition, the only
    transition step that runs is ``regression`` with verdict HALT.
    No subsequent step (monotonicity / hard-cap / proceed) is
    consulted, per SKILL.md:1054."""

    def test_shrinking_regression_is_only_step_at_halting_transition(
        self, shrinking_log: HaltLog
    ):
        halting = [t for t in shrinking_log.transitions if t[0] == 3]
        assert len(halting) == 1, (
            f"expected exactly one transition step at the halting boundary, "
            f"got {len(halting)}: {halting}"
        )
        assert halting[0][1] == "regression", (
            f"sole step at halting boundary is {halting[0][1]!r}, not 'regression'"
        )
        assert "HALT" in halting[0][2], (
            f"regression verdict at halting boundary is {halting[0][2]!r}, expected HALT"
        )

    def test_non_shrinking_regression_is_only_step_at_halting_transition(
        self, non_shrinking_log: HaltLog
    ):
        halting = [t for t in non_shrinking_log.transitions if t[0] == 3]
        assert len(halting) == 1, (
            f"expected exactly one transition step at the halting boundary "
            f"in non-shrinking case, got {len(halting)}: {halting} — "
            "precedence rule violated (monotonicity was consulted despite "
            "regression HALT)"
        )
        assert halting[0][1] == "regression"
        assert "HALT" in halting[0][2]

    def test_shrinking_halt_line_immediately_follows_regression_step(
        self, shrinking_log: HaltLog
    ):
        # The HALT emission line must appear AFTER the regression
        # step line in the emitted log; that proves the emitter
        # fires after the verdict transition, not before.
        lines = shrinking_log.lines
        reg_idx: Optional[int] = None
        halt_idx: Optional[int] = None
        for idx, ln in enumerate(lines):
            if ln.startswith("TRANSITION 2->3 step=regression"):
                reg_idx = idx
            if ln.startswith("HALT Regression"):
                halt_idx = idx
        assert reg_idx is not None, "missing regression step line"
        assert halt_idx is not None, "missing HALT Regression emission line"
        assert reg_idx < halt_idx, (
            f"HALT emission at line {halt_idx} precedes regression step at "
            f"line {reg_idx} — emitter ordering inverted"
        )


# ---------------------------------------------------------------------------
# AC3 — Monotonicity NOT consulted on regressed transition.
# ---------------------------------------------------------------------------


class TestMonotonicityNotConsultedOnRegression:
    """No ``HALT-MONOTONICITY`` token appears in either log, even in
    the non-shrinking case where the cardinality condition is met."""

    def test_shrinking_log_has_no_monotonicity_halt(self, shrinking_log: HaltLog):
        joined = "\n".join(shrinking_log.lines)
        assert "HALT-MONOTONICITY" not in joined, (
            "monotonicity halt token unexpectedly present on shrinking regression run"
        )

    def test_non_shrinking_log_has_no_monotonicity_halt(
        self, non_shrinking_log: HaltLog
    ):
        joined = "\n".join(non_shrinking_log.lines)
        assert "HALT-MONOTONICITY" not in joined, (
            "monotonicity halt token unexpectedly present on non-shrinking "
            "regression run — precedence rule violated (monotonicity would "
            "have fired with |F|=5 if step 2 had been consulted)"
        )

    def test_non_shrinking_cardinality_would_have_halted_monotonicity(self):
        """Sanity: prove monotonicity WOULD have fired (|F|=5,5) if
        the regression step had not exited first. Construct cycles
        with identical PASS→PASS overlap (no regression) and a NEW
        FAIL item at cycle 2 disjoint from PASS@1 (so |F| stays 5
        without flipping a previously-PASS item)."""
        no_regression_cycles = [
            CycleState(
                cycle=1,
                fail_set={"2.1", "5.4", "7.1", "9.3", "11.1"},
                pass_set={"1.1", "3.2", "4.2", "6.1", "8.2", "10.1"},
            ),
            CycleState(
                cycle=2,
                # 11.1 fixed (FAIL→PASS, refinement). New FAIL 12.1
                # appears (not in cycle-1 PASS set, so not a
                # regression). Cycle-1 PASS set ⊆ cycle-2 PASS set,
                # so no PASS→FAIL flip occurs. |F_2|=5 = |F_1|=5.
                fail_set={"2.1", "5.4", "7.1", "9.3", "12.1"},
                pass_set={"1.1", "3.2", "4.2", "6.1", "8.2", "10.1", "11.1"},
            ),
        ]
        log = run_fix_cycle(no_regression_cycles)
        assert log.halt_message == "[HALT-MONOTONICITY] |F|=5", (
            f"counterfactual scenario did NOT trigger monotonicity halt: "
            f"{log.halt_message!r} — precedence test cannot prove monotonicity "
            "would have fired absent the regression"
        )


# ---------------------------------------------------------------------------
# AC4 — Cycle 3 never attempted on regression HALT.
# ---------------------------------------------------------------------------


class TestCycle3NeverAttempted:
    """Both fixtures halt at the cycle-2 → cycle-3 transition; the
    per-gate counter stops at 2/3."""

    def test_shrinking_cycle_3_never_started(self, shrinking_log: HaltLog):
        assert 3 not in shrinking_log.cycles_started, (
            f"cycle 3 attempted: cycles_started={shrinking_log.cycles_started}"
        )

    def test_non_shrinking_cycle_3_never_started(self, non_shrinking_log: HaltLog):
        assert 3 not in non_shrinking_log.cycles_started, (
            f"cycle 3 attempted: cycles_started={non_shrinking_log.cycles_started}"
        )


# ---------------------------------------------------------------------------
# AC5 — Canonical D-0057 synthetic fixture log parity.
# ---------------------------------------------------------------------------


class TestCanonicalFixtureParity:
    """The TEST-016 runtime emission and the D-0057 canonical
    synthetic logs agree on the load-bearing lines (HALT + halting
    transition + em-dash presence)."""

    def test_canonical_shrinking_log_present(self):
        assert CANONICAL_LOG_SHRINKING.is_file(), (
            f"D-0057 shrinking fixture missing at {CANONICAL_LOG_SHRINKING}"
        )

    def test_canonical_non_shrinking_log_present(self):
        assert CANONICAL_LOG_NON_SHRINKING.is_file(), (
            f"D-0057 non-shrinking fixture missing at {CANONICAL_LOG_NON_SHRINKING}"
        )

    EXPECTED_CANONICAL_HALT_LINE = (
        "HALT Regression detected on Item 3.2 — previously PASS at cycle 1, "
        "now FAIL. Halt overrides monotonicity check."
    )

    def test_canonical_shrinking_halt_byte_exact(self, canonical_shrinking_text: str):
        halts = [
            ln for ln in canonical_shrinking_text.splitlines() if ln.startswith("HALT ")
        ]
        assert halts == [self.EXPECTED_CANONICAL_HALT_LINE], (
            f"D-0057 shrinking fixture HALT line(s) {halts!r} differ from "
            f"byte-exact {self.EXPECTED_CANONICAL_HALT_LINE!r}"
        )

    def test_canonical_non_shrinking_halt_byte_exact(
        self, canonical_non_shrinking_text: str
    ):
        halts = [
            ln
            for ln in canonical_non_shrinking_text.splitlines()
            if ln.startswith("HALT ")
        ]
        assert halts == [self.EXPECTED_CANONICAL_HALT_LINE], (
            f"D-0057 non-shrinking fixture HALT line(s) {halts!r} differ from "
            f"byte-exact {self.EXPECTED_CANONICAL_HALT_LINE!r}"
        )

    def test_canonical_no_monotonicity_halt_in_either_fixture(
        self, canonical_shrinking_text: str, canonical_non_shrinking_text: str
    ):
        for label, txt in (
            ("shrinking", canonical_shrinking_text),
            ("non-shrinking", canonical_non_shrinking_text),
        ):
            assert "HALT-MONOTONICITY" not in txt, (
                f"D-0057 {label} fixture unexpectedly contains "
                "HALT-MONOTONICITY token — precedence rule violated in evidence pack"
            )

    def test_canonical_no_cycle_3_in_either_fixture(
        self, canonical_shrinking_text: str, canonical_non_shrinking_text: str
    ):
        for label, txt in (
            ("shrinking", canonical_shrinking_text),
            ("non-shrinking", canonical_non_shrinking_text),
        ):
            assert "CYCLE 3" not in txt, (
                f"D-0057 {label} fixture unexpectedly references CYCLE 3"
            )

    def test_runtime_and_canonical_halt_strings_match(
        self,
        shrinking_log: HaltLog,
        non_shrinking_log: HaltLog,
        canonical_shrinking_text: str,
        canonical_non_shrinking_text: str,
    ):
        for log, canon_text, label in (
            (shrinking_log, canonical_shrinking_text, "shrinking"),
            (non_shrinking_log, canonical_non_shrinking_text, "non-shrinking"),
        ):
            canon_halts = [
                ln[len("HALT ") :]
                for ln in canon_text.splitlines()
                if ln.startswith("HALT ")
            ]
            assert canon_halts == [log.halt_message], (
                f"{label}: runtime halt {log.halt_message!r} disagrees with "
                f"canonical halt(s) {canon_halts!r}"
            )


# ---------------------------------------------------------------------------
# Negative case — guard against constant-emit regressions.
# ---------------------------------------------------------------------------


class TestNoRegressionAllowsLoopToContinue:
    """If no PASS→FAIL flip occurs across the transition, the
    regression emitter MUST NOT fire. The loop proceeds to step 2
    and onward."""

    def test_no_flip_no_regression_halt(self):
        cycles = [
            CycleState(
                cycle=1,
                fail_set={"2.1", "5.4", "7.1", "9.3", "11.1"},
                pass_set={"1.1", "3.2", "4.2", "6.1", "8.2", "10.1"},
            ),
            CycleState(
                cycle=2,
                # No PASS@1 item flips: 11.1 went FAIL→PASS
                # (legitimate refinement) which is NOT a regression.
                fail_set={"2.1", "5.4", "7.1", "9.3"},
                pass_set={"1.1", "3.2", "4.2", "6.1", "8.2", "10.1", "11.1"},
            ),
        ]
        log = run_fix_cycle(cycles)
        assert log.halt_message is None, (
            f"unexpected halt {log.halt_message!r} — no PASS→FAIL flip occurred"
        )
        joined = "\n".join(log.lines)
        assert "HALT Regression" not in joined, (
            "regression emitter fired despite no PASS→FAIL flip — "
            "constant-emit regression"
        )

    def test_fail_to_pass_is_not_a_regression(self):
        # Item 11.1 was FAIL at cycle 1 and PASS at cycle 2.
        # That is legitimate refinement, NOT regression.
        cycles = [
            CycleState(
                cycle=1,
                fail_set={"11.1"},
                pass_set={"1.1"},
            ),
            CycleState(
                cycle=2,
                fail_set=set(),
                pass_set={"1.1", "11.1"},
            ),
        ]
        log = run_fix_cycle(cycles)
        assert log.halt_message is None, (
            f"FAIL→PASS flip on 11.1 was misclassified as regression: "
            f"{log.halt_message!r}"
        )
