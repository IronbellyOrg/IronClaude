# Phase 5 -- Sprint Integration

Wire the wiring analysis into the sprint executor with mode-aware behavior (off/shadow/soft/full), validated independently from roadmap integration. This phase achieves milestone M3b: sprint execution honors shadow/soft/full semantics without regressions.

### T05.01 -- Add wiring_gate_mode Field to SprintConfig in sprint/models.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-026 |
| Why | Sprint executor needs a configuration field to control wiring gate behavior per task execution, defaulting to shadow mode per section 5.8 |
| Effort | S |
| Risk | Medium |
| Risk Drivers | schema (model field addition), compliance (section 5.8) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0023/spec.md

**Deliverables:**
- `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` field added to `SprintConfig` dataclass in `src/superclaude/cli/sprint/models.py`

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/sprint/models.py` to locate `SprintConfig` dataclass and understand existing field patterns
2. **[PLANNING]** Verify OQ-4 decision (SprintConfig.source_dir existence) from Phase 1 decision log
3. **[EXECUTION]** Add `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` field to `SprintConfig`
4. **[EXECUTION]** Add `from typing import Literal` import if not already present
5. **[VERIFICATION]** Verify `SprintConfig(wiring_gate_mode="shadow")` instantiates without errors and default is "shadow"
6. **[COMPLETION]** Document field semantics: off=disabled, shadow=log only, soft=warn on critical, full=block on critical+major

**Acceptance Criteria:**
- `SprintConfig` accepts `wiring_gate_mode` parameter with type `Literal["off", "shadow", "soft", "full"]`
- Default value is `"shadow"` when not specified
- Existing `SprintConfig` instantiations continue to work without modification (backward compatible)
- Field is accessible as `config.wiring_gate_mode` with correct type

**Validation:**
- `uv run pytest tests/ -k "sprint_config" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0023/spec.md

**Dependencies:** Phase 4 validated (roadmap integration stable before touching sprint hot path)
**Rollback:** Remove `wiring_gate_mode` field from `SprintConfig`

---

### T05.02 -- Implement Sprint Post-Task Wiring Hook in sprint/executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027 |
| Why | G-005 requires the sprint executor to apply wiring analysis after each task with behavior determined by the configured gate mode |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance (sprint hot path per R4), pipeline (executor modification) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0024, D-0049 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0024/spec.md
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0049/spec.md

