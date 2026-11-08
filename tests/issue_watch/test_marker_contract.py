"""Marker contract test for the issue watcher (DF-21, DF-46).

``predicates.CLAIM_MARKER`` is the one marker constant; ``github.MARKER_JQ`` is
built from it. The skill files that tell the claiming agent to end its comment
with the marker must carry the same literal. The two tracked ``src/`` copies are
required; the project ``.claude/`` copy and the installed ``~/.claude`` copy are
read only when present (an absent folder passes). Nothing is written and
``.dev/`` is never read.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.issue_watch.github import MARKER_JQ
from superclaude.cli.issue_watch.predicates import CLAIM_MARKER

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_REL = Path("skills") / "sc-issue-protocol"
FILES = (Path("refs") / "claim.md", Path("templates") / "claim-comment.md")
SRC_ROOT = REPO_ROOT / "src" / "superclaude"
OPTIONAL_ROOTS = {
    "project .claude": REPO_ROOT / ".claude",
    "installed ~/.claude": Path.home() / ".claude",
}


def test_marker_in_every_existing_copy__fr009() -> None:
    """Required src copies hold the marker; optional copies do when present."""
    for rel in FILES:
        path = SRC_ROOT / SKILL_REL / rel
        assert path.is_file(), f"required source copy missing: {path}"
        assert CLAIM_MARKER in path.read_text(encoding="utf-8"), path
    for label, root in OPTIONAL_ROOTS.items():
        for rel in FILES:
            path = root / SKILL_REL / rel
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                assert CLAIM_MARKER in text, f"{label} copy lacks marker: {path}"


def test_template_last_line_is_marker__fr009() -> None:
    """The claim-comment template ends with the marker as its last line."""
    path = SRC_ROOT / SKILL_REL / FILES[1]
    assert path.is_file(), f"required source copy missing: {path}"
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert lines, f"template is empty: {path}"
    assert lines[-1].strip() == CLAIM_MARKER


def test_marker_jq_is_built_from_claim_marker__fr009() -> None:
    """DF-21: one constant; the jq filter embeds CLAIM_MARKER."""
    assert CLAIM_MARKER in MARKER_JQ
