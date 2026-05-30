# Research: Test Conventions
**Topic type:** Test & Verification
**Scope:** test_obligation_scanner.py + test_obligation_scanner_meta_context.py + e2e path
**Status:** Complete
**Date:** 2026-05-29
---

## 1. Test file layout

### File A: `tests/roadmap/test_obligation_scanner.py` (738 lines)

- **Module docstring** (lines 1-11): enumerates what the file covers (scaffold terms FR-MOD1.1, discharge FR-MOD1.3/1.5, exempt FR-MOD1.7, code-block demotion FR-MOD1.8, regression). Notes "All tests use real content fixtures, no mocks."
- **Imports** (lines 13-15): only `from superclaude.cli.roadmap.obligation_scanner import (scan_obligations,)`. No pytest import at module level. No textwrap.
- **Fixtures**: module-level **constant string fixtures** — not pytest fixtures. Five triple-quoted constants at lines 19-96:
  - `MULTI_MILESTONE_ROADMAP` (line 19)
  - `UNDISCHARGED_ROADMAP` (line 41)
  - `EXEMPT_ROADMAP` (line 55)
  - `CODE_BLOCK_ROADMAP` (line 66)
  - `CLI_PORTIFY_REGRESSION` (line 82)
- **No helper functions**.
- **Test class structure** — 14 test classes, ~50 test methods total:
  1. `TestScaffoldTermDetection` (line 99) — 13 methods, one per scaffold term.
  2. `TestDischargeMatching` (line 170) — 4 methods.
  3. `TestExemptComments` (line 202) — 3 methods.
  4. `TestCodeBlockSeverityDemotion` (line 228) — 3 methods.
  5. `TestObjectiveParagraphExemption` (line 260) — 4 methods.
  6. `TestCliPortifyRegression` (line 332) — 2 methods.
  7. `TestObligationReportProperties` (line 352) — 2 methods.
  8. `TestPhaseParsing` (line 367) — 3 methods.
  9. `TestScaffoldingDescriptiveUseNotDetected` (line 393) — 5 methods.
  10. `TestFieldLabelComponentExtraction` (line 471) — 3 methods.
  11. `TestFix1TailSectionTermination` (line 547) — 1 method.
  12. `TestFix3DescriptiveContext` (line 573) — 3 methods.
  13. `TestFix1Fix3RegressionPreservesTrueCatches` (line 672) — 1 method.
  14. `TestEndToEndMultiModelSwarmRoadmap` (line 698) — 1 method (the e2e).
- **Naming**: classes are `TestPascalCase` describing the behavior cluster; methods are `test_snake_case`. Layer- or fix-numbered features use `TestFix3DescriptiveContext` / `TestFix1TailSectionTermination` style — so a new Layer 5 cluster would be `TestFix5H3SubsectionContext` or `TestLayer5H3Subsection`.
- **Markers**: NONE. No `@pytest.mark.*` decorators used.
- **Skip pattern**: only the e2e test uses `pytest.skip` (line 719) when the roadmap fixture is missing.

### File B: `tests/roadmap/test_obligation_scanner_meta_context.py` (394 lines)

- **Module docstring** (lines 1-6): "Tests the 2-layer meta-context classification system: Layer 1 structural exemptions, Layer 2 negation/meta-context."
- **Imports** (lines 8-17): `from __future__ import annotations`, `import textwrap`, `import pytest`, and `from superclaude.cli.roadmap.obligation_scanner import (_is_meta_context, scan_obligations,)`.
- **Fixtures**: inline `textwrap.dedent("""...""")` literals per-test — no module-level constants.
- **No helper functions**.
- **Test class structure** — 6 classes:
  1. `TestLayer1InlineCode` (line 20) — 2 methods.
  2. `TestLayer1CompletedChecklist` (line 55) — 2 methods.
  3. `TestIsMetaContext` (line 90) — 1 parameterized method covering 16 cases (the **only** use of `@pytest.mark.parametrize` in either file).
  4. `TestMetaContextFalsePositiveSuppression` (line 140) — 4 methods.
  5. `TestExistingBehaviorPreserved` (line 211) — 3 methods (regression).
  6. `TestLayer3StructuralPatterns` (line 246) — 7 methods.
- **Naming**: `TestLayer{N}{Feature}` style for layer-scoped tests. `TestLayer3StructuralPatterns` is the closest mirror to the new Layer 5 — it groups behavior unique to one layer using `textwrap.dedent` per-test fixtures.
- **Markers**: only `@pytest.mark.parametrize` on `test_is_meta_context` (line 93). No custom pytest markers.

## 2. Fixture pattern

Two distinct styles, one per file:

**Style A — module-level constant strings** (test_obligation_scanner.py:19-96):
```python
MULTI_MILESTONE_ROADMAP = """\
## M1: Skeleton Implementation

Build the executor skeleton with **mocked steps** for initial testing.
...
"""
```
Used when fixtures are reused across many tests in the file.

**Style B — inline `textwrap.dedent` per-test** (test_obligation_scanner_meta_context.py:25-33):
```python
content = textwrap.dedent(
    """\
    ## Phase 1: Implementation
    - Build the auth module

    ## Phase 2: Verification
    - Remove all `placeholder` values from config
"""
)
report = scan_obligations(content)
```
Used when each test exercises a slightly different markdown shape.

**Feeding into scanner**: in BOTH files, the input is a Python `str` passed directly to `scan_obligations(content)`. There is no file-path fixture, no pytest fixture, no parameterized fixture (beyond the lone parametrize in `TestIsMetaContext`). The ONLY filesystem read is the e2e test at test_obligation_scanner.py:711-723, which uses `Path(".dev/releases/Current/MultiModelSwarm/roadmap.md").read_text()`.

## 3. Layer 4 tests (mirror target)

Layer 4 is exercised exclusively in **`TestFix3DescriptiveContext`** (test_obligation_scanner.py:573-669). Three methods:

| Method | Lines | Input shape | Assertion pattern |
|---|---|---|---|
| `test_fix3_dummy_value_remains_high` | 579-604 | M1 with `Inject a (dummy value) for the API key`; no descriptor noun present. | Filter `dummy_obs = [o for o in report.obligations if o.term.lower() == "dummy"]`; assert `dummy_obs` non-empty; `assert all(o.severity == "HIGH" for o in dummy_obs)`. |
| `test_fix3_stub_tested_mitigation_demoted` | 606-635 | M1 with H3 subsection `### Risk Assessment and Mitigation — M1` containing `Mitigated by stub-tested fallback`. | Filter `stub_obs = [o for o in report.obligations if o.term.lower().startswith("stub")]`; assert non-empty; `assert all(o.severity == "MEDIUM" for o in stub_obs)` with diagnostic message tuple `(o.term, o.severity, o.context)`. |
| `test_fix3_discharge_guard_preserves_obligation` | 637-669 | M1 with `outcome: stub needs replacement in M3` (both descriptor noun `outcome` AND discharge verb `replacement`). | Filter `stub_obs` AND `"M1" in o.phase`; then `high_obs = [o for o in stub_obs if o.severity == "HIGH"]`; assert `high_obs` non-empty (the discharge guard preserves HIGH). |

Additional Layer 4 coverage at:
- `test_obligation_scanner.py:418-443` (`test_descriptive_noun_context_not_detected`) — accepts both "dropped entirely OR demoted to MEDIUM" under Layer 4, with `assert report.undischarged_count == 0`.
- `test_obligation_scanner_meta_context.py:355-394` (`test_descriptive_prose_scaffolding_still_suppressed`) — covers the regression where descriptive prose stays MEDIUM via Layer 4.

**Layer attribution**: tests do NOT check WHICH layer demoted a finding. The `Obligation` dataclass (obligation_scanner.py:148-160) has fields `phase, term, component, context, line_number, severity, discharged, exempt, discharge_phase, discharge_context` — no `layer` field. Tests verify behavior (severity, count, discharge) and let the layer be inferred from the fixture text. **Implication for Layer 5 tests**: do NOT assert "Layer 5 fired"; assert the OUTCOME (severity == MEDIUM and/or undischarged_count == 0).

## 4. Canonical assertion patterns

Across both files, the canonical Layer-N test shape is:

**A. Filter by term**:
```python
scaffold_obs = [o for o in report.obligations if "scaffold" in o.term.lower()]
assert scaffold_obs, "Expected scaffold obligation to be detected"
```
(test_obligation_scanner_meta_context.py:263-264 — also recurs at lines 281-284, 301-302, 317-318, 335-336, 351-352, 378-379.)

**B. Severity assertion** (`all` or `any`):
```python
assert all(o.severity == "MEDIUM" for o in scaffold_obs)
```
or for the inverse:
```python
assert any(o.severity == "HIGH" for o in mock_obs)
```

**C. Gate assertion** (count-level):
```python
assert report.undischarged_count == 0
```
With diagnostic message when failure is informative:
```python
assert report.undischarged_count == 0, (
    f"Descriptive prose must not contribute to undischarged_count, "
    f"got: {report.undischarged_count}"
)
```
(test_obligation_scanner_meta_context.py:391-394.)

