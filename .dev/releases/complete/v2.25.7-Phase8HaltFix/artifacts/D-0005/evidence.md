# D-0005: End-to-End env_vars Propagation Trace

**Task:** T01.04 (Milestone M1.3)
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Propagation Chain Trace

```
execute_sprint(config)                                    # executor.py:490
  │
  │  [FUTURE - Phase 2] setup_isolation(config)
  │    → IsolationLayers.env_vars = {
  │        "CLAUDE_WORK_DIR": str(release_dir),
  │        "GIT_CEILING_DIRECTORIES": str(release_dir),
  │        "CLAUDE_PLUGIN_DIR": str(plugin_dir),
  │        "CLAUDE_SETTINGS_DIR": str(settings_dir),
  │      }
  │
  ├─ ClaudeProcess(config, phase, env_vars=isolation.env_vars)
  │    sprint/process.py:ClaudeProcess.__init__()         # process.py:97
  │    │
  │    ├─ self._extra_env_vars = env_vars                 # stored on sprint instance
  │    │
  │    └─ super().__init__(                               # → pipeline/process.py
  │           ...,
  │           env_vars=env_vars,                          # forwarded to base
  │       )
  │         pipeline/process.py:ClaudeProcess.__init__()  # process.py:37
  │         │
  │         └─ self._extra_env_vars = env_vars            # stored on base instance
  │
  └─ proc_manager.start()                                 # pipeline/process.py:102
       │
       └─ self.build_env(env_vars=self._extra_env_vars)   # process.py:113
            │
            ├─ env = os.environ.copy()
            ├─ env.pop("CLAUDECODE", None)
            ├─ env.pop("CLAUDE_CODE_ENTRYPOINT", None)
            └─ if env_vars: env.update(env_vars)          # CLAUDE_WORK_DIR injected
            │
            └─ subprocess.Popen(cmd, env=env)             # subprocess receives CLAUDE_WORK_DIR
```

---

## Handoff Points Verified

| Handoff | From | To | Value Preserved? |
|---------|------|----|-----------------|
| 1 | `execute_sprint()` arg | `sprint/ClaudeProcess.__init__(env_vars=...)` | Yes — keyword arg |
| 2 | `sprint/__init__` param | `self._extra_env_vars` attribute | Yes — direct assignment |
| 3 | `sprint/__init__` param | `super().__init__(env_vars=env_vars)` | Yes — forwarded |
| 4 | `pipeline/__init__` param | `self._extra_env_vars` attribute | Yes — direct assignment |
| 5 | `self._extra_env_vars` | `build_env(env_vars=self._extra_env_vars)` | Yes — passed from start() |
| 6 | `build_env()` param | `env.update(env_vars)` | Yes — override merge |
| 7 | `env` dict | `subprocess.Popen(env=env)` | Yes — subprocess env |

No loss points in the chain.

---

## None Passthrough Verified

When `env_vars=None` (current default, no caller passes it yet):
- `self._extra_env_vars = None` in both `__init__` levels
- `build_env(env_vars=None)` called from `start()`
- `if env_vars:` evaluates False → `env.update()` skipped
- Returns identical dict to prior implementation

**Prior behavior preserved for all existing callers.**

---

## Call Site Audit: No Keyword-Only Violations

### sprint/ClaudeProcess callers
| File | Line | Call | Breaks? |
|------|------|------|---------|
| executor.py | 542 | `ClaudeProcess(config, phase)` | No — env_vars defaults None |

### pipeline/ClaudeProcess callers
| File | Line | Call | Breaks? |
|------|------|------|---------|
| roadmap/executor.py | 202 | `ClaudeProcess(prompt=..., ...)` | No — env_vars defaults None |
| roadmap/validate_executor.py | 117 | `ClaudeProcess(prompt=..., ...)` | No — env_vars defaults None |
| roadmap/remediate_executor.py | 192 | `ClaudeProcess(prompt=..., ...)` | No — env_vars defaults None |
| tasklist/executor.py | 129 | `ClaudeProcess(prompt=..., ...)` | No — env_vars defaults None |

All existing callers use keyword arguments already; `env_vars` with `None` default causes no breakage.

---

## Test Results

```
uv run pytest tests/sprint/ -v --tb=short
629 passed in 37.18s

uv run pytest tests/ --ignore=tests/cli_portify --tb=short
2705 passed, 1 pre-existing failure, 92 skipped
```

`cli_portify` errors are pre-existing `ModuleNotFoundError` collection errors unrelated to Phase 1 changes.

---

## Milestone M1.3 Status: SATISFIED

All handoff points verified. No gaps in propagation. Existing call sites unaffected. Tests pass.
