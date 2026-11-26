"""K9: the sandbox root of Recipe Ledger is /tmp/evalsb-recipe; the sibling's root is refused with exit 4 (TESTING 4)."""

import os
import subprocess
from pathlib import Path

import pytest

RL = Path(__file__).resolve().parents[1]
ENV_SH = RL / "bin" / "rl-env.sh"
COMMON_SH = RL / "bin" / "common.sh"


def run(snippet, **env):
    e = {k: v for k, v in os.environ.items() if not k.startswith(("SW_", "RL_"))}
    e.update(env)
    return subprocess.run(
        ["bash", "-c", f"source {ENV_SH}; {snippet}"],
        capture_output=True,
        text=True,
        env=e,
    )


def test_own_root_is_the_default():
    r = run('echo "$SW_SB_ROOT"')
    assert r.returncode == 0 and r.stdout.strip() == "/tmp/evalsb-recipe"


def test_common_sh_then_uses_the_own_root():
    """The copied common.sh reads SW_SB_ROOT, so sourcing rl-env.sh first moves every sandbox to the own root."""
    r = run(f'source {COMMON_SH}; echo "$SB"')
    assert r.returncode == 0 and r.stdout.strip() == "/tmp/evalsb-recipe"


@pytest.mark.parametrize(
    "root",
    [
        "/tmp/evalsb-sweep",
        "/tmp/evalsb-sweep/",
        "/tmp/evalsb-sweep/doc1",
        "/tmp/x/../evalsb-sweep",
    ],
)
def test_sibling_root_is_refused(root):
    r = run("echo survived", SW_SB_ROOT=root)
    assert (
        r.returncode == 4
        and "E_SIBLING_ROOT" in r.stderr
        and "survived" not in r.stdout
    )


def test_another_tmp_root_is_accepted():
    r = run('echo "$SW_SB_ROOT"', SW_SB_ROOT="/tmp/evalsb-recipe-test")
    assert r.returncode == 0 and r.stdout.strip() == "/tmp/evalsb-recipe-test"


@pytest.mark.parametrize("value", ["lens", "check", "reask"])
def test_force_exc_accepts_only_the_three_components(value):
    assert run("true", RL_FORCE_EXC=value).returncode == 0


@pytest.mark.parametrize("value", ["bogus", "LENS", "lens,check", "all"])
def test_force_exc_refuses_anything_else(value):
    r = run("echo survived", RL_FORCE_EXC=value)
    assert r.returncode == 2 and "E_HOOK" in r.stderr and "survived" not in r.stdout


LAUNCHER = RL / "bin" / "run-panel.sh"


def test_launcher_sets_its_own_root(tmp_path):
    """K9, the launcher half: run-panel.sh sources rl-env.sh before common.sh, so with no SW_SB_ROOT it works under
    /tmp/evalsb-recipe, and the sibling's root is refused with exit 4 before anything is written."""
    text = LAUNCHER.read_text()
    assert text.index('source "$HERE/rl-env.sh"') < text.index(
        'source "$HERE/common.sh"'
    )
    env = {k: v for k, v in os.environ.items() if not k.startswith(("SW_", "RL_"))}
    env.update(NOFALLBACK="1", RL_RUNS_ROOT=str(tmp_path / "runs"))
    args = [
        "--arm",
        "Z0",
        "--panel",
        "primary",
        "--doc",
        "NO-SUCH-DOC",
        "--replicate",
        "1",
        "--block",
        "1",
    ]
    args += ["--seed", "1", "--run-id", "k9"]
    r = subprocess.run(
        ["bash", str(LAUNCHER), *args], capture_output=True, text=True, env=env
    )
    assert r.returncode == 2 and "NO-SUCH-DOC under /tmp/evalsb-recipe " in r.stderr
    r = subprocess.run(
        ["bash", str(LAUNCHER), *args],
        capture_output=True,
        text=True,
        env=dict(env, SW_SB_ROOT="/tmp/evalsb-sweep"),
    )
    assert r.returncode == 4 and "E_SIBLING_ROOT" in r.stderr
    assert not (tmp_path / "runs").exists()
