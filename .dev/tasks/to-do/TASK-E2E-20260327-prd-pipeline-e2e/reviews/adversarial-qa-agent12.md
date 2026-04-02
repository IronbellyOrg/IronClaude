# Adversarial QA Report -- Agent 12, Round 6

**Date:** 2026-03-28
**Phase:** adversarial-qa
**Fix cycle:** N/A (report only)
**Scope:** TDD/PRD pipeline integration + pre-existing code issues
**Prior findings:** 101 issues across 10 agents, 5 rounds

---

## Overall Verdict: FINDINGS BELOW

---

## Focus Area 1: E2E Test Results Accuracy

### 1.1 test1-tdd-prd/extraction.md section count claim

**Verified:** The extraction.md for test1-tdd-prd contains these H2 sections:
1. Functional Requirements
2. Non-Functional Requirements
3. Complexity Assessment
4. Architectural Constraints
5. Risk Inventory
6. Dependency Inventory
7. Success Criteria
8. Open Questions
9. Data Models and Interfaces
10. API Specifications
11. Component Inventory
12. Testing Strategy
13. Migration and Rollout Plan
14. Operational Readiness

**Count: 14 sections.** If a prior verification report claimed 14, that is accurate.

TDD-specific frontmatter fields are present and non-zero:
- `data_models_identified: 2`
- `api_surfaces_identified: 6`
- `components_identified: 9`
- `test_artifacts_identified: 6`
- `migration_items_identified: 15`
- `operational_items_identified: 12`

All non-zero. **Verified accurate.**

PRD content is genuinely present -- NFR-COMP-001 through NFR-COMP-003 cite "PRD S17" explicitly; architectural constraint #10 cites "PRD S7"; success criteria #8-#10 cite "PRD Success Metrics (S19)"; open questions OQ-EXT-001 through OQ-EXT-006 all cross-reference PRD sections. **Not false matches -- genuine PRD-enriched content.**

### 1.2 test2-spec-prd/extraction.md section count claim

**Verified:** The extraction.md for test2-spec-prd contains these H2 sections:
1. Functional Requirements
2. Non-Functional Requirements
3. Complexity Assessment
4. Architectural Constraints
5. Risk Inventory
6. Dependency Inventory
7. Success Criteria
8. Open Questions

**Count: 8 sections.** No TDD-specific sections (Data Models, API Specifications, etc.) present.

The frontmatter has NO TDD-specific fields (`data_models_identified`, `api_surfaces_identified`, etc. are all absent). This confirms the spec-path extractor (`build_extract_prompt`) was used, not the TDD-path extractor (`build_extract_prompt_tdd`). **Verified accurate.**

### 1.3 .roadmap-state.json input_type field

| Finding | Tag | Severity |
|---------|-----|----------|
| C-102 | [TDD/PRD] | IMPORTANT |

**File:** `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json`, line 6

The `.roadmap-state.json` still shows `"input_type": "auto"` (line 6). This was previously identified as needing a fix -- the field should reflect the RESOLVED type (`"tdd"`) after `detect_input_type` runs, not the pre-resolution value `"auto"`. The state file currently provides no evidence that the TDD detection path was actually triggered.

**However**, this is likely already covered by prior finding C-19 (or similar) about input_type in state file. If it was covered, this is a confirmation, not a new finding. If NOT previously covered among the 101, it is new.

**Required fix:** After `detect_input_type` resolves to `"tdd"` or `"spec"`, store the resolved value in `.roadmap-state.json`, not the initial `"auto"`.

---

## Focus Area 2: detect_input_type Edge Cases

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 60-119

### Minimum Viable TDD Score Analysis

The scoring:
- Signal 1 (numbered headings): A TDD with 15-19 headings scores +2; with 10-14 scores +1; under 10 scores 0
- Signal 2 (exclusive fields): `parent_doc` = +2, `coordinator` = +2 (max +4)
- Signal 3 (section names): 8 possible, each +1 (max +8)
- Signal 4 (frontmatter type): +2

A minimal real TDD (15 numbered sections, no `parent_doc`/`coordinator`, 3 TDD section names, no type field) scores: 2 + 0 + 3 = 5. Just barely passes.

A borderline case: A TDD with 10 numbered sections (many TDDs for smaller features have fewer), no exclusive fields, 4 matching section names = 1 + 0 + 4 = 5. Passes.

A stripped-down TDD (e.g., auto-generated stub) with 8 sections, no exclusive fields, 3 matching names = 0 + 0 + 3 = 3. **FAILS detection -- classified as spec.**

