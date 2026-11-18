a9eb8f0f62ba7ec69d91f5e22e96dee0d41baac4
Review one task for spec compliance.

Task brief: ## Task 9: Sync the dev copies and stage the changes
Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8

Run `make sync-dev` so the gitignored `.claude/` copies of the edited command and skill files match `src/superclaude/`. Stage the `src/`, `tests/`, `docs/` and `plugins/` paths this plan changed and always `git add .dev/tasks`; never `git add` anything under `.claude/`.
Acceptance criteria (ids):
T9.AC1: `make verify-sync` exits 0, and its result is saved under `./artifacts/t9-evidence.log`.
T9.AC2: `uv run pytest tests/commands/test_issue_command.py tests/skills/test_issue_protocol.py tests/skills/test_model_alias_policy.py tests/skills/test_worker_contract.py tests/issue_watch -v` passes, with its result in `./artifacts/t9-evidence.log`.
T9.AC3: `git status --short` lists no path under `.claude/` as staged and shows `.dev/tasks` staged.
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
Start sha: a9eb8f0f62ba7ec69d91f5e22e96dee0d41baac4
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-refactorTheScIss-20261118-054817/artifacts/t9-evidence.log b/.dev/tasks/to-do/TASK-WF-refactorTheScIss-20261118-054817/artifacts/t9-evidence.log
new file mode 100644
index 000000000..3739929bc
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-refactorTheScIss-20261118-054817/artifacts/t9-evidence.log
@@ -0,0 +1,15 @@
+# T9 evidence (orchestrator ran these)
+make sync-dev:
+   Hooks:     17 files
+   Templates: 52 files
+make verify-sync:
+
+✅ All components in sync.
+verify-sync exit=0
+tests:
+
+============================ 3604 passed in 24.96s =============================
+staging:
+staged paths under .claude/: 0
+staged .dev/tasks files for this package: 27
+unstaged .dev/tasks changes: 0

--- new file .dev/tasks/to-do/TASK-WF-refactorTheScIss-20261118-054817/artifacts/t9-evidence.log (full contents) ---
# T9 evidence (orchestrator ran these)
make sync-dev:
   Hooks:     17 files
   Templates: 52 files
make verify-sync:

✅ All components in sync.
verify-sync exit=0
tests:

============================ 3604 passed in 24.96s =============================
staging:
staged paths under .claude/: 0
staged .dev/tasks files for this package: 27
unstaged .dev/tasks changes: 0


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
