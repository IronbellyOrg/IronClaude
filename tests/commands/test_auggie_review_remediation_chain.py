"""Regression pins for the single `/sc:auggie-review` remediation chain.

The command, protocol and handoff ref are Markdown, so these tests pin the
literals the behavior depends on, sliced by section so a literal in the wrong
place fails. Every review `--depth` (quick, standard, deep) dispatches to ONE
chain: /sc:design -> sc:workflow (which runs its own `/sc:reflect --mode pre`)
-> user-run /sc:implement -> /sc:reflect --mode post. The removed `--depth deep`
route (task-builder -> MDTM task file -> user-run /task) must not come back in
any file of the primitive. Reads SOURCE files, not the installed or `.claude/`
copies.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src" / "superclaude"
SKILL_DIR = SRC / "skills" / "sc-auggie-review-protocol"
CMD_PATH = SRC / "commands" / "auggie-review.md"
AGENT_PATH = SRC / "agents" / "auggie-reviewer.md"
CMD = CMD_PATH.read_text(encoding="utf-8")
SKILL = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
REF = (SKILL_DIR / "refs" / "remediation-handoff.md").read_text(encoding="utf-8")


def _between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    return text[i : text.index(end, i + len(start))]


def _line(text: str, prefix: str) -> str:
    return next(ln for ln in text.splitlines() if ln.strip().startswith(prefix))


# Every place the chain is described. Looked up per test, so a moved or missing
# section fails its own test instead of breaking collection for all of them.
SURFACES = {
    "command option row": lambda: _line(CMD, "| `--remediation-offer`"),
    "command example": lambda: _between(CMD, "### Remediation chain", "## Boundaries"),
    "skill step 4": lambda: _between(
        SKILL, "4. If the user accepts", "5. Return the structured output"
    ),
    "ref offer prompt": lambda: _between(REF, "## The offer prompt", "## Phase A"),
}
CHAIN_ORDER = [
    "/sc:design",
    "sc:workflow",
    "--mode pre",
    "/sc:implement",
    "--mode post",
]


def _in_order(text: str, tokens: list[str]) -> bool:
    pos = 0
    for token in tokens:
        pos = text.find(token, pos)
        if pos < 0:
            return False
        pos += len(token)
    return True


@pytest.mark.parametrize("name", SURFACES)
def test_chain_order(name):
    assert _in_order(SURFACES[name](), CHAIN_ORDER), name


@pytest.mark.parametrize("name", SURFACES)
def test_dispatch_never_branches_on_depth(name):
    assert not re.search(r"\bdeep\b", SURFACES[name](), re.IGNORECASE), name


def test_dispatch_literals():
    step4 = SURFACES["skill step 4"]()
    assert "never `--handoff implement`" in step4
    assert "never `--handoff implement`" in REF
    for literal in (
        "Skill sc:workflow-protocol",
        "--handoff none",
        "/sc:implement <pkg>/<id>.md",
        "/sc:reflect --mode post",
        "does NOT auto-execute",
    ):
        assert literal in step4, literal


# The removed route, as markers that must not appear anywhere in the primitive.
REMOVED_ROUTE = {
    "task-builder skill": re.compile(r"task[- ]builder", re.IGNORECASE),
    "MDTM task file": re.compile(r"\bMDTM\b", re.IGNORECASE),
    "/task command": re.compile(r"(?<![\w:])/task\b"),
    "/sc:reflect --type task": re.compile(r"--type task\b"),
    "route naming": re.compile(
        r"\b(?:plan|mdtm)[ -]route\b|Route selection", re.IGNORECASE
    ),
}
# Old state-file keys may be named only to say they are ignored.
LEGACY_KEYS = re.compile(r"task_file_path|task_reflect_")


def _primitive_files() -> list[Path]:
    files = [CMD_PATH, AGENT_PATH]
    files += sorted(
        p
        for p in SKILL_DIR.rglob("*")
        if p.is_file() and p.suffix in {".md", ".json", ".yaml", ".yml"}
    )
    return files


def test_removed_deep_route_is_gone_from_the_primitive():
    offenders = []
    for path in _primitive_files():
        rel = path.relative_to(REPO_ROOT)
        for no, ln in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            offenders += [
                f"{rel}:{no} [{label}]"
                for label, rx in REMOVED_ROUTE.items()
                if rx.search(ln)
            ]
            if LEGACY_KEYS.search(ln) and "ignore" not in ln:
                offenders.append(f"{rel}:{no} [legacy key kept]")
    assert offenders == []
