ad5823289c69c2eccf6aa4e4a7a7e9b51616b0d5
Review one task for spec compliance.

Task brief: ## Task 4: Add the dry-run report and apply

Depends on: Task 1, Task 2, Task 3

Add `dry_run_report(...)` and `apply_repo(runner, org, repo, out_dir, confirm, now)` to `scripts/apply_org_rulesets.py` as in source.md sections 2.3 step 4 and 2.4. `dry_run_report` assembles and returns the printed lines from the results of Task 3: repo facts, the push-check result per branch with its evidence count, the existing state, the count of `v*` tags with a warning line that the tag ruleset blocks moving and deleting tags so release workflows must be checked by hand first, the rulesets that would be created in order (a same-name ruleset already present is listed as skipped), the digest from `payload_digest` and the exact apply command. `dry_run_report(runner, org, repo, now)` itself calls `read_repo`, `check_push` and `read_existing`. `apply_repo` carries no state from the dry run: it calls the same three functions again and recomputes the digest of all rendered bodies in order (a skipped same-name ruleset does not change the digest). It refuses, with the failed check named and no write call, unless `confirm` equals that digest, the push check is `pass`, no branch has classic protection, the repo has no refusal reason and `out_dir` is given. Then it writes `<repo>-before.json` into `out_dir` once (it must not exist; it holds the full body of every existing ruleset read by id and the protection state of each branch of the set, a 404 recorded as the string `"none"`, a 403 raises and writes nothing); then for each body in order, skipping a body whose name is already present, it POSTs the body (`name` is recorded in the `CommandRecord`), reads the ruleset back by id and compares it with `compare_bodies`; it stops at the first failure and returns what was written. A `TIMED_OUT` POST is followed by one list call before any other call, a matching same-name ruleset is adopted, and a POST is never repeated. It returns the ids by name and the one-line comment text for issue 838 (repo, date, ids by name); it never posts the comment and never makes a call that names the ruleset ids 28081842, 28081844 or 28081845. It also returns the manual rollback commands, one `gh api --method DELETE repos/<org>/<repo>/rulesets/<id>` per id it created.

Create `tests/org_rulesets/test_apply.py`.

Acceptance criteria:
- A dry run makes no POST call and its lines contain every item listed above.
- `apply_repo` with a wrong `confirm`, a push check of `blocked` or `incomplete`, classic protection, an archived repo or no `out_dir` makes no write call and no file, and names the failed check.
- The recorded call order is tag ruleset, then `integration`, then `master`, each read back before the next write; three POSTs get three different ids from the fake.
- `<repo>-before.json` holds complete bodies even when the list call returns summaries without `rules`; a second `apply_repo` for the same repo and folder refuses because the file exists, before any write.
- A read-back mismatch stops the run after the first ruleset and the returned result lists only what was written; a non-success POST does the same.
- A `TIMED_OUT` POST is followed by a list call and never by a second POST; a matching same-name ruleset found by that list is adopted.
- A same-name ruleset already present gets no POST and no PUT; the fake records no PUT and no DELETE in any test.
- The comment line and the rollback commands contain the created ids.
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

Start sha: ad5823289c69c2eccf6aa4e4a7a7e9b51616b0d5
Diff against the start snapshot: diff --git a/scripts/apply_org_rulesets.py b/scripts/apply_org_rulesets.py
index 7026a5f48..6fa1917c7 100644
--- a/scripts/apply_org_rulesets.py
+++ b/scripts/apply_org_rulesets.py
@@ -551,3 +551,256 @@ def read_existing(runner: Runner, org: str, repo: str, branches: list[str]) -> d
         "protection": protection,
         "v_tags": v_tags,
     }
