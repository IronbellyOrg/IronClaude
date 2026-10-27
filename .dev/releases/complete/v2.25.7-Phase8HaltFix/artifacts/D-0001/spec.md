# OQ-006 Resolution: @ Reference Resolution Mechanism

**Status:** RESOLVED
**Decision Date:** 2026-03-16
**Phase:** Phase 1 Gate (M1.0)

---

## Question

OQ-006: Does `CLAUDE_WORK_DIR` env var or subprocess `cwd` control `@` reference resolution scope in Claude subprocess?

---

## Resolution: CLAUDE_WORK_DIR (env var) is the canonical mechanism

### Evidence

1. `IsolationLayers.env_vars` (executor.py:115-123) is already designed to return `CLAUDE_WORK_DIR` as
   the scope-control variable, alongside `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`.

2. `setup_isolation()` (executor.py:140-172) constructs an `IsolationLayers` object with
   `scoped_work_dir=config.release_dir` — this dir is the intended isolation scope.

3. The subprocess `cwd` is NOT set explicitly in `ClaudeProcess.start()` (pipeline/process.py:101-128);
   it inherits the parent process cwd. Therefore `cwd` is NOT a controlled isolation mechanism.

4. `CLAUDE_WORK_DIR` is already present in the `IsolationLayers.env_vars` property — it is the
   intended and designed mechanism. Its value is `str(self.scoped_work_dir)` = the release dir path.

### Current Gap

`setup_isolation()` is called nowhere in `execute_sprint()`. The `IsolationLayers` object (and its
`env_vars` dict) is never constructed or passed to `ClaudeProcess`. Phase 2 must wire this up.

### Explicit Defaults

| Mechanism | Decision |
|-----------|----------|
| `CLAUDE_WORK_DIR` env var | **PRIMARY** — controls `@` resolution scope |
| subprocess `cwd` | NOT used for isolation; inherits parent cwd |
| Fallback | None needed — env var is the sole mechanism |

### Fallback Determination

No fallback to `cwd` is required. The env var mechanism is well-defined and already structured in
`IsolationLayers`. Phase 2 will wire `setup_isolation()` into `execute_sprint()` and pass
`layers.env_vars` through `ClaudeProcess` → `build_env()` → subprocess environment.

---

## Impact on Phase 2

Phase 2 can proceed using the env var path. No timeline re-estimation required.
The propagation chain modifications (T01.02, T01.03) will enable env vars to flow from
`execute_sprint()` → `ClaudeProcess(env_vars=layers.env_vars)` → `build_env(env_vars=...)` →
`env.update(env_vars)` → subprocess env.

---

## Trace Path (for Phase 2 implementation)

```
execute_sprint()
  isolation = setup_isolation(config)      # IsolationLayers with env_vars dict
  ClaudeProcess(config, phase,
    env_vars=isolation.env_vars)           # T01.02: new keyword-only param
    → super().__init__(...,
        env_vars=self._extra_env_vars)     # forwarded to pipeline ClaudeProcess
      → self._extra_env_vars stored
  proc_manager.start()
    → self.build_env(env_vars=self._extra_env_vars)   # T01.03: new param
      → env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env.pop("CLAUDE_CODE_ENTRYPOINT", None)
        if env_vars: env.update(env_vars)  # CLAUDE_WORK_DIR injected here
        return env
    → subprocess.Popen(..., env=env)       # subprocess receives CLAUDE_WORK_DIR
```
