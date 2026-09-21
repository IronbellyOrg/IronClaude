# Focused MCP contract tests

- **Command:** `uv run pytest tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_registry.py tests/cli/test_mcp_project_config.py tests/docs/test_tavily_doc_alignment.py -v`
- **Result:** PASS — 22 passed, 1 skipped (`TAVILY_API_KEY`-gated live smoke test).
- **Evidence:** `focused-pytest.txt`, exit code `0` in `focused-pytest.exit`.
