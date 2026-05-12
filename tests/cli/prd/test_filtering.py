"""Unit tests for superclaude.cli.prd.filtering.

Section 8.1 test plan: 4 tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.prd.filtering import (
    compile_gaps,
    load_synthesis_mapping,
    merge_qa_partition_reports,
    partition_files,
)


class TestPartitionFiles:
    """File list partitioning for parallel processing."""

    def test_partition_files_below_threshold(self) -> None:
        """Returns single partition when count <= threshold."""
        files = [Path(f"file-{i}.md") for i in range(4)]
        result = partition_files(files, 6)
        assert len(result) == 1
        assert result[0] == files

    def test_partition_files_at_threshold(self) -> None:
        files = [Path(f"file-{i}.md") for i in range(6)]
        result = partition_files(files, 6)
        assert len(result) == 1
        assert result[0] == files

    def test_partition_files_above_threshold(self) -> None:
        """Splits into correct partition count when above threshold."""
        files = [Path(f"file-{i}.md") for i in range(8)]
        result = partition_files(files, 6)
        assert len(result) == 2
        # All original items present
        flattened = [item for partition in result for item in partition]
        assert flattened == files

    def test_partition_files_empty(self) -> None:
        """Empty input returns empty result."""
        result = partition_files([], 6)
        assert result == []


class TestMergeQaPartitionReports:
    """QA report merging with pessimistic verdict strategy."""

    def test_merge_qa_partition_reports(self) -> None:
        """Merges reports; pessimistic verdict (FAIL if ANY FAIL)."""
        reports = [
            {"verdict": "PASS", "issues": []},
            {"verdict": "FAIL", "issues": ["Missing section 3"]},
            {"verdict": "PASS", "issues": []},
        ]
        merged = merge_qa_partition_reports(reports)

        assert merged["verdict"] == "FAIL"
        assert merged["partition_count"] == 3
        assert merged["partitions_passed"] == 2
        assert merged["partitions_failed"] == 1
        assert len(merged["issues"]) == 1

    def test_merge_qa_all_pass(self) -> None:
        reports = [
            {"verdict": "PASS", "issues": []},
            {"verdict": "PASS", "issues": []},
        ]
        merged = merge_qa_partition_reports(reports)
        assert merged["verdict"] == "PASS"
        assert merged["partitions_failed"] == 0

    def test_merge_qa_empty_reports(self) -> None:
        merged = merge_qa_partition_reports([])
        assert merged["verdict"] == "PASS"
        assert merged["partition_count"] == 0


class TestCompileGaps:
    """Gap extraction and deduplication from research files."""

    def test_compile_gaps(self, tmp_path: Path) -> None:
        """Extracts and deduplicates gaps from research files."""
        research_dir = tmp_path / "research"
        research_dir.mkdir()

        # File with explicit GAP markers
        (research_dir / "research-01.md").write_text(
            "# Research\n"
            "- GAP: Missing API documentation\n"
            "- Gap: No error handling spec\n"
        )

        # File with duplicate gap (should be deduplicated)
        (research_dir / "research-02.md").write_text(
            "# Research\n"
            "- GAP: Missing API documentation\n"
            "- GAP: No performance benchmarks\n"
        )

        gaps = compile_gaps(research_dir)

        # Should deduplicate "Missing API documentation"
        descriptions = [g["description"] for g in gaps]
        assert "Missing API documentation" in descriptions
        assert "No error handling spec" in descriptions
        assert "No performance benchmarks" in descriptions
        assert len(gaps) == 3  # 4 total - 1 duplicate = 3

    def test_compile_gaps_no_dir(self, tmp_path: Path) -> None:
        """Returns empty list when research dir doesn't exist."""
        assert compile_gaps(tmp_path / "nonexistent") == []


class TestLoadSynthesisMapping:
    """Synthesis mapping table loading."""

    def test_load_synthesis_mapping(self) -> None:
        """Returns exactly 9 entries with correct structure."""
        mapping = load_synthesis_mapping(Path("."))
        assert len(mapping) == 9

        # Verify structure of each entry
        for entry in mapping:
            assert "synth_file" in entry
            assert "sections" in entry
            assert "source_research" in entry
            assert entry["synth_file"].startswith("synth-")
            assert entry["synth_file"].endswith(".md")
            assert len(entry["sections"]) >= 1

        # Verify first and last entries
        assert mapping[0]["synth_file"] == "synth-01-exec-problem-vision.md"
        assert mapping[8]["synth_file"] == "synth-09-resources-maintenance.md"
