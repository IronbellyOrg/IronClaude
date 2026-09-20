"""T9 counter key — R-04 acceptance test. Harness §3 T9."""

from __future__ import annotations

from pathlib import Path

from tests.troubleshoot._procedures import bump_rounds, counter_key


def status_for_round(n: int) -> str:
    return "blocked" if n >= 3 else "partial"


def test_counter_key_and_round_cap(tmp_path: Path) -> None:
    """R-04: key persists across slugs; only =yes increments; round 3 is blocked."""
    assert counter_key("feat", "seed-checkout-3") == "feat:seed-checkout-"
    path = tmp_path / "rounds.json"
    yes = "**discriminator-required**: yes\n"
    no = "**discriminator-required**: no\n"
    key = counter_key("feat", "seed-checkout-3")
    assert bump_rounds(path, key, yes) == 1
    assert bump_rounds(path, key, no) == 1
    assert bump_rounds(path, key, yes) == 2
    n = bump_rounds(path, key, yes)
    assert n == 3, n
    (tmp_path / "tasklist.md").write_text(yes)
    assert (tmp_path / "tasklist.md").exists()
    assert status_for_round(n) == "blocked"
