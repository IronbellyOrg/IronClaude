744981f44a45e66809cb88abc8b938beb255030d
Review one task for spec compliance.

Task brief: ## Task 8: Add command and protocol agreement checks

Depends on: Task 7

Edit `tests/commands/test_issue_command.py`, adding tests in its existing style (module helper `_text()` for the command, `SKILL` for the skill) that check the command file and SKILL.md agree: both keep the direct-posting promise, both say the only pause is one question for a contradiction of the user's own words, neither contains the old broad trigger (built from fragments at run time, as in Task 7, so no whole copy of it sits in `tests/`), and the command's create Outputs row still lists the six create files and mentions retained additions. Add one mutation case on a copy that restores "nothing is shown for approval first" without the contradiction exception and asserts the agreement check fails. Do not weaken or replace the existing metadata, options, STOP-rule, activation, `test_no_source_tree_path` or rule-10 tests.

Acceptance criteria:
- [T8.AC1] `uv run pytest tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py -v` passes, with the new agreement tests listed in the output.
- [T8.AC2] The mutation case fails when the contradiction exception is removed from the command text copy.
- [T8.AC3] `grep -rn "new material or a contradiction" tests/` still prints nothing.
- [T8.AC4] The five-file focused gate `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py tests/skills/test_worker_contract.py tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py -v` passes.
Global constraints: ## Constraints

- Base branch is `integration` (the issue text says `master`; that is stale). Edit only canonical sources under `src/superclaude/`, `docs/` and `tests/`. The generated project mirrors are refreshed only by `make sync-dev`, never edited by hand.
- Keep `AskUserQuestion` in the `allowed-tools` line of `src/superclaude/skills/sc-issue-protocol/SKILL.md` (pinned by `ALLOWED_TOOLS` in `tests/skills/test_issue_protocol.py:40`).
- Keep the full issue body never shown for approval (default B1), the post-create flag pushback comment (create Wave 5, `templates/create-review-comment.md`), the three required plan sections and their one shared rule sentence (`PLAN_SECTIONS_RULE`, `tests/skills/test_issue_worker_agents.py:34-39`), claim assignment, ClickUp, Orca, watcher and launch safeguards, the stage-claim recommendation skip from pull request 833, and the launched `worktree` agent's plan-approval boundary. None of these text blocks may change in meaning. Task 9 and Task 10 each carry a check that the launch-level safeguards stay untouched.
- Lines of `src/superclaude/skills/sc-issue-protocol/refs/create.md` that `tests/skills/test_worker_contract.py` pins verbatim (the GitHub-write rule paragraph near line 9, the lookup paragraph near line 20 and step 6 of Wave 5 near line 95) must stay byte-identical. SKILL.md step 6 of create mode (line 103) is also pinned there; Task 4 updates that pinned copy together with the line.
- Do not add a new return-contract field, flag, script, agent or dependency to the product. The classification is instruction text plus tests, as the current rule is. The kit of Task 9 is evidence tooling under this package's `./artifacts/`, not product code.
- A contradiction counts only with all three parts: its category, the user's own words (a quote from `description.md` or a flag passed on the command line), and the conflicting evidence (draft text, or a verified `path:line` of code the worker read). A line missing any part is New material. `None` is the empty marker, never an item, and a notes file with `- None` under both headings is the same state as empty notes.
- The changed-flag category means the drafted issue itself would not honor a flag the user passed (for example it would be filed with another mode or type). A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag; it stays a pushback comment.
- When an addition is also the only evidence for a contradiction, it is listed under Contradictions, and "keep my wording" removes only that content; every other New material item stays.
- The session that carries out this plan is a launched session whose guard refuses the installer for the whole tool, a child agent session, a Skill call to the issue protocol and any Bash text that names the GitHub CLI together with `issue` or `api`. No task here runs a create flow, starts a child session or runs `superclaude install`. Task 9 therefore prepares a kit and leaves the controlled runs to a person, and the final report calls the plan partial until that run fills the matrix.
Start sha: 744981f44a45e66809cb88abc8b938beb255030d
Diff against the start snapshot: diff --git a/tests/commands/test_issue_command.py b/tests/commands/test_issue_command.py
index 279ba8282..456d916ce 100644
--- a/tests/commands/test_issue_command.py
+++ b/tests/commands/test_issue_command.py
@@ -268,3 +268,76 @@ def test_no_source_tree_path():
 @pytest.mark.parametrize("path", [COMMAND, SKILL], ids=["command", "skill"])
 def test_rule_10_line_is_carried_verbatim(path):
     assert RULE_10_LINE in path.read_text(encoding="utf-8").splitlines()
