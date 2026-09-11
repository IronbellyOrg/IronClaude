"""Focused contracts for pinned, compatibility-preserving MCP registry entries."""

import json
from pathlib import Path

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
            server = template[server_names[filename]]
            assert server["args"] == args
            if filename == "morphllm.json":
                assert "@morph-llm/morph-fast-apply" not in json.dumps(template)
                assert "/home/" not in server["args"]
