045b0a1d8cc199ad2e4bdc3ff50fa0d74643b5a4
Review one task for spec compliance.

Task brief: ## Task 23: Write the dispatcher core

Create `src/superclaude/cli/issue_watch/dispatch.py` with the loop of requirements R5, R15, R16, R26 and R32. It lists repos (Task 18), calls `ensure_config` and `first_run` (Tasks 19 and 21) for any repo without a config, then starts `superclaude issue-watch once --config <file>` as a child process per repo, one after another. Rules: total loop cap 270 seconds; each child is killed after 255 seconds, longer than the cycle's own 240 second deadline (`DEADLINE_TOTAL_S`, `cycle.py` line 41); repos not reached are skipped and reported; the repo order rotates each sweep (the next start index is kept in a small file under the state directory); the loop stops starting children after the first child whose output has a `launched:` or an `attempted:` line; a child killed or timed out counts as a launch attempt and stops the loop too, unless the repo's `dispatch.json` store (read through `record.py`, read-only) shows no pending or launched entry created during this sweep; `DAY_CAP` stays per repo. Use the `Runner` interface so tests use fakes, pass absolute paths because cron has no PATH, and take the injectable base directories of Task 19.

Depends on: Task 18, Task 19, Task 21, Task 22

Acceptance criteria:
- T23.AC1: New `tests/issue_watch/test_dispatch.py` covers: rotation across three sweeps, a stop after the first `launched:` line, a stop after an `attempted:` line, a child killed after 255 seconds with a pending store entry stopping the loop, the same kill with no pending entry letting later repos run, the 270 second cap with unreached repos reported, a repo with no config being generated first, and a failed `orca repo list` giving an error result rather than a clean one.
- T23.AC2: A child timeout never kills the loop, and each child's exit code and reason are kept for Task 25.
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
Start sha: 045b0a1d8cc199ad2e4bdc3ff50fa0d74643b5a4
Diff against the start snapshot: diff --git a/tests/issue_watch/test_module_boundaries.py b/tests/issue_watch/test_module_boundaries.py
index 0f5dc51b4..e57ac45c1 100644
--- a/tests/issue_watch/test_module_boundaries.py
+++ b/tests/issue_watch/test_module_boundaries.py
@@ -81,6 +81,12 @@ RULES: dict[str, Rule] = {
             {"cycle", "defaults", "launch", "record", "repo_init", "runner"}
         )
     ),
