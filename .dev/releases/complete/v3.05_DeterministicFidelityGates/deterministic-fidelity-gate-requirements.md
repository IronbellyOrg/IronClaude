---
title: "Deterministic Spec-Fidelity Gate — Requirements Specification"
version: "1.2.0"
status: draft
created: 2026-03-19
amended: 2026-03-19
source: "/sc:brainstorm systematic deep codebase"
parent_feature: v3.0_unified-audit-gating
amendment_source:
  - "adversarial-design-review (7 blocking findings resolved)"
  - "turnledger-integration/v3.05/design.md"
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
  - src/superclaude/cli/sprint/models.py
  - src/superclaude/cli/pipeline/trailing_gate.py
baseline_commit: f4d9035
module_disposition:
  - file: src/superclaude/cli/roadmap/convergence.py
    action: MODIFY
    lines: 323
    extends_frs: [FR-6, FR-7, FR-8, FR-10]
    imports: [superclaude.cli.sprint.models.TurnLedger]
    import_note: "Conditional import (convergence mode only); long-term migration target: pipeline/models.py"
    new_helpers: [reimburse_for_progress]
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
  - file: src/superclaude/cli/sprint/models.py
    action: CONSUME
    note: "TurnLedger imported into convergence.py; no modifications to sprint/models.py"
    extends_frs: [FR-7]
  - file: src/superclaude/cli/roadmap/fidelity.py
    action: DELETE
    note: "Dead code — zero imports"
  - file: src/superclaude/cli/roadmap/deviation_registry.py
    action: REMOVE_FROM_MANIFEST
    note: "Class exists inside convergence.py:50-225, no separate file"
pre_satisfied_count: 19
---

# Deterministic Spec-Fidelity Gate — Requirements Specification

## 1. Problem Statement

The current roadmap CLI pipeline has a spec-fidelity gate that uses an LLM to
compare a spec against a generated roadmap and report deviations. This gate is
non-deterministic and gets stuck in infinite remediation loops.

After 4 failed runs on the v3.0 release, five failure modes were identified:

1. **Severity drift** — MEDIUM→HIGH across runs with no anchoring
2. **Full document regeneration** — destroying prior fixes
3. **Attention degradation** — on large inline-embedded documents
4. **No convergence mechanism** — no memory of prior findings
5. **Goalpost movement** — severity criteria re-interpreted each run

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| Runs 1→3 showed gradual convergence (3→1 HIGH), then Run 4 regressed catastrophically | `fidelity-remediation-log.md` | All prior fixes lost |
| Severity classifications drift between runs on identical content | Run logs, vote files | Non-deterministic gate behavior |
| Full roadmap regenerated from scratch on Run 4 | `fidelity-remediation-log.md` | Phase structure, numbering, paths all changed |
| Phantom requirement IDs (FR-009..FR-038) fabricated by LLM | `vote-2.md`, `vote-4.md` | False deviations inflate severity counts |
| Gate only checks `high_severity_count == 0` in frontmatter | `gates.py` | No validation of report quality or classification accuracy |

### 1.2 Scope Boundary

**In scope**: Refactoring the fidelity comparison, severity classification,
deviation tracking, remediation editing, and convergence control subsystems.
Budget enforcement for the convergence loop via TurnLedger (imported from
sprint/models.py as a pure-data economic primitive). The convergence engine
receives a pre-allocated TurnLedger instance from the pipeline executor; it
does not construct its own.

**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step. TurnLedger class
modifications (consumed as-is). TurnLedger migration to pipeline/models.py
(future cleanup). Sprint-level budget wiring (execute_sprint,
execute_phase_tasks). Gate-pass reimbursement activation in the sprint loop
(v3.1 scope). Convergence-specific tracking (run counting, monotonic progress)
is handled by the convergence loop and DeviationRegistry, not by a separate
budget dataclass.

**Preserved and coexisting**: `spec_patch.py` (the accepted-deviation workflow)
operates in both legacy and convergence modes. In legacy mode, it patches
spec text before fidelity comparison. In convergence mode, its `spec_hash`
interaction with FR-6 (registry reset on spec change) is preserved. v3.05
does not modify spec_patch.py; it coexists with the new fidelity subsystem.

### 1.3 v3.0 Baseline

This spec was originally drafted before v3.0 shipped. During v3.0 implementation,
~60% of the v3.05 infrastructure was pre-built. The spec MUST be read as
"extend existing code," not "build from scratch." The following inventory is
verified against commit `f4d9035`.

#### Pre-Existing Modules (MODIFY, not CREATE)

| Module | Lines | Key Capabilities | v3.05 FRs That Extend |
|--------|-------|------------------|-----------------------|
| `convergence.py` | 323 | DeviationRegistry lifecycle, compute_stable_id(), ConvergenceResult, _check_regression() (structural-only), temp dir isolation + atexit, get_prior_findings_summary(). v3.05 adds: `from superclaude.cli.sprint.models import TurnLedger` | FR-6, FR-7, FR-8, FR-10 |
| `semantic_layer.py` | 337 | Prompt budget constants + enforcement (FR-4.2), build_semantic_prompt(), debate scoring (RubricScores, score_argument, judge_verdict), wire_debate_verdict(), prosecutor/defender templates | FR-4, FR-4.1, FR-4.2, FR-5 |
| `remediate_executor.py` | 563 | Snapshot create/restore/cleanup, enforce_allowlist(), parallel ClaudeProcess agents, _check_diff_size() at 50% per-file (current behavior, changed to per-patch 30% by FR-9), all-or-nothing rollback | FR-9 |

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
| `TurnLedger` class | sprint/models.py:488-525 | FR-7 |
| `TurnLedger.reimbursement_rate=0.8` | sprint/models.py:499 | FR-7 (first production consumer) |
| `check_budget_guard()` | sprint/executor.py:337-350 | FR-7 (pre-launch guard pattern) |

**TurnLedger methods consumed by convergence engine**: `debit()`, `credit()`,
`can_launch()`, `can_remediate()`, `reimbursement_rate`.

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

---

## 2. Clarified User Goals

G1. **Determinism**: Same spec + same roadmap → same findings and severity
    classifications, every time.

G2. **Convergence**: The pipeline MUST terminate. 3 runs max (catch → verify →
    backup). If it can't converge in 3, halt and report — don't loop.

G3. **Edit preservation**: Remediation never destroys prior fixes. No full
    document regeneration without explicit user consent.

G4. **Anchored severity**: Severity is determined by structural rules where
    possible (~70% of deviations). When LLM assigns HIGH, adversarial debate
    validates it before the pipeline acts on it.

G5. **Scalability**: Large specs and roadmaps handled via chunked/sectional
    comparison, not full-inline embedding.

G6. **Auditability**: Every finding, every severity assignment, every
    remediation edit is traceable to a rule or debate verdict.

---

## 3. Functional Requirements

### FR-1: Decomposed Structural Checkers (5 Dimensions)

