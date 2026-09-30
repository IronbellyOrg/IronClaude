"""Dedicated chrome-devtools MCP docs must not ship; Playwright MCP stays."""

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]


def test_chrome_devtools_mcp_docs_removed_playwright_remains():
    gone = [
        _REPO / "src/superclaude/mcp/MCP_Chrome-DevTools.md",
        _REPO / "plugins/superclaude/mcp/MCP_Chrome-DevTools.md",
    ]
    stay = [
        _REPO / "src/superclaude/mcp/MCP_Playwright.md",
        _REPO / "src/superclaude/mcp/configs/playwright.json",
        _REPO / "plugins/superclaude/mcp/MCP_Playwright.md",
        _REPO / "plugins/superclaude/mcp/configs/playwright.json",
    ]
    still_present = [str(p.relative_to(_REPO)) for p in gone if p.exists()]
    missing = [str(p.relative_to(_REPO)) for p in stay if not p.exists()]
    assert still_present == [], f"chrome-devtools MCP docs still shipped: {still_present}"
    assert missing == [], f"Playwright MCP files missing: {missing}"
