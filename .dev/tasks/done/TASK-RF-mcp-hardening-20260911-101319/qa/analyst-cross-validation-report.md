# Cross-Validation Report

**Topic:** MCP hardening — final cross-validation of source authority, compatibility, and scope
**Date:** 2026-09-11
**Research files reviewed:** 8 (`01`–`08`)

---

## Verdict: PASS — the intended minimal scope is internally consistent

**Method:** Re-read research files 01–08, then checked their current-state and migration assertions against the repository registry, root configuration, CLI selection/reconciliation path, direct command documentation, hooks/eval namespace consumers, and focused tests. Release facts are accepted from primary-source research 03 and gap fills 05–06 for this internal-consistency review; no new external verification was requested.

## Scope Decision

| Boundary | Decision | Evidence |
|---|---|---|
| Runtime authority | Change only `src/superclaude/cli/install_mcp.py` registry values/metadata for the five target servers. | The CLI selects by `MCP_SERVERS` key and registers the entry's `name` and `command` (`install_mcp.py:617–771, 877–954`). JSON templates are not installer inputs (07:34–48). |
| Registry names | Preserve `sequential-thinking`, `serena`, `morphllm-fast-apply`, `tavily`, and `auggie`. | CLI selectors are registry keys (`install_mcp.py:877–888`); 06:7–13 establishes a Morph command-only migration; 07:72–87 establishes root Auggie key preservation. |
| Root configuration | Change `.mcp.json` launcher tokens only; retain `mcpServers.auggie-mcp`, `type: stdio`, and empty `env`. | The root config currently uses the third-party `npx -y auggie-mcp` form (`.mcp.json:2–10`). Both hooks and the shell matcher deliberately support `mcp__auggie-mcp__*` (`hooks.json:60–67`; `auggie-flag-clear.sh:22–31`). |
| Legacy registrations | Do not add old-name discovery/removal, aliases, or hook/eval migrations. | Reconciliation removes only the selected entry's exact `name` (`install_mcp.py:623–685`). Preserving every name makes each command upgrade use the existing same-name reconciliation path. |
| Direct command docs/tests | Update only docs and tests that state or assert a changed registry/root command; do not consolidate unrelated legacy/template surfaces. | `mcp-installation.md` publishes CLI selector/catalog values (`:14–33`); `mcp-servers.md` contains concrete install/config commands (`:250–275`); `MCP_Auggie.md` and `MCP_Tavily.md` state current commands/pins (`MCP_Auggie.md:43–57`; `MCP_Tavily.md:5`). Existing Tavily tests deliberately pin `0.2.20` (`test_install_mcp_tavily.py:27–37`; `test_tavily_doc_alignment.py:76–85`). |
| Excluded artifacts | Leave `src/superclaude/mcp/configs/*`, `plugins/superclaude/mcp/configs/*`, hooks/eval capabilities, and non-command architecture/reference cleanup untouched. | Config templates are packaged references but not read by the installer (07:42–48); 07:89–105 identifies them as pre-existing drift outside the minimal runtime migration. |

## Claim Cross-Validation

| # | Claim after gap fills | Verdict | Evidence |
|---|---|---|---|
| 1 | Serena can move from the floating Git launcher to a pinned `serena-agent==1.7.0` launcher without a server-name migration. | **VERIFIED** | 05:5–13 supplies the complete launcher. The registry's existing key/name is `serena` (`install_mcp.py:65–70`), and command drift is reconciled by that same exact name (`:632–685`). |
| 2 | Morph can use `npx -y @morphllm/morphmcp` while keeping registry key and Claude registration `morphllm-fast-apply`. | **VERIFIED** | 06:7–15 explicitly makes this compatibility decision and preserves `MORPH_API_KEY`; the current registry uses the same key/name and environment contract (`install_mcp.py:72–80`). |
| 3 | The root project config can use official `auggie --mcp --mcp-auto-workspace` without renaming `auggie-mcp`. | **VERIFIED** | 07:70–94 gives the exact key-preserving JSON. The launcher matches the existing runtime registry and packaged reference (`install_mcp.py:98–108`; `src/superclaude/mcp/configs/auggie.json:2–7`). |
| 4 | No old-registration cleanup is necessary or warranted for this change. | **VERIFIED** | Name stability means no legacy registration is superseded by another name. Existing exact-name reconciliation re-registers command drift and never searches/removes unrelated names (`install_mcp.py:623–685`). |
| 5 | Registry key preservation avoids invalidating direct `superclaude mcp --servers ...` invocations. | **VERIFIED** | Unknown selectors are rejected (`install_mcp.py:877–888`), while the current direct guide names `morphllm-fast-apply` in its all-server invocation/catalog (`mcp-installation.md:18,30`). |
| 6 | Direct documentation and targeted tests still require updates even though template/legacy cleanup is excluded. | **VERIFIED** | The direct docs contain the old Tavily pin and current commands (`mcp-servers.md:250–275`; `MCP_Tavily.md:5`; `MCP_Auggie.md:43–57`). The Tavily source/docs scanner will fail after a registry-only pin update unless remaining in-scope literals move together (`test_tavily_doc_alignment.py:76–85`). |

