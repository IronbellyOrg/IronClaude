d0fceb99a82a5553b5fc8c6ac7776ae1930b4cf4
Review one task for spec compliance.

Task brief: ## Task 11: Update the coordinator duties, the worker brief and the push rule

Depends on: Task 6, Task 7

Apply the remaining decisions of Task 6 to `src/superclaude/core/WORKER-CONTRACT.md` section "Issue pipeline duties" (line 291 onward) and to the rule that a push needs the person's go (line 245). The duties section names the Status-to-command table, says how the coordinator reads the Status and Pipeline, covers claims at every level (today it covers only `--pipeline none`, line 293), and names which stored record is the automatic approval record (R29): the claim-time approval in `dispatch.json` and the adoption row, never the plan-hash row. Line 242 (every such action targets `IronbellyOrg/IronClaude`) is reworded to say each action targets the repo the issue belongs to, never the SuperClaude upstream, and the `stage-status` call at line 298 names the issue's repo with `--repo` (Task 15 implements the flag). The brief is used only at level `none` (Task 6) and has no level slot. It states that after the coordinator mirrors the Status (line 298) or moves it to In review, the Project values have changed, so any relaunch needs a fresh approval label. Line 245 gets the replacement sentence decided in Task 6, so the coordinator never pushes worker commits on the Pipeline setting. Update the worker brief template `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `src/superclaude/cli/issue_pipeline/brief.py` so the brief carries the Command for the issue's Status, keeping the closed-set checks (no issue text reaches the brief). Update `tests/skills/test_worker_contract.py` and `tests/issue_pipeline/test_brief.py` for the new text and rows, and add the claim-time cases below to `tests/issue_pipeline/test_stage_predicates.py` and `tests/issue_pipeline/test_stage_status.py`. `approval_record.py` and `stage_predicates.py` are not changed: the rule that refuses a claim-time event exists. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- T11.AC1: `tests/issue_pipeline/test_stage_predicates.py` and `tests/issue_pipeline/test_stage_status.py` show that an approval (the `Approved` field event, which the code sees as a label event named by `approval_label`, R35) carrying the claim-time event id and approver id (a `dispatch.json` fixture), dated before the plan reply, gives `approved: false` with the reason `label-before-plan`, and that an approval dated after the plan reply is accepted. `tests/issue_pipeline/test_approval_record.py` shows `record_create` refuses a missing or malformed plan hash and a missing adoption row, and that the `record-create` verb requires `--plan-hash`. The duties text says the coordinator calls `record-create` only with evidence that `stage-status` reports as accepted.
- T11.AC2: `tests/issue_pipeline/test_brief.py` shows one brief row per allowed Status at level `none` (the only level that uses the brief), that the Debug row at `none` runs `/sc:troubleshoot` without `--fix` (Task 6 table), and that a bad Status, issue number or nonce is refused with a closed reason. The Worktree, Full and Full Submit troubleshoot forms are tested against the launch prompt in Task 10.
- T11.AC3: A test shows the Spec judgment: a well-defined issue yields the `/sc:design` row, an issue that is not yields the `/sc:brainstorm` row with the handoff to `/sc:design` for high complexity, and the reason is recorded in `issue-summary.md`.
- T11.AC4: `tests/skills/test_worker_contract.py` asserts the new push sentence and the absence of any coordinator push grant tied to Pipeline; `uv run pytest tests/skills tests/issue_pipeline -q` passes.
- T11.AC5: `make verify-sync` is clean and no `.claude/` path is staged.
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
Start sha: d0fceb99a82a5553b5fc8c6ac7776ae1930b4cf4
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/brief.py b/src/superclaude/cli/issue_pipeline/brief.py
index c0eb39a47..722cea680 100644
--- a/src/superclaude/cli/issue_pipeline/brief.py
+++ b/src/superclaude/cli/issue_pipeline/brief.py
@@ -1,11 +1,12 @@
-"""Build the plan-writing worker's brief from a fixed template (plan Task 7).
+"""Build the coordinator's worker brief from a fixed template (plan Tasks 7 and 11).
 
 The output is the Task spec the coordinator passes to ``worker-start --spec``, in the brief
-layout of ``src/superclaude/core/WORKER-CONTRACT.md`` section 5. The only inputs are the issue
-number (a validated integer) and two values read from the claim's summary, the type and the
-complexity, each checked against a closed set. No issue text can reach the brief: the template
-holds every other character. Only the three Feature rows are built; type ``bug`` is refused.
-The rows stop before ``/sc:implement`` and ``/task``.
+layout of ``src/superclaude/core/WORKER-CONTRACT.md`` section 5. It is used only at launch
+level ``none``. The inputs are the issue number (a validated integer), the stage word of the
+issue's Status (research, spec, plan or debug) and, for the spec stage, the route read from the
+``spec-route:`` line of the claim's ``issue-summary.md`` (design or brainstorm), each checked
+against a closed set. No issue text can reach the brief: the template holds every other
+character. The rows stop before ``/sc:implement`` and ``/task``, and the debug row has no ``--fix``.
 """
 
 from __future__ import annotations
@@ -15,8 +16,8 @@ from importlib import resources
 
 from superclaude.cli.issue_watch.predicates import valid_issue_number
 
-TYPES = ("feature", "bug")
-COMPLEXITIES = ("simple", "medium", "complex")
+STAGES = ("research", "spec", "plan", "debug")
+ROUTES = ("design", "brainstorm")
 
 
 class BriefRefused(Exception):
@@ -49,26 +50,31 @@ _NONCE = re.compile(r"[0-9a-f]{32}")
 
 
 def build(
-    issue: object, type_: object, complexity: object, nonce: object = None
+    issue: object, stage: object, route: object = None, nonce: object = None
 ) -> str:
-    """Return the brief for a Feature issue, or raise ``BriefRefused`` with a closed reason.
+    """Return the brief for one Status of an issue, or raise ``BriefRefused`` with a closed reason.
 
-    ``nonce`` is the launch nonce a governed worker is bound with (the coordinator gets
-    it from ``orca_worktree.py pending``); only then does the brief carry the one
+    ``route`` is required for the spec stage and refused for every other stage. ``nonce`` is
+    the launch nonce a governed worker is bound with (the coordinator gets it from
+    ``orca_worktree.py pending``); only then does the brief carry the one
     ``[sc-launch:v1:<nonce>]`` marker line. The brief of the one G1 test issue has none.
     """
     if not valid_issue_number(issue):
         raise BriefRefused("bad-issue")
-    if type_ not in TYPES:
-        raise BriefRefused("bad-type")
-    if type_ == "bug":
-        raise BriefRefused("type-not-supported")
-    if complexity not in COMPLEXITIES:
-        raise BriefRefused("bad-complexity")
+    if stage not in STAGES:
+        raise BriefRefused("bad-stage")
+    if stage == "spec":
+        if route not in ROUTES:
+            raise BriefRefused("bad-route")
+        row = f"spec-{route}"
+    else:
+        if route is not None:
+            raise BriefRefused("bad-route")
+        row = str(stage)
     if nonce is not None and not (isinstance(nonce, str) and _NONCE.fullmatch(nonce)):
         raise BriefRefused("bad-nonce")
     sections = _sections()
     marker = sections["marker"] if nonce is not None else []
-    lines = [*sections["head"], *marker, *sections[str(complexity)]]
-    text = "\n".join(lines).replace("{N}", str(issue))
+    lines = [*sections["head"], *marker, *sections[row]]
+    text = "\n".join(lines).replace("{N}", str(issue)).replace("{STAGE}", str(stage))
     return text.replace("{NONCE}", str(nonce)) + "\n"
diff --git a/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt b/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt
index 2d92fa671..c5a113606 100644
--- a/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt
+++ b/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt
@@ -1,27 +1,29 @@
-# Worker brief template for the plan-writing worker (issue pipeline, plan Task 7).
-# Slots: {N} (a validated issue number) only. The five fixed lines below are copied from
-# section 5 of src/superclaude/core/WORKER-CONTRACT.md; a test keeps the two copies equal.
-# The Worktree line differs on purpose: the coordinator fills the path of the worktree the
-# claim script made (Plan B Task 9). Rows stop before /sc:implement and /task.
+# Worker brief template for a coordinator's worker at level none (issue pipeline, plan Tasks 7 and 11).
+# One row per allowed Status (research, spec, plan, debug); the spec row has two routes, chosen from
+# the `spec-route:` line of issue-summary.md. Slots: {N} (a validated issue number) and {STAGE} (one
+# of the four closed stage words) only. The five fixed lines below are copied from section 5 of
+# src/superclaude/core/WORKER-CONTRACT.md; a test keeps the two copies equal. The Worktree line
+# differs on purpose: the coordinator fills the path of the worktree the claim script made. No row
+# runs /sc:implement, /task, a commit or a push. The debug row has no --fix.
 [head]
 Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
 Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
 On a blocked gate: report blocked
 Plan approval: after writing the plan, follow rule WC-17 in ~/.claude/WORKER-CONTRACT.md before any further step.
 Local commit: not authorized
-Report directory: .dev/issues/{N}/worker-plan
+Report directory: .dev/issues/{N}/worker-{STAGE}
 Worktree: path:<existing worktree>
 Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
+Relaunch: the coordinator's mirror of the Status, or its move to In review, changes the Project values, so a relaunch needs a fresh Approved set to Yes after the last Project change.
 [marker]
 Launch marker: [sc-launch:v1:{NONCE}]
-[simple]
-Command: /sc:brainstorm "issue {N} @.dev/issues/{N}/issue-summary.md" --depth quick --unattended --output .dev/issues/{N}/worker-plan/brainstorm
-Command: /sc:workflow .dev/issues/{N}/worker-plan/brainstorm/merged-requirements.md --depth quick --handoff none --unattended --report-dir .dev/issues/{N}/worker-plan/workflow
-[medium]
-Command: /sc:brainstorm "issue {N} @.dev/issues/{N}/issue-summary.md" --blind --unattended --output .dev/issues/{N}/worker-plan/brainstorm
-Command: /sc:design .dev/issues/{N}/worker-plan/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir .dev/issues/{N}/worker-plan/design
-Command: /sc:workflow .dev/issues/{N}/worker-plan/design/design-report.md --depth standard --handoff none --unattended --report-dir .dev/issues/{N}/worker-plan/workflow
-[complex]
-Command: /sc:brainstorm "issue {N} @.dev/issues/{N}/issue-summary.md" --depth deep --research deep --codebase --blind --unattended --output .dev/issues/{N}/worker-plan/brainstorm
-Command: /sc:design .dev/issues/{N}/worker-plan/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir .dev/issues/{N}/worker-plan/design
-Command: /sc:workflow .dev/issues/{N}/worker-plan/design/design-report.md --depth deep --handoff none --unattended --report-dir .dev/issues/{N}/worker-plan/workflow
+[research]
+Command: /sc:research "issue {N} @.dev/issues/{N}/issue-summary.md" --unattended --report-dir .dev/issues/{N}/worker-research
+[spec-design]
+Command: /sc:design .dev/issues/{N}/issue-summary.md --type architecture --format spec --unattended --report-dir .dev/issues/{N}/worker-spec
+[spec-brainstorm]
+Command: /sc:brainstorm "issue {N} @.dev/issues/{N}/issue-summary.md" --blind --handoff design --unattended --output .dev/issues/{N}/worker-spec
+[plan]
+Command: /sc:workflow .dev/issues/{N}/issue-summary.md --depth standard --handoff none --unattended --report-dir .dev/issues/{N}/worker-plan
+[debug]
+Command: /sc:troubleshoot "issue {N} @.dev/issues/{N}/issue-summary.md" --unattended --report-dir .dev/issues/{N}/worker-debug
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index bc2967679..385ca2e3e 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -239,10 +239,10 @@ A WC-3 re-invocation keeps every token of the `Command:` line and only adds the
 ### Git and GitHub ownership
 
 - The coordinator performs every git and GitHub outward action, and every install, VM or paid run, in its own conversation, only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation.
-- Every such action targets `IronbellyOrg/IronClaude`: never the SuperClaude upstream, and never through Orca's issue or PR linking while Orca records the project as the upstream.
+- Every such action targets the repo the issue belongs to (`IronbellyOrg/IronClaude` for this repository): never the SuperClaude upstream, and never through Orca's issue or PR linking while Orca records the project as the upstream.
 - Progress posts (issue comments, project fields) are such actions, made from contracts the coordinator has read; workers report progress only through heartbeats and `worker_done` (WC-5, WC-10).
 - PRs go only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states, never as a worker.
-- Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. A commit grant covers one Task and ends at that Task's `worker_done`.
+- Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. At Full Submit the launched agent pushes only its own feature branch to origin and opens the pull request through /sc:pr-submit; the owner's Pipeline value plus an approval later than the last Project change is the go for that issue only. The coordinator never pushes worker commits on that basis; for every other push the rule above stands. A commit grant covers one Task and ends at that Task's `worker_done`.
 - The coordinator commits or merges in a worktree only when no worker runs there and no `/sc:implement` Task there is frozen (below). It compares `git status --porcelain` with the settled contracts and reports unlisted paths, stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run, which satisfies the repo's always-staged rule for worker sessions, commits with `git commit --only -- <paths>`, treats "nothing to commit" as success, and stops and reports on any hook rewrite, hook failure or conflict, never `--no-verify`.
 - The plan or brief records who owns each PR.
 
@@ -292,10 +292,11 @@ The coordinator keeps watching its Run until every Task it created is settled an
 
 These duties apply only to an issue that the issue watcher claimed with `/sc:issue --claim <N> --pipeline <level> --stage <stage>` (any level) and that this coordinator now owns. One person-opened coordinator owns every watcher-claimed issue on the host; nothing starts while it is down. The CLI verbs named here are the `superclaude issue-pipeline` group.
 
-- **Adopt from sources that exist after a `--pipeline none` claim.** Such a claim creates no worktree and writes no worktree record, so the coordinator reads only the watcher store's `claimed` entry in `dispatch.json` (read-only) and `.dev/issues/<N>/issue-summary.md` and `next-steps.md` in the checkout that ran the claim.
+- **Adopt from sources that exist after a `--pipeline none` claim.** Such a claim creates no worktree and writes no worktree record, so the coordinator reads only the watcher store's `claimed` entry in `dispatch.json` (read-only) and `.dev/issues/<N>/issue-summary.md` and `next-steps.md` in the checkout that ran the claim. The claim's stage and level are the `Stage:` and `Level:` lines of `next-steps.md`. The coordinator never trusts a Status it remembers: it rereads the Project item through `stage-status --repo <the issue's repo>` at each gate.
+- **Status to command (level `none` only).** The coordinator starts a worker only for a `none` claim, and the brief it passes to `worker-start --spec` is built by `superclaude.cli.issue_pipeline.brief` with one row per Status: Research runs `/sc:research`; Spec runs `/sc:design` when `issue-summary.md` has `spec-route: design` and `/sc:brainstorm` (with `--handoff design`) when it has `spec-route: brainstorm`; Plan runs `/sc:workflow` and stops before `/sc:implement` and `/task`; Debug runs `/sc:troubleshoot` without `--fix`. Ready, Backlog, In progress, In review and Done start nothing. Claims at the other levels (`worktree`, `full`, `full submit`) launch their own agent, which runs the stage command from its launch prompt; the coordinator starts no worker for them and no brief has a level slot. After the coordinator mirrors the Status or moves it to In review, the Project values have changed, so any relaunch needs a fresh `Approved` field set to Yes after the last Project change.
 - **Reserve before starting.** Create the adoption row (`adopt-create`) before `worker-start`; only a `created` result may start a worker. Mark the row `started` with the Dispatch id (`adopt-mark`) when `worker-start` returns ready, and `uncertain` when it does not. Never start again for an `uncertain` row: settle it by reading `worker-list`.
 - **Worktree, then worker.** Run the existing worktree step of the installed `sc-issue-protocol` skill (the script orca_worktree.py, subcommand worktree, with `--repo <R> --number <N> --base origin/<B> --source <the claim's issue folder>`), which creates or reuses the worktree with no agent, then run `worker-start --worktree path:<exact path it printed> --agent claude --spec <the worker brief for the issue>` straight after it.
