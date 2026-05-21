"""COMP-013 ClaudeProcess reuse adapter (Task T02.19 / D-0038).

FR-G1 requires every eval to drive the real ``claude`` binary as a child
process; the cliEval harness must never short-circuit through an
in-process ``anthropic`` SDK call. This module is the single integration
point between :class:`~superclaude.cli.eval.isolation.HomeIsolation` (per-
eval HOME + ``CLAUDE_SESSION_ID`` env layer) and
:class:`~superclaude.cli.pipeline.process.ClaudeProcess` (the production
subprocess lifecycle manager with signal handling, ``--print``-mode
command building, stdout/stderr file separation, and timeout-aware
``wait`` / ``terminate``).

The adapter has three jobs:

1. **Reuse, do not duplicate.** Delegate command construction
   (``build_command``) and base env construction (``build_env``) to
   :class:`ClaudeProcess`. The adapter assembles the per-eval env by
   merging :meth:`HomeIsolation.env` *on top of* whatever extra env vars
   the caller supplied so ``HOME`` / ``CLAUDE_SESSION_ID`` always win.
2. **Pin cwd.** ``ClaudeProcess`` itself does not expose a ``cwd``
   Popen kwarg today; the adapter holds the cwd argument and ``chdir``-s
   into it around :meth:`ClaudeProcess.start` so the forked child
   inherits the desired working directory. The chdir is fenced by a
   try/finally so the parent's cwd is always restored, even on a spawn
   exception.
3. **Reinforce FR-G1.** The companion ruff lint rule (registered in
   ``pyproject.toml`` under ``[tool.ruff.lint.flake8-tidy-imports.
   banned-api]``) rejects any ``anthropic`` SDK import. ``ruff check
   src/superclaude/cli/eval/`` therefore fires on a synthetic
   ``import anthropic`` anywhere in this subtree before the adapter
   even runs. The two layers (subprocess discipline + lint rule)
   together close the FR-G1 surface.

Stdout/stderr separation
========================

:class:`ClaudeProcess` opens ``output_file`` and ``error_file`` as
*separate* real file handles and passes them as ``stdout=`` and
``stderr=`` to :func:`subprocess.Popen`. The adapter inherits this
separation verbatim — the AC requires distinct stdout / stderr
artifacts for downstream gate scoring, and routing the spawn through
``ClaudeProcess`` (rather than re-implementing the popen pattern) is
the simplest way to keep that guarantee.

PtyDriver versus ClaudeProcess
==============================

The cliEval harness has two real-claude entry points:

* :class:`~superclaude.cli.eval.pty_driver.PtyDriver` (T02.16,
  COMP-007) drives the *interactive* ``claude`` REPL through a
  pseudo-terminal. Used by the Expect-style assertion layer
  (T04.07).
* :class:`ClaudeProcessAdapter` (this module, COMP-013) drives
  the *non-interactive* ``claude --print`` mode through
  :class:`ClaudeProcess`. Used by capability gate tests and
  any eval that wants a single-shot transcript with separated
  stdout / stderr.

Both satisfy FR-G1 (real subprocess discipline). They are not
interchangeable: the PTY path merges stdout and stderr into one stream
(unavoidable in a TTY), while ``ClaudeProcess`` keeps them split. The
adapter therefore lives beside ``PtyDriver`` instead of replacing it.

Cross-links
===========

* COMP-006 :class:`HomeIsolation` (T02.11 / D-0032) — supplies the
  per-eval env via :meth:`HomeIsolation.env`.
* COMP-007 :class:`PtyDriver` (T02.16 / D-0036) — sibling real-claude
  spawner for interactive mode.
* :class:`~superclaude.cli.pipeline.process.ClaudeProcess` (lines
  24-150 of ``cli/pipeline/process.py``) — wrapped here.
* Ruff config: ``[tool.ruff.lint.flake8-tidy-imports.banned-api]`` in
  ``pyproject.toml`` — registers the ``anthropic`` ban.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from superclaude.cli.pipeline.process import ClaudeProcess

if TYPE_CHECKING:  # pragma: no cover - typing only
    from superclaude.cli.eval.isolation import HomeIsolation

__all__ = [
    "ClaudeProcessAdapter",
    "ClaudeProcessAdapterError",
]


class ClaudeProcessAdapterError(Exception):
    """Raised by :class:`ClaudeProcessAdapter` on configuration failures.

    The adapter itself never wraps :class:`ClaudeProcess` runtime
    exceptions — those propagate verbatim so the caller's existing
    ``ClaudeProcess`` error handling (timeout 124, signal handling)
    keeps working. This exception type covers only adapter-local
    misuse: a ``cwd`` argument that does not exist on disk, a
    :class:`HomeIsolation` whose ``setup`` has not run yet, etc.
    """


class ClaudeProcessAdapter:
    """Wrap :class:`ClaudeProcess` for per-eval HOME-isolated spawning.

    The adapter exists to:

    * Inject :meth:`HomeIsolation.env` into the subprocess env (HOME,
      CLAUDE_SESSION_ID, optional CLAUDE_FAKE_TIME_OFFSET).
    * Pin the child's working directory by ``chdir``-ing the parent
      around :meth:`ClaudeProcess.start` (Popen inherits cwd at fork).
    * Re-export ``ClaudeProcess``'s stdout / stderr file separation
      without changes.

    The class deliberately mirrors :class:`ClaudeProcess`'s constructor
    parameters so callers familiar with the upstream lifecycle do not
    need to relearn the surface; the only structural addition is the
    ``home`` and ``cwd`` keyword arguments. All other kwargs flow
    straight through to :class:`ClaudeProcess`.

    Lifecycle
    ---------

    1. Build the adapter with the per-eval :class:`HomeIsolation` (which
       MUST have :meth:`HomeIsolation.setup` already run), the prompt,
       and the stdout / stderr file destinations.
    2. Call :meth:`spawn` to actually launch the child. ``spawn``
       returns the underlying :class:`ClaudeProcess` so the caller can
       drive ``.wait()`` / ``.terminate()`` directly — the adapter does
       not interpose on those lifecycle methods, keeping the
       :class:`ClaudeProcess` contract unaltered.

    Parameters
    ----------
    home:
        :class:`HomeIsolation` instance whose ``setup`` has already
        materialized the per-eval HOME. The adapter calls
        :meth:`HomeIsolation.env` at spawn time; calling ``env``
        without ``setup`` would itself raise :class:`RuntimeError`,
        which the adapter does not catch.
    prompt:
        Prompt text delivered to ``claude --print`` over stdin (see
        :meth:`ClaudeProcess.start`).
    output_file:
        Path where ``claude``'s stdout will be written.
    error_file:
        Path where ``claude``'s stderr will be written. Distinct file
        handle from ``output_file`` — required by the AC.
    cwd:
        Working directory the child should inherit. Must exist on disk
        (the adapter resolves it eagerly and raises
        :class:`ClaudeProcessAdapterError` otherwise). Defaults to the
        per-eval HOME directory when not supplied.
    extra_env:
        Optional env-var overlay applied BEFORE
        :meth:`HomeIsolation.env`. Lets callers inject capability
        toggles (e.g. ``CLAUDE_DISABLE_MCP``) without overriding the
        isolation keys; the merge order is ``os.environ → extra_env →
        HomeIsolation.env`` so the isolation layer always wins.
    timeout_seconds, max_turns, model, permission_flag, output_format,
    extra_args, on_spawn, on_signal, on_exit, tool_write_mode:
        Forwarded verbatim to :class:`ClaudeProcess`. See its
        docstring for the contract.
    """

    def __init__(
        self,
        *,
        home: "HomeIsolation",
        prompt: str,
        output_file: Path,
        error_file: Path,
        cwd: Path | None = None,
        extra_env: dict[str, str] | None = None,
        timeout_seconds: int = 6300,
        max_turns: int = 100,
        model: str = "",
        permission_flag: str = "--dangerously-skip-permissions",
        output_format: str = "stream-json",
        extra_args: list[str] | None = None,
        on_spawn: Callable[[int], None] | None = None,
        on_signal: Callable[[int, str], None] | None = None,
        on_exit: Callable[[int, int | None], None] | None = None,
        tool_write_mode: bool = False,
    ) -> None:
        if output_file == error_file:
            raise ClaudeProcessAdapterError(
                "output_file and error_file must be distinct paths "
                "(AC: stdout/stderr separation)"
            )

        self._home = home
        self._prompt = prompt
        self._output_file = Path(output_file)
        self._error_file = Path(error_file)
        self._extra_env: dict[str, str] = dict(extra_env) if extra_env else {}
        self._timeout_seconds = timeout_seconds
        self._max_turns = max_turns
        self._model = model
        self._permission_flag = permission_flag
        self._output_format = output_format
        self._extra_args: list[str] = list(extra_args) if extra_args else []
        self._on_spawn = on_spawn
        self._on_signal = on_signal
        self._on_exit = on_exit
        self._tool_write_mode = tool_write_mode

        # Resolve cwd eagerly so spawn-time errors are localized to
        # construction (the orchestrator pre-builds adapters and only
        # spawns later — fail-fast keeps the failure surface tight).
        self._cwd: Path = Path(cwd) if cwd is not None else None  # type: ignore[assignment]
        # Defer existence check until we know whether to default to
        # home_path. HomeIsolation.home_path raises before setup, which
        # is the failure mode we want here too.
        if self._cwd is None:
            self._cwd = self._home.home_path
        if not self._cwd.exists():
            raise ClaudeProcessAdapterError(
                f"cwd {self._cwd!s} does not exist on disk"
            )

    # ------------------------------------------------------------------
    # Env assembly
    # ------------------------------------------------------------------

    def build_env(self) -> dict[str, str]:
        """Return the env dict the spawned ``claude`` will see.

        Merge order (later keys win):

        1. ``os.environ`` snapshot (taken inside :meth:`ClaudeProcess.
           build_env`, after stripping ``CLAUDECODE`` /
           ``CLAUDE_CODE_ENTRYPOINT`` to prevent nested-session
           detection).
        2. ``extra_env`` (capability toggles, debug flags).
        3. :meth:`HomeIsolation.env` — ``HOME``, ``CLAUDE_SESSION_ID``,
           and optional ``CLAUDE_FAKE_TIME_OFFSET``. Isolation always
           wins so a misconfigured ``extra_env`` cannot leak the
           operator's real HOME into the child.

        The returned dict is the same object semantics as
        :meth:`ClaudeProcess.build_env` (i.e., a new ``dict[str, str]``
        the caller owns).
        """

        # Build a throwaway ClaudeProcess just for its build_env helper.
        # The helper does the CLAUDECODE / CLAUDE_CODE_ENTRYPOINT
        # scrubbing that the adapter must inherit verbatim.
        merged: dict[str, str] = {}
        merged.update(self._extra_env)
        merged.update(self._home.env())
        proc = self._build_process()
        return proc.build_env(env_vars=merged)

    def build_command(self) -> list[str]:
        """Return the argv that will be ``exec``-ed by :class:`ClaudeProcess`.

        Useful for tests and dry-run reporters; the argv is identical
        to what :meth:`ClaudeProcess.build_command` would emit because
        the adapter delegates directly. No anthropic SDK calls are
        involved in either branch.
        """

        return self._build_process().build_command()

    # ------------------------------------------------------------------
    # Process construction
    # ------------------------------------------------------------------

    def _build_process(self) -> ClaudeProcess:
        """Construct a fresh (not started) :class:`ClaudeProcess`.

        The env merge happens via the ``env_vars`` kwarg so
        ``ClaudeProcess`` re-applies its own ``os.environ.copy`` +
        scrub on every call (consistent with its upstream contract).
        """

        merged_env: dict[str, str] = {}
        merged_env.update(self._extra_env)
        # HomeIsolation.env wins by construction (applied last).
        merged_env.update(self._home.env())
        return ClaudeProcess(
            prompt=self._prompt,
            output_file=self._output_file,
            error_file=self._error_file,
            max_turns=self._max_turns,
            model=self._model,
            permission_flag=self._permission_flag,
            timeout_seconds=self._timeout_seconds,
            output_format=self._output_format,
            extra_args=self._extra_args,
            on_spawn=self._on_spawn,
            on_signal=self._on_signal,
            on_exit=self._on_exit,
            env_vars=merged_env,
            tool_write_mode=self._tool_write_mode,
        )

    # ------------------------------------------------------------------
    # Spawn
    # ------------------------------------------------------------------

    @property
    def cwd(self) -> Path:
        """Working directory the child will inherit at fork time."""

        return self._cwd

    @property
    def home(self) -> "HomeIsolation":
        """The :class:`HomeIsolation` driving env injection."""

        return self._home

    def spawn(self) -> ClaudeProcess:
        """Construct and start a :class:`ClaudeProcess` with cwd pinned.

        Steps:

        1. Build a fresh :class:`ClaudeProcess` instance (so the
           adapter can be re-spawned without leaking the prior child).
        2. ``chdir`` the parent process to :attr:`cwd`. Popen inherits
           the cwd at fork time, so this is the canonical way to pin
           the child's working directory without modifying the
           upstream :class:`ClaudeProcess` constructor.
        3. Invoke :meth:`ClaudeProcess.start`. Any exception (FileNotFoundError
           for missing ``claude`` binary, OSError for the
           ``output_file`` open, etc.) propagates verbatim.
        4. Restore the parent's prior cwd inside a ``finally`` so
           spawn failures cannot strand the parent in the per-eval
           HOME.

        Thread-safety
        -------------

        ``os.chdir`` is process-wide; concurrent spawns from
        multiple threads can race on cwd. The orchestrator (T03.16)
        serializes spawn calls behind its scheduler so this is a
        non-issue in production. Tests that spawn in parallel must
        either serialize with a lock or pre-pin cwd to a shared root.

        Returns
        -------
        ClaudeProcess
            The started process. The caller owns the lifecycle: call
            ``.wait()`` to block for exit, ``.terminate()`` to send
            SIGTERM, etc.
        """

        proc = self._build_process()
        prior_cwd = Path(os.getcwd())
        try:
            os.chdir(str(self._cwd))
            proc.start()
        finally:
            # Always restore parent cwd, even if start() raised. Use
            # try/except on the restore because the prior cwd could
            # have been deleted under us (rare but documented in
            # os.chdir docs); a failed restore should not mask the
            # original spawn exception.
            try:
                os.chdir(str(prior_cwd))
            except OSError:  # pragma: no cover - defensive
                pass
        return proc
