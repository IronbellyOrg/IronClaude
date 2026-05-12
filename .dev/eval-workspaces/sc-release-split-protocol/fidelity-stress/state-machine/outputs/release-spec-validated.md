---
parent-spec: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/evals/files/fidelity-stress-state-machine.md
split-analysis: "no-split-recommended"
rationale: "Dense cross-component dependencies prevent meaningful decomposition; shadow mode deployment provides superior real-world validation"
status: validated
release: pipeline-state-machine-v2.0
version: 2.0.0
priority: P0
estimated_scope: 1200-1600 lines production code
enforcement_model: "shadow -> soft -> full (3-phase)"
---

# Pipeline State Machine v2.0 — Validated Release Specification

## Why This Release Stays Intact

The split analysis evaluated 4 candidate seams and found none viable:

1. **Core vs. Operational Infrastructure**: Events are inline side effects in transition tables, not a separable downstream consumer. Concurrency limits are guard conditions embedded in transition rows.
2. **State Machine vs. Migration/Observability/Testing**: Migration mapping requires all states defined; observability enables invariant enforcement; incident regression tests are the proof the system solves its motivating problems.
3. **Schema Only vs. Implementation**: The spec IS the schema — implementing it as code IS the deliverable. No intermediate "schema hardening" step provides standalone value.
4. **Single-Scope vs. Multi-Scope**: Cross-scope dependencies (task failures increment `phase.failure_count`, circuit breaker triggers phase transitions, pipeline emergency stop kills active tasks) make scope isolation impractical.

The adversarial review confirmed this assessment with 0.92 convergence. The strongest counter-argument (task scope alone could prevent INC-047) was refuted by the observation that task transitions reference phase-level state as guard conditions.

## Risks Addressed Without Splitting

| Risk | Mitigation Strategy |
|------|-------------------|
| Large implementation scope (1200-1600 LOC) | Staged internal implementation within single branch: task scope → phase scope → pipeline scope, with property tests at each stage |
| Design flaws discovered late | Shadow mode deployment (§7.2 Phase 1) validates complete state machine against real pipeline runs with zero production risk |
| Incident regression not proven early | INC-041/047/052 regression tests (§8.2) implemented alongside the state machine, not deferred |
| Integration complexity | File manifest (§10) provides clear single-responsibility boundaries across 10 files |
| Cross-scope edge cases | Circuit breaker interaction with phase transitions tested via dedicated test file (§10: `test_circuit_breaker.py`) |

## Validation Strategy

The spec's built-in 3-phase migration strategy IS the validation strategy:

1. **Phase 1 (Shadow Mode)**: Deploy v2.0 state machine alongside v1.0 boolean flags. v2.0 logs state transitions and divergences. v1.0 continues to drive behavior. This provides real-world validation of the state machine design against actual pipeline runs without risk.

2. **Migration Gate**: Phase 2 activation requires zero state divergences between v1.0 and v2.0 for a minimum of 50 pipeline runs. This is a quantitative, auditable gate.

3. **Phase 2 (Soft Cutover)**: Switch to v2.0 as primary. v1.0 flags written for backward compatibility but not read. Any regression triggers immediate rollback to Phase 1.

4. **Phase 3 (Full)**: Remove v1.0 flag infrastructure after extended Phase 2 validation.

**Additional internal milestones** (not release boundaries):
- Milestone 1: Task scope state machine + property tests + INC-047 regression test
- Milestone 2: Phase scope + cross-scope tests + INC-041 regression test
- Milestone 3: Pipeline scope + circuit breaker + INC-052 regression test
- Milestone 4: Event system + audit trail + observability metrics
- Milestone 5: Migration infrastructure + shadow mode + integration tests

## Original Spec — Complete Preservation

All content below is preserved verbatim from the original specification. No requirements have been added, removed, weakened, or paraphrased.

---

## 1. Problem Statement

The pipeline executor's state management is implicit — states are derived from combinations of boolean flags (`is_running`, `has_error`, `is_complete`) rather than a formal state machine. This caused three production incidents:

