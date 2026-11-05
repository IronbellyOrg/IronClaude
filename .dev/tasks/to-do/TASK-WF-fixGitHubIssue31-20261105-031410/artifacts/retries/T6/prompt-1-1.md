68452bae4a42000ec0997738b027d452c5256ffc
Review one task for spec compliance.

Task brief: ## Task 6: Add tests for the auto-name helper and the question outcomes

Depends on: Task 5

Add tests to tests/unit/test_ccsession_tag.py for `ccsession --auto-name` (valid and shell-safe for hostile text, 80-character cap, unique against saved topics with -2 and -3, no text) and for `ccsession --ask` (default 30-second limit shown in the hint, exit 1 on timeout, exit 3 for the 246-byte line, the tab line and the two-line paste, exit 0 and a name for `my fix plan`, `*` still lists, a blank line still means Enter).

Acceptance criteria:
- T6.AC1: `uv run pytest tests/unit/test_ccsession_tag.py -k "auto_name or ask" -v` passes with at least one test per listed case.
- T6.AC2: Each new test fails when the matching behaviour in ccsession is reverted (checked once by temporarily reverting the exit 3 path and seeing the paste test fail, then restoring it).
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
Start sha: 68452bae4a42000ec0997738b027d452c5256ffc
Diff against the start snapshot: diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index 03dfa838..b336de73 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -1302,7 +1302,9 @@ def test_plain_double_dash_still_reaches_claude(tmp_path: Path) -> None:
 # the real ccsession against a fake claude that records its argv and env, and a
 # fake shim that ccsession reuses.
 ORCA = SKILL_DIR / "ccsession-orca"
-ORCA_QUESTION = "Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s): "
+ORCA_QUESTION = (
+    "Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s): "
+)
 # What ccsession --auto-name makes in the tests' working folder "work": the
 # folder, up to four words of the task, then month-day, time with seconds and a
 # random part.
@@ -2088,6 +2090,383 @@ def test_ask_prints_only_the_name_on_stdout(tmp_path: Path) -> None:
     assert (no_tty.returncode, no_tty.stdout) == (1, b"")
 
 
