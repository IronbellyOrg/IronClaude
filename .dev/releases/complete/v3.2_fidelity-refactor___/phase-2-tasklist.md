# Phase 2 -- Sprint Integration

Wire the analysis engine into the sprint execution loop with budget tracking and enforcement modes. Implement TurnLedger extensions (debit/credit/floor-to-zero), SprintConfig fields with migration shim, and the `run_post_task_wiring_hook()` with BLOCKING/SHADOW/SOFT mode paths. All work requires Phase 1 complete and OQ-2/OQ-6 prerequisites resolved.

---

### T02.01 -- Resolve Phase 2 Entry Prerequisites (OQ-2, OQ-6)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016, R-017 |
| Why | Phase 2 work cannot begin until WIRING_ANALYSIS_TURNS/REMEDIATION_COST budget constants and SprintGatePolicy constructor compatibility are resolved as explicit entry gates. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0011/spec.md`

**Deliverables:**
1. Decision record documenting OQ-2 resolution: conservative defaults (`WIRING_ANALYSIS_TURNS=1`, `REMEDIATION_COST=2`) with SprintConfig overrides and rationale
2. Decision record documenting OQ-6 resolution: `trailing_gate.py` source read, SprintGatePolicy constructor requirements validated, interface contract documented

**Steps:**
1. **[PLANNING]** Read roadmap OQ-2 and OQ-6 recommended resolutions
2. **[PLANNING]** Read `src/superclaude/cli/sprint/` source to validate SprintGatePolicy constructor signature in `trailing_gate.py`
3. **[EXECUTION]** Document OQ-2 resolution: set `WIRING_ANALYSIS_TURNS=1`, `REMEDIATION_COST=2` as defaults with SprintConfig override mechanism
4. **[EXECUTION]** Document OQ-6 resolution: record SprintGatePolicy constructor requirements and interface contract
5. **[COMPLETION]** Write decision record to D-0011/spec.md

**Acceptance Criteria:**
- File `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0011/spec.md` exists with resolutions for both OQ-2 and OQ-6
- OQ-2 specifies exact default values and SprintConfig override field names
- OQ-6 documents SprintGatePolicy constructor signature validated against actual source
- Both resolutions are traceable to roadmap Phase 2 Entry Prerequisites table

**Validation:**
- Manual check: decision record matches roadmap recommended resolutions for OQ-2 and OQ-6
- Evidence: decision record artifact produced at D-0011/spec.md

**Dependencies:** Phase 1 complete (T01.01-T01.08)
**Rollback:** Delete D-0011/spec.md

---

### T02.02 -- Implement TurnLedger Extensions

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018, R-019, R-020, R-021 |
| Why | TurnLedger must track wiring analysis budget consumption with debit-before-analysis and floor-to-zero credit arithmetic to enable budget-aware gate enforcement. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | database (model modification), migration (field additions) |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0012/spec.md`

**Deliverables:**
1. TurnLedger extensions in `src/superclaude/cli/sprint/models.py`: 3 new fields (defaulting to zero per NFR-004), `debit_wiring()`, `credit_wiring()` with floor-to-zero arithmetic, and `can_run_wiring_gate()`

**Steps:**
1. **[PLANNING]** Read T02.01 decision record for OQ-2 budget constant values; read current `sprint/models.py` TurnLedger implementation
2. **[PLANNING]** Confirm NFR-004 (all new fields default to zero) and R7 risk (floor-to-zero is by design)
3. **[EXECUTION]** Add 3 new fields to TurnLedger dataclass (names per T02.01 decision record, e.g. `wiring_turns_used`, `wiring_turns_credited`, `wiring_budget_exhausted`), all defaulting to 0
4. **[EXECUTION]** Implement `debit_wiring()` method: debit before analysis, decrement available turns
5. **[EXECUTION]** Implement `credit_wiring(turns, rate)` with explicit floor-to-zero: `int(turns * rate)` where `credit_wiring(1, 0.8)` MUST return 0 credits
6. **[EXECUTION]** Implement `can_run_wiring_gate()` method: check if budget allows analysis
7. **[VERIFICATION]** Verify `credit_wiring(1, 0.8)` returns 0; all fields default to zero; debit/credit tracking is accurate
8. **[COMPLETION]** Record implementation details to D-0012/spec.md

