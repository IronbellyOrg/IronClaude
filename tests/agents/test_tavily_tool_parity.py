"""Frontmatter↔prose Tavily tool-parity drift guards (Clusters C2 + C6, invariants X7 + X5).

Per reflect finding H1, the parity glob covers BOTH ``src/superclaude/agents/**/*.md`` and
``src/superclaude/skills/**/*.md`` and parses BOTH the ``tools:`` (YAML list) and
``allowed-tools:`` (inline comma list) frontmatter keys — so ``sc-recommend`` is in scope.

Parity semantics (faithful to X7 without false-failing the no-change consumers):
- Only files declaring a tool surface (``tools:`` or ``allowed-tools:``) are checked; narrative
  reference docs (e.g. ``refs/*.md``) with no tool-surface key are skipped.
- Universal direction — ``referenced ⊆ declared``: a file may not reference a ``mcp__tavily__*``
  tool in prose without declaring it in frontmatter.
- Bidirectional direction — for files that DOCUMENT a Tavily tool in prose (≥1 full id in the
  body), ``declared == referenced`` exactly. Files that mention Tavily only generically
  (``sc-recommend``, ``sc-reflect`` pre-edit) have an empty referenced set and are exempt from
  the equality, which is the intended behavior (they inherit, they do not document the surface).

All assertions read real file content; CI-safe (no network).
"""

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_AGENTS_DIR = _REPO_ROOT / "src" / "superclaude" / "agents"
_SKILLS_DIR = _REPO_ROOT / "src" / "superclaude" / "skills"

_TAVILY_ID = re.compile(r"mcp__(?:tavily__tavily|litellm__Tavily-tavily)_[a-z]+")
_TOOL_ENTRY = re.compile(r"mcp__[A-Za-z0-9_-]+")
_TOOL_SURFACE_KEY = re.compile(r"^\s*(tools|allowed-tools):", re.MULTILINE)


def _md_files() -> list[Path]:
    files: list[Path] = []
    for root in (_AGENTS_DIR, _SKILLS_DIR):
        files.extend(sorted(root.rglob("*.md")))
    return files


def _split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body). If no leading frontmatter block, ('', text)."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def test_prose_tavily_ids_are_declared():
    """referenced ⊆ declared — no file uses a Tavily tool it did not declare (X7)."""
    files = _md_files()
    assert files, "parity guard scanned 0 .md files (vacuous; M1)"
    violations = []
    for f in files:
        fm, body = _split_frontmatter(f.read_text(encoding="utf-8"))
        if not _TOOL_SURFACE_KEY.search(fm):
            continue
        declared = set(_TAVILY_ID.findall(fm))
        referenced = set(_TAVILY_ID.findall(body))
        undeclared = referenced - declared
        if undeclared:
            violations.append((str(f.relative_to(_REPO_ROOT)), sorted(undeclared)))
    assert not violations, f"prose references undeclared Tavily tools: {violations}"


def test_documenting_files_have_exact_parity():
    """declared == referenced for files that document Tavily tools in prose (X7 bidirectional)."""
    files = _md_files()
    assert files, "parity guard scanned 0 .md files (vacuous; M1)"
    mismatches = []
    for f in files:
        fm, body = _split_frontmatter(f.read_text(encoding="utf-8"))
        if not _TOOL_SURFACE_KEY.search(fm):
            continue
        declared = set(_TAVILY_ID.findall(fm))
        referenced = set(_TAVILY_ID.findall(body))
        if referenced and declared != referenced:
            mismatches.append(
                {
                    "file": str(f.relative_to(_REPO_ROOT)),
                    "declared": sorted(declared),
                    "referenced": sorted(referenced),
                }
            )
    assert not mismatches, f"frontmatter↔prose Tavily parity mismatch: {mismatches}"


def _declared_tools(fm: str) -> list[str]:
    """Ordered tool ids from a ``tools:`` / ``allowed-tools:`` value, YAML list or inline list."""
    tools: list[str] = []
    in_list = False
    for line in fm.splitlines():
        key = _TOOL_SURFACE_KEY.match(line)
        if key:
            tools.extend(_TOOL_ENTRY.findall(line[key.end() :]))
            in_list = True
        elif in_list and line.lstrip().startswith("- "):
            tools.extend(_TOOL_ENTRY.findall(line.split("#", 1)[0]))
        else:
            in_list = False
    return tools


def test_proxy_tavily_listed_before_direct_twin():
    """Issue #454: each agent's declared direct Tavily tool has its LiteLLM proxy twin just before it."""
    checked, missing = 0, []
    for f in sorted(_AGENTS_DIR.rglob("*.md")):
        fm, _ = _split_frontmatter(f.read_text(encoding="utf-8"))
        tools = _declared_tools(fm)
        for i, tool in enumerate(tools):
            if tool.startswith("mcp__tavily__tavily_"):
                checked += 1
                twin = tool.replace("mcp__tavily__", "mcp__litellm__Tavily-", 1)
                if i == 0 or tools[i - 1] != twin:
                    missing.append((str(f.relative_to(_REPO_ROOT)), tool))
    assert checked, "proxy-twin guard found 0 direct Tavily tools (vacuous; M1)"
    assert not missing, (
        f"direct Tavily tool without its proxy twin right before it: {missing}"
    )


def test_declared_tools_parses_list_and_inline_forms():
    yaml_list = "tools:\n  - Read\n  - mcp__a__x    # note\n  - mcp__b__y\nmodel: x\n- mcp__c__z\n"
    assert _declared_tools(yaml_list) == ["mcp__a__x", "mcp__b__y"]
    assert _declared_tools("allowed-tools: Read, mcp__a__x, mcp__b__y\n") == [
        "mcp__a__x",
        "mcp__b__y",
    ]


def test_rf_no_map_crawl():
    """X5 guard — no rf-* agent references map/crawl (confined to the research engine)."""
    rf_files = sorted(_AGENTS_DIR.glob("rf-*.md"))
    assert rf_files, "X5 guard found 0 rf-* agents (vacuous; M1)"
    offenders = []
    for f in rf_files:
        text = f.read_text(encoding="utf-8")
        if "tavily-map" in text or "tavily-crawl" in text:
            offenders.append(f.name)
    assert not offenders, f"rf-* agents must not reference map/crawl (X5): {offenders}"


def test_rf_fallback_provenance_present():
    """Each rf-* agent retains a Tavily-first + fallback-provenance form."""
    missing = []
    rf_files = sorted(_AGENTS_DIR.glob("rf-*.md"))
    assert rf_files, "expected rf-* agent files to exist"
    for f in rf_files:
        text = f.read_text(encoding="utf-8")
        has_tavily = "mcp__tavily__tavily_search" in text
        has_provenance = (
            "Tavily-first" in text
            and "fallback" in text.lower()
            and "WebSearch" in text
        )
        if not (has_tavily and has_provenance):
            missing.append(f.name)
    assert not missing, (
        f"rf-* agents missing Tavily-first/fallback provenance: {missing}"
    )
