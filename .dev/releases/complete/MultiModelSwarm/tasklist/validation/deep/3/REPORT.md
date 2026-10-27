# Reflect Report — MultiModelSwarm Phase 3 (M3 Dispatch & Concurrency / Wave 1)

**Mode:** post  
**Depth:** deep / Tier 2-style ensemble review  
**Diff basis:** `git diff HEAD`, scoped to Phase 3 deliverables from `phase-3-tasklist.md`  
**Status:** **failed** — Phase 3 has verified regressions and cannot be promoted.

## Scope

Audited Phase 3 tasks T03.01–T03.22 only: run command wiring, Wave 1 dispatch, state/logging, stub + OpenAI-compatible transports, retry/timeout policy, Python-only concurrency, output confinement, no-cache/no-Anthropic guards, and Phase 3 validation tests. Files in the diff that belong only to later milestones (normalize/reduce/resume/TUI/skill migration/docs handoff) were treated as out-of-scope except where they broke Phase 3 validation.

## Verification run

Ran the Phase 3 targeted suite:

```text
uv run pytest tests/swarm/test_commands_run.py tests/swarm/test_dispatch.py tests/swarm/test_imm3_parallel.py tests/swarm/test_state.py tests/swarm/test_logging.py tests/swarm/test_openai_compat.py tests/swarm/test_stub_transport.py tests/swarm/test_swarm_run_inputs.py tests/swarm/test_retry_policy.py tests/swarm/test_dual_log_emission.py tests/swarm/test_imm6_atomic_write.py tests/swarm/test_concurrency_python_only.py tests/swarm/test_parallel_executor_routing.py tests/swarm/test_nfr002_atomicity.py tests/swarm/test_output_confinement.py tests/swarm/test_no_response_cache.py tests/swarm/test_no_anthropic_routing.py tests/swarm/test_t2_env_contract.py -q
```

Result: **208 passed, 2 failed**. Both failures are in `tests/swarm/test_concurrency_python_only.py` and are Phase 3 load-bearing because T03.14 requires that test to be green and the concurrency surface to remain Python-only.

Also ran a stub smoke command:

```text
uv run superclaude swarm run --lens bare-review --target <tmp>/target.txt --output <tmp>/out --transport stub
```

Observed output: `swarm run: dispatched job (mode=lens, workers=3, results=0)`, and the output directory contained only `manifest.json`.

## Deviation summary

| Class | Count | Meaning |
|---|---:|---|
| Regression | 2 | Contradicts Phase 3 acceptance or fails Phase 3 validation. |
| Drift | 4 | Implemented surface silently diverges from Phase 3 tasklist intent, but is not yet proven as a failing default path. |
| Necessary | 0 | No technically forced deviations were documented. |
| Authorized | 0 | No explicit Phase 3 scope-expansion authorization was found. |

## Findings

### R1 — `swarm run --transport stub` discards the selected transport and dispatches zero workers

**Class:** Regression  
**Tasks:** T03.01, T03.08, T03.10, T03.22  
**Evidence:**