| Incident | Date | Root Cause | Impact |
|----------|------|-----------|--------|
| INC-041 | 2026-02-14 | Phase entered `RUNNING` while predecessor was `BLOCKED` — no transition guard | 3 phases executed out of order, corrupt artifacts |
| INC-047 | 2026-02-28 | Task set to `COMPLETE` while gate was `PENDING` — gate silently skipped | Ungated release shipped |
| INC-052 | 2026-03-08 | `RETRY` state looped indefinitely — no max-retry counter, no backoff, no circuit breaker | Sprint consumed 847K tokens before manual kill |

## 2. State Machine Definition

### 2.1 States

The pipeline operates on three scopes with distinct state sets:

**Task scope** (7 states):
`PENDING` → `QUEUED` → `RUNNING` → `GATING` → `COMPLETE` | `FAILED` | `SKIPPED`

**Phase scope** (6 states):
`PENDING` → `RUNNING` → `GATING` → `COMPLETE` | `FAILED` | `BLOCKED`

**Pipeline scope** (5 states):
`INITIALIZING` → `RUNNING` → `FINALIZING` → `COMPLETE` | `FAILED`

### 2.2 Transition Table — Task Scope

| From | To | Guard Condition | Side Effect | Rollback Action |
|------|----|----------------|-------------|-----------------|
| PENDING | QUEUED | `phase.state == RUNNING` AND `all_predecessors(task).state in {COMPLETE, SKIPPED}` | Emit `task.queued` event with `enqueue_timestamp_utc` | None |
| QUEUED | RUNNING | `active_task_count(phase) < phase.concurrency_limit` | Acquire task lock; emit `task.started` with `start_timestamp_utc` | Release task lock |
| RUNNING | GATING | `task.execution_result is not None` AND `task.execution_result.exit_code == 0` | Run gate checks sequentially; emit `task.gating` | Revert to RUNNING with `gate_attempt += 1` |
| RUNNING | FAILED | `task.execution_result.exit_code != 0` OR `task.wall_time > task.timeout_seconds` | Emit `task.failed` with `failure_reason`; increment `phase.failure_count` | None (terminal) |
| GATING | COMPLETE | `all(gate.passed for gate in task.required_gates)` | Emit `task.completed`; decrement `phase.pending_count`; release task lock | None (terminal) |
| GATING | FAILED | `any(gate.hard_failed for gate in task.required_gates)` AND `task.gate_retry_count >= task.max_gate_retries` | Emit `task.gate_failed`; record gate failure evidence in `DeferredRemediationLog` | None (terminal) |
| GATING | RUNNING | `any(gate.soft_failed for gate in task.required_gates)` AND `task.gate_retry_count < task.max_gate_retries` | Increment `gate_retry_count`; emit `task.gate_retry` with backoff delay `min(2^retry * base_delay_ms, max_delay_ms)` where `base_delay_ms=500` and `max_delay_ms=30000` | None |
| PENDING | SKIPPED | `skip_condition(task) == True` OR `any_predecessor(task).state == FAILED` AND `task.skip_on_predecessor_failure == True` | Emit `task.skipped` with `skip_reason` | None (terminal) |

**Invariants (must hold at ALL times, enforced by transition validator):**
- INV-T1: A task in `RUNNING` state MUST hold exactly one task lock. Zero locks or multiple locks is a violation.
- INV-T2: `gate_retry_count` MUST be monotonically increasing and MUST NOT exceed `max_gate_retries` (default: 3).
- INV-T3: A task MUST NOT transition to `COMPLETE` if any gate with `enforcement_tier == "STRICT"` has `passed == False`.
- INV-T4: Transition timestamps MUST be monotonically increasing: `enqueue_timestamp_utc < start_timestamp_utc < completion_timestamp_utc`.
- INV-T5: A task in a terminal state (`COMPLETE`, `FAILED`, `SKIPPED`) MUST NOT accept any further transitions. The transition validator MUST reject and log the attempt.
- INV-T6: The `GATING → RUNNING` retry transition MUST NOT fire if `gate_retry_count >= max_gate_retries`. If this condition is met, the ONLY valid transition is `GATING → FAILED`.

