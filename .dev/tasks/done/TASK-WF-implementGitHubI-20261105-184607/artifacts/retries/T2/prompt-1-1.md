98fea712edea9ddacd8152084b5229bbc89781f5
Review one task for spec compliance.

Task brief: ## Task 2: Add the ccsession-orca print-mode test to tests/unit/test_ccsession_tag.py

Depends on: Task 1

Source requirement: shim routing is kept when the variable is set, on the path the Coder wrapper actually uses (`ccsession-orca -p ...`, which hands off to `ccsession --shim --claude-args`), and the variable stays exported. Work in `tests/unit/test_ccsession_tag.py`, next to `test_orca_print_mode_is_untagged_and_never_asked`, using its `_orca_no_tty(tmp_path, *args, **extra)` helper, whose record holds `argv`, `base_url` and `env_names`.

- Add a test named `test_orca_print_mode_permissions_default_keeps_shim_routing` that runs `_orca_no_tty(tmp_path, "-p", "hello")` once without the variable (control) and once with `CCSESSION_PERMISSIONS="default"` (passed as an extra environment value). Both calls may share one `tmp_path`: each returns its own parsed `record.json` before the next call overwrites it.

Acceptance criteria:
- The control run records `argv == [*ORCA_FLAGS, "-p", "hello"]` and the opted-in run records `argv == ["--allowedTools=Grep", "-p", "hello"]`.
- Both records pass the existing `_assert_through_shim(record)` helper (`base_url == "http://127.0.0.1:4555"` and one credential set), proving shim routing is kept.
- The opted-in record's `env_names` contains `CCSESSION_PERMISSIONS` and the control record's does not, proving the variable stays exported to Claude.
- Saved output of `uv run pytest tests/unit/test_ccsession_tag.py -k orca_print_mode_permissions -q` against the unchanged launcher is in `./artifacts/t2-red.log` and shows this test failing on the argument list.

AC ids (in source order):
T2.AC1: The control run records `argv == [*ORCA_FLAGS, "-p", "hello"]` and the opted-in run records `argv == ["--allowedTools=Grep", "-p", "hello"]`.
T2.AC2: Both records pass the existing `_assert_through_shim(record)` helper (`base_url == "http://127.0.0.1:4555"` and one credential set), proving shim routing is kept.
T2.AC3: The opted-in record's `env_names` contains `CCSESSION_PERMISSIONS` and the control record's does not, proving the variable stays exported to Claude.
T2.AC4: Saved output of `uv run pytest tests/unit/test_ccsession_tag.py -k orca_print_mode_permissions -q` against the unchanged launcher is in `./artifacts/t2-red.log` and shows this test failing on the argument list.
Global constraints: ## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.
Start sha: 98fea712edea9ddacd8152084b5229bbc89781f5
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index d5b874a9..279a7d81 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -2949,6 +2949,24 @@ def test_orca_print_mode_is_untagged_and_never_asked(
     assert record["argv"] == [*ORCA_FLAGS, *args]
 
 
+def test_orca_print_mode_permissions_default_keeps_shim_routing(
+    tmp_path: Path,
+) -> None:
+    # The path the Coder wrapper uses: ccsession-orca -p ... hands off to
+    # ccsession --shim. The opt-in drops only the bypass flag; the shim and its
+    # credentials stay, and the variable stays exported to Claude (nested launches).
+    _, control = _orca_no_tty(tmp_path, "-p", "hello")
+    _, opted_in = _orca_no_tty(
+        tmp_path, "-p", "hello", CCSESSION_PERMISSIONS="default"
+    )
+    assert control["argv"] == [*ORCA_FLAGS, "-p", "hello"]
+    assert opted_in["argv"] == ["--allowedTools=Grep", "-p", "hello"]
+    _assert_through_shim(control)
+    _assert_through_shim(opted_in)
+    assert "CCSESSION_PERMISSIONS" in opted_in["env_names"]
+    assert "CCSESSION_PERMISSIONS" not in control["env_names"]
+
+
 @pytest.mark.parametrize(
     "args",
     [("--version",), ("-h",), ("mcp", "list"), ("doctor",)],

diff --git a/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t2-red.log b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t2-red.log
new file mode 100644
index 00000000..e083670d
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t2-red.log
@@ -0,0 +1,23 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-390
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 276 items / 275 deselected / 1 selected
+
+tests/unit/test_ccsession_tag.py F                                       [100%]
+
+=================================== FAILURES ===================================
+_________ test_orca_print_mode_permissions_default_keeps_shim_routing __________
+tests/unit/test_ccsession_tag.py:2963: in test_orca_print_mode_permissions_default_keeps_shim_routing
+    assert opted_in["argv"] == ["--allowedTools=Grep", "-p", "hello"]
+E   AssertionError: assert ['--dangerous...'-p', 'hello'] == ['--allowedTo...'-p', 'hello']
+E     
+E     At index 0 diff: '--dangerously-skip-permissions' != '--allowedTools=Grep'
+E     Left contains one more item: 'hello'
+E     Use -v to get more diff
+=========================== short test summary info ============================
+FAILED tests/unit/test_ccsession_tag.py::test_orca_print_mode_permissions_default_keeps_shim_routing
+====================== 1 failed, 275 deselected in 1.20s =======================
+rc=1

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

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
