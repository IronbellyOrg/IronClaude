"""Key-reader spike child: ``rich.live.Live(screen=True)`` repainting every 100 ms
while reading keys through ``KeySource``. Run only by ``test_keys_spike.py`` on a pty.

It waits for one line on stdin (still in cooked mode) so the test can read the
original terminal attributes first, then logs one event per line to the screen
and to the file given with ``--log``.
"""

from __future__ import annotations

import argparse
import sys
import time

from rich.console import Console, ConsoleOptions, RenderResult
from rich.live import Live
from rich.text import Text

from superclaude.cli.observe.keys import KeySource

REPAINT_SECONDS = 0.1


class _Screen:
    """Rendered on every repaint; reports the size Rich sees right now."""

    def __init__(self, log: "_Log") -> None:
        self.log = log
        self.repaints = 0

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        self.repaints += 1
        size = f"{options.size.width}x{options.size.height}"
        self.log.write(f"repaint n={self.repaints} size={size}")
        yield Text(f"SPIKE repaint={self.repaints} size={size}")
        for line in self.log.tail(5):
            yield Text(f"EVT:{line}")


class _Log:
    def __init__(self, path: str | None) -> None:
        self.path = path
        self.lines: list[str] = []

    def write(self, line: str) -> None:
        self.lines.append(line)
        if self.path:
            with open(self.path, "a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    def tail(self, count: int) -> list[str]:
        events = [x for x in self.lines if not x.startswith("repaint")]
        return events[-count:]


def run(mode: str, log: _Log) -> int:
    with KeySource() as keys:
        if not keys.available:
            log.write("unavailable")
            return 2
        screen = _Screen(log)
        with Live(screen, console=Console(), screen=True, auto_refresh=False) as live:
            log.write("ready")
            last = 0.0
            tick = 0
            while True:
                key = keys.read(0.05)
                if key is not None:
                    detail = key.name if key.name != "text" else f"text:{key.char}"
                    log.write(f"key:{detail}")
                    if key.name == "text" and key.char == "q":
                        log.write("quit")
                        return 0
                if keys.consume_redraw():
                    log.write("redraw")
                    last = 0.0
                now = time.monotonic()
                if now - last >= REPAINT_SECONDS:
                    last = now
                    tick += 1
                    live.update(screen, refresh=True)
                    if mode == "raise" and tick == 5:
                        raise RuntimeError("spike: exception inside the loop")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default=None)
    parser.add_argument("--mode", default="normal", choices=["normal", "raise"])
    args = parser.parse_args()
    log = _Log(args.log)
    sys.stdin.readline()  # cooked mode: the test reads the original attributes, then sends "go"
    try:
        return run(args.mode, log)
    except KeyboardInterrupt:
        log.write("interrupted")
        return 130


if __name__ == "__main__":
    sys.exit(main())
