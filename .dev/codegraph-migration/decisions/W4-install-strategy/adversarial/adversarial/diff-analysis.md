# Diff Analysis: install-strategy decision Comparison

## Metadata
- Generated: 2026-10-29T16:15:00Z
- Variants compared: 3
  - Variant 1 = `option-a.md` (IronClaude-owned verified tarball install)
  - Variant 2 = `option-b.md` (delegate to upstream `install.sh` + `codegraph install`)
  - Variant 3 = `option-c.md` (bake binary in Coder image; IronClaude verifies + registers)
- Evidence file: `.dev/codegraph-migration/research/codegraph-evaluation.md` sections 1-5
- Repo facts re-checked this run: `src/superclaude/cli/main.py:254-262` (Codebase Memory phase), `src/superclaude/cli/install_mcp.py:775-786` (`claude mcp add-json ... --scope user`), `src/superclaude/cli/install_core.py:62-71` (`--force` copies every core `.md`, including `CLAUDE.md`, over `~/.claude/`), `update.sh` (`pipx install --force ./`, `superclaude install --force`, `make sync-dev`, `superclaude doctor`), `src/superclaude/cli/install_codebase_memory.py:611-660` (`acquire_codebase_memory`: reuses an existing external executable, else runs the upstream bootstrap; Linux only)
- Total differences found: 22
- Categories: structural (2), content (12), contradictions (3), unique (10), shared assumptions (5 promoted; 3 stated, not promoted)

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|------|---------------|---------------|---------------|----------|
| S-001 | Section model | H1 + What it does / Strengths / Weaknesses | Same | Same | Low |
| S-002 | Granularity of "What it does" | 9 bullets incl. exact MCP JSON, layout, receipt, tests, Coder stance | 3 numbered steps + update + Coder stance | 3 bullets (image build, install-phase check, bump coupling) | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|-------|---------------|---------------|---------------|----------|
| C-001 | Binary acquisition | IronClaude downloads pinned `codegraph-<os>-<arch>.tar.gz` itself | Upstream `install.sh` fetched at pinned tag | Baked into Coder image at build time | High |
| C-002 | Integrity verification | SHA-256 per platform hard-coded in reviewed IronClaude source; optional `gh attestation verify` | None (install.sh does not check `SHA256SUMS`, eval §1/§5.2) | Pinned SHA-256 checked at image build (Coder only) | High |
| C-003 | MCP registration | IronClaude `claude mcp add-json codegraph {...alwaysLoad...} --scope user` | Upstream `codegraph install --target=claude --location=global --yes` | IronClaude `claude mcp add-json` (as A) | Medium |
| C-004 | Agent guidance location | `src/superclaude/core/CLAUDE.md` (survives `--force`) | Upstream marker block in `~/.claude/CLAUDE.md` (erased by next `superclaude install --force`) | `src/superclaude/core/CLAUDE.md` (as A) | High |
| C-005 | `UserPromptSubmit` prompt hook | Explicitly not installed | Installed (`codegraph prompt-hook`) | Not addressed | Medium |
| C-006 | Telemetry / update check | `CODEGRAPH_TELEMETRY=0`, `CODEGRAPH_NO_UPDATE_CHECK=1` in the MCP entry `env` | `codegraph telemetry off` (writes `~/.codegraph/telemetry.json`) | `CODEGRAPH_TELEMETRY=0` in image env; update check not addressed | Medium |
| C-007 | Install location / ownership | `~/.codegraph/versions/v1.6.2/` + `~/.local/bin/codegraph` (user-writable) | Same as A (upstream layout) | `/opt/codegraph/v1.6.2/` + `/usr/local/bin/codegraph` (root-owned) | Medium |
| C-008 | Version-bump / update vector | Edit pin + 4 hashes in IronClaude; `./update.sh` delivers | `./update.sh` re-runs installer; `codegraph upgrade` | Image rebuild + IronClaude pin bump, two repos in sync | High |
| C-009 | Coder image stance | Do not bake | Do not bake | Bake | High |
| C-010 | Non-Coder platforms | linux/darwin x64/arm64 via same code path | Whatever `install.sh` supports (linux/darwin) | Fails clearly, or falls back to A if both built | Medium |
| C-011 | Receipt / uninstall | Reuses the receipt pattern of `install_codebase_memory.py` | `codegraph uninstall` (also removes Claude config) | Image-owned; not addressed | Low |
| C-012 | Version check | Implicit (pin) | "a version check" (unspecified) | Explicit `codegraph --version` == IronClaude expected version | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) Position | Variant 2 (B) Position | Variant 3 (C) Position | Impact |
|---|-------------------|------------------------|------------------------|------------------------|--------|
| X-001 | Whether upstream may own Claude config | "no upstream installer editing `~/.claude.json`, `~/.claude/settings.json` or `~/.claude/CLAUDE.md` behind IronClaude's back" | "Upstream keeps its own config shape correct across releases" (while conceding the CLAUDE.md block is wiped by `--force`) | Sides with A (IronClaude registers) | High |
| X-002 | Which channel carries codegraph upgrades | `./update.sh` (IronClaude pin) | `./update.sh` / `codegraph upgrade` | Image rebuild; "`codegraph upgrade` cannot update a root-owned `/usr/local/bin` install"; "`./update.sh` may expect a newer one" | High |
| X-003 | Which option "matches current practice" | Claims to mirror `install_codebase_memory.py` (receipt) | Implicitly matches: current codebase-memory acquisition runs the upstream bootstrap (`install_codebase_memory.py:611-660`) | Claims to match the current baked `/usr/local/bin/codebase-memory-mcp` pattern | Medium |