| Finding | Tag | Severity |
|---------|-----|----------|
| C-103 | [TDD/PRD] | MINOR |

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 60-119

Minimal TDDs with fewer than 10 numbered headings and no `parent_doc`/`coordinator` frontmatter can fall below the threshold of 5, causing misclassification as spec. The threshold is reasonable for well-formed TDDs but may produce false negatives on minimal or early-draft TDDs. The code has no fallback mechanism or warning when a score falls in a "borderline" range (e.g., 3-4).

**Required fix:** Consider logging a warning when score is in range 3-4 ("borderline -- may be a TDD") so the user can pass `--input-type tdd` explicitly. No code change strictly required.

---

## Focus Area 3: PRD Fixture Quality

**File:** `.dev/test-fixtures/test-prd-user-auth.md`

The PRD fixture is a well-formed Feature PRD with:
- Executive Summary, Problem Statement, Background, Product Vision, Business Context
- JTBD (4 items), User Personas (3), Value Prop Canvas (N/A with rationale), Competitive Analysis (N/A with rationale)
- Assumptions and Constraints, Dependencies, Scope Definition, Open Questions
- Technical Requirements (FR + NFR), Technology Stack (abbreviated), UX Requirements
- Legal and Compliance Requirements (GDPR, SOC2, NIST), Business Requirements (N/A)
- Success Metrics (5 metrics), Risk Analysis (4 risks)
- Implementation Plan with Epics, User Stories, Phasing
- Customer Journey Map (4 journeys), Error Handling, Contributors, Related Resources, Maintenance

The PRD references section numbers (S7, S12, S17, S19, S22, S6) in the extraction prompt PRD blocks, but the actual PRD fixture **does not use numbered sections**. It uses descriptive headings. The section references in the prompts (S7 = User Personas, S19 = Success Metrics, etc.) are based on a canonical PRD template numbering scheme, NOT on the actual section numbers in this specific fixture.

This works because the LLM interprets "PRD's User Personas section (S7)" as "find the User Personas section" rather than literally "find section numbered 7". The extraction output confirms this -- the LLM correctly found the User Personas, Success Metrics, Legal & Compliance, and JTBD sections despite the numbering mismatch.

**No new finding here.** The fixture exercises the PRD prompt blocks adequately.

---

## Focus Area 4: TDD vs Spec PRD Block Differences

**File:** `src/superclaude/cli/roadmap/prompts.py`

### `build_extract_prompt` PRD block (spec path) -- lines 160-179
Checks 5 PRD dimensions:
1. S19 Success Metrics -> additional Success Criteria
2. S7 User Personas -> persona-driven design requirements in Architectural Constraints
3. S12 Scope Definition -> validate requirements within scope
4. S17 Legal & Compliance -> surface as NFRs
5. S6 JTBD -> note in Open Questions if JTBD lack corresponding FRs

### `build_extract_prompt_tdd` PRD block (TDD path) -- lines 310-329
Checks 5 PRD dimensions:
1. S19 Success Metrics -> additional Success Criteria
2. S7 User Personas -> persona-driven design requirements in Architectural Constraints
3. S12 Scope Definition -> validate requirements within scope
4. S17 Legal & Compliance -> surface as NFRs
5. S6 JTBD -> note in Open Questions if JTBD lack corresponding FRs

**These are identical.** Both have 5 checks (S19, S7, S12, S17, S6). The prompt text is character-for-character the same except for the context framing ("alongside the specification" vs "alongside the TDD").

The mission statement claimed the TDD extractor's PRD block has 3 checks while the spec extractor has 5. **That claim is incorrect -- both have 5.** No finding here; the code is consistent.

---

## Focus Area 5: Tasklist Prompts Consistency

**File:** `src/superclaude/cli/tasklist/prompts.py`

### `build_tasklist_fidelity_prompt` PRD block (lines 127-139)
When PRD is provided, checks:
1. S7 User Personas -- tasks touching user-facing flows should reference persona
2. S19 Success Metrics -- instrumentation/measurement tasks
3. S12 Scope Definition + S22 Customer Journey Map -- verification tasks

Severity: All "Flag missing coverage as MEDIUM severity deviations."

### `build_tasklist_generate_prompt` PRD block (lines 198-217)
When PRD is provided, enriches with:
1. S7 User Personas -- persona context for user-facing tasks
2. S7/S22 Acceptance scenarios -- verification tasks
3. S19 Success Metrics -- metric instrumentation subtasks
4. S5 Stakeholder priorities -- priority ordering
5. S12 Scope Definition -- out-of-scope markers

