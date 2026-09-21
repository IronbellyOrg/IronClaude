# Research: MCP Hardening Documentation and Configuration
**Scope:** Project-owned MCP documentation, configuration, source config examples, and source/mirror synchronization conventions
**Status:** Complete
**Date:** 2026-09-11
---

## Project-owned user guide

### `docs/user-guide/mcp-installation.md` (246 lines)

- The guide documents `superclaude mcp` installation and management at lines 1-19, including a server list command, interactive invocation, selected servers, and an “all servers” example.
- It currently calls `auggie` an available server and says it requires `auggie login` at lines 21-34; the API-key section expands this to session auth or `AUGMENT_SESSION_AUTH` at lines 54-64.
- It presents three Claude MCP scopes — local, project, and user — at lines 35-52; the project scope is explicitly a version-controlled `.mcp.json` and the user scope is machine-wide.
- It currently directs readers to verify with `claude mcp list` (lines 132-145) and repeats the same command in troubleshooting (lines 182-202).
- Its examples document `superclaude mcp --scope project` at lines 164-170 and tell readers not to commit API keys (lines 234-239).
- Required hardening documentation must preserve the distinction: the repository guide may document project-owned setup/verification, but must not prescribe edits to user-level Claude configuration or describe credentials as repository content.

## Auggie source guidance and project configuration

### `src/superclaude/mcp/MCP_Auggie.md` (65 lines)

- This source-owned MCP reference defines Auggie’s intended semantic-search role (lines 3-31) and says it should precede significant edits/design work (lines 5-11).
- Its managed-install snippet is `superclaude mcp --servers auggie` (lines 43-49), followed by global package installation and browser OAuth instructions.
- The manual alternative explicitly installs `@augmentcode/auggie@latest`, runs login, then adds the server with `claude mcp add --transport stdio --scope user auggie -- auggie --mcp --mcp-auto-workspace` (lines 51-59). This is an external/user-level configuration action and is out of scope for repository implementation changes.
- Documentation hardening should change this reference only if needed to remove/scope the user-level manual command. It must not add, mutate, or test an actual user-scoped MCP registration.

### `src/superclaude/mcp/configs/auggie.json` (10 lines)

- The canonical packaged config example defines key `auggie`, command `auggie`, and arguments `--mcp` and `--mcp-auto-workspace` (lines 1-9).
- This is the source config requiring any project-owned hardening change; the configuration matches the arguments stated in the user-scope manual documentation, but not the repository root config server name/command described below.

### `.mcp.json` (13 lines)

- The project-owned checked-in MCP config declares `mcpServers.auggie-mcp` as `stdio` (lines 1-4), runs `npx` (line 5), and passes `-y auggie-mcp` (lines 6-9), with an empty environment object (line 10).
- This root config is structurally different from the packaged source example: server key `auggie-mcp` versus `auggie`, and package command `npx -y auggie-mcp` versus installed CLI `auggie --mcp --mcp-auto-workspace`.
- The two configurations must be treated as distinct unless implementation/code tests prove a deliberate migration. Do not claim equivalence from the documentation alone.

## Required task changes, by owned file

1. `docs/user-guide/mcp-installation.md`
   - Update only the included server catalog/examples to agree with the verified registry and the project-local official Auggie configuration.
   - Keep scope explanations, but clearly identify project `.mcp.json` as the repository-owned surface and state that user configuration/authentication is outside the repository change.
   - Retain the no-secrets guidance (current lines 234-239). Do not add credentials to examples or `.mcp.json`.

2. `src/superclaude/mcp/MCP_Auggie.md`
   - Replace floating `@latest` installation guidance and the user-scope manual `claude mcp add` command only after the requested official Auggie `0.36.0` command/configuration is primary-source verified.
   - The source guide must point users to the project-local official executable configuration rather than asking implementation to mutate `~/.claude`/user-scoped registrations.

3. `.mcp.json`
   - Replace its third-party `npx -y auggie-mcp` declaration with the primary-vendor-verified, project-local official Auggie executable registration; keep the config project-owned and credential-free.
   - Add a focused test that parses this file and asserts the exact intended server key, `stdio` transport, executable command, arguments, and absence of inline credential values. This requirement comes directly from `BUILD-REQUEST.md` lines 7-17 and prevents the current root/config-example split from returning.

