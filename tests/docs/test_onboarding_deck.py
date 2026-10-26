"""The onboarding deck names only commands and flags the routing guide states."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_DECK = _REPO / "docs/onboarding/ironclaude-onboarding.html"
_GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"
_RECOMMEND = _REPO / "src/superclaude/commands/recommend.md"

# Flags the guide does not state but another source owns: flag -> source file.
_FLAG_SOURCES = {"--plugin": _RECOMMEND}

# A slash command starts the text or follows whitespace, an opening bracket or a
# quote, so paths such as `.dev/tasks/to-do/<id>/<id>.md` are not commands.
_COMMAND_RE = re.compile(
    r"(?:^|(?<=[\s(\[{\"'`]))(/[a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)?)"
)
_FLAG_RE = re.compile(r"(?:^|(?<=[\s(\[{\"'`]))(--[a-z][a-z0-9-]*)")
_FOOTER_RE = re.compile(r"Built from HOW-WE-WORK\.md at commit [0-9a-f]{7,40}\b")

# Elements whose text is a claim: inline code, and the text inside SVG diagrams.
_CLAIM_TAGS = {"code", "text", "title", "desc"}


class _ClaimText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.texts: list[str] = []
        self._depth = 0
        self._svg = 0
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "svg":
            self._svg += 1
        # The page <title> is not a claim; only <title> inside an <svg> is.
        if tag in _CLAIM_TAGS and (tag != "title" or self._svg):
            self._depth += 1

    def handle_endtag(self, tag):
        if tag in _CLAIM_TAGS and self._depth and (tag != "title" or self._svg):
            self._depth -= 1
            if not self._depth:
                self.texts.append("".join(self._buf))
                self._buf = []
        if tag == "svg" and self._svg:
            self._svg -= 1

    def handle_data(self, data):
        if self._depth:
            self._buf.append(data)


def _claim_texts(html: str) -> list[str]:
    parser = _ClaimText()
    parser.feed(html)
    return parser.texts


def _has_token(token: str, text: str) -> bool:
    # Whole token: `/task` is not satisfied by `/task-builder`.
    return re.search(r"(?<![\w/-])" + re.escape(token) + r"(?![\w-])", text) is not None


def _unknown_tokens(html: str, guide: str) -> list[str]:
    tokens = set()
    for text in _claim_texts(html):
        tokens.update(_COMMAND_RE.findall(text))
        tokens.update(_FLAG_RE.findall(text))
    unknown = []
    for token in sorted(tokens):
        source = _FLAG_SOURCES.get(token)
        source_text = source.read_text(encoding="utf-8") if source else guide
        if not _has_token(token, source_text):
            unknown.append(token)
    return unknown


def test_every_deck_command_and_flag_is_in_the_guide():
    html = _DECK.read_text(encoding="utf-8")
    guide = _GUIDE.read_text(encoding="utf-8")
    unknown = _unknown_tokens(html, guide)
    assert not unknown, f"not in HOW-WE-WORK.md (or the flag's source file): {unknown}"


def test_deck_keeps_its_build_commit_footer():
    assert _FOOTER_RE.search(_DECK.read_text(encoding="utf-8"))


def test_checks_catch_planted_failures():
    guide = "Run `/sc:workflow` with `--depth quick`, then `/task-builder`."
    planted = (
        "<p><code>/sc:workflow --depth quick</code></p>"
        "<p><code>/sc:not-a-command</code> and <code>--no-such-flag</code></p>"
        "<p><code>/task</code></p>"
        "<p><code>.dev/tasks/to-do/x/x.md</code></p>"
        "<svg><text>/svg-only-command</text><title>--title-flag</title></svg>"
    )
    unknown = _unknown_tokens(planted, guide)
    # `/task` is not satisfied by `/task-builder`; the path is not a command.
    assert unknown == [
        "--no-such-flag",
        "--title-flag",
        "/sc:not-a-command",
        "/svg-only-command",
        "/task",
    ]
    assert not _FOOTER_RE.search("Built from HOW-WE-WORK.md")
    assert _FOOTER_RE.search("Built from HOW-WE-WORK.md at commit 070399eb")
