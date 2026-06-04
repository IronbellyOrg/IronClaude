# Enrichment: Codebase Integration Surfaces

Source: `mcp__auggie__codebase-retrieval` + verified file reads, 2026-06-04.
Quality tier: **primary** (Auggie ran cleanly).

## MCP registration mechanism

- Individual servers live in `src/superclaude/cli/install_mcp.py` → `MCP_SERVERS` dict
  (each entry: `name`, `description`, `transport: stdio`, `command`, `required`).
- Install path: `superclaude mcp --servers <name>` OR
  `claude mcp add --transport stdio --scope user <name> -- <binary> [args]`
  (Auggie precedent: `claude mcp add --transport stdio --scope user auggie -- auggie --mcp --mcp-auto-workspace`).
- AIRIS MCP Gateway is the preferred unified SSE endpoint (Docker), but individual
  stdio registration is fully supported and is the right fit for the three Rust binaries
  (`sem-mcp`, inspect MCP, weave MCP).
- ⇒ Incorporation = add 3 entries to `MCP_SERVERS` (sem/inspect/weave) + docs, behind a
  Rust/cargo availability check. Reversible via `claude mcp remove`.

## Skill-wiring targets (ranked by overlap)

1. **`sc-auggie-review-protocol`** (`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`)
   — 5-wave PR/diff review. Wave 1 collects diff+metadata+file list; Wave 2 runs
   `auggie --print --output-format json --ask`. **inspect overlaps Wave 1+2 directly**:
   `inspect_triage` could (a) pre-filter the diff to the riskiest entities before the
   Auggie pass (token savings), or (b) run as a second independent review engine to
   cross-validate (precision/recall complementarity). Its low precision (33%) argues for
   **pre-filter/advisory**, not replacement.
2. **`code-review` / `simplify`** (built-in skills) — review current diff. `sem diff` +
   `sem context` could supply entity-scoped, token-budgeted context to these.
3. **`sc:git`** — git operations. **weave** registers here as a merge driver (`weave setup`).
4. **Roadmap scanner + `cleanup-audit`** — diff/structure consumers. `sem entities` /
   `sem impact` could feed structural-risk signals (e.g., the Layer-5 scanner detectors).
5. **Worktree parallel dev** — CLAUDE.md documents heavy `git worktree` usage for parallel
   Claude sessions. **weave** is most valuable exactly here: merging concurrent worktree
   branches that touch the same files in independent functions = its core "false conflict"
   use case.

## New-dependency / risk notes

- **Rust/cargo** is NOT currently a framework dependency (UV-only Python). All three tools
  need it (or Homebrew/npm prebuilt binaries). This is the dominant maintenance-cost factor.
- `sem` binary name **collides with GNU parallel's `sem`** — must resolve (alias, full path,
  or `sem-cli` invocation) before any `sem setup` global git integration.
- weave **MCP tool names undocumented** — spike must enumerate them before MCP wiring.
- Source-of-truth: all skill edits in `src/superclaude/`, then `make sync-dev`. Never stage `.claude/`.
