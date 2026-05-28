"""TEST-014 — Severity-floor / Critical Rules block preservation (R-087 / FR-CONV.4 PR-07).

Phase-4 / T04.14 deliverable (D-0052). Asserts that the severity-floor /
Critical Rules block at rf-qa-qualitative.md is byte-identical to the
pre-M4 baseline at commit ``3a57a0d`` (the last commit on this branch
before PR-07 axis-overlay landed). Two equality proofs are checked:

1. The strict ``:786-795`` spec range (pre-M4) maps to ``:831-840``
   (post-M4) with SHA-256
   ``770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7``.
2. The entire Critical Rules block (``## Critical Rules`` header + Rules
   #1..#11) has SHA-256
   ``cc57869c5580b32d9c38a9a64089820a9ea92e4103c8eb68d5b5ff041e5de06b``
   (re-pinned 2026-05-24 after markdownlint MD013 reflow in
   TASK-RF-20260523-234320-markdownlint-remediation).

Rule #6 — "Contradictions are always IMPORTANT or CRITICAL" — must
appear verbatim with no softening verbs.

Acceptance reference (phase-4-tasklist.md T04.14 AC):
- ``uv run pytest tests/audit/test_severity_floor_unweakened.py -v`` exits 0.
- TEST-014 asserts byte-diff of Critical Rules block is zero.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0052/evidence.md``.

Run: ``uv run pytest tests/audit/test_severity_floor_unweakened.py -v``
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
AGENT_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa-qualitative.md"

# Baselines captured in D-0049 evidence (pre-M4 commit 3a57a0d).
BASELINE_SLICE_SHA = (
    "770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7"
)
# Updated 2026-05-24: re-pinned to post-reflow content following the
# authorized markdownlint MD013 remediation in
# TASK-RF-20260523-234320-markdownlint-remediation. The Critical Rules
# block was reflowed (no semantic content change); recompute reflects
# the new byte sequence of the same logical block.
BASELINE_BLOCK_SHA = (
    "cc57869c5580b32d9c38a9a64089820a9ea92e4103c8eb68d5b5ff041e5de06b"  # pragma: allowlist secret
)

# Rule #6 verbatim text (the explicit severity floor).
RULE_6_TEXT = (
    "**Contradictions are always IMPORTANT or CRITICAL** — If two sections "
    "say different things about the same topic, that's never minor. Always "
    "surface contradictions."
)

CRITICAL_RULES_HEADER = "## Critical Rules"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _slice_lines(path: Path, start: int, end_inclusive: int) -> str:
    """Return the substring of ``path`` covering 1-based lines [start, end_inclusive].

    Preserves the trailing newline of the last line if present in source, matching
    the byte semantics of ``sed -n 'A,Bp'``.
    """
    raw = path.read_text(encoding="utf-8")
    # Split keeping line endings so we can reconstruct byte-identically.
    lines = raw.splitlines(keepends=True)
    if start < 1 or end_inclusive > len(lines):
        return ""
    return "".join(lines[start - 1 : end_inclusive])


def _find_line(path: Path, predicate) -> int:
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if predicate(line):
            return idx
    return -1


def _critical_rules_block(path: Path) -> tuple[int, int, str]:
    """Return (header_line, end_line_inclusive, block_text).

    The block runs from the ``## Critical Rules`` header through Rule #11
    inclusive (the last numbered rule in the file)."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_line = -1
    rule_11_line = -1
    for idx, line in enumerate(lines, start=1):
        if header_line == -1 and line.strip() == CRITICAL_RULES_HEADER:
            header_line = idx
            continue
        if header_line != -1 and re.match(r"\s*11\.\s+\*\*", line):
            rule_11_line = idx
            # Don't break; in case Rule #11 has continuation lines, keep last
            # numbered-rule start as the end anchor for now.
    assert header_line != -1, f"`{CRITICAL_RULES_HEADER}` not found in {path}"
    assert rule_11_line != -1, f"Rule #11 not found in {path}"
    # Block spans header through end-of-Rule-#11. Rule #11 is one logical
    # line (no blank-line continuation in this file), so end == rule_11_line.
    block_text = "".join(lines[header_line - 1 : rule_11_line])
    return header_line, rule_11_line, block_text


@pytest.fixture(scope="module")
def src_text() -> str:
    return AGENT_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def mirror_text() -> str:
    return AGENT_MIRROR.read_text(encoding="utf-8")


