"""The plugin copy of sc-recommend mirrors src, plus the routing guide.

Plugin installs never receive core/ files, so the guide ships inside the
plugin's sc-recommend skill as refs/HOW-WE-WORK.md. Every other file in the
plugin skill must be a byte copy of src; src must not carry its own guide copy.
"""

from __future__ import annotations

import filecmp
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SRC_SKILL = _REPO / "src/superclaude/skills/sc-recommend"
_PLUG_SKILL = _REPO / "plugins/superclaude/skills/sc-recommend"
_GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"


def _rels(root: Path) -> set[str]:
    return {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.name != "__init__.py"
    }


def test_sc_recommend_plugin_tree_mirrors_src_plus_guide():
    src, plug = _rels(_SRC_SKILL), _rels(_PLUG_SKILL)
    assert "refs/HOW-WE-WORK.md" not in src
    assert plug - src == {"refs/HOW-WE-WORK.md"}
    assert src <= plug, src - plug
    _, mismatch, errors = filecmp.cmpfiles(
        _SRC_SKILL, _PLUG_SKILL, sorted(src), shallow=False
    )
    assert not mismatch and not errors, mismatch + errors
    assert filecmp.cmp(_GUIDE, _PLUG_SKILL / "refs/HOW-WE-WORK.md", shallow=False)
