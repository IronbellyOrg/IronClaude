---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-detachTheCcsessi-20261102-034618
version: "1"
priority: Medium
created_date: "2026-11-02"
---

# Detach the ccsession gateway shim from the terminal that starts it

Source: ./source.md
Goal: A ccsession gateway shim keeps serving every session on its port when the terminal that launched it is closed or killed, because the shim is no longer a descendant of that terminal and no longer in its session or process group.

## Constraints

- Scope is exactly the four files named in the source: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md`. Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341).
- Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them); never edit anything under `~/.claude`, `~/.ccsession` or the running config; never run `superclaude install`, `superclaude update`, `./update.sh` or `install.sh`.
- Doc restrictions (remediation-source.md AC6; doc-context.md in the troubleshoot directory): the shim's argv keeps the script path (ccsession uses `pgrep -f -- "$CC_SHIM_SCRIPT"` at ccsession:722 and users stop shims with `pkill -f local-gateway-alias-proxy.py`); the shim inherits the launching env; no `setsid` binary (macOS has none) and only Python standard library; bash 3.2 syntax; logging stays opt-in; ccsession never stops a running shim.
- Tests: run only named test files and tests that read the edited files; never the full suite and never `tests/cli/eval/` as a directory. Use `uv run` for Python.
- Every throwaway shim or test process started while working is stopped by its exact pid; no temp files left behind.

## Phase 1: Regression tests that capture the failure

## Task 1: Add a test that a launched shim survives the terminal that started it

In `tests/unit/test_ccsession_tiers.py`, add `test_shim_outlives_the_terminal_that_started_it` next to `test_a_busy_shim_is_never_stopped_by_a_new_launch` (around line 1379), reusing `StandInGateway` (line 488), `_free_port` (568), `_defaults`/`TIER_BLOCK`, `_ask_raw` (1051) and `SKILL_DIR`. Mirror `_real_launch` (1344) but start the real `SKILL_DIR / "ccsession"` with `subprocess.Popen(..., start_new_session=True)` (a stand-in for an Orca terminal) and a fake `claude` that writes `$ANTHROPIC_BASE_URL` to a seen file and then `exec sleep 60`; `CC_SHIM_SCRIPT` is a per-test copy of `local-gateway-alias-proxy.py` in `tmp_path`, `CC_SHIM_PORT` a free port. After the seen file appears: read the shim pid from `/__ccsession_shim`; compute the terminal root's descendants by walking `ps -axo pid=,ppid=`; set `gateway.script["muse-spark-1.3"] = [("pause-stream", 4)]` and start `_ask_raw(url, "claude-gw-tier2", stream=True)` in a thread; after 1 s send SIGTERM to every descendant of the root and the root, wait 0.5 s, SIGKILL survivors (this is what Orca does when it closes a terminal: remediation-source.md Summary, troubleshoot `tier1-observation.md` O8). Clean up in `finally`: kill the shim by its pid, `pkill -f` the per-test copy path, close the gateway, and kill any remaining root process.

Acceptance criteria:
- The test asserts the shim pid is not among the terminal root's descendants, the streamed reply returns status 200 and contains `b"message_stop"`, and `/__ccsession_shim` still answers with the same pid after the terminal is gone.
- Run against the unmodified source, the test fails (record the command and its failing output in ./artifacts/t1-before.log).
- No shim or sleep process from the test is left running after it finishes (checked with `pgrep -f <tmp copy path>` returning nothing).

## Task 2: Add a test that a directly started shim leaves the starter's session

Depends on: Task 1

In `tests/unit/test_ccsession_tiers.py`, add `test_a_directly_started_shim_leaves_the_launchers_session` using the existing `shim` fixture (line 574-614, which starts the shim with `subprocess.Popen` from the test process). Read the shim pid from `/__ccsession_shim` and assert `os.getsid(pid) != os.getsid(0)` and `os.getpgid(pid) != os.getpgid(0)`. The fixture's `proc.terminate()` must still stop the shim at teardown (the shim stays the Popen child).

Acceptance criteria:
- The test fails against the unmodified source (output appended to ./artifacts/t1-before.log) and needs no new fixture.
- After the fixture's teardown the shim process is gone (assert in the test or verify with `pgrep -f` that no shim from this test survives).

## Phase 2: Start the shim in its own session

## Task 3: Make the shim leave the launcher's session and process group at start-up

Depends on: Task 2

In `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` `__main__` (lines 857-872), before `ThreadingServer(LISTEN, Handler)` binds, call `os.setsid()` inside `try/except OSError: pass` (it raises when the process already leads a process group, for example when run by hand in an interactive shell), with a short comment saying why: a shim is shared by many sessions, so terminal or process-group signals aimed at the session that started it must not reach it. No fork, no new import (`os` is already imported), argv and env unchanged.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k "directly_started_shim" -q` passes.
- `uv run pytest tests/unit/test_ccsession_tiers.py -q` and `uv run pytest tests/unit/test_ccsession_tag.py -q` pass except `test_shim_outlives_the_terminal_that_started_it`, which still fails until Task 4 (its failure reason recorded in ./artifacts/t3-tests.log).

## Phase 3: Reparent the launched shim away from the terminal

## Task 4: Start the shim from a subshell in ccsession setup_shim

Depends on: Task 3

In `src/superclaude/skills/ccsession-tag/ccsession` `setup_shim`, wrap the start statement at lines 801-804 (`GW_PROXY_UPSTREAM=... GW_PROXY_PORT=... CCSESSION_DIR=... nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &`) in a `( ... )` subshell so the subshell exits at once and the shim is no longer a descendant of the launching terminal (Orca kills a closed terminal's descendants; issue #341). Update the comment above it (lines 799-800) to say this, keep the env assignments and the redirect, keep bash 3.2 syntax. The listener and health waits that follow (lines 805-824) stay unchanged.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k "outlives_the_terminal or directly_started_shim or busy_shim_is_never_stopped" -q` passes (output in ./artifacts/t4-tests.log).
- `bash -n src/superclaude/skills/ccsession-tag/ccsession` succeeds.
- Live check against the changed source: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>` (starts a throwaway shim on a free port through the real ccsession and kills only processes it started) writes its output to `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/after.txt`, which shows `shim is a descendant of the terminal: False`, `stream finished: True`, the port still answering, and the surviving throwaway shim stopped by its pid; the scratch dir is removed afterwards.
- The live shims on ports 4013 and 4114 report the same pids before and after (`curl -s http://127.0.0.1:<port>/__ccsession_shim`), recorded in ./artifacts/t4-tests.log.

## Phase 4: Record and prove the change

## Task 5: Add the CHANGELOG entry

Depends on: Task 4

In `CHANGELOG.md` under `## [Unreleased]`, add a `### ccsession: shim survives its launching terminal (#341)` section with a `#### Fixed` bullet in plain words: the shared gateway shim was started inside the terminal that first launched it, so closing that terminal (Orca kills its descendants) cut every other session's reply and refused new ones until a later launch started a new shim; ccsession now starts it from a subshell and the shim starts its own session, so it keeps running until stopped (`pkill -f local-gateway-alias-proxy.py`).

Acceptance criteria:
- The new section sits directly under `## [Unreleased]`, references #341, and names no file outside the scope.
- Every test file that reads the edited files (found with `grep -rlE "local-gateway-alias-proxy|ccsession-tag" tests/` and listed in ./artifacts/t5-checks.log) passes, and `make lint` and `make verify-sync` pass, with commands and results in ./artifacts/t5-checks.log.
