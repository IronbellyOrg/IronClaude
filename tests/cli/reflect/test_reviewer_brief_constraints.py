"""L4 reviewer-brief-constraints guard (source-text, cross-file, falsifier-disciplined).

Reads both SOURCE files (never the ``.claude/`` mirror) and asserts:
(a) the ``## Constraints (READ-ONLY)`` section is PRESENT in reviewer-spec.md;
(b) the Step 3B.0 live-exec prohibition is PRESENT in SKILL.md;
(c) the ``reflect-reviewer`` agent-type appears in the reviewer rotation of BOTH
    SKILL.md §7.1 AND reviewer-spec.md ``## Composition`` — a cross-file
    consistency assertion that FAILS if either file is repointed but not the other
    (the highest cross-file drift risk in the L4 anchor set).

Falsifier discipline: fails-before (sections/repoints absent) and passes-after.
"""

from __future__ import annotations

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SKILL_SRC = _REPO_ROOT / "src/superclaude/skills/sc-reflect-protocol/SKILL.md"
_SPEC_SRC = (
    _REPO_ROOT / "src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md"
)


def _section(text: str, start_pat: str, end_pat: str = r"\n#{1,3} ") -> str:
    """Return the slice from a heading match to the next heading (or EOF)."""
    m = re.search(start_pat, text, re.MULTILINE)
    assert m is not None, f"section start {start_pat!r} not found"
    rest = text[m.end() :]
    end = re.search(end_pat, rest, re.MULTILINE)
    return rest[: end.start()] if end else rest


def test_constraints_readonly_section_present_in_reviewer_spec() -> None:
    spec = _SPEC_SRC.read_text(encoding="utf-8")
    assert re.search(r"^## Constraints \(READ-ONLY\)", spec, re.MULTILINE), (
        "reviewer-spec.md must carry a `## Constraints (READ-ONLY)` section (L4)"
    )
    # The section must state the read-only / no-shell / no-git / no-mutation intent.
    section = _section(spec, r"^## Constraints \(READ-ONLY\)", r"\n## ")
    low = section.lower()
    assert "read-only" in low
    assert "no shell" in low or "no `bash`" in low or "no shell execution" in low
    assert "git" in low and "mutat" in low


def test_step_3b0_live_exec_prohibition_present_in_skill() -> None:
    skill = _SKILL_SRC.read_text(encoding="utf-8")
    assert "Live-execution prohibition" in skill, (
        "SKILL.md Step 3B.0 must carry the live-execution prohibition (L4)"
    )
    assert "MUST NOT embed live-execution instructions" in skill
    # The sanctioned FR-4 verification-results hunk pattern is the cross-ref.
    assert "FR-4 verification-results" in skill


def test_reflect_reviewer_repointed_in_both_rotation_tables() -> None:
    """Cross-file consistency: the fixed `reflect-reviewer` agent-type must appear
    in the reviewer rotation of BOTH files. Fails if only one was repointed."""
    skill = _SKILL_SRC.read_text(encoding="utf-8")
    spec = _SPEC_SRC.read_text(encoding="utf-8")
    skill_71 = _section(skill, r"^### 7\.1 Reviewer composition rules", r"\n### ")
    spec_comp = _section(spec, r"^## Composition", r"\nXXX_NO_MATCH")  # to EOF
    assert "reflect-reviewer" in skill_71, (
        "SKILL.md §7.1 rotation must point at the fixed `reflect-reviewer` agent-type"
    )
    assert "reflect-reviewer" in spec_comp, (
        "reviewer-spec.md `## Composition` must point at `reflect-reviewer` (cross-file drift!)"
    )
