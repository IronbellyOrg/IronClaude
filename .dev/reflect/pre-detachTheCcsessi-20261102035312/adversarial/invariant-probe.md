# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent general-purpose agent (read-only), persisted by the orchestrator on receipt.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | subshell + setsid keeps the shim working after its terminal dies, whatever started it | UNADDRESSED | MEDIUM | stderr writes on every request (local-gateway-alias-proxy.py:490-491, 126-127; only the log-file write is guarded, 129-133). ccsession path is safe (stderr /dev/null, ccsession:804). A shim started by hand through a wrapper (`uv run`, `make`, IDE) is not a group leader, so setsid succeeds, the shim keeps the pty as stderr and no longer gets SIGHUP; after the terminal closes every stderr write fails (EIO), health fails, and ccsession classes the port "other" (ccsession:785-788) and refuses. Fix: setsid only when stderr is not a terminal, or document. |
| INV-002 | sufficiency_challenge | Test A proves both halves of the fix | UNADDRESSED | MEDIUM | Task 1 (plan:29) signals only ppid-walk descendants, never the process group/session, so Test A greens with the subshell alone; the setsid half on the ccsession path is unproven (REPORT.md: process-group signalling by Orca not established). Fix: assert `os.getsid(shim_pid) != os.getsid(root_pid)` in Test A, or killpg the root's group. |
| INV-003 | sufficiency_challenge | Orca finds a terminal's processes only by ppid (maybe pgid) | UNADDRESSED | LOW | shim inherits ORCA_TERMINAL_HANDLE (tier1-observation.md O3 env listing); terminateOwnedTree read from minified code. If Orca matched by that handle or cgroup, neither change protects the shim. Record as residual risk. |
| INV-004 | interaction_effects | the orphan is adopted outside the terminal tree | ADDRESSED (this host) | LOW | nearest PR_SET_CHILD_SUBREAPER ancestor adopts orphans; here PID 1 (`./coder agent`) reaps. On a non-reaping PID 1 a killed shim stays a zombie, so `kill -0` reports alive: F5 should check /proc/<pid>/stat state or the port. |
| INV-005 | guard_conditions | `&` stays inside the parentheses | ADDRESSED | LOW | `( ... ) &` would make python a direct child again; Test A catches it. |
| INV-006 | guard_conditions | subshell can abort setup_shim under `set -e` | ADDRESSED | LOW | ccsession:86 `set -e` only; a subshell with only a background command exits 0; no `$!` readers; test_ccsession_tag.py:811 needs `GW_PROXY_PORT="$CC_SHIM_PORT"` verbatim (kept). |
| INV-007 | guard_conditions | `except OSError: pass` only swallows the group-leader case on the ccsession path | ADDRESSED | LOW | non-interactive script, no `set -m`; shim never leads its group there. |
| INV-008 | state_variables | something between start and serve_forever still ties the shim to the terminal | ADDRESSED | LOW | stdin /dev/null (bash async + nohup), stdout/stderr /dev/null (ccsession:804), HUP/INT/QUIT ignored, no children/forks, socket created in the shim, setsid before bind so ccsession's waits (806-824) cannot complete before detach. |
| INV-009 | interaction_effects | setsid in the proxy breaks existing tests | ADDRESSED | LOW | no fork, pid unchanged (test_ccsession_tag.py:874 `pop("pid") == proxy.pid`; fixture terminate tests:611-613); runpy loaders use non-`__main__` run names, so setsid must stay inside `__main__`; real-launch tests clean up with `pkill -f <copy>`. |
| INV-010 | interaction_effects | Ctrl-C on pytest still stops test-started shims | UNADDRESSED | LOW | after setsid they rely only on fixture teardown; double Ctrl-C / SIGKILL / hard timeout leaves orphans. |
| INV-011 | collection_boundaries | lifelong shims fit in the six port slots | ADDRESSED (docs only) | MEDIUM | 6 attempts `base_port + 101*_attempt` (ccsession:769-770), stale shims never stopped (782-784); each update or settings change adds a permanent shim; 6 combinations later "no free shim port" (793-795) until restart or pkill. |
| INV-012 | count_divergence | listener check works with several shims alive | ADDRESSED | LOW | `pgrep ... \| head -n 1` (ccsession:722) used only for emptiness after a connect probe (721). |
| INV-013 | guard_conditions | EADDRINUSE branch reports a lost race | UNADDRESSED (pre-existing) | LOW | local-gateway-alias-proxy.py:862 checks errno 48 (macOS); Linux 98 -> traceback to /dev/null; no interaction with setsid placement. |

Orchestrator note (captured read-only this session, `ls -l /proc/2258510/fd`): the live 4114 shim also holds descriptors leaked from its Orca ancestors (fd 26, 43-46 Orca resource packs; fd 41/42 a pipe; fd 36 a socket; eventpoll/eventfd/inotify), because `nohup ... &` closes nothing beyond stdio. Not a kill path; hygiene only (LOW).

## Summary

- **Total findings**: 13
- **ADDRESSED**: 8
- **UNADDRESSED**: 5
  - HIGH: 0
  - MEDIUM: 2 (INV-001, INV-002)
  - LOW: 3 (INV-003, INV-010, INV-013)
- Invariant gate: no HIGH + UNADDRESSED -> convergence not blocked. WARNING: 2 MEDIUM-severity UNADDRESSED invariants (INV-001, INV-002) should be reviewed.
