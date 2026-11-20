20cd30f5c17dfc37dca5138efff1c1f3b1779870
Review one task for spec compliance.

Task brief: ## Task 3: Read the Pipeline field and the Status and Pipeline value times

Depends on: Task 1

In `src/superclaude/cli/issue_watch/github.py`, extend `PROJECT_ITEMS_QUERY` (lines 88 to 103). Today it reads only the Status `name`. Change it to two aliased single-select reads, `status: fieldValueByName(name: "Status")` and `pipeline: fieldValueByName(name: "Pipeline")`, each `... on ProjectV2ItemFieldSingleSelectValue { name createdAt updatedAt }`. Extend `_project_item` (lines 764 to 775) to parse them, and add `pipeline_name: str | None`, `status_changed_at: datetime | None` and `pipeline_changed_at: datetime | None` to the `ProjectItem` dataclass in `src/superclaude/cli/issue_watch/predicates.py` (around lines 113 to 118). The item-level `updatedAt` is not read (a label or a comment may move it; owner decision R33). The Pipeline values on the board are `None`, `Worktree`, `Full` and `Full Submit`; an absent Pipeline value is `pipeline_name = None` and `pipeline_changed_at = None`, which means the Pipeline has no value and so no time (it is the `None` pipeline); it is not an unreadable time. A Status or Pipeline value object that is present but carries no `createdAt` or `updatedAt`, or a time that does not parse, fails the whole read with the existing `unreadable` outcome. The query stays read-only. Requirement R31 relies on the value times: before relying on them, run one read-only GraphQL schema query for the type `ProjectV2ItemFieldSingleSelectValue` (`gh api graphql -f query='query { __type(name: "ProjectV2ItemFieldSingleSelectValue") { fields { name } } }'`) and save its output to `./artifacts/t3-single-select-value-fields.txt`. If either `createdAt` or `updatedAt` is not listed, stop and return the fallback of R31 (a level-specific approval label) to the owner.

Acceptance criteria:
- T3.AC1: `./artifacts/t3-single-select-value-fields.txt` exists and lists both `createdAt` and `updatedAt` (or the task stops with the R31 fallback reported).
- T3.AC2: `tests/issue_watch/test_github.py` parses a fixture with a Pipeline value and value times, a fixture with a null Pipeline (it parses to `pipeline_name = None` and `pipeline_changed_at = None`, not an error) and a malformed one (a present value with a missing or unparseable time gives the existing `non_json` or `unreadable` outcome, not an exception). The shape fixture `tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json` is updated.
- T3.AC3: `tests/issue_watch/test_security_invariants.py` still passes: the query contains no `mutation`.
- T3.AC4: Every other constructor call of `ProjectItem` in `tests/issue_watch/` is updated, and `uv run pytest tests/issue_watch -q` passes.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval label, the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the approval label after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: 20cd30f5c17dfc37dca5138efff1c1f3b1779870
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/github.py b/src/superclaude/cli/issue_watch/github.py
index 0b43a37ea..5ed8da6ec 100644
--- a/src/superclaude/cli/issue_watch/github.py
+++ b/src/superclaude/cli/issue_watch/github.py
@@ -92,8 +92,11 @@ PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
         nodes {
           isArchived
           project { id }
-          fieldValueByName(name: "Status") {
-            ... on ProjectV2ItemFieldSingleSelectValue { name }
+          status: fieldValueByName(name: "Status") {
+            ... on ProjectV2ItemFieldSingleSelectValue { name createdAt updatedAt }
+          }
+          pipeline: fieldValueByName(name: "Pipeline") {
+            ... on ProjectV2ItemFieldSingleSelectValue { name createdAt updatedAt }
           }
         }
         pageInfo { hasNextPage endCursor }
@@ -101,7 +104,10 @@ PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
     }
   }
 }"""
-"""G6: the issue's Project items with their Status value."""
+"""G6: the issue's Project items with their Status and Pipeline values and times.
+
+The item-level ``updatedAt`` is not read: a label or a comment may move it (R33).
+"""
 
 # --- argv builders (design 8.1, G1 to G7) -----------------------------------
 # Every REST path call carries --method GET (gh defaults to POST once parameters
@@ -765,16 +771,31 @@ def _project_item(node: object) -> ProjectItem:
     d = _obj(node)
     archived = d.get("isArchived")
     _check(type(archived) is bool)
-    # [UNVERIFIED] reply shape (design 837, FU-1): treated as None when the value
-    # is null or has no name; any other non-object value is malformed.
-    status = d.get("fieldValueByName")
+    status_name, status_at = _single_select(d.get("status"))
+    pipeline_name, pipeline_at = _single_select(d.get("pipeline"))
     return ProjectItem(
         is_archived=bool(archived),
         project_id=_text(_obj(d.get("project")).get("id")),
-        status_name=None if status is None else _opt_text(_obj(status).get("name")),
+        status_name=status_name,
+        pipeline_name=pipeline_name,
+        status_changed_at=status_at,
+        pipeline_changed_at=pipeline_at,
     )
 
 
