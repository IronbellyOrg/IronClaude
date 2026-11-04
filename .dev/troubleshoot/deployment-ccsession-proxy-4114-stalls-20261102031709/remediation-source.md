# Remediation source: detach the ccsession gateway shim from the terminal that starts it

Source report: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/REPORT.md (Tier 1, calibrated confidence 0.92). GitHub issue: IronbellyOrg/IronClaude#341.

## Summary

`ccsession` (src/superclaude/skills/ccsession-tag/ccsession, setup_shim, lines 797-804) starts the shared gateway shim `local-gateway-alias-proxy.py` with `nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &` and then `exec`s Claude Code. The shim therefore stays a descendant of the launching terminal, in its process group and session. Every later session with the same settings reuses that shim. When Orca closes the launching terminal it SIGTERMs, then SIGKILLs, every descendant; the shim dies, every other session's in-flight streamed reply is cut ("Connection lost mid-response") and the port refuses connections until some later launch starts a new shim. Live reproduction: the evidence directory's live-check/orca_close_repro.py (before.txt: descendant=True, stream finished=False, port refused).

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

## References

- REPORT.md, tier1-observation.md (O1-O12), hc1-runtime-entrypoint.md, hc2-contract-ledger.md, doc-context.md in .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/
- tests/unit/test_ccsession_tiers.py:488-614 (StandInGateway, `_free_port`, `shim` fixture), 1344-1419 (`_real_launch`, `test_a_busy_shim_is_never_stopped_by_a_new_launch`)

## Pipeline Hardening

Applicable: true (CLI -> subprocess boundary). Closure verdict: advisory (HC3/HC4 rationalized N/A). HC1 requires the replay to go through the real `ccsession` launch plus a terminal-descendant kill, with the negative witness already observed at HEAD (live-check/before.txt) and the positive witness produced by AC1/AC3. HC5: off-path review required (PR reviewers and /sc:reflect --mode post).
