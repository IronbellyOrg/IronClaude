"""Behavior tests for the /sc:issue ClickUp claim script (design section 12).

Enforcement type: EXECUTABLE (script behavior). ``urllib.request.urlopen`` is
patched with a fake ClickUp server that serves recorded response shapes. Every
fixture value is made up; no live value is ever copied here.

Every test starts with all four ``CLICKUP_*`` variables cleared, so an
exported real token, workspace, list filter or page cap never reaches a test.
"""

import ast
import copy
import email.message
import importlib.util
import io
import json
import sys
import urllib.error
import urllib.parse
from pathlib import Path

import pytest

_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py"
)
_spec = importlib.util.spec_from_file_location("clickup_claim", _SCRIPT)
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)

TOKEN = "pk_000000_FAKETOKENFORTESTSONLY"
WORKSPACE = "9000000001"
REPO = "IronbellyOrg/IronClaude"
NUMBER = 302
ISSUE_URL = f"https://github.com/{REPO}/issues/{NUMBER}"
ARGS = ["--issue-url", ISSUE_URL, "--issue-number", str(NUMBER), "--repo", REPO]
CLICKUP_VARS = ("CLICKUP_API_TOKEN", "CLICKUP_WORKSPACE_ID", "CLICKUP_LIST_IDS", "CLICKUP_MAX_PAGES")

# --- recorded response shapes (made-up values) --------------------------------

# GET /api/v2/user (getauthorizeduser)
USER_RESPONSE = {
    "user": {
        "id": 4242,
        "username": "Test User",
        "email": "test.user@example.com",
        "color": "#000000",
        "profilePicture": None,
        "initials": "TU",
        "week_start_day": 0,
        "global_font_support": False,
        "timezone": "UTC",
    }
}

# one task of GET /api/v2/team/{team_Id}/task (getfilteredteamtasks)
TASK_TEMPLATE = {
    "id": "86abc0001",
    "custom_id": None,
    "name": "Example task",
    "text_content": "",
    "description": "",
    "markdown_description": "",
    "status": {"status": "to do", "type": "open"},
    "assignees": [],
    "watchers": [],
    "tags": [],
    "custom_fields": [],
    "team_id": WORKSPACE,
    "url": "https://app.clickup.com/t/86abc0001",
    "list": {"id": "900100000001"},
}

# PUT /api/v2/task/{task_id} (updatetask)
UPDATE_RESPONSE = {"id": "86abc0001", "name": "Example task", "status": {"status": "to do"}}


def task(task_id, name="Example task", markdown="", custom=None, assignees=None):
    t = copy.deepcopy(TASK_TEMPLATE)
    t.update(
        id=task_id,
        name=name,
        markdown_description=markdown,
        url=f"https://app.clickup.com/t/{task_id}",
        custom_fields=custom or [],
        assignees=[{"id": a, "username": f"user{a}"} for a in (assignees or [])],
    )
    return t


class FakeClickUp:
    """Serves the recorded shapes and records every request."""

    def __init__(self, pages=None, user_status=200, statuses=None):
        self.pages = pages if pages is not None else [[]]
        self.user_status = user_status
        self.statuses = list(statuses or [])  # forced statuses, consumed in order
        self.calls = []

    def _error(self, url, code, retry_after=None):
        headers = email.message.Message()
        if retry_after is not None:
            headers["Retry-After"] = str(retry_after)
        return urllib.error.HTTPError(url, code, "error", headers, io.BytesIO(b"{}"))

    def __call__(self, req, timeout=None):
        url = req.full_url
        body = json.loads(req.data.decode("utf-8")) if req.data else None
        self.calls.append(
            {
                "method": req.get_method(),
                "url": url,
                "body": body,
                "auth": req.get_header("Authorization"),
            }
        )
        if self.statuses:
            code, retry_after = self.statuses.pop(0)
            if code != 200:
                raise self._error(url, code, retry_after)
        parsed = urllib.parse.urlparse(url)
        if req.get_method() == "GET" and parsed.path == "/api/v2/user":
            if self.user_status != 200:
                raise self._error(url, self.user_status)
            payload = USER_RESPONSE
        elif req.get_method() == "GET" and parsed.path == f"/api/v2/team/{WORKSPACE}/task":
            page = int(urllib.parse.parse_qs(parsed.query)["page"][0])
            tasks = self.pages[page] if page < len(self.pages) else []
            payload = {"tasks": tasks}
        elif req.get_method() == "PUT" and parsed.path.startswith("/api/v2/task/"):
            payload = UPDATE_RESPONSE
        else:  # pragma: no cover - a request the script must never make
            raise AssertionError(f"unexpected request {req.get_method()} {url}")
        return io.BytesIO(json.dumps(payload).encode("utf-8"))

    def puts(self):
        return [c for c in self.calls if c["method"] == "PUT"]

    def pages_requested(self):
        return [
            int(urllib.parse.parse_qs(urllib.parse.urlparse(c["url"]).query)["page"][0])
            for c in self.calls
            if "/task?" in c["url"]
        ]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch, capsys):
    for name in CLICKUP_VARS:
        monkeypatch.delenv(name, raising=False)
    sleeps = []
    monkeypatch.setattr(cc.time, "sleep", sleeps.append)
    yield sleeps
    out, err = capsys.readouterr()
    assert TOKEN not in out and TOKEN not in err


