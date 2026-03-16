# Phase 9 -- Observability Completion

Complete operational visibility infrastructure beyond the Phase 3 baseline. Required for real usage and post-run troubleshooting.

---

### T09.01 -- Complete PortifyTUI with Rich Real-Time Progress Display

| Field | Value |
|---|---|
| Roadmap Item IDs | R-058 |
| Why | Long-running Claude steps (600–1200s) require real-time visibility; without TUI progress, users cannot distinguish a running pipeline from a hung one |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0054 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0054/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/tui.py` complete: `PortifyTUI` with `rich` Progress, Live display, step status table, real-time byte count and elapsed time per step (NFR-008)

**Steps:**
1. **[PLANNING]** Load existing `tui.py` content; identify baseline lifecycle vs. completion gaps
2. **[EXECUTION]** Implement `PortifyTUI.update_step(step_id, status, bytes_written, elapsed_s)` updating Rich Progress bar
3. **[EXECUTION]** Implement `PortifyTUI.update_convergence(iteration, findings_count, placeholder_count)` for Phase 8 loop display
4. **[EXECUTION]** Implement step status table using `rich.table.Table` showing step_id, status, elapsed, bytes
5. **[EXECUTION]** Wire `OutputMonitor.update()` callback to call `PortifyTUI.update_step()` on each subprocess output chunk during execution (not only on completion — needed for real-time visibility during 600–1200s Claude steps)
6. **[EXECUTION]** Use `rich.live.Live` context manager for flicker-free updates
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "tui_complete or tui_update" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0054/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "tui_update"` exits 0
- `PortifyTUI.update_step()` callable without exception for all PortifyStatus values
- `PortifyTUI.update_convergence()` callable with iteration 1–3 without exception
- `PortifyTUI.start()` and `PortifyTUI.stop()` lifecycle tested end-to-end
- Progress bar shows at least one intermediate update during a mocked 5s subprocess run (real-time update, not post-completion only)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "tui_complete" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0054/spec.md` produced

**Dependencies:** T03.13 (TUI lifecycle baseline), T08.01 (ConvergenceState for convergence display)
**Rollback:** Revert `tui.py` to baseline lifecycle only

---

### T09.02 -- Complete OutputMonitor with Convergence and Finding Tracking

| Field | Value |
|---|---|
| Roadmap Item IDs | R-059 |
| Why | The Phase 3 monitor baseline tracked bytes and stall; Phase 8 panel review requires convergence iteration, findings count, and placeholder count tracking for diagnostics |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0055 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0055/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/monitor.py` complete: `OutputMonitor` adds `convergence_iteration`, `findings_count`, `placeholder_count` fields with update methods (NFR-009)

**Steps:**
1. **[PLANNING]** Load existing `monitor.py`; identify which of the 8 NFR-009 fields are missing
2. **[EXECUTION]** Add `convergence_iteration: int = 0` field; implement `set_convergence_iteration(n: int)` method
3. **[EXECUTION]** Add `findings_count: int = 0` field; implement `increment_findings(n: int)` method
4. **[EXECUTION]** Add `placeholder_count: int = 0` field; implement `set_placeholder_count(n: int)` method
5. **[EXECUTION]** Wire `set_convergence_iteration()` into `ConvergenceLoop.run_iteration()` calls
6. **[EXECUTION]** Wire `set_placeholder_count()` into placeholder scan in T07.03
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "monitor_complete or convergence_tracking" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0055/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "monitor_complete"` exits 0
- All 8 NFR-009 fields present in `OutputMonitor`: output_bytes, growth_rate_bps, stall_seconds, events, line_count, convergence_iteration, findings_count, placeholder_count
- `set_convergence_iteration(2)` updates `monitor.convergence_iteration` to 2
- `set_placeholder_count(0)` reflects in monitor state

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "convergence_tracking" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0055/spec.md` produced

**Dependencies:** T03.13 (monitor baseline), T08.01 (ConvergenceLoop for wiring)
**Rollback:** Revert `monitor.py` to Phase 3 baseline

---

