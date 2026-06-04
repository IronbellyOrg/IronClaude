# Phase 3 -- Dispatch & Concurrency (Wave 1)

**Goal:** Build Wave 1 — code-enforced true-parallel `ThreadPoolExecutor` dispatch routed through `superclaude.execution.parallel.ParallelExecutor`, the httpx `openai_compat` and deterministic-fixture transports, per-worker 180s timeout with 5xx-once retry policy, atomic `.swarm-state.json` transitions, and dual-format JSONL+Markdown event logging with lock-coordinated appends. Exit when N stub workers overlap in wall-clock (IMM-3 verified), retry matrix matches §7 policy exactly, all writes are atomic and confined to `--output`, and `swarm run` executes Wave 0→1 end-to-end against the deterministic-fixture transport.

### T03.01 -- Build `commands` module wiring run through preflight→dispatch

| Field | Value |
|---|---|
| Roadmap | R-060 (COMP-002) |
| Deliverables | D-0050 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit, auggie (codebase-retrieval), context7 (Click) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_commands_run.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/commands.py` with Click subcommand wiring for `run`.
2. `swarm run` exercises Wave 0 (preflight) then Wave 1 (dispatch) end-to-end.

**Steps:**
1. [PLANNING] Auggie-retrieve sprint commands.py as the structural template.
2. [PLANNING] Identify the Click decorators and option set required for `run` (spec file, stdin, `--lens`).
3. [EXECUTION] Create `commands.py` with `@swarm_group.command("run")` invoking preflight→dispatch.
4. [EXECUTION] Wire return-contract emission stub (to be completed in M5).
5. [VERIFICATION] Invoke `uv run superclaude swarm run --help` and check option set.
6. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- `src/superclaude/cli/swarm/commands.py` defines `run_cmd` exported through `swarm_group`.
- `swarm run` invokes Wave 0→1 against the deterministic-fixture transport in a smoke test.
- All run-spec input modes (spec file, stdin, `--lens`) resolve to the same internal `JobSpec`.
- `tests/swarm/test_commands_run.py` asserts subcommand registration and dispatch wiring.

**Validation:**
- `uv run pytest tests/swarm/test_commands_run.py -v` passes.
- `uv run superclaude swarm run --help` exits 0 with documented flags.

**Dependencies:** T02.02 (preflight), T03.02 (dispatch). **Rollback:** remove `commands.py` and the `swarm_group.add_command(run_cmd)` line.
**Notes:** This module grows in M7 with status/logs/attach/kill/scaffold.

### T03.02 -- Build `dispatch` module (Wave 1) with ParallelExecutor + per-worker outcome recording

| Field | Value |
|---|---|
| Roadmap | R-061 (COMP-007) |
| Deliverables | D-0051 |
| Effort | L |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie (codebase-retrieval), context7 (httpx, ThreadPoolExecutor), serena |
| Sub-Agent | tech-research (concurrency design review) |
| Verification | tests: `uv run pytest tests/swarm/test_dispatch.py tests/swarm/test_imm3_parallel.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/dispatch.py` with `dispatch_wave1(job_spec, transport, parallel_executor) -> list[WorkerResult]`.
2. Per-worker outcome recording (success / partial / failed / parse_error) into WorkerResult.

**Steps:**
1. [PLANNING] Read `src/superclaude/execution/parallel.py::ParallelExecutor` interface via serena.
2. [PLANNING] Auggie-retrieve current ThreadPoolExecutor invocation patterns and lock conventions.
3. [EXECUTION] Implement `dispatch_wave1` routing N workers via `ParallelExecutor`; never instantiate ThreadPoolExecutor directly (AC-004).
4. [EXECUTION] Capture WorkerResult per future: index, model_id, status, http_code, attempts, elapsed_ms.
5. [EXECUTION] Add docstring documenting threading semantics + ParallelExecutor contract.
6. [VERIFICATION] Run stub-transport parallelism test asserting overlap.
7. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- N workers dispatched concurrently against the stub transport (overlap window ≥ 80% of max(elapsed)).
- Every worker outcome (success/failed/timeout/parse_error) recorded with WorkerResult fields populated.
- Dispatch routed through `superclaude.execution.parallel.ParallelExecutor` (no raw `ThreadPoolExecutor()` calls anywhere in swarm).
- Tests `tests/swarm/test_dispatch.py` and `tests/swarm/test_imm3_parallel.py` are green.

**Validation:**
- `uv run pytest tests/swarm/test_dispatch.py tests/swarm/test_imm3_parallel.py -v` passes.
- `grep -RnE "ThreadPoolExecutor\(" src/superclaude/cli/swarm/` returns no instantiation (only references via ParallelExecutor).

**Dependencies:** T01.10 (Transport Protocol), T03.03 (state), T03.04 (logging_). **Rollback:** revert `dispatch.py`; downstream commands fail closed.
**Notes:** IMM-3 + INV-002 + NFR-001 + AC-004 all bind here.

### T03.03 -- Implement `state` module with atomic `.swarm-state.json` transitions

| Field | Value |
|---|---|
| Roadmap | R-062 (COMP-011) |
| Deliverables | D-0052 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_state.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/state.py` with `read_state` / `write_state` using tmp+`os.replace`.

