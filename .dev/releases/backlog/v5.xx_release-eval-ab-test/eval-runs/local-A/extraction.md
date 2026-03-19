---
spec_source: "eval-spec.md"
generated: "2026-03-19T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 10
nonfunctional_requirements: 5
total_requirements: 15
complexity_score: 0.45
complexity_class: MEDIUM
domains_detected: [backend, cli, observability, testing]
risks_identified: 4
dependencies_identified: 8
success_criteria_count: 7
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 50.0, started_at: "2026-03-19T17:05:06.050215+00:00", finished_at: "2026-03-19T17:05:56.059047+00:00"}
---

## Functional Requirements

- **FR-001** (from FR-EVAL-001.1): After each pipeline step completes (pass or fail), write a JSON entry to the progress file containing `step_id`, `status` (pass/fail/skip), `duration_ms`, `gate_verdict` (pass/fail/null), and `output_file`.
- **FR-002** (from FR-EVAL-001.1): Progress file must be created on first step completion and remain valid JSON after every write (no partial/corrupt states).
- **FR-003** (from FR-EVAL-001.1): Parallel steps (generate-A, generate-B) must produce independent entries with correct per-step timing.
- **FR-004** (from FR-EVAL-001.2): Add `--progress-file` CLI option to `superclaude roadmap run` accepting a file path argument, defaulting to `{output_dir}/progress.json`.
- **FR-005** (from FR-EVAL-001.2): Validate `--progress-file` path before pipeline starts (parent directory must exist). Overwrite existing file rather than append.
- **FR-006** (from FR-EVAL-001.3): In `--dry-run` mode, output a Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks — covering all steps including conditional ones (remediate, certify), explicitly marking conditional steps.
- **FR-007** (from FR-EVAL-001.4): Capture each deviation analysis iteration within the spec-fidelity convergence loop as a sub-entry in the progress file, recording the convergence loop's pass count.
- **FR-008** (from FR-EVAL-001.5): When remediation triggers, the progress entry for the remediate step must include `trigger_reason` and `finding_count`. Entry written only when remediation executes. Certification step entry must reference the remediation it validates.
- **FR-009** (from FR-EVAL-001.6): Wiring verification progress entry must include `unwired_count`, `orphan_count`, `blocking_count`, and `rollout_mode` from wiring gate configuration. Gate verdict must reflect `WIRING_GATE` semantic check results.
- **FR-010** (implicit): Implement `StepProgress` and `PipelineProgress` data models as specified in Section 4.5, with serialization to JSON.

## Non-Functional Requirements

- **NFR-001** (NFR-EVAL-001.1): Progress file write latency must be < 50ms per step, measured via step duration delta with/without progress reporting.
- **NFR-002** (NFR-EVAL-001.2): Progress file must survive pipeline crash — achieved via atomic writes (write-to-tmp + `os.replace()`). File must be valid JSON after any interruption.
- **NFR-003** (NFR-EVAL-001.3): `progress.py` must have zero import-time side effects — no I/O at import time.
- **NFR-004** (implicit): Progress reporting must not alter existing pipeline behavior — callback is additive, no signature changes to existing methods.
- **NFR-005** (implicit): `summary()` method addition to gate constants must be backward-compatible — additive only, no changes to existing gate constant interfaces.

## Complexity Assessment

**Score**: 0.45 / **Class**: MEDIUM

**Rationale**:
- **Integration surface** is moderate: one new file (`progress.py`), three modified files (`executor.py`, `commands.py`, `gates.py`). No deep architectural changes.
- **Callback mechanism** is straightforward — hooks into existing `execute_pipeline()` post-step flow. No threading, no new concurrency.
- **Atomic file write** pattern (`write-to-tmp` + `os.replace()`) is well-understood and low-risk.
- **Complexity drivers**: deviation analysis sub-reporting (FR-007) requires understanding the convergence loop internals; wiring verification integration (FR-009) crosses module boundaries into `audit/wiring_gate.py`.
- **Ambiguity tax**: Two intentionally seeded ambiguities (deviation sub-entry schema, "significant findings" threshold) add design overhead but are flagged as eval artifacts.

## Architectural Constraints