**Acceptance Criteria:**
- `sprint/models.py` contains 3 new TurnLedger fields all defaulting to 0 (NFR-004)
- `credit_wiring(1, 0.8)` returns exactly 0 credits (`int(1 * 0.8)` = 0) — explicit floor-to-zero by design (R7)
- `debit_wiring()` decrements available turns before analysis runs
- `can_run_wiring_gate()` returns boolean based on remaining budget

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py tests/sprint/ -k "debit or credit or budget" -v`
- Evidence: linkable artifact produced at D-0012/spec.md

**Dependencies:** T02.01
**Rollback:** Revert TurnLedger field additions and methods from `sprint/models.py`

---

### T02.03 -- Implement SprintConfig Fields and Migration Shim

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022, R-023 |
| Why | SprintConfig needs wiring gate configuration fields with a backward-compatible migration shim that emits deprecation warnings for renamed fields. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration (config field rename), schema (SprintConfig extension) |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0013/spec.md`

**Deliverables:**
1. 3 SprintConfig fields and `__post_init__` migration shim with deprecation warning in `src/superclaude/cli/sprint/models.py` (NFR-007: shim scoped to 1 release)

**Steps:**
1. **[PLANNING]** Read current SprintConfig in `sprint/models.py`; identify field naming conventions
2. **[PLANNING]** Review R8 risk mitigation: `__post_init__` migration shim with deprecation warning, scoped to 1 release (NFR-007)
3. **[EXECUTION]** Add 3 SprintConfig fields: `wiring_gate_scope`, `wiring_analysis_turns`, `remediation_cost` (inputs to `resolve_gate_mode()` per Goal-5d) with defaults from OQ-2 resolution
4. **[EXECUTION]** Implement `__post_init__` migration shim: detect old field names, copy values to new fields, emit `warnings.warn()` deprecation
5. **[VERIFICATION]** Verify old field names trigger deprecation warning and values migrate correctly; new fields have correct defaults
6. **[COMPLETION]** Record implementation details to D-0013/spec.md

**Acceptance Criteria:**
- `sprint/models.py` contains 3 new SprintConfig fields with defaults matching OQ-2 resolution
- `__post_init__` migration shim emits deprecation warning when old field names are used (R8 mitigation)
- Migration shim is clearly marked for removal after 1 release (NFR-007)
- New field defaults match T02.01 decision record values

**Validation:**
- `uv run pytest tests/sprint/ -k "config or migration or deprecation" -v`
- Evidence: linkable artifact produced at D-0013/spec.md

**Dependencies:** T02.01, T02.02
**Rollback:** Revert SprintConfig field additions and migration shim from `sprint/models.py`

---

### T02.04 -- Implement run_post_task_wiring_hook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | The hook function is the central integration point that invokes wiring analysis after each sprint task, managing mode resolution, budget tracking, and enforcement dispatch. |
| Effort | L |
| Risk | High |
| Risk Drivers | auth (callable-based remediation interface), cross-cutting (executor + ledger + gate interaction), pipeline |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0014/spec.md`

**Deliverables:**
1. `run_post_task_wiring_hook()` function in `src/superclaude/cli/sprint/executor.py` with `resolve_gate_mode(scope, grace_period)` for mode resolution and callable-based remediation interface (`can_remediate`, `debit`) avoiding TurnLedger import in trailing_gate.py (Constraint 7). Includes helper functions required by the hook (FR: T07b-f). Null-ledger compatibility is split to T02.07 per FR: T07b-e.

**Steps:**
1. **[PLANNING]** Read current `sprint/executor.py` structure; identify hook insertion point in post-task pipeline
2. **[PLANNING]** Review Constraint 7 (callable-based interface), Goal-5d (resolve_gate_mode replaces string-switch), NFR-006 (zero modifications to pipeline/ files)
3. **[EXECUTION]** Implement `run_post_task_wiring_hook()` with mode resolution via `resolve_gate_mode(scope, grace_period)`
4. **[EXECUTION]** Implement callable-based remediation interface: accept `can_remediate` and `debit` callables to avoid coupling to TurnLedger
5. **[EXECUTION]** Wire hook into executor post-task pipeline; implement budget check via `can_run_wiring_gate()` before analysis
6. **[VERIFICATION]** Verify hook dispatches correctly to BLOCKING/SHADOW/SOFT paths; verify no imports added to pipeline/ files
7. **[COMPLETION]** Record implementation details to D-0014/spec.md

**Acceptance Criteria:**
- `run_post_task_wiring_hook()` exists in `src/superclaude/cli/sprint/executor.py` with mode resolution via `resolve_gate_mode()`
- Callable-based remediation interface avoids importing TurnLedger into trailing_gate.py (Constraint 7)
- Hook checks `can_run_wiring_gate()` before running analysis (debit-before-analysis budget model)
- Zero modifications to `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py` (NFR-006)

**Validation:**
- `uv run pytest tests/sprint/ -k "wiring_hook" -v`
- Evidence: linkable artifact produced at D-0014/spec.md

**Dependencies:** T02.02, T02.03
**Rollback:** Remove `run_post_task_wiring_hook()` from `sprint/executor.py`

---

### Checkpoint: Phase 2 / Tasks T02.01-T02.05

**Purpose:** Verify TurnLedger extensions and hook function are implemented before mode-specific path tests.
**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/CP-P02-T01-T05.md`
**Verification:**
- TurnLedger has 3 new fields, `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()` all functional
- SprintConfig has 3 new fields with migration shim emitting deprecation warnings
- `run_post_task_wiring_hook()` dispatches to mode-specific paths
**Exit Criteria:**
- `credit_wiring(1, 0.8)` returns 0 (floor-to-zero verified)
- All new fields default to zero (NFR-004 verified)
- Hook function callable without errors in isolated test context

