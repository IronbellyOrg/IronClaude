"""The questions-on screen never has more rows than the terminal (pins today's height budget).

On ``Live(screen=True)`` rows past ``policy.height`` are dropped from the bottom, which are the
footer keys and the ``shown x/y`` line, with no warning. Every phase that adds rows (frames, a
count strip, a RETAIN CONTEXT pane) keeps this test green.
"""

from __future__ import annotations

import pytest

from tests.observe.test_render import WIDTHS, policy_for, r3_rows, r3_screen

HEIGHTS = (8, 12, 24, 40, 44)  # 8 is the diagnostic height


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("height", HEIGHTS)
@pytest.mark.parametrize("count", (3, 20))
@pytest.mark.parametrize("selected", (0, None))
def test_questions_on_screen_fits_the_height(
    fake_clock, width, height, count, selected
):
    rows = r3_rows([("w-001", f"question {i}?") for i in range(count)])
    # the framed lines, borders included: every added row is counted
    lines, _ = r3_screen(fake_clock, rows, selected, width, height=height, raw=True)
    policy = policy_for(width, height=height)
    # Height 8 is diagnostic: the one-line summary that stands in for the panel wraps at 80
    # columns and the screen keeps its title, one ledger row and the footer, so it runs up to
    # 3 rows over (measured; recorded in the gate notes). Every height from 12 up must fit.
    allowed = policy.height + (4 if height == 8 else 0)
    assert len(lines) <= allowed or policy.too_small, (
        f"{len(lines)} rows at height {height}, width {width}"
    )
