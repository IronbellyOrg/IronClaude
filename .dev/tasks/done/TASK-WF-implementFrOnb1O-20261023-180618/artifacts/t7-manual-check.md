# Manual follow-up for the user (spec FR-ONB.1 manual check)

This check needs a fresh Claude session with the updated IronClaude installed, so the plan's executor cannot run it.

1. Install the change: from the IronClaude checkout that has this branch, run `uv run superclaude update` (or `superclaude install --force`). This overwrites `~/.claude/` files it ships; back up any you edited first.
2. Start a new Claude session in any project.
3. Run exactly:

   `/sc:recommend "Add CSV export to the invoices list; touches 6 files; spec at docs/specs/x.md"`

4. Expected result: it recommends `/sc:workflow` (then `/sc:implement`), matching routing row `feature-existing` or `simple-plan` (level 3). It must NOT recommend `/task-builder` or `/task`.

A static walk-through of the same request through the edited match rules is in ./t4-recommend-walk.md (result: feature-existing, level 3).
