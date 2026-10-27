# Merged Refactoring Plan — v3.05 Spec

> Generated: 2026-03-20
> Target: `deterministic-fidelity-gate-requirements.md` (v1.1.0)
> Issues resolved: 23 of 24 (ISS-004 superseded by ISS-003)
> Apply top-to-bottom in a single pass against the spec.

---

## How to Use This Document

Each change block below specifies:
- **Location**: Line range or insertion point in the current spec
- **Action**: INSERT / REPLACE / DELETE
- **Provenance**: Which ISS-NNN contributed each piece
- **Before**: Current spec text (for verification)
- **After**: New text to apply

Changes are ordered by spec position (top-to-bottom). Apply sequentially — later changes assume earlier changes have been applied.

---

## Change 1: YAML Frontmatter — Remove Dead Code + Add Disposition Table

**Location**: Lines 1–24 (YAML frontmatter block)
**Action**: DELETE line 16 (`fidelity.py`), DELETE line 19 (`deviation_registry.py`), INSERT `spec_patch.py`, INSERT `module_disposition` block after `relates_to`
**Provenance**: ISS-020 (delete fidelity.py), ISS-008 (delete deviation_registry.py), ISS-011 (add spec_patch.py), ISS-001 #3 supplement (module_disposition)

### Before (lines 10–24):

```yaml
relates_to:
  - src/superclaude/cli/roadmap/executor.py
  - src/superclaude/cli/roadmap/prompts.py
  - src/superclaude/cli/roadmap/gates.py
  - src/superclaude/cli/roadmap/remediate.py
  - src/superclaude/cli/roadmap/remediate_executor.py
  - src/superclaude/cli/roadmap/fidelity.py
  - src/superclaude/cli/roadmap/convergence.py
  - src/superclaude/cli/roadmap/semantic_layer.py
  - src/superclaude/cli/roadmap/deviation_registry.py
  - src/superclaude/cli/roadmap/structural_checkers.py
  - src/superclaude/cli/roadmap/spec_parser.py
  - src/superclaude/cli/roadmap/models.py
  - src/superclaude/cli/roadmap/commands.py
---
```

### After:

```yaml
relates_to:
  - src/superclaude/cli/roadmap/executor.py
  - src/superclaude/cli/roadmap/prompts.py
  - src/superclaude/cli/roadmap/gates.py
  - src/superclaude/cli/roadmap/remediate.py
  - src/superclaude/cli/roadmap/remediate_executor.py
  - src/superclaude/cli/roadmap/convergence.py
  - src/superclaude/cli/roadmap/semantic_layer.py
  - src/superclaude/cli/roadmap/structural_checkers.py
  - src/superclaude/cli/roadmap/spec_parser.py
  - src/superclaude/cli/roadmap/spec_patch.py
  - src/superclaude/cli/roadmap/models.py
  - src/superclaude/cli/roadmap/commands.py
baseline_commit: f4d9035
module_disposition:
  - file: src/superclaude/cli/roadmap/convergence.py
    action: MODIFY
    lines: 323
    extends_frs: [FR-6, FR-7, FR-8, FR-10]
  - file: src/superclaude/cli/roadmap/semantic_layer.py
    action: MODIFY
    lines: 337
    extends_frs: [FR-4, FR-4.1, FR-4.2, FR-5]
  - file: src/superclaude/cli/roadmap/remediate_executor.py
    action: MODIFY
    lines: 563
    extends_frs: [FR-9]
  - file: src/superclaude/cli/roadmap/spec_parser.py
    action: CREATE
    extends_frs: [FR-2]
  - file: src/superclaude/cli/roadmap/structural_checkers.py
    action: CREATE
    extends_frs: [FR-1]
  - file: src/superclaude/cli/roadmap/fidelity.py
    action: DELETE
    note: "Dead code — zero imports"
  - file: src/superclaude/cli/roadmap/deviation_registry.py
    action: REMOVE_FROM_MANIFEST
    note: "Class exists inside convergence.py:50-225, no separate file"
pre_satisfied_count: 19
---
```

