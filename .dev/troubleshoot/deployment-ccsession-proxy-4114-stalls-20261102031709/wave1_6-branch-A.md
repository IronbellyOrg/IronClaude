# Wave 1.6 Branch A (log-call inspection) — returned by troubleshoot-analyst

degraded: true (Grep/Read only). captured_bytes: null for every hit (both live shims write to /dev/null; parent supplied no capture).

## Inventory (condensed from the returned JSON; file paths relative to src/superclaude/skills/ccsession-tag/)

| file:line | call_type | richness / note |
|---|---|---|
| local-gateway-alias-proxy.py:123 audit() | error_reporter_init (custom) | only persistent sink, active only with GW_PROXY_LOGFILE; second-resolution timestamp, no pid |
| local-gateway-alias-proxy.py:132 | exception_handler | silent (log-file write failure swallowed) |
| local-gateway-alias-proxy.py:91, 60, 62 | logger_call / exception_handler | startup config warnings/errors only |
| local-gateway-alias-proxy.py:490 log_message | logger_call | access line at send_response, before any body bytes; says nothing about stream completion; no timestamp |
| local-gateway-alias-proxy.py:580, 582, 599-600, 626 | logger_call | alias map events |
| local-gateway-alias-proxy.py:583, 610, 631, 636 | exception_handler | silent / access line only |
| local-gateway-alias-proxy.py:684, 696, 699 | exception_handler | minimal; audited by _forward_tier (730, 736), not by _proxy |
| local-gateway-alias-proxy.py:711, 730, 736, 755, 790, 798, 813, 817 | logger_call | tier routing events; 755 marks a stream START; nothing marks a stream END |
| local-gateway-alias-proxy.py:756 | exception_handler | silent try/finally |
| local-gateway-alias-proxy.py:762 | exception_handler | rich (error bodies only) |
| local-gateway-alias-proxy.py:834, 848 | exception_handler | silent: upstream EOF / client BrokenPipe leave no trace |
| local-gateway-alias-proxy.py:841 | logger_call | first 8 KB model sniff; no byte count or end |
| local-gateway-alias-proxy.py:852 | error_reporter_init | socketserver default handle_error traceback -> stderr (/dev/null); daemon_threads=True |
| local-gateway-alias-proxy.py:861 | exception_handler | checks errno 48 (macOS EADDRINUSE); Linux is 98, so the friendly message never prints on Linux (side finding) |
| local-gateway-alias-proxy.py:871-872 | print / exception_handler | startup line; no shutdown log, no signal handler, no atexit anywhere in ccsession-tag/ |
| local-gateway-alias-proxy.py:536 | health JSON | pull-based pid/active; ccsession discards them |
| ccsession:731 | exception_handler | silent curl failure -> "other" |
| ccsession:779, 783, 787, 794, 798, 811, 822 | print | launcher messages to the launching terminal only; no pid, no timestamp |
| ccsession:804 | error_reporter_init | `nohup python3 ... >/dev/null 2>&1 &`: all shim output discarded; no setsid/disown; shim stays in the launcher's session and process group |

## What the instrumentation can and cannot answer (returned summary)

- When did the shim exit: not from the shim (no shutdown log, all output to /dev/null).
- Which signal: not from the shim (SIGTERM/SIGKILL end it silently; SIGHUP ignored by nohup).
- Which streams were cut: not from the shim even with GW_PROXY_LOGFILE (only stream starts are logged).
