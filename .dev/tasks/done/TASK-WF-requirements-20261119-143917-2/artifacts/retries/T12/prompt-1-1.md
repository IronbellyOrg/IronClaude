5d0ad2bf80ec319f84ba3083693c35b258bbbf76
Review one task for spec compliance.

Task brief: ## Task 12: Write the result comment and move the Status to In review

Depends on: Task 3, Task 6, Task 7

Create `src/superclaude/cli/issue_pipeline/complete.py` (requirement R24). A function takes the repo, the issue number, the configured Project node id `project_id` (validated against `^PVT_[A-Za-z0-9_-]+$`), the approval event id of the run, an outcome word (`succeeded`, `failed`, `blocked` or `partial`), a pointer to the result summary file and a Runner from `src/superclaude/cli/issue_watch/runner.py`. For `succeeded`, before any write (the comment included) it reads the issue's Project items and selects the one non-archived item of that Project with the helper Task 7 adds next to `project_check`; zero items gives `refused:project_missing`, more than one `refused:project_ambiguous`, and a Status field without an `In review` option `refused:status_option_missing`. It posts one result comment through `gh api --method POST repos/<owner>/<name>/issues/<N>/comments` carrying the marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->`, which never contains the claim marker (`predicates.py` line 14); it posts no second comment only when an exact marker written by its own login is present. For `succeeded` only it then sets the Status with the GraphQL mutation `updateProjectV2ItemFieldValue`, and only when the item's current Status is one of the allowed Statuses that Task 1 names as one module constant (imported, not copied); any other current Status (for example a person moved it to Done) posts the comment and returns `status_moved_by_person` without a mutation. A second call still retries the Status move when the first call's move failed. The end Status comes from one named table keyed by the allowed Status (all four map to `In review`), so an exception is a one-line change. A failed, blocked or partial outcome posts the comment and does not move the Status. Result words are closed and no issue or comment text is echoed. The read-then-write is not atomic, so a person's move inside that window can still be overwritten; the module docstring says so. The module lives outside `github.py`, which stays read-only.

Acceptance criteria:
- T12.AC1: New `tests/issue_pipeline/test_complete.py` uses the fake runner and covers: succeeded posts one comment and one Status mutation to the `In review` option on the configured Project's item; failed, blocked and partial post a comment and no mutation; an issue on two Projects uses the configured `projectId` and its item id; zero items and two live items in the Project are refused with no write; an item already at Done gets the comment and no mutation (`status_moved_by_person`); a second call with the same run id and own-login marker posts no comment; another run id does not suppress it; a marker posted by another login does not suppress it; a failed first move is retried on the second call; an unknown outcome word, a bad issue number, a bad project id and a bad repo are refused before any call; a failed mutation reports a closed failure word and leaves the comment in place; the marker does not contain the claim marker.
- T12.AC2: One test shows the coordinator's own comment leaves `unchanged_since` clean (comments by the watcher's own login are skipped).
- T12.AC3: `tests/issue_watch/test_security_invariants.py` is updated so its NG-2 scope and header (line 10) read `github.py` and the cycle, name `complete.py` and `repo_init.py` as the only allowed writers, and the argv scan (lines 712 to 730) also covers the read calls of the new modules; the test still proves `github.py` has no mutation.
- T12.AC4: `tests/issue_watch/test_module_boundaries.py` passes with the new module, and `uv run pytest tests/issue_pipeline tests/issue_watch -q` passes.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- This plan applies requirement R35 (owner decision of 2026-11-19): the approval is no longer the label `issue-watch:approved`. It is the organization issue field `Approved` (single select, one option `Yes`, field id 50144115 on `IronbellyOrg`) set to `Yes` by an allowed approver (IronBelly, Clay or a maintainer, the approvers file of today). The trigger label `issue-watch:trigger` stays. Who set the field and when comes from the issue's GraphQL timeline events `IssueFieldAddedEvent`, `IssueFieldChangedEvent` and `IssueFieldRemovedEvent` (each carries `actor`, `createdAt`, `issueField` and the value; verified read-only on 2026-11-19 against issue 675 with another field), because the REST events endpoint names the event but not the field or the value. Task 4a builds the read; the approval predicates, the approval-void rule and the claim-time refusal keep their logic and see the field events as label events named by `approval_label`. A real label with the old name never approves. Task 4 is amended to observe the field instead of the label; the plan was copied from `TASK-WF-requirements-20261119-143917` (Tasks 1 to 3 complete there) and edited by owner instruction, and `source.md` still carries the label wording of the requirements file (Task 28 updates the requirements file).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval (the `Approved` issue field set to Yes, R35), the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the `Approved` field after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 4a, 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 4a, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 4a, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: 5d0ad2bf80ec319f84ba3083693c35b258bbbf76
Diff against the start snapshot: diff --git a/tests/issue_watch/test_security_invariants.py b/tests/issue_watch/test_security_invariants.py
index 550a540a7..557c204e3 100644
--- a/tests/issue_watch/test_security_invariants.py
+++ b/tests/issue_watch/test_security_invariants.py
@@ -9,7 +9,10 @@ These tests pin the controls of design section 9.1 that cut across modules:
 - T5, T9, NFR-002, NFR-003, AC-20: every argv the runner sees is one of the
   allowed forms, never names the upstream repository, ``{owner}``, a title or a
   body, and every REST path call carries ``--method GET`` (DF-28).
