---
spec_source: "eval-spec.md"
generated: "2026-03-19T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 12
nonfunctional_requirements: 5
total_requirements: 17
complexity_score: 0.45
complexity_class: MEDIUM
domains_detected: [backend, cli, observability, testing]
risks_identified: 4
dependencies_identified: 8
success_criteria_count: 9
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 55.0, started_at: "2026-03-19T17:19:23.348141+00:00", finished_at: "2026-03-19T17:20:18.358932+00:00"}
---

## Functional Requirements

- **FR-001** — Progress File Writer: After each pipeline step completes (pass or fail), write a JSON entry to the progress file containing `step_id`, `status` (pass/fail/skip), `duration_ms`, `gate_verdict` (pass/fail/null), and `output_file`. *(Source: FR-EVAL-001.1)*
- **FR-002** — Progress file creation on first step completion. *(Source: FR-EVAL-001.1 AC1)*
- **FR-003** — Progress file must be valid JSON after every write (no partial/corrupt states). Achieved via atomic write-to-tmp + `os.replace()`. *(Source: FR-EVAL-001.1 AC3, NFR-EVAL-001.2)*
- **FR-004** — Parallel steps (generate-A, generate-B) produce independent entries with correct per-step timing. *(Source: FR-EVAL-001.1 AC4)*
- **FR-005** — CLI Option `--progress-file PATH` added to `superclaude roadmap run`, accepting a file path argument. Default: `{output_dir}/progress.json`. *(Source: FR-EVAL-001.2)*
- **FR-006** — Progress file path validated before pipeline starts (parent directory must exist). *(Source: FR-EVAL-001.2 AC3)*
- **FR-007** — If progress file already exists, it is overwritten (not appended). *(Source: FR-EVAL-001.2 AC4)*
- **FR-008** — Dry-Run Gate Summary: When `--dry-run` is used, output includes a Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks. All steps including conditional ones (remediate, certify) are listed and conditional steps are explicitly marked. *(Source: FR-EVAL-001.3)*
- **FR-009** — Deviation Analysis Sub-Reporting: Each deviation analysis iteration within the spec-fidelity convergence loop produces a sub-entry in the progress file, and the convergence loop's pass count is recorded. *(Source: FR-EVAL-001.4)*
- **FR-010** — Remediation Trigger Reporting: When remediation is triggered, the progress entry includes `trigger_reason` and `finding_count`. Entry is only written when remediation actually executes. Certification step entry references the remediation it validates. *(Source: FR-EVAL-001.5)*
- **FR-011** — Wiring Verification Integration: Wiring step progress entry includes `unwired_count`, `orphan_count`, `blocking_count`, and `rollout_mode` from wiring gate configuration. Gate verdict reflects `WIRING_GATE` semantic check results. *(Source: FR-EVAL-001.6)*
- **FR-012** — Gate constants in `gates.py` expose a `summary()` method for dry-run reporting. *(Source: Section 4.2, implicit from FR-008)*

## Non-Functional Requirements

- **NFR-001** — Progress file write latency < 50ms per step. Measured via step duration delta with/without progress writing. *(Source: NFR-EVAL-001.1)*
- **NFR-002** — Progress file must survive pipeline crash — atomic writes via write-to-tmp + `os.replace()` ensure valid JSON after any interruption. *(Source: NFR-EVAL-001.2)*
- **NFR-003** — No import-time side effects in `progress.py` — zero I/O at import time. Verified by importing module and checking no files created. *(Source: NFR-EVAL-001.3)*
- **NFR-004** — Sequential callback invocation: `on_step_complete` callback is invoked sequentially by `execute_pipeline()` even for parallel steps, preventing concurrent write corruption. *(Source: Section 7, Risk row 2 — implicit constraint)*
- **NFR-005** — Additive-only changes to gate constants: `summary()` method must not alter signatures of existing methods. *(Source: Section 7, Risk row 3 — implicit constraint)*

## Complexity Assessment

**Score**: 0.45 / 1.0
**Class**: MEDIUM

**Rationale**:
- **Integration surface** is moderate — touches 3 existing files (`executor.py`, `commands.py`, `gates.py`) plus 1 new file (`progress.py`). No deep refactoring required.
- **Data model** is straightforward — two dataclasses (`StepProgress`, `PipelineProgress`) with simple serialization.
- **Concurrency concern** is pre-mitigated by the existing sequential callback architecture.
- **Atomic file writing** is a well-understood pattern (`write-to-tmp` + `os.replace()`).
- **Two seeded ambiguities** (deviation sub-entry schema, "significant findings" threshold) add minor specification risk but are acknowledged as intentional.
- **No new external dependencies** — pure Python stdlib plus existing project infrastructure.

Complexity is driven primarily by the number of integration points and the need to handle edge cases (parallel steps, crash safety, conditional steps) rather than algorithmic difficulty.

## Architectural Constraints

