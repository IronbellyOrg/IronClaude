---
cluster: C8
title: Core reference + docs alignment with tavily-mcp 0.2.x
convergence_score: 0.90
adversarial_status: pass
base_variant: opus:technical-writer
created: 2026-06-23
---

# C8 Merged Spec — Core Reference + Docs

## Convergence summary
2 variants (opus:technical-writer, sonnet:qa), high agreement. Docs must reflect (not re-decide) the cross-cluster decisions and POINT to source of truth (MCP_Tavily.md / install_mcp.py), never duplicate param tables. Both flag the same risk: over-editing docs into duplicated tool schemas recreates the drift the upgrade removes.

**New finding (techwriter, verified-worthy):** `docs/reference/comprehensive-features.md:~98` lists the now-DELETED `tavily.json` in a config inventory → dangling pointer; correct the earlier "no doc edit for the deletion" assumption — this single reference needs removal.

## Decisions / concrete edits (by file)
| File | Edit |
|------|------|
| `docs/user-guide/mcp-servers.md:273` | `tavily-mcp@latest` → `tavily-mcp@0.2.20` (the only version string in docs; kills the third stance). |
| `docs/user-guide/mcp-servers.md:~138` | "Node.js 16+" → "Node.js 18+" (installer `check_prerequisites` requires 18+). |
| `docs/user-guide/mcp-servers.md:~136` | one broadened capability line: "search, extraction, site-mapping, domain-crawl — see MCP_Tavily.md" (pointer, no param table). |
| `docs/reference/comprehensive-features.md:~75` | one broadened tavily capability line + pointer to MCP_Tavily.md. |
| `docs/reference/comprehensive-features.md:~98` | **remove the deleted `tavily.json`** from the config inventory. |
| `src/superclaude/core/FLAGS.md` (`--tavily`) | broaden Behavior from search-only → "search/extract/map/crawl" + pointer to MCP_Tavily.md. **Then `make sync-dev` + `make verify-sync`** (core/ syncs to .claude/). |
| `docs/eval/retry.md:~138` | `requires: [mcp.tavily]` → `requires: [mcp_server.tavily]` (C7 stale-token fix). |
| Need NOTHING | `core/MODES.md`, `core/COMMANDS.md`, `docs/user-guide/{mcp-installation,commands,flags,modes,agents}.md`, `docs/mcp/{mcp-integration-policy,mcp-optional-design}.md`, `docs/reference/basic-examples.md` — name-only mentions, no version/param/install specifics. |
| EXCLUDED | `docs/research/*`, `docs/analysis/*` — research-output artifacts, not integration docs. |

## Verification / tests (`tests/docs/test_tavily_doc_alignment.py`)
| Test | Asserts |
|------|---------|
| `test_tavily_version_single_pin` | every `tavily-mcp@<ver>` string in `src/superclaude/` + in-scope `docs/` is exactly `0.2.20` (or pulls from one constant) — **highest-value guard**, catches installer/docs mismatch pre-release |
| `test_no_stale_mcp_tavily_token` | no `mcp.tavily` anywhere in src/docs/eval; only `mcp_server.tavily` (shared with C7) |
| `test_no_tavily_json_references` | no doc references `configs/tavily.json` (it's deleted) |
| `test_docs_no_default_params_duplication` | in-scope docs name tools/capabilities + link to MCP_Tavily.md but do not duplicate DEFAULT_PARAMETERS values |

## Acceptance criteria
- AC1: All tavily version strings = `0.2.20`; drift test green.
- AC2: No stale `mcp.tavily`; no `tavily.json` references.
- AC3: map/crawl mentioned via one-line pointers only (no duplicated param tables).
- AC4: FLAGS.md edited in src/ then synced (`verify-sync` green).
- AC5: Node version reads 18+ where the installer requires it.

## Cross-cluster handoffs
- Consumes C1 (version 0.2.20, tavily.json deletion), C2 (MCP_Tavily.md canonical + map/crawl), C7 (`mcp_server.tavily` token).
- `test_tavily_version_single_pin` is the shared release guard for the whole upgrade.
- **Mandatory sync:** FLAGS.md lives in `src/superclaude/core/` → after editing, `make sync-dev` (never edit `.claude/` directly).
