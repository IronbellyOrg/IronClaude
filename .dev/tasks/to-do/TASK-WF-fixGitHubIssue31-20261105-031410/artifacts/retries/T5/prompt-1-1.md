c966f12a5ee9e1dc2280747d741d4db032ac66a4
Review one task for spec compliance.

Task brief: ## Task 5: Update the tests that pinned the old untagged behaviour

Depends on: Task 4

In tests/unit/test_ccsession_tag.py, update the Orca tests that assert the old behaviour, using the existing harness helpers (`_orca_env`, `_orca_tty`, `_orca_no_tty`, `_spawn_on_pty`) and the changed question text constant `ORCA_QUESTION`: `test_orca_enter_or_ctrl_c_starts_untagged` (Enter now auto-names; Ctrl+C now exits 130 with no Claude start), `test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal` (still restores the terminal and now exits 130), `test_orca_unanswered_question_starts_untagged` (timeout now auto-names), `test_orca_keys_already_typed_skip_the_question`, `test_orca_without_a_terminal_never_asks`, `test_orca_prompt_reaches_claude_unchanged_and_is_never_a_label`, `test_orca_prefill_passes_through_and_its_text_is_not_a_flag`, `test_orca_a_launch_with_more_than_options_is_asked_as_before`, `test_orca_relaunch_without_a_terminal_or_autostart_changes_nothing` and any other Orca test in the file that asserts `record["topic"] is None` or an unchanged argument list for a launch that is now auto-named. Rename tests whose names no longer describe them. Keep `test_orca_resume_skips_the_question`, `test_orca_autostart_off_never_asks` and the relaunch reopen tests asserting untagged or reopened behaviour as they are.

