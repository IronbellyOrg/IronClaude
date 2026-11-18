1078cb0cbdf5ae0366dd98f8f4f990d86136a6fd
Review one task for spec compliance.

Task brief: ## Task 2: Update the chain tests for the new simple feature row
Depends on: Task 1

In `tests/skills/test_issue_protocol.py`, change `test_brainstorm_steps_have_no_handoff_and_use_default_models` so it expects 2 brainstorm steps across the 6 rows (it asserts 3 today). Add a new test next to it that finds the `Feature, simple` row of `src/superclaude/skills/sc-issue-protocol/refs/chains.md` and asserts it has no `/sc:brainstorm`, contains `/sc:workflow <S> --depth quick --handoff none` and contains `/sc:implement <plan path printed by step 1>`. Also change `test_issue_chains_use_the_default_brainstorm_models` in `tests/skills/test_model_alias_policy.py` (lines 191-196), which asserts at least 3 `/sc:brainstorm` spans in `chains.md`, to assert at least 2; keep its check that no span carries `--models`.
Acceptance criteria (ids):
T2.AC1: `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_model_alias_policy.py -v` passes.
T2.AC2: Restoring the old brainstorm step into the row makes the new test and the 2-step count fail.
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
Start sha: 1078cb0cbdf5ae0366dd98f8f4f990d86136a6fd
Diff against the start snapshot: diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index f8e89060f..fa3041a32 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -659,7 +659,7 @@ def test_brainstorm_steps_have_no_handoff_and_use_default_models():
         for s in _COMMAND_SPAN.findall(row)
         if s.startswith("/sc:brainstorm")
     ]
-    assert len(steps) == 3
+    assert len(steps) == 2
     for step in steps:
         assert "--handoff tasklist" not in step and "--handoff design" not in step
         assert "--models" not in step
@@ -667,6 +667,17 @@ def test_brainstorm_steps_have_no_handoff_and_use_default_models():
     assert "--handoff tasklist" not in text and "--handoff design" not in text
 
 
+def test_feature_simple_row_plans_directly_from_the_summary():
+    row = next(
+        r
+        for r in chain_rows(_text(REFS / "chains.md"))
+        if r.startswith("| Feature, simple |")
+    )
+    assert "/sc:brainstorm" not in row
+    assert "`/sc:workflow <S> --depth quick --handoff none`" in row
+    assert "`/sc:implement <plan path printed by step 1>`" in row
+
+
 # --- fork safety (design section 13, section 20 item 4) ---------------------------
 
 
diff --git a/tests/skills/test_model_alias_policy.py b/tests/skills/test_model_alias_policy.py
index b77a3cace..94388f5d8 100644
--- a/tests/skills/test_model_alias_policy.py
+++ b/tests/skills/test_model_alias_policy.py
@@ -192,7 +192,7 @@ def test_issue_chains_use_the_default_brainstorm_models() -> None:
     """The /sc:issue chains pass no --models flag to /sc:brainstorm."""
     text = (SRC / "skills/sc-issue-protocol/refs/chains.md").read_text(encoding="utf-8")
     steps = re.findall(r"`(/sc:brainstorm[^`]*)`", text)
-    assert len(steps) >= 3
+    assert len(steps) >= 2
     assert [step for step in steps if "--models" in step] == []
 
 


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
