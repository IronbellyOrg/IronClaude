"""Tests for the entry point of the vcs helper: ``emit`` and the exit codes (FR-010, FR-012).

``emit`` is the one place that prints JSON: sorted keys, lists capped at 200 entries
with a ``truncated`` flag, output above 64 KiB refused (NFR-006, NFR-007).
"""

from __future__ import annotations

import importlib
import io
import json
import subprocess
import sys

import pytest

from .conftest import SCRIPTS


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


def emitted(vcs, obj):
    stream = io.StringIO()
    code = vcs.emit(obj, stream=stream)
    return code, stream.getvalue()


def test_emit_sorts_keys_and_adds_the_contract(vcs):
    code, text = emitted(vcs, {"verb": "x", "status": "ok", "a": 1})
    assert code == 0
    assert text.endswith("\n") and text.count("\n") == 1
    data = json.loads(text)
    assert data["vcs_contract"] == "1"
    assert list(data) == sorted(data)
    assert text == vcs.emit_text(data)


def test_emit_forces_the_contract_value(vcs):
    _, text = emitted(vcs, {"vcs_contract": "9", "verb": "x", "status": "ok"})
    assert json.loads(text)["vcs_contract"] == "1"


def test_emit_caps_lists_at_200(vcs):
    _, text = emitted(
        vcs, {"verb": "x", "status": "ok", "paths": [f"p{i}" for i in range(500)]}
    )
    data = json.loads(text)
    assert len(data["paths"]) == 200
    assert data["paths"][0] == "p0"
    assert data["truncated"] is True


def test_emit_caps_nested_lists_and_keeps_a_short_list_whole(vcs):
    _, text = emitted(
        vcs,
        {
            "verb": "x",
            "status": "ok",
            "rows": [{"inner": list(range(201))}],
            "few": [1, 2, 3],
        },
    )
    data = json.loads(text)
    assert len(data["rows"][0]["inner"]) == 200
    assert data["few"] == [1, 2, 3]
    assert data["truncated"] is True


def test_emit_not_truncated_is_false(vcs):
    _, text = emitted(vcs, {"verb": "x", "status": "ok", "paths": ["a"]})
    assert json.loads(text)["truncated"] is False


def test_emit_keeps_a_truncated_flag_the_verb_set(vcs):
    _, text = emitted(vcs, {"verb": "x", "status": "ok", "truncated": True})
    assert json.loads(text)["truncated"] is True


def test_emit_refuses_output_above_64_kib(vcs):
    code, text = emitted(vcs, {"verb": "x", "status": "ok", "blob": "a" * 70000})
    assert code == 0
    data = json.loads(text)
    assert (data["status"], data["reason"]) == ("refused", "output-too-large")
    assert data["verb"] == "x"
    assert data["vcs_contract"] == "1"
    assert len(text) < 1000


def test_emit_is_deterministic_for_odd_bytes_in_paths(vcs):
    obj = {"verb": "x", "status": "ok", "p": "caf\udcffé"}
    assert emitted(vcs, obj) == emitted(vcs, obj)


def run_cli(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "vcs.py"), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_cli_preflight_prints_one_json_object(repo):
    done = run_cli("preflight", "--cwd", str(repo.work))
    assert done.returncode == 0, done.stderr
    assert done.stdout.count("\n") == 1
    data = json.loads(done.stdout)
    assert data["vcs_contract"] == "1"
    assert data["verb"] == "preflight"


def test_cli_preflight_defaults_to_the_current_directory(repo):
    done = run_cli("preflight", cwd=repo.work)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["top"] == str(repo.work.resolve())


def test_cli_exit_0_even_when_the_status_is_refused(repo):
    done = run_cli("preflight", "--cwd", str(repo.work))  # main is protected
    assert done.returncode == 0
    assert json.loads(done.stdout)["status"] == "refused"


@pytest.mark.parametrize(
    "args", [[], ["no-such-verb"], ["preflight", "--bogus"], ["preflight", "--cwd"]]
)
def test_cli_usage_error_exits_64(args):
    done = run_cli(*args)
    assert done.returncode == 64
    assert done.stdout == ""
    assert done.stderr.strip()


def test_cli_missing_directory_exits_69(tmp_path):
    done = run_cli("preflight", "--cwd", str(tmp_path / "absent"))
    assert done.returncode == 69
    assert done.stdout == ""
    assert "lookup failed" in done.stderr


def test_cli_missing_git_binary_exits_69(repo, tmp_path, monkeypatch):
    empty = tmp_path / "empty-bin"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))
    done = run_cli("preflight", "--cwd", str(repo.work))
    assert done.returncode == 69
    assert done.stdout == ""
    assert "lookup failed" in done.stderr


def test_cli_timeout_exits_69(vcs, repo, plan_module, monkeypatch):
    class Slow(plan_module.GitRunner):
        def run(self, argv, **kw):
            return plan_module.TIMEOUT_RC, ""

    with pytest.raises(vcs.LookupFailed):
        vcs.run_preflight(str(repo.work), make_runner=Slow)
    monkeypatch.setattr(vcs, "GitRunner", Slow)
    assert vcs.main(["preflight", "--cwd", str(repo.work)]) == 69


@pytest.fixture
def plan_module(scripts_dir):
    return importlib.import_module("vcs_plan")