**Steps:**
1. [PLANNING] Locate sprint `state.py` for the atomic-write idiom.
2. [EXECUTION] Implement `write_state(path, state)` writing to `path.tmp` then `os.replace(path.tmp, path)`.
3. [EXECUTION] Implement `read_state(path) -> SwarmState | None` returning None when file missing.
4. [VERIFICATION] Add mid-write-kill test using `os.kill(os.getpid(), SIGKILL)` from subprocess and assert no partial file.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- State transitions go through tmp+`os.replace`; no `open(path, "w")` writes the live path directly.
- `read_state` returns `SwarmState` dataclass on success, `None` if missing, raises on corrupt JSON.
- Mid-write kill leaves no partial state file (verified by subprocess test).
- `tests/swarm/test_state.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_state.py -v` passes.
- `grep -nE "open\(.*\".*state.*\.json.*w" src/superclaude/cli/swarm/state.py` returns no direct-write matches.

**Dependencies:** T01.10 (SwarmState dataclass available). **Rollback:** revert state module.
**Notes:** NFR-002 atomicity binds here.

### T03.04 -- Implement `logging_` module with dual JSONL + Markdown logs (lock-coordinated)

| Field | Value |
|---|---|
| Roadmap | R-063 (COMP-012) |
| Deliverables | D-0053 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie, context7 (threading) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_logging.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/logging_.py` with append-only lock-coordinated JSONL + human-readable Markdown emitter.
2. `EventRecord` serialization roundtrip + concurrent-append safety test.

**Steps:**
1. [PLANNING] Define `Logger(threading.Lock, jsonl_path, md_path)`.
2. [EXECUTION] Implement `log_event(record: EventRecord)` acquiring lock, appending JSONL + appending md line.
3. [EXECUTION] Document JSONL append-only contract in module docstring.
4. [VERIFICATION] Concurrency test fires 100 events from 10 threads; assert all 100 JSONL lines parse cleanly.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- `cli/swarm/logging_.py` exposes `Logger` class with `log_event(EventRecord) -> None`.
- JSONL appends serialized by `threading.Lock`; concurrent test parses every line.
- Markdown log is human-readable (one event per line, no JSON noise).
- `tests/swarm/test_logging.py` covers single-thread and 10-thread cases.

**Validation:**
- `uv run pytest tests/swarm/test_logging.py -v` passes.
- 100-event concurrent test produces 100 valid JSONL lines (no interleaving).

**Dependencies:** T01.10 (EventRecord dataclass). **Rollback:** revert logging_ module.
**Notes:** NFR-002 + FR-026 bind here.

### T03.05 -- Implement `openai_compat` httpx transport (Phase-1 reference)

| Field | Value |
|---|---|
| Roadmap | R-064 (COMP-032), R-068 (FR-022), R-081 (AC-005), R-085 (AC-017) merged |
| Deliverables | D-0054, D-0067 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, context7 (httpx), auggie |
| Sub-Agent | tech-research (transport contract review) |
| Verification | tests: `uv run pytest tests/swarm/test_openai_compat.py` (env-gated live lane) |

**Deliverables:**
1. `src/superclaude/cli/swarm/transports/openai_compat.py` implementing Transport Protocol via httpx.
2. T2 proxy env-var reader (`T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`).

**Steps:**
1. [PLANNING] Read Transport Protocol from `cli/swarm/transports/__init__.py`.
2. [PLANNING] Confirm httpx in `pyproject.toml`; if missing, add `httpx`.
3. [EXECUTION] Implement `OpenAICompatTransport.send(prompt, timeout) -> WorkerResult` using `httpx.post`.
4. [EXECUTION] Read `T2ProxyUrl`, `T2ProxyKey`, `T2Model0N` at Wave 0 via `read_env()`.
5. [EXECUTION] Record `http_code` + `attempts` + `elapsed_ms` on every outcome.
6. [VERIFICATION] Env-gated live test against reachable T2 proxy when env present; otherwise skip.
7. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- `transports/openai_compat.py` defines `OpenAICompatTransport` implementing `send(prompt, timeout) -> WorkerResult`.
- Endpoint+key+model resolved from `T2ProxyUrl` / `T2ProxyKey` / `T2Model0N` env vars (AC-017).
- httpx is the underlying HTTP library (AC-005).
- `tests/swarm/test_openai_compat.py` covers happy-path parse + 4xx + 5xx + timeout outcomes.

**Validation:**
- `uv run pytest tests/swarm/test_openai_compat.py -v` passes (live lane gated on env).
- `grep -nE "import\s+httpx" src/superclaude/cli/swarm/transports/openai_compat.py` matches.

**Dependencies:** T01.10 (Transport Protocol). **Rollback:** revert transport module; stub path remains operational.
**Notes:** Merged: COMP-032 + FR-022 + AC-005 + AC-017 share the same artifact.

### T03.06 -- Checkpoint: Phase 3 entry gate (tasks 1-5 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP3-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T03.01..T03.05 marked done in execution-log.
- `phase-3-cp1.md` checkpoint report written.
- COMP-002, COMP-007, COMP-011, COMP-012, COMP-032 modules importable.
- ParallelExecutor invocation site present in dispatch (AC-004).

**Validation:**
- Checkpoint file exists under `tasklist/checkpoints/`.
- `uv run pytest tests/swarm/test_dispatch.py tests/swarm/test_state.py tests/swarm/test_logging.py -v` passes.

**Dependencies:** T03.01..T03.05.

### T03.07 -- Implement deterministic-fixture (stub) transport

| Field | Value |
|---|---|
| Roadmap | R-065 (COMP-033), R-069 (FR-023) merged |
| Deliverables | D-0055 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_stub_transport.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/transports/stub.py` with deterministic worker outputs and no network calls.

