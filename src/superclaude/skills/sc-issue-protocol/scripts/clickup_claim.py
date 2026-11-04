#!/usr/bin/env python3
"""Assign the ClickUp task that tracks a GitHub issue to the token owner.

Standard library only (``urllib``). Called by /sc:issue --claim in Wave 3 as
``clickup_claim.py --issue-url <url> --issue-number <N> --repo <owner/repo>``;
the skill writes stdout to ``.dev/issues/<N>/clickup.json``.

Configuration (environment only):
    CLICKUP_API_TOKEN     required; the person's own personal token (pk_...).
                          Sent only in the Authorization header. Never printed,
                          logged or written to disk.
    CLICKUP_WORKSPACE_ID  required; the workspace (team) ID.
    CLICKUP_LIST_IDS      optional; comma-separated list IDs, sent as
                          ``list_ids[]=<id>`` to narrow the search.
    CLICKUP_MAX_PAGES     optional; page cap for the search, default 20.
                          A value that is not a positive integer (for example
                          ``0``, ``-1``, ``abc`` or empty) is ignored: the
                          default 20 is used and the run continues. Exit code
                          2 stays reserved for bad command-line arguments.

ClickUp API v2 endpoints and the response fields this script relies on
(developer.clickup.com/reference, read 2026-11-04 through Context7 and the web):
    GET https://api.clickup.com/api/v2/user                (getauthorizeduser)
        200 body ``{"user": {"id": <int>, "username": ..., ...}}``; the
        script reads ``user.id``.
    GET https://api.clickup.com/api/v2/team/{team_Id}/task (getfilteredteamtasks)
        query ``page`` ("Page to fetch (starts at 0)", so the first page is
        0), ``subtasks=true``, ``include_markdown_description=true`` and
        optional ``list_ids[]``. At most 100 tasks per page; closed tasks are
        excluded by default. 200 body ``{"tasks": [<task>, ...]}``; per task
        the script reads ``id``, ``name``, ``url``, ``markdown_description``
        (``description`` when it is absent), ``assignees[].id`` and
        ``custom_fields[].value``. An empty ``tasks`` list ends the search.
        Reaching the page cap before an empty page means the search did not
        see every task, so it ends with ``error``/``page_cap`` and nothing is
        assigned: a match found on the fetched pages may not be the only one.
    PUT https://api.clickup.com/api/v2/task/{task_id}       (updatetask)
        body ``{"assignees": {"add": [<user id>]}}``; a 2xx status means the
        assignment was made (the 200 body carries the task ``id``).
    Authentication: header ``Authorization: <personal token>``.

Matching (design default D2):
    Rule 1, GitHub link: the markdown description or any custom field value
    contains ``https://github.com/<owner>/<repo>/issues/<N>``, compared
    case-insensitively, not followed by another digit (so a trailing ``/`` or
    ``#...`` is ignored and ``/issues/3020`` does not match ``/issues/302``).
    Rule 2, only when rule 1 found nothing: the task name contains ``#<N>`` as
    a whole token, not followed by a digit.

Output: one JSON object on stdout, always exit 0 except for bad arguments:
    {"status": "skipped", "reason": "no_token"|"no_workspace"}
    {"status": "not_found"}
    {"status": "ambiguous", "rule": ..., "candidates": [{"task_id", "task_url"}, ...]}
    {"status": "already_assigned", "task_id", "task_url", "rule"}
    {"status": "assigned", "task_id", "task_url", "rule": "github_link"|"title_number"}
    {"status": "error", "reason": "auth"|"rate_limited"|"page_cap"|"<short>"}
HTTP 401/403 gives ``auth``. HTTP 429 waits the ``Retry-After`` seconds once,
retries once, then gives ``rate_limited``. Bad arguments exit 2 (argparse).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.clickup.com/api/v2"
DEFAULT_MAX_PAGES = 20
FIRST_PAGE = 0
TIMEOUT_SECONDS = 30
_REPO = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")


class ClickUpError(Exception):
    """A failure reported as ``{"status": "error", "reason": <reason>}``."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def max_pages_from_env(value: str | None) -> int:
    """Return the page cap; anything but a positive integer gives the default."""
    try:
        pages = int((value or "").strip())
    except ValueError:
        return DEFAULT_MAX_PAGES
    return pages if pages > 0 else DEFAULT_MAX_PAGES


def _retry_after(headers) -> float:
    try:
        return max(0.0, float(headers.get("Retry-After", "1")))
    except (TypeError, ValueError):
        return 1.0


