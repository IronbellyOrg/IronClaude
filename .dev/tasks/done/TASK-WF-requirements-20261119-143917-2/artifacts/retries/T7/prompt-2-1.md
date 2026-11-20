adc880232c23f71b22a83dfb626af4bb6f9a78e8
Review one task for spec compliance.

Task brief: ## Task 7: Build the per-status prompt from the revalidated item

Depends on: Task 1, Task 3, Task 5, Task 6

Implement the prompt rules of Task 6 in `src/superclaude/cli/issue_watch/launch.py` (`build_claim_prompt` at line 84, `PROMPT_PATTERN` at line 33, `launch_argv` at line 95, `retry_argv` at line 119) and in `src/superclaude/cli/issue_watch/cycle.py` (`_examine` at line 915, `_revalidate` at line 979 and `_launch` at line 1026). Today `_launch` builds the prompt at line 1054 and only then calls `_revalidate` (line 1058), which rereads the project items (lines 1012 to 1016) but checks only `project_check` (requirement R27). Change the order so the prompt is built from the item that `_revalidate` rereads. The order inside `_revalidate` is fixed: the approval reread (lines 1007 to 1011, `revalidation_failed`), then the value-time rule of Task 5 (`edited_after_approval`), then `project_check` and the comparison of the examined Status and Pipeline with the reread ones (both `revalidation_failed`). Add a small helper next to `project_check` in `predicates.py` that returns the one live item. `status_report` (`cycle.py` line 1270) builds a retry command with `build_claim_prompt`; it must keep printing a valid command for every allowed Status and Pipeline. Keep `ValueError` for any input that does not match, so no other text reaches `--prompt`.

The seven test files that pin the old prompt move into this task because `launch_argv` rejects any prompt that does not fullmatch `PROMPT_PATTERN` (`launch.py` line 101) and the tree would be red until a later task: `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py` and `test_security_invariants.py` (45 lines hold `--pipeline none`, counted by the remediation debate; recount with Grep before editing). The new `_PROMPT_RE` in `test_security_invariants.py` is written out in the test, not imported from `launch.py`, so the test pins the closed set instead of mirroring it. Its docstring (lines 5 to 6), `_PROMPT_RE` (line 67), the malformed list and the prompt assertions are rewritten.

Acceptance criteria:
- T7.AC1: `tests/issue_watch/test_launch.py` covers the prompt for each allowed Status crossed with each Pipeline value and an empty Pipeline, and rejects an invalid number, an unknown Status, an unknown Pipeline, extra text and `--submit` without `full`.
- T7.AC2: `tests/issue_watch/test_cycle.py` shows the prompt sent for an issue in each allowed Status, and shows two refusals with every value time kept before the approval: Status changed from Research to Debug between examine and launch, and Pipeline lowered from Full Submit to None between examine and launch. Both end with `revalidation_failed` and no launch call. It also shows the overlap case: a Pipeline lowered with a value time after the approval ends `edited_after_approval`.
- T7.AC3: `uv run pytest tests/issue_watch -q` passes with all seven files updated, and `tests/issue_watch/test_no_shell.py` passes (no new text path, no shell).
- T7.AC4: The `once` dry-run output (`would_launch`) keeps its shape, and the `status_report` retry command is valid in a test for each Status.
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
Start sha: adc880232c23f71b22a83dfb626af4bb6f9a78e8
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/cli.py b/src/superclaude/cli/issue_watch/cli.py
index ff8ff7998..fc7d4027a 100644
--- a/src/superclaude/cli/issue_watch/cli.py
+++ b/src/superclaude/cli/issue_watch/cli.py
@@ -158,7 +158,10 @@ def _print_status(report: dict) -> None:
     click.echo(f"retry: {len(report['retry'])}")
     for item in report["retry"]:
         click.echo(f"  issue {item['issue']}: run from {item['cwd']}")
-        click.echo(f"    {shlex.join(item['argv'])}")
+        if item["argv"] is None:
+            click.echo("    (no claim prompt was recorded for this launch)")
+        else:
+            click.echo(f"    {shlex.join(item['argv'])}")
 
 
 @issue_watch_group.command("status")
diff --git a/src/superclaude/cli/issue_watch/cycle.py b/src/superclaude/cli/issue_watch/cycle.py
index b3a1f98f0..354b640ee 100644
--- a/src/superclaude/cli/issue_watch/cycle.py
+++ b/src/superclaude/cli/issue_watch/cycle.py
@@ -526,6 +526,7 @@ class _Cand:
     issue: DiscoveredIssue
     entry: Entry | None
     approval: ApprovalResult | None = None
+    item: predicates.ProjectItem | None = None  # the live Project item examined
     launching: bool = False  # True once the issue passed every GitHub check
 
 
@@ -991,6 +992,7 @@ class _Cycle:
         why = predicates.project_check(items, cfg.project_id)  # type: ignore[arg-type]
         if why is not None:
             raise _Skip(why)
+        c.item = predicates.live_item(items, cfg.project_id)  # type: ignore[arg-type]
         return self._launch(c, approval)
 
     # -- step 12: the launch steps ---------------------------------------------
@@ -1009,8 +1011,12 @@ class _Cycle:
             raise _Transient
         raise _Skip("revalidation_failed")
 
-    def _revalidate(self, c: _Cand) -> None:
-        """FR-011: G7, G3' and G6' with the 3 reserved calls."""
+    def _revalidate(self, c: _Cand) -> predicates.ProjectItem:
+        """FR-011: G7, G3' and G6' with the 3 reserved calls.
+
+        Returns the live Project item the re-read confirmed: the Status and
+        Pipeline must equal the ones examined (``revalidation_failed``).
+        """
         d, cfg = self.deps, self.deps.config
         snap: predicates.IssueSnapshot = self._rv(  # type: ignore[assignment]
             github.reread(d.runner, self.budget, c.n, self._tf)
@@ -1052,6 +1058,14 @@ class _Cycle:
             raise _Skip(why)
         if predicates.project_check(items, cfg.project_id) is not None:  # type: ignore[arg-type]
             raise _Skip("revalidation_failed")
+        item = predicates.live_item(items, cfg.project_id)  # type: ignore[arg-type]
+        assert item is not None  # project_check passed, so exactly one live item
+        if c.item is not None and (item.status_name, item.pipeline_name) != (
+            c.item.status_name,
+            c.item.pipeline_name,
+        ):
+            raise _Skip("revalidation_failed")
+        return item
 
     def _fail(self, c: _Cand, reason: str) -> tuple[str, str]:
         assert self.doc is not None
@@ -1089,13 +1103,17 @@ class _Cycle:
                 raise _Skip("budget_exhausted")
             raise _Stop("orca_not_found", stamp=True)
         try:
-            prompt = launch.build_claim_prompt(c.n)
-        except ValueError:
-            return self._fail(c, "prompt_invalid")
-        try:
-            self._revalidate(c)
+            item = self._revalidate(c)
         except _Transient:
             return self._fail(c, "revalidation_transient")
+        try:
+            # Built from the item the re-read just confirmed, so a Status or
+            # Pipeline moved since examine can never launch the old command (R27).
+            prompt = launch.build_claim_prompt(
+                c.n, item.status_name, item.pipeline_name
+            )
+        except ValueError:
+            return self._fail(c, "prompt_invalid")
         if self._day_cap_reached():
             raise _Skip("day_cap")
         if d.store.disabled():
@@ -1134,6 +1152,7 @@ class _Cycle:
             self._set(before_pending)
             self._save()
             raise _Skip("budget_exhausted")
+        _remember_prompt(cfg.state_dir, c.n, prompt)
         outcome = d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)
         now = self.now()
         if outcome.kind == "launched":
