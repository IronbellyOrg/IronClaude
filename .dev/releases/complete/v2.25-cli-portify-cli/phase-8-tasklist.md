# Phase 8 -- Panel Review Convergence Loop

Implement the highest-risk quality-control stage: bounded expert review with convergence scoring. The convergence loop is internal — it does NOT use the outer retry mechanism.

---

### T08.01 -- Implement Convergence State Machine in review.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-052 |
| Why | The state machine defines the legal state transitions for the panel review loop; incorrect transitions could allow infinite looping or premature termination |
| Effort | L |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0048 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0048/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/review.py` `ConvergenceLoop` class implementing state machine: `NOT_STARTED → REVIEWING → INCORPORATING → SCORING → CONVERGED|ESCALATED` (FR-030)

**Steps:**
1. **[PLANNING]** Load `ConvergenceState` enum from `models.py`; review roadmap FR-030 state transitions
2. **[EXECUTION]** Create `src/superclaude/cli/cli_portify/review.py`
3. **[EXECUTION]** Implement `ConvergenceLoop` class with `state: ConvergenceState`, `iteration: int`, `max_iterations: int = 3`
4. **[EXECUTION]** Implement state transitions: `start()` → REVIEWING; `record_findings()` → INCORPORATING; `record_scores()` → SCORING; `evaluate()` → CONVERGED or REVIEWING (if not done) or ESCALATED (if max_iterations reached)
5. **[EXECUTION]** Raise `ConvergenceStateError` on invalid transition
6. **[EXECUTION]** State transitions must be logged to `execution-log.jsonl` via `LoggingManager`
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "convergence_state or convergence_loop" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0048/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "convergence_state"` exits 0
- All valid state transitions execute without exception
- `ESCALATED` state reached when `iteration >= max_iterations` and not yet CONVERGED
- `CONVERGED` state reached when zero unaddressed CRITICALs (verified by T08.03)
- Invalid transition raises `ConvergenceStateError`

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "convergence_loop" -v` — all transition paths covered
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0048/spec.md` produced

**Dependencies:** T03.01 (ConvergenceState enum in models.py)
**Rollback:** Remove `review.py`; revert to prior state

---

### T08.02 -- Implement Per-Iteration Logic (4a–4d)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-053 |
| Why | Each iteration's 4-substep logic (expert focus, finding incorporation, panel critique, convergence scoring) must execute in order; skipping any substep produces incomplete quality assessment |
| Effort | XL |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0049 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0049/spec.md`

**Deliverables:**
- `review.py` per-iteration logic: (4a) 4-expert focus pass (Fowler, Nygard, Whittaker, Crispin), (4b) finding incorporation (CRITICAL→mandatory, MAJOR→incorporated, MINOR→Section 11), (4c) full panel critique with quality scoring (clarity, completeness, testability, consistency), (4d) convergence scoring (FR-031)

**Steps:**
1. **[PLANNING]** Review roadmap FR-031: 4 substeps per iteration; note SKILL.md uses 4a–4d notation
2. **[EXECUTION]** Implement `execute_expert_focus_pass(spec_content, expert_name, process) -> list[Finding]` for each of 4 experts
3. **[EXECUTION]** Implement `incorporate_findings(spec_content, findings) -> str`: CRITICAL → mandatory body update; MAJOR → incorporated; MINOR → Section 11
4. **[EXECUTION]** Implement `execute_panel_critique(spec_content, process) -> QualityScores` calling Claude for scores on clarity, completeness, testability, consistency
5. **[EXECUTION]** Implement `compute_convergence_score(findings: list[Finding]) -> bool`: returns True when zero unaddressed CRITICALs (FR-032). Note: overall>=7.0 scoring drives `downstream_ready` only (FR-034) and is handled exclusively in T08.05 — do NOT fold it into convergence here.
6. **[EXECUTION]** Wire 4 substeps into `ConvergenceLoop.run_iteration(spec_content, process)`
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "per_iteration or expert_focus or panel_critique" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0049/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "per_iteration"` exits 0
- All 4 expert focus passes (Fowler, Nygard, Whittaker, Crispin) executed per iteration
- Finding severity routing: CRITICAL → body, MINOR → Section 11
- `QualityScores` has clarity, completeness, testability, consistency, overall fields
- Convergence score computation: zero unaddressed CRITICALs → converged (FR-032); overall>=7.0 is a separate concern handled by T08.05 downstream_ready gate (FR-034)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "panel_critique" -v` — 4 expert names verified in prompt calls
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0049/spec.md` produced

