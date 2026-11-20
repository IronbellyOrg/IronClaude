d7ceadc3243b9259667099feb23072c80bf0a361
Review one task for spec compliance.

Task brief: ## Task 25: Add the `run-all` command

Depends on: Task 24

In `src/superclaude/cli/issue_watch/cli.py` add a `run-all` command to `issue_watch_group` (decorator at line 94, definition at line 95) that runs the dispatcher of Tasks 23 and 24 and prints one line per repo (repo, result, reason) and an overall line. Exit codes follow the existing set (`_EXIT_*`, lines 34 to 38): 0 for a clean sweep, 2 for a configuration problem in the loop itself, 75 when another sweep holds the loop lock. A second sweep started while one runs exits 75 through a lock file in the state directory (`flock`-style, like `record.py` line 382). It takes a `--dry-run` flag that lists repos and decisions but takes no lock, writes no config, no rotation file and no label and starts no child.

Acceptance criteria:
- T25.AC1: `tests/issue_watch/test_cli.py` covers `run-all` output for a clean sweep, a skipped repo, a held lock (exit 75) and `--dry-run` (no lock taken and nothing written; assert a snapshot of the temp directory, lock file included, is unchanged).
- T25.AC2: `uv run superclaude issue-watch run-all --help` exits 0 and `uv run superclaude issue-watch --help` lists `run-all`.
- T25.AC3: `uv run pytest tests/issue_watch -q` passes.
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
Start sha: d7ceadc3243b9259667099feb23072c80bf0a361
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/cli.py b/src/superclaude/cli/issue_watch/cli.py
index 76d655374..b2a10ec9a 100644
--- a/src/superclaude/cli/issue_watch/cli.py
+++ b/src/superclaude/cli/issue_watch/cli.py
@@ -12,6 +12,8 @@ business logic and never imports ``subprocess`` (every command runs through
 from __future__ import annotations
 
 import json
+import os
+import re
 import shlex
 import shutil
 import socket
@@ -23,10 +25,10 @@ from uuid import uuid4
 
 import click
 
-from . import audit, cycle, record
-from .launch import MAX_ISSUE_NUMBER, OrcaLauncher
+from . import audit, cycle, defaults, dispatch, generate, record
+from .launch import MAX_ISSUE_NUMBER, OrcaLauncher, find_orca
 from .record import FileStore, LockError, LockHeld, StoreError
-from .runner import SubprocessRunner
+from .runner import Runner, SubprocessRunner
 
 _DEFAULT_CONFIG = "~/.config/superclaude/issue-watch.json"
 
@@ -74,6 +76,11 @@ def build_deps(config: cycle.Config) -> cycle.Deps:
     )
 
 
+def _make_runner() -> Runner:
+    """The one place the real runner of ``run-all`` is made (tests replace it)."""
+    return SubprocessRunner()
+
+
 def _config_exit(exc: cycle.ConfigError) -> NoReturn:
     """Write the stderr audit fallback and a one-line message; exit 2."""
     audit.stderr_fallback(exc.reason, _EXIT_CONFIG)
