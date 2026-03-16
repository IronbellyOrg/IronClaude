# v2.25-cli-portify — Resume Tasklist
# Cross-Release Conflict Analysis: Pre-Resume Amendments and Verification
#
# Source analysis: v2.24.2, v2.24.5, v2.25.5-PreFlightExecutor, v2.25.5-pass-no-report-fix
# vs. v2.25-cli-portify roadmap.md
#
# Context:
#   - Phases 1, 2, 3 of cli-portify are ALREADY BUILT (interrupted at Phase 3 checkpoint write)
#   - Resume point: Phase 4 (Gate System) — confirmed by agent analysis
#   - One design conflict (--file) requires roadmap amendment before Phase 6
#   - Several Phase 0 open questions are pre-resolved by prior releases
#
# Sprint compatibility: superclaude sprint run resume-tasklist.md

## Phase PRE — Pre-Resume Verification and Amendment
## Purpose: Validate existing Phases 1–3 output, resolve OQs closed by prior releases,
##          and amend the roadmap for the --file design conflict before any new code is written.
## Milestone: All blockers resolved; team can proceed to Phase 4 with no unknowns.

- [x] PRE-001 — Run existing test suite to confirm Phases 1–3 are regression-free
  - VERIFIED 2026-03-16: Sprint suite 713 passed, 0 failures
  - Portify test files all fail at COLLECTION (ModuleNotFoundError) — expected; tests are
    pre-written for modules not yet built (gates.py, prompts.py, contract.py, steps/*).
    This is not a regression — it confirms the interrupted state. Tests will pass as
    each phase's modules are implemented.
  - Sprint baseline confirmed clean.

- [x] PRE-002 — Verify PyYAML is present (v2.24.2 may have added it)
  - VERIFIED 2026-03-16: pyyaml 6.0.3 installed. No action needed.

- [x] PRE-003 — Verify `--tools default` in PortifyProcess (inherited from ClaudeProcess)
  - VERIFIED 2026-03-16:
    - ClaudeProcess.build_command() (pipeline/process.py:79-80) includes "--tools", "default"
    - PortifyProcess (cli_portify/process.py:187) calls super().build_command() — inherits correctly
    - PortifyProcess is at line 121, inherits via ClaudeProcess — confirmed
  - No code change needed.

- [x] PRE-004 — Confirm framework base types are importable and stable (closes Phase 0 D-008)
  - VERIFIED 2026-03-16:
    - ClaudeProcess: OK (pipeline.process)
    - PipelineConfig, Step, StepResult: OK (pipeline.models)
    - GateCriteria, GateMode, SemanticCheck: OK (pipeline.models)
  - CRITICAL NOTE: GateCriteria/GateMode/SemanticCheck are in `superclaude.cli.pipeline.models`,
    NOT in `superclaude.cli.sprint.models`. Any cli_portify code importing from sprint.models
    for these types will fail. Use pipeline.models.

- [x] PRE-005 — Close Phase 0 OQ-008 (--file subprocess behavior) — DO NOT re-investigate
  - CLOSED: oq-resolutions.md written with full resolution.
  - Finding: `claude --file <path>` broken — use inline `-p` embedding exclusively.
  - Impact applied in T07.06.

- [x] PRE-006 — Close Phase 0 OQ-013 (PASS_NO_SIGNAL retry behavior)
  - CLOSED: oq-resolutions.md written with full resolution.
  - PASS_NO_SIGNAL → retry; PASS_NO_REPORT → no retry (treat as pass).
  - Already documented in roadmap.md Phase 3 gate note (line 189).
  - T04.15 implements this distinction in gate retry logic.

- [ ] PRE-007 — Amend roadmap.md Phase 6 Action 7: replace --file with inline embedding
  - File: `.dev/releases/backlog/v2.25-cli-portify-cli/roadmap.md`
  - Find Phase 6, Action 7 (line ~330): "if len(template_content) > 50_000, write template to
    a temp file and pass via --file <path> to the Claude subprocess (R-011)..."
  - Replace with: "if len(template_content) > _EMBED_SIZE_LIMIT (120 * 1024 bytes), raise
    PortifyValidationError. For content under limit, pass inline via -p. --file is broken
    (confirmed v2.24.5 empirical testing; see oq-resolutions.md OQ-008)."
  - Also update Risk 11 in Risk Assessment: change from "Resolve file argument passing
    mechanism in Phase 0 (OQ-008)" to "RESOLVED: --file broken; use inline embedding only."
  - This is the only required code-plan change from the 4-release conflict analysis.

- [x] PRE-008 — Read main.py and confirm clean registration point for Phase 9
  - VERIFIED 2026-03-16: grep found zero portify/cli_portify references in main.py.
  - Phase 10 T10.04 registration point is clean.

---

## Phase 4 — Gate System and Semantic Validation Layer
## (roadmap Phase 3 — renumbered to account for PRE phase above)
## Prerequisite: PRE phase complete; Phases 1–3 verified passing
## Milestone M3: All 12 gates validate correctly against synthetic test data

- [ ] T04.01 — Implement gates.py skeleton with 12 gate stubs (G-000 through G-011)
  - File: `src/superclaude/cli/cli_portify/gates.py`
  - Each gate: name, tier (STANDARD/STRICT), GateMode.BLOCKING, check function stub

- [ ] T04.02 — Implement G-000: has_valid_yaml_config
  - Check: config YAML valid with required fields (workflow_path, cli_name, output_dir)

- [ ] T04.03 — Implement G-001: has_component_inventory
  - Check: inventory lists at least one component with SKILL.md

- [ ] T04.04 — Implement G-002: EXIT_RECOMMENDATION marker present
  - Used by: protocol-map.md output gate

- [ ] T04.05 — Implement G-003: EXIT_RECOMMENDATION present + has_required_analysis_sections
  - Required sections: Source Components, Step Graph, Parallel Groups, Gates Summary, Data Flow, Classifications, Recommendations
  - Used by: analysis-report.md gate

- [ ] T04.06 — Implement G-004: has_approval_status
  - Check: approval status field present (approved/rejected/pending)

- [ ] T04.07 — Implement G-005: EXIT_RECOMMENDATION marker present

- [ ] T04.08 — Implement G-006: return type pattern check

- [ ] T04.09 — Implement G-007: EXIT_RECOMMENDATION marker present

- [ ] T04.10 — Implement G-008: EXIT_RECOMMENDATION present + step-count consistency
  - Check: step_mapping count matches declared steps

- [ ] T04.11 — Implement G-009: has_approval_status

- [ ] T04.12 — Implement G-010: EXIT_RECOMMENDATION + has_zero_placeholders + has_brainstorm_section
  - Zero {{SC_PLACEHOLDER:*}} sentinels
  - Section 12 Brainstorm Gap Analysis present

- [ ] T04.13 — Implement G-011: has_quality_scores + has_criticals_addressed
  - Quality scores: clarity, completeness, testability, consistency, overall
  - All CRITICAL findings marked [INCORPORATED] or [DISMISSED]

- [ ] T04.14 — Implement gate diagnostics formatting
  - Failure reason, which check failed, artifact path, remediation hint

- [ ] T04.15 — Implement retry semantics: PASS_NO_SIGNAL triggers retry; PASS_NO_REPORT does not
  - Verify this distinction in gate retry logic matches PRE-006 resolution

- [ ] T04.16 — Unit tests: all 12 gates with passing and failing synthetic inputs
  - File: `tests/cli_portify/test_gates.py`
  - Each gate: at least one passing test and one failing test
  - Verify gate diagnostics output is well-formed on failure

- [ ] T04.17 — Write phase result file
  - Path: `.dev/portify-workdir/phase-4-result.md`
  - Include: gates implemented, test results, milestone M3 status
  - Sentinel: EXIT_RECOMMENDATION: CONTINUE

---

## Phase 5 — Claude-Assisted Analysis Pipeline
## (roadmap Phase 4)
## Prerequisite: Phase 4 (gates) complete
## Milestone M4: Phase 1 completes; review gate pauses; resume validates status: approved

- [ ] T05.01 — Implement prompts.py skeleton with Phase 1 prompt builders
  - File: `src/superclaude/cli/cli_portify/prompts.py`
  - Builders: build_protocol_mapping_prompt(), build_analysis_synthesis_prompt()

- [ ] T05.02 — Implement protocol-mapping step
  - Prompt builder → Claude subprocess → output: protocol-map.md
  - Required YAML frontmatter per FR-013
  - Enforce EXIT_RECOMMENDATION marker (FR-014)
  - Timeout: 600s (NFR-001)

- [ ] T05.03 — Implement analysis-synthesis step
  - Prompt builder → Claude subprocess → output: portify-analysis-report.md
  - Required sections per FR-016
  - Enforce EXIT_RECOMMENDATION marker (FR-017)
  - Timeout: 600s (NFR-001)

- [ ] T05.04 — Implement user-review-p1 gate
  - Write phase1-approval.yaml with status: pending
  - Print resume instructions to stdout
  - Exit cleanly (do not error)

- [ ] T05.05 — Implement --resume logic for Phase 1
  - Require status: approved in phase1-approval.yaml
  - YAML parse + schema validation (not raw string match)
  - Reject malformed YAML or missing status field

- [ ] T05.06 — Unit tests: review gate writes pending YAML; resume validates approved
  - File: `tests/cli_portify/test_review_gates.py`
  - SC-006 and SC-007 coverage

- [ ] T05.07 — Write phase result file
  - Path: `.dev/portify-workdir/phase-5-result.md`
  - Sentinel: EXIT_RECOMMENDATION: CONTINUE

---

## Phase 6 — Claude-Assisted Specification Pipeline
## (roadmap Phase 5)
## Prerequisite: Phase 5 complete
## Milestone M5: Phase 2 produces valid unified spec passing G-008

- [ ] T06.01 — Add Phase 2 prompt builders to prompts.py
  - Builders: build_step_graph_design_prompt(), build_models_gates_design_prompt(),
    build_prompts_executor_design_prompt(), build_pipeline_spec_assembly_prompt()

- [ ] T06.02 — Implement step-graph-design step → step-graph-spec.md (FR-020)

- [ ] T06.03 — Implement models-gates-design step → models-gates-spec.md (FR-021)

- [ ] T06.04 — Implement prompts-executor-design step → prompts-executor-spec.md (FR-022)

- [ ] T06.05 — Implement pipeline-spec-assembly step
  - Programmatic pre-assembly (concatenation, dedup) + Claude synthesis → portify-spec.md (FR-023)

- [ ] T06.06 — Enforce EXIT_RECOMMENDATION markers on all Phase 2 Claude steps (FR-024)

- [ ] T06.07 — Enforce 600s timeout per step (NFR-001)

- [ ] T06.08 — Implement user-review-p2 validation
  - status: completed, all blocking gates passed, step_mapping has entries (FR-025)
  - phase2-approval.yaml resume enforcement with YAML parse + schema validation (FR-026)

- [ ] T06.09 — Write phase result file
  - Sentinel: EXIT_RECOMMENDATION: CONTINUE

---

## Phase 7 — Release Spec Synthesis and Brainstorm Enrichment
## (roadmap Phase 6) — AMENDED: --file replaced with inline embedding
## Prerequisite: Phase 6 complete
## Milestone M6: Step 10 produces release spec passing G-010

- [ ] T07.01 — Load release spec template from src/superclaude/examples/release-spec-template.md
  - Verify file exists with all 13 sections and {{SC_PLACEHOLDER:*}} sentinels
  - Raise PortifyValidationError on missing file (D-007 dependency)

- [ ] T07.02 — Implement working copy creation (substep 3a)

- [ ] T07.03 — Implement template population: all 13 sections from Phase 1+2 outputs (substep 3b)

- [ ] T07.04 — Implement 3-persona brainstorm pass (substep 3c)
  - Personas: architect, analyzer, backend
  - Finding model: {gap_id, description, severity, affected_section, persona}

- [ ] T07.05 — Implement finding incorporation (substep 3d)
  - Actionable findings → body; unresolvable → Section 11

- [ ] T07.06 — AMENDED (from PRE-007): Implement inline embedding for large templates
  - If len(template_content) > 120 * 1024 (_EMBED_SIZE_LIMIT): raise PortifyValidationError
  - For content under 120KB: pass inline via -p to Claude subprocess
  - DO NOT use --file (broken, confirmed v2.24.5)
  - Reference or import _EMBED_SIZE_LIMIT from src/superclaude/cli/roadmap/executor.py

- [ ] T07.07 — Validate zero {{SC_PLACEHOLDER:*}} sentinels (FR-028)

- [ ] T07.08 — Validate Section 12 present (FR-029)

- [ ] T07.09 — Emit portify-release-spec.md with frontmatter {title, status, quality_scores}

- [ ] T07.10 — Enforce 900s timeout (NFR-001)

- [ ] T07.11 — Write phase result file
  - Sentinel: EXIT_RECOMMENDATION: CONTINUE

---

## Phase 8 — Panel Review Convergence Loop
## (roadmap Phase 7)
## Prerequisite: Phase 7 complete
## Milestone M7: Convergence or escalation deterministic; downstream_ready gated on score >=7.0

- [ ] T08.01 — Implement review.py with convergence state machine
  - States: NOT_STARTED → REVIEWING → INCORPORATING → SCORING → CONVERGED|ESCALATED (FR-030)

- [ ] T08.02 — Implement per-iteration logic (substeps 4a–4d)
  - 4a: 4-expert focus pass (Fowler, Nygard, Whittaker, Crispin)
  - 4b: finding incorporation (CRITICAL → mandatory, MAJOR → incorporated, MINOR → Section 11)
  - 4c: full panel critique with quality scoring (clarity, completeness, testability, consistency)
  - 4d: convergence scoring

- [ ] T08.03 — Implement CONVERGED condition: zero unaddressed CRITICALs → status: success (FR-032)

- [ ] T08.04 — Implement ESCALATED condition: 3 iterations exhausted → status: partial (FR-033)

- [ ] T08.05 — Gate downstream_ready on overall >= 7.0 (FR-034, NFR-005)

- [ ] T08.06 — Emit panel-report.md on BOTH CONVERGED and ESCALATED terminal conditions (FR-035)
  - panel-report.md is required in both paths (return contract references it in both)

- [ ] T08.07 — Emit updated portify-release-spec.md

- [ ] T08.08 — Use internal convergence loop (NOT outer retry mechanism — AC-011)

- [ ] T08.09 — Enforce 1200s timeout (NFR-001)

- [ ] T08.10 — Write phase result file
  - Sentinel: EXIT_RECOMMENDATION: CONTINUE

---

## Phase 9 — Observability Completion and Diagnostics
## (roadmap Phase 8)
## Prerequisite: Phase 8 complete
## Milestone M8: Failures diagnosable; TUI provides real-time visibility

- [ ] T09.01 — Complete PortifyTUI lifecycle: full real-time progress display via rich (NFR-008)
  - File: src/superclaude/cli/cli_portify/tui.py

- [ ] T09.02 — Complete OutputMonitor integration
  - File: src/superclaude/cli/cli_portify/monitor.py
  - Tracking: convergence iteration, findings count, placeholder count (NFR-009)

- [ ] T09.03 — Implement failure diagnostics collection
  - File: src/superclaude/cli/cli_portify/diagnostics.py
  - Fields: gate failure reason, exit code, missing artifacts, resume guidance (FR-042)

- [ ] T09.04 — Finalize execution-log.jsonl and execution-log.md with complete event coverage
  - File: src/superclaude/cli/cli_portify/logging_.py
  - Reference pattern from sprint/logging_.py (v2.25.7 battle-tested)

- [ ] T09.05 — Write phase result file
  - Sentinel: EXIT_RECOMMENDATION: CONTINUE

---

## Phase 10 — CLI Integration and Registration
## (roadmap Phase 9)
## Prerequisite: Phase 9 complete
## Milestone M9: superclaude cli-portify run is invokable

- [ ] T10.01 — Read src/superclaude/cli/main.py before making any changes
  - Confirm current registration pattern for existing command groups
  - Confirm no cli_portify already registered

- [ ] T10.02 — Implement commands.py with Click command group
  - File: src/superclaude/cli/cli_portify/commands.py
  - Subcommand: run
  - Options: --name, --output, --max-turns (default 200), --model, --dry-run, --resume, --debug

- [ ] T10.03 — Implement --dry-run: limit to PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION phase types (FR-037, SC-012)

- [ ] T10.04 — Register in src/superclaude/cli/main.py
  - main.add_command(cli_portify_group) per FR-048, AC-005
  - Match existing registration pattern in file

- [ ] T10.05 — Implement prompt splitting
  - If aggregate prompt length > 300 lines → split to portify-prompts.md (FR-050, AC-010)

- [ ] T10.06 — Verify module generation order enforced (NFR-006, AC-012)
  - Order: models → gates → prompts → config → inventory → monitor → process → executor → tui → logging_ → diagnostics → commands → __init__

- [ ] T10.07 — Write phase result file
  - Sentinel: EXIT_RECOMMENDATION: CONTINUE

---

## Phase 11 — Verification, Stabilization, and Release Readiness
## (roadmap Phase 10)
## Prerequisite: Phase 10 complete
## Milestone M10: All 14 success criteria validated; ready for merge

- [ ] T11.01 — Unit tests: all 5 validation error paths (NAME_COLLISION, OUTPUT_NOT_WRITABLE, AMBIGUOUS_PATH, INVALID_PATH, DERIVATION_FAILED)
  - File: tests/cli_portify/test_models.py

- [ ] T11.02 — Unit tests: all 12 gates with passing and failing inputs (SC-003, SC-004)

- [ ] T11.03 — Unit tests: _determine_status() exhaustively
  - Cover: PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, TIMEOUT, ERROR, INTERRUPTED
  - Reference freshness guard pattern from sprint/executor.py (v2.25.5-pass-no-report-fix)

- [ ] T11.04 — Unit tests: TurnLedger budget tracking and exhaustion

- [ ] T11.05 — Unit tests: exit code mapping and timeout classification (exit 124 → TIMEOUT, SC-014)

- [ ] T11.06 — Integration test: dry-run against real skill directory; assert no Phase 3–4 artifacts (SC-012)

- [ ] T11.07 — Integration test: resume flow across both review boundaries (SC-007)

- [ ] T11.08 — Integration test: signal handling (SIGINT → INTERRUPTED + return-contract emitted, SC-011)

- [ ] T11.09 — Integration test: gate failure + retry (missing EXIT_RECOMMENDATION → retry triggers)

- [ ] T11.10 — Edge case: ambiguous skill name raises AMBIGUOUS_PATH with candidate list

- [ ] T11.11 — Edge case: name collision with non-portified module raises NAME_COLLISION before any work

- [ ] T11.12 — Edge case: budget exhaustion mid-pipeline → HALTED with resume_command in contract

- [ ] T11.13 — Edge case: convergence ESCALATED path → panel-report.md emitted, downstream_ready=false

- [ ] T11.14 — Edge case: template > 120KB raises PortifyValidationError (amended from >50KB --file)
  - Replaces original SC edge case for "template >50KB" — behavior changed by PRE-007 amendment

- [ ] T11.15 — Run full project test suite: `uv run pytest`
  - Accept: zero failures; no regressions in sprint/, roadmap/, tasklist/ suites

- [ ] T11.16 — Validate all 14 success criteria SC-001 through SC-014
  - Produce validation report at: .dev/portify-workdir/validation-report.md

- [ ] T11.17 — Perform sample runs
  - Valid workflow end-to-end
  - Ambiguous workflow (error path)
  - Insufficient turn budget (HALTED path)
  - Interrupted execution (SIGINT path)
  - Escalation case (3 iterations, partial)

- [ ] T11.18 — Confirm logs and workdir artifacts are scoped correctly (no source-tree writes during execution)

- [ ] T11.19 — Write final release readiness checklist
  - Path: .dev/portify-workdir/release-readiness.md
  - Sign off: all SC-001–SC-014 passing, all risks mitigated, main.py integration verified