## Minimal Implementation Surface

1. **Runtime registry:** `src/superclaude/cli/install_mcp.py`
   - Pin Tavily `0.2.22`, Sequential Thinking `2026.8.31`, Serena `serena-agent==1.7.0` using 05's verified launcher, and Auggie `@augmentcode/auggie@0.36.0` install metadata.
   - Replace only the Morph launcher with `npx -y @morphllm/morphmcp`; retain `morphllm-fast-apply` as both key and `name`, and retain `MORPH_API_KEY`.
   - Do not modify `install_mcp_server()` reconciliation logic or `main.py`.

2. **Project runtime config:** `.mcp.json`
   - Retain `auggie-mcp`, `stdio`, and `env: {}`.
   - Replace only `npx`, `-y`, and `auggie-mcp` launcher tokens with `auggie`, `--mcp`, and `--mcp-auto-workspace`.

3. **Direct command documentation:** assess only concrete installer/config snippets whose server command or pin changes; update `docs/user-guide/mcp-servers.md`, `src/superclaude/mcp/MCP_Auggie.md`, and `src/superclaude/mcp/MCP_Tavily.md`, and update `docs/user-guide/mcp-installation.md` only if its retained catalog/prerequisite wording becomes inaccurate.
   - Do not recast legacy examples into a new registration namespace; their command contents can be aligned while their existing server names stay stable.

4. **Tests:** update the two Tavily pin guards, add targeted registry command assertions for the four non-Tavily registry entries, and parse root `.mcp.json` to assert the preserved key plus the official executable/arguments and no inline credentials.

## Resolved Prior Inconsistencies

- **Morph migration:** 01/04 correctly identified that a name change would require a separate cleanup policy, but left it undecided. Gap fill 06 makes the stable-name, command-only route explicit; the old cleanup concern is therefore not in scope.
- **Auggie namespace:** 02/04 described the risk of replacing `auggie-mcp` with `auggie`. Gap fill 07 resolves it by retaining `auggie-mcp` while replacing only its executable tokens. Hooks/eval aliases remain valid without edits.
- **Config-template ownership:** 04 raised `src/` and plugin JSON templates as possible stale surfaces. Gap fill 07 establishes that neither is an installer input; changing them would broaden the task without hardening the runtime registry or root config.
- **Documentation boundary:** Direct command/pin docs remain in scope because they publish executable values and are covered by the Tavily docs scanner. Broader architecture/reference cleanup remains excluded.

## Validation Requirements

- Run focused installer and documentation tests through UV, including changed registry assertions, root-config parsing, `tests/cli/test_install_mcp_tavily.py`, and `tests/docs/test_tavily_doc_alignment.py`.
- Confirm command-drift behavior using an existing-name fixture for each stable-name upgrade; no test should expect deletion or discovery of `morphllm-fast-apply` or `auggie-mcp` under a different name.
- Run `make sync-dev` and `make verify-sync` only as required project validation. They do not create an MCP config/doc mirror; do not stage generated `.claude/` content.

## Residual, Non-Blocking Documentation Debt

`src/superclaude/mcp/configs/{serena,morphllm}.json`, their plugin-tree counterparts, and broader reference/architecture pages can retain stale pre-task values because they are neither runtime registry inputs nor direct command documentation selected by this bounded change. Track their ownership/consolidation separately; do not use this task to remove legacy registrations or redefine their namespaces.

## Conclusion

The gap fills close the two earlier migration blockers: Serena now has an exact pinned launcher, and Morph has an explicit stable-name successor strategy. The key-preserving Auggie root-config migration likewise avoids the known hook/eval namespace coupling. With direct command docs/tests aligned to the new registry values, the requested minimal scope is sufficient and does not require legacy-registration cleanup.

---

## Final Cross-Validation — Research 01–08

### Command-source authority

| Decision | Verdict | Cross-validation evidence |
|---|---|---|
| `MCP_SERVERS` is the sole runtime authority for `superclaude mcp` commands. | **VERIFIED** | `install_mcp_servers()` accepts only registry keys and resolves each selected key directly from `MCP_SERVERS` before installation (`src/superclaude/cli/install_mcp.py:877–888, 952–954`). `install_mcp_server()` reads that entry's `name`, `transport`, and `command` (`:617–620`) and passes the split command to `claude mcp add` (`:754–771`). |
| Packaged JSON configs are not a second installer command authority. | **VERIFIED** | Research 07's consumption trace is consistent with the code path above: no template is consulted by the CLI; shipped configs are reference artifacts. The current Auggie template already has the intended executable/arguments (`src/superclaude/mcp/configs/auggie.json:2–8`). |
| Project-root `.mcp.json` is an independent, project-owned runtime configuration. | **VERIFIED** | It currently defines `auggie-mcp` with a third-party `npx -y auggie-mcp` launcher (`.mcp.json:2–10`), distinct from the installer registry's `auggie` entry (`install_mcp.py:98–108`). |
| Docs are publication surfaces, not command authority. | **VERIFIED** | Current direct commands/pins in `docs/user-guide/mcp-servers.md:250–275`, `src/superclaude/mcp/MCP_Auggie.md:45–57`, and `src/superclaude/mcp/MCP_Tavily.md:5` are stale relative to the selected releases; they must follow the registry decisions rather than drive them. |

