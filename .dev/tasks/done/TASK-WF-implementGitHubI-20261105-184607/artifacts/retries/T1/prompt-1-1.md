8399bef7cf4b7c724823960fa0f3a8272b23dda2
Review one task for spec compliance.

Task brief: ## Task 1: Add launcher tests for CCSESSION_PERMISSIONS to tests/unit/test_ccsession_tag.py

Source requirement: tests that fail on the old code (set: no bypass flag and shim/model routing kept; unset: unchanged), the exit-2 behavior, and the documented `--help` text. Work in `tests/unit/test_ccsession_tag.py`, next to `test_every_launch_restores_grep_and_glob`, which asserts the default flags on all six launch lines.

- Give `_label_launch` an optional keyword argument `extra_env: dict[str, str] | None = None` that is merged into the child environment after `HOME`, `CLAUDE_BIN` and `CCSESSION_ENV_FILE`; existing callers stay unchanged.
- Add a helper `_run_ccsession(tmp_path, *args, **extra)` that returns the `subprocess.CompletedProcess` without raising. It is modelled on the environment of `_label_launch` and must be safe on the unchanged launcher: it creates `tmp_path / "work"` and `tmp_path / "home"` with `mkdir(parents=True, exist_ok=True)`; `CLAUDE_BIN` is a fake script that only writes a marker file `tmp_path / "claude-ran"`; `HOME` is `tmp_path / "home"`; `CCSESSION_ENV_FILE` is a missing file in `tmp_path` unless `extra` sets it; `CC_CLAUDE_FLAGS` and `CCSESSION_PERMISSIONS` are removed from the inherited environment before `extra` is applied; and the call uses `stdin=subprocess.DEVNULL`, `timeout=60`, `check=False` and `cwd=tmp_path / "work"`.
- Add `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` to the variables deleted by the autouse environment-clearing block near the top of the file (the list that holds `CCSESSION_LAUNCH_ID` and `CLAUDE_TOPIC`), and `CCSESSION_PERMISSIONS` to the excluded-names tuple in `_orca_env` (the tuple that already holds `CC_CLAUDE_FLAGS`), so a value in the developer's shell never leaks into a test.
- Name every new test `test_permissions_default_<what it checks>` so `-k permissions` selects them, and add: a parametrized test over the same arguments-and-transcript matrix as `test_every_launch_restores_grep_and_glob` (all six launch lines: untagged, new and resumed, each with and without `--profile claude`) that runs with `CCSESSION_PERMISSIONS=default` and asserts the launched argument list starts with `--allowedTools=Grep`, contains no `--dangerously-skip-permissions`, contains `--model` exactly when `--profile` was given and `--resume` exactly when a transcript exists; `CCSESSION_PERMISSIONS=""` behaving like unset (starts with `--dangerously-skip-permissions`, `--allowedTools=Grep`); `CC_CLAUDE_FLAGS=--verbose` with the variable set to `default` launching with `--verbose` first and neither default flag; an empty `CC_CLAUDE_FLAGS` with the variable set to `default` launching with `--allowedTools=Grep` first and no bypass flag; an empty `CC_CLAUDE_FLAGS` with the variable unset taking the full old default; the variable set to `default` inside a `CCSESSION_ENV_FILE` (an `export` line) not enabling it, so the launched argument list still starts with `--dangerously-skip-permissions`; `CC_CLAUDE_FLAGS=--verbose` set inside a `CCSESSION_ENV_FILE` together with `CCSESSION_PERMISSIONS=default` in the shell launching with `--verbose` first (the env file still wins); and `ccsession demo --claude-args --dangerously-skip-permissions` with the variable set to `default` launching with `--allowedTools=Grep` first and the caller's `--dangerously-skip-permissions` still present in the argument list.
- Add exit-2 tests through `_run_ccsession`, parametrized over the values `bypass` and `Default`: `ccsession demo` returns 2, standard error names `CCSESSION_PERMISSIONS`, and the `claude-ran` marker does not exist; and one test that the value `bypass` with `--help` also returns 2 (the check is global).
- Add one help test through `_run_ccsession(tmp_path, "--help")` with no bad value: standard output contains `CCSESSION_PERMISSIONS=default` and contains neither `set -e` nor `CLAUDE_BIN=`, which proves the new text is in `--help` and that `show_help` still stops at the header.