**Steps:**
1. [PLANNING] Define deterministic-fixture worker-output corpus (one per worker index).
2. [EXECUTION] Implement `StubTransport.send(prompt, timeout) -> WorkerResult` returning seeded outputs by index.
3. [VERIFICATION] Two-run identical-input test asserts identical outputs.
4. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- `transports/stub.py` exposes `StubTransport` implementing Transport Protocol.
- Outputs are deterministic across runs given identical inputs.
- Tests pass without any network access (CI-default lane).
- `tests/swarm/test_stub_transport.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_stub_transport.py -v` passes.
- Two consecutive runs yield byte-identical `WorkerResult.path` contents.

**Dependencies:** T01.10. **Rollback:** revert stub transport.
**Notes:** This transport is the primary CI lane for IMM-3 parallelism test.

### T03.08 -- Implement `swarm run` subcommand (3 input modes)

| Field | Value |
|---|---|
| Roadmap | R-066 (FR-001) |
| Deliverables | D-0056 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit, context7 (Click) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_swarm_run_inputs.py` |

**Deliverables:**
1. `run_cmd` in `commands.py` supporting spec file, stdin, and `--lens` shortcut inputs.

**Steps:**
1. [PLANNING] Enumerate Click options: `--spec`, `--lens`, `--target`, `--output`, stdin fallback.
2. [EXECUTION] Implement input-mode resolution into a single `JobSpec` instance.
3. [EXECUTION] Pass `JobSpec` to preflight then dispatch.
4. [VERIFICATION] Run integration test exercising all 3 modes against stub transport.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- All 3 input modes (spec file, stdin, `--lens`) dispatch a job successfully against stub.
- Mutually exclusive option validation surfaces a Click error on conflicting flags.
- `tests/swarm/test_swarm_run_inputs.py` covers each mode.
- `swarm run --help` documents all 3 modes.

**Validation:**
- `uv run pytest tests/swarm/test_swarm_run_inputs.py -v` passes.
- `echo '{...}' | uv run superclaude swarm run --stdin --transport stub` exits 0.

**Dependencies:** T03.01, T03.02. **Rollback:** disable `--lens` shortcut, keep spec-file mode.
**Notes:** `--lens` shortcut builds a JobSpec with lens-driven defaults from FR-020.

### T03.09 -- Implement per-worker timeout + retry policy (180s, 5xx-once)

| Field | Value |
|---|---|
| Roadmap | R-067 (FR-017), R-076 (NFR-010), R-077 (NFR-011) merged |
| Deliverables | D-0057 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, context7 (httpx timeout) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_retry_policy.py` |

