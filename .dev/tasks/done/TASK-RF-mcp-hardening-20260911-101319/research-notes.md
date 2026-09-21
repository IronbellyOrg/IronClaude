# Research Notes: MCP installer hardening

**Date:** 2026-09-11
**Scenario:** A
**Depth Tier:** Standard
**Track Count:** 1
**Status:** Complete

## EXISTING_FILES
- `src/superclaude/cli/install_mcp.py`: project MCP registry and exact-command drift reconciliation.
- `src/superclaude/cli/main.py`: `superclaude mcp` CLI entry point.
- `tests/cli/test_install_mcp_tavily.py`: registry-pin and re-registration regression tests.
- `tests/docs/test_tavily_doc_alignment.py`: pinned Tavily documentation alignment test.
- `docs/user-guide/mcp-installation.md`: public installer catalog and examples.
- `src/superclaude/mcp/MCP_Auggie.md`: official Auggie guidance.
- `.mcp.json`: project-local Claude Code MCP registration, currently third-party `auggie-mcp`.

## PATTERNS_AND_CONVENTIONS
- `MCP_SERVERS` in `install_mcp.py` is the registry source of truth.
- Existing install logic compares an exact registered command and only re-registers the precise existing server when it differs.
- Tavily uses `TAVILY_MCP_VERSION` as the version single source of truth with literal backstop assertions in tests.
- Distributable source changes are made in `src/superclaude/`, then copied to `.claude/` with `make sync-dev`; generated `.claude/` paths are never staged.
- Tests use pytest through UV and intercept subprocess calls rather than installing MCPs.

## GAPS_AND_QUESTIONS
- Re-verify release/version identities from primary official sources immediately before edits because initial research had conflicting registry observations for some unrelated packages.
- Confirm the documented Serena 1.7.0 command and context option; preserve required project discovery behavior.
- Confirm Morph's current documented command and stable server name; ensure the replacement's tool contract is a valid successor.
- Do not modify Context7, Playwright, Chrome DevTools, Magic, AIRIS, Markdown Collab, or user-level Codebase Memory in this task.

## RECOMMENDED_OUTPUTS
- `research/01-registry-tests.md`: inventory registry fields, reconciliation behavior, and existing test patterns.
- `research/02-docs-config.md`: document/config surfaces and source-of-truth rules.
- `research/03-official-releases.md`: primary-source verification for included and excluded MCPs.
- `research/04-integration-impact.md`: caller/test impact and minimal file list.

## SUGGESTED_PHASES
1. Verify official release data and local ownership boundaries.
2. Update the MCP registry and project-local official Auggie configuration.
3. Update targeted regression and documentation-alignment tests.
4. Update public docs/source guidance.
5. Sync generated development mirrors and run focused/full validation.

## TEMPLATE_NOTES
Use Template 02 because the task must verify external package facts before changing installation behavior, modifies code/config/tests/docs, and must validate sync output.

## AMBIGUITIES_FOR_USER
None — implementation scope is explicitly bounded to verified, project-owned MCP configuration surfaces.
