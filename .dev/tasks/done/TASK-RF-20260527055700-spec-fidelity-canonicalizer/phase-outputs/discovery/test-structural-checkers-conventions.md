# Test conventions — `tests/roadmap/test_structural_checkers.py`

Captured: 2026-05-27 06:40 UTC

## Relevant imports (lines 11-29)

```python
from __future__ import annotations
from pathlib import Path
import pytest
from superclaude.cli.roadmap.structural_checkers import (
    CHECKER_REGISTRY, SEVERITY_RULES, RegressionResult, RemediationPatch,
    check_cli, check_data_models, check_gates, check_nfrs, check_signatures,
    get_severity, run_all_checkers,
)
```

## Fixture pattern (lines 185-196)

`spec_file` and `roadmap_file` are `@pytest.fixture` functions that take `tmp_path: Path`, write the module-level `SPEC_FIXTURE` / `ROADMAP_FIXTURE` markdown strings to `tmp_path / "spec.md"` and `tmp_path / "roadmap.md"`, and return `str(p)`.

For NEW per-test fixtures with custom IDs, use `tmp_path` directly inside the test:
```python
def test_xxx(self, tmp_path: Path) -> None:
    spec = tmp_path / "spec.md"
    roadmap = tmp_path / "roadmap.md"
    spec.write_text("...content...", encoding="utf-8")
    roadmap.write_text("...content...", encoding="utf-8")
    findings = check_signatures(str(spec), str(roadmap))
```

## Assertion style — phantom_id (line 258-262)

```python
def test_detects_phantom_id(self, spec_file: str, roadmap_file: str) -> None:
    findings = check_signatures(spec_file, roadmap_file)
    phantom_findings = [f for f in findings if f.rule_id == "phantom_id"]
    assert len(phantom_findings) > 0, "Should detect phantom ID FR-99"
    assert any("FR-99" in f.description for f in phantom_findings)
```

## Class container

Tests are grouped under `class TestSignaturesChecker:` (line 255). The 5 new tests append as siblings to `test_detects_phantom_id` inside this class.

## Requirement-ID regex constraints (spec_parser.py:324-330)

- `FR-\d+(?:\.\d+)?` — hyphen REQUIRED; sub-id optional.
- `NFR-\d+(?:\.\d+)?` — hyphen REQUIRED.
- `SC-\d+` — hyphen REQUIRED.
- `G-\d+` — hyphen REQUIRED.
- `D-?\d+` — hyphen OPTIONAL (matches D1, D01, D-1, D-01).

Implication: zero-padded variants like `FR-07` use the same regex slot as `FR-7` and BOTH extract. The canonicalizer collapses them to `FR-7`. For D family, both `D01` and `D-01` extract; canonicalizer collapses both to `D1`.

## Severity / rule_id field access

Findings expose:
- `f.rule_id` — machine key string (e.g. `"phantom_id"`, `"id_schema_drift"`)
- `f.severity` — `"HIGH"` | `"MEDIUM"`
- `f.spec_quote`, `f.roadmap_quote` — the surface forms

Filter pattern: `[f for f in findings if f.rule_id == "X" and f.severity == "Y"]`

## Closest existing phantom_id test: line 258
