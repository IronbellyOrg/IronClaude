"""Focused contracts for pinned, compatibility-preserving MCP registry entries."""

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