**Deliverables:**
- Post-task wiring hook in `src/superclaude/cli/sprint/executor.py` that runs `run_wiring_analysis()` after each task and applies mode-aware behavior
- Mode-aware behavior: off=skip, shadow=log findings without affecting task status, soft=warn on critical findings, full=block task on critical+major findings

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/sprint/executor.py` to identify the post-task hook injection point
2. **[PLANNING]** Read section 5.8 for sprint hook behavior specification and R4 performance constraints (<2s target, <5s hard budget)
3. **[EXECUTION]** Add post-task hook that checks `config.wiring_gate_mode`; if "off", return immediately
4. **[EXECUTION]** For shadow/soft/full: call `run_wiring_analysis()` with task source files, log findings
5. **[EXECUTION]** Implement mode-aware response: shadow=log only, soft=emit warning on critical, full=raise/return failure on critical+major
6. **[EXECUTION]** Short-circuit on excluded/skipped files per R4 performance mitigation
7. **[VERIFICATION]** Run `uv run pytest tests/integration/ -k "sprint_wiring_hook" -v` to validate all 4 modes
8. **[COMPLETION]** Document performance characteristics and mode behavior in function docstring

**Acceptance Criteria:**
- Sprint hook respects `wiring_gate_mode`: off skips analysis, shadow logs without affecting status (SC-006), soft warns, full blocks
- Hook execution completes in <5s for typical task scope (R4 hard budget)
- Task status is unchanged when running in shadow mode with findings present (SC-006)
- Import path is `from superclaude.cli.audit.wiring_gate import run_wiring_analysis` (not from pipeline)

**Validation:**
- `uv run pytest tests/integration/ -k "sprint_wiring_hook" -v` exits 0 with all mode tests passing
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0024/spec.md

**Dependencies:** T05.01 (SprintConfig field), T02.03-T02.05 (analyzers)
**Rollback:** Remove post-task hook from sprint/executor.py

---

### T05.03 -- Implement Pre-Activation Safeguards in sprint/executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | SC-010 and section 7 Phase 1 checklist require sanity checks before wiring analysis activates: >50 files must produce >0 findings to prevent misconfigured silent failures |
| Effort | S |
| Risk | Medium |
| Risk Drivers | compliance (SC-010, section 7 Phase 1 checklist) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0025/spec.md

**Deliverables:**
- Pre-activation safeguard checks in sprint executor: (1) zero-match warning when >50 files scanned but 0 findings produced, (2) whitelist validation confirming whitelist file is parseable, (3) `provider_dir_names` configuration sanity check

**Steps:**
1. **[PLANNING]** Read SC-010, section 7 Phase 1 checklist, and R5 mitigation for safeguard requirements
2. **[PLANNING]** Identify where safeguards run: before first wiring analysis in a sprint session
3. **[EXECUTION]** Implement zero-match warning: if `files_scanned > 50` and `len(findings) == 0`, emit WARNING log with operator-visible message
4. **[EXECUTION]** Implement whitelist validation: attempt to load whitelist file at startup, log WARNING if parse fails
5. **[EXECUTION]** Implement `provider_dir_names` check: verify configured directories exist, log WARNING if any are missing
6. **[VERIFICATION]** Run `uv run pytest tests/integration/ -k "safeguard" -v` with intentionally misconfigured provider_dir_names
7. **[COMPLETION]** Document safeguard behaviors in function docstring

**Acceptance Criteria:**
- Running with misconfigured `provider_dir_names` (pointing to nonexistent directory) produces a WARNING log message (SC-010)
- Zero-match warning emitted when >50 files scanned but 0 findings produced
- Invalid whitelist YAML produces a WARNING log at sprint startup without crashing
- Safeguard checks do not block sprint execution; they only produce warnings

**Validation:**
- `uv run pytest tests/integration/ -k "safeguard" -v` exits 0 with warning verification
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0025/spec.md

**Dependencies:** T05.02 (sprint hook), T02.01 (WiringConfig, whitelist loading)
**Rollback:** Remove safeguard check functions from sprint/executor.py

---

### T05.04 -- Implement Integration Tests for Sprint Hook with All 4 Mode Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029, R-030 |
| Why | SC-006 requires integration proof that sprint task status is unchanged with shadow findings, and all 4 modes (off/shadow/soft/full) must be validated independently |
| Effort | M |
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
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0026/evidence.md

**Deliverables:**
- `tests/integration/test_sprint_wiring.py` with >=4 integration tests: (1) off mode skips analysis entirely, (2) shadow mode logs findings without changing task status (SC-006), (3) soft mode warns on critical findings, (4) full mode blocks on critical+major findings

**Steps:**
1. **[PLANNING]** Review SC-006 and section 5.8 sprint integration validation requirements
2. **[PLANNING]** Design test fixtures with known findings (critical, major, minor severity mix)
3. **[EXECUTION]** Write test_off_mode: configure `wiring_gate_mode="off"`, run task, verify no wiring analysis executed
4. **[EXECUTION]** Write test_shadow_mode: configure `wiring_gate_mode="shadow"`, run task with critical findings, verify task status unchanged (SC-006)
5. **[EXECUTION]** Write test_soft_mode: configure `wiring_gate_mode="soft"`, run task with critical findings, verify warning emitted
6. **[EXECUTION]** Write test_full_mode: configure `wiring_gate_mode="full"`, run task with critical+major findings, verify task blocked
7. **[VERIFICATION]** Run `uv run pytest tests/integration/test_sprint_wiring.py -v` and verify all 4 tests pass
8. **[COMPLETION]** Record test results and verify no performance regression on task execution path

**Acceptance Criteria:**
- `uv run pytest tests/integration/test_sprint_wiring.py -v` exits 0 with >=4 tests passing
- Shadow mode test confirms task status unchanged with findings present (SC-006)
- Full mode test confirms task blocked when critical+major findings exist
- No performance regression: test execution completes within normal time bounds

**Validation:**
- `uv run pytest tests/integration/test_sprint_wiring.py -v` exits 0 with >=4 tests passing
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0026/evidence.md

**Dependencies:** T05.01, T05.02, T05.03
**Rollback:** Delete `tests/integration/test_sprint_wiring.py`

---

### Checkpoint: End of Phase 5

**Purpose:** Validate milestone M3b: sprint execution honors shadow/soft/full semantics without regressions.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P05-END.md
**Verification:**
- Sprint hook logs findings without affecting task status in shadow mode (SC-006)
- Sprint hook warns on critical findings in soft mode
- Sprint hook blocks on critical+major findings in full mode
**Exit Criteria:**
- `uv run pytest tests/integration/test_sprint_wiring.py -v` exits 0 with >=4 tests passing
- No performance regression on task execution path (<5s hard budget per R4)
- Pre-activation safeguards emit warnings for misconfigured provider_dir_names (SC-010)
