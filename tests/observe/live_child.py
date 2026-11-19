"""Live-screen child: draws one questions screen through the real ``LiveScreen`` on a pty.

Run only by ``test_live_screen_pty.py``. It reads the terminal size and the environment the way
the command does (``detect_size``, ``resolve_policy``), draws once, prints ``LIVE_READY`` and
waits for one line on stdin, then closes the screen so the alternate screen is left cleanly.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from superclaude.cli.observe.commands import LiveScreen  # noqa: E402
from superclaude.cli.observe.terminal import (  # noqa: E402
    detect_size,
    output_encoding,
    resolve_policy,
)
from tests.observe.conftest import FakeClock  # noqa: E402
from tests.observe.test_render import r3_rows, r3_screen  # noqa: E402


def main() -> int:
    width, height = detect_size()
    policy = resolve_policy(os.environ, output_encoding(), {}, width, height)
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?"), ("w-003", "third?")])
    _, view = r3_screen(FakeClock(), rows, 1, width, height)
    screen = LiveScreen()
    screen.draw(view, policy, None)
    sys.stdout.write("LIVE_READY\n")
    sys.stdout.flush()
    sys.stdin.readline()
    screen.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
