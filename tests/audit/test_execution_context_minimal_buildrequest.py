"""TEST-005 — Minimal-BUILD_REQUEST References-only degradation (R-044).

Backs T02.09 / D-0023 evidence: under a minimal BUILD_REQUEST (GOAL is the
only populated rollup-signal field), the `## Execution Context` block
degenerates to a single ``**References:**`` bullet. ``Source areas:`` and
``Key constraints:`` bullets are PHYSICALLY ABSENT from the rendered block
— not present-and-blank, not stub-bulleted. R-038 (DM-001 contract-freeze
T01.13 / D-0011 § 1).

Run: ``uv run pytest tests/audit/test_execution_context_minimal_buildrequest.py -v``
"""

from __future__ import annotations

from pathlib import Path

FIXTURE = (
    Path(__file__).parent / "fixtures" / "execution_context" / "minimal_buildrequest.md"
)

HEADING = "## Execution Context"


def _extract_header_range(text: str) -> str:
    """Return the byte range from the `## Execution Context` heading line
    through the next standalone ``---`` separator."""
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == HEADING)
    except StopIteration as exc:
        raise AssertionError(f"fixture missing `{HEADING}` heading") from exc
    end = start + 1
    while end < len(lines) and lines[end].strip() != "---":
        end += 1
    return "\n".join(lines[start : end + 1])


class TestExecutionContextMinimal:
    """Minimal BUILD_REQUEST → References-only degraded form."""

    def test_fixture_exists(self):
        assert FIXTURE.is_file(), f"fixture missing: {FIXTURE}"

    def test_block_heading_present(self):
        text = FIXTURE.read_text(encoding="utf-8")
        assert HEADING in text, (
            "degraded form still emits the `## Execution Context` heading"
        )

    def test_references_bullet_present(self):
        block = _extract_header_range(FIXTURE.read_text(encoding="utf-8"))
        assert "**References:**" in block, (
            "degraded form MUST retain the `**References:**` bullet (R-038)"
        )

    def test_source_areas_bullet_absent(self):
        """R-038 — bullet must be physically removed under minimal BUILD_REQUEST,
        not rendered as a blank or stub bullet."""
        block = _extract_header_range(FIXTURE.read_text(encoding="utf-8"))
        assert "Source areas:" not in block, (
            "degraded form MUST omit `Source areas:` line (not blank-but-present)"
        )

    def test_key_constraints_bullet_absent(self):
        """R-038 — bullet must be physically removed under minimal BUILD_REQUEST."""
        block = _extract_header_range(FIXTURE.read_text(encoding="utf-8"))
        assert "Key constraints:" not in block, (
            "degraded form MUST omit `Key constraints:` line (not blank-but-present)"
        )

    def test_only_one_labeled_bullet_in_block(self):
        """Exactly one labeled bullet (`**References:**`) in the degraded form."""
        block = _extract_header_range(FIXTURE.read_text(encoding="utf-8"))
        labeled_lines = [
            line
            for line in block.splitlines()
            if line.startswith("- **")
            and line.endswith(":**")
            or (line.startswith("- **") and ":**" in line)
        ]
        assert len(labeled_lines) == 1, (
            f"expected 1 labeled bullet in degraded block, found {len(labeled_lines)}: "
            f"{labeled_lines!r}"
        )
        assert labeled_lines[0].startswith("- **References:**"), (
            "the single bullet in the degraded form MUST be `**References:**`"
        )
