"""The real ``LiveScreen`` on a pty: alternate screen, colour depth, no blink, no mouse (Q5 live gate).

``Console(file=StringIO)`` writes nothing under ``Live(screen=True)``, so the live path is only
checked on a real pseudo-terminal. The child is ``live_child.py``.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pytest

pexpect = pytest.importorskip("pexpect")
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX pty test")

CHILD = Path(__file__).with_name("live_child.py")
ROOT = Path(__file__).resolve().parents[2]
SGR = re.compile(rb"\x1b\[([0-9;]*)m")
MOUSE = (b"\x1b[?1000h", b"\x1b[?1002h", b"\x1b[?1003h", b"\x1b[?1006h")


def run_child(env_extra: dict, rows: int = 40, cols: int = 160) -> bytes:
    """Everything the live screen wrote to the terminal, from start to a clean exit."""
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("COLUMNS", "LINES", "NO_COLOR", "COLORTERM", "TERM")
    }
    env["TERM"] = "xterm"
    env.update(env_extra)
    child = pexpect.spawn(
        sys.executable,
        [str(CHILD)],
        env=env,
        dimensions=(rows, cols),
        encoding=None,
        cwd=str(ROOT),
        timeout=60,
    )
    child.expect(b"LIVE_READY")
    before = child.before + b"LIVE_READY"
    child.sendline(b"")
    child.expect(pexpect.EOF)
    return before + child.before


def sgr_codes(data: bytes) -> list[int]:
    """Every SGR code in ``data``; the arguments of extended colours (38 and 48) are skipped."""
    codes: list[int] = []
    for match in SGR.finditer(data):
        params = [int(p) if p else 0 for p in match.group(1).split(b";")]
        i = 0
        while i < len(params):
            if params[i] in (38, 48) and i + 1 < len(params):
                i += 3 if params[i + 1] == 5 else 5
                continue
            codes.append(params[i])
            i += 1
    return codes


CSI = re.compile(rb"\x1b\[[0-9;?]*[A-Za-z]")


@pytest.mark.parametrize("rows", (24, 40))
def test_the_last_row_of_a_framed_screen_is_the_shown_x_of_y_footer(rows):
    """A frame row that overflows would push the footer off the bottom with no warning."""
    out = run_child({}, rows=rows)
    drawn = out.split(b"LIVE_READY")[0]
    text = CSI.sub(b"", drawn).decode("utf-8", errors="replace")
    lines = [ln.rstrip() for ln in text.replace("\r", "").split("\n") if ln.strip()]
    assert re.search(r"shown \d+/\d+$", lines[-1]), lines[-3:]
    assert any("COORDINATOR QUESTIONS" in ln for ln in lines)  # the frame was drawn


def test_the_live_screen_uses_the_alternate_screen_and_no_mouse_or_blink():
    out = run_child({})
    assert b"\x1b[?1049h" in out and b"\x1b[?1049l" in out  # entered and left cleanly
    assert not any(seq in out for seq in MOUSE)
    assert not {5, 6} & set(sgr_codes(out))  # no blink


def test_a_truecolor_terminal_gets_the_mockup_palette():
    out = run_child({"COLORTERM": "truecolor"})
    assert b"38;2;" in out


def test_a_256_colour_terminal_gets_indexed_colours_only():
    out = run_child({"TERM": "xterm-256color"})
    assert b"38;5;" in out and b"38;2;" not in out


def test_a_16_colour_terminal_gets_only_16_colour_codes():
    out = run_child({})
    codes = sgr_codes(out)
    assert codes and b"38;2;" not in out and b"38;5;" not in out
    assert all(c in (0, 1, 22) or 30 <= c <= 37 or 90 <= c <= 97 for c in codes)


def test_no_color_writes_no_colour_or_weight_codes():
    out = run_child({"NO_COLOR": "1", "COLORTERM": "truecolor"})
    assert b"\x1b[?1049h" in out
    # Measured: with NO_COLOR the console sets no style at all, so no SGR sequence is written.
    assert sgr_codes(out) == []
