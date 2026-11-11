59831f56b5978a4c0ffa686fabaaa089c1e88c50
Review one task for spec compliance.

Task brief: 
## Task 6: Add the question template, forbidden verbs and error codes to adapter.py

Depends on: Task 4

Edit `src/superclaude/cli/observe/adapter.py` and `tests/observe/conftest.py` and add tests to `tests/observe/test_adapter.py`.

- Add `QUESTION_TEMPLATE = ("orchestration", "check", "--all", "--types", "question")` plus `--run <runId>` then `--json`; extend `FORBIDDEN_PREFIXES` with `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`; the existing `check` prefix stays forbidden except for exactly this template (the allow decision is made on the whole argv, not the token). `--peek` and a `check --all` without `--types question` or without `--run` stay refused.
- Extend `assert_allowed`, `_option_positions` and `build_argv` (new `build_question_argv(orca, run_id)`) so the run id passes `check_run_id`.
- Add `LiveSource.read_questions(clock, budget_deadline, run_id)`: one call, no paging, same timeout and output-cap handling; returns a `SourceResult` whose single page is the decoded envelope. When the decoded stdout is an object with `ok` false, map `error.code` `consumer_fenced` to source code `consumer-fenced` and `no_active_terminal` to `no-active-terminal` (add both to `CODES`), whatever the exit status; any other error code maps to `exit:<n>` or `json` as today. Diagnostics stay sanitized and under 2 KiB.
- Update `argv_allowed` in `tests/observe/conftest.py` to accept the question template and nothing else new.

Acceptance criteria:
- `uv run pytest tests/observe/test_adapter.py -v` passes with new tests: the fake runner receives exactly the template argv with `--run run_14cfcbd8edf2`-style ids; each of `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`, `inbox`, plain `check`, `check --peek`, `check --all` without `--types question`, the template without `--run`, a run id starting with `-` and a malformed run id raises `ArgvRejected` before the runner is called.
- A fake runner returning the recorded `consumer_fenced` error envelope (exit 1) yields `FAILED` with code `consumer-fenced`; one returning `no_active_terminal` yields `FAILED` with code `no-active-terminal`; both leave the argv log with exactly one message call.
- A static test shows `--ack`, `--wait`, `--retry-request`, `--peek` and `run-use` appear in adapter.py only inside the forbidden set.

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

Start sha: 59831f56b5978a4c0ffa686fabaaa089c1e88c50
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/adapter.py b/src/superclaude/cli/observe/adapter.py
index de0746968..d8bcfcc6e 100644
--- a/src/superclaude/cli/observe/adapter.py
+++ b/src/superclaude/cli/observe/adapter.py
@@ -1,8 +1,9 @@
 """The one read-only edge to the Orca CLI (AD-3, AD-4, AD-5).
 
-Only two argv shapes are ever run: the worker-list template (with optional run and cursor
-pairs) and the one-time binary discovery probe that ``_find_orca`` makes. Every argv is
-checked against a forbidden set before any call, and the set only ever grows.
+Only three argv shapes are ever run: the worker-list template (with optional run and cursor
+pairs), the one-time binary discovery probe that ``_find_orca`` makes, and the one R2
+message template for a single named Run (used only past the gate guard in ``commands.py``).
+Every argv is checked against a forbidden set before any call, and the set only ever grows.
 """
 
 from __future__ import annotations
@@ -27,9 +28,25 @@ Discover = Callable[[], "str | None"]
 
 WORKER_LIST_TEMPLATE = ("orchestration", "worker-list", "--json", "--limit", "100")
 DISCOVERY_TEMPLATE = ("skills", "list", "--json")