**Changes made**:
- Removed `fidelity.py` (ISS-020: dead code, zero imports)
- Removed `deviation_registry.py` (ISS-008: phantom file, class lives in convergence.py)
- Added `spec_patch.py` (ISS-011: active module not listed)
- Added `baseline_commit`, `module_disposition`, `pre_satisfied_count` (ISS-001 #3 supplement + ISS-019 complement)

---

## Change 2: Section 1.2 — Add spec_patch.py Coexistence Clause

**Location**: End of Section 1.2 (line 58), before the `---` separator
**Action**: INSERT paragraph
**Provenance**: ISS-011

### Before (lines 53–59):

```markdown
**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step.

---
```

### After:

```markdown
**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step.

**Preserved and coexisting**: `spec_patch.py` (the accepted-deviation workflow)
operates in both legacy and convergence modes. In legacy mode, it patches
spec text before fidelity comparison. In convergence mode, its `spec_hash`
interaction with FR-6 (registry reset on spec change) is preserved. v3.05
does not modify spec_patch.py; it coexists with the new fidelity subsystem.

---
```

---

## Change 3: New Section 1.3 — v3.0 Baseline

**Location**: After the `---` separator following Section 1.2 (line 59), before Section 2
**Action**: INSERT new section
**Provenance**: ISS-019 (global baseline inventory)

### Insert:

```markdown

### 1.3 v3.0 Baseline

This spec was originally drafted before v3.0 shipped. During v3.0 implementation,
~60% of the v3.05 infrastructure was pre-built. The spec MUST be read as
"extend existing code," not "build from scratch." The following inventory is
verified against commit `f4d9035`.

#### Pre-Existing Modules (MODIFY, not CREATE)

| Module | Lines | Key Capabilities | v3.05 FRs That Extend |
|--------|-------|------------------|-----------------------|
| `convergence.py` | 323 | DeviationRegistry lifecycle, compute_stable_id(), ConvergenceResult, _check_regression() (structural-only), temp dir isolation + atexit, get_prior_findings_summary() | FR-6, FR-7, FR-8, FR-10 |
| `semantic_layer.py` | 337 | Prompt budget constants + enforcement (FR-4.2), build_semantic_prompt(), debate scoring (RubricScores, score_argument, judge_verdict), wire_debate_verdict(), prosecutor/defender templates | FR-4, FR-4.1, FR-4.2, FR-5 |
| `remediate_executor.py` | 563 | Snapshot create/restore/cleanup, enforce_allowlist(), parallel ClaudeProcess agents, _check_diff_size() at 50% per-file, all-or-nothing rollback | FR-9 |

#### Pre-Existing Config & Pipeline Wiring (no work needed)

| Component | Location | Spec Requirement |
|-----------|----------|------------------|
| `ACTIVE` in `VALID_FINDING_STATUSES` | models.py:16 | FR-6/BF-1 |
| `Finding.source_layer` field | models.py:44 | FR-6/BF-3 |
| `RoadmapConfig.convergence_enabled` | models.py:107 | FR-7 |
| `RoadmapConfig.allow_regeneration` | models.py:108 | FR-9.1 |
| `--allow-regeneration` CLI flag | commands.py:89-94 | FR-9.1 |
| `WIRING_GATE` registered in `ALL_GATES` | gates.py:944 | NFR-7 |
| `SPEC_FIDELITY_GATE` conditional bypass | executor.py:521 | FR-7 |
| `first_seen_run` / `last_seen_run` tracking | convergence.py:104-130 | FR-10 |
| Prior findings in semantic prompt | semantic_layer.py:140,215-221 | FR-10 |

#### Preserved Legacy Modules

| Module | Role | v3.05 Impact |
|--------|------|-------------|
| `spec_patch.py` | Accepted-deviation workflow (legacy + convergence modes) | Coexists; not modified |

#### Genuinely New Modules (CREATE)

| Module | Spec Ref | Description |
|--------|----------|-------------|
| `spec_parser.py` | FR-2 | Spec & roadmap structural data extraction |
| `structural_checkers.py` | FR-1 | 5 deterministic dimension checkers |

#### Dead Code (DELETE)

| Module | Evidence |
|--------|----------|
| `fidelity.py` (66 lines) | Zero imports across codebase; superseded by Finding + DeviationRegistry |

**Reading convention**: In all subsequent FR sections, acceptance criteria marked
`[x]` with a source reference are v3.0 baseline items (verify, do not rebuild).
Unchecked `[ ]` items require implementation.
```

---

## Change 4: FR-2 — Parser Robustness ACs + Critical Path Note

**Location**: FR-2 Acceptance Criteria (lines 121–131) and after Dependencies (line 133)
**Action**: INSERT 5 ACs + Critical Path Note + Dependencies annotation
**Provenance**: ISS-015

### Before (lines 121–133):

```markdown
**Acceptance Criteria**:
- [ ] Parses YAML frontmatter from both spec and roadmap
- [ ] Extracts markdown tables by section (keyed by heading path)
- [ ] Extracts fenced code blocks with language annotation
- [ ] Extracts requirement ID families via regex: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- [ ] Extracts Python function signatures from fenced blocks: `def name(params) -> return_type`
- [ ] Extracts file paths from manifest tables (Sec 4.1, 4.2, 4.3)
- [ ] Extracts `Literal[...]` enum values from code blocks
- [ ] Extracts numeric threshold expressions: `< 5s`, `>= 90%`, `minimum 20`
- [ ] Returns structured objects, not raw text

**Dependencies**: None
```

### After:

```markdown
**Acceptance Criteria**:
- [ ] Parses YAML frontmatter from both spec and roadmap
- [ ] Extracts markdown tables by section (keyed by heading path)
- [ ] Extracts fenced code blocks with language annotation
- [ ] Extracts requirement ID families via regex: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- [ ] Extracts Python function signatures from fenced blocks: `def name(params) -> return_type`
- [ ] Extracts file paths from manifest tables (Sec 4.1, 4.2, 4.3)
- [ ] Extracts `Literal[...]` enum values from code blocks
- [ ] Extracts numeric threshold expressions: `< 5s`, `>= 90%`, `minimum 20`
- [ ] Returns structured objects, not raw text
- [ ] Graceful degradation on malformed YAML frontmatter: returns partial parse + `ParseWarning`
- [ ] Graceful degradation on irregular markdown tables (missing columns, extra pipes): best-effort extraction + `ParseWarning`
- [ ] Graceful degradation on missing/wrong language tags in fenced blocks: extracts content as raw text + `ParseWarning`
- [ ] `ParseWarning` list collected per parse call, surfaced to caller (not silently swallowed)
- [ ] Validated against real spec (`deterministic-fidelity-gate-requirements.md`) — not just synthetic test fixtures

**Critical Path Note**: FR-2 is the entry point for the structural checker pipeline:
FR-2 (parser) → FR-1 (checkers) → FR-4 (semantic layer) → FR-7 (convergence gate).
A parser failure cascades to all downstream FRs. Robustness against real-world spec
variations is not optional.

**Dependencies**: None. FR-1, FR-4, FR-5, FR-7 all depend on FR-2.
```

---

## Change 5: FR-3 — Canonical Machine Keys + Implementation Contract

**Location**: FR-3 Rule Examples table (lines 142–161) and Acceptance Criteria (lines 163–167)
**Action**: REPLACE rule table, INSERT implementation contract, INSERT 4 missing mismatch types, ADD baseline statement
**Provenance**: ISS-009

### Before (lines 142–167):

```markdown
**Rule Examples**:

| Dimension | Mismatch Type | Severity |
|-----------|--------------|----------|
| Signatures | Roadmap references ID not in spec | HIGH |
| Signatures | Function missing from roadmap | HIGH |
| Signatures | Parameter arity mismatch | MEDIUM |
| Data Models | Required spec file missing from roadmap | HIGH |
| Data Models | File path prefix mismatch | HIGH |
| Data Models | Enum literal not covered | MEDIUM |
| Gates | Required frontmatter field not covered | HIGH |
| Gates | Step parameter missing | MEDIUM |
| Gates | Ordering constraint violated | MEDIUM |
| CLI | Config mode not covered | MEDIUM |
| CLI | Default value mismatch | MEDIUM |
| NFRs | Numeric threshold contradicted | HIGH |
| NFRs | Security primitive missing | HIGH |
| NFRs | Dependency direction violated | HIGH |
| NFRs | Coverage threshold mismatch | MEDIUM |

**Acceptance Criteria**:
- [ ] Every structural checker has an explicit rule table
- [ ] Rules are defined in code (not prompt text), keyed by `(dimension, mismatch_type) → severity`
- [ ] Same inputs always produce the same severity — no randomness, no LLM interpretation
- [ ] Rule table is extensible (new rules can be added without changing checker logic)
```

### After:

```markdown
**Severity Rule Table** (canonical machine keys):

| Dimension | Machine Key | Human Description | Severity |
|-----------|------------|-------------------|----------|
| Signatures | `phantom_id` | Roadmap references ID not in spec | HIGH |
| Signatures | `function_missing` | Function in spec missing from roadmap | HIGH |
| Signatures | `param_arity_mismatch` | Parameter count differs between spec and roadmap | MEDIUM |
| Signatures | `param_type_mismatch` | Parameter type differs between spec and roadmap | MEDIUM |
| Data Models | `file_missing` | Required spec file missing from roadmap | HIGH |
| Data Models | `path_prefix_mismatch` | File path prefix differs (e.g., `audit/` vs `cli/audit/`) | HIGH |
| Data Models | `enum_uncovered` | Enum literal from spec not covered in roadmap | MEDIUM |
| Data Models | `field_missing` | Dataclass/model field from spec not referenced in roadmap | MEDIUM |
| Gates | `frontmatter_field_missing` | Required frontmatter field not covered | HIGH |
| Gates | `step_param_missing` | Step parameter from spec missing in roadmap | MEDIUM |
| Gates | `ordering_violated` | Step ordering constraint violated | MEDIUM |
| Gates | `semantic_check_missing` | Named semantic check not mapped to task | MEDIUM |
| CLI | `mode_uncovered` | Config mode from spec not covered | MEDIUM |
| CLI | `default_mismatch` | Default value differs between spec and roadmap | MEDIUM |
| NFRs | `threshold_contradicted` | Numeric threshold contradicted | HIGH |
| NFRs | `security_missing` | Security primitive missing | HIGH |
| NFRs | `dep_direction_violated` | Dependency direction violated | HIGH |
| NFRs | `coverage_mismatch` | Coverage threshold mismatch | MEDIUM |
| NFRs | `dep_rule_missing` | Dependency rule from spec not addressed | MEDIUM |

**Implementation Contract**:

```python
# Canonical severity rules: dict keyed by (dimension, machine_key) → severity
SEVERITY_RULES: dict[tuple[str, str], str] = {
    ("signatures", "phantom_id"): "HIGH",
    ("signatures", "function_missing"): "HIGH",
    # ... all rows from table above
}

def get_severity(dimension: str, mismatch_type: str) -> str:
    """Look up severity for a given dimension + mismatch type.

    Returns severity string. Raises KeyError for unknown combinations
    (forces explicit rule addition, not silent defaults).
    """
```

**Baseline**: No severity rule infrastructure exists in v3.0. This is genuinely new
code (CREATE). The `compute_stable_id()` function in `convergence.py` uses
`mismatch_type` as a hash input but does not define the rule table.

**Acceptance Criteria**:
- [ ] Every structural checker has an explicit rule table
- [ ] Rules are defined in code (not prompt text), keyed by `(dimension, mismatch_type) → severity`
- [ ] Machine keys (`phantom_id`, `function_missing`, etc.) are used in code — not prose descriptions
- [ ] Same inputs always produce the same severity — no randomness, no LLM interpretation
- [ ] Rule table is extensible (new rules can be added without changing checker logic)
- [ ] Unknown `(dimension, mismatch_type)` combinations raise `KeyError` — no silent defaults
- [ ] `SEVERITY_RULES` dict and `get_severity()` function are the canonical API
- [ ] Finding objects use machine keys in `mismatch_type` field (see FR-6 ISS-024 for field extension)

**Dependencies**: FR-1. ISS-024 (Finding dataclass `rule_id` field extension).
```

---

## Change 6: FR-4 — Existing Baseline Acknowledgment

**Location**: FR-4 Description (lines 172–178), FR-4.1 ACs (lines 234–239), FR-4.2 ACs (lines 266–272)
**Action**: INSERT paragraph in FR-4, MODIFY ACs in FR-4.1, INSERT AC in FR-4.2
**Provenance**: ISS-002 (baseline + AC marks), ISS-014 (function signature + ACs), ISS-017 (truncation AC)

### Change 6a: FR-4 Description — Add Baseline Paragraph (ISS-002)

#### Before (lines 177–180):

```markdown
triggers a lightweight adversarial debate to validate the rating.

**Semantic/structural boundary**: Structural checkers declare their
```

#### After:

```markdown
triggers a lightweight adversarial debate to validate the rating.

**Existing baseline**: `semantic_layer.py` (337 lines) already implements prompt
budget constants and enforcement (FR-4.2), `build_semantic_prompt()` with
proportional budget allocation, debate scoring infrastructure (`RubricScores`,
`score_argument()`, `judge_verdict()`), and `wire_debate_verdict()`. v3.05 adds
`validate_semantic_high()` (orchestrator for FR-4.1 debate protocol) and
`run_semantic_layer()` (entry point for the residual semantic pass).

**Semantic/structural boundary**: Structural checkers declare their
```

### Change 6b: FR-4.1 — Insert Function Signature + Replace ACs (ISS-002 + ISS-014)

#### Before (lines 216–239):

```markdown
7. Write debate output YAML to `output_dir/debates/{finding.stable_id}/debate.yaml`

**Scoring Rubric** (4 criteria, each 0–3 points):
...
**Acceptance Criteria** (FR-4.1):
- [ ] Prosecutor and defender execute in parallel (2 LLM calls, not sequential)
- [ ] Judge is deterministic Python — same scores always produce the same verdict
- [ ] Conservative tiebreak: margin within ±0.15 always produces CONFIRM_HIGH
- [ ] Debate output YAML written per finding with rubric scores, margin, and verdict
- [ ] Registry updated with `debate_verdict` and `debate_transcript` reference after each debate
```

#### After:

```markdown
7. Write debate output YAML to `output_dir/debates/{finding.stable_id}/debate.yaml`

**Orchestrator Function**:

```python
def validate_semantic_high(
    finding: Finding,
    registry: DeviationRegistry,
    output_dir: Path,
    *,
    claude_process_factory: Callable | None = None,
) -> str:
    """Orchestrate lightweight adversarial debate for a semantic HIGH finding.

    Implements FR-4.1 protocol steps 1-7:
    1. Build prosecutor + defender prompts from finding context
    2. Execute both via ClaudeProcess in parallel (2 LLM calls)
    3. Parse YAML responses; default scores to 0 on parse failure
    4. Score both via score_argument() against 4-criterion rubric
    5. Compute verdict via judge_verdict()
    6. Write debate YAML to output_dir/debates/{stable_id}/debate.yaml
    7. Call wire_debate_verdict() to update registry

    Args:
        finding: The semantic HIGH finding to validate.
        registry: Active deviation registry for verdict recording.
        output_dir: Directory for debate output artifacts.
        claude_process_factory: Optional factory for ClaudeProcess creation
            (default: None uses standard ClaudeProcess). Enables testing
            without live LLM calls.

    Returns:
        Verdict string: "CONFIRM_HIGH", "DOWNGRADE_TO_MEDIUM", or
        "DOWNGRADE_TO_LOW".
    """
```

**Scoring Rubric** (4 criteria, each 0–3 points):
...
**Acceptance Criteria** (FR-4.1):
- [x] Debate scoring infrastructure exists: `score_argument()`, `judge_verdict()`, `wire_debate_verdict()` (v3.0 baseline)
- [x] Prosecutor/defender prompt templates exist (v3.0 baseline)
- [x] `RubricScores` dataclass exists (v3.0 baseline)
- [ ] `validate_semantic_high()` exists in semantic_layer.py and implements protocol steps 1-7
- [ ] `validate_semantic_high()` accepts a `claude_process_factory` parameter for test injection
- [ ] Prosecutor and defender execute in parallel (2 LLM calls, not sequential)
- [ ] Judge is deterministic Python — same scores always produce the same verdict
- [ ] Conservative tiebreak: margin within ±0.15 always produces CONFIRM_HIGH
- [ ] Debate output YAML written per finding with rubric scores, margin, and verdict
- [ ] Registry updated with `debate_verdict` and `debate_transcript` reference after each debate
```

### Change 6c: FR-4.2 ACs — Mark Baseline + Add Truncation Heading AC (ISS-002 + ISS-017)

#### Before (lines 266–272):

```markdown
**Acceptance Criteria** (FR-4.2):
- [ ] `MAX_PROMPT_BYTES = 30_720` as configurable module constant
- [ ] Budget ratios are module-level constants, overridable via config
- [ ] Oversized sections are tail-truncated on line boundaries with visible markers
- [ ] `assert` before LLM call confirms prompt ≤ budget
- [ ] Template exceeding 5% allocation raises `ValueError`
- [ ] Empty sections produce a valid prompt without errors
```

#### After:

```markdown
**Acceptance Criteria** (FR-4.2):
- [x] `MAX_PROMPT_BYTES = 30_720` as configurable module constant (v3.0: semantic_layer.py constants)
- [x] Budget ratios are module-level constants, overridable via config (v3.0: semantic_layer.py constants)
- [x] Oversized sections are tail-truncated on line boundaries with visible markers (v3.0: `_truncate_to_budget()`)
- [ ] Truncation markers include section heading: `[TRUNCATED: N bytes omitted from '<heading>']`
- [x] `assert` before LLM call confirms prompt ≤ budget (v3.0: `build_semantic_prompt()`)
- [ ] Template exceeding 5% allocation raises `ValueError`
- [x] Empty sections produce a valid prompt without errors (v3.0: `build_semantic_prompt()`)
```

---

## Change 7: FR-5 — Expanded Splitter Specification

**Location**: FR-5 Description (lines 278–292)
**Action**: REPLACE description and ACs with expanded specification
**Provenance**: ISS-018

### Before (lines 278–292):

```markdown
### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only.

**Acceptance Criteria**:
- [ ] Spec is split by `## N. Section Name` headings into named chunks
- [ ] Roadmap is split by phase/task headings into named chunks
- [ ] Each checker receives only the sections relevant to its dimension
- [ ] No single prompt contains both full documents inline
- [ ] Prompt size per checker call is bounded (configurable, default ~30KB)
- [ ] Section mapping is deterministic: dimension → spec sections → roadmap sections

**Dependencies**: FR-2 (parser)
```

### After:

```markdown
### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only. The splitter produces typed
`SpecSection` objects that carry heading metadata through the pipeline.

**Section Splitter Specification**:

```python
@dataclass
class SpecSection:
    heading: str           # e.g., "3. Functional Requirements"
    heading_path: str      # e.g., "3.Functional Requirements/FR-1"
    level: int             # heading level (1-6)
    content: str           # section body text (excluding heading line)
    start_line: int        # line number of heading in source
    end_line: int          # line number of last content line
```

**Splitting Rules**:
1. Split on `^#{1,6} ` heading lines
2. Each section includes content up to (but not including) the next same-or-higher-level heading
3. Nested sections are children of their parent heading
4. YAML frontmatter is a special section with `heading="frontmatter"`, `level=0`
5. Content before the first heading is a special section with `heading="preamble"`, `level=0`

**Dimension-to-Section Mapping**:

| Dimension | Spec Sections | Roadmap Sections |
|-----------|--------------|-----------------|
| Signatures | FR sections (fenced code blocks) | Task descriptions |
| Data Models | Sec 4.1, 4.2, 4.3 (file manifest tables) | File-related tasks |
| Gates | FR-7, FR-8 (gate criteria) | Gate implementation tasks |
| CLI | Sec 5.1 (CLI table) | Config/option tasks |
| NFRs | Sec 6 (thresholds, security, dependencies) | Corresponding validation tasks |

**Acceptance Criteria**:
- [ ] `SpecSection` dataclass defined with fields: heading, heading_path, level, content, start_line, end_line
- [ ] `split_into_sections(content: str) -> list[SpecSection]` function in spec_parser.py
- [ ] Spec is split by `## N. Section Name` headings into named `SpecSection` chunks
- [ ] Roadmap is split by phase/task headings into named `SpecSection` chunks
- [ ] YAML frontmatter extracted as special section (level=0, heading="frontmatter")
- [ ] Content before first heading extracted as preamble section (level=0)
- [ ] Each checker receives only the sections relevant to its dimension (per mapping table)
- [ ] Supplementary sections (cross-referenced from primary) included when reference graph detects them
- [ ] No single prompt contains both full documents inline
- [ ] Prompt size per checker call is bounded (configurable, default ~30KB)
- [ ] Section mapping is deterministic: dimension → spec sections → roadmap sections
- [ ] `SpecSection.heading` propagated to truncation markers when sections are truncated (see FR-4.2)

**Dependencies**: FR-2 (parser). ISS-015 critical path: FR-2 must be robust before FR-5 consumes its output.
```

---

## Change 8: FR-6 — Finding Dataclass Extension + RunMetadata AC

**Location**: After Source Layer Tracking paragraph (line 312), and after FR-6 ACs (line 329)
**Action**: INSERT subsection (ISS-024), INSERT AC (ISS-021), UPDATE description (ISS-008)
**Provenance**: ISS-024 (Finding fields), ISS-021 (RunMetadata), ISS-008 (DeviationRegistry location)

### Change 8a: FR-6 Description — DeviationRegistry Location (ISS-008)

The FR-6 description references the registry conceptually. Add a note clarifying the class location:

#### Insert after line 298 ("registry of all findings"):

```markdown
**Implementation note**: The `DeviationRegistry` class exists in `convergence.py`
(lines 50-225), not in a separate `deviation_registry.py` file. This co-location
is correct: the registry is tightly coupled with `compute_stable_id()`,
`_check_regression()`, and the convergence loop orchestrator. The
`deviation_registry.py` entry has been removed from the `relates_to` frontmatter.
```

### Change 8b: Finding Dataclass Extension (ISS-024)

#### Insert after Source Layer Tracking paragraph (line 312):

```markdown
**Finding Dataclass Extension**: v3.05 requires additional fields on the
`Finding` dataclass (in `models.py`):

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `rule_id` | `str` | `""` | Machine key from FR-3 severity rules (e.g., `phantom_id`) |
| `spec_quote` | `str` | `""` | Exact text from spec that the finding references |
| `roadmap_quote` | `str` | `""` | Exact text from roadmap (or `"MISSING"` for omission findings) |

All new fields have defaults for backward compatibility with pre-v3.05 registries.
`stable_id` remains a computed property (via `compute_stable_id()` in
`convergence.py`), not a stored field.
```

### Change 8c: RunMetadata AC (ISS-021)

#### Insert after FR-6 AC list (after line 329):

```markdown
- [ ] Run metadata uses a typed dataclass (`RunMetadata`) — not raw dicts — to ensure field presence and type safety at construction time
```

---

## Change 9: FR-7 — Baseline + Pipeline Integration + Step Ordering + Interface Contract + Legacy Expansion

**Location**: FR-7 section (lines 335–367)
**Action**: Multiple insertions and modifications
**Provenance**: ISS-001 (baseline + description edit), ISS-012 (Pipeline Integration), ISS-013 (Step Ordering), ISS-016 (FR-7.1 Interface Contract), ISS-023 (legacy mode expansion), ISS-010 (convergence wraps remediation)

### Change 9a: FR-7 Description Edit (ISS-001)

#### Before (lines 335–337):

```markdown
### FR-7: Convergence Gate

**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
```

#### After:

```markdown
### FR-7: Convergence Gate

**Description**: Extends the existing `convergence.py` (323 lines, v3.0) with
`execute_fidelity_with_convergence()` and `handle_regression()`. The fidelity
gate evaluates convergence based on registry state with these criteria:
```

### Change 9b: FR-7 Baseline Subsection (ISS-001)

#### Insert before the Gate Authority Model paragraph (before line 344):

```markdown
**FR-7 Baseline** (v3.0, commit `f4d9035`):

| Component | Location | Status |
|-----------|----------|--------|
| `DeviationRegistry` class | convergence.py:50-225 | Exists — 176 lines, 11 methods |
| `compute_stable_id()` | convergence.py:24-32 | Exists — hash-based ID generation |
| `ConvergenceResult` dataclass | convergence.py:228-237 | Exists — result container |
| `_check_regression()` (structural-only) | convergence.py:240-272 | Exists — structural HIGH comparison |
| Temp dir isolation + atexit cleanup | convergence.py:278-323 | Exists — used by FR-8 |
| `get_prior_findings_summary()` | convergence.py:179-188 | Exists — for FR-10 |
| `RoadmapConfig.convergence_enabled` | models.py:107 | Exists — config field |

v3.05 adds: `execute_fidelity_with_convergence()` (orchestrator), `handle_regression()` (FR-8 interface).

```

### Change 9c: Gate Authority Model — Legacy Mode Expansion (ISS-023)

#### Before (lines 350–352):

```markdown
In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
exactly as in pre-v3.05, validating the LLM-generated report frontmatter.
The two authorities never coexist in the same execution mode.
```

#### After:

```markdown
In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
exactly as in pre-v3.05, validating the LLM-generated report frontmatter
(generated by `prompts.py:build_spec_fidelity_prompt()`). In convergence mode,
`build_spec_fidelity_prompt()` is still called to generate the human-readable
`spec-fidelity.md` summary report, but its output is NOT gated — only the
`DeviationRegistry` is authoritative.
The two authorities never coexist in the same execution mode.
```

### Change 9d: Pipeline Integration Subsection (ISS-012)

#### Insert after Gate Authority Model paragraph:

```markdown
**Pipeline Integration**: The convergence engine operates *within* step 8
(fidelity gate) of the existing pipeline, not as a new pipeline phase. When
`convergence_enabled=true`, step 8 executes up to 3 fidelity runs internally:

1. **Run 1** (catch): Full structural + semantic checker suite
2. **Run 2** (verify): Re-run after remediation; monotonic progress check
3. **Run 3** (backup): Final attempt if Run 2 did not converge

The pipeline's step 9 (certification) and all upstream steps (1-7) are
unaffected. Step 8 either produces a PASS (0 active HIGHs) or HALT (budget
exhausted) — the pipeline never sees intermediate convergence state.

The existing wiring-verification bypass pattern (step 8 skips `_embed_inputs()`
when `wiring_only=True`) is preserved and unaffected by convergence mode.
```

### Change 9e: Step Ordering Table (ISS-013)

#### Insert after Pipeline Integration subsection:

```markdown
**Step Ordering Semantics** (convergence mode):

| Step | Behavior When `convergence_enabled=true` | Notes |
|------|------------------------------------------|-------|
| Steps 1-7 | Unchanged | Upstream pipeline unaffected |
| Step 8 | Convergence engine is sole authority | Up to 3 internal runs |
| Step 9 | `spec_fidelity_file` input is decorative | Report written but not gated |
| Wiring-verification | Bypasses `_embed_inputs()` | Pattern preserved |

These semantics are undocumented in v3.0 code but implemented correctly.
v3.05 makes them normative.
```

### Change 9f: Convergence Wraps Remediation (ISS-010)

#### Insert after Step Ordering:

```markdown
**Intra-Loop Remediation**: Within the convergence loop,
`execute_fidelity_with_convergence()` calls `execute_remediation()` between
runs. `remediate_executor.py` remains a pure execution engine — it is not
modified for convergence awareness. The convergence loop owns the budget
(3 runs) and translates remediation results into `DeviationRegistry` updates.

**Budget isolation**: Two different budget systems coexist:
- Convergence mode: 3 fidelity runs (FR-7 budget). `_check_remediation_budget()`
  and `_print_terminal_halt()` are NOT invoked.
- Legacy mode: 2 remediation attempts (existing behavior). Completely untouched
  by convergence mode.

The two budget systems MUST never overlap. `convergence_enabled=true` disables
the legacy remediation budget check.
```

### Change 9g: FR-7 Acceptance Criteria — Add New ACs (ISS-012 + ISS-013 + ISS-010)

#### Insert after existing FR-7 ACs (after line 365):

```markdown
- [ ] Convergence loop executes within step 8 boundary, not as new pipeline phase
- [ ] Steps 1-7 and step 9 are unaffected by `convergence_enabled=true`
- [ ] Wiring-verification bypass preserved in convergence mode
- [ ] Step 9 `spec_fidelity_file` is written but not gated in convergence mode
- [ ] Step ordering documented as normative (table above)
- [ ] `spec_fidelity_file` input to step 9 is decorative in convergence mode; convergence status comes from registry
- [ ] Step 9 can read convergence result without re-evaluating findings
- [ ] `execute_fidelity_with_convergence()` calls `execute_remediation()` between convergence runs
- [ ] `_check_remediation_budget()` and `_print_terminal_halt()` are NOT invoked when `convergence_enabled=true`
- [ ] Legacy remediation budget (2 attempts) is completely untouched by convergence mode
- [ ] Convergence budget (3 runs) and legacy budget (2 attempts) never overlap
```

### Change 9h: FR-7.1 Interface Contract (ISS-016)

#### Insert after FR-7 Acceptance Criteria:

```markdown
#### FR-7.1: FR-7/FR-8 Interface Contract

**Description**: Specifies the calling convention between the convergence gate
(FR-7) and regression detection (FR-8). The circular dependency (FR-7 triggers
FR-8; FR-8 feeds back into FR-7) requires explicit interface design.

**Calling Convention**:

```python
def handle_regression(
    current_run: RunMetadata,
    previous_run: RunMetadata,
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    output_dir: Path,
) -> RegressionResult:
    """Orchestrate parallel validation for structural regression.

    Spawns 3 agents in isolated temp dirs, merges findings,
    runs adversarial debate on each HIGH, updates registry.
    """
```

**Return Contract**:

```python
@dataclass
class RegressionResult:
    validated_findings: list[Finding]
    debate_verdicts: dict[str, str]  # stable_id → verdict
    agents_succeeded: int            # out of 3
    consolidated_report_path: Path
```

**Lifecycle Within Convergence Loop**:
1. Run N completes → convergence engine checks `structural_high_count`
2. If regression detected → `handle_regression()` called
3. `handle_regression()` spawns 3 parallel agents (FR-8)
4. Results merged → adversarial debate validates each HIGH
5. Registry updated with validated findings and debate verdicts
6. **This entire flow counts as one "run" toward the budget of 3**
7. Convergence engine proceeds to next run or halts

**Budget Accounting Rule**: A regression validation + its subsequent remediation
= 1 budget unit. Example: Run 1 → regression → Run 2 (with FR-8 validation) →
remediation → Run 3. The budget allows this sequence.

**Ownership Boundaries**:
- FR-7 owns: convergence budget, run sequencing, progress evaluation
- FR-8 owns: parallel agent spawning, result merging, adversarial debate
- FR-6 is shared: both FR-7 and FR-8 read/write the DeviationRegistry

**Acceptance Criteria** (FR-7.1):
- [ ] `handle_regression()` callable from convergence loop with documented signature
- [ ] `RegressionResult` dataclass returned with validated findings and debate verdicts
- [ ] Regression validation + remediation counts as one budget unit
- [ ] FR-7 does not spawn agents directly (delegated to FR-8 via `handle_regression()`)
- [ ] FR-8 does not evaluate convergence (delegated back to FR-7 via return value)
- [ ] Both FR-7 and FR-8 access `DeviationRegistry` — no ownership conflict on concurrent access (serialized within convergence loop)

**Dependencies**: FR-7 (convergence gate), FR-8 (regression detection), FR-6 (registry)
```

### Change 9i: FR-7 Dependencies Update

#### Before:

```markdown
**Dependencies**: FR-6 (registry), FR-8 (regression handling)
```

#### After:

```markdown
**Dependencies**: FR-6 (registry), FR-7.1 (FR-8 interface contract), FR-8 (regression handling)
```

---

## Change 10: FR-8 — Existing Code Acknowledgment

**Location**: FR-8 Description (lines 373-378), Isolation mechanism (lines 380-384), Cleanup protocol (lines 386-390)
**Action**: REPLACE 3 paragraphs with versions acknowledging existing code
**Provenance**: ISS-022

### Change 10a: FR-8 Description

#### Before (lines 373–378):

```markdown
**Description**: When run N+1 has MORE **structural** HIGHs than run N
(regression detected), the system spawns 3 parallel validation agents in
isolated temporary directories. Each independently re-runs the fidelity check.
Their findings are collected, merged by stable ID, deduplicated, sorted by
severity, and written to a consolidated report. After consolidation, an
adversarial debate validates the severity of each HIGH.
```

#### After:

```markdown
**Description**: When run N+1 has MORE **structural** HIGHs than run N
(regression detected), the system extends the existing temp dir isolation
mechanism in `convergence.py` (lines 278-323) to spawn 3 parallel validation
agents in isolated temporary directories. Each independently re-runs the
fidelity check. Their findings are collected, merged by stable ID,
deduplicated, sorted by severity, and written to a consolidated report. After
consolidation, an adversarial debate validates the severity of each HIGH.
```

### Change 10b: FR-8 Isolation Mechanism

#### Before (lines 380–384):

```markdown
**Isolation mechanism**: Each agent operates in its own temporary directory
containing independent copies of all input files (spec, roadmap, registry
snapshot). This replaces git worktrees because the files that need isolation
(roadmap, registry) are output artifacts not tracked by git. Temp directories
provide true input isolation at ~1.5MB vs ~150MB per worktree.
```

#### After:

```markdown
**Isolation mechanism**: Each agent operates in its own temporary directory
containing independent copies of all input files (spec, roadmap, registry
snapshot), reusing and extending the temp dir + atexit cleanup pattern already
implemented in `convergence.py`. This replaces git worktrees because the files
that need isolation (roadmap, registry) are output artifacts not tracked by
git. Temp directories provide true input isolation at ~1.5MB vs ~150MB per
worktree.
```

### Change 10c: FR-8 Cleanup Protocol

#### Before (line 386):

```markdown
**Cleanup protocol**:
```

#### After:

```markdown
**Cleanup protocol** (extends existing `atexit` cleanup in `convergence.py:310-323`):
```

---

## Change 11: FR-9 — Unified Rewrite (ISS-003 + ISS-007 combined)

**Location**: FR-9 Description (lines 411–417), Patch Format (lines 419–433), ACs (lines 435–445)
**Action**: REPLACE description, REPLACE patch format section, MODIFY ACs
**Provenance**: ISS-003 (baseline/delta framing), ISS-007 (ClaudeProcess-primary), ISS-005 (per-patch ACs), ISS-006 (per-file rollback ACs)

### Change 11a: FR-9 Description (ISS-003 + ISS-007 merged)

#### Before (lines 411–417):

```markdown
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

#### After:

```markdown
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Extends the existing `remediate_executor.py` (563 lines, v3.0)
to produce structured patches in a MorphLLM-compatible JSON format, applied via
ClaudeProcess (the established pipeline execution engine). The patch format is
engine-agnostic: a future migration to MorphLLM requires only swapping the
applicator, not the patch generation or validation logic.

**v3.0 Baseline** (commit `f4d9035`):

| Component | Location | Status |
|-----------|----------|--------|
| `create_snapshots()` / `restore_from_snapshots()` / `cleanup_snapshots()` | lines 53-101 | Exists — per-file snapshot primitives |
| `enforce_allowlist()` | lines 110-137 | Exists — file path validation |
| `_run_agent_for_file()` | lines 161-211 | Exists — ClaudeProcess agent dispatch |
| `_check_diff_size()` | lines 416-473 | Exists — whole-file diff check at 50% |
| `_handle_failure()` | lines 475-502 | Exists — all-or-nothing rollback |
| `_DIFF_SIZE_THRESHOLD_PCT = 50` | line 45 | Exists — MUST change to 30 (ISS-004/BF-5) |

**Delta** (v3.05 changes to existing code):

| # | Change | Provenance |
|---|--------|-----------|
| 1 | `MODIFY _DIFF_SIZE_THRESHOLD_PCT: 50 → 30` | ISS-004, BF-5 |
| 2 | `MODIFY _check_diff_size()`: per-file → per-patch granularity | ISS-005 |
| 3 | `MODIFY _handle_failure()`: all-or-nothing → per-file rollback with coherence check | ISS-006 |
| 4 | `NEW RemediationPatch` dataclass: typed JSON patch schema | FR-9 |
| 5 | `NEW apply_patches()`: sequential patch application per file | FR-9 |
| 6 | `NEW fallback_apply()`: deterministic text replacement fallback | FR-9, ISS-007 |
| 7 | `NEW check_morphllm_available()`: MCP runtime probe (future) | ISS-007 |
```

### Change 11b: Patch Format Section (ISS-007)

#### Before (lines 419–433):

```markdown
**Patch Format (MorphLLM Lazy Snippets)**:
Patches use MorphLLM's semantic merging format, NOT unified diffs:
```json
{
  "target_file": "roadmap.md",
  ...
}
```
Context markers (`// ... existing code ...`) indicate unchanged regions.
MorphLLM applies edits via semantic understanding, tolerating minor
line-number or formatting discrepancies.
```

#### After:

```markdown
**Patch Format (Engine-Agnostic Lazy Snippets)**:
Patches use a JSON schema compatible with MorphLLM's semantic merging format.
This format is NOT tied to MorphLLM as execution engine — it is a structured
intermediate representation that any applicator can consume:
```json
{
  "target_file": "roadmap.md",
  "finding_id": "SIG-001",
  "original_code": "<relevant section from current file>",
  "instruction": "Replace phantom FR-009 reference with correct G-001 ID",
  "update_snippet": "// ... existing code ...\n<changed lines>\n// ... existing code ...",
  "rationale": "Roadmap references FR-009 which does not exist in spec ID set"
}
```
Context markers (`// ... existing code ...`) indicate unchanged regions.

**Applicator Selection**:
1. **Primary**: `ClaudeProcess` — generates and applies patches via LLM subprocess
   (established pattern; same as executor.py and validate_executor.py)
2. **Fallback**: Deterministic Python text replacement using `original_code` as
   anchor (minimum anchor: 5 lines or 200 chars). Used when ClaudeProcess fails
   or for simple substitutions.
3. **Future**: MorphLLM MCP (`morphllm-fast-apply`) — when integrated, replaces
   ClaudeProcess as applicator. `check_morphllm_available()` probes MCP runtime.
   Patch format requires zero changes for this migration.
```

### Change 11c: FR-9 Acceptance Criteria (ISS-003 + ISS-005 + ISS-006 + ISS-007)

#### Before (lines 435–445):

```markdown
**Acceptance Criteria**:
- [ ] Remediation agents output MorphLLM-compatible lazy edit snippets per finding
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] MorphLLM (when available) applies patches via semantic merging
- [ ] Fallback applicator (when MorphLLM unavailable): deterministic Python text replacement using original_code as anchor (minimum anchor: 5 lines or 200 chars)
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file (not all-or-nothing)
- [ ] Existing snapshot/restore mechanism retained for per-file rollback
```

#### After:

```markdown
**Acceptance Criteria**:
- [x] Snapshot create/restore/cleanup primitives exist (v3.0: lines 53-101)
- [x] File path allowlist enforcement exists (v3.0: `enforce_allowlist()`)
- [x] ClaudeProcess agent dispatch exists (v3.0: `_run_agent_for_file()`)
- [ ] Remediation agents output structured lazy edit snippets per finding (MorphLLM-compatible JSON format)
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] `RemediationPatch` dataclass defined with typed fields matching JSON schema
- [ ] ClaudeProcess applies patches as primary engine; `fallback_apply()` handles failures via deterministic text replacement (minimum anchor: 5 lines or 200 chars)
- [ ] `check_morphllm_available()` probes MCP runtime; when True, MorphLLM replaces ClaudeProcess as applicator
- [ ] Per-patch diff-size guard: each `RemediationPatch` independently evaluated against threshold — reject if `changed_lines / total_file_lines > 30%`
- [ ] `_check_diff_size()` retired; replaced by per-patch evaluation of `RemediationPatch` objects
- [ ] Partial rejection supported: valid patches applied even when others for the same file are rejected
- [ ] Rejected patches logged with reason (patch ID, actual ratio, threshold); finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file: each file evaluated independently after all its patches are applied
- [ ] Post-execution coherence check: if a file's patches succeed but the file shares cross-file findings with a failed file, coherence pass evaluates whether to roll back the successful file
- [ ] Existing snapshot/restore mechanism retained for per-file rollback
- [ ] `_DIFF_SIZE_THRESHOLD_PCT` changed from 50 to 30 (BF-5 adversarial review)
```

---

## Change 12: Resolved Questions Update

**Location**: Resolved Questions table (lines 538–551)
**Action**: UPDATE Q#3
**Provenance**: ISS-007

### Before (Q#3, line 544):

```markdown
| 3 | What is the patch schema for MorphLLM integration? | **Lazy edit snippets with semantic merging.** MorphLLM does NOT use unified diffs or git diff format. It accepts: (1) original code, (2) editing instruction, (3) update snippet with `// ... existing code ...` context markers. Morph uses semantic understanding to merge, tolerating minor line-number or formatting errors. FR-9 patch model should produce MorphLLM-compatible lazy snippets, not unified diff hunks. |
```

### After:

```markdown
| 3 | What is the patch schema for structured remediation? | **Engine-agnostic lazy edit snippets.** Remediation agents produce typed JSON patches with `original_code` anchors and `update_snippet` replacements. Context markers (`// ... existing code ...`) indicate unchanged regions. The format is MorphLLM-compatible but engine-agnostic: ClaudeProcess is the primary applicator, with deterministic Python fallback. MorphLLM integration is a future swap requiring zero patch format changes. |
```

---

## Change 13: Appendix A — Convergence Detail Diagram

**Location**: After Appendix A "Proposed Remediation Flow" (line 611)
**Action**: INSERT convergence detail subsection
**Provenance**: ISS-012

### Insert:

```markdown

