"""L3 §6.1.1 no-mutation denylist guard (source-text, falsifier-disciplined).

Reads the SOURCE SKILL.md (never the ``.claude/`` mirror, per SoT discipline),
extracts the §6.1.1 ``No-mutation gate.`` denylist sentence via a stable
heading-anchored regex, and asserts the read-but-forbidden working-tree git
verbs are enumerated as a defense-in-depth backstop, while the pre-existing
entries (``git commit``/``git push``, ``pip install``, ``rm``) are retained.

L3 is defense-in-depth: control (b)'s allowlist already rejects every git verb
(closed set, ``git`` absent), and §6.1.1 governs the ``execute_shell_command``/
serena path, NOT the Bash-tool/L1 incident vector. This test guards the
denylist TEXT (there is no ``verify`` subcommand to exercise the gate at runtime).

Falsifier discipline: fails-before (the git verbs were absent from the denylist)
and passes-after (the L3 enumeration landed).
"""

from __future__ import annotations

import re
from pathlib import Path

# Repo root = four parents up from this file (tests/cli/reflect/<file>).
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SKILL_SRC = _REPO_ROOT / "src/superclaude/skills/sc-reflect-protocol/SKILL.md"

# Anchor on the bold "No-mutation gate." lead and bound at the end of its
# paragraph (the next blank line), so unrelated prose never false-positives.
_NO_MUTATION_GATE_RE = re.compile(
    r"\*\*No-mutation gate\.\*\*(.*?)(?:\n\n|\n#)", re.DOTALL
)

# The read-but-forbidden working-tree git verbs L3 enumerates as a backstop.
_REQUIRED_GIT_VERBS = (
    "git reset",
    "git stash",
    "git checkout",
    "git clean",
    "git rebase",
    "git merge",
    "git worktree",
    "git restore",
)
# Pre-existing denylist entries that MUST be retained.
_RETAINED_ENTRIES = ("git commit", "git push", "pip install", "rm")


def _no_mutation_gate_text() -> str:
    src = _SKILL_SRC.read_text(encoding="utf-8")
    m = _NO_MUTATION_GATE_RE.search(src)
    assert m is not None, "§6.1.1 No-mutation gate paragraph not found in SKILL.md"
    return m.group(1)


def test_denylist_enumerates_all_read_but_forbidden_git_verbs() -> None:
    gate = _no_mutation_gate_text()
    missing = [verb for verb in _REQUIRED_GIT_VERBS if verb not in gate]
    assert missing == [], (
        f"§6.1.1 no-mutation denylist must enumerate every git verb; missing: {missing}"
    )


def test_denylist_retains_preexisting_entries() -> None:
    gate = _no_mutation_gate_text()
    missing = [entry for entry in _RETAINED_ENTRIES if entry not in gate]
    assert missing == [], (
        f"§6.1.1 no-mutation denylist dropped pre-existing entries: {missing}"
    )


def test_denylist_framed_as_defense_in_depth() -> None:
    """L3 must NOT overstate: the git enumeration is a defense-in-depth backstop,
    not the closure of the Bash-tool/L1 incident vector."""
    gate = _no_mutation_gate_text()
    assert "defense-in-depth" in gate.lower()
    assert "backstop" in gate.lower()
