2bedec008cefe57b5bf82c5119fca51ae846f16e
Review one task for spec compliance.

Task brief: ## Task 4a: Read the Approved issue field as the approval

Depends on: Task 3

Implement requirement R35 so the approval is the issue field `Approved` set to `Yes` and the approval logic of today keeps working unchanged. In `src/superclaude/cli/issue_watch/github.py` add a read-only GraphQL query next to `EDITS_QUERY`, written the same way so Task 15 threads the repo through it: `timelineItems(first: 100, after: $after, itemTypes: [ISSUE_FIELD_ADDED_EVENT, ISSUE_FIELD_CHANGED_EVENT, ISSUE_FIELD_REMOVED_EVENT])`, reading `__typename`, `createdAt`, `actor { __typename login ... on User { databaseId } }`, `issueField { ... on IssueFieldSingleSelect { name } }`, and on the added event `value`, on the changed event `newValue`. Add its argv builder and a public read `approval_events` that pages like the other GraphQL reads (the cursor rules of DF-19 apply) and returns `LabelEvent` values for the field named `Approved` only, with these rules: `label` is the constant `APPROVAL_FIELD_LABEL = "issue-field:Approved"`; an added event with value `Yes`, or a changed event with `newValue` `Yes`, is `labeled`; a removed event, or a changed event whose `newValue` is not `Yes`, is `unlabeled`; `actor_id` is the actor's `databaseId`, and an actor without one (a bot) keeps `actor_id` 0, which no approver id equals, so a bot can never approve but a bot's removal still withdraws the approval; `actor_type` is the actor's `__typename`; `id` is the event's `createdAt` as whole seconds since the epoch (shortcut: two approval events on one issue inside one second share an id, and the GraphQL node id is a string that the integer `LabelEvent.id` cannot hold; upgrade when the approval record can store a string id). Events for any other field are ignored. A reply with a missing or unparseable `createdAt`, `actor` or value is unreadable with the reason the other event reads use.

Make the approval predicates see the field. `DEFAULT_APPROVAL_LABEL` (`cycle.py` line 56) becomes `APPROVAL_FIELD_LABEL`, so `approval_label` in the config now names the field's pseudo label; a real label `issue-watch:approved` is never read as an approval. In `cycle.py` the examine and revalidate steps merge `approval_events` into the REST label events (dropping any REST event whose label equals `APPROVAL_FIELD_LABEL`), and the issue reread (G7) adds `APPROVAL_FIELD_LABEL` to `IssueSnapshot.labels` when the issue's `issue_field_values` hold `Approved` with the option `Yes`, so `approval_of` (`predicates.py` lines 189 to 220) and `_revalidate` (`cycle.py` line 988) need no change. In `src/superclaude/cli/issue_pipeline/reads.py`, `read_stage_evidence` merges the same events so `stage-status` judges the same approval. Keep `github.py` read-only (no mutation, no POST).

Acceptance criteria:
- T4a.AC1: `tests/issue_watch/test_github.py` parses fixtures for: added Yes by a user, changed to Yes, removed, changed away from Yes, an event for another field (ignored), a bot actor (`actor_id` 0), a missing `createdAt` (unreadable), and a repeated end cursor (incomplete). A new fixture `tests/issue_watch/fixtures/_assumed_shape/graphql_issue_field_events.json` holds the verified shape (`value` and `newValue` are plain strings; `actor.databaseId` is an integer).
- T4a.AC2: `tests/issue_watch/test_predicates.py` or `test_cycle.py` shows an approver's `Approved`=Yes event approves, the same event by a non-approver does not, a removal after it withdraws it, a real label named `issue-watch:approved` applied by an approver never approves, a bot's `Yes` never approves, and the approval time compared by `unchanged_since` is the latest set event's `createdAt`.
- T4a.AC3: `tests/issue_pipeline/test_reads.py` or `test_stage_status.py` shows `stage-status` sees the same field approval.
- T4a.AC4: `tests/issue_watch/test_security_invariants.py` covers the new query (no `mutation`, no `subscription`, read-only argv) and passes; `uv run pytest tests/issue_watch tests/issue_pipeline -q` passes.
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
Start sha: 2bedec008cefe57b5bf82c5119fca51ae846f16e
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/reads.py b/src/superclaude/cli/issue_pipeline/reads.py
index 4a3d79266..4b08990ef 100644
--- a/src/superclaude/cli/issue_pipeline/reads.py
+++ b/src/superclaude/cli/issue_pipeline/reads.py
@@ -32,7 +32,11 @@ from superclaude.cli.issue_watch.github import (
     _text,
     _time,
 )
-from superclaude.cli.issue_watch.predicates import EditEvidence, LabelEvent
+from superclaude.cli.issue_watch.predicates import (
+    EditEvidence,
+    LabelEvent,
+    merge_approval_events,
+)
 from superclaude.cli.issue_watch.runner import Runner
 
 from .stage_predicates import CommentFact, PlanMarker
