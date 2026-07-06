---
title: "Tavily MCP Installer Upgrade Requirements"
domain: code
strategy: systematic
status: merged
convergence_score: 0.92
created: 2026-06-22T23:31:36Z
source_worktree: "/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade"
---

# Tavily MCP Installer Upgrade Requirements

## 1. Executive Decision

Upgrade IronClaude's live `superclaude mcp --servers tavily` installation path from stale local `tavily-mcp@0.1.2` to **local stdio `tavily-mcp@latest`** as the default. Do **not** switch the default to remote HTTP/OAuth in this change. Reconcile installer, docs, and dormant config artifacts so the live installer is the single source of truth and tests prevent another docs/installer drift.

This decision resolves the version-strategy debate as follows:

- **Default package policy:** use a centralized package token, e.g. `TAVILY_MCP_PACKAGE = "tavily-mcp@latest"`.
- **Current npm latest snapshot:** record `0.2.20` in tests/docs only as verified context, not as the installed command target.
- **Default transport:** keep `transport: "stdio"`, using `TAVILY_API_KEY` via Claude CLI `-e` env handling.
- **Remote HTTP:** document as future/optional work only; do not make it the default until the installer supports native HTTP command grammar and explicit auth behavior.

## 2. Non-Goals

- Do not implement a broad MCP config-loader from `src/superclaude/mcp/configs/`.
- Do not switch the existing `tavily` server entry to remote HTTP/OAuth by default.
- Do not require a browser OAuth flow for the default Tavily install.
- Do not require live Claude CLI, Node network install, or a Tavily API key for unit tests.
- Do not modify the AIRIS gateway path as part of this Tavily individual-server upgrade.

## 3. Functional Requirements

### FR-1 — Update the live Tavily package spec

**Target file:** `src/superclaude/cli/install_mcp.py`

The live `MCP_SERVERS["tavily"]` entry must no longer hard-pin `npx -y tavily-mcp@0.1.2`. It must derive its command from one centralized Tavily package token such as:

```python
TAVILY_MCP_PACKAGE = "tavily-mcp@latest"
```

The resulting command must be equivalent to:

```text
npx -y tavily-mcp@latest
```

**Acceptance criteria:**

- `MCP_SERVERS["tavily"]["command"]` contains `tavily-mcp@latest`.
- Active Python source under `src/superclaude/` contains no live `tavily-mcp@0.1.x` installer pin.
- The command remains `transport: "stdio"` with `api_key_env: "TAVILY_API_KEY"`.

### FR-2 — Keep local stdio as the default transport

**Target files:**

- `src/superclaude/cli/install_mcp.py`
- `docs/user-guide/mcp-servers.md`

The default `tavily` installer path must remain local stdio. The project must not silently switch to remote HTTP because the current installer command builder models stdio command execution, while native HTTP requires a different Claude CLI command shape.

**Acceptance criteria:**

- Tavily registry entry still has `transport == "stdio"`.
- Dry-run output for `superclaude mcp --servers tavily --dry-run` shows `--transport stdio` and `npx -y tavily-mcp@latest`.
- Documentation states that remote HTTP/OAuth is a separate option/future path, not the default behavior of `superclaude mcp --servers tavily`.

### FR-3 — Add stale Tavily install reconciliation

**Target file:** `src/superclaude/cli/install_mcp.py`

The installer must not skip users who already have a `tavily` server installed with a stale 0.1.x command. Current name-only installed checks are insufficient because they report `tavily` as installed regardless of package version.

Add a Tavily-scoped reconciliation path:

1. Detect exact server name `tavily` as installed.
2. Inspect the installed command/config enough to classify it as stale if it contains `tavily-mcp@0.1.x` or otherwise disagrees with `TAVILY_MCP_PACKAGE`.
3. If stale and not dry-run, remove the exact `tavily` server entry and re-add with the current package token.
4. If stale and dry-run, print the intended remove/re-add actions without mutation.
5. If current, preserve the existing "already installed" short-circuit.

**Acceptance criteria:**

- Mocked stale install triggers remove-before-add behavior.
- Mocked current install skips without remove/add.
- Dry-run stale install prints both the stale removal intent and the current add command.
- Reconciliation only targets exact server name `tavily`, never substring matches or AIRIS gateway entries.

### FR-4 — Redact API key values in displayed commands

**Target file:** `src/superclaude/cli/install_mcp.py`

Dry-run and command echo output must not include actual API key values. This is data-exposure prevention for terminals, transcripts, and CI logs.

**Acceptance criteria:**

- With `TAVILY_API_KEY` set to a sentinel value, dry-run output does not contain the sentinel.
- Displayed env args appear masked, e.g. `TAVILY_API_KEY=***`, while the actual subprocess command still receives the real value when not dry-run.
- Any future URL query form containing `tavilyApiKey=` is redacted before display.

### FR-5 — Reconcile docs with installer policy

**Target file:** `docs/user-guide/mcp-servers.md`

Docs must agree with the live installer and explain the chosen defaults.

Required doc content:

- Tavily local config example uses `tavily-mcp@latest`.
- The documented default transport is local stdio.
- `TAVILY_API_KEY` remains the default env-var path for local stdio.
- The tool surface includes at least `tavily-search`, `tavily-extract`, `tavily-map`, and `tavily-crawl`.
- Remote HTTP/OAuth is noted as an optional/future path, not the default installer path.
- Troubleshooting/verification tells users how to confirm Tavily is installed and how to inspect available tools after restart.

**Acceptance criteria:**

- A docs-installer parity test extracts the Tavily package token from both docs and installer and asserts equality.
- Docs contain no current recommendation to install `tavily-mcp@0.1.x`.
- Docs include map/crawl verification guidance.

