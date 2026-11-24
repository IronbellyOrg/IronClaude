083d7a4b43ae59d307ace0b6e403ba867e3ecd28
Review one task for spec compliance.

Task brief: ## Task 5: Add one test that the four base-branch statements agree

Depends on: Task 1, Task 3, Task 4

Add `tests/core/test_default_branch_agreement.py` with one test. It reads the base branch once per source: the fallback `--base <name>` token of the `gh pr create` line in `CLAUDE.md`, the `origin/<name>` in the "Branch rebased onto" line of `.github/PULL_REQUEST_TEMPLATE.md`, `config._DEFAULT_BASE_BRANCH` from `superclaude.cli.reflect.config`, and that `refs/heads/<name>` is in the `L2_PROTECTED=(...)` array of `src/superclaude/hooks/scripts/launch-level-pre-push.sh`. It asserts the first three are equal and the fourth is present, with a message naming the disagreeing file.

Acceptance criteria (ids):
T5.AC1: The test passes on the finished tree and fails (checked by temporarily changing any one of the four sources) when one of them names a different branch.
T5.AC2: Full `uv run pytest` and `make lint` pass (any failure is reported honestly in `.dev/issues/769/default-branch-result.md`), and `git status` shows no staged `.claude/` mirror.
Global constraints: - One pull request, base `integration`, branch `fix/default-branch-integration`, opened only through `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`. Never merge, never touch SuperClaude-Org, no Orca link flags, no model flag, never Opus.
- Edit only `src/superclaude/**`, `tests/**`, `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (a committed byte-identical mirror with no generator: `scripts/build_superclaude_plugin.py` writes `dist/` only) and the two root files `CLAUDE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
- Do not touch `docs/generated`, `docs/testing`, the `/sc:impact` and `/sc:auggie-review` diff examples, release tooling (`/sc:post-release`, `release-procedure.md`), or any text that says master is the production branch. Change no ABSOLUTE RULE wording in `CLAUDE.md` other than branch names.
- Never stage `.claude/` mirrors (only `.claude/settings.json` is tracked); `.dev/tasks` is staged. Commit only on the feature branch with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- Follow-ups to list in the PR body, not fix here: the L1 command guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 59 text, line 736 `master | main`) still classifies only master and main as PROTECTED (the L2 hook is the backstop); release tooling that assumes master.
Start sha: 083d7a4b43ae59d307ace0b6e403ba867e3ecd28
Diff against the start snapshot: diff --git a/tests/core/test_default_branch_agreement.py b/tests/core/test_default_branch_agreement.py
new file mode 100644
index 000000000..c3e896af0
--- /dev/null
+++ b/tests/core/test_default_branch_agreement.py
@@ -0,0 +1,29 @@
+"""CLAUDE.md, the PR template, the L2 pre-push hook and the reflect default must name one base branch."""
+
+import re
+from pathlib import Path
+
+from superclaude.cli.reflect.config import _DEFAULT_BASE_BRANCH
+
+ROOT = Path(__file__).resolve().parents[2]
+
+
+def _find(path: str, pattern: str) -> str:
+    match = re.search(pattern, (ROOT / path).read_text(), re.M)
+    assert match, f"{path}: no match for {pattern!r}"
+    return match.group(1)
+
+
+def test_base_branch_is_the_same_everywhere() -> None:
+    claude_md = _find("CLAUDE.md", r"^gh pr create .*--base (\S+) ")
+    template = _find(
+        ".github/PULL_REQUEST_TEMPLATE.md", r"rebased onto `origin/([^`]+)`"
+    )
+    assert claude_md == template == _DEFAULT_BASE_BRANCH, (
+        f"CLAUDE.md={claude_md} PR template={template} reflect={_DEFAULT_BASE_BRANCH}"
+    )
+    hook = _find(
+        "src/superclaude/hooks/scripts/launch-level-pre-push.sh",
+        r"^L2_PROTECTED=\((.*)\)$",
+    )
+    assert f"refs/heads/{_DEFAULT_BASE_BRANCH}" in hook.split(), hook

Codegraph context
index_state: absent
checked_at: n/a
worktree_root: /home/coder/workspaces/worktrees/IronClaude/fix-default-branch-integration
projectPath: n/a
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor.

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