**Description**: Replace the monolithic LLM fidelity comparison with 5
independent, statically-typed checkers — one per dimension. Each checker
extracts structured data from spec and roadmap, compares deterministically,
and produces typed findings with predetermined severity rules.

**Checkers**:

| # | Checker | Extracts From Spec | Extracts From Roadmap | Structural % |
|---|---------|--------------------|-----------------------|-------------|
| 1 | **Signatures** | Function sigs from fenced Python, FR/NFR/SC ID sets | Referenced IDs, function names/params in task descriptions | 80% |
| 2 | **Data Models** | File manifest tables (Sec 4.1/4.2), dataclass fields, enum literals | File paths in tasks, field references, mode coverage | 85% |
| 3 | **Gates** | `GateCriteria` fields, `Step(...)` params, semantic check names, step ordering | Gate implementation tasks, parameter coverage | 65% |
| 4 | **CLI Options** | CLI table (Sec 5.1), config fields, `Literal[...]` modes, defaults | Config/option coverage in tasks | 75% |
| 5 | **NFRs** | Numeric thresholds, security primitives, dependency rules (Sec 6) | Corresponding targets/validations in roadmap | 55% |

**Acceptance Criteria**:
- [ ] Each checker is an independent callable that takes (spec_path, roadmap_path) → List[Finding]
- [ ] Each checker produces findings with severity assigned by structural rules, not LLM prose
- [ ] Checkers can run in parallel (no shared state)
- [ ] Each finding includes: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location
- [ ] A checker registry maps dimension names to checker callables

**Dependencies**: FR-2 (spec parser), FR-3 (severity rules)

---

### FR-2: Spec & Roadmap Parser

**Description**: A parser that extracts structured data from the spec template
format (YAML frontmatter, markdown tables, fenced code blocks, heading
hierarchy, requirement ID patterns) and from roadmap markdown.

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

---

### FR-3: Anchored Severity Rules

**Description**: Each structural checker has a severity rule table that maps
specific structural mismatch types to fixed severity levels. Severity is NOT
LLM-judged for structural findings.

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

---

### FR-4: Residual Semantic Layer with Adversarial Validation

**Description**: After structural checkers complete, a residual LLM pass
handles the ~30% of checks that require semantic judgment (prose sufficiency,
spec contradiction resolution, additive-but-benign assessment). When the
semantic layer assigns HIGH severity, it does NOT auto-accept. Instead, it
triggers a lightweight adversarial debate to validate the rating.

**Existing baseline**: `semantic_layer.py` (337 lines) already implements prompt
budget constants and enforcement (FR-4.2), `build_semantic_prompt()` with
proportional budget allocation, debate scoring infrastructure (`RubricScores`,
`score_argument()`, `judge_verdict()`), and `wire_debate_verdict()`. v3.05 adds
`validate_semantic_high()` (orchestrator for FR-4.1 debate protocol) and
`run_semantic_layer()` (entry point for the residual semantic pass).

**Semantic/structural boundary**: Structural checkers declare their
`mismatch_types` via their rule tables. Anything NOT in any checker's rule
table is "uncovered" and belongs to the semantic layer.

