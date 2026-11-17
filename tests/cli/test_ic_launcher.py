"""Tests for the `ic` launcher script (src/superclaude/scripts/ic).

The script is run for real with `bash`. A stub `claude` first on PATH prints the
three model-slot variables and the arguments it received, so a test can see what
the launcher would have handed to Claude Code. The environment is built from
scratch, so no model variable leaks in from the machine running the tests.
"""

from __future__ import annotations

import shutil
import subprocess
from importlib.resources import files
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    shutil.which("bash") is None, reason="the ic launcher needs bash"
)

IC_SCRIPT = Path(str(files("superclaude.scripts").joinpath("ic")))

# The stub prints one line per fact so tests can match whole lines.
_STUB_CLAUDE = """#!/bin/sh
echo "ran-claude"
echo "OPUS=${ANTHROPIC_DEFAULT_OPUS_MODEL-}"
echo "SONNET=${ANTHROPIC_DEFAULT_SONNET_MODEL-}"
echo "HAIKU=${ANTHROPIC_DEFAULT_HAIKU_MODEL-}"
for a in "$@"; do echo "ARG=$a"; done
"""


def run_ic(
    tmp_path: Path,
    args: list[str],
    aienv: str | None = "",
) -> subprocess.CompletedProcess[str]:
    """Run the script with a stub `claude`.

    `aienv` is the text of the AIENV file; None points AIENV at a file that
    does not exist.
    """
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    stub = bin_dir / "claude"
    stub.write_text(_STUB_CLAUDE)
    stub.chmod(0o755)

    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    aienv_path = tmp_path / "aienv"
    if aienv is not None:
        aienv_path.write_text(aienv)

    env = {
        "PATH": f"{bin_dir}:/usr/bin:/bin",
        "HOME": str(home),
        "AIENV": str(aienv_path),
    }
    return subprocess.run(
        ["bash", str(IC_SCRIPT), *args],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def stub_ran(proc: subprocess.CompletedProcess[str]) -> bool:
    return "ran-claude" in proc.stdout.splitlines()


# ---------------------------------------------------------------------------
# #544: --help must not depend on the AIENV file
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("flag", ["--help", "-h"])
def test_help_works_when_aienv_file_fails(tmp_path, flag):
    proc = run_ic(tmp_path, [flag], aienv="false\n")
    assert proc.returncode == 0, proc.stderr
    assert "ic <alias-or-model>" in proc.stdout
    assert not stub_ran(proc)


def test_help_works_when_aienv_file_is_missing(tmp_path):
    proc = run_ic(tmp_path, ["--help"], aienv=None)
    assert proc.returncode == 0, proc.stderr
    assert "ic <alias-or-model>" in proc.stdout
    assert "not found" not in proc.stderr


def test_normal_launch_still_stops_on_failing_aienv_file(tmp_path):
    proc = run_ic(tmp_path, [], aienv="false\n")
    assert proc.returncode != 0
    assert not stub_ran(proc)


def test_arguments_after_double_dash_are_not_help(tmp_path):
    proc = run_ic(tmp_path, ["--", "--help"])
    assert proc.returncode == 0, proc.stderr
    assert "ARG=--help" in proc.stdout.splitlines()
    assert "ic <alias-or-model>" not in proc.stdout


def test_option_value_named_help_is_not_help(tmp_path):
    proc = run_ic(tmp_path, ["-H", "--help"])
    assert proc.returncode == 0, proc.stderr
    assert "HAIKU=--help" in proc.stdout.splitlines()
    assert "ic <alias-or-model>" not in proc.stdout
