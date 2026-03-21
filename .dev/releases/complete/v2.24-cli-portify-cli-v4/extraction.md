---
spec_source: "portify-release-spec.md"
generated: "2026-03-20T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 7
nonfunctional_requirements: 11
total_requirements: 18
complexity_score: 0.85
complexity_class: HIGH
domains_detected: [backend, cli, devops, testing]
risks_identified: 9
dependencies_identified: 8
success_criteria_count: 12
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 146.0, started_at: "2026-03-20T16:43:37.277670+00:00", finished_at: "2026-03-20T16:46:03.298069+00:00"}
---

## Functional Requirements

### FR-PORTIFY-CLI.1: Config Validation (Step: validate-config)

**Type**: Pure-programmatic
**Priority**: Critical (pipeline gate — blocks all downstream steps)
**Consolidates**: Logical Step 0

| Sub-ID | Requirement | Acceptance Criterion |
|--------|-------------|---------------------|
| FR-PORTIFY-CLI.1a | Resolve `--workflow` to directory containing `SKILL.md` | Emits `INVALID_PATH` error on missing SKILL.md |
| FR-PORTIFY-CLI.1b | Derive CLI name from workflow path | Strips `sc-` prefix and `-protocol` suffix, converts to kebab/snake case; emits `DERIVATION_FAILED` on failure |
| FR-PORTIFY-CLI.1c | Validate output directory writability | Parent directory must exist and be writable; emits `OUTPUT_NOT_WRITABLE` |
| FR-PORTIFY-CLI.1d | Detect name collisions with non-portified modules | Emits `NAME_COLLISION` if target directory exists with non-portified `__init__.py` |
| FR-PORTIFY-CLI.1e | Produce config result artifact | Writes `validate-config-result.json` with resolved paths |
| FR-PORTIFY-CLI.1f | Performance constraint | Completes in <1s (no Claude subprocess) |

**Dependencies**: None

---

### FR-PORTIFY-CLI.2: Component Discovery (Step: discover-components)

**Type**: Pure-programmatic
**Priority**: Critical (feeds all Claude-assisted steps)
**Consolidates**: Logical Step 1

| Sub-ID | Requirement | Acceptance Criterion |
|--------|-------------|---------------------|
| FR-PORTIFY-CLI.2a | Find SKILL.md | Located in workflow directory root |
| FR-PORTIFY-CLI.2b | Discover subdirectory files | Finds all files in `refs/`, `rules/`, `templates/`, `scripts/` via `Path.rglob()` |
| FR-PORTIFY-CLI.2c | Locate matching command file | Searches `src/superclaude/commands/` and `.claude/commands/sc/` |
| FR-PORTIFY-CLI.2d | Count lines per component | Accurate line count for each discovered file |
| FR-PORTIFY-CLI.2e | Produce inventory artifact | `component-inventory.md` with YAML frontmatter (`source_skill`, `component_count`) |
| FR-PORTIFY-CLI.2f | Performance constraint | Completes in <5s (no Claude subprocess) |

**Dependencies**: FR-PORTIFY-CLI.1

---

### FR-PORTIFY-CLI.3: Workflow Analysis (Step: analyze-workflow)

**Type**: Claude-assisted
**Priority**: Critical
**Consolidates**: Logical Steps 2 (protocol mapping), 3 (step identification/classification), 4 (gate extraction), 5 (analysis assembly)

| Sub-ID | Requirement | Acceptance Criterion |
|--------|-------------|---------------------|
| FR-PORTIFY-CLI.3a | Produce analysis document | `portify-analysis.md` with YAML frontmatter: `source_skill`, `step_count`, `parallel_groups`, `gate_count`, `complexity` |
| FR-PORTIFY-CLI.3b | Required sections | Must contain: Source Components, Step Graph, Gates Summary, Data Flow Diagram, Classification Summary |
| FR-PORTIFY-CLI.3c | Step classification | Every identified step classified as pure-programmatic, claude-assisted, or hybrid |
| FR-PORTIFY-CLI.3d | Data flow diagram | Present with arrow notation (`-->` or `--->`) |
| FR-PORTIFY-CLI.3e | Output size | Under 400 lines |
| FR-PORTIFY-CLI.3f | Gate enforcement | Passes STRICT tier validation |