-- **Plan approval.** The worker asks once with the plan path, file list and plan hash. Post the plan reply with the hash and file list and mention the assignee, then read GitHub through `stage-status` at each gate or wake. Create the plan-hash approval row (`record-create`) only when the worker's `ask` carries the plan hash. On approval write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status; mark the row `instructed` and then, from the worker's ack, `acked` (`record-mark`).
+- **Plan approval.** The worker asks once with the plan path, file list and plan hash. Post the plan reply with the hash and file list and mention the assignee, then read GitHub through `stage-status --repo <the issue's repo>` at each gate or wake. The automatic approval record is the claim-time approval kept in `dispatch.json` plus the adoption row; it is never the plan-hash row, and `stage-status` refuses a claim-time approval dated before the plan reply (`label-before-plan`). Create the plan-hash approval row (`record-create`) only when the worker's `ask` carries the plan hash and `stage-status` reports the approval as accepted. On approval write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status; mark the row `instructed` and then, from the worker's ack, `acked` (`record-mark`).
 - **Route B adds no exception to "never answer a person prompt".** The worker's plan boundary is crossed by the reply to its own `ask`, which is not a person prompt, so the coordinator types nothing into a worker's terminal for this flow.
 - **Never:** tell a worker to pass its plan boundary without an approval row; act on a Status move alone; relaunch a dead worker by itself (WC-6 and the person decide); post an issue write without that issue's grant row.
 
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index 6a0285009..a92a919a5 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -57,7 +57,7 @@ Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` sizes the issue `c
 - checks each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code, and checks each merged pull request and changed file from `scout.md` for relevance;
 - writes `<D>/accuracy-check.md` from `templates/accuracy-check-comment.md` with the verdict `current` or `out_of_date` and the evidence for each changed claim;
 - when `out_of_date`: runs `/sc:analyze` on the paths the issue touches (`--depth deep` when complex, no `--depth` otherwise) and saves the report as `<D>/analysis/analyze-<scope>.md` (`<scope>` in this file name is the last segment of the main path the issue touches; no file under `<D>/analysis/` has a name that starts with analysis, report, summary or findings);