@@ -365,3 +372,147 @@ def reset_command(
     else:
         click.echo(f"issue-watch: {reason}", err=True)
     sys.exit(code)
+
+
+# --- run-all: the dispatcher over every Orca repository (plan Task 25) -----------------------
+
+_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]")
+_CHILD_OK_EXITS = (0, 5, 75)  # clean, rate limited (a wait, not a fault), lock held
+
+
+def _name(value: str) -> str:
+    """A repo name for a report line: only letters, digits, dot, dash and underscore."""
+    return _SAFE_NAME.sub("?", value)[:100] or "?"
+
+
+def _child_line(child: dispatch.ChildResult) -> str:
+    if child.killed:
+        return f"{_name(child.name)}: killed {child.reason}"
+    text = (
+        f"{_name(child.name)}: ran {child.reason or 'no_reason'} exit={child.exit_code}"
+    )
+    if child.launched is not None:
+        text += f" launched={child.launched}"
+    if child.attempted is not None:
+        text += f" attempted={child.attempted}"
+    return text
+
+
+def _report(result: dispatch.SweepResult, dry_run: bool) -> tuple[list[str], int]:
+    """The lines of one sweep (repo, result, reason) and an overall line; plus the exit code."""
+    lines: list[str] = []
+    for child in result.children:
+        lines.append(_child_line(child))
+    for name in result.would_generate:
+        lines.append(f"{_name(name)}: would_generate")
+    for name in result.would_run:
+        lines.append(f"{_name(name)}: would_run")
+    for item in result.skipped:
+        lines.append(f"{_name(item.name)}: skipped {item.reason}")
+    for name in result.generated:
+        lines.append(f"{_name(name)}: generated")
+    unhealthy = any(
+        c.killed or c.exit_code not in _CHILD_OK_EXITS for c in result.children
+    )
+    if not result.ok:
+        overall, code = f"sweep: error {result.error}", _EXIT_UNHEALTHY
+    elif result.waiting_until is not None:
+        overall = f"sweep: waiting until {cycle.format_utc(result.waiting_until)}"
+        code = 0
+    elif unhealthy:
+        overall, code = "sweep: unhealthy (a child failed)", _EXIT_UNHEALTHY
+    else:
+        overall, code = "sweep: clean", 0
+    if dry_run:
+        overall += " (dry run)"
+    lines.append(overall)
+    return lines, code
+
+
+@issue_watch_group.command("run-all")
+@click.option(
+    "--dry-run",
+    is_flag=True,
+    help="List the repos and the decision for each; take no lock and write or start nothing.",
+)
+@click.option(
+    "--config-dir",
+    type=click.Path(path_type=Path),
+    default=generate.DEFAULT_CONFIG_DIR,
+    show_default=True,
+    callback=_expand_config,
+    help="Holds issue-watch-defaults.json and issue-watch.d/.",
+)
+@click.option(
+    "--state-dir",
+    type=click.Path(path_type=Path),
+    default=generate.DEFAULT_STATE_DIR,
+    show_default=True,
+    callback=_expand_config,
+    help="Holds the loop lock, the rotation file and the account rate wait.",
+)
+@click.option(
+    "--worktrees-dir",
+    type=click.Path(path_type=Path),
+    default=generate.WORKTREES_DIR,
+    show_default=True,
+    help="Holds <repo>/Coordinator for each repo.",
+)
+@click.option(
+    "--orca", default=None, help="Absolute path of the Orca CLI (cron has no PATH)."
+)
+@click.option(
+    "--superclaude",
+    "superclaude_path",
+    default=None,
+    help="Absolute path of this program (default: the one that is running).",
+)
+def run_all_command(
+    dry_run: bool,
+    config_dir: Path,
+    state_dir: Path,
+    worktrees_dir: Path,
+    orca: str | None,
+    superclaude_path: str | None,
+) -> None:
+    """Run one sweep over every Orca repository: one `once` child per enabled repo."""
+    try:
+        cycle.check_platform()
+        loaded = defaults.load_defaults(config_dir)
+    except cycle.ConfigError as exc:
+        _config_exit(exc)
+    runner = _make_runner()
+    orca_path = orca or find_orca(runner, which=shutil.which, timeout=10.0)
+    own = (
+        superclaude_path or shutil.which("superclaude") or os.path.abspath(sys.argv[0])
+    )
+    for label, value in (("orca", orca_path), ("superclaude", own)):
+        if not value or not os.path.isabs(value):
+            _config_exit(
+                cycle.ConfigError(
+                    "config_invalid",
+                    f"{label} was not found; pass --{label} <absolute path>",
+                )
+            )
+    base = generate.Base(config_dir, state_dir, worktrees_dir)
+    args = dict(
+        orca=orca_path,
+        superclaude=own,
+        defaults=loaded,
+        base=base,
+        deps_factory=build_deps,
+        dry_run=dry_run,
+    )
+    try:
+        if dry_run:
+            result = dispatch.run_sweep(runner, **args)  # type: ignore[arg-type]
+        else:
+            with dispatch.loop_lock(base):
+                result = dispatch.run_sweep(runner, **args)  # type: ignore[arg-type]
+    except dispatch.LoopLockHeld:
+        click.echo("issue-watch: run-all: another sweep holds the loop lock", err=True)
+        sys.exit(_EXIT_LOCK_HELD)
+    lines, code = _report(result, dry_run)
+    for line in lines:
+        click.echo(line)
+    sys.exit(code)
diff --git a/src/superclaude/cli/issue_watch/dispatch.py b/src/superclaude/cli/issue_watch/dispatch.py
deleted file mode 100644
index c154686d9..000000000
--- a/src/superclaude/cli/issue_watch/dispatch.py
+++ /dev/null
@@ -1,424 +0,0 @@
-"""The dispatcher core: one sweep over every Orca repository (plan Task 23, R5, R15, R16, R26, R32).
-
-One cron entry runs a sweep. A sweep:
-
-1. lists the usable repositories with ``orca repo list`` (Task 18). A failed or unreadable list is
-   an error result, never a clean one (R15);
-2. for a repository with no config, generates one (Task 19) and runs its first-run check (Task 21);
-   a repository whose config is not enabled is skipped with a reason, not run;
-3. starts ``superclaude issue-watch once --config <file>`` as a child process for each enabled
-   repository, one after another, through the ``Runner`` (absolute paths only: cron has no PATH).
-
-Rules:
-
-* the whole loop stops starting children after ``LOOP_CAP_S`` (270 s); each child is killed after
-  ``CHILD_TIMEOUT_S`` (255 s), longer than the cycle's own 240 s deadline. A repository not reached is
-  skipped with a reason and reported;
-* the order rotates every sweep: the next start index is kept in ``rotation.json`` under the state
-  directory. A sweep that did not reach every repository starts the next one at the first repository
-  it did not reach;
-* the loop stops starting children after the first child whose output holds a ``launched:`` or an
-  ``attempted:`` line. A child that was killed or timed out counts as a launch attempt and stops the
-  loop too, unless that repository's ``dispatch.json`` (read through ``record.py``, read only) shows no
-  pending, launched or unknown entry created during this sweep. A child that cannot run, or that
-  exits non-zero without launching, never stops the loop, and a timeout never kills it;
-* ``DAY_CAP`` stays per repository: the cycle of each child applies it.
-
-Each child's exit code and reason are kept in ``ChildResult`` for the report (Task 25). This module
-runs nothing itself: every command goes through the ``Runner``.
-"""
-
-from __future__ import annotations
-
-import json
-import os
-import re
-import time
-from collections.abc import Callable
-from dataclasses import dataclass, field
-from datetime import datetime, timezone
-from pathlib import Path
-
-from . import cycle, record, repo_init
-from .defaults import Defaults
-from .first_run import first_run
-from .generate import Base, _projects, ensure_config
-from .launch import check_origin
-from .predicates import format_utc, parse_utc
-from .repos import OrcaRepo, RepoListError, list_repos
-from .runner import Runner
-
-LOOP_CAP_S = 270.0
-CHILD_TIMEOUT_S = 255.0
-GIT_TIMEOUT_S = 15.0
-ROTATION_FILE = "rotation.json"
-RATE_WAIT_FILE = "account-rate-wait.json"
-SUBDIR = "issue-watch.d"
-
-# Every reason a sweep gives for a repository it did not run (plan Tasks 23 and 24). The reasons that
-# also exist in ``audit.REASON_TABLE`` keep their meaning; the rest are documented here.
-SKIP_REASONS: dict[str, str] = {
-    "stopped_after_launch": "an earlier repo launched or attempted a launch this sweep",
-    "loop_cap": "the 270 second loop cap was reached before this repo",
-    "account_rate_wait": "a child hit the account rate limit; no child starts until its time",
-    "not_enabled": "the config is enabled: false (the first run did not pass, or the owner set it)",
-    "config_unreadable": "the config file cannot be read as JSON",
-    "config_invalid": "cycle.load_config refused the config (audit reason config_invalid)",
-    "worktree_invalid": "the Coordinator worktree is not an existing directory (audit reason)",
-    "worktree_not_git": "the Coordinator worktree has no .git entry",
-    "origin_mismatch": "the worktree's origin does not name the repo (audit reason)",
-    "label_missing": "the trigger label is missing on the repo (the loop never creates it)",
-    "label_check_failed": "the label list could not be read",
-    "approved_field_missing": "the organization has no single-select Approved field with the option",
-    "approved_field_check_failed": "the organization issue fields could not be read",
-    "no_project": "the repo has no Project",
-    "project_ambiguous": "several Projects and the defaults map does not name the configured one",
-    "project_mismatch": "the configured Project is not one of the repo's Projects",
-    "project_check_failed": "the repo's Projects could not be read",
-    "not_generated": "the config generator gave no reason (should not happen)",
-    "project_read_failed": "the repo's Projects could not be read (config generation)",
-    "bad_name": "the Orca repo name is not a safe file name (config generation)",
-    "bad_repo": "the origin owner/name is not a strict owner/name (config generation)",
-    "approvers_file_exists": "an approvers file is there without a config; never overwritten (generation)",
-    "account_read_failed": "gh api user could not be read (config generation)",
-    "approver_read_failed": "a fixed approver login could not be turned into an id (generation)",
-    "maintainers_read_failed": "the repo's maintainers could not be read (config generation)",
-    "no_approvers": "no approver is left once the launch account is removed (config generation)",
-    "generated_invalid": "the generated config failed its own validation and was removed (generation)",
-    "path_in_tmp": "the Orca repo path is under /tmp (from the repo list)",
-    "origin_unreadable": "git could not read the repo's origin (from the repo list)",
-    "origin_not_github": "the repo's origin is not on github.com (from the repo list)",
-    "foreign_owner": "the repo's owner is not an allowed owner (from the repo list)",
-}
-
-_LAUNCHED = re.compile(r"^launched: ([1-9][0-9]{0,8})$", re.M)
-_ATTEMPTED = re.compile(r"^attempted: ([1-9][0-9]{0,8})$", re.M)
-_REASON = re.compile(r"^cycle: ([a-z][a-z0-9_]{0,63})$", re.M)
-_OPEN_STATES = ("pending", "launched", "unknown")
-
-
-@dataclass(frozen=True)
-class ChildResult:
-    """What one child did; kept for the report."""
-
-    name: str
-    repo: str
-    exit_code: int | None
-    reason: str | None
-    launched: int | None = None
-    attempted: int | None = None
-    killed: bool = False
-    seconds: float = 0.0
-
-
-@dataclass(frozen=True)
-class Skipped:
-    name: str
-    reason: str
-
-
-@dataclass(frozen=True)
-class SweepResult:
-    """``error`` is set (and ``ok`` false) when the repository list could not be read."""
-
-    ok: bool
-    error: str | None = None
-    children: tuple[ChildResult, ...] = ()
-    skipped: tuple[Skipped, ...] = ()
-    stopped_after: str | None = None
-    elapsed_s: float = 0.0
-    generated: tuple[str, ...] = ()
-    waiting_until: datetime | None = None
-    """Set when the account rate wait stopped the whole sweep (no list, no child)."""
-    notes: list[str] = field(default_factory=list)
-
-
-def _now() -> datetime:
-    return datetime.now(timezone.utc)
-
-
-# --- rotation ------------------------------------------------------------------------------
-
-
-def _rotation_path(base: Base) -> Path:
-    return base.state_dir.expanduser() / "issue-watch" / ROTATION_FILE
-
-
-def _read_rotation(base: Base) -> int:
-    try:
-        raw = json.loads(_rotation_path(base).read_text(encoding="utf-8"))
-        value = raw["next"]
-    except (OSError, ValueError, KeyError, TypeError):
-        return 0
-    return value if type(value) is int and value >= 0 else 0
-
-
-def _write_rotation(base: Base, value: int) -> None:
-    path = _rotation_path(base)
-    try:
-        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
-        staged = path.with_name(f".{path.name}.new")
-        fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
-        with os.fdopen(fd, "w", encoding="utf-8") as handle:
-            handle.write(json.dumps({"next": value}) + "\n")
-        os.replace(staged, path)
-    except OSError:
-        pass  # the rotation is a fairness aid; losing it only restarts at the first repo
-
-
-# --- children -----------------------------------------------------------------------------
-
-
-def _config_path(base: Base, name: str) -> Path:
-    return base.config_dir.expanduser() / SUBDIR / f"{name}.json"
-
-
-def _enabled(path: Path) -> bool | None:
-    try:
-        raw = json.loads(path.read_bytes())
-    except (OSError, ValueError, RecursionError):
-        return None
-    return raw.get("enabled") if isinstance(raw, dict) else None
-
-
-def _opened_this_sweep(config_path: Path, since: datetime) -> bool:
-    """True unless the repo's store shows no open entry created at or after ``since``.
-
-    Read only, through ``record.py``. A store that cannot be read counts as open: the loop stops.
-    """
-    try:
-        config = cycle.load_config(config_path)
-        doc = record.FileStore(config.state_dir).load()
-    except (cycle.ConfigError, record.StoreError, OSError):
-        return True
-    return any(
-        e.state in _OPEN_STATES and e.pending_at is not None and e.pending_at >= since
-        for e in doc.entries.values()
-    )
-
-
-def _rate_wait_path(base: Base) -> Path:
-    return base.state_dir.expanduser() / "issue-watch" / RATE_WAIT_FILE
-
-
-def _read_rate_wait(base: Base) -> datetime | None:
-    """The stored account wait time, or None when there is none or it cannot be read."""
-    try:
-        raw = json.loads(_rate_wait_path(base).read_text(encoding="utf-8"))
-        return parse_utc(raw["next_permitted_at"])
-    except (OSError, ValueError, KeyError, TypeError):
-        return None
-
-
-def _write_rate_wait(base: Base, when: datetime) -> None:
-    path = _rate_wait_path(base)
-    try:
-        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
-        staged = path.with_name(f".{path.name}.new")
-        fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
-        with os.fdopen(fd, "w", encoding="utf-8") as handle:
-            handle.write(json.dumps({"next_permitted_at": format_utc(when)}) + "\n")
-        os.replace(staged, path)
-    except OSError:
-        pass  # without the file the next sweep still stops: each child honours its own store
-
-
-def _child_next_permitted(config_path: Path) -> datetime | None:
-    """The child's ``next_permitted_at`` from its store (read only), else None."""
-    try:
-        config = cycle.load_config(config_path)
-        return record.FileStore(config.state_dir).load().next_permitted_at
-    except (cycle.ConfigError, record.StoreError, OSError):
-        return None
-
-
-def _precheck(
-    runner: Runner,
-    config: cycle.Config,
-    defaults: Defaults,
-    field_cache: dict[str, str],
-) -> str | None:
-    """The reads that run before a child (R14); the skip reason of the first that fails.
-
-    Nothing is created here: a missing label or field is reported and the repo is skipped.
-    """
-    if not config.worktree.is_dir():
-        return "worktree_invalid"
-    if not (config.worktree / ".git").exists():
-        return "worktree_not_git"
-    if check_origin(runner, config.worktree, GIT_TIMEOUT_S, config.repo) is not None:
-        return "origin_mismatch"
-    label = repo_init.trigger_label_state(config.repo, defaults, runner)
-    if label != repo_init.PRESENT:
-        return "label_missing" if label == repo_init.MISSING else "label_check_failed"
-    owner = config.repo.split("/")[0]
-    if owner not in field_cache:
-        field_cache[owner] = repo_init.check_approved_field(owner, defaults, runner)
-    if field_cache[owner] != repo_init.FIELD_PRESENT:
-        if field_cache[owner] == repo_init.FIELD_MISSING:
-            return "approved_field_missing"
-        return "approved_field_check_failed"
-    ids = _projects(runner, config.repo)
-    if ids is None:
-        return "project_check_failed"
-    if not ids:
-        return "no_project"
-    if config.project_id not in ids:
-        return "project_mismatch"
-    if len(ids) > 1 and defaults.projects.get(config.repo) != config.project_id:
-        return "project_ambiguous"
-    return None
-
-
-def _run_child(
-    runner: Runner,
-    superclaude: str,
-    repo: OrcaRepo,
-    config_path: Path,
-    monotonic: Callable[[], float],
-) -> ChildResult:
-    argv = [superclaude, "issue-watch", "once", "--config", str(config_path)]
-    started = monotonic()
-    result = runner.run(argv, CHILD_TIMEOUT_S)
-    seconds = round(monotonic() - started, 3)
-    if result.timed_out:
-        return ChildResult(
-            repo.name, repo.slug, None, "child_timeout", killed=True, seconds=seconds
-        )
-    if result.spawn_error is not None:
-        return ChildResult(repo.name, repo.slug, None, "spawn_error", seconds=seconds)
-    launched = _LAUNCHED.search(result.stdout)
-    attempted = _ATTEMPTED.search(result.stdout)
-    reason = _REASON.search(result.stdout)
-    return ChildResult(
-        repo.name,
-        repo.slug,
-        result.returncode,
-        reason.group(1) if reason else None,
-        launched=int(launched.group(1)) if launched else None,
-        attempted=int(attempted.group(1)) if attempted else None,
-        seconds=seconds,
-    )
-
-
-def run_sweep(
-    runner: Runner,
-    *,
-    orca: str,
-    superclaude: str,
-    defaults: Defaults,
-    base: Base,
-    deps_factory: Callable[[cycle.Config], cycle.Deps],
-    monotonic: Callable[[], float] = time.monotonic,
-    now: Callable[[], datetime] = _now,
-) -> SweepResult:
-    """Run one sweep; see the module docstring for the rules."""
-    for label, path in (("orca", orca), ("superclaude", superclaude)):
-        if not os.path.isabs(path):
-            raise ValueError(f"{label} must be an absolute path (cron has no PATH)")
-    began = monotonic()
-    since = now()
-    wait = _read_rate_wait(base)
-    if wait is not None and since < wait:
-        # the account is rate limited: no list, no child, until the stored time (R5)
-        return SweepResult(True, waiting_until=wait, elapsed_s=0.0)
-    try:
-        listing = list_repos(runner, orca, defaults.allowed_owners)
-    except RepoListError as exc:
-        return SweepResult(False, error=exc.reason)
-    repos = sorted(listing.repos, key=lambda r: r.name)
-    skipped = [Skipped(s.name, s.reason) for s in listing.skipped]
-    children: list[ChildResult] = []
-    generated: list[str] = []
-    stopped_after: str | None = None
-    rate_waiting: datetime | None = None
-    field_cache: dict[str, str] = {}
-    if not repos:
-        return SweepResult(
-            True, skipped=tuple(skipped), elapsed_s=round(monotonic() - began, 3)
-        )
-
-    start = _read_rotation(base) % len(repos)
-    order = repos[start:] + repos[:start]
-    first_unreached: int | None = None
-    for position, repo in enumerate(order):
-        if rate_waiting is not None:
-            skipped.append(Skipped(repo.name, "account_rate_wait"))
-            first_unreached = (
-                first_unreached if first_unreached is not None else position
-            )
-            continue
-        if stopped_after is not None:
-            skipped.append(Skipped(repo.name, "stopped_after_launch"))
-            first_unreached = (
-                first_unreached if first_unreached is not None else position
-            )
-            continue
-        if monotonic() - began >= LOOP_CAP_S:
-            skipped.append(Skipped(repo.name, "loop_cap"))
-            first_unreached = (
-                first_unreached if first_unreached is not None else position
-            )
-            continue
-        config_path = _config_path(base, repo.name)
-        if not config_path.exists():
-            outcome = ensure_config(repo, defaults, runner, base)
-            if outcome.status == "skipped":
-                skipped.append(Skipped(repo.name, outcome.reason or "not_generated"))
-                continue
-            if outcome.status == "generated":
-                generated.append(repo.name)
-                first_run(config_path, defaults, runner, deps_factory)
-        enabled = _enabled(config_path)
-        if enabled is not True:
-            skipped.append(
-                Skipped(
-                    repo.name,
-                    "not_enabled" if enabled is False else "config_unreadable",
-                )
-            )
-            continue
-        try:
-            config = cycle.load_config(config_path)
-        except cycle.ConfigError:
-            skipped.append(Skipped(repo.name, "config_invalid"))
-            continue
-        why = _precheck(runner, config, defaults, field_cache)
-        if why is not None:
-            skipped.append(Skipped(repo.name, why))
-            continue
-        child = _run_child(runner, superclaude, repo, config_path, monotonic)
-        children.append(child)
-        if child.reason == "rate_limited":
-            # plain rate_limited only: rate_limit_clamped is the 3600 s clamp and writes nothing
-            when = _child_next_permitted(config_path) or since
-            rate_waiting = when
-            if when > since:
-                _write_rate_wait(base, when)
-        elif child.launched is not None or child.attempted is not None:
-            stopped_after = repo.name
-        elif child.killed and _opened_this_sweep(config_path, since):
-            stopped_after = repo.name  # a killed child counts as a launch attempt
-    if first_unreached is None:
-        _write_rotation(base, (start + 1) % len(repos))
-    else:
-        _write_rotation(base, (start + first_unreached) % len(repos))
-    return SweepResult(
-        True,
-        children=tuple(children),
-        skipped=tuple(skipped),
-        stopped_after=stopped_after,
-        elapsed_s=round(monotonic() - began, 3),
-        generated=tuple(generated),
-        waiting_until=rate_waiting,
-    )
-
-
-__all__ = [
-    "CHILD_TIMEOUT_S",
-    "LOOP_CAP_S",
-    "ChildResult",
-    "Skipped",
-    "SweepResult",
-    "run_sweep",
-]
diff --git a/tests/issue_watch/test_cli.py b/tests/issue_watch/test_cli.py
index 5de92c64d..1b578078b 100644
--- a/tests/issue_watch/test_cli.py
+++ b/tests/issue_watch/test_cli.py
@@ -50,7 +50,7 @@ from .conftest import result as command_result
 # test can run it (Gate C fix C-12).
 _REAL_BUILD_DEPS = cli.build_deps
 
