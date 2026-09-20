"""T5 locus card — R-01 acceptance test. Harness §3 T5."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import (
    derive_same_env,
    locus_complete,
    parse_locus,
    requires_runs_in,
)

FIX = Path(__file__).parent / "fixtures" / "procedures" / "locus"


def test_complete_card_ok() -> None:
    """R-01: a complete locus card is accepted."""
    ok, missing = locus_complete((FIX / "complete.md").read_text())
    assert ok, missing
    d = parse_locus((FIX / "complete.md").read_text())
    assert d["RUN-SITE"], d


def test_missing_run_site_fails_wave1() -> None:
    """R-01: missing RUN-SITE fails Wave 1 completeness."""
    ok, missing = locus_complete((FIX / "missing-run-site.md").read_text())
    assert not ok, missing
    assert "RUN-SITE" in missing, missing


@pytest.mark.parametrize(
    "name,expect",
    [("one-env", "yes"), ("two-env", "no"), ("no-env", "unknown")],
    ids=["one-env", "two-env", "no-env"],
)
def test_same_env_derivation(name: str, expect: str) -> None:
    """R-01: SAME-ENV derives yes/no/unknown from issue labels."""
    assert derive_same_env((FIX / f"{name}.md").read_text()) == expect, name


@pytest.mark.parametrize(
    "issue,grounding,expected",
    [
        ("- symptom\n- retry", "", "unknown"),
        ("runner ci-a\n- symptom", "", "yes"),
        ("matrix:\n  runner:\n    - ci-a\n- symptom", "", "yes"),
        ("matrix:\n  - ci-a\n  - ci-b\n- symptom", "", "no"),
        ("env:\n  - ci-a\n\nSymptoms:\n  - retry", "", "yes"),
        ("runner:\n  - ci-a\nnotes:\n  - symptom", "", "yes"),
        ("runner: -\njob failed\n  - symptom", "", "unknown"),
        ("runner: ci-a", "runner: ci-b", "no"),
        ("runner:\n  -\njob failed", "", "unknown"),
        ("runner:\n- ci-a", "", "unknown"),
    ],
)
def test_environment_lists_are_scoped(
    issue: str, grounding: str, expected: str
) -> None:
    assert derive_same_env(issue, grounding) == expected


def test_card_without_runs_in_is_returned() -> None:
    """R-01: cards lacking runs-in= are returned when SAME-ENV is not yes."""
    card = (FIX / "complete.md").read_text().replace("runs-in=ci-runner-sysbox", "")
    assert requires_runs_in("## Claim\nno locus line\n", "no") is True
    assert requires_runs_in("runs-in=sysbox\n", "no") is False
    assert requires_runs_in(card, "yes") is False