Acceptance criteria:
- Run `uv run pytest tests/unit/test_ccsession_tag.py -k "permissions or grep_and_glob" -q` against the unchanged launcher and save the output to `./artifacts/t1-red.log`. These fail: the opt-in matrix, the empty-`CC_CLAUDE_FLAGS`-with-`default` test, the caller-passed-flag test (its first-argument check), the exit-2 test (both parametrized values, `bypass` and `Default`), the `--help` bad-value test and the help test. These pass: `test_every_launch_restores_grep_and_glob`, the empty-variable test, the `CC_CLAUDE_FLAGS=--verbose` override test, the env-file `CC_CLAUDE_FLAGS` test, the empty-`CC_CLAUDE_FLAGS`-with-variable-unset test and the env-file `CCSESSION_PERMISSIONS` test.
- During that red run no real `claude` process starts: every new test that launches `ccsession` uses a fake `CLAUDE_BIN`, and the exit-2 tests assert the marker file is absent.
- The new tests do not read or depend on the developer's own `CCSESSION_PERMISSIONS` or `CC_CLAUDE_FLAGS` values.

AC ids (in source order):
T1.AC1: Run `uv run pytest tests/unit/test_ccsession_tag.py -k "permissions or grep_and_glob" -q` against the unchanged launcher and save the output to `./artifacts/t1-red.log`. These fail: the opt-in matrix, the empty-`CC_CLAUDE_FLAGS`-with-`default` test, the caller-passed-flag test (its first-argument check), the exit-2 test (both parametrized values, `bypass` and `Default`), the `--help` bad-value test and the help test. These pass: `test_every_launch_restores_grep_and_glob`, the empty-variable test, the `CC_CLAUDE_FLAGS=--verbose` override test, the env-file `CC_CLAUDE_FLAGS` test, the empty-`CC_CLAUDE_FLAGS`-with-variable-unset test and the env-file `CCSESSION_PERMISSIONS` test.
T1.AC2: During that red run no real `claude` process starts: every new test that launches `ccsession` uses a fake `CLAUDE_BIN`, and the exit-2 tests assert the marker file is absent.
T1.AC3: The new tests do not read or depend on the developer's own `CCSESSION_PERMISSIONS` or `CC_CLAUDE_FLAGS` values.
Global constraints: ## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.
Start sha: 8399bef7cf4b7c724823960fa0f3a8272b23dda2
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index 62cf1979..d5b874a9 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -62,6 +62,11 @@ def _offline_model_data(monkeypatch, tmp_path_factory):
         "XDG_STATE_HOME",
         "CLAUDE_TOPIC",
         "CCSESSION_TOPIC_CWD",
