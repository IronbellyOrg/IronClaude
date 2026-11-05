"""Regression tests for the packaged ccsession skill and model shim."""

from __future__ import annotations

import fcntl
import gzip
import http.server
import json
import os
import pty
import re
import runpy
import select
import shutil
import socket
import stat
import subprocess
import sys
import termios
import threading
import time
import urllib.request
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "ccsession-tag"
sys.path.insert(0, str(SKILL_DIR))
import models  # noqa: E402

from superclaude.cli.eval.commands import _parse_version  # noqa: E402

# A fake shim reports the code fingerprint of the real one, so launches reuse it.
SHIM_CODE = models.code_digest(str(SKILL_DIR / "local-gateway-alias-proxy.py"))


@pytest.fixture(autouse=True)
def _offline_model_data(monkeypatch, tmp_path_factory):
    """Keep tests off the network, the real model-data cache, and tier settings.

    Developers run these tests inside Coder workspaces, whose shell exports the
    tier variables and whose image has the workspace env file; neither may leak
    into a test that expects the Mac behaviour.
    """
    monkeypatch.setenv("CCSESSION_MODELS_REFRESH", "0")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path_factory.mktemp("cache")))
    monkeypatch.setenv(
        "AIDEV_AI_DEFAULTS_PATH", "/nonexistent/ccsession-test/defaults.sh"
    )
    for name in list(os.environ):
        if name.startswith("T") and ("Model" in name or name.endswith("_WINDOW")):
            monkeypatch.delenv(name)
        # A developer's Orca terminal: the hooks would rename its real tab.
        if name.startswith("ORCA_"):
            monkeypatch.delenv(name)
    for name in (
        "CLAUDECODE",  # set when the tests run inside Claude Code
        "CLAUDE_CODE_DISABLE_TERMINAL_TITLE",
        "CCSESSION_LAUNCH_ID",
        "CCSESSION_LAUNCH_CWD",
        "CLAUDE_ENV_FILE",
        # Orca tab records go under each test's own HOME.
        "XDG_STATE_HOME",
        "CLAUDE_TOPIC",
        "CCSESSION_TOPIC_CWD",
        # A permission choice or flag override exported in the developer's shell
        # would change the flags every launch test expects (and a bad value
        # makes ccsession exit 2).
        "CCSESSION_PERMISSIONS",
        "CC_CLAUDE_FLAGS",
    ):
        monkeypatch.delenv(name, raising=False)
    for name in (
        "CCSESSION_DEFAULT_TIER",
        "CCSESSION_SHOW_ALL_MODELS",
        "CCSESSION_TIERS",
        "CCSESSION_ACCESS",
        "CCSESSION_TIER_RULES",
        "CCSESSION_MODEL_ORDER",
        # The workspace owner is part of the shim settings fingerprint.
        "CODER_WORKSPACE_OWNER_NAME",
        "CODER_WORKSPACE_OWNER_ROLES",
    ):
        monkeypatch.delenv(name, raising=False)


def _profile_result(tmp_path: Path, profile: str, shim: bool = True) -> dict[str, str]:
    home = tmp_path / profile
    home.mkdir()
    fake_bin = tmp_path / f"claude-{profile}"
    fake_bin.write_text(
        """#!/usr/bin/env python3
import json, os, sys
print(json.dumps({
    "model": sys.argv[sys.argv.index("--model") + 1],
    "context": os.environ.get("CLAUDE_CODE_MAX_CONTEXT_TOKENS", ""),
    "compact": os.environ.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW", ""),
    "custom": os.environ.get("ANTHROPIC_CUSTOM_MODEL_OPTION", ""),
}))
"""
    )
    fake_bin.chmod(fake_bin.stat().st_mode | stat.S_IXUSR)
    fake_lsof = tmp_path / "lsof"
    fake_lsof.write_text("#!/bin/sh\nprintf '4242\\n'\n")
    fake_lsof.chmod(fake_lsof.stat().st_mode | stat.S_IXUSR)
    fake_curl = tmp_path / "curl"
    fake_curl.write_text(
        '#!/bin/sh\nprintf \'{"service":"ccsession-gateway-alias-proxy",'
        '"upstream":"http://gateway.example:4000/cli","port":4555,"model_data":"t",'
        '"tiers":{},"show_all":false,"settings":"e3b0c44298fc1c14",'
        f'"code":"{SHIM_CODE}"}}\'\n'
    )
    fake_curl.chmod(fake_curl.stat().st_mode | stat.S_IXUSR)

    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "CLAUDE_BIN": str(fake_bin),
            "PATH": f"{tmp_path}:{env['PATH']}",
            "ANTHROPIC_BASE_URL": "http://gateway.example:4000/cli",
            "CC_SHIM_PORT": "4555",
            "CC_SHIM_SCRIPT": str(SKILL_DIR / "local-gateway-alias-proxy.py"),
        }
    )
    command = [str(SKILL_DIR / "ccsession"), "--profile", profile]
    if shim:
        command.append("--shim")
    result = subprocess.run(
        command, env=env, text=True, capture_output=True, check=True
    )
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_profiles_launch_expected_models_and_windows(tmp_path: Path) -> None:
    expected = {
        "claude": ("claude-opus-5-5[1m]", "1000000", "1000000", ""),
        "gpt": ("gpt-6.1-sol", "850000", "850000", "gpt-6.1-sol"),
        "grok": ("grok-4.7", "500000", "500000", "grok-4.7"),
        "muse": ("muse-spark-1.3", "950000", "950000", "muse-spark-1.3"),
        "wonderfull": (
            "muse-wonder-full-1.0",
            "1000000",
            "1000000",
            "muse-wonder-full-1.0",
        ),
        "wonder": ("muse-wonder-1.0", "1000000", "1000000", "muse-wonder-1.0"),
        "qwen": ("Qwen3.8-max", "1000000", "1000000", "Qwen3.8-max"),
        "glm": ("glm-5.3", "1000000", "1000000", "glm-5.3"),
    }
    for profile, wanted in expected.items():
        result = _profile_result(tmp_path, profile, shim=profile != "claude")
        assert tuple(result.values()) == wanted


def test_help_lists_all_commands_and_profiles() -> None:
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--help"],
        text=True,
        capture_output=True,
        check=True,
    )
    for expected in (
        "--profile claude",
        "--profile muse",
        "--profile wonderfull",
        "--profile wonder",
        "--profile gpt",
        "--profile qwen",
        "--profile glm",
        "--list",
        "--here",
        "--rm",
    ):
        assert expected in result.stdout


def _addon_launch(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    home = tmp_path / "home"
    addons = home / ".config" / "ccsession" / "profiles.d"
    addons.mkdir(parents=True, exist_ok=True)
    addon = addons / "local.sh"
    addon.write_text(
        "ccsession_profile_local_test() {\n"
        "  CCSESSION_SKIP_ENV_FILE=1\n"
        "  CCSESSION_REFUSE_SHIM=1\n"
        "}\n"
    )
    addon.chmod(0o600)
    work_env = tmp_path / "work.env"
    work_env.write_text("export CCSESSION_WORK_FILE=loaded\n")
    fake_bin = tmp_path / "claude-addon"
    fake_bin.write_text(
        """#!/usr/bin/env python3
import json, os, sys
print(json.dumps({"argv": sys.argv[1:],
                  "work": os.environ.get("CCSESSION_WORK_FILE", ""),
                  "context": os.environ.get("CLAUDE_CODE_MAX_CONTEXT_TOKENS", "")}))
"""
    )
    fake_bin.chmod(0o700)
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "CLAUDE_BIN": str(fake_bin),
            "CCSESSION_ENV_FILE": str(work_env),
        }
    )
    env.pop("CLAUDE_CODE_MAX_CONTEXT_TOKENS", None)
    return subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        env=env,
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )


def test_local_addon_profile_controls_env_model_and_shim(tmp_path: Path) -> None:
    result = _addon_launch(tmp_path, "--profile", "local-test")
    assert result.returncode == 0, result.stderr
    child = json.loads(result.stdout.strip().splitlines()[-1])
    assert "--model" not in child["argv"]
    assert child["work"] == ""
    assert child["context"] == ""
    refused = _addon_launch(tmp_path, "--profile", "local-test", "--shim")
    assert refused.returncode == 2
    assert "cannot use the company gateway shim" in refused.stderr
    company = _addon_launch(tmp_path, "--profile", "claude")
    assert company.returncode == 0, company.stderr
    assert json.loads(company.stdout.strip().splitlines()[-1])["work"] == "loaded"


def test_local_addon_that_others_can_write_is_ignored(tmp_path: Path) -> None:
    _addon_launch(tmp_path, "--profile", "claude")
    addon_dir = tmp_path / "home" / ".config" / "ccsession" / "profiles.d"
    loose = addon_dir / "loose.sh"
    loose.write_text("ccsession_profile_loose() { :; }\n")
    loose.chmod(0o666)
    result = _addon_launch(tmp_path, "--profile", "loose")
    assert result.returncode == 2
    assert "skipping add-on not owner-only" in result.stderr
    assert "unknown profile 'loose'" in result.stderr


def _seed(tmp_path: Path, content: str | None, url: str) -> Path:
    env_file = tmp_path / "ccsession.env"
    example = SKILL_DIR / "ccsession.env.example"
    env_file.write_text(example.read_text() if content is None else content)
    env = os.environ.copy()
    env["ANTHROPIC_BASE_URL"] = url
    subprocess.run(
        [sys.executable, str(SKILL_DIR / "seed-env.py"), str(env_file), str(example)],
        env=env,
        check=True,
        capture_output=True,
    )
    return env_file


def test_seed_records_gateway_only_in_unedited_env(tmp_path: Path) -> None:
    seeded = _seed(tmp_path, None, "http://gateway.example:4000/cli")
    text = seeded.read_text()
    assert "export ANTHROPIC_BASE_URL=http://gateway.example:4000/cli" in text
    assert "LITELLM" not in text.split("captured from the workspace")[1]
    assert stat.S_IMODE(seeded.stat().st_mode) == 0o600
    # A later install with a new address refreshes the installer-owned file.
    env = os.environ.copy()
    env["ANTHROPIC_BASE_URL"] = "https://new-gateway.example/cli"
    subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "seed-env.py"),
            str(seeded),
            str(SKILL_DIR / "ccsession.env.example"),
        ],
        env=env,
        check=True,
        capture_output=True,
    )
    refreshed = seeded.read_text()
    assert refreshed.count("\nexport ANTHROPIC_BASE_URL=") == 1
    assert "new-gateway.example" in refreshed


def test_seed_leaves_user_file_and_placeholders_alone(tmp_path: Path) -> None:
    edited = "export ANTHROPIC_BASE_URL=http://mine:4000/cli\n"
    assert (
        _seed(tmp_path, edited, "http://gateway.example:4000/cli").read_text() == edited
    )
    example = (SKILL_DIR / "ccsession.env.example").read_text()
    for bad in (
        "${ANTHROPIC_BASE_URL:-https://anthropic-base-url.coder-agent-env-injected.invalid}",
        "https://anthropic-base-url.coder-agent-env-injected.invalid",
        "",
    ):
        assert _seed(tmp_path, None, bad).read_text() == example


def test_seed_keeps_lines_added_after_seeding(tmp_path: Path) -> None:
    seeded = _seed(tmp_path, None, "http://gateway.example:4000/cli")
    edited = seeded.read_text() + "export ANTHROPIC_AUTH_TOKEN=user-added\n"
    seeded.write_text(edited)
    example = SKILL_DIR / "ccsession.env.example"
    for url in ("http://gateway.example:4000/cli", "https://new-gateway.example/cli"):
        env = os.environ.copy()
        env["ANTHROPIC_BASE_URL"] = url
        subprocess.run(
            [sys.executable, str(SKILL_DIR / "seed-env.py"), str(seeded), str(example)],
            env=env,
            check=True,
            capture_output=True,
        )
        assert seeded.read_text() == edited


def _key_env(tmp_path: Path, **values: str) -> dict[str, str]:
    fake = tmp_path / "claude-keys"
    fake.write_text(
        """#!/usr/bin/env python3
import json, os
print(json.dumps({k: bool(os.environ.get(k)) for k in
                  ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}))
"""
    )
    fake.chmod(0o700)
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "LITELLM_API_KEY")
    }
    env.update(
        {
            "HOME": str(tmp_path),
            "CLAUDE_BIN": str(fake),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
            **values,
        }
    )
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--profile", "claude"],
        env=env,
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_launch_maps_workspace_key_without_changing_explicit_auth(
    tmp_path: Path,
) -> None:
    assert _key_env(tmp_path, LITELLM_API_KEY="k") == {
        "ANTHROPIC_API_KEY": True,
        "ANTHROPIC_AUTH_TOKEN": False,
    }
    assert _key_env(tmp_path, ANTHROPIC_API_KEY="k", ANTHROPIC_AUTH_TOKEN="k") == {
        "ANTHROPIC_API_KEY": True,
        "ANTHROPIC_AUTH_TOKEN": False,
    }
    # A local setup that uses only the token, as the example file shows, is untouched.
    assert _key_env(tmp_path, ANTHROPIC_AUTH_TOKEN="t", LITELLM_API_KEY="k") == {
        "ANTHROPIC_API_KEY": False,
        "ANTHROPIC_AUTH_TOKEN": True,
    }


def test_shim_is_detected_without_lsof(tmp_path: Path) -> None:
    tools = tmp_path / "no-lsof-bin"
    tools.mkdir()
    first_source = tmp_path / "first-source"
    second_source = tmp_path / "second-source"
    first_source.mkdir()
    second_source.mkdir()
    basename = "ccsession-test-dangling-tool"
    (first_source / basename).symlink_to(tmp_path / "missing-tool")
    (second_source / basename).write_text("unused\n")
    for directory in (
        first_source,
        second_source,
        "/usr/local/bin",
        "/opt/homebrew/bin",
        "/usr/bin",
        "/bin",
        "/usr/sbin",
        "/sbin",
    ):
        base = Path(directory)
        if not base.is_dir():
            continue
        for tool in base.iterdir():
            link = tools / tool.name
            if tool.name != "lsof" and not link.exists() and not link.is_symlink():
                link.symlink_to(tool)
    dangling_link = tools / basename
    assert dangling_link.is_symlink()
    assert dangling_link.readlink() == first_source / basename
    assert not dangling_link.exists()
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    fake = tmp_path / "claude-shim"
    fake.write_text("#!/bin/sh\necho launched\n")
    fake.chmod(0o700)
    # A private copy of the shim gives cleanup an exact process to stop.
    shim_copy = tmp_path / "test-owned-shim.py"
    shim_copy.write_text((SKILL_DIR / "local-gateway-alias-proxy.py").read_text())
    home = tmp_path / "home"
    home.mkdir()
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "PATH": str(tools),
            "CLAUDE_BIN": str(fake),
            "ANTHROPIC_BASE_URL": "http://127.0.0.1:9/cli",
            "ANTHROPIC_AUTH_TOKEN": "t",
            "CC_SHIM_PORT": str(port),
            "CC_SHIM_SCRIPT": str(shim_copy),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
        }
    )
    command = [str(SKILL_DIR / "ccsession"), "--profile", "grok", "--shim"]
    try:
        first = subprocess.run(
            command,
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
            stdin=subprocess.DEVNULL,
        )
        assert first.returncode == 0, first.stderr
        assert "Starting model-alias shim" in first.stderr
        assert first.stdout == "launched\n"
        second = subprocess.run(
            command,
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
            stdin=subprocess.DEVNULL,
        )
        assert second.returncode == 0, second.stderr
        assert "already running" in second.stderr
        assert second.stdout == "launched\n"
    finally:
        subprocess.run(["pkill", "-f", str(shim_copy)], check=False)


def test_package_contains_no_personal_account_routing() -> None:
    for path in SKILL_DIR.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            text = path.read_text(errors="ignore").lower()
            for marker in (
                "chatgpt",
                "8417",
                "cliproxyapi",
                "ccsession-personal",
                "codex oauth",
            ):
                assert marker not in text, f"{marker} found in {path}"


def test_renamed_profiles_are_rejected(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    for profile in (
        "gpt1",
        "6sol",
        "6astra",
        "5.6sol",
        "6.1sol",
        "372k",
        "1mm",
        "500k",
    ):
        result = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--profile", profile],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 2
        assert f"unknown profile '{profile}'" in result.stderr


def test_profile_warms_complete_gateway_cache_before_claude_starts(
    tmp_path: Path,
) -> None:
    upstream = "http://gateway.example:4000/cli"

    class Shim(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/__ccsession_shim":
                payload = {
                    "service": "ccsession-gateway-alias-proxy",
                    "upstream": upstream,
                    "port": self.server.server_port,
                    "model_data": "t",
                    "tiers": {},
                    "show_all": False,
                    "settings": "e3b0c44298fc1c14",
                    "code": SHIM_CODE,
                }
            else:
                payload = {
                    "data": [
                        {
                            "id": "claude-gw-gpt-6-astra[1m]",
                            "display_name": "GPT 6 Astra",
                        },
                        {
                            "id": "claude-gw-qwen3.8-max[1m]",
                            "display_name": "Qwen 3.8 Max",
                        },
                    ]
                }
            body = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: object) -> None:
            pass

    shim = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Shim)
    thread = threading.Thread(target=shim.serve_forever, daemon=True)
    thread.start()

    home = tmp_path / "warm-home"
    home.mkdir()
    tools = tmp_path / "warm-tools"
    tools.mkdir()
    fake_lsof = tools / "lsof"
    fake_lsof.write_text("#!/bin/sh\nprintf '4242\\n'\n")
    fake_lsof.chmod(fake_lsof.stat().st_mode | stat.S_IXUSR)
    fake_claude = tmp_path / "cache-reader.py"
    fake_claude.write_text(
        """#!/usr/bin/env python3
import json, pathlib
cache = pathlib.Path.home() / ".claude/cache/gateway-models.json"
print(cache.read_text())
"""
    )
    fake_claude.chmod(fake_claude.stat().st_mode | stat.S_IXUSR)

    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "PATH": f"{tools}:{env['PATH']}",
            "CLAUDE_BIN": str(fake_claude),
            "ANTHROPIC_BASE_URL": upstream,
            "CC_SHIM_PORT": str(shim.server_port),
            "CC_SHIM_SCRIPT": str(SKILL_DIR / "local-gateway-alias-proxy.py"),
        }
    )
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--profile", "claude", "--shim"],
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        cache = json.loads(result.stdout.strip().splitlines()[-1])
        assert cache["baseUrl"] == f"http://127.0.0.1:{shim.server_port}"
        assert [model["id"] for model in cache["models"]] == [
            "claude-gw-gpt-6-astra[1m]",
            "claude-gw-qwen3.8-max[1m]",
        ]
    finally:
        shim.shutdown()
        shim.server_close()


def test_profile_keeps_same_shim_cache_when_warmup_fails(tmp_path: Path) -> None:
    upstream = "http://gateway.example:4000/cli"

    class Shim(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/__ccsession_shim":
                body = json.dumps(
                    {
                        "service": "ccsession-gateway-alias-proxy",
                        "upstream": upstream,
                        "port": self.server.server_port,
                        "model_data": "t",
                        "tiers": {},
                        "show_all": False,
                        "settings": "e3b0c44298fc1c14",
                        "code": SHIM_CODE,
                    }
                ).encode()
                self.send_response(200)
            else:
                body = b'{"error":"unavailable"}'
                self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: object) -> None:
            pass

    shim = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Shim)
    thread = threading.Thread(target=shim.serve_forever, daemon=True)
    thread.start()

    home = tmp_path / "failed-warmup-home"
    home.mkdir()
    cache_file = home / ".claude" / "cache" / "gateway-models.json"
    cache_file.parent.mkdir(parents=True)
    seeded_cache = json.dumps(
        {
            "baseUrl": f"http://127.0.0.1:{shim.server_port}",
            "fetchedAt": 1,
            "models": [{"id": "claude-gw-gpt-6-astra[1m]"}],
        },
        separators=(",", ":"),
    )
    cache_file.write_text(seeded_cache)
    tools = tmp_path / "failed-warmup-tools"
    tools.mkdir()
    fake_lsof = tools / "lsof"
    fake_lsof.write_text("#!/bin/sh\nprintf '4242\\n'\n")
    fake_lsof.chmod(fake_lsof.stat().st_mode | stat.S_IXUSR)
    fake_claude = tmp_path / "cache-reader.py"
    fake_claude.write_text(
        """#!/usr/bin/env python3
import pathlib
cache = pathlib.Path.home() / ".claude/cache/gateway-models.json"
print(cache.read_text())
"""
    )
    fake_claude.chmod(fake_claude.stat().st_mode | stat.S_IXUSR)

    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "PATH": f"{tools}:{env['PATH']}",
            "CLAUDE_BIN": str(fake_claude),
            "ANTHROPIC_BASE_URL": upstream,
            "CC_SHIM_PORT": str(shim.server_port),
            "CC_SHIM_SCRIPT": str(SKILL_DIR / "local-gateway-alias-proxy.py"),
        }
    )
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--profile", "claude", "--shim"],
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        assert result.stdout.strip().splitlines()[-1] == seeded_cache
        assert (
            "[ccsession] WARNING: could not pre-load gateway models; Claude Code will retry "
            "discovery after launch" in result.stderr
        )
    finally:
        shim.shutdown()
        shim.server_close()