**Dependencies**: FR-PORTIFY-CLI.2

---

### FR-PORTIFY-CLI.4: Pipeline Design (Step: design-pipeline)

**Type**: Claude-assisted
**Priority**: Critical
**Consolidates**: Logical Step 6

| Sub-ID | Requirement | Acceptance Criterion |
|--------|-------------|---------------------|
| FR-PORTIFY-CLI.4a | Produce pipeline spec | `portify-spec.md` with YAML frontmatter: `step_mapping_count`, `model_count`, `gate_definition_count` |
| FR-PORTIFY-CLI.4b | Step mapping completeness | Contains step mapping entries for every pipeline step |
| FR-PORTIFY-CLI.4c | Gate definition completeness | All steps have corresponding gate definitions |
| FR-PORTIFY-CLI.4d | Pure-programmatic code | Pure-programmatic steps include actual Python implementation |
| FR-PORTIFY-CLI.4e | Prompt builder spec | Claude-assisted steps specify required output format and machine-readable markers |
| FR-PORTIFY-CLI.4f | Execution model | Executor design uses synchronous threading (not async/await) |
| FR-PORTIFY-CLI.4g | Gate enforcement | Passes STRICT tier validation |
| FR-PORTIFY-CLI.4h | User review gate | Review gate after this step; `--dry-run` halts pipeline here |

**Dependencies**: FR-PORTIFY-CLI.3

---

### FR-PORTIFY-CLI.5: Spec Synthesis (Step: synthesize-spec)

**Type**: Claude-assisted
**Priority**: Critical
**Consolidates**: Logical Steps 7 (template instantiation), 8 (content population)

| Sub-ID | Requirement | Acceptance Criterion |
|--------|-------------|---------------------|
| FR-PORTIFY-CLI.5a | Produce release spec | `portify-release-spec.md` with complete YAML frontmatter |
| FR-PORTIFY-CLI.5b | Zero placeholders (SC-003) | Zero remaining `{{SC_PLACEHOLDER:*}}` sentinels |
| FR-PORTIFY-CLI.5c | FR count | Contains 7 functional requirements (one per pipeline step) |
| FR-PORTIFY-CLI.5d | Consolidation mapping | Explicit mapping of which logical steps each FR covers |
| FR-PORTIFY-CLI.5e | Conditional sections | Includes portification-type sections: 4.3, 4.5, 5, 8.3, 9 |
| FR-PORTIFY-CLI.5f | Gate enforcement | Passes STRICT tier validation |
| FR-PORTIFY-CLI.5g | Retry with specifics (F-005) | On gate failure, retry prompt includes specific remaining placeholder names |

**Dependencies**: FR-PORTIFY-CLI.4

---

### FR-PORTIFY-CLI.6: Brainstorm Gap Analysis (Step: brainstorm-gaps)

**Type**: Claude-assisted (skill reuse)
**Priority**: High
**Consolidates**: Logical Step 9

| Sub-ID | Requirement | Acceptance Criterion |
|--------|-------------|---------------------|
| FR-PORTIFY-CLI.6a | Skill invocation | Subprocess invokes `/sc:brainstorm` (not reimplemented patterns) |
| FR-PORTIFY-CLI.6b | Section 12 appended | Brainstorm Gap Analysis section appended to spec |
| FR-PORTIFY-CLI.6c | Structured findings | Format: `{gap_id, description, severity, affected_section, persona}` |
| FR-PORTIFY-CLI.6d | Actionable incorporation | Actionable findings incorporated into spec sections, marked `[INCORPORATED]` |
| FR-PORTIFY-CLI.6e | Open item routing | Unresolvable items routed to Section 11, marked `[OPEN]` |
| FR-PORTIFY-CLI.6f | Summary stats | Includes `{total_gaps, incorporated, open, severity_distribution}` |
| FR-PORTIFY-CLI.6g | Zero-gap validity | Zero-gap outcome does not block pipeline |
| FR-PORTIFY-CLI.6h | Gate enforcement | Passes STANDARD tier validation |
| FR-PORTIFY-CLI.6i | Section 12 structural validation (F-007) | Must contain findings table (with Gap ID column) or literal zero-gap summary text; heading alone insufficient |
| FR-PORTIFY-CLI.6j | Pre-flight skill check (GAP-001) | Verify `/sc:brainstorm` available; fall back to inline multi-persona prompt with warning if unavailable |

