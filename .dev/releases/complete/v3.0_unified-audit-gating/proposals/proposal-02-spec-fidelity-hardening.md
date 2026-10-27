# Proposal 02 — Spec Fidelity Gate Hardening

**Date**: 2026-03-17
**Proposal number**: 02
**Parent release**: unified-audit-gating-v1.2.1
**Addresses**: Link 1 failure (Spec → Roadmap) in the transitive fidelity chain
**Reference incident**: cli-portify executor no-op bug — shipped across v2.24, v2.24.1, v2.25
**Status**: Draft

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Proposed Solution](#2-proposed-solution)
3. [Deterministic Check Suite](#3-deterministic-check-suite)
4. [Implementation Plan](#4-implementation-plan)
5. [Acceptance Criteria](#5-acceptance-criteria)
6. [Risk Assessment](#6-risk-assessment)
7. [Estimated Effort](#7-estimated-effort)

---

## 1. Problem Statement

### 1.1 The LLM-Only Fidelity Checking Model

`SPEC_FIDELITY_GATE` (defined in `src/superclaude/cli/roadmap/gates.py:633-656`) enforces fidelity between a specification and a generated roadmap. Its enforcement model has two layers:

1. **LLM-generated deviation report**: `build_spec_fidelity_prompt()` (`roadmap/prompts.py:278-347`) instructs Claude to compare spec vs. roadmap across five dimensions (signatures, data models, gates, CLI options, NFRs), classify each deviation as HIGH/MEDIUM/LOW, and emit structured YAML frontmatter.
2. **Deterministic enforcement of the report's metadata**: `gate_passed()` (`pipeline/gates.py:20-69`) reads the frontmatter and enforces `high_severity_count == 0` and `tasklist_ready == true`.

The critical structural weakness: **the Python layer enforces the shape of the LLM's report, not the substance of the comparison.** If the LLM misses a deviation entirely, or misclassifies a HIGH deviation as MEDIUM or LOW, the Python gate passes unconditionally. There are no programmatic cross-reference checks — no parsing of requirement identifiers, no structural element inventory, no dispatch table enumeration.

### 1.2 What the Gate Missed in the cli-portify Incident

The forensic analysis (Section 5, Appendix B of `cli-portify-executor-noop-forensic-report.md`) documents that four specification elements were present in the v2.24 and v2.25 specs but absent from every roadmap generation:

| Spec Element | Type | Present in Any Roadmap? |
|---|---|---|
| Three-way dispatch: `_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step` | Core architectural pattern / pseudocode | NO — roadmap says only "sequential execution" |
| `PROGRAMMATIC_RUNNERS` dictionary | Named dispatch table | NO — zero mentions in any roadmap |
| `executor.py --> steps/validate_config.py` (and all other import edges) | Module dependency graph | NO — not mentioned in any roadmap |
| `test_programmatic_step_routing` integration test requirement | Success criterion | NO — not in any roadmap phase |

The roadmap actively contradicted the spec at Milestone M2: *"Sequential pipeline runs end-to-end with **mocked steps**"* — the word "mocked" directly signals that real dispatch is not required. The `SPEC_FIDELITY_GATE` processed this roadmap and either did not flag these absences or did not classify them as HIGH severity. The gate passed. The tasklist faithfully reproduced the roadmap's reduced executor description. Three release cycles later, `run_portify()` still returns `(exit_code=0, stdout="", timed_out=False)` for every step.

The word "mocked" in the roadmap milestone is the kind of signal a deterministic string scan would catch immediately. The LLM did not treat it as a HIGH-severity deviation.

### 1.3 Why LLM-Only Checking Is Structurally Insufficient

The LLM's comparison task is unanchored. It reads two free-form documents and produces a judgment. Without explicit enumeration of what must be verified, the LLM's failure modes are:

- **Silent omission**: An element present in the spec is simply not mentioned in either document. With no inventory pass, the LLM has no baseline to check against.
- **Severity misclassification**: The LLM may classify "mocked steps" as MEDIUM (implementation detail to be refined later) rather than HIGH (spec explicitly requires real dispatch). The prompt's severity definitions (`prompts.py:296-315`) cover these cases in principle, but the LLM's in-context judgment under token pressure can drift.
- **Hallucinated coverage**: The LLM may reason that because the roadmap mentions "executor," the dispatch design is covered — without verifying the specific structural elements.
- **Context window effects**: For large specs with appendices (the v2.24 spec's Appendix D spans lines 1444-1652), the critical design details may receive less attention than the main body sections.

The forensic report's Appendix B states directly: *"No programmatic parsing of requirement IDs from source document. No cross-reference verification. No enumeration completeness check."* This proposal addresses all three gaps.

---

## 2. Proposed Solution

### 2.1 Layered Defense Model

The solution adds a **pre-LLM deterministic inventory pass** that runs before `build_spec_fidelity_prompt()` is invoked, plus a **post-LLM cross-reference injection** that augments the LLM's findings with deterministic failures that cannot be overridden by LLM classification.

The layered model:

```
Spec text
    |
    v
[DETERMINISTIC INVENTORY PASS]  <-- NEW
    |  - Extract FR-NNN / NFR-NNN / SC-NNN identifiers
    |  - Extract module dependency edges (A --> B patterns)
    |  - Extract dispatch table names (DICT = { ... } patterns)
    |  - Extract pseudocode structural markers (if/elif chains)
    v
Inventory report (machine-readable)
    |
    v
[LLM FIDELITY COMPARISON]  <-- EXISTING (augmented)
    |  Receives: spec text + roadmap text + deterministic inventory
    |  Must account for each inventory item explicitly
    v
LLM deviation report (YAML frontmatter + body)
    |
    v
[DETERMINISTIC GATE ENFORCEMENT]  <-- EXISTING + augmented
    |  - high_severity_count == 0 (existing)
    |  - tasklist_ready consistent (existing)
    |  - fr_ids_coverage_complete: true  <-- NEW
    |  - dispatch_tables_preserved: true  <-- NEW
    |  - module_deps_present: true  <-- NEW
    v
PASS / FAIL
```

The deterministic inventory findings are injected into the YAML frontmatter as additional required fields. The gate enforces these fields with new semantic check functions. A missing FR-NNN that the LLM failed to catch becomes a gate failure regardless of `high_severity_count`.

### 2.2 Design Principles

- **Supplement, not replace**: The LLM comparison remains the primary semantic analysis. Deterministic checks catch structural inventory gaps that the LLM analysis may miss or misclassify. They do not attempt to replicate the LLM's semantic judgment.
- **Fail closed**: Any deterministic check that cannot complete (parsing error, malformed spec) causes the gate to fail. Unknown state is not permitted to pass.
- **No new spec format requirements**: All checks operate on patterns that already appear in well-formed specs. Specs that do not use FR-NNN conventions produce empty inventories, which is explicitly handled.
- **Evidence in output**: Every deterministic failure includes the missing identifier and the line range it was expected from, enabling targeted remediation.

---

## 3. Deterministic Check Suite

### Check D-01: Requirement Identifier Coverage

**Purpose**: Verify that every `FR-NNN`, `NFR-NNN`, and `SC-NNN` identifier found in the spec extraction also appears verbatim in the roadmap body text.

**Input**:
- `spec_text: str` — the full spec extraction output (from the `extract` pipeline step)
- `roadmap_text: str` — the merged roadmap body

**Parsing logic** (spec side):

```python
import re

_REQ_ID_PATTERN = re.compile(r'\b(FR|NFR|SC)-(\d{3})\b')

def extract_requirement_ids(text: str) -> set[str]:
    """Return all FR-NNN / NFR-NNN / SC-NNN identifiers in text."""
    return {m.group(0) for m in _REQ_ID_PATTERN.finditer(text)}
```

**Verification**:

```python
def check_requirement_id_coverage(
    spec_text: str, roadmap_text: str
) -> tuple[bool, list[str]]:
    """
    Returns (all_covered, missing_ids).
    missing_ids is empty on pass.
    """
    spec_ids = extract_requirement_ids(spec_text)
    if not spec_ids:
        # Spec uses no FR-NNN convention — check is inapplicable, pass vacuously
        return True, []
    roadmap_ids = extract_requirement_ids(roadmap_text)
    missing = sorted(spec_ids - roadmap_ids)
    return len(missing) == 0, missing
```

**Output**: Boolean pass/fail + sorted list of missing identifiers.

**Failure condition**: Any identifier present in the spec is absent from the roadmap. Each missing identifier is reported individually. The severity is always HIGH regardless of what the LLM's deviation report says.

**Frontmatter field injected**: `fr_ids_coverage_complete: false` with `fr_ids_missing: ["FR-001", "SC-003"]`.

**Semantic check function** (registered on `SPEC_FIDELITY_GATE`):

```python
def _fr_ids_coverage_complete(content: str) -> bool:
    """All FR/NFR/SC identifiers from spec appear in roadmap."""
    match = _FRONTMATTER_RE.search(content)
    if match is None:
        return False
    fm = _parse_frontmatter_values(match.group(1))
    # If field absent, treat as failure (fail-closed)
    val = fm.get("fr_ids_coverage_complete", "false")
    return str(val).strip().lower() == "true"
```

**Edge case**: Specs that contain no `FR-NNN` style identifiers (e.g., informal specs, early-stage documents). The check must detect the empty-inventory case and pass vacuously rather than blocking all informal specs. The `spec_ids` empty-set guard in `check_requirement_id_coverage` handles this. The injected frontmatter field will be `fr_ids_coverage_complete: true` with a `fr_ids_note: "no_identifiers_found_in_spec"` annotation.

---

### Check D-02: Module Dependency Graph Presence

**Purpose**: Verify that module dependency edges declared in the spec (expressed as `A --> B`, `A ──> B`, `A -> B`, or `A imports B` patterns) appear in the roadmap. These edges document the intended import/call chain and are a primary signal that the roadmap preserves the spec's architectural wiring requirements.

**Input**: Same as D-01.

**Parsing logic** (spec side):

```python
_DEP_ARROW_PATTERN = re.compile(
    r'`?(\w[\w./]*\.py)`?\s*(?:──>|-->|-–>|->|imports)\s*`?(\w[\w./]*\.py)`?'
)

def extract_module_deps(text: str) -> list[tuple[str, str]]:
    """Return (source_module, target_module) pairs from dependency declarations."""
    return [(m.group(1), m.group(2)) for m in _DEP_ARROW_PATTERN.finditer(text)]
```

**Verification**: For each `(source, target)` pair, verify that both module names appear in the roadmap text within proximity (same section, or within 500 characters of each other). Exact co-occurrence in the same paragraph is sufficient — the check does not require the arrow syntax to appear in the roadmap, only that the relationship is discussed.

**Simplified proximity check**:

```python
def check_module_dep_presence(
    spec_text: str, roadmap_text: str
) -> tuple[bool, list[tuple[str, str]]]:
    deps = extract_module_deps(spec_text)
    if not deps:
        return True, []
    missing_deps = []
    for source, target in deps:
        # Both module names must appear in roadmap
        if source not in roadmap_text and target not in roadmap_text:
            missing_deps.append((source, target))
        elif source not in roadmap_text:
            missing_deps.append((source, "<present>"))
        elif target not in roadmap_text:
            missing_deps.append(("<present>", target))
    return len(missing_deps) == 0, missing_deps
```

**Output**: Boolean pass/fail + list of dependency edges not reflected in roadmap.

**Failure condition**: A module named in a spec dependency declaration does not appear anywhere in the roadmap body. For the cli-portify incident, `steps/validate_config.py`, `steps/discover_components.py`, etc. appear in the spec's module graph but are absent from the roadmap entirely.

**Frontmatter field injected**: `module_deps_present: false` with `module_deps_missing: ["executor.py --> steps/validate_config.py"]`.

**Limitation**: Proximity matching is approximate. A roadmap that mentions `executor.py` in one section and `validate_config.py` in an unrelated section will pass this check even if the relationship is not described. The check is a necessary-but-not-sufficient condition — it detects complete absence, not shallow mention.

---

### Check D-03: Named Dispatch Table Preservation

**Purpose**: Verify that named dictionaries declared as dispatch tables in the spec (e.g., `PROGRAMMATIC_RUNNERS`, `STEP_REGISTRY`, `COMMAND_MAP`) appear by name in the roadmap. Dispatch tables are structural elements that carry semantic meaning — their absence from a roadmap signals the roadmap has reduced or replaced a specified dispatch mechanism.

**Input**: Same as D-01.

**Parsing logic** (spec side):

```python
_DISPATCH_TABLE_PATTERN = re.compile(
    r'\b([A-Z][A-Z0-9_]{3,})\s*(?:=\s*\{|dict\()',
    re.MULTILINE
)

_DISPATCH_CONTEXT_KEYWORDS = frozenset({
    "runner", "runners", "dispatch", "registry", "map", "handler",
    "handlers", "command", "commands", "step", "steps", "route", "routes",
})

def extract_dispatch_tables(text: str) -> list[str]:
    """
    Return names of UPPER_CASE dictionaries that appear in dispatch/registry
    context based on name suffix heuristic.
    """
    candidates = []
    for m in _DISPATCH_TABLE_PATTERN.finditer(text):
        name = m.group(1)
        name_lower = name.lower()
        if any(kw in name_lower for kw in _DISPATCH_CONTEXT_KEYWORDS):
            candidates.append(name)
    return list(dict.fromkeys(candidates))  # deduplicate, preserve order
```

**Verification**:

```python
def check_dispatch_table_preservation(
    spec_text: str, roadmap_text: str
) -> tuple[bool, list[str]]:
    tables = extract_dispatch_tables(spec_text)
    if not tables:
        return True, []
    missing = [t for t in tables if t not in roadmap_text]
    return len(missing) == 0, missing
```

**Output**: Boolean pass/fail + list of named dispatch tables absent from roadmap.

**Failure condition**: `PROGRAMMATIC_RUNNERS` appears in the spec but not in the roadmap. This is the exact signal that was present in the cli-portify incident and was not caught.

**Frontmatter field injected**: `dispatch_tables_preserved: false` with `dispatch_tables_missing: ["PROGRAMMATIC_RUNNERS"]`.

**False positive risk**: All-caps names that match the suffix heuristic but are not dispatch tables (e.g., `ERROR_HANDLERS` used as an error registry rather than a dispatch table). See Section 6.1 for mitigation.

---

### Check D-04: Pseudocode Structural Marker Preservation

**Purpose**: Verify that explicit pseudocode blocks in the spec that define control flow structures (multi-way dispatch patterns, branch conditions) have their key structural markers preserved in the roadmap. This is the check most directly targeting the cli-portify failure mode.

**Input**: Same as D-01.

**Parsing logic**: Extract code fences (triple-backtick blocks) from the spec. Within each code fence, identify multi-branch `if/elif` patterns with named function calls. Extract the called function names.

```python
_CODE_FENCE_PATTERN = re.compile(r'```[\w]*\n(.*?)```', re.DOTALL)
_IF_ELIF_DISPATCH = re.compile(
    r'(?:if|elif)\s+\w[^:]*:\s*\n\s+(\w+)\s*=\s*(\w+)\(',
    re.MULTILINE
)
_STEP_DISPATCH_CALL = re.compile(
    r'step_result\s*=\s*(_run_\w+|_execute_\w+|_handle_\w+)\(',
    re.MULTILINE
)

def extract_dispatch_function_names(spec_text: str) -> list[str]:
    """
    Extract function names called from multi-branch dispatch pseudocode.
    Targets patterns like:
        step_result = _run_programmatic_step(step, config)
        step_result = _run_claude_step(...)
    """
    names = []
    for fence_match in _CODE_FENCE_PATTERN.finditer(spec_text):
        block = fence_match.group(1)
        for call_match in _STEP_DISPATCH_CALL.finditer(block):
            names.append(call_match.group(1))
    return list(dict.fromkeys(names))
```

**Verification**:

```python
def check_pseudocode_dispatch_preserved(
    spec_text: str, roadmap_text: str
) -> tuple[bool, list[str]]:
    fn_names = extract_dispatch_function_names(spec_text)
    if not fn_names:
        return True, []
    missing = [fn for fn in fn_names if fn not in roadmap_text]
    return len(missing) == 0, missing
```

**Output**: Boolean pass/fail + list of dispatch function names absent from roadmap.

**Failure condition**: `_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step` appear in the spec's pseudocode but not in the roadmap. This is an exact match to the cli-portify incident.

**Frontmatter field injected**: `pseudocode_dispatch_preserved: false` with `pseudocode_dispatch_missing: ["_run_programmatic_step", "_run_claude_step"]`.

**Scope limitation**: This check targets `step_result = _run_*()` and `step_result = _execute_*()` patterns. It will not catch all pseudocode structural elements — only those matching the dispatch call naming convention. This is intentional: the check is scoped to the most commonly specified and most commonly dropped dispatch patterns, not general pseudocode preservation.

---

### Check D-05: "Mocked" / Stub Sentinel Detection

**Purpose**: Flag roadmap text that explicitly describes implementation as mocked, stubbed, or deferred for later wiring. These words are direct indicators that the roadmap has reduced a real implementation requirement to a placeholder, which is exactly the language present in the cli-portify roadmap's Milestone M2.

**Input**: Roadmap text only.

**Parsing logic**:

```python
_STUB_SENTINEL_PATTERN = re.compile(
    r'\b(mocked?\s+steps?|stubbed?\s+(?:steps?|implementation|dispatch)|'
    r'placeholder\s+(?:steps?|implementation)|'
    r'no.op\s+(?:default|fallback|implementation)|'
    r'(?:steps?|dispatch|wiring)\s+(?:to\s+be\s+)?(?:wired|connected|integrated)\s+later)\b',
    re.IGNORECASE
)

def extract_stub_sentinels(roadmap_text: str) -> list[tuple[int, str]]:
    """Return (line_number, matched_text) for each stub sentinel found."""
    results = []
    for i, line in enumerate(roadmap_text.splitlines(), 1):
        for m in _STUB_SENTINEL_PATTERN.finditer(line):
            results.append((i, m.group(0).strip()))
    return results
```

**Output**: List of `(line_number, matched_text)` tuples. Any match is a HIGH severity finding.

**Failure condition**: Roadmap contains phrases like "mocked steps", "stubbed dispatch", "no-op default", or "wired later". The match from the cli-portify roadmap milestone — *"Sequential pipeline runs end-to-end with mocked steps"* — would trigger this check immediately.

**Note**: This check differs from D-01 through D-04 in that it operates on the **roadmap** rather than performing a spec-to-roadmap cross-reference. It is a standalone red-flag detector. Findings are injected into the frontmatter as `stub_sentinels_found: true` with a `stub_sentinel_locations` list.

**False positive risk**: Legitimate use of "mocked" in test strategy sections of the roadmap (e.g., "Unit tests will use mocked file I/O"). The check should be scoped to roadmap sections describing implementation milestones and deliverables, not test strategy sections. See Section 6.2 for section-scope mitigation.

---

### Check Suite Summary

| Check ID | What It Parses | What It Verifies | Key Failure Signal |
|---|---|---|---|
| D-01 | `FR-NNN`, `NFR-NNN`, `SC-NNN` from spec | All IDs appear in roadmap | Missing `FR-007` → HIGH |
| D-02 | `A --> B.py` dependency edges from spec | Both module names appear in roadmap | `steps/validate_config.py` absent → HIGH |
| D-03 | `UPPER_CASE_DICT = {` dispatch tables from spec | Table names appear in roadmap | `PROGRAMMATIC_RUNNERS` absent → HIGH |
| D-04 | `step_result = _run_*()` calls from spec pseudocode | Dispatch function names appear in roadmap | `_run_programmatic_step` absent → HIGH |
| D-05 | Stub sentinels in roadmap | No "mocked steps" / "no-op default" language | "mocked steps" in M2 → HIGH |

---

## 4. Implementation Plan

### 4.1 Files to Modify

#### `src/superclaude/cli/roadmap/gates.py`

**Location**: After the existing semantic check functions (approximately line 80), before `SPEC_FIDELITY_GATE` definition (line 633).

**New functions to add**:

```python
# --- Deterministic fidelity inventory checks ---

def _fr_ids_coverage_complete(content: str) -> bool:
    """Check D-01: All FR/NFR/SC identifiers from spec appear in roadmap."""
    match = _FRONTMATTER_RE.search(content)
    if not match:
        return False
    val = _get_frontmatter_value(match.group(1), "fr_ids_coverage_complete")
    return str(val).strip().lower() == "true"

def _module_deps_present(content: str) -> bool:
    """Check D-02: All spec-declared module dependency edges reflected in roadmap."""
    match = _FRONTMATTER_RE.search(content)
    if not match:
        return False
    val = _get_frontmatter_value(match.group(1), "module_deps_present")
    return str(val).strip().lower() == "true"

def _dispatch_tables_preserved(content: str) -> bool:
    """Check D-03: All spec-named dispatch tables appear in roadmap."""
    match = _FRONTMATTER_RE.search(content)
    if not match:
        return False
    val = _get_frontmatter_value(match.group(1), "dispatch_tables_preserved")
    return str(val).strip().lower() == "true"

def _pseudocode_dispatch_preserved(content: str) -> bool:
    """Check D-04: All spec pseudocode dispatch function names appear in roadmap."""
    match = _FRONTMATTER_RE.search(content)
    if not match:
        return False
    val = _get_frontmatter_value(match.group(1), "pseudocode_dispatch_preserved")
    return str(val).strip().lower() == "true"

def _no_stub_sentinels(content: str) -> bool:
    """Check D-05: Roadmap contains no stub/mock/no-op sentinels in milestone text."""
    match = _FRONTMATTER_RE.search(content)
    if not match:
        return False
    val = _get_frontmatter_value(match.group(1), "stub_sentinels_found")
    # stub_sentinels_found: false means no sentinels found — gate passes
    return str(val).strip().lower() == "false"
```

**Modify `SPEC_FIDELITY_GATE`**: Add the five new `SemanticCheck` entries to `semantic_checks`:

```python
SPEC_FIDELITY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "high_severity_count",
        "medium_severity_count",
        "low_severity_count",
        "total_deviations",
        "validation_complete",
        "tasklist_ready",
        # NEW: deterministic inventory fields
        "fr_ids_coverage_complete",
        "module_deps_present",
        "dispatch_tables_preserved",
        "pseudocode_dispatch_preserved",
        "stub_sentinels_found",
    ],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="high_severity_count_zero",
            check_fn=_high_severity_count_zero,
            failure_message="high_severity_count must be 0 for spec-fidelity gate to pass",
        ),
        SemanticCheck(
            name="tasklist_ready_consistent",
            check_fn=_tasklist_ready_consistent,
            failure_message="tasklist_ready is inconsistent with severity counts or validation_complete",
        ),
        # NEW: deterministic checks
        SemanticCheck(
            name="fr_ids_coverage_complete",
            check_fn=_fr_ids_coverage_complete,
            failure_message=(
                "One or more FR-NNN/NFR-NNN/SC-NNN identifiers from the spec are absent "
                "from the roadmap. Check fr_ids_missing in frontmatter for details."
            ),
        ),
        SemanticCheck(
            name="module_deps_present",
            check_fn=_module_deps_present,
            failure_message=(
                "One or more module dependency edges declared in the spec are not "
                "reflected in the roadmap. Check module_deps_missing in frontmatter."
            ),
        ),
        SemanticCheck(
            name="dispatch_tables_preserved",
            check_fn=_dispatch_tables_preserved,
            failure_message=(
                "One or more named dispatch tables from the spec are absent from the "
                "roadmap. Check dispatch_tables_missing in frontmatter for details."
            ),
        ),
        SemanticCheck(
            name="pseudocode_dispatch_preserved",
            check_fn=_pseudocode_dispatch_preserved,
            failure_message=(
                "One or more dispatch function names from spec pseudocode are absent "
                "from the roadmap. Check pseudocode_dispatch_missing in frontmatter."
            ),
        ),
        SemanticCheck(
            name="no_stub_sentinels",
            check_fn=_no_stub_sentinels,
            failure_message=(
                "Roadmap contains stub/mock/no-op sentinel language indicating a "
                "placeholder implementation. Check stub_sentinel_locations in frontmatter."
            ),
        ),
    ],
)
```

**New helper module**: `src/superclaude/cli/roadmap/fidelity_inventory.py`

This module contains the pure-Python parsing and cross-reference functions for all five checks. It has no subprocess imports, no LLM invocation, and no roadmap/sprint imports (consistent with `NFR-003` and `NFR-007` from `pipeline/gates.py`). It exposes:

```python
def run_deterministic_inventory(
    spec_text: str,
    roadmap_text: str,
) -> dict[str, object]:
    """
    Run all five deterministic inventory checks and return a dict of
    frontmatter-ready fields.

    Return shape:
    {
        "fr_ids_coverage_complete": bool,
        "fr_ids_missing": list[str],          # empty on pass
        "fr_ids_note": str | None,            # "no_identifiers_found_in_spec" if applicable
        "module_deps_present": bool,
        "module_deps_missing": list[str],     # empty on pass
        "dispatch_tables_preserved": bool,
        "dispatch_tables_missing": list[str], # empty on pass
        "pseudocode_dispatch_preserved": bool,
        "pseudocode_dispatch_missing": list[str],
        "stub_sentinels_found": bool,
        "stub_sentinel_locations": list[str], # "line N: <matched text>"
    }
    """
```

#### `src/superclaude/cli/roadmap/prompts.py`

**Modify `build_spec_fidelity_prompt()`**: Add a section that explicitly requires the LLM to account for the deterministic inventory results. The prompt receives the inventory as a pre-computed input and must address each item.

The function signature extends to:

```python
def build_spec_fidelity_prompt(
    spec_file: Path,
    roadmap_path: Path,
    deterministic_inventory: dict[str, object] | None = None,
) -> str:
```

When `deterministic_inventory` is provided, inject a new section after the existing `## Comparison Dimensions` block:

```
## Deterministic Inventory Pre-Check Results

The following items were extracted programmatically from the spec and checked
against the roadmap. You MUST address each item explicitly in your deviation report
and reflect the results in your frontmatter fields.

### Requirement Identifier Coverage
fr_ids_missing: {fr_ids_missing}
If non-empty, each missing identifier must appear as a HIGH severity deviation.

### Module Dependency Edges
module_deps_missing: {module_deps_missing}
If non-empty, each missing edge must appear as a HIGH severity deviation.

### Named Dispatch Tables
dispatch_tables_missing: {dispatch_tables_missing}
If non-empty, each missing table must appear as a HIGH severity deviation.

### Pseudocode Dispatch Functions
pseudocode_dispatch_missing: {pseudocode_dispatch_missing}
If non-empty, each missing function name must appear as a HIGH severity deviation.

### Stub Sentinel Language
stub_sentinels_found: {stub_sentinels_found}
stub_sentinel_locations: {stub_sentinel_locations}
If stub_sentinels_found is true, each location must appear as a HIGH severity deviation.
```

**Modify output requirements block**: Add the five new frontmatter fields to the output specification.

#### `src/superclaude/cli/roadmap/executor.py` (or equivalent step runner)

The step that invokes `build_spec_fidelity_prompt()` must be modified to:

1. Call `run_deterministic_inventory(spec_text, roadmap_text)` before constructing the prompt.
2. Pass the inventory dict to `build_spec_fidelity_prompt()`.
3. After receiving the LLM's output, merge the inventory dict fields into the frontmatter if the LLM omitted them (fail-closed: if LLM omits a required deterministic field, inject `false` for boolean fields).

The step runner for `spec-fidelity` lives in the roadmap pipeline executor. The exact location depends on how the roadmap pipeline invokes Claude — this implementation step requires reading the roadmap pipeline executor to identify the call site.

### 4.2 New Test File

`tests/roadmap/test_fidelity_inventory.py`

Tests for all five parsing functions and the `run_deterministic_inventory` integration function:

- `test_extract_requirement_ids_standard_format` — FR-001, NFR-002, SC-003 extracted correctly
- `test_extract_requirement_ids_empty_spec` — empty spec returns empty set, check passes vacuously
- `test_extract_module_deps_arrow_variants` — `-->`, `──>`, `->` all parsed
- `test_extract_dispatch_tables_programmatic_runners` — `PROGRAMMATIC_RUNNERS = {` extracted
- `test_extract_dispatch_tables_no_false_positives` — `ERROR_CODE = 42` not extracted
- `test_extract_pseudocode_dispatch_three_way` — `_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step` all extracted from the v2.25 spec pseudocode
- `test_stub_sentinel_detection_mocked_steps` — "mocked steps" triggers D-05
- `test_stub_sentinel_detection_no_op_default` — "no-op default" triggers D-05
- `test_stub_sentinel_clean_roadmap` — roadmap with no sentinel language passes D-05
- `test_run_deterministic_inventory_cli_portify_case` — uses the actual v2.25 spec extraction and the actual cli-portify roadmap; verifies D-03, D-04, and D-05 all return failures

---

## 5. Acceptance Criteria

### 5.1 Would These Checks Have Caught the cli-portify Roadmap Reduction?

**Yes. Specifically:**

| Check | Would Have Triggered | Evidence |
|---|---|---|
| D-01 (FR-NNN coverage) | Likely, if the spec used FR-NNN notation | v2.24/v2.25 spec sections use SC-NNN success criteria notation; forensic report references `test_programmatic_step_routing` as a specified integration test — if coded as `SC-NNN` it would have been caught |
| D-02 (module deps) | **Yes, definitively** | `executor.py ──> steps/validate_config.py` appears in the v2.24 spec (Section 4 of forensic report). Neither `steps/validate_config.py` nor `steps/discover_components.py` appears anywhere in the roadmap. D-02 would have produced `module_deps_present: false` |
| D-03 (dispatch tables) | **Yes, definitively** | `PROGRAMMATIC_RUNNERS` appears in the v2.24 spec. It appears zero times in any roadmap (forensic report Section 5). D-03 would have produced `dispatch_tables_preserved: false` |
| D-04 (pseudocode dispatch) | **Yes, definitively** | `_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step` appear in v2.25 spec's explicit pseudocode block (forensic report Section 4). None appear in any roadmap. D-04 would have produced `pseudocode_dispatch_preserved: false` |
| D-05 (stub sentinels) | **Yes, definitively** | Roadmap Milestone M2 text: *"Sequential pipeline runs end-to-end with mocked steps"* — `mocked steps` matches D-05 pattern. D-05 would have produced `stub_sentinels_found: true` |

At minimum, D-03, D-04, and D-05 would have triggered on the first roadmap generation for v2.24. The gate would have failed, the pipeline would have halted, and the "mocked steps" reduction would have required explicit remediation before the roadmap could be used as a tasklist input.

### 5.2 Formal Acceptance Criteria for This Proposal

**AC-01**: `run_deterministic_inventory()` called with the v2.25 spec text and the v2.25 cli-portify roadmap returns `dispatch_tables_preserved: false`, `pseudocode_dispatch_preserved: false`, and `stub_sentinels_found: true`.

**AC-02**: `SPEC_FIDELITY_GATE` rejects a fidelity report that has `dispatch_tables_preserved: false` even when `high_severity_count: 0` (the LLM-only gate would have passed).

**AC-03**: `SPEC_FIDELITY_GATE` rejects a fidelity report that is missing any of the five new required frontmatter fields.

**AC-04**: `run_deterministic_inventory()` called with a spec that contains no `FR-NNN` identifiers returns `fr_ids_coverage_complete: true` with `fr_ids_note: "no_identifiers_found_in_spec"` (vacuous pass, no false block).

**AC-05**: `build_spec_fidelity_prompt()` with a non-empty deterministic inventory includes the inventory section in its output, and the inventory section explicitly names each missing item.

**AC-06**: All tests in `tests/roadmap/test_fidelity_inventory.py` pass, including `test_run_deterministic_inventory_cli_portify_case`.

**AC-07**: `make verify-sync` passes after implementation (src/superclaude/ and .claude/ in sync).

---

## 6. Risk Assessment

### 6.1 False Positives from Over-Aggressive Dispatch Table Matching (D-03)

**Risk**: The `UPPER_CASE_DICT = {` pattern combined with the suffix keyword heuristic may match names that are not dispatch tables. Examples: `ERROR_HANDLERS` (an error message map), `LOG_LEVEL_MAP` (configuration), `VALID_COMMANDS` (an allowlist). If such a name appears in the spec but not in the roadmap, D-03 blocks.

**Likelihood**: Medium. All-caps dictionary names with `_RUNNER`, `_REGISTRY`, `_DISPATCH`, `_MAP`, `_HANDLER` suffixes are common in spec documents for describing architectural components.

**Mitigation**:
1. The suffix keyword set in `_DISPATCH_CONTEXT_KEYWORDS` should be narrow. Do not include generic suffixes like `_MAP` or `_SET`. Prefer `runner`, `runners`, `dispatch`, `registry`, `route`, `routes`.
2. Add an opt-out annotation: specs may include `<!-- fidelity-inventory: ignore DICT_NAME -->` comments to exclude specific names. The parser recognizes this annotation and removes the name from the inventory.
3. In the first release of this feature, set the false-positive behavior to produce a MEDIUM severity deterministic finding rather than a HIGH. Escalate to HIGH in a subsequent release after calibrating against real spec corpus.

**Alternative**: Require explicit tagging in spec documents: `<!-- dispatch-table: PROGRAMMATIC_RUNNERS -->`. This eliminates false positives entirely but requires spec authors to annotate. Given that the existing spec corpus is not annotated, this would reduce initial catch rate. Recommend tagging as a best-practice recommendation, not a requirement, for v1 of this feature.

### 6.2 Stub Sentinel False Positives in Test Strategy Sections (D-05)

**Risk**: Many roadmaps legitimately describe test strategies that use mocked dependencies. A roadmap that says "Unit tests will use mocked step implementations to isolate executor logic" should not trigger D-05. The pattern `mocked? steps?` would match this text.

**Likelihood**: High. Test strategy sections almost universally use the word "mocked."

**Mitigation**:
1. The D-05 check should exclude roadmap sections that contain a `## Test Strategy`, `## Testing`, or `## Unit Tests` heading. The section-scoped check parses headings and resets the scan context when entering a test section.
2. Additional context filter: the sentinel must appear within 200 characters of a milestone, deliverable, or acceptance criteria marker (e.g., `**M\d+`**, `**D-\d+`**, `acceptance criteria:`). Sentinels in non-milestone sections are downgraded to LOW.
3. The `no.op default` and `steps? (?:to be)? wired later` patterns are higher-confidence signals that do not commonly appear in test sections and should remain HIGH severity without section filtering.

### 6.3 Specs That Do Not Use FR-NNN Conventions (D-01)

**Risk**: Many specs in the project — especially early-stage or informal specs — do not use formal `FR-NNN` / `NFR-NNN` / `SC-NNN` identifier notation. For these specs, D-01 produces an empty inventory and passes vacuously. This is intentional behavior, but it means D-01 provides no protection for informal specs.

**Likelihood**: High that many specs lack formal IDs; certain for new feature specs that start informally.

**Mitigation**: This is an accepted limitation. D-01's value is high for specs that do use formal IDs (which the CLI tooling encourages via roadmap pipeline guidance). The empty-inventory vacuous pass is correct behavior. Document this limitation in the gate's failure message for `fr_ids_coverage_complete: true` with `fr_ids_note: "no_identifiers_found_in_spec"`.

**Future improvement**: If a spec extraction step is added that auto-generates `FR-NNN` identifiers for informal specs, D-01's catch rate would increase. This is out of scope for this proposal.

### 6.4 Parsing Brittleness for Arrow Syntax Variants (D-02)

**Risk**: The module dependency arrow pattern `_DEP_ARROW_PATTERN` covers `-->`, `──>`, `->`, and `imports` but may miss other conventions used in different spec authors' styles (e.g., `→`, `==>`, `calls into`).

**Likelihood**: Low to medium. The existing specs in the corpus use `──>` and `-->` consistently (per forensic report Section 4). New specs may introduce variations.

**Mitigation**: Add `→` (Unicode right arrow, U+2192) and `==>` to the pattern. Keep the pattern conservative — prefer false negatives (missing an edge) over false positives (flagging a non-existent edge). Add `calls` as a keyword synonym alongside `imports`.

### 6.5 LLM Output Non-Compliance with New Frontmatter Fields

**Risk**: The LLM generating the fidelity report may not include the five new required frontmatter fields in its output, causing the gate to fail on a frontmatter-field-missing error rather than a meaningful fidelity finding.

**Likelihood**: Medium. The prompt update makes these fields required, but LLMs can omit fields under token pressure or when the deterministic inventory provides no failures (all items present).

**Mitigation**: The step runner (Section 4.1) merges deterministic inventory results into the frontmatter after LLM generation. If the LLM omits a field but the inventory computed it, the merger supplies it. This ensures the gate always has values to check. If the merger itself fails (inventory could not be computed), the gate fails with a `system` failure class rather than a `policy` failure class, enabling appropriate retry semantics.

---

## 7. Estimated Effort

### 7.1 Phase Mapping

This proposal maps to the existing unified-audit-gating v1.2.1 phase plan (`unified-audit-gating-v1.2.1-release-spec.md`, Section 10.1).

| Phase | v1.2.1 Definition | Proposal 02 Work |
|---|---|---|
| Phase 0 | Design/policy lock | Approve D-01 through D-05 check definitions; approve false-positive mitigations; assign owner for `fidelity_inventory.py` |
| Phase 1 | Deterministic contracts + evaluator | Implement `fidelity_inventory.py`; add semantic check functions to `roadmap/gates.py`; extend `SPEC_FIDELITY_GATE` with new fields |
| Phase 2 | Runtime controls | Modify step runner to call inventory pre-pass and merge results; handle inventory computation failure as `system` failure class |
| Phase 3 | Sprint CLI integration | Modify `build_spec_fidelity_prompt()` to accept and embed inventory; update `required_frontmatter_fields` in gate definition |
| Phase 4 | Rollout + KPI gates | Calibrate false positive rate against existing spec corpus; tune sentinel section-scope filter; promote D-03 matching to HIGH after calibration |

### 7.2 Effort Estimate by Component

| Component | Estimated Effort | Notes |
|---|---|---|
| `fidelity_inventory.py` — all five parsing functions | 3–4 hours | Pure Python, regex-based, no external dependencies |
| `roadmap/gates.py` — new semantic check functions + SPEC_FIDELITY_GATE modification | 1–2 hours | Pattern-follows existing semantic check functions |
| `roadmap/prompts.py` — extend `build_spec_fidelity_prompt()` | 1 hour | Additive change to existing prompt construction |
| Step runner modification (inventory pre-pass + frontmatter merge) | 2–3 hours | Requires locating the spec-fidelity step invocation site in the roadmap executor |
| `tests/roadmap/test_fidelity_inventory.py` — 10 test cases | 3–4 hours | Includes cli-portify regression test using actual spec/roadmap artifacts |
| Calibration against existing spec corpus | 2–3 hours | Run against v2.24, v2.24.1, v2.25, v2.26 spec extractions and roadmaps; adjust thresholds |
| **Total** | **12–17 hours** | Fits within a single sprint cycle |

### 7.3 Dependencies

- Requires the roadmap pipeline executor's spec-fidelity step invocation to be accessible for modification (no architectural blocker identified).
- The cli-portify regression test (`test_run_deterministic_inventory_cli_portify_case`) requires the v2.25 spec extraction artifact and the v2.25 roadmap to be available as test fixtures. Both exist in `.dev/releases/complete/v2.25-cli-portify-cli/`.
- Does not depend on any other proposal in the unified-audit-gating v1.2.1 backlog — this proposal is independently implementable.

---

## Appendix A: cli-portify Incident Replay Walkthrough

This walkthrough shows the exact gate failure sequence that would have occurred under the hardened gate.

**Inputs**:
- Spec extraction: v2.25 spec, Section 6 "Executor Design" pseudocode block
- Roadmap: v2.25 cli-portify roadmap, Phase 2 Key Action 4 + Milestone M2

**Step 1 — Deterministic inventory pre-pass**:

```
extract_dispatch_tables(spec_text):
    Match: "PROGRAMMATIC_RUNNERS = {"
    → ["PROGRAMMATIC_RUNNERS"]

extract_dispatch_function_names(spec_text):
    Code fence found: three-way dispatch pseudocode
    Match: "step_result = _run_programmatic_step("
    Match: "step_result = _run_claude_step("
    → ["_run_programmatic_step", "_run_claude_step"]
    (Note: _run_convergence_step uses different assignment pattern, may vary)

extract_module_deps(spec_text):
    Match: "executor.py ──> steps/validate_config.py"
    Match: "executor.py ──> steps/discover_components.py"
    → [("executor.py", "steps/validate_config.py"),
       ("executor.py", "steps/discover_components.py"), ...]

extract_stub_sentinels(roadmap_text):
    Line 47: "Sequential pipeline runs end-to-end with mocked steps"
    → [(47, "mocked steps")]
```

**Step 2 — Cross-reference**:

```
"PROGRAMMATIC_RUNNERS" in roadmap_text → False → dispatch_tables_preserved: false
"_run_programmatic_step" in roadmap_text → False → pseudocode_dispatch_preserved: false
"steps/validate_config.py" in roadmap_text → False → module_deps_present: false
stub_sentinels_found: true (line 47)
```

**Step 3 — Prompt injection**: The LLM receives the inventory with four explicit failure items. Even if the LLM's semantic comparison misses these, the frontmatter merge step supplies the deterministic values.

**Step 4 — Gate enforcement**: `gate_passed()` evaluates the fidelity report. `dispatch_tables_preserved: false` causes `_dispatch_tables_preserved()` to return `False`. Gate returns `(False, "Semantic check 'dispatch_tables_preserved' failed: One or more named dispatch tables from the spec are absent from the roadmap.")`.

**Outcome**: Pipeline halts at the `spec-fidelity` step. The roadmap cannot proceed to tasklist generation. The "mocked steps" executor design is blocked before any tasklist decomposition occurs.

---

## Appendix B: Relationship to Other Proposals in This Backlog

This proposal addresses **Link 1** of the fidelity chain (Spec → Roadmap). A complementary proposal addressing **Link 2** (Roadmap → Tasklist) would apply the same D-01/D-02/D-03/D-04 inventory logic to the `TASKLIST_FIDELITY_GATE` in `src/superclaude/cli/tasklist/gates.py`, cross-referencing roadmap deliverable IDs (`D-NNNN`, `R-NNN`) against tasklist task text. That is out of scope for this proposal but shares the `fidelity_inventory.py` helper module, which is designed to be reusable across both gates.

The `scoring-framework.md` in this directory provides the evaluation axes against which this proposal should be scored. Under those axes:

- **Catch Rate (Axis 1)**: 9/10 — D-03, D-04, D-05 each independently catch the cli-portify failure; D-02 provides additional coverage.
- **Generalizability (Axis 2)**: 7/10 — The dispatch table and pseudocode checks are applicable to any spec that defines named dispatch structures. The stub sentinel check catches the "defined but not wired" pattern category identified in the forensic report (three additional instances: `DEVIATION_ANALYSIS_GATE`, `SprintGatePolicy`, `TrailingGateRunner`).
- **Implementation Complexity (Axis 3, inverted)**: 7/10 — Pure Python regex with no new dependencies. Moderate complexity from section-scope filtering for D-05.
- **False Positive Rate (Axis 4, inverted)**: 6/10 — D-03 and D-05 have known false positive risks (Section 6.1, 6.2) mitigated but not eliminated in v1.
- **Spec Format Independence (Axis 5)**: 8/10 — Empty-inventory vacuous passes handle specs without formal IDs. Arrow-pattern parsing handles most common syntaxes.
- **Determinism (Axis 6)**: 10/10 — All five checks are pure functions of string input with no LLM invocation. Same input always produces same output.