def test_gateway_profile_requires_shim(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()
    env = os.environ.copy()
    env["HOME"] = str(home)
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--profile", "gpt"],
        env=env,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2
    assert "requires --shim" in result.stderr


def test_shim_refuses_an_unrelated_listener(tmp_path: Path) -> None:
    home = tmp_path / "unrelated-home"
    home.mkdir()
    fake_lsof = tmp_path / "unrelated-lsof"
    fake_lsof.write_text("#!/bin/sh\nprintf '4242\\n'\n")
    fake_lsof.chmod(fake_lsof.stat().st_mode | stat.S_IXUSR)
    fake_curl = tmp_path / "unrelated-curl"
    fake_curl.write_text('#!/bin/sh\nprintf \'{"service":"not-ccsession"}\'\n')
    fake_curl.chmod(fake_curl.stat().st_mode | stat.S_IXUSR)
    tools = tmp_path / "unrelated-tools"
    tools.mkdir()
    (tools / "lsof").symlink_to(fake_lsof)
    (tools / "curl").symlink_to(fake_curl)

    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "PATH": f"{tools}:{env['PATH']}",
            "ANTHROPIC_BASE_URL": "http://gateway.example:4000/cli",
            "CC_SHIM_PORT": "4555",
            "CC_SHIM_SCRIPT": str(SKILL_DIR / "local-gateway-alias-proxy.py"),
        }
    )
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--profile", "gpt", "--shim"],
        env=env,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 1
    assert "owned by another service" in result.stderr


def test_shim_curates_models_and_preserves_wire_aliases() -> None:
    module = runpy.run_path(
        str(SKILL_DIR / "local-gateway-alias-proxy.py"), run_name="shim_test"
    )
    payload = {
        "data": [
            {"id": "gpt-image-2.5-flare"},
            {"id": "gpt-5.6-sol"},
            {"id": "gpt-5.6-luna"},
            {"id": "gpt-5.6-terra"},
            {"id": "gpt-6-astra"},
            {"id": "gpt-6-sol"},
            {"id": "gpt-6-luna"},
            {"id": "gpt-image-2.5"},
            {"id": "kimi-k3"},
            {"id": "kimi-k2.8"},
            {"id": "kimi-k2.8-code"},
            {"id": "glm-5.2"},
            {"id": "glm-5.3"},
            {"id": "claude-opus-5"},
            {"id": "claude-opus-5-5"},
            {"id": "claude-fable-5-1"},
            {"id": "grok-4.7"},
            {"id": "grok-4.7-build-fast"},
            {"id": "grok-4.6"},
            {"id": "grok-imagine-image-2.0"},
            {"id": "muse-spark-1.2"},
            {"id": "muse-spark-1.3"},
            {"id": "muse-spark-1.1"},
            {"id": "muse-spark-1.2-contributor"},
            {"id": "muse-spark-1.3-contributor"},
            {"id": "muse-wonder-1.0"},
            {"id": "muse-wonder-full-1.0"},
            {"id": "muse-wonder-1.0-contributor"},
            {"id": "muse-wonder-full-1.0-contributor"},
            {"id": "Qwen/Qwen3-Max"},
            {"id": "Qwen3.8-max"},
            {"id": "gpt-image-2.5-sunburst"},
            {"id": "gpt-5.5"},
        ]
    }

    models = module["transform_models"](payload)["data"]
    ids = [model["id"] for model in models]
    aliases = module["alias_to_real"]

    # Exactly the allow list (picker.show), in its order, limited to models the
    # gateway lists (gpt-6.1-sol and claude-sonnet-5-5 are absent here).
    assert ids == [
        "claude-opus-5-5[1m]",
        "claude-gw-gpt-6-astra[1m]",
        "claude-gw-gpt-6-luna[1m]",
        "claude-gw-grok-4.7",
        "claude-gw-muse-wonder-full-1.0[1m]",
        "claude-gw-muse-wonder-1.0[1m]",
        "claude-gw-muse-spark-1.3[1m]",
        "claude-fable-5-1[1m]",
        "claude-gw-qwen3.8-max[1m]",
        "claude-gw-glm-5.3[1m]",
        "claude-gw-gpt-image-2.5-sunburst",
        "claude-gw-gpt-image-2.5",
        "claude-gw-gpt-image-2.5-flare",
        "claude-gw-grok-imagine-image-2.0",
    ]
    for hidden in (
        "claude-gw-gpt-6-sol[1m]",
        "claude-gw-gpt-5.6-sol[1m]",
        "claude-gw-gpt-5.6-luna[1m]",
        "claude-gw-gpt-5.6-terra[1m]",
        "claude-gw-muse-spark-1.2[1m]",
        "claude-gw-qwen-qwen3-max",
        "claude-opus-5",
        "claude-gw-gpt-5.5",
        "claude-gw-kimi-k3",
        "claude-gw-kimi-k2.8",
        "claude-gw-kimi-k2.8-code",
        "claude-gw-glm-5.2",
        "claude-gw-grok-4.6",
        "claude-gw-grok-4.7-build-fast",
        "claude-gw-muse-spark-1.1",
        "claude-gw-muse-spark-1.2-contributor",
        "claude-gw-muse-spark-1.3-contributor",
        "claude-gw-muse-wonder-1.0-contributor",
        "claude-gw-muse-wonder-full-1.0-contributor",
    ):
        assert hidden not in ids
    # Hidden models keep an alias, so /model or a resumed session still routes.
    assert aliases["claude-gw-gpt-6-astra"] == "gpt-6-astra"
    assert aliases["claude-gw-gpt-6-sol"] == "gpt-6-sol"
    assert aliases["claude-gw-gpt-6-luna"] == "gpt-6-luna"
    assert aliases["claude-gw-gpt-5.6-sol"] == "gpt-5.6-sol"
    assert aliases["claude-gw-muse-spark-1.3"] == "muse-spark-1.3"
    assert not any(alias.endswith("[1m]") for alias in aliases)


def test_shim_uses_a_local_placeholder_default() -> None:
    source = (SKILL_DIR / "local-gateway-alias-proxy.py").read_text()
    assert "GW_PROXY_UPSTREAM" in source
    assert '"http://127.0.0.1:4000/cli"' in source
    assert 'GW_PROXY_PORT="$CC_SHIM_PORT"' in (SKILL_DIR / "ccsession").read_text()


