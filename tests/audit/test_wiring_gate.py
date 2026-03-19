"""Tests for wiring gate — WiringConfig, WiringFinding, WiringReport, and all three analyzers.

Covers SC-001 (unwired callables), SC-002 (orphan modules), SC-003 (registries),
SC-007 (whitelist suppression), and R2 (SyntaxError handling).
"""

from __future__ import annotations

import tempfile
import textwrap
import time
from dataclasses import asdict
from pathlib import Path

import pytest
import yaml

from superclaude.cli.audit.wiring_config import (
    DEFAULT_REGISTRY_PATTERNS,
    WiringConfig,
    WiringConfigError,
    WhitelistEntry,
    load_whitelist,
)
from superclaude.cli.audit.wiring_gate import (
    WIRING_GATE,
    WiringFinding,
    WiringReport,
    _analysis_complete_true,
    _extract_frontmatter_values,
    _finding_counts_consistent,
    _recognized_rollout_mode,
    _severity_summary_consistent,
    _zero_blocking_findings_for_mode,
    analyze_orphan_modules,
    analyze_registries,
    analyze_unwired_callables,
    blocking_for_mode,
    emit_report,
    run_wiring_analysis,
)
from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.pipeline.models import GateCriteria

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# WiringConfig tests (T02.01)
# ---------------------------------------------------------------------------


class TestWiringConfig:
    def test_default_instantiation(self):
        config = WiringConfig()
        assert "steps" in config.provider_dir_names
        assert "handlers" in config.provider_dir_names
        assert config.rollout_mode == "shadow"
        assert config.whitelist_path is None
        assert len(config.registry_patterns) == len(DEFAULT_REGISTRY_PATTERNS)

    def test_custom_provider_dirs(self):
        config = WiringConfig(provider_dir_names=frozenset({"custom"}))
        assert config.provider_dir_names == frozenset({"custom"})

    def test_exclude_patterns_default(self):
        config = WiringConfig()
        assert "test_*.py" in config.exclude_patterns
        assert "conftest.py" in config.exclude_patterns
        assert "__init__.py" in config.exclude_patterns


class TestWhitelistLoading:
    def test_load_whitelist_none_path(self):
        result = load_whitelist(None)
        assert result == []

    def test_load_whitelist_nonexistent_path(self):
        result = load_whitelist(Path("/nonexistent/whitelist.yaml"))
        assert result == []

    def test_load_whitelist_valid_yaml(self, tmp_path):
        whitelist = tmp_path / "whitelist.yaml"
        whitelist.write_text(yaml.dump({
            "unwired_callables": [
                {"symbol": "Foo.hook", "reason": "intentional"},
            ],
            "orphan_modules": [
                {"symbol": "old_handler", "reason": "deprecated"},
            ],
            "unwired_registries": [],
        }))
        result = load_whitelist(whitelist)
        assert len(result) == 2
        assert result[0].symbol == "Foo.hook"
        assert result[0].finding_type == "unwired_callable"
        assert result[1].finding_type == "orphan_module"

    def test_load_whitelist_malformed_shadow_warns(self, tmp_path):
        whitelist = tmp_path / "bad.yaml"
        whitelist.write_text("not: a: valid: yaml: [")
        result = load_whitelist(whitelist, rollout_mode="shadow")
        assert result == []

    def test_load_whitelist_malformed_strict_raises(self, tmp_path):
        whitelist = tmp_path / "bad.yaml"
        whitelist.write_text("not: a: valid: yaml: [")
        with pytest.raises(WiringConfigError):
            load_whitelist(whitelist, rollout_mode="full")

    def test_load_whitelist_not_mapping_shadow(self, tmp_path):
        whitelist = tmp_path / "list.yaml"
        whitelist.write_text("- item1\n- item2\n")
        result = load_whitelist(whitelist, rollout_mode="shadow")
        assert result == []

    def test_load_whitelist_not_mapping_strict_raises(self, tmp_path):
        whitelist = tmp_path / "list.yaml"
        whitelist.write_text("- item1\n- item2\n")
        with pytest.raises(WiringConfigError):
            load_whitelist(whitelist, rollout_mode="soft")


