8e0aa4769daecdba07cac3080bf79ea32da9019b
Review one task for spec compliance.

Task brief: ## Task 7: Add pseudo-terminal tests for every launch path the plan table lists

Depends on: Task 5

Add tests to tests/unit/test_ccsession_tag.py, one per launch path this repo controls, each run through ccsession-orca on a pseudo-terminal or without one in a throwaway HOME: the Claude button (no arguments, terminal: question, name, Enter, timeout); a worktree-create or agent-launch launch with a prompt (terminal and no terminal: no question, auto-name, prompt last); worker-start without a prompt (CCSESSION_NAME given: no question, label is the name; nothing given and a task typed ahead of the question: no question, the typed text stays for Claude); the typed-line safety net (long line, tab line, paste, ordinary name with spaces); resume (`--resume`, `--continue`, `--fork-session`: no question, no label); the pull request 355 plain relaunch (reopens, no question); a plain relaunch of a tab with no record (asked); print mode `-p` (untagged); CCSESSION_AUTOSTART=0 (untagged); Claude `--name x` and `CCSESSION_NAME=x` (label x, one `--name` in Claude's arguments); an auto-named session is listed by `ccsession --here` once the session hook records it.

Acceptance criteria:
- T7.AC1: `uv run pytest tests/unit/test_ccsession_tag.py -k orca -v` passes with a test for every path listed above, each asserting the question shown or not shown, the topic, and the exact Claude arguments from the fake Claude record.
- T7.AC2: The launch-path results (path, expected, observed) are written to ./artifacts/launch-paths.md in this package by the final test run.
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
Start sha: 8e0aa4769daecdba07cac3080bf79ea32da9019b
Diff against the start snapshot: diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index dd595563..46a5bbc4 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -1683,8 +1683,19 @@ def test_orca_a_line_that_cannot_be_a_name_goes_to_claude_as_a_message(
         ("--resume", SESSION_ID, "--fork-session"),
         (f"--resume={SESSION_ID}",),
         ("--continue",),
+        ("-r", SESSION_ID),
+        ("--fork-session",),
+        ("--from-pr", "12"),
+    ],
+    ids=[
+        "resume",
+        "resume-fork",
+        "resume-equals",
+        "continue",
+        "resume-short",
+        "fork-session-alone",
+        "from-pr",
     ],
-    ids=["resume", "resume-fork", "resume-equals", "continue"],
 )
 def test_orca_resume_skips_the_question(tmp_path: Path, args: tuple[str, ...]) -> None:
     _seed_label(tmp_path, "demo")