def configure(monkeypatch, fake, **extra):
    monkeypatch.setenv("CLICKUP_API_TOKEN", TOKEN)
    monkeypatch.setenv("CLICKUP_WORKSPACE_ID", WORKSPACE)
    for name, value in extra.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(cc.urllib.request, "urlopen", fake)


def run(capsys, args=ARGS):
    code = cc.main(list(args))
    out, err = capsys.readouterr()
    assert TOKEN not in out and TOKEN not in err
    return code, json.loads(out)


# --- skipped -----------------------------------------------------------------


def test_skipped_without_token(monkeypatch, capsys):
    fake = FakeClickUp()
    monkeypatch.setenv("CLICKUP_WORKSPACE_ID", WORKSPACE)
    monkeypatch.setattr(cc.urllib.request, "urlopen", fake)
    assert run(capsys) == (0, {"status": "skipped", "reason": "no_token"})
    assert fake.calls == []


def test_skipped_without_workspace(monkeypatch, capsys):
    fake = FakeClickUp()
    monkeypatch.setenv("CLICKUP_API_TOKEN", TOKEN)
    monkeypatch.setattr(cc.urllib.request, "urlopen", fake)
    assert run(capsys) == (0, {"status": "skipped", "reason": "no_workspace"})
    assert fake.calls == []


# --- matching ------------------------------------------------------------------


def test_github_link_match_beats_title_match(monkeypatch, capsys):
    fake = FakeClickUp(
        pages=[
            [
                task("86title", name=f"Fix #{NUMBER} quickly"),
                task("86link", markdown=f"Tracks {ISSUE_URL}/ in GitHub"),
            ]
        ]
    )
    configure(monkeypatch, fake)
    code, out = run(capsys)
    assert code == 0
    assert out == {
        "status": "assigned",
        "task_id": "86link",
        "task_url": "https://app.clickup.com/t/86link",
        "rule": "github_link",
    }


def test_github_link_in_custom_field_value_matches(monkeypatch, capsys):
    custom = [{"id": "cf1", "name": "GitHub", "type": "url", "value": ISSUE_URL.upper() + "#top"}]
    fake = FakeClickUp(pages=[[task("86cf", custom=custom)]])
    configure(monkeypatch, fake)
    assert run(capsys)[1]["rule"] == "github_link"


