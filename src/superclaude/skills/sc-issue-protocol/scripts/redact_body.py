"""Redact credential values from issue drafts in place, printing only a count.

usage: redact_body.py FILE [FILE ...]

``/sc:issue --create`` runs this on ``issue-body.md`` and ``draft-notes.md``
before the issue is posted. It matches by value shape (private key blocks,
well-known token formats, bearer and JWT tokens, the password part of a
``user:password@`` URL) and by name (``password``, ``api_key``, ``token`` and
similar, case-insensitive, with ``-`` or ``_``). A strong name (``password``,
``secret``, ``api_key``, ``authorization``) redacts a quoted value, or the rest of
the line, and a ``Cookie:`` header is redacted to the end of the line. A weak name such as ``token`` or
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

# A long base64-looking run (upper case, lower case and a digit, 40 or more characters)
# is treated as an encoded credential. Git hashes are lower-case hex, so they are not
# redacted. A run with two or more ``/`` that sits inside URL or path syntax (next to
# ``.``, ``-``, ``_``, ``#`` or ``?`` with a letter or digit beyond it, as in a GitHub
# permalink; a full stop that ends a sentence does not count) is kept; a standalone
# run with slashes, such as a session token, is redacted. This narrows, but cannot
# close, the encoded-secret gap: a worker that deliberately obfuscates a value can
# still get past any pattern.
_URL_EDGE = ".-_#?"


def _in_url_or_path(text: str, start: int, end: int) -> bool:
    """True when the run ``text[start:end]`` is joined to URL or path syntax."""
    before = text[start - 1] if start >= 1 else ""
    before2 = text[start - 2] if start >= 2 else ""
    after = text[end] if end < len(text) else ""
    after2 = text[end + 1] if end + 1 < len(text) else ""
    return bool(
        (before and before in _URL_EDGE and before2.isalnum())
        or (after and after in _URL_EDGE and after2.isalnum())
    )


BASE64_BLOB = re.compile(
    r"(?<![A-Za-z0-9+/=])"
    r"(?=[A-Za-z0-9+/]*[A-Z])(?=[A-Za-z0-9+/]*[a-z])(?=[A-Za-z0-9+/]*[0-9])"
    r"[A-Za-z0-9+/]{40,}={0,2}(?![A-Za-z0-9+/=])"
)

# The scheme must start where a run of scheme characters starts (no ``\b``): a long
# run of letters is then scanned once, not again from every position.
URL_PASSWORD = re.compile(
    r"((?<![a-z0-9+.-])[a-z][a-z0-9+.-]*://[^\s/:@]*:)([^\s/@]+)(@)", re.I
)

_SEP = r"""["']?\s*[:=]\s*"""
# Double quotes escape with a backslash; single quotes also escape by doubling (YAML).
_QUOTED = r"""(?:"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.|'')*')"""
# A strong name may hold a multi-line quoted value (YAML). It runs to the closing
# quote, however far away: over-redacting is the safe failure for a public issue.
_QUOTED_ML = (
    # TOML triple quotes: a basic string honours backslash escapes (``\"""``)
    r"""(?:\"{3}(?:[^"\\]|\\[\s\S]|"(?!""))*\"{3}"""
    r"""|'{3}(?:[^']|'(?!''))*'{3}"""
    r"""|"(?:[^"\\]|\\[\s\S])*"|'(?:[^'\\]|\\[\s\S]|'')*')"""
)
# A name run is scanned once: the leading part starts where a run of name characters
# starts (so a long string is not rescanned from every position), and the part after
# the credential word is bounded (so a string that repeats ``password`` stays linear).
_NAME_LEAD = r"(?<![A-Za-z0-9_.-])[A-Za-z0-9_.-]*"
_NAME_CHARS = r"[A-Za-z0-9_.-]{0,64}"
_STRONG_NAMES = r"""(?:api[_-]?key|secret|passw(?:or)?d|passwd|private[_-]?key
           |authorization|credential|session[_-]?id
           |(?:access|auth|refresh|id|bearer)[_-]?token)"""

# A credential line whose value may continue on the more indented lines below it:
# ``password: |`` (a YAML block scalar) or ``password: first-line`` (a plain scalar).
STRONG_LINE = re.compile(
    rf"^[ \t]*(?:-[ \t]+)?[\"']?[A-Za-z0-9_.-]*(?:{_STRONG_NAMES}|(?:set-)?cookie)"
    rf"{_NAME_CHARS}{_SEP}(?P<rest>.*)$",
    re.VERBOSE | re.IGNORECASE,
)

# A whole header line: ``Cookie: theme=dark; session=...`` holds several values.
COOKIE_LINE = re.compile(
    rf"""\b(?P<head>(?:set-)?cookie["']?\s*[:=]\s*)(?P<value>{_QUOTED_ML}(?=[ \t]*(?:[,}}\]]|\#|$))|[^\n]+)""",
    re.IGNORECASE | re.MULTILINE,
)

# netrc style, with no ``:`` or ``=``: ``machine h login u password p`` on one line,
# or a line that is only ``password p``.
NETRC_LOGIN = re.compile(
    rf"(?P<head>\blogin\s+\S+\s+password\s+)(?P<value>{_QUOTED}|\S+)",
    re.IGNORECASE,
)
NETRC_LINE = re.compile(
    rf"^(?P<head>[ \t]*password[ \t]+)(?P<value>{_QUOTED}|\S+)[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)

# ``.pgpass`` style: ``host:port:database:user:password`` on a line of its own. The
# host must contain a letter or ``*``, so a time such as ``10:30:15:00:05`` is left.
PGPASS_LINE = re.compile(
    r"^(?P<head>(?:(?=[^\s:]*[A-Za-z*])[^\s:]+|\d{1,3}(?:\.\d{1,3}){3}):(?:\d+|\*):[^\s:]*:[^\s:]*:)"
    r"(?P<value>\S+)[ \t]*$",
    re.MULTILINE,
)

# Names that always hold a credential: a quoted value, or the rest of the line (a
# passphrase may have several words; over-redacting a line is the safe failure).
STRONG_PAIR = re.compile(
    rf"""(?P<head>{_NAME_LEAD}{_STRONG_NAMES}{_NAME_CHARS}{_SEP})
        (?P<value>{_QUOTED_ML}|[^\n]+)""",
    re.VERBOSE | re.IGNORECASE,
)

# Names that may be harmless (``key: ArrowUp``): replaced only for secret-shaped values.
WEAK_PAIR = re.compile(
    rf"""(?P<head>{_NAME_LEAD}(?:token|key){_NAME_CHARS}{_SEP})
        (?P<value>{_QUOTED}|[^\s"',;]+)""",
    re.VERBOSE | re.IGNORECASE,
)

# A bare ``auth`` field (a Docker ``config.json`` holds ``"auth": "<base64 of user:pass>"``):
# replaced only for a base64-looking value, so ``auth: required`` and ``author: Bob`` stay.
AUTH_PAIR = re.compile(
    rf"""(?P<head>(?<![A-Za-z0-9])auth["']?\s*[:=]\s*)(?P<value>{_QUOTED}|[^\s"',;]+)""",
    re.IGNORECASE,
)

# Exact placeholder shapes only: a real secret that merely starts with ``$`` or
# ``<`` (``$ecret123``) is still redacted.
_PLACEHOLDER = re.compile(
    r"""<REDACTED>
      | <[a-z][a-z _-]*>            # <your-password> (lower case only: <Secret123> is a value)
      | \$\{[^}]*\}                 # ${PASSWORD}
      | \$[A-Z_][A-Z0-9_]*          # $API_KEY (upper-case variable)
      | \{\{[^{}]*\}\}              # {{ secret }}
      | %[A-Za-z_][A-Za-z0-9_]*%    # %PASSWORD%
      | \*+                         # ******
      | [|>][-+0-9]*(?:[ \t]+\#.*)? # a YAML block-scalar header (its lines are handled apart)
    """,
    re.VERBOSE,
)


def _unquote(value: str) -> tuple[str, str]:
    """Split a value into its quote character (or ``""``) and the inner text."""
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        return value[0], value[1:-1]
    return "", value


def _is_placeholder(value: str) -> bool:
    inner = _unquote(value.strip())[1]
    return (
        _PLACEHOLDER.fullmatch(inner) is not None
        or inner.upper() == "REDACTED"
        or inner.lower() in {"bearer", "basic"}  # the scheme word, not the secret
    )


def _secret_shaped(value: str) -> bool:
    return (
        len(value) >= 16
        and any(ch.isdigit() for ch in value)
        and any(ch.isalpha() for ch in value)
    )


def _auth_shaped(value: str) -> bool:
    """A short base64-looking value: 8 or more characters with a digit, ``=`` or mixed case."""
    return (
        len(value) >= 8
        and re.fullmatch(r"[A-Za-z0-9+/_-]+={0,2}", value) is not None
        and (
            any(ch.isdigit() for ch in value)
            or value.endswith("=")
            or (any(ch.isupper() for ch in value) and any(ch.islower() for ch in value))
        )
    )


def _redact_block_scalars(text: str) -> tuple[str, int]:
    """Redact the indented lines under ``password: |`` (a YAML block scalar)."""
    lines = text.split("\n")
    out: list[str] = []
    count = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        head = STRONG_LINE.match(line)
        if not head:
            continue
        rest = head["rest"].strip()
        if rest and rest[0] in "\"'":  # a quoted value (handled apart)
            continue
        # Whatever the first line holds (a block marker, a value, a placeholder or
        # nothing), more indented lines under a credential name are part of the value.
        base = len(line) - len(line.lstrip())
        redacted_any = False
        while i < len(lines) and (
            not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) > base
        ):
            body = lines[i]
            if body.strip():
                out.append(body[: len(body) - len(body.lstrip())] + REDACTED)
                redacted_any = True
            else:
                out.append(body)
            i += 1
        count += redacted_any
    return "\n".join(out), count


def redact(text: str) -> tuple[str, int]:
    """Return ``text`` with credential values replaced and the replacement count."""
    total = 0
    text, n = PRIVATE_KEY_BLOCK.subn(REDACTED, text)
    total += n
    text, n = SHAPED_VALUES.subn(REDACTED, text)
    total += n
    blobs = 0

    def blob(match: re.Match[str]) -> str:
        nonlocal blobs
        if match.group(0).count("/") >= 2 and _in_url_or_path(
            match.string, match.start(), match.end()
        ):
            return match.group(0)
        blobs += 1
        return REDACTED

    text = BASE64_BLOB.sub(blob, text)
    total += blobs
    text, n = _redact_block_scalars(text)
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

    def replace(
        match: re.Match[str], only_if_shaped: bool, shape=_secret_shaped
    ) -> str:
        nonlocal total
        value = match["value"]
        quote, inner = _unquote(value)
        if _is_placeholder(value) or (only_if_shaped and not shape(inner)):
            return match.group(0)
        total += 1
        return match["head"] + quote + REDACTED + quote

    text = PGPASS_LINE.sub(lambda m: replace(m, False), text)
    text = NETRC_LOGIN.sub(lambda m: replace(m, False), text)
    text = NETRC_LINE.sub(lambda m: replace(m, False), text)
    text = COOKIE_LINE.sub(lambda m: replace(m, False), text)
    text = STRONG_PAIR.sub(lambda m: replace(m, False), text)
    text = WEAK_PAIR.sub(lambda m: replace(m, True), text)
    text = AUTH_PAIR.sub(lambda m: replace(m, True, _auth_shaped), text)
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
