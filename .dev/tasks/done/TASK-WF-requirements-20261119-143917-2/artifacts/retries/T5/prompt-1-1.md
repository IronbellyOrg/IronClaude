24c5eca234bfb513c30e5728588aaad2fc2caf2c
Review one task for spec compliance.

Task brief: ## Task 5: Void an approval when the Status or Pipeline value changed after it

Depends on: Task 1, Task 3, Task 4, Task 4a

Implement requirement R31 in `src/superclaude/cli/issue_watch/predicates.py` and `src/superclaude/cli/issue_watch/cycle.py`. Add a predicate next to `edited_after_approval` (line 258) that returns the existing reason `edited_after_approval` when the later of the value times that exist is at or after the approval's time: the Status value time, and the Pipeline value time only when the Pipeline has a value. An absent Pipeline value contributes no time, so an issue whose Pipeline is empty (the `None` pipeline, the only level the closed ship gate lets launch) is judged on its Status time alone; a Pipeline cleared after the approval reads the same way and launches at `None`, the lowest level, so it raises no authority. An equal time counts as changed, as in `unchanged_since` (one-second resolution, line 257), and a Status name with no Status time also refuses (Task 3's read layer already rejects a present value with a missing or unparseable time). In `_examine` (line 915) call it after `unchanged_since` (lines 949 to 956) and before `project_check` (lines 957 to 960). In `_revalidate` (line 979) call it after the approval reread (lines 1007 to 1011) and the items reread (lines 1012 to 1014), and before `project_check`, so a Pipeline or Status changed after the approval label cannot launch and the specific reason wins. Reuse the reason code so no reason table changes.

Acceptance criteria:
- T5.AC1: `tests/issue_watch/test_predicates.py` covers: value times before approval pass, at the same instant refuse, after approval refuse, a Status name with no Status time refuses, a value an hour older than the approval passes, an empty Pipeline with a Status time before the approval passes, a Pipeline cleared after the approval passes at the `None` pipeline, and a Pipeline value changed after the approval refuses.
- T5.AC2: `tests/issue_watch/test_cycle.py` shows a Pipeline raised from None to Full Submit after approval ends with `edited_after_approval` and no launch call, both at examine time and between examine and launch, and shows an approved issue whose Pipeline is empty and whose Status time is before the approval launches with `--pipeline none` (it is not refused as edited after approval).
- T5.AC3: `tests/issue_watch/test_security_invariants.py` passes and `uv run pytest tests/issue_watch -q` passes.
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
Start sha: 24c5eca234bfb513c30e5728588aaad2fc2caf2c
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/cycle.py b/src/superclaude/cli/issue_watch/cycle.py
index d199be9b1..b3a1f98f0 100644
--- a/src/superclaude/cli/issue_watch/cycle.py
+++ b/src/superclaude/cli/issue_watch/cycle.py
@@ -981,6 +981,13 @@ class _Cycle:
         if why is not None:
             raise _Skip(why)
         items = self._val(github.project_items(d.runner, self.budget, c.n, self._tf))
+        why = predicates.value_changed_after(
+            items,  # type: ignore[arg-type]
+            cfg.project_id,
+            approval.approved_at,  # type: ignore[arg-type]
+        )
+        if why is not None:
+            raise _Skip(why)
         why = predicates.project_check(items, cfg.project_id)  # type: ignore[arg-type]
         if why is not None:
             raise _Skip(why)
@@ -1036,6 +1043,13 @@ class _Cycle:
         items = self._rv(
             github.project_items(d.runner, self.budget, c.n, self._tf, reserved=True)
         )
+        why = predicates.value_changed_after(
+            items,  # type: ignore[arg-type]
+            cfg.project_id,
+            again.approved_at,  # type: ignore[arg-type]
+        )
+        if why is not None:
+            raise _Skip(why)
         if predicates.project_check(items, cfg.project_id) is not None:  # type: ignore[arg-type]
             raise _Skip("revalidation_failed")
 