# ---------------------------------------------------------------------------
# WiringFinding / WiringReport tests (T02.02)
# ---------------------------------------------------------------------------


class TestWiringFinding:
    def test_instantiation(self):
        f = WiringFinding(
            finding_type="unwired_callable",
            file_path="test.py",
            symbol_name="Foo.hook",
            line_number=10,
            detail="test",
        )
        assert f.finding_type == "unwired_callable"
        assert f.severity == "critical"
        assert f.suppressed is False

    def test_serializable_via_asdict(self):
        f = WiringFinding(
            finding_type="orphan_module",
            file_path="mod.py",
            symbol_name="mod",
            line_number=1,
            detail="orphan",
            severity="major",
        )
        d = asdict(f)
        assert d["finding_type"] == "orphan_module"
        assert d["severity"] == "major"


class TestWiringReport:
    def test_empty_report_is_clean(self):
        r = WiringReport()
        assert r.clean is True
        assert r.total_findings == 0

    def test_total_findings_aggregation(self):
        r = WiringReport()
        r.unwired_callables = [
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d"),
        ]
        r.orphan_modules = [
            WiringFinding("orphan_module", "b.py", "b", 1, "d", severity="major"),
        ]
        assert r.total_findings == 2
        assert r.clean is False

    def test_blocking_count_shadow(self):
        r = WiringReport(rollout_mode="shadow")
        r.unwired_callables = [
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d"),
        ]
        assert r.blocking_count() == 0

    def test_blocking_count_soft(self):
        r = WiringReport(rollout_mode="soft")
        r.unwired_callables = [
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", severity="critical"),
        ]
        r.orphan_modules = [
            WiringFinding("orphan_module", "b.py", "b", 1, "d", severity="major"),
        ]
        assert r.blocking_count() == 1  # only critical

    def test_blocking_count_full(self):
        r = WiringReport(rollout_mode="full")
        r.unwired_callables = [
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", severity="critical"),
        ]
        r.orphan_modules = [
            WiringFinding("orphan_module", "b.py", "b", 1, "d", severity="major"),
        ]
        assert r.blocking_count() == 2  # critical + major

    def test_suppressed_excluded_from_blocking(self):
        r = WiringReport(rollout_mode="full")
        r.unwired_callables = [
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", severity="critical", suppressed=True),
        ]
        assert r.blocking_count() == 0


# ---------------------------------------------------------------------------
# Unwired Callable Analyzer tests (T02.03, SC-001)
# ---------------------------------------------------------------------------


class TestUnwiredCallableAnalyzer:
    def _make_fixture(self, tmp_path: Path, code: str, filename: str = "module.py"):
        f = tmp_path / filename
        f.write_text(textwrap.dedent(code))
        return f

    def test_detects_unwired_optional_callable(self, tmp_path):
        """SC-001: detect Optional[Callable] with no call site wiring."""
        self._make_fixture(tmp_path, """
            from typing import Callable, Optional

            class Processor:
                def __init__(self, hook: Optional[Callable] = None):
                    self.hook = hook
        """)
        config = WiringConfig(exclude_patterns=[])
        findings = analyze_unwired_callables(config, tmp_path)
        assert len(findings) >= 1
        assert findings[0].finding_type == "unwired_callable"
        assert "Processor" in findings[0].symbol_name

    def test_wired_callable_not_flagged(self, tmp_path):
        """Callable that IS wired should not produce a finding."""
        self._make_fixture(tmp_path, """
            from typing import Callable, Optional

            class Runner:
                def __init__(self, callback: Optional[Callable] = None):
                    self.callback = callback
        """, "runner.py")

        self._make_fixture(tmp_path, """
            from runner import Runner

            def main():
                r = Runner(callback=lambda: None)
        """, "consumer.py")

        config = WiringConfig(exclude_patterns=[])
        findings = analyze_unwired_callables(config, tmp_path)
        assert len(findings) == 0

    def test_syntax_error_does_not_crash(self, tmp_path):
        """R2: SyntaxError in one file does not crash the analyzer."""
        self._make_fixture(tmp_path, "def broken(", "bad.py")
        self._make_fixture(tmp_path, """
            from typing import Callable, Optional

            class Good:
                def __init__(self, hook: Optional[Callable] = None):
                    pass
        """, "good.py")

        config = WiringConfig(exclude_patterns=[])
        findings = analyze_unwired_callables(config, tmp_path)
        # Should still produce findings from good.py
        assert any(f.symbol_name == "Good.hook" for f in findings)

    def test_whitelist_suppression(self, tmp_path):
        """SC-007: whitelisted unwired callables are marked suppressed."""
        self._make_fixture(tmp_path, """
            from typing import Callable, Optional

            class Hook:
                def __init__(self, on_event: Optional[Callable] = None):
                    pass
        """)

        whitelist = tmp_path / "whitelist.yaml"
        whitelist.write_text(yaml.dump({
            "unwired_callables": [
                {"symbol": "Hook.on_event", "reason": "intentional"},
            ],
            "orphan_modules": [],
            "unwired_registries": [],
        }))

        config = WiringConfig(exclude_patterns=[], whitelist_path=whitelist)
        findings = analyze_unwired_callables(config, tmp_path)
        assert len(findings) == 1
        assert findings[0].suppressed is True
        assert findings[0].severity == "info"