+# R2 message template: these five items, then ``--run <runId>``, then ``--json``.
+QUESTION_TEMPLATE = ("orchestration", "check", "--all", "--types", "question")
 # Matched by prefix against every verb and flag position, never against run or cursor values.
 FORBIDDEN_PREFIXES = frozenset(
-    {"check", "--ack", "--wait", "--retry-request", "dispatch", "inbox"}
+    {
+        "check",
+        "--ack",
+        "--wait",
+        "--retry-request",
+        "--peek",
+        "dispatch",
+        "inbox",
+        "run-use",
+        "run-create",
+        "send",
+        "ask",
+        "reply",
+        "reset",
+    }
 )
 
 RUN_ID_PATTERN = re.compile(
@@ -58,8 +75,15 @@ CODES = frozenset(
         "cursor-rejected",
         "cursor-stalled",
         "empty-page",
+        "consumer-fenced",
+        "no-active-terminal",
     }
 )
+# Error codes of an ``{"ok": false, "error": {"code": ...}}`` envelope -> source codes.
+_ERROR_CODES = {
+    "consumer_fenced": "consumer-fenced",
+    "no_active_terminal": "no-active-terminal",
+}
 
 
 class ArgvRejected(ValueError):
@@ -101,9 +125,22 @@ def check_cursor(cursor: object) -> str:
     return cursor
 
 
+def _is_question_shape(tokens: list[str]) -> bool:
+    """True when the whole argv (after the binary) has the R2 message template's shape."""
+    return (
+        len(tokens) == 8
+        and tuple(tokens[:5]) == QUESTION_TEMPLATE
+        and tokens[5] == "--run"
+        and tokens[7] == "--json"
+    )
+
+
 def _option_positions(tokens: list[str]) -> set[int]:
     """Indexes (into ``tokens``) that are verbs or flags rather than option values."""
     positions = set(range(len(tokens)))
+    if _is_question_shape(tokens):
+        # The verb of the whole template and its two values are not forbidden tokens.
+        return positions - {1, 4, 6}
     if tokens[:5] == list(WORKER_LIST_TEMPLATE):
         i = 5
         while i + 1 < len(tokens) and tokens[i] in ("--run", "--cursor"):
@@ -113,7 +150,7 @@ def _option_positions(tokens: list[str]) -> set[int]:
 
 
 def assert_allowed(argv: list) -> None:
-    """Refuse any argv that is not one of the two templates; names the forbidden token."""
+    """Refuse any argv that is not one of the three templates; names the forbidden token."""
     if not argv or not all(isinstance(a, str) for a in argv) or len(argv) < 2:
         raise ArgvRejected("argv", "not a list of strings")
     if argv[0].startswith("-") or not argv[0]:
@@ -127,6 +164,9 @@ def assert_allowed(argv: list) -> None:
                 )
     if tokens == list(DISCOVERY_TEMPLATE):
         return
+    if _is_question_shape(tokens):
+        check_run_id(tokens[6])
+        return
     if tokens[:5] != list(WORKER_LIST_TEMPLATE):
         raise ArgvRejected("argv", "not an allow-listed argv")
     rest = tokens[5:]
