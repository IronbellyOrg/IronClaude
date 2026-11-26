96b10a0052c479adad15d5178b613c07a6f64a37
Review one task for spec compliance.

Task brief: ## Task 6: Create the policy test file with the name checker and its tests

Depends on: Task 5

Create `tests/core/test_how_we_work_worktree_policy.py` following the contract of section 5 of `./source.md`. Imports are `re`, `pytest` and `pathlib.Path`; constants `_REPO = Path(__file__).resolve().parents[2]`, `_GUIDE`, `_TWIN` (the mirror) and `_DECK`. Define the helpers `_NUMBER_RUN` (the regular expression `(?<!\d)\d{2,4}(?!\d)`, the same bound as `scripts/worktree_cleanup.py:1462`), `branch_errors(branch)` (whole string matches `^[A-Za-z0-9]+(-[A-Za-z0-9]+)*/issue-[1-9][0-9]*(-[a-z0-9]+)*$`, `len(branch) <= 24`, the words part has no `_NUMBER_RUN` match, and when the bare form `<login>/issue-<N>` is itself over 24 the error text contains the word `stop`) and `max_words_length(login, digits)` (`16 - len(login) - digits`). Add the tests `test_checker_accepts`, `test_checker_rejects`, `test_bare_form_over_the_limit_is_a_stop` and `test_budget_formula`, parametrized with the names and values listed in the section 5 table of `./source.md`. The checker lives only in this test file; no production code is added.

