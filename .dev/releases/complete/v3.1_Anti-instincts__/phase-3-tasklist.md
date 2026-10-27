# Phase 3 -- Sprint Integration & Rollout Mode

Wire the anti-instinct gate into the sprint executor with rollout mode control (`off`/`shadow`/`soft`/`full`) and TurnLedger integration. Ships with `gate_rollout_mode=off` — gate evaluates but result is ignored until shadow validation confirms accuracy. Milestone M3: sprint executor supports `gate_rollout_mode` for anti-instinct with shadow metrics recording.

---

### T03.01 -- Extend `SprintConfig` with `gate_rollout_mode`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | The rollout mode field controls anti-instinct gate behavior in sprint context, defaulting to `off` for backward compatibility per NFR-006. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0018/spec.md`

**Deliverables:**
1. `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` field added to `SprintConfig` in `src/superclaude/cli/sprint/models.py` (FR-SPRINT.1)

**Steps:**
1. **[PLANNING]** Read current `src/superclaude/cli/sprint/models.py` to identify `SprintConfig` dataclass/model fields
2. **[PLANNING]** Confirm `Literal` type import is available; verify default `"off"` causes no behavioral change
3. **[EXECUTION]** Add `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` to `SprintConfig`
4. **[EXECUTION]** Verify field serializes/deserializes correctly in existing config loading paths
5. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` to verify no regression
6. **[COMPLETION]** Record implementation evidence to D-0018/spec.md

**Acceptance Criteria:**
- `SprintConfig` in `src/superclaude/cli/sprint/models.py` contains `gate_rollout_mode` field with `Literal["off", "shadow", "soft", "full"]` type and `"off"` default
- Default `"off"` causes zero behavioral change in existing sprint execution (NFR-006)
- Field is accessible from sprint executor context
- Existing sprint config loading and validation passes without modification

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0 (no regression)
- Evidence: models.py diff archived to D-0018/spec.md

**Dependencies:** None (model change is independent)
**Rollback:** Revert `models.py` to pre-edit state (git checkout)

---

### T03.02 -- Wire Anti-Instinct Gate in Sprint Executor

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | Sprint executor wiring implements the rollout mode behavior matrix, TurnLedger credit/remediation, ShadowGateMetrics recording, and KPI aggregation — the core sprint-side integration for anti-instinct enforcement. |
| Effort | L |
| Risk | High |
| Risk Drivers | breaking change (sprint executor), system-wide (rollout modes), performance (gate evaluation latency), rollback (remediation/budget logic) |
| Tier | STRICT |
| Confidence | [█████████░] 92% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0019, D-0020, D-0021, D-0022 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0019/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0020/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0021/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0022/spec.md`

**Deliverables:**
1. Rollout mode behavior matrix in `src/superclaude/cli/sprint/executor.py`: `off` (evaluate, ignore result), `shadow` (evaluate, record metrics), `soft` (evaluate, record, credit/remediate), `full` (evaluate, record, credit/remediate, fail task) (FR-SPRINT.3)
2. `ShadowGateMetrics.record(passed, evaluation_ms)` integration called in shadow/soft/full modes (FR-SPRINT.4)
3. TurnLedger credit on PASS (`ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))`), remediation + `BUDGET_EXHAUSTED` on FAIL (soft/full), `TaskResult.status = FAIL` on FAIL (full only) — all TurnLedger calls guarded with `if ledger is not None` (FR-SPRINT.3, FR-SPRINT.5, NFR-007)
4. Anti-instinct trailing-gate results fed into `build_kpi_report()` / `GateKPIReport` in sprint context (FR-SPRINT.4)

