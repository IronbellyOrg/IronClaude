# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (independent agent, sonnet; persisted on receipt 2026-11-02T05:31Z)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | ccsession runs without job control, so the shim is not a group leader and `os.setsid()` succeeds | UNADDRESSED | MEDIUM | with `set -m`, exported `SHELLOPTS=monitor` or `bash -i`, the `&` at ccsession:808 makes the shim a group leader; setsid then fails with EPERM, swallowed at proxy:864-867; shim stays in the terminal's session (subshell still removes it from the ppid sweep); both tests use the no-job-control path (test:1486-1494, :595-598). Orchestrator note: ccsession is a `#!/bin/bash` script (ccsession:1) with no `set -m`. |
| INV-002 | sufficiency_challenge | Orca's close plus the kernel hangup is the only teardown path | UNADDRESSED at probe time (see Resolution) | HIGH | falsified by a cgroup/systemd-scope stop, logind KillUserProcesses / sshd session teardown, or an environment-tag match; the shim inherits the full environment (ccsession:805-808); T1/T2 cannot detect it (A-001 restated) |
| INV-003 | sufficiency_challenge | `python3` execs straight into the interpreter | UNADDRESSED | LOW | a non-exec wrapper (pyenv/conda launcher) would stay in the terminal's group/session while the child Python calls setsid (ccsession:808, proxy:863-865) |
| INV-004 | sufficiency_challenge | the shim is reparented to init or a subreaper outside the terminal tree | UNADDRESSED | LOW | a subreaper inside the terminal tree keeps the shim a descendant after the subshell exits (ccsession:804-809); setsid does not change ppid; raised only by V1 (U-003) |
| INV-005 | guard_conditions | the isatty guard only affects hand-run starts; missing stderr no worse than before | UNADDRESSED | LOW | ccsession always sends stderr to /dev/null (808); a hand-run start from a terminal stays in the terminal's session (contradicts unconditional CHANGELOG.md:11); stderr closed → AttributeError at proxy:863 before bind, where old code would bind and serve (per-request failure via audit, proxy:123-127, claimed by the calibrator) |
| INV-006 | count_divergence | existing shims are unaffected by this change | UNADDRESSED | LOW | editing proxy.py changes the code digest (models.py:772, proxy:169), so running shims read as stale (ccsession:782-784), are never stopped (762-764); each launch moves up a port, 6 tries (769), then "no free shim port" (793-796); CHANGELOG.md:11 covers old behaviour, not port use |
| INV-007 | state_variables | T1 and T2 prove survival of group/session signals | UNADDRESSED | LOW | T1 signals per pid from a ppid snapshot (test:1521-1532); T2/getsid compare ids only (test:1538, 1562-1563); no test signals a group or session and observes survival |
| INV-008 | interaction_effects | the comment's Ctrl-C rationale applies to the ccsession path | ADDRESSED | LOW | nohup (ccsession:808) ignores SIGHUP; non-interactive bash ignores SIGINT/SIGQUIT for async commands; the Ctrl-C text (proxy:859-862) fits hand-runs only, matching the consensus "imprecise comment" note |
| INV-009 | collection_boundaries | the shim is detached from the moment it starts | UNADDRESSED | LOW | imports and the digest (proxy:98-169) run before setsid (863-865); a group signal in that window still hits the shim; the proxy has no subprocess/fork/thread calls of its own |

## Summary (probe as returned)

- Total findings: 9
- ADDRESSED: 1
- UNADDRESSED: 8 — HIGH: 1 (INV-002), MEDIUM: 1 (INV-001), LOW: 6

## Resolution of the blocking item (targeted round, 2026-11-02T05:31Z)

Orchestrator evidence (read-only):
- `/proc/1788/cgroup` and `/proc/self/cgroup` both read `0::/init.scope`. All processes in this workspace share one cgroup, so there is no per-terminal scope to stop.
- The long-lived 4013 shim (pid 1788; PPID 1, PGID 369, SID 369, started Sat Oct 31 12:24:43) is detached the same way the fix detaches new shims. It has survived every terminal close since then, including the two closes on 2026-11-01 that killed the 4114 shims.

Advocate verdicts: both ACCEPT (advocate-v1 and advocate-v2, 2026-11-02T05:31Z). INV-002 → ADDRESSED for this environment (Linux Coder workspace under Orca). Residual (non-gating, MEDIUM, UNVERIFIED): Orca on macOS or other hosts, logind KillUserProcesses / sshd session teardown on such hosts, and an environment-tag teardown (no evidence either way; O8 shows a ppid walk). Re-check on macOS before relying on it there.

## Gate after resolution

- HIGH + UNADDRESSED: 0 → invariant gate passes.
- MEDIUM + UNADDRESSED (warning, non-blocking): INV-001; INV-002 residual (other hosts).
- LOW: INV-003, INV-004, INV-005, INV-006, INV-007, INV-009 (recorded as risks).
