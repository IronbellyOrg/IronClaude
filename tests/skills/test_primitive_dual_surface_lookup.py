"""Drift guard: primitives that look up another installed primitive must accept BOTH surfaces.

A skill or agent can live at ``~/.claude/...`` (``superclaude install``) or at the project's
``.claude/...`` (``make sync-dev`` in a dev checkout). PR #278 first rewrote ``src/superclaude/...``
paths to a home-only path, which broke dev checkouts. Skills and agents resolve in opposite
orders (personal skill beats project skill; project agent beats user agent), so the rf-qa lookup
must name the project copy first. CI-safe, no network.
"""

import re
from pathlib import Path

_SKILLS = Path(__file__).resolve().parents[2] / "src" / "superclaude" / "skills"
_ADV_HOME = "~/.claude/skills/sc-adversarial-protocol/SKILL.md"
_ADV_PROJECT = re.compile(r"(?<!~/)\.claude/skills/sc-adversarial-protocol/SKILL\.md")
_ADV_SITES = [
    "sc-brainstorm-protocol/SKILL.md",
    "sc-release-split-protocol/SKILL.md",
    "sc-roadmap-protocol/SKILL.md",
    "sc-roadmap-protocol/refs/adversarial-integration.md",
]


def _lines(rel: str) -> list[str]:
    return (_SKILLS / rel).read_text(encoding="utf-8").splitlines()


def test_adversarial_prerequisite_checks_accept_both_surfaces():
    for rel in _ADV_SITES:
        hits = [ln for ln in _lines(rel) if _ADV_HOME in ln]
        assert hits, f"{rel}: expected the adversarial prerequisite check"
        for ln in hits:
            assert _ADV_PROJECT.search(ln), (
                f"{rel}: home-only check: {ln.strip()[:120]}"
            )


def test_persona_check_accepts_both_surfaces():
    (line,) = [
        ln
        for ln in _lines("sc-brainstorm-protocol/refs/agent-spec-builder.md")
        if ln.startswith("**Persona availability**")
    ]
    assert (
        re.search(r"(?<!~/)\.claude/agents/<persona>\.md", line)
        and "~/.claude/agents/<persona>.md" in line
    )


def test_rf_qa_lookup_is_project_first():
    (line,) = [
        ln
        for ln in _lines("task-builder/SKILL.md")
        if ln.startswith("1. **Locate `rf-qa.md`.**")
    ]
    project = re.search(r"(?<!~/)\.claude/agents/rf-qa\.md", line)
    home = line.find("~/.claude/agents/rf-qa.md")
    assert project and home != -1, "both rf-qa surfaces must be named"
    assert project.start() < home, (
        "project copy must be read first (project agent beats user agent)"
    )
    assert "authoritative" not in line
