```yaml
---
title: "Pipeline Progress Reporting for Roadmap Executor"
version: "1.0.0"
status: draft
feature_id: FR-EVAL-001
parent_feature: null
spec_type: new_feature
complexity_score: 0.45
complexity_class: MEDIUM
target_release: v3.1.0-eval
authors: [user, claude]
created: 2026-03-19
quality_scores:
  clarity: 8.0
  completeness: 7.5
  testability: 8.5
  consistency: 7.0
  overall: 7.8
---
```

## 1. Problem Statement

The `superclaude roadmap run` pipeline executor (`src/superclaude/cli/roadmap/executor.py`) lacks structured progress reporting. When a 10-step pipeline runs, operators have no machine-readable way to track which steps completed, how long each took, or what gate results were produced. The only feedback is log lines and final exit codes.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| Pipeline runs produce no structured progress file | `src/superclaude/cli/roadmap/executor.py` | Operators cannot build dashboards or alerting on pipeline health |
| `.roadmap-state.json` tracks resume state but not timing or gate verdicts per step | `src/superclaude/cli/roadmap/executor.py:_save_roadmap_state()` | No post-hoc analysis of pipeline performance |
| `--dry-run` mode reports steps but not expected gate criteria | `src/superclaude/cli/roadmap/commands.py` | Dry-run output is less useful for pre-flight validation |

### 1.2 Scope Boundary

**In scope**: Adding a `progress.json` file written after each step completes, enriching `--dry-run` output with gate summaries, and adding a `--progress-file` CLI option.

**Out of scope**: Real-time streaming progress (WebSocket/SSE), GUI dashboards, modifications to the gate validation logic itself, changes to `pipeline/gates.py` enforcement code.

## 2. Solution Overview

Add a lightweight progress reporter that writes a JSON file after each pipeline step completes. The reporter hooks into the existing `execute_pipeline()` callback mechanism. A new `--progress-file` CLI option controls the output path. `--dry-run` mode is enriched to include gate criteria summaries in its output.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Progress format | Wrapped JSON with atomic rewrite (write to `.tmp` + `os.replace()`) | CSV, YAML, JSONL (append-safe but not valid JSON) | JSON is parseable by all downstream tools; atomic rewrite ensures crash-safe valid JSON; single-file avoids directory sprawl |
| Hook mechanism | Post-step callback in `execute_pipeline()` | Separate observer thread, file watcher | Callback is simplest; no threading complexity |
| Gate summary in dry-run | Inline Markdown table | Separate file, structured YAML | Consistent with existing dry-run output format |

### 2.2 Workflow / Data Flow

```
spec.md
  |
  v
[extract] --> progress.json (step 1 entry)
  |
  v
[generate-A] + [generate-B] --> progress.json (step 2-3 entries)
  |
  v
[diff] --> progress.json (step 4 entry)
  |
  v
[debate] --> progress.json (step 5 entry)
  |
  v
[score] --> progress.json (step 6 entry)
  |
  v
[merge] --> progress.json (step 7 entry)
  |
  v
[test-strategy] --> progress.json (step 8 entry)
  |
  v
[spec-fidelity] --> progress.json (step 9 entry)
  |     |
  |     +--[deviation-analysis loop]--> progress.json (sub-entries)
  |
  v
[wiring-verification] --> progress.json (step 10 entry)
  |
  v (conditional: spec-fidelity FAIL with HIGH findings)
[remediate] --> progress.json (step 11 entry)
  |
  v
[certify] --> progress.json (step 12 entry)
```

## 3. Functional Requirements

### FR-EVAL-001.1: Progress File Writer

**Description**: After each pipeline step completes (pass or fail), write a JSON entry to the progress file containing step ID, status, duration, gate verdict, and output file path.

**Acceptance Criteria**:
- [ ] Progress file is created on first step completion
- [ ] Each entry contains: `step_id`, `status` (pass/fail/skip), `duration_ms`, `gate_verdict` (pass/fail/null), `output_file`
- [ ] File is valid JSON after every write (not partial/corrupt)
- [ ] Parallel steps (generate-A, generate-B) produce independent entries with correct timing

**Dependencies**: `src/superclaude/cli/roadmap/executor.py` (`execute_pipeline` callback), `src/superclaude/cli/roadmap/models.py` (`StepResult`)

### FR-EVAL-001.2: CLI Option for Progress File

**Description**: Add `--progress-file` option to `superclaude roadmap run` that specifies where to write progress output.

