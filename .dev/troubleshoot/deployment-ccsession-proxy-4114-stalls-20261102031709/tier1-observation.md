# Tier 1 observation

All commands below were run read-only from this worktree shell on 2026-11-02 between 03:17 and 03:20 UTC. No live shim was signalled.

## O1. What serves the ports (ps, run=2026-11-02T03:17Z, arm=both)

```
   1788       1     369     369 ?        Sat Oct 31 12:24:43 2026  1-14:53:00 Sl   239048 python3 /home/coder/.claude/skills/ccsession-tag/local-gateway-alias-proxy.py
2258510 2258462 2258462 2257514 pts/18   Mon Nov  2 03:08:37 2026       09:06 Sl+  70172 python3 /home/coder/.claude/skills/ccsession-tag/local-gateway-alias-proxy.py
```
Columns: pid ppid pgid sid tty lstart etime stat rss args. Port from /proc/<pid>/environ: 1788 GW_PROXY_PORT=4013; 2258510 GW_PROXY_PORT=4114.

## O2. Process tree of the 4114 shim (ps, same session 2257514)

```
2257514    1101 2257514 2257514 Mon Nov  2 03:08:20 2026 /bin/bash --rcfile /home/coder/.config/orca/shell-wrappers/d708bd5180e1f186/shell-ready/bash/rcfile
2258462 2257514 2258462 2257514 Mon Nov  2 03:08:36 2026 /opt/nvm/versions/node/v24.22.1/bin/claude --dangerously-skip-permissions ... --model claude-gw-tier1a[1m]
2258510 2258462 2258462 2257514 Mon Nov  2 03:08:37 2026 python3 /home/coder/.claude/skills/ccsession-tag/local-gateway-alias-proxy.py
```
The 4114 shim is a CHILD of a Claude Code process (2258462) in an Orca terminal (env: ORCA_TERMINAL_HANDLE=term_41eaf7f8-..., PWD=/home/coder/workspaces/worktrees/Coder/auggie-mcp-regNotConnected), a different worktree from the two failing workers (review-severity-rule). It is in that Claude's process group and terminal session, and in the terminal's foreground group (stat `Sl+`).

## O3. Process tree of the 4013 shim

