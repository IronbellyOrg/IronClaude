da3c0b47cfc5a8bfde13ed504e937d6b0c797cc6
Review one task for spec compliance.

Task brief: 
## Task 12: Add the `--questions` flag and the gate guard to commands.py

Depends on: Task 9, Task 10

Edit `src/superclaude/cli/observe/commands.py` and add tests to `tests/observe/test_commands.py` and `tests/observe/test_registration.py`.

- Add option `--questions` (flag). It requires `--run <runId>` (checked with `check_run_id`) and a live source; with `--fixture`, without `--run`, or with a malformed run id the command exits non-zero with a plain message and runs no Orca call.
- Add one module constant `QUESTION_GATE_PASSED = False` with a comment naming `release-gates.md` and Task 18. While False, `--questions` exits non-zero with `question read not enabled: QUESTION-OBSERVATION has not passed` and makes no Orca call, not even discovery.
- Pass `questions=True` into the `Collector` only past the guard. Update `HELP` with: the one-named-Run rule, "run it from the terminal that already holds the Run; the observer never runs run-use", the disclosure label, and "message bodies are received by this process; subjects are shown, bodies are not kept".

Acceptance criteria:
- `uv run pytest tests/observe/test_commands.py tests/observe/test_registration.py -v` passes: T56 (guard False: exit non-zero, empty argv log); with the constant monkeypatched True, `--run run_14cfcbd8edf2 --questions --once` through the fake runner logs worker-list calls plus one template message call and prints the panel; `--questions` without `--run`, with `--fixture`, and with `--run -x` are refused with no Orca call; the `--help` text contains `never runs run-use`.

Global constraints: 
## Constraints

- Shorthand. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. REPORT is the file `RESEARCH-REPORT-phase2-gate.md` in the folder `TASK-RESEARCH-phase2-gate-20261111-200400` under `.dev/tasks/` (the folder may sit in to-do or done); its recorded evidence is the `research/evidence/` folder next to it, files numbered 01 to 27. OWNER is `.dev/issues/409/owner-decisions-20261111.md`. "The probe shapes" are the recorded outputs in REPORT's evidence folder: envelope `{id, ok, result:{acknowledged, count, messages[], runId}, _meta}`; message row keys `id` (msg_...), `run_id`, `delivery_contract`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `created_at`, `delivered_at`; error envelope `{ok:false, error:{code, message}}` with codes `consumer_fenced` (exit status 1) and `no_active_terminal`.
- Scope is release 2 only, as fixed by OWNER and REPORT sections 7 to 9. Decision 8: only messages of type `question`, labelled "coordinator questions", never "human". Decision 6: read permission for one named Run, `--types question`, never `run-use`. The owner has not yet named the Run (open question for the owner; Task 17 is blocked until they do).
- Fixed design basis, not reopened. One named Run only; no rotation across Runs; the observer runs where it already holds the Run. Every read passes `--types question`. Only `check --all` is used: `--peek` hides acked rows so it is not a source. Question identity is `message.id`, labelled UNVERIFIED for any Run other than the probe Runs and the coordinator's own Run; a worker `dispatchId` is never a question identity. The disclosure text, verbatim, is `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.
- UNVERIFIED facts that stay gated risks, each with a named verification task and never an assumption. Q-1: whether an observer terminal that has a handle but holds no Run can read (Task 16). Q-2: the effect of `run-use` on a live coordinator (not tested, forbidden for the observer; Task 6 pins `run-use` as a forbidden argv and Task 2 records Q-2 as never tested). Message rate on a Run other than the coordinator's own, and identity on real traffic (Task 17). Whether `ask` writes type `question` (Q-3) is recorded in the register as UNVERIFIED; no R2 behaviour depends on it because the label says "coordinator questions" and the observer lists type `question` rows however they were written.
- Safety. No consuming read (`check` without `--all` or `--peek`, `check --ack`), no `run-use`, `run-create`, `send`, `ask`, `reply` or `reset` against any Run except where a task names a throwaway probe Run and a non-consuming form. Raw Orca output is never logged, committed or exported; committed samples hold only redacted values (no terminal handle, token, credential or absolute path). Bodies of messages are received by the observer process (acquisition cannot be undone by dropping them at parse time), so the design never claims bodies were not acquired; it only does not keep or show them.
- Rules carried from release 1. UV only (`uv run pytest ...`). Python 3.10 compatible, no new dependency. A fact the source does not give is the `UNKNOWN` sentinel and renders as `unknown`; unknown is never 0, false, blank or `null`. Source loss never closes a question, lowers an open count or turns a value into `failed`. Every source string passes `sanitize` before it reaches the view model; strings render as literal text, never Rich markup; truncation uses cell width. Plan edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Out of scope: R3 links (QUESTION-LINK), `inbox`, closure evidence, history beyond the 100-row window, `--include-remote`, write-back, per-question selection and marking (the `m` key keeps its release 1 meaning), any message call other than the one template.
- Plan-author choices (PROPOSED, the owner may change them). The opt-in flag is `--questions`, valid only with `--run <runId>` and a live source. The message call budget is one call per cycle; when questions are on, worker-list paging is limited to 4 calls so the cycle total stays inside the 5-call cap. The panel shows `subject` and age only, never `body`. The reason column reads `reason unknown` because no verified reason field exists. Retention is in memory for the process, bounded at 1,000 records.
- Gate honesty. QUESTION-OBSERVATION is NOT passed as of this plan: proof (a) failed as worded, proof (b) is partly proven, proof (c) is unmeasured, non-consumption passed only as the Run's owner on a probe Run. The live question read is guarded by one constant that Task 18 may flip only against an owner-written record.

