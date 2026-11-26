320c34db4c5d46214b6de94872a71fa197ae2e15
Review one task for spec compliance.

Task brief: ## Task 9: Add the stub-row and forwarded-flag tests for install --force and update

In `tests/cli/test_update_command.py`, add a recording variant of `_stub_installers` (line 74; the existing `fake` at lines 80-84 ignores keyword arguments) that stores the `force` keyword each fake installer receives. Add a test for TR-016, parametrized over `failing` in `install_core_files`, `install_agents`, `install_templates` and over the command `["install", "--force"]` and `["update"]`: the exit code is 1 and `"<name> result"` appears in the output (the pattern of `test_update_propagates_hook_install_failure` at line 118). Add assertions on the forwarded flag: with `["install"]` the three installers receive `force=False`; with `["install", "--force"]` and `["update"]` they receive `force=True`.

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py -q` passes with the new tests present.
- A change of `main.py` that stopped forwarding the flag (`main.py:180,198,229` for `install`, `383,396,417` for `update`) would fail the forwarded-flag assertions.
- The existing `_stub_installers` helper and its callers are unchanged.

AC ids:
- T9.AC1: `uv run pytest tests/cli/test_update_command.py -q` passes with the new tests present.
- T9.AC2: A change of `main.py` that stopped forwarding the flag (`main.py:180,198,229` for `install`, `383,396,417` for `update`) would fail the forwarded-flag assertions.
- T9.AC3: The existing `_stub_installers` helper and its callers are unchanged.
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
Start sha: 320c34db4c5d46214b6de94872a71fa197ae2e15
Diff against the start snapshot: diff --git a/tests/cli/test_update_command.py b/tests/cli/test_update_command.py
index 59b983232..ba9e3b56d 100644
--- a/tests/cli/test_update_command.py
+++ b/tests/cli/test_update_command.py
@@ -278,6 +278,59 @@ def test_install_force_target_do_not_redirect(monkeypatch, isolated_home_guard):
     }
 
 
+_FORCED_INSTALLERS = (
+    "superclaude.cli.install_core.install_core_files",
+    "superclaude.cli.install_agents.install_agents",
+    "superclaude.cli.install_templates.install_templates",
+)
+
+
+def _stub_installers_recording_force(monkeypatch, *, failing: str | None = None):
+    """Like ``_stub_installers``, but the core, agent and template fakes also record the
+    ``force`` keyword they receive (the plain fake ignores keyword arguments)."""
+    _stub_installers(monkeypatch, failing=failing)
+    forced: dict[str, object] = {}
+    for path in _FORCED_INSTALLERS:
+        name = path.rsplit(".", 1)[-1]
+
+        def fake(*args, _name=name, **kwargs):
+            forced[_name] = kwargs.get("force")
+            return (_name != failing, f"{_name} result")
+
+        monkeypatch.setattr(path, fake)
+    return forced
+
+
+@pytest.mark.parametrize("command", [["install", "--force"], ["update"]])
+@pytest.mark.parametrize(
+    "failing", [path.rsplit(".", 1)[-1] for path in _FORCED_INSTALLERS]
+)
+def test_failed_core_agent_or_template_install_exits_nonzero(
+    monkeypatch, command, failing
+):
+    _stub_installers_recording_force(monkeypatch, failing=failing)
+    result = CliRunner().invoke(main, command)
+    assert result.exit_code == 1, result.output
+    assert f"{failing} result" in result.output
+
+
+@pytest.mark.parametrize(
+    ("command", "expected"),
+    [(["install"], False), (["install", "--force"], True), (["update"], True)],
+)
+def test_force_reaches_the_core_agent_and_template_installers(
+    monkeypatch, command, expected
+):
+    forced = _stub_installers_recording_force(monkeypatch)
+    result = CliRunner().invoke(main, command)
+    assert result.exit_code == 0, result.output
+    assert forced == {
+        "install_core_files": expected,
+        "install_agents": expected,
+        "install_templates": expected,
+    }
+
+
 def _victim_baks(victim: Path) -> list[Path]:
     """Saved copies of this one file. Never count ``~/.claude`` as a whole: the hook
     installer writes ``settings.json.bak.<stamp>`` there on every run."""

Task-owned evidence artifact artifacts/t9-test.log (a log the task wrote; cite it as ./artifacts/t9-test.log:<line>):
1: $ MUTATION CHECK: main.py:180 changed from install_core_files(force=force) to install_core_files(force=False) (temporary, restored afterwards)
2: $ uv run pytest -p no:cacheprovider tests/cli/test_update_command.py -q -k force_reaches
3: E   AssertionError: assert {'install_cor...plates': True} == {'install_cor...plates': True}
4: E     
5: (the test then fails on: install_core_files False != True for install --force)
6: main.py restored byte-identical (cmp against the saved copy; git diff --stat -- src/superclaude/cli/main.py is empty)
7: 
8: $ uv run pytest -p no:cacheprovider tests/cli/test_update_command.py -q
9: tests/cli/test_update_command.py ...............................         [100%]
10: 
11: ============================== 31 passed in 2.57s ==============================
12: 
13: $ uv run pytest -p no:cacheprovider tests/cli/test_update_command.py -v -k "force_reaches or failed_core_agent"
14: test_failed_core_agent_or_template_install_exits_nonzero[install_core_files-command0] PASSED [ 11%]
15: test_failed_core_agent_or_template_install_exits_nonzero[install_core_files-command1] PASSED [ 22%]
16: test_failed_core_agent_or_template_install_exits_nonzero[install_agents-command0] PASSED [ 33%]
17: test_failed_core_agent_or_template_install_exits_nonzero[install_agents-command1] PASSED [ 44%]
18: test_failed_core_agent_or_template_install_exits_nonzero[install_templates-command0] PASSED [ 55%]
19: test_failed_core_agent_or_template_install_exits_nonzero[install_templates-command1] PASSED [ 66%]
20: test_force_reaches_the_core_agent_and_template_installers[command0-False] PASSED [ 77%]
21: test_force_reaches_the_core_agent_and_template_installers[command1-True] PASSED [ 88%]
22: test_force_reaches_the_core_agent_and_template_installers[command2-True] PASSED [100%]
23: ======================= 9 passed, 22 deselected in 0.99s =======================
24: 
25: removed lines in the diff of the test file: 0
26: _stub_installers definition unchanged: 0
27: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: test-only change in tests/cli/test_update_command.py. src/superclaude/cli/main.py was edited once and restored byte-identical for the mutation check in ./artifacts/t9-test.log (git diff --stat -- src/superclaude/cli/main.py is empty), so it is not in the diff. The tests rely on the call sites main.py:180,198,229 (install) and 383,396,417 (update), which pass force by keyword.
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