pid 1788: ppid 1, pgid 369, sid 369 (369 = `/opt/Orca/orca-ide ... serve`, Orca's own process group), no tty. It was started 3 s after Orca itself (12:24:40) and later reparented to init. Nothing that closes a terminal can reach it.

## O4. Signal disposition (/proc/<pid>/status)

Both shims: `SigIgn: 0000000001001007` = SIGHUP, SIGINT, SIGQUIT, SIGPIPE, SIGXFSZ ignored. SIGTERM and SIGKILL are NOT ignored (and SIGKILL cannot be).

## O5. Logs

fd 0/1/2 of both shims -> /dev/null (`ls -l /proc/<pid>/fd`). GW_PROXY_LOGFILE is not set in either environ. `dmesg -T | grep -iE 'oom|killed process'`: no output. `journalctl ... | grep -iE 'oom|local-gateway|python3'`: no output. The shim keeps no log on disk: its death leaves no trace of its own.

## O6. Health of both shims (curl /__ccsession_shim, 03:18Z)

```
{'port': 4013, 'pid': 1788, 'code': '6e7d1d51209e49e6', 'settings': '3faa3b818eb0ab08', 'active': 4, 'model_data': '2026-10-28.1'}
{'port': 4114, 'pid': 2258510, 'code': '6e7d1d51209e49e6', 'settings': '3faa3b818eb0ab08', 'active': 4, 'model_data': '2026-10-28.1'}
```
Installed code digest now: 6e7d1d51209e49e6. Port arithmetic: models.py shim_port() = 4010 + 1 + digest % 97 = 4013 for these settings; 4114 = 4013 + 101, the first fallback port setup_shim tries when 4013 is held by a shim reported `stale` (ccsession:769-784).

## O7. Orca daemon log (/home/coder/.config/orca/logs/daemon.log) correlated with the worker failures

| daemon.log line | event | failure on the 4114 workers |
|---|---|---|
| 668-669 2026-10-31T23:44:24Z | session-created release-readiness@@5e7df77c | (38 s before worker 1297298 started 23:45:02 on 4114) |
| 680-681 2026-11-01T00:01:42Z | session-exited cause=signaled + session-killed immediate=true, release-readiness@@5e7df77c | 00:01 "Connection lost mid-response" ending a 16-min turn |
| (no shim up) | | 00:59 ECONNREFUSED |
| 744-745 2026-11-01T22:41:32Z | session-created IB-CPlus-01@@b846db04 | (6 min before worker 2089859 started 22:47:22 on 4114) |
| 750-751 2026-11-01T22:59:18Z | session-exited cause=signaled + session-killed immediate=true, IB-CPlus-01@@b846db04 | 22:59 "Connection lost mid-response" ending an 11-min turn, then ECONNREFUSED retries |
| 752-753 2026-11-02T03:08:20Z | session-created serve-46e81c2f (pid 2257514) | 03:08 shim back as pid 2258510, child of claude 2258462 in session 2257514 (O2) |

## O8. Orca kill mechanism (read from /opt/Orca/resources/app.asar.unpacked/out/main, minified)

- daemon-entry.js: `session-killed` is logged after `host.kill(n,{immediate:r})`; agent sessions are killed through `g.u(pid, ..., {terminateOwnedTree, terminateDescendants, awaitEscalation})` ("descendant-aware graceful kill").
- chunks/pty-descendant-exit-verification-DKf-exmf.js: builds the descendant set of the pty root from `ps -axo pid=,ppid=,pgid=,lstart=` by walking ppid links, then `for (t of e.descendants) n(t.pid, 'SIGTERM')` and, after a grace period, SIGKILL for any descendant still alive with the same start time and pgid.

So when Orca closes or kills a terminal session, every process whose ppid chain leads to that terminal gets SIGTERM, then SIGKILL. The shim started by `nohup ... &` from that terminal's ccsession launch is in that chain (O2) and does not ignore SIGTERM (O4).

## O9. Launch code (repo source)

- src/superclaude/skills/ccsession-tag/ccsession:801-804: `GW_PROXY_UPSTREAM=... GW_PROXY_PORT=... CCSESSION_DIR=... nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &` -- a plain background child; no new session, no reparenting.
- ccsession:1379-1440: the script then `exec`s Claude Code, so Claude becomes the shim's parent.
- ccsession:761-784: later launches with the same settings REUSE that shim ("Shim already running ... (reusing)"); nothing restarts it if it dies, until a later launch finds the port free and starts a new one (ccsession:772-774, 797-804).
- local-gateway-alias-proxy.py:857-872: `__main__` binds and serves; it never detaches itself.
- local-gateway-alias-proxy.py:99-117, 687: no read timeout once the gateway starts answering (`conn.sock.settimeout(None)`); FIRST_BYTE_TIMEOUT (300 s) applies only before the first byte of a tier stream. So a long turn is not cut by the shim's own timers.

## O10. Live reproduction, pre-fix (throwaway shim, run=2026-11-02T03:22Z, arm=HEAD f90877be source)

Script: `live-check/orca_close_repro.py` in this directory (run from a private scratch dir). It runs the REAL worktree `ccsession --shim` with a fake `claude` (`exec sleep 300`) inside its own session (an Orca-pty stand-in), on a free port, against a local stand-in gateway whose streamed reply pauses 5 s after the first event. 1.5 s into the reply it does what Orca's descendant sweep does: SIGTERM every descendant of the terminal root plus the root, then SIGKILL. Only processes the script started are signalled. Captured output (`live-check/before.txt`):

```
terminal root pid=2296743 shim pid=2296833 base=http://127.0.0.1:49961
shim is a descendant of the terminal: True
stream finished: False error=None bytes=53
port after close: URLError(ConnectionRefusedError(111, 'Connection refused'))
cleanup: shim pid 2296833 already gone
```

Both reported symptoms reproduce from one event: the streamed reply ends after 53 bytes with no `message_stop` (the shim speaks HTTP/1.0 close-delimited, so the client sees an early end of stream = "Connection lost mid-response"), and the port then refuses connections (ECONNREFUSED).

## O11. Producers of the observed strings

`grep -rn "Connection lost mid-response\|ECONNREFUSED" src/`: no hits. Both strings are produced by Claude Code's HTTP client, outside this repo; the repo-side producer of the condition is the shim process exiting.

## O12. Who started each 4114 shim, and why 4114 (added after evidence validation, run=2026-11-02T03:38Z)

Orca keeps terminal scrollback under `/home/coder/.config/orca/terminal-history/<session>/` (output.log / checkpoint.json; killed sessions' folders are gone). `grep -ohaE '\[ccsession\][^"\\]{0,140}'` over the surviving folders:

| session (created) | ccsession launch lines |
|---|---|
| review-severity-rule@@d1747ae5 (2026-10-31 23:45:02, worker 1297298) | `A shim with other settings or older code is on 127.0.0.1:4013; leaving it running for its sessions` / `Shim already running on 127.0.0.1:4114 (reusing)` |
| serve-c727018a (2026-11-01 22:46:55, claude 2088377, still alive, ANTHROPIC_BASE_URL=http://127.0.0.1:4114) | same two lines: `... 4013; leaving it running ...` / `Shim already running on 127.0.0.1:4114 (reusing)` |
| review-severity-rule@@d6954559 (2026-11-01 22:47:23, worker 2089859) | same two lines (reusing 4114) |
| serve-46e81c2f (2026-11-02 03:08:20, claude 2258462) | `... 4013; leaving it running ...` / `Starting model-alias shim on 127.0.0.1:4114` |

Files: `serve-c727018a-b59c-46c6-8ff4-8f60919250e0/output.log` (2 matching lines), `...review-severity-rule%40%40d1747ae5/checkpoint.json`, `...review-severity-rule%40%40d6954559/checkpoint.json`, `serve-46e81c2f-1d0c-4eff-abf8-2b697673c1c1/checkpoint.json` (1 matching line each).

Consequences:
- Every one of these launches found a 4114 shim ALREADY RUNNING and reused it (none started it), except serve-46e81c2f at 03:08, which started the current one. So the shim alive at 22:46:55 was started earlier, by a session created before 22:46:55; serve-c727018a is still alive today, so it did not own the shim that died at 22:59. Of the sessions created before 22:46:55, the only one killed at 22:59:18 is IB-CPlus-01@@b846db04 (daemon.log:750-751). Likewise the shim reused at 23:45:02 already existed; release-readiness@@5e7df77c (created 23:44:24) is the only session created between the previous kill (23:32:13) and 23:45:02, and it was killed at 00:01:42. The killed sessions' own scrollback is gone, so their "Starting model-alias shim" line cannot be shown directly.
- Why 4114 and not 4013: every launch reports the 4013 shim as "other settings or older code" (stale). Health now (curl /__ccsession_shim, 03:38Z): 4013 `upstream_sha=c7df6bb80904`, 4114 `upstream_sha=915eeb72d126` (sha256 prefix of the reported upstream URL), same `settings` 3faa3b818eb0ab08 and `code` 6e7d1d51209e49e6. The upstream differs, so ccsession's health check (ccsession:741-747) reports 4013 stale and moves to 4013 + 101 = 4114. `~/.claude/ccsession.env` was modified 2026-10-31 23:44:00, 24 s before the release-readiness session started the first 4114 shim.
