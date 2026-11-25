ea941ce4f5b0d55e65af541fd94e3aa178d31281
Review one task for spec compliance.

Task brief: ## Task 7: Add the four create-decision tests and their mutation cases

Depends on: Task 6

Edit `tests/skills/test_issue_protocol.py`, using its existing helpers `_text`, `REFS`, `TEMPLATES`, `SKILL` and the mutation style of `test_plan_section_check_fails_when_a_heading_is_removed` (lines 784-811). Add exactly these four tests (names from the issue). `test_create_questions_only_for_contradictions`: the Contradiction prompt rule section of `refs/create.md` asks one question only for a supported contradiction, names all four categories and "exactly one", applies the answer before Wave 5, and no longer contains the old trigger text or the old "keep all" choice. `test_draft_notes_separates_additions_and_contradictions`: the template keeps the two headings, states "no question" for New material and "one question" for Contradictions, and keeps `None` as the empty marker. `test_create_reports_additions_without_approval`: Wave 5 step 8 of `refs/create.md` and create step 6 of SKILL.md both contain the line form `kept without approval:`, while the "never shown for approval" wording is checked in the places that carry it, which are the Contradiction prompt rule section of `refs/create.md` and the "Posts go up directly" line of SKILL.md (not in the print steps). `test_contradiction_categories_require_user_evidence`: the reference and the template both require category, the user's own words and conflicting evidence, treat an incomplete line as new material, and say worker disagreement with a supplied flag is not a contradiction. For each, add a mutation case that edits a copy of the text under `tmp_path` (restore the old broad trigger, delete a category, delete the `None` rule, delete the flag exception) and asserts the check reports the problem, following the problems-list pattern of `plan_section_problems`. The old trigger text must never be written as one literal string anywhere in `tests/`: build it from fragments joined at run time (for example the three words groups "lists new", "material or a", "contradiction"), so a search of `tests/` for the whole phrase finds nothing. Do not change `ALLOWED_TOOLS`, `plan_section_problems` or the existing tests.

Acceptance criteria:
- [T7.AC1] `uv run pytest tests/skills/test_issue_protocol.py -k "create_questions_only_for_contradictions or draft_notes_separates_additions_and_contradictions or create_reports_additions_without_approval or contradiction_categories_require_user_evidence" -v` runs all four named tests and they pass.
- [T7.AC2] Each of the four checks has at least one mutation case that fails against the old text (restoring the old broad trigger makes the first check report a problem).
- [T7.AC3] `grep -rn "new material or a contradiction" tests/` prints nothing.
- [T7.AC4] `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py tests/skills/test_worker_contract.py -v` passes with no existing test edited except the single key in Task 4.
- [T7.AC5] `test_stage_claim_skips_recommend_and_plain_claim_keeps_it` (lines 1162-1180) is untouched and passes.
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
Start sha: ea941ce4f5b0d55e65af541fd94e3aa178d31281
Diff against the start snapshot: diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index 3026a7080..116be2bd3 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -1178,3 +1178,189 @@ def test_stage_claim_skips_recommend_and_plain_claim_keeps_it():
     )
     assert "`Default row not used` line is not written" in claim
     assert "a `--stage` claim never calls it" in claim
