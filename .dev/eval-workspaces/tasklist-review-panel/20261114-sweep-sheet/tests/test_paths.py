"""K1: writes stay under SW, SB or /tmp; overrides are judged by kind (TESTING section 4)."""

import os

import pytest
from helpers import REPO, SW, sh


def test_accepts_sw_sb_and_tmp(tmp_path):
    assert sh(f"sw_assert_writable {SW}/runs/x").returncode == 0
    assert sh("sw_assert_writable /tmp/evalsb-sweep/TASK-WF-x/repo").returncode == 0
    assert sh(f"sw_assert_writable {tmp_path}/out").returncode == 0


def test_refuses_output_outside_sw(tmp_path):
    for p in (
        REPO / "src/superclaude/x.py",
        REPO / "tests/x.py",
        REPO / ".claude/skills/x",
        REPO / ".dev/tasks/to-do/x",
        SW / ".." / "20261113-collab/x",
        "/home/coder/not-here",
    ):
        r = sh(f"sw_assert_writable '{p}'")
        assert r.returncode == 1, p
        assert "E_NOT_WRITABLE" in r.stderr, p
    # a dot-dot path that starts under SW but leaves it
    assert sh(f"sw_assert_writable '{SW}/../../../../src/x'").returncode == 1
    # a symlink under /tmp that points into src is judged by where it leads
    link = tmp_path / "to-src"
    os.symlink(REPO / "src", link)
    r = sh(f"sw_assert_writable '{link}/x'")
    assert r.returncode == 1 and "E_NOT_WRITABLE" in r.stderr


def test_override_must_be_under_tmp(tmp_path):
    for name in ("SW_SB_ROOT", "SW_SRC_REPO"):
        assert sh(f"sw_assert_override {name} {tmp_path}/sb").returncode == 0, name
        for bad in ("/home/x", str(REPO), "/tmp", "/tmp/../home/x"):
            r = sh(f"sw_assert_override {name} '{bad}'")
            assert r.returncode == 1 and "E_OVERRIDE" in r.stderr, (name, bad)
    # set in the environment, the check runs when common.sh is sourced and stops the shell
    r = sh("echo reached", {"SW_SB_ROOT": "/home/x"})
    assert r.returncode == 1 and "E_OVERRIDE" in r.stderr and "reached" not in r.stdout
    r = sh("echo $SB", {"SW_SB_ROOT": str(tmp_path / "sb")})
    assert r.returncode == 0 and r.stdout.strip() == str(tmp_path / "sb")


def test_kill_s_is_numeric_only():
    for ok in ("1", "0.1", "15", "7.5"):
        assert sh(f"sw_assert_override SW_KILL_S '{ok}'").returncode == 0, ok
    for bad in ("9999", "abc", "", "0", "0.05", "15.1", "-1", "1;rm", "1 2"):
        assert sh(f"sw_assert_override SW_KILL_S '{bad}'").returncode == 1, bad
    assert sh("echo reached", {"SW_KILL_S": "1"}).returncode == 0
    for bad in ("9999", "abc"):
        r = sh("echo reached", {"SW_KILL_S": bad})
        assert r.returncode == 1 and "reached" not in r.stdout, bad


def test_prepass_cmd_stub_only():
    for ok in ("sleep 5", "sleep 0.5", "false"):
        assert sh(f"sw_assert_override SW_PREPASS_CMD '{ok}'").returncode == 0, ok
    for bad in (
        "rm -rf x",
        "",
        "sleeper 5",
        "sleep 5; rm -rf x",
        "sleep 5 && true",
        "false | cat",
        "sleep $(id)",
        "true",
    ):
        r = sh(f"sw_assert_override SW_PREPASS_CMD '{bad}'")
        assert r.returncode == 1, bad
    assert sh("echo reached", {"SW_PREPASS_CMD": "sleep 5"}).returncode == 0
    r = sh("echo reached", {"SW_PREPASS_CMD": "rm -rf x"})
    assert r.returncode == 1 and "reached" not in r.stdout


def test_render_cmd_stub_only():
    assert sh("sw_assert_override SW_RENDER_CMD false").returncode == 0
    for bad in ("true", "", "false; rm -rf x", "sleep 5", "false false"):
        assert sh(f"sw_assert_override SW_RENDER_CMD '{bad}'").returncode == 1, bad
    assert sh("echo reached", {"SW_RENDER_CMD": "false"}).returncode == 0
    r = sh("echo reached", {"SW_RENDER_CMD": "rm -rf x"})
    assert r.returncode == 1 and "reached" not in r.stdout


def test_unknown_override_refused():
    assert sh("sw_assert_override SW_OTHER x").returncode == 1


@pytest.mark.parametrize("var", ["SW", "REPO"])
def test_path_variables(var):
    r = sh(f"echo ${var}")
    assert r.stdout.strip() == str({"SW": SW, "REPO": REPO}[var])
