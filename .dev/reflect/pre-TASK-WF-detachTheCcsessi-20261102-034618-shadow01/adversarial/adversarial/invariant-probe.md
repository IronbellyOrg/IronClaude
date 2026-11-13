# Invariant Probe Results

## Round 2.5: fault-finder analysis (opus-class agent, read-only)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Following the plan alone keeps every session served after a terminal closes | UNADDRESSED | MEDIUM | plan:20 forbids install/update and `~/.claude`; shims already running keep the old code and are reported stale (ccsession:1011-1013); sessions on them stay exposed until they stop |
| INV-002 | interaction_effects | A reparented shim leaves the terminal's tree (goes to init) | UNADDRESSED | MEDIUM (inferred) | orphans go to the nearest subreaper; claim cites launch-job-identity.sh:310-312, 483-484 (not yet re-Read by the orchestrator) |
| INV-003 | sufficiency_challenge | The plan's tests prove "no longer in its session or process group" on the real launch path | UNADDRESSED | MEDIUM | plan:32 checks descendant/200/message_stop/pid only; session check only on direct start (plan:40); HEAD added `getsid` assertion at test:2019 |
| INV-004 | guard_conditions | `os.setsid()` runs when ccsession starts the shim | ADDRESSED | LOW | proxy:1015-1019; ccsession:1037 |
| INV-005 | state_variables | Shim never sits in the terminal's session while the terminal can close | ADDRESSED | LOW | proxy:1015-1028; ccsession:1040-1058 |
| INV-006 | interaction_effects | SIGHUP and bash 3.2 `( cmd & )` do not return the shim to the terminal | ADDRESSED | LOW | nohup; stdout/stderr to /dev/null (ccsession:1037) |
| INV-007 | count_divergence | Descendant snapshot and pid checks count the right processes | ADDRESSED | LOW | test:1908, 2002, 2009, 2017-2018 |
| INV-008 | collection_boundaries | A colliding port cannot reuse or kill another live shim | ADDRESSED | LOW | ccsession:949-955, 1015-1017; test:1964, 2026-2028 |

## Summary

- Total findings: 8; ADDRESSED 5; UNADDRESSED 3 (HIGH 0, MEDIUM 3, LOW 0)
- Convergence gate: no HIGH + UNADDRESSED item, so convergence is not blocked. MEDIUM items are warnings carried into the report.
- Fault-finder limits (its own words): did not confirm that Orca kills by walking descendants rather than by control group; did not confirm ccsession is ever launched inside a governed Bash call (INV-002 inferred).
- Orchestrator note: INV-003's premise "if setsid were skipped on the ccsession path" cannot occur by construction, because `os.setsid()` lives in the shim itself and runs on every start except under the `isatty` guard; the finding is kept as a test-coverage gap (minor), not a goal failure.