**Acceptance Criteria**:
- [ ] Option accepts a file path argument
- [ ] Default value is `{output_dir}/progress.json`
- [ ] Option is validated before pipeline starts (parent directory must exist)
- [ ] If progress file already exists, it is overwritten (not appended to)

**Dependencies**: `src/superclaude/cli/roadmap/commands.py` (Click option registration)

### FR-EVAL-001.3: Dry-Run Gate Summary

**Description**: When `--dry-run` is used, include a table of all pipeline steps with their gate criteria (required frontmatter fields count, semantic check count, enforcement tier).

**Acceptance Criteria**:
- [ ] Dry-run output includes a Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks
- [ ] All steps including conditional ones (remediate, certify) are listed
- [ ] Output explicitly marks conditional steps

**Dependencies**: `src/superclaude/cli/roadmap/gates.py` (gate constant definitions), `src/superclaude/cli/roadmap/commands.py`

### FR-EVAL-001.4: Deviation Analysis Sub-Reporting

<!-- EVAL-SEEDED-AMBIGUITY: This requirement intentionally omits the data schema for deviation sub-entries in progress.json. The convergence loop may produce 1-N deviation analysis iterations, but no format is specified for how these nest inside the progress file. This will produce a BLOCKING finding in spec-fidelity because the data model (Section 4.5) cannot be validated against an undefined schema. -->

**Description**: The progress reporter should capture deviation analysis iterations that occur within the spec-fidelity convergence loop and include them in the progress output.

**Acceptance Criteria**:
- [ ] Each deviation analysis iteration produces a sub-entry in the progress file
- [ ] The convergence loop's pass count is recorded

**Dependencies**: `src/superclaude/cli/roadmap/convergence.py`

### FR-EVAL-001.5: Remediation Trigger Reporting

<!-- EVAL-SEEDED-AMBIGUITY: This requirement uses "significant findings" without defining the threshold. The spec-fidelity gate defines HIGH severity findings as the trigger for remediation, but this requirement says "significant" which is ambiguous. This will produce a WARNING finding because the acceptance criteria cannot be deterministically verified. -->

**Description**: When the pipeline triggers remediation due to significant findings in spec-fidelity, the progress file should record the trigger condition and finding count.

**Acceptance Criteria**:
- [ ] Progress entry for remediate step includes `trigger_reason` and `finding_count`
- [ ] Entry is only written when remediation actually executes
- [ ] Certification step entry references the remediation it validates

**Dependencies**: `src/superclaude/cli/roadmap/executor.py` (remediate/certify conditional logic)

### FR-EVAL-001.6: Wiring Verification Integration

**Description**: The progress reporter must capture wiring verification results including the count of unwired symbols, orphan modules, and blocking findings.

**Acceptance Criteria**:
- [ ] Wiring step progress entry includes `unwired_count`, `orphan_count`, `blocking_count`
- [ ] Entry includes `rollout_mode` from the wiring gate configuration
- [ ] Gate verdict correctly reflects `WIRING_GATE` semantic check results

**Dependencies**: `src/superclaude/cli/audit/wiring_gate.py` (WIRING_GATE), `src/superclaude/cli/roadmap/executor.py`

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/cli/roadmap/progress.py` | Progress file writer class | `models.py`, `gates.py` |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/cli/roadmap/executor.py` | Add progress callback invocation after each step | Core integration point |
| `src/superclaude/cli/roadmap/commands.py` | Add `--progress-file` Click option | CLI surface expansion |
| `src/superclaude/cli/roadmap/gates.py` | Add `summary()` method to gate constants for dry-run reporting | Dry-run enrichment |

### 4.4 Module Dependency Graph

```
commands.py ──> executor.py ──> progress.py (new)
                    |                |
                    v                v
               gates.py         models.py
                    |
                    v
          audit/wiring_gate.py
```

