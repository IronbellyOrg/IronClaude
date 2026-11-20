fe4ba5ed49ff151df1c3ddcf8645953b67bd95b4
Review one task for spec compliance.

Task brief: ## Task 16: Add the repo to the config and use it for the origin check

Depends on: Task 7, Task 9, Task 15

In `src/superclaude/cli/issue_watch/cycle.py` add an optional `repo` key to `_TOP_KEYS` (line 58, which Task 9 also edits), to `Config` (line 97) and to `load_config` (line 195); when absent it defaults to `IronbellyOrg/IronClaude` so a hand-written config such as `/home/coder/.config/superclaude/issue-watch.json` stays valid. Pass `cfg.repo` from the cycle to every `github.*` call of Task 15. In `src/superclaude/cli/issue_watch/launch.py` change `check_origin` (line 233) and its use (`ORIGIN_REPO` line 50, compared at line 249; called from `cycle.py` `_origin_ok` line 670 and the launch step) to compare against the configured repo, case-insensitively as today. In `src/superclaude/cli/issue_pipeline/cli.py` make `stage-status --repo` optional (Task 15 made it required): when absent it takes the `repo` key of the chosen `--config` (which defaults to `IronbellyOrg/IronClaude` when the key is absent), and when both are given and differ the verb refuses with `refused:repo-mismatch`.

Acceptance criteria:
- T16.AC1: `tests/issue_watch/test_cycle.py` runs a cycle for a config with `repo` set to another name and shows every `gh` call carries it and the origin check uses it; a worktree whose origin names a different repo ends with `origin_mismatch`.
- T16.AC2: `tests/issue_watch/test_origin_parity.py` and `tests/issue_watch/test_launch.py` are updated and pass.
- T16.AC3: A config without `repo` behaves as before (existing tests pass unchanged).
- T16.AC4: `tests/issue_pipeline/test_stage_status.py` shows `stage-status --config <config with repo Other/Repo>` without `--repo` reads `Other/Repo`, with the hand-written config (no `repo` key) reads `IronbellyOrg/IronClaude`, and `--repo` naming a different repo than the config's is refused with `refused:repo-mismatch` before any call.
- T16.AC5: `uv run pytest tests/issue_watch -q` passes.
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
Start sha: fe4ba5ed49ff151df1c3ddcf8645953b67bd95b4
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/cli.py b/src/superclaude/cli/issue_pipeline/cli.py
index 68375c13a..bd2e64e9c 100644
--- a/src/superclaude/cli/issue_pipeline/cli.py
+++ b/src/superclaude/cli/issue_pipeline/cli.py
@@ -263,10 +263,17 @@ def complete_command(
 # --- stage-status: read-only -------------------------------------------------
 
 
-def _load_stage_inputs(config_path: Path) -> tuple[str, frozenset[int]]:
-    """The approval label and the approver ids of the watcher's configuration."""
+def _load_stage_inputs(config_path: Path) -> tuple[str, frozenset[int], str]:
+    """The approval label, the approver ids and the repo of the watcher's configuration.
+
+    The repo is the config's ``repo`` key, or ``IronbellyOrg/IronClaude`` when it is absent.
+    """
     config = cycle.load_config(config_path)
-    return config.approval_label, cycle.validate_approvers(config.approvers_file)
+    return (
+        config.approval_label,
+        cycle.validate_approvers(config.approvers_file),
+        config.repo,
+    )
 
 
 def _timeout() -> float | None:
@@ -378,9 +385,10 @@ class _StatusRefused(Exception):
 @click.argument("issue", type=click.IntRange(min=1))
 @click.option(
     "--repo",
-    required=True,
-    help="owner/name of the repository the issue belongs to (no default: a coordinator "
-    "for another repository must name it).",
+    default=None,
+    help="owner/name of the repository the issue belongs to. Default: the `repo` key of "
+    "--config (IronbellyOrg/IronClaude when the key is absent). When both are given and "
+    "differ, the verb refuses with refused:repo-mismatch before any call.",
 )
 @click.option(
     "--json",
@@ -415,7 +423,7 @@ class _StatusRefused(Exception):
 )
 def stage_status_command(
     issue: int,
-    repo: str,
+    repo: str | None,
     as_json: bool,
     config_path: Path,
     approvals_dir: Path | None,
@@ -423,14 +431,19 @@ def stage_status_command(
     plan_files: tuple[str, ...],
 ) -> None:
     """Print the plan-stage status of ISSUE as closed keys; writes nothing, prints no GitHub text."""
-    if not gh.valid_repo(repo):
+    if repo is not None and not gh.valid_repo(repo):
         click.echo("refused:bad-repo")
         raise SystemExit(_EXIT_REFUSED)
     try:
-        label, approvers = _load_stage_inputs(config_path.expanduser())
+        label, approvers, config_repo = _load_stage_inputs(config_path.expanduser())
     except cycle.ConfigError as exc:
         click.echo(f"refused:{exc.reason}")
         raise SystemExit(_EXIT_CONFIG) from None
+    if repo is None:
+        repo = config_repo
+    elif repo.lower() != config_repo.lower():
+        click.echo("refused:repo-mismatch")
+        raise SystemExit(_EXIT_REFUSED)
     try:
         result = _stage_status(
             issue,
diff --git a/src/superclaude/cli/issue_watch/cycle.py b/src/superclaude/cli/issue_watch/cycle.py
index a8c165ae7..ff8947c45 100644
--- a/src/superclaude/cli/issue_watch/cycle.py
+++ b/src/superclaude/cli/issue_watch/cycle.py
@@ -67,6 +67,7 @@ _TOP_KEYS = frozenset(
         "approvers_file",
         "state_dir",
         "approval_excluded_ids",
+        "repo",
     }
 )
 _LABEL_KEYS = frozenset({"trigger", "approval"})
@@ -109,6 +110,8 @@ class Config:
     state_dir: Path
     approval_excluded_ids: frozenset[int] = frozenset()
     """Account ids whose approval never counts (R33); empty by default."""
+    repo: str = github.REPO
+    """The ``owner/name`` the watcher serves; the fork when the key is absent."""
 
 
 def _invalid(detail: str) -> ConfigError:
@@ -270,6 +273,10 @@ def load_config(path: str | os.PathLike[str]) -> Config:
             "approval_excluded_ids must be a list of integers from 1 to 10**20-1"
         )
 
+    repo = raw.get("repo", github.REPO)
+    if not github.valid_repo(repo):
+        raise _invalid("repo must be owner/name (letters, digits, . _ - only)")
+
     for key in ("worktree", "approvers_file"):
         if not _is_abs_path(raw.get(key)):
             raise _invalid(f"{key} must be an absolute path (a ~ is not expanded)")
@@ -297,6 +304,7 @@ def load_config(path: str | os.PathLike[str]) -> Config:
         approvers_file=Path(raw["approvers_file"]),
         state_dir=state_dir,
         approval_excluded_ids=frozenset(excluded),
+        repo=repo,
     )
 
 