Start sha: da3c0b47cfc5a8bfde13ed504e937d6b0c797cc6
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/commands.py b/src/superclaude/cli/observe/commands.py
index ccb220b7a..f85be55b8 100644
--- a/src/superclaude/cli/observe/commands.py
+++ b/src/superclaude/cli/observe/commands.py
@@ -60,6 +60,21 @@ REDRAW_SECONDS = (
 )
 WIDTHS = ("160", "116", "80")
 
+# The live coordinator-questions read is guarded by this one constant. It stays False until
+# the owner has written a record that QUESTION-OBSERVATION passed (release-gates.md, "Agents
+# cite the owner's statement, never write it"); plan Task 18 may flip it only against that
+# record, cited by path. While False, ``--questions`` makes no Orca call, not even discovery.
+QUESTION_GATE_PASSED = False
+QUESTION_GATE_TEXT = (
+    "question read not enabled: QUESTION-OBSERVATION has not passed"  # PROPOSED wording
+)
+QUESTIONS_NEED_RUN_TEXT = (
+    "--questions needs --run <runId>: it reads the questions of one named Run only"
+)
+QUESTIONS_NEED_LIVE_TEXT = (
+    "--questions needs a live source; it cannot be combined with --fixture"
+)
+
 HELP = """Read-only terminal observer for Orca workers.
 
 Shows the worker ledger Orca reports for its workers (verbatim next-action kind,
@@ -68,6 +83,13 @@ snapshot. It never writes to Orca: no key and no option maps to an Orca call.
 
 Poll caps (one read every 15 s, at most 5 calls per read) are per observer process; several
 observers running at once multiply the load on Orca.
+
+Coordinator questions (--questions, off until the owner records that QUESTION-OBSERVATION
+passed): with --run <runId> the observer lists the messages of type question of that one
+named Run, from one read per cycle. Run it from the terminal that already holds the Run: the
+observer never runs run-use and never binds to a Run. The list is bounded best effort;
+coverage unknown; bursts over 100 rows between reads may be lost. Message bodies are
+received by this process; subjects are shown, bodies are not kept.
 """
 
 
@@ -98,6 +120,7 @@ class Options:
     fixture: str | None = None
     run_id: str | None = None
     snapshot: str | None = None
+    questions: bool = False  # R2: list the coordinator questions of the one --run Run
 
 
 @dataclass
@@ -142,6 +165,28 @@ def _build_source(options: Options, deps: Deps) -> Any:
     return LiveSource(deps.runner or production_runner, **kwargs)
 
 
+def _questions_on(options: Options) -> bool:
+    """True only when ``--questions`` is asked for and the gate guard is open."""
+    return bool(options.questions and QUESTION_GATE_PASSED)
+
+
+def _question_refusal(options: Options) -> tuple[int, str] | None:
+    """(exit code, plain message) when ``--questions`` cannot run; checked before any Orca call."""
+    if not options.questions:
+        return None
+    if options.fixture:
+        return 2, QUESTIONS_NEED_LIVE_TEXT
+    if not options.run_id:
+        return 2, QUESTIONS_NEED_RUN_TEXT
+    try:
+        check_run_id(options.run_id)
+    except ArgvRejected as exc:
+        return 2, f"--questions needs a valid --run id: {exc}"
+    if not QUESTION_GATE_PASSED:
+        return 1, QUESTION_GATE_TEXT
+    return None
+
+
 def _emit(text: str, deps: Deps) -> None:
     if deps.stdout is not None:
         deps.stdout.write(text)
@@ -170,7 +215,9 @@ def _write_snapshot(view: Any, target: Path) -> str | None:
 def run_once(options: Options, deps: Deps) -> int:
     clock = deps.clock or SystemClock()
     source = _build_source(options, deps)
