"""T1 validator assertions — R-14/R-19 acceptance test. Harness §3 T1."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._assertions import (
    evaluate_validator,
    fired_flags,
    fired_ids,
    load_fixture,
    validator_inputs,
)

FIX = Path(__file__).parent / "fixtures"
A_FILES = sorted(FIX.glob("assertions/A*/*/*.md"))


def _case_id(path: Path) -> str:
    return f"{path.parent.parent.name}-{path.parent.name}-{path.stem}"


@pytest.mark.parametrize("fixture_path", A_FILES, ids=[_case_id(p) for p in A_FILES])
def test_validator_fixture_fires_expected_flags(fixture_path: Path) -> None:
    """R-19 T1: each A-fixture fires exactly its expected flag set."""
    fx = load_fixture(fixture_path)
    got = fired_flags(fx)
    exp = set(fx.meta["expected_flags"] or [])
    assert got == exp, f"{fixture_path}: flags {got} != {exp}"
    ids = fired_ids(fx)
    if str(fx.meta.get("polarity")) == "pos" or "pos" in fixture_path.stem:
        assert ids, f"{fixture_path}: pos fixture fired no ids"


def test_validator_status_mapping() -> None:
    """R-14: status precedence FAIL > blocked > partial."""
    a7 = evaluate_validator(
        validator_inputs(load_fixture(FIX / "assertions/A7/io/pos.md"))
    )
    a8 = evaluate_validator(
        validator_inputs(load_fixture(FIX / "assertions/A8/io/pos.md"))
    )
    a1 = evaluate_validator(
        validator_inputs(load_fixture(FIX / "assertions/A1/io/pos.md"))
    )
    assert a7.status == "FAIL", a7.status
    assert a8.status == "blocked", a8.status
    assert a1.status == "partial", a1.status
