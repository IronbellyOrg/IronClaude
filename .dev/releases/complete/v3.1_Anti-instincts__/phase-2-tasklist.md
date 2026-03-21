# Phase 2 -- Gate Definition, Executor Wiring & Prompt Hardening

Wire the four detection modules into the roadmap pipeline as the `anti-instinct` gate step, including prompt modifications to improve upstream plan quality. No sprint integration yet. Milestone M2: `anti-instinct` step executes between `merge` and `test-strategy` in standalone roadmap mode with prompts instructing explicit integration wiring.

---

### T02.01 -- Define `ANTI_INSTINCT_GATE` in `roadmap/gates.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | The gate definition formalizes the anti-instinct checks as a pipeline gate with STRICT enforcement tier, positioned between merge and test-strategy in the gate registry. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | breaking change (gate registry modification), system-wide (ALL_GATES ordering) |
| Tier | STRICT |
| Confidence | [█████████░] 92% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0011/spec.md`

**Deliverables:**
1. `ANTI_INSTINCT_GATE` definition added to `src/superclaude/cli/roadmap/gates.py` — `GateCriteria` with required frontmatter fields (`undischarged_obligations: int`, `uncovered_contracts: int`, `fingerprint_coverage: float`, `min_lines=10`, `gate_scope=GateScope.TASK`), three semantic checks (`_no_undischarged_obligations`, `_integration_contracts_covered`, `_fingerprint_coverage_check`), `enforcement_tier="STRICT"`, inserted into `ALL_GATES` between `merge` and `test-strategy`

**Steps:**
1. **[PLANNING]** Read current `src/superclaude/cli/roadmap/gates.py` to identify `ALL_GATES` structure and insertion point between `merge` and `test-strategy`
2. **[PLANNING]** Check for WIRING_GATE definition per T01.01 merge coordination plan; confirm additive-only insertion
3. **[EXECUTION]** Define `ANTI_INSTINCT_GATE` as `GateCriteria` with required frontmatter fields and `gate_scope=GateScope.TASK` (FR-GATE.1)
4. **[EXECUTION]** Implement `_no_undischarged_obligations` (assert == 0), `_integration_contracts_covered` (assert == 0), `_fingerprint_coverage_check` (assert >= 0.7) as semantic checks (FR-GATE.2)
5. **[EXECUTION]** Set `enforcement_tier="STRICT"` per NFR-005 and insert `("anti-instinct", ANTI_INSTINCT_GATE)` into `ALL_GATES` between `merge` and `test-strategy` (FR-GATE.3)
6. **[VERIFICATION]** Verify `gate_passed()` signature is unchanged (NFR-009); run existing gate tests to confirm no regression
7. **[COMPLETION]** Record implementation evidence to D-0011/spec.md

**Acceptance Criteria:**
- `ANTI_INSTINCT_GATE` exists in `src/superclaude/cli/roadmap/gates.py` with all three semantic checks and `enforcement_tier="STRICT"`
- `ALL_GATES` contains `("anti-instinct", ANTI_INSTINCT_GATE)` at the position between `merge` and `test-strategy`
- `gate_passed()` function signature is unchanged from pre-edit state (NFR-009)
- No merge conflicts with existing WIRING_GATE definition; changes are additive-only

**Validation:**
- `uv run pytest tests/roadmap/ -v` exits 0 (no regression in existing gate tests)
- Evidence: diff of gates.py showing additive-only changes archived to D-0011/spec.md

**Dependencies:** T01.02, T01.03, T01.04 (all detection modules must exist)
**Rollback:** Revert `gates.py` to pre-edit state (git checkout)
**Notes:** Coordinate with WIRING_GATE timing; both modify gates.py. Additive-only changes minimize conflict risk.

---

### T02.02 -- Integrate Anti-Instinct Step in `roadmap/executor.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | The executor integration wires the detection modules into the roadmap pipeline as a non-LLM step, producing the anti-instinct-audit.md artifact and preparing sprint-side integration exports. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | system-wide (pipeline step ordering), breaking change (step registry), pipeline |
| Tier | STRICT |
| Confidence | [█████████░] 92% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0012, D-0013, D-0014 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0012/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0013/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0014/spec.md`

**Deliverables:**
1. Anti-instinct step added to `_build_steps()` in `src/superclaude/cli/roadmap/executor.py` between `merge` and `test-strategy` with `timeout_seconds=30`, `retry_limit=0`, `gate=ANTI_INSTINCT_GATE`, `gate_scope=GateScope.TASK` (FR-EXEC.2)
2. `_run_anti_instinct_audit()` function: reads spec + merged roadmap, invokes obligation scanner + integration contracts + fingerprint checker, writes `anti-instinct-audit.md` with YAML frontmatter + markdown report (FR-EXEC.3)
3. Sprint-side integration artifacts exported: `TrailingGateResult`, `DeferredRemediationLog`, and `"anti-instinct"` maintained in `_get_all_step_ids()` between `"merge"` and `"test-strategy"` (FR-EXEC.4)

**Steps:**
1. **[PLANNING]** Read current `src/superclaude/cli/roadmap/executor.py` to identify `_build_steps()`, step ordering, and import structure
2. **[PLANNING]** Verify module imports for obligation_scanner, integration_contracts, fingerprint are available
3. **[EXECUTION]** Add `_run_structural_audit()` hook after EXTRACT_GATE pass, before generate steps — warning-only (FR-EXEC.1)
4. **[EXECUTION]** Add `anti-instinct` step to `_build_steps()` with specified timeout, retry, gate, and scope (FR-EXEC.2)
5. **[EXECUTION]** Implement `_run_anti_instinct_audit()` reading spec + merged roadmap, invoking all three modules, writing `anti-instinct-audit.md` with YAML frontmatter (FR-EXEC.3)
6. **[EXECUTION]** Add executor import/update bundle for `TrailingGateResult`, `DeferredRemediationLog`, and maintain `"anti-instinct"` in `_get_all_step_ids()` (FR-EXEC.4)
7. **[VERIFICATION]** Run `uv run pytest tests/roadmap/ -v` to verify no regression; verify anti-instinct step is non-LLM
8. **[COMPLETION]** Record implementation evidence to D-0012, D-0013, D-0014 spec.md files

**Acceptance Criteria:**
- `_build_steps()` contains `anti-instinct` step positioned between `merge` and `test-strategy` with `timeout_seconds=30`, `retry_limit=0`
- `_run_anti_instinct_audit()` invokes all three detection modules and writes `anti-instinct-audit.md` with YAML frontmatter containing `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage` fields
- Anti-instinct step is non-LLM: executor runs the audit function directly without LLM invocation
- `_get_all_step_ids()` returns list with `"anti-instinct"` between `"merge"` and `"test-strategy"`

**Validation:**
- `uv run pytest tests/roadmap/ -v` exits 0 (no regression)
- Evidence: executor.py diff and sample anti-instinct-audit.md output archived to D-0012/spec.md

**Dependencies:** T02.01
**Rollback:** Revert `executor.py` to pre-edit state (git checkout)

---

### T02.03 -- Add Prompt Blocks in `roadmap/prompts.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Prompt modifications improve upstream LLM plan quality by instructing explicit integration enumeration and wiring verification, reducing the work the deterministic gate must catch. |
| Effort | S |
| Risk | Low |
| Risk Drivers | cross-cutting (affects LLM output quality) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0015, D-0016 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0015/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0016/spec.md`

**Deliverables:**
1. `INTEGRATION_ENUMERATION_BLOCK` added to `build_generate_prompt()` in `src/superclaude/cli/roadmap/prompts.py` before `_OUTPUT_FORMAT_BLOCK` — instructs LLM to enumerate integration points with named artifacts, wired components, owning phase, cross-reference section (FR-PROMPT.1)
2. `INTEGRATION_WIRING_DIMENSION` added as dimension 6 to `build_spec_fidelity_prompt()` after dimension 5 — instructs LLM to verify wiring tasks for dispatch tables, registries, DI points (FR-PROMPT.2)

**Steps:**
1. **[PLANNING]** Read current `src/superclaude/cli/roadmap/prompts.py` to identify `build_generate_prompt()` structure and `_OUTPUT_FORMAT_BLOCK` position
2. **[PLANNING]** Identify `build_spec_fidelity_prompt()` dimension ordering (currently 5 dimensions)
3. **[EXECUTION]** Add `INTEGRATION_ENUMERATION_BLOCK` constant and insert into `build_generate_prompt()` before `_OUTPUT_FORMAT_BLOCK` (FR-PROMPT.1)
4. **[EXECUTION]** Add `INTEGRATION_WIRING_DIMENSION` constant and insert as dimension 6 into `build_spec_fidelity_prompt()` after dimension 5 (FR-PROMPT.2)
5. **[VERIFICATION]** Run `uv run pytest tests/roadmap/ -v` to verify no regression in prompt generation
6. **[COMPLETION]** Record implementation evidence to D-0015 and D-0016 spec.md files

**Acceptance Criteria:**
- `INTEGRATION_ENUMERATION_BLOCK` exists in prompts.py and appears in `build_generate_prompt()` output before `_OUTPUT_FORMAT_BLOCK`
- `INTEGRATION_WIRING_DIMENSION` exists in prompts.py as dimension 6 in `build_spec_fidelity_prompt()` output
- Both blocks are string constants (probability reducers, not enforcement mechanisms)
- No existing prompt dimensions or blocks are modified or reordered

**Validation:**
- `uv run pytest tests/roadmap/ -v` exits 0 (no regression)
- Evidence: prompts.py diff archived to D-0015/spec.md

**Dependencies:** None (prompt changes are independent of gate/executor wiring)
**Rollback:** Revert `prompts.py` to pre-edit state (git checkout)
**Notes:** Prompt changes are probability reducers only. Deterministic modules remain the source of truth per roadmap architect recommendation #3.

---

### T02.04 -- Write Anti-Instinct Integration Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Integration tests validate the full pipeline with anti-instinct gate active, proving end-to-end correctness against known-good and known-bad roadmaps including the cli-portify regression case (SC-001). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | end-to-end (full pipeline), system-wide |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0017/evidence.md`

