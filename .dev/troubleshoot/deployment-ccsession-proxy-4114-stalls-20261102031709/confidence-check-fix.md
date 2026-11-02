# Confidence check (skill: confidence-check) — FIX

Run: 2026-11-02T04:47Z, after `/sc:implement` completed Tasks 1-5 of `.dev/tasks/to-do/TASK-WF-detachTheCcsessi-20261102-034618/` (the package moves to `.dev/tasks/done/` when archived).

Claim checked: the fix for issue #341 keeps a ccsession gateway shim serving every session on its port when the terminal that launched it is closed. It has two parts:

1. `src/superclaude/skills/ccsession-tag/ccsession` `setup_shim` starts the shim from a `( ... & )` subshell. The subshell exits at once, so the shim is reparented and is no longer a descendant of the launching terminal.
2. `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` `__main__` calls `os.setsid()` before it binds, when stderr is not a terminal, ignoring `OSError`. The shim then leaves the launcher's session and process group.

| # | Check (weight) | Result | Evidence |
|---|---|---|---|
| 1 | No duplicate implementations (25%) | PASS | Grep for `setsid\|start_new_session\|disown\|double.?fork` in `src/superclaude` finds the new lines (local-gateway-alias-proxy.py:862, 865) and one unrelated hit, `src/superclaude/cli/install_mcp.py:782 start_new_session=True` (MCP install helper). Nothing else detaches the shim. |
| 2 | Architecture compliance (25%) | PASS | Python standard library only (`os.setsid`, `sys.stderr.isatty`, no new import); plain bash 3.2 subshell syntax; no `setsid` binary. The argv keeps the script path, so `pgrep -f -- "$CC_SHIM_SCRIPT"` (ccsession:722) and `pkill -f local-gateway-alias-proxy.py` still find it. `make lint` and `make verify-sync` pass (package `artifacts/t5-checks.log`). |
| 3 | Official documentation verified (20%) | PASS | docs.python.org/3/library/os.html: "os.setsid() — Call the system call setsid(). See the Unix manual for the semantics. Availability: Unix, not WASI." man7.org setsid(2): "setsid() creates a new session if the calling process is not a process group leader"; "The calling process will be the only process in the new process group and in the new session"; EPERM: "setsid() fails if the calling process is already a process group leader" (the reason for the `except OSError`). |
| 4 | Working OSS reference (15%) | PASS | CPython `subprocess.Popen(start_new_session=True)` performs the same `setsid()` in the child, and this repo already uses it to detach a process (`src/superclaude/cli/install_mcp.py:782`). The fork-then-setsid daemon pattern is cited in confidence-check-root-cause.md check 4 (discuss.python.org/t/proper-way-to-create-a-daemon-process/79824). |
| 5 | Root cause identified (15%) | PASS | confidence-check-root-cause.md (1.00) and the calibrated diagnosis (0.92). The regression test that reproduces it, `test_shim_outlives_the_terminal_that_started_it`, fails on the unmodified source with `assert <shim pid> not in {<shim pid>}`: the shim was a descendant of the terminal (package `artifacts/t1-before.log`). It passes after the fix (package `artifacts/t4-tests.log`). |

Verification of the fix itself (not part of the score):

- **Tests.** Both new tests fail before the fix and pass after it (`artifacts/t1-before.log`, `artifacts/t4-tests.log`). Every test file that reads the edited files passes: 457 passed (`artifacts/t5-checks.log`).
- **Live check.** Run against a throwaway shim on a free port through the real changed ccsession (`live-check/after.txt`):
  - `shim is a descendant of the terminal: False`
  - `stream finished: True`
  - `port after close: answers`

  Before the fix (`live-check/before.txt`): `True`, `False`, and `Connection refused`.
- **Live shims.** The running shims on ports 4013 (pid 1788) and 4114 (pid 2258510) kept the same pids before and after (`artifacts/t4-tests.log`).

📊 Confidence: 1.00 (100%). Every check passes; the fix is supported by a failing-then-passing regression test and a live reproduction.

Residual limits:

- The fix reaches installed copies only after merge and `superclaude install`/update. A shim already running keeps the old behaviour until it is stopped and a later launch starts a new one.
- A shim run by hand with stderr on a terminal does not call setsid, so Ctrl-C still stops it. It is still detached from the tree when ccsession starts it.