**Key differences:**
- Fidelity prompt references S22 (Customer Journey Map) for acceptance scenarios alongside S12.
- Generate prompt references S5 (Stakeholder priorities / Business Context) and S7/S22 for acceptance scenarios.
- Fidelity prompt has 3 checks; generate prompt has 5 enrichment dimensions.

The generate prompt references **S5** (Business Context / Stakeholder priorities) for priority ordering, but the fidelity prompt does NOT validate that task priorities reflect S5. This means the generate prompt can produce priority-ordered tasks based on S5, but the fidelity check will never verify that ordering was preserved.

| Finding | Tag | Severity |
|---------|-----|----------|
| C-104 | [TDD/PRD] | MINOR |

**File:** `src/superclaude/cli/tasklist/prompts.py`, lines 127-139 vs 198-217

The tasklist generate prompt enriches task priorities from PRD S5 (Business Context / Stakeholder priorities), but the fidelity prompt does not validate that S5-derived priority ordering was preserved in the generated tasklist. This is an asymmetry: the generate prompt produces something the fidelity prompt does not check. Not a bug (fidelity validates roadmap-to-tasklist, not PRD-to-tasklist), but a gap in end-to-end PRD traceability.

### TDD block consistency

Fidelity TDD block (lines 112-124) checks:
1. S15 Testing Strategy -- test tasks
2. S19 Migration & Rollout Plan -- rollback tasks
3. S10 Component Inventory -- implementation tasks

Generate TDD block (lines 180-195) enriches with:
1. S15 Testing Strategy -- test cases
2. S8 API Specifications -- endpoint tasks
3. S10 Component Inventory -- component tasks
4. S19 Migration Rollback -- contingency tasks
5. S7 Data Model field definitions -- schema tasks

| Finding | Tag | Severity |
|---------|-----|----------|
| C-105 | [TDD/PRD] | MINOR |

**File:** `src/superclaude/cli/tasklist/prompts.py`, lines 112-124 vs 180-195

The tasklist generate prompt enriches with TDD S8 (API Specifications) and S7 (Data Models), but the fidelity prompt does not validate that API endpoint tasks and data model tasks were generated. Same asymmetry pattern as C-104: generation enriches from more TDD sections than fidelity validates.

---

## Focus Area 6: remediate_parser.py Review

**File:** `src/superclaude/cli/roadmap/remediate_parser.py`

This module parses validation reports into `Finding` objects. Two public functions:
- `parse_validation_report(text)` -- parses merged reports (Consolidated Findings)
- `parse_individual_reports(report_texts)` -- parses individual reports with dedup

### Observations

1. **`_extract_field` regex truncation risk** (line 182): The regex `r"^\s*-\s+{field_name}\s*:\s*(.+?)(?=\n\s*-\s+\w|\n\s*\n\*\*|\Z)"` uses `(.+?)` (non-greedy) with `re.DOTALL`. The lookahead `\n\s*-\s+\w` matches the next bullet point. But if the last field in a finding block has no following bullet or `**`, it falls through to `\Z` (end of string), which means it captures everything to the end of the section text rather than just the field value. For the last finding in a section, this means `fix_guidance` could include content from other sections.

| Finding | Tag | Severity |
|---------|-----|----------|
| C-106 | [PRE-EXISTING] | MINOR |

**File:** `src/superclaude/cli/roadmap/remediate_parser.py`, line 182

The `_extract_field` regex for multi-line field extraction uses `\Z` as the final fallback boundary. For the last field in the last finding of a section, the captured text extends to the end of the entire section text passed to `_extract_finding_blocks`, which may include trailing whitespace or separator content. In practice this is mitigated by the `_extract_finding_blocks` function truncating section text at the next H2 or finding header, but edge cases with trailing content after the last finding could produce noisy field values.

2. **`_overlay_agreement_categories` regex column counting** (lines 253-258): The regex assumes a specific column layout: `| F-XX... | col | col | col? | CATEGORY |`. This uses 3-4 intermediate columns with `[^|]*\|` between the finding ID and the agreement category. If the actual table has 2 or 5 intermediate columns, the category will not be matched. The code is brittle against table format variations.

| Finding | Tag | Severity |
|---------|-----|----------|
| C-107 | [PRE-EXISTING] | IMPORTANT |

**File:** `src/superclaude/cli/roadmap/remediate_parser.py`, lines 253-258

