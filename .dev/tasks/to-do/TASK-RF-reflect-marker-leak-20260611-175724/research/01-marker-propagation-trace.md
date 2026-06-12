# Research: Marker Propagation Trace

## Topic type
Integration Points — marker-propagation trace

## Scope
- `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py`
- `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/runner.py`
- `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/pipeline/process.py`

## Status
Complete

## Date
2026-06-11

## 1. `commands.py`: marker constant and recursion-breaker guard

Evidence from `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py`:

- The wrapper marker env-var constant is `_WRAPPER_MARKER_ENV = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` at line 44.
- The group callback documents that the marker is exported into a child `claude --print` subprocess and that a child terminal reflect gate should immediately exit before any audit at lines 38-43.
- The load-bearing placement is the `reflect_group()` Click group callback: lines 62-68 state it runs during parsing before the `run` subcommand path validation and that truthiness is exactly string `"1"`.
- Exact guard predicate at line 69:

```python
if os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1":
```

- On match, it emits `"reflect-wrapper recursion breaker: nested gate suppressed"` and exits 0 at lines 70-73.

Conclusion: this guard is correct and must stay. The file itself states the guard is required to break recursion before audit and before Click path validation; that same predicate is the one nested gates and leaked verification tests trip when the environment contains `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`.

## 2. `runner.py`: marker constant, export sites, and re-verification loop

Evidence from `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/runner.py`:

- The runner marker constant is `_WRAPPER_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` at line 53.
- Lines 48-52 document the intended semantics: export the marker as `"1"` into every child the wrapper spawns inside the fix subtree, including audit and auto-run `/task`, so nested `superclaude reflect run` terminal gates self-suppress.

Export site A — reflect-audit `ClaudeProcess` in `_audit_once()`:

```python
proc = ClaudeProcess(
    prompt=self._build_prompt(),
    output_file=config.output_dir / "reflect-stdout.json",
    error_file=config.output_dir / "reflect-stderr.log",
    model=config.model,
    timeout_seconds=config.timeout_seconds,
    max_turns=config.max_turns,  # G1: explicit, never the primitive's 100.
    output_format="stream-json",
    # Contract 3.1: marker exported into the audit child too. The audit is
    # /sc:reflect (not `superclaude reflect run`), so it does NOT self-suppress;
    # build_env() overlays this on the full inherited env (process.py:97-112).
    env_vars={_WRAPPER_MARKER: "1"},
)
```

- This export appears at lines 405-416; the actual marker injection is line 416.
- Lines 413-415 explicitly say the audit child receives the marker and should not self-suppress because it is `/sc:reflect`, not `superclaude reflect run`.

Export site B — corrective-MDTM `/task` `ClaudeProcess` in `_apply_remediation()`:

```python
proc = ClaudeProcess(
    prompt=f"/task {remediation_task_path}",
    output_file=config.output_dir / f"fix-{iteration}-stdout.json",
    error_file=config.output_dir / f"fix-{iteration}-stderr.log",
    model=config.model,
    timeout_seconds=config.timeout_seconds,
    max_turns=config.max_turns,
    output_format="stream-json",
    env_vars={_WRAPPER_MARKER: "1"},
)
```

- This export appears at lines 440-448; the actual marker injection is line 448.
- Lines 433-435 state the corrective tasklist's own terminal `superclaude reflect run` gate is expected to self-suppress because the marker is exported.

Re-verification path:

- The bounded loop comment at lines 531-533 describes `audit -> classify -> apply -> re-verify`.
- The loop re-verifies by calling `result = self._audit_once()` at line 537.
- There is no pytest invocation in this re-verification loop in the inspected lines. The wrapper's Python runner re-runs the reflect audit subprocess; therefore the §6.1 step 5.5 verification pytest is inside the reflect skill subprocess launched by `_audit_once()`, not directly in `runner.py`.

## 3. `pipeline/process.py`: `ClaudeProcess.build_env()` env propagation

Evidence from `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/pipeline/process.py`:

- `ClaudeProcess.__init__` accepts `env_vars` at line 100 and stores it as `self._extra_env_vars` at line 115.
- `build_env()` is defined at line 145.
- Lines 151-153 document that provided `env_vars` are merged with override semantics after `os.environ.copy()`.
- Exact merge logic at lines 155-160:

```python
env = os.environ.copy()
env.pop("CLAUDECODE", None)
env.pop("CLAUDE_CODE_ENTRYPOINT", None)
if env_vars:
    env.update(env_vars)
return env
```

- `start()` passes that environment to `subprocess.Popen` through `popen_kwargs`: line 187 is `"env": self.build_env(env_vars=self._extra_env_vars),`.

Conclusion: a `ClaudeProcess` child launched with `env_vars={_WRAPPER_MARKER: "1"}` receives the full parent `os.environ` minus only `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`, plus `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`. There is no marker-specific scrub in `build_env()` at lines 155-160. Therefore the reflect audit subprocess environment contains the marker, and any verification subprocess it launches without an explicit env scrub inherits that marker from the reflect audit process environment by default.

## 4. Precise leak chain

1. Constant definition: `commands.py` names `_WRAPPER_MARKER_ENV = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` at line 44; `runner.py` names `_WRAPPER_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` at line 53.
2. Export site: `runner.py` `_audit_once()` constructs the reflect-audit `ClaudeProcess` at lines 405-417 with `env_vars={_WRAPPER_MARKER: "1"}` at line 416.
3. Env construction: `pipeline/process.py` `ClaudeProcess.build_env()` starts from `os.environ.copy()` at line 155, removes only `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` at lines 156-157, overlays caller env vars at lines 158-159, and returns the result at line 160.
4. Process launch: `pipeline/process.py` `start()` passes `"env": self.build_env(env_vars=self._extra_env_vars)` to the child process at line 187.
5. Reflect skill subprocess state: the launched reflect-audit child therefore receives `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` because `_audit_once()` supplied it and `build_env()` overlays it.
6. Verification pytest inheritance: the §6.1 step 5.5 pytest is not launched by `runner.py`; the wrapper loop only calls `_audit_once()` again at `runner.py` line 537. Therefore the verification pytest is a grandchild of the marked reflect-audit subprocess. If that verification launcher does not scrub `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, it inherits the marker from the reflect-audit environment.
7. Guard trip: when the verification pytest exercises the reflect CLI, `commands.py` group callback evaluates `os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1"` at line 69 and exits 0 at lines 70-73 before normal command behavior. That is the false self-suppression path that makes reflect-CLI tests such as `test_cli_smoke` and `test_promote_plumbing` observe the recursion-breaker instead of the expected CLI behavior.

## 5. Critical conclusion for corrective task targeting

Do not remove the marker from `runner.py` or the guard from `commands.py`.

Why:

- `commands.py` lines 38-43 define the marker/guard as the recursion breaker for child terminal reflect gates, and lines 62-68 explain why the guard must run in the group callback before subcommand parsing.
- `runner.py` lines 48-52 define the marker's intended contract: export `"1"` into children in the fix subtree so nested `superclaude reflect run` gates self-suppress.
- `runner.py` lines 433-435 specifically require the corrective `/task` child to carry the marker so the corrective tasklist's own terminal reflect gate self-suppresses.

Removing the marker export or weakening the `commands.py` guard would break nested-gate suppression. The fix should instead strip `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` only for the reflect skill's §6.1 step 5.5 verification subprocess. That insertion point is not in the three Python files inspected here; it belongs to the reflect skill verification surface covered by R2.

## Summary

The leak is caused by intentional marker propagation from `runner.py` into the reflect-audit `ClaudeProcess`, combined with `ClaudeProcess.build_env()` preserving the parent environment and overlaying `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`. The wrapper's fix loop re-verifies by re-running `_audit_once()`, so the pytest verification is inside the marked reflect skill subprocess. If the reflect skill launches pytest without scrubbing the marker, the pytest process inherits it; reflect CLI tests then hit the correct `commands.py` recursion-breaker guard and exit through the nested-gate suppression path. The corrective task should target the verification subprocess env scrub, not the wrapper marker contract.