def test_shim_uses_custom_port_and_requests_uncompressed_models() -> None:
    class Upstream(http.server.BaseHTTPRequestHandler):
        seen_encoding = None

        def do_GET(self) -> None:
            type(self).seen_encoding = self.headers.get("Accept-Encoding")
            payload = json.dumps({"data": [{"id": "gpt-6-astra"}]}).encode()
            if type(self).seen_encoding != "identity":
                payload = gzip.compress(payload)
                self.send_response(200)
                self.send_header("Content-Encoding", "gzip")
            else:
                self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, _format: str, *_args: object) -> None:
            pass

    upstream = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Upstream)
    thread = threading.Thread(target=upstream.serve_forever, daemon=True)
    thread.start()
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        proxy_port = reservation.getsockname()[1]

    env = os.environ.copy()
    env.update(
        {
            "GW_PROXY_UPSTREAM": f"http://127.0.0.1:{upstream.server_port}",
            "GW_PROXY_PORT": str(proxy_port),
        }
    )
    proxy = subprocess.Popen(
        [sys.executable, str(SKILL_DIR / "local-gateway-alias-proxy.py")],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", proxy_port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.05)
        with urllib.request.urlopen(
            f"http://127.0.0.1:{proxy_port}/__ccsession_shim", timeout=5
        ) as response:
            health = json.loads(response.read())
        request = urllib.request.Request(
            f"http://127.0.0.1:{proxy_port}/v1/models",
            headers={"Accept-Encoding": "gzip"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            models = json.loads(response.read())["data"]
        assert health.pop("pid") == proxy.pid
        assert health.pop("active") == 0
        assert health == {
            "service": "ccsession-gateway-alias-proxy",
            "upstream": f"http://127.0.0.1:{upstream.server_port}",
            "port": proxy_port,
            "model_data": json.loads((SKILL_DIR / "ccsession-models.json").read_text())[
                "version"
            ],
            "settings": "e3b0c44298fc1c14",
            "code": SHIM_CODE,
            "show_all": False,
            "tier_mode": False,
            "tiers": {},
        }
        assert Upstream.seen_encoding == "identity"
        assert models[0]["id"] == "claude-gw-gpt-6-astra[1m]"
    finally:
        proxy.terminate()
        proxy.wait(timeout=5)
        upstream.shutdown()
        upstream.server_close()


def test_installer_wires_complete_package_without_overwriting_secrets(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    env = os.environ.copy()
    env["HOME"] = str(home)
    stale_plan = (
        home / ".claude" / "skills" / "ccsession-tag" / "PLAN-context-save-load.md"
    )
    stale_plan.parent.mkdir(parents=True)
    stale_plan.write_text("retired plan\n")

    first = subprocess.run(
        [str(SKILL_DIR / "install.sh")],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    target = home / ".claude" / "skills" / "ccsession-tag"
    env_file = home / ".claude" / "ccsession.env"
    settings_file = home / ".claude" / "settings.json"
    command_link = home / ".local" / "bin" / "ccsession"

    assert "Install complete" in first.stdout
    assert command_link.is_symlink()
    assert command_link.resolve() == target / "ccsession"
    orca_link = home / ".local" / "bin" / "ccsession-orca"
    assert orca_link.is_symlink()
    assert orca_link.resolve() == target / "ccsession-orca"
    assert os.access(orca_link, os.X_OK)
    assert (target / "local-gateway-alias-proxy.py").exists()
    assert (target / "SKILL.md").exists()
    assert not stale_plan.exists()
    assert stat.S_IMODE(env_file.stat().st_mode) == 0o600

    env_file.write_text("PRIVATE_SENTINEL\n")
    second = subprocess.run(
        [str(SKILL_DIR / "install.sh")],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "already exists (leaving untouched)" in second.stdout
    assert env_file.read_text() == "PRIVATE_SENTINEL\n"

    settings = json.loads(settings_file.read_text())
    hooks = settings["hooks"]["SessionStart"]
    matching = [
        hook
        for group in hooks
        for hook in group.get("hooks", [])
        if "ccsession-tag/hooks/session-start.sh" in hook.get("command", "")
    ]
    assert len(matching) == 1
    # /rename reaches ccsession's list through these, registered once each.
    for event in ("UserPromptSubmit", "SessionEnd"):
        commands = [
            hook["command"]
            for group in settings["hooks"][event]
            for hook in group.get("hooks", [])
        ]
        assert commands == [f'bash "{target}/hooks/session-name.sh"']
    assert os.access(target / "hooks" / "session-name.sh", os.X_OK)


def test_packaged_skill_installer_copies_the_shim(tmp_path: Path) -> None:
    from superclaude.cli.install_skill import install_skill_command

    target = tmp_path / "skills"
    success, message = install_skill_command("ccsession-tag", target, force=False)

    assert success, message
    installed = target / "ccsession-tag"
    assert (installed / "ccsession").exists()
    assert (installed / "local-gateway-alias-proxy.py").exists()
    assert not (installed / "PLAN-context-save-load.md").exists()


MODELS = SKILL_DIR / "models.py"


def _bundled() -> dict:
    return json.loads((SKILL_DIR / "ccsession-models.json").read_text())


def test_shipped_model_data_is_valid() -> None:
    """CI gate: a bad data file must never reach master, where every launch reads it."""
    module = runpy.run_path(str(MODELS), run_name="models_test")
    assert module["validate"](_bundled()) == ""


class _DataServer:
    """Serves model data with an ETag and honours If-None-Match like GitHub."""

    def __init__(self, payload: dict, delay: float = 0.0) -> None:
        self.payload = payload
        self.delay = delay
        self.statuses: list[int] = []
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                time.sleep(owner.delay)
                body = json.dumps(owner.payload).encode()
                etag = f'"{hash(body)}"'
                if self.headers.get("If-None-Match") == etag:
                    owner.statuses.append(304)
                    self.send_response(304)
                    self.end_headers()
                    return
                owner.statuses.append(200)
                self.send_response(200)
                self.send_header("ETag", etag)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args: object) -> None:
                pass

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/models.json"

    def close(self) -> None:
        self.server.shutdown()


def _models(tmp_path: Path, url: str, *args: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.update({"CCSESSION_MODELS_URL": url, "XDG_CACHE_HOME": str(tmp_path)})
    return subprocess.run(
        [sys.executable, str(MODELS), *args],
        env=env,
        text=True,
        capture_output=True,
        check=True,
        timeout=30,
    )


def test_refresh_downloads_then_uses_not_modified(tmp_path: Path) -> None:
    newer = _bundled()
    newer["version"] = "9999-01-01.1"
    newer["profiles"]["newone"] = dict(newer["profiles"]["claude"], aliases=[])
    newer["picker"]["show"] = newer["picker"]["show"][1:]
    server = _DataServer(newer)
    try:
        first = _models(tmp_path, server.url, "refresh")
        assert "model list updated to 9999-01-01.1" in first.stdout
        assert "+profile newone" in first.stdout
        second = _models(tmp_path, server.url, "refresh")
        assert second.stdout == ""
        assert server.statuses == [200, 304]
        resolved = _models(tmp_path, server.url, "resolve", "newone").stdout
        assert "PROFILE_MODEL=claude-opus-5-5[1m]" in resolved
    finally:
        server.close()


def test_refresh_rejects_bad_or_older_data(tmp_path: Path) -> None:
    bad = _bundled()
    bad["profiles"]["claude"]["model"] = "$(rm -rf ~)"
    server = _DataServer(bad)
    try:
        assert _models(tmp_path, server.url, "refresh").stdout == ""
        assert not (tmp_path / "ccsession" / "models.json").exists()
        older = _bundled()
        older["version"] = "2000-01-01.1"
        server.payload = older
        _models(tmp_path, server.url, "refresh")
        status = _models(tmp_path, server.url, "status").stdout
        assert f"{_bundled()['version']} (bundled)" in status
    finally:
        server.close()


def test_numeric_versions_win_and_rollbacks_keep_the_cache(tmp_path: Path) -> None:
    newest = _bundled()
    newest["version"] = "9999-01-01.10"
    server = _DataServer(newest)
    try:
        _models(tmp_path, server.url, "refresh")
        rollback = _bundled()
        rollback["version"] = "9999-01-01.9"
        server.payload = rollback
        _models(tmp_path, server.url, "refresh")
        status = _models(tmp_path, server.url, "status").stdout
        assert "9999-01-01.10 (downloaded)" in status
    finally:
        server.close()


def test_help_resolves_symlink_without_readlink_f(tmp_path: Path) -> None:
    """Older macOS readlink has no -f; the installer's symlink must still work."""
    fake_bin = tmp_path / "fakebin"
    fake_bin.mkdir()
    real = subprocess.run(
        ["sh", "-c", "command -v readlink"], text=True, capture_output=True, check=True
    ).stdout.strip()
    shim = fake_bin / "readlink"
    shim.write_text(f'#!/bin/sh\n[ "$1" = -f ] && exit 1\nexec {real} "$@"\n')
    shim.chmod(0o755)
    link_dir = tmp_path / "bin"
    link_dir.mkdir()
    (link_dir / "ccsession").symlink_to(SKILL_DIR / "ccsession")
    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
    help_text = subprocess.run(
        [str(link_dir / "ccsession"), "--help"],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    for name in _bundled()["profiles"]:
        assert f"--profile {name}" in help_text


def test_refresh_never_waits_past_its_limit(tmp_path: Path) -> None:
    server = _DataServer(_bundled(), delay=5)
    try:
        start = time.monotonic()
        _models(tmp_path, server.url, "refresh", "--wait", "1")
        assert time.monotonic() - start < 3
    finally:
        server.close()


def test_help_and_unknown_profile_list_data_profiles(tmp_path: Path) -> None:
    help_text = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--help"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    for name, profile in _bundled()["profiles"].items():
        flag = " --shim" if profile["requires_shim"] else ""
        assert f"--profile {name}{flag}\n" in help_text
        assert profile["label"] in help_text
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--profile", "nope"],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert "Valid profiles: " + ", ".join(_bundled()["profiles"]) in result.stderr


def _label_run(
    tmp_path: Path,
    transcript: bool,
    args: tuple[str, ...] = ("demo",),
    extra_env: dict[str, str] | None = None,
) -> tuple[subprocess.CompletedProcess[str], bool]:
    """Run ccsession on a saved label; return the finished process and whether the label stayed."""
    home = tmp_path / "home"
    work = tmp_path / "work"
    work.mkdir(parents=True)
    fake = tmp_path / "claude-args"
    fake.write_text(
        "#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n"
    )
    fake.chmod(0o700)
    projects = home / ".claude" / "projects"
    topics = projects / str(work.resolve()).replace("/", "-") / "topics"
    topics.mkdir(parents=True)
    (topics / "demo.txt").write_text("abc12345-0000-0000-0000-000000000000\n")
    if transcript:
        other = projects / "-some-project"
        other.mkdir()
        (other / "abc12345-0000-0000-0000-000000000000.jsonl").write_text("{}\n")
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "CLAUDE_BIN": str(fake),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
            **(extra_env or {}),
        }
    )
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        env=env,
        cwd=work,
        text=True,
        capture_output=True,
        check=True,
    )
    return result, (topics / "demo.txt").exists()


def _label_launch(
    tmp_path: Path,
    transcript: bool,
    args: tuple[str, ...] = ("demo",),
    extra_env: dict[str, str] | None = None,
) -> tuple[str, bool]:
    """Like _label_run, but only the standard output (Claude's last line is its JSON)."""
    result, label_kept = _label_run(tmp_path, transcript, args, extra_env)
    return result.stdout, label_kept


def _run_ccsession(
    tmp_path: Path, *args: str, **extra: str
) -> subprocess.CompletedProcess[str]:
    """Run ccsession without raising, and without any way to start a real Claude.

    The fake Claude only touches ``tmp_path / "claude-ran"``, so a test can tell
    whether the launcher got as far as starting it, also on a launcher that
    ignores the setting under test.
    """
    home = tmp_path / "home"
    work = tmp_path / "work"
    home.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    fake = tmp_path / "fake-claude"
    fake.write_text(f'#!/bin/sh\ntouch "{tmp_path / "claude-ran"}"\n')
    fake.chmod(0o700)
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("CC_CLAUDE_FLAGS", "CCSESSION_PERMISSIONS")
    }
    env.update(
        {
            "HOME": str(home),
            "CLAUDE_BIN": str(fake),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
            **extra,
        }
    )
    return subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        env=env,
        cwd=work,
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )


def test_rm_removes_an_existing_label_that_starts_with_a_dash(tmp_path: Path) -> None:
    # Older /ccsession-tag versions could write one; it must stay removable.
    home = tmp_path / "home"
    work = tmp_path / "work"
    work.mkdir(parents=True)
    topics = (
        home / ".claude" / "projects" / str(work.resolve()).replace("/", "-") / "topics"
    )
    topics.mkdir(parents=True)
    (topics / "-old.txt").write_text("abc12345-0000-0000-0000-000000000000\n")
    env = {**os.environ, "HOME": str(home)}
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--rm", "-old"],
        env=env,
        cwd=work,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert not (topics / "-old.txt").exists()


def test_label_with_missing_transcript_starts_new_session(tmp_path: Path) -> None:
    result, label_kept = _label_run(tmp_path, transcript=False)
    assert "has no saved conversation; starting a new one" in result.stderr
    assert "[ccsession]" not in result.stdout
    assert "--resume" not in json.loads(result.stdout.strip().splitlines()[-1])
    assert not label_kept


def test_label_with_saved_transcript_resumes(tmp_path: Path) -> None:
    stdout, label_kept = _label_launch(tmp_path, transcript=True)
    args = json.loads(stdout.strip().splitlines()[-1])
    assert args[-2:] == ["--resume", "abc12345-0000-0000-0000-000000000000"]
    assert label_kept


_LAUNCH_CASES = [
    (("-p", "x"), False),
    (("--profile", "claude", "-p", "x"), False),
    (("demo",), False),
    (("demo",), True),
    (("--profile", "claude", "demo"), False),
    (("--profile", "claude", "demo"), True),
]


@pytest.mark.parametrize(("args", "transcript"), _LAUNCH_CASES)
def test_every_launch_restores_grep_and_glob(
    tmp_path: Path, args: tuple[str, ...], transcript: bool, monkeypatch
) -> None:
    # On macOS, Linux, and WSL, Claude Code leaves Grep and Glob out by default;
    # naming either one in --allowedTools at launch brings both back, and the =
    # form keeps the flag to one argument.
    # The cases cover all six launch lines: untagged, new and resumed, each
    # with and without a profile model.
    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
    stdout, _ = _label_launch(tmp_path, transcript=transcript, args=args)
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[:2] == ["--dangerously-skip-permissions", "--allowedTools=Grep"]
    assert ("--model" in launched) == ("--profile" in args)
    assert ("--resume" in launched) == transcript


@pytest.mark.parametrize(("args", "transcript"), _LAUNCH_CASES)
def test_launch_status_lines_are_on_stderr_only(
    tmp_path: Path, args: tuple[str, ...], transcript: bool, monkeypatch
) -> None:
    # Issue 389: a scripted `claude` call must see only Claude's own output on
    # standard output. Here that is the stand-in's one JSON line; every
    # [ccsession] notice belongs on standard error.
    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
    result, _ = _label_run(tmp_path, transcript=transcript, args=args)
    assert len(result.stdout.strip().splitlines()) == 1, result.stdout
    assert "[ccsession]" not in result.stdout
    assert "[ccsession]" in result.stderr


# CCSESSION_PERMISSIONS=default (issue 390): the same six launch lines as above.
_BYPASS = "--dangerously-skip-permissions"
_PERMISSIONS_MATRIX = [
    (("-p", "x"), False),
    (("--profile", "claude", "-p", "x"), False),
    (("demo",), False),
    (("demo",), True),
    (("--profile", "claude", "demo"), False),
    (("--profile", "claude", "demo"), True),
]


@pytest.mark.parametrize(("args", "transcript"), _PERMISSIONS_MATRIX)
def test_permissions_default_drops_the_bypass_on_every_launch_line(
    tmp_path: Path, args: tuple[str, ...], transcript: bool
) -> None:
    # Only --allowedTools=Grep is added; the model and resume arguments stay.
    stdout, _ = _label_launch(
        tmp_path,
        transcript=transcript,
        args=args,
        extra_env={"CCSESSION_PERMISSIONS": "default"},
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[0] == "--allowedTools=Grep"
    assert _BYPASS not in launched
    assert ("--model" in launched) == ("--profile" in args)
    assert ("--resume" in launched) == transcript


def test_permissions_default_empty_value_is_unset(tmp_path: Path) -> None:
    stdout, _ = _label_launch(
        tmp_path,
        transcript=False,
        extra_env={"CCSESSION_PERMISSIONS": ""},
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[:2] == [_BYPASS, "--allowedTools=Grep"]


def test_permissions_default_non_empty_claude_flags_still_win(tmp_path: Path) -> None:
    stdout, _ = _label_launch(
        tmp_path,
        transcript=False,
        extra_env={"CCSESSION_PERMISSIONS": "default", "CC_CLAUDE_FLAGS": "--verbose"},
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[0] == "--verbose"
    assert _BYPASS not in launched
    assert "--allowedTools=Grep" not in launched


def test_permissions_default_empty_claude_flags_take_the_opt_in_default(
    tmp_path: Path,
) -> None:
    # An empty CC_CLAUDE_FLAGS is not special: the :- default applies, and with
    # the opt-in that default has no bypass flag.
    stdout, _ = _label_launch(
        tmp_path,
        transcript=False,
        extra_env={"CCSESSION_PERMISSIONS": "default", "CC_CLAUDE_FLAGS": ""},
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[0] == "--allowedTools=Grep"
    assert _BYPASS not in launched


def test_permissions_default_empty_claude_flags_without_it_take_the_old_default(
    tmp_path: Path,
) -> None:
    stdout, _ = _label_launch(
        tmp_path, transcript=False, extra_env={"CC_CLAUDE_FLAGS": ""}
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[:2] == [_BYPASS, "--allowedTools=Grep"]


def test_permissions_default_in_the_env_file_does_not_enable_it(tmp_path: Path) -> None:
    # The variable is read at the flag-default line, before the env file is sourced.
    env_file = tmp_path / "ccsession.env"
    env_file.write_text("export CCSESSION_PERMISSIONS=default\n")
    stdout, _ = _label_launch(
        tmp_path,
        transcript=False,
        extra_env={"CCSESSION_ENV_FILE": str(env_file)},
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[:2] == [_BYPASS, "--allowedTools=Grep"]


@pytest.mark.parametrize("shell_value", [None, "default"])
def test_permissions_in_the_env_file_never_reaches_a_nested_launch(
    tmp_path: Path, shell_value: str | None
) -> None:
    # Claude, and so a nested ccsession, must see what the shell set (or nothing),
    # never a value the env file exported after the flags were chosen.
    home = tmp_path / "home"
    work = tmp_path / "work"
    home.mkdir()
    work.mkdir()
    fake = tmp_path / "fake-claude"
    fake.write_text(
        "#!/usr/bin/env python3\nimport os\n"
        "print('PERM=' + repr(os.environ.get('CCSESSION_PERMISSIONS')))\n"
    )
    fake.chmod(0o700)
    env_file = tmp_path / "ccsession.env"
    env_file.write_text("export CCSESSION_PERMISSIONS=bogus\n")
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("CC_CLAUDE_FLAGS", "CCSESSION_PERMISSIONS")
    }
    env.update(HOME=str(home), CLAUDE_BIN=str(fake), CCSESSION_ENV_FILE=str(env_file))
    if shell_value is not None:
        env["CCSESSION_PERMISSIONS"] = shell_value
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "-p", "x"],
        env=env,
        cwd=work,
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert f"PERM={shell_value!r}" in result.stdout


def test_permissions_default_claude_flags_in_the_env_file_still_win(
    tmp_path: Path,
) -> None:
    env_file = tmp_path / "ccsession.env"
    env_file.write_text("CC_CLAUDE_FLAGS=--verbose\n")
    stdout, _ = _label_launch(
        tmp_path,
        transcript=False,
        extra_env={
            "CCSESSION_ENV_FILE": str(env_file),
            "CCSESSION_PERMISSIONS": "default",
        },
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[0] == "--verbose"
    assert _BYPASS not in launched


def test_permissions_default_keeps_a_flag_the_caller_passes(tmp_path: Path) -> None:
    # Only the flags ccsession adds change; Claude's own arguments pass through.
    stdout, _ = _label_launch(
        tmp_path,
        transcript=False,
        args=("demo", "--claude-args", _BYPASS),
        extra_env={"CCSESSION_PERMISSIONS": "default"},
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[0] == "--allowedTools=Grep"
    assert launched[-1] == _BYPASS


@pytest.mark.parametrize("value", ["bypass", "Default"])
def test_permissions_default_any_other_value_exits_2(
    tmp_path: Path, value: str
) -> None:
    result = _run_ccsession(tmp_path, "demo", CCSESSION_PERMISSIONS=value)
    assert result.returncode == 2
    assert "CCSESSION_PERMISSIONS" in result.stderr
    assert not (tmp_path / "claude-ran").exists()


def test_permissions_default_bad_value_also_stops_help(tmp_path: Path) -> None:
    # The check runs before the argument dispatch, so it covers every call.
    result = _run_ccsession(tmp_path, "--help", CCSESSION_PERMISSIONS="bypass")
    assert result.returncode == 2
    assert "CCSESSION_PERMISSIONS" in result.stderr


def test_permissions_default_help_lists_the_variable_and_stops_at_the_header(
    tmp_path: Path,
) -> None:
    result = _run_ccsession(tmp_path, "--help")
    assert result.returncode == 0
    assert "CCSESSION_PERMISSIONS=default" in result.stdout
    # show_help stops at the header comment; the code below it must not appear.
    assert "set -e" not in result.stdout
    assert "CLAUDE_BIN=" not in result.stdout


def test_private_addon_profiles_never_download_model_data(
    tmp_path: Path, monkeypatch
) -> None:
    server = _DataServer(_bundled())
    monkeypatch.setenv("CCSESSION_MODELS_REFRESH", "1")
    monkeypatch.setenv("CCSESSION_MODELS_URL", server.url)
    try:
        assert _addon_launch(tmp_path, "--profile", "local-test").returncode == 0
        assert server.statuses == []
        assert _addon_launch(tmp_path, "--profile", "claude").returncode == 0
        assert server.statuses == [200]
    finally:
        server.close()


def test_model_list_update_note_goes_to_stderr_at_launch(
    tmp_path: Path, monkeypatch
) -> None:
    newer = _bundled()
    newer["version"] = "9999-01-01.1"
    server = _DataServer(newer)
    monkeypatch.setenv("CCSESSION_MODELS_REFRESH", "1")
    monkeypatch.setenv("CCSESSION_MODELS_URL", server.url)
    try:
        result = _addon_launch(tmp_path, "--profile", "claude")
    finally:
        server.close()
    assert result.returncode == 0, result.stderr
    assert "model list updated to 9999-01-01.1" in result.stderr
    assert "model list updated" not in result.stdout


def test_refresh_models_report_stays_on_stdout(tmp_path: Path) -> None:
    # `ccsession --refresh-models` is a report the user asked for, so unlike a
    # launch notice it stays on standard output.
    server = _DataServer(_bundled())
    env = {
        **os.environ,
        "HOME": str(tmp_path),
        "XDG_CACHE_HOME": str(tmp_path),
        "CCSESSION_MODELS_URL": server.url,
    }
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--refresh-models"],
            env=env,
            cwd=tmp_path,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
    finally:
        server.close()
    assert result.returncode == 0, result.stderr
    assert "[ccsession] model data check:" in result.stdout
    assert "model data check" not in result.stderr


def test_claude_args_passes_the_rest_to_claude_unchanged(tmp_path: Path) -> None:
    # After --claude-args nothing is a label or a ccsession option, and the
    # marker itself is not passed on.
    stdout, _ = _label_launch(
        tmp_path,
        transcript=True,
        args=("demo", "--claude-args", "--shim", "--help", "x y"),
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[-5:] == [
        "--resume",
        "abc12345-0000-0000-0000-000000000000",
        "--shim",
        "--help",
        "x y",
    ]


def test_plain_double_dash_still_reaches_claude(tmp_path: Path) -> None:
    # Claude Code's own end-of-options marker keeps protecting a dash-led prompt.
    stdout, _ = _label_launch(
        tmp_path, transcript=True, args=("demo", "--", "-weird prompt")
    )
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[-2:] == ["--", "-weird prompt"]


def test_status_lines_in_launcher_scripts_go_to_stderr() -> None:
    # Issue 389. A launch test cannot reach the Reopening notices (terminal and
    # ORCA_PANE_KEY only) or the model cache print (needs a gateway), so read
    # the scripts themselves.
    for name in ("ccsession", "ccsession-orca"):
        for number, line in enumerate((SKILL_DIR / name).read_text().splitlines(), 1):
            if 'echo "[ccsession]' in line:
                assert ">&2" in line, (
                    f"{name}:{number} prints to stdout: {line.strip()}"
                )
    lines = (SKILL_DIR / "ccsession").read_text().splitlines()
    assert any(line.strip() == "python3 - >&2 <<'PY'" for line in lines), (
        "ccsession: the cache warm-up heredoc must start with python3 - >&2 <<'PY'"
    )
    refresh = [
        (number, line)
        for number, line in enumerate(lines, 1)
        if 'refresh --wait "${CCSESSION_MODELS_WAIT' in line
    ]
    assert len(refresh) == 1, refresh
    number, line = refresh[0]
    assert ">&2 || true" in line, f"ccsession:{number} refresh note goes to stdout"


# ccsession-orca: Orca's Claude command. Each launch runs the real wrapper and
# the real ccsession against a fake claude that records its argv and env, and a
# fake shim that ccsession reuses.
ORCA = SKILL_DIR / "ccsession-orca"
ORCA_QUESTION = (
    "Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s): "
)
# What ccsession --auto-name makes in the tests' working folder "work": the
# folder, up to four words of the task, then month-day, time with seconds and a
# random part.
AUTO_LABEL = re.compile(r"^work(-[a-z0-9]+)*-\d{4}-\d{6}-[0-9a-f]{4}$")
ORCA_FLAGS = ["--dangerously-skip-permissions", "--allowedTools=Grep"]
SESSION_ID = "abc12345-0000-0000-0000-000000000000"


def _orca_env(tmp_path: Path, **extra: str) -> dict[str, str]:
    tools = tmp_path / "tools"
    for directory in (tmp_path / "home", tmp_path / "work", tools):
        directory.mkdir(exist_ok=True)
    fake = tools / "claude-record"
    fake.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, sys, termios\n"
        "keys = ('ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN')\n"
        "try:\n"
        "    icanon = bool(termios.tcgetattr(0)[3] & termios.ICANON)\n"
        "except termios.error:\n"
        "    icanon = None  # stdin is not a terminal\n"
        "with open(os.environ['FAKE_CLAUDE_RECORD'], 'w') as f:\n"
        "    json.dump({'argv': sys.argv[1:], 'icanon': icanon,\n"
        "               'topic': os.environ.get('CLAUDE_TOPIC'),\n"
        "               'base_url': os.environ.get('ANTHROPIC_BASE_URL'),\n"
        "               'env_names': sorted(os.environ),\n"
        "               'set': {k: bool(os.environ.get(k)) for k in keys}}, f)\n"
    )
    fake.chmod(0o700)
    (tools / "lsof").write_text("#!/bin/sh\nprintf '4242\\n'\n")
    (tools / "lsof").chmod(0o700)
    env = {
        k: v
        for k, v in os.environ.items()
        if k
        not in (
            "ANTHROPIC_API_KEY",
            "ANTHROPIC_AUTH_TOKEN",
            "LITELLM_API_KEY",
            "CC_CLAUDE_FLAGS",
            "CCSESSION_PERMISSIONS",
            "CCSESSION_AUTOSTART",
            "CCSESSION_ASK_TIMEOUT",
            "CCSESSION_NAME",
            "CLAUDE_TOPIC",
        )
    }
    env.update(
        {
            "HOME": str(tmp_path / "home"),
            "PATH": f"{tools}:{env['PATH']}",
            "CLAUDE_BIN": str(fake),
            "FAKE_CLAUDE_RECORD": str(tmp_path / "record.json"),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
            "ANTHROPIC_BASE_URL": "http://gateway.example:4000/cli",
            "CC_SHIM_PORT": "4555",
            "CC_SHIM_SCRIPT": str(SKILL_DIR / "local-gateway-alias-proxy.py"),
            # Both carry the same key, as in a Coder workspace shell.
            "ANTHROPIC_API_KEY": "k",
            "ANTHROPIC_AUTH_TOKEN": "k",
            **extra,
        }
    )
    digest = subprocess.run(
        [sys.executable, str(MODELS), "settings-digest"],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    health = json.dumps(
        {
            "service": "ccsession-gateway-alias-proxy",
            "upstream": "http://gateway.example:4000/cli",
            "port": 4555,
            "model_data": "t",
            "tiers": {},
            "show_all": False,
            "settings": digest,
            "code": SHIM_CODE,
        }
    )
    (tools / "curl").write_text(f"#!/bin/sh\nprintf '%s\\n' '{health}'\n")
    (tools / "curl").chmod(0o700)
    return env


def _seed_label(tmp_path: Path, name: str) -> None:
    projects = tmp_path / "home" / ".claude" / "projects"
    work = (tmp_path / "work").resolve()
    topics = projects / str(work).replace("/", "-") / "topics"
    topics.mkdir(parents=True, exist_ok=True)
    (topics / f"{name}.txt").write_text(f"{SESSION_ID}\n")
    (topics.parent / f"{SESSION_ID}.jsonl").write_text("{}\n")


def _read_pty(fd: int, until: str | None = None, timeout: float = 60) -> str:
    """Read the terminal until the text appears, or until the program closes it."""
    out = b""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if until is not None and until.encode() in out:
            break
        if not select.select([fd], [], [], 0.2)[0]:
            continue
        try:
            chunk = os.read(fd, 4096)
        except OSError:  # Linux: EIO once every holder of the terminal is gone
            break
        if not chunk:
            break
        out += chunk
    return out.decode(errors="replace")


def _spawn_on_pty(
    command: list[str], env: dict[str, str], cwd: Path, typed_ahead: str = "", **io
) -> tuple[subprocess.Popen, int]:
    """Start a command whose controlling terminal is a fresh pseudo-terminal."""
    master, slave = pty.openpty()
    if typed_ahead:
        os.write(master, typed_ahead.encode())
    streams = {"stdin": slave, "stdout": slave, "stderr": slave, **io}
    proc = subprocess.Popen(
        command,
        env=env,
        cwd=cwd,
        start_new_session=True,
        # The terminal must be the controlling one, or Ctrl+C sends no SIGINT.
        preexec_fn=lambda: fcntl.ioctl(0, termios.TIOCSCTTY, 0),
        **streams,
    )
    os.close(slave)
    return proc, master


def _orca_tty(
    tmp_path: Path,
    *args: str,
    keys: str | None,
    env: dict[str, str] | None = None,
    typed_ahead: str = "",
) -> tuple[str, dict]:
    """Launch ccsession-orca on a terminal. keys=None: expect no question."""
    env = env or _orca_env(tmp_path)
    proc, master = _spawn_on_pty(
        [str(ORCA), *args], env, tmp_path / "work", typed_ahead
    )
    try:
        output = ""
        if keys is not None:
            output = _read_pty(master, until=ORCA_QUESTION)
            assert ORCA_QUESTION in output, output
            os.write(master, keys.encode())
        output += _read_pty(master)
        assert proc.wait(timeout=60) == 0, output
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    return output, json.loads((tmp_path / "record.json").read_text())


def _orca_no_tty(tmp_path: Path, *args: str, **extra: str) -> tuple[str, dict]:
    result = subprocess.run(
        [str(ORCA), *args],
        env=_orca_env(tmp_path, **extra),
        cwd=tmp_path / "work",
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=60,
        check=True,
    )
    return result.stdout + result.stderr, json.loads(
        (tmp_path / "record.json").read_text()
    )


def test_version_through_orca_keeps_stdout_clean(tmp_path: Path) -> None:
    """Issue 389: a scripted `claude --version` gets only Claude's own output.

    The status lines of ccsession go to standard error. Reading the streams
    apart (not through _orca_no_tty, which joins them) is the point of this test.
    """
    # A Coder workspace runs in tier mode, so its first status line names the
    # tier; give the scratch launch the same mode (a workspace env block with
    # one stand-in model per slot the bundled model data asks for).
    defaults = tmp_path / "defaults.sh"
    lines = ["export CCSESSION_DEFAULT_TIER=tier2"]
    for name, tier in models.load()[0]["tiers"].items():
        lines.append(f"export T{models.tier_number(name)}_WINDOW=500000")
        for slot in tier["models_env"]:
            lines.append(f"export {slot}=stand-in-{slot.lower()}")
            lines.append(f"export {slot}_WINDOW=500000")
    defaults.write_text("\n".join(lines) + "\n")
    env = _orca_env(tmp_path, AIDEV_AI_DEFAULTS_PATH=str(defaults))
    stand_in = tmp_path / "tools" / "claude-record"
    stand_in.write_text("#!/bin/sh\necho '2.1.318 (Claude Code)'\n")
    stand_in.chmod(0o700)
    result = subprocess.run(
        [str(ORCA), "--version"],
        env=env,
        cwd=tmp_path / "work",
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "2.1.318 (Claude Code)\n"
    assert "[ccsession] Starting untagged session" in result.stderr
    # superclaude eval reads the Claude version from this text.
    assert _parse_version(result.stdout + result.stderr) == (2, 1, 318)


def _assert_through_shim(record: dict) -> None:
    assert record["base_url"] == "http://127.0.0.1:4555"
    # One credential reaches Claude Code, never both.
    assert record["set"] == {"ANTHROPIC_API_KEY": False, "ANTHROPIC_AUTH_TOKEN": True}


def test_orca_name_starts_a_labeled_session_through_the_shim(tmp_path: Path) -> None:
    output, record = _orca_tty(tmp_path, keys="orca-demo\r")
    assert "Starting new session labeled 'orca-demo'" in output
    assert record["topic"] == "orca-demo"
    # The label is also Claude Code's name for the session.
    assert record["argv"] == [*ORCA_FLAGS, "--name", "orca-demo"]
    _assert_through_shim(record)


def _auto_label(record: dict) -> str:
    """The automatic name Claude was started with (--name <label>)."""
    argv = record["argv"]
    assert "--name" in argv, argv
    label = argv[argv.index("--name") + 1]
    assert AUTO_LABEL.match(label), label
    assert record["topic"] == label
    return label


def test_orca_saved_name_is_listed_and_resumes_at_the_question(
    tmp_path: Path,
) -> None:
    _seed_label(tmp_path, "demo")
    output, record = _orca_tty(tmp_path, keys="demo\r")
    assert "Saved sessions in" in output
    assert "demo" in output.split(ORCA_QUESTION)[0]
    assert record["topic"] == "demo"
    assert record["argv"] == [
        *ORCA_FLAGS,
        "--name",
        "demo",
        "--resume",
        SESSION_ID,
    ]


def test_orca_saved_name_in_ccsession_name_resumes_before_the_prompt(
    tmp_path: Path,
) -> None:
    # An explicit name is not asked about: it resumes the saved session of that
    # name, loudly, and the prompt still reaches Claude last.
    _seed_label(tmp_path, "demo")
    env = _orca_env(tmp_path, CCSESSION_NAME="demo")
    output, record = _orca_tty(tmp_path, "fix it", keys=None, env=env)
    assert "Session name" not in output
    assert "Resuming 'demo'" in output
    assert record["topic"] == "demo"
    assert record["argv"] == [
        *ORCA_FLAGS,
        "--name",
        "demo",
        "--resume",
        SESSION_ID,
        "fix it",
    ]
    assert "CCSESSION_NAME" not in record["env_names"]


def test_orca_claude_name_with_a_saved_label_passes_through_unchanged(
    tmp_path: Path,
) -> None:
    # A Claude --name in Orca's arguments is Claude's own: it is not read as a
    # ccsession name, so a saved label of the same name is not resumed, the
    # question is not asked, and the prompt stays last.
    _seed_label(tmp_path, "demo")
    output, record = _orca_tty(tmp_path, "--name", "demo", "fix it", keys=None)
    assert "Session name" not in output
    assert "Resuming" not in output
    assert "--resume" not in record["argv"]
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "--name", "demo", "fix it"]


def test_orca_enter_gets_an_auto_name(tmp_path: Path) -> None:
    output, record = _orca_tty(tmp_path, keys="\r")
    label = _auto_label(record)
    assert f"Starting new session labeled '{label}'" in output
    assert record["argv"] == [*ORCA_FLAGS, "--name", label]
    _assert_through_shim(record)
    # The question's default time limit is not left in Claude's environment.
    assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]


def test_orca_ctrl_c_cancels_without_starting_claude(tmp_path: Path) -> None:
    proc, master = _spawn_on_pty([str(ORCA)], _orca_env(tmp_path), tmp_path / "work")
    try:
        assert ORCA_QUESTION in _read_pty(master, until=ORCA_QUESTION)
        os.write(master, b"\x03")
        output = _read_pty(master)
        assert proc.wait(timeout=60) == 130, output
        assert termios.tcgetattr(master)[3] & termios.ICANON
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    assert "Starting" not in output
    assert not (tmp_path / "record.json").exists()


def _slow_probe(tmp_path: Path) -> None:
    # The keys-waiting probe runs while line mode is off; a python3 shim that
    # pauses before it leaves time to press Ctrl+C inside that window.
    real = subprocess.run(
        ["sh", "-c", "command -v python3"], capture_output=True, text=True
    ).stdout.strip()
    shim = tmp_path / "tools" / "python3"
    shim.write_text(
        f'#!/bin/sh\ncase "$*" in *select.select*) sleep 3 ;; esac\nexec {real} "$@"\n'
    )
    shim.chmod(0o700)


def test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal(
    tmp_path: Path,
) -> None:
    # A Ctrl+C before the question appears used to kill ccsession before it put
    # line mode back, and Claude then started on that terminal.
    env = _orca_env(tmp_path)
    _slow_probe(tmp_path)
    # No prompt argument: a launch with a task is never asked, so never probed.
    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
    try:
        time.sleep(1)
        os.write(master, b"\x03")
        output = _read_pty(master)
        # Ctrl+C cancels the launch (status 130); Claude is not started.
        assert proc.wait(timeout=60) == 130, output
        assert termios.tcgetattr(master)[3] & termios.ICANON
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    assert ORCA_QUESTION not in output
    # The probe was interrupted; its traceback must not reach the terminal.
    assert "KeyboardInterrupt" not in output
    assert not (tmp_path / "record.json").exists()


def test_ask_ctrl_c_while_line_mode_is_off_exits_130_and_restores(
    tmp_path: Path,
) -> None:
    env = _orca_env(tmp_path)
    _slow_probe(tmp_path)
    master, slave = pty.openpty()
    proc = subprocess.Popen(
        [str(SKILL_DIR / "ccsession"), "--ask"],
        env=env,
        cwd=tmp_path / "work",
        stdin=slave,
        stdout=subprocess.PIPE,
        stderr=slave,
        start_new_session=True,
        preexec_fn=lambda: fcntl.ioctl(0, termios.TIOCSCTTY, 0),
    )
    try:
        time.sleep(1)
        os.write(master, b"\x03")
        assert proc.communicate(timeout=30)[0] == b""
        assert proc.returncode == 130
        # The terminal outlives the process: line mode must be back on.
        assert termios.tcgetattr(slave)[3] & termios.ICANON
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(slave)
        os.close(master)


@pytest.mark.parametrize(
    "line",
    ["x" * 246, "あ" * 82, "foo\tbar", "\tfoo", "foo\t"],
    ids=["246 bytes", "82 CJK characters", "inner tab", "leading tab", "trailing tab"],
)
def test_orca_a_line_that_cannot_be_a_name_goes_to_claude_as_a_message(
    tmp_path: Path, line: str
) -> None:
    # A name too long for a file name (or holding a control character) can never
    # be saved, so it is not a name: it is the first message for Claude, and the
    # launch is auto-named. (One starting with "-" is fine as a name:
    # ccsession-orca passes it as --name.)
    output, record = _orca_tty(tmp_path, keys=line + "\r")
    assert "invalid label" not in output
    label = _auto_label(record)
    assert label != line
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, line]


@pytest.mark.parametrize(
    "args",
    [
        ("--resume", SESSION_ID),
        ("--resume", SESSION_ID, "--fork-session"),
        (f"--resume={SESSION_ID}",),
        ("--continue",),
        ("-r", SESSION_ID),
        ("--fork-session",),
        ("--from-pr", "12"),
    ],
    ids=[
        "resume",
        "resume-fork",
        "resume-equals",
        "continue",
        "resume-short",
        "fork-session-alone",
        "from-pr",
    ],
)
def test_orca_resume_skips_the_question(tmp_path: Path, args: tuple[str, ...]) -> None:
    _seed_label(tmp_path, "demo")
    output, record = _orca_tty(tmp_path, *args, keys=None)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, *args]
    _assert_through_shim(record)


@pytest.mark.parametrize(
    "prompt",
    [
        "fix the 'login' bug and say \"done\"",
        "-p looks like a flag",
        "--shim",
        "--help",
        "demo",
        "two words; $(not run) `either`",
    ],
)
def test_orca_prompt_reaches_claude_unchanged_and_is_never_a_label(
    tmp_path: Path, prompt: str
) -> None:
    # "demo" is a saved label: read as one, the launch would resume it.
    _seed_label(tmp_path, "demo")
    output, record = _orca_no_tty(tmp_path, prompt)
    assert "Resuming" not in output
    assert record["topic"] != "demo"
    assert "--resume" not in record["argv"]
    # The prompt is Claude's last argument, unchanged. A prompt that is itself
    # an option (--help) starts no session, so it gets no automatic name.
    assert record["argv"][-1] == prompt
    if prompt == "--help":
        assert record["argv"] == [*ORCA_FLAGS, prompt]
    else:
        label = record["argv"][record["argv"].index("--name") + 1]
        assert label.startswith("work-")
        assert record["topic"] == label


def test_orca_prefill_passes_through_and_its_text_is_not_a_flag(
    tmp_path: Path,
) -> None:
    # The prefill text "--resume" is input-box text, not a flag: the launch
    # carries a task (no question) and is auto-named, not treated as a resume.
    output, record = _orca_tty(tmp_path, "--prefill", "--resume", keys=None)
    assert "Session name" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "--prefill", "--resume"]
    output, record = _orca_no_tty(tmp_path, "--prefill", "draft 'text' here")
    label = _auto_label(record)
    assert record["argv"] == [
        *ORCA_FLAGS,
        "--name",
        label,
        "--prefill",
        "draft 'text' here",
    ]


def test_orca_without_a_terminal_never_asks(tmp_path: Path) -> None:
    output, record = _orca_no_tty(tmp_path, "hello")
    assert "Session name" not in output
    label = _auto_label(record)
    assert label.startswith("work-hello-")
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "hello"]
    _assert_through_shim(record)


def test_orca_autostart_off_never_asks(tmp_path: Path) -> None:
    env = _orca_env(tmp_path, CCSESSION_AUTOSTART="0")
    output, record = _orca_tty(tmp_path, "hello", keys=None, env=env)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "hello"]


def test_orca_unanswered_question_is_auto_named(tmp_path: Path) -> None:
    # Orca's supervised workers fail when Claude is not ready within 60s.
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="1")
    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
    try:
        shown = _read_pty(master, until="auto-named after 1s): ")
        assert "auto-named after 1s): " in shown
        output = _read_pty(master)
        assert proc.wait(timeout=60) == 0, output
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    record = json.loads((tmp_path / "record.json").read_text())
    label = _auto_label(record)
    assert f"Starting new session labeled '{label}'" in output
    assert record["argv"] == [*ORCA_FLAGS, "--name", label]
    assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]


def test_orca_keys_already_typed_skip_the_question(tmp_path: Path) -> None:
    # Something typing into the tab before the question would become the name:
    # it is left for Claude instead, and the launch is auto-named.
    output, record = _orca_tty(tmp_path, keys=None, typed_ahead="x")
    assert "Session name" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label]


