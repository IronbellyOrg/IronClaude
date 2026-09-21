# Research: MCP hardening integration impact
**Scope:** Install-MCP registry/CLI callers, tests, documentation, and server-name/configuration references
**Status:** Complete
**Date:** 2026-09-11
---

## Registry and CLI call chain

- **`src/superclaude/cli/install_mcp.py`** (969 lines): the authoritative runtime registry is `MCP_SERVERS` at lines 34–116. Its keys are the accepted `--servers` identifiers because `install_mcp_servers()` filters each selected name with `if server_name in MCP_SERVERS` at lines 877–888, then looks it up by that same key at lines 952–954.
- **`src/superclaude/cli/main.py`** (447 lines): Click exposes `superclaude mcp` at lines 215–257. `--servers/-s` is repeatable (line 216), values are converted to a list (line 249), and passed into `install_mcp_servers()` (lines 248–252). This is the only source-level CLI caller found so far.
- **Registry entries needing hardening review:**
  - Tavily: key/name `tavily`, `npx -y tavily-mcp@{TAVILY_MCP_VERSION}` and `TAVILY_MCP_VERSION = "0.2.20"` (`install_mcp.py:28–30,81–90`).
  - Sequential: key/name `sequential-thinking`; command `npx -y @modelcontextprotocol/server-sequential-thinking` (`install_mcp.py:35–41`).
  - Serena: key/name `serena`; direct Git install command `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --enable-web-dashboard false --enable-gui-log-window false` (`install_mcp.py:65–71`).
  - Morph: key/name `morphllm-fast-apply`; command `npx -y @morph-llm/morph-fast-apply` (`install_mcp.py:72–80`).
  - Auggie: key/name `auggie`; command `auggie --mcp --mcp-auto-workspace`; it additionally performs a PATH version probe and may run `npm install -g @augmentcode/auggie@latest` (`install_mcp.py:98–115,711–746`).
- **Rename effect:** a rename of a registry *key* is breaking for `superclaude mcp --servers <key>` and for interactive selection (the latter uses `list(MCP_SERVERS.keys())`, `install_mcp.py:932–938`). A changed registry `name` changes the exact installed Claude MCP registration and is therefore a migration/re-registration concern (`install_mcp.py:617,632–685,754–771`).

## Project configuration and documentation surface

### Configuration files

- **`.mcp.json:1–13`** is the task’s project-local configuration surface. It registers the *different* name `auggie-mcp` and launches `npx -y auggie-mcp`; this does not match the installer’s official `auggie` registry name/command (`install_mcp.py:98–115`). Any replacement with the official project-local executable changes that project registration’s tool namespace from `mcp__auggie-mcp__*` to the namespace produced by the replacement server. **[CODE-VERIFIED]**
- **`src/superclaude/mcp/configs/auggie.json:1–9`** duplicates the current official-style `auggie --mcp --mcp-auto-workspace` command shape, but it is a distributable config artifact, not read by the installer (the install path consumes only the Python `MCP_SERVERS` entry). **[CODE-VERIFIED]** command duplication; **[UNVERIFIED]** runtime consumption outside this repository.
- **`src/superclaude/mcp/configs/sequential.json:1–9`** matches the registry’s current Sequential package command token (`@modelcontextprotocol/server-sequential-thinking`). **[CODE-VERIFIED]** against `install_mcp.py:35–41`.
- **`src/superclaude/mcp/configs/serena.json:1–13`** still uses the floating `git+https://github.com/oraios/serena` installation, with fewer flags than the registry. **[CODE-CONTRADICTED]** with the goal’s official Serena 1.7.0 replacement; it must change if this distributable config remains in scope.
- **`src/superclaude/mcp/configs/serena-docker.json:1–14`** independently installs an unpinned `serena-ai` inside a Python Docker image. The build request calls for only verified Serena installation surfaces, but does not explicitly say whether this optional Docker config is in scope. **[UNVERIFIED]**—decide before editing.
- **`src/superclaude/mcp/configs/morphllm.json:1–13`** preserves the deprecated Fast Apply registry name/package and includes a hard-coded `/home/` argument. **[CODE-CONTRADICTED]** with the requested supported successor; update/remove only after its official server name and command are verified.
- The same legacy Serena and Morph config files exist under **`plugins/superclaude/mcp/configs/serena.json:1–13`** and **`plugins/superclaude/mcp/configs/morphllm.json:1–13`**. No source code examined imports these plugin artifacts. **[UNVERIFIED]** runtime use; treat them as documentation/plugin compatibility surfaces rather than installer inputs unless an owning workflow is identified.

