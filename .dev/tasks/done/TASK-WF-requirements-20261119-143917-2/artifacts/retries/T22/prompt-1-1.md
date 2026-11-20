d3850ca238d5d8c52d155e17cfc813c3983d05f7
Review one task for spec compliance.

Task brief: ## Task 22: Print the launched and attempted issue from `once`

Depends on: Task 7, Task 16

In `src/superclaude/cli/issue_watch/cli.py` `once_command` (line 118) currently prints `cycle: <reason>` and `exit: <code>`, and prints `would_launch` only in a dry run. Also print `launched: <issue number>` when the cycle launched an issue (`CycleResult.launched_issue`, `cycle.py` line 455) and `attempted: <issue number>` when a launch ended with an unknown outcome (requirement R26). Today `cycle.py` lines 1106 to 1109 return `launch_unknown` without setting `launched_issue`; add an `attempted_issue` field to `CycleResult`, set there. Print each line only once, and only the number, so the dispatcher can read it from a child's output.

Acceptance criteria:
- T22.AC1: `tests/issue_watch/test_cli.py` shows `launched: 12` appears after a confirmed launch, `attempted: 12` appears after an unknown outcome and neither appears otherwise; the existing outputs are unchanged.
- T22.AC2: `tests/issue_watch/test_cycle.py` shows `attempted_issue` is set for `launch_unknown` and for no other result.
- T22.AC3: `tests/issue_watch/test_no_text.py` still passes (each line contains a number only).
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
Start sha: d3850ca238d5d8c52d155e17cfc813c3983d05f7
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/cli.py b/src/superclaude/cli/issue_watch/cli.py
index 445774de3..76d655374 100644
--- a/src/superclaude/cli/issue_watch/cli.py
+++ b/src/superclaude/cli/issue_watch/cli.py
@@ -129,6 +129,11 @@ def once_command(dry_run: bool, config_path: Path) -> None:
         sys.exit(_EXIT_CRASH)
     click.echo(f"cycle: {result.reason}")
     click.echo(f"exit: {result.exit_code}")
+    # One line each, only the number: the dispatcher reads these from a child's output (R26).
+    if result.launched_issue is not None:
+        click.echo(f"launched: {result.launched_issue}")
+    if result.attempted_issue is not None:
+        click.echo(f"attempted: {result.attempted_issue}")
     if dry_run:
         if result.probe is not None:
             click.echo(f"probe: {result.probe}")
diff --git a/src/superclaude/cli/issue_watch/cycle.py b/src/superclaude/cli/issue_watch/cycle.py
index ff8947c45..ad7457975 100644
--- a/src/superclaude/cli/issue_watch/cycle.py
+++ b/src/superclaude/cli/issue_watch/cycle.py
@@ -481,6 +481,8 @@ class CycleResult:
     would_launch: int | None = None
     probe: str | None = None
     lines: tuple[dict, ...] = ()
+    attempted_issue: int | None = None
+    """The issue whose launch ended with an unknown outcome (R26); None otherwise."""
 
 
 # Exit precedence (design 4.3, OD-10).
@@ -587,6 +589,7 @@ class _Cycle:
         self.examined: list[int] = []
         self.halt = False
         self.launched_issue: int | None = None
+        self.attempted_issue: int | None = None
         self.would_launch: int | None = None
         self.shadow: record.DryRunDoc | None = None
         self.shadow_reset = False
@@ -1210,6 +1213,7 @@ class _Cycle:
             return "launched", "launched"
         if outcome.kind == "unknown":
             self._set(record.mark_unknown(self.doc, c.n, outcome.operation_id, now))
+            self.attempted_issue = c.n
             self._cond("launch_unknown")
             return "launch_unknown", "unknown"
         self._set(record.mark_spawn_error(self.doc, c.n, now))
@@ -1313,6 +1317,7 @@ class _Cycle:
             would_launch=self.would_launch,
             probe="skipped" if self.would_launch is not None else None,
             lines=lines,
+            attempted_issue=self.attempted_issue,
         )
 
 
diff --git a/tests/issue_watch/test_cli.py b/tests/issue_watch/test_cli.py
index 4a5b8ed5b..5de92c64d 100644
--- a/tests/issue_watch/test_cli.py
+++ b/tests/issue_watch/test_cli.py
@@ -568,7 +568,50 @@ def test_once_without_dry_run_prints_no_probe_or_would_launch_line(
     )
     result = run("once", "--config", str(config_file))
     assert result.exit_code == 0
