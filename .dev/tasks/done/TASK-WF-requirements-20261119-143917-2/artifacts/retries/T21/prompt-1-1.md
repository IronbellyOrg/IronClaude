e3bf3867225640604102a3659be325fa6aaa2858
Review one task for spec compliance.

Task brief: ## Task 21: Run the first-run check and enable a repo

Create `src/superclaude/cli/issue_watch/first_run.py` (requirements R7, R18 and R28). For a freshly generated config it runs, in order: config validation (`check-config` logic), label creation through Task 20, `init-state`, one dry-run cycle (`once --dry-run` logic), the lock test (a second run while the lock is held ends with exit 75, using the store lock of `src/superclaude/cli/issue_watch/record.py`) and the restart test (the state document reloads and a second dry run changes nothing). All pass: it rewrites the config with `enabled: true`. Any fails: the config stays `enabled: false` and a one-line reason is written to `<state dir>/issue-watch/<name>/first-run.txt`. The report it writes also states the ship gate (`GOVERNED_LEVELS_ALLOWED`, Task 8: closed means only Pipeline None launches) and prints `approver_is_launch_account` when the approvers file holds the launch account (Task 9). It is idempotent: a repo whose state already exists is not re-initialised and a repo already enabled is left alone. It takes the same injectable base directories as Task 19. The live-test record of the runbook stays an owner check and is not part of this task.

Depends on: Task 8, Task 9, Task 19, Task 20

