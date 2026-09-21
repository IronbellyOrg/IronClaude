# Research: MCP Registry Hardening
**Scope:** `src/superclaude/cli/install_mcp.py`, its entry points/callers, and relevant tests for Tavily, Sequential Thinking, Serena, Auggie, and Morph
**Status:** Complete
**Date:** 2026-09-11
---

## Investigation Log

- Codebase-memory MCP tools were not available in this session; local repository search is being used as the fallback discovery method.
- The dedicated `Grep`/`Glob` tools also failed at runtime because the vendored ripgrep executable was unavailable. File discovery below uses `git ls-files` only as a fallback.

## Registry Constants — Initial Evidence

Source: `src/superclaude/cli/install_mcp.py`.

- `TAVILY_MCP_VERSION = "0.2.20"` is the explicit single-source registry pin (`install_mcp.py:28-30`). The Tavily command is interpolated as `npx -y tavily-mcp@{TAVILY_MCP_VERSION}` (`:81-90`), resolving to `npx -y tavily-mcp@0.2.20`.
- Target registry entries and exact current commands:
  - Sequential Thinking key/name `sequential-thinking`: `npx -y @modelcontextprotocol/server-sequential-thinking` (`:35-41`).
  - Serena key/name `serena`: `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --enable-web-dashboard false --enable-gui-log-window false` (`:65-71`).
  - Morph key/name `morphllm-fast-apply`: `npx -y @morph-llm/morph-fast-apply`; its API key environment variable is `MORPH_API_KEY` (`:72-80`).
  - Tavily key/name `tavily`: see pin above; API key environment variable `TAVILY_API_KEY`; default parameters are `{"search_depth": "basic", "max_results": 10}` (`:81-90`).
  - Auggie key/name `auggie`: `auggie --mcp --mcp-auto-workspace`; global prerequisite binary is `auggie`, with install command `npm install -g @augmentcode/auggie@latest` and package `@augmentcode/auggie` (`:98-115`).
- All five are `transport: "stdio"` and `required: False` in `MCP_SERVERS` (`:35-115`).

## Entry Point and Call Chain

- Packaging exposes `superclaude` through `superclaude.cli.main:main` (`pyproject.toml:70-73`).
- The Click `mcp` command is defined directly in `src/superclaude/cli/main.py:215-257`; it accepts repeatable `--servers/-s`, `--list`, `--scope` (`local|project|user`, default `user`), and `--dry-run` (`:215-228`).
- With `--list`, the entry point imports and calls `list_available_servers()` then returns (`main.py:239-243`). Otherwise it passes `list(servers)` (or `None`), `scope`, and `dry_run` to `install_mcp_servers()` (`:248-252`); a false success value ends with `sys.exit(1)` (`:254-257`).
- `install_mcp_servers()` validates prerequisites before selection (`install_mcp.py:847-869`), filters explicit selections exclusively by **registry key** (`:877-888`), or derives interactive/all selections from `MCP_SERVERS` insertion order (`:903-941`), then resolves each selected key back to `MCP_SERVERS[server_name]` and calls `install_mcp_server()` (`:946-968`).
- Consequence for Morph: renaming/replacing the `morphllm-fast-apply` registry key changes the valid CLI argument and docs example. Keeping the key while changing only its `name` changes the registered Claude MCP name but preserves the CLI selector. The BUILD REQUEST requires a supported Morph successor but does not state its target stable name; that identity must be confirmed from the primary Morph source before choosing between these compatibility behaviors.

## Exact-Command Reconciliation Behavior

- `check_mcp_server_installed(name)` runs `claude mcp list` and uses a case-insensitive substring search (`install_mcp.py:476-495`); it is deliberately only a cheap prefilter.
- `_run_mcp_get(name)` performs exact `claude mcp get <name>` lookup and returns stdout only for zero exit status (`:498-518`). `_parse_mcp_get_command()` reads `Command:` and `Args:` lines, tokenizes `Args:` with `shlex.split`, and returns a normalized space-joined command; missing command or malformed quoting returns `None` (`:521-546`). `_parse_mcp_get_scope()` maps the `Scope:` line to `local`, `user`, or `project`, else `None` (`:549-562`). `get_registered_mcp_command()` is the public thin parse wrapper (`:565-576`).
- `install_mcp_server(server_info, scope="user", dry_run=False)` reads `name`, `transport`, and `command` (`:603-620`). When the substring check hits, it calls exact `get`; no exact entry means fresh install without removal (`:623-640`). Otherwise, it compares the normalized registered command with `expected_command = " ".join(shlex.split(command))` (`:642-649`). Exact equality is a no-op success.
- Any command drift or unparseable registration produces a re-register action (`:651-685`): dry-run reports it only (`:657-662`); real execution removes the exact name before normal add. Removal uses parsed registered scope when it is `user` or `project`, omits `--scope` for `local` and unknown scope, and aborts on failed removal (`:664-684`). Therefore, changing any registry command automatically reconciles existing installations of the same registered **name**.
- API keys are prompted per `api_key_env`; values are passed as repeatable `-e KEY=value` but are masked in displayed commands (`:687-710`, `:773-786`). Registry `default_parameters` are serialized as compact JSON to `-e DEFAULT_PARAMETERS=...` independently of API-key entry (`:702-710`). Auggie can conditionally install and validate a declared global binary prior to registration (`:711-746`).
- Registration argv shape is `claude mcp add --transport <transport> [--scope <scope>] <name> [-e ...] -- <split-command>` (`:748-771`). This means no reconciliation code change is required for simple command-string version upgrades. A server-name migration (potentially Morph) is different: old-name discovery/replacement is not implemented, because all lookup/removal calls use the new entry's `name`.

