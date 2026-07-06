# Variant 3 — BACKEND Spec: Tavily MCP Upgrade

**Author**: backend-architect agent
**Date**: 2026-06-22
**Lens**: DEFAULT_PARAMETERS config plumbing + API-key data integrity + DRY config inheritance

## (a) Version Policy + Single Config Source of Truth

### Version Policy

- **Pin to the 0.2.x line**: `npx -y tavily-mcp@0.2.20` in `install_mcp.py` MCP_SERVERS["tavily"]. Use the exact dist-tags.latest version at upgrade time, but lock it to the minor band (`@0.2.20`, not `@latest`) to prevent surprise breakage on future 0.3 releases.
- **Future upgrades**: Bump the pin via PR only after verifying tool signatures (`tavily-search`, `tavily-extract`, `tavily-map`, `tavily-crawl`) have not regressed. `@latest` is reserved for servers with semver-stable APIs and proven upgrade safety (e.g. `@playwright/mcp@latest`); Tavily 0.1.x to 0.2.x was a breaking jump, so `@latest` is inappropriate here.
- **Retire the remote config JSON**: `src/superclaude/mcp/configs/tavily.json` contains an `mcp-remote` URL that embeds `${TAVILY_API_KEY}` directly into the URL query string. This config is not referenced by any Python reader in the codebase and serves no installation purpose. Its presence is dead code + a secret-in-URL hazard. **Delete it** from the upgrade PR. If `mcp-remote` is desired as a fallback transport, it belongs as an optional entry in the AIRIS gateway config, not in the individual-server registry.

### Single Config Source of Truth

- `MCP_SERVERS["tavily"]` in `src/superclaude/cli/install_mcp.py` is the **only** authoritative source for the install command, API key env var, and now DEFAULT_PARAMETERS. No other file should carry Tavily configuration for installation purposes.
- The `src/superclaude/mcp/configs/` directory remains for AIRIS gateway compose templates only, not for individual server install config.

## (b) Updated Install Args

### Command Update

```python
# Before (line 80):
"command": "npx -y tavily-mcp@0.1.2",

# After:
"command": "npx -y tavily-mcp@0.2.20",
```

### DEFAULT_PARAMETERS in the CLI Registration

The Tavily 0.2.x MCP server supports a `DEFAULT_PARAMETERS` environment variable (JSON string) that seeds sensible defaults for all tools. This should be injected as an additional `-e` flag during `claude mcp add`:

```python
"tavily": {
    "name": "tavily",
    "description": "Web search and real-time information retrieval for deep research",
    "transport": "stdio",
    "command": "npx -y tavily-mcp@0.2.20",
    "required": False,
    "api_key_env": "TAVILY_API_KEY",
    "api_key_description": "Tavily API key for web search (get from https://app.tavily.com)",
    "default_parameters": {
        "search_depth": "basic",
        "max_results": 10,
    },
},
```

### install_mcp_server() Modification

In `install_mcp_server()` (line 516), add a block after the API key handling (after line 552) to inject DEFAULT_PARAMETERS:

```python
    # Handle DEFAULT_PARAMETERS if provided (Tavily 0.2.x)
    if "default_parameters" in server_info:
        import json as _json
        params_json = _json.dumps(server_info["default_parameters"])
        env_args.extend(["-e", f"DEFAULT_PARAMETERS={params_json}"])
```

This reuses the existing `env_args` list that already flows into `cmd.extend(env_args)` at line 608, so no structural changes to the CLI registration command builder are needed. The `claude mcp add` invocation becomes:

```
claude mcp add --transport stdio tavily \
  -e TAVILY_API_KEY=<key> \
  -e 'DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}' \
  -- npx -y tavily-mcp@0.2.20
```

## (c) DEFAULT_PARAMETERS Design

### Authoritative Location

`default_parameters` lives **inline in `MCP_SERVERS["tavily"]`** as a Python `dict`. This is the single source of truth because:

