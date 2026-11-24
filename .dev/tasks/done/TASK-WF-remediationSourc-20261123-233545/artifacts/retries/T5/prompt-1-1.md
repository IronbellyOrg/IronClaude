06b540de34ad0a8281a7d6a5d6487876a76c82ab
Review one task for spec compliance.

Task brief: ## Task 5: Test the retry in test_dispatch.py

Depends on: Task 2

In `tests/issue_watch/test_dispatch.py`, add a `World.report(name, first_line)` helper next to `World.config` (line 48) that writes `first-run.txt` in `World.state_dir(name)` with mode 600, and tests that monkeypatch `dispatch.first_run` as the existing tests at lines 364-369 and 390-397 do (the `sweep()` helper at line 141 uses a `deps_factory` that fails, so the real `first_run` must not run). Set report ages with `os.utime`. Cover: failed `config` report then valid worktree then the next sweep enables the config and starts the child (`world.started()`); a repeated failure stays `not_enabled` with exactly one fake `first_run` call; no report means no call (the existing test at line 421 stays as it is); a `passed` report on a disabled config means no call; a dry-run sweep means no call and no file change; a failure at `label` younger than 3600 seconds means no call and older than 3600 seconds means one call; an existing `dispatch.json` and `lock` in the state directory are unchanged after a retry that fails.

Acceptance criteria:
- T5.AC1: Every case above has its own test, and the retry tests fail against the code before Task 2.
- T5.AC2: `uv run pytest tests/issue_watch -q` passes with no change to `tests/issue_watch/test_security_invariants.py`.
Global constraints: ## Constraints