### T09.03 -- Implement Failure Diagnostics Collection in diagnostics.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-060 |
| Why | Gate failures, subprocess errors, and timeout events must be diagnosable without re-reading raw artifacts; diagnostics.py provides structured failure context |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0056 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0056/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/diagnostics.py` `DiagnosticsCollector`: collects gate failure reason, exit code, missing artifact paths, and resume guidance; writes `workdir/diagnostics.md` on pipeline failure (FR-042)

**Steps:**
1. **[PLANNING]** Review roadmap FR-042: gate failure reason, exit code, missing artifacts, resume guidance
2. **[EXECUTION]** Create `diagnostics.py` with `DiagnosticsBundle` dataclass: `{step_id, gate_failures: list[GateFailure], exit_code: int | None, missing_artifacts: list[str], resume_guidance: str}`
3. **[EXECUTION]** Implement `DiagnosticsCollector.record_gate_failure(failure: GateFailure)` and `record_exit_code(code: int)`
4. **[EXECUTION]** Implement `DiagnosticsCollector.emit_diagnostics(workdir: Path) -> Path` writing `workdir/diagnostics.md`
5. **[EXECUTION]** Wire `DiagnosticsCollector` into executor: on non-PASS step result, collect diagnostics; emit on pipeline failure
6. **[EXECUTION]** Include `resume_guidance` from `resume_command()` (T03.12)
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "diagnostics_collector or diagnostics_emit" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0056/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "diagnostics_collector"` exits 0
- `DiagnosticsBundle` contains gate_failures, exit_code, missing_artifacts, resume_guidance
- `emit_diagnostics()` writes `diagnostics.md` to workdir with all collected fields
- Gate failure from G-003 shows missing section name in diagnostic message

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "diagnostics_emit" -v` — diagnostics.md content verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0056/spec.md` produced

**Dependencies:** T04.03 (GateFailure dataclass), T03.12 (resume_command), T03.11 (return-contract)
**Rollback:** Remove `diagnostics.py`; revert executor wiring

---

### T09.04 -- Finalize execution-log.jsonl and execution-log.md with Complete Event Coverage

| Field | Value |
|---|---|
| Roadmap Item IDs | R-061 |
| Why | The skeleton from Phase 3 only logged step start/end; complete event coverage adds gate evaluations, convergence transitions, and signal events needed for post-run diagnosis |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0057 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0057/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/logging_.py` complete: events logged to `execution-log.jsonl` and `execution-log.md` including step_start, step_end, gate_eval, gate_fail, convergence_transition, signal_received, budget_warning, pipeline_outcome (NFR-007)

**Steps:**
1. **[PLANNING]** Load existing `logging_.py`; list event types present vs. missing
2. **[EXECUTION]** Define event schema: `{timestamp, event_type, step_id, data: dict}`
3. **[EXECUTION]** Add missing event types: `gate_eval`, `gate_fail`, `convergence_transition`, `signal_received`, `budget_warning`
4. **[EXECUTION]** Wire `gate_eval` logging into gate check in `executor.py`
5. **[EXECUTION]** Wire `convergence_transition` logging into `ConvergenceLoop` state changes
6. **[EXECUTION]** Wire `budget_warning` logging into `TurnLedger.can_launch()` when budget < 10% remaining
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "logging_complete or log_events" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0057/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "log_events"` exits 0
- `execution-log.jsonl` contains `gate_eval` event after each gate check
- `execution-log.jsonl` contains `convergence_transition` event on each state change
- `execution-log.md` human-readable format mirrors jsonl content
- All event types have `timestamp` (ISO-8601), `event_type`, and `step_id` fields

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "logging_complete" -v` — all 8 event types verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0057/spec.md` produced

**Dependencies:** T03.13 (logging skeleton), T08.01 (ConvergenceLoop for transition events), T04.01 (gates for gate_eval events)
**Rollback:** Revert `logging_.py` to Phase 3 skeleton

---

### Checkpoint: End of Phase 9

**Purpose:** Verify complete observability infrastructure — TUI, monitor, diagnostics, and logging — is operational before CLI integration and final verification.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P09-END.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "tui_complete or monitor_complete or diagnostics or log_events" -v` exits 0
- All 8 OutputMonitor fields confirmed (NFR-009)
- Diagnostics.md emitted on pipeline failure with gate failure reason and resume guidance

**Exit Criteria:**
- All 4 Phase 9 tasks complete with D-0054 through D-0057 artifacts
- Milestone M8: Failures diagnosable without re-reading raw artifacts; TUI provides real-time progress
- Logging covers all 8 event types with consistent schema
