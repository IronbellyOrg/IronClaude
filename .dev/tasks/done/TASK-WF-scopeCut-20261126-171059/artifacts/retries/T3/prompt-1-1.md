7d3fba74c50116cec2c2962153a7011f26bb0d72
Review one task for spec compliance.

Task brief: ## Task 3: Add the repo read, the 90-day push check and the existing-state read

Depends on: Task 1, Task 2

Add to `scripts/apply_org_rulesets.py`, each taking a `Runner` and returning plain data: `read_repo(runner, org, repo)` (canonical owner and name, `archived`, `default_branch`, `permissions.admin`, which of `master` and `integration` exist through GET `branches/<b>`; it returns the refusal reasons `archived`, `no-admin` and `no-default-branch` as data); `check_push(runner, org, repo, branches, now)` as in source.md section 2.3 step 2 (one UTC cutoff of now minus 90 days; the `activity` source with pagination, counting `push`, `force_push` and `branch_deletion` and ignoring `pr_merge`; the fallback to `commits` plus `commits/<sha>/pulls` when the primary source answers 403 or 404 or paginates past a cap of pages named in one constant; more than 200 pull-request lookups gives `incomplete`; the result per branch is `pass`, `blocked` or `incomplete` with an evidence count, and the overall result is `pass` only when every branch passes); and `read_existing(runner, org, repo, branches)` (GET `rulesets` with pagination, the names present; GET `branches/<b>/protection` per branch, 200 means classic protection, 404 means none, anything else is recorded as unknown; GET `git/matching-refs/tags/v` for the count of `v*` tags).

Create `tests/org_rulesets/test_checks.py` using `FakeRunner`.

Acceptance criteria:
- `read_repo` accepts a different letter case and stores GitHub's canonical spelling; it returns the reasons `archived`, `no-admin` and `no-default-branch` for an archived repo, a repo without admin and a repo with no default branch.
- Zero direct pushes on every branch gives `pass`; a `push` event inside the window gives `blocked`; a `pr_merge` event is ignored; an event older than the cutoff is ignored by both sources.
- A 403 on `activity` falls back to commits: a commit with a merged pull request is not a direct push and a commit with none is; a 403 on both sources, a truncated page chain and a failed pull-request lookup each give `incomplete`; 201 lookups gives `incomplete`. `incomplete` is never reported as `pass`.
- `read_existing` reports a same-name ruleset, classic protection (200), none (404), unknown (any other answer) and the count of `v*` tags.
- The closing checks of the Constraints pass.

Global constraints: ## Constraints