-    collector = Collector(source, clock, run_id=options.run_id)
+    collector = Collector(
+        source, clock, run_id=options.run_id, questions=_questions_on(options)
+    )
     result = collector.run_once()
     session = apply_cycle(Session(), result, clock)
     view = build_view(result, session, clock)
@@ -305,6 +352,7 @@ def run_interactive(options: Options, deps: Deps) -> int:
             clock,
             interval=deps.interval if deps.interval is not None else 15.0,
             run_id=options.run_id,
+            questions=_questions_on(options),
         )
         directory = deps.state_directory or state_dir()
         live = not options.fixture
@@ -324,6 +372,10 @@ def run_interactive(options: Options, deps: Deps) -> int:
 
 def execute(options: Options, deps: Deps | None = None) -> int:
     """Run the command; returns the process exit code."""
+    refusal = _question_refusal(options)  # before any Orca call, discovery included
+    if refusal is not None:
+        click.echo(refusal[1], err=True)
+        return refusal[0]
     deps = deps or Deps()
     if options.once:
         return run_once(options, deps)
@@ -393,6 +445,13 @@ def _check_run(
     default=None,
     help="Write the JSON snapshot to this file (default for live mode: the per-user state directory).",
 )
+@click.option(
+    "--questions",
+    "questions",
+    is_flag=True,
+    help="List the coordinator questions (message type question) of the one Run named by "
+    "--run. Needs --run and a live source; refused until QUESTION-OBSERVATION has passed.",
+)
 @click.pass_context
 def observe_group(
     ctx: click.Context,
@@ -402,6 +461,7 @@ def observe_group(
     fixture: str | None,
     run_id: str | None,
     snapshot: str | None,
+    questions: bool,
 ) -> None:
     if ctx.invoked_subcommand is not None:
         return
@@ -412,6 +472,7 @@ def observe_group(
         fixture=fixture,
         run_id=run_id,
         snapshot=snapshot,
+        questions=questions,
     )
     code = execute(options)
     if code:
diff --git a/tests/observe/test_commands.py b/tests/observe/test_commands.py
index 1eb9fd0df..dc1ea5a0a 100644
--- a/tests/observe/test_commands.py
+++ b/tests/observe/test_commands.py
@@ -592,3 +592,151 @@ def test_no_module_other_than_the_adapter_imports_subprocess_and_none_names_an_o
         commands_text,
         re.M,
     )