1. **Single new file only**: All progress logic must reside in `src/superclaude/cli/roadmap/progress.py`. No new directories or ancillary modules.
2. **Callback-based integration**: Progress reporting hooks into `execute_pipeline()` via post-step callback — no separate observer threads or file watchers.
3. **Atomic JSON writes**: Progress file must use write-to-tmp + `os.replace()` pattern. No JSONL append, no partial writes.
4. **Click CLI framework**: `--progress-file` option must be registered as a `click.Path` parameter in `commands.py`.
5. **No gate logic changes**: The gate validation logic in `gates.py` must not be modified — only an additive `summary()` method is permitted.
6. **Sequential callback invocation**: Even for parallel steps, `on_step_complete` is invoked sequentially by `execute_pipeline()`, eliminating concurrency concerns for the progress writer.
7. **Module dependency direction**: `progress.py` depends on `models.py` and `gates.py` — never the reverse.

## Risk Inventory

1. **RISK-001** (Low severity): Progress writes slow down pipeline. *Mitigation*: Write is < 50ms; pipeline steps take minutes. NFR-001 enforces measurement.
2. **RISK-002** (Medium severity): Concurrent generate steps corrupt progress file. *Mitigation*: Callback is invoked sequentially by `execute_pipeline()` even for parallel steps — no concurrent writes occur.
3. **RISK-003** (High severity): Gate `summary()` method breaks existing gate constants. *Mitigation*: Method is purely additive with no signature changes to existing methods.
4. **RISK-004** (Medium severity): Undefined deviation sub-entry schema (GAP-002) causes implementation ambiguity. *Mitigation*: Acknowledged eval-seeded ambiguity — requires schema design decision before implementation. Flagged as open question.

## Dependency Inventory

1. **`src/superclaude/cli/roadmap/executor.py`** — Primary integration target; `execute_pipeline()` callback mechanism and `_build_steps()`.
2. **`src/superclaude/cli/roadmap/commands.py`** — Click command registration for `--progress-file` option.
3. **`src/superclaude/cli/roadmap/gates.py`** — Gate constant definitions; target for `summary()` method.
4. **`src/superclaude/cli/roadmap/models.py`** — `StepResult` dataclass used by progress entries.
5. **`src/superclaude/cli/roadmap/convergence.py`** — Convergence engine for deviation-analysis sub-reporting hooks.
6. **`src/superclaude/cli/audit/wiring_gate.py`** — `WIRING_GATE` definition used in wiring-verification step.
7. **Python stdlib `os.replace()`** — Atomic file replacement for crash-safe writes.
8. **Python stdlib `json`** — JSON serialization of progress data.

## Success Criteria

1. **SC-001**: A full pipeline run produces a `progress.json` file containing one entry per executed step, with all fields populated (`step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`).
2. **SC-002**: `progress.json` is valid JSON at all times — verified by interrupting a pipeline mid-run and parsing the file.
3. **SC-003**: `--dry-run` output includes a Markdown table listing all 13 gate definitions with tier, required fields, and semantic check counts.
4. **SC-004**: Parallel steps (generate-A, generate-B) have independent, accurate `duration_ms` values that reflect their actual execution time.
5. **SC-005**: `--progress-file /custom/path.json` writes to the specified path; default writes to `{output_dir}/progress.json`.
6. **SC-006**: Progress file write adds < 50ms overhead per step (NFR-001).
7. **SC-007**: `import superclaude.cli.roadmap.progress` produces zero file I/O side effects (NFR-003).

## Open Questions

1. **OQ-001** (GAP-002, Medium): What is the JSON schema for deviation analysis sub-entries within `progress.json`? The convergence loop may produce 1–N iterations, but no nesting structure or field set is defined. **Blocks**: FR-007 implementation and data model validation.
2. **OQ-002** (GAP-003, Medium): What constitutes "significant findings" that trigger remediation (FR-008)? The spec-fidelity gate uses HIGH severity findings as the trigger, but FR-EVAL-001.5 uses "significant" without defining a threshold. **Blocks**: Deterministic acceptance testing of FR-008.
3. **OQ-003** (GAP-001, Low): Should the progress file have rotation or size limits? For long-running or repeated pipeline executions, the file could grow unbounded. Current spec says overwrite on each run, but no retention policy is defined.
4. **OQ-004**: FR-EVAL-001.2 says "overwrite if exists" but integration test `test_resume_preserves_progress` (Section 8.2) says `--resume` should append to existing progress without overwriting. These are contradictory — clarification needed on resume behavior vs. fresh-run behavior.
5. **OQ-005**: The `metadata` field on `StepProgress` is an open `dict` with no schema constraints. What metadata keys are expected for standard steps vs. special steps (wiring, remediation, deviation)?