**Acceptance Criteria**:
- [ ] Semantic layer receives only dimensions/aspects not covered by structural checkers
- [ ] Semantic layer uses chunked input (per-section, not full-document inline)
- [ ] When semantic layer assigns HIGH: pipeline pauses, spawns adversarial debate
- [ ] Adversarial debate produces a verdict: CONFIRM_HIGH, DOWNGRADE_TO_MEDIUM, or DOWNGRADE_TO_LOW
- [ ] Verdict is recorded in the deviation registry with debate transcript reference
- [ ] Semantic MEDIUM and LOW findings are accepted without debate
- [ ] Semantic layer prompt includes the structural findings as context (to avoid re-checking what's already checked)
- [ ] All semantic findings are tagged with `source_layer="semantic"` (see FR-6)

#### FR-4.1: Lightweight Debate Protocol

The adversarial debate for semantic HIGH validation uses a single-round
prosecutor/defender model with a deterministic automated judge. This is the
**lightweight** variant; the full `/sc:adversarial` protocol is reserved for
FR-8 regression validation.

**Roles**:

| Role | Type | LLM Calls | Purpose |
|------|------|-----------|---------|
| Prosecutor | ClaudeProcess | 1 | Argues finding IS correctly HIGH |
| Defender | ClaudeProcess | 1 | Argues finding should be downgraded |
| Judge | Deterministic Python | 0 | Scores both against rubric, produces verdict |

**Protocol**:
1. Build prosecutor prompt (argues HIGH) and defender prompt (argues downgrade)
2. Execute both via ClaudeProcess in **parallel** (2 LLM calls)
3. Parse YAML responses from each
4. Score both against 4-criterion rubric (deterministic Python, no LLM)
5. Compute margin = prosecutor_weighted − defender_weighted
6. Verdict: margin > 0.15 → CONFIRM_HIGH; margin < −0.15 → DOWNGRADE; else → CONFIRM_HIGH (conservative tiebreak)
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

| Criterion | Weight | 3 (Strong) | 0 (Missing) |
|-----------|--------|------------|-------------|
| Evidence Quality | 30% | 2+ exact quotes with section refs | No citations |
| Impact Specificity | 25% | Names specific function/data flow | No impact stated |
| Logical Coherence | 25% | Argument follows from evidence | Self-contradictory |
| Concession Handling | 20% | Addresses strongest counter-point | Field missing |

**Token budget**: ~3,800 per finding (hard cap: 5,000). Prosecutor and
defender prompts require YAML-formatted responses with `evidence_citations`,
`impact_argument`/`mitigation_argument`, and `confidence` fields.

**YAML parse failure**: If a side fails to produce valid YAML, all rubric
scores default to 0 for that side.

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

#### FR-4.2: Prompt Budget Enforcement (NFR-3)

The semantic layer enforces NFR-3 (no prompt > 30KB) via proportional budget
allocation with tail-truncation.

**Budget allocation** (total: 30,720 bytes):

| Component | Share | Bytes | Contents |
|-----------|-------|-------|----------|
| Spec + roadmap sections | 60% | 18,432 | Primary + supplementary sections for dimension |
| Structural findings context | 20% | 6,144 | "Already checked" findings to prevent re-reporting |
| Prior findings summary | 15% | 4,608 | Registry summary (max 50 entries) |
| Prompt template overhead | 5% | 1,536 | Role instructions, output format |

**Truncation rules**:
- Sections: tail-truncated on line boundary with `[TRUNCATED: N bytes omitted from '<heading>']` marker
- Structural findings: truncated at finding boundary (complete findings only)
- Prior summary: truncated at line boundary
- Template: raises `ValueError` if exceeded (code bug, not runtime condition)

**Truncation priority** (what gets cut first):
1. Prior findings summary (least critical)
2. Structural findings context (secondary)
3. Spec/roadmap sections (last resort)

**Acceptance Criteria** (FR-4.2):
- [x] `MAX_PROMPT_BYTES = 30_720` as configurable module constant (v3.0: semantic_layer.py constants)
- [x] Budget ratios are module-level constants, overridable via config (v3.0: semantic_layer.py constants)
- [x] Oversized sections are tail-truncated on line boundaries with visible markers (v3.0: `_truncate_to_budget()`)
- [ ] Truncation markers include section heading: `[TRUNCATED: N bytes omitted from '<heading>']`
- [x] `assert` before LLM call confirms prompt ≤ budget (v3.0: `build_semantic_prompt()`)
- [ ] Template exceeding 5% allocation raises `ValueError`
- [x] Empty sections produce a valid prompt without errors (v3.0: `build_semantic_prompt()`)

**Dependencies**: FR-1 (structural findings as input), FR-6 (deviation registry)

---

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

---

### FR-6: Deviation Registry

**Description**: A persistent, file-backed registry of all findings across
runs within a release. Each run appends new findings, updates status of
existing ones. The gate evaluates registry state, not fresh-scan results.

**Implementation note**: The `DeviationRegistry` class exists in `convergence.py`
(lines 50-225), not in a separate `deviation_registry.py` file. This co-location
is correct: the registry is tightly coupled with `compute_stable_id()`,
`_check_regression()`, and the convergence loop orchestrator. The
`deviation_registry.py` entry has been removed from the `relates_to` frontmatter.

**Registry Lifecycle**: Resets when spec version changes (new spec = new registry).

**Statuses**: PENDING, ACTIVE, FIXED, SKIPPED, FAILED. Both PENDING and ACTIVE
are valid initial statuses representing "not yet resolved." ACTIVE is used by
the deviation registry for findings under active tracking; PENDING is the
legacy default in existing pipeline code. Both are non-terminal.

**Source Layer Tracking**: Each finding carries a `source_layer` field
(`"structural"` or `"semantic"`) indicating which layer produced it. This
enables split tracking for convergence (see FR-7). Default is `"structural"`
for backward compatibility with pre-v3.05 registries.

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

**Run Metadata**: Each run record includes split HIGH counts:
- `structural_high_count`: HIGHs from structural checkers
- `semantic_high_count`: HIGHs from semantic layer
- `total_high_count`: sum of both

**Acceptance Criteria**:
- [ ] Registry is a JSON file in the release output directory (matching existing `DeviationRegistry` serialisation in `convergence.py`)
- [ ] Each finding has a stable ID derived from (dimension, rule_id, spec_location, mismatch_type)
- [ ] Each finding has a `source_layer` field: `"structural"` or `"semantic"`
- [ ] New runs compare current findings against registry: new findings are appended, existing findings are matched by stable ID
- [ ] Fixed findings are marked FIXED (finding no longer reproduced on current inputs)
- [ ] Registry includes run metadata: run_number, timestamp, spec_hash, roadmap_hash, structural_high_count, semantic_high_count, total_high_count
- [ ] Gate reads registry to determine pass/fail — not the raw fidelity report
- [ ] Registry resets when `spec_hash` changes (new spec version)
- [ ] Findings with `status="ACTIVE"` are accepted without error (ACTIVE added to valid statuses)
- [ ] Registries from pre-v3.05 (without `source_layer`) default missing fields to `"structural"`
- [ ] Run metadata uses a typed dataclass (`RunMetadata`) — not raw dicts — to ensure field presence and type safety at construction time

**Dependencies**: FR-1 (findings to register)

---

### FR-7: Convergence Gate

**Description**: Extends the existing `convergence.py` (323 lines, v3.0) with
`execute_fidelity_with_convergence()` and `handle_regression()`. The fidelity
gate evaluates convergence based on registry state with these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED) — includes both structural AND semantic HIGHs
- **Monotonic progress**: Each run must have ≤ **structural** HIGHs than previous run. Semantic HIGH fluctuations are logged as warnings but do NOT constitute regression.
- **Hard budget**: TurnLedger-backed budget accounting. Each checker suite run debits `CHECKER_COST` before execution; each remediation cycle debits `REMEDIATION_COST` before execution. The `can_launch()` guard replaces the fixed run counter — the engine continues as long as the ledger has sufficient budget for at least one more checker run. Cost constants are module-level in `convergence.py`. The catch/verify/backup semantic framing is preserved: Run 1 (catch) discovers deviations, Run 2 (verify) confirms remediation worked, Run 3 (backup) is the final attempt if Run 2 did not converge
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, trigger parallel validation (see FR-8)

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

**TurnLedger Injection Rationale**: The convergence engine receives a
pre-allocated `TurnLedger` instance rather than constructing its own because:
(a) the caller (pipeline executor) owns the overall budget and may have
consumed budget in steps 1-7 already; (b) the pipeline may have consumed
budget in prior steps before reaching step 8; (c) the caller may want to
reserve budget for step 9 (certification). Budget isolation (FR-7: convergence
budget vs legacy budget) is enforced by the caller choosing whether to pass a
ledger at all.

**Function Signature**:

```python
def execute_fidelity_with_convergence(
    config: RoadmapConfig,
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    output_dir: Path,
    ledger: TurnLedger,
    *,
    run_checkers: Callable[[Path, Path], tuple[list[Finding], list[Finding]]] | None = None,
    run_remediation: Callable[[list[Finding], RoadmapConfig], dict] | None = None,
    handle_regression_fn: Callable[..., RegressionResult] | None = None,
) -> ConvergenceResult:
    """Orchestrate up to 3 fidelity runs within step 8 of the pipeline.

    Args:
        config: Roadmap pipeline configuration (convergence_enabled must be True).
        registry: Active DeviationRegistry for this release.
        spec_path: Path to the spec document.
        roadmap_path: Path to the merged roadmap.
        output_dir: Pipeline output directory.
        ledger: TurnLedger instance governing budget for all fidelity runs
            and intra-loop remediation. The caller (pipeline executor) constructs
            this with initial_budget calibrated to the convergence workload.
        run_checkers: Optional injectable checker suite (default: real structural +
            semantic checkers). Signature: (spec, roadmap) -> (structural, semantic).
        run_remediation: Optional injectable remediation executor (default:
            execute_remediation from remediate_executor.py).
        handle_regression_fn: Optional injectable regression handler (default:
            handle_regression from convergence.py). Enables testing without
            spawning real parallel agents.

    Returns:
        ConvergenceResult with pass/fail, run count, and diagnostic logs.
    """
```

**Gate Authority Model**: In convergence mode (`convergence_enabled=true`),
the convergence engine is the **sole authority** for pass/fail, evaluating
only the DeviationRegistry (`registry.get_active_high_count() == 0`). The
existing `SPEC_FIDELITY_GATE` is NOT invoked. The `spec-fidelity.md` report
is still written as a human-readable summary but is not gated.

In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
exactly as in pre-v3.05, validating the LLM-generated report frontmatter
(generated by `prompts.py:build_spec_fidelity_prompt()`). In convergence mode,
`build_spec_fidelity_prompt()` is still called to generate the human-readable
`spec-fidelity.md` summary report, but its output is NOT gated — only the
`DeviationRegistry` is authoritative.
The two authorities never coexist in the same execution mode.

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