### FR-6 — Retire dormant divergent Tavily config artifacts

**Target files:**

- `src/superclaude/mcp/configs/tavily.json`
- `plugins/superclaude/mcp/configs/tavily.json`

These files currently advertise an `mcp-remote` remote bridge form but are not loaded by the Python installer. They must not remain as contradictory apparent sources of truth.

Preferred behavior: delete both Tavily JSON files.

Fallback behavior if implementation discovers a packaging dependency: rewrite them to mirror the live local stdio installer shape and add an explicit non-authoritative note in adjacent documentation or generation logic.

**Acceptance criteria:**

- Preferred: the two Tavily JSON config files are absent.
- Test scans active source/plugin config locations and fails if a dormant Tavily config advertises `mcp-remote` or any package policy that conflicts with `TAVILY_MCP_PACKAGE`.
- No Python code is added that makes the old JSON config silently authoritative.

### FR-7 — Add a testable MCP add command builder seam

**Target file:** `src/superclaude/cli/install_mcp.py`

The installer command-building logic should be testable without invoking a real Claude CLI. Extract a pure helper or otherwise expose a test seam that builds the `claude mcp add` argv list.

**Acceptance criteria:**

- Stdio builder output preserves the existing grammar: server name before `-e`, env args before `--`, and command argv after `--`.
- Builder tests cover Tavily with and without API key env args.
- If HTTP support is added later, tests can assert that HTTP uses positional URL grammar without `--`.

### FR-8 — Add map/crawl tool-surface verification

**Target files:**

- `tests/cli/test_install_mcp_tavily.py` or `tests/mcp/test_tavily_upgrade.py`
- `docs/user-guide/mcp-servers.md`

Unit tests must verify the installer selects the package that should include Tavily's 0.2.x tool surface. A live tool enumeration check should be optional/integration-marked.

**Acceptance criteria:**

- Unit tests verify `tavily-mcp@latest` and fail on `0.1.x`.
- Docs name `tavily-map` and `tavily-crawl` as expected tools.
- Optional integration test is skipped unless required tools/credentials are present; when enabled, it checks that map/crawl tools appear in the connected MCP tool list.

## 4. Test Requirements

Create a Tavily-focused test module. Preferred location: `tests/cli/test_install_mcp_tavily.py` if following existing CLI test organization; `tests/mcp/test_tavily_upgrade.py` is acceptable if the project has or creates an MCP test namespace.

### Required unit/regression tests

1. **Registry package token:** Tavily command contains `tavily-mcp@latest` via the centralized token.
2. **No stale pin:** active installer source does not contain a live `tavily-mcp@0.1.x` pin.
3. **Fresh install command:** mocked install emits `claude mcp add --transport stdio ... -- npx -y tavily-mcp@latest`.
4. **Existing stale install:** mocked stale `tavily-mcp@0.1.x` installed entry triggers remove then add.
5. **Existing current install:** mocked current installed entry skips remove/add.
6. **Dry-run stale behavior:** dry-run prints remove/add intent but does not call remove/add subprocesses.
7. **Dry-run fresh behavior:** dry-run prints add command with `@latest` and no remove intent.
8. **API key env behavior:** `TAVILY_API_KEY` env is passed via `-e` in the real command path.
9. **API key display redaction:** sentinel key never appears in stdout/stderr captured from dry-run or command echo.
10. **Docs-installer parity:** docs package token equals installer package token.
11. **Dormant config cleanup:** active Tavily JSON config artifacts are deleted or match the installer policy.
12. **Transport default:** Tavily remains `stdio` by default.
13. **Command ordering regression:** server name precedes env flags, env flags precede `--`, command follows `--`.
14. **Installed-check robustness:** installed-check helper handles empty/None stdout without exception.
15. **Optional live tool surface:** skipped unless live prerequisites exist; when enabled, verifies map/crawl tool availability.

All Python test commands must be run with UV, e.g.:

```text
uv run pytest tests/cli/test_install_mcp_tavily.py -v
```

## 5. Migration and Back-Compat

| User state | Required behavior |
|---|---|
| No `tavily` server installed | Install local stdio `npx -y tavily-mcp@latest`. |
| Existing exact `tavily` server uses `tavily-mcp@0.1.x` | Detect stale, remove exact `tavily`, reinstall with `@latest`; dry-run reports intended actions only. |
| Existing exact `tavily` server already uses `tavily-mcp@latest` | Report already installed/current and do not mutate. |
| Existing Tavily via AIRIS gateway or other server name | Leave untouched. |
| Missing `TAVILY_API_KEY` | Preserve existing prompt/warning behavior; do not block installation solely due to missing key. |

## 6. Implementation Notes

- Treat the user-provided facts and enrichment artifacts as the requirements source; do not reintroduce a pin to 0.1.x.
- Keep the change narrowly scoped to Tavily's individual-server install path.
- If implementing stale detection with `claude mcp get`, gracefully fall back if that subcommand is unavailable; tests can mock both success and unavailable cases.
- Do not expose API key values in any paste-ready output, dry-run output, or logs.
- If dead config deletion reveals plugin packaging expectations, preserve package build by either removing matching references or rewriting the files consistently; do not leave them contradictory.

## 7. Acceptance Summary

The upgrade is complete when:

- `superclaude mcp --servers tavily --dry-run` shows `tavily-mcp@latest`, stdio transport, and masked API-key values.
- Existing stale 0.1.x `tavily` installs are no longer silently skipped.
- Docs, installer, and config artifacts no longer disagree.
- Unit/regression tests cover version, migration, docs parity, redaction, config cleanup, and command grammar.
- Optional live verification documents or confirms the expected `tavily-map` and `tavily-crawl` capabilities.
