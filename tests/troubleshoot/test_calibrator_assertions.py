"""T2 calibrator assertions — R-14/R-19 acceptance test. Harness §3 T2."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._assertions import (
    calibrator_inputs,
    evaluate_calibrator,
    fired_flags,
    load_fixture,
)

FIX = Path(__file__).parent / "fixtures"
C_FILES = sorted(FIX.glob("assertions/C*/*/*.md"))


def _case_id(path: Path) -> str:
    return f"{path.parent.parent.name}-{path.parent.name}-{path.stem}"


@pytest.mark.parametrize("fixture_path", C_FILES, ids=[_case_id(p) for p in C_FILES])
def test_calibrator_fixture_fires_expected_flags(fixture_path: Path) -> None:
    """R-19 T2: each C-fixture fires exactly its expected flag set."""
    fx = load_fixture(fixture_path)
    got = fired_flags(fx)
    exp = set(fx.meta["expected_flags"] or [])
    assert got == exp, f"{fixture_path}: flags {got} != {exp}"


def test_c1_forces_escalate() -> None:
    """R-14 C1: verdict is ESCALATE on a C1 pos fixture."""
    fx = load_fixture(FIX / "assertions/C1/io/pos.md")
    result = evaluate_calibrator(calibrator_inputs(fx))
    assert result.verdict == "ESCALATE", result.verdict


def test_c2_zeroes_runtime_check() -> None:
    """R-14 C2: Runtime check dimension is 0.0."""
    fx = load_fixture(FIX / "assertions/C2/io/pos.md")
    result = evaluate_calibrator(calibrator_inputs(fx))
    assert result.dims["Runtime check"] == 0.0, result.dims


def test_c6_caps_calibrated_at_0_3() -> None:
    """R-14 C6: calibrated cap is 0.3."""
    fx = load_fixture(FIX / "assertions/C6/io/pos.md")
    result = evaluate_calibrator(calibrator_inputs(fx))
    assert result.cap == 0.3, result.cap


def test_c7_c8_cap_calibrated_at_0_5() -> None:
    """R-14 C7/C8: calibrated cap is 0.5."""
    c7 = evaluate_calibrator(
        calibrator_inputs(load_fixture(FIX / "assertions/C7/io/pos.md"))
    )
    c8 = evaluate_calibrator(
        calibrator_inputs(load_fixture(FIX / "assertions/C8/io/pos.md"))
    )
    assert c7.cap == 0.5, c7.cap
    assert c8.cap == 0.5, c8.cap
