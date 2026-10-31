"""Drift guards for the shared codegraph guide `core/CODEGRAPH.md` (issue #323, Phase 3).

The guide is installed to `~/.claude/CODEGRAPH.md` and is the one place that holds
the codegraph usage rules; primitives carry a single lookup line. These tests pin
its size, its closed vocabulary, the version pin shared with the Phase 2
installer, the confinement of banned verbs to its "Never" section, its byte-identical
plugin copy, and that no other primitive copies its rules (sentinel sentence).
CI-safe: pure file-content assertions, no network, no codegraph binary.
"""

import filecmp
import re
from pathlib import Path

from superclaude.cli.install_codegraph import VERSION

_REPO = Path(__file__).resolve().parents[2]
_GUIDE = _REPO / "src" / "superclaude" / "core" / "CODEGRAPH.md"
_PLUGIN_GUIDE = _REPO / "plugins" / "superclaude" / "core" / "CODEGRAPH.md"

_TOOLS = ["node", "search", "callers", "callees", "impact", "files", "status"]
_TOKENS = [
    "graph:absent",
    "graph:unlisted",
    "graph:disabled",
    "graph:not_initialized",
    "graph:foreign_index",
    "graph:stale",
    "graph:version_mismatch",
    "graph:provenance_unproven",
    "graph:empty",
    "graph:ambiguous",
    "graph:truncated",
    "graph:parse_failed",
    "graph:unresolved",
    "graph:telemetry_on",
]
_SENTINEL = "Caller rows give the caller's definition line, not the call site."
_BANNED_OUTSIDE_NEVER = re.compile(
    r"explore|codegraph (?:index|sync|uninit|unlock|upgrade|install|uninstall)\b"
)


def _text() -> str:
    return _GUIDE.read_text(encoding="utf-8")


def _split_never(text: str) -> tuple[str, str]:
    parts = re.split(r"^## \d+\. Never\b.*$", text, maxsplit=1, flags=re.M)
    assert len(parts) == 2, "CODEGRAPH.md has no '## N. Never' section"
    return parts[0], parts[1]


def test_guide_exists_and_is_short():
    assert _GUIDE.is_file(), "src/superclaude/core/CODEGRAPH.md is missing"
    assert len(_text().splitlines()) <= 120, "CODEGRAPH.md is over 120 lines"


def test_guide_has_seven_sections():
    headings = re.findall(r"^## (\d+)\. ", _text(), flags=re.M)
    assert headings == [str(n) for n in range(1, 8)], headings


def test_guide_names_seven_tools_and_closed_token_list():
    text = _text()
    for tool in _TOOLS:
        assert f"codegraph_{tool}" in text, f"guide does not name codegraph_{tool}"
    for token in _TOKENS:
        assert token in text, f"guide does not name {token}"
    found = set(re.findall(r"graph:[a-z_]+", text))
    assert found == set(_TOKENS), f"tokens outside the closed list: {found - set(_TOKENS)}"


def test_guide_fixed_lines_and_pin_parity():
    text = _text()
    pin = re.search(r"^Pinned codegraph version: (\S+)$", text, flags=re.M)
    assert pin, "guide lacks the 'Pinned codegraph version:' line"
    assert pin.group(1) == VERSION, f"guide pin {pin.group(1)} != installer VERSION {VERSION}"
    assert re.search(
        r"^Freshness experiment E-1: (pending|outcome-A|outcome-B)$", text, flags=re.M
    ), "guide lacks the 'Freshness experiment E-1:' line"


def test_banned_names_only_in_never_section():
    before, never = _split_never(_text())
    hits = _BANNED_OUTSIDE_NEVER.findall(before)
    assert not hits, f"explore or a mutating verb named outside 'Never': {hits}"
    assert "explore" in never
    for verb in ("index", "sync", "uninit", "unlock", "upgrade", "install", "uninstall"):
        assert f"codegraph {verb}" in never, f"'Never' does not name codegraph {verb}"


def test_guide_names_switches_and_status_guard():
    text = _text()
    assert "SUPERCLAUDE_CODEGRAPH_PRIMITIVES" in text
    assert "SUPERCLAUDE_CODEGRAPH_AUTOINIT" in text
    assert "pgrep -f" in text


def test_guide_holds_sentinel_and_no_source_path():
    text = _text()
    assert _SENTINEL in text
    assert "src/superclaude/" not in text, "installed guide must not name a src/ path"


def test_not_initialized_message_names_graph_status():
    line = next(
        (ln for ln in _text().splitlines() if "graph:not_initialized" in ln and "tell the user" in ln),
        "",
    )
    assert "/sc:graph status" in line, "graph:not_initialized message must name /sc:graph status"


def test_plugin_copy_is_byte_identical():
    assert _PLUGIN_GUIDE.is_file(), "plugins/superclaude/core/CODEGRAPH.md is missing"
    assert filecmp.cmp(_GUIDE, _PLUGIN_GUIDE, shallow=False)


def test_sentinel_only_in_the_guide():
    roots = [
        _REPO / "src" / "superclaude" / d for d in ("commands", "skills", "agents", "core", "modes")
    ] + [_REPO / "plugins" / "superclaude"]
    allowed = {_GUIDE.resolve(), _PLUGIN_GUIDE.resolve()}
    offenders = [
        str(p.relative_to(_REPO))
        for root in roots
        for p in root.rglob("*.md")
        if p.resolve() not in allowed and _SENTINEL in p.read_text(encoding="utf-8")
    ]
    assert not offenders, f"guide rules copied into: {offenders}"
