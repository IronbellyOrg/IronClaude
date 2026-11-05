# Confidence check (skill: confidence-check) — ROOT CAUSE

Run: 2026-11-02T03:30Z, before planning the fix.

Claim checked: `ccsession` setup_shim starts the shared gateway shim with `nohup python3 ... &` and then `exec`s Claude Code, so the shim stays in the launching Orca terminal's process tree, process group and session; when Orca kills that terminal its pty descendant sweep (SIGTERM, then SIGKILL, by ppid walk) kills the shim, cutting every other session's stream and refusing new connections until a later launch restarts it.

| # | Check (weight) | Result | Evidence |
|---|---|---|---|
| 1 | No duplicate implementations (25%) | PASS | `grep -rn 'os\.fork\|os\.setsid\|start_new_session\|setsid\|disown\|daemoni' src/superclaude`: one hit, `src/superclaude/cli/install_mcp.py:782 start_new_session=True` (unrelated MCP install helper). Nothing in ccsession-tag/ detaches the shim (also wave1_5-branch-C.md: "the files here never mention setsid"). |
| 2 | Architecture compliance (25%) | PASS | Fix uses only the Python standard library (`os.fork`, `os.setsid`) inside the existing shim and one env variable in the existing bash launcher; follows the ccsession:351 precedent (python3 instead of a util-linux binary absent on macOS). No new dependency. |
| 3 | Official documentation verified (20%) | PASS | docs.python.org/3/library/os.html: "os.setsid() — Call the system call setsid(). See the Unix manual for the semantics. Availability: Unix, not WASI." Orca's own kill semantics read from the installed code (behaviour-definitions.md row 1, tier1-observation.md O8). |
| 4 | Working OSS reference (15%) | PASS | discuss.python.org/t/proper-way-to-create-a-daemon-process/79824: "Call fork() ... In the child, call setsid() to detach from any terminal and create an independent session. In the child, call fork() again"; 0xjet.github.io/3OHA/2022/04/11/post.html (Stevens double-fork daemonize). |
| 5 | Root cause identified (15%) | PASS | Live process tree of the current 4114 shim (O2), signal mask (O4), Orca daemon.log session-killed events matching both cut-off turns to the minute (O7), Orca descendant-sweep code (O8), and a live reproduction from worktree source reproducing both symptoms from one sweep (O10, live-check/before.txt). |

📊 Confidence: 1.00 (100%) by the skill formula. ✅ Proceed to planning.

Residual uncertainty recorded honestly (does not flip a check): the ancestry of the two 4114 shims that died on 2026-11-01 is inferred from daemon.log timing, not observed (those processes are gone). The current live 4114 shim shows the same ancestry pattern (child of another terminal's Claude), and the reproduction shows the mechanism deterministically.
