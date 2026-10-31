**Phase 2 (install codegraph) progress: G1 installer core**

- Commits on `ironbelly/feat-codememory-codegraph-init`: ef172df0 `feat(install): add pinned, checksum-verified codegraph acquisition` (Tasks 3 and 4), 5b493cae `feat(mcp): register codegraph at user scope with exact-entry repair` (Task 5)
- Done: Task 3 (tool-list size check: byte delta D = 7597, undecided band; four live `claude -p` runs gave T = 1861 tokens <= 2000, so `MCP_TOOLS` = `node,search,callers,callees,impact,files,status`; explore is hidden and a call to it errors; the 2K threshold and band edges are still proposals, not user-confirmed). Task 4 (pinned, SHA-256-verified acquisition module and 30 tests). Task 5 (user-scope registration with exact-entry repair, bounded runner, registry entry and dispatch, shape probe stored in `P2-add-json-shape.json`).
- Tests: `uv run pytest tests/cli/test_install_codegraph.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/recommend -q -p no:cacheprovider` -> 389 passed, 1 skipped. Wider run `tests/cli tests/unit tests/recommend tests/core` (without `tests/cli/eval`) -> 1715 passed, 3 skipped. `ruff check` clean.
- Decisions taken: all logged in `.dev/codegraph-migration/decisions/P2X-log.md` (all "self"; no adversarial run was needed)
- Next: G2 CLI wiring and Serena retirement (Tasks 6-8)

