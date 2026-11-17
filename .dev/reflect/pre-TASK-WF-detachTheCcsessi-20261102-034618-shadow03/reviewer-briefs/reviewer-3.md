# Reviewer 3 brief (persona: refactorer)

Mode UC-1 (pre-execution). You are read-only: return findings, run nothing, edit nothing.
Persona: refactorer. Audit the plan for defects that would make a task fail, an acceptance criterion unmeetable, or a step contradict a constraint. The package was already executed and archived (progress.md FINAL: pass); the fix is in HEAD. Judge the PLAN as a plan, using HEAD only to verify the plan's anchors and claims.

## T1 card excerpt

## Risk surface

Safety constraints (never signal ports 4013/4114, never edit ~/.claude|~/.ccsession, no install/update) are carried verbatim into Constraints and were respected by the landed run (t4-tests.log records pid equality; live-pids-before.txt matches). Bash-3.2, no-new-imports, argv/env-unchanged restrictions are restated in Tasks 3-4 and hold in HEAD.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.
## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:22Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### src/superclaude/skills/ccsession-tag/ccsession:962-975 (setup_shim head)

```bash
setup_shim() {
  # Route this session through the local model-alias shim: start it if it
  # isn't already listening, then point ANTHROPIC_BASE_URL at it and enable
  # gateway model discovery. The shim forwards to the ccsession.env base URL
  # (via GW_PROXY_UPSTREAM), so env stays the single source of truth.
  if [ ! -f "$CC_SHIM_SCRIPT" ]; then
    echo "[ccsession] ERROR: shim script not found: $CC_SHIM_SCRIPT" >&2
    exit 1
  fi
  # A launch from inside a shim session inherits that session's shim URL as
  # ANTHROPIC_BASE_URL. The session also exported the gateway it forwards to
  # (CCSESSION_GATEWAY_URL, below), so forward there instead.
  if [ -n "${CCSESSION_GATEWAY_URL:-}" ] && [ -n "${CCSESSION_SHIM_URL:-}" ] \
    && [ "${ANTHROPIC_BASE_URL%/}" = "${CCSESSION_SHIM_URL%/}" ]; then
```

### src/superclaude/skills/ccsession-tag/ccsession:1031-1052 (subshell + waits)

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
      sleep 0.3
    done
    if [ -z "$(shim_listener_pid)" ]; then
      echo "[ccsession] ERROR: shim failed to start (try: python3 $CC_SHIM_SCRIPT)" >&2
      exit 1
    fi
    # Another launch may have won the port at the same moment: attach only to
    # a shim with this session's settings and code.
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      health_status=$(shim_health_status)
      [ "$health_status" = match ] && break
```

### src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1009-1023 (setsid)

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

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:19-23 (constraints)

```markdown
- Scope is exactly the four files named in the source: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md`. Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341).
- Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them); never edit anything under `~/.claude`, `~/.ccsession` or the running config; never run `superclaude install`, `superclaude update`, `./update.sh` or `install.sh`.
- Doc restrictions (remediation-source.md AC6; doc-context.md in the troubleshoot directory): the shim's argv keeps the script path (ccsession uses `pgrep -f -- "$CC_SHIM_SCRIPT"` at ccsession:722 and users stop shims with `pkill -f local-gateway-alias-proxy.py`); the shim inherits the launching env; no `setsid` binary (macOS has none) and only Python standard library; bash 3.2 syntax; logging stays opt-in; ccsession never stops a running shim.
- Tests: run only named test files and tests that read the edited files; never the full suite and never `tests/cli/eval/` as a directory. Use `uv run` for Python.
- Every throwaway shim or test process started while working is stopped by its exact pid; no temp files left behind.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 -> Tasks 3+4 structure | - | covered | ccsession:1033-1039; proxy:1014-1021 |
