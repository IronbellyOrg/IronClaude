# D-0008: Isolation Path Passed to Subprocess via CLAUDE_WORK_DIR

**Task:** T02.03 (Milestone M2.4)
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Mechanism Selected

Per OQ-006 resolution (D-0001): **PRIMARY** — `CLAUDE_WORK_DIR` env var controls `@` reference resolution scope.

The `cwd` mechanism was NOT used (it is not a controlled isolation mechanism per D-0001).

---

## Implementation

`env_vars={"CLAUDE_WORK_DIR": str(isolation_dir)}` passed to `ClaudeProcess` constructor.

**Location:** `executor.py` lines 550-554

```python
# Launch claude with isolation env vars (CLAUDE_WORK_DIR → isolation_dir)
_phase_env_vars = {
    "CLAUDE_WORK_DIR": str(isolation_dir),
}
proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
```

---

## Propagation Chain (per D-0005 trace)

```
execute_sprint()
  _phase_env_vars = {"CLAUDE_WORK_DIR": str(isolation_dir)}
  ClaudeProcess(config, phase, env_vars=_phase_env_vars)
    sprint/process.py: self._extra_env_vars = env_vars
    super().__init__(..., env_vars=env_vars)
      pipeline/process.py: self._extra_env_vars = env_vars
  proc_manager.start()
    → build_env(env_vars=self._extra_env_vars)
      → env.update(env_vars)  # CLAUDE_WORK_DIR injected
    → subprocess.Popen(cmd, env=env)  # subprocess receives CLAUDE_WORK_DIR=isolation_dir
```

---

## Acceptance Criteria Verification

| Criterion | Status |
|-----------|--------|
| Mechanism: `env_vars={"CLAUDE_WORK_DIR": str(isolation_dir)}` | PASS |
| Matches OQ-006 resolution in D-0001 | PASS — env var is primary mechanism |
| `tasklist-index.md` mechanically unreachable from subprocess | PASS — isolation_dir contains only phase file |
| `uv run pytest tests/sprint/ -v --tb=short` exits 0 | PASS — 629 passed |

---

## Test Results

```
uv run pytest tests/sprint/ -v --tb=short
629 passed in 37.27s
```

---

## Milestone M2.4: SATISFIED