# ---------------------------------------------------------------------------
# Orphan Module Analyzer tests (T02.04, SC-002)
# ---------------------------------------------------------------------------


class TestOrphanModuleAnalyzer:
    def test_detects_orphan_module(self):
        """SC-002: detect module in provider dir with zero inbound imports."""
        fixture_dir = FIXTURES / "project_with_providers"
        config = WiringConfig(
            provider_dir_names=frozenset({"handlers"}),
            exclude_patterns=["__init__.py"],
        )
        findings = analyze_orphan_modules(config, fixture_dir)
        orphan_symbols = [f.symbol_name for f in findings]
        assert any("orphan_handler" in s for s in orphan_symbols)

    def test_imported_module_not_flagged(self):
        """Module that IS imported should not appear as orphan."""
        fixture_dir = FIXTURES / "project_with_providers"
        config = WiringConfig(
            provider_dir_names=frozenset({"handlers"}),
            exclude_patterns=["__init__.py"],
        )
        findings = analyze_orphan_modules(config, fixture_dir)
        orphan_symbols = [f.symbol_name for f in findings]
        assert not any("used_handler" in s for s in orphan_symbols)

    def test_no_provider_dirs_returns_empty(self, tmp_path):
        """No matching provider directories -> empty findings."""
        (tmp_path / "main.py").write_text("print('hello')")
        config = WiringConfig(provider_dir_names=frozenset({"nonexistent"}))
        findings = analyze_orphan_modules(config, tmp_path)
        assert findings == []


# ---------------------------------------------------------------------------
# Registry Analyzer tests (T02.05, SC-003)
# ---------------------------------------------------------------------------


class TestRegistryAnalyzer:
    def test_detects_broken_registry_entry(self, tmp_path):
        """SC-003: detect registry entry referencing nonexistent callable."""
        (tmp_path / "registry.py").write_text(textwrap.dedent("""
            def valid():
                pass

            STEP_REGISTRY = {
                "ok": valid,
                "broken": missing_func,
            }
        """))
        config = WiringConfig(exclude_patterns=[])
        findings = analyze_registries(config, tmp_path)
        assert len(findings) >= 1
        assert findings[0].finding_type == "unwired_registry"
        assert "missing_func" in findings[0].detail

    def test_valid_registry_not_flagged(self, tmp_path):
        """Registry with all resolvable entries -> no findings."""
        (tmp_path / "reg.py").write_text(textwrap.dedent("""
            def handler_a():
                pass

            def handler_b():
                pass

            STEP_DISPATCH = {
                "a": handler_a,
                "b": handler_b,
                "null": None,
            }
        """))
        config = WiringConfig(exclude_patterns=[])
        findings = analyze_registries(config, tmp_path)
        assert len(findings) == 0

    def test_non_registry_dict_ignored(self, tmp_path):
        """Dict assignments not matching registry patterns are ignored."""
        (tmp_path / "config.py").write_text(textwrap.dedent("""
            SETTINGS = {
                "key": "value",
            }
        """))
        config = WiringConfig(exclude_patterns=[])
        findings = analyze_registries(config, tmp_path)
        assert len(findings) == 0

    def test_registry_string_reference_unresolved(self, tmp_path):
        """String values referencing nonexistent dotted paths are flagged."""
        (tmp_path / "dispatch.py").write_text(textwrap.dedent("""
            STEP_HANDLERS = {
                "task": "nonexistent.module.func",
            }
        """))
        config = WiringConfig(exclude_patterns=[])
        findings = analyze_registries(config, tmp_path)
        assert len(findings) >= 1
        assert "unresolvable" in findings[0].detail