**Step Ordering Semantics** (convergence mode):

| Step | Behavior When `convergence_enabled=true` | Notes |
|------|------------------------------------------|-------|
| Steps 1-7 | Unchanged | Upstream pipeline unaffected |
| Step 8 | Convergence engine is sole authority | Up to 3 internal runs |
| Step 9 | `spec_fidelity_file` input is decorative | Report written but not gated |
| Wiring-verification | Bypasses `_embed_inputs()` | Pattern preserved |

These semantics are undocumented in v3.0 code but implemented correctly.
v3.05 makes them normative.

**Intra-Loop Remediation**: Within the convergence loop,
`execute_fidelity_with_convergence()` calls `execute_remediation()` between
runs. `remediate_executor.py` remains a pure execution engine — it is not
modified for convergence awareness. The convergence loop owns the budget
(3 runs) and translates remediation results into `DeviationRegistry` updates.

**Budget Isolation — TurnLedger vs Legacy Dispatch**:

Two budget systems exist but are **mutually exclusive** via `convergence_enabled`:

1. **Convergence mode** (`convergence_enabled=true`): `TurnLedger` governs all
   budget decisions. `can_launch()` and `can_remediate()` are the sole budget
   guards. `_check_remediation_budget()` and `_print_terminal_halt()` are
   **NOT** invoked — they belong exclusively to the legacy path.

2. **Legacy mode** (`convergence_enabled=false`): The state-file budget
   (`_check_remediation_budget()` / `_print_terminal_halt()`) governs
   remediation attempts. `TurnLedger` is **NEVER** constructed. No TurnLedger
   import occurs in this code path.

**Critical invariant**: Mutual exclusion via `convergence_enabled` is the
single dispatch point. If both budget systems run simultaneously,
double-charging occurs. The pipeline executor dispatch code is specified in
the "Pipeline Executor Wiring" subsection (see below).

#### Reimbursement Semantics

`reimburse_for_progress()` is the first production consumer of
`TurnLedger.reimbursement_rate`. When a convergence run demonstrates forward
progress (fewer structural HIGHs than the previous run), the engine credits
back a fraction of the run's cost as a reward for convergence.

**Reimbursement Mapping**:

| Scenario | Reimbursement | Rationale |
|----------|--------------|-----------|
| Converges to 0 HIGHs (PASS) | `credit(CONVERGENCE_PASS_CREDIT)` | Full early-exit credit; unused runs refunded |
| Forward progress (fewer structural HIGHs) | `credit(int(CHECKER_COST * reimbursement_rate))` | Partial credit; convergence is working |
| Stalls (same HIGH count) | No credit | No forward progress; budget consumed |
| Regresses (more structural HIGHs) | No credit + extra debit via FR-8 | Regression costs more than neutral |

**Helper Function Signature**:

```python
def reimburse_for_progress(
    ledger: TurnLedger,
    run_cost: int,
    prev_structural_highs: int,
    curr_structural_highs: int,
) -> int:
    """Credit partial refund when convergence shows forward progress.

    Returns the number of turns credited (0 if no progress).
    Uses ledger.reimbursement_rate as the credit fraction.
    """
```

**Acceptance Criteria** (Reimbursement Semantics):
- [ ] `reimburse_for_progress()` uses `ledger.reimbursement_rate`, never a hardcoded value
- [ ] Returns 0 when `curr_structural_highs >= prev_structural_highs`
- [ ] Calls `ledger.credit()` only when `credit > 0`
- [ ] Progress credit events logged to diagnostic log with format: `"Run {n}: progress credit {credit} turns (structural {prev} -> {curr})"`
- [ ] `reimbursement_rate` is sourced from the TurnLedger instance passed by the caller

#### Budget Calibration Constants

Cost constants are module-level in `convergence.py`, overridable via
`TurnLedger(initial_budget=N)`.

**Cost Constants**:

| Constant | Value | Purpose |
|----------|-------|---------|
| `CHECKER_COST` | 10 | Turns per checker suite run (structural + semantic) |
| `REMEDIATION_COST` | 8 | Turns per remediation cycle |
| `REGRESSION_VALIDATION_COST` | 15 | Turns for FR-8 (3 parallel agents + debate) |
| `CONVERGENCE_PASS_CREDIT` | 5 | Turns credited on early convergence pass |

**Derived Budgets**:

| Budget | Formula | Value |
|--------|---------|-------|
| `MIN_CONVERGENCE_BUDGET` | `CHECKER_COST * 2 + REMEDIATION_COST` | 28 |
| `STD_CONVERGENCE_BUDGET` | `CHECKER_COST * 3 + REMEDIATION_COST * 2` | 46 |
| `MAX_CONVERGENCE_BUDGET` | `STD_CONVERGENCE_BUDGET + REGRESSION_VALIDATION_COST` | 61 |

**Risk note**: These are recommended defaults; acceptance criteria should
validate existence and overridability rather than exact numeric values.
Constants may need recalibration based on real-world convergence behavior.

**Acceptance Criteria**:
- [ ] Gate reads deviation registry, not raw fidelity output
- [ ] Pass requires: `active_high_count == 0` (total: structural + semantic)
- [ ] Monotonic progress check uses `structural_high_count` only
- [ ] Semantic HIGH count increases are logged as warnings, not regressions
- [ ] Run 2 must have `structural_high_count <= run_1.structural_high_count` or trigger FR-8
- [ ] Run 3 is final: pass or halt with full report
- [ ] If budget exhausted without convergence: halt, write diagnostic report, exit non-zero
- [ ] Progress proof logged with split counts: `structural: {n} → {n+1}, semantic: {n} → {n+1}`
- [ ] In convergence mode, `SPEC_FIDELITY_GATE` is never invoked
- [ ] In legacy mode, behavior is byte-identical to pre-v3.05
- [ ] `convergence_enabled: bool = False` field on pipeline config (default preserves legacy behavior)
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
- [ ] Convergence budget and legacy budget never overlap
- [ ] `ledger: TurnLedger` is a required positional parameter on `execute_fidelity_with_convergence()` — the convergence engine does not internally construct a TurnLedger
- [ ] `run_checkers`, `run_remediation`, and `handle_regression_fn` are keyword-only optional callable overrides for testing
- [ ] Pipeline executor constructs `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` when `convergence_enabled=true`
- [ ] Legacy mode (`convergence_enabled=false`) never constructs a TurnLedger
- [ ] `_check_remediation_budget()` is never called in convergence mode
- [ ] `CHECKER_COST` debited from ledger before each checker suite run
- [ ] `REMEDIATION_COST` debited from ledger before each remediation cycle
- [ ] `can_launch()` checked before each convergence run; if false, halt with `"convergence_budget_exhausted"`
- [ ] `can_remediate()` checked before each remediation cycle; if false, halt with `"remediation_budget_exhausted"`
- [ ] Early convergence pass credits `CONVERGENCE_PASS_CREDIT` to ledger
- [ ] Forward progress credits via `reimburse_for_progress()` using `ledger.reimbursement_rate`
- [ ] `reimburse_for_progress()` helper encapsulates the reimbursement policy — credit logic is not scattered
- [ ] `reimbursement_rate` consumed as first production consumer (field previously defined but unused)
- [ ] Cost constants (`CHECKER_COST`, `REMEDIATION_COST`, `REGRESSION_VALIDATION_COST`, `CONVERGENCE_PASS_CREDIT`) are module-level in `convergence.py` and overridable
- [ ] TurnLedger imported from `superclaude.cli.sprint.models`

