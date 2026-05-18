"""TEST-011 — Five Adversarial Axes header subsection ordering (R-084 / FR-CONV.4 PR-07).

Phase-4 / T04.14 deliverable (D-0052). Asserts that the
``#### Five Adversarial Axes`` header subsection is inserted BEFORE the
``#### Checklist (15 items)`` header in the source-of-truth
rf-qa-qualitative.md and its ``.claude/`` mirror.

Acceptance reference (phase-4-tasklist.md T04.14 AC):
- ``uv run pytest tests/audit/test_five_axes_overlay.py -v`` exits 0.
- Axes header precedes Checklist header.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0052/evidence.md``.

Run: ``uv run pytest tests/audit/test_five_axes_overlay.py -v``
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
AGENT_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa-qualitative.md"

AXES_HEADER_PREFIX = "#### Five Adversarial Axes"
CHECKLIST_HEADER = "#### Checklist (15 items)"


def _line_of(path: Path, predicate) -> int:
    """Return 1-based line number of the first matching line, or -1."""
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if predicate(line):
            return idx
    return -1


@pytest.fixture(scope="module")
def src_text() -> str:
    return AGENT_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def mirror_text() -> str:
    return AGENT_MIRROR.read_text(encoding="utf-8")


class TestFiveAxesHeaderPresent:
    """The axes header subsection is present in both rf-qa-qualitative surfaces."""

    def test_agent_source_exists(self):
        assert AGENT_SRC.is_file(), f"missing source rf-qa-qualitative.md at {AGENT_SRC}"

    def test_agent_mirror_exists(self):
        assert AGENT_MIRROR.is_file(), f"missing mirror rf-qa-qualitative.md at {AGENT_MIRROR}"

    def test_axes_header_present_in_source(self, src_text: str):
        assert AXES_HEADER_PREFIX in src_text, (
            f"axes header subsection not found in {AGENT_SRC}"
        )

    def test_axes_header_present_in_mirror(self, mirror_text: str):
        assert AXES_HEADER_PREFIX in mirror_text, (
            f"axes header subsection not found in {AGENT_MIRROR}"
        )

    def test_checklist_header_present_in_source(self, src_text: str):
        assert CHECKLIST_HEADER in src_text, (
            f"15-item checklist header not found in {AGENT_SRC}"
        )


class TestFiveAxesHeaderOrdering:
    """The axes header subsection precedes the 15-item Checklist header."""

    def _ordering(self, path: Path) -> dict[str, int]:
        axes = _line_of(path, lambda line: line.startswith(AXES_HEADER_PREFIX))
        checklist = _line_of(path, lambda line: line.strip() == CHECKLIST_HEADER)
        return {"axes": axes, "checklist": checklist}

    def test_ordering_in_source(self):
        ord_ = self._ordering(AGENT_SRC)
        assert ord_["axes"] != -1, f"axes header not found in source (ord={ord_})"
        assert ord_["checklist"] != -1, f"checklist header not found in source (ord={ord_})"
        assert ord_["axes"] < ord_["checklist"], (
            f"axes header must precede checklist header in source: {ord_}"
        )

    def test_ordering_in_mirror(self):
        ord_ = self._ordering(AGENT_MIRROR)
        assert ord_["axes"] != -1, f"axes header not found in mirror (ord={ord_})"
        assert ord_["checklist"] != -1, f"checklist header not found in mirror (ord={ord_})"
        assert ord_["axes"] < ord_["checklist"], (
            f"axes header must precede checklist header in mirror: {ord_}"
        )


class TestFiveAxesCanonicalAxes:
    """Canonical AX-1..AX-5 entries appear between the axes header and the checklist."""

    AXIS_TOKENS = ["AX-1", "AX-2", "AX-3", "AX-4", "AX-5"]

    def _slice_between_headers(self, path: Path) -> list[str]:
        lines = path.read_text(encoding="utf-8").splitlines()
        axes = -1
        checklist = -1
        for idx, line in enumerate(lines, start=1):
            if axes == -1 and line.startswith(AXES_HEADER_PREFIX):
                axes = idx
            elif axes != -1 and line.strip() == CHECKLIST_HEADER:
                checklist = idx
                break
        assert axes != -1 and checklist != -1, (
            f"could not locate axes/checklist headers in {path}: axes={axes}, checklist={checklist}"
        )
        return lines[axes - 1 : checklist - 1]

    def test_all_five_axes_appear_in_source(self):
        body = "\n".join(self._slice_between_headers(AGENT_SRC))
        for token in self.AXIS_TOKENS:
            assert token in body, f"{token} missing from axes subsection in source"

    def test_all_five_axes_appear_in_mirror(self):
        body = "\n".join(self._slice_between_headers(AGENT_MIRROR))
        for token in self.AXIS_TOKENS:
            assert token in body, f"{token} missing from axes subsection in mirror"


class TestFiveAxesSourceMirrorParity:
    """Source and mirror agree byte-for-byte."""

    def test_byte_identical_files(self, src_text: str, mirror_text: str):
        assert src_text == mirror_text, (
            "src/superclaude/agents/rf-qa-qualitative.md and "
            ".claude/agents/rf-qa-qualitative.md must be byte-identical "
            "(run `make sync-dev`)"
        )
