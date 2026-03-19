---
artifact: wiring-verification-gate-v1.0-release-spec.md
plan_type: spec-refactoring
date: 2026-03-17
source: 5-agent adversarial debate + spec-panel review synthesis
total_changes: 14
sections_modified: 4.2.1, 4.3, 6.2, 6.3, 8, 9
sections_added: (none — all changes are additions within existing sections)
---

# Spec Refactoring Plan — Wiring Verification Gate v1.0

All changes are additions or replacements within the existing spec document.
Zero changes touch the gate infrastructure constraints (GateCriteria, SemanticCheck, gate_passed).
Changes are ordered by section for sequential application.

---

## Change 1 — Section 4.2.1: Replace algorithm step 2b with normalization algorithm

**Type**: REPLACE
**Priority**: High (was BC-1, reclassified advisory but still warranted before T02)
**Risk**: Low — text clarification only, no behavioral change to gate infrastructure

**Locate**: Section 4.2.1, under "Algorithm", step 2b:
```
b. Extract parameters where:
   - annotation contains "Callable" AND
   - default is None (ast.Constant(value=None))
```

**Replace with**:
```
b. Extract parameters where annotation references Callable with a None default:

   Normalize annotation to string:
     annotation_str = ast.unparse(param.annotation) if param.annotation else ""

   Match using word-boundary pattern (prevents false positives on names
   containing "Callable" as a substring, e.g., NotCallableType):
     callable_pattern = re.compile(
         r'\b(typing\.)?Callable\b|'
         r'\bcollections\.abc\.Callable\b'
     )

   Record as injectable if:
     callable_pattern.search(annotation_str)
     AND isinstance(param.default, ast.Constant)
     AND param.default.value is None

   Note: ast.unparse() handles all annotation forms correctly, including
   ast.Subscript nodes (Optional[Callable[...]]) and manually-quoted
   forward references ("Callable[...]") which render as quoted literals
   still matchable by the pattern above.
   Note: from __future__ import annotations does NOT change ast.parse()
   output — annotations remain AST nodes in all Python versions.
   No eval() is required or appropriate here.
```

---

## Change 2 — Section 4.2.1: Append Known Limitation note after algorithm block

**Type**: APPEND (after the algorithm block, before "Pattern matched" example)
**Priority**: High (NB-1 — prevents silent null result and corrupt Phase 1 baseline)
**Risk**: Low — documentation only

**Append after the algorithm description**:
```
**Known Limitation — Import Aliases and Re-exports (tracked for v1.1)**

The call-site search matches class names as they appear in the defining module.
Classes re-exported through __init__.py and consumed via aliases
(e.g., `from package import ClassName` where the package __init__.py
re-exports it) will not be resolved. This produces false positives for
re-exported classes.

Expected FPR contribution in codebases using package-level re-exports:
30–70% of unwired-callable findings in shadow mode may be re-export false
positives. Phase 2 thresholds must be calibrated against Phase 1 data with
this in mind (see Section 8 threshold calibration guidance).

Planned fix (v1.1): pre-pass alias map construction via ast.Import /
ast.ImportFrom traversal with __init__.py chain resolution (max 3 hops).
```

---

## Change 3 — Section 4.2.1: Replace whitelist mechanism description with schema + validation spec

**Type**: REPLACE
**Priority**: High (NB-2 — schema and audit visibility required before gate is useful)
**Risk**: Low — extends the whitelist specification without changing its behavior

**Locate**: Section 4.2.1, the whitelist mechanism paragraph:
```
**Whitelist mechanism**: A `wiring_whitelist.yaml` file can list intentionally-optional
callables (event hooks, logging callbacks) excluded from analysis.

```yaml
# wiring_whitelist.yaml
unwired_callables:
  - class: Pipeline
    param: on_complete
    reason: "Optional event hook, not a dependency"
```
```