+
+
+# --- The dry run and apply ----------------------------------------------------------
+
+# The IronClaude rulesets. The script never names these ids in any call: a repo that
+# lists one of them is refused.
+PROTECTED_RULESET_IDS = frozenset({28081842, 28081844, 28081845})
+
+_REFUSAL_TEXT = {
+    "archived": "repo is archived",
+    "no-admin": "no admin permission on the repo",
+    "no-default-branch": "repo has no default branch",
+    "unreadable": "repo cannot be read (HTTP {status})",
+    "unreadable-branch": "a branch lookup failed",
+}
+
+
+def _assess(runner: Runner, org: str, repo: str, now: datetime) -> dict:
+    """Everything a dry run and an apply both need, read fresh from GitHub. ``problems``
+    names every check that makes ``--apply`` refuse (nothing is carried between runs)."""
+    info = read_repo(runner, org, repo)
+    problems = [
+        _REFUSAL_TEXT[r].format(status=info["status"]) for r in info["refusals"]
+    ]
+    found = {"info": info, "problems": problems, "bodies": None, "digest": None}
+    if "unreadable" in info["refusals"] or not info["default_branch"]:
+        return found
+    owner, name = info["owner"], info["name"]
+    try:
+        branches = branch_set(info["default_branch"], info["existing"])
+        bodies = plan_bodies(branches)
+    except ValueError as exc:
+        problems.append(f"branch not supported: {exc}")
+        return found
+    push = check_push(runner, owner, name, branches, now)
+    existing = read_existing(runner, owner, name, branches)
+    if push["result"] != "pass":
+        problems.append(f"push check is {push['result']}")
+    for branch, state in existing["protection"].items():
+        if state == "classic":
+            problems.append(f"classic branch protection on {branch}")
+        elif state == "unknown":
+            problems.append(f"branch protection state unknown on {branch}")
+    if existing["rulesets"] is None:
+        status = existing["rulesets_status"]
+        problems.append(f"ruleset list cannot be read (HTTP {status})")
+    elif PROTECTED_RULESET_IDS & set(existing["rulesets"].values()):
+        problems.append("repo lists a ruleset id this script never touches")
+    found.update(
+        branches=branches,
+        push=push,
+        existing=existing,
+        bodies=bodies,
+        digest=payload_digest(bodies),
+    )
+    return found
+
+
+def dry_run_report(runner: Runner, org: str, repo: str, now: datetime) -> list[str]:
+    """The lines a dry run prints. It makes no write."""
+    found = _assess(runner, org, repo, now)
+    info = found["info"]
+    lines = [
+        f"repo: {info['owner']}/{info['name']} (default branch: "
+        f"{info['default_branch'] or 'none'}, archived: "
+        f"{'yes' if info['archived'] else 'no'}, admin: "
+        f"{'yes' if info['admin'] else 'no'})"
+    ]
+    if found["bodies"] is None:
+        lines += [f"would refuse --apply: {p}" for p in found["problems"]]
+        return lines + ["no plan: the repo could not be planned"]
+    push, existing = found["push"], found["existing"]
+    lines.append(
+        f"push check, last {PUSH_WINDOW_DAYS} days since {push['cutoff']}: "
+        f"{push['result']}"
+    )
+    for branch, got in push["branches"].items():
+        note = f", {got['note']}" if got.get("note") else ""
+        lines.append(
+            f"  {branch}: {got['result']} (source {got['source']}, "
+            f"direct pushes {got['direct_pushes']}, examined {got['examined']}{note})"
+        )
+    names = existing["rulesets"]
+    lines.append(
+        "existing rulesets: "
+        + ("unknown" if names is None else ", ".join(sorted(names)) or "none")
+    )
+    lines.append(
+        "classic protection: "
+        + ", ".join(f"{b} {s}" for b, s in existing["protection"].items())
+    )
+    tags = existing["v_tags"]
+    lines.append(f"v* tags: {'unknown' if tags is None else tags}")
+    lines.append(
+        "WARNING: the tag ruleset blocks moving and deleting v* tags; check the "
+        "release workflows of this repo by hand before applying."
+    )
+    lines.append("would create, in this order:")
+    for number, body in enumerate(found["bodies"], 1):
+        present = names is not None and body["name"] in names
+        lines.append(
+            f"  {number}. {body['name']} ({body['target']})"
+            + (" - skipped, a ruleset of this name already exists" if present else "")
+        )
+    lines += [f"would refuse --apply: {p}" for p in found["problems"]]
+    lines.append(f"digest: {found['digest']}")
+    lines.append(
+        f"apply with: uv run python scripts/apply_org_rulesets.py --org {info['owner']}"
+        f" --repo {info['name']} --out <DIR> --apply --confirm {found['digest']}"
+    )
+    return lines
+
+
+def _before_state(runner, base, existing, digest, owner, name, now):
+    """The saved before state, or a refusal text. Every existing ruleset is read by id
+    (the list answer may hold summaries only); the branch protection of the set was
+    read just before and is ``none`` on every branch, or the run would have refused."""
+    rulesets = {}
+    for rid in sorted(existing["rulesets"].values()):
+        data = _json_object(runner.run(["gh", "api", f"{base}/rulesets/{rid}"]))
+        if data is None:
+            return None, f"before-state read failed for ruleset {rid}"
+        rulesets[str(rid)] = data
+    state = {
+        "org": owner,
+        "repo": name,
+        "saved_at": _iso(now),
+        "digest": digest,
+        "rulesets": rulesets,
+        "protection": dict.fromkeys(existing["protection"], "none"),
+    }
+    return state, None
+
+
+def _adopt(runner: Runner, base: str, ruleset_name: str) -> int | None:
+    """After a POST that timed out: the id of the ruleset of that name, if it exists."""
+    listed = runner.run(
+        ["gh", "api", "--paginate", f"{base}/rulesets?per_page={PER_PAGE}"]
+    )
+    try:
+        items, _ = _items(listed)
+        return next((i["id"] for i in items if i["name"] == ruleset_name), None)
+    except (ValueError, KeyError, TypeError):
+        return None
+
+
+def apply_repo(
+    runner: Runner,
+    org: str,
+    repo: str,
+    out_dir: str | Path | None,
+    confirm: str | None,
+    now: datetime,
+) -> dict:
+    """Create the rulesets of one repo, each read back before the next write.
+
+    Nothing is carried over from a dry run: every check is read again and ``confirm``
+    must equal the digest of the bodies rendered now. Any refusal makes no write call
+    and writes no file. Returns ``ok``, ``error``, ``refusals``, ``ids`` (name to id of
+    what was created or adopted), ``skipped``, ``comment`` (the line for issue 838,
+    never posted), ``rollback`` (manual DELETE commands) and ``before_file``.
+    """
+    result = {
+        "ok": False,
+        "error": None,
+        "refusals": [],
+        "ids": {},
+        "skipped": [],
+        "comment": None,
+        "rollback": [],
+        "before_file": None,
+    }
+
+    def stop(*messages: str) -> dict:
+        result["error"] = "; ".join(messages)
+        result["refusals"] = list(messages)
+        return result
+
+    if not out_dir:
+        return stop("no --out folder given")
+    found = _assess(runner, org, repo, now)
+    info, problems = found["info"], list(found["problems"])
+    if confirm != found["digest"]:
+        problems.append("confirm digest does not match the rulesets rendered now")
+    owner, name = info["owner"], info["name"]
+    before_file = Path(out_dir) / f"{name}-before.json"
+    if before_file.exists():
+        problems.append(f"before-state file already exists: {before_file}")
+    if problems:
+        return stop(*problems)
+
+    base = f"repos/{owner}/{name}"
+    existing = found["existing"]
+    state, problem = _before_state(
+        runner, base, existing, found["digest"], owner, name, now
+    )
+    if problem:
+        return stop(problem)
+    try:
+        before_file.parent.mkdir(parents=True, exist_ok=True)
+        with open(before_file, "x", encoding="utf-8") as handle:
+            json.dump(state, handle, indent=2, sort_keys=True)
+            handle.write("\n")
+    except FileExistsError:
+        return stop(f"before-state file already exists: {before_file}")
+    result["before_file"] = str(before_file)
+
+    def fail(message: str) -> dict:
+        result["error"] = message
+        result["rollback"] = rollback()
+        return result
+
+    def rollback() -> list[str]:
+        """Manual DELETE commands, newest first, for the ids this run created."""
+        return [
+            f"gh api --method DELETE {base}/rulesets/{rid}"
+            for rid in reversed(list(result["ids"].values()))
+        ]
+
+    post = ["gh", "api", "--method", "POST", f"{base}/rulesets", "--input", "-"]
+    for body in found["bodies"]:
+        rname = body["name"]
+        if rname in existing["rulesets"]:
+            result["skipped"].append(rname)
+            continue
+        posted = runner.run(post, json.dumps(body))
+        if posted == TIMED_OUT:
+            rid = _adopt(runner, base, rname)
+            if rid is None:
+                return fail(
+                    f"POST of {rname} timed out and no ruleset of that name found"
+                )
+        else:
+            data = _json_object(posted)
+            rid = data.get("id") if data else None
+            if not isinstance(rid, int):
+                status = http_status(posted)
+                return fail(f"POST of {rname} failed (HTTP {status})")
+        result["ids"][rname] = rid
+        remote = _json_object(runner.run(["gh", "api", f"{base}/rulesets/{rid}"]))
+        if remote is None:
+            return fail(f"read-back of {rname} (id {rid}) failed")
+        diffs = compare_bodies(body, remote)
+        if diffs:
+            return fail(f"read-back of {rname} (id {rid}) differs: " + "; ".join(diffs))
+    result["ok"] = True
+    ids = ", ".join(f"{n}={i}" for n, i in result["ids"].items()) or "none created"
+    result["comment"] = (
+        f"Applied rulesets to {owner}/{name} on {now.astimezone(timezone.utc):%Y-%m-%d}"
+        f": {ids}"
+    )
+    result["rollback"] = rollback()
+    return result
diff --git a/tests/org_rulesets/test_apply.py b/tests/org_rulesets/test_apply.py
new file mode 100644
index 000000000..4dc37ca15
--- /dev/null
+++ b/tests/org_rulesets/test_apply.py
@@ -0,0 +1,391 @@
+"""dry_run_report and apply_repo, against a fake GitHub (no live call)."""
+
+from __future__ import annotations
+
+import json
+from datetime import datetime, timezone
+
+import pytest
+
+NOW = datetime(2026, 11, 26, 17, 0, tzinfo=timezone.utc)
+REPO = "repos/acme/acme-one"
+LIST = f"{REPO}/rulesets?per_page=100"
+TAGS = f"{REPO}/git/matching-refs/tags/v?per_page=100"
+SERVER = {"source": "acme-one", "source_type": "Repository", "created_at": "2026"}
+TAG_RULESET = "protect-release-tags"
+PUSH = {"activity_type": "push", "timestamp": "2026-10-01T10:00:00Z"}
+
+
+def activity(branch):
+    return f"{REPO}/activity?ref=refs/heads/{branch}&time_period=quarter&per_page=100"
+
+
+@pytest.fixture
+def world(fake_runner_cls):
+    """A factory for a fake GitHub holding one repo: default branch ``master`` and an
+    ``integration`` branch, no direct pushes, no protection, no rulesets, two v* tags.
+    ``gets`` replaces or adds canned GET answers; ``post`` replaces the POST answer."""
+    ok, http = fake_runner_cls.ok, fake_runner_cls.http
+
+    def build(*, gets=None, post=None, **repo_changes):
+        store = {}
+
+        def default_post(argv, stdin):
+            number = 101 + len(store)
+            store[number] = json.loads(stdin)
+            return ok({"id": number})
+
+        def readback(number):
+            def reply(argv, stdin):
+                return ok({**store[number], "id": number, **SERVER})
+
+            return reply
+
+        repo = {
+            "owner": {"login": "acme"},
+            "name": "acme-one",
+            "archived": False,
+            "default_branch": "master",
+            "permissions": {"admin": True},
+            **repo_changes,
+        }
+        answers = {
+            REPO: ok(repo),
+            f"{REPO}/branches/master": ok({}),
+            f"{REPO}/branches/integration": ok({}),
+            activity("master"): ok([]),
+            activity("integration"): ok([]),
+            f"{REPO}/branches/master/protection": http(404),
+            f"{REPO}/branches/integration/protection": http(404),
+            LIST: ok([]),
+            TAGS: ok([{}, {}]),
+            **{f"{REPO}/rulesets/{n}": readback(n) for n in range(101, 104)},
+            **(gets or {}),
+        }
+        replies = {("GET", path): answer for path, answer in answers.items()}
+        replies[("POST", f"{REPO}/rulesets")] = post or default_post
+        runner = fake_runner_cls(replies)
+        runner.store = store
+        return runner
+
+    return build
+
+
+def digest_of(orr):
+    return orr.payload_digest(orr.plan_bodies(["master", "integration"]))
+
+
+def posts(runner, fake_runner_cls):
+    return [c for c in runner.commands if fake_runner_cls.method_of(c.argv) == "POST"]
+
+
+def apply(orr, runner, tmp_path, confirm=None):
+    confirm = confirm or digest_of(orr)
+    return orr.apply_repo(runner, "acme", "acme-one", tmp_path / "out", confirm, NOW)
+
+
+# --- the dry run -------------------------------------------------------------------
+
+
+def test_dry_run_prints_every_item_and_writes_nothing(world, orr, fake_runner_cls):
+    runner = world()
+    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
+    assert posts(runner, fake_runner_cls) == []
+    assert "acme/acme-one" in text and "default branch: master" in text
+    assert "push check" in text and ": pass" in text
+    assert "integration: pass (source activity, direct pushes 0" in text
+    assert "classic protection: integration none, master none" in text
+    assert "existing rulesets: none" in text
+    assert "v* tags: 2" in text
+    assert "blocks moving and deleting v* tags" in text and "by hand" in text
+    names = (TAG_RULESET, "protect-integration", "protect-master")
+    order = [text.index(n) for n in names]
+    assert order == sorted(order)
+    digest = digest_of(orr)
+    assert f"digest: {digest}" in text
+    assert f"--apply --confirm {digest}" in text
+    assert "--org acme --repo acme-one" in text
+    assert "would refuse" not in text
+
+
+def test_dry_run_with_a_read_only_runner_never_posts(world, orr, fake_runner_cls):
+    runner = world()
+    runner.read_only = True
+    assert orr.dry_run_report(runner, "acme", "acme-one", NOW)
+    assert posts(runner, fake_runner_cls) == []
+
+
+def test_dry_run_lists_a_same_name_ruleset_as_skipped_with_the_same_digest(
+    world, orr, fake_runner_cls
+):
+    summary = fake_runner_cls.ok([{"id": 7, "name": "protect-master"}])
+    runner = world(gets={LIST: summary})
+    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
+    assert "protect-master (branch) - skipped" in text
+    assert f"digest: {digest_of(orr)}" in text
+
+
+def test_dry_run_names_what_would_refuse(world, orr, fake_runner_cls):
+    pushed = fake_runner_cls.ok([PUSH])
+    runner = world(gets={activity("master"): pushed}, archived=True)
+    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
+    assert "would refuse --apply: repo is archived" in text
+    assert "would refuse --apply: push check is blocked" in text
+
+
+def test_dry_run_of_an_unreadable_repo(world, orr, fake_runner_cls):
+    runner = world(gets={REPO: fake_runner_cls.http(404)})
+    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
+    assert "repo cannot be read (HTTP 404)" in text and "no plan" in text
+
+
+# --- apply: refusals ---------------------------------------------------------------
+
+COMMITS = f"{REPO}/commits?sha=master&since=2026-08-28T17:00:00Z&per_page=100"
+
+# name -> (what to change in the fake GitHub, text the refusal must hold)
+REFUSALS = {
+    "wrong-confirm": ({}, "confirm digest does not match"),
+    "no-out": ({}, "no --out folder"),
+    "push-blocked": (
+        {"gets": {activity("integration"): ("ok", [PUSH])}},
+        "push check is blocked",
+    ),
+    "push-incomplete": (
+        {"gets": {activity("master"): ("http", 403), COMMITS: ("http", 403)}},
+        "push check is incomplete",
+    ),
+    "classic": (
+        {"gets": {f"{REPO}/branches/master/protection": ("ok", {})}},
+        "classic branch protection on master",
+    ),
+    "archived": ({"archived": True}, "repo is archived"),
+    "no-admin": ({"permissions": {"admin": False}}, "no admin permission"),
+    "protected-id": (
+        {"gets": {LIST: ("ok", [{"id": 28081842, "name": "x"}])}},
+        "ruleset id this script never touches",
+    ),
+    "rulesets-unreadable": (
+        {"gets": {LIST: ("http", 403)}},
+        "ruleset list cannot be read (HTTP 403)",
+    ),
+}
+
+
+@pytest.mark.parametrize("name", sorted(REFUSALS))
+def test_a_refusal_writes_nothing_and_names_the_check(
+    world, orr, fake_runner_cls, tmp_path, name
+):
+    changes, text = REFUSALS[name]
+    gets = {
+        path: getattr(fake_runner_cls, kind)(value)
+        for path, (kind, value) in changes.get("gets", {}).items()
+    }
+    options = {k: v for k, v in changes.items() if k != "gets"}
+    runner = world(gets=gets, **options)
+    confirm = "0" * 64 if name == "wrong-confirm" else digest_of(orr)
+    out_dir = None if name == "no-out" else tmp_path / "out"
+    got = orr.apply_repo(runner, "acme", "acme-one", out_dir, confirm, NOW)
+    assert got["ok"] is False and text in got["error"]
+    assert posts(runner, fake_runner_cls) == []
+    assert list(tmp_path.iterdir()) == []
+    assert got["ids"] == {} and got["comment"] is None and got["before_file"] is None
+    # nothing was read by id either: no call names a ruleset id
+    assert not any("/rulesets/" in c.argv[-1] for c in runner.commands)
+
+
+# --- apply: the write loop -----------------------------------------------------------
+
+
+def test_the_write_order_and_the_read_back_after_each_write(
+    world, orr, fake_runner_cls, tmp_path
+):
+    runner = world()
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is True and got["error"] is None
+    assert got["ids"] == {
+        TAG_RULESET: 101,
+        "protect-integration": 102,
+        "protect-master": 103,
+    }
+    steps = []
+    for record in runner.commands:
+        if fake_runner_cls.method_of(record.argv) == "POST":
+            steps.append(f"POST {record.stdin_name}")
+        elif "/rulesets/" in record.argv[-1]:
+            steps.append("GET " + record.argv[-1].rsplit("/", 1)[1])
+    assert steps == [
+        f"POST {TAG_RULESET}",
+        "GET 101",
+        "POST protect-integration",
+        "GET 102",
+        "POST protect-master",
+        "GET 103",
+    ]
+
+
+def test_the_comment_and_the_rollback_commands_hold_the_ids(world, orr, tmp_path):
+    got = apply(orr, world(), tmp_path)
+    for name, number in got["ids"].items():
+        assert f"{name}={number}" in got["comment"]
+    assert "acme/acme-one" in got["comment"] and "2026-11-26" in got["comment"]
+    assert got["rollback"] == [
+        f"gh api --method DELETE {REPO}/rulesets/{n}" for n in (103, 102, 101)
+    ]
+
+
+def test_the_before_file_holds_complete_bodies_and_is_written_once(
+    world, orr, fake_runner_cls, tmp_path
+):
+    ok = fake_runner_cls.ok
+    full = {
+        "id": 7,
+        "name": "other",
+        "target": "branch",
+        "rules": [{"type": "deletion"}],
+        "bypass_actors": [],
+    }
+    gets = {LIST: ok([{"id": 7, "name": "other"}]), f"{REPO}/rulesets/7": ok(full)}
+    runner = world(gets=gets)
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is True
+    path = tmp_path / "out" / "acme-one-before.json"
+    saved = json.loads(path.read_text(encoding="utf-8"))
+    assert saved["rulesets"] == {"7": full}
+    assert saved["protection"] == {"integration": "none", "master": "none"}
+    assert saved["digest"] == digest_of(orr) and saved["repo"] == "acme-one"
+    assert got["before_file"] == str(path)
+    # a second run for the same repo and folder refuses before any write
+    count = len(posts(runner, fake_runner_cls))
+    again = apply(orr, runner, tmp_path)
+    assert again["ok"] is False and "already exists" in again["error"]
+    assert len(posts(runner, fake_runner_cls)) == count
+    assert json.loads(path.read_text(encoding="utf-8")) == saved
+
+
+def test_a_failed_before_state_read_writes_nothing(
+    world, orr, fake_runner_cls, tmp_path
+):
+    f = fake_runner_cls
+    gets = {LIST: f.ok([{"id": 7, "name": "other"}]), f"{REPO}/rulesets/7": f.http(403)}
+    runner = world(gets=gets)
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is False
+    assert "before-state read failed for ruleset 7" in got["error"]
+    assert posts(runner, f) == [] and list(tmp_path.iterdir()) == []
+
+
+def test_a_read_back_mismatch_stops_after_the_first_ruleset(
+    world, orr, fake_runner_cls, tmp_path
+):
+    def changed(argv, stdin):
+        posted = json.loads(runner.executed[-2][1])
+        return fake_runner_cls.ok({**posted, "enforcement": "disabled"})
+
+    runner = world(gets={f"{REPO}/rulesets/101": changed})
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is False and "differs" in got["error"]
+    assert "enforcement" in got["error"]
+    assert got["ids"] == {TAG_RULESET: 101}
+    assert len(posts(runner, fake_runner_cls)) == 1
+    assert got["rollback"] == [f"gh api --method DELETE {REPO}/rulesets/101"]
+    assert got["comment"] is None
+
+
+def test_a_failed_read_back_stops_the_run(world, orr, fake_runner_cls, tmp_path):
+    runner = world(gets={f"{REPO}/rulesets/101": fake_runner_cls.http(500)})
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is False and "read-back" in got["error"]
+    assert got["ids"] == {TAG_RULESET: 101}
+    assert len(posts(runner, fake_runner_cls)) == 1
+
+
+def test_a_failed_post_stops_the_run(world, orr, fake_runner_cls, tmp_path):
+    runner = world(post=fake_runner_cls.http(422))
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is False
+    assert "POST of protect-release-tags failed" in got["error"]
+    assert got["ids"] == {} and got["rollback"] == []
+    assert len(posts(runner, fake_runner_cls)) == 1
+    assert (tmp_path / "out" / "acme-one-before.json").exists()
+
+
+def test_a_post_without_an_id_stops_the_run(world, orr, fake_runner_cls, tmp_path):
+    runner = world(post=fake_runner_cls.ok({"message": "no id"}))
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is False and got["ids"] == {}
+
+
+def timed_out_world(world, orr, fake_runner_cls, listed):
+    """The first POST times out; the list that follows answers ``listed``."""
+    ok = fake_runner_cls.ok
+    tag_body = {**orr.render_tags(), "id": 55, **SERVER}
+    runner = world(gets={LIST: [ok([]), listed], f"{REPO}/rulesets/55": ok(tag_body)})
+    store = runner.store
+
+    def post(argv, stdin):
+        number = 101 + len(store)
+        store[number] = json.loads(stdin)
+        return ok({"id": number})
+
+    runner.replies[("POST", f"{REPO}/rulesets")] = [orr.TIMED_OUT, post, post]
+    return runner
+
+
+def test_a_timed_out_post_is_followed_by_a_list_and_adopts_the_ruleset(
+    world, orr, fake_runner_cls, tmp_path
+):
+    listed = fake_runner_cls.ok([{"id": 55, "name": TAG_RULESET}])
+    runner = timed_out_world(world, orr, fake_runner_cls, listed)
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is True
+    assert got["ids"][TAG_RULESET] == 55
+    kinds = [fake_runner_cls.method_of(c.argv) for c in runner.commands]
+    after = runner.commands[kinds.index("POST") + 1]
+    assert after.argv[-1] == LIST and "--paginate" in after.argv
+    # the timed-out POST is never repeated: one POST per ruleset
+    assert [c.stdin_name for c in posts(runner, fake_runner_cls)] == [
+        TAG_RULESET,
+        "protect-integration",
+        "protect-master",
+    ]
+    assert f"gh api --method DELETE {REPO}/rulesets/55" in got["rollback"]
+
+
+def test_a_timed_out_post_with_nothing_found_stops(
+    world, orr, fake_runner_cls, tmp_path
+):
+    listed = fake_runner_cls.ok([])
+    runner = timed_out_world(world, orr, fake_runner_cls, listed)
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is False and "timed out" in got["error"]
+    assert len(posts(runner, fake_runner_cls)) == 1 and got["ids"] == {}
+
+
+def test_a_same_name_ruleset_gets_no_write_of_any_kind(
+    world, orr, fake_runner_cls, tmp_path
+):
+    ok = fake_runner_cls.ok
+    full = {"id": 7, "name": "protect-master", "target": "branch", "rules": []}
+    summary = ok([{"id": 7, "name": "protect-master"}])
+    runner = world(gets={LIST: summary, f"{REPO}/rulesets/7": ok(full)})
+    got = apply(orr, runner, tmp_path)
+    assert got["ok"] is True and got["skipped"] == ["protect-master"]
+    assert "protect-master" not in got["ids"]
+    assert [c.stdin_name for c in posts(runner, fake_runner_cls)] == [
+        TAG_RULESET,
+        "protect-integration",
+    ]
+    methods = {fake_runner_cls.method_of(c.argv) for c in runner.commands}
+    assert methods == {"GET", "POST"}
+    saved = json.loads((tmp_path / "out" / "acme-one-before.json").read_text())
+    assert saved["rulesets"] == {"7": full}
+
+
+def test_no_call_names_a_protected_ruleset_id(world, orr, tmp_path):
+    runner = world()
+    apply(orr, runner, tmp_path)
+    assert orr.PROTECTED_RULESET_IDS == {28081842, 28081844, 28081845}
+    for record in runner.commands:
+        text = " ".join(record.argv)
+        assert not any(str(i) in text for i in orr.PROTECTED_RULESET_IDS)

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