#### Import Boundary Justification

The cross-module import (`convergence.py` → `sprint/models.py`) is a
deliberate architectural decision:

1. TurnLedger is a pure data class with no sprint-specific dependencies
2. The import is conditional (convergence mode only)
3. The `trailing_gate` module already imports from pipeline (precedent for
   cross-module imports)
4. Long-term migration to `pipeline/models.py` tracked by cross-release
   summary (see Section 1.2 scope boundary and design.md Section 5.4)

#### Pipeline Executor Wiring

The pipeline executor step 8 dispatch code constructs a TurnLedger only when
`convergence_enabled=true`:

```python
# In roadmap/executor.py, step 8 handling:
if step.id == "spec-fidelity" and config.convergence_enabled:
    from .convergence import execute_fidelity_with_convergence
    from superclaude.cli.sprint.models import TurnLedger

    convergence_ledger = TurnLedger(
        initial_budget=MAX_CONVERGENCE_BUDGET,
        minimum_allocation=CHECKER_COST,
        minimum_remediation_budget=REMEDIATION_COST,
        reimbursement_rate=0.8,
    )
    convergence_result = execute_fidelity_with_convergence(
        config=config,
        registry=registry,
        spec_path=config.spec_file,
        roadmap_path=merge_file,
        output_dir=out,
        ledger=convergence_ledger,
    )
    # Map convergence result to StepResult for pipeline
    step_result = StepResult(
        step=step,
        status=StepStatus.PASS if convergence_result.passed else StepStatus.FAIL,
        ...
    )
    continue
else:
    # Legacy mode: state-file budget governs
    # TurnLedger is NEVER constructed
    if _check_remediation_budget(output_dir):
        execute_remediation(...)
```

See design.md Section 5.3 for detailed rationale.

**Acceptance Criteria** (Pipeline Executor Wiring):
- [ ] Dispatch code constructs TurnLedger only when `convergence_enabled=true`
- [ ] Legacy branch does not import or reference TurnLedger
- [ ] Convergence result mapped to `StepResult` for pipeline compatibility

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
    debate_verdicts: dict[str, str]  # stable_id -> verdict
    agents_succeeded: int            # out of 3
    consolidated_report_path: Path
```

**Lifecycle Within Convergence Loop**:
1. Run N completes -> convergence engine checks `structural_high_count`
2. If regression detected -> `handle_regression()` called
3. `handle_regression()` spawns 3 parallel agents (FR-8)
4. Results merged -> adversarial debate validates each HIGH
5. Registry updated with validated findings and debate verdicts
6. **This entire flow counts as one "run" toward the budget of 3**
7. Convergence engine proceeds to next run or halts

**Budget Accounting Rule** (TurnLedger terms): Regression validation debits
`REGRESSION_VALIDATION_COST` from TurnLedger. This debit **subsumes**
post-regression remediation within the same run — there is no separate
`REMEDIATION_COST` debit for remediation that occurs as part of regression
handling. `handle_regression()` does NOT perform any ledger operations
internally — budget ownership stays with FR-7 (the convergence engine debits
before calling `handle_regression()`). `handle_regression_fn: Callable` is
injectable for testing (see FR-7 function signature).

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
- [ ] `ledger.debit(REGRESSION_VALIDATION_COST)` called before `handle_regression()` invocation
- [ ] `handle_regression()` does not perform any ledger operations internally
- [ ] No separate `REMEDIATION_COST` debit for post-regression remediation within the same run (subsumes)

**Dependencies** (FR-7.1): FR-7 (convergence gate), FR-8 (regression detection), FR-6 (registry)

**Dependencies**: FR-6 (registry), FR-7.1 (FR-8 interface contract), FR-8 (regression handling)

---

### FR-8: Regression Detection & Parallel Validation

**Description**: When run N+1 has MORE **structural** HIGHs than run N
(regression detected), the system extends the existing temp dir isolation
mechanism in `convergence.py` (lines 278-323) to spawn 3 parallel validation
agents in isolated temporary directories. Each independently re-runs the
fidelity check. Their findings are collected, merged by stable ID,
deduplicated, sorted by severity, and written to a consolidated report. After
consolidation, an adversarial debate validates the severity of each HIGH.

**Isolation mechanism**: Each agent operates in its own temporary directory
containing independent copies of all input files (spec, roadmap, registry
snapshot), reusing and extending the temp dir + atexit cleanup pattern already
implemented in `convergence.py`. This replaces git worktrees because the files
that need isolation (roadmap, registry) are output artifacts not tracked by
git. Temp directories provide true input isolation at ~1.5MB vs ~150MB per
worktree.

**Cleanup protocol** (extends existing `atexit` cleanup in `convergence.py:310-323`):
1. Primary: `finally` block in the orchestrator guarantees cleanup
2. Fallback: `atexit` handler registered after directory creation (pattern already in convergence.py)
3. Identification: directories use prefix `fidelity-validation-{session_id}-`
4. No git state pollution (no `.git/worktrees/` entries)

**Acceptance Criteria**:
- [ ] Regression detected when `current_run.structural_high_count > previous_run.structural_high_count`
- [ ] Semantic HIGH increases alone do NOT trigger regression (see FR-7)
- [ ] 3 agents spawned in parallel, each in its own isolated temporary directory containing independent copies of all input files (spec, roadmap, registry snapshot)
- [ ] Each agent runs the full checker suite (structural + semantic) independently
- [ ] Results are merged: findings matched by stable ID across all 3 agents
- [ ] Unique findings (those appearing in any agent's results) are preserved
- [ ] Consolidated report written to `fidelity-regression-validation.md`
- [ ] Findings sorted by severity (HIGH → MEDIUM → LOW)
- [ ] After consolidation: adversarial debate validates severity of each HIGH
- [ ] Debate verdicts update the deviation registry
- [ ] This entire flow counts as one "run" toward the budget of 3
- [ ] All 3 agents must succeed for the consolidated result to be valid; if any agent fails, the entire regression validation is marked FAILED and the run is not counted toward the budget
- [ ] Cleanup guaranteed via try/finally; atexit fallback registered
- [ ] No git worktree calls; no `.git/worktrees/` artifacts after completion

**Dependencies**: FR-1 (checkers), FR-4 (adversarial), FR-6 (registry), FR-7 (budget)

---

### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Extends the existing `remediate_executor.py` (563 lines, v3.0)
to produce structured patches in a MorphLLM-compatible JSON format, applied via
ClaudeProcess (the established pipeline execution engine). The patch format is
engine-agnostic: a future migration to MorphLLM requires only swapping the
applicator, not the patch generation or validation logic.

**Note**: The convergence engine debits `REMEDIATION_COST` before calling
`execute_remediation()`; the remediation executor itself does not interact
with TurnLedger.

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

**Patch Format (Engine-Agnostic Lazy Snippets)**:
Patches use a JSON schema compatible with MorphLLM's semantic merging format.
This format is NOT tied to MorphLLM as execution engine — it is a structured
intermediate representation that any applicator can consume:
```
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