**Replace with**:
```
**Whitelist mechanism**: A `wiring_whitelist.yaml` file can list intentionally-optional
callables (event hooks, logging callbacks) excluded from analysis.

**Schema**: each entry must conform to:

```yaml
# wiring_whitelist.yaml
unwired_callables:
  - symbol: "module.path.ClassName.param_name"  # required; dotted path
    reason: "string"                             # required; non-empty
```

The legacy `class` + `param` split form is accepted as equivalent to
`symbol: "ClassName.param"` and normalized on load.

**Validation behavior (Phase 1 — shadow mode)**:
- `load_wiring_config()` MUST validate each entry against the schema above.
- Entries missing `symbol` or `reason`, or with an empty `reason`, are MALFORMED.
  Malformed entries MUST be skipped with a WARNING:
    `WARNING: wiring_whitelist.yaml entry [N] malformed (missing: <field>), skipping.`
- `load_wiring_config()` MUST NOT raise `WiringConfigError` for malformed entries
  during Phase 1 shadow mode — the gate must continue running to preserve
  observation data.

**Phase 2 note**: `load_wiring_config()` will be updated to raise `WiringConfigError`
on any malformed entry before Phase 2 activation. Resolve all whitelist warnings
before Phase 2 cutover.
```

---

## Change 4 — Section 4.3: Append YAML serialization requirement

**Type**: APPEND (at end of Section 4.3, after the report format example)
**Priority**: Medium (BC-2 reclassified advisory — required before production stabilization)
**Risk**: Low — implementation guidance, does not alter report schema

**Append after the report format example block**:
```
**4.3.1 Frontmatter Serialization Requirements**

The `emit_report` function (T05) MUST serialize all string-valued frontmatter
fields using `yaml.safe_dump()` rather than f-string or `str.format()` interpolation.
This applies to: `target_dir`, `symbol_name`, `detail`.

Boolean and integer fields that are gate-evaluated (`analysis_complete`,
`unwired_count`, `orphan_count`, `registry_count`, `total_findings`) are
serialized as Python literals and are exempt from this requirement.

**Rationale**: f-string interpolation of filesystem paths and symbol names into
YAML produces malformed output when values contain YAML-special characters (`:`,
`|`, `{`, `}`, `[`, `]`). While these cannot appear in Python identifiers, they
can appear in `target_dir` values. Malformed frontmatter causes report parse
errors; defensively handled, these produce gate failures rather than bypasses,
but the failure mode is confusing and avoidable.

**Implementation pattern**:
```python
import yaml
metadata_str = {
    "target_dir": str(target_dir),
    "symbol_name": finding.symbol_name,
    "detail": finding.detail,
}
frontmatter_str = yaml.safe_dump(metadata_str, default_flow_style=False)
```

**4.3.2 Whitelist Audit Visibility in Frontmatter**

`emit_report()` MUST include the following field in YAML frontmatter:

```yaml
whitelist_entries_applied: 0   # integer; count of entries that suppressed ≥1 finding
```

This field is required regardless of whether a whitelist file is configured.
If no whitelist is configured or no entries matched, emit `whitelist_entries_applied: 0`.

**Rationale**: reviewers must be able to detect whitelist-based suppression from
the gate report alone, without diffing `wiring_whitelist.yaml` across commits.
```

---

## Change 5 — Section 4.4: Add `enforcement_mode` to WIRING_GATE required fields

**Type**: APPEND (within WIRING_GATE.required_frontmatter_fields list)
**Priority**: Low — consistency with report format (Section 4.3 already includes `enforcement_mode`)
**Risk**: Negligible

**Locate**: Section 4.4, `WIRING_GATE = GateCriteria(required_frontmatter_fields=[...])`

**Add to the list**:
```python
"enforcement_mode",
"whitelist_entries_applied",
```

These fields appear in every emitted report (Section 4.3) but are not in the gate's
required_frontmatter_fields list. Add them for consistency.

---

## Change 6 — Section 6.2: Augment WiringConfig documentation

**Type**: REPLACE (whitelist_path field docstring)
**Priority**: Medium (NB-2)
**Risk**: Low — documentation only