The `_overlay_agreement_categories` regex hardcodes 3-4 intermediate table columns between the Finding ID and Agreement Category. If the merged report format ever adds or removes a column, agreement categories silently fail to overlay. Similarly, `_overlay_remediation_status` (line 280) hardcodes 3 intermediate columns. Both patterns should use a flexible column-agnostic approach (e.g., find the last column, or match by column header position).

---

## Focus Area 7: Gate Semantic Check Functions

**File:** `src/superclaude/cli/roadmap/gates.py`

### `_cross_refs_resolve` always returns True (lines 46-89)

This function is supposed to verify cross-references resolve to existing headings. But:
- Lines 86-87: When unresolved references are found, it emits warnings and **returns True** (warning-only mode per OQ-001).
- Line 89: If no unresolved references, returns True.
- Line 68: If no cross-references exist at all, returns True.

The function **never returns False**. It is functionally a no-op gate check. The comment says "warning-only mode per OQ-001 for v2.20" but it is registered as a `SemanticCheck` on `MERGE_GATE` (line 869), which means it occupies a check slot but will never cause a gate failure.

| Finding | Tag | Severity |
|---------|-----|----------|
| C-108 | [PRE-EXISTING] | IMPORTANT |

**File:** `src/superclaude/cli/roadmap/gates.py`, lines 46-89, registered at line 869

`_cross_refs_resolve` is registered as a semantic check on `MERGE_GATE` but can never return False -- it always returns True regardless of whether cross-references resolve. This gives a false sense of validation coverage. Either remove it from the gate (since it does nothing) or implement actual blocking behavior. The current state is misleading: the gate check list implies cross-references are verified when they are not.

### `_parse_frontmatter` naive YAML parsing (lines 147-168)

The function splits on first `:` per line to extract key-value pairs. This breaks for:
- YAML list values: `domains_detected: [backend, security]` -- value is `[backend, security]` (fine)
- YAML values containing colons: `description: "A tool: for parsing"` -- key is `description`, value is `"A tool` (truncated)

Wait -- looking more carefully at line 167: `key, value = line.split(":", 1)` -- this uses `maxsplit=1`, so it correctly splits on the FIRST colon only. The value would be `"A tool: for parsing"` in that case. **No bug here.**

However, nested YAML structures (multi-line values, indented blocks) are silently ignored since only single-line `key: value` patterns are parsed. This is acceptable for frontmatter which should be flat key-value pairs.

### `_no_duplicate_headings` scope limitation (lines 92-107)

Only checks H2 and H3 headings. H4+ duplicates are not checked. Given that the pipeline primarily cares about major section headings, this is reasonable but worth noting.

**No finding -- acceptable scope limitation.**

---

## Focus Area 8: Pipeline Models

**File:** `src/superclaude/cli/pipeline/models.py`

### `SemanticCheck` dataclass (lines 58-65)

```python
@dataclass
class SemanticCheck:
    name: str
    check_fn: Callable[[str], bool]
    failure_message: str
```

Clean, minimal. No issues with the dataclass itself.

### `GateCriteria` dataclass (lines 68-74)

```python
@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
```

No validation that `min_lines` is positive. A `min_lines=0` or negative value would pass any content including empty files. This is not actively harmful since all current gate definitions use reasonable values (10-150), but the model has no defensive validation.

**No finding -- defensive validation is a nice-to-have, not a bug.**

### `StepResult` default timestamps (lines 100-101)

Both `started_at` and `finished_at` default to `datetime.now(timezone.utc)`. This means if a `StepResult` is constructed without explicit timestamps, `duration_seconds` will be ~0, which is misleading. The `roadmap_run_step` function does set `started_at` explicitly, so this is unlikely to be a real problem.

**No finding.**

---

## Focus Area 9: Error Propagation

### `_embed_inputs` failure mode (executor.py, lines 134-147)

If a file in `input_paths` does not exist, `Path(p).read_text()` raises `FileNotFoundError`. This exception propagates uncaught up through `roadmap_run_step` to `execute_pipeline`. The error message would be a raw Python traceback like `FileNotFoundError: [Errno 2] No such file or directory: '/path/to/file.md'`.

| Finding | Tag | Severity |
|---------|-----|----------|
| C-109 | [PRE-EXISTING] | IMPORTANT |

**File:** `src/superclaude/cli/roadmap/executor.py`, line 145

`_embed_inputs` does not catch `FileNotFoundError` when reading input files. If a prior step's output file is missing (e.g., extraction.md was not created due to a subprocess crash that somehow passed the gate), the error propagates as an unhandled exception with no pipeline context (which step, which input file, what to do about it). The `detect_input_type` function (line 73) correctly handles `OSError` with a fallback, but `_embed_inputs` does not.