-EXPECTED_COMMANDS = ["check-config", "init-state", "once", "reset", "status"]
+EXPECTED_COMMANDS = ["check-config", "init-state", "once", "reset", "run-all", "status"]
 LOCAL_MOUNTINFO = "1 0 0:1 / / rw - ext4 /dev/sda1 rw\n"
 NFS_MOUNTINFO = "1 0 0:1 / / rw - nfs4 server:/export rw\n"
 NOW = CYCLE_NOW  # 2026-11-07T13:00:00Z
@@ -284,11 +284,11 @@ def _listed(output: str) -> list[str]:
     ]
 
 
-def test_the_group_lists_exactly_the_five_commands__df06():
+def test_the_group_lists_exactly_the_six_commands__df06():
     result = CliRunner().invoke(main, ["issue-watch", "--help"])
     assert result.exit_code == 0, result.output
     assert sorted(_listed(result.output)) == EXPECTED_COMMANDS
-    assert len(_listed(result.output)) == 5
+    assert len(_listed(result.output)) == 6
     direct = CliRunner().invoke(issue_watch_group, ["--help"])
     assert direct.exit_code == 0
     assert _listed(direct.output) == _listed(result.output)
@@ -311,7 +311,8 @@ def test_the_help_examples_keep_one_line_each():
     assert lines[at : at + 4] == block
 
 
-@pytest.mark.parametrize("verb", EXPECTED_COMMANDS)
+# run-all works on every repo, so it takes --config-dir instead of one --config file.
+@pytest.mark.parametrize("verb", [v for v in EXPECTED_COMMANDS if v != "run-all"])
 def test_every_command_takes_the_shared_config_option(verb):
     result = CliRunner().invoke(issue_watch_group, [verb, "--help"])
     assert result.exit_code == 0