@@ -1305,15 +1324,56 @@ def _retry_orca(which: Callable[[str], str | None]) -> str:
     return launch._ORCA_CLIS[0]
 
 
+PROMPTS_FILE = "launch-prompts.json"
+"""The claim prompt of each launch, so ``status`` can print a retry command.
+
+The dispatch store is a closed schema and keeps neither the Status nor the
+Pipeline that chose the prompt (R23), so the prompt is kept beside it.
+"""
+
+
+def _read_prompts(state_dir: Path) -> dict[str, str]:
+    """The kept prompts; an unreadable or malformed file reads as none."""
+    try:
+        data = json.loads((state_dir / PROMPTS_FILE).read_text(encoding="utf-8"))
+    except (OSError, ValueError):
+        return {}
+    if not isinstance(data, dict):
+        return {}
+    return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, str)}
+
+
+def _remember_prompt(state_dir: Path, n: int, prompt: str) -> None:
+    """Keep ``prompt`` for issue ``n`` (mode 0600, atomic). Best effort: a failure
+    only means ``status`` prints no retry command for this launch."""
+    try:
+        data = _read_prompts(state_dir)
+        data[str(n)] = prompt
+        tmp = state_dir / (PROMPTS_FILE + ".tmp")
+        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
+        with os.fdopen(fd, "w", encoding="utf-8") as handle:
+            json.dump(data, handle, sort_keys=True)
+        os.replace(tmp, state_dir / PROMPTS_FILE)
+    except OSError:
+        pass
+
+
 def status_report(
     store: Store,
     audit: audit.AuditLog | None,
     now: datetime,
     *,
     which: Callable[[str], str | None] = shutil.which,
+    prompts: dict[int, str] | None = None,
 ) -> dict:
     """Return the ``status --json`` fields of design 10.2.
 
+    The retry argv carries the claim prompt the launch sent: ``prompts`` (issue
+    number to prompt) when the caller gives one, else the one kept in
+    ``launch-prompts.json`` beside the store. For an ``unknown`` entry with no
+    kept prompt, or one that is not a prompt the watcher could have built,
+    ``argv`` is ``None`` rather than a guessed command.
+
     Reads ``dispatch.json`` and the ``DISABLED`` mtime and nothing else: no
     lock, no write, no probe, no ``gh``. ``audit`` is accepted for the fixed
     signature and not read. Only typed scalars are returned, never issue text.
@@ -1330,6 +1390,7 @@ def status_report(
     since = store.disabled_since()
     next_at = doc.next_permitted_at
     orca = _retry_orca(which)
+    kept = _read_prompts(getattr(store, "state_dir", Path("/nonexistent")))
     stale: list[dict] = []
     retry: list[dict] = []
     for n in sorted(doc.entries):
@@ -1344,15 +1405,15 @@ def status_report(
                 }
             )
         if entry.state == "unknown" and entry.operation_id and entry.launch_cwd:
-            try:
-                argv = launch.retry_argv(
-                    orca,
-                    entry.launch_cwd,
-                    launch.build_claim_prompt(n),
-                    entry.operation_id,
-                )
-            except ValueError:  # an id that cannot be printed as a command
-                continue
+            argv = None
+            prompt = (prompts or {}).get(n) or kept.get(str(n))
+            if prompt is not None and launch.PROMPT_PATTERN.fullmatch(prompt):
+                try:
+                    argv = launch.retry_argv(
+                        orca, entry.launch_cwd, prompt, entry.operation_id
+                    )
+                except ValueError:  # an id or a prompt that cannot be printed
+                    continue
             retry.append(
                 {
                     "issue": n,
diff --git a/src/superclaude/cli/issue_watch/launch.py b/src/superclaude/cli/issue_watch/launch.py
index 1c5cf889b..d3471a7b5 100644
--- a/src/superclaude/cli/issue_watch/launch.py
+++ b/src/superclaude/cli/issue_watch/launch.py
@@ -30,9 +30,30 @@ ORCA_AGENT = "claude"
 MAX_ISSUE_NUMBER = 999_999_999
 """Largest issue number ``build_claim_prompt`` accepts (FR-012)."""
 
-PROMPT_PATTERN = re.compile(r"^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$")
+PROMPT_PATTERN = re.compile(
+    r"^/sc:issue --claim [1-9][0-9]{0,8}"
+    r" --pipeline (?:none|worktree|full(?: --submit)?)"
+    r" --stage (?:research|spec|plan|debug)$"
+)
 """Every prompt ``build_claim_prompt`` can return, and nothing else."""
 
+STAGE_OF_STATUS = {
+    "Research": "research",
+    "Spec": "spec",
+    "Plan": "plan",
+    "Debug": "debug",
+}
+"""The stage word the claim runs for each allowed Project Status (R23)."""
+
+PIPELINE_ARGS = {
+    None: "none",
+    "None": "none",
+    "Worktree": "worktree",
+    "Full": "full",
+    "Full Submit": "full --submit",
+}
+"""The ``--pipeline`` text for each Pipeline value; an empty Pipeline is ``none``."""
+
 OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
 """Operation ids that may be stored and printed in a retry command (design 9.2)."""
 
@@ -81,15 +102,28 @@ def _check_timeout(timeout: object) -> float:
     return float(timeout)
 
 
-def build_claim_prompt(n: object) -> str:
-    """Return ``/sc:issue --claim <n> --pipeline none`` for an ``int`` in 1..999999999.
+def build_claim_prompt(n: object, status: object, pipeline: object) -> str:
+    """Return the claim prompt for issue ``n``, its Project ``status`` and ``pipeline``.
 
-    A ``bool``, a ``str``, a ``float`` or an out-of-range ``int`` raises
-    ``ValueError`` (FR-012, design 9.3).
+    For example ``/sc:issue --claim 9 --pipeline full --submit --stage plan``.
+    ``n`` is an ``int`` in 1..999999999; ``status`` is one of ``Research``,
+    ``Spec``, ``Plan``, ``Debug``; ``pipeline`` is ``None`` (no value), ``None``
+    as text, ``Worktree``, ``Full`` or ``Full Submit``. Anything else, a ``bool``
+    or a ``str`` issue number included, raises ``ValueError`` (FR-012, design 9.3,
+    ``docs/designs/issue-watcher-status-pipelines.md`` section 3).
     """
     if type(n) is not int or not 1 <= n <= MAX_ISSUE_NUMBER:
         raise ValueError("issue number must be an int in 1..999999999")
