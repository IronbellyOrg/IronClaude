# Round 2: Advocate for Variant 2 (Option B), rebuttals

Sources re-checked read-only: `install_mcp.py:52-62,1310-1330`, `git show 0e7bc31f` (`install_mcp.py` and docs hunks), `install_codebase_memory.py:28,74-86,323-390`.

## Responses to criticisms

**1. Keeping the receipt-gated removal behind consent costs too much (A). Conceded.** My narrowed B needed the bounded supervisor, the receipt parser and their tests to stay in the codebase, all for kind-B workspaces whose existence is UNVERIFIED. The path it keeps waits up to 300 s (`install_codebase_memory.py:28`, `:352-355`). A's amended rule gets the part of B that mattered: delete IronClaude's receipt and `.pending` marker only when `~/.local/bin/codebase-memory-mcp` is absent and each file is a regular, single-link, user-owned file. When the receipt is present, A keeps the registration and prints `codebase-memory-mcp uninstall -y`, which keeps the existing order (native uninstall first, `install_mcp.py:993-999`). I accept that rule in full. B's automated binary removal is withdrawn.

**2. Should the serena entry be removed automatically on dev workspaces? Partly withdrawn, with one split I still argue for.**
- **Against my Round 1 position:** the current pin `uvx --from serena-agent==1.7.0 ... --context claude-code --project-from-cwd ...` (`install_mcp.py:59`) is byte-identical to Coder's bundle argv (context.md:13). IronClaude cannot tell whether it wrote this entry or Coder did. Unlike the codebase-memory entry, it still works after Phase 1, because uvx fetches the package itself and does not depend on a binary the image will stop shipping. Removing an unprovable, still-working entry breaks the hand-off clause. For the current pin I therefore move to A/C: keep it and print `claude mcp remove serena --scope user`.
- **What survives:** the older registry form `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --enable-web-dashboard false --enable-gui-log-window false` was written only by IronClaude's own registry code before 0e7bc31f (the removed line in that commit's `install_mcp.py` hunk). Nothing in this repo shows Coder's bundle ever writing it; Coder's older bundle versions are UNVERIFIED. The older docs told users to type a different, shorter command by hand (`... --context ide-assistant` with no `--enable-*` flags, in the same commit's docs hunks), so an exact match on the full registry argv tells IronClaude's own registration apart from a doc-guided hand-made one. That entry is provably IronClaude-owned, and the goal says `./update.sh` must leave no Serena MCP entry "that IronClaude owns". Remove that exact older argv automatically. Keep the current pin and print the removal command for it.
- **Honest limit:** this split only helps dev workspaces registered before 2026-09-11. Its value is small, and it adds one allowlist row.

**3. No consented serena removal path exists (A). Confirmed.** `install_mcp.py:1320-1324` rejects `--uninstall` for anything except `codebase-memory-mcp`. A printed `claude mcp remove serena --scope user` gives the same consent with no new flag. That beats C's `--retire-legacy` on cost.

## Updated assessment

What made B unique in Round 1 is now either inside amended A (receipt and marker cleanup, kept in the right order) or withdrawn (binary removal, `uv tool uninstall`, deleting the updater). B as a separate variant should not win. What is left of B is the provenance split for serena: a shape written only by IronClaude code is removed, and the ambiguous current pin is kept and printed.

## New evidence

- The older IronClaude registry argv (`git show 0e7bc31f`, `install_mcp.py` hunk) differs from the older doc-guided hand command (same commit, docs hunks) by the two `--enable-*` flags, so exact-argv matching can tell code-written entries from hand-made ones.
- The current serena pin does not depend on any binary the Coder image will stop shipping, so keeping it leaves no broken registration. That is a lower-harm leftover than the codebase-memory entry.

## Updated per-point positions (changed points only)

| Point | Preferred | Reason |
|---|---|---|
| C-001 | merge: A automatic for codebase-memory and the older IronClaude-only serena argv; current pin kept and its removal command printed | Remove what is provably owned; print what cannot be proven |
| C-002 | merge: amended A; receipt and marker deleted once the binary is absent; no binary or uv-tool removal | B's binary automation withdrawn |
| C-003 | merge: exact allowlist, with ownership tier per shape (older serena form = owned, current pin = ambiguous) | Provenance differs by shape |
| C-006 | C's handoff for serena; A for codebase-memory | The bundle re-adds serena |
| C-008 | amended A (receipt present: keep the registration, print the upstream command) | Keeps the order without keeping the module |
| X-004 | C for the current pin; A for the older form | The current pin is indistinguishable from Coder's |
| A-002 | C for the current serena pin; A for codebase-memory and the older serena form | Shape proves ownership only when one writer is possible |
| A-005 | amended A's skip-and-print | Matches `install_mcp.py:993-999` |
| A-006 | C's condition (delete only after the binary is absent) | Keeps the proof while it is still needed |