**Steps:**
1. **[PLANNING]** Read current `src/superclaude/cli/sprint/executor.py` to identify gate evaluation flow, `_all_gate_results`, and TurnLedger usage patterns
2. **[PLANNING]** Identify `TrailingGateResult`, `ShadowGateMetrics`, `GateKPIReport`, and `build_kpi_report()` interfaces
3. **[EXECUTION]** Wrap anti-instinct gate result in `TrailingGateResult(passed, evaluation_ms, gate_name)` and submit to `_all_gate_results` (FR-SPRINT.2)
4. **[EXECUTION]** Implement rollout mode behavior matrix: `off` ignores, `shadow` records, `soft` records+credits/remediates, `full` records+credits/remediates+fails (FR-SPRINT.3)
5. **[EXECUTION]** Add `ShadowGateMetrics.record()` calls for shadow/soft/full modes and integrate into KPI aggregation (FR-SPRINT.4)
6. **[EXECUTION]** Guard ALL TurnLedger calls with `if ledger is not None` including credit and remediation paths (FR-SPRINT.5, NFR-007)
7. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` to verify no regression; verify None-safe ledger guards
8. **[COMPLETION]** Record implementation evidence to D-0019 through D-0022 spec.md files

**Acceptance Criteria:**
- Sprint executor implements all 4 rollout modes per the behavior matrix table in the roadmap
- `ShadowGateMetrics.record(passed, evaluation_ms)` called in shadow, soft, and full modes (not in off mode)
- ALL TurnLedger calls (credit, remediation) guarded with `if ledger is not None` — sprint runs without TurnLedger must not raise
- Anti-instinct and wiring-integrity gates evaluate independently (NFR-010): no shared state between gate evaluations

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0 (no regression)
- Evidence: executor.py diff archived to D-0019/spec.md

**Dependencies:** T03.01, T02.02 (executor integration artifacts must exist)
**Rollback:** Revert `sprint/executor.py` to pre-edit state (git checkout)
**Notes:** Highest coordination-risk edit in Phase 3. TurnLedger None-safe guards are critical for standalone mode (NFR-007).

---

### T03.03 -- Write Sprint Integration Tests for Anti-Instinct

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | Sprint integration tests validate the rollout mode matrix, None-safe ledger guards, ShadowGateMetrics recording, gate independence, and full pipeline flow with reimbursement path. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | end-to-end (sprint pipeline), system-wide, performance |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0023, D-0024, D-0025 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0023/evidence.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0024/evidence.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0025/evidence.md`

**Deliverables:**
1. `tests/sprint/test_anti_instinct_sprint.py` — rollout mode matrix tests: all 4 modes (off/shadow/soft/full) x pass/fail scenarios, None-safe ledger guards (standalone mode without TurnLedger), independent gate evaluation (anti-instinct and wiring-integrity do not interact per NFR-010)
2. `tests/sprint/test_shadow_mode.py` — ShadowGateMetrics recording tests: verify metrics recorded in shadow/soft/full modes, verify no recording in off mode, verify data point structure
3. `tests/pipeline/test_full_flow.py` — full pipeline flow tests: reimbursement path (credit on pass), remediation path (BUDGET_EXHAUSTED on fail), TaskResult.status=FAIL in full mode

**Steps:**
1. **[PLANNING]** Identify sprint executor test invocation API and fixture patterns
2. **[PLANNING]** Prepare test configurations for each rollout mode and pass/fail scenario
3. **[EXECUTION]** Write `test_anti_instinct_sprint.py`: 8 tests for 4 modes x pass/fail plus None-safe ledger guards and gate independence
4. **[EXECUTION]** Write `test_shadow_mode.py`: verify ShadowGateMetrics recording per mode
5. **[EXECUTION]** Write `test_full_flow.py`: verify credit/remediation/fail paths end-to-end
6. **[VERIFICATION]** Run `uv run pytest tests/sprint/ tests/pipeline/ -v`
7. **[COMPLETION]** Record test results to D-0023, D-0024, D-0025 evidence.md files

**Acceptance Criteria:**
- `tests/sprint/test_anti_instinct_sprint.py` covers all 4 modes x pass/fail (8 scenarios minimum) plus None-safe ledger test
- `tests/sprint/test_shadow_mode.py` verifies recording in shadow/soft/full and no recording in off mode
- `tests/pipeline/test_full_flow.py` verifies credit on pass, BUDGET_EXHAUSTED on fail, TaskResult.status=FAIL in full mode
- `uv run pytest tests/sprint/ tests/pipeline/ -v` exits 0 with all tests passing
- `wiring_gate_mode` behavior is unaffected by anti-instinct gate configuration (no interaction verified by test)

**Validation:**
- `uv run pytest tests/sprint/ tests/pipeline/ -v` exits 0
- Evidence: test output logs archived to D-0023, D-0024, D-0025 evidence.md files

**Dependencies:** T03.02
**Rollback:** Delete test files

---

### Checkpoint: End of Phase 3

**Purpose:** Validate rollout readiness (Checkpoint B): sprint pipeline runs with shadow mode, metrics recording confirmed, no merge conflicts, audit outputs explain failures clearly.
**Checkpoint Report Path:** `.dev/releases/current/v3.1_Anti-instincts__/checkpoints/CP-P03-END.md`
**Verification:**
- Sprint pipeline runs with `gate_rollout_mode=shadow` and records `ShadowGateMetrics` (SC-008 baseline)
- Zero merge conflicts with TurnLedger (SC-009)
- `uv run pytest` (full test suite) exits 0 with zero regressions (SC-007)
**Exit Criteria:**
- All 3 tasks (T03.01-T03.03) completed with deliverables D-0018 through D-0025 produced
- Anti-instinct audit output includes human-readable failure explanations
- Anti-instinct and wiring-integrity gates evaluate independently (NFR-010 verified)
- cli-portify regression case passes end-to-end (Checkpoint B requirement)
