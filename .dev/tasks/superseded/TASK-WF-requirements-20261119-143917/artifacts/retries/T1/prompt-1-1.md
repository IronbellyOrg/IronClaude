b617d176112d3b52a6476d2736d79c455fbf9c83
Review one task for spec compliance.

Task brief: ## Task 1: Replace the Backlog check with a Status allow-list

In `src/superclaude/cli/issue_watch/predicates.py`, change `project_check` (lines 262 to 271) so an issue passes only when it is the one live item of the configured Project and its Status name is one of `Research`, `Spec`, `Plan` or `Debug` (requirement R22). Every other value, including `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later, returns `project_mismatch`. Keep the reason code `project_mismatch` (it is in `audit.REASON_TABLE`, `audit.py` line 72) so no reason table changes. Name the allowed set as one module constant, which Task 12 imports instead of copying the four words. The callers `cycle.py` lines 958 (`_examine`) and 1015 (`_revalidate`) keep calling `project_check` unchanged.

Acceptance criteria:
- T1.AC1: `project_check` returns `None` for each of `Research`, `Spec`, `Plan` and `Debug`, and `project_mismatch` for `Backlog`, `Ready`, `In progress`, `In review`, `Done`, `None` and an unknown name such as `Triage`.
- T1.AC2: `tests/issue_watch/test_predicates.py` has one case per status above, and the old `Backlog`-passes case is replaced, not left alongside.
- T1.AC3: `tests/issue_watch/test_cycle.py` and `tests/issue_watch/conftest.py` fixtures that used `Backlog` as the passing status now use an allowed status, and `uv run pytest tests/issue_watch -q` passes.
- T1.AC4: `src/superclaude/cli/issue_pipeline/reads.py` (a dependent of `issue_watch/github.py`) still imports and passes its tests: `uv run pytest tests/issue_pipeline -q`.
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
Start sha: b617d176112d3b52a6476d2736d79c455fbf9c83
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/predicates.py b/src/superclaude/cli/issue_watch/predicates.py
index 5280f311a..f8c6ce0eb 100644
--- a/src/superclaude/cli/issue_watch/predicates.py
+++ b/src/superclaude/cli/issue_watch/predicates.py
@@ -259,14 +259,18 @@ def unchanged_since(
     return None
 
 
+ALLOWED_STATUSES: tuple[str, ...] = ("Research", "Spec", "Plan", "Debug")
+
+
 def project_check(items: Iterable[ProjectItem], project_id: str) -> str | None:
-    """Return ``project_mismatch`` unless exactly one live item is in Backlog.
+    """Return ``project_mismatch`` unless exactly one live item has an allowed Status.
 
-    The item must be non-archived, in ``project_id`` and have Status
-    ``Backlog``.
+    The item must be non-archived, in ``project_id`` and have a Status named in
+    ``ALLOWED_STATUSES`` (R22). Any other value, a new board status included,
+    is a mismatch until it is added there.
     """
     matching = [i for i in items if not i.is_archived and i.project_id == project_id]
-    if len(matching) == 1 and matching[0].status_name == "Backlog":
+    if len(matching) == 1 and matching[0].status_name in ALLOWED_STATUSES:
         return None
     return "project_mismatch"
 
diff --git a/tests/issue_watch/conftest.py b/tests/issue_watch/conftest.py
index 9c25ea37b..97a6a52a2 100644
--- a/tests/issue_watch/conftest.py
+++ b/tests/issue_watch/conftest.py
@@ -547,7 +547,7 @@ class GhWorld:
     - ``edits``: ``created_at``, ``edited_at`` and ``comments`` (list of
       ``{id, author, created_at, edited_at}``); default the fixture as it is;
     - ``items``: Project items (list of ``{project_id, status, archived}``);
-      default one live item in the configured project with status Backlog;
+      default one live item in the configured project with status Research;
     - ``reread``: raw overrides of the G7 re-read reply.
 
     Events and comments are served in pages of ``github.PAGE_SIZE``; the two
@@ -870,10 +870,10 @@ class GhWorld:
                 "isArchived": spec.get("archived", False),
                 "project": {"id": spec.get("project_id", self.config.project_id)},
                 "fieldValueByName": None
-                if spec.get("status", "Backlog") is None
+                if spec.get("status", "Research") is None
                 else {
                     **template["fieldValueByName"],
-                    "name": spec.get("status", "Backlog"),
+                    "name": spec.get("status", "Research"),
                 },
             }
             for spec in ([{}] if specs is None else specs)
diff --git a/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json b/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json
index 55cc10196..0c1bf73c5 100644
--- a/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json
+++ b/tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json
@@ -14,7 +14,7 @@
                   "id": "PVT_test_project_0001"
                 },
                 "fieldValueByName": {
-                  "name": "Backlog"
+                  "name": "Research"
                 }
               }
             ],
diff --git a/tests/issue_watch/test_github.py b/tests/issue_watch/test_github.py
index 64e085887..c9ab51b21 100644
--- a/tests/issue_watch/test_github.py
+++ b/tests/issue_watch/test_github.py
@@ -972,7 +972,7 @@ def item_node(i: int = 0, **over: object) -> dict:
     node: dict = {
         "isArchived": False,
         "project": {"id": "PVT_1"},
-        "fieldValueByName": {"name": "Backlog"},
+        "fieldValueByName": {"name": "Research"},
     }
     node.update(over)
     return node
@@ -1052,7 +1052,7 @@ def test_project_items_has_next_page_then_false_reads_both_pages__fr007(
     got = github.project_items(runner, github.CallBudget(), 42, timeout)
     assert (got.reason, got.kind) == (None, "ok")
     assert got.value == (
-        ProjectItem(False, "PVT_1", "Backlog"),
+        ProjectItem(False, "PVT_1", "Research"),
         ProjectItem(True, "PVT_1", None),
     )
     assert [c[0] for c in runner.calls] == [
@@ -1484,7 +1484,7 @@ def test_project_items_reads_the_graphql_project_fixture__fr007(fake_runner) ->
     runner = fake_runner({argv: ok(payload, argv)})
     got = github.project_items(runner, github.CallBudget(), 42, timeout)
     assert (got.reason, got.kind) == (None, "ok")
-    assert got.value == (ProjectItem(False, "PVT_test_project_0001", "Backlog"),)
+    assert got.value == (ProjectItem(False, "PVT_test_project_0001", "Research"),)
     assert re.fullmatch(r"PVT_[A-Za-z0-9_-]{1,64}", got.value[0].project_id)
 
 
diff --git a/tests/issue_watch/test_predicates.py b/tests/issue_watch/test_predicates.py
index 5da7b272c..08bde613c 100644
--- a/tests/issue_watch/test_predicates.py
+++ b/tests/issue_watch/test_predicates.py
@@ -451,15 +451,25 @@ def item(
     *,
     project_id: str = PROJECT_ID,
     archived: bool = False,
-    status: str | None = "Backlog",
+    status: str | None = "Research",
 ) -> ProjectItem:
-    """Build a ``ProjectItem`` that is live, in ``PROJECT_ID`` and in Backlog."""
+    """Build a ``ProjectItem`` that is live, in ``PROJECT_ID`` and in Research."""
     return ProjectItem(is_archived=archived, project_id=project_id, status_name=status)
 
 
-def test_fr007_one_live_backlog_item_passes() -> None:
-    """FR-007: exactly one live item in the project at Backlog passes."""
-    assert project_check([item()], PROJECT_ID) is None
+@pytest.mark.parametrize("status", ["Research", "Spec", "Plan", "Debug"])
+def test_fr007_one_live_item_in_an_allowed_status_passes(status) -> None:
+    """R22: exactly one live item at Research, Spec, Plan or Debug passes."""
+    assert project_check([item(status=status)], PROJECT_ID) is None
+
+
+@pytest.mark.parametrize(
+    "status",
+    ["Backlog", "Ready", "In progress", "In review", "Done", None, "Triage"],
+)
+def test_r22_every_other_status_is_a_mismatch(status) -> None:
+    """R22: Backlog, Ready, In progress, In review, Done, empty and unknown refuse."""
+    assert project_check([item(status=status)], PROJECT_ID) == "project_mismatch"
 
 
 @pytest.mark.parametrize(
@@ -468,9 +478,7 @@ def test_fr007_one_live_backlog_item_passes() -> None:
         pytest.param([item(project_id="PVT_other")], id="wrong-project"),
         pytest.param([item(), item()], id="two-items"),
         pytest.param([item(archived=True)], id="archived-item"),
-        pytest.param([item(status="In progress")], id="status-in-progress"),
-        pytest.param([item(status="Backlog ")], id="status-near-miss"),
-        pytest.param([item(status=None)], id="status-missing"),
+        pytest.param([item(status="Research ")], id="status-near-miss"),
         pytest.param([], id="no-items"),
     ],
 )


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents of project_check not in the diff (Grep, call sites read): src/superclaude/cli/issue_watch/cycle.py:958 (_examine) and :1015 (_revalidate); both call project_check(items, cfg.project_id) unchanged. src/superclaude/cli/issue_pipeline/ has no call.

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
