"""T19 menu equality — R-02 acceptance test. Harness §3 T19."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import (
    enumerate_producers,
    menu_equal,
    surviving_yes,
    write_producers_md,
)

FIX = Path(__file__).parent / "fixtures"
SRC = (FIX / "procedures" / "producers" / "io.sh").read_text()


@pytest.mark.parametrize("ok", [True, False], ids=["equal", "missing-one"])
def test_menu_equality(ok: bool, tmp_path: Path) -> None:
    """R-02: prompt enum count equals surviving=yes; mismatch is False."""
    p = enumerate_producers({"io.sh": SRC}, "runner-unavailable", "rc")
    md = write_producers_md(p, tmp_path / "producers.md")
    n = surviving_yes(md)
    full = " ".join(f"`tok-{i}-x`" for i in range(n))
    if ok:
        assert menu_equal(full, md) is True, (n, md)
    else:
        assert menu_equal("`tok-0-x`", md) is False, n