@@ -160,6 +200,13 @@ def build_argv(
     return argv
 
 
+def build_question_argv(orca: str, run_id: object) -> list[str]:
+    """The R2 message argv: the literal template with the checked run id as one item."""
+    argv = [orca, *QUESTION_TEMPLATE, "--run", check_run_id(run_id), "--json"]
+    assert_allowed(argv)
+    return argv
+
+
 # -- the production runner --------------------------------------------------------------------
 
 
@@ -431,3 +478,48 @@ class LiveSource:
                 return self._stop(pages, "cursor-stalled", "", calls)
             used.add(next_cursor)
             cursor = next_cursor
+
+    def read_questions(
+        self, clock: Any, budget_deadline: float, run_id: str
+    ) -> SourceResult:
+        """One R2 message call for one named Run: no paging, same timeout and output cap.
+
+        The decoded reply is the one page of the result. An ``ok: false`` error envelope is
+        decoded whatever the exit status, so ``consumer_fenced`` and ``no_active_terminal``
+        get their own source codes; any other failure maps as ``read_pages`` maps it.
+        """
+        if not self.discover():
+            return SourceResult("FAILED", code="not-found")
+        remaining = budget_deadline - clock.monotonic()
+        if remaining <= 0 or self._cancelled.is_set():
+            return self._stop([], "overrun", "", 0)
+        argv = build_question_argv(self.orca, run_id)  # ArgvRejected before any call
+        budget_limited = remaining < self.per_call_timeout
+        try:
+            reply = self._runner(argv, min(self.per_call_timeout, remaining))
+        except (TimeoutError, subprocess.TimeoutExpired):
+            return self._stop([], "overrun" if budget_limited else "timeout", "", 1)
+        except RunnerFailure as exc:
+            code = "overrun" if exc.code == "timeout" and budget_limited else exc.code
+            return self._stop([], code, exc.stderr, 1)
+        except OSError as exc:
+            return self._stop([], "spawn-error", str(exc), 1)
+        returncode, stdout = reply[0], reply[1]
+        stderr = reply[2] if len(reply) > 2 else ""
+        try:
+            page = json.loads(stdout)
+        except (ValueError, TypeError, RecursionError):
+            page = None
+            decoded = False
+        else:
+            decoded = True
+        if decoded and isinstance(page, dict) and page.get("ok") is False:
+            error = page.get("error")
+            name = error.get("code") if isinstance(error, dict) else None
+            if isinstance(name, str) and name in _ERROR_CODES:
+                return self._stop([], _ERROR_CODES[name], stderr, 1)
+        if returncode != 0:
+            return self._stop([], f"exit:{returncode}", stderr, 1)
+        if not decoded or (isinstance(page, dict) and page.get("ok") is False):
+            return self._stop([], "json", stderr, 1)
+        return SourceResult("OK", (page,), calls=1)
diff --git a/tests/observe/conftest.py b/tests/observe/conftest.py
index f6218a39a..b18950f2b 100644
--- a/tests/observe/conftest.py
+++ b/tests/observe/conftest.py
@@ -17,6 +17,7 @@ from superclaude.cli.observe.terminal import make_console, resolve_policy
 BASE_TIME = datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.utc)
 WORKER_LIST_BASE = ["orchestration", "worker-list", "--json", "--limit", "100"]
 DISCOVERY_TAIL = ["skills", "list", "--json"]
+QUESTION_BASE = ["orchestration", "check", "--all", "--types", "question"]
 
 
 # -- subprocess guard -------------------------------------------------------------------
@@ -79,13 +80,21 @@ def fake_clock() -> FakeClock:
 
 
 def argv_allowed(argv) -> bool:
-    """The only argv the observer may ever run: worker-list (with optional pairs) or discovery."""
+    """The only argv the observer may ever run: worker-list (with optional pairs), discovery,
+    or the one R2 message template for one named Run."""
     argv = list(argv)
     if len(argv) < 2 or not all(isinstance(a, str) for a in argv):
         return False
     tail = argv[1:]
     if tail == DISCOVERY_TAIL:
         return True
+    if tail[:5] == QUESTION_BASE:
+        return (
+            len(tail) == 8
+            and tail[5] == "--run"
+            and not tail[6].startswith("-")
+            and tail[7] == "--json"
+        )
     if tail[:5] != WORKER_LIST_BASE:
         return False
     rest = tail[5:]
