# Managed final review brief

## Governing review contract
Read `/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md`, sections `Managed FINAL review` and `FINAL derived test`, and `/home/coder/.claude/skills/sc-implement-protocol/refs/managed-workspace.md`, section `Completion: fresh FINAL, then archive`. These govern this review, including the protocol severity model in preference to the output style. This is one fresh independent final review, not a new planning, diagnosis or code-quality workflow.

## Inputs
Package root: `/home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff/.dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-185337`.
Read the current full `TASK-WF-planTheFixForIss-20261123-185337.md`, `source.md` and `progress.md`. Read `artifacts/final-state-before.json`; its `files` array is the complete current delivery list from the archive helper. Read the current contents of every listed delivery file. Paths in that list are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff`.
Read every saved prompt, review, probe, brief and notes file present under `artifacts/retries/`, plus `artifacts/superseded-prompts/` if it exists. Read the actual per-task review outputs at `artifacts/task-1-review.md` through `artifacts/task-4-review.md`, but never treat their conclusions as proof. The FINAL is explicitly allowed to read retries files. There are no delegated writers still running.

## Required review
Do not trust the implementer's report. Verify every task's acceptance criteria and the plan's Constraints against the real current source, tests, documentation and actual evidence logs, not copied ledger citations. An archived historical diagnosis does not prove a repaired-state outcome; do not rewrite it or follow its old shared-checkout paths. Judge each required log outcome against the actual criterion that requested it. A moved citation alone is not an issue. Apply the protocol's four blocking questions, anchor Read-back and FINAL derived test to any finding. Notes with all four answers no do not produce issues; confirmed blocking defects do.
Compare saved per-task prompt text after its first hash line and outside its seven filled slots with the closed template under `Subagent prompt` in the live qa.md. Ignore only blank-line/trailing-whitespace differences. The graph-context block is part of the diff slot. Check any superseded-prompt history if present, per the governing contract.
The repaired CLI capture is under `artifacts/repaired-cli/`: check its complete suggested command and actual readable report inputs against the shipped consumer, without invoking the suggestion. Do not access the original shared checkout. Historical absolute paths inside copied reports or saved test/CLI captures are provenance, not lookup instructions.
Do not implement, alter delivery files or ledger, stage, commit, push, run paid/model-backed reviews, create workers/worktrees, or execute the emitted comparison. Do not re-run the full test suite as this review. Targeted read-only checks are allowed.

## Graph context
index_state: fresh
checked_at: 2026-11-23T20:00:21Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
call codegraph only when index_state: fresh, never to widen scope
The run has changed these files since that initial readiness check; graph rows are leads only and require direct source verification. Grep/Read is sufficient here. Do not run another readiness check or index command.

## Output
Write only `<package root>/artifacts/final-review.md`. Read the governing review sections first, then immediately create the report header and full section skeleton before collecting findings. Derive the report structure from that contract: Verdict (`pass` or `issues`), per-task Acceptance checks with current path:line evidence for every AC, Constraints and saved prompts, Findings (four checklist answers and one valid anchor per yes), and Scope and limits. Populate it incrementally. A zero-finding result must state what was checked and why the criteria are met. Return only the report path. The parent will consume the file and recheck the helper state before archiving; you must not archive.