### 2.3 Transition Table — Phase Scope

| From | To | Guard Condition | Side Effect |
|------|----|----------------|-------------|
| PENDING | RUNNING | `pipeline.state == RUNNING` AND `all_predecessor_phases(phase).state == COMPLETE` | Initialize task queue; emit `phase.started` |
| RUNNING | GATING | `all_tasks(phase).state in {COMPLETE, FAILED, SKIPPED}` AND `phase.failure_count <= phase.max_failures` | Run phase-level gates |
| RUNNING | FAILED | `phase.failure_count > phase.max_failures` | Emit `phase.failed`; set `pipeline.should_abort = True` if `phase.abort_on_failure == True` |
| GATING | COMPLETE | `all(gate.passed for gate in phase.required_gates)` | Emit `phase.completed`; unblock successor phases |
| GATING | FAILED | `any(gate.hard_failed for gate in phase.required_gates)` | Emit `phase.gate_failed` |
| PENDING | BLOCKED | `any_predecessor_phase(phase).state == FAILED` AND `phase.skip_on_predecessor_failure == False` | Emit `phase.blocked` with `blocking_phase_id` |

**Invariants:**
- INV-P1: A phase MUST NOT enter `RUNNING` while any predecessor phase is in `RUNNING`, `GATING`, `PENDING`, or `BLOCKED` state. ONLY `COMPLETE` satisfies the predecessor guard.
- INV-P2: `phase.failure_count` MUST equal the count of tasks in that phase with `state == FAILED`. It MUST NOT be independently settable.
- INV-P3: Phase `max_failures` default is `0` (zero tolerance). This means a SINGLE task failure triggers `RUNNING → FAILED` transition for the phase UNLESS `max_failures` is explicitly configured higher.
- INV-P4: The `BLOCKED` state is terminal for the current pipeline run. A blocked phase MUST NOT transition to any other state within the same run.

### 2.4 Transition Table — Pipeline Scope

| From | To | Guard Condition | Side Effect |
|------|----|----------------|-------------|
| INITIALIZING | RUNNING | `config_validated == True` AND `at_least_one_phase_defined == True` | Load phase DAG; emit `pipeline.started` |
| RUNNING | FINALIZING | `all_phases(pipeline).state in {COMPLETE, FAILED, BLOCKED, SKIPPED}` | Begin finalization sequence |
| FINALIZING | COMPLETE | `finalization_tasks_done == True` AND `pipeline.critical_phase_failures == 0` | Emit `pipeline.completed`; write final report |
| FINALIZING | FAILED | `pipeline.critical_phase_failures > 0` OR `finalization_timeout_exceeded == True` | Emit `pipeline.failed` with aggregated failure report |
| RUNNING | FAILED | `pipeline.should_abort == True` | Emergency stop; kill active tasks with `SIGTERM` then `SIGKILL` after 5s grace period |

**Invariants:**
- INV-PL1: `pipeline.critical_phase_failures` counts ONLY phases where `abort_on_failure == True` AND `state == FAILED`. Non-critical phase failures do NOT increment this counter.
- INV-PL2: The emergency stop sequence (`RUNNING → FAILED` via `should_abort`) MUST send `SIGTERM` first, wait exactly 5 seconds, then send `SIGKILL` to any remaining processes. It MUST NOT send `SIGKILL` without the 5-second grace period.
- INV-PL3: Pipeline MUST NOT enter `FINALIZING` while any phase is in `RUNNING` or `GATING` state.

## 3. Error Handling Contracts

### 3.1 Retry Semantics

**Gate retry** (task scope):
- Applies ONLY to `soft_failed` gates, NEVER to `hard_failed` gates
- Backoff formula: `delay_ms = min(2^retry_count * 500, 30000)`
  - Retry 0: 500ms
  - Retry 1: 1000ms
  - Retry 2: 2000ms
  - Retry 3: max_gate_retries reached → GATING → FAILED