**Locate**: Section 6.2, `whitelist_path: Path | None = None`

**Replace with**:
```python
# Path to wiring_whitelist.yaml. Entries suppress gate findings for matched symbols.
# See Section 4.2.1 for entry schema and validation behavior.
# Count of applied entries is reported in gate output frontmatter (Section 4.3.2).
whitelist_path: Path | None = None
```

**Also locate**: `provider_dir_names` field and **append** after it:

```python
# IMPORTANT: provider_dir_names must be set to match the target repository's
# actual provider directory conventions before shadow mode activation.
# The default value {"steps", "handlers", "validators", "checks"} reflects
# common framework conventions and will produce zero orphan findings (a false
# clean result) in codebases using different naming (e.g., "audit/",
# "execution/", "pm_agent/"). This field is not optional for production deployments.
# See Section 8 pre-activation checklist.
provider_dir_names: frozenset[str] = frozenset({
    "steps", "handlers", "validators", "checks",
})
```

---

## Change 7 — Section 6.3: Add `whitelist_entries_applied` to Gate Contract table

**Type**: APPEND (new row in Frontmatter contract table)
**Priority**: Medium (NB-2 — consistency with Section 4.3.2)
**Risk**: Low

**Locate**: Section 6.3, Frontmatter contract table.

**Append row**:
```
| `whitelist_entries_applied` | int | >= 0; count of whitelist entries that suppressed findings |
```

---

## Change 8 — Section 7: Add R6 (convention mismatch) to Risk Assessment

**Type**: APPEND (new row in risk table)
**Priority**: Medium (NB-1 — W1.3 is an identified risk not in the original table)
**Risk**: Low — documentation only

**Locate**: Section 7, risk table. **Append new row**:

```
| R6: provider_dir_names mismatch with actual codebase | High | High | Pre-activation validation checklist (Section 8); zero-findings sanity check |
```

---

## Change 9 — Section 8: Add Phase 1 pre-activation checklist

**Type**: APPEND (at start of Phase 1 block, before current description)
**Priority**: High (NB-1 — prevents silent null results corrupting baseline)
**Risk**: Low — process documentation

**Locate**: Section 8, "### Phase 1: Shadow (this release)"

**Prepend before the bullet list**:
```
**Pre-activation checklist (blocking — shadow mode must not start until both pass):**

1. **Provider directory validation**: Confirm that at least one directory matching
   `provider_dir_names` exists in the target repository and contains at least one
   Python file. If zero matches are found, update `provider_dir_names` in
   `WiringConfig` before proceeding. A shadow run against a misconfigured
   `provider_dir_names` produces a silent null result indistinguishable from a
   genuinely clean codebase and corrupts baseline data.

2. **Zero-findings sanity check**: If the first shadow run produces zero findings
   across ALL analyzers on a repository with >50 Python files, treat this as a
   configuration error requiring investigation, not a passing result.
   Log `WARN: zero-findings-on-first-run` and halt baseline collection until
   the configuration is verified.
```

---

## Change 10 — Section 8: Add Phase 2 threshold calibration guidance

**Type**: APPEND (at end of Phase 2 block)
**Priority**: High (NB-1 — without this, Phase 2 thresholds will be set against noisy data)
**Risk**: Low — process documentation

**Locate**: Section 8, "### Phase 2: Soft (release +1, ...)"

**Append at end of Phase 2 block, before Phase 3**:
```
**Threshold calibration for known FPR sources**:

When setting Phase 2 activation thresholds from Phase 1 baseline data,
explicitly account for the following known false-positive sources:

| Source | Expected FPR contribution | v1.0 mitigation | Planned fix |
|---|---|---|---|
| Re-exported classes (import aliases) | 30–70% of unwired-callable findings | Raise Phase 2 unwired-callable threshold; document noise floor | v1.1 alias pre-pass |
| provider_dir_names misconfiguration | 100% of orphan-module findings (silent) | Pre-activation validation checklist (Section 8) | N/A — config |

**Decision rule**: Phase 2 MUST NOT be activated if Phase 1 unwired-callable
FPR cannot be separated from the re-export noise floor. Document the estimated
noise floor in the Phase 1 report. Set Phase 2 thresholds at
`measured_FPR + 2σ` above the noise floor estimate, not above zero.
```

