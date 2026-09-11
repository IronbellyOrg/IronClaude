"""Focused contracts for pinned, compatibility-preserving MCP registry entries."""

import json
import shlex
from pathlib import Path
from types import SimpleNamespace

from superclaude.cli import install_mcp


def test_updated_mcp_registry_commands_are_pinned_and_stable():
    expected = {
        "sequential-thinking": "npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31",
        "serena": (
            "uvx --from serena-agent==1.7.0 serena start-mcp-server "
            "--context claude-code --project-from-cwd "
            "--enable-web-dashboard false --enable-gui-log-window false"
        ),
        "morphllm-fast-apply": "npx -y @morphllm/morphmcp",
        "auggie": "auggie --mcp --mcp-auto-workspace",
    }

    for key, command in expected.items():
        entry = install_mcp.MCP_SERVERS[key]
        assert entry["name"] == key
        assert entry["transport"] == "stdio"
        assert entry["command"] == command

    assert (
        install_mcp.MCP_SERVERS["morphllm-fast-apply"]["api_key_env"] == "MORPH_API_KEY"
    )
    assert (
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"]["install_command"]
        == "npm install -g @augmentcode/auggie@0.36.0"
    )


def test_distributable_mcp_templates_match_pinned_registry_commands():
    root = Path(__file__).resolve().parents[2]
    expected = {
        "serena.json": [
            "--from",
            "serena-agent==1.7.0",
            "serena",
            "start-mcp-server",
            "--context",
            "claude-code",
            "--project-from-cwd",
            "--enable-web-dashboard",
            "false",
            "--enable-gui-log-window",
            "false",
        ],
        "morphllm.json": ["-y", "@morphllm/morphmcp"],
        "sequential.json": [
            "-y",
            "@modelcontextprotocol/server-sequential-thinking@2026.8.31",
        ],
    }
    server_names = {
        "serena.json": "serena",
        "morphllm.json": "morphllm-fast-apply",
        "sequential.json": "sequential-thinking",
    }

    for base in (
        root / "src/superclaude/mcp/configs",
        root / "plugins/superclaude/mcp/configs",
    ):
        for filename, args in expected.items():
            template = json.loads((base / filename).read_text())
            server_name = server_names[filename]
            server = template[server_name]
            assert server["args"] == args
            assert [server["command"], *server["args"]] == shlex.split(
                install_mcp.MCP_SERVERS[server_name]["command"]
            )
            if filename == "morphllm.json":
                assert "@morph-llm/morph-fast-apply" not in json.dumps(template)
                assert "/home/" not in server["args"]


def test_auggie_global_binary_reconciles_stale_version(monkeypatch):
    calls = []
    versions = iter(["auggie 0.35.0", "auggie 0.36.0"])

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        if cmd == ["auggie", "--version"]:
            return SimpleNamespace(returncode=0, stdout=next(versions), stderr="")
        assert cmd == ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"]
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp.click, "confirm", lambda *args, **kwargs: True)

    assert install_mcp.ensure_global_binary(
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"], False
    )
    assert calls == [
        ["auggie", "--version"],
        ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"],
        ["auggie", "--version"],
    ]


def test_auggie_global_binary_rejects_post_install_version_mismatch(monkeypatch):
    versions = iter(["auggie 0.35.0", "auggie 0.35.0"])

    def fake_run_command(cmd, **kwargs):
        if cmd == ["auggie", "--version"]:
            return SimpleNamespace(returncode=0, stdout=next(versions), stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp.click, "confirm", lambda *args, **kwargs: True)

    assert not install_mcp.ensure_global_binary(
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"], False
    )


def test_auggie_global_binary_skips_install_at_pinned_version(monkeypatch):
    calls = []

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="auggie 0.36.0", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)

    assert install_mcp.ensure_global_binary(
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"], False
    )
    assert calls == [["auggie", "--version"]]


def test_auggie_reconciles_binary_before_up_to_date_registration(monkeypatch):
    calls = []
    versions = iter(["auggie 0.35.0", "auggie 0.36.0"])

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        if cmd == ["auggie", "--version"]:
            return SimpleNamespace(returncode=0, stdout=next(versions), stderr="")
        if cmd == ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"]:
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        assert cmd == ["claude", "mcp", "get", "auggie"]
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "auggie:\n"
                "  Scope: User config\n"
                "  Command: auggie\n"
                "  Args: --mcp --mcp-auto-workspace\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: True)
    monkeypatch.setattr(install_mcp.click, "confirm", lambda *args, **kwargs: True)

    assert install_mcp.install_mcp_server(install_mcp.MCP_SERVERS["auggie"])
    assert calls.index(
        ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"]
    ) < calls.index(["claude", "mcp", "get", "auggie"])
