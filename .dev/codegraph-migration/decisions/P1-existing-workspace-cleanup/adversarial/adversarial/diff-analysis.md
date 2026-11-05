# Diff Analysis: architectural-decision Comparison (P1 existing-workspace cleanup, issue #323)

## Metadata
- Generated: 2026-10-29T16:30:00Z
- Variants compared: 3
  - Variant 1 = option-a.md (registration-only retire step inside `superclaude install`)
  - Variant 2 = option-b.md (retire step + IronClaude-provable binaries + Serena uv tool)
  - Variant 3 = option-c.md (no automatic step; explicit consented command + handoffs)
- Shared fact base: `context.md` (same folder). Facts spot-checked read-only against source at 55d40308 (see "Spot-check log" below).
- Total differences found: 23 debatable points (+7 unique contributions)
- Categories: structural (2), content (10), contradictions (4), unique (7), shared assumptions (7)

## Spot-check log (read-only, orchestrator)

| Claim in context/variants | Source checked | Result |
|---|---|---|
| `update.sh` runs 4 commands in order, `set -euo pipefail` | `update.sh:2,7-10`; `tests/cli/test_update_script.py:13-18,81-88` | Confirmed. NEW detail: `set -euo pipefail` plus the test at `:81-88` mean a non-zero `superclaude install` exit stops `make sync-dev` and `superclaude doctor`. |
| Required codebase-memory phase in install | `src/superclaude/cli/main.py:254-275` | Confirmed; failure sets exit 1. |
| `read_user_mcp_entry` reads only top-level `mcpServers`, rejects duplicate keys, honours `CLAUDE_CONFIG_DIR` | `install_mcp.py:714-754` | Confirmed. |
| `_run_registration_command` 60 s timeout, no output echo | `install_mcp.py:766-772` | Confirmed. |
| `_cleanup_user_native_registration` removes exact user entry, re-reads to verify | `install_mcp.py:916-948` | Confirmed; hard-coded to `codebase_memory.BINARY_NAME`. |
| Existing matcher for IronClaude-written codebase-memory entry | `install_mcp.py:757-763` | NEW detail: existing matcher requires `command == str(executable)` exactly (full path), stdio, `args == []`. Option A proposes a looser basename match. |
| Install already removes/replaces an exact user entry with no prompt | `install_mcp.py:874-895` | NEW detail: prompt-free `claude mcp remove ... --scope user` followed by `add-json` is existing install behaviour. The consent gate at `:981-986` applies only to the account-wide native uninstall. |
| Serena registry pin | `install_mcp.py:55-61` | Confirmed (current). NEW detail (git `0e7bc31f`): earlier IronClaude releases registered `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --enable-web-dashboard false --enable-gui-log-window false`. Option A's `serena-agent` substring matcher would not match that older IronClaude-written shape. |
| How IronClaude stores a registry server | `install_mcp.py:1142-1159` | `claude mcp add --transport stdio [--scope user] <name> -- <shlex.split(command)>`, so the stored entry is `command` = first token (`uvx`), `args` = remaining tokens. Exact argv comparison is possible. |
| Hook matcher names Serena tools | `src/superclaude/hooks/hooks.json:47` | Confirmed; refreshed in place under `--force` (`install_hooks.py:393-431`). |
| Missing-CLI skip pattern | `install_user_setup.py:251-258` | Confirmed (`shutil.which("claude")` -> "claude CLI not found; skipped", success). |
| Kind-B IronClaude-written files | `install_codebase_memory.py:81-86` | NEW detail: IronClaude writes two private files next to the binary: receipt `~/.local/bin/.superclaude-codebase-memory.json` and marker `~/.local/bin/.superclaude-codebase-memory.pending`. No variant handles the `.pending` marker. |
| Coder `catalogue/ironclaude/install.sh`, Coder bundle behaviour | not in this repo | Taken from `context.md` as given; UNVERIFIED here. |

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|------|---------------|---------------|---------------|----------|
| S-001 | Section set | What it does (6 steps) + Implementation/Sunset paragraph + stale-primitives note + For/Against | What it does (4 steps, delta over A) + For/Against | What it does (5 steps) + For/Against | Low |
| S-002 | Self-containment | Fully self-contained | Defined as "Everything in Option A, plus..." (depends on Variant 1 text) | Self-contained, but "shape-matched" left undefined | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|-------|---------------|---------------|---------------|----------|
| C-001 | Trigger point | Automatic, end of every `superclaude install` (reached by `update.sh` and Coder) | Same as A | No automatic step; new explicit `superclaude mcp --retire-legacy [--dry-run] [--yes]` with interactive confirm | High |
| C-002 | What is removed automatically | Exact user-scope `codebase-memory-mcp` and `serena` registrations only | A + kind-B binary via upstream `codebase-memory-mcp uninstall -y`, updater `~/.local/bin/install.sh`, receipt; + `uv tool uninstall serena-agent` (opt. `uv cache clean`) | Nothing automatically | High |
| C-003 | Ownership proof for registrations | Shape matcher: cbm = stdio, `args []`, basename `codebase-memory-mcp`, no env/headers; serena = stdio, argv contains `serena-agent` and `start-mcp-server`, no env/headers | Inherits A; receipt + sha256 for kind-B binary | "shape-matched" (undefined) | Medium |
| C-004 | Failure semantics | Non-fatal: warning, install exit code unchanged; missing `claude` -> skip with note | Non-fatal, non-interactive | Install only prints a notice; the explicit command's failure semantics unspecified | Medium |
| C-005 | Data (indexes, caches, `~/.serena`, project `.serena/`) | Kept; prints manual delete command | Kept; prints how to delete | Kept (prints manual commands) | Low |
| C-006 | Coder workspaces | Same step runs; acknowledges bundle re-adds `serena` until Coder changes | Also uninstalls Coder-installed uv tool; bundle reinstalls; health-check churn | Entirely delegated to Phase 2 Coder handoff | Medium |
| C-007 | Time budget vs Coder 60 s bound | <= 2 CLI calls, timeout lowered to 10 s | Upstream uninstall 60 s + uv 30 s (exceeds bound) | None added to install | Medium |
| C-008 | Kind-B workspaces (IronClaude ran upstream installer) | Print `codebase-memory-mcp uninstall -y` | Automate receipt-gated upstream uninstall for one release | Print manual commands | Medium |
| C-009 | Missing `claude` CLI | Explicit skip-with-note (install_plugins pattern) | Not stated | Not stated | Low |
| C-010 | Lifecycle of migration code | `RETIRED_MCP_SERVERS` table with sunset comment | Keeps slimmed `install_codebase_memory.py` receipt logic for one release | New flag/help/docs/tests to remove later | Low |

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact |
|---|-------------------|---------------|---------------|---------------|--------|
| X-001 | Is prompt-free removal of an exact user MCP entry allowed? | Yes (keeps "exact user scope, CLI-only mutation, verify") | Yes, and even account-wide upstream uninstall prompt-free | No: "Keeps the existing consent rule for every removal (no prompt-free mutation of the user's MCP configuration)". Source evidence: `install_mcp.py:874-883` already does prompt-free exact-entry remove during install; consent gate `:981-986` is for account-wide native removal only. | High |
| X-002 | Who owns the `serena-agent` uv tool? | Coder (print `uv tool uninstall serena-agent`) | IronClaude may remove it | Coder (manual command / handoff) | High |
| X-003 | Does `./update.sh` alone satisfy the goal? | Yes | Yes | No (C's own "Against" concedes it) | High |
| X-004 | May IronClaude remove a `serena` entry that, on Coder, Coder's bundle wrote? Goal: "Leftovers owned by the Coder image ... are handed off, not removed by IronClaude." | Removes it (argv indistinguishable from IronClaude's registry pin) | Removes it | Hands Coder's off; dev workspaces only via explicit command | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Name-parameterised `_cleanup_user_native_registration`, reused by Phase 2 codegraph registration | Medium |
| U-002 | A | Same-name entry with a different shape is kept and reported "kept: not an IronClaude registration" | High |
| U-003 | A | Stale-primitive / hook-matcher analysis: nothing retired in Phase 1; forced install rewrites matcher and `~/.claude/CLAUDE.md` | Medium |
| U-004 | B | Receipt + sha256 ownership proof for the kind-B binary | Medium |
| U-005 | C | Read-only dry-run preview of what would be removed | Medium |
| U-006 | C | One-line install notice when legacy registrations are present | Low |
| U-007 | A | Sunset condition tied to Coder image/bundle no longer shipping either server | Low |