**Acceptance Criteria**:
- [x] Snapshot create/restore/cleanup primitives exist (v3.0: lines 53-101)
- [x] File path allowlist enforcement exists (v3.0: `enforce_allowlist()`)
- [x] ClaudeProcess agent dispatch exists (v3.0: `_run_agent_for_file()`)
- [ ] Remediation agents output structured lazy edit snippets per finding (MorphLLM-compatible JSON format)
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] `RemediationPatch` dataclass defined with typed fields matching JSON schema
- [ ] ClaudeProcess applies patches as primary engine; `fallback_apply()` handles failures via deterministic text replacement (minimum anchor: 5 lines or 200 chars)
- [ ] `check_morphllm_available()` probes MCP runtime; when True, MorphLLM replaces ClaudeProcess as applicator
- [ ] Per-patch diff-size guard: each `RemediationPatch` independently evaluated against threshold — reject if `changed_lines / patch_original_lines > 30%` (denominator is the line count of the patch's `original_code` block, not the entire target file)
- [ ] `_check_diff_size()` retired; replaced by per-patch evaluation of `RemediationPatch` objects
- [ ] Partial rejection supported: valid patches applied even when others for the same file are rejected
- [ ] Rejected patches logged with reason (patch ID, actual ratio, threshold); finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file: each file evaluated independently after all its patches are applied
- [ ] Post-execution coherence check: if a file's patches succeed but the file shares cross-file findings with a failed file, coherence pass evaluates whether to roll back the successful file
- [ ] Existing snapshot/restore mechanism retained for per-file rollback
- [ ] `_DIFF_SIZE_THRESHOLD_PCT` changed from 50 to 30 (BF-5 adversarial review)

#### FR-9.1: `--allow-regeneration` Flag

The `--allow-regeneration` CLI flag provides explicit user consent for patches
that exceed the diff-size threshold. This is a binary flag (not a continuous
scale) to prevent accidental over-permitting.

**Mechanism**:
- `allow_regeneration: bool = False` field on `RoadmapConfig`
- CLI: `superclaude roadmap run spec.md --allow-regeneration`
- When `True` and a patch exceeds the threshold: log WARNING and proceed
- When `False` (default) and a patch exceeds the threshold: reject, mark FAILED

**Acceptance Criteria** (FR-9.1):
- [ ] `--allow-regeneration` is a Click `is_flag=True` option on the `run` command
- [ ] Config field defaults to `False`
- [ ] Without flag: patches exceeding 30% threshold are rejected (FAILED)
- [ ] With flag: patches exceeding 30% threshold are applied with WARNING log
- [ ] WARNING log includes patch ID, actual ratio, and threshold
- [ ] Existing behavior preserved when flag is not passed

**Dependencies**: FR-6 (finding IDs link patches to registry)

---

### FR-10: Run-to-Run Memory

**Description**: Each fidelity run has access to prior run findings and their
outcomes. The deviation registry (FR-6) is the primary memory mechanism. The
fidelity prompt (for the semantic layer) includes a summary of prior findings
to prevent re-discovery of already-fixed issues and to anchor severity
classification.

Each run's metadata captures TurnLedger state at completion (consumed,
reimbursed, available) for convergence diagnostics. This enables post-hoc
analysis of budget consumption patterns and reimbursement effectiveness.

**Optional `RunMetadata` field**: `budget_snapshot: dict | None = None`
containing `budget_consumed`, `budget_reimbursed`, and `budget_available`
integer values. Defaults to `None` for backward compatibility with
pre-v3.05 registries.

**Acceptance Criteria**:
- [ ] Semantic layer prompt includes: prior findings summary (ID, severity, status, run_number)
- [ ] Structural checkers implicitly have memory via registry diff (new vs known findings)
- [ ] Registry tracks `first_seen_run` and `last_seen_run` per finding
- [ ] Fixed findings from prior runs are not re-reported as new
- [ ] Summary is bounded: max 50 prior findings in prompt, oldest first truncated
- [ ] Run metadata includes ledger snapshot (`budget_consumed`, `budget_reimbursed`, `budget_available`) when convergence mode is active
- [ ] Progress proof logging includes budget state: `"budget: consumed={c}, reimbursed={r}, available={a}"`
- [ ] Progress credit events logged with format: `"Run {n}: progress credit {credit} turns (structural {prev} -> {curr})"`

**Dependencies**: FR-4 (semantic layer), FR-6 (registry)

---

## 4. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | Determinism | Same inputs → identical structural findings | Run twice on same inputs, diff output |
| NFR-2 | Convergence | ≤3 runs to pass or halt | Run counter in registry |
| NFR-3 | Prompt size | No single prompt exceeds 30KB | Proportional budget allocation in `build_semantic_prompt`; tail-truncation with `[TRUNCATED]` markers; `assert` before LLM call (see FR-4.2) |
| NFR-4 | Checker independence | Checkers share no mutable state | Code review; parallel execution test |
| NFR-5 | Edit safety | No file changes >30% without user consent | Diff-size guard metric |
| NFR-6 | Traceability | Every finding traceable to rule_id or debate verdict | Audit log review |
| NFR-7 | Backward compat | Existing pipeline steps (1-7) unchanged | Integration test |

---

## 5. User Stories / Acceptance Criteria

### US-1: Pipeline operator runs fidelity gate on v3.0 spec
**Given** a spec and merged roadmap
**When** the fidelity gate runs
**Then** structural checkers produce deterministic findings, semantic layer handles residual checks, and the gate evaluates the deviation registry — producing a PASS (0 active HIGHs) or FAIL with a clear report.

### US-2: LLM assigns HIGH severity to a semantic finding
**Given** a semantic finding classified as HIGH
**When** the pipeline reaches that classification
**Then** an adversarial debate is spawned, produces a verdict (CONFIRM/DOWNGRADE), and the verdict is recorded in the registry before the gate evaluates.

### US-3: Run 2 regresses (more structural HIGHs than Run 1)
**Given** Run 2 produces more structural HIGHs than Run 1
**When** structural regression is detected
**Then** 3 parallel agents in isolated temp directories independently validate, results are merged/deduped into `fidelity-regression-validation.md`, adversarial debate validates each HIGH, and updated findings are written to the registry. Semantic HIGH increases alone do not trigger this flow.

