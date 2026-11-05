b64ad96f65deb163f196730f5d5457d6baa87d37
Review one task for spec compliance.

Task brief: ## Task 4: Isolate the install and update tests that run ccsession from the developer's shell

Source requirement: because the exit-2 check runs on every `ccsession` call, a bad `CCSESSION_PERMISSIONS` exported in a developer's shell would make other tests that run `ccsession` with the inherited environment fail. Work in two files.

- In `tests/unit/test_install_ccsession.py`, add an autouse fixture that deletes `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` with `monkeypatch.delenv(..., raising=False)`. It covers `test_wire_moves_names_saved_per_folder_into_the_repo_list` (the install step runs `ccsession --migrate-names` with the inherited environment) and `test_wire_symlink_runs_help` (runs `ccsession --help` with `**os.environ` and `check=True`).
- In `tests/cli/test_update_command.py`, add the same autouse fixture next to the existing autouse fixture of that file. It covers `test_real_install_launches_ccsession`, which runs the installed `ccsession --help` with `**os.environ` and `check=True`.

Acceptance criteria:
- With `CCSESSION_PERMISSIONS=typo` and `CC_CLAUDE_FLAGS=--verbose` exported, `uv run pytest tests/unit/test_install_ccsession.py tests/cli/test_update_command.py -q` passes on the unchanged launcher. This run is a smoke check only (the unchanged launcher ignores the variable, so it passes with or without the fixtures); the proof that the fixtures isolate the tests is the Task 5 isolation log on the changed launcher.
- Each of the two files has exactly one new autouse fixture and no other behavior change.

AC ids (in source order):
T4.AC1: With `CCSESSION_PERMISSIONS=typo` and `CC_CLAUDE_FLAGS=--verbose` exported, `uv run pytest tests/unit/test_install_ccsession.py tests/cli/test_update_command.py -q` passes on the unchanged launcher. This run is a smoke check only (the unchanged launcher ignores the variable, so it passes with or without the fixtures); the proof that the fixtures isolate the tests is the Task 5 isolation log on the changed launcher.
T4.AC2: Each of the two files has exactly one new autouse fixture and no other behavior change.
Global constraints: ## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.
Start sha: b64ad96f65deb163f196730f5d5457d6baa87d37
Diff against the start snapshot: 
diff --git a/tests/unit/test_install_ccsession.py b/tests/unit/test_install_ccsession.py
index f241a763..2f359e73 100644
--- a/tests/unit/test_install_ccsession.py
+++ b/tests/unit/test_install_ccsession.py
@@ -11,6 +11,18 @@ import pytest
 from superclaude.cli.install_ccsession import wire_ccsession
 
 
+@pytest.fixture(autouse=True)
+def _no_ccsession_permission_env(monkeypatch):
+    """Keep the developer's shell out of every ccsession run in this file.
+
+    The install step (``ccsession --migrate-names``) and the symlink tests run
+    ccsession with the inherited environment, and ccsession exits 2 on a bad
+    CCSESSION_PERMISSIONS (and CC_CLAUDE_FLAGS would change its launch flags).
+    """
+    monkeypatch.delenv("CCSESSION_PERMISSIONS", raising=False)
+    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
+
+
 @pytest.fixture
 def home(tmp_path):
     skill = tmp_path / ".claude/skills/ccsession-tag"

diff --git a/tests/cli/test_update_command.py b/tests/cli/test_update_command.py
index df2ade09..b5e2f184 100644
--- a/tests/cli/test_update_command.py
+++ b/tests/cli/test_update_command.py
@@ -54,6 +54,18 @@ def isolated_home_guard(tmp_path, monkeypatch):
     return state
 
 
+@pytest.fixture(autouse=True)
+def _no_ccsession_permission_env(monkeypatch):
+    """Keep the developer's shell out of the real ccsession run.
+
+    ``test_real_install_launches_ccsession`` runs the installed ccsession with the
+    inherited environment, and ccsession exits 2 on a bad CCSESSION_PERMISSIONS
+    (and CC_CLAUDE_FLAGS would change its launch flags).
+    """
+    monkeypatch.delenv("CCSESSION_PERMISSIONS", raising=False)
+    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
+
+
 def _stub_installers(monkeypatch, *, failing: str | None = None):
     calls: list[str] = []
 

diff --git a/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t4-smoke.log b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t4-smoke.log
new file mode 100644
index 00000000..dc631bca
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t4-smoke.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-390
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 42 items
+
+tests/unit/test_install_ccsession.py ......................              [ 52%]
+tests/cli/test_update_command.py ....................                    [100%]
+
+============================== 42 passed in 1.96s ==============================
+rc=0

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
