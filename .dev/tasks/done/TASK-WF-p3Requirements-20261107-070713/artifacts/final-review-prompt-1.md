Managed FINAL review (archive gate) for one workflow package.

Do not trust the implementer's report. Start from the assumption that mistakes exist and try to find them. You have read-only tools (Read, Grep, Glob); you cannot run commands.

Repository root: /home/coder/workspaces/worktrees/IronClaude/issue-361-late-conflict-resync
Package root: /home/coder/workspaces/worktrees/IronClaude/issue-361-late-conflict-resync/.dev/tasks/to-do/TASK-WF-p3Requirements-20261107-070713

Read in full:
1. The plan: <package>/TASK-WF-p3Requirements-20261107-070713.md (10 tasks; read its "## Constraints" section and every task's "Acceptance criteria:").
2. The ledger: <package>/progress.md (every task must have a "complete" line; check the latest "PLAN:" pin is above the first "start" line).
3. The current contents of every delivery file below (they are the end state; judge the end state, not the history).
4. The package logs: every file under <package>/artifacts/retries/ (notes.md, probe-*.md, review-*.md, prompt-*-*.md, q0-head, briefs) and <package>/artifacts/superseded-prompts/ if it exists.
5. The rules: /home/coder/.claude/skills/sc-implement-protocol/refs/qa.md, sections "Severity model", "FINAL derived test" and "Managed FINAL review (archive gate)". Apply them exactly. Only a confirmed blocking defect is "issues". Minor findings and notes are recorded as notes, never "issues".

Delivery files (the helper's state list):
CHANGELOG.md
docs/user-guide/commands.md
docs/user-guide/flags.md
src/superclaude/commands/pr-submit.md
src/superclaude/pr_submit/__init__.py
src/superclaude/pr_submit/conflicts.py
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md
src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
tests/pr_submit/test_ci_classify.py
tests/pr_submit/test_conflict_scripts.py
tests/pr_submit/test_conflict_sync_protocol.py
tests/pr_submit/test_conflicts_core.py
tests/pr_submit/test_static_grep.py
tests/skills/test_worker_contract.py

For each of the 10 tasks, verify every acceptance criterion against the real current files and cite path:line evidence from the current files or the package logs (not copied from the ledger). A moved line number alone is never "issues". Return "issues" when an acceptance criterion is unmet at the end state, no evidence can be found, a later change contradicts it, a plan Constraints item is violated, or a log cited on a task's latest "complete" line shows a failure at its outcome line.

Also check:
- Saved prompts: for each <package>/artifacts/retries/T<id>/prompt-<k>-<j>.md, line 1 is the task's start sha; the lines after it, outside the slots, must match the reviewer template in refs/qa.md (blank-line differences are a note).
- Every task with a blocking review finding has a later fix and a passing re-review recorded.
- The plan Constraints carry an owner-authorization bullet: the owner (via the Orca coordinator, 2026-11-07) authorized two word-level corrections and minor guardrails applied in place to the plan and source.md after the 3-review cap, with no new review. That authorization is a recorded fact, not a defect. Check that the corrections do not contradict the end state.
- Delivery files must not contain: "sync_cycles" anywhere under src; "#361" in refs/conflict-mechanical.md; the phrase "is #361" in CHANGELOG.md.
- No change to src/superclaude/pr_submit/fsm.py, run_log.py, models.py or ci.py (Constraints).

Output format:
1. "Verdict: pass" or "Verdict: issues".
2. Per task T1..T10: each AC with met/unmet and a path:line citation.
3. Findings, one per line, each: "F<n> severity=blocking|minor|note at=<path:line> anchor=<quoted text you read> chk=<four y/n answers per the checklist in refs/qa.md> : <statement>".
4. A short Self-Audit naming what you actively checked.
5. Then stop. Do not write any file.
