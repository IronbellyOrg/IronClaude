"""Tests for scripts/merged_pr_log.py.

The JSON under tests/merged_pr_log/fixtures/ is hand-written in the GitHub REST
response shape, trimmed to the fields the script reads (plus ``merged_by``, which the
script must never read). No authorized capture of live responses existed when these
were written, so none of the fixtures is a literal recording.

Environment values used here are the obvious placeholder below, never a real token.
"""

import ast
import importlib.util
import json
import re
import sys
import urllib.error
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "merged_pr_log.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

_spec = importlib.util.spec_from_file_location("merged_pr_log", SCRIPT)
mod = importlib.util.module_from_spec(_spec)
sys.modules["merged_pr_log"] = mod
_spec.loader.exec_module(mod)

PLACEHOLDER = "placeholder-not-a-secret"
CHICAGO = ZoneInfo("America/Chicago")
NOW = datetime(2026, 11, 19, 18, 0, tzinfo=timezone.utc)  # 12:00 in Chicago
SINCE = date(2026, 10, 29)  # 21 days before 2026-11-19


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class FakeGitHub:
    """Serves recorded-shape responses by request path and keeps the call list."""

    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def __call__(self, path, params=None):
        self.calls.append(path)
        if path not in self.routes:
            raise mod.GitHubError(f"GitHub returned HTTP 404 for {path}")
        data = self.routes[path]
        if isinstance(data, list):
            page = (params or {}).get("page", 1)
            start = (page - 1) * mod.PAGE_SIZE
            return data[start : start + mod.PAGE_SIZE]
        return data


def routes(run=1):
    """Responses for one run. Run 2 lists one more repo in IronbellyGroup."""
    served = {
        "/orgs/IronbellyOrg/repos": load("orgs/IronbellyOrg-repos-run1.json"),
        "/orgs/IronbellyGroup/repos": load(f"orgs/IronbellyGroup-repos-run{run}.json"),
        "/repos/IronbellyOrg/alpha/pulls": load("pulls/IronbellyOrg-alpha.json"),
        "/repos/IronbellyOrg/beta-private/pulls": load(
            "pulls/IronbellyOrg-beta-private.json"
        ),
        "/repos/IronbellyOrg/quiet/pulls": load("pulls/IronbellyOrg-quiet.json"),
        "/repos/IronbellyGroup/gamma/pulls": load("pulls/IronbellyGroup-gamma.json"),
        # Branch commits, read only for PRs opened by a bot.
        "/repos/IronbellyOrg/alpha/pulls/103/commits": load(
            "commits/IronbellyOrg-alpha-103.json"
        ),
        "/repos/IronbellyOrg/alpha/pulls/104/commits": load(
            "commits/IronbellyOrg-alpha-104.json"
        ),
        "/rate_limit": load("rate_limit.json"),
    }
    if run == 2:
        served["/repos/IronbellyGroup/delta-new/pulls"] = load(
            "pulls/IronbellyGroup-delta-new.json"
        )
    return served


# --- token and settings ----------------------------------------------------------


def test_token_requires_gh_token_and_never_falls_back():
    with pytest.raises(SystemExit) as exc:
        mod.token({"GITHUB_TOKEN": PLACEHOLDER})
    assert "GH_TOKEN" in str(exc.value)
    assert PLACEHOLDER not in str(exc.value)


@pytest.mark.parametrize("env", [{}, {"GH_TOKEN": ""}, {"GH_TOKEN": "   "}])
def test_token_rejects_missing_or_blank(env):
    with pytest.raises(SystemExit) as exc:
        mod.token(env)
    assert "GH_TOKEN" in str(exc.value)


def test_token_returns_the_value():
    assert mod.token({"GH_TOKEN": f" {PLACEHOLDER} "}) == PLACEHOLDER


