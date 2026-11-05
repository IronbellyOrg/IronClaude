# Invariant resolutions: Advocate for Variant 2 (Option B)

Re-checked read-only: `git show 5bee1571 -- setup/components/mcp.py`, `install_mcp.py:125-141`, `install_codebase_memory.py:594-604`.

| INV | Verdict | Reason |
|---|---|---|
| INV-001 | ACCEPT | This extends my Round 2 provenance split correctly. 5bee1571 registered serena with a list argv and `run_command.split()`, using `shell=False` on Linux, so a literal `$(pwd)` token was stored. On Windows `cmd` does not expand `$(pwd)` either. No human shell produces that token, so code-written rows are provable. I also accept that pre-fork shapes count as IronClaude-owned, because they come from the same installer lineage. |
| INV-002 | ACCEPT | Discovery returns any external PATH hit (`install_codebase_memory.py:597-603`), and install writes exactly that path (`install_mcp.py:866`), so a basename match on an absolute command is the honest boundary. |
| INV-003 | QUALIFY | I accept replacing my receipt gate with a binary-existence gate. It covers `.pending` with no receipt, and a user-installed binary that has no receipt. Addition: print the absolute upstream uninstall whenever `$HOME/.local/bin/codebase-memory-mcp` exists, even when the entry that matched points elsewhere (for example `/usr/local/bin`). Otherwise upstream companions in `~/.local/bin` go unmentioned. |
| INV-004 | ACCEPT | Classify everything first, then run actions in a fixed order. That ends the two-run convergence. |
| INV-005 | ACCEPT | It matches IronClaude's own call, which passes the absolute path and `--dir` (`install_codebase_memory.py:352-355`). |
| INV-006 | ACCEPT | Making the matcher required, re-matching before the remove, and never retrying a different shape closes the gap in the existing name-only helper (`install_mcp.py:916-934`). |
| INV-007 | ACCEPT | Confirmed: `_run_command` runs `$SHELL` with `shell=True` (`install_mcp.py:136-141`), so the timeout kills only the shell. Calling `claude` directly with group kill and a 15 s cap fixes that. I also accept placing the step after the framework-file steps instead of first. |
| INV-008 | ACCEPT | A restart note plus a doctor warning (never a failure) costs nothing and keeps the `update.sh` exit code unchanged. |
| INV-009 | ACCEPT | `update` keeps its documented MCP contract and prints only a read-only notice. Scoping the goal claim to `--force` paths is honest. |
| INV-010 | ACCEPT | The record should say "goal met except", with each closing condition. |
| INV-011 | ACCEPT | Reuse the stricter existing predicates exactly (`install_codebase_memory.py:95-100`, `:125-139`). |
| INV-012 | ACCEPT | The cause-specific warning comes with the exact manual command. |
| INV-013 | ACCEPT | One shared classifier makes `--list` and the step agree. |
| INV-014 | ACCEPT | The single serena line already states that Coder re-adds the entry. A heuristic for detecting Coder adds risk for no gain. |

## Summary

- **Option B:** nothing in it remains in conflict with the consensus.
- **INV-001:** I accept it as the closure of my Round 2 serena split. Remove only rows that IronClaude's code alone could have written, and keep and print the rest.
- **INV-003:** I accept it as a replacement for B's receipt gate, with the one printing addition above.