**Deliverables:**
1. `tests/roadmap/test_anti_instinct_integration.py` — integration tests covering: end-to-end roadmap pipeline run with anti-instinct gate active, gate blocks on known-bad roadmap (cli-portify regression SC-001), gate passes on known-good roadmap, structural audit emits warning without blocking, `anti-instinct-audit.md` output format and frontmatter correctness. All tests use real pipeline invocations, no mocks.

**Steps:**
1. **[PLANNING]** Identify pipeline invocation API for end-to-end test execution
2. **[PLANNING]** Prepare known-good roadmap fixture and known-bad (cli-portify) roadmap fixture
3. **[EXECUTION]** Write end-to-end test: full roadmap pipeline completes with anti-instinct gate
4. **[EXECUTION]** Write regression test (SC-001): three semantic checks block on cli-portify regression case
5. **[EXECUTION]** Write tests for structural audit warning-only behavior and `anti-instinct-audit.md` output format validation
6. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_anti_instinct_integration.py -v`
7. **[COMPLETION]** Record test results to D-0017/evidence.md

**Acceptance Criteria:**
- `tests/roadmap/test_anti_instinct_integration.py` exists with tests covering all 5 integration scenarios
- SC-001 test verifies all three semantic checks pass on cli-portify regression (end-to-end)
- `anti-instinct-audit.md` output validated for YAML frontmatter containing `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`
- `uv run pytest tests/roadmap/test_anti_instinct_integration.py -v` exits 0 with all tests passing

**Validation:**
- `uv run pytest tests/roadmap/test_anti_instinct_integration.py -v` exits 0
- Evidence: test output log archived to D-0017/evidence.md

**Dependencies:** T02.01, T02.02, T02.03
**Rollback:** Delete `tests/roadmap/test_anti_instinct_integration.py`

---

### Checkpoint: End of Phase 2

**Purpose:** Validate pipeline integration (Checkpoint A extended): full roadmap pipeline completes with anti-instinct gate, SC-001 regression proven, latency confirmed, no test breakage.
**Checkpoint Report Path:** `.dev/releases/current/v3.1_Anti-instincts__/checkpoints/CP-P02-END.md`
**Verification:**
- `uv run pytest tests/roadmap/ -v` exits 0 with all new and existing tests passing
- SC-001 end-to-end regression passes (three semantic checks block on cli-portify case)
- SC-006 combined latency < 1s confirmed via timing assertions in integration tests
**Exit Criteria:**
- All 4 tasks (T02.01-T02.04) completed with deliverables D-0011 through D-0017 produced
- `gate_passed()` signature unchanged (NFR-009)
- `uv run pytest` (full test suite) exits 0 with zero regressions (SC-007)