1. **Single new file only**: All progress reporting logic must reside in `src/superclaude/cli/roadmap/progress.py`. No additional new files.
2. **Callback-based integration**: Progress reporting hooks into the existing `execute_pipeline()` callback mechanism — no separate observer threads or file watchers.
3. **Atomic JSON writes**: Progress file must use write-to-tmp + `os.replace()` pattern. Not JSONL, not CSV, not YAML.
4. **Click CLI framework**: `--progress-file` option must be registered as a `click.Path` option on the existing `roadmap run` command.
5. **No modifications to gate validation logic**: Gate enforcement in `pipeline/gates.py` is out of scope. Only additive `summary()` method on gate constants.
6. **Existing data model dependency**: Must extend/use `StepResult` from `models.py`; progress entries map to pipeline steps as defined by `_build_steps()` in `executor.py`.
7. **Python ≥3.10**: Uses `list[StepProgress]` syntax (PEP 585) and `dataclasses`.
8. **UV-only execution**: All test and run commands via `uv run`.

## Risk Inventory

1. **RISK-001** (Low severity) — Progress writes slow down pipeline. *Mitigation*: Write is < 50ms; pipeline steps take minutes. Negligible overhead.
2. **RISK-002** (Medium severity) — Concurrent generate steps corrupt progress file. *Mitigation*: `on_step_complete` callback is invoked sequentially by `execute_pipeline()` even for parallel steps.
3. **RISK-003** (High severity) — Gate summary method breaks existing gate constants. *Mitigation*: `summary()` is additive only, no signature changes to existing methods.
4. **RISK-004** (Medium severity) — Seeded ambiguities (GAP-002, GAP-003) propagate to implementation as undefined behavior. *Mitigation*: These are intentional eval artifacts; resolution requires stakeholder clarification before implementation proceeds past spec-fidelity gate.

## Dependency Inventory

| # | Dependency | Type | Location |
|---|-----------|------|----------|
| 1 | `src/superclaude/cli/roadmap/executor.py` | Internal module | `execute_pipeline()` callback mechanism, `_build_steps()`, `_save_roadmap_state()` |
| 2 | `src/superclaude/cli/roadmap/commands.py` | Internal module | Click command registration, `--dry-run` handling |
| 3 | `src/superclaude/cli/roadmap/models.py` | Internal module | `StepResult` dataclass |
| 4 | `src/superclaude/cli/roadmap/gates.py` | Internal module | Gate constant definitions |
| 5 | `src/superclaude/cli/roadmap/convergence.py` | Internal module | Convergence loop for deviation analysis sub-reporting |
| 6 | `src/superclaude/cli/audit/wiring_gate.py` | Internal module | `WIRING_GATE` definition |
| 7 | Python `os` stdlib | External (stdlib) | `os.replace()` for atomic file writes |
| 8 | Python `json` stdlib | External (stdlib) | JSON serialization |

## Success Criteria

1. **SC-001**: `progress.json` is created after first pipeline step and contains valid JSON after every subsequent step completion.
2. **SC-002**: Each progress entry contains all 5 required fields: `step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`.
3. **SC-003**: `--progress-file` CLI option is accepted and validated; pipeline fails fast if parent directory does not exist.
4. **SC-004**: Default progress file path resolves to `{output_dir}/progress.json` when option is not specified.
5. **SC-005**: `--dry-run` output includes a Markdown table with Step, Gate Tier, Required Fields, and Semantic Checks columns for all 13 gate definitions.
6. **SC-006**: Wiring verification entry includes `unwired_count`, `orphan_count`, `blocking_count`, and `rollout_mode`.
7. **SC-007**: Progress file write latency < 50ms per step (measured by benchmarking).
8. **SC-008**: Progress file survives simulated crash — file is valid JSON even if pipeline is killed mid-write.
9. **SC-009**: `import superclaude.cli.roadmap.progress` produces zero filesystem I/O (no import-time side effects).

## Open Questions

1. **OQ-001** (Medium, Blocking) — **Deviation sub-entry schema undefined**: FR-EVAL-001.4 specifies that deviation analysis iterations produce sub-entries but does not define the JSON schema for these sub-entries. How do they nest inside `PipelineProgress.steps`? Are they child entries of the spec-fidelity `StepProgress`, or top-level entries with a parent reference? *(Source: GAP-002, EVAL-SEEDED-AMBIGUITY)*

2. **OQ-002** (Medium, Blocking) — **"Significant findings" threshold undefined**: FR-EVAL-001.5 uses "significant findings" as the remediation trigger condition but does not define what qualifies as significant. Section 3 mentions "HIGH severity findings" in the seeded ambiguity comment, but the acceptance criteria say "significant." Which threshold applies? *(Source: GAP-003, EVAL-SEEDED-AMBIGUITY)*

3. **OQ-003** (Low) — **Progress file rotation/size limits**: No specification for what happens when progress files grow large across many runs. Is rotation or size-limiting needed? *(Source: GAP-001)*

4. **OQ-004** (Low) — **Resume behavior**: Section 8.2 mentions `test_resume_preserves_progress` (resume appends to existing progress file without overwriting), but FR-EVAL-001.2 AC4 states "if progress file already exists, it is overwritten." These contradict. Which behavior applies on `--resume`?

5. **OQ-005** (Low) — **Section 4.3 missing**: The spec jumps from Section 4.2 to Section 4.4, suggesting a deleted or omitted section. Was content planned for 4.3?

6. **OQ-006** (Low) — **Metadata field usage**: `StepProgress.metadata` is defined as `dict` but no requirements specify what keys populate it. Is this an extension point, or should specific keys be mandated?