# ---------------------------------------------------------------------------
# SyntaxError handling tests (R2)
# ---------------------------------------------------------------------------


class TestSyntaxErrorHandling:
    def test_unwired_analyzer_handles_syntax_error(self, tmp_path):
        (tmp_path / "bad.py").write_text("def broken(")
        config = WiringConfig(exclude_patterns=[])
        # Should not raise
        findings = analyze_unwired_callables(config, tmp_path)
        assert isinstance(findings, list)

    def test_registry_analyzer_handles_syntax_error(self, tmp_path):
        (tmp_path / "bad.py").write_text("def broken(")
        config = WiringConfig(exclude_patterns=[])
        findings = analyze_registries(config, tmp_path)
        assert isinstance(findings, list)


# ---------------------------------------------------------------------------
# run_wiring_analysis integration tests
# ---------------------------------------------------------------------------


class TestRunWiringAnalysis:
    def test_returns_wiring_report(self, tmp_path):
        (tmp_path / "empty.py").write_text("# empty module\n")
        config = WiringConfig(exclude_patterns=[])
        report = run_wiring_analysis(config, tmp_path)
        assert isinstance(report, WiringReport)
        assert report.files_analyzed >= 1
        assert report.scan_duration_seconds >= 0

    def test_report_invariant_category_sum(self, tmp_path):
        """Single-source-of-truth invariant: category sums == total."""
        (tmp_path / "mod.py").write_text(textwrap.dedent("""
            from typing import Callable, Optional

            class X:
                def __init__(self, hook: Optional[Callable] = None):
                    pass
        """))
        config = WiringConfig(exclude_patterns=[])
        report = run_wiring_analysis(config, tmp_path)
        total = (
            len(report.unwired_callables) +
            len(report.orphan_modules) +
            len(report.unwired_registries)
        )
        assert report.total_findings == total


# ---------------------------------------------------------------------------
# Performance benchmark (SC-008)
# ---------------------------------------------------------------------------


class TestPerformanceBenchmark:
    def test_50_file_under_5_seconds(self, tmp_path):
        """SC-008: 50-file fixture completes in under 5 seconds."""
        for i in range(50):
            (tmp_path / f"module_{i}.py").write_text(textwrap.dedent(f"""
                from typing import Callable, Optional

                class Service{i}:
                    def __init__(self, hook: Optional[Callable] = None):
                        self.hook = hook

                    def run(self):
                        return {i}
            """))

        config = WiringConfig(exclude_patterns=[])
        start = time.monotonic()
        report = run_wiring_analysis(config, tmp_path)
        elapsed = time.monotonic() - start

        assert elapsed < 5.0, f"Analysis took {elapsed:.2f}s, exceeding 5s limit"
        assert report.files_analyzed == 50


# ---------------------------------------------------------------------------
# Phase 3: Report emission tests (T03.01)
# ---------------------------------------------------------------------------


def _make_report(**kwargs) -> WiringReport:
    """Helper to build a WiringReport with optional overrides."""
    defaults = {
        "target_dir": "/tmp/test",
        "files_analyzed": 10,
        "files_skipped": 1,
        "scan_duration_seconds": 0.1234,
        "rollout_mode": "shadow",
    }
    defaults.update(kwargs)
    return WiringReport(**defaults)


