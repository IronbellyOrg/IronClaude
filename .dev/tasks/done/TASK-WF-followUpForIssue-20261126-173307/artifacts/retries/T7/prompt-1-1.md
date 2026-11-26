e25122a5f1774e71136a75f91927e935041b744c
Review one task for spec compliance.

Task brief: ## Task 7: Pin the new CLAUDE.md examples in tests/core/test_claude_md_worktree_rule.py

Depends on: Task 4

Add two tests to `tests/core/test_claude_md_worktree_rule.py` using its existing `_section()`: `test_names_follow_the_guide_pattern` asserts the section contains the `Names:` bullet text `<login>/issue-<N>[-<words>]`, `at most 24 characters`, `no spaces`, `--name issue-<N>-<words>` and the words `Worktrees and branches`; `test_examples_use_issue_names` asserts the section no longer contains `pm-agent` or `name:integration`, that its `orca worktree create` example line contains `--name issue-` and `--agent`, and that the `orca worktree rm` example line names an `issue-` worktree. The three existing tests stay unchanged.

Acceptance criteria:
T7.AC1: `uv run pytest tests/core/test_claude_md_worktree_rule.py -q` passes with five tests.
T7.AC2: Reverting Task 4 on a scratch copy of the section text (re-inserting `pm-agent`) makes `test_examples_use_issue_names` fail.
T7.AC3: `uv run ruff check tests/core/test_claude_md_worktree_rule.py` and `uv run ruff format --check tests/core/test_claude_md_worktree_rule.py` pass.
Global constraints: ## Constraints

- Test, guide, deck and CLAUDE.md edits only; no production code (nothing under `src/superclaude/cli/`, `scripts/`, hooks or skills changes).
- Never edit or stage anything under `.claude/`. `.dev/tasks/` stays staged.
- ASCII only in the guide section; keep every existing rule that the six answers do not change, in the owner's wording where the source quotes it.
- Decision recorded here: answer 2 says "never stop", so a name whose bare form `<login>/issue-<N>` is over 24 characters is kept and the work goes on. The sentence "create nothing and ask the owner", its key phrase and the "stop" test are replaced. A name that carries words over 24 characters is still an error: drop the words.
- Not in scope (MB-2): reading the digit-run pattern from scripts/worktree_cleanup.py. The user withdrew that item; the hand-copied _NUMBER_RUN of tests/core/test_how_we_work_worktree_policy.py stays as it is.
- The branch `clayphi/issue-289-rest` was created in the reused worktree with `git switch -c` on the owner's order; the guide's "never switch branches in a worktree" line is left as it is.
Start sha: e25122a5f1774e71136a75f91927e935041b744c
Diff against the start snapshot: --- a/tests/core/test_claude_md_worktree_rule.py
+++ b/tests/core/test_claude_md_worktree_rule.py
@@ -5,12 +5,29 @@
 CLAUDE_MD = Path(__file__).resolve().parents[2] / "CLAUDE.md"
 
 
-def _section() -> str:
-    text = CLAUDE_MD.read_text()
+def _section(text: str | None = None) -> str:
+    text = CLAUDE_MD.read_text() if text is None else text
     start = text.index("### Parallel Development with Git Worktrees")
     return text[start:].split("\n## ", 1)[0]
 
 
+def _example_errors(section: str) -> list[str]:
+    """Reasons the worktree examples in a section are stale; empty means fine."""
+    errors = [
+        f"stale name {s!r}" for s in ("pm-agent", "name:integration") if s in section
+    ]
+    lines = section.splitlines()
+    create = [ln for ln in lines if ln.startswith("orca worktree create")]
+    if not create or not all(
+        "--name issue-" in ln and "--agent" in ln for ln in create
+    ):
+        errors.append("create example needs --name issue-<N>... and --agent")
+    remove = [ln for ln in lines if ln.startswith("orca worktree rm")]
+    if not remove or not all("name:issue-" in ln for ln in remove):
+        errors.append("rm example must name an issue- worktree")
+    return errors
+
+
 def test_every_worktree_gets_an_agent_and_its_creator_owns_it() -> None:
     section = _section()
     assert "--agent claude" in section
@@ -31,6 +48,26 @@
     assert all("--agent" in ln for ln in lines), lines
 
 
+def test_names_follow_the_guide_pattern() -> None:
+    section = _section()
+    for phrase in (
+        "Worktrees and branches",
+        "<login>/issue-<N>[-<words>]",
+        "at most 24 characters",
+        "no spaces",
+        "--name issue-<N>-<words>",
+    ):
+        assert phrase in section, phrase
+
+
+def test_examples_use_issue_names() -> None:
+    assert _example_errors(_section()) == []
+    # The check itself fails on the old examples, so it cannot pass by accident.
+    stale = _section() + "\norca worktree create --name pm-agent --agent claude\n"
+    assert _example_errors(stale)
+    assert _example_errors(_section().replace("name:issue-", "name:integration"))
+
+
 def test_existing_worktree_rules_are_kept() -> None:
     section = _section()
     assert "every project worktree is created through Orca" in section


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