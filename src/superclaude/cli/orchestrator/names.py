"""The naming rule (design 5.12, owner ruling 15): nothing a person reads names the agent.

``names_check(text)`` returns one :class:`NameHit` for each place where text that
a person will read names a model or an agent: a model identifier
(a gateway tier id such as ``claude-gw-`` plus a tier name, any ``claude-...``,
``gpt-...``, ``gemini-...``), the
product name of an agent or model family, or a "generated with" line for an
agent. An empty list means the text passes.

The deny list and the allow list are data below. The allow list holds the names
of the review apps (``Augment``, ``Codex``, ``augmentcode[bot]``,
``chatgpt-codex-connector[bot]``), which are facts about the reviewers, and the
one co-author trailer that this repository puts on commits (ruling 39).

Text is not scanned where the name is a fact about the repository and not a
signature:

* inside a backtick span on one line;
* inside the title of a Markdown link (``[text](url "title")``);
* inside a fenced block whose heading says it quotes data: the last non-blank
  line before the opening fence starts with ``Quoted from the issue`` or
  ``Quoted from the worker`` (``QUOTED_HEADINGS``; marks such as ``#``, ``**`` and
  a closing colon are ignored). A fence that is never closed is scanned, not
  skipped, and any other fenced block is scanned too.

The writer verbs ``report-entry`` and ``escalate`` run this on the text they are
about to write and exit 2 when it returns a hit.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

ALLOWED_NAMES: Final = (
    "chatgpt-codex-connector[bot]",
    "augmentcode[bot]",
    "Augment",
    "Codex",
)
"""The review apps. Matched as whole tokens, longest first, before the deny scan."""

ALLOWED_LINES: Final = ("Co-Authored-By: Claude Code <noreply@anthropic.com>",)
"""Whole lines that pass: the commit trailer of this repository (ruling 39)."""

QUOTED_HEADINGS: Final = ("quoted from the issue", "quoted from the worker")
"""A fenced block under one of these headings is quoted data and is not scanned."""

DENY_PATTERNS: Final = (
    (
        "model_id",
        re.compile(
            r"(?<![A-Za-z0-9])(?:claude|gpt|gemini)-[A-Za-z0-9][A-Za-z0-9._-]*", re.I
        ),
    ),
    (
        "agent_name",
        re.compile(
            r"(?<![A-Za-z0-9])(?:claude|anthropic|chatgpt|openai|copilot)(?![A-Za-z0-9])",
            re.I,
        ),
    ),
    ("agent_name", re.compile(r"(?<![A-Za-z0-9])Gemini(?![A-Za-z0-9])")),
    ("agent_name", re.compile(r"(?<![A-Za-z0-9])GPT-?[0-9][0-9A-Za-z.]*")),
    ("agent_name", re.compile(r"(?<![A-Za-z0-9])(?:Opus|Sonnet|Haiku)\s+[0-9]")),
    (
        "attribution",
        re.compile(
            r"^[ \t>*_-]*(?:\U0001f916[ \t]*)?generated[ \t]+(?:with|by)\b[^\n]*"
            r"\b(?:ai|agent|assistant|llm|model|bot)\b",
            re.I | re.M,
        ),
    ),
    (
        "attribution",
        re.compile(
            r"^[ \t]*co-authored-by:[^\n]*\b(?:ai|agent|assistant|llm|model)\b",
            re.I | re.M,
        ),
    ),
)
"""``(kind, pattern)`` pairs: model identifiers, agent product names, attribution lines."""

_FENCE = re.compile(r"^[ ]{0,3}(?P<mark>`{3,}|~{3,})")
_CODE_SPAN = re.compile(r"(?P<tick>`+)(?!`)[^\n]*?(?<!`)(?P=tick)(?!`)")
_LINK_TITLE = re.compile(r"\]\(\s*[^)\s]*\s+(?P<q>[\"'])(?P<title>.*?)(?P=q)\s*\)")
_REF_TITLE = re.compile(
    r"^[ ]{0,3}\[[^\]\n]+\]:[ \t]*\S+[ \t]+(?P<q>[\"'(])(?P<title>.*?)[\"')][ \t]*$",
    re.M,
)


@dataclass(frozen=True)
class NameHit:
    """One place that names an agent or a model.

    ``kind`` is ``model_id``, ``agent_name`` or ``attribution``; ``line`` counts
    from 1; ``text`` is the matched text of the writer's own words.
    """

    kind: str
    line: int
    text: str


def _blank(chars: list[str], start: int, end: int) -> None:
    """Replace ``chars[start:end]`` by spaces, keeping line breaks so lines stay put."""
    for i in range(start, end):
        if chars[i] != "\n":
            chars[i] = " "


def _heading_is_quoted(line: str) -> bool:
    plain = re.sub(r"[#*_:>\s]+", " ", line).strip().lower()
    return any(plain.startswith(h) for h in QUOTED_HEADINGS)


def _mask_quoted_fences(text: str, chars: list[str]) -> None:
    lines = text.split("\n")
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line) + 1)
    last_text = ""  # the last non-blank line before the current position
    i = 0
    while i < len(lines):
        match = _FENCE.match(lines[i])
        if match is None:
            if lines[i].strip():
                last_text = lines[i]
            i += 1
            continue
        mark = match["mark"]
        close = next(
            (
                j
                for j in range(i + 1, len(lines))
                if lines[j].strip().startswith(mark[0] * len(mark))
                and not lines[j].strip().strip(mark[0])
            ),
            None,
        )
        if close is None:  # never closed: scan it, do not skip it
            i += 1
            continue
        if _heading_is_quoted(last_text):
            _blank(chars, offsets[i], min(offsets[close + 1] - 1, len(chars)))
        last_text = ""
        i = close + 1


def _mask_names(text: str, chars: list[str]) -> None:
    for line in ALLOWED_LINES:
        for m in re.finditer(r"^" + re.escape(line) + r"[ \t]*$", text, re.M):
            _blank(chars, m.start(), m.end())
    for name in ALLOWED_NAMES:
        pattern = r"(?<![A-Za-z0-9_-])" + re.escape(name) + r"(?![A-Za-z0-9_-])"
        for m in re.finditer(pattern, text):
            _blank(chars, m.start(), m.end())


def names_check(text: str) -> list[NameHit]:
    """Return every place in ``text`` that names an agent or a model; empty means it passes."""
    chars = list(text)
    _mask_quoted_fences(text, chars)
    for pattern, group in (
        (_CODE_SPAN, 0),
        (_LINK_TITLE, "title"),
        (_REF_TITLE, "title"),
    ):
        masked = "".join(chars)
        for m in pattern.finditer(masked):
            _blank(chars, m.start(group), m.end(group))
    _mask_names(text, chars)
    scan = "".join(chars)
    found = sorted(
        (m.start(), -m.end(), kind, m.group(0))
        for kind, pattern in DENY_PATTERNS
        for m in pattern.finditer(scan)
    )
    hits: list[NameHit] = []
    covered_to = (
        0  # a hit inside an earlier, longer one (a tier id) is not a second hit
    )
    for start, neg_end, kind, matched in found:
        if -neg_end <= covered_to:
            continue
        covered_to = -neg_end
        hits.append(NameHit(kind, scan.count("\n", 0, start) + 1, matched))
    return hits