- T03.01 requires `swarm run` to invoke Wave 0→1 against the deterministic-fixture transport in a smoke test: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:31-39`.
- T03.22 requires `swarm run` to execute Wave 0→1 end-to-end against stub transport and the Phase 3 surface to pass: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:776-783`.
- The command exposes `--transport` and documents `stub` as the deterministic in-process transport: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/commands.py:1029-1039`.
- The command then always calls `dispatch_wave1(preflight_result, transport=None, logger=logger)`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/commands.py:1264-1266`.
- `dispatch_wave1` explicitly returns `[]` when `transport is None`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/dispatch.py:386-392`.

**Impact:** The CLI appears to succeed but performs no worker dispatch. The stub smoke path prints `workers=3, results=0` and produces only `manifest.json`; it produces no worker outputs and no dispatch log entries. This directly violates the Phase 3 end-to-end stub dispatch criterion.

**Verifier:** rerun the smoke command above and assert `results == workers` plus worker artifacts/log events exist.

**Recommended fix:** construct the resolved `Transport` from `preflight_result.manifest.preflight.transport_kind` / resolved `JobSpec.transport.kind` before calling `dispatch_wave1`; pass a `StubTransport` for `--transport stub` and an `OpenAICompatTransport` for `openai_compat`.

### R2 — Phase 3 Python-only concurrency test fails because later tmux subprocess code is in the Phase 3 scan surface

**Class:** Regression  
**Task:** T03.14 / INV-002  
**Evidence:**

- T03.14 requires no shell dispatch path and `tests/swarm/test_concurrency_python_only.py` green: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:492-500`.
- The test flags module-level `subprocess` / `shlex` imports as INV-002 violations: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_concurrency_python_only.py:221-239`.
- The test flags actual `subprocess` calls as shell-dispatch violations: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_concurrency_python_only.py:242-258`.
- `tmux.py` imports `shlex` and `subprocess`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/tmux.py:64-68`.
- `tmux.py` calls `subprocess.run` for tmux lifecycle commands: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/tmux.py:128-138` and `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/tmux.py:198-201`.
- `commands.py` imports subprocess in detached-mode code: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/commands.py:879-889`.

**Impact:** The targeted Phase 3 validation suite fails with 2 failures. Even if the tmux code is later-milestone/M7 functionality, it is present in the current diff and breaks the Phase 3 guard as written.

**Verifier:** `uv run pytest tests/swarm/test_concurrency_python_only.py -q`.

**Recommended fix:** either narrow the INV-002 test to the M3 dispatch/transport path while explicitly excluding M7 tmux lifecycle code, or defer adding tmux subprocess code until after the Phase 3 gate. The current state cannot be called Phase 3-clean.

### D1 — Preflight constructs `SwarmState` but the run path does not persist `.swarm-state.json`

**Class:** Drift  
**Tasks:** T03.03, T03.16, T03.22  
**Evidence:**

- T03.03 requires state transitions through tmp + `os.replace`: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:100-118`.
- `run_preflight` constructs `SwarmState(state="preflight_ok")`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/preflight.py:1790-1797`.
- In the output-dir branch, `run_preflight` writes only `manifest.json` via `write_manifest(...)`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/preflight.py:1799-1802`.
- The run command proceeds directly to dispatch without calling `write_state`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/commands.py:1264-1266`.

**Impact:** A successful run has no durable `.swarm-state.json` transition despite M3 requiring state observability/atomicity. The smoke command confirmed that the output directory contained only `manifest.json`.

**Verifier:** after a stub run, `test -f <out>/.swarm-state.json` should pass; currently it fails.

**Recommended fix:** persist the preflight state immediately after manifest emit and transition to `dispatching` / terminal states using `write_state(confined_path, state)` in the run path.

### D2 — Retry policy can retry 4xx and timeout outcomes when flags are set, despite the Phase 3 matrix saying never

**Class:** Drift  
**Task:** T03.09  
**Evidence:**

- T03.09 states the matrix as `4xx→0 retries` and `timeout/network→0`: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:311-330`.
- `retry_policy` sets `should_retry = True` for 4xx when `retry.on_4xx` is true: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/dispatch.py:250-256`.
- `retry_policy` sets `should_retry = True` for timeout when `retry.on_timeout` is true: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/dispatch.py:259-260`.

**Impact:** Defaults may still encode the intended matrix, but the production policy is no longer the exact Phase 3 policy. Tests currently assert that the escape flags are honored, so the test suite blesses behavior that the Phase 3 tasklist says should never happen.

**Verifier:** `uv run pytest tests/swarm/test_retry_policy.py::test_retry_policy_honours_on_4xx_flag tests/swarm/test_retry_policy.py::test_retry_policy_honours_on_timeout_flag -q` currently passes, demonstrating the drift.

**Recommended fix:** either remove 4xx/timeout retry behavior from Phase 3 or update the tasklist/roadmap to explicitly authorize configurable retry overrides and document their safe defaults.

### D3 — OpenAI-compatible network exceptions bypass transport-side result stamping and lose model identity

**Class:** Drift  
**Tasks:** T03.02, T03.05, T03.09  
**Evidence:**

