e1bafa8877256de791a9fa834db838708d587ee9
Review one task for spec compliance.

Task brief: 
## Task 1: Run the Rich Live plus stdlib key-reader spike and build `keys.py`

Create `src/superclaude/cli/observe/__init__.py` (package marker), `src/superclaude/cli/observe/view.py` containing only the frozen `Key` dataclass for now (names `up`, `down`, `enter`, `escape`, `backspace`, `ctrl_c`, `text` with a `char` for `text`; later tasks extend this file), `src/superclaude/cli/observe/keys.py`, `tests/observe/__init__.py`, `tests/observe/spike_child.py` and `tests/observe/test_keys_spike.py`, and record the outcome in `./artifacts/t1-spike.md`. Follow SPECDIR `ARCHITECTURE-SPINE.md` AD-14 and `stack.md`. `keys.py` defines `KeySource`, a context manager that enters cbreak mode with `tty.setcbreak(fd, termios.TCSANOW)` and restores the saved attributes in `finally` and from SIGINT, SIGTERM, SIGHUP, SIGTSTP and SIGCONT handlers (SIGINT restores, then raises `KeyboardInterrupt`; SIGHUP restores and exits; SIGTSTP restores the terminal and then stops the process; SIGCONT re-enters cbreak mode and asks the loop to redraw, per SPECDIR `stack.md`; previous handlers are put back), and `read(timeout)` (timeout at most 0.25 s) that decodes arrows, Enter, a lone Escape (told apart from an arrow sequence by a short follow-up read), Backspace, Ctrl-C and printable characters into `Key`. It imports `view.py` only for `Key`, and `termios` and `tty` only inside the module. A non-tty descriptor makes `KeySource` report itself unavailable instead of raising. `spike_child.py` runs a `rich.live.Live(screen=True)` loop that repaints every 100 ms while reading keys through `KeySource`, and prints a one-line event log. The test drives it with `pexpect` on a real pseudo-terminal.

