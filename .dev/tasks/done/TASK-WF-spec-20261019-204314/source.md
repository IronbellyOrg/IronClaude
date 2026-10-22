---
title: Codebase Memory MCP installer integration
status: proposed
date: 2026-10-19
scope: superclaude install; superclaude mcp
---

# Codebase Memory MCP installer integration

## 1. Goal and decisions

Make Codebase Memory MCP part of a normal IronClaude installation and add it to the MCP management menu for installation and uninstallation. This document specifies changes only; it does not authorize implementation, remote-script execution, commits, or publishing a release.

The default setup must use the official installer requested by the user:

```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

**Design decision: retain the upstream installer's full setup, not binary-only setup.** The upstream installer can configure multiple detected clients and installs companion instructions, skills, agents, and hooks. Its matching uninstaller removes its owned integrations across detected clients as well as its binary. Consequently, Codebase Memory installation/removal is a **user-level tool lifecycle**, not a project-scoped registration toggle. Show these effects in the CLI; never label full removal as scoped deregistration.

Use the upstream lifecycle rather than reimplementing its download, checksum, activation, client-file merge, or cleanup logic. Keep existing MCP registration/listing infrastructure. Do not add a generic package-manager framework.

## 2. Verified baseline

Inspected in the isolated CodebaseMemoryMCP worktree on 2026-10-19.

| Source | Existing behavior |
|---|---|
| `src/superclaude/cli/main.py`, `install` | Installs core, commands, agents, skills, ccsession wiring, hooks, templates and user setup. No MCP setup. Aggregates mandatory failures into exit 1. `--list` returns before mutation; `--target` changes only slash-command destination. |
| `src/superclaude/cli/main.py`, `mcp` | Flat command, not a subgroup. Supports repeatable `--servers/-s`, `--list`, `--scope`, `--dry-run`; no uninstall or confirmation-bypass flag. Default scope is user. |
| `src/superclaude/cli/install_mcp.py` | `MCP_SERVERS` drives list/menu entries. `install_mcp_server` handles binary requirements and exact-name registration reconciliation. `ensure_global_binary` is an npm-oriented acquisition precedent, not a pipeline executor. |
| Same module, `check_prerequisites` | Currently checks Node for every selection, including non-Node servers. Selection must precede native-tool prerequisite checks. |
| Same module, `install_mcp_servers` | Gateway-first interactive installation only. An explicit gateway selection currently short-circuits all additional selections. |
| `docs/mcp/mcp-optional-design.md` | Runtime MCP use is optional with native fallbacks. Distinguish that runtime policy from the new default installation step. |

Upstream references:

- [Official installer](https://github.com/DeusData/codebase-memory-mcp/blob/main/install.sh).
- [Official README: installation and uninstall](https://github.com/DeusData/codebase-memory-mcp/blob/main/README.md).
- [CLI implementation: install/uninstall and client configuration](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/cli/cli.c).
- [Configuration documentation](https://github.com/DeusData/codebase-memory-mcp/blob/main/docs/CONFIGURATION.md).

Upstream `main` was observed at `32445b200156d23002aa6e11b8a808b2ca856795` during research. Revalidate flags and side effects before implementation: the requested script tracks `main`, while the script fetches release assets from `releases/latest/download`; those are independently moving inputs.

Verified upstream contract: default executable `~/.local/bin/codebase-memory-mcp`; stdio server starts with no arguments; MCP key `codebase-memory-mcp`. The shell installer supports `--dir`, `--clients=...`, and `--skip-config`; it invokes the candidate's installer with `-y --force`, verifies checksums, and preserves existing indexes unless reset is explicitly requested. The native uninstaller accepts `--dir`, `--dry-run`, and `-y/--yes`; it has no client-scoped removal flag. Uninstall with `-y` preserves indexes unless `--delete-indexes` is explicitly supplied. The adjacent updater script is reported, not deleted.

## 3. Public CLI contract

### Normal framework installation

`superclaude install` must ensure Codebase Memory MCP is installed, runnable, and registered for Claude Code at user scope. It is a default phase, not an additional opt-in question. Before acquisition, print the source URL, intended executable location, and the fact that upstream also configures detected clients and companion assets.

- Run the new phase after existing user setup, so framework installation has already established its files.
- A fresh install executes the official script using the safe execution equivalent in section 4.
- A working existing executable plus an exact, correct user registration is a no-op. Do not fetch latest on every framework install.
- A working executable with missing user registration is registered using the existing MCP registration mechanism; do not rerun the upstream installer merely to repair registration.
- A missing/non-runnable default executable is acquired/repaired through upstream. Do not replace an external package-manager installation silently.
- Acquisition, executable verification, or registration failure makes the overall install exit 1. Preserve successful framework work and report the failed phase and retry command.
- `--list` remains read-only and includes Codebase Memory availability/status. `--force` retains its framework-file meaning; it does not force a native-tool upgrade or erase indexes.
- `--target` retains its existing meaning and does not redirect native-tool or MCP configuration locations.

`superclaude update` is unchanged in this scope. It must not silently reinstall a tool the user explicitly uninstalled. A later explicit `superclaude install` restores the default bundle. Automatic native-tool upgrades, opt-out persistence, and a new framework-wide dry-run are out of scope.

### MCP menu and explicit selection

Keep the flat command and all existing installation invocations working. Add:

```text
superclaude mcp --servers codebase-memory-mcp
superclaude mcp --uninstall --servers codebase-memory-mcp
superclaude mcp --uninstall --servers codebase-memory-mcp --yes
superclaude mcp --uninstall --servers codebase-memory-mcp --dry-run
```

`--uninstall` and `--yes/-y` are NEW flags proposed by this design. They do not exist in the baseline. `--yes` bypasses consent prompts for the explicitly selected Codebase Memory lifecycle only; it must not select servers automatically, affect unrelated API-key prompts, or imply index deletion. `--list` cannot be combined with mutation modes; reject incompatible combinations before effects.

With no explicit servers, show an action choice: **Install MCP servers** (default), **Uninstall Codebase Memory MCP**, **Cancel**. The install branch retains the gateway-first server menu and adds Codebase Memory as a normal registry entry. The uninstall action explicitly names Codebase Memory; do not imply full uninstall support for other servers. Installation option 0 includes the new individual server. Explicit gateway-plus-Codebase-Memory selection must process both rather than silently dropping the native server.

Codebase Memory supports `--scope user` only in this increment because the requested full upstream lifecycle is account-wide. Reject project/local scope with a clear explanation before any download or write. Other servers retain their existing scopes. Do not silently ignore the requested scope or configure all clients while claiming project-only installation.

Noninteractive behavior: require an explicit server selection; no menu prompts on non-TTY input. Explicit Codebase Memory installation authorizes its documented default setup. Native removal requires either interactive confirmation or `--yes`. Dry-run never prompts for consent or invokes the upstream lifecycle.

## 4. Shared acquisition and registration

Add one small native-tool helper module, proposed as `src/superclaude/cli/install_codebase_memory.py`. Both the framework installation phase and the MCP Codebase Memory selection call the same install function. Keep the registry entry descriptive: exact name, stdio transport, executable with no server arguments, no API key and no Node requirement. Do not store a shell pipeline in `requires_global_binary.install_command`: existing token splitting/quoting would treat `|` as an argument.

### Acquisition sequence

1. Validate user scope and platform before effects. Initial automated support: Linux and macOS, amd64/arm64. Normalize architecture aliases and let upstream handle release-asset selection and Rosetta details. Native Windows is not supported by this Bash integration; report the official Windows installer as a separate manual path. A default framework install on an unsupported platform reports the unavailable required phase and exits 1 rather than claiming complete setup.
2. Verify Claude CLI is available. Check the canonical executable first, then a usable existing PATH installation. Do not require npm, Node, Docker, an API key, or a compiler for this native server. Missing curl/Bash is an acquisition prerequisite failure only if acquisition is actually needed.
3. If acquisition is needed, create a private temporary directory, download the complete official script with curl, require successful download and nonempty content, then execute it with Bash and no configuration-suppression flags. Use argv-based subprocess calls, not `shell=True`, a user-shell pipeline, or string interpolation. This preserves the requested upstream installation behavior while preventing execution of an incomplete download.
4. Use HTTPS-only download/redirect handling, a 60-second download timeout and a 300-second installer timeout. Clean up the temporary script on success/failure. Timeout handling must terminate/reap the launched installer tree rather than leave background installation continuing after a failure report. Catch expected OS/subprocess errors and return structured failure, not a traceback. Do not elevate privileges or disable upstream integrity checks.
5. Verify the resulting executable by its absolute path with `--version` and a bounded timeout. Do not assume `~/.local/bin` is on PATH. Preserve the upstream output describing client configuration and any shell/PATH changes; do not add a second independent shell-profile editor.
6. Ensure the exact user-scoped Claude MCP registration is stdio, points to the selected absolute executable and has no server arguments. If upstream already created the correct entry, do nothing. Otherwise use the existing Claude CLI registration flow. Keep all companion client/skill/agent/hook/instruction management upstream-owned.
7. Report acquisition, verification and registration outcomes separately; tell the user to restart their client to load new integrations. Do not claim graph indexing or a live MCP handshake occurred merely because registration succeeded.

This is a download-on-missing policy, not version pinning or an update manager. Display the verified version. The requested mutable upstream bootstrap remains a trust dependency; release checksums do not authenticate that bootstrap itself. A future pinning policy is separate work.

### Registration safety

Reuse exact-name lookup and command normalization. The new path must verify **user scope** as well as command/transport before declaring a no-op; a same-named project entry is not user installation success. Never remove a different scope to resolve an ambiguity. Prepare executable/prerequisites before registration changes. For a stale user entry, preserve its exact configuration before replacement and restore it if the add fails; report restoration failure distinctly. Treat query errors as errors, not proof of absence.

## 5. Uninstall lifecycle

Uninstall in this design means **remove the native tool and its upstream-owned integrations**, not merely remove the Claude Code registration.

1. Validate the selected server and scope before effects. This increment accepts only `codebase-memory-mcp` for `--uninstall`; unsupported names or a mixed unsupported removal selection fail before anything is removed.
2. Resolve the canonical upstream installation. Never run a PATH executable's uninstaller against an unrelated default directory. If only an externally managed/custom installation is found, stop with its resolved path and instructions to use its own installation mechanism; do not delete it or guess ownership.
3. Print a removal preview and require confirmation (default No). State that this affects Codebase Memory integrations across detected clients, may stop its active sessions, and keeps graph indexes. `--yes` is explicit consent to that described removal, not consent to delete indexes.
4. Execute the verified canonical binary with argv equivalent to `codebase-memory-mcp uninstall -y --dir=<canonical-install-directory>`. Always pass `-y` so the native tool cannot separately offer index deletion. Never pass `--delete-indexes`, reset flags, or manually delete caches, project files, skills or hooks. Let upstream own activation/daemon shutdown and owned-file cleanup.
5. Verify the canonical binary and exact user registration were removed. If upstream leaves the exact user registration, remove only that entry through the existing Claude CLI mechanism. Do not remove same-named project registrations or unrelated entries. Report an unexpected surviving registration as failure if it cannot be safely removed.
6. Preserve/report the adjacent updater script as upstream does. A leftover updater is not a failed uninstall. If a different PATH installation remains, report it rather than claiming all installations disappeared.
7. A fully absent binary and user registration is an idempotent success. Binary absent but registration present is a partial-install cleanup: after confirmation remove that exact user entry only and state that upstream companion assets were not audited/removed. Do not claim full cleanup or download a binary solely to uninstall it. Ambiguous discovery or failed probes fail closed.
8. On nonzero exit/timeout, report possible partial removal, retain output and provide a retry path. Do not launch a second blind deletion pass or imply rollback of upstream-managed effects.

**Dry-run:** show planned acquisition/registration/removal, source URL, user-level effects and index retention. Permit bounded read-only discovery; no network downloads, upstream install/uninstall processes, config changes, file deletion or prompts. `superclaude mcp --dry-run` without explicit servers prints available choices and exits instead of opening a menu.

## 6. Minimal change map

| File | Required change |
|---|---|
| `src/superclaude/cli/main.py` | Add the default install phase and failure aggregation; extend MCP options/action dispatch/help; retain `--list` early return. Do not alter update behavior. |
| `src/superclaude/cli/install_mcp.py` | Add registry entry, native-server dispatch, selection-aware prerequisites, menu action/entry, Codebase Memory removal dispatch, and process gateway-plus-native selections. Reuse registration helpers; make only the targeted safety changes needed by this path. |
| Proposed `src/superclaude/cli/install_codebase_memory.py` | Shared native acquisition/install/uninstall orchestration; no generic package framework. It must not create a circular import with MCP orchestration; keep Claude registration operations in `install_mcp.py`. |
| `tests/cli/test_install_mcp_registry.py` | Registry identity, native dispatch, executable-before-registration checks, existing Auggie behavior unchanged. |
| `tests/cli/test_update_command.py` | Add/mock the install phase, assert its order and fatal failure propagation; retain update's existing behavior. |
| Proposed `tests/cli/test_install_codebase_memory.py` | Mocked native lifecycle tests; use the existing test suite, not a new harness. |
| `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md` | Default setup, dependencies, full upstream side effects, user-only lifecycle, menu/flags, failure recovery and index preservation. |
| `docs/mcp/mcp-optional-design.md` | Explain default provisioning versus optional runtime usage; all other MCPs and native fallbacks remain unchanged. |

Update any directly affected install help/README statements that enumerate installed components. No unrelated documentation rewrite. Source edits belong in `src/superclaude/`; sync development mirrors only when distributable components change, and verify sync before any later commit. Never stage generated `.claude/` content.

## 7. Acceptance checks

All automated tests mock network and native/Claude subprocesses. No developer's real HOME, settings, binary or indexes may be modified by tests.

- Fresh normal install runs acquisition once, verifies the absolute binary, ensures exact user registration, and includes its result in the overall exit code.
- Missing registration repairs without network; correct binary plus registration performs no acquisition/mutation. An existing external binary is reused, never force-overwritten.
- `install --list` performs no acquisition/mutation; framework `--force` does not force native upgrade; update does not reinstall a removed tool.
- Missing curl/Bash, unsupported platform, download error/empty response, installer nonzero/timeout, failed postcheck and registration failure produce accurate nonzero outcomes without dependent steps running.
- Native-only selection succeeds without Node/npm/Docker/API keys; npm server prerequisite behavior remains intact.
- List/menu includes Codebase Memory; install-all includes it; explicit gateway-plus-native selection handles both; cancellation makes no changes.
- Project/local Codebase Memory scope is rejected before effects. Same-named registration in another scope is never removed or mistaken for user-scope success.
- Dry-run is prompt-free and mutation-free, including fresh install, stale registration, uninstall and no explicit servers.
- Uninstall decline changes nothing; noninteractive removal without `--yes` fails safely; confirmed removal invokes upstream once with `-y`, explicit canonical directory and no index-deletion flags.
- Removal keeps index/cache sentinel files and unrelated registrations/assets untouched by IronClaude; upstream-owned effects are represented accurately by fixtures. Native failures do not print success.
- Missing-binary partial cleanup and complete absence follow the distinct outcomes above. External/custom installs do not trigger guessed binary deletion.
- Paths with spaces remain single argv tokens. Failed registration replacement restores the captured user entry or reports failed restoration explicitly.

Before shipping, run one separately authorized live smoke test in a disposable user environment, not the developer's HOME: perform default setup, inspect the real upstream companion-file changes for preservation of preexisting framework/user hooks, register/query the MCP, repeat install for idempotence, then uninstall while retaining index sentinels. Verify released binary behavior as well as the moving script; mocked tests cannot prove upstream merge safety. If upstream overwrites unrelated files, block release and revise the integration rather than silently switching away from the full setup requested here.

## 8. Explicit exclusions

No graph indexing during installation; no new MCP usage policy, bundled graph skill/agents, gateway embedding, automatic native upgrades, index deletion, general uninstall support for every server, project-scoped full native lifecycle, Windows PowerShell integration, or replacement of the existing installer architecture.