# Reopening an Orca tab's own session when Orca relaunches the tab after a
# workspace restart (Coder #433). Orca then runs ccsession-orca again with only
# its default options, the same ORCA_PANE_KEY and a new ORCA_TERMINAL_HANDLE.
PANE = "tab-1:leaf-1"
OTHER_SESSION = "def67890-0000-0000-0000-000000000000"
ORCA_DEFAULT = "--dangerously-skip-permissions"


def _tab_env(
    tmp_path: Path, pane: str = PANE, handle: str = "term_after", **extra: str
) -> dict[str, str]:
    """ccsession-orca's environment in an Orca tab (a relaunch by default)."""
    return _orca_env(tmp_path, ORCA_PANE_KEY=pane, ORCA_TERMINAL_HANDLE=handle, **extra)


def _tab_runs(
    tmp_path: Path,
    session: str,
    pane: str = PANE,
    event: str = "SessionStart",
    handle: str = "term_before",
    launched: bool = True,
    nested: bool = False,
    **extra: str,
) -> None:
    """The hooks of the Claude Code ccsession launched in an Orca tab, reporting
    a session; the transcript is saved as Claude Code saves it."""
    env = _orca_env(tmp_path, ORCA_PANE_KEY=pane, ORCA_TERMINAL_HANDLE=handle, **extra)
    if launched:
        env["CCSESSION_LAUNCH_ID"] = f"{os.getpid()}.1"
    work = (tmp_path / "work").resolve()
    saved = tmp_path / "home" / ".claude" / "projects" / str(work).replace("/", "-")
    saved.mkdir(parents=True, exist_ok=True)
    (saved / f"{session}.jsonl").write_text("{}\n")
    _hook(env, work, session, event, nested=nested)


def _tab_records(tmp_path: Path) -> dict[str, list[str]]:
    tabs = tmp_path / "home" / ".local" / "state" / "ccsession" / "orca-tabs"
    if not tabs.is_dir():
        return {}
    # The lock and half-written files start with ".".
    return {
        f.name: f.read_text().splitlines()
        for f in tabs.iterdir()
        if f.is_file() and not f.name.startswith(".")
    }


def test_orca_relaunch_reopens_the_tabs_named_session(tmp_path: Path) -> None:
    _seed_label(tmp_path, "demo")
    _tab_runs(tmp_path, SESSION_ID)
    work = str((tmp_path / "work").resolve())
    assert _tab_records(tmp_path) == {"tab-1+leaf-1": [SESSION_ID, work, "term_before"]}
    output, record = _orca_tty(
        tmp_path, ORCA_DEFAULT, keys=None, env=_tab_env(tmp_path)
    )
    assert "Session name" not in output
    assert "Reopening this tab's session 'demo'" in output
    assert record["topic"] == "demo"
    assert record["argv"] == [
        *ORCA_FLAGS,
        "--name",
        "demo",
        "--resume",
        SESSION_ID,
        ORCA_DEFAULT,
    ]
    _assert_through_shim(record)
    # The launch tells the hooks its folder, for the next record.
    assert "CCSESSION_LAUNCH_CWD" in record["env_names"]


def test_orca_relaunch_reopens_an_untagged_session_by_id(tmp_path: Path) -> None:
    _tab_runs(tmp_path, SESSION_ID)
    output, record = _orca_tty(
        tmp_path, ORCA_DEFAULT, keys=None, env=_tab_env(tmp_path)
    )
    assert "Session name" not in output
    assert f"Reopening this tab's session {SESSION_ID[:8]}" in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, ORCA_DEFAULT, "--resume", SESSION_ID]


@pytest.mark.parametrize("named", [True, False], ids=["by name", "by id"])
def test_orca_reopen_leaves_the_name_and_the_limit_out_of_claudes_environment(
    tmp_path: Path, named: bool
) -> None:
    # An invalid CCSESSION_NAME is dropped, so it does not stop the reopen; it
    # and the question's time limit must not reach the Claude that is reopened.
    if named:
        _seed_label(tmp_path, "demo")
    _tab_runs(tmp_path, SESSION_ID)
    env = _tab_env(tmp_path, CCSESSION_NAME="bad\tname", CCSESSION_ASK_TIMEOUT="7")
    output, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys=None, env=env)
    assert "Reopening this tab's session" in output
    assert "CCSESSION_NAME" not in record["env_names"]
    assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]


@pytest.mark.parametrize(
    ("pane", "handle"),
    [("tab-2:leaf-1", "term_after"), (PANE, "term_before")],
    ids=["new tab", "same terminal, run again by hand"],
)
def test_orca_a_new_tab_or_a_rerun_is_still_asked(
    tmp_path: Path, pane: str, handle: str
) -> None:
    _seed_label(tmp_path, "demo")
    _tab_runs(tmp_path, SESSION_ID)
    env = _tab_env(tmp_path, pane=pane, handle=handle)
    output, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys="\r", env=env)
    assert "Reopening" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]


@pytest.mark.parametrize(
    ("args", "named"),
    [
        (("fix it",), True),
        (("--prefill", "draft"), True),
        (("--name", "other"), False),
        ((ORCA_DEFAULT, "-p"), False),
        (("--session-id", OTHER_SESSION), True),
    ],
    ids=["prompt", "prefill", "name", "print", "session-id"],
)
def test_orca_a_launch_with_more_than_options_is_not_asked_and_never_reopens(
    tmp_path: Path, args: tuple[str, ...], named: bool
) -> None:
    # A task or a name is carried, so there is no question; the tab's recorded
    # session is not reopened either. A task gets an automatic name; a Claude
    # --name or print mode passes through unchanged.
    _tab_runs(tmp_path, SESSION_ID)
    output, record = _orca_tty(tmp_path, *args, keys=None, env=_tab_env(tmp_path))
    assert "Reopening" not in output
    assert "Session name" not in output
    if named:
        label = _auto_label(record)
        assert record["argv"] == [*ORCA_FLAGS, "--name", label, *args]
    else:
        assert record["argv"] == [*ORCA_FLAGS, *args]
        assert record["topic"] is None


@pytest.mark.parametrize(
    "args",
    [("--resume", OTHER_SESSION), ("--continue",)],
    ids=["resume", "continue"],
)
def test_orca_a_session_choice_wins_over_the_tabs_record(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    _tab_runs(tmp_path, SESSION_ID)
    output, record = _orca_tty(tmp_path, *args, keys=None, env=_tab_env(tmp_path))
    assert "Reopening" not in output
    assert record["argv"] == [*ORCA_FLAGS, *args]


def test_orca_relaunch_without_a_terminal_or_autostart_changes_nothing(
    tmp_path: Path,
) -> None:
    _tab_runs(tmp_path, SESSION_ID)
    extra = {"ORCA_PANE_KEY": PANE, "ORCA_TERMINAL_HANDLE": "term_after"}
    output, record = _orca_no_tty(tmp_path, ORCA_DEFAULT, **extra)
    assert "Reopening" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]
    env = _tab_env(tmp_path, CCSESSION_AUTOSTART="0")
    output, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys=None, env=env)
    assert "Reopening" not in output
    assert record["argv"] == [*ORCA_FLAGS, ORCA_DEFAULT]


def test_orca_relaunch_whose_conversation_is_gone_is_asked(tmp_path: Path) -> None:
    _tab_runs(tmp_path, SESSION_ID)
    for transcript in (tmp_path / "home" / ".claude" / "projects").glob("*/*.jsonl"):
        transcript.unlink()
    output, record = _orca_tty(
        tmp_path, ORCA_DEFAULT, keys="\r", env=_tab_env(tmp_path)
    )
    assert "Reopening" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]


def test_orca_two_tabs_never_reopen_the_same_session(tmp_path: Path) -> None:
    _tab_runs(tmp_path, SESSION_ID)
    _tab_runs(tmp_path, OTHER_SESSION, pane="tab-3:leaf-1")
    # The first tab's session is opened in a second tab: it is that tab's now.
    _tab_runs(tmp_path, SESSION_ID, pane="tab-2:leaf-1", handle="term_two")
    records = _tab_records(tmp_path)
    assert sorted(records) == ["tab-2+leaf-1", "tab-3+leaf-1"]
    assert records["tab-2+leaf-1"][0] == SESSION_ID
    output, record = _orca_tty(
        tmp_path, ORCA_DEFAULT, keys="\r", env=_tab_env(tmp_path)
    )
    assert "Reopening" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]
    env = _tab_env(tmp_path, pane="tab-2:leaf-1")
    _, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys=None, env=env)
    assert record["argv"][-2:] == ["--resume", SESSION_ID]
    # A tab whose conversation is gone is forgotten at the next record.
    for transcript in (tmp_path / "home" / ".claude" / "projects").glob(
        f"*/{OTHER_SESSION}.jsonl"
    ):
        transcript.unlink()
    _tab_runs(tmp_path, SESSION_ID, pane="tab-2:leaf-1", handle="term_three")
    assert sorted(_tab_records(tmp_path)) == ["tab-2+leaf-1"]


def test_orca_clear_in_the_tab_moves_its_record_to_the_new_session(
    tmp_path: Path,
) -> None:
    _tab_runs(tmp_path, SESSION_ID)
    # /clear starts another session in the same Claude Code; its first prompt
    # reports it (SessionStart is registered for startup and resume only).
    _tab_runs(tmp_path, OTHER_SESSION, event="UserPromptSubmit")
    assert _tab_records(tmp_path)["tab-1+leaf-1"][0] == OTHER_SESSION
    _, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys=None, env=_tab_env(tmp_path))
    assert record["argv"][-2:] == ["--resume", OTHER_SESSION]


@pytest.mark.parametrize(
    ("launched", "nested"),
    [(False, False), (True, True)],
    ids=["claude not launched by ccsession", "claude inside the session"],
)
def test_orca_only_the_launched_claude_records_the_tab(
    tmp_path: Path, launched: bool, nested: bool
) -> None:
    _tab_runs(tmp_path, SESSION_ID, launched=launched, nested=nested)
    assert _tab_records(tmp_path) == {}


def test_orca_tab_record_follows_the_launch_folder_and_worktree(
    tmp_path: Path,
) -> None:
    # A tab reopens only a session it ran in its own worktree (the session list
    # is per worktree), and in the folder ccsession launched it in even when
    # Claude Code has moved since.
    main, worktree, projects, env = _named_repo(tmp_path)
    env.update({"ORCA_PANE_KEY": PANE, "ORCA_TERMINAL_HANDLE": "term_before"})
    _transcript(projects, main, SESSION_ID)
    hook_env = {
        **env,
        "CCSESSION_LAUNCH_ID": f"{os.getpid()}.1",
        "CCSESSION_LAUNCH_CWD": str(main.resolve()),
    }
    (main / "sub").mkdir()
    _hook(hook_env, main / "sub", SESSION_ID, "UserPromptSubmit", session_title="notes")
    relaunch = {**env, "ORCA_TERMINAL_HANDLE": "term_after"}
    assert _ccs(main, relaunch, "--orca-tab-reopen").stdout == f"{SESSION_ID}\tnotes\n"
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--orca-tab-reopen"],
        cwd=worktree,
        env=relaunch,
        capture_output=True,
        text=True,
    )
    assert (result.returncode, result.stdout) == (1, "")
    # Inside Claude Code (its Bash tool) the tab is never its own.
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--orca-tab-reopen"],
        cwd=main,
        env={**relaunch, "CLAUDECODE": "1"},
        capture_output=True,
        text=True,
    )
    assert (result.returncode, result.stdout) == (1, "")