+
+
+# --- command and skill agree on the create question (issue 834) --------------------
+
+# The old broad trigger is built from fragments, so no whole copy of it sits in tests/.
+OLD_TRIGGER = "new" + " material" + " or a" + " contradiction"
+CREATE_FILES = [
+    "description.md",
+    "scout.md",
+    "flags.md",
+    "issue-body.md",
+    "draft-notes.md",
+    "create-review.md",
+]
+
+
+def agreement_problems(command: str, skill: str) -> list[str]:
+    """Problems with how the command file and SKILL.md describe the create question."""
+    problems = []
+    if "nothing is shown for approval first" not in command:
+        problems.append("the command lost the direct-posting promise")
+    if "never shown for approval" not in skill:
+        problems.append("SKILL.md lost the no-approval promise")
+    if "contradicts your own description, instruction or flag" not in command:
+        problems.append("the command lacks the contradiction exception")
+    if (
+        "supported contradiction of the user's own description, instruction or flag"
+        not in skill
+    ):
+        problems.append("SKILL.md lacks the contradiction-only prompt rule")
+    for where, text in (("the command", command), ("SKILL.md", skill)):
+        if OLD_TRIGGER in text:
+            problems.append(f"{where} still carries the old broad trigger")
+    row = next((ln for ln in command.splitlines() if ln.startswith("| create |")), "")
+    problems += [
+        f"the create Outputs row lacks {name}"
+        for name in CREATE_FILES
+        if name not in row
+    ]
+    if "printed in the final output" not in row:
+        problems.append("the create Outputs row does not mention retained additions")
+    return problems
+
+
+def test_command_and_skill_agree_on_the_create_question():
+    assert agreement_problems(_text(), SKILL.read_text(encoding="utf-8")) == []
+
+
+def test_agreement_check_fails_when_the_contradiction_exception_is_removed(tmp_path):
+    copy = tmp_path / "issue.md"
+    copy.write_text(re.sub(r" The one exception is `--create`:[^\n]*", "", _text()))
+    problems = agreement_problems(
+        copy.read_text(encoding="utf-8"), SKILL.read_text(encoding="utf-8")
+    )
+    assert problems == ["the command lacks the contradiction exception"]
+
+
+def test_agreement_check_fails_when_the_old_trigger_returns(tmp_path):
+    copy = tmp_path / "SKILL.md"
+    copy.write_text(
+        SKILL.read_text(encoding="utf-8") + f"\nAsk when notes list {OLD_TRIGGER}.\n"
+    )
+    problems = agreement_problems(_text(), copy.read_text(encoding="utf-8"))
+    assert problems == ["SKILL.md still carries the old broad trigger"]
+
+
+def test_agreement_check_fails_when_the_create_row_loses_a_file(tmp_path):
+    copy = tmp_path / "issue.md"
+    copy.write_text(_text().replace("`create-review.md`", "`review.md`"))
+    problems = agreement_problems(
+        copy.read_text(encoding="utf-8"), SKILL.read_text(encoding="utf-8")
+    )
+    assert problems == ["the create Outputs row lacks create-review.md"]


Codegraph context:
index_state=stale checked_at=2026-11-25T19:23:07Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-834 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-834
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor; dependents of the changed text that are not in this task's touched set are edited by later tasks of the plan.

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