@@ -2527,6 +2538,223 @@ print(json.dumps({"disable": os.environ.get("CLAUDE_CODE_DISABLE_TERMINAL_TITLE"
     return output, json.loads(last[last.index("{") :])
 
 
+# Every launch path this repo controls, run through ccsession-orca (the real
+# wrapper and ccsession, a fake claude that records its arguments). Each test
+# asserts whether the question is shown, the session's topic and the exact
+# arguments Claude received.
+
+
+@pytest.mark.parametrize("terminal", [True, False], ids=["terminal", "no-terminal"])
+def test_orca_launch_with_a_prompt_is_auto_named_and_never_asked(
+    tmp_path: Path, terminal: bool
+) -> None:
+    # An agent or worktree launch that carries its task.
+    if terminal:
+        output, record = _orca_tty(tmp_path, "fix the login bug", keys=None)
+    else:
+        output, record = _orca_no_tty(tmp_path, "fix the login bug")
+    assert "Session name" not in output
+    label = _auto_label(record)
+    assert label.startswith("work-fix-the-login-bug-")
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "fix the login bug"]
+    _assert_through_shim(record)
+
+
+def test_orca_launch_with_nothing_and_no_terminal_is_auto_named(
+    tmp_path: Path,
+) -> None:
+    # A worker start with neither a task nor a name, and nobody to ask.
+    output, record = _orca_no_tty(tmp_path)
+    assert "Session name" not in output
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label]
+
+
+@pytest.mark.parametrize("terminal", [True, False], ids=["terminal", "no-terminal"])
+@pytest.mark.parametrize("prompt", [None, "do the thing"], ids=["no-prompt", "prompt"])
+def test_orca_ccsession_name_names_the_session_and_is_never_asked(
+    tmp_path: Path, terminal: bool, prompt: str | None
+) -> None:
+    # A worker start that names its session in the environment.
+    args = (prompt,) if prompt else ()
+    env = _orca_env(tmp_path, CCSESSION_NAME="worker-7")
+    if terminal:
+        output, record = _orca_tty(tmp_path, *args, keys=None, env=env)
+    else:
+        output, record = _orca_no_tty(tmp_path, *args, CCSESSION_NAME="worker-7")
+    assert "Session name" not in output
+    assert record["topic"] == "worker-7"
+    assert record["argv"] == [*ORCA_FLAGS, "--name", "worker-7", *args]
+    assert "CCSESSION_NAME" not in record["env_names"]
+    _assert_through_shim(record)
+
+
+@pytest.mark.parametrize(
+    "bad",
+    ["bad\tname", "x" * 300, "two\nlines", "   "],
+    ids=["tab", "300 characters", "newline", "blank"],
+)
+def test_orca_invalid_ccsession_name_never_stops_claude(
+    tmp_path: Path, bad: str
+) -> None:
+    # Dropped with a warning; the launch is then handled as if none was given.
+    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME=bad)
+    assert "CCSESSION_NAME is not a valid session name" in output
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "go"]
+    assert "CCSESSION_NAME" not in record["env_names"]
+    # With no task and a terminal, the question is asked after all.
+    tmp2 = tmp_path / "again"
+    tmp2.mkdir()
+    env = _orca_env(tmp2, CCSESSION_NAME=bad)
+    output, record = _orca_tty(tmp2, keys="\r", env=env)
+    assert "CCSESSION_NAME is not a valid session name" in output
+    assert record["argv"] == [*ORCA_FLAGS, "--name", _auto_label(record)]
+
+
+def test_orca_ccsession_name_equal_to_a_saved_label_resumes_it_loudly(
+    tmp_path: Path,
+) -> None:
+    _seed_label(tmp_path, "worker-7")
+    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME="worker-7")
+    assert "Resuming 'worker-7'" in output
+    assert record["argv"] == [
+        *ORCA_FLAGS,
+        "--name",
+        "worker-7",
+        "--resume",
+        SESSION_ID,
+        "go",
+    ]
+
+
+def test_orca_ccsession_name_longer_than_the_limit_is_dropped_not_cut(
+    tmp_path: Path,
+) -> None:
+    # 245 bytes is the longest name; one more is not shortened into a name.
+    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME="n" * 245)
+    assert record["topic"] == "n" * 245
+    output, record = _orca_no_tty(tmp_path, "go", CCSESSION_NAME="n" * 246)
+    assert record["topic"] != "n" * 246
+    assert _auto_label(record)
+
+
+@pytest.mark.parametrize(
+    ("keys", "message", "separator"),
+    [
+        ("line one\rline two\r", "line one\nline two", False),
+        ("- item one\r- item two\r", "- item one\n- item two", True),
+        ("-starts with a dash and is too long " + "x" * 250 + "\r", None, True),
+    ],
+    ids=["paste", "dash-paste", "dash-too-long"],
+)
+def test_orca_typed_text_that_cannot_be_a_name_is_claudes_first_message(
+    tmp_path: Path, keys: str, message: str | None, separator: bool
+) -> None:
+    message = message or keys.rstrip("\r")
+    output, record = _orca_tty(tmp_path, keys=keys)
+    label = _auto_label(record)
+    tail = ["--", message] if separator else [message]
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, *tail]
+
+
+@pytest.mark.parametrize(
+    "args",
+    [("-p", "hello"), ("--print", "hello"), ("-p",)],
+    ids=["-p", "--print", "-p-only"],
+)
+def test_orca_print_mode_is_untagged_and_never_asked(
+    tmp_path: Path, args: tuple[str, ...]
+) -> None:
+    output, record = _orca_tty(tmp_path, *args, keys=None)
+    assert "Session name" not in output
+    assert record["topic"] is None
+    assert record["argv"] == [*ORCA_FLAGS, *args]
+    output, record = _orca_no_tty(tmp_path, *args)
+    assert record["topic"] is None
+    assert record["argv"] == [*ORCA_FLAGS, *args]
+
+
+@pytest.mark.parametrize(
+    "args",
+    [("--version",), ("-h",), ("mcp", "list"), ("doctor",)],
+    ids=["version", "help", "mcp", "doctor"],
+)
+def test_orca_commands_that_start_no_session_get_no_name_and_no_question(
+    tmp_path: Path, args: tuple[str, ...]
+) -> None:
+    output, record = _orca_tty(tmp_path, *args, keys=None)
+    assert "Session name" not in output
+    assert record["topic"] is None
+    assert record["argv"] == [*ORCA_FLAGS, *args]
+
+
+@pytest.mark.parametrize(
+    "name_args",
+    [("--name", "mine"), ("-n", "mine"), ("--name=mine",)],
+    ids=["--name", "-n", "--name="],
+)
+def test_orca_claude_name_is_kept_once_and_never_asked(
+    tmp_path: Path, name_args: tuple[str, ...]
+) -> None:
+    for terminal in (True, False):
+        if terminal:
+            output, record = _orca_tty(tmp_path, *name_args, "go", keys=None)
+        else:
+            output, record = _orca_no_tty(tmp_path, *name_args, "go")
+        assert "Session name" not in output
+        assert record["topic"] is None
+        assert record["argv"] == [*ORCA_FLAGS, *name_args, "go"]
+        # One --name for Claude, not a second one from ccsession.
+        assert (
+            sum(
+                a in ("--name", "-n") or a.startswith("--name=") for a in record["argv"]
+            )
+            == 1
+        )
+
+
+def test_orca_session_id_launch_carries_a_task_and_is_auto_named(
+    tmp_path: Path,
+) -> None:
+    # --session-id starts a chosen new session: no question, but a name.
+    sid = "11111111-2222-3333-4444-555555555555"
+    output, record = _orca_tty(tmp_path, "--session-id", sid, keys=None)
+    assert "Session name" not in output
+    label = _auto_label(record)
+    assert record["argv"] == [*ORCA_FLAGS, "--name", label, "--session-id", sid]
+
+
+def test_orca_autostart_off_with_no_task_is_untagged_and_never_asked(
+    tmp_path: Path,
+) -> None:
+    env = _orca_env(tmp_path, CCSESSION_AUTOSTART="0")
+    output, record = _orca_tty(tmp_path, keys=None, env=env)
+    assert "Session name" not in output
+    assert record["topic"] is None
+    assert record["argv"] == ORCA_FLAGS
+
+
+def test_orca_auto_named_session_is_listed_once_the_session_hook_records_it(
+    tmp_path: Path,
+) -> None:
+    _, record = _orca_no_tty(tmp_path, "fix the login bug")
+    label = _auto_label(record)
+    env = _orca_env(tmp_path)
+    work = (tmp_path / "work").resolve()
+    projects = tmp_path / "home" / ".claude" / "projects"
+    # The hook that Claude Code runs at session start saves the launch's name;
+    # the topic Claude was started with is the one it saves.
+    _hook(
+        {**env, "CLAUDE_TOPIC": record["topic"], "CCSESSION_TOPIC_CWD": str(work)},
+        work,
+        SESSION_ID,
+        "SessionStart",
+    )
+    _transcript(projects, work, SESSION_ID)
+    assert _listed(work, env, "--here") == {label: SESSION_ID[:8]}
+
+
 def test_orca_terminal_title_keeps_claude_recognisable(tmp_path: Path) -> None:
     # Untagged: plain "Claude Code", and Claude Code must not overwrite it.
     output, claude = _title_launch(tmp_path)
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