+
+
+# -- R2: --questions and the gate guard (T56) --------------------------------------------------------------------------------
+
+from tests.observe.conftest import (  # noqa: E402
+    QRUN,
+    make_question_envelope,
+    make_question_rows,
+    routed_runner_responses,
+)
+
+
+def question_runner(argv_log, rows=None):
+    worker = reply(3)
+    rows = make_question_rows(4) if rows is None else rows
+    message = (0, json.dumps(make_question_envelope(rows)))
+    return FakeRunner(argv_log, [routed_runner_responses(worker, message)])
+
+
+def messages_in(argv_log):
+    return [a for a in argv_log if a[1:3] == ["orchestration", "check"]]
+
+
+def test_t56_with_the_guard_off_questions_is_refused_and_no_orca_call_is_made(
+    fake_clock, argv_log
+):
+    assert (
+        commands.QUESTION_GATE_PASSED is False
+    )  # ships OFF until the owner's record exists
+    runner = question_runner(argv_log)
+    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
+    code, out = once(Options(once=True, run_id=QRUN, questions=True), deps)
+    assert code != 0 and out == ""
+    assert argv_log == [] and runner.calls == 0  # not even discovery
+    via_click = CliRunner().invoke(
+        observe_group, ["--once", "--run", QRUN, "--questions"]
+    )
+    assert via_click.exit_code != 0
+    assert (
+        "question read not enabled: QUESTION-OBSERVATION has not passed"
+        in via_click.output
+    )
+
+
+def test_the_interactive_path_is_refused_too_with_the_guard_off(fake_clock, argv_log):
+    runner = question_runner(argv_log)
+    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
+    assert execute(Options(run_id=QRUN, questions=True), deps) != 0
+    assert argv_log == []
+
+
+def test_with_the_guard_open_one_template_message_call_follows_the_worker_list_calls(
+    fake_clock, argv_log, monkeypatch
+):
+    monkeypatch.setattr(commands, "QUESTION_GATE_PASSED", True)
+    runner = question_runner(argv_log)
+    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
+    code, out = once(Options(once=True, run_id=QRUN, questions=True), deps)
+    assert code == 0
+    message = messages_in(argv_log)
+    assert message == [
+        [
+            "/opt/fake/orca", "orchestration", "check", "--all", "--types", "question",
+            "--run", QRUN, "--json",
+        ]
+    ]  # fmt: skip
+    worker = [a for a in argv_log if a[1:3] == ["orchestration", "worker-list"]]
+    assert len(worker) == 1 and "--peek" not in message[0]
+    lines = out.splitlines()
+    assert "COORDINATOR QUESTIONS" in lines and f"one Run only: {QRUN}" in lines
+    assert sum("reason unknown" in l for l in lines) == 4
+    assert "observed open: 4 | closed by evidence: unavailable (no source)" in lines
+
+
+def test_with_the_guard_open_and_a_width_the_screen_shows_the_panel(
+    fake_clock, argv_log, monkeypatch
+):
+    monkeypatch.setattr(commands, "QUESTION_GATE_PASSED", True)
+    deps = deps_for(
+        fake_clock,
+        runner=question_runner(argv_log),
+        discover=FakeDiscover(argv_log),
+        size=lambda: (160, 50),
+    )
+    code, out = once(Options(once=True, run_id=QRUN, questions=True, width=116), deps)
+    lines = out.splitlines()
+    assert code == 0 and all(cell_len(l) <= 116 for l in lines)
+    assert "COORDINATOR QUESTIONS" in lines and GAP_NOTICE not in lines
+
+
+def test_questions_without_a_run_or_with_a_fixture_or_a_bad_run_is_refused_with_no_call(
+    fake_clock, argv_log, monkeypatch
+):
+    for guard in (False, True):
+        monkeypatch.setattr(commands, "QUESTION_GATE_PASSED", guard)
+        runner = question_runner(argv_log)
+        deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
+        for options in (
+            Options(once=True, questions=True),
+            Options(once=True, questions=True, fixture="base", run_id=QRUN),
+            Options(once=True, questions=True, run_id="-x"),
+            Options(once=True, questions=True, run_id="bad id"),
+        ):
+            assert execute(options, deps) == 2
+        assert argv_log == []
+    for args in (
+        ["--once", "--questions"],
+        ["--once", "--questions", "--fixture", "base", "--run", QRUN],
+        ["--once", "--questions", "--run", "-x"],
+        ["--once", "--questions", "--run", "bad id"],
+    ):
+        result = CliRunner().invoke(observe_group, args)
+        assert result.exit_code != 0, args
+
+
+def test_questions_off_leaves_the_message_source_unused_even_with_a_run(
+    fake_clock, argv_log
+):
+    runner = question_runner(argv_log)
+    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
+    code, out = once(Options(once=True, run_id=QRUN), deps)
+    assert code == 0 and messages_in(argv_log) == []
+    assert GAP_NOTICE in out.splitlines() and "COORDINATOR" not in out
+
+
+def test_help_states_the_one_run_rule_the_disclosure_and_that_run_use_is_never_run():
+    result = CliRunner().invoke(observe_group, ["--help"])
+    flat = " ".join(result.output.split())
+    assert result.exit_code == 0 and "--questions" in flat
+    assert "never runs run-use" in flat
+    assert "the observer never runs run-use and never binds to a Run" in flat
+    assert "Run it from the terminal that already holds the Run" in flat
+    assert (
+        "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost"
+        in flat
+    )
+    assert (
+        "Message bodies are received by this process; subjects are shown, bodies are not kept"
+        in flat
+    )
+    assert "one named Run" in flat
+
+
+def test_the_guard_constant_is_a_literal_false_with_a_comment_naming_the_gate_record():
+    text = Path(commands.__file__).read_text(encoding="utf-8")
+    assert len(re.findall(r"^QUESTION_GATE_PASSED = (True|False)$", text, re.M)) == 1
+    assert "QUESTION_GATE_PASSED = False" in text
+    assert "release-gates.md" in text and "Task 18" in text
diff --git a/tests/observe/test_registration.py b/tests/observe/test_registration.py
index cadfc6ce1..91ec218c6 100644
--- a/tests/observe/test_registration.py
+++ b/tests/observe/test_registration.py
@@ -22,8 +22,25 @@ def test_the_group_lists_observe_among_its_commands():
 def test_observe_help_lists_every_option():
     result = CliRunner().invoke(main, ["observe", "--help"])
     assert result.exit_code == 0
-    for option in ("--once", "--width", "--ascii", "--fixture", "--run", "--snapshot"):
+    for option in (
+        "--once",
+        "--width",
+        "--ascii",
+        "--fixture",
+        "--run",
+        "--snapshot",
+        "--questions",
+    ):
         assert option in result.output
+    assert "never runs run-use" in " ".join(result.output.split())
+
+
+def test_questions_through_the_shipped_cli_is_refused_while_the_gate_guard_is_off():
+    result = CliRunner().invoke(
+        main, ["observe", "--once", "--run", "run_x", "--questions"]
+    )
+    assert result.exit_code != 0
+    assert "question read not enabled" in result.output
 
 
 def test_once_fixture_base_prints_a_record_with_the_synthetic_banner_first():


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