1. `install_mcp.py` is already the sole reader of `MCP_SERVERS` for install-time config.
2. The `install_mcp_server()` function already iterates `server_info` keys to drive install behavior. Adding one more key is O(1) and zero indirection.
3. No JSON config file, no env var parsing, no YAML, no cross-file synchronization. The dict is serialized to JSON at install time only.

### Concrete Default Values

| Parameter    | Value      | Rationale                                                                 |
|------------- |------------|---------------------------------------------------------------------------|
| `search_depth` | `"basic"`  | The 0.2.x default. "advanced" adds latency and cost; operators can escalate via their own env override. |
| `max_results`  | `10`       | Matches the Tavily docs recommendation and the 0.2.x default. Provides sufficient breadth for research without flooding context windows. |

### Why Not an Env Var or Settings Key?

- **Env var `TAVILY_DEFAULT_PARAMETERS`**: Adds indirection. The operator would need to remember to set it before running `superclaude mcp`. The inline dict is self-documenting in the source and requires zero operator action.
- **`~/.claude/settings.json` or `settings.local.json`**: Those are Claude Code harness settings, not MCP server config. Adding MCP defaults there conflates concern boundaries and would require the install script to parse JSON settings.
- **Separate JSON config file**: `tavily.json` was already dead code. Adding another JSON file for defaults repeats the pattern.

### Propagation Path

```
MCP_SERVERS["tavily"]["default_parameters"]  (Python dict)
  └─ install_mcp_server() reads server_info["default_parameters"]
       └─ json.dumps() → "-e DEFAULT_PARAMETERS=..." appended to env_args
            └─ cmd.extend(env_args) → passed to "claude mcp add"
                 └─ Claude Code settings.json stores the env var with the server
                      └─ npx launches tavily-mcp@0.2.20 with DEFAULT_PARAMETERS in its process env
```

## (d) Secret Hygiene: URL-Embedded Key

### Verdict on `src/superclaude/mcp/configs/tavily.json`

The remote config `tavily.json` embeds the API key into a URL:
```
https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}
```

This is a **leak risk**. URL query strings appear in:
- Process listings (`ps aux`, `/proc/<pid>/cmdline`)
- System logs and audit trails
- Proxy/access logs (any reverse proxy or load balancer)
- Browser/app network logs
- MCP transport diagnostics

The stdio transport via `npx -y tavily-mcp@0.2.20` with the key passed as `-e TAVILY_API_KEY=<key>` is **superior** because the env var is never part of a URL, never appears in process command lines beyond the `-e` flag that `claude mcp add` already stores in the user's settings.json (which is local, not transmitted).

**Action**: Delete `src/superclaude/mcp/configs/tavily.json` entirely. The stdio install path covers all use cases. If `mcp-remote` is needed for AIRIS gateway users, that config belongs in the gateway's own `docker-compose.yml` + `.env`, not in the individual server registry.

## (e) Tests

### Test File: `tests/cli/test_mcp_tavily_config.py`

New test file with four assertions:

**T1. Version pin is 0.2.20**
```python
def test_tavily_version_pinned():
    from superclaude.cli.install_mcp import MCP_SERVERS
    cmd = MCP_SERVERS["tavily"]["command"]
    assert "tavily-mcp@0.2.20" in cmd
    assert "@0.1" not in cmd  # regression guard
```

**T2. DEFAULT_PARAMETERS dict reaches env_args in install_mcp_server**
```python
def test_default_parameters_propagated(monkeypatch):
    """Verify DEFAULT_PARAMETERS JSON is appended to env_args during install."""
    from superclaude.cli.install_mcp import MCP_SERVERS, install_mcp_server
    import json

    captured_cmds = []
    def fake_run(cmd, **kw):
        captured_cmds.append(cmd)
        r = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        return r

    monkeypatch.setattr("superclaude.cli.install_mcp._run_command", fake_run)
    monkeypatch.setattr("superclaude.cli.install_mcp.check_mcp_server_installed", lambda n: False)
    monkeypatch.setattr("superclaude.cli.install_mcp.click.confirm", lambda *a, **k: False)

    install_mcp_server(MCP_SERVERS["tavily"], scope="user", dry_run=False)

    # Find the claude mcp add command in captured calls
    add_cmd = [c for c in captured_cmds if c[:3] == ["claude", "mcp", "add"]][0]
    default_params = [v for v in add_cmd if v.startswith("DEFAULT_PARAMETERS=")]
    assert len(default_params) == 1
    parsed = json.loads(default_params[0].split("=", 1)[1])
    assert parsed == {"search_depth": "basic", "max_results": 10}
```

