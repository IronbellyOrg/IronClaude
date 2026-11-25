"""Redact credential values from issue drafts in place, printing only a count.

usage: redact_body.py FILE [FILE ...]

``/sc:issue --create`` runs this on ``issue-body.md`` and ``draft-notes.md``
before the issue is posted. It matches by value shape (private key blocks,
well-known token formats, bearer and JWT tokens, the password part of a
``user:password@`` URL) and by name (``password``, ``api_key``, ``token`` and
similar, case-insensitive, with ``-`` or ``_``). A weak name such as ``token`` or
``key`` is redacted only when its value looks like a secret (16 or more
characters with a letter and a digit), so ``key: ArrowUp`` stays. It never
prints a line or a value: the only output is ``redacted: <n>`` (the number of
values replaced). Exit code 2 when a file cannot be read or written.
"""

from __future__ import annotations

import re
import sys

REDACTED = "<REDACTED>"

PRIVATE_KEY_BLOCK = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.DOTALL,
)

# Values that are credentials by their own shape, wherever they appear.
SHAPED_VALUES = re.compile(
    r"""(?:
        \bgh[pousr]_[A-Za-z0-9]{20,}
      | \bgithub_pat_[A-Za-z0-9_]{20,}
      | \bsk-[A-Za-z0-9_-]{20,}
      | \bxox[abprs]-[A-Za-z0-9-]{10,}
      | \bAKIA[0-9A-Z]{16}\b
      | \bAIza[0-9A-Za-z_-]{30,}
      | \beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}
      | (?<=\bBearer\s)[A-Za-z0-9._~+/=-]{16,}
      | (?<=\bBasic\s)[A-Za-z0-9+/=]{8,}
    )""",
    re.VERBOSE | re.IGNORECASE,
)

URL_PASSWORD = re.compile(r"(\b[a-z][a-z0-9+.-]*://[^\s/:@]+:)([^\s/@]+)(@)", re.I)

_SEP = r"""["']?\s*[:=]\s*["']?"""
_VALUE = r"""[^\s"',;]+"""
_NAME_CHARS = r"[A-Za-z0-9_.-]*"

# Names that always hold a credential: any value is replaced.
STRONG_PAIR = re.compile(
    rf"""(?P<head>{_NAME_CHARS}
        (?:api[_-]?key|secret|passw(?:or)?d|passwd|private[_-]?key
           |authorization|credential|session[_-]?id|cookie)
        {_NAME_CHARS}{_SEP})(?P<value>{_VALUE})""",
    re.VERBOSE | re.IGNORECASE,
)

# Names that may be harmless (``key: ArrowUp``): replaced only for secret-shaped values.
WEAK_PAIR = re.compile(
    rf"""(?P<head>{_NAME_CHARS}(?:token|key){_NAME_CHARS}{_SEP})(?P<value>{_VALUE})""",
    re.VERBOSE | re.IGNORECASE,
)

_PLACEHOLDER_START = ("<", "$", "{", "%", "*")


def _is_placeholder(value: str) -> bool:
    return (
        value.startswith(_PLACEHOLDER_START)
        or value.upper() == "REDACTED"
        or value.lower() in {"bearer", "basic"}  # the scheme word, not the secret
    )


def _secret_shaped(value: str) -> bool:
    return (
        len(value) >= 16
        and any(ch.isdigit() for ch in value)
        and any(ch.isalpha() for ch in value)
    )


def redact(text: str) -> tuple[str, int]:
    """Return ``text`` with credential values replaced and the replacement count."""
    total = 0
    text, n = PRIVATE_KEY_BLOCK.subn(REDACTED, text)
    total += n
    text, n = SHAPED_VALUES.subn(REDACTED, text)
    total += n
    text, n = URL_PASSWORD.subn(
        lambda m: (
            m.group(0)
            if _is_placeholder(m.group(2))
            else m.group(1) + REDACTED + m.group(3)
        ),
        text,
    )
    total += n

    def strong(match: re.Match[str]) -> str:
        nonlocal total
        if _is_placeholder(match["value"]):
            return match.group(0)
        total += 1
        return match["head"] + REDACTED

    def weak(match: re.Match[str]) -> str:
        nonlocal total
        value = match["value"]
        if _is_placeholder(value) or not _secret_shaped(value):
            return match.group(0)
        total += 1
        return match["head"] + REDACTED

    text = STRONG_PAIR.sub(strong, text)
    text = WEAK_PAIR.sub(weak, text)
    return text, total


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: redact_body.py FILE [FILE ...]")
        return 2
    total = 0
    for name in argv:
        try:
            with open(name, encoding="utf-8") as handle:
                original = handle.read()
            redacted, count = redact(original)
            if redacted != original:
                with open(name, "w", encoding="utf-8") as handle:
                    handle.write(redacted)
        except OSError as exc:
            print(f"redact_body: cannot process {name}: {exc.strerror}")
            return 2
        total += count
    print(f"redacted: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