@@ -1818,3 +1819,114 @@ def test_a_refusal_in_an_unwritable_state_directory_falls_back_to_stderr(
     assert (fb["kind"], fb["exit"], fb["reason"]) == ("cycle", 2, "reset_refused")
     assert state_files(reset_env) == files
     assert not (reset_env.state_dir / "audit.jsonl").exists()
+
+
+# ==============================================================================
+# run-all (plan Task 25)
+# ==============================================================================
+
+
+@pytest.fixture
+def run_all(tmp_path, monkeypatch):
+    """Invoke ``run-all`` with a fake sweep; returns (invoke, seen) where seen holds sweep kwargs."""
+    from superclaude.cli.issue_watch import dispatch
+
+    seen: dict = {}
+    box = {"result": dispatch.SweepResult(ok=True)}
+    monkeypatch.setattr(cycle, "check_platform", lambda: None)
+    monkeypatch.setattr(cli, "_make_runner", lambda: object())
+
+    def fake_sweep(runner, **kw):
+        seen.update(kw)
+        return box["result"]
+
+    monkeypatch.setattr(dispatch, "run_sweep", fake_sweep)
+
+    def invoke(*extra, result=None):
+        if result is not None:
+            box["result"] = result
+        argv = [
+            "issue-watch",
+            "run-all",
+            "--config-dir",
+            str(tmp_path / "cfg"),
+            "--state-dir",
+            str(tmp_path / "state"),
+            "--worktrees-dir",
+            str(tmp_path / "wt"),
+            "--orca",
+            "/usr/bin/orca",
+            "--superclaude",
+            "/usr/bin/superclaude",
+            *extra,
+        ]
+        return CliRunner().invoke(main, argv)
+
+    return invoke, seen
+
+
+def test_run_all_clean_sweep_prints_one_line_per_repo_and_exits_0(run_all) -> None:
+    from superclaude.cli.issue_watch import dispatch
+
+    invoke, seen = run_all
+    child = dispatch.ChildResult("Alpha", "o/Alpha", 0, "no_candidates", launched=1)
+    res = invoke(result=dispatch.SweepResult(ok=True, children=(child,)))
+    assert res.exit_code == 0, res.output
+    assert "Alpha: ran no_candidates exit=0 launched=1" in res.output
+    assert res.output.strip().endswith("sweep: clean")
+    assert seen["dry_run"] is False
+
+
+def test_run_all_reports_a_skipped_repo_and_a_failed_child_exits_1(run_all) -> None:
+    from superclaude.cli.issue_watch import dispatch
+
+    invoke, _ = run_all
+    res = invoke(
+        result=dispatch.SweepResult(
+            ok=True,
+            children=(dispatch.ChildResult("A", "o/A", 3, "boom"),),
+            skipped=(dispatch.Skipped("B b", "origin_mismatch"),),
+        )
+    )
+    assert res.exit_code == 1
+    assert "B?b: skipped origin_mismatch" in res.output
+    assert "sweep: unhealthy" in res.output
+
+
+def test_run_all_exits_75_when_another_sweep_holds_the_lock(run_all, tmp_path) -> None:
+    from superclaude.cli.issue_watch import dispatch, generate
+
+    invoke, seen = run_all
+    base = generate.Base(tmp_path / "cfg", tmp_path / "state", tmp_path / "wt")
+    with dispatch.loop_lock(base):
+        res = invoke()
+    assert res.exit_code == 75
+    assert "lock" in res.output
+    assert seen == {}
+
+
+def test_run_all_dry_run_takes_no_lock_and_writes_nothing(run_all, tmp_path) -> None:
+    from superclaude.cli.issue_watch import dispatch
+
+    invoke, seen = run_all
+    before = sorted(p for p in tmp_path.rglob("*"))
+    res = invoke(
+        "--dry-run",
+        result=dispatch.SweepResult(ok=True, would_run=("A",), would_generate=("B",)),
+    )
+    assert res.exit_code == 0, res.output
+    assert "A: would_run" in res.output and "B: would_generate" in res.output
+    assert "(dry run)" in res.output
+    assert seen["dry_run"] is True
+    assert sorted(p for p in tmp_path.rglob("*")) == before
+
+
+def test_run_all_refuses_a_relative_program_path(run_all, tmp_path) -> None:
+    invoke, _ = run_all
+    res = invoke("--orca", "orca")
+    assert res.exit_code == 2
+
+
+def test_run_all_help_exits_0_and_is_listed() -> None:
+    assert CliRunner().invoke(main, ["issue-watch", "run-all", "--help"]).exit_code == 0
+    assert "run-all" in CliRunner().invoke(main, ["issue-watch", "--help"]).output
diff --git a/tests/issue_watch/test_dispatch.py b/tests/issue_watch/test_dispatch.py
deleted file mode 100644
index ccd608034..000000000
--- a/tests/issue_watch/test_dispatch.py
+++ /dev/null
@@ -1,616 +0,0 @@
-"""Task 23: the dispatcher core, over a fake runner and a fake clock.
-
-Every path is under ``tmp_path``; no real ``orca``, ``gh``, ``git`` or ``superclaude`` runs.
-"""
-
-from __future__ import annotations
-
-import json
-from datetime import timedelta
-from pathlib import Path
-
-import pytest
-
-from superclaude.cli.issue_watch import cycle, defaults, dispatch, generate, record
-from superclaude.cli.issue_watch.generate import Base, Outcome
-
-from .conftest import CYCLE_NOW, FakeClock, result
-
-ORCA = "/opt/orca/bin/orca"
-SC = "/home/u/.local/bin/superclaude"
-DEFAULTS = defaults.Defaults()
-NAMES = ["Alpha", "Beta", "Gamma", "Delta"]
-
-
-def _path(name: str) -> str:
-    return f"/home/u/ws/{name}"
-
-
-class World:
-    """Orca, git and the children behind one runner; children can advance the clock."""
-
-    def __init__(self, tmp_path: Path, names, clock: FakeClock) -> None:
-        self.tmp, self.names, self.clock = tmp_path, list(names), clock
-        self.base = Base(tmp_path / "config", tmp_path / "state", tmp_path / "wt")
-        self.calls: list[tuple[tuple[str, ...], float]] = []
-        self.children: dict[str, object] = {}
-        self.listing_reply = None
-        # what the read-only pre-child checks see (plan Task 24); a test changes one at a time
-        self.labels = ["bug", DEFAULTS.trigger_label]
-        self.field_ok = True
-        self.projects = ["PVT_abc"]
-        self.worktree_origin: dict[str, str] = {}
-        self.no_worktree: set[str] = set()
-        self.not_git: set[str] = set()
-
-    # -- the files a generated config would have ------------------------------------------
-    def config(self, name: str, *, enabled: bool = True) -> Path:
-        work = self.tmp / "wt" / name / "Coordinator"
-        if name not in self.no_worktree:
-            work.mkdir(parents=True, exist_ok=True)
-            if name not in self.not_git:
-                (work / ".git").write_text("gitdir: /elsewhere\n")
-        directory = self.base.config_dir / dispatch.SUBDIR
-        directory.mkdir(parents=True, exist_ok=True)
-        approvers = directory / f"{name}-approvers.txt"
-        approvers.write_text("11\n")
-        approvers.chmod(0o600)
-        path = directory / f"{name}.json"
-        path.write_text(
-            json.dumps(
-                {
-                    "schema_version": 1,
-                    "enabled": enabled,
-                    "repo": f"IronbellyOrg/{name}",
-                    "project_id": "PVT_abc",
-                    "worktree": str(self.tmp / "wt" / name / "Coordinator"),
-                    "approvers_file": str(approvers),
-                    "state_dir": str(self.state_dir(name)),
-                }
-            )
-        )
-        path.chmod(0o600)
-        return path
-
-    def state_dir(self, name: str) -> Path:
-        return self.tmp / "state" / "issue-watch" / name
-
-    def child(
-        self,
-        name: str,
-        *,
-        stdout="cycle: cycle_complete\nexit: 0\n",
-        code=0,
-        seconds=1.0,
-        timed_out=False,
-    ):
-        def reply() -> object:
-            self.clock.advance(seconds)
-            return result(
-                stdout="" if timed_out else stdout, returncode=code, timed_out=timed_out
-            )
-
-        self.children[name] = reply
-
-    # -- the runner ------------------------------------------------------------------------
-    def run(self, argv, timeout, *, cwd=None):
-        key = tuple(argv)
-        self.calls.append((key, timeout))
-        if key == (ORCA, "repo", "list"):
-            if self.listing_reply is not None:
-                return self.listing_reply
-            lines = [
-                f"00000000-0000-4000-8000-{i:012d}  {n}  {_path(n)}"
-                for i, n in enumerate(self.names, 1)
-            ]
-            return result(stdout="\n".join(lines) + "\n")
-        if key[0] == "git":
-            parts = key[2].rstrip("/").rsplit("/", 2)
-            name = parts[1] if parts[2] == "Coordinator" else parts[2]
-            if parts[2] == "Coordinator" and name in self.worktree_origin:
-                return result(stdout=self.worktree_origin[name])
-            return result(stdout=f"https://github.com/IronbellyOrg/{name}.git\n")
-        if key[:3] == ("gh", "label", "list"):
-            return result(stdout=json.dumps([{"name": n} for n in self.labels]))
-        if key[:3] == ("gh", "api", "--method") and "issue-fields" in key[4]:
-            option = "Yes" if self.field_ok else "No"
-            row = {"name": "Approved", "data_type": "single_select"}
-            row["options"] = [{"name": option}]
-            return result(stdout=json.dumps([row]))
-        if key[:3] == ("gh", "api", "graphql"):
-            nodes = [{"id": i, "number": n} for n, i in enumerate(self.projects, 1)]
-            body = {"data": {"repository": {"projectsV2": {"nodes": nodes}}}}
-            return result(stdout=json.dumps(body))
-        assert key[0] == SC and key[1:4] == ("issue-watch", "once", "--config"), key
-        name = Path(key[4]).stem
-        return self.children[name]()
-
-    def started(self) -> list[str]:
-        return [Path(k[4]).stem for k, _ in self.calls if k[0] == SC]
-
-
-@pytest.fixture
-def world(tmp_path):
-    return World(tmp_path, NAMES[:3], FakeClock(CYCLE_NOW))
-
-
-def sweep(w: World, **over) -> dispatch.SweepResult:
-    args = dict(
-        orca=ORCA,
-        superclaude=SC,
-        defaults=DEFAULTS,
-        base=w.base,
-        deps_factory=lambda cfg: pytest.fail("no first run expected"),
-        monotonic=w.clock.monotonic,
-        now=w.clock.now,
-    )
-    args.update(over)
-    return dispatch.run_sweep(w, **args)
-
-
-def prepare(w: World, names=None) -> None:
-    for name in names or w.names:
-        w.config(name)
-        w.child(name)
-
-
-def test_the_order_rotates_across_three_sweeps(world) -> None:
-    prepare(world)
-    orders = []
-    for _ in range(3):
-        before = len(world.started())
-        out = sweep(world)
-        assert out.ok and out.stopped_after is None and out.skipped == ()
-        orders.append(world.started()[before:])
-    assert orders == [
-        ["Alpha", "Beta", "Gamma"],
-        ["Beta", "Gamma", "Alpha"],
-        ["Gamma", "Alpha", "Beta"],
-    ]
-
-
-def test_the_loop_stops_after_the_first_launched_line(world) -> None:
-    prepare(world)
-    world.child("Alpha", stdout="cycle: cycle_complete\nexit: 0\nlaunched: 12\n")
-    out = sweep(world)
-    assert world.started() == ["Alpha"]
-    assert out.stopped_after == "Alpha"
-    assert [(c.name, c.launched, c.attempted) for c in out.children] == [
-        ("Alpha", 12, None)
-    ]
-    assert [(s.name, s.reason) for s in out.skipped] == [
-        ("Beta", "stopped_after_launch"),
-        ("Gamma", "stopped_after_launch"),
-    ]
-
-
-def test_the_loop_stops_after_an_attempted_line(world) -> None:
-    prepare(world)
-    world.child("Alpha")
-    world.child("Beta", stdout="cycle: launch_unknown\nexit: 7\nattempted: 5\n", code=7)
-    out = sweep(world)
-    assert world.started() == ["Alpha", "Beta"]
-    assert out.stopped_after == "Beta"
-    beta = out.children[1]
-    assert (beta.exit_code, beta.reason, beta.attempted) == (7, "launch_unknown", 5)
-    assert [(s.name, s.reason) for s in out.skipped] == [
-        ("Gamma", "stopped_after_launch")
-    ]
-
-
-def test_a_sweep_that_stopped_early_starts_the_next_one_where_it_stopped(world) -> None:
-    prepare(world)
-    world.child("Alpha", stdout="cycle: cycle_complete\nexit: 0\nlaunched: 3\n")
-    sweep(world)
-    world.child("Alpha")  # nothing is launched any more
-    before = len(world.started())
-    sweep(world)
-    assert world.started()[before:] == ["Beta", "Gamma", "Alpha"]
-
-
-def _pend(w: World, name: str, *, at) -> None:
-    state_dir = w.state_dir(name)
-    store = record.init_state(state_dir, CYCLE_NOW - timedelta(days=1))
-    ctx = record.PendingContext(
-        approver_id=11,
-        approval_event_id=77,
-        approved_at=CYCLE_NOW - timedelta(hours=1),
-        launch_cwd=str(w.tmp),
-        launch_login="owner-login",
-        launch_account_id=1001,
-    )
-    store.save(record.mark_pending(store.load(), 9, ctx, at))
-
-
-def test_a_child_killed_after_255_s_with_a_pending_entry_stops_the_loop(world) -> None:
-    prepare(world)
-    world.child("Alpha", seconds=255.0, timed_out=True)
-    _pend(
-        world, "Alpha", at=CYCLE_NOW + timedelta(seconds=10)
-    )  # created during this sweep
-    out = sweep(world)
-    assert world.started() == ["Alpha"]
-    alpha = out.children[0]
-    assert (alpha.killed, alpha.exit_code, alpha.reason) == (
-        True,
-        None,
-        "child_timeout",
-    )
-    assert out.stopped_after == "Alpha"
-    assert [s.name for s in out.skipped] == ["Beta", "Gamma"]
-    # every child got the 255 second kill time
-    assert {t for k, t in world.calls if k[0] == SC} == {dispatch.CHILD_TIMEOUT_S}
-    assert (
-        dispatch.CHILD_TIMEOUT_S == 255.0
-        and dispatch.CHILD_TIMEOUT_S > cycle.DEADLINE_TOTAL_S
-    )
-
-
-def test_the_same_kill_with_no_pending_entry_lets_the_later_repos_run(world) -> None:
-    prepare(world)
-    world.child("Alpha", seconds=255.0, timed_out=True)
-    record.init_state(world.state_dir("Alpha"), CYCLE_NOW - timedelta(days=1))
-    out = sweep(world)
-    assert world.started() == [
-        "Alpha",
-        "Beta",
-        "Gamma",
-    ]  # the timeout never kills the loop
-    assert out.stopped_after is None and out.children[0].killed is True
-
-
-def test_an_entry_from_before_this_sweep_does_not_stop_the_loop(world) -> None:
-    prepare(world)
-    world.child("Alpha", seconds=255.0, timed_out=True)
-    _pend(world, "Alpha", at=CYCLE_NOW - timedelta(hours=5))  # an old entry
-    out = sweep(world)
-    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.stopped_after is None
-
-
-def test_a_killed_child_with_an_unreadable_store_stops_the_loop(world) -> None:
-    prepare(world)
-    world.child("Alpha", seconds=255.0, timed_out=True)
-    world.state_dir("Alpha").mkdir(parents=True)
-    (world.state_dir("Alpha") / "dispatch.json").write_text("{not json")
-    out = sweep(world)
-    assert world.started() == ["Alpha"] and out.stopped_after == "Alpha"
-
-
-def test_the_270_second_cap_reports_the_repos_not_reached(tmp_path) -> None:
-    w = World(tmp_path, NAMES, FakeClock(CYCLE_NOW))
-    prepare(w)
-    for name in w.names:
-        w.child(name, seconds=100.0)
-    out = sweep(w)
-    # the order is by name (Alpha, Beta, Delta, Gamma); children start at 0, 100 and 200 s
-    assert w.started() == ["Alpha", "Beta", "Delta"]
-    assert [(s.name, s.reason) for s in out.skipped] == [("Gamma", "loop_cap")]
-    assert out.elapsed_s == 300.0 and dispatch.LOOP_CAP_S == 270.0
-    # the next sweep starts at the repo that was not reached
-    w.clock.advance(1)
-    for name in w.names:
-        w.child(name, seconds=1.0)
-    before = len(w.started())
-    sweep(w)
-    assert w.started()[before:][0] == "Gamma"
-
-
-def test_a_repo_with_no_config_is_generated_and_checked_before_it_runs(
-    world, monkeypatch
-) -> None:
-    world.config("Alpha")
-    world.config("Gamma")
-    for name in ("Alpha", "Beta", "Gamma"):
-        world.child(name)
-    order: list[str] = []
-
-    def fake_ensure(repo, defs, runner, base):
-        order.append(f"ensure:{repo.name}")
-        world.config(repo.name, enabled=False)
-        return Outcome("generated", repo.name, config_path=base.config_dir)
-
-    def fake_first_run(path, defs, runner, deps_factory):
-        order.append(f"first_run:{Path(path).stem}")
-        data = json.loads(Path(path).read_text())
-        data["enabled"] = True
-        Path(path).write_text(json.dumps(data))
-
-    monkeypatch.setattr(dispatch, "ensure_config", fake_ensure)
-    monkeypatch.setattr(dispatch, "first_run", fake_first_run)
-    out = sweep(world)
-    assert order == ["ensure:Beta", "first_run:Beta"]
-    assert out.generated == ("Beta",)
-    assert world.started() == ["Alpha", "Beta", "Gamma"]
-
-
-def test_a_repo_whose_generation_is_skipped_is_reported_not_run(
-    world, monkeypatch
-) -> None:
-    world.config("Alpha")
-    world.config("Gamma")
-    world.child("Alpha")
-    world.child("Gamma")
-    monkeypatch.setattr(
-        dispatch,
-        "ensure_config",
-        lambda repo, d, r, b: Outcome("skipped", repo.name, "no_project"),
-    )
-    out = sweep(world)
-    assert world.started() == ["Alpha", "Gamma"]
-    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "no_project")]
-
-
-def test_a_config_that_is_not_enabled_is_skipped_with_a_reason(world) -> None:
-    prepare(world)
-    world.config("Beta", enabled=False)
-    out = sweep(world)
-    assert world.started() == ["Alpha", "Gamma"]
-    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "not_enabled")]
-
-
-@pytest.mark.parametrize(
-    "reply",
-    [
-        result(stderr="boom", returncode=1),
-        result(timed_out=True),
-        result(spawn_error="FileNotFoundError"),
-        result(stdout="not a list\n"),
-    ],
-)
-def test_a_failed_orca_list_gives_an_error_result_not_a_clean_one(world, reply) -> None:
-    prepare(world)
-    world.listing_reply = reply
-    out = sweep(world)
-    assert out.ok is False and out.error in {
-        "list_failed",
-        "list_timeout",
-        "unreadable_list",
-    }
-    assert out.children == () and world.started() == []
-
-
-def test_an_empty_but_successful_list_is_a_clean_empty_sweep(world) -> None:
-    world.listing_reply = result(stdout="")
-    out = sweep(world)
-    assert out.ok is True and out.error is None and out.children == ()
-
-
-def test_each_childs_exit_code_and_reason_are_kept(world) -> None:
-    prepare(world)
-    world.child("Alpha", stdout="cycle: gh_auth_failed\nexit: 3\n", code=3, seconds=2.0)
-    world.child("Beta", stdout="cycle: cycle_complete\nexit: 0\n", seconds=3.0)
-    out = sweep(world)
-    assert [(c.name, c.exit_code, c.reason) for c in out.children] == [
-        ("Alpha", 3, "gh_auth_failed"),
-        ("Beta", 0, "cycle_complete"),
-        ("Gamma", 0, "cycle_complete"),
-    ]
-    assert [c.seconds for c in out.children][:2] == [2.0, 3.0]
-    # a failing child without a launch never stops the loop
-    assert out.stopped_after is None and world.started() == ["Alpha", "Beta", "Gamma"]
-
-
-def test_a_child_that_cannot_start_never_kills_the_loop(world) -> None:
-    prepare(world)
-    world.children["Alpha"] = lambda: result(spawn_error="FileNotFoundError")
-    out = sweep(world)
-    assert (out.children[0].reason, out.children[0].killed) == ("spawn_error", False)
-    assert world.started() == ["Alpha", "Beta", "Gamma"]
-
-
-def test_the_child_command_is_an_absolute_argv_with_the_config_path(world) -> None:
-    prepare(world)
-    sweep(world)
-    children = [k for k, _ in world.calls if k[0] == SC]
-    assert children[0] == (
-        SC,
-        "issue-watch",
-        "once",
-        "--config",
-        str(world.base.config_dir / dispatch.SUBDIR / "Alpha.json"),
-    )
-    assert all(Path(k[4]).is_absolute() for k in children)
-
-
-@pytest.mark.parametrize("orca,sc", [("orca", SC), (ORCA, "superclaude")])
-def test_relative_program_paths_are_refused_because_cron_has_no_path(
-    world, orca, sc
-) -> None:
-    with pytest.raises(ValueError):
-        sweep(world, orca=orca, superclaude=sc)
-    assert world.calls == []
-
-
-def test_the_rotation_file_is_private_and_a_broken_one_restarts_at_the_first_repo(
-    world,
-) -> None:
-    prepare(world)
-    sweep(world)
-    path = world.base.state_dir / "issue-watch" / dispatch.ROTATION_FILE
-    assert json.loads(path.read_text()) == {"next": 1}
-    assert oct(path.stat().st_mode & 0o777) == "0o600"
-    path.write_text("garbage")
-    before = len(world.started())
-    sweep(world)
-    assert world.started()[before:][0] == "Alpha"
-
-
-def test_nothing_is_written_outside_tmp_path(world, tmp_path) -> None:
-    prepare(world)
-    sweep(world)
-    assert not (tmp_path / "home").exists()
-    assert generate.Base.default().config_dir.expanduser() != world.base.config_dir
-
-
-# --- plan Task 24: the account rate wait and the pre-child checks -------------------------
-
-
-def _rate_limited(w: World, name: str, minutes: float = 10.0):
-    """A child that ended `rate_limited` and a store that holds the time it may run again."""
-    until = CYCLE_NOW + timedelta(minutes=minutes)
-    store = record.init_state(w.state_dir(name), CYCLE_NOW - timedelta(days=1))
-    store.save(record.set_next_permitted(store.load(), until))
-    w.child(name, stdout="cycle: rate_limited\nexit: 5\n", code=5)
-    return until
-
-
-def _wait_file(w: World) -> Path:
-    return w.base.state_dir / "issue-watch" / dispatch.RATE_WAIT_FILE
-
-
-def test_a_rate_limited_child_stops_later_children_until_the_stored_time(world) -> None:
-    prepare(world)
-    until = _rate_limited(world, "Alpha")
-    out = sweep(world)
-    assert world.started() == ["Alpha"]
-    assert out.children[0].reason == "rate_limited" and out.waiting_until == until
-    assert [(s.name, s.reason) for s in out.skipped] == [
-        ("Beta", "account_rate_wait"),
-        ("Gamma", "account_rate_wait"),
-    ]
-    stored = json.loads(_wait_file(world).read_text())
-    assert stored == {"next_permitted_at": until.strftime("%Y-%m-%dT%H:%M:%SZ")}
-    assert oct(_wait_file(world).stat().st_mode & 0o777) == "0o600"
-
-
-def test_a_restart_of_the_loop_honours_the_file_until_its_time(world) -> None:
-    prepare(world)
-    until = _rate_limited(world, "Alpha")
-    sweep(world)
-    calls = len(world.calls)
-    world.clock.advance(60)  # a new sweep a minute later: still waiting
-    again = sweep(world)
-    assert again.waiting_until == until and again.children == ()
-    assert len(world.calls) == calls  # no orca list, no gh read, no child
-    world.clock.advance(10 * 60)  # past the stored time
-    for name in world.names:
-        world.child(name)
-    after = sweep(world)
-    assert after.waiting_until is None and len(after.children) == 3
-
-
-def test_a_rate_limit_clamped_child_does_not_write_the_file(world) -> None:
-    prepare(world)
-    world.child("Alpha", stdout="cycle: rate_limit_clamped\nexit: 5\n", code=5)
-    out = sweep(world)
-    assert not _wait_file(world).exists()
-    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.waiting_until is None
-
-
-def test_an_expired_wait_file_is_ignored(world) -> None:
-    prepare(world)
-    path = _wait_file(world)
-    path.parent.mkdir(parents=True)
-    past = (CYCLE_NOW - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
-    path.write_text(json.dumps({"next_permitted_at": past}))
-    out = sweep(world)
-    assert out.waiting_until is None and world.started() == ["Alpha", "Beta", "Gamma"]
-
-
-def test_a_broken_wait_file_is_ignored(world) -> None:
-    prepare(world)
-    path = _wait_file(world)
-    path.parent.mkdir(parents=True)
-    path.write_text("garbage")
-    assert sweep(world).waiting_until is None
-
-
-def _created(w: World) -> list:
-    return [k for k, _ in w.calls if k[:3] == ("gh", "label", "create")]
-
-
-@pytest.mark.parametrize(
-    "arrange, reason",
-    [
-        (lambda w: w.no_worktree.add("Beta"), "worktree_invalid"),
-        (lambda w: w.not_git.add("Beta"), "worktree_not_git"),
-        (
-            lambda w: w.worktree_origin.update(
-                Beta="https://github.com/SomeoneElse/Beta.git\n"
-            ),
-            "origin_mismatch",
-        ),
-        (lambda w: w.labels.remove(DEFAULTS.trigger_label), "label_missing"),
-        (lambda w: setattr(w, "field_ok", False), "approved_field_missing"),
-        (lambda w: setattr(w, "projects", []), "no_project"),
-        (lambda w: setattr(w, "projects", ["PVT_other"]), "project_mismatch"),
-        (lambda w: setattr(w, "projects", ["PVT_abc", "PVT_two"]), "project_ambiguous"),
-    ],
-)
-def test_each_failed_pre_child_check_gives_its_own_skip_reason_and_creates_nothing(
-    tmp_path, arrange, reason
-) -> None:
-    w = World(tmp_path, ["Beta"], FakeClock(CYCLE_NOW))
-    arrange(w)
-    prepare(w)
-    out = sweep(w)
-    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", reason)]
-    assert out.children == () and w.started() == []
-    assert reason in dispatch.SKIP_REASONS
-    assert _created(w) == []  # the loop never creates a label
-    assert not any(k[:2] == ("gh", "project") for k, _ in w.calls)
-
-
-def test_a_failed_pre_child_check_skips_only_that_repo(world) -> None:
-    world.no_worktree.add("Beta")  # set before the configs are written
-    prepare(world)
-    out = sweep(world)
-    assert world.started() == ["Alpha", "Gamma"]
-    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "worktree_invalid")]
-
-
-def test_a_failed_label_or_field_read_is_reported_not_treated_as_missing(
-    world, monkeypatch
-) -> None:
-    prepare(world)
-    real = world.run
-
-    def run(argv, timeout, *, cwd=None):
-        if tuple(argv)[:3] == ("gh", "label", "list"):
-            return result(stderr="HTTP 502", returncode=1)
-        return real(argv, timeout, cwd=cwd)
-
-    world.run = run  # type: ignore[method-assign]
-    out = sweep(world)
-    assert {s.reason for s in out.skipped} == {"label_check_failed"}
-    assert world.started() == []
-
-
-def test_the_org_field_is_read_once_per_owner_per_sweep(world) -> None:
-    prepare(world)
-    sweep(world)
-    reads = [k for k, _ in world.calls if "issue-fields" in " ".join(k)]
-    assert len(reads) == 1  # one owner, three repos
-
-
-def test_every_skip_reason_a_sweep_gives_is_in_the_documented_table(world) -> None:
-    prepare(world)
-    world.no_worktree.add("Beta")
-    world.config("Beta")
-    out = sweep(world)
-    for item in out.skipped:
-        assert item.reason in dispatch.SKIP_REASONS
-    from superclaude.cli.issue_watch import audit
-
-    for reason, text in dispatch.SKIP_REASONS.items():
-        assert text and (reason in audit.REASON_TABLE or "(audit reason" not in text), (
-            reason
-        )
-
-
-def test_every_reason_the_generator_and_the_repo_list_can_give_is_in_the_table() -> (
-    None
-):
-    """The sweep passes these through; the table must name each (plan Task 24, AC 2)."""
-    import re
-
-    pkg = Path(dispatch.__file__).parent
-    generated = set(
-        re.findall(r'_skip\(name, "([a-z_]+)"\)', (pkg / "generate.py").read_text())
-    )
-    listed = set(re.findall(r'skip\("([a-z_]+)"\)', (pkg / "repos.py").read_text()))
-    assert {"no_project", "project_ambiguous", "generated_invalid"} <= generated
-    assert {"path_in_tmp", "foreign_owner"} <= listed
-    assert (generated | listed) <= set(dispatch.SKIP_REASONS), (
-        generated | listed
-    ) - set(dispatch.SKIP_REASONS)
diff --git a/tests/issue_watch/test_module_boundaries.py b/tests/issue_watch/test_module_boundaries.py
index c1f1f7e90..9a89c7918 100644
--- a/tests/issue_watch/test_module_boundaries.py
+++ b/tests/issue_watch/test_module_boundaries.py
@@ -103,7 +103,18 @@ RULES: dict[str, Rule] = {
         siblings=frozenset({"cycle", "defaults", "github", "repos", "runner"})
     ),
     "cli": Rule(
-        siblings=frozenset({"cycle", "record", "audit", "launch", "runner"}),
+        siblings=frozenset(
+            {
+                "cycle",
+                "record",
+                "audit",
+                "launch",
+                "runner",
+                "defaults",
+                "dispatch",
+                "generate",
+            }
+        ),
         third_party=frozenset({"click"}),
     ),
 }
