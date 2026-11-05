# Troubleshoot Report

**Target**: ccsession gateway shim on 127.0.0.1:4114 keeps stalling Claude sessions ("Connection lost mid-response" on long turns, then ECONNREFUSED until a new shim appears)
**Type**: deployment
**Tier reached**: 1
**Confidence**: 0.92
**Status**: partial
**Escalation reason**: none
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/doc-context.md
**Duration**: 1722
**Date**: 2026-11-02T03:45:51Z

---

## Summary

Status is partial because two evidence-validation passes dropped four overstated sentences (timeline and exclusion wording; corrected below); the mechanism itself is reproduced, and the owners of the two dead 2026-11-01 shims are inferred, not observed. Port 4114 is served by the ccsession gateway shim (`local-gateway-alias-proxy.py`), started by whichever `ccsession --shim` launch first finds the port free and then shared by every later session with the same settings. `ccsession` starts it as a plain background child (`nohup ... &`) and then turns into Claude Code, so the shared shim lives inside one Orca terminal's process tree, process group and session. When Orca closes that terminal it sends SIGTERM, then SIGKILL, to every descendant, which kills the shim: every other session's open reply is cut ("Connection lost mid-response") and new requests are refused until some later launch starts a new shim. The fix is to start the shim detached from the launching terminal (reparented away from it and in its own session).

## Documentation Context

- **Relevant refs**: src/superclaude/skills/ccsession-tag/README.md, src/superclaude/skills/ccsession-tag/SKILL.md, .dev/specs/ccsession-native-install.md, .dev/specs/ccsession-native-install-design.md, .dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md
- **Documented behavior**: one shim per settings/port is shared by every session and "keeps running until you stop it"; "ccsession never stops a running shim by itself"; no time limit once a reply starts.
- **Restrictions honored**: never stop another shim; keep the script path in argv (pgrep/pkill); keep the inherited env; no `setsid` binary (macOS); bash 3.2; logging stays opt-in.
- **Restrictions overridden**: None
- **Card path**: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: trivial
**Captured-bytes (failing run)**: n/a

The shim logs only to stderr, which ccsession sends to /dev/null, and it has no shutdown or signal log.
Gap: the shim cannot report when or why it exited; the dead 4114 shims left no trace of their own.
Implication: the diagnosis rests on Orca's daemon log, the live process tree and a runtime reproduction, which cover when, where and why directly.