### US-4: Remediation edits a roadmap section
**Given** a HIGH finding with a recommended correction
**When** remediation runs
**Then** a structured patch is generated, validated against the diff-size guard (≤30% changed lines), applied to the target file, and the finding is marked FIXED in the registry. If the patch exceeds the threshold, it is rejected and the finding is marked FAILED.

### US-5: Budget exhausted without convergence
**Given** 3 runs completed without reaching 0 active HIGHs
**When** the budget check triggers
**Then** the pipeline halts, writes a diagnostic report listing all active findings with run history, and exits non-zero.

Note: Budget exhaustion may also occur before all 3 runs complete if individual
operations (checker suite, remediation, regression validation) consume more
budget than anticipated. The diagnostic report includes TurnLedger state
(consumed, reimbursed, available) for root-cause analysis.

### US-6: New spec version cuts
**Given** the spec hash changes (new version)
**When** the pipeline starts
**Then** the deviation registry is reset (fresh start for new spec), and all prior findings are archived.

---

## 6. Resolved Questions

| # | Question | Resolution |
|---|----------|------------|
| 1 | Should structural checkers produce confidence scores alongside severity? | **No.** Fixed severity is sufficient. Structural checkers are deterministic — their findings are definitionally certain. |
| 2 | Should FR-8 adversarial debate use full `/sc:adversarial` or lighter variant? | **Lighter-weight variant.** Full adversarial protocol is reserved for FR-4 (semantic HIGH validation). Regression validation uses a streamlined debate focused solely on severity confirmation, reducing token budget and latency. |
| 3 | What is the patch schema for structured remediation? | **Engine-agnostic lazy edit snippets.** Remediation agents produce typed JSON patches with `original_code` anchors and `update_snippet` replacements. Context markers (`// ... existing code ...`) indicate unchanged regions. The format is MorphLLM-compatible but engine-agnostic: ClaudeProcess is the primary applicator, with deterministic Python fallback. MorphLLM integration is a future swap requiring zero patch format changes. |
| 4 | Should diff-size guard be per-file or per-patch? | **Per-patch.** Each individual patch is evaluated against the 30% threshold independently. This prevents a single large edit from hiding behind many small ones, and allows fine-grained rejection of oversized patches while accepting valid small ones for the same file. |
| 5 | How should cross-section references be handled in sectional comparison? | **Reference graph with bidirectional linking.** When the parser extracts structured data, it also extracts cross-references (e.g., FR-1.2 in Sec 3 referencing a signature in Sec 4). Checkers receive their primary sections plus any referenced sections as supplementary context. This keeps prompts bounded while preserving semantic completeness. The section→dimension mapping includes a "supplementary sections" field populated by reference extraction. |
| 6 | Should monotonic progress check include semantic HIGHs? | **No — structural only.** Semantic layer is LLM-based and non-deterministic; temperature variation can cause false regressions. Monotonic enforcement applies only to `structural_high_count`. Semantic fluctuations are logged as warnings. The gate still requires 0 total HIGHs (structural + semantic) to pass. (BF-3) |
| 7 | Should parallel validation use git worktrees? | **No — temporary directories.** The files needing isolation (roadmap, registry) are output artifacts not tracked by git. Worktrees isolate source code, which checkers only read. Temp directories with file copies provide true input isolation at ~1.5MB vs ~150MB per worktree. (BF-4) |
| 8 | How should SPEC_FIDELITY_GATE and the registry coexist? | **Mutual exclusion.** In convergence mode, only the registry is authoritative. SPEC_FIDELITY_GATE is excluded entirely. In legacy mode, only SPEC_FIDELITY_GATE is used. The two never coexist. (BF-2) |
| 9 | What initial statuses are valid for Finding? | **Both PENDING and ACTIVE.** ACTIVE is added for registry use; PENDING is retained for legacy pipeline code. Both represent "not yet resolved." Removing PENDING would break existing serialized data and tests. (BF-1) |
| 10 | How is NFR-3 prompt size enforced? | **Proportional budget allocation with tail-truncation.** 60% spec/roadmap, 20% structural context, 15% prior summary, 5% template. Truncation snaps to line boundaries. `assert` before LLM call. `ValueError` if template exceeds its 5% allocation. (BF-7) |
| 11 | What debate protocol for semantic HIGH validation? | **Single-round prosecutor/defender with deterministic judge.** Lightweight variant: 2 parallel LLM calls, YAML responses, 4-criterion rubric (evidence 30%, impact 25%, coherence 25%, concession 20%), 0.15 margin threshold, conservative tiebreak favors CONFIRM_HIGH. ~3,800 tokens per finding. (BF-6) |

---

## 7. Handoff

**Next steps**:
- `/sc:roadmap` — Generate roadmap from this amended requirements spec
- `/sc:tasklist` — Generate implementation tasklist from the roadmap

**Completed prior steps**:
- `/sc:design` — Architecture design completed (see `architecture-design.md`)
- `/sc:adversarial` — Design review completed, 7 blocking findings identified and resolved
- BF resolutions folded into this spec as amendments (v1.0.0 → v1.1.0)

**TurnLedger integration notes**:
1. `reimbursement_rate=0.8` activated as first production consumer via `reimburse_for_progress()` in convergence loop
2. TurnLedger class itself is NOT modified — consumed as-is from `sprint/models.py`
3. Cross-release dependency: v3.1 wires gate-pass reimbursement via same `reimbursement_rate` field, different code path — semantics are complementary, not conflicting
4. Future cleanup: TurnLedger migration `sprint/models.py` → `pipeline/models.py` (coordinate with v3.1)

**Risk**: Cross-module import (`convergence.py` → `sprint/models.py`) becomes
a one-line fix if TurnLedger migrates to `pipeline/models.py`.

**Key implementation risks**:
1. Spec parser robustness — real specs may deviate from template
2. Stable finding IDs — hash collisions or overly-specific IDs causing false "new" findings
3. Temp directory cleanup — atexit + finally must guarantee no leaked dirs
4. Debate rubric calibration — heuristic scoring thresholds may need tuning on real findings
5. Backward compatibility — all new behavior gated behind `convergence_enabled=False` default
6. Cross-module import (`convergence.py` → `sprint/models.py`) — one-line migration fix if TurnLedger moves to `pipeline/models.py`; tracked in handoff notes

---

## Appendix A: Current vs Proposed Architecture

### Current (as-is)
```
Spec + Roadmap (full inline) → Single LLM call → Fidelity report (YAML frontmatter)
  → Gate checks high_severity_count == 0
  → If fail: LLM agents edit files in-place (full file context)
  → Retry once → Pass or halt
```

