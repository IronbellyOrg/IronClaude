53a5007d42628bd0ce82b1bd6a387ebc3cc2a16f
Review one task for spec compliance.

Task brief: ## Task 15: Pass the repo into the GitHub reads and the coordinator's stage evidence read

Depends on: Task 3, Task 14

First read the DF-14 rationale (the research file that `tests/issue_watch/test_security_invariants.py` line 919 cites) and stop if it forbids non-null variables outright. In `src/superclaude/cli/issue_watch/github.py`, replace the module constant use of `REPO` (line 37; used at lines 187, 208 and 259) and the hard-coded owner and name inside `EDITS_QUERY` (line 74) and `PROJECT_ITEMS_QUERY` (line 88) with a `repo` parameter (`owner/name`) on `argv_discover`, `_argv_rest_page`, `argv_events` (line 218), `argv_comments` (line 223), `_argv_graphql`, `argv_edits`, `argv_project_items`, `argv_reread` and on the public reads `discover`, `events`, `marker_comments`, `edits`, `project_items` and `reread`. GraphQL queries take `$owner` and `$name` as variables, declared `String!` because `repository(owner:, name:)` needs non-null values; the cursor `$after` stays nullable. Keep `REPO` as the default value of the `github.py` functions so the watcher's own tests keep working unchanged, but `src/superclaude/cli/issue_pipeline/reads.py` takes no default: `read_stage_evidence` and the comments read (`argv_comments_projected`, `reads.py` lines 65 to 67) get a required `repo` parameter that they pass to `gh.events`, `gh.edits` and the comments call (`reads.py` lines 142 and 148). Today the coordinator's `stage-status` verb reads IronClaude's issue whatever repo it serves (`src/superclaude/cli/issue_pipeline/cli.py` line 279 calls `gh.reread` with no repo and line 282 calls `read_stage_evidence`; `github.py` line 37 fixes `REPO`), so a coordinator for another repo would judge approvals from the wrong issue. In `cli.py` add `--repo` (strict `owner/name`, required) to `stage-status` (the verb at line 368 and `_stage_status`, lines 266 to 305) and pass it to `gh.reread` and `read_stage_evidence`; Task 16 makes it optional with the config's `repo` as the default. Validate the value with a strict `owner/name` pattern and raise `ValueError` before any call for anything else. The test `tests/issue_watch/test_security_invariants.py` lines 911 to 919 asserts the old literal `repository(owner: "IronbellyOrg", name: "IronClaude")` and the absence of `$owner` and `$name`; rewrite it: `$after: String` stays nullable, the regex `\$(\w+): String!` yields exactly the names owner and name, `query.count("String!") == 2`, no literal repository, no `mutation` and no `subscription`. A default value such as `$owner: String = "IronbellyOrg"` is not used, because a missing variable would silently read the fork.

Acceptance criteria:
- T15.AC1: `tests/issue_watch/test_github.py` shows each argv, `argv_events` and `argv_comments` included, carries the passed repo, and rejects `a/b/c`, an empty string, a value with a space or a leading dash.
- T15.AC2: `tests/issue_watch/test_security_invariants.py` lines 911 to 919 are rewritten as described and pass, and the no-mutation checks on the query constants still pass.
- T15.AC3: `tests/issue_pipeline/test_stage_status.py` and the test file that covers `read_stage_evidence` show that `stage-status` without `--repo` is a usage error (exit 2), that a `--repo` that is not `owner/name` is refused, that with `--repo Other/Repo` every argv of the reread, events, edits and comments calls carries `Other/Repo` and none carries `IronbellyOrg/IronClaude`, and that an approval label on the IronClaude issue of the same number never approves the other repo's issue (the fake runner serves different labels per repo).
- T15.AC4: `uv run pytest tests/issue_pipeline tests/issue_watch -q` passes.
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
Start sha: 53a5007d42628bd0ce82b1bd6a387ebc3cc2a16f
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/cli.py b/src/superclaude/cli/issue_pipeline/cli.py
index 4cb43b359..68375c13a 100644
--- a/src/superclaude/cli/issue_pipeline/cli.py
+++ b/src/superclaude/cli/issue_pipeline/cli.py
@@ -312,15 +312,16 @@ def _stage_status(
     approvals_dir: Path | None,
     plan_dir: Path | None,
     plan_names: list[str],
+    repo: str,
 ) -> dict[str, Any]:
     budget = gh.CallBudget()
     login = gh.user(runner, _timeout)
     if login.value is None:
         raise _StatusRefused(login.reason)
-    snapshot = gh.reread(runner, budget, issue, _timeout)
+    snapshot = gh.reread(runner, budget, issue, _timeout, repo=repo)
     if snapshot.value is None:
         raise _StatusRefused(snapshot.reason)
-    evidence = reads.read_stage_evidence(runner, issue, _timeout, budget)
+    evidence = reads.read_stage_evidence(runner, issue, _timeout, budget, repo=repo)
     if evidence.value is None:
         raise _StatusRefused(evidence.reason)
     host = login.value.login
@@ -375,6 +376,12 @@ class _StatusRefused(Exception):
 
 @issue_pipeline_group.command("stage-status")
 @click.argument("issue", type=click.IntRange(min=1))
