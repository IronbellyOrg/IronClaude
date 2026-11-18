90ed0977eb8afec0efa777cc9608000c3ced6941
Review one task for spec compliance.

Task brief: ## Task 4: Pin the picked default in the command tests
Depends on: Task 3

In `tests/commands/test_issue_command.py`: in `test_option_defaults` (line 113) change the `--pipeline` default assertion from `` "`full`" `` to the new cell text of Task 3 (the `--pipeline` row default cell, "`full` or `worktree`, picked from the issue"); extend `test_default_level_is_for_a_person_and_the_watcher_stays_explicit` (line 182) with assertions that the command text says an explicit `--pipeline` wins and that it points to `refs/claim.md` for the rule, and that the text "even though `full` is the default" is gone from the command file; keep `test_submit_rule_stops_a_bare_submit_and_keeps_its_message` (line 188) unchanged. Do not edit `tests/issue_watch/`.
Acceptance criteria (ids):
T4.AC1: `uv run pytest tests/commands/test_issue_command.py tests/issue_watch/test_launch.py tests/issue_watch/test_security_invariants.py -v` passes with `tests/issue_watch/` unchanged (`git status --short tests/issue_watch` prints nothing).
T4.AC2: Changing the default cell in `src/superclaude/commands/issue.md` back to `` `full` `` makes `test_option_defaults` fail, removing "always passes `--pipeline none`" makes the watcher test fail, and putting ", even though `full` is the default" back into `issue.md` makes the same test fail.
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
Start sha: 90ed0977eb8afec0efa777cc9608000c3ced6941
Diff against the start snapshot: diff --git a/tests/commands/test_issue_command.py b/tests/commands/test_issue_command.py
index 37df9d668..14632a537 100644
--- a/tests/commands/test_issue_command.py
+++ b/tests/commands/test_issue_command.py
@@ -110,7 +110,7 @@ def test_option_defaults():
         rows[f][1] == "create" for f in ("--create", "--depth", "--mode", "--type")
     )
     assert rows["--pipeline"][1] == rows["--submit"][1] == "claim"
-    assert rows["--pipeline"][2] == "`full`"
+    assert rows["--pipeline"][2] == "`full` or `worktree`, picked from the issue"
     assert rows["--submit"][2] == "off"
     assert rows["--submit"][3] == "no value"
     assert "`--pipeline full`" in rows["--submit"][4]
@@ -183,6 +183,9 @@ def test_default_level_is_for_a_person_and_the_watcher_stays_explicit():
     text = _text()
     assert "always passes `--pipeline none`" in text
     assert "/sc:issue --claim 302 --pipeline worktree" in text.splitlines()
+    assert "an explicit `--pipeline` always wins" in text
+    assert "`refs/claim.md`" in text
+    assert "even though `full` is the default" not in text
 
 
 def test_submit_rule_stops_a_bare_submit_and_keeps_its_message():


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
