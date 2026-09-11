"""Contracts for the repository-owned Claude MCP configuration."""

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def test_project_auggie_configuration_uses_official_cli_and_stable_key():
    config = json.loads((_REPO_ROOT / ".mcp.json").read_text())
    server = config["mcpServers"]["auggie-mcp"]

    assert server == {
        "type": "stdio",
        "command": "auggie",
        "args": ["--mcp", "--mcp-auto-workspace"],
        "env": {},
    }
    assert server["command"] != "npx"
    assert "AUGMENT_SESSION_AUTH" not in server["env"]
