"""Every gateway MCP tool name used by a shipped consumer must exist on the gateway.

Tavily, Context7 and Augment are served by the LiteLLM MCP gateway. Claude Code exposes
them as ``mcp__<registration>__<tool>``. An agent ``tools:`` list or skill ``allowed-tools:``
naming a tool the gateway does not serve silently loses that tool, with no error. This guard
checks every such token in ``src/superclaude`` and ``plugins/superclaude`` against the
discovery snapshot in ``tests/fixtures/mcp_gateway_tools.json``.

``tests/`` is not scanned: the coverage-gate tests use synthetic tool names on purpose.
"""

import json
import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_FIXTURE = _REPO_ROOT / "tests" / "fixtures" / "mcp_gateway_tools.json"
_SCAN_ROOTS = (_REPO_ROOT / "src" / "superclaude", _REPO_ROOT / "plugins" / "superclaude")
_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".sh", ".js"}
# A trailing `*` (shell case pattern) or `.` + `*` (regex matcher) is a prefix match, not a tool.
_TOKEN = re.compile(r"mcp__(tavily|context7|auggie|auggie-mcp)__([A-Za-z0-9_-]+)(?![A-Za-z0-9_*-])")


# The local Auggie tool name, retired with the gateway. Prose that still tells the model to
# call it points at nothing, even without the mcp__ prefix.
_RETIRED = re.compile(r"(?<![A-Za-z0-9_-])codebase-retrieval(?![A-Za-z0-9_-])")


def _known_tokens() -> set[str]:
    servers = json.loads(_FIXTURE.read_text())["servers"]
    return {f"mcp__{name}__{tool}" for name, row in servers.items() for tool in row["tools"]}


def _unknown_tokens(text: str, known: set[str]) -> set[str]:
    found = {m.group(0) for m in _TOKEN.finditer(text)} - known
    return found | ({"codebase-retrieval"} if _RETIRED.search(text) else set())


def test_fixture_has_the_three_gateway_servers() -> None:
    servers = json.loads(_FIXTURE.read_text())["servers"]
    assert {name: row["alias"] for name, row in servers.items()} == {
        "tavily": "tavily",
        "context7": "context7",
        "auggie": "augment_code",
    }
    assert all(row["tools"] for row in servers.values())


def test_every_consumer_token_exists_on_the_gateway() -> None:
    known = _known_tokens()
    bad: dict[str, set[str]] = {}
    for root in _SCAN_ROOTS:
        for path in root.rglob("*"):
            if path.suffix not in _SUFFIXES or "__pycache__" in path.parts or not path.is_file():
                continue
            unknown = _unknown_tokens(path.read_text(encoding="utf-8", errors="replace"), known)
            if unknown:
                bad[str(path.relative_to(_REPO_ROOT))] = unknown
    assert not bad, f"tools not served by the gateway: {bad}"


def _scanned_files():
    for root in _SCAN_ROOTS:
        for path in root.rglob("*"):
            if path.suffix in _SUFFIXES and "__pycache__" not in path.parts and path.is_file():
                yield path, path.read_text(encoding="utf-8", errors="replace")


def test_crash_recovery_does_not_call_augment() -> None:
    crash = _REPO_ROOT / "src" / "superclaude" / "skills" / "sc-crash-recovery"
    bad = [str(p) for p, text in _scanned_files() if crash in p.parents and "augment_code_search" in text]
    assert not bad, bad


def test_codebase_memory_only_as_auggie_review_hint() -> None:
    # Its index lags the working tree, so it may only supply caller hints in
    # /sc:auggie-review (through its own scout agent), never tools or grounding.
    review = _REPO_ROOT / "src" / "superclaude" / "skills" / "sc-auggie-review-protocol" / "SKILL.md"
    bad = [str(p) for p, text in _scanned_files() if "codebase-memory" in text and p != review]
    assert not bad, bad
    assert "mcp__codebase-memory" not in review.read_text(encoding="utf-8")


def test_no_local_auggie_call_args() -> None:
    bad = [
        str(p)
        for p, text in _scanned_files()
        if "directory_path" in text or "information_request" in text
    ]
    assert not bad, bad


def test_stale_token_is_caught() -> None:
    known = _known_tokens()
    text = "tools: Read, mcp__auggie__codebase-retrieval, mcp__tavily__tavily_search"
    assert _unknown_tokens(text, known) == {"mcp__auggie__codebase-retrieval"}
    assert _unknown_tokens("call auggie codebase-retrieval first", known) == {"codebase-retrieval"}
    assert _unknown_tokens("matcher: mcp__auggie__.* and case mcp__auggie__*)", known) == set()
