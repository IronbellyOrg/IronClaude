"""Regression guard for the LiteLLM proxy MCP names (issue #454).

Every installed primitive that names a direct MCP tool must also name its
`mcp__litellm__` proxy twin, so a session that only has the proxy still finds the
tool. CI-safe: pure file-content assertions over the source and plugin trees.
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_ROOTS = [
    _REPO / "src" / "superclaude" / "agents",
    _REPO / "src" / "superclaude" / "skills",
    _REPO / "src" / "superclaude" / "commands",
    _REPO / "src" / "superclaude" / "core",
    _REPO / "plugins" / "superclaude",
]

_AUGGIE = "mcp__auggie__codebase-retrieval"
_AUG = "mcp__litellm__augment_code-augment_code_search"
_AUGGIE_MCP = "mcp__auggie-mcp__"
_TOOLS_LINE = re.compile(r"^\s*(?:-\s*)?(?:tools|allowed-tools)\s*:")
_TAVILY_DIRECT = re.compile(r"mcp__tavily__tavily_([a-z]+)")


def _lines():
    for root in _ROOTS:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            rel = path.relative_to(_REPO).as_posix()
            for n, line in enumerate(text.splitlines(), 1):
                yield path, f"{rel}:{n}", line


def test_auggie_lines_also_name_the_proxy_tool():
    bad = []
    for path, where, line in _lines():
        if _AUGGIE not in line:
            continue
        if path.name.startswith("freshness-") or path.name == "hooks.json":
            continue
        if _AUG not in line:
            bad.append(f"{where}: names {_AUGGIE} without {_AUG}")
        elif _TOOLS_LINE.match(line) and line.index(_AUG) > line.index(_AUGGIE):
            bad.append(f"{where}: allow-list names {_AUGGIE} before {_AUG}")
    assert not bad, "\n".join(bad)


def test_tavily_allow_lists_also_name_the_proxy_tool():
    bad = []
    for _path, where, line in _lines():
        if not _TOOLS_LINE.match(line):
            continue
        for tool in _TAVILY_DIRECT.findall(line):
            if f"mcp__litellm__Tavily-tavily_{tool}" not in line:
                bad.append(
                    f"{where}: lists mcp__tavily__tavily_{tool} without its proxy twin"
                )
    assert not bad, "\n".join(bad)


def test_auggie_mcp_prefix_only_in_hook_matchers():
    allowed = {"hooks.json", "auggie-flag-clear.sh"}
    bad = sorted(
        {
            where.rsplit(":", 1)[0]
            for path, where, line in _lines()
            if _AUGGIE_MCP in line and path.name not in allowed
        }
    )
    assert not bad, "files naming " + _AUGGIE_MCP + ": " + ", ".join(bad)


def test_guard_scans_the_expected_trees():
    assert all(root.is_dir() for root in _ROOTS)
    assert any(_AUGGIE in line for _p, _w, line in _lines())