### Proposed (to-be)
```
Spec + Roadmap → Parser extracts structured data per section
  → 5 Structural Checkers (parallel) → Typed findings (source_layer="structural")
  → Residual Semantic Layer (chunked, budget-enforced ≤30KB) → Semantic findings (source_layer="semantic")
    → If any semantic HIGH: lightweight debate (prosecutor/defender + deterministic judge) → verdict
  → All findings → Deviation Registry (append/update, split structural/semantic counts)
  → Convergence Gate reads registry (sole authority in convergence mode)
    → Pass: 0 active HIGHs (structural + semantic)
    → Structural regression detected: 3 parallel agents in temp dirs → merge → debate
    → Semantic fluctuation: log warning, continue (not regression)
    → Fail + budget remaining: structured patch remediation (diff-size guarded, --allow-regeneration opt-in)
    → Fail + budget exhausted: halt with diagnostic report
```

### Proposed Remediation Flow
```
Active findings → Group by target file
  → Per file: generate MorphLLM-compatible lazy edit snippets
  → Validate: per-patch diff-size guard (≤30% changed lines)
    → If exceeds AND --allow-regeneration: log WARNING, proceed
    → If exceeds AND no flag: reject, mark FAILED
  → Apply: ClaudeProcess (or deterministic fallback with original_code anchor)
  → Rollback: per-file snapshot/restore on failure
  → Update registry: FIXED / FAILED per finding
```

### Proposed Convergence Loop Detail (TurnLedger-Annotated)
```
Step 8 (Fidelity Gate) with convergence_enabled=true:
┌──────────────────────────────────────────────────────────────┐
│ Pipeline Executor:                                            │
│   ledger = TurnLedger(initial_budget=61)  ← MAX_CONVERGENCE  │
│                                                                │
│ execute_fidelity_with_convergence(ledger):                     │
│                                                                │
│  Run 1 (catch):                                                │
│    ← ledger.can_launch() guard                                 │
│    ← ledger.debit(CHECKER_COST=10)                             │
│    Structural checkers (parallel) → findings                   │
│    Semantic layer (chunked) → findings                         │
│    → Deviation Registry update                                 │
│    → Check: 0 active HIGHs? → ledger.credit(CONVERGENCE_PASS_ │
│      CREDIT=5) → PASS → exit                                  │
│                                                                │
│  ← ledger.can_remediate() guard                                │
│  ← ledger.debit(REMEDIATION_COST=8)                           │
│  Remediation (structured patches, diff-guarded)                │
│                                                                │
│  Run 2 (verify):                                               │
│    ← ledger.can_launch() guard                                 │
│    ← ledger.debit(CHECKER_COST=10)                             │
│    Same checker suite → new findings                           │
│    → Monotonic check (structural only)                         │
│    → If forward progress: reimburse_for_progress()             │
│    → If regression: ledger.debit(REGRESSION_VALIDATION_COST=15)│
│      → handle_regression() [FR-8]                              │
│    → Check: 0 active HIGHs? → ledger.credit(5) → PASS → exit  │
│                                                                │
│  ← ledger.can_remediate() guard                                │
│  ← ledger.debit(REMEDIATION_COST=8)                           │
│  Remediation                                                   │
│                                                                │
│  Run 3 (backup — final):                                       │
│    ← ledger.can_launch() guard                                 │
│    ← ledger.debit(CHECKER_COST=10)                             │
│    Same checker suite → final findings                         │
│    → Check: 0 active HIGHs? → ledger.credit(5) → PASS → exit  │
│    → Else: HALT with diagnostic report + TurnLedger state      │
│                                                                │
│  Budget exhaustion at any guard → HALT with diagnostic report  │
│  Pipeline sees: PASS or HALT (never intermediate)              │
└──────────────────────────────────────────────────────────────┘
```

## Appendix B: Structural Checkability Evidence

Based on analysis of real deviations from 4 failed runs on v3.0:

| Deviation | Dimension | Could Be Structural? | Rule |
|-----------|-----------|---------------------|------|
| Phantom FR-009..FR-038 IDs | Signatures | Yes | Roadmap IDs ⊆ spec-defined IDs |
| Phantom NFR IDs | Signatures | Yes | Same |
| Missing `wiring_config.py` | Data Models | Yes | Spec manifest files ⊆ roadmap files |
| Wrong path prefix (`audit/` vs `cli/audit/`) | Data Models | Yes | Path prefix exact match |
| Missing test infrastructure files | Data Models | Yes | Manifest coverage |
| `ast_analyze_file()` dual placement | Signatures | Partial | Duplicate function detection |
| `audit_artifacts_used` omission | Gates | Partial | Field set comparison (but spec contradiction complicates) |
| `<2s` vs `<5s` threshold | NFRs | Yes | Numeric threshold extraction + comparison |
| Missing `yaml.safe_dump()` | NFRs | Yes | Security primitive presence check |
| Missing `_get_all_step_ids()` update | Gates | Mostly | Explicit MUST item → task mapping |
| Wrong `gate_passed()` signature | Signatures | Yes | Function signature matching |
| Missing step parameters | Gates | Yes | `Step(...)` parameter set comparison |
| "Implicitly covers" a requirement | Cross-cutting | No | Requires semantic judgment |
| Stricter phasing than spec | Gates | Partial | Dependency graph comparison (structural); intent judgment (semantic) |
| Additive risk R9 | Cross-cutting | No | Requires judgment on additive content |

## Appendix C: v1.1.0 Amendment Traceability

Amendments from adversarial design review (7 blocking findings). Each BF
resolution was debated, scored, and validated before incorporation.

| BF | Severity | Spec Section Amended | Change Summary | Solution Source |
|----|----------|---------------------|----------------|----------------|
| BF-1 | CRITICAL | FR-6 (statuses), Resolved Q#9 | Added ACTIVE to valid Finding statuses alongside PENDING | `bf1-final.md` |
| BF-2 | HIGH | FR-7 (gate authority), Resolved Q#8 | Gate authority model: registry-only in convergence mode, SPEC_FIDELITY_GATE excluded | `bf2-final.md` |
| BF-3 | HIGH | FR-6 (source_layer), FR-7 (monotonic), FR-8 (trigger), US-3, Resolved Q#6 | Split structural/semantic tracking; monotonic enforcement on structural only | `bf3-final.md` |
| BF-4 | HIGH | FR-8 (isolation), US-3, Appendix A, Resolved Q#7 | Replaced git worktrees with temp directory copies for parallel validation | `bf4-final.md` |
| BF-5 | HIGH | FR-9.1, Appendix A (remediation flow) | Added `--allow-regeneration` binary flag with full CLI/config/guard spec | `bf5-final.md` |
| BF-6 | HIGH | FR-4.1, Resolved Q#11 | Specified lightweight debate protocol: single-round, deterministic rubric, YAML output | `bf6-final.md` |
| BF-7 | HIGH | FR-4.2, NFR-3, Resolved Q#10 | Specified prompt budget enforcement: proportional allocation, tail-truncation, assert | `bf7-final.md` |

**Solution documents**: `adversarial-design-review/solutions/bf{1-7}-final.md`
**Debate transcript**: `adversarial-design-review/adversarial/debate-transcript.md`
**Validation report**: `adversarial-design-review/workflow/validation-report.md`