Acceptance criteria:
- T21.AC1: New `tests/issue_watch/test_first_run.py` covers: all pass gives `enabled: true`; a worktree that does not exist gives `enabled: false` with `worktree_invalid` in the report; a dry-run failure keeps it false; a held lock is detected by the lock test; a state document that does not reload fails the restart test; a second run changes nothing; the report shows the closed gate state and the launch-account warning.
- T21.AC2: No real `gh`, Orca or network call is made in the tests, and nothing is written under the real home.
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
Start sha: e3bf3867225640604102a3659be325fa6aaa2858
Diff against the start snapshot: diff --git a/tests/issue_watch/test_module_boundaries.py b/tests/issue_watch/test_module_boundaries.py
index 3917e6568..0f5dc51b4 100644
--- a/tests/issue_watch/test_module_boundaries.py
+++ b/tests/issue_watch/test_module_boundaries.py
@@ -75,6 +75,12 @@ RULES: dict[str, Rule] = {
     "repos": Rule(siblings=frozenset({"runner", "launch"})),
     # plan Task 20: the trigger label and the Approved field check; the one watcher module that creates a label.
     "repo_init": Rule(siblings=frozenset({"defaults", "github", "runner"})),
+    # plan Task 21: the first-run check; it sequences the other modules and runs nothing itself.
+    "first_run": Rule(
+        siblings=frozenset(
+            {"cycle", "defaults", "launch", "record", "repo_init", "runner"}
+        )
+    ),
     # plan Task 19: one repo's generated config; reads through the Runner, writes two files.
     "generate": Rule(
         siblings=frozenset({"cycle", "defaults", "github", "repos", "runner"})
diff --git a/src/superclaude/cli/issue_watch/first_run.py b/src/superclaude/cli/issue_watch/first_run.py
new file mode 100644
index 000000000..46038d597
--- /dev/null
+++ b/src/superclaude/cli/issue_watch/first_run.py
@@ -0,0 +1,252 @@
+"""The first-run check of one repository's generated configuration (plan Task 21, R7, R18, R28).
+
+A freshly generated config starts ``enabled: false``. ``first_run`` turns it on only after a
+fixed list of checks all pass, in this order:
+
+1. ``config``: the platform, ``cycle.load_config`` and ``cycle.validate_setup`` (the logic of
+   ``check-config``);
+2. ``label``: the trigger label exists on the repository (created through ``repo_init``);
+3. ``init_state``: the state directory and store exist (a store that already exists is kept, never
+   re-initialised);
+4. ``dry_run``: one dry-run cycle exits 0 (the logic of ``once --dry-run``);
+5. ``lock``: while the store lock is held, a second cycle ends with exit 75;
+6. ``restart``: the state document reloads, a second dry-run exits 0, and ``dispatch.json`` is
+   byte-for-byte what it was before the first dry-run.
+
+When every step passes the config is rewritten with ``enabled: true`` (an atomic replace that
+keeps mode 600). When one fails the config stays ``enabled: false``. Either way a short report is
+written to ``<state dir>/first-run.txt``: the result line, the ship gate (``GOVERNED_LEVELS_ALLOWED``
+of ``launch.py``: closed means only Pipeline None launches), the check of the ``Approved`` field and
+``warning: approver_is_launch_account`` when the approvers file holds the launch account.
+
+It is idempotent: a repository whose config is already enabled is left alone and runs no check.
+Nothing here runs a process itself: the dry-run cycles take their dependencies from the caller's
+``deps_factory`` and every ``gh`` call goes through the caller's ``Runner``. The base directories
+and the clock are injectable, so a test writes only under ``tmp_path``.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+from collections.abc import Callable
+from dataclasses import dataclass, field
+from datetime import datetime, timezone
+from pathlib import Path
+
+from . import cycle, launch, record, repo_init
+from .defaults import Defaults
+from .runner import Runner
+
+REPORT_FILE = "first-run.txt"
+LOCK_HELD_EXIT = 75
+
+STEPS = ("config", "label", "init_state", "dry_run", "lock", "restart")
+
+
+@dataclass(frozen=True)
+class Step:
+    name: str
+    ok: bool
+    reason: str = "ok"
+
+
+@dataclass(frozen=True)
+class FirstRunResult:
+    """``enabled`` is the config's ``enabled`` after the call; ``status`` says what happened."""
+
+    status: str  # "enabled", "failed" or "already_enabled"
+    enabled: bool
+    steps: tuple[Step, ...] = ()
+    report: str = ""
+    report_path: Path | None = None
+    notes: list[str] = field(default_factory=list)
+
+
+def _now() -> datetime:
+    return datetime.now(timezone.utc)
+
+
+def _raw_config(path: Path) -> dict | None:
+    try:
+        raw = json.loads(path.read_bytes())
+    except (OSError, ValueError, RecursionError):
+        return None
+    return raw if isinstance(raw, dict) else None
+
+
+def _report_dir(config_path: Path, raw: dict | None) -> Path:
+    """The state dir named in the config, else the folder that holds the config."""
+    state = raw.get("state_dir") if raw else None
+    if isinstance(state, str) and os.path.isabs(state):
+        return Path(state)
+    return config_path.parent
+
+
+def _write_report(directory: Path, text: str, name: str = REPORT_FILE) -> Path | None:
+    path = directory / name
+    try:
+        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
+        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
+        with os.fdopen(fd, "w", encoding="utf-8") as handle:
+            handle.write(text)
+    except OSError:
+        return None
+    return path
+
+
+def _enable(config_path: Path, raw: dict) -> bool:
+    """Rewrite the config with ``enabled: true``; an atomic replace that keeps mode 600."""
+    staged = config_path.with_name(f".{config_path.name}.enable")
+    try:
+        fd = os.open(
+            staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600
+        )
+        with os.fdopen(fd, "w", encoding="utf-8") as handle:
+            handle.write(
+                json.dumps({**raw, "enabled": True}, indent=2, sort_keys=True) + "\n"
+            )
+        cycle.load_config(staged)  # the rewritten file must still load
+        os.replace(staged, config_path)
+        return True
+    except (OSError, cycle.ConfigError):
+        return False
+    finally:
+        staged.unlink(missing_ok=True)
+
+
+def _store_bytes(state_dir: Path) -> bytes | None:
+    try:
+        return (state_dir / record.STORE_FILE).read_bytes()
+    except OSError:
+        return None
+
+
+def first_run(
+    config_path: Path,
+    defaults: Defaults,
+    runner: Runner,
+    deps_factory: Callable[[cycle.Config], cycle.Deps],
+    *,
+    now: Callable[[], datetime] = _now,
+) -> FirstRunResult:
+    """Run the first-run check for ``config_path`` and enable it when every step passes."""
+    config_path = Path(config_path)
+    raw = _raw_config(config_path)
+    if raw is not None and raw.get("enabled") is True:
+        return FirstRunResult("already_enabled", True)
+    directory = _report_dir(config_path, raw)
+    # A config with no readable state_dir reports next to itself, under its own name, so two
+    # repositories never overwrite one report.
+    report_name = (
+        REPORT_FILE
+        if directory != config_path.parent
+        else (f"{config_path.stem}-{REPORT_FILE}")
+    )
+    steps: list[Step] = []
+    lines: list[str] = []
+
+    def done(failed: Step | None) -> FirstRunResult:
+        ok = failed is None
+        enabled = False
+        if ok and raw is not None:
+            enabled = _enable(config_path, raw)
+            if not enabled:
+                failed = Step("config", False, "enable_failed")
+                steps.append(failed)
+                ok = False
+        head = (
+            "first-run: passed"
+            if ok
+            else f"first-run: failed {failed.name}: {failed.reason}"
+        )  # type: ignore[union-attr]
+        gate = "open" if launch.GOVERNED_LEVELS_ALLOWED else "closed"
+        gate_note = (
+            "all pipeline levels may launch"
+            if gate == "open"
+            else "only Pipeline None launches"
+        )
+        text = "\n".join([head, f"ship_gate: {gate} ({gate_note})", *lines]) + "\n"
+        path = _write_report(directory, text, report_name)
+        return FirstRunResult(
+            "enabled" if ok else "failed", enabled, tuple(steps), text, path
+        )
+
+    # 1. config: the platform, the file, the worktree and the approvers
+    try:
+        cycle.check_platform()
+        config = cycle.load_config(config_path)
+        approvers = cycle.validate_setup(config)
+    except cycle.ConfigError as exc:
+        step = Step("config", False, exc.reason)
+        steps.append(step)
+        return done(step)
+    steps.append(Step("config", True))
+    directory = config.state_dir  # the report now lives in the state directory
+    report_name = REPORT_FILE
+    if config.owner_account_id in approvers and (
+        config.owner_account_id not in config.approval_excluded_ids
+    ):
+        lines.append("warning: approver_is_launch_account")
+
+    # 2. the trigger label (created when missing) and the Approved field (reported only)
+    label = repo_init.ensure_trigger_label(config.repo, defaults, runner)
+    lines.append(f"trigger_label: {label}")
+    owner = config.repo.split("/")[0]
+    lines.append(
+        f"approved_field: {repo_init.check_approved_field(owner, defaults, runner)}"
+    )
+    if label not in (repo_init.CREATED, repo_init.PRESENT):
+        step = Step("label", False, "label_failed")
+        steps.append(step)
+        return done(step)
+    steps.append(Step("label", True, label))
+
+    # 3. the state directory and store; an existing store is kept, never re-initialised
+    try:
+        record.init_state(config.state_dir, now())
+        steps.append(Step("init_state", True, "created"))
+    except record.StateExists:
+        steps.append(Step("init_state", True, "state_exists"))
+    except record.StoreError as exc:
+        step = Step("init_state", False, exc.reason)
+        steps.append(step)
+        return done(step)
+    baseline = _store_bytes(config.state_dir)
+
+    # 4. one dry-run cycle
+    first = cycle.run_cycle(deps_factory(config), True)
+    if first.exit_code != 0:
+        step = Step("dry_run", False, str(first.reason))
+        steps.append(step)
+        return done(step)
+    steps.append(Step("dry_run", True))
+
+    # 5. the lock test: while the store lock is held, a second cycle ends with exit 75
+    second_deps = deps_factory(config)
+    with second_deps.store.lock():
+        held = cycle.run_cycle(deps_factory(config), True)
+    if held.exit_code != LOCK_HELD_EXIT:
+        step = Step("lock", False, "lock_not_detected")
+        steps.append(step)
+        return done(step)
+    steps.append(Step("lock", True))
+
+    # 6. the restart test: the state reloads and a second dry-run changes nothing
+    try:
+        record.FileStore(config.state_dir).load()
+    except record.StoreError:
+        step = Step("restart", False, "state_not_reloadable")
+        steps.append(step)
+        return done(step)
+    again = cycle.run_cycle(deps_factory(config), True)
+    if again.exit_code != 0:
+        step = Step("restart", False, f"dry_run:{again.reason}")
+        steps.append(step)
+        return done(step)
+    if _store_bytes(config.state_dir) != baseline:
+        step = Step("restart", False, "state_changed")
+        steps.append(step)
+        return done(step)
+    steps.append(Step("restart", True))
+    return done(None)
diff --git a/tests/issue_watch/test_first_run.py b/tests/issue_watch/test_first_run.py
new file mode 100644
index 000000000..d757a82ed
--- /dev/null
+++ b/tests/issue_watch/test_first_run.py
@@ -0,0 +1,352 @@
+"""Task 21: the first-run check and enabling a repo.
+
+No real ``gh``, Orca or network call is made: the cycles run over a ``GhWorld`` and a
+``FakeLauncher``, the label and field reads over a scripted runner. HOME and XDG are redirected
+into ``tmp_path`` and the tests assert nothing was written there.
+"""
+
+from __future__ import annotations
+
+import dataclasses
+import json
+import os
+import stat
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_watch import (
+    audit,
+    cycle,
+    defaults,
+    first_run,
+    launch,
+    record,
+    repo_init,
+)
+from superclaude.cli.issue_watch.record import FileStore
+
+from .conftest import (
+    CYCLE_NOW,
+    FakeClock,
+    FakeLauncher,
+    GhWorld,
+    default_which,
+    launched_outcome,
+    result,
+)
+
+REPO = "IronbellyOrg/IronClaude"
+DEFAULTS = defaults.Defaults()
+LAUNCH_ID = 1001
+
+
+@pytest.fixture(autouse=True)
+def _home(tmp_path, monkeypatch):
+    monkeypatch.setenv("HOME", str(tmp_path / "home"))
+    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
+
+
+def _config(tmp_path: Path, *, approvers=(11, 22), worktree=True, **extra) -> Path:
+    work = tmp_path / "worktrees" / "IronClaude" / "Coordinator"
+    if worktree:
+        work.mkdir(parents=True)
+    approvers_file = tmp_path / "cfg" / "approvers.txt"
+    approvers_file.parent.mkdir(parents=True, exist_ok=True)
+    approvers_file.write_text("".join(f"{i}\n" for i in approvers))
+    approvers_file.chmod(0o600)
+    raw = {
+        "schema_version": 1,
+        "enabled": False,
+        "repo": REPO,
+        "project_id": "PVT_abc",
+        "owner_account_id": LAUNCH_ID,
+        "worktree": str(work),
+        "approvers_file": str(approvers_file),
+        "state_dir": str(tmp_path / "state" / "issue-watch" / "IronClaude"),
+        **extra,
+    }
+    path = tmp_path / "cfg" / "IronClaude.json"
+    path.write_text(json.dumps(raw))
+    path.chmod(0o600)
+    return path
+
+
+class Router:
+    """The label and field reads go to a script; everything else to the world's runner."""
+
+    def __init__(self, world: GhWorld, labels=("bug",), field_ok=True) -> None:
+        self.world, self.calls = world, []
+        self.created: list[tuple[str, ...]] = []
+        self.labels = list(labels)
+        self.field_ok = field_ok
+
+    def run(self, argv, timeout, *, cwd=None):
+        key = tuple(argv)
+        self.calls.append(key)
+        if key[:3] == ("gh", "label", "list"):
+            return result(stdout=json.dumps([{"name": n} for n in self.labels]))
+        if key[:3] == ("gh", "label", "create"):
+            self.created.append(key)
+            self.labels.append(key[3])
+            return result()
+        if key[:4] == ("gh", "api", "--method", "GET") and "issue-fields" in key[4]:
+            row = {"name": "Approved", "data_type": "single_select"}
+            row["options"] = [{"name": "Yes" if self.field_ok else "No"}]
+            return result(stdout=json.dumps([row]))
+        return self.world.runner.run(argv, timeout, cwd=cwd)
+
+
+class Harness:
+    def __init__(self, tmp_path: Path, **config_kw) -> None:
+        self.path = _config(tmp_path, **config_kw)
+        self.cfg = cycle.load_config(self.path)
+        self.world = GhWorld(FakeClock(CYCLE_NOW), self.cfg)
+        self.router = Router(self.world)
+        self.launcher = FakeLauncher([launched_outcome()])
+        self.factory_calls = 0
+        self.on_factory = None
+
+    def factory(self, cfg: cycle.Config) -> cycle.Deps:
+        self.factory_calls += 1
+        if self.on_factory:
+            self.on_factory(self.factory_calls, cfg)
+        return cycle.Deps(
+            runner=self.world.runner,
+            store=FileStore(cfg.state_dir),
+            launcher=self.launcher,
+            clock=self.world.clock,
+            audit=audit.AuditLog(cfg.state_dir),
+            config=cfg,
+            which=default_which,
+            host="test-host",
+        )
+
+    def run(self):
+        return first_run.first_run(
+            self.path,
+            DEFAULTS,
+            self.router,
+            self.factory,
+            now=lambda: CYCLE_NOW,
+        )
+
+    def enabled(self) -> bool:
+        return json.loads(self.path.read_text())["enabled"]
+
+    @property
+    def report(self) -> Path:
+        return self.cfg.state_dir / first_run.REPORT_FILE
+
+
+def _no_real_calls(h: Harness, tmp_path: Path) -> None:
+    assert h.launcher.calls == []  # no Orca launch
+    assert not (tmp_path / "home").exists()  # nothing under the redirected home
+    assert not any(a[0] == "orca" for a, _ in h.world.runner.calls)
+
+
+def test_when_every_step_passes_the_config_is_enabled(tmp_path) -> None:
+    h = Harness(tmp_path)
+    out = h.run()
+    assert out.status == "enabled" and out.enabled and h.enabled()
+    assert [(s.name, s.ok) for s in out.steps] == [(n, True) for n in first_run.STEPS]
+    assert cycle.load_config(h.path).enabled is True
+    assert stat.S_IMODE(h.path.stat().st_mode) == 0o600
+    assert (h.cfg.state_dir / "dispatch.json").exists()
+    assert h.report.read_text().splitlines()[0] == "first-run: passed"
+    assert h.router.created == [
+        (
+            "gh",
+            "label",
+            "create",
+            "issue-watch:trigger",
+            "--repo",
+            REPO,
+            "--color",
+            repo_init.LABEL_COLOR,
+            "--description",
+            repo_init.LABEL_DESCRIPTION,
+        )
+    ]
+    _no_real_calls(h, tmp_path)
+
+
+def test_a_worktree_that_does_not_exist_keeps_the_config_disabled(tmp_path) -> None:
+    h = Harness(tmp_path, worktree=False)
+    out = h.run()
+    assert out.status == "failed" and not h.enabled()
+    assert [s.name for s in out.steps] == ["config"]
+    text = h.report.read_text() if h.report.exists() else out.report
+    assert "worktree_invalid" in text and "first-run: failed config" in text
+    assert h.router.calls == []  # nothing was read or created
+    assert not (h.cfg.state_dir / "dispatch.json").exists()
+
+
+def test_a_dry_run_failure_keeps_the_config_disabled(tmp_path) -> None:
+    h = Harness(tmp_path)
+    h.world.fail("origin", "foreign_origin", times=None)
+    out = h.run()
+    assert out.status == "failed" and not h.enabled()
+    failing = out.steps[-1]
+    assert (failing.name, failing.ok) == ("dry_run", False)
+    assert failing.reason == "origin_mismatch"
+    assert h.report.read_text().splitlines()[0] == (
+        "first-run: failed dry_run: origin_mismatch"
+    )
+
+
+def test_a_failed_label_stops_before_the_state_is_created(tmp_path) -> None:
+    h = Harness(tmp_path)
+
+    class NoCreate(Router):
+        def run(self, argv, timeout, *, cwd=None):
+            if tuple(argv)[:3] == ("gh", "label", "create"):
+                return result(stderr="HTTP 403", returncode=1)
+            return super().run(argv, timeout, cwd=cwd)
+
+    h.router = NoCreate(h.world)
+    out = h.run()
+    assert (out.steps[-1].name, out.steps[-1].reason) == ("label", "label_failed")
+    assert not h.enabled() and not (h.cfg.state_dir / "dispatch.json").exists()
+
+
+def test_a_held_lock_is_detected_by_the_lock_test(tmp_path) -> None:
+    h = Harness(tmp_path)
+    out = h.run()
+    lock = next(s for s in out.steps if s.name == "lock")
+    assert lock.ok  # the second cycle really ended with exit 75 while the lock was held
+
+
+def test_a_lock_that_does_not_hold_fails_the_lock_test(tmp_path, monkeypatch) -> None:
+    h = Harness(tmp_path)
+    real = cycle.run_cycle
+    seen = {"n": 0}
+
+    def fake(deps, dry_run):
+        seen["n"] += 1
+        res = real(deps, dry_run)
+        if seen["n"] == 2:  # the cycle that ran while the lock was held
+            assert res.exit_code == 75  # the real lock did hold; now pretend it did not
+            return dataclasses.replace(res, exit_code=0, reason="ok")
+        return res
+
+    monkeypatch.setattr(first_run.cycle, "run_cycle", fake)
+    out = h.run()
+    assert (out.steps[-1].name, out.steps[-1].reason) == ("lock", "lock_not_detected")
+    assert not h.enabled()
+
+
+def test_a_state_document_that_does_not_reload_fails_the_restart_test(tmp_path) -> None:
+    h = Harness(tmp_path)
+
+    def corrupt(n: int, cfg: cycle.Config) -> None:
+        if n == 3:  # deps made for the lock test's second cycle
+            (cfg.state_dir / "dispatch.json").write_bytes(b"{not json")
+
+    h.on_factory = corrupt
+    out = h.run()
+    assert (out.steps[-1].name, out.steps[-1].reason) == (
+        "restart",
+        "state_not_reloadable",
+    )
+    assert not h.enabled()
+    assert "first-run: failed restart: state_not_reloadable" in h.report.read_text()
+
+
+def test_a_second_dry_run_that_changes_the_store_fails_the_restart_test(
+    tmp_path,
+) -> None:
+    h = Harness(tmp_path)
+
+    def tweak(n: int, cfg: cycle.Config) -> None:
+        if n == 4:  # deps made for the restart test's dry-run
+            path = cfg.state_dir / "dispatch.json"
+            doc = json.loads(path.read_text())
+            doc["considered"] = {"7": "2026-11-16T10:00:00Z"}
+            path.write_text(json.dumps(doc))
+
+    h.on_factory = tweak
+    out = h.run()
+    assert (out.steps[-1].name, out.steps[-1].reason) == ("restart", "state_changed")
+    assert not h.enabled()
+
+
+def test_a_second_run_changes_nothing(tmp_path) -> None:
+    h = Harness(tmp_path)
+    assert h.run().status == "enabled"
+    config_bytes = h.path.read_bytes()
+    store_bytes = (h.cfg.state_dir / "dispatch.json").read_bytes()
+    calls = (len(h.router.calls), len(h.world.runner.calls), h.factory_calls)
+    again = h.run()
+    assert again.status == "already_enabled" and again.steps == ()
+    assert h.path.read_bytes() == config_bytes
+    assert (h.cfg.state_dir / "dispatch.json").read_bytes() == store_bytes
+    assert (len(h.router.calls), len(h.world.runner.calls), h.factory_calls) == calls
+
+
+def test_a_state_that_already_exists_is_kept_and_not_re_initialised(tmp_path) -> None:
+    h = Harness(tmp_path)
+    store = record.init_state(h.cfg.state_dir, CYCLE_NOW)
+    before = (h.cfg.state_dir / "dispatch.json").read_bytes()
+    out = h.run()
+    step = next(s for s in out.steps if s.name == "init_state")
+    assert (step.ok, step.reason) == (True, "state_exists")
+    assert out.status == "enabled"
+    assert (h.cfg.state_dir / "dispatch.json").read_bytes() == before
+    assert store is not None
+
+
+def test_the_report_shows_the_closed_gate_and_the_launch_account_warning(
+    tmp_path,
+) -> None:
+    h = Harness(tmp_path, approvers=(11, LAUNCH_ID))
+    out = h.run()
+    lines = h.report.read_text().splitlines()
+    assert launch.GOVERNED_LEVELS_ALLOWED is False
+    assert "ship_gate: closed (only Pipeline None launches)" in lines
+    assert "warning: approver_is_launch_account" in lines
+    assert "approved_field: approved_field_present" in lines
+    assert "trigger_label: created" in lines
+    assert out.report == h.report.read_text()
+
+
+def test_no_warning_when_the_launch_account_is_not_an_approver(tmp_path) -> None:
+    h = Harness(tmp_path)
+    h.run()
+    assert "approver_is_launch_account" not in h.report.read_text()
+
+
+def test_an_open_gate_is_reported_open(tmp_path, monkeypatch) -> None:
+    monkeypatch.setattr(launch, "GOVERNED_LEVELS_ALLOWED", True)
+    h = Harness(tmp_path)
+    h.run()
+    assert "ship_gate: open (all pipeline levels may launch)" in h.report.read_text()
+
+
+def test_a_missing_approved_field_is_reported_but_does_not_block(tmp_path) -> None:
+    h = Harness(tmp_path)
+    h.router.field_ok = False
+    out = h.run()
+    assert out.status == "enabled"
+    assert "approved_field: approved_field_missing" in h.report.read_text()
+
+
+def test_the_report_file_is_private(tmp_path) -> None:
+    h = Harness(tmp_path)
+    h.run()
+    assert stat.S_IMODE(h.report.stat().st_mode) == 0o600
+    assert stat.S_IMODE(h.cfg.state_dir.stat().st_mode) == 0o700
+
+
+def test_an_unreadable_config_reports_next_to_itself_under_its_own_name(
+    tmp_path,
+) -> None:
+    path = tmp_path / "cfg" / "Broken.json"
+    path.parent.mkdir()
+    path.write_text("not json")
+    h = Harness(tmp_path)  # only for its router and factory
+    out = first_run.first_run(path, DEFAULTS, h.router, h.factory)
+    assert out.status == "failed" and not out.enabled
+    assert out.report_path == path.parent / "Broken-first-run.txt"
+    assert "config_invalid" in out.report_path.read_text()
+    assert os.path.exists(path) and path.read_text() == "not json"

Task 21 context. first_run.py is new; it takes a deps_factory (the caller passes cli.build_deps) so it runs no process itself, and the module-boundaries table gained a "first_run" row. The report file is `<state dir>/first-run.txt`; a config whose state_dir cannot be read reports next to itself as `<config stem>-first-run.txt`. The `Approved` field check is reported but does not block enabling (it is an organization setting for the owner). The dry-run writes only dry-run.json; "changes nothing" is checked on dispatch.json byte for byte. Tests run: tests/issue_watch 2960 passed; ruff clean; make verify-sync clean; no real home written (HOME redirected).

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