- The retry delay is BLOCKING — the task remains in `RUNNING` state during the delay, not `GATING`
- During retry delay, the task lock MUST remain held (INV-T1 still applies)

**Phase retry** (not supported in v2.0):
- Phase-level retry is explicitly OUT OF SCOPE for this release
- A failed phase remains `FAILED` for the remainder of the pipeline run
- Phase retry is deferred to v2.1 pending state machine hardening validation

### 3.2 Timeout Handling

**Task timeout**:
- `task.timeout_seconds` default: `300` (5 minutes)
- Timeout is measured from `start_timestamp_utc`, NOT from `enqueue_timestamp_utc`
- When a task exceeds `timeout_seconds`, the state machine transitions `RUNNING → FAILED` with `failure_reason = "timeout_exceeded"`
- The subprocess is killed with `SIGTERM`, 5-second grace, then `SIGKILL` (same as pipeline emergency stop)
- A timed-out task MUST NOT enter `GATING` state — timeout preempts gate evaluation

**Phase timeout**:
- `phase.timeout_seconds` default: `1800` (30 minutes)
- Phase timeout triggers `RUNNING → FAILED` for the phase AND cancels all `QUEUED` tasks in that phase
- `RUNNING` tasks within a timed-out phase receive individual timeout handling per above

**Pipeline timeout**:
- `pipeline.timeout_seconds` default: `7200` (2 hours)
- Pipeline timeout sets `pipeline.should_abort = True`, triggering emergency stop

### 3.3 Circuit Breaker

When a phase accumulates `circuit_breaker_threshold` consecutive task failures (default: 3), the phase transitions to `FAILED` regardless of `max_failures` setting.

**Critical distinction**: `circuit_breaker_threshold` counts CONSECUTIVE failures only. If tasks A, B, C fail but task D succeeds between B and C, the counter resets to 1 after D's success.

The circuit breaker MUST NOT fire on `SKIPPED` tasks — only `FAILED` tasks increment the consecutive failure counter. A sequence of FAILED, SKIPPED, FAILED counts as 1 consecutive failure (the counter resets on SKIPPED because SKIPPED is not a failure).

**Wait — correction**: SKIPPED tasks do NOT reset the consecutive failure counter. They are transparent to it. A sequence of FAILED, SKIPPED, FAILED counts as 2 consecutive failures. Only a COMPLETE task resets the counter to 0.

## 4. Event System

### 4.1 Event Schema

Every state transition emits a structured event:

```python
@dataclass
class StateTransitionEvent:
    scope: Literal["task", "phase", "pipeline"]
    entity_id: str
    from_state: str
    to_state: str
    timestamp_utc: datetime
    guard_conditions_evaluated: list[str]
    guard_conditions_passed: list[str]
    guard_conditions_failed: list[str]  # empty on success
    side_effects_executed: list[str]
    transition_duration_ms: int
    metadata: dict[str, Any]
```

### 4.2 Event Ordering Guarantees

- Events within a single scope (same `entity_id`) MUST be strictly ordered by `timestamp_utc`
- Events across scopes (different entity IDs) are partially ordered: a phase `COMPLETE` event MUST precede any successor phase `RUNNING` event
- Event delivery is AT-LEAST-ONCE — consumers must be idempotent
- Event buffer capacity: 10,000 events. When buffer is full, oldest events are evicted with a `buffer_overflow` warning logged. Events are NEVER dropped silently.

### 4.3 Audit Trail Requirements

The state machine MUST maintain a complete audit trail of ALL attempted transitions, including rejected ones:

```python
@dataclass
class AuditEntry:
    attempted_transition: tuple[str, str]  # (from_state, to_state)
    accepted: bool
    rejection_reason: str | None  # populated only when accepted == False
    invariants_checked: list[str]
    invariants_violated: list[str]  # empty when accepted == True
    timestamp_utc: datetime
    actor: str  # "system" | "user_override" | "timeout" | "circuit_breaker"
```