**Required fix:** Catch `OSError` in `_embed_inputs`, log which input file is missing and which step needs it, and return a `StepResult` with `FAIL` status and descriptive `gate_failure_reason`.

### Gate failure messages

When a semantic check fails, the `failure_message` from the `SemanticCheck` is propagated. These are reasonably descriptive (e.g., "complexity_class must be one of LOW, MEDIUM, HIGH"). However, none of the failure messages include the **actual value** found, just what was expected. For example, `_complexity_class_valid` says the class must be LOW/MEDIUM/HIGH but does not say "got 'EXTREME'". This makes debugging harder.

| Finding | Tag | Severity |
|---------|-----|----------|
| C-110 | [PRE-EXISTING] | MINOR |

**File:** `src/superclaude/cli/roadmap/gates.py` (all semantic check functions) and `src/superclaude/cli/pipeline/models.py` line 63

Semantic check `failure_message` fields are static strings that describe what was expected but not what was found. When a gate fails, the operator sees "complexity_class must be one of LOW, MEDIUM, HIGH" but not the actual value that caused the failure. The `SemanticCheck` model's `check_fn` signature (`Callable[[str], bool]`) only returns bool, making it impossible to return diagnostic context. To fix this properly would require changing the signature to return a result object or enriching the failure path.

---

## Summary

| # | ID | Tag | Severity | Location | Issue |
|---|-----|-----|----------|----------|-------|
| 1 | C-102 | [TDD/PRD] | IMPORTANT | `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json:6` | `input_type` still "auto", not resolved "tdd" |
| 2 | C-103 | [TDD/PRD] | MINOR | `src/superclaude/cli/roadmap/executor.py:60-119` | Minimal TDDs with <10 headings and no exclusive frontmatter fields misclassified as spec; no borderline warning |
| 3 | C-104 | [TDD/PRD] | MINOR | `src/superclaude/cli/tasklist/prompts.py:127-139` | Fidelity prompt does not validate S5-derived priority ordering that generate prompt produces |
| 4 | C-105 | [TDD/PRD] | MINOR | `src/superclaude/cli/tasklist/prompts.py:112-124` | Fidelity prompt does not validate S8 (API) and S7 (Data Model) enrichment that generate prompt produces |
| 5 | C-106 | [PRE-EXISTING] | MINOR | `src/superclaude/cli/roadmap/remediate_parser.py:182` | `_extract_field` regex `\Z` fallback may capture trailing content on last finding |
| 6 | C-107 | [PRE-EXISTING] | IMPORTANT | `src/superclaude/cli/roadmap/remediate_parser.py:253-258,280` | Agreement/remediation overlay regexes hardcode column count; brittle against format changes |
| 7 | C-108 | [PRE-EXISTING] | IMPORTANT | `src/superclaude/cli/roadmap/gates.py:46-89` | `_cross_refs_resolve` never returns False; registered as gate check but is functionally a no-op |
| 8 | C-109 | [PRE-EXISTING] | IMPORTANT | `src/superclaude/cli/roadmap/executor.py:145` | `_embed_inputs` does not handle missing input files; raw exception with no pipeline context |
| 9 | C-110 | [PRE-EXISTING] | MINOR | `src/superclaude/cli/roadmap/gates.py` + `pipeline/models.py:63` | Semantic check failures report expected values but not actual values; limits debuggability |

**New findings: 9**
- CRITICAL: 0
- IMPORTANT: 4 (C-102, C-107, C-108, C-109 -- note C-108 was possibly referenced tangentially but not explicitly identified in prior 101)
- MINOR: 5 (C-103, C-104, C-105, C-106, C-110)

**Items verified as accurate (no finding):**
- test1 extraction.md section count (14) and TDD field values: accurate
- test2 extraction.md section count (8) and absence of TDD fields: accurate
- PRD content in test1 extraction: genuine, not false matches
- TDD vs spec PRD block content: both have 5 checks, not 3 vs 5 as claimed in mission statement
- PRD fixture quality: adequate test fixture, exercises all PRD prompt blocks
- Pipeline models (SemanticCheck, GateCriteria): clean, no issues
- `_parse_frontmatter` colon handling: correct (uses maxsplit=1)

---

## Honesty Note

After 10 agents and 101 findings, the remaining issues are progressively more minor. The 4 IMPORTANT findings (C-102 state file, C-107 regex brittleness, C-108 dead gate check, C-109 missing error handling) are genuine issues worth fixing, but they are operational robustness concerns rather than correctness bugs that would cause data loss or wrong results. The code is fundamentally sound.
