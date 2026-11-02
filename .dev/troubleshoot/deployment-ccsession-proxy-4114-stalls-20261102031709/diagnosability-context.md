# Diagnosability Context Card

**Issue**: ccsession gateway shim on 127.0.0.1:4114 disappears; sessions reusing it see "Connection lost mid-response" then ECONNREFUSED.
**failing_component**: src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py (process lifetime) started by src/superclaude/skills/ccsession-tag/ccsession setup_shim (ccsession:752-830)
**Verdict**: partial
**Complexity**: trivial (score 1: scope spans > 2 files +1; no intermittent/performance keywords; cause class "Other: process lifecycle")
**Hard-stop fired**: false
**Round**: n/a (discriminator-required: no, no counted emission)
**Captured bytes (failing run)**: n/a (shim stdout/stderr are /dev/null; no GW_PROXY_LOGFILE)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | yes (external) | Not from the shim (Branch A: no shutdown log; Branch B: all sinks filtered_out). Answered by Orca's daemon.log session-killed timestamps (tier1-observation.md O7) aligned to the worker screen times. |
| Where | yes (external) | ps/proc process tree of the live 4114 shim (O2) and the Orca descendant-sweep code (O8). |
| Why   | yes (runtime repro) | Live reproduction from worktree source (O10): closing the launching terminal kills the shim, cuts the stream and refuses the port. The shim's own instrumentation could not have shown it. |

## Branch A — Log-call inventory

Total: ~45 hits. The shim's signal is audit()/log_message/print to stderr plus default socketserver tracebacks; exception handlers around streaming are mostly silent; no signal handler, atexit or shutdown log. `degraded`: true.

## Branch B — Log-config reachability

Effective sink for the shim: /dev/null (ccsession:804). GW_PROXY_LOGFILE is opt-in and set by nothing shipped. Reachability: shim sites filtered_out 3, launcher echo lines reaches_sink 1 (terminal, not saved). `degraded`: true.

## Sufficiency rubric application

Row fired: degradation cap (auggie unavailable, Grep/Glob found signal => partial). S14 does not apply (no layer substitutes the disputed datum; the datum was captured directly by the live reproduction). Without the external evidence the shim-only instrumentation would fire S10-like `insufficient` for When/Why; the external daemon log, ps tree and reproduction cover all three W's.

## Implication for diagnosis confidence

The shim itself logs nothing that survives (stderr -> /dev/null, no shutdown/signal log).
Gap: the shim cannot report when or why it exited; earlier shim deaths left no trace of their own.
Consequence: the diagnosis rests on Orca's daemon log, the live process tree and a runtime reproduction, not on shim logs; that evidence is direct and sufficient for this mechanism.
Next step: proceed to hypothesis formation; optional invocation-site logging (GW_PROXY_LOGFILE) is listed in the tasklist for operators who want future exits recorded.

## Tasklist reference

.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/diagnosability-tasklist.md
