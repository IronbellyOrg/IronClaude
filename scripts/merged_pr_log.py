#!/usr/bin/env python3
"""Daily log of merged pull requests, per day and per person, across two GitHub orgs.

Adapted from ``scripts/build-fleet-daily-digest.py`` by Jay Wedgeworth
(Simple-With-Us/AI-Fleet-Coordinator), which is licensed under the Apache License,
Version 2.0. This file was modified: it reads two orgs instead of one owner, lists
every non-archived repo fresh on each run, credits the person who made the branch
and submitted the pull request, and publishes the digest to a ClickUp Doc page. The
issue feed, the calendar feed, the public repo allowlist and every title-parsing
feature of the original were removed.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or
agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing permissions and
limitations under the License.

Environment (names only; credentials are read from the environment and nowhere else):
  GH_TOKEN               token that can read pull requests in both orgs (required)
  CLICKUP_API_TOKEN      ClickUp personal token (required unless --dry-run)
  CLICKUP_WORKSPACE_ID   ClickUp workspace id (required unless --dry-run)
  CLICKUP_DOC_ID         ClickUp Doc id (required unless --dry-run)
  CLICKUP_PAGE_ID        ClickUp page id inside that Doc (required unless --dry-run)
  DIGEST_TZ              time zone for day buckets (default America/Chicago)
  DIGEST_LOOKBACK_DAYS   lookback in days (default 21)

Usage:
  python3 scripts/merged_pr_log.py --out <dir> [--dry-run]
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ORGS = ("IronbellyOrg", "IronbellyGroup")

# Login to person. A login that is not here and is not a bot is shown as the login.
# Never guess a person: add a row only when the owner says who a login is.
LOGIN_TO_PERSON = {
    "clayphi": "Clay",
    "ironbelly": "Ryan",
    "IBC-ChrisG": "Chris",
    "IB-Lea": "Leandro",
    "swill-ib": "William",
}
_PERSON_BY_LOGIN = {login.casefold(): name for login, name in LOGIN_TO_PERSON.items()}
API_ROOT = "https://api.github.com"
CLICKUP_API_ROOT = "https://api.clickup.com/api"
CLICKUP_VARS = (
    "CLICKUP_API_TOKEN",
    "CLICKUP_WORKSPACE_ID",
    "CLICKUP_DOC_ID",
    "CLICKUP_PAGE_ID",
)
DEFAULT_TZ = "America/Chicago"
DEFAULT_LOOKBACK_DAYS = 21
PAGE_SIZE = 100
USER_AGENT = "merged-pr-log"

# get(path, params=None) -> decoded JSON. Production wiring is make_get(); tests pass a
# fake that serves recorded responses.
GetFn = Callable[..., Any]


class GitHubError(RuntimeError):
    """A GitHub request failed. The message holds the status and path, never a token."""


def env_int(env: Mapping[str, str], name: str, default: int) -> int:
    raw = (env.get(name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        raise SystemExit(f"error: {name} must be a whole number, got {raw!r}") from None


def token(env: Mapping[str, str]) -> str:
    """Return GH_TOKEN. There is deliberately no fallback to any stored login."""
    value = (env.get("GH_TOKEN") or "").strip()
    if not value:
        raise SystemExit(
            "error: GH_TOKEN is not set. Set it to a token that can read pull requests "
            "in both orgs; this script never falls back to a stored login."
        )
    return value


def settings(env: Mapping[str, str]) -> tuple[ZoneInfo, int]:
    """Return (time zone, lookback days) from DIGEST_TZ and DIGEST_LOOKBACK_DAYS."""
    tz_name = (env.get("DIGEST_TZ") or "").strip() or DEFAULT_TZ
    try:
        tz = ZoneInfo(tz_name)
    except (ZoneInfoNotFoundError, ValueError):
        raise SystemExit(
            f"error: DIGEST_TZ {tz_name!r} is not a known time zone"
        ) from None
    return tz, env_int(env, "DIGEST_LOOKBACK_DAYS", DEFAULT_LOOKBACK_DAYS)


def window_start(now: datetime, tz: ZoneInfo, lookback_days: int) -> date:
    """First local day of the window, computed the way the original `main` does."""
    return now.astimezone(tz).date() - timedelta(days=lookback_days)


def make_get(tok: str) -> GetFn:
    """Build the production GET function (urllib, REST). The token goes in a header."""

    def get(path: str, params: Mapping[str, Any] | None = None) -> Any:
        url = API_ROOT + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {tok}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": USER_AGENT,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise GitHubError(f"GitHub returned HTTP {exc.code} for {path}") from None
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            raise GitHubError(f"GitHub request failed for {path}: {exc}") from None

    return get


def gh_pages(
    get: GetFn,
    path: str,
    params: Mapping[str, Any] | None = None,
    max_pages: int = 10,
) -> Iterator[list[dict[str, Any]]]:
    """Yield one page at a time. A short page ends the list.

    Unlike the original, an error or an unexpected shape is raised, never skipped, and
    running out of pages while pages are still full is an error too: a log built from
    a partial list must not replace the page that is already published.
    """
    for page in range(1, max_pages + 1):
        data = get(path, {**(params or {}), "page": page, "per_page": PAGE_SIZE})
        if not isinstance(data, list):
            raise GitHubError(f"unexpected response for {path}: expected a list")
        yield data
        if len(data) < PAGE_SIZE:
            return
    raise GitHubError(
        f"{path} has more than {max_pages} pages; refusing a partial list"
    )


def gh_list(
    get: GetFn,
    path: str,
    params: Mapping[str, Any] | None = None,
    max_pages: int = 10,
) -> list[dict[str, Any]]:
    return [item for page in gh_pages(get, path, params, max_pages) for item in page]


def parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def to_local_day(dt: datetime, tz: ZoneInfo) -> date:
    return dt.astimezone(tz).date()


def list_repos(get: GetFn, orgs: tuple[str, ...] = ORGS) -> list[tuple[str, str]]:
    """Every non-archived repo of every org, public and private, listed fresh each call.

    Nothing is cached or stored, so a repo created after the last run appears on the
    next one with no edit.
    """
    repos: list[tuple[str, str]] = []
    for org in orgs:
        for item in gh_list(get, f"/orgs/{org}/repos", {"type": "all"}, max_pages=20):
            if item.get("archived"):
                continue
            name = item.get("name")
            if name:
                repos.append((org, name))
    return sorted(repos)


def fetch_merged_prs(
    get: GetFn, org: str, repo: str, since: date, tz: ZoneInfo
) -> list[dict[str, Any]]:
    """Merged PRs of one repo whose merge day (in ``tz``) is on or after ``since``.

    Reads the REST pulls list (closed, newest update first), which does not touch the
    search API. The list is ordered by ``updated_at``, which is never earlier than
    ``merged_at``, so the first PR last updated before the window ends the scan. The
    PR's merger is never read.
    """
    out: list[dict[str, Any]] = []
    path = f"/repos/{org}/{repo}/pulls"
    params = {"state": "closed", "sort": "updated", "direction": "desc"}
    for page in gh_pages(get, path, params, max_pages=10):
        for item in page:
            updated = parse_iso(item.get("updated_at"))
            if updated and to_local_day(updated, tz) < since:
                return out
            merged = parse_iso(item.get("merged_at"))
            if not merged or to_local_day(merged, tz) < since:
                continue
            user = item.get("user") or {}
            number = item.get("number")
            out.append(
                {
                    "org": org,
                    "repo": repo,
                    "number": number,
                    "title": (item.get("title") or "").strip(),
                    "url": item.get("html_url")
                    or f"https://github.com/{org}/{repo}/pull/{number}",
                    "user": user.get("login"),
                    "user_type": user.get("type"),
                    "when": merged,
                }
            )
    return out


def is_bot(login: str | None, user_type: str | None = None) -> bool:
    """A bot account has the type Bot or a login that ends in [bot]."""
    return user_type == "Bot" or (login or "").endswith("[bot]")


def person_name(login: str) -> str:
    """The person on file for a login (case does not matter), else the login itself."""
    return _PERSON_BY_LOGIN.get(login.casefold(), login)


def credit_for_pr(get: GetFn, org: str, repo: str, pr: Mapping[str, Any]) -> str | None:
    """Who a merged PR is credited to, or None when no person is behind it.

    Credit goes to the person who made the branch and submitted the PR, never to
    whoever merged it: the merger is not an input here. A PR opened by a person credits
    that login. A PR opened by a bot credits the author of the branch's commits (the
    first commit, in order, whose author login is not a bot). A bot never gets credit,
    and a PR made wholly by bots returns None so it is counted on its own line.
    """
    login = pr.get("user")
    if login and not is_bot(login, pr.get("user_type")):
        return person_name(login)
    path = f"/repos/{org}/{repo}/pulls/{pr['number']}/commits"
    for commit in gh_list(get, path, max_pages=3):
        author = commit.get("author") or {}
        author_login = author.get("login")
        if author_login and not is_bot(author_login, author.get("type")):
            return person_name(author_login)
    return None


@dataclass
class DayBucket:
    day: date
    by_person: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    no_person: list[dict[str, Any]] = field(default_factory=list)

    def total(self) -> int:
        return sum(len(prs) for prs in self.by_person.values()) + len(self.no_person)

    def is_empty(self) -> bool:
        return self.total() == 0

    def counts_line(self) -> str:
        n = self.total()
        return f"{n} PR{'' if n == 1 else 's'} merged"


def _pr_order(pr: Mapping[str, Any]) -> tuple[str, str, int]:
    return (pr["org"], pr["repo"], pr.get("number") or 0)


def bucket_all(
    credited: list[tuple[dict[str, Any], str | None]], tz: ZoneInfo
) -> dict[date, DayBucket]:
    """Group credited PRs by local merge day in ``tz``, then by person.

    PRs credited to nobody go in the day's own ``no_person`` list. Days come back
    newest first, people alphabetically, PRs by repo then number.
    """
    buckets: dict[date, DayBucket] = {}
    for pr, person in credited:
        day = to_local_day(pr["when"], tz)
        bucket = buckets.setdefault(day, DayBucket(day=day))
        if person is None:
            bucket.no_person.append(pr)
        else:
            bucket.by_person.setdefault(person, []).append(pr)
    for bucket in buckets.values():
        bucket.no_person.sort(key=_pr_order)
        bucket.by_person = {
            person: sorted(prs, key=_pr_order)
            for person, prs in sorted(
                bucket.by_person.items(), key=lambda item: item[0].casefold()
            )
        }
    return dict(sorted(buckets.items(), reverse=True))


_MD_ESCAPES = str.maketrans({ch: "\\" + ch for ch in "\\[]<>*_`"})
NO_PERSON = "No person"


def md_escape(text: str) -> str:
    """Escape the characters that would turn PR text into markdown or a raw tag."""
    return text.translate(_MD_ESCAPES)


def pr_ref(pr: Mapping[str, Any]) -> str:
    return f"{pr['org']}/{pr['repo']}#{pr['number']}"


def _safe_href(url: str) -> str:
    return url if url.startswith("https://") else "#"


def _format_day_heading(d: date) -> str:
    """Human day heading, e.g. 'August 10, 2026' (no leading zero on the day)."""
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def _format_created_lede(generated: datetime, tz: ZoneInfo) -> str:
    """Subheading timestamp, e.g. 'Created: Aug 9, 2026 at 10:22pm'."""
    local = generated.astimezone(tz)
    hour12 = local.hour % 12 or 12
    ampm = "am" if local.hour < 12 else "pm"
    return (
        f"Created: {local.strftime('%b')} {local.day}, {local.year} "
        f"at {hour12}:{local.strftime('%M')}{ampm}"
    )


def _context_line(tz: ZoneInfo, since: date, repos_scanned: int) -> str:
    return (
        f"time zone {tz.key} · lookback window from {since.isoformat()} · "
        f"{repos_scanned} repos scanned"
    )


def build_markdown(
    days: list[DayBucket],
    generated: datetime,
    tz: ZoneInfo,
    since: date,
    repos_scanned: int,
) -> str:
    stamp = generated.astimezone(tz).strftime("%Y-%m-%d %H:%M %Z")
    lines = [
        "# Merged pull requests, by day and person",
        "",
        f"_Generated {stamp} · {_context_line(tz, since, repos_scanned)}_",
        "",
        "Credit goes to the person who made the branch and submitted the pull "
        "request. A pull request made wholly by a bot is listed under "
        f"{NO_PERSON}.",
        "",
    ]
    shown = [day for day in days if not day.is_empty()]
    if not shown:
        lines += ["_No merged pull requests in the window._", ""]
    for day in shown:
        lines += [f"## {day.day.isoformat()}", "", f"*{day.counts_line()}*", ""]
        groups = list(day.by_person.items())
        if day.no_person:
            groups.append((NO_PERSON, day.no_person))
        for name, prs in groups:
            lines += [f"### {md_escape(name)} ({len(prs)})", ""]
            lines += [
                f"- [{md_escape(pr_ref(p))}]({p['url']}): {md_escape(p['title'])}"
                for p in prs
            ]
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


_PAGE_CSS = """
    :root {
      --bg: #f4f6f9; --card: #ffffff; --text: #1a2332; --muted: #5b6b82;
      --accent: #0f766e; --link: #0369a1; --border: #e2e8f0;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto,
        Helvetica, Arial, sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.5;
      padding: 1.5rem clamp(1rem, 4vw, 2.5rem) 3rem;
      max-width: 54rem; margin-inline: auto;
    }
    h1 { font-size: 1.6rem; margin: 0 0 0.35rem; letter-spacing: -0.02em; }
    h2 { font-size: 1.2rem; margin: 0 0 0.35rem; color: var(--accent); }
    h3 {
      font-size: 0.8rem; margin: 1rem 0 0.4rem; color: var(--muted);
      text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;
    }
    .lede { color: var(--muted); margin: 0 0 1rem; }
    .links { margin-bottom: 1.5rem; font-size: 0.95rem; }
    a { color: var(--link); text-decoration: underline; }
    .day {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 12px; padding: 1rem 1.15rem 1.15rem; margin-bottom: 1rem;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    details.day > summary { cursor: pointer; }
    .meta { color: var(--muted); font-size: 0.9rem; margin: 0 0 0.5rem; }
    ul { margin: 0.25rem 0 0; padding-left: 0; list-style: none; }
    li { margin: 0.35rem 0; padding: 0.35rem 0.5rem; border-radius: 8px;
      overflow-wrap: anywhere; }
    li:nth-child(even) { background: #f8fafc; }
    footer { margin-top: 2rem; color: var(--muted); font-size: 0.85rem; }
    code { font-size: 0.85em; background: #e2e8f0; padding: 0.1em 0.35em;
      border-radius: 4px; color: #0f172a; }
    @media (prefers-color-scheme: dark) {
      :root { --bg: #0f172a; --card: #1e293b; --text: #e2e8f0; --muted: #94a3b8;
        --link: #7dd3fc; --border: #334155; }
      li:nth-child(even) { background: #0f172a; }
      code { background: #334155; color: #e2e8f0; }
    }
"""


def build_html(
    days: list[DayBucket],
    generated: datetime,
    tz: ZoneInfo,
    since: date,
    repos_scanned: int,
) -> str:
    esc = html.escape

    def item(pr: Mapping[str, Any]) -> str:
        link = f'<a href="{esc(_safe_href(pr["url"]))}">{esc(pr_ref(pr))}</a>'
        return f"<li>{link}: {esc(pr['title'])}</li>"

    def block(name: str, prs: list[dict[str, Any]]) -> str:
        return (
            f"<h3>{esc(name)} ({len(prs)})</h3><ul>"
            + "".join(item(p) for p in prs)
            + "</ul>"
        )

    sections: list[str] = []
    for index, day in enumerate(d for d in days if not d.is_empty()):
        blocks = [block(name, prs) for name, prs in day.by_person.items()]
        if day.no_person:
            blocks.append(block(NO_PERSON, day.no_person))
        label = esc(_format_day_heading(day.day))
        meta = f'<p class="meta">{esc(day.counts_line())}</p>'
        anchor = day.day.isoformat()
        if index == 0:
            sections.append(
                f'<section class="day" id="{anchor}"><h2>{label}</h2>{meta}'
                + "".join(blocks)
                + "</section>"
            )
        else:
            # Older days collapse so the page stays scannable; the content is still in
            # the page.
            sections.append(
                f'<details class="day" id="{anchor}"><summary><h2>{label}</h2>'
                f"{meta}</summary>" + "".join(blocks) + "</details>"
            )
    body = "\n".join(sections) or "<p>No merged pull requests in the window.</p>"
    lede = esc(f"{_format_created_lede(generated, tz)} · ")
    lede += esc(_context_line(tz, since, repos_scanned))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Merged pull requests</title>
  <style>{_PAGE_CSS}  </style>
</head>
<body>
  <h1>Merged pull requests, by day and person</h1>
  <p class="lede">{lede}</p>
  <nav class="links"><a href="digest.md">Markdown</a></nav>
  {body}
  <footer>
    Built by <code>scripts/merged_pr_log.py</code>, adapted from Jay Wedgeworth's
    daily digest generator (Apache-2.0). Credit goes to the person who made the
    branch and submitted the pull request; a pull request made wholly by a bot is
    listed under {NO_PERSON}.
  </footer>
</body>
</html>
"""


class ClickUpError(RuntimeError):
    """A ClickUp request failed. The message holds the status and path, never a token."""


def make_clickup_put(tok: str) -> Callable[[str, Mapping[str, Any]], None]:
    """Build the production PUT function for ClickUp (personal token, no Bearer)."""

    def put(path: str, body: Mapping[str, Any]) -> None:
        req = urllib.request.Request(
            CLICKUP_API_ROOT + path,
            data=json.dumps(body).encode("utf-8"),
            method="PUT",
            headers={
                "Authorization": tok,
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60):
                return None
        except urllib.error.HTTPError as exc:
            raise ClickUpError(f"ClickUp returned HTTP {exc.code} for {path}") from None
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ClickUpError(f"ClickUp request failed for {path}: {exc}") from None

    return put


def publish_clickup(
    put: Callable[[str, Mapping[str, Any]], Any],
    env: Mapping[str, str],
    markdown: str,
) -> None:
    """Replace the content of one ClickUp Doc page with the markdown digest."""
    ids = [
        urllib.parse.quote((env.get(name) or "").strip(), safe="")
        for name in ("CLICKUP_WORKSPACE_ID", "CLICKUP_DOC_ID", "CLICKUP_PAGE_ID")
    ]
    path = "/v3/workspaces/{}/docs/{}/pages/{}".format(*ids)
    put(
        path,
        {
            "content": markdown,
            "content_format": "text/md",
            "content_edit_mode": "replace",
        },
    )


def missing_env(env: Mapping[str, str], dry_run: bool) -> list[str]:
    """Names of required variables that are unset or blank."""
    names = ["GH_TOKEN"] + ([] if dry_run else list(CLICKUP_VARS))
    return [name for name in names if not (env.get(name) or "").strip()]


def print_rate_limit(get: GetFn, label: str) -> None:
    """Print the remaining request budget (this call does not count against it)."""
    resources = (get("/rate_limit") or {}).get("resources") or {}
    parts = []
    for name in ("core", "graphql", "search"):
        res = resources.get(name) or {}
        parts.append(f"{name}={res.get('remaining')}/{res.get('limit')}")
    print(f"rate limit {label}: " + " ".join(parts))


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="merged_pr_log",
        description="Build the per-day, per-person log of merged pull requests.",
    )
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="folder that receives index.html and digest.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="build the files and print the rate limit before and after; "
        "do not call ClickUp (only GH_TOKEN is required)",
    )
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
    env: Mapping[str, str] | None = None,
    get: GetFn | None = None,
    put: Callable[[str, Mapping[str, Any]], Any] | None = None,
    now: datetime | None = None,
) -> int:
    args = parse_args(argv)
    env = os.environ if env is None else env
    missing = missing_env(env, args.dry_run)
    if missing:
        raise SystemExit(
            "error: missing environment variable(s): "
            + ", ".join(missing)
            + ". Credentials and ids are read from the environment only."
        )
    tz, lookback = settings(env)
    get = get or make_get(token(env))
    now = now or datetime.now(timezone.utc)
    since = window_start(now, tz, lookback)

    try:
        if args.dry_run:
            print_rate_limit(get, "before")
        repos = list_repos(get)
        credited = []
        for org, repo in repos:
            for pr in fetch_merged_prs(get, org, repo, since, tz):
                credited.append((pr, credit_for_pr(get, org, repo, pr)))
        if args.dry_run:
            print_rate_limit(get, "after")
    except Exception as exc:
        # Nothing is written or published from a partial read.
        print(
            f"error: reading GitHub failed ({type(exc).__name__}): {exc}",
            file=sys.stderr,
        )
        return 1

    days = list(bucket_all(credited, tz).values())
    markdown = build_markdown(days, now, tz, since, len(repos))
    page = build_html(days, now, tz, since, len(repos))
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "digest.md").write_text(markdown, encoding="utf-8")
    (args.out / "index.html").write_text(page, encoding="utf-8")
    print(
        f"wrote {args.out / 'index.html'} and {args.out / 'digest.md'}: "
        f"{len(credited)} merged PRs on {len(days)} days from {len(repos)} repos"
    )
    if args.dry_run:
        print("dry run: ClickUp was not called")
        return 0

    try:
        put = put or make_clickup_put(env["CLICKUP_API_TOKEN"].strip())
        publish_clickup(put, env, markdown)
    except Exception as exc:
        print(
            f"error: publishing to ClickUp failed ({type(exc).__name__}): {exc}",
            file=sys.stderr,
        )
        return 1
    print("published the digest to ClickUp")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