**Dependencies**: FR-PORTIFY-CLI.5

---

### FR-PORTIFY-CLI.7: Panel Review with Convergence (Step: panel-review)

**Type**: Claude-assisted (skill reuse + convergence loop)
**Priority**: Critical
**Consolidates**: Logical Steps 10 (focus pass), 11 (critique/scoring/convergence)

| Sub-ID | Requirement | Acceptance Criterion |
|--------|-------------|---------------------|
| FR-PORTIFY-CLI.7a | Skill invocation | Each iteration invokes `/sc:spec-panel` (not reimplemented expert patterns) |
| FR-PORTIFY-CLI.7b | Convergence loop management | Executor manages loop with iteration counter and hard cap (max 3) |
| FR-PORTIFY-CLI.7c | Convergence predicate | Zero findings with `severity: CRITICAL` and status not `[INCORPORATED]` or `[DISMISSED]` |
| FR-PORTIFY-CLI.7d | Quality scores | Spec frontmatter contains: clarity, completeness, testability, consistency (all 0-10 float) |
| FR-PORTIFY-CLI.7e | Overall score calculation (SC-010) | `overall = mean(clarity, completeness, testability, consistency)` |
| FR-PORTIFY-CLI.7f | Panel report artifact | `panel-report.md` with all findings, scores, convergence status |
| FR-PORTIFY-CLI.7g | Machine-readable convergence block | Contains `CONVERGENCE_STATUS`, `UNADDRESSED_CRITICALS`, `QUALITY_OVERALL` |
| FR-PORTIFY-CLI.7h | Terminal states | CONVERGED (success) or ESCALATED (partial, with user escalation) |
| FR-PORTIFY-CLI.7i | Downstream ready gate (SC-012) | `overall >= 7.0` (boundary: 7.0 true, 6.9 false) |
| FR-PORTIFY-CLI.7j | Gate enforcement | Passes STRICT tier validation |
| FR-PORTIFY-CLI.7k | User review gate | Review gate at end of step |
| FR-PORTIFY-CLI.7l | Pre-flight skill check (GAP-001) | Verify `/sc:spec-panel` available; fall back to inline expert panel prompt with warning if unavailable |
| FR-PORTIFY-CLI.7m | Dual-mode iterations (GAP-006) | Each iteration runs both focus pass (discussion) and critique pass (critique) within a single subprocess |
| FR-PORTIFY-CLI.7n | Independent iteration timeout (F-004) | Each iteration has independent timeout (default 300s); TurnLedger guards budget before each launch |

**Dependencies**: FR-PORTIFY-CLI.6

---

## Non-Functional Requirements

