---
version: "1"
priority: Medium
created_date: "2026-10-23"
---

# Correct automatic-gateway inclusion claims

Source: ../REPORT.md (Correct automatic-gateway claims); ../../mcp-installation.md
Goal: Correct the repository instruction's automatic MindBase-inclusion assurance while preserving supported gateway/native installation and the separate manual deployment.

## Constraints

- Written plan only, using the registered simple-task template; not a managed workflow package and not executed. Separate implementation authorization is required.
- Product allowlist is repository-root `CLAUDE.md`, only its `MCP Server Integration` gateway recommendation/service-inclusion paragraph (current lines 353-368). Preserve all unrelated rules and individual-server guidance. Do not edit global `~/.claude/CLAUDE.md` or installed core copies.
- Preserve `src/superclaude/cli/install_mcp.py`, native lifecycle helpers, ordinary install/update, all MCP descriptors/manual guides, mixed-selection behavior, Unicode/result handling and February configuration/health/SSE fixes byte-for-byte.
- Do not run installers, Docker, registrations, home-folder writes, remote lookups or a historical revert. Do not label the separate manual clone/Compose deployment disproved.
- No hard dependency on legacy/plugin/memory edits; this is recommended fourth only to keep the documentation follow-through separate. The memory plan owns memory-specific policy wording; this plan does not edit that policy.
- Before authorized edits, capture a fresh checkout/branch/HEAD/status and protected-file hash baseline. Keep task-owned checks/evidence under `../implementation-evidence/04-gateway-claims/`; use UV for Python.
- No staging, commits, pushes, PR operations or remote branch deletion. Preserve the completed sync/Codecov cleanup and all pre-existing work. Independent final review must verify the exact one-file boundary.
- Service availability, downloadable upstream contents, advertised tool/token counts, runtime behavior and effort remain UNVERIFIED.

## Phase 1: Make the built-in recommendation accurate

## Task 1: Qualify the gateway-service assurance in repository instructions

Read the validation report's automatic-gateway section, repository `CLAUDE.md` gateway paragraph, `src/superclaude/cli/install_mcp.py:293-358`, and the two manual resource guides `src/superclaude/mcp/MCP_Airis-Agent.md:15-21` / `src/superclaude/mcp/MCP_Mindbase.md:20-29`. Re-anchor before edits; old line numbers are pointers, not an exact substitution command.

Capture a baseline. Change only the repository gateway recommendation/included-services assurance to distinguish the built-in automatic installation from separate manual clone/Compose setup. Explain that, on successful download of a fresh backend template, the installer disables `mindbase` and `airis-agent` because their containers are not included in the distribution Compose file. Existing configuration is reused; fallback/parse-failure paths differ. Do not generalize the normal fresh-template behavior into a guarantee about every existing or manual deployment. Preserve the supported gateway default/recommendation and individual/native server guidance. Qualify untested service/tool-count/token-savings claims in this same paragraph rather than asserting measurements.

Add a small task-owned static check comparing the exact changed paragraph boundary and hashes of the protected implementation/manual guides/descriptors. Check the corrected description against the source branches, not a live network service. Record commands and outcomes under the task evidence directory.

Acceptance criteria:
- `CLAUDE.md` is the only changed product file, and only the gateway paragraph changes. Its automatic inclusion assurance now discloses the successful fresh-template disabling condition without asserting all installations behave identically.
- The text distinguishes manual clone/Compose deployment and leaves its availability explicitly UNVERIFIED; it neither says manual MindBase is disproved nor promises an implemented PM MindBase backend.
- Gateway, native, individual and mixed-selection behavior, Unicode/result guards and the February repair remain byte-identical, as do resource JSON examples/manual guides and all unrelated repository instructions.
- A runnable static boundary/preservation check succeeds and its output is retained. No Docker, download, registration, installer, test suite, home write or remote mutation is necessary or performed for this text correction.
- A fresh independent review verifies wording against live source and the exact one-file diff. Unmeasured service availability/tool counts/token reduction remain marked UNVERIFIED; no runtime success is inferred from corrected prose.
