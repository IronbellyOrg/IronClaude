# Round 1: Advocate for Variant 1 (Option A)

Persona: architect (structure, dependencies, long-term impact) with analyzer rigor.
Sources spot-checked read-only: `src/superclaude/cli/main.py:60-275`, `src/superclaude/cli/install_mcp.py:55-61,714-999`, `src/superclaude/cli/install_codebase_memory.py:74-86`.

## Position summary

Option A, amended. Make the matchers exact, delete the two private files IronClaude wrote, and keep Option C's Coder handoff. Option A is the only option that meets the goal through `./update.sh` alone. It adds no new kind of destructive behaviour, so it stays within the existing safety rules. Its weak spot is its matchers, and that can be fixed: they should be exact argument-list allowlists like the existing matcher at `install_mcp.py:757-763`, not basename or substring checks.

## Steelman of Variant 2 (Option B)

B is the only option that leaves workspaces where IronClaude ran the upstream installer (kind B) actually clean, with no human step. That matches the goal's "leave no... binary registration... companion". It also reuses receipt-plus-sha256 ownership proof that already has tests instead of inventing a new one.

## Steelman of Variant 3 (Option C)

C refuses to touch anything Coder wrote. That is a literal reading of "Leftovers owned by the Coder image... are handed off". It adds a dry-run preview, and it leaves both the pinned `update.sh` and the install's time budget unchanged.

## Strengths claimed

1. **The step really is reached.** Install has no early return after the `--list` branch. Every step runs and failures are only collected for `sys.exit(1)` (`main.py:189-275`). The native phase is not gated on `--force` (`main.py:255`). A step placed before `main.py:264` therefore runs on every path, including a Coder start without a SHA change.
2. **No new class of mutation.** Install already removes an exact user entry with no prompt (`install_mcp.py:874-895`). The consent gate at `install_mcp.py:981-986` covers only the account-wide native uninstall.
3. **Reuses existing pieces.** It builds on `read_user_mcp_entry` (`install_mcp.py:714-754`) and a name-parameterised `_cleanup_user_native_registration` (`install_mcp.py:916-948`), which Phase 2 also needs.
4. **Fits the time limit.** It does two file reads and at most two CLI calls, well inside Coder's 60 s bound.
5. **Keeps same-name entries that are not ours.** An entry with the same name but a different shape is kept and reported (U-002).

## Weaknesses in Variant 2

1. It runs `uv tool uninstall serena-agent` on a tool that Coder's bundle installed, with no ownership proof. That contradicts the handoff clause, and B's own "Against" admits it churns Coder's health check.
2. It runs the upstream account-wide uninstall with no prompt. The current code forbids exactly that without confirmation (`install_mcp.py:981-986`).
3. Its timeouts (60 s plus 30 s) exceed Coder's 60 s total bound.
4. It keeps part of `install_codebase_memory.py` alive in the phase meant to delete it, to serve kind-B workspaces whose existence is UNVERIFIED.

## Weaknesses in Variant 3

1. By C's own admission it fails the goal on `./update.sh` (X-003).
2. Its central premise is wrong. Install already removes user MCP entries with no prompt (`install_mcp.py:874-895`), so "no prompt-free mutation" is not an existing rule.
3. "Shape-matched" is never defined (S-002).
4. It adds a flag, help text, docs and tests that exist only for the migration and must be removed later.
5. Coder workspaces depend entirely on another repo's schedule.

## Concessions

- A's serena substring matcher misses the older shape that IronClaude itself wrote (A-001). It is also looser than the exact path check at `install_mcp.py:757-763`. **Fix:**
  - `codebase-memory-mcp`: match only the exact commands `/usr/local/bin/codebase-memory-mcp` and `~/.local/bin/codebase-memory-mcp`, with `args []`.
  - `serena`: match only the exact command `uvx` plus the argument list of each of the two known shapes (`install_mcp.py:59` and the older `git+https://github.com/oraios/serena ... --context ide-assistant` form). This works because entries are stored as their first token plus the remaining arguments (`install_mcp.py:1142-1159`).
- On Coder, A removes a `serena` entry that Coder's bundle wrote (X-004). The removal is harmless, but A still needs C's Coder handoff to end the churn.
- C's dry-run preview is worth adopting as a read-only `--dry-run` path.

## Shared-assumption responses

- **A-001: ACCEPT** (the contradiction is real). Fix it with the exact allowlist of both known shapes above.
- **A-002: QUALIFY.** A hand-made entry with an exact known shape and no env or headers is functionally identical to ours and can be re-added with one command. Print that command.
- **A-003: QUALIFY.** The step is reached on every path (`main.py:189-275`). It must sit before `main.py:264` and catch its own exceptions; an uncaught exception from an earlier step would still bypass it.
- **A-004: QUALIFY.** The reader honours `CLAUDE_CONFIG_DIR` (`install_mcp.py:731-736`). Whether the Claude CLI resolves the same file is UNVERIFIED. The re-read after removal catches a mismatch. A concurrent rewrite by another session is a risk the existing path (`install_mcp.py:874-898`) already accepts.
- **A-005: QUALIFY.** It is UNVERIFIED whether the upstream uninstall tolerates an already-removed registration. Print its command before A's removal message and label it for kind-B workspaces only.
- **A-006: REJECT.** The receipt and the `.pending` marker are written by IronClaude (`install_codebase_memory.py:81-86`). A should delete both when they are regular, single-link files.
- **A-007: ACCEPT.** Install already removes and re-adds entries while sessions are running (`install_mcp.py:874-895`). Print "restart Claude sessions".

## Per-point preference table

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | It is the only option that covers stale primitives and sunset. |
| S-002 | A | Fully self-contained; B depends on A's text and C leaves "shape-matched" undefined. |
| C-001 | A | An automatic step is the only way to meet the goal on the `update.sh` path. |
| C-002 | A | Removes registrations only and leaves Coder-owned software alone. |
| C-003 | merge: A plus exact argument-list allowlist | The basename and substring checks are too loose. |
| C-004 | A | Non-fatal, and the missing-CLI skip is specified. |
| C-005 | tie (all) | All keep data and print how to delete it. |
| C-006 | merge: A plus C's Coder handoff | Ends the bundle re-adding `serena`. |
| C-007 | A | Fits the 60 s bound; B exceeds it. |
| C-008 | merge: A's printed command plus deleting the receipt and marker | Removes IronClaude's own files without touching the binary. |
| C-009 | A | The only option that states the missing-CLI behaviour. |
| C-010 | A | The sunset is tied to Coder dropping both servers. |
| X-001 | A | Prompt-free exact-entry removal is existing behaviour (`install_mcp.py:874-895`). |
| X-002 | A or C | The uv tool is Coder's, so print the command rather than run it. |
| X-003 | A | B also meets it, but at a cost in safety and time. |
| X-004 | merge: A plus C's handoff | Dev workspaces need the removal; Coder's entry is handed off. |
| A-001 | merge | Exact allowlist covering both known shapes. |
| A-002 | A, plus print the re-add command | Removal loses nothing the user cannot restore. |
| A-003 | A | Placed before `main.py:264` with its own exception guard. |
| A-004 | A | The verify re-read catches a mismatch. |
| A-005 | A | Print the upstream command first and label it. |
| A-006 | B's direction, extended to the marker | Delete IronClaude-written files only. |
| A-007 | A | Add the restart note. |