+def _single_select(value: object) -> tuple[str | None, datetime | None]:
+    """Name and change time of one single-select value (R31).
+
+    An absent value (null) has no name and no time. A present value must carry
+    parseable ``createdAt`` and ``updatedAt``; the change time is the later one.
+    """
+    if value is None:
+        return None, None
+    d = _obj(value)
+    changed = max(_time(d.get("createdAt")), _time(d.get("updatedAt")))
+    return _opt_text(d.get("name")), changed
+
+
 # --- typed reads: public API --------------------------------------------------
 # ``timeout_for`` returns the next call's timeout, or None when no new ``gh``
 # call may start (under 5 s left, design 8.5). Every read returns a ``Read`` and
diff --git a/src/superclaude/cli/issue_watch/predicates.py b/src/superclaude/cli/issue_watch/predicates.py
index f8c6ce0eb..a49f575b6 100644
--- a/src/superclaude/cli/issue_watch/predicates.py
+++ b/src/superclaude/cli/issue_watch/predicates.py
@@ -116,6 +116,9 @@ class ProjectItem:
     is_archived: bool
     project_id: str
     status_name: str | None
+    pipeline_name: str | None = None
+    status_changed_at: datetime | None = None
+    pipeline_changed_at: datetime | None = None
 
 
 @dataclass(frozen=True)
diff --git a/tests/issue_watch/conftest.py b/tests/issue_watch/conftest.py
index 97a6a52a2..7496ecc3e 100644
--- a/tests/issue_watch/conftest.py
+++ b/tests/issue_watch/conftest.py
@@ -869,12 +869,15 @@ class GhWorld:
                 **template,
                 "isArchived": spec.get("archived", False),
                 "project": {"id": spec.get("project_id", self.config.project_id)},
-                "fieldValueByName": None
+                "status": None
                 if spec.get("status", "Research") is None
                 else {
-                    **template["fieldValueByName"],
+                    **template["status"],
                     "name": spec.get("status", "Research"),
                 },
+                "pipeline": None
+                if spec.get("pipeline") is None
+                else {**template["pipeline"], "name": spec["pipeline"]},
             }
             for spec in ([{}] if specs is None else specs)
         ]
diff --git a/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json b/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json
index 0c1bf73c5..f5ddeb533 100644
--- a/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json
+++ b/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json
@@ -13,8 +13,15 @@
                 "project": {
                   "id": "PVT_test_project_0001"
                 },
-                "fieldValueByName": {
-                  "name": "Research"
+                "status": {
+                  "name": "Research",
+                  "createdAt": "2026-01-01T00:00:00Z",
+                  "updatedAt": "2026-01-02T00:00:00Z"
+                },
+                "pipeline": {
+                  "name": "Worktree",
+                  "createdAt": "2026-01-03T00:00:00Z",
+                  "updatedAt": "2026-01-03T00:00:00Z"
                 }
               }
             ],
diff --git a/tests/issue_watch/test_github.py b/tests/issue_watch/test_github.py
index c9ab51b21..b7cfbf911 100644
--- a/tests/issue_watch/test_github.py
+++ b/tests/issue_watch/test_github.py
@@ -65,8 +65,11 @@ PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
         nodes {
           isArchived
           project { id }
-          fieldValueByName(name: "Status") {
-            ... on ProjectV2ItemFieldSingleSelectValue { name }
+          status: fieldValueByName(name: "Status") {
+            ... on ProjectV2ItemFieldSingleSelectValue { name createdAt updatedAt }
+          }
+          pipeline: fieldValueByName(name: "Pipeline") {
+            ... on ProjectV2ItemFieldSingleSelectValue { name createdAt updatedAt }
           }
         }
         pageInfo { hasNextPage endCursor }
@@ -295,8 +298,9 @@ def test_graphql_constants_equal_the_literal_drafts__df14() -> None:
                 "projectItems(first: 100, after: $after)",
                 "isArchived",
                 "project { id }",
-                'fieldValueByName(name: "Status")',
-                "ProjectV2ItemFieldSingleSelectValue { name }",
+                'status: fieldValueByName(name: "Status")',
+                'pipeline: fieldValueByName(name: "Pipeline")',
+                "ProjectV2ItemFieldSingleSelectValue { name createdAt updatedAt }",
                 "pageInfo { hasNextPage endCursor }",
             ],
         ),
@@ -603,6 +607,8 @@ def test_every_assumed_shape_fixture_is_read_by_a_test__df32() -> None:
 
 STAMP = "2026-11-07T10:00:00Z"
 STAMPED = datetime(2026, 11, 7, 10, 0, 0, tzinfo=timezone.utc)
+LATER = "2026-11-08T10:00:00Z"
+LATER_AT = datetime(2026, 11, 8, 10, 0, 0, tzinfo=timezone.utc)
 
 
 def timeout() -> float:
@@ -972,7 +978,8 @@ def item_node(i: int = 0, **over: object) -> dict:
     node: dict = {
         "isArchived": False,
         "project": {"id": "PVT_1"},
-        "fieldValueByName": {"name": "Research"},
+        "status": {"name": "Research", "createdAt": STAMP, "updatedAt": STAMP},
+        "pipeline": None,
     }
     node.update(over)
     return node