## Relevant Tests and Reusable Helpers

### `tests/cli/test_install_mcp_tavily.py` (377 lines)

- Existing Tavily registry contract: asserts `TAVILY_MCP_VERSION == "0.2.20"`, interpolated and literal command equality, and `stdio` transport (`:27-38`). `test_default_parameters_field()` asserts the registry baseline (`:40-44`); `test_tavily_json_absent()` guards the removed config path (`:46-49`).
- `_FakeCompleted` supplies class attributes `returncode=0`, `stderr=""`, `stdout=""` (`:52-58`). `_patch_install_path(monkeypatch, dummy_key)` replaces `_run_command`, `check_mcp_server_installed`, and `prompt_for_api_key`, returning captured argv calls (`:60-74`). This is the smallest pattern for direct registry/add-argv tests of Sequential, Serena, Auggie, and a Morph successor; it prevents real `claude`, `npx`, or `uvx` execution.
- `test_default_parameters_propagated()` and `test_default_parameters_without_api_key()` assert `claude mcp add` argv and environment placement (`:77-132`); `test_api_key_never_in_logged_command()` uses `capsys` to protect secret masking (`:135-148`). Reuse only for a successor that retains `api_key_env`; do not copy the Tavily-only `DEFAULT_PARAMETERS` assertion to servers without that field.
- `_FakeGet`, `_get_output(version, scope=...)`, and `_patch_already_installed(...)` construct deterministic `claude mcp get` outputs and capture subsequent `remove`/`add` argv (`:150-194`). The version mismatch test proves remove-then-add order and scope targeting (`:197-229`); up-to-date test asserts get-only/no destructive call (`:232-247`); dry run asserts no remove/add (`:249-260`); malformed argv re-registers rather than raising (`:262-294`); substring false positive adds fresh without removal (`:297-319`); project-vs-user scope test requires removal at the registered scope (`:321-344`).
- Parser unit coverage exists for normalized command output (`:347-357`) and scope parsing (`:360-368`). The one live smoke test is `TAVILY_API_KEY`-gated and CI-safe (`:371-377`).

### `tests/docs/test_tavily_doc_alignment.py` (130 lines)

- The scoped scanner visits text files below only `src/superclaude` and `docs`, excluding generated/archive folders (`:12-55`); it has a non-vacuity assertion of more than 100 files (`:65-73`).
- `test_tavily_version_single_pin()` scans every `tavily-mcp@<version>` occurrence in that source/docs scope and currently permits only `0.2.20` (`:76-85`). Any Tavily bump must update this literal as well as `TAVILY_MCP_VERSION` and the literal backstop in `test_install_mcp_tavily.py`.
- The same module additionally guards removed `tavily.json`, stale `mcp.tavily` tokens, and docs duplication of Tavily default parameters (`:88-129`); those assertions are unrelated to a package version bump unless an implementation alters those surfaces.

### Other test coverage

- `tests/cli/test_cli_registration.py` freezes top-level CLI names and includes `mcp` in its expected command set (`:28-49`), then checks all registered help paths through `CliRunner` (`:56-119`). It is entrypoint coverage, not registry-content coverage; no change is necessary unless command registration itself changes.
- `tests/unit/test_cli_install.py` covers `install_commands`/skills only and does **not** import `install_mcp` (`:1-418`); it is not a target for this work.
- Repository-wide tracked-Python reference search found only `src/superclaude/cli/main.py` and `tests/cli/test_install_mcp_tavily.py` as callers/references to the MCP installer APIs/registry; no other production Python caller was found. [CODE-VERIFIED by `git grep` output, 2026-09-11]

## Related Configuration and Documentation Surfaces

