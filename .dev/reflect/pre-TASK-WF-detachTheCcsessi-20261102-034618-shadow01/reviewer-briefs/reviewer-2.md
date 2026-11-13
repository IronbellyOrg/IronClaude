# Reviewer 2 brief (persona: qa)

Mode UC-1 (pre-execution). You are read-only: return findings, run nothing, edit nothing.
Persona: qa. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## T1 card excerpt

## Coverage / acceptance section (qa slice)

Pass 1 (regex): 0 IDs in the spec, 0 in the tasklist. Pass 2: 2 inferred rows from source.md:1 (INF-001 the detach directive; INF-002 the four-file deliverable list). Deterministic containment match: INF-001 to Task 4 (0.7059), INF-002 to Task 3 (0.72). `coverage_pct` is null (no parsed rows); `coverage_pct_union` is 1.0; `coverage_degraded: parsed-sparse`.

- **F5 (Medium) The 100% union coverage is vacuous.** The spec is one line (source.md:1) that delegates every real requirement to `remediation-source.md`. INF-002 (a file list) matches Task 3 only through word overlap, because the rule has no notion of "this task owns the four files". A manual supplementary map of remediation-source.md (Required change 1-4, AC1-AC6) to the tasks finds every item covered: change 1 to Task 4, change 2 to Task 3, 3a to Task 1, 3b to Task 2, change 4 to Task 5, AC1 to T1/T2/T4 ACs, AC2 to T3.AC2 and T5.AC2, AC3 to T4.AC3, AC4 to T5.AC2, AC5 and AC6 to Constraints. This supplementary map is not a contract field.
- Verified not a gap: T5.AC2's grep pattern (`local-gateway-alias-proxy|ccsession-tag`) is a superset of remediation-source AC2's pattern at HEAD (11 files versus 9).
- AC6 items (argv keeps the script path, bash 3.2, logging opt-in) are enforced as Constraints only; `bash -n` checks syntax, not 3.2 compatibility.
- remediation-source.md "Pipeline Hardening" HC5 (off-path review with `/sc:reflect --mode post`) has no tasklist item; it is a downstream step, not a plan defect.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T20:01Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:19-21

```markdown
- Scope is exactly the four files named in the source: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md`. Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341).
- Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them); never edit anything under `~/.claude`, `~/.ccsession` or the running config; never run `superclaude install`, `superclaude update`, `./update.sh` or `install.sh`.
- Doc restrictions (remediation-source.md AC6; doc-context.md in the troubleshoot directory): the shim's argv keeps the script path (ccsession uses `pgrep -f -- "$CC_SHIM_SCRIPT"` at ccsession:722 and users stop shims with `pkill -f local-gateway-alias-proxy.py`); the shim inherits the launching env; no `setsid` binary (macOS has none) and only Python standard library; bash 3.2 syntax; logging stays opt-in; ccsession never stops a running shim.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:52-52

