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
from collections import Counter
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
    # A Coder workspace has a managed cleanupPeriodDays under /etc/claude-code;
    # a test of the retention warning must not depend on it.
    monkeypatch.setenv(
        "CCSESSION_MANAGED_SETTINGS_DIR", str(tmp_path_factory.mktemp("managed"))
    )
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
        "CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP",  # a shell value must not leak in
        "CLAUDECODE",  # set when the tests run inside Claude Code
        "CLAUDE_CODE_DISABLE_TERMINAL_TITLE",
        "CCSESSION_LAUNCH_ID",
        "CCSESSION_LAUNCH_CWD",
        # Exported by a shim session: a nested launch would forward to them.
        "CCSESSION_GATEWAY_URL",
        "CCSESSION_SHIM_URL",
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
        # --prune skips the running session and reads its days from these.
        "CLAUDE_SESSION_ID",
        "CCSESSION_AGENT_KEEP_DAYS",
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


SEED_MARKER = (
    "# Gateway address captured from the workspace by the ccsession installer."
)


def _unseed(tmp_path: Path, content: str) -> Path:
    env_file = tmp_path / "ccsession.env"
    env_file.write_text(content)
    env_file.chmod(0o600)
    subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "unseed-env.py"),
            str(env_file),
            str(SKILL_DIR / "ccsession.env.example"),
        ],
        check=True,
        capture_output=True,
    )
    return env_file


def _seeded(url: str) -> str:
    """A file exactly as the old installer (seed-env.py) left it."""
    example = (SKILL_DIR / "ccsession.env.example").read_text()
    return f"{example.rstrip()}\n\n{SEED_MARKER}\nexport ANTHROPIC_BASE_URL={url}\n"


@pytest.mark.parametrize(
    "url",
    [
        # The 2026-11-06 incident: a shim address saved from inside a session.
        "http://127.0.0.1:4114",
        "http://192.168.133.101:4000/cli",
    ],
)
def test_unseed_resets_an_installer_owned_file_to_the_example(
    tmp_path: Path, url: str
) -> None:
    env_file = _unseed(tmp_path, _seeded(url))
    assert env_file.read_text() == (SKILL_DIR / "ccsession.env.example").read_text()
    assert stat.S_IMODE(env_file.stat().st_mode) == 0o600


def test_unseed_leaves_edited_files_alone(tmp_path: Path) -> None:
    for edited in (
        "export ANTHROPIC_BASE_URL=http://mine:4000/cli\n",
        _seeded("http://127.0.0.1:4114") + "export ANTHROPIC_AUTH_TOKEN=user-added\n",
        _seeded("http://192.168.133.101:4000/cli") + "# pinned by hand\n",
        (SKILL_DIR / "ccsession.env.example").read_text(),
    ):
        assert _unseed(tmp_path, edited).read_text() == edited


def test_installers_no_longer_save_the_gateway_address() -> None:
    assert not (SKILL_DIR / "seed-env.py").exists()
    for installer in (
        SKILL_DIR / "install.sh",
        REPO_ROOT / "src" / "superclaude" / "cli" / "install_ccsession.py",
    ):
        text = installer.read_text()
        assert "seed-env.py" not in text.replace("unseed-env.py", "")
        assert "unseed-env.py" in text


@pytest.mark.parametrize(
    ("url", "base", "is_shim"),
    [
        ("http://127.0.0.1:4013", 4010, True),
        ("http://127.0.0.1:4114", 4010, True),
        ("http://localhost:4010/", 4010, True),
        ("http://127.0.0.1:4612", 4010, True),
        ("http://127.0.0.1:4000/cli", 4010, False),  # a local gateway is allowed
        ("http://127.0.0.1:4009", 4010, False),
        ("http://127.0.0.1:4108", 4010, False),  # between two attempt ranges
        ("http://127.0.0.1:4613", 4010, False),
        ("http://192.168.133.101:4013/cli", 4010, False),
        ("http://gateway.example:4013/cli", 4010, False),
        ("http://127.0.0.1/cli", 4010, False),
        ("http://127.0.0.1:5003", 5000, True),
    ],
)
def test_shim_upstream_check_flags_only_shim_addresses(
    url: str, base: int, is_shim: bool
) -> None:
    assert bool(models.shim_upstream_problem(url, base)) is is_shim


def _free_local_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@pytest.mark.parametrize("source", ["inherited", "env-file"])
def test_launch_refuses_a_shim_address_as_upstream(tmp_path: Path, source: str) -> None:
    """The 4013 -> 4114 -> refused failure: refused before any shim starts.

    Nothing listens on the shim address: the check must not need the network.
    """
    base = _free_local_port()
    shim_address = f"http://127.0.0.1:{base + 104}"
    home = tmp_path / "home"
    home.mkdir()
    env_file = tmp_path / "ccsession.env"
    env_file.write_text(
        f"export ANTHROPIC_BASE_URL={shim_address}\n" if source == "env-file" else ""
    )
    fake = tmp_path / "claude"
    fake.write_text("#!/bin/sh\necho launched\n")
    fake.chmod(0o700)
    shim_copy = tmp_path / "refused-shim.py"
    shim_copy.write_text((SKILL_DIR / "local-gateway-alias-proxy.py").read_text())
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "CLAUDE_BIN": str(fake),
            "ANTHROPIC_BASE_URL": shim_address
            if source == "inherited"
            else "http://gateway.example:4000/cli",
            "ANTHROPIC_AUTH_TOKEN": "t",
            "CC_SHIM_PORT": str(base),
            "CC_SHIM_SCRIPT": str(shim_copy),
            "CCSESSION_ENV_FILE": str(env_file),
        }
    )
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--profile", "grok", "--shim"],
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
            stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 1, result.stderr
        assert "refusing to start a shim that forwards to another shim" in result.stderr
        assert shim_address in result.stderr
        assert "launched" not in result.stdout
        assert "Starting model-alias shim" not in result.stderr
    finally:
        subprocess.run(["pkill", "-f", str(shim_copy)], check=False)


def test_nested_launch_forwards_to_the_gateway_not_the_parent_shim(
    tmp_path: Path,
) -> None:
    """A ccsession started inside a shim session forwards to the real gateway."""
    base = _free_local_port()
    parent_shim = f"http://127.0.0.1:{base + 3}"
    # A local gateway: loopback but not a shim port, so it is allowed.
    gateway = "http://127.0.0.1:9/cli"
    home = tmp_path / "home"
    home.mkdir()
    fake = tmp_path / "claude"
    fake.write_text(
        """#!/usr/bin/env python3
import json, os
print(json.dumps({k: os.environ.get(k, "") for k in
    ("ANTHROPIC_BASE_URL", "CCSESSION_GATEWAY_URL", "CCSESSION_SHIM_URL")}))
"""
    )
    fake.chmod(0o700)
    shim_copy = tmp_path / "nested-shim.py"
    shim_copy.write_text((SKILL_DIR / "local-gateway-alias-proxy.py").read_text())
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "CLAUDE_BIN": str(fake),
            # What a parent shim session exports.
            "ANTHROPIC_BASE_URL": parent_shim,
            "CCSESSION_SHIM_URL": parent_shim,
            "CCSESSION_GATEWAY_URL": gateway,
            "ANTHROPIC_AUTH_TOKEN": "t",
            "CC_SHIM_PORT": str(base),
            "CC_SHIM_SCRIPT": str(shim_copy),
            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
        }
    )
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--profile", "grok", "--shim"],
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
            stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, result.stderr
        seen = json.loads(result.stdout.strip().splitlines()[-1])
        own_shim = f"http://127.0.0.1:{base}"
        assert seen == {
            "ANTHROPIC_BASE_URL": own_shim,
            "CCSESSION_GATEWAY_URL": gateway,
            "CCSESSION_SHIM_URL": own_shim,
        }
        with urllib.request.urlopen(f"{own_shim}/__ccsession_shim", timeout=5) as r:
            assert json.loads(r.read())["upstream"] == gateway
    finally:
        subprocess.run(["pkill", "-f", str(shim_copy)], check=False)