- T03.02 requires every worker outcome to record populated WorkerResult fields, including model/status/http/attempts/elapsed: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:59-80`.
- T03.09 requires outcome recording regardless of branch: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:322-330`.
- `OpenAICompatTransport.send` catches only `httpx.TimeoutException`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/transports/openai_compat.py:322-337`.
- The transport-side `_build_result` is the path that stamps `model_id` and `model_label`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/transports/openai_compat.py:366-383`.
- Dispatch catches generic exceptions and returns a synthetic `WorkerResult(status="proxy_error")` without model identity: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/dispatch.py:180-187`.

**Impact:** DNS/connectivity failures become `proxy_error` results but lose the configured model label, weakening operator triage and violating the “every outcome fields populated” intent.

**Verifier:** simulate an `httpx.RequestError` from the transport and assert the returned `WorkerResult.model_id` / `model_label` are preserved.

**Recommended fix:** catch `httpx.RequestError` in `OpenAICompatTransport.send` and return `_build_result(status="proxy_error", http_code=None, ...)`, or make dispatch’s exception fallback preserve worker slot model metadata.

### D4 — Logger confinement support is not used by the production run call site

**Class:** Drift  
**Tasks:** T03.10, T03.17  
**Evidence:**

- T03.10 requires execution logs post-dispatch: `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-3-tasklist.md:358-366`.
- `Logger` only applies `confine_path` when `output_dir is not None`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/logging_.py:101-115`.
- The run command constructs `Logger` with `jsonl_path` and `md_path` but no `output_dir`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/commands.py:1259-1263`.

**Impact:** In the current path, log paths are derived from `manifest_path.parent`, so this is not an immediate path escape. It is still a Phase 3 guard drift: the explicit confinement guard exists but is bypassed by the production caller.

**Verifier:** inspect `Logger(...)` construction in `run_cmd` and assert `output_dir=manifest_dir` (or the resolved output root) is passed.

**Recommended fix:** pass `output_dir=manifest_dir` to `Logger` at construction.

### D5 — Output-confinement test only checks that modules contain the string `confine_path`

**Class:** Drift  
**Task:** T03.17  
**Evidence:**

- `tests/swarm/test_output_confinement.py` defines writer modules, then `test_writers_invoke_confine_path` reads each module and asserts only that the substring `confine_path` appears: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_output_confinement.py:280-301`.

**Impact:** A writer can leave `confine_path` in a docstring/import/dead helper while no longer invoking it at the write call site. That weakens T03.17’s “all writer call sites import and call confine_path” gate.

**Verifier:** mutate a writer to stop calling `confine_path` while leaving a docstring mention; this test would still pass.

**Recommended fix:** replace the substring check with an AST-level or call-site-specific assertion for each writer function (`write_state`, `write_manifest`, `emit_env_missing_contract`, `Logger.__init__`).

## High-confidence passes

- No raw `ThreadPoolExecutor(` instantiation was found under `src/superclaude/cli/swarm/`; dispatch creates `ParallelExecutor(max_workers=workers_requested)`: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/dispatch.py:403-406`.
- The state writer itself uses tmp + `os.replace`; the integration gap is that the run path does not persist state.
- The OpenAI-compatible transport uses `httpx` for the HTTP call: `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/transports/openai_compat.py:322-329`.

## Promotion verdict

**Do not promote Phase 3.** Gate failures:

1. `status_success`: fail — regression findings present.
2. `tasklist_completion_pct_1_0`: fail — T03.01/T03.14/T03.22 are not verified complete.
3. `no_drift_no_regression`: fail — 2 regressions + 4 drifts.
4. `no_user_decision_pending`: pass — no human authorization ambiguity is needed to classify these findings.

## Recommended next move

Fix R1 and R2 first, then rerun the Phase 3 targeted suite and stub smoke. Paste-ready command after fixes:

```text
uv run pytest tests/swarm/test_commands_run.py tests/swarm/test_dispatch.py tests/swarm/test_imm3_parallel.py tests/swarm/test_state.py tests/swarm/test_logging.py tests/swarm/test_openai_compat.py tests/swarm/test_stub_transport.py tests/swarm/test_swarm_run_inputs.py tests/swarm/test_retry_policy.py tests/swarm/test_dual_log_emission.py tests/swarm/test_imm6_atomic_write.py tests/swarm/test_concurrency_python_only.py tests/swarm/test_parallel_executor_routing.py tests/swarm/test_nfr002_atomicity.py tests/swarm/test_output_confinement.py tests/swarm/test_no_response_cache.py tests/swarm/test_no_anthropic_routing.py tests/swarm/test_t2_env_contract.py -q
```