-- always writes `<D>/issue-summary.md` from `templates/issue-summary.md`: what the issue asks for, the relevant files and systems (the cheatsheet), type, complexity, the effort estimate in hours using the rubric below (B3), and links to anything under `<D>/analysis/` (default D22);
+- always writes `<D>/issue-summary.md` from `templates/issue-summary.md`: what the issue asks for, the relevant files and systems (the cheatsheet), type, complexity, the effort estimate in hours using the rubric below (B3), the one `spec-route: design|brainstorm — <reason>` line (`design` only when the complexity is Simple or Medium and the issue states an acceptance criterion; anything else, and every Complex issue, is `brainstorm`, which hands off to `/sc:design`), and links to anything under `<D>/analysis/` (default D22);
 - returns both paths.
 
 Missing or empty file: retry the worker once, then STOP `E-WORKER-NO-OUTPUT` naming the missing path.
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md b/src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md
index 18b67a5ca..fc9b1c116 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md
@@ -7,6 +7,7 @@ Handled by issue-worker-t2 (tier 2): tier1b is not available to this user.
 - Type: <feature | bug>
 - Complexity: <simple | medium | complex> (rubric: `refs/claim.md`)
 - Effort estimate: <hours> hours
+- spec-route: <design | brainstorm> — <one-line reason> (design: Simple or Medium with a stated acceptance criterion; brainstorm: anything else, and always for Complex, which then hands off to `/sc:design`)
 
 ## What the issue asks for
 