def test_ask_prints_only_the_name_on_stdout(tmp_path: Path) -> None:
    env = _orca_env(tmp_path)
    _seed_label(tmp_path, "demo")
    command = [str(SKILL_DIR / "ccsession"), "--ask"]
    question = (
        "Session name (Enter = untagged, Ctrl+C = plain shell; gives up after 30s): "
    )
    proc, master = _spawn_on_pty(
        command, env, tmp_path / "work", stdout=subprocess.PIPE
    )
    try:
        shown = _read_pty(master, until=question)
        assert "Saved sessions in" in shown and "demo" in shown
        os.write(master, b"demo\r")
        assert proc.communicate(timeout=30)[0] == b"demo\n"
        assert proc.returncode == 0
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)

    proc, master = _spawn_on_pty(
        command, env, tmp_path / "work", stdout=subprocess.PIPE
    )
    try:
        _read_pty(master, until=question)
        os.write(master, b"\x03")
        assert proc.communicate(timeout=30)[0] == b""
        assert proc.returncode == 130
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)

    no_tty = subprocess.run(
        command, env=env, stdin=subprocess.DEVNULL, capture_output=True
    )
    assert (no_tty.returncode, no_tty.stdout) == (1, b"")


# ccsession --auto-name: the label for a launch that carries no name.
AUTO_STAMP = r"\d{4}-\d{6}-[0-9a-f]{4}"


def _auto_name(
    tmp_path: Path, text: str | None = None, cwd: Path | None = None, **extra: str
) -> subprocess.CompletedProcess:
    """Run `ccsession --auto-name [text]` in the test's work folder, no terminal."""
    command = [str(SKILL_DIR / "ccsession"), "--auto-name"]
    if text is not None:
        command.append(text)
    return subprocess.run(
        command,
        env=_orca_env(tmp_path, **extra),
        cwd=cwd or tmp_path / "work",
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_auto_name_without_text_is_the_folder_and_a_stamp(tmp_path: Path) -> None:
    result = _auto_name(tmp_path)
    assert result.returncode == 0, result.stderr
    assert re.fullmatch(rf"work-{AUTO_STAMP}\n", result.stdout), result.stdout


@pytest.mark.parametrize(
    "text",
    [
        "fix the 'login' bug and say \"done\"",
        "$(touch PWNED) `touch PWNED` ; touch PWNED",
        "../../etc/passwd",
        "\x1b[31mred\x1b[0m\x07 bell",
        "line one\nline two\n\tindented",
        "--model",
        "--claude-args",
        "--shim",
        "--tier=x",
        "--name",
        "あいう えお",
        "%2F %s %n",
        "!!!",
    ],
    ids=[
        "quotes",
        "command substitution",
        "path",
        "escape codes",
        "several lines",
        "--model",
        "--claude-args",
        "--shim",
        "--tier=x",
        "--name",
        "CJK",
        "format characters",
        "punctuation only",
    ],
)
def test_auto_name_is_valid_and_shell_safe_for_any_text(
    tmp_path: Path, text: str
) -> None:
    result = _auto_name(tmp_path, text)
    assert result.returncode == 0, result.stderr
    # One line, only a-z, 0-9 and hyphens (the folder here is lower case), and a
    # label ccsession itself accepts. Nothing in the text was run.
    assert re.fullmatch(rf"work(-[a-z0-9]+)*-{AUTO_STAMP}\n", result.stdout), (
        result.stdout
    )
    label = result.stdout.strip()
    check = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--check-name", label],
        env=_orca_env(tmp_path),
        stdin=subprocess.DEVNULL,
    )
    assert check.returncode == 0
    assert not (tmp_path / "work" / "PWNED").exists()


def test_auto_name_uses_at_most_four_words_of_twelve_characters(tmp_path: Path) -> None:
    result = _auto_name(
        tmp_path, "Alpha beta GAMMA delta epsilon abcdefghijklmnopqrstuvwxyz"
    )
    assert re.fullmatch(
        rf"work-alpha-beta-gamma-delta-{AUTO_STAMP}\n", result.stdout
    ), result.stdout
    result = _auto_name(tmp_path, "abcdefghijklmnopqrstuvwxyz")
    assert re.fullmatch(rf"work-abcdefghijkl-{AUTO_STAMP}\n", result.stdout), (
        result.stdout
    )


def test_auto_name_stays_short_and_keeps_its_stamp_for_a_long_folder(
    tmp_path: Path,
) -> None:
    folder = tmp_path / ("x" * 100)
    folder.mkdir()
    # Folder cut to 20 characters, four words of 12: 20 + 4 * 13 = 72 characters
    # before the stamp. Without the cut of the folder-and-words part to 59
    # characters the label would be 89 characters long; with it the fourth word
    # goes and the stamp stays.
    words = " ".join(["abcdefghijkl"] * 4 + ["z" * 400])
    result = _auto_name(tmp_path, words, cwd=folder)
    label = result.stdout.strip()
    assert len(label) <= 80, label
    assert re.fullmatch(rf"x{{20}}(-abcdefghijkl){{3}}-{AUTO_STAMP}", label), label


def test_auto_name_two_calls_in_the_same_second_differ(tmp_path: Path) -> None:
    # A clock that never moves: only the random part can tell the labels apart.
    _orca_env(tmp_path)
    fake_date = tmp_path / "tools" / "date"
    fake_date.write_text("#!/bin/sh\necho 0101-000000\n")
    fake_date.chmod(0o700)
    labels = {_auto_name(tmp_path, "same task").stdout for _ in range(3)}
    assert all(label.startswith("work-same-task-0101-000000-") for label in labels)
    # The random part differs (a 1 in 65536 chance for each pair to match).
    assert len(labels) >= 2


def test_auto_name_never_equals_a_saved_name(tmp_path: Path) -> None:
    # A saved name resumes its session, so an auto-name must be a new one: when
    # the label is taken it gets -2, then -3.
    stamp = "0101-000000-aaaa"
    base = f"work-same-task-{stamp}"
    _orca_env(tmp_path)
    _seed_label(tmp_path, base)
    result = _auto_name(tmp_path, "same task", CCSESSION_AUTO_NAME_STAMP=stamp)
    assert result.stdout == f"{base}-2\n"
    _seed_label(tmp_path, f"{base}-2")
    result = _auto_name(tmp_path, "same task", CCSESSION_AUTO_NAME_STAMP=stamp)
    assert result.stdout == f"{base}-3\n"
    # Another task, or no saved label, is not touched.
    assert (
        _auto_name(tmp_path, "other", CCSESSION_AUTO_NAME_STAMP=stamp).stdout
        == f"work-other-{stamp}\n"
    )


@pytest.mark.skipif(os.geteuid() == 0, reason="root can write to any folder")
def test_auto_name_prints_nothing_when_the_name_list_cannot_be_written(
    tmp_path: Path,
) -> None:
    # A launch under a label would stop at the save; with no label, the caller
    # starts Claude without a name instead.
    _orca_env(tmp_path)
    projects = tmp_path / "home" / ".claude" / "projects"
    projects.mkdir(parents=True)
    projects.chmod(0o500)
    try:
        result = _auto_name(tmp_path, "fix it")
    finally:
        projects.chmod(0o700)
    assert (result.returncode, result.stdout) == (1, "")


def test_auto_name_stamp_override_is_cut_to_safe_characters(tmp_path: Path) -> None:
    result = _auto_name(tmp_path, "x", CCSESSION_AUTO_NAME_STAMP="0101-000000-a b/c;d")
    assert result.stdout == "work-x-0101-000000-a-b-c-d\n"


def test_auto_name_in_a_hidden_folder_with_cjk_characters_is_still_valid(
    tmp_path: Path,
) -> None:
    folder = tmp_path / ".hidden-あいう"
    folder.mkdir()
    result = _auto_name(tmp_path, "task", cwd=folder)
    assert re.fullmatch(rf"hidden-task-{AUTO_STAMP}\n", result.stdout), result.stdout


def test_auto_name_check_name_judges_names_and_help_lists_the_new_options(
    tmp_path: Path,
) -> None:
    env = _orca_env(tmp_path)
    ccsession = str(SKILL_DIR / "ccsession")

    def check(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [ccsession, "--check-name", *args],
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
        )

    for good in ("demo", "my fix plan", "y" * 245):
        assert check(good).returncode == 0, good
    for bad in ("", "   ", "bad\tname", "two\nlines", "x" * 246, "あ" * 82):
        result = check(bad)
        # Only the status answers; nothing is printed.
        assert (result.returncode, result.stdout, result.stderr) == (1, "", ""), bad
    assert check().returncode == 1

    help_text = subprocess.run(
        [ccsession, "--help"],
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
    ).stdout
    for text in ("--auto-name", "--check-name", "@LIMIT@", "130 Ctrl+C"):
        assert text in help_text, text


# ccsession --ask on a terminal: the naming question and its exit codes.
def _ask_on_pty(
    tmp_path: Path,
    steps: list[tuple[float, bytes]],
    *args: str,
    env: dict[str, str] | None = None,
    typed_ahead: bytes = b"",
) -> tuple[int, bytes, str, bool, float]:
    """Run `ccsession --ask [hint]` on a terminal, then play the steps.

    Each step is (seconds to wait, bytes to type). Returns the exit status,
    what it printed on stdout, what the terminal showed, whether the terminal is
    back in line mode, and how long the run took.
    """
    env = env or _orca_env(tmp_path)
    started = time.monotonic()
    proc, master = _spawn_on_pty(
        [str(SKILL_DIR / "ccsession"), "--ask", *args],
        env,
        tmp_path / "work",
        typed_ahead.decode(),
        stdout=subprocess.PIPE,
    )
    try:
        shown = _read_pty(master, until="): ", timeout=15)
        for delay, data in steps:
            time.sleep(delay)
            os.write(master, data)
        stdout = proc.communicate(timeout=60)[0]
        shown += _read_pty(master, timeout=5)
        line_mode = bool(termios.tcgetattr(master)[3] & termios.ICANON)
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    return proc.returncode, stdout, shown, line_mode, time.monotonic() - started


def test_ask_default_limit_is_30_seconds_and_shown_in_the_question(
    tmp_path: Path,
) -> None:
    status, stdout, shown, line_mode, _ = _ask_on_pty(tmp_path, [(0.3, b"\x03")])
    assert "Enter = untagged, Ctrl+C = plain shell; gives up after 30s): " in shown
    assert (status, stdout) == (130, b"")
    assert line_mode


def test_ask_gives_up_after_the_limit_with_exit_1(tmp_path: Path) -> None:
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="1")
    status, stdout, shown, line_mode, seconds = _ask_on_pty(tmp_path, [], env=env)
    assert "gives up after 1s): " in shown
    assert (status, stdout) == (1, b"")
    assert line_mode
    assert seconds < 20


def test_ask_limit_0_waits_for_ever_and_drops_the_limit_from_the_question(
    tmp_path: Path,
) -> None:
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="0")
    status, stdout, shown, _, _ = _ask_on_pty(tmp_path, [(1.5, b"\x03")], env=env)
    assert "gives up" not in shown
    assert (status, stdout) == (130, b"")
    # Not a whole number of seconds (or only zeros): the same as no limit, not
    # a wait of no time at all.
    for value in ("soon", "1.5", "30s", "00"):
        env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT=value)
        status, stdout, shown, _, _ = _ask_on_pty(tmp_path, [(0.8, b"\x03")], env=env)
        assert "gives up" not in shown, value
        assert (status, stdout) == (130, b""), value


def test_ask_limit_starts_again_after_a_star(tmp_path: Path) -> None:
    # The limit is for each wait for a typed line: a "*" at 1.2 s of a 2 s limit
    # lists and asks again, so the question is still open at 2.4 s and gives up
    # about 2 s after the star, not 2 s after the start.
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="2")
    status, stdout, _, _, seconds = _ask_on_pty(tmp_path, [(1.2, b"*\r")], env=env)
    assert (status, stdout) == (1, b"")
    assert seconds >= 3.0


def test_ask_limit_with_leading_zeros_is_read_as_the_number(tmp_path: Path) -> None:
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="002")
    status, stdout, shown, _, seconds = _ask_on_pty(tmp_path, [], env=env)
    assert "gives up after 2s): " in shown
    assert (status, stdout) == (1, b"")
    assert 1 <= seconds < 20


def test_ask_end_of_input_exits_1(tmp_path: Path) -> None:
    # Ctrl+D on an empty line ends the input.
    status, stdout, _, line_mode, _ = _ask_on_pty(tmp_path, [(0.3, b"\x04")])
    assert (status, stdout) == (1, b"")
    assert line_mode


def test_ask_hint_placeholder_follows_the_limit(tmp_path: Path) -> None:
    hint = "Enter = auto-named; auto-named after @LIMIT@s"
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="2")
    _, _, shown, _, _ = _ask_on_pty(tmp_path, [(0.3, b"\x03")], hint, env=env)
    assert "Session name (Enter = auto-named; auto-named after 2s): " in shown
    # No limit: the part of the hint that names it goes, with its separator.
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="0")
    _, _, shown, _, _ = _ask_on_pty(tmp_path, [(0.3, b"\x03")], hint, env=env)
    assert "Session name (Enter = auto-named): " in shown
    assert "@LIMIT@" not in shown


def test_orca_ask_question_hint_follows_the_limit_and_the_timeout_auto_names(
    tmp_path: Path,
) -> None:
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="2")
    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
    try:
        shown = _read_pty(master, until="auto-named after 2s): ")
        assert (
            "Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 2s): "
            in shown
        )
        shown += _read_pty(master)
        assert proc.wait(timeout=60) == 0, shown
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    record = json.loads((tmp_path / "record.json").read_text())
    assert record["topic"] == _auto_label(record)
    assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]


@pytest.mark.parametrize(
    ("steps", "text"),
    [
        ([(0.2, b"x" * 246 + b"\r")], b"x" * 246),
        ([(0.2, "あ".encode() * 82 + b"\r")], "あ".encode() * 82),
        ([(0.2, b"foo\tbar\r")], b"foo\tbar"),
        ([(0.2, b"\tfoo\r")], b"\tfoo"),
        ([(0.2, b"foo\t\r")], b"foo\t"),
        ([(0.2, b"line one\rline two\r")], b"line one\nline two"),
        ([(0.2, b"line one\r"), (0.05, b"line two\r")], b"line one\nline two"),
    ],
    ids=[
        "246 bytes",
        "82 CJK characters",
        "inner tab",
        "leading tab",
        "trailing tab",
        "paste in one write",
        "paste in two writes",
    ],
)
def test_ask_a_line_that_cannot_be_a_name_exits_3_and_prints_it_as_typed(
    tmp_path: Path, steps: list[tuple[float, bytes]], text: bytes
) -> None:
    status, stdout, _, line_mode, _ = _ask_on_pty(tmp_path, steps)
    assert (status, stdout) == (3, text)
    assert line_mode


def test_ask_a_name_with_spaces_is_a_name(tmp_path: Path) -> None:
    status, stdout, _, _, _ = _ask_on_pty(tmp_path, [(0.2, b"my fix plan\r")])
    assert (status, stdout) == (0, b"my fix plan\n")
    # Surrounding spaces are not part of the name.
    status, stdout, _, _, _ = _ask_on_pty(tmp_path, [(0.2, b"  padded name  \r")])
    assert (status, stdout) == (0, b"padded name\n")
    # 245 bytes is the longest name.
    status, stdout, _, _, _ = _ask_on_pty(tmp_path, [(0.2, b"y" * 245 + b"\r")])
    assert (status, stdout) == (0, b"y" * 245 + b"\n")


def test_ask_a_blank_line_means_enter(tmp_path: Path) -> None:
    status, stdout, _, line_mode, _ = _ask_on_pty(tmp_path, [(0.2, b"\r")])
    assert (status, stdout) == (0, b"\n")
    assert line_mode
    # A line of only spaces or tabs is blank too, not a message with a tab in it.
    # So is a paste that starts with a blank line: the lines behind it stay in
    # the terminal and are not returned as text.
    for blank in (b"\t\r", b"   \r", b" \t \r", b"\rline two\rline three\r"):
        status, stdout, _, _, _ = _ask_on_pty(tmp_path, [(0.2, blank)])
        assert (status, stdout) == (0, b"\n"), blank


def test_ask_star_lists_the_saved_sessions_and_asks_again(tmp_path: Path) -> None:
    _orca_env(tmp_path)
    _seed_label(tmp_path, "demo")
    status, stdout, shown, _, _ = _ask_on_pty(
        tmp_path, [(0.2, b"*\r"), (0.5, b"after star\r")]
    )
    assert (status, stdout) == (0, b"after star\n")
    # Listed once with the question and once more for the star.
    assert shown.count("Saved sessions in") == 2


def test_ask_is_not_asked_when_keys_are_already_waiting(tmp_path: Path) -> None:
    # Typed ahead means someone is already at the keyboard with a task for Claude.
    status, stdout, shown, _, _ = _ask_on_pty(tmp_path, [], typed_ahead=b"x")
    assert (status, stdout) == (1, b"")
    assert "Session name" not in shown


def test_ask_ctrl_c_while_pasted_text_is_collected_exits_130_and_restores(
    tmp_path: Path,
) -> None:
    # After a line, --ask waits briefly for more pasted lines with line mode off;
    # Ctrl+C in that window must still end it with line mode back on.
    status, stdout, _, line_mode, _ = _ask_on_pty(
        tmp_path, [(0.2, b"some name\r"), (0.04, b"\x03")]
    )
    assert (status, stdout) == (130, b"")
    assert line_mode


def _title_launch(
    tmp_path: Path, *args: str, orca: bool = True
) -> tuple[bytes, dict[str, str]]:
    """Launch ccsession on a terminal; return its output and what Claude was given."""
    fake = tmp_path / "claude-title"
    fake.write_text(
        """#!/usr/bin/env python3
import json, os, sys
print(json.dumps({"disable": os.environ.get("CLAUDE_CODE_DISABLE_TERMINAL_TITLE", ""),
                  "resume": sys.argv[sys.argv.index("--resume") + 1]
                  if "--resume" in sys.argv else ""}))
"""
    )
    fake.chmod(0o700)
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("ORCA_PANE_KEY", "CLAUDE_CODE_DISABLE_TERMINAL_TITLE")
    }
    env.update(
        {
            "HOME": str(tmp_path),
            "CLAUDE_BIN": str(fake),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
        }
    )
    if orca:
        env["ORCA_PANE_KEY"] = "tab-1:leaf-1"
    master, slave = pty.openpty()
    try:
        subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--profile", "claude", *args],
            env=env,
            cwd=tmp_path,
            stdin=subprocess.DEVNULL,
            stdout=slave,
            stderr=subprocess.DEVNULL,
            check=True,
            timeout=60,
        )
    finally:
        os.close(slave)
    output = b""
    while True:
        try:
            chunk = os.read(master, 65536)
        except OSError:
            break
        if not chunk:
            break
        output += chunk
    os.close(master)
    # The title escape has no newline, so Claude's line follows it on the same line.
    last = output.decode().strip().splitlines()[-1]
    return output, json.loads(last[last.index("{") :])


# Every launch path this repo controls, run through ccsession-orca (the real
# wrapper and ccsession, a fake claude that records its arguments). Each test
# asserts whether the question is shown, the session's topic and the exact
# arguments Claude received.


@pytest.mark.parametrize("terminal", [True, False], ids=["terminal", "no-terminal"])
def test_orca_launch_with_a_prompt_is_auto_named_and_never_asked(
    tmp_path: Path, terminal: bool
) -> None:
    # An agent or worktree launch that carries its task.
    if terminal:
        output, record = _orca_tty(tmp_path, "fix the login bug", keys=None)
    else:
        output, record = _orca_no_tty(tmp_path, "fix the login bug")
    assert "Session name" not in output
    label = _auto_label(record)
    assert label.startswith("work-fix-the-login-bug-")
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "fix the login bug"]
    _assert_through_shim(record)


def test_orca_launch_with_nothing_and_no_terminal_is_auto_named(
    tmp_path: Path,
) -> None:
    # A worker start with neither a task nor a name, and nobody to ask.
    output, record = _orca_no_tty(tmp_path)
    assert "Session name" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label]


@pytest.mark.parametrize("terminal", [True, False], ids=["terminal", "no-terminal"])
@pytest.mark.parametrize("prompt", [None, "do the thing"], ids=["no-prompt", "prompt"])
def test_orca_ccsession_name_names_the_session_and_is_never_asked(
    tmp_path: Path, terminal: bool, prompt: str | None
) -> None:
    # A worker start that names its session in the environment.
    args = (prompt,) if prompt else ()
    env = _orca_env(tmp_path, CCSESSION_NAME="worker-7")
    if terminal:
        output, record = _orca_tty(tmp_path, *args, keys=None, env=env)
    else:
        output, record = _orca_no_tty(tmp_path, *args, CCSESSION_NAME="worker-7")
    assert "Session name" not in output
    assert record["topic"] == "worker-7"
    assert record["argv"] == [*ORCA_FLAGS, "--name", "worker-7", *args]
    assert "CCSESSION_NAME" not in record["env_names"]
    _assert_through_shim(record)


