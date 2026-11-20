b7f78e146c3cd9609e42262d6d9f1255269308b6
Review one task for spec compliance.

Task brief: ## Task 9: Add the warn-only self-approval exclusion

Depends on: Task 7

In `src/superclaude/cli/issue_watch/predicates.py` add a keyword `excluded_ids: Collection[int] = ()` to `approval_of` (line 185); an approval whose `actor_id` is in that set returns `not_approved`, checked next to the approver test (lines 216 to 223). In `src/superclaude/cli/issue_watch/cycle.py` add one closed-set key `approval_excluded_ids` (a list of integers, default empty) to `_TOP_KEYS` (line 58), `Config` and `load_config`, and pass it at both call sites of `approval_of` (`_approve`, line 883, and `_revalidate`, line 998). With the default empty list nothing changes. In `src/superclaude/cli/issue_watch/cli.py` make `check-config` (lines 185 to 198, which prints only "configuration is valid" and three info lines today) print one warning line `approver_is_launch_account` when the approvers file holds the config's own account id (`self.account_id`, `cycle.py` lines 767 to 768). The hand-written config for this host lists account 7361222 both as the account and as an approver, so the warning shows there. The Task 19 generator never writes the account id into a generated approvers file, and the Task 21 first-run report prints the same warning (those tasks name it).

Acceptance criteria:
- T9.AC1: `tests/issue_watch/test_predicates.py` shows an approval by an excluded id returns `not_approved` and the same event by another approver passes.
- T9.AC2: `tests/issue_watch/test_cycle.py` shows a launch-account approval at examine time gives no launch when the key lists that account, and none when the approval appears between examine and launch; with the default empty list the same approval launches as before.
- T9.AC3: `tests/issue_watch/test_cli.py` shows `check-config` prints `approver_is_launch_account` for an approvers file that holds the account and does not print it otherwise, and an unknown config key is still rejected.
- T9.AC4: `uv run pytest tests/issue_watch -q` passes.
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
Start sha: b7f78e146c3cd9609e42262d6d9f1255269308b6
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/cli.py b/src/superclaude/cli/issue_watch/cli.py
index fc7d4027a..445774de3 100644
--- a/src/superclaude/cli/issue_watch/cli.py
+++ b/src/superclaude/cli/issue_watch/cli.py
@@ -199,6 +199,17 @@ def check_config_command(config_path: Path) -> None:
     click.echo(f"state_dir: {config.state_dir}")
     click.echo(f"approvers_file mtime: {mtime}")
     click.echo(f"approvers_file entries: {count}")
+    # The launch account is also an approver: its own approval would count (R33).
+    # Setting approval_excluded_ids in the configuration excludes it.
+    try:
+        approvers = cycle.validate_approvers(config.approvers_file)
+    except cycle.ConfigError as exc:
+        _config_exit(exc)
+    if (
+        config.owner_account_id in approvers
+        and config.owner_account_id not in config.approval_excluded_ids
+    ):
+        click.echo("warning: approver_is_launch_account")
 
 
 @issue_watch_group.command("init-state")
diff --git a/src/superclaude/cli/issue_watch/cycle.py b/src/superclaude/cli/issue_watch/cycle.py
index 0848ab435..a8c165ae7 100644
--- a/src/superclaude/cli/issue_watch/cycle.py
+++ b/src/superclaude/cli/issue_watch/cycle.py
@@ -66,6 +66,7 @@ _TOP_KEYS = frozenset(
         "worktree",
         "approvers_file",
         "state_dir",
+        "approval_excluded_ids",
     }
 )
 _LABEL_KEYS = frozenset({"trigger", "approval"})
@@ -106,6 +107,8 @@ class Config:
     worktree: Path
     approvers_file: Path
     state_dir: Path
+    approval_excluded_ids: frozenset[int] = frozenset()
+    """Account ids whose approval never counts (R33); empty by default."""
 
 
 def _invalid(detail: str) -> ConfigError:
@@ -259,6 +262,14 @@ def load_config(path: str | os.PathLike[str]) -> Config:
     ):
         raise _invalid("owner_account_id must be an integer from 1 to 10**20-1")
 
+    excluded = raw.get("approval_excluded_ids", [])
+    if not isinstance(excluded, list) or not all(
+        _is_int(i) and 1 <= i <= _ACCOUNT_ID_MAX for i in excluded
+    ):
+        raise _invalid(
+            "approval_excluded_ids must be a list of integers from 1 to 10**20-1"
+        )
+
     for key in ("worktree", "approvers_file"):
         if not _is_abs_path(raw.get(key)):
             raise _invalid(f"{key} must be an absolute path (a ~ is not expanded)")