@@ -1046,13 +1053,13 @@ def test_project_items_has_next_page_then_false_reads_both_pages__fr007(
 ) -> None:
     replies = [
         project_page([item_node()], True, "c1"),
-        project_page([item_node(fieldValueByName=None, isArchived=True)], False, None),
+        project_page([item_node(status=None, isArchived=True)], False, None),
     ]
     runner = fake_runner(cursor_script(github.argv_project_items, replies))
     got = github.project_items(runner, github.CallBudget(), 42, timeout)
     assert (got.reason, got.kind) == (None, "ok")
     assert got.value == (
-        ProjectItem(False, "PVT_1", "Research"),
+        ProjectItem(False, "PVT_1", "Research", None, STAMPED, None),
         ProjectItem(True, "PVT_1", None),
     )
     assert [c[0] for c in runner.calls] == [
@@ -1484,10 +1491,60 @@ def test_project_items_reads_the_graphql_project_fixture__fr007(fake_runner) ->
     runner = fake_runner({argv: ok(payload, argv)})
     got = github.project_items(runner, github.CallBudget(), 42, timeout)
     assert (got.reason, got.kind) == (None, "ok")
-    assert got.value == (ProjectItem(False, "PVT_test_project_0001", "Research"),)
+    assert got.value == (
+        ProjectItem(
+            False,
+            "PVT_test_project_0001",
+            "Research",
+            "Worktree",
+            datetime(2026, 1, 2, tzinfo=timezone.utc),
+            datetime(2026, 1, 3, tzinfo=timezone.utc),
+        ),
+    )
     assert re.fullmatch(r"PVT_[A-Za-z0-9_-]{1,64}", got.value[0].project_id)
 
 
+def test_project_item_with_a_pipeline_value_keeps_name_and_later_time__r31(
+    fake_runner,
+) -> None:
+    pipeline = {"name": "Full Submit", "createdAt": STAMP, "updatedAt": LATER}
+    replies = [project_page([item_node(pipeline=pipeline)])]
+    runner = fake_runner(cursor_script(github.argv_project_items, replies))
+    got = github.project_items(runner, github.CallBudget(), 42, timeout)
+    (only,) = got.value
+    assert (only.pipeline_name, only.pipeline_changed_at) == ("Full Submit", LATER_AT)
+
+
+def test_project_item_with_a_null_pipeline_is_none_not_an_error__r34(
+    fake_runner,
+) -> None:
+    replies = [project_page([item_node(pipeline=None)])]
+    runner = fake_runner(cursor_script(github.argv_project_items, replies))
+    got = github.project_items(runner, github.CallBudget(), 42, timeout)
+    assert got.reason is None
+    (only,) = got.value
+    assert (only.pipeline_name, only.pipeline_changed_at) == (None, None)
+
+
+@pytest.mark.parametrize(
+    "over",
+    [
+        {"status": {"name": "Research", "updatedAt": STAMP}},
+        {"status": {"name": "Research", "createdAt": STAMP}},
+        {"status": {"name": "Research", "createdAt": "x", "updatedAt": STAMP}},
+        {"pipeline": {"name": "Full", "createdAt": STAMP}},
+        {"pipeline": {"name": "Full", "createdAt": STAMP, "updatedAt": 5}},
+    ],
+)
+def test_project_item_value_without_a_parseable_time_is_unreadable__r31(
+    fake_runner, over: dict
+) -> None:
+    replies = [project_page([item_node(**over)])]
+    runner = fake_runner(cursor_script(github.argv_project_items, replies))
+    got = github.project_items(runner, github.CallBudget(), 42, timeout)
+    assert (got.value, got.reason) == (None, "project_unreadable")
+
+
 # --- A-3: fixtures for the replies that had none ---------------------------------
 
 
diff --git a/.dev/tasks/to-do/TASK-WF-requirements-20261119-143917/artifacts/t3-single-select-value-fields.txt b/.dev/tasks/to-do/TASK-WF-requirements-20261119-143917/artifacts/t3-single-select-value-fields.txt
new file mode 100644
index 000000000..f7a3d1004
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-requirements-20261119-143917/artifacts/t3-single-select-value-fields.txt
@@ -0,0 +1 @@
+{"data":{"__type":{"fields":[{"name":"color"},{"name":"createdAt"},{"name":"creator"},{"name":"databaseId"},{"name":"description"},{"name":"descriptionHTML"},{"name":"field"},{"name":"id"},{"name":"item"},{"name":"name"},{"name":"nameHTML"},{"name":"optionId"},{"name":"updatedAt"}]}}}
\ No newline at end of file


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (Grep, read): ProjectItem constructors outside the touched files: tests/issue_watch/test_predicates.py:457 (uses the three original fields; the new fields default to None). src/superclaude/cli/issue_pipeline/reads.py calls github.project_items without constructing ProjectItem. The new fields are dataclass defaults, so no other constructor call needs a change. The full run of tests/issue_watch and tests/issue_pipeline passed (2903).

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