**Deliverables:**
1. `dispatch.py::retry_policy(transport, prompt, spec)` enforcing 180s timeout + 5xx-once retry + backoff.
2. Retry-matrix parametrized test covering 200/4xx/5xx/timeout/network.

**Steps:**
1. [PLANNING] Tabulate retry matrix per §7: 200→none, 4xx→0 retries, 5xx→1 retry+backoff, timeout/network→0.
2. [EXECUTION] Implement `retry_policy` wrapping transport.send with httpx timeout=180s default.
3. [EXECUTION] Backoff sleep applied between 5xx attempts.
4. [VERIFICATION] Parametrize tests over the 5 outcome classes; assert attempts/elapsed/http_code.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- 180s default timeout configurable via `workers.timeout_sec`.
- 5xx retried exactly once with backoff; 4xx never retried; timeout/network never retried.
- Outcome recorded into WorkerResult regardless of branch.
- `tests/swarm/test_retry_policy.py` covers all 5 matrix branches.

**Validation:**
- `uv run pytest tests/swarm/test_retry_policy.py -v` passes.
- Retry matrix table in dispatch.py docstring matches §7 exactly.

**Dependencies:** T03.02 (dispatch), T03.05 (openai_compat). **Rollback:** disable retry; default to single attempt with timeout only.
**Notes:** NFR-010 + NFR-011 covered together with FR-017.

### T03.10 -- Implement dual-format log emission (JSONL append-only + Markdown)

| Field | Value |
|---|---|
| Roadmap | R-070 (FR-026) |
| Deliverables | D-0058 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_dual_log_emission.py` |

**Deliverables:**
1. `execution-log.jsonl` + `execution-log.md` emitted side-by-side during dispatch.

**Steps:**
1. [PLANNING] Confirm Logger from T03.04 covers both streams.
2. [EXECUTION] Wire Logger emission into dispatch worker callbacks (worker_start/progress/done/wave_transition).
3. [VERIFICATION] Run dispatch; assert both files present and parseable.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- `execution-log.jsonl` exists post-dispatch with one record per event.
- `execution-log.md` exists with human-readable rendering of the same events.
- Concurrent append test produces no interleaved/corrupt lines in JSONL.
- `tests/swarm/test_dual_log_emission.py` parses both files end-to-end.

**Validation:**
- `uv run pytest tests/swarm/test_dual_log_emission.py -v` passes.
- `jq . < execution-log.jsonl` exits 0 (valid JSONL).

**Dependencies:** T03.04. **Rollback:** disable md log; keep JSONL.
**Notes:** Builds on T03.04 Logger; emits content at dispatch wiring points.

### T03.11 -- Verify IMM-3 true-parallel dispatch (stub-worker overlap test)

| Field | Value |
|---|---|
| Roadmap | R-071 (IMM-3) |
| Deliverables | D-0059 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie, Bash |
| Sub-Agent | tech-research (concurrency verification) |
| Verification | tests: `uv run pytest tests/swarm/test_imm3_parallel.py` |

**Deliverables:**
1. `tests/swarm/test_imm3_parallel.py` proving wall-clock overlap of N workers against stub.

**Steps:**
1. [PLANNING] Design fixture: each stub worker sleeps S seconds then returns; expect N*S sequential, ~S parallel.
2. [EXECUTION] Write test using `time.monotonic()` to measure dispatch wall-clock.
3. [EXECUTION] Assert wall-clock < N*S * 0.4 (i.e., real concurrency).
4. [VERIFICATION] Run test; if fails, audit ParallelExecutor wiring (AC-004).
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- Fixture-worker parallelism test confirms N workers overlap in wall-clock.
- Test asserts ParallelGroup invoked exactly once (single dispatch call).
- Sequential baseline (one worker) also measured; speedup ≥ 0.4 * N.
- `tests/swarm/test_imm3_parallel.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_imm3_parallel.py -v` passes with timing assertion.
- `pytest --collect-only -q` lists IMM-3 test under `tests/swarm/`.

**Dependencies:** T03.02 (dispatch), T03.07 (stub). **Rollback:** mark IMM-3 test xfail and capture diagnosis in CP.
**Notes:** Code-enforced parallelism replaces attention-mediated tool calls per spec §1.

### T03.12 -- Checkpoint: Phase 3 mid-phase gate (tasks 6-11 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP3-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T03.07..T03.11 marked done in execution-log.
- `phase-3-cp2.md` checkpoint report written.
- IMM-3 parallelism test green; retry-matrix coverage complete.
- Stub-transport-only CI lane defined and passing.

**Validation:**
- `uv run pytest tests/swarm/test_imm3_parallel.py tests/swarm/test_retry_policy.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T03.07..T03.11.

