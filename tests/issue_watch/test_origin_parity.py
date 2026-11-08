"""Parity of ``launch.parse_origin`` with the skill script's ``parse_origin_url``.

The script (``sc-issue-protocol/scripts/origin_repo.py``) is not a package, so it
is loaded from the checkout by path under a private module name that is never
put into ``sys.modules``. One table drives both parsers (design row C3, AC-16).
The one intended difference is pinned: both parsers keep the host case-sensitive
and keep the owner and repo case; only the poller's ``check_origin`` compares
the result lower-cased with ``ironbellyorg/ironclaude``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import launch
from superclaude.cli.issue_watch.launch import ORIGIN_MISMATCH, check_origin
from superclaude.cli.issue_watch.runner import CommandResult

_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py"
)
_MODULE_NAME = "_issue_watch_parity_origin_repo"

OWNER_REPO = "IronbellyOrg/IronClaude"
WORKTREE = "/work/tree"
GIT_ARGV = ("git", "-C", WORKTREE, "remote", "get-url", "origin")

# (url, expected value from both parsers)
PARITY_TABLE: list[tuple[str, str | None]] = [
    ("https://github.com/IronbellyOrg/IronClaude", OWNER_REPO),
    ("https://github.com/IronbellyOrg/IronClaude.git", OWNER_REPO),
    ("https://github.com/IronbellyOrg/IronClaude/", OWNER_REPO),
    ("https://github.com/IronbellyOrg/IronClaude.git/", OWNER_REPO),
    ("https://github.com/IronbellyOrg/IronClaude\n", OWNER_REPO),
    ("git@github.com:IronbellyOrg/IronClaude", OWNER_REPO),
    ("git@github.com:IronbellyOrg/IronClaude.git", OWNER_REPO),
    ("git@github.com:IronbellyOrg/IronClaude/", OWNER_REPO),
    ("git@github.com:IronbellyOrg/IronClaude.git/", OWNER_REPO),
    ("git@github.com:IronbellyOrg/IronClaude\n", OWNER_REPO),
    ("https://github.com/IronbellyOrg", None),
    ("https://github.com/IronbellyOrg/", None),
    ("https://github.com/IronbellyOrg/.git", None),
    ("https://gitlab.com/IronbellyOrg/IronClaude.git", None),
    ("git@bitbucket.org:IronbellyOrg/IronClaude.git", None),
    ("/srv/git/IronClaude.git", None),
    ("", None),
    ("ssh://git@github.com/IronbellyOrg/IronClaude.git", None),
    ("http://github.com/IronbellyOrg/IronClaude.git", None),
    (
        "https://user:token@github.com/IronbellyOrg/IronClaude.git",  # pragma: allowlist secret
        None,
    ),
    ("https://GitHub.com/IronbellyOrg/IronClaude", None),
    ("git@GITHUB.COM:IronbellyOrg/IronClaude", None),
    ("https://github.com/IRONBELLYORG/IRONCLAUDE", "IRONBELLYORG/IRONCLAUDE"),
    ("https://github.com/ironbellyorg/ironclaude.git", "ironbellyorg/ironclaude"),
]


@pytest.fixture(scope="module")
def original():
    """Load ``origin_repo.py`` by path without registering it in ``sys.modules``."""
    assert _MODULE_NAME not in sys.modules
    spec = importlib.util.spec_from_file_location(_MODULE_NAME, _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert _MODULE_NAME not in sys.modules
    return module


def _git_reply(url: str) -> CommandResult:
    return CommandResult(
        argv=GIT_ARGV,
        returncode=0,
        stdout=url,
        stderr="",
        timed_out=False,
        spawn_error=None,
        duration_s=0.0,
    )


@pytest.mark.parametrize(("url", "expected"), PARITY_TABLE)
def test_ac16_parse_origin_matches_parse_origin_url__fr025_nfr003(
    original, url, expected
):
    """AC-16 FR-025 NFR-003: both parsers return the same value for each row."""
    assert original.parse_origin_url(url) == expected
    assert launch.parse_origin(url) == expected


def test_ac16_parity_table_covers_every_required_shape__fr025_nfr003():
    """AC-16 FR-025 NFR-003: the table holds accepted and rejected rows."""
    accepted = [url for url, value in PARITY_TABLE if value is not None]
    rejected = [url for url, value in PARITY_TABLE if value is None]
    assert any(u.startswith("https://") for u in accepted)
    assert any(u.startswith("git@") for u in accepted)
    assert any(u.endswith(".git") for u in accepted)
    assert any(u.endswith("/") for u in accepted)
    assert any(u.endswith(".git/") for u in accepted)
    assert any(u.endswith("\n") for u in accepted)
    for needle in ("gitlab", "bitbucket", "ssh://", "http://", "user:token@"):
        assert any(needle in u for u in rejected), needle
    assert "" in rejected
    assert "/srv/git/IronClaude.git" in rejected
    assert "https://github.com/IronbellyOrg" in rejected
    assert any("GitHub.com" in u for u in rejected)


def test_ac16_original_module_is_not_registered_in_sys_modules__nfr003(original):
    """NFR-003: loading the script leaves no entry in ``sys.modules``."""
    assert _MODULE_NAME not in sys.modules
    assert Path(original.__file__).resolve() == _SCRIPT.resolve()


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/IRONBELLYORG/IRONCLAUDE",
        "https://github.com/ironbellyorg/ironclaude.git",
        "git@github.com:IronbellyOrg/IronClaude.git",
    ],
)
def test_ac16_both_parsers_keep_owner_repo_case__fr025(original, url):
    """AC-16 FR-025: neither parser lower-cases the owner or the repo."""
    path = url.split("github.com", 1)[1].lstrip("/:")
    path = path.removesuffix(".git")
    assert original.parse_origin_url(url) == path
    assert launch.parse_origin(url) == path


@pytest.mark.parametrize("url", ["https://GitHub.com/IronbellyOrg/IronClaude"])
def test_ac16_both_parsers_are_case_sensitive_on_host__fr025(original, url):
    """AC-16 FR-025: an upper-case host is rejected by both parsers."""
    assert original.parse_origin_url(url) is None
    assert launch.parse_origin(url) is None


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/IronbellyOrg/IronClaude.git\n",
        "git@github.com:IronbellyOrg/IronClaude",
        "https://github.com/IRONBELLYORG/IRONCLAUDE",
        "https://github.com/ironbellyorg/ironclaude/",
    ],
)
def test_ac16_only_check_origin_compares_lower_case__fr025(original, fake_runner, url):
    """AC-16 FR-025: the poller accepts any case; the script's value keeps it."""
    runner = fake_runner({GIT_ARGV: _git_reply(url)})
    assert check_origin(runner, WORKTREE, 5) is None
    parsed = original.parse_origin_url(url)
    assert parsed is not None
    assert launch.parse_origin(url) == parsed
    assert parsed.lower() == launch.ORIGIN_REPO
    assert not hasattr(original, "ORIGIN_REPO")


@pytest.mark.parametrize(
    "url",
    [
        "https://GitHub.com/IRONBELLYORG/IRONCLAUDE",
        "https://github.com/IronbellyOrg/IronClaudeX",
        "https://gitlab.com/IronbellyOrg/IronClaude",
        "",
    ],
)
def test_ac16_check_origin_rejects_what_parse_rejects_or_foreign__fr025(
    fake_runner, url
):
    """AC-16 FR-025: a host in the wrong case or a foreign repo is a mismatch."""
    runner = fake_runner({GIT_ARGV: _git_reply(url)})
    assert check_origin(runner, WORKTREE, 5) == ORIGIN_MISMATCH
