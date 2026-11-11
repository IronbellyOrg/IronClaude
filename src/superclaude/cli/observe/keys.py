"""POSIX key reader: cbreak mode plus a small decoder (POSIX only, imported lazily).

``KeySource`` puts the terminal in cbreak mode (ISIG kept, so Ctrl-C still raises
SIGINT) and always restores the saved attributes: in ``__exit__`` and from the
SIGINT, SIGTERM, SIGHUP, SIGTSTP and SIGCONT handlers.
"""

from __future__ import annotations

import os
import select
import signal
import sys
import termios
import threading
import time
import tty
from types import TracebackType

from superclaude.cli.observe.view import Key

MAX_TIMEOUT = 0.25  # longest single read() wait, seconds
ESC_WAIT = 0.05  # how long a lone ESC waits for the rest of an arrow sequence

_NEED_MORE = object()
_ESC = 0x1B
_HANDLED = (
    signal.SIGINT,
    signal.SIGTERM,
    signal.SIGHUP,
    signal.SIGTSTP,
    signal.SIGCONT,
)


class KeySource:
    """Context manager that reads keys from a terminal descriptor.

    A descriptor that is not a terminal makes the source unavailable
    (``available`` is False, ``read`` returns None); nothing raises.
    """

    def __init__(self, fd: int | None = None) -> None:
        self._fd = sys.stdin.fileno() if fd is None else fd
        self.available = False
        self._saved: list | None = None
        self._previous: dict[int, object] = {}
        self._buf = b""
        self._redraw = False

    # -- terminal state -------------------------------------------------
    def __enter__(self) -> KeySource:
        try:
            is_tty = os.isatty(self._fd)
        except (OSError, ValueError):
            is_tty = False
        if not is_tty:
            return self
        try:
            self._saved = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd, termios.TCSANOW)
        except (termios.error, OSError):
            self._saved = None
            return self
        self.available = True
        self._install_handlers()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._restore()
        self._remove_handlers()
        self.available = False

    def _restore(self) -> None:
        if self._saved is None:
            return
        try:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
        except (termios.error, OSError):
            pass

    def _enter_cbreak(self) -> None:
        try:
            tty.setcbreak(self._fd, termios.TCSANOW)
        except (termios.error, OSError):
            pass

    # -- signals ---------------------------------------------------------
    def _install_handlers(self) -> None:
        if threading.current_thread() is not threading.main_thread():
            return  # signal.signal only works in the main thread
        handlers = {
            signal.SIGINT: self._on_int,
            signal.SIGTERM: self._on_term,
            signal.SIGHUP: self._on_hup,
            signal.SIGTSTP: self._on_tstp,
            signal.SIGCONT: self._on_cont,
        }
        for sig, handler in handlers.items():
            self._previous[sig] = signal.signal(sig, handler)

    def _remove_handlers(self) -> None:
        for sig, previous in self._previous.items():
            try:
                signal.signal(sig, previous)  # type: ignore[arg-type]
            except (ValueError, OSError):
                pass
        self._previous.clear()

    def _on_int(self, signum: int, frame: object) -> None:
        self._restore()
        raise KeyboardInterrupt

    def _on_term(self, signum: int, frame: object) -> None:
        self._restore()
        raise SystemExit(128 + signal.SIGTERM)

    def _on_hup(self, signum: int, frame: object) -> None:
        self._restore()
        raise SystemExit(128 + signal.SIGHUP)

    def _on_tstp(self, signum: int, frame: object) -> None:
        # Give the terminal back, then stop. SIGSTOP (not SIGTSTP with the
        # default action) because a process group the shell does not own is
        # "orphaned" and ignores the default SIGTSTP action.
        self._restore()
        os.kill(os.getpid(), signal.SIGSTOP)

    def _on_cont(self, signum: int, frame: object) -> None:
        self._enter_cbreak()
        self._redraw = True

    def consume_redraw(self) -> bool:
        """True once after a SIGCONT: the loop should repaint."""
        redraw, self._redraw = self._redraw, False
        return redraw

    # -- reading ---------------------------------------------------------
    def read(self, timeout: float = MAX_TIMEOUT) -> Key | None:
        """Return the next key, or None when nothing arrived within ``timeout``."""
        timeout = min(max(timeout, 0.0), MAX_TIMEOUT)
        if not self.available:
            time.sleep(timeout)
            return None
        deadline = time.monotonic() + timeout
        while True:
            key = self._take()
            if key is not _NEED_MORE:
                if key is not None:
                    return key  # type: ignore[return-value]
                continue  # a swallowed sequence; look at the next bytes
            wait = ESC_WAIT if self._buf else max(deadline - time.monotonic(), 0.0)
            try:
                ready, _, _ = select.select([self._fd], [], [], wait)
            except (OSError, ValueError, InterruptedError):
                ready = []
            if not ready:
                if self._buf == b"\x1b":
                    self._buf = b""
                    return Key("escape")
                self._buf = b""  # an incomplete sequence is dropped
                return None
            try:
                data = os.read(self._fd, 4096)
            except OSError:
                data = b""
            if not data:
                return None
            self._buf += data

    def _take(self) -> object:
        """Decode one key from the buffer: a Key, None (swallowed) or _NEED_MORE."""
        buf = self._buf
        if not buf:
            return _NEED_MORE
        b0 = buf[0]
        if b0 == _ESC:
            return self._take_escape()
        self._buf = buf[1:]
        if b0 in (0x0D, 0x0A):
            return Key("enter")
        if b0 in (0x7F, 0x08):
            return Key("backspace")
        if b0 == 0x03:
            return Key("ctrl_c")
        if b0 < 0x20:
            return None
        if b0 < 0x80:
            return Key("text", chr(b0))
        return self._take_utf8(b0)

    def _take_utf8(self, lead: int) -> object:
        need = 2 if lead >> 5 == 0b110 else 3 if lead >> 4 == 0b1110 else 4 if lead >> 3 == 0b11110 else 1
        raw = bytes([lead]) + self._buf[: need - 1]
        if len(raw) < need:
            self._buf = bytes([lead]) + self._buf
            return _NEED_MORE
        self._buf = self._buf[need - 1 :]
        char = raw.decode("utf-8", errors="replace")
        if char.isprintable():
            return Key("text", char)
        return None

    def _take_escape(self) -> object:
        buf = self._buf
        if len(buf) == 1:
            return _NEED_MORE
        second = buf[1]
        if second == ord("["):
            for i in range(2, len(buf)):
                if 0x40 <= buf[i] <= 0x7E:  # final byte of a CSI sequence
                    final = buf[i]
                    self._buf = buf[i + 1 :]
                    return {ord("A"): Key("up"), ord("B"): Key("down")}.get(final)
            return _NEED_MORE
        if second == ord("O"):
            if len(buf) < 3:
                return _NEED_MORE
            self._buf = buf[3:]
            return {ord("A"): Key("up"), ord("B"): Key("down")}.get(buf[2])
        self._buf = buf[1:]  # ESC followed by something else: a plain Escape
        return Key("escape")
