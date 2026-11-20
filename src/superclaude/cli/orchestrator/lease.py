"""The verb ``superclaude orchestrator lease``: the second line against a double claim (design DQ3; wave 1).

    lease post    --repo <R> --number <N> [--orchestrator <id>] [--tag <tag>]
    lease check   --repo <R> --number <N> [--orchestrator <id>] [--tag <tag>]
    lease release --repo <R> --number <N> [--orchestrator <id>] [--tag <tag>]

The poll routes each issue to one orchestrator under one lock, and the state file is made
with exclusive create. What those cannot see is a second poll on another host, another
user's orchestrator, a hand-run ``--take`` or a restored store. For those, before wave 1
the orchestrator posts a lease comment

    <!-- sc:orchestrator:lease host=<host> run=<run id> -->

and keeps the claim only when its own lease is the one with the lowest comment id among the
active leases written by its own login. ``host`` and ``run`` are the host and Run id of
``runs/<orchestrator id>.json`` (wave 0 writes it first).

``post`` writes the comment and prints its id. It is safe to repeat: an active lease of this
very host and run is returned (``reused``) and nothing is posted twice, which is how a
restart settles a ``lease_posted`` step that has no ``done`` line (reading GitHub, never
repeating the act). ``check`` lists the lease comments of the issue (every page; a list that
cannot be read whole is ``external_unreadable``, exit 6, and never a shorter list) and prints
``keep: true`` when the own lease is the lowest. Otherwise the loser edits its own lease to
the released form and exits 3 with ``lease_lost`` (the skill records ``claimed_elsewhere``
and takes nothing, ``E-LEASE-LOST``). A missing own lease is ``lease_missing`` (exit 3).

THE WINNER'S RELEASE (finding F6 of issue 675 and 665: a winner that stops would keep the
lowest id for ever and every later orchestrator of that issue would lose). ``release`` edits
the own lease to the released form,

    <!-- sc:orchestrator:lease host=<host> run=<run id> state=released -->

and is run by wave 9 for every issue whose state file leaves ``in_progress`` (``done``,
``skipped``, ``failed`` or ``escalated``): the orchestrator has stopped working the issue
for now, so it stops holding it. A released lease is never counted. If a person's answer
reopens an escalated issue, ``post`` is run again first. ``release`` with no own active lease
releases nothing and is not an error, so wave 9 can run it twice.

Every write here is a GitHub write through an own verb, so it needs the grant ``issue.comment``
and a listed, enabled repo (``no_grant``, ``repo_not_listed``, ``repo_disabled``; exit 2). The
verb prints the ``grant`` it used; the skill puts it in the ``done`` line of the step, which is
how the state file's log names the grant (5.6). The comments are read through ``gh api``, and
only comments by the user's own login (``gh api user``) are leases.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import click

from superclaude.cli.issue_watch.predicates import valid_issue_number, valid_repo
from superclaude.cli.issue_watch.runner import Runner

from . import common, ext, repos_file, state
from .state import EXIT_CONFLICT, EXIT_INVALID, EXIT_NOT_FOUND, StateError

GRANT: Final = "issue.comment"
_LEASE: Final = re.compile(
    r"<!-- sc:orchestrator:lease host=(?P<host>[A-Za-z0-9._-]{1,100}) "
    r"run=(?P<run>[A-Za-z0-9._:-]{1,128})(?P<released> state=released)? -->"
)
_COMMENTS_JQ: Final = ".[] | {id: .id, login: .user.login, body: .body}"


@dataclass(frozen=True)
class Lease:
    """One lease comment of the user's own login."""

    comment_id: int
    host: str
    run: str
    released: bool


def marker(host: str, run: str, released: bool = False) -> str:
    """The body of a lease comment (the released form adds ``state=released``)."""
    tail = " state=released" if released else ""
    return f"<!-- sc:orchestrator:lease host={host} run={run}{tail} -->"


def _own_login(runner: Runner) -> str:
    login = ext.run_checked(runner, ["gh", "api", "user", "--jq", ".login"]).strip()
    if not login:
        raise StateError("external_unreadable", ext.EXIT_EXTERNAL)
    return login


def list_leases(runner: Runner, repo: str, number: int, login: str) -> list[Lease]:
    """Every lease comment of ``login`` on the issue (released ones included), all pages."""
    text = ext.run_checked(
        runner,
        [
            "gh",
            "api",
            "--paginate",
            f"repos/{repo}/issues/{number}/comments",
            "--jq",
            _COMMENTS_JQ,
        ],
    )
    leases: list[Lease] = []
    for value in ext.json_values(text):
        if not isinstance(value, dict) or type(value.get("id")) is not int:
            raise StateError("external_unreadable", ext.EXIT_EXTERNAL)
        body, who = value.get("body"), value.get("login")
        if (
            not isinstance(body, str)
            or not isinstance(who, str)
            or who.lower() != login.lower()
        ):
            continue
        match = _LEASE.fullmatch(body.strip())
        if match is not None:
            leases.append(
                Lease(
                    value["id"],
                    match["host"],
                    match["run"],
                    match["released"] is not None,
                )
            )
    return leases


