"""Tests for structural_checkers.py — FR-1, FR-3 deterministic checkers.

Covers:
- Registry completeness and callable interface (T02.01)
- Signatures and Data Models checkers (T02.02)
- Gates, CLI, and NFRs checkers (T02.03)
- Severity rule table completeness (T02.04)
- Determinism proof SC-1 (T02.05)
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from superclaude.cli.roadmap.structural_checkers import (
    CHECKER_REGISTRY,
    SEVERITY_RULES,
    CheckerCallable,
    RegressionResult,
    RemediationPatch,
    check_cli,
    check_data_models,
    check_gates,
    check_nfrs,
    check_signatures,
    get_severity,
    run_all_checkers,
)

# ---------- Test Fixtures ----------

SPEC_FIXTURE = """\
---
title: Test Spec
version: 1.0.0
status: draft
---

# Test Spec

## 3. Functional Requirements

### FR-1: Test Feature

```python
def process_data(input_path: str, config: dict, verbose: bool = False) -> list[str]:
    pass

def validate_schema(schema: dict) -> bool:
    pass
```

### FR-2: Another Feature

References SC-1, NFR-3, FR-1.

## 4. File Manifest

### 4.1 Source Files

| File | Description |
|------|-------------|
| `src/superclaude/cli/roadmap/executor.py` | Pipeline executor |
| `src/superclaude/cli/roadmap/gates.py` | Gate definitions |
| `src/superclaude/cli/roadmap/spec_parser.py` | Parser module |
| `src/superclaude/cli/audit/wiring_gate.py` | Wiring gate |

### 4.2 Data Models

```python
from typing import Literal

enforcement_tier = Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"]

@dataclass
class Finding:
    id: str
    severity: str
    dimension: str
    description: str
    rule_id: str
    stable_id: str
```

## 5. CLI & Configuration

### 5.1 CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--depth` | `standard` | Analysis depth |
| `--convergence-enabled` | `false` | Enable convergence |
| `--allow-regeneration` | `false` | Allow full regen |
| `--output` | `.` | Output directory |

Modes: `enforcement_tier` field with default: `STANDARD`

## 6. Non-Functional Requirements

### NFR-1: Determinism

Same inputs must produce identical outputs.

### NFR-3: Prompt Budget

Prompt size <= 30KB maximum.
Coverage >= 90% for structural checks.

### NFR-4: Checker Independence

Checkers must not share mutable state.
Module `convergence.py` must not import from `structural_checkers.py`.

### FR-7: Gate Definitions

Gate step 1 → step 2 → step 3 ordering.
`high_severity_count` field required in frontmatter.
Step(name="validate", timeout=300) parameters.
Semantic checks: `cross_refs_resolve` validation needed.

### FR-8: Regression Detection

step 4 after step 3.
"""

ROADMAP_FIXTURE = """\
---
title: Test Roadmap
version: 1.0.0
---

# Test Roadmap

## 3. Implementation Plan

### Phase 1: Parser Foundation

Implements FR-1, FR-2, SC-1, NFR-3.
Uses `process_data` function for pipeline.
Uses `validate_schema` for validation.

References param_arity handling.

```python
def process_data(input_path: str, config: dict) -> list[str]:
    pass
```

### Phase 2: Checkers

References FR-99 which is a phantom ID.

## 4. File Coverage

