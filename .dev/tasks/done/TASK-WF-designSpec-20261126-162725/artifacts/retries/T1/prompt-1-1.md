a06b7e3002192c61fbeb4e8a09018d8bc5f76faf
Review one task for spec compliance.

Task brief: ## Task 1: Record the baseline, create the test setup and the single question file

First, before creating any other file, run `git status --short` and save its output to `./artifacts/baseline-status.txt` in the package. Then create `.dev/research/jev-vs-keyword-table-611/questions.py`, `.dev/research/jev-vs-keyword-table-611/harness/__init__.py` (empty), `.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py`.

`questions.py` is the only place Jev question wording lives. It imports `choice` and `noul` from `jevlib.questions` and exposes `QSET_VERSION`, `TYPES = ("bug", "build", "performance", "deployment", "security", "test")` and `build_questions() -> dict` returning two questions: `problem_type`, a `choice` over the six types with a one-sentence plain definition per option (no positional option names such as `a` or `option1`), and `any_type_fits`, a `noul` asking whether any of the six types fits the problem in `state["prompt"]`, with `true` and `false` criteria. No corpus prompt, label or corpus-derived example appears in the file, and it does not copy the table's cue phrases (the table is `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` lines 153 to 158).

`conftest.py` inserts `.dev/research/346-review-loop-experiments/p15/jev` and the experiment folder into `sys.path` (the same pattern as `p15/jev/tests/conftest.py`). It provides an autouse fixture that fails any test that calls `socket.socket.connect`, a fixture that sets a fake `JEV_API_KEY` with `monkeypatch.setenv`, and an autouse fixture that records the existence, size and modification time of the real experiment folder's `events.jsonl`, `manifest.json`, `ledger/spend.json` and `runs/` before each test and fails the test if any of them changed. The real folder is found from the conftest's own location, so this fixture needs no other module.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py -v` passes.
- `test_questions.py` shows that `jevlib.questions.build_request({"prompt": "x"}, build_questions())` succeeds, the choice has exactly the six type names, the noul has `true` and `false` criteria, and `request_sha256` is identical across two calls.
- A test shows the socket guard fails a test that tries to connect, and a test shows the real-state snapshot helper reports a change when a file in a temporary folder is edited.
- A test asserts that none of these cue phrases appears, ignoring case, in the text of `questions.py`: stack trace, NameError, undefined, tsc, compiled, lint, slow, latency, p99, too long to load, takes forever, hangs, container, env var, service won't start, CVE, vulnerab, pytest, jest, flake, intermittent, passing locally. The test names the words it exempts because they are type names or ordinary English: build, make, deploy, production, memory, leak, auth, token, exposed, null.
- `./artifacts/baseline-status.txt` exists and does not list `.dev/research/jev-vs-keyword-table-611`.

Acceptance criterion ids (in source order):
T1.AC1: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py -v` passes.
T1.AC2: `test_questions.py` shows that `jevlib.questions.build_request({"prompt": "x"}, build_questions())` succeeds, the choice has exactly the six type names, the noul has `true` and `false` criteria, and `request_sha256` is identical across two calls.
T1.AC3: A test shows the socket guard fails a test that tries to connect, and a test shows the real-state snapshot helper reports a change when a file in a temporary folder is edited.
T1.AC4: A test asserts that none of these cue phrases appears, ignoring case, in the text of `questions.py`: stack trace, NameError, undefined, tsc, compiled, lint, slow, latency, p99, too long to load, takes forever, hangs, container, env var, service won't start, CVE, vulnerab, pytest, jest, flake, intermittent, passing locally. The test names the words it exempts because they are type names or ordinary English: build, make, deploy, production, memory, leak, auth, token, exposed, null.
T1.AC5: `./artifacts/baseline-status.txt` exists and does not list `.dev/research/jev-vs-keyword-table-611`.
Global constraints: ## Constraints

