"""TEST-007 — Inherited Structural Verdict block presence (R-063 / FR-CONV.3 PR-04).

Phase-3 / T03.11 deliverable (D-0035). Asserts that the
``## Inherited Structural Verdict`` block header appears verbatim in
the task-builder A.10.5 spawn-prompt template, at the API-002
wire-contract position (after TARGET FILES + PROJECT CONVENTIONS,
before ADVERSARIAL STANCE / INSTRUCTIONS), in BOTH the source-of-truth
SKILL.md and its ``.claude/`` mirror.

Acceptance reference (phase-3-tasklist.md L539-542):
- ``uv run pytest tests/audit/test_inherited_verdict_present.py -v`` exits 0.
- Fixture's assertion matches the block header verbatim.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0035/evidence.md``.

The "spawn-log" in the phase task description is the spawn-prompt
template itself (the QA-prompt fenced block inside A.10.5). Per
D-0028 §5, the block is verified via static grep over
``src/superclaude/skills/task-builder/SKILL.md`` — there is no
separate runtime log file; the template IS the log under test.

Run: ``uv run pytest tests/audit/test_inherited_verdict_present.py -v``
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"
SKILL_MIRROR = REPO_ROOT / ".claude" / "skills" / "task-builder" / "SKILL.md"

BLOCK_HEADER = "## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)"

TARGET_FILES_RE = re.compile(r"^TARGET FILES \(verify ALL")
PROJECT_CONVENTIONS_RE = re.compile(r"^PROJECT CONVENTIONS:\s*$")
INSTRUCTIONS_RE = re.compile(r"^INSTRUCTIONS:\s*$")
ADVERSARIAL_RE = re.compile(r"^\*\*ADVERSARIAL STANCE:")


def _first_line(path: Path, predicate) -> int:
    """Return 1-based line number of the first line matching ``predicate``, or -1."""
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if predicate(line):
            return idx
    return -1


def _line_of_header(path: Path) -> int:
    return _first_line(path, lambda line: line.strip() == BLOCK_HEADER)


@pytest.fixture(scope="module")
def src_text() -> str:
    return SKILL_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def mirror_text() -> str:
    return SKILL_MIRROR.read_text(encoding="utf-8")


class TestInheritedVerdictHeaderPresent:
    """The verbatim block header is present in both SKILL.md surfaces."""

    def test_skill_md_source_exists(self):
        assert SKILL_SRC.is_file(), f"missing source SKILL.md at {SKILL_SRC}"

    def test_skill_md_mirror_exists(self):
        assert SKILL_MIRROR.is_file(), f"missing mirror SKILL.md at {SKILL_MIRROR}"

    def test_header_present_in_source(self, src_text: str):
        assert BLOCK_HEADER in src_text, (
            f"verbatim block header not found in {SKILL_SRC}"
        )

    def test_header_present_in_mirror(self, mirror_text: str):
        assert BLOCK_HEADER in mirror_text, (
            f"verbatim block header not found in {SKILL_MIRROR}"
        )

    def test_header_appears_exactly_once_in_source(self, src_text: str):
        count = src_text.count(BLOCK_HEADER)
        assert count == 1, (
            f"expected exactly 1 occurrence of block header in {SKILL_SRC}, got {count}"
        )

    def test_header_appears_exactly_once_in_mirror(self, mirror_text: str):
        count = mirror_text.count(BLOCK_HEADER)
        assert count == 1, (
            f"expected exactly 1 occurrence of block header in {SKILL_MIRROR}, got {count}"
        )


class TestInheritedVerdictHeaderPosition:
    """API-002 wire-contract: header sits after TARGET FILES + PROJECT CONVENTIONS,
    before ADVERSARIAL STANCE / INSTRUCTIONS (D-0028 §2.2)."""

    def _ordering(self, path: Path) -> dict[str, int]:
        target = _first_line(path, lambda line: bool(TARGET_FILES_RE.match(line)))
        conv = _first_line(path, lambda line: bool(PROJECT_CONVENTIONS_RE.match(line)))
        header = _line_of_header(path)
        # The ADVERSARIAL STANCE inside the QA prompt template is the one
        # AFTER the verdict block (the file has earlier occurrences too).
        text_lines = path.read_text(encoding="utf-8").splitlines()
        adversarial = -1
        for idx in range(header, len(text_lines)):
            if ADVERSARIAL_RE.match(text_lines[idx]):
                adversarial = idx + 1
                break
        instructions = -1
        for idx in range(header, len(text_lines)):
            if INSTRUCTIONS_RE.match(text_lines[idx]):
                instructions = idx + 1
                break
        return {
            "TARGET FILES": target,
            "PROJECT CONVENTIONS": conv,
            "## Inherited Structural Verdict": header,
            "ADVERSARIAL STANCE": adversarial,
            "INSTRUCTIONS": instructions,
        }

    def test_ordering_in_source(self):
        ord_ = self._ordering(SKILL_SRC)
        for name, line in ord_.items():
            assert line != -1, f"{name} not found in {SKILL_SRC} (ord={ord_})"
        assert (
            ord_["TARGET FILES"]
            < ord_["PROJECT CONVENTIONS"]
            < ord_["## Inherited Structural Verdict"]
            < ord_["ADVERSARIAL STANCE"]
            < ord_["INSTRUCTIONS"]
        ), f"API-002 ordering violated in source SKILL.md: {ord_}"

    def test_ordering_in_mirror(self):
        ord_ = self._ordering(SKILL_MIRROR)
        for name, line in ord_.items():
            assert line != -1, f"{name} not found in {SKILL_MIRROR} (ord={ord_})"
        assert (
            ord_["TARGET FILES"]
            < ord_["PROJECT CONVENTIONS"]
            < ord_["## Inherited Structural Verdict"]
            < ord_["ADVERSARIAL STANCE"]
            < ord_["INSTRUCTIONS"]
        ), f"API-002 ordering violated in mirror SKILL.md: {ord_}"


class TestInheritedVerdictMirrorParity:
    """Source and mirror agree byte-for-byte at the block-header line, and the
    block header appears at the same 1-based line number in both surfaces."""

    def test_byte_identical_files(self, src_text: str, mirror_text: str):
        assert src_text == mirror_text, (
            "src/superclaude/skills/task-builder/SKILL.md and "
            ".claude/skills/task-builder/SKILL.md must be byte-identical "
            "(run `make sync-dev`)"
        )

    def test_header_at_same_line_number(self):
        src_line = _line_of_header(SKILL_SRC)
        mirror_line = _line_of_header(SKILL_MIRROR)
        assert src_line == mirror_line and src_line != -1, (
            f"block header line drift: source={src_line}, mirror={mirror_line}"
        )


class TestInheritedVerdictGrepAssertion:
    """Phase-3-tasklist AC: 'Grep-on-spawn-log assertion green' — emulates the
    literal grep an operator would run, returning the matching line text."""

    def test_grep_returns_header_line(self):
        """Equivalent of:
        ``grep -n "Inherited Structural Verdict" src/superclaude/skills/task-builder/SKILL.md``
        — at least one returned line equals the verbatim block header.
        """
        matches = [
            line
            for line in SKILL_SRC.read_text(encoding="utf-8").splitlines()
            if "Inherited Structural Verdict" in line
        ]
        assert matches, "grep returned no matches in source SKILL.md"
        assert any(line.strip() == BLOCK_HEADER for line in matches), (
            "no grep match equals the verbatim block header "
            f"({BLOCK_HEADER!r}); got {matches!r}"
        )
