"""R0 key-reader spike: Rich Live plus the stdlib ``KeySource`` on a real pseudo-terminal.

This is the only test module in ``tests/observe`` that uses a real pty (AD-14, AD-16).
"""

from __future__ import annotations

import os
import signal
import sys
import time
from pathlib import Path

import pytest

pexpect = pytest.importorskip("pexpect")
termios = pytest.importorskip("termios")

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX pty test")

CHILD = Path(__file__).with_name("spike_child.py")


class Child:
    """A spike child on a pty, with its event log and the master's terminal attributes."""

    def __init__(self, tmp_path: Path, mode: str = "normal") -> None:
        self.log = tmp_path / "events.log"
        env = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
        env["TERM"] = "xterm"
        self.proc = pexpect.spawn(
            sys.executable,
            [str(CHILD), "--log", str(self.log), "--mode", mode],
            env=env,
            dimensions=(24, 80),
            encoding=None,
        )
        self.orig = termios.tcgetattr(self.proc.child_fd)  # cooked mode, before "go"

    def pump(self, seconds: float) -> None:
        """Read the pty so the child never blocks on a full buffer."""
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            try:
                self.proc.read_nonblocking(65536, timeout=0.02)
            except (pexpect.TIMEOUT, pexpect.EOF):
                time.sleep(0.01)

    def events(self) -> list[str]:
        try:
            return self.log.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            return []

    def wait_for(self, predicate, timeout: float = 5.0, what: str = "condition") -> None:
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if predicate():
                return
            self.pump(0.03)
        raise AssertionError(f"timed out waiting for {what}; events={self.events()[-8:]}")

    def wait_event(self, text: str, timeout: float = 5.0) -> None:
        self.wait_for(lambda: text in self.events(), timeout, f"event {text!r}")

    def start(self) -> None:
        self.proc.sendline("go")
        self.wait_event("ready")

    def send(self, data: bytes) -> None:
        self.proc.send(data)

    def wait_exit(self, timeout: float = 5.0) -> int:
        self.wait_for(lambda: not self.proc.isalive(), timeout, "child exit")
        # Keep the master open: the attributes are read from it after the child is gone.
        return self.proc.exitstatus if self.proc.exitstatus is not None else -(self.proc.signalstatus or 0)

    def attrs(self) -> list:
        return termios.tcgetattr(self.proc.child_fd)

    def cbreak_active(self) -> bool:
        lflag = self.attrs()[3]
        return not (lflag & termios.ICANON) and not (lflag & termios.ECHO)

    def finish(self) -> None:
        if self.proc.isalive():
            self.proc.terminate(force=True)
        self.proc.close(force=True)


@pytest.fixture
def child(tmp_path):
    made: list[Child] = []

    def factory(mode: str = "normal") -> Child:
        c = Child(tmp_path, mode)
        made.append(c)
        return c

    yield factory
    for c in made:
        c.finish()


def _keys(events: list[str]) -> list[str]:
    return [e[4:] for e in events if e.startswith("key:")]


def test_lone_escape_and_arrow_sequences_are_told_apart(child):
    c = child()
    c.start()
    c.send(b"\x1b")
    c.wait_event("key:escape")
    c.send(b"\x1b[A")
    c.wait_event("key:up")
    c.send(b"\x1b[B")
    c.wait_event("key:down")
    c.send(b"\x1bOA")
    c.wait_for(lambda: _keys(c.events()).count("up") == 2, what="application-mode up")
    c.send(b"q")
    assert c.wait_exit() == 0
    assert _keys(c.events()) == ["escape", "up", "down", "up", "text:q"]