### Compatibility choices

| Surface | Required compatible choice | Verdict | Evidence |
|---|---|---|---|
| Sequential Thinking | Retain `sequential-thinking` key/name; pin only the npm package command. | **VERIFIED** | Key selection is public CLI behavior (`install_mcp.py:877–888`); research 08 supplies `npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31`. No name migration is needed. |
| Serena | Retain `serena` key/name; replace the floating Git source with the verified pinned `uvx --from serena-agent==1.7.0` launcher. | **VERIFIED** | Same-name command drift triggers exact-name removal and re-add (`install_mcp.py:632–685`). Research 05 supplies the complete v1.7.0 launcher and required `claude-code`/project flags. |
| Morph | Retain client key and Claude registration name `morphllm-fast-apply`; replace only the deprecated launcher with `npx -y @morphllm/morphmcp`; retain `MORPH_API_KEY`. | **VERIFIED** | Research 06 explicitly separates the vendor package identity from the retained Claude client name. Existing same-name reconciliation supports this command-only replacement; changing the key would reject existing documented selectors (`install_mcp.py:877–888`). |
| Tavily | Retain `tavily` name and update the version constant and all literal test/doc guards to `0.2.22`. | **VERIFIED** | The registry uses `TAVILY_MCP_VERSION` (`install_mcp.py:28–30, 81–90`); the focused installer test and source/docs scan currently hard-code `0.2.20` (`tests/cli/test_install_mcp_tavily.py:27–37, 197–224`; `tests/docs/test_tavily_doc_alignment.py:76–85`). |
| Auggie | Retain installer name `auggie` and root-config key `auggie-mcp`; replace only root launcher tokens with `auggie --mcp --mcp-auto-workspace`; pin global install metadata to `@augmentcode/auggie@0.36.0`. | **VERIFIED** | Both prefixes are intentionally supported in the hook and script (`hooks.json:60–67`; `auggie-flag-clear.sh:22–31`) and eval capabilities/suite (`capabilities.py:218–232`; `real.yaml:36–41, 112–140`). Retaining `auggie-mcp` avoids an unrequested namespace migration. |

### Required-surface coverage

| Build-request requirement | Covered implementation surface | Status |
|---|---|---|
| Five verified registry upgrades | `src/superclaude/cli/install_mcp.py` | COVERED |
| Preserve exact-command reconciliation | No reconciliation-logic change; test its stable-name behavior through the existing helper pattern | COVERED |
| Changed registry-command tests | Update Tavily tests and add focused registry assertions for Sequential, Serena, Morph, and Auggie | COVERED |
| Project-local official Auggie configuration test | Add a parser-based root `.mcp.json` test preserving `auggie-mcp`, `stdio`, and empty `env`, while asserting official executable/arguments | COVERED |
| Direct user-facing command/pin documentation | Update `docs/user-guide/mcp-servers.md`, `src/superclaude/mcp/MCP_Auggie.md`, and `src/superclaude/mcp/MCP_Tavily.md`; assess `docs/user-guide/mcp-installation.md` and update only if its retained catalog/prerequisite wording becomes inaccurate | COVERED |
| Source of truth and generated output policy | Edit `src/superclaude/` first; run `make sync-dev`; never stage generated `.claude/` content | COVERED |
| Required validation | Targeted installer/docs tests through UV, then `make sync-dev`, `make verify-sync` with pre-change baseline capture, `make lint`, and relevant unit suite | COVERED |
| Excluded integrations and user/machine configuration | Do not modify excluded MCPs, credentials, `~/.claude`, global runtime state, hooks/evals, or template/plugin consolidation | COVERED |

### Disposition of apparent extra surfaces

- `src/superclaude/mcp/configs/auggie.json` already expresses the selected official command, so it requires **no content change**. `src/superclaude/mcp/configs/{serena,morphllm}.json`, their plugin-tree counterparts, and Serena Docker configuration are packaged legacy/reference artifacts with no discovered CLI consumer; research 07 correctly places their ownership consolidation outside this bounded task.
- Existing hooks and evals intentionally support both Auggie namespaces. Because the root configuration retains `auggie-mcp`, those surfaces require **no migration or test edits**.
- `docs/developer-guide/technical-architecture.md` and `docs/reference/mcp-server-guide.md` contain pre-existing stale MCP guidance, but they do not publish the selected direct installation surface and are not required to meet the BUILD REQUEST. Treat as separate documentation debt, not a scope gap.
- Research 02's conditional wording for the Auggie packaged template is consistent with research 07: the selected command/arguments already match, so no update is triggered.

## Final Verdict: PASS

All eight research files converge on one executable authority (`MCP_SERVERS`), preserve public registry keys and client registration names where compatibility depends on them, and identify every required source, test, documentation, root-config, validation, and exclusion boundary in `BUILD-REQUEST.md`. No unhandled required surface remains. This PASS is contingent on the builder re-verifying the cited primary commands immediately before edits and implementing the listed focused tests and direct documentation updates.
