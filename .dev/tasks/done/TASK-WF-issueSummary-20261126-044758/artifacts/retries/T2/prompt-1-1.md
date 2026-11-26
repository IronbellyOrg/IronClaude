173e7339c87317b5cc18664374556bc0ce5845eb
Review one task for spec compliance.

Task brief:  Extend content and installation regression coverage

Depends on: Task 1

Extend `tests/commands/test_pragmatic_plain_english.py` using its existing literal/section/order pattern to guard the new rule and preserve earlier question rules. Strengthen `tests/cli/test_install_user_setup.py:test_output_style_installs` to compare installed Pragmatic bytes to the canonical source through `install_output_styles(home=tmp_path)`. Reuse the keep/forced-refresh/backup checks already in `tests/cli/test_install_keep.py`, rather than adding duplicate cases. Installer functions and callers remain unchanged.

Acceptance criteria:
- T2.AC1: Focused content tests fail if the new rule disappears, moves outside Decision requests, duplicates, or loses any required context/implications/risk, existing-file-only, no-file-creation or missing-detail behavior. They also guard the original one-question, self-sufficient-option and answer-lines requirements and their order.
- T2.AC2: The isolated-home installer test verifies byte-for-byte equality with canonical pragmatic.md, not just its header; no network or real-home writes are needed. Existing keep and forced-refresh/backup tests pass unchanged.
- T2.AC3: Run `uv run pytest tests/commands/test_pragmatic_plain_english.py tests/cli/test_install_user_setup.py tests/cli/test_install_keep.py tests/commands/test_sweep_command.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_mapping.py tests/skills/test_review_severity_rule.py -v`, then `uv run pytest`, `make lint`, `make sync-dev` and `make verify-sync`; retain observed outputs under ./artifacts/. Report any unrelated failures accurately rather than changing unrelated code or claiming a pass.
- T2.AC4: Treat sync verification as a separate regression check, not output-style delivery proof. State that static content, installation and sample review do not guarantee live model responses obey the rule.

Global constraints: 

- Change only the canonical Pragmatic style and its focused content/delivery tests; leave core RULES, worker communications, AskUserQuestion, installer behavior and Makefile behavior unchanged.
- Do not generate or curate detail files merely to provide a link. Never change the real user's home configuration; installation checks use temporary homes.
- Preserve all existing decision-request, answer-line and general response-format rules unchanged. Required question context is useful information, not filler prohibited by the no-preamble rule.
- Work on the existing feature branch against integration. Stage `.dev/tasks/` including evidence, but never stage `.dev/issues/`, generated `.claude/` mirrors or project-root `artifacts/`.
- Decided for this work: Nothing to decide: build what the issue asks for, within its own scope.


Start sha: 173e7339c87317b5cc18664374556bc0ce5845eb
Diff against the start snapshot: diff --git a/tests/cli/test_install_user_setup.py b/tests/cli/test_install_user_setup.py
index dee9564d5..cb3250e6b 100644
--- a/tests/cli/test_install_user_setup.py
+++ b/tests/cli/test_install_user_setup.py
@@ -71,6 +71,7 @@ def test_output_style_installs(tmp_path: Path) -> None:
     assert ok, message
     style = tmp_path / ".claude" / "output-styles" / "pragmatic.md"
     assert style.read_text().startswith("---\nname: Pragmatic")
+    assert style.read_bytes() == (PKG / "output-styles" / "pragmatic.md").read_bytes()
 
 
 def test_settings_defaults_fill_only_missing_values(tmp_path: Path) -> None:
diff --git a/tests/commands/test_pragmatic_plain_english.py b/tests/commands/test_pragmatic_plain_english.py
index 344e29c3f..e135b6dfa 100644
--- a/tests/commands/test_pragmatic_plain_english.py
+++ b/tests/commands/test_pragmatic_plain_english.py
@@ -25,6 +25,29 @@ _PLAIN_ENGLISH_BULLETS = [
     "- Before sending, check four things:",
 ]
 