**Dependencies:** T08.01 (ConvergenceLoop), T03.01 (models)
**Rollback:** Revert `review.py` iteration logic; convergence loop becomes non-functional

---

### T08.03 -- Implement CONVERGED Terminal Condition

| Field | Value |
|---|---|
| Roadmap Item IDs | R-054 |
| Why | CONVERGED is the success terminal state; its condition (zero unaddressed CRITICALs) must be evaluated correctly or the loop terminates prematurely with unresolved critical findings |
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
| Deliverable IDs | D-0050 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0050/spec.md`

**Deliverables:**
- `review.py` CONVERGED condition: zero unaddressed CRITICALs → `ConvergenceLoop.state = CONVERGED`, `status = "success"` (FR-032, SC-009)

**Steps:**
1. **[PLANNING]** Review roadmap FR-032: CONVERGED iff zero unaddressed CRITICALs
2. **[EXECUTION]** Implement `_count_unaddressed_criticals(spec_content: str) -> int`: count CRITICAL findings NOT marked `[INCORPORATED]` or `[DISMISSED]`
3. **[EXECUTION]** In `ConvergenceLoop.evaluate()`: if `_count_unaddressed_criticals() == 0` → transition to CONVERGED, set `status = "success"`
4. **[EXECUTION]** CONVERGED is terminal: no further iterations
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "converged_condition" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0050/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "converged_condition"` exits 0 (SC-009)
- Spec with zero unaddressed CRITICALs → state CONVERGED, status "success"
- Spec with one unaddressed CRITICAL → not CONVERGED (continue looping or ESCALATED)
- CRITICAL marked `[INCORPORATED]` is not counted as unaddressed

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "converged_condition" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0050/spec.md` produced

**Dependencies:** T08.02 (per-iteration logic), T08.01 (state machine evaluate())
**Rollback:** Revert CONVERGED condition logic

---

### T08.04 -- Implement ESCALATED Terminal Condition

| Field | Value |
|---|---|
| Roadmap Item IDs | R-055 |
| Why | ESCALATED must be a distinct terminal state from CONVERGED; confusing the two would incorrectly set `downstream_ready = true` on a partial result |
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
| Deliverable IDs | D-0051 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0051/spec.md`

**Deliverables:**
- `review.py` ESCALATED condition: 3 iterations exhausted without CONVERGED → `status = "partial"` (FR-033)

**Steps:**
1. **[PLANNING]** Review roadmap FR-033: ESCALATED when max_iterations (3) reached and not CONVERGED
2. **[EXECUTION]** In `ConvergenceLoop.evaluate()`: after incrementing `iteration`, if `iteration >= max_iterations` and not CONVERGED → transition to ESCALATED, set `status = "partial"`
3. **[EXECUTION]** ESCALATED is terminal: no further iterations
4. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "escalated_condition" -v`
5. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0051/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "escalated_condition"` exits 0
- After 3 iterations without CONVERGED → state ESCALATED, status "partial"
- `status = "partial"` is distinct from `status = "success"`
- `downstream_ready` is NOT set to true on ESCALATED (verified by T08.05)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "escalated_condition" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0051/spec.md` produced

**Dependencies:** T08.01 (state machine), T08.03 (CONVERGED defined before ESCALATED can be distinguished)
**Rollback:** Revert ESCALATED condition; loop runs unbounded

---

### T08.05 -- Gate downstream_ready and Emit panel-report.md on Both Terminal Conditions

| Field | Value |
|---|---|
| Roadmap Item IDs | R-056 |
| Why | `downstream_ready = false` on ESCALATED prevents a partial output being mistaken for a completed review; `panel-report.md` must exist on both paths because the return contract references it |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0052 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0052/spec.md`

**Deliverables:**
- `review.py` `downstream_ready` flag: set True only when `overall >= 7.0` (FR-034, NFR-005); `panel-report.md` emitted on both CONVERGED and ESCALATED terminal conditions (FR-035, SC-010)

