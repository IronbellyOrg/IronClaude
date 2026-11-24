ba95318dc5073899a2a0c3ae143eb5ebd9dfa080
Review one task for spec compliance.

Task brief: ## Task 3: Update the dispatcher docstring and the not_enabled reason

Depends on: Task 2

In `src/superclaude/cli/issue_watch/dispatch.py`, update the module docstring step 2 (lines 7-8) to say that a repository whose first-run report says the last attempt failed is retried on a later sweep (immediately for a `config` failure, after one hour for other steps), and change the `not_enabled` entry of `SKIP_REASONS` (line 66) to say the config is `enabled: false` because the first run did not pass and has not yet been retried successfully, or because the owner set it. Source requirement 6.

Acceptance criteria:
- T3.AC1: The docstring and the `SKIP_REASONS["not_enabled"]` text describe the retry rule and the one-hour delay.
- T3.AC2: `tests/issue_watch/test_dispatch.py` and `tests/issue_watch/test_cli.py` still pass; no test pins the old wording (checked with `grep -rn "did not pass, or the owner" tests src`).
Global constraints: ## Constraints

- Reuse the existing `first_run` function as the only setup path; do not add GitHub writes, label creation or store creation to `dispatch.py` or `cycle.py` (the boundary pinned by `tests/issue_watch/test_security_invariants.py` stays intact).
- Do not change the config schema (`_TOP_KEYS` in `src/superclaude/cli/issue_watch/cycle.py`) and do not change `ensure_config` in `src/superclaude/cli/issue_watch/generate.py`.
- A config with no first-run report, or whose report starts with `first-run: passed`, is never retried.
- A dry-run sweep makes no `first_run` call and writes no file.
- Do not edit anything under `.claude/`; change `src/` and `tests/` only.
Start sha: ba95318dc5073899a2a0c3ae143eb5ebd9dfa080
Diff against the start snapshot: 
```diff
diff --git a/src/superclaude/cli/issue_watch/dispatch.py b/src/superclaude/cli/issue_watch/dispatch.py
index 22bd264db..b1fde96d0 100644
--- a/src/superclaude/cli/issue_watch/dispatch.py
+++ b/src/superclaude/cli/issue_watch/dispatch.py
@@ -5,7 +5,9 @@ One cron entry runs a sweep. A sweep:
 1. lists the usable repositories with ``orca repo list`` (Task 18). A failed or unreadable list is
    an error result, never a clean one (R15);
 2. for a repository with no config, generates one (Task 19) and runs its first-run check (Task 21);
-   a repository whose config is not enabled is skipped with a reason, not run;
+   a repository whose config is not enabled is skipped with a reason, not run, except that one
+   whose first-run report says the last attempt failed is retried on a later sweep (at once for a
+   ``config`` step failure, after one hour for any other step; never on a dry run);
 3. starts ``superclaude issue-watch once --config <file>`` as a child process for each enabled
    repository, one after another, through the ``Runner`` (absolute paths only: cron has no PATH).
 
@@ -64,7 +66,7 @@ SKIP_REASONS: dict[str, str] = {
     "stopped_after_launch": "an earlier repo launched or attempted a launch this sweep",
     "loop_cap": "the 270 second loop cap was reached before this repo",
     "account_rate_wait": "a child hit the account rate limit; no child starts until its time",
-    "not_enabled": "the config is enabled: false (the first run did not pass, or the owner set it)",
+    "not_enabled": "the config is enabled: false (the first run did not pass and is retried on a later sweep, or the owner set it)",
     "config_unreadable": "the config file cannot be read as JSON",
     "config_invalid": "cycle.load_config refused the config (audit reason config_invalid)",
     "worktree_invalid": "the Coordinator worktree is not an existing directory (audit reason)",
```

Codegraph context
index_state: fresh
checked_at: 2026-11-24T02:39:04Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-751
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-751
call codegraph only when index_state: fresh, never to widen scope
Dependents not in the diff (Q2b): Only strings changed (module docstring lines 7-10 and SKIP_REASONS['not_enabled']); no code path changed; consumers of SKIP_REASONS text: none found in tests or src (grep of the old wording in .py files: 0 matches).

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