## Shared Assumptions

Agreement points scanned: (1) all keep indexes/caches/memories; (2) all restrict mutation to exact top-level user scope; (3) all mutate only through `claude mcp remove --scope user` and verify; (4) all treat binaries/uv tools on Coder as at least partly Coder's; (5) all print manual commands for what they do not remove.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| — | (1) | Deleting indexes/memories is not required by the goal | STATED (A step 4, B step 3, C step 2; `install_codebase_memory.py:74-78`) | No |
| — | (2),(3) | Exact user scope + CLI-only mutation is the safety boundary | STATED (A step 3-4) | No |
| A-001 | (3) + C-003 | The only `serena` shape IronClaude ever wrote is the current `serena-agent==1.7.0` pin | CONTRADICTED (git `0e7bc31f`: earlier IronClaude wrote the `git+https://github.com/oraios/serena ... --context ide-assistant` form) | Yes (flagged) |
| A-002 | (2) | Entry shape is sufficient proof of IronClaude ownership; an identical hand-made entry may be removed | UNSTATED | Yes |
| A-003 | (1)-(3) for A/B | The retire step is reached on every install path: without `--force` (Coder non-SHA-change start), and even when an earlier install step failed | UNSTATED | Yes |
| A-004 | (3) | `claude mcp remove --scope user` resolves the same file as `read_user_mcp_entry` (`CLAUDE_CONFIG_DIR`), and a concurrent Claude session rewriting `~/.claude.json` cannot resurrect the entry unseen | UNSTATED | Yes |
| A-005 | (5) | The printed upstream `codebase-memory-mcp uninstall -y` still works after IronClaude has already removed the user registration (ordering) | UNSTATED | Yes |
| A-006 | (5) | IronClaude-written kind-B files (receipt `.superclaude-codebase-memory.json`, marker `.superclaude-codebase-memory.pending`) need no handling (A, C silent; B removes receipt only) | UNSTATED | Yes |
| A-007 | (3) | Removing a registration while Claude sessions are running is safe (running sessions keep the server until restart; nothing breaks) | UNSTATED | Yes |

