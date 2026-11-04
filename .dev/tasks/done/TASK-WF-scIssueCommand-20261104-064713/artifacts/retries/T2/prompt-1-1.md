7ff9aca8e07b5f0a0ed293c9ac3b2e7336868081
Review one task for spec compliance.

Task brief: ## Task 2: Create the ClickUp claim script and its tests

Create `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` exactly as source section 12 specifies: standard library only (`urllib`); arguments `--issue-url <url> --issue-number <N> --repo <owner/repo>`; configuration only from the environment variables `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID`, `CLICKUP_LIST_IDS` (optional, comma-separated, sent as `list_ids[]=`) and `CLICKUP_MAX_PAGES` (optional, default `20`). Steps, in order: token or workspace missing prints `{"status": "skipped", "reason": "no_token"|"no_workspace"}` and exits 0; `GET https://api.clickup.com/api/v2/user` for the token owner's user ID; page through `GET https://api.clickup.com/api/v2/team/{CLICKUP_WORKSPACE_ID}/task?page=<p>&subtasks=true&include_markdown_description=true` until an empty page or the page cap; match by rule 1 (the issue URL `https://github.com/<owner>/<repo>/issues/<N>` in the markdown description or any custom field value, case-insensitive, trailing `/` or `#...` ignored), and only if rule 1 found nothing, rule 2 (`#<N>` as a whole token in the task name, not followed by a digit) (source default D2); more than one match prints `{"status": "ambiguous", "candidates": [...]}` with no PUT; none prints `{"status": "not_found"}`; already an assignee prints `{"status": "already_assigned", ...}` with no PUT; otherwise `PUT https://api.clickup.com/api/v2/task/{task_id}` with body `{"assignees": {"add": [<user id>]}}` and print `{"status": "assigned", "task_id": ..., "task_url": ..., "rule": "github_link"|"title_number"}`. HTTP 401/403 prints `{"status": "error", "reason": "auth"}`; HTTP 429 waits the `Retry-After` seconds once, retries once, then prints `{"status": "error", "reason": "rate_limited"}`; any other failure prints `{"status": "error", "reason": "<short>"}`. Exit 0 for every outcome above; exit 2 only for bad arguments. The token is never printed, logged or written to disk. Take the `GET /user`, task-list and update-task response shapes and the first page number of the task list from the ClickUp v2 reference (`developer.clickup.com/reference/getfilteredteamtasks`, `.../updatetask`, read through Context7 or the web) and record them in the script's module docstring. Define and document in the docstring what the script does when `CLICKUP_MAX_PAGES` is not a positive integer.

Create `tests/skills/test_clickup_claim.py` (source section 16 row) with `urllib` patched and recorded JSON fixtures for the three response shapes. Every test clears `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` with `monkeypatch.delenv(..., raising=False)` before setting the values it needs, so an exported real token never reaches a test. Fixtures hold made-up values only. The tests pin: skipped without token; skipped without workspace; GitHub-link match beats title match; title match only as a whole `#N` token (`#3020` does not match `#302`); ambiguous returns candidates and makes no PUT; already-assigned makes no PUT; assign sends `{"assignees": {"add": [id]}}`; 401 gives `auth`; 429 is retried exactly once (with the sleep patched); the page cap from `CLICKUP_MAX_PAGES` is honoured and the first requested page is the documented first page; the documented behaviour for a non-positive or non-integer `CLICKUP_MAX_PAGES`; the token value never appears in stdout or stderr in any test; bad arguments exit 2.

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` exists, imports only standard-library modules, and its docstring names the ClickUp v2 endpoints, the response fields and the first page number it relies on.
- `uv run pytest tests/skills/test_clickup_claim.py -v` passes, with one test per behaviour listed above.
- `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --issue-url https://github.com/IronbellyOrg/IronClaude/issues/302 --issue-number 302 --repo IronbellyOrg/IronClaude` prints `{"status": "skipped", "reason": "no_token"}` and exits 0; output saved to `./artifacts/t2-clickup-skipped.txt`.

AC ids: T2.AC1 = first acceptance bullet (script exists, standard library only, docstring names the endpoints, response fields and first page number); T2.AC2 = second bullet (pytest passes, one test per listed behaviour); T2.AC3 = third bullet (skipped output saved to .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t2-clickup-skipped.txt).