-- NG-2: nothing writes to GitHub (no ``mutation``, no POST to a REST path).
+- NG-2: ``github.py`` and the cycle write nothing to GitHub (no ``mutation``, no POST
+  to a REST path). ``issue_pipeline/complete.py`` (the coordinator's result comment and
+  Status move) and ``issue_watch/repo_init.py`` (labels) are the only modules allowed to
+  write; a scan of both packages below keeps it that way.
 - T10: the launch argv is the 12-element list of FR-013 with no extra flag.
 
 No test sleeps, and none touches a real ``gh``, ``git`` or Orca: every cycle runs
@@ -1039,3 +1042,49 @@ def test_dispatch_json_entries_keep_their_keys_with_the_pipeline_none_prompt(tmp
     assert ran.prompts == ["/sc:issue --claim 9 --pipeline none --stage research"]
     raw = json.loads((ran.store.state_dir / "dispatch.json").read_text("utf-8"))
     assert set(raw["entries"]["9"]) == _DISPATCH_ENTRY_KEYS
+
+
+# ==============================================================================
+# NG-2 widened (plan Task 12): the only writers are complete.py and repo_init.py
+# ==============================================================================
+
+_WRITER_MODULES = {"complete.py", "repo_init.py"}
+_SRC = Path(__file__).resolve().parents[2] / "src/superclaude/cli"
+_WRITE_SIGN = re.compile(r'"POST"|"PUT"|"PATCH"|"DELETE"|\bmutation\s*[({]')
+
+
+def test_only_complete_and_repo_init_may_write_to_github():
+    scanned = sorted(
+        [*(_SRC / "issue_watch").glob("*.py"), *(_SRC / "issue_pipeline").glob("*.py")]
+    )
+    assert {p.name for p in scanned} >= {"github.py", "cycle.py", "complete.py"}
+    writers = {p.name for p in scanned if _WRITE_SIGN.search(p.read_text("utf-8"))}
+    assert writers <= _WRITER_MODULES, writers
+    assert "complete.py" in writers  # the scan is not vacuous
+    # github.py and the cycle stay read-only
+    for name in ("github.py", "cycle.py"):
+        assert name not in writers
+
+
+def test_the_read_calls_of_complete_py_are_get_or_read_only_graphql():
+    from tests.issue_pipeline.test_complete import World, call
+
+    world = World()
+    assert call(world) == "completed"
+    reads = [
+        a
+        for a in world.argvs
+        if "POST" not in a and not any(x.startswith("query=mutation") for x in a)
+    ]
+    assert len(reads) == 3  # own login, the Project items, the comments
+    for argv in reads:
+        assert not any(UPSTREAM.lower() in a.lower() for a in argv), argv
+        assert not any("{owner}" in a for a in argv), argv
+        if argv[:3] == ["gh", "api", "graphql"]:
+            query = next(a for a in argv if a.startswith("query="))
+            assert query.startswith("query=query(") and "mutation" not in query.lower()
+        elif argv[:3] != ["gh", "api", "user"]:
+            assert argv[2:4] == ["--method", "GET"], argv
+        assert not _TEXT_FIELD.search(
+            " ".join(a for a in argv if a.startswith("query="))
+        ), argv
diff --git a/src/superclaude/cli/issue_pipeline/complete.py b/src/superclaude/cli/issue_pipeline/complete.py
new file mode 100644
index 000000000..82b199cd4
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/complete.py
@@ -0,0 +1,424 @@
+"""Post the result comment of a run and move the issue's Project Status (plan Task 12, R24).
+
+Only the coordinator calls this, under the issue's grant row (``WORKER-CONTRACT.md``,
+"Issue pipeline duties"). A launched agent and every worker report through their result file
+and never call it. This module and ``issue_watch/repo_init.py`` are the only code that writes
+to GitHub; ``issue_watch/github.py`` stays read-only (security invariant NG-2).
+
+One call does, in order:
+
+1. validates every input and refuses with a closed word before any ``gh`` call;
+2. for ``succeeded`` only, reads the issue's Project items and selects the one non-archived item
+   of the configured Project (zero items, several items, or a Status field with no end option
+   refuse before any write, the comment included);
+3. posts one result comment carrying the per-run marker ``<!-- sc:issue:result issue=<N>
+   run=<approval event id> -->``, unless a comment written by the runner's own login already
+   holds that exact marker (a second call for the same run posts nothing new);
+4. for ``succeeded`` only, sets the Status to the end Status of the item's current Status, and
+   only when that current Status is one of ``ALLOWED_STATUSES``; any other current Status
+   (a person moved it, say to Done) leaves the Status alone and returns
+   ``status_moved_by_person``.
+
+A failed, blocked or partial outcome posts the comment and never moves the Status. Every result
+is a closed word; no issue or comment text is echoed, and the comment holds only the outcome
+word, validated artifact paths and a pull request number.
+
+Known limit (shortcut: read then write, upgrade only if a person's move inside that window
+ever matters): the Status read and the Status write are two calls, not one atomic step, so a
+person's move between them can still be overwritten.
+"""
+
+from __future__ import annotations
+
+import json
+import re
+from dataclasses import dataclass
+from pathlib import Path
+
+from superclaude.cli.issue_watch.predicates import (
+    ALLOWED_STATUSES,
+    CLAIM_MARKER,
+    ProjectItem,
+    live_item,
+    valid_issue_number,
+)
+from superclaude.cli.issue_watch.runner import CommandResult, Runner
+
+TIMEOUT_S = 60.0
+PAGE_SIZE = 100
+PAGE_CAP = 5
+
+OUTCOMES = ("succeeded", "failed", "blocked", "partial")
+
+# The end Status of each allowed Status (owner decision of 2026-11-19: all four pipelines end
+# at In review). An exception is a one-line change here.
+END_STATUS: dict[str, str] = {
+    "Research": "In review",
+    "Spec": "In review",
+    "Plan": "In review",
+    "Debug": "In review",
+}
+
+# Closed result words.
+COMPLETED = (
+    "completed"  # succeeded: comment in place and the Status is at its end value
+)
+COMMENTED = (
+    "commented"  # failed, blocked or partial: comment in place, Status untouched
+)
+STATUS_MOVED_BY_PERSON = "status_moved_by_person"
+RESULT_WORDS = frozenset(
+    {
+        COMPLETED,
+        COMMENTED,
+        STATUS_MOVED_BY_PERSON,
+        "refused:bad_outcome",
+        "refused:bad_issue",
+        "refused:bad_project_id",
+        "refused:bad_repo",
+        "refused:bad_run",
+        "refused:bad_summary",
+        "refused:project_missing",
+        "refused:project_ambiguous",
+        "refused:status_option_missing",
+        "failed:project_read",
+        "failed:own_login",
+        "failed:comments_read",
+        "failed:comment_post",
+        "failed:status_move",
+    }
+)
+
+_REPO = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
+_PROJECT_ID = re.compile(r"PVT_[A-Za-z0-9_-]+")
+_NODE_ID = re.compile(r"[A-Za-z0-9_=-]{1,200}")
+_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
+_PATH = re.compile(r"[A-Za-z0-9._][A-Za-z0-9._/-]{0,199}")
+_PULL_REQUEST = re.compile(r"[1-9][0-9]{0,8}")
+MAX_ARTIFACTS = 20
+
+ITEMS_QUERY = """query($owner: String!, $name: String!, $number: Int!, $after: String) {
+  repository(owner: $owner, name: $name) {
+    issue(number: $number) {
+      projectItems(first: 100, after: $after) {
+        nodes {
+          id
+          isArchived
+          project {
+            id
+            field(name: "Status") {
+              ... on ProjectV2SingleSelectField { id options { id name } }
+            }
+          }
+          status: fieldValueByName(name: "Status") {
+            ... on ProjectV2ItemFieldSingleSelectValue { name }
+          }
+        }
+        pageInfo { hasNextPage endCursor }
+      }
+    }
+  }
+}"""
+
+MOVE_MUTATION = """mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
+  updateProjectV2ItemFieldValue(input: {projectId: $projectId, itemId: $itemId, fieldId: $fieldId, value: {singleSelectOptionId: $optionId}}) {
+    projectV2Item { id }
+  }
+}"""
+
+
+def result_marker(issue: int, run_id: int) -> str:
+    """The per-run marker; it never contains the claim marker."""
+    return f"<!-- sc:issue:result issue={issue} run={run_id} -->"
+
+
+@dataclass(frozen=True)
+class _Summary:
+    artifacts: tuple[str, ...]
+    pull_request: str | None
+
+
+def _read_summary(path: object) -> _Summary | None:
+    """Read the closed three-line result file; None when it is absent or malformed."""
+    if path is None:
+        return _Summary((), None)
+    try:
+        lines = Path(str(path)).read_text(encoding="utf-8").splitlines()
+    except (OSError, UnicodeDecodeError):
+        return None
+    keys = [line.partition(":")[0] for line in lines]
+    if keys != ["outcome", "artifacts", "pull_request"]:
+        return None
+    artifacts_text = lines[1].partition(":")[2].strip()
+    artifacts = (
+        tuple(a.strip() for a in artifacts_text.split(",")) if artifacts_text else ()
+    )
+    if len(artifacts) > MAX_ARTIFACTS or not all(
+        _PATH.fullmatch(a) and ".." not in a for a in artifacts
+    ):
+        return None
+    pr = lines[2].partition(":")[2].strip()
+    if pr == "none":
+        return _Summary(artifacts, None)
+    if _PULL_REQUEST.fullmatch(pr):
+        return _Summary(artifacts, pr)
+    return None
+
+
+def _comment_body(marker: str, outcome: str, summary: _Summary) -> str:
+    artifacts = ", ".join(summary.artifacts) if summary.artifacts else "none"
+    pr = f"#{summary.pull_request}" if summary.pull_request else "none"
+    return (
+        f"{marker}\nResult of the run: {outcome}\n"
+        f"Artifacts: {artifacts}\nPull request: {pr}"
+    )
+
+
+def _validate(
+    repo: object, issue: object, project_id: object, run_id: object, outcome: object
+) -> str | None:
+    if outcome not in OUTCOMES:
+        return "refused:bad_outcome"
+    if not valid_issue_number(issue):
+        return "refused:bad_issue"
+    if not isinstance(project_id, str) or not _PROJECT_ID.fullmatch(project_id):
+        return "refused:bad_project_id"
+    if not isinstance(repo, str) or not _REPO.fullmatch(repo):
+        return "refused:bad_repo"
+    if type(run_id) is not int or not 0 < run_id < 10**18:
+        return "refused:bad_run"
+    return None
+
+
+def _run(runner: Runner, argv: list[str]) -> CommandResult | None:
+    result = runner.run(argv, TIMEOUT_S)
+    if result.returncode != 0 or result.timed_out or result.spawn_error is not None:
+        return None
+    return result
+
+
+def _json(result: CommandResult | None) -> object | None:
+    if result is None:
+        return None
+    try:
+        parsed = json.loads(result.stdout)
+    except ValueError:
+        return None
+    if isinstance(parsed, dict) and parsed.get("errors"):
+        return None
+    return parsed
+
+
+@dataclass(frozen=True)
+class _Target:
+    item_id: str
+    field_id: str
+    current: str | None
+    options: dict[str, str]
+
+
+def _items(runner: Runner, owner: str, name: str, issue: int) -> list[dict] | None:
+    nodes: list[dict] = []
+    after: str | None = None
+    for _ in range(PAGE_CAP):
+        argv = [
+            "gh",
+            "api",
+            "graphql",
+            "-f",
+            f"query={ITEMS_QUERY}",
+            "-f",
+            f"owner={owner}",
+            "-f",
+            f"name={name}",
+            "-F",
+            f"number={issue}",
+        ]
+        if after is not None:
+            argv += ["-f", f"after={after}"]
+        data = _json(_run(runner, argv))
+        try:
+            page = data["data"]["repository"]["issue"]["projectItems"]  # type: ignore[index]
+            nodes += [n for n in page["nodes"] if isinstance(n, dict)]
+            info = page["pageInfo"]
+            if not info["hasNextPage"]:
+                return nodes
+            after = info["endCursor"]
+        except (KeyError, TypeError):
+            return None
+        if not isinstance(after, str) or not re.fullmatch(
+            r"[A-Za-z0-9+/=_.:-]{1,256}", after
+        ):
+            return None
+    return None  # more pages than the cap: unknown, so no write
+
+
+def _select(
+    nodes: list[dict], project_id: str, end_statuses: set[str]
+) -> _Target | str:
+    pairs: list[tuple[ProjectItem, dict]] = []
+    for node in nodes:
+        project = node.get("project") or {}
+        status = node.get("status") or {}
+        pairs.append(
+            (
+                ProjectItem(
+                    bool(node.get("isArchived")),
+                    str(project.get("id")),
+                    status.get("name") if isinstance(status.get("name"), str) else None,
+                ),
+                node,
+            )
+        )
+    matching = [p for p, _ in pairs if not p.is_archived and p.project_id == project_id]
+    if not matching:
+        return "refused:project_missing"
+    if len(matching) > 1:
+        return "refused:project_ambiguous"
+    item = live_item([p for p, _ in pairs], project_id)
+    node = next(n for p, n in pairs if p is item)
+    field = (node.get("project") or {}).get("field") or {}
+    options = {
+        o["name"]: o["id"]
+        for o in field.get("options") or []
+        if isinstance(o, dict)
+        and isinstance(o.get("name"), str)
+        and isinstance(o.get("id"), str)
+        and _NODE_ID.fullmatch(o["id"])
+    }
+    item_id, field_id = node.get("id"), field.get("id")
+    if (
+        not isinstance(item_id, str)
+        or not _NODE_ID.fullmatch(item_id)
+        or not isinstance(field_id, str)
+        or not _NODE_ID.fullmatch(field_id)
+        or not end_statuses <= set(options)
+    ):
+        return "refused:status_option_missing"
+    assert item is not None
+    return _Target(item_id, field_id, item.status_name, options)
+
+
+def _own_login(runner: Runner) -> str | None:
+    result = _run(runner, ["gh", "api", "user", "--jq", ".login"])
+    login = result.stdout.strip() if result is not None else ""
+    return login if _LOGIN.fullmatch(login) else None
+
+
+def _marker_present(
+    runner: Runner, owner: str, name: str, issue: int, marker: str, login: str
+) -> bool | None:
+    jq = (
+        "[.[] | {login: .user.login, "
+        f"marker: (.body | contains({json.dumps(marker)}))}}]"
+    )
+    for page in range(1, PAGE_CAP + 1):
+        argv = [
+            "gh",
+            "api",
+            "--method",
+            "GET",
+            f"repos/{owner}/{name}/issues/{issue}/comments",
+            "-F",
+            f"per_page={PAGE_SIZE}",
+            "-F",
+            f"page={page}",
+            "--jq",
+            jq,
+        ]
+        rows = _json(_run(runner, argv))
+        if not isinstance(rows, list):
+            return None
+        if any(
+            isinstance(r, dict) and r.get("marker") is True and r.get("login") == login
+            for r in rows
+        ):
+            return True
+        if len(rows) < PAGE_SIZE:
+            return False
+    return None  # a full last page: the answer is unknown, so no new comment
+
+
+def complete(
+    repo: object,
+    issue: object,
+    project_id: object,
+    run_id: object,
+    outcome: object,
+    summary_path: object,
+    runner: Runner,
+) -> str:
+    """Post the run's result comment and, for ``succeeded``, move the Status; return a closed word."""
+    refused = _validate(repo, issue, project_id, run_id, outcome)
+    if refused is not None:
+        return refused
+    assert isinstance(repo, str) and isinstance(issue, int)
+    assert isinstance(project_id, str) and isinstance(run_id, int)
+    summary = _read_summary(summary_path)
+    if summary is None:
+        return "refused:bad_summary"
+    owner, name = repo.split("/")
+    marker = result_marker(issue, run_id)
+    assert CLAIM_MARKER not in marker
+
+    target: _Target | None = None
+    if outcome == "succeeded":
+        nodes = _items(runner, owner, name, issue)
+        if nodes is None:
+            return "failed:project_read"
+        picked = _select(nodes, project_id, set(END_STATUS.values()))
+        if isinstance(picked, str):
+            return picked
+        target = picked
+
+    login = _own_login(runner)
+    if login is None:
+        return "failed:own_login"
+    present = _marker_present(runner, owner, name, issue, marker, login)
+    if present is None:
+        return "failed:comments_read"
+    if not present:
+        body = _comment_body(marker, str(outcome), summary)
+        posted = _run(
+            runner,
+            [
+                "gh",
+                "api",
+                "--method",
+                "POST",
+                f"repos/{owner}/{name}/issues/{issue}/comments",
+                "-f",
+                f"body={body}",
+            ],
+        )
+        if posted is None:
+            return "failed:comment_post"
+    if target is None:
+        return COMMENTED
+
+    current = target.current
+    if current in END_STATUS.values():
+        return COMPLETED  # an earlier call already moved it
+    if current not in ALLOWED_STATUSES:
+        return STATUS_MOVED_BY_PERSON
+    move = _json(
+        _run(
+            runner,
+            [
+                "gh",
+                "api",
+                "graphql",
+                "-f",
+                f"query={MOVE_MUTATION}",
+                "-f",
+                f"projectId={project_id}",
+                "-f",
+                f"itemId={target.item_id}",
+                "-f",
+                f"fieldId={target.field_id}",
+                "-f",
+                f"optionId={target.options[END_STATUS[current]]}",
+            ],
+        )
+    )
+    return COMPLETED if move is not None else "failed:status_move"
diff --git a/tests/issue_pipeline/test_complete.py b/tests/issue_pipeline/test_complete.py
new file mode 100644
index 000000000..a52e192c8
--- /dev/null
+++ b/tests/issue_pipeline/test_complete.py
@@ -0,0 +1,418 @@
+"""Task 12: the result comment and the Status move (``complete.py``), over a fake runner."""
+
+from __future__ import annotations
+
+import json
+import re
+from datetime import datetime, timezone
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_pipeline import complete
+from superclaude.cli.issue_watch import predicates
+from superclaude.cli.issue_watch.runner import CommandResult
+
+REPO = "IronbellyOrg/IronClaude"
+ISSUE = 9
+PROJECT = "PVT_cfg"
+OTHER_PROJECT = "PVT_other"
+RUN = 4242
+OWN = "coord-login"
+IN_REVIEW_ID = "opt-in-review"
+OPTIONS = [
+    {"id": "opt-research", "name": "Research"},
+    {"id": "opt-done", "name": "Done"},
+    {"id": IN_REVIEW_ID, "name": "In review"},
+]
+CANARY = "CANARY-12-NO-ECHO"
+
+
+def node(
+    item_id: str = "PVTI_cfg",
+    project: str = PROJECT,
+    status: str | None = "Plan",
+    *,
+    archived: bool = False,
+    options: list[dict] | None = None,
+) -> dict:
+    return {
+        "id": item_id,
+        "isArchived": archived,
+        "project": {
+            "id": project,
+            "field": {
+                "id": "PVTSSF_status",
+                "options": OPTIONS if options is None else options,
+            },
+        },
+        "status": {"name": status} if status is not None else None,
+    }
+
+
+def ok(stdout: str = "") -> CommandResult:
+    return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)
+
+
+def bad() -> CommandResult:
+    return CommandResult(("gh",), 1, "", "boom", False, None, 0.0)
+
+
+class World:
+    """A scripted ``gh`` for one issue: its Project items, comments and the writes made."""
+
+    def __init__(self, *nodes: dict) -> None:
+        self.nodes = list(nodes) if nodes else [node()]
+        self.comments: list[dict] = []  # {login, body}
+        self.argvs: list[list[str]] = []
+        self.posts: list[str] = []
+        self.mutations: list[list[str]] = []
+        self.fail_move = False
+        self.fail_post = False
+
+    def other_comment(self, login: str, body: str) -> None:
+        self.comments.append({"login": login, "body": body})
+
+    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
+        self.argvs.append(list(argv))
+        if argv[:3] == ["gh", "api", "user"]:
+            return ok(OWN + "\n")
+        if argv[:3] == ["gh", "api", "graphql"]:
+            query = next(a for a in argv if a.startswith("query="))
+            if "mutation" in query:
+                self.mutations.append(list(argv))
+                return bad() if self.fail_move else ok('{"data": {}}')
+            return ok(
+                json.dumps(
+                    {
+                        "data": {
+                            "repository": {
+                                "issue": {
+                                    "projectItems": {
+                                        "nodes": self.nodes,
+                                        "pageInfo": {
+                                            "hasNextPage": False,
+                                            "endCursor": None,
+                                        },
+                                    }
+                                }
+                            }
+                        }
+                    }
+                )
+            )
+        if "POST" in argv:
+            assert argv[argv.index("POST") - 1] == "--method"
+            if self.fail_post:
+                return bad()
+            body = next(a for a in argv if a.startswith("body="))[len("body=") :]
+            self.posts.append(body)
+            self.comments.append({"login": OWN, "body": body})
+            return ok("{}")
+        assert argv[2:4] == ["--method", "GET"], argv
+        page = int(next(a for a in argv if a.startswith("page="))[len("page=") :])
+        jq = argv[argv.index("--jq") + 1]
+        marker = json.loads(re.search(r"contains\((\".*\")\)", jq).group(1))
+        rows = [
+            {"login": c["login"], "marker": marker in c["body"]} for c in self.comments
+        ]
+        return ok(json.dumps(rows if page == 1 else []))
+
+
+def call(
+    world: World,
+    outcome: str = "succeeded",
+    *,
+    run_id: int = RUN,
+    summary: object = None,
+    **over,
+) -> str:
+    args = {
+        "repo": REPO,
+        "issue": ISSUE,
+        "project_id": PROJECT,
+        "run_id": run_id,
+        "outcome": outcome,
+        "summary_path": summary,
+    }
+    args.update(over)
+    return complete.complete(runner=world, **args)
+
+
+def moved_option(world: World) -> str:
+    argv = world.mutations[0]
+    return next(a for a in argv if a.startswith("optionId="))[len("optionId=") :]
+
+
+def test_succeeded_posts_one_comment_and_moves_the_status_to_in_review() -> None:
+    world = World(node(status="Plan"))
+    assert call(world) == complete.COMPLETED
+    assert len(world.posts) == 1 and len(world.mutations) == 1
+    assert moved_option(world) == IN_REVIEW_ID
+    assert "itemId=PVTI_cfg" in world.mutations[0]
+    assert f"projectId={PROJECT}" in world.mutations[0]
+    assert "fieldId=PVTSSF_status" in world.mutations[0]
+
+
+@pytest.mark.parametrize("status", predicates.ALLOWED_STATUSES)
+def test_every_allowed_status_ends_at_in_review(status: str) -> None:
+    world = World(node(status=status))
+    assert call(world) == complete.COMPLETED
+    assert moved_option(world) == IN_REVIEW_ID
+
+
+def test_the_end_status_table_is_keyed_by_exactly_the_allowed_statuses() -> None:
+    assert tuple(complete.END_STATUS) == predicates.ALLOWED_STATUSES
+    assert set(complete.END_STATUS.values()) == {"In review"}
+
+
+@pytest.mark.parametrize("outcome", ["failed", "blocked", "partial"])
+def test_other_outcomes_post_a_comment_and_never_move_the_status(outcome: str) -> None:
+    world = World(node(status="Plan"))
+    assert call(world, outcome) == complete.COMMENTED
+    assert len(world.posts) == 1 and world.mutations == []
+    assert f"Result of the run: {outcome}" in world.posts[0]
+    # no Project read is needed for a non-moving outcome
+    assert not any("projectItems" in " ".join(a) for a in world.argvs)
+
+
+def test_an_issue_on_two_projects_uses_the_configured_project_and_its_item() -> None:
+    world = World(
+        node("PVTI_other", OTHER_PROJECT, "Plan"), node("PVTI_cfg", PROJECT, "Plan")
+    )
+    assert call(world) == complete.COMPLETED
+    assert "itemId=PVTI_cfg" in world.mutations[0]
+    assert f"projectId={PROJECT}" in world.mutations[0]
+    assert "itemId=PVTI_other" not in world.mutations[0]
+
+
+def test_zero_items_in_the_project_are_refused_with_no_write() -> None:
+    world = World(node("PVTI_other", OTHER_PROJECT, "Plan"))
+    assert call(world) == "refused:project_missing"
+    assert world.posts == [] and world.mutations == []
+
+
+def test_an_archived_item_does_not_count() -> None:
+    world = World(node("PVTI_old", PROJECT, "Plan", archived=True))
+    assert call(world) == "refused:project_missing"
+    world = World(node("PVTI_old", PROJECT, "Plan", archived=True), node("PVTI_new"))
+    assert call(world) == complete.COMPLETED
+    assert "itemId=PVTI_new" in world.mutations[0]
+
+
+def test_two_live_items_in_the_project_are_refused_with_no_write() -> None:
+    world = World(node("PVTI_a"), node("PVTI_b"))
+    assert call(world) == "refused:project_ambiguous"
+    assert world.posts == [] and world.mutations == []
+
+
+def test_a_status_field_without_an_in_review_option_is_refused_with_no_write() -> None:
+    world = World(node(options=OPTIONS[:2]))
+    assert call(world) == "refused:status_option_missing"
+    assert world.posts == [] and world.mutations == []
+    world = World(node(options=[]))
+    assert call(world) == "refused:status_option_missing"
+    assert world.posts == [] and world.mutations == []
+
+
+@pytest.mark.parametrize("status", ["Done", "Backlog", "In progress", None])
+def test_a_status_a_person_moved_gets_the_comment_and_no_mutation(
+    status: str | None,
+) -> None:
+    world = World(node(status=status))
+    assert call(world) == complete.STATUS_MOVED_BY_PERSON
+    assert len(world.posts) == 1 and world.mutations == []
+
+
+def test_a_second_call_for_the_same_run_posts_no_second_comment() -> None:
+    world = World(node(status="Plan"))
+    assert call(world, "failed") == complete.COMMENTED
+    assert call(world, "failed") == complete.COMMENTED
+    assert len(world.posts) == 1
+
+
+def test_another_run_id_does_not_suppress_the_comment() -> None:
+    world = World()
+    call(world, "failed", run_id=4242)
+    call(
+        world, "failed", run_id=42420
+    )  # 4242 is a prefix of 42420: still its own marker
+    call(world, "failed", run_id=4243)
+    assert len(world.posts) == 3
+
+
+def test_a_marker_posted_by_another_login_does_not_suppress_the_comment() -> None:
+    world = World()
+    world.other_comment("someone-else", complete.result_marker(ISSUE, RUN))
+    assert call(world, "failed") == complete.COMMENTED
+    assert len(world.posts) == 1
+
+
+def test_a_failed_first_move_is_retried_by_the_second_call() -> None:
+    world = World(node(status="Plan"))
+    world.fail_move = True
+    assert call(world) == "failed:status_move"
+    assert len(world.posts) == 1 and len(world.mutations) == 1  # the comment stays
+    world.fail_move = False
+    assert call(world) == complete.COMPLETED
+    assert len(world.posts) == 1  # no second comment
+    assert len(world.mutations) == 2
+
+
+def test_a_call_after_a_successful_move_changes_nothing() -> None:
+    world = World(node(status="In review"))
+    assert call(world) == complete.COMPLETED
+    assert world.mutations == []
+
+
+def test_a_graphql_error_in_a_200_reply_is_a_failed_move() -> None:
+    world = World(node(status="Plan"))
+    real = world.run
+
+    def run(argv, timeout, *, cwd=None):
+        if argv[:3] == ["gh", "api", "graphql"] and any(
+            a.startswith("query=mutation") for a in argv
+        ):
+            world.mutations.append(list(argv))
+            return ok('{"errors": [{"message": "no"}]}')
+        return real(argv, timeout, cwd=cwd)
+
+    world.run = run  # type: ignore[method-assign]
+    assert call(world) == "failed:status_move"
+    assert len(world.posts) == 1
+
+
+def test_a_failed_comment_post_moves_nothing() -> None:
+    world = World(node(status="Plan"))
+    world.fail_post = True
+    assert call(world) == "failed:comment_post"
+    assert world.mutations == []
+
+
+@pytest.mark.parametrize(
+    "over,word",
+    [
+        ({"outcome": "done"}, "refused:bad_outcome"),
+        ({"outcome": None}, "refused:bad_outcome"),
+        ({"outcome": "Succeeded"}, "refused:bad_outcome"),
+        ({"issue": 0}, "refused:bad_issue"),
+        ({"issue": "9"}, "refused:bad_issue"),
+        ({"issue": True}, "refused:bad_issue"),
+        ({"issue": 10**9}, "refused:bad_issue"),
+        ({"project_id": "PVT_x; rm"}, "refused:bad_project_id"),
+        ({"project_id": "PVT_"}, "refused:bad_project_id"),
+        ({"project_id": "PVT_cfg\n"}, "refused:bad_project_id"),
+        ({"project_id": None}, "refused:bad_project_id"),
+        ({"repo": "SuperClaude-Org"}, "refused:bad_repo"),
+        ({"repo": "a/b/c"}, "refused:bad_repo"),
+        ({"repo": "a/b c"}, "refused:bad_repo"),
+        ({"repo": "{owner}/{repo}"}, "refused:bad_repo"),
+        ({"repo": None}, "refused:bad_repo"),
+        ({"run_id": 0}, "refused:bad_run"),
+        ({"run_id": "4242"}, "refused:bad_run"),
+        ({"run_id": True}, "refused:bad_run"),
+    ],
+)
+def test_bad_inputs_are_refused_before_any_call(over: dict, word: str) -> None:
+    world = World()
+    assert call(world, **over) == word
+    assert world.argvs == []
+
+
+def test_the_marker_never_contains_the_claim_marker() -> None:
+    marker = complete.result_marker(ISSUE, RUN)
+    assert marker == "<!-- sc:issue:result issue=9 run=4242 -->"
+    assert predicates.CLAIM_MARKER not in marker
+    world = World()
+    call(world, "failed")
+    assert predicates.CLAIM_MARKER not in world.posts[0]
+    assert world.posts[0].startswith(marker)
+
+
+def test_the_comment_holds_only_the_outcome_artifacts_and_pull_request(
+    tmp_path: Path,
+) -> None:
+    summary = tmp_path / "result.md"
+    summary.write_text(
+        "outcome: succeeded\nartifacts: .dev/issues/9/a.md, docs/b.md\npull_request: 12\n"
+    )
+    world = World(node(status="Plan"))
+    assert call(world, summary=str(summary)) == complete.COMPLETED
+    assert world.posts[0].splitlines()[1:] == [
+        "Result of the run: succeeded",
+        "Artifacts: .dev/issues/9/a.md, docs/b.md",
+        "Pull request: #12",
+    ]
+    bare = World()
+    call(bare, "failed")
+    assert bare.posts[0].splitlines()[2:] == ["Artifacts: none", "Pull request: none"]
+
+
+@pytest.mark.parametrize(
+    "text",
+    [
+        "",
+        "outcome: failed\n",
+        f"outcome: failed\nartifacts: {CANARY} and more\npull_request: none\n",
+        "outcome: failed\nartifacts: ../etc/passwd\npull_request: none\n",
+        "outcome: failed\nartifacts: a.md\npull_request: 0\n",
+        "outcome: failed\nartifacts: a.md\npull_request: #5\n",
+        "artifacts: a.md\noutcome: failed\npull_request: none\n",
+        "outcome: failed\nartifacts: a.md\npull_request: none\nextra: x\n",
+        "outcome: failed\nartifacts: "
+        + ", ".join(f"f{i}" for i in range(21))
+        + "\npull_request: none\n",
+    ],
+)
+def test_a_malformed_result_file_is_refused_with_no_call_and_nothing_echoed(
+    tmp_path: Path, text: str
+) -> None:
+    summary = tmp_path / "result.md"
+    summary.write_text(text)
+    world = World()
+    assert call(world, "failed", summary=str(summary)) == "refused:bad_summary"
+    assert world.argvs == []
+    assert call(world, "failed", summary=str(tmp_path / "missing.md")) == (
+        "refused:bad_summary"
+    )
+
+
+def test_every_result_is_a_closed_word_and_no_text_is_echoed(tmp_path: Path) -> None:
+    summary = tmp_path / "result.md"
+    summary.write_text("outcome: failed\nartifacts: a.md\npull_request: none\n")
+    words = set()
+    for status in ("Plan", "Done", "In review"):
+        words.add(call(World(node(status=status))))
+    words.add(call(World(), "failed", summary=str(summary)))
+    words.add(call(World(), "bogus"))
+    assert words <= complete.RESULT_WORDS
+    assert all(CANARY not in w for w in words)
+
+
+def test_the_coordinators_own_comment_leaves_unchanged_since_clean() -> None:
+    """Comments by the watcher's own login are skipped, so the result comment voids nothing."""
+    at = lambda s: datetime(2026, 11, 16, 10, s, 0, tzinfo=timezone.utc)  # noqa: E731
+    approved_at = at(10)
+    own = predicates.CommentEdit(1, OWN, at(30), at(31))
+    edits = predicates.EditEvidence(at(0), None, (own,))
+    assert predicates.unchanged_since(approved_at, edits, [], own_login=OWN) is None
+    other = predicates.CommentEdit(2, "stranger", at(30), None)
+    edits = predicates.EditEvidence(at(0), None, (own, other))
+    assert (
+        predicates.unchanged_since(approved_at, edits, [], own_login=OWN)
+        == "edited_after_approval"
+    )
+
+
+def test_the_module_writes_only_through_the_two_gh_forms_it_names() -> None:
+    world = World(node(status="Plan"))
+    call(world)
+    writes = [
+        a
+        for a in world.argvs
+        if "POST" in a or any(x.startswith("query=mutation") for x in a)
+    ]
+    assert len(writes) == 2
+    post = next(a for a in writes if "POST" in a)
+    assert post[:4] == ["gh", "api", "--method", "POST"]
+    assert post[4] == f"repos/{REPO}/issues/{ISSUE}/comments"

Task 12 context. complete.py is new and lives in src/superclaude/cli/issue_pipeline (outside github.py, which stays read-only). The result file pointer is the closed three-line result.md (outcome, artifacts, pull_request; run id is a separate parameter, per the Task 10 note). The helper "Task 7 adds next to project_check" is predicates.live_item, which complete.py uses. Result words are closed (RESULT_WORDS). The NG-2 scope change lives in tests/issue_watch/test_security_invariants.py (header and two new tests at the end). Tests run: tests/issue_pipeline tests/issue_watch: 3114 passed; ruff clean; make verify-sync clean.

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