### Promoted Shared-Assumption Diff Points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Only the current serena pin was ever written | C-003 matcher | High: older IronClaude-written entries survive (goal miss) or a broad substring matcher hits user entries | CONTRADICTED — debate |
| A-002 | Shape == ownership | Exact-user-scope agreement | Medium: an identical hand-registered entry is removed | UNSTATED — debate |
| A-003 | Step reached on every install path | Automatic-trigger agreement (A/B) | High: goal miss on Coder non-`--force` starts or after an earlier failure | UNSTATED — debate |
| A-004 | Same config file + no concurrent resurrection | CLI-only mutation | Medium | UNSTATED — debate |
| A-005 | Upstream uninstall order-independent | Print-manual-command agreement | Low | UNSTATED — debate |
| A-006 | IronClaude receipt/marker files ignorable | Hand-off agreement | Medium: IronClaude-owned companion files left behind (goal says none left) | UNSTATED — debate |
| A-007 | Live-session removal safe | CLI-only mutation | Low | UNSTATED — debate |

## Summary
- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 4
- Total unique contributions: 7
- Total shared assumptions surfaced: 9 (UNSTATED: 6, STATED: 2, CONTRADICTED: 1); promoted: 7 (A-001..A-007)
- Debatable diff points (convergence denominator S+C+X+A): 2 + 10 + 4 + 7 = 23
- Highest-severity items: C-001, C-002, X-001, X-002, X-003, A-001, A-003
- Similarity check: variants differ materially (well above 10%); debate proceeds.