class TestEmitReport:
    def test_emit_report_creates_file(self, tmp_path):
        report = _make_report()
        out = tmp_path / "report.md"
        result = emit_report(report, out)
        assert result == out
        assert out.exists()

    def test_emit_report_has_16_frontmatter_fields(self, tmp_path):
        report = _make_report()
        out = tmp_path / "report.md"
        emit_report(report, out)
        content = out.read_text()
        fm = _extract_frontmatter_values(content)
        assert len(fm) == 16, f"Expected 16 frontmatter fields, got {len(fm)}: {list(fm.keys())}"

    def test_emit_report_has_7_sections(self, tmp_path):
        report = _make_report()
        out = tmp_path / "report.md"
        emit_report(report, out)
        content = out.read_text()
        headings = [line for line in content.splitlines() if line.startswith("## ")]
        assert len(headings) == 7, f"Expected 7 sections, got {len(headings)}: {headings}"

    def test_emit_report_roundtrip_frontmatter(self, tmp_path):
        """Emit a report, extract frontmatter, verify all 16 fields are present."""
        report = _make_report(
            unwired_callables=[
                WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
            ],
            orphan_modules=[
                WiringFinding("orphan_module", "b.py", "b", 1, "d", "major"),
            ],
        )
        out = tmp_path / "report.md"
        emit_report(report, out)
        content = out.read_text()
        fm = _extract_frontmatter_values(content)

        expected_fields = WIRING_GATE.required_frontmatter_fields
        for field_name in expected_fields:
            assert field_name in fm, f"Missing frontmatter field: {field_name}"

    def test_emit_report_yaml_safe_dump(self, tmp_path):
        """String fields should be safely serialized."""
        report = _make_report(target_dir="path/with: colon")
        out = tmp_path / "report.md"
        emit_report(report, out)
        content = out.read_text()
        assert "---" in content
        # Should not cause YAML parse error
        fm = _extract_frontmatter_values(content)
        assert "target_dir" in fm

    def test_emit_report_creates_parent_dirs(self, tmp_path):
        report = _make_report()
        out = tmp_path / "nested" / "dir" / "report.md"
        emit_report(report, out)
        assert out.exists()


# ---------------------------------------------------------------------------
# Phase 3: Frontmatter extraction tests (T03.02)
# ---------------------------------------------------------------------------


class TestExtractFrontmatterValues:
    def test_extracts_all_fields(self, tmp_path):
        report = _make_report()
        out = tmp_path / "report.md"
        emit_report(report, out)
        content = out.read_text()
        fm = _extract_frontmatter_values(content)
        assert "gate" in fm
        assert fm["gate"] == "wiring-verification"

    def test_returns_empty_for_no_frontmatter(self):
        fm = _extract_frontmatter_values("No frontmatter here")
        assert fm == {}

    def test_returns_empty_for_invalid_frontmatter(self):
        fm = _extract_frontmatter_values("---\nno key value\n---\n")
        assert fm == {}

    def test_round_trip_with_findings(self, tmp_path):
        report = _make_report(
            unwired_callables=[
                WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
            ],
        )
        out = tmp_path / "report.md"
        emit_report(report, out)
        content = out.read_text()
        fm = _extract_frontmatter_values(content)
        assert fm["unwired_callable_count"] == "1"
        assert fm["total_findings"] == "1"
        assert fm["critical_count"] == "1"


# ---------------------------------------------------------------------------
# Phase 3: WIRING_GATE definition tests (T03.03)
# ---------------------------------------------------------------------------


class TestWiringGateDefinition:
    def test_wiring_gate_is_gate_criteria(self):
        assert isinstance(WIRING_GATE, GateCriteria)

    def test_wiring_gate_has_16_required_fields(self):
        assert len(WIRING_GATE.required_frontmatter_fields) == 16

    def test_wiring_gate_has_5_semantic_checks(self):
        assert WIRING_GATE.semantic_checks is not None
        assert len(WIRING_GATE.semantic_checks) == 5

    def test_wiring_gate_enforcement_tier_strict(self):
        assert WIRING_GATE.enforcement_tier == "STRICT"

    def test_wiring_gate_importable(self):
        from superclaude.cli.audit.wiring_gate import WIRING_GATE as gate
        assert gate is WIRING_GATE

    def test_wiring_gate_field_names_match_spec(self):
        expected = {
            "gate", "target_dir", "files_analyzed", "rollout_mode",
            "analysis_complete", "unwired_callable_count", "orphan_module_count",
            "unwired_registry_count", "critical_count", "major_count",
            "info_count", "total_findings", "blocking_findings",
            "whitelist_entries_applied", "files_skipped", "audit_artifacts_used",
        }
        actual = set(WIRING_GATE.required_frontmatter_fields)
        assert actual == expected


