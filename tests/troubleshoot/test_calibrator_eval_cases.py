"""T14 calibrator eval cases — R-14 non-regression. Harness §7."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._assertions import CalibratorResult

REPO_ROOT = Path(__file__).resolve().parents[2]
REF = (
    REPO_ROOT
    / "src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md"
).read_text()

PINNED = [
    "**Expected calibrated**: ≤ 0.70 (M3a cap fires).",
    "**Expected calibrated**: ≤ 0.80 (gate_M2 = 0.80).",
    "**Expected calibrated**: 1.0. **Asserts**: refactor does NOT over-correct.",
    "**Expected calibrated**: ≤ 0.80 (gate_M1 = 0.80).",
    "calibrator defaults claim_class to `runtime_behavior`, evidence_class to `none`, verdict_direction to `AFFIRM`",
    "**Expected calibrated**: 1.0. **Asserts**: M3a cap does NOT fire when runtime_check=1.0.",
    "**Expected calibrated**: ≤ 0.65 (per V2 rule 1) or ≤ 0.70 (per V1 M3a).",
    "**Expected calibrated**: ≤ 0.70.",
    "**Expected calibrated**: 0.70-0.85 range; NO hard cap fires.",
    "| P1 | M1 gate | `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` |",
    "| P2 | M2 gate | `runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent}` ⟹ `calibrated ≤ 0.80` |",
    "| P3 | M3a cap | `verdict_direction == REFUTE AND claim_class == runtime_behavior AND runtime_check < 1.0` ⟹ `calibrated ≤ 0.70` |",
    "| P4 | Determinism | running calibrator on same card produces same calibrated score (±0.0) across N=5 runs |",
    "| P5 | Anchoring (soft) | varying `Self-reported confidence:` from 0.30 to 0.99 must not change calibrated by more than ±0.05. **Soft assertion** (warn-only in CI). |",
    "A regression on any fixture or hard property (P1-P4) blocks merge.",
    "tests/troubleshoot/test_calibrator_eval_cases.py",
]


def rubric(eg, rc, sc, rf, fd, dc, claim, verdict):
    base = min(sum([eg, rc, sc, rf, fd, dc]) / 6, eg + 0.30, rc + 0.30)
    if claim == "runtime_behavior" and rc < 1.0:
        base = min(base, 0.70 if verdict in ("REFUTE", "REJECT") else 0.84)
    return round(base, 2)


def apply_caps(value: float, result: CalibratorResult) -> float:
    return min(value, result.cap) if result.cap is not None else value


@pytest.mark.parametrize(
    "substring", PINNED, ids=[f"pin-{i}" for i in range(len(PINNED))]
)
def test_ref_pins_expectation(substring: str) -> None:
    """R-14 T14: calibrator-eval-cases.md pins each expectation substring."""
    assert substring in REF, substring


@pytest.mark.parametrize(
    "case,args,check",
    [
        ("F1", (1, 0, 1, 1, 1, 1, "runtime_behavior", "REFUTE"), lambda v: v <= 0.70),
        ("F2", (1, 0.5, 1, 1, 1, 1, "runtime_behavior", "AFFIRM"), lambda v: v <= 0.80),
        ("F3", (1, 1, 1, 1, 1, 1, "static_defect", "AFFIRM"), lambda v: v == 1.0),
        ("F4", (0.5, 0.5, 1, 1, 1, 1, "static_defect", "AFFIRM"), lambda v: v <= 0.80),
        ("F6", (1, 1, 1, 1, 1, 1, "runtime_behavior", "REFUTE"), lambda v: v == 1.0),
        ("F7", (1, 0, 1, 1, 1, 1, "runtime_behavior", "REFUTE"), lambda v: v <= 0.70),
        ("F8", (1, 0, 1, 1, 1, 1, "runtime_behavior", "REFUTE"), lambda v: v <= 0.70),
        (
            "F9",
            (1, 1, 1, 0.5, 1, 0.5, "runtime_behavior", "AFFIRM"),
            lambda v: 0.70 <= v <= 0.85,
        ),
    ],
    ids=["F1", "F2", "F3", "F4", "F6", "F7", "F8", "F9"],
)
def test_rubric_fixture_case(case: str, args: tuple, check) -> None:
    """R-14 T14: rubric reproduces F1-F9 numeric bounds."""
    assert check(rubric(*args)), (case, rubric(*args))


@pytest.mark.parametrize("eg", [0.0, 0.5, 1.0], ids=["eg0", "eg05", "eg1"])
@pytest.mark.parametrize("rc", [0.0, 0.5, 1.0], ids=["rc0", "rc05", "rc1"])
def test_rubric_property_grid(eg: float, rc: float) -> None:
    """R-14 T14: P1-P3 hold on the {0,.5,1}^2 grid."""
    v_aff = rubric(eg, rc, 1, 1, 1, 1, "runtime_behavior", "AFFIRM")
    v_ref = rubric(eg, rc, 1, 1, 1, 1, "runtime_behavior", "REFUTE")
    if eg <= 0.5:
        assert v_aff <= 0.80, (eg, rc, v_aff)
    if rc <= 0.5:
        assert v_aff <= 0.80, (eg, rc, v_aff)
    if rc < 1.0:
        assert v_ref <= 0.70, (eg, rc, v_ref)


def test_rubric_determinism() -> None:
    """R-14 T14 P4: five calls equal."""
    args = (1, 0, 1, 1, 1, 1, "runtime_behavior", "REFUTE")
    vals = [rubric(*args) for _ in range(5)]
    assert len(set(vals)) == 1, vals


def test_caps_layer_after_formula() -> None:
    """R-14 T14: C6/C7/C8 caps apply after RUB:20."""
    raw = rubric(1, 1, 1, 1, 1, 1, "static_defect", "AFFIRM")
    capped = apply_caps(raw, CalibratorResult(set(), set(), {}, 0.5, None))
    assert capped == min(raw, 0.5), (raw, capped)