### T03.13 -- Verify IMM-6 atomic-write idempotency (mid-write kill test)

| Field | Value |
|---|---|
| Roadmap | R-072 (IMM-6) |
| Deliverables | D-0060 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_imm6_atomic_write.py` |

**Deliverables:**
1. `tests/swarm/test_imm6_atomic_write.py` proving mid-write kill leaves no partial files.

**Steps:**
1. [PLANNING] Identify every writer path (state, log, contract, sentinel).
2. [EXECUTION] Write test that spawns subprocess writing a payload then SIGKILL mid-write.
3. [EXECUTION] Assert target file either absent or fully written; no partial.
4. [VERIFICATION] Re-run after the kill is idempotent (same content).
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Mid-write kill leaves no partial file at the live path.
- Rerun produces identical content (idempotent).
- All output files (state, log, contract, sentinel) follow tmp+`os.replace` pattern.
- `tests/swarm/test_imm6_atomic_write.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_imm6_atomic_write.py -v` passes.
- `grep -RnE "os\.replace\(" src/superclaude/cli/swarm/` covers each writer.

**Dependencies:** T03.03 (state). **Rollback:** mark IMM-6 test xfail with diagnosis.
**Notes:** IMM-6 + NFR-002 share the same enforcement surface.

### T03.14 -- Verify INV-002 Python-only concurrency (no shell dispatch path)

| Field | Value |
|---|---|
| Roadmap | R-073 (INV-002) |
| Deliverables | D-0061 |
| Effort | S |
| Risk | LOW |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash (grep), auggie |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_concurrency_python_only.py` |

**Deliverables:**
1. `tests/swarm/test_concurrency_python_only.py` asserting no shell dispatch path exists.

**Steps:**
1. [PLANNING] Enumerate forbidden patterns: `swarm_dispatch.sh`, `subprocess.Popen(['bash', ...])`.
2. [EXECUTION] Write test that greps `src/superclaude/cli/swarm/` for forbidden patterns.
3. [EXECUTION] Assert no `.sh` files inside swarm package directory.
4. [VERIFICATION] Run test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- No `swarm_dispatch.sh` references in swarm package.
- No `subprocess.Popen` with shell dispatch arguments.
- Concurrency surface routes purely through Python (ParallelExecutor).
- `tests/swarm/test_concurrency_python_only.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_concurrency_python_only.py -v` passes.
- `find src/superclaude/cli/swarm/ -name '*.sh'` returns empty.

**Dependencies:** T03.02. **Rollback:** soft-fail the assertion while issue triaged.
**Notes:** PIPE_BUF assumption retired with shell path.

### T03.15 -- Enforce NFR-001 ParallelExecutor invocation mandate