- No task calls GitHub or touches any IronbellyGroup repo. Every GitHub call in a test goes through `FakeRunner` of `tests/org_rulesets/conftest.py`; no test starts the real `gh`.
- `.github/rulesets/*.json`, the commands in `docs/developer-guide/branch-protection.md` and `tests/docs/test_branch_protection_rulesets.py` stay unchanged. The only edit to the guide is the one link line of Task 7. The existing test must keep passing.
- Python 3.10, standard library only; ruff rules `E,F,I,N,W,TID` at line length 88 as set in `pyproject.toml`.
- No real private repo name and no real org login is written in any tracked file. Tests use synthetic names such as `acme-one`. The script holds no org or repo name, except the upstream org name it refuses.
- Only these paths may change: `scripts/apply_org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`, `docs/developer-guide/branch-protection.md` (one link line) and `docs/developer-guide/documentation-index.md`. Nothing under `.claude/` or `.github/` changes.
- "source.md section 2.3" names a heading of `./source.md`.
- Test setup follows `tests/worktree_cleanup/conftest.py` (the session fixture `wc` at lines 26 to 37 loads the script once; `RecordingRunner` at lines 68 to 109 subclasses the real `Runner` and overrides `_execute`). `tests/org_rulesets/conftest.py` defines the session fixture `orr` (the script module) and every shared fixture exactly once; a test module never imports a fixture from another module, because CI lists fixtures with `pytest --fixtures` and a duplicate crashes it.
- Location rule: the repo root is `Path(__file__).resolve().parent.parent`, the rule files are read from `<root>/.github/rulesets/`, and no function reads the current working folder. The before-state file is written into the folder given with `--out`.
- Choices for the owner's review (all are made inside the scope cut and listed in the pull request): one repo per run; the push check excuses no direct push by a named person; the tag ruleset is applied with a printed warning and a manual check of release workflows; rollback is manual.
- Every task ends with the same checks: `uv run pytest tests/org_rulesets/` passes (plus `tests/docs/test_branch_protection_rulesets.py` from Task 6 on), `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing.

Start sha: 7d3fba74c50116cec2c2962153a7011f26bb0d72
Diff against the start snapshot: diff --git a/scripts/apply_org_rulesets.py b/scripts/apply_org_rulesets.py
index eafeb9141..7026a5f48 100644
--- a/scripts/apply_org_rulesets.py
+++ b/scripts/apply_org_rulesets.py
@@ -18,6 +18,7 @@ import os
 import re
 import subprocess
 from dataclasses import dataclass, field
+from datetime import datetime, timedelta, timezone
 from pathlib import Path
 
 EXIT_OK = 0
@@ -316,3 +317,237 @@ class Runner:
         except OSError as exc:
             return Result(127, "", f"{type(exc).__name__}: {exc}")
         return Result(proc.returncode, proc.stdout, proc.stderr)
+
+
+# --- Reads: the repo, the 90-day push check, what already exists ------------------
+
+PUSH_WINDOW_DAYS = 90
+PER_PAGE = 100
+# More pages than this and a list answer counts as cut short.
+PAGE_CAP = 10
+# More commits than this and the pull-request lookups of one branch stop.
+LOOKUP_CAP = 200
+# The activity event types that are direct pushes (``pr_merge`` is not).
+DIRECT_PUSH_TYPES = frozenset({"push", "force_push", "branch_deletion"})
+
+
+def http_status(result: Result) -> int:
+    """200 for a successful call, else the HTTP status ``gh`` printed, else 0."""
+    if result.returncode == 0:
+        return 200
+    found = re.search(r"HTTP (\d{3})", result.stderr)
+    return int(found.group(1)) if found else 0
+
+
+def _items(result: Result) -> tuple[list, int]:
+    """The items and the page count of a paginated list answer. ``gh --paginate``
+    prints one JSON array per page back to back; anything else is a ValueError."""
+    text = result.stdout.strip()
+    if result.returncode != 0 or not text:
+        raise ValueError("the call failed or gave no answer")
+    decoder = json.JSONDecoder()
+    items: list = []
+    pages = pos = 0
+    while pos < len(text):
+        value, pos = decoder.raw_decode(text, pos)
+        if not isinstance(value, list):
+            raise ValueError("a page is not a list")
+        items.extend(value)
+        pages += 1
+        while pos < len(text) and text[pos].isspace():
+            pos += 1
+    return items, pages
+
+
+def _json_object(result: Result) -> dict | None:
+    if http_status(result) != 200:
+        return None
+    try:
+        data = json.loads(result.stdout)
+    except ValueError:
+        return None
+    return data if isinstance(data, dict) else None
+
+
+def read_repo(runner: Runner, org: str, repo: str) -> dict:
+    """Facts about the repo, and the reasons the script must refuse it (``archived``,
+    ``no-admin``, ``no-default-branch``, ``unreadable``, ``unreadable-branch``)."""
+    answer = runner.run(["gh", "api", f"repos/{org}/{repo}"])
+    info = {
+        "owner": org,
+        "name": repo,
+        "archived": False,
+        "default_branch": None,
+        "admin": False,
+        "existing": [],
+        "refusals": [],
+        "status": http_status(answer),
+    }
+    data = _json_object(answer)
+    if data is None:
+        info["refusals"].append("unreadable")
+        return info
+    info["owner"] = (data.get("owner") or {}).get("login") or org
+    info["name"] = data.get("name") or repo
+    info["archived"] = bool(data.get("archived"))
+    info["default_branch"] = data.get("default_branch") or None
+    info["admin"] = bool((data.get("permissions") or {}).get("admin"))
+    if info["archived"]:
+        info["refusals"].append("archived")
+    if not info["admin"]:
+        info["refusals"].append("no-admin")
+    if not info["default_branch"]:
+        info["refusals"].append("no-default-branch")
+    base = f"repos/{info['owner']}/{info['name']}"
+    for branch in FIXED_BRANCHES:
+        status = http_status(runner.run(["gh", "api", f"{base}/branches/{branch}"]))
+        if status == 200:
+            info["existing"].append(branch)
+        elif status != 404:
+            info["refusals"].append("unreadable-branch")
+    return info
+
+
+def _stamp(text: str) -> datetime:
+    return datetime.fromisoformat(text.replace("Z", "+00:00"))
+
+
+def _push_activity(runner, org, repo, branch, cutoff):
+    """The activity source for one branch, or None when it gives no full answer."""
+    query = f"ref=refs/heads/{branch}&time_period=quarter&per_page={PER_PAGE}"
+    answer = runner.run(
+        ["gh", "api", "--paginate", f"repos/{org}/{repo}/activity?{query}"]
+    )
+    if answer.returncode != 0:
+        return None
+    try:
+        items, pages = _items(answer)
+        if pages > PAGE_CAP:
+            return None
+        window = [e for e in items if _stamp(e["timestamp"]) >= cutoff]
+        direct = sum(1 for e in window if e["activity_type"] in DIRECT_PUSH_TYPES)
+    except (ValueError, KeyError, TypeError):
+        return None
+    return {
+        "result": "blocked" if direct else "pass",
+        "source": "activity",
+        "direct_pushes": direct,
+        "examined": len(window),
+    }
+
+
+def _merged_into(pulls: object, branch: str) -> bool:
+    if not isinstance(pulls, list):
+        raise ValueError("not a list of pull requests")
+    return any(
+        isinstance(p, dict)
+        and p.get("merged_at")
+        and (p.get("base") or {}).get("ref", branch) == branch
+        for p in pulls
+    )
+
+
+def _push_commits(runner, org, repo, branch, cutoff):
+    """The fallback: a commit with no merged pull request is a direct push."""
+    out = {"source": "commits", "direct_pushes": 0, "examined": 0}
+    query = f"sha={branch}&since={_iso(cutoff)}&per_page={PER_PAGE}"
+    answer = runner.run(
+        ["gh", "api", "--paginate", f"repos/{org}/{repo}/commits?{query}"]
+    )
+    try:
+        if answer.returncode != 0:
+            raise ValueError("the commit list failed")
+        commits, pages = _items(answer)
+        shas = [c["sha"] for c in commits]
+        if pages > PAGE_CAP:
+            raise ValueError("the commit list was cut short")
+    except (ValueError, KeyError, TypeError) as exc:
+        return {**out, "result": "incomplete", "note": str(exc)}
+    unknown = len(shas) > LOOKUP_CAP
+    for sha in shas[:LOOKUP_CAP]:
+        reply = runner.run(["gh", "api", f"repos/{org}/{repo}/commits/{sha}/pulls"])
+        out["examined"] += 1
+        try:
+            if reply.returncode != 0:
+                raise ValueError("a pull-request lookup failed")
+            merged = _merged_into(json.loads(reply.stdout), branch)
+        except ValueError:
+            unknown = True
+            continue
+        if not merged:
+            out["direct_pushes"] += 1
+    if out["direct_pushes"]:
+        return {**out, "result": "blocked"}
+    if unknown:
+        return {**out, "result": "incomplete", "note": "not every commit was checked"}
+    return {**out, "result": "pass"}
+
+
+def _iso(moment: datetime) -> str:
+    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")
+
+
+def check_push(
+    runner: Runner, org: str, repo: str, branches: list[str], now: datetime
+) -> dict:
+    """The direct-push check, per branch, over the last 90 days.
+
+    One UTC cutoff for the run. A branch is ``pass`` only with zero direct pushes
+    from a source that gave a full answer, ``blocked`` with any, ``incomplete``
+    otherwise. The overall result is ``pass`` only when every branch passes.
+    """
+    cutoff = now.astimezone(timezone.utc) - timedelta(days=PUSH_WINDOW_DAYS)
+    per_branch = {}
+    for branch in branches:
+        found = _push_activity(runner, org, repo, branch, cutoff)
+        per_branch[branch] = found or _push_commits(runner, org, repo, branch, cutoff)
+    results = {v["result"] for v in per_branch.values()}
+    if "blocked" in results:
+        overall = "blocked"
+    elif results == {"pass"}:
+        overall = "pass"
+    else:
+        overall = "incomplete"
+    return {"result": overall, "cutoff": _iso(cutoff), "branches": per_branch}
+
+
+def read_existing(runner: Runner, org: str, repo: str, branches: list[str]) -> dict:
+    """What the repo already has: ruleset names (``rulesets`` is None when the list
+    could not be read), classic protection per branch (``classic``, ``none`` or
+    ``unknown``) and the number of ``v*`` tags (None when unknown)."""
+    base = f"repos/{org}/{repo}"
+    listed = runner.run(
+        ["gh", "api", "--paginate", f"{base}/rulesets?per_page={PER_PAGE}"]
+    )
+    rulesets = None
+    try:
+        items, _ = _items(listed)
+        rulesets = {}
+        for item in items:
+            rulesets.setdefault(item["name"], item["id"])
+    except (ValueError, KeyError, TypeError):
+        rulesets = None
+    protection = {}
+    for branch in branches:
+        status = http_status(
+            runner.run(["gh", "api", f"{base}/branches/{branch}/protection"])
+        )
+        protection[branch] = {200: "classic", 404: "none"}.get(status, "unknown")
+    tags = runner.run(
+        [
+            "gh",
+            "api",
+            "--paginate",
+            f"{base}/git/matching-refs/tags/v?per_page={PER_PAGE}",
+        ]
+    )
+    try:
+        v_tags = len(_items(tags)[0])
+    except (ValueError, TypeError):
+        v_tags = None
+    return {
+        "rulesets": rulesets,
+        "rulesets_status": http_status(listed),
+        "protection": protection,
+        "v_tags": v_tags,
+    }
diff --git a/tests/org_rulesets/conftest.py b/tests/org_rulesets/conftest.py
index 2bca4720c..e35c25af7 100644
--- a/tests/org_rulesets/conftest.py
+++ b/tests/org_rulesets/conftest.py
@@ -56,6 +56,16 @@ def fake_runner_cls(orr):
         def ok(data):
             return orr.Result(0, json.dumps(data), "")
 
+        @staticmethod
+        def pages(*pages):
+            """What ``gh api --paginate`` prints: one JSON array per page."""
+            return orr.Result(0, "".join(json.dumps(p) for p in pages), "")
+
+        @staticmethod
+        def http(status):
+            """A failed call, as ``gh`` reports it."""
+            return orr.Result(1, '{"message": "m"}', f"gh: m (HTTP {status})")
+
         @staticmethod
         def method_of(argv):
             return argv[argv.index("--method") + 1] if "--method" in argv else "GET"
diff --git a/tests/org_rulesets/test_checks.py b/tests/org_rulesets/test_checks.py
new file mode 100644
index 000000000..20de31a8a
--- /dev/null
+++ b/tests/org_rulesets/test_checks.py
@@ -0,0 +1,353 @@
+"""read_repo, check_push (the 90-day direct-push check) and read_existing."""
+
+from __future__ import annotations
+
+from datetime import datetime, timezone
+
+import pytest
+
+NOW = datetime(2026, 11, 26, 17, 0, tzinfo=timezone.utc)
+CUTOFF = "2026-08-28T17:00:00Z"  # NOW minus 90 days
+IN_WINDOW = "2026-10-01T10:00:00Z"
+OLD = "2026-08-01T10:00:00Z"
+REPO = "repos/acme/acme-one"
+
+
+def sha(n):
+    return f"{n:040x}"
+
+
+def event(kind, when=IN_WINDOW):
+    return {"activity_type": kind, "timestamp": when}
+
+
+def activity_path(branch):
+    return f"{REPO}/activity?ref=refs/heads/{branch}&time_period=quarter&per_page=100"
+
+
+def commits_path(branch):
+    return f"{REPO}/commits?sha={branch}&since={CUTOFF}&per_page=100"
+
+
+@pytest.fixture
+def make(fake_runner_cls):
+    """A fake runner whose canned answers are given as a dict of GET paths."""
+
+    def build(gets):
+        return fake_runner_cls({("GET", path): answer for path, answer in gets.items()})
+
+    return build
+
+
+# --- read_repo ---------------------------------------------------------------------
+
+
+def repo_answer(ok, **changes):
+    data = {
+        "owner": {"login": "acme"},
+        "name": "acme-one",
+        "archived": False,
+        "default_branch": "main",
+        "permissions": {"admin": True},
+    }
+    return ok({**data, **changes})
+
+
+def test_read_repo_uses_the_canonical_spelling(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    runner = make(
+        {
+            "repos/ACME/Acme-One": repo_answer(ok),
+            f"{REPO}/branches/master": ok({}),
+            f"{REPO}/branches/integration": fake_runner_cls.http(404),
+        }
+    )
+    info = orr.read_repo(runner, "ACME", "Acme-One")
+    assert (info["owner"], info["name"]) == ("acme", "acme-one")
+    assert info["default_branch"] == "main"
+    assert info["existing"] == ["master"]
+    assert info["refusals"] == []
+    # the branch calls name the canonical repo in full
+    assert runner.commands[1].argv[-1] == f"{REPO}/branches/integration"
+
+
+@pytest.mark.parametrize(
+    ("changes", "reasons"),
+    [
+        ({"archived": True}, ["archived"]),
+        ({"permissions": {"admin": False}}, ["no-admin"]),
+        ({"permissions": None}, ["no-admin"]),
+        ({"default_branch": None}, ["no-default-branch"]),
+        (
+            {"archived": True, "permissions": {}, "default_branch": ""},
+            ["archived", "no-admin", "no-default-branch"],
+        ),
+    ],
+)
+def test_read_repo_refusal_reasons(make, orr, fake_runner_cls, changes, reasons):
+    ok = fake_runner_cls.ok
+    runner = make(
+        {
+            REPO: repo_answer(ok, **changes),
+            f"{REPO}/branches/master": ok({}),
+            f"{REPO}/branches/integration": ok({}),
+        }
+    )
+    assert orr.read_repo(runner, "acme", "acme-one")["refusals"] == reasons
+
+
+def test_read_repo_unreadable(make, orr, fake_runner_cls):
+    runner = make({REPO: fake_runner_cls.http(404)})
+    info = orr.read_repo(runner, "acme", "acme-one")
+    assert info["refusals"] == ["unreadable"] and info["status"] == 404
+    assert len(runner.executed) == 1
+
+
+def test_read_repo_branch_lookup_failure_is_a_refusal(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    runner = make(
+        {
+            REPO: repo_answer(ok),
+            f"{REPO}/branches/master": fake_runner_cls.http(500),
+            f"{REPO}/branches/integration": ok({}),
+        }
+    )
+    info = orr.read_repo(runner, "acme", "acme-one")
+    assert info["refusals"] == ["unreadable-branch"]
+    assert info["existing"] == ["integration"]
+
+
+# --- check_push --------------------------------------------------------------------
+
+
+def test_zero_direct_pushes_pass(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    runner = make(
+        {
+            activity_path("master"): ok([event("pr_merge"), event("branch_creation")]),
+            activity_path("integration"): fake_runner_cls.pages([], []),
+        }
+    )
+    got = orr.check_push(runner, "acme", "acme-one", ["integration", "master"], NOW)
+    assert got["result"] == "pass" and got["cutoff"] == CUTOFF
+    assert got["branches"]["master"]["direct_pushes"] == 0
+    assert got["branches"]["master"]["examined"] == 2
+    assert got["branches"]["master"]["source"] == "activity"
+
+
+@pytest.mark.parametrize("kind", ["push", "force_push", "branch_deletion"])
+def test_a_direct_push_in_the_window_blocks(make, orr, fake_runner_cls, kind):
+    ok = fake_runner_cls.ok
+    runner = make({activity_path("master"): ok([event("pr_merge"), event(kind)])})
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "blocked"
+    assert got["branches"]["master"]["direct_pushes"] == 1
+
+
+def test_old_events_and_merges_are_ignored(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    events = [event("push", OLD), event("force_push", OLD), event("pr_merge")]
+    runner = make({activity_path("master"): ok(events)})
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "pass"
+
+
+def test_pages_are_joined(make, orr, fake_runner_cls):
+    pages = fake_runner_cls.pages([event("pr_merge")], [event("push")])
+    runner = make({activity_path("master"): pages})
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "blocked"
+
+
+def commit_runner(make, fake_runner_cls, branch, commits, pulls):
+    """Activity answers 403; the commit list and the pull lookups are canned."""
+    gets = {
+        activity_path(branch): fake_runner_cls.http(403),
+        commits_path(branch): fake_runner_cls.ok([{"sha": sha(n)} for n in commits]),
+    }
+    for n, answer in pulls.items():
+        gets[f"{REPO}/commits/{sha(n)}/pulls"] = answer
+    return make(gets)
+
+
+def merged(branch="master"):
+    return [{"merged_at": "2026-10-01T10:00:00Z", "base": {"ref": branch}}]
+
+
+def test_fallback_a_merged_commit_is_not_a_direct_push(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    runner = commit_runner(
+        make, fake_runner_cls, "master", [1, 2], {1: ok(merged()), 2: ok(merged())}
+    )
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "pass"
+    assert got["branches"]["master"]["source"] == "commits"
+    assert got["branches"]["master"]["examined"] == 2
+
+
+def test_fallback_a_commit_with_no_merged_pull_is_a_direct_push(
+    make, orr, fake_runner_cls
+):
+    ok = fake_runner_cls.ok
+    opened = [{"merged_at": None, "base": {"ref": "master"}}]
+    other = merged("other")
+    pulls = {1: ok(merged()), 2: ok([]), 3: ok(opened), 4: ok(other)}
+    runner = commit_runner(make, fake_runner_cls, "master", [1, 2, 3, 4], pulls)
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "blocked"
+    assert got["branches"]["master"]["direct_pushes"] == 3
+
+
+def test_both_sources_forbidden_is_incomplete(make, orr, fake_runner_cls):
+    http = fake_runner_cls.http
+    runner = make(
+        {activity_path("master"): http(403), commits_path("master"): http(403)}
+    )
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "incomplete"
+
+
+def test_a_failed_pull_lookup_is_incomplete(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    pulls = {1: ok(merged()), 2: fake_runner_cls.http(502)}
+    runner = commit_runner(make, fake_runner_cls, "master", [1, 2], pulls)
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "incomplete"
+
+
+def test_a_direct_push_wins_over_a_failed_lookup(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    pulls = {1: fake_runner_cls.http(502), 2: ok([])}
+    runner = commit_runner(make, fake_runner_cls, "master", [1, 2], pulls)
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "blocked"
+
+
+def test_a_truncated_page_chain_is_incomplete(make, orr, fake_runner_cls):
+    too_many = fake_runner_cls.pages(*[[] for _ in range(orr.PAGE_CAP + 1)])
+    runner = make({activity_path("master"): too_many, commits_path("master"): too_many})
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "incomplete"
+    assert got["branches"]["master"]["source"] == "commits"
+
+
+def test_activity_past_the_cap_falls_back_to_commits(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    too_many = fake_runner_cls.pages(*[[] for _ in range(orr.PAGE_CAP + 1)])
+    runner = make({activity_path("master"): too_many, commits_path("master"): ok([])})
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "pass"
+    assert got["branches"]["master"]["source"] == "commits"
+
+
+def test_201_lookups_is_incomplete_and_200_are_made(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    numbers = list(range(1, 202))
+    pulls = {n: ok(merged()) for n in numbers}
+    runner = commit_runner(make, fake_runner_cls, "master", numbers, pulls)
+    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+    assert got["result"] == "incomplete"
+    looked_up = [c for c in runner.commands if c.argv[-1].endswith("/pulls")]
+    assert len(looked_up) == orr.LOOKUP_CAP == 200
+
+
+def test_exactly_200_lookups_can_pass(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    numbers = list(range(1, 201))
+    pulls = {n: ok(merged()) for n in numbers}
+    runner = commit_runner(make, fake_runner_cls, "master", numbers, pulls)
+    assert (
+        orr.check_push(runner, "acme", "acme-one", ["master"], NOW)["result"] == "pass"
+    )
+
+
+def test_overall_result_blocked_beats_incomplete_beats_pass(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    http = fake_runner_cls.http
+    gets = {
+        activity_path("integration"): ok([]),
+        activity_path("master"): ok([event("push")]),
+        activity_path("main"): http(403),
+        commits_path("main"): http(403),
+    }
+    runner = make(gets)
+    run = orr.check_push
+    assert (
+        run(runner, "acme", "acme-one", ["integration", "master"], NOW)["result"]
+        == "blocked"
+    )
+    assert (
+        run(runner, "acme", "acme-one", ["integration", "main"], NOW)["result"]
+        == "incomplete"
+    )
+    assert run(runner, "acme", "acme-one", ["integration"], NOW)["result"] == "pass"
+    assert (
+        run(runner, "acme", "acme-one", ["master", "main"], NOW)["result"] == "blocked"
+    )
+
+
+def test_no_branch_is_never_a_pass(make, orr):
+    assert (
+        orr.check_push(make({}), "acme", "acme-one", [], NOW)["result"] == "incomplete"
+    )
+
+
+def test_garbage_from_both_sources_is_incomplete(make, orr, fake_runner_cls):
+    for text in ("", "not json", '{"a": 1}', '[{"timestamp": "x"}]'):
+        bad = orr.Result(0, text, "")
+        runner = make({activity_path("master"): bad, commits_path("master"): bad})
+        got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
+        assert got["result"] == "incomplete", text
+
+
+# --- read_existing -----------------------------------------------------------------
+
+
+def test_read_existing_reports_each_part(make, orr, fake_runner_cls):
+    ok, http = fake_runner_cls.ok, fake_runner_cls.http
+    runner = make(
+        {
+            f"{REPO}/rulesets?per_page=100": fake_runner_cls.pages(
+                [{"id": 9, "name": "protect-master"}], [{"id": 10, "name": "other"}]
+            ),
+            f"{REPO}/branches/integration/protection": ok({}),
+            f"{REPO}/branches/master/protection": http(404),
+            f"{REPO}/branches/main/protection": http(500),
+            f"{REPO}/git/matching-refs/tags/v?per_page=100": ok([{}, {}, {}]),
+        }
+    )
+    got = orr.read_existing(
+        runner, "acme", "acme-one", ["integration", "master", "main"]
+    )
+    assert got["rulesets"] == {"protect-master": 9, "other": 10}
+    assert got["protection"] == {
+        "integration": "classic",
+        "master": "none",
+        "main": "unknown",
+    }
+    assert got["v_tags"] == 3
+
+
+def test_read_existing_unknown_when_the_reads_fail(make, orr, fake_runner_cls):
+    http = fake_runner_cls.http
+    runner = make(
+        {
+            f"{REPO}/rulesets?per_page=100": http(403),
+            f"{REPO}/git/matching-refs/tags/v?per_page=100": http(403),
+        }
+    )
+    got = orr.read_existing(runner, "acme", "acme-one", [])
+    assert got["rulesets"] is None and got["rulesets_status"] == 403
+    assert got["v_tags"] is None and got["protection"] == {}
+
+
+def test_read_existing_no_rulesets_and_no_tags(make, orr, fake_runner_cls):
+    ok = fake_runner_cls.ok
+    runner = make(
+        {
+            f"{REPO}/rulesets?per_page=100": ok([]),
+            f"{REPO}/git/matching-refs/tags/v?per_page=100": ok([]),
+        }
+    )
+    got = orr.read_existing(runner, "acme", "acme-one", [])
+    assert got["rulesets"] == {} and got["v_tags"] == 0

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
