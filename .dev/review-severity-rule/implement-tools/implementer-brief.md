# Implementer brief (same for every task; the orchestrator names the task number)

Repository root: /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (git worktree, branch fix/review-severity-rule).
Plan: .dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-053741/TASK-WF-removeTheAnyIssu-20261102-053741.md
Package artifacts dir (for logs the task asks you to save; `./artifacts/` in the plan means this dir):
.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-053741/artifacts/

Rules:
1. Read the plan's `## Constraints` section and your task section in full first. Implement ONLY your task: its body and its
   Acceptance criteria. Never make an edit the plan reserves for another task (e.g. a cap-edits.yaml `old` fragment belongs
   to Tasks 12-17, sweep-edits.yaml rows to Task 19). Smallest correct change; keep surrounding text, Markdown and quoting.
2. Site lists: `.dev/review-severity-rule/inventory.md`, `.dev/review-severity-rule/cap-edits.yaml`,
   `.dev/review-severity-rule/sweep-edits.yaml`. Locate sites by their quoted text (line numbers drift as tasks land).
   Canonical sentences S1-S5 are inventory section 1; after Task 1 copy them from `src/superclaude/output-styles/pragmatic.md`.
3. Edit only `src/superclaude/`, `plugins/superclaude/` twins, `tests/` and `CHANGELOG.md`. Never edit or stage `.claude/`
   (run `make sync-dev` to refresh it). Never commit, push or `git add`. Never run the full test suite or `tests/cli/eval/`
   as a directory. Python only through `uv run`. Prefix test runs with `PYTHONDONTWRITEBYTECODE=1`.
4. Never add a `src/superclaude/...` path to an installed primitive (agents, skills, commands, templates, rules, core,
   output-styles, hooks).
5. Run every check your Acceptance criteria name, exactly, and save each output where the criteria say
   (`... > <artifacts>/tN-x.log 2>&1; echo "rc=$?" >> <artifacts>/tN-x.log`). If a check fails, fix your own edits until it
   passes; if it fails for a reason outside your task, stop and report it with the failing output.
6. Do not read `.dev/tasks/to-do/<pkg>/artifacts/retries/` or `.dev/troubleshoot/`.
7. Final reply, under 25 lines: files changed; for each acceptance criterion the evidence as `path:line` (for logs, the
   line showing the outcome, e.g. the pytest summary line); anything you could not do and why.