+    # plan Task 23: the dispatcher core; commands only through the Runner, no subprocess import.
+    "dispatch": Rule(
+        siblings=frozenset(
+            {"cycle", "defaults", "first_run", "generate", "record", "repos", "runner"}
+        )
+    ),
     # plan Task 19: one repo's generated config; reads through the Runner, writes two files.
     "generate": Rule(
         siblings=frozenset({"cycle", "defaults", "github", "repos", "runner"})
diff --git a/src/superclaude/cli/issue_watch/dispatch.py b/src/superclaude/cli/issue_watch/dispatch.py
new file mode 100644
index 000000000..5bd00c76c
--- /dev/null
+++ b/src/superclaude/cli/issue_watch/dispatch.py
@@ -0,0 +1,281 @@
+"""The dispatcher core: one sweep over every Orca repository (plan Task 23, R5, R15, R16, R26, R32).
+
+One cron entry runs a sweep. A sweep:
+
+1. lists the usable repositories with ``orca repo list`` (Task 18). A failed or unreadable list is
+   an error result, never a clean one (R15);
+2. for a repository with no config, generates one (Task 19) and runs its first-run check (Task 21);
+   a repository whose config is not enabled is skipped with a reason, not run;
+3. starts ``superclaude issue-watch once --config <file>`` as a child process for each enabled
+   repository, one after another, through the ``Runner`` (absolute paths only: cron has no PATH).
+
+Rules:
+
+* the whole loop stops starting children after ``LOOP_CAP_S`` (270 s); each child is killed after
+  ``CHILD_TIMEOUT_S`` (255 s), longer than the cycle's own 240 s deadline. A repository not reached is
+  skipped with a reason and reported;
+* the order rotates every sweep: the next start index is kept in ``rotation.json`` under the state
+  directory. A sweep that did not reach every repository starts the next one at the first repository
+  it did not reach;
+* the loop stops starting children after the first child whose output holds a ``launched:`` or an
+  ``attempted:`` line. A child that was killed or timed out counts as a launch attempt and stops the
+  loop too, unless that repository's ``dispatch.json`` (read through ``record.py``, read only) shows no
+  pending, launched or unknown entry created during this sweep. A child that cannot run, or that
+  exits non-zero without launching, never stops the loop, and a timeout never kills it;
+* ``DAY_CAP`` stays per repository: the cycle of each child applies it.
+
+Each child's exit code and reason are kept in ``ChildResult`` for the report (Task 25). This module
+runs nothing itself: every command goes through the ``Runner``.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import re
+import time
+from collections.abc import Callable
+from dataclasses import dataclass, field
+from datetime import datetime, timezone
+from pathlib import Path
+
+from . import cycle, record
+from .defaults import Defaults
+from .first_run import first_run
+from .generate import Base, ensure_config
+from .repos import OrcaRepo, RepoListError, list_repos
+from .runner import Runner
+
+LOOP_CAP_S = 270.0
+CHILD_TIMEOUT_S = 255.0
+ROTATION_FILE = "rotation.json"
+SUBDIR = "issue-watch.d"
+
+_LAUNCHED = re.compile(r"^launched: ([1-9][0-9]{0,8})$", re.M)
+_ATTEMPTED = re.compile(r"^attempted: ([1-9][0-9]{0,8})$", re.M)
+_REASON = re.compile(r"^cycle: ([a-z][a-z0-9_]{0,63})$", re.M)
+_OPEN_STATES = ("pending", "launched", "unknown")
+
+
+@dataclass(frozen=True)
+class ChildResult:
+    """What one child did; kept for the report."""
+
+    name: str
+    repo: str
+    exit_code: int | None
+    reason: str | None
+    launched: int | None = None
+    attempted: int | None = None
+    killed: bool = False
+    seconds: float = 0.0
+
+
+@dataclass(frozen=True)
+class Skipped:
+    name: str
+    reason: str
+
+
+@dataclass(frozen=True)
+class SweepResult:
+    """``error`` is set (and ``ok`` false) when the repository list could not be read."""
+
+    ok: bool
+    error: str | None = None
+    children: tuple[ChildResult, ...] = ()
+    skipped: tuple[Skipped, ...] = ()
+    stopped_after: str | None = None
+    elapsed_s: float = 0.0
+    generated: tuple[str, ...] = ()
+    notes: list[str] = field(default_factory=list)
+
+
+def _now() -> datetime:
+    return datetime.now(timezone.utc)
+
+
+# --- rotation ------------------------------------------------------------------------------
+
+
+def _rotation_path(base: Base) -> Path:
+    return base.state_dir.expanduser() / "issue-watch" / ROTATION_FILE
+
+
+def _read_rotation(base: Base) -> int:
+    try:
+        raw = json.loads(_rotation_path(base).read_text(encoding="utf-8"))
+        value = raw["next"]
+    except (OSError, ValueError, KeyError, TypeError):
+        return 0
+    return value if type(value) is int and value >= 0 else 0
+
+
+def _write_rotation(base: Base, value: int) -> None:
+    path = _rotation_path(base)
+    try:
+        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
+        staged = path.with_name(f".{path.name}.new")
+        fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
+        with os.fdopen(fd, "w", encoding="utf-8") as handle:
+            handle.write(json.dumps({"next": value}) + "\n")
+        os.replace(staged, path)
+    except OSError:
+        pass  # the rotation is a fairness aid; losing it only restarts at the first repo
+
+
+# --- children -----------------------------------------------------------------------------
+
+
+def _config_path(base: Base, name: str) -> Path:
+    return base.config_dir.expanduser() / SUBDIR / f"{name}.json"
+
+
+def _enabled(path: Path) -> bool | None:
+    try:
+        raw = json.loads(path.read_bytes())
+    except (OSError, ValueError, RecursionError):
+        return None
+    return raw.get("enabled") if isinstance(raw, dict) else None
+
+
+def _opened_this_sweep(config_path: Path, since: datetime) -> bool:
+    """True unless the repo's store shows no open entry created at or after ``since``.
+
+    Read only, through ``record.py``. A store that cannot be read counts as open: the loop stops.
+    """
+    try:
+        config = cycle.load_config(config_path)
+        doc = record.FileStore(config.state_dir).load()
+    except (cycle.ConfigError, record.StoreError, OSError):
+        return True
+    return any(
+        e.state in _OPEN_STATES and e.pending_at is not None and e.pending_at >= since
+        for e in doc.entries.values()
+    )
+
+
+def _run_child(
+    runner: Runner,
+    superclaude: str,
+    repo: OrcaRepo,
+    config_path: Path,
+    monotonic: Callable[[], float],
+) -> ChildResult:
+    argv = [superclaude, "issue-watch", "once", "--config", str(config_path)]
+    started = monotonic()
+    result = runner.run(argv, CHILD_TIMEOUT_S)
+    seconds = round(monotonic() - started, 3)
+    if result.timed_out:
+        return ChildResult(
+            repo.name, repo.slug, None, "child_timeout", killed=True, seconds=seconds
+        )
+    if result.spawn_error is not None:
+        return ChildResult(repo.name, repo.slug, None, "spawn_error", seconds=seconds)
+    launched = _LAUNCHED.search(result.stdout)
+    attempted = _ATTEMPTED.search(result.stdout)
+    reason = _REASON.search(result.stdout)
+    return ChildResult(
+        repo.name,
+        repo.slug,
+        result.returncode,
+        reason.group(1) if reason else None,
+        launched=int(launched.group(1)) if launched else None,
+        attempted=int(attempted.group(1)) if attempted else None,
+        seconds=seconds,
+    )
+
+
+def run_sweep(
+    runner: Runner,
+    *,
+    orca: str,
+    superclaude: str,
+    defaults: Defaults,
+    base: Base,
+    deps_factory: Callable[[cycle.Config], cycle.Deps],
+    monotonic: Callable[[], float] = time.monotonic,
+    now: Callable[[], datetime] = _now,
+) -> SweepResult:
+    """Run one sweep; see the module docstring for the rules."""
+    for label, path in (("orca", orca), ("superclaude", superclaude)):
+        if not os.path.isabs(path):
+            raise ValueError(f"{label} must be an absolute path (cron has no PATH)")
+    began = monotonic()
+    since = now()
+    try:
+        listing = list_repos(runner, orca, defaults.allowed_owners)
+    except RepoListError as exc:
+        return SweepResult(False, error=exc.reason)
+    repos = sorted(listing.repos, key=lambda r: r.name)
+    skipped = [Skipped(s.name, s.reason) for s in listing.skipped]
+    children: list[ChildResult] = []
+    generated: list[str] = []
+    stopped_after: str | None = None
+    if not repos:
+        return SweepResult(
+            True, skipped=tuple(skipped), elapsed_s=round(monotonic() - began, 3)
+        )
+
+    start = _read_rotation(base) % len(repos)
+    order = repos[start:] + repos[:start]
+    first_unreached: int | None = None
+    for position, repo in enumerate(order):
+        if stopped_after is not None:
+            skipped.append(Skipped(repo.name, "stopped_after_launch"))
+            first_unreached = (
+                first_unreached if first_unreached is not None else position
+            )
+            continue
+        if monotonic() - began >= LOOP_CAP_S:
+            skipped.append(Skipped(repo.name, "loop_cap"))
+            first_unreached = (
+                first_unreached if first_unreached is not None else position
+            )
+            continue
+        config_path = _config_path(base, repo.name)
+        if not config_path.exists():
+            outcome = ensure_config(repo, defaults, runner, base)
+            if outcome.status == "skipped":
+                skipped.append(Skipped(repo.name, outcome.reason or "not_generated"))
+                continue
+            if outcome.status == "generated":
+                generated.append(repo.name)
+                first_run(config_path, defaults, runner, deps_factory)
+        enabled = _enabled(config_path)
+        if enabled is not True:
+            skipped.append(
+                Skipped(
+                    repo.name,
+                    "not_enabled" if enabled is False else "config_unreadable",
+                )
+            )
+            continue
+        child = _run_child(runner, superclaude, repo, config_path, monotonic)
+        children.append(child)
+        if child.launched is not None or child.attempted is not None:
+            stopped_after = repo.name
+        elif child.killed and _opened_this_sweep(config_path, since):
+            stopped_after = repo.name  # a killed child counts as a launch attempt
+    if first_unreached is None:
+        _write_rotation(base, (start + 1) % len(repos))
+    else:
+        _write_rotation(base, (start + first_unreached) % len(repos))
+    return SweepResult(
+        True,
+        children=tuple(children),
+        skipped=tuple(skipped),
+        stopped_after=stopped_after,
+        elapsed_s=round(monotonic() - began, 3),
+        generated=tuple(generated),
+    )
+
+
+__all__ = [
+    "CHILD_TIMEOUT_S",
+    "LOOP_CAP_S",
+    "ChildResult",
+    "Skipped",
+    "SweepResult",
+    "run_sweep",
+]
diff --git a/tests/issue_watch/test_dispatch.py b/tests/issue_watch/test_dispatch.py
new file mode 100644
index 000000000..8fd3f99e0
--- /dev/null
+++ b/tests/issue_watch/test_dispatch.py
@@ -0,0 +1,416 @@
+"""Task 23: the dispatcher core, over a fake runner and a fake clock.
+
+Every path is under ``tmp_path``; no real ``orca``, ``gh``, ``git`` or ``superclaude`` runs.
+"""
+
+from __future__ import annotations
+
+import json
+from datetime import timedelta
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_watch import cycle, defaults, dispatch, generate, record
+from superclaude.cli.issue_watch.generate import Base, Outcome
+
+from .conftest import CYCLE_NOW, FakeClock, result
+
+ORCA = "/opt/orca/bin/orca"
+SC = "/home/u/.local/bin/superclaude"
+DEFAULTS = defaults.Defaults()
+NAMES = ["Alpha", "Beta", "Gamma", "Delta"]
+
+
+def _path(name: str) -> str:
+    return f"/home/u/ws/{name}"
+
+
+class World:
+    """Orca, git and the children behind one runner; children can advance the clock."""
+
+    def __init__(self, tmp_path: Path, names, clock: FakeClock) -> None:
+        self.tmp, self.names, self.clock = tmp_path, list(names), clock
+        self.base = Base(tmp_path / "config", tmp_path / "state", tmp_path / "wt")
+        self.calls: list[tuple[tuple[str, ...], float]] = []
+        self.children: dict[str, object] = {}
+        self.listing_reply = None
+
+    # -- the files a generated config would have ------------------------------------------
+    def config(self, name: str, *, enabled: bool = True) -> Path:
+        directory = self.base.config_dir / dispatch.SUBDIR
+        directory.mkdir(parents=True, exist_ok=True)
+        approvers = directory / f"{name}-approvers.txt"
+        approvers.write_text("11\n")
+        approvers.chmod(0o600)
+        path = directory / f"{name}.json"
+        path.write_text(
+            json.dumps(
+                {
+                    "schema_version": 1,
+                    "enabled": enabled,
+                    "repo": f"IronbellyOrg/{name}",
+                    "project_id": "PVT_abc",
+                    "worktree": str(self.tmp / "wt" / name / "Coordinator"),
+                    "approvers_file": str(approvers),
+                    "state_dir": str(self.state_dir(name)),
+                }
+            )
+        )
+        path.chmod(0o600)
+        return path
+
+    def state_dir(self, name: str) -> Path:
+        return self.tmp / "state" / "issue-watch" / name
+
+    def child(
+        self,
+        name: str,
+        *,
+        stdout="cycle: cycle_complete\nexit: 0\n",
+        code=0,
+        seconds=1.0,
+        timed_out=False,
+    ):
+        def reply() -> object:
+            self.clock.advance(seconds)
+            return result(
+                stdout="" if timed_out else stdout, returncode=code, timed_out=timed_out
+            )
+
+        self.children[name] = reply
+
+    # -- the runner ------------------------------------------------------------------------
+    def run(self, argv, timeout, *, cwd=None):
+        key = tuple(argv)
+        self.calls.append((key, timeout))
+        if key == (ORCA, "repo", "list"):
+            if self.listing_reply is not None:
+                return self.listing_reply
+            lines = [
+                f"00000000-0000-4000-8000-{i:012d}  {n}  {_path(n)}"
+                for i, n in enumerate(self.names, 1)
+            ]
+            return result(stdout="\n".join(lines) + "\n")
+        if key[0] == "git":
+            name = key[2].rsplit("/", 1)[1]
+            return result(stdout=f"https://github.com/IronbellyOrg/{name}.git\n")
+        assert key[0] == SC and key[1:4] == ("issue-watch", "once", "--config"), key
+        name = Path(key[4]).stem
+        return self.children[name]()
+
+    def started(self) -> list[str]:
+        return [Path(k[4]).stem for k, _ in self.calls if k[0] == SC]
+
+
+@pytest.fixture
+def world(tmp_path):
+    return World(tmp_path, NAMES[:3], FakeClock(CYCLE_NOW))
+
+
+def sweep(w: World, **over) -> dispatch.SweepResult:
+    args = dict(
+        orca=ORCA,
+        superclaude=SC,
+        defaults=DEFAULTS,
+        base=w.base,
+        deps_factory=lambda cfg: pytest.fail("no first run expected"),
+        monotonic=w.clock.monotonic,
+        now=w.clock.now,
+    )
+    args.update(over)
+    return dispatch.run_sweep(w, **args)
+
+
+def prepare(w: World, names=None) -> None:
+    for name in names or w.names:
+        w.config(name)
+        w.child(name)
+
+
+def test_the_order_rotates_across_three_sweeps(world) -> None:
+    prepare(world)
+    orders = []
+    for _ in range(3):
+        before = len(world.started())
+        out = sweep(world)
+        assert out.ok and out.stopped_after is None and out.skipped == ()
+        orders.append(world.started()[before:])
+    assert orders == [
+        ["Alpha", "Beta", "Gamma"],
+        ["Beta", "Gamma", "Alpha"],
+        ["Gamma", "Alpha", "Beta"],
+    ]
+
+
+def test_the_loop_stops_after_the_first_launched_line(world) -> None:
+    prepare(world)
+    world.child("Alpha", stdout="cycle: cycle_complete\nexit: 0\nlaunched: 12\n")
+    out = sweep(world)
+    assert world.started() == ["Alpha"]
+    assert out.stopped_after == "Alpha"
+    assert [(c.name, c.launched, c.attempted) for c in out.children] == [
+        ("Alpha", 12, None)
+    ]
+    assert [(s.name, s.reason) for s in out.skipped] == [
+        ("Beta", "stopped_after_launch"),
+        ("Gamma", "stopped_after_launch"),
+    ]
+
+
+def test_the_loop_stops_after_an_attempted_line(world) -> None:
+    prepare(world)
+    world.child("Alpha")
+    world.child("Beta", stdout="cycle: launch_unknown\nexit: 7\nattempted: 5\n", code=7)
+    out = sweep(world)
+    assert world.started() == ["Alpha", "Beta"]
+    assert out.stopped_after == "Beta"
+    beta = out.children[1]
+    assert (beta.exit_code, beta.reason, beta.attempted) == (7, "launch_unknown", 5)
+    assert [(s.name, s.reason) for s in out.skipped] == [
+        ("Gamma", "stopped_after_launch")
+    ]
+
+
+def test_a_sweep_that_stopped_early_starts_the_next_one_where_it_stopped(world) -> None:
+    prepare(world)
+    world.child("Alpha", stdout="cycle: cycle_complete\nexit: 0\nlaunched: 3\n")
+    sweep(world)
+    world.child("Alpha")  # nothing is launched any more
+    before = len(world.started())
+    sweep(world)
+    assert world.started()[before:] == ["Beta", "Gamma", "Alpha"]
+
+
+def _pend(w: World, name: str, *, at) -> None:
+    state_dir = w.state_dir(name)
+    store = record.init_state(state_dir, CYCLE_NOW - timedelta(days=1))
+    ctx = record.PendingContext(
+        approver_id=11,
+        approval_event_id=77,
+        approved_at=CYCLE_NOW - timedelta(hours=1),
+        launch_cwd=str(w.tmp),
+        launch_login="owner-login",
+        launch_account_id=1001,
+    )
+    store.save(record.mark_pending(store.load(), 9, ctx, at))
+
+
+def test_a_child_killed_after_255_s_with_a_pending_entry_stops_the_loop(world) -> None:
+    prepare(world)
+    world.child("Alpha", seconds=255.0, timed_out=True)
+    _pend(
+        world, "Alpha", at=CYCLE_NOW + timedelta(seconds=10)
+    )  # created during this sweep
+    out = sweep(world)
+    assert world.started() == ["Alpha"]
+    alpha = out.children[0]
+    assert (alpha.killed, alpha.exit_code, alpha.reason) == (
+        True,
+        None,
+        "child_timeout",
+    )
+    assert out.stopped_after == "Alpha"
+    assert [s.name for s in out.skipped] == ["Beta", "Gamma"]
+    # every child got the 255 second kill time
+    assert {t for k, t in world.calls if k[0] == SC} == {dispatch.CHILD_TIMEOUT_S}
+    assert (
+        dispatch.CHILD_TIMEOUT_S == 255.0
+        and dispatch.CHILD_TIMEOUT_S > cycle.DEADLINE_TOTAL_S
+    )
+
+
+def test_the_same_kill_with_no_pending_entry_lets_the_later_repos_run(world) -> None:
+    prepare(world)
+    world.child("Alpha", seconds=255.0, timed_out=True)
+    record.init_state(world.state_dir("Alpha"), CYCLE_NOW - timedelta(days=1))
+    out = sweep(world)
+    assert world.started() == [
+        "Alpha",
+        "Beta",
+        "Gamma",
+    ]  # the timeout never kills the loop
+    assert out.stopped_after is None and out.children[0].killed is True
+
+
+def test_an_entry_from_before_this_sweep_does_not_stop_the_loop(world) -> None:
+    prepare(world)
+    world.child("Alpha", seconds=255.0, timed_out=True)
+    _pend(world, "Alpha", at=CYCLE_NOW - timedelta(hours=5))  # an old entry
+    out = sweep(world)
+    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.stopped_after is None
+
+
+def test_a_killed_child_with_an_unreadable_store_stops_the_loop(world) -> None:
+    prepare(world)
+    world.child("Alpha", seconds=255.0, timed_out=True)
+    world.state_dir("Alpha").mkdir(parents=True)
+    (world.state_dir("Alpha") / "dispatch.json").write_text("{not json")
+    out = sweep(world)
+    assert world.started() == ["Alpha"] and out.stopped_after == "Alpha"
+
+
+def test_the_270_second_cap_reports_the_repos_not_reached(tmp_path) -> None:
+    w = World(tmp_path, NAMES, FakeClock(CYCLE_NOW))
+    prepare(w)
+    for name in w.names:
+        w.child(name, seconds=100.0)
+    out = sweep(w)
+    # the order is by name (Alpha, Beta, Delta, Gamma); children start at 0, 100 and 200 s
+    assert w.started() == ["Alpha", "Beta", "Delta"]
+    assert [(s.name, s.reason) for s in out.skipped] == [("Gamma", "loop_cap")]
+    assert out.elapsed_s == 300.0 and dispatch.LOOP_CAP_S == 270.0
+    # the next sweep starts at the repo that was not reached
+    w.clock.advance(1)
+    for name in w.names:
+        w.child(name, seconds=1.0)
+    before = len(w.started())
+    sweep(w)
+    assert w.started()[before:][0] == "Gamma"
+
+
+def test_a_repo_with_no_config_is_generated_and_checked_before_it_runs(
+    world, monkeypatch
+) -> None:
+    world.config("Alpha")
+    world.config("Gamma")
+    for name in ("Alpha", "Beta", "Gamma"):
+        world.child(name)
+    order: list[str] = []
+
+    def fake_ensure(repo, defs, runner, base):
+        order.append(f"ensure:{repo.name}")
+        world.config(repo.name, enabled=False)
+        return Outcome("generated", repo.name, config_path=base.config_dir)
+
+    def fake_first_run(path, defs, runner, deps_factory):
+        order.append(f"first_run:{Path(path).stem}")
+        data = json.loads(Path(path).read_text())
+        data["enabled"] = True
+        Path(path).write_text(json.dumps(data))
+
+    monkeypatch.setattr(dispatch, "ensure_config", fake_ensure)
+    monkeypatch.setattr(dispatch, "first_run", fake_first_run)
+    out = sweep(world)
+    assert order == ["ensure:Beta", "first_run:Beta"]
+    assert out.generated == ("Beta",)
+    assert world.started() == ["Alpha", "Beta", "Gamma"]
+
+
+def test_a_repo_whose_generation_is_skipped_is_reported_not_run(
+    world, monkeypatch
+) -> None:
+    world.config("Alpha")
+    world.config("Gamma")
+    world.child("Alpha")
+    world.child("Gamma")
+    monkeypatch.setattr(
+        dispatch,
+        "ensure_config",
+        lambda repo, d, r, b: Outcome("skipped", repo.name, "no_project"),
+    )
+    out = sweep(world)
+    assert world.started() == ["Alpha", "Gamma"]
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "no_project")]
+
+
+def test_a_config_that_is_not_enabled_is_skipped_with_a_reason(world) -> None:
+    prepare(world)
+    world.config("Beta", enabled=False)
+    out = sweep(world)
+    assert world.started() == ["Alpha", "Gamma"]
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "not_enabled")]
+
+
+@pytest.mark.parametrize(
+    "reply",
+    [
+        result(stderr="boom", returncode=1),
+        result(timed_out=True),
+        result(spawn_error="FileNotFoundError"),
+        result(stdout="not a list\n"),
+    ],
+)
+def test_a_failed_orca_list_gives_an_error_result_not_a_clean_one(world, reply) -> None:
+    prepare(world)
+    world.listing_reply = reply
+    out = sweep(world)
+    assert out.ok is False and out.error in {
+        "list_failed",
+        "list_timeout",
+        "unreadable_list",
+    }
+    assert out.children == () and world.started() == []
+
+
+def test_an_empty_but_successful_list_is_a_clean_empty_sweep(world) -> None:
+    world.listing_reply = result(stdout="")
+    out = sweep(world)
+    assert out.ok is True and out.error is None and out.children == ()
+
+
+def test_each_childs_exit_code_and_reason_are_kept(world) -> None:
+    prepare(world)
+    world.child("Alpha", stdout="cycle: gh_auth_failed\nexit: 3\n", code=3, seconds=2.0)
+    world.child("Beta", stdout="cycle: cycle_complete\nexit: 0\n", seconds=3.0)
+    out = sweep(world)
+    assert [(c.name, c.exit_code, c.reason) for c in out.children] == [
+        ("Alpha", 3, "gh_auth_failed"),
+        ("Beta", 0, "cycle_complete"),
+        ("Gamma", 0, "cycle_complete"),
+    ]
+    assert [c.seconds for c in out.children][:2] == [2.0, 3.0]
+    # a failing child without a launch never stops the loop
+    assert out.stopped_after is None and world.started() == ["Alpha", "Beta", "Gamma"]
+
+
+def test_a_child_that_cannot_start_never_kills_the_loop(world) -> None:
+    prepare(world)
+    world.children["Alpha"] = lambda: result(spawn_error="FileNotFoundError")
+    out = sweep(world)
+    assert (out.children[0].reason, out.children[0].killed) == ("spawn_error", False)
+    assert world.started() == ["Alpha", "Beta", "Gamma"]
+
+
+def test_the_child_command_is_an_absolute_argv_with_the_config_path(world) -> None:
+    prepare(world)
+    sweep(world)
+    children = [k for k, _ in world.calls if k[0] == SC]
+    assert children[0] == (
+        SC,
+        "issue-watch",
+        "once",
+        "--config",
+        str(world.base.config_dir / dispatch.SUBDIR / "Alpha.json"),
+    )
+    assert all(Path(k[4]).is_absolute() for k in children)
+
+
+@pytest.mark.parametrize("orca,sc", [("orca", SC), (ORCA, "superclaude")])
+def test_relative_program_paths_are_refused_because_cron_has_no_path(
+    world, orca, sc
+) -> None:
+    with pytest.raises(ValueError):
+        sweep(world, orca=orca, superclaude=sc)
+    assert world.calls == []
+
+
+def test_the_rotation_file_is_private_and_a_broken_one_restarts_at_the_first_repo(
+    world,
+) -> None:
+    prepare(world)
+    sweep(world)
+    path = world.base.state_dir / "issue-watch" / dispatch.ROTATION_FILE
+    assert json.loads(path.read_text()) == {"next": 1}
+    assert oct(path.stat().st_mode & 0o777) == "0o600"
+    path.write_text("garbage")
+    before = len(world.started())
+    sweep(world)
+    assert world.started()[before:][0] == "Alpha"
+
+
+def test_nothing_is_written_outside_tmp_path(world, tmp_path) -> None:
+    prepare(world)
+    sweep(world)
+    assert not (tmp_path / "home").exists()
+    assert generate.Base.default().config_dir.expanduser() != world.base.config_dir

Task 23 context. dispatch.py is new; it is the sweep logic only (the cron command and the report are Tasks 24 and 25). It sorts usable repos by name, rotates the start index kept in `<state dir>/issue-watch/rotation.json`, skips a repo whose config is not enabled (reported as not_enabled), and reads a killed child repo store through record.py only. A killed child stops the loop unless its store shows no pending/launched/unknown entry with pending_at at or after the sweep start; an unreadable store counts as open. The module-boundaries table gained a "dispatch" row. Tests run: tests/issue_watch passed; ruff clean; make verify-sync clean.

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
