"""T6 discriminator form — R-07 acceptance test. Harness §3 T6."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._assertions import ValidatorInputs, evaluate_validator
from tests.troubleshoot._procedures import outcome_match, parse_discriminator_form

FIX = Path(__file__).parent / "fixtures" / "procedures" / "discriminator"


@pytest.mark.parametrize(
    "form,vector,winner",
    [("io", "false", "A"), ("nonio", "true", "A")],
    ids=["io", "nonio"],
)
def test_form_parses_and_exactly_one_row_matches(
    form: str, vector: str, winner: str
) -> None:
    """R-07: form parses; exactly one outcome row; A9 fires on reference mismatch."""
    text = (FIX / f"{form}.md").read_text()
    parsed = parse_discriminator_form(text)
    matched = outcome_match(parsed, {parsed.observable: vector})
    assert matched is not None, parsed.table
    assert matched[0] == winner, matched
    ref = parsed.reference_value
    other = "false" if ref == "true" else "true"
    obs = f"reference arm: {parsed.observable}={other}\n"
    result = evaluate_validator(ValidatorInputs(report=text, observation_text=obs))
    assert "probe_suspect" in result.flags, result.flags
