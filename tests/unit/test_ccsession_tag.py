"""Regression tests for the packaged ccsession skill and model shim."""

from __future__ import annotations

import gzip
import http.server
import json
import os
import runpy
import socket
import stat
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "ccsession-tag"


@pytest.fixture(autouse=True)
def _offline_model_data(monkeypatch, tmp_path_factory):
    """Keep tests off the network and off the real model-data cache."""
    monkeypatch.setenv("CCSESSION_MODELS_REFRESH", "0")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path_factory.mktemp("cache")))


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
        '"upstream":"http://gateway.example:4000/cli","port":4555,"model_data":"t"}\'\n'
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
        "1mm": ("claude-opus-5-5[1m]", "1000000", "1000000", ""),
        "5.6sol": ("gpt-5.6-sol", "850000", "850000", "gpt-5.6-sol"),
        "372k": ("gpt-5.6-sol", "850000", "850000", "gpt-5.6-sol"),
        "6astra": ("gpt-6-astra", "850000", "850000", "gpt-6-astra"),
        "6sol": ("gpt-6-sol", "850000", "850000", "gpt-6-sol"),
        "grok": ("grok-4.7", "500000", "500000", "grok-4.7"),
        "500k": ("grok-4.7", "500000", "500000", "grok-4.7"),
        "muse": ("muse-spark-1.3", "950000", "950000", "muse-spark-1.3"),
    }
    for profile, wanted in expected.items():
        result = _profile_result(
            tmp_path, profile, shim=profile not in {"claude", "1mm"}
        )
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
        "--profile 5.6sol",
        "--profile 6astra",
        "--profile 6sol",
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
    for directory in (
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
            if tool.name != "lsof" and not link.exists():
                link.symlink_to(tool)
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
    for profile in ("gpt", "gpt1"):
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
        [str(SKILL_DIR / "ccsession"), "--profile", "6astra"],
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
        [str(SKILL_DIR / "ccsession"), "--profile", "6astra", "--shim"],
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
            {"id": "Qwen/Qwen3-Max"},
            {"id": "Qwen3.8-max"},
            {"id": "gpt-image-2.5-sunburst"},
            {"id": "gpt-5.5"},
        ]
    }

    models = module["transform_models"](payload)["data"]
    ids = [model["id"] for model in models]
    aliases = module["alias_to_real"]

    assert ids[:11] == [
        "claude-opus-5-5[1m]",
        "claude-gw-gpt-6-astra[1m]",
        "claude-gw-gpt-6-sol[1m]",
        "claude-gw-gpt-6-luna[1m]",
        "claude-gw-gpt-5.6-sol[1m]",
        "claude-gw-gpt-5.6-luna[1m]",
        "claude-gw-gpt-5.6-terra[1m]",
        "claude-gw-grok-4.7",
        "claude-gw-muse-spark-1.3[1m]",
        "claude-gw-muse-spark-1.2[1m]",
        "claude-gw-qwen-qwen3-max",
    ]
    assert ids[-4:] == [
        "claude-gw-gpt-image-2.5-sunburst",
        "claude-gw-gpt-image-2.5",
        "claude-gw-gpt-image-2.5-flare",
        "claude-gw-grok-imagine-image-2.0",
    ]
    for hidden in (
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
    ):
        assert hidden not in ids
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
        assert health == {
            "service": "ccsession-gateway-alias-proxy",
            "upstream": f"http://127.0.0.1:{upstream.server_port}",
            "port": proxy_port,
            "model_data": json.loads((SKILL_DIR / "ccsession-models.json").read_text())[
                "version"
            ],
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
    newer["picker"]["pinned"] = newer["picker"]["pinned"][1:]
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
    assert "Valid profiles: claude, grok" in result.stderr