**T3. API key never logged/echoed in dry-run or install output**
```python
def test_api_key_never_echoed(monkeypatch, capsys):
    """Verify the API key does not appear in any click.echo or logged command."""
    from superclaude.cli.install_mcp import install_mcp_server
    import json

    fake_key = "tv-test-key-12345abcdef"
    server = {
        "name": "tavily",
        "transport": "stdio",
        "command": "npx -y tavily-mcp@0.2.20",
        "api_key_env": "TAVILY_API_KEY",
        "api_key_description": "test",
        "default_parameters": {"search_depth": "basic", "max_results": 10},
    }

    def fake_run(cmd, **kw):
        return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr("superclaude.cli.install_mcp._run_command", fake_run)
    monkeypatch.setattr("superclaude.cli.install_mcp.check_mcp_server_installed", lambda n: False)
    monkeypatch.setattr("superclaude.cli.install_mcp.click.prompt", lambda *a, **k: fake_key)
    monkeypatch.setattr("superclaude.cli.install_mcp.click.confirm", lambda *a, **k: True)

    install_mcp_server(server, scope="user", dry_run=True)

    out = capsys.readouterr().out
    assert fake_key not in out, f"API key leaked to stdout: {out}"
```

**T4. tavily.json is deleted (or at minimum, not referenced by install path)**
```python
def test_no_tavily_json_config_dependency():
    """Verify install_mcp.py does not import or read tavily.json."""
    import ast
    source = Path("src/superclaude/cli/install_mcp.py").read_text()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            assert "tavily.json" not in node.value, "install_mcp.py must not reference tavily.json"
```

## (f) File Targets Summary

| Action | File |
|--------|------|
| **Edit** | `src/superclaude/cli/install_mcp.py` — pin version to `@0.2.20`, add `default_parameters` dict, add env_args injection in `install_mcp_server()` |
| **Delete** | `src/superclaude/mcp/configs/tavily.json` — dead code + secret-in-URL hazard |
| **Add** | `tests/cli/test_mcp_tavily_config.py` — 4 tests (version pin, DEFAULT_PARAMETERS propagation, key non-leak, no JSON config dependency) |
| **No change** | `src/superclaude/cli/main.py` — help text is generic, no Tavily-specific flags |

## (g) Acceptance Criteria

1. `uv run pytest tests/cli/test_mcp_tavily_config.py -v` passes all 4 tests.
2. `superclaude mcp --servers tavily --dry-run` shows `tavily-mcp@0.2.20` in output, `DEFAULT_PARAMETERS=` with `{"search_depth":"basic","max_results":10}`, and no API key in stdout.
3. `src/superclaude/mcp/configs/tavily.json` no longer exists.
4. The `claude mcp add` command produced by install includes `-e DEFAULT_PARAMETERS=...` as a second env var after `-e TAVILY_API_KEY=...`.
5. CI runs without `TAVILY_API_KEY` set (tests mock the key prompt and never require a real key).

## (h) Biggest Risk

**Tool signature drift on 0.2.x minor bump**. If 0.2.21 or 0.2.22 changes default parameter names or removes DEFAULT_PARAMETERS support, the install silently produces a server that ignores our defaults. Mitigation: the version pin (`@0.2.20`) prevents auto-upgrade. When bumping, verify tool signatures via `npx tavily-mcp@0.2.N --help` or by inspecting the npm package before changing the pin.