### Public documentation and stale claims

- **`docs/user-guide/mcp-installation.md:15–33,60–63,95,161`** is the installer-facing catalog/examples. It uses all current registry selection keys (including `sequential-thinking`, `morphllm-fast-apply`, and `auggie`) and says `uv` is Serena’s prerequisite. **[CODE-VERIFIED]** selection-key agreement with `install_mcp.py:35–115,877–888`.
- **`docs/user-guide/mcp-servers.md:14–23,104–117,119–166,239–283`** duplicates concrete commands for Sequential, Morph Fast Apply, Serena Git install, and Tavily 0.2.20. The Sequential command matches the current registry. **[CODE-VERIFIED]**. The Serena snippet lacks the registry’s two GUI/dashboard flags; the two still share the floating Git source. **[CODE-CONTRADICTED]** in exact command shape with `install_mcp.py:65–71`.
- **`src/superclaude/mcp/MCP_Auggie.md:43–59`** documents the registry command and global `@augmentcode/auggie@latest` installation. **[CODE-VERIFIED]** against `install_mcp.py:98–115`, but **[CODE-CONTRADICTED]** with the requested project-local official executable configuration because it prescribes global installation.
- **`src/superclaude/mcp/MCP_Tavily.md:5,38–66`** is the canonical capability reference and explicitly pins `0.2.20`; it must change with the new pin. **[CODE-VERIFIED]** against `install_mcp.py:28–30,81–90`.
- **`docs/developer-guide/technical-architecture.md:274–286`** calls its JSON an MCP configuration and specifies `sequential-thinking-mcp@latest`, unlike the actual registry and config artifact (`@modelcontextprotocol/server-sequential-thinking`). **[CODE-CONTRADICTED]**—this is stale and should not be copied into new guidance.

## Downstream server-name impact

### Auggie: rename/migration is breaking downstream

- The project’s active `.mcp.json` server name is `auggie-mcp`, whereas the installer registry and current source guidance use `auggie` (`.mcp.json:3–9`; `install_mcp.py:98–115`; `MCP_Auggie.md:45–57`). This is already a split deployment surface, not a no-op configuration upgrade.
- **Runtime hooks:** `src/superclaude/hooks/hooks.json:60–67` and `src/superclaude/hooks/scripts/auggie-flag-clear.sh:22–32` explicitly match both `mcp__auggie__*` and `mcp__auggie-mcp__*`. The implementation supports coexistence, but removal/rename of the latter requires deciding whether to retain its compatibility matcher. **[CODE-VERIFIED]**
- **Evaluation runtime:** `src/superclaude/cli/eval/capabilities.py:218–248` registers both `mcp_server.auggie` and `mcp_server.auggie-mcp`; `src/superclaude/cli/eval/suites/real.yaml:36–41,112–140` has a required `mcp_server.auggie-mcp` capability and issues `mcp__auggie-mcp__ask_question`. A project-local replacement which removes `auggie-mcp` makes this real evaluation soft-skip unless its capability/test fixture/suite are migrated or an alias remains. **[CODE-VERIFIED]**
- **Tests that encode this namespace:** `tests/hooks/test_auggie_flag_clear_mcp_prefix.py:50–177`, `tests/cli/eval/test_capability_gates.py:43–73,130–154`, and `tests/cli/eval/test_coverage_gate.py:58–99`, plus the coverage-gate fixtures under `tests/cli/eval/fixtures/coverage_gate/` and `tests/cli/eval/fixtures/valid_suite.yaml` (enumerated by tracked-content search). These are only in scope if removing, rather than retaining, the `auggie-mcp` compatibility path.
- Many source commands/skills declare `auggie-mcp` in `mcp-servers:` metadata while other source documents call `mcp__auggie__codebase-retrieval` (for example, `src/superclaude/commands/brainstorm.md:6` versus `src/superclaude/commands/reflect.md:148–156`). **[CODE-CONTRADICTED]** naming convention; an Auggie rename must not blindly replace all strings without defining whether metadata names select a server or describe tool availability.

### Morph: installer-key rename is CLI/document breaking, not presently tool-namespace breaking