Acceptance criteria:
- [T1.AC1] `uv run pytest tests/observe/test_keys_spike.py -v` passes. It sends a lone Escape and an Up-arrow sequence and asserts the child decoded `escape` and `up` respectively.
- [T1.AC2] A burst of 20 keystrokes sent while the child is repainting is all received in order (none lost), and at least 5 repaints happen during the burst.
- [T1.AC3] The terminal attributes read from the pty master with `termios.tcgetattr` after the child exits are identical to those before it started, in five cases: normal exit on `q`, SIGINT, SIGTERM, SIGHUP and an exception raised inside the loop; and a SIGTSTP followed by SIGCONT test shows the original attributes while the child is stopped and cbreak mode active again, with a repaint, after SIGCONT.
- [T1.AC4] After the pty window is resized (`setwinsize` plus SIGWINCH), the child repaints with the new size within 1 s.
- [T1.AC5] A non-tty descriptor test shows `KeySource` unavailable without raising.
- [T1.AC6] `./artifacts/t1-spike.md` states pass or fail per criterion above, the Python and Rich versions, that "no visible flicker" was not automated and is UNVERIFIED, and the decision (continue with Rich, or blocked pending the owner). The artifact says fail whenever any automated criterion fails.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: e1bafa8877256de791a9fa834db838708d587ee9
Diff against the start snapshot: 
diff --git a/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/artifacts/t1-spike.md b/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/artifacts/t1-spike.md
new file mode 100644
index 000000000..26778f317
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/artifacts/t1-spike.md
@@ -0,0 +1,25 @@
+# T1 spike: Rich Live plus stdlib key reader
+
+Run: `uv run pytest tests/observe/test_keys_spike.py -v` gave `12 passed in 8.67s`; two more runs gave `12 passed in 8.68s` and `12 passed in 8.97s`. Python 3.11.15, Rich 15.0.0, pexpect 4.9.0, pytest 9.2.0, Linux 6.8.0 (pty from pexpect). Pass or fail below is the automated result only.
+
+| Criterion | Result | Test |
+|---|---|---|
+| Lone Escape decoded as `escape`, Up-arrow sequence as `up` (also Down, and the application-mode `ESC O A` form) | pass | `test_lone_escape_and_arrow_sequences_are_told_apart` |
+| 20 keystrokes sent during repainting arrive in order, none lost; at least 5 repaints during the burst | pass | `test_burst_of_keys_is_received_in_order_while_repainting` |
+| Terminal attributes identical before start and after exit: normal exit on `q` | pass | `test_terminal_attributes_restored[q]` |
+| ... SIGINT | pass | `test_terminal_attributes_restored[sigint]` |
+| ... SIGTERM | pass | `test_terminal_attributes_restored[sigterm]` |
+| ... SIGHUP | pass | `test_terminal_attributes_restored[sighup]` |
+| ... exception raised inside the loop | pass | `test_terminal_attributes_restored[exception]` |
+| SIGTSTP then SIGCONT: original attributes while the child is stopped, cbreak mode active again with a repaint after SIGCONT | pass | `test_sigtstp_restores_terminal_and_sigcont_reenters_cbreak` |
+| Pty resize (`setwinsize` plus SIGWINCH): repaint with the new size within 1 s | pass | `test_resize_repaints_with_the_new_size_within_one_second` |
+| Non-tty descriptor: `KeySource` unavailable, no exception | pass | `test_non_tty_descriptor_is_unavailable_without_raising` |
+
+Notes:
+
+- SIGTSTP stops the child with SIGSTOP after restoring the terminal. A process group started by pexpect is orphaned, and an orphaned group ignores the default SIGTSTP action, so SIGSTOP is what makes the stop observable. A real shell sees the same stopped state.
+- Ctrl-C reaches the child as SIGINT (ISIG kept), so the decoder's `ctrl_c` key is covered by a decoder unit test, not by the pty test.
+- "No visible flicker" was not automated and is UNVERIFIED. It needs a human watching a real terminal.
+- The Textual fallback (AD-14) was not built or tried.
+
+Decision: every automated criterion passed, so continue with Rich `Live(screen=True)` and the stdlib `KeySource`. Textual is not added.
diff --git a/src/superclaude/cli/observe/__init__.py b/src/superclaude/cli/observe/__init__.py
new file mode 100644
index 000000000..b46886716
--- /dev/null
+++ b/src/superclaude/cli/observe/__init__.py
@@ -0,0 +1 @@
+"""Read-only terminal observer for Orca workers (``superclaude observe``)."""
diff --git a/src/superclaude/cli/observe/keys.py b/src/superclaude/cli/observe/keys.py
new file mode 100644
index 000000000..9da5c01e5
--- /dev/null
+++ b/src/superclaude/cli/observe/keys.py
@@ -0,0 +1,227 @@
+"""POSIX key reader: cbreak mode plus a small decoder (POSIX only, imported lazily).
+
+``KeySource`` puts the terminal in cbreak mode (ISIG kept, so Ctrl-C still raises
+SIGINT) and always restores the saved attributes: in ``__exit__`` and from the
+SIGINT, SIGTERM, SIGHUP, SIGTSTP and SIGCONT handlers.
+"""
+
+from __future__ import annotations
+
+import os
+import select
+import signal
+import sys
+import termios
+import threading
+import time
+import tty
+from types import TracebackType
+
+from superclaude.cli.observe.view import Key
+
+MAX_TIMEOUT = 0.25  # longest single read() wait, seconds
+ESC_WAIT = 0.05  # how long a lone ESC waits for the rest of an arrow sequence
+
+_NEED_MORE = object()
+_ESC = 0x1B
+_HANDLED = (
+    signal.SIGINT,
+    signal.SIGTERM,
+    signal.SIGHUP,
+    signal.SIGTSTP,
+    signal.SIGCONT,
+)
+
+
+class KeySource:
+    """Context manager that reads keys from a terminal descriptor.
+
+    A descriptor that is not a terminal makes the source unavailable
+    (``available`` is False, ``read`` returns None); nothing raises.
+    """
+
+    def __init__(self, fd: int | None = None) -> None:
+        self._fd = sys.stdin.fileno() if fd is None else fd
+        self.available = False
+        self._saved: list | None = None
+        self._previous: dict[int, object] = {}
+        self._buf = b""
+        self._redraw = False
+
+    # -- terminal state -------------------------------------------------
+    def __enter__(self) -> KeySource:
+        try:
+            is_tty = os.isatty(self._fd)
+        except (OSError, ValueError):
+            is_tty = False
+        if not is_tty:
+            return self
+        try:
+            self._saved = termios.tcgetattr(self._fd)
+            tty.setcbreak(self._fd, termios.TCSANOW)
+        except (termios.error, OSError):
+            self._saved = None
+            return self
+        self.available = True
+        self._install_handlers()
+        return self
+
+    def __exit__(
+        self,
+        exc_type: type[BaseException] | None,
+        exc: BaseException | None,
+        tb: TracebackType | None,
+    ) -> None:
+        self._restore()
+        self._remove_handlers()
+        self.available = False
+
+    def _restore(self) -> None:
+        if self._saved is None:
+            return
+        try:
+            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
+        except (termios.error, OSError):
+            pass
+
+    def _enter_cbreak(self) -> None:
+        try:
+            tty.setcbreak(self._fd, termios.TCSANOW)
+        except (termios.error, OSError):
+            pass
+
+    # -- signals ---------------------------------------------------------
+    def _install_handlers(self) -> None:
+        if threading.current_thread() is not threading.main_thread():
+            return  # signal.signal only works in the main thread
+        handlers = {
+            signal.SIGINT: self._on_int,
+            signal.SIGTERM: self._on_term,
+            signal.SIGHUP: self._on_hup,
+            signal.SIGTSTP: self._on_tstp,
+            signal.SIGCONT: self._on_cont,
+        }
+        for sig, handler in handlers.items():
+            self._previous[sig] = signal.signal(sig, handler)
+
+    def _remove_handlers(self) -> None:
+        for sig, previous in self._previous.items():
+            try:
+                signal.signal(sig, previous)  # type: ignore[arg-type]
+            except (ValueError, OSError):
+                pass
+        self._previous.clear()
+
+    def _on_int(self, signum: int, frame: object) -> None:
+        self._restore()
+        raise KeyboardInterrupt
+
+    def _on_term(self, signum: int, frame: object) -> None:
+        self._restore()
+        raise SystemExit(128 + signal.SIGTERM)
+
+    def _on_hup(self, signum: int, frame: object) -> None:
+        self._restore()
+        raise SystemExit(128 + signal.SIGHUP)
+
+    def _on_tstp(self, signum: int, frame: object) -> None:
+        # Give the terminal back, then stop. SIGSTOP (not SIGTSTP with the
+        # default action) because a process group the shell does not own is
+        # "orphaned" and ignores the default SIGTSTP action.
+        self._restore()
+        os.kill(os.getpid(), signal.SIGSTOP)
+
+    def _on_cont(self, signum: int, frame: object) -> None:
+        self._enter_cbreak()
+        self._redraw = True
+
+    def consume_redraw(self) -> bool:
+        """True once after a SIGCONT: the loop should repaint."""
+        redraw, self._redraw = self._redraw, False
+        return redraw
+
+    # -- reading ---------------------------------------------------------
+    def read(self, timeout: float = MAX_TIMEOUT) -> Key | None:
+        """Return the next key, or None when nothing arrived within ``timeout``."""
+        timeout = min(max(timeout, 0.0), MAX_TIMEOUT)
+        if not self.available:
+            time.sleep(timeout)
+            return None
+        deadline = time.monotonic() + timeout
+        while True:
+            key = self._take()
+            if key is not _NEED_MORE:
+                if key is not None:
+                    return key  # type: ignore[return-value]
+                continue  # a swallowed sequence; look at the next bytes
+            wait = ESC_WAIT if self._buf else max(deadline - time.monotonic(), 0.0)
+            try:
+                ready, _, _ = select.select([self._fd], [], [], wait)
+            except (OSError, ValueError, InterruptedError):
+                ready = []
+            if not ready:
+                if self._buf == b"\x1b":
+                    self._buf = b""
+                    return Key("escape")
+                self._buf = b""  # an incomplete sequence is dropped
+                return None
+            try:
+                data = os.read(self._fd, 4096)
+            except OSError:
+                data = b""
+            if not data:
+                return None
+            self._buf += data
+
+    def _take(self) -> object:
+        """Decode one key from the buffer: a Key, None (swallowed) or _NEED_MORE."""
+        buf = self._buf
+        if not buf:
+            return _NEED_MORE
+        b0 = buf[0]
+        if b0 == _ESC:
+            return self._take_escape()
+        self._buf = buf[1:]
+        if b0 in (0x0D, 0x0A):
+            return Key("enter")
+        if b0 in (0x7F, 0x08):
+            return Key("backspace")
+        if b0 == 0x03:
+            return Key("ctrl_c")
+        if b0 < 0x20:
+            return None
+        if b0 < 0x80:
+            return Key("text", chr(b0))
+        return self._take_utf8(b0)
+
+    def _take_utf8(self, lead: int) -> object:
+        need = 2 if lead >> 5 == 0b110 else 3 if lead >> 4 == 0b1110 else 4 if lead >> 3 == 0b11110 else 1
+        raw = bytes([lead]) + self._buf[: need - 1]
+        if len(raw) < need:
+            self._buf = bytes([lead]) + self._buf
+            return _NEED_MORE
+        self._buf = self._buf[need - 1 :]
+        char = raw.decode("utf-8", errors="replace")
+        if char.isprintable():
+            return Key("text", char)
+        return None
+
+    def _take_escape(self) -> object:
+        buf = self._buf
+        if len(buf) == 1:
+            return _NEED_MORE
+        second = buf[1]
+        if second == ord("["):
+            for i in range(2, len(buf)):
+                if 0x40 <= buf[i] <= 0x7E:  # final byte of a CSI sequence
+                    final = buf[i]
+                    self._buf = buf[i + 1 :]
+                    return {ord("A"): Key("up"), ord("B"): Key("down")}.get(final)
+            return _NEED_MORE
+        if second == ord("O"):
+            if len(buf) < 3:
+                return _NEED_MORE
+            self._buf = buf[3:]
+            return {ord("A"): Key("up"), ord("B"): Key("down")}.get(buf[2])
+        self._buf = buf[1:]  # ESC followed by something else: a plain Escape
+        return Key("escape")
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
new file mode 100644
index 000000000..11b3e4e29
--- /dev/null
+++ b/src/superclaude/cli/observe/view.py
@@ -0,0 +1,21 @@
+"""View model for the observer. Later tasks add ``Session``, ``View`` and the pure builders."""
+
+from __future__ import annotations
+
+from dataclasses import dataclass
+
+KEY_NAMES = ("up", "down", "enter", "escape", "backspace", "ctrl_c", "text")
+
+
+@dataclass(frozen=True)
+class Key:
+    """One decoded key press. ``char`` is set only for ``text``."""
+
+    name: str
+    char: str = ""
+
+    def __post_init__(self) -> None:
+        if self.name not in KEY_NAMES:
+            raise ValueError(f"unknown key name: {self.name!r}")
+        if (self.name == "text") != bool(self.char):
+            raise ValueError("char is required for text keys and forbidden for others")
diff --git a/tests/observe/__init__.py b/tests/observe/__init__.py
new file mode 100644
index 000000000..e69de29bb
diff --git a/tests/observe/spike_child.py b/tests/observe/spike_child.py
new file mode 100644
index 000000000..45fb5f26d
--- /dev/null
+++ b/tests/observe/spike_child.py
@@ -0,0 +1,101 @@
+"""Key-reader spike child: ``rich.live.Live(screen=True)`` repainting every 100 ms
+while reading keys through ``KeySource``. Run only by ``test_keys_spike.py`` on a pty.
+
+It waits for one line on stdin (still in cooked mode) so the test can read the
+original terminal attributes first, then logs one event per line to the screen
+and to the file given with ``--log``.
+"""
+
+from __future__ import annotations
+
+import argparse
+import sys
+import time
+
+from rich.console import Console, ConsoleOptions, RenderResult
+from rich.live import Live
+from rich.text import Text
+
+from superclaude.cli.observe.keys import KeySource
+
+REPAINT_SECONDS = 0.1
+
+
+class _Screen:
+    """Rendered on every repaint; reports the size Rich sees right now."""
+
+    def __init__(self, log: "_Log") -> None:
+        self.log = log
+        self.repaints = 0
+
+    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
+        self.repaints += 1
+        size = f"{options.size.width}x{options.size.height}"
+        self.log.write(f"repaint n={self.repaints} size={size}")
+        yield Text(f"SPIKE repaint={self.repaints} size={size}")
+        for line in self.log.tail(5):
+            yield Text(f"EVT:{line}")
+
+
+class _Log:
+    def __init__(self, path: str | None) -> None:
+        self.path = path
+        self.lines: list[str] = []
+
+    def write(self, line: str) -> None:
+        self.lines.append(line)
+        if self.path:
+            with open(self.path, "a", encoding="utf-8") as handle:
+                handle.write(line + "\n")
+
+    def tail(self, count: int) -> list[str]:
+        events = [x for x in self.lines if not x.startswith("repaint")]
+        return events[-count:]
+
+
+def run(mode: str, log: _Log) -> int:
+    with KeySource() as keys:
+        if not keys.available:
+            log.write("unavailable")
+            return 2
+        screen = _Screen(log)
+        with Live(screen, console=Console(), screen=True, auto_refresh=False) as live:
+            log.write("ready")
+            last = 0.0
+            tick = 0
+            while True:
+                key = keys.read(0.05)
+                if key is not None:
+                    detail = key.name if key.name != "text" else f"text:{key.char}"
+                    log.write(f"key:{detail}")
+                    if key.name == "text" and key.char == "q":
+                        log.write("quit")
+                        return 0
+                if keys.consume_redraw():
+                    log.write("redraw")
+                    last = 0.0
+                now = time.monotonic()
+                if now - last >= REPAINT_SECONDS:
+                    last = now
+                    tick += 1
+                    live.update(screen, refresh=True)
+                    if mode == "raise" and tick == 5:
+                        raise RuntimeError("spike: exception inside the loop")
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser()
+    parser.add_argument("--log", default=None)
+    parser.add_argument("--mode", default="normal", choices=["normal", "raise"])
+    args = parser.parse_args()
+    log = _Log(args.log)
+    sys.stdin.readline()  # cooked mode: the test reads the original attributes, then sends "go"
+    try:
+        return run(args.mode, log)
+    except KeyboardInterrupt:
+        log.write("interrupted")
+        return 130
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/observe/test_keys_spike.py b/tests/observe/test_keys_spike.py
new file mode 100644
index 000000000..6e245761e
--- /dev/null
+++ b/tests/observe/test_keys_spike.py
@@ -0,0 +1,232 @@
+"""R0 key-reader spike: Rich Live plus the stdlib ``KeySource`` on a real pseudo-terminal.
+
+This is the only test module in ``tests/observe`` that uses a real pty (AD-14, AD-16).
+"""
+
+from __future__ import annotations
+
+import os
+import signal
+import sys
+import time
+from pathlib import Path
+
+import pytest
+
+pexpect = pytest.importorskip("pexpect")
+termios = pytest.importorskip("termios")
+
+pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX pty test")
+
+CHILD = Path(__file__).with_name("spike_child.py")
+
+
+class Child:
+    """A spike child on a pty, with its event log and the master's terminal attributes."""
+
+    def __init__(self, tmp_path: Path, mode: str = "normal") -> None:
+        self.log = tmp_path / "events.log"
+        env = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
+        env["TERM"] = "xterm"
+        self.proc = pexpect.spawn(
+            sys.executable,
+            [str(CHILD), "--log", str(self.log), "--mode", mode],
+            env=env,
+            dimensions=(24, 80),
+            encoding=None,
+        )
+        self.orig = termios.tcgetattr(self.proc.child_fd)  # cooked mode, before "go"
+
+    def pump(self, seconds: float) -> None:
+        """Read the pty so the child never blocks on a full buffer."""
+        end = time.monotonic() + seconds
+        while time.monotonic() < end:
+            try:
+                self.proc.read_nonblocking(65536, timeout=0.02)
+            except (pexpect.TIMEOUT, pexpect.EOF):
+                time.sleep(0.01)
+
+    def events(self) -> list[str]:
+        try:
+            return self.log.read_text(encoding="utf-8").splitlines()
+        except FileNotFoundError:
+            return []
+
+    def wait_for(self, predicate, timeout: float = 5.0, what: str = "condition") -> None:
+        end = time.monotonic() + timeout
+        while time.monotonic() < end:
+            if predicate():
+                return
+            self.pump(0.03)
+        raise AssertionError(f"timed out waiting for {what}; events={self.events()[-8:]}")
+
+    def wait_event(self, text: str, timeout: float = 5.0) -> None:
+        self.wait_for(lambda: text in self.events(), timeout, f"event {text!r}")
+
+    def start(self) -> None:
+        self.proc.sendline("go")
+        self.wait_event("ready")
+
+    def send(self, data: bytes) -> None:
+        self.proc.send(data)
+
+    def wait_exit(self, timeout: float = 5.0) -> int:
+        self.wait_for(lambda: not self.proc.isalive(), timeout, "child exit")
+        # Keep the master open: the attributes are read from it after the child is gone.
+        return self.proc.exitstatus if self.proc.exitstatus is not None else -(self.proc.signalstatus or 0)
+
+    def attrs(self) -> list:
+        return termios.tcgetattr(self.proc.child_fd)
+
+    def cbreak_active(self) -> bool:
+        lflag = self.attrs()[3]
+        return not (lflag & termios.ICANON) and not (lflag & termios.ECHO)
+
+    def finish(self) -> None:
+        if self.proc.isalive():
+            self.proc.terminate(force=True)
+        self.proc.close(force=True)
+
+
+@pytest.fixture
+def child(tmp_path):
+    made: list[Child] = []
+
+    def factory(mode: str = "normal") -> Child:
+        c = Child(tmp_path, mode)
+        made.append(c)
+        return c
+
+    yield factory
+    for c in made:
+        c.finish()
+
+
+def _keys(events: list[str]) -> list[str]:
+    return [e[4:] for e in events if e.startswith("key:")]
+
+
+def test_lone_escape_and_arrow_sequences_are_told_apart(child):
+    c = child()
+    c.start()
+    c.send(b"\x1b")
+    c.wait_event("key:escape")
+    c.send(b"\x1b[A")
+    c.wait_event("key:up")
+    c.send(b"\x1b[B")
+    c.wait_event("key:down")
+    c.send(b"\x1bOA")
+    c.wait_for(lambda: _keys(c.events()).count("up") == 2, what="application-mode up")
+    c.send(b"q")
+    assert c.wait_exit() == 0
+    assert _keys(c.events()) == ["escape", "up", "down", "up", "text:q"]
+
+
+def test_burst_of_keys_is_received_in_order_while_repainting(child):
+    c = child()
+    c.start()
+    letters = "0123456789abcdefghij"  # no "q": that key quits the child
+    for ch in letters[:10]:  # spaced out: a repaint happens between most of them
+        c.send(ch.encode())
+        c.pump(0.04)
+    c.send(letters[10:].encode())  # the rest in one write
+    c.wait_for(lambda: len(_keys(c.events())) >= 20, what="all 20 keys")
+    events = c.events()
+    assert [k for k in _keys(events) if k.startswith("text:")] == [f"text:{x}" for x in letters]
+    first = events.index("key:text:0")
+    last = events.index("key:text:j")
+    assert sum(1 for e in events[first:last] if e.startswith("repaint")) >= 5
+    c.send(b"q")
+    assert c.wait_exit() == 0
+
+
+@pytest.mark.parametrize("how", ["q", "sigint", "sigterm", "sighup", "exception"])
+def test_terminal_attributes_restored(child, how):
+    c = child("raise" if how == "exception" else "normal")
+    c.start()
+    assert c.cbreak_active(), "cbreak mode should be on while the loop runs"
+    expected_status = {"q": 0, "sigint": 130, "sigterm": 143, "sighup": 129, "exception": 1}[how]
+    if how == "q":
+        c.send(b"q")
+    elif how != "exception":
+        os.kill(c.proc.pid, {"sigint": signal.SIGINT, "sigterm": signal.SIGTERM, "sighup": signal.SIGHUP}[how])
+    assert c.wait_exit() == expected_status
+    assert c.attrs() == c.orig
+
+
+@pytest.mark.skipif(not os.path.exists("/proc/self/stat"), reason="needs /proc")
+def test_sigtstp_restores_terminal_and_sigcont_reenters_cbreak(child):
+    c = child()
+    c.start()
+    assert c.cbreak_active()
+
+    def state() -> str:
+        with open(f"/proc/{c.proc.pid}/stat", encoding="utf-8") as handle:
+            return handle.read().rsplit(")", 1)[1].split()[0]
+
+    os.kill(c.proc.pid, signal.SIGTSTP)
+    c.wait_for(lambda: state() == "T", what="child stopped")
+    assert c.attrs() == c.orig, "original attributes while the child is stopped"
+
+    os.kill(c.proc.pid, signal.SIGCONT)
+    c.wait_event("redraw")
+    c.wait_for(
+        lambda: any(e.startswith("repaint") for e in c.events()[c.events().index("redraw") :]),
+        what="repaint after SIGCONT",
+    )
+    assert c.cbreak_active(), "cbreak mode active again after SIGCONT"
+    c.send(b"q")
+    assert c.wait_exit() == 0
+    assert c.attrs() == c.orig
+
+
+def test_resize_repaints_with_the_new_size_within_one_second(child):
+    c = child()
+    c.start()
+    c.wait_for(lambda: any("size=80x24" in e for e in c.events()), what="first repaint")
+    started = time.monotonic()
+    c.proc.setwinsize(30, 100)
+    c.wait_for(lambda: any("size=100x30" in e for e in c.events()), timeout=1.0, what="resized repaint")
+    assert time.monotonic() - started < 1.0
+    c.send(b"q")
+    assert c.wait_exit() == 0
+
+
+def test_non_tty_descriptor_is_unavailable_without_raising():
+    from superclaude.cli.observe.keys import KeySource
+
+    read_fd, write_fd = os.pipe()
+    try:
+        with KeySource(read_fd) as source:
+            assert source.available is False
+            assert source.read(0.01) is None
+    finally:
+        os.close(read_fd)
+        os.close(write_fd)
+    with open(os.devnull, encoding="utf-8") as devnull, KeySource(devnull.fileno()) as source:
+        assert source.available is False
+
+
+def test_decoder_handles_enter_backspace_ctrl_c_text_and_unknown_sequences():
+    from superclaude.cli.observe.keys import KeySource
+    from superclaude.cli.observe.view import Key
+
+    source = KeySource(0)
+    source._buf = b"\r\x7f\x03a\xc3\xa9\x1b[5~\x01"
+    taken = []
+    while source._buf:
+        key = source._take()
+        if key is not None:
+            taken.append(key)
+    assert taken == [Key("enter"), Key("backspace"), Key("ctrl_c"), Key("text", "a"), Key("text", "é")]
+
+
+def test_key_validates_its_name_and_char():
+    from superclaude.cli.observe.view import Key
+
+    with pytest.raises(ValueError):
+        Key("nope")
+    with pytest.raises(ValueError):
+        Key("text")
+    with pytest.raises(ValueError):
+        Key("up", "x")

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