def request(method: str, url: str, token: str, body: dict | None = None):
    """Send one request and return the decoded JSON body (or ``{}``)."""
    data = None if body is None else json.dumps(body).encode("utf-8")
    for attempt in (1, 2):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", token)
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise ClickUpError("auth") from None
            if exc.code == 429:
                if attempt == 1:
                    time.sleep(_retry_after(exc.headers or {}))
                    continue
                raise ClickUpError("rate_limited") from None
            raise ClickUpError(f"http_{exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise ClickUpError("network") from None
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ClickUpError("bad_response") from None
    raise ClickUpError("rate_limited")  # pragma: no cover


def _strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    if value is None or isinstance(value, bool):
        return []
    return [str(value)]


def match_rule(task: dict, issue_url: str, number: int) -> str | None:
    """Return ``github_link``, ``title_number`` or ``None`` for one task."""
    link = re.compile(re.escape(issue_url.rstrip("/")) + r"(?![0-9])", re.IGNORECASE)
    texts = _strings(task.get("markdown_description") or task.get("description") or "")
    for field in task.get("custom_fields") or []:
        if isinstance(field, dict):
            texts.extend(_strings(field.get("value")))
    if any(link.search(text) for text in texts):
        return "github_link"
    title = re.compile(rf"(?<![\w#])#{number}(?![0-9])")
    if title.search(str(task.get("name") or "")):
        return "title_number"
    return None


def claim(issue_url: str, number: int, env: dict) -> dict:
    token = (env.get("CLICKUP_API_TOKEN") or "").strip()
    if not token:
        return {"status": "skipped", "reason": "no_token"}
    workspace = (env.get("CLICKUP_WORKSPACE_ID") or "").strip()
    if not workspace:
        return {"status": "skipped", "reason": "no_workspace"}
    max_pages = max_pages_from_env(env.get("CLICKUP_MAX_PAGES"))
    list_ids = [
        s.strip() for s in (env.get("CLICKUP_LIST_IDS") or "").split(",") if s.strip()
    ]

    try:
        user = request("GET", f"{API}/user", token)
        user_id = (user.get("user") or {}).get("id")
        if user_id is None:
            raise ClickUpError("bad_response")

        found: dict[str, list[dict]] = {"github_link": [], "title_number": []}
        seen: set[str] = set()
        complete = False  # True only when an empty page ended the search
        for page in range(FIRST_PAGE, FIRST_PAGE + max_pages):
            query = [
                ("page", str(page)),
                ("subtasks", "true"),
                ("include_markdown_description", "true"),
            ] + [("list_ids[]", list_id) for list_id in list_ids]
            url = f"{API}/team/{urllib.parse.quote(workspace, safe='')}/task?{urllib.parse.urlencode(query)}"
            tasks = request("GET", url, token).get("tasks") or []
            if not tasks:
                complete = True
                break
            for task in tasks:
                task_id = str(task.get("id") or "")
                if not task_id or task_id in seen:
                    continue
                seen.add(task_id)
                rule = match_rule(task, issue_url, number)
                if rule:
                    found[rule].append(task)
        if not complete:
            # The cap stopped the search: a later page could hold another
            # match, so "exactly one match" cannot be checked (design D2).
            return {"status": "error", "reason": "page_cap"}

        rule = "github_link" if found["github_link"] else "title_number"
        matches = found[rule]
        if not matches:
            return {"status": "not_found"}
        if len(matches) > 1:
            return {
                "status": "ambiguous",
                "rule": rule,
                "candidates": [
                    {"task_id": str(t.get("id")), "task_url": t.get("url")}
                    for t in matches
                ],
            }
        task = matches[0]
        result = {
            "task_id": str(task.get("id")),
            "task_url": task.get("url"),
            "rule": rule,
        }
        assignees = {
            str(a.get("id")) for a in task.get("assignees") or [] if isinstance(a, dict)
        }
        if str(user_id) in assignees:
            return {"status": "already_assigned", **result}
        request(
            "PUT",
            f"{API}/task/{urllib.parse.quote(result['task_id'], safe='')}",
            token,
            {"assignees": {"add": [user_id]}},
        )
        return {"status": "assigned", **result}
    except ClickUpError as exc:
        return {"status": "error", "reason": exc.reason}
    except Exception:  # never let a traceback (and anything in it) reach output
        return {"status": "error", "reason": "unexpected"}


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--issue-url", required=True)
    parser.add_argument("--issue-number", required=True, type=int)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args(argv)
    if args.issue_number <= 0:
        parser.error("--issue-number must be a positive integer")
    if not _REPO.match(args.repo):
        parser.error("--repo must be owner/repo")
    expected = f"https://github.com/{args.repo}/issues/{args.issue_number}"
    if args.issue_url.rstrip("/").lower() != expected.lower():
        parser.error(f"--issue-url must be {expected}")
    args.issue_url = expected
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = claim(args.issue_url, args.issue_number, os.environ)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
