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

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "ccsession-tag"


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
        '"upstream":"http://gateway.example:4000/cli","port":4555}\'\n'
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
        "gpt": ("gpt-5.6-sol", "850000", "850000", "gpt-5.6-sol"),
        "372k": ("gpt-5.6-sol", "850000", "850000", "gpt-5.6-sol"),
        "gpt1": ("gpt-6-astra", "850000", "850000", "gpt-6-astra"),
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
        "--profile gpt1",
        "--list",
        "--here",
        "--rm",
    ):
        assert expected in result.stdout


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
        [str(SKILL_DIR / "ccsession"), "--profile", "gpt1"],
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
        [str(SKILL_DIR / "ccsession"), "--profile", "gpt1", "--shim"],
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
            {"id": "Qwen/Qwen3-Max"},
            {"id": "Qwen3.8-max"},
            {"id": "gpt-image-2.5-sunburst"},
            {"id": "gpt-5.5"},
        ]
    }

    models = module["transform_models"](payload)["data"]
    ids = [model["id"] for model in models]
    aliases = module["alias_to_real"]

    assert ids[:9] == [
        "claude-opus-5-5[1m]",
        "claude-gw-gpt-6-astra[1m]",
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
    ):
        assert hidden not in ids
    assert aliases["claude-gw-gpt-6-astra"] == "gpt-6-astra"
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
