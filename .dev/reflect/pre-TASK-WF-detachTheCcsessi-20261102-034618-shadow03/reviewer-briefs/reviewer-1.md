# Reviewer 1 brief (persona: analyzer)

Mode UC-1 (pre-execution). You are read-only: return findings, run nothing, edit nothing.
Persona: analyzer. Audit the plan for defects that would make a task fail, an acceptance criterion unmeetable, or a step contradict a constraint. The package was already executed and archived (progress.md FINAL: pass); the fix is in HEAD. Judge the PLAN as a plan, using HEAD only to verify the plan's anchors and claims.

## T1 card excerpt

## Findings

- **F1 (Medium) T5.AC2 depends on a step the plan never schedules.** T5.AC2 requires `make verify-sync` to pass (tasklist:82) while Constraints cap edits at four files (tasklist:19), three of them under src/. `verify-sync` diffs every `src/superclaude/skills/*/` against `.claude/skills/` (Makefile:166-174), so editing `src/superclaude/skills/ccsession-tag/` without a `make sync-dev` step leaves the tree drifted and the AC unmeetable as planned. The prior run hit exactly this and had to run sync-dev mid-task (artifacts/t5-checks.log; prior-run notes).
- **F2 (Medium) T4.AC4 reads a baseline nobody records.** T4.AC4 compares live-shim pids on ports 4013/4114 "before and after" (tasklist:70), but no task instructs capturing the "before" pids. The prior run improvised `artifacts/live-pids-before.txt`.
- **F3 (minor) Stale line anchors raise executor search cost.** tasklist:29 (busy-shim test ~1379; StandInGateway 488; _free_port 568; _ask_raw 1051; _real_launch 1344), tasklist:52 (proxy __main__ 857-872), tasklist:64 (ccsession start statement 801-804), tasklist:21 (pgrep at ccsession:722) vs HEAD anchors 1861/739/819/1464/1757, 1009-1028, 1033-1039, 932. Symbols are named alongside, so edits land correctly after a search.
- **F4 (minor) T1.AC3 over-claims cleanup scope.** "No shim or sleep process from the test is left running" checked via `pgrep -f <tmp copy path>` (tasklist:34) cannot see the `exec sleep 60` child: its argv contains no copy path. The check is sound for the shim only.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.
## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:22Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:19-23 (constraints)

```markdown
- Scope is exactly the four files named in the source: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md`. Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341).
- Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them); never edit anything under `~/.claude`, `~/.ccsession` or the running config; never run `superclaude install`, `superclaude update`, `./update.sh` or `install.sh`.
- Doc restrictions (remediation-source.md AC6; doc-context.md in the troubleshoot directory): the shim's argv keeps the script path (ccsession uses `pgrep -f -- "$CC_SHIM_SCRIPT"` at ccsession:722 and users stop shims with `pkill -f local-gateway-alias-proxy.py`); the shim inherits the launching env; no `setsid` binary (macOS has none) and only Python standard library; bash 3.2 syntax; logging stays opt-in; ccsession never stops a running shim.
- Tests: run only named test files and tests that read the edited files; never the full suite and never `tests/cli/eval/` as a directory. Use `uv run` for Python.
- Every throwaway shim or test process started while working is stopped by its exact pid; no temp files left behind.
```

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:52-56 (Task 3)

```markdown
In `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` `__main__` (lines 857-872), before `ThreadingServer(LISTEN, Handler)` binds, call `os.setsid()` inside `try/except OSError: pass` (it raises when the process already leads a process group, for example when run by hand in an interactive shell), with a short comment saying why: a shim is shared by many sessions, so terminal or process-group signals aimed at the session that started it must not reach it. No fork, no new import (`os` is already imported), argv and env unchanged.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k "directly_started_shim" -q` passes.
- `uv run pytest tests/unit/test_ccsession_tiers.py -q` and `uv run pytest tests/unit/test_ccsession_tag.py -q` pass except `test_shim_outlives_the_terminal_that_started_it`, which still fails until Task 4 (its failure reason recorded in ./artifacts/t3-tests.log).
```

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:64-70 (Task 4)

```markdown
In `src/superclaude/skills/ccsession-tag/ccsession` `setup_shim`, wrap the start statement at lines 801-804 (`GW_PROXY_UPSTREAM=... GW_PROXY_PORT=... CCSESSION_DIR=... nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &`) in a `( ... )` subshell so the subshell exits at once and the shim is no longer a descendant of the launching terminal (Orca kills a closed terminal's descendants; issue #341). Update the comment above it (lines 799-800) to say this, keep the env assignments and the redirect, keep bash 3.2 syntax. The listener and health waits that follow (lines 805-824) stay unchanged.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k "outlives_the_terminal or directly_started_shim or busy_shim_is_never_stopped" -q` passes (output in ./artifacts/t4-tests.log).
- `bash -n src/superclaude/skills/ccsession-tag/ccsession` succeeds.
- Live check against the changed source: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>` (starts a throwaway shim on a free port through the real ccsession and kills only processes it started) writes its output to `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/after.txt`, which shows `shim is a descendant of the terminal: False`, `stream finished: True`, the port still answering, and the surviving throwaway shim stopped by its pid; the scratch dir is removed afterwards.
- The live shims on ports 4013 and 4114 report the same pids before and after (`curl -s http://127.0.0.1:<port>/__ccsession_shim`), recorded in ./artifacts/t4-tests.log.
```

### src/superclaude/skills/ccsession-tag/ccsession:1031-1041 (landed subshell)

```bash
    # descendant of this terminal: closing a terminal (Orca kills its
    # descendants) must not stop a shim other sessions use (issue #341).
    (
      GW_PROXY_UPSTREAM="$ANTHROPIC_BASE_URL" \
        GW_PROXY_PORT="$CC_SHIM_PORT" \
        CCSESSION_DIR="$CCSESSION_DIR" \
        nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &
    )
    # Wait briefly for the port to come up.
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      [ -n "$(shim_listener_pid)" ] && break
```

### src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1009-1023 (landed setsid)

```python
if __name__ == "__main__":
    host, port = LISTEN
    # One shim serves every session on its port, so signals aimed at the
    # terminal session or process group that started it must not reach it
    # (issue #341). Run by hand with output on a terminal, it stays there so
    # Ctrl-C still stops it; setsid fails harmlessly for a group leader.
    if not sys.stderr.isatty():
        try:
            os.setsid()
        except OSError:
            pass
    if upstream_is_self():
        print(
            f"[proxy] ERROR: upstream {UPSTREAM} is this shim's own address; "
            "set GW_PROXY_UPSTREAM to the gateway",
```

### Makefile:166-174 (verify-sync)

```makefile
verify-sync:
	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
	@drift=0; \
	echo ""; \
	echo "=== Skills ==="; \
	for skill_dir in src/superclaude/skills/*/; do \
		name=$$(basename "$$skill_dir"); \
		case "$$name" in __*) continue;; esac; \
		if [ ! -d ".claude/skills/$$name" ]; then \
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 shim detach goal -> Tasks 3+4 | F1,F3 | covered | tasklist:52,64; ccsession:1033-1039; proxy:1014-1021 |
| INF-002 spec pointer -> Constraints | F1,F2 | covered | tasklist:19-23; remediation-source.md:9-17 |
