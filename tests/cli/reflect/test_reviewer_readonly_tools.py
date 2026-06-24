"""L1 + L5-static reviewer read-only ``tools:`` allowlist guard.

Static guard for the reflect-reviewer agent (L1). Reads the SOURCE agent file
``src/superclaude/agents/reflect-reviewer.md`` (never the ``.claude/`` mirror, per
SoT discipline) and asserts its ``tools:`` allowlist is present, non-empty,
contains the read-only core (Read/Grep/Glob), and intersects the mutator set
{Bash, Edit, Write, NotebookEdit, Task, execute_shell_command} EMPTY.

A negative fixture (a reviewer persona with the ``tools:`` line stripped, under
``tests/cli/reflect/fixtures/reviewer-personas/``) proves the SAME guard helper
FLAGS a stripped line -- not just the happy path. This is the L5-static half;
the L5-dynamic no-mutation ledger test is deferred (producer absent).

Falsifier discipline: fails-before (``reflect-reviewer.md`` absent or its
``tools:`` line stripped) and passes-after (the read-only allowlist landed).
"""

from __future__ import annotations

import re
from pathlib import Path

# Repo root = four parents up from this file (tests/cli/reflect/<file>).
_REPO_ROOT = Path(__file__).resolve().parents[3]
_AGENT_SRC = _REPO_ROOT / "src/superclaude/agents/reflect-reviewer.md"
_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "reviewer-personas"
_NO_TOOLS_FIXTURE = _FIXTURE_DIR / "reviewer-persona-no-tools.md"

# Mutator tools that MUST NOT appear in a read-only reviewer allowlist.
_MUTATORS = frozenset(
    {"Bash", "Edit", "Write", "NotebookEdit", "Task", "execute_shell_command"}
)
# Read-only core that MUST be present.
_REQUIRED_READONLY = frozenset({"Read", "Grep", "Glob"})

# Anchored on the frontmatter ``tools:`` line (line start) within the YAML
# frontmatter block ONLY, so body prose mentioning "tools" never false-positives.
_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_TOOLS_LINE_RE = re.compile(r"^tools:[ \t]*(.*)$", re.MULTILINE)


def _frontmatter(text: str) -> str:
    m = _FRONTMATTER_RE.search(text)
    assert m is not None, "agent file has no YAML frontmatter block"
    return m.group(1)


def _parse_tools(text: str) -> list[str] | None:
    """Return the parsed tools list, or None if the frontmatter has no
    non-empty ``tools:`` line (i.e. the agent inherits ALL tools -- unsafe)."""
    fm = _frontmatter(text)
    m = _TOOLS_LINE_RE.search(fm)
    if m is None:
        return None
    raw = m.group(1).strip()
    if not raw:
        return None
    return [t.strip() for t in raw.split(",") if t.strip()]


def _is_readonly_safe(tools: list[str] | None) -> bool:
    """A reviewer tool set is read-only-safe iff it is present, non-empty,
    contains the read-only core, and names no mutator."""
    if not tools:
        return False
    if not _REQUIRED_READONLY.issubset(set(tools)):
        return False
    return not (_MUTATORS & set(tools))


def test_reflect_reviewer_tools_line_present_and_nonempty() -> None:
    """(a) the ``tools:`` line is PRESENT and NON-EMPTY."""
    text = _AGENT_SRC.read_text(encoding="utf-8")
    tools = _parse_tools(text)
    assert tools is not None and len(tools) > 0, (
        "reflect-reviewer.md must carry a non-empty `tools:` allowlist"
    )


def test_reflect_reviewer_tools_excludes_all_mutators() -> None:
    """(b) parsed tool set ∩ mutators == ∅."""
    text = _AGENT_SRC.read_text(encoding="utf-8")
    tools = _parse_tools(text)
    assert tools is not None
    intersection = _MUTATORS & set(tools)
    assert intersection == set(), (
        f"reflect-reviewer.md `tools:` must exclude every mutator; found {intersection}"
    )


def test_reflect_reviewer_tools_includes_readonly_core() -> None:
    """(c) the read-only tools Read, Grep, Glob are PRESENT."""
    text = _AGENT_SRC.read_text(encoding="utf-8")
    tools = _parse_tools(text)
    assert tools is not None
    missing = _REQUIRED_READONLY - set(tools)
    assert missing == set(), (
        f"reflect-reviewer.md `tools:` missing read-only core: {missing}"
    )


def test_reflect_reviewer_is_readonly_safe() -> None:
    """Composite: reflect-reviewer.md is read-only-safe by the guard helper."""
    text = _AGENT_SRC.read_text(encoding="utf-8")
    assert _is_readonly_safe(_parse_tools(text)) is True


def test_guard_flags_stripped_tools_line_fixture() -> None:
    """(d) the SAME guard helper FLAGS a reviewer persona whose ``tools:`` line
    was stripped -- proving it catches a stripped line, not just the happy path."""
    text = _NO_TOOLS_FIXTURE.read_text(encoding="utf-8")
    assert _parse_tools(text) is None, (
        "stripped-tools fixture should parse to None (no tools line)"
    )
    assert _is_readonly_safe(_parse_tools(text)) is False, (
        "guard must flag a stripped-tools persona as NOT read-only-safe"
    )
