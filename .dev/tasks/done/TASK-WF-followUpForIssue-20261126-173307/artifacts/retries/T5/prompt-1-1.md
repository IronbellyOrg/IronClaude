e47b26891f6e0209ec370f4cc565607cd826ea4e
Review one task for spec compliance.

Task brief: ## Task 5: Rewrite the name checker in tests/core/test_how_we_work_worktree_policy.py to follow the answers

Edit `tests/core/test_how_we_work_worktree_policy.py` (top of file to the end of `test_budget_formula`, about lines 1 to 116). (b) Make the login optional in `_BRANCH_RE` so the bare form `issue-<N>[-<words>]` matches. (c) Rewrite `branch_errors`: no login (bare form): errors only for more than 24 characters in all and for a digit run in the words (`_NUMBER_RUN.search`); with a login: an error when the words are present and the whole name is over 24 characters ("drop the words"), an error for a digit run in the words, an error for a digit run in the login ("leave the login out and use issue-<N>-<words>"); a bare `<login>/issue-<N>` over 24 characters is no error (never stop). Because the cleanup pattern has a capture group, search with `.search` on the text only, never `.findall`. (d) Update the parametrized cases: accepts add `issue-289-wtrule`, `issue-289`, `averylonglogin/issue-289` (bare form over 24, kept), `dev1/issue-289`; rejects add `dev42/issue-289`, `dev42/issue-289-words`, `issue-289-py312`, `issue-0289`, `averylonglogin1/issue-289-x` (words do not fit); keep the other existing cases that still hold and remove none that still hold. (e) Replace `test_bare_form_over_the_limit_is_a_stop` by `test_bare_form_over_the_limit_is_kept` (accepted, no "stop" in any message) and update `test_budget_formula` so it no longer asserts a "stop" message: for words that fit it asserts `[]`, one character more asserts an error, and the bare form is always accepted.
Acceptance criteria:
T5.AC1: `uv run pytest tests/core/test_how_we_work_worktree_policy.py -q -k "checker or budget or bare"` passes, and the parametrized rejects include `dev42/issue-289` and the accepts include `averylonglogin/issue-289`.
T5.AC2: `uv run ruff check tests/core/test_how_we_work_worktree_policy.py` and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py` pass.
Global constraints: ## Constraints

- Test, guide, deck and CLAUDE.md edits only; no production code (nothing under `src/superclaude/cli/`, `scripts/`, hooks or skills changes).
- Never edit or stage anything under `.claude/`. `.dev/tasks/` stays staged.
- ASCII only in the guide section; keep every existing rule that the six answers do not change, in the owner's wording where the source quotes it.
- Decision recorded here: answer 2 says "never stop", so a name whose bare form `<login>/issue-<N>` is over 24 characters is kept and the work goes on. The sentence "create nothing and ask the owner", its key phrase and the "stop" test are replaced. A name that carries words over 24 characters is still an error: drop the words.
- Not in scope (MB-2): reading the digit-run pattern from scripts/worktree_cleanup.py. The user withdrew that item; the hand-copied _NUMBER_RUN of tests/core/test_how_we_work_worktree_policy.py stays as it is.
- The branch `clayphi/issue-289-rest` was created in the reused worktree with `git switch -c` on the owner's order; the guide's "never switch branches in a worktree" line is left as it is.
Start sha: e47b26891f6e0209ec370f4cc565607cd826ea4e
Diff against the start snapshot: --- a/tests/core/test_how_we_work_worktree_policy.py
+++ b/tests/core/test_how_we_work_worktree_policy.py
@@ -19,8 +19,10 @@
 # Same bound as `_NAME_NUMBER_RE` in scripts/worktree_cleanup.py: cleanup reads a
 # standalone run of 2 to 4 digits in a branch name as an issue number.
 _NUMBER_RUN = re.compile(r"(?<!\d)\d{2,4}(?!\d)")
+# The login is optional: a person whose login holds a run of 2 to 4 digits leaves it
+# out and uses the form `issue-<N>[-<words>]`.
 _BRANCH_RE = re.compile(
-    r"^[A-Za-z0-9]+(-[A-Za-z0-9]+)*/issue-[1-9][0-9]*(-[a-z0-9]+)*$"
+    r"^([A-Za-z0-9]+(-[A-Za-z0-9]+)*/)?issue-[1-9][0-9]*(-[a-z0-9]+)*$"
 )
 _ISSUE_PART_RE = re.compile(r"issue-[1-9][0-9]*")
 _MAX_LENGTH = 24
@@ -29,24 +31,26 @@
 def branch_errors(branch: str) -> list[str]:
     """Reasons a branch name breaks the rule; an empty list means it is valid."""
     if not _BRANCH_RE.match(branch):
-        return ["does not match <login>/issue-<N>[-<words>], no spaces"]
-    login, rest = branch.split("/", 1)
+        return ["does not match [<login>/]issue-<N>[-<words>], no spaces"]
+    login, _, rest = branch.rpartition("/")  # login is "" when the name has none
     issue_part = _ISSUE_PART_RE.match(rest).group(0)
     words = rest[len(issue_part) :]
     errors = []
-    bare = f"{login}/{issue_part}"
-    if len(bare) > _MAX_LENGTH:
+    if not login:
+        if len(branch) > _MAX_LENGTH:
+            errors.append(f"{len(branch)} characters, at most {_MAX_LENGTH}")
+    elif words and len(branch) > _MAX_LENGTH:
         errors.append(
-            f"stop: even {bare} is over {_MAX_LENGTH} characters; "
-            "create nothing and ask the owner"
+            f"{len(branch)} characters, at most {_MAX_LENGTH}: drop the words"
         )
-    elif len(branch) > _MAX_LENGTH:
-        errors.append(f"{len(branch)} characters, at most {_MAX_LENGTH}")
+    # A name with a login and no words is never an error for its length: when even
+    # <login>/issue-<N> is over the limit the rule keeps it and goes on.
     if _NUMBER_RUN.search(words):
         errors.append("the words hold a run of 2 to 4 digits that cleanup reads")
-    if _NUMBER_RUN.search(login):
+    if login and _NUMBER_RUN.search(login):
         errors.append(
-            "the login holds a run of 2 to 4 digits that cleanup reads as an issue"
+            "the login holds a run of 2 to 4 digits that cleanup reads as an issue: "
+            "leave the login out and use issue-<N>-<words>"
         )
     return errors
 
@@ -68,6 +72,10 @@
         "Ab-c/issue-5",  # 12
         "a/issue-1-v12345",  # 16; a 5-digit run is not a 2 to 4 digit run
         "dev1/issue-289",  # 14; a 1-digit run in the login is not read by cleanup
+        "issue-289-wtrule",  # 16; no login: a login with a digit run leaves it out
+        "issue-289",  # 9
+        "averylonglogin/issue-289",  # 24
+        "abcdefghijklmno/issue-289",  # 25; the bare form over 24 is kept
     ],
 )
 def test_checker_accepts(branch):
@@ -88,16 +96,21 @@
         "-a/issue-1",  # a login that starts with a hyphen
         "a/issue-1-x/y",  # a second slash
         "dev42/issue-289",  # a 2 digit run in the login: cleanup also reads issue 42
+        "dev42/issue-289-words",  # the same, with words
+        "issue-289-py312",  # a 3 digit run in the words, no login
+        "issue-0289",  # leading zero, no login
+        "averylonglogin1/issue-289-x",  # 27; the words do not fit
     ],
 )
 def test_checker_rejects(branch):
     assert branch_errors(branch)
 
 
-def test_bare_form_over_the_limit_is_a_stop():
-    errors = branch_errors("averylonglogin1/issue-289")  # 25 characters
-    assert errors
-    assert "stop" in " ".join(errors)
+def test_bare_form_over_the_limit_is_kept():
+    for branch in ("averylonglogin1/issue-289", "abcdefghijklmno/issue-289"):
+        assert len(branch) > _MAX_LENGTH  # 25 characters
+        assert branch_errors(branch) == []  # never stop on it
+    assert not any("stop" in e for e in branch_errors("averylonglogin1/issue-289-x"))
 
 
 @pytest.mark.parametrize(
@@ -116,10 +129,12 @@
     bare = f"{login}/issue-{'1' * digits}"
     # The bare form overflows exactly when the login and the digits make 18.
     assert (len(bare) > _MAX_LENGTH) == (len(login) + digits >= 18)
-    assert any("stop" in e for e in branch_errors(bare)) == (len(bare) > _MAX_LENGTH)
+    assert branch_errors(bare) == []  # the bare form is always accepted
     if expected >= 1:
         assert branch_errors(f"{bare}-{'b' * expected}") == []
         assert branch_errors(f"{bare}-{'b' * (expected + 1)}")
+    else:
+        assert branch_errors(f"{bare}-b")  # no room for words: drop them
 
 
 _SECTION_HEADING = "## Worktrees and branches"


Codegraph context
index_state: fresh
checked_at: 2026-11-26T17:40:41Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-289
call codegraph only when index_state: fresh, never to widen scope

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