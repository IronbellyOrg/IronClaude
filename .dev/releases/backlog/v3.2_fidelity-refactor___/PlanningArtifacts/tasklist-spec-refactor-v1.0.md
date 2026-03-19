---
tasklist: wiring-gate-spec-refactor-v1.0
source_plan: adversarial/spec-refactoring-plan.md
source_spec: wiring-verification-gate-v1.0-release-spec.md
executor: sc:task-unified
compliance_tier: STANDARD
date: 2026-03-17
total_tasks: 14
dependencies_tracked: true
---

# Tasklist: Wiring Verification Gate v1.0 — Spec Refactoring

**Target file**: `.dev/releases/backlog/fidelity-refactor/wiring-verification-gate-v1.0-release-spec.md`
**All edits are text-only additions or replacements within the spec. Zero implementation code changes.**

---

## Phase A — Section 4.2.1 (Unwired Callable Analysis)
*3 tasks — all modify Section 4.2.1; must execute in order A1 → A2 → A3*

---

### TASK-A1 — Replace algorithm step 2b with normalization algorithm

**Maps to**: Refactoring Plan Change 1
**Section**: 4.2.1, Algorithm block, step 2b
**Type**: REPLACE
**Priority**: High

**Context**:
The current spec says "annotation contains 'Callable'" which is not a directly implementable algorithm. Replace with `ast.unparse()` canonicalization + word-boundary regex. Remove any mention of PEP 563 `eval()` (which is factually incorrect for `ast.parse()`-based analysis).

**Locate this text** in Section 4.2.1:
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

**Verification**: After edit, Section 4.2.1 algorithm step 2b must contain `ast.unparse`, `callable_pattern`, `\bCallable\b`, and must NOT contain "annotation contains" or "eval()".

**Deps**: none

---

### TASK-A2 — Append Known Limitation note (re-export FPR) after algorithm block

**Maps to**: Refactoring Plan Change 2
**Section**: 4.2.1, after algorithm block, before "Pattern matched" example
**Type**: APPEND
**Priority**: High

**Context**:
The call-site search is blind to classes re-exported via `__init__.py`. Without documenting this, Phase 1 shadow mode will produce cascading false positives with no explanation, poisoning the baseline data used for Phase 2 threshold-setting. The fix is v1.1 work; v1.0 needs the limitation documented with expected FPR range.

**Locate insertion point**: The line `**Pattern matched** (from forensic report):` in Section 4.2.1.

**Insert BEFORE that line**:
```
**Known Limitation — Import Aliases and Re-exports (tracked for v1.1)**

The call-site search matches class names as they appear in the defining module.
Classes re-exported through `__init__.py` and consumed via aliases
(e.g., `from package import ClassName` where the package `__init__.py`
re-exports it) will not be resolved. This produces false positives for
re-exported classes.

Expected FPR contribution in codebases using package-level re-exports:
30–70% of unwired-callable findings in shadow mode may be re-export false
positives. Phase 2 thresholds must be calibrated against Phase 1 data with
this in mind (see Section 8 threshold calibration guidance).

Planned fix (v1.1): pre-pass alias map construction via `ast.Import` /
`ast.ImportFrom` traversal with `__init__.py` chain resolution (max 3 hops).

```

**Verification**: After edit, the text "Known Limitation" and "30–70%" must appear in Section 4.2.1, before the "Pattern matched" heading.

**Deps**: TASK-A1 (same section — apply sequentially)

---

### TASK-A3 — Replace whitelist mechanism description with schema + validation spec

**Maps to**: Refactoring Plan Change 3
**Section**: 4.2.1, whitelist mechanism paragraph
**Type**: REPLACE
**Priority**: High

**Context**:
The current whitelist description allows any entry format with no validation. Replace with a formal schema (`symbol` + `reason` required), malformed-entry WARNING behavior (not hard failure in shadow mode), and a Phase 2 note about future strictness.

**Locate this entire block** in Section 4.2.1:
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

**Verification**: After edit, the old `class: Pipeline` example must be gone. The new text must contain `symbol:`, `MALFORMED`, `WiringConfigError`, and `Phase 2 note`.

**Deps**: TASK-A2 (same section — apply sequentially)

---

## Phase B — Sections 4.3 and 4.4 (Report Format + Gate Definition)
*2 tasks — independent of Phase A; can execute after A3 completes*