@@ -285,6 +296,7 @@ def load_config(path: str | os.PathLike[str]) -> Config:
         worktree=Path(raw["worktree"]),
         approvers_file=Path(raw["approvers_file"]),
         state_dir=state_dir,
+        approval_excluded_ids=frozenset(excluded),
     )
 
 
@@ -916,6 +928,7 @@ class _Cycle:
             approval_label=cfg.approval_label,
             approvers=self.approvers,
             store_created_at=self.doc.created_at,
+            excluded_ids=cfg.approval_excluded_ids,
         )
         if not result.approved:
             raise _Skip(fallback or result.reason or "not_approved")
@@ -1047,6 +1060,7 @@ class _Cycle:
             approval_label=cfg.approval_label,
             approvers=self.approvers,
             store_created_at=self.doc.created_at,
+            excluded_ids=cfg.approval_excluded_ids,
         )
         # A voided approval, or a newer approval event (edits are not re-read), fails.
         if (
diff --git a/src/superclaude/cli/issue_watch/predicates.py b/src/superclaude/cli/issue_watch/predicates.py
index d235c476f..908978a5d 100644
--- a/src/superclaude/cli/issue_watch/predicates.py
+++ b/src/superclaude/cli/issue_watch/predicates.py
@@ -227,11 +227,13 @@ def approval_of(
     approval_label: str,
     approvers: Collection[int],
     store_created_at: datetime,
+    excluded_ids: Collection[int] = (),
 ) -> ApprovalResult:
     """Apply spec Section 3 "Approved by a human" checks (a) to (e).
 
     ``events`` must be the complete event history; absent evidence never
-    counts as positive.
+    counts as positive. An approval whose actor is in ``excluded_ids`` is no
+    approval (R33: the owner's way to exclude the launch account).
     """
     ordered = sorted(events, key=lambda e: (e.created_at, e.id))
     appr_on = [e for e in ordered if e.event == "labeled" and e.label == approval_label]
@@ -256,6 +258,7 @@ def approval_of(
         or approval.actor_login.endswith("[bot]")
         or type(approval.actor_id) is not int
         or approval.actor_id not in approvers
+        or approval.actor_id in excluded_ids
     ):
         return _not_approved("not_approved")
     # OQ-38: no trigger `labeled` event means check (c) cannot pass; this also
diff --git a/tests/issue_watch/test_cli.py b/tests/issue_watch/test_cli.py
index a47e12dfc..4a5b8ed5b 100644
--- a/tests/issue_watch/test_cli.py
+++ b/tests/issue_watch/test_cli.py
@@ -375,6 +375,49 @@ def test_check_config_prints_the_mtime_and_count_and_writes_nothing(
     assert not config.state_dir.exists()
 
 
+def test_check_config_warns_when_an_approver_is_the_launch_account__r33(
+    tmp_path, config, config_file
+):
+    """R33: the warning shows when the approvers file holds the account id."""
+    config.approvers_file.write_text("1001\n7654321\n", "utf-8")
+    write_config(config_file, config, owner_account_id=1001)
+    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
+    assert result.exit_code == 0
+    assert "warning: approver_is_launch_account\n" in result.output
+    assert "1001" not in result.output
+
+
+def test_check_config_has_no_warning_otherwise__r33(tmp_path, config, config_file):
+    config.approvers_file.write_text("7654321\n", "utf-8")
+    write_config(config_file, config, owner_account_id=1001)
+    quiet = run_readonly(tmp_path, "check-config", "--config", str(config_file))
+    assert "approver_is_launch_account" not in quiet.output
+    # No account id in the configuration: nothing to compare.
+    config.approvers_file.write_text("1001\n", "utf-8")
+    write_config(config_file, config)
+    unset = run_readonly(tmp_path, "check-config", "--config", str(config_file))
+    assert "approver_is_launch_account" not in unset.output
+    # Excluded by the owner: no warning either.
+    write_config(
+        config_file, config, owner_account_id=1001, approval_excluded_ids=[1001]
+    )
+    excluded = run_readonly(tmp_path, "check-config", "--config", str(config_file))
+    assert excluded.exit_code == 0
+    assert "approver_is_launch_account" not in excluded.output
+
+
+def test_an_unknown_config_key_is_still_rejected_and_the_exclusion_key_is_checked__r33(
+    tmp_path, config, config_file
+):
+    write_config(config_file, config, extra_key=1)
+    bad_key = run_readonly(tmp_path, "check-config", "--config", str(config_file))
+    assert bad_key.exit_code == 2
+    for bad in ("1001", [0], ["1001"], [True], [10**21]):
+        write_config(config_file, config, approval_excluded_ids=bad)
+        out = run_readonly(tmp_path, "check-config", "--config", str(config_file))
+        assert out.exit_code == 2, bad
+
+
 def _bad_config(tmp_path, config, config_file):
     write_config(config_file, config, project_id="not-a-project")
 
diff --git a/tests/issue_watch/test_cycle.py b/tests/issue_watch/test_cycle.py
index fef113db5..1a595ee79 100644
--- a/tests/issue_watch/test_cycle.py
+++ b/tests/issue_watch/test_cycle.py
@@ -2949,6 +2949,54 @@ def test_a_pipeline_lowered_with_a_time_after_the_approval_is_edited__r27_r31(
     assert deps.launcher.calls == []
 
 
+def test_a_launch_account_approval_launches_by_default__r33(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    world.issue(9)  # the default approver is the launch account's id
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
+
+
+def test_an_excluded_approval_gives_no_launch_at_examine_time__r33(
+    tmp_path, tmp_state, gh_world
+):
+    config = make_config(tmp_path, approval_excluded_ids=frozenset({APPROVER_ID}))
+    world = gh_world(config=config)
+    world.issue(9)
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "not_approved")]
+    assert deps.launcher.calls == []
+
+
+def test_an_excluded_approval_that_appears_before_launch_is_refused__r33(
+    tmp_path, tmp_state, gh_world
+):
+    """Another approver approves at examine time; the excluded account approves
+    later and becomes the latest approval, so the re-read refuses the launch."""
+    config = make_config(tmp_path, approval_excluded_ids=frozenset({APPROVER_ID}))
+    world = gh_world(config=config)
+    other = 4242
+    approvers = config.approvers_file
+    approvers.write_text(f"{APPROVER_ID}\n{other}\n", encoding="utf-8")
+    approvers.chmod(0o600)
+    first = _ev(world, approver=other)
+    later = label_event(
+        3,
+        "labeled",
+        world.config.approval_label,
+        T_APPROVED + timedelta(minutes=1),
+        actor_id=APPROVER_ID,
+        actor_login=OWN_LOGIN,
+    )
+    world.issue(9, events=first)
+    _on_nth(world, "events", 9, 2, lambda: world.update(9, events=[*first, later]))
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert deps.launcher.calls == []
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "revalidation_failed")]
+    assert tmp_state.load().entries == {}
+
+
 def test_a_real_label_named_issue_watch_approved_never_approves__r35(
     tmp_path, tmp_state, gh_world
 ):
