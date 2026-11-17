c55c074cbc068c46a3d004a5d6aeca52b8836d9f
Review one task for spec compliance.

Task brief: ## Task 4: Write the stage predicates for the label and the "approved" comment

Depends on: Task 2

First step, before any predicate is written: record real GitHub responses. Plan rules allow only lower-numbered dependencies, so this is the first step and the first acceptance criterion of this task (no renumbering). Read the issue number from owner input O-1 (`tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md`, one line `ISSUE: <number>`, an issue the owner wrote; never pick one). Save, with read-only GET calls only and the same `gh api` argv shapes that `argv_events`, `argv_comments` (the new comments read of Task 5) and `argv_edits` of src/superclaude/cli/issue_watch/github.py build, the raw responses for that one issue: its comments, its timeline events and the edits GraphQL query. Save them as files under `tests/issue_pipeline/fixtures/recorded/` and write the call list and date in `tests/issue_pipeline/fixtures/recorded/README.md`. The predicate tests below, and the tests of Tasks 5 and 6, then run against those recorded files as well as against hand-built cases, so a wrong field name shows up before the first live test.

Create `src/superclaude/cli/issue_pipeline/stage_predicates.py` and `tests/issue_pipeline/test_stage_predicates.py`. These are pure functions over the evidence types already defined in src/superclaude/cli/issue_watch/predicates.py (`LabelEvent`, `CommentEdit`, `EditEvidence`); the existing `approval_of` and `unchanged_since` are not reused as they are, because `unchanged_since` skips comments written by the host login (predicates.py:253-255) and the coordinator posts the plan reply as that login, so an edited plan reply would go unseen, and `approval_of` orders an approval against the trigger label and the store creation time, not against a plan reply.

Rules the predicates implement, written once here:
- The plan reply is the latest comment by the host login that carries the hidden marker `<!-- sc:stage:plan id=<record-id> plan=<64 hex> -->`. It must be unedited since it was posted, and the plan files must still hash to the marker's value.
- Label channel: the approval label was applied after the plan reply, still applied, the actor is a `User` and not a bot, and the actor is the assignee or in the approvers file. The assignee is a login (`DiscoveredIssue.assignees`, predicates.py:85) and the approvers file holds ids, so the actor's login is compared with the assignee and the actor's id with the file; `LabelEvent` carries both (predicates.py:90-99), while `CommentEdit` carries only the author login (:133-139), so a comment author's id and type come from the Task 5 projection. A Status move is the visible sign of the approval (owner decision 3 of the approval-flow record, answer A): it is read where the code can and reported as `status_seen`, never required, because no code reads who moved a Project Status.
- Comment channel: the comment is exactly `approved` or `approved <record-id> plan-sha256=<hash>`; its author is the issue assignee or a listed approver, is a `User` and not a bot, and every other commenter is ignored because the repository is public; it was created after the latest plan reply; it has never been edited; the long form's hash equals the latest plan reply's hash; the short form binds by position to the latest plan reply's hash. A comment created before a newer plan reply never counts for the newer plan.
- Both channels map to the same key (issue, stage, plan hash), so Task 3 can return one row for both.
- Revocation: removing the approval label after the record exists is a revocation signal; deleting or editing an approving comment is not (the record stands), and a Status move back alone is reported, never acted on.
- Facts that the code cannot check are carried as flags in the result, not hidden: the actor equals the host login (an agent on this host could have posted it, Decision 4), and the assignee is the host login after a claim.

Start condition: can start now.

Acceptance criteria:
- Real fixtures exist before the predicates do: `grep -c "^ISSUE: [1-9][0-9]*$" tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` prints 1, `tests/issue_pipeline/fixtures/recorded/` holds the raw comments, timeline events and edits responses for that issue plus a README with the call list, every call in the README is a GET (or the fixed edits GraphQL query), and `tests/issue_pipeline/test_stage_predicates.py` has at least one test that loads a recorded file. If the O-1 line is missing the executor stops here and picks no issue.
- `tests/issue_pipeline/test_stage_predicates.py` has one test per rule and one negative per clause: bot author, non-assignee non-approver author, comment before the plan reply, comment after a newer plan reply for an older hash, edited comment, edited plan reply, plan file changed after the reply, wrong hash in the long form, label applied then removed, comment text with trailing space.
- A test shows a label and a comment for the same plan produce the same key, and a test shows an approval for plan version A is ignored once plan reply B exists.
- A test shows a label with no Status move is still accepted and reports `status_seen: false`, and a label with a Status move reports `status_seen: true`; neither changes the key.
- A test shows the host-login flag is set when the actor is the host login and the result is still accepted, as Decision 4 states.
- `uv run pytest tests/issue_pipeline/test_stage_predicates.py -v` passes.

AC ids (source order): T4.AC1 = bullet 1 of "Acceptance criteria"; T4.AC2 = bullet 2 of "Acceptance criteria"; T4.AC3 = bullet 3 of "Acceptance criteria"; T4.AC4 = bullet 4 of "Acceptance criteria"; T4.AC5 = bullet 5 of "Acceptance criteria"; T4.AC6 = bullet 6 of "Acceptance criteria"
Global constraints: ## Constraints

