e94872ee0ce7ba5d7715e716e1094ebac6844616
Review one task for spec compliance.

Task brief: ## Task 2: Add the installer-row test scaffold and the core-row tests to tests/cli/test_install_keep.py

Depends on: Task 1

In `tests/cli/test_install_keep.py` add a section parametrized by one row table, the pattern of `_INSTALLERS` in `tests/unit/test_cli_install.py:993-1005`. Each row is a pytest param with an id, the installer function, a target factory (`tmp_path` based), a victim picker, a noun and a failure-key function (core `victim.name`, agents `victim.stem`, templates `str(victim.relative_to(target))`), because the failure line starts with that key and it differs per installer. This task adds only the `core` row: call `install_core_files(target_path=t, force=f)`, target `tmp_path / ".claude"`, victim the first `*.md` in the target, noun `core file`. Write the table so that Tasks 4 and 7 add a row without changing a test.

Add these helpers, local to the section:

- `_victim_baks(victim)` returns `sorted(victim.parent.glob(victim.name + ".bak.*"))`, so a stray file in the folder cannot change a count.
- `_edit(victim)` writes `b"my own edit\n"` and returns the shipped bytes read beforehand.
- `_wrap_copy(monkeypatch, victim, fail_on, error)` replaces `install_keep.shutil.copy2` with a wrapper around the real function; it records every destination and raises `error` when `fail_on(dst)` is true. Provide two predicates: backup-only (`dst.name.startswith(victim.name + ".bak.")`) and replacement-only (`dst == victim`).
- `_freeze_clock(monkeypatch)` replaces `install_keep.datetime` with a stub whose `now(tz)` returns one fixed instant.

Add these tests, each run for every row (add `import errno` and the needed imports):