+@click.option(
+    "--repo",
+    required=True,
+    help="owner/name of the repository the issue belongs to (no default: a coordinator "
+    "for another repository must name it).",
+)
 @click.option(
     "--json",
     "as_json",
@@ -408,6 +415,7 @@ class _StatusRefused(Exception):
 )
 def stage_status_command(
     issue: int,
+    repo: str,
     as_json: bool,
     config_path: Path,
     approvals_dir: Path | None,
@@ -415,6 +423,9 @@ def stage_status_command(
     plan_files: tuple[str, ...],
 ) -> None:
     """Print the plan-stage status of ISSUE as closed keys; writes nothing, prints no GitHub text."""
+    if not gh.valid_repo(repo):
+        click.echo("refused:bad-repo")
+        raise SystemExit(_EXIT_REFUSED)
     try:
         label, approvers = _load_stage_inputs(config_path.expanduser())
     except cycle.ConfigError as exc:
@@ -429,6 +440,7 @@ def stage_status_command(
             approvals_dir,
             plan_dir,
             list(plan_files),
+            repo,
         )
     except _StatusRefused as exc:
         click.echo(f"refused:{exc.reason}")
diff --git a/src/superclaude/cli/issue_pipeline/reads.py b/src/superclaude/cli/issue_pipeline/reads.py
index 4b08990ef..e0e185676 100644
--- a/src/superclaude/cli/issue_pipeline/reads.py
+++ b/src/superclaude/cli/issue_pipeline/reads.py
@@ -66,9 +66,13 @@ _TYPE_RE = re.compile(r"[A-Za-z]{1,20}")
 COMMENTS_UNREADABLE = "comments_unreadable"
 
 
-def argv_comments_projected(n: int, page: int) -> list[str]:
-    """One REST page of the issue's comments, reduced by ``COMMENTS_JQ``."""
-    return _argv_rest_page(n, "comments", page, COMMENTS_JQ)
+def argv_comments_projected(n: int, page: int, repo: str) -> list[str]:
+    """One REST page of the issue's comments in ``repo``, reduced by ``COMMENTS_JQ``.
+
+    ``repo`` has no default here: a coordinator for another repository must name it, so a
+    forgotten value cannot read IronClaude's issue of the same number.
+    """
+    return _argv_rest_page(n, "comments", page, COMMENTS_JQ, repo)
 
 
 def _pattern_or_none(value: object, pattern: re.Pattern[str]) -> str | None:
@@ -109,14 +113,19 @@ def _comment_fact(item: dict) -> CommentFact:
 
 
 def comments(
-    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
+    runner: Runner,
+    budget: CallBudget,
+    n: int,
+    timeout_for: Callable[[], float | None],
+    *,
+    repo: str,
 ) -> Read:
     """A tuple of ``CommentFact`` for the issue's comments; every failure is ``comments_unreadable``."""
     return _rest_read(
         runner,
         budget,
         timeout_for,
-        lambda page: argv_comments_projected(n, page),
+        lambda page: argv_comments_projected(n, page, repo),
         _comment_fact,
         COMMENTS_UNREADABLE,
         COMMENTS_UNREADABLE,
@@ -136,24 +145,28 @@ def read_stage_evidence(
     n: int,
     timeout_for: Callable[[], float | None],
     budget: CallBudget | None = None,
+    *,
+    repo: str,
 ) -> Read:
-    """Read events, comments and edits under one ``CallBudget``.
+    """Read events, comments and edits of ``repo``'s issue under one ``CallBudget``.
 
     Returns ``Read(StageEvidence)``, or the first failed ``Read`` (value None, a closed
-    reason): a partial read never yields an approval.
+    reason): a partial read never yields an approval. ``repo`` is required and is passed to
+    every read; a value that is not ``owner/name`` raises ``ValueError`` before any call.
     """
+    gh._repo_arg(repo)
     budget = budget or CallBudget()
-    events = gh.events(runner, budget, n, timeout_for)
+    events = gh.events(runner, budget, n, timeout_for, repo=repo)
     if events.value is None:
         return events
-    field_events = gh.approval_events(runner, budget, n, timeout_for)
+    field_events = gh.approval_events(runner, budget, n, timeout_for, repo=repo)
     if field_events.value is None:
         return field_events
     merged = merge_approval_events(events.value, field_events.value)  # type: ignore[arg-type]
-    found = comments(runner, budget, n, timeout_for)
+    found = comments(runner, budget, n, timeout_for, repo=repo)
     if found.value is None:
         return found
-    edits = gh.edits(runner, budget, n, timeout_for)
+    edits = gh.edits(runner, budget, n, timeout_for, repo=repo)
     if edits.value is None:
         return edits
     return Read(StageEvidence(found.value, merged, edits.value))  # type: ignore[arg-type]
diff --git a/src/superclaude/cli/issue_watch/github.py b/src/superclaude/cli/issue_watch/github.py
index 5c1432bb2..c14d1e620 100644
--- a/src/superclaude/cli/issue_watch/github.py
+++ b/src/superclaude/cli/issue_watch/github.py
@@ -82,8 +82,8 @@ REREAD_JQ = (
 # [PROPOSAL, UNVERIFIED] drafts from decision DF-14 (research 06, Table 1.5).
 # Field names follow the public schema; reply shapes are unverified (FU-1, FU-3).
 
-EDITS_QUERY = """query($number: Int!, $after: String) {
-  repository(owner: "IronbellyOrg", name: "IronClaude") {
+EDITS_QUERY = """query($owner: String!, $name: String!, $number: Int!, $after: String) {
+  repository(owner: $owner, name: $name) {
     issue(number: $number) {
       createdAt
       lastEditedAt
@@ -96,8 +96,8 @@ EDITS_QUERY = """query($number: Int!, $after: String) {
 }"""
 """G5: issue and comment edit timestamps."""
 
-PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
-  repository(owner: "IronbellyOrg", name: "IronClaude") {
+PROJECT_ITEMS_QUERY = """query($owner: String!, $name: String!, $number: Int!, $after: String) {
+  repository(owner: $owner, name: $name) {
     issue(number: $number) {
       projectItems(first: 100, after: $after) {
         nodes {
@@ -120,8 +120,8 @@ PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
 The item-level ``updatedAt`` is not read: a label or a comment may move it (R33).
 """
 
-APPROVAL_EVENTS_QUERY = """query($number: Int!, $after: String) {
-  repository(owner: "IronbellyOrg", name: "IronClaude") {
+APPROVAL_EVENTS_QUERY = """query($owner: String!, $name: String!, $number: Int!, $after: String) {
+  repository(owner: $owner, name: $name) {
     issue(number: $number) {
       timelineItems(first: 100, after: $after, itemTypes: [ISSUE_FIELD_ADDED_EVENT, ISSUE_FIELD_CHANGED_EVENT, ISSUE_FIELD_REMOVED_EVENT]) {
         nodes {
@@ -195,6 +195,31 @@ def _cursor_args(after: str | None) -> list[str]:
     return ["-f", f"after={after}"]
 
 
+# A strict ``owner/name``: the owner starts with a letter or digit (so no value can start
+# with a dash), the name has no space, slash or leading dash. GitHub's own limits are
+# 39 and 100 characters.
+_REPO_RE = re.compile(
+    r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9._][A-Za-z0-9._-]{0,99}"
+)
+
+
+def valid_repo(value: object) -> bool:
+    """True for a strict ``owner/name`` string."""
+    return (
+        isinstance(value, str)
+        and _REPO_RE.fullmatch(value) is not None
+        and value.split("/")[1] not in (".", "..")
+    )
+
+
+def _repo_arg(repo: object) -> str:
+    """Return ``repo`` when it is a strict ``owner/name``, else raise ``ValueError``."""
+    if not valid_repo(repo):
+        raise ValueError("invalid repository")
+    assert isinstance(repo, str)
+    return repo
+
+
 def _trigger_arg(trigger: object) -> str:
     """Return ``trigger`` when it is safe as one ``--label`` value.
 
@@ -225,14 +250,14 @@ def argv_user() -> list[str]:
     return ["gh", "api", "user", "--include"]
 
 
-def argv_discover(trigger: str, login: str) -> list[str]:
+def argv_discover(trigger: str, login: str, repo: str = REPO) -> list[str]:
     """G2: open issues carrying ``trigger`` and assigned to ``login`` (FR-003)."""
     return [
         "gh",
         "issue",
         "list",
         "--repo",
-        REPO,
+        _repo_arg(repo),
         "--state",
         "open",
         "--label",
@@ -246,14 +271,16 @@ def argv_discover(trigger: str, login: str) -> list[str]:
     ]
 
 
-def _argv_rest_page(n: object, kind: str, page: object, jq: str) -> list[str]:
+def _argv_rest_page(
+    n: object, kind: str, page: object, jq: str, repo: str = REPO
+) -> list[str]:
     """One REST page of ``repos/R/issues/N/<kind>`` projected by ``jq``."""
     return [
         "gh",
         "api",
         "--method",
         "GET",
-        f"repos/{REPO}/issues/{_issue_arg(n)}/{kind}",
+        f"repos/{_repo_arg(repo)}/issues/{_issue_arg(n)}/{kind}",
         "-F",
         f"per_page={PAGE_SIZE}",
         "-F",
@@ -263,53 +290,66 @@ def _argv_rest_page(n: object, kind: str, page: object, jq: str) -> list[str]:
     ]
 
 
-def argv_events(n: int, page: int) -> list[str]:
+def argv_events(n: int, page: int, repo: str = REPO) -> list[str]:
     """G3: one page of the issue's event history (FR-005, FR-006)."""
-    return _argv_rest_page(n, "events", page, EVENTS_JQ)
+    return _argv_rest_page(n, "events", page, EVENTS_JQ, repo)
 
 
-def argv_comments(n: int, page: int) -> list[str]:
+def argv_comments(n: int, page: int, repo: str = REPO) -> list[str]:
     """G4: one page of the issue's comments, reduced to marker evidence (FR-009)."""
-    return _argv_rest_page(n, "comments", page, MARKER_JQ)
+    return _argv_rest_page(n, "comments", page, MARKER_JQ, repo)
 
 
-def _argv_graphql(query: str, n: object, after: str | None) -> list[str]:
-    """One GraphQL page; ``-F`` sends ``number`` typed, no ``after`` sends null."""
+def _argv_graphql(
+    query: str, n: object, after: str | None, repo: str = REPO
+) -> list[str]:
+    """One GraphQL page; ``-F`` sends ``number`` typed, no ``after`` sends null.
+
+    ``owner`` and ``name`` are string variables (the query declares them non-null), so a
+    call that forgets the repository fails instead of reading another one.
+    """
+    owner, name = _repo_arg(repo).split("/")
     return [
         "gh",
         "api",
         "graphql",
         "-f",
         f"query={query}",
+        "-f",
+        f"owner={owner}",
+        "-f",
+        f"name={name}",
         "-F",
         f"number={_issue_arg(n)}",
         *_cursor_args(after),
     ]
 
 
-def argv_edits(n: int, after: str | None = None) -> list[str]:
+def argv_edits(n: int, after: str | None = None, repo: str = REPO) -> list[str]:
     """G5: one page of issue and comment edit timestamps."""
-    return _argv_graphql(EDITS_QUERY, n, after)
+    return _argv_graphql(EDITS_QUERY, n, after, repo)
 
 
-def argv_project_items(n: int, after: str | None = None) -> list[str]:
+def argv_project_items(n: int, after: str | None = None, repo: str = REPO) -> list[str]:
     """G6: one page of the issue's Project items (FR-007)."""
-    return _argv_graphql(PROJECT_ITEMS_QUERY, n, after)
+    return _argv_graphql(PROJECT_ITEMS_QUERY, n, after, repo)
 
 
-def argv_approval_events(n: int, after: str | None = None) -> list[str]:
+def argv_approval_events(
+    n: int, after: str | None = None, repo: str = REPO
+) -> list[str]:
     """G8: one page of the issue's issue-field events (R35)."""
-    return _argv_graphql(APPROVAL_EVENTS_QUERY, n, after)
+    return _argv_graphql(APPROVAL_EVENTS_QUERY, n, after, repo)
 
 
-def argv_reread(n: int) -> list[str]:
+def argv_reread(n: int, repo: str = REPO) -> list[str]:
     """G7: re-read the issue's number, state, labels and assignees (FR-011)."""
     return [
         "gh",
         "api",
         "--method",
         "GET",
-        f"repos/{REPO}/issues/{_issue_arg(n)}",
+        f"repos/{_repo_arg(repo)}/issues/{_issue_arg(n)}",
         "--jq",
         REREAD_JQ,
     ]
@@ -919,7 +959,12 @@ def user(runner: Runner, timeout_for: Callable[[], float | None]) -> Read:
 
 
 def discover(
-    runner: Runner, trigger: str, login: str, timeout_for: Callable[[], float | None]
+    runner: Runner,
+    trigger: str,
+    login: str,
+    timeout_for: Callable[[], float | None],
+    *,
+    repo: str = REPO,
 ) -> Read:
     """G2: a tuple of ``DiscoveredIssue`` (FR-003, FR-004).
 
@@ -928,7 +973,7 @@ def discover(
     ``ValueError`` before any call for a ``trigger`` or ``login`` that is unsafe
     as a command-line value (the cycle checks both first).
     """
-    reply = _call(runner, None, timeout_for, argv_discover(trigger, login))
+    reply = _call(runner, None, timeout_for, argv_discover(trigger, login, repo))
     if reply is None:
         return _SHARED_NO_CALL
     if reply.kind != "ok":
@@ -966,13 +1011,14 @@ def events(
     timeout_for: Callable[[], float | None],
     *,
     reserved: bool = False,
+    repo: str = REPO,
 ) -> Read:
     """G3 (G3' with ``reserved``): a tuple of ``LabelEvent`` (FR-005, FR-006)."""
     return _rest_read(
         runner,
         budget,
         timeout_for,
-        lambda page: argv_events(n, page),
+        lambda page: argv_events(n, page, repo),
         _event,
         "events_unreadable",
         "events_incomplete",
@@ -981,7 +1027,12 @@ def events(
 
 
 def marker_comments(
-    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
+    runner: Runner,
+    budget: CallBudget,
+    n: int,
+    timeout_for: Callable[[], float | None],
+    *,
+    repo: str = REPO,
 ) -> Read:
     """G4: a tuple of ``MarkerEvidence`` for comments with a login (FR-009).
 
@@ -992,7 +1043,7 @@ def marker_comments(
         runner,
         budget,
         timeout_for,
-        lambda page: argv_comments(n, page),
+        lambda page: argv_comments(n, page, repo),
         _marker,
         "marker_unreadable",
         "marker_unreadable",
@@ -1001,14 +1052,19 @@ def marker_comments(
 
 
 def edits(
-    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
+    runner: Runner,
+    budget: CallBudget,
+    n: int,
+    timeout_for: Callable[[], float | None],
+    *,
+    repo: str = REPO,
 ) -> Read:
     """G5: an ``EditEvidence``; every failure is ``edits_unreadable`` (DF-02)."""
     out = _graphql_read(
         runner,
         budget,
         timeout_for,
-        lambda after: argv_edits(n, after),
+        lambda after: argv_edits(n, after, repo),
         "comments",
         _edit_issue,
         _comment_edit,
@@ -1028,6 +1084,7 @@ def project_items(
     timeout_for: Callable[[], float | None],
     *,
     reserved: bool = False,
+    repo: str = REPO,
 ) -> Read:
     """G6 (G6' with ``reserved``): a tuple of ``ProjectItem`` (FR-007).
 
@@ -1038,7 +1095,7 @@ def project_items(
         runner,
         budget,
         timeout_for,
-        lambda after: argv_project_items(n, after),
+        lambda after: argv_project_items(n, after, repo),
         "projectItems",
         lambda issue: None,
         _project_item,
@@ -1055,6 +1112,7 @@ def approval_events(
     timeout_for: Callable[[], float | None],
     *,
     reserved: bool = False,
+    repo: str = REPO,
 ) -> Read:
     """G8: a tuple of ``LabelEvent`` for the ``Approved`` issue field (R35).
 
@@ -1064,7 +1122,7 @@ def approval_events(
         runner,
         budget,
         timeout_for,
-        lambda after: argv_approval_events(n, after),
+        lambda after: argv_approval_events(n, after, repo),
         "timelineItems",
         lambda issue: None,
         _field_event,
@@ -1077,14 +1135,19 @@ def approval_events(
 
 
 def reread(
-    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
+    runner: Runner,
+    budget: CallBudget,
+    n: int,
+    timeout_for: Callable[[], float | None],
+    *,
+    repo: str = REPO,
 ) -> Read:
     """G7: an ``IssueSnapshot`` from one reserved call (FR-011).
 
     A timeout or 5xx is ``revalidation_transient``; any other failure, or a
     reply for another number, is ``revalidation_failed``.
     """
-    reply = _call(runner, budget, timeout_for, argv_reread(n), reserved=True)
+    reply = _call(runner, budget, timeout_for, argv_reread(n, repo), reserved=True)
     if reply is None:
         return _NO_CALL
     if reply.kind != "ok":
diff --git a/tests/issue_pipeline/test_reads.py b/tests/issue_pipeline/test_reads.py
index 6f9208d49..68ba26b72 100644
--- a/tests/issue_pipeline/test_reads.py
+++ b/tests/issue_pipeline/test_reads.py
@@ -14,6 +14,7 @@ from superclaude.cli.issue_watch import github as gh
 from superclaude.cli.issue_watch.runner import CommandResult
 
 RECORDED = Path(__file__).parent / "fixtures" / "recorded"
+REPO = "IronbellyOrg/IronClaude"
 CANARY = "CANARY-9f3a-DO-NOT-LEAK"
 H = "a" * 64
 RID = "ap-9-plan-" + H[:12]
@@ -159,7 +160,7 @@ def test_the_plan_marker_is_read_with_its_hash() -> None:
 
 
 def test_the_new_argv_asks_for_no_body_field() -> None:
-    argv = reads.argv_comments_projected(452, 1)
+    argv = reads.argv_comments_projected(452, 1, REPO)
     assert argv[:5] == [
         "gh",
         "api",
@@ -196,7 +197,7 @@ def test_a_hostile_body_never_reaches_output_argv_result_or_a_file(
     projected = jq(reads.COMMENTS_JQ, raw)
     assert CANARY not in projected
     runner = Served(lambda argv: ok(projected))
-    out = reads.comments(runner, gh.CallBudget(), 452, never_expires)
+    out = reads.comments(runner, gh.CallBudget(), 452, never_expires, repo=REPO)
     assert out.reason is None and len(out.value) == 4
     assert CANARY not in repr(out) and CANARY not in " ".join(
         " ".join(a) for a in runner.argvs
@@ -217,7 +218,7 @@ def test_python_rejects_a_captured_value_that_breaks_its_pattern(field: str) ->
     with pytest.raises(gh._Malformed):
         reads._comment_fact(row)
     served = Served(lambda argv: ok(json.dumps([row])))
-    result = reads.comments(served, gh.CallBudget(), 9, never_expires)
+    result = reads.comments(served, gh.CallBudget(), 9, never_expires, repo=REPO)
     assert result.value is None and result.reason == "comments_unreadable"
 
 
@@ -252,7 +253,7 @@ def test_page_cap_stops_a_comment_read_that_never_ends() -> None:
         return ok(_page(gh.PAGE_SIZE, offset=page * 1000))
 
     runner = Served(answer)
-    result = reads.comments(runner, gh.CallBudget(), 9, never_expires)
+    result = reads.comments(runner, gh.CallBudget(), 9, never_expires, repo=REPO)
     assert result.value is None and result.reason == "comments_unreadable"
     assert len(runner.argvs) == gh.PAGE_CAP
 
@@ -272,7 +273,7 @@ def test_call_cap_is_shared_across_events_comments_and_edits() -> None:
         )
 
     runner = Served(answer)
-    out = reads.read_stage_evidence(runner, 452, never_expires, budget)
+    out = reads.read_stage_evidence(runner, 452, never_expires, budget, repo=REPO)
     assert out.value is None and out.reason == "budget_exhausted"
     assert budget.calls <= gh.CALL_CAP - gh.RESERVED_CALLS
     assert len(runner.argvs) == 2  # the third read never ran
@@ -292,9 +293,11 @@ def test_a_transient_gh_failure_returns_a_closed_reason_not_a_partial_approval()
             return ok(_recorded_events())
         return failed()
 
-    out = reads.read_stage_evidence(Served(answer), 452, never_expires)
+    out = reads.read_stage_evidence(Served(answer), 452, never_expires, repo=REPO)
     assert out.value is None and out.reason == "comments_unreadable"
-    first = reads.read_stage_evidence(Served(lambda argv: failed()), 452, never_expires)
+    first = reads.read_stage_evidence(
+        Served(lambda argv: failed()), 452, never_expires, repo=REPO
+    )
     assert first.value is None and first.reason == "events_unreadable"
 
 
@@ -312,7 +315,7 @@ def test_the_whole_read_over_the_recorded_files_succeeds() -> None:
         assert argv[4].endswith("/comments")
         return ok(jq(reads.COMMENTS_JQ, raw_comments))
 
-    out = reads.read_stage_evidence(Served(answer), 452, never_expires)
+    out = reads.read_stage_evidence(Served(answer), 452, never_expires, repo=REPO)
     assert out.reason is None
     evidence = out.value
     assert (
@@ -320,3 +323,47 @@ def test_the_whole_read_over_the_recorded_files_succeeds() -> None:
         and evidence.events
         and evidence.edits.comments
     )
+
+
+# --- the repository is required and reaches every read (plan Task 15) -----------------
+
+
+def test_read_stage_evidence_and_comments_require_a_repo() -> None:
+    with pytest.raises(TypeError):
+        reads.read_stage_evidence(Served(lambda argv: failed()), 452, never_expires)  # type: ignore[call-arg]
+    with pytest.raises(TypeError):
+        reads.comments(
+            Served(lambda argv: failed()), gh.CallBudget(), 452, never_expires
+        )  # type: ignore[call-arg]
+    with pytest.raises(TypeError):
+        reads.argv_comments_projected(452, 1)  # type: ignore[call-arg]
+
+
+@pytest.mark.parametrize("bad", ["a/b/c", "", "a b/c", "-a/b", "a"])
+def test_a_repo_that_is_not_owner_slash_name_raises_before_any_call(bad: str) -> None:
+    runner = Served(lambda argv: failed())
+    with pytest.raises(ValueError):
+        reads.read_stage_evidence(runner, 452, never_expires, repo=bad)
+    with pytest.raises(ValueError):
+        reads.argv_comments_projected(452, 1, bad)
+    assert runner.argvs == []
+
+
+def test_every_read_of_the_stage_evidence_carries_the_given_repo() -> None:
+    def answer(argv: list[str]) -> CommandResult:
+        if is_timeline(argv):
+            return ok(EMPTY_TIMELINE)
+        if argv[:3] == ["gh", "api", "graphql"]:
+            return ok((RECORDED / "edits-page1.json").read_text())
+        if argv[4].endswith("/events"):
+            return ok(_recorded_events())
+        return ok(_page(0))
+
+    runner = Served(answer)
+    out = reads.read_stage_evidence(runner, 452, never_expires, repo="Other/Repo")
+    assert out.reason is None
+    assert len(runner.argvs) == 4  # events, approval events, comments, edits
+    for argv in runner.argvs:
+        text = "\n".join(argv)
+        assert "IronClaude" not in text and "IronbellyOrg" not in text
+        assert "Other/Repo" in text or ("owner=Other" in argv and "name=Repo" in argv)
diff --git a/tests/issue_pipeline/test_stage_status.py b/tests/issue_pipeline/test_stage_status.py
index 8cd3e85a8..2cb50b17b 100644
--- a/tests/issue_pipeline/test_stage_status.py
+++ b/tests/issue_pipeline/test_stage_status.py
@@ -26,6 +26,8 @@ HOST = "host-login"
 OWNER = "owner-login"
 LABEL = "plan-approved"
 ISSUE = 9
+REPO = "IronbellyOrg/IronClaude"
+OTHER = "Other/Repo"
 CANARY = "CANARY-6e1b-NO-LEAK"
 T0 = "2026-11-16T10:00:00Z"
 T1 = "2026-11-16T10:05:00Z"
@@ -99,9 +101,13 @@ class World:
     """Raw GitHub evidence for one issue, served through the injected runner."""
 
     def __init__(
-        self, *, host: str = HOST, assignees: tuple[str, ...] = (OWNER,)
+        self,
+        *,
+        host: str = HOST,
+        assignees: tuple[str, ...] = (OWNER,),
+        repo: str = REPO,
     ) -> None:
-        self.host, self.assignees = host, assignees
+        self.host, self.assignees, self.repo = host, assignees, repo
         self.comments: list[dict] = []
         self.events: list[dict] = []
         self.field_nodes: list[dict] = []  # G8 nodes: the Approved field events (R35)
@@ -179,8 +185,22 @@ class World:
         )
 
     # the injected runner
+    @staticmethod
+    def named_repo(argv) -> str | None:
+        """The repository an argv names: a REST path, a GraphQL owner and name, or none."""
+        for a in argv:
+            if a.startswith("repos/"):
+                return "/".join(a.split("/")[1:3])
+        owner = next((a[6:] for a in argv if a.startswith("owner=")), None)
+        name = next((a[5:] for a in argv if a.startswith("name=")), None)
+        return f"{owner}/{name}" if owner and name else None
+
     def run(self, argv, timeout, *, cwd=None) -> CommandResult:
         self.argvs.append(list(argv))
+        named = self.named_repo(argv)
+        assert named in (None, self.repo), (
+            f"{named} was read from the {self.repo} world"
+        )
         if argv[:3] == ["gh", "api", "graphql"] and "timelineItems" in argv[4]:
             # The Approved field events (R35): none in these tests.
             return ok(
@@ -271,11 +291,13 @@ def invoke(
     issue: int = ISSUE,
     approvers=frozenset({222}),
     label: str = LABEL,
+    repo: str = REPO,
 ):
     monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
     monkeypatch.setattr(cli_mod, "_load_stage_inputs", lambda path: (label, approvers))
     return CliRunner().invoke(
-        issue_pipeline_group, ["stage-status", str(issue), "--json", *args]
+        issue_pipeline_group,
+        ["stage-status", str(issue), "--repo", repo, "--json", *args],
     )
 
 
@@ -601,3 +623,108 @@ def test_an_approval_dated_after_the_plan_reply_is_accepted(
     assert out["approved"] is True and out["state"] == "approved"
     assert out["approvals"]["label"]["reason"] == "ok"
     assert out["approvals"]["label"]["actor_id"] == entry["approver_id"]
+
+
+# --- the repository is named by the caller (plan Task 15) ----------------------------
+
+
+class Router:
+    """A runner that serves each repository from its own ``World``."""
+
+    def __init__(self, **worlds: World) -> None:
+        self.worlds = worlds  # keyed by "owner/name" through ``by_repo``
+        self.by_repo = {w.repo: w for w in worlds.values()}
+        self.argvs: list[list[str]] = []
+
+    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
+        self.argvs.append(list(argv))
+        repo = World.named_repo(argv)
+        world = self.by_repo[repo] if repo else next(iter(self.by_repo.values()))
+        return world.run(argv, timeout, cwd=cwd)
+
+
+def test_stage_status_without_repo_is_a_usage_error(monkeypatch) -> None:
+    monkeypatch.setattr(cli_mod, "_make_runner", lambda: World())
+    result = CliRunner().invoke(issue_pipeline_group, ["stage-status", str(ISSUE)])
+    assert result.exit_code == 2 and "--repo" in result.output
+
+
+@pytest.mark.parametrize(
+    "bad", ["a/b/c", "", "a b/c", "-a/b", "a/-b", "justone", "a/b\n", "{owner}/{repo}"]
+)
+def test_a_repo_that_is_not_owner_slash_name_is_refused_before_any_call(
+    monkeypatch, bad: str
+) -> None:
+    world = World()
+    result = invoke(world, monkeypatch, repo=bad)
+    assert result.exit_code == 1 and result.output == "refused:bad-repo\n"
+    assert world.argvs == []
+
+
+def test_with_another_repo_every_read_carries_it_and_none_names_the_default(
+    monkeypatch, plan_dir: Path
+) -> None:
+    world = World(repo=OTHER)
+    world.plan_reply(plan_sha(plan_dir))
+    result = invoke(world, monkeypatch, repo=OTHER)
+    assert result.exit_code == 0, result.output
+    reads_ = [a for a in world.argvs if a != ["gh", "api", "user", "--include"]]
+    kinds = {
+        "reread": lambda a: (
+            a[:4] == ["gh", "api", "--method", "GET"]
+            and a[4].endswith(f"/issues/{ISSUE}")
+        ),
+        "events": lambda a: len(a) > 4 and a[4].endswith("/events"),
+        "comments": lambda a: len(a) > 4 and a[4].endswith("/comments"),
+        "edits": lambda a: (
+            a[:3] == ["gh", "api", "graphql"] and "comments(first" in " ".join(a)
+        ),
+        "approval_events": lambda a: (
+            a[:3] == ["gh", "api", "graphql"] and "timelineItems" in " ".join(a)
+        ),
+    }
+    for kind, test in kinds.items():
+        matched = [a for a in reads_ if test(a)]
+        assert matched, kind
+        for argv in matched:
+            text = "\n".join(argv)
+            assert "Other/Repo" in text or (
+                "owner=Other" in argv and "name=Repo" in argv
+            ), kind
+            assert "IronClaude" not in text and "IronbellyOrg" not in text, kind
+
+
+def test_an_approval_on_the_default_repos_issue_never_approves_the_other_repo(
+    monkeypatch, plan_dir: Path
+) -> None:
+    sha = plan_sha(plan_dir)
+    fork = World(repo=REPO)
+    fork.plan_reply(sha)
+    fork.label("labeled", T1)  # approved on IronClaude's issue of the same number
+    other = World(repo=OTHER)
+    other.plan_reply(sha)  # the same plan, no approval on the other repo
+    router = Router(fork=fork, other=other)
+    result = invoke(
+        router,
+        monkeypatch,
+        "--plan-dir",
+        str(plan_dir),
+        "--plan-file",
+        "plan.md",
+        repo=OTHER,
+    )
+    out = json.loads(result.output)
+    assert result.exit_code == 0 and out["approved"] is False
+    assert out["approvals"]["label"]["reason"] == "no-label"
+    assert not any("IronClaude" in " ".join(a) for a in router.argvs)
+    # and the same call for the default repo does see its own approval
+    again = invoke(
+        router,
+        monkeypatch,
+        "--plan-dir",
+        str(plan_dir),
+        "--plan-file",
+        "plan.md",
+        repo=REPO,
+    )
+    assert json.loads(again.output)["approved"] is True
diff --git a/tests/issue_watch/test_github.py b/tests/issue_watch/test_github.py
index f7109e7fc..3b9839cf9 100644
--- a/tests/issue_watch/test_github.py
+++ b/tests/issue_watch/test_github.py
@@ -29,7 +29,7 @@ from superclaude.cli.issue_watch.predicates import (
     approval_of,
 )
 
-from .conftest import result
+from .conftest import FakeRunner, result
 
 FIXTURES = Path(__file__).parent / "fixtures" / "_assumed_shape"
 NOW = datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)
@@ -51,8 +51,8 @@ REREAD_JQ = (
 
 # The two GraphQL drafts, written out literally (plan step 3.6): a change to the
 # page size, a field name or the paging block in github.py must fail a test.
-EDITS_QUERY = """query($number: Int!, $after: String) {
-  repository(owner: "IronbellyOrg", name: "IronClaude") {
+EDITS_QUERY = """query($owner: String!, $name: String!, $number: Int!, $after: String) {
+  repository(owner: $owner, name: $name) {
     issue(number: $number) {
       createdAt
       lastEditedAt
@@ -63,8 +63,8 @@ EDITS_QUERY = """query($number: Int!, $after: String) {
     }
   }
 }"""
-PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
-  repository(owner: "IronbellyOrg", name: "IronClaude") {
+PROJECT_ITEMS_QUERY = """query($owner: String!, $name: String!, $number: Int!, $after: String) {
+  repository(owner: $owner, name: $name) {
     issue(number: $number) {
       projectItems(first: 100, after: $after) {
         nodes {
@@ -183,6 +183,9 @@ def test_g4_argv_is_literal__fr009() -> None:
     ]
 
 
+REPO_VARS = ["-f", "owner=IronbellyOrg", "-f", "name=IronClaude"]
+
+
 def test_g5_argv_first_page_has_no_cursor__fr003() -> None:
     assert github.argv_edits(42) == [
         "gh",
@@ -190,6 +193,7 @@ def test_g5_argv_first_page_has_no_cursor__fr003() -> None:
         "graphql",
         "-f",
         f"query={EDITS_QUERY}",
+        *REPO_VARS,
         "-F",
         "number=42",
     ]
@@ -202,6 +206,7 @@ def test_g5_argv_later_page_adds_the_cursor() -> None:
         "graphql",
         "-f",
         f"query={EDITS_QUERY}",
+        *REPO_VARS,
         "-F",
         "number=42",
         "-f",
@@ -216,6 +221,7 @@ def test_g6_argv_first_page_has_no_cursor__fr007() -> None:
         "graphql",
         "-f",
         f"query={PROJECT_ITEMS_QUERY}",
+        *REPO_VARS,
         "-F",
         "number=42",
     ]
@@ -228,6 +234,7 @@ def test_g6_argv_later_page_adds_the_cursor__fr007() -> None:
         "graphql",
         "-f",
         f"query={PROJECT_ITEMS_QUERY}",
+        *REPO_VARS,
         "-F",
         "number=42",
         "-f",
@@ -235,6 +242,69 @@ def test_g6_argv_later_page_adds_the_cursor__fr007() -> None:
     ]
 
 
+# --- the repository is a parameter (plan Task 15) -----------------------------------
+
+OTHER = "Other-Org/Other.Repo"
+
+
+def _every_argv_for(repo: str) -> dict[str, list[str]]:
+    return {
+        "discover": github.argv_discover("sc:issue", "owner-login", repo),
+        "events": github.argv_events(42, 1, repo),
+        "comments": github.argv_comments(42, 1, repo),
+        "edits": github.argv_edits(42, None, repo),
+        "project_items": github.argv_project_items(42, None, repo),
+        "approval_events": github.argv_approval_events(42, None, repo),
+        "reread": github.argv_reread(42, repo),
+    }
+
+
+def test_every_argv_carries_the_passed_repo_and_not_the_default() -> None:
+    owner, name = OTHER.split("/")
+    for kind, argv in _every_argv_for(OTHER).items():
+        joined = "\n".join(argv)
+        assert "IronbellyOrg" not in joined and "IronClaude" not in joined, kind
+        if kind in ("edits", "project_items", "approval_events"):
+            assert f"owner={owner}" in argv and f"name={name}" in argv, kind
+        else:
+            assert OTHER in joined, kind
+
+
+def test_the_default_repo_is_the_forks() -> None:
+    assert github.argv_events(42, 2) == github.argv_events(42, 2, github.REPO)
+    assert github.argv_edits(42) == github.argv_edits(42, None, github.REPO)
+
+
+@pytest.mark.parametrize(
+    "bad",
+    ["a/b/c", "", "a b/c", "a/b c", "-a/b", "a/-b", "a", "/b", "a/", "a/..", "a/b\n"],
+)
+def test_a_repo_that_is_not_owner_slash_name_is_refused_before_any_call(
+    bad: str,
+) -> None:
+    for build in (
+        lambda: github.argv_discover("sc:issue", "owner-login", bad),
+        lambda: github.argv_events(42, 1, bad),
+        lambda: github.argv_comments(42, 1, bad),
+        lambda: github.argv_edits(42, None, bad),
+        lambda: github.argv_project_items(42, None, bad),
+        lambda: github.argv_approval_events(42, None, bad),
+        lambda: github.argv_reread(42, bad),
+    ):
+        with pytest.raises(ValueError):
+            build()
+
+
+def test_the_public_reads_pass_the_repo_and_raise_before_a_call() -> None:
+    fake_runner = FakeRunner()
+    budget = github.CallBudget()
+    with pytest.raises(ValueError):
+        github.events(fake_runner, budget, 42, lambda: 30.0, repo="a/b/c")
+    with pytest.raises(ValueError):
+        github.reread(fake_runner, budget, 42, lambda: 30.0, repo=" ")
+    assert fake_runner.calls == []
+
+
 def test_g7_argv_is_literal__fr011() -> None:
     assert github.argv_reread(42) == [
         "gh",
@@ -271,8 +341,11 @@ def test_no_graphql_argv_has_method() -> None:
 
 @pytest.mark.parametrize("query", [github.EDITS_QUERY, github.PROJECT_ITEMS_QUERY])
 def test_graphql_constants_name_the_repo_and_never_mutate(query: str) -> None:
-    assert 'owner: "IronbellyOrg", name: "IronClaude"' in query
-    assert "mutation" not in query.lower()
+    assert "repository(owner: $owner, name: $name)" in query
+    assert re.findall(r"\$(\w+): String!", query) == ["owner", "name"]
+    assert query.count("String!") == 2
+    assert "IronClaude" not in query
+    assert "mutation" not in query.lower() and "subscription" not in query.lower()
     assert "$after: String" in query
     assert "$after: String!" not in query
     assert re.search(r"\$after: String(?!!)", query)
diff --git a/tests/issue_watch/test_security_invariants.py b/tests/issue_watch/test_security_invariants.py
index 557c204e3..48e4989ec 100644
--- a/tests/issue_watch/test_security_invariants.py
+++ b/tests/issue_watch/test_security_invariants.py
@@ -303,12 +303,19 @@ def classify_argv(argv: object, worktree: object) -> str:
         return "rest"
     if argv[:4] == ["gh", "api", "graphql", "-f"]:
         assert argv[4] in _QUERIES, shown
-        assert argv[5] == "-F" and re.fullmatch(r"number=[1-9][0-9]{0,8}", argv[6]), (
+        # The repository travels as two string variables (plan Task 15), never in the query.
+        assert argv[5] == "-f" and re.fullmatch(r"owner=[A-Za-z0-9-]{1,39}", argv[6]), (
             shown
         )
-        assert len(argv) in (7, 9), shown
-        if len(argv) == 9:
-            assert argv[7] == "-f" and argv[8].startswith("after="), shown
+        assert argv[7] == "-f" and re.fullmatch(
+            r"name=[A-Za-z0-9._-]{1,100}", argv[8]
+        ), shown
+        assert argv[9] == "-F" and re.fullmatch(r"number=[1-9][0-9]{0,8}", argv[10]), (
+            shown
+        )
+        assert len(argv) in (11, 13), shown
+        if len(argv) == 13:
+            assert argv[11] == "-f" and argv[12].startswith("after="), shown
         return "graphql"
     if argv[0] == "git":
         assert len(argv) == 6 and argv[1] == "-C", shown
@@ -938,14 +945,18 @@ def test_no_string_constant_of_github_py_contains_mutation():
 @pytest.mark.parametrize(
     "name", ["EDITS_QUERY", "PROJECT_ITEMS_QUERY", "APPROVAL_EVENTS_QUERY"]
 )
-def test_both_graphql_constants_name_the_literal_repository_and_only_read(name):
+def test_the_graphql_constants_take_the_repository_as_variables_and_only_read(name):
     query = getattr(github, name)
-    assert github.REPO == FORK
-    assert 'repository(owner: "IronbellyOrg", name: "IronClaude")' in query, name
+    assert github.REPO == FORK  # the default of the github.py functions
+    # the repository is two non-null string variables (plan Task 15), never a literal
+    assert re.findall(r"\$(\w+): String!", query) == ["owner", "name"], name
+    assert query.count("String!") == 2, name
+    assert "repository(owner: $owner, name: $name)" in query, name
+    assert 'repository(owner: "' not in query and "IronClaude" not in query
     assert query.startswith("query("), name  # an operation that reads
     assert "mutation" not in query.lower() and "subscription" not in query.lower()
-    assert "$owner" not in query and "$name" not in query and "{owner}" not in query
-    assert "$after: String)" in query and "String!" not in query  # DF-14
+    assert "{owner}" not in query
+    assert "$after: String)" in query  # DF-14: the cursor stays nullable
     assert not _TEXT_FIELD.search(query), f"{name} asks for a title or body"
 
 

Task 15 context. github.py keeps REPO as the default of its functions (the watcher tests are unchanged apart from the GraphQL argv layout, which now holds -f owner= and -f name= before -F number=). reads.py and the stage-status verb take no default repo. I ran `ruff format` over src and tests by mistake once; it rewrote 12 unrelated markdown files, which I restored with git checkout from HEAD, so the diff holds only Task 15 files. Tests run: tests/issue_pipeline tests/issue_watch: 3160 passed; ruff clean; make verify-sync clean; no .claude/ path staged.

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