---

### T02.05 -- Implement BLOCKING Mode Path

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025 |
| Why | BLOCKING mode causes sprint task failure on wiring defect detection and triggers remediation via the callable interface, enabling enforcement after shadow/soft validation. |
| Effort | M |
| Risk | High |
| Risk Drivers | breaking (task failure behavior), pipeline (sprint execution flow) |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0015/spec.md`

**Deliverables:**
1. BLOCKING mode path in `src/superclaude/cli/sprint/executor.py`: fail sprint task on findings, invoke `can_remediate`/`debit` callable pair for remediation (Goal-5c)

**Steps:**
1. **[PLANNING]** Read Goal-5c requirements and remediation callable interface from T02.04
2. **[PLANNING]** Review budget debit semantics for remediation turns
3. **[EXECUTION]** Implement BLOCKING branch in `run_post_task_wiring_hook()`: on findings, fail task and invoke remediation callable
4. **[EXECUTION]** Implement remediation budget debit via `debit` callable; handle budget exhaustion (BUDGET_EXHAUSTED state)
5. **[VERIFICATION]** Verify BLOCKING mode fails task on findings and invokes remediation; verify budget exhaustion handled
6. **[COMPLETION]** Record implementation details to D-0015/spec.md

**Acceptance Criteria:**
- BLOCKING mode path in `sprint/executor.py` fails sprint task when wiring findings are detected (Goal-5c)
- Remediation invoked via callable interface (`can_remediate`, `debit`) without direct TurnLedger coupling
- Budget exhaustion produces BUDGET_EXHAUSTED state without crashing
- Mode path is functionally distinct from SHADOW and SOFT paths

**Validation:**
- `uv run pytest tests/sprint/ -k "blocking" -v`
- Evidence: linkable artifact produced at D-0015/spec.md

**Dependencies:** T02.04
**Rollback:** Remove BLOCKING branch from `run_post_task_wiring_hook()`

---

### T02.06 -- Implement SHADOW Mode Path

| Field | Value |
|---|---|
| Roadmap Item IDs | R-026 |
| Why | SHADOW mode logs wiring analysis results without interfering with sprint execution, providing baseline data collection for rollout validation. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0016/spec.md`

**Deliverables:**
1. SHADOW mode path in `src/superclaude/cli/sprint/executor.py`: log-only, non-interfering analysis that records findings without affecting sprint task status (Goal-5a)

**Steps:**
1. **[PLANNING]** Read Goal-5a requirements for shadow/log-only mode
2. **[EXECUTION]** Implement SHADOW branch in `run_post_task_wiring_hook()`: run analysis, log findings, do not modify task status
3. **[EXECUTION]** Implement deferred log recording for shadow findings (DeferredRemediationLog integration)
4. **[VERIFICATION]** Verify SHADOW mode does not affect sprint task pass/fail status; findings are logged
5. **[COMPLETION]** Record implementation details to D-0016/spec.md

**Acceptance Criteria:**
- SHADOW mode path in `sprint/executor.py` runs analysis and logs findings without affecting task status (Goal-5a)
- Findings recorded via deferred log for later analysis
- Sprint task pass/fail status is identical with and without SHADOW mode enabled (non-interference)
- Mode path is functionally distinct from BLOCKING and SOFT paths

**Validation:**
- `uv run pytest tests/sprint/ -k "shadow" -v`
- Evidence: linkable artifact produced at D-0016/spec.md

**Dependencies:** T02.04
**Rollback:** Remove SHADOW branch from `run_post_task_wiring_hook()`

