"""NFR-REL1 signal handling and cooperative cancellation primitives.

This module implements the cancellation half of NFR-REL1 (T03.07 / D-0050):

* :class:`CancellationToken` — thread-safe cooperative cancellation flag
  shared between the signal handlers, the orchestrator (T03.15), and the
  per-eval ``EvalRunner.run`` (T03.05). Setting the token causes
  in-flight runners to stop honouring new work; the orchestrator then
  produces ``INTERRUPTED`` :class:`EvalOutcome` rows for every eval that
  had started but not finished.
* :class:`SignalHandlerInstaller` — context manager that binds
  ``SIGINT``/``SIGTERM`` to a callback that sets the cancellation token
  (and optionally invokes an on-signal callback for partial-summary
  bookkeeping). Restores the previous handlers on exit so the harness
  never leaves the process with a permanently re-bound signal handler.
* :data:`EXIT_INTERRUPTED` — process exit code 3 used when SIGINT/SIGTERM
  cancels a run, per design-spec §4 / NFR-REL1.

The signal handler does *not* itself terminate any subprocess. The
per-eval timeout path inside :class:`EvalRunner` is responsible for
killing the underlying :class:`PtyDriver` subprocess and reaping its
zombie; the signal handler only flips the cooperative flag so the
orchestrator can stop scheduling new evals and the in-flight ones can be
classified as ``INTERRUPTED`` once they exit (whether cleanly or via the
subprocess kill).
"""

from __future__ import annotations

import signal
import threading
from types import FrameType
from typing import Callable, Iterable, Optional

__all__ = [
    "EXIT_INTERRUPTED",
    "DEFAULT_INTERRUPT_SIGNALS",
    "CancellationToken",
    "SignalHandlerInstaller",
]


# Per design-spec §4 (Exit codes table) and NFR-REL1: SIGINT / SIGTERM
# during a run terminates with exit code 3. The constant lives here so
# the orchestrator (T03.15) and the CLI dispatcher (Phase 4) import a
# single source of truth.
EXIT_INTERRUPTED: int = 3


# ``SIGINT`` and ``SIGTERM`` are both wired to the same cancellation
# action per design-spec §12 "Signal handling". ``SIGINT`` is the Ctrl-C
# path; ``SIGTERM`` is the supervisor / container path.
DEFAULT_INTERRUPT_SIGNALS: tuple[int, ...] = (signal.SIGINT, signal.SIGTERM)


class CancellationToken:
    """Thread-safe cooperative cancellation flag.

    Wraps :class:`threading.Event` so producers can ``cancel()`` the
    token from the signal handler (or from a unit test) and consumers
    can poll ``is_cancelled()`` or block on ``wait(timeout)``. The flag
    is one-shot — once cancelled the token stays cancelled for the rest
    of its lifetime; the harness allocates a fresh token per run rather
    than resetting an in-use one. The optional ``signum_holder``
    attribute records the signal number that triggered cancellation so
    downstream consumers can include it in the partial summary.
    """

    __slots__ = ("_event", "_signum", "_signum_lock")

    def __init__(self) -> None:
        self._event = threading.Event()
        self._signum: Optional[int] = None
        self._signum_lock = threading.Lock()

    def cancel(self, *, signum: Optional[int] = None) -> bool:
        """Flip the token to the cancelled state.

        Parameters
        ----------
        signum:
            Optional signal number that caused the cancellation. Stored
            on the token so the orchestrator / reporter can record
            ``"interrupted_by"`` in the partial summary. Only the first
            ``cancel()`` call captures the signum; subsequent calls
            return ``False`` without overwriting.

        Returns
        -------
        bool
            ``True`` if this call was the one that flipped the flag,
            ``False`` if the token was already cancelled. Lets the
            orchestrator distinguish "I cancelled" from "I observed
            an already-cancelled token" without racing against a
            second signal.
        """
        first = not self._event.is_set()
        if first:
            with self._signum_lock:
                if not self._event.is_set():
                    if signum is not None:
                        self._signum = int(signum)
                    self._event.set()
                else:
                    first = False
        return first

    def is_cancelled(self) -> bool:
        """Return ``True`` once the token has been cancelled."""
        return self._event.is_set()

    def wait(self, timeout: Optional[float] = None) -> bool:
        """Block until cancelled or ``timeout`` elapses.

        Returns ``True`` if the token is cancelled when the call
        returns, ``False`` on timeout. Matches the
        :meth:`threading.Event.wait` contract so callers familiar with
        ``Event`` semantics need no adapter.
        """
        return self._event.wait(timeout)

    @property
    def signum(self) -> Optional[int]:
        """The signal number that caused cancellation, if any."""
        with self._signum_lock:
            return self._signum