### 4.5 Data Models

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class StepProgress:
    """Progress entry for a single pipeline step."""
    step_id: str
    status: str  # "pass", "fail", "skip"
    duration_ms: int
    gate_verdict: Optional[str]  # "pass", "fail", None
    output_file: Optional[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class PipelineProgress:
    """Aggregate progress for the full pipeline run."""
    spec_file: str
    started_at: str  # ISO 8601
    steps: list[StepProgress] = field(default_factory=list)
    completed: bool = False
```

### 4.6 Implementation Order

```
1. Create progress.py with StepProgress/PipelineProgress models  -- foundation
2. Add --progress-file option to commands.py                      -- CLI surface
   Add summary() to gate constants in gates.py                    -- [parallel with step 2]
3. Wire progress callback into executor.py                        -- depends on 1, 2
4. Enrich --dry-run output with gate summary table                -- depends on 2
5. Add deviation sub-reporting in convergence loop                -- depends on 3
```

## 5. Interface Contracts

### 5.1 CLI Surface

```
superclaude roadmap run SPEC_FILE [OPTIONS]

New option:
  --progress-file PATH   Write step-by-step progress to PATH
                         (default: {output_dir}/progress.json)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--progress-file` | `click.Path` | `{output_dir}/progress.json` | Path to write pipeline progress JSON |

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-EVAL-001.1 | Progress file write latency | < 50ms per step | Measured via step duration delta with/without progress |
| NFR-EVAL-001.2 | Progress file must survive pipeline crash | Atomic writes via write-to-tmp + `os.replace()` | File is valid JSON after any interruption |
| NFR-EVAL-001.3 | No import-time side effects in progress.py | Zero I/O at import | Verified by importing module and checking no files created |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Progress writes slow down pipeline | Low | Low | Write is < 50ms, pipeline steps take minutes |
| Concurrent generate steps corrupt progress file | Low | Medium | Mitigated: `on_step_complete` callback is invoked sequentially by `execute_pipeline()` even for parallel steps |
| Gate summary method breaks existing gate constants | Low | High | summary() is additive, no signature changes to existing methods |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_step_progress_serialization` | `tests/roadmap/test_progress.py` | StepProgress dataclass serializes to valid JSON |
| `test_pipeline_progress_append` | `tests/roadmap/test_progress.py` | Steps can be appended without corrupting file |
| `test_gate_summary_all_steps` | `tests/roadmap/test_progress.py` | Gate summary includes all 13 gate definitions |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `test_dry_run_includes_gate_table` | --dry-run output contains gate summary Markdown table |
| `test_full_pipeline_produces_progress` | End-to-end run writes progress.json with entries for all executed steps |
| `test_resume_preserves_progress` | --resume appends to existing progress file without overwriting |

## 10. Downstream Inputs

### For sc:roadmap
- Theme: "Observability" — adds pipeline introspection capability
- Milestone: Single phase, can be implemented in one sprint
- Complexity MEDIUM maps to interleave ratio 1:2 (1 validation milestone per 2 work milestones)

### For sc:tasklist
- 5 implementation tasks mapping to implementation order (Section 4.6)
- 3 test tasks mapping to unit + integration tests
- 1 documentation task for CLI help text updates

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| ~~OI-001~~ | ~~JSONL vs JSON array~~ — **Resolved**: wrapped JSON with atomic rewrite (`write-to-tmp` + `os.replace()`). See Section 2.1 and NFR-EVAL-001.2. | N/A | Resolved 2026-03-19 |

## 12. Brainstorm Gap Analysis

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| GAP-001 | No specification of progress file rotation or size limits | Low | Section 6 (NFR) | devops |
| GAP-002 | Deviation sub-entry schema undefined (intentional for eval) | Medium | Section 3 (FR-EVAL-001.4) | architect |
| GAP-003 | "Significant findings" threshold undefined (intentional for eval) | Medium | Section 3 (FR-EVAL-001.5) | qa |

These gaps are acknowledged. GAP-002 and GAP-003 are intentional eval-seeded ambiguities designed to trigger spec-fidelity findings.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Gate verdict | The pass/fail result of a `GateCriteria` evaluation against a step's output file |
| Progress entry | A single JSON object representing one completed pipeline step |
| Convergence loop | The iterative spec-fidelity checking mechanism in `convergence.py` that may run deviation analysis multiple times |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `src/superclaude/cli/roadmap/executor.py` | Primary integration target; contains `_build_steps()` and `execute_roadmap()` |
| `src/superclaude/cli/roadmap/commands.py` | CLI surface where `--progress-file` will be added |
| `src/superclaude/cli/roadmap/gates.py` | Gate constant definitions; target for `summary()` enrichment |
| `src/superclaude/cli/main.py` | Entry point; confirms roadmap group is registered |
| `src/superclaude/cli/roadmap/convergence.py` | Convergence engine where deviation-analysis sub-reporting hooks in |
| `src/superclaude/cli/audit/wiring_gate.py` | WIRING_GATE definition used in wiring-verification step |