@pytest.mark.parametrize(
    ("args", "extra"),
    [
        (("-p", "hello"), {}),
        (("--version",), {}),
        (("mcp", "list"), {}),
        (("hi",), {"CCSESSION_AUTOSTART": "0"}),
    ],
    ids=["print mode", "--version", "subcommand", "autostart off"],
)
def test_orca_valid_ccsession_name_is_passed_even_where_a_launch_stays_untagged(
    tmp_path: Path, args: tuple[str, ...], extra: dict[str, str]
) -> None:
    # Without a name these launches start untagged; an explicit name wins.
    output, record = _orca_no_tty(tmp_path, *args, CCSESSION_NAME="worker-7", **extra)
    assert record["topic"] == "worker-7"
    assert record["argv"] == [*ORCA_FLAGS, "--name", "worker-7", *args]


@pytest.mark.parametrize(
    "bad",
    ["bad\tname", "x" * 300, "two\nlines", "   "],
    ids=["tab", "300 characters", "newline", "blank"],
)
def test_orca_invalid_ccsession_name_never_stops_claude(
    tmp_path: Path, bad: str
) -> None:
    # Dropped with a warning; the launch is then handled as if none was given.
    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME=bad)
    assert "CCSESSION_NAME is not a valid session name" in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "go"]
    assert "CCSESSION_NAME" not in record["env_names"]
    # With no task and a terminal, the question is asked after all.
    tmp2 = tmp_path / "again"
    tmp2.mkdir()
    env = _orca_env(tmp2, CCSESSION_NAME=bad)
    output, record = _orca_tty(tmp2, keys="\r", env=env)
    assert "CCSESSION_NAME is not a valid session name" in output
    assert record["argv"] == [*ORCA_FLAGS, "--name", _auto_label(record)]


def test_orca_ccsession_name_equal_to_a_saved_label_resumes_it_loudly(
    tmp_path: Path,
) -> None:
    _seed_label(tmp_path, "worker-7")
    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME="worker-7")
    assert "Resuming 'worker-7'" in output
    assert record["argv"] == [
        *ORCA_FLAGS,
        "--name",
        "worker-7",
        "--resume",
        SESSION_ID,
        "go",
    ]


def test_orca_ccsession_name_longer_than_the_limit_is_dropped_not_cut(
    tmp_path: Path,
) -> None:
    # 245 bytes is the longest name; one more is not shortened into a name.
    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME="n" * 245)
    assert record["topic"] == "n" * 245
    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME="n" * 246)
    assert record["topic"] != "n" * 246
    assert _auto_label(record)


@pytest.mark.parametrize(
    ("keys", "message", "separator"),
    [
        ("line one\rline two\r", "line one\nline two", False),
        ("- item one\r- item two\r", "- item one\n- item two", True),
        ("-starts with a dash and is too long " + "x" * 250 + "\r", None, True),
    ],
    ids=["paste", "dash-paste", "dash-too-long"],
)
def test_orca_typed_text_that_cannot_be_a_name_is_claudes_first_message(
    tmp_path: Path, keys: str, message: str | None, separator: bool
) -> None:
    message = message or keys.rstrip("\r")
    output, record = _orca_tty(tmp_path, keys=keys)
    label = _auto_label(record)
    tail = ["--", message] if separator else [message]
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, *tail]


@pytest.mark.parametrize(
    "args",
    [("-p", "hello"), ("--print", "hello"), ("-p",)],
    ids=["-p", "--print", "-p-only"],
)
def test_orca_print_mode_is_untagged_and_never_asked(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    output, record = _orca_tty(tmp_path, *args, keys=None)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, *args]
    output, record = _orca_no_tty(tmp_path, *args)
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, *args]


def test_orca_print_mode_permissions_default_keeps_shim_routing(
    tmp_path: Path,
) -> None:
    # The path the Coder wrapper uses: ccsession-orca -p ... hands off to
    # ccsession --shim. The opt-in drops only the bypass flag; the shim and its
    # credentials stay, and the variable stays exported to Claude (nested launches).
    _, control = _orca_no_tty(tmp_path, "-p", "hello")
    _, opted_in = _orca_no_tty(tmp_path, "-p", "hello", CCSESSION_PERMISSIONS="default")
    assert control["argv"] == [*ORCA_FLAGS, "-p", "hello"]
    assert opted_in["argv"] == ["--allowedTools=Grep", "-p", "hello"]
    _assert_through_shim(control)
    _assert_through_shim(opted_in)
    assert "CCSESSION_PERMISSIONS" in opted_in["env_names"]
    assert "CCSESSION_PERMISSIONS" not in control["env_names"]


@pytest.mark.parametrize(
    "args",
    [("--version",), ("-h",), ("mcp", "list"), ("doctor",)],
    ids=["version", "help", "mcp", "doctor"],
)
def test_orca_commands_that_start_no_session_get_no_name_and_no_question(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    output, record = _orca_tty(tmp_path, *args, keys=None)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, *args]


@pytest.mark.parametrize(
    "name_args",
    [("--name", "mine"), ("-n", "mine"), ("--name=mine",)],
    ids=["--name", "-n", "--name="],
)
def test_orca_claude_name_is_kept_once_and_never_asked(
    tmp_path: Path, name_args: tuple[str, ...]
) -> None:
    for terminal in (True, False):
        if terminal:
            output, record = _orca_tty(tmp_path, *name_args, "go", keys=None)
        else:
            output, record = _orca_no_tty(tmp_path, *name_args, "go")
        assert "Session name" not in output
        assert record["topic"] is None
        assert record["argv"] == [*ORCA_FLAGS, *name_args, "go"]
        # One --name for Claude, not a second one from ccsession.
        assert (
            sum(
                a in ("--name", "-n") or a.startswith("--name=") for a in record["argv"]
            )
            == 1
        )


@pytest.mark.parametrize(
    "args",
    [
        ("--prefill=hello world",),
        (f"--session-id={SESSION_ID}",),
        ("--some-new-option", "its value"),
    ],
    ids=["--prefill=", "--session-id=", "unknown option and its value"],
)
def test_orca_equals_forms_and_unknown_options_count_as_a_task(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    # The classification reads --prefill=<text> and --session-id=<id> as a task;
    # an option it does not know fails safe: its value is taken as the task.
    output, record = _orca_tty(tmp_path, *args, keys=None)
    assert "Session name" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, *args]


def test_orca_trailing_name_with_no_value_is_a_name_given(tmp_path: Path) -> None:
    output, record = _orca_tty(tmp_path, "--name", keys=None)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "--name"]


@pytest.mark.parametrize(
    "args",
    [
        ("--model", "opus"),
        ("--permission-mode", "plan"),
        ("--add-dir", "/tmp"),
        ("--allowedTools", "Bash"),
        ("--mcp-config", "servers.json"),
    ],
    ids=["--model", "--permission-mode", "--add-dir", "--allowedTools", "--mcp-config"],
)
def test_orca_the_value_of_a_known_option_is_not_a_task(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    # Only options: no task, no name, no resume, so the question is asked.
    output, record = _orca_tty(tmp_path, *args, keys="\r")
    assert ORCA_QUESTION in output
    label = _auto_label(record)
    assert record["argv"][-2:] == list(args)
    assert "--name" in record["argv"] and label


def test_orca_launch_in_a_hidden_folder_with_cjk_characters_reaches_claude(
    tmp_path: Path,
) -> None:
    # A leading dot and 4-byte-free CJK characters in the folder name must not
    # stop the launch; the automatic name is built from the cleaned folder name.
    folder = tmp_path / ".hidden-あいう"
    folder.mkdir()
    env = _orca_env(tmp_path)
    subprocess.run(
        [str(ORCA), "go"],
        env=env,
        cwd=folder,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    record = json.loads((tmp_path / "record.json").read_text())
    label = record["argv"][record["argv"].index("--name") + 1]
    assert re.fullmatch(rf"hidden-go-{AUTO_STAMP}", label), label
    assert record["argv"][-1] == "go"
    assert record["topic"] == label


def test_orca_typed_option_looking_text_at_the_question(tmp_path: Path) -> None:
    # A single typed word that looks like an option is a name, passed as --name
    # so Claude never reads it as an option.
    output, record = _orca_tty(tmp_path, keys="--version\r")
    assert record["topic"] == "--version"
    assert record["argv"] == [*ORCA_FLAGS, "--name", "--version"]
    # Pasted with a second line it is a message, after "--".
    tmp2 = tmp_path / "again"
    tmp2.mkdir()
    output, record = _orca_tty(tmp2, keys="--version\rsecond line\r")
    label = _auto_label(record)
    assert record["argv"] == [
        *ORCA_FLAGS,
        "--name",
        label,
        "--",
        "--version\nsecond line",
    ]


def test_orca_session_id_launch_carries_a_task_and_is_auto_named(
    tmp_path: Path,
) -> None:
    # --session-id starts a chosen new session: no question, but a name.
    sid = "11111111-2222-3333-4444-555555555555"
    output, record = _orca_tty(tmp_path, "--session-id", sid, keys=None)
    assert "Session name" not in output
    label = _auto_label(record)
    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "--session-id", sid]


def test_orca_autostart_off_with_no_task_is_untagged_and_never_asked(
    tmp_path: Path,
) -> None:
    env = _orca_env(tmp_path, CCSESSION_AUTOSTART="0")
    output, record = _orca_tty(tmp_path, keys=None, env=env)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == ORCA_FLAGS


@pytest.mark.skipif(os.geteuid() == 0, reason="root can write to any folder")
def test_orca_starts_untagged_when_the_name_list_cannot_be_written(
    tmp_path: Path,
) -> None:
    # No automatic name can be saved, so none is made: Claude still starts,
    # with the prompt and without a name, and nothing asks or fails.
    _orca_env(tmp_path)
    projects = tmp_path / "home" / ".claude" / "projects"
    projects.mkdir(parents=True)
    projects.chmod(0o500)
    try:
        output, record = _orca_tty(tmp_path, "fix it", keys=None)
    finally:
        projects.chmod(0o700)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "fix it"]


def test_orca_auto_named_session_is_listed_once_the_session_hook_records_it(
    tmp_path: Path,
) -> None:
    _, record = _orca_no_tty(tmp_path, "fix the login bug")
    label = _auto_label(record)
    env = _orca_env(tmp_path)
    work = (tmp_path / "work").resolve()
    projects = tmp_path / "home" / ".claude" / "projects"
    # The hook that Claude Code runs at session start saves the launch's name;
    # the topic Claude was started with is the one it saves.
    _hook(
        {**env, "CLAUDE_TOPIC": record["topic"], "CCSESSION_TOPIC_CWD": str(work)},
        work,
        SESSION_ID,
        "SessionStart",
    )
    _transcript(projects, work, SESSION_ID)
    assert _listed(work, env, "--here") == {label: SESSION_ID[:8]}


def test_orca_terminal_title_keeps_claude_recognisable(tmp_path: Path) -> None:
    # Untagged: plain "Claude Code", and Claude Code must not overwrite it.
    output, claude = _title_launch(tmp_path)
    assert b"\x1b]0;Claude Code\x07" in output
    assert claude == {"disable": "1", "resume": ""}

    # A new labelled session carries its label.
    output, claude = _title_launch(tmp_path, "demo")
    assert "\x1b]0;demo · Claude Code\x07".encode() in output
    assert claude == {"disable": "1", "resume": ""}

    # Resuming by label: the case Orca dropped at once (Claude's title is its AI name).
    topics = (
        tmp_path / ".claude" / "projects" / str(tmp_path).replace("/", "-") / "topics"
    )
    (topics / "demo.txt").write_text("session-1\n")
    (topics.parent / "session-1.jsonl").write_text("{}\n")
    output, claude = _title_launch(tmp_path, "demo")
    assert "\x1b]0;demo · Claude Code\x07".encode() in output
    assert claude == {"disable": "1", "resume": "session-1"}


def test_title_untouched_outside_orca(tmp_path: Path) -> None:
    output, claude = _title_launch(tmp_path, "demo", orca=False)
    assert b"\x1b]0;" not in output
    assert claude == {"disable": "", "resume": ""}


# Session names belong to the repo, not the folder: every worktree, branch and
# copy of a repo shares one name list under ~/.claude/projects/<key>/topics.


def _git_env(home: Path) -> dict[str, str]:
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("GIT_")
        and k not in ("CLAUDE_TOPIC", "CCSESSION_TOPIC_CWD", "CLAUDE_ENV_FILE")
    }
    env["HOME"] = str(home)
    return env


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
        cwd=cwd,
        env=_git_env(cwd),
        check=True,
        capture_output=True,
    )


def _repo_with_worktree(tmp_path: Path, origin: str | None) -> tuple[Path, Path]:
    main = tmp_path / "repo"
    main.mkdir()
    _git(main, "init", "-q")
    if origin:
        _git(main, "remote", "add", "origin", origin)
    _git(main, "commit", "-q", "--allow-empty", "-m", "init")
    worktree = tmp_path / "wt-feature"
    _git(main, "worktree", "add", "-q", "-b", "feature", str(worktree))
    return main, worktree


def _name_key(cwd: Path, home: Path) -> str:
    return subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--key"],
        cwd=cwd,
        env=_git_env(home),
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


@pytest.mark.parametrize(
    "origin",
    [
        "https://github.com/Org/Repo",
        "https://github.com/Org/Repo.git",
        "https://github.com/Org/Repo/",
        "https://user:REDACTED@github.com/Org/Repo.git",  # pragma: allowlist secret
        "git@github.com:Org/Repo.git",
        "ssh://git@github.com/Org/Repo.git",
    ],
)
def test_name_key_is_the_repo_origin_in_every_worktree(
    tmp_path: Path, origin: str
) -> None:
    main, worktree = _repo_with_worktree(tmp_path, origin)
    (main / "sub").mkdir()
    home = tmp_path / "home"
    keys = {_name_key(folder, home) for folder in (main, worktree, main / "sub")}
    # Same slug function as before (/ becomes -); credentials never kept.
    assert keys == {"github.com-Org-Repo"}


def test_name_key_without_origin_is_the_main_worktree(tmp_path: Path) -> None:
    main, worktree = _repo_with_worktree(tmp_path, origin=None)
    home = tmp_path / "home"
    expected = str(main.resolve()).replace("/", "-")
    assert _name_key(main, home) == expected
    assert _name_key(worktree, home) == expected


def test_name_key_with_a_separate_git_dir_is_that_git_dir(tmp_path: Path) -> None:
    # git records no main checkout for --separate-git-dir, so the shared git
    # folder is the key: the checkout, its subfolders and worktrees agree.
    meta = tmp_path / "meta"
    meta.mkdir()
    main = tmp_path / "repo"
    _git(tmp_path, "init", "-q", f"--separate-git-dir={meta / 'repo'}", str(main))
    _git(main, "commit", "-q", "--allow-empty", "-m", "init")
    worktree = tmp_path / "wt"
    _git(main, "worktree", "add", "-q", "-b", "feature", str(worktree))
    (main / "sub").mkdir()
    home = tmp_path / "home"
    keys = {_name_key(folder, home) for folder in (main, main / "sub", worktree)}
    assert keys == {str((meta / "repo").resolve()).replace("/", "-")}


def test_name_key_outside_git_is_the_folder_as_before(tmp_path: Path) -> None:
    folder = tmp_path / "plain"
    folder.mkdir()
    assert _name_key(folder, tmp_path / "home") == str(folder).replace("/", "-")


def test_name_from_one_worktree_resumes_in_another(tmp_path: Path) -> None:
    main, worktree = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    home = tmp_path / "home"
    session = "abc12345-0000-0000-0000-000000000000"
    projects = home / ".claude" / "projects"
    topics = projects / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True)
    (topics / "demo.txt").write_text(f"{session}\n")
    # Claude Code saved the conversation under the folder it ran in.
    started = projects / str(worktree).replace("/", "-")
    started.mkdir()
    (started / f"{session}.jsonl").write_text("{}\n")
    fake = tmp_path / "claude-args"
    fake.write_text(
        "#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n"
    )
    fake.chmod(0o700)
    env = _git_env(home)
    env.update(
        {"CLAUDE_BIN": str(fake), "CCSESSION_ENV_FILE": str(tmp_path / "none.env")}
    )
    for folder in (main, worktree):
        result = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "demo"],
            cwd=folder,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        launched = json.loads(result.stdout.strip().splitlines()[-1])
        assert launched[-2:] == ["--resume", session]
        here = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--here"],
            cwd=folder,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        # The listing finds the conversation under the folder it ran in.
        line = next(ln for ln in here.stdout.splitlines() if "demo" in ln)
        assert "transcript missing" not in line


def test_session_start_hook_saves_the_name_under_the_repo(tmp_path: Path) -> None:
    _, worktree = _repo_with_worktree(tmp_path, "git@github.com:Org/Repo.git")
    home = tmp_path / "home"
    env = _git_env(home)
    env["CLAUDE_TOPIC"] = "demo"
    env.pop("CLAUDE_ENV_FILE", None)
    payload = json.dumps({"session_id": "sid-1", "cwd": str(worktree)})
    subprocess.run(
        ["bash", str(SKILL_DIR / "hooks" / "session-start.sh")],
        input=payload,
        env=env,
        text=True,
        check=True,
    )
    topics = home / ".claude" / "projects" / "github.com-Org-Repo" / "topics"
    assert (topics / "demo.txt").read_text().strip() == "sid-1"
    assert (topics / ".cwd").read_text().strip() == str(worktree)


def test_retired_ccsession_tag_command_can_not_run() -> None:
    # /rename names a session now. SKILL.md stays only so the folder installs:
    # neither a person (/ccsession-tag) nor Claude can run it.
    front = (SKILL_DIR / "SKILL.md").read_text().split("---")[1]
    fields = dict(
        line.split(":", 1) for line in front.strip().splitlines() if ":" in line
    )
    assert fields["user-invocable"].strip() == "false"
    assert fields["disable-model-invocation"].strip() == "true"
    assert "```bash" not in (SKILL_DIR / "SKILL.md").read_text()


def test_names_saved_per_folder_move_to_the_repo_once(tmp_path: Path) -> None:
    main, worktree = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    home = tmp_path / "home"
    projects = home / ".claude" / "projects"

    def old_list(folder: Path, names: dict[str, str]) -> Path:
        topics = projects / str(folder).replace("/", "-") / "topics"
        topics.mkdir(parents=True)
        (topics / ".cwd").write_text(f"{folder}\n")
        for name, session in names.items():
            (topics / f"{name}.txt").write_text(f"{session}\n")
        return topics

    main_list = old_list(main, {"alpha": "s-a", "shared": "s-main"})
    wt_list = old_list(worktree, {"beta": "s-b", "shared": "s-wt"})
    # The worktree was used last, so it keeps the plain name "shared".
    os.utime(main_list / ".cwd", (1_000_000_000, 1_000_000_000))
    # A list whose folder no longer exists is left where it is.
    gone_list = old_list(tmp_path / "deleted-folder", {"gamma": "s-g"})
    env = _git_env(home)

    def ccsession(*args: str, cwd: Path = worktree) -> str:
        return subprocess.run(
            [str(SKILL_DIR / "ccsession"), *args],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        ).stdout

    here = ccsession("--here")
    repo = projects / "github.com-Org-Repo" / "topics"
    moved = {p.stem: p.read_text().strip() for p in repo.glob("*.txt")}
    # Copies only; the other session with a taken name stays reachable under
    # <name>-<folder>.
    assert moved == {
        "alpha": "s-a",
        "beta": "s-b",
        "shared": "s-wt",
        "shared-repo": "s-main",
    }
    for name in ("alpha", "beta", "shared-repo"):
        assert name in here
    assert (main_list / "alpha.txt").exists() and (wt_list / "beta.txt").exists()
    assert (gone_list / "gamma.txt").exists() and "gamma" not in moved
    assert (projects / ".ccsession-names-by-repo").exists()
    # The copied per-folder lists no longer show up as duplicates in --list.
    assert ccsession("--list").count("alpha") == 1

    # Each old list is copied once: a removed name stays removed and a later
    # file in an old list is not picked up, however often installs re-run it.
    assert "Removed label" in ccsession("--rm", "alpha", cwd=main)
    (main_list / "late.txt").write_text("s-late\n")
    for _ in range(2):
        ccsession("--migrate-names")
    after = {p.stem: p.read_text().strip() for p in repo.glob("*.txt")}
    assert after == {k: v for k, v in moved.items() if k != "alpha"}


