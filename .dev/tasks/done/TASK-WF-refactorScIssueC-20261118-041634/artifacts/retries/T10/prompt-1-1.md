69e7d98e931420049c5235a37dd9b4eec76db816
Review one task for spec compliance.

Task brief: ## Task 10: Sync the dev copies
Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Run `make sync-dev` so the gitignored `.claude/` copies of the edited command and skill files match `src/superclaude/`. Stage the `src/`, `tests/`, `docs/` and `plugins/` paths you changed and always `git add .dev/tasks`; never `git add` anything under `.claude/`.
Acceptance criteria (ids):
T10.AC1: `make verify-sync` exits 0.
T10.AC2: `git status --short` lists no path under `.claude/` as staged and shows `.dev/tasks` staged.
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
Start sha: 69e7d98e931420049c5235a37dd9b4eec76db816
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/artifacts/t10-evidence.log b/.dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/artifacts/t10-evidence.log
new file mode 100644
index 000000000..cf0fab3eb
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/artifacts/t10-evidence.log
@@ -0,0 +1,8 @@
+# T10 evidence (orchestrator ran these)
+make verify-sync:
+
+✅ All components in sync.
+exit=0
+staged paths under .claude/: 0
+staged .dev/tasks files: 37
+unstaged .dev/tasks changes: 1

--- new file .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/artifacts/t10-evidence.log (full contents) ---
# T10 evidence (orchestrator ran these)
make verify-sync:

✅ All components in sync.
exit=0
staged paths under .claude/: 0
staged .dev/tasks files: 37
unstaged .dev/tasks changes: 1


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
