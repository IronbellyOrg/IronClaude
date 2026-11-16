"""Shared fixtures: SW on sys.path, temporary roots under /tmp, the fake claude first on PATH, the override guard."""

import os
import shlex
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

SW = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SW))

from helpers import sh  # noqa: E402

FAKES = SW / "tests" / "fakes"


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: tests that launch a harness script on the fake claude"
    )
    config.addinivalue_line(
        "markers",
        "freeze: tests that need the real ground truth; the build does not run them",
    )


def guard_overrides(env):
    """Run every SW_* override of env through sw_assert_override of bin/common.sh (K1)."""
    for name, val in env.items():
        if name.startswith("SW_"):
            r = sh(f"sw_assert_override {name} {shlex.quote(val)}")
            assert r.returncode == 0, r.stderr


def assert_fake_first(env):
    """The first `claude` on env's PATH must be tests/fakes/claude, else no test may start a launcher."""
    for d in env["PATH"].split(os.pathsep):
        if (Path(d) / "claude").is_file():
            assert Path(d) / "claude" == FAKES / "claude", (
                f"first claude on PATH is {d}/claude"
            )
            return
    raise AssertionError("no claude on PATH")


@pytest.fixture
def tmp_roots(tmp_path):
    """Roots under the pytest temp dir plus an environment for harness scripts; with_env() guards extra SW_* values."""
    assert str(tmp_path).startswith("/tmp/")
    env = {k: v for k, v in os.environ.items() if not k.startswith(("SW_", "FAKE_"))}
    env.update(
        {
            "PATH": f"{FAKES}{os.pathsep}{os.environ['PATH']}",
            "SW_SB_ROOT": str(tmp_path / "sb"),
            "FAKE_CALL_LOG": str(tmp_path / "calls.log"),
            "NOFALLBACK": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    guard_overrides(env)

    def with_env(**extra):
        e = dict(env, **extra)
        guard_overrides(e)
        assert_fake_first(e)
        return e

    return SimpleNamespace(
        root=tmp_path,
        sb=tmp_path / "sb",
        runs=tmp_path / "runs",
        call_log=tmp_path / "calls.log",
        env=env,
        with_env=with_env,
    )