+_QUESTION_CONTEXT = (
+    "- Before every question or decision request (including approval), assume the user "
+    "is coming in blind, with none of the session's context. Give the context, "
+    "implications and risks in roughly one line each before asking; this is necessary "
+    "context, not filler. Link an existing file with more detail when available. "
+    "Never create a file just to link it. If no existing file has the detail, say so plainly."
+)
+
+_DECISION_BULLETS = [
+    "- Never ask what can be self-answered. Three-way gate before surfacing anything: "
+    "(a) answer findable in the artifacts/code/own capability: resolve it and report, "
+    "never ask; (b) genuinely the user's decision (taste, scope, priorities, destructive "
+    "or outward actions): ask EXACTLY ONE clear plain-English question with a "
+    "recommendation; (c) neither (speculative, non-actionable): do not raise it.",
+    '- No hedging: no half-formed "one nuance worth flagging" offers that are neither '
+    "a committed action nor a clear question.",
+    "- Present decisions ONE at a time, never as a batched table of terms. Each option "
+    "must be self-sufficient: define the term, state concretely what each value would "
+    "DO and why it matters, give an example, and include a recommendation.",
+    '- Never manufacture a multi-option "design decision" out of a defect-to-fix. '
+    "State the defect plainly in one sentence with the one concrete example first.",
+]
+
 _WRAP_UP_HEADINGS = [
     "**What I did**",
     "**How**",
@@ -63,6 +86,28 @@ def test_plain_english_bullets_sit_in_the_writing_conventions_section():
         assert bullet in section
 
 
+def test_question_context_rule_is_unique_and_in_decision_requests():
+    text = _text()
+    section = text.split("#### Decision requests", 1)[1].split(
+        "#### Status and wrap-ups", 1
+    )[0]
+    assert text.count(_QUESTION_CONTEXT) == 1
+    assert _QUESTION_CONTEXT in section
+
+
+def test_existing_question_rules_remain_in_source_order():
+    text = _text()
+    section = text.split("#### Decision requests", 1)[1].split(
+        "#### Status and wrap-ups", 1
+    )[0]
+    for bullet in _DECISION_BULLETS:
+        assert text.count(bullet) == 1, bullet
+        assert bullet in section
+    assert _in_order(
+        text, [_PLAIN_ENGLISH_BULLETS[2], _QUESTION_CONTEXT, *_DECISION_BULLETS]
+    )
+
+
 def test_wrap_up_template_names_the_five_headings_in_order():
     text = _text()
     template = text.split("**Wrap-up** (completed work;", 1)[1].split(

Full new task evidence file .dev/tasks/to-do/TASK-WF-issueSummary-20261126-044758/artifacts/T2-review.md:
start=173e7339c87317b5cc18664374556bc0ce5845eb tree=pending

T2.AC1: {{RF_PLACEHOLDER:ac1}}
T2.AC2: {{RF_PLACEHOLDER:ac2}}
T2.AC3: {{RF_PLACEHOLDER:ac3}}
T2.AC4: {{RF_PLACEHOLDER:ac4}}

Findings: {{RF_PLACEHOLDER:findings}}

Observed verification: focused run 300 passed (T2-focused-tests.log:311); full run 17 failed, 25149 passed, 69 skipped, 11 errors (T2-full-tests.log:25773). Full-run failures concern absent generated .claude mirrors and two tests that require the ruff Python module in the local environment. After the prescribed sync, the affected audit/sync/adapter test set has 1115 passed and only those same two missing-module failures (T2-environment-recheck.log:1166). None of the failing test paths is task-owned, and their tracebacks do not implicate the changed style or its tests. No unrelated source was changed and no missing tool was installed. make lint passed (T2-lint.log:144), make sync-dev completed (T2-sync.log:2), and make verify-sync passed (T2-verify-sync.log:201). The guard also rejected ten invalid rule variants (T2-guard-negatives.log:11). The full suite is not claimed green.

Verification boundary: Static content assertions, exact installed-byte equality in a temporary home, and sample wording review do not guarantee live model responses follow the instruction. Sync checks are independent regression checks, not proof that output styles are delivered. Installer behavior and the existing keep/force/backup tests remain unchanged. No real-home installation or live-model evaluation was run. Typecheck is skipped: no configured typecheck target was found and no production Python code changed.

AC-required observed outputs are under .dev/tasks/to-do/TASK-WF-issueSummary-20261126-044758/artifacts: T2-focused-tests.log, T2-full-tests.log, T2-lint.log, T2-sync.log, T2-verify-sync.log, T2-environment-recheck.log, T2-guard-negatives.log. Read their outcome rows directly for evidence-type AC.
Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:40:07Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-758
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-758
call codegraph only when index_state: fresh, never to widen scope
Grep/Read floor: two test files changed; no production symbols changed; no other indexed file depends on these test files. Existing keep/force/backup tests remain unchanged.
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