```markdown
In `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` `__main__` (lines 857-872), before `ThreadingServer(LISTEN, Handler)` binds, call `os.setsid()` inside `try/except OSError: pass` (it raises when the process already leads a process group, for example when run by hand in an interactive shell), with a short comment saying why: a shim is shared by many sessions, so terminal or process-group signals aimed at the session that started it must not reach it. No fork, no new import (`os` is already imported), argv and env unchanged.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:64-64

```markdown
In `src/superclaude/skills/ccsession-tag/ccsession` `setup_shim`, wrap the start statement at lines 801-804 (`GW_PROXY_UPSTREAM=... GW_PROXY_PORT=... CCSESSION_DIR=... nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &`) in a `( ... )` subshell so the subshell exits at once and the shim is no longer a descendant of the launching terminal (Orca kills a closed terminal's descendants; issue #341). Update the comment above it (lines 799-800) to say this, keep the env assignments and the redirect, keep bash 3.2 syntax. The listener and health waits that follow (lines 805-824) stay unchanged.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:69-70

```markdown
- Live check against the changed source: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>` (starts a throwaway shim on a free port through the real ccsession and kills only processes it started) writes its output to `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/after.txt`, which shows `shim is a descendant of the terminal: False`, `stream finished: True`, the port still answering, and the surviving throwaway shim stopped by its pid; the scratch dir is removed afterwards.
- The live shims on ports 4013 and 4114 report the same pids before and after (`curl -s http://127.0.0.1:<port>/__ccsession_shim`), recorded in ./artifacts/t4-tests.log.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:78-82

```markdown
In `CHANGELOG.md` under `## [Unreleased]`, add a `### ccsession: shim survives its launching terminal (#341)` section with a `#### Fixed` bullet in plain words: the shared gateway shim was started inside the terminal that first launched it, so closing that terminal (Orca kills its descendants) cut every other session's reply and refused new ones until a later launch started a new shim; ccsession now starts it from a subshell and the shim starts its own session, so it keeps running until stopped (`pkill -f local-gateway-alias-proxy.py`).

Acceptance criteria:
- The new section sits directly under `## [Unreleased]`, references #341, and names no file outside the scope.
- Every test file that reads the edited files (found with `grep -rlE "local-gateway-alias-proxy|ccsession-tag" tests/` and listed in ./artifacts/t5-checks.log) passes, and `make lint` and `make verify-sync` pass, with commands and results in ./artifacts/t5-checks.log.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/source.md:1-1

```markdown
Detach the ccsession gateway shim from the terminal that starts it, as specified in .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md (diagnosis: REPORT.md in the same directory; issue #341). Code: src/superclaude/skills/ccsession-tag/ccsession (setup_shim start statement lines 797-804), src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py (__main__), tests/unit/test_ccsession_tiers.py, CHANGELOG.md.
```

### .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md:9-26

```markdown
## Required change (scope: exactly these, nothing else)

1. `src/superclaude/skills/ccsession-tag/ccsession` — wrap the shim start statement (lines 801-804) in a `( ... )` subshell so the subshell exits at once and the shim is reparented away from the launching terminal. Update the comment above it to say why. Keep bash 3.2 syntax, keep the env assignments (GW_PROXY_UPSTREAM, GW_PROXY_PORT, CCSESSION_DIR) and the `>/dev/null 2>&1` redirect.
2. `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` — in `__main__`, before binding, call `os.setsid()` so the shim leaves the launcher's session and process group; ignore `OSError` (raised when the process already leads a process group, e.g. run by hand in an interactive shell). Add a short comment. No new imports beyond `os` (already imported), no fork, argv unchanged.
3. Regression tests in `tests/unit/test_ccsession_tiers.py` (reuse StandInGateway, `_free_port`, `_defaults`, TIER_BLOCK, `_ask_raw`, SKILL_DIR):
   a. `test_shim_outlives_the_terminal_that_started_it`: run the real `ccsession` (fake `claude` that records ANTHROPIC_BASE_URL then `exec sleep 60`) in its own session (`start_new_session=True`, an Orca-terminal stand-in) with `CC_SHIM_SCRIPT` = a per-test copy of the shim; wait for the seen file; read the shim pid from `/__ccsession_shim`; assert the shim pid is not among the terminal root's descendants (walk `ps -axo pid=,ppid=`); start a streamed tier2 request with `gateway.script["muse-spark-1.3"] = [("pause-stream", 4)]`; 1 s later SIGTERM every descendant of the root plus the root, then SIGKILL survivors; assert the reply status is 200 and ends with `message_stop`, and the health endpoint still reports the same pid. Clean up: kill the shim by pid and `pkill -f <copy path>`; close the gateway; kill the root group if still alive.
   b. `test_a_directly_started_shim_leaves_the_launchers_session`: start the shim with the existing `shim` fixture (Popen from the test process) and assert `os.getsid(<shim pid>) != os.getsid(0)` and `os.getpgid(<shim pid>) != os.getpgid(0)`; the fixture's `terminate()` must still stop it.
   Both must fail on the current code and pass after the change.
4. `CHANGELOG.md` — one Unreleased entry (Fixed) describing the fix in plain words, referencing #341.

## Acceptance criteria

- AC1: the new tests fail before the change (verified by running them against the unmodified source) and pass after.
- AC2: `uv run pytest tests/unit/test_ccsession_tiers.py tests/unit/test_ccsession_tag.py -q` passes, plus any other test file that reads the edited files (find them with `grep -rln "local-gateway-alias-proxy\|ccsession-tag/ccsession\|SKILL_DIR / \"ccsession\"" tests/`). Never run the full suite or tests/cli/eval/ as a directory.
- AC3: live check: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree> <private scratch dir>` against the changed source prints `shim is a descendant of the terminal: False`, `stream finished: True`, and the port still answers; output saved as live-check/after.txt; the surviving throwaway shim is stopped by its exact pid.
- AC4: `make lint` and `make verify-sync` pass.
- AC5: nothing under `~/.claude`, `~/.ccsession` or the running config is edited; the live shims (ports 4013 and 4114) are never signalled; `superclaude install/update` is not run.
- AC6: the doc restrictions hold: script path stays in the shim's argv (ccsession:722 `pgrep -f`), env is inherited, no `setsid` binary is required, logging stays opt-in, no running shim is ever stopped by ccsession.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/live-pids-before.txt:1-3

```
live shim baseline before any change (2026-11-02T04:26:09Z, curl -s http://127.0.0.1:<port>/__ccsession_shim)
port 4013 pid 1788
port 4114 pid 2258510
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 detach directive (source.md:1) | F5 | containment to Task 4 (0.7059) | source.md:1 |
| INF-002 four-file list (source.md:1) | F5 | containment to Task 3 (0.72), mechanical | source.md:1 |
| remediation-source change 1 | - | Task 4 | tasklist:64 |
| remediation-source change 2 | - | Task 3 | tasklist:52 |
| remediation-source change 3a / 3b | - | Task 1 / Task 2 | tasklist:29,40 |
| remediation-source change 4 | - | Task 5 | tasklist:78 |
| AC1-AC6 | - | T1/T2/T3/T4/T5 ACs and Constraints | tasklist:19-21,34,43,56,67-70,82 |