- `test_forced_install_saves_a_differing_file_then_replaces_it` (TR-001): after installing into the target, edit the victim, install again with `force=True`; the victim equals the shipped bytes, `_victim_baks` holds exactly the edited bytes, and the message contains `Saved 1 changed <noun>` and the backup path.
- `test_forced_install_of_a_matching_or_missing_file_makes_no_backup` (TR-002): a forced run over matching files, and a forced run into an empty target, succeed with no backup and no `Saved`.
- `test_a_second_forced_run_makes_no_further_backup` (TR-003): backup count stays 1.
- `test_plain_install_keeps_the_edit_and_makes_no_backup` (TR-004): bytes kept, no backup; the core message contains `differ from this version`.
- `test_core_kept_note_names_the_bak_naming` (TR-005, core row only): the message of a plain install over an edited victim contains `saved as <name>.bak.<time> first`.
- `test_failed_save_leaves_the_file_untouched` (TR-006), parametrized over `PermissionError("denied")` and `OSError(errno.ENOSPC, "No space left on device")`: use the backup-only predicate; assert the result is not ok, the message contains `<key>: could not save a copy first, left untouched` and the error text, the victim bytes are unchanged, the recorded copies to the victim number zero, and a second edited file in the same target is saved and replaced.
- `test_save_then_failed_replacement_keeps_the_backup` (TR-007): use the replacement-only predicate (the backup copy goes through); assert not ok, the backup holds the edited bytes and its path is in the saved block, and the victim is listed under `❌ Failed`; assert nothing about the victim's bytes.
- `test_backup_names_do_not_collide_on_one_instant` (TR-009): with the frozen clock, edit, force, edit, force; the second backup name ends in `-2` and each backup holds its own edit.
- `test_same_size_same_mtime_edit_is_saved_when_forced` (TR-010): rewrite the victim with `_rewrite_keeping_stat` to the same size and mtime, then force; a backup exists.
- `test_directory_at_the_victim_path_fails_closed` (spec 3.5, risk R-10): replace the victim with a directory and run with `force=True`; assert the result is not ok, the message contains `<key>: could not save a copy first, left untouched`, no `.bak.` entry exists beside it, and the directory is still there.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_keep.py -q` passes with the new tests present for the `core` row and the existing tests in the file unchanged.
- TR-006 asserts the `left untouched` wording and zero copies to the victim, so a missing `except OSError` guard in Task 1 fails it.
- Adding a row to the table is the only change needed to run every test for another installer (the table is the single place a row is defined).

AC ids:
- T2.AC1: `uv run pytest tests/cli/test_install_keep.py -q` passes with the new tests present for the `core` row and the existing tests in the file unchanged.
- T2.AC2: TR-006 asserts the `left untouched` wording and zero copies to the victim, so a missing `except OSError` guard in Task 1 fails it.
- T2.AC3: Adding a row to the table is the only change needed to run every test for another installer (the table is the single place a row is defined).
Global constraints: ## Constraints

- Scope: change only `src/superclaude/cli/install_core.py`, `install_agents.py`, `install_templates.py` (and the docstring of `install_keep.py`), tests under `tests/cli/`, the documentation files named in the tasks, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (the routing-guide copy) and `CHANGELOG.md`. Do not change `src/superclaude/cli/main.py`. Do not change the logic of `backup_if_differs`, `same_content` or `_backup_target`. Add no shared helper function and no code that deletes backups.
- Non-goals: no stale-file notes for agents and templates on a plain `install` (recorded as a follow-up), no change to skill-folder or hook-script copying, no rollback of a failed replacement, no change to `README.md:68` (a 6.0.0 section pinned to `@v6.0.0`), no change to released CHANGELOG entries, `docs/testing/`, `docs/designs/` or `docs/docs-product/`.
- Never hand-edit or stage a path under `.claude/`; regenerate the gitignored mirrors with `make sync-dev`, whose output is never staged. Edit the file under `src/superclaude/` or `plugins/` instead.
- Line numbers in the tasks are as at HEAD 3cf7e2259; locate by the quoted text if an earlier task shifted them.
- When commits are requested, make one per work package as in `./source.md` section 6: each installer's code together with its test row, and the docstring, guide copy and CHANGELOG with the documentation. `/sc:implement` itself never commits.
- The helper contract (unchanged): `backup_if_differs(shipped: Path, target: Path) -> Path | None` in `src/superclaude/cli/install_keep.py` returns `None` when the bytes match, otherwise copies `target` to `<name>.bak.<YYYYmmddTHHMMSSZ>` beside it (a `-2`, `-3` suffix while that name exists) and returns that path; it raises `OSError` when the copy fails, and the caller must then leave `target` untouched.
- Exact strings every installer uses. Saved block, printed only when `backed_up` is non-empty, after the skipped and kept notes and before the failed block: the text `\n💾 Saved {n} changed {noun}(s) before overwriting:` and then one line `   - {backup path}` per saved copy; nouns are `core file`, `agent`, `template`. Failure line, added to `failed`: `<key>: could not save a copy first, left untouched (<error>)`.
- Pattern to copy for the code tasks: `src/superclaude/cli/install_commands.py` lines 54-82 (the backup step with its own `try`/`except OSError`, then the copy `try`) and 108-113 (the saved block).
- Terms: the six backed-up categories are commands, rules, output styles, core files, agents and templates. Skill folders (deleted and re-copied) and hook scripts (`src/superclaude/cli/install_hooks.py:286-287`, a plain `shutil.copy2`) are overwritten with no copy. The word "excluded" names the `agent-memory` folder the template installer never writes.
- Documentation wording kit (use the pieces the task names; keep the wording the same in every file). W-1: "`superclaude install --force` and `superclaude update` overwrite every file they ship. When a command, rule, output-style, core, agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders (deleted and re-copied) and hook scripts get no copy." W-2: "Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either command." W-3: "Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy." W-4: "`could not save a copy first, left untouched`: the installer could not write the `.bak.` copy next to a file, because the folder is not writable, the disk is full, the file cannot be read, or a folder sits at the file's path. That file is left as it is, the run lists it under the failed files, and `superclaude install --force` or `superclaude update` exits 1. Make the folder writable or free space and run the command again, or move the file aside yourself. A `.bak.` file left behind by a failed save may be incomplete."
- Test conventions: run tests with `uv run pytest`; never `python -m` or bare `pip`. Unit tests live in `tests/cli/test_install_keep.py` (existing helpers `_baks` at line 32 and `_rewrite_keeping_stat` at line 39; existing failed-save tests at lines 144-157 and 202-214 patch `install_keep.shutil.copy2`, which is the same `shutil` module the installers call).
Start sha: e94872ee0ce7ba5d7715e716e1094ebac6844616
Diff against the start snapshot: diff --git a/tests/cli/test_install_keep.py b/tests/cli/test_install_keep.py
index 96ab7b2ba..1c9d01a42 100644
--- a/tests/cli/test_install_keep.py
+++ b/tests/cli/test_install_keep.py
@@ -11,8 +11,11 @@ installer, because only the current shipped bytes are known; both are covered.
 
 from __future__ import annotations
 
+import errno
 import os
+from datetime import datetime, timezone
 from pathlib import Path
+from typing import Callable, NamedTuple
 
 import pytest
 
@@ -212,3 +215,224 @@ def test_commands_failed_save_leaves_the_file_untouched(tmp_path: Path, monkeypa
     ok, message = install_commands(target_path=target, force=True)
     assert not ok and "left untouched" in message
     assert victim.read_text() == "my own edit\n"
+
+
+# --- core files, agents and templates (one table, one row per installer) ---------
+
+
+class _Row(NamedTuple):
+    id: str
+    install: Callable  # (target, force) -> (ok, message)
+    target: Callable  # (tmp_path) -> installer target folder
+    victims: (
+        Callable  # (target) -> sorted shipped files in the target, first is the victim
+    )
+    noun: str  # as in "Saved N changed <noun>(s)"
+    key: Callable  # (victim, target) -> name the failure line starts with
+    kept_note: bool  # a plain install names a kept file that differs
+
+
+_ROWS = {
+    row.id: row
+    for row in (
+        _Row(
+            id="core",
+            install=lambda t, f: install_core_files(target_path=t, force=f),
+            target=lambda tmp: tmp / ".claude",
+            victims=lambda t: sorted(t.glob("*.md")),
+            noun="core file",
+            key=lambda v, t: v.name,
+            kept_note=True,
+        ),
+    )
+}
+
+
+@pytest.fixture(params=list(_ROWS), ids=list(_ROWS))
+def row(request) -> _Row:
+    return _ROWS[request.param]
+
+
+def _victim_baks(victim: Path) -> list[Path]:
+    """Backups of this one file; a stray file in the folder cannot change the count."""
+    return sorted(victim.parent.glob(victim.name + ".bak.*"))
+
+
+def _edit(victim: Path) -> bytes:
+    shipped = victim.read_bytes()
+    victim.write_bytes(b"my own edit\n")
+    return shipped
+
+
+def _wrap_copy(monkeypatch, fail_on: Callable, error: Exception) -> list[Path]:
+    """Wrap the copy every installer and the helper call; record each destination and
+    raise ``error`` when ``fail_on(dst)``. Failing only the victim's copy keeps the
+    other files processable."""
+    real = install_keep.shutil.copy2
+    seen: list[Path] = []
+
+    def wrapper(src, dst, *args, **kwargs):
+        seen.append(Path(dst))
+        if fail_on(Path(dst)):
+            raise error
+        return real(src, dst, *args, **kwargs)
+
+    monkeypatch.setattr(install_keep.shutil, "copy2", wrapper)
+    return seen
+
+
+def _backup_only(victim: Path) -> Callable:
+    return lambda dst: dst.name.startswith(victim.name + ".bak.")
+
+
+def _replacement_only(victim: Path) -> Callable:
+    return lambda dst: dst == victim
+
+
+def _freeze_clock(monkeypatch) -> None:
+    class _Frozen:
+        @staticmethod
+        def now(tz=None):
+            return datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
+
+    monkeypatch.setattr(install_keep, "datetime", _Frozen)
+
+
+def _installed_target(row: _Row, tmp_path: Path) -> tuple[Path, Path]:
+    target = row.target(tmp_path)
+    ok, message = row.install(target, False)
+    assert ok, message
+    return target, row.victims(target)[0]
+
+
+def test_forced_install_saves_a_differing_file_then_replaces_it(row, tmp_path):
+    target, victim = _installed_target(row, tmp_path)
+    shipped = _edit(victim)
+    ok, message = row.install(target, True)
+    assert ok, message
+    assert victim.read_bytes() == shipped
+    baks = _victim_baks(victim)
+    assert [b.read_bytes() for b in baks] == [b"my own edit\n"]
+    assert f"Saved 1 changed {row.noun}" in message and str(baks[0]) in message
+    # a saved file still counts as installed (FR-042)
+    assert f"   - {row.key(victim, target)}" in message.split("💾")[0]
+
+
+def test_forced_install_of_a_matching_or_missing_file_makes_no_backup(row, tmp_path):
+    target = row.target(tmp_path)
+    ok, message = row.install(target, True)  # empty target: nothing to save
+    assert ok, message
+    assert "Saved" not in message
+    ok, message = row.install(target, True)  # every file matches
+    assert ok, message
+    assert "Saved" not in message
+    assert not list(target.rglob("*.bak.*"))
+
+
+def test_a_second_forced_run_makes_no_further_backup(row, tmp_path):
+    target, victim = _installed_target(row, tmp_path)
+    _edit(victim)
+    assert row.install(target, True)[0]
+    ok, message = row.install(target, True)
+    assert ok, message
+    assert "Saved" not in message
+    assert len(_victim_baks(victim)) == 1
+
+
+def test_plain_install_keeps_the_edit_and_makes_no_backup(row, tmp_path):
+    target, victim = _installed_target(row, tmp_path)
+    _edit(victim)
+    ok, message = row.install(target, False)
+    assert ok, message
+    assert victim.read_bytes() == b"my own edit\n"
+    assert not _victim_baks(victim)
+    assert ("differ from this version" in message) == row.kept_note
+    if not row.kept_note:
+        assert "differ" not in message
+
+
+def test_core_kept_note_names_the_bak_naming(tmp_path):
+    row = _ROWS["core"]
+    target, victim = _installed_target(row, tmp_path)
+    _edit(victim)
+    ok, message = row.install(target, False)
+    assert ok, message
+    assert "saved as <name>.bak.<time> first" in message
+
+
+@pytest.mark.parametrize(
+    "error",
+    [PermissionError("denied"), OSError(errno.ENOSPC, "No space left on device")],
+    ids=["permission", "enospc"],
+)
+def test_failed_save_leaves_the_file_untouched(row, tmp_path, monkeypatch, error):
+    target, victim = _installed_target(row, tmp_path)
+    second = row.victims(target)[1]
+    second_shipped = _edit(second)
+    _edit(victim)
+    seen = _wrap_copy(monkeypatch, _backup_only(victim), error)
+    ok, message = row.install(target, True)
+    assert not ok
+    assert (
+        f"{row.key(victim, target)}: could not save a copy first, left untouched"
+        in message
+    )
+    assert str(error) in message
+    assert victim.read_bytes() == b"my own edit\n"
+    assert [d for d in seen if d == victim] == []  # the replacement was never attempted
+    assert not _victim_baks(victim)
+    # another file in the same run is saved and replaced
+    assert second.read_bytes() == second_shipped
+    assert [b.read_bytes() for b in _victim_baks(second)] == [b"my own edit\n"]
+
+
+def test_save_then_failed_replacement_keeps_the_backup(row, tmp_path, monkeypatch):
+    target, victim = _installed_target(row, tmp_path)
+    _edit(victim)
+    _wrap_copy(monkeypatch, _replacement_only(victim), OSError("boom"))
+    ok, message = row.install(target, True)
+    assert not ok
+    baks = _victim_baks(victim)
+    assert [b.read_bytes() for b in baks] == [b"my own edit\n"]
+    before_failed, failed_block = message.split("❌ Failed", 1)
+    assert "💾 Saved" in before_failed  # the saved block comes before the failed block
+    assert str(baks[0]) in before_failed.split("💾 Saved", 1)[1]
+    assert f"{row.key(victim, target)}: boom" in failed_block
+
+
+def test_backup_names_do_not_collide_on_one_instant(row, tmp_path, monkeypatch):
+    target, victim = _installed_target(row, tmp_path)
+    _freeze_clock(monkeypatch)
+    victim.write_bytes(b"first edit\n")
+    assert row.install(target, True)[0]
+    victim.write_bytes(b"second edit\n")
+    assert row.install(target, True)[0]
+    first, second = _victim_baks(victim)
+    assert second.name == first.name + "-2"
+    assert first.read_bytes() == b"first edit\n"
+    assert second.read_bytes() == b"second edit\n"
+
+
+def test_same_size_same_mtime_edit_is_saved_when_forced(row, tmp_path):
+    target, victim = _installed_target(row, tmp_path)
+    shipped = victim.read_bytes()
+    assert shipped
+    _rewrite_keeping_stat(victim, "z" * len(shipped))
+    ok, message = row.install(target, True)
+    assert ok, message
+    assert victim.read_bytes() == shipped
+    assert [b.read_bytes() for b in _victim_baks(victim)] == [b"z" * len(shipped)]
+
+
+def test_directory_at_the_victim_path_fails_closed(row, tmp_path):
+    target, victim = _installed_target(row, tmp_path)
+    victim.unlink()
+    victim.mkdir()
+    ok, message = row.install(target, True)
+    assert not ok
+    assert (
+        f"{row.key(victim, target)}: could not save a copy first, left untouched"
+        in message
+    )
+    assert victim.is_dir()
+    assert not _victim_baks(victim)

Task-owned evidence artifact artifacts/t2-test.log (a log the task wrote; cite it as ./artifacts/t2-test.log:<line>):
1: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py -q
2: 
3: tests/cli/test_install_keep.py ...........................               [100%]
4: 
5: ============================== 27 passed in 1.10s ==============================
6: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: the task adds only test code under tests/cli/test_install_keep.py (no production symbol changed); the dependents of the helpers it uses are install_core_files (Task 1, already complete) and install_keep helpers (unchanged). The ordering and key facts it relies on: install_core.py failure key is the file name (install_core.py:84-86).
Delta diff from the previous reviewed tree (empty on the first review): TR-007 (test_save_then_failed_replacement_keeps_the_backup) now splits the message at the failed block and checks the backup path inside the saved block and the failure line inside the failed block; nothing else changed.
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=tests/cli/test_install_keep.py:397 anchor="its path is in the saved block, and the victim is listed under `❌ Failed`" chk=n,n,n,y family=test-assert-scope fix=split the message at "💾 Saved" and "❌ Failed"; assert the backup path appears in the saved-block slice and the failure line in the slice after "❌ Failed" first=A1 origin=new: TR-007 checks the backup path and the failure line against the whole message and only the order of the two blocks.
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
