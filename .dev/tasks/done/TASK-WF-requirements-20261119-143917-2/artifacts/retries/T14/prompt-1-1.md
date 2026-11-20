1920d470d202411c28f98aacd43342834ff44cce
Review one task for spec compliance.

Task brief: ## Task 14: Add the coordinator-only `complete` verb and make the coordinator call it

Depends on: Task 10, Task 11, Task 12, Task 13

In `src/superclaude/cli/issue_pipeline/cli.py` add an `issue-pipeline complete` verb (next to `release-worker` at line 200 and `stage-status` at line 335) that calls Task 12 and prints one closed result word. It takes `--repo`, `--issue`, `--project-id`, `--run` (the approval event id) and the outcome; the coordinator copies the project id from the repo's watcher config. Update `src/superclaude/core/WORKER-CONTRACT.md` section "Issue pipeline duties" so the coordinator runs the verb under the issue's grant row after it has read a worker's `worker_done` contract (level None) or a launched agent's result file (other levels), per Task 6, and passes the run id. The duties section states that a failed outcome never moves the Status and that the guard pattern of Task 13 is best effort. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- T14.AC1: A new `tests/issue_pipeline/test_complete_cli.py` covers the verb: a succeeded call prints the closed success word, a refused call prints a `refused:` word and exits 1, the project id and run id are passed through, and no verb output holds issue text.
- T14.AC2: The duties section names the verb, the grant-row rule and the rule that a failed outcome never moves the Status; `tests/skills/test_worker_contract.py` is updated and `uv run pytest tests/hooks tests/skills tests/issue_pipeline -q` passes.
- T14.AC3: `make verify-sync` is clean and no `.claude/` path is staged.
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
Start sha: 1920d470d202411c28f98aacd43342834ff44cce
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/cli.py b/src/superclaude/cli/issue_pipeline/cli.py
index b02ee636a..4cb43b359 100644
--- a/src/superclaude/cli/issue_pipeline/cli.py
+++ b/src/superclaude/cli/issue_pipeline/cli.py
@@ -20,6 +20,7 @@ from superclaude.cli.issue_watch.runner import Runner, SubprocessRunner
 from . import (
     approval_line,
     approval_record,
+    complete,
     plan_hash,
     reads,
     release,
@@ -214,14 +215,54 @@ def release_worker_command(session_id: str, store: Path | None) -> None:
         raise SystemExit(_EXIT_REFUSED) from None
 
 
-# --- stage-status: read-only -------------------------------------------------
-
-
 def _make_runner() -> Runner:
     """The one place a real ``gh`` runner is made (tests replace it)."""
     return SubprocessRunner()
 
 
+# --- complete: the coordinator's result comment and Status move ---------------
+
+
+@issue_pipeline_group.command("complete")
+@click.option("--repo", required=True, help="owner/name of the issue's repository.")
+@click.option("--issue", type=int, required=True)
+@click.option(
+    "--project-id",
+    required=True,
+    help="The Project node id (PVT_...), copied from the repo's watcher config.",
+)
+@click.option("--run", "run_id", type=int, required=True, help="The approval event id.")
+@click.option("--outcome", required=True, help="succeeded, failed, blocked or partial.")
+@click.option(
+    "--summary",
+    type=click.Path(),
+    default=None,
+    help="The closed three-line result file (outcome, artifacts, pull_request).",
+)
+def complete_command(
+    repo: str,
+    issue: int,
+    project_id: str,
+    run_id: int,
+    outcome: str,
+    summary: str | None,
+) -> None:
+    """Post the run's result comment and, for `succeeded`, move the Status (coordinator only).
+
+    Run it only under the issue's grant row, after reading the worker's contract or the
+    launched agent's result file. A failed, blocked or partial outcome never moves the Status.
+    """
+    word = complete.complete(
+        repo, issue, project_id, run_id, outcome, summary, _make_runner()
+    )
+    click.echo(word)
+    if word.startswith(("refused:", "failed:")):
+        raise SystemExit(_EXIT_REFUSED)
+
+
+# --- stage-status: read-only -------------------------------------------------
+
+
 def _load_stage_inputs(config_path: Path) -> tuple[str, frozenset[int]]:
     """The approval label and the approver ids of the watcher's configuration."""
     config = cycle.load_config(config_path)
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 385ca2e3e..07066a99d 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -298,6 +298,7 @@ These duties apply only to an issue that the issue watcher claimed with `/sc:iss
 - **Worktree, then worker.** Run the existing worktree step of the installed `sc-issue-protocol` skill (the script orca_worktree.py, subcommand worktree, with `--repo <R> --number <N> --base origin/<B> --source <the claim's issue folder>`), which creates or reuses the worktree with no agent, then run `worker-start --worktree path:<exact path it printed> --agent claude --spec <the worker brief for the issue>` straight after it.
 - **Plan approval.** The worker asks once with the plan path, file list and plan hash. Post the plan reply with the hash and file list and mention the assignee, then read GitHub through `stage-status --repo <the issue's repo>` at each gate or wake. The automatic approval record is the claim-time approval kept in `dispatch.json` plus the adoption row; it is never the plan-hash row, and `stage-status` refuses a claim-time approval dated before the plan reply (`label-before-plan`). Create the plan-hash approval row (`record-create`) only when the worker's `ask` carries the plan hash and `stage-status` reports the approval as accepted. On approval write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status; mark the row `instructed` and then, from the worker's ack, `acked` (`record-mark`).
 - **Route B adds no exception to "never answer a person prompt".** The worker's plan boundary is crossed by the reply to its own `ask`, which is not a person prompt, so the coordinator types nothing into a worker's terminal for this flow.
+- **Completion.** After the coordinator has read a level-`none` worker's `worker_done` contract, or a launched agent's result file `.dev/issues/<N>/result.md` (noticed through the `/sc:sweep` report it already reads, WC-16), it runs `superclaude issue-pipeline complete --repo <the issue's repo> --issue <N> --project-id <the Project id from the repo's watcher config> --run <the approval event id of this run, from the issue's dispatch.json entry> --outcome <succeeded|failed|blocked|partial> [--summary <the result file>]`, only under that issue's grant row. The verb prints one closed word (a `refused:` or `failed:` word exits 1) and echoes no issue text. It posts one result comment per run; only `succeeded` moves the Status, to In review, and a failed, blocked or partial outcome never moves the Status. A worker and a launched agent never run this verb. The launch-level guard refuses it by a text pattern that is best effort; the grant-row rule is the control.
 - **Never:** tell a worker to pass its plan boundary without an approval row; act on a Status move alone; relaunch a dead worker by itself (WC-6 and the person decide); post an issue write without that issue's grant row.
 
 ### Worked example: gate hit, answer, new Task
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index af921c11a..b26181447 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -3461,3 +3461,18 @@ def test_the_duties_name_the_claim_time_approval_and_the_adoption_row_as_the_aut
         "only when the worker's `ask` carries the plan hash and `stage-status` "
         "reports the approval as accepted"
     ) in duties
