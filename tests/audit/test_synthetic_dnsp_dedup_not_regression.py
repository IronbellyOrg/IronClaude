"""TEST-022 — cross-cycle synthetic-dnsp dedup is NOT a regression (R-107 / INV-012).

Phase-5 / T05.14 deliverable (D-0065). Codifies the INV-012
cross-cycle dedup composition rule documented at SKILL.md
L1061-1079: a synthetic-dnsp finding emitted with an identical
``dedup_key = (assigned_files_range, escalation_ladder_exhaust_point)``
across consecutive fix cycles is a DEDUP case, NOT a regression.
Its prior-cycle verdict was already FAIL, not PASS, so the Step 1
set predicate ``dedup_key ∈ PASS_n ∩ FAIL_{n+1}`` is FALSE by
construction.

The cross-cycle persistence contributes ``1`` (not ``2``) to
``|F_{n+1}|`` per the dedup-key identity rule (SKILL.md L1050).
If the rest of the fail-set shrinks, the loop continues; if the
cardinality is non-shrinking, monotonicity halts — the intended
behavior (the partition agent is stuck on the same dedup_key).

This fixture exercises the SHRINKING case (the loop continues to
cycle 3 per the task spec: "TEST-022 synthetic with same dedup_key
in cycles 1+2 proceeds to cycle 3 (INV-012)"). It mirrors the
canonical D-0059 ``fixture-cross-cycle-dedup-shrinking.log``.

Asserted invariants:

1. The runtime emits ZERO halt of any kind on the shrinking
   fixture — no ``HALT-MONOTONICITY``, no regression halt-message,
   no hard-cap HALT line.
2. The regression check verdict at the cycle-1 → cycle-2
   transition is PASS — synthetic-dnsp persistence does NOT
   trigger the regression halt despite the synthetic appearing in
   both F_1 AND F_2.
3. ``|F_2| < |F_1|`` (strict shrink: 2 < 3) is verified at runtime;
   monotonicity step returns PROCEED.
4. ``CYCLE 3 START`` is attempted; cycle 3 converges with
   ``|F_3|=0`` (the partition recovered).
5. The non-shrinking counterfactual (synthetic persists AND nothing
   else changes, so ``|F|=2,2``) DOES halt with the byte-exact
   monotonicity message — proving that the INV-012 regression-non-
   emission invariant is load-bearing (it does NOT suppress the
   monotonicity halt; the synthetic still counts as a real failure).
6. The SKILL.md §A.9 INV-012 composition rule still encodes the
   "contributes 1 (not 2)" wording and the "Regression non-emission
   invariant" clause for synthetic-dnsp persistence.
7. The generated log shape matches the canonical D-0059 synthetic
   fixture at the load-bearing transition + cycle-3 spawn lines.

Acceptance reference (phase-5-tasklist.md L676-679):
- ``uv run pytest tests/audit/test_synthetic_dnsp_dedup_not_regression.py -v`` exits 0.
- TEST-022 assertion: no regression halt emitted for cross-cycle dedup.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0065/evidence.md``.

Run: ``uv run pytest tests/audit/test_synthetic_dnsp_dedup_not_regression.py -v``
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# Allow ``from _halt_emitter import ...`` regardless of how pytest
# composes sys.path for tests/audit/. TEST-022 reuses the same
# 4-step iterator as TEST-015 / TEST-016 / TEST-017 so the dedup-key
# identity rule (Set[str] semantics in ``CycleState.fail_set``) is
# exercised against the actual emitter whose halt strings the rest
# of the M5 fixtures verify byte-for-byte.
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
    / "D-0059"
    / "fixture-cross-cycle-dedup-shrinking.log"
)

CANONICAL_LOG_NON_SHRINKING = (
    REPO_ROOT
    / ".dev"
    / "releases"
    / "complete"
    / "task-builder-merge"
    / "artifacts"
    / "D-0059"
    / "fixture-cross-cycle-dedup-non-shrink.log"
)

# Synthetic-dnsp dedup_key per the canonical D-0059 fixture. The
# helper's Set[str] semantics collapse identical entries — so
# emitting the same dedup_key string in both cycle 1 and cycle 2
# contributes 1 element to each |F_n|, exactly per SKILL.md L1050.
SYNTH_DEDUP_KEY = "synth[(src/api/auth.py:42-118, llm_timeout)]"


# ---------------------------------------------------------------------------
# Fixtures — shrinking + non-shrinking cross-cycle dedup.
# ---------------------------------------------------------------------------


# SHRINKING case (the primary TEST-022 fixture).
#
# Cycle 1: F_1 = {item-3.1, item-3.2, synth-K}; |F_1|=3.
# Cycle 2: F_2 = {item-3.2, synth-K}; |F_2|=2 (item-3.1 fixed).
# Cycle 3: F_3 = ∅ (everything fixed, including synth-K — the
# partition recovered).
#
# Regression check at TRANSITION 2->3 (the first transition between
# cycle 1 and cycle 2 in the helper's labeling):
#   PASS_1 ∩ FAIL_2 = ∅ because:
#     - item-3.2 was FAIL_1 (NOT in PASS_1), so not a regression.
#     - synth-K was FAIL_1 (NOT in PASS_1), so not a regression —
#       this is the INV-012 invariant in action.
#
# Monotonicity check at TRANSITION 2->3: |F_2|=2 < |F_1|=3 → PROCEED.
F_CROSS_CYCLE_DEDUP_SHRINKING = [
    CycleState(
        cycle=1,
        fail_set={"item-3.1", "item-3.2", SYNTH_DEDUP_KEY},
        pass_set={"item-1.1", "item-4.2", "item-6.1", "item-8.2"},
    ),
    CycleState(
        cycle=2,
        fail_set={"item-3.2", SYNTH_DEDUP_KEY},
        pass_set={"item-1.1", "item-3.1", "item-4.2", "item-6.1", "item-8.2"},
    ),
    CycleState(
        cycle=3,
        fail_set=set(),
        pass_set={
            "item-1.1",
            "item-3.1",
            "item-3.2",
            "item-4.2",
            "item-6.1",
            "item-8.2",
            SYNTH_DEDUP_KEY,
        },
    ),
]

# NON-SHRINKING counterfactual.
#
# Cycle 1: F_1 = {item-3.1, synth-K}; |F_1|=2.
# Cycle 2: F_2 = {item-3.2, synth-K}; |F_2|=2 (item-3.1 fixed,
#   item-3.2 newly fails — item-3.2 was PASS_1's complement so this
#   is NOT a regression; synth-K persists).
#
# This is the canonical D-0059 non-shrink fixture: the loop SHOULD
# halt via monotonicity at the cycle-1 → cycle-2 transition, with
# the byte-exact `[HALT-MONOTONICITY] |F|=2` message. The
# regression check still returns PASS (synth-K's persistence is
# NOT a regression by the dedup-key identity rule).
F_CROSS_CYCLE_DEDUP_NON_SHRINKING = [
    CycleState(
        cycle=1,
        fail_set={"item-3.1", SYNTH_DEDUP_KEY},
        # item-3.2 is in PASS_1 so a FAIL@2 of item-3.2 WOULD be a
        # regression — we deliberately DON'T do that here. Instead
        # we let a brand-new item-3.4 fail at cycle 2 (so the
        # regression path stays clean and the test isolates the
        # monotonicity behavior on synthetic persistence).
        pass_set={"item-1.1", "item-3.2", "item-4.2", "item-6.1", "item-8.2"},
    ),
    CycleState(
        cycle=2,
        # item-3.1 fixed (FAIL→PASS); item-3.4 newly fails (was NOT
        # in PASS_1's set per the construction below — see comment
        # in cycle 1's pass_set). synth-K persists. |F_2|=2 = |F_1|.
        fail_set={"item-3.4", SYNTH_DEDUP_KEY},
        pass_set={
            "item-1.1",
            "item-3.1",
            "item-3.2",
            "item-4.2",
            "item-6.1",
            "item-8.2",
        },
    ),
]


@pytest.fixture(scope="module")
def shrinking_log() -> HaltLog:
    return run_fix_cycle(F_CROSS_CYCLE_DEDUP_SHRINKING)


@pytest.fixture(scope="module")
def non_shrinking_log() -> HaltLog:
    return run_fix_cycle(F_CROSS_CYCLE_DEDUP_NON_SHRINKING)


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
# Static schema / source guards — SKILL.md INV-012 wording.
# ---------------------------------------------------------------------------


class TestSkillInv012Documented:
    """SKILL.md §A.9 still encodes the INV-012 cross-cycle dedup
    composition rule + the regression non-emission invariant. A
    regression to "synthetic-dnsp persistence IS a regression"
    would silently break this test suite."""

    def test_skill_src_exists(self):
        assert SKILL_SRC.is_file(), f"missing SKILL.md at {SKILL_SRC}"

    def test_inv_012_label_present(self, skill_text: str):
        assert "INV-012" in skill_text, (
            "SKILL.md missing 'INV-012' label — cross-cycle dedup composition "
            "rule undocumented"
        )

    def test_inv_012_contributes_one_not_two(self, skill_text: str):
        # The literal "contributes `1` (not `2`)" appears in
        # SKILL.md L1065-1067 per the INV-012 operational rule.
        assert "contributes `1` (not `2`)" in skill_text, (
            "SKILL.md missing the 'contributes `1` (not `2`)' clause — "
            "INV-012 cross-cycle dedup composition rule undocumented"
        )

    def test_regression_non_emission_invariant_present(self, skill_text: str):
        # The literal "Regression non-emission invariant" appears in
        # SKILL.md L1077 per the INV-012 wire-level invariant.
        assert "Regression non-emission invariant" in skill_text, (
            "SKILL.md missing the 'Regression non-emission invariant' "
            "clause — cross-cycle synthetic-dnsp behavior undocumented"
        )

    def test_dedup_key_identity_rule_present(self, skill_text: str):
        # The dedup-key identity rule appears in SKILL.md L1050.
        assert "AFTER dedup-key deduplication" in skill_text, (
            "SKILL.md missing the 'AFTER dedup-key deduplication' clause "
            "— |F_n| cardinality semantics undocumented"
        )


# ---------------------------------------------------------------------------
# AC1 — SHRINKING case emits ZERO halts.
# ---------------------------------------------------------------------------


class TestShrinkingCaseEmitsNoHalt:
    """Strict shrink (|F|=3,2) with synthetic-dnsp persistence MUST
    proceed past the cycle-1 → cycle-2 transition. No halt of any
    kind is emitted."""

    def test_halt_message_is_none(self, shrinking_log: HaltLog):
        assert shrinking_log.halt_message is None, (
            f"cross-cycle dedup shrinking fixture emitted unexpected halt: "
            f"{shrinking_log.halt_message!r} — INV-012 regressed (synthetic "
            "persistence misclassified as regression OR monotonicity)"
        )

    def test_no_halt_line_in_log(self, shrinking_log: HaltLog):
        halt_lines = [ln for ln in shrinking_log.lines if ln.startswith("HALT ")]
        assert halt_lines == [], (
            f"cross-cycle dedup shrinking fixture emitted HALT line(s): "
            f"{halt_lines!r} — loop must continue per INV-012"
        )

    def test_no_regression_halt_anywhere(self, shrinking_log: HaltLog):
        # The load-bearing assertion (Acceptance Criterion AC3 of the
        # tasklist row): "no regression halt emitted for cross-cycle
        # dedup". Even though synth-K appears in BOTH F_1 and F_2,
        # the regression emitter must NOT fire.
        joined = "\n".join(shrinking_log.lines)
        assert "HALT Regression" not in joined, (
            "regression halt unexpectedly emitted for cross-cycle synthetic-"
            "dnsp persistence — INV-012 regression non-emission invariant "
            "violated (SKILL.md L1077-1079)"
        )
        assert "Regression detected on Item" not in joined, (
            "regression halt-message string unexpectedly present in log "
            "for cross-cycle synthetic-dnsp persistence"
        )

    def test_no_monotonicity_halt_anywhere(self, shrinking_log: HaltLog):
        joined = "\n".join(shrinking_log.lines)
        assert "HALT-MONOTONICITY" not in joined, (
            "monotonicity halt unexpectedly emitted on strict-shrink "
            "cross-cycle dedup fixture — emitter over-fired"
        )


# ---------------------------------------------------------------------------
# AC2 — Regression step verdict is PASS at the cycle-1 → cycle-2 transition.
# ---------------------------------------------------------------------------


class TestRegressionStepReturnsPass:
    """At the cycle-1 → cycle-2 transition (TRANSITION 2->3 in the
    helper's labeling), the regression check must return PASS. The
    synthetic-dnsp dedup_key persists across F_1 and F_2, but
    PASS_1 ∩ FAIL_2 = ∅ because synth-K was FAIL_1 (not PASS_1).
    This is the INV-012 invariant in action."""

    def test_regression_verdict_is_pass(self, shrinking_log: HaltLog):
        first_transition = [t for t in shrinking_log.transitions if t[0] == 3]
        regression_steps = [t for t in first_transition if t[1] == "regression"]
        assert len(regression_steps) == 1, (
            f"expected exactly one regression step at TRANSITION 2->3, "
            f"got {len(regression_steps)}: {regression_steps}"
        )
        assert regression_steps[0][2] == "PASS", (
            f"regression verdict at TRANSITION 2->3 is "
            f"{regression_steps[0][2]!r}, expected 'PASS' — synthetic-dnsp "
            "persistence must NOT trigger regression halt (INV-012)"
        )

    def test_synth_key_present_in_both_fail_sets(self):
        # Sanity: the dedup_key is in BOTH F_1 and F_2. If we
        # accidentally omitted it from one of them, the
        # "persistence" claim is vacuous.
        assert SYNTH_DEDUP_KEY in F_CROSS_CYCLE_DEDUP_SHRINKING[0].fail_set, (
            "synth dedup_key not in F_1 — fixture invariant broken"
        )
        assert SYNTH_DEDUP_KEY in F_CROSS_CYCLE_DEDUP_SHRINKING[1].fail_set, (
            "synth dedup_key not in F_2 — persistence claim vacuous"
        )

    def test_synth_key_not_in_pass_set_of_cycle_1(self):
        # The INV-012 invariant depends on synth-K being a FAIL_1
        # item (NOT a PASS_1 item). If it were in PASS_1, then its
        # FAIL_2 verdict WOULD be a regression — which is exactly
        # what INV-012 says happens by construction (synthetic-dnsp
        # findings emit at FAIL verdicts, never PASS).
        assert SYNTH_DEDUP_KEY not in F_CROSS_CYCLE_DEDUP_SHRINKING[0].pass_set, (
            "synth dedup_key incorrectly placed in PASS_1 — INV-012 "
            "non-emission invariant cannot be tested if the dedup_key "
            "starts as a PASS item"
        )


# ---------------------------------------------------------------------------
# AC3 — Cycle 3 IS attempted (loop continues).
# ---------------------------------------------------------------------------


class TestLoopProceedsToCycle3:
    """The tasklist row's primary assertion: "TEST-022 synthetic
    with same dedup_key in cycles 1+2 proceeds to cycle 3
    (INV-012)". Cycle 3 must be spawned and recorded in the log."""

    def test_cycle_3_in_cycles_started(self, shrinking_log: HaltLog):
        assert 3 in shrinking_log.cycles_started, (
            f"cycle 3 NOT attempted: cycles_started={shrinking_log.cycles_started} "
            "— INV-012 regressed (cross-cycle dedup falsely halted the loop)"
        )

    def test_cycle_3_start_line_present(self, shrinking_log: HaltLog):
        cycle_3_lines = [ln for ln in shrinking_log.lines if "CYCLE 3 START" in ln]
        assert len(cycle_3_lines) == 1, (
            f"expected exactly one 'CYCLE 3 START' line, got "
            f"{len(cycle_3_lines)}: {cycle_3_lines}"
        )

    def test_monotonicity_step_proceed_at_first_transition(
        self, shrinking_log: HaltLog
    ):
        first_transition = [t for t in shrinking_log.transitions if t[0] == 3]
        mon_steps = [t for t in first_transition if t[1] == "monotonicity"]
        assert len(mon_steps) == 1, (
            f"expected exactly one monotonicity step at TRANSITION 2->3, "
            f"got {len(mon_steps)}: {mon_steps}"
        )
        assert mon_steps[0][2] == "PROCEED", (
            f"monotonicity verdict at TRANSITION 2->3 is "
            f"{mon_steps[0][2]!r}, expected 'PROCEED' (strict shrink 2 < 3)"
        )


# ---------------------------------------------------------------------------
# AC4 — Counterfactual: non-shrinking case HALTS via monotonicity.
# ---------------------------------------------------------------------------


class TestNonShrinkingCounterfactualHalts:
    """Constructive proof that the INV-012 regression non-emission
    invariant does NOT suppress the monotonicity halt — it ONLY
    suppresses the regression halt. With ``|F|=2,2`` and synth-K
    persisting, the monotonicity guard fires with the byte-exact
    message. This is the "persistence trips monotonicity (intended)"
    behavior documented at SKILL.md L1071-1072."""

    def test_counterfactual_halts_with_monotonicity(self, non_shrinking_log: HaltLog):
        assert non_shrinking_log.halt_message == "[HALT-MONOTONICITY] |F|=2", (
            f"counterfactual non-shrinking dedup fixture did NOT halt with "
            f"byte-exact '[HALT-MONOTONICITY] |F|=2': got "
            f"{non_shrinking_log.halt_message!r} — INV-012 cannot prove the "
            "non-emission invariant is scoped to regression only"
        )

    def test_counterfactual_regression_step_pass(self, non_shrinking_log: HaltLog):
        first_transition = [t for t in non_shrinking_log.transitions if t[0] == 3]
        regression_steps = [t for t in first_transition if t[1] == "regression"]
        assert len(regression_steps) == 1, (
            f"expected exactly one regression step at TRANSITION 2->3 in the "
            f"counterfactual, got {len(regression_steps)}: {regression_steps}"
        )
        assert regression_steps[0][2] == "PASS", (
            f"regression verdict at TRANSITION 2->3 (counterfactual) is "
            f"{regression_steps[0][2]!r}, expected 'PASS' — synthetic "
            "persistence must NEVER be classified as regression"
        )

    def test_counterfactual_cycle_3_never_started(self, non_shrinking_log: HaltLog):
        assert 3 not in non_shrinking_log.cycles_started, (
            "counterfactual non-shrinking dedup fixture unexpectedly attempted cycle 3"
        )


# ---------------------------------------------------------------------------
# AC5 — Canonical D-0059 synthetic fixture log parity.
# ---------------------------------------------------------------------------


class TestCanonicalFixtureParity:
    """The TEST-022 runtime emission and the D-0059 canonical
    synthetic logs agree on the load-bearing lines (no HALT in the
    shrinking case; byte-exact monotonicity HALT in the non-shrink
    case; cycle 3 attempted in the shrinking case)."""

    def test_canonical_shrinking_log_present(self):
        assert CANONICAL_LOG_SHRINKING.is_file(), (
            f"D-0059 shrinking fixture missing at {CANONICAL_LOG_SHRINKING} "
            "— T05.07 evidence pack regressed"
        )

    def test_canonical_non_shrinking_log_present(self):
        assert CANONICAL_LOG_NON_SHRINKING.is_file(), (
            f"D-0059 non-shrinking fixture missing at {CANONICAL_LOG_NON_SHRINKING}"
        )

    def test_canonical_shrinking_log_has_no_halt(self, canonical_shrinking_text: str):
        halt_lines = [
            ln for ln in canonical_shrinking_text.splitlines() if ln.startswith("HALT ")
        ]
        assert halt_lines == [], (
            f"D-0059 shrinking fixture HALT line(s) {halt_lines!r} — "
            "INV-012 regressed in the evidence pack"
        )

    def test_canonical_shrinking_log_has_cycle_3(self, canonical_shrinking_text: str):
        assert "CYCLE 3 START" in canonical_shrinking_text, (
            "D-0059 shrinking fixture missing 'CYCLE 3 START' — INV-012 "
            "primary behavior (proceeds to cycle 3) regressed in the "
            "evidence pack"
        )

    EXPECTED_NON_SHRINK_HALT_LINE = "HALT [HALT-MONOTONICITY] |F|=2"

    def test_canonical_non_shrinking_halt_byte_exact(
        self, canonical_non_shrinking_text: str
    ):
        halts = [
            ln
            for ln in canonical_non_shrinking_text.splitlines()
            if ln.startswith("HALT ")
        ]
        assert halts == [self.EXPECTED_NON_SHRINK_HALT_LINE], (
            f"D-0059 non-shrinking fixture HALT line(s) {halts!r} differ "
            f"from byte-exact {self.EXPECTED_NON_SHRINK_HALT_LINE!r}"
        )

    def test_canonical_non_shrinking_log_no_regression_halt(
        self, canonical_non_shrinking_text: str
    ):
        # Even in the non-shrinking case, the regression halt MUST
        # NOT fire — only the monotonicity halt is intended per
        # INV-012's "persistence trips monotonicity (intended)" rule.
        assert "HALT Regression" not in canonical_non_shrinking_text, (
            "D-0059 non-shrinking fixture unexpectedly contains a "
            "regression halt — INV-012 regression non-emission invariant "
            "violated in the evidence pack"
        )

    def test_canonical_non_shrinking_log_no_cycle_3(
        self, canonical_non_shrinking_text: str
    ):
        assert "CYCLE 3 START" not in canonical_non_shrinking_text, (
            "D-0059 non-shrinking fixture unexpectedly references "
            "'CYCLE 3 START' — monotonicity halt should have stopped the loop"
        )

    def test_runtime_and_canonical_non_shrink_halt_match(
        self, non_shrinking_log: HaltLog, canonical_non_shrinking_text: str
    ):
        canon_halts = [
            ln[len("HALT ") :]
            for ln in canonical_non_shrinking_text.splitlines()
            if ln.startswith("HALT ")
        ]
        assert canon_halts == [non_shrinking_log.halt_message], (
            f"runtime non-shrink halt {non_shrinking_log.halt_message!r} "
            f"disagrees with D-0059 canonical halt(s) {canon_halts!r}"
        )

    def test_canonical_shrinking_log_monotonicity_proceeds(
        self, canonical_shrinking_text: str
    ):
        # The canonical D-0059 fixture uses the "TRANSITION 1->2"
        # labeling (older convention) while the helper uses
        # "TRANSITION 2->3" — both record the same comparison
        # between cycle 1 and cycle 2 with monotonicity verdict
        # PROCEED. Match the canonical labeling here.
        lines = canonical_shrinking_text.splitlines()
        mon_idx: Optional[int] = None
        for idx, ln in enumerate(lines):
            if ln.startswith("TRANSITION 1->2 step=monotonicity"):
                mon_idx = idx
                assert "PROCEED" in ln, (
                    f"D-0059 shrinking monotonicity step at line {idx} did "
                    f"not record PROCEED: {ln!r}"
                )
                break
        assert mon_idx is not None, (
            "D-0059 shrinking fixture missing 'TRANSITION 1->2 step=monotonicity' line"
        )