+
+
+# --- create decision rule: ask only for a contradiction (issue 834) -------------------
+
+CONFLICT_CATEGORIES = [
+    "reversed choice",
+    "dropped requirement",
+    "changed flag",
+    "contradicted by verified code",
+]
+# The old broad trigger and the old first choice are built from fragments, so no
+# whole copy of either sits in tests/ (a search of tests/ for them finds nothing).
+OLD_TRIGGER = "new" + " material" + " or a" + " contradiction"
+OLD_KEEP_ALL = '"keep' + ' all"'
+
+
+def prompt_rule_section(text: str) -> str:
+    """The body of the Contradiction prompt rule section of refs/create.md."""
+    start = text.index("### Contradiction prompt rule")
+    return text[start : text.index("\n## ", start)]
+
+
+def line_starting(text: str, prefix: str) -> str:
+    return next((ln for ln in text.splitlines() if ln.startswith(prefix)), "")
+
+
+def _mutated(tmp_path: Path, name: str, text: str) -> str:
+    copy = tmp_path / name
+    copy.write_text(text, encoding="utf-8")
+    return copy.read_text(encoding="utf-8")
+
+
+def create_question_problems(ref: str, skill: str) -> list[str]:
+    """Problems with the rule that create asks only for a supported contradiction."""
+    section = prompt_rule_section(ref)
+    problems = [
+        f"prompt rule section lacks the category {name!r}"
+        for name in CONFLICT_CATEGORIES
+        if name not in section
+    ]
+    for needle in ("exactly one", "before Wave 5", "zero questions"):
+        if needle not in section:
+            problems.append(f"prompt rule section lacks {needle!r}")
+    for where, text in (("refs/create.md", ref), ("SKILL.md", skill)):
+        if OLD_TRIGGER in text:
+            problems.append(f"{where} still carries the old broad trigger")
+    if OLD_KEEP_ALL in ref:
+        problems.append("refs/create.md still offers the old keep-all choice")
+    return problems
+
+
+def draft_notes_problems(text: str) -> list[str]:
+    """Problems with the two lists and their different consequences."""
+    problems = []
+    if headings(text) != ["New material", "Contradictions"]:
+        problems.append("the two headings are not exactly New material, Contradictions")
+    if text.count("\n- None") != 2:
+        problems.append("each list must keep a '- None' empty marker")
+    for needle in ("no question", "one question"):
+        if needle not in text:
+            problems.append(f"the template does not say {needle!r}")
+    return problems
+
+
+def additions_report_problems(ref: str, skill: str) -> list[str]:
+    """Problems with the retained-additions line and the no-approval promise."""
+    problems = []
+    step8 = line_starting(ref, "8. Print the issue URL")
+    step6 = line_starting(skill, "6. **Wave 5, post.**")
+    if "kept without approval:" not in step8:
+        problems.append(
+            "refs/create.md Wave 5 step 8 lacks the retained-additions line"
+        )
+    if "kept without approval:" not in step6:
+        problems.append("SKILL.md create step 6 lacks the retained-additions line")
+    if "never shown for approval" not in prompt_rule_section(ref):
+        problems.append(
+            "the prompt rule section no longer says the body is never shown"
+        )
+    if "never shown for approval" not in line_starting(skill, "- Posts go up directly"):
+        problems.append("SKILL.md 'Posts go up directly' no longer says it")
+    return problems
+
+
+def evidence_rule_problems(ref: str, template: str) -> list[str]:
+    """Problems with the three-part contradiction rule and the flag carve-out."""
+    problems = []
+    for where, text in (("refs/create.md", ref), ("draft-notes template", template)):
+        for needle in (
+            "user's own words",
+            "conflicting evidence",
+            "missing any of the three",
+            "disagreement with a",
+            "not a contradiction",
+        ):
+            if needle not in text:
+                problems.append(f"{where} lacks {needle!r}")
+    return problems
+
+
+def test_create_questions_only_for_contradictions():
+    ref, skill = _text(REFS / "create.md"), _text(SKILL)
+    assert create_question_problems(ref, skill) == []
+
+
+def test_create_question_check_fails_when_the_old_trigger_returns(tmp_path):
+    ref, skill = _text(REFS / "create.md"), _text(SKILL)
+    back = ref + "\nAsk when `draft-notes.md` lists " + OLD_TRIGGER + ".\n"
+    problems = create_question_problems(_mutated(tmp_path, "create.md", back), skill)
+    assert problems == ["refs/create.md still carries the old broad trigger"]
+
+
+@pytest.mark.parametrize("name", CONFLICT_CATEGORIES)
+def test_create_question_check_fails_when_a_category_is_deleted(name, tmp_path):
+    ref, skill = _text(REFS / "create.md"), _text(SKILL)
+    section = prompt_rule_section(ref)
+    cut = ref.replace(section, section.replace(name, "removed"))
+    problems = create_question_problems(_mutated(tmp_path, "create.md", cut), skill)
+    assert problems == [f"prompt rule section lacks the category {name!r}"]
+
+
+def test_create_question_check_fails_when_the_keep_all_choice_returns(tmp_path):
+    ref, skill = _text(REFS / "create.md"), _text(SKILL)
+    back = ref + "\nChoices: " + OLD_KEEP_ALL + ".\n"
+    problems = create_question_problems(_mutated(tmp_path, "create.md", back), skill)
+    assert problems == ["refs/create.md still offers the old keep-all choice"]
+
+
+def test_draft_notes_separates_additions_and_contradictions():
+    assert draft_notes_problems(_text(TEMPLATES / "draft-notes.md")) == []
+
+
+def test_draft_notes_check_fails_when_the_none_marker_is_deleted(tmp_path):
+    text = _text(TEMPLATES / "draft-notes.md")
+    cut = text.replace("\n- None", "\n- ", 1)
+    problems = draft_notes_problems(_mutated(tmp_path, "draft-notes.md", cut))
+    assert problems == ["each list must keep a '- None' empty marker"]
+
+
+def test_draft_notes_check_fails_when_the_consequences_are_deleted(tmp_path):
+    text = _text(TEMPLATES / "draft-notes.md")
+    cut = text.replace("cause no question", "cause nothing").replace(
+        "exactly one question", "a prompt"
+    )
+    problems = draft_notes_problems(_mutated(tmp_path, "draft-notes.md", cut))
+    assert problems == [
+        "the template does not say 'no question'",
+        "the template does not say 'one question'",
+    ]
+
+
+def test_create_reports_additions_without_approval():
+    assert additions_report_problems(_text(REFS / "create.md"), _text(SKILL)) == []
+
+
+def test_additions_report_check_fails_when_the_literal_is_removed(tmp_path):
+    ref, skill = _text(REFS / "create.md"), _text(SKILL)
+    cut = skill.replace("kept without approval:", "kept")
+    problems = additions_report_problems(ref, _mutated(tmp_path, "SKILL.md", cut))
+    assert problems == ["SKILL.md create step 6 lacks the retained-additions line"]
+
+
+def test_additions_report_check_fails_when_the_promise_is_removed(tmp_path):
+    ref, skill = _text(REFS / "create.md"), _text(SKILL)
+    section = prompt_rule_section(ref)
+    cut = ref.replace(section, section.replace("never shown for approval", "shown"))
+    problems = additions_report_problems(_mutated(tmp_path, "create.md", cut), skill)
+    assert problems == [
+        "the prompt rule section no longer says the body is never shown"
+    ]
+
+
+def test_contradiction_categories_require_user_evidence():
+    ref, template = _text(REFS / "create.md"), _text(TEMPLATES / "draft-notes.md")
+    assert evidence_rule_problems(ref, template) == []
+
+
+@pytest.mark.parametrize(
+    "needle",
+    ["conflicting evidence", "missing any of the three", "disagreement with a"],
+)
+def test_evidence_rule_check_fails_when_a_requirement_is_deleted(needle, tmp_path):
+    ref, template = _text(REFS / "create.md"), _text(TEMPLATES / "draft-notes.md")
+    cut = template.replace(needle, "removed")
+    problems = evidence_rule_problems(ref, _mutated(tmp_path, "draft-notes.md", cut))
+    assert problems == [f"draft-notes template lacks {needle!r}"]


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