diff --git a/src/superclaude/cli/issue_watch/dispatch.py b/src/superclaude/cli/issue_watch/dispatch.py
new file mode 100644
index 000000000..42ee4c338
--- /dev/null
+++ b/src/superclaude/cli/issue_watch/dispatch.py
@@ -0,0 +1,479 @@
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
+from collections.abc import Callable, Iterator
+from contextlib import contextmanager
+from dataclasses import dataclass, field
+from datetime import datetime, timezone
+from pathlib import Path
+
+from . import cycle, record, repo_init
+from .defaults import Defaults
+from .first_run import first_run
+from .generate import Base, _projects, ensure_config
+from .launch import check_origin
+from .predicates import format_utc, parse_utc
+from .repos import OrcaRepo, RepoListError, list_repos
+from .runner import Runner
+
+LOOP_CAP_S = 270.0
+CHILD_TIMEOUT_S = 255.0
+GIT_TIMEOUT_S = 15.0
+ROTATION_FILE = "rotation.json"
+RATE_WAIT_FILE = "account-rate-wait.json"
+LOCK_FILE = "run-all.lock"
+SUBDIR = "issue-watch.d"
+
+# Every reason a sweep gives for a repository it did not run (plan Tasks 23 and 24). The reasons that
+# also exist in ``audit.REASON_TABLE`` keep their meaning; the rest are documented here.
+SKIP_REASONS: dict[str, str] = {
+    "stopped_after_launch": "an earlier repo launched or attempted a launch this sweep",
+    "loop_cap": "the 270 second loop cap was reached before this repo",
+    "account_rate_wait": "a child hit the account rate limit; no child starts until its time",
+    "not_enabled": "the config is enabled: false (the first run did not pass, or the owner set it)",
+    "config_unreadable": "the config file cannot be read as JSON",
+    "config_invalid": "cycle.load_config refused the config (audit reason config_invalid)",
+    "worktree_invalid": "the Coordinator worktree is not an existing directory (audit reason)",
+    "worktree_not_git": "the Coordinator worktree has no .git entry",
+    "origin_mismatch": "the worktree's origin does not name the repo (audit reason)",
+    "label_missing": "the trigger label is missing on the repo (the loop never creates it)",
+    "label_check_failed": "the label list could not be read",
+    "approved_field_missing": "the organization has no single-select Approved field with the option",
+    "approved_field_check_failed": "the organization issue fields could not be read",
+    "no_project": "the repo has no Project",
+    "project_ambiguous": "several Projects and the defaults map does not name the configured one",
+    "project_mismatch": "the configured Project is not one of the repo's Projects",
+    "project_check_failed": "the repo's Projects could not be read",
+    "not_generated": "the config generator gave no reason (should not happen)",
+    "project_read_failed": "the repo's Projects could not be read (config generation)",
+    "bad_name": "the Orca repo name is not a safe file name (config generation)",
+    "bad_repo": "the origin owner/name is not a strict owner/name (config generation)",
+    "approvers_file_exists": "an approvers file is there without a config; never overwritten (generation)",
+    "account_read_failed": "gh api user could not be read (config generation)",
+    "approver_read_failed": "a fixed approver login could not be turned into an id (generation)",
+    "maintainers_read_failed": "the repo's maintainers could not be read (config generation)",
+    "no_approvers": "no approver is left once the launch account is removed (config generation)",
+    "generated_invalid": "the generated config failed its own validation and was removed (generation)",
+    "path_in_tmp": "the Orca repo path is under /tmp (from the repo list)",
+    "origin_unreadable": "git could not read the repo's origin (from the repo list)",
+    "origin_not_github": "the repo's origin is not on github.com (from the repo list)",
+    "foreign_owner": "the repo's owner is not an allowed owner (from the repo list)",
+}
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
+    waiting_until: datetime | None = None
+    """Set when the account rate wait stopped the whole sweep (no list, no child)."""
+    would_run: tuple[str, ...] = ()
+    would_generate: tuple[str, ...] = ()
+    """Filled by a dry run only: the repos a real sweep would run, and generate a config for."""
+    notes: list[str] = field(default_factory=list)
+
+
+def _now() -> datetime:
+    return datetime.now(timezone.utc)
+
+
+# --- the loop lock ---------------------------------------------------------------------------
+
+
+class LoopLockHeld(Exception):
+    """Another sweep holds the loop lock."""
+
+
+@contextmanager
+def loop_lock(base: Base) -> Iterator[None]:
+    """Hold an exclusive ``flock`` on ``<state dir>/issue-watch/run-all.lock`` for one sweep.
+
+    Raises ``LoopLockHeld`` at once when another sweep holds it (never waits). The lock is
+    released and its descriptor closed in a ``finally``.
+    """
+    import fcntl  # not at module level: importing the package must work off Linux
+
+    path = base.state_dir.expanduser() / "issue-watch" / LOCK_FILE
+    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
+    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
+    try:
+        try:
+            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
+        except OSError:
+            raise LoopLockHeld from None
+        yield
+    finally:
+        os.close(fd)  # closing the descriptor releases the flock
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
+def _rate_wait_path(base: Base) -> Path:
+    return base.state_dir.expanduser() / "issue-watch" / RATE_WAIT_FILE
+
+
+def _read_rate_wait(base: Base) -> datetime | None:
+    """The stored account wait time, or None when there is none or it cannot be read."""
+    try:
+        raw = json.loads(_rate_wait_path(base).read_text(encoding="utf-8"))
+        return parse_utc(raw["next_permitted_at"])
+    except (OSError, ValueError, KeyError, TypeError):
+        return None
+
+
+def _write_rate_wait(base: Base, when: datetime) -> None:
+    path = _rate_wait_path(base)
+    try:
+        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
+        staged = path.with_name(f".{path.name}.new")
+        fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
+        with os.fdopen(fd, "w", encoding="utf-8") as handle:
+            handle.write(json.dumps({"next_permitted_at": format_utc(when)}) + "\n")
+        os.replace(staged, path)
+    except OSError:
+        pass  # without the file the next sweep still stops: each child honours its own store
+
+
+def _child_next_permitted(config_path: Path) -> datetime | None:
+    """The child's ``next_permitted_at`` from its store (read only), else None."""
+    try:
+        config = cycle.load_config(config_path)
+        return record.FileStore(config.state_dir).load().next_permitted_at
+    except (cycle.ConfigError, record.StoreError, OSError):
+        return None
+
+
+def _precheck(
+    runner: Runner,
+    config: cycle.Config,
+    defaults: Defaults,
+    field_cache: dict[str, str],
+) -> str | None:
+    """The reads that run before a child (R14); the skip reason of the first that fails.
+
+    Nothing is created here: a missing label or field is reported and the repo is skipped.
+    """
+    if not config.worktree.is_dir():
+        return "worktree_invalid"
+    if not (config.worktree / ".git").exists():
+        return "worktree_not_git"
+    if check_origin(runner, config.worktree, GIT_TIMEOUT_S, config.repo) is not None:
+        return "origin_mismatch"
+    label = repo_init.trigger_label_state(config.repo, defaults, runner)
+    if label != repo_init.PRESENT:
+        return "label_missing" if label == repo_init.MISSING else "label_check_failed"
+    owner = config.repo.split("/")[0]
+    if owner not in field_cache:
+        field_cache[owner] = repo_init.check_approved_field(owner, defaults, runner)
+    if field_cache[owner] != repo_init.FIELD_PRESENT:
+        if field_cache[owner] == repo_init.FIELD_MISSING:
+            return "approved_field_missing"
+        return "approved_field_check_failed"
+    ids = _projects(runner, config.repo)
+    if ids is None:
+        return "project_check_failed"
+    if not ids:
+        return "no_project"
+    if config.project_id not in ids:
+        return "project_mismatch"
+    if len(ids) > 1 and defaults.projects.get(config.repo) != config.project_id:
+        return "project_ambiguous"
+    return None
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
+    dry_run: bool = False,
+) -> SweepResult:
+    """Run one sweep; see the module docstring for the rules.
+
+    ``dry_run`` lists the repositories and the decision for each, and only reads: it generates no
+    config, writes no rotation or wait file, creates no label and starts no child.
+    """
+    for label, path in (("orca", orca), ("superclaude", superclaude)):
+        if not os.path.isabs(path):
+            raise ValueError(f"{label} must be an absolute path (cron has no PATH)")
+    began = monotonic()
+    since = now()
+    wait = _read_rate_wait(base)
+    if wait is not None and since < wait:
+        # the account is rate limited: no list, no child, until the stored time (R5)
+        return SweepResult(True, waiting_until=wait, elapsed_s=0.0)
+    try:
+        listing = list_repos(runner, orca, defaults.allowed_owners)
+    except RepoListError as exc:
+        return SweepResult(False, error=exc.reason)
+    repos = sorted(listing.repos, key=lambda r: r.name)
+    skipped = [Skipped(s.name, s.reason) for s in listing.skipped]
+    children: list[ChildResult] = []
+    generated: list[str] = []
+    would_run: list[str] = []
+    would_generate: list[str] = []
+    stopped_after: str | None = None
+    rate_waiting: datetime | None = None
+    field_cache: dict[str, str] = {}
+    if not repos:
+        return SweepResult(
+            True, skipped=tuple(skipped), elapsed_s=round(monotonic() - began, 3)
+        )
+
+    start = _read_rotation(base) % len(repos)
+    order = repos[start:] + repos[:start]
+    first_unreached: int | None = None
+    for position, repo in enumerate(order):
+        if rate_waiting is not None:
+            skipped.append(Skipped(repo.name, "account_rate_wait"))
+            first_unreached = (
+                first_unreached if first_unreached is not None else position
+            )
+            continue
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
+            if (
+                dry_run
+            ):  # generating writes files and calls GitHub: a dry run only says so
+                would_generate.append(repo.name)
+                continue
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
+        try:
+            config = cycle.load_config(config_path)
+        except cycle.ConfigError:
+            skipped.append(Skipped(repo.name, "config_invalid"))
+            continue
+        why = _precheck(runner, config, defaults, field_cache)
+        if why is not None:
+            skipped.append(Skipped(repo.name, why))
+            continue
+        if dry_run:
+            would_run.append(repo.name)
+            continue
+        child = _run_child(runner, superclaude, repo, config_path, monotonic)
+        children.append(child)
+        if child.reason == "rate_limited":
+            # plain rate_limited only: rate_limit_clamped is the 3600 s clamp and writes nothing
+            when = _child_next_permitted(config_path) or since
+            rate_waiting = when
+            if when > since:
+                _write_rate_wait(base, when)
+        elif child.launched is not None or child.attempted is not None:
+            stopped_after = repo.name
+        elif child.killed and _opened_this_sweep(config_path, since):
+            stopped_after = repo.name  # a killed child counts as a launch attempt
+    if dry_run:
+        pass  # a dry run writes no rotation file
+    elif first_unreached is None:
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
+        waiting_until=rate_waiting,
+        would_run=tuple(would_run),
+        would_generate=tuple(would_generate),
+    )
+
+
+__all__ = [
+    "CHILD_TIMEOUT_S",
+    "LOOP_CAP_S",
+    "ChildResult",
+    "LoopLockHeld",
+    "Skipped",
+    "SweepResult",
+    "loop_lock",
+    "run_sweep",
+]
diff --git a/tests/issue_watch/test_dispatch.py b/tests/issue_watch/test_dispatch.py
new file mode 100644
index 000000000..ccd608034
--- /dev/null
+++ b/tests/issue_watch/test_dispatch.py
@@ -0,0 +1,616 @@
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
+        # what the read-only pre-child checks see (plan Task 24); a test changes one at a time
+        self.labels = ["bug", DEFAULTS.trigger_label]
+        self.field_ok = True
+        self.projects = ["PVT_abc"]
+        self.worktree_origin: dict[str, str] = {}
+        self.no_worktree: set[str] = set()
+        self.not_git: set[str] = set()
+
+    # -- the files a generated config would have ------------------------------------------
+    def config(self, name: str, *, enabled: bool = True) -> Path:
+        work = self.tmp / "wt" / name / "Coordinator"
+        if name not in self.no_worktree:
+            work.mkdir(parents=True, exist_ok=True)
+            if name not in self.not_git:
+                (work / ".git").write_text("gitdir: /elsewhere\n")
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
+            parts = key[2].rstrip("/").rsplit("/", 2)
+            name = parts[1] if parts[2] == "Coordinator" else parts[2]
+            if parts[2] == "Coordinator" and name in self.worktree_origin:
+                return result(stdout=self.worktree_origin[name])
+            return result(stdout=f"https://github.com/IronbellyOrg/{name}.git\n")
+        if key[:3] == ("gh", "label", "list"):
+            return result(stdout=json.dumps([{"name": n} for n in self.labels]))
+        if key[:3] == ("gh", "api", "--method") and "issue-fields" in key[4]:
+            option = "Yes" if self.field_ok else "No"
+            row = {"name": "Approved", "data_type": "single_select"}
+            row["options"] = [{"name": option}]
+            return result(stdout=json.dumps([row]))
+        if key[:3] == ("gh", "api", "graphql"):
+            nodes = [{"id": i, "number": n} for n, i in enumerate(self.projects, 1)]
+            body = {"data": {"repository": {"projectsV2": {"nodes": nodes}}}}
+            return result(stdout=json.dumps(body))
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
+
+
+# --- plan Task 24: the account rate wait and the pre-child checks -------------------------
+
+
+def _rate_limited(w: World, name: str, minutes: float = 10.0):
+    """A child that ended `rate_limited` and a store that holds the time it may run again."""
+    until = CYCLE_NOW + timedelta(minutes=minutes)
+    store = record.init_state(w.state_dir(name), CYCLE_NOW - timedelta(days=1))
+    store.save(record.set_next_permitted(store.load(), until))
+    w.child(name, stdout="cycle: rate_limited\nexit: 5\n", code=5)
+    return until
+
+
+def _wait_file(w: World) -> Path:
+    return w.base.state_dir / "issue-watch" / dispatch.RATE_WAIT_FILE
+
+
+def test_a_rate_limited_child_stops_later_children_until_the_stored_time(world) -> None:
+    prepare(world)
+    until = _rate_limited(world, "Alpha")
+    out = sweep(world)
+    assert world.started() == ["Alpha"]
+    assert out.children[0].reason == "rate_limited" and out.waiting_until == until
+    assert [(s.name, s.reason) for s in out.skipped] == [
+        ("Beta", "account_rate_wait"),
+        ("Gamma", "account_rate_wait"),
+    ]
+    stored = json.loads(_wait_file(world).read_text())
+    assert stored == {"next_permitted_at": until.strftime("%Y-%m-%dT%H:%M:%SZ")}
+    assert oct(_wait_file(world).stat().st_mode & 0o777) == "0o600"
+
+
+def test_a_restart_of_the_loop_honours_the_file_until_its_time(world) -> None:
+    prepare(world)
+    until = _rate_limited(world, "Alpha")
+    sweep(world)
+    calls = len(world.calls)
+    world.clock.advance(60)  # a new sweep a minute later: still waiting
+    again = sweep(world)
+    assert again.waiting_until == until and again.children == ()
+    assert len(world.calls) == calls  # no orca list, no gh read, no child
+    world.clock.advance(10 * 60)  # past the stored time
+    for name in world.names:
+        world.child(name)
+    after = sweep(world)
+    assert after.waiting_until is None and len(after.children) == 3
+
+
+def test_a_rate_limit_clamped_child_does_not_write_the_file(world) -> None:
+    prepare(world)
+    world.child("Alpha", stdout="cycle: rate_limit_clamped\nexit: 5\n", code=5)
+    out = sweep(world)
+    assert not _wait_file(world).exists()
+    assert world.started() == ["Alpha", "Beta", "Gamma"] and out.waiting_until is None
+
+
+def test_an_expired_wait_file_is_ignored(world) -> None:
+    prepare(world)
+    path = _wait_file(world)
+    path.parent.mkdir(parents=True)
+    past = (CYCLE_NOW - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
+    path.write_text(json.dumps({"next_permitted_at": past}))
+    out = sweep(world)
+    assert out.waiting_until is None and world.started() == ["Alpha", "Beta", "Gamma"]
+
+
+def test_a_broken_wait_file_is_ignored(world) -> None:
+    prepare(world)
+    path = _wait_file(world)
+    path.parent.mkdir(parents=True)
+    path.write_text("garbage")
+    assert sweep(world).waiting_until is None
+
+
+def _created(w: World) -> list:
+    return [k for k, _ in w.calls if k[:3] == ("gh", "label", "create")]
+
+
+@pytest.mark.parametrize(
+    "arrange, reason",
+    [
+        (lambda w: w.no_worktree.add("Beta"), "worktree_invalid"),
+        (lambda w: w.not_git.add("Beta"), "worktree_not_git"),
+        (
+            lambda w: w.worktree_origin.update(
+                Beta="https://github.com/SomeoneElse/Beta.git\n"
+            ),
+            "origin_mismatch",
+        ),
+        (lambda w: w.labels.remove(DEFAULTS.trigger_label), "label_missing"),
+        (lambda w: setattr(w, "field_ok", False), "approved_field_missing"),
+        (lambda w: setattr(w, "projects", []), "no_project"),
+        (lambda w: setattr(w, "projects", ["PVT_other"]), "project_mismatch"),
+        (lambda w: setattr(w, "projects", ["PVT_abc", "PVT_two"]), "project_ambiguous"),
+    ],
+)
+def test_each_failed_pre_child_check_gives_its_own_skip_reason_and_creates_nothing(
+    tmp_path, arrange, reason
+) -> None:
+    w = World(tmp_path, ["Beta"], FakeClock(CYCLE_NOW))
+    arrange(w)
+    prepare(w)
+    out = sweep(w)
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", reason)]
+    assert out.children == () and w.started() == []
+    assert reason in dispatch.SKIP_REASONS
+    assert _created(w) == []  # the loop never creates a label
+    assert not any(k[:2] == ("gh", "project") for k, _ in w.calls)
+
+
+def test_a_failed_pre_child_check_skips_only_that_repo(world) -> None:
+    world.no_worktree.add("Beta")  # set before the configs are written
+    prepare(world)
+    out = sweep(world)
+    assert world.started() == ["Alpha", "Gamma"]
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "worktree_invalid")]
+
+
+def test_a_failed_label_or_field_read_is_reported_not_treated_as_missing(
+    world, monkeypatch
+) -> None:
+    prepare(world)
+    real = world.run
+
+    def run(argv, timeout, *, cwd=None):
+        if tuple(argv)[:3] == ("gh", "label", "list"):
+            return result(stderr="HTTP 502", returncode=1)
+        return real(argv, timeout, cwd=cwd)
+
+    world.run = run  # type: ignore[method-assign]
+    out = sweep(world)
+    assert {s.reason for s in out.skipped} == {"label_check_failed"}
+    assert world.started() == []
+
+
+def test_the_org_field_is_read_once_per_owner_per_sweep(world) -> None:
+    prepare(world)
+    sweep(world)
+    reads = [k for k, _ in world.calls if "issue-fields" in " ".join(k)]
+    assert len(reads) == 1  # one owner, three repos
+
+
+def test_every_skip_reason_a_sweep_gives_is_in_the_documented_table(world) -> None:
+    prepare(world)
+    world.no_worktree.add("Beta")
+    world.config("Beta")
+    out = sweep(world)
+    for item in out.skipped:
+        assert item.reason in dispatch.SKIP_REASONS
+    from superclaude.cli.issue_watch import audit
+
+    for reason, text in dispatch.SKIP_REASONS.items():
+        assert text and (reason in audit.REASON_TABLE or "(audit reason" not in text), (
+            reason
+        )
+
+
+def test_every_reason_the_generator_and_the_repo_list_can_give_is_in_the_table() -> (
+    None
+):
+    """The sweep passes these through; the table must name each (plan Task 24, AC 2)."""
+    import re
+
+    pkg = Path(dispatch.__file__).parent
+    generated = set(
+        re.findall(r'_skip\(name, "([a-z_]+)"\)', (pkg / "generate.py").read_text())
+    )
+    listed = set(re.findall(r'skip\("([a-z_]+)"\)', (pkg / "repos.py").read_text()))
+    assert {"no_project", "project_ambiguous", "generated_invalid"} <= generated
+    assert {"path_in_tmp", "foreign_owner"} <= listed
+    assert (generated | listed) <= set(dispatch.SKIP_REASONS), (
+        generated | listed
+    ) - set(dispatch.SKIP_REASONS)

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