diff --git a/src/superclaude/cli/issue_watch/predicates.py b/src/superclaude/cli/issue_watch/predicates.py
index efad7341e..b2c9329bb 100644
--- a/src/superclaude/cli/issue_watch/predicates.py
+++ b/src/superclaude/cli/issue_watch/predicates.py
@@ -296,6 +296,37 @@ def unchanged_since(
     return None
 
 
+def value_changed_after(
+    items: Iterable[ProjectItem], project_id: str, approved_at: datetime
+) -> str | None:
+    """Return ``edited_after_approval`` when the Status or Pipeline changed since approval.
+
+    Looks at the one live item of ``project_id`` (any other shape is left to
+    ``project_check``). The later of the value times that exist counts: the
+    Status time, and the Pipeline time only when the Pipeline has a value, so an
+    empty Pipeline (the ``None`` pipeline) has no time to compare and a Pipeline
+    cleared after the approval raises no authority. An equal time counts as
+    changed, as in ``unchanged_since``; a Status name with no Status time refuses
+    (R31, R34).
+    """
+    live = [i for i in items if not i.is_archived and i.project_id == project_id]
+    if len(live) != 1:
+        return None
+    item = live[0]
+    times: list[datetime] = []
+    if item.status_name is not None:
+        if item.status_changed_at is None:
+            return "edited_after_approval"
+        times.append(item.status_changed_at)
+    if item.pipeline_name is not None:
+        if item.pipeline_changed_at is None:
+            return "edited_after_approval"
+        times.append(item.pipeline_changed_at)
+    if times and max(times) >= approved_at:
+        return "edited_after_approval"
+    return None
+
+
 ALLOWED_STATUSES: tuple[str, ...] = ("Research", "Spec", "Plan", "Debug")
 
 
diff --git a/tests/issue_watch/conftest.py b/tests/issue_watch/conftest.py
index f9291fb33..1f11f0de2 100644
--- a/tests/issue_watch/conftest.py
+++ b/tests/issue_watch/conftest.py
@@ -330,6 +330,14 @@ def _stamp(value: object) -> object:
     return format_utc(value) if isinstance(value, datetime) else value
 
 
+def _value_times(at: object) -> dict:
+    """``createdAt`` and ``updatedAt`` of a Project field value set to ``at`` (R31).
+
+    ``None`` keeps the fixture's own times.
+    """
+    return {} if at is None else {"createdAt": _stamp(at), "updatedAt": _stamp(at)}
+
+
 def _stamped(item: dict) -> dict:
     return {key: _stamp(value) for key, value in item.items()}
 
@@ -934,10 +942,15 @@ class GhWorld:
                 else {
                     **template["status"],
                     "name": spec.get("status", "Research"),
+                    **_value_times(spec.get("status_at")),
                 },
                 "pipeline": None
                 if spec.get("pipeline") is None
-                else {**template["pipeline"], "name": spec["pipeline"]},
+                else {
+                    **template["pipeline"],
+                    "name": spec["pipeline"],
+                    **_value_times(spec.get("pipeline_at")),
+                },
             }
             for spec in ([{}] if specs is None else specs)
         ]
diff --git a/tests/issue_watch/test_cycle.py b/tests/issue_watch/test_cycle.py
index bd475b798..2fb6f43d9 100644
--- a/tests/issue_watch/test_cycle.py
+++ b/tests/issue_watch/test_cycle.py
@@ -2775,6 +2775,65 @@ def test_an_unreadable_issue_skips_and_the_next_one_is_still_examined__fr007_fr0
     )
 
 