def test_shim_refuses_its_own_address_as_upstream(tmp_path: Path) -> None:
    port = _free_local_port()
    env = os.environ.copy()
    env.update(
        {
            "GW_PROXY_UPSTREAM": f"http://127.0.0.1:{port}/cli",
            "GW_PROXY_PORT": str(port),
        }
    )
    result = subprocess.run(
        [sys.executable, str(SKILL_DIR / "local-gateway-alias-proxy.py")],
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 1
    assert "is this shim's own address" in result.stderr


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
    fake_source: str | None = None,
) -> tuple[subprocess.CompletedProcess[str], bool]:
    """Run ccsession on a saved label; return the finished process and whether the label stayed."""
    home = tmp_path / "home"
    work = tmp_path / "work"
    work.mkdir(parents=True)
    fake = tmp_path / "claude-args"
    fake.write_text(
        fake_source
        or "#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n"
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


@pytest.mark.parametrize(
    ("args", "transcript"),
    [
        (("-p", "x"), False),  # untagged
        (("demo",), False),  # new label
        (("demo",), True),  # resumed label
    ],
)
@pytest.mark.parametrize("zero_from", [None, "shell", "env_file"])
def test_every_launch_sets_bg_shell_pressure_reap_switch(
    tmp_path: Path,
    args: tuple[str, ...],
    transcript: bool,
    zero_from: str | None,
    monkeypatch,
) -> None:
    # Issue 765: Claude must start with the switch at 1, also when the shell or the
    # env file (CCSESSION_ENV_FILE, sourced before the export) had 0.
    # The stand-in records only this one variable, never the whole environment.
    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
    fake_source = (
        "#!/usr/bin/env python3\nimport json, os\n"
        "print(json.dumps(os.environ.get("
        "'CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP')))\n"
    )
    extra_env: dict[str, str] = {}
    if zero_from == "shell":
        extra_env["CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP"] = "0"
    elif zero_from == "env_file":
        env_file = tmp_path / "reap.env"
        env_file.write_text("export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=0\n")
        extra_env["CCSESSION_ENV_FILE"] = str(env_file)
    result, _ = _label_run(
        tmp_path,
        transcript=transcript,
        args=args,
        extra_env=extra_env,
        fake_source=fake_source,
    )
    assert json.loads(result.stdout.strip().splitlines()[-1]) == "1"


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
        "               'origin': os.environ.get('CCSESSION_ORIGIN'),\n"
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
            "CCSESSION_ORIGIN",
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
    # The commands that tell agent sessions from a person's (issue 638).
    for text in ("--agents", "--classify", "--mark", "--prune"):
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
        and k
        not in (
            "CLAUDE_TOPIC",
            "CCSESSION_TOPIC_CWD",
            "CLAUDE_ENV_FILE",
            "CCSESSION_ORIGIN",
        )
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


# A list belongs to a repo, so its heading is the repo's name. It used to be the
# folder in .cwd, which is only the worktree that wrote the list last.

REPO_URL = "https://github.com/Some-Org/my-repo.git"  # dashed: the key cannot be split


def _repo_list(tmp_path: Path):
    """main, a worktree, and the repo's one list with a session; its .cwd names
    the worktree, the last folder to write it."""
    main, worktree, projects, env = _named_repo(tmp_path)
    _git(main, "remote", "set-url", "origin", REPO_URL)
    topics = projects / "github.com-Some-Org-my-repo" / "topics"
    topics.mkdir(parents=True)
    _transcript(projects, worktree, SESSION_ID)
    (topics / "demo.txt").write_text(f"{SESSION_ID}\n")
    (topics / ".cwd").write_text(f"{worktree}\n")
    return main, worktree, projects, topics, env


def _heading(out: str) -> str:
    return next(line for line in out.splitlines() if line.strip())


def test_list_heads_a_repo_list_with_the_repo_name_not_a_worktree(
    tmp_path: Path,
) -> None:
    main, worktree, _, _, env = _repo_list(tmp_path)
    for folder in (main, worktree):
        out = _ccs(folder, env, "--list").stdout
        assert _heading(out) == "my-repo"
        assert "wt-feature" not in out.split("  demo")[0]


def test_here_shows_the_repo_name_and_this_worktree(tmp_path: Path) -> None:
    main, worktree, _, _, env = _repo_list(tmp_path)
    assert _heading(_ccs(main, env, "--here").stdout) == "my-repo  (worktree: repo)"
    assert (
        _heading(_ccs(worktree, env, "--here").stdout)
        == "my-repo  (worktree: wt-feature)"
    )
    # Every worktree's sessions are listed under the repo alone.
    assert _heading(_ccs(worktree, env, "--here", "--all").stdout) == "my-repo"


def test_the_repo_name_stays_after_its_worktrees_are_gone(tmp_path: Path) -> None:
    main, worktree, _, topics, env = _repo_list(tmp_path)
    _launched(worktree, env, "second")  # a named launch writes .cwd and .repo
    assert (topics / ".repo").read_text() == "my-repo\n"
    assert (topics / ".cwd").read_text().strip() == str(worktree)
    _git(main, "worktree", "remove", "--force", str(worktree))
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert _heading(_ccs(elsewhere, env, "--list").stdout) == "my-repo"


def test_the_heading_is_found_for_a_list_written_before_repo_files_existed(
    tmp_path: Path,
) -> None:
    # No .repo yet: the folder in .cwd still is a checkout of the repo.
    _, _, _, topics, env = _repo_list(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert not (topics / ".repo").exists()
    assert _heading(_ccs(elsewhere, env, "--list").stdout) == "my-repo"


def test_lists_without_a_network_origin_keep_their_folder_heading(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _git(main, "remote", "remove", "origin")  # a local-only repo
    local = projects / str(main.resolve()).replace("/", "-") / "topics"
    local.mkdir(parents=True)
    _transcript(projects, main, SESSION_ID)
    (local / "local work.txt").write_text(f"{SESSION_ID}\n")
    (local / ".cwd").write_text(f"{main}\n")
    # An old per-folder list whose folder is gone.
    old = projects / str(tmp_path / "old-folder").replace("/", "-") / "topics"
    old.mkdir(parents=True)
    (old / "old.txt").write_text("99999999-0000-0000-0000-000000000000\n")
    (old / ".cwd").write_text(f"{tmp_path / 'old-folder'}\n")
    out = _ccs(main, env, "--list").stdout.splitlines()
    assert "repo" in out and "old-folder" in out
    assert _heading(_ccs(main, env, "--here").stdout) == "repo"
    assert not list(projects.glob("*/topics/.repo"))


def test_listing_never_writes_the_name_lists(tmp_path: Path) -> None:
    main, worktree, projects, topics, env = _repo_list(tmp_path)
    for args in (("--list",), ("--here",), ("--here", "--all")):
        _ccs(main, env, *args)  # the first run may mark the migration done

    def snapshot() -> dict[str, bytes]:
        return {
            str(p): p.read_bytes() for p in projects.glob("**/topics/*") if p.is_file()
        }

    before = snapshot()
    for folder in (main, worktree):
        for args in (("--list",), ("--here",), ("--here", "--all")):
            _ccs(folder, env, *args)
    assert snapshot() == before
    assert (topics / "demo.txt").read_text() == f"{SESSION_ID}\n"


# Claude Code deletes a saved conversation whose file was last changed more than
# cleanupPeriodDays days ago (default 30) and has no exemption for a named
# session, so retention.py raises the user's value and warns when it is low.

RETENTION = SKILL_DIR / "retention.py"


def _retention(tmp_path: Path, *args: str, managed: dict | None = None):
    home = tmp_path / "home"
    folder = tmp_path / "managed"
    if managed is not None:
        folder.mkdir(exist_ok=True)
        for name, content in managed.items():
            target = folder / name
            target.parent.mkdir(exist_ok=True)
            target.write_text(json.dumps(content))
    return subprocess.run(
        [sys.executable, str(RETENTION), *args],
        env={
            **os.environ,
            "HOME": str(home),
            "CCSESSION_MANAGED_SETTINGS_DIR": str(folder),
        },
        text=True,
        capture_output=True,
    )


def _user_settings(tmp_path: Path, content: object | None) -> Path:
    path = tmp_path / "home" / ".claude" / "settings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if content is not None:
        path.write_text(
            content if isinstance(content, str) else json.dumps(content, indent=2)
        )
    return path


@pytest.mark.parametrize(
    "before, after",
    [
        ({"theme": "dark"}, 90),  # key absent
        ({"theme": "dark", "cleanupPeriodDays": 30}, 90),  # lower
        ({"theme": "dark", "cleanupPeriodDays": 89}, 90),
        ({"theme": "dark", "cleanupPeriodDays": 90}, 90),  # equal
        ({"theme": "dark", "cleanupPeriodDays": 365}, 365),  # higher: kept
        ({"theme": "dark", "cleanupPeriodDays": 3650}, 3650),  # higher: kept
    ],
)
def test_retention_ensure_raises_a_low_value_and_keeps_a_high_one(
    tmp_path: Path, before: dict, after: int
) -> None:
    settings = _user_settings(tmp_path, before)
    raw = settings.read_bytes()
    result = _retention(tmp_path, "ensure", str(settings))
    assert result.returncode == 0, result.stderr
    saved = json.loads(settings.read_text())
    assert saved["cleanupPeriodDays"] == after
    assert saved["theme"] == "dark"  # everything else is kept
    backups = list(settings.parent.glob("settings.json.bak.*"))
    if after == before.get("cleanupPeriodDays", 0) and "cleanupPeriodDays" in before:
        assert settings.read_bytes() == raw and not backups  # untouched
    else:
        assert len(backups) == 1 and backups[0].read_bytes() == raw


def test_retention_ensure_creates_the_settings_file_when_there_is_none(
    tmp_path: Path,
) -> None:
    settings = _user_settings(tmp_path, None)
    assert _retention(tmp_path, "ensure", str(settings)).returncode == 0
    assert json.loads(settings.read_text()) == {"cleanupPeriodDays": 90}


@pytest.mark.parametrize(
    "content",
    ["{ not json", "[1, 2]", {"cleanupPeriodDays": "30"}, {"cleanupPeriodDays": True}],
)
def test_retention_ensure_leaves_a_file_it_cannot_judge_untouched(
    tmp_path: Path, content: object
) -> None:
    settings = _user_settings(tmp_path, content)
    raw = settings.read_bytes()
    result = _retention(tmp_path, "ensure", str(settings))
    # Exit 3: the value could not be raised, so a caller can report the line.
    assert result.returncode == 3 and "WARNING" in result.stdout
    assert settings.read_bytes() == raw
    assert not list(settings.parent.glob("settings.json.bak.*"))


def test_retention_ensure_never_writes_where_managed_settings_win(
    tmp_path: Path,
) -> None:
    settings = _user_settings(tmp_path, None)
    result = _retention(
        tmp_path,
        "ensure",
        str(settings),
        managed={"managed-settings.d/10-retention.json": {"cleanupPeriodDays": 60}},
    )
    assert result.returncode == 3
    assert "managed settings file" in result.stdout and "60" in result.stdout
    assert not settings.exists()


def test_retention_check_names_the_source_of_a_low_value(tmp_path: Path) -> None:
    settings = _user_settings(tmp_path, None)
    unset = _retention(tmp_path, "check", str(settings)).stdout
    assert "after 30 days" in unset and "Claude Code's default applies" in unset
    settings.write_text(json.dumps({"cleanupPeriodDays": 60}))
    user = _retention(tmp_path, "check", str(settings)).stdout
    assert "after 60 days" in user and "set in ~/.claude/settings.json" in user
    managed = _retention(
        tmp_path,
        "check",
        str(settings),
        managed={"managed-settings.d/10-retention.json": {"cleanupPeriodDays": 60}},
    ).stdout
    assert "after 60 days" in managed
    assert "10-retention.json" in managed and "cannot override" in managed
    assert "90 or more" in managed  # the target the advice names


def test_retention_check_is_silent_when_the_value_in_force_is_long_enough(
    tmp_path: Path,
) -> None:
    settings = _user_settings(tmp_path, {"cleanupPeriodDays": 3650})
    assert _retention(tmp_path, "check", str(settings)).stdout == ""
    # A managed value wins over a larger user value, in either direction.
    low_managed = {"managed-settings.json": {"cleanupPeriodDays": 60}}
    assert (
        "after 60 days"
        in _retention(tmp_path, "check", str(settings), managed=low_managed).stdout
    )
    # A managed 90 is the target itself: nothing to warn about.
    target = {"managed-settings.json": {"cleanupPeriodDays": 90}}
    assert _retention(tmp_path, "check", str(settings), managed=target).stdout == ""
    settings.write_text(json.dumps({"cleanupPeriodDays": 30}))
    long_managed = {"managed-settings.json": {"cleanupPeriodDays": 400}}
    assert (
        _retention(tmp_path, "check", str(settings), managed=long_managed).stdout == ""
    )


def test_retention_check_reads_managed_files_in_claude_codes_order(
    tmp_path: Path,
) -> None:
    # managed-settings.json first, then managed-settings.d/*.json alphabetically;
    # the last file that sets the key is the one in force.
    settings = _user_settings(tmp_path, None)
    managed = {
        "managed-settings.json": {"cleanupPeriodDays": 30},
        "managed-settings.d/10-a.json": {"cleanupPeriodDays": 400},
        "managed-settings.d/20-b.json": {"other": 1},
    }
    assert _retention(tmp_path, "check", str(settings), managed=managed).stdout == ""
    managed["managed-settings.d/30-c.json"] = {"cleanupPeriodDays": 45}
    out = _retention(tmp_path, "check", str(settings), managed=managed).stdout
    assert "after 45 days" in out and "30-c.json" in out


def test_list_warns_on_stderr_only_and_only_when_retention_is_short(
    tmp_path: Path,
) -> None:
    main, worktree, _, _, env = _repo_list(tmp_path)
    settings = _user_settings(tmp_path, None)
    for args in (("--list",), ("--here",)):
        short = _ccs(main, env, *args)
        assert "Claude Code deletes saved sessions after 30 days" in short.stderr
        assert "days" not in short.stdout  # the rows are as before
    settings.write_text(json.dumps({"cleanupPeriodDays": 89}))
    assert "after 89 days" in _ccs(main, env, "--list").stderr
    for days in (90, 365):  # the target and above: silent
        settings.write_text(json.dumps({"cleanupPeriodDays": days}))
        assert _ccs(main, env, "--list").stderr == ""
        assert _ccs(worktree, env, "--here").stderr == ""


@pytest.mark.parametrize(
    "before, after",
    [(None, 90), (30, 90), (89, 90), (90, 90), (365, 365), (3650, 3650)],
)
def test_install_sh_sets_retention_only_when_absent_or_lower(
    tmp_path: Path, before: int | None, after: int
) -> None:
    home = tmp_path / "home"
    settings = home / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    if before is not None:
        settings.write_text(json.dumps({"cleanupPeriodDays": before, "theme": "dark"}))
    env = {**os.environ, "HOME": str(home)}
    for _ in range(2):  # a second run changes nothing more
        run = subprocess.run(
            [str(SKILL_DIR / "install.sh")],
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
    saved = json.loads(settings.read_text())
    assert saved["cleanupPeriodDays"] == after
    assert "SessionStart" in saved["hooks"]  # the hook registration still happens
    assert "Session retention" in run.stdout
    if before is not None:
        assert saved["theme"] == "dark"


def test_install_sh_leaves_user_settings_alone_where_managed_settings_win(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    managed = tmp_path / "managed"
    managed.mkdir()
    (managed / "managed-settings.json").write_text('{"cleanupPeriodDays": 60}')
    env = {
        **os.environ,
        "HOME": str(home),
        "CCSESSION_MANAGED_SETTINGS_DIR": str(managed),
    }
    run = subprocess.run(
        [str(SKILL_DIR / "install.sh")],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    saved = json.loads((home / ".claude" / "settings.json").read_text())
    assert "cleanupPeriodDays" not in saved
    assert "managed settings file" in run.stdout


@pytest.mark.parametrize("days", [90, 365])
def test_retention_ensure_accepts_a_managed_value_that_is_long_enough(
    tmp_path: Path, days: int
) -> None:
    # Managed settings win and already keep sessions long enough (the 90-day
    # target or more): nothing to raise and nothing to warn about (exit 0), and
    # the user file is not created.
    settings = _user_settings(tmp_path, None)
    result = _retention(
        tmp_path,
        "ensure",
        str(settings),
        managed={"managed-settings.json": {"cleanupPeriodDays": days}},
    )
    assert result.returncode == 0
    assert "at least 90" in result.stdout and "managed settings file" in result.stdout
    assert not settings.exists()


def test_retention_target_is_90_days() -> None:
    # The installer's target and the warning threshold, in one place.
    assert re.search(r"^MIN_DAYS = 90$", RETENTION.read_text(), re.MULTILINE)


# The list is built in time that does not grow in processes started per saved name
# beyond a few fixed ones (issue 607). Counting shims stand first on PATH and log
# every call, then run the real tool; the tests run the real entry points.

_COUNTED_TOOLS = ("date", "stat", "head", "ls", "basename", "dirname", "grep", "awk")
_LISTINGS = (("--here",), ("--here", "--all"), ("--list",))


def _shims(
    tmp_path: Path, tools: tuple[str, ...] = _COUNTED_TOOLS
) -> tuple[Path, Path]:
    """Shims for the given tools, first on PATH: each appends
    "<tool> <LC_ALL or <unset>>|<arguments>" to the log, then runs the real tool."""
    shims = tmp_path / "shims"
    shims.mkdir()
    log = tmp_path / "shim-calls"
    log.touch()
    for tool in tools:
        real = shutil.which(tool)
        assert real, tool
        shim = shims / tool
        shim.write_text(
            "#!/bin/sh\n"
            f'printf \'%s %s|%s\\n\' {tool} "${{LC_ALL-<unset>}}" "$*" >> {log}\n'
            f'exec {real} "$@"\n'
        )
        shim.chmod(0o755)
    return shims, log


def _calls(log: Path) -> list[str]:
    return log.read_text().splitlines()


def _many_sessions(
    tmp_path: Path, n: int, *, transcripts: bool = True
) -> tuple[Path, Path, dict[str, str]]:
    """N saved names in the repo's list; each session's transcript sits under a
    per-folder store (three folders), not under the repo-keyed folder."""
    main, _, projects, env = _named_repo(tmp_path)
    env.pop("LC_ALL", None)
    topics = projects / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True)
    for i in range(n):
        session = f"{i:08x}-0000-0000-0000-000000000000"
        folder = main / f"d{i % 3}"
        folder.mkdir(exist_ok=True)
        if transcripts:
            _transcript(projects, folder, session)
        (topics / f"name {i:03d}.txt").write_text(f"{session}\n")
    return main, projects, env


@pytest.mark.parametrize(
    "args, per_row",
    [
        # one head, grep and awk per session find where it was started; the time
        # work is one stat and one date for each of its two times
        (("--here",), {"date": 2, "stat": 1, "head": 1, "grep": 1, "awk": 1}),
        (("--here", "--all"), {"date": 2, "stat": 1}),
        (("--list",), {"date": 2, "stat": 1}),
    ],
)
def test_listing_starts_a_fixed_number_of_processes_per_saved_name(
    tmp_path: Path, args: tuple[str, ...], per_row: dict[str, int]
) -> None:
    # The shell code, which the list falls back to where python3 is missing.
    counts: dict[int, Counter] = {}
    for n in (10, 60):
        sub = tmp_path / f"n{n}"
        sub.mkdir()
        main, _, env = _many_sessions(sub, n)
        shims, log = _shims(sub)
        env["PATH"] = f"{shims}:{_python_shim(sub, 'absent')}:{env['PATH']}"
        _ccs(main, env, *args)
        counts[n] = Counter(line.split(" ", 1)[0] for line in _calls(log))
    for tool in _COUNTED_TOOLS:
        # basename, dirname and ls (the transcript index) start none per name
        assert counts[60][tool] - counts[10][tool] == 50 * per_row.get(tool, 0), (
            tool,
            counts,
        )


def test_the_transcript_index_is_built_once_for_the_whole_list(tmp_path: Path) -> None:
    main, _, env = _many_sessions(tmp_path, 40)
    shims, log = _shims(tmp_path)
    env["PATH"] = f"{shims}:{_python_shim(tmp_path, 'absent')}:{env['PATH']}"
    rows = _listed(main, env, "--here")
    assert len(rows) == 40
    ls_calls = [c for c in _calls(log) if c.startswith("ls ") and ".jsonl" in c]
    # the one index (every transcript as an argument), and no ls per session
    assert [c.count(".jsonl") for c in ls_calls] == [40]


def test_an_empty_index_leaves_each_name_to_the_per_session_lookup(
    tmp_path: Path,
) -> None:
    main, _, env = _many_sessions(tmp_path, 5, transcripts=False)
    shims, log = _shims(tmp_path)
    env["PATH"] = f"{shims}:{_python_shim(tmp_path, 'absent')}:{env['PATH']}"
    out = _ccs(main, env, "--here").stdout
    assert out.count("(transcript missing)") == 5
    # the index (nothing matched) and one lookup for each name
    assert len([c for c in _calls(log) if c.startswith("ls ") and ".jsonl" in c]) == 6


def test_a_failing_ls_for_the_index_does_not_stop_the_listing(tmp_path: Path) -> None:
    main, _, env = _many_sessions(tmp_path, 4)
    shims = tmp_path / "failing"
    shims.mkdir()
    real = shutil.which("ls")
    (shims / "ls").write_text(
        f'#!/bin/sh\ncase "$*" in *.jsonl*) exit 2 ;; esac\nexec {real} "$@"\n'
    )
    (shims / "ls").chmod(0o755)
    env["PATH"] = f"{shims}:{_python_shim(tmp_path, 'absent')}:{env['PATH']}"
    result = _ccs(main, env, "--here")  # check=True: the exit code is 0 under set -e
    assert result.stdout.count("(transcript missing)") == 4


@pytest.mark.parametrize("user_locale", [None, "POSIX"])
def test_grep_and_awk_run_in_the_c_locale_whatever_the_users(
    tmp_path: Path, user_locale: str | None
) -> None:
    main, _, env = _many_sessions(tmp_path, 6)
    if user_locale:
        env["LC_ALL"] = user_locale
    shims, log = _shims(tmp_path, ("grep", "awk"))
    env["PATH"] = f"{shims}:{_python_shim(tmp_path, 'absent')}:{env['PATH']}"
    _ccs(main, env, "--here")
    seen = [c.split(" ", 1) for c in _calls(log)]
    assert len(seen) >= 12  # a grep and an awk for each session
    assert {rest.split("|")[0] for _, rest in seen} == {"C"}


def _date_shim(tmp_path: Path, flavour: str) -> tuple[Path, Path]:
    """A `date` of another family; its calls (arguments) are logged."""
    real = shutil.which("date")
    shims = tmp_path / f"date-{flavour}"
    shims.mkdir()
    log = tmp_path / f"date-{flavour}-calls"
    log.touch()
    bodies = {
        # GNU: -r takes a file name, which an epoch is not
        "gnu": f'exec {real} "$@"\n',
        # BSD: no --version, no -d @epoch, -r takes the epoch
        "bsd": (
            'case "$1" in\n'
            "  --version) exit 1 ;;\n"
            f'  -r) shift; e=$1; shift; exec {real} -d "@$e" "$@" ;;\n'
            "  *) exit 1 ;;\n"
            "esac\n"
        ),
        # busybox: no --version, no -r <epoch>, -d @epoch works
        "busybox": (
            'case "$1" in\n'
            "  --version) exit 1 ;;\n"
            "  -r) exit 1 ;;\n"
            f'  -d) exec {real} "$@" ;;\n'
            "  *) exit 1 ;;\n"
            "esac\n"
        ),
    }
    (shims / "date").write_text(f'#!/bin/sh\necho "$*" >> {log}\n' + bodies[flavour])
    (shims / "date").chmod(0o755)
    return shims, log


@pytest.mark.parametrize("flavour", ["gnu", "bsd", "busybox"])
def test_the_date_text_is_the_same_for_every_date_flavour(
    tmp_path: Path, flavour: str
) -> None:
    main, _, env = _many_sessions(tmp_path, 4)
    reference = _ccs(main, env, "--here").stdout
    assert "started 20" in reference
    shims, log = _date_shim(tmp_path, flavour)
    env["PATH"] = f"{shims}:{env['PATH']}"
    assert _ccs(main, env, "--here").stdout == reference
    calls = _calls(log)
    flags = [c.split(" ", 1)[0] for c in calls if not c.startswith("--version")]
    if flavour == "gnu":
        assert "-r" not in flags  # no failing `date -r <epoch>` first
        assert flags and set(flags) == {"-d"}
    elif flavour == "bsd":
        assert flags and set(flags) == {"-r"}  # the BSD order is kept
    else:
        # -r first (it fails), then -d, for every time
        assert flags and flags[0::2] == ["-r"] * (len(flags) // 2)
        assert flags[1::2] == ["-d"] * (len(flags) // 2)
    assert sum(c.startswith("--version") for c in calls) == 1  # probed once


@pytest.mark.parametrize(
    "path", ["/home/u/.claude/projects/-a-b/abc.jsonl", "/p/topics/two words.txt"]
)
def test_parameter_expansions_give_what_basename_and_dirname_gave(path: str) -> None:
    script = (
        "p=$1; d=${p%/*}; b=${p##*/}; s=${d##*/}\n"
        '[ "$d" = "$(dirname "$p")" ] || exit 1\n'
        '[ "$b" = "$(basename "$p")" ] || exit 2\n'
        '[ "$s" = "$(basename "$(dirname "$p")")" ] || exit 3\n'
        '[ "${b%.txt}" = "$(basename "$p" .txt)" ] || exit 4\n'
    )
    assert subprocess.run(["bash", "-c", script, "x", path]).returncode == 0


def test_an_unreadable_topic_file_shows_no_session_and_not_the_previous_one(
    tmp_path: Path,
) -> None:
    if os.geteuid() == 0:
        pytest.skip("root can read a mode 000 file")
    main, projects, env = _many_sessions(tmp_path, 3)
    bad = projects / "github.com-Org-Repo" / "topics" / "name 001.txt"
    bad.chmod(0)
    try:
        result = _ccs(main, env, "--here")  # check=True: exit 0 under set -e
    finally:
        bad.chmod(0o644)
    rows = {
        line.split("  ")[1].strip(): line
        for line in result.stdout.splitlines()
        if line.startswith("  name ")
    }
    assert "(transcript missing)" in rows["name 001"]
    assert "00000000" not in rows["name 001"]  # the row before it
    assert rows["name 000"].rstrip().endswith("00000000")
    assert rows["name 002"].rstrip().endswith("00000002")


def test_an_empty_list_and_a_one_name_list(tmp_path: Path) -> None:
    (tmp_path / "empty").mkdir()
    empty, _, env = _many_sessions(tmp_path / "empty", 0)
    result = _ccs(empty, env, "--here")  # check=True: exit 0
    assert "No labeled sessions" in result.stdout
    (tmp_path / "one").mkdir()
    one, _, env1 = _many_sessions(tmp_path / "one", 1)
    assert _listed(one, env1, "--here") == {"name 000": "00000000"}


def test_listing_creates_and_changes_no_file_in_home_or_tmp(tmp_path: Path) -> None:
    main, projects, env = _many_sessions(tmp_path, 6)
    tmp = tmp_path / "tmpdir"
    tmp.mkdir()
    env["TMPDIR"] = str(tmp)
    home = projects.parent.parent
    for args in _LISTINGS:
        _ccs(main, env, *args)  # the first run may mark the migration done

    def snapshot() -> dict[str, tuple[int, int]]:
        return {
            str(p): (p.stat().st_size, p.stat().st_mtime_ns)
            for root in (home, tmp)
            for p in root.rglob("*")
            if p.is_file()
        }

    before = snapshot()
    for args in _LISTINGS:
        _ccs(main, env, *args)
    assert snapshot() == before
    assert list(tmp.iterdir()) == []


_BASH4_CONSTRUCTS = [
    r"\b(declare|typeset|local)\s+-[a-zA-Z]*A",
    r"\b(mapfile|readarray|coproc)\b",
    r"printf\s+['\"]%\(",
    r"\$\{[^}]*(,,|\^\^)[^}]*\}",
    r"&>>|\|&|;;&|;&",
]


def test_the_listing_code_uses_no_bash_4_construct() -> None:
    # macOS ships bash 3.2 and no test runs under it, so the changed code is read.
    text = (SKILL_DIR / "ccsession").read_text()
    regions = [
        ("session_home() {", "git_here() ("),
        ("probe_date() {", "format_duration() {"),
        ("list_sessions() {", "retention_warning() {"),
    ]
    for start, end in regions:
        region = text[text.index(start) : text.index(end)]
        code = "\n".join(
            line for line in region.splitlines() if not line.lstrip().startswith("#")
        )
        for pattern in _BASH4_CONSTRUCTS:
            assert not re.search(pattern, code), (start, pattern)


# Stage 2 of issue 607: scan_sessions.py finds every transcript and start folder of a
# list in one python3 process. The list must read the same with it, without it (python3
# not found, or a helper that fails or answers short) and before the helper existed.

HELPER = SKILL_DIR / "scan_sessions.py"
_HEAD, _TAIL = 262144, 1048576


def _python_shim(tmp_path: Path, mode: str) -> Path:
    """A `python3` first on PATH. A call of the helper is logged. Then it runs the
    real python3 ("spy"), is not found ("absent", every call), exits 1 ("fails",
    helper only) or answers one empty record ("short", helper only)."""
    shims = tmp_path / f"python3-{mode}"
    shims.mkdir(exist_ok=True)
    log = tmp_path / f"python3-{mode}-calls"
    log.touch()
    real = f'exec {sys.executable} "$@"\n'
    helper_only = {"fails": "exit 1", "short": "printf '\\037\\037\\n'; exit 0"}
    body = {"spy": real, "absent": "exit 127\n"}.get(mode) or (
        f'case "$1" in\n  *scan_sessions.py) {helper_only[mode]} ;;\nesac\n{real}'
    )
    (shims / "python3").write_text(
        f'#!/bin/sh\ncase "$1" in *scan_sessions.py) echo "$*" >> {log} ;; esac\n'
        + body
    )
    (shims / "python3").chmod(0o755)
    return shims


def _quiet_retention(env: dict[str, str]) -> None:
    """A retention long enough that its warning (printed through python3) stays off,
    so that stderr can be compared with and without python3."""
    settings = Path(env["HOME"]) / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps({"cleanupPeriodDays": 400}))


def _run_bytes(cwd: Path, env: dict[str, str], *args: str) -> tuple[bytes, bytes, int]:
    done = subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        stdin=subprocess.DEVNULL,
    )
    return done.stdout, done.stderr, done.returncode


def _ask_screen(cwd: Path, env: dict[str, str]) -> str:
    """What `ccsession --ask` shows (the worktree list) before its question."""
    question = "Session name (q): "
    proc, master = _spawn_on_pty(
        [str(SKILL_DIR / "ccsession"), "--ask", "q"], env, cwd, stdout=subprocess.PIPE
    )
    try:
        shown = _read_pty(master, until=question)
        os.write(master, b"\r")
        proc.wait(timeout=60)
        return shown
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)


def _same_with_and_without_the_helper(
    tmp_path: Path, cwd: Path, env: dict[str, str], *, rows: bool = True
) -> dict[tuple[str, ...], bytes]:
    """Every view, byte for byte (stdout, stderr, exit code), with the helper and with
    python3 not found; the helper must have been called when there are rows (a list
    without rows never asks it). Returns the standard output of each view."""
    _quiet_retention(env)
    spy = {**env, "PATH": f"{_python_shim(tmp_path, 'spy')}:{env['PATH']}"}
    gone = {**env, "PATH": f"{_python_shim(tmp_path, 'absent')}:{env['PATH']}"}
    shown: dict[tuple[str, ...], bytes] = {}
    for args in _LISTINGS:
        with_helper = _run_bytes(cwd, spy, *args)
        assert with_helper == _run_bytes(cwd, gone, *args), args
        shown[args] = with_helper[0]
    called = (tmp_path / "python3-spy-calls").read_text().strip()
    assert bool(called) == rows, "the helper is asked for a list with rows only"
    assert _ask_screen(cwd, spy) == _ask_screen(cwd, gone)
    return shown


def _put(
    projects: Path, folder: str, session: str, data: bytes, mtime: int | None = None
) -> Path:
    store = projects / folder
    store.mkdir(parents=True, exist_ok=True)
    path = store / f"{session}.jsonl"
    path.write_bytes(data)
    if mtime is not None:
        os.utime(path, (mtime, mtime))
    return path


def _row(cwd: bytes | str) -> bytes:
    """One transcript line the way Claude Code writes it (compact JSON); a bytes cwd
    goes in as it is, JSON-escaped by hand for quote and backslash only."""
    if isinstance(cwd, str):
        cwd = json.dumps(cwd, ensure_ascii=False)[1:-1].encode("utf-8")
    else:
        cwd = cwd.replace(b"\\", b"\\\\").replace(b'"', b'\\"')
    return b'{"type":"user","cwd":"' + cwd + b'","sessionId":"s"}\n'


def _filler(n: int) -> bytes:
    """Exactly n bytes of lines without any folder in them."""
    return (b'{"p":"' + b"a" * 191 + b'"}\n') * (n // 200) + b"\n" * (n % 200)


def _store_name(cwd: bytes | str) -> str:
    """Claude Code's folder name for a cwd, taken byte by byte as ccsession does."""
    raw = cwd.encode() if isinstance(cwd, str) else cwd
    return re.sub(rb"[^A-Za-z0-9]", b"-", raw).decode("ascii")


def _sid(i: int) -> str:
    return f"{i:08x}-0000-0000-0000-000000000000"


def _name_list(projects: Path, *names: tuple[str, str]) -> Path:
    topics = projects / "github.com-Org-Repo" / "topics"
    topics.mkdir(parents=True, exist_ok=True)
    for name, session in names:
        # the file name of a saved name: "%" and "/" escaped (ccsession's name_to_file)
        fname = name.replace("%", "%25").replace("/", "%2F")
        (topics / f"{fname}.txt").write_text(f"{session}\n")
    return topics


@pytest.mark.parametrize(
    "case",
    [
        "missing",
        "other-folder",
        "two-copies",
        "repo-folder-wins",
        "names-with-escapes",
        "unreadable-topic",
        "empty-list",
        "one-name",
    ],
)
def test_the_helper_finds_the_same_transcripts_as_the_shell(
    tmp_path: Path, case: str
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    here = str(main)
    names: list[tuple[str, str]] = []
    if case == "missing":  # a name whose transcript is gone, and one that is there
        names = [("gone away", _sid(1)), ("present", _sid(2))]
        _put(projects, "-x", _sid(2), _row(here))
    elif case == "other-folder":
        names = [("one", _sid(1))]
        _put(projects, "-somewhere-else", _sid(1), _row(here))
    elif case == "two-copies":  # the newest copy is the one that counts
        names = [("both", _sid(1))]
        _put(projects, "-old-copy", _sid(1), _row("/nowhere"), mtime=1_700_000_000)
        _put(projects, "-new-copy", _sid(1), _row(here), mtime=1_790_000_000)
    elif case == "repo-folder-wins":  # the repo-keyed folder first, though older
        names = [("both", _sid(1))]
        _put(projects, "github.com-Org-Repo", _sid(1), _row(here), 1_700_000_000)
        _put(projects, "-newer-elsewhere", _sid(1), _row("/nowhere"), 1_790_000_000)
    elif case == "names-with-escapes":
        names = [
            ("my work/v2 50%", _sid(1)),
            ("-dash", _sid(2)),
            ("two  spaces", _sid(3)),
        ]
        for i in (1, 2, 3):
            _put(projects, "-x", _sid(i), _row(here))
    elif case == "unreadable-topic":
        if os.geteuid() == 0:
            pytest.skip("root can read a mode 000 file")
        names = [("fine", _sid(1)), ("locked", _sid(2))]
        for i in (1, 2):
            _put(projects, "-x", _sid(i), _row(here))
    elif case == "one-name":
        names = [("only", _sid(1))]
        _put(projects, "-x", _sid(1), _row(here))
    topics = _name_list(projects, *names)
    if case == "unreadable-topic":
        (topics / "locked.txt").chmod(0)
    try:
        shown = _same_with_and_without_the_helper(
            tmp_path, main, env, rows=case != "empty-list"
        )
    finally:
        if (topics / "locked.txt").exists():
            (topics / "locked.txt").chmod(0o644)
    if case == "empty-list":
        assert b"No labeled sessions" in shown[("--here",)]
    elif case == "missing":
        assert b"(transcript missing)" in shown[("--here",)]
    elif case in ("two-copies", "repo-folder-wins"):
        assert b"both" in shown[("--here",)]  # this worktree's, not "/nowhere"'s


def test_a_helper_that_fails_or_answers_short_leaves_the_list_unchanged(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _quiet_retention(env)
    for i in (1, 2, 3):
        _put(projects, "-x", _sid(i), _row(str(main)))
    _name_list(projects, *[(f"n{i}", _sid(i)) for i in (1, 2, 3)])
    gone = {**env, "PATH": f"{_python_shim(tmp_path, 'absent')}:{env['PATH']}"}
    reference = {args: _run_bytes(main, gone, *args) for args in _LISTINGS}
    for mode in ("fails", "short"):
        shimmed = {**env, "PATH": f"{_python_shim(tmp_path, mode)}:{env['PATH']}"}
        for args in _LISTINGS:
            assert _run_bytes(main, shimmed, *args) == reference[args], (mode, args)
        assert (tmp_path / f"python3-{mode}-calls").read_text().strip()


def test_the_helper_is_one_process_for_the_whole_list(tmp_path: Path) -> None:
    main, _, env = _many_sessions(tmp_path, 40)
    shims, log = _shims(tmp_path, ("grep", "awk", "head", "ls"))
    spy = _python_shim(tmp_path, "spy")
    env["PATH"] = f"{spy}:{shims}:{env['PATH']}"
    _ccs(main, env, "--here")
    assert len((tmp_path / "python3-spy-calls").read_text().splitlines()) == 1
    seen = Counter(line.split(" ", 1)[0] for line in _calls(log))
    # no grep, awk or head for a session, and no ls index: the helper did all of it
    assert seen["grep"] == seen["awk"] == seen["head"] == 0
    assert not [c for c in _calls(log) if c.startswith("ls ") and ".jsonl" in c]


@pytest.mark.parametrize("args", _LISTINGS)
def test_with_the_helper_a_listing_starts_two_dates_and_a_stat_per_saved_name(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    counts: dict[int, Counter] = {}
    for n in (10, 60):
        sub = tmp_path / f"n{n}"
        sub.mkdir()
        main, _, env = _many_sessions(sub, n)
        shims, log = _shims(sub)
        env["PATH"] = f"{_python_shim(sub, 'spy')}:{shims}:{env['PATH']}"
        _ccs(main, env, *args)
        counts[n] = Counter(line.split(" ", 1)[0] for line in _calls(log))
    for tool in _COUNTED_TOOLS:
        per_row = {"date": 2, "stat": 1}.get(tool, 0)
        assert counts[60][tool] - counts[10][tool] == 50 * per_row, (tool, counts)


def test_the_helper_writes_no_file(tmp_path: Path) -> None:
    main, projects, env = _many_sessions(tmp_path, 8)
    tmp = tmp_path / "tmpdir"
    tmp.mkdir()
    home = projects.parent.parent

    def snapshot() -> dict[str, tuple[int, int]]:
        return {
            str(p): (p.stat().st_size, p.stat().st_mtime_ns)
            for root in (home, tmp)
            for p in root.rglob("*")
            if p.is_file()
        }

    before = snapshot()
    done = subprocess.run(
        [
            sys.executable,
            str(HELPER),
            str(projects),
            str(projects / "github.com-Org-Repo"),
            *[_sid(i) for i in range(8)],
        ],
        env={**env, "TMPDIR": str(tmp)},
        capture_output=True,
        check=True,
    )
    assert done.stdout.count(b"\n") == 8
    assert snapshot() == before and list(tmp.iterdir()) == []


@pytest.mark.parametrize(
    "case",
    [
        "tail-only",
        "first-cwd-no-match",
        "escaped-quote-and-backslash",
        "non-ascii",
        "invalid-utf8",
        "small-file",
        "unread-middle",
        "straddles-the-head-cut",
        "straddles-the-head-cut-big-file",
        "tail-starts-mid-line",
        "nul-byte",
    ],
)
def test_the_helper_finds_the_same_start_folder_as_the_shell(
    tmp_path: Path, case: str
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    target: bytes | str = str(tmp_path / "removed worktree")  # never made: removed
    store = None
    if case == "tail-only":  # the folder is only in the last 1 MiB of a long file
        row = _row(target)
        data = _row("/not/it") + _filler(1_500_000) + row
    elif case == "first-cwd-no-match":  # none matches the folder: the first one
        data = _row("/first/one") + _row("/second/one")
        store = "-matches-nothing"
    elif case == "escaped-quote-and-backslash":
        target = b'/tmp/quote"and\\backslash dir'
        data = _row(target)
    elif case == "non-ascii":
        target = "/tmp/café ünï 日本"
        data = _row(target)
    elif case == "invalid-utf8":
        target = b"/tmp/bad\xff\xfebytes"
        data = _row(target)
    elif case == "small-file":
        data = _row(target)
    elif case == "unread-middle":  # the middle of a long file is never read
        data = (
            _row("/head/cwd")
            + _filler(400_000)
            + _row(target)
            + _filler(1_400_000)
            + _row("/tail/cwd")
        )
    elif case == "straddles-the-head-cut":  # the tail covers the whole short file
        data = _filler(_HEAD - 30) + _row(target) + _filler(300_000)
    elif case == "straddles-the-head-cut-big-file":  # out of reach of the tail too
        data = _row("/head/cwd") + _filler(_HEAD - 30) + _row(target)
        data += _filler(2_000_000)
    elif case == "tail-starts-mid-line":
        row = _row(target)
        head = _row("/head/cwd") + _filler(500_000)
        data = head + row + _filler(_TAIL + 18 - len(row))  # the cut is inside the row
    elif case == "nul-byte":  # grep would call this text binary: the shell decides
        data = _row(target) + b"\0" + _row("/later")
    _put(projects, store or _store_name(target), _sid(1), data)
    _put(projects, "-x", _sid(2), _row(str(main)))  # and a session that is here
    _name_list(projects, ("probe", _sid(1)), ("here", _sid(2)))
    shown = _same_with_and_without_the_helper(tmp_path, main, env)
    assert b"probe" in shown[("--here",)] or case in ("first-cwd-no-match",)


def test_a_birth_time_of_zero_still_reads_times_unavailable(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _put(projects, "-x", _sid(1), _row(str(main)))
    _name_list(projects, ("old fs", _sid(1)))
    real = shutil.which("stat")
    shims = tmp_path / "stat0"
    shims.mkdir()
    (shims / "stat").write_text(
        f'#!/bin/sh\ncase "$*" in\n  *%W*) shift 2; exec {real} -c \'0 %Y\' "$@" ;;\nesac\n'
        f'exec {real} "$@"\n'
    )
    (shims / "stat").chmod(0o755)
    env["PATH"] = f"{shims}:{env['PATH']}"
    shown = _same_with_and_without_the_helper(tmp_path, main, env)
    assert b"(times unavailable)" in shown[("--here",)]


def test_scan_sessions_ships_in_the_skill_folder_that_installers_copy() -> None:
    assert HELPER.is_file() and (SKILL_DIR / "retention.py").is_file()
    assert HELPER.parent == SKILL_DIR


# --- origin marker (issue 638) ------------------------------------------------
# Who chose a session's name is written next to the name list, when the name is
# saved: <list>/.origin/<session id> holds "human" or "agent". Only the hook's
# --sync-name (given --event) and --mark write one. "agent" is written in exactly
# one place: a new session (SessionStart, source startup) from an agent launch.

ORIGIN_LIST = "github.com-Org-Repo"
OTHER_SESSION = "def67890-0000-0000-0000-000000000000"


def _marker(
    projects: Path, session: str = SESSION_ID, list_name: str = ORIGIN_LIST
) -> str | None:
    path = projects / list_name / "topics" / ".origin" / session
    return path.read_text().strip() if path.is_file() else None


def _sync(
    cwd: Path,
    env: dict[str, str],
    session: str,
    name: str,
    *opts: str,
    keep: str = "",
) -> subprocess.CompletedProcess:
    """ccsession --sync-name as the hook runs it: options after a literal --."""
    args = ["--sync-name", session, name]
    if keep:
        args.append(keep)
    if opts:
        args += ["--", *opts]
    return _ccs(cwd, env, *args)


def _sync_opts(event: str, source: str | None, origin: str | None) -> list[str]:
    opts = ["--event", event]
    if source:
        opts += ["--source", source]
    if origin:
        opts += ["--origin", origin]
    return opts


def test_sync_name_without_an_event_writes_no_marker(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    # The import and dot-label paths call sync_name with no --event: whatever
    # CCSESSION_ORIGIN holds in the environment, no marker is written.
    agent_env = {**env, "CCSESSION_ORIGIN": "agent"}
    _sync(main, agent_env, SESSION_ID, "demo")
    assert _marker(projects) is None
    assert (projects / ORIGIN_LIST / "topics" / "demo.txt").is_file()


@pytest.mark.parametrize(
    ("event", "source", "origin", "expected"),
    [
        ("SessionStart", "startup", "agent", "agent"),
        ("SessionStart", "startup", "human", "human"),
        ("SessionStart", "startup", None, None),
        ("SessionStart", "resume", "agent", None),
        ("SessionStart", "resume", "human", None),
        ("SessionStart", "clear", "agent", None),
        ("SessionStart", "compact", "agent", None),
        ("SessionStart", None, "agent", None),
        ("UserPromptSubmit", None, "agent", "human"),
        ("UserPromptSubmit", None, None, "human"),
        ("SessionEnd", None, "agent", "human"),
        ("SessionEnd", None, None, "human"),
    ],
)
def test_agent_is_written_in_one_place_only(
    tmp_path: Path,
    event: str,
    source: str | None,
    origin: str | None,
    expected: str | None,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    # A session with a name that is new for it, and no marker yet.
    _sync(main, env, SESSION_ID, "demo", *_sync_opts(event, source, origin))
    assert _marker(projects) == expected


@pytest.mark.parametrize(
    ("event", "source", "origin", "expected"),
    [
        ("SessionStart", "startup", "human", "agent"),  # a marker is never replaced
        ("SessionStart", "resume", "human", "agent"),
        ("SessionStart", "resume", "agent", "agent"),
        ("UserPromptSubmit", None, "human", "agent"),  # same name: nothing new
        ("SessionEnd", None, "human", "agent"),
    ],
)
def test_an_existing_marker_is_not_changed_by_a_name_it_already_has(
    tmp_path: Path, event: str, source: str | None, origin: str | None, expected: str
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _sync(
        main, env, SESSION_ID, "demo", *_sync_opts("SessionStart", "startup", "agent")
    )
    assert _marker(projects) == "agent"
    _sync(main, env, SESSION_ID, "demo", *_sync_opts(event, source, origin))
    assert _marker(projects) == expected


def test_a_rename_writes_human_over_agent_and_the_same_name_again_changes_nothing(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _sync(
        main, env, SESSION_ID, "auto", *_sync_opts("SessionStart", "startup", "agent")
    )
    assert _marker(projects) == "agent"
    # /rename: a name that is new for the session, seen at a prompt, with no origin
    # at all (a Claude Code that ccsession did not start gives none).
    _sync(main, env, SESSION_ID, "mine", "--event", "UserPromptSubmit")
    assert _marker(projects) == "human"
    # The same name again, even over a marker set back to agent, changes nothing.
    _ccs(main, env, "--mark", "mine", "agent")
    _sync(main, env, SESSION_ID, "mine", "--event", "UserPromptSubmit")
    assert _marker(projects) == "agent"


def test_a_list_clean_up_alone_never_decides_a_marker(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    topics = projects / ORIGIN_LIST / "topics"
    _sync(
        main, env, SESSION_ID, "demo", *_sync_opts("SessionStart", "startup", "agent")
    )
    # A second name file of the same session (what migration can leave behind):
    # --check-others removes it, and that is not a rename.
    (topics / "old-copy.txt").write_text(SESSION_ID + "\n")
    _sync(
        main,
        env,
        SESSION_ID,
        "demo",
        *_sync_opts("SessionStart", "resume", "agent"),
        keep="--check-others",
    )
    assert not (topics / "old-copy.txt").exists()
    assert _marker(projects) == "agent"


def test_a_rename_in_another_repos_list_is_human_and_the_first_list_is_untouched(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    (tmp_path / "b").mkdir()
    other_main, _ = _repo_with_worktree(tmp_path / "b", "https://github.com/Org/Other")
    other_list = "github.com-Org-Other"
    _transcript(projects, main, SESSION_ID)
    _sync(
        main, env, SESSION_ID, "auto", *_sync_opts("SessionStart", "startup", "agent")
    )
    # The folder moved into repo B and the person renamed the session there.
    _sync(other_main, env, SESSION_ID, "mine", "--event", "UserPromptSubmit")
    assert _marker(projects, list_name=other_list) == "human"
    assert _marker(projects) == "agent"
    # Seen again from the first repo's folder, the name is one the session already
    # has in the other list: no write, so the human marker is not undone.
    _sync(main, env, SESSION_ID, "mine", "--event", "UserPromptSubmit")
    assert _marker(projects, list_name=other_list) == "human"
    assert _marker(projects) == "agent"


def test_a_collision_suffixed_own_name_in_another_list_is_not_new(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    (tmp_path / "b").mkdir()
    other_main, _ = _repo_with_worktree(tmp_path / "b", "https://github.com/Org/Other")
    other_list = projects / "github.com-Org-Other" / "topics"
    _transcript(projects, main, SESSION_ID)
    _transcript(projects, other_main, OTHER_SESSION)
    # Repo B already has "mine" for another session, so this session's own copy
    # there is "mine-2".
    _sync(other_main, env, OTHER_SESSION, "mine")
    _sync(other_main, env, SESSION_ID, "mine")
    assert (other_list / "mine-2.txt").read_text().strip() == SESSION_ID
    _sync(
        main, env, SESSION_ID, "auto", *_sync_opts("SessionStart", "startup", "agent")
    )
    # In repo A the title "mine" is new for the list but the session already has
    # it (as mine-2) in repo B: not a rename.
    _sync(main, env, SESSION_ID, "mine", "--event", "UserPromptSubmit")
    assert _marker(projects) == "agent"


def test_mark_sets_a_marker_both_ways_and_reports_its_errors(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _sync(main, env, SESSION_ID, "demo")
    assert _ccs(main, env, "--mark", "demo", "human").stdout.strip() == (
        "Marked 'demo' as human."
    )
    assert _marker(projects) == "human"
    _ccs(main, env, "--mark", "demo", "agent")
    assert _marker(projects) == "agent"

    def run(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(SKILL_DIR / "ccsession"), "--mark", *args],
            cwd=main,
            env=env,
            text=True,
            capture_output=True,
        )

    assert run("nothing-by-that-name", "human").returncode == 1
    assert run("demo", "maybe").returncode == 2
    assert run("demo").returncode == 2
    assert _marker(projects) == "agent"
    # The command adds only the .origin folder to the list: the name file is
    # untouched and no other name file appears.
    topics = projects / ORIGIN_LIST / "topics"
    assert {p.name for p in topics.glob("*.txt")} == {"demo.txt"}
    assert (topics / ".origin").is_dir()


def test_an_origin_folder_does_not_change_what_a_listing_shows(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _transcript(projects, main, SESSION_ID)
    _sync(main, env, SESSION_ID, "demo")
    before = _ccs(main, env, "--here", "--all").stdout
    _ccs(main, env, "--mark", "demo", "human")
    assert (projects / ORIGIN_LIST / "topics" / ".origin" / SESSION_ID).is_file()
    assert _ccs(main, env, "--here", "--all").stdout == before


def test_import_and_migration_paths_write_no_marker(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    # A name given with /rename before ccsession kept names: a custom-title line.
    _transcript(projects, main, SESSION_ID, "given-by-a-person")
    agent_env = {**env, "CCSESSION_ORIGIN": "agent"}
    _ccs(main, agent_env, "--migrate-names")
    assert (projects / ORIGIN_LIST / "topics" / "given-by-a-person.txt").is_file()
    assert _marker(projects) is None


def test_a_session_saved_before_the_upgrade_stays_unmarked_when_an_agent_launch_resumes_it(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _transcript(projects, main, SESSION_ID)
    # Saved by an older ccsession: a name file and no marker.
    _sync(main, env, SESSION_ID, "mine")
    # A worker started with CCSESSION_NAME equal to the saved name resumes it; so
    # does /resume inside an agent launch. SessionStart reports source "resume".
    for origin in ("agent", "human"):
        _sync(
            main, env, SESSION_ID, "mine", *_sync_opts("SessionStart", "resume", origin)
        )
        _sync(main, env, SESSION_ID, "mine", "--event", "UserPromptSubmit")
    assert _marker(projects) is None
    assert _listed(main, env) == {"mine": SESSION_ID[:8]}


# --- who chose the name, handed to the hook (issue 638, Task 2) ---------------


def test_orca_hands_a_typed_name_over_as_human(tmp_path: Path) -> None:
    _, record = _orca_tty(tmp_path, keys="mine-by-hand\r")
    assert record["topic"] == "mine-by-hand"
    assert record["origin"] == "human"


def test_orca_enter_at_the_question_is_an_agent_name(tmp_path: Path) -> None:
    _, record = _orca_tty(tmp_path, keys="\r")
    assert AUTO_LABEL.match(record["topic"]), record["topic"]
    assert record["origin"] == "agent"


def test_orca_ccsession_name_and_a_carried_name_are_agent_names(tmp_path: Path) -> None:
    _, record = _orca_no_tty(tmp_path, CCSESSION_NAME="worker-a")
    assert record["topic"] == "worker-a"
    assert record["origin"] == "agent"
    _, record = _orca_no_tty(tmp_path, "--name", "carried-name")
    assert record["origin"] == "agent"


def test_orca_untagged_start_is_agent(tmp_path: Path) -> None:
    _, record = _orca_no_tty(tmp_path, CCSESSION_AUTOSTART="0")
    assert record["topic"] is None
    assert record["origin"] == "agent"


def test_orca_resume_hands_no_origin_over(tmp_path: Path) -> None:
    # An origin left in the environment (a person's, from an earlier launch) is
    # dropped by a resume; ccsession then falls back to its own default, which on
    # a launch with no terminal is agent. A resume writes no marker either way.
    _, record = _orca_no_tty(tmp_path, "--resume", SESSION_ID, CCSESSION_ORIGIN="human")
    assert record["origin"] == "agent"


def _origin_fake(tmp_path: Path, env: dict[str, str]) -> dict[str, str]:
    fake = tmp_path / "claude-origin"
    fake.write_text(
        "#!/usr/bin/env python3\nimport os\n"
        "print('ORIGIN=' + os.environ.get('CCSESSION_ORIGIN', 'unset'))\n"
    )
    fake.chmod(0o700)
    return {**env, "CLAUDE_BIN": str(fake)}


def test_ccsession_launch_origin_follows_terminal_and_claudecode(
    tmp_path: Path,
) -> None:
    main, _, _, env = _named_repo(tmp_path)
    env = _origin_fake(tmp_path, env)
    # No terminal: an agent's launch.
    assert "ORIGIN=agent" in _ccs(main, env, "demo").stdout
    # An origin handed over (by ccsession-orca) is kept when valid.
    assert (
        "ORIGIN=human"
        in _ccs(main, {**env, "CCSESSION_ORIGIN": "human"}, "demo").stdout
    )
    # An invalid one is ignored.
    assert (
        "ORIGIN=agent"
        in _ccs(main, {**env, "CCSESSION_ORIGIN": "bogus"}, "demo").stdout
    )

    def on_terminal(extra: dict[str, str]) -> str:
        proc, master = _spawn_on_pty(
            [str(SKILL_DIR / "ccsession"), "demo"], {**env, **extra}, main
        )
        try:
            output = _read_pty(master)
            assert proc.wait(timeout=60) == 0, output
        finally:
            if proc.poll() is None:
                proc.kill()
            os.close(master)
        return output

    # A person on a terminal.
    assert "ORIGIN=human" in on_terminal({})
    # An origin handed over stays whatever the terminal says.
    assert "ORIGIN=agent" in on_terminal({"CCSESSION_ORIGIN": "agent"})
    # Inside Claude Code, even on a terminal, and whatever was handed over.
    assert "ORIGIN=agent" in on_terminal({"CLAUDECODE": "1"})
    assert "ORIGIN=agent" in on_terminal(
        {"CLAUDECODE": "1", "CCSESSION_ORIGIN": "human"}
    )


def test_sync_name_with_claudecode_set_still_writes_the_given_origin(
    tmp_path: Path,
) -> None:
    # Claude Code sets CLAUDECODE for its hook processes, so --sync-name always
    # runs with it set: the launch rule must never reach this path.
    main, _, projects, env = _named_repo(tmp_path)
    env = {**env, "CLAUDECODE": "1"}
    _sync(
        main, env, SESSION_ID, "demo", *_sync_opts("SessionStart", "startup", "human")
    )
    assert _marker(projects) == "human"
    _sync(main, env, SESSION_ID, "renamed", "--event", "UserPromptSubmit")
    assert _marker(projects) == "human"
    _sync(
        main,
        env,
        OTHER_SESSION,
        "auto-one",
        *_sync_opts("SessionStart", "startup", "agent"),
    )
    assert _marker(projects, OTHER_SESSION) == "agent"


# --- the hook hands the origin to ccsession (issue 638, task 3) ---------------
# The hook passes the event, the source and the launch's origin after a literal
# "--", only for the Claude Code ccsession launched (or one it did not start).
# It never reads CLAUDECODE: Claude Code sets that for every hook process.


def _owner_env(env: dict[str, str], origin: str | None = None) -> dict[str, str]:
    """The environment of a hook run by the Claude Code ccsession launched."""
    out = {**env, "CCSESSION_LAUNCH_ID": f"{os.getpid()}.1"}
    if origin:
        out["CCSESSION_ORIGIN"] = origin
    return out


def test_hook_source_never_reads_claudecode() -> None:
    lines = (SKILL_DIR / "hooks" / "session-name.sh").read_text().splitlines()
    code = [x for x in lines if not x.lstrip().startswith("#")]
    assert not [x for x in code if "CLAUDECODE" in x]


@pytest.mark.parametrize("claudecode", [False, True])
@pytest.mark.parametrize("form", ["native", "standalone"])
@pytest.mark.parametrize("origin", ["agent", "human"])
def test_hook_new_session_of_the_launch_gets_the_launch_origin(
    tmp_path: Path, origin: str, form: str, claudecode: bool
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    env = _owner_env(env, origin)
    if claudecode:
        env["CLAUDECODE"] = "1"  # Claude Code sets it for hook processes
    topic = {**env, "CLAUDE_TOPIC": "auto-name", "CCSESSION_TOPIC_CWD": str(main)}
    _hook(topic, main, SESSION_ID, "SessionStart", form=form, source="startup")
    assert _marker(projects) == origin


@pytest.mark.parametrize("source", ["resume", "clear", "compact"])
def test_hook_start_that_is_not_a_new_session_writes_no_marker(
    tmp_path: Path, source: str
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    env = _owner_env(env, "agent")
    _hook(env, main, SESSION_ID, "SessionStart", source=source, session_title="demo")
    assert _marker(projects) is None
    assert (projects / ORIGIN_LIST / "topics" / "demo.txt").is_file()


def test_hook_start_without_a_source_writes_no_marker(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _hook(
        _owner_env(env, "agent"),
        main,
        SESSION_ID,
        "SessionStart",
        session_title="demo",
    )
    assert _marker(projects) is None


@pytest.mark.parametrize("claudecode", [False, True])
def test_hook_of_a_nested_claude_writes_no_marker(
    tmp_path: Path, claudecode: bool
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    env = _owner_env(env, "agent")
    if claudecode:
        env["CLAUDECODE"] = "1"
    # A claude started inside the launch is another process: not the owner.
    _hook(
        env,
        main,
        SESSION_ID,
        "SessionStart",
        nested=True,
        source="startup",
        session_title="inner",
    )
    _hook(env, main, SESSION_ID, "UserPromptSubmit", nested=True, session_title="in2")
    assert _marker(projects) is None


@pytest.mark.parametrize("claudecode", [False, True])
def test_hook_rename_after_an_untagged_start_marks_human(
    tmp_path: Path, claudecode: bool
) -> None:
    # Route 1: CCSESSION_AUTOSTART=0 starts the session with no name and no
    # marker; the person's /rename is picked up at the next prompt.
    main, _, projects, env = _named_repo(tmp_path)
    env = _owner_env(env, "agent")
    if claudecode:
        env["CLAUDECODE"] = "1"
    _hook(env, main, SESSION_ID, "SessionStart", source="startup")
    assert _marker(projects) is None
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="mine")
    assert _marker(projects) == "human"


@pytest.mark.parametrize("event", ["UserPromptSubmit", "SessionEnd"])
def test_hook_rename_of_an_agent_session_marks_it_human(
    tmp_path: Path, event: str
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    env = _owner_env(env, "agent")
    topic = {**env, "CLAUDE_TOPIC": "auto-name", "CCSESSION_TOPIC_CWD": str(main)}
    _hook(topic, main, SESSION_ID, "SessionStart", source="startup")
    assert _marker(projects) == "agent"
    fields = {"session_title": "my own name"}
    if event == "SessionEnd":
        fields = {
            "transcript_path": str(
                _transcript(projects, main, SESSION_ID, "my own name")
            )
        }
    _hook(env, main, SESSION_ID, event, **fields)
    assert _marker(projects) == "human"
    # A later prompt with the same name changes nothing.
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="my own name")
    assert _marker(projects) == "human"


def test_hook_rename_in_plain_claude_with_no_launch_marks_human(
    tmp_path: Path,
) -> None:
    # Claude Code not started by ccsession: no launch id, no origin. A rename is
    # still seen (OWNER is 1), and only a person renames.
    main, _, projects, env = _named_repo(tmp_path)
    assert "CCSESSION_LAUNCH_ID" not in env
    assert "CCSESSION_ORIGIN" not in env
    _hook(env, main, SESSION_ID, "SessionStart", source="startup")
    assert _marker(projects) is None
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="renamed")
    assert _marker(projects) == "human"


def test_hook_plain_claude_start_with_a_name_given_writes_no_origin(
    tmp_path: Path,
) -> None:
    # `claude --name x` outside ccsession: startup, a title, no origin handed over.
    main, _, projects, env = _named_repo(tmp_path)
    _hook(env, main, SESSION_ID, "SessionStart", source="startup", session_title="x")
    assert _marker(projects) is None
    assert (projects / ORIGIN_LIST / "topics" / "x.txt").is_file()


def test_hook_resume_keeps_the_marker_and_leaves_an_unmarked_session_alone(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    # An agent session resumed: stays agent, whatever the resume's launch says.
    first = _owner_env(env, "agent")
    topic = {**first, "CLAUDE_TOPIC": "auto-name", "CCSESSION_TOPIC_CWD": str(main)}
    _hook(topic, main, SESSION_ID, "SessionStart", source="startup")
    _hook(
        _owner_env(env, "human"),
        main,
        SESSION_ID,
        "SessionStart",
        source="resume",
        session_title="auto-name",
    )
    assert _marker(projects) == "agent"
    # A session saved before the upgrade (no marker) resumed: still no marker.
    topics = projects / ORIGIN_LIST / "topics"
    (topics / "old.txt").write_text(f"{OTHER_SESSION}\n")
    _hook(
        _owner_env(env, "agent"),
        main,
        OTHER_SESSION,
        "SessionStart",
        source="resume",
        session_title="old",
    )
    assert _marker(projects, OTHER_SESSION) is None


def test_hook_tab_reopen_without_an_origin_changes_no_marker(tmp_path: Path) -> None:
    # An Orca tab reopens its session: a resume, and ccsession-orca hands no
    # origin over. The marker stays as it was.
    main, _, projects, env = _named_repo(tmp_path)
    _orca_launch_env(tmp_path, env)
    topic = {
        **env,
        "CCSESSION_ORIGIN": "agent",
        "CLAUDE_TOPIC": "tab-name",
        "CCSESSION_TOPIC_CWD": str(main),
    }
    _hook(topic, main, SESSION_ID, "SessionStart", source="startup")
    assert _marker(projects) == "agent"
    reopened = {k: v for k, v in env.items() if k != "CCSESSION_ORIGIN"}
    _hook(reopened, main, SESSION_ID, "SessionStart", source="resume")
    assert _marker(projects) == "agent"


def test_hook_keeps_a_marker_set_by_mark(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    env = _owner_env(env, "agent")
    topic = {**env, "CLAUDE_TOPIC": "auto-name", "CCSESSION_TOPIC_CWD": str(main)}
    _hook(topic, main, SESSION_ID, "SessionStart", source="startup")
    assert _marker(projects) == "agent"
    _ccs(main, env, "--mark", "auto-name", "human")
    assert _marker(projects) == "human"
    # Neither the same name again nor a new start with an agent origin undoes it.
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="auto-name")
    _hook(topic, main, SESSION_ID, "SessionStart", source="startup")
    assert _marker(projects) == "human"


@pytest.mark.parametrize("claudecode", [False, True])
def test_hook_rename_seen_from_another_repos_folder_marks_human_there_only(
    tmp_path: Path, claudecode: bool
) -> None:
    # B1 route 2: an agent session saved under an auto-name in repo A; its folder
    # moved into repo B, where the person renamed it.
    main, _, projects, env = _named_repo(tmp_path)
    (tmp_path / "b").mkdir()
    other_main, _ = _repo_with_worktree(tmp_path / "b", "https://github.com/Org/Other")
    env = _owner_env(env, "agent")
    if claudecode:
        env["CLAUDECODE"] = "1"
    topic = {**env, "CLAUDE_TOPIC": "auto-name", "CCSESSION_TOPIC_CWD": str(main)}
    _hook(topic, main, SESSION_ID, "SessionStart", source="startup")
    assert _marker(projects) == "agent"
    other = "github.com-Org-Other"
    _hook(env, other_main, SESSION_ID, "UserPromptSubmit", session_title="mine")
    assert _marker(projects, list_name=other) == "human"
    assert _marker(projects) == "agent"
    # The same title seen again from repo A's folder is one the session already
    # has: nothing is written, and neither marker changes.
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="mine")
    assert _marker(projects, list_name=other) == "human"
    assert _marker(projects) == "agent"


def test_hook_same_name_again_in_plain_claude_writes_nothing_new(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="renamed")
    marker = projects / ORIGIN_LIST / "topics" / ".origin" / SESSION_ID
    assert marker.read_text().strip() == "human"
    before = marker.stat().st_mtime_ns
    _hook(env, main, SESSION_ID, "UserPromptSubmit", session_title="renamed")
    assert marker.stat().st_mtime_ns == before


# --- agent rows hidden in the lists (issue 638, tasks 4 and 5) -----------------
# A session whose marker is "agent" is left out of --list, --here and the new-tab
# question unless --agents (or "+" at the question) asks for it. Display only.


def _mark_session(env: dict[str, str], n: int, origin: str = "agent") -> None:
    """Write the origin marker for a session made by _add_session (same n)."""
    session = f"{n}{n}{n}{n}0000-0000-0000-0000-000000000000"
    folder = Path(env["HOME"]) / ".claude" / "projects" / ORIGIN_LIST / "topics"
    (folder / ".origin").mkdir(exist_ok=True)
    (folder / ".origin" / session).write_text(origin + "\n")


def _mixed_sessions(
    tmp_path: Path,
) -> tuple[Path, dict[str, str]]:
    """main with three sessions in its folder: agent, human and unmarked."""
    main, _, projects, env = _named_repo(tmp_path)
    (projects / ORIGIN_LIST / "topics").mkdir(parents=True)
    _add_session(env, main, 1, "auto one", "")
    _add_session(env, main, 2, "my work", "")
    _add_session(env, main, 3, "old one", "")
    _mark_session(env, 1, "agent")
    _mark_session(env, 2, "human")
    return main, env


@pytest.mark.parametrize(
    ("args", "command"),
    [
        (("--list",), "ccsession --list --agents"),
        (("--here",), "ccsession --here --agents"),
        (("--here", "--all"), "ccsession --here --all --agents"),
    ],
)
def test_lists_hide_agent_rows_and_say_how_many(
    tmp_path: Path, args: tuple[str, ...], command: str
) -> None:
    main, env = _mixed_sessions(tmp_path)
    out = _ccs(main, env, *args).stdout
    assert set(_listed(main, env, *args)) == {"my work", "old one"}
    assert out.rstrip().splitlines()[-1] == f"1 agent sessions hidden: {command}"


@pytest.mark.parametrize(
    "args",
    [
        ("--list", "--agents"),
        ("--here", "--agents"),
        ("--here", "--all", "--agents"),
        ("--here", "--agents", "--all"),
    ],
)
def test_agents_flag_shows_every_row_and_no_count_line(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    main, env = _mixed_sessions(tmp_path)
    out = _ccs(main, env, *args).stdout
    assert set(_listed(main, env, *args)) == {"auto one", "my work", "old one"}
    assert "hidden" not in out


def test_here_all_gives_the_same_output_in_either_flag_order(tmp_path: Path) -> None:
    main, env = _mixed_sessions(tmp_path)
    one = _ccs(main, env, "--here", "--all", "--agents").stdout
    two = _ccs(main, env, "--here", "--agents", "--all").stdout
    assert one == two


def test_a_list_without_markers_prints_as_before(tmp_path: Path) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    (projects / ORIGIN_LIST / "topics").mkdir(parents=True)
    _add_session(env, main, 1, "one", "")
    _add_session(env, main, 2, "two", "")
    out = _ccs(main, env, "--here").stdout
    assert "hidden" not in out
    assert set(_listed(main, env, "--here")) == {"one", "two"}


@pytest.mark.parametrize("args", [("--list",), ("--here",), ("--here", "--all")])
def test_all_rows_hidden_prints_no_heading_and_the_count_instead(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    (projects / ORIGIN_LIST / "topics").mkdir(parents=True)
    _add_session(env, main, 1, "auto one", "")
    _add_session(env, main, 2, "auto two", "")
    _mark_session(env, 1)
    _mark_session(env, 2)
    out = _ccs(main, env, *args).stdout
    lines = [x for x in out.splitlines() if x.strip()]
    assert len(lines) == 1
    assert lines[0].startswith("2 agent sessions hidden: ccsession ")
    assert "No labeled sessions" not in out


def test_a_list_of_only_agent_rows_gets_no_heading_while_others_keep_theirs(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    other = projects / "github.com-Org-Other" / "topics"
    other.mkdir(parents=True)
    _transcript(projects, main, OTHER_SESSION)
    (other / "bot.txt").write_text(f"{OTHER_SESSION}\n")
    (other / ".origin").mkdir()
    (other / ".origin" / OTHER_SESSION).write_text("agent\n")
    (projects / ORIGIN_LIST / "topics").mkdir(parents=True)
    _add_session(env, main, 1, "mine", "")
    out = _ccs(main, env, "--list").stdout
    assert "Other" not in out and "bot" not in out
    assert "mine" in out
    assert out.rstrip().splitlines()[-1] == (
        "1 agent sessions hidden: ccsession --list --agents"
    )
    shown = _ccs(main, env, "--list", "--agents").stdout
    assert "bot" in shown


def test_a_hidden_agent_row_of_another_worktree_is_not_an_other_worktree_session(
    tmp_path: Path,
) -> None:
    main, b, _, env = _three_worktrees(tmp_path)
    before = _ccs(b, env, "--here").stdout
    assert "2 more sessions in other worktrees of this repo" in before
    _mark_session(env, 1)  # "main work", a session of the other worktree
    after = _ccs(b, env, "--here").stdout
    assert "1 more session in other worktrees of this repo" in after
    assert "1 agent sessions hidden: ccsession --here --agents" in after
    # The agent view counts it again as another worktree's session.
    shown = _ccs(b, env, "--here", "--agents").stdout
    assert "2 more sessions in other worktrees of this repo" in shown


def test_a_hidden_session_still_resumes_by_name_and_can_be_removed(
    tmp_path: Path,
) -> None:
    main, env = _mixed_sessions(tmp_path)
    assert "auto one" not in _listed(main, env, "--here")
    assert _launched(main, env, "auto one")[-2:] == [
        "--resume",
        "11110000-0000-0000-0000-000000000000",
    ]
    _ccs(main, env, "--rm", "auto one")
    assert "auto one" not in _listed(main, env, "--here", "--agents")


def test_hiding_agent_rows_starts_no_process_per_row(tmp_path: Path) -> None:
    counts: dict[int, Counter] = {}
    for n in (10, 60):
        sub = tmp_path / f"n{n}"
        sub.mkdir()
        main, projects, env = _many_sessions(sub, n)
        origin = projects / ORIGIN_LIST / "topics" / ".origin"
        origin.mkdir()
        for i in range(0, n, 2):  # half of them are agent sessions
            (origin / f"{i:08x}-0000-0000-0000-000000000000").write_text("agent\n")
        shims, log = _shims(sub)
        env["PATH"] = f"{shims}:{_python_shim(sub, 'absent')}:{env['PATH']}"
        assert len(_listed(main, env, "--list")) == n // 2
        counts[n] = Counter(line.split(" ", 1)[0] for line in _calls(log))
    # The 25 more hidden rows cost nothing; the 25 more shown rows cost what a
    # shown row always did (two dates and one stat).
    assert counts[60]["date"] - counts[10]["date"] == 25 * 2
    assert counts[60]["stat"] - counts[10]["stat"] == 25 * 1
    for tool in ("head", "grep", "awk", "basename", "dirname"):
        assert counts[60][tool] == counts[10][tool], (tool, counts)


def test_name_question_hides_agent_rows_and_plus_lists_them(tmp_path: Path) -> None:
    _, b, _, env = _three_worktrees(tmp_path)
    _mark_session(env, 3)  # "b work"
    _mark_session(env, 1)  # "main work", another worktree's
    question = "Session name (q): "
    proc, master = _spawn_on_pty(
        [str(SKILL_DIR / "ccsession"), "--ask", "q"], env, b, stdout=subprocess.PIPE
    )
    try:
        first = _read_pty(master, until=question)
        assert "removed work" in first
        assert "b work" not in first
        assert "2 agent sessions hidden: type + to list them" in first
        assert "1 more session in other worktrees of this repo" in first
        os.write(master, b"+\r")
        more = _read_pty(master, until=question)
        assert "b work" in more and "removed work" in more
        assert "hidden" not in more
        # "+" is never a name: the question was asked again. A hidden session's
        # name still resumes it.
        os.write(master, b"b work\r")
        assert proc.wait(timeout=60) == 0
        assert proc.stdout.read() == b"b work\n"
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)


def test_name_question_with_only_agent_rows_shows_the_count_line_alone(
    tmp_path: Path,
) -> None:
    main, _, projects, env = _named_repo(tmp_path)
    (projects / ORIGIN_LIST / "topics").mkdir(parents=True)
    _add_session(env, main, 1, "auto one", "")
    _mark_session(env, 1)
    question = "Session name (q): "
    proc, master = _spawn_on_pty(
        [str(SKILL_DIR / "ccsession"), "--ask", "q"], env, main, stdout=subprocess.PIPE
    )
    try:
        first = _read_pty(master, until=question)
        assert "1 agent sessions hidden: type + to list them" in first
        assert "Saved sessions in" not in first
        os.write(master, b"\r")
        assert proc.wait(timeout=60) == 0
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)


# --- ccsession --classify (issue 638, task 7) ----------------------------------

CLASSIFY_LABEL = "demo-run-1118-150248-ab12"  # what --auto-name makes


def _tree(root: Path) -> dict[str, object]:
    """Every path under root with its content and time: a change shows."""
    seen: dict[str, object] = {}
    for path in sorted(root.rglob("*")):
        rel = str(path.relative_to(root))
        if path.is_symlink():
            seen[rel] = ("link", os.readlink(path))
        elif path.is_dir():
            seen[rel] = "dir"
        else:
            seen[rel] = (path.read_bytes(), path.stat().st_mtime_ns)
    return seen


def _classify_tree(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    main, _, projects, env = _named_repo(tmp_path)
    topics = projects / ORIGIN_LIST / "topics"
    topics.mkdir(parents=True)
    old = projects / "-home-me-old-folder" / "topics"  # an old per-folder list
    old.mkdir(parents=True)
    (topics / f"{CLASSIFY_LABEL}.txt").write_text(f"{SESSION_ID}\n")
    (old / f"{CLASSIFY_LABEL}.txt").write_text(f"{SESSION_ID}\n")
    (topics / "fix-1118-notes.txt").write_text(f"{OTHER_SESSION}\n")
    return main, env


def test_classify_dry_run_leaves_the_whole_home_untouched_and_prints_counts(
    tmp_path: Path,
) -> None:
    main, env = _classify_tree(tmp_path)
    home = Path(env["HOME"])
    before = _tree(home)
    out = _ccs(main, env, "--classify").stdout
    assert _tree(home) == before  # not even a migration stamp
    assert "Would mark agent: 2 session names" in out
    assert "Auto-named sessions: 1." in out and "not an auto-name): 1." in out
    assert "Dry run: nothing was written. Run with --apply to write the markers." in out


def test_classify_apply_marks_the_auto_named_session_everywhere_once(
    tmp_path: Path,
) -> None:
    main, env = _classify_tree(tmp_path)
    projects = Path(env["HOME"]) / ".claude" / "projects"
    out = _ccs(main, env, "--classify", "--apply").stdout
    assert "Marked agent: 2 session names" in out
    assert _marker(projects) == "agent"
    assert _marker(projects, list_name="-home-me-old-folder") == "agent"
    assert _marker(projects, OTHER_SESSION) is None  # a person's name: left alone
    before = _tree(Path(env["HOME"]))
    again = _ccs(main, env, "--classify", "--apply").stdout
    assert "Marked agent: 0 session names" in again
    assert _tree(Path(env["HOME"])) == before


def test_classified_sessions_leave_the_lists_until_agents_is_given(
    tmp_path: Path,
) -> None:
    main, env = _classify_tree(tmp_path)
    (Path(env["HOME"]) / ".claude" / "projects" / ORIGIN_LIST / "topics").mkdir(
        exist_ok=True
    )
    projects = Path(env["HOME"]) / ".claude" / "projects"
    _transcript(projects, main, SESSION_ID)
    _transcript(projects, main, OTHER_SESSION)
    assert set(_listed(main, env, "--here")) == {CLASSIFY_LABEL, "fix-1118-notes"}
    _ccs(main, env, "--classify", "--apply")
    assert set(_listed(main, env, "--here")) == {"fix-1118-notes"}
    assert set(_listed(main, env, "--here", "--agents")) == {
        CLASSIFY_LABEL,
        "fix-1118-notes",
    }


def test_classify_refuses_options_it_does_not_know(tmp_path: Path) -> None:
    main, env = _classify_tree(tmp_path)
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--classify", "--bogus"],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2 and "usage" in result.stderr


# --- ccsession --prune and the older-than hint (issue 638, task 8) -------------
# The pruner's own rules are in tests/unit/test_session_keep.py; these run it
# through the command, in a throwaway HOME.


def _agent_session(
    env: dict[str, str],
    folder: Path,
    n: int,
    name: str,
    days: float,
    origin: str | None = "agent",
) -> Path:
    """A saved session whose transcript last changed `days` days ago."""
    _add_session(env, folder, n, name, "")
    if origin:
        _mark_session(env, n, origin)
    session = f"{n}{n}{n}{n}0000-0000-0000-0000-000000000000"
    projects = Path(env["HOME"]) / ".claude" / "projects"
    (transcript,) = projects.glob(f"*/{session}.jsonl")
    when = time.time() - days * 86400
    os.utime(transcript, (when, when))
    return transcript


def _keep_a_year(env: dict[str, str]) -> None:
    """The limit Claude Code uses in the owner's workspace: 365 days."""
    settings = Path(env["HOME"]) / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps({"cleanupPeriodDays": 365}))


def _prune_tree(tmp_path: Path) -> tuple[Path, dict[str, str], dict[str, Path]]:
    main, _, projects, env = _named_repo(tmp_path)
    (projects / ORIGIN_LIST / "topics").mkdir(parents=True)
    _keep_a_year(env)
    sessions = {
        "agent old": _agent_session(env, main, 1, "agent old", 60),
        "agent new": _agent_session(env, main, 2, "agent new", 5),
        "mine old": _agent_session(env, main, 3, "mine old", 200, origin=None),
        "human old": _agent_session(env, main, 4, "human old", 200, origin="human"),
    }
    return main, env, sessions


def test_prune_dry_run_lists_candidates_and_writes_nothing_at_all(
    tmp_path: Path,
) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    before = _tree(Path(env["HOME"]))
    out = _ccs(main, env, "--prune").stdout
    assert _tree(Path(env["HOME"])) == before  # no migration stamp, no lock file
    assert "  agent old  last change " in out and "60 days old" in out
    assert "agent new" not in out and "mine old" not in out and "human old" not in out
    assert "Would delete 1 agent session " in out
    lines = out.splitlines()
    assert lines[-2].startswith(
        "LOWERS THE LIMIT: Claude Code keeps sessions 365 days here; this removes 1 "
        "agent sessions that are between 30 and 365 days old ("
    )
    assert lines[-1] == "Dry run: nothing was deleted. Run with --apply to delete."
    assert all(path.is_file() for path in sessions.values())


def test_prune_apply_deletes_only_the_old_agent_session_and_its_name(
    tmp_path: Path,
) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    projects = Path(env["HOME"]) / ".claude" / "projects"
    out = _ccs(main, env, "--prune", "--apply", "--yes").stdout
    assert "Deleted 1 agent session " in out and "Dry run" not in out
    assert not sessions["agent old"].exists()
    assert not (projects / ORIGIN_LIST / "topics" / "agent old.txt").exists()
    assert _marker(projects, "11110000-0000-0000-0000-000000000000") is None
    for survivor in ("agent new", "mine old", "human old"):
        assert sessions[survivor].is_file()
        assert (projects / ORIGIN_LIST / "topics" / f"{survivor}.txt").is_file()
    again = _ccs(main, env, "--prune", "--apply", "--yes").stdout
    assert "Deleted 0 agent sessions" in again


def test_prune_skips_the_running_session(tmp_path: Path) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    running = "11110000-0000-0000-0000-000000000000"
    out = _ccs(
        main, {**env, "CLAUDE_SESSION_ID": running}, "--prune", "--apply", "--yes"
    ).stdout
    assert "kept: agent old: this is the running session" in out
    assert sessions["agent old"].is_file()


@pytest.mark.parametrize(
    ("args", "env_days", "code"),
    [
        (["--days", "0"], None, 2),
        (["--days", "abc"], None, 2),
        (["--days", "29"], None, 2),
        ([], "abc", 2),
        ([], "29", 2),
        (["--days", "45"], "29", 2),
        (["--days", "30"], None, 0),
        (["--days", "45"], None, 0),
        ([], "45", 0),
    ],
)
def test_prune_refuses_days_below_30_and_deletes_nothing(
    tmp_path: Path, args: list[str], env_days: str | None, code: int
) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    if env_days is not None:
        env["CCSESSION_AGENT_KEEP_DAYS"] = env_days
    result = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--prune", "--apply", "--yes", *args],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
    )
    assert result.returncode == code, result.stderr
    if code == 2:
        assert "at least 30" in result.stderr and "nothing was deleted" in result.stderr
        assert all(path.is_file() for path in sessions.values())
    else:
        assert not sessions["agent old"].exists()  # 60 days is past 30 and 45


def test_prune_with_a_claude_code_limit_of_30_says_claude_code_deletes_first(
    tmp_path: Path,
) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    (Path(env["HOME"]) / ".claude" / "settings.json").unlink()  # the default, 30
    out = _ccs(main, env, "--prune", "--apply", "--yes").stdout
    assert "Claude Code already deletes saved sessions after 30 days here" in out
    assert "LOWERS THE LIMIT" not in out
    assert all(path.is_file() for path in sessions.values())


def test_listings_say_when_agent_sessions_are_past_the_days(tmp_path: Path) -> None:
    main, env, _ = _prune_tree(tmp_path)
    hint = (
        "1 agent sessions are older than 30 days: ccsession --prune shows what "
        "would be removed"
    )
    for args in (("--list",), ("--here",), ("--here", "--all")):
        out = _ccs(main, env, *args).stdout
        assert out.rstrip().splitlines()[-1] == hint, args
    # With nothing marked agent past the days the listings print what they always did.
    _ccs(main, env, "--mark", "agent old", "human")
    for args in (("--list",), ("--here",)):
        assert "older than" not in _ccs(main, env, *args).stdout


@pytest.mark.parametrize("bad", ["29", "abc", "0", "-4"])
def test_listings_and_the_question_never_fail_on_a_bad_keep_days(
    tmp_path: Path, bad: str
) -> None:
    main, env, _ = _prune_tree(tmp_path)
    env["CCSESSION_AGENT_KEEP_DAYS"] = bad
    for args in (("--list",), ("--here",), ("--here", "--all")):
        done = subprocess.run(
            [str(SKILL_DIR / "ccsession"), *args],
            cwd=main,
            env=env,
            text=True,
            capture_output=True,
        )
        assert done.returncode == 0 and done.stderr == "", (args, done.stderr)
        assert "older than 30 days" in done.stdout  # an invalid value counts as 30
    status, stdout, shown, _, _ = _ask_on_pty(
        tmp_path,
        [(0.3, b"\r")],
        env=_orca_env(tmp_path, CCSESSION_AGENT_KEEP_DAYS=bad),
    )
    assert (status, stdout) == (0, b"\n") and "rror" not in shown


def test_listings_are_unchanged_where_the_helper_is_missing(tmp_path: Path) -> None:
    main, env, _ = _prune_tree(tmp_path)
    plain = _ccs(main, env, "--here").stdout
    copy = tmp_path / "skill-copy"
    shutil.copytree(SKILL_DIR, copy, ignore=shutil.ignore_patterns("__pycache__"))
    (copy / "session_keep.py").unlink()
    done = subprocess.run(
        [str(copy / "ccsession"), "--here"],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
    )
    assert done.returncode == 0 and done.stderr == ""
    assert done.stdout == plain.replace(
        "1 agent sessions are older than 30 days: ccsession --prune shows what "
        "would be removed\n",
        "",
    )
    missing = subprocess.run(
        [str(copy / "ccsession"), "--prune"],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
    )
    assert missing.returncode == 1 and "session_keep.py is missing" in missing.stderr


def test_a_hidden_session_still_reopens_in_its_orca_tab(tmp_path: Path) -> None:
    main, env, _ = _prune_tree(tmp_path)
    session = "11110000-0000-0000-0000-000000000000"
    assert "agent old" not in _listed(main, env, "--here")  # hidden
    tabs = Path(env["HOME"]) / ".local" / "state" / "ccsession" / "orca-tabs"
    tabs.mkdir(parents=True)
    (tabs / "tab-1+leaf-1").write_text(f"{session}\n{main.resolve()}\nterm_old\n")
    env = {**env, "ORCA_PANE_KEY": "tab-1:leaf-1", "ORCA_TERMINAL_HANDLE": "term_new"}
    assert _ccs(main, env, "--orca-tab-reopen").stdout == f"{session}\tagent old\n"


def test_a_linked_origin_folder_is_never_written_through(tmp_path: Path) -> None:
    # An .origin that is a symlink would send the marker to the link's target:
    # --mark says so and the hook's write is skipped, writing nothing outside.
    main, _, projects, env = _named_repo(tmp_path)
    topics = projects / ORIGIN_LIST / "topics"
    topics.mkdir(parents=True)
    (topics / "demo.txt").write_text(f"{SESSION_ID}\n")
    outside = tmp_path / "outside"
    outside.mkdir()
    (topics / ".origin").symlink_to(outside)
    marked = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--mark", "demo", "human"],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
    )
    assert marked.returncode == 1 and "symlink" in marked.stderr
    _sync(
        main,
        env,
        OTHER_SESSION,
        "auto-one",
        *_sync_opts("SessionStart", "startup", "agent"),
    )
    assert (topics / "auto-one.txt").is_file()  # the name itself is still saved
    assert list(outside.iterdir()) == []


# --- ccsession --prune --apply asks for a typed confirmation -------------------


def _prune_apply_on_pty(
    main: Path, env: dict[str, str], answer: str | None, *extra: str
) -> tuple[int, str]:
    proc, master = _spawn_on_pty(
        [str(SKILL_DIR / "ccsession"), "--prune", "--apply", *extra], env, main
    )
    try:
        shown = _read_pty(master, until="anything else cancels: ")
        if answer is not None:
            os.write(master, (answer + "\r").encode())
        shown += _read_pty(master, timeout=20)
        return proc.wait(timeout=60), shown
    finally:
        if proc.poll() is None:
            proc.kill()
        os.close(master)


def test_prune_apply_on_a_terminal_shows_the_plan_and_deletes_on_the_typed_number(
    tmp_path: Path,
) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    status, shown = _prune_apply_on_pty(main, env, "1")
    assert status == 0, shown
    assert "agent old  last change" in shown and "60 days old" in shown
    assert "This will delete 1 thing: 1 agent session (" in shown
    assert "Type 1 to delete them, anything else cancels: " in shown
    assert not sessions["agent old"].exists()
    assert all(sessions[n].is_file() for n in ("agent new", "mine old", "human old"))


def test_prune_apply_on_a_terminal_deletes_nothing_on_a_wrong_answer(
    tmp_path: Path,
) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    before = _tree(Path(env["HOME"]))
    status, shown = _prune_apply_on_pty(main, env, "yes")
    assert status == 1 and "Cancelled: nothing was deleted." in shown
    assert _tree(Path(env["HOME"])) == before


def test_prune_apply_without_a_terminal_refuses_unless_yes_is_given(
    tmp_path: Path,
) -> None:
    main, env, sessions = _prune_tree(tmp_path)
    before = _tree(Path(env["HOME"]))
    refused = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--prune", "--apply"],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
        input="1\n",  # a pipe: an answer typed there is not a person's
    )
    assert refused.returncode == 2
    assert "not a terminal" in refused.stderr and "--yes" in refused.stderr
    assert _tree(Path(env["HOME"])) == before
    allowed = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "--prune", "--apply", "--yes"],
        cwd=main,
        env=env,
        text=True,
        capture_output=True,
        stdin=subprocess.DEVNULL,
    )
    assert allowed.returncode == 0, allowed.stderr
    assert "Deleted 1 agent session " in allowed.stdout
    assert not sessions["agent old"].exists()
