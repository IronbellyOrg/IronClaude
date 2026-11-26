4352094c0e6e9e26bb82ed1442abb25beedabc04
Review one task for spec compliance.

Task brief: ## Task 3: Default the reflect base branch to integration

Edit `src/superclaude/cli/reflect/config.py`: `_DEFAULT_BASE_BRANCH = "integration"` (line 44), rewrite the OQ1 comment above it (lines 40-43, which says the trunk is master and integration must not be hardcoded) to say the default branch is now integration, and fix the docstring mentions of `master` at line 13 of the module and line 281 (`base_branch` argument). No helper that resolves the repository default branch exists (`_resolve_base` only runs `git merge-base HEAD <base_branch>`), so the constant is the single source. The only reader is `resolve_config(... base_branch=_DEFAULT_BASE_BRANCH)` at line 259 feeding `_resolve_base` (line 312); `tests/cli/reflect/test_cli_smoke.py` and `test_base_precedence.py` mock `_git` and do not depend on the value.

Acceptance criteria (ids):
T3.AC1: `grep -n "master" src/superclaude/cli/reflect/config.py` finds no statement that master is the default base.
T3.AC2: `uv run pytest tests/cli/reflect -q` passes.
Global constraints: - One pull request, base `integration`, branch `fix/default-branch-integration`, opened only through `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`. Never merge, never touch SuperClaude-Org, no Orca link flags, no model flag, never Opus.
- Edit only `src/superclaude/**`, `tests/**`, `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (a committed byte-identical mirror with no generator: `scripts/build_superclaude_plugin.py` writes `dist/` only) and the two root files `CLAUDE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
- Do not touch `docs/generated`, `docs/testing`, the `/sc:impact` and `/sc:auggie-review` diff examples, release tooling (`/sc:post-release`, `release-procedure.md`), or any text that says master is the production branch. Change no ABSOLUTE RULE wording in `CLAUDE.md` other than branch names.
- Never stage `.claude/` mirrors (only `.claude/settings.json` is tracked); `.dev/tasks` is staged. Commit only on the feature branch with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- Follow-ups to list in the PR body, not fix here: the L1 command guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 59 text, line 736 `master | main`) still classifies only master and main as PROTECTED (the L2 hook is the backstop); release tooling that assumes master.
Start sha: 4352094c0e6e9e26bb82ed1442abb25beedabc04
Diff against the start snapshot: diff --git a/src/superclaude/cli/reflect/config.py b/src/superclaude/cli/reflect/config.py
index 5c716c8be..53acc5939 100644
--- a/src/superclaude/cli/reflect/config.py
+++ b/src/superclaude/cli/reflect/config.py
@@ -10,7 +10,7 @@ Isolation guardrails:
 - Imports nothing from ``commands.py`` / ``runner.py`` / ``contract.py``.
 
 FR-3 input derivation, FR-4 pinned output dir + ``.claude`` STOP, G1 max_turns
-default (Open Question OQ6), OQ1 base-branch default ``master``.
+default (Open Question OQ6), OQ1 base-branch default ``integration``.
 """
 
 from __future__ import annotations
@@ -38,10 +38,10 @@ _DEFAULT_TIMEOUT_SECONDS = 3600
 # ``--max-turns`` flag in v1 (keeps the spec Section 9 option set exact).
 _DEFAULT_MAX_TURNS = 250
 
-# OQ1 (LOAD-BEARING): the project trunk is ``master`` (origin/HEAD -> master);
-# an ``integration`` branch also exists but hardcoding it would compute the
-# WRONG base. Make it a parameter defaulting to ``master``, never hardcode.
-_DEFAULT_BASE_BRANCH = "master"
+# OQ1 (LOAD-BEARING): since 2026-11-24 the repository default (and PR base)
+# branch is ``integration``; ``master`` stays the production branch and would
+# compute the WRONG base. Keep it a parameter defaulting to ``integration``.
+_DEFAULT_BASE_BRANCH = "integration"
 
 # FR-4 STOP: an ``--output`` resolving under any of these ``.claude`` subtrees
 # is a reflect STOP condition -- reject before launch.
@@ -278,7 +278,7 @@ def resolve_config(
         max_turns: Per-process turn ceiling (G1; default 250, never None).
         promote / allow_single_vendor / tmux / dry_run / print_command /
         resume: wrapper-side flags threaded through to the runner.
-        base_branch: base for ``git merge-base`` fallback (default ``master``).
+        base_branch: base for ``git merge-base`` fallback (default ``integration``).
         transport: Tier-2 worker transport (``openai_compat`` or ``stub``).
         reviewers: Tier-2 reviewer slots; ``1`` is preserved as the negative
             witness, otherwise values are clamped to ``[2,4]``.

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
