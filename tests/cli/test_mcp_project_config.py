"""Contracts for the repository-owned Claude MCP configuration.

Codebase search now goes through the central LiteLLM proxy (issue #454), so the
repository must not register the local ``auggie`` stdio server, which fails
with ENOENT wherever the ``auggie`` binary is absent.
"""

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def test_project_mcp_config_has_no_auggie_stdio_server():
    path = _REPO_ROOT / ".mcp.json"
    if not path.exists():
        return
    servers = json.loads(path.read_text()).get("mcpServers", {})

    assert "auggie-mcp" not in servers
    assert not [
        name
        for name, server in servers.items()
        if server.get("type", "stdio") == "stdio" and server.get("command") == "auggie"
    ]