4. `src/superclaude/mcp/configs/auggie.json`
   - Update in the same unit of work if the official Auggie 0.36.0 command/arguments change. It is a packaged source config, so leaving its current generic CLI declaration while `.mcp.json` changes would preserve configuration drift.
   - Add or extend a unit assertion which compares its command/args against the verified canonical values. Whether it must match `.mcp.json` by identical JSON shape is unverified: the source example lacks `mcpServers`/transport today.

5. `tests/cli/test_install_mcp_tavily.py` and a new focused installer/config test (suggested `tests/cli/test_install_mcp_auggie.py`)
   - Existing tests establish the project convention: inspect live `MCP_SERVERS` registry data and intercept `_run_command`, rather than invoking installed MCP binaries (`test_install_mcp_tavily.py` lines 7-8, 60-101).
   - Extend/add tests for changed registry command pins (Tavily, Sequential, Serena, and the Morph successor) and for Auggie’s registry command plus the project `.mcp.json` official configuration. No test should call `claude mcp add`, `auggie login`, npm global install, or touch a user/machine config.

6. `tests/docs/test_tavily_doc_alignment.py`
   - Update its literal `0.2.20` assertions and descriptions to `0.2.22` after the primary-source release verification, because it scans all `src/superclaude` and `docs` text (lines 12-38 and 76-85).
   - Preserve its deliberately bounded scan roots and exclusions: `.dev/`, `.claude/`, and `dist/` are excluded at lines 12-34, enabling documented sources to be guarded without treating generated/historical files as current documentation.

## Source/mirror and package boundaries

- [CODE-VERIFIED] `src/superclaude/` is the distributable source of truth. The Makefile’s `sync-dev` only copies skills, agents, commands, hooks, and templates into `.claude/` (lines 108-158); it does not copy `src/superclaude/mcp/` docs or config examples.
- [CODE-VERIFIED] The Makefile’s `verify-sync` checks only those same generated categories (skills at lines 165-200; agents/commands/hooks thereafter). Therefore, changes to `src/superclaude/mcp/configs/` have no `.claude/` mirror to edit or verify.
- [CODE-VERIFIED] `.claude/*` is ignored except for listed exceptions including `.claude/settings.json` (`.gitignore` lines 104-125). Task validation must run `make sync-dev` and `make verify-sync` as requested, but generated `.claude/` output remains unstaged.
- [CODE-VERIFIED] `plugins/superclaude/mcp/configs/` is a separate plugin-source tree, not a mirror managed by `sync-dev`. Its existing `context7.json` and `serena.json` equal their `src` counterparts, but it has no Auggie config according to tracked-file inventory. The plugin build script copies only agents, commands, hooks, scripts, and skills (lines 74-96), not `mcp/`; plugin MCP changes are outside this task unless a separate packaging requirement is introduced.

## Explicit out-of-scope external and user-level configuration

- Actual user-scope Claude registrations (`claude mcp add/remove --scope user`), `~/.claude/**`, global npm state, and browser OAuth/session authentication (`auggie login`, `AUGMENT_SESSION_AUTH`) must not be modified. The task constraint at `BUILD-REQUEST.md` lines 12-17 explicitly prohibits machine/user configuration changes.
- API keys and environment values are excluded. The guide already prohibits committing API keys; `.mcp.json` currently uses `env: {}`.
- Context7, Playwright, Chrome DevTools, Magic, AIRIS, Markdown Collab, and user-level Codebase Memory are excluded by `BUILD-REQUEST.md` lines 12-17. Do not broaden tests/docs/config cleanup into those integrations.

## Gaps and questions

- [UNVERIFIED] This research did not independently validate the vendor commands/releases for Auggie 0.36.0, Tavily 0.2.22, Sequential Thinking 2026.8.31, Serena 1.7.0, or the Morph successor. The builder must depend on the dedicated primary-source release research before specifying exact replacement strings.
- [CODE-CONTRADICTED] The checked-in project `.mcp.json` uses third-party `auggie-mcp`, whereas source docs/configs and the installer registry use the installed `auggie` executable. The hardening task is explicitly intended to resolve that divergence; do not copy either existing value forward without primary-source verification.
- [UNVERIFIED] No automatic source-to-plugin mirror exists for MCP references/configs. Existing plugin config parity for Context7 and Serena is observational, not an enforced synchronization contract.

## Summary

The minimal documentation/configuration work is confined to the project-owned user guide, Auggie source guidance/config example, root `.mcp.json`, and focused test guards. Source-to-`.claude` synchronization is required as validation only; it does not generate MCP configs or MCP docs. External user-level Claude configuration, authentication, global installations, API keys, and the explicitly excluded MCP integrations remain out of scope.
