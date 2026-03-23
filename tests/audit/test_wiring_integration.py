"""Integration test: cli-portify fixture reproducing the step_runner=None no-op bug.

Validates SC-010 behavioral contract: analyze_unwired_callables() must detect
exactly 1 WiringFinding(unwired_callable) when a class declares an
Optional[Callable] constructor parameter with default None that is never wired.

This fixture models the original cli-portify defect pattern where
PortifyExecutor.__init__(step_runner: Optional[Callable] = None) was declared
but no call site ever passed step_runner=<something>.

Deliverable: D-0021
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from superclaude.cli.audit.wiring_config import WiringConfig
from superclaude.cli.audit.wiring_gate import (
    WiringFinding,
    analyze_unwired_callables,
    run_wiring_analysis,
)


@pytest.fixture
def cli_portify_fixture(tmp_path: Path) -> Path:
    """Create a minimal package reproducing the step_runner=None no-op bug.

    Structure:
        pkg/
            __init__.py
            executor.py   — declares step_runner: Optional[Callable] = None
            main.py       — instantiates Executor() WITHOUT passing step_runner
    """
    pkg = tmp_path / "pkg"
    pkg.mkdir()

    (pkg / "__init__.py").write_text("")

    (pkg / "executor.py").write_text(
        textwrap.dedent("""\
        from typing import Callable, Optional

        class PortifyExecutor:
            def __init__(
                self,
                workdir: str,
                step_runner: Optional[Callable] = None,
            ) -> None:
                self.workdir = workdir
                self._step_runner = step_runner

            def run(self) -> int:
                if self._step_runner is not None:
                    return self._step_runner()
                return 0
        """)
    )

    (pkg / "main.py").write_text(
        textwrap.dedent("""\
        from .executor import PortifyExecutor

        def main():
            # BUG: step_runner never wired — executor silently no-ops
            executor = PortifyExecutor("/tmp/work")
            return executor.run()
        """)
    )

    return pkg


class TestCliPortifyWiringIntegration:
    """SC-010: cli-portify fixture must produce exactly 1 unwired_callable finding."""

    def test_analyze_unwired_callables_detects_noop_bug(
        self, cli_portify_fixture: Path
    ):
        """analyze_unwired_callables returns exactly 1 finding for the fixture."""
        config = WiringConfig(
            exclude_patterns=["__init__.py"],
            rollout_mode="shadow",
        )

        findings = analyze_unwired_callables(config, cli_portify_fixture)

        # SC-010: exactly 1 finding
        assert len(findings) == 1, (
            f"Expected exactly 1 unwired_callable finding, got {len(findings)}: "
            f"{[f.symbol_name for f in findings]}"
        )

        finding = findings[0]
        assert finding.finding_type == "unwired_callable"
        assert "step_runner" in finding.symbol_name
        assert "PortifyExecutor" in finding.symbol_name
        assert finding.severity == "critical"
        assert "Optional[Callable]" in finding.detail or "never wired" in finding.detail

    def test_run_wiring_analysis_full_report(self, cli_portify_fixture: Path):
        """Full analysis pipeline produces report with exactly 1 unwired callable."""
        config = WiringConfig(
            exclude_patterns=["__init__.py"],
            rollout_mode="shadow",
        )

        report = run_wiring_analysis(config, cli_portify_fixture)

        # Report metadata
        assert report.files_analyzed >= 2  # executor.py + main.py
        assert report.target_dir == str(cli_portify_fixture)

        # Exactly 1 unwired callable
        assert len(report.unwired_callables) == 1
        assert report.unwired_callables[0].finding_type == "unwired_callable"
        assert "step_runner" in report.unwired_callables[0].symbol_name

        # Total findings includes only the unwired callable
        assert report.total_findings >= 1

    def test_finding_references_original_noop_pattern(
        self, cli_portify_fixture: Path
    ):
        """Finding detail references the specific unwired callable (step_runner)."""
        config = WiringConfig(
            exclude_patterns=["__init__.py"],
            rollout_mode="shadow",
        )

        findings = analyze_unwired_callables(config, cli_portify_fixture)
        assert len(findings) == 1

        finding = findings[0]
        # Must reference the specific symbol
        assert finding.symbol_name == "PortifyExecutor.step_runner"
        # Must reference the file containing the declaration
        assert "executor.py" in finding.file_path
        # Line number must be positive
        assert finding.line_number > 0

    def test_wiring_fixed_produces_zero_findings(self, tmp_path: Path):
        """When step_runner IS wired at a call site, zero findings produced."""
        pkg = tmp_path / "pkg_fixed"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")

        (pkg / "executor.py").write_text(
            textwrap.dedent("""\
            from typing import Callable, Optional

            class PortifyExecutor:
                def __init__(
                    self,
                    workdir: str,
                    step_runner: Optional[Callable] = None,
                ) -> None:
                    self.workdir = workdir
                    self._step_runner = step_runner
            """)
        )

        (pkg / "main.py").write_text(
            textwrap.dedent("""\
            from .executor import PortifyExecutor

            def _real_runner():
                return 42

            def main():
                # FIXED: step_runner properly wired
                executor = PortifyExecutor("/tmp/work", step_runner=_real_runner)
                return executor.run()
            """)
        )

        config = WiringConfig(
            exclude_patterns=["__init__.py"],
            rollout_mode="shadow",
        )

        findings = analyze_unwired_callables(config, pkg)
        assert len(findings) == 0, (
            f"Expected 0 findings when step_runner is wired, got {len(findings)}"
        )
