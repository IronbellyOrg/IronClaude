"""Working-tree questions never reach Augment; absence needs a cited Grep or Read.

Hosted Augment indexes the default branch only, so consumers that ground claims about the
working tree must not call it, and every consumer that can call it carries the absence
sentence verbatim. Spec: .dev/brainstorms/20261019-204829-stale-augment-grounding.
Files owned by the auggie-review rework (auggie-reviewer, sc-auggie-review-protocol,
commands/auggie-review.md) are excluded here.
"""

import re
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src" / "superclaude"
_ALIAS = re.compile(r"mcp__auggie[\w-]*__[\w-]+|augment_code_search|\bcodebase-retrieval\b")
SHORT = (
    "A miss from Augment (default branch only), Serena (exact symbols only) or any index never"
    " proves absence. Before claiming something is missing, unimplemented, unused or uncalled,"
    " check the diff for a renamed equivalent, then Grep or Read the working tree and cite the"
    " pattern and root searched. Read every hit before citing it: a hit whose file or"
    " identifier is gone was deleted or renamed here."
)
DONOT = "Do not use `augment_code_search` for questions about this working tree."
_OWNED = ("agents/auggie-reviewer.md", "skills/sc-auggie-review-protocol/", "commands/auggie-review.md")
_FRONTMATTER_KEY = re.compile(r"^(tools|allowed-tools|mcp-servers):(.*)$", re.M)


def _rel(path: Path) -> str:
    return path.relative_to(_SRC).as_posix()


def _frontmatter(text: str) -> str:
    parts = text.split("\n---", 1)
    return parts[0] if text.startswith("---") and len(parts) == 2 else ""


def _names_augment(text: str) -> bool:
    return any(
        "auggie" in v or _ALIAS.search(v) for _, v in _FRONTMATTER_KEY.findall(_frontmatter(text))
    )


def _missing_short(paths) -> list[str]:
    return [str(p) for p in paths if SHORT not in p.read_text(encoding="utf-8")]


def _working_tree_consumers() -> list[Path]:
    trouble = sorted((_SRC / "skills" / "sc-troubleshoot-protocol").rglob("*.md"))
    return trouble + [
        _SRC / "commands" / "troubleshoot.md",
        _SRC / "agents" / "reflect-reviewer.md",
        _SRC / "agents" / "eval-docs-loader.md",
    ]


def test_working_tree_consumers_never_name_augment() -> None:
    bad = {}
    for path in _working_tree_consumers():
        # The R-9 brief line names the tool only to forbid it.
        text = path.read_text(encoding="utf-8").replace(DONOT, "")
        hits = set(_ALIAS.findall(text))
        if hits:
            bad[_rel(path)] = hits
    assert not bad, bad


def test_every_augment_consumer_carries_the_absence_sentence() -> None:
    files = [
        p
        for d in ("skills", "agents", "commands")
        for p in sorted((_SRC / d).rglob("*.md"))
        if not any(o in _rel(p) for o in _OWNED) and _names_augment(p.read_text(encoding="utf-8"))
    ]
    assert files, "frontmatter scan found no Augment consumer"
    assert not _missing_short(files + [_SRC / "agents" / "reflect-reviewer.md"])


def test_spawn_briefs_forbid_augment_for_the_working_tree() -> None:
    reflect = (_SRC / "skills" / "sc-reflect-protocol" / "SKILL.md").read_text(encoding="utf-8")
    trouble = (_SRC / "skills" / "sc-troubleshoot-protocol" / "SKILL.md").read_text(encoding="utf-8")
    assert SHORT in reflect and DONOT in reflect
    # Wave 1.7, Wave 3 and Wave 4 briefs.
    assert trouble.count(DONOT) >= 3 and trouble.count(SHORT) >= 3


def test_checker_flags_a_consumer_without_the_sentence(tmp_path) -> None:
    good = tmp_path / "good.md"
    bad = tmp_path / "bad.md"
    good.write_text(f"---\ntools: Read, mcp__auggie__augment_code_search\n---\n{SHORT}\n")
    bad.write_text("---\ntools: Read, mcp__auggie__augment_code_search\n---\nbody\n")
    assert _names_augment(bad.read_text()) and not _names_augment("---\ntools: Read\n---\n")
    assert _missing_short([good, bad]) == [str(bad)]


def test_core_claude_routes_existence_to_grep_and_states_absence_rule() -> None:
    text = (_SRC / "core" / "CLAUDE.md").read_text(encoding="utf-8")
    rows = [line for line in text.splitlines() if line.startswith("|")]
    assert not [r for r in rows if "anywhere" in r and _ALIAS.search(r)]
    assert f"**Absence claims.** {SHORT}" in text
    assert not re.search(r"\bcodebase-retrieval\b", text)


def test_no_codebase_memory_tools_or_mcp_servers_in_components() -> None:
    bad = [
        _rel(p)
        for d in ("skills", "agents", "commands")
        for p in (_SRC / d).rglob("*.md")
        if "mcp__codebase-memory-mcp__" in (t := p.read_text(encoding="utf-8")) or "mcpServers:" in t
    ]
    assert not bad, bad


def test_diagnosability_audit_has_no_augment_procedure() -> None:
    text = (_SRC / "skills" / "sc-troubleshoot-protocol" / "refs" / "diagnosability-audit.md").read_text(
        encoding="utf-8"
    )
    assert not _ALIAS.search(text)
    s10 = [line for line in text.splitlines() if "S10" in line and "insufficient" in line]
    assert s10 and all("Read" in line for line in s10)


def test_reflect_counts_in_scope_untracked_as_dirty() -> None:
    text = (_SRC / "skills" / "sc-reflect-protocol" / "SKILL.md").read_text(encoding="utf-8")
    assert "Untracked entries do not count" not in text


def test_mcp_auggie_carries_the_scope_contract() -> None:
    text = " ".join((_SRC / "mcp" / "MCP_Auggie.md").read_text(encoding="utf-8").split())
    assert "`augment_code_search` answers one question: what exists on `<default-branch>`." in text
    assert "A miss is never evidence of absence, on any branch." in text
    assert "[BRANCH_NOT_FOUND]" in text and "[REPO_NOT_FOUND]" in text
