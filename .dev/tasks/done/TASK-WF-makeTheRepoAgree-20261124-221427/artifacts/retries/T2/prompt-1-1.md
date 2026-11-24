32b0e98738e39a2ef10629d21ef15a37e01567c5
Review one task for spec compliance.

Task brief: ## Task 2: Prove a governed push to integration is refused and a feature-branch push is allowed

Depends on: Task 1

In `tests/hooks/test_launch_level_pre_push.py` (the real L2 hook tests; `tests/hooks/test_launch_level_guard.py` covers the separate L1 command guard and is not edited) change `BRANCHES = ["main", "master"]` (line 49) to include `"integration"` so every parametrized actor and malformed-stream test also covers it, and make sure a governed push to `refs/heads/integration` asserts `protected(...)` while a governed push to a feature branch such as `refs/heads/feature/x` asserts `allowed(...)` (add one small test only if no existing test already pushes a non-protected ref for a governed actor).

Acceptance criteria (ids):
T2.AC1: A governed actor pushing `HEAD:integration` exits non-zero with the `L2-PROTECTED ... refs/heads/integration` line, and a governed actor pushing a feature branch exits 0.
T2.AC2: `uv run pytest tests/hooks -q` passes; reverting line 17 of the hook makes the new integration cases fail.
Global constraints: - One pull request, base `integration`, branch `fix/default-branch-integration`, opened only through `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`. Never merge, never touch SuperClaude-Org, no Orca link flags, no model flag, never Opus.
- Edit only `src/superclaude/**`, `tests/**`, `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (a committed byte-identical mirror with no generator: `scripts/build_superclaude_plugin.py` writes `dist/` only) and the two root files `CLAUDE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
- Do not touch `docs/generated`, `docs/testing`, the `/sc:impact` and `/sc:auggie-review` diff examples, release tooling (`/sc:post-release`, `release-procedure.md`), or any text that says master is the production branch. Change no ABSOLUTE RULE wording in `CLAUDE.md` other than branch names.
- Never stage `.claude/` mirrors (only `.claude/settings.json` is tracked); `.dev/tasks` is staged. Commit only on the feature branch with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- Follow-ups to list in the PR body, not fix here: the L1 command guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 59 text, line 736 `master | main`) still classifies only master and main as PROTECTED (the L2 hook is the backstop); release tooling that assumes master.
Start sha: 32b0e98738e39a2ef10629d21ef15a37e01567c5
Diff against the start snapshot: diff --git a/tests/hooks/test_launch_level_pre_push.py b/tests/hooks/test_launch_level_pre_push.py
index 57048589d..3b64d0472 100644
--- a/tests/hooks/test_launch_level_pre_push.py
+++ b/tests/hooks/test_launch_level_pre_push.py
@@ -46,7 +46,7 @@ def orca_module():
 
 P = "launch-level pre-push:"
 GATE = "<gate>"
-BRANCHES = ["main", "master"]
+BRANCHES = ["main", "master", "integration"]
 ACTORS = ["governed", "unknown", "human"]
 ROUTE = (
     "pre-push.launch-level and ~/.claude/hooks/launch-job-identity.sh) or "

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