---

### TASK-B1 — Append YAML serialization requirements and whitelist audit field to Section 4.3

**Maps to**: Refactoring Plan Change 4
**Section**: 4.3, end of section (after the report format example block)
**Type**: APPEND
**Priority**: Medium

**Context**:
Two additions: (1) mandate `yaml.safe_dump()` for string metadata fields in `emit_report` to prevent malformed YAML from unusual path characters; (2) require `whitelist_entries_applied: N` in every emitted report frontmatter so whitelist suppression is visible to reviewers.

**Locate insertion point**: The end of Section 4.3, after the closing ```` ``` ```` of the report example block (the block ending with `Gate status: FAIL (enforcement: shadow -- logged only).`).

**Append after that block**:
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

**Verification**: After edit, Section 4.3 must contain `yaml.safe_dump()`, `4.3.1`, `4.3.2`, and `whitelist_entries_applied`.

**Deps**: TASK-A3 (logical; same spec file — work sequentially)

---

### TASK-B2 — Add `enforcement_mode` and `whitelist_entries_applied` to WIRING_GATE required fields

**Maps to**: Refactoring Plan Change 5
**Section**: 4.4, `WIRING_GATE = GateCriteria(required_frontmatter_fields=[...])`
**Type**: APPEND (within the list)
**Priority**: Low

**Context**:
Both fields are emitted in every report (Section 4.3) but absent from the gate's `required_frontmatter_fields`. This makes the gate unable to fail a report that omits them. Add for consistency.

**Locate this list** in Section 4.4:
```python
WIRING_GATE = GateCriteria(
    required_frontmatter_fields=[
        "gate",
        "target_dir",
        "files_analyzed",
        "unwired_count",
        "orphan_count",
        "registry_count",
        "total_findings",
        "analysis_complete",
    ],
```

**Replace the `required_frontmatter_fields` list** with:
```python
    required_frontmatter_fields=[
        "gate",
        "target_dir",
        "files_analyzed",
        "unwired_count",
        "orphan_count",
        "registry_count",
        "total_findings",
        "analysis_complete",
        "enforcement_mode",
        "whitelist_entries_applied",
    ],
```

**Verification**: After edit, `"enforcement_mode"` and `"whitelist_entries_applied"` must appear in the `required_frontmatter_fields` list in Section 4.4.

**Deps**: TASK-B1

---

## Phase C — Sections 6.2 and 6.3 (Interface Contracts)
*2 tasks — independent of Phase B; can execute in parallel with Phase B after Phase A*

---

### TASK-C1 — Augment WiringConfig documentation (provider_dir_names + whitelist_path)

**Maps to**: Refactoring Plan Change 6
**Section**: 6.2, WiringConfig dataclass documentation
**Type**: REPLACE + APPEND
**Priority**: Medium

**Context**:
Two sub-edits: (1) replace the `whitelist_path` comment to reference schema and audit visibility; (2) append a critical deployment warning to `provider_dir_names` explaining that the default frozenset will produce zero results on this codebase and must be configured before shadow mode.

**Sub-edit 1 — Replace `whitelist_path` comment**:

Locate:
```python
    # Whitelisted callables (intentionally optional)
    whitelist_path: Path | None = None
```

Replace with:
```python
    # Path to wiring_whitelist.yaml. Entries suppress gate findings for matched symbols.
    # See Section 4.2.1 for entry schema and validation behavior.
    # Count of applied entries is reported in gate output frontmatter (Section 4.3.2).
    whitelist_path: Path | None = None
```

**Sub-edit 2 — Replace `provider_dir_names` field block**:

Locate:
```python
    # Directories treated as "provider" directories for orphan analysis
    provider_dir_names: frozenset[str] = frozenset({
        "steps", "handlers", "validators", "checks",
    })
```

Replace with:
```python
    # Directories treated as "provider" directories for orphan analysis.
    # IMPORTANT: must be set to match the target repository's actual provider
    # directory conventions before shadow mode activation.
    # The default value {"steps", "handlers", "validators", "checks"} reflects
    # common framework conventions and will produce zero orphan findings (a false
    # clean result) in codebases using different naming (e.g., "audit/",
    # "execution/", "pm_agent/"). This field is not optional for production deployments.
    # See Section 8 pre-activation checklist.
    provider_dir_names: frozenset[str] = frozenset({
        "steps", "handlers", "validators", "checks",
    })
```

**Verification**: After edit, the `whitelist_path` comment must reference "Section 4.2.1" and "Section 4.3.2". The `provider_dir_names` comment must contain "IMPORTANT" and "pre-activation checklist".

**Deps**: TASK-A3 (references Section 4.2.1 and 4.3.2 which must exist first)

---

### TASK-C2 — Add `whitelist_entries_applied` row to Gate Contract table

**Maps to**: Refactoring Plan Change 7
**Section**: 6.3, Frontmatter contract table
**Type**: APPEND (new table row)
**Priority**: Medium

**Context**:
Section 6.3 defines the gate contract as a table. The new `whitelist_entries_applied` field added in TASK-B1 must appear here for completeness.

**Locate the table** in Section 6.3. It ends with:
```
| `analysis_complete` | bool | Must be true |
```

**Append after that last row**:
```
| `whitelist_entries_applied` | int | >= 0; count of whitelist entries that suppressed findings |
```

Note: `enforcement_mode` is already present in the Section 4.3 report format example but is NOT explicitly required by Change 7. Do not add it here — Change 5 (TASK-B2) covers the `required_frontmatter_fields` list; Change 7 covers only the gate contract table row for `whitelist_entries_applied`.

**Verification**: After edit, the `whitelist_entries_applied` row must exist in the Section 6.3 Frontmatter contract table.

**Deps**: TASK-B1, TASK-B2

---

## Phase D — Section 7 (Risk Assessment)
*1 task — independent; can run after Phase A*

---

### TASK-D1 — Add R6 (provider_dir_names convention mismatch) to Risk Assessment table

**Maps to**: Refactoring Plan Change 8
**Section**: 7, risk table
**Type**: APPEND (new table row)
**Priority**: Medium

**Context**:
The provider_dir_names mismatch risk (W1.3 from expert panel) is High/High — first shadow run against this codebase with default config produces silent zero findings. Not in original risk table.

**Locate the risk table** in Section 7. It ends with:
```
| R5: Naming convention heuristics miss new registry patterns | Medium | Low | Configurable `registry_patterns` regex; log when no registries found |
```

**Append after that row**:
```
| R6: `provider_dir_names` mismatch with actual codebase conventions | High | High | Pre-activation validation checklist (Section 8 Phase 1); zero-findings sanity check required on first run |
```

**Verification**: After edit, R6 must exist in the Section 7 risk table with likelihood "High" and impact "High".

**Deps**: none (independent)

---

## Phase E — Section 8 (Rollout Plan)
*2 tasks — E1 then E2 sequentially; can start after Phase A*

---

### TASK-E1 — Prepend Phase 1 pre-activation checklist to Section 8

**Maps to**: Refactoring Plan Change 9
**Section**: 8, Phase 1 block
**Type**: PREPEND (before existing Phase 1 bullet list)
**Priority**: High

**Context**:
Without provider directory validation before first run, zero findings look like a pass. Without a zero-findings sanity check, a misconfigured gate silently collects no data. Both checks must be in place before shadow mode starts.

**Locate** in Section 8:
```
### Phase 1: Shadow (this release)

- Wiring analysis runs after every task in sprint execution
```

**Insert BETWEEN** `### Phase 1: Shadow (this release)` and `- Wiring analysis runs...`:

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

**Verification**: After edit, the text "Pre-activation checklist" and "zero-findings-on-first-run" must appear in Section 8 Phase 1, before the first bullet point.

**Deps**: TASK-D1 (risk R6 references this checklist; logical ordering)

---

### TASK-E2 — Append Phase 2 threshold calibration guidance to Section 8

**Maps to**: Refactoring Plan Change 10
**Section**: 8, Phase 2 block (after existing content, before Phase 3 heading)
**Type**: APPEND
**Priority**: High

**Context**:
Phase 2 thresholds set from noisy Phase 1 data will be wrong. Without explicit guidance on accounting for the re-export noise floor (30–70% of unwired-callable FPR), Phase 2 may either never activate (threshold too loose) or block on false positives (threshold too strict).

**Locate** in Section 8:
```
### Phase 3: Full (release +2, pending soft data review)
```

**Insert BEFORE** that heading (i.e., at end of Phase 2 block):
```

**Threshold calibration for known FPR sources**:

When setting Phase 2 activation thresholds from Phase 1 baseline data,
explicitly account for the following known false-positive sources:

| Source | Expected FPR contribution | v1.0 mitigation | Planned fix |
|---|---|---|---|
| Re-exported classes (import aliases) | 30–70% of unwired-callable findings | Raise Phase 2 unwired-callable threshold; document noise floor | v1.1 alias pre-pass |
| `provider_dir_names` misconfiguration | 100% of orphan-module findings (silent) | Pre-activation validation checklist (Section 8 Phase 1) | N/A — config |

**Decision rule**: Phase 2 MUST NOT be activated if Phase 1 unwired-callable
FPR cannot be separated from the re-export noise floor. Document the estimated
noise floor in the Phase 1 report. Set Phase 2 thresholds at
`measured_FPR + 2σ` above the noise floor estimate, not above zero.

```

**Verification**: After edit, the text "Threshold calibration" and "measured_FPR + 2σ" must appear in Section 8, after Phase 2 content and before the Phase 3 heading.

**Deps**: TASK-E1

---

## Phase F — Section 9 (Testing Strategy)
*1 task — replace entire section; highest priority single change*

---

### TASK-F1 — Replace Section 9 with behavioral coverage specification

**Maps to**: Refactoring Plan Change 11
**Section**: 9 (entire section)
**Type**: REPLACE (full section)
**Priority**: High

**Context**:
The current Section 9 is a headcount ("11 unit tests") rather than a coverage specification. Replace with behavioral requirements organized by analyzer function. Remove TC-04 (alias) and TC-05 (kwargs) which are out-of-scope per Section 2's dynamic dispatch exclusion. Replace prescriptive SC-010 fixture source code with a behavioral contract (exact class names and file names are T06 implementation decisions, not spec decisions). Keep 14 unit + 2 integration structure.

**Locate** the section heading `## 9. Testing Strategy` through to `## 10. Success Criteria` (the next section heading).

**Replace everything between those headings** (exclusive of the headings themselves) with:

```markdown
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

All WiringFinding `finding_type` values (`"unwired_callable"`, `"orphan_module"`,
`"unwired_registry"`) must appear in at least one test assertion.
Gate exit paths (pass and fail) must each appear in at least one test assertion.
```

**Verification**: After edit, Section 9 must NOT contain "11 unit tests" or "test_detect_unwired_callable_basic". It MUST contain "minimum 14 tests", "Out of scope", "behavioral contract (non-negotiable)", and "9.3 Test Infrastructure".

**Deps**: TASK-A1 through TASK-A3 (references scope exclusions from Section 2 and algorithm from 4.2.1)

---

## Phase G — Section 10 (Success Criteria)
*2 tasks — G1 and G2; execute after Phase F*

---

### TASK-G1 — Update SC-007 verification to reference whitelist schema and audit field

**Maps to**: Refactoring Plan Change 12
**Section**: 10, SC-007 row
**Type**: MODIFY (Verification column only)
**Priority**: Low

**Context**:
SC-007's verification now needs to validate both whitelist suppression AND that `whitelist_entries_applied: 1` appears in the emitted report frontmatter.

**Locate this row** in Section 10:
```
| SC-007 | Whitelist mechanism excludes intentional optionals | Unit test: `test_detect_unwired_callable_whitelist` |
```

**Replace the entire row** with:
```
| SC-007 | Whitelist mechanism excludes intentional optionals and records suppression count | Unit test: whitelist positive case (per Section 9.1 — whitelist test); AND `emit_report()` frontmatter includes `whitelist_entries_applied: 1` |
```

**Verification**: After edit, SC-007 row must reference `whitelist_entries_applied: 1` in the Verification column.

**Deps**: TASK-F1, TASK-B1

---

### TASK-G2 — Add SC-011 (zero-findings sanity check) to success criteria table

**Maps to**: Refactoring Plan Change 13
**Section**: 10, success criteria table
**Type**: APPEND (new table row)
**Priority**: Medium

**Context**:
The pre-activation zero-findings sanity check (TASK-E1) needs a corresponding success criterion to be verifiable.

**Locate** the last row in the Section 10 table:
```
| SC-010 | Retrospective: would catch the cli-portify executor no-op bug | Run against actual `cli_portify/` directory |
```

**Append after that row**:
```
| SC-011 | `provider_dir_names` pre-activation validation emits `WARN: zero-findings-on-first-run` when zero provider dirs match | Integration: shadow run against target with no matching provider dirs emits warning and halts baseline collection |
```

**Verification**: After edit, the Section 10 table must contain an SC-011 row that includes both `zero-findings-on-first-run` and language describing an integration test that validates the warning is emitted when zero provider dirs match.

**Deps**: TASK-E1

---

## Phase H — Section 12 (Tasklist Index)
*1 task — final; execute last*

---

### TASK-H1 — Update T06 deliverables to reference Section 9.1/9.2 behavioral contracts

**Maps to**: Refactoring Plan Change 14
**Section**: 12, T06 row
**Type**: MODIFY (Deliverables column)
**Priority**: Low

**Context**:
T06's deliverables column currently lists raw file paths. After TASK-F1, these files are now governed by behavioral contracts in Section 9.1 and 9.2. Update the reference.

**Locate this row** in Section 12:
```
| T06 | Unit tests for T02-T04 + test fixtures | `tests/audit/test_wiring_gate.py`, `tests/audit/fixtures/` | T02, T03, T04 |
```

**Replace the Deliverables column** (third column) with:
```
`tests/audit/test_wiring_gate.py` (minimum 14 unit tests per Section 9.1), `tests/audit/fixtures/` (SC-010 fixture structure per Section 9.2 behavioral contract)
```

**Verification**: After edit, T06 row Deliverables must reference "Section 9.1" and "Section 9.2 behavioral contract".

**Deps**: TASK-F1

---

## Execution Order (Dependency Graph)

```
Phase A (sequential):
  TASK-A1 → TASK-A2 → TASK-A3

Phase B (after A3):
  TASK-A3 → TASK-B1 → TASK-B2

Phase C (after A3, parallel with B):
  TASK-A3 → TASK-C1
  TASK-B1 + TASK-B2 → TASK-C2

Phase D (independent, parallel with A):
  TASK-D1  (no deps)

Phase E (after D):
  TASK-D1 → TASK-E1 → TASK-E2

Phase F (after A1-A3):
  TASK-A3 → TASK-F1

Phase G (after F + B1):
  TASK-F1 + TASK-B1 → TASK-G1
  TASK-E1 → TASK-G2

Phase H (after F):
  TASK-F1 → TASK-H1
```

**Critical path**: A1 → A2 → A3 → B1 → B2 → C2 → G1 → H1
**Parallel track**: D1 → E1 → E2 → G2

---

## Completion Checklist

After all 14 tasks are applied, verify the following in the spec file:

- [ ] Section 4.2.1 step 2b: contains `ast.unparse`, `callable_pattern`, `\bCallable\b`; does NOT contain "annotation contains" or "eval()"
- [ ] Section 4.2.1: contains "Known Limitation" and "30–70%" before "Pattern matched"
- [ ] Section 4.2.1: whitelist schema shows `symbol:` field; contains `MALFORMED` and `WiringConfigError`
- [ ] Section 4.3: contains `4.3.1`, `yaml.safe_dump()`, `4.3.2`, `whitelist_entries_applied`
- [ ] Section 4.4: `required_frontmatter_fields` list contains `"enforcement_mode"` and `"whitelist_entries_applied"`
- [ ] Section 6.2: `whitelist_path` comment references Sections 4.2.1 and 4.3.2; `provider_dir_names` comment contains "IMPORTANT"
- [ ] Section 6.3: table contains `whitelist_entries_applied` row (Change 7 only; `enforcement_mode` row is NOT required here)
- [ ] Section 7: R6 row exists with High/High
- [ ] Section 8 Phase 1: "Pre-activation checklist" block present before first bullet
- [ ] Section 8 Phase 2: "Threshold calibration" table and "measured_FPR + 2σ" present before Phase 3
- [ ] Section 9: contains "minimum 14 tests", "Out of scope", "behavioral contract (non-negotiable)", "9.3 Test Infrastructure"; does NOT contain "11 unit tests"
- [ ] Section 10: SC-007 row Verification column references `whitelist_entries_applied: 1`
- [ ] Section 10: SC-011 row exists and contains `zero-findings-on-first-run`
- [ ] Section 12: T06 deliverables reference "Section 9.1" and "Section 9.2 behavioral contract"