**D. Full canonical paste — `test_table_cell_imperative_scaffold_is_medium` (test_obligation_scanner_meta_context.py:249-265)**:
```python
def test_table_cell_imperative_scaffold_is_medium(self):
    """Scaffold as first word in table task cell -> MEDIUM."""
    content = textwrap.dedent(
        """\
        ## Phase 2: Create Artifacts
        | Sub-step | Task | Requirements |
        |----------|------|-------------|
        | 2.2.1 | Scaffold command file using template | FR-001 |

        ## Phase 3: Verify
        - Run validation checks
    """
    )
    report = scan_obligations(content)
    scaffold_obs = [o for o in report.obligations if "scaffold" in o.term.lower()]
    assert scaffold_obs, "Expected scaffold obligation to be detected"
    assert all(o.severity == "MEDIUM" for o in scaffold_obs)
```

**E. Phase scoping** (when test needs to constrain matches to a specific milestone):
```python
stub_obs = [
    o for o in report.obligations
    if o.term.lower().startswith("stub") and "M1" in o.phase
]
```
(test_obligation_scanner.py:657-662.)

## 5. Where Layer 5 tests should live

**Recommendation: add to `tests/roadmap/test_obligation_scanner.py` as a new class `TestLayer5H3SubsectionContext`** (or `TestFix5H3SubsectionDemotion` to mirror the Fix-numbered convention used by Fix 1 / Fix 3).

**Reasoning**:
1. Layer 4 lives in **`TestFix3DescriptiveContext`** in test_obligation_scanner.py (line 573), NOT in the meta-context file. The Fix-N naming convention is established there.
2. The Risk Assessment subsection demotion is the natural extension of `test_fix3_stub_tested_mitigation_demoted` (test_obligation_scanner.py:606-635), which **already uses an H3 `### Risk Assessment and Mitigation — M1` subsection** as its fixture. That test exists in test_obligation_scanner.py.
3. test_obligation_scanner_meta_context.py is scoped per its docstring to "2-layer meta-context classification (Layer 1, Layer 2)" — adding Layer 5 there breaks the docstring contract and the file's `TestLayer{N}` numbering would jump from 3 to 5.
4. test_obligation_scanner.py already hosts `TestFix1Fix3RegressionPreservesTrueCatches` (line 672) and `TestEndToEndMultiModelSwarmRoadmap` (line 698) — the new tests and any e2e tightening belong adjacent to these.

**Style for new tests**: either Style A (constants like `H3_RISK_ASSESSMENT_ROADMAP = """..."""`) or Style B (per-test `textwrap.dedent`). The Fix 3 tests at test_obligation_scanner.py:579-669 use plain triple-quoted strings inside each test (no `textwrap.dedent`). For consistency with Fix 3, the new Layer 5 tests should use **plain triple-quoted strings inline** (no `textwrap.dedent`, no module-level constants).

## 6. The 3 specific Layer 5 tests to propose

All three live in a new class `TestLayer5H3SubsectionContext` appended after `TestFix1Fix3RegressionPreservesTrueCatches` (test_obligation_scanner.py:696) and before the e2e class.

### Test 1: H3 subsection demotion happy-path
**Name**: `test_layer5_risk_assessment_h3_demotes_scaffold_to_medium`
**Fixture shape**: `## M1: Foundation` → some body → `### Risk Assessment Matrix` → a line containing a scaffold term (e.g., `stub`) → `## M2: ...`.
**Assertion plan** (canonical shape D): filter `stub_obs` by `o.term.lower().startswith("stub")`; `assert stub_obs`; `assert all(o.severity == "MEDIUM" for o in stub_obs)`; `assert report.undischarged_count == 0`.

### Test 2: H3 context resets at next H2 (no leakage)
**Name**: `test_layer5_h3_context_resets_at_next_h2_milestone`
**Fixture shape**: `## M1: Foundation` → `### Risk Assessment Matrix` → some scaffold-term line (demoted MEDIUM) → `## M2: Implementation` → a scaffold term in the M2 body (no H3 above it) → no later discharge.
**Assertion plan**: filter scaffold obligations for `o.phase` containing `M2`; assert at least one; `assert any(o.severity == "HIGH" for o in m2_obs)` (the M2 mention must NOT inherit the M1 H3 demotion); `assert report.undischarged_count >= 1`. Mirrors the Layer 4 inverse pattern at test_obligation_scanner.py:236-240 (`test_non_code_block_scaffold_is_high`).

### Test 3: Integration Points subsection demotion
**Name**: `test_layer5_integration_points_h3_demotes_scaffold_to_medium`
**Fixture shape**: `## M2: Core` → body → `### Integration Points` → bullet containing a scaffold term (e.g., `Mock the upstream service for integration testing`) → `## M3: Hardening` with no discharge.
**Assertion plan** (canonical shape D + phase scoping): filter `mock_obs` for `mock` in `o.term.lower()` AND `"M2" in o.phase`; assert non-empty; `assert all(o.severity == "MEDIUM" for o in mock_obs)`; `assert report.undischarged_count == 0`. (Other valid third tests would substitute `### Milestone Dependencies` or `### Open Questions` per spec.)

