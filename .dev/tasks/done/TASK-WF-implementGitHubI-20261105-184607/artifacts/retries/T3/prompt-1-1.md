f2b9f207fb6d8327db1f649a773ba4b26406f2ad
Review one task for spec compliance.

Task brief: ## Task 3: Add the tier-mode test and the tier fixture isolation to tests/unit/test_ccsession_tiers.py

Source requirement: tier models are kept when the variable is set, and the tier tests do not depend on the developer's shell. Work in `tests/unit/test_ccsession_tiers.py`, which has `_launch(tmp_path, *args, defaults=TIER_BLOCK, **extra)` (it runs `ccsession` with a fake `claude` that writes `seen.json` with `argv`, `settings` and `base_url`) and the autouse `_isolated` fixture.

- Add `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` to the names deleted in the autouse `_isolated` fixture (the list that holds `CCSESSION_SHOW_ALL_MODELS`).
- Add a test named `test_tier_launch_permissions_default_keeps_tier_routing` that calls `_launch(tmp_path, "work", "--tier", "tier0")` once as the control and once more with the extra argument `CCSESSION_PERMISSIONS="default"`. Neither call passes `--dangerously-skip-permissions` or any other flag explicitly (the tests that call `ccsession-orca` with that flag, for example the ones that pass it at the start of their argument list, are not the model for this test).

Acceptance criteria:
- The opted-in run's `seen["argv"]` contains no `--dangerously-skip-permissions` and begins with `--allowedTools=Grep`; the control run's begins with `--dangerously-skip-permissions`.
- The opted-in run has the same `settings` value, the same `--model` argument (when the control has one) and the same `base_url` as the control run.
- Saved output of `uv run pytest tests/unit/test_ccsession_tiers.py -k permissions -q` against the unchanged launcher is in `./artifacts/t3-red.log` and shows this test failing.

AC ids (in source order):
T3.AC1: The opted-in run's `seen["argv"]` contains no `--dangerously-skip-permissions` and begins with `--allowedTools=Grep`; the control run's begins with `--dangerously-skip-permissions`.
T3.AC2: The opted-in run has the same `settings` value, the same `--model` argument (when the control has one) and the same `base_url` as the control run.
T3.AC3: Saved output of `uv run pytest tests/unit/test_ccsession_tiers.py -k permissions -q` against the unchanged launcher is in `./artifacts/t3-red.log` and shows this test failing.
Global constraints: ## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.
Start sha: f2b9f207fb6d8327db1f649a773ba4b26406f2ad
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index df655a5d..194a9289 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -118,6 +118,11 @@ def _isolated(monkeypatch, tmp_path_factory):
         "CCSESSION_MODEL_ORDER",
         "CODER_WORKSPACE_OWNER_NAME",
         "CODER_WORKSPACE_OWNER_ROLES",
+        # A permission choice or flag override exported in the developer's shell
+        # would change the flags the launch tests expect (and a bad value makes
+        # ccsession exit 2).
+        "CCSESSION_PERMISSIONS",
+        "CC_CLAUDE_FLAGS",
     ):
         monkeypatch.delenv(name, raising=False)
 
@@ -544,6 +549,24 @@ def test_tier_flag_and_named_model(tmp_path: Path) -> None:
     assert "not in any tier" in err
 
 
+def test_tier_launch_permissions_default_keeps_tier_routing(tmp_path: Path) -> None:
+    # CCSESSION_PERMISSIONS=default drops only the bypass flag: the tier model,
+    # its settings and the shim address are the control launch's. Neither launch
+    # passes a flag of its own.
+    rc, _, err, control = _launch(tmp_path, "work", "--tier", "tier0")
+    assert rc == 0, err
+    rc, _, err, opted_in = _launch(
+        tmp_path, "work", "--tier", "tier0", CCSESSION_PERMISSIONS="default"
+    )
+    assert rc == 0, err
+    assert control["argv"][0] == "--dangerously-skip-permissions"
+    assert opted_in["argv"][0] == "--allowedTools=Grep"
+    assert "--dangerously-skip-permissions" not in opted_in["argv"]
+    assert opted_in["settings"] == control["settings"]
+    assert _model_arg(opted_in) == _model_arg(control) == "claude-gw-tier0[1m]"
+    assert opted_in["base_url"] == control["base_url"] == "http://127.0.0.1:4555"
+
+
 def test_tier_mode_refuses_profiles_and_bad_tiers(tmp_path: Path) -> None:
     rc, _, err, seen = _launch(tmp_path, "work", "--profile", "gpt", "--shim")
     assert rc == 2 and seen is None

diff --git a/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t3-red.log b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t3-red.log
new file mode 100644
index 00000000..109e1fcd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t3-red.log
@@ -0,0 +1,22 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-390
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 137 items / 136 deselected / 1 selected
+
+tests/unit/test_ccsession_tiers.py F                                     [100%]
+
+=================================== FAILURES ===================================
+___________ test_tier_launch_permissions_default_keeps_tier_routing ____________
+tests/unit/test_ccsession_tiers.py:563: in test_tier_launch_permissions_default_keeps_tier_routing
+    assert opted_in["argv"][0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+=========================== short test summary info ============================
+FAILED tests/unit/test_ccsession_tiers.py::test_tier_launch_permissions_default_keeps_tier_routing
+====================== 1 failed, 136 deselected in 1.96s =======================
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
