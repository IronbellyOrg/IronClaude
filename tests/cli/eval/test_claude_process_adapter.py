"""COMP-013 ClaudeProcessAdapter contract tests (Task T02.19 / D-0038).

These tests pin the T02.19 acceptance criteria as executable assertions:

1. ``ClaudeProcessAdapter`` spawns the real ``claude`` binary with
   ``cwd`` pinned, :meth:`HomeIsolation.env` injected, and stdout /
   stderr written to separate files. Verified via a fake ``claude``
   shim on PATH so the test is host-portable.
2. ``uv run ruff check src/superclaude/cli/eval/`` flags any
   ``anthropic`` SDK import under that subtree. Verified by writing a
   throwaway probe module under ``cli/eval/`` and running ruff
   programmatically; the probe is removed before the test returns
   regardless of outcome.
3. No ``from anthropic`` / ``import anthropic`` import exists anywhere
   under ``src/superclaude/cli/eval/``. Verified by grep over the
   subtree on disk.
4. The adapter never invokes an in-process anthropic SDK code path —
   it always returns a :class:`~superclaude.cli.pipeline.process.
   ClaudeProcess` (real subprocess). Verified by asserting the
   spawned object's class identity.

Test strategy
=============

The adapter wraps :class:`ClaudeProcess`, which itself spawns the
``claude`` binary via :func:`subprocess.Popen`. We do NOT want the
test suite to depend on a real ``claude`` install — that would make
the suite host-coupled and slow. The tests instead place a tiny
shell-script shim named ``claude`` on the front of ``PATH``; the
shim writes a deterministic stdout line, a distinct stderr line, and
exits 0. This exercises the full Popen + fd-routing pipeline while
keeping the test isolated.

A small set of unit-only tests skip the spawn dance and inspect the
adapter's intermediate state (``build_env``, ``build_command``,
``cwd``) directly so they run even on a host without a usable PATH.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from superclaude.cli.eval import (
    ClaudeProcessAdapter,
    ClaudeProcessAdapterError,
    EvalConfig,
    HomeIsolation,
)
from superclaude.cli.pipeline.process import ClaudeProcess

REPO_ROOT = Path(__file__).resolve().parents[3]
EVAL_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "eval"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    root = tmp_path / "eval-runs"
    root.mkdir()
    return root


@pytest.fixture
def permissive_config(scratch_root: Path) -> EvalConfig:
    return EvalConfig(allowed_scratch_roots=(scratch_root,))


@pytest.fixture
def home_iso(scratch_root: Path, permissive_config: EvalConfig) -> HomeIsolation:
    """A :class:`HomeIsolation` with ``setup`` already invoked."""

    iso = HomeIsolation(
        eval_id="E1",
        home_root=scratch_root,
        session_id="sess-T02-19",
    )
    iso.setup(config=permissive_config)
    try:
        yield iso
    finally:
        iso.teardown(keep=False)


@pytest.fixture
def io_files(tmp_path: Path) -> tuple[Path, Path]:
    """Distinct stdout / stderr destinations for the spawned claude."""

    out = tmp_path / "out.log"
    err = tmp_path / "err.log"
    return out, err


@dataclass(frozen=True)
class FakeClaudeShim:
    """Bundle of the bash claude shim path + its marker files."""

    shim: Path
    cwd_marker: Path
    env_marker: Path


@pytest.fixture
def fake_claude_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> FakeClaudeShim:
    """Drop a ``claude`` shim on PATH that writes deterministic stdout/stderr.

    The shim reads its stdin (mimicking the prompt delivery in
    :meth:`ClaudeProcess.start`) and discards it, then emits one line
    to stdout (``__OK__``) and one line to stderr (``__ERR__``) before
    exiting 0. This is enough to assert:

    * stdout was written to ``output_file`` (and only to ``output_file``).
    * stderr was written to ``error_file`` (and only to ``error_file``).
    * The cwd inherited by the child matches ``adapter.cwd``.

    The shim writes its starting cwd to a marker file the test can
    read back so cwd-inheritance is observable.
    """

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    cwd_marker = tmp_path / "cwd-marker.txt"
    env_marker = tmp_path / "env-marker.txt"
    shim = bin_dir / "claude"
    shim.write_text(
        "#!/usr/bin/env bash\n"
        "# Read and discard stdin (ClaudeProcess.start writes the prompt there).\n"
        "cat > /dev/null\n"
        f"pwd > {cwd_marker!s}\n"
        f"printenv HOME > {env_marker!s}\n"
        "echo __OK__\n"
        "echo __ERR__ >&2\n"
        "exit 0\n",
        encoding="utf-8",
    )
    shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", f"{bin_dir!s}{os.pathsep}{os.environ['PATH']}")
    return FakeClaudeShim(shim=shim, cwd_marker=cwd_marker, env_marker=env_marker)


# ---------------------------------------------------------------------------
# AC1 — ClaudeProcessAdapter spawns real claude with HomeIsolation.env()
# ---------------------------------------------------------------------------


def test_spawn_invokes_real_subprocess_not_anthropic_sdk(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
    fake_claude_path: FakeClaudeShim,
) -> None:
    """``spawn()`` returns a started :class:`ClaudeProcess` (real subprocess)."""

    output_file, error_file = io_files
    adapter = ClaudeProcessAdapter(
        home=home_iso,
        prompt="probe",
        output_file=output_file,
        error_file=error_file,
        cwd=home_iso.home_path,
        timeout_seconds=10,
    )
    proc = adapter.spawn()
    try:
        rc = proc.wait()
    finally:
        proc.terminate()
    assert rc == 0
    # Returned object is the real ClaudeProcess type (not a mock and not
    # any anthropic-SDK wrapper).
    assert isinstance(proc, ClaudeProcess)


def test_spawn_separates_stdout_and_stderr_to_distinct_files(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
    fake_claude_path: FakeClaudeShim,
) -> None:
    """AC: stdout written to output_file, stderr to error_file (no cross-leak)."""

    output_file, error_file = io_files
    adapter = ClaudeProcessAdapter(
        home=home_iso,
        prompt="probe",
        output_file=output_file,
        error_file=error_file,
        timeout_seconds=10,
    )
    proc = adapter.spawn()
    try:
        rc = proc.wait()
    finally:
        proc.terminate()
    assert rc == 0
    assert output_file.read_text(encoding="utf-8").strip() == "__OK__"
    assert error_file.read_text(encoding="utf-8").strip() == "__ERR__"
    # No cross-leak: the stdout file MUST NOT contain the stderr marker
    # and vice versa.
    assert "__ERR__" not in output_file.read_text(encoding="utf-8")
    assert "__OK__" not in error_file.read_text(encoding="utf-8")


def test_spawn_pins_child_cwd_to_adapter_cwd(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
    fake_claude_path: FakeClaudeShim,
    tmp_path: Path,
) -> None:
    """AC: ``cwd`` is pinned at fork time; child inherits ``adapter.cwd``."""

    output_file, error_file = io_files
    child_cwd = tmp_path / "child-cwd"
    child_cwd.mkdir()

    adapter = ClaudeProcessAdapter(
        home=home_iso,
        prompt="probe",
        output_file=output_file,
        error_file=error_file,
        cwd=child_cwd,
        timeout_seconds=10,
    )
    prior_cwd = Path.cwd()
    proc = adapter.spawn()
    try:
        proc.wait()
    finally:
        proc.terminate()

    # Parent cwd was restored even though we chdir'd into child_cwd.
    assert Path.cwd() == prior_cwd
    # The shim recorded its starting cwd; symlink resolution is OS-
    # dependent on macOS (/var -> /private/var), so compare resolved paths.
    recorded = Path(
        fake_claude_path.cwd_marker.read_text(encoding="utf-8").strip()
    ).resolve()
    assert recorded == child_cwd.resolve()


def test_spawn_injects_home_isolation_env_into_child(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
    fake_claude_path: FakeClaudeShim,
) -> None:
    """AC: ``HomeIsolation.env`` is injected; child sees per-eval HOME."""

    output_file, error_file = io_files
    adapter = ClaudeProcessAdapter(
        home=home_iso,
        prompt="probe",
        output_file=output_file,
        error_file=error_file,
        timeout_seconds=10,
    )
    proc = adapter.spawn()
    try:
        proc.wait()
    finally:
        proc.terminate()

    recorded_home = Path(
        fake_claude_path.env_marker.read_text(encoding="utf-8").strip()
    ).resolve()
    assert recorded_home == home_iso.home_path.resolve()


# ---------------------------------------------------------------------------
# Build-env / build-command unit tests (no spawn)
# ---------------------------------------------------------------------------


def test_build_env_isolation_keys_win_over_extra_env(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
) -> None:
    """Merge order: ``os.environ -> extra_env -> HomeIsolation.env``."""

    output_file, error_file = io_files
    # Try to spoof HOME via extra_env; HomeIsolation.env() must win.
    adapter = ClaudeProcessAdapter(
        home=home_iso,
        prompt="probe",
        output_file=output_file,
        error_file=error_file,
        extra_env={"HOME": "/should/be/overridden", "EXTRA_KEY": "extra"},
    )
    env = adapter.build_env()
    assert env["HOME"] == str(home_iso.home_path)
    assert env["CLAUDE_SESSION_ID"] == home_iso.session_id
    # extra_env keys that don't collide with isolation are preserved.
    assert env["EXTRA_KEY"] == "extra"
    # ClaudeProcess.build_env scrubs CLAUDECODE / CLAUDE_CODE_ENTRYPOINT.
    assert "CLAUDECODE" not in env
    assert "CLAUDE_CODE_ENTRYPOINT" not in env


def test_build_command_delegates_to_claude_process(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
) -> None:
    """``build_command`` returns the same argv as :meth:`ClaudeProcess.build_command`."""

    output_file, error_file = io_files
    adapter = ClaudeProcessAdapter(
        home=home_iso,
        prompt="probe",
        output_file=output_file,
        error_file=error_file,
        output_format="text",
        model="opus-test",
    )
    cmd = adapter.build_command()
    assert cmd[0] == "claude"
    assert "--print" in cmd
    assert "--output-format" in cmd
    assert "text" in cmd
    assert "opus-test" in cmd


# ---------------------------------------------------------------------------
# AC2 — distinct stdout/stderr paths enforced at construction
# ---------------------------------------------------------------------------


def test_construction_rejects_identical_output_and_error_files(
    home_iso: HomeIsolation,
    tmp_path: Path,
) -> None:
    """AC enforcement: stdout/stderr separation is a construction-time invariant."""

    same = tmp_path / "merged.log"
    with pytest.raises(ClaudeProcessAdapterError):
        ClaudeProcessAdapter(
            home=home_iso,
            prompt="probe",
            output_file=same,
            error_file=same,
        )


def test_construction_rejects_nonexistent_cwd(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
    tmp_path: Path,
) -> None:
    """``cwd`` must exist on disk so the chdir cannot fail at spawn time."""

    output_file, error_file = io_files
    missing = tmp_path / "does-not-exist"
    with pytest.raises(ClaudeProcessAdapterError):
        ClaudeProcessAdapter(
            home=home_iso,
            prompt="probe",
            output_file=output_file,
            error_file=error_file,
            cwd=missing,
        )


def test_default_cwd_is_home_path(
    home_iso: HomeIsolation,
    io_files: tuple[Path, Path],
) -> None:
    """When ``cwd`` is unset, the adapter pins to the per-eval HOME."""

    output_file, error_file = io_files
    adapter = ClaudeProcessAdapter(
        home=home_iso,
        prompt="probe",
        output_file=output_file,
        error_file=error_file,
    )
    assert adapter.cwd == home_iso.home_path


# ---------------------------------------------------------------------------
# AC3/AC4 — ruff ban-import rule + no anthropic imports under cli/eval/
# ---------------------------------------------------------------------------


def test_no_anthropic_imports_anywhere_under_cli_eval() -> None:
    """AC: zero ``import anthropic`` / ``from anthropic`` lines under cli/eval/."""

    offenders = []
    for py_file in EVAL_DIR.rglob("*.py"):
        # Skip the vendored ptytest subtree (T02.01) — upstream sources
        # are outside our authoring scope; per task spec the rule covers
        # superclaude-authored code under cli/eval/.
        if "pty" in py_file.parts and py_file.parts[-2] == "pty":
            continue
        text = py_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            # Skip comments, docstrings already-stripped non-import refs.
            if stripped.startswith("#"):
                continue
            if stripped.startswith("import anthropic") or stripped.startswith(
                "from anthropic"
            ):
                offenders.append(f"{py_file}:{lineno}: {stripped}")
    assert offenders == [], (
        "FR-G1 violation — anthropic SDK imports under cli/eval/:\n"
        + "\n".join(offenders)
    )


def test_ruff_flags_synthetic_anthropic_import_under_cli_eval(
    tmp_path: Path,
) -> None:
    """AC: ``ruff check src/superclaude/cli/eval/`` flags ``import anthropic``.

    The test writes a throwaway probe module under ``cli/eval/``,
    invokes ruff via subprocess, and asserts the TID251 ban-api rule
    fires. The probe is removed in a ``finally`` so a failed ruff run
    does not leave the repo dirty.
    """

    probe = EVAL_DIR / "_t02_19_ban_probe.py"
    probe.write_text(
        "import anthropic\nfrom anthropic import Anthropic\n"
        "_ = (anthropic, Anthropic)\n",
        encoding="utf-8",
    )
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--no-cache",
                str(probe),
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        probe.unlink(missing_ok=True)

    # The probe must trip the rule — non-zero exit AND TID251 in output.
    assert result.returncode != 0, (
        "ruff did not flag the synthetic anthropic import; FR-G1 rule "
        f"is not registered. stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    assert "TID251" in result.stdout, (
        f"Expected TID251 ban-api violation in ruff output; got: {result.stdout!r}"
    )
    assert "anthropic" in result.stdout


def test_ruff_passes_on_real_adapter_module() -> None:
    """Sanity check: the production adapter module passes the ban rule itself."""

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--no-cache",
            "--select=TID251",
            str(EVAL_DIR / "claude_process.py"),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"adapter module trips its own ban rule: {result.stdout!r} {result.stderr!r}"
    )


# ---------------------------------------------------------------------------
# Public-surface assertion — ClaudeProcessAdapter is exported
# ---------------------------------------------------------------------------


def test_public_surface_exports_adapter() -> None:
    """``superclaude.cli.eval`` re-exports the adapter + error class."""

    from superclaude.cli import eval as eval_pkg

    assert "ClaudeProcessAdapter" in eval_pkg.__all__
    assert "ClaudeProcessAdapterError" in eval_pkg.__all__
    assert eval_pkg.ClaudeProcessAdapter is ClaudeProcessAdapter
    assert eval_pkg.ClaudeProcessAdapterError is ClaudeProcessAdapterError


# ---------------------------------------------------------------------------
# Skip-on-host marker for spawn tests that need /bin/bash
# ---------------------------------------------------------------------------


pytestmark = pytest.mark.skipif(
    shutil.which("bash") is None,
    reason="fake claude shim requires bash; skipping spawn tests on host",
)