+        # A permission choice or flag override exported in the developer's shell
+        # would change the flags every launch test expects (and a bad value
+        # makes ccsession exit 2).
+        "CCSESSION_PERMISSIONS",
+        "CC_CLAUDE_FLAGS",
     ):
         monkeypatch.delenv(name, raising=False)
     for name in (
@@ -1156,7 +1161,10 @@ def test_help_and_unknown_profile_list_data_profiles(tmp_path: Path) -> None:
 
 
 def _label_launch(
-    tmp_path: Path, transcript: bool, args: tuple[str, ...] = ("demo",)
+    tmp_path: Path,
+    transcript: bool,
+    args: tuple[str, ...] = ("demo",),
+    extra_env: dict[str, str] | None = None,
 ) -> tuple[str, bool]:
     home = tmp_path / "home"
     work = tmp_path / "work"
@@ -1180,6 +1188,7 @@ def _label_launch(
             "HOME": str(home),
             "CLAUDE_BIN": str(fake),
             "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
+            **(extra_env or {}),
         }
     )
     result = subprocess.run(
@@ -1193,6 +1202,47 @@ def _label_launch(
     return result.stdout, (topics / "demo.txt").exists()
 
 
+def _run_ccsession(
+    tmp_path: Path, *args: str, **extra: str
+) -> subprocess.CompletedProcess[str]:
+    """Run ccsession without raising, and without any way to start a real Claude.
+
+    The fake Claude only touches ``tmp_path / "claude-ran"``, so a test can tell
+    whether the launcher got as far as starting it, also on a launcher that
+    ignores the setting under test.
+    """
+    home = tmp_path / "home"
+    work = tmp_path / "work"
+    home.mkdir(parents=True, exist_ok=True)
+    work.mkdir(parents=True, exist_ok=True)
+    fake = tmp_path / "fake-claude"
+    fake.write_text(f'#!/bin/sh\ntouch "{tmp_path / "claude-ran"}"\n')
+    fake.chmod(0o700)
+    env = {
+        k: v
+        for k, v in os.environ.items()
+        if k not in ("CC_CLAUDE_FLAGS", "CCSESSION_PERMISSIONS")
+    }
+    env.update(
+        {
+            "HOME": str(home),
+            "CLAUDE_BIN": str(fake),
+            "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
+            **extra,
+        }
+    )
+    return subprocess.run(
+        [str(SKILL_DIR / "ccsession"), *args],
+        env=env,
+        cwd=work,
+        stdin=subprocess.DEVNULL,
+        text=True,
+        capture_output=True,
+        timeout=60,
+        check=False,
+    )
+
+
 def test_rm_removes_an_existing_label_that_starts_with_a_dash(tmp_path: Path) -> None:
     # Older /ccsession-tag versions could write one; it must stay removable.
     home = tmp_path / "home"
@@ -1256,6 +1306,155 @@ def test_every_launch_restores_grep_and_glob(
     assert ("--resume" in launched) == transcript
 
 
+# CCSESSION_PERMISSIONS=default (issue 390): the same six launch lines as above.
+_BYPASS = "--dangerously-skip-permissions"
+_PERMISSIONS_MATRIX = [
+    (("-p", "x"), False),
+    (("--profile", "claude", "-p", "x"), False),
+    (("demo",), False),
+    (("demo",), True),
+    (("--profile", "claude", "demo"), False),
+    (("--profile", "claude", "demo"), True),
+]
+
+
+@pytest.mark.parametrize(("args", "transcript"), _PERMISSIONS_MATRIX)
+def test_permissions_default_drops_the_bypass_on_every_launch_line(
+    tmp_path: Path, args: tuple[str, ...], transcript: bool
+) -> None:
+    # Only --allowedTools=Grep is added; the model and resume arguments stay.
+    stdout, _ = _label_launch(
+        tmp_path,
+        transcript=transcript,
+        args=args,
+        extra_env={"CCSESSION_PERMISSIONS": "default"},
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[0] == "--allowedTools=Grep"
+    assert _BYPASS not in launched
+    assert ("--model" in launched) == ("--profile" in args)
+    assert ("--resume" in launched) == transcript
+
+
+def test_permissions_default_empty_value_is_unset(tmp_path: Path) -> None:
+    stdout, _ = _label_launch(
+        tmp_path,
+        transcript=False,
+        extra_env={"CCSESSION_PERMISSIONS": ""},
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[:2] == [_BYPASS, "--allowedTools=Grep"]
+
+
+def test_permissions_default_non_empty_claude_flags_still_win(tmp_path: Path) -> None:
+    stdout, _ = _label_launch(
+        tmp_path,
+        transcript=False,
+        extra_env={"CCSESSION_PERMISSIONS": "default", "CC_CLAUDE_FLAGS": "--verbose"},
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[0] == "--verbose"
+    assert _BYPASS not in launched
+    assert "--allowedTools=Grep" not in launched
+
+
+def test_permissions_default_empty_claude_flags_take_the_opt_in_default(
+    tmp_path: Path,
+) -> None:
+    # An empty CC_CLAUDE_FLAGS is not special: the :- default applies, and with
+    # the opt-in that default has no bypass flag.
+    stdout, _ = _label_launch(
+        tmp_path,
+        transcript=False,
+        extra_env={"CCSESSION_PERMISSIONS": "default", "CC_CLAUDE_FLAGS": ""},
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[0] == "--allowedTools=Grep"
+    assert _BYPASS not in launched
+
+
+def test_permissions_default_empty_claude_flags_without_it_take_the_old_default(
+    tmp_path: Path,
+) -> None:
+    stdout, _ = _label_launch(
+        tmp_path, transcript=False, extra_env={"CC_CLAUDE_FLAGS": ""}
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[:2] == [_BYPASS, "--allowedTools=Grep"]
+
+
+def test_permissions_default_in_the_env_file_does_not_enable_it(tmp_path: Path) -> None:
+    # The variable is read at the flag-default line, before the env file is sourced.
+    env_file = tmp_path / "ccsession.env"
+    env_file.write_text("export CCSESSION_PERMISSIONS=default\n")
+    stdout, _ = _label_launch(
+        tmp_path,
+        transcript=False,
+        extra_env={"CCSESSION_ENV_FILE": str(env_file)},
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[:2] == [_BYPASS, "--allowedTools=Grep"]
+
+
+def test_permissions_default_claude_flags_in_the_env_file_still_win(
+    tmp_path: Path,
+) -> None:
+    env_file = tmp_path / "ccsession.env"
+    env_file.write_text("CC_CLAUDE_FLAGS=--verbose\n")
+    stdout, _ = _label_launch(
+        tmp_path,
+        transcript=False,
+        extra_env={
+            "CCSESSION_ENV_FILE": str(env_file),
+            "CCSESSION_PERMISSIONS": "default",
+        },
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[0] == "--verbose"
+    assert _BYPASS not in launched
+
+
+def test_permissions_default_keeps_a_flag_the_caller_passes(tmp_path: Path) -> None:
+    # Only the flags ccsession adds change; Claude's own arguments pass through.
+    stdout, _ = _label_launch(
+        tmp_path,
+        transcript=False,
+        args=("demo", "--claude-args", _BYPASS),
+        extra_env={"CCSESSION_PERMISSIONS": "default"},
+    )
+    launched = json.loads(stdout.strip().splitlines()[-1])
+    assert launched[0] == "--allowedTools=Grep"
+    assert launched[-1] == _BYPASS
+
+
+@pytest.mark.parametrize("value", ["bypass", "Default"])
+def test_permissions_default_any_other_value_exits_2(
+    tmp_path: Path, value: str
+) -> None:
+    result = _run_ccsession(tmp_path, "demo", CCSESSION_PERMISSIONS=value)
+    assert result.returncode == 2
+    assert "CCSESSION_PERMISSIONS" in result.stderr
+    assert not (tmp_path / "claude-ran").exists()
+
+
+def test_permissions_default_bad_value_also_stops_help(tmp_path: Path) -> None:
+    # The check runs before the argument dispatch, so it covers every call.
+    result = _run_ccsession(tmp_path, "--help", CCSESSION_PERMISSIONS="bypass")
+    assert result.returncode == 2
+    assert "CCSESSION_PERMISSIONS" in result.stderr
+
+
+def test_permissions_default_help_lists_the_variable_and_stops_at_the_header(
+    tmp_path: Path,
+) -> None:
+    result = _run_ccsession(tmp_path, "--help")
+    assert result.returncode == 0
+    assert "CCSESSION_PERMISSIONS=default" in result.stdout
+    # show_help stops at the header comment; the code below it must not appear.
+    assert "set -e" not in result.stdout
+    assert "CLAUDE_BIN=" not in result.stdout
+
+
 def test_private_addon_profiles_never_download_model_data(
     tmp_path: Path, monkeypatch
 ) -> None:
@@ -1345,6 +1544,7 @@ def _orca_env(tmp_path: Path, **extra: str) -> dict[str, str]:
             "ANTHROPIC_AUTH_TOKEN",
             "LITELLM_API_KEY",
             "CC_CLAUDE_FLAGS",
+            "CCSESSION_PERMISSIONS",
             "CCSESSION_AUTOSTART",
             "CCSESSION_ASK_TIMEOUT",
             "CCSESSION_NAME",

diff --git a/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t1-red.log b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t1-red.log
new file mode 100644
index 00000000..79fd1a9a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/artifacts/t1-red.log
@@ -0,0 +1,102 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-390
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 275 items / 252 deselected / 23 selected
+
+tests/unit/test_ccsession_tag.py ......FFFFFF..F...FFFFF                 [100%]
+
+=================================== FAILURES ===================================
+_ test_permissions_default_drops_the_bypass_on_every_launch_line[args0-False] __
+tests/unit/test_ccsession_tag.py:1333: in test_permissions_default_drops_the_bypass_on_every_launch_line
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+_ test_permissions_default_drops_the_bypass_on_every_launch_line[args1-False] __
+tests/unit/test_ccsession_tag.py:1333: in test_permissions_default_drops_the_bypass_on_every_launch_line
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+_ test_permissions_default_drops_the_bypass_on_every_launch_line[args2-False] __
+tests/unit/test_ccsession_tag.py:1333: in test_permissions_default_drops_the_bypass_on_every_launch_line
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+__ test_permissions_default_drops_the_bypass_on_every_launch_line[args3-True] __
+tests/unit/test_ccsession_tag.py:1333: in test_permissions_default_drops_the_bypass_on_every_launch_line
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+_ test_permissions_default_drops_the_bypass_on_every_launch_line[args4-False] __
+tests/unit/test_ccsession_tag.py:1333: in test_permissions_default_drops_the_bypass_on_every_launch_line
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+__ test_permissions_default_drops_the_bypass_on_every_launch_line[args5-True] __
+tests/unit/test_ccsession_tag.py:1333: in test_permissions_default_drops_the_bypass_on_every_launch_line
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+_____ test_permissions_default_empty_claude_flags_take_the_opt_in_default ______
+tests/unit/test_ccsession_tag.py:1372: in test_permissions_default_empty_claude_flags_take_the_opt_in_default
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+___________ test_permissions_default_keeps_a_flag_the_caller_passes ____________
+tests/unit/test_ccsession_tag.py:1426: in test_permissions_default_keeps_a_flag_the_caller_passes
+    assert launched[0] == "--allowedTools=Grep"
+E   AssertionError: assert '--dangerousl...p-permissions' == '--allowedTools=Grep'
+E     
+E     - --allowedTools=Grep
+E     + --dangerously-skip-permissions
+___________ test_permissions_default_any_other_value_exits_2[bypass] ___________
+tests/unit/test_ccsession_tag.py:1433: in test_permissions_default_any_other_value_exits_2
+    assert result.returncode == 2
+E   assert 0 == 2
+E    +  where 0 = CompletedProcess(args=['/home/coder/workspaces/worktrees/IronClaude/ic-issue-390/src/superclaude/skills/ccsession-tag/ccsession', 'demo'], returncode=0, stdout="[ccsession] Starting new session labeled 'demo'\n", stderr='').returncode
+__________ test_permissions_default_any_other_value_exits_2[Default] ___________
+tests/unit/test_ccsession_tag.py:1433: in test_permissions_default_any_other_value_exits_2
+    assert result.returncode == 2
+E   assert 0 == 2
+E    +  where 0 = CompletedProcess(args=['/home/coder/workspaces/worktrees/IronClaude/ic-issue-390/src/superclaude/skills/ccsession-tag/ccsession', 'demo'], returncode=0, stdout="[ccsession] Starting new session labeled 'demo'\n", stderr='').returncode
+______________ test_permissions_default_bad_value_also_stops_help ______________
+tests/unit/test_ccsession_tag.py:1441: in test_permissions_default_bad_value_also_stops_help
+    assert result.returncode == 2
+E   AssertionError: assert 0 == 2
+E    +  where 0 = CompletedProcess(args=['/home/coder/workspaces/worktrees/IronClaude/ic-issue-390/src/superclaude/skills/ccsession-tag/...Max and 1M context\n  ccsession --profile glm --shim\n                            GLM 5.3 and 1M context\n', stderr='').returncode
+___ test_permissions_default_help_lists_the_variable_and_stops_at_the_header ___
+tests/unit/test_ccsession_tag.py:1450: in test_permissions_default_help_lists_the_variable_and_stops_at_the_header
+    assert "CCSESSION_PERMISSIONS=default" in result.stdout
+E   assert 'CCSESSION_PERMISSIONS=default' in "ccsession — Claude Code session manager with labeled resume\n\nPart of the 'ccsession' skill. Symlinked from ~/.local...   Qwen 3.8 Max and 1M context\n  ccsession --profile glm --shim\n                            GLM 5.3 and 1M context\n"
+E    +  where "ccsession — Claude Code session manager with labeled resume\n\nPart of the 'ccsession' skill. Symlinked from ~/.local...   Qwen 3.8 Max and 1M context\n  ccsession --profile glm --shim\n                            GLM 5.3 and 1M context\n" = CompletedProcess(args=['/home/coder/workspaces/worktrees/IronClaude/ic-issue-390/src/superclaude/skills/ccsession-tag/...Max and 1M context\n  ccsession --profile glm --shim\n                            GLM 5.3 and 1M context\n', stderr='').stdout
+=========================== short test summary info ============================
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_drops_the_bypass_on_every_launch_line[args0-False]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_drops_the_bypass_on_every_launch_line[args1-False]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_drops_the_bypass_on_every_launch_line[args2-False]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_drops_the_bypass_on_every_launch_line[args3-True]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_drops_the_bypass_on_every_launch_line[args4-False]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_drops_the_bypass_on_every_launch_line[args5-True]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_empty_claude_flags_take_the_opt_in_default
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_keeps_a_flag_the_caller_passes
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_any_other_value_exits_2[bypass]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_any_other_value_exits_2[Default]
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_bad_value_also_stops_help
+FAILED tests/unit/test_ccsession_tag.py::test_permissions_default_help_lists_the_variable_and_stops_at_the_header
+================ 12 failed, 11 passed, 252 deselected in 3.90s =================
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
