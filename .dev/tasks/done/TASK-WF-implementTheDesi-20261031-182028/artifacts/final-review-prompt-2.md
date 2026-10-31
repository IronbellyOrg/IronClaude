Managed FINAL review (archive gate) for the /sc:implement package at /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028.

Do not trust the implementer's report.

Inputs (read the real current files; paths are absolute):
- Plan (with ## Constraints): /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md
- Ledger: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/progress.md
- Package root for ./artifacts/ tokens: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028 (logs in /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/)
- Retry folders to read in full: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/retries/T*/ (review-*.md, repair-*.md, probe-*.md, prompt-*.md, notes.md, advice-*, approach-*, attempt-*.diff) and briefs /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/retries/T*_brief-*.md
- Specification: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex/.dev/pr-submit-codex/design/pr-submit-codex-design.md (section 18 amendments A0-A5 override earlier text; the ledger's T2 Ruling line records a coordinator ruling)
- Reviewer template the saved prompts must match outside their slots: /home/coder/.claude/skills/sc-implement-protocol/refs/qa.md section 'Subagent prompt (when not inline)' (the first line of each prompt file is the task's start sha, which the protocol requires)
- Delivery files (current contents, repo root /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex):
  - CHANGELOG.md
  - CLAUDE.md
  - docs/guides/prd-skill-release-guide.md
  - docs/guides/tdd-skill-release-guide.md
  - docs/user-guide/commands.md
  - src/superclaude/commands/pr-submit.md
  - src/superclaude/pr_submit/__init__.py
  - src/superclaude/pr_submit/classifier.py
  - src/superclaude/pr_submit/detection.py
  - src/superclaude/pr_submit/models.py
  - src/superclaude/pr_submit/reviewers.py
  - src/superclaude/pr_submit/run_log.py
  - src/superclaude/pr_submit/severity_router.py
  - src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
  - src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh
  - src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
  - src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh
  - tests/pr_submit/fixtures/codex-clean-pr334.json
  - tests/pr_submit/fixtures/codex-findings-pr336.json
  - tests/pr_submit/test_codex_reviews.py
  - tests/pr_submit/test_cosmos_protocol.py
  - tests/pr_submit/test_detection_contract.py
  - tests/pr_submit/test_run_log.py

Task: for every task T1-T15 in the plan, verify each acceptance criterion against the current files and the package's ./artifacts/ logs, and return pass or issues with path:line evidence per task AC (not copied from the ledger; a moved line number alone is never issues). Return issues when an AC is unmet at the end state, no evidence can be found, a later change contradicts it, a plan ## Constraints item is violated, or a log cited on a task's latest complete line shows a failure at its outcome line. Also judge the retry folders and briefs against the plan, and compare each saved prompt-<k>-<j>.md with the reviewer template (issues when they differ outside the slots).

Severity (from refs/qa.md, which governs this review and takes precedence over any output style): only a blocking defect at the end state makes the result issues. For every defect you find, answer four questions yes/no: (1) ac-outcome-missing (an AC's required output is absent or contradicted), (2) false-claim (a claim in delivered text or code is false against live source), (3) harmful-effect (delivered code or recipe writes/deletes data or exposes a secret beyond its declared outputs), (4) quoted-constraint-breach (the end state violates a quoted plan constraint or task instruction). Cite exactly one anchor per yes (the quoted AC words; the live-source path:line holding the contradicting text; the write line; the quoted constraint). A defect with any anchored yes is blocking; all-no defects are noted, never issues. A notes.md entry whose answers are all no is noted, not an unmet AC; a review-*.md blocking line later marked resolved, and a notes line prefixed 'superseded ', are history: judge the end state.

Output, exactly:
RESULT: pass|issues
One line per task AC: Ti.ACk met|unmet at=<path:line>
One line per defect: D<n> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n>: <text>
Then a short self-audit naming what you checked.

Note: this is the second archive attempt. The first FINAL (artifacts/final-review-1.md) returned issues for two false sentences; Task 2 and Task 12 were reopened by operator ruling (Ruling lines in the ledger) to correct exactly those sentences. Judge the current end state afresh.
