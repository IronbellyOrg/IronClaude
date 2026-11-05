eb88958b2256539003623d17084b7d08f2494d57
Review one task for spec compliance.

Task brief: ## Task 5: Add the CCSESSION_PERMISSIONS switch and its --help text to src/superclaude/skills/ccsession-tag/ccsession

Depends on: Task 1, Task 2, Task 3, Task 4

Source requirement: when `CCSESSION_PERMISSIONS=default` is set, no permission-bypass flag on any launch; unset is unchanged; empty `CC_CLAUDE_FLAGS` handling is unchanged; the variable is documented where ccsession documents its other variables (the header printed by `ccsession --help`). Make both edits in this one task so the tests of Task 1 pass together at its end.

Edit (a), the flag-default block. Replace the single assignment `CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:---dangerously-skip-permissions --allowedTools=Grep}"` (line 124) with a `case` on `"${CCSESSION_PERMISSIONS:-}"` that picks the default flag string, then keeps the existing `:-` expansion:

```
case "${CCSESSION_PERMISSIONS:-}" in
  "") _cc_default_flags="--dangerously-skip-permissions --allowedTools=Grep" ;;
  default) _cc_default_flags="--allowedTools=Grep" ;;
  *) echo "ccsession: CCSESSION_PERMISSIONS must be 'default' or unset (got '$CCSESSION_PERMISSIONS')" >&2; exit 2 ;;
esac
CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:-$_cc_default_flags}"
```

The six `exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ...` launch lines (around lines 1799 to 1868) already expand the variable and are not edited. The variable is not unset before any `exec`.

Edit (b), the header text. `ccsession --help` prints the header only up to the first line that starts with `# The wrapper always runs` (line 109; `show_help` at line 1652), so the new text goes above it. Do not edit `show_help`.
- Add a usage entry in the same format as its neighbours, directly before the `ccsession --refresh-models` entry (line 99) and after the line `In tier mode --profile is not used and the shim is always on.`, outside the Coder-workspaces tier block: `CCSESSION_PERMISSIONS=default ccsession <topic>`, with continuation lines saying it starts Claude without `--dangerously-skip-permissions` (only `--allowedTools=Grep` is added), that shim and tier routing are unchanged, that any other non-empty value exits 2 on every `ccsession` call including `--help`, that it is read from the shell environment and not from `~/.claude/ccsession.env`, that it stays exported to nested launches, and that flags the caller passes and a `CC_CLAUDE_FLAGS` set in the shell or in the env file still apply. The text must not contain the strings `--tier tier`, `--tier tier0` or `--tier tier1a`: existing help tests assert they are absent outside tier mode.
- Reword the sentence at lines 109 to 114 so it stays true, keeping its first words: `# The wrapper always runs claude with --allowedTools=Grep and, unless CCSESSION_PERMISSIONS=default is set, with --dangerously-skip-permissions.` Keep the existing explanation of why `--allowedTools=Grep` is kept and the note about the `=` form.

Acceptance criteria:
- `bash -n src/superclaude/skills/ccsession-tag/ccsession` reports no syntax error.
- `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/unit/test_install_ccsession.py tests/cli/test_update_command.py -q` passes completely, with the output saved to `./artifacts/t5-green.log`; every test that failed in the red logs of Tasks 1 to 3 now passes, the help test included.
- The same four files pass with `CCSESSION_PERMISSIONS=typo` and `CC_CLAUDE_FLAGS=--verbose` exported in the shell (output in `./artifacts/t5-isolation.log`), proving Tasks 1, 3 and 4 isolate the suite.
- `grep -n '^# The wrapper always runs' src/superclaude/skills/ccsession-tag/ccsession` finds exactly one line, and `git diff` shows no change to the `show_help` function and no change to any launch line; the `${CC_CLAUDE_FLAGS:-...}` expansion is kept as written (an empty value still takes the default); the only changed regions are the flag-default block and the header comment above `show_help`.