Note on X-003: the repo shows the real current pattern is a hybrid: the Coder image bakes the binary, and IronClaude reuses an existing executable if found, otherwise acquires one (`acquire_codebase_memory`, "Reuse an executable or run the complete official bootstrap once"). Each variant matches one half.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | A | Optional `gh attestation verify` when `gh` is authenticated | Low (needs auth; writes sigstore cache under `$HOME`, eval §5.1) |
| U-002 | A | `CODEGRAPH_NO_UPDATE_CHECK=1` in the MCP env | Medium |
| U-003 | A | Mirror upstream on-disk layout so `codegraph upgrade`/`uninstall` still understand it | Medium |
| U-004 | A | Single-place version bump covered by unit tests | Medium |
| U-005 | A | Explicit decision not to install the prompt hook | Medium |
| U-006 | B | Prompt hook front-loads context | Low (measured 41-symbol payload per prompt, unchosen context cost) |
| U-007 | B | Upstream `--refresh` config migrations / legacy hook cleanup | Low |
| U-008 | C | No first-run 63 MB download / 286 MB per-home copy; works offline | Medium |
| U-009 | C | Root-owned, non-user-writable binary | Medium |
| U-010 | C | Explicit `codegraph --version` equality check with clear failure path, and a named fallback to A | High (this is the detection hook that makes an A+C combination work) |

## Shared Assumptions

Stated (documented, not promoted): all pin v1.6.2; all keep telemetry off; all replace the Codebase Memory phase in `superclaude install`.

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Installing the CLI + MCP is enough; per-project index state (`codegraph init` in each clone/worktree) is someone else's job | All three stop at install + register; eval §4 says nothing upstream runs `init` automatically, sibling worktrees answer "not initialized" | High | UNSTATED |
| A-002 | Claude CLI is present and `~/.claude.json` is writable at install time (guard on registration) | A and C call `claude mcp add-json`; B calls `codegraph install` which edits it | Medium | UNSTATED |
| A-003 | A bare `"command":"codegraph"` resolves to the intended binary in the Claude Code process PATH (`~/.local/bin` on PATH; when baked and user copies both exist, the right one wins) | All MCP entries use bare `codegraph` | High | UNSTATED |
| A-004 | Replacing the binary on update while a per-project daemon (outlives clients, 300 s idle, eval §5.7) is running is safe | All update paths swap the binary in place | Medium | UNSTATED |
| A-005 | Pinned GitHub release assets from a single-maintainer repo stay available | All fetch from github.com releases (C at build time) | Low | UNSTATED |

## Summary
- Total structural differences: 2
- Total content differences: 12
- Total contradictions: 3
- Total unique contributions: 10
- Total shared assumptions surfaced: 8 (UNSTATED: 5, STATED: 3, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-004, C-008, C-009, X-001, X-002, A-001, A-003
- Taxonomy pre-tag: L1 = S-001, S-002; L2 = C-001, C-003, C-004, C-005, C-007, C-008, C-009, C-010, C-011, X-001, X-002, X-003, A-005; L3 = C-002, C-006, C-012, A-001, A-002, A-003, A-004. All three levels have points.
- Similarity check: differences far exceed 10%; debate proceeds.