- Scope is build and test only. No task sends a prompt to TypeSafe, reads `TYPESAFE_API_KEY` or `JEV_API_KEY` from the real environment, or opens a network connection. Tests use `MockTransport` and a socket guard, set a fake key with `monkeypatch.setenv`, and use a temporary experiment root for every file the gates, events, runner and scorer write. The live run is a coordinator action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` (lines 145 to 165).
- Left for a person or the coordinator, not in this plan: choosing and labelling about 30 public prompts (a named human labeller is required), applying the keyword table to them (a session or person who sees prompts only, after Gate 1), the live run with `keyscan.py`, scoring and the report, and the updates on issues 611, 609 and 612. Tasks 7 and 8 produce the procedures, templates and instructions those steps need. The pull request that delivers this plan says `Refs #611` and lists parts B to E of section 8 of the design as left (Task 8 puts that sentence in the README).
- Nothing under `src/`, `tests/`, `.claude/` or the existing `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` folder is changed. `jevlib` is imported read-only, and only from its submodules (`client`, `budget`, `journal`, `transport`, `questions`, `manifest`, `config`), because `jevlib/__init__.py` exports only `MODEL`, `API_URL` and `KEY_ENV`.
- Spend cap is 1 dollar in total; public prompts only; the key is never printed, logged, written to a file, put on a command line or put in a pull request. The runner copies `TYPESAFE_API_KEY` into `JEV_API_KEY` inside its own process only, because `jevlib.config.KEY_ENV` is `JEV_API_KEY`.
- Agreed decision rule (AGREED 2026-11-26 by the IronFlow session and the build agent, relayed by the lead; Clay's own words as quoted by the IronFlow session, not typed by Clay: "you and the agent debate whats correct way to handle this and do it").
- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. Per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Still open, so written as `UNSET` in the rule file: the operators at exactly 0.3 and 0.7 for the Noul band, and the count of unresolved failures that makes a run invalid. Gate 1 accepts `UNSET` and does not freeze the rule file's hash. The scorer, the `freeze-rule` command and Gate 2 refuse any `UNSET` value, and `freeze-rule` is the step that freezes the rule file's hash after the owner has filled the fields.
- The real client behaves differently from a mock-backed dry run: `JevClient` with `live=False` builds, screens and budgets the request, then returns `refused` with error `dry_run` before any transport call. So the runner has two subcommands: `run` needs `--live`, both gates and the key; `rehearse` never posts and needs no gate and no key. Tests that need the transport path use `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`.
- Test run command, recorded by `gate.py record-tests`: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. The repository's `testpaths` is `tests`, so tests under `.dev/` are only collected when this path is given.
- Each of the four command-line modules (`gate.py`, `events.py`, `runner.py` and `scorer.py`) inserts the existing `jevlib` folder and the experiment folder into `sys.path` itself, as `.dev/research/346-review-loop-experiments/p15/jev/probe.py` does (read-only reference), because only `conftest.py` does so for tests (finding M-12).
Start sha: a06b7e3002192c61fbeb4e8a09018d8bc5f76faf
Diff against the start snapshot: diff --git a/.dev/research/jev-vs-keyword-table-611/questions.py b/.dev/research/jev-vs-keyword-table-611/questions.py
new file mode 100644
index 000000000..0fd1ac315
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/questions.py
@@ -0,0 +1,35 @@
+"""The only place Jev question wording for the issue 611 experiment lives (contract J7).
+
+Two questions are asked about the prompt in ``state["prompt"]``: which of six problem types it is (a Choice), and whether any of
+the six fits at all (a Noul).  The six definitions are written in plain words; they are not a copy of the keyword table the
+experiment compares against, and no corpus prompt, label or example appears here.
+"""
+from jevlib.questions import choice, noul
+
+QSET_VERSION = "issue611-q1"
+TYPES = ("bug", "build", "performance", "deployment", "security", "test")
+
+_DEFINITIONS = {
+    "bug": "The program gives a wrong result or stops with an error because of a mistake in its own code.",
+    "build": "The steps that assemble the project, or check it before it runs, stop with an error.",
+    "performance": "The program works but uses too much time or memory for what it does.",
+    "deployment": "The program works where it was built but fails when it is installed, configured or started on the machine meant to run it.",
+    "security": "Someone could misuse the program to read or change data they should not, or to take control of something.",
+    "test": "The automated checks of the program fail, pass only some of the time, or do not check what they claim to check.",
+}
+
+
+def build_questions() -> dict:
+    """Return the two questions in a fixed order; the request hash is stable across calls."""
+    return {
+        "problem_type": choice(
+            "Read the problem described in the prompt field of the state and pick the one type that describes it best.",
+            {t: _DEFINITIONS[t] for t in TYPES},
+        ),
+        "any_type_fits": noul(
+            "Read the problem described in the prompt field of the state. Decide whether any of the six problem types "
+            "(bug, build, performance, deployment, security, test) describes it.",
+            true="At least one of the six problem types describes the problem.",
+            false="None of the six problem types describes the problem.",
+        ),
+    }
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/__init__.py b/.dev/research/jev-vs-keyword-table-611/harness/__init__.py
new file mode 100644
index 000000000..e69de29bb
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
new file mode 100644
index 000000000..cf4b70646
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
@@ -0,0 +1,59 @@
+"""Shared test setup: import paths, a network guard, a fake key, and a guard on the real experiment folder."""
+import pathlib
+import socket
+import sys
+
+import pytest
+
+EXP = pathlib.Path(__file__).resolve().parents[2]          # .dev/research/jev-vs-keyword-table-611
+JEV = EXP.parent / "346-review-loop-experiments" / "p15" / "jev"   # parent folder of the jevlib package
+for _p in (JEV, EXP):
+    if str(_p) not in sys.path:
+        sys.path.insert(0, str(_p))
+
+FAKE_KEY = "fake-test-key-0123456789abcdef"
+
+
+def real_state_snapshot(root=EXP):
+    """Existence, size and modification time of the state files under ``root``; for ``runs`` every file below it as well."""
+    root = pathlib.Path(root)
+    snap = {}
+    for rel in ("events.jsonl", "manifest.json", "ledger/spend.json"):
+        p = root / rel
+        snap[rel] = (p.stat().st_size, p.stat().st_mtime_ns) if p.is_file() else None
+    runs = root / "runs"
+    if runs.is_dir():
+        snap["runs"] = tuple(sorted((str(f.relative_to(runs)), f.stat().st_size, f.stat().st_mtime_ns)
+                                    for f in runs.rglob("*") if f.is_file()))
+        snap["runs/"] = runs.stat().st_mtime_ns
+    else:
+        snap["runs"] = None
+    return snap
+
+
+@pytest.fixture(autouse=True)
+def no_network(monkeypatch):
+    """Fail any test that opens a socket connection."""
+    def refuse(self, *args, **kwargs):
+        raise AssertionError("a test tried to open a network connection")
+    monkeypatch.setattr(socket.socket, "connect", refuse)
+    monkeypatch.setattr(socket.socket, "connect_ex", refuse)
+
+
+@pytest.fixture(autouse=True)
+def real_state_untouched():
+    """The real events log, manifest, ledger and runs folder must be the same after each test as before it."""
+    before = real_state_snapshot()
+    yield
+    assert real_state_snapshot() == before, "a test changed the real experiment state"
+
+
+@pytest.fixture
+def fake_key(monkeypatch):
+    monkeypatch.setenv("JEV_API_KEY", FAKE_KEY)
+    return FAKE_KEY
+
+
+@pytest.fixture
+def snapshot_fn():
+    return real_state_snapshot
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py
new file mode 100644
index 000000000..930a991f4
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py
@@ -0,0 +1,65 @@
+import pathlib
+import socket
+
+import pytest
+import questions as q
+from jevlib.questions import build_request, request_sha256
+
+QUESTIONS_PY = pathlib.Path(q.__file__)
+
+# Distinctive cue phrases of the keyword table (SKILL.md lines 153 to 158). Words that are type names or ordinary English
+# (build, make, deploy, production, memory, leak, auth, token, exposed, null) are exempt on purpose.
+CUE_PHRASES = [
+    "stack trace", "nameerror", "undefined", "tsc", "compiled", "lint", "slow", "latency", "p99", "too long to load",
+    "takes forever", "hangs", "container", "env var", "service won't start", "cve", "vulnerab", "pytest", "jest", "flake",
+    "intermittent", "passing locally",
+]
+
+
+def test_request_builds_and_is_stable():
+    req = build_request({"prompt": "x"}, q.build_questions())
+    again = build_request({"prompt": "x"}, q.build_questions())
+    assert request_sha256(req) == request_sha256(again)
+    assert req["model"] == "jev-1.14.0"
+
+
+def test_choice_has_exactly_the_six_types():
+    qs = q.build_questions()
+    assert qs["problem_type"]["type"] == "choice"
+    assert list(qs["problem_type"]["criteria"]) == list(q.TYPES)
+    assert q.TYPES == ("bug", "build", "performance", "deployment", "security", "test")
+    assert all(text.strip() for text in qs["problem_type"]["criteria"].values())
+
+
+def test_noul_has_true_and_false_criteria():
+    qs = q.build_questions()
+    assert qs["any_type_fits"]["type"] == "noul"
+    assert set(qs["any_type_fits"]["criteria"]) == {"true", "false"}
+    assert all(qs["any_type_fits"]["criteria"].values())
+
+
+def test_only_two_questions_in_a_fixed_order():
+    assert list(q.build_questions()) == ["problem_type", "any_type_fits"]
+
+
+def test_questions_file_copies_none_of_the_tables_cue_phrases():
+    text = QUESTIONS_PY.read_text(encoding="utf-8").lower()
+    found = [c for c in CUE_PHRASES if c in text]
+    assert found == []
+
+
+def test_socket_guard_fails_a_connection_attempt():
+    with pytest.raises(AssertionError):
+        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("127.0.0.1", 9))
+
+
+def test_real_state_snapshot_reports_an_edit_of_an_existing_nested_file(tmp_path, snapshot_fn):
+    run = tmp_path / "runs" / "r1"
+    run.mkdir(parents=True)
+    (run / "jev-rows.jsonl").write_text("a\n")
+    before = snapshot_fn(tmp_path)
+    (run / "jev-rows.jsonl").write_text("ab\n")          # edit an existing nested file
+    assert snapshot_fn(tmp_path) != before
+    before = snapshot_fn(tmp_path)
+    (tmp_path / "events.jsonl").write_text("{}\n")        # create a top-level state file
+    assert snapshot_fn(tmp_path) != before
diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/baseline-status.txt b/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/baseline-status.txt
new file mode 100644
index 000000000..db0bc1413
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/baseline-status.txt
@@ -0,0 +1,25 @@
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-144507/artifacts/archive-undo.txt
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-144507/artifacts/codegraph-grounding.md
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-144507/return-contract.yaml
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-144507/source.md
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-152817/artifacts/archive-undo.txt
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-152817/artifacts/codegraph-grounding.md
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-152817/return-contract.yaml
+A  .dev/tasks/archive/TASK-WF-designSpec-20261126-152817/source.md
+A  .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/TASK-WF-designSpec-20261126-162725.md
+A  .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/old-plan.md
+A  .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/plan.diff
+A  .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/prior-findings.md
+A  .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/revision-log.md
+A  .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/return-contract.yaml
+A  .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/source.md
+?? .dev/brainstorms/20261126-jev-vs-keyword-table-611/
+?? .dev/issues/611/
+?? .dev/reflect/pre-designSpec-20261126145044/
+?? .dev/reflect/pre-designSpec-20261126153331/
+?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/baseline-status.txt
+?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/codegraph.md
+?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/retries/
+?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/progress.md


Codegraph context
index_state: fresh
checked_at: 2026-11-26T16:38:23Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the files of this task are new or only used by later tasks; no dependent outside the touched files.
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
