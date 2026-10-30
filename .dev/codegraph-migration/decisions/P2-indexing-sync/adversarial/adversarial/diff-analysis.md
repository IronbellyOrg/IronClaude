# Diff Analysis: P2 indexing-and-sync decision options

## Metadata
- Generated: 2026-10-29T16:30:00Z
- Variants compared: 3 (V1 = option-a, V2 = option-b, V3 = option-c; Mode A copies in this directory)
- Shared context read for every point: `../../context.md` (verified codegraph v1.6.2 behaviour, IronClaude hook facts)
- Verified by the orchestrator before analysis: index file is `.codegraph/codegraph.db` (sandbox `/tmp/codegraph-eval.fQfO/project/.codegraph/`); SessionStart in `src/superclaude/hooks/hooks.json` has 3 entries; `_FRESHNESS_SCRIPTS` is `src/superclaude/cli/install_hooks.py:42-79`.
- Total differences found: 26 (22 diff items + 4 promoted shared assumptions)
- Categories: structural (2), content (10), contradictions (2), unique (8), shared assumptions (4 promoted of 7 found)
- Taxonomy tags: L1 = surface, L2 = structural, L3 = state mechanics

## Structural Differences

| # | Area | V1 (A) | V2 (B) | V3 (C) | Severity | Level |
|---|------|--------|--------|--------|----------|-------|
| S-001 | Document shape | 4 bullets + strengths/weaknesses | 5 bullets with a 4-step numbered behaviour list | 3 bullets + strengths/weaknesses | Low | L1 |
| S-002 | Implementation specificity | Names only the CLAUDE.md file and a docs page | Names script path, hooks.json matcher/timeout, installer list, plugin mirror, env var, lock, log path | Names template path, 3 hook names, git config key; no script/test/uninstall detail | Medium | L2 |

## Content Differences

| # | Topic | V1 (A) | V2 (B) | V3 (C) | Severity | Level |
|---|-------|--------|--------|--------|----------|-------|
| C-001 | Who triggers the first index | Agent or user, after a "not initialized" reply | Claude SessionStart hook, detached background `codegraph init --yes` | Git template hooks on clone/checkout | High | L2 |
| C-002 | Freshness after the first index | Upstream watcher + connect-time catch-up | Same as A | Watcher + `codegraph sync --quiet` in git hooks | Medium | L3 |
| C-003 | Existing clones and sibling worktrees | Manual only | Any git checkout on its first session | Nothing until re-clone; worktrees only of templated repos | High | L2 |
| C-004 | Global state mutation | None | None (log under `${XDG_STATE_HOME:-~/.local/state}`) | Sets global `init.templateDir` | High | L2 |
| C-005 | Opt-out | Not needed | `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` | None stated | Medium | L2 |
| C-006 | Concurrent init control | Not addressed | `mkdir` lock | Ignores the daemon's lock error | Medium | L3 |
| C-007 | Where the 1 GB / seconds-to-minutes cost lands | Inside an agent turn | Detached, at the first session | Foreground in `git clone`/`checkout` unless backgrounded | Medium | L2 |
| C-008 | Core CLAUDE.md fallback rule | Defines it | Keeps it | Keeps it | Low | L1 |
| C-009 | Maintenance surface | Docs text only | 1 script + hooks.json + plugin mirror + `_FRESHNESS_SCRIPTS` + test pin | Installer code + 3 hook scripts + git config write + (unstated) uninstall | Medium | L2 |
| C-010 | Boundary guards | "at the git top-level" | Non-git skip, `$HOME` and `/` skip | Implicit (git only) | Medium | L3 |

## Contradictions

| # | Point of Conflict | Position 1 | Position 2 | Impact | Level |
|---|-------------------|------------|------------|--------|-------|
| X-001 | C runs sync during sessions while adopting A's rule | V3: hooks run `codegraph sync --quiet` "ignoring the lock error" | V3 also adopts V1's rule "never run `codegraph sync` while a session is open"; context.md: sync fails with a lock error while the daemon holds the writer lock | Medium | L3 |
| X-002 | Is a background 1 GB process at session start acceptable | V1: "no surprise 1 GB RSS process at session start" is a strength | V2: background cost "paid once per checkout" is acceptable | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V2 | Env opt-out `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` | Medium |
| U-002 | V2 | Skip non-git dirs, `$HOME`, `/` (mirrors `init`'s own refusal) | High |
| U-003 | V2 | Lock so two sessions do not both init | Medium |
| U-004 | V2 | Log outside the checkout | Low |
| U-005 | V3 | Freshness across pulls/branch switches with no MCP client | Medium |
| U-006 | V3 | Index ready before the first session | Medium |
| U-007 | V1 | Docs page listing `init --yes`, `uninit`, `codegraph.json` excludes | Medium |
| U-008 | V1 | Explicit rule "never run `codegraph sync` while a session is open" | High |

## Shared Assumptions

Found 7; STATED: A-001 `codegraph` must be on PATH (V2 checks it), A-002 one index per working tree at the git top-level (V1, V2, context), A-007 Coder covers Coder worktree creation (V1, context). Promoted UNSTATED points:

| # | Assumption | Source Agreement | Impact | Status | Level |
|---|------------|------------------|--------|--------|-------|
| A-003 | An existing `.codegraph/codegraph.db` means a complete index; an interrupted init (OOM, kill) never leaves a partial DB that is then skipped forever | V2 step 3, V3 "if no index exists", V1 "not initialized" trigger | High | UNSTATED | L3 |
| A-004 | codegraph is registered as an MCP server and connected in sessions, so the daemon watcher really provides freshness | All three rely on the watcher | High | UNSTATED | L3 |
| A-005 | Indexing every git repo a user opens is wanted (disk ~70 KB/file, ~1.9 GB at 27k files) | V2 and V3 auto-index everything | Medium | UNSTATED | L2 |
| A-006 | The agent can recognise "not initialized" from the MCP tool reply text (CLI `query` exits 1; MCP reply wording unverified) | All three keep the fallback rule | Medium | UNSTATED | L3 |

## Summary
- Structural 2, content 10, contradictions 2, unique 8, shared assumptions 7 (UNSTATED 4, STATED 3, CONTRADICTED 0)
- Diff points for convergence: 2 + 10 + 2 + 4 = 18
- Taxonomy coverage: L1 (S-001, C-008), L2 (8 points), L3 (C-002, C-006, C-010, X-001, A-003, A-004, A-006)
- Highest severity: C-001, C-003, C-004, U-002, U-008, A-003, A-004
- Similarity check: variants differ materially (>10%); debate proceeds.