- Reuse the existing `first_run` function as the only setup path; do not add GitHub writes, label creation or store creation to `dispatch.py` or `cycle.py` (the boundary pinned by `tests/issue_watch/test_security_invariants.py` stays intact).
- Do not change the config schema (`_TOP_KEYS` in `src/superclaude/cli/issue_watch/cycle.py`) and do not change `ensure_config` in `src/superclaude/cli/issue_watch/generate.py`.
- A config with no first-run report, or whose report starts with `first-run: passed`, is never retried.
- A dry-run sweep makes no `first_run` call and writes no file.
- Do not edit anything under `.claude/`; change `src/` and `tests/` only.
Start sha: 06b540de34ad0a8281a7d6a5d6487876a76c82ab
Diff against the start snapshot: 
```diff
diff --git a/tests/issue_watch/test_dispatch.py b/tests/issue_watch/test_dispatch.py
index e17d4bfc7..d89270b27 100644
--- a/tests/issue_watch/test_dispatch.py
+++ b/tests/issue_watch/test_dispatch.py
@@ -6,6 +6,7 @@ Every path is under ``tmp_path``; no real ``orca``, ``gh``, ``git`` or ``supercl
 from __future__ import annotations
 
 import json
+import os
 from datetime import timedelta
 from pathlib import Path
 
@@ -77,6 +78,17 @@ class World:
     def state_dir(self, name: str) -> Path:
         return self.tmp / "state" / "issue-watch" / name
 
+    def report(self, name: str, first_line: str, *, age_s: float = 0.0) -> Path:
+        """The first-run report a first run left in the state dir, ``age_s`` before the sweep."""
+        directory = self.state_dir(name)
+        directory.mkdir(parents=True, exist_ok=True)
+        path = directory / "first-run.txt"
+        path.write_text(first_line + "\nship_gate: closed\n")
+        path.chmod(0o600)
+        when = (CYCLE_NOW - timedelta(seconds=age_s)).timestamp()
+        os.utime(path, (when, when))
+        return path
+
     def child(
         self,
         name: str,
@@ -707,3 +719,128 @@ def test_every_reason_the_generator_and_the_repo_list_can_give_is_in_the_table()
     assert (generated | listed) <= set(dispatch.SKIP_REASONS), (
         generated | listed
     ) - set(dispatch.SKIP_REASONS)
+
+
+# --- a failed first run is retried on a later sweep (issue 751) --------------------------------
+
+FAILED_CONFIG = "first-run: failed config: worktree_invalid"
+
+
+def _spy_first_run(monkeypatch, calls: list[str], *, enable: bool) -> None:
+    def fake(path, defs, runner, deps_factory):
+        calls.append(Path(path).stem)
+        if enable:
+            data = json.loads(Path(path).read_text())
+            data["enabled"] = True
+            Path(path).write_text(json.dumps(data))
+
+    monkeypatch.setattr(dispatch, "first_run", fake)
+
+
+def _disabled_beta(world: World, first_line: str | None, *, age_s: float = 0.0) -> Path:
+    prepare(world)
+    path = world.config("Beta", enabled=False)
+    if first_line is not None:
+        world.report("Beta", first_line, age_s=age_s)
+    return path
+
+
+def test_a_failed_config_step_is_retried_and_the_repo_then_runs(
+    world, monkeypatch
+) -> None:
+    _disabled_beta(world, FAILED_CONFIG)
+    calls: list[str] = []
+    _spy_first_run(monkeypatch, calls, enable=True)
+    out = sweep(world)
+    assert calls == ["Beta"]
+    assert world.started() == ["Alpha", "Beta", "Gamma"]
+    assert out.skipped == ()
+
+
+def test_a_repeated_failure_stays_not_enabled_with_one_retry_per_sweep(
+    world, monkeypatch
+) -> None:
+    _disabled_beta(world, FAILED_CONFIG)
+    calls: list[str] = []
+    _spy_first_run(monkeypatch, calls, enable=False)
+    out = sweep(world)
+    assert calls == ["Beta"]
+    assert world.started() == ["Alpha", "Gamma"]
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "not_enabled")]
+
+
+@pytest.mark.parametrize(
+    "first_line", [None, "first-run: passed", "something else entirely"]
+)
+def test_a_disabled_config_without_a_failed_report_is_not_retried(
+    world, monkeypatch, first_line
+) -> None:
+    _disabled_beta(world, first_line)
+    calls: list[str] = []
+    _spy_first_run(monkeypatch, calls, enable=True)
+    out = sweep(world)
+    assert calls == []
+    assert world.started() == ["Alpha", "Gamma"]
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "not_enabled")]
+
+
+def test_a_dry_run_sweep_makes_no_retry_and_changes_no_file(world, monkeypatch) -> None:
+    path = _disabled_beta(world, FAILED_CONFIG)
+    report = world.state_dir("Beta") / "first-run.txt"
+    before = (path.read_bytes(), report.read_bytes(), report.stat().st_mtime)
+    calls: list[str] = []
+    _spy_first_run(monkeypatch, calls, enable=True)
+    out = sweep(world, dry_run=True)
+    assert calls == [] and world.started() == []
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "not_enabled")]
+    assert (path.read_bytes(), report.read_bytes(), report.stat().st_mtime) == before
+
+
+@pytest.mark.parametrize("step", ["label", "dry_run", "restart"])
+def test_a_failure_past_the_config_step_waits_an_hour_before_the_retry(
+    world, monkeypatch, step
+) -> None:
+    line = f"first-run: failed {step}: label_failed"
+    _disabled_beta(world, line, age_s=dispatch.RETRY_AFTER_S - 60)
+    calls: list[str] = []
+    _spy_first_run(monkeypatch, calls, enable=False)
+    sweep(world)
+    assert calls == []
+    world.report("Beta", line, age_s=dispatch.RETRY_AFTER_S + 60)
+    sweep(world)
+    assert calls == ["Beta"]
+
+
+def test_a_config_generated_in_this_sweep_is_not_retried_a_second_time(
+    world, monkeypatch
+) -> None:
+    prepare(world, ["Alpha", "Gamma"])
+    world.child("Beta")
+    calls: list[str] = []
+    _spy_first_run(monkeypatch, calls, enable=False)
+
+    def fake_ensure(repo, defs, runner, base):
+        world.config(repo.name, enabled=False)
+        world.report(repo.name, FAILED_CONFIG)
+        return Outcome("generated", repo.name, config_path=base.config_dir)
+
+    monkeypatch.setattr(dispatch, "ensure_config", fake_ensure)
+    out = sweep(world)
+    assert calls == ["Beta"]
+    assert out.generated == ("Beta",)
+
+
+def test_a_failed_retry_keeps_the_existing_store_and_lock(world) -> None:
+    world.no_worktree.add("Beta")
+    path = _disabled_beta(world, FAILED_CONFIG)
+    state = world.state_dir("Beta")
+    (state / "dispatch.json").write_text('{"kept": true}\n')
+    (state / "lock").write_text("")
+    report = state / "first-run.txt"
+    stale = report.read_text()
+    out = sweep(world)  # the real first_run runs and fails again at the config step
+    assert [(s.name, s.reason) for s in out.skipped] == [("Beta", "not_enabled")]
+    assert report.read_text() != stale and report.read_text().startswith(FAILED_CONFIG)
+    assert (state / "dispatch.json").read_text() == '{"kept": true}\n'
+    assert (state / "lock").read_text() == ""
+    assert json.loads(path.read_text())["enabled"] is False
```

Codegraph context
index_state: fresh
checked_at: 2026-11-24T02:39:04Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-751
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-751
call codegraph only when index_state: fresh, never to widen scope
Dependents not in the diff (Q2b): Test-only change to tests/issue_watch/test_dispatch.py (World.report helper, import os, appended tests). Orchestrator ran: the new retry tests fail against dispatch.py as of HEAD (6 failures) and pass with Task 2's code; full tests/issue_watch: 3030 passed; tests/issue_watch/test_security_invariants.py is not modified.

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
