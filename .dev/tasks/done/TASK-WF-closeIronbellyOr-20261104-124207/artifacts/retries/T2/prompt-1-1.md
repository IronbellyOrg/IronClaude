ecee3366c69f7b2a73586a350a84c3d4cb9b3b79
Review one task for spec compliance.

Task brief: ## Task 2: Report plugin install failures by plugin id or marketplace repo

Depends on: Task 1

Fix the shared failure label in `install_plugins` in `src/superclaude/cli/install_user_setup.py` (FR-005, Design 3.2). Today an install command is `["plugin", "install", p, "--scope", "user", "-y"]`, so `args[3]` is `"--scope"`: the non-zero-exit and exception paths (`:303`, `:305`) append `--scope`, and the time-limit path (`:292`) builds `install <p> --scope (time limit)`. Compute one name per command (the repo for a `marketplace add`, `args[3]`; the plugin id for an `install`, `args[2]`) and use it in all three places, the time-limit one as `f"{name} (time limit)"`. At most 5 changed lines; `ok` stays `True` on every path; no other change to the function.

In `tests/cli/test_install_user_setup.py`:
- T5: extend `test_plugin_failures_and_time_limit_never_fail_install` (`:229-242`, its `playwright`-only fixture). Non-zero-exit leg: `ok is True`, message contains `anthropics/claude-plugins-official` and `playwright@claude-plugins-official`, and `"--scope" not in message`. `deadline=0` leg: `ok is True`, message contains `(time limit)` and the same two names, and `"--scope" not in message`.
- T5c: new test that monkeypatches `setup.shutil.which` to return `None` and asserts `setup.install_plugins(home=tmp_path) == (True, "⏭️  Plugins: claude CLI not found; skipped")` (two spaces after the emoji, as at `install_user_setup.py:258`).

Acceptance criteria:
- `git diff src/superclaude/cli/install_user_setup.py` changes at most 5 lines, all inside `install_plugins`.
- A failed plugin install is reported as e.g. `⚠️  Plugins: not installed: DietrichGebert/ponytail, ponytail@ponytail; rerun ...` (never `--scope`); T5 fails on the unfixed code and passes after the fix.
- T5c passes.
- `uv run pytest tests/cli/test_install_user_setup.py tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py tests/unit/test_cli_install.py -v` passes, `make lint` is clean and `uv run ruff format --check src/ tests/` reports no change; output saved to `./artifacts/t2-tests.log`.

AC ids: T2.AC1,T2.AC2,T2.AC3,T2.AC4 (in the order of the Acceptance criteria bullets)
Global constraints: ## Constraints

- Change only `src/superclaude/cli/user_settings_defaults.json`, `src/superclaude/cli/install_user_setup.py` (at most 5 changed lines, failure label only), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md` and `CHANGELOG.md`. No change to `main.py`, `update.sh`, `doctor.py`, output styles, rules, hooks, any skill, command or agent, or any `.claude/` file.
- Never run `superclaude install`, `superclaude update`, `./update.sh` or `claude plugin ...` against this workspace's `~/.claude`; any manual proof uses a throwaway `HOME` under `/tmp` that is removed afterwards.
- No `pluginConfigs` entry, no `statusLine` setting, no write outside `~/.claude`, no version pin, no new module, constant, flag or CLI option.
- A user's existing `enabledPlugins`, `env` and marketplace values are never changed.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); never stage `.claude/` paths.
- The superseded package `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/` and `.dev/reflect/pre-closeIronbellyOr-20261104084538/` stay on disk untouched.
Start sha: ecee3366c69f7b2a73586a350a84c3d4cb9b3b79
Diff against the start snapshot: diff --git a/src/superclaude/cli/install_user_setup.py b/src/superclaude/cli/install_user_setup.py
index ad0e8efe..d9d11fec 100644
--- a/src/superclaude/cli/install_user_setup.py
+++ b/src/superclaude/cli/install_user_setup.py
@@ -287,9 +287,10 @@ def install_plugins(
 
     failed = []
     for args in commands:
+        name = args[3] if args[1] == "marketplace" else args[2]
         remaining = deadline - time.monotonic()
         if remaining < 2:
-            failed.append(" ".join(args[1:3]) + f" {args[3]} (time limit)")
+            failed.append(f"{name} (time limit)")
             continue
         try:
             result = subprocess.run(
@@ -300,9 +301,9 @@ def install_plugins(
                 stdin=subprocess.DEVNULL,
             )
             if result.returncode != 0:
-                failed.append(args[3])
+                failed.append(name)
         except (OSError, subprocess.SubprocessError):
-            failed.append(args[3])
+            failed.append(name)
     if failed:
         return True, (
             f"⚠️  Plugins: not installed: {', '.join(failed)}; "
diff --git a/tests/cli/test_install_user_setup.py b/tests/cli/test_install_user_setup.py
index 394f530d..ba43348f 100644
--- a/tests/cli/test_install_user_setup.py
+++ b/tests/cli/test_install_user_setup.py
@@ -312,10 +312,23 @@ def test_plugin_failures_and_time_limit_never_fail_install(
         "run",
         lambda command, **k: subprocess.CompletedProcess(command, 1, "", "boom"),
     )
+    names = ("anthropics/claude-plugins-official", "playwright@claude-plugins-official")
     ok, message = setup.install_plugins(home=home)
     assert ok and message.startswith("⚠️  Plugins")
+    assert all(name in message for name in names), message
+    assert "--scope" not in message
     ok, message = setup.install_plugins(home=home, deadline=0)
     assert ok and "time limit" in message
+    assert all(f"{name} (time limit)" in message for name in names), message
+    assert "--scope" not in message
+
+
+def test_plugins_skip_when_claude_cli_is_absent(tmp_path: Path, monkeypatch) -> None:
+    monkeypatch.setattr(setup.shutil, "which", lambda _name: None)
+    assert setup.install_plugins(home=tmp_path) == (
+        True,
+        "⏭️  Plugins: claude CLI not found; skipped",
+    )
 
 
 def test_shipped_setup_contains_no_personal_home_paths() -> None:

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