Acceptance criteria:
T6.AC1: `tests/core/test_how_we_work_worktree_policy.py` exists and `uv run pytest tests/core/test_how_we_work_worktree_policy.py -q` passes.
T6.AC2: `branch_errors` accepts `clayphi/issue-289-wtrule` (24), `clayphi/issue-834-clean` (23), `ironbelly/issue-517-orca` (24), `clayphi/issue-1234-docs` (23), `clayphi/issue-289` (17), `longloginname/issue-289` (23), `Ab-c/issue-5` (12) and `a/issue-1-v12345` (16), and rejects `clayphi/issue-289-wtrules` (25), a name with a space, `clayphi/issue-0289`, `clayphi/issue-`, `clayphi/issue-289-`, `clayphi/issue-289-py312`, `clayphi/issue-289-v2024`, `a--b/issue-1`, `-a/issue-1` and `a/issue-1-x/y`.
T6.AC3: `branch_errors("averylonglogin1/issue-289")` returns an error containing `stop`; `max_words_length("clayphi", 3)` is 6, `max_words_length("clayphi", 4)` is 5 and `max_words_length("longloginname", 3)` is 0.
T6.AC4: `uv run ruff check tests/core/test_how_we_work_worktree_policy.py` and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py` pass.
Global constraints: ## Constraints

- Scope is five deliverables: the new guide section and the removal-timing pointer in `src/superclaude/core/HOW-WE-WORK.md`, the byte-identical mirror `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, the worktree card and build footer of `docs/onboarding/ironclaude-onboarding.html`, and the new `tests/core/test_how_we_work_worktree_policy.py`. No production code changes.
- Out of scope: the claim launcher and its `issue-<N>` naming, the cleanup script and its rules, the issue watcher, the `CLAUDE.md` examples at lines 318-341, the issue 290 card, the slide introduction at lines 516-518, and any tool that extracts lessons. Section 1 of `./source.md` lists them.
- The open owner questions of section 7 of `./source.md` (dropping the words from a name, lessons of issue-less worktrees, whether the watcher or the claim should refuse an issue that already has a worktree, the slide introduction, the `CLAUDE.md` examples, the footer rule) are not decided by this plan and are not written into the guide. They belong in the pull request body.
- The guide is a shared file: the level-table, routing-table and other-commands marker comments and every other section stay as they are, and every line the change adds is ASCII (plain hyphens, no en dashes).
- The mirror is never edited by hand: it is a copy of the guide after the guide's last edit.
- Python and tests run through uv (`uv run pytest`, `uv run ruff`); never `python -m` or bare `pip`.
- The tasks run in a straight line and the new test file comes last (the design's section 6 puts it first) so that the acceptance criteria of every task can pass the moment that task is done.
- Stage the changed files and `.dev/tasks`; never stage anything under `.claude/` or `.dev/issues/`. Staging is not committing.
- Where this plan and `./source.md` disagree this plan wins: it overrides source.md line 106 (page-wide absence of "is being worked out in") and lines 53 and 108 (the list of 13 key phrases, now 15), as stated in Tasks 1, 4 and 7 (D-1, D-3).
Start sha: 96b10a0052c479adad15d5178b613c07a6f64a37
Diff against the start snapshot: NEW FILE --- a/tests/core/test_how_we_work_worktree_policy.py
+++ b/tests/core/test_how_we_work_worktree_policy.py
@@ -0,0 +1,116 @@
+"""Policy checks for the "Worktrees and branches" section of the how-we-work guide.
+
+The name checker lives only in this file. It is the machine-readable form of the
+naming rule in the guide, and no production code uses it.
+"""
+
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+import pytest
+
+_REPO = Path(__file__).resolve().parents[2]
+_GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"
+_TWIN = _REPO / "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md"
+_DECK = _REPO / "docs/onboarding/ironclaude-onboarding.html"
+
+# Same bound as `_NAME_NUMBER_RE` in scripts/worktree_cleanup.py: cleanup reads a
+# standalone run of 2 to 4 digits in a branch name as an issue number.
+_NUMBER_RUN = re.compile(r"(?<!\d)\d{2,4}(?!\d)")
+_BRANCH_RE = re.compile(
+    r"^[A-Za-z0-9]+(-[A-Za-z0-9]+)*/issue-[1-9][0-9]*(-[a-z0-9]+)*$"
+)
+_ISSUE_PART_RE = re.compile(r"issue-[1-9][0-9]*")
+_MAX_LENGTH = 24
+
+
+def branch_errors(branch: str) -> list[str]:
+    """Reasons a branch name breaks the rule; an empty list means it is valid."""
+    if not _BRANCH_RE.match(branch):
+        return ["does not match <login>/issue-<N>[-<words>], no spaces"]
+    login, rest = branch.split("/", 1)
+    issue_part = _ISSUE_PART_RE.match(rest).group(0)
+    words = rest[len(issue_part) :]
+    errors = []
+    bare = f"{login}/{issue_part}"
+    if len(bare) > _MAX_LENGTH:
+        errors.append(
+            f"stop: even {bare} is over {_MAX_LENGTH} characters; "
+            "create nothing and ask the owner"
+        )
+    elif len(branch) > _MAX_LENGTH:
+        errors.append(f"{len(branch)} characters, at most {_MAX_LENGTH}")
+    if _NUMBER_RUN.search(words):
+        errors.append("the words hold a run of 2 to 4 digits that cleanup reads")
+    return errors
+
+
+def max_words_length(login: str, digits: int) -> int:
+    """Characters left for the words once the login and the issue number are in."""
+    return _MAX_LENGTH - len(login) - len("/issue-") - digits - len("-")
+
+
+@pytest.mark.parametrize(
+    "branch",
+    [
+        "clayphi/issue-289-wtrule",  # 24
+        "clayphi/issue-834-clean",  # 23
+        "ironbelly/issue-517-orca",  # 24
+        "clayphi/issue-1234-docs",  # 23
+        "clayphi/issue-289",  # 17
+        "longloginname/issue-289",  # 23
+        "Ab-c/issue-5",  # 12
+        "a/issue-1-v12345",  # 16; a 5-digit run is not a 2 to 4 digit run
+    ],
+)
+def test_checker_accepts(branch):
+    assert branch_errors(branch) == []
+
+
+@pytest.mark.parametrize(
+    "branch",
+    [
+        "clayphi/issue-289-wtrules",  # 25 characters
+        "clayphi/issue-289 wtrule",  # a space
+        "clayphi/issue-0289",  # leading zero
+        "clayphi/issue-",  # no issue number
+        "clayphi/issue-289-",  # empty words
+        "clayphi/issue-289-py312",  # a 3 digit run in the words
+        "clayphi/issue-289-v2024",  # a 4 digit run in the words
+        "a--b/issue-1",  # a double hyphen in the login
+        "-a/issue-1",  # a login that starts with a hyphen
+        "a/issue-1-x/y",  # a second slash
+    ],
+)
+def test_checker_rejects(branch):
+    assert branch_errors(branch)
+
+
+def test_bare_form_over_the_limit_is_a_stop():
+    errors = branch_errors("averylonglogin1/issue-289")  # 25 characters
+    assert errors
+    assert "stop" in " ".join(errors)
+
+
+@pytest.mark.parametrize(
+    ("login", "digits", "expected"),
+    [
+        ("clayphi", 3, 6),
+        ("clayphi", 4, 5),
+        ("longloginname", 3, 0),
+        ("abcdefghijklmn", 3, -1),  # the bare form is exactly 24 characters
+        ("abcdefghijklmno", 3, -2),  # the bare form is 25 characters
+    ],
+)
+def test_budget_formula(login, digits, expected):
+    assert max_words_length(login, digits) == expected
+    assert expected == 16 - len(login) - digits
+    bare = f"{login}/issue-{'1' * digits}"
+    # The bare form overflows exactly when the login and the digits make 18.
+    assert (len(bare) > _MAX_LENGTH) == (len(login) + digits >= 18)
+    assert any("stop" in e for e in branch_errors(bare)) == (len(bare) > _MAX_LENGTH)
+    if expected >= 1:
+        assert branch_errors(f"{bare}-{'b' * expected}") == []
+        assert branch_errors(f"{bare}-{'b' * (expected + 1)}")


Codegraph context
index_state: fresh
checked_at: 2026-11-26T14:52:15Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-289
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents (floor: Grep for the new names; codegraph fresh but the file is new this run, so graph rows would be leads only): nothing imports tests/core/test_how_we_work_worktree_policy.py or its helpers (Grep for `branch_errors` and `max_words_length` outside the file: no hit). The checker's number bound mirrors scripts/worktree_cleanup.py:1462 (`_NAME_NUMBER_RE`). Context only.

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