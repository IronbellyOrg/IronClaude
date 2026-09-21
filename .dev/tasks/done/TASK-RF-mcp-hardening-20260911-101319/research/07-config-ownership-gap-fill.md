# Research: MCP Config Ownership and `.mcp.json` Migration
**Scope:** `src/superclaude/mcp/configs/`, `plugins/superclaude/mcp/configs/`, installer/build/package consumers, and MCP documentation
**Status:** Complete
**Date:** 2026-09-11
---

## Investigation log

- Began inventory and consumption tracing for the requested MCP configuration artifacts.

## Config inventory

### Canonical Python-package config directory

`src/superclaude/mcp/configs/` contains the four requested artifacts:

| File | Server key | Invocation | Evidence |
|---|---|---|---|
| `src/superclaude/mcp/configs/sequential.json` | `sequential-thinking` | `npx -y @modelcontextprotocol/server-sequential-thinking` | lines 1–9 |
| `src/superclaude/mcp/configs/serena.json` | `serena` | `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant` | lines 1–14 |
| `src/superclaude/mcp/configs/morphllm.json` | `morphllm-fast-apply` | `npx @morph-llm/morph-fast-apply /home/`; blank `MORPH_API_KEY`, `ALL_TOOLS=true` | lines 1–13 |
| `src/superclaude/mcp/configs/auggie.json` | `auggie` | `auggie --mcp --mcp-auto-workspace` | lines 1–10 |

### Plugin-tree duplicate config directory

`plugins/superclaude/mcp/configs/` contains `sequential.json`, `serena.json`, and `morphllm.json`, content-equivalent to the corresponding `src/` configs based on the read content. It has no `auggie.json` (directory listing). This is an ownership/alignment gap if the plugin tree is still distributed or built.

### Repository runtime MCP file

`.mcp.json` is a separate project-root runtime configuration. It defines only `mcpServers.auggie-mcp` (`.mcp.json:2–12`) and currently invokes the unrelated npm executable `npx -y auggie-mcp` (`.mcp.json:5–9`). The requested official invocation already exists in the package config but under its distinct server key `auggie`.

## Consumption and distribution trace

### Actual installer authority: registry, not JSON templates

**[CODE-VERIFIED]** `src/superclaude/cli/install_mcp.py:34–116` defines the executable `MCP_SERVERS` registry. It contains the commands used by `superclaude mcp`, including Sequential (`:35–41`), Serena (`:65–71`), Morph (`:72–80`), and Auggie (`:98–115`). The Auggie registry command is already `auggie --mcp --mcp-auto-workspace` (`:102`).

**[CODE-VERIFIED]** `install_mcp_server()` takes `server_info["command"]` (`install_mcp.py:603–620`), splits it, and appends it after `claude mcp add … --` (`:748–771`). `install_mcp_servers()` obtains each entry solely from `MCP_SERVERS` (`:877–954`). Therefore a registry command change affects real installer registration; no requested JSON template participates in this path.

**[CODE-VERIFIED]** Registry command drift is reconciled by exact `claude mcp get` command comparison (`install_mcp.py:623–685`), then remove/re-add before registering, so changing the registry is the supported installer migration mechanism.

### Package/build distribution

**[CODE-VERIFIED]** All `src/superclaude/mcp/configs/*.json` files are distributable package artifacts: wheel configuration includes `src/**` (`pyproject.toml:79–88`), and sdist explicitly includes `src/` (`:90–98`); `MANIFEST.in:14` independently includes `src/superclaude/mcp` Markdown and JSON.

**[CODE-VERIFIED]** Plugin configs are also distributable, even though not consumed by the active installer: `pyproject.toml:81–88` includes and force-includes `plugins/**` into wheels, `:90–98` includes `plugins/` in sdists, and `MANIFEST.in:20–25` recursively includes plugin JSON including `plugins/superclaude/mcp/configs/*.json`.

**[CODE-VERIFIED]** A repository-wide tracked-content search for all requested template paths/keys and invocation tokens found no source-code reader of either config directory. The only active command source found is `src/superclaude/cli/install_mcp.py` above. Thus the JSON configs are packaged reference/template artifacts, not installer inputs.

### Documentation ownership

**[CODE-VERIFIED]** `src/superclaude/mcp/MCP_Auggie.md:43–59` is a distributable, accurate Auggie installation guide: it delegates to `superclaude mcp --servers auggie` and gives the manual official registration command with `auggie --mcp --mcp-auto-workspace` (`:54–57`). It is included in package artifacts by `MANIFEST.in:14`.

**[CODE-VERIFIED]** `docs/user-guide/mcp-installation.md:1–245` is user-facing installer documentation, lists Auggie (`:33`), and describes project scope as version-controlled `.mcp.json` (`:35–52`), but does not provide the root-file's Auggie JSON command. It is distributed in source packages under `MANIFEST.in:8`.

**[CODE-CONTRADICTED]** `docs/user-guide/mcp-servers.md` says SuperClaude integrates eight servers (`:5`) while its own list includes Auggie as a ninth server (`:14–23`, `:153–166`). Its configuration JSON (`:239–283`) omits Auggie. It should not be used as proof of current full registry coverage.