def test_settings_defaults_and_overrides():
    tz, days = mod.settings({})
    assert tz.key == "America/Chicago"
    assert days == 21
    tz, days = mod.settings({"DIGEST_TZ": "Asia/Tokyo", "DIGEST_LOOKBACK_DAYS": "7"})
    assert (tz.key, days) == ("Asia/Tokyo", 7)


def test_settings_reject_bad_values():
    with pytest.raises(SystemExit, match="DIGEST_TZ"):
        mod.settings({"DIGEST_TZ": "Not/AZone"})
    with pytest.raises(SystemExit, match="DIGEST_LOOKBACK_DAYS"):
        mod.settings({"DIGEST_LOOKBACK_DAYS": "three"})


def test_window_start_is_lookback_days_before_the_local_today():
    assert mod.window_start(NOW, CHICAGO, 21) == SINCE


# --- request layer ---------------------------------------------------------------


def test_make_get_sends_the_token_only_in_a_header(monkeypatch):
    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b"[]"

    def fake_urlopen(req, timeout):
        captured["req"] = req
        return Response()

    monkeypatch.setattr(mod.urllib.request, "urlopen", fake_urlopen)
    assert mod.make_get(PLACEHOLDER)("/orgs/x/repos", {"page": 1}) == []
    req = captured["req"]
    assert PLACEHOLDER not in req.full_url
    assert req.get_header("Authorization") == f"Bearer {PLACEHOLDER}"