| ID | Requirement | Target | Measurement Method |
|----|-------------|--------|--------------------|
| NFR-001 | Phase 3 wall clock time | < 10 minutes | `phase_timing.phase_3_seconds`; advisory warning if exceeded |
| NFR-002 | Phase 4 wall clock time | < 15 minutes | `phase_timing.phase_4_seconds`; advisory warning if exceeded |
| NFR-003 | Synchronous execution only | Zero `async def` or `await` in `cli_portify/` | Code review + static analysis |
| NFR-004 | Gate function signatures | All return `tuple[bool, str]` | Type checking + unit tests |
| NFR-005 | Runner-authored truth | Reports from observed data only (exit codes, artifacts, gates) | No Claude self-reporting in status determination |
| NFR-006 | Deterministic flow control | Python controls all step sequencing | No step uses Claude to decide "what's next" |
| NFR-007 | No pipeline/sprint modification | Zero changes to `pipeline/` or `sprint/` base modules | `git diff` verification |
| NFR-008 | Additive-only spec modifications | Panel review never rewrites existing content | Append/extend only in Steps 4b, 4d |
| NFR-009 | Failure path defaults | All contract fields populated on every failure type | Unit test coverage per failure type |
| NFR-010 | Skill reuse | brainstorm-gaps invokes `/sc:brainstorm`; panel-review invokes `/sc:spec-panel` | Prompt content inspection + integration test |
| NFR-011 | User review gates | When not `--skip-review`, executor pauses TUI, prompts on stderr; `y` continues, `n` halts with `USER_REJECTED` | Manual test |

---

## Complexity Assessment

**Score**: 0.85 / 1.0
**Class**: HIGH

**Scoring Rationale**:

| Factor | Score | Weight | Justification |
|--------|-------|--------|---------------|
| Module count | 0.9 | 20% | 18 new modules + 1 modified file; `steps/` subdirectory with 7 step implementations |
| Integration surface | 0.85 | 20% | Extends 4 existing base classes (`PipelineConfig`, `StepResult`, `ClaudeProcess`, `TurnLedger`); integrates with `main.py` CLI registration; invokes 2 external skills (`/sc:brainstorm`, `/sc:spec-panel`) in subprocesses |
| Convergence logic | 0.9 | 15% | Executor-managed iteration loop with budget guards, convergence predicate parsing, dual-mode subprocess invocation, section hashing for additive-only enforcement |
| State management | 0.8 | 15% | 6 data models with complex state transitions; `ConvergenceState` enum with valid-transition dictionary; resume decision table with per-step resumability |
| Gate system | 0.8 | 15% | 7 gate definitions across 3 enforcement tiers; 8 semantic check functions with YAML parsing; tiered enforcement (EXEMPT/STANDARD/STRICT) |
| CLI/TUI | 0.75 | 15% | Click CLI group with 8 options; Rich TUI live dashboard; JSONL + Markdown logging; 5 signal types; unified `monitor.py` with DiagnosticCollector, FailureClassifier, ReportGenerator |

**Weighted total**: 0.85

---

## Architectural Constraints

1. **Synchronous execution only** (NFR-003): No `async def` or `await` anywhere in `cli_portify/`. Threading + `time.sleep()` polling for subprocess monitoring.

2. **Extend existing base types**: `PortifyConfig` extends `PipelineConfig`, `PortifyStepResult` extends `StepResult`, `PortifyProcess` extends `ClaudeProcess`. No reimplementation of base functionality.

3. **Zero modifications to base modules** (NFR-007): No changes to `pipeline/` or `sprint/` packages. New module is purely additive.

4. **File passing via `@path` references**: Claude subprocesses read artifacts via `@path` references (matching sprint `ClaudeProcess` pattern), not `--file` CLI args or inline embedding.

5. **Executor-controlled flow** (NFR-006): Python controls all step sequencing, convergence iteration, and gate evaluation. Claude subprocesses handle content generation only.

6. **Skill reuse over reimplementation** (NFR-010): Steps 6 and 7 invoke existing `/sc:brainstorm` and `/sc:spec-panel` skills. No reimplementation of multi-persona or expert panel logic.

7. **Runner-authored truth** (NFR-005): All status determination from observed data (exit codes, artifact existence, gate checks). No Claude self-reporting accepted.

8. **18-module structure with `steps/` subdirectory** (DEV-001): Accepted deviation from original 13-file flat layout. Produced through adversarial debate consensus (D-02, D-04, D-11, D-12, D-14).

9. **Contract emission on all exit paths**: Return contract YAML produced for success, partial, failed, and dry_run outcomes. All fields populated with defaults on failure.

10. **Click CLI integration**: Registered via `app.add_command()` in `main.py`. Single `run` subcommand under `cli-portify` group.