---

### T02.07 -- Implement SOFT Mode and Null-Ledger Compatibility

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027, R-028 |
| Why | SOFT mode surfaces warnings without failing tasks, and null-ledger compatibility ensures the hook functions correctly when no TurnLedger is provided (legacy path). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | breaking (warning surfacing), rollback (null-ledger path must match prior behavior) |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0017/spec.md`

**Deliverables:**
1. SOFT mode path and null-ledger compatibility in `src/superclaude/cli/sprint/executor.py`: warning surfacing without task failure (Goal-5b) and `ledger is None` path matching prior behavior exactly (NFR-004)

**Steps:**
1. **[PLANNING]** Read Goal-5b (SOFT mode) and NFR-004 (null-ledger compat) requirements
2. **[PLANNING]** Identify current `ledger is None` behavior to ensure exact match
3. **[EXECUTION]** Implement SOFT branch in `run_post_task_wiring_hook()`: surface findings as warnings without failing task (Goal-5b)
4. **[EXECUTION]** Implement null-ledger guard: when `ledger is None`, skip budget operations, match prior behavior exactly
5. **[VERIFICATION]** Verify SOFT mode surfaces warnings without task failure; verify `ledger is None` path produces identical behavior to pre-hook state
6. **[COMPLETION]** Record implementation details to D-0017/spec.md

**Acceptance Criteria:**
- SOFT mode path in `sprint/executor.py` surfaces findings as warnings without failing sprint task (Goal-5b)
- `ledger is None` path matches prior behavior exactly — no budget operations, no crashes (NFR-004)
- SOFT mode is functionally distinct from SHADOW (warnings visible to user) and BLOCKING (no task failure)
- Null-ledger compatibility tested with explicit assertion of behavioral equivalence

**Validation:**
- `uv run pytest tests/sprint/ -k "soft or null_ledger" -v`
- Evidence: linkable artifact produced at D-0017/spec.md

**Dependencies:** T02.04
**Rollback:** Remove SOFT branch and null-ledger guard from `run_post_task_wiring_hook()`

---

### T02.08 -- Write TurnLedger Unit Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029, R-030 |
| Why | Unit tests validate debit/credit tracking correctness and the critical floor-to-zero behavior that is by-design and must be explicitly asserted. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0018/evidence.md`

**Deliverables:**
1. 3 TurnLedger unit tests validating `debit_wiring`/`credit_wiring` tracking with explicit floor-to-zero assertion (SC-012, SC-013)

**Steps:**
1. **[PLANNING]** Review T02.02 implementation; identify critical edge cases including floor-to-zero
2. **[EXECUTION]** Write test: `debit_wiring()` correctly decrements available turns and prevents over-debit
3. **[EXECUTION]** Write test: `credit_wiring(1, 0.8)` returns 0 credits (explicit floor-to-zero assertion per R7)
4. **[EXECUTION]** Write test: sequential `debit_wiring()`/`credit_wiring()` cycle correctly tracks cumulative budget consumption
5. **[VERIFICATION]** `uv run pytest tests/sprint/ -k "debit or credit or budget" -v` exits 0 with all 3 tests passing
6. **[COMPLETION]** Record test results to D-0018/evidence.md

**Acceptance Criteria:**
- 3 TurnLedger tests exist validating `debit_wiring`/`credit_wiring` tracking semantics
- Floor-to-zero explicitly asserted: `credit_wiring(1, 0.8)` returns 0 (SC-012)
- `debit_wiring`/`credit_wiring` tracking validated (SC-013)
- `uv run pytest tests/sprint/ -k "debit or credit or budget" -v` exits 0

**Validation:**
- `uv run pytest tests/sprint/ -k "debit or credit or budget" -v`
- Evidence: test output log archived to D-0018/evidence.md

**Dependencies:** T02.02
**Rollback:** Delete TurnLedger test functions

---

### Checkpoint: End of Phase 2

**Purpose:** Gate for Phase 3 entry — verify sprint integration is complete with all mode paths functional and budget semantics proven.
**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/CP-P02-END.md`
**Verification:**
- Shadow, soft, and blocking branches are functionally distinct and testable
- `ledger is None` path matches prior behavior exactly (NFR-004)
- Budget debit/credit semantics proven with explicit floor-to-zero assertions (R7)
**Exit Criteria:**
- All 8 tasks (T02.01-T02.08) completed with deliverables D-0011 through D-0018 produced
- `run_post_task_wiring_hook()` dispatches correctly to all three mode paths
- Zero modifications to `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py` (NFR-006)