Acceptance criteria:
- T5.AC1: `uv run pytest tests/unit/test_ccsession_tag.py -k orca -v` passes, and no remaining Orca test asserts that a prompt-bearing, no-terminal, Enter or timeout launch is untagged.
- T5.AC2: The prompt text `demo` with a saved label `demo` still never resumes that label (the prompt is not a label).
Global constraints: 
- Scope is the IronClaude part of issue 315 only: src/superclaude/skills/ccsession-tag/ccsession, src/superclaude/skills/ccsession-tag/ccsession-orca, their tests and docs. The Coder repo (New Terminal hook, the claude wrapper handoff) is out of scope and is not touched.
- Build on master. Never rebase on or merge origin/clayphi/433-ccsession-orca-resume; its work is already in master through pull request 355 and it must not be pushed to or edited.
- The pull request 355 tab reopen in ccsession-orca keeps running first, under the same conditions as today (terminal, CCSESSION_AUTOSTART not 0, no resume option, ORCA_PANE_KEY set, only Orca's own options), ahead of the question and ahead of the auto-name.
- The typed prompt is never read as a label. A line typed at the question is a name unless it cannot be one (control character, more than one line, or over 245 bytes); normal lines, spaces included, stay names. No other input guessing.
- Decisions taken by the plan author where the source is silent, to be reported to the owner: CCSESSION_AUTOSTART=0 keeps meaning a plain untagged start with no question and no auto-name; print-mode launches (-p, --print) stay untagged because they are not interactive sessions; resume-like launches (--resume, -r, --continue, -c, --fork-session, --from-pr) keep their own session and get no label; CCSESSION_NAME is the supported explicit name and is read by ccsession-orca, while a Claude --name or -n in Orca's arguments is NOT lifted: it passes through to Claude unchanged and counts as a name carried (no question, no auto-name). This replaces the earlier lift decision (see the amendments below).
- Claude Agent Teams stays the one documented exception: it is documented and listed as a follow-up, not changed.
- All tests run only in throwaway HOME directories under the pytest tmp_path, with the fake Claude binary of the existing harness. Never touch the live ~/.claude or the live ccsession shim. Edit src/superclaude files only; never stage .claude/ mirrors except .claude/settings.json.
- Amendments from the advisory review, resolved before execution (source: .dev/reflect/pre-fixGitHubIssue31-20261105031639/adversarial/merged-verdict.yaml; they apply to every task and win over any task text that conflicts with them):
- RN-1: an invalid CCSESSION_NAME, an empty or failing --auto-name result (control character, over 245 bytes, a folder name with a leading dot or 4-byte characters, an unwritable topics directory) or an unexpected --ask status never stops Claude from starting. Fallback order: drop the bad name with a stderr warning, then auto-name, then a plain untagged start; ccsession-orca never exits 2 for these. A name equal to a saved label never silently resumes that conversation. Tests in Tasks 3, 4 and 7: leading-dot folder, name with a tab, 300-character CCSESSION_NAME, name equal to a saved label, failing --auto-name; each reaches the fake Claude.
- RN-2: Claude --name/-n/--name= in Orca's arguments is not lifted (Task 3 criterion 2 and the Task 7 --name case change accordingly): such a launch counts as name-carried and passes unchanged. CCSESSION_NAME is validated (RN-1) and unset before every exec.
- RN-3: --auto-name is dispatched in the early fast-path case of ccsession (before the main argument loop, after ensure_names_migrated), not next to --ask; tests for the texts --model, --claude-args, --shim and --tier=x.
- RN-4: Task 5 also updates test_orca_a_new_tab_or_a_rerun_is_still_asked and test_orca_relaunch_whose_conversation_is_gone_is_asked (Enter now auto-names), rewrites test_orca_invalid_name_asks_again, drops the "the prompt" argument from the Ctrl+C line-mode test, changes test_orca_saved_name_is_listed_and_resumes_before_the_prompt to the `--name demo "fix it"` form, and adds CCSESSION_NAME to the environment exclusion lists in tests/unit/test_ccsession_tag.py and tests/unit/test_ccsession_tiers.py. "Keep as they are" applies only to reopen tests that do not press Enter.
- RN-5: the typed line is read with IFS= read -r and tested raw for control characters and the 245-byte rule before any trimming; an exit-3 message that starts with "-" is passed after "--"; tests for a leading tab, a trailing tab, a mid-line tab, "- a list" and "--version".
- RN-6: ccsession-orca unsets CCSESSION_ASK_TIMEOUT and CCSESSION_NAME before the final exec (the one-second timeout test sets the variable while Claude's recorded environment must not contain it).
- RN-7: the Task 3 classification covers --session-id=*, --prefill=* and --name=*, a trailing --name with no value, and treats the values of known value-taking options (--model, --permission-mode, --add-dir, --allowedTools, --mcp-config) as non-positional; unknown options fail safe (counted as a task); one test per form.
- RN-8: a test runs ccsession --ask with CCSESSION_ASK_TIMEOUT=2 and asserts the hint reads "auto-named after 2s", next to the default-hint test, so a default left unlimited fails.
- RN-9: the auto-name carries seconds or a short random part, folder name and task words are cut first so the stamp is kept, and two --auto-name calls in the same minute with no saved topic give different labels.
- RN-10: the executor writes ./artifacts/launch-paths.md from the final pytest output; no test writes outside tmp_path.
- RN-11: ccsession-orca passes the auto-name hint; the default hint of ask_session_name stays as today for other callers; the Task 11 handoff states that the 30 s default now also applies to the Coder New Terminal hook and that the dependency on orchestrators passing a task or name is documented, not enforced.
- RN-12: the Task 9 criterion also pins the --session-id statement in README.md.
Start sha: c966f12a5ee9e1dc2280747d741d4db032ac66a4
Diff against the start snapshot: diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index aaee1654..9e3c8fed 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -1302,7 +1302,11 @@ def test_plain_double_dash_still_reaches_claude(tmp_path: Path) -> None:
 # the real ccsession against a fake claude that records its argv and env, and a
 # fake shim that ccsession reuses.
 ORCA = SKILL_DIR / "ccsession-orca"
-ORCA_QUESTION = "Session name (Enter or Ctrl+C = untagged; untagged after 30s): "
+ORCA_QUESTION = "Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s): "
+# What ccsession --auto-name makes in the tests' working folder "work": the
+# folder, up to four words of the task, then month-day, time with seconds and a
+# random part.
+AUTO_LABEL = re.compile(r"^work(-[a-z0-9]+)*-\d{4}-\d{6}-[0-9a-f]{4}$")
 ORCA_FLAGS = ["--dangerously-skip-permissions", "--allowedTools=Grep"]
 SESSION_ID = "abc12345-0000-0000-0000-000000000000"
 
@@ -1341,6 +1345,7 @@ def _orca_env(tmp_path: Path, **extra: str) -> dict[str, str]:
             "CC_CLAUDE_FLAGS",
             "CCSESSION_AUTOSTART",
             "CCSESSION_ASK_TIMEOUT",
+            "CCSESSION_NAME",
             "CLAUDE_TOPIC",
         )
     }