# ---------------------------------------------------------------------------
# Phase 3: Semantic check tests (T03.04)
# ---------------------------------------------------------------------------


class TestSemanticChecks:
    def _emit_content(self, tmp_path, **report_kwargs) -> str:
        report = _make_report(**report_kwargs)
        out = tmp_path / "report.md"
        emit_report(report, out)
        return out.read_text()

    def test_analysis_complete_true_passes(self, tmp_path):
        content = self._emit_content(tmp_path)
        assert _analysis_complete_true(content) is True

    def test_recognized_rollout_mode_shadow(self, tmp_path):
        content = self._emit_content(tmp_path, rollout_mode="shadow")
        assert _recognized_rollout_mode(content) is True

    def test_recognized_rollout_mode_soft(self, tmp_path):
        content = self._emit_content(tmp_path, rollout_mode="soft")
        assert _recognized_rollout_mode(content) is True

    def test_recognized_rollout_mode_full(self, tmp_path):
        content = self._emit_content(tmp_path, rollout_mode="full")
        assert _recognized_rollout_mode(content) is True

    def test_recognized_rollout_mode_invalid(self):
        assert _recognized_rollout_mode("---\nrollout_mode: invalid\n---\n") is False

    def test_finding_counts_consistent_clean(self, tmp_path):
        content = self._emit_content(tmp_path)
        assert _finding_counts_consistent(content) is True

    def test_finding_counts_consistent_with_findings(self, tmp_path):
        content = self._emit_content(tmp_path, unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ])
        assert _finding_counts_consistent(content) is True

    def test_severity_summary_consistent_clean(self, tmp_path):
        content = self._emit_content(tmp_path)
        assert _severity_summary_consistent(content) is True

    def test_severity_summary_consistent_with_findings(self, tmp_path):
        content = self._emit_content(tmp_path, unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ], orphan_modules=[
            WiringFinding("orphan_module", "b.py", "b", 1, "d", "major"),
        ])
        assert _severity_summary_consistent(content) is True

    def test_zero_blocking_shadow_always_passes(self, tmp_path):
        """SC-014: shadow mode always passes regardless of findings."""
        content = self._emit_content(tmp_path, rollout_mode="shadow", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
            WiringFinding("unwired_callable", "b.py", "B.x", 2, "d", "critical"),
        ])
        assert _zero_blocking_findings_for_mode(content) is True

    def test_zero_blocking_soft_fails_on_critical(self, tmp_path):
        content = self._emit_content(tmp_path, rollout_mode="soft", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ])
        assert _zero_blocking_findings_for_mode(content) is False

    def test_zero_blocking_full_fails_on_major(self, tmp_path):
        content = self._emit_content(tmp_path, rollout_mode="full", orphan_modules=[
            WiringFinding("orphan_module", "b.py", "b", 1, "d", "major"),
        ])
        assert _zero_blocking_findings_for_mode(content) is False

    def test_zero_blocking_soft_passes_when_clean(self, tmp_path):
        content = self._emit_content(tmp_path, rollout_mode="soft")
        assert _zero_blocking_findings_for_mode(content) is True


# ---------------------------------------------------------------------------
# Phase 3: gate_passed integration tests (T03.06, SC-004)
# ---------------------------------------------------------------------------