- `morphllm-fast-apply` is a public selection key in the registry (`install_mcp.py:72–80`) and in the all-servers command/catalog (`docs/user-guide/mcp-installation.md:18,30`) plus the detailed guide/config example (`docs/user-guide/mcp-servers.md:20,37,104–117,263–267,375`). Replacing it with the successor name without an alias makes these documented `superclaude mcp --servers morphllm-fast-apply` calls invalid because unknown keys are discarded at `install_mcp.py:877–888`. **[CODE-VERIFIED]**
- No active source/test references of an `mcp__morph...` or `mcp__morphllm...` tool namespace were found in the scoped tracked-code search. The older `morphllm` mentions are capability-routing prose/metadata, while `src/superclaude/cli/roadmap/remediate_executor.py` uses a separate, explicitly not-integrated MorphLLM probe per the tracked search output. Therefore no direct hook/eval tool-name rename is currently evidenced. **[UNVERIFIED]** successor namespace until primary vendor verification.

## Exact test impact and minimal test plan

1. **Update `tests/cli/test_install_mcp_tavily.py`** (377 lines): change every 0.2.20 backstop/string expectation to 0.2.22 while retaining its existing registry, argv, drift-reconciliation, scope, malformed-output, and API-key masking coverage (`:27–49,77–147,197–375`). This is mandatory: a 0.2.20 assertion is deliberately an upgrade-blocking backstop.
2. **Update `tests/docs/test_tavily_doc_alignment.py`** (130 lines): its scanner currently fails if any `tavily-mcp@...` token within `src/superclaude` or `docs` differs from 0.2.20 (`:12–85`). Change its expected pin to 0.2.22 and keep its non-vacuity assertion (`:65–73`). This is mandatory for `MCP_Tavily.md` and `docs/user-guide/mcp-servers.md` updates.
3. **Add `tests/cli/test_install_mcp_registry.py`**: parameterized/pure registry-command assertions for the changed Sequential, Serena, Morph successor, and Auggie entries. The existing Tavily file is intentionally Tavily-specific and contains shared fake subprocess helpers (`test_install_mcp_tavily.py:52–74,171–194`), so adding one focused registry test file avoids coupling unrelated server upgrades to Tavily defaults. Assert the exact `key`, `name`, `transport`, command string, and relevant environment/binary metadata only after primary-source verification.
4. **Add `tests/cli/test_mcp_project_config.py`**: parse root `.mcp.json` and assert the official project-local Auggie server key, executable, ordered arguments, and absence of `npx`/`auggie-mcp`. The build request explicitly requires a test for this configuration; no existing test validates `.mcp.json` (tracked-content search found only eval fixtures, not a root-config test).
5. **Conditional only—if `auggie-mcp` compatibility is removed:** update `tests/hooks/test_auggie_flag_clear_mcp_prefix.py`, `tests/cli/eval/test_capability_gates.py`, `tests/cli/eval/test_coverage_gate.py`, `tests/cli/eval/test_no_mcp_skip.py`, `tests/cli/eval/test_doctor.py`, and the cited eval fixtures/`real.yaml`, in lockstep with `hooks.json`, `auggie-flag-clear.sh`, and capability registry. If both prefixes remain supported, preserve these tests unchanged and add only a root-config assertion proving the project now selects official `auggie`.

## Gaps and questions

- **[UNVERIFIED]** The official exact commands/package IDs for Sequential 2026.8.31, Serena 1.7.0, Auggie 0.36.0, and the Morph successor are not verified in this integration pass; implementation must use primary vendor evidence before editing (per build request).
- **[UNVERIFIED]** Whether `serena-docker.json` and `plugins/superclaude/mcp/configs/*` are maintained installation surfaces. They contain the old Serena/Morph mechanisms, but no code path found reads them.
- **[CODE-CONTRADICTED]** Existing documentation has at least two stale command surfaces: Serena’s guide snippet omits registry flags, and the technical architecture document names a different Sequential package (`docs/user-guide/mcp-servers.md:268–271`; `docs/developer-guide/technical-architecture.md:274–286`). Do not use either as command authority.

## Summary for task building

Minimal unconditional file set: `src/superclaude/cli/install_mcp.py`, `.mcp.json`, `tests/cli/test_install_mcp_tavily.py`, `tests/docs/test_tavily_doc_alignment.py`, new `tests/cli/test_install_mcp_registry.py`, new `tests/cli/test_mcp_project_config.py`, `docs/user-guide/mcp-installation.md`, `docs/user-guide/mcp-servers.md`, `src/superclaude/mcp/MCP_Auggie.md`, and `src/superclaude/mcp/MCP_Tavily.md`; generated `.claude/` mirrors follow from `make sync-dev` and are not staged. Add `src/superclaude/mcp/configs/{serena,morphllm}.json` only after deciding that distributable configs are owned by this task. Treat all Auggie hook/eval changes as conditional on removing the `auggie-mcp` compatibility namespace.
