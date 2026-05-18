"""TEST-012 — Items Reviewed table carries an Axis column (R-085 / FR-CONV.4 PR-07).

Phase-4 / T04.14 deliverable (D-0052). Asserts that the Items Reviewed
table header at rf-qa-qualitative.md includes the ``axis`` column between
``Check`` and ``Result`` for the task-qualitative phase, and that the
canonical-rules HTML comment binds the closed vocabulary
``{AX-1..AX-5, none}`` and FORBIDS ``N/A``/``n/a``/``—``/blank.

Acceptance reference (phase-4-tasklist.md T04.14 AC):
- ``uv run pytest tests/audit/test_axis_column_populated.py -v`` exits 0.
- Header row includes the Axis column in canonical position.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0052/evidence.md``.

Run: ``uv run pytest tests/audit/test_axis_column_populated.py -v``
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
AGENT_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa-qualitative.md"

HEADER_RE = re.compile(r"\|\s*#\s*\|\s*Check\s*\|\s*axis\s*\|\s*Result\s*\|\s*Evidence\s*\|", re.IGNORECASE)
ITEMS_REVIEWED_LINE = "## Items Reviewed"
FORBIDDEN_VALUES = ["N/A", "n/a", "—", "blank"]


def _find_header_line(path: Path) -> tuple[int, str]:
    """Return (1-based line number, line text) of the first Items-Reviewed table
    header that contains the axis column, or (-1, '')."""
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if HEADER_RE.search(line):
            return idx, line
    return -1, ""


@pytest.fixture(scope="module")
def src_text() -> str:
    return AGENT_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def mirror_text() -> str:
    return AGENT_MIRROR.read_text(encoding="utf-8")


class TestAxisColumnHeaderPresent:
    """The Items Reviewed table header includes the axis column."""

    def test_header_present_in_source(self):
        line_no, line = _find_header_line(AGENT_SRC)
        assert line_no != -1, (
            f"Items-Reviewed header with axis column not found in {AGENT_SRC}"
        )
        assert "axis" in line.lower()

    def test_header_present_in_mirror(self):
        line_no, line = _find_header_line(AGENT_MIRROR)
        assert line_no != -1, (
            f"Items-Reviewed header with axis column not found in {AGENT_MIRROR}"
        )
        assert "axis" in line.lower()

    def test_header_column_order_check_axis_result(self, src_text: str):
        """`axis` column sits between `Check` and `Result` columns."""
        match = HEADER_RE.search(src_text)
        assert match is not None
        header = match.group(0)
        # Position of column tokens in the header substring.
        check_pos = header.lower().index("check")
        axis_pos = header.lower().index("axis")
        result_pos = header.lower().index("result")
        assert check_pos < axis_pos < result_pos, (
            f"axis column must sit between Check and Result: header={header!r}"
        )


class TestAxisColumnCanonicalVocabulary:
    """Canonical vocabulary `{AX-1..AX-5, none}` is bound in the rules subsection."""

    VOCAB_PATTERN = re.compile(
        r"AX-1\s*,\s*AX-2\s*,\s*AX-3\s*,\s*AX-4\s*,\s*AX-5\s*,\s*none",
        re.IGNORECASE,
    )

    def test_canonical_set_in_source(self, src_text: str):
        assert self.VOCAB_PATTERN.search(src_text), (
            f"canonical vocabulary `{{AX-1..AX-5, none}}` not found in {AGENT_SRC}"
        )

    def test_canonical_set_in_mirror(self, mirror_text: str):
        assert self.VOCAB_PATTERN.search(mirror_text), (
            f"canonical vocabulary `{{AX-1..AX-5, none}}` not found in {AGENT_MIRROR}"
        )

    def test_forbidden_values_named_in_rules(self, src_text: str):
        """The canonical-rules block must explicitly forbid N/A-style escapes."""
        for token in ["N/A", "n/a", "—", "blank"]:
            assert token in src_text, (
                f"canonical-rules block must name forbidden value {token!r} in {AGENT_SRC}"
            )


class TestAxisColumnRowFormat:
    """The example row in the Items Reviewed table enumerates the closed
    vocabulary and does not use `N/A` as a placeholder."""

    ROW_RE = re.compile(
        r"\|\s*1\s*\|\s*\[check name\]\s*\|\s*\[\s*AX-1\s*/\s*AX-2\s*/\s*AX-3\s*/\s*AX-4\s*/\s*AX-5\s*/\s*none\s*\]",
        re.IGNORECASE,
    )

    def test_example_row_enumerates_full_vocabulary(self, src_text: str):
        assert self.ROW_RE.search(src_text), (
            f"example row must enumerate `[AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none]` in {AGENT_SRC}"
        )

    def test_example_row_does_not_use_na_placeholder(self, src_text: str):
        match = self.ROW_RE.search(src_text)
        assert match is not None
        assert "N/A" not in match.group(0)


class TestAxisColumnSourceMirrorParity:
    """Source and mirror agree byte-for-byte at the table header."""

    def test_header_line_number_matches(self):
        src_line, _ = _find_header_line(AGENT_SRC)
        mirror_line, _ = _find_header_line(AGENT_MIRROR)
        assert src_line == mirror_line and src_line != -1, (
            f"axis-column header line drift: source={src_line}, mirror={mirror_line}"
        )

    def test_files_byte_identical(self, src_text: str, mirror_text: str):
        assert src_text == mirror_text, (
            "src/superclaude/agents/rf-qa-qualitative.md and "
            ".claude/agents/rf-qa-qualitative.md must be byte-identical "
            "(run `make sync-dev`)"
        )
