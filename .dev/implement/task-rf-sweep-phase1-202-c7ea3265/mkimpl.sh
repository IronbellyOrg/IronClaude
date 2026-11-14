#!/usr/bin/env bash
# Build the implementer prompt for a task: mkimpl.sh Tn "<extra instructions>"  -> prints the prompt file path
set -u
D=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
id=$1; extra=${2:-}
out=$D/work/$id/impl-prompt.md
{
cat <<'EOT'
You are the implementer for ONE task of a plan being executed with a per-task spec-compliance review. Do exactly the task below, nothing more. Another agent will review your work from the files on disk afterwards, so make the files and result records true.

Repository root: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode (a git worktree; run every command from there). Use `uv run` for every Python command (never bare `python`, `python3`, `python -m` or `pip`). Read files in chunks of at most 150 lines. Never commit, push, merge or stage a `.claude/` path; never run a live Orca, ccsession or Claude command (tests use the seam fakes). Never edit `docs/designs/orchestrator-mode.md`, the SPEC, the task file's item text or any QA report. The plan file is `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; its `### Key Constraints` section (lines 157-168) binds you. Do not tick the item's checkbox and do not edit the Execution Log (the orchestrator does both).

The task item (copied from the plan file; the item's Verification and Completion gate lines tell you what "done" means):
-----
EOT
sed -n '2,$p' "$D/work/$id/brief.txt" | sed '/^AC ids:/,$d'
cat <<'EOT'
-----
Rules for a test-writing task: write real tests, one per listed DESIGN case (a parametrized case counts), that assert the exact values DESIGN states (class names and note strings byte-exact). If a test exposes a bug in `src/superclaude/cli/sweep/`, fix the code (not the test) with the smallest change that follows DESIGN, and list each such fix with its file:line in your final message so the orchestrator can log it in `### Phase 10 Findings`. A DESIGN conflict you cannot close from DESIGN alone: leave the test marked `pytest.mark.xfail(strict=True, reason=...)` only if the item allows it, otherwise stop and report it. Run `uv run ruff format` on the test files you create or edit and `uv run ruff check src/superclaude/cli/sweep tests/sweep` before you finish. Create each result file as a header stub first, then fill it; a result file holds the real pytest stdout plus the case-to-test map, never a summary written from memory.
EOT
printf '%s\n' "$extra"
cat <<'EOT'

Final message: list the files you created or edited, each code fix (file:line and why), the exact pytest command and its pass count, and anything you could not do. Do not claim anything you did not run.
EOT
} > "$out"
echo "$out"
