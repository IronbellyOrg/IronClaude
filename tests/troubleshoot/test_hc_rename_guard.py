"""HC-rename guard — R-17 regression test. Harness §3 extra / P25."""

from __future__ import annotations

from pathlib import Path

from tests.troubleshoot._procedures import hc_rename_hits

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "src/superclaude/skills/sc-troubleshoot-protocol"
REFS = SKILL / "refs"


def test_no_h_tokens_outside_allow_list() -> None:
    """R-17/D11: no bare H0-H5 tokens outside the allow-list lines."""
    paths = [SKILL / "SKILL.md", *REFS.glob("*.md"), *REFS.glob("probe-packs/*.md")]
    hits = hc_rename_hits(paths)
    assert hits == [], hits