11. **Python >=3.10**: Uses `int | None` union syntax, `@dataclass`, `Enum`, `Path`.

12. **Technology mandates**: Click for CLI, Rich for TUI, YAML for contracts, JSONL for logging.

---

## Risk Inventory

| # | Risk | Severity | Probability | Mitigation |
|---|------|----------|-------------|------------|
| 1 | Large context windows in Steps 5-7 cause Claude output truncation | High | Medium | Use `@path` references instead of inline embedding; generous `max_turns` |
| 2 | Convergence loop exhausts budget before 3 iterations | Medium | Medium | TurnLedger pre-launch guards; per-iteration budget estimation; ESCALATED terminal state |
| 3 | `/sc:brainstorm` and `/sc:spec-panel` fail to produce machine-readable convergence markers | High | Medium | Post-processing parses output; fallback to structural checks if markers missing |
| 4 | Sequential execution yields long wall-clock time | Low | High | Inherent to data dependencies; 7 steps vs 12 reduces overhead; timing advisory only |
| 5 | Self-portification circularity | Medium | Low | Source skill files read-only during portification; generated code in separate directory |
| 6 | Subprocess skill invocation fails if commands not installed | High | Low | Pre-flight check verifies `claude` binary; config validation checks skill availability |
| 7 | Subprocess cannot read `@path` files outside working directory scope | High | Medium | `PortifyProcess` passes `--add-dir` for work_dir and workflow_path (GAP-002) |
| 8 | User review gates lack programmatic interaction mechanism | Medium | Medium | `--skip-review` flag bypasses; executor pauses TUI, prompts on stderr (GAP-003) |
| 9 | Panel review convergence prompt uses wrong mode mapping across iterations | High | High | Each iteration runs both focus (discussion) + critique within single subprocess (GAP-006) |

---

## Dependency Inventory

| # | Dependency | Type | Used By | Notes |
|---|-----------|------|---------|-------|
| 1 | `pipeline.models` (PipelineConfig, Step, StepResult, GateCriteria, GateMode) | Internal package | models.py, gates.py | Base types extended by portify models |
| 2 | `pipeline.gates` (gate_passed) | Internal package | executor.py, step modules | Gate validation engine |
| 3 | `pipeline.process` (ClaudeProcess) | Internal package | process.py | Base class for PortifyProcess |
| 4 | `sprint.models` (TurnLedger) | Internal package | executor.py | Budget tracking for multi-subprocess execution |
| 5 | `sprint.process` (SignalHandler) | Internal package | executor.py | Graceful shutdown handling |
| 6 | `/sc:brainstorm` skill | External skill (subprocess) | brainstorm_gaps.py | Multi-persona gap analysis; fallback available if unavailable |
| 7 | `/sc:spec-panel` skill | External skill (subprocess) | panel_review.py | Expert panel review with quality scoring; fallback available if unavailable |
| 8 | `claude` binary | External system | executor.py pre-flight | Required for all Claude-assisted steps; validated at pipeline start |

**Python library dependencies** (inherited from project):
- `click>=8.0.0` — CLI framework
- `rich>=13.0.0` — TUI dashboard
- `pyyaml` — Contract emission and frontmatter parsing

---

## Success Criteria