@@ -1491,14 +1496,44 @@ def test_orca_name_starts_a_labeled_session_through_the_shim(tmp_path: Path) ->
     _assert_through_shim(record)
 
 
-def test_orca_saved_name_is_listed_and_resumes_before_the_prompt(
+def _auto_label(record: dict) -> str:
+    """The automatic name Claude was started with (--name <label>)."""
+    argv = record["argv"]
+    assert "--name" in argv, argv
+    label = argv[argv.index("--name") + 1]
+    assert AUTO_LABEL.match(label), label
+    assert record["topic"] == label
+    return label
+
+
+def test_orca_saved_name_is_listed_and_resumes_at_the_question(
     tmp_path: Path,
 ) -> None:
     _seed_label(tmp_path, "demo")
-    output, record = _orca_tty(tmp_path, "fix it", keys="demo\r")
+    output, record = _orca_tty(tmp_path, keys="demo\r")
     assert "Saved sessions in" in output
     assert "demo" in output.split(ORCA_QUESTION)[0]
     assert record["topic"] == "demo"
+    assert record["argv"] == [
+        *ORCA_FLAGS,
+        "--name",
+        "demo",
+        "--resume",
+        SESSION_ID,
+    ]
+
+
+def test_orca_saved_name_in_ccsession_name_resumes_before_the_prompt(
+    tmp_path: Path,
+) -> None:
+    # An explicit name is not asked about: it resumes the saved session of that
+    # name, loudly, and the prompt still reaches Claude last.
+    _seed_label(tmp_path, "demo")
+    env = _orca_env(tmp_path, CCSESSION_NAME="demo")
+    output, record = _orca_tty(tmp_path, "fix it", keys=None, env=env)
+    assert "Session name" not in output
+    assert "Resuming 'demo'" in output
+    assert record["topic"] == "demo"
     assert record["argv"] == [
         *ORCA_FLAGS,
         "--name",
@@ -1507,19 +1542,35 @@ def test_orca_saved_name_is_listed_and_resumes_before_the_prompt(
         SESSION_ID,
         "fix it",
     ]
+    assert "CCSESSION_NAME" not in record["env_names"]
 
 
-@pytest.mark.parametrize("keys", ["\r", "\x03"], ids=["enter", "ctrl-c"])
-def test_orca_enter_or_ctrl_c_starts_untagged(tmp_path: Path, keys: str) -> None:
-    output, record = _orca_tty(tmp_path, "the prompt", keys=keys)
-    assert "Starting untagged session" in output
-    assert record["topic"] is None
-    assert record["argv"] == [*ORCA_FLAGS, "the prompt"]
+def test_orca_enter_gets_an_auto_name(tmp_path: Path) -> None:
+    output, record = _orca_tty(tmp_path, keys="\r")
+    label = _auto_label(record)
+    assert f"Starting new session labeled '{label}'" in output
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label]
     _assert_through_shim(record)
     # The question's default time limit is not left in Claude's environment.
     assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]
 
 
+def test_orca_ctrl_c_cancels_without_starting_claude(tmp_path: Path) -> None:
+    proc, master = _spawn_on_pty([str(ORCA)], _orca_env(tmp_path), tmp_path / "work")
+    try:
+        assert ORCA_QUESTION in _read_pty(master, until=ORCA_QUESTION)
+        os.write(master, b"\x03")
+        output = _read_pty(master)
+        assert proc.wait(timeout=60) == 130, output
+        assert termios.tcgetattr(master)[3] & termios.ICANON
+    finally:
+        if proc.poll() is None:
+            proc.kill()
+        os.close(master)
+    assert "Starting" not in output
+    assert not (tmp_path / "record.json").exists()
+
+
 def _slow_probe(tmp_path: Path) -> None:
     # The keys-waiting probe runs while line mode is off; a python3 shim that
     # pauses before it leaves time to press Ctrl+C inside that window.