+# ccsession --auto-name: the label for a launch that carries no name.
+AUTO_STAMP = r"\d{4}-\d{6}-[0-9a-f]{4}"
+
+
+def _auto_name(
+    tmp_path: Path, text: str | None = None, cwd: Path | None = None, **extra: str
+) -> subprocess.CompletedProcess:
+    """Run `ccsession --auto-name [text]` in the test's work folder, no terminal."""
+    command = [str(SKILL_DIR / "ccsession"), "--auto-name"]
+    if text is not None:
+        command.append(text)
+    return subprocess.run(
+        command,
+        env=_orca_env(tmp_path, **extra),
+        cwd=cwd or tmp_path / "work",
+        stdin=subprocess.DEVNULL,
+        capture_output=True,
+        text=True,
+        timeout=60,
+    )
+
+
+def test_auto_name_without_text_is_the_folder_and_a_stamp(tmp_path: Path) -> None:
+    result = _auto_name(tmp_path)
+    assert result.returncode == 0, result.stderr
+    assert re.fullmatch(rf"work-{AUTO_STAMP}\n", result.stdout), result.stdout
+
+
+@pytest.mark.parametrize(
+    "text",
+    [
+        "fix the 'login' bug and say \"done\"",
+        "$(touch PWNED) `touch PWNED` ; touch PWNED",
+        "../../etc/passwd",
+        "\x1b[31mred\x1b[0m\x07 bell",
+        "line one\nline two\n\tindented",
+        "--model",
+        "--claude-args",
+        "--shim",
+        "--tier=x",
+        "--name",
+        "あいう えお",
+        "%2F %s %n",
+        "!!!",
+    ],
+    ids=[
+        "quotes",
+        "command substitution",
+        "path",
+        "escape codes",
+        "several lines",
+        "--model",
+        "--claude-args",
+        "--shim",
+        "--tier=x",
+        "--name",
+        "CJK",
+        "format characters",
+        "punctuation only",
+    ],
+)
+def test_auto_name_is_valid_and_shell_safe_for_any_text(
+    tmp_path: Path, text: str
+) -> None:
+    result = _auto_name(tmp_path, text)
+    assert result.returncode == 0, result.stderr
+    # One line, only a-z, 0-9 and hyphens (the folder here is lower case), and a
+    # label ccsession itself accepts. Nothing in the text was run.
+    assert re.fullmatch(rf"work(-[a-z0-9]+)*-{AUTO_STAMP}\n", result.stdout), (
+        result.stdout
+    )
+    label = result.stdout.strip()
+    check = subprocess.run(
+        [str(SKILL_DIR / "ccsession"), "--check-name", label],
+        env=_orca_env(tmp_path),
+        stdin=subprocess.DEVNULL,
+    )
+    assert check.returncode == 0
+    assert not (tmp_path / "work" / "PWNED").exists()
+
+
+def test_auto_name_uses_at_most_four_words_of_twelve_characters(tmp_path: Path) -> None:
+    result = _auto_name(
+        tmp_path, "Alpha beta GAMMA delta epsilon abcdefghijklmnopqrstuvwxyz"
+    )
+    assert re.fullmatch(
+        rf"work-alpha-beta-gamma-delta-{AUTO_STAMP}\n", result.stdout
+    ), result.stdout
+    result = _auto_name(tmp_path, "abcdefghijklmnopqrstuvwxyz")
+    assert re.fullmatch(rf"work-abcdefghijkl-{AUTO_STAMP}\n", result.stdout), (
+        result.stdout
+    )
+
+
+def test_auto_name_stays_short_and_keeps_its_stamp_for_a_long_folder(
+    tmp_path: Path,
+) -> None:
+    folder = tmp_path / ("x" * 100)
+    folder.mkdir()
+    result = _auto_name(tmp_path, "alpha beta gamma delta " + "z" * 400, cwd=folder)
+    label = result.stdout.strip()
+    # Folder name cut to 20 characters, four words cut to 12 characters each; the
+    # label stays well under the 80-character cap and still ends in the stamp.
+    assert len(label) <= 80, label
+    assert re.fullmatch(rf"x{{20}}-alpha-beta-gamma-delta-{AUTO_STAMP}", label), label
+
+
+def test_auto_name_two_calls_in_the_same_second_differ(tmp_path: Path) -> None:
+    labels = {_auto_name(tmp_path, "same task").stdout for _ in range(3)}
+    # The random part differs (a 1 in 65536 chance for each pair to match).
+    assert len(labels) >= 2
+
+
+def test_auto_name_never_equals_a_saved_name(tmp_path: Path) -> None:
+    # A saved name resumes its session, so an auto-name must be a new one: when
+    # the label is taken it gets -2, then -3.
+    stamp = "0101-000000-aaaa"
+    base = f"work-same-task-{stamp}"
+    _orca_env(tmp_path)
+    _seed_label(tmp_path, base)
+    result = _auto_name(tmp_path, "same task", CCSESSION_AUTO_NAME_STAMP=stamp)
+    assert result.stdout == f"{base}-2\n"
+    _seed_label(tmp_path, f"{base}-2")
+    result = _auto_name(tmp_path, "same task", CCSESSION_AUTO_NAME_STAMP=stamp)
+    assert result.stdout == f"{base}-3\n"
+    # Another task, or no saved label, is not touched.
+    assert (
+        _auto_name(tmp_path, "other", CCSESSION_AUTO_NAME_STAMP=stamp).stdout
+        == f"work-other-{stamp}\n"
+    )
+
+
+@pytest.mark.skipif(os.geteuid() == 0, reason="root can write to any folder")
+def test_auto_name_prints_nothing_when_the_name_list_cannot_be_written(
+    tmp_path: Path,
+) -> None:
+    # A launch under a label would stop at the save; with no label, the caller
+    # starts Claude without a name instead.
+    _orca_env(tmp_path)
+    projects = tmp_path / "home" / ".claude" / "projects"
+    projects.mkdir(parents=True)
+    projects.chmod(0o500)
+    try:
+        result = _auto_name(tmp_path, "fix it")
+    finally:
+        projects.chmod(0o700)
+    assert (result.returncode, result.stdout) == (1, "")
+
+
+def test_auto_name_stamp_override_is_cut_to_safe_characters(tmp_path: Path) -> None:
+    result = _auto_name(tmp_path, "x", CCSESSION_AUTO_NAME_STAMP="0101-000000-a b/c;d")
+    assert result.stdout == "work-x-0101-000000-a-b-c-d\n"
+
+
+def test_auto_name_in_a_hidden_folder_with_cjk_characters_is_still_valid(
+    tmp_path: Path,
+) -> None:
+    folder = tmp_path / ".hidden-あいう"
+    folder.mkdir()
+    result = _auto_name(tmp_path, "task", cwd=folder)
+    assert re.fullmatch(rf"hidden-task-{AUTO_STAMP}\n", result.stdout), result.stdout
+
+
+def test_auto_name_check_name_judges_names_and_help_lists_the_new_options(
+    tmp_path: Path,
+) -> None:
+    env = _orca_env(tmp_path)
+    ccsession = str(SKILL_DIR / "ccsession")
+
+    def check(*args: str) -> subprocess.CompletedProcess:
+        return subprocess.run(
+            [ccsession, "--check-name", *args],
+            env=env,
+            stdin=subprocess.DEVNULL,
+            capture_output=True,
+            text=True,
+        )
+
+    for good in ("demo", "my fix plan", "y" * 245):
+        assert check(good).returncode == 0, good
+    for bad in ("", "   ", "bad\tname", "two\nlines", "x" * 246, "あ" * 82):
+        result = check(bad)
+        # Only the status answers; nothing is printed.
+        assert (result.returncode, result.stdout, result.stderr) == (1, "", ""), bad
+    assert check().returncode == 1
+
+    help_text = subprocess.run(
+        [ccsession, "--help"],
+        env=env,
+        stdin=subprocess.DEVNULL,
+        capture_output=True,
+        text=True,
+    ).stdout
+    for text in ("--auto-name", "--check-name", "@LIMIT@", "130 Ctrl+C"):
+        assert text in help_text, text
+
+
+# ccsession --ask on a terminal: the naming question and its exit codes.
+def _ask_on_pty(
+    tmp_path: Path,
+    steps: list[tuple[float, bytes]],
+    *args: str,
+    env: dict[str, str] | None = None,
+    typed_ahead: bytes = b"",
+) -> tuple[int, bytes, str, bool, float]:
+    """Run `ccsession --ask [hint]` on a terminal, then play the steps.
+
+    Each step is (seconds to wait, bytes to type). Returns the exit status,
+    what it printed on stdout, what the terminal showed, whether the terminal is
+    back in line mode, and how long the run took.
+    """
+    env = env or _orca_env(tmp_path)
+    started = time.monotonic()
+    proc, master = _spawn_on_pty(
+        [str(SKILL_DIR / "ccsession"), "--ask", *args],
+        env,
+        tmp_path / "work",
+        typed_ahead.decode(),
+        stdout=subprocess.PIPE,
+    )
+    try:
+        shown = _read_pty(master, until="): ", timeout=15)
+        for delay, data in steps:
+            time.sleep(delay)
+            os.write(master, data)
+        stdout = proc.communicate(timeout=60)[0]
+        shown += _read_pty(master, timeout=5)
+        line_mode = bool(termios.tcgetattr(master)[3] & termios.ICANON)
+    finally:
+        if proc.poll() is None:
+            proc.kill()
+        os.close(master)
+    return proc.returncode, stdout, shown, line_mode, time.monotonic() - started
+
+
+def test_ask_default_limit_is_30_seconds_and_shown_in_the_question(
+    tmp_path: Path,
+) -> None:
+    status, stdout, shown, line_mode, _ = _ask_on_pty(tmp_path, [(0.3, b"\x03")])
+    assert "Enter = untagged, Ctrl+C = plain shell; gives up after 30s): " in shown
+    assert (status, stdout) == (130, b"")
+    assert line_mode
+
+
+def test_ask_gives_up_after_the_limit_with_exit_1(tmp_path: Path) -> None:
+    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="1")
+    status, stdout, shown, line_mode, seconds = _ask_on_pty(tmp_path, [], env=env)
+    assert "gives up after 1s): " in shown
+    assert (status, stdout) == (1, b"")
+    assert line_mode
+    assert seconds < 20
+
+
+def test_ask_limit_0_waits_for_ever_and_drops_the_limit_from_the_question(
+    tmp_path: Path,
+) -> None:
+    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="0")
+    status, stdout, shown, _, _ = _ask_on_pty(tmp_path, [(1.5, b"\x03")], env=env)
+    assert "gives up" not in shown
+    assert (status, stdout) == (130, b"")
+    # Not a number: the same as no limit.
+    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="soon")
+    status, stdout, shown, _, _ = _ask_on_pty(tmp_path, [(0.3, b"\x03")], env=env)
+    assert "gives up" not in shown
+    assert (status, stdout) == (130, b"")
+
+
+def test_ask_hint_placeholder_follows_the_limit(tmp_path: Path) -> None:
+    hint = "Enter = auto-named; auto-named after @LIMIT@s"
+    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="2")
+    _, _, shown, _, _ = _ask_on_pty(tmp_path, [(0.3, b"\x03")], hint, env=env)
+    assert "Session name (Enter = auto-named; auto-named after 2s): " in shown
+    # No limit: the part of the hint that names it goes, with its separator.
+    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="0")
+    _, _, shown, _, _ = _ask_on_pty(tmp_path, [(0.3, b"\x03")], hint, env=env)
+    assert "Session name (Enter = auto-named): " in shown
+    assert "@LIMIT@" not in shown
+
+
+def test_orca_ask_question_hint_follows_the_limit_and_the_timeout_auto_names(
+    tmp_path: Path,
+) -> None:
+    env = _orca_env(tmp_path, CCSESSION_ASK_TIMEOUT="2")
+    proc, master = _spawn_on_pty([str(ORCA)], env, tmp_path / "work")
+    try:
+        shown = _read_pty(master, until="auto-named after 2s): ")
+        assert (
+            "Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 2s): "
+            in shown
+        )
+        shown += _read_pty(master)
+        assert proc.wait(timeout=60) == 0, shown
+    finally:
+        if proc.poll() is None:
+            proc.kill()
+        os.close(master)
+    record = json.loads((tmp_path / "record.json").read_text())
+    assert record["topic"] == _auto_label(record)
+    assert "CCSESSION_ASK_TIMEOUT" not in record["env_names"]
+
+
+@pytest.mark.parametrize(
+    ("steps", "text"),
+    [
+        ([(0.2, b"x" * 246 + b"\r")], b"x" * 246),
+        ([(0.2, "あ".encode() * 82 + b"\r")], "あ".encode() * 82),
+        ([(0.2, b"foo\tbar\r")], b"foo\tbar"),
+        ([(0.2, b"\tfoo\r")], b"\tfoo"),
+        ([(0.2, b"foo\t\r")], b"foo\t"),
+        ([(0.2, b"line one\rline two\r")], b"line one\nline two"),
+        ([(0.2, b"line one\r"), (0.05, b"line two\r")], b"line one\nline two"),
+    ],
+    ids=[
+        "246 bytes",
+        "82 CJK characters",
+        "inner tab",
+        "leading tab",
+        "trailing tab",
+        "paste in one write",
+        "paste in two writes",
+    ],
+)
+def test_ask_a_line_that_cannot_be_a_name_exits_3_and_prints_it_as_typed(
+    tmp_path: Path, steps: list[tuple[float, bytes]], text: bytes
+) -> None:
+    status, stdout, _, line_mode, _ = _ask_on_pty(tmp_path, steps)
+    assert (status, stdout) == (3, text)
+    assert line_mode
+
+
+def test_ask_a_name_with_spaces_is_a_name(tmp_path: Path) -> None:
+    status, stdout, _, _, _ = _ask_on_pty(tmp_path, [(0.2, b"my fix plan\r")])
+    assert (status, stdout) == (0, b"my fix plan\n")
+    # Surrounding spaces are not part of the name.
+    status, stdout, _, _, _ = _ask_on_pty(tmp_path, [(0.2, b"  padded name  \r")])
+    assert (status, stdout) == (0, b"padded name\n")
+    # 245 bytes is the longest name.
+    status, stdout, _, _, _ = _ask_on_pty(tmp_path, [(0.2, b"y" * 245 + b"\r")])
+    assert (status, stdout) == (0, b"y" * 245 + b"\n")
+
+
+def test_ask_a_blank_line_means_enter(tmp_path: Path) -> None:
+    status, stdout, _, line_mode, _ = _ask_on_pty(tmp_path, [(0.2, b"\r")])
+    assert (status, stdout) == (0, b"\n")
+    assert line_mode
+
+
+def test_ask_star_lists_the_saved_sessions_and_asks_again(tmp_path: Path) -> None:
+    _orca_env(tmp_path)
+    _seed_label(tmp_path, "demo")
+    status, stdout, shown, _, _ = _ask_on_pty(
+        tmp_path, [(0.2, b"*\r"), (0.5, b"after star\r")]
+    )
+    assert (status, stdout) == (0, b"after star\n")
+    # Listed once with the question and once more for the star.
+    assert shown.count("Saved sessions in") == 2
+
+
+def test_ask_is_not_asked_when_keys_are_already_waiting(tmp_path: Path) -> None:
+    # Typed ahead means someone is already at the keyboard with a task for Claude.
+    status, stdout, shown, _, _ = _ask_on_pty(tmp_path, [], typed_ahead=b"x")
+    assert (status, stdout) == (1, b"")
+    assert "Session name" not in shown
+
+
+def test_ask_ctrl_c_while_pasted_text_is_collected_exits_130_and_restores(
+    tmp_path: Path,
+) -> None:
+    # After a line, --ask waits briefly for more pasted lines with line mode off;
+    # Ctrl+C in that window must still end it with line mode back on.
+    status, stdout, _, line_mode, _ = _ask_on_pty(
+        tmp_path, [(0.2, b"some name\r"), (0.04, b"\x03")]
+    )
+    assert (status, stdout) == (130, b"")
+    assert line_mode
+
+
 def _title_launch(
     tmp_path: Path, *args: str, orca: bool = True
 ) -> tuple[bytes, dict[str, str]]:
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