| # | Criterion | Threshold | Measurement |
|---|-----------|-----------|-------------|
| 1 | Full pipeline execution completes | Steps 1-7 all PASS | Integration test: end-to-end portification of a real skill |
| 2 | Dry-run halts correctly | Phases 0-2 complete, Phases 3-4 SKIPPED, `dry_run` contract emitted | Integration test with `--dry-run` flag |
| 3 | STRICT gates enforce quality | Gate failure halts pipeline with diagnostic report | Integration test with deliberately malformed output |
| 4 | Convergence loop terminates | CONVERGED on 0 CRITICALs or ESCALATED after max iterations | Unit test + integration test |
| 5 | Downstream readiness gate | `overall >= 7.0` → true; `6.9` → false (SC-012) | Unit test boundary check |
| 6 | Quality scores arithmetic | `overall = mean(clarity, completeness, testability, consistency)` (SC-010) | Unit test with known values |
| 7 | Zero placeholders (SC-003) | Zero `{{SC_PLACEHOLDER:*}}` in synthesized spec | Gate semantic check |
| 8 | Return contract completeness | All fields populated on success, partial, failed, dry_run paths (NFR-009) | Unit test per outcome type |
| 9 | Resume command generation | Correct `--resume --start <step>` command for resumable failures | Unit test |
| 10 | No base module changes | Zero `git diff` in `pipeline/` and `sprint/` (NFR-007) | CI check |
| 11 | Synchronous execution | Zero `async def` or `await` in `cli_portify/` (NFR-003) | Static analysis |
| 12 | Self-portification | `superclaude cli-portify run src/superclaude/skills/sc-cli-portify-protocol/` completes | E2E meta-test |

---

## Open Questions

| # | Question | Source | Impact | Suggested Resolution |
|---|----------|--------|--------|---------------------|
| 1 | **Resume from Phase 3 failure** (GAP-005): If `synthesize-spec` partially wrote the spec file, does the gate pass on resume? Should resume re-run synthesize-spec or only brainstorm? | Section 11 | Medium — resume may fail silently | Define explicit resume entry points: if spec file exists but fails gate, re-run synthesize-spec; if passes gate, skip to brainstorm |
| 2 | **NDJSON signal vocabulary** (GAP-008): What domain-specific signals does `monitor.py` extract from Claude subprocess output? | Section 11 | Medium — affects TUI accuracy | Define signal vocabulary during monitor.py development: persona switches, section completion, placeholder count, convergence markers, quality score updates |
| 3 | **Resume from Phase 4** (F-006): Prior `focus-findings.md` preserved as context injection into first iteration's prompt, but convergence counter resets to 1 | Section 11 | Medium — affects resume correctness | Implement as specified; verify counter reset doesn't cause re-evaluation of already-addressed findings |
| 4 | **Rounding tolerance** (GAP-004): `_overall_is_mean` uses `< 0.01` tolerance but display precision not specified | Section 12 | Low — edge case in quality score validation | Specify 2 decimal places for display; keep `< 0.01` tolerance for gate validation |
| 5 | **Inline imports** (GAP-007): `to_contract()` in spec uses inline imports (`hashlib`, `yaml`) — should be module-level in `contract.py` | Section 12 | Low — code quality | Move to module-level imports during implementation |
| 6 | **1MB line-counting cap**: `discover_components` has 1MB cap with warning per step implementation table, but reference code in Appendix D.1 has no cap | Section 4.1 vs Appendix D.1 | Low — inconsistency between spec sections | Implement the 1MB cap as stated in the architecture table; update reference code |
| 7 | **Scope boundary inconsistency**: Section 1.2 states "13 new Python modules" but Section 4.1 describes 18 modules (post DEV-001 deviation) | Section 1.2 vs 4.1 | Low — documentation drift | Update Section 1.2 to reflect accepted 18-module architecture |
| 8 | **Phase timing boundary**: Phase 3 timing starts at `synthesize-spec` but Phase 3 conceptually includes `brainstorm-gaps` — should the boundary be clearer? | Section 2.2 data flow vs executor pseudocode | Low — advisory-only metric | Document that phase_3_seconds covers synthesize-spec + brainstorm-gaps (as implemented in executor) |
| 9 | **`--resume` and `--start` CLI flags**: Referenced in `resume_command()` output but not declared in CLI Surface (Section 5.1) | Section 4.5 vs 5.1 | Medium — missing CLI contract | Add `--resume` (flag) and `--start` (string) to CLI Surface table |
| 10 | **`_all_gates_defined` semantic check**: Defined in Section 5.2.1 but not used in any GateCriteria object in Section 5.2.2 | Section 5.2.1 vs 5.2.2 | Low — dead code in spec | Either add to `DESIGN_PIPELINE_GATE` or remove from spec |
