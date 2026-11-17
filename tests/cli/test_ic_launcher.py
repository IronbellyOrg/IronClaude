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


# ---------------------------------------------------------------------------
# #543: an option that needs a value gives a clear message when it has none
# ---------------------------------------------------------------------------

VALUE_OPTIONS = ["-p", "--preset", "-H", "--haiku", "-S", "--sonnet", "-O", "--opus"]


@pytest.mark.parametrize("option", VALUE_OPTIONS)
def test_option_without_value_prints_a_clear_message(tmp_path, option):
    proc = run_ic(tmp_path, [option])
    assert proc.returncode == 2
    assert f"ic: option {option} requires a value" in proc.stderr
    assert "unbound variable" not in proc.stderr
    assert not stub_ran(proc)


def test_option_without_value_after_other_arguments(tmp_path):
    proc = run_ic(tmp_path, ["--no-yolo", "-S"])
    assert proc.returncode == 2
    assert "ic: option -S requires a value" in proc.stderr
    assert not stub_ran(proc)


def test_preset_with_a_value_still_sets_every_slot(tmp_path):
    aienv = 'export IC_PRESET_coding="opus=o-model sonnet=s-model haiku=h-model"\n'
    proc = run_ic(tmp_path, ["-p", "coding"], aienv=aienv)
    assert proc.returncode == 0, proc.stderr
    lines = proc.stdout.splitlines()
    assert {"OPUS=o-model", "SONNET=s-model", "HAIKU=h-model"} <= set(lines)


def test_unknown_preset_still_exits_2(tmp_path):
    proc = run_ic(tmp_path, ["-p", "nosuchpreset"])
    assert proc.returncode == 2
    assert "unknown preset 'nosuchpreset'" in proc.stderr


# ---------------------------------------------------------------------------
# #542: only alias names resolve through a variable; everything else is literal
# ---------------------------------------------------------------------------

ALIASES = "export kimi=kimi-k2.6\n"

# (arguments that carry one model value as "{v}", slot line the stub prints)
SLOT_FORMS = [
    (["-H", "{v}"], "HAIKU"),
    (["--haiku", "{v}"], "HAIKU"),
    (["-S", "{v}"], "SONNET"),
    (["--sonnet", "{v}"], "SONNET"),
    (["-O", "{v}"], "OPUS"),
    (["--opus", "{v}"], "OPUS"),
    (["{v}"], "HAIKU"),  # bare positional shortcut sets the haiku slot
]


def slot_args(form: list[str], value: str) -> list[str]:
    return [a.replace("{v}", value) for a in form]


@pytest.mark.parametrize("name", ["HOME", "PATH"])
@pytest.mark.parametrize("form,slot", SLOT_FORMS)
def test_environment_variable_names_are_not_resolved(tmp_path, form, slot, name):
    proc = run_ic(tmp_path, ["--no-yolo", *slot_args(form, name)], aienv=ALIASES)
    assert proc.returncode == 0, proc.stderr
    assert f"{slot}={name}" in proc.stdout.splitlines()


def test_uppercase_variable_defined_in_aienv_is_not_an_alias(tmp_path):
    aienv = ALIASES + "export SOME_SETTING=not-a-model\n"
    proc = run_ic(tmp_path, ["-H", "SOME_SETTING"], aienv=aienv)
    assert "HAIKU=SOME_SETTING" in proc.stdout.splitlines()


@pytest.mark.parametrize("form,slot", SLOT_FORMS)
def test_lowercase_alias_from_aienv_still_resolves(tmp_path, form, slot):
    proc = run_ic(tmp_path, slot_args(form, "kimi"), aienv=ALIASES)
    assert proc.returncode == 0, proc.stderr
    assert f"{slot}=kimi-k2.6" in proc.stdout.splitlines()


def test_literal_model_ids_pass_through(tmp_path):
    for value in ("qwen3.6-plus", "nosuchalias"):
        proc = run_ic(tmp_path, ["-H", value], aienv=ALIASES)
        assert f"HAIKU={value}" in proc.stdout.splitlines()


def test_preset_values_follow_the_same_rule(tmp_path):
    aienv = ALIASES + 'export IC_PRESET_mix="opus=HOME sonnet=PATH haiku=kimi"\n'
    proc = run_ic(tmp_path, ["-p", "mix"], aienv=aienv)
    assert proc.returncode == 0, proc.stderr
    lines = proc.stdout.splitlines()
    assert {"OPUS=HOME", "SONNET=PATH", "HAIKU=kimi-k2.6"} <= set(lines)