@@ -1540,12 +1591,15 @@ def test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal(
     # line mode back, and Claude then started on that terminal.
     env = _orca_env(tmp_path)
     _slow_probe(tmp_path)
-    proc, master = _spawn_on_pty([str(ORCA), "the prompt"], env, tmp_path / "work")
+    # No prompt argument: a launch with a task is never asked, so never probed.
+    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
     try:
         time.sleep(1)
         os.write(master, b"\x03")
         output = _read_pty(master)
-        assert proc.wait(timeout=60) == 0, output
+        # Ctrl+C cancels the launch (status 130); Claude is not started.
+        assert proc.wait(timeout=60) == 130, output
+        assert termios.tcgetattr(master)[3] & termios.ICANON
     finally:
         if proc.poll() is None:
             proc.kill()
@@ -1553,10 +1607,7 @@ def test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal(
     assert ORCA_QUESTION not in output
     # The probe was interrupted; its traceback must not reach the terminal.
     assert "KeyboardInterrupt" not in output
-    record = json.loads((tmp_path / "record.json").read_text())
-    assert record["icanon"] is True
-    assert record["topic"] is None
-    assert record["argv"] == [*ORCA_FLAGS, "the prompt"]
+    assert not (tmp_path / "record.json").exists()
 
 
 def test_ask_ctrl_c_while_line_mode_is_off_exits_130_and_restores(
@@ -1589,25 +1640,23 @@ def test_ask_ctrl_c_while_line_mode_is_off_exits_130_and_restores(
         os.close(master)
 
 
-def test_orca_invalid_name_asks_again(tmp_path: Path) -> None:
-    # A name too long for a file name can never be saved (one starting with "-"
-    # is fine now: ccsession-orca passes it as --name).
-    env = _orca_env(tmp_path)
-    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
-    try:
-        assert ORCA_QUESTION in _read_pty(master, until=ORCA_QUESTION)
-        for bad in (b"x" * 246, "あ".encode() * 82):
-            os.write(master, bad + b"\r")
-            again = _read_pty(master, until=ORCA_QUESTION)
-            assert "invalid label" in again and again.count(ORCA_QUESTION) == 1
-        os.write(master, b"good\r")
-        _read_pty(master)
-        assert proc.wait(timeout=60) == 0
-    finally:
-        if proc.poll() is None:
-            proc.kill()
-        os.close(master)
-    assert json.loads((tmp_path / "record.json").read_text())["topic"] == "good"
+@pytest.mark.parametrize(
+    "line",
+    ["x" * 246, "あ" * 82, "foo\tbar", "\tfoo", "foo\t"],
+    ids=["246 bytes", "82 CJK characters", "inner tab", "leading tab", "trailing tab"],
+)
+def test_orca_a_line_that_cannot_be_a_name_goes_to_claude_as_a_message(
+    tmp_path: Path, line: str
+) -> None:
+    # A name too long for a file name (or holding a control character) can never
+    # be saved, so it is not a name: it is the first message for Claude, and the
+    # launch is auto-named. (One starting with "-" is fine as a name:
+    # ccsession-orca passes it as --name.)
+    output, record = _orca_tty(tmp_path, keys=line + "\r")
+    assert "invalid label" not in output
+    label = _auto_label(record)
+    assert label != line
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, line]
 
 
 @pytest.mark.parametrize(
@@ -1646,26 +1695,46 @@ def test_orca_prompt_reaches_claude_unchanged_and_is_never_a_label(
     # "demo" is a saved label: read as one, the launch would resume it.
     _seed_label(tmp_path, "demo")
     output, record = _orca_no_tty(tmp_path, prompt)
-    assert record["topic"] is None
-    assert record["argv"] == [*ORCA_FLAGS, prompt]
     assert "Resuming" not in output
+    assert record["topic"] != "demo"
+    assert "--resume" not in record["argv"]
+    # The prompt is Claude's last argument, unchanged. A prompt that is itself
+    # an option (--help) starts no session, so it gets no automatic name.
+    assert record["argv"][-1] == prompt
+    if prompt == "--help":
+        assert record["argv"] == [*ORCA_FLAGS, prompt]
+    else:
+        label = record["argv"][record["argv"].index("--name") + 1]
+        assert label.startswith("work-")
+        assert record["topic"] == label
 
 
 def test_orca_prefill_passes_through_and_its_text_is_not_a_flag(
     tmp_path: Path,
 ) -> None:
-    # The prefill text "--resume" is input-box text, so the question is asked.
-    output, record = _orca_tty(tmp_path, "--prefill", "--resume", keys="\r")
-    assert record["argv"] == [*ORCA_FLAGS, "--prefill", "--resume"]
+    # The prefill text "--resume" is input-box text, not a flag: the launch
+    # carries a task (no question) and is auto-named, not treated as a resume.
+    output, record = _orca_tty(tmp_path, "--prefill", "--resume", keys=None)
+    assert "Session name" not in output
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "--prefill", "--resume"]
     output, record = _orca_no_tty(tmp_path, "--prefill", "draft 'text' here")
-    assert record["argv"] == [*ORCA_FLAGS, "--prefill", "draft 'text' here"]
+    label = _auto_label(record)
+    assert record["argv"] == [
+        *ORCA_FLAGS,
+        "--name",
+        label,
+        "--prefill",
+        "draft 'text' here",
+    ]
 
 
 def test_orca_without_a_terminal_never_asks(tmp_path: Path) -> None:
     output, record = _orca_no_tty(tmp_path, "hello")
     assert "Session name" not in output
-    assert record["topic"] is None
-    assert record["argv"] == [*ORCA_FLAGS, "hello"]
+    label = _auto_label(record)
+    assert label.startswith("work-hello-")
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "hello"]
     _assert_through_shim(record)
 
 
@@ -1677,30 +1746,33 @@ def test_orca_autostart_off_never_asks(tmp_path: Path) -> None:
     assert record["argv"] == [*ORCA_FLAGS, "hello"]
 
 
-def test_orca_unanswered_question_starts_untagged(tmp_path: Path) -> None:
+def test_orca_unanswered_question_is_auto_named(tmp_path: Path) -> None:
     # Orca's supervised workers fail when Claude is not ready within 60s.
     env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="1")
-    proc, master = _spawn_on_pty([str(ORCA), "task"], env, tmp_path / "work")
+    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
     try:
-        shown = _read_pty(master, until="untagged after 1s): ")
-        assert "untagged after 1s): " in shown
+        shown = _read_pty(master, until="auto-named after 1s): ")
+        assert "auto-named after 1s): " in shown
         output = _read_pty(master)
         assert proc.wait(timeout=60) == 0, output
     finally:
         if proc.poll() is None:
             proc.kill()
         os.close(master)
-    assert "Starting untagged session" in output
     record = json.loads((tmp_path / "record.json").read_text())
-    assert record["topic"] is None
-    assert record["argv"] == [*ORCA_FLAGS, "task"]
+    label = _auto_label(record)
+    assert f"Starting new session labeled '{label}'" in output
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label]
+    assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]
 
 
 def test_orca_keys_already_typed_skip_the_question(tmp_path: Path) -> None:
-    # Something typing into the tab before the question would become the name.
+    # Something typing into the tab before the question would become the name:
+    # it is left for Claude instead, and the launch is auto-named.
     output, record = _orca_tty(tmp_path, keys=None, typed_ahead="x")
     assert "Session name" not in output
-    assert record["topic"] is None
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label]
 
 
 # Reopening an Orca tab's own session when Orca relaunches the tab after a
@@ -1800,28 +1872,37 @@ def test_orca_a_new_tab_or_a_rerun_is_still_asked(
     env = _tab_env(tmp_path, pane=pane, handle=handle)
     output, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys="\r", env=env)
     assert "Reopening" not in output
-    assert record["topic"] is None
-    assert record["argv"] == [*ORCA_FLAGS, ORCA_DEFAULT]
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]
 
 
 @pytest.mark.parametrize(
-    "args",
+    ("args", "named"),
     [
-        ("fix it",),
-        ("--prefill", "draft"),
-        ("--name", "other"),
-        (ORCA_DEFAULT, "-p"),
-        ("--session-id", OTHER_SESSION),
+        (("fix it",), True),
+        (("--prefill", "draft"), True),
+        (("--name", "other"), False),
+        ((ORCA_DEFAULT, "-p"), False),
+        (("--session-id", OTHER_SESSION), True),
     ],
     ids=["prompt", "prefill", "name", "print", "session-id"],
 )
