"""The observer's own text sanitizer: untrusted text in, printable literal text out (AD-9).

Written for this package; the weaker ``ANSI_ESCAPE_RE`` in ``eval/pty_stream.py`` and the
design prototype are not used. Markup safety is not this module's job: renderers build
``rich.text.Text`` objects from data and never parse worker text as markup.
"""

from __future__ import annotations

import re
import unicodedata

# One pass over every escape form. Strings (OSC, DCS, SOS, PM, APC) run to their
# terminator or, when there is none, to the end of the text.
_ESCAPES = re.compile(
    r"(?:\x1b\]|\x9d)[\s\S]*?(?:\x07|\x1b\\|\x9c|\Z)"  # OSC: BEL, ST or end
    r"|(?:\x1b[PX^_]|[\x90\x98\x9e\x9f])[\s\S]*?(?:\x1b\\|\x9c|\Z)"  # DCS, SOS, PM, APC
    r"|(?:\x1b\[|\x9b)[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]?"  # CSI, 7-bit and 8-bit
    r"|\x1b[\s\S]?"  # any other ESC plus the next character
)
_NEWLINES = re.compile(
    r"\r\n|\r|" + chr(0x2028) + "|" + chr(0x2029)
)  # CRLF, CR, LS, PS
_DROPPED = frozenset({"Cc", "Cf", "Cs"})  # C0, DEL, C1, format (bidi) and surrogates


def sanitize(text: object, mode: str = "line") -> str:
    """Return ``text`` as printable characters only.

    ``mode="line"`` turns each newline into one space; ``mode="block"`` keeps newlines
    (used only for ``stage.detail``, ``stage.activity`` and stderr in the inspector).
    """
    if mode not in ("line", "block"):
        raise ValueError(f"unknown sanitize mode: {mode!r}")
    if text is None:
        return ""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    elif not isinstance(text, str):
        text = str(text)
    text = _ESCAPES.sub("", text)
    text = _NEWLINES.sub("\n", text)
    newline = " " if mode == "line" else "\n"
    return "".join(
        newline if ch == "\n" else ch
        for ch in text
        if ch == "\n" or unicodedata.category(ch) not in _DROPPED
    )