class TestSeverityFloorSliceHash:
    """The 10-line severity-floor slice matches the pre-M4 baseline byte-for-byte."""

    def _locate_post_m4_slice(self, path: Path) -> tuple[int, int, str]:
        """Locate the 10-line window whose SHA-256 matches BASELINE_SLICE_SHA.

        Per D-0049 §2.1 the baseline slice (pre-M4 ``:786-795``) is a
        10-line window anchored 3 lines above the ``## Critical Rules``
        header (the blank line preceding the trailing ``---`` separator)
        through Rule #5 inclusive. Post-M4 the equivalent window lives at
        ``:831-840`` (line-offset +45 from strictly-additive insertions
        above the section). Anchoring by the header keeps the test stable
        across future strictly-additive insertions above the block.
        """
        header_line = _find_line(path, lambda line: line.strip() == CRITICAL_RULES_HEADER)
        assert header_line != -1, f"`{CRITICAL_RULES_HEADER}` not found in {path}"
        start = header_line - 3
        end = header_line + 6
        return start, end, _slice_lines(path, start, end)

    def test_slice_hash_matches_baseline_source(self):
        start, end, slice_text = self._locate_post_m4_slice(AGENT_SRC)
        actual_sha = _sha256(slice_text)
        assert actual_sha == BASELINE_SLICE_SHA, (
            f"severity-floor slice {AGENT_SRC.name}:{start}-{end} drifted from baseline. "
            f"Expected SHA-256 {BASELINE_SLICE_SHA}, got {actual_sha}. "
            "Slice anchored at trailing `---` before `## Critical Rules`."
        )

    def test_slice_hash_matches_baseline_mirror(self):
        start, end, slice_text = self._locate_post_m4_slice(AGENT_MIRROR)
        actual_sha = _sha256(slice_text)
        assert actual_sha == BASELINE_SLICE_SHA, (
            f"severity-floor slice {AGENT_MIRROR.name}:{start}-{end} drifted from baseline. "
            f"Expected SHA-256 {BASELINE_SLICE_SHA}, got {actual_sha}."
        )


class TestCriticalRulesBlockHash:
    """The entire Critical Rules block matches the pre-M4 baseline byte-for-byte."""

    def test_block_hash_matches_baseline_source(self):
        _, _, block_text = _critical_rules_block(AGENT_SRC)
        actual_sha = _sha256(block_text)
        assert actual_sha == BASELINE_BLOCK_SHA, (
            f"Critical Rules block in {AGENT_SRC} drifted from baseline. "
            f"Expected SHA-256 {BASELINE_BLOCK_SHA}, got {actual_sha}. "
            "Byte-diff of the block must be zero."
        )

    def test_block_hash_matches_baseline_mirror(self):
        _, _, block_text = _critical_rules_block(AGENT_MIRROR)
        actual_sha = _sha256(block_text)
        assert actual_sha == BASELINE_BLOCK_SHA, (
            f"Critical Rules block in {AGENT_MIRROR} drifted from baseline. "
            f"Expected SHA-256 {BASELINE_BLOCK_SHA}, got {actual_sha}."
        )

    def test_byte_diff_block_source_vs_mirror_is_zero(self):
        _, _, src_block = _critical_rules_block(AGENT_SRC)
        _, _, mirror_block = _critical_rules_block(AGENT_MIRROR)
        assert src_block == mirror_block, (
            "Critical Rules block byte-diff between source and mirror must be zero "
            "(run `make sync-dev`)."
        )


class TestRule6Verbatim:
    """Rule #6 — the explicit severity floor — appears verbatim with no softening."""

    SOFTENING_TOKENS = [
        "may be MINOR",
        "may be minor",
        "could be MINOR",
        "could be minor",
        "typically",
        "should be IMPORTANT",
        "consider IMPORTANT",
    ]

    def test_rule_6_present_in_source(self, src_text: str):
        assert RULE_6_TEXT in src_text, (
            f"Rule #6 verbatim text not found in {AGENT_SRC}; severity floor may have been weakened"
        )

    def test_rule_6_present_in_mirror(self, mirror_text: str):
        assert RULE_6_TEXT in mirror_text, (
            f"Rule #6 verbatim text not found in {AGENT_MIRROR}; severity floor may have been weakened"
        )

    def test_no_softening_tokens_in_critical_rules_block(self):
        _, _, block_text = _critical_rules_block(AGENT_SRC)
        for token in self.SOFTENING_TOKENS:
            assert token not in block_text, (
                f"softening token {token!r} found in Critical Rules block — severity floor weakened"
            )