def test_burst_of_keys_is_received_in_order_while_repainting(child):
    c = child()
    c.start()
    letters = "0123456789abcdefghij"  # no "q": that key quits the child
    for ch in letters[:10]:  # spaced out: a repaint happens between most of them
        c.send(ch.encode())
        c.pump(0.04)
    c.send(letters[10:].encode())  # the rest in one write
    c.wait_for(lambda: len(_keys(c.events())) >= 20, what="all 20 keys")
    events = c.events()
    assert [k for k in _keys(events) if k.startswith("text:")] == [f"text:{x}" for x in letters]
    first = events.index("key:text:0")
    last = events.index("key:text:j")
    assert sum(1 for e in events[first:last] if e.startswith("repaint")) >= 5
    c.send(b"q")
    assert c.wait_exit() == 0


@pytest.mark.parametrize("how", ["q", "sigint", "sigterm", "sighup", "exception"])
def test_terminal_attributes_restored(child, how):
    c = child("raise" if how == "exception" else "normal")
    c.start()
    assert c.cbreak_active(), "cbreak mode should be on while the loop runs"
    expected_status = {"q": 0, "sigint": 130, "sigterm": 143, "sighup": 129, "exception": 1}[how]
    if how == "q":
        c.send(b"q")
    elif how != "exception":
        os.kill(c.proc.pid, {"sigint": signal.SIGINT, "sigterm": signal.SIGTERM, "sighup": signal.SIGHUP}[how])
    assert c.wait_exit() == expected_status
    assert c.attrs() == c.orig


@pytest.mark.skipif(not os.path.exists("/proc/self/stat"), reason="needs /proc")
def test_sigtstp_restores_terminal_and_sigcont_reenters_cbreak(child):
    c = child()
    c.start()
    assert c.cbreak_active()

    def state() -> str:
        with open(f"/proc/{c.proc.pid}/stat", encoding="utf-8") as handle:
            return handle.read().rsplit(")", 1)[1].split()[0]

    os.kill(c.proc.pid, signal.SIGTSTP)
    c.wait_for(lambda: state() == "T", what="child stopped")
    assert c.attrs() == c.orig, "original attributes while the child is stopped"

    os.kill(c.proc.pid, signal.SIGCONT)
    c.wait_event("redraw")
    c.wait_for(
        lambda: any(e.startswith("repaint") for e in c.events()[c.events().index("redraw") :]),
        what="repaint after SIGCONT",
    )
    assert c.cbreak_active(), "cbreak mode active again after SIGCONT"
    c.send(b"q")
    assert c.wait_exit() == 0
    assert c.attrs() == c.orig


def test_resize_repaints_with_the_new_size_within_one_second(child):
    c = child()
    c.start()
    c.wait_for(lambda: any("size=80x24" in e for e in c.events()), what="first repaint")
    started = time.monotonic()
    c.proc.setwinsize(30, 100)
    c.wait_for(lambda: any("size=100x30" in e for e in c.events()), timeout=1.0, what="resized repaint")
    assert time.monotonic() - started < 1.0
    c.send(b"q")
    assert c.wait_exit() == 0


def test_non_tty_descriptor_is_unavailable_without_raising():
    from superclaude.cli.observe.keys import KeySource

    read_fd, write_fd = os.pipe()
    try:
        with KeySource(read_fd) as source:
            assert source.available is False
            assert source.read(0.01) is None
    finally:
        os.close(read_fd)
        os.close(write_fd)
    with open(os.devnull, encoding="utf-8") as devnull, KeySource(devnull.fileno()) as source:
        assert source.available is False


def test_decoder_handles_enter_backspace_ctrl_c_text_and_unknown_sequences():
    from superclaude.cli.observe.keys import KeySource
    from superclaude.cli.observe.view import Key

    source = KeySource(0)
    source._buf = b"\r\x7f\x03a\xc3\xa9\x1b[5~\x01"
    taken = []
    while source._buf:
        key = source._take()
        if key is not None:
            taken.append(key)
    assert taken == [Key("enter"), Key("backspace"), Key("ctrl_c"), Key("text", "a"), Key("text", "é")]


def test_key_validates_its_name_and_char():
    from superclaude.cli.observe.view import Key

    with pytest.raises(ValueError):
        Key("nope")
    with pytest.raises(ValueError):
        Key("text")
    with pytest.raises(ValueError):
        Key("up", "x")