-    return f"/sc:issue --claim {n} --pipeline none"
+    if not isinstance(status, str) or status not in STAGE_OF_STATUS:
+        raise ValueError("status must be Research, Spec, Plan or Debug")
+    if pipeline is not None and (
+        not isinstance(pipeline, str) or pipeline not in PIPELINE_ARGS
+    ):
+        raise ValueError("pipeline must be empty, None, Worktree, Full or Full Submit")
+    return (
+        f"/sc:issue --claim {n} --pipeline {PIPELINE_ARGS[pipeline]}"
+        f" --stage {STAGE_OF_STATUS[status]}"
+    )
 
 
 def launch_argv(orca: str, worktree: Path | str, prompt: str) -> list[str]:
diff --git a/src/superclaude/cli/issue_watch/predicates.py b/src/superclaude/cli/issue_watch/predicates.py
index b2c9329bb..d235c476f 100644
--- a/src/superclaude/cli/issue_watch/predicates.py
+++ b/src/superclaude/cli/issue_watch/predicates.py
@@ -337,12 +337,18 @@ def project_check(items: Iterable[ProjectItem], project_id: str) -> str | None:
     ``ALLOWED_STATUSES`` (R22). Any other value, a new board status included,
     is a mismatch until it is added there.
     """
-    matching = [i for i in items if not i.is_archived and i.project_id == project_id]
-    if len(matching) == 1 and matching[0].status_name in ALLOWED_STATUSES:
+    item = live_item(items, project_id)
+    if item is not None and item.status_name in ALLOWED_STATUSES:
         return None
     return "project_mismatch"
 
 
+def live_item(items: Iterable[ProjectItem], project_id: str) -> ProjectItem | None:
+    """The one non-archived item of ``project_id``, or None for zero or several."""
+    matching = [i for i in items if not i.is_archived and i.project_id == project_id]
+    return matching[0] if len(matching) == 1 else None
+
+
 def marker_time(marker: MarkerEvidence) -> datetime:
     """Return the later of the marker comment's creation and update (DF-16)."""
     return max(marker.created_at, marker.updated_at)
diff --git a/tests/issue_watch/test_cli.py b/tests/issue_watch/test_cli.py
index bda4c01e7..a47e12dfc 100644
--- a/tests/issue_watch/test_cli.py
+++ b/tests/issue_watch/test_cli.py
@@ -210,9 +210,17 @@ def seed_store(
     last_completed: datetime | None = None,
     next_permitted: datetime | None = None,
     entries: tuple[Entry, ...] = (),
+    prompts: dict[int, str] | None = None,
 ) -> record.FileStore:
-    """Create the state directory and store, then replace the interesting fields."""
+    """Create the state directory and store, then replace the interesting fields.
+
+    ``prompts`` is written as the kept claim prompts that ``status`` retries use.
+    """
     store = record.init_state(config.state_dir, NOW - timedelta(days=3))
