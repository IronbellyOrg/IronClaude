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
        "CLAUDE_TOPIC",
        "CCSESSION_TOPIC_CWD",
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
        assert "Starting model-alias shim" in first.stdout
        second = subprocess.run(
            command,
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
            stdin=subprocess.DEVNULL,
        )
        assert second.returncode == 0, second.stderr
        assert "already running" in second.stdout
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


def _label_launch(
    tmp_path: Path, transcript: bool, args: tuple[str, ...] = ("demo",)
) -> tuple[str, bool]:
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
    return result.stdout, (topics / "demo.txt").exists()


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
    stdout, label_kept = _label_launch(tmp_path, transcript=False)
    assert "has no saved conversation; starting a new one" in stdout
    assert "--resume" not in json.loads(stdout.strip().splitlines()[-1])
    assert not label_kept


def test_label_with_saved_transcript_resumes(tmp_path: Path) -> None:
    stdout, label_kept = _label_launch(tmp_path, transcript=True)
    args = json.loads(stdout.strip().splitlines()[-1])
    assert args[-2:] == ["--resume", "abc12345-0000-0000-0000-000000000000"]
    assert label_kept


@pytest.mark.parametrize(
    ("args", "transcript"),
    [
        (("-p", "x"), False),
        (("--profile", "claude", "-p", "x"), False),
        (("demo",), False),
        (("demo",), True),
        (("--profile", "claude", "demo"), False),
        (("--profile", "claude", "demo"), True),
    ],
)
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


# ccsession-orca: Orca's Claude command. Each launch runs the real wrapper and
# the real ccsession against a fake claude that records its argv and env, and a
# fake shim that ccsession reuses.
ORCA = SKILL_DIR / "ccsession-orca"
ORCA_QUESTION = "Session name (Enter or Ctrl+C = untagged; untagged after 30s): "
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
            "CCSESSION_AUTOSTART",
            "CCSESSION_ASK_TIMEOUT",
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


def test_orca_saved_name_is_listed_and_resumes_before_the_prompt(
    tmp_path: Path,
) -> None:
    _seed_label(tmp_path, "demo")
    output, record = _orca_tty(tmp_path, "fix it", keys="demo\r")
    assert "Saved sessions in" in output
    assert "demo" in output.split(ORCA_QUESTION)[0]
    assert record["topic"] == "demo"
    assert record["argv"] == [
        *ORCA_FLAGS,
        "--name",
        "demo",
        "--resume",
        SESSION_ID,
        "fix it",
    ]


@pytest.mark.parametrize("keys", ["\r", "\x03"], ids=["enter", "ctrl-c"])
def test_orca_enter_or_ctrl_c_starts_untagged(tmp_path: Path, keys: str) -> None:
    output, record = _orca_tty(tmp_path, "the prompt", keys=keys)
    assert "Starting untagged session" in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "the prompt"]
    _assert_through_shim(record)
    # The question's default time limit is not left in Claude's environment.
    assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]


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
    proc, master = _spawn_on_pty([str(ORCA), "the prompt"], env, tmp_path / "work")
    try:
        time.sleep(1)
        os.write(master, b"\x03")
        output = _read_pty(master)
        assert proc.wait(timeout=60) == 0, output
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    assert ORCA_QUESTION not in output
    # The probe was interrupted; its traceback must not reach the terminal.
    assert "KeyboardInterrupt" not in output
    record = json.loads((tmp_path / "record.json").read_text())
    assert record["icanon"] is True
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "the prompt"]


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


def test_orca_invalid_name_asks_again(tmp_path: Path) -> None:
    # A name too long for a file name can never be saved (one starting with "-"
    # is fine now: ccsession-orca passes it as --name).
    env = _orca_env(tmp_path)
    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
    try:
        assert ORCA_QUESTION in _read_pty(master, until=ORCA_QUESTION)
        for bad in (b"x" * 246, "あ".encode() * 82):
            os.write(master, bad + b"\r")
            again = _read_pty(master, until=ORCA_QUESTION)
            assert "invalid label" in again and again.count(ORCA_QUESTION) == 1
        os.write(master, b"good\r")
        _read_pty(master)
        assert proc.wait(timeout=60) == 0
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    assert json.loads((tmp_path / "record.json").read_text())["topic"] == "good"


@pytest.mark.parametrize(
    "args",
    [
        ("--resume", SESSION_ID),
        ("--resume", SESSION_ID, "--fork-session"),
        (f"--resume={SESSION_ID}",),
        ("--continue",),
    ],
    ids=["resume", "resume-fork", "resume-equals", "continue"],
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
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, prompt]
    assert "Resuming" not in output


def test_orca_prefill_passes_through_and_its_text_is_not_a_flag(
    tmp_path: Path,
) -> None:
    # The prefill text "--resume" is input-box text, so the question is asked.
    output, record = _orca_tty(tmp_path, "--prefill", "--resume", keys="\r")
    assert record["argv"] == [*ORCA_FLAGS, "--prefill", "--resume"]
    output, record = _orca_no_tty(tmp_path, "--prefill", "draft 'text' here")
    assert record["argv"] == [*ORCA_FLAGS, "--prefill", "draft 'text' here"]


def test_orca_without_a_terminal_never_asks(tmp_path: Path) -> None:
    output, record = _orca_no_tty(tmp_path, "hello")
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "hello"]
    _assert_through_shim(record)


def test_orca_autostart_off_never_asks(tmp_path: Path) -> None:
    env = _orca_env(tmp_path, CCSESSION_AUTOSTART="0")
    output, record = _orca_tty(tmp_path, "hello", keys=None, env=env)
    assert "Session name" not in output
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "hello"]


def test_orca_unanswered_question_starts_untagged(tmp_path: Path) -> None:
    # Orca's supervised workers fail when Claude is not ready within 60s.
    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="1")
    proc, master = _spawn_on_pty([str(ORCA), "task"], env, tmp_path / "work")
    try:
        shown = _read_pty(master, until="untagged after 1s): ")
        assert "untagged after 1s): " in shown
        output = _read_pty(master)
        assert proc.wait(timeout=60) == 0, output
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)
    assert "Starting untagged session" in output
    record = json.loads((tmp_path / "record.json").read_text())
    assert record["topic"] is None
    assert record["argv"] == [*ORCA_FLAGS, "task"]


def test_orca_keys_already_typed_skip_the_question(tmp_path: Path) -> None:
    # Something typing into the tab before the question would become the name.
    output, record = _orca_tty(tmp_path, keys=None, typed_ahead="x")
    assert "Session name" not in output
    assert record["topic"] is None


def test_ask_prints_only_the_name_on_stdout(tmp_path: Path) -> None:
    env = _orca_env(tmp_path)
    _seed_label(tmp_path, "demo")
    command = [str(SKILL_DIR / "ccsession"), "--ask"]
    question = "Session name (Enter = untagged, Ctrl+C = plain shell): "
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


def _transcript(projects: Path, folder: Path, session: str, *titles: str) -> Path:
    """A saved conversation, written the way Claude Code writes it (compact JSON)."""
    saved = projects / str(folder).replace("/", "-")
    saved.mkdir(parents=True, exist_ok=True)
    rows = [{"type": "user", "cwd": str(folder), "sessionId": session}]
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
    """The names `ccsession --here` lists, each with its session's short id."""
    rows = {}
    for line in _ccs(cwd, env, *(args or ("--here",))).stdout.splitlines():
        match = re.match(
            r"^  (.+?) {2,}(?:started |\(transcript missing\)|\(times unavailable\)).*"
            r" (\S+)$",
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