---

## Change 11 — Section 9: Replace testing strategy with behavioral coverage specification

**Type**: REPLACE (full Section 9 content)
**Priority**: High (BC-3 — coverage categories must be in spec before T06)
**Risk**: Low — no behavioral change to gate; removes prescriptive TC numbers

**Replace Section 9 entirely with**:

```markdown
## 9. Testing Strategy

### 9.1 Coverage Requirements

The test suite shall validate the wiring analysis gate across two layers.

#### Unit Tests (minimum 14 tests, across 4 analyzer functions)

**analyze_unwired_callables** (minimum 4 tests):
- Positive: detects a callable parameter with `Optional[Callable] = None` that
  has zero call sites providing it — produces 1 `WiringFinding(unwired_callable)`
- Negative: same class, call site provides the parameter by keyword —
  produces 0 findings
- Whitelist: parameter matches a whitelist entry — produces 0 findings
- Parse error: source file with a Python syntax error — gate does not crash;
  logs a warning; `analysis_complete` field reflects degraded state
- **Out of scope** (dynamic dispatch exclusion, Section 2): alias-based
  injection and `**kwargs`-forwarded injection do not require test cases

**analyze_orphan_modules** (minimum 5 tests):
- Positive: function in a provider directory with zero importers —
  produces 1 `WiringFinding(orphan_module)`
- Negative (direct import): same function, explicitly imported by consumer —
  produces 0 findings
- Negative (`__init__.py` re-export): function re-exported via package
  `__init__.py` and consumed transitively — produces 0 findings
- Private function (`_name` prefix): excluded from analysis — produces 0 findings
- `conftest.py`: pytest infrastructure files excluded — produces 0 findings

**analyze_unwired_registries** (minimum 2 tests):
- Positive: registry entry whose value symbol cannot be resolved —
  produces 1 `WiringFinding(unwired_registry)`
- Negative: registry entry whose value symbol resolves correctly —
  produces 0 findings

**emit_report / gate** (minimum 3 tests):
- Findings present → `gate_passed()` returns `(False, reason)`; report
  frontmatter has non-zero count fields
- No findings → `gate_passed()` returns `(True, None)`; report frontmatter
  has all count fields == 0
- YAML-safe serialization: a report emitted when `target_dir` contains a
  YAML-special character (e.g., colon) and `symbol_name` contains a block
  indicator character must parse without `yaml.YAMLError`; `gate_passed()`
  must return the expected result based on finding counts

### 9.2 Integration Tests (minimum 2 tests)

**SC-010: cli-portify fixture integration**

A dedicated fixture module set shall exist under `tests/audit/fixtures/`.
The fixture must contain:
- A source file defining a class with a constructor parameter typed
  `Optional[Callable]` with a `None` default
- A second source file that instantiates that class without providing the
  callable parameter

Behavioral contract (non-negotiable): `run_wiring_analysis()` on the fixture
directory MUST produce exactly 1 `WiringFinding` of type `"unwired_callable"`
identifying the specific class and parameter. Zero findings or more than 1
finding constitutes test failure.

The fixture file structure, class names, parameter names, and module layout
are implementation decisions finalized at T06. Only the behavioral contract
above is fixed by this specification.

**SC-006: sprint shadow mode non-interference**

When the wiring gate executes in shadow mode within a sprint run, the following
must hold after gate execution regardless of gate outcome:
- Task status fields (state, assignee, priority) in the sprint manifest are
  unchanged
- No exception is propagated to the sprint runner
- A `logger.info(...)` or equivalent trace is emitted with finding count

### 9.3 Test Infrastructure

**Fixture directory**: `tests/audit/fixtures/` (existing in file manifest)
**Size budget**: 50–80 LOC total (unchanged)
**Coverage target**: ≥ 90% line coverage on `src/superclaude/cli/audit/wiring_gate.py`

All WiringFinding `finding_type` values ("unwired_callable", "orphan_module",
"unwired_registry") must appear in at least one test assertion.
Gate exit paths (pass and fail) must each appear in at least one test assertion.
```