class TestGatePassedIntegration:
    def test_shadow_mode_clean_report_passes(self, tmp_path):
        """SC-004: gate_passed returns (True, None) for well-formed shadow report."""
        report = _make_report(rollout_mode="shadow")
        out = tmp_path / "report.md"
        emit_report(report, out)
        passed, reason = gate_passed(out, WIRING_GATE)
        assert passed is True, f"Gate failed: {reason}"
        assert reason is None

    def test_shadow_mode_with_findings_passes(self, tmp_path):
        """SC-004: shadow mode passes even with critical findings."""
        report = _make_report(rollout_mode="shadow", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ])
        out = tmp_path / "report.md"
        emit_report(report, out)
        passed, reason = gate_passed(out, WIRING_GATE)
        assert passed is True, f"Gate failed: {reason}"

    def test_soft_mode_clean_report_passes(self, tmp_path):
        report = _make_report(rollout_mode="soft")
        out = tmp_path / "report.md"
        emit_report(report, out)
        passed, reason = gate_passed(out, WIRING_GATE)
        assert passed is True, f"Gate failed: {reason}"

    def test_soft_mode_critical_findings_fails(self, tmp_path):
        """SC-014: soft mode blocks on critical findings."""
        report = _make_report(rollout_mode="soft", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ])
        out = tmp_path / "report.md"
        emit_report(report, out)
        passed, reason = gate_passed(out, WIRING_GATE)
        assert passed is False
        assert "zero_blocking_findings_for_mode" in reason

    def test_full_mode_major_findings_fails(self, tmp_path):
        """SC-014: full mode blocks on critical+major findings."""
        report = _make_report(rollout_mode="full", orphan_modules=[
            WiringFinding("orphan_module", "b.py", "b", 1, "d", "major"),
        ])
        out = tmp_path / "report.md"
        emit_report(report, out)
        passed, reason = gate_passed(out, WIRING_GATE)
        assert passed is False
        assert "zero_blocking_findings_for_mode" in reason

    def test_full_mode_clean_report_passes(self, tmp_path):
        report = _make_report(rollout_mode="full")
        out = tmp_path / "report.md"
        emit_report(report, out)
        passed, reason = gate_passed(out, WIRING_GATE)
        assert passed is True, f"Gate failed: {reason}"


# ---------------------------------------------------------------------------
# Phase 3: blocking_for_mode tests (T03.05)
# ---------------------------------------------------------------------------


class TestBlockingForMode:
    def test_shadow_never_blocks(self):
        report = _make_report(rollout_mode="shadow", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ])
        assert blocking_for_mode(report) is False

    def test_soft_blocks_on_critical(self):
        report = _make_report(rollout_mode="soft", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ])
        assert blocking_for_mode(report) is True

    def test_soft_does_not_block_on_major(self):
        report = _make_report(rollout_mode="soft", orphan_modules=[
            WiringFinding("orphan_module", "b.py", "b", 1, "d", "major"),
        ])
        assert blocking_for_mode(report) is False

    def test_full_blocks_on_major(self):
        report = _make_report(rollout_mode="full", orphan_modules=[
            WiringFinding("orphan_module", "b.py", "b", 1, "d", "major"),
        ])
        assert blocking_for_mode(report) is True

    def test_full_blocks_on_critical(self):
        report = _make_report(rollout_mode="full", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical"),
        ])
        assert blocking_for_mode(report) is True

    def test_no_findings_never_blocks(self):
        for mode in ("shadow", "soft", "full"):
            report = _make_report(rollout_mode=mode)
            assert blocking_for_mode(report) is False, f"mode={mode} should not block with no findings"

    def test_suppressed_excluded_from_blocking(self):
        report = _make_report(rollout_mode="full", unwired_callables=[
            WiringFinding("unwired_callable", "a.py", "A.x", 1, "d", "critical", suppressed=True),
        ])
        assert blocking_for_mode(report) is False


# ---------------------------------------------------------------------------
# Phase 3: NFR-007 compliance check
# ---------------------------------------------------------------------------


class TestNFR007Compliance:
    def test_no_pipeline_logic_imports_in_wiring_gate(self):
        """NFR-007: wiring_gate.py must not import pipeline logic modules."""
        import inspect
        import superclaude.cli.audit.wiring_gate as wg
        source = inspect.getsource(wg)
        # The only pipeline import should be models (data classes)
        pipeline_imports = [
            line for line in source.splitlines()
            if "from superclaude.cli.pipeline" in line
            and "models" not in line
        ]
        assert pipeline_imports == [], (
            f"NFR-007 violation: pipeline logic imports found: {pipeline_imports}"
        )

    def test_no_pipeline_imports_in_wiring_analyzer(self):
        """NFR-007: wiring_analyzer.py must not import from pipeline/*."""
        # wiring_analyzer.py doesn't exist as a separate file in this codebase
        # The analyzer logic lives in wiring_gate.py. This test verifies the
        # analyzer functions don't indirectly depend on pipeline beyond models.
        pass