+
+
+def test_the_duties_name_the_complete_verb_the_grant_row_and_the_failed_outcome_rule():
+    duties = _duties()
+    assert "superclaude issue-pipeline complete --repo" in duties
+    assert "--project-id" in duties and "--run <the approval event id" in duties
+    assert "only under that issue's grant row" in duties
+    assert (
+        "only `succeeded` moves the Status, to In review, and a failed, blocked or "
+        "partial outcome never moves the Status"
+    ) in duties
+    assert "A worker and a launched agent never run this verb" in duties
+    assert "best effort; the grant-row rule is the control" in duties
+    # it runs after the worker's contract (level none) or the launched agent's result file
+    assert "`worker_done` contract" in duties and ".dev/issues/<N>/result.md" in duties
diff --git a/tests/issue_pipeline/test_complete_cli.py b/tests/issue_pipeline/test_complete_cli.py
new file mode 100644
index 000000000..c17ecc698
--- /dev/null
+++ b/tests/issue_pipeline/test_complete_cli.py
@@ -0,0 +1,133 @@
+"""Task 14: the coordinator-only ``issue-pipeline complete`` verb."""
+
+from __future__ import annotations
+
+from pathlib import Path
+
+import pytest
+from click.testing import CliRunner
+
+from superclaude.cli.issue_pipeline import cli as cli_mod
+from superclaude.cli.issue_pipeline import complete
+from superclaude.cli.issue_pipeline.cli import issue_pipeline_group
+from tests.issue_pipeline.test_complete import (
+    CANARY,
+    ISSUE,
+    PROJECT,
+    REPO,
+    RUN,
+    World,
+    node,
+)
+
+
+def invoke(world: World, monkeypatch, *extra: str, **over: str):
+    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
+    args = {
+        "--repo": REPO,
+        "--issue": str(ISSUE),
+        "--project-id": PROJECT,
+        "--run": str(RUN),
+        "--outcome": "succeeded",
+    }
+    args.update(over)
+    argv = ["complete", *(x for kv in args.items() for x in kv), *extra]
+    return CliRunner().invoke(issue_pipeline_group, argv)
+
+
+def test_a_succeeded_call_prints_the_closed_success_word(monkeypatch) -> None:
+    world = World(node(status="Plan"))
+    result = invoke(world, monkeypatch)
+    assert result.exit_code == 0 and result.output == "completed\n"
+    assert len(world.posts) == 1 and len(world.mutations) == 1
+
+
+def test_a_failed_outcome_prints_commented_and_moves_nothing(monkeypatch) -> None:
+    world = World(node(status="Plan"))
+    result = invoke(world, monkeypatch, **{"--outcome": "failed"})
+    assert result.exit_code == 0 and result.output == "commented\n"
+    assert world.mutations == []
+
+
+def test_a_person_moved_status_exits_zero_with_its_word(monkeypatch) -> None:
+    result = invoke(World(node(status="Done")), monkeypatch)
+    assert result.exit_code == 0 and result.output == "status_moved_by_person\n"
+
+
+@pytest.mark.parametrize(
+    "over,word",
+    [
+        ({"--outcome": "done"}, "refused:bad_outcome"),
+        ({"--issue": "0"}, "refused:bad_issue"),
+        ({"--project-id": "PVT_x y"}, "refused:bad_project_id"),
+        ({"--repo": "SuperClaude-Org"}, "refused:bad_repo"),
+        ({"--run": "0"}, "refused:bad_run"),
+    ],
+)
+def test_a_refused_call_prints_a_refused_word_and_exits_one(
+    monkeypatch, over: dict, word: str
+) -> None:
+    world = World()
+    result = invoke(world, monkeypatch, **over)
+    assert result.exit_code == 1 and result.output == f"{word}\n"
+    assert world.argvs == []
+
+
+def test_a_project_the_issue_is_not_on_is_refused_with_exit_one(monkeypatch) -> None:
+    world = World(node("PVTI_other", "PVT_other", "Plan"))
+    result = invoke(world, monkeypatch)
+    assert result.exit_code == 1 and result.output == "refused:project_missing\n"
+    assert world.posts == [] and world.mutations == []
+
+
+def test_a_failed_move_prints_a_failed_word_and_exits_one(monkeypatch) -> None:
+    world = World(node(status="Plan"))
+    world.fail_move = True
+    result = invoke(world, monkeypatch)
+    assert result.exit_code == 1 and result.output == "failed:status_move\n"
+    assert len(world.posts) == 1  # the comment stays
+
+
+def test_the_project_id_and_run_id_are_passed_through(monkeypatch) -> None:
+    world = World(node("PVTI_a", "PVT_other", "Plan"), node("PVTI_b", PROJECT, "Plan"))
+    result = invoke(world, monkeypatch, **{"--run": "777"})
+    assert result.exit_code == 0
+    assert f"projectId={PROJECT}" in world.mutations[0]
+    assert "itemId=PVTI_b" in world.mutations[0]
+    assert complete.result_marker(ISSUE, 777) in world.posts[0]
+    assert f"issues/{ISSUE}/comments" in " ".join(
+        a for argv in world.argvs for a in argv if "POST" in argv
+    )
+
+
+def test_the_summary_file_is_read_and_no_issue_text_reaches_the_output(
+    monkeypatch, tmp_path: Path
+) -> None:
+    summary = tmp_path / "result.md"
+    summary.write_text("outcome: failed\nartifacts: a.md\npull_request: none\n")
+    world = World(node(status="Plan"))
+    world.other_comment("someone", f"{CANARY} a hostile comment")
+    result = invoke(world, monkeypatch, "--summary", str(summary))
+    assert result.exit_code == 0 and CANARY not in result.output
+    assert "Artifacts: a.md" in world.posts[0]
+    bad = tmp_path / "bad.md"
+    bad.write_text(f"outcome: failed\nartifacts: {CANARY} x\npull_request: none\n")
+    result = invoke(World(), monkeypatch, "--summary", str(bad))
+    assert result.output == "refused:bad_summary\n" and CANARY not in result.output
+
+
+def test_every_printed_word_is_a_closed_word(monkeypatch) -> None:
+    for status in ("Plan", "Done"):
+        out = invoke(World(node(status=status)), monkeypatch).output.strip()
+        assert out in complete.RESULT_WORDS
+    assert (
+        invoke(World(), monkeypatch, **{"--outcome": "x"}).output.strip()
+        in complete.RESULT_WORDS
+    )
+
+
+def test_the_verb_is_listed_in_the_group_help() -> None:
+    result = CliRunner().invoke(issue_pipeline_group, ["--help"])
+    assert "complete" in result.output
+    help_text = CliRunner().invoke(issue_pipeline_group, ["complete", "--help"]).output
+    assert "coordinator only" in help_text

Task 14 context. The verb lives in src/superclaude/cli/issue_pipeline/cli.py and calls complete.complete (Task 12). --issue and --run are plain ints so complete.py returns the closed refused: words instead of click usage errors. Tests run: tests/hooks tests/skills tests/issue_pipeline tests/issue_watch: 10070 passed, 15 skipped; make verify-sync clean; no .claude/ path staged.

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