(Full card: /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/diagnosability-context.md)
(Tasklist (informational): /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: `ccsession` starts the shared gateway shim as an ordinary child of the launching terminal (`nohup python3 ... &`, then `exec` Claude Code), so the shim dies whenever Orca closes that terminal, taking every other session's connection with it.

**Cause class**: Other: process lifecycle (a shared service bound to one client's process tree)

**Detailed explanation**: What serves 4114 and its lifecycle (Evidence 1-6): `ccsession-orca` runs `ccsession --shim`; `ccsession` computes the port from the settings (`models.py shim-port`: 4010 + 1 + digest % 97 = 4013 here), then `setup_shim`, if a shim with other settings or older code holds it, tries 4013 + 101 = 4114 and so on. A launch reuses a matching shim, or starts one when the port is free; nothing restarts a dead shim, and nothing stops one except the user. The 4114 shim live now (pid 2258510) is a child of a Claude Code process in an Orca terminal for a different worktree (auggie-mcp-regNotConnected), in that terminal's foreground process group and session. The 4013 shim (pid 1788) started 3 s after Orca itself and now has parent pid 1 in Orca's own process group with no terminal (inferred: launched by Orca outside any terminal), so no terminal close can reach it; the 4013 shim is still alive (the coordinator reports its session on 4013 never failed). Launches choose 4114 because the 4013 shim reports a different upstream URL than the launches use (inference from ccsession:741-747 and the health values in Evidence 13), so ccsession treats it as stale and moves to 4013 + 101. `~/.claude/ccsession.env` was modified at 2026-10-31 23:44:00 (captured `stat`), 24 s before Orca created the release-readiness terminal (daemon.log:669), the inferred owner of the first 4114 shim.

Why it stalls (Evidence 7-9): the shim ignores SIGHUP (nohup) but not SIGTERM. Orca's terminal kill walks the descendants of the terminal by parent pid and sends SIGTERM then SIGKILL. Orca's terminal scrollback (Evidence 13) shows that both 4114 workers, and the still-running session serve-c727018a, REUSED a 4114 shim that was already running when they launched, so none of them owned it; only the 03:08 launch says "Starting model-alias shim on 127.0.0.1:4114". Orca's daemon log shows a terminal session killed at 2026-11-01T00:01:42Z (release-readiness, the only session created between the previous kill at 23:32 and the first worker's launch at 23:45) and another at 22:59:18Z (IB-CPlus-01, the only session created before 22:46:55 that was killed at the time of the second cut), matching the coordinator-reported screen times of the two cut-off turns (00:01 and 22:59). These two terminals are the best-fitting owners of the dead shims; their own scrollback was deleted with them, so their start lines cannot be shown. No session started between 22:59 and 03:08:20, when a new terminal's launch started the current shim. The shim speaks HTTP/1.0 with close-delimited bodies, so the dying shim closes each open stream early, which Claude Code reports as "Connection lost mid-response"; the empty port then gives ECONNREFUSED. The live reproduction (Evidence 10) shows both symptoms from one terminal kill. Ruled out: shim timeouts (Evidence 11), a single-threaded server and OOM (Evidence 12), SIGHUP (ignored, Evidence 8), and port conflicts (bind errors only stop a shim at start-up, `local-gateway-alias-proxy.py:857-870`, and ccsession never stops a running shim, `ccsession:762-764`). An upstream drop would cut one stream but leave the local port listening, so it cannot produce the ECONNREFUSED that followed each cut; and each cut coincides with a terminal kill.

## Evidence

1. `src/superclaude/skills/ccsession-tag/ccsession-orca:81` — `exec "$CCSESSION" --shim --claude-args "$@"` (Orca launches go through the shim).
2. `src/superclaude/skills/ccsession-tag/models.py:799` — `return base + 1 + int.from_bytes(digest[:2], "big") % 97` (shim port per settings; 4013 here).
3. `src/superclaude/skills/ccsession-tag/ccsession:769-770` — `for _attempt in 0 1 2 3 4 5; do` / `CC_SHIM_PORT=$((base_port + 101 * _attempt))` (4114 = 4013 + 101).
4. `src/superclaude/skills/ccsession-tag/ccsession:801-804` — `GW_PROXY_UPSTREAM="$ANTHROPIC_BASE_URL" \ GW_PROXY_PORT="$CC_SHIM_PORT" \ CCSESSION_DIR="$CCSESSION_DIR" \ nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &` (plain background child, output discarded).
5. `src/superclaude/skills/ccsession-tag/ccsession:1438` — `exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ... --name "$TOPIC" "$@"` (the launcher becomes Claude Code, the shim's parent).
6. `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:871-872` — `print(f"[proxy] listening on http://{host}:{port}  ->  {UPSTREAM}", file=sys.stderr)` / `srv.serve_forever()` (no detach, no signal handling).
7. Command: `ps -eo pid,ppid,pgid,sid,tty,lstart,etime,stat,rss,args | grep local-gateway-alias-prox[y]` and the session listing (tier1-observation.md O1-O3) → `2258510 2258462 2258462 2257514 pts/18 ... Sl+ python3 .../local-gateway-alias-proxy.py` with `2258462 ... claude --dangerously-skip-permissions ...` in Orca terminal session 2257514; `1788 1 369 369 ? ...` for 4013.
8. Command: `grep -E 'SigIgn' /proc/2258510/status /proc/1788/status` → `SigIgn: 0000000001001007` (HUP, INT, QUIT, PIPE, XFSZ ignored; TERM not).
9. `/home/coder/.config/orca/logs/daemon.log:680-681` and `:750-751` — `"ts":"2026-11-01T00:01:42.345Z" ... "event":"session-killed" ... release-readiness@@5e7df77c` and `"ts":"2026-11-01T22:59:18.584Z" ... "event":"session-killed" ... IB-CPlus-01@@b846db04`; `:752-753` new session at `2026-11-02T03:08:20.854Z` (pid 2257514, the current shim's session). Orca kill code: `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/pty-descendant-exit-verification-DKf-exmf.js` (`for(let t of e.descendants)n(t.pid,'SIGTERM')`, then SIGKILL).
10. Command: `python3 -I live-check/orca_close_repro.py <worktree> <scratch>` (real worktree `ccsession --shim`, throwaway shim on a free port, terminal-kill emulation) → `shim is a descendant of the terminal: True` / `stream finished: False error=None bytes=53` / `port after close: URLError(ConnectionRefusedError(111, 'Connection refused'))` (live-check/before.txt).
11. `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:687` — `conn.sock.settimeout(None)` (no read timeout after connect; the 300 s first-byte wait only precedes the first byte, lines 112-117).
12. `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:852-853` — `class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):` / `daemon_threads = True` (threaded server); `dmesg`/`journalctl` show no OOM lines (tier1-observation.md O5); both shims report the same code `6e7d1d51209e49e6` (O6).
13. Orca scrollback `/home/coder/.config/orca/terminal-history/serve-c727018a-b59c-46c6-8ff4-8f60919250e0/output.log` — `[ccsession] Shim already running on 127.0.0.1:4114 (reusing)`; the same reuse line in `.../terminal-history/de550e99-...review-severity-rule%40%40d1747ae5/checkpoint.json` and `...review-severity-rule%40%40d6954559/checkpoint.json`; `[ccsession] Starting model-alias shim on 127.0.0.1:4114` in `.../terminal-history/serve-46e81c2f-1d0c-4eff-abf8-2b697673c1c1/checkpoint.json`; every launch also prints `A shim with other settings or older code is on 127.0.0.1:4013; leaving it running for its sessions`. Health (03:38Z): 4013 and 4114 report different `upstream` values (sha256 prefixes c7df6bb80904 vs 915eeb72d126) with equal `settings` and `code` (tier1-observation.md O12).

## Proposed Fix

Start the shim detached from the terminal that launches it, in two small changes:

**Files to change**:
- `src/superclaude/skills/ccsession-tag/ccsession` — run the start statement (lines 801-804) inside a `( ... )` subshell so the subshell exits at once and the shim is reparented away from the launching terminal (no longer its descendant).
- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` — in `__main__`, call `os.setsid()` before binding (ignore `OSError` when the process already leads a group, as when run by hand in an interactive shell) so the shim leaves the terminal's session and process group: no terminal or process-group signal reaches it. Python standard library only (macOS has no `setsid` binary); argv, env and logging are unchanged; the README restart recipe already uses a subshell and gains the new session automatically.

Variant considered (Tier 1 card): an opt-in double fork inside the proxy (`GW_PROXY_DETACH=1`). It gives the same result but forks the process that tests start directly unless gated; the subshell plus `setsid` keeps direct starts as plain children (test fixtures stop them with `terminate()`), so it is the smaller change.

**Test to verify**:
- Add `tests/unit/test_ccsession_tiers.py::test_shim_outlives_the_terminal_that_started_it`: the real `ccsession --shim` in its own session with a fake `claude`, a paused streamed reply through the shim, then SIGTERM/SIGKILL of every descendant of the terminal root; asserts the shim was not a descendant, the reply ends with `message_stop`, and the shim still answers with the same pid. Fails at HEAD (live-check/before.txt).
- Add a test that a directly started shim runs in its own session (`os.getsid(pid) != os.getsid(0)`).
- Existing: `test_a_busy_shim_is_never_stopped_by_a_new_launch` and the rest of `tests/unit/test_ccsession_tiers.py` and `tests/unit/test_ccsession_tag.py` must still pass.

**Apply with**: `sc:workflow` → `/sc:implement`, as directed by the coordinator brief (the skill's own Tier 3 offer is gated on status `success`).

## Risk + Rollback

- **Likelihood of regression**: low, in shim start-up and discovery (ccsession's listener/health waits at ccsession:806-824 and `pgrep -f` lookup at ccsession:722 depend on argv and the listening socket, both unchanged).
- **Test coverage of the changed code**: partial today (no test covers process placement); the new tests close it.
- **Rollback**: `git revert` of the fix commit; already-running detached shims keep running until stopped with `pkill -f local-gateway-alias-proxy.py`.
- Watch: a detached shim outlives every terminal, so stale shims accumulate until the user stops them; this is the documented model (README.md:415-418).

## Operator workaround for sessions already running (not applied)

The fix reaches installed copies only after merge and `superclaude update`. Until then:

1. Find the terminal that owns a shim, and keep it open while other sessions use that port: `curl -s http://127.0.0.1:4114/__ccsession_shim` gives `pid`; `ps -o pid,ppid,pgid,sid,tty,args -p <pid>` and `ps -o args -p <ppid>` show the owning Claude Code process; `tr '\0' '\n' < /proc/<pid>/environ | grep -E '^(PWD|ORCA_TERMINAL_HANDLE)='` names its worktree and Orca terminal. Today 4114 belongs to the Claude Code session in worktree auggie-mcp-regNotConnected (terminal handle term_41eaf7f8-...). Closing that tab kills 4114 for every session on it, including this one.
2. To make a dead port come back within about 2 seconds without touching the running shim, start a detached standby loop once (it fails to bind while the current shim holds the port and takes over when it dies; an in-flight reply on the dying shim is still lost):
   ```bash
   ( UPSTREAM=$(tr '\0' '\n' < /proc/<shim-pid>/environ | sed -n 's/^GW_PROXY_UPSTREAM=//p')
     GW_PROXY_UPSTREAM="$UPSTREAM" GW_PROXY_PORT=4114 CCSESSION_DIR="$HOME/.claude/skills/ccsession-tag" \
       setsid nohup bash -c 'while :; do python3 "$CCSESSION_DIR/local-gateway-alias-proxy.py"; sleep 2; done' >/dev/null 2>&1 & )
   ```
   Stop it later with `pkill -f 'while :; do python3'` and then the shim it started, by pid.
3. New sessions are unaffected by old shims once the fix is installed; existing sessions keep their port for life.

## Follow-up tasks

- The "port already in use" message checks errno 48 (macOS value); on Linux EADDRINUSE is 98, so the friendly message never prints there (`local-gateway-alias-proxy.py:862`). Suggested type: bug.
- The shim records no exit and no end of stream; consider a shutdown/signal audit line and an opt-in default log path so a future death leaves evidence (wave1_6-branch-A.md). Suggested type: observability.
- A changed upstream URL in `~/.claude/ccsession.env` leaves the old shim (4013) serving older sessions while new launches move to 4114; this is by design, but it means two shims with different owners coexist. No change proposed. Suggested type: docs.

## Grounding Gaps

- auggie was unavailable; grounding used codegraph (python only), Grep and Read.
- The 4114 shims that died on 2026-11-01 are gone and their owners' scrollback was deleted; their owners (release-readiness@@5e7df77c, IB-CPlus-01@@b846db04) are inferred from Orca's daemon log and the surviving sessions' reuse lines, not observed.
- The cut-off times (00:01, 22:59), the two error strings, and the coordinator's session on 4013 never failing are coordinator-reported (worker screens and the brief); they are not in a captured log span.
- Evidence validation dropped one claim in pass 1 (evidence-validation.md) and three in pass 2 (evidence-validation-pass2.md); all were reworded to what the evidence supports. The drops keep the report status at partial.
- The Tier 1 card's exclusion "4013 uses the same upstream" (tier1-hypothesis.md, Alternatives) is contradicted by later evidence (O12: the upstreams differ); the report does not rely on 4013 as an upstream control. The card was calibrated before O12 existed.
- The owner elimination counts Orca terminal creations, not ccsession launches; a long-lived terminal could relaunch ccsession later. Hence "best-fitting" and "inferred".
- The reproduction emulates Orca's descendant sweep with a script; Orca itself was not driven. Whether Orca also signals the whole process group is not established; the fix covers both.

## Next Steps

- The skill's Tier 3 remediation offer requires status `success`, so it is not offered from this partial report. The coordinator brief directly instructs the fix via `/sc:workflow` then `/sc:implement`; that runs as a separate, brief-directed step (recorded under Remediation below), followed by `/sc:reflect --mode post` before committing.
- Informational tasklist row (no discriminator rows): optional `GW_PROXY_LOGFILE` env override in `~/.claude/ccsession.env` for operators who want routing events persisted (diagnosability-tasklist.md Task 1).

## Remediation (applied after diagnosis, brief-directed)

- **Plan.** `/sc:workflow` wrote the plan package `TASK-WF-detachTheCcsessi-20261102-034618` under `.dev/tasks/` (`to-do/`, or `done/` once archived). Its advisory pre-execution reflection is `.dev/reflect/pre-detachTheCcsessi-20261102035312/REPORT.md` (status partial, confidence 0.85). Its medium findings were applied during implementation:
  - Test A runs with its own HOME.
  - The sweep runs before the assertions, and the stream thread records its exceptions.
  - The cleanup checks the exact pid and the per-test copy path, never a generic match.
  - `setsid` runs only when stderr is not a terminal.
  - Test A asserts the shim's session differs from the terminal's.
  - The CHANGELOG notes that a shim already running keeps the old behaviour.
- **Execution.** `/sc:implement` ran Tasks 1-5. Each task was reviewed by a fresh reviewer and all five are compliant; the ledger is the package's `progress.md`.
- **Changes:**
  - `ccsession` starts the shim from a `( ... & )` subshell.
  - `local-gateway-alias-proxy.py` calls `os.setsid()` when stderr is not a terminal.
  - Two regression tests were added in `tests/unit/test_ccsession_tiers.py`.
  - The CHANGELOG has an Unreleased entry.
- **Validation before commit:**
  - Both new tests fail at HEAD and pass with the fix.
  - Every test file that reads the edited files passes: 457 passed.
  - `make lint` and `make verify-sync` pass.
  - Live check: live-check/after.txt shows the shim is not a descendant of the closed terminal, its stream finished, and the port still answers. Before the fix, live-check/before.txt showed it was killed.
  - The running shims on 4013 (pid 1788) and 4114 (pid 2258510) were never touched; their pids were the same before and after.
- **Fix confidence check:** confidence-check-fix.md (1.00).
- **Post-execution reflection** (`/sc:reflect --mode post`, Tier 2, gate before commit): `.dev/reflect/post-detachTheCcsessi-20261102044547/REPORT.md`.
  - Result: all 13 acceptance criteria met, no regression, contract status partial.
  - Five low-severity deviations: three necessary, two CHANGELOG-wording drift.
  - Four grounding-gap rows, none of which changes a verdict.
  - Residual risk: hosts other than this Linux workspace (for example Orca on macOS) are unverified.

## Audit

- **Hypothesis cards**: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/tier1-hypothesis.md (calibration: tier1-calibration.md, 0.92 STOP)
- **Adversarial artifacts**: Not invoked — single proposal
- **Root-cause confidence check**: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/confidence-check-root-cause.md (1.00)
- **Fix confidence check**: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/confidence-check-fix.md (1.00)
- **Audit log**: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/audit.log

## Pipeline Hardening Closure

**Applicable**: true
**Closure verdict**: advisory
**Waiver status**: none
**Backtest status**: not_run
**Off-path review**: required

**Wave statuses**:

- **HC0 Applicability + Boundary Scan**: PASS — CLI-to-subprocess boundary; typed boundary scan in hardening-closure.md.
- **HC1 Runtime-Entrypoint Verification**: N/A at diagnosis time (fix not applied); replay and negative witness pre-registered (negative witness observed: live-check/before.txt). Re-evaluated after implementation: PASS — positive witness observed in live-check/after.txt and the regression test (hc1-runtime-entrypoint.md).
- **HC2 Contract Enumeration**: PASS — producers, consumers and the README sibling launch path classified.
- **HC3 Unmask + Sweep**: N/A — no generated artifact or classifier involved.
- **HC4 Effective-Input Proof**: N/A — no review gate consumes an indirect selector.
- **HC5 Off-Path Reviewer + Waiver**: PASS — off-path review required; `/sc:reflect --mode post` performed it with two heterogeneous reviewers and an adversarial merge (.dev/reflect/post-detachTheCcsessi-20261102044547/REPORT.md); the PR reviewers follow.

**Evidence cards**:

- Runtime-entrypoint card: /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/hc1-runtime-entrypoint.md
- Contract ledger: /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/hc2-contract-ledger.md
- Unmask/sweep card: —
- Effective-input card: —

**Known escapes caught**: None claimed

**Closure blockers**:

- ADVISORY — scoped closure with rationalized N/A
