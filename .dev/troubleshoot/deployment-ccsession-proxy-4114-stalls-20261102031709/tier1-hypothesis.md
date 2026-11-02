# Hypothesis: the 4114 shim runs inside the process tree of the Orca terminal that launched it, so Orca's descendant sweep kills it when that terminal is closed

**Agent**: root-cause-analyst (troubleshoot-analyst, read-only lens)
**Tier**: 1
**Timestamp**: 2026-11-02T03:28:01Z (stamped by the parent on receipt)
**Cause class**: Other: process lifecycle. The shared shim is not detached from the terminal that launched it. No triage class fits: nothing is wrong with config, timing or resources.
**Claim class**: `runtime_behavior`
**Evidence class**: `runtime_repro`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned. The claim and fix match the documented contract: README.md:415-418 says a shim "keeps running until you stop it", and ccsession:762-763 says "a started reply must never be cut off". The code breaks that contract; the docs are not wrong.
runs-in=src/superclaude/skills/ccsession-tag/ccsession:801-804 + local-gateway-alias-proxy.py:857-872 @ Coder workspace host (SAME-ENV: yes)

## Claim
`setup_shim` starts the shared shim as a plain background child (`nohup ... &`). It then `exec`s Claude Code, so the shim stays a descendant of the Orca terminal whose launch started it, in that terminal's process group and session. When Orca kills that terminal, its pty descendant sweep sends SIGTERM and then SIGKILL to every process descended from it by parent pid. The shim ignores SIGHUP but not SIGTERM, so it dies. Every other session attached to that port then sees its open stream end with no `message_stop` ("Connection lost mid-response"). Later requests get ECONNREFUSED until some later launch finds the port free and starts a new shim. The 4013 shim never fails because it has ppid 1 and pgid 369 (Orca's own group) with no tty, so no sweep can reach it.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | source_citation | ccsession:801-804, 1438; local-gateway-alias-proxy.py:857-872 | `nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &`, then `exec "$CLAUDE_BIN" ... --name "$TOPIC" "$@"`. `__main__` only binds and calls `srv.serve_forever()`. It has no fork or setsid. |
| E2 | log_artifact | tier1-observation.md O2, O4 (ps and /proc, 03:17Z) | Shim `2258510 ppid 2258462 (claude) pgid 2258462 sid 2257514 pts/18 Sl+`. `SigIgn: 0000000001001007` means HUP, INT, QUIT, PIPE and XFSZ are ignored, TERM is not. Compare 4013: `1788 ppid 1 pgid 369 tty ?`. |
| E3 | log_artifact | ~/.config/orca/logs/daemon.log:680-681, 750-751 | `2026-11-01T00:01:42.345Z ... session-killed ... release-readiness@@5e7df77c` and `2026-11-01T22:59:18.584Z ... session-killed ... IB-CPlus-01@@b846db04`. Each matches one cut-off turn to the minute (O7). |
| E4 | executed_reproducer | O10, `live-check/orca_close_repro.py` -> `live-check/before.txt` (HEAD f90877be) | `shim is a descendant of the terminal: True` / `stream finished: False error=None bytes=53` / `port after close: URLError(ConnectionRefusedError(111...))`. One sweep reproduces both symptoms. |

- behaviour-definition: row 1. Orca's sweep sends SIGTERM, then SIGKILL, to descendants found by parent pid (fetched from the local install, O8).
- behaviour-definition: row 2. `nohup cmd &` followed by `exec` leaves cmd as a child in the same process group and session, ignoring only HUP, INT and QUIT (observed at runtime, O2 and O4).
- Producer-citation check skipped: the menu in producers.md is empty because both strings come from Claude Code's HTTP client (O11). The card uses ordinary source and captured-output citations instead.

**Adversarial timeline check (daemon.log:668-759):**
- Who started the shim: the shim that died at 00:01 cannot have been the worker's own child (the worker's session, created 23:45:02, shows no exit and survived to see the error). Only release-readiness@@5e7df77c (23:44:24 -> 00:01:42) was created before the worker and killed at the moment of the cut. Second incident: IB-CPlus-01@@b846db04 (22:41:32 -> 22:59:18) is the only session created before worker 2089859 (22:47:22) and killed at 22:59.
- 00:59 refusal: 57 minutes after the 00:01:42 kill; no session-created event between 23:51:11 and 01:01:27, so nothing restarted the shim. Fits.
- 01:00:57 kill of IB-CPlus-01@@b798175f: after the 00:59 refusal, so not its cause; does not contradict the claim.
- Second outage: no session-created event between 22:59:18 and 03:08:20 (serve-46e81c2f), matching refusals until 03:08 when shim 2258510 appeared as a child of claude in that session.

## Proposed Fix
After `ThreadingServer` binds successfully, have the shim detach itself when `GW_PROXY_DETACH=1` is set: fork, `os.setsid()` in the child, fork again; the first two processes exit 0 and the grandchild calls `serve_forever()`. The grandchild then belongs to init or the nearest subreaper, sits in its own session and group with no tty, and is outside any terminal's descendant set. Uses Python (no `setsid` binary; macOS-safe, precedent ccsession:351); argv unchanged so `pgrep -f "$CC_SHIM_SCRIPT"` (ccsession:722) still finds it; env inherited; logging stays opt-in; bash side adds one variable (bash 3.2 safe); no shim is ever stopped; binding before forking keeps the EADDRINUSE error visible; no threads exist before `serve_forever`, so forking is safe.