+    if prompts is not None:
+        (config.state_dir / cycle.PROMPTS_FILE).write_text(
+            json.dumps({str(n): p for n, p in prompts.items()}), encoding="utf-8"
+        )
     store.save(
         replace(
             store.load(),
@@ -237,7 +245,7 @@ def retry_argv(orca: str, n: int, cwd: str, op: str) -> list[str]:
         "--surface",
         "terminal",
         "--prompt",
-        f"/sc:issue --claim {n} --pipeline none",
+        f"/sc:issue --claim {n} --pipeline none --stage research",
         "--retry-launch",
         op,
         "--json",
@@ -602,12 +610,17 @@ def test_build_deps_wires_the_real_dependencies_from_the_config(config, monkeypa
     # the worktree as the working directory (the one call that passes cwd).
     assert isinstance(deps.launcher, launch.OrcaLauncher)
     deps.launcher.launch(
-        "orca-x", config.worktree, "/sc:issue --claim 9 --pipeline none", 30.0
+        "orca-x",
+        config.worktree,
+        "/sc:issue --claim 9 --pipeline none --stage research",
+        30.0,
     )
     assert seen == [
         (
             launch.launch_argv(
-                "orca-x", config.worktree, "/sc:issue --claim 9 --pipeline none"
+                "orca-x",
+                config.worktree,
+                "/sc:issue --claim 9 --pipeline none --stage research",
             ),
             30.0,
             str(config.worktree),
@@ -741,6 +754,10 @@ def seed_rich_store(config: cycle.Config) -> None:
         config,
         last_completed=NOW - timedelta(seconds=120),
         next_permitted=NOW + timedelta(minutes=10),
+        prompts={
+            5: "/sc:issue --claim 5 --pipeline none --stage research",
+            8: "/sc:issue --claim 8 --pipeline none --stage research",
+        },
         entries=(
             entry(
                 5,
@@ -886,6 +903,49 @@ def _launched_like(n: int, state: str, reason: str, **over: object) -> Entry:
     )
 
 
+@pytest.mark.parametrize("status", ["Research", "Spec", "Plan", "Debug"])
+@pytest.mark.parametrize("pipeline", [None, "Worktree", "Full", "Full Submit"])
+def test_status_retry_command_is_valid_for_each_status_and_pipeline__r23(
+    config, status, pipeline
+):
+    """A retry command carries the kept prompt, whatever Status and Pipeline chose it."""
+    prompt = launch.build_claim_prompt(9, status, pipeline)
+    seed_store(
+        config,
+        last_completed=NOW - timedelta(seconds=60),
+        prompts={9: prompt},
+        entries=(_launched_like(9, "unknown", "launch_unknown"),),
+    )
+    report = cycle.status_report(record.FileStore(config.state_dir), None, NOW)
+    (item,) = report["retry"]
+    assert item["argv"][item["argv"].index("--prompt") + 1] == prompt
+    assert item["argv"][-3:] == ["--retry-launch", "op-9", "--json"]
+
+
+@pytest.mark.parametrize(
+    "kept",
+    [
+        pytest.param(None, id="no-file"),
+        pytest.param(
+            {8: "/sc:issue --claim 8 --pipeline none --stage research"},
+            id="other-issue",
+        ),
+        pytest.param({9: "/sc:issue --claim 9; rm -rf /"}, id="not-a-claim-prompt"),
+    ],
+)
+def test_status_retry_has_no_command_when_no_valid_prompt_is_kept__r23(config, kept):
+    """No prompt is guessed: a missing or foreign kept prompt gives ``argv`` None."""
+    seed_store(
+        config,
+        last_completed=NOW - timedelta(seconds=60),
+        prompts=kept,
+        entries=(_launched_like(9, "unknown", "launch_unknown"),),
+    )
+    report = cycle.status_report(record.FileStore(config.state_dir), None, NOW)
+    (item,) = report["retry"]
+    assert item["argv"] is None
+
+
 def test_status_retry_lists_only_unknown_entries_with_an_id_and_a_cwd__ac9_fr015(
     tmp_path, config, config_file, fixed_clock, monkeypatch
 ):
@@ -893,6 +953,7 @@ def test_status_retry_lists_only_unknown_entries_with_an_id_and_a_cwd__ac9_fr015
     seed_store(
         config,
         last_completed=NOW - timedelta(seconds=60),
+        prompts={8: "/sc:issue --claim 8 --pipeline none --stage research"},
         entries=(
             _launched_like(5, "launched", "launched"),
             _launched_like(6, "claimed", "claimed"),
@@ -1008,6 +1069,7 @@ def _retry_argv0(tmp_path, config, config_file) -> tuple[int, list[str]]:
     seed_store(
         config,
         last_completed=NOW - timedelta(seconds=60),
+        prompts={9: "/sc:issue --claim 9 --pipeline none --stage research"},
         entries=(
             entry(
                 9,
diff --git a/tests/issue_watch/test_cli_e2e.py b/tests/issue_watch/test_cli_e2e.py
index 9aa5cf226..c27941064 100644
--- a/tests/issue_watch/test_cli_e2e.py
+++ b/tests/issue_watch/test_cli_e2e.py
@@ -252,7 +252,7 @@ def launch_argv_literal(orca: str, worktree: Path) -> list[str]:
         "--surface",
         "terminal",
         "--prompt",
-        "/sc:issue --claim 9 --pipeline none",
+        "/sc:issue --claim 9 --pipeline none --stage research",
         "--json",
     ]
 
@@ -365,7 +365,7 @@ def test_fr010_fr013_eligible_issue_launches_once_through_orca_ide(tmp_path, stu
     )
     assert len([orca_ide, *launch_call["argv"]]) == 12
     assert launch_call["argv"][launch_call["argv"].index("--prompt") + 1] == (
-        "/sc:issue --claim 9 --pipeline none"
+        "/sc:issue --claim 9 --pipeline none --stage research"
     )
     assert Path(launch_call["cwd"]).resolve() == watcher.config.worktree.resolve()
     # orca-ide is resolved first, so the plain orca stub is never called
diff --git a/tests/issue_watch/test_crash_injection.py b/tests/issue_watch/test_crash_injection.py
index fe8eeb61d..cf83bb4d1 100644
--- a/tests/issue_watch/test_crash_injection.py
+++ b/tests/issue_watch/test_crash_injection.py
@@ -35,7 +35,7 @@ from .conftest import (
 ISSUE = 9
 RERUNS = 5
 GAP_S = 300  # the clock moves 5 minutes before each run, as a timer would
-PROMPT = f"/sc:issue --claim {ISSUE} --pipeline none"
+PROMPT = f"/sc:issue --claim {ISSUE} --pipeline none --stage research"
 USER_ARGV = tuple(github.argv_user())
 
 
@@ -361,7 +361,8 @@ def test_c5_crash_after_the_outcome_save_loses_only_the_audit_lines__nfr005(
     doc = rig.doc()
     assert ISSUE in doc.considered
     assert doc.last_completed_cycle_at == CYCLE_NOW
-    assert rig.file_names() == rig.names_before
+    # The launch kept its claim prompt beside the store (R23); nothing else is new.
+    assert rig.file_names() == sorted([*rig.names_before, "launch-prompts.json"])
     assert [call[2] for call in rig.crash_launcher.calls] == [PROMPT]
     # No decision line for this launch (no line of the cycle was written).
     rig.assert_untouched_audit()
diff --git a/tests/issue_watch/test_cycle.py b/tests/issue_watch/test_cycle.py
index 2fb6f43d9..560991d41 100644
--- a/tests/issue_watch/test_cycle.py
+++ b/tests/issue_watch/test_cycle.py
@@ -12,6 +12,7 @@ from __future__ import annotations
 import itertools
 import json
 import os
+import re
 import sys
 import threading
 from dataclasses import replace
@@ -2385,7 +2386,7 @@ _LAUNCH_TRACE = [
     "items:9",
     "origin",
 ]
-_CLAIM_9 = "/sc:issue --claim 9 --pipeline none"
+_CLAIM_9 = "/sc:issue --claim 9 --pipeline none --stage research"
 _T_MARK = T_APPROVED + timedelta(minutes=1)  # a claim marker after the approval
 _SHADOW_AT = "2026-11-07T13:00:00Z"  # CYCLE_NOW, as dry-run.json writes it
 
@@ -2831,7 +2832,80 @@ def test_an_empty_pipeline_with_a_status_before_the_approval_launches_none__r34(
     )
     res, deps = _run(tmp_path, tmp_state, world)
     assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
-    assert [c[2] for c in deps.launcher.calls] == [_CLAIM_9]
+    assert [c[2] for c in deps.launcher.calls] == [
+        "/sc:issue --claim 9 --pipeline none --stage plan"
+    ]
+
+
+@pytest.mark.parametrize("status", ["Research", "Spec", "Plan", "Debug"])
+def test_the_prompt_sent_names_the_stage_of_the_issues_status__r23(
+    tmp_path, tmp_state, gh_world, status
+):
+    world = gh_world()
+    world.issue(9, items=[{"status": status}])
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
+    assert [c[2] for c in deps.launcher.calls] == [
+        f"/sc:issue --claim 9 --pipeline none --stage {status.lower()}"
+    ]
+
+
+def test_a_launch_keeps_its_prompt_for_the_status_retry_command__r23(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    world.issue(9, items=[{"status": "Debug"}])
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
+    kept = json.loads((tmp_state.state_dir / cycle.PROMPTS_FILE).read_text("utf-8"))
+    assert kept == {"9": "/sc:issue --claim 9 --pipeline none --stage debug"}
+    assert (tmp_state.state_dir / cycle.PROMPTS_FILE).stat().st_mode & 0o777 == 0o600
+
+
+@pytest.mark.parametrize(
+    ("examined", "reread"),
+    [
+        pytest.param(
+            [{"status": "Research"}], [{"status": "Debug"}], id="status-moved"
+        ),
+        pytest.param(
+            [{"pipeline": "Full Submit"}],
+            [{"pipeline": None}],
+            id="pipeline-lowered-to-none",
+        ),
+        pytest.param(
+            [{"pipeline": "Full Submit"}],
+            [{"pipeline": "Worktree"}],
+            id="pipeline-lowered-to-worktree",
+        ),
+    ],
+)
+def test_a_status_or_pipeline_moved_between_examine_and_launch_fails__r27(
+    tmp_path, tmp_state, gh_world, examined, reread
+):
+    """Every value time stays before the approval, so only the comparison refuses."""
+    world = gh_world()
+    world.issue(9, items=examined)
+    _on_nth(world, "items", 9, 2, lambda: world.update(9, items=reread))
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "revalidation_failed")]
+    assert deps.launcher.calls == []
+    assert tmp_state.load().entries == {}
+
+
+def test_a_pipeline_lowered_with_a_time_after_the_approval_is_edited__r27_r31(
+    tmp_path, tmp_state, gh_world
+):
+    """The overlap case: the value-time rule wins over the comparison."""
+    world = gh_world()
+    world.issue(9, items=[{"pipeline": "Full Submit"}])
+    lowered = [
+        {"pipeline": "Worktree", "pipeline_at": T_APPROVED + timedelta(minutes=1)}
+    ]
+    _on_nth(world, "items", 9, 2, lambda: world.update(9, items=lowered))
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "edited_after_approval")]
+    assert deps.launcher.calls == []
 
 
 def test_a_real_label_named_issue_watch_approved_never_approves__r35(
@@ -3519,7 +3593,7 @@ def test_no_orca_cli_on_the_path_is_exit_2_without_a_probe_call__fr013(
 def test_a_prompt_value_error_writes_failed_prompt_invalid__fr012_fr014(
     tmp_path, tmp_state, gh_world, monkeypatch
 ):
-    def refuse(n):
+    def refuse(n, status, pipeline):
         raise ValueError("no prompt")
 
     monkeypatch.setattr(cycle.launch, "build_claim_prompt", refuse)
@@ -3528,7 +3602,7 @@ def test_a_prompt_value_error_writes_failed_prompt_invalid__fr012_fr014(
     res, deps = _run(tmp_path, tmp_state, world)
     assert (res.exit_code, res.reason) == (7, "prompt_invalid")
     assert deps.launcher.calls == []
-    assert _trace(world)[-1] == "probe"  # the prompt build precedes the re-read
+    assert _trace(world)[-1] == "items:9"  # the prompt is built after the re-read (R27)
     entry = _entry(tmp_state, 9)
     assert (entry.state, entry.attempts, entry.launches) == ("failed", 1, 0)
     assert (entry.consumed_at, entry.pending_at) == (None, None)
@@ -3938,7 +4012,9 @@ def test_s1_case_b_fifteen_eligible_issues_examine_and_launch_exactly_one__fr016
     lines1 = _lines_of(tmp_state, res1)
     assert (res1.exit_code, res1.launched_issue) == (0, 1)
     assert _decisions(lines1) == [(1, "launched")]
-    assert [c[2] for c in launcher.calls] == ["/sc:issue --claim 1 --pipeline none"]
+    assert [c[2] for c in launcher.calls] == [
+        "/sc:issue --claim 1 --pipeline none --stage research"
+    ]
     assert _touched(world) == {1}  # later candidates are neither read ...
     stored = tmp_state.load()
     assert dict(stored.considered) == {1: CYCLE_NOW}  # ... nor stamped
@@ -3949,8 +4025,8 @@ def test_s1_case_b_fifteen_eligible_issues_examine_and_launch_exactly_one__fr016
     res2, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
     assert _decisions(_lines_of(tmp_state, res2)) == [(2, "launched")]
     assert [c[2] for c in launcher.calls] == [
-        "/sc:issue --claim 1 --pipeline none",
-        "/sc:issue --claim 2 --pipeline none",
+        "/sc:issue --claim 1 --pipeline none --stage research",
+        "/sc:issue --claim 2 --pipeline none --stage research",
     ]
     assert sorted(tmp_state.load().entries) == [1, 2]
     assert dict(tmp_state.load().considered) == {
@@ -4413,12 +4489,11 @@ def _prompt_numbers(launcher) -> list[int]:
     """The issue numbers the launcher was asked for, after checking each prompt."""
     numbers = []
     for _orca, _worktree, prompt, _timeout in launcher.calls:
-        head, _, tail = prompt.rpartition(" ")
-        assert tail == "none" and head.endswith(" --pipeline")
-        prefix, _, digits = head[: -len(" --pipeline")].rpartition(" ")
-        assert prefix == "/sc:issue --claim"
-        assert digits.isdigit() and digits == str(int(digits))
-        numbers.append(int(digits))
+        found = re.fullmatch(
+            r"/sc:issue --claim ([1-9][0-9]*) --pipeline none --stage research", prompt
+        )
+        assert found, prompt
+        numbers.append(int(found.group(1)))
     return numbers
 
 
@@ -4531,7 +4606,7 @@ def test_acceptance_property(tmp_path, tmp_state, gh_world, count):
         if made:
             assert (
                 launcher.calls[-1][2]
-                == f"/sc:issue --claim {res.launched_issue} --pipeline none"
+                == f"/sc:issue --claim {res.launched_issue} --pipeline none --stage research"
             )
         world.clock.advance(_HALF_HOUR)
         return res, lines
@@ -4653,7 +4728,7 @@ def test_the_three_reserved_calls_remain_for_the_re_read__nfr009(
     assert _the_cycle_line(lines)["gh_calls"] == 2 + 34
     assert _reads(world, 7) == [] and _reads(world, 8) == []
     assert [c[2] for c in deps.launcher.calls] == [
-        "/sc:issue --claim 6 --pipeline none"
+        "/sc:issue --claim 6 --pipeline none --stage research"
     ]
     assert _entry(tmp_state, 6).state == "launched"
 
@@ -5041,7 +5116,7 @@ def test_a_dry_run_migrates_in_memory_and_never_writes_the_store__df17_fr019_c9(
 
 
 def _refuse_prompt(monkeypatch):
-    def refuse(n):
+    def refuse(n, status, pipeline):
         raise ValueError("no prompt")
 
     monkeypatch.setattr(cycle.launch, "build_claim_prompt", refuse)
diff --git a/tests/issue_watch/test_launch.py b/tests/issue_watch/test_launch.py
index 245a072f5..0cfca605e 100644
--- a/tests/issue_watch/test_launch.py
+++ b/tests/issue_watch/test_launch.py
@@ -33,40 +33,106 @@ from .conftest import result
 
 ORCA = "/opt/orca/bin/orca-ide"
 WORKTREE = "/work/tree"
-PROMPT = "/sc:issue --claim 9 --pipeline none"
+PROMPT = "/sc:issue --claim 9 --pipeline none --stage research"
 
 # --- prompt (FR-012, design 9.3) ----------------------------------------------
 
 
 def test_ac7_prompt_accepts_only_the_int_nine__fr012_nfr001():
     """AC-7 FR-012 NFR-001: of the spec's seven inputs only ``9`` returns a prompt."""
-    assert build_claim_prompt(9) == "/sc:issue --claim 9 --pipeline none"
+    assert (
+        build_claim_prompt(9, "Research", None)
+        == "/sc:issue --claim 9 --pipeline none --stage research"
+    )
 
 
 @pytest.mark.parametrize("value", ["9", True, 0, -1, 10**9, 9.0])
 def test_ac7_prompt_rejects_every_other_input__fr012_nfr001(value):
     """AC-7 FR-012 NFR-001: a str, bool, zero, negative, too large or float raises."""
     with pytest.raises(ValueError):
-        build_claim_prompt(value)
+        build_claim_prompt(value, "Research", None)
 
 
 @pytest.mark.parametrize("value", [None, "", "9; rm -rf /", [9], b"9", 9.5, False])
 def test_ac7_prompt_rejects_hostile_non_ints__fr012_nfr001(value):
     """AC-7 FR-012 NFR-001: other types and hostile text raise, nothing is built."""
     with pytest.raises(ValueError):
-        build_claim_prompt(value)
+        build_claim_prompt(value, "Research", None)
+
+
+_LEVEL_TEXT = {
+    None: "none",
+    "None": "none",
+    "Worktree": "worktree",
+    "Full": "full",
+    "Full Submit": "full --submit",
+}
+
+
+@pytest.mark.parametrize("status", ["Research", "Spec", "Plan", "Debug"])
+@pytest.mark.parametrize("pipeline", [None, "None", "Worktree", "Full", "Full Submit"])
+def test_r23_prompt_for_each_status_crossed_with_each_pipeline_value(status, pipeline):
+    """R23: the prompt names the level and the stage, and the pattern pins it."""
+    prompt = build_claim_prompt(12, status, pipeline)
+    assert prompt == (
+        f"/sc:issue --claim 12 --pipeline {_LEVEL_TEXT[pipeline]} "
+        f"--stage {status.lower()}"
+    )
+    assert launch.PROMPT_PATTERN.fullmatch(prompt) is not None
+    assert launch_argv(ORCA, WORKTREE, prompt)[9:] == ["--prompt", prompt, "--json"]
+
+
+@pytest.mark.parametrize(
+    ("status", "pipeline"),
+    [
+        ("Backlog", None),
+        ("Ready", None),
+        ("In review", "Full"),
+        (None, None),
+        ("research", None),
+        ("Research", "Triage"),
+        ("Research", "full"),
+        ("Research", "Full Submit; rm -rf /"),
+        ("Research", 3),
+        (5, None),
+    ],
+)
+def test_r23_prompt_rejects_an_unknown_status_or_pipeline(status, pipeline):
+    with pytest.raises(ValueError):
+        build_claim_prompt(9, status, pipeline)
+
+
+@pytest.mark.parametrize(
+    "prompt",
+    [
+        "/sc:issue --claim 9 --pipeline none --stage research --submit",
+        "/sc:issue --claim 9 --pipeline worktree --submit --stage research",
+        "/sc:issue --claim 9 --pipeline none --submit --stage research",
+        "/sc:issue --claim 9 --pipeline full --submit --submit --stage plan",
+        "/sc:issue --claim 9 --pipeline full --stage ready",
+        "/sc:issue --claim 9 --pipeline full",
+        "/sc:issue --claim 9 --pipeline Full --stage plan",
+        "/sc:issue --claim 9 --pipeline full --stage plan extra",
+        "/sc:issue --claim 9 --pipeline full --stage plan\n",
+        "/sc:issue --claim 09 --pipeline full --stage plan",
+    ],
+)
+def test_r23_the_pattern_refuses_extra_text_and_a_submit_without_full(prompt):
+    assert launch.PROMPT_PATTERN.fullmatch(prompt) is None
+    with pytest.raises(ValueError):
+        launch_argv(ORCA, WORKTREE, prompt)
 
 
 @pytest.mark.parametrize(
     ("value", "expected"),
     [
-        (1, "/sc:issue --claim 1 --pipeline none"),
-        (999999999, "/sc:issue --claim 999999999 --pipeline none"),
+        (1, "/sc:issue --claim 1 --pipeline none --stage research"),
+        (999999999, "/sc:issue --claim 999999999 --pipeline none --stage research"),
     ],
 )
 def test_ac7_prompt_accepts_both_range_ends__fr012(value, expected):
     """AC-7 FR-012: 1 and 999999999 are the first and last accepted numbers."""
-    assert build_claim_prompt(value) == expected
+    assert build_claim_prompt(value, "Research", None) == expected
 
 
 # --- launch argv (FR-013, threat T10) ------------------------------------------
@@ -86,7 +152,7 @@ def test_ac8_launch_argv_equals_the_literal_twelve_elements__fr013():
         "--surface",
         "terminal",
         "--prompt",
-        "/sc:issue --claim 9 --pipeline none",
+        "/sc:issue --claim 9 --pipeline none --stage research",
         "--json",
     ]
     assert len(argv) == 12
@@ -122,9 +188,9 @@ def test_ac8_orca_agent_constant_is_claude__fr013():
         "/sc:issue --claim 9 --pipeline worktree",
         "/sc:issue --claim 9 --pipeline none --pipeline full",
         "/sc:issue --claim 9 --pipeline none ",
-        "/sc:issue --claim 0 --pipeline none",
-        "/sc:issue --claim 09 --pipeline none",
-        "/sc:issue --claim 1000000000 --pipeline none",
+        "/sc:issue --claim 0 --pipeline none --stage research",
+        "/sc:issue --claim 09 --pipeline none --stage research",
+        "/sc:issue --claim 1000000000 --pipeline none --stage research",
         "/sc:issue --claim 0",
         "/sc:issue --claim 09",
         "/sc:issue --claim 1000000000",
@@ -171,7 +237,7 @@ def test_ac9_retry_argv_puts_retry_launch_right_before_json__fr015():
         "--surface",
         "terminal",
         "--prompt",
-        "/sc:issue --claim 9 --pipeline none",
+        "/sc:issue --claim 9 --pipeline none --stage research",
         "--retry-launch",
         "op-1",
         "--json",
@@ -930,13 +996,19 @@ def test_ac8_orca_agent_is_pinned_to_the_literal_claude__fr013_df11():
 
 
 def test_build_claim_prompt_returns_exactly_the_pipeline_none_form():
-    assert build_claim_prompt(9) == "/sc:issue --claim 9 --pipeline none"
+    assert (
+        build_claim_prompt(9, "Research", None)
+        == "/sc:issue --claim 9 --pipeline none --stage research"
+    )
 
 
 def test_the_old_claim_prompt_no_longer_matches_and_launch_argv_refuses_it():
     old = "/sc:issue --claim 9"
     assert launch.PROMPT_PATTERN.fullmatch(old) is None
-    assert launch.PROMPT_PATTERN.fullmatch(build_claim_prompt(9)) is not None
+    assert launch.PROMPT_PATTERN.fullmatch(build_claim_prompt(9, "Plan", None))
+    assert (
+        launch.PROMPT_PATTERN.fullmatch("/sc:issue --claim 9 --pipeline none") is None
+    )
     with pytest.raises(ValueError):
         launch_argv(ORCA, WORKTREE, old)
     with pytest.raises(ValueError):
@@ -944,7 +1016,7 @@ def test_the_old_claim_prompt_no_longer_matches_and_launch_argv_refuses_it():
 
 
 def test_launch_and_retry_argv_keep_their_shape_with_the_longer_prompt():
-    prompt = build_claim_prompt(9)
+    prompt = build_claim_prompt(9, "Debug", "Full Submit")
     argv = launch_argv(ORCA, WORKTREE, prompt)
     assert len(argv) == 12 and argv[9:] == ["--prompt", prompt, "--json"]
     retry = retry_argv(ORCA, WORKTREE, prompt, "op-1")
diff --git a/tests/issue_watch/test_no_text.py b/tests/issue_watch/test_no_text.py
index 93ce48e22..d9ed0382e 100644
--- a/tests/issue_watch/test_no_text.py
+++ b/tests/issue_watch/test_no_text.py
@@ -63,7 +63,10 @@ _REAL_BUILD_DEPS = cli.build_deps
 SENT = "PWNED-TITLE"
 STEM = "PWNED"  # a shorter needle also catches a truncated or re-cased copy
 HOSTILE_PAD = "x" * 600
-PROMPT_SHAPE = re.compile(r"^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$")
+PROMPT_SHAPE = re.compile(
+    r"^/sc:issue --claim [1-9][0-9]{0,8} --pipeline (?:none|worktree|full(?: --submit)?)"
+    r" --stage (?:research|spec|plan|debug)$"
+)
 LOCAL_MOUNTINFO = "1 0 0:1 / / rw - ext4 /dev/sda1 rw\n"
 FILLER = "#"  # first character of the padding line the rotation test writes
 
@@ -463,7 +466,9 @@ def _build_scenarios() -> list[Scenario]:
 
 def _orca_reply(world: GhWorld, reply: CommandResult) -> None:
     argv = launch.launch_argv(
-        ORCA_PATH, world.config.worktree, "/sc:issue --claim 7 --pipeline none"
+        ORCA_PATH,
+        world.config.worktree,
+        "/sc:issue --claim 7 --pipeline none --stage research",
     )
     world.runner.script[tuple(argv)] = reply
 
@@ -557,9 +562,11 @@ def test_a_launching_cycle_records_the_prompt_and_stays_clean(
     out = run.once()
     run.status()
     assert out.exit_code == 0 and "cycle: cycle_complete" in out.output
-    assert [c[2] for c in run.launcher.calls] == ["/sc:issue --claim 7 --pipeline none"]
+    assert [c[2] for c in run.launcher.calls] == [
+        "/sc:issue --claim 7 --pipeline none --stage research"
+    ]
     assert run.launcher.argvs[0][run.launcher.argvs[0].index("--prompt") + 1] == (
-        "/sc:issue --claim 7 --pipeline none"
+        "/sc:issue --claim 7 --pipeline none --stage research"
     )
     assert run.spy.canary_served()
     run.check()
diff --git a/tests/issue_watch/test_security_invariants.py b/tests/issue_watch/test_security_invariants.py
index 7dbfeb7e3..550a540a7 100644
--- a/tests/issue_watch/test_security_invariants.py
+++ b/tests/issue_watch/test_security_invariants.py
@@ -3,7 +3,9 @@
 These tests pin the controls of design section 9.1 that cut across modules:
 
 - T1, NFR-001, AC-7: the only text after ``--prompt`` is
-  ``/sc:issue --claim <n> --pipeline none`` for an ``int`` in 1..999999999, whatever GitHub, the config or the login holds.
+  ``/sc:issue --claim <n> --pipeline <level> --stage <stage>`` for an ``int`` in
+  1..999999999, a level of none, worktree, full or full --submit and a stage of
+  research, spec, plan or debug, whatever GitHub, the config or the login holds.
 - T5, T9, NFR-002, NFR-003, AC-20: every argv the runner sees is one of the
   allowed forms, never names the upstream repository, ``{owner}``, a title or a
   body, and every REST path call carries ``--method GET`` (DF-28).
@@ -64,7 +66,13 @@ FORK = "IronbellyOrg/IronClaude"
 
 # Every prompt a launch may carry. ``fullmatch`` (not ``$``) so a trailing newline
 # fails too.
-_PROMPT_RE = re.compile(r"/sc:issue --claim [1-9][0-9]{0,8} --pipeline none")
+# Written out here, not imported from launch.py, so the test pins the closed set
+# instead of mirroring it.
+_PROMPT_RE = re.compile(
+    r"/sc:issue --claim [1-9][0-9]{0,8}"
+    r" --pipeline (?:none|worktree|full(?: --submit)?)"
+    r" --stage (?:research|spec|plan|debug)"
+)
 _TEXT_FIELD = re.compile(r"(?i)\b(?:title|body\w*)\b")
 _REST_PATH = re.compile(
     r"repos/IronbellyOrg/IronClaude/issues/[1-9][0-9]{0,8}(?:/(?:events|comments))?"
@@ -216,7 +224,12 @@ def _draw(rng: random.Random) -> object:
 # ==============================================================================
 
 
-def _literal_launch(orca: str, worktree: object, n: int) -> tuple[str, ...]:
+def _literal_launch(
+    orca: str,
+    worktree: object,
+    n: int,
+    tail: str = "--pipeline none --stage research",
+) -> tuple[str, ...]:
     """The FR-013 launch argv written out in full (T10), not built by the source."""
     return (
         orca,
@@ -229,7 +242,7 @@ def _literal_launch(orca: str, worktree: object, n: int) -> tuple[str, ...]:
         "--surface",
         "terminal",
         "--prompt",
-        f"/sc:issue --claim {n} --pipeline none",
+        f"/sc:issue --claim {n} {tail}",
         "--json",
     )
 
@@ -305,9 +318,8 @@ def classify_argv(argv: object, worktree: object) -> str:
     assert len(argv) == 12 and argv[1:3] == ["agent", "launch"], shown
     prompt = argv[10]
     assert is_claim_prompt(prompt), shown
-    assert tuple(argv) == _literal_launch(argv[0], worktree, int(prompt.split()[2])), (
-        shown
-    )
+    n, tail = prompt.split(" ", 3)[2], prompt.split(" ", 3)[3]
+    assert tuple(argv) == _literal_launch(argv[0], worktree, int(n), tail), shown
     return "launch"
 
 
@@ -482,8 +494,10 @@ def test_prompt_regex_property(tmp_path):
         kinds[type(value).__name__] += 1
         if is_claim_number(value):
             valid["valid"] += 1
-            prompt = build_claim_prompt(value)
-            assert prompt == f"/sc:issue --claim {value} --pipeline none", where
+            prompt = build_claim_prompt(value, "Research", None)
+            assert (
+                prompt == f"/sc:issue --claim {value} --pipeline none --stage research"
+            ), where
             assert is_claim_prompt(prompt), where
             argv = launch_argv(ORCA_PATH, worktree, prompt)
             assert len(argv) == 12 and argv[10] == prompt, where
@@ -491,7 +505,7 @@ def test_prompt_regex_property(tmp_path):
         else:
             valid["invalid"] += 1
             with pytest.raises(ValueError):
-                build_claim_prompt(value)
+                build_claim_prompt(value, "Research", None)
         # The launch layer takes only a string that is itself a claim prompt, so a
         # raw drawn value can never become the --prompt argument.
         if not is_claim_prompt(value):
@@ -525,9 +539,9 @@ def test_prompt_regex_property(tmp_path):
     for k, n in enumerate(numbers):
         ran = run_world(tmp_path / f"cycle-{k}", lambda w, n=n: w.issue(n))
         assert (ran.result.exit_code, ran.result.launched_issue) == (0, n), n
-        assert ran.prompts == [f"/sc:issue --claim {n} --pipeline none"], (
-            f"cycle {k}: issue {n}"
-        )
+        assert ran.prompts == [
+            f"/sc:issue --claim {n} --pipeline none --stage research"
+        ], f"cycle {k}: issue {n}"
         assert all(is_claim_prompt(p) for p in ran.prompts), n
         assert ran.store.load().entries[n].launches == 1, n
 
@@ -574,7 +588,7 @@ def test_hostile_labels_logins_and_commenters_never_reach_the_prompt(tmp_path, h
     ran = run_world(tmp_path, build)
     assert ran.result.exit_code == 0 and ran.result.reason == "cycle_complete"
     assert ran.result.launched_issue == 9
-    assert ran.prompts == ["/sc:issue --claim 9 --pipeline none"], (
+    assert ran.prompts == ["/sc:issue --claim 9 --pipeline none --stage research"], (
         f"hostile: {hostile!r:.100}"
     )
     assert ran.forms == list(SCENARIOS["eligible"].forms)
@@ -611,7 +625,7 @@ def test_hostile_config_labels_stay_one_argv_element_and_never_reach_the_prompt(
         config_over={"trigger_label": trigger, "approval_label": approval},
     )
     assert (ran.result.exit_code, ran.result.launched_issue) == (0, 9)
-    assert ran.prompts == ["/sc:issue --claim 9 --pipeline none"]
+    assert ran.prompts == ["/sc:issue --claim 9 --pipeline none --stage research"]
     holders = [argv for argv in ran.argvs if any(trigger in arg for arg in argv)]
     assert len(holders) == 1 and holders[0][:3] == ("gh", "issue", "list"), holders
     assert holders[0][holders[0].index("--label") + 1] == trigger  # one element
@@ -733,7 +747,10 @@ def test_every_argv_builder_of_the_package_gives_an_allowed_form(tmp_path):
             expected.append((github.argv_project_items(n, cursor), "graphql"))
             expected.append((github.argv_approval_events(n, cursor), "graphql"))
         expected.append(
-            (launch_argv(ORCA_PATH, worktree, build_claim_prompt(n)), "launch")
+            (
+                launch_argv(ORCA_PATH, worktree, build_claim_prompt(n, "Plan", "Full")),
+                "launch",
+            )
         )
     recorder = _Recorder()
     assert launch.check_origin(recorder, worktree, 5.0) == "origin_mismatch"
@@ -943,7 +960,9 @@ def test_both_graphql_constants_name_the_literal_repository_and_only_read(name):
     ],
 )
 def test_launch_argv_is_the_twelve_element_list_with_no_extra_flag(orca, worktree):
-    argv = launch_argv(orca, worktree, "/sc:issue --claim 9 --pipeline none")
+    argv = launch_argv(
+        orca, worktree, "/sc:issue --claim 9 --pipeline none --stage research"
+    )
     assert argv == [
         orca,
         "agent",
@@ -955,7 +974,7 @@ def test_launch_argv_is_the_twelve_element_list_with_no_extra_flag(orca, worktre
         "--surface",
         "terminal",
         "--prompt",
-        "/sc:issue --claim 9 --pipeline none",
+        "/sc:issue --claim 9 --pipeline none --stage research",
         "--json",
     ]
     assert len(argv) == 12
@@ -980,7 +999,7 @@ def test_the_launch_the_cycle_makes_is_the_literal_argv_in_the_worktree(tmp_path
             "--surface",
             "terminal",
             "--prompt",
-            "/sc:issue --claim 9 --pipeline none",
+            "/sc:issue --claim 9 --pipeline none --stage research",
             "--json",
         )
     ]
@@ -1017,6 +1036,6 @@ _DISPATCH_ENTRY_KEYS = {
 
 def test_dispatch_json_entries_keep_their_keys_with_the_pipeline_none_prompt(tmp_path):
     ran = run_world(tmp_path, lambda w: w.issue(9))
-    assert ran.prompts == ["/sc:issue --claim 9 --pipeline none"]
+    assert ran.prompts == ["/sc:issue --claim 9 --pipeline none --stage research"]
     raw = json.loads((ran.store.state_dir / "dispatch.json").read_text("utf-8"))
     assert set(raw["entries"]["9"]) == _DISPATCH_ENTRY_KEYS


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Fix pass after review 1: record.py stays unchanged (closed dispatch.json schema, guarded by tests). cycle._launch now keeps the claim prompt in launch-prompts.json beside the store (cycle._remember_prompt, mode 0600) just before the launch call, and status_report reads it (cycle._read_prompts), so the real status command prints a retry command again; an entry with no kept or valid prompt still gets argv None. tests/issue_watch and tests/issue_pipeline: 3003 passed. Probe: .dev tasks retries T7 probe-1-1.md (not for the reviewer to read).

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): F1.1 ac=T7.AC4 at=src/superclaude/cli/issue_watch/cli.py:161 anchor="it must keep printing a valid command for every allowed Status and Pipeline" chk=y,n,n,y family=status-retry fix=recover the prompt on the real path sev=blocking trigger=B4 first=start origin=new: status_report prints argv None unless the caller passes prompts; the CLI passes none

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