-def test_orca_a_launch_with_more_than_options_is_asked_as_before(
-    tmp_path: Path, args: tuple[str, ...]
+def test_orca_a_launch_with_more_than_options_is_not_asked_and_never_reopens(
+    tmp_path: Path, args: tuple[str, ...], named: bool
 ) -> None:
+    # A task or a name is carried, so there is no question; the tab's recorded
+    # session is not reopened either. A task gets an automatic name; a Claude
+    # --name or print mode passes through unchanged.
     _tab_runs(tmp_path, SESSION_ID)
-    output, record = _orca_tty(tmp_path, *args, keys="\r", env=_tab_env(tmp_path))
+    output, record = _orca_tty(tmp_path, *args, keys=None, env=_tab_env(tmp_path))
     assert "Reopening" not in output
-    assert record["argv"] == [*ORCA_FLAGS, *args]
+    assert "Session name" not in output
+    if named:
+        label = _auto_label(record)
+        assert record["argv"] == [*ORCA_FLAGS, "--name", label, *args]
+    else:
+        assert record["argv"] == [*ORCA_FLAGS, *args]
+        assert record["topic"] is None
 
 
 @pytest.mark.parametrize(
@@ -1845,7 +1926,8 @@ def test_orca_relaunch_without_a_terminal_or_autostart_changes_nothing(
     extra = {"ORCA_PANE_KEY": PANE, "ORCA_TERMINAL_HANDLE": "term_after"}
     output, record = _orca_no_tty(tmp_path, ORCA_DEFAULT, **extra)
     assert "Reopening" not in output
-    assert record["argv"] == [*ORCA_FLAGS, ORCA_DEFAULT]
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]
     env = _tab_env(tmp_path, CCSESSION_AUTOSTART="0")
     output, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys=None, env=env)
     assert "Reopening" not in output
@@ -1860,7 +1942,8 @@ def test_orca_relaunch_whose_conversation_is_gone_is_asked(tmp_path: Path) -> No
         tmp_path, ORCA_DEFAULT, keys="\r", env=_tab_env(tmp_path)
     )
     assert "Reopening" not in output
-    assert record["argv"] == [*ORCA_FLAGS, ORCA_DEFAULT]
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]
 
 
 def test_orca_two_tabs_never_reopen_the_same_session(tmp_path: Path) -> None:
@@ -1875,7 +1958,8 @@ def test_orca_two_tabs_never_reopen_the_same_session(tmp_path: Path) -> None:
         tmp_path, ORCA_DEFAULT, keys="\r", env=_tab_env(tmp_path)
     )
     assert "Reopening" not in output
-    assert record["argv"] == [*ORCA_FLAGS, ORCA_DEFAULT]
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, ORCA_DEFAULT]
     env = _tab_env(tmp_path, pane="tab-2:leaf-1")
     _, record = _orca_tty(tmp_path, ORCA_DEFAULT, keys=None, env=env)
     assert record["argv"][-2:] == ["--resume", SESSION_ID]
@@ -1953,7 +2037,9 @@ def test_ask_prints_only_the_name_on_stdout(tmp_path: Path) -> None:
     env = _orca_env(tmp_path)
     _seed_label(tmp_path, "demo")
     command = [str(SKILL_DIR / "ccsession"), "--ask"]
-    question = "Session name (Enter = untagged, Ctrl+C = plain shell): "
+    question = (
+        "Session name (Enter = untagged, Ctrl+C = plain shell; gives up after 30s): "
+    )
     proc, master = _spawn_on_pty(
         command, env, tmp_path / "work", stdout=subprocess.PIPE
     )
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index a4d18431..d837d285 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -421,7 +421,12 @@ def test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier(
 
     session = "abc12345-0000-0000-0000-000000000000"
     env = _launch_env(tmp_path)
-    for name in ("CLAUDECODE", "XDG_STATE_HOME", "CCSESSION_ASK_TIMEOUT"):
+    for name in (
+        "CLAUDECODE",
+        "XDG_STATE_HOME",
+        "CCSESSION_ASK_TIMEOUT",
+        "CCSESSION_NAME",
+    ):
         env.pop(name, None)
     env.update(ORCA_PANE_KEY="tab-1:leaf-1", ORCA_TERMINAL_HANDLE="term_after")
     folder = str(tmp_path.resolve())
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