def test_migration_never_overwrites_a_label_written_meanwhile(tmp_path: Path) -> None:
    # A cp shim plays the SessionStart hook: just before migration's copy runs,
    # it saves a newer label under the same name in the repo's list.
    main, _ = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    home = tmp_path / "home"
    projects = home / ".claude" / "projects"
    old = projects / str(main).replace("/", "-") / "topics"
    old.mkdir(parents=True)
    (old / ".cwd").write_text(f"{main}\n")
    (old / "name.txt").write_text("s-legacy\n")
    repo = projects / "github.com-Org-Repo" / "topics"
    shim = tmp_path / "bin"
    shim.mkdir()
    (shim / "cp").write_text(
        "#!/bin/bash\n"
        '[ -e "$RACE_DEST" ] || { mkdir -p "${RACE_DEST%/*}"; '
        'echo s-newer > "$RACE_DEST"; }\n'
        f'exec {shutil.which("cp")} "$@"\n'
    )
    (shim / "cp").chmod(0o755)
    env = _git_env(home)
    env["PATH"] = f"{shim}:{env['PATH']}"
    env["RACE_DEST"] = str(repo / "name.txt")
    subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--migrate-names"],
        cwd=main,
        env=env,
        check=True,
        capture_output=True,
    )
    labels = {p.name: p.read_text() for p in repo.glob("*.txt")}
    assert labels == {"name.txt": "s-newer\n", "name-repo.txt": "s-legacy\n"}
    assert not list(repo.glob(".ccsession-copy.*"))


def test_migration_keeps_going_past_an_unreadable_list(tmp_path: Path) -> None:
    main, _ = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    home = tmp_path / "home"
    projects = home / ".claude" / "projects"
    bad = projects / "-a-bad" / "topics"
    bad.mkdir(parents=True)
    (bad / ".cwd").write_text(f"{main}\n")
    (bad / ".cwd").chmod(0)
    good = projects / str(main).replace("/", "-") / "topics"
    good.mkdir(parents=True)
    (good / ".cwd").write_text(f"{main}\n")
    (good / "keep.txt").write_text("s-keep\n")
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--migrate-names"],
        env=_git_env(home),
        capture_output=True,
    )
    (bad / ".cwd").chmod(0o600)
    repo = projects / "github.com-Org-Repo" / "topics"
    assert (repo / "keep.txt").read_text() == "s-keep\n"
    if os.geteuid() != 0:  # root can read the file anyway
        # Reported, and left unmarked so the next install retries that list;
        # everyday launches stop rescanning (the done marker is written).
        assert result.returncode != 0
        assert not (bad / ".ccsession-moved-to-repo").exists()
    assert (projects / ".ccsession-names-by-repo").exists()


def test_migration_never_hides_a_repo_list_whose_last_folder_moved_on(
    tmp_path: Path,
) -> None:
    # A repo list's .cwd is just the folder last used. If that folder's origin
    # changes, the list must stay visible to the repo's other clones.
    home = tmp_path / "home"
    clones = []
    for name in ("a", "b"):
        clone = tmp_path / name
        clone.mkdir()
        _git(clone, "init", "-q")
        _git(clone, "remote", "add", "origin", "git@github.com:Org/Repo.git")
        clones.append(clone)
    topics = home / ".claude" / "projects" / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True)
    (topics / ".cwd").write_text(f"{clones[0]}\n")
    (topics / "notes.txt").write_text("s-notes\n")
    _git(clones[0], "remote", "set-url", "origin", "git@github.com:Me/Fork.git")
    env = _git_env(home)
    subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--migrate-names"], env=env, check=True
    )
    here = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--here"],
        cwd=clones[1],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    assert "notes" in here
    assert not (topics / ".ccsession-moved-to-repo").exists()
    assert not (home / ".claude" / "projects" / "github.com-Me-Fork").exists()


@pytest.mark.parametrize(
    "origin",
    [
        ".",
        "..",
        "../Repo.git",
        "/srv/repos/Repo",
        "file:///srv/repos/Repo",
        "https://user:pa/ss@github.com/Org/Repo",
        "relative/dir:foo",
        "C:/x/y",
    ],
)
def test_name_key_ignores_local_relative_or_unsafe_origins(
    tmp_path: Path, origin: str
) -> None:
    main, worktree = _repo_with_worktree(tmp_path, origin)
    home = tmp_path / "home"
    expected = str(main.resolve()).replace("/", "-")
    assert _name_key(main, home) == expected
    assert _name_key(worktree, home) == expected


@pytest.mark.parametrize(
    "origin",
    [
        "https://github.com/Org/Repo.git?token=abc#frag",
        "ssh://git@github.com:22/Org/Repo.git",
        "HTTPS://GitHub.com:443/Org/Repo//",
        "https://github.com//Org//Repo.git",
        "git@github.com:/Org/Repo.git",
    ],
)
def test_name_key_drops_query_port_and_case(tmp_path: Path, origin: str) -> None:
    main, _ = _repo_with_worktree(tmp_path, origin)
    assert _name_key(main, tmp_path / "home") == "github.com-Org-Repo"


def test_name_key_ignores_git_dir_from_the_environment(tmp_path: Path) -> None:
    main, _ = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    plain = tmp_path / "plain"
    plain.mkdir()
    env = _git_env(tmp_path / "home")
    env["GIT_DIR"] = str(main / ".git")
    key = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--key"],
        cwd=plain,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    assert key == str(plain).replace("/", "-")


def test_nested_claude_in_another_worktree_keeps_the_parent_name(
    tmp_path: Path,
) -> None:
    main, worktree = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    home = tmp_path / "home"
    topics = home / ".claude" / "projects" / "github.com-Org-Repo" / "topics"
    env = _git_env(home)
    env.pop("CLAUDE_ENV_FILE", None)
    # ccsession labeled the session in the main folder...
    env.update({"CLAUDE_TOPIC": "notes", "CCSESSION_TOPIC_CWD": str(main.resolve())})

    def hook(session: str, cwd: Path) -> None:
        payload = json.dumps({"session_id": session, "cwd": str(cwd)})
        subprocess.run(
            ["bash", str(SKILL_DIR / "hooks" / "session-start.sh")],
            input=payload,
            env=env,
            text=True,
            check=True,
        )

    hook("parent-sid", main)
    # ...and a claude started by a pipeline in a worktree inherits the label.
    hook("child-sid", worktree)
    assert (topics / "notes.txt").read_text().strip() == "parent-sid"


def test_symlinked_hook_still_saves_under_the_repo(tmp_path: Path) -> None:
    _, worktree = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    home = tmp_path / "home"
    link = tmp_path / "hooks" / "ccs.sh"
    link.parent.mkdir()
    link.symlink_to(SKILL_DIR / "hooks" / "session-start.sh")
    env = _git_env(home)
    env.pop("CLAUDE_ENV_FILE", None)
    env.pop("CCSESSION_TOPIC_CWD", None)
    env["CLAUDE_TOPIC"] = "linked"
    payload = json.dumps({"session_id": "sid-l", "cwd": str(worktree)})
    subprocess.run(["bash", str(link)], input=payload, env=env, text=True, check=True)
    topics = home / ".claude" / "projects" / "github.com-Org-Repo" / "topics"
    assert (topics / "linked.txt").read_text().strip() == "sid-l"


# One name per session, however it was given: `ccsession <name>`, or Claude
# Code's --name and /rename, which the hooks copy into ccsession's list.


def _named_repo(tmp_path: Path) -> tuple[Path, Path, Path, dict[str, str]]:
    main, worktree = _repo_with_worktree(tmp_path, "https://github.com/Org/Repo")
    fake = tmp_path / "claude-args"
    fake.write_text(
        "#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n"
    )
    fake.chmod(0o700)
    home = tmp_path / "home"
    env = _git_env(home)
    env.update(
        {
            "CLAUDE_BIN": str(fake),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
            "XDG_CACHE_HOME": str(tmp_path / "cache"),
        }
    )
    return main, worktree, home / ".claude" / "projects", env


def _transcript(
    projects: Path, folder: Path, session: str, *titles: str, branch: str = ""
) -> Path:
    """A saved conversation, written the way Claude Code writes it (compact JSON)."""
    saved = projects / str(folder).replace("/", "-")
    saved.mkdir(parents=True, exist_ok=True)
    first: dict[str, str] = {"type": "user", "cwd": str(folder), "sessionId": session}
    if branch:
        first["gitBranch"] = branch
    rows = [first]
    rows += [
        {"type": "custom-title", "customTitle": t, "sessionId": session} for t in titles
    ]
    path = saved / f"{session}.jsonl"
    path.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows))
    return path


def _ccs(cwd: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


def _launched(cwd: Path, env: dict[str, str], name: str) -> list[str]:
    return json.loads(_ccs(cwd, env, name).stdout.strip().splitlines()[-1])


# Runs a command from a process of its own, as a claude started inside a
# session does: its hooks then find that process, not the launched Claude Code.
_NESTED = [
    sys.executable,
    "-c",
    "import subprocess, sys; sys.exit(subprocess.run(sys.argv[1:]).returncode)",
]


def _hook(
    env: dict[str, str],
    cwd: Path,
    session: str,
    event: str,
    nested: bool = False,
    form: str = "native",
    **fields: str,
) -> None:
    """Run a hook as Claude Code does: sh -c '<command>', with the command as
    hooks.json registers it ("native": the script path) or as the standalone
    install.sh does ("standalone": bash "<path>"); session-start.sh for
    SessionStart.

    The test process stands in for the Claude Code that runs the hook, so
    CCSESSION_LAUNCH_ID=<this pid>.<n> makes it the one ccsession launched.
    """
    script = (
        SKILL_DIR
        / "hooks"
        / ("session-start.sh" if event == "SessionStart" else "session-name.sh")
    )
    command = f"'{script}'" if form == "native" else f'bash "{script}"'
    payload = {"session_id": session, "cwd": str(cwd), **fields}
    if event != "SessionStart":
        payload["hook_event_name"] = event
    subprocess.run(
        [*(_NESTED if nested else []), "sh", "-c", command],
        input=json.dumps(payload),
        env=env,
        text=True,
        check=True,
    )


def _listed(cwd: Path, env: dict[str, str], *args: str) -> dict[str, str]:
    """The names `ccsession --here --all` (or the given listing) shows, each
    with its session's short id."""
    rows = {}
    for line in _ccs(cwd, env, *(args or ("--here", "--all"))).stdout.splitlines():
        match = re.match(
            r"^  (.+?) {2,}(?:started |\(transcript missing\)|\(times unavailable\)).*?"
            r" (\S+)(?:  \(was [^)]*\))?$",
            line,
        )
        if match:
            rows[match.group(1)] = match.group(2)
    return rows


def _fake_orca(tmp_path: Path, env: dict[str, str]) -> Path:
    """An orca CLI that records each call and keeps the tab's title like Orca:
    `terminal rename --title` sets it, `terminal rename` alone resets it to the
    terminal's own title, `terminal show` reports it. Returns the record file."""
    tools = tmp_path / "orca-tools"
    tools.mkdir(exist_ok=True)
    record = tmp_path / "orca-calls"
    title = tmp_path / "orca-tab-title"
    (tools / "orca").write_text(
        f"""#!/usr/bin/env python3
import json, pathlib, sys
args = sys.argv[1:]
title = pathlib.Path({str(title)!r})
if args[:2] == ["terminal", "show"]:
    now = title.read_text() if title.exists() else "terminal's own title"
    print(json.dumps({{"result": {{"terminal": {{"title": now}}}}}}))
    sys.exit(0)
open({str(record)!r}, "a").write(json.dumps(args) + "\\n")
if args[:2] == ["terminal", "rename"]:
    if "--title" in args:
        title.write_text(args[args.index("--title") + 1])
    else:
        title.unlink(missing_ok=True)
"""
    )
    (tools / "orca").chmod(0o700)
    env["PATH"] = f"{tools}:{env['PATH']}"
    return record


def _orca_calls(record: Path) -> list[list[str]]:
    if not record.exists():
        return []
    return [json.loads(line) for line in record.read_text().splitlines()]


def test_a_name_with_spaces_and_slashes_starts_lists_and_resumes(
    tmp_path: Path,
) -> None:
    main, worktree, projects, env = _named_repo(tmp_path)
    name = "my work/v2 50%"
    # A new session: Claude Code gets the same name.
    assert _launched(main, env, name) == [*ORCA_FLAGS, "--name", name]
    _hook(
        {**env, "CLAUDE_TOPIC": name, "CCSESSION_TOPIC_CWD": str(main.resolve())},
        main,
        SESSION_ID,
        "SessionStart",
    )
    _transcript(projects, main, SESSION_ID)
    topics = projects / "github.com-Org-Repo" / "topics"
    assert (topics / "my work%2Fv2 50%25.txt").read_text().strip() == SESSION_ID
    assert _listed(worktree, env) == {name: SESSION_ID[:8]}
    # Resumed from another worktree of the repo, under the same name.
    assert _launched(worktree, env, name)[-4:] == [
        "--name",
        name,
        "--resume",
        SESSION_ID,
    ]
    _ccs(worktree, env, "--rm", name)
    assert _listed(main, env) == {}


@pytest.mark.parametrize("bad", ["", "   ", "tab\there", "line\nbreak"])
def test_blank_names_and_control_characters_are_refused(
    tmp_path: Path, bad: str
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--sync-name", SESSION_ID, bad],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2
    assert not list(projects.glob("*/topics/*.txt"))


def test_rename_in_claude_code_renames_the_listed_name(tmp_path: Path) -> None:
    main, worktree, projects, env = _named_repo(tmp_path)
    topic_env = {**env, "CLAUDE_TOPIC": "demo", "CCSESSION_TOPIC_CWD": str(main)}
    _hook(topic_env, main, SESSION_ID, "SessionStart")
    _transcript(projects, main, SESSION_ID)
    assert _listed(main, env) == {"demo": SESSION_ID[:8]}
    # /rename, picked up by the next prompt: listed once, under the new name.
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="renamed one")
    assert _listed(main, env) == {"renamed one": SESSION_ID[:8]}
    assert _launched(worktree, env, "renamed one")[-4:] == [
        "--name",
        "renamed one",
        "--resume",
        SESSION_ID,
    ]
    # A prompt without a name, or with the same one, changes nothing.
    _hook(env, main, SESSION_ID, "UserPromptSubmit")
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="renamed one")
    assert _listed(main, env) == {"renamed one": SESSION_ID[:8]}


