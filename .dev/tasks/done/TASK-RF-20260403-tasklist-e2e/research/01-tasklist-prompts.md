# R01: Tasklist Prompts & Generation Code

**Source**: `src/superclaude/cli/tasklist/prompts.py`
**Researcher**: r01
**Status**: Complete
**Date**: 2026-04-02

---

## Module Overview

The module contains **two pure functions** (no I/O, no side effects per NFR-004) that build prompt strings for tasklist operations. Both import `_OUTPUT_FORMAT_BLOCK` from `superclaude.cli.roadmap.prompts` and append it at the end of the returned string.

**Validation layering guard** (module docstring): Tasklist fidelity checks roadmap-to-tasklist ONLY. It does NOT check spec-to-tasklist (that is the spec-fidelity step's job).

---

## 1. `build_tasklist_fidelity_prompt`

### Signature

```python
def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
```

### Purpose

Prompt for the **tasklist-fidelity validation step**. Instructs Claude to compare the roadmap against the generated tasklist, checking deliverable coverage, signature preservation, traceability ID validity, and dependency chain correctness.

### Base Prompt Content

The base prompt (always present) contains these sections in order:

1. **Role**: "You are a tasklist fidelity analyst."
2. **Instruction**: Read roadmap + tasklist files, compare systematically, identify deviations.
3. **Validation Layering Guard** (`## VALIDATION LAYERING GUARD`): Explicitly scopes validation to ROADMAP -> TASKLIST only. Five bullet points forbidding spec-level checks.
4. **Severity Definitions** (`## Severity Definitions`):
   - **HIGH**: Omits, contradicts, or fundamentally misrepresents a roadmap item. Tasklist cannot be used as-is. Examples: missing R-NNN mapping, fabricated D-NNNN, contradicted dependency chain, omitted deliverable outputs.
   - **MEDIUM**: Addresses roadmap item but with insufficient detail, ambiguous language, or minor misalignment. Examples: divergent effort estimate, weaker acceptance criteria, improperly sequenced dependency, differing verification method.
   - **LOW**: Minor stylistic, formatting, or organizational differences. Examples: different heading structure, terminology variations, missing cross-references.
5. **Comparison Dimensions** (`## Comparison Dimensions`) -- 5 numbered checks:
   1. Deliverable Coverage (D-NNNN matching)
   2. Signature Preservation (function/method/API signatures)
   3. Traceability ID Validity (R-NNN, D-NNNN back-trace; flag fabricated IDs)
   4. Dependency Chain Correctness
   5. Acceptance Criteria Completeness
6. **Output Requirements** (`## Output Requirements`): YAML frontmatter with fields:
   - `source_pair: roadmap-to-tasklist`
   - `upstream_file`, `downstream_file`
   - `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations` (integers)
   - `validation_complete` (boolean)
   - `tasklist_ready` (boolean) -- true ONLY if `high_severity_count == 0` AND `validation_complete == true`
7. **Deviation Report**: Numbered entries with DEV-NNN ID, Severity, Deviation, Upstream Quote, Downstream Quote (or `[MISSING]`), Impact, Recommended Correction.
8. **Summary**: Brief summary with severity distribution.

### TDD Conditional Block (`if tdd_file is not None`)

Appends `## Supplementary TDD Validation (when TDD file is provided)` with 5 checks:

| # | TDD Section Reference | Check |
|---|----------------------|-------|
| 1 | S15 Testing Strategy | Test cases should have corresponding validation/test tasks |
| 2 | S19 Migration & Rollout Plan | Rollback procedures should have contingency/rollback tasks |
| 3 | S10 Component Inventory | Components should have corresponding implementation tasks |
| 4 | S7 Data Models | Data model entities should have schema implementation tasks |
| 5 | S8 API Specifications | API endpoints should have endpoint implementation tasks |

**Severity for missing coverage**: MEDIUM

### PRD Conditional Block (`if prd_file is not None`)

Appends `## Supplementary PRD Validation (when PRD file is provided)` with 4 checks:

| # | PRD Section Reference | Check |
|---|----------------------|-------|
| 1 | S7 User Personas | Tasks touching user-facing flows should reference which persona is served |
| 2 | S19 Success Metrics | Should have corresponding instrumentation/measurement tasks |
| 3 | S12 Scope Definition + S22 Customer Journey Map | Acceptance scenarios should have corresponding verification tasks |
| 4 | S5 Business Context | Task priority should reflect business value hierarchy, not just technical dependency. Priority contradictions flagged as **LOW** severity. |

**Severity for missing coverage**: MEDIUM (except priority contradictions which are LOW)

### Return Value

`base + _OUTPUT_FORMAT_BLOCK`

---

## 2. `build_tasklist_generate_prompt`

### Signature

```python
def build_tasklist_generate_prompt(
    roadmap_file: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
```

### Purpose

Prompt for **tasklist generation** enriched with TDD/PRD source documents. Used by the `/sc:tasklist` skill protocol for inference-based generation workflows. **NOT** called by the CLI `tasklist validate` executor. There is no `tasklist generate` CLI subcommand -- generation is handled by the skill protocol reading this prompt builder directly.

### Base Prompt Content

1. **Role**: "You are a tasklist generator."
2. **Instruction**: Read roadmap, decompose into structured tasklist with actionable tasks. Each roadmap item should produce one or more tasks with:
   - Clear task title
   - Deliverable IDs traced to roadmap (R-NNN, D-NNNN)
   - Acceptance criteria
   - Effort estimate
   - Dependencies on other tasks
   - Verification method
3. **Organization**: Tasks organized by roadmap phase. Preserve all roadmap item IDs, deliverable IDs, and dependency chains exactly as specified.

### TDD Enrichment Block (`if tdd_file is not None`)

Appends `## Supplementary TDD Enrichment (for task generation)` with 5 enrichment items:

| # | TDD Section | Enrichment |
|---|-------------|------------|
| 1 | S15 Testing Strategy | Each test case maps to a validation task with exact test name and expected behavior |
| 2 | S8 API Specifications | Each endpoint has implementation tasks with request/response field details |
| 3 | S10 Component Inventory | Each component has tasks with prop types, dependencies, integration points |
| 4 | S19 Migration & Rollout | Each rollback procedure is a contingency task with trigger conditions |
| 5 | S7 Data Models | Each entity has schema implementation tasks with exact field types |

### PRD Enrichment Block (`if prd_file is not None`)

Appends `## Supplementary PRD Enrichment (for task generation)` with 5 enrichment items:

| # | PRD Section | Enrichment |
|---|-------------|------------|
| 1 | S7 User Personas | Tasks reference which persona is served and specific needs |
| 2 | S12 Scope Definition + S22 Customer Journey Map | Each acceptance criterion maps to a verification task |
| 3 | S19 Success Metrics | Tasks include metric instrumentation subtasks (tracking, dashboards, alerts) |
| 4 | S5 Business Context | Task priority reflects business value ordering, not just technical dependency |
| 5 | S12 Scope Definition | Tasks must not exceed defined scope; generate explicit "out of scope" markers |

**Key constraint**: "PRD context informs task descriptions and priorities but does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them."

### Combined TDD+PRD Block (`if tdd_file is not None and prd_file is not None`)

Appends `## TDD + PRD Interaction` with precedence rules:

- TDD provides **structural engineering detail**; PRD provides **product context**.
- **TDD takes precedence** for implementation specifics (test cases, schemas, components).
- **PRD shapes** task descriptions, acceptance criteria, and priority ordering.

### Return Value

`base + _OUTPUT_FORMAT_BLOCK`

---

## 3. `_OUTPUT_FORMAT_BLOCK` (imported from `roadmap/prompts.py`)

Defined at line 62 of `src/superclaude/cli/roadmap/prompts.py`. Appended to the end of every prompt. Content:

```
<output_format>
CRITICAL: Your response MUST begin with YAML frontmatter (--- delimited block).
Do NOT include any text, preamble, or commentary before the opening ---.
Do NOT say "Here is...", "Sure!", or any conversational text before the frontmatter.

Correct start:
---
key: value
---

Incorrect start:
Here is the output:
---
key: value
---
</output_format>
```

---

## 4. All Four Enrichment Scenarios

### Scenario A: No supplementary files (`tdd_file=None, prd_file=None`)

| Function | Sections Included |
|----------|------------------|
| `build_tasklist_fidelity_prompt` | Base (role + layering guard + severity defs + comparison dims + output reqs + deviation report + summary) + `_OUTPUT_FORMAT_BLOCK` |
| `build_tasklist_generate_prompt` | Base (role + instruction + organization) + `_OUTPUT_FORMAT_BLOCK` |

### Scenario B: TDD only (`tdd_file=<path>, prd_file=None`)

| Function | Additional Sections |
|----------|-------------------|
| `build_tasklist_fidelity_prompt` | + "Supplementary TDD Validation" (5 checks, MEDIUM severity) |
| `build_tasklist_generate_prompt` | + "Supplementary TDD Enrichment" (5 enrichment items) |

### Scenario C: PRD only (`tdd_file=None, prd_file=<path>`)

| Function | Additional Sections |
|----------|-------------------|
| `build_tasklist_fidelity_prompt` | + "Supplementary PRD Validation" (4 checks, MEDIUM/LOW severity) |
| `build_tasklist_generate_prompt` | + "Supplementary PRD Enrichment" (5 enrichment items + constraint note) |

### Scenario D: Both TDD and PRD (`tdd_file=<path>, prd_file=<path>`)

| Function | Additional Sections |
|----------|-------------------|
| `build_tasklist_fidelity_prompt` | + "Supplementary TDD Validation" + "Supplementary PRD Validation" |
| `build_tasklist_generate_prompt` | + "Supplementary TDD Enrichment" + "Supplementary PRD Enrichment" + "TDD + PRD Interaction" (precedence rules) |

**Key difference in Scenario D**: Only `build_tasklist_generate_prompt` adds the "TDD + PRD Interaction" section. The fidelity prompt does NOT have a combined interaction block.

---

## 5. Cross-references for Other Researchers

- **r02 (skill protocol)**: `build_tasklist_generate_prompt` is called by the `/sc:tasklist` skill protocol, not the CLI executor. The skill protocol reads this prompt builder directly.
- **r03 (executor/CLI)**: `build_tasklist_fidelity_prompt` is the one used by the CLI `tasklist validate` command. There is no `tasklist generate` CLI subcommand.
- **r04 (roadmap artifacts)**: The fidelity prompt expects roadmap files with R-NNN item IDs and D-NNNN deliverable IDs. YAML frontmatter output includes `source_pair: roadmap-to-tasklist`.
- **r05 (MDTM templates)**: Generated tasks should include: task title, deliverable IDs (R-NNN, D-NNNN), acceptance criteria, effort estimate, dependencies, verification method.

---

## 6. Testing Implications

For E2E validation of the prompt builders:

1. **Unit tests** should verify all 4 scenarios (A-D) for both functions, checking substring presence/absence of each conditional block.
2. **The fidelity prompt** can be tested by asserting YAML frontmatter field names appear in the output.
3. **The generate prompt** can be tested by asserting the "TDD + PRD Interaction" section appears ONLY in Scenario D.
4. **Severity classification** should be tested: TDD validation flags MEDIUM, PRD validation flags MEDIUM (except priority contradictions = LOW).
5. **`_OUTPUT_FORMAT_BLOCK`** is always appended -- assert it appears at the end of every returned string.