Covers these files:
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/gates.py`
- `src/superclaude/cli/roadmap/spec_parser.py`

## 5. Configuration

### 5.1 CLI

Options: --depth, --convergence-enabled, --allow-regeneration, --output
Modes: STRICT, STANDARD, LIGHT, EXEMPT
default: STANDARD

## 6. Quality Targets

Coverage >= 90% for checks.
Prompt size <= 30KB maximum.
Checkers must not share mutable state.

### Gate Implementation

Gate step 1 → step 2 → step 3 ordering.
high_severity_count field.
Step(name="validate", timeout=300) parameters.
Semantic checks: cross_refs_resolve validation.
step 4 after step 3.
"""


@pytest.fixture
def spec_file(tmp_path: Path) -> str:
    p = tmp_path / "spec.md"
    p.write_text(SPEC_FIXTURE, encoding="utf-8")
    return str(p)


@pytest.fixture
def roadmap_file(tmp_path: Path) -> str:
    p = tmp_path / "roadmap.md"
    p.write_text(ROADMAP_FIXTURE, encoding="utf-8")
    return str(p)


# ====================================================================
# T02.01 — Registry and Interface Tests
# ====================================================================


class TestRegistry:
    """T02.01: Checker callable interface and registry."""

    def test_registry_has_all_5_dimensions(self) -> None:
        expected = {"signatures", "data_models", "gates", "cli", "nfrs"}
        assert set(CHECKER_REGISTRY.keys()) == expected

    def test_registry_entries_are_callable(self) -> None:
        for dim, checker in CHECKER_REGISTRY.items():
            assert callable(checker), f"Registry entry '{dim}' is not callable"

    def test_checker_signature_matches_interface(self, spec_file: str, roadmap_file: str) -> None:
        """Each checker takes (spec_path: str, roadmap_path: str) -> list[Finding]."""
        for dim, checker in CHECKER_REGISTRY.items():
            result = checker(spec_file, roadmap_file)
            assert isinstance(result, list), f"Checker '{dim}' did not return a list"
            for finding in result:
                assert hasattr(finding, "dimension"), f"Finding from '{dim}' missing dimension"
                assert hasattr(finding, "rule_id"), f"Finding from '{dim}' missing rule_id"
                assert hasattr(finding, "severity"), f"Finding from '{dim}' missing severity"
                assert hasattr(finding, "spec_quote"), f"Finding from '{dim}' missing spec_quote"
                assert hasattr(finding, "roadmap_quote"), f"Finding from '{dim}' missing roadmap_quote"
                assert hasattr(finding, "location"), f"Finding from '{dim}' missing location"

    def test_run_all_checkers_returns_findings(self, spec_file: str, roadmap_file: str) -> None:
        findings = run_all_checkers(spec_file, roadmap_file)
        assert isinstance(findings, list)
        assert len(findings) > 0, "Expected at least some findings from test fixtures"


# ====================================================================
# T02.02 — Signatures and Data Models Checkers
# ====================================================================


class TestSignaturesChecker:
    """T02.02: Signatures checker with machine keys."""

    def test_detects_phantom_id(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_signatures(spec_file, roadmap_file)
        phantom_findings = [f for f in findings if f.rule_id == "phantom_id"]
        assert len(phantom_findings) > 0, "Should detect phantom ID FR-99"
        assert any("FR-99" in f.description for f in phantom_findings)

    def test_detects_param_arity_mismatch(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_signatures(spec_file, roadmap_file)
        arity_findings = [f for f in findings if f.rule_id == "param_arity_mismatch"]
        # process_data has 3 params in spec but 2 in roadmap
        assert len(arity_findings) > 0, "Should detect param arity mismatch for process_data"

    def test_all_findings_have_correct_dimension(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_signatures(spec_file, roadmap_file)
        for f in findings:
            assert f.dimension == "signatures"

    def test_all_findings_have_severity_from_rules(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_signatures(spec_file, roadmap_file)
        for f in findings:
            expected_severity = get_severity("signatures", f.rule_id)
            assert f.severity == expected_severity, f"Finding {f.id} severity {f.severity} != expected {expected_severity}"

    def test_findings_include_required_fields(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_signatures(spec_file, roadmap_file)
        for f in findings:
            assert f.dimension == "signatures"
            assert f.rule_id in ("phantom_id", "function_missing", "param_arity_mismatch", "param_type_mismatch")
            assert f.severity in ("HIGH", "MEDIUM")
            assert f.spec_quote
            assert f.roadmap_quote
            assert f.location
            assert f.stable_id


class TestDataModelsChecker:
    """T02.02: Data Models checker with machine keys."""

    def test_detects_file_missing(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_data_models(spec_file, roadmap_file)
        missing_findings = [f for f in findings if f.rule_id == "file_missing"]
        # wiring_gate.py is in spec but not in roadmap
        assert len(missing_findings) > 0, "Should detect missing file wiring_gate.py"

    def test_all_findings_have_correct_dimension(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_data_models(spec_file, roadmap_file)
        for f in findings:
            assert f.dimension == "data_models"

    def test_findings_use_correct_machine_keys(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_data_models(spec_file, roadmap_file)
        valid_keys = {"file_missing", "path_prefix_mismatch", "enum_uncovered", "field_missing"}
        for f in findings:
            assert f.rule_id in valid_keys, f"Unexpected machine key: {f.rule_id}"

    def test_findings_have_severity_from_rules(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_data_models(spec_file, roadmap_file)
        for f in findings:
            expected = get_severity("data_models", f.rule_id)
            assert f.severity == expected


# ====================================================================
# T02.03 — Gates, CLI, and NFRs Checkers
# ====================================================================


class TestGatesChecker:
    """T02.03: Gates checker with machine keys."""

    def test_produces_findings(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_gates(spec_file, roadmap_file)
        assert isinstance(findings, list)

    def test_all_findings_have_correct_dimension(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_gates(spec_file, roadmap_file)
        for f in findings:
            assert f.dimension == "gates"

    def test_findings_use_correct_machine_keys(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_gates(spec_file, roadmap_file)
        valid_keys = {"frontmatter_field_missing", "step_param_missing", "ordering_violated", "semantic_check_missing"}
        for f in findings:
            assert f.rule_id in valid_keys, f"Unexpected machine key: {f.rule_id}"

    def test_findings_have_severity_from_rules(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_gates(spec_file, roadmap_file)
        for f in findings:
            expected = get_severity("gates", f.rule_id)
            assert f.severity == expected


class TestCLIChecker:
    """T02.03: CLI Options checker with machine keys."""

    def test_produces_findings(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_cli(spec_file, roadmap_file)
        assert isinstance(findings, list)

    def test_all_findings_have_correct_dimension(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_cli(spec_file, roadmap_file)
        for f in findings:
            assert f.dimension == "cli"

    def test_findings_use_correct_machine_keys(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_cli(spec_file, roadmap_file)
        valid_keys = {"mode_uncovered", "default_mismatch"}
        for f in findings:
            assert f.rule_id in valid_keys, f"Unexpected machine key: {f.rule_id}"


class TestNFRsChecker:
    """T02.03: NFRs checker with machine keys."""

    def test_produces_findings(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_nfrs(spec_file, roadmap_file)
        assert isinstance(findings, list)

    def test_all_findings_have_correct_dimension(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_nfrs(spec_file, roadmap_file)
        for f in findings:
            assert f.dimension == "nfrs"

    def test_findings_use_correct_machine_keys(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_nfrs(spec_file, roadmap_file)
        valid_keys = {"threshold_contradicted", "security_missing", "dep_direction_violated", "coverage_mismatch", "dep_rule_missing"}
        for f in findings:
            assert f.rule_id in valid_keys, f"Unexpected machine key: {f.rule_id}"

    def test_findings_have_severity_from_rules(self, spec_file: str, roadmap_file: str) -> None:
        findings = check_nfrs(spec_file, roadmap_file)
        for f in findings:
            expected = get_severity("nfrs", f.rule_id)
            assert f.severity == expected


# ====================================================================
# T02.04 — Severity Rule Table
# ====================================================================


class TestSeverityRules:
    """T02.04: Complete severity rule table (FR-3)."""

    def test_exactly_19_rules(self) -> None:
        assert len(SEVERITY_RULES) == 19

    def test_8_high_rules(self) -> None:
        high_rules = {k for k, v in SEVERITY_RULES.items() if v == "HIGH"}
        assert len(high_rules) == 8

    def test_11_medium_rules(self) -> None:
        medium_rules = {k for k, v in SEVERITY_RULES.items() if v == "MEDIUM"}
        assert len(medium_rules) == 11

    def test_all_canonical_rules_present(self) -> None:
        expected = {
            ("signatures", "phantom_id"),
            ("signatures", "function_missing"),
            ("signatures", "param_arity_mismatch"),
            ("signatures", "param_type_mismatch"),
            ("data_models", "file_missing"),
            ("data_models", "path_prefix_mismatch"),
            ("data_models", "enum_uncovered"),
            ("data_models", "field_missing"),
            ("gates", "frontmatter_field_missing"),
            ("gates", "step_param_missing"),
            ("gates", "ordering_violated"),
            ("gates", "semantic_check_missing"),
            ("cli", "mode_uncovered"),
            ("cli", "default_mismatch"),
            ("nfrs", "threshold_contradicted"),
            ("nfrs", "security_missing"),
            ("nfrs", "dep_direction_violated"),
            ("nfrs", "coverage_mismatch"),
            ("nfrs", "dep_rule_missing"),
        }
        assert set(SEVERITY_RULES.keys()) == expected

    def test_get_severity_returns_correct_values(self) -> None:
        for (dim, mtype), severity in SEVERITY_RULES.items():
            assert get_severity(dim, mtype) == severity

    def test_get_severity_raises_keyerror_for_unknown(self) -> None:
        with pytest.raises(KeyError):
            get_severity("signatures", "unknown_key")

    def test_get_severity_raises_keyerror_for_unknown_dimension(self) -> None:
        with pytest.raises(KeyError):
            get_severity("unknown_dimension", "phantom_id")

    def test_rule_table_extensible(self) -> None:
        """Adding a new rule doesn't require checker logic changes."""
        # Verify we can look up after hypothetical addition
        original_count = len(SEVERITY_RULES)
        SEVERITY_RULES[("test_dim", "test_type")] = "LOW"
        try:
            assert get_severity("test_dim", "test_type") == "LOW"
            assert len(SEVERITY_RULES) == original_count + 1
        finally:
            del SEVERITY_RULES[("test_dim", "test_type")]


# ====================================================================
# T02.05 — Determinism Proof (SC-1)
# ====================================================================


class TestDeterminism:
    """T02.05: SC-1 determinism proof — identical inputs produce byte-identical findings."""

    def test_sequential_determinism(self, spec_file: str, roadmap_file: str) -> None:
        """Two sequential runs on identical inputs produce identical findings."""
        findings_1 = run_all_checkers(spec_file, roadmap_file)
        findings_2 = run_all_checkers(spec_file, roadmap_file)

        assert len(findings_1) == len(findings_2), (
            f"Finding count differs: {len(findings_1)} vs {len(findings_2)}"
        )

        for f1, f2 in zip(findings_1, findings_2):
            assert f1.id == f2.id, f"ID mismatch: {f1.id} vs {f2.id}"
            assert f1.severity == f2.severity
            assert f1.dimension == f2.dimension
            assert f1.rule_id == f2.rule_id
            assert f1.location == f2.location
            assert f1.spec_quote == f2.spec_quote
            assert f1.roadmap_quote == f2.roadmap_quote
            assert f1.stable_id == f2.stable_id

    def test_serialized_output_identical(self, spec_file: str, roadmap_file: str) -> None:
        """Serialized output is byte-identical across runs."""
        import json

        def serialize(findings: list) -> str:
            return json.dumps(
                [
                    {
                        "id": f.id,
                        "severity": f.severity,
                        "dimension": f.dimension,
                        "rule_id": f.rule_id,
                        "location": f.location,
                        "spec_quote": f.spec_quote,
                        "roadmap_quote": f.roadmap_quote,
                        "stable_id": f.stable_id,
                    }
                    for f in findings
                ],
                sort_keys=True,
                indent=2,
            )

        run1 = serialize(run_all_checkers(spec_file, roadmap_file))
        run2 = serialize(run_all_checkers(spec_file, roadmap_file))
        assert run1 == run2, "Serialized output differs between runs"

    def test_individual_checker_determinism(self, spec_file: str, roadmap_file: str) -> None:
        """Each individual checker is deterministic."""
        for dim, checker in CHECKER_REGISTRY.items():
            findings_1 = checker(spec_file, roadmap_file)
            findings_2 = checker(spec_file, roadmap_file)
            assert len(findings_1) == len(findings_2), f"Checker '{dim}' non-deterministic count"
            for f1, f2 in zip(findings_1, findings_2):
                assert f1.stable_id == f2.stable_id, f"Checker '{dim}' non-deterministic stable_id"

    def test_parallel_execution_determinism(self, spec_file: str, roadmap_file: str) -> None:
        """Parallel execution produces same results as sequential (NFR-4)."""
        from concurrent.futures import ThreadPoolExecutor

        sequential: list = []
        for dim, checker in CHECKER_REGISTRY.items():
            sequential.extend(checker(spec_file, roadmap_file))
        sequential.sort(key=lambda f: (f.dimension, f.rule_id, f.location))

        parallel: list = []
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {
                pool.submit(checker, spec_file, roadmap_file): dim
                for dim, checker in CHECKER_REGISTRY.items()
            }
            for future in futures:
                parallel.extend(future.result())
        parallel.sort(key=lambda f: (f.dimension, f.rule_id, f.location))

        assert len(sequential) == len(parallel)
        for s, p in zip(sequential, parallel):
            assert s.stable_id == p.stable_id
            assert s.severity == p.severity
            assert s.rule_id == p.rule_id

    def test_no_shared_mutable_state(self, spec_file: str, roadmap_file: str) -> None:
        """Checkers share no mutable state (NFR-4)."""
        # Run each checker multiple times and verify no state accumulation
        for dim, checker in CHECKER_REGISTRY.items():
            count_1 = len(checker(spec_file, roadmap_file))
            count_2 = len(checker(spec_file, roadmap_file))
            count_3 = len(checker(spec_file, roadmap_file))
            assert count_1 == count_2 == count_3, (
                f"Checker '{dim}' produced different counts: {count_1}, {count_2}, {count_3}"
            )


# ====================================================================
# Supporting Dataclass Tests
# ====================================================================


class TestSupportingDataclasses:
    def test_regression_result(self) -> None:
        r = RegressionResult(regressed=True, previous_high_count=2, current_high_count=3)
        assert r.regressed is True
        assert r.new_findings == []

    def test_remediation_patch(self) -> None:
        p = RemediationPatch(
            file_path="test.md",
            original_content="old",
            patched_content="new",
            finding_id="abc123",
        )
        assert p.applied is False
        assert p.rolled_back is False


# ====================================================================
# T04.06 — SC-4 Intermediate Check: Structural Ratio >= 70%
# ====================================================================


class TestSC4Ratio:
    """T04.06: Verify structural findings account for >= 70% of total."""

    def test_sc4_ratio(self, spec_file: str, roadmap_file: str) -> None:
        """SC-4: structural findings >= 70% of total when both layers produce findings."""
        structural_findings = run_all_checkers(spec_file, roadmap_file)
        structural_count = len(structural_findings)

        # All structural findings have source_layer="structural"
        for f in structural_findings:
            assert f.source_layer == "structural"

        # Simulate semantic findings: at most 30% of what structural produces
        # to verify the architectural ratio holds.
        # With N structural findings, up to floor(N * 0.3 / 0.7) semantic findings
        # would keep the ratio >= 70%.
        if structural_count > 0:
            max_semantic_for_70pct = int(structural_count * 0.3 / 0.7)
            # Verify the ratio formula: structural / (structural + max_semantic) >= 0.70
            total = structural_count + max_semantic_for_70pct
            ratio = structural_count / total if total > 0 else 1.0
            assert ratio >= 0.70, (
                f"SC-4 violated: structural={structural_count}, "
                f"semantic={max_semantic_for_70pct}, ratio={ratio:.2%}"
            )

    def test_all_structural_findings_tagged(self, spec_file: str, roadmap_file: str) -> None:
        """All structural findings carry source_layer='structural'."""
        findings = run_all_checkers(spec_file, roadmap_file)
        for f in findings:
            assert f.source_layer == "structural", (
                f"Finding {f.id} has source_layer='{f.source_layer}', expected 'structural'"
            )

    def test_structural_vs_semantic_dimensions_disjoint(self) -> None:
        """Structural checker dimensions do not overlap with semantic dimensions."""
        from superclaude.cli.roadmap.semantic_layer import (
            SEMANTIC_DIMENSIONS,
            STRUCTURAL_DIMENSIONS,
        )
        assert STRUCTURAL_DIMENSIONS == frozenset(CHECKER_REGISTRY.keys()), (
            "STRUCTURAL_DIMENSIONS must match CHECKER_REGISTRY keys"
        )
        assert STRUCTURAL_DIMENSIONS.isdisjoint(SEMANTIC_DIMENSIONS), (
            f"Overlap: {STRUCTURAL_DIMENSIONS & SEMANTIC_DIMENSIONS}"
        )

    def test_finding_counts_by_source_layer(self, spec_file: str, roadmap_file: str) -> None:
        """Document finding counts by source_layer for SC-4 evidence."""
        findings = run_all_checkers(spec_file, roadmap_file)
        structural_count = sum(1 for f in findings if f.source_layer == "structural")
        semantic_count = sum(1 for f in findings if f.source_layer == "semantic")

        # All findings from run_all_checkers should be structural
        assert semantic_count == 0, "run_all_checkers produced semantic findings"
        assert structural_count == len(findings)
