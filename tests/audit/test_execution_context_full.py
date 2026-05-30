"""TEST-004 — Fully-populated `## Execution Context` block fixture (R-043).

Backs T02.09 / D-0023 evidence: a fully-populated BUILD_REQUEST produces a
header block containing all three DM-001 labeled bullets — References,
Source areas, Key constraints — in declared order, between the frontmatter
and the first `### T<PP>.<TT>` phase task.

Run: ``uv run pytest tests/audit/test_execution_context_full.py -v``
"""

from __future__ import annotations

from pathlib import Path

FIXTURE = (
    Path(__file__).parent / "fixtures" / "execution_context" / "fully_populated.md"
)

HEADING = "## Execution Context"
LABELS = ("**References:**", "**Source areas:**", "**Key constraints:**")


def _extract_header_range(text: str) -> str:
    """Return the byte range from the `## Execution Context` heading line
    through the next standalone ``---`` separator (the block boundary
    defined by the DM-001 contract-freeze at T01.13 / D-0011 § 1)."""
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == HEADING)
    except StopIteration as exc:
        raise AssertionError(f"fixture missing `{HEADING}` heading") from exc
    end = start + 1
    while end < len(lines) and lines[end].strip() != "---":
        end += 1
    return "\n".join(lines[start : end + 1])


class TestExecutionContextFull:
    """All three DM-001 labeled bullets render for a fully-populated BUILD_REQUEST."""

    def test_fixture_exists(self):
        assert FIXTURE.is_file(), f"fixture missing: {FIXTURE}"

    def test_block_heading_present(self):
        text = FIXTURE.read_text(encoding="utf-8")
        assert HEADING in text, "fixture must contain `## Execution Context` heading"

    def test_block_sits_between_frontmatter_and_first_phase(self):
        text = FIXTURE.read_text(encoding="utf-8")
        lines = text.splitlines()
        # Line-based scan so substrings inside the YAML frontmatter description
        # are not mistaken for the actual heading line.
        heading_idx = next(i for i, line in enumerate(lines) if line.strip() == HEADING)
        sep_indices = [i for i, line in enumerate(lines) if line.strip() == "---"]
        assert len(sep_indices) >= 2, "frontmatter delimiters missing"
        frontmatter_close = sep_indices[1]
        assert heading_idx > frontmatter_close, "header must sit AFTER frontmatter"
        first_phase_idx = next(
            i for i, line in enumerate(lines) if line.startswith("### T01.01")
        )
        assert heading_idx < first_phase_idx, (
            "header must sit BEFORE the first `### T<PP>.<TT>` phase task"
        )

    def test_all_three_labeled_bullets_present(self):
        block = _extract_header_range(FIXTURE.read_text(encoding="utf-8"))
        for label in LABELS:
            assert label in block, f"fully-populated block missing label `{label}`"

    def test_labeled_bullets_in_declared_order(self):
        """DM-001 § 1 mandates the bullet order: References, Source areas, Key constraints."""
        block = _extract_header_range(FIXTURE.read_text(encoding="utf-8"))
        positions = [block.index(label) for label in LABELS]
        assert positions == sorted(positions), (
            "labeled bullets must appear in DM-001 declared order "
            "(References, Source areas, Key constraints)"
        )
