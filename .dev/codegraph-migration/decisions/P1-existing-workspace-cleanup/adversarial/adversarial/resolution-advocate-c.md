# Invariant resolutions: Advocate for Variant 3 (Option C)

Re-checked read-only: `git show 5bee1571 -- setup/components/mcp.py`, `install_mcp.py:125-142`.

| INV | Verdict | Reason |
|---|---|---|
| INV-001 | ACCEPT | Confirmed: in `5bee1571` (diff lines 68 and 73) the registration was `subprocess.run([... "-s","user","--",name] + run_command.split())` with `shell=` true only on win32, so `$(pwd)` was stored as a literal token that no shell expanded. That makes the two-tier split sound. The ambiguous tier gets only a printed line, never a change, so least privilege holds. Counting pre-fork shapes as IronClaude-owned is right, since the same `superclaude` installer wrote them. |
| INV-002 | ACCEPT (I withdraw my exact-path request) | My R1 two-path rule would label IronClaude's own PATH-discovered entries (`install_codebase_memory.py:597-603`, `install_mcp.py:866`) "not ours", which is a false statement. The required phase already adopted any such entry as its own at `install_mcp.py:864-865`. Blast radius is unchanged: only the registration goes, never a binary, and the user can re-add it with one command. |
| INV-003 | ACCEPT | Gating on the binary is the more conservative rule. An entry that one of two writers could have made is kept. |
| INV-004 | ACCEPT | Read all state first, then act in a fixed order. This gives one-run convergence and no stale hint. |
| INV-005 | ACCEPT | An absolute path plus `--dir` stops the printed hint from reaching Coder's `/usr/local/bin` copy. |
| INV-006 | ACCEPT | A required matcher with a re-match before removal is a real least-privilege gain. The sub-second window caused by delete-by-name must stay written down as residual risk. |
| INV-007 | QUALIFY | Accept direct exec, the process-group kill, the 15 s cap and the end slot. Note: `_run_command` uses `$SHELL -c` "to support aliases" (`install_mcp.py:134-141`), so a user whose `claude` exists only as an alias is now skipped by `shutil.which`. The skip note must print the exact manual `claude mcp remove <name> --scope user`, so skipping fails safe and is visible. |
| INV-008 | ACCEPT | A doctor warning that never fails keeps the `update.sh` exit code unchanged. |
| INV-009 | ACCEPT | Keeping `superclaude update`'s "never touches MCP" contract and having it only print a read-only notice is the least-surprise choice. |
| INV-010 | ACCEPT | This matches the residual statement I proposed in round2-advocate-c.md. |
| INV-011 | ACCEPT | Reuse the stricter existing predicates exactly. A HOME mismatch keeps the entry and says so: it fails safe and is reported. |
| INV-012 | ACCEPT | Warnings that name their cause, with a manual command, stop a permanent warning that tells the user nothing. |
| INV-013 | ACCEPT | One shared classifier stops the preview and the action from disagreeing. It also replaces the separate dry-run I conceded in R2. |
| INV-014 | ACCEPT (dropping the heuristic) | The uv-tool signal is unverified (I said in R2 it should not ship without Coder's confirmation), and here it would only change wording, never what is removed. The single printed line already says Coder adds it back at start, so the user makes an informed choice. |

Least-privilege summary: with these resolutions, IronClaude removes only entries one writer could have made (or that only IronClaude's code could have produced), never touches a binary or uv tool, keeps every ambiguous entry, and prints the exact command for the user's own decision. I see no remaining objection that blocks convergence.
