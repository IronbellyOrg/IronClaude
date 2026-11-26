import os
import subprocess

from conftest import R3


def sh(cmd, **env):
    return subprocess.run(
        ["bash", "-c", f"source {R3}/lib/common.sh; {cmd}"],
        capture_output=True,
        text=True,
        env={**os.environ, **env},
    )


def test_allowed_models_pass():
    for m in (
        "muse-ember-1.0",
        "gpt-6-luna",
        "claude-haiku-5-5",
        "claude-sonnet-5-5",
        "grok-4.7",
    ):
        assert sh(f"r3_assert_model {m}").returncode == 0


def test_refused_models():
    for m in ("Qwen3.8-max", "glm-5.3", "claude-opus-5-5", "gpt-6.1-sol", '""'):
        assert sh(f"r3_assert_model {m}").returncode == 1, m


def test_reviewer_refuses_without_nofallback(tmp_path):
    e = {k: v for k, v in os.environ.items() if k != "NOFALLBACK"}
    for mode in ("phase1", "phase2"):
        r = subprocess.run(
            [
                "bash",
                str(R3 / "lib/reviewer.sh"),
                mode,
                str(tmp_path / "TASK-WF-x"),
                "t4-1",
                "gpt-6-luna",
            ],
            capture_output=True,
            text=True,
            env=e,
        )
        assert r.returncode == 1 and "NOFALLBACK" in r.stderr
    r = subprocess.run(
        [
            "bash",
            str(R3 / "lib/reviewer.sh"),
            "phase1",
            str(tmp_path / "TASK-WF-x"),
            "t4-1",
            "glm-5.3",
        ],
        capture_output=True,
        text=True,
        env={**e, "NOFALLBACK": "1"},
    )
    assert r.returncode == 1