def test_github_link_with_longer_number_does_not_match(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86other", markdown=f"{ISSUE_URL}0")]])
    configure(monkeypatch, fake)
    assert run(capsys)[1] == {"status": "not_found"}


def test_title_match_only_as_whole_token(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86a", name=f"Refactor #{NUMBER}0"), task("86b", name=f"x#{NUMBER}")]])
    configure(monkeypatch, fake)
    assert run(capsys)[1] == {"status": "not_found"}
    assert fake.puts() == []


def test_title_match_assigns_with_title_rule(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86a", name=f"Refactor #{NUMBER}0"), task("86b", name=f"[#{NUMBER}] claim it")]])
    configure(monkeypatch, fake)
    out = run(capsys)[1]
    assert out["status"] == "assigned" and out["task_id"] == "86b" and out["rule"] == "title_number"


def test_ambiguous_returns_candidates_and_makes_no_put(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86one", markdown=ISSUE_URL), task("86two", markdown=ISSUE_URL)]])
    configure(monkeypatch, fake)
    code, out = run(capsys)
    assert code == 0
    assert out["status"] == "ambiguous"
    assert [c["task_id"] for c in out["candidates"]] == ["86one", "86two"]
    assert fake.puts() == []


def test_not_found(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86none", name="Unrelated")]])
    configure(monkeypatch, fake)
    assert run(capsys) == (0, {"status": "not_found"})


# --- assignment ---------------------------------------------------------------


def test_already_assigned_makes_no_put(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86mine", markdown=ISSUE_URL, assignees=[4242])]])
    configure(monkeypatch, fake)
    out = run(capsys)[1]
    assert out == {
        "status": "already_assigned",
        "task_id": "86mine",
        "task_url": "https://app.clickup.com/t/86mine",
        "rule": "github_link",
    }
    assert fake.puts() == []


def test_assign_sends_assignees_add_body(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86todo", markdown=ISSUE_URL, assignees=[7])]])
    configure(monkeypatch, fake)
    assert run(capsys)[1]["status"] == "assigned"
    [put] = fake.puts()
    assert put["url"] == "https://api.clickup.com/api/v2/task/86todo"
    assert put["body"] == {"assignees": {"add": [4242]}}
    assert all(c["auth"] == TOKEN for c in fake.calls)


def test_list_ids_narrow_the_search(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[]])
    configure(monkeypatch, fake, CLICKUP_LIST_IDS="111, 222")
    run(capsys)
    [search] = [c for c in fake.calls if "/task?" in c["url"]]
    query = urllib.parse.parse_qs(urllib.parse.urlparse(search["url"]).query)
    assert query["list_ids[]"] == ["111", "222"]
    assert query["subtasks"] == ["true"] and query["include_markdown_description"] == ["true"]


# --- errors -------------------------------------------------------------------


@pytest.mark.parametrize("status", [401, 403])
def test_auth_failure_gives_auth(monkeypatch, capsys, status):
    fake = FakeClickUp(user_status=status)
    configure(monkeypatch, fake)
    assert run(capsys) == (0, {"status": "error", "reason": "auth"})


def test_429_is_retried_exactly_once_then_continues(monkeypatch, capsys, clean_env):
    fake = FakeClickUp(pages=[[task("86t", markdown=ISSUE_URL)]], statuses=[(429, 7)])
    configure(monkeypatch, fake)
    assert run(capsys)[1]["status"] == "assigned"
    assert clean_env == [7.0]
    assert [c["method"] for c in fake.calls[:2]] == ["GET", "GET"]
    assert fake.calls[0]["url"] == fake.calls[1]["url"]


def test_429_twice_gives_rate_limited(monkeypatch, capsys, clean_env):
    fake = FakeClickUp(statuses=[(429, 3), (429, 3)])
    configure(monkeypatch, fake)
    assert run(capsys) == (0, {"status": "error", "reason": "rate_limited"})
    assert clean_env == [3.0]
    assert len(fake.calls) == 2


def test_other_http_error_gives_short_reason(monkeypatch, capsys):
    fake = FakeClickUp(statuses=[(500, None)])
    configure(monkeypatch, fake)
    assert run(capsys) == (0, {"status": "error", "reason": "http_500"})


# --- paging ---------------------------------------------------------------------


def test_page_cap_is_honoured_and_first_page_is_zero(monkeypatch, capsys):
    pages = [[task(f"86p{i}", name="Unrelated")] for i in range(10)]
    fake = FakeClickUp(pages=pages)
    configure(monkeypatch, fake, CLICKUP_MAX_PAGES="3")
    assert run(capsys)[1] == {"status": "not_found"}
    assert fake.pages_requested() == [0, 1, 2]
    assert cc.FIRST_PAGE == 0


def test_empty_page_ends_the_search(monkeypatch, capsys):
    fake = FakeClickUp(pages=[[task("86p0", name="Unrelated")], []])
    configure(monkeypatch, fake)
    run(capsys)
    assert fake.pages_requested() == [0, 1]


@pytest.mark.parametrize("value", ["0", "-1", "abc", "", "2.5"])
def test_invalid_max_pages_falls_back_to_default(monkeypatch, capsys, value):
    pages = [[task(f"86p{i}", name="Unrelated")] for i in range(30)]
    fake = FakeClickUp(pages=pages)
    configure(monkeypatch, fake, CLICKUP_MAX_PAGES=value)
    code, out = run(capsys)
    assert code == 0 and out == {"status": "not_found"}
    assert fake.pages_requested() == list(range(cc.DEFAULT_MAX_PAGES))
    assert cc.DEFAULT_MAX_PAGES == 20


# --- arguments ------------------------------------------------------------------


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["--issue-url", ISSUE_URL, "--issue-number", str(NUMBER)],
        ["--issue-url", ISSUE_URL, "--issue-number", "abc", "--repo", REPO],
        ["--issue-url", ISSUE_URL, "--issue-number", "0", "--repo", REPO],
        ["--issue-url", ISSUE_URL, "--issue-number", str(NUMBER), "--repo", "not-a-repo"],
        ["--issue-url", f"https://github.com/{REPO}/issues/1", "--issue-number", str(NUMBER), "--repo", REPO],
    ],
)
def test_bad_arguments_exit_2(monkeypatch, args):
    fake = FakeClickUp()
    configure(monkeypatch, fake)
    with pytest.raises(SystemExit) as exc:
        cc.main(args)
    assert exc.value.code == 2
    assert fake.calls == []


def test_token_never_printed_on_any_outcome(monkeypatch, capsys):
    for fake in (
        FakeClickUp(pages=[[task("86t", markdown=ISSUE_URL)]]),
        FakeClickUp(user_status=401),
        FakeClickUp(statuses=[(429, 1), (429, 1)]),
        FakeClickUp(statuses=[(500, None)]),
    ):
        configure(monkeypatch, fake)
        cc.main(list(ARGS))
        out, err = capsys.readouterr()
        assert TOKEN not in out and TOKEN not in err


def test_script_imports_only_standard_library():
    tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    assert names <= set(sys.stdlib_module_names)
