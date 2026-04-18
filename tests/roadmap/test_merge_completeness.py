"""Tests for `_validate_merge_completeness` — the tail-completeness gate.

The merge step writes the final roadmap section-by-section via tool calls.
If the LLM's turn budget is exhausted mid-sequence, the output file on
disk may be structurally incomplete even though it is non-empty. The
gate catches these cases so the pipeline retries merge instead of
silently accepting a truncated file.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.roadmap.executor import _validate_merge_completeness


def _complete_roadmap() -> str:
    return (
        "---\n"
        "schema_version: 1\n"
        "milestones: 2\n"
        "open_questions: 1\n"
        "---\n"
        "\n"
        "# Roadmap\n"
        "\n"
        "## Milestone Summary\n"
        "\n"
        "| ID | Title |\n"
        "|---|---|\n"
        "| M1 | Foundations |\n"
        "| M2 | Launch |\n"
        "\n"
        "## M1: Foundations\n"
        "\n"
        "| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| 1 | DM-001 | Schema | User schema | AUTH | - | ac | 2 | H |\n"
        "\n"
        "### Integration Points — M1\n"
        "- none\n"
        "\n"
        "### Milestone Dependencies — M1\n"
        "- none\n"
        "\n"
        "### Open Questions — M1\n"
        "\n"
        "| # | ID | Question | Impact | Owner | Target |\n"
        "|---|---|---|---|---|---|\n"
        "| 1 | OQ-001 | Token TTL? | HIGH | lead | 2026-05 |\n"
        "\n"
        "## M2: Launch\n"
        "\n"
        "| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| 1 | API-010 | Login | Login endpoint | AUTH | DM-001 | ac | 3 | H |\n"
        "\n"
        "### Integration Points — M2\n"
        "- none\n"
        "\n"
        "### Milestone Dependencies — M2\n"
        "- M1\n"
        "\n"
        "## Risk Assessment and Mitigation\n"
        "| Risk | Mitigation |\n"
        "|---|---|\n"
        "| R-1 | mitigate |\n"
        "\n"
        "## Success Criteria and Validation Approach\n"
        "| Criterion | Validation |\n"
        "|---|---|\n"
        "| S-1 | test |\n"
        "\n"
        "## Decision Summary\n"
        "- choice 1\n"
        "\n"
        "## Timeline Estimates\n"
        "- M1: 4 weeks\n"
        "- M2: 6 weeks\n"
    )


def test_complete_roadmap_passes(tmp_path: Path) -> None:
    out = tmp_path / "roadmap.md"
    out.write_text(_complete_roadmap(), encoding="utf-8")

    assert _validate_merge_completeness(out) == []


def test_m5_and_tail_truncated(tmp_path: Path) -> None:
    text = _complete_roadmap().replace(
        "## Risk Assessment and Mitigation",
        "## Risk Assessment and Mitigation (truncated)\n\n<TRUNCATED>",
    )
    # Drop everything from "Risk Assessment" onward to simulate the LLM
    # cutting off mid-sequence. Also drop the M2 body to simulate loss
    # of the final milestone.
    truncated = text.split("## M2: Launch")[0] + "## Milestone Summary extra\n"
    # Re-declare M2 in the summary table (already present) to force the
    # cross-check to notice the missing body.
    out = tmp_path / "roadmap.md"
    out.write_text(truncated, encoding="utf-8")

    missing = _validate_merge_completeness(out)

    assert any("M2" in m and "missing" in m for m in missing), missing
    assert any("Risk Assessment" in m for m in missing), missing
    assert any("Success Criteria" in m for m in missing), missing
    assert any("Decision Summary" in m for m in missing), missing
    assert any("Timeline Estimates" in m for m in missing), missing


def test_oq_row_in_deliverable_table_flagged(tmp_path: Path) -> None:
    # Replace a deliverable row with an OQ-xxx row to simulate the
    # schema violation observed in test14 output.
    text = _complete_roadmap().replace(
        "| 1 | DM-001 | Schema | User schema | AUTH | - | ac | 2 | H |",
        "| 1 | DM-001 | Schema | User schema | AUTH | - | ac | 2 | H |\n"
        "| 2 | OQ-002 | Token TTL policy | Decision | AUTH | - | - | - | - |",
    )
    out = tmp_path / "roadmap.md"
    out.write_text(text, encoding="utf-8")

    missing = _validate_merge_completeness(out)

    assert any("OQ-xxx" in m and "OQ-002" in m for m in missing), missing


def test_milestone_without_oqs_omits_subsection(tmp_path: Path) -> None:
    # Drop the OQ subsection from M1 and set open_questions=0 in
    # frontmatter to simulate a milestone legitimately having no OQs.
    text = _complete_roadmap()
    text = text.replace("open_questions: 1\n", "open_questions: 0\n")
    # Remove the M1 OQ subsection along with its table rows.
    oq_block = (
        "### Open Questions — M1\n"
        "\n"
        "| # | ID | Question | Impact | Owner | Target |\n"
        "|---|---|---|---|---|---|\n"
        "| 1 | OQ-001 | Token TTL? | HIGH | lead | 2026-05 |\n"
        "\n"
    )
    assert oq_block in text
    text = text.replace(oq_block, "")
    out = tmp_path / "roadmap.md"
    out.write_text(text, encoding="utf-8")

    # Gate must pass: omission is legal when frontmatter says there are
    # no OQs.
    assert _validate_merge_completeness(out) == []


def test_global_open_questions_section_rejected(tmp_path: Path) -> None:
    text = _complete_roadmap() + (
        "\n## Open Questions\n\n"
        "| ID | Question |\n"
        "|---|---|\n"
        "| OQ-001 | legacy global table |\n"
    )
    out = tmp_path / "roadmap.md"
    out.write_text(text, encoding="utf-8")

    missing = _validate_merge_completeness(out)

    assert any("global '## Open Questions'" in m for m in missing), missing


def test_frontmatter_oqs_positive_but_no_subsection(tmp_path: Path) -> None:
    text = _complete_roadmap()
    # Drop the only per-milestone OQ subsection while leaving the
    # frontmatter count at 1.
    oq_block = (
        "### Open Questions — M1\n"
        "\n"
        "| # | ID | Question | Impact | Owner | Target |\n"
        "|---|---|---|---|---|---|\n"
        "| 1 | OQ-001 | Token TTL? | HIGH | lead | 2026-05 |\n"
        "\n"
    )
    text = text.replace(oq_block, "")
    out = tmp_path / "roadmap.md"
    out.write_text(text, encoding="utf-8")

    missing = _validate_merge_completeness(out)

    assert any(
        "open_questions > 0" in m for m in missing
    ), missing


def test_missing_integration_points_flagged(tmp_path: Path) -> None:
    text = _complete_roadmap().replace(
        "### Integration Points — M2\n- none\n\n",
        "",
    )
    out = tmp_path / "roadmap.md"
    out.write_text(text, encoding="utf-8")

    missing = _validate_merge_completeness(out)

    assert any(
        "Integration Points — M2" in m for m in missing
    ), missing


def test_missing_output_file_returns_nonempty(tmp_path: Path) -> None:
    out = tmp_path / "does_not_exist.md"
    missing = _validate_merge_completeness(out)
    assert missing and "does not exist" in missing[0]