Coordinator constraint C4 (binding; recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md and round2-minor-findings.md): two round-2 minor findings are applied inside this task as correctness fixes: F-05 (every test clears all four CLICKUP_* variables, not only the token and workspace) and F-13 (a non-positive or non-integer CLICKUP_MAX_PAGES falls back to the default 20 and the run continues with exit 0, because exit 2 is reserved for bad arguments). No live ClickUp call is made in this task.
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md section 12 (lines 284-314) and section 16.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 7ff9aca8e07b5f0a0ed293c9ac3b2e7336868081
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py b/src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py
new file mode 100644
index 00000000..343ae55c
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py
@@ -0,0 +1,252 @@
+#!/usr/bin/env python3
+"""Assign the ClickUp task that tracks a GitHub issue to the token owner.
+
+Standard library only (``urllib``). Called by /sc:issue --claim in Wave 3 as
+``clickup_claim.py --issue-url <url> --issue-number <N> --repo <owner/repo>``;
+the skill writes stdout to ``.dev/issues/<N>/clickup.json``.
+
+Configuration (environment only):
+    CLICKUP_API_TOKEN     required; the person's own personal token (pk_...).
+                          Sent only in the Authorization header. Never printed,
+                          logged or written to disk.
+    CLICKUP_WORKSPACE_ID  required; the workspace (team) ID.
+    CLICKUP_LIST_IDS      optional; comma-separated list IDs, sent as
+                          ``list_ids[]=<id>`` to narrow the search.
+    CLICKUP_MAX_PAGES     optional; page cap for the search, default 20.
+                          A value that is not a positive integer (for example
+                          ``0``, ``-1``, ``abc`` or empty) is ignored: the
+                          default 20 is used and the run continues. Exit code
+                          2 stays reserved for bad command-line arguments.
+
+ClickUp API v2 endpoints and the response fields this script relies on
+(developer.clickup.com/reference, read 2026-11-04 through Context7 and the web):
+    GET https://api.clickup.com/api/v2/user                (getauthorizeduser)
+        200 body ``{"user": {"id": <int>, "username": ..., ...}}``; the
+        script reads ``user.id``.
+    GET https://api.clickup.com/api/v2/team/{team_Id}/task (getfilteredteamtasks)
+        query ``page`` ("Page to fetch (starts at 0)", so the first page is
+        0), ``subtasks=true``, ``include_markdown_description=true`` and
+        optional ``list_ids[]``. At most 100 tasks per page; closed tasks are
+        excluded by default. 200 body ``{"tasks": [<task>, ...]}``; per task
+        the script reads ``id``, ``name``, ``url``, ``markdown_description``
+        (``description`` when it is absent), ``assignees[].id`` and
+        ``custom_fields[].value``. An empty ``tasks`` list ends the search.
+    PUT https://api.clickup.com/api/v2/task/{task_id}       (updatetask)
+        body ``{"assignees": {"add": [<user id>]}}``; a 2xx status means the
+        assignment was made (the 200 body carries the task ``id``).
+    Authentication: header ``Authorization: <personal token>``.
+
+Matching (design default D2):
+    Rule 1, GitHub link: the markdown description or any custom field value
+    contains ``https://github.com/<owner>/<repo>/issues/<N>``, compared
+    case-insensitively, not followed by another digit (so a trailing ``/`` or
+    ``#...`` is ignored and ``/issues/3020`` does not match ``/issues/302``).
+    Rule 2, only when rule 1 found nothing: the task name contains ``#<N>`` as
+    a whole token, not followed by a digit.
+
+Output: one JSON object on stdout, always exit 0 except for bad arguments:
+    {"status": "skipped", "reason": "no_token"|"no_workspace"}
+    {"status": "not_found"}
+    {"status": "ambiguous", "rule": ..., "candidates": [{"task_id", "task_url"}, ...]}
+    {"status": "already_assigned", "task_id", "task_url", "rule"}
+    {"status": "assigned", "task_id", "task_url", "rule": "github_link"|"title_number"}
+    {"status": "error", "reason": "auth"|"rate_limited"|"<short>"}
+HTTP 401/403 gives ``auth``. HTTP 429 waits the ``Retry-After`` seconds once,
+retries once, then gives ``rate_limited``. Bad arguments exit 2 (argparse).
+"""
+
+from __future__ import annotations
+
+import argparse
+import json
+import os
+import re
+import sys
+import time
+import urllib.error
+import urllib.parse
+import urllib.request
+
+API = "https://api.clickup.com/api/v2"
+DEFAULT_MAX_PAGES = 20
+FIRST_PAGE = 0
+TIMEOUT_SECONDS = 30
+_REPO = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
+
+
+class ClickUpError(Exception):
+    """A failure reported as ``{"status": "error", "reason": <reason>}``."""
+
+    def __init__(self, reason: str) -> None:
+        super().__init__(reason)
+        self.reason = reason
+
+
+def max_pages_from_env(value: str | None) -> int:
+    """Return the page cap; anything but a positive integer gives the default."""
+    try:
+        pages = int((value or "").strip())
+    except ValueError:
+        return DEFAULT_MAX_PAGES
+    return pages if pages > 0 else DEFAULT_MAX_PAGES
+
+
+def _retry_after(headers) -> float:
+    try:
+        return max(0.0, float(headers.get("Retry-After", "1")))
+    except (TypeError, ValueError):
+        return 1.0
+
+
+def request(method: str, url: str, token: str, body: dict | None = None):
+    """Send one request and return the decoded JSON body (or ``{}``)."""
+    data = None if body is None else json.dumps(body).encode("utf-8")
+    for attempt in (1, 2):
+        req = urllib.request.Request(url, data=data, method=method)
+        req.add_header("Authorization", token)
+        req.add_header("Accept", "application/json")
+        if data is not None:
+            req.add_header("Content-Type", "application/json")
+        try:
+            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
+                raw = resp.read()
+        except urllib.error.HTTPError as exc:
+            if exc.code in (401, 403):
+                raise ClickUpError("auth") from None
+            if exc.code == 429:
+                if attempt == 1:
+                    time.sleep(_retry_after(exc.headers or {}))
+                    continue
+                raise ClickUpError("rate_limited") from None
+            raise ClickUpError(f"http_{exc.code}") from None
+        except (urllib.error.URLError, TimeoutError, OSError):
+            raise ClickUpError("network") from None
+        if not raw:
+            return {}
+        try:
+            return json.loads(raw.decode("utf-8"))
+        except (UnicodeDecodeError, json.JSONDecodeError):
+            raise ClickUpError("bad_response") from None
+    raise ClickUpError("rate_limited")  # pragma: no cover
+
+
+def _strings(value) -> list[str]:
+    if isinstance(value, str):
+        return [value]
+    if isinstance(value, dict):
+        return [s for v in value.values() for s in _strings(v)]
+    if isinstance(value, list):
+        return [s for v in value for s in _strings(v)]
+    if value is None or isinstance(value, bool):
+        return []
+    return [str(value)]
+
+
+def match_rule(task: dict, issue_url: str, number: int) -> str | None:
+    """Return ``github_link``, ``title_number`` or ``None`` for one task."""
+    link = re.compile(re.escape(issue_url.rstrip("/")) + r"(?![0-9])", re.IGNORECASE)
+    texts = _strings(task.get("markdown_description") or task.get("description") or "")
+    for field in task.get("custom_fields") or []:
+        if isinstance(field, dict):
+            texts.extend(_strings(field.get("value")))
+    if any(link.search(text) for text in texts):
+        return "github_link"
+    title = re.compile(rf"(?<![\w#])#{number}(?![0-9])")
+    if title.search(str(task.get("name") or "")):
+        return "title_number"
+    return None
+
+
+def claim(issue_url: str, number: int, env: dict) -> dict:
+    token = (env.get("CLICKUP_API_TOKEN") or "").strip()
+    if not token:
+        return {"status": "skipped", "reason": "no_token"}
+    workspace = (env.get("CLICKUP_WORKSPACE_ID") or "").strip()
+    if not workspace:
+        return {"status": "skipped", "reason": "no_workspace"}
+    max_pages = max_pages_from_env(env.get("CLICKUP_MAX_PAGES"))
+    list_ids = [s.strip() for s in (env.get("CLICKUP_LIST_IDS") or "").split(",") if s.strip()]
+
+    try:
+        user = request("GET", f"{API}/user", token)
+        user_id = (user.get("user") or {}).get("id")
+        if user_id is None:
+            raise ClickUpError("bad_response")
+
+        found: dict[str, list[dict]] = {"github_link": [], "title_number": []}
+        seen: set[str] = set()
+        for page in range(FIRST_PAGE, FIRST_PAGE + max_pages):
+            query = [
+                ("page", str(page)),
+                ("subtasks", "true"),
+                ("include_markdown_description", "true"),
+            ] + [("list_ids[]", list_id) for list_id in list_ids]
+            url = f"{API}/team/{urllib.parse.quote(workspace, safe='')}/task?{urllib.parse.urlencode(query)}"
+            tasks = request("GET", url, token).get("tasks") or []
+            if not tasks:
+                break
+            for task in tasks:
+                task_id = str(task.get("id") or "")
+                if not task_id or task_id in seen:
+                    continue
+                seen.add(task_id)
+                rule = match_rule(task, issue_url, number)
+                if rule:
+                    found[rule].append(task)
+
+        rule = "github_link" if found["github_link"] else "title_number"
+        matches = found[rule]
+        if not matches:
+            return {"status": "not_found"}
+        if len(matches) > 1:
+            return {
+                "status": "ambiguous",
+                "rule": rule,
+                "candidates": [
+                    {"task_id": str(t.get("id")), "task_url": t.get("url")} for t in matches
+                ],
+            }
+        task = matches[0]
+        result = {"task_id": str(task.get("id")), "task_url": task.get("url"), "rule": rule}
+        assignees = {str(a.get("id")) for a in task.get("assignees") or [] if isinstance(a, dict)}
+        if str(user_id) in assignees:
+            return {"status": "already_assigned", **result}
+        request(
+            "PUT",
+            f"{API}/task/{urllib.parse.quote(result['task_id'], safe='')}",
+            token,
+            {"assignees": {"add": [user_id]}},
+        )
+        return {"status": "assigned", **result}
+    except ClickUpError as exc:
+        return {"status": "error", "reason": exc.reason}
+    except Exception:  # never let a traceback (and anything in it) reach output
+        return {"status": "error", "reason": "unexpected"}
+
+
+def parse_args(argv: list[str] | None) -> argparse.Namespace:
+    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
+    parser.add_argument("--issue-url", required=True)
+    parser.add_argument("--issue-number", required=True, type=int)
+    parser.add_argument("--repo", required=True)
+    args = parser.parse_args(argv)
+    if args.issue_number <= 0:
+        parser.error("--issue-number must be a positive integer")
+    if not _REPO.match(args.repo):
+        parser.error("--repo must be owner/repo")
+    expected = f"https://github.com/{args.repo}/issues/{args.issue_number}"
+    if args.issue_url.rstrip("/").lower() != expected.lower():
+        parser.error(f"--issue-url must be {expected}")
+    args.issue_url = expected
+    return args
+
+
+def main(argv: list[str] | None = None) -> int:
+    args = parse_args(argv)
+    result = claim(args.issue_url, args.issue_number, os.environ)
+    print(json.dumps(result))
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/skills/test_clickup_claim.py b/tests/skills/test_clickup_claim.py
new file mode 100644
index 00000000..54ace0d9
--- /dev/null
+++ b/tests/skills/test_clickup_claim.py
@@ -0,0 +1,402 @@
+"""Behavior tests for the /sc:issue ClickUp claim script (design section 12).
+
+Enforcement type: EXECUTABLE (script behavior). ``urllib.request.urlopen`` is
+patched with a fake ClickUp server that serves recorded response shapes. Every
+fixture value is made up; no live value is ever copied here.
+
+Every test starts with all four ``CLICKUP_*`` variables cleared, so an
+exported real token, workspace, list filter or page cap never reaches a test.
+"""
+
+import ast
+import copy
+import email.message
+import importlib.util
+import io
+import json
+import sys
+import urllib.error
+import urllib.parse
+from pathlib import Path
+
+import pytest
+
+_SCRIPT = (
+    Path(__file__).resolve().parents[2]
+    / "src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py"
+)
+_spec = importlib.util.spec_from_file_location("clickup_claim", _SCRIPT)
+cc = importlib.util.module_from_spec(_spec)
+_spec.loader.exec_module(cc)
+
+TOKEN = "pk_000000_FAKETOKENFORTESTSONLY"
+WORKSPACE = "9000000001"
+REPO = "IronbellyOrg/IronClaude"
+NUMBER = 302
+ISSUE_URL = f"https://github.com/{REPO}/issues/{NUMBER}"
+ARGS = ["--issue-url", ISSUE_URL, "--issue-number", str(NUMBER), "--repo", REPO]
+CLICKUP_VARS = ("CLICKUP_API_TOKEN", "CLICKUP_WORKSPACE_ID", "CLICKUP_LIST_IDS", "CLICKUP_MAX_PAGES")
+
+# --- recorded response shapes (made-up values) --------------------------------
+
+# GET /api/v2/user (getauthorizeduser)
+USER_RESPONSE = {
+    "user": {
+        "id": 4242,
+        "username": "Test User",
+        "email": "test.user@example.com",
+        "color": "#000000",
+        "profilePicture": None,
+        "initials": "TU",
+        "week_start_day": 0,
+        "global_font_support": False,
+        "timezone": "UTC",
+    }
+}
+
+# one task of GET /api/v2/team/{team_Id}/task (getfilteredteamtasks)
+TASK_TEMPLATE = {
+    "id": "86abc0001",
+    "custom_id": None,
+    "name": "Example task",
+    "text_content": "",
+    "description": "",
+    "markdown_description": "",
+    "status": {"status": "to do", "type": "open"},
+    "assignees": [],
+    "watchers": [],
+    "tags": [],
+    "custom_fields": [],
+    "team_id": WORKSPACE,
+    "url": "https://app.clickup.com/t/86abc0001",
+    "list": {"id": "900100000001"},
+}
+
+# PUT /api/v2/task/{task_id} (updatetask)
+UPDATE_RESPONSE = {"id": "86abc0001", "name": "Example task", "status": {"status": "to do"}}
+
+
+def task(task_id, name="Example task", markdown="", custom=None, assignees=None):
+    t = copy.deepcopy(TASK_TEMPLATE)
+    t.update(
+        id=task_id,
+        name=name,
+        markdown_description=markdown,
+        url=f"https://app.clickup.com/t/{task_id}",
+        custom_fields=custom or [],
+        assignees=[{"id": a, "username": f"user{a}"} for a in (assignees or [])],
+    )
+    return t
+
+
+class FakeClickUp:
+    """Serves the recorded shapes and records every request."""
+
+    def __init__(self, pages=None, user_status=200, statuses=None):
+        self.pages = pages if pages is not None else [[]]
+        self.user_status = user_status
+        self.statuses = list(statuses or [])  # forced statuses, consumed in order
+        self.calls = []
+
+    def _error(self, url, code, retry_after=None):
+        headers = email.message.Message()
+        if retry_after is not None:
+            headers["Retry-After"] = str(retry_after)
+        return urllib.error.HTTPError(url, code, "error", headers, io.BytesIO(b"{}"))
+
+    def __call__(self, req, timeout=None):
+        url = req.full_url
+        body = json.loads(req.data.decode("utf-8")) if req.data else None
+        self.calls.append(
+            {
+                "method": req.get_method(),
+                "url": url,
+                "body": body,
+                "auth": req.get_header("Authorization"),
+            }
+        )
+        if self.statuses:
+            code, retry_after = self.statuses.pop(0)
+            if code != 200:
+                raise self._error(url, code, retry_after)
+        parsed = urllib.parse.urlparse(url)
+        if req.get_method() == "GET" and parsed.path == "/api/v2/user":
+            if self.user_status != 200:
+                raise self._error(url, self.user_status)
+            payload = USER_RESPONSE
+        elif req.get_method() == "GET" and parsed.path == f"/api/v2/team/{WORKSPACE}/task":
+            page = int(urllib.parse.parse_qs(parsed.query)["page"][0])
+            tasks = self.pages[page] if page < len(self.pages) else []
+            payload = {"tasks": tasks}
+        elif req.get_method() == "PUT" and parsed.path.startswith("/api/v2/task/"):
+            payload = UPDATE_RESPONSE
+        else:  # pragma: no cover - a request the script must never make
+            raise AssertionError(f"unexpected request {req.get_method()} {url}")
+        return io.BytesIO(json.dumps(payload).encode("utf-8"))
+
+    def puts(self):
+        return [c for c in self.calls if c["method"] == "PUT"]
+
+    def pages_requested(self):
+        return [
+            int(urllib.parse.parse_qs(urllib.parse.urlparse(c["url"]).query)["page"][0])
+            for c in self.calls
+            if "/task?" in c["url"]
+        ]
+
+
+@pytest.fixture(autouse=True)
+def clean_env(monkeypatch, capsys):
+    for name in CLICKUP_VARS:
+        monkeypatch.delenv(name, raising=False)
+    sleeps = []
+    monkeypatch.setattr(cc.time, "sleep", sleeps.append)
+    yield sleeps
+    out, err = capsys.readouterr()
+    assert TOKEN not in out and TOKEN not in err
+
+
+def configure(monkeypatch, fake, **extra):
+    monkeypatch.setenv("CLICKUP_API_TOKEN", TOKEN)
+    monkeypatch.setenv("CLICKUP_WORKSPACE_ID", WORKSPACE)
+    for name, value in extra.items():
+        monkeypatch.setenv(name, value)
+    monkeypatch.setattr(cc.urllib.request, "urlopen", fake)
+
+
+def run(capsys, args=ARGS):
+    code = cc.main(list(args))
+    out, err = capsys.readouterr()
+    assert TOKEN not in out and TOKEN not in err
+    return code, json.loads(out)
+
+
+# --- skipped -----------------------------------------------------------------
+
+
+def test_skipped_without_token(monkeypatch, capsys):
+    fake = FakeClickUp()
+    monkeypatch.setenv("CLICKUP_WORKSPACE_ID", WORKSPACE)
+    monkeypatch.setattr(cc.urllib.request, "urlopen", fake)
+    assert run(capsys) == (0, {"status": "skipped", "reason": "no_token"})
+    assert fake.calls == []
+
+
+def test_skipped_without_workspace(monkeypatch, capsys):
+    fake = FakeClickUp()
+    monkeypatch.setenv("CLICKUP_API_TOKEN", TOKEN)
+    monkeypatch.setattr(cc.urllib.request, "urlopen", fake)
+    assert run(capsys) == (0, {"status": "skipped", "reason": "no_workspace"})
+    assert fake.calls == []
+
+
+# --- matching ------------------------------------------------------------------
+
+
+def test_github_link_match_beats_title_match(monkeypatch, capsys):
+    fake = FakeClickUp(
+        pages=[
+            [
+                task("86title", name=f"Fix #{NUMBER} quickly"),
+                task("86link", markdown=f"Tracks {ISSUE_URL}/ in GitHub"),
+            ]
+        ]
+    )
+    configure(monkeypatch, fake)
+    code, out = run(capsys)
+    assert code == 0
+    assert out == {
+        "status": "assigned",
+        "task_id": "86link",
+        "task_url": "https://app.clickup.com/t/86link",
+        "rule": "github_link",
+    }
+
+
+def test_github_link_in_custom_field_value_matches(monkeypatch, capsys):
+    custom = [{"id": "cf1", "name": "GitHub", "type": "url", "value": ISSUE_URL.upper() + "#top"}]
+    fake = FakeClickUp(pages=[[task("86cf", custom=custom)]])
+    configure(monkeypatch, fake)
+    assert run(capsys)[1]["rule"] == "github_link"
+
+
+def test_github_link_with_longer_number_does_not_match(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86other", markdown=f"{ISSUE_URL}0")]])
+    configure(monkeypatch, fake)
+    assert run(capsys)[1] == {"status": "not_found"}
+
+
+def test_title_match_only_as_whole_token(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86a", name=f"Refactor #{NUMBER}0"), task("86b", name=f"x#{NUMBER}")]])
+    configure(monkeypatch, fake)
+    assert run(capsys)[1] == {"status": "not_found"}
+    assert fake.puts() == []
+
+
+def test_title_match_assigns_with_title_rule(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86a", name=f"Refactor #{NUMBER}0"), task("86b", name=f"[#{NUMBER}] claim it")]])
+    configure(monkeypatch, fake)
+    out = run(capsys)[1]
+    assert out["status"] == "assigned" and out["task_id"] == "86b" and out["rule"] == "title_number"
+
+
+def test_ambiguous_returns_candidates_and_makes_no_put(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86one", markdown=ISSUE_URL), task("86two", markdown=ISSUE_URL)]])
+    configure(monkeypatch, fake)
+    code, out = run(capsys)
+    assert code == 0
+    assert out["status"] == "ambiguous"
+    assert [c["task_id"] for c in out["candidates"]] == ["86one", "86two"]
+    assert fake.puts() == []
+
+
+def test_not_found(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86none", name="Unrelated")]])
+    configure(monkeypatch, fake)
+    assert run(capsys) == (0, {"status": "not_found"})
+
+
+# --- assignment ---------------------------------------------------------------
+
+
+def test_already_assigned_makes_no_put(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86mine", markdown=ISSUE_URL, assignees=[4242])]])
+    configure(monkeypatch, fake)
+    out = run(capsys)[1]
+    assert out == {
+        "status": "already_assigned",
+        "task_id": "86mine",
+        "task_url": "https://app.clickup.com/t/86mine",
+        "rule": "github_link",
+    }
+    assert fake.puts() == []
+
+
+def test_assign_sends_assignees_add_body(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86todo", markdown=ISSUE_URL, assignees=[7])]])
+    configure(monkeypatch, fake)
+    assert run(capsys)[1]["status"] == "assigned"
+    [put] = fake.puts()
+    assert put["url"] == "https://api.clickup.com/api/v2/task/86todo"
+    assert put["body"] == {"assignees": {"add": [4242]}}
+    assert all(c["auth"] == TOKEN for c in fake.calls)
+
+
+def test_list_ids_narrow_the_search(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[]])
+    configure(monkeypatch, fake, CLICKUP_LIST_IDS="111, 222")
+    run(capsys)
+    [search] = [c for c in fake.calls if "/task?" in c["url"]]
+    query = urllib.parse.parse_qs(urllib.parse.urlparse(search["url"]).query)
+    assert query["list_ids[]"] == ["111", "222"]
+    assert query["subtasks"] == ["true"] and query["include_markdown_description"] == ["true"]
+
+
+# --- errors -------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("status", [401, 403])
+def test_auth_failure_gives_auth(monkeypatch, capsys, status):
+    fake = FakeClickUp(user_status=status)
+    configure(monkeypatch, fake)
+    assert run(capsys) == (0, {"status": "error", "reason": "auth"})
+
+
+def test_429_is_retried_exactly_once_then_continues(monkeypatch, capsys, clean_env):
+    fake = FakeClickUp(pages=[[task("86t", markdown=ISSUE_URL)]], statuses=[(429, 7)])
+    configure(monkeypatch, fake)
+    assert run(capsys)[1]["status"] == "assigned"
+    assert clean_env == [7.0]
+    assert [c["method"] for c in fake.calls[:2]] == ["GET", "GET"]
+    assert fake.calls[0]["url"] == fake.calls[1]["url"]
+
+
+def test_429_twice_gives_rate_limited(monkeypatch, capsys, clean_env):
+    fake = FakeClickUp(statuses=[(429, 3), (429, 3)])
+    configure(monkeypatch, fake)
+    assert run(capsys) == (0, {"status": "error", "reason": "rate_limited"})
+    assert clean_env == [3.0]
+    assert len(fake.calls) == 2
+
+
+def test_other_http_error_gives_short_reason(monkeypatch, capsys):
+    fake = FakeClickUp(statuses=[(500, None)])
+    configure(monkeypatch, fake)
+    assert run(capsys) == (0, {"status": "error", "reason": "http_500"})
+
+
+# --- paging ---------------------------------------------------------------------
+
+
+def test_page_cap_is_honoured_and_first_page_is_zero(monkeypatch, capsys):
+    pages = [[task(f"86p{i}", name="Unrelated")] for i in range(10)]
+    fake = FakeClickUp(pages=pages)
+    configure(monkeypatch, fake, CLICKUP_MAX_PAGES="3")
+    assert run(capsys)[1] == {"status": "not_found"}
+    assert fake.pages_requested() == [0, 1, 2]
+    assert cc.FIRST_PAGE == 0
+
+
+def test_empty_page_ends_the_search(monkeypatch, capsys):
+    fake = FakeClickUp(pages=[[task("86p0", name="Unrelated")], []])
+    configure(monkeypatch, fake)
+    run(capsys)
+    assert fake.pages_requested() == [0, 1]
+
+
+@pytest.mark.parametrize("value", ["0", "-1", "abc", "", "2.5"])
+def test_invalid_max_pages_falls_back_to_default(monkeypatch, capsys, value):
+    pages = [[task(f"86p{i}", name="Unrelated")] for i in range(30)]
+    fake = FakeClickUp(pages=pages)
+    configure(monkeypatch, fake, CLICKUP_MAX_PAGES=value)
+    code, out = run(capsys)
+    assert code == 0 and out == {"status": "not_found"}
+    assert fake.pages_requested() == list(range(cc.DEFAULT_MAX_PAGES))
+    assert cc.DEFAULT_MAX_PAGES == 20
+
+
+# --- arguments ------------------------------------------------------------------
+
+
+@pytest.mark.parametrize(
+    "args",
+    [
+        [],
+        ["--issue-url", ISSUE_URL, "--issue-number", str(NUMBER)],
+        ["--issue-url", ISSUE_URL, "--issue-number", "abc", "--repo", REPO],
+        ["--issue-url", ISSUE_URL, "--issue-number", "0", "--repo", REPO],
+        ["--issue-url", ISSUE_URL, "--issue-number", str(NUMBER), "--repo", "not-a-repo"],
+        ["--issue-url", f"https://github.com/{REPO}/issues/1", "--issue-number", str(NUMBER), "--repo", REPO],
+    ],
+)
+def test_bad_arguments_exit_2(monkeypatch, args):
+    fake = FakeClickUp()
+    configure(monkeypatch, fake)
+    with pytest.raises(SystemExit) as exc:
+        cc.main(args)
+    assert exc.value.code == 2
+    assert fake.calls == []
+
+
+def test_token_never_printed_on_any_outcome(monkeypatch, capsys):
+    for fake in (
+        FakeClickUp(pages=[[task("86t", markdown=ISSUE_URL)]]),
+        FakeClickUp(user_status=401),
+        FakeClickUp(statuses=[(429, 1), (429, 1)]),
+        FakeClickUp(statuses=[(500, None)]),
+    ):
+        configure(monkeypatch, fake)
+        cc.main(list(ARGS))
+        out, err = capsys.readouterr()
+        assert TOKEN not in out and TOKEN not in err
+
+
+def test_script_imports_only_standard_library():
+    tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
+    names = set()
+    for node in ast.walk(tree):
+        if isinstance(node, ast.Import):
+            names.update(alias.name.split(".")[0] for alias in node.names)
+        elif isinstance(node, ast.ImportFrom) and node.module:
+            names.add(node.module.split(".")[0])
+    assert names <= set(sys.stdlib_module_names)
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t2-pytest.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t2-pytest.log
new file mode 100644
index 00000000..1bfb83fd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t2-pytest.log
@@ -0,0 +1,44 @@
+$ uv run pytest tests/skills/test_clickup_claim.py -v
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 32 items
+
+tests/skills/test_clickup_claim.py::test_skipped_without_token PASSED    [  3%]
+tests/skills/test_clickup_claim.py::test_skipped_without_workspace PASSED [  6%]
+tests/skills/test_clickup_claim.py::test_github_link_match_beats_title_match PASSED [  9%]
+tests/skills/test_clickup_claim.py::test_github_link_in_custom_field_value_matches PASSED [ 12%]
+tests/skills/test_clickup_claim.py::test_github_link_with_longer_number_does_not_match PASSED [ 15%]
+tests/skills/test_clickup_claim.py::test_title_match_only_as_whole_token PASSED [ 18%]
+tests/skills/test_clickup_claim.py::test_title_match_assigns_with_title_rule PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_ambiguous_returns_candidates_and_makes_no_put PASSED [ 25%]
+tests/skills/test_clickup_claim.py::test_not_found PASSED                [ 28%]
+tests/skills/test_clickup_claim.py::test_already_assigned_makes_no_put PASSED [ 31%]
+tests/skills/test_clickup_claim.py::test_assign_sends_assignees_add_body PASSED [ 34%]
+tests/skills/test_clickup_claim.py::test_list_ids_narrow_the_search PASSED [ 37%]
+tests/skills/test_clickup_claim.py::test_auth_failure_gives_auth[401] PASSED [ 40%]
+tests/skills/test_clickup_claim.py::test_auth_failure_gives_auth[403] PASSED [ 43%]
+tests/skills/test_clickup_claim.py::test_429_is_retried_exactly_once_then_continues PASSED [ 46%]
+tests/skills/test_clickup_claim.py::test_429_twice_gives_rate_limited PASSED [ 50%]
+tests/skills/test_clickup_claim.py::test_other_http_error_gives_short_reason PASSED [ 53%]
+tests/skills/test_clickup_claim.py::test_page_cap_is_honoured_and_first_page_is_zero PASSED [ 56%]
+tests/skills/test_clickup_claim.py::test_empty_page_ends_the_search PASSED [ 59%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[0] PASSED [ 62%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[-1] PASSED [ 65%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[abc] PASSED [ 68%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[] PASSED [ 71%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[2.5] PASSED [ 75%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args0] PASSED [ 78%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args1] PASSED [ 81%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args2] PASSED [ 84%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args3] PASSED [ 87%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args4] PASSED [ 90%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args5] PASSED [ 93%]
+tests/skills/test_clickup_claim.py::test_token_never_printed_on_any_outcome PASSED [ 96%]
+tests/skills/test_clickup_claim.py::test_script_imports_only_standard_library PASSED [100%]
+
+============================== 32 passed in 0.14s ==============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t2-clickup-skipped.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t2-clickup-skipped.txt
new file mode 100644
index 00000000..dd6e2915
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t2-clickup-skipped.txt
@@ -0,0 +1,3 @@
+$ env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --issue-url https://github.com/IronbellyOrg/IronClaude/issues/302 --issue-number 302 --repo IronbellyOrg/IronClaude
+{"status": "skipped", "reason": "no_token"}
+rc=0

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
