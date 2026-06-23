"""C8 doc-alignment + release drift guards for the Tavily 0.2.x upgrade (H3/H4).

Scoped to ``src/superclaude`` + ``docs`` ONLY — archived/build trees (``.dev/``,
``.claude/``, ``dist/``) are excluded so stale historical pins (e.g. an archived
``tavily-mcp@0.1.2`` under ``.dev/releases/``) and the ``mcp.tavily.com`` URL do not
false-positive (reflect findings H3/H4). CI-safe: pure file-content scans.
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_ROOTS = [_REPO / "src" / "superclaude", _REPO / "docs"]
_EXCLUDE_DIRS = {
    ".dev",
    ".claude",
    "dist",
    "node_modules",
    ".venv",
    "__pycache__",
    ".git",
}
_TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".sh",
    ".cfg",
    ".ini",
    ".toml",
}

# `mcp.tavily` as a stale capability token, but NOT the `mcp.tavily.com` URL (H4).
_STALE_TOKEN_RE = re.compile(r"mcp\.tavily(?!\.com)")
_VERSION_RE = re.compile(r"tavily-mcp@([A-Za-z0-9.\-]+)")


def _iter_text_files(roots: list[Path]):
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            # Exclude only dirs UNDER the root — never match ancestor components of an
            # absolute path (the worktree itself lives under `.dev/worktrees/…`, so testing
            # `p.parts` would exclude every file and make this guard vacuous).
            if any(part in _EXCLUDE_DIRS for part in p.relative_to(root).parts):
                continue
            if p.suffix.lower() not in _TEXT_SUFFIXES:
                continue
            yield p


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def test_tavily_version_single_pin():
    """Every `tavily-mcp@<ver>` in src/ + docs/ is pinned to 0.2.20 (X1 / H3)."""
    bad = []
    for p in _iter_text_files(_ROOTS):
        for m in _VERSION_RE.finditer(_read(p)):
            if m.group(1) != "0.2.20":
                bad.append((str(p.relative_to(_REPO)), m.group(1)))
    assert not bad, f"tavily-mcp pinned to a version other than 0.2.20: {bad}"


def test_no_stale_mcp_tavily_token():
    """No stale `mcp.tavily` capability token in src/ + docs/ (X4 / H4); `mcp.tavily.com` is allowed."""
    bad = [
        str(p.relative_to(_REPO))
        for p in _iter_text_files(_ROOTS)
        if _STALE_TOKEN_RE.search(_read(p))
    ]
    assert not bad, (
        f"stale 'mcp.tavily' token (use 'mcp_server.tavily') found in: {bad}"
    )


def test_no_tavily_json_references():
    """No in-scope file references the deleted `tavily.json` config (X2)."""
    bad = []
    for p in _iter_text_files(_ROOTS):
        text = _read(p)
        if "configs/tavily.json" in text or re.search(r"\btavily\.json\b", text):
            bad.append(str(p.relative_to(_REPO)))
    assert not bad, f"reference to the deleted tavily.json found in: {bad}"


def test_docs_no_default_params_duplication():
    """docs/ POINT to MCP_Tavily.md and do not duplicate DEFAULT_PARAMETERS values (X6).

    The canonical value lives in `install_mcp.py` and `src/superclaude/mcp/MCP_Tavily.md`;
    the `docs/` tree must not restate it.
    """
    bad = []
    for p in _iter_text_files([_REPO / "docs"]):
        text = _read(p)
        if (
            '"search_depth"' in text
            or "search_depth: basic" in text
            or re.search(r"max_results['\"]?\s*[:=]\s*10", text)
        ):
            bad.append(str(p.relative_to(_REPO)))
    assert not bad, (
        f"docs duplicate DEFAULT_PARAMETERS values (should point to MCP_Tavily.md): {bad}"
    )