AC ids (in source order):
T5.AC1: `bash -n src/superclaude/skills/ccsession-tag/ccsession` reports no syntax error.
T5.AC2: `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/unit/test_install_ccsession.py tests/cli/test_update_command.py -q` passes completely, with the output saved to `./artifacts/t5-green.log`; every test that failed in the red logs of Tasks 1 to 3 now passes, the help test included.
T5.AC3: The same four files pass with `CCSESSION_PERMISSIONS=typo` and `CC_CLAUDE_FLAGS=--verbose` exported in the shell (output in `./artifacts/t5-isolation.log`), proving Tasks 1, 3 and 4 isolate the suite.
T5.AC4: `grep -n '^# The wrapper always runs' src/superclaude/skills/ccsession-tag/ccsession` finds exactly one line, and `git diff` shows no change to the `show_help` function and no change to any launch line; the `${CC_CLAUDE_FLAGS:-...}` expansion is kept as written (an empty value still takes the default); the only changed regions are the flag-default block and the header comment above `show_help`.
Global constraints: ## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.
Start sha: eb88958b2256539003623d17084b7d08f2494d57
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index 2f443f04..bf4ec5ac 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -96,6 +96,16 @@
 #   CCSESSION_SHOW_ALL_MODELS=1 ccsession <topic>
 #                             Also list the tier models one by one in /model
 #   In tier mode --profile is not used and the shim is always on.
+#   CCSESSION_PERMISSIONS=default ccsession <topic>
+#                             Start Claude without --dangerously-skip-permissions
+#                             (only --allowedTools=Grep is added); the shim and the
+#                             tier models are unchanged. Any other non-empty value
+#                             exits 2 on every ccsession call, --help included. Read
+#                             from the shell environment, not from
+#                             ~/.claude/ccsession.env; stays exported to nested
+#                             launches. Flags you pass to Claude, and a
+#                             CC_CLAUDE_FLAGS set in the shell or the env file,
+#                             still apply
 #   ccsession --refresh-models
 #                             Check now for the latest profiles and model list
 #   ccsession --models-status Show which model data is in use and when it was checked
@@ -106,8 +116,9 @@
 # ~/.cache/ccsession/). Private add-on profiles skip it; set
 # CCSESSION_MODELS_REFRESH=0 to skip it everywhere.
 #
-# The wrapper always runs claude with --dangerously-skip-permissions and
-# --allowedTools=Grep. On macOS, Linux, and WSL, Claude Code leaves the Grep and
+# The wrapper always runs claude with --allowedTools=Grep and, unless
+# CCSESSION_PERMISSIONS=default is set, with --dangerously-skip-permissions.
+# On macOS, Linux, and WSL, Claude Code leaves the Grep and
 # Glob tools out by default. Naming either one in --allowedTools when the
 # session starts brings both back; a settings-file allow rule does not. Keep the
 # = form: a bare --allowedTools takes the next arguments as tool names.
@@ -121,7 +132,12 @@
 set -e
 
 CLAUDE_BIN="${CLAUDE_BIN:-claude}"
-CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:---dangerously-skip-permissions --allowedTools=Grep}"
+case "${CCSESSION_PERMISSIONS:-}" in
+  "") _cc_default_flags="--dangerously-skip-permissions --allowedTools=Grep" ;;
+  default) _cc_default_flags="--allowedTools=Grep" ;;
+  *) echo "ccsession: CCSESSION_PERMISSIONS must be 'default' or unset (got '$CCSESSION_PERMISSIONS')" >&2; exit 2 ;;
+esac
+CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:-$_cc_default_flags}"
 # Extra Claude Code arguments for this launch (tier mode: per-model settings).
 CC_SETTINGS_ARGS=()
 PROJECTS_DIR="$HOME/.claude/projects"

diff --git a/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t5-green.log b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t5-green.log
new file mode 100644
index 00000000..20d6f319
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t5-green.log
@@ -0,0 +1,21 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-390
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 455 items
+
+tests/unit/test_ccsession_tag.py ....................................... [  8%]
+........................................................................ [ 24%]
+........................................................................ [ 40%]
+........................................................................ [ 56%]
+.....................                                                    [ 60%]
+tests/unit/test_ccsession_tiers.py ..................................... [ 68%]
+........................................................................ [ 84%]
+............................                                             [ 90%]
+tests/unit/test_install_ccsession.py ......................              [ 95%]
+tests/cli/test_update_command.py ....................                    [100%]
+
+======================= 455 passed in 263.28s (0:04:23) ========================
+rc=0

diff --git a/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t5-isolation.log b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t5-isolation.log
new file mode 100644
index 00000000..ac9c4a1d
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t5-isolation.log
@@ -0,0 +1,21 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-390
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 455 items
+
+tests/unit/test_ccsession_tag.py ....................................... [  8%]
+........................................................................ [ 24%]
+........................................................................ [ 40%]
+........................................................................ [ 56%]
+.....................                                                    [ 60%]
+tests/unit/test_ccsession_tiers.py ..................................... [ 68%]
+........................................................................ [ 84%]
+............................                                             [ 90%]
+tests/unit/test_install_ccsession.py ......................              [ 95%]
+tests/cli/test_update_command.py ....................                    [100%]
+
+======================= 455 passed in 261.96s (0:04:21) ========================
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
