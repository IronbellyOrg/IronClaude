"""Post the result comment of a run and move the issue's Project Status (plan Task 12, R24).

Only the coordinator calls this, under the issue's grant row (``WORKER-CONTRACT.md``,
"Issue pipeline duties"). A launched agent and every worker report through their result file
and never call it. This module and ``issue_watch/repo_init.py`` are the only code that writes
to GitHub; ``issue_watch/github.py`` stays read-only (security invariant NG-2).

One call does, in order:

1. validates every input and refuses with a closed word before any ``gh`` call;
2. for ``succeeded`` only, reads the issue's Project items and selects the one non-archived item
   of the configured Project (zero items, several items, or a Status field with no end option
   refuse before any write, the comment included);
3. posts one result comment carrying the per-run marker ``<!-- sc:issue:result issue=<N>
   run=<approval event id> -->``, unless a comment written by the runner's own login already
   holds that exact marker (a second call for the same run posts nothing new);
4. for ``succeeded`` only, sets the Status to the end Status of the item's current Status, and
   only when that current Status is one of ``ALLOWED_STATUSES``; any other current Status
   (a person moved it, say to Done) leaves the Status alone and returns
   ``status_moved_by_person``.

A failed, blocked or partial outcome posts the comment and never moves the Status. Every result
is a closed word; no issue or comment text is echoed, and the comment holds only the outcome
word, validated artifact paths and a pull request number.

Known limit (shortcut: read then write, upgrade only if a person's move inside that window
ever matters): the Status read and the Status write are two calls, not one atomic step, so a
person's move between them can still be overwritten.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from superclaude.cli.issue_watch.predicates import (
    ALLOWED_STATUSES,
    CLAIM_MARKER,
    ProjectItem,
    live_item,
    valid_issue_number,
)
from superclaude.cli.issue_watch.runner import CommandResult, Runner

TIMEOUT_S = 60.0
PAGE_SIZE = 100
PAGE_CAP = 5

OUTCOMES = ("succeeded", "failed", "blocked", "partial")

# The end Status of each allowed Status (owner decision of 2026-11-19: all four pipelines end
# at In review). An exception is a one-line change here.
END_STATUS: dict[str, str] = {
    "Research": "In review",
    "Spec": "In review",
    "Plan": "In review",
    "Debug": "In review",
}

# Closed result words.
COMPLETED = (
    "completed"  # succeeded: comment in place and the Status is at its end value
)
COMMENTED = (
    "commented"  # failed, blocked or partial: comment in place, Status untouched
)
STATUS_MOVED_BY_PERSON = "status_moved_by_person"
RESULT_WORDS = frozenset(
    {
        COMPLETED,
        COMMENTED,
        STATUS_MOVED_BY_PERSON,
        "refused:bad_outcome",
        "refused:bad_issue",
        "refused:bad_project_id",
        "refused:bad_repo",
        "refused:bad_run",
        "refused:bad_summary",
        "refused:project_missing",
        "refused:project_ambiguous",
        "refused:status_option_missing",
        "failed:project_read",
        "failed:own_login",
        "failed:comments_read",
        "failed:comment_post",
        "failed:status_move",
    }
)

_REPO = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
_PROJECT_ID = re.compile(r"PVT_[A-Za-z0-9_-]+")
_NODE_ID = re.compile(r"[A-Za-z0-9_=-]{1,200}")
_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
_PATH = re.compile(r"[A-Za-z0-9._][A-Za-z0-9._/-]{0,199}")
_PULL_REQUEST = re.compile(r"[1-9][0-9]{0,8}")
MAX_ARTIFACTS = 20

ITEMS_QUERY = """query($owner: String!, $name: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    issue(number: $number) {
      projectItems(first: 100, after: $after) {
        nodes {
          id
          isArchived
          project {
            id
            field(name: "Status") {
              ... on ProjectV2SingleSelectField { id options { id name } }
            }
          }
          status: fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue { name }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}"""

MOVE_MUTATION = """mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(input: {projectId: $projectId, itemId: $itemId, fieldId: $fieldId, value: {singleSelectOptionId: $optionId}}) {
    projectV2Item { id }
  }
}"""


def result_marker(issue: int, run_id: int) -> str:
    """The per-run marker; it never contains the claim marker."""
    return f"<!-- sc:issue:result issue={issue} run={run_id} -->"


@dataclass(frozen=True)
class _Summary:
    artifacts: tuple[str, ...]
    pull_request: str | None


def _read_summary(path: object) -> _Summary | None:
    """Read the closed three-line result file; None when it is absent or malformed."""
    if path is None:
        return _Summary((), None)
    try:
        lines = Path(str(path)).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    keys = [line.partition(":")[0] for line in lines]
    if keys != ["outcome", "artifacts", "pull_request"]:
        return None
    artifacts_text = lines[1].partition(":")[2].strip()
    artifacts = (
        tuple(a.strip() for a in artifacts_text.split(",")) if artifacts_text else ()
    )
    if len(artifacts) > MAX_ARTIFACTS or not all(
        _PATH.fullmatch(a) and ".." not in a for a in artifacts
    ):
        return None
    pr = lines[2].partition(":")[2].strip()
    if pr == "none":
        return _Summary(artifacts, None)
    if _PULL_REQUEST.fullmatch(pr):
        return _Summary(artifacts, pr)
    return None


def _comment_body(marker: str, outcome: str, summary: _Summary) -> str:
    artifacts = ", ".join(summary.artifacts) if summary.artifacts else "none"
    pr = f"#{summary.pull_request}" if summary.pull_request else "none"
    return (
        f"{marker}\nResult of the run: {outcome}\n"
        f"Artifacts: {artifacts}\nPull request: {pr}"
    )


def _validate(
    repo: object, issue: object, project_id: object, run_id: object, outcome: object
) -> str | None:
    if outcome not in OUTCOMES:
        return "refused:bad_outcome"
    if not valid_issue_number(issue):
        return "refused:bad_issue"
    if not isinstance(project_id, str) or not _PROJECT_ID.fullmatch(project_id):
        return "refused:bad_project_id"
    if not isinstance(repo, str) or not _REPO.fullmatch(repo):
        return "refused:bad_repo"
    if type(run_id) is not int or not 0 < run_id < 10**18:
        return "refused:bad_run"
    return None


def _run(runner: Runner, argv: list[str]) -> CommandResult | None:
    result = runner.run(argv, TIMEOUT_S)
    if result.returncode != 0 or result.timed_out or result.spawn_error is not None:
        return None
    return result


def _json(result: CommandResult | None) -> object | None:
    if result is None:
        return None
    try:
        parsed = json.loads(result.stdout)
    except ValueError:
        return None
    if isinstance(parsed, dict) and parsed.get("errors"):
        return None
    return parsed


@dataclass(frozen=True)
class _Target:
    item_id: str
    field_id: str
    current: str | None
    options: dict[str, str]


def _items(runner: Runner, owner: str, name: str, issue: int) -> list[dict] | None:
    nodes: list[dict] = []
    after: str | None = None
    for _ in range(PAGE_CAP):
        argv = [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={ITEMS_QUERY}",
            "-f",
            f"owner={owner}",
            "-f",
            f"name={name}",
            "-F",
            f"number={issue}",
        ]
        if after is not None:
            argv += ["-f", f"after={after}"]
        data = _json(_run(runner, argv))
        try:
            page = data["data"]["repository"]["issue"]["projectItems"]  # type: ignore[index]
            nodes += [n for n in page["nodes"] if isinstance(n, dict)]
            info = page["pageInfo"]
            if not info["hasNextPage"]:
                return nodes
            after = info["endCursor"]
        except (KeyError, TypeError):
            return None
        if not isinstance(after, str) or not re.fullmatch(
            r"[A-Za-z0-9+/=_.:-]{1,256}", after
        ):
            return None
    return None  # more pages than the cap: unknown, so no write


def _select(
    nodes: list[dict], project_id: str, end_statuses: set[str]
) -> _Target | str:
    pairs: list[tuple[ProjectItem, dict]] = []
    for node in nodes:
        project = node.get("project") or {}
        status = node.get("status") or {}
        pairs.append(
            (
                ProjectItem(
                    bool(node.get("isArchived")),
                    str(project.get("id")),
                    status.get("name") if isinstance(status.get("name"), str) else None,
                ),
                node,
            )
        )
    matching = [p for p, _ in pairs if not p.is_archived and p.project_id == project_id]
    if not matching:
        return "refused:project_missing"
    if len(matching) > 1:
        return "refused:project_ambiguous"
    item = live_item([p for p, _ in pairs], project_id)
    node = next(n for p, n in pairs if p is item)
    field = (node.get("project") or {}).get("field") or {}
    options = {
        o["name"]: o["id"]
        for o in field.get("options") or []
        if isinstance(o, dict)
        and isinstance(o.get("name"), str)
        and isinstance(o.get("id"), str)
        and _NODE_ID.fullmatch(o["id"])
    }
    item_id, field_id = node.get("id"), field.get("id")
    if (
        not isinstance(item_id, str)
        or not _NODE_ID.fullmatch(item_id)
        or not isinstance(field_id, str)
        or not _NODE_ID.fullmatch(field_id)
        or not end_statuses <= set(options)
    ):
        return "refused:status_option_missing"
    assert item is not None
    return _Target(item_id, field_id, item.status_name, options)


def _own_login(runner: Runner) -> str | None:
    result = _run(runner, ["gh", "api", "user", "--jq", ".login"])
    login = result.stdout.strip() if result is not None else ""
    return login if _LOGIN.fullmatch(login) else None


def _marker_present(
    runner: Runner, owner: str, name: str, issue: int, marker: str, login: str
) -> bool | None:
    jq = (
        "[.[] | {login: .user.login, "
        f"marker: (.body | contains({json.dumps(marker)}))}}]"
    )
    for page in range(1, PAGE_CAP + 1):
        argv = [
            "gh",
            "api",
            "--method",
            "GET",
            f"repos/{owner}/{name}/issues/{issue}/comments",
            "-F",
            f"per_page={PAGE_SIZE}",
            "-F",
            f"page={page}",
            "--jq",
            jq,
        ]
        rows = _json(_run(runner, argv))
        if not isinstance(rows, list):
            return None
        if any(
            isinstance(r, dict) and r.get("marker") is True and r.get("login") == login
            for r in rows
        ):
            return True
        if len(rows) < PAGE_SIZE:
            return False
    return None  # a full last page: the answer is unknown, so no new comment


def complete(
    repo: object,
    issue: object,
    project_id: object,
    run_id: object,
    outcome: object,
    summary_path: object,
    runner: Runner,
) -> str:
    """Post the run's result comment and, for ``succeeded``, move the Status; return a closed word."""
    refused = _validate(repo, issue, project_id, run_id, outcome)
    if refused is not None:
        return refused
    assert isinstance(repo, str) and isinstance(issue, int)
    assert isinstance(project_id, str) and isinstance(run_id, int)
    summary = _read_summary(summary_path)
    if summary is None:
        return "refused:bad_summary"
    owner, name = repo.split("/")
    marker = result_marker(issue, run_id)
    assert CLAIM_MARKER not in marker

    target: _Target | None = None
    if outcome == "succeeded":
        nodes = _items(runner, owner, name, issue)
        if nodes is None:
            return "failed:project_read"
        picked = _select(nodes, project_id, set(END_STATUS.values()))
        if isinstance(picked, str):
            return picked
        target = picked

    login = _own_login(runner)
    if login is None:
        return "failed:own_login"
    present = _marker_present(runner, owner, name, issue, marker, login)
    if present is None:
        return "failed:comments_read"
    if not present:
        body = _comment_body(marker, str(outcome), summary)
        posted = _run(
            runner,
            [
                "gh",
                "api",
                "--method",
                "POST",
                f"repos/{owner}/{name}/issues/{issue}/comments",
                "-f",
                f"body={body}",
            ],
        )
        if posted is None:
            return "failed:comment_post"
    if target is None:
        return COMMENTED

    current = target.current
    if current in END_STATUS.values():
        return COMPLETED  # an earlier call already moved it
    if current not in ALLOWED_STATUSES:
        return STATUS_MOVED_BY_PERSON
    move = _json(
        _run(
            runner,
            [
                "gh",
                "api",
                "graphql",
                "-f",
                f"query={MOVE_MUTATION}",
                "-f",
                f"projectId={project_id}",
                "-f",
                f"itemId={target.item_id}",
                "-f",
                f"fieldId={target.field_id}",
                "-f",
                f"optionId={target.options[END_STATUS[current]]}",
            ],
        )
    )
    return COMPLETED if move is not None else "failed:status_move"