**[CODE-CONTRADICTED]** `docs/reference/mcp-server-guide.md` contains older tool/version guidance (for example Node 16 at `:20–24`), whereas the active installer enforces Node 18+ (`src/superclaude/cli/install_mcp.py:443–461`). It has no specific current Auggie installation entry in the read content and is not required for this narrow migration.

## `.mcp.json` migration compatibility

### Existing namespace coupling

**[CODE-VERIFIED]** The project-root server key is `auggie-mcp` (`.mcp.json:3`), which forms the observed MCP tool namespace `mcp__auggie-mcp__*`.

**[CODE-VERIFIED]** The distributable hook matcher explicitly supports that namespace alongside `mcp__auggie__*` and AIRIS (`src/superclaude/hooks/hooks.json:47–68`; specifically `:60`). Its script repeats the same three-prefix set in its `case` expression (`src/superclaude/hooks/scripts/auggie-flag-clear.sh:1–33`; specifically `:22–31`).

**[CODE-VERIFIED]** `tests/hooks/test_auggie_flag_clear_mcp_prefix.py:50–94` directly asserts that `mcp__auggie-mcp__ask_question` and `mcp__auggie-mcp__implement` clear the sticky state. Its structural checks require the `mcp__auggie-mcp__` prefix in both hook surfaces (`:148–177`). The eval capability suite also intentionally carries both `auggie` and `auggie-mcp` capability names (repo trace in `tests/cli/eval/fixtures/valid_suite.yaml` and related tests).

### Valid minimal migration

Retain the complete enclosing `mcpServers` structure and the server key `auggie-mcp`; retain `type: "stdio"` and `env: {}`. Replace only the executable and arguments:

```json
{
  "mcpServers": {
    "auggie-mcp": {
      "type": "stdio",
      "command": "auggie",
      "args": ["--mcp", "--mcp-auto-workspace"],
      "env": {}
    }
  }
}
```

This exactly matches the command tokens already used by the active Auggie registry (`src/superclaude/cli/install_mcp.py:98–115`) and packaged Auggie template (`src/superclaude/mcp/configs/auggie.json:1–10`), while preserving `mcp__auggie-mcp__*`. It avoids an unrequested hook/eval namespace migration. The `auggie` installer registration and project-local `auggie-mcp` registration can coexist as distinct Claude MCP server names; that operational coexistence is a likely duplicate-server concern, but the requested key-preserving root-file migration does not rename or remove either registration.

## Exact minimal scope recommendation

1. **Change `.mcp.json` only** for this project-local hardening: retain the `auggie-mcp` key and schema; replace its `npx -y auggie-mcp` command tokens with `auggie --mcp --mcp-auto-workspace` as shown above.
2. **Do not change `src/superclaude/cli/install_mcp.py`**: its executable registry already has the official Auggie command and its reconciliation logic will update installer-managed `auggie` registrations.
3. **Do not change `src/superclaude/mcp/configs/auggie.json` or `src/superclaude/mcp/MCP_Auggie.md`**: each already agrees with the registry's official invocation.
4. **Do not add `plugins/superclaude/mcp/configs/auggie.json` in this task**: the plugin config directory has no active installer consumer, lacks the file today, and adding a legacy duplicate expands scope without repairing the root runtime config. The plugin tree remains a packaged legacy/reference artifact; address its broader duplication only in a dedicated consolidation task.
5. **No documentation change is needed for the one-file `.mcp.json` command replacement.** `docs/user-guide/mcp-installation.md` explains `.mcp.json` project scope but does not prescribe the stale executable. Separately, open a documentation-debt task for `docs/user-guide/mcp-servers.md` and `docs/reference/mcp-server-guide.md`; do not bundle their unrelated stale guidance into this hardening.

## Gaps and questions

- **[CODE-CONTRADICTED] Template drift already predates this task:** `serena.json` lacks the active registry's `--enable-web-dashboard false --enable-gui-log-window false` options, and `morphllm.json` differs from the registry by omitting `-y` while adding `/home/`, a blank API key, and `ALL_TOOLS=true`. Since neither directory is read by the installer, there is no automatic consistency guarantee. Decide in a later task whether templates should be deleted, generated from the registry, or explicitly documented as legacy examples.
- **[CODE-CONTRADICTED] Plugin asymmetry:** `plugins/superclaude/mcp/configs/` is shipped but not installed from and has no `auggie.json`, whereas `src/superclaude/mcp/configs/auggie.json` exists. This makes the plugin directory unsuitable as a second source of truth.
- **[UNVERIFIED] Runtime behavior of two registrations:** no local Claude runtime listing was queried, so this research does not establish whether users commonly have both installer-managed `auggie` and project-local `auggie-mcp` registered simultaneously. The requested key preservation is sufficient to avoid breaking the hook/eval namespace regardless.

## Summary

The only active installer command authority is `MCP_SERVERS` in `src/superclaude/cli/install_mcp.py`, which already uses the official Auggie executable. The requested package/plugin JSON files are shipped but have no discovered installer consumer. The lowest-risk hardening is therefore a one-file `.mcp.json` command/arguments replacement that preserves `auggie-mcp`; no hook, eval, installer, template, plugin, or documentation edit belongs in this change.
