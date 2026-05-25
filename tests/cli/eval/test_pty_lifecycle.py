"""TEST-006 / D-0063 — PTY lifecycle integration tests (FR-G1 enforcement).

Pins the FR-G1 "real-subprocess discipline" contract end-to-end. Where
``test_pty_driver.py`` exercises the COMP-007 PtyDriver method surface in
isolation, this module verifies that the **integration** between the
PtyDriver, the FR-LC1 EvalRunner lifecycle, and the real ``claude``
binary holds together.

Coverage matrix (T03.22 / phase-3-tasklist.md):

* **Real spawn + transcript.** ``claude --help`` is spawned via the real
  PtyDriver, the captured output is persisted to a transcript file, and
  the exit code is asserted == 0. Skipped on hosts without the binary.
* **Prompt readiness + input injection.** A deterministic Python
  subprocess stub mimics the prompt-ready / echo round-trip a real
  REPL performs. This isolates the interactive mechanics from the
  real-binary auth requirement.
* **Timeout reaps the child.** A hanging subprocess is driven through
  the EvalRunner with ``timeout_sec=0.5``; the runner returns a
  ``TIMEOUT`` outcome AND the PtyDriver child is terminated (no zombie,
  ``is_alive() is False``).
* **Transcript file existence.** The end-to-end runner path produces a
  transcript file on disk at the path passed to the EvalRunner
  constructor, regardless of outcome status.

The ban-import lint rule (TID251 / ``banned-api``) is covered in a
separate file (``test_ban_import_rule.py``) per the T03.22 AC; this
module focuses on runtime PTY behaviour.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import textwrap
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import pytest

from superclaude.cli.eval import PtyDriver
from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.models import (
    EvalContext,
    EvalSpec,
    ExpectResult,
)
from superclaude.cli.eval.runner import (
    EvalRunner,
    ExecutorContext,
    LifecycleExecutor,
    ObservedRun,
)

# ---------------------------------------------------------------------------
# Stub builders (shared shape with test_pty_driver.py, kept local so the
# integration tests can evolve independently of the unit tests).
# ---------------------------------------------------------------------------


def _prompt_stub_source(exit_code: int = 0) -> str:
    """Python source: banner -> prompt-ready -> echo stdin -> exit."""

    return textwrap.dedent(
        f"""
        import sys
        sys.stdout.write("banner: stub up\\r\\n")
        sys.stdout.write("> \\r\\n")
        sys.stdout.flush()
        line = sys.stdin.readline()
        sys.stdout.write("echo: " + line)
        sys.stdout.flush()
        sys.exit({int(exit_code)})
        """
    ).strip()


def _hang_stub_source() -> str:
    """Python source: print a banner then block on stdin forever.

    Used to exercise the timeout-reap path. The child has no prompt-ready
    marker so ``expect_prompt_ready`` would also time out, but the
    integration tests in this module drive the timeout through the
    EvalRunner so the behaviour observed is the full FR-LC1 reap.
    """

    return textwrap.dedent(
        """
        import sys
        sys.stdout.write("banner only\\r\\n")
        sys.stdout.flush()
        sys.stdin.read()
        """
    ).strip()


# ---------------------------------------------------------------------------
# FakeHome — minimal HomeIsolation duck-type shared with test_runner_class.py
# ---------------------------------------------------------------------------


class FakeHome:
    """HomeIsolation stand-in scoped to the integration tests.

    The runner only consumes ``setup``, ``teardown``, ``env`` and the
    ``home_path`` property, so a hand-rolled mutable class is the
    minimal surface that keeps these tests independent of FR-ISO1's
    containment guard machinery.
    """

    def __init__(
        self,
        *,
        eval_id: str,
        home_root: Path,
        session_id: str = "sess-pty-lifecycle",
    ) -> None:
        self.eval_id = eval_id
        self.home_root = home_root
        self.session_id = session_id
        self._home_path: Path | None = None
        self.last_teardown_keep: bool | None = None

    def setup(self, *, config: EvalConfig) -> Path:
        self.home_root.mkdir(parents=True, exist_ok=True)
        home = self.home_root / f"{self.eval_id}-fake-home"
        home.mkdir(parents=True, exist_ok=True)
        self._home_path = home
        return home

    def teardown(self, keep: bool) -> None:
        self.last_teardown_keep = keep

    def env(self) -> dict[str, str]:
        return {
            "HOME": str(self.home_path),
            "CLAUDE_SESSION_ID": self.session_id,
        }

    @property
    def home_path(self) -> Path:
        if self._home_path is None:
            raise RuntimeError("FakeHome.setup() must run before home_path")
        return self._home_path


# ---------------------------------------------------------------------------
# PtyDriver-backed LifecycleExecutor
# ---------------------------------------------------------------------------


@dataclass
class PtyLifecycleExecutor:
    """Wires a PtyDriver into the FR-LC1 spawn/inject/observe trio.

    The executor owns one driver per ``run()`` invocation. ``spawn``
    starts the child, ``inject`` writes the prompt (after waiting for
    prompt-ready when applicable), and ``observe`` drains stdout into
    the transcript file the runner allocated, blocks on ``wait_exit``,
    and returns an ``ObservedRun``.

    The deliberate split between ``inject`` (prompt-ready + send) and
    ``observe`` (drain + wait_exit) keeps the executor faithful to the
    FR-LC1 contract: spawn never reads stdin, observe never sends
    anything new.
    """

    command: list[str]
    prompt_to_inject: str | None = None
    wait_for_prompt_ready: bool = True
    timeout: float = 5.0
    prompt_ready_pattern: str | None = None
    _driver: PtyDriver | None = field(default=None, init=False, repr=False)
    # ``expect_prompt_ready`` consumes everything up to and including the
    # prompt-ready marker from the pexpect buffer. The text it returns
    # ("the banner the user saw before the prompt") is therefore NOT
    # observable from a subsequent ``read_stdout`` and must be captured
    # at the inject step so observe() can prepend it to the transcript.
    _banner_capture: str = field(default="", init=False, repr=False)

    def spawn(self, ctx: ExecutorContext) -> None:
        kwargs: dict = {"default_timeout": self.timeout}
        if self.prompt_ready_pattern is not None:
            kwargs["prompt_ready_pattern"] = self.prompt_ready_pattern
        self._driver = PtyDriver(command=list(self.command), **kwargs)
        self._driver.spawn()
        self._banner_capture = ""

    def inject(self, ctx: ExecutorContext) -> None:
        driver = self._require_driver()
        if self.wait_for_prompt_ready:
            before = driver.expect_prompt_ready(timeout=self.timeout)
            # Reconstruct the on-screen transcript by re-attaching the
            # banner pexpect consumed plus a marker for the prompt
            # itself. Tests assert on banner text and on ``> ``, so
            # both halves must survive the FR-LC1 inject step.
            self._banner_capture = before + "> \r\n"
        if self.prompt_to_inject is not None:
            driver.inject_prompt(self.prompt_to_inject)

    def observe(self, ctx: ExecutorContext) -> ObservedRun:
        driver = self._require_driver()
        start = time.monotonic()
        collected = self._banner_capture
        deadline = start + self.timeout
        # Drain stdout while the child is alive (and a bit after, in
        # case the PTY still has buffered bytes once the child exits).
        while time.monotonic() < deadline and driver.is_alive():
            chunk = driver.read_stdout(timeout=0.2)
            if chunk:
                collected += chunk
        # Final drain after the child has likely exited.
        collected += driver.read_stdout(timeout=0.2)
        exit_code = driver.wait_exit(timeout=self.timeout)
        duration = time.monotonic() - start
        # Persist the transcript to the path the runner reserved.
        ctx.transcript_path.parent.mkdir(parents=True, exist_ok=True)
        ctx.transcript_path.write_text(collected, encoding="utf-8")
        return ObservedRun(
            exit_code=exit_code,
            stdout=collected,
            stderr="",
            duration_sec=duration,
        )

    # NFR-REL1: the runner calls cancel() from the timeout path so the
    # PtyDriver child is reaped before the orchestrator collects the
    # next outcome. The PtyLifecycleExecutor's daemon worker thread
    # cannot observe this directly (it is stuck in observe()) but
    # cancel() from the main thread terminates the child, which makes
    # the worker's wait_exit unblock and the thread exit.
    def cancel(self) -> None:
        if self._driver is None:
            return
        try:
            if self._driver.is_alive():
                self._driver.terminate(force=True)
        finally:
            self._driver.close()

    # ---------------- helpers ----------------

    def _require_driver(self) -> PtyDriver:
        if self._driver is None:
            raise RuntimeError("PtyLifecycleExecutor.spawn() must run before this")
        return self._driver

    @property
    def driver(self) -> PtyDriver | None:
        return self._driver


_PROTOCOL_CHECK: LifecycleExecutor = PtyLifecycleExecutor(command=["true"])


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    root = tmp_path / "scratch"
    root.mkdir()
    return root


@pytest.fixture
def eval_config(scratch_root: Path) -> EvalConfig:
    return EvalConfig(allowed_scratch_roots=(scratch_root,))


@pytest.fixture
def home(scratch_root: Path) -> FakeHome:
    return FakeHome(eval_id="PtyLifecycleEval", home_root=scratch_root)


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="PtyLifecycleEval", title="pty lifecycle integration")


@pytest.fixture
def run_paths(tmp_path: Path) -> dict[str, Path]:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir()
    return {
        "run_dir": run_dir,
        "artifacts_dir": artifacts_dir,
        "stdout_path": artifacts_dir / "stdout.log",
        "stderr_path": artifacts_dir / "stderr.log",
        "transcript_path": artifacts_dir / "pty.transcript",
    }


def _make_runner(
    *,
    home: FakeHome,
    eval_config: EvalConfig,
    executor: LifecycleExecutor,
    run_paths: dict[str, Path],
    expects: tuple = (),
    deploy_hooks: Callable[[Path], None] | None = None,
    default_timeout_sec: float | None = None,
) -> EvalRunner:
    return EvalRunner(
        home=home,  # type: ignore[arg-type]
        config=eval_config,
        executor=executor,
        run_dir=run_paths["run_dir"],
        artifacts_dir=run_paths["artifacts_dir"],
        stdout_path=run_paths["stdout_path"],
        stderr_path=run_paths["stderr_path"],
        transcript_path=run_paths["transcript_path"],
        expect_callables=expects,
        deploy_hooks=deploy_hooks if deploy_hooks is not None else (lambda _p: None),
        default_timeout_sec=default_timeout_sec,
    )


def _exit_zero_expect(ctx: EvalContext) -> ExpectResult:
    return ExpectResult(
        name="exit_zero",
        passed=ctx.exit_code == 0,
        message=f"exit_code={ctx.exit_code!r}",
    )


# ---------------------------------------------------------------------------
# 1. Real ``claude --help`` smoketest (opt-in; skips when binary missing)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    shutil.which("claude") is None,
    reason="real claude binary not installed on this host",
)
def test_real_claude_help_spawn_and_transcript(
    eval_spec, home, eval_config, run_paths
):
    """FR-G1 — drive the real ``claude --help`` through the lifecycle.

    ``--help`` is non-interactive: the binary prints usage text and
    exits. We therefore skip the prompt-ready expectation and just
    verify (a) spawn succeeded, (b) the transcript was written to the
    runner-allocated path, (c) ``Usage`` appeared somewhere in the
    captured output (the standard help banner), and (d) the exit code
    was 0.
    """

    executor = PtyLifecycleExecutor(
        command=["claude", "--help"],
        prompt_to_inject=None,
        wait_for_prompt_ready=False,
        timeout=15.0,
    )
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_exit_zero_expect,),
        default_timeout_sec=20.0,
    )

    outcome = runner.run(eval_spec)

    transcript = run_paths["transcript_path"]
    assert transcript.is_file(), f"transcript not written at {transcript}"
    captured = transcript.read_text(encoding="utf-8")
    assert "Usage" in captured or "usage" in captured, (
        f"expected help banner in transcript; got: {captured[:300]!r}"
    )
    assert outcome.status == "PASS", (
        f"expected PASS; got {outcome.status} / error_class={outcome.error_class}"
    )


# ---------------------------------------------------------------------------
# 2. Prompt-ready + input injection (deterministic stub)
# ---------------------------------------------------------------------------


def test_lifecycle_prompt_ready_and_input_injection(
    eval_spec, home, eval_config, run_paths
):
    """The interactive REPL contract: wait for ``> ``, send a line, see it echoed.

    Uses a Python stub instead of the real ``claude`` binary so the
    assertion is deterministic on hosts where the binary is not
    authenticated (real claude requires auth even for interactive
    mode). The PtyDriver / LifecycleExecutor wiring is identical to
    the real-binary path; only the child is different.
    """

    executor = PtyLifecycleExecutor(
        command=[sys.executable, "-u", "-c", _prompt_stub_source()],
        prompt_to_inject="hello-from-test",
        wait_for_prompt_ready=True,
        timeout=5.0,
    )
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_exit_zero_expect,),
        default_timeout_sec=10.0,
    )

    outcome = runner.run(eval_spec)

    transcript = run_paths["transcript_path"]
    assert transcript.is_file(), f"transcript missing at {transcript}"
    captured = transcript.read_text(encoding="utf-8")
    assert "banner: stub up" in captured, captured
    assert "> " in captured, "prompt-ready marker missing from transcript"
    assert "echo: hello-from-test" in captured, (
        f"stub echo missing — inject_prompt did not round-trip: {captured!r}"
    )
    assert outcome.status == "PASS", (
        f"expected PASS; got {outcome.status} / error_class={outcome.error_class}"
    )
    assert executor.driver is not None and executor.driver.exit_code == 0


# ---------------------------------------------------------------------------
# 3. Timeout reaps the child (no zombie)
# ---------------------------------------------------------------------------


def test_lifecycle_timeout_reaps_child(
    home, eval_config, run_paths
):
    """A hanging subprocess must be reaped when the runner's timeout fires.

    The stub blocks forever on ``stdin.read()``. With
    ``timeout_sec=0.5`` on the spec, the EvalRunner timeout path
    (``EvalRunner._handle_timeout``) fires, calls ``cancel()`` on the
    executor (which terminates the PtyDriver child), and returns a
    ``TIMEOUT`` outcome. We assert the outcome status AND that the
    PtyDriver reports the child is dead — both halves of the no-zombie
    contract.
    """

    spec = EvalSpec(
        id="PtyLifecycleEval",
        title="timeout reaps child",
        timeout_sec=1,  # spec.timeout_sec is int; will be overridden below
    )
    # spec.timeout_sec is int per the dataclass; we want a sub-second
    # timeout to keep this test fast. The runner's ``_resolve_timeout``
    # falls back to ``default_timeout_sec`` if ``spec.timeout_sec`` is
    # missing or 0. Use the default_timeout_sec constructor knob (float)
    # to pin 0.5s precisely.
    spec = EvalSpec(id="PtyLifecycleEval", title="timeout reaps child")

    executor = PtyLifecycleExecutor(
        command=[sys.executable, "-u", "-c", _hang_stub_source()],
        prompt_to_inject="never-arrives",
        # The stub never emits the prompt-ready marker, so we must NOT
        # wait for it — otherwise the executor's inject() blocks
        # inside expect_prompt_ready and the timeout fires there
        # instead of at the EvalRunner layer. Skipping expect_prompt
        # also matches the "child hangs after spawn" failure mode the
        # NFR-REL1 reap path was designed for.
        wait_for_prompt_ready=False,
        timeout=30.0,
    )
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(),
        default_timeout_sec=0.5,
    )

    outcome = runner.run(spec)

    assert outcome.status == "TIMEOUT", (
        f"expected TIMEOUT; got {outcome.status} / error_class={outcome.error_class}"
    )
    # NFR-REL1 reap: the executor's cancel() ran and terminated the
    # child. Give the OS a tick to finalize the wait().
    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline:
        if executor.driver is None or not executor.driver.is_alive():
            break
        time.sleep(0.05)
    assert executor.driver is not None
    assert not executor.driver.is_alive(), (
        "PtyDriver child still alive after timeout — zombie not reaped"
    )


# ---------------------------------------------------------------------------
# 4. Transcript file existence (end-to-end through EvalRunner)
# ---------------------------------------------------------------------------


def test_lifecycle_transcript_persisted_end_to_end(
    eval_spec, home, eval_config, run_paths
):
    """The runner-allocated transcript path must hold output after run()."""

    executor = PtyLifecycleExecutor(
        command=[sys.executable, "-u", "-c", _prompt_stub_source(exit_code=0)],
        prompt_to_inject="ping",
        wait_for_prompt_ready=True,
        timeout=5.0,
    )
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        default_timeout_sec=10.0,
    )

    outcome = runner.run(eval_spec)

    assert outcome.status == "PASS"
    transcript = run_paths["transcript_path"]
    assert transcript.is_file()
    text = transcript.read_text(encoding="utf-8")
    assert "banner: stub up" in text
    assert "echo: ping" in text

    # JSONL log written under home_path/.eval-logs/ — the FR-LC1 +
    # COMP-004 contract guarantees this for every completed run.
    log_path = home.home_path / ".eval-logs" / f"{eval_spec.id}.jsonl"
    assert log_path.is_file(), f"per-eval JSONL log missing at {log_path}"


# ---------------------------------------------------------------------------
# 5. FR-G1 import-discipline cross-check (runtime probe)
# ---------------------------------------------------------------------------


def test_eval_package_does_not_import_anthropic_at_runtime() -> None:
    """FR-G1 also forbids importing ``anthropic`` inside ``cli/eval``.

    The static ban is enforced by ruff (TID251, covered in
    ``test_ban_import_rule.py``). This runtime probe defends against a
    future edit that dynamically imports ``anthropic`` via
    ``importlib`` to sidestep the linter: after loading every public
    submodule of ``superclaude.cli.eval``, ``sys.modules`` must not
    contain ``anthropic`` from this package's side.
    """

    code = textwrap.dedent(
        """
        import importlib
        import sys
        import pkgutil

        package = importlib.import_module("superclaude.cli.eval")
        for _info in pkgutil.iter_modules(package.__path__):
            try:
                importlib.import_module(f"superclaude.cli.eval.{_info.name}")
            except Exception:
                # Some submodules guard imports behind optional deps.
                # Skip them — the only thing we care about is that
                # importing them does not pull anthropic into sys.modules.
                pass
        leaked = [m for m in sys.modules if m == "anthropic" or m.startswith("anthropic.")]
        if leaked:
            raise SystemExit(f"FR-G1 violation: anthropic leaked into sys.modules: {leaked}")
        """
    ).strip()
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        # Run from the repo root so the import path is the installed
        # editable copy, not a transient site-packages snapshot.
        cwd=Path(__file__).resolve().parents[3],
        check=False,
    )
    assert result.returncode == 0, (
        f"FR-G1 runtime probe failed.\nstdout={result.stdout!r}\nstderr={result.stderr!r}"
    )
