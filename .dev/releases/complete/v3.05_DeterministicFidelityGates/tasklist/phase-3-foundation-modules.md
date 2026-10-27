---
phase: 3
title: "Foundation Modules"
tasks: 4
depends_on: [1]
parallelizable: partial
---

# Phase 3: Foundation Modules

These are the base modules that all other new code depends on.
Dependency order: T08 (parser) → T10 (checkers), T09 (severity rules) → T10 (checkers), T11 independent.

```
T08 (parser) ──┐
               ├──→ T10 (checkers)
T09 (rules)  ──┘

T11 (section splitter) — independent, can parallel with T08/T09
```

---

### T08: Create spec_parser.py (FR-2)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/spec_parser.py (NEW)
**FR**: FR-2 — Spec & Roadmap Parser
**Risk**: HIGH — critical path (§7f). Parser robustness against real specs is implementation risk #1.

**Action**: Create a parser that extracts structured data from spec and roadmap markdown. FR-2 specifies 10 extraction capabilities:

1. Parse YAML frontmatter from both spec and roadmap
2. Extract markdown tables by section (keyed by heading path)
3. Extract fenced code blocks with language annotation
4. Extract requirement ID families via regex: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
5. Extract Python function signatures from fenced blocks: `def name(params) -> return_type`
6. Extract file paths from manifest tables (Sec 4.1, 4.2, 4.3)
7. Extract `Literal[...]` enum values from code blocks
8. Extract numeric threshold expressions: `< 5s`, `>= 90%`, `minimum 20`
9. Return structured objects, not raw text
10. Support cross-section reference extraction (FR-5 Resolved Q#5)

**Interface**: `parse_spec(spec_path: Path) -> ParsedSpec` and `parse_roadmap(roadmap_path: Path) -> ParsedRoadmap`

**Testing**: Parse the actual v3.05 spec (`deterministic-fidelity-gate-requirements.md`) as a smoke test. Verify all 10 extraction types produce non-empty results.

**Acceptance criteria**:
- [ ] All 10 FR-2 acceptance criteria met
- [ ] Returns structured dataclass objects
- [ ] Handles missing sections gracefully (empty result, not exception)
- [ ] Smoke test passes against real v3.05 spec

---

### T09: Create severity rule tables (FR-3)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/structural_checkers.py (or severity_rules.py — co-locate with checkers)
**FR**: FR-3 — Anchored Severity Rules
**Risk**: HIGH — foundation dependency (§7e). Every checker depends on this.

**Action**: Define severity rule tables as code data structures (not prompt text). The spec provides the initial rule table in FR-3:

```python
# Keyed by (dimension, mismatch_type) → severity
SEVERITY_RULES: dict[tuple[str, str], str] = {
    ("signatures", "id_not_in_spec"): "HIGH",
    ("signatures", "function_missing"): "HIGH",
    ("signatures", "param_arity_mismatch"): "MEDIUM",
    ("data_models", "required_file_missing"): "HIGH",
    ("data_models", "path_prefix_mismatch"): "HIGH",
    ("data_models", "enum_literal_uncovered"): "MEDIUM",
    ("gates", "frontmatter_field_missing"): "HIGH",
    ("gates", "step_param_missing"): "MEDIUM",
    ("gates", "ordering_violated"): "MEDIUM",
    ("cli", "config_mode_uncovered"): "MEDIUM",
    ("cli", "default_mismatch"): "MEDIUM",
    ("nfrs", "threshold_contradicted"): "HIGH",
    ("nfrs", "security_primitive_missing"): "HIGH",
    ("nfrs", "dependency_violated"): "HIGH",
    ("nfrs", "coverage_mismatch"): "MEDIUM",
}
```

**Requirements**:
- Rules defined in code, keyed by `(dimension, mismatch_type) → severity`
- Same inputs always produce same severity (deterministic)
- Extensible: new rules can be added without changing checker logic
- Lookup function: `get_severity(dimension: str, mismatch_type: str) -> str`

**Acceptance criteria**:
- [ ] All 4 FR-3 acceptance criteria met
- [ ] Rule table covers all 15 mismatch types from spec
- [ ] `get_severity()` returns deterministic results
- [ ] Adding a new rule requires only a dict entry, not code changes

---

### T10: Create structural_checkers.py (FR-1)

**Tier**: complex
**File**: src/superclaude/cli/roadmap/structural_checkers.py (NEW)
**FR**: FR-1 — Decomposed Structural Checkers (5 Dimensions)
**Depends on**: T08 (parser), T09 (severity rules)

**Action**: Create 5 independent checkers, one per dimension:

| # | Checker | Input from Parser | Structural % |
|---|---------|------------------|--------------|
| 1 | Signatures | Function sigs, FR/NFR/SC ID sets | 80% |
| 2 | Data Models | File manifest tables, dataclass fields, enum literals | 85% |
| 3 | Gates | GateCriteria fields, Step params, step ordering | 65% |
| 4 | CLI Options | CLI table, config fields, Literal modes, defaults | 75% |
| 5 | NFRs | Numeric thresholds, security primitives, dependency rules | 55% |

**Interface**: Each checker is `Callable[[Path, Path], list[Finding]]` taking `(spec_path, roadmap_path)`.

**Requirements**:
- Each checker uses spec_parser (T08) for extraction
- Each checker uses severity_rules (T09) for severity assignment
- Checkers produce `Finding` objects with: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location
- Checkers can run in parallel (no shared state — NFR-4)
- A registry maps dimension names to checker callables

**Acceptance criteria**:
- [ ] All 5 FR-1 acceptance criteria met
- [ ] Each checker is independent and stateless
- [ ] Checkers use severity rule table, not LLM prose
- [ ] Each Finding includes rule_id and source_layer="structural"
- [ ] Checker registry allows parallel dispatch

---

### T11: Create section splitter for chunked comparison (FR-5)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/spec_parser.py (extend T08's parser)
**FR**: FR-5 — Sectional/Chunked Comparison

**Action**: Add section-splitting capability to the parser so that checkers and the semantic layer receive per-section input rather than full documents:

1. Split spec by `## N. Section Name` headings into named chunks
2. Split roadmap by phase/task headings into named chunks
3. Provide dimension→sections mapping: which spec sections are relevant to each checker
4. Support supplementary sections via cross-reference extraction (Resolved Q#5)
5. Enforce prompt size bound per chunk (default ~30KB, configurable)

**Interface**: `split_by_sections(doc_path: Path) -> dict[str, str]` returning `{section_name: section_content}`

**Acceptance criteria**:
- [ ] All 6 FR-5 acceptance criteria met
- [ ] Section mapping is deterministic
- [ ] No single prompt contains both full documents inline
- [ ] Cross-references include supplementary sections