| Field | Value |
|---|---|
| Roadmap | R-074 (NFR-001), R-080 (AC-004) merged |
| Deliverables | D-0062 |
| Effort | S |
| Risk | LOW |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash (grep), serena |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_parallel_executor_routing.py` |

**Deliverables:**
1. `tests/swarm/test_parallel_executor_routing.py` asserting dispatch routes through ParallelExecutor.

**Steps:**
1. [PLANNING] Use serena to locate ParallelExecutor public surface.
2. [EXECUTION] Write test importing dispatch module and asserting `ParallelExecutor` symbol used.
3. [EXECUTION] Add static grep assertion: no `ThreadPoolExecutor(` instantiation in swarm package.
4. [VERIFICATION] Run test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Dispatch invokes `superclaude.execution.parallel.ParallelExecutor`, not raw `ThreadPoolExecutor`.
- Static grep finds no `ThreadPoolExecutor(` calls in `src/superclaude/cli/swarm/`.
- AC-004 mandate documented in `dispatch.py` docstring.
- `tests/swarm/test_parallel_executor_routing.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_parallel_executor_routing.py -v` passes.
- `grep -RnE "ThreadPoolExecutor\(" src/superclaude/cli/swarm/` returns no instantiations.

**Dependencies:** T03.02. **Rollback:** none — this is a guard.
**Notes:** NFR-001 + AC-004 merge into one enforcement test.

### T03.16 -- Verify NFR-002 atomicity (state + JSONL lock)

| Field | Value |
|---|---|
| Roadmap | R-075 (NFR-002) |
| Deliverables | D-0063 |
| Effort | S |
| Risk | LOW |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_nfr002_atomicity.py` |

**Deliverables:**
1. `tests/swarm/test_nfr002_atomicity.py` combining state atomic-write + concurrent JSONL.

**Steps:**
1. [PLANNING] Compose state + log atomic-write assertions.
2. [EXECUTION] Write parameterized test exercising both surfaces concurrently.
3. [VERIFICATION] Run test in CI lane.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- No partial state files under concurrent write attempts.
- JSONL appends serialized by `threading.Lock`; no interleaved bytes.
- Test passes under `pytest -p no:cacheprovider`.
- `tests/swarm/test_nfr002_atomicity.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_nfr002_atomicity.py -v` passes.
- Concurrent 100-event run produces 100 valid JSONL records.

**Dependencies:** T03.03, T03.04, T03.13. **Rollback:** capture failure in CP.

### T03.17 -- Enforce NFR-013 output-directory write confinement

| Field | Value |
|---|---|
| Roadmap | R-078 (NFR-013), R-083 (AC-014) merged |
| Deliverables | D-0064 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_output_confinement.py` |

**Deliverables:**
1. `state.py::confine_path(path, output_dir)` rejecting any path outside `--output`.
2. Test exercising directory-escape attempts (..`/etc/passwd`, absolute paths).

**Steps:**
1. [PLANNING] Define `confine_path` using `Path.resolve().is_relative_to(output_dir.resolve())`.
2. [EXECUTION] Add guard at every write site (state, log, contract, sentinel).
3. [VERIFICATION] Test escapes (relative `..`, absolute) raise.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Attempted writes outside `--output` rejected with explicit exception.
- All writer call sites import and call `confine_path`.
- Tests cover absolute escape, `..` traversal, and symlink escape.
- `tests/swarm/test_output_confinement.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_output_confinement.py -v` passes.
- `grep -RnE "confine_path\(" src/superclaude/cli/swarm/` covers each writer.

**Dependencies:** T03.03. **Rollback:** soft-allow with WARN log; raise issue.
**Notes:** NFR-013 + AC-014 share guard.

### T03.18 -- Checkpoint: Phase 3 invariants gate (tasks 12-17 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP3-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T03.13..T03.17 marked done in execution-log.
- `phase-3-cp3.md` checkpoint report written.
- IMM-3, IMM-6, INV-002, NFR-001, NFR-002, NFR-013 all enforced and tested.
- ParallelExecutor invocation site present in dispatch.

**Validation:**
- `uv run pytest tests/swarm/test_imm6_atomic_write.py tests/swarm/test_concurrency_python_only.py tests/swarm/test_parallel_executor_routing.py tests/swarm/test_nfr002_atomicity.py tests/swarm/test_output_confinement.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T03.13..T03.17.

### T03.18a -- Checkpoint: Phase 3 transport-env gate (interim, pre-exit)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP3-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- AC-014 output-confinement, NFR-013 path guard verified.
- T03.18 invariants gate green.
- Pre-exit verification that transport env contract (T03.21) and caching guards (T03.19, T03.20) are scheduled to run.
- Provisional sign-off for end-of-phase exit (T03.22) granted.

**Validation:**
- Phase 3 task IDs T03.13..T03.18 marked complete.
- Checkpoint file `phase-3-cp4.md` written under `tasklist/checkpoints/`.

**Dependencies:** T03.18.

### T03.19 -- Enforce NFR-014 no-cross-invocation response caching

| Field | Value |
|---|---|
| Roadmap | R-079 (NFR-014), R-084 (AC-015) merged |
| Deliverables | D-0065 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, Bash (grep) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_no_response_cache.py` |

**Deliverables:**
1. `tests/swarm/test_no_response_cache.py` asserting no cache layer in dispatch/transport.

**Steps:**
1. [PLANNING] Enumerate forbidden cache patterns (`functools.lru_cache`, `cachetools`, `requests_cache`).
2. [EXECUTION] Write test grepping swarm package for cache imports.
3. [EXECUTION] Add integration test: two identical runs both hit transport (assert hit count == 2).
4. [VERIFICATION] Run tests.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- No response cache module present in swarm.
- Two identical runs both hit transport (call count 2, not 1).
- No cache-decorator imports detected.
- `tests/swarm/test_no_response_cache.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_no_response_cache.py -v` passes.
- `grep -RnE "lru_cache|cachetools|requests_cache" src/superclaude/cli/swarm/` returns empty.

**Dependencies:** T03.02, T03.05. **Rollback:** none — guard test.

### T03.20 -- Enforce AC-010 no-routing-to-Anthropic-models guard

| Field | Value |
|---|---|
| Roadmap | R-082 (AC-010) |
| Deliverables | D-0066 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash (grep) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_no_anthropic_routing.py` |

**Deliverables:**
1. `tests/swarm/test_no_anthropic_routing.py` greps transport config for Anthropic endpoints.

**Steps:**
1. [PLANNING] Enumerate forbidden strings: `api.anthropic.com`, `claude-`, `anthropic` (case-insensitive) in transport configs.
2. [EXECUTION] Write test asserting transport config audit finds no Anthropic endpoints.
3. [EXECUTION] Confirm openai_compat base URL env var is not pointed at Anthropic.
4. [VERIFICATION] Run test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- No `api.anthropic.com` or `claude-*` model names in transport configs.
- T2 proxy endpoint resolves to non-Anthropic upstream.
- Test asserts audit cleanliness on every transport module.
- `tests/swarm/test_no_anthropic_routing.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_no_anthropic_routing.py -v` passes.
- `grep -RniE "anthropic|claude-" src/superclaude/cli/swarm/transports/` returns empty.

**Dependencies:** T03.05. **Rollback:** none — guard.

### T03.21 -- Wire T2 proxy env contract reader (`T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`)

| Field | Value |
|---|---|
| Roadmap | R-085 (AC-017) |
| Deliverables | D-0067 |
| Effort | S |
| Risk | LOW |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_t2_env_contract.py` |

**Deliverables:**
1. `openai_compat.py::read_env()` enumerating T2 env vars and emitting structured config.

**Steps:**
1. [PLANNING] Enumerate `T2ProxyUrl`, `T2ProxyKey`, `T2Model0N` (N=1..max).
2. [EXECUTION] Implement env reader returning `TransportConfig`.
3. [EXECUTION] Document env var contract in module docstring.
4. [VERIFICATION] Test reads all vars from controlled env; missing vars surface clear error.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Transport reads endpoint + key + model from env at Wave 0.
- Missing env vars surface explicit failure (consumed by INV-007 path).
- Env contract documented in `docs/swarm/runbook.md`.
- `tests/swarm/test_t2_env_contract.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_t2_env_contract.py -v` passes.
- `grep -nE "T2ProxyUrl|T2ProxyKey|T2Model0" src/superclaude/cli/swarm/transports/openai_compat.py` matches.

**Dependencies:** T03.05. **Rollback:** revert env reader.
**Notes:** Couples with INV-007 (T02.11) empty-pool failure path.

### T03.22 -- Checkpoint: Phase 3 exit gate (end-of-phase)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase) |
| Deliverables | D-CP3-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T03.01..T03.21 marked done in execution-log.
- `phase-3-cp4.md` end-of-phase checkpoint written.
- `swarm run` executes Wave 0→1 end-to-end against stub transport.
- IMM-3 + IMM-6 + INV-002 + NFR-001/002/010/011/013/014 all green; AC-004/005/010/014/015/017 enforced.

**Validation:**
- `uv run pytest tests/swarm/ -v` passes for Phase 3 surface.
- Checkpoint file under `tasklist/checkpoints/`; OQ-007/008 confirmed resolved by M2 exit.

**Dependencies:** T03.01..T03.21. **Rollback:** none — phase exit gate.
**Notes:** M3 exit unblocks M4 normalize work.
