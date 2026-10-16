"""Files retired by the routing consolidation stay retired and unlinked."""

from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]

_RETIRED = [
    "src/superclaude/core/ORCHESTRATOR.md",
    "src/superclaude/core/COMMANDS.md",
    "src/superclaude/core/PERSONAS.md",
    "src/superclaude/core/MODES.md",
    "src/superclaude/core/FLAGS.md",
    "src/superclaude/core/MCP.md",
    "plugins/superclaude/core/FLAGS.md",
    "docs/reference/examples-cookbook.md",
    "docs/reference/basic-examples.md",
    "docs/reference/advanced-workflows.md",
    "docs/reference/advanced-patterns.md",
    "docs/reference/integration-patterns.md",
    "docs/reference/commands-list.md",
    "docs/reference/suggested-commands.md",
    "docs/reference/comprehensive-features.md",
    "docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md",
    "docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md",
]
_LINK_RE = re.compile(r"\]\(([^)\s#]+)")


def test_retired_files_are_gone():
    present = [p for p in _RETIRED if (_REPO / p).exists()]
    assert not present, present


def test_no_markdown_link_points_at_a_retired_file():
    retired = {(_REPO / p).resolve() for p in _RETIRED}
    files = [_REPO / "README.md"]
    for root in ("src/superclaude", "plugins/superclaude", "docs"):
        files += sorted((_REPO / root).rglob("*.md"))
    bad = []
    for path in files:
        for target in _LINK_RE.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if (path.parent / target).resolve() in retired:
                bad.append(f"{path.relative_to(_REPO)} -> {target}")
    assert not bad, bad
