a9adfbafe7ed5a0802280a437f23b812d84c51ab
Review one task for spec compliance.

Task brief: ## Task 5: Pin the rule in the protocol tests
Depends on: Task 1, Task 2

In `tests/skills/test_issue_protocol.py`: in `test_default_level_is_full_and_only_worktree_waits_for_a_person` (line 681) replace the assertion on "or `full` when the flag was omitted" with assertions that `_wave(claim, 5)` contains the new step's words (the `Level:` line formats `(explicit)` and `(default: `, the unreadable case, and the 16-hour line), and change the check on `SKILL.md` to the new line 17 wording; keep its checks on Wave 8 ("`<L>` is the same level as in Wave 5."), the next-steps template (now "at level `full`"), and "run the printed implement command" appearing only in the `worktree` sentence of the `launched` item. Add one new test, `test_default_level_rule_is_bug_full_complex_feature_worktree`, that reads Wave 5 and asserts: the new step sits after the `next-steps.md` step and before the plan-boundary step (compare `index` of the three step phrases); it names `Type`, `Complexity` and `Effort estimate` of `issue-summary.md`; bug gives `full`; a simple or medium feature of 16 hours or less gives `full`; a complex feature or over 16 hours gives `worktree`; unreadable gives `worktree`; an explicit `--pipeline` wins. The same test also asserts that the unreadable sentence comes before the bug sentence (compare their `index` in Wave 5), and that the final-output `launched` item states the `Level:` line, the stored level for `already_launched` and no `Level:` line for a failed worktree or launch (pin one phrase for each of the three).
Acceptance criteria (ids):
T5.AC1: `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_model_alias_policy.py tests/skills/test_worker_contract.py -v` passes.
T5.AC2: Removing the unreadable-gives-`worktree` sentence from Wave 5 of `refs/claim.md` makes the new test fail, moving the new step after the plan-boundary step makes it fail, swapping the unreadable sentence below the bug sentence makes it fail, and deleting the `Level:` instruction from the final-output `launched` item makes it fail.
T5.AC3: `tests/skills/test_issue_protocol.py` still pins the ten return-contract fields and `pipeline_level` is not renamed.
Global constraints: ## Constraints
- The rule is authored once, in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (Wave 5). `issue.md`, `SKILL.md`, the next-steps template, the docs and the routing guide state the outcome in one sentence, which may name the 16-hour line once per file, and do not restate the order of the rule's checks or its unreadable fallback as a second rule; the full rule lives only in `refs/claim.md`.
- The rule reads three lines of `<D>/issue-summary.md`, which Wave 4 already writes from `templates/issue-summary.md`: `Type`, `Complexity` and `Effort estimate`. A value that is missing or not one of the allowed words counts as unreadable and gives `worktree`.
- No new return-contract field. The claim return contract keeps its ten fields (a test pins them); `pipeline_level` carries the level actually used.
- An `already_launched` re-claim still reports the stored level from the `launch` entry of `worktree.json` or its mirror file; that path is not changed.
- `--submit` still stops with `E-SUBMIT-NEEDS-FULL` when `--pipeline full` is not written out, including when `--pipeline` is omitted. The rule text of that STOP and its quoted message "--submit needs --pipeline full" stay as they are.
- Do not edit `tests/issue_watch/`, `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the launch-level guard text, or the ship-gate and OB-H paragraphs. The issue watcher keeps passing an explicit `--pipeline none` and never reaches the rule.
- Text added to installed skill, command and core files names no `src/superclaude/` path and no git or gh verb that `tests/skills/test_worker_contract.py` audits in new lines.
- Design and user-guide records keep their original text: this change only adds dated "Amended 2026-11-18" notes, and a note on a table row goes inside that row's last cell so the table stays a table.
- The new text is prose that a model follows, so the tests pin its wording and order, not an executable rule. Each task says which words are pinned.
- Never `git add` or `git add -f` any path under `.claude/`; `make sync-dev` writes those copies and they stay unstaged. `claim-handoff-planb` edits some of the same files, so rebase onto `origin/master` before any PR.
Start sha: a9adfbafe7ed5a0802280a437f23b812d84c51ab
Diff against the start snapshot: diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index 2e9f860cb..6f9979562 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -679,11 +679,15 @@ def test_feature_simple_row_plans_directly_from_the_summary():
 
 
 def test_default_level_is_full_and_only_worktree_waits_for_a_person():
-    assert "`full` (default) also implements" in _text(SKILL)
+    skill = _text(SKILL)
+    assert "`full` also implements without a commit or a push" in skill
+    assert "`full` (default)" not in skill
     claim = _text(REFS / "claim.md")
-    assert "or `full` when the flag was omitted" in _wave(claim, 5)
+    wave5 = _wave(claim, 5)
+    assert "(explicit)" in wave5 and "(default: " in wave5 and "16 hours" in wave5
     assert "`<L>` is the same level as in Wave 5." in _wave(claim, 8)
-    assert "default level `full`" in _text(TEMPLATES / "next-steps.md")
+    next_steps = _text(TEMPLATES / "next-steps.md")
+    assert "at level `full`" in next_steps and "default level `full`" not in next_steps
     launched = next(ln for ln in claim.splitlines() if "- `launched`:" in ln)
     before, rest = launched.split("For `worktree`:", 1)
     worktree, full = rest.split("For `full`:", 1)
@@ -691,6 +695,38 @@ def test_default_level_is_full_and_only_worktree_waits_for_a_person():
     assert "run the printed implement command" not in before + full
 
 
+def test_default_level_rule_is_bug_full_complex_feature_worktree():
+    claim = _text(REFS / "claim.md")
+    wave5 = _wave(claim, 5)
+    next_steps = wave5.index("Write `<D>/next-steps.md`")
+    start = wave5.index("Resolve the level `<L>`")
+    boundary = wave5.index("Set the plan boundary")
+    assert next_steps < start < boundary
+    rule = wave5[start:boundary]
+    for token in ("`Type`", "`Complexity`", "`Effort estimate`", "issue-summary.md"):
+        assert token in rule
+    assert rule.index("cannot be read") < rule.index("`full` for a bug")
+    assert "`<L>` is `worktree` and no other check runs" in rule
+    assert "also gets `worktree`" in rule
+    assert (
+        "`full` for a feature whose complexity is `simple` or `medium` and whose "
+        "effort is 16 hours or less"
+    ) in rule
+    assert (
+        "`worktree` for a feature whose complexity is `complex` or whose effort "
+        "is over 16 hours"
+    ) in rule
+    assert "an explicit value always wins" in rule
+    lines = claim.splitlines()
+    launched = next(ln for ln in lines if "- `launched`:" in ln)
+    assert "Print the `Level:` line of Wave 5 with this result." in launched
+    already = next(ln for ln in lines if "- `already_launched`:" in ln)
+    assert "`Level: <stored level> (stored)`" in already
+    assert "the stored level wins" in already
+    failed = next(ln for ln in lines if ln.lstrip().startswith("- Failed worktree"))
+    assert "print no `Level:` line" in failed
+
+
 # --- fork safety (design section 13, section 20 item 4) ---------------------------
 
 


Codegraph context
index_state: fresh
checked_at: 2026-11-18T06:18:32Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the task changes Markdown or test text, not code symbols; no dependents outside the touched set were listed.

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