# Signal-handler callback signature: ``(signum, frame, token)`` — matches
# the stdlib :class:`signal.signal` callback plus the token so callers
# can implement extra bookkeeping (partial-summary writing, telemetry)
# without keeping a global token reference.
OnSignalCallback = Callable[[int, Optional[FrameType], "CancellationToken"], None]


class SignalHandlerInstaller:
    """Context manager binding ``SIGINT``/``SIGTERM`` to a cancellation token.

    On ``__enter__`` the installer registers a handler for each signal
    in ``signals`` that:

    1. Calls ``token.cancel(signum=...)`` so cooperative consumers wake
       up immediately.
    2. Invokes the optional ``on_signal`` callback if provided. Failures
       inside the callback are swallowed — signal handlers must always
       return cleanly because the runtime may re-enter Python at a
       restricted point. Use the callback for *bookkeeping only*
       (logging, writing a partial-summary stub); the heavy work of
       writing the final partial summary belongs in the orchestrator
       once the main thread returns from its blocking join.

    On ``__exit__`` the previous handlers (captured on entry) are
    restored. Installing twice nests cleanly: the inner installer
    captures the outer installer's handler and restores it on exit.

    Limitations
    -----------

    Python's :func:`signal.signal` may only be called from the main
    thread of the main interpreter. Constructing this installer outside
    the main thread raises :class:`ValueError`. Tests that exercise the
    handler path must run on the main thread or substitute a stub.
    """

    def __init__(
        self,
        token: CancellationToken,
        *,
        signals: Iterable[int] = DEFAULT_INTERRUPT_SIGNALS,
        on_signal: Optional[OnSignalCallback] = None,
    ) -> None:
        self._token = token
        self._signals: tuple[int, ...] = tuple(int(s) for s in signals)
        if not self._signals:
            raise ValueError("at least one signal number is required")
        self._on_signal = on_signal
        self._previous: dict[int, object] = {}
        self._installed = False

    # ------------------------------------------------------------------
    # Context-manager surface
    # ------------------------------------------------------------------

    def __enter__(self) -> "SignalHandlerInstaller":
        self.install()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.restore()

    # ------------------------------------------------------------------
    # Explicit install / restore (for callers that cannot use ``with``)
    # ------------------------------------------------------------------

    def install(self) -> None:
        """Bind the handler for every configured signal.

        Idempotent: calling install twice is a no-op on the second call
        (the previous-handler snapshot is taken once).
        """
        if self._installed:
            return
        if threading.current_thread() is not threading.main_thread():
            raise ValueError(
                "SignalHandlerInstaller must be installed from the main thread"
            )
        for signum in self._signals:
            prev = signal.signal(signum, self._make_handler())
            self._previous[signum] = prev
        self._installed = True

    def restore(self) -> None:
        """Restore the previous handler for every configured signal.

        Idempotent: safe to call without a prior ``install()``. If
        :func:`signal.signal` fails (e.g. the previous handler captured
        a C-level extension that cannot be re-registered from Python)
        the per-signal failure is swallowed so the harness shutdown
        path stays clean.
        """
        if not self._installed:
            return
        for signum in self._signals:
            prev = self._previous.get(signum, signal.SIG_DFL)
            try:
                signal.signal(signum, prev)  # type: ignore[arg-type]
            except (ValueError, OSError):  # pragma: no cover - defensive
                # Restoration is best-effort; failure here cannot block
                # shutdown.
                pass
        self._previous.clear()
        self._installed = False

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _make_handler(self) -> Callable[[int, Optional[FrameType]], None]:
        token = self._token
        on_signal = self._on_signal

        def _handler(signum: int, frame: Optional[FrameType]) -> None:
            token.cancel(signum=signum)
            if on_signal is None:
                return
            try:
                on_signal(signum, frame, token)
            except BaseException:  # noqa: BLE001 — signal handlers must not raise
                # Bookkeeping callbacks are best-effort; swallow any
                # failure so the runtime never re-raises from inside the
                # signal handler context.
                return

        return _handler