diff --git a/tests/hooks/test_launch_level_guard_worker.py b/tests/hooks/test_launch_level_guard_worker.py
index 4a700b19f..496445150 100644
--- a/tests/hooks/test_launch_level_guard_worker.py
+++ b/tests/hooks/test_launch_level_guard_worker.py
@@ -321,10 +321,10 @@ def test_a_brief_built_with_a_pending_nonce_binds_the_worker_and_one_without_doe
         check=True,
     ).stdout
     nonce = json.loads(out)["nonce"]
-    governed = brief.build(9, "feature", "simple", nonce)
+    governed = brief.build(9, "plan", None, nonce)
     assert _allowed(_run(_prompt(governed), tmp_path))
     _assert_bound(tmp_path, SID, "worktree")
     other = tmp_path / "other"
     other.mkdir()
-    assert _allowed(_run(_prompt(brief.build(9, "feature", "simple")), other))
+    assert _allowed(_run(_prompt(brief.build(9, "plan")), other))
     assert not (_store(other / "home") / "sessions" / SID).exists()
diff --git a/tests/issue_pipeline/test_approval_record.py b/tests/issue_pipeline/test_approval_record.py
index 595c89f0d..fd3539584 100644
--- a/tests/issue_pipeline/test_approval_record.py
+++ b/tests/issue_pipeline/test_approval_record.py
@@ -422,3 +422,45 @@ def test_a_structurally_damaged_adoption_row_is_a_closed_refusal(
         with pytest.raises(ar.ApprovalError) as err:
             call()
         assert err.value.reason == "row-invalid"
+
+
+# --- the plan-hash row is never made from claim-time fields (plan Task 11, R29) ------
+
+
+@pytest.mark.parametrize("bad_hash", ["", None, "a" * 63, "A" * 64, "z" * 64, H1 + "0"])
+def test_record_create_refuses_a_missing_or_malformed_plan_hash(
+    adir: Path, bad_hash: object
+) -> None:
+    _adopt_started(adir)
+    with pytest.raises(ar.ApprovalError):
+        ar.record_create(adir, 9, "plan", bad_hash, "label", "e1", "u1", T)  # type: ignore[arg-type]
+
+
+def test_record_create_without_the_adoption_row_refuses_even_with_a_valid_hash(
+    adir: Path,
+) -> None:
+    with pytest.raises(ar.ApprovalError) as err:
+        _create(adir, "label", "e1", H1)
+    assert err.value.reason == "no-adoption"
+
+
+def test_the_record_create_verb_requires_plan_hash(adir: Path) -> None:
+    _adopt_started(adir)
+    result = CliRunner().invoke(
+        issue_pipeline_group,
+        [
+            "record-create",
+            str(adir),
+            "--issue",
+            "9",
+            "--stage",
+            "plan",
+            "--channel",
+            "label",
+            "--evidence-id",
+            "e1",
+            "--actor",
+            "u1",
+        ],
+    )
+    assert result.exit_code != 0 and "--plan-hash" in result.output
diff --git a/tests/issue_pipeline/test_brief.py b/tests/issue_pipeline/test_brief.py
index 35b947458..0de6af774 100644
--- a/tests/issue_pipeline/test_brief.py
+++ b/tests/issue_pipeline/test_brief.py
@@ -1,4 +1,4 @@
-"""Task 7: the worker brief is built from fixed templates."""
+"""Tasks 7 and 11: the worker brief is built from fixed templates, one row per Status."""
 
 from __future__ import annotations
 
@@ -13,44 +13,97 @@ from superclaude.cli.issue_pipeline import brief
 ROOT = Path(__file__).resolve().parents[2]
 CONTRACT = ROOT / "src/superclaude/core/WORKER-CONTRACT.md"
 TEMPLATE = ROOT / "src/superclaude/cli/issue_pipeline/templates/worker-brief.txt"
+SUMMARY_TEMPLATE = (
+    ROOT / "src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md"
+)
+CLAIM_REF = ROOT / "src/superclaude/skills/sc-issue-protocol/refs/claim.md"
 
 HEAD = """Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
 Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
 On a blocked gate: report blocked
 Plan approval: after writing the plan, follow rule WC-17 in ~/.claude/WORKER-CONTRACT.md before any further step.
 Local commit: not authorized
-Report directory: .dev/issues/452/worker-plan
+Report directory: .dev/issues/452/worker-{stage}
 Worktree: path:<existing worktree>
 Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
+Relaunch: the coordinator's mirror of the Status, or its move to In review, changes the Project values, so a relaunch needs a fresh Approved set to Yes after the last Project change.
 """
-D = ".dev/issues/452/worker-plan"
-BRAIN = '/sc:brainstorm "issue 452 @.dev/issues/452/issue-summary.md"'
-GOLDEN = {
-    "simple": HEAD
-    + f"Command: {BRAIN} --depth quick --unattended --output {D}/brainstorm\n"
-    + f"Command: /sc:workflow {D}/brainstorm/merged-requirements.md --depth quick --handoff none --unattended --report-dir {D}/workflow\n",
-    "medium": HEAD
-    + f"Command: {BRAIN} --blind --unattended --output {D}/brainstorm\n"
-    + f"Command: /sc:design {D}/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir {D}/design\n"
-    + f"Command: /sc:workflow {D}/design/design-report.md --depth standard --handoff none --unattended --report-dir {D}/workflow\n",
-    "complex": HEAD
-    + f"Command: {BRAIN} --depth deep --research deep --codebase --blind --unattended --output {D}/brainstorm\n"
-    + f"Command: /sc:design {D}/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir {D}/design\n"
-    + f"Command: /sc:workflow {D}/design/design-report.md --depth deep --handoff none --unattended --report-dir {D}/workflow\n",
+S = '"issue 452 @.dev/issues/452/issue-summary.md"'
+D = ".dev/issues/452"
+# one row per allowed Status: (stage, route) -> the Command line
+ROWS = {
+    (
+        "research",
+        None,
+    ): f"Command: /sc:research {S} --unattended --report-dir {D}/worker-research\n",
+    (
+        "spec",
+        "design",
+    ): f"Command: /sc:design {D}/issue-summary.md --type architecture --format spec --unattended --report-dir {D}/worker-spec\n",
+    (
+        "spec",
+        "brainstorm",
+    ): f"Command: /sc:brainstorm {S} --blind --handoff design --unattended --output {D}/worker-spec\n",
+    (
+        "plan",
+        None,
+    ): f"Command: /sc:workflow {D}/issue-summary.md --depth standard --handoff none --unattended --report-dir {D}/worker-plan\n",
+    (
+        "debug",
+        None,
+    ): f"Command: /sc:troubleshoot {S} --unattended --report-dir {D}/worker-debug\n",
 }
 
 
-@pytest.mark.parametrize("complexity", ["simple", "medium", "complex"])
-def test_golden_brief_per_feature_row(complexity: str) -> None:
-    assert brief.build(452, "feature", complexity) == GOLDEN[complexity]
+def golden(stage: str, route: str | None) -> str:
+    return HEAD.format(stage=stage) + ROWS[(stage, route)]
+
+
+@pytest.mark.parametrize("stage,route", list(ROWS))
+def test_golden_brief_per_allowed_status(stage: str, route: str | None) -> None:
+    assert brief.build(452, stage, route) == golden(stage, route)
+
+
+def test_there_is_one_row_per_allowed_status() -> None:
+    assert (
+        {stage for stage, _ in ROWS}
+        == set(brief.STAGES)
+        == {
+            "research",
+            "spec",
+            "plan",
+            "debug",
+        }
+    )
+    assert {route for stage, route in ROWS if stage == "spec"} == set(brief.ROUTES)
+
+
+def test_the_debug_row_at_level_none_runs_troubleshoot_without_fix() -> None:
+    text = brief.build(452, "debug")
+    commands = [line for line in text.splitlines() if line.startswith("Command:")]
+    assert len(commands) == 1 and commands[0].startswith("Command: /sc:troubleshoot ")
+    assert "--fix" not in text
+
 
+def test_the_spec_row_follows_the_route_of_the_judgment() -> None:
+    well_defined = brief.build(452, "spec", "design")
+    not_defined = brief.build(452, "spec", "brainstorm")
+    assert "/sc:design " in well_defined and "/sc:brainstorm" not in well_defined
+    assert "/sc:brainstorm " in not_defined
+    # the brainstorm row hands off to /sc:design (high complexity or scope)
+    assert "--handoff design" in not_defined
 
-@pytest.mark.parametrize("complexity", ["medium", "complex"])
-def test_design_rows_use_a_fixed_architecture_type(complexity: str) -> None:
-    text = brief.build(7, "feature", complexity)
-    design = [line for line in text.splitlines() if "/sc:design" in line]
-    assert len(design) == 1 and "--type architecture --format spec" in design[0]
-    assert "/sc:design" not in brief.build(7, "feature", "simple")
+
+def test_the_spec_judgment_is_recorded_in_issue_summary_not_decided_by_code() -> None:
+    """The claim worker writes `spec-route: design|brainstorm — <reason>`; the brief only reads it."""
+    summary = SUMMARY_TEMPLATE.read_text()
+    assert "- spec-route: <design | brainstorm> — <one-line reason>" in summary
+    claim = CLAIM_REF.read_text()
+    assert "`spec-route: design|brainstorm — <reason>`" in claim
+    # Simple or Medium with a stated acceptance criterion is well defined; the rest, and Complex, is not
+    assert "only when the complexity is Simple or Medium" in claim
+    assert "every Complex issue, is `brainstorm`" in claim
+    assert "`/sc:design`" in claim
 
 
 def _template_characters() -> set[str]:
@@ -67,15 +120,14 @@ def test_output_holds_only_template_characters_plus_the_issue_number() -> None:
     rng = random.Random(7)
     numbers = [1, 9, 452, 99999, *(rng.randrange(1, 10**9) for _ in range(30))]
     for n in numbers:
-        for complexity in ("simple", "medium", "complex"):
-            text = brief.build(n, "feature", complexity)
+        for stage, route in ROWS:
+            text = brief.build(n, stage, route)
             assert set(text) <= allowed
-            # the output is the template section with {N} replaced by the validated number, nothing else
-            assert text == _expected_from_template(n, complexity)
+            assert text == _expected_from_template(n, stage, route)
             assert text.count(str(n)) >= 3
 
 
-def _expected_from_template(n: int, complexity: str) -> str:
+def _expected_from_template(n: int, stage: str, route: str | None) -> str:
     sections: dict[str, list[str]] = {}
     current: list[str] | None = None
     for line in TEMPLATE.read_text().splitlines():
@@ -85,8 +137,11 @@ def _expected_from_template(n: int, complexity: str) -> str:
             current = sections.setdefault(line[1:-1], [])
         elif current is not None:
             current.append(line)
+    row = f"spec-{route}" if stage == "spec" else stage
     return (
-        "\n".join([*sections["head"], *sections[complexity]]).replace("{N}", str(n))
+        "\n".join([*sections["head"], *sections[row]])
+        .replace("{N}", str(n))
+        .replace("{STAGE}", stage)
         + "\n"
     )
 
@@ -94,27 +149,47 @@ def _expected_from_template(n: int, complexity: str) -> str:
 HOSTILE = [
     "<script>x</script>",
     "$(rm -rf /)",
-    "simple; /sc:implement x",
-    "simple\n/sc:implement x",
-    "SIMPLE",
+    "plan; /sc:implement x",
+    "plan\n/sc:implement x",
+    "PLAN",
     "",
-    " simple",
-    "simple ",
+    " plan",
+    "plan ",
+    "ready",
+    "implement",
     None,
     5,
-    ["simple"],
-    "‮simple",
+    ["plan"],
+    "‮plan",
 ]
 
 
 @pytest.mark.parametrize("value", HOSTILE)
-def test_values_outside_the_enums_refuse_with_a_closed_reason(value: object) -> None:
+def test_a_status_outside_the_closed_set_is_refused_with_a_closed_reason(
+    value: object,
+) -> None:
+    with pytest.raises(brief.BriefRefused) as err:
+        brief.build(452, value)
+    assert err.value.reason == "bad-stage"
+
+
+@pytest.mark.parametrize("value", HOSTILE)
+def test_a_route_outside_the_closed_set_is_refused(value: object) -> None:
+    if value is None:
+        value = "missing"  # a spec row with no route is refused too
     with pytest.raises(brief.BriefRefused) as err:
-        brief.build(452, "feature", value)
-    assert err.value.reason == "bad-complexity"
+        brief.build(452, "spec", value)
+    assert err.value.reason == "bad-route"
     with pytest.raises(brief.BriefRefused) as err:
-        brief.build(452, value, "simple")
-    assert err.value.reason == "bad-type"
+        brief.build(452, "spec")
+    assert err.value.reason == "bad-route"
+
+
+@pytest.mark.parametrize("stage", ["research", "plan", "debug"])
+def test_a_route_is_refused_for_every_stage_but_spec(stage: str) -> None:
+    with pytest.raises(brief.BriefRefused) as err:
+        brief.build(452, stage, "design")
+    assert err.value.reason == "bad-route"
 
 
 @pytest.mark.parametrize(
@@ -122,27 +197,20 @@ def test_values_outside_the_enums_refuse_with_a_closed_reason(value: object) ->
 )
 def test_a_non_integer_issue_number_is_refused(issue: object) -> None:
     with pytest.raises(brief.BriefRefused) as err:
-        brief.build(issue, "feature", "simple")
+        brief.build(issue, "plan")
     assert err.value.reason == "bad-issue"
 
 
-@pytest.mark.parametrize("complexity", ["simple", "medium", "complex", "bogus"])
-def test_type_bug_is_refused_and_builds_no_brief(complexity: str) -> None:
-    with pytest.raises(brief.BriefRefused) as err:
-        brief.build(452, "bug", complexity)
-    assert err.value.reason == "type-not-supported"
-
-
 def test_no_row_runs_implement_commit_push_or_submit_and_every_command_is_unattended() -> (
     None
 ):
     forbidden = ("/sc:implement", "/task", "git commit", "git push", "/sc:pr-submit")
-    for complexity in ("simple", "medium", "complex"):
-        text = brief.build(452, "feature", complexity)
+    for stage, route in ROWS:
+        text = brief.build(452, stage, route)
         commands = [line for line in text.splitlines() if line.startswith("Command:")]
-        assert len(commands) >= 2
+        assert len(commands) == 1
         for token in forbidden:
-            assert token not in text, (complexity, token)
+            assert token not in text, (stage, token)
         for line in commands:
             assert "--unattended" in line
             assert (
@@ -152,6 +220,30 @@ def test_no_row_runs_implement_commit_push_or_submit_and_every_command_is_unatte
                 assert "--handoff none" in line
 
 
+def test_the_brief_has_no_level_slot() -> None:
+    """The brief is used only at level none: it names no level and offers no level argument."""
+    import inspect
+
+    assert list(inspect.signature(brief.build).parameters) == [
+        "issue",
+        "stage",
+        "route",
+        "nonce",
+    ]
+    assert "{LEVEL}" not in TEMPLATE.read_text()
+    assert "--pipeline" not in brief.build(452, "plan")
+
+
+def test_the_brief_says_a_relaunch_needs_a_fresh_approval() -> None:
+    lines = brief.build(452, "plan").splitlines()
+    relaunch = [line for line in lines if line.startswith("Relaunch:")]
+    assert len(relaunch) == 1
+    assert "In review" in relaunch[0] and "fresh Approved set to Yes" in relaunch[0]
+    assert lines.index(relaunch[0]) < next(
+        i for i, line in enumerate(lines) if line.startswith("Command:")
+    )
+
+
 def test_fixed_lines_equal_the_contract_template_word_for_word() -> None:
     contract = CONTRACT.read_text()
     block = (
@@ -161,7 +253,7 @@ def test_fixed_lines_equal_the_contract_template_word_for_word() -> None:
         .group(1)
         .splitlines()
     )
-    ours = brief.build(452, "feature", "simple").splitlines()
+    ours = brief.build(452, "plan").splitlines()
     for prefix in (
         "Guard:",
         "Chain:",
@@ -182,8 +274,8 @@ def test_fixed_lines_equal_the_contract_template_word_for_word() -> None:
 def test_brief_points_at_the_plan_approval_rule_of_the_contract() -> None:
     contract = CONTRACT.read_text()
     assert "**WC-17. Plan approval is the reply to the worker's own ask.**" in contract
-    for complexity in ("simple", "medium", "complex"):
-        lines = brief.build(452, "feature", complexity).splitlines()
+    for stage, route in ROWS:
+        lines = brief.build(452, stage, route).splitlines()
         pointer = [line for line in lines if line.startswith("Plan approval:")]
         assert len(pointer) == 1 and "WC-17" in pointer[0]
         assert lines.index(pointer[0]) < next(
@@ -195,9 +287,11 @@ NONCE = "0123456789abcdef0123456789abcdef"
 MARKER_RE = re.compile(r"\[sc-launch:v1:[0-9a-f]{32}\]")
 
 
-@pytest.mark.parametrize("complexity", ["simple", "medium", "complex"])
-def test_a_governed_brief_carries_exactly_one_marker_line(complexity: str) -> None:
-    text = brief.build(452, "feature", complexity, NONCE)
+@pytest.mark.parametrize("stage,route", list(ROWS))
+def test_a_governed_brief_carries_exactly_one_marker_line(
+    stage: str, route: str | None
+) -> None:
+    text = brief.build(452, stage, route, NONCE)
     lines = text.splitlines()
     marked = [line for line in lines if MARKER_RE.search(line)]
     assert marked == [f"Launch marker: [sc-launch:v1:{NONCE}]"]
@@ -206,12 +300,14 @@ def test_a_governed_brief_carries_exactly_one_marker_line(complexity: str) -> No
     assert lines.index(marked[0]) < next(
         i for i, line in enumerate(lines) if line.startswith("Command:")
     )
-    assert text.replace(marked[0] + "\n", "") == brief.build(452, "feature", complexity)
+    assert text.replace(marked[0] + "\n", "") == brief.build(452, stage, route)
 
 
-@pytest.mark.parametrize("complexity", ["simple", "medium", "complex"])
-def test_the_g1_test_issue_brief_carries_no_marker(complexity: str) -> None:
-    assert "sc-launch" not in brief.build(452, "feature", complexity)
+@pytest.mark.parametrize("stage,route", list(ROWS))
+def test_the_g1_test_issue_brief_carries_no_marker(
+    stage: str, route: str | None
+) -> None:
+    assert "sc-launch" not in brief.build(452, stage, route)
 
 
 @pytest.mark.parametrize(
@@ -220,5 +316,5 @@ def test_the_g1_test_issue_brief_carries_no_marker(complexity: str) -> None:
 )
 def test_a_nonce_outside_the_guard_form_is_refused(nonce: object) -> None:
     with pytest.raises(brief.BriefRefused) as err:
-        brief.build(452, "feature", "simple", nonce)
+        brief.build(452, "plan", None, nonce)
     assert err.value.reason == "bad-nonce"
diff --git a/tests/issue_pipeline/test_stage_predicates.py b/tests/issue_pipeline/test_stage_predicates.py
index c5ebfc3ce..2c2839d1d 100644
--- a/tests/issue_pipeline/test_stage_predicates.py
+++ b/tests/issue_pipeline/test_stage_predicates.py
@@ -464,3 +464,69 @@ def test_the_host_login_flag_is_set_and_the_approval_is_still_accepted() -> None
     assert by_comment.approved and by_comment.comment.actor_is_host_login
     plain = run([plan_reply(10, 0)], [label_event(1, 2)])
     assert not plain.label.actor_is_host_login and not plain.assignee_is_host_login
+
+
+# --- claim-time approval (plan Task 11, R29, R35) ----------------------------------
+
+FIELD_LABEL = "issue-field:Approved"
+
+
+def _claim_time_event(tmp_path: Path, minutes: int) -> LabelEvent:
+    """The `Approved` field event the watcher kept in dispatch.json at claim time."""
+    stamp = at(minutes).strftime("%Y-%m-%dT%H:%M:%SZ")
+    path = tmp_path / "dispatch.json"
+    path.write_text(
+        json.dumps(
+            {
+                "9": {
+                    "state": "claimed",
+                    "approver_id": APPROVER_ID,
+                    "approval_event_id": 4242,
+                    "approved_at": stamp,
+                }
+            }
+        )
+    )
+    entry = json.loads(path.read_text())["9"]
+    return LabelEvent(
+        entry["approval_event_id"],
+        "labeled",
+        FIELD_LABEL,
+        entry["approver_id"],
+        "approver-login",
+        "User",
+        parse_utc(entry["approved_at"]),
+    )
+
+
+def _run_field(comments, events) -> sp.StageStatus:
+    return sp.evaluate(
+        9,
+        comments,
+        events,
+        edits_for(*comments),
+        plan_hash_now=H_A,
+        host_login=HOST,
+        assignees=(OWNER,),
+        approvers=frozenset({APPROVER_ID}),
+        approval_label=FIELD_LABEL,
+    )
+
+
+def test_a_claim_time_approval_dated_before_the_plan_reply_gives_label_before_plan(
+    tmp_path: Path,
+) -> None:
+    claim = _claim_time_event(tmp_path, 0)
+    status = _run_field([plan_reply(10, 5)], [claim])
+    assert status.approved is False and status.state == "awaiting-approval"
+    assert (status.label.accepted, status.label.reason) == (False, "label-before-plan")
+
+
+def test_an_approval_dated_after_the_plan_reply_is_accepted_even_with_a_claim_time_one(
+    tmp_path: Path,
+) -> None:
+    claim = _claim_time_event(tmp_path, 0)
+    fresh = replace(claim, id=4243, created_at=at(8))
+    status = _run_field([plan_reply(10, 5)], [claim, fresh])
+    assert status.approved is True and status.label.reason == "ok"
+    assert status.label.evidence_id == 4243 and status.label.actor_id == APPROVER_ID
diff --git a/tests/issue_pipeline/test_stage_status.py b/tests/issue_pipeline/test_stage_status.py
index d66362692..8cd3e85a8 100644
--- a/tests/issue_pipeline/test_stage_status.py
+++ b/tests/issue_pipeline/test_stage_status.py
@@ -535,3 +535,69 @@ def test_the_command_only_reads_and_never_calls_orca(
 def test_stage_status_help_exits_zero() -> None:
     result = CliRunner().invoke(issue_pipeline_group, ["stage-status", "--help"])
     assert result.exit_code == 0 and "stage-status" in result.output
+
+
+# --- claim-time approval (plan Task 11, R29, R35) ----------------------------------
+
+
+def _claim_entry(tmp_path: Path, approved_at: str) -> dict:
+    """The watcher store's claimed entry for the issue (a dispatch.json fixture)."""
+    path = tmp_path / "dispatch.json"
+    path.write_text(
+        json.dumps(
+            {
+                str(ISSUE): {
+                    "state": "claimed",
+                    "approver_id": 222,
+                    "approval_event_id": 4242,
+                    "approved_at": approved_at,
+                }
+            }
+        )
+    )
+    return json.loads(path.read_text())[str(ISSUE)]
+
+
+def _field_status(world: World, monkeypatch, plan_dir: Path) -> dict:
+    from superclaude.cli.issue_watch.predicates import APPROVAL_FIELD_LABEL
+
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
+    assert_closed(out)
+    return out
+
+
+def test_a_claim_time_approval_dated_before_the_plan_reply_is_not_plan_approval(
+    monkeypatch, plan_dir: Path, tmp_path: Path
+) -> None:
+    entry = _claim_entry(tmp_path, T0)
+    world = World()
+    world.field_set(entry["approved_at"], uid=entry["approver_id"])
+    world.plan_reply(plan_sha(plan_dir), at=T1)
+    out = _field_status(world, monkeypatch, plan_dir)
+    assert out["approved"] is False and out["state"] == "awaiting-approval"
+    assert out["approvals"]["label"]["accepted"] is False
+    assert out["approvals"]["label"]["reason"] == "label-before-plan"
+
+
+def test_an_approval_dated_after_the_plan_reply_is_accepted(
+    monkeypatch, plan_dir: Path, tmp_path: Path
+) -> None:
+    entry = _claim_entry(tmp_path, T0)
+    world = World()
+    world.field_set(entry["approved_at"], uid=entry["approver_id"])
+    world.plan_reply(plan_sha(plan_dir), at=T1)
+    world.field_set(T2, uid=entry["approver_id"])  # a fresh approval after the reply
+    out = _field_status(world, monkeypatch, plan_dir)
+    assert out["approved"] is True and out["state"] == "approved"
+    assert out["approvals"]["label"]["reason"] == "ok"
+    assert out["approvals"]["label"]["actor_id"] == entry["approver_id"]
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 0e7a1568d..af921c11a 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -282,7 +282,7 @@ RULE_PHRASES = {
     "git-github-ownership": (
         None,
         [
-            "Every such action targets `IronbellyOrg/IronClaude`",
+            "Every such action targets the repo the issue belongs to (`IronbellyOrg/IronClaude` for this repository)",
             "PRs go only through `/sc:pr-submit --monitor 3`",
             "Before any push that would publish worker commits the person has not seen",
             "stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run",
@@ -3384,3 +3384,80 @@ def test_issue_pipeline_duties_allow_no_typing_into_a_worker_prompt():
     section = _contract().split("### Issue pipeline duties", 1)[1].split("\n### ", 1)[0]
     assert "terminal send" not in section
     assert "types nothing into a worker's terminal" in section
+
+
+# --- issue pipeline duties and the push rule (plan Task 11) -----------------------
+
+
+def _duties() -> str:
+    text = _contract()
+    start = text.index("### Issue pipeline duties")
+    return text[start : text.index("### Worked example", start)]
+
+
+def _ownership() -> str:
+    text = _contract()
+    start = text.index("### Git and GitHub ownership")
+    return text[start : text.index("### Reading a result", start)]
+
+
+def test_the_push_rule_names_full_submit_and_grants_the_coordinator_nothing_on_the_pipeline():
+    section = _ownership()
+    assert (
+        "At Full Submit the launched agent pushes only its own feature branch to origin "
+        "and opens the pull request through /sc:pr-submit; the owner's Pipeline value "
+        "plus an approval later than the last Project change is the go for that issue "
+        "only. The coordinator never pushes worker commits on that basis; for every "
+        "other push the rule above stands."
+    ) in section
+    assert "pushes only on the person's go" in section
+    # no sentence grants the coordinator a push because of the Pipeline value
+    for sentence in re.split(r"(?<=[.;])\s+", section):
+        if "Pipeline" in sentence and "push" in sentence:
+            assert "never pushes worker commits on that basis" in sentence or (
+                "launched agent pushes only its own feature branch" in sentence
+            ), sentence
+
+
+def test_every_outward_action_targets_the_repo_the_issue_belongs_to():
+    section = _ownership()
+    assert "targets the repo the issue belongs to" in section
+    assert "never the SuperClaude upstream" in section
+
+
+def test_the_duties_cover_claims_at_every_level():
+    duties = _duties()
+    assert "--pipeline <level> --stage <stage>" in duties and "(any level)" in duties
+    assert (
+        "apply only to an issue that the issue watcher claimed with `/sc:issue --claim <N> --pipeline none`"
+        not in duties
+    )
+
+
+def test_the_duties_name_the_status_to_command_table_and_the_brief_at_level_none_only():
+    duties = _duties()
+    for command in (
+        "`/sc:research`",
+        "`/sc:design`",
+        "`/sc:brainstorm`",
+        "`/sc:workflow`",
+        "`/sc:troubleshoot` without `--fix`",
+    ):
+        assert command in duties, command
+    assert "level `none` only" in duties and "no brief has a level slot" in duties
+    assert "needs a fresh `Approved` field set to Yes" in duties
+
+
+def test_the_duties_read_the_status_through_stage_status_with_the_issues_repo():
+    duties = _duties()
+    assert duties.count("stage-status --repo <the issue's repo>") == 2
+
+
+def test_the_duties_name_the_claim_time_approval_and_the_adoption_row_as_the_automatic_record():
+    duties = _duties()
+    assert "claim-time approval kept in `dispatch.json` plus the adoption row" in duties
+    assert "never the plan-hash row" in duties and "`label-before-plan`" in duties
+    assert (
+        "only when the worker's `ask` carries the plan hash and `stage-status` "
+        "reports the approval as accepted"
+    ) in duties

Task 11 context. The brief API changed from build(issue, type, complexity, nonce) to build(issue, stage, route=None, nonce=None): one row per allowed Status at level none, plus two routes for Spec chosen from the `spec-route:` line of issue-summary.md (the Spec judgment is made by the claim worker, as docs/designs/issue-watcher-status-pipelines.md section 6 decides; no code judges it). Claim-time cases are tested through the code that enforces them (stage_predicates, stage-status) with a dispatch.json fixture; approval_record.py and stage_predicates.py are not changed by design. The duties text names `stage-status --repo` (Task 15 implements the flag). `.claude/` copies come from `make sync-dev` and are not staged. Tests run: tests/skills tests/issue_pipeline tests/commands tests/hooks/test_launch_level_guard_worker.py: 2912 passed.

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
