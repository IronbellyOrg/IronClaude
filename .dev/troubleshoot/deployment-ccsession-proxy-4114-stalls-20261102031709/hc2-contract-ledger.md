# HC2 — Contract ledger (shim process lifetime and identity)

| role | component | contract it relies on | classification after a detach fix |
|---|---|---|---|
| producer | ccsession setup_shim start (ccsession:797-804) | starts the shim with the session's env | changes: must start it detached |
| producer (sibling) | README.md:479-497 manual restart recipe (`nohup python3 ... &` at 494-495, inside a `( ... )` subshell opened at 480) | the subshell exits after starting the shim, so the shim is already reparented away from the terminal; it still shares the terminal's session and process group | swept: covered if the shim itself leaves the launcher's session at startup (os.setsid in the proxy); no README change needed for the reparenting |
| consumer | ccsession shim_listener_pid (ccsession:712-724): `lsof -ti tcp:PORT -s TCP:LISTEN`, else connect + `pgrep -f -- "$CC_SHIM_SCRIPT"` | listener pid discoverable; script path in argv | unchanged if argv keeps the script path and the detached process holds the listening socket |
| consumer | ccsession post-start waits (ccsession:806-824): listener appears within ~3 s, then health `match` | the shim answers health quickly after start | unchanged if the detach happens after bind and the grandchild serves |
| consumer | ccsession shim_health_status (ccsession:726-750): `pid`, `code`, `settings`, `port` | health fields | unchanged (`pid` becomes the detached process's pid) |
| consumer | Claude Code sessions (ANTHROPIC_BASE_URL) | the port keeps answering for the shim's lifetime | fixed: lifetime no longer tied to the launching terminal |
| consumer | user stop path README.md:415-418, 502 (`pkill -f local-gateway-alias-proxy.py`) | script path in argv | unchanged |
| consumer | tests: `shim` fixture (test_ccsession_tiers.py:574-614) terminates its Popen; `_real_launch` users clean up with `pkill -f <tmp shim path>` (e.g. 1416-1418) | direct-start shims stay children; launched shims found by argv | direct start must stay attached (fixture's proc.terminate() must still stop it); launched shims must keep argv |

Duplicate evaluators: none. Status: PASS (non-empty ledger, every consumer classified, sibling launch path identified).