**Steps:**
1. **[PLANNING]** Review roadmap FR-034/FR-035/NFR-005: downstream_ready gated on overall ≥ 7.0; panel-report.md required on both paths
2. **[EXECUTION]** Implement `set_downstream_ready(scores: QualityScores) -> bool`: return `scores.overall >= 7.0`
3. **[EXECUTION]** Set `self.downstream_ready = set_downstream_ready(scores)` after scoring in both CONVERGED and ESCALATED paths
4. **[EXECUTION]** Implement `emit_panel_report(loop: ConvergenceLoop, workdir: Path) -> Path` writing `workdir/panel-report.md`
5. **[EXECUTION]** Call `emit_panel_report()` in both CONVERGED and ESCALATED terminal paths
6. **[EXECUTION]** `panel-report.md` includes: terminal status, iteration count, final scores, unaddressed findings list, `downstream_ready` value
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "downstream_ready or panel_report" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0052/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "downstream_ready"` exits 0 (SC-010)
- `overall = 6.9` → `downstream_ready = False`
- `overall = 7.0` → `downstream_ready = True`
- `panel-report.md` exists in workdir after CONVERGED terminal condition
- `panel-report.md` exists in workdir after ESCALATED terminal condition (return contract requires it on both paths)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "panel_report" -v` — both CONVERGED and ESCALATED paths emit panel-report.md
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0052/spec.md` produced

**Dependencies:** T08.03 (CONVERGED), T08.04 (ESCALATED), T08.02 (QualityScores)
**Rollback:** Remove `downstream_ready` gate; remove `emit_panel_report()` calls

---

### T08.06 -- Enforce Internal Convergence Loop and 1200s Timeout

| Field | Value |
|---|---|
| Roadmap Item IDs | R-057 |
| Why | Using the outer retry mechanism for convergence would consume retry budget; AC-011 mandates the internal loop; 1200s timeout prevents indefinite expert review execution |
| Effort | S |
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
| Deliverable IDs | D-0053 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0053/spec.md`

**Deliverables:**
- `executor.py` panel-review step uses internal `ConvergenceLoop.run()` — NOT outer retry; `timeout_s = 1200` in STEP_REGISTRY for panel-review step (AC-011, NFR-001)

**Steps:**
1. **[PLANNING]** Review roadmap AC-011: internal loop, not outer retry; NFR-001: 1200s timeout
2. **[EXECUTION]** Confirm panel-review step in STEP_REGISTRY has `retry_limit = 0` (no outer retry)
3. **[EXECUTION]** Confirm `timeout_s = 1200` in STEP_REGISTRY for panel-review step
4. **[EXECUTION]** Confirm executor calls `ConvergenceLoop.run(max_iterations=3)` internally, not `_execute_step_with_retry()`
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "panel_timeout or convergence_internal" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0053/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "panel_timeout"` exits 0
- Panel-review STEP_REGISTRY entry has `retry_limit = 0`
- Panel-review STEP_REGISTRY entry has `timeout_s = 1200`
- Executor calls `ConvergenceLoop` directly, not outer retry path

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "convergence_internal" -v` — confirms no outer retry involvement
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0053/spec.md` produced

**Dependencies:** T08.01 (ConvergenceLoop.run()), T03.04 (STEP_REGISTRY)
**Rollback:** N/A (configuration verification; no functional change if already correct)

---

### Checkpoint: End of Phase 8

**Purpose:** Verify panel review converges or escalates deterministically, downstream_ready is correctly gated, and panel-report.md is emitted on both terminal paths before observability completion and CLI integration begin.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P08-END.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "convergence or panel_report or downstream_ready" -v` exits 0
- SC-009 (CONVERGED within 3 iterations) and SC-010 (quality score ≥7.0, downstream_ready=true) verified
- `panel-report.md` emitted on both CONVERGED and ESCALATED paths

**Exit Criteria:**
- All 6 Phase 8 tasks complete with D-0048 through D-0053 artifacts
- Milestone M7: Step 11 converges or escalates deterministically; downstream_ready gated correctly
- Internal convergence loop confirmed (no outer retry consumption)