-    assert result.output == "cycle: launched\nexit: 0\n"
+    # a confirmed launch adds one `launched: <n>` line; probe and would_launch stay dry-run only
+    assert result.output == "cycle: launched\nexit: 0\nlaunched: 42\n"
+
+
+def _fake_result(monkeypatch, **fields):
+    monkeypatch.setattr(cli, "build_deps", lambda cfg: object())
+    monkeypatch.setattr(
+        cycle,
+        "run_cycle",
+        lambda deps, dry_run: cycle.CycleResult(
+            exit_code=fields.pop("exit_code", 0),
+            reason=fields.pop("reason", "launched"),
+            cycle_id="0" * 32,
+            **fields,
+        ),
+    )
+
+
+def test_once_prints_launched_after_a_confirmed_launch(config_file, monkeypatch):
+    _fake_result(monkeypatch, launched_issue=12)
+    result = run("once", "--config", str(config_file))
+    lines = result.output.splitlines()
+    assert lines.count("launched: 12") == 1
+    assert not any(line.startswith("attempted:") for line in lines)
+
+
+def test_once_prints_attempted_after_an_unknown_outcome(config_file, monkeypatch):
+    _fake_result(monkeypatch, exit_code=7, reason="launch_unknown", attempted_issue=12)
+    result = run("once", "--config", str(config_file))
+    lines = result.output.splitlines()
+    assert result.exit_code == 7
+    assert lines.count("attempted: 12") == 1
+    assert not any(line.startswith("launched:") for line in lines)
+
+
+def test_once_prints_neither_line_when_nothing_was_launched(config_file, monkeypatch):
+    _fake_result(monkeypatch, reason="not_approved")
+    result = run("once", "--config", str(config_file))
+    assert result.output == "cycle: not_approved\nexit: 0\n"
+    _fake_result(monkeypatch, reason="not_approved", would_launch=12, probe="skipped")
+    dry = run("once", "--dry-run", "--config", str(config_file))
+    assert dry.output == (
+        "cycle: not_approved\nexit: 0\nprobe: skipped\nwould_launch: 12\n"
+    )
 
 
 def test_once_on_a_config_error_writes_the_fallback_and_exits_2(
diff --git a/tests/issue_watch/test_cli_e2e.py b/tests/issue_watch/test_cli_e2e.py
index c27941064..b53f749fe 100644
--- a/tests/issue_watch/test_cli_e2e.py
+++ b/tests/issue_watch/test_cli_e2e.py
@@ -348,7 +348,8 @@ def test_fr010_fr013_eligible_issue_launches_once_through_orca_ide(tmp_path, stu
     done = watcher.cli("once")
 
     assert done.returncode == 0, done
-    assert done.stdout == "cycle: cycle_complete\nexit: 0\n", done.stdout
+    # the confirmed launch prints its issue number once (plan Task 22, R26)
+    assert done.stdout == "cycle: cycle_complete\nexit: 0\nlaunched: 9\n", done.stdout
     assert done.stderr == ""
     calls = watcher.calls()
     # every external call, in order; the stub never sees the program path
@@ -412,7 +413,10 @@ def test_nfr010_second_once_launches_nothing(tmp_path, stub_path):
     )
 
     first = watcher.cli("once")
-    assert (first.returncode, first.stdout) == (0, "cycle: cycle_complete\nexit: 0\n")
+    assert (first.returncode, first.stdout) == (
+        0,
+        "cycle: cycle_complete\nexit: 0\nlaunched: 9\n",
+    )
     first_calls = len(watcher.calls())
     entry_after_first = watcher.store()["entries"][str(ISSUE)]
     assert entry_after_first["state"] == "launched"
diff --git a/tests/issue_watch/test_cycle.py b/tests/issue_watch/test_cycle.py
index dbe874a92..d636d13d7 100644
--- a/tests/issue_watch/test_cycle.py
+++ b/tests/issue_watch/test_cycle.py
@@ -5399,3 +5399,44 @@ def test_a_repo_key_is_read_and_must_be_owner_slash_name(tmp_path):
         with pytest.raises(cycle.ConfigError) as err:
             cycle.load_config(_config_file(tmp_path, repo=bad))
         assert err.value.reason == "config_invalid"
+
+
+# --- attempted_issue (plan Task 22, R26) ---------------------------------------------
+
+
+@pytest.mark.parametrize(("outcome", "operation_id"), _UNKNOWN_OUTCOMES)
+def test_attempted_issue_is_set_for_an_unknown_launch(
+    tmp_path, tmp_state, gh_world, outcome, operation_id
+):
+    world = gh_world()
+    world.issue(9)
+    res, _ = _run(tmp_path, tmp_state, world, launcher=FakeLauncher([outcome()]))
+    assert (res.reason, res.attempted_issue, res.launched_issue) == (
+        "launch_unknown",
+        9,
+        None,
+    )
+
+
+def test_attempted_issue_is_none_for_a_confirmed_launch(tmp_path, tmp_state, gh_world):
+    world = gh_world()
+    world.issue(9)
+    res, _ = _run(tmp_path, tmp_state, world)
+    assert (res.launched_issue, res.attempted_issue) == (9, None)
+
+
+def test_attempted_issue_is_none_for_a_spawn_error_and_for_no_launch(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    world.issue(9)
+    spawn = FakeLauncher([spawn_error_outcome()])
+    res, _ = _run(tmp_path, tmp_state, world, launcher=spawn)
+    assert (res.reason, res.attempted_issue, res.launched_issue) == (
+        "spawn_error",
+        None,
+        None,
+    )
+    empty = gh_world()
+    res, _ = _run(tmp_path, tmp_state, empty)
+    assert (res.attempted_issue, res.launched_issue) == (None, None)

Task 22 context. once prints `launched: <n>` and `attempted: <n>` after `exit:`; CycleResult gained attempted_issue (None except for a launch_unknown). Two end-to-end tests and one cli test that pinned the old output for a confirmed launch were updated on purpose, because the task adds the launched line. Tests run: tests/issue_watch tests/issue_pipeline passed; ruff clean; make verify-sync clean.

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
