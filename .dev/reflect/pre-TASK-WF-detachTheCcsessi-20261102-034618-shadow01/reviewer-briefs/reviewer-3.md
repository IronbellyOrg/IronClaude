# Reviewer 3 brief (persona: refactorer)

Mode UC-1 (pre-execution). You are read-only: return findings, run nothing, edit nothing.
Persona: refactorer. Audit task ordering, dependencies, scope boundaries and structural risks.

## T1 card excerpt

## Structural / tech-debt section (refactorer slice)

- Dependencies are linear (T1, T2, T3, T4, T5). Task 2 does not need Task 1's output; the chain is only an ordering preference.
- Task 3 specifies `try: os.setsid() except OSError: pass` for every start. The landed code adds an `if not sys.stderr.isatty()` guard (local-gateway-alias-proxy.py:1015-1019) that the plan never mentions. That is a post-execution deviation, not a plan defect, and is out of scope for this UC-1 pass.

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

### tests/unit/test_ccsession_tiers.py:842-882

```python
@pytest.fixture
def shim(tmp_path: Path):
    """Start the real shim against a stand-in gateway in tier mode."""
    gateway = StandInGateway()
    port = _free_port()
    procs = []

    def start(defaults: str = TIER_BLOCK, **extra: str):
        env = os.environ.copy()
        env.update(
            {
                "GW_PROXY_UPSTREAM": gateway.url,
                "GW_PROXY_PORT": str(port),
                "CCSESSION_DIR": str(SKILL_DIR),
                "AIDEV_AI_DEFAULTS_PATH": str(_defaults(tmp_path, defaults)),
                "CCSESSION_COOLDOWN_SECONDS": "3600",
                "CCSESSION_FIRST_BYTE_TIMEOUT": "2",
            }
        )
        env.update(extra)
        proc = subprocess.Popen(
            [sys.executable, str(SKILL_DIR / "local-gateway-alias-proxy.py")],
            env=env,
            stderr=open(tmp_path / "shim.log", "w"),
        )
        procs.append(proc)
        for _ in range(50):
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/__ccsession_shim", timeout=1
                )
                break
            except OSError:
                time.sleep(0.1)
        return f"http://127.0.0.1:{port}"

    yield gateway, start, tmp_path / "shim.log"
    for proc in procs:
        proc.terminate()
        proc.wait(timeout=5)
    gateway.close()
```

### src/superclaude/skills/ccsession-tag/ccsession:930-933

```bash
  # reported as "other" so it is never killed.
  if python3 -c 'import socket, sys; s = socket.socket(); s.settimeout(0.3); sys.exit(s.connect_ex(("127.0.0.1", int(sys.argv[1]))))' "$CC_SHIM_PORT" 2>/dev/null; then
    pgrep -f -- "$CC_SHIM_SCRIPT" 2>/dev/null | head -n 1 | grep . || echo other
  fi
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Task dependency chain T1 to T5 | - | linear; T2 does not need T1 output | tasklist:38,50,62,76 |
| Task 2 test relies on the `shim` fixture | - | covered | test_ccsession_tiers.py:843-882 |
| Task 3 setsid guard | - | plan unconditional; HEAD adds isatty guard (post-exec) | local-gateway-alias-proxy.py:1015-1019 |