Files that change:
- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`: opt-in double fork plus setsid in `__main__`, between `srv = ThreadingServer(...)` and `srv.serve_forever()`.
- `src/superclaude/skills/ccsession-tag/ccsession`: add `GW_PROXY_DETACH=1 \` to the start statement at 801-804.

Tests:
- New: `tests/unit/test_ccsession_tiers.py::test_shim_outlives_the_terminal_that_started_it`, ported from O10: real `ccsession --shim` with a fake `claude` (`exec sleep 300`) under `start_new_session=True`; streamed tier2 reply against `StandInGateway` with `pause-stream`; assert the shim pid is not among the terminal's descendants; SIGTERM then SIGKILL the root and its descendants; assert the reply completes with `b"message_stop"` and `/__ccsession_shim` still reports the same pid; clean up with `pkill -f <tmp shim path>`. Fails before the fix (O10 `before.txt`).
- Existing: `test_a_busy_shim_is_never_stopped_by_a_new_launch` (test_ccsession_tiers.py:1379) must still pass; its `pkill -f` cleanup at 1416-1418 depends on argv keeping the script path.

## Confidence
Self-reported confidence: 0.85
- Evidence grounding: 1.0 — source lines, live process tree, daemon.log lines and a captured reproduction all agree.
- Runtime check: 1.0 — O10 is an executed reproducer with captured output; its stand-in sweep copies behaviour row 1 rather than running Orca itself.
- Symptom coverage: 1.0 — explains both error strings, both incidents to the minute, the 03:08 recovery and why 4013 is healthy.
- Reproducibility fit: 0.5 — mechanism deterministic and reproduced, but the parentage of the dead 4114 shims is inferred from the timeline, not observed.
- Fix directness: 1.0 — two files, one change each, at the start site.
- Domain coherence: 1.0 — a killed parent tree explains a cut close-delimited HTTP/1.0 stream followed by refusals.

## Risks
- If `claude` (node) or the Orca pty host sets PR_SET_CHILD_SUBREAPER, the orphaned shim would be re-parented inside the terminal tree and still be swept. The new test's ppid assertion catches this; the 4013 shim's ppid of 1 suggests no subreaper here.
- Detached shims are harder to find and clean up; that is already the documented model (README.md:417-418, `pkill -f local-gateway-alias-proxy.py`).
- Tests that start the shim directly without `GW_PROXY_DETACH` keep the old behaviour; their `pkill -f` cleanup must stay.

## If I'm wrong, it's probably because...
The 4114 shim died for a reason that only coincides with session kills (for example a Python exception that killed the process with stderr sent to /dev/null), and the matching timestamps are chance.

## Falsification standard
Any of these proves the hypothesis wrong: a future "Connection lost mid-response" on 4114 while `/__ccsession_shim` still returns the same pid; a 4114 shim death with no `session-killed` event for its owning terminal within ±5 s; the O10 reproducer at HEAD printing `stream finished: True` and a live port after the sweep.

## Evidence classification
- **Claim class**: runtime_behavior — whether the shim lives depends on its process ancestry at runtime and on Orca's signals.
- **Evidence class**: runtime_repro — O10 executed the real worktree `ccsession --shim` and captured its output; daemon.log provides the field correlation.
- **Runtime check performed?**: yes (parent-captured, O10).
- **If REFUTE verdict, coverage statement**: Not applicable — verdict is AFFIRM.

## Alternatives considered
- Shim timeouts or buffering: rejected — no socket timeout after the first byte (local-gateway-alias-proxy.py:687; timers 99-117); `_stream` uses `read1` (834); a timeout would leave the port listening, not refusing.
- Single-threaded server: rejected — `ThreadingServer(ThreadingMixIn, HTTPServer)` with `daemon_threads` (852-854); a blocked server queues, not refuses.
- Upstream keep-alive or gateway drop: rejected — 4013 uses the same upstream and code digest (O6) without errors; an upstream drop cannot make the local port refuse.
- OOM: rejected — no OOM lines in dmesg/journalctl (O5); would not align to session kills.
- SIGHUP: rejected — ignored (SigIgn bit 0, O4).
- Port conflict: rejected — EADDRINUSE only affects startup (857-870); ccsession never stops a running shim (762-764).

## Grounding gaps
- The 4114 shims that died on 2026-11-01 cannot be inspected; their ancestry is inferred from the daemon.log timeline.
- Why launches chose 4114 instead of reusing 4013 is unverified (a `stale` health result at the time is assumed; ccsession:741-747, 782-784).
- Orca's kill code was read from minified files (O8); whether `terminateOwnedTree` also signals the whole process group is not established. A new session covers both cases.
- O10 imitated the sweep with a script; it did not run Orca itself.
- Diagnosability verdict: partial (diagnosability-context.md): the shim logs nothing; its exits are visible only through external evidence.
