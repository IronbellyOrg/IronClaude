# Invariant resolutions: Advocate for Variant 1 (Option A)

Re-checked read-only: `install_mcp.py:129-141` (`_run_command` runs `$SHELL -c` with `shell=True`), `install_codebase_memory.py:597-603,637-650` (PATH fallback and reuse of external binaries), `install_core.py:84` ("use --force to overwrite").

| INV | Verdict | Reason |
|---|---|---|
| INV-001 | QUALIFY | Accept the two tiers, and accept counting pre-fork SuperClaude shapes as IronClaude-owned. The `$(pwd)` tier proves code wrote the entry only if the pre-fork code passed the argument list to `claude mcp add` without a shell. Had it gone through a shell string, `$(pwd)` would have been expanded, and a literal token would mean a hand-typed single-quoted command. Confirm the call style in `git show 5bee1571` and `git show 43112779` before pinning the row; if a shell was used, move the row to the ambiguous tier. |
| INV-002 | ACCEPT | Discovery registered any PATH hit (`install_codebase_memory.py:597-603`, `install_mcp.py:866`). Require `command` to be an absolute path. |
| INV-003 | ACCEPT | Using the binary as the gate fixes the case where a user or upstream installed into `~/.local/bin` (`install_codebase_memory.py:643-650`). |
| INV-004 | ACCEPT | Reading all state first and acting in a fixed order lets every run converge in one pass. |
| INV-005 | ACCEPT | Matches IronClaude's own call, `[str(executable), "uninstall", "-y", f"--dir=..."]`. |
| INV-006 | ACCEPT | The matcher becomes a required parameter, with a re-read and re-match before removal. A sub-second race remains because removal is by name; that residual is stated honestly. |
| INV-007 | ACCEPT, including the move from "first" | My Round 2 "first" placement assumed a hard 10 s bound per call. `_run_command` goes through `$SHELL -c` (`install_mcp.py:134-141`), so a timeout kills only the shell and an orphaned `claude` process can block, which voids that assumption. Direct exec with a process-group kill and a 15 s cap for the whole step removes the hang. After that, framework files matter more than the retire step, and a killed run retries next time. Two conditions: the slot must stay before the `sys.exit` block (`main.py:264`), and the deleted codebase-memory phase frees more time than 15 s (UNVERIFIED but plausible). Note that direct exec drops support for a `claude` defined only as a shell alias (the alias comment at `install_mcp.py:134-137`). `shutil.which` then reports a skip, which is the correct fail-safe. |
| INV-008 | ACCEPT | The restart note plus a doctor warning that never fails keeps the `update.sh` exit code unchanged. |
| INV-009 | ACCEPT | A read-only notice from `update` keeps its contract (`docs/user-guide/mcp-installation.md:24`). Non-forced installs already print the skip notice (`install_core.py:84`). |
| INV-010 | ACCEPT | Record "goal met except", with each closing condition. |
| INV-011 | ACCEPT | Reuse the existing private-file and directory predicates exactly. |
| INV-012 | ACCEPT | Name the cause and print the manual command. |
| INV-013 | ACCEPT | One pure classifier shared by install, `--list`, doctor and update, with one table-driven test. |
| INV-014 | ACCEPT | No heuristic to detect Coder; the single printed line already covers it. |

Net: INV-001 is resolved, with one source check left. My only qualification is whether the `$(pwd)` row may sit in the code-written tier.
