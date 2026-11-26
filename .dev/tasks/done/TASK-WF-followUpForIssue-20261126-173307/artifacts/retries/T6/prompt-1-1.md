b948d51126c7ace3f26482b8fae6c64eb66548cf
Review one task for spec compliance.

Task brief: ## Task 6: Update the key phrases, the word cap and the deck assertions in tests/core/test_how_we_work_worktree_policy.py

Depends on: Task 1, Task 3, Task 5

Edit the section-pinning part of `tests/core/test_how_we_work_worktree_policy.py` (from `_KEY_PHRASES` to the end of the file). (a) In `_KEY_PHRASES` remove `create nothing and ask the owner` and add the phrases of Task 1 that state the new rules, each of which occurs exactly once in the section: `Neither refuses an issue that already has a worktree`, `iteration start check asks the owner first`, `skips only the already-claimed check`, `match on repository, issue and branch`, `drop them and keep`, `never stop on it`, `is left out: use`, `keeps the launcher's`, `own `.dev/` notes`, `issue 881`. No phrase may contain another phrase (the deletion test removes one phrase and expects only it to be reported). (b) Change the 400-word cap in `test_section_is_at_most_400_words` (rename to `test_section_is_within_the_word_cap`) to the measured word count of the new section rounded up to the next multiple of 10, no higher. (c) Update `test_deck_card_is_replaced_and_neighbours_untouched` to assert the new slide: `Contributing and worktrees` present, `Worktree and branch protocol` and `Contributing rules` cards present, `clayphi/issue-289-wtrule` present, the old strings `Contributing, and one open topic`, `still open in its own issue`, `issues #289 and #290`, `how they are named is being worked out` and `issues/289` all absent, the exact new introduction paragraph text of Task 3 present (MB-1), the words `still open` absent between `id="s12"` and `id="s13"` in the deck so that an introduction that still calls the topic open fails (MB-1), and the footer regex `Built from HOW-WE-WORK\.md at commit [0-9a-f]{7,40}\b` present. (d) Keep the mirror, pointer, backticked-example and ASCII tests as they are.

Acceptance criteria:
T6.AC1: `uv run pytest tests/core/test_how_we_work_worktree_policy.py -q` passes, with `test_section_states_each_rule` and `test_deletion_is_detected` collected for every phrase of the new list (the new phrases included) and no phrase reported twice.
T6.AC2: Deleting any one new phrase from a copy of the section makes the suite's `_missing_phrases` report exactly that phrase (the existing parametrized deletion test shows it).
T6.AC3: `uv run pytest tests/core tests/docs tests/commands/test_worktrees_command.py tests/worktree_cleanup -q` passes, `make lint` passes, and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py tests/core/test_claude_md_worktree_rule.py` passes.
Global constraints: ## Constraints

- Test, guide, deck and CLAUDE.md edits only; no production code (nothing under `src/superclaude/cli/`, `scripts/`, hooks or skills changes).
- Never edit or stage anything under `.claude/`. `.dev/tasks/` stays staged.
- ASCII only in the guide section; keep every existing rule that the six answers do not change, in the owner's wording where the source quotes it.
- Decision recorded here: answer 2 says "never stop", so a name whose bare form `<login>/issue-<N>` is over 24 characters is kept and the work goes on. The sentence "create nothing and ask the owner", its key phrase and the "stop" test are replaced. A name that carries words over 24 characters is still an error: drop the words.
- Not in scope (MB-2): reading the digit-run pattern from scripts/worktree_cleanup.py. The user withdrew that item; the hand-copied _NUMBER_RUN of tests/core/test_how_we_work_worktree_policy.py stays as it is.
- The branch `clayphi/issue-289-rest` was created in the reused worktree with `git switch -c` on the owner's order; the guide's "never switch branches in a worktree" line is left as it is.
Start sha: b948d51126c7ace3f26482b8fae6c64eb66548cf
Diff against the start snapshot: --- a/tests/core/test_how_we_work_worktree_policy.py
+++ b/tests/core/test_how_we_work_worktree_policy.py
@@ -155,7 +155,6 @@
     "at most 24 characters",
     "no spaces",
     "no run of 2 to 4 digits",
-    "create nothing and ask the owner",
     "Lessons comment",
     "pins the worktree",
     "checks that comment first",
@@ -169,6 +168,16 @@
     "the PR that counts",
     "the watcher claims by itself",
     "after the first session has stopped",
+    "Neither refuses an issue that already has a worktree",
+    "iteration start check asks the owner first",
+    "skips only the already-claimed check",
+    "match on repository, issue and branch",
+    "drop them and keep",
+    "never stop on it",
+    "is left out: use",
+    "keeps the launcher's",
+    "own `.dev/` notes",
+    "issue 881",
 ]
 
 
@@ -198,8 +207,8 @@
     assert "<!--" not in section
 
 
-def test_section_is_at_most_400_words():
-    assert len(_section().split()) <= 400
+def test_section_is_within_the_word_cap():
+    assert len(_section().split()) <= 500
 
 
 def test_section_is_pure_ascii_and_has_no_banned_phrase():
@@ -244,11 +253,29 @@
     assert "item 4 of issue 289" not in rows[0]
 
 
+_S12_INTRO = (
+    "<p>Both rules are settled. The worktree rule is the left card and the guide "
+    'section "Worktrees and branches"; the contributing rule is the right card, '
+    "with its history in issue #290. If a case is not covered, ask your lead.</p>"
+)
+
+
 def test_deck_card_is_replaced_and_neighbours_untouched():
     deck = _DECK.read_text(encoding="utf-8")
+    assert "Contributing and worktrees" in deck
     assert "Worktree and branch protocol" in deck
     assert "clayphi/issue-289-wtrule" in deck
-    assert "how they are named is being worked out" not in deck
-    assert "issues/289" not in deck
+    for old in (
+        "Contributing, and one open topic",
+        "still open in its own issue",
+        "issues #289 and #290",
+        "how they are named is being worked out",
+        "issues/289",
+    ):
+        assert old not in deck, old
+    assert _S12_INTRO in deck
+    # No call that the worktree topic is open anywhere on slide 12.
+    slide_12 = deck[deck.index('id="s12"') : deck.index('id="s13"')]
+    assert "still open" not in slide_12
     assert "Contributing rules" in deck
     assert re.search(r"Built from HOW-WE-WORK\.md at commit [0-9a-f]{7,40}\b", deck)


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