@@ -142,13 +146,17 @@ def read_stage_evidence(
     events = gh.events(runner, budget, n, timeout_for)
     if events.value is None:
         return events
+    field_events = gh.approval_events(runner, budget, n, timeout_for)
+    if field_events.value is None:
+        return field_events
+    merged = merge_approval_events(events.value, field_events.value)  # type: ignore[arg-type]
     found = comments(runner, budget, n, timeout_for)
     if found.value is None:
         return found
     edits = gh.edits(runner, budget, n, timeout_for)
     if edits.value is None:
         return edits
-    return Read(StageEvidence(found.value, events.value, edits.value))  # type: ignore[arg-type]
+    return Read(StageEvidence(found.value, merged, edits.value))  # type: ignore[arg-type]
 
 
 __all__ = [
diff --git a/src/superclaude/cli/issue_watch/cycle.py b/src/superclaude/cli/issue_watch/cycle.py
index 7aa7e2fb9..d199be9b1 100644
--- a/src/superclaude/cli/issue_watch/cycle.py
+++ b/src/superclaude/cli/issue_watch/cycle.py
@@ -53,7 +53,8 @@ NETWORK_FS_TYPES = frozenset(
 
 SCHEMA_VERSION = 1
 DEFAULT_TRIGGER_LABEL = "issue-watch:trigger"
-DEFAULT_APPROVAL_LABEL = "issue-watch:approved"
+DEFAULT_APPROVAL_LABEL = predicates.APPROVAL_FIELD_LABEL
+"""The approval is the ``Approved`` issue field, seen as this pseudo label (R35)."""
 
 _TOP_KEYS = frozenset(
     {
@@ -241,6 +242,10 @@ def load_config(path: str | os.PathLike[str]) -> Config:
     approval = _label(labels.get("approval", DEFAULT_APPROVAL_LABEL), "approval")
     if trigger == approval:
         raise _invalid("labels.approval must differ from labels.trigger")
+    if approval != DEFAULT_APPROVAL_LABEL:
+        raise _invalid(
+            "labels.approval is the Approved issue field now (R35); remove the key"
+        )
 
     project_id = raw.get("project_id")
     if not isinstance(project_id, str) or _PROJECT_ID.fullmatch(project_id) is None:
@@ -845,6 +850,26 @@ class _Cycle:
             raise _Skip("budget_exhausted")
         raise _Skip(fallback or read.reason)
 
+    def _events(
+        self, n: int, fallback: str | None = None, *, reserved: bool = False
+    ) -> tuple[predicates.LabelEvent, ...]:
+        """The label events plus the ``Approved`` field events of issue ``n`` (R35)."""
+        d = self.deps
+
+        def check(read: github.Read) -> object:
+            return self._rv(read) if reserved else self._val(read, fallback)
+
+        # One after the other: a failed first read stops the cycle before the second.
+        label_events = check(
+            github.events(d.runner, self.budget, n, self._tf, reserved=reserved)
+        )
+        field_events = check(
+            github.approval_events(
+                d.runner, self.budget, n, self._tf, reserved=reserved
+            )
+        )
+        return predicates.merge_approval_events(label_events, field_events)  # type: ignore[arg-type]
+
     def _hit(
         self,
         markers: object,
@@ -882,7 +907,10 @@ class _Cycle:
         cfg = self.deps.config
         result = predicates.approval_of(
             events,  # type: ignore[arg-type]
-            labels_now=c.issue.labels,
+            labels_now=predicates.with_approval_field(
+                c.issue.labels,
+                events,  # type: ignore[arg-type]
+            ),
             trigger_label=cfg.trigger_label,
             approval_label=cfg.approval_label,
             approvers=self.approvers,
@@ -904,9 +932,7 @@ class _Cycle:
         markers = self._val(
             github.marker_comments(d.runner, self.budget, c.n, self._tf)
         )
-        events = self._val(
-            github.events(d.runner, self.budget, c.n, self._tf), fallback
-        )
+        events = self._events(c.n, fallback)
         approval = self._approve(c, events, fallback)
         if self._hit(markers, None, approval.approved_at):
             return self._claim(c, approval)
@@ -941,7 +967,7 @@ class _Cycle:
         markers = self._val(
             github.marker_comments(d.runner, self.budget, c.n, self._tf)
         )
-        events = self._val(github.events(d.runner, self.budget, c.n, self._tf))
+        events = self._events(c.n)
         approval = self._approve(c, events)
         if self._hit(markers, None, approval.approved_at):
             return self._claim(c, approval)  # T-11, T-12
@@ -992,9 +1018,7 @@ class _Cycle:
         if not owned:
             raise _Skip(why or "assigned_other")
         assert self.doc is not None and c.approval is not None
-        events = self._rv(
-            github.events(d.runner, self.budget, c.n, self._tf, reserved=True)
-        )
+        events = self._events(c.n, reserved=True)
         again = predicates.approval_of(
             events,  # type: ignore[arg-type]
             labels_now=snap.labels,
diff --git a/src/superclaude/cli/issue_watch/github.py b/src/superclaude/cli/issue_watch/github.py
index 5ed8da6ec..5c1432bb2 100644
--- a/src/superclaude/cli/issue_watch/github.py
+++ b/src/superclaude/cli/issue_watch/github.py
@@ -20,6 +20,9 @@ from email.utils import parsedate_to_datetime
 from typing import TypeVar
 
 from .predicates import (
+    APPROVAL_FIELD_LABEL,
+    APPROVAL_FIELD_NAME,
+    APPROVAL_FIELD_VALUE,
     CLAIM_MARKER,
     CommentEdit,
     DiscoveredIssue,
@@ -64,8 +67,16 @@ MARKER_JQ = (
 )
 """G4 projection of one comments page: the body becomes a boolean."""
 
-REREAD_JQ = "{number, state, labels: [.labels[].name], assignees: [.assignees[].login]}"
-"""G7 projection of the FR-011 issue re-read."""
+REREAD_JQ = (
+    "{number, state, labels: ([.labels[].name] + [.issue_field_values[]? | "
+    f"select(.issue_field_name == {json.dumps(APPROVAL_FIELD_NAME)} and "
+    f".single_select_option.name == {json.dumps(APPROVAL_FIELD_VALUE)}) | "
+    f"{json.dumps(APPROVAL_FIELD_LABEL)}]), assignees: [.assignees[].login]}}"
+)
+"""G7 projection of the FR-011 issue re-read.
+
+``Approved`` = ``Yes`` among the issue's field values shows as the pseudo label (R35).
+"""
 
 # --- GraphQL queries (design 8.1, G5, G6) -----------------------------------
 # [PROPOSAL, UNVERIFIED] drafts from decision DF-14 (research 06, Table 1.5).
@@ -109,6 +120,37 @@ PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
 The item-level ``updatedAt`` is not read: a label or a comment may move it (R33).
 """
 
+APPROVAL_EVENTS_QUERY = """query($number: Int!, $after: String) {
+  repository(owner: "IronbellyOrg", name: "IronClaude") {
+    issue(number: $number) {
+      timelineItems(first: 100, after: $after, itemTypes: [ISSUE_FIELD_ADDED_EVENT, ISSUE_FIELD_CHANGED_EVENT, ISSUE_FIELD_REMOVED_EVENT]) {
+        nodes {
+          __typename
+          ... on IssueFieldAddedEvent {
+            createdAt
+            actor { __typename login ... on User { databaseId } }
+            issueField { ... on IssueFieldSingleSelect { name } }
+            value
+          }
+          ... on IssueFieldChangedEvent {
+            createdAt
+            actor { __typename login ... on User { databaseId } }
+            issueField { ... on IssueFieldSingleSelect { name } }
+            newValue
+          }
+          ... on IssueFieldRemovedEvent {
+            createdAt
+            actor { __typename login ... on User { databaseId } }
+            issueField { ... on IssueFieldSingleSelect { name } }
+          }
+        }
+        pageInfo { hasNextPage endCursor }
+      }
+    }
+  }
+}"""
+"""G8: the issue's issue-field events, who set a field and when (R35)."""
+
 # --- argv builders (design 8.1, G1 to G7) -----------------------------------
 # Every REST path call carries --method GET (gh defaults to POST once parameters
 # are added); the GraphQL calls are POST and carry no --method (DF-28).
@@ -255,6 +297,11 @@ def argv_project_items(n: int, after: str | None = None) -> list[str]:
     return _argv_graphql(PROJECT_ITEMS_QUERY, n, after)
 
 
+def argv_approval_events(n: int, after: str | None = None) -> list[str]:
+    """G8: one page of the issue's issue-field events (R35)."""
+    return _argv_graphql(APPROVAL_EVENTS_QUERY, n, after)
+
+
 def argv_reread(n: int) -> list[str]:
     """G7: re-read the issue's number, state, labels and assignees (FR-011)."""
     return [
@@ -783,6 +830,55 @@ def _project_item(node: object) -> ProjectItem:
     )
 
 
+_FIELD_EVENT_TYPES = {
+    "IssueFieldAddedEvent": "value",
+    "IssueFieldChangedEvent": "newValue",
+    "IssueFieldRemovedEvent": None,
+}
+
+
+def _field_event(node: object) -> LabelEvent | None:
+    """One G8 node as a ``LabelEvent`` for ``Approved``, or None for another field.
+
+    The event id is the time in whole epoch seconds (shortcut: two approval
+    events on one issue inside one second share an id, because the GraphQL node
+    id is a string; upgrade when the approval record can store a string id).
+    A bot or deleted actor has no ``databaseId``: ``actor_id`` 0 is no approver,
+    yet its removal still withdraws the approval.
+    """
+    d = _obj(node)
+    kind = _text(d.get("__typename"))
+    _check(kind in _FIELD_EVENT_TYPES)
+    created = _time(d.get("createdAt"))
+    _check("actor" in d)
+    actor = d["actor"]
+    actor_id, login, actor_type = 0, None, None
+    if actor is not None:
+        a = _obj(actor)
+        login, actor_type = _text(a.get("login")), _text(a.get("__typename"))
+        db = a.get("databaseId")
+        actor_id = _pos_int(db) if db is not None else 0
+    _check("issueField" in d)
+    name = _obj(d["issueField"]).get("name") if d["issueField"] is not None else None
+    key = _FIELD_EVENT_TYPES[kind]
+    value = None
+    if key is not None:
+        _check(key in d)
+        value = _opt_text(d[key])
+    if name != APPROVAL_FIELD_NAME:
+        return None
+    on = key is not None and value == APPROVAL_FIELD_VALUE
+    return LabelEvent(
+        id=int(created.timestamp()),
+        event="labeled" if on else "unlabeled",
+        label=APPROVAL_FIELD_LABEL,
+        actor_id=actor_id,
+        actor_login=login,
+        actor_type=actor_type,
+        created_at=created,
+    )
+
+
 def _single_select(value: object) -> tuple[str | None, datetime | None]:
     """Name and change time of one single-select value (R31).
 
@@ -952,6 +1048,34 @@ def project_items(
     return out if isinstance(out, Read) else Read(out[1])
 
 
+def approval_events(
+    runner: Runner,
+    budget: CallBudget,
+    n: int,
+    timeout_for: Callable[[], float | None],
+    *,
+    reserved: bool = False,
+) -> Read:
+    """G8: a tuple of ``LabelEvent`` for the ``Approved`` issue field (R35).
+
+    Every failure is ``events_unreadable``, like the label events it joins.
+    """
+    out = _graphql_read(
+        runner,
+        budget,
+        timeout_for,
+        lambda after: argv_approval_events(n, after),
+        "timelineItems",
+        lambda issue: None,
+        _field_event,
+        "events_unreadable",
+        reserved,
+    )
+    if isinstance(out, Read):
+        return out
+    return Read(tuple(e for e in out[1] if e is not None))
+
+
 def reread(
     runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
 ) -> Read:
diff --git a/src/superclaude/cli/issue_watch/predicates.py b/src/superclaude/cli/issue_watch/predicates.py
index a49f575b6..efad7341e 100644
--- a/src/superclaude/cli/issue_watch/predicates.py
+++ b/src/superclaude/cli/issue_watch/predicates.py
@@ -14,6 +14,14 @@ from datetime import datetime, timedelta, timezone
 CLAIM_MARKER = "<!-- sc:issue:claim -->"
 """Claim-comment marker; ``github.MARKER_JQ`` is built from this constant."""
 
+APPROVAL_FIELD_NAME = "Approved"
+"""The organization issue field whose value ``Yes`` is the approval (R35)."""
+
+APPROVAL_FIELD_VALUE = "Yes"
+
+APPROVAL_FIELD_LABEL = "issue-field:Approved"
+"""The pseudo label that field events carry, so the approval logic stays generic."""
+
 SKEW_TOLERANCE_S = 300
 """Seconds a claim marker may precede ``pending_at`` and still count."""
 
@@ -185,6 +193,32 @@ def _second(value: datetime) -> datetime:
     return value.replace(microsecond=0)
 
 
+def merge_approval_events(
+    label_events: Iterable[LabelEvent], field_events: Iterable[LabelEvent]
+) -> tuple[LabelEvent, ...]:
+    """Label events plus the ``Approved`` field events (R35).
+
+    A REST label event that carries ``APPROVAL_FIELD_LABEL`` is dropped, so only
+    a real field event can stand for the approval.
+    """
+    kept = [e for e in label_events if e.label != APPROVAL_FIELD_LABEL]
+    return (*kept, *field_events)
+
+
+def with_approval_field(
+    labels: Iterable[str], events: Iterable[LabelEvent]
+) -> tuple[str, ...]:
+    """``labels`` plus ``APPROVAL_FIELD_LABEL`` when the latest field event is a set."""
+    mine = sorted(
+        (e for e in events if e.label == APPROVAL_FIELD_LABEL),
+        key=lambda e: (e.created_at, e.id),
+    )
+    out = tuple(labels)
+    if mine and mine[-1].event == "labeled" and APPROVAL_FIELD_LABEL not in out:
+        out += (APPROVAL_FIELD_LABEL,)
+    return out
+
+
 def approval_of(
     events: Iterable[LabelEvent],
     *,
diff --git a/tests/issue_pipeline/test_reads.py b/tests/issue_pipeline/test_reads.py
index dccc151d1..6f9208d49 100644
--- a/tests/issue_pipeline/test_reads.py
+++ b/tests/issue_pipeline/test_reads.py
@@ -52,6 +52,27 @@ def ok(stdout: str) -> CommandResult:
     return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)
 
 
+EMPTY_TIMELINE = json.dumps(
+    {
+        "data": {
+            "repository": {
+                "issue": {
+                    "timelineItems": {
+                        "nodes": [],
+                        "pageInfo": {"hasNextPage": False, "endCursor": None},
+                    }
+                }
+            }
+        }
+    }
+)
+"""A G8 reply with no ``Approved`` field events (R35)."""
+
+
+def is_timeline(argv: list[str]) -> bool:
+    return argv[:3] == ["gh", "api", "graphql"] and "timelineItems" in argv[4]
+
+
 def failed(stderr: str = "HTTP 502: Bad Gateway") -> CommandResult:
     return CommandResult(("gh",), 1, "", stderr, False, None, 0.0)
 
@@ -244,6 +265,8 @@ def test_call_cap_is_shared_across_events_comments_and_edits() -> None:
     recorded = {"events": _recorded_events(), "comments": _page(1)}
 
     def answer(argv: list[str]) -> CommandResult:
+        if is_timeline(argv):
+            return ok(EMPTY_TIMELINE)
         return ok(
             recorded["events"] if argv[4].endswith("/events") else recorded["comments"]
         )
@@ -263,6 +286,8 @@ def test_a_transient_gh_failure_returns_a_closed_reason_not_a_partial_approval()
     None
 ):
     def answer(argv: list[str]) -> CommandResult:
+        if is_timeline(argv):
+            return ok(EMPTY_TIMELINE)
         if argv[4].endswith("/events"):
             return ok(_recorded_events())
         return failed()
@@ -278,6 +303,8 @@ def test_the_whole_read_over_the_recorded_files_succeeds() -> None:
     edits = (RECORDED / "edits-page1.json").read_text()
 
     def answer(argv: list[str]) -> CommandResult:
+        if is_timeline(argv):
+            return ok(EMPTY_TIMELINE)
         if argv[:3] == ["gh", "api", "graphql"]:
             return ok(edits)
         if argv[4].endswith("/events"):
diff --git a/tests/issue_pipeline/test_stage_status.py b/tests/issue_pipeline/test_stage_status.py
index 8ed42af59..d66362692 100644
--- a/tests/issue_pipeline/test_stage_status.py
+++ b/tests/issue_pipeline/test_stage_status.py
@@ -104,6 +104,7 @@ class World:
         self.host, self.assignees = host, assignees
         self.comments: list[dict] = []
         self.events: list[dict] = []
+        self.field_nodes: list[dict] = []  # G8 nodes: the Approved field events (R35)
         self.edited: dict[int, str] = {}
         self.argvs: list[list[str]] = []
         self._next = 100
@@ -153,6 +154,20 @@ class World:
             }
         )
 
+    def field_set(
+        self, at: str, login: str = OWNER, uid: int = 111, kind: str = "User"
+    ) -> None:
+        """The Approved issue field set to Yes (R35), as GraphQL gives it."""
+        self.field_nodes.append(
+            {
+                "__typename": "IssueFieldAddedEvent",
+                "createdAt": at,
+                "actor": {"__typename": kind, "login": login, "databaseId": uid},
+                "issueField": {"name": "Approved"},
+                "value": "Yes",
+            }
+        )
+
     def status_move(self, at: str) -> None:
         self.events.append(
             {
@@ -166,6 +181,27 @@ class World:
     # the injected runner
     def run(self, argv, timeout, *, cwd=None) -> CommandResult:
         self.argvs.append(list(argv))
+        if argv[:3] == ["gh", "api", "graphql"] and "timelineItems" in argv[4]:
+            # The Approved field events (R35): none in these tests.
+            return ok(
+                json.dumps(
+                    {
+                        "data": {
+                            "repository": {
+                                "issue": {
+                                    "timelineItems": {
+                                        "nodes": self.field_nodes,
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
         if argv == ["gh", "api", "user", "--include"]:
             return ok(
                 "HTTP/2.0 200 OK\ndate: Mon, 16 Nov 2026 10:00:00 GMT\n\n"
@@ -234,9 +270,10 @@ def invoke(
     *args: str,
     issue: int = ISSUE,
     approvers=frozenset({222}),
+    label: str = LABEL,
 ):
     monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
-    monkeypatch.setattr(cli_mod, "_load_stage_inputs", lambda path: (LABEL, approvers))
+    monkeypatch.setattr(cli_mod, "_load_stage_inputs", lambda path: (label, approvers))
     return CliRunner().invoke(
         issue_pipeline_group, ["stage-status", str(issue), "--json", *args]
     )
@@ -295,7 +332,7 @@ def test_recorded_files_through_the_injected_runner_print_only_closed_keys(
     real_run = world.run
 
     def run(argv, timeout, *, cwd=None):
-        if argv[:3] == ["gh", "api", "graphql"]:
+        if argv[:3] == ["gh", "api", "graphql"] and "timelineItems" not in argv[4]:
             world.argvs.append(list(argv))
             return ok(json.dumps(raw_edits))
         return real_run(argv, timeout, cwd=cwd)
@@ -346,6 +383,29 @@ def test_label_only(monkeypatch, plan_dir: Path) -> None:
     assert out["status_seen"] is False
 
 
+def test_the_approved_field_is_seen_as_the_label_approval__r35(
+    monkeypatch, plan_dir: Path
+) -> None:
+    from superclaude.cli.issue_watch.predicates import APPROVAL_FIELD_LABEL
+
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    world.field_set(T1, uid=222)
+    result = invoke(
+        world,
+        monkeypatch,
+        "--plan-dir",
+        str(plan_dir),
+        "--plan-file",
+        "plan.md",
+        label=APPROVAL_FIELD_LABEL,
+    )
+    assert result.exit_code == 0, result.output
+    out = json.loads(result.output)
+    assert out["approved"] and out["approvals"]["label"]["accepted"]
+    assert out["approvals"]["label"]["actor_id"] == 222
+
+
 def test_comment_only(monkeypatch, plan_dir: Path) -> None:
     world = World()
     world.plan_reply(plan_sha(plan_dir))
@@ -460,7 +520,8 @@ def test_the_command_only_reads_and_never_calls_orca(
     assert sorted(p.name for p in tmp_path.rglob("*")) == before  # nothing was written
     assert world.argvs
     graphql = [a for a in world.argvs if a[:3] == ["gh", "api", "graphql"]]
-    assert graphql == [gh.argv_edits(ISSUE)]  # the watcher's fixed query, untouched
+    # the watcher's fixed queries, untouched: the Approved field events, then edits
+    assert graphql == [gh.argv_approval_events(ISSUE), gh.argv_edits(ISSUE)]
     for argv in world.argvs:
         assert argv[0] == "gh" and "orca" not in " ".join(argv).lower().split()
         if "--method" in argv:
diff --git a/tests/issue_watch/conftest.py b/tests/issue_watch/conftest.py
index 7496ecc3e..f9291fb33 100644
--- a/tests/issue_watch/conftest.py
+++ b/tests/issue_watch/conftest.py
@@ -744,6 +744,9 @@ class GhWorld:
             script[tuple(github.argv_comments(n, page))] = self._served(
                 "comments", n, lambda argv, p=page: self._comments_reply(argv, n, p)
             )
+        script[tuple(github.argv_approval_events(n))] = self._served(
+            "approval_events", n, lambda argv: self._approval_reply(argv, n)
+        )
         script[tuple(github.argv_edits(n))] = self._served(
             "edits", n, lambda argv: self._ok(argv, self._edits_payload(n))
         )
@@ -823,11 +826,68 @@ class GhWorld:
         chunk = items[(page - 1) * size : page * size]
         return self._ok(argv, [_stamped(item) for item in chunk])
 
-    def _events_reply(self, argv: tuple[str, ...], n: int, page: int) -> CommandResult:
+    def _all_events(self, n: int) -> list[dict]:
         events = self.issues[n]["events"]
-        events = default_events(self.config) if events is None else events
+        return default_events(self.config) if events is None else events
+
+    def _events_reply(self, argv: tuple[str, ...], n: int, page: int) -> CommandResult:
+        """The REST label events; approval-label events are served as field events."""
+        approval = self._field_label()
+        events = [e for e in self._all_events(n) if e.get("label") != approval]
         return self._paged(argv, events, page)
 
+    def _field_label(self) -> str | None:
+        """The approval label when it is the field's pseudo label, else None.
+
+        A test config that names a real label keeps that label in the REST events.
+        """
+        label = self.config.approval_label
+        return label if label == cycle.predicates.APPROVAL_FIELD_LABEL else None
+
+    def _approval_reply(self, argv: tuple[str, ...], n: int) -> CommandResult:
+        """The GraphQL field events G8: the approval-label events of ``events`` (R35)."""
+        approval = self._field_label()
+        nodes: list[dict] = []
+        for e in self._all_events(n):
+            if (
+                approval is None
+                or e.get("label") != approval
+                or e.get("event")
+                not in (
+                    "labeled",
+                    "unlabeled",
+                )
+            ):
+                continue
+            node = {
+                "__typename": "IssueFieldAddedEvent"
+                if e["event"] == "labeled"
+                else "IssueFieldRemovedEvent",
+                "createdAt": _stamp(e["created_at"]),
+                "actor": {
+                    "__typename": e.get("actor_type") or "User",
+                    "login": e.get("actor_login") or "ghost",
+                    "databaseId": e.get("actor_id"),
+                },
+                "issueField": {"name": "Approved"},
+            }
+            if e["event"] == "labeled":
+                node["value"] = "Yes"
+            nodes.append(node)
+        payload = {
+            "data": {
+                "repository": {
+                    "issue": {
+                        "timelineItems": {
+                            "nodes": nodes,
+                            "pageInfo": {"hasNextPage": False, "endCursor": None},
+                        }
+                    }
+                }
+            }
+        }
+        return self._ok(argv, payload)
+
     def _comments_reply(
         self, argv: tuple[str, ...], n: int, page: int
     ) -> CommandResult:
diff --git a/tests/issue_watch/test_cli_e2e.py b/tests/issue_watch/test_cli_e2e.py
index 074cdcebe..9aa5cf226 100644
--- a/tests/issue_watch/test_cli_e2e.py
+++ b/tests/issue_watch/test_cli_e2e.py
@@ -267,11 +267,13 @@ def expected_eligible_sequence(watcher: Watcher) -> list[tuple[str, list[str]]]:
         ("gh", DISCOVERY_ARGV),
         ("gh", github.argv_comments(ISSUE, 1)[1:]),
         ("gh", github.argv_events(ISSUE, 1)[1:]),
+        ("gh", github.argv_approval_events(ISSUE)[1:]),
         ("gh", github.argv_edits(ISSUE)[1:]),
         ("gh", github.argv_project_items(ISSUE)[1:]),
         ("orca-ide", ["skills", "list", "--json"]),
         ("gh", github.argv_reread(ISSUE)[1:]),
         ("gh", github.argv_events(ISSUE, 1)[1:]),
+        ("gh", github.argv_approval_events(ISSUE)[1:]),
         ("gh", github.argv_project_items(ISSUE)[1:]),
         ("git", git),
         ("orca-ide", launch_argv_literal("ORCA", watcher.config.worktree)[1:]),
diff --git a/tests/issue_watch/test_crash_injection.py b/tests/issue_watch/test_crash_injection.py
index a58d43d77..fe8eeb61d 100644
--- a/tests/issue_watch/test_crash_injection.py
+++ b/tests/issue_watch/test_crash_injection.py
@@ -171,7 +171,10 @@ class Rig:
         assert (entry.state, entry.launches, entry.attempts) == ("pending", 1, 0)
         assert (entry.consumed_at, entry.pending_at) == (when, when)
         assert (entry.operation_id, entry.last_reason) == (None, None)
-        assert (entry.approver_id, entry.approval_event_id) == (APPROVER_ID, 2)
+        assert (entry.approver_id, entry.approval_event_id) == (
+            APPROVER_ID,
+            int(T_APPROVED.timestamp()),  # a field event's id is its epoch second
+        )
         assert entry.approved_at == T_APPROVED
         assert entry.launch_cwd == str(cfg.worktree)
         assert (entry.launch_login, entry.launch_account_id) == (OWN_LOGIN, OWN_ID)
diff --git a/tests/issue_watch/test_cycle.py b/tests/issue_watch/test_cycle.py
index 79c11b50d..bd475b798 100644
--- a/tests/issue_watch/test_cycle.py
+++ b/tests/issue_watch/test_cycle.py
@@ -102,7 +102,7 @@ def test_load_config_minimal_applies_every_default__fr027(tmp_path, monkeypatch)
     assert config == cycle.Config(
         enabled=False,
         trigger_label="issue-watch:trigger",
-        approval_label="issue-watch:approved",
+        approval_label="issue-field:Approved",
         project_id=PROJECT,
         owner_account_id=None,
         worktree=tmp_path / "wt",
@@ -115,14 +115,14 @@ def test_load_config_fully_populated__fr027(tmp_path):
     path = _write_config(
         tmp_path,
         enabled=True,
-        labels={"trigger": "go", "approval": "ok"},
+        labels={"trigger": "go", "approval": "issue-field:Approved"},
         owner_account_id=42,
         state_dir=str(tmp_path / "state"),
     )
     assert cycle.load_config(path) == cycle.Config(
         enabled=True,
         trigger_label="go",
-        approval_label="ok",
+        approval_label="issue-field:Approved",
         project_id=PROJECT,
         owner_account_id=42,
         worktree=tmp_path / "wt",
@@ -180,11 +180,16 @@ def test_load_config_owner_account_id_bounds_accepted__fr027(tmp_path):
 
 
 def test_load_config_label_of_50_characters_is_accepted__fr027(tmp_path):
-    config = cycle.load_config(
-        _write_config(tmp_path, labels={"trigger": "t" * 50, "approval": "a" * 50})
-    )
+    config = cycle.load_config(_write_config(tmp_path, labels={"trigger": "t" * 50}))
     assert config.trigger_label == "t" * 50
-    assert config.approval_label == "a" * 50
+
+
+def test_load_config_refuses_a_real_approval_label__r35(tmp_path):
+    """R35: the approval is the Approved field; a configured label never approves."""
+    path = _write_config(tmp_path, labels={"approval": "issue-watch:approved"})
+    with pytest.raises(cycle.ConfigError) as caught:
+        cycle.load_config(path)
+    assert caught.value.reason == "config_invalid"
 
 
 def test_load_config_project_id_of_64_characters_is_accepted__fr027(tmp_path):
@@ -223,7 +228,7 @@ INVALID_CONFIGS = [
         id="labels_equal",
     ),
     pytest.param(
-        {"labels": {"trigger": "issue-watch:approved"}},
+        {"labels": {"trigger": "issue-field:Approved"}},
         (),
         "must differ",
         id="trigger_equals_default_approval",
@@ -2396,6 +2401,7 @@ def _trace(world) -> list[str]:
         for page in range(1, github.PAGE_CAP + 1):
             names[tuple(github.argv_events(n, page))] = f"events:{n}"
             names[tuple(github.argv_comments(n, page))] = f"comments:{n}"
+        names[tuple(github.argv_approval_events(n))] = f"approval:{n}"
         names[tuple(github.argv_edits(n))] = f"edits:{n}"
         names[tuple(github.argv_project_items(n))] = f"items:{n}"
         names[tuple(github.argv_reread(n))] = f"reread:{n}"
@@ -2406,10 +2412,26 @@ def _trace(world) -> list[str]:
         elif "skills" in argv:
             out.append("probe")
         else:
-            out.append(names[argv])
+            name = names[argv]
+            # The Approved field events (R35) are part of the events read.
+            if not name.startswith("approval:"):
+                out.append(name)
     return out
 
 
+_APPROVAL_ID = int(T_APPROVED.timestamp())
+"""A field event's id is its time in whole epoch seconds (R35, ``github._field_event``)."""
+
+
+def _approval_calls(world) -> int:
+    """How many Approved field event reads (R35) the cycle made, all issues."""
+    return sum(
+        1
+        for argv, _ in world.runner.calls
+        if argv[0] == "gh" and any("timelineItems" in a for a in argv)
+    )
+
+
 def _reads(world, n) -> list[str]:
     """The per-issue ``gh`` reads made for issue ``n``, in call order."""
     return [t.split(":")[0] for t in _trace(world) if t.endswith(f":{n}")]
@@ -2542,10 +2564,23 @@ SKIP_CASES = [
         id="approver_not_on_the_list",
     ),
     pytest.param(
-        lambda w: w.issue(9, labels=[w.config.trigger_label]),
+        lambda w: w.issue(
+            9,
+            events=[
+                *_ev(w),
+                label_event(
+                    3,
+                    "unlabeled",
+                    w.config.approval_label,
+                    T_APPROVED + timedelta(minutes=1),
+                    actor_id=APPROVER_ID,
+                    actor_login=OWN_LOGIN,
+                ),
+            ],
+        ),
         "not_approved",
         ["comments", "events"],
-        id="approval_label_no_longer_set",
+        id="approval_field_no_longer_set",
     ),
     pytest.param(
         lambda w: w.issue(9, events=_ev(w, trigger=_T_MARK)),
@@ -2699,7 +2734,7 @@ def test_every_per_issue_skip_reason_through_a_whole_cycle__fr005_fr009_fr022(
     assert _reads(world, 9) == reads
     assert not _probed(world)
     assert deps.launcher.calls == []
-    assert _the_cycle_line(lines)["gh_calls"] == 2 + len(reads)
+    assert _the_cycle_line(lines)["gh_calls"] == 2 + len(reads) + _approval_calls(world)
     stored = tmp_state.load()
     assert stored.entries == {}
     assert dict(stored.considered) == {9: CYCLE_NOW}  # a skip is still examined
@@ -2735,7 +2770,80 @@ def test_an_unreadable_issue_skips_and_the_next_one_is_still_examined__fr007_fr0
     assert _entry(tmp_state, 8) is None
     assert _entry(tmp_state, 9).state == "launched"
     assert dict(tmp_state.load().considered) == {8: CYCLE_NOW, 9: CYCLE_NOW}
-    assert _the_cycle_line(lines)["gh_calls"] == 2 + len(reads) + 7
+    assert _the_cycle_line(lines)["gh_calls"] == 2 + len(reads) + 7 + _approval_calls(
+        world
+    )
+
+
+def test_a_real_label_named_issue_watch_approved_never_approves__r35(
+    tmp_path, tmp_state, gh_world
+):
+    """R35: only the Approved field approves; the old label by an approver does not."""
+    world = gh_world()
+    events = [
+        *_ev(world, approval=None),
+        label_event(
+            2,
+            "labeled",
+            "issue-watch:approved",
+            T_APPROVED,
+            actor_id=APPROVER_ID,
+            actor_login=OWN_LOGIN,
+        ),
+    ]
+    world.issue(9, events=events)
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "not_approved")]
+    assert deps.launcher.calls == []
+
+
+def test_a_bot_setting_the_approved_field_never_approves__r35(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    events = _ev(world)
+    events[-1].update(actor_type="Bot", actor_login="approver-app[bot]")
+    world.issue(9, events=events)
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "not_approved")]
+    assert deps.launcher.calls == []
+
+
+def test_the_approval_time_is_the_latest_approved_event__r35(
+    tmp_path, tmp_state, gh_world
+):
+    """A foreign comment between two sets is before the latest approval: it launches."""
+    world = gh_world()
+    later = T_APPROVED + timedelta(minutes=10)
+    events = [
+        *_ev(world),
+        label_event(
+            3,
+            "unlabeled",
+            world.config.approval_label,
+            T_APPROVED + timedelta(minutes=3),
+            actor_id=APPROVER_ID,
+            actor_login=OWN_LOGIN,
+        ),
+        label_event(
+            4,
+            "labeled",
+            world.config.approval_label,
+            later,
+            actor_id=APPROVER_ID,
+            actor_login=OWN_LOGIN,
+        ),
+    ]
+    comment = {
+        "id": 1,
+        "author": "someone-else",
+        "created_at": T_APPROVED + timedelta(minutes=5),
+        "edited_at": None,
+    }
+    world.issue(9, events=events, edits={"comments": [comment]})
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
+    assert _entry(tmp_state, 9).approved_at == later
 
 
 def test_a_marker_read_failure_never_counts_as_claimed__fr009_df02(
@@ -2931,7 +3039,7 @@ def test_an_own_claim_marker_gives_claimed_and_no_launch__ac5_fr009(
         decision["approver_id"],
         decision["approval_event_id"],
         decision["approved_at"],
-    ) == (APPROVER_ID, 2, "2026-11-07T12:02:00Z")
+    ) == (APPROVER_ID, _APPROVAL_ID, "2026-11-07T12:02:00Z")
     assert _reads(world, 9) == ["comments", "events"]  # claimed before the edit reads
     assert not _probed(world)
     assert deps.launcher.calls == []
@@ -2941,7 +3049,7 @@ def test_an_own_claim_marker_gives_claimed_and_no_launch__ac5_fr009(
     assert entry.last_reason == "claimed"
     assert (entry.approver_id, entry.approval_event_id, entry.approved_at) == (
         APPROVER_ID,
-        2,
+        _APPROVAL_ID,
         T_APPROVED,
     )
     assert tmp_state.load().last_completed_cycle_at == CYCLE_NOW
@@ -3039,7 +3147,7 @@ def test_a_failed_entry_with_a_marker_after_the_approval_becomes_claimed__ac5_fr
     assert (entry.consumed_at, entry.pending_at) == (None, None)
     assert (entry.approver_id, entry.approval_event_id, entry.approved_at) == (
         APPROVER_ID,
-        2,
+        _APPROVAL_ID,
         T_APPROVED,
     )
     assert deps.launcher.calls == []
@@ -3067,7 +3175,7 @@ def test_a_tombstone_with_an_own_marker_after_the_approval_becomes_claimed__df43
     assert (entry.consumed_at, entry.last_reason) == (None, "claimed")
     assert (entry.approver_id, entry.approval_event_id, entry.approved_at) == (
         APPROVER_ID,
-        2,
+        _APPROVAL_ID,
         T_APPROVED,
     )
     assert deps.launcher.calls == []
@@ -3170,7 +3278,7 @@ def test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_f
     assert stored_at_origin == [{}, {}]
     # Every read and probe call is done when the launch call starts.
     ((entries, calls_at_launch),) = seen
-    assert calls_at_launch == len(_LAUNCH_TRACE)
+    assert calls_at_launch == len(_LAUNCH_TRACE) + _approval_calls(world)
     assert entries == {
         "9": {
             "issue": 9,
@@ -3179,7 +3287,7 @@ def test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_f
             "launches": 1,
             "operation_id": None,
             "approver_id": APPROVER_ID,
-            "approval_event_id": 2,
+            "approval_event_id": _APPROVAL_ID,
             "approved_at": "2026-11-07T12:02:00Z",
             "launch_cwd": str(world.config.worktree),
             "launch_login": OWN_LOGIN,
@@ -3193,7 +3301,8 @@ def test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_f
         }
     }
     assert launcher.calls == [(ORCA_PATH, str(world.config.worktree), _CLAIM_9, 120.0)]
-    assert world.runner.timeouts[_LAUNCH_TRACE.index("probe")] == 10.0
+    probe_at = next(i for i, (a, _) in enumerate(world.runner.calls) if "skills" in a)
+    assert world.runner.timeouts[probe_at] == 10.0
     entry = _entry(tmp_state, 9)
     assert (entry.state, entry.operation_id, entry.launches) == (
         "launched",
@@ -3205,8 +3314,11 @@ def test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_f
     lines = _lines_of(tmp_state, res)
     (decision,) = _of_kind(lines, "decision")
     assert (decision["reason"], decision["state"]) == ("launched", "launched")
-    assert (decision["approver_id"], decision["approval_event_id"]) == (APPROVER_ID, 2)
-    assert _the_cycle_line(lines)["gh_calls"] == 9
+    assert (decision["approver_id"], decision["approval_event_id"]) == (
+        APPROVER_ID,
+        _APPROVAL_ID,
+    )
+    assert _the_cycle_line(lines)["gh_calls"] == 9 + _approval_calls(world)
     assert tmp_state.load().last_completed_cycle_at == CYCLE_NOW
 
 
@@ -3596,8 +3708,8 @@ def test_a_refused_reserved_call_gives_budget_exhausted_and_no_entry__fr011_nfr0
     tmp_path, tmp_state, gh_world
 ):
     world = gh_world()
-    world.issues_from(range(1, 8), items=[{"status": "In progress"}])  # 7 x 4 = 28
-    world.issue(8)
+    world.issues_from(range(1, 6), items=[{"status": "In progress"}])  # 5 x 5 = 25
+    world.issue(6)
     padding = [
         label_event(
             100 + i,
@@ -3607,29 +3719,30 @@ def test_a_refused_reserved_call_gives_budget_exhausted_and_no_entry__fr011_nfr0
             actor_id=2001,
             actor_login="issue-author",
         )
-        for i in range(99)
+        for i in range(199)
     ]
-    # The re-read's events call now needs a second page: 33, 34, 35, then refused.
+    # The re-read's events call now needs three pages: 31 (re-read), 32, 33, 34,
+    # the field events 35, then the items re-read is refused.
     _on_nth(
         world,
         "events",
-        8,
+        6,
         2,
-        lambda: world.update(8, events=[*padding, *_ev(world)]),
+        lambda: world.update(6, events=[*padding, *_ev(world)]),
     )
     res, deps = _run(tmp_path, tmp_state, world)
     assert (res.exit_code, res.reason) == (0, "cycle_complete")
     lines = _lines_of(tmp_state, res)
-    assert _decisions(lines)[-1] == (8, "budget_exhausted")
+    assert _decisions(lines)[-1] == (6, "budget_exhausted")
     assert "state" not in _of_kind(lines, "decision")[-1]
     shared = ("user", "discover", "origin", "probe")
     per_issue = [t for t in _trace(world) if t not in shared]
-    assert len(per_issue) == github.CALL_CAP
-    assert _trace(world)[-1] == "events:8"  # the items re-read was refused
+    assert len(per_issue) + _approval_calls(world) == github.CALL_CAP
+    assert _trace(world)[-1] == "events:6"  # the items re-read was refused
     assert _the_cycle_line(lines)["gh_calls"] == github.CALL_CAP + 2
     stored = tmp_state.load()
     assert stored.entries == {}
-    assert sorted(stored.considered) == list(range(1, 8))  # 8 is not stamped
+    assert sorted(stored.considered) == list(range(1, 6))  # 6 is not stamped
     assert deps.launcher.calls == []
 
 
@@ -3722,36 +3835,33 @@ def test_s1_case_a_fifteen_skipping_issues_examine_k_then_the_rest__fr016_df50(
     tmp_path, tmp_state, gh_world
 ):
     world = gh_world()
-    world.issues_from(range(1, 16), items=[{"status": "In progress"}])  # r = 4
+    world.issues_from(range(1, 16), items=[{"status": "In progress"}])  # r = 5 (R35)
     launcher = FakeLauncher()
     res1, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
     lines1 = _lines_of(tmp_state, res1)
-    k = min(10, (github.CALL_CAP - github.RESERVED_CALLS) // 4)
-    assert k == 8
+    k = min(10, (github.CALL_CAP - github.RESERVED_CALLS) // 5)
+    assert k == 6
     assert _decisions(lines1) == [
         *[(n, "project_mismatch") for n in range(1, k + 1)],
-        (9, "budget_exhausted"),
-        (10, "budget_exhausted"),
+        *[(n, "budget_exhausted") for n in range(7, 11)],
     ]
     assert _the_cycle_line(lines1)["gh_calls"] == 2 + 32
     t0 = CYCLE_NOW
     stored = tmp_state.load()
-    assert dict(stored.considered) == {n: t0 for n in range(1, 9)}  # 9, 10 unstamped
+    assert dict(stored.considered) == {n: t0 for n in range(1, 7)}  # 7 to 10 unstamped
 
     world.clock.advance(60)
     t1 = world.clock.now()
     res2, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
     lines2 = _lines_of(tmp_state, res2)
-    # Cycle 2 starts with the 7 never-examined issues, then the oldest examined.
+    # Cycle 2 starts with the 9 never-examined issues, six of which fit.
     assert _decisions(lines2) == [
-        *[(n, "project_mismatch") for n in range(9, 16)],
-        (1, "project_mismatch"),
-        (2, "budget_exhausted"),
-        (3, "budget_exhausted"),
+        *[(n, "project_mismatch") for n in range(7, 13)],
+        *[(n, "budget_exhausted") for n in (13, 14, 15, 1)],
     ]
     assert dict(tmp_state.load().considered) == {
-        **{n: t0 for n in range(2, 9)},
-        **{n: t1 for n in (*range(9, 16), 1)},
+        **{n: t0 for n in range(1, 7)},
+        **{n: t1 for n in range(7, 13)},
     }
     assert launcher.calls == []
     assert tmp_state.load().entries == {}
@@ -3774,7 +3884,7 @@ def test_s1_case_b_fifteen_eligible_issues_examine_and_launch_exactly_one__fr016
     stored = tmp_state.load()
     assert dict(stored.considered) == {1: CYCLE_NOW}  # ... nor stamped
     assert sorted(stored.entries) == [1]
-    assert _the_cycle_line(lines1)["gh_calls"] == 9
+    assert _the_cycle_line(lines1)["gh_calls"] == 9 + _approval_calls(world)
 
     world.clock.advance(60)
     res2, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
@@ -3944,14 +4054,14 @@ def test_a_dry_run_reports_would_launch_and_writes_nothing_but_the_shadow__fr019
         "reason": "launched",
         "issue": 9,
         "approver_id": APPROVER_ID,
-        "approval_event_id": 2,
+        "approval_event_id": _APPROVAL_ID,
         "approved_at": "2026-11-07T12:02:00Z",
     }
     cycle_line = _the_cycle_line(lines)
     assert (cycle_line["dry_run"], cycle_line["exit"], cycle_line["gh_calls"]) == (
         True,
         0,
-        6,
+        7,
     )
     shadow = json.loads((tmp_state.state_dir / "dry-run.json").read_text("utf-8"))
     assert shadow == {
@@ -4154,7 +4264,7 @@ def test_a_failed_entry_is_retried_after_the_backoff_and_the_third_failure_aband
 
     # Cycle 2, 9 min 59 s after the failure: still in backoff, no probe, no re-read.
     world.clock.advance(599)
-    calls = len(world.runner.calls)
+    calls = len(_trace(world))
     two, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
     assert (two.exit_code, two.reason) == (0, "cycle_complete")
     assert _decisions(_lines_of(tmp_state, two)) == [(9, "in_backoff")]
@@ -4169,7 +4279,7 @@ def test_a_failed_entry_is_retried_after_the_backoff_and_the_third_failure_aband
 
     # Cycle 3, exactly 10 minutes after: retried, the second failure.
     world.clock.advance(1)
-    calls = len(world.runner.calls)
+    calls = len(_trace(world))
     three, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
     assert (three.exit_code, three.reason) == (7, "revalidation_transient")
     assert _trace(world)[calls + 3 :] == [
@@ -4206,7 +4316,7 @@ def test_a_failed_entry_is_retried_after_the_backoff_and_the_third_failure_aband
 
     # Cycle 5: the tombstone is never launched, whatever the time.
     world.clock.advance(3600)
-    calls = len(world.runner.calls)
+    calls = len(_trace(world))
     five, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
     assert (five.exit_code, five.reason) == (0, "cycle_complete")
     assert _decisions(_lines_of(tmp_state, five)) == [(9, "already_dispatched")]
@@ -4447,20 +4557,20 @@ def test_ten_skipping_candidates_stop_at_32_calls_and_leave_two_unread__nfr009(
 ):
     assert (github.CALL_CAP, github.RESERVED_CALLS) == (35, 3)
     world = gh_world()
-    world.issues_from(range(1, 11), items=[{"status": "In progress"}])  # r = 4
+    world.issues_from(range(1, 11), items=[{"status": "In progress"}])  # r = 5 (R35)
     res, deps = _run(tmp_path, tmp_state, world)
     lines = _lines_of(tmp_state, res)
     assert _decisions(lines) == [
-        *[(n, "project_mismatch") for n in range(1, 9)],
-        (9, "budget_exhausted"),
-        (10, "budget_exhausted"),
+        *[(n, "project_mismatch") for n in range(1, 7)],
+        *[(n, "budget_exhausted") for n in range(7, 11)],
     ]
-    assert _per_issue_calls(world) == 32  # the cap minus the 3 reserved calls
+    assert _per_issue_calls(world) + _approval_calls(world) == 32  # cap minus 3
     assert _the_cycle_line(lines)["gh_calls"] == 2 + 32
-    for n in range(1, 9):
+    for n in range(1, 7):
         assert _reads(world, n) == _FULL_READS
-    assert _reads(world, 9) == [] and _reads(world, 10) == []
-    assert dict(tmp_state.load().considered) == {n: CYCLE_NOW for n in range(1, 9)}
+    assert _reads(world, 7) == ["comments", "events"]  # the third read is refused
+    assert _reads(world, 8) == [] and _reads(world, 9) == []
+    assert dict(tmp_state.load().considered) == {n: CYCLE_NOW for n in range(1, 7)}
     assert deps.launcher.calls == []
 
 
@@ -4468,25 +4578,25 @@ def test_the_three_reserved_calls_remain_for_the_re_read__nfr009(
     tmp_path, tmp_state, gh_world
 ):
     world = gh_world()
-    world.issues_from(range(1, 8), items=[{"status": "In progress"}])  # 7 x 4 = 28
-    world.issues_from(range(8, 11))  # the 8th candidate is the first eligible one
+    world.issues_from(range(1, 6), items=[{"status": "In progress"}])  # 5 x 5 = 25
+    world.issues_from(range(6, 11))  # the 6th candidate is the first eligible one
     res, deps = _run(tmp_path, tmp_state, world)
     lines = _lines_of(tmp_state, res)
-    assert (res.exit_code, res.launched_issue) == (0, 8)
+    assert (res.exit_code, res.launched_issue) == (0, 6)
     assert _decisions(lines) == [
-        *[(n, "project_mismatch") for n in range(1, 8)],
-        (8, "launched"),
+        *[(n, "project_mismatch") for n in range(1, 6)],
+        (6, "launched"),
     ]
-    # 28 for the seven skips + 4 for the checks of 8 = the 32 allowed, then the
-    # reserved 3 (re-read, events, items) bring the per-issue total to exactly 35.
-    assert _reads(world, 8) == [*_FULL_READS, "reread", "events", "items"]
-    assert _per_issue_calls(world) == 35
-    assert _the_cycle_line(lines)["gh_calls"] == 2 + 35
-    assert _reads(world, 9) == [] and _reads(world, 10) == []
+    # 25 for the five skips + 5 for the checks of 6 = 30 of the 32 allowed, then the
+    # reserved calls (re-read, events, field events, items: 4 here) finish the cycle.
+    assert _reads(world, 6) == [*_FULL_READS, "reread", "events", "items"]
+    assert _per_issue_calls(world) + _approval_calls(world) == 34
+    assert _the_cycle_line(lines)["gh_calls"] == 2 + 34
+    assert _reads(world, 7) == [] and _reads(world, 8) == []
     assert [c[2] for c in deps.launcher.calls] == [
-        "/sc:issue --claim 8 --pipeline none"
+        "/sc:issue --claim 6 --pipeline none"
     ]
-    assert _entry(tmp_state, 8).state == "launched"
+    assert _entry(tmp_state, 6).state == "launched"
 
 
 # ==============================================================================
@@ -4667,11 +4777,13 @@ def test_every_runner_call_of_a_launch_cycle_gets_its_configured_timeout__fr029_
         20.0,  # discover
         20.0,  # comments
         20.0,  # events
+        20.0,  # Approved field events
         20.0,  # edits
         20.0,  # items
         10.0,  # probe
         20.0,  # reread
         20.0,  # events
+        20.0,  # Approved field events
         20.0,  # items
         10.0,  # origin
     ]
diff --git a/tests/issue_watch/test_github.py b/tests/issue_watch/test_github.py
index b7cfbf911..f7109e7fc 100644
--- a/tests/issue_watch/test_github.py
+++ b/tests/issue_watch/test_github.py
@@ -42,7 +42,12 @@ MARKER_JQ = (
     "[.[] | {id, login: .user.login, created_at, updated_at, "
     'marker: (.body | contains("<!-- sc:issue:claim -->"))}]'
 )
-REREAD_JQ = "{number, state, labels: [.labels[].name], assignees: [.assignees[].login]}"
+REREAD_JQ = (
+    "{number, state, labels: ([.labels[].name] + [.issue_field_values[]? | "
+    'select(.issue_field_name == "Approved" and '
+    '.single_select_option.name == "Yes") | "issue-field:Approved"]), '
+    "assignees: [.assignees[].login]}"
+)
 
 # The two GraphQL drafts, written out literally (plan step 3.6): a change to the
 # page size, a field name or the paging block in github.py must fail a test.
@@ -579,7 +584,7 @@ def test_user_reads_login_id_and_date_from_the_g1_fixture__fr002(fake_runner) ->
 def test_every_assumed_shape_fixture_parses_and_is_labelled() -> None:
     """Stands in for the check-json hook that is not installed locally."""
     files = sorted(FIXTURES.glob("*.json"))
-    assert len(files) == 19
+    assert len(files) == 20
     for path in files:
         data = json.loads(path.read_text(encoding="utf-8"))
         assert data["_assumed_shape"] is True, path.name
@@ -1526,6 +1531,116 @@ def test_project_item_with_a_null_pipeline_is_none_not_an_error__r34(
     assert (only.pipeline_name, only.pipeline_changed_at) == (None, None)
 
 
+# --- G8: the Approved issue field events (R35) ---------------------------------
+
+
+def field_node(kind: str = "IssueFieldAddedEvent", **over: object) -> dict:
+    """One G8 node; the shape was read from a live issue on 2026-11-19."""
+    node: dict = {
+        "__typename": kind,
+        "createdAt": STAMP,
+        "actor": {"__typename": "User", "login": "ironbelly", "databaseId": 7361222},
+        "issueField": {"name": "Approved"},
+    }
+    if kind == "IssueFieldAddedEvent":
+        node["value"] = "Yes"
+    elif kind == "IssueFieldChangedEvent":
+        node["newValue"] = "Yes"
+    node.update(over)
+    return node
+
+
+def field_page(nodes: list, more: bool = False, cursor: object = None):
+    return gql("timelineItems", nodes, more, cursor)
+
+
+def read_field_events(fake_runner, replies: list):
+    runner = fake_runner(cursor_script(github.argv_approval_events, replies))
+    return github.approval_events(runner, github.CallBudget(), 42, timeout)
+
+
+def test_approval_events_added_yes_by_a_user_is_a_labeled_event__r35(fake_runner):
+    got = read_field_events(fake_runner, [field_page([field_node()])])
+    assert (got.reason, got.kind) == (None, "ok")
+    (event,) = got.value
+    assert (event.event, event.label, event.actor_id, event.actor_type) == (
+        "labeled",
+        "issue-field:Approved",
+        7361222,
+        "User",
+    )
+    assert (event.actor_login, event.created_at) == ("ironbelly", STAMPED)
+    assert event.id == int(STAMPED.timestamp())
+
+
+def test_approval_events_changed_and_removed_follow_the_value__r35(fake_runner):
+    nodes = [
+        field_node("IssueFieldChangedEvent"),
+        field_node("IssueFieldChangedEvent", newValue="No"),
+        field_node("IssueFieldRemovedEvent"),
+    ]
+    got = read_field_events(fake_runner, [field_page(nodes)])
+    assert [e.event for e in got.value] == ["labeled", "unlabeled", "unlabeled"]
+
+
+def test_approval_events_ignore_other_fields_and_keep_a_bot_with_id_zero__r35(
+    fake_runner,
+):
+    nodes = [
+        field_node(issueField={"name": "Complexity"}, value="Simple"),
+        field_node(issueField={}),
+        field_node(actor={"__typename": "Bot", "login": "app[bot]"}),
+        field_node(actor=None),
+    ]
+    got = read_field_events(fake_runner, [field_page(nodes)])
+    assert [(e.actor_id, e.actor_type) for e in got.value] == [(0, "Bot"), (0, None)]
+
+
+@pytest.mark.parametrize(
+    "over",
+    [
+        {"createdAt": None},
+        {"createdAt": "x"},
+        {"__typename": "Surprise"},
+        {"value": None, "__typename": "IssueFieldAddedEvent", "actor": 5},
+    ],
+)
+def test_approval_events_malformed_node_is_unreadable__r35(fake_runner, over):
+    got = read_field_events(fake_runner, [field_page([field_node(**over)])])
+    assert (got.value, got.reason) == (None, "events_unreadable")
+
+
+def test_approval_events_missing_actor_key_is_unreadable__r35(fake_runner):
+    node = field_node()
+    del node["actor"]
+    got = read_field_events(fake_runner, [field_page([node])])
+    assert (got.value, got.reason) == (None, "events_unreadable")
+
+
+def test_approval_events_repeated_end_cursor_is_incomplete__r35(fake_runner):
+    replies = [
+        field_page([field_node()], True, "c1"),
+        field_page([field_node()], True, "c1"),
+    ]
+    got = read_field_events(fake_runner, replies)
+    assert (got.value, got.reason) == (None, "events_unreadable")
+
+
+def test_approval_events_read_the_recorded_shape_fixture__r35(fake_runner):
+    payload = load("graphql_issue_field_events.json")["payload"]
+    argv = tuple(github.argv_approval_events(42))
+    runner = fake_runner({argv: ok(payload, argv)})
+    got = github.approval_events(runner, github.CallBudget(), 42, timeout)
+    assert [(e.event, e.actor_id) for e in got.value] == [("labeled", 7361222)]
+
+
+def test_reread_projection_shows_an_approved_yes_field_as_the_pseudo_label__r35():
+    """REREAD_JQ turns ``Approved`` = ``Yes`` into the pseudo label (jq is not run here)."""
+    assert '"issue-field:Approved"' in github.REREAD_JQ
+    assert '.issue_field_name == "Approved"' in github.REREAD_JQ
+    assert '.single_select_option.name == "Yes"' in github.REREAD_JQ
+
+
 @pytest.mark.parametrize(
     "over",
     [
diff --git a/tests/issue_watch/test_security_invariants.py b/tests/issue_watch/test_security_invariants.py
index cc9bc761d..7dbfeb7e3 100644
--- a/tests/issue_watch/test_security_invariants.py
+++ b/tests/issue_watch/test_security_invariants.py
@@ -69,7 +69,11 @@ _TEXT_FIELD = re.compile(r"(?i)\b(?:title|body\w*)\b")
 _REST_PATH = re.compile(
     r"repos/IronbellyOrg/IronClaude/issues/[1-9][0-9]{0,8}(?:/(?:events|comments))?"
 )
-_QUERIES = ("query=" + github.EDITS_QUERY, "query=" + github.PROJECT_ITEMS_QUERY)
+_QUERIES = (
+    "query=" + github.EDITS_QUERY,
+    "query=" + github.PROJECT_ITEMS_QUERY,
+    "query=" + github.APPROVAL_EVENTS_QUERY,
+)
 _T_MARK = T_APPROVED + timedelta(minutes=1)  # a claim marker after the approval
 
 HOSTILE = [
@@ -419,12 +423,14 @@ SCENARIOS = {
         (
             *_START,
             "rest",  # comments (the claim marker)
-            "rest",  # events (the approval)
+            "rest",  # events (the label events)
+            "graphql",  # the Approved field events (the approval, R35)
             "graphql",  # edits
             "graphql",  # project items
             "probe",
             "rest",  # re-read of the issue
             "rest",  # re-read of the events
+            "graphql",  # re-read of the Approved field events
             "graphql",  # re-read of the project items
             "origin",
             "launch",
@@ -436,7 +442,7 @@ SCENARIOS = {
         False,
         0,
         "cycle_complete",
-        (*_START, "rest", "rest"),
+        (*_START, "rest", "rest", "graphql"),
         ((9, "claimed"),),
     ),
     "rate_limited": Scenario(
@@ -447,7 +453,7 @@ SCENARIOS = {
         True,
         0,
         "cycle_complete",
-        (*_START, "rest", "rest", "graphql", "graphql"),
+        (*_START, "rest", "rest", "graphql", "graphql", "graphql"),
         ((9, "launched"),),
     ),
 }
@@ -725,6 +731,7 @@ def test_every_argv_builder_of_the_package_gives_an_allowed_form(tmp_path):
         for cursor in (None, "Y3Vyc29yOnYyOpHOAAAB", "a.b:c-d_e=="):
             expected.append((github.argv_edits(n, cursor), "graphql"))
             expected.append((github.argv_project_items(n, cursor), "graphql"))
+            expected.append((github.argv_approval_events(n, cursor), "graphql"))
         expected.append(
             (launch_argv(ORCA_PATH, worktree, build_claim_prompt(n)), "launch")
         )
@@ -908,7 +915,9 @@ def test_no_string_constant_of_github_py_contains_mutation():
         assert "{owner}" not in value, f"github.{name} holds the {{owner}} placeholder"
 
 
-@pytest.mark.parametrize("name", ["EDITS_QUERY", "PROJECT_ITEMS_QUERY"])
+@pytest.mark.parametrize(
+    "name", ["EDITS_QUERY", "PROJECT_ITEMS_QUERY", "APPROVAL_EVENTS_QUERY"]
+)
 def test_both_graphql_constants_name_the_literal_repository_and_only_read(name):
     query = getattr(github, name)
     assert github.REPO == FORK
diff --git a/tests/issue_watch/fixtures/_assumed_shape/graphql_issue_field_events.json b/tests/issue_watch/fixtures/_assumed_shape/graphql_issue_field_events.json
new file mode 100644
index 000000000..8f1e388e8
--- /dev/null
+++ b/tests/issue_watch/fixtures/_assumed_shape/graphql_issue_field_events.json
@@ -0,0 +1,47 @@
+{
+  "_assumed_shape": true,
+  "source": "gh api graphql timelineItems(itemTypes: [ISSUE_FIELD_ADDED_EVENT, ISSUE_FIELD_CHANGED_EVENT, ISSUE_FIELD_REMOVED_EVENT]) on issues 675 and 642 of the fork, read-only, 2026-11-19 (requirement R35)",
+  "note": "The shape is a real capture; the values are trimmed. value and newValue are plain strings, actor.databaseId is an integer.",
+  "payload": {
+    "data": {
+      "repository": {
+        "issue": {
+          "timelineItems": {
+            "nodes": [
+              {
+                "__typename": "IssueFieldAddedEvent",
+                "createdAt": "2026-11-19T18:23:59Z",
+                "actor": {
+                  "__typename": "User",
+                  "login": "ironbelly",
+                  "databaseId": 7361222
+                },
+                "issueField": {
+                  "name": "Approved"
+                },
+                "value": "Yes"
+              },
+              {
+                "__typename": "IssueFieldAddedEvent",
+                "createdAt": "2026-11-19T15:21:58Z",
+                "actor": {
+                  "__typename": "User",
+                  "login": "clayphi",
+                  "databaseId": 193966884
+                },
+                "issueField": {
+                  "name": "Complexity"
+                },
+                "value": "Simple"
+              }
+            ],
+            "pageInfo": {
+              "hasNextPage": false,
+              "endCursor": null
+            }
+          }
+        }
+      }
+    }
+  }
+}


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (Grep, call sites read): approval_label is read by src/superclaude/cli/issue_pipeline/cli.py:228 (_load_stage_inputs passes config.approval_label to stage_predicates.evaluate, unchanged) and src/superclaude/cli/issue_pipeline/stage_predicates.py:147-157 (matches events by label, unchanged). predicates.approval_of (predicates.py) is unchanged and sees field events as label events. cycle.py _reclaim, _examine and _revalidate now call self._events. Full run of tests/issue_watch and tests/issue_pipeline: 2920 passed. Docs that still say "approval label" (docs/designs/issue-watcher*.md, WORKER-CONTRACT.md) belong to Tasks 11 and 26, not this task.

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