@@ -693,7 +701,8 @@ class _Cycle:
         None, so a ``Runner`` never gets one (design 8.5).
         """
         worktree = self.deps.config.worktree
-        return launch.check_origin(self.deps.runner, worktree, timeout) is None
+        repo = self.deps.config.repo
+        return launch.check_origin(self.deps.runner, worktree, timeout, repo) is None
 
     # -- the cycle -----------------------------------------------------------
 
@@ -812,7 +821,11 @@ class _Cycle:
     def _discover(self) -> tuple[DiscoveredIssue, ...]:
         cfg = self.deps.config
         read = github.discover(
-            self.deps.runner, cfg.trigger_label, self.login or "", self._tf_shared
+            self.deps.runner,
+            cfg.trigger_label,
+            self.login or "",
+            self._tf_shared,
+            repo=cfg.repo,
         )
         if read.reason is not None:
             if read.kind == "rate_limited":
@@ -873,12 +886,15 @@ class _Cycle:
             return self._rv(read) if reserved else self._val(read, fallback)
 
         # One after the other: a failed first read stops the cycle before the second.
+        repo = d.config.repo
         label_events = check(
-            github.events(d.runner, self.budget, n, self._tf, reserved=reserved)
+            github.events(
+                d.runner, self.budget, n, self._tf, reserved=reserved, repo=repo
+            )
         )
         field_events = check(
             github.approval_events(
-                d.runner, self.budget, n, self._tf, reserved=reserved
+                d.runner, self.budget, n, self._tf, reserved=reserved, repo=repo
             )
         )
         return predicates.merge_approval_events(label_events, field_events)  # type: ignore[arg-type]
@@ -944,7 +960,9 @@ class _Cycle:
         """A tombstone or a ``failed`` entry in backoff: find the approval floor."""
         d = self.deps
         markers = self._val(
-            github.marker_comments(d.runner, self.budget, c.n, self._tf)
+            github.marker_comments(
+                d.runner, self.budget, c.n, self._tf, repo=d.config.repo
+            )
         )
         events = self._events(c.n, fallback)
         approval = self._approve(c, events, fallback)
@@ -964,7 +982,9 @@ class _Cycle:
             or (state == "abandoned" and e.pending_at is not None)
         ):
             markers = self._val(
-                github.marker_comments(d.runner, self.budget, c.n, self._tf)
+                github.marker_comments(
+                    d.runner, self.budget, c.n, self._tf, repo=cfg.repo
+                )
             )
             if self._hit(markers, e.pending_at, None):
                 return self._claim(c, None)  # T-10
@@ -979,13 +999,15 @@ class _Cycle:
         if not owned:
             raise _Skip(why or "assigned_other")
         markers = self._val(
-            github.marker_comments(d.runner, self.budget, c.n, self._tf)
+            github.marker_comments(d.runner, self.budget, c.n, self._tf, repo=cfg.repo)
         )
         events = self._events(c.n)
         approval = self._approve(c, events)
         if self._hit(markers, None, approval.approved_at):
             return self._claim(c, approval)  # T-11, T-12
-        edits = self._val(github.edits(d.runner, self.budget, c.n, self._tf))
+        edits = self._val(
+            github.edits(d.runner, self.budget, c.n, self._tf, repo=cfg.repo)
+        )
         why = predicates.unchanged_since(
             approval.approved_at,  # type: ignore[arg-type]
             edits,  # type: ignore[arg-type]
@@ -994,7 +1016,9 @@ class _Cycle:
         )
         if why is not None:
             raise _Skip(why)
-        items = self._val(github.project_items(d.runner, self.budget, c.n, self._tf))
+        items = self._val(
+            github.project_items(d.runner, self.budget, c.n, self._tf, repo=cfg.repo)
+        )
         why = predicates.value_changed_after(
             items,  # type: ignore[arg-type]
             cfg.project_id,
@@ -1040,7 +1064,7 @@ class _Cycle:
         """
         d, cfg = self.deps, self.deps.config
         snap: predicates.IssueSnapshot = self._rv(  # type: ignore[assignment]
-            github.reread(d.runner, self.budget, c.n, self._tf)
+            github.reread(d.runner, self.budget, c.n, self._tf, repo=cfg.repo)
         )
         if (
             snap.state.lower() != "open"
@@ -1069,7 +1093,9 @@ class _Cycle:
         ):
             raise _Skip("revalidation_failed")
         items = self._rv(
-            github.project_items(d.runner, self.budget, c.n, self._tf, reserved=True)
+            github.project_items(
+                d.runner, self.budget, c.n, self._tf, reserved=True, repo=cfg.repo
+            )
         )
         why = predicates.value_changed_after(
             items,  # type: ignore[arg-type]
diff --git a/src/superclaude/cli/issue_watch/launch.py b/src/superclaude/cli/issue_watch/launch.py
index 07d57f6ec..ad68a9d24 100644
--- a/src/superclaude/cli/issue_watch/launch.py
+++ b/src/superclaude/cli/issue_watch/launch.py
@@ -272,9 +272,14 @@ def parse_origin(url: object) -> str | None:
 
 
 def check_origin(
-    runner: Runner, worktree: Path | str, timeout: float | None
+    runner: Runner,
+    worktree: Path | str,
+    timeout: float | None,
+    repo: str = ORIGIN_REPO,
 ) -> str | None:
-    """Return None when the worktree's origin is IronbellyOrg/IronClaude.
+    """Return None when the worktree's origin is ``repo`` (default IronbellyOrg/IronClaude).
+
+    The compare is case-insensitive, as GitHub names are.
 
     Otherwise return ``"origin_mismatch"``: a ``timeout`` of None (no process is
     started), a timed-out or failed ``git``, or an unparseable or foreign URL.
@@ -286,8 +291,8 @@ def check_origin(
     result = runner.run(argv, _check_timeout(timeout))
     if result.timed_out or result.spawn_error is not None or result.returncode != 0:
         return ORIGIN_MISMATCH
-    repo = parse_origin(result.stdout)
-    if repo is None or repo.lower() != ORIGIN_REPO:
+    found = parse_origin(result.stdout)
+    if found is None or found.lower() != repo.lower():
         return ORIGIN_MISMATCH
     return None
 
diff --git a/tests/issue_pipeline/test_stage_status.py b/tests/issue_pipeline/test_stage_status.py
index 2cb50b17b..00dbaa694 100644
--- a/tests/issue_pipeline/test_stage_status.py
+++ b/tests/issue_pipeline/test_stage_status.py
@@ -292,9 +292,14 @@ def invoke(
     approvers=frozenset({222}),
     label: str = LABEL,
     repo: str = REPO,
+    config_repo: str | None = None,
 ):
     monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
-    monkeypatch.setattr(cli_mod, "_load_stage_inputs", lambda path: (label, approvers))
+    monkeypatch.setattr(
+        cli_mod,
+        "_load_stage_inputs",
+        lambda path: (label, approvers, config_repo or repo),
+    )
     return CliRunner().invoke(
         issue_pipeline_group,
         ["stage-status", str(issue), "--repo", repo, "--json", *args],
@@ -643,10 +648,18 @@ class Router:
         return world.run(argv, timeout, cwd=cwd)
 
 
-def test_stage_status_without_repo_is_a_usage_error(monkeypatch) -> None:
-    monkeypatch.setattr(cli_mod, "_make_runner", lambda: World())
-    result = CliRunner().invoke(issue_pipeline_group, ["stage-status", str(ISSUE)])
-    assert result.exit_code == 2 and "--repo" in result.output
+def test_stage_status_without_repo_and_without_a_config_reads_nothing(
+    monkeypatch, tmp_path: Path
+) -> None:
+    world = World()
+    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
+    missing = tmp_path / "absent.json"
+    result = CliRunner().invoke(
+        issue_pipeline_group,
+        ["stage-status", str(ISSUE), "--config", str(missing)],
+    )
+    assert result.exit_code == 2 and result.output == "refused:config_invalid\n"
+    assert world.argvs == []
 
 
 @pytest.mark.parametrize(
@@ -728,3 +741,75 @@ def test_an_approval_on_the_default_repos_issue_never_approves_the_other_repo(
         repo=REPO,
     )
     assert json.loads(again.output)["approved"] is True
+
+
+# --- the repo defaults to the config's (plan Task 16) --------------------------------
+
+
+def _write_config(tmp_path: Path, **extra: object) -> Path:
+    """A real watcher config file, so the verb's own loader reads it."""
+    approvers = tmp_path / "approvers"
+    approvers.write_text("222\n")
+    approvers.chmod(0o600)
+    raw = {
+        "schema_version": 1,
+        "project_id": "PVT_abc",
+        "worktree": str(tmp_path),
+        "approvers_file": str(approvers),
+        "state_dir": str(tmp_path / "state"),
+        **extra,
+    }
+    path = tmp_path / "issue-watch.json"
+    path.write_text(json.dumps(raw))
+    return path
+
+
+def _stage_cli(world, monkeypatch, config: Path, *extra: str):
+    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
+    return CliRunner().invoke(
+        issue_pipeline_group,
+        ["stage-status", str(ISSUE), "--config", str(config), "--json", *extra],
+    )
+
+
+def test_without_repo_the_config_repo_is_read(monkeypatch, tmp_path: Path) -> None:
+    world = World(repo=OTHER)
+    result = _stage_cli(world, monkeypatch, _write_config(tmp_path, repo=OTHER))
+    assert result.exit_code == 0, result.output
+    assert world.argvs  # it read, and the World asserts every argv names Other/Repo
+    assert not any("IronClaude" in " ".join(a) for a in world.argvs)
+
+
+def test_a_hand_written_config_without_a_repo_key_reads_the_fork(
+    monkeypatch, tmp_path: Path
+) -> None:
+    world = World(repo=REPO)
+    result = _stage_cli(world, monkeypatch, _write_config(tmp_path))
+    assert result.exit_code == 0, result.output
+    assert any(f"repos/{REPO}/issues/{ISSUE}" in " ".join(a) for a in world.argvs)
+
+
+def test_a_repo_that_differs_from_the_configs_is_refused_before_any_call(
+    monkeypatch, tmp_path: Path
+) -> None:
+    world = World(repo=OTHER)
+    config = _write_config(tmp_path, repo=OTHER)
+    result = _stage_cli(world, monkeypatch, config, "--repo", REPO)
+    assert result.exit_code == 1 and result.output == "refused:repo-mismatch\n"
+    assert world.argvs == []
+    # a default config (no repo key) against --repo Other/Repo is a mismatch too
+    (tmp_path / "plain").mkdir()
+    plain = _write_config(tmp_path / "plain")
+    result = _stage_cli(world, monkeypatch, plain, "--repo", OTHER)
+    assert result.output == "refused:repo-mismatch\n" and world.argvs == []
+
+
+def test_a_repo_that_matches_the_configs_is_accepted(
+    monkeypatch, tmp_path: Path
+) -> None:
+    # the compare is case-insensitive; the repo the caller typed is the one that is read
+    world = World(repo=OTHER.lower())
+    config = _write_config(tmp_path, repo=OTHER)
+    result = _stage_cli(world, monkeypatch, config, "--repo", OTHER.lower())
+    assert result.exit_code == 0, result.output
+    assert world.argvs
diff --git a/tests/issue_watch/conftest.py b/tests/issue_watch/conftest.py
index 1f11f0de2..2ea53d8c9 100644
--- a/tests/issue_watch/conftest.py
+++ b/tests/issue_watch/conftest.py
@@ -586,7 +586,11 @@ class GhWorld:
         self.skew_s = 0.0
         self.date_text: str | None = None
         self.user_retry_after: str | None = "120"
-        self.origin_url = ORIGIN_URL
+        self.origin_url = (
+            ORIGIN_URL
+            if config.repo == github.REPO
+            else f"https://github.com/{config.repo}.git"
+        )
         self.issues: dict[int, dict] = {}
         self._login = login
         self._fails: dict[tuple[str, int | None], list[_Fail]] = {}
@@ -728,7 +732,7 @@ class GhWorld:
         script, cfg = self.runner.script, self.config
         script[tuple(github.argv_user())] = self._served("user", None, self._user_reply)
         try:
-            discover = github.argv_discover(cfg.trigger_label, self.login)
+            discover = github.argv_discover(cfg.trigger_label, self.login, cfg.repo)
         except ValueError:  # an invalid login never reaches discovery
             pass
         else:
@@ -736,7 +740,7 @@ class GhWorld:
                 "discover", None, self._discovery_reply
             )
         origin = _ArgvRecorder()
-        launch.check_origin(origin, cfg.worktree, 1.0)
+        launch.check_origin(origin, cfg.worktree, 1.0, cfg.repo)
         script[origin.argvs[0]] = self._served("origin", None, self._origin_reply)
         probe = _ArgvRecorder()
         launch.find_orca(probe, which=self.which, timeout=1.0)
@@ -744,24 +748,24 @@ class GhWorld:
             script[argv] = self._served("probe", None, self._probe_reply)
 
     def _register_issue(self, n: int) -> None:
-        script = self.runner.script
+        script, repo = self.runner.script, self.config.repo
         for page in range(1, github.PAGE_CAP + 1):
-            script[tuple(github.argv_events(n, page))] = self._served(
+            script[tuple(github.argv_events(n, page, repo))] = self._served(
                 "events", n, lambda argv, p=page: self._events_reply(argv, n, p)
             )
-            script[tuple(github.argv_comments(n, page))] = self._served(
+            script[tuple(github.argv_comments(n, page, repo))] = self._served(
                 "comments", n, lambda argv, p=page: self._comments_reply(argv, n, p)
             )
-        script[tuple(github.argv_approval_events(n))] = self._served(
+        script[tuple(github.argv_approval_events(n, None, repo))] = self._served(
             "approval_events", n, lambda argv: self._approval_reply(argv, n)
         )
-        script[tuple(github.argv_edits(n))] = self._served(
+        script[tuple(github.argv_edits(n, None, repo))] = self._served(
             "edits", n, lambda argv: self._ok(argv, self._edits_payload(n))
         )
-        script[tuple(github.argv_project_items(n))] = self._served(
+        script[tuple(github.argv_project_items(n, None, repo))] = self._served(
             "items", n, lambda argv: self._ok(argv, self._items_payload(n))
         )
-        script[tuple(github.argv_reread(n))] = self._served(
+        script[tuple(github.argv_reread(n, repo))] = self._served(
             "reread", n, lambda argv: self._ok(argv, self._reread_payload(n))
         )
 
diff --git a/tests/issue_watch/test_cycle.py b/tests/issue_watch/test_cycle.py
index 1a595ee79..dbe874a92 100644
--- a/tests/issue_watch/test_cycle.py
+++ b/tests/issue_watch/test_cycle.py
@@ -5315,3 +5315,87 @@ def test_load_config_refuses_a_network_state_dir_through_the_real_reader__df52_c
     _expect("config_invalid", "network filesystem", cycle.load_config, path)
     source.write_text(ROOT_LINE + "\n", encoding="utf-8")  # a local type passes
     assert cycle.load_config(path).state_dir == tmp_path / "state"
+
+
+# --- the repo key (plan Task 16) ------------------------------------------------------
+
+_OTHER_REPO = "Other-Org/Other.Repo"
+
+
+def test_a_config_for_another_repo_sends_every_gh_call_to_it_and_checks_that_origin(
+    tmp_path, tmp_state, gh_world
+):
+    cfg = make_config(tmp_path, repo=_OTHER_REPO)
+    world = gh_world(config=cfg)  # its script holds only argvs that carry the repo
+    world.issue(9)
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert (res.exit_code, res.launched_issue) == (0, 9)
+    assert len(deps.launcher.calls) == 1
+    gh_calls = world.gh_argvs
+    assert len(gh_calls) > 5
+    for argv in gh_calls:
+        text = "\n".join(argv)
+        assert "IronClaude" not in text and "IronbellyOrg" not in text, argv
+        if argv != _USER_ARGV:
+            owner, name = _OTHER_REPO.split("/")
+            assert _OTHER_REPO in text or (
+                f"owner={owner}" in argv and f"name={name}" in argv
+            ), argv
+    # the origin check read the configured worktree and accepted the other repo's URL
+    assert any(argv[0] == "git" for argv, _ in world.runner.calls)
+
+
+def test_a_worktree_whose_origin_is_the_default_repo_is_a_mismatch_for_another_repo(
+    tmp_path, tmp_state, gh_world
+):
+    cfg = make_config(tmp_path, repo=_OTHER_REPO)
+    world = gh_world(config=cfg)
+    world.origin_url = "https://github.com/IronbellyOrg/IronClaude.git"
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert (res.exit_code, res.reason) == (2, "origin_mismatch")
+    assert deps.launcher.calls == []
+
+
+def test_the_origin_compare_for_a_configured_repo_ignores_case(
+    tmp_path, tmp_state, gh_world
+):
+    cfg = make_config(tmp_path, repo=_OTHER_REPO)
+    world = gh_world(config=cfg)
+    world.issue(9)
+    world.origin_url = f"https://github.com/{_OTHER_REPO.upper()}.git"
+    res, _deps = _run(tmp_path, tmp_state, world)
+    assert res.exit_code == 0 and res.launched_issue == 9
+
+
+def _config_file(tmp_path, **extra):
+    import json as _json
+
+    approvers = tmp_path / "approvers"
+    approvers.write_text("1001\n")
+    approvers.chmod(0o600)
+    raw = {
+        "schema_version": 1,
+        "project_id": "PVT_abc",
+        "worktree": str(tmp_path),
+        "approvers_file": str(approvers),
+        "state_dir": str(tmp_path / "state"),
+        **extra,
+    }
+    path = tmp_path / "cfg.json"
+    path.write_text(_json.dumps(raw))
+    return path
+
+
+def test_a_config_without_a_repo_key_serves_the_fork(tmp_path):
+    cfg = cycle.load_config(_config_file(tmp_path))
+    assert cfg.repo == "IronbellyOrg/IronClaude"
+
+
+def test_a_repo_key_is_read_and_must_be_owner_slash_name(tmp_path):
+    assert (
+        cycle.load_config(_config_file(tmp_path, repo=_OTHER_REPO)).repo == _OTHER_REPO
+    )
+    for bad in ("a/b/c", "", "a b/c", "-a/b", "justone", 5, None, ["a/b"]):
+        with pytest.raises(cycle.ConfigError) as err:
+            cycle.load_config(_config_file(tmp_path, repo=bad))
+        assert err.value.reason == "config_invalid"
diff --git a/tests/issue_watch/test_launch.py b/tests/issue_watch/test_launch.py
index 0cfca605e..59921b8d9 100644
--- a/tests/issue_watch/test_launch.py
+++ b/tests/issue_watch/test_launch.py
@@ -1022,3 +1022,26 @@ def test_launch_and_retry_argv_keep_their_shape_with_the_longer_prompt():
     retry = retry_argv(ORCA, WORKTREE, prompt, "op-1")
     assert len(retry) == 14
     assert retry[-4:] == [prompt, "--retry-launch", "op-1", "--json"]
+
+
+@pytest.mark.parametrize(
+    ("url", "repo", "expected"),
+    [
+        ("https://github.com/Other-Org/Other.Repo.git", "Other-Org/Other.Repo", None),
+        (
+            "https://github.com/IronbellyOrg/IronClaude.git",
+            "Other-Org/Other.Repo",
+            "origin_mismatch",
+        ),
+        ("https://github.com/Other-Org/Other.Repo.git", None, "origin_mismatch"),
+    ],
+)
+def test_check_origin_takes_the_configured_repo_and_defaults_to_the_fork__plan_task_16(
+    fake_runner, tmp_path, url, repo, expected
+):
+    _key, script = _origin_script(tmp_path, result(stdout=url))
+    runner = fake_runner(script)
+    if repo is None:
+        assert check_origin(runner, tmp_path, 10.0) == expected  # the default repo
+    else:
+        assert check_origin(runner, tmp_path, 10.0, repo) == expected
diff --git a/tests/issue_watch/test_origin_parity.py b/tests/issue_watch/test_origin_parity.py
index 3f9faadfd..bb8eee5a7 100644
--- a/tests/issue_watch/test_origin_parity.py
+++ b/tests/issue_watch/test_origin_parity.py
@@ -177,3 +177,34 @@ def test_ac16_check_origin_rejects_what_parse_rejects_or_foreign__fr025(
     """AC-16 FR-025: a host in the wrong case or a foreign repo is a mismatch."""
     runner = fake_runner({GIT_ARGV: _git_reply(url)})
     assert check_origin(runner, WORKTREE, 5) == ORIGIN_MISMATCH
+
+
+@pytest.mark.parametrize(
+    ("url", "repo", "expected"),
+    [
+        ("https://github.com/Other-Org/Other.Repo.git", "Other-Org/Other.Repo", None),
+        ("git@github.com:other-org/other.repo", "Other-Org/Other.Repo", None),
+        (
+            "https://github.com/IronbellyOrg/IronClaude.git",
+            "Other-Org/Other.Repo",
+            ORIGIN_MISMATCH,
+        ),
+        (
+            "https://github.com/Other-Org/Other.Repo.git",
+            "IronbellyOrg/IronClaude",
+            ORIGIN_MISMATCH,
+        ),
+        (
+            "https://github.com/Other-Org/Other.RepoX",
+            "Other-Org/Other.Repo",
+            ORIGIN_MISMATCH,
+        ),
+    ],
+)
+def test_check_origin_compares_with_the_configured_repo_ignoring_case__plan_task_16(
+    fake_runner, url, repo, expected
+):
+    runner = fake_runner({GIT_ARGV: _git_reply(url)})
+    assert check_origin(runner, WORKTREE, 5, repo) == expected
+    # the parsers themselves still keep the case; only the compare lower-cases
+    assert launch.parse_origin(url) is None or launch.parse_origin(url).count("/") == 1

Task 16 context. A config without a repo key serves IronbellyOrg/IronClaude. The cycle passes cfg.repo to every github.* call and to check_origin. The test world in tests/issue_watch/conftest.py now registers argvs with config.repo and an origin URL for that repo, so any call that forgot the repo would be an unscripted argv and fail the test. `stage-status` now takes the repo from --config when --repo is absent; _load_stage_inputs returns a third value (the repo). Task 15 test that said "no --repo is a usage error" was rewritten, because Task 16 makes --repo optional. Tests run: tests/issue_pipeline tests/issue_watch: 3177 passed; ruff clean; make verify-sync clean; no .claude/ path staged.

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
