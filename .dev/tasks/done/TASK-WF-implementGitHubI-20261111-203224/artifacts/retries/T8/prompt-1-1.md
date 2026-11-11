a066ff74f53e8ec2ede8648da6c8d660d246d04a
Review one task for spec compliance.

Task brief: 
## Task 8: Add pins for the new coordinator rules, with a failing-case test

Depends on: Task 7

In `tests/skills/test_worker_contract.py` add new `RULE_PHRASES` entries and make sure the existing tests that iterate `RULE_PHRASES` pick them up. Add: a rule for the preflight whose phrases are `### Before the first task-create for a command`, `the coordinator decides by the two-copy test` and both copy paths `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`; a rule whose phrase is `re-invocation keeps every token` (it must also match the Brief guard paragraph); a rule for the positive default whose phrases include `on every \`Command:\` line` and `never as a session-wide setting`; a rule for the drop list whose phrases name `approval-required`, `--strategy planning`, `--handoff implement` and `WC-9`; a rule whose phrases are `a person-in-the-loop run is not a worker` and `Skill call`; a rule for the refusal repairs whose phrases are the repair clauses of Task 1. Add one negative test, in the style of `test_p2_brief_check_fails_when_until_p2_is_back`, that removes the `the coordinator decides by the two-copy test` phrase from the contract text and asserts the rule check raises `AssertionError`.

Acceptance criteria:
- T8.AC1: `uv run pytest tests/skills/test_worker_contract.py -q` passes and its pass count is greater than before the change.
- T8.AC2: The new negative test fails when the phrase `the coordinator decides by the two-copy test` is removed from a copy of the contract text.
- T8.AC3: Every new pin phrase exists word for word in `src/superclaude/core/WORKER-CONTRACT.md` as written by Tasks 1 to 4.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: a066ff74f53e8ec2ede8648da6c8d660d246d04a
Diff against the start snapshot: 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 6b2631a9d..73202b099 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -363,6 +363,54 @@ RULE_PHRASES = {
             "Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).",
         ],
     ),
+    "coordinator-preflight": (
+        None,
+        [
+            "### Before the first task-create for a command",
+            "the coordinator decides by the two-copy test",
+            "`.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`",
+            "A run of that command that needs a person at a gate is a person-in-the-loop run, not a worker.",
+        ],
+    ),
+    "reinvocation-keeps-every-token": (
+        None,
+        [
+            "re-invocation keeps every token of the `Command:` line and only adds the answer",
+        ],
+    ),
+    "positive-default": (
+        None,
+        [
+            "on every `Command:` line, for each step and never as a session-wide setting",
+            'unless the two-copy test in "Before the first task-create for a command" (section 4) fails for that command',
+        ],
+    ),
+    "flag-drops": (
+        None,
+        [
+            "skip every approval-required item and list it as not applied",
+            "`/sc:test` ends `succeeded` even when its suite fails",
+            "`/sc:research` is forced to `--strategy planning`",
+            "`/sc:workflow` skips `--handoff implement`",
+            "every push, PR, comment and other outward action is off (WC-9)",
+        ],
+    ),
+    "skill-call-and-person-in-the-loop": (
+        None,
+        [
+            "A command is started through its Skill call (WC-7)",
+            "A person-in-the-loop run is not a worker",
+        ],
+    ),
+    "guard-refusal-repairs": (
+        None,
+        [
+            "(coordinator: add --unattended and exactly one report directory to this Command: line, then create a new Task)",
+            "(coordinator: refresh ~/.claude if its copy is stale, or drop --unattended for this command, then create a new Task)",
+            "(coordinator: refresh the stale copy named in <paths>, normally ~/.claude, then create a new Task)",
+            "A refusal is report-only: the worker never installs or refreshes a command copy and never rewrites its own brief",
+        ],
+    ),
 }
 
 GUARD_LINE = (
@@ -999,6 +1047,36 @@ def test_nested_result_check_fails_when_a_phrase_is_removed(phrase):
         _check_nested_result_rule(_contract().replace(phrase, ""))
 
 
+_PREFLIGHT_HEADING = "### Before the first task-create for a command"
+_PREFLIGHT_PHRASES = (
+    "the coordinator decides by the two-copy test",
+    "re-invocation keeps every token",
+)
+
+
+def _check_preflight_section(text: str) -> None:
+    """Both coordinator pins sit inside the numbered preflight subsection, not above it."""
+    assert text.count(_PREFLIGHT_HEADING) == 1, (
+        "preflight heading not found exactly once"
+    )
+    body = text.split(_PREFLIGHT_HEADING, 1)[1].split("\n### ", 1)[0]
+    for phrase in _PREFLIGHT_PHRASES:
+        assert phrase in body, f"preflight subsection lacks: {phrase}"
+    assert re.search(r"^1\. .*\n2\. .*\n3\. ", body, re.M), (
+        "preflight steps are not numbered"
+    )
+
+
+def test_preflight_subsection_holds_the_coordinator_pins():
+    _check_preflight_section(_contract())
+
+
+@pytest.mark.parametrize("phrase", _PREFLIGHT_PHRASES)
+def test_preflight_check_fails_when_a_pin_is_removed(phrase):
+    with pytest.raises(AssertionError):
+        _check_preflight_section(_contract().replace(phrase, ""))
+
+
 def test_unattended_sections_match_the_listed_commands():
     _check_no_unattended_sections()
 


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