def test_make_get_turns_http_errors_into_github_error_without_the_token(monkeypatch):
    def fake_urlopen(req, timeout):
        raise urllib.error.HTTPError(req.full_url, 403, "forbidden", {}, None)

    monkeypatch.setattr(mod.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(mod.GitHubError) as exc:
        mod.make_get(PLACEHOLDER)("/orgs/x/repos")
    assert "403" in str(exc.value)
    assert PLACEHOLDER not in str(exc.value)


def test_gh_list_raises_when_pages_run_out_while_still_full():
    full = [{"name": f"r{i}"} for i in range(mod.PAGE_SIZE)]
    with pytest.raises(mod.GitHubError, match="more than 2 pages"):
        mod.gh_list(lambda path, params=None: full, "/x", max_pages=2)


def test_gh_list_raises_on_an_unexpected_shape():
    with pytest.raises(mod.GitHubError, match="expected a list"):
        mod.gh_list(lambda path, params=None: {"message": "nope"}, "/x")


# --- repo listing ----------------------------------------------------------------


def test_list_repos_covers_both_orgs_private_included_archived_excluded():
    fake = FakeGitHub(routes())
    repos = mod.list_repos(fake)
    assert repos == [
        ("IronbellyGroup", "gamma"),
        ("IronbellyOrg", "alpha"),
        ("IronbellyOrg", "beta-private"),
        ("IronbellyOrg", "quiet"),
    ]
    assert ("IronbellyOrg", "old-archived") not in repos


def test_repo_added_after_the_first_run_appears_with_no_edit():
    first = mod.list_repos(FakeGitHub(routes(run=1)))
    second = mod.list_repos(FakeGitHub(routes(run=2)))
    assert ("IronbellyGroup", "delta-new") not in first
    assert ("IronbellyGroup", "delta-new") in second
    assert set(first) < set(second)


def test_archived_repo_is_never_requested():
    fake = FakeGitHub(routes())
    for org, repo in mod.list_repos(fake):
        mod.fetch_merged_prs(fake, org, repo, SINCE, CHICAGO)
    assert not any("old-archived" in call for call in fake.calls)


# --- merged PR window ------------------------------------------------------------


def test_fetch_merged_prs_keeps_the_window_and_drops_unmerged_and_older():
    prs = mod.fetch_merged_prs(
        FakeGitHub(routes()), "IronbellyOrg", "alpha", SINCE, CHICAGO
    )
    assert [p["number"] for p in prs] == [101, 103, 102, 104]
    first = prs[0]
    assert first["url"] == "https://github.com/IronbellyOrg/alpha/pull/101"
    assert first["user"] == "clayphi"
    assert first["title"] == "Add login form"
    assert "merged_by" not in first


def test_repo_with_no_merges_gives_an_empty_list():
    prs = mod.fetch_merged_prs(
        FakeGitHub(routes()), "IronbellyOrg", "quiet", SINCE, CHICAGO
    )
    assert prs == []


def test_window_edge_is_the_first_local_day():
    pulls = [
        {
            "number": 2,
            "title": "inside",
            "merged_at": "2026-10-29T06:00:00Z",  # 01:00 on 10-29 in Chicago
            "updated_at": "2026-10-29T06:01:00Z",
            "user": {"login": "clayphi", "type": "User"},
        },
        {
            "number": 1,
            "title": "just outside",
            "merged_at": "2026-10-29T04:00:00Z",  # 23:00 on 10-28 in Chicago
            "updated_at": "2026-10-29T04:01:00Z",
            "user": {"login": "clayphi", "type": "User"},
        },
    ]
    fake = FakeGitHub({"/repos/o/r/pulls": pulls})
    prs = mod.fetch_merged_prs(fake, "o", "r", SINCE, CHICAGO)
    assert [p["number"] for p in prs] == [2]


# --- structure -------------------------------------------------------------------


def test_script_imports_only_the_standard_library_and_has_no_subprocess():
    source = SCRIPT.read_text(encoding="utf-8")
    assert "subprocess" not in source
    imported = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            imported.add(node.module.split(".")[0])
    assert imported <= set(sys.stdlib_module_names)


# --- credit rule and bucketing ---------------------------------------------------


def collect(fake, since=SINCE, tz=CHICAGO):
    """List repos, read merged PRs and credit each one, as `main` does."""
    credited = []
    for org, repo in mod.list_repos(fake):
        for pr in mod.fetch_merged_prs(fake, org, repo, since, tz):
            credited.append((pr, mod.credit_for_pr(fake, org, repo, pr)))
    return credited


def pr_by_number(credited, number, repo="alpha"):
    return next(
        (pr, who)
        for pr, who in credited
        if pr["number"] == number and pr["repo"] == repo
    )


def opened_by(login, user_type="User", number=9):
    return {
        "org": "o",
        "repo": "r",
        "number": number,
        "user": login,
        "user_type": user_type,
    }


@pytest.mark.parametrize(
    ("login", "person"),
    [
        ("clayphi", "Clay"),
        ("ironbelly", "Ryan"),
        ("IBC-ChrisG", "Chris"),
        ("IB-Lea", "Leandro"),
        ("swill-ib", "William"),
        ("IBC-CHRISG", "Chris"),
        ("CLAYPHI", "Clay"),
    ],
)
def test_human_opener_is_credited_through_the_table(login, person):
    fake = FakeGitHub({})
    assert mod.credit_for_pr(fake, "o", "r", opened_by(login)) == person
    assert fake.calls == []  # a person's PR needs no commit lookup


def test_human_pr_in_the_fixture_is_credited_to_its_opener():
    credited = collect(FakeGitHub(routes()))
    assert pr_by_number(credited, 102)[1] == "Leandro"
    assert pr_by_number(credited, 3, repo="gamma")[1] == "William"


def test_unmapped_human_login_is_shown_as_the_login():
    credited = collect(FakeGitHub(routes()))
    assert pr_by_number(credited, 7, repo="beta-private")[1] == "contractor-dev"


def test_bot_opened_pr_credits_the_author_of_the_branch_commits():
    fake = FakeGitHub(routes())
    credited = collect(fake)
    assert pr_by_number(credited, 103)[1] == "Leandro"
    assert "/repos/IronbellyOrg/alpha/pulls/103/commits" in fake.calls


def test_any_bot_account_credits_the_branch_author():
    commits = [{"author": {"login": "swill-ib", "type": "User"}}]
    routes_ = {"/repos/o/r/pulls/9/commits": commits}
    by_suffix = opened_by("some-app[bot]", user_type="User")
    by_type = opened_by("release-helper", user_type="Bot")
    assert mod.credit_for_pr(FakeGitHub(routes_), "o", "r", by_suffix) == "William"
    assert mod.credit_for_pr(FakeGitHub(routes_), "o", "r", by_type) == "William"


def test_pr_made_wholly_by_a_bot_is_credited_to_nobody():
    credited = collect(FakeGitHub(routes()))
    assert pr_by_number(credited, 104)[1] is None


@pytest.mark.parametrize(
    "commits",
    [
        [],
        [{"author": None}],
        [{"author": {"login": "dependabot[bot]", "type": "Bot"}}, {"author": None}],
    ],
)
def test_bot_pr_with_no_person_among_its_commits_is_credited_to_nobody(commits):
    fake = FakeGitHub({"/repos/o/r/pulls/9/commits": commits})
    assert mod.credit_for_pr(fake, "o", "r", opened_by("bot-x[bot]", "Bot")) is None


def test_deleted_opener_falls_back_to_the_branch_commits():
    commits = [{"author": {"login": "ironbelly", "type": "User"}}]
    fake = FakeGitHub({"/repos/o/r/pulls/9/commits": commits})
    assert mod.credit_for_pr(fake, "o", "r", opened_by(None, None)) == "Ryan"


def test_the_merger_never_decides_the_credit():
    credited = collect(FakeGitHub(routes()))
    raw = {p["number"]: p for p in load("pulls/IronbellyOrg-alpha.json")}
    # #101 was opened by clayphi and merged by ironbelly: Clay is credited.
    assert raw[101]["merged_by"]["login"] == "ironbelly"
    assert pr_by_number(credited, 101)[1] == "Clay"
    # #103 and #104 were merged by clayphi, but a bot-opened PR never credits a merger.
    assert raw[104]["merged_by"]["login"] == "clayphi"
    assert pr_by_number(credited, 104)[1] is None
    assert pr_by_number(credited, 103)[1] == "Leandro"


def test_bucket_all_groups_by_day_then_person_with_a_no_person_list():
    buckets = mod.bucket_all(collect(FakeGitHub(routes())), CHICAGO)
    assert list(buckets) == [  # newest day first, as returned
        date(2026, 11, 19),
        date(2026, 11, 18),
        date(2026, 11, 17),
        date(2026, 11, 16),
        date(2026, 11, 12),
    ]
    nov17 = buckets[date(2026, 11, 17)]
    # #103 merged 03:30 UTC on the 18th is 21:30 on the 17th in Chicago.
    assert list(nov17.by_person) == ["Leandro"]
    assert [p["number"] for p in nov17.by_person["Leandro"]] == [102, 103]
    assert nov17.no_person == []
    nov12 = buckets[date(2026, 11, 12)]
    assert nov12.by_person == {}
    assert [p["number"] for p in nov12.no_person] == [104]
    assert nov12.total() == 1
    assert nov12.counts_line() == "1 PR merged"
    assert buckets[date(2026, 11, 17)].counts_line() == "2 PRs merged"


def test_a_merge_near_midnight_utc_lands_on_a_different_day_in_another_zone():
    credited = collect(FakeGitHub(routes()))
    chicago = mod.bucket_all(credited, CHICAGO)
    tokyo = mod.bucket_all(credited, ZoneInfo("Asia/Tokyo"))

    def numbers(buckets, day):
        return [p["number"] for p in buckets[day].by_person.get("Leandro", [])]

    # #103 merged at 03:30 UTC on 11-18: 21:30 on 11-17 in Chicago, 12:30 on 11-18 in
    # Tokyo. #102 merged at 20:00 UTC on 11-17: 14:00 on 11-17 in Chicago, 05:00 on
    # 11-18 in Tokyo.
    assert numbers(chicago, date(2026, 11, 17)) == [102, 103]
    assert numbers(tokyo, date(2026, 11, 18)) == [102, 103]
    assert date(2026, 11, 17) not in tokyo
    assert numbers(chicago, date(2026, 11, 18)) == []


# --- rendering -------------------------------------------------------------------


def render(credited=None, repos_scanned=4):
    """Render the digest and the page from the fixture pipeline (or given PRs)."""
    credited = collect(FakeGitHub(routes())) if credited is None else credited
    days = list(mod.bucket_all(credited, CHICAGO).values())
    md = mod.build_markdown(days, NOW, CHICAGO, SINCE, repos_scanned)
    page = mod.build_html(days, NOW, CHICAGO, SINCE, repos_scanned)
    return md, page


def md_day(md, day):
    """The markdown text of one day section."""
    after = md.split(f"## {day}\n", 1)[1]
    return after.split("\n## ", 1)[0]


def page_day(page, day):
    """The HTML of one day section or details block."""
    after = page.split(f'id="{day}"', 1)[1]
    return after.split(' id="2026-', 1)[0]


def fake_pr(number, title, **extra):
    pr = {
        "org": "IronbellyOrg",
        "repo": "alpha",
        "number": number,
        "title": title,
        "url": f"https://github.com/IronbellyOrg/alpha/pull/{number}",
        "user": "clayphi",
        "user_type": "User",
        "when": datetime(2026, 11, 18, 15, 0, tzinfo=timezone.utc),
    }
    return {**pr, **extra}


def test_digest_and_page_link_every_pr_under_its_day_and_person():
    md, page = render()
    url = "https://github.com/IronbellyOrg/alpha/pull/101"
    section = md_day(md, "2026-11-18")
    assert section.index("### Clay (1)") < section.index(url)
    assert "[IronbellyOrg/alpha#101](" + url + "): Add login form" in section
    block = page_day(page, "2026-11-18")
    assert block.index("Clay (1)") < block.index(f'href="{url}"')
    assert ">IronbellyOrg/alpha#101</a>: Add login form" in block
    # every PR of the run is linked in both outputs
    for pr, _who in collect(FakeGitHub(routes())):
        assert pr["url"] in md
        assert f'href="{pr["url"]}"' in page


def test_a_day_with_a_bot_only_pr_shows_a_no_person_line():
    md, page = render()
    section = md_day(md, "2026-11-12")
    assert "### No person (1)" in section
    assert "[IronbellyOrg/alpha#104](" in section
    assert section.count("###") == 1  # no person heading besides No person
    block = page_day(page, "2026-11-12")
    assert "No person (1)" in block
    assert ">IronbellyOrg/alpha#104</a>" in block


def test_page_escapes_pr_text_and_names():
    credited = [
        (fake_pr(1, "<script>alert(1)</script> & more"), 'Tom "T" <b>'),
        (fake_pr(2, "plain", url='javascript:alert("x")'), "Clay"),
    ]
    _md, page = render(credited)
    assert "<script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt; &amp; more" in page
    assert "<b>" not in page
    assert "&lt;b&gt;" in page
    assert 'href="javascript:' not in page
    assert 'href="#"' in page


def test_digest_escapes_markdown_in_titles():
    credited = [(fake_pr(1, "[click](http://evil.example) <b>x</b> *y* `z`"), "Clay")]
    md, _page = render(credited)
    assert "\\[click\\]" in md
    assert "<b>" not in md
    assert "\\<b\\>x\\</b\\>" in md


def test_text_the_script_writes_names_no_agent():
    md, page = render()
    for out in (md, page):
        lowered = out.lower()
        assert "claude" not in lowered
        assert "agent" not in lowered


def test_no_issue_calendar_or_allowlist_content():
    md, page = render()
    for out in (md, page):
        lowered = out.lower()
        for word in ("issue", "calendar", ".ics", "allowlist", "legend"):
            assert word not in lowered


def test_headers_give_zone_window_and_repo_count():
    md, page = render(repos_scanned=62)
    assert "time zone America/Chicago" in md
    assert "lookback window from 2026-10-29" in md
    assert "62 repos scanned" in md
    assert "Generated 2026-11-19 12:00 CST" in md
    assert "Created: Nov 19, 2026 at 12:00pm" in page
    assert "62 repos scanned" in page


def test_an_empty_window_still_renders():
    md, page = render([])
    assert "_No merged pull requests in the window._" in md
    assert "No merged pull requests in the window." in page


# --- publishing and main ---------------------------------------------------------

FULL_ENV = {
    "GH_TOKEN": PLACEHOLDER,
    "CLICKUP_API_TOKEN": PLACEHOLDER,
    "CLICKUP_WORKSPACE_ID": "W1",
    "CLICKUP_DOC_ID": "D1",
    "CLICKUP_PAGE_ID": "P1",
}


class FakePut:
    def __init__(self, error=None):
        self.calls = []
        self.error = error

    def __call__(self, path, body):
        self.calls.append((path, body))
        if self.error:
            raise self.error


def run_main(out, *, env=None, fake=None, put=None, args=()):
    fake = FakeGitHub(routes()) if fake is None else fake
    put = FakePut() if put is None else put
    env = FULL_ENV if env is None else env
    argv = ["--out", str(out), *args]
    rc = mod.main(argv, env=env, get=fake, put=put, now=NOW)
    return rc, fake, put


def test_main_writes_both_files_and_publishes_the_digest_once(tmp_path, capsys):
    rc, _fake, put = run_main(tmp_path / "site")
    assert rc == 0
    digest = (tmp_path / "site" / "digest.md").read_text(encoding="utf-8")
    page = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert "### Clay (1)" in digest
    assert page.startswith("<!DOCTYPE html>")
    assert len(put.calls) == 1
    path, body = put.calls[0]
    assert path == "/v3/workspaces/W1/docs/D1/pages/P1"
    assert body == {
        "content": digest,
        "content_format": "text/md",
        "content_edit_mode": "replace",
    }
    assert PLACEHOLDER not in capsys.readouterr().out


def test_a_repo_added_after_the_first_run_shows_up_in_the_next_digest(tmp_path):
    run_main(tmp_path / "first")
    run_main(tmp_path / "second", fake=FakeGitHub(routes(run=2)))
    first = (tmp_path / "first" / "digest.md").read_text(encoding="utf-8")
    second = (tmp_path / "second" / "digest.md").read_text(encoding="utf-8")
    assert "delta-new" not in first
    assert "IronbellyGroup/delta-new#1" in second
    assert "### Ryan (1)" in second


@pytest.mark.parametrize("name", sorted(mod.CLICKUP_VARS))
def test_each_missing_clickup_variable_stops_before_any_call(tmp_path, name):
    env = {k: v for k, v in FULL_ENV.items() if k != name}
    fake, put = FakeGitHub(routes()), FakePut()
    with pytest.raises(SystemExit) as exc:
        mod.main(["--out", str(tmp_path)], env=env, get=fake, put=put, now=NOW)
    assert name in str(exc.value)
    assert fake.calls == []
    assert put.calls == []
    assert not (tmp_path / "digest.md").exists()


def test_every_missing_variable_is_named(tmp_path):
    with pytest.raises(SystemExit) as exc:
        mod.main(["--out", str(tmp_path)], env={}, get=FakeGitHub({}), now=NOW)
    for name in ("GH_TOKEN", *mod.CLICKUP_VARS):
        assert name in str(exc.value)


def test_gh_token_is_required_even_for_a_dry_run(tmp_path):
    env = {k: v for k, v in FULL_ENV.items() if k != "GH_TOKEN"}
    fake = FakeGitHub(routes())
    with pytest.raises(SystemExit, match="GH_TOKEN"):
        mod.main(["--out", str(tmp_path), "--dry-run"], env=env, get=fake, now=NOW)
    assert fake.calls == []


def test_dry_run_needs_only_gh_token_prints_the_rate_limit_twice_and_never_publishes(
    tmp_path, capsys
):
    rc, fake, put = run_main(
        tmp_path / "site", env={"GH_TOKEN": PLACEHOLDER}, args=["--dry-run"]
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert put.calls == []
    assert out.count("rate limit before: core=4990/5000") == 1
    assert out.count("rate limit after: core=4990/5000") == 1
    assert "graphql=5000/5000 search=30/30" in out
    assert fake.calls[0] == "/rate_limit" and fake.calls[-1] == "/rate_limit"
    assert (tmp_path / "site" / "digest.md").exists()
    assert (tmp_path / "site" / "index.html").exists()
    assert PLACEHOLDER not in out


def test_a_github_error_for_one_repo_ends_the_run_and_publishes_nothing(
    tmp_path, capsys
):
    served = routes()
    del served["/repos/IronbellyOrg/beta-private/pulls"]
    rc, _fake, put = run_main(tmp_path / "site", fake=FakeGitHub(served))
    captured = capsys.readouterr()
    assert rc == 1
    assert put.calls == []
    assert "beta-private" in captured.err
    assert not (tmp_path / "site" / "digest.md").exists()
    assert PLACEHOLDER not in captured.err


def test_a_clickup_error_ends_the_run_non_zero(tmp_path, capsys):
    put = FakePut(error=mod.ClickUpError("ClickUp returned HTTP 500 for /v3/x"))
    rc, _fake, _put = run_main(tmp_path / "site", put=put)
    assert rc == 1
    assert "HTTP 500" in capsys.readouterr().err


def test_a_missing_out_folder_argument_is_an_error():
    with pytest.raises(SystemExit) as exc:
        mod.main([], env=FULL_ENV, get=FakeGitHub({}), now=NOW)
    assert exc.value.code == 2


def test_publish_clickup_quotes_the_ids_it_puts_in_the_path():
    put = FakePut()
    env = {**FULL_ENV, "CLICKUP_PAGE_ID": "a/b c"}
    mod.publish_clickup(put, env, "# digest")
    assert put.calls[0][0] == "/v3/workspaces/W1/docs/D1/pages/a%2Fb%20c"


def test_make_clickup_put_sends_the_token_as_is_and_a_replace_body(monkeypatch):
    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def fake_urlopen(req, timeout):
        captured["req"] = req
        return Response()

    monkeypatch.setattr(mod.urllib.request, "urlopen", fake_urlopen)
    put = mod.make_clickup_put(PLACEHOLDER)
    mod.publish_clickup(put, FULL_ENV, "# digest")
    req = captured["req"]
    assert req.get_method() == "PUT"
    assert req.full_url == (
        "https://api.clickup.com/api/v3/workspaces/W1/docs/D1/pages/P1"
    )
    assert req.get_header("Authorization") == PLACEHOLDER  # no Bearer prefix
    assert json.loads(req.data) == {
        "content": "# digest",
        "content_format": "text/md",
        "content_edit_mode": "replace",
    }


def test_make_clickup_put_hides_the_token_when_a_request_fails(monkeypatch):
    def fake_urlopen(req, timeout):
        raise urllib.error.HTTPError(req.full_url, 401, "unauthorized", {}, None)

    monkeypatch.setattr(mod.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(mod.ClickUpError) as exc:
        mod.make_clickup_put(PLACEHOLDER)("/v3/x", {})
    assert "401" in str(exc.value)
    assert PLACEHOLDER not in str(exc.value)


# --- the Orca automation definition ----------------------------------------------

ORCA_DOC = ROOT / "scripts" / "merged_pr_log_orca_automation.md"


def orca_field(label):
    match = re.search(rf"^{re.escape(label)}: (.+)$", orca_text(), re.MULTILINE)
    assert match, f"{label} line missing"
    return match.group(1).strip()


def orca_text():
    return ORCA_DOC.read_text(encoding="utf-8")


def test_orca_definition_has_the_name_trigger_and_status_lines():
    name = orca_field("Name")
    assert name == "merged-pr-log-refresh"
    assert not name.startswith("coordinator-")
    assert orca_field("Trigger (UTC)") == "5 0,6,12,18 * * *"
    assert orca_field("Status") == "written, not switched on"


def test_orca_definition_names_the_variables_and_holds_no_secret_value():
    text = orca_text()
    for name in ("GH_TOKEN", *mod.CLICKUP_VARS):
        assert name in text
    for shape in (r"ghp_\w", r"github_pat_", r"\bpk_\d", r"Bearer \S", r"gho_\w"):
        assert not re.search(shape, text), shape


def test_orca_definition_lists_the_human_steps_and_says_nothing_was_created():
    text = orca_text()
    assert "Create the ClickUp Doc" in text
    assert "Clay switches the automation on." in text
    assert "has been created in Orca, switched on or triggered" in text
    assert "--dry-run" in text


def test_orca_definition_depends_on_neither_the_work_report_nor_the_orchestrator():
    text = orca_text()
    for needle in ("agent-work-report", "config.json", "orchestrator"):
        assert needle not in text


# --- opt-in, independence and secrets (guards for the hard rules) ----------------

SRC = ROOT / "src" / "superclaude"
DELIVERED = [
    SCRIPT,
    ORCA_DOC,
    Path(__file__).resolve(),
    *sorted(FIXTURES.rglob("*.json")),
]
SECRET_SHAPES = [
    r"ghp_[A-Za-z0-9]{20,}",
    r"gh[osu]_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"\bpk_\d{5,}",
    r"xox[abp]-[A-Za-z0-9-]{10,}",
    r"AKIA[0-9A-Z]{16}",
    r"Bearer [A-Za-z0-9._-]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
]


def test_script_names_neither_the_work_report_the_orchestrator_nor_ironflow():
    lowered = SCRIPT.read_text(encoding="utf-8").lower()
    for needle in (
        "superclaude",
        "work report",
        "work-report",
        "orchestrator",
        "ironflow",
        "claude",
    ):
        assert needle not in lowered


def test_nothing_under_src_superclaude_mentions_or_ships_the_log():
    """No skill, command, agent, hook or template exists for it, so an install of
    this repo copies nothing new."""
    named = [p for p in SRC.rglob("*") if "merged_pr_log" in p.name]
    assert named == []
    text_suffixes = {".py", ".md", ".json", ".toml", ".sh", ".yaml", ".yml", ".txt"}
    mentions = [
        p
        for p in SRC.rglob("*")
        if p.is_file()
        and p.suffix in text_suffixes
        and "merged_pr_log" in p.read_text(encoding="utf-8", errors="ignore")
    ]
    assert mentions == []


def test_no_delivered_file_holds_a_token_shaped_string():
    for path in DELIVERED:
        text = path.read_text(encoding="utf-8")
        for shape in SECRET_SHAPES:
            assert not re.search(shape, text), f"{path.name} matches {shape}"


def test_credentials_come_only_from_the_environment_mapping():
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    os_attributes = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "os"
    }
    assert os_attributes == {"environ"}  # no getenv, no os.path or file access
    read_calls = {
        node.func.id if isinstance(node.func, ast.Name) else node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and (
            (isinstance(node.func, ast.Name) and node.func.id == "open")
            or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr in {"open", "read_text", "read_bytes"}
            )
        )
    }
    assert read_calls == set()  # the script writes its two files and reads none


def test_no_agent_name_is_ever_a_credit():
    agent_words = ("claude", "codex", "copilot", "gemini", "grok", "cursor", "devin")
    credits = {who for _pr, who in collect(FakeGitHub(routes())) if who}
    credits |= set(mod.LOGIN_TO_PERSON.values())
    for credit in credits:
        assert not any(word in credit.lower() for word in agent_words)
    assert set(mod.LOGIN_TO_PERSON.values()) == {
        "Clay",
        "Ryan",
        "Chris",
        "Leandro",
        "William",
    }