+def test_a_pipeline_raised_after_the_approval_is_edited_after_approval__r31(
+    tmp_path, tmp_state, gh_world
+):
+    """R31: Pipeline None to Full Submit after the approval voids it; no launch."""
+    world = gh_world()
+    world.issue(
+        9,
+        items=[
+            {
+                "pipeline": "Full Submit",
+                "pipeline_at": T_APPROVED + timedelta(minutes=1),
+            }
+        ],
+    )
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "edited_after_approval")]
+    assert deps.launcher.calls == []
+    assert not _probed(world)
+
+
+def test_a_pipeline_raised_between_examine_and_launch_is_edited_after_approval__r31(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    world.issue(9)
+    raised = [
+        {"pipeline": "Full Submit", "pipeline_at": T_APPROVED + timedelta(minutes=1)}
+    ]
+    _on_nth(world, "items", 9, 2, lambda: world.update(9, items=raised))
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "edited_after_approval")]
+    assert deps.launcher.calls == []
+    assert tmp_state.load().entries == {}
+
+
+def test_a_status_changed_after_the_approval_is_edited_after_approval__r31(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    world.issue(
+        9, items=[{"status": "Debug", "status_at": T_APPROVED + timedelta(seconds=1)}]
+    )
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "edited_after_approval")]
+    assert deps.launcher.calls == []
+
+
+def test_an_empty_pipeline_with_a_status_before_the_approval_launches_none__r34(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    world.issue(
+        9, items=[{"status": "Plan", "status_at": T_APPROVED - timedelta(hours=1)}]
+    )
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
+    assert [c[2] for c in deps.launcher.calls] == [_CLAIM_9]
+
+
 def test_a_real_label_named_issue_watch_approved_never_approves__r35(
     tmp_path, tmp_state, gh_world
 ):
diff --git a/tests/issue_watch/test_predicates.py b/tests/issue_watch/test_predicates.py
index 08bde613c..21e1d88cc 100644
--- a/tests/issue_watch/test_predicates.py
+++ b/tests/issue_watch/test_predicates.py
@@ -29,6 +29,7 @@ from superclaude.cli.issue_watch.predicates import (
     unchanged_since,
     valid_issue_number,
     valid_operation_id,
+    value_changed_after,
 )
 
 T0 = datetime(2026, 11, 1, 12, 0, 0, tzinfo=timezone.utc)
@@ -487,6 +488,86 @@ def test_fr007_project_mismatch_rows(items) -> None:
     assert project_check(items, PROJECT_ID) == "project_mismatch"
 
 
+# --- value_changed_after (R31, R34) ---------------------------------------------
+
+APPROVED_AT = at(1000)
+
+
+def timed(
+    *,
+    status_at: datetime | None = at(100),
+    pipeline: str | None = None,
+    pipeline_at: datetime | None = None,
+    status: str | None = "Research",
+) -> list[ProjectItem]:
+    return [
+        ProjectItem(
+            is_archived=False,
+            project_id=PROJECT_ID,
+            status_name=status,
+            pipeline_name=pipeline,
+            status_changed_at=status_at,
+            pipeline_changed_at=pipeline_at,
+        )
+    ]
+
+
+@pytest.mark.parametrize(
+    ("items", "expected"),
+    [
+        pytest.param(timed(), None, id="status-before-approval-passes"),
+        pytest.param(timed(status_at=at(1000 - 3600)), None, id="an-hour-older-passes"),
+        pytest.param(
+            timed(status_at=APPROVED_AT),
+            "edited_after_approval",
+            id="status-at-the-same-instant",
+        ),
+        pytest.param(
+            timed(status_at=at(1001)),
+            "edited_after_approval",
+            id="status-after-approval",
+        ),
+        pytest.param(
+            timed(status_at=None),
+            "edited_after_approval",
+            id="status-name-without-a-time",
+        ),
+        pytest.param(
+            timed(pipeline="Worktree", pipeline_at=at(200)),
+            None,
+            id="both-before-passes",
+        ),
+        pytest.param(
+            timed(pipeline="Full Submit", pipeline_at=at(1500)),
+            "edited_after_approval",
+            id="pipeline-changed-after-approval",
+        ),
+        pytest.param(
+            timed(pipeline="Full", pipeline_at=None),
+            "edited_after_approval",
+            id="pipeline-name-without-a-time",
+        ),
+        pytest.param(
+            timed(pipeline=None, pipeline_at=None), None, id="empty-pipeline-passes"
+        ),
+    ],
+)
+def test_r31_value_times_after_the_approval_void_it(items, expected) -> None:
+    assert value_changed_after(items, PROJECT_ID, APPROVED_AT) == expected
+
+
+def test_r34_a_pipeline_cleared_after_the_approval_launches_at_none() -> None:
+    """A cleared Pipeline has no value and no time; the Status time before approval stands."""
+    items = timed(status_at=at(100), pipeline=None, pipeline_at=None)
+    assert value_changed_after(items, PROJECT_ID, APPROVED_AT) is None
+
+
+def test_r31_other_item_shapes_are_left_to_project_check() -> None:
+    assert value_changed_after([], PROJECT_ID, APPROVED_AT) is None
+    two = timed(status_at=at(5000)) + timed(status_at=at(5000))
+    assert value_changed_after(two, PROJECT_ID, APPROVED_AT) is None
+
+
 def test_fr007_archived_item_does_not_count_toward_the_one() -> None:
     """FR-007: an archived duplicate is ignored, so one live item still passes."""
     assert project_check([item(archived=True), item()], PROJECT_ID) is None


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (Grep, read): value_changed_after is new and called only from cycle.py _examine and _revalidate (both in the diff). The reason edited_after_approval is already in audit.REASON_TABLE, so no reason table changes. ProjectItem's three time fields default to None, so the other constructors (tests/issue_watch/test_predicates.py item(), test_github.py) are unaffected. Full run of tests/issue_watch and tests/issue_pipeline: 2935 passed.

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