- Plan only. The owner approved this plan with fixes on 2026-11-15 and asked for the review changes on the same day; every owner decision in Task 19 is answered, and what stays open are facts the first live test must measure (Task 8), not decisions. Running `/sc:implement` from this plan still needs the owner's separate go. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- This is Plan A of two. It holds only work that can run now, in this file order: Task 16 first (its own branch from origin/master, its own pull request later), then Tasks 1, 2, 8 (a document only), 3, 4, 5, 6, 7 and 19. Task numbers are stable across both plans, so they are not contiguous here. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` text, so the order of the items is the gate. A `Depends on` line names only a task that appears earlier in this file. Plan B lives in its own package folder, `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909-planB/plan-b-gated-tasks.md` (Tasks 20, 9, 10, 11, 12, 13, 14, 15, 17, 18). It opens with an owner-run gate item, the first live test recorded in docs/designs/issue-pipeline-fu1.md, and is not run from this file.
- Archive. Plan B sits in its own package folder, so archiving this plan's folder when it completes does not move Plan B.
- Owner input O-1 (not chosen by this plan): the number of one GitHub issue that the owner wrote, which Task 4 records real GitHub responses for. It is written by the owner into `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` as one line `ISSUE: <number>`. An executor that finds no such line stops at Task 4 and never picks an issue.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers: see Task 19.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Plan B Tasks 13 to 15).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Always stage `.dev/tasks` and the `src/` changes, never `.claude/`; commit only when the owner asks.
- The merged requirements file in the brainstorm folder is not edited by any task; Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.
Start sha: c55c074cbc068c46a3d004a5d6aeca52b8836d9f
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/stage_predicates.py b/src/superclaude/cli/issue_pipeline/stage_predicates.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/stage_predicates.py
@@ -0,0 +1,257 @@
+"""Stage predicates for the plan stage: the approval label and the ``approved`` comment.
+
+Pure functions over the evidence types of ``issue_watch.predicates``
+(``LabelEvent``, ``CommentEdit``, ``EditEvidence``) and one projected-comment type
+defined here (``CommentFact``, filled by the jq projection of ``reads.py``).
+
+The watcher's ``approval_of`` and ``unchanged_since`` are not reused: ``unchanged_since``
+skips comments written by the host login (the coordinator posts the plan reply as that
+login, so an edited plan reply would go unseen), and ``approval_of`` orders an approval
+against the trigger label and the store creation time, not against a plan reply.
+
+Rules, written once:
+
+* The plan reply is the latest comment by the host login that carries the hidden marker
+  ``<!-- sc:stage:plan id=<record-id> plan=<64 hex> -->``. It must be unedited since it
+  was posted, and the plan files must still hash to the marker's value.
+* Label channel: applied after the plan reply, still applied, the actor is a ``User`` (not
+  a bot) and is the assignee (by login) or listed in the approvers file (by id).
+* Comment channel: the whole comment is ``approved`` or the long form; its author is the
+  assignee or a listed approver and a ``User``; every other commenter is ignored (the
+  repository is public); created after the latest plan reply; never edited; a long form
+  carries the latest plan reply's record id and hash; the short form binds by position.
+* Both channels map to the same key (issue, stage, plan hash).
+* Revocation: removing the approval label after it was applied is a revocation signal;
+  deleting or editing an approving comment is not; a Status move back alone is reported.
+* A Status move after the plan reply is the visible sign of approval: reported as
+  ``status_seen``, never required, never part of the key.
+* What the code cannot check is carried as a flag, not hidden: the actor equals the host
+  login (an agent on this host could have posted it, Decision 4), and the assignee is the
+  host login (the case after a claim).
+
+Equal timestamps never count as "after" (fail closed): GitHub times have one-second
+granularity.
+"""
+
+from __future__ import annotations
+
+from collections.abc import Collection, Iterable
+from dataclasses import dataclass
+from datetime import datetime
+
+from superclaude.cli.issue_watch.predicates import CommentEdit, EditEvidence, LabelEvent
+
+STATUS_EVENT = "project_v2_item_status_changed"
+STAGE = "plan"
+
+
+@dataclass(frozen=True)
+class PlanMarker:
+    """The values of a ``<!-- sc:stage:plan id=... plan=... -->`` marker."""
+
+    record_id: str
+    plan_hash: str
+
+
+@dataclass(frozen=True)
+class CommentFact:
+    """One comment reduced to booleans and ids by the jq projection (no text)."""
+
+    id: int
+    author_login: str | None
+    author_id: int | None
+    author_type: str | None
+    created_at: datetime
+    approval_form: str | None  # "short", "long" or None: the whole body matches a form
+    approval_record_id: str | None  # captured from a long form
+    approval_hash: str | None  # captured from a long form
+    plan_marker: PlanMarker | None
+
+
+@dataclass(frozen=True)
+class ChannelResult:
+    accepted: bool
+    reason: str  # a closed word; "ok" when accepted
+    evidence_id: int | None = None  # label event id or comment id
+    actor_id: int | None = None
+    actor_is_host_login: bool = False
+
+
+@dataclass(frozen=True)
+class StageStatus:
+    state: str  # no-plan-reply | plan-reply-invalid | plan-changed | awaiting-approval | approved | revoked
+    plan_reason: str  # ok or the closed reason the plan reply is unusable
+    plan_reply_id: int | None
+    plan_hash: str | None
+    record_id: str | None
+    key: tuple[int, str, str] | None  # (issue, stage, plan hash); the same for both channels
+    label: ChannelResult
+    comment: ChannelResult
+    approved: bool
+    label_revoked: bool
+    status_seen: bool
+    assignee_is_host_login: bool
+
+
+_NONE = ChannelResult(False, "no-plan-reply")
+
+
+def _closed_plan(reason: str, plan_reply_id: int | None = None) -> StageStatus:
+    return StageStatus(
+        state="no-plan-reply" if reason == "no-plan-reply" else "plan-reply-invalid",
+        plan_reason=reason,
+        plan_reply_id=plan_reply_id,
+        plan_hash=None,
+        record_id=None,
+        key=None,
+        label=_NONE,
+        comment=_NONE,
+        approved=False,
+        label_revoked=False,
+        status_seen=False,
+        assignee_is_host_login=False,
+    )
+
+
+def latest_plan_reply(comments: Iterable[CommentFact], host_login: str) -> CommentFact | None:
+    """The latest comment by the host login that carries the plan marker."""
+    candidates = [c for c in comments if c.author_login == host_login and c.plan_marker is not None]
+    return max(candidates, key=lambda c: (c.created_at, c.id), default=None)
+
+
+def _is_allowed_actor(
+    login: str | None, account_id: int | None, assignees: Collection[str], approvers: Collection[int]
+) -> bool:
+    return (login is not None and login in assignees) or (account_id is not None and account_id in approvers)
+
+
+def _edit_of(edits: EditEvidence, comment_id: int) -> CommentEdit | None:
+    return next((e for e in edits.comments if e.database_id == comment_id), None)
+
+
+def _label_channel(
+    reply: CommentFact,
+    events: Iterable[LabelEvent],
+    approval_label: str,
+    assignees: Collection[str],
+    approvers: Collection[int],
+    host_login: str,
+) -> tuple[ChannelResult, bool]:
+    relevant = sorted(
+        (e for e in events if e.label == approval_label and e.event in ("labeled", "unlabeled")),
+        key=lambda e: (e.created_at, e.id),
+    )
+    applied_after = [e for e in relevant if e.event == "labeled" and e.created_at > reply.created_at]
+    if not applied_after:
+        reason = "label-before-plan" if any(e.event == "labeled" for e in relevant) else "no-label"
+        return ChannelResult(False, reason), False
+    latest = applied_after[-1]
+    removed = any(e.event == "unlabeled" and (e.created_at, e.id) > (latest.created_at, latest.id) for e in relevant)
+    if removed:
+        return ChannelResult(False, "label-removed", latest.id, latest.actor_id), True
+    if latest.actor_type != "User":
+        return ChannelResult(False, "actor-not-user", latest.id, latest.actor_id), False
+    if not _is_allowed_actor(latest.actor_login, latest.actor_id, assignees, approvers):
+        return ChannelResult(False, "actor-not-allowed", latest.id, latest.actor_id), False
+    return (
+        ChannelResult(True, "ok", latest.id, latest.actor_id, latest.actor_login == host_login),
+        False,
+    )
+
+
+def _comment_channel(
+    reply: CommentFact,
+    comments: Iterable[CommentFact],
+    edits: EditEvidence,
+    assignees: Collection[str],
+    approvers: Collection[int],
+    host_login: str,
+) -> ChannelResult:
+    assert reply.plan_marker is not None
+    first_reason: str | None = None  # why the latest candidate failed, when none is accepted
+    for comment in sorted(comments, key=lambda c: (c.created_at, c.id), reverse=True):
+        if comment.approval_form is None:
+            continue
+        # Every other commenter is ignored: the repository is public.
+        if comment.author_type != "User" or not _is_allowed_actor(
+            comment.author_login, comment.author_id, assignees, approvers
+        ):
+            first_reason = first_reason or "author-not-allowed"
+            continue
+        failure = _comment_failure(comment, reply, edits)
+        if failure is not None:
+            first_reason = first_reason or failure
+            continue
+        return ChannelResult(True, "ok", comment.id, comment.author_id, comment.author_login == host_login)
+    return ChannelResult(False, first_reason or "no-comment")
+
+
+def _comment_failure(comment: CommentFact, reply: CommentFact, edits: EditEvidence) -> str | None:
+    """The closed reason an otherwise allowed approving comment does not count, or None."""
+    assert reply.plan_marker is not None
+    if comment.created_at <= reply.created_at:
+        return "comment-before-plan"
+    edit = _edit_of(edits, comment.id)
+    if edit is None:
+        return "edit-unknown"
+    if edit.last_edited_at is not None:
+        return "comment-edited"
+    if comment.approval_form == "long" and (
+        comment.approval_hash != reply.plan_marker.plan_hash
+        or comment.approval_record_id != reply.plan_marker.record_id
+    ):
+        return "hash-mismatch"
+    return None
+
+
+def evaluate(
+    issue: int,
+    comments: Iterable[CommentFact],
+    events: Iterable[LabelEvent],
+    edits: EditEvidence,
+    *,
+    plan_hash_now: str | None,
+    host_login: str,
+    assignees: Collection[str],
+    approvers: Collection[int],
+    approval_label: str,
+) -> StageStatus:
+    """Apply the rules to one issue's evidence and return a closed result."""
+    comments = tuple(comments)
+    events = tuple(events)
+    reply = latest_plan_reply(comments, host_login)
+    if reply is None or reply.plan_marker is None:
+        return _closed_plan("no-plan-reply")
+    edit = _edit_of(edits, reply.id)
+    if edit is None:
+        return _closed_plan("plan-reply-edit-unknown", reply.id)
+    if edit.last_edited_at is not None:
+        return _closed_plan("plan-reply-edited", reply.id)
+    marker = reply.plan_marker
+    changed = plan_hash_now is None or plan_hash_now != marker.plan_hash
+    label, revoked = _label_channel(reply, events, approval_label, assignees, approvers, host_login)
+    comment = _comment_channel(reply, comments, edits, assignees, approvers, host_login)
+    status_seen = any(e.event == STATUS_EVENT and e.created_at > reply.created_at for e in events)
+    approved = (label.accepted or comment.accepted) and not changed
+    if changed:
+        state = "plan-changed"
+    elif approved:
+        state = "approved"
+    elif revoked:
+        state = "revoked"
+    else:
+        state = "awaiting-approval"
+    return StageStatus(
+        state=state,
+        plan_reason="plan-changed" if changed else "ok",
+        plan_reply_id=reply.id,
+        plan_hash=marker.plan_hash,
+        record_id=marker.record_id,
+        key=(issue, STAGE, marker.plan_hash),
+        label=label,
+        comment=comment,
+        approved=approved,
+        label_revoked=revoked,
+        status_seen=status_seen,
+        assignee_is_host_login=host_login in assignees,
+    )
diff --git a/tests/issue_pipeline/fixtures/recorded/README.md b/tests/issue_pipeline/fixtures/recorded/README.md
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/fixtures/recorded/README.md
@@ -0,0 +1,16 @@
+# Recorded GitHub responses (plan Task 4, O-1)
+
+Recorded on 2026-11-16 for issue 452 of IronbellyOrg/IronClaude, the one issue the owner named in `OWNER-INPUT.md` (`ISSUE: 452`). The issue is closed and was written by the owner. Every call below is a read-only GET, except the fixed edits GraphQL query (a POST that only reads, as `tests/issue_watch/test_security_invariants.py` already allows). No `jq` projection was passed, so each file is the raw response (pretty-printed with sorted keys; nothing else was changed).
+
+| File | Call (argv shape of `src/superclaude/cli/issue_watch/github.py`) |
+|---|---|
+| `comments-page1.json` | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/452/comments -F per_page=100 -F page=1` (the shape `argv_comments` builds, without its `--jq`) |
+| `events-page1.json` | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/452/events -F per_page=100 -F page=1` (the shape `argv_events` builds, without its `--jq`) |
+| `edits-page1.json` | `gh api graphql -f query=<EDITS_QUERY> -F number=452` (the call `argv_edits(452)` builds; GraphQL, reads only) |
+
+What the files show (field names, for the predicate and read tests):
+
+- A comment has `id`, `user.login`, `user.id`, `user.type`, `created_at`, `updated_at`, `author_association` and `body`.
+- An event has `id`, `event`, `actor.login`, `actor.id`, `actor.type`, `created_at` and, for a label event, `label.name`. This issue's events hold no label event: the kinds seen are `added_to_project_v2`, `project_v2_item_status_changed` (actor type `Bot`), `assigned`, `mentioned`, `subscribed` and `closed`.
+- The edits reply holds `data.repository.issue.lastEditedAt`, and per comment `databaseId`, `author.login`, `createdAt` and `lastEditedAt` (all `null` here: nothing was edited).
+- The recorded issue has no approval label, no plan reply and no `approved` comment, so label and approval-comment cases are covered by hand-built evidence in the tests; a field name still has to match these files, and FU-1 (Task 8) re-checks the label event and the web-editor comment on a live test issue.
diff --git a/tests/issue_pipeline/fixtures/recorded/comments-page1.json b/tests/issue_pipeline/fixtures/recorded/comments-page1.json
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/fixtures/recorded/comments-page1.json
@@ -0,0 +1,143 @@
+[
+  {
+    "author_association": "MEMBER",
+    "body": "## Accuracy check for #452\n\n**Verdict:** current\n\nChecked against `origin/master` at `5dc29d23b15eb7db4ead50623bb409f696a0d7d3`, and the pull requests merged since the issue was opened (0, list truncated: no). GitHub's master branch SHA matches the local origin reference. The scout lists no merged pull requests or changed files since creation, and the default-branch log since `2026-11-08T07:32:18Z` is empty. The issue had no comments when checked.\n\n| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |\n|---|---|---|---|\n| 1 | \"Nothing yet.\" | still true as the issue's initial report; live completion is Not known yet | Issue #452 has no comments or recorded results at inspection. This accuracy check does not certify that no activity occurred outside the issue. |\n| 2 | \"This is a throwaway test issue created on 2026-11-08 to exercise `/sc:issue --claim` end to end\" | still true | GitHub reports creation at `2026-11-08T07:32:18Z`; the title and pick-up note identify a disposable live test. `src/superclaude/commands/issue.md` at commit `5dc29d23b15eb7db4ead50623bb409f696a0d7d3` documents `--claim` and its end-to-end flow. |\n| 3 | \"after PR #449 (every Orca worktree gets an agent)\" and \"PR #449: https://github.com/IronbellyOrg/IronClaude/pull/449\" | still true as the PR's policy and purpose, not a claim that every live check passed | PR #449 exists, is titled \"feat(orca): require an agent on every worktree create\", and merged at `2026-11-08T07:05:30Z`, before the issue. Its merge commit `24d79b7fa5215d5ad27545386f8cd8b1f63ca9a9` is an ancestor of `origin/master`. The PR explicitly documents the claim script's deliberate create-without-agent exception: copy and pending state precede the later agent launch. |\n| 4 | \"`.dev/tasks/done/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/t8-delivery.md` (live checks 1, 3 and 5)\" | still true | The exact file exists at commit `5dc29d23b15eb7db4ead50623bb409f696a0d7d3`. Its \"Pending live checks\" section contains item 1 (claim leaves no plain tab and copies before launch), item 3 (bare create blocked in a governed claim session), and item 5 (`--pipeline none` makes no worktree). These are pending checks, not observed passes. |\n| 5 | \"The claim has been run once and the results are recorded; this issue is then closed.\" | still true as the acceptance condition; completion is Not known yet | Issue #452 was OPEN with no comments when inspected. The linked delivery file identifies the live checks to record; the body does not claim they have already passed. |\n| 6 | \"Do not work on this issue. It exists only for a live test and is closed right after.\" | still true as the scope restriction and intended lifecycle | Issue #452 requests no implementation or product change. Closing follows the live test; the issue being OPEN during this check does not contradict that instruction. |\n\n### Merged pull requests that touch this issue\n\n| PR | Title | Relevant files | Effect on the issue |\n|---|---|---|---|\n| None since creation | None | None | No later merged PR or changed file from the scout requires updating the issue. |\n| #449 (before creation; explicitly linked) | feat(orca): require an agent on every worktree create | `.dev/tasks/done/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/t8-delivery.md`; `src/superclaude/commands/issue.md`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md`; `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | Supplies the policy, claim-flow changes and pending live checks that this disposable issue is intended to exercise. It does not make the issue obsolete. |\n\n<!-- sc:issue:accuracy-check -->\n",
+    "created_at": "2026-11-08T07:35:23Z",
+    "html_url": "https://github.com/IronbellyOrg/IronClaude/issues/452#issuecomment-6718803733",
+    "id": 6718803733,
+    "issue_url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/452",
+    "minimized": null,
+    "node_id": "IC_kwDOPOT5c88AAAABkHjPFQ",
+    "performed_via_github_app": null,
+    "pin": null,
+    "reactions": {
+      "+1": 0,
+      "-1": 0,
+      "confused": 0,
+      "eyes": 0,
+      "heart": 0,
+      "hooray": 0,
+      "laugh": 0,
+      "rocket": 0,
+      "total_count": 0,
+      "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/comments/6718803733/reactions"
+    },
+    "updated_at": "2026-11-08T07:35:23Z",
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/comments/6718803733",
+    "user": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    }
+  },
+  {
+    "author_association": "MEMBER",
+    "body": "## Claimed by @ironbelly\n\n- **ClickUp:** skipped (no_token)\n- **Accuracy check:** current (see the accuracy-check comment on this issue)\n\n### Summary\n\nThis disposable issue exists only to exercise `/sc:issue --claim --pipeline none` after PR #449, record the results, and then close the issue. Nothing is to be implemented.\n\n- **Effort estimate:** 0.5 hours\n- **Complexity:** simple\n- **Type:** feature\n- **First next step:** `/sc:brainstorm \"[TEST] throwaway issue for /sc:issue --claim live check @.dev/issues/452/issue-summary.md\" --depth quick` (written for form only; do not run it)\n\n### Files\n\n- Summary: `.dev/issues/452/issue-summary.md`\n- Next steps: `.dev/issues/452/next-steps.md`\n- Analysis: `.dev/issues/452/analysis/`\n\nThese links are paths in the repository; they open on GitHub only after someone commits and pushes the files.\n\n<!-- sc:issue:claim -->\n",
+    "created_at": "2026-11-08T07:35:24Z",
+    "html_url": "https://github.com/IronbellyOrg/IronClaude/issues/452#issuecomment-6718803883",
+    "id": 6718803883,
+    "issue_url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/452",
+    "minimized": null,
+    "node_id": "IC_kwDOPOT5c88AAAABkHjPqw",
+    "performed_via_github_app": null,
+    "pin": null,
+    "reactions": {
+      "+1": 0,
+      "-1": 0,
+      "confused": 0,
+      "eyes": 0,
+      "heart": 0,
+      "hooray": 0,
+      "laugh": 0,
+      "rocket": 0,
+      "total_count": 0,
+      "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/comments/6718803883/reactions"
+    },
+    "updated_at": "2026-11-08T07:35:24Z",
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/comments/6718803883",
+    "user": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    }
+  },
+  {
+    "author_association": "MEMBER",
+    "body": "## Live check results (2026-11-08, after PR #449)\n\n| Check | Result |\n|---|---|\n| Hook in a real session | A bare `orca worktree create --name hook-check` was blocked by `require-orca-worktree-agent.sh` with the full message; no worktree was made. |\n| Create with an agent | `orca worktree create --name hook-agent-check --agent claude --prompt \"...\" --no-parent` left exactly one terminal, the Claude agent behind the ccsession shim, and no empty tab. The same with `--activate` and with `--setup run`: no extra tab either. |\n| 5: `/sc:issue --claim 452 --pipeline none` | Both comments posted, `next-steps.md` written, no `issue-452` worktree and no `worktree.json`. |\n| 1: default claim, worktree part | `orca_worktree.py worktree` returned `created` with no warning. Orca listed 0 terminals in the new worktree before the launch (the plain tab was closed), and the issue directory was already copied into it. |\n| 1: launch | `launched` with warnings `W-LAUNCH-NOT-CCSESSION` (the shim check found no ccsession text on the screen) and `W-L2-ABSENT` (expected, the L2 layer is not built). The launched agent's tab title carried the `sc-launch-v1` marker. |\n| 3: bare create from the governed agent | The agent ran `orca worktree create --name gov-hook-check` and it was blocked, so no worktree was made. The message shown was from `launch-level-guard.sh`, which blocks any `orca` command in a governed session. So the hook-order question does not arise for governed sessions: the guard already forbids the command. |\n\nOpen item: `W-LAUNCH-NOT-CCSESSION` on the governed launch. The agent's title shows it started, but the shim text was not on the screen when the script checked. Needs a look separately; it is not part of PR #449.\n\nAll test worktrees and agents were removed. Closing this issue.\n",
+    "created_at": "2026-11-08T07:37:46Z",
+    "html_url": "https://github.com/IronbellyOrg/IronClaude/issues/452#issuecomment-6718824242",
+    "id": 6718824242,
+    "issue_url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/452",
+    "minimized": null,
+    "node_id": "IC_kwDOPOT5c88AAAABkHkfMg",
+    "performed_via_github_app": null,
+    "pin": null,
+    "reactions": {
+      "+1": 0,
+      "-1": 0,
+      "confused": 0,
+      "eyes": 0,
+      "heart": 0,
+      "hooray": 0,
+      "laugh": 0,
+      "rocket": 0,
+      "total_count": 0,
+      "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/comments/6718824242/reactions"
+    },
+    "updated_at": "2026-11-08T07:37:46Z",
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/comments/6718824242",
+    "user": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    }
+  }
+]
diff --git a/tests/issue_pipeline/fixtures/recorded/edits-page1.json b/tests/issue_pipeline/fixtures/recorded/edits-page1.json
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/fixtures/recorded/edits-page1.json
@@ -0,0 +1,42 @@
+{
+  "data": {
+    "repository": {
+      "issue": {
+        "comments": {
+          "nodes": [
+            {
+              "author": {
+                "login": "ironbelly"
+              },
+              "createdAt": "2026-11-08T07:35:23Z",
+              "databaseId": 6718803733,
+              "lastEditedAt": null
+            },
+            {
+              "author": {
+                "login": "ironbelly"
+              },
+              "createdAt": "2026-11-08T07:35:24Z",
+              "databaseId": 6718803883,
+              "lastEditedAt": null
+            },
+            {
+              "author": {
+                "login": "ironbelly"
+              },
+              "createdAt": "2026-11-08T07:37:46Z",
+              "databaseId": 6718824242,
+              "lastEditedAt": null
+            }
+          ],
+          "pageInfo": {
+            "endCursor": "Y3Vyc29yOnYyOpHPAAAAAZB5HzI=",
+            "hasNextPage": false
+          }
+        },
+        "createdAt": "2026-11-08T07:32:18Z",
+        "lastEditedAt": null
+      }
+    }
+  }
+}
diff --git a/tests/issue_pipeline/fixtures/recorded/events-page1.json b/tests/issue_pipeline/fixtures/recorded/events-page1.json
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/fixtures/recorded/events-page1.json
@@ -0,0 +1,264 @@
+[
+  {
+    "actor": {
+      "avatar_url": "https://avatars.githubusercontent.com/in/235829?v=4",
+      "events_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/events{/privacy}",
+      "followers_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/followers",
+      "following_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/following{/other_user}",
+      "gists_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/apps/github-project-automation",
+      "id": 113052574,
+      "login": "github-project-automation[bot]",
+      "node_id": "BOT_kgDOBr0Lng",
+      "organizations_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/orgs",
+      "received_events_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/received_events",
+      "repos_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/subscriptions",
+      "type": "Bot",
+      "url": "https://api.github.com/users/github-project-automation%5Bbot%5D",
+      "user_view_type": "public"
+    },
+    "commit_id": null,
+    "commit_url": null,
+    "created_at": "2026-11-08T07:32:20Z",
+    "event": "added_to_project_v2",
+    "id": 35481476426,
+    "node_id": "ATPVTE_lADOPOT5c88AAAABdaV4WM8AAAAIQtxdSg",
+    "performed_via_github_app": null,
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/events/35481476426"
+  },
+  {
+    "actor": {
+      "avatar_url": "https://avatars.githubusercontent.com/in/235829?v=4",
+      "events_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/events{/privacy}",
+      "followers_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/followers",
+      "following_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/following{/other_user}",
+      "gists_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/apps/github-project-automation",
+      "id": 113052574,
+      "login": "github-project-automation[bot]",
+      "node_id": "BOT_kgDOBr0Lng",
+      "organizations_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/orgs",
+      "received_events_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/received_events",
+      "repos_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/subscriptions",
+      "type": "Bot",
+      "url": "https://api.github.com/users/github-project-automation%5Bbot%5D",
+      "user_view_type": "public"
+    },
+    "commit_id": null,
+    "commit_url": null,
+    "created_at": "2026-11-08T07:32:22Z",
+    "event": "project_v2_item_status_changed",
+    "id": 35481478047,
+    "node_id": "PVTISC_lADOPOT5c88AAAABdaV4WM8AAAAIQtxjnw",
+    "performed_via_github_app": null,
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/events/35481478047"
+  },
+  {
+    "actor": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    },
+    "assignee": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    },
+    "assigner": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    },
+    "commit_id": null,
+    "commit_url": null,
+    "created_at": "2026-11-08T07:33:32Z",
+    "event": "assigned",
+    "id": 35481514137,
+    "intent": null,
+    "node_id": "AE_lADOPOT5c88AAAABdaV4WM8AAAAIQtzwmQ",
+    "performed_via_github_app": null,
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/events/35481514137"
+  },
+  {
+    "actor": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    },
+    "commit_id": null,
+    "commit_url": null,
+    "created_at": "2026-11-08T07:35:26Z",
+    "event": "mentioned",
+    "id": 35481572520,
+    "node_id": "MEE_lADOPOT5c88AAAABdaV4WM8AAAAIQt3UqA",
+    "performed_via_github_app": null,
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/events/35481572520"
+  },
+  {
+    "actor": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    },
+    "commit_id": null,
+    "commit_url": null,
+    "created_at": "2026-11-08T07:35:27Z",
+    "event": "subscribed",
+    "id": 35481572737,
+    "node_id": "SE_lADOPOT5c88AAAABdaV4WM8AAAAIQt3VgQ",
+    "performed_via_github_app": null,
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/events/35481572737"
+  },
+  {
+    "actor": {
+      "avatar_url": "https://avatars.githubusercontent.com/u/7361222?v=4",
+      "events_url": "https://api.github.com/users/ironbelly/events{/privacy}",
+      "followers_url": "https://api.github.com/users/ironbelly/followers",
+      "following_url": "https://api.github.com/users/ironbelly/following{/other_user}",
+      "gists_url": "https://api.github.com/users/ironbelly/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/ironbelly",
+      "id": 7361222,
+      "login": "ironbelly",
+      "node_id": "MDQ6VXNlcjczNjEyMjI=",
+      "organizations_url": "https://api.github.com/users/ironbelly/orgs",
+      "received_events_url": "https://api.github.com/users/ironbelly/received_events",
+      "repos_url": "https://api.github.com/users/ironbelly/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/ironbelly/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/ironbelly/subscriptions",
+      "type": "User",
+      "url": "https://api.github.com/users/ironbelly",
+      "user_view_type": "public"
+    },
+    "commit_id": null,
+    "commit_url": null,
+    "created_at": "2026-11-08T07:37:47Z",
+    "event": "closed",
+    "id": 35481644168,
+    "intent": null,
+    "node_id": "CE_lADOPOT5c88AAAABdaV4WM8AAAAIQt7siA",
+    "performed_via_github_app": null,
+    "state_reason": null,
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/events/35481644168"
+  },
+  {
+    "actor": {
+      "avatar_url": "https://avatars.githubusercontent.com/in/235829?v=4",
+      "events_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/events{/privacy}",
+      "followers_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/followers",
+      "following_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/following{/other_user}",
+      "gists_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/gists{/gist_id}",
+      "gravatar_id": "",
+      "html_url": "https://github.com/apps/github-project-automation",
+      "id": 113052574,
+      "login": "github-project-automation[bot]",
+      "node_id": "BOT_kgDOBr0Lng",
+      "organizations_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/orgs",
+      "received_events_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/received_events",
+      "repos_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/repos",
+      "site_admin": false,
+      "starred_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/starred{/owner}{/repo}",
+      "subscriptions_url": "https://api.github.com/users/github-project-automation%5Bbot%5D/subscriptions",
+      "type": "Bot",
+      "url": "https://api.github.com/users/github-project-automation%5Bbot%5D",
+      "user_view_type": "public"
+    },
+    "commit_id": null,
+    "commit_url": null,
+    "created_at": "2026-11-08T07:37:49Z",
+    "event": "project_v2_item_status_changed",
+    "id": 35481645444,
+    "node_id": "PVTISC_lADOPOT5c88AAAABdaV4WM8AAAAIQt7xhA",
+    "performed_via_github_app": null,
+    "url": "https://api.github.com/repos/IronbellyOrg/IronClaude/issues/events/35481645444"
+  }
+]
diff --git a/tests/issue_pipeline/test_stage_predicates.py b/tests/issue_pipeline/test_stage_predicates.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_stage_predicates.py
@@ -0,0 +1,326 @@
+"""Task 4: stage predicates for the approval label and the ``approved`` comment."""
+
+from __future__ import annotations
+
+import json
+import re
+from dataclasses import replace
+from datetime import datetime, timedelta, timezone
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_pipeline import approval_line
+from superclaude.cli.issue_pipeline import stage_predicates as sp
+from superclaude.cli.issue_watch.predicates import (
+    CommentEdit,
+    EditEvidence,
+    LabelEvent,
+    parse_utc,
+)
+
+RECORDED = Path(__file__).parent / "fixtures" / "recorded"
+HOST = "host-login"
+OWNER = "owner-login"
+OWNER_ID = 111
+APPROVER_ID = 222
+LABEL = "plan-approved"
+H_A = "a" * 64
+H_B = "b" * 64
+BASE = datetime(2026, 11, 16, 10, 0, 0, tzinfo=timezone.utc)
+
+
+def at(minutes: int) -> datetime:
+    return BASE + timedelta(minutes=minutes)
+
+
+def rid(h: str, issue: int = 9) -> str:
+    return approval_line.record_id(issue, h)
+
+
+def plan_reply(cid: int, minutes: int, h: str = H_A) -> sp.CommentFact:
+    return sp.CommentFact(cid, HOST, 1, "User", at(minutes), None, None, None, sp.PlanMarker(rid(h), h))
+
+
+def approving(
+    cid: int, minutes: int, text: str = "approved", *, login: str = OWNER, uid: int = OWNER_ID, kind: str = "User"
+) -> sp.CommentFact:
+    form, record, digest = approval_line.parse(text)
+    return sp.CommentFact(cid, login, uid, kind, at(minutes), None if form == "none" else form, record, digest, None)
+
+
+def label_event(eid: int, minutes: int, event: str = "labeled", *, login: str = OWNER, uid: int = OWNER_ID, kind: str = "User") -> LabelEvent:
+    return LabelEvent(eid, event, LABEL, uid, login, kind, at(minutes))
+
+
+def status_event(eid: int, minutes: int) -> LabelEvent:
+    return LabelEvent(eid, sp.STATUS_EVENT, None, 5, "bot", "Bot", at(minutes))
+
+
+def edits_for(*comments: sp.CommentFact, edited: dict[int, int] | None = None) -> EditEvidence:
+    edited = edited or {}
+    rows = tuple(
+        CommentEdit(c.id, c.author_login, c.created_at, at(edited[c.id]) if c.id in edited else None) for c in comments
+    )
+    return EditEvidence(at(-60), None, rows)
+
+
+def run(comments, events=(), *, edited=None, plan_hash_now=H_A, assignees=(OWNER,), approvers=frozenset()) -> sp.StageStatus:
+    return sp.evaluate(
+        9,
+        comments,
+        events,
+        edits_for(*comments, edited=edited),
+        plan_hash_now=plan_hash_now,
+        host_login=HOST,
+        assignees=assignees,
+        approvers=approvers,
+        approval_label=LABEL,
+    )
+
+
+# --- real recorded files ------------------------------------------------------
+
+
+def _recorded(name: str):
+    return json.loads((RECORDED / name).read_text())
+
+
+def _facts_from_raw_comments(raw: list[dict]) -> list[sp.CommentFact]:
+    marker = re.compile(r"<!-- sc:stage:plan id=(ap-[1-9][0-9]*-plan-[0-9a-f]{12}) plan=([0-9a-f]{64}) -->")
+    facts = []
+    for c in raw:
+        form, record, digest = approval_line.parse(c["body"])
+        found = marker.search(c["body"])
+        facts.append(
+            sp.CommentFact(
+                c["id"],
+                c["user"]["login"],
+                c["user"]["id"],
+                c["user"]["type"],
+                parse_utc(c["created_at"]),
+                None if form == "none" else form,
+                record,
+                digest,
+                sp.PlanMarker(found.group(1), found.group(2)) if found else None,
+            )
+        )
+    return facts
+
+
+def _events_from_raw(raw: list[dict]) -> list[LabelEvent]:
+    return [
+        LabelEvent(
+            e["id"],
+            e["event"],
+            (e.get("label") or {}).get("name"),
+            (e.get("actor") or {}).get("id"),
+            (e.get("actor") or {}).get("login"),
+            (e.get("actor") or {}).get("type"),
+            parse_utc(e["created_at"]),
+        )
+        for e in raw
+    ]
+
+
+def _edits_from_raw(raw: dict) -> EditEvidence:
+    issue = raw["data"]["repository"]["issue"]
+    nodes = issue["comments"]["nodes"]
+    last = lambda v: parse_utc(v) if v else None  # noqa: E731
+    return EditEvidence(
+        parse_utc(issue["createdAt"]),
+        last(issue["lastEditedAt"]),
+        tuple(CommentEdit(n["databaseId"], (n["author"] or {}).get("login"), parse_utc(n["createdAt"]), last(n["lastEditedAt"])) for n in nodes),
+    )
+
+
+def test_recorded_files_load_and_a_plan_less_issue_has_no_plan_reply() -> None:
+    comments = _facts_from_raw_comments(_recorded("comments-page1.json"))
+    events = _events_from_raw(_recorded("events-page1.json"))
+    edits = _edits_from_raw(_recorded("edits-page1.json"))
+    assert comments and events and edits.comments  # real fields were found under the names used here
+    status = sp.evaluate(
+        452, comments, events, edits, plan_hash_now=None, host_login="ironbelly", assignees=("ironbelly",),
+        approvers=frozenset(), approval_label=LABEL,
+    )
+    assert (status.state, status.approved, status.key) == ("no-plan-reply", False, None)
+    assert {e.actor_type for e in events} == {"Bot", "User"}  # the Bot/User field name is the real one
+
+
+def test_recorded_comments_join_the_recorded_edits_by_database_id() -> None:
+    comments = _facts_from_raw_comments(_recorded("comments-page1.json"))
+    edits = _edits_from_raw(_recorded("edits-page1.json"))
+    assert {c.id for c in comments} == {e.database_id for e in edits.comments}
+
+
+# --- rules, one test each ------------------------------------------------------
+
+
+def test_no_plan_reply_yet() -> None:
+    status = run([approving(1, 5)])
+    assert (status.state, status.plan_reason, status.key) == ("no-plan-reply", "no-plan-reply", None)
+
+
+def test_plan_reply_and_no_approval_is_awaiting() -> None:
+    status = run([plan_reply(10, 0)])
+    assert status.state == "awaiting-approval" and not status.approved
+    assert status.key == (9, "plan", H_A) and status.record_id == rid(H_A)
+    assert (status.label.reason, status.comment.reason) == ("no-label", "no-comment")
+
+
+def test_the_plan_reply_is_the_latest_host_comment_with_the_marker() -> None:
+    other = replace(plan_reply(11, 3), author_login="someone-else")  # not the host login: ignored
+    status = run([plan_reply(10, 0), plan_reply(12, 2, H_B), other], plan_hash_now=H_B)
+    assert status.plan_reply_id == 12 and status.plan_hash == H_B
+
+
+def test_label_channel_accepts_after_the_plan_reply() -> None:
+    status = run([plan_reply(10, 0)], [label_event(1, 2)])
+    assert (status.state, status.label.accepted, status.label.reason) == ("approved", True, "ok")
+    assert status.label.evidence_id == 1 and status.label.actor_id == OWNER_ID
+
+
+def test_label_by_an_approver_id_is_accepted() -> None:
+    event = label_event(1, 2, login="approver-login", uid=APPROVER_ID)
+    status = run([plan_reply(10, 0)], [event], approvers=frozenset({APPROVER_ID}))
+    assert status.label.accepted
+
+
+def test_comment_channel_accepts_the_short_and_the_long_form() -> None:
+    assert run([plan_reply(10, 0), approving(11, 2)]).comment.accepted
+    long_text = f"approved {rid(H_A)} plan-sha256={H_A}"
+    assert run([plan_reply(10, 0), approving(11, 2, long_text)]).comment.accepted
+
+
+def test_label_and_comment_for_the_same_plan_give_the_same_key() -> None:
+    by_label = run([plan_reply(10, 0)], [label_event(1, 2)])
+    by_comment = run([plan_reply(10, 0), approving(11, 2)])
+    both = run([plan_reply(10, 0), approving(11, 2)], [label_event(1, 3)])
+    assert by_label.key == by_comment.key == both.key == (9, "plan", H_A)
+    assert both.label.accepted and both.comment.accepted and both.state == "approved"
+
+
+def test_an_approval_for_plan_version_a_is_ignored_once_plan_reply_b_exists() -> None:
+    comments = [plan_reply(10, 0, H_A), approving(11, 2), plan_reply(12, 5, H_B)]
+    status = run(comments, [label_event(1, 3)], plan_hash_now=H_B)
+    assert status.plan_hash == H_B and status.key == (9, "plan", H_B)
+    assert not status.label.accepted and status.label.reason == "label-before-plan"
+    assert not status.comment.accepted and status.comment.reason == "comment-before-plan"
+    assert status.state == "awaiting-approval"
+
+
+# --- one negative per clause ---------------------------------------------------
+
+
+def test_bot_author_is_ignored_on_both_channels() -> None:
+    bot_comment = approving(11, 2, login=OWNER, kind="Bot")
+    status = run([plan_reply(10, 0), bot_comment], [label_event(1, 2, kind="Bot")])
+    assert not status.comment.accepted and status.comment.reason == "author-not-allowed"
+    assert not status.label.accepted and status.label.reason == "actor-not-user"
+
+
+def test_a_commenter_who_is_neither_assignee_nor_approver_is_ignored() -> None:
+    stranger = approving(11, 2, login="stranger", uid=999)
+    status = run([plan_reply(10, 0), stranger], [label_event(1, 2, login="stranger", uid=999)])
+    assert (status.comment.accepted, status.comment.reason) == (False, "author-not-allowed")
+    assert (status.label.accepted, status.label.reason) == (False, "actor-not-allowed")
+
+
+def test_comment_before_the_plan_reply_does_not_count() -> None:
+    status = run([approving(11, 1), plan_reply(10, 2)])
+    assert not status.comment.accepted and status.comment.reason == "comment-before-plan"
+
+
+def test_equal_timestamps_do_not_count_as_after() -> None:
+    status = run([plan_reply(10, 2), approving(11, 2)], [label_event(1, 2)])
+    assert not status.comment.accepted and not status.label.accepted
+
+
+def test_a_long_form_for_an_older_hash_after_a_newer_plan_reply_is_refused() -> None:
+    old_long = f"approved {rid(H_A)} plan-sha256={H_A}"
+    status = run([plan_reply(10, 0, H_A), plan_reply(12, 1, H_B), approving(11, 2, old_long)], plan_hash_now=H_B)
+    assert status.comment.reason == "hash-mismatch" and not status.comment.accepted
+
+
+def test_wrong_hash_in_the_long_form() -> None:
+    wrong = f"approved {rid(H_A)} plan-sha256={H_B}"
+    assert run([plan_reply(10, 0), approving(11, 2, wrong)]).comment.reason == "hash-mismatch"
+
+
+def test_edited_approving_comment_does_not_count() -> None:
+    status = run([plan_reply(10, 0), approving(11, 2)], edited={11: 4})
+    assert not status.comment.accepted and status.comment.reason == "comment-edited"
+
+
+def test_missing_edit_evidence_fails_closed() -> None:
+    comments = [plan_reply(10, 0), approving(11, 2)]
+    status = sp.evaluate(
+        9, comments, (), EditEvidence(at(-60), None, edits_for(comments[0]).comments), plan_hash_now=H_A,
+        host_login=HOST, assignees=(OWNER,), approvers=frozenset(), approval_label=LABEL,
+    )
+    assert status.comment.reason == "edit-unknown" and not status.approved
+
+
+def test_edited_plan_reply_is_unusable_even_when_the_host_login_wrote_it() -> None:
+    status = run([plan_reply(10, 0), approving(11, 2)], edited={10: 1})
+    assert (status.state, status.plan_reason, status.approved) == ("plan-reply-invalid", "plan-reply-edited", False)
+
+
+def test_plan_files_changed_after_the_reply() -> None:
+    status = run([plan_reply(10, 0), approving(11, 2)], [label_event(1, 3)], plan_hash_now=H_B)
+    assert (status.state, status.plan_reason, status.approved) == ("plan-changed", "plan-changed", False)
+    assert run([plan_reply(10, 0)], plan_hash_now=None).state == "plan-changed"
+
+
+def test_label_applied_then_removed_is_a_revocation() -> None:
+    status = run([plan_reply(10, 0)], [label_event(1, 2), label_event(2, 4, "unlabeled")])
+    assert (status.state, status.label_revoked, status.label.reason) == ("revoked", True, "label-removed")
+
+
+def test_a_comment_approval_stands_when_the_label_is_removed() -> None:
+    status = run([plan_reply(10, 0), approving(11, 2)], [label_event(1, 2), label_event(2, 4, "unlabeled")])
+    assert status.approved and status.label_revoked and status.state == "approved"
+
+
+def test_label_applied_again_after_removal_counts_again() -> None:
+    events = [label_event(1, 2), label_event(2, 3, "unlabeled"), label_event(3, 4)]
+    assert run([plan_reply(10, 0)], events).label.accepted
+
+
+def test_deleting_an_approving_comment_is_not_a_revocation() -> None:
+    gone = run([plan_reply(10, 0)])  # the comment no longer exists: the predicates see no approval, no revoke signal
+    assert gone.state == "awaiting-approval" and not gone.label_revoked
+
+
+@pytest.mark.parametrize("text", ["approved ", " approved", "approved\n", "Approved", "approved.", "> approved", "I approved"])
+def test_comment_text_that_is_not_exactly_an_approval_form_never_approves(text: str) -> None:
+    assert not run([plan_reply(10, 0), approving(11, 2, text)]).comment.accepted
+
+
+# --- Status move and host-login flags ------------------------------------------
+
+
+def test_label_with_no_status_move_is_accepted_with_status_seen_false() -> None:
+    status = run([plan_reply(10, 0)], [label_event(1, 2)])
+    assert status.approved and status.status_seen is False
+
+
+def test_label_with_a_status_move_reports_status_seen_true_and_the_same_key() -> None:
+    plain = run([plan_reply(10, 0)], [label_event(1, 2)])
+    moved = run([plan_reply(10, 0)], [label_event(1, 2), status_event(2, 3)])
+    assert moved.approved and moved.status_seen is True and moved.key == plain.key
+
+
+def test_a_status_move_before_the_plan_reply_is_not_seen_and_never_approves_alone() -> None:
+    status = run([plan_reply(10, 5)], [status_event(2, 3)])
+    assert status.status_seen is False and not status.approved
+    assert run([plan_reply(10, 0)], [status_event(2, 3)]).approved is False
+
+
+def test_the_host_login_flag_is_set_and_the_approval_is_still_accepted() -> None:
+    by_label = run([plan_reply(10, 0)], [label_event(1, 2, login=HOST)], assignees=(HOST,))
+    assert by_label.approved and by_label.label.actor_is_host_login and by_label.assignee_is_host_login
+    by_comment = run([plan_reply(10, 0), approving(11, 2, login=HOST)], assignees=(HOST,))
+    assert by_comment.approved and by_comment.comment.actor_is_host_login
+    plain = run([plan_reply(10, 0)], [label_event(1, 2)])
+    assert not plain.label.actor_is_host_login and not plain.assignee_is_host_login

Codegraph context
index_state: fresh
checked_at: 2026-11-16T21:51:31Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: ran on the Grep/Read floor.

Note for the reviewer: the owner input file tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md was written by the owner session (content ISSUE: 452) and is not part of the diff; the recorded files were fetched with read-only GET calls on 2026-11-16.
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
