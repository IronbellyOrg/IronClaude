"""TEST-006 — Hidden-input determinism (NFR-CONV.3, R-045).

Backs T02.09 / D-0023 evidence: the rendered `## Execution Context` block
contains NO specific file paths or ``file:line`` citations. The header-wide
hidden-input guard (R-039) is enforced as a post-assembly grep:

    grep -cE "src/|/.*:[0-9]+" <header-range>  →  returns 0

This test asserts the positive path (clean fixtures yield 0 hits) and the
negative path (a deliberately leaky fixture yields ≥1 hit, demonstrating
the detector is wired correctly — not vacuously passing).

Run: ``uv run pytest tests/audit/test_execution_context_no_file_paths.py -v``
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "execution_context"
FULL_FIXTURE = FIXTURE_DIR / "fully_populated.md"
MINIMAL_FIXTURE = FIXTURE_DIR / "minimal_buildrequest.md"
LEAK_FIXTURE = FIXTURE_DIR / "hidden_input_leak.md"

HEADING = "## Execution Context"
# NFR-CONV.3 hidden-input determinism regex (R-039 / D-0017 § 2).
HIDDEN_INPUT_PATTERN = re.compile(r"src/|/.*:[0-9]+")


def _extract_header_range(text: str) -> str:
    """Return the byte range from `## Execution Context` heading to the
    next standalone ``---`` separator."""
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == HEADING)
    except StopIteration as exc:
        raise AssertionError(f"fixture missing `{HEADING}` heading") from exc
    end = start + 1
    while end < len(lines) and lines[end].strip() != "---":
        end += 1
    return "\n".join(lines[start : end + 1])


def _grep_count(text: str) -> int:
    """Mirror ``grep -cE "src/|/.*:[0-9]+"`` over the supplied text:
    return the count of lines that match the regex (grep's ``-c``
    semantics)."""
    return sum(1 for line in text.splitlines() if HIDDEN_INPUT_PATTERN.search(line))


def _grep_count_via_subprocess(text: str) -> int:
    """Independent oracle: shell out to real ``grep -cE`` so the test
    cannot drift from the production verification command."""
    result = subprocess.run(
        ["grep", "-cE", "src/|/.*:[0-9]+"],
        input=text,
        capture_output=True,
        text=True,
        check=False,
    )
    # grep -c exits 1 when no matches; stdout is the integer count either way.
    return int(result.stdout.strip() or "0")


class TestHiddenInputGuardCleanFixtures:
    """Positive path: clean fixtures yield zero hidden-input hits in the header range."""

    def test_fully_populated_header_has_zero_hidden_input_hits(self):
        block = _extract_header_range(FULL_FIXTURE.read_text(encoding="utf-8"))
        assert _grep_count(block) == 0, (
            "fully-populated header must not contain `src/` or `file:line` citations"
        )

    def test_minimal_header_has_zero_hidden_input_hits(self):
        block = _extract_header_range(MINIMAL_FIXTURE.read_text(encoding="utf-8"))
        assert _grep_count(block) == 0, (
            "degraded header must not contain `src/` or `file:line` citations"
        )

    def test_clean_fixtures_match_real_grep_output(self):
        """Cross-check the in-process regex helper against ``grep -cE`` itself."""
        for fixture in (FULL_FIXTURE, MINIMAL_FIXTURE):
            block = _extract_header_range(fixture.read_text(encoding="utf-8"))
            assert _grep_count_via_subprocess(block) == 0, (
                f"`grep -cE` returned non-zero against clean fixture {fixture.name}"
            )


class TestHiddenInputGuardDetectsLeaks:
    """Negative path: a deliberately leaky header yields non-zero hits.

    Ensures the guard is wired and not vacuously passing because the regex
    is wrong or the header-range extractor returns an empty string."""

    def test_leak_fixture_has_nonzero_hidden_input_hits(self):
        block = _extract_header_range(LEAK_FIXTURE.read_text(encoding="utf-8"))
        assert _grep_count(block) >= 1, (
            "leak fixture must trigger at least one hidden-input hit "
            "(detector wiring sanity check)"
        )

    def test_leak_fixture_matches_real_grep_output(self):
        block = _extract_header_range(LEAK_FIXTURE.read_text(encoding="utf-8"))
        assert _grep_count_via_subprocess(block) >= 1, (
            "`grep -cE` returned zero against the leaky fixture — production "
            "verification command would falsely pass"
        )