### Proposed Convergence Loop Detail
```
Step 8 (Fidelity Gate) with convergence_enabled=true:
┌─────────────────────────────────────────────────┐
│ execute_fidelity_with_convergence()              │
│                                                   │
│  Run 1 (catch):                                   │
│    Structural checkers (parallel) → findings      │
│    Semantic layer (chunked) → findings            │
│    → Deviation Registry update                    │
│    → Check: 0 active HIGHs? → PASS → exit        │
│                                                   │
│  Remediation (structured patches, diff-guarded)   │
│                                                   │
│  Run 2 (verify):                                  │
│    Same checker suite → new findings              │
│    → Monotonic check (structural only)            │
│    → If regression: handle_regression() [FR-8]    │
│      (counts as part of this run's budget)        │
│    → Check: 0 active HIGHs? → PASS → exit        │
│                                                   │
│  Remediation                                      │
│                                                   │
│  Run 3 (backup — final):                          │
│    Same checker suite → final findings            │
│    → Check: 0 active HIGHs? → PASS → exit        │
│    → Else: HALT with diagnostic report            │
│                                                   │
│  Pipeline sees: PASS or HALT (never intermediate) │
└─────────────────────────────────────────────────┘
```
```

---

## Summary

| Metric | Value |
|--------|-------|
| Total changes | 13 change blocks (some with sub-changes a–i) |
| Issues resolved | 23 of 24 |
| ISS-004 | SUPERSEDED by ISS-003 delta item 5 |
| Spec sections modified | ~25 distinct locations |
| New sections added | 6 (Section 1.3, FR-7 Pipeline Integration, FR-7 Step Ordering, FR-7.1, FR-5 splitter spec, FR-6 Finding Extension) |
| New ACs added | ~48 |
| ACs marked `[x]` (baseline) | ~14 |
| Lines added | ~300 |
| Lines modified | ~40 |
| Lines deleted | ~5 (fidelity.py + deviation_registry.py from relates_to) |
| Resolved Question updated | Q#3 (MorphLLM → engine-agnostic) |
| Appendix addition | Convergence loop detail diagram |

### Provenance Summary

| Issue ID | Severity | Changes Contributed |
|----------|----------|-------------------|
| ISS-001 | CRITICAL | Change 1 (module_disposition), Change 9a-9b (FR-7 baseline) |
| ISS-002 | CRITICAL | Change 6a (FR-4 baseline), Change 6b (FR-4.1 AC marks), Change 6c (FR-4.2 AC marks) |
| ISS-003 | CRITICAL | Change 1 (module_disposition), Change 11a (FR-9 description + baseline/delta) |
| ISS-004 | HIGH | SUPERSEDED by ISS-003 delta item 5 (threshold 50→30 in Change 11a + 11c) |
| ISS-005 | HIGH | Change 11c (per-patch ACs replacing per-file) |
| ISS-006 | HIGH | Change 11c (per-file rollback + coherence check ACs) |
| ISS-007 | HIGH | Change 11a (ClaudeProcess-primary description), Change 11b (Applicator Selection), Change 11c (AC refinements), Change 12 (Q#3) |
| ISS-008 | HIGH | Change 1 (remove deviation_registry.py from relates_to), Change 8a (FR-6 location note) |
| ISS-009 | HIGH | Change 5 (FR-3 canonical keys + implementation contract) |
| ISS-010 | HIGH | Change 9f (intra-loop remediation), Change 9g (budget isolation ACs) |
| ISS-011 | MEDIUM | Change 1 (add spec_patch.py to relates_to), Change 2 (Section 1.2 coexistence clause) |
| ISS-012 | MEDIUM | Change 9d (Pipeline Integration), Change 9g (4 ACs), Change 13 (Appendix A diagram) |
| ISS-013 | MEDIUM | Change 9e (Step Ordering table), Change 9g (3 ACs) |
| ISS-014 | MEDIUM | Change 6b (validate_semantic_high() signature + 2 ACs) |
| ISS-015 | MEDIUM | Change 4 (FR-2 robustness ACs + Critical Path Note) |
| ISS-016 | MEDIUM | Change 9h (FR-7.1 Interface Contract + 6 ACs) |
| ISS-017 | MEDIUM | Change 6c (truncation heading AC in FR-4.2) |
| ISS-018 | MEDIUM | Change 7 (FR-5 splitter specification + 12 ACs) |
| ISS-019 | MEDIUM | Change 3 (Section 1.3 v3.0 Baseline) |
| ISS-020 | LOW | Change 1 (delete fidelity.py from relates_to) |
| ISS-021 | LOW | Change 8c (RunMetadata AC in FR-6) |
| ISS-022 | LOW | Change 10a-10c (FR-8 existing code acknowledgment) |
| ISS-023 | LOW | Change 9c (FR-7 legacy mode expansion) |
| ISS-024 | LOW | Change 8b (Finding Dataclass Extension subsection in FR-6) |
