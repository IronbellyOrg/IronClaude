# Variant 2 — DevOps Spec: Tavily MCP Install/Config Upgrade

## Decision

Use deterministic local stdio as the `superclaude mcp --servers tavily` default, pinned to npm `tavily-mcp@0.2.20`. The npm dist-tag is the authoritative version source; do not keep the current `0.1.2` pin and do not encode the stale docs page version. The hosted Tavily remote endpoint remains a supported alternate configuration, but it must not be represented as the same registration shape as local stdio.

Source-of-truth changes:

1. `src/superclaude/cli/install_mcp.py`: update `MCP_SERVERS["tavily"]` to local stdio `npx -y tavily-mcp@0.2.20` and add install-time default-parameter metadata.
2. `src/superclaude/mcp/configs/tavily.json`: reconcile by converting it from an unreferenced conflicting remote default into an explicit alternate profile, e.g. `tavily-local` and `tavily-remote`, or delete it if no Python reader exists. If retained, `tavily-local` must match the CLI default exactly; `tavily-remote` must use the Tavily hosted URL and a remote transport/wrapper shape, not masquerade as the default installer path.
3. `src/superclaude/cli/main.py`: no functional change required for the help example.

## Exact default install command

The upgraded default local registration argv for user scope is:

```python
[
    "claude", "mcp", "add",
    "--transport", "stdio",
    "--scope", "user",
    "tavily",
    "-e", "TAVILY_API_KEY=<redacted>",
    "-e", 'DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}',
    "--",
    "npx", "-y", "tavily-mcp@0.2.20",
]
```

Operator-visible dry-run output must show the same argv shape but must never print the actual API key. It may print `TAVILY_API_KEY=<redacted>` or `TAVILY_API_KEY=<from-env>`.

Keep the existing CLI grammar invariant: server name before all `-e KEY=VALUE` flags, then `--`, then the shlex-split command. Keep the idempotency check before prompting for secrets or building side-effectful command output: `check_mcp_server_installed("tavily")` still uses `claude mcp list`; if already installed, return success and do not prompt for `TAVILY_API_KEY`.

## DEFAULT_PARAMETERS plumbing

Add a generic installer field such as:

```python
"default_parameters": {"search_depth": "basic", "max_results": 10},
"default_parameters_env": "DEFAULT_PARAMETERS",
```

For local stdio, serialize compact JSON with stable separators and append it as another repeatable env var:

```python
-e DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}
```

This should be computed from structured data, not hard-coded into the command string, so tests can assert the exact JSON. Treat API key and default parameters as separate env vars. Do not log the API key in dry-run, normal run, errors, or post-install messages.

For the remote Tavily profile, do not reuse the local stdio command. Remote registration must either be native remote transport or an explicit `mcp-remote` stdio wrapper profile. In both cases, document it as alternate, not default:

- Remote URL source: `https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}`.
- If using native remote transport, register the URL directly with the appropriate Claude transport and attach `DEFAULT_PARAMETERS` through the supported header/default-parameter mechanism.
- If using `mcp-remote`, the config must include an explicit header/env forwarding mechanism for `DEFAULT_PARAMETERS`; otherwise remote defaults are unsupported and must be called out rather than silently omitted.

## Implementation mechanics

Refactor command construction into a pure helper, e.g. `_build_mcp_add_command(server_info, scope, env_values, redact=False) -> list[str]`. `install_mcp_server()` should use it for both dry-run and execution. This makes CI assertions possible without spawning `npx` or `claude`.

Acceptance details:

- `check_prerequisites()` can continue requiring Node 18+ because default Tavily remains local npm stdio.
- `prompt_for_api_key()` should not run during dry-run if the env var is absent; dry-run should use a placeholder/masked value.
- `_run_command()` receives a list argv; tests assert the list before platform shell wrapping.
- Failed installs must report command failure without echoing secret env values.

## Test and verification plan

Add `tests/cli/test_install_mcp_tavily.py`.

Pure unit tests, CI-safe:

1. `test_tavily_registry_pins_0_2_20`: asserts `MCP_SERVERS["tavily"]["command"] == "npx -y tavily-mcp@0.2.20"`, transport is `stdio`, and default parameters are `{"search_depth":"basic","max_results":10}`.
2. `test_tavily_builds_exact_claude_mcp_add_argv`: monkeypatch `check_mcp_server_installed` to `False`, `prompt_for_api_key` to return `tvly-test`, and `_run_command` to capture argv and return success. Assert captured argv equals the literal local argv above with `TAVILY_API_KEY=tvly-test` and `DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}`. No `npx` process is spawned.
3. `test_tavily_dry_run_masks_api_key_and_does_not_execute`: monkeypatch `_run_command` to fail if called for install execution; assert dry-run output contains `tavily-mcp@0.2.20`, contains `DEFAULT_PARAMETERS=`, and does not contain the test key.
4. `test_tavily_already_installed_short_circuits`: monkeypatch installed check to `True`; assert no API-key prompt and no install command.

Opt-in live smoke, skipped in CI:

- Add `tests/cli/live/test_tavily_mcp_live.py` or mark `@pytest.mark.live_mcp`.
- Skip unless `TAVILY_API_KEY` is set and `CI` is not set.
- Run `claude mcp add --transport stdio --scope user tavily-smoke -e TAVILY_API_KEY=<key> -e DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10} -- npx -y tavily-mcp@0.2.20`.
- Then perform a Tavily search round-trip through Claude/MCP tooling and assert at least one non-empty result item.
- Cleanup should remove `tavily-smoke` if the Claude CLI supports removal; otherwise use a unique name and document manual cleanup.

CI acceptance: `uv run pytest tests/cli/test_install_mcp_tavily.py -v` passes without network, without a real Tavily key, and without spawning `npx`.