---

## Change 12 — Section 10: Update SC-007 to reference whitelist schema

**Type**: MODIFY (SC-007 verification column)
**Priority**: Low — consistency with whitelist schema changes
**Risk**: Negligible

**Locate**: Section 10, row SC-007:
```
| SC-007 | Whitelist mechanism excludes intentional optionals | Unit test: `test_detect_unwired_callable_whitelist` |
```

**Replace Verification column with**:
```
Unit test: whitelist positive case (per Section 9.1 — whitelist test)
AND: `emit_report()` frontmatter includes `whitelist_entries_applied: 1`
```

---

## Change 13 — Section 10: Add SC-011 for zero-findings sanity check

**Type**: APPEND (new row in success criteria table)
**Priority**: Medium (NB-1 — W1.3 pre-activation validation)
**Risk**: Low

**Append to Section 10 table**:
```
| SC-011 | `provider_dir_names` pre-activation validation raises WARN when zero provider dirs found | Integration: first shadow run against unconfigured target emits `WARN: zero-findings-on-first-run` |
```

---

## Change 14 — Section 12 (Tasklist): Update T06 scope note

**Type**: APPEND (T06 row "Notes" or expand Deliverables column)
**Priority**: Low — process clarity
**Risk**: Negligible

**Locate**: Section 12, T06 row:
```
| T06 | Unit tests for T02-T04 + test fixtures | `tests/audit/test_wiring_gate.py`, `tests/audit/fixtures/` | T02, T03, T04 |
```

**Replace Deliverables with**:
```
`tests/audit/test_wiring_gate.py` (minimum 14 unit tests per Section 9.1),
`tests/audit/fixtures/` (SC-010 fixture structure per Section 9.2 behavioral contract)
```

---

## Summary

| Change | Section | Type | Priority | Source |
|--------|---------|------|----------|--------|
| 1 | 4.2.1 | Replace step 2b | High | BC-1 (improved) |
| 2 | 4.2.1 | Append limitation note | High | NB-1 (W1.2) |
| 3 | 4.2.1 | Replace whitelist description | High | NB-2 (schema) |
| 4 | 4.3 | Append serialization + audit fields | Medium | BC-2 + NB-2 |
| 5 | 4.4 | Append frontmatter fields | Low | Consistency |
| 6 | 6.2 | Augment WiringConfig docs | Medium | NB-1 (W1.3) + NB-2 |
| 7 | 6.3 | Append gate contract row | Medium | NB-2 |
| 8 | 7 | Append R6 risk | Medium | NB-1 (W1.3) |
| 9 | 8 | Add pre-activation checklist | High | NB-1 (W1.3) |
| 10 | 8 | Add Phase 2 threshold guidance | High | NB-1 (W1.2) |
| 11 | 9 | Replace with behavioral coverage spec | High | BC-3 |
| 12 | 10 | Update SC-007 | Low | NB-2 |
| 13 | 10 | Add SC-011 | Medium | NB-1 |
| 14 | 12 | Update T06 deliverables | Low | BC-3 |

**Total changes**: 14
**Blocking conditions resolved**: All 3 (BC-1, BC-2, BC-3) addressed with appropriately scoped text
**Non-blocking conditions resolved**: Both (NB-1, NB-2) with correct phasing
**Implementation risk**: None — all changes are spec text only; zero impact on gate infrastructure
**Recommended application order**: Changes 1–3 (Section 4.2.1) → Change 4 (4.3) → Change 5 (4.4) → Changes 6–7 (6.x) → Change 8 (7) → Changes 9–10 (8) → Change 11 (9) → Changes 12–13 (10) → Change 14 (12)