- `.mcp.json` currently registers a different, third-party server named `auggie-mcp` using `npx -y auggie-mcp` (`.mcp.json:1-12`). This is separate from the installer registry's `auggie` entry. The BUILD REQUEST explicitly calls for a project-local official executable configuration, so this file is a required modification surface.
- `docs/user-guide/mcp-installation.md` hard-codes the all-server selector example including `morphllm-fast-apply` (`:7-19`), names that server in its catalog (`:21-34`), describes Morph API-key setup (`:54-82`), and says Serena requires `uv` (`:84-108`). These statements need reconciliation with the verified official Serena and Morph successors.
- `src/superclaude/mcp/MCP_Auggie.md` currently documents global latest installation (`npm install -g @augmentcode/auggie@latest`) and user-scoped command `auggie --mcp --mcp-auto-workspace` (`:43-59`). It must be aligned with the verified `0.36.0` official guidance and the `.mcp.json` project-local configuration, without treating either unverified final command form as settled.

## Minimal File-Level Modification Plan

1. **`src/superclaude/cli/install_mcp.py` — required.**
   - Change only the five target `MCP_SERVERS` entries/constants: Tavily pin to `0.2.22`; Sequential Thinking exact official `2026.8.31` command; Serena official pinned `1.7.0` command replacing the floating git source; Auggie official pinned `0.36.0` installation guidance/command; and Morph's official successor key/name/command/API-key metadata as verified.
   - Preserve `install_mcp_server()` and its exact-command comparison for version-only command changes. Add migration logic only if primary Morph guidance requires a new registered name and the task explicitly requires automatic removal of the deprecated old registration; present code cannot detect it.

2. **`tests/cli/test_install_mcp_tavily.py` — required and sufficient unit-test home for installer registry changes.**
   - Update the three Tavily `0.2.20` literal expectations (registry, re-registration add argv, live gated suffix) and `_get_output`-driven expected add values to `0.2.22`.
   - Add concise parameterized/direct assertions for the four non-Tavily target entries, reading actual registry values and capturing generated add argv with existing `_patch_install_path`. Include Auggie prerequisite metadata and command behavior. Add an old-vs-new reconciliation assertion only where the registered name remains unchanged; cover a Morph name migration separately if adopted.

3. **`tests/docs/test_tavily_doc_alignment.py` — required for Tavily only.** Change the permitted literal from `0.2.20` to `0.2.22`; retain scanner scope and existing unrelated drift guards.

4. **`.mcp.json` — required.** Replace the `auggie-mcp` third-party definition with the primary-vendor-confirmed project-local official Auggie executable configuration. This configuration is not generated `.claude/` content and is eligible for normal source control.

5. **`docs/user-guide/mcp-installation.md` — required.** Update all-server invocation, catalog naming/description, Morph API-key wording if the successor's credential contract differs, and Serena prerequisite guidance if its official install method changes.

6. **`src/superclaude/mcp/MCP_Auggie.md` — required.** Replace floating `@latest` advice with confirmed `0.36.0` guidance and describe the repository `.mcp.json` configuration consistently.

7. **No `src/superclaude/cli/main.py` change is needed.** Its registry-neutral selection/pass-through API already handles changes to entry command strings; modify it only if a backward-compatible Morph CLI alias is explicitly requested.

## Gaps and Questions

- **[UNVERIFIED] Exact final command strings other than Tavily.** The BUILD REQUEST supplies target versions but not authoritative command syntax for Sequential Thinking `2026.8.31`, Serena `1.7.0`, Auggie `0.36.0`, or the Morph successor. This report intentionally does not infer package names, launch subcommands, transport/name, API environment variables, or Morph key migration from version labels. Primary vendor-source verification is a prerequisite before editing.
- **[UNVERIFIED] Morph migration policy.** Reconciliation only works on one exact registered name. If the supported successor has a new `name`, existing `morphllm-fast-apply` registrations will remain untouched. Decide whether preserving a deprecated entry is acceptable or whether automatic old-name cleanup is a stated requirement; do not introduce destructive cross-name removal speculatively.
- **[CODE-CONTRADICTED] Auggie configuration is currently split.** The installer registers official `auggie` via a global executable (`install_mcp.py:98-115`), while project `.mcp.json` registers unrelated `auggie-mcp` via `npx` (`.mcp.json:3-11`). The BUILD REQUEST selects an official project-local executable configuration, so the source/config docs must converge on the vendor-verified approach.

## Summary

- The registry and its exact-command, same-name reconciliation path are isolated to `src/superclaude/cli/install_mcp.py`; `src/superclaude/cli/main.py` is a registry-neutral Click pass-through.
- Focused regression coverage already exists in `tests/cli/test_install_mcp_tavily.py`, including reusable fake subprocess/captured-argv and stale-registration helpers. Tavily also has a separate source/docs single-pin guard in `tests/docs/test_tavily_doc_alignment.py`.
- Minimum confirmed modification surface: installer registry, focused installer tests, Tavily drift test, `.mcp.json`, MCP install guide, and Auggie guide. Final non-Tavily registry values remain intentionally blocked on primary-vendor verification.
