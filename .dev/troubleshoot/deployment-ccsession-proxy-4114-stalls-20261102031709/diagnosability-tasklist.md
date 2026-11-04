# Diagnosability Tasklist
**Issue**: ccsession gateway shim on 4114 disappears, cutting and then refusing reused sessions
**Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py  **Round**: n/a (no counted emission)  **re-run permitted**: no (live shims 1788/2258510 must never be signalled; a throwaway shim on a free port is permitted)  **discriminator-required**: no  **capability-verdict**: n/a
**branch**: fix/ccsession-proxy-stall  **repro-venue-id**: live-check/orca_close_repro.py (throwaway shim, free port)

## Emitter search
emitter-search: n/a (no single-expression predicate; the disputed condition is the shim process's lifetime)
emitters-found: 0
already-read-files: 2 (local-gateway-alias-proxy.py, ccsession)
usable-capture-routes: 1 — Orca daemon log `/home/coder/.config/orca/logs/daemon.log` (session-killed events, read-only, already captured in tier1-observation.md O7); plus the live throwaway reproduction (O10). Shim stderr / audit(): excluded (sink is /dev/null at ccsession:804; GW_PROXY_LOGFILE unset).

## Discriminator rows
core-rows=0, pack-rows=0, total-rows=0. No discriminator required: one mechanism, directly reproduced (O10).

## Fix candidate
Proposal only (governed by the --fix flow in REPORT.md): detach the shim from the launching terminal's process tree and session (ccsession:801-804 and local-gateway-alias-proxy.py `__main__`). Paired verification: live-check/orca_close_repro.py must print `shim is a descendant of the terminal: False`, `stream finished: True`, and the port must still answer.

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
### Task 1: Persist the shim's audit lines at the invocation site (optional, operator)
- Invocation site: `~/.claude/ccsession.env` (sourced at ccsession:667-671).
- Current code: no GW_PROXY_LOGFILE line.
- Task type: 1 (env override). Add `export GW_PROXY_LOGFILE="$HOME/.claude/ccsession-shim.log"  # Diagnosability-tasklist instrumentation: revert after defect closed.`
- Rationale: answers WHEN for future routing events (stream starts, gateway unreachable); it still cannot record the shim's own exit (no shutdown log exists).

## Verification
After Task 1, a new shim's routing lines appear in the file on the next request.

## Rollback
Remove the export line from `~/.claude/ccsession.env`; new shims stop writing the file.

## Patch-round counter
Not incremented (discriminator-required: no). Authoritative store `.dev/troubleshoot/diagnosability-rounds.json` untouched.
