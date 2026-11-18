b8f2397c3fab910cae9f06809b030195f0dc2d57
Review one task for spec compliance.

Task brief: ## Task 5: Pin the new default in the command tests
Depends on: Task 3

In `tests/commands/test_issue_command.py`, change `test_option_defaults` so `rows["--pipeline"][2] == "`full`"`. Add a test that the command text says the issue watcher always passes `--pipeline none` and that `/sc:issue --claim 302 --pipeline worktree` is an example line. Add a test that the `E-SUBMIT-NEEDS-FULL` rule text says a `--submit` with no `--pipeline` stops (it contains "no `--pipeline`") and still carries the quoted message `"--submit needs --pipeline full"`. Do not edit `tests/issue_watch/test_launch.py`: its tests at lines 929-939 already assert `build_claim_prompt(9)` returns `/sc:issue --claim 9 --pipeline none` and that the bare form no longer matches `PROMPT_PATTERN`.
Acceptance criteria (ids):
T5.AC1: `uv run pytest tests/commands/test_issue_command.py tests/issue_watch/test_launch.py tests/issue_watch/test_security_invariants.py -v` passes with `tests/issue_watch/` unchanged.
T5.AC2: Setting the Options table default back to `` `worktree` `` makes `test_option_defaults` fail.
T5.AC3: Removing "no `--pipeline`" from the stop rule makes the new submit-rule test fail.
Global constraints: ## Constraints
- Edit only source files: `src/superclaude/...`, `tests/...`, `docs/...` and the one mirror file `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Never edit or stage anything under `.claude/`; Task 10 regenerates those copies with `make sync-dev`.
- The default level applies to a bare `--claim`. The issue watcher always passes `--pipeline none` (`build_claim_prompt` in `src/superclaude/cli/issue_watch/launch.py`, pinned by `tests/issue_watch/test_launch.py`). Do not edit either file and do not add any human-versus-agent detection.
- The default level does not authorize a commit, a push or a pull request: `E-SUBMIT-NEEDS-FULL` keeps its meaning, so a `--submit` with no `--pipeline` still stops and `--submit` needs an explicit `--pipeline full` (the design record `docs/designs/sc-issue-claim-pipeline-flag.md` line 85 already says so).
- No file under `src/superclaude/skills/sc-issue-protocol/` and not `src/superclaude/commands/issue.md` may contain the text `src/superclaude/` (`tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files` and `tests/commands/test_issue_command.py::test_no_source_tree_path` forbid it): in those files cite code by file name, never by its `src/superclaude/` path.
- New lines in command and skill files must not contain `git add`, `git commit`, `git push`, `git merge`, `gh pr` or `gh api`: `tests/skills/test_worker_contract.py` audits those verbs line by line.
- Leave the ship-gate sentences (OB-H1, OB-H2, OB-H3) and the `--pipeline none` coordinator-handoff paragraph exactly as written. The worktree `claim-handoff-planb` edits the same files (`issue.md`, `SKILL.md`, `refs/claim.md`, `HOW-WE-WORK.md`), so keep every edit narrow and rebase onto `origin/master` before any pull request.
- Out of scope: `/tech-research`, `/task-builder` and `/task` handling, the complex bug row, model tiers, `orca_worktree.py`, every other chain row, and the command version (it stays 1.1.0, which `tests/commands/test_issue_command.py` pins).
- Also out of scope, recorded on purpose: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` lines 17-19 (the coordinator path keeps its brainstorm step for simple work); the owner-run bare launch prompts in `docs/designs/issue-watcher-setup.md` lines 616-619 (a launch with them now starts at `full`; update them before reuse if a claim-only capture is wanted); and the dated records `docs/designs/issue-watcher.md` lines 41 and 48 and `docs/designs/issue-watcher-setup.md` line 575.
- Known risk, not fixed here: a person's bare `/sc:issue --claim <N>` on an issue that a coordinator already owns reuses its worktree and starts a second agent, now at `full`, because only the claim's own launch step writes the launch record (`cmd_pending` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` writes only a pending record). Do not claim such an issue without `--pipeline none`.
Start sha: b8f2397c3fab910cae9f06809b030195f0dc2d57
Diff against the start snapshot: diff --git a/tests/commands/test_issue_command.py b/tests/commands/test_issue_command.py
index 7604e08d6..37df9d668 100644
--- a/tests/commands/test_issue_command.py
+++ b/tests/commands/test_issue_command.py
@@ -110,7 +110,7 @@ def test_option_defaults():
         rows[f][1] == "create" for f in ("--create", "--depth", "--mode", "--type")
     )
     assert rows["--pipeline"][1] == rows["--submit"][1] == "claim"
-    assert rows["--pipeline"][2] == "`worktree`"
+    assert rows["--pipeline"][2] == "`full`"
     assert rows["--submit"][2] == "off"
     assert rows["--submit"][3] == "no value"
     assert "`--pipeline full`" in rows["--submit"][4]
@@ -179,6 +179,21 @@ def test_claim_outputs_and_examples_cover_the_new_flags():
     assert "E-ORCA-REQUIRED" in text
 
 
+def test_default_level_is_for_a_person_and_the_watcher_stays_explicit():
+    text = _text()
+    assert "always passes `--pipeline none`" in text
+    assert "/sc:issue --claim 302 --pipeline worktree" in text.splitlines()
+
+
+def test_submit_rule_stops_a_bare_submit_and_keeps_its_message():
+    text = _text()
+    stops = text.index("## STOP rules")
+    rules = text[stops : text.index("\n## ", stops + 1)]
+    rule = next(ln for ln in rules.splitlines() if "E-SUBMIT-NEEDS-FULL" in ln)
+    assert "no `--pipeline`" in rule
+    assert '"--submit needs --pipeline full"' in rule
+
+
 def test_activation_names_the_skill():
     activation = _text().split("## Activation", 1)[1]
     assert "> Skill sc:issue-protocol" in activation


Codegraph context
index_state: fresh
checked_at: 2026-11-18T05:09:43Z
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