Rejected transitions MUST be logged at `WARNING` level with the rejection reason and violated invariants. They MUST NOT raise exceptions — the state machine silently rejects invalid transitions and continues operating.

## 5. Concurrency Model

### 5.1 Task Concurrency

Within a phase, up to `phase.concurrency_limit` tasks may be in `RUNNING` state simultaneously.

- Default `concurrency_limit`: 3
- Minimum: 1 (serial execution)
- Maximum: 10 (hard cap, not configurable above this)
- The concurrency limit applies to `RUNNING` tasks only — `GATING` tasks do NOT count against the limit
- When a task transitions from `RUNNING` to `GATING`, the concurrency slot is freed and a `QUEUED` task may start

**Critical**: Tasks in `GATING` state do NOT count against concurrency limit. This is intentional — gate evaluation is I/O bound (reading report files) not CPU bound, and blocking new task starts during gate evaluation would serialize the pipeline unnecessarily.

### 5.2 Phase Concurrency

Phases execute sequentially by default. The phase DAG defines ordering constraints.

- Phases with no dependency relationship MAY execute concurrently if `pipeline.parallel_phases == True` (default: False)
- Even with `parallel_phases == True`, predecessor constraints are enforced: a phase cannot start until all predecessors are `COMPLETE`
- The `parallel_phases` flag does NOT override the phase DAG — it only enables concurrency between phases that have no ordering constraint

### 5.3 Lock Semantics

Task locks are re-entrant within the same execution context but NOT across contexts.

- Lock acquisition timeout: 10 seconds. If the lock cannot be acquired within 10 seconds, the `QUEUED → RUNNING` transition fails and the task returns to `QUEUED` state with `lock_acquisition_failures += 1`
- After 3 consecutive lock acquisition failures, the task transitions `QUEUED → FAILED` with `failure_reason = "lock_acquisition_timeout"`
- Lock release is GUARANTEED on any transition out of `RUNNING` state (via context manager `__exit__`)
- Stale lock detection: if a task has held a lock for longer than `task.timeout_seconds + 30` seconds without any state transition, the lock is considered stale and is forcibly released with a `stale_lock_released` event

## 6. Observability

### 6.1 Metrics

The state machine exposes the following metrics via the telemetry SDK:

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `sm.transition.total` | Counter | `scope`, `from_state`, `to_state`, `accepted` | Total transition attempts |
| `sm.transition.duration_ms` | Histogram | `scope`, `from_state`, `to_state` | Transition execution time |
| `sm.state.duration_seconds` | Gauge | `scope`, `entity_id`, `state` | Time spent in current state |
| `sm.invariant.violation` | Counter | `scope`, `invariant_id` | Invariant violations detected |
| `sm.lock.acquisition_time_ms` | Histogram | `entity_id` | Lock acquisition latency |
| `sm.lock.stale_releases` | Counter | `entity_id` | Stale locks forcibly released |
| `sm.circuit_breaker.trips` | Counter | `phase_id` | Circuit breaker activations |
| `sm.event_buffer.overflow` | Counter | — | Event buffer overflow incidents |

### 6.2 Health Check

The state machine exposes a health check endpoint returning:

```json
{
  "healthy": true,
  "active_tasks": 3,
  "active_phases": 1,
  "locks_held": 3,
  "stale_locks": 0,
  "event_buffer_utilization": 0.23,
  "last_transition_utc": "2026-03-18T14:32:01Z",
  "invariant_violations_last_hour": 0
}
```

`healthy` is `false` if ANY of: `stale_locks > 0`, `event_buffer_utilization > 0.9`, `invariant_violations_last_hour > 0`.

## 7. Migration from v1.0

### 7.1 Compatibility

