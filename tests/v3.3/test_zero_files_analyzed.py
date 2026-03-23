"""T03.05: Validate 0-files-analyzed on non-empty dir returns FAIL (FR-5.1, SC-10).

Calls real ``run_wiring_analysis()`` on a non-empty source directory whose
Python files are all excluded by config patterns, producing 0 files_analyzed.
Asserts the function returns a FAIL report with a descriptive ``failure_reason``.

Dependencies: T03.01 (0-files guard in wiring_gate.py)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.audit.wiring_gate import WiringReport, run_wiring_analysis
from superclaude.cli.audit.wiring_config import WiringConfig


class TestZeroFilesAnalyzedFail:
    """FR-5.1: 0 files analyzed on non-empty dir must return FAIL."""

    def test_zero_files_analyzed_returns_fail(
        self, tmp_path: Path, audit_trail
    ) -> None:
        """Non-empty source dir with all files excluded -> FAIL + failure_reason.

        Setup: create a directory with Python files whose names match the
        exclude patterns, so ``_collect_python_files()`` returns 0 files
        while ``source_dir.rglob('*.py')`` still finds them.

        Spec refs: FR-5.1, SC-10
        """
        audit_trail.start_timer()

        # Create non-empty source dir with Python files
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "test_example.py").write_text("def test_foo(): pass\n")
        (src_dir / "conftest.py").write_text("import pytest\n")
        (src_dir / "__init__.py").write_text("")

        # Configure to exclude all files present (test_*, conftest, __init__)
        config = WiringConfig(
            exclude_patterns=["test_*.py", "conftest.py", "__init__.py"],
        )

        # Act: run real wiring analysis
        report: WiringReport = run_wiring_analysis(config, src_dir)

        # Assert: FAIL with failure_reason
        assert report.files_analyzed == 0, (
            f"Expected 0 files_analyzed, got {report.files_analyzed}"
        )
        assert report.failure_reason, (
            "Expected non-empty failure_reason for 0-files-analyzed on non-empty dir"
        )
        assert "0 files analyzed" in report.failure_reason
        assert report.target_dir == str(src_dir)

        # Emit audit record
        audit_trail.record(
            test_id="test_zero_files_analyzed_returns_fail",
            spec_ref="FR-5.1, SC-10",
            assertion_type="behavioral",
            inputs={
                "source_dir": str(src_dir),
                "python_files_present": 3,
                "exclude_patterns": config.exclude_patterns,
            },
            observed={
                "files_analyzed": report.files_analyzed,
                "failure_reason": report.failure_reason,
            },
            expected={
                "files_analyzed": 0,
                "failure_reason_present": True,
            },
            verdict="PASS",
            evidence=(
                "run_wiring_analysis() returned FAIL with "
                f"failure_reason='{report.failure_reason}' "
                "when 0 files analyzed in non-empty directory"
            ),
        )