def _setup(
    root: Path, repo: str, number: int, orchestrator: str | None, tag: str | None
) -> tuple[Runner, str, str]:
    """The guarded runner, the host and the Run id of this orchestrator; the repo and grant checked."""
    if not valid_repo(repo) or not valid_issue_number(number):
        raise StateError("invalid_input", EXIT_INVALID)
    ident, _ = ext.identity(orchestrator, tag)
    try:
        run = state.load_run(root, ident)
    except StateError as exc:
        if exc.reason == "not_found":
            raise StateError("run_not_found", EXIT_NOT_FOUND) from None
        raise
    if re.fullmatch(r"[A-Za-z0-9._-]{1,100}", run["host"]) is None:
        raise StateError("invalid_host", EXIT_INVALID)
    return ext.make_runner("lease"), run["host"], run["run_id"]


def _grant(root: Path, runner: Runner, repo: str) -> None:
    repos_file.require_grant(repos_file.load_doc(root, runner), repo, GRANT)


def _edit(runner: Runner, repo: str, comment_id: int, body: str) -> None:
    ext.run_checked(
        runner,
        [
            "gh",
            "api",
            "-X",
            "PATCH",
            f"repos/{repo}/issues/comments/{comment_id}",
            "-f",
            f"body={body}",
        ],
    )


def post(
    root: Path, repo: str, number: int, orchestrator: str | None, tag: str | None
) -> dict[str, Any]:
    """Post the own lease, or return the active one of this host and run."""
    runner, host, run = _setup(root, repo, number, orchestrator, tag)
    _grant(root, runner, repo)
    login = _own_login(runner)
    for lease in list_leases(runner, repo, number, login):
        if (lease.host, lease.run, lease.released) == (host, run, False):
            return {"comment_id": lease.comment_id, "reused": True, "grant": GRANT}
    out = ext.run_checked(
        runner,
        ["gh", "api", "-X", "POST", f"repos/{repo}/issues/{number}/comments",
         "-f", f"body={marker(host, run)}", "--jq", ".id"],
    )  # fmt: skip
    try:
        comment_id = int(out.strip())
    except ValueError:
        raise StateError("external_unreadable", ext.EXIT_EXTERNAL) from None
    return {"comment_id": comment_id, "reused": False, "grant": GRANT}


def check(
    root: Path, repo: str, number: int, orchestrator: str | None, tag: str | None
) -> dict[str, Any]:
    """Keep the claim only with the lowest active lease; the loser releases its own and exits 3."""
    runner, host, run = _setup(root, repo, number, orchestrator, tag)
    login = _own_login(runner)
    active = [x for x in list_leases(runner, repo, number, login) if not x.released]
    own = next((x for x in active if (x.host, x.run) == (host, run)), None)
    if own is None:
        raise StateError("lease_missing", EXIT_CONFLICT)
    lowest = min(x.comment_id for x in active)
    if own.comment_id == lowest:
        return {
            "keep": True,
            "comment_id": own.comment_id,
            "lowest_comment_id": lowest,
            "active_leases": len(active),
        }
    _grant(root, runner, repo)
    _edit(runner, repo, own.comment_id, marker(host, run, released=True))
    raise StateError(
        "lease_lost",
        EXIT_CONFLICT,
        comment_id=own.comment_id,
        winner_comment_id=lowest,
        released=True,
        grant=GRANT,
    )


def release(
    root: Path, repo: str, number: int, orchestrator: str | None, tag: str | None
) -> dict[str, Any]:
    """Edit every active lease of this host and run to the released form (the winner's release)."""
    runner, host, run = _setup(root, repo, number, orchestrator, tag)
    _grant(root, runner, repo)
    login = _own_login(runner)
    mine = [
        x
        for x in list_leases(runner, repo, number, login)
        if (x.host, x.run) == (host, run) and not x.released
    ]
    for lease in mine:
        _edit(runner, repo, lease.comment_id, marker(host, run, released=True))
    return {"released": [x.comment_id for x in mine], "grant": GRANT}


_repo = click.option("--repo", required=True, help="owner/name of the issue's repo.")
_number = click.option("--number", required=True, type=int, help="The issue number.")
_orch = click.option(
    "--orchestrator",
    default=None,
    help="My orchestrator id (default: from the session tag).",
)
_tag = click.option(
    "--tag",
    default=None,
    help="My session tag (default: the CLAUDE_TOPIC of this session).",
)


@click.group(name="lease")
def lease_group() -> None:
    """Post, check and release the claim lease comment of an issue."""


@lease_group.command("post")
@_repo
@_number
@_orch
@_tag
def post_cmd(repo, number, orchestrator, tag) -> None:
    """Post my lease comment (or find the one already posted)."""
    common.run(lambda: post(common.root(), repo, number, orchestrator, tag))


@lease_group.command("check")
@_repo
@_number
@_orch
@_tag
def check_cmd(repo, number, orchestrator, tag) -> None:
    """Keep the claim only when my lease has the lowest comment id; the loser releases its own."""
    common.run(lambda: check(common.root(), repo, number, orchestrator, tag))


@lease_group.command("release")
@_repo
@_number
@_orch
@_tag
def release_cmd(repo, number, orchestrator, tag) -> None:
    """Release my lease when I stop working the issue (wave 9)."""
    common.run(lambda: release(common.root(), repo, number, orchestrator, tag))