def test_a_rename_just_before_quitting_is_kept(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    # SessionEnd reports no name: the newest one in the transcript is used.
    path = _transcript(projects, main, SESSION_ID, "first", "last one")
    _hook(env, main, SESSION_ID, "SessionEnd", transcript_path=str(path))
    assert _listed(main, env) == {"last one": SESSION_ID[:8]}


def test_a_name_another_session_has_gets_a_number(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    other = "def67890-0000-0000-0000-000000000000"
    _transcript(projects, main, SESSION_ID)
    _transcript(projects, main, other)
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="shared")
    _hook(env, main, other, "UserPromptSubmit", session_title="shared")
    assert _listed(main, env) == {"shared": SESSION_ID[:8], "shared-2": other[:8]}
    # A name whose conversation no longer exists is free again.
    topics = projects / "github.com-Org-Repo" / "topics"
    (topics / "gone.txt").write_text("99999999-0000-0000-0000-000000000000\n")
    _hook(env, main, other, "UserPromptSubmit", session_title="gone")
    assert _listed(main, env) == {"shared": SESSION_ID[:8], "gone": other[:8]}


def test_sessions_without_a_name_never_join_the_list(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _transcript(projects, main, SESSION_ID)
    _hook(env, main, SESSION_ID, "SessionStart")
    _hook(env, main, SESSION_ID, "UserPromptSubmit")
    _hook(env, main, SESSION_ID, "SessionEnd", transcript_path="/nonexistent")
    assert not list(projects.glob("*/topics/*.txt"))


def _orca_launch_env(tmp_path: Path, env: dict[str, str]) -> Path:
    """The environment ccsession leaves for Claude Code in an Orca tab."""
    env.update(
        {
            "ORCA_PANE_KEY": "tab-1:leaf-1",
            "ORCA_TERMINAL_HANDLE": "term_test",
            "CLAUDE_CODE_DISABLE_TERMINAL_TITLE": "1",
            # This test process stands in for the Claude Code ccsession launched.
            "CCSESSION_LAUNCH_ID": f"{os.getpid()}.1",
        }
    )
    return _fake_orca(tmp_path, env)


@pytest.mark.parametrize("form", ["native", "standalone"])
def test_orca_tab_follows_a_rename_of_the_launched_session(
    tmp_path: Path, form: str
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    record = _orca_launch_env(tmp_path, env)
    topic_env = {**env, "CLAUDE_TOPIC": "notes", "CCSESSION_TOPIC_CWD": str(main)}
    # No session_title: the label comes from the launch (CLAUDE_TOPIC) alone.
    _hook(topic_env, main, SESSION_ID, "SessionStart", form=form)
    _transcript(projects, main, SESSION_ID)
    assert _listed(main, env) == {"notes": SESSION_ID[:8]}
    rename = ["terminal", "rename", "--terminal", "term_test", "--title"]
    assert _orca_calls(record) == [[*rename, "notes · Claude Code"]]
    _hook(env, main, SESSION_ID, "UserPromptSubmit", form=form, session_title="notes")
    assert len(_orca_calls(record)) == 1  # unchanged name: Orca is not asked
    _hook(env, main, SESSION_ID, "UserPromptSubmit", form=form, session_title="notes 2")
    assert _orca_calls(record)[-1] == [*rename, "notes 2 · Claude Code"]
    # /clear: the next conversation runs in the same Claude Code, so it is the
    # launched session too, and the tab stays.
    gone = "/nonexistent"
    _hook(
        env,
        main,
        SESSION_ID,
        "SessionEnd",
        form=form,
        transcript_path=gone,
        reason="clear",
    )
    calls = len(_orca_calls(record))
    after = "def67890-0000-0000-0000-000000000000"
    _hook(env, main, after, "UserPromptSubmit", form=form, session_title="after clear")
    assert len(_orca_calls(record)) == calls + 1
    assert _orca_calls(record)[-1] == [*rename, "after clear · Claude Code"]
    # Leaving Claude Code takes the title ccsession set back off the tab.
    _hook(
        env, main, after, "SessionEnd", form=form, transcript_path=gone, reason="other"
    )
    assert _orca_calls(record)[-1] == ["terminal", "rename", "--terminal", "term_test"]
    assert not (tmp_path / "cache/ccsession/orca-titles/term_test").exists()


def test_where_processes_cannot_be_read_the_hook_acts_for_the_launch(
    tmp_path: Path,
) -> None:
    # No /proc entry and no ps line for the process to start from (here, one
    # that does not exist): ownership cannot be checked, so it is assumed.
    main, _, projects, env = _named_repo(tmp_path)
    record = _orca_launch_env(tmp_path, env)
    env["CCSESSION_HOOK_PARENT"] = "999999999"
    _transcript(projects, main, SESSION_ID)
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="unchecked")
    assert _listed(main, env) == {"unchecked": SESSION_ID[:8]}
    assert _orca_calls(record)[-1][-1] == "unchecked · Claude Code"


def test_a_claude_started_inside_a_session_takes_neither_its_name_nor_its_tab(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    record = _orca_launch_env(tmp_path, env)
    topic_env = {**env, "CLAUDE_TOPIC": "notes", "CCSESSION_TOPIC_CWD": str(main)}
    _hook(topic_env, main, SESSION_ID, "SessionStart")
    _transcript(projects, main, SESSION_ID)
    calls = len(_orca_calls(record))
    # A pipeline's claude in the same folder inherits all of that environment,
    # before the session's next prompt, after a /clear, or after it quit.
    gone = "/nonexistent"
    _hook(env, main, SESSION_ID, "SessionEnd", transcript_path=gone, reason="clear")
    child = "c0ffee00-0000-0000-0000-000000000000"
    _hook(topic_env, main, child, "SessionStart", nested=True)
    _transcript(projects, main, child)
    _hook(env, main, child, "UserPromptSubmit", nested=True, session_title="job")
    _hook(env, main, child, "SessionEnd", nested=True, transcript_path=gone)
    assert _listed(main, env) == {"notes": SESSION_ID[:8], "job": child[:8]}
    assert len(_orca_calls(record)) == calls
    # The launched Claude Code still owns its tab after all that.
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="notes 2")
    assert _orca_calls(record)[-1][-1] == "notes 2 · Claude Code"


def test_ccsession_inside_claude_code_leaves_the_tab_and_label_alone(
    tmp_path: Path,
) -> None:
    # A ccsession run by Claude Code (its Bash tool) inherits the session's
    # label and Orca tab; neither belongs to it.
    main, _, _, env = _named_repo(tmp_path)
    record = _orca_launch_env(tmp_path, env)
    fake = tmp_path / "claude-env"
    names = [
        "CLAUDE_TOPIC",
        "CCSESSION_TOPIC_CWD",
        "ORCA_PANE_KEY",
        "ORCA_TERMINAL_HANDLE",
        "CLAUDE_CODE_DISABLE_TERMINAL_TITLE",
    ]
    fake.write_text(
        "#!/usr/bin/env python3\nimport json, os\n"
        f"print(json.dumps({{n: os.environ.get(n) for n in {names!r}}}))\n"
    )
    fake.chmod(0o700)
    env.update(
        {
            "CLAUDECODE": "1",
            "CLAUDE_BIN": str(fake),
            "CLAUDE_TOPIC": "parent",
            "CCSESSION_TOPIC_CWD": str(main),
        }
    )
    del env["CLAUDE_CODE_DISABLE_TERMINAL_TITLE"]
    seen = json.loads(
        _ccs(main, env, "--profile", "claude").stdout.strip().splitlines()[-1]
    )
    assert seen == dict.fromkeys(names)
    assert _orca_calls(record) == []


@pytest.mark.parametrize("tab", ["ours", "typed since", "never set"])
def test_launch_clears_only_a_tab_title_ccsession_set(tmp_path: Path, tab: str) -> None:
    main, _, _, env = _named_repo(tmp_path)
    record = _orca_launch_env(tmp_path, env)
    del env["CLAUDE_CODE_DISABLE_TERMINAL_TITLE"], env["CCSESSION_LAUNCH_ID"]
    mark = tmp_path / "cache/ccsession/orca-titles/term_test"
    if tab != "never set":
        # The title an earlier session's /rename gave the tab, before a crash.
        mark.parent.mkdir(parents=True)
        mark.write_text("old · Claude Code\n")
        shown = "old · Claude Code" if tab == "ours" else "deploy box"
        (tmp_path / "orca-tab-title").write_text(shown)
    _ccs(main, env, "demo")
    deadline = time.monotonic() + 10
    while mark.exists() and time.monotonic() < deadline:
        time.sleep(0.1)
    time.sleep(0.5)  # the clear runs in the background
    expected = (
        [["terminal", "rename", "--terminal", "term_test"]] if tab == "ours" else []
    )
    assert _orca_calls(record) == expected
    assert not mark.exists()
    if tab == "typed since":
        assert (tmp_path / "orca-tab-title").read_text() == "deploy box"


def test_a_name_starting_with_a_dash_is_listed_and_resumes(tmp_path: Path) -> None:
    main, worktree, projects, env = _named_repo(tmp_path)
    _transcript(projects, main, SESSION_ID)
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="-wip")
    assert _listed(main, env) == {"-wip": SESSION_ID[:8]}
    launched = json.loads(
        _ccs(worktree, env, "--name", "-wip").stdout.strip().splitlines()[-1]
    )
    assert launched[-4:] == ["--name", "-wip", "--resume", SESSION_ID]


def test_orca_question_takes_a_name_starting_with_a_dash(tmp_path: Path) -> None:
    _, record = _orca_tty(tmp_path, keys="-x\r")
    assert record["topic"] == "-x"
    assert record["argv"] == [*ORCA_FLAGS, "--name", "-x"]


def test_labels_older_versions_saved_with_a_leading_dot_still_resume(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    topics = projects / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True)
    (topics / ".hidden.txt").write_text(f"{SESSION_ID}\n")
    _transcript(projects, main, SESSION_ID)
    _ccs(main, env, "--migrate-names")
    assert _listed(main, env) == {".hidden": SESSION_ID[:8]}
    assert _launched(main, env, ".hidden")[-2:] == ["--resume", SESSION_ID]


@pytest.mark.parametrize("copied_before", [False, True])
def test_a_hidden_label_in_an_old_per_folder_list_reaches_the_repo_list(
    tmp_path: Path, copied_before: bool
) -> None:
    # Older versions kept one list per folder, and saved a leading-"." name as
    # a hidden file the copy to the repo's list never saw.
    main, _, projects, env = _named_repo(tmp_path)
    old = projects / str(main.resolve()).replace("/", "-") / "topics"
    old.mkdir(parents=True)
    (old / ".cwd").write_text(f"{main.resolve()}\n")
    (old / ".notes.txt").write_text(f"{SESSION_ID}\n")
    if copied_before:  # the list was copied by an earlier version
        (old / ".ccsession-moved-to-repo").write_text("")
    _transcript(projects, main, SESSION_ID)
    _ccs(main, env, "--migrate-names")
    assert _listed(main, env) == {".notes": SESSION_ID[:8]}
    assert _launched(main, env, ".notes")[-2:] == ["--resume", SESSION_ID]


def test_a_hidden_label_whose_name_the_repo_list_has_gets_a_number(
    tmp_path: Path,
) -> None:
    # The old list was copied already and the repo's list has ".notes" for
    # another session: both sessions stay listed.
    main, _, projects, env = _named_repo(tmp_path)
    other = "def67890-0000-0000-0000-000000000000"
    old = projects / str(main.resolve()).replace("/", "-") / "topics"
    old.mkdir(parents=True)
    (old / ".cwd").write_text(f"{main.resolve()}\n")
    (old / ".ccsession-moved-to-repo").write_text("")
    (old / ".notes.txt").write_text(f"{SESSION_ID}\n")
    repo = projects / "github.com-Org-Repo" / "topics"
    repo.mkdir(parents=True)
    (repo / "%2Enotes.txt").write_text(f"{other}\n")
    for session in (SESSION_ID, other):
        _transcript(projects, main, session)
    _ccs(main, env, "--migrate-names")
    assert _listed(main, env) == {".notes": other[:8], ".notes-2": SESSION_ID[:8]}


def test_sessions_renamed_to_one_name_at_once_both_stay_listed(
    tmp_path: Path,
) -> None:
    # Two hooks at the same moment: without the list's lock both saw the name
    # free, and one entry overwrote the other.
    main, _, projects, env = _named_repo(tmp_path)
    sessions = [f"{n}{n}{n}{n}0000-0000-0000-0000-000000000000" for n in "ab"]
    for session in sessions:
        _transcript(projects, main, session)
    topics = projects / "github.com-Org-Repo" / "topics"
    for _ in range(10):
        for f in topics.glob("*.txt"):
            f.unlink()
        runs = [
            subprocess.Popen(
                [str(SKILL_DIR / "ccsession"), "--sync-name", s, "shared"],
                cwd=main,
                env=env,
                stdout=subprocess.DEVNULL,
            )
            for s in sessions
        ]
        assert [r.wait(timeout=60) for r in runs] == [0, 0]
        listed = _listed(main, env)
        assert set(listed) == {"shared", "shared-2"}
        assert sorted(listed.values()) == [s[:8] for s in sessions]


@pytest.mark.parametrize("left", ["empty", "not empty"])
def test_a_lock_folder_left_by_the_earlier_build_is_handled(
    tmp_path: Path, left: str
) -> None:
    # A build before flock locked with an empty .ccsession-lock folder; a killed
    # run could leave it, and the lock file then could not be opened.
    main, _, projects, env = _named_repo(tmp_path)
    _transcript(projects, main, SESSION_ID)
    lock = projects / "github.com-Org-Repo" / "topics" / ".ccsession-lock"
    lock.mkdir(parents=True)
    if left == "not empty":
        (lock / "stray").write_text("")
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--sync-name", SESSION_ID, "named"],
        cwd=main,
        env=env,
        capture_output=True,
        text=True,
    )
    if left == "empty":
        assert result.returncode == 0, result.stderr
        assert lock.is_file()
        assert _listed(main, env) == {"named": SESSION_ID[:8]}
    else:  # someone else's folder: left alone, with a clear message
        assert result.returncode == 1
        assert "is a folder that is not empty" in result.stderr
        assert (lock / "stray").exists()


def test_a_live_lock_holder_is_waited_for_and_a_killed_one_frees_it(
    tmp_path: Path,
) -> None:
    # A sync that takes long keeps the list to itself: nobody takes its lock over
    # (the earlier 3-second take-over let two runs in). A killed holder's lock
    # goes with its process.
    main, _, projects, env = _named_repo(tmp_path)
    _transcript(projects, main, SESSION_ID)
    topics = projects / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True)
    hold = [
        sys.executable,
        "-c",
        "import fcntl, sys, time; f = open(sys.argv[1], 'a');"
        " fcntl.flock(f, fcntl.LOCK_EX); print('held', flush=True);"
        " time.sleep(float(sys.argv[2]))",
        str(topics / ".ccsession-lock"),
    ]
    holder = subprocess.Popen([*hold, "1.5"], stdout=subprocess.PIPE, text=True)
    assert holder.stdout.readline().strip() == "held"
    start = time.monotonic()
    _ccs(main, env, "--sync-name", SESSION_ID, "waited")
    assert time.monotonic() - start >= 1.0  # it waited for the holder
    assert holder.wait(timeout=60) == 0
    assert _listed(main, env) == {"waited": SESSION_ID[:8]}
    killed = subprocess.Popen([*hold, "60"], stdout=subprocess.PIPE, text=True)
    assert killed.stdout.readline().strip() == "held"
    killed.kill()
    killed.wait(timeout=60)
    start = time.monotonic()
    _ccs(main, env, "--sync-name", SESSION_ID, "after kill")
    assert time.monotonic() - start < 3
    assert _listed(main, env) == {"after kill": SESSION_ID[:8]}


@pytest.mark.parametrize(
    ("name", "ok"),
    [
        ("/" * 81, True),  # 243 bytes as a file name
        ("/" * 82, False),
        ("あ" * 81, True),
        ("あ" * 82, False),
        ("x" * 245, True),
        ("x" * 246, False),
    ],
)
def test_the_name_length_limit_is_the_documented_one(
    tmp_path: Path, name: str, ok: bool
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _transcript(projects, main, SESSION_ID)
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--sync-name", SESSION_ID, name],
        cwd=main,
        env=env,
        capture_output=True,
        text=True,
    )
    assert (result.returncode == 0) == ok, result.stderr
    if ok:  # it fits even with a collision suffix
        assert _listed(main, env) == {name: SESSION_ID[:8]}


def test_orca_tab_is_left_to_claude_code_where_ccsession_does_not_own_it(
    tmp_path: Path,
) -> None:
    # Outside a ccsession launch Claude Code's own title shows a /rename itself.
    main, _, projects, env = _named_repo(tmp_path)
    record = _orca_launch_env(tmp_path, env)
    del env["CLAUDE_CODE_DISABLE_TERMINAL_TITLE"]
    _transcript(projects, main, SESSION_ID)
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="plain")
    assert _listed(main, env) == {"plain": SESSION_ID[:8]}
    assert _orca_calls(record) == []


def test_names_given_before_ccsession_kept_them_are_imported_once(
    tmp_path: Path,
) -> None:
    main, worktree, projects, env = _named_repo(tmp_path)
    renamed = "11111111-0000-0000-0000-000000000000"
    gone = "22222222-0000-0000-0000-000000000000"
    _transcript(projects, worktree, renamed, "old", "newer name")
    _transcript(projects, tmp_path / "deleted-folder", gone, "from gone")
    _transcript(projects, main, SESSION_ID)  # never named
    _ccs(main, env, "--migrate-names")
    assert _listed(main, env) == {"newer name": renamed[:8]}
    # A folder that no longer exists keeps its names in its own folder's list.
    assert _listed(main, env, "--list") == {
        "newer name": renamed[:8],
        "from gone": gone[:8],
    }
    # Once only: a name removed afterwards is not brought back.
    _ccs(main, env, "--rm", "newer name")
    _ccs(main, env, "--migrate-names")
    assert _listed(main, env) == {}


def test_orca_question_takes_a_name_with_spaces(tmp_path: Path) -> None:
    _, record = _orca_tty(tmp_path, keys="my work\r")
    assert record["topic"] == "my work"
    assert record["argv"] == [*ORCA_FLAGS, "--name", "my work"]


def test_framework_hooks_register_the_rename_hook() -> None:
    hooks = json.loads(
        (REPO_ROOT / "src" / "superclaude" / "hooks" / "hooks.json").read_text()
    )["hooks"]
    for event in ("UserPromptSubmit", "SessionEnd"):
        commands = [h["command"] for reg in hooks[event] for h in reg["hooks"]]
        assert "~/.claude/skills/ccsession-tag/hooks/session-name.sh" in commands
    assert os.access(SKILL_DIR / "hooks" / "session-name.sh", os.X_OK)


# The default list follows the worktree (#347): Claude Code continues a resumed
# conversation in the folder it starts in, so a session of another worktree
# that still exists is counted, not listed; one whose worktree was removed has
# nowhere else to go and is listed in a section of its own.


def _three_worktrees(tmp_path: Path) -> tuple[Path, Path, Path, dict[str, str]]:
    """main, worktree b and a removed worktree, each with one session (and one
    more in a folder of main), all named in the repo's one list."""
    main, b, projects, env = _named_repo(tmp_path)
    removed = tmp_path / "wt-removed"
    _git(main, "worktree", "add", "-q", "-b", "removed", str(removed))
    (main / "sub").mkdir()
    topics = projects / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True)
    for n, (folder, name) in enumerate(
        [
            (main, "main work"),
            (main / "sub", "main sub"),
            (b, "b work"),
            (removed, "removed work"),
        ],
        start=1,
    ):
        session = f"{n}{n}{n}{n}0000-0000-0000-0000-000000000000"
        _transcript(projects, folder, session)
        (topics / f"{name}.txt").write_text(f"{session}\n")
    _git(main, "worktree", "remove", str(removed))
    return main, b, removed, env


def test_here_lists_this_worktree_then_removed_ones_and_counts_the_rest(
    tmp_path: Path,
) -> None:
    main, b, removed, env = _three_worktrees(tmp_path)
    out = _ccs(main, env, "--here").stdout
    assert _listed(main, env, "--here") == {
        "main work": "11110000",
        "main sub": "22220000",
        "removed work": "44440000",
    }
    rows = out.splitlines()
    section = rows.index("Sessions whose worktree was removed (they continue here):")
    assert [r for r in rows[section:] if "removed work" in r] == [
        next(r for r in rows if "removed work" in r)
    ]
    assert f"(was {removed})" in out
    assert (
        "1 more session in other worktrees of this repo: ccsession --here --all" in out
    )
    assert _listed(b, env, "--here") == {
        "b work": "33330000",
        "removed work": "44440000",
    }
    assert "2 more sessions in other worktrees" in _ccs(b, env, "--here").stdout
    # --here --all lists every worktree's sessions, as before.
    assert set(_listed(b, env, "--here", "--all")) == {
        "main work",
        "main sub",
        "b work",
        "removed work",
    }


def test_resuming_a_session_of_another_live_worktree_warns(tmp_path: Path) -> None:
    main, b, _, env = _three_worktrees(tmp_path)
    other = _ccs(b, env, "main work")
    assert json.loads(other.stdout.strip().splitlines()[-1])[-2:] == [
        "--resume",
        "11110000-0000-0000-0000-000000000000",
    ]
    assert f"WARNING: 'main work' was started in {main}" in other.stderr
    assert f"It continues here, in {b}" in other.stderr
    # Its own worktree, or a removed one: no warning.
    assert "WARNING" not in _ccs(b, env, "b work").stderr
    assert "WARNING" not in _ccs(b, env, "removed work").stderr
    assert "WARNING" not in _ccs(main, env, "main sub").stderr


def test_name_question_lists_this_worktree_and_star_lists_every_one(
    tmp_path: Path,
) -> None:
    _, b, _, env = _three_worktrees(tmp_path)
    question = "Session name (q): "
    proc, master = _spawn_on_pty(
        [str(SKILL_DIR / "ccsession"), "--ask", "q"], env, b, stdout=subprocess.PIPE
    )
    try:
        first = _read_pty(master, until=question)
        assert "b work" in first and "removed work" in first
        assert "main work" not in first
        assert (
            "2 more sessions in other worktrees of this repo: type * to list them"
            in first
        )
        os.write(master, b"*\r")
        every = _read_pty(master, until=question)
        assert "Saved sessions in every worktree of this repo" in every
        assert "main work" in every and "main sub" in every
        os.write(master, b"\r")
        assert proc.wait(timeout=60) == 0
        assert proc.stdout.read() == b"\n"  # Enter: untagged
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)


def test_a_session_belongs_to_the_worktree_it_was_started_in(tmp_path: Path) -> None:
    # Transcript lines record the session shell's folder, which follows a cd;
    # Claude Code stores the transcript under the folder the session was
    # started in (each character other than a letter or digit becomes "-").
    main, b, projects, env = _named_repo(tmp_path)
    session = "abcd1234-0000-0000-0000-000000000000"
    store = projects / re.sub(r"[^A-Za-z0-9]", "-", str(main))
    store.mkdir(parents=True)
    rows = [  # copied from another machine first, then cd'ed into worktree b
        {"type": "user", "cwd": "/Users/someone/orca/Repo", "sessionId": session},
        {"type": "user", "cwd": str(main), "sessionId": session},
        {"type": "assistant", "cwd": str(b), "sessionId": session},
    ]
    (store / f"{session}.jsonl").write_text(
        "".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows)
    )
    topics = projects / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True)
    (topics / "started in main.txt").write_text(f"{session}\n")
    assert _listed(main, env, "--here") == {"started in main": "abcd1234"}
    assert _listed(b, env, "--here") == {}
    assert "WARNING" in _ccs(b, env, "started in main").stderr
    assert "WARNING" not in _ccs(main, env, "started in main").stderr


def test_worktree_list_ignores_git_variables_from_the_caller(tmp_path: Path) -> None:
    # A hook or script run for another checkout can leave GIT_DIR and
    # GIT_WORK_TREE set; the list must still follow the current folder.
    main, b, _, env = _three_worktrees(tmp_path)
    env.update({"GIT_DIR": str(main / ".git"), "GIT_WORK_TREE": str(main)})
    assert set(_listed(b, env, "--here")) == {"b work", "removed work"}
    assert "WARNING" in _ccs(b, env, "main work").stderr


def test_a_deleted_folder_of_a_live_worktree_stays_with_that_worktree(
    tmp_path: Path,
) -> None:
    # Deleting the folder a session started in does not remove its worktree:
    # the session is still main's, not an orphan shown everywhere.
    main, b, _, env = _three_worktrees(tmp_path)
    (main / "sub").rmdir()
    assert set(_listed(b, env, "--here")) == {"b work", "removed work"}
    assert "main sub" in _listed(main, env, "--here")
    assert "WARNING" in _ccs(b, env, "main sub").stderr


def test_a_removed_worktree_inside_an_ignored_folder_is_still_removed(
    tmp_path: Path,
) -> None:
    # A worktree under the main checkout (e.g. .dev/worktrees/<name>, which is
    # gitignored) leaves only its ignored parent behind when removed.
    main, b, _, env = _three_worktrees(tmp_path)
    (main / ".gitignore").write_text(".dev/worktrees/\n")
    nested = main / ".dev" / "worktrees" / "gone"
    _git(main, "worktree", "add", "-q", "-b", "nested", str(nested))
    projects = tmp_path / "home" / ".claude" / "projects"
    session = "55550000-0000-0000-0000-000000000000"
    _transcript(projects, nested, session, branch="nested")
    topics = projects / "github.com-Org-Repo" / "topics"
    (topics / "nested work.txt").write_text(f"{session}\n")
    _git(main, "worktree", "remove", str(nested))
    assert "nested work" in _listed(b, env, "--here")
    assert "WARNING" not in _ccs(b, env, "nested work").stderr


def _branch(repo: Path) -> str:
    return subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"],
        cwd=repo,
        env=_git_env(repo),
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def _add_session(
    env: dict[str, str], folder: Path, n: int, name: str, branch: str
) -> None:
    projects = Path(env["HOME"]) / ".claude" / "projects"
    session = f"{n}{n}{n}{n}0000-0000-0000-0000-000000000000"
    _transcript(projects, folder, session, branch=branch)
    topics = projects / "github.com-Org-Repo" / "topics"
    (topics / f"{name}.txt").write_text(f"{session}\n")


def test_a_deleted_ignored_folder_of_a_live_worktree_stays_with_it(
    tmp_path: Path,
) -> None:
    # An ignored folder (build output) is not a worktree: a session started
    # there on the worktree's own branch still belongs to that worktree.
    main, b, _, env = _three_worktrees(tmp_path)
    (main / ".gitignore").write_text("build\n")
    (main / "build").mkdir()
    _add_session(env, main / "build", 6, "build work", _branch(main))
    shutil.rmtree(main / "build")
    assert "build work" not in _listed(b, env, "--here")
    assert "build work" in _listed(main, env, "--here")
    assert "WARNING" in _ccs(b, env, "build work").stderr


def test_a_deleted_folder_of_another_copy_of_the_repo_stays_with_that_copy(
    tmp_path: Path,
) -> None:
    # Another clone of the same repo is not one of this clone's worktrees,
    # but it still exists: its session is not an orphan.
    main, b, _, env = _three_worktrees(tmp_path)
    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "-q", str(main), str(clone))
    _git(clone, "remote", "set-url", "origin", "https://github.com/Org/Repo")
    (clone / "sub").mkdir()
    _add_session(env, clone / "sub", 7, "clone sub", _branch(clone))
    (clone / "sub").rmdir()
    assert "clone sub" not in _listed(b, env, "--here")
    assert "clone sub" not in _listed(main, env, "--here")
    assert "WARNING" in _ccs(b, env, "clone sub").stderr