## 7. e2e re-verification path

The **standalone scanner has NO dedicated CLI subcommand**. Verification options, ranked from fastest to most thorough:

### Option A (RECOMMENDED for FP-count diff): one-shot Python via `uv run`
There is no shell wrapper — the canonical pattern is the e2e pytest test itself (test_obligation_scanner.py:710-738) or a `uv run python -c` invocation. The minimal FP-count command:

```bash
uv run python -c "
from pathlib import Path
from superclaude.cli.roadmap.obligation_scanner import scan_obligations
r = scan_obligations(Path('.dev/releases/Current/MultiModelSwarm/roadmap.md').read_text())
fp = [o for o in r.obligations if not o.discharged and not o.exempt and o.severity != 'MEDIUM']
print(f'undischarged_count={r.undischarged_count}  HIGH-undischarged={len(fp)}')
for o in fp:
    print(f'  L{o.line_number:>4}  {o.term:<12}  phase={o.phase:<30}  ctx={o.context[:80]}')
"
```

Output: stdout. The "FP count" is `r.undischarged_count` (which excludes MEDIUM/discharged/exempt — see the filter logic mirrored at test_obligation_scanner.py:727-731).

### Option B: full pipeline via `superclaude roadmap run`
The scanner is invoked end-to-end as Step 7 "anti-instinct" in the roadmap executor:
- Invocation: executor.py:985 calls `_run_anti_instinct_audit(spec_file, merge_file, step.output_file)`.
- Step definition: executor.py:2130-2138 — output goes to `<out>/anti-instinct-audit.md`.
- The audit writer (executor.py:734-810) emits YAML frontmatter with `undischarged_obligations: N` plus a markdown body listing each `Line {o.line_number}: {o.term} in {o.phase} ({o.component})` for every `not o.discharged and not o.exempt and o.severity != "MEDIUM"` obligation (executor.py:796-802).
- CLI command shape: `superclaude roadmap run <spec.md>` (full pipeline) — overkill for FP-count diff because it re-runs 7 LLM steps before the scanner.

### Option C: pytest e2e
```bash
uv run pytest tests/roadmap/test_obligation_scanner.py::TestEndToEndMultiModelSwarmRoadmap -v
```
Asserts the original 6 FP lines (`{311, 519, 529, 541, 553, 600}`) are not re-flagged (test_obligation_scanner.py:710-738). The test skips gracefully if the roadmap is missing (line 718-722). Does NOT assert `undischarged_count == 0` — it allows newly-surfaced in-milestone H3 findings (which is exactly what Layer 5 is meant to address, per the test's own docstring at lines 698-708).

### Before/after FP count comparison method
1. Capture baseline: run Option A on master / pre-Layer-5 HEAD; record `undischarged_count` and the per-line list.
2. Apply Layer 5 changes.
3. Re-run Option A; diff the per-line list.
4. Strengthen Option C: after Layer 5 lands, the docstring at test_obligation_scanner.py:698-708 (which currently documents 8 newly-surfaced findings) should be updated and the assertion may be tightened toward `undischarged_count == 0`.

**File:line citations for the e2e wiring**:
- Standalone e2e test: test_obligation_scanner.py:698-738.
- Scanner entry point: obligation_scanner.py:190 (`def scan_obligations(content: str) -> ObligationReport`).
- Pipeline integration: executor.py:734-810 (`_run_anti_instinct_audit`), executor.py:985 (call site), executor.py:2130-2138 (step config).
- Gate that consumes the report: gates.py:317-328 (`_no_undischarged_obligations`) and gates.py:1363-1365 (gate registration named `no_undischarged_obligations`).

## 8. Test fixture for the e2e roadmap

The MultiModelSwarm roadmap is referenced in code at **`tests/roadmap/test_obligation_scanner.py:715-717`**:
```python
roadmap_path = Path(
    ".dev/releases/Current/MultiModelSwarm/roadmap.md"
)
```
It is a relative path resolved against the pytest CWD (repo / worktree root). There is no `conftest.py` fixture, no `pytest.fixture`, no `tmp_path` indirection. The fallback is `pytest.skip(...)` at line 719 if the file is missing. No other test file in `tests/roadmap/` references this path (verified by the absence of `MultiModelSwarm` matches in the test file scan).

The conftest at `tests/roadmap/conftest.py` provides only an `audit_trail` session fixture; it does NOT provide any roadmap-content fixture.