diff --git a/tests/observe/test_adapter.py b/tests/observe/test_adapter.py
index f5b018e9b..2071c9ad6 100644
--- a/tests/observe/test_adapter.py
+++ b/tests/observe/test_adapter.py
@@ -21,6 +21,7 @@ from superclaude.cli.observe.adapter import (
     RunnerFailure,
     assert_allowed,
     build_argv,
+    build_question_argv,
     production_runner,
 )
 from tests.observe.conftest import (
@@ -162,18 +163,32 @@ def test_forbidden_words_appear_only_inside_the_forbidden_set():
     assert block, "the forbidden set must be one frozenset literal"
     for word in ("--ack", "--wait", "--retry-request"):
         assert word in block.group(0)
-    assert text.count('"check"') == 1 and '"check"' in block.group(0)
+    # "check" is the forbidden verb and, once, the verb of the one R2 message template.
+    assert text.count('"check"') == 2 and '"check"' in block.group(0)
+    assert text.count('"check"') == block.group(0).count('"check"') + 1
     assert (
         "check" not in adapter.WORKER_LIST_TEMPLATE
         and "check" not in adapter.DISCOVERY_TEMPLATE
     )
+    # T2: these words appear in the module only inside the forbidden set.
+    for word in ("--peek", "run-use"):
+        assert text.count(word) == 1 and word in block.group(0), word
+    for verb in ("run-create", "send", "ask", "reply", "reset"):
+        assert text.count(f'"{verb}"') == 1 and f'"{verb}"' in block.group(0), verb
     assert FORBIDDEN_PREFIXES >= {
         "check",
         "--ack",
         "--wait",
         "--retry-request",
+        "--peek",
         "dispatch",
         "inbox",
+        "run-use",
+        "run-create",
+        "send",
+        "ask",
+        "reply",
+        "reset",
     }
 
 
@@ -572,3 +587,166 @@ def test_adapter_imports_sanitize_but_not_parse_or_collector_and_owns_subprocess
     assert re.search(r"^from superclaude\.cli\.observe\.sanitize import", text, re.M)
     assert not re.search(r"observe\.(parse|collector|view|render|export)\b", text)
     assert re.search(r"^import subprocess$", text, re.M)
+
+
+# -- R2: the one message template, its forbidden neighbours and its error envelopes (T52, T53) ---------------
+
+QUESTION_RUN = "run_14cfcbd8edf2"
+QUESTION_ARGV = [
+    ORCA,
+    "orchestration",
+    "check",
+    "--all",
+    "--types",
+    "question",
+    "--run",
+    QUESTION_RUN,
+    "--json",
+]
+
+
+def question_reply(n=2, run=QUESTION_RUN):
+    rows = [
+        {
+            "id": f"msg_{i:012x}",
+            "run_id": run,
+            "type": "question",
+            "subject": f"probe question {i}",
+            "created_at": "2026-11-11T20:01:11Z",
+        }
+        for i in range(n)
+    ]
+    envelope = {
+        "id": "env-1",
+        "ok": True,
+        "result": {"acknowledged": None, "count": n, "messages": rows, "runId": run},
+    }
+    return 0, json.dumps(envelope)
+
+
+def error_reply(code, status=1):
+    envelope = {"id": "env-2", "ok": False, "error": {"code": code, "message": code}}
+    return status, json.dumps(envelope)
+
+
+def read_questions(source, clock, run_id=QUESTION_RUN, budget=15.0):
+    return source.read_questions(clock, clock.monotonic() + budget, run_id)
+
+
+def test_the_fake_runner_receives_exactly_the_question_template(argv_log, fake_clock):
+    source, runner = source_with([question_reply(2)], argv_log)
+    result = read_questions(source, fake_clock)
+    assert result.state == "OK" and result.calls == 1 and len(result.pages) == 1
+    assert [a for a in runner.log if a[1:3] == ["orchestration", "check"]] == [
+        QUESTION_ARGV
+    ]
+    assert build_question_argv(ORCA, QUESTION_RUN) == QUESTION_ARGV
+    assert tuple(QUESTION_ARGV[1:6]) == adapter.QUESTION_TEMPLATE
+    assert_allowed(QUESTION_ARGV)
+    assert argv_allowed(QUESTION_ARGV)
+
+
+@pytest.mark.parametrize(
+    "argv",
+    [
+        [ORCA, "orchestration", "run-use", "--id", QUESTION_RUN],
+        [ORCA, "orchestration", "run-create", "--json"],
+        [ORCA, "orchestration", "send", "--to", f"run:{QUESTION_RUN}"],
+        [ORCA, "orchestration", "ask", "--question", "x"],
+        [ORCA, "orchestration", "reply", "--id", "msg_1"],
+        [ORCA, "orchestration", "reset"],
+        [ORCA, "orchestration", "inbox", "--json"],
+        [ORCA, "orchestration", "check", "--json"],
+        [ORCA, "orchestration", "check", "--peek", "--types", "question", "--json"],
+        [*QUESTION_ARGV[:-1], "--peek", "--json"],
+        [ORCA, "orchestration", "check", "--all", "--json"],
+        [ORCA, "orchestration", "check", "--all", "--run", QUESTION_RUN, "--json"],
+        [ORCA, "orchestration", "check", "--all", "--types", "question", "--json"],
+        [
+            ORCA,
+            "orchestration",
+            "check",
+            "--all",
+            "--types",
+            "status",
+            "--run",
+            QUESTION_RUN,
+            "--json",
+        ],
+        [*QUESTION_ARGV, "--ack", "d1"],
+        [*QUESTION_ARGV, "--wait"],
+        [*QUESTION_ARGV[:7], "--ack", "d1", "--json"],
+    ],
+)
+def test_neighbours_of_the_question_template_are_rejected_before_any_call(argv):
+    with pytest.raises(ArgvRejected):
+        assert_allowed(argv)
+    assert not argv_allowed(argv)
+
+
+@pytest.mark.parametrize("bad", ["-x", "--evil", "bad id", "a/b", "", 5, None])
+def test_a_bad_question_run_id_fails_before_the_runner_is_called(
+    bad, argv_log, fake_clock
+):
+    source, runner = source_with([question_reply(1)], argv_log)
+    with pytest.raises(ArgvRejected) as info:
+        read_questions(source, fake_clock, run_id=bad)
+    assert info.value.code == "run-id"
+    assert runner.calls == 0 and not any(a[1] == "orchestration" for a in argv_log)
+    if isinstance(bad, str):
+        with pytest.raises(ArgvRejected):
+            assert_allowed([ORCA, *adapter.QUESTION_TEMPLATE, "--run", bad, "--json"])
+
+
+def test_a_run_id_that_looks_like_a_verb_is_still_a_value():
+    assert_allowed([ORCA, *adapter.QUESTION_TEMPLATE, "--run", "send-7", "--json"])
+
+
+@pytest.mark.parametrize(
+    "code,expected",
+    [
+        ("consumer_fenced", "consumer-fenced"),
+        ("no_active_terminal", "no-active-terminal"),
+    ],
+)
+@pytest.mark.parametrize("status", [1, 0])
+def test_error_envelopes_map_to_source_codes_whatever_the_exit_status(
+    code, expected, status, argv_log, fake_clock
+):
+    source, runner = source_with([error_reply(code, status)], argv_log)
+    result = read_questions(source, fake_clock)
+    assert (result.state, result.code, result.pages) == ("FAILED", expected, ())
+    assert expected in adapter.CODES
+    assert sum(1 for a in argv_log if a[1:3] == ["orchestration", "check"]) == 1
+    assert runner.calls == 1
+
+
+def test_other_failures_keep_their_existing_codes(argv_log, fake_clock):
+    for response, code in (
+        (error_reply("something_else", 2), "exit:2"),
+        (error_reply("something_else", 0), "json"),
+        ((3, ""), "exit:3"),
+        ((0, "not json"), "json"),
+        (TimeoutError("slow"), "timeout"),
+    ):
+        source, _ = source_with([response], argv_log)
+        result = read_questions(source, fake_clock)
+        assert (result.state, result.code) == ("FAILED", code)
+
+
+def test_the_question_read_is_one_call_with_no_paging_and_respects_the_budget(
+    argv_log, fake_clock
+):
+    source, runner = source_with([question_reply(100)], argv_log)
+    assert read_questions(source, fake_clock).calls == 1 and runner.calls == 1
+    source, runner = source_with([question_reply(1)], argv_log)
+    spent = source.read_questions(fake_clock, fake_clock.monotonic() - 1, QUESTION_RUN)
+    assert (spent.state, spent.code, runner.calls) == ("FAILED", "overrun", 0)
+
+
+def test_the_question_diagnostic_is_sanitized_and_bounded(argv_log, fake_clock):
+    noisy = "\x1b[31mboom\x1b[0m" + "x" * 5000
+    source, _ = source_with([(1, error_reply("consumer_fenced")[1], noisy)], argv_log)
+    result = read_questions(source, fake_clock)
+    assert result.code == "consumer-fenced"
+    assert "\x1b" not in result.diagnostic and len(result.diagnostic.encode()) <= 2048


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
