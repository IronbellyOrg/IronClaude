#!/usr/bin/env python3
"""Resolve the origin GitHub repository and check a /sc:issue claim argument.

Standard library only. Wave 0 of both /sc:issue modes runs this script, so the
repository rule of the design (section 13) is tested code, not prose.

Usage:
    origin_repo.py
        Print ``owner/repo`` parsed from ``git remote get-url origin``.
    origin_repo.py --claim <number|#number|url>
        Resolve origin as above, then check the claim argument against it and
        print ``{"repo": "owner/repo", "number": N}`` as one JSON line.

Only the ``origin`` remote is read. ``gh repo set-default``, gh's fork-parent
default and every other remote are never consulted.

Accepted origin URLs (a trailing ``/`` is tolerated):
    https://github.com/<owner>/<repo>
    https://github.com/<owner>/<repo>.git
    git@github.com:<owner>/<repo>
    git@github.com:<owner>/<repo>.git

Claim argument rules (``check_claim``):
    ``302`` or ``#302``                         -> N = 302
    ``https://github.com/<origin>/issues/302``  -> N = 302; a trailing ``/``,
                                                   a ``#fragment`` or a
                                                   ``?query`` is ignored
    a GitHub URL naming any other owner or      -> E-FOREIGN-REPO
    repo, or naming no repo                        (owner and repo compare
                                                   case-insensitively and as
                                                   whole path segments, so
                                                   ``IronClaudeX`` is foreign)
    a URL (``<scheme>://...`` or               -> E-FOREIGN-REPO
    ``git@<host>:...``) on any host other
    than github.com
    ``https://github.com/<origin>/pull/302``    -> E-NOT-AN-ISSUE
    a GitHub URL on origin whose path is not    -> E-NOT-AN-ISSUE
    ``/issues/<N>``
    anything else (not a number, not a URL)     -> E-NOT-AN-ISSUE
A GitHub URL may start with ``https://``, ``http://`` or no scheme, may carry
``www.``, and may be written ``git@github.com:<owner>/<repo>/...``; every form
is read by the same rules above. N is read only from the path segment right
after ``/issues/``; digits in the owner or repo name never become N.

Exit codes and messages (the message goes to stderr):
    0  success
    1  E-NO-ORIGIN     no origin remote, git failed, or origin is not GitHub
    2  bad command-line arguments (argparse)
    3  E-FOREIGN-REPO  the claim URL names a repository other than origin
    4  E-NOT-AN-ISSUE  the claim argument is not an issue number or issue URL
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

EXIT_NO_ORIGIN = 1
EXIT_FOREIGN_REPO = 3
EXIT_NOT_AN_ISSUE = 4

_NAME = r"[A-Za-z0-9._-]+"
_ORIGIN_PATTERNS = (
    re.compile(rf"^https://github\.com/(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
    re.compile(rf"^git@github\.com:(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
)
_GITHUB_URL = re.compile(
    r"^(?:(?:https?://)?(?:www\.)?github\.com/|git@github\.com:)(?P<path>[^?#]*)",
    re.IGNORECASE,
)
_NUMBER = re.compile(r"^#?(?P<n>[1-9][0-9]*)$")


class ClaimError(Exception):
    """A claim argument that /sc:issue must STOP on."""

    def __init__(self, code: str, exit_code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code


def parse_origin_url(url: str) -> str | None:
    """Return ``owner/repo`` for a GitHub origin URL, else ``None``."""
    url = url.strip()
    for pattern in _ORIGIN_PATTERNS:
        match = pattern.match(url)
        if match:
            owner = match.group("owner")
            repo = match.group("repo")
            if repo.endswith(".git"):
                repo = repo[: -len(".git")]
            if not repo or owner in (".", "..") or repo in (".", ".."):
                return None
            return "/".join((owner, repo))
    return None


def check_claim(arg: str, origin: str) -> int:
    """Return the issue number a claim argument names on ``origin``.

    Raises ``ClaimError`` with ``E-FOREIGN-REPO`` or ``E-NOT-AN-ISSUE``.
    """
    arg = arg.strip()
    number = _NUMBER.match(arg)
    if number:
        return int(number.group("n"))

    url = _GITHUB_URL.match(arg)
    if not url:
        if "://" in arg or arg.lower().startswith("git@"):
            raise ClaimError(
                "E-FOREIGN-REPO",
                EXIT_FOREIGN_REPO,
                f"{arg} is not a GitHub URL, so it is not on the origin repo {origin}",
            )
        raise ClaimError(
            "E-NOT-AN-ISSUE",
            EXIT_NOT_AN_ISSUE,
            f"{arg} is not an issue number or an issue URL",
        )

    segments = [s for s in url.group("path").split("/") if s]
    if len(segments) < 2:
        raise ClaimError(
            "E-FOREIGN-REPO", EXIT_FOREIGN_REPO, f"{arg} names no repository"
        )
    owner, repo = segments[0], segments[1]
    if repo.lower().endswith(".git"):
        repo = repo[: -len(".git")]
    origin_owner, origin_repo = origin.split("/", 1)
    if owner.lower() != origin_owner.lower() or repo.lower() != origin_repo.lower():
        raise ClaimError(
            "E-FOREIGN-REPO",
            EXIT_FOREIGN_REPO,
            "/".join((owner, repo)) + f" is not the origin repo {origin}",
        )

    rest = segments[2:]
    if len(rest) == 2 and rest[0] == "issues":
        number = _NUMBER.match(rest[1])
        if number and not rest[1].startswith("#"):
            return int(number.group("n"))
    if rest and rest[0] == "pull":
        raise ClaimError(
            "E-NOT-AN-ISSUE",
            EXIT_NOT_AN_ISSUE,
            f"{arg} is a pull request, not an issue",
        )
    raise ClaimError("E-NOT-AN-ISSUE", EXIT_NOT_AN_ISSUE, f"{arg} is not an issue URL")


def read_origin() -> str:
    """Return ``owner/repo`` of the ``origin`` remote, or raise ``ClaimError``."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise ClaimError(
            "E-NO-ORIGIN", EXIT_NO_ORIGIN, f"git could not run: {exc}"
        ) from exc
    if result.returncode != 0:
        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, "no origin remote")
    parsed = parse_origin_url(result.stdout)
    if parsed is None:
        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, "origin is not a GitHub URL")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--claim", metavar="NUMBER_OR_URL")
    args = parser.parse_args(argv)
    try:
        origin = read_origin()
        if args.claim is None:
            print(origin)
            return 0
        number = check_claim(args.claim, origin)
    except ClaimError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return exc.exit_code
    print(json.dumps({"repo": origin, "number": number}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