- v1.0 boolean flag combinations map to v2.0 states as follows:
  - `is_running=True, has_error=False, is_complete=False` → `RUNNING`
  - `is_running=False, has_error=True, is_complete=False` → `FAILED`
  - `is_running=False, has_error=False, is_complete=True` → `COMPLETE`
  - `is_running=True, has_error=True, is_complete=False` → `RUNNING` (error flag was previously ignored during execution — this is INC-041's root cause)
  - All other combinations → `PENDING` (conservative default for unmappable states)

### 7.2 Migration Strategy

- Phase 1: Deploy v2.0 state machine in shadow mode alongside v1.0 flags. Both systems run; v2.0 logs divergences but v1.0 drives behavior.
- Phase 2: Switch to v2.0 as primary. v1.0 flags are written for backward compatibility but not read.
- Phase 3: Remove v1.0 flag infrastructure entirely.

**Migration gate**: Phase 2 activation requires zero state divergences between v1.0 and v2.0 for a minimum of 50 pipeline runs.

## 8. Testing Strategy

### 8.1 State Machine Property Tests

Using hypothesis or equivalent:
- **Reachability**: Every defined state is reachable from `PENDING` (task) / `PENDING` (phase) / `INITIALIZING` (pipeline)
- **No orphan states**: Every state has at least one outgoing transition OR is terminal
- **Invariant preservation**: No sequence of valid transitions violates any INV-* invariant
- **Deadlock freedom**: No state exists from which no transition is possible except terminal states
- **Determinism**: Given the same state and guard conditions, the transition outcome is always the same

### 8.2 Incident Regression Tests

Each of INC-041, INC-047, and INC-052 must have a dedicated regression test proving the v2.0 state machine prevents the incident scenario:

- INC-041 regression: Attempt `phase.PENDING → phase.RUNNING` while predecessor is `RUNNING` → transition MUST be rejected by INV-P1
- INC-047 regression: Attempt `task.GATING → task.COMPLETE` while a STRICT gate has `passed == False` → transition MUST be rejected by INV-T3
- INC-052 regression: Trigger gate retry loop → `gate_retry_count` MUST NOT exceed `max_gate_retries` (INV-T6); circuit breaker MUST trip after `circuit_breaker_threshold` consecutive failures

## 9. Non-Functional Requirements

- State transition latency: p99 < 5ms (excluding side effects)
- Audit trail write latency: p99 < 2ms
- Event emission latency: p99 < 1ms
- State machine memory footprint: < 50MB for a pipeline with 100 tasks across 10 phases
- Lock contention rate: < 1% under normal concurrency (3 concurrent tasks per phase)

## 10. File Manifest

| File | Action | LOC | Purpose |
|------|--------|-----|---------|
| `src/superclaude/pipeline/state_machine.py` | CREATE | 400-500 | Core state machine: states, transitions, guards, invariants |
| `src/superclaude/pipeline/events.py` | CREATE | 120-150 | Event system: schema, buffer, emission |
| `src/superclaude/pipeline/locks.py` | CREATE | 80-100 | Lock management: acquisition, release, stale detection |
| `src/superclaude/pipeline/circuit_breaker.py` | CREATE | 60-80 | Circuit breaker: consecutive failure tracking |
| `src/superclaude/pipeline/metrics.py` | MODIFY | +40 | Add state machine metrics to telemetry SDK |
| `src/superclaude/cli/sprint/executor.py` | MODIFY | +80 | Replace boolean flags with state machine calls |
| `src/superclaude/cli/sprint/config.py` | MODIFY | +15 | Add state machine config fields |
| `tests/pipeline/test_state_machine.py` | CREATE | 300-400 | Property tests + invariant tests |
| `tests/pipeline/test_incidents.py` | CREATE | 100-120 | INC-041, INC-047, INC-052 regression tests |
| `tests/pipeline/test_circuit_breaker.py` | CREATE | 60-80 | Circuit breaker edge cases |

## Traceability

All 10 sections of the original specification are preserved verbatim in this validated spec. No requirements were added, removed, weakened, or paraphrased. The only additions are the validation strategy preamble sections which document the split analysis outcome and risk mitigations.