diff --git a/tests/issue_watch/test_predicates.py b/tests/issue_watch/test_predicates.py
index 21e1d88cc..4b1a6846c 100644
--- a/tests/issue_watch/test_predicates.py
+++ b/tests/issue_watch/test_predicates.py
@@ -94,6 +94,25 @@ def decide(events, *, labels_now=(TRIGGER, APPROVAL), store_created_at=T0):
     )
 
 
+def test_r33_an_approval_by_an_excluded_id_is_not_approved() -> None:
+    """R33: the exclusion turns an allow-listed approver's approval into none."""
+    events = [trigger_on(), approval_on()]
+    common = dict(
+        labels_now=(TRIGGER, APPROVAL),
+        trigger_label=TRIGGER,
+        approval_label=APPROVAL,
+        approvers={APPROVER_ID, OUTSIDER_ID},
+        store_created_at=T0,
+    )
+    excluded = approval_of(events, excluded_ids={APPROVER_ID}, **common)
+    assert_skipped(excluded, "not_approved")
+    # The same event by another approver passes, and an empty exclusion changes nothing.
+    other = [trigger_on(), approval_on(actor_id=OUTSIDER_ID)]
+    assert approval_of(other, excluded_ids={APPROVER_ID}, **common).approved is True
+    assert approval_of(events, **common).approved is True
+    assert approval_of(events, excluded_ids=(), **common).approved is True
+
+
 def assert_skipped(result, reason: str) -> None:
     """Assert a not-approved result with ``reason`` and no approval fields."""
     assert result.approved is False


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (Grep, read): approval_of has exactly two call sites, cycle.py _approve and _revalidate, both in the diff; its new keyword defaults to an empty tuple. Config gained a defaulted last field, so every Config(...) constructor in tests and make_config is unaffected. check-config compares config.owner_account_id (the launch account, set by the owner in the config) with the approvers file, because check-config makes no gh call. Task 19 (generator) and Task 21 (first-run report) will name the same warning. Full run of tests/issue_watch and tests/issue_pipeline: 3017 passed.

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